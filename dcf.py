"""Five-year FCFF DCF valuation (all dollar figures are in USD millions)."""

# =========================
# Editable inputs
# =========================
starting_fcff = 100.0
growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 50.0
debt = 300.0
diluted_shares = 50.0


def main() -> None:
    if terminal_growth >= wacc:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the Gordon-growth formula."
        )

    if len(growth_rates) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")
    if diluted_shares <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    fcff_by_year = []
    current_fcff = starting_fcff
    for growth_rate in growth_rates:
        current_fcff *= 1 + growth_rate
        fcff_by_year.append(current_fcff)

    pv_explicit_fcff = sum(
        fcff / (1 + wacc) ** year
        for year, fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = fcff_by_year[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value_year_5 / (1 + wacc) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt
    value_per_diluted_share = equity_value / diluted_shares
    pv_terminal_value_share_of_ev = pv_terminal_value / enterprise_value

    for year, fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {fcff:.4f}")
    print(f"Present Value of Explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present Value of Terminal Value: {pv_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(
        "PV of Terminal Value as Share of Enterprise Value: "
        f"{pv_terminal_value_share_of_ev:.4f}"
    )


if __name__ == "__main__":
    main()
