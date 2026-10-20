"""Meridian Foundation Reserve mandate checker.

Run: python3 mandate.py
Probe: python3 mandate.py --probe-long-only
Standard library only. Amounts are portfolio weights in percent unless noted.
"""

from __future__ import annotations

import sys
from copy import deepcopy


# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "days_to_redeem": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days_to_redeem": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days_to_redeem": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "days_to_redeem": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "days_to_redeem": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "days_to_redeem": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days_to_redeem": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days_to_redeem": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # AI-partner attack candidate: it passes coded rules but exposes S9's undefined loss rule.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 97, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    # Lab 14 benchmark: 40% investment-grade bonds and 60% global equity.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
ISSUER_EXEMPTIONS = {"none", "U.S. Treasury", "diversified fund"}


def reserve_minimum_percent() -> float:
    return QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100


def measures(weights: dict[str, float]) -> dict[str, float]:
    """Calculate every reported rule metric from holdings and editable inputs."""
    issuer_exposure: dict[str, float] = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in ISSUER_EXEMPTIONS:
            issuer_exposure[issuer] = issuer_exposure.get(issuer, 0.0) + weight

    return {
        "weight_sum": sum(weights.values()),
        "lowest_weight": min(weights.values()),
        "reserve_eligible": sum(
            weight for holding, weight in weights.items() if HOLDINGS[holding]["reserve_eligible"]
        ),
        "liquid_weight": sum(
            weight for holding, weight in weights.items()
            if HOLDINGS[holding]["days_to_redeem"] <= LIQUIDITY_WINDOW_DAYS
        ),
        "largest_company": max(issuer_exposure.values(), default=0.0),
    }


def print_rule(label: str, value: float, passes: bool) -> bool:
    print(f"  {label:<43} {value:>6.1f} {'pass' if passes else 'FAIL'}")
    return passes


def check_candidate(name: str, weights: dict[str, float]) -> None:
    values = measures(weights)
    print(f"\nCandidate {name}")
    failures = 0
    failures += not print_rule("Weights sum to 100", values["weight_sum"], abs(values["weight_sum"] - 100) < 1e-9)
    failures += not print_rule("Long-only (lowest weight)", values["lowest_weight"], values["lowest_weight"] >= 0)
    failures += not print_rule(
        f"Reserve >= {reserve_minimum_percent():.1f}%", values["reserve_eligible"],
        values["reserve_eligible"] >= reserve_minimum_percent(),
    )
    failures += not print_rule(
        f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.0f}%",
        values["liquid_weight"], values["liquid_weight"] >= MINIMUM_LIQUID_SHARE,
    )
    failures += not print_rule(
        f"Largest single company <= {ISSUER_LIMIT:.0f}%", values["largest_company"],
        values["largest_company"] <= ISSUER_LIMIT,
    )
    print("  Calendar-year loss                         requires CIO clarification")
    if failures == 0:
        print("  Verdict                                    passes every checkable rule")
    else:
        print(f"  Verdict                                    fails {failures} rule(s)")


def main() -> None:
    candidates = deepcopy(CANDIDATES)
    if "--probe-long-only" in sys.argv:
        candidates = {"A probe": candidates["A"]}
        candidates["A probe"]["Cash"] = -2
        candidates["A probe"]["Global equity index fund"] = 64
        print("Long-only probe: Cash changed to -2.0; global equity index fund changed to 64.0.")

    print(f"Reserve minimum: {reserve_minimum_percent():.1f}% of the portfolio")
    for name, weights in candidates.items():
        check_candidate(name, weights)


if __name__ == "__main__":
    main()
