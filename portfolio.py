"""Simple portfolio return, volatility, and reserve-eligibility calculations."""

from math import sqrt

# Editable course-authored inputs. Values use decimal form (for example, 3.5% is 0.035).
SLEEVES = (
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
)
EXPECTED_RETURNS = (0.035, 0.043, 0.050, 0.080)
VOLATILITIES = (0.005, 0.070, 0.060, 0.160)
CORRELATIONS = (
    (1.00, 0.10, 0.05, 0.00),
    (0.10, 1.00, 0.80, -0.10),
    (0.05, 0.80, 1.00, 0.25),
    (0.00, -0.10, 0.25, 1.00),
)
OBJECTIVE_RETURN = 0.065

RESERVE_ELIGIBLE = ("Treasury bills", "Treasury 10-year note")


def validate_correlations(correlations):
    """Raise ValueError unless correlations are square, symmetric, and in [-1, 1]."""
    size = len(correlations)
    if size != len(SLEEVES) or any(len(row) != size for row in correlations):
        raise ValueError("Correlation table must be square and match the number of sleeves.")
    for row_index, row in enumerate(correlations):
        for column_index, value in enumerate(row):
            if not -1.0 <= value <= 1.0:
                raise ValueError(
                    f"Correlation at row {row_index + 1}, column {column_index + 1} "
                    f"is {value}; correlations must be between -1 and 1."
                )
            if value != correlations[column_index][row_index]:
                raise ValueError("Correlation table must be symmetric.")


def covariance_matrix(volatilities, correlations):
    """Return covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return tuple(
        tuple(correlations[i][j] * volatilities[i] * volatilities[j]
              for j in range(len(volatilities)))
        for i in range(len(volatilities))
    )


def expected_return(weights, returns):
    """Return the weighted expected return."""
    return sum(weight * asset_return for weight, asset_return in zip(weights, returns))


def portfolio_variance(weights, covariance):
    """Return w'Cov(w), including every covariance term."""
    return sum(
        weights[i] * covariance[i][j] * weights[j]
        for i in range(len(weights))
        for j in range(len(weights))
    )


def portfolio_volatility(weights, covariance):
    """Return the square root of portfolio variance."""
    return sqrt(portfolio_variance(weights, covariance))


def reserve_eligible_weight(weights, sleeves, eligible_sleeves):
    """Return the total portfolio weight in the specified reserve-eligible sleeves."""
    return sum(weight for sleeve, weight in zip(sleeves, weights) if sleeve in eligible_sleeves)


def inverse_volatility_weights(volatilities):
    """Weight each sleeve by 1 / volatility and normalize the weights to one."""
    unscaled = tuple(1 / volatility for volatility in volatilities)
    total = sum(unscaled)
    return tuple(weight / total for weight in unscaled)


def portfolio_definitions():
    """Return the three required simple portfolios in sleeve order."""
    return (
        ("Benchmark", (0.0, 0.0, 0.4, 0.6)),
        ("Equal weight", (0.25, 0.25, 0.25, 0.25)),
        ("Inverse volatility", inverse_volatility_weights(VOLATILITIES)),
    )


def print_portfolio(name, weights, covariance):
    """Calculate and print the required metrics for one portfolio."""
    result_return = expected_return(weights, EXPECTED_RETURNS)
    result_volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights, SLEEVES, RESERVE_ELIGIBLE)
    weight_text = " / ".join(f"{weight:.1%}" for weight in weights)
    meets_objective = "yes" if result_return >= OBJECTIVE_RETURN else "no"
    print(f"{name}: {weight_text}")
    print(f"  Expected return: {result_return:.2%}")
    print(f"  Volatility: {result_volatility:.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight:.1%}")
    print(f"  Meets {OBJECTIVE_RETURN:.1%} objective? {meets_objective}")


def main():
    validate_correlations(CORRELATIONS)
    covariance = covariance_matrix(VOLATILITIES, CORRELATIONS)
    print("Weights are bills / 10-year note / IG bond fund / global equity index fund.\n")
    for name, weights in portfolio_definitions():
        print_portfolio(name, weights, covariance)


if __name__ == "__main__":
    main()
