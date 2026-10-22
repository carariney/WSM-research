"""Simple portfolio return, volatility, and reserve-eligibility calculations."""

import csv
from itertools import combinations, product
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


def validate_correlations(correlations, expected_size=None):
    """Raise ValueError unless correlations are square, symmetric, and in [-1, 1]."""
    size = len(correlations)
    if expected_size is None:
        expected_size = size
    if size != expected_size or any(len(row) != size for row in correlations):
        raise ValueError("Correlation table must be square and match the number of assets.")
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


def solve_linear_system(matrix, vector):
    """Solve a square linear system using Gaussian elimination with pivoting."""
    size = len(vector)
    augmented = [list(row) + [value] for row, value in zip(matrix, vector)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("Optimization system is singular for this set of constraints.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return tuple(row[-1] for row in augmented)


def _minimum_variance_candidate(covariance, returns, reserve_flags, target, reserve_minimum,
                                support, return_binds, reserve_binds):
    """Find one equality-constrained minimum-variance candidate on a support set."""
    constraints = [[1.0] * len(support)]
    targets = [1.0]
    if return_binds:
        constraints.append([returns[index] for index in support])
        targets.append(target)
    if reserve_binds:
        constraints.append([reserve_flags[index] for index in support])
        targets.append(reserve_minimum)
    if len(constraints) > len(support):
        raise ValueError("Too many binding constraints for this support set.")

    size = len(support)
    count = size + len(constraints)
    system = [[0.0] * count for _ in range(count)]
    for row, asset_i in enumerate(support):
        for column, asset_j in enumerate(support):
            system[row][column] = 2 * covariance[asset_i][asset_j]
    for constraint_index, constraint in enumerate(constraints):
        for asset_index, value in enumerate(constraint):
            system[asset_index][size + constraint_index] = value
            system[size + constraint_index][asset_index] = value

    solution = solve_linear_system(system, [0.0] * size + targets)
    weights = [0.0] * len(returns)
    for asset_index, value in zip(support, solution[:size]):
        weights[asset_index] = value
    return tuple(weights)


def minimum_variance_weights(covariance, returns, reserve_flags, target, reserve_minimum):
    """Return the lowest-volatility long-only weights meeting return and reserve limits.

    The function enumerates the possible binding return/reserve constraints and
    positive-weight asset sets. Each candidate is solved exactly as a small
    equality-constrained quadratic problem, then tested against all constraints.
    """
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0% and 100%.")
    if len(covariance) != len(returns) or len(returns) != len(reserve_flags):
        raise ValueError("Optimization inputs must have the same number of assets.")

    best_weights = None
    best_variance = None
    asset_indices = range(len(returns))
    tolerance = 1e-9
    for support_size in range(1, len(returns) + 1):
        for support in combinations(asset_indices, support_size):
            for return_binds, reserve_binds in product((False, True), repeat=2):
                try:
                    weights = _minimum_variance_candidate(
                        covariance, returns, reserve_flags, target, reserve_minimum,
                        support, return_binds, reserve_binds,
                    )
                except ValueError:
                    continue
                if any(weight < -tolerance for weight in weights):
                    continue
                if expected_return(weights, returns) < target - tolerance:
                    continue
                if sum(weight * flag for weight, flag in zip(weights, reserve_flags)) < reserve_minimum - tolerance:
                    continue
                variance = portfolio_variance(weights, covariance)
                if best_variance is None or variance < best_variance - tolerance:
                    best_weights = tuple(max(0.0, weight) for weight in weights)
                    best_variance = variance

    if best_weights is None:
        raise ValueError("No long-only mix can meet both the return and reserve constraints.")
    return best_weights


def _five_point_weight_mixes(asset_count, units_left=20):
    """Yield every long-only weight tuple in 5-percentage-point increments."""
    if asset_count == 1:
        yield (units_left / 20,)
        return
    for units in range(units_left + 1):
        for remaining in _five_point_weight_mixes(asset_count - 1, units_left - units):
            yield (units / 20,) + remaining


def search_lowest_risk_mix(returns, volatilities, correlations, objective,
                           reserve_flags, reserve_minimum):
    """Find the lowest-volatility feasible long-only mix in 5-point steps.

    A feasible mix must have expected return at least ``objective`` and a
    reserve-eligible weight at least ``reserve_minimum``. Returns ``None`` if
    no mix meets both requirements.
    """
    asset_count = len(returns)
    if asset_count < 1:
        raise ValueError("At least one asset is required.")
    if len(volatilities) != asset_count or len(reserve_flags) != asset_count:
        raise ValueError("Returns, volatilities, and reserve flags must have the same length.")
    validate_correlations(correlations, asset_count)
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0% and 100%.")

    covariance = covariance_matrix(volatilities, correlations)
    best = None
    for weights in _five_point_weight_mixes(asset_count):
        mix_return = expected_return(weights, returns)
        mix_reserve = sum(weight for weight, eligible in zip(weights, reserve_flags) if eligible)
        if mix_return < objective - 1e-12 or mix_reserve < reserve_minimum - 1e-12:
            continue
        mix_volatility = portfolio_volatility(weights, covariance)
        if best is None or mix_volatility < best["volatility"] - 1e-12:
            best = {
                "weights": weights,
                "return": mix_return,
                "volatility": mix_volatility,
                "reserve_eligible": mix_reserve,
            }
    return best


def estimate_from_prices_csv(csv_source, last_36_months=False):
    """Estimate annualized moments from oldest-first monthly adjusted-close prices.

    ``csv_source`` may be a file path or an open text stream. The first column
    must be dates, followed by one numeric price column per ticker. The estimates
    use simple monthly returns, arithmetic mean times 12, sample standard
    deviation times sqrt(12), and Pearson correlations.
    """
    should_close = False
    if isinstance(csv_source, (str, bytes)):
        csv_source = open(csv_source, "r", newline="", encoding="utf-8")
        should_close = True
    try:
        reader = csv.reader(csv_source)
        header = next(reader, None)
        if header is None or len(header) < 2:
            raise ValueError("CSV needs a date column followed by at least one ticker column.")
        tickers = tuple(name.strip() for name in header[1:])
        if not all(tickers) or len(set(tickers)) != len(tickers):
            raise ValueError("Ticker column names must be present and unique.")
        prices = [[] for _ in tickers]
        for row_number, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise ValueError(f"Row {row_number} has the wrong number of columns.")
            try:
                values = [float(value) for value in row[1:]]
            except ValueError as error:
                raise ValueError(f"Row {row_number} contains a non-numeric price.") from error
            if any(value <= 0 for value in values):
                raise ValueError(f"Row {row_number} contains a non-positive price.")
            for index, value in enumerate(values):
                prices[index].append(value)
    finally:
        if should_close:
            csv_source.close()

    if len(prices[0]) < 3:
        raise ValueError("CSV needs at least three monthly price rows.")
    monthly_returns = [
        tuple(price_series[index] / price_series[index - 1] - 1
              for index in range(1, len(price_series)))
        for price_series in prices
    ]
    if last_36_months:
        monthly_returns = [returns[-36:] for returns in monthly_returns]
    observation_count = len(monthly_returns[0])
    if observation_count < 2:
        raise ValueError("At least two monthly returns are required for an estimate.")

    means = tuple(sum(returns) / observation_count for returns in monthly_returns)
    monthly_stdevs = tuple(
        sqrt(sum((value - mean) ** 2 for value in returns) / (observation_count - 1))
        for returns, mean in zip(monthly_returns, means)
    )
    if any(stdev == 0 for stdev in monthly_stdevs):
        raise ValueError("Each ticker needs price variation to calculate correlations.")
    correlations = [[1.0 if row == column else 0.0 for column in range(len(tickers))]
                    for row in range(len(tickers))]
    for row in range(len(tickers)):
        for column in range(row):
            correlation = sum(
                (monthly_returns[row][index] - means[row]) *
                (monthly_returns[column][index] - means[column])
                for index in range(observation_count)
            ) / ((observation_count - 1) * monthly_stdevs[row] * monthly_stdevs[column])
            correlations[row][column] = correlation
            correlations[column][row] = correlation
    correlations = tuple(tuple(row) for row in correlations)
    validate_correlations(correlations, len(tickers))
    return {
        "tickers": tickers,
        "expected_returns": tuple(mean * 12 for mean in means),
        "volatilities": tuple(stdev * sqrt(12) for stdev in monthly_stdevs),
        "correlations": correlations,
        "monthly_return_observations": observation_count,
    }


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
