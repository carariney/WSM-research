# Williams-Sonoma Project 1 Model

## Decision and output

This locally runnable model supports a buy-side decision on whether to initiate WSM as of August 31, 2026. The current model output is a **watch/defer** conclusion, not investment advice. The integrated base FCFF/WACC value is $138.88 per common share; the combined operating downside/base/high FCFF range is $123.00-$156.69 per share. `output/visible_final_results.json` exposes the dated inputs, results, and action without running code.

## Run

No credentials or third-party packages are required with Python 3. Run from the repository root:

```bash
python3 validate_wsm_model.py
python3 wsm_proforma.py
python3 lab08_wsm_pe_comps.py
python3 wsm_workbench.py
```

## Files

- `wsm_proforma.py` — five-year linked statements, FCFF/FCFE reconciliation, FCFF DCF, WACC-growth sensitivity, integrated scenarios, and validation assertions.
- `validate_wsm_model.py` — synthetic known-answer and final-model validation suite.
- `lab08_wsm_pe_comps.py` — P/E and EV/EBIT peer calculations.
- `wsm_workbench.py` — local, semi-adjustable browser workbench that calls `wsm_proforma.py` directly; see `docs/wsm-workbench.md`.
- `docs/WSM_Final_Valuation_and_Validation.md` — dated conventions, sources, results, and limitations.
- `Lab06_WSM.md`, `Lab08_WSM_PE_Comps.md`, `Lab10_WSM_ProForma.md`, and `Lab11_WSM_Sensitivity.md` — research and historical lab evidence.

## Important conventions and limitations

The model uses a 10.0% WACC/cost of equity, 3.0% terminal growth, $1,028.936M reported cash, zero financial debt, and 117.779173M shares. It treats all reported cash as non-operating in the base case and excludes operating and finance lease liabilities from debt. A 0%/50%/100% cash sensitivity returns $130.15/$134.51/$138.88 per share; the August 31 market price implies 6.28% terminal growth when all base operating assumptions remain fixed. These are disclosed conventions requiring final student judgment; they are not facts established by the model. The historical market price, forecast assumptions, and peer balance-sheet dates are explicitly dated in the linked documentation.
