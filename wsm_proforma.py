"""Five-year WSM pro forma, FY2026E-FY2030E (USD millions except per-share data).

Opening balance sheet: WSM Form 10-Q at August 2, 2026.  FY2025 revenue is
the full-year base. Forecast inputs labeled JUDGMENT are transparent model
choices, not reported company guidance.
"""

from __future__ import annotations

from copy import deepcopy

YEARS = (2026, 2027, 2028, 2029, 2030)

# Latest reported balance sheet: August 2, 2026 Form 10-Q, $ millions.
# Other assets aggregate accounts receivable, prepaid/current assets, lease ROU
# assets, deferred tax assets, goodwill, and other long-term assets. Other
# liabilities aggregate all reported liabilities; WSM reported no financial debt.
OPENING = {
    "revenue": 7_806.816,  # FY2025 audited revenue, not a six-month annualization
    "cash": 1_028.936,
    "inventory": 1_447.423,
    "ppe": 1_121.677,
    "other_assets": 1_908.270,
    "other_liabilities": 3_365.392,
    "equity": 2_140.914,
}

# Separate, unchanged base input set.  Each sensitivity run receives a fresh
# deep copy so only the named driver differs and linked accounting recalculates.
BASE_INPUTS = {
    # FY2026 is the midpoint of 4.7%-7.2% company guidance; later years fade.
    "revenue_growth": (0.0595, 0.0400, 0.0350, 0.0300, 0.0300),
    "gross_margin": 0.455,  # Judgment: Q2 FY2026 non-GAAP margin reference.
    "cash_sga_as_pct_gross_profit": 0.543,  # FY25 SG&A less D&A / gross profit.
    "depreciation_as_pct_opening_ppe": 0.211,  # FY25 D&A / ending PP&E.
    "capex": 260.0,  # Judgment anchored to FY25 reported $259.438m capex.
    "tax_rate": 0.251,  # FY25 effective tax rate.
    "inventory_days": 127.0,  # FY25 ending inventory / COGS x 365.
    "other_working_capital_as_pct_revenue_change": 0.005,  # Judgment.
    "dividends": 325.0,  # Judgment near FY25 cash dividend level.
    "buybacks": 500.0,  # Judgment, below FY25's unusually large repurchases.
    "cost_of_equity": 0.10,  # Existing WSM DCF convention.
    "terminal_growth": 0.03,  # Existing WSM DCF convention.
    "shares": 117.779173,  # Common shares outstanding August 23, 2026.
}

# Existing, preselected one-at-a-time ranges.  Growth moves by 2.0 percentage
# points in every forecast year; gross margin moves by 2.0 percentage points.
SENSITIVITY_CASES = {
    "Revenue growth": {
        "units": "% by year (FY2026E–FY2030E)",
        "input": "revenue_growth",
        "Low": (0.0395, 0.0200, 0.0150, 0.0100, 0.0100),
        "Base": BASE_INPUTS["revenue_growth"],
        "High": (0.0795, 0.0600, 0.0550, 0.0500, 0.0500),
    },
    "Gross margin": {
        "units": "% (each forecast year)",
        "input": "gross_margin",
        "Low": 0.435,
        "Base": BASE_INPUTS["gross_margin"],
        "High": 0.475,
    },
}


def assert_balanced(year: int, gap: float) -> None:
    if abs(gap) > 0.05:
        raise ValueError(f"{year}: balance sheet gap is {gap:.1f} million.")


