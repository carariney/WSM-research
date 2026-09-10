"""Five-year FCFF DCF valuation (all dollar figures are in USD millions)."""

# =========================
# Editable inputs
# =========================
starting_fcff = 1055.451
growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 1019.801
debt = 0.0
diluted_shares = 123.153

# Sensitivity and reverse-DCF inputs
sensitivity_wacc_values = [0.09, 0.10, 0.11]
sensitivity_terminal_growth_values = [0.02, 0.03, 0.04]
target_share_price = 227.52
reverse_shift_lower_bound = -0.05
reverse_shift_upper_bound = 0.10


def value_dcf(
    valuation_wacc: float,
    valuation_terminal_growth: float,
    valuation_growth_rates: list[float],
) -> dict[str, float | list[float]]:
    """Return DCF results using the supplied discount and growth assumptions."""
    fcff_by_year = []
    current_fcff = starting_fcff
    for growth_rate in valuation_growth_rates:
        current_fcff *= 1 + growth_rate
        fcff_by_year.append(current_fcff)

    pv_explicit_fcff = sum(
        fcff / (1 + valuation_wacc) ** year
        for year, fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1] * (1 + valuation_terminal_growth)
        / (valuation_wacc - valuation_terminal_growth)
    )
    pv_terminal_value = terminal_value_year_5 / (1 + valuation_wacc) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt

    return {
        "fcff_by_year": fcff_by_year,
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": equity_value / diluted_shares,
        "pv_terminal_value_share_of_ev": pv_terminal_value / enterprise_value,
    }


def print_sensitivity_grid() -> None:
    """Print value per share for each editable WACC/growth combination."""
    print("\nSensitivity Grid: Value per Diluted Share")
    column_width = 16
    print(
        f"{'WACC \\ Terminal Growth':>{column_width}}"
        + "".join(f"{growth:>{column_width}.2%}" for growth in sensitivity_terminal_growth_values)
    )
    for sensitivity_wacc in sensitivity_wacc_values:
        cells = []
        for sensitivity_growth in sensitivity_terminal_growth_values:
            if sensitivity_growth >= sensitivity_wacc:
                cells.append("INVALID")
            else:
                value = value_dcf(
                    sensitivity_wacc, sensitivity_growth, growth_rates
                )["value_per_diluted_share"]
                cells.append(f"{value:.4f}")
        print(
            f"{sensitivity_wacc:>{column_width}.2%}"
            + "".join(f"{cell:>{column_width}}" for cell in cells)
        )


def solve_reverse_dcf() -> float | None:
    """Find the uniform explicit-growth shift, or None if the bracket misses."""
    if reverse_shift_lower_bound >= reverse_shift_upper_bound:
        raise ValueError("reverse-DCF lower bound must be less than the upper bound.")
    if any(
        growth_rate + bound <= -1
        for growth_rate in growth_rates
        for bound in (reverse_shift_lower_bound, reverse_shift_upper_bound)
    ):
        raise ValueError(
            "reverse-DCF bracket is invalid: it pushes an annual growth rate to -100% or below."
        )

    def price_for_shift(shift: float) -> float:
        shifted_growth_rates = [growth_rate + shift for growth_rate in growth_rates]
        return value_dcf(wacc, terminal_growth, shifted_growth_rates)[
            "value_per_diluted_share"
        ]

    lower = reverse_shift_lower_bound
    upper = reverse_shift_upper_bound
    lower_price = price_for_shift(lower)
    upper_price = price_for_shift(upper)
    if target_share_price < lower_price or target_share_price > upper_price:
        return None
    if abs(lower_price - target_share_price) < 1e-10:
        return lower
    if abs(upper_price - target_share_price) < 1e-10:
        return upper

    for _ in range(100):
        midpoint = (lower + upper) / 2
        midpoint_price = price_for_shift(midpoint)
        if abs(midpoint_price - target_share_price) < 1e-10:
            return midpoint
        if midpoint_price < target_share_price:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def print_reverse_dcf() -> None:
    """Print the reverse-DCF outcome and every assumption held fixed."""
    print("\nReverse DCF: Uniform Shift to All Five Explicit Growth Rates")
    print(f"Target Share Price: {target_share_price:.4f}")
    print("Inputs held fixed:")
    print(f"  Starting FCFF: {starting_fcff:.4f}")
    print("  Base Explicit Growth Rates: " + ", ".join(f"{rate:.2%}" for rate in growth_rates))
    print(f"  WACC: {wacc:.2%}")
    print(f"  Terminal Growth: {terminal_growth:.2%}")
    print(f"  Non-operating Cash: {non_operating_cash:.4f}")
    print(f"  Debt: {debt:.4f}")
    print(f"  Diluted Shares: {diluted_shares:.4f}")
    print(
        "  Shift Search Bounds: "
        f"{reverse_shift_lower_bound:.2%} to {reverse_shift_upper_bound:.2%}"
    )
    print(
        "Interpretation: any solved shift is one set of assumptions consistent with "
        "the target price, not proof of mispricing."
    )
    try:
        solved_shift = solve_reverse_dcf()
    except ValueError as error:
        print(f"Solved Uniform Growth Shift: no solution ({error})")
        return
    if solved_shift is None:
        print("Solved Uniform Growth Shift: no solution in that bracket")
    else:
        print(f"Solved Uniform Growth Shift: {solved_shift:.6%}")


def main() -> None:
    if terminal_growth >= wacc:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the Gordon-growth formula."
        )

    if len(growth_rates) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")
    if diluted_shares <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    results = value_dcf(wacc, terminal_growth, growth_rates)
    fcff_by_year = results["fcff_by_year"]
    pv_explicit_fcff = results["pv_explicit_fcff"]
    terminal_value_year_5 = results["terminal_value_year_5"]
    pv_terminal_value = results["pv_terminal_value"]
    enterprise_value = results["enterprise_value"]
    equity_value = results["equity_value"]
    value_per_diluted_share = results["value_per_diluted_share"]
    pv_terminal_value_share_of_ev = results["pv_terminal_value_share_of_ev"]

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
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
