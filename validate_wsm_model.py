"""Runnable validation for the integrated WSM pro-forma and valuation engine."""

from copy import deepcopy

import wsm_proforma as model


def assert_close(actual: float, expected: float, tolerance: float, label: str) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{label}: {actual} differs from {expected} by more than {tolerance}.")


def known_answer_dcf_check() -> None:
    """Reproduce the Week 3 synthetic checkpoint without using WSM inputs."""
    starting_fcff = 100.0
    growth = (0.08, 0.06, 0.05, 0.04, 0.03)
    wacc, terminal_growth = 0.10, 0.03
    fcff = []
    current = starting_fcff
    for rate in growth:
        current *= 1 + rate
        fcff.append(current)
    pv_explicit = sum(value / (1 + wacc) ** year for year, value in enumerate(fcff, 1))
    terminal = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal / (1 + wacc) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + 50.0 - 300.0
    assert_close(equity_value / 50.0, 27.497370, 0.01, "synthetic per-share DCF")
    assert_close(pv_terminal / enterprise_value, 0.724014, 0.0002, "synthetic terminal-value share")


def main() -> None:
    known_answer_dcf_check()
    model.assert_base_year_reconciliation()
    inputs = deepcopy(model.BASE_INPUTS)
    rows = model.project(inputs)
    if not all(abs(row["gap"]) <= 0.05 and row["cash"] >= 0 for row in rows):
        raise AssertionError("Pro-forma articulation failed: a balance-sheet gap or negative cash remains.")
    if not all(abs(row["fcff"] - row["fcfe"]) <= 0.05 for row in rows):
        raise AssertionError("FCFF/FCFE reconciliation failed under the no-debt convention.")
    model.assert_valuation_reconciliation(rows, inputs)
    model.assert_dcf_directionality(rows, inputs)
    base = model.value_fcff(rows, inputs)
    assert_close(base["enterprise_value"] + model.OPENING["cash"], base["equity_value"], 0.05,
                 "enterprise-to-equity bridge")
    print("PASS: known-answer DCF, base-year reconciliation, pro-forma articulation, "
          "FCFF/FCFE reconciliation, enterprise-to-equity bridge, and DCF directionality.")
    print(f"PASS: integrated base FCFF value per share = ${base['per_share']:.2f} as of {model.VALUATION_DATE}.")


if __name__ == "__main__":
    main()