def project(inputs: dict[str, object] | None = None) -> list[dict[str, float]]:
    inputs = deepcopy(BASE_INPUTS if inputs is None else inputs)
    state = OPENING.copy()
    rows: list[dict[str, float]] = []
    for index, year in enumerate(YEARS):
        opening = state.copy()
        revenue = opening["revenue"] * (1 + inputs["revenue_growth"][index])
        gross_profit = revenue * inputs["gross_margin"]
        cash_sga = gross_profit * inputs["cash_sga_as_pct_gross_profit"]
        depreciation = opening["ppe"] * inputs["depreciation_as_pct_opening_ppe"]
        operating_income = gross_profit - cash_sga - depreciation
        pretax_income = operating_income  # No financial debt; interest income conservatively omitted.
        taxes = max(0.0, pretax_income) * inputs["tax_rate"]
        net_income = pretax_income - taxes

        inventory = revenue * (1 - inputs["gross_margin"]) * inputs["inventory_days"] / 365
        inventory_change = inventory - opening["inventory"]
        revenue_change = revenue - opening["revenue"]
        other_wc_change = revenue_change * inputs["other_working_capital_as_pct_revenue_change"]
        ppe = opening["ppe"] + inputs["capex"] - depreciation
        other_assets = opening["other_assets"] + other_wc_change
        other_liabilities = opening["other_liabilities"]
        fcfe = net_income + depreciation - inputs["capex"] - inventory_change - other_wc_change
        cash = opening["cash"] + fcfe - inputs["dividends"] - inputs["buybacks"]
        equity = opening["equity"] + net_income - inputs["dividends"] - inputs["buybacks"]

        assets = cash + inventory + ppe + other_assets
        liabilities_equity = other_liabilities + equity
        gap = assets - liabilities_equity
        assert_balanced(year, gap)
        rows.append(locals().copy())
        state.update({"revenue": revenue, "cash": cash, "inventory": inventory,
                      "ppe": ppe, "other_assets": other_assets,
                      "other_liabilities": other_liabilities, "equity": equity})
    return rows


def print_table(title: str, lines: list[tuple[str, list[float]]]) -> None:
    width = 34
    print(f"\n{title}")
    print(f"{'$ millions':<{width}}" + "".join(f"{year:>12}" for year in YEARS))
    for label, values in lines:
        print(f"{label:<{width}}" + "".join(f"{value:>12,.1f}" for value in values))


def value_equity(rows: list[dict[str, float]], inputs: dict[str, object]) -> tuple[float, float, float]:
    if inputs["cost_of_equity"] <= inputs["terminal_growth"]:
        raise ValueError("Valuation unavailable: cost of equity must exceed terminal growth.")
    pv_explicit = sum(row["fcfe"] / (1 + inputs["cost_of_equity"]) ** (index + 1)
                      for index, row in enumerate(rows))
    terminal_value = rows[-1]["fcfe"] * (1 + inputs["terminal_growth"]) / (inputs["cost_of_equity"] - inputs["terminal_growth"])
    pv_terminal = terminal_value / (1 + inputs["cost_of_equity"]) ** len(rows)
    equity_value = pv_explicit + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / inputs["shares"]


def format_input(value: object) -> str:
    if isinstance(value, tuple):
        return ", ".join(f"{item:.2%}" for item in value)
    return f"{value:.2%}"


def run_case(driver: str, case: str, value: object) -> dict[str, object]:
    """Run one scenario from a new full base-input copy; flag, do not rank, errors."""
    inputs = deepcopy(BASE_INPUTS)
    inputs[SENSITIVITY_CASES[driver]["input"]] = value
    try:
        rows = project(inputs)
        equity_value, terminal_share, per_share = value_equity(rows, inputs)
        checks_pass = all(abs(row["gap"]) <= 0.05 and row["cash"] >= 0.0 for row in rows)
        if not checks_pass:
            return {"case": case, "input": value, "valid": False,
                    "error": "accounting gap or negative cash", "rows": rows}
        return {"case": case, "input": value, "rows": rows, "valid": True,
                "operating_income": rows[-1]["operating_income"], "fcfe": rows[-1]["fcfe"],
                "per_share": per_share, "equity_value": equity_value,
                "terminal_share": terminal_share, "gap": rows[-1]["gap"]}
    except ValueError as error:
        return {"case": case, "input": value, "valid": False, "error": str(error)}


