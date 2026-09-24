"""Five-year WSM pro forma, FY2026E-FY2030E (USD millions except per-share data).

Opening balance sheet: WSM Form 10-Q at August 2, 2026.  FY2025 revenue is
the full-year base. Forecast inputs labeled JUDGMENT are transparent model
choices, not reported company guidance.
"""

from __future__ import annotations


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

# Forecast assumptions: guidance, history, and stated judgments.
REVENUE_GROWTH = (0.0595, 0.0400, 0.0350, 0.0300, 0.0300)
# FY2026 is the midpoint of 4.7%-7.2% company guidance; later years fade.
GROSS_MARGIN = 0.455  # Judgment: Q2 FY2026 non-GAAP gross-margin reference.
CASH_SGA_AS_PCT_GROSS_PROFIT = 0.543  # FY2025 SG&A less D&A, divided by gross profit.
DEPRECIATION_AS_PCT_OPENING_PPE = 0.211  # FY2025 D&A / ending PP&E.
CAPEX = 260.0  # Judgment anchored to FY2025 reported $259.438m capex.
TAX_RATE = 0.251  # FY2025 effective tax rate.
INVENTORY_DAYS = 127.0  # FY2025 ending inventory / COGS x 365.
OTHER_WORKING_CAPITAL_AS_PCT_REVENUE_CHANGE = 0.005  # Judgment.
DIVIDENDS = 325.0  # Judgment near FY2025 cash dividend level.
BUYBACKS = 500.0  # Judgment, below FY2025's unusually large repurchase level.
COST_OF_EQUITY = 0.10  # Existing WSM DCF convention.
TERMINAL_GROWTH = 0.03  # Existing WSM DCF convention.
SHARES = 117.779173  # WSM common shares outstanding August 23, 2026.


def assert_balanced(year: int, gap: float) -> None:
    if abs(gap) > 0.05:
        raise ValueError(f"{year}: balance sheet gap is {gap:.1f} million.")


def project() -> list[dict[str, float]]:
    state = OPENING.copy()
    rows: list[dict[str, float]] = []
    for index, year in enumerate(YEARS):
        opening = state.copy()
        revenue = opening["revenue"] * (1 + REVENUE_GROWTH[index])
        gross_profit = revenue * GROSS_MARGIN
        cash_sga = gross_profit * CASH_SGA_AS_PCT_GROSS_PROFIT
        depreciation = opening["ppe"] * DEPRECIATION_AS_PCT_OPENING_PPE
        operating_income = gross_profit - cash_sga - depreciation
        pretax_income = operating_income  # No financial debt; interest income conservatively omitted.
        taxes = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - taxes

        inventory = revenue * (1 - GROSS_MARGIN) * INVENTORY_DAYS / 365
        inventory_change = inventory - opening["inventory"]
        revenue_change = revenue - opening["revenue"]
        other_wc_change = revenue_change * OTHER_WORKING_CAPITAL_AS_PCT_REVENUE_CHANGE
        ppe = opening["ppe"] + CAPEX - depreciation
        other_assets = opening["other_assets"] + other_wc_change
        other_liabilities = opening["other_liabilities"]
        fcfe = net_income + depreciation - CAPEX - inventory_change - other_wc_change
        cash = opening["cash"] + fcfe - DIVIDENDS - BUYBACKS
        equity = opening["equity"] + net_income - DIVIDENDS - BUYBACKS

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


def value_equity(rows: list[dict[str, float]]) -> tuple[float, float, float]:
    pv_explicit = sum(row["fcfe"] / (1 + COST_OF_EQUITY) ** (index + 1)
                      for index, row in enumerate(rows))
    terminal_value = rows[-1]["fcfe"] * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(rows)
    equity_value = pv_explicit + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / SHARES


def main() -> None:
    rows = project()
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
        ("Capital spending", [CAPEX] * len(YEARS)),
        ("Change in inventory", values("inventory_change")),
        ("Change in other working capital", values("other_wc_change")),
        ("FCFE", values("fcfe")), ("Dividends", [DIVIDENDS] * len(YEARS)),
        ("Share repurchases", [BUYBACKS] * len(YEARS)),
    ])
    print_table("Annual Checks", [
        ("Assets - liabilities - equity", values("gap")),
        ("Cash >= 0 (1=yes)", [1.0 if row["cash"] >= 0 else 0.0 for row in rows]),
    ])
    equity_value, terminal_share, per_share = value_equity(rows)
    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${per_share:,.2f}")


if __name__ == "__main__":
    main()
