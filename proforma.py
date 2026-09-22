"""ABG five-year linked pro-forma model, 2026-2030 (USD millions)."""

from __future__ import annotations


YEARS = (2026, 2027, 2028, 2029, 2030)

# ABG FY2025 Form 10-K, December 31, 2025. Debt includes current and long-term
# debt. Other assets/liabilities aggregate reported accounts not separately forecast.
OPENING = {
    "revenue": 17_999.0, "cash": 40.4, "inventory": 2_135.8,
    "floor_plan": 2_027.0, "ppe": 3_070.4, "other_assets": 6_371.6,
    "debt": 3_572.0, "revolver": 0.0, "other_liabilities": 2_127.3,
    "equity": 3_891.9,
}

# Supplied assumptions.
GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_RATIO = (0.665, 0.655, 0.645, 0.645, 0.645)
DEPR_RATIO = 82.4 / 3_070.4
IMPAIRMENT, CAPEX, TAX_RATE = 120.0, 250.0, 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365
FLOOR_PLAN_RATIO = 2_027.0 / 2_135.8
OTHER_WC_PCT = 0.008
MIN_CASH, REVOLVER_LIMIT, REVOLVER_RATE = 25.0, 850.0, 0.06
DEBT_REPAYMENT, BUYBACK = 150.0, 150.0
FLOOR_PLAN_RATE, TERM_DEBT_RATE = 0.0467, 0.0544
COST_OF_EQUITY, TERMINAL_GROWTH, SHARES = 0.10, 0.025, 17.951349


def assert_balanced(year: int, gap: float, cash: float) -> None:
    """Raise a named error for either required annual check."""
    if abs(gap) > 0.05:
        raise ValueError(f"{year}: balance sheet gap is {gap:.1f}.")
    if cash < MIN_CASH - 0.05:
        raise ValueError(f"{year}: cash {cash:.1f} is below minimum {MIN_CASH:.1f}.")


def project() -> list[dict[str, float]]:
    """Project statements in the sequence stated in the assignment."""
    state = OPENING.copy()
    output: list[dict[str, float]] = []
    for i, year in enumerate(YEARS):
        opening = state.copy()

        # Income statement.
        revenue = opening["revenue"] * (1 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_RATIO[i]
        depreciation = opening["ppe"] * DEPR_RATIO
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = (opening["floor_plan"] * FLOOR_PLAN_RATE
                    + opening["debt"] * TERM_DEBT_RATE
                    + opening["revolver"] * REVOLVER_RATE)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        # Balance sheet except cash/revolver.
        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_RATIO
        ppe = opening["ppe"] + CAPEX - depreciation
        revenue_change = revenue - opening["revenue"]
        other_wc_change = OTHER_WC_PCT * revenue_change
        other_assets = opening["other_assets"] + other_wc_change - IMPAIRMENT
        debt = opening["debt"] - DEBT_REPAYMENT
        if debt < 0:
            raise ValueError(f"{year}: debt repayment exceeds opening debt.")
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - BUYBACK

        # FCFE, then cash sweep. FCFE includes the specified scheduled debt repayment.
        inventory_change = inventory - opening["inventory"]
        floor_plan_change = floor_plan - opening["floor_plan"]
        fcfe = (net_income + depreciation + IMPAIRMENT - CAPEX - inventory_change
                - other_wc_change + floor_plan_change - DEBT_REPAYMENT)
        cash_before_revolver = opening["cash"] + fcfe - BUYBACK
        draw = repayment = 0.0
        if cash_before_revolver < MIN_CASH:
            draw = MIN_CASH - cash_before_revolver
            revolver = opening["revolver"] + draw
            if revolver > REVOLVER_LIMIT + 0.05:
                raise ValueError(f"{year}: revolver {revolver:.1f} exceeds limit {REVOLVER_LIMIT:.1f}.")
            cash = MIN_CASH
        else:
            repayment = min(opening["revolver"], cash_before_revolver - MIN_CASH)
            revolver = opening["revolver"] - repayment
            cash = cash_before_revolver - repayment

        assets = cash + inventory + ppe + other_assets
        liabilities_equity = floor_plan + debt + revolver + other_liabilities + equity
        gap = assets - liabilities_equity
        assert_balanced(year, gap, cash)
        row = locals().copy()
        row.update({"year": float(year), "impairment": IMPAIRMENT, "capex": CAPEX,
                    "buyback": BUYBACK, "assets": assets,
                    "liabilities_equity": liabilities_equity, "gap": gap})
        output.append(row)
        state.update({"revenue": revenue, "cash": cash, "inventory": inventory,
                      "floor_plan": floor_plan, "ppe": ppe, "other_assets": other_assets,
                      "debt": debt, "revolver": revolver,
                      "other_liabilities": other_liabilities, "equity": equity})
    return output


def print_table(title: str, rows: list[tuple[str, list[float]]]) -> None:
    width = 33
    print(f"\n{title}")
    print(f"{'$ millions':<{width}}" + "".join(f"{year:>12}" for year in YEARS))
    for label, values in rows:
        print(f"{label:<{width}}" + "".join(f"{value:>12,.1f}" for value in values))


def value_equity(rows: list[dict[str, float]]) -> tuple[float, float, float]:
    pv_fcfe = sum(row["fcfe"] / (1 + COST_OF_EQUITY) ** (i + 1)
                  for i, row in enumerate(rows))
    terminal_value = ((rows[-1]["fcfe"] + DEBT_REPAYMENT) * (1 + TERMINAL_GROWTH)
                      / (COST_OF_EQUITY - TERMINAL_GROWTH))
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(rows)
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / SHARES


def main() -> None:
    rows = project()
    values = lambda key: [row[key] for row in rows]
    print_table("Income Statement", [
        ("Revenue", values("revenue")), ("Gross profit", values("gross_profit")),
        ("SG&A", values("sga")), ("Depreciation", values("depreciation")),
        ("Impairment", values("impairment")), ("Operating income", values("operating_income")),
        ("Interest", values("interest")), ("Pretax income", values("pretax_income")),
        ("Tax", values("tax")), ("Net income", values("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Cash", values("cash")), ("Inventory", values("inventory")),
        ("PP&E, net", values("ppe")), ("Other assets", values("other_assets")),
        ("Total assets", values("assets")), ("Floor plan", values("floor_plan")),
        ("Term debt", values("debt")), ("Revolver", values("revolver")),
        ("Other liabilities", values("other_liabilities")), ("Equity", values("equity")),
        ("Liabilities + equity", values("liabilities_equity")),
    ])
    print_table("Cash Flow Statement", [
        ("Net income", values("net_income")), ("Depreciation", values("depreciation")),
        ("Impairment", values("impairment")), ("Capital spending", values("capex")),
        ("Change in inventory", values("inventory_change")),
        ("Change in other working capital", values("other_wc_change")),
        ("Change in floor plan", values("floor_plan_change")),
        ("Debt repayment", [DEBT_REPAYMENT] * len(YEARS)), ("FCFE", values("fcfe")),
        ("Share buyback", values("buyback")), ("Revolver draw", values("draw")),
        ("Revolver repayment", values("repayment")),
    ])
    print_table("Annual Checks", [
        ("Assets - liabilities - equity", values("gap")),
        ("Cash >= minimum (1=yes)", [1.0 if row["cash"] >= MIN_CASH else 0.0 for row in rows]),
    ])
    equity_value, terminal_share, value_per_share = value_equity(rows)
    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
