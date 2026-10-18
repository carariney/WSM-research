"""Local, semi-adjustable WSM pro-forma workbench.

Run from the repository root with ``python3 wsm_workbench.py`` and open
http://127.0.0.1:8000.  This interface imports the validated model directly;
it does not maintain a second set of forecast or valuation calculations.
"""
from __future__ import annotations

from copy import deepcopy
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import wsm_proforma as model


HOST, PORT = "127.0.0.1", 8000
BASE = deepcopy(model.BASE_INPUTS)

# Bounds are intentionally narrower than a broad stress test. They keep the
# interactive panel tied to the disclosed challenge ranges and prevent casual
# use from producing an incoherent forecast. The separate validation demo
# safely shows an invalid discount-rate/growth relationship without modifying
# the underlying engine or the base case.
BOUNDS = {
    "fy2026_growth": (0.0395, 0.0795),
    "gross_margin": (0.435, 0.475),
    "wacc": (0.09, 0.11),
    "terminal_growth": (0.02, 0.04),
}


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def parse_inputs(query: dict[str, list[str]]) -> dict[str, object]:
    """Apply only exposed, bounded controls to a fresh base-case input set."""
    inputs = deepcopy(BASE)

    def control(name: str, base_value: float) -> float:
        raw = query.get(name, [str(base_value)])[0]
        try:
            value = float(raw)
        except ValueError:
            value = base_value
        lower, upper = BOUNDS[name]
        return clamp(value, lower, upper)

    growth = list(inputs["revenue_growth"])
    growth[0] = control("fy2026_growth", growth[0])
    inputs["revenue_growth"] = tuple(growth)
    inputs["gross_margin"] = control("gross_margin", float(inputs["gross_margin"]))
    inputs["wacc"] = control("wacc", float(inputs["wacc"]))
    inputs["cost_of_equity"] = inputs["wacc"]
    inputs["terminal_growth"] = control("terminal_growth", float(inputs["terminal_growth"]))
    return inputs