def print_sensitivity() -> None:
    print("\nOne-at-a-Time Sensitivity Analysis")
    print("Each run starts from a fresh independent copy of BASE_INPUTS; only the named input changes.")
    for driver, specification in SENSITIVITY_CASES.items():
        cases = [run_case(driver, case, value) for case, value in
                 (("Low", specification["Low"]), ("Base", specification["Base"]),
                  ("High", specification["High"]))]
        base = next(case for case in cases if case["case"] == "Base")
        print(f"\n{driver} — input units: {specification['units']}")
        print(f"{'Case':<8}{'Actual input':<42}{'FY2030 op. income':>20}{'Δ from base':>15}"
              f"{'FY2030 FCFE':>16}{'Δ from base':>15}{'Value/share':>15}{'Δ from base':>15}{'Checks':>29}")
        valid = []
        for case in cases:
            if not case["valid"]:
                print(f"{case['case']:<8}{format_input(case['input']):<42}{'Invalid run: ' + case['error']}")
                continue
            valid.append(case)
            print(f"{case['case']:<8}{format_input(case['input']):<42}"
                  f"{case['operating_income']:>20,.1f}{case['operating_income'] - base['operating_income']:>+15,.1f}"
                  f"{case['fcfe']:>16,.1f}{case['fcfe'] - base['fcfe']:>+15,.1f}"
                  f"{case['per_share']:>15,.2f}{case['per_share'] - base['per_share']:>+15,.2f}"
                  f" | {'Pass: all gaps 0; cash positive':<29}")
        if valid:
            for output, label in (("operating_income", "FY2030 operating income"),
                                  ("fcfe", "FY2030 FCFE"), ("per_share", "value per share")):
                span = max(case[output] for case in valid) - min(case[output] for case in valid)
                suffix = " million" if output != "per_share" else " per share"
                print(f"{label} span (max − min across valid cases): {span:,.2f}{suffix}")
        # Selected, traceable low-case statement details and check.
        selected = cases[0]
        if selected["valid"]:
            final = selected["rows"][-1]
            print("Trace (low case, FY2030, $ millions): "
                  f"revenue {final['revenue']:,.1f}; gross profit {final['gross_profit']:,.1f}; "
                  f"cash SG&A {final['cash_sga']:,.1f}; depreciation {final['depreciation']:,.1f}; "
                  f"operating income {final['operating_income']:,.1f}; net income {final['net_income']:,.1f}; "
                  f"FCFE {final['fcfe']:,.1f}; cash {final['cash']:,.1f}; inventory {final['inventory']:,.1f}; "
                  f"PP&E {final['ppe']:,.1f}; total assets {final['assets']:,.1f}; equity {final['equity']:,.1f}; "
                  f"assets − liabilities − equity {final['gap']:,.1f}.")


def main() -> None:
    base_inputs = deepcopy(BASE_INPUTS)
    rows = project(base_inputs)
    values = lambda name: [row[name] for row in rows]
    print_table("Income Statement", [
        ("Revenue", values("revenue")), ("Gross profit", values("gross_profit")),
        ("Cash SG&A", values("cash_sga")), ("Depreciation", values("depreciation")),
        ("Operating income", values("operating_income")), ("Taxes", values("taxes")),
        ("Net income", values("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Cash", values("cash")), ("Inventory", values("inventory")),
        ("PP&E, net", values("ppe")), ("Other assets", values("other_assets")),
        ("Total assets", values("assets")), ("Other liabilities", values("other_liabilities")),
        ("Equity", values("equity")), ("Liabilities + equity", values("liabilities_equity")),
    ])
    print_table("Cash Flow Statement", [
        ("Net income", values("net_income")), ("Depreciation", values("depreciation")),
        ("Capital spending", [base_inputs["capex"]] * len(YEARS)),
        ("Change in inventory", values("inventory_change")),
        ("Change in other working capital", values("other_wc_change")),
        ("FCFE", values("fcfe")), ("Dividends", [base_inputs["dividends"]] * len(YEARS)),
        ("Share repurchases", [base_inputs["buybacks"]] * len(YEARS)),
    ])
    print_table("Annual Checks", [
        ("Assets - liabilities - equity", values("gap")),
        ("Cash >= 0 (1=yes)", [1.0 if row["cash"] >= 0 else 0.0 for row in rows]),
    ])
    equity_value, terminal_share, per_share = value_equity(rows, base_inputs)
    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${per_share:,.2f}")
    print_sensitivity()
    # Explicitly restore and rerun the unchanged base case after all scenarios.
    restored_rows = project(deepcopy(BASE_INPUTS))
    _, _, restored_per_share = value_equity(restored_rows, deepcopy(BASE_INPUTS))
    print(f"\nBase restored and rerun: FY2030 FCFE ${restored_rows[-1]['fcfe']:,.1f} million; "
          f"value per share ${restored_per_share:,.2f}; FY2030 gap ${restored_rows[-1]['gap']:,.1f} million.")


if __name__ == "__main__":
    main()
