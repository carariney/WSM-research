"""Five-year WSM pro forma, FY2026E-FY2030E (USD millions except per-share data).

Opening balance sheet: WSM Form 10-Q at August 2, 2026.  FY2025 revenue is
the full-year base. Forecast inputs labeled JUDGMENT are transparent model
choices, not reported company guidance.
"""

from __future__ import annotations

from copy import deepcopy

YEARS = (2026, 2027, 2028, 2029, 2030)
VALUATION_DATE = "August 31, 2026"
MARKET_PRICE = 228.25  # August 31, 2026 close; retained from the peer-input ledger.

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

# Filed FY2025 values used only for the required base-year reconciliation.
# They are not an annualization of the August 2026 quarterly balance sheet.
BASE_YEAR_REPORTED = {
    "revenue": 7_806.816,
    "gross_profit": 3_603.051,
    "sga": 2_187.329,
    "operating_income": 1_415.722,
    "net_income": 1_088.437,
    "capex": 259.438,
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

# With no projected financial debt or interest expense, WACC equals the cost
# of equity under this deliberately simple capital-structure convention.
BASE_INPUTS["wacc"] = BASE_INPUTS["cost_of_equity"]

# Integrated operating cases.  Low/high reuse the already disclosed one-at-a-
# time ranges; downside combines their adverse directions.  They are scenarios,
# not probabilities.
VALUATION_SCENARIOS = {
    "Downside": {"revenue_growth": (0.0395, 0.0200, 0.0150, 0.0100, 0.0100),
                 "gross_margin": 0.435, "action": "Do not initiate"},
    "Base": {"revenue_growth": BASE_INPUTS["revenue_growth"],
             "gross_margin": BASE_INPUTS["gross_margin"], "action": "Watch / defer"},
    "High": {"revenue_growth": (0.0795, 0.0600, 0.0550, 0.0500, 0.0500),
             "gross_margin": 0.475, "action": "Reassess; not an automatic initiation"},
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


def assert_base_year_reconciliation() -> None:
    """Fail loudly if the filed FY2025 anchors feeding the forecast are altered."""
    checks = {
        "opening revenue": (OPENING["revenue"], BASE_YEAR_REPORTED["revenue"]),
        "FY2025 gross profit": (BASE_YEAR_REPORTED["gross_profit"], 3_603.051),
        "FY2025 SG&A": (BASE_YEAR_REPORTED["sga"], 2_187.329),
        "FY2025 operating income": (BASE_YEAR_REPORTED["operating_income"], 1_415.722),
        "FY2025 net income": (BASE_YEAR_REPORTED["net_income"], 1_088.437),
        "FY2025 capex": (BASE_YEAR_REPORTED["capex"], 259.438),
    }
    for label, (actual, expected) in checks.items():
        if abs(actual - expected) > 0.001:
            raise ValueError(f"Base-year reconciliation failed for {label}: {actual} != {expected}.")


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
        nopat = operating_income * (1 - inputs["tax_rate"])
        fcff = nopat + depreciation - inputs["capex"] - inventory_change - other_wc_change
        # No financial debt or interest expense is modeled; therefore FCFE equals
        # FCFF here. Dividends and buybacks are distributions after FCFE, not an
        # additional deduction from cash flow available to equity holders.
        fcfe = net_income + depreciation - inputs["capex"] - inventory_change - other_wc_change
        if abs(fcff - fcfe) > 0.05:
            raise ValueError(f"{year}: FCFF and FCFE should reconcile under the no-debt convention.")
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


def value_fcff(rows: list[dict[str, float]], inputs: dict[str, object]) -> dict[str, float]:
    """Value pro-forma FCFF with WACC, then bridge EV to common equity."""
    wacc = inputs["wacc"]
    if wacc <= inputs["terminal_growth"]:
        raise ValueError("Valuation unavailable: WACC must exceed terminal growth.")
    pv_explicit = sum(row["fcff"] / (1 + wacc) ** (index + 1) for index, row in enumerate(rows))
    terminal_value = rows[-1]["fcff"] * (1 + inputs["terminal_growth"]) / (wacc - inputs["terminal_growth"])
    pv_terminal = terminal_value / (1 + wacc) ** len(rows)
    enterprise_value = pv_explicit + pv_terminal
    # Existing project convention: all reported cash is treated as non-operating.
    # This is intentionally surfaced as a judgment to challenge, not a factual claim.
    equity_value = enterprise_value + OPENING["cash"]
    return {"pv_explicit": pv_explicit, "terminal_value": terminal_value,
            "pv_terminal": pv_terminal, "enterprise_value": enterprise_value,
            "equity_value": equity_value, "per_share": equity_value / inputs["shares"],
            "terminal_share": pv_terminal / enterprise_value}


def value_with_excess_cash(enterprise_value: float, inputs: dict[str, object], excess_cash_fraction: float) -> float:
    """Return per-share equity value for an explicit excess-cash treatment."""
    if not 0.0 <= excess_cash_fraction <= 1.0:
        raise ValueError("Excess-cash fraction must be between zero and one.")
    return (enterprise_value + OPENING["cash"] * excess_cash_fraction) / inputs["shares"]


def solve_market_implied_terminal_growth(rows: list[dict[str, float]], inputs: dict[str, object]) -> float | None:
    """Solve g that matches the dated market price with base operations held fixed."""
    lower, upper = 0.0, inputs["wacc"] - 0.0001

    def price(growth: float) -> float:
        changed = deepcopy(inputs)
        changed["terminal_growth"] = growth
        return value_fcff(rows, changed)["per_share"]

    if not price(lower) <= MARKET_PRICE <= price(upper):
        return None
    for _ in range(100):
        midpoint = (lower + upper) / 2
        if price(midpoint) < MARKET_PRICE:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def value_fcfe(rows: list[dict[str, float]], inputs: dict[str, object]) -> dict[str, float]:
    """Cross-check FCFF using the identical operating forecast and no-debt convention."""
    rate = inputs["cost_of_equity"]
    if rate <= inputs["terminal_growth"]:
        raise ValueError("Valuation unavailable: cost of equity must exceed terminal growth.")
    pv_explicit = sum(row["fcfe"] / (1 + rate) ** (index + 1) for index, row in enumerate(rows))
    terminal_value = rows[-1]["fcfe"] * (1 + inputs["terminal_growth"]) / (rate - inputs["terminal_growth"])
    pv_terminal = terminal_value / (1 + rate) ** len(rows)
    operating_equity_value = pv_explicit + pv_terminal
    equity_value = operating_equity_value + OPENING["cash"]
    return {"operating_equity_value": operating_equity_value, "equity_value": equity_value,
            "per_share": equity_value / inputs["shares"], "terminal_share": pv_terminal / operating_equity_value}


def assert_valuation_reconciliation(rows: list[dict[str, float]], inputs: dict[str, object]) -> None:
    fcff = value_fcff(rows, inputs)
    fcfe = value_fcfe(rows, inputs)
    if abs(fcff["equity_value"] - fcfe["equity_value"]) > 0.05:
        raise ValueError("FCFF enterprise-to-equity bridge does not reconcile to FCFE value.")
    if abs(fcff["enterprise_value"] + OPENING["cash"] - fcff["equity_value"]) > 0.05:
        raise ValueError("Enterprise-to-equity bridge failed.")


def assert_dcf_directionality(rows: list[dict[str, float]], inputs: dict[str, object]) -> None:
    """Test expected monotonic DCF behavior before results are reported."""
    lower_wacc = deepcopy(inputs); lower_wacc["wacc"] = 0.09
    higher_wacc = deepcopy(inputs); higher_wacc["wacc"] = 0.11
    lower_g = deepcopy(inputs); lower_g["terminal_growth"] = 0.02
    higher_g = deepcopy(inputs); higher_g["terminal_growth"] = 0.04
    if not value_fcff(rows, lower_wacc)["per_share"] > value_fcff(rows, higher_wacc)["per_share"]:
        raise ValueError("DCF monotonicity failed: lower WACC did not increase value.")
    if not value_fcff(rows, lower_g)["per_share"] < value_fcff(rows, higher_g)["per_share"]:
        raise ValueError("DCF monotonicity failed: higher terminal growth did not increase value.")


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
        valuation = value_fcff(rows, inputs)
        checks_pass = all(abs(row["gap"]) <= 0.05 and row["cash"] >= 0.0 for row in rows)
        if not checks_pass:
            return {"case": case, "input": value, "valid": False,
                    "error": "accounting gap or negative cash", "rows": rows}
        return {"case": case, "input": value, "rows": rows, "valid": True,
                "operating_income": rows[-1]["operating_income"], "fcfe": rows[-1]["fcfe"],
                "per_share": valuation["per_share"], "equity_value": valuation["equity_value"],
                "terminal_share": valuation["terminal_share"], "gap": rows[-1]["gap"]}
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


def print_valuation_scenarios() -> None:
    print("\nIntegrated FCFF Valuation Scenarios")
    print("All scenarios use the same WACC, terminal growth, cash, debt, and shares; only revenue growth and gross margin change.")
    print(f"{'Scenario':<12}{'FY2030 FCFF':>15}{'Enterprise value':>20}{'Equity value':>18}{'Value/share':>15}{'Committee action':>39}")
    for name, changes in VALUATION_SCENARIOS.items():
        inputs = deepcopy(BASE_INPUTS)
        inputs.update({"revenue_growth": changes["revenue_growth"], "gross_margin": changes["gross_margin"]})
        rows = project(inputs)
        value = value_fcff(rows, inputs)
        print(f"{name:<12}{rows[-1]['fcff']:>15,.1f}{value['enterprise_value']:>20,.1f}"
              f"{value['equity_value']:>18,.1f}{value['per_share']:>15,.2f}{changes['action']:>39}")


def print_dcf_sensitivity(rows: list[dict[str, float]], inputs: dict[str, object]) -> None:
    print("\nFCFF DCF Sensitivity: Value per Common Share")
    header = "WACC \\ Terminal Growth"
    print(f"{header:>26}{'2.0%':>12}{'3.0%':>12}{'4.0%':>12}")
    for rate in (0.09, 0.10, 0.11):
        cells = []
        for growth in (0.02, 0.03, 0.04):
            changed = deepcopy(inputs); changed["wacc"] = rate; changed["terminal_growth"] = growth
            cells.append(value_fcff(rows, changed)["per_share"])
        print(f"{rate:>26.1%}" + "".join(f"{cell:>12.2f}" for cell in cells))


def main() -> None:
    base_inputs = deepcopy(BASE_INPUTS)
    assert_base_year_reconciliation()
    rows = project(base_inputs)
    assert_valuation_reconciliation(rows, base_inputs)
    assert_dcf_directionality(rows, base_inputs)
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
        ("FCFF", values("fcff")), ("FCFE", values("fcfe")),
        ("Dividends", [base_inputs["dividends"]] * len(YEARS)),
        ("Share repurchases", [base_inputs["buybacks"]] * len(YEARS)),
    ])
    print_table("Annual Checks", [
        ("Assets - liabilities - equity", values("gap")),
        ("Cash >= 0 (1=yes)", [1.0 if row["cash"] >= 0 else 0.0 for row in rows]),
    ])
    fcff_value = value_fcff(rows, base_inputs)
    fcfe_value = value_fcfe(rows, base_inputs)
    print(f"\nIntegrated Valuation — {VALUATION_DATE}")
    print(f"FCFF enterprise value: ${fcff_value['enterprise_value']:,.2f} million")
    print(f"Add: reported cash under existing all-cash convention: ${OPENING['cash']:,.2f} million")
    print("Less: financial debt under existing convention: $0.00 million")
    print(f"FCFF equity value: ${fcff_value['equity_value']:,.2f} million")
    print(f"FCFF value per share: ${fcff_value['per_share']:,.2f}")
    print(f"FCFE cross-check equity value: ${fcfe_value['equity_value']:,.2f} million")
    print(f"FCFE cross-check value per share: ${fcfe_value['per_share']:,.2f}")
    print(f"Terminal value share of enterprise value: {fcff_value['terminal_share']:.1%}")
    print("Cash-treatment sensitivity: "
          f"0% excess ${value_with_excess_cash(fcff_value['enterprise_value'], base_inputs, 0.0):.2f}; "
          f"50% excess ${value_with_excess_cash(fcff_value['enterprise_value'], base_inputs, 0.5):.2f}; "
          f"100% excess ${value_with_excess_cash(fcff_value['enterprise_value'], base_inputs, 1.0):.2f} per share.")
    implied_g = solve_market_implied_terminal_growth(rows, base_inputs)
    if implied_g is None:
        print(f"Market-implied terminal growth: no solution below WACC for ${MARKET_PRICE:.2f} market price.")
    else:
        print(f"Market-implied terminal growth: {implied_g:.2%} to match ${MARKET_PRICE:.2f}, holding the base operating forecast and WACC fixed.")
    print("Validation: base-year reconciliation, balance-sheet articulation, FCFF/FCFE reconciliation, bridge, and DCF directionality all passed.")
    print_dcf_sensitivity(rows, base_inputs)
    print_valuation_scenarios()
    print_sensitivity()
    # Explicitly restore and rerun the unchanged base case after all scenarios.
    restored_rows = project(deepcopy(BASE_INPUTS))
    restored_per_share = value_fcff(restored_rows, deepcopy(BASE_INPUTS))["per_share"]
    print(f"\nBase restored and rerun: FY2030 FCFE ${restored_rows[-1]['fcfe']:,.1f} million; "
          f"value per share ${restored_per_share:,.2f}; FY2030 gap ${restored_rows[-1]['gap']:,.1f} million.")


if __name__ == "__main__":
    main()