def compact_rows(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    fields = ("year", "revenue", "gross_profit", "operating_income", "net_income",
              "cash", "inventory", "ppe", "assets", "equity", "fcff", "fcfe", "gap")
    return [{field: row[field] for field in fields} for row in rows]


def case_result(inputs: dict[str, object], label: str, changed: dict[str, object]) -> dict[str, object]:
    tested = deepcopy(inputs)
    tested.update(changed)
    rows = model.project(tested)
    valuation = model.value_fcff(rows, tested)
    return {"case": label, "fy2030_operating_income": rows[-1]["operating_income"],
            "fy2030_fcff": rows[-1]["fcff"], "per_share": valuation["per_share"]}


def sensitivity(inputs: dict[str, object]) -> dict[str, list[dict[str, object]]]:
    growth = list(inputs["revenue_growth"])
    low_growth = growth.copy(); low_growth[0] = max(BOUNDS["fy2026_growth"][0], growth[0] - 0.02)
    high_growth = growth.copy(); high_growth[0] = min(BOUNDS["fy2026_growth"][1], growth[0] + 0.02)
    gross = float(inputs["gross_margin"])
    return {
        "FY2026 revenue growth": [
            case_result(inputs, "Low", {"revenue_growth": tuple(low_growth)}),
            case_result(inputs, "Base", {"revenue_growth": tuple(growth)}),
            case_result(inputs, "High", {"revenue_growth": tuple(high_growth)}),
        ],
        "Gross margin": [
            case_result(inputs, "Low", {"gross_margin": max(BOUNDS["gross_margin"][0], gross - 0.02)}),
            case_result(inputs, "Base", {"gross_margin": gross}),
            case_result(inputs, "High", {"gross_margin": min(BOUNDS["gross_margin"][1], gross + 0.02)}),
        ],
    }


def checks(inputs: dict[str, object], rows: list[dict[str, float]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for name, check in (
        ("Base-year reconciliation", model.assert_base_year_reconciliation),
        ("Enterprise-to-equity bridge", lambda: model.assert_valuation_reconciliation(rows, inputs)),
        ("DCF directionality", lambda: model.assert_dcf_directionality(rows, inputs)),
    ):
        try:
            check()
            results.append({"name": name, "status": "PASS", "detail": "Validated by the existing model."})
        except ValueError as error:
            results.append({"name": name, "status": "FAIL", "detail": str(error)})
    articulation = all(abs(row["gap"]) <= 0.05 and row["cash"] >= 0 for row in rows)
    results.append({"name": "Five-year articulation", "status": "PASS" if articulation else "FAIL",
                    "detail": "All annual balance-sheet gaps are within $0.05M and cash remains nonnegative."
                    if articulation else "A balance-sheet gap or negative cash was detected."})
    return results


def run_model(query: dict[str, list[str]]) -> dict[str, object]:
    inputs = parse_inputs(query)
    rows = model.project(inputs)
    valuation = model.value_fcff(rows, inputs)
    validation_demo = query.get("demo", ["pass"])[0]
    demo = {"status": "PASS", "detail": "Base validation example: WACC exceeds terminal growth."}
    if validation_demo == "invalid":
        invalid = deepcopy(inputs)
        invalid["wacc"], invalid["cost_of_equity"], invalid["terminal_growth"] = 0.03, 0.03, 0.04
        try:
            model.value_fcff(rows, invalid)
        except ValueError as error:
            demo = {"status": "FAIL (intentional and safe)", "detail": str(error)}
        else:
            demo = {"status": "UNEXPECTED", "detail": "The incoherent valuation did not fail as expected."}
    return {
        "valuation_date": model.VALUATION_DATE,
        "market_price": model.MARKET_PRICE,
        "inputs": {
            "fy2026_growth": inputs["revenue_growth"][0], "gross_margin": inputs["gross_margin"],
            "wacc": inputs["wacc"], "terminal_growth": inputs["terminal_growth"],
        },
        "rows": compact_rows(rows),
        "valuation": {**valuation,
                      "reverse_dcf_growth": model.solve_market_implied_terminal_growth(rows, inputs)},
        "checks": checks(inputs, rows),
        "sensitivity": sensitivity(inputs),
        "validation_demo": demo,
    }


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WSM Pro-Forma Workbench</title><style>
body{font-family:Arial,sans-serif;margin:0;background:#f4f7f9;color:#142735}header{background:#142735;color:white;padding:20px 5%;}main{max-width:1280px;margin:24px auto;padding:0 20px}.layout{display:grid;grid-template-columns:275px 1fr;gap:20px}.card{background:white;border:1px solid #ccd6dc;border-radius:7px;padding:16px;margin-bottom:16px}h1{margin:0;font-size:28px}h2{font-size:19px;margin-top:0}h3{font-size:16px}.muted{color:#52616b;font-size:14px}.control{margin:14px 0}.control label{display:block;font-weight:bold;margin-bottom:5px}.control output{float:right}.control input{width:100%}button{background:#285e8e;color:white;border:0;border-radius:4px;padding:9px 12px;margin:3px 0;cursor:pointer}.secondary{background:#607783}.fail{background:#a33636}.grid{display:grid;grid-template-columns:repeat(4,minmax(130px,1fr));gap:10px}.metric{background:#edf3f6;padding:11px;border-radius:4px}.metric b{display:block;font-size:20px}table{border-collapse:collapse;width:100%;font-size:13px}th{background:#142735;color:white}th,td{padding:7px;border:1px solid #ccd6dc;text-align:right}th:first-child,td:first-child{text-align:left}.pass{color:#1d6b3a;font-weight:bold}.bad{color:#a33636;font-weight:bold}.notice{padding:10px;border-radius:4px}.notice.pass{background:#e8f5ed}.notice.bad{background:#fae9e9}@media(max-width:800px){.layout{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><h1>Williams-Sonoma Pro-Forma Workbench</h1><div>Local interface using <code>wsm_proforma.py</code> directly. USD millions except per-share values.</div></header><main><div class="layout"><aside class="card"><h2>Driver Panel</h2><p class="muted">Bounded controls use the disclosed sensitivity ranges. Reset restores the validated base case.</p>
<div class="control"><label>FY2026 revenue growth <output id="growthOut"></output></label><input id="growth" type="range" min="3.95" max="7.95" step="0.05" value="5.95"></div>
<div class="control"><label>Gross margin <output id="marginOut"></output></label><input id="margin" type="range" min="43.5" max="47.5" step="0.1" value="45.5"></div>
<div class="control"><label>WACC <output id="waccOut"></output></label><input id="wacc" type="range" min="9" max="11" step="0.1" value="10"></div>
<div class="control"><label>Terminal growth <output id="terminalOut"></output></label><input id="terminal" type="range" min="2" max="4" step="0.1" value="3"></div>
<button onclick="loadModel()">Run Workbench</button><button class="secondary" onclick="resetBase()">Reset Base Case</button><hr><h3>Safe Failing-Check Demo</h3><p class="muted">This does not change statements. It asks the engine to value an incoherent case where terminal growth exceeds WACC.</p><button class="fail" onclick="loadModel('invalid')">Show Invalid Valuation Check</button><button class="secondary" onclick="loadModel('pass')">Recover Passing Check</button></aside>
<section><div class="card"><h2>Decision Snapshot</h2><div id="snapshot" class="grid"></div><p class="muted">Recommendation remains Watch/Defer; this workbench shows scenario mechanics, not a new recommendation.</p></div>
<div class="card"><h2>Visible Checks</h2><div id="demo"></div><table><thead><tr><th>Check</th><th>Status</th><th>Result</th></tr></thead><tbody id="checks"></tbody></table></div>
<div class="card"><h2>Five-Year Linked Financial Statements</h2><div style="overflow-x:auto"><table><thead><tr><th>Metric</th><th>FY2026E</th><th>FY2027E</th><th>FY2028E</th><th>FY2029E</th><th>FY2030E</th></tr></thead><tbody id="statements"></tbody></table></div></div>
<div class="card"><h2>One-at-a-Time Sensitivity Outputs</h2><p class="muted">Each comparison changes only the named driver from the current workbench case; other displayed inputs remain fixed.</p><div id="sensitivities"></div></div>
</section></div></main><script>
const ids=['growth','margin','wacc','terminal']; const outs=['growthOut','marginOut','waccOut','terminalOut'];
function fmt(n,d=1){return Number(n).toLocaleString(undefined,{minimumFractionDigits:d,maximumFractionDigits:d})} function pct(n){return fmt(n*100,1)+'%'}
function sync(){document.getElementById('growthOut').textContent=document.getElementById('growth').value+'%';document.getElementById('marginOut').textContent=document.getElementById('margin').value+'%';document.getElementById('waccOut').textContent=document.getElementById('wacc').value+'%';document.getElementById('terminalOut').textContent=document.getElementById('terminal').value+'%'} ids.forEach(id=>document.getElementById(id).addEventListener('input',sync));
function resetBase(){[['growth',5.95],['margin',45.5],['wacc',10],['terminal',3]].forEach(([id,v])=>document.getElementById(id).value=v);sync();loadModel('pass')}
async function loadModel(demo='pass'){const q=new URLSearchParams({fy2026_growth:document.getElementById('growth').value/100,gross_margin:document.getElementById('margin').value/100,wacc:document.getElementById('wacc').value/100,terminal_growth:document.getElementById('terminal').value/100,demo});const r=await fetch('/api/model?'+q);const d=await r.json();render(d)}
function render(d){const v=d.valuation;document.getElementById('snapshot').innerHTML=`<div class="metric">FCFF value/share<b>$${fmt(v.per_share,2)}</b></div><div class="metric">Market price<b>$${fmt(d.market_price,2)}</b></div><div class="metric">Enterprise value<b>$${fmt(v.enterprise_value,1)}M</b></div><div class="metric">Terminal-value share<b>${pct(v.terminal_share)}</b></div>`; const bad=d.validation_demo.status.startsWith('FAIL');document.getElementById('demo').innerHTML=`<p class="notice ${bad?'bad':'pass'}"><b>${d.validation_demo.status}:</b> ${d.validation_demo.detail}</p>`;document.getElementById('checks').innerHTML=d.checks.map(c=>`<tr><td>${c.name}</td><td class="${c.status==='PASS'?'pass':'bad'}">${c.status}</td><td>${c.detail}</td></tr>`).join('');const rows=[['Revenue','revenue'],['Gross profit','gross_profit'],['Operating income','operating_income'],['Net income','net_income'],['Cash','cash'],['Inventory','inventory'],['PP&E, net','ppe'],['Total assets','assets'],['Equity','equity'],['FCFF','fcff'],['FCFE','fcfe'],['Balance-sheet gap','gap']];document.getElementById('statements').innerHTML=rows.map(([label,key])=>`<tr><td>${label}</td>${d.rows.map(x=>`<td>${fmt(x[key])}</td>`).join('')}</tr>`).join('');document.getElementById('sensitivities').innerHTML=Object.entries(d.sensitivity).map(([name,cases])=>`<h3>${name}</h3><table><thead><tr><th>Case</th><th>FY2030 Operating Income</th><th>FY2030 FCFF</th><th>Value/Share</th></tr></thead><tbody>${cases.map(c=>`<tr><td>${c.case}</td><td>$${fmt(c.fy2030_operating_income)}M</td><td>$${fmt(c.fy2030_fcff)}M</td><td>$${fmt(c.per_share,2)}</td></tr>`).join('')}</tbody></table>`).join('')}
sync();loadModel();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/model":
            try:
                payload = json.dumps(run_model(parse_qs(parsed.query))).encode("utf-8")
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(payload)
            except (ValueError, KeyError) as error:
                self.send_error(400, str(error))
            return
        if parsed.path in ("/", "/index.html"):
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(HTML.encode("utf-8")); return
        self.send_error(404, "Not found")

    def log_message(self, format: str, *args: object) -> None:
        print("workbench:", format % args)


if __name__ == "__main__":
    print(f"WSM workbench: http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
