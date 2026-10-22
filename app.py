"""Streamlit interface for the reusable portfolio engine.

Run locally with: streamlit run app.py
"""

import io

import streamlit as st

import portfolio


MERIDIAN_RESERVE_MINIMUM = 0.03


def meridian_inputs():
    """Return imported Meridian inputs without duplicating portfolio math."""
    return {
        "assets": portfolio.SLEEVES,
        "returns": portfolio.EXPECTED_RETURNS,
        "volatilities": portfolio.VOLATILITIES,
        "correlations": portfolio.CORRELATIONS,
        "reserve_flags": tuple(asset in portfolio.RESERVE_ELIGIBLE for asset in portfolio.SLEEVES),
    }


def search(inputs, objective, reserve_minimum):
    """Call the engine's required 5-point search."""
    return portfolio.search_lowest_risk_mix(
        inputs["returns"], inputs["volatilities"], inputs["correlations"],
        objective, inputs["reserve_flags"], reserve_minimum,
    )


def result_rows(assets, result):
    """Format an engine result for display without recalculating it."""
    if result is None:
        return []
    rows = [
        {"Asset": asset, "Weight": f"{weight:.1%}"}
        for asset, weight in zip(assets, result["weights"])
    ]
    rows.extend([
        {"Asset": "Expected return", "Weight": f"{result['return']:.2%}"},
        {"Asset": "Volatility", "Weight": f"{result['volatility']:.2%}"},
        {"Asset": "Reserve-eligible weight", "Weight": f"{result['reserve_eligible']:.1%}"},
    ])
    return rows


def show_result(title, assets, result):
    """Display one search result."""
    st.subheader(title)
    if result is None:
        st.error("No mix meets the objective and reserve minimum.")
    else:
        st.dataframe(result_rows(assets, result), hide_index=True, use_container_width=True)


def main():
    st.set_page_config(page_title="Portfolio Mix Finder", layout="wide")
    st.title("Portfolio Mix Finder")
    st.caption("Built with AI help, a learning demonstration, not investment advice.")

    with st.sidebar:
        st.header("Mandate")
        objective_percent = st.number_input("Objective return (%)", 0.0, 100.0, 6.5, 0.1)
        reserve_percent = st.number_input("Reserve minimum (%)", 0.0, 100.0, 3.0, 0.1)
        st.header("Price data")
        upload = st.file_uploader("Upload prices.csv", type="csv")
        last_36 = st.toggle("Use only the last 36 monthly returns", value=False)

    loaded = meridian_inputs()
    loaded_label = "Meridian inputs as loaded"
    if upload is not None:
        try:
            raw_csv = upload.getvalue().decode("utf-8")
            all_months = portfolio.estimate_from_prices_csv(io.StringIO(raw_csv), False)
            selected_months = portfolio.estimate_from_prices_csv(io.StringIO(raw_csv), last_36)
        except (UnicodeDecodeError, ValueError) as error:
            st.error(f"Could not estimate from prices.csv: {error}")
            return
        loaded = {
            "assets": all_months["tickers"],
            "returns": all_months["expected_returns"],
            "volatilities": all_months["volatilities"],
            "correlations": all_months["correlations"],
            "reserve_flags": tuple(False for _ in all_months["tickers"]),
        }
        active = {
            "assets": selected_months["tickers"],
            "returns": selected_months["expected_returns"],
            "volatilities": selected_months["volatilities"],
            "correlations": selected_months["correlations"],
            "reserve_flags": tuple(False for _ in selected_months["tickers"]),
        }
        loaded_label = f"CSV as loaded: all {all_months['monthly_return_observations']} monthly returns"
        st.info(
            f"CSV estimates use {selected_months['monthly_return_observations']} monthly returns. "
            "Historical averages are estimates, not forecasts."
        )
    else:
        active = dict(loaded)

    period_key = "last36" if upload is not None and last_36 else "all_months"
    st.subheader("Edit expected-return estimates and reserve eligibility")
    edited_returns = []
    edited_flags = []
    columns = st.columns(len(active["assets"]))
    for index, (asset, asset_return, default_flag) in enumerate(
        zip(active["assets"], active["returns"], active["reserve_flags"])
    ):
        with columns[index]:
            st.markdown(f"**{asset}**")
            edited_returns.append(st.number_input(
                "Expected return (%)", -100.0, 100.0, float(asset_return * 100), 0.1,
                key=f"return_{asset}_{period_key}",
            ) / 100)
            edited_flags.append(st.checkbox(
                "Reserve-eligible", value=default_flag, key=f"reserve_{asset}",
            ))
    active["returns"] = tuple(edited_returns)
    active["reserve_flags"] = tuple(edited_flags)

    objective = objective_percent / 100
    reserve_minimum = reserve_percent / 100
    baseline = dict(loaded)
    baseline["reserve_flags"] = tuple(edited_flags)
    try:
        changed_result = search(active, objective, reserve_minimum)
        loaded_result = search(baseline, objective, reserve_minimum)
    except ValueError as error:
        st.error(f"The engine could not search these inputs: {error}")
        return

    left, right = st.columns(2)
    with left:
        show_result("Lowest-risk mix for your edited inputs", active["assets"], changed_result)
    with right:
        show_result(loaded_label, loaded["assets"], loaded_result)

    if changed_result is not None and loaded_result is not None:
        largest_change = max(
            abs(after - before)
            for before, after in zip(loaded_result["weights"], changed_result["weights"])
        )
        st.write(f"Largest weight change: **{largest_change:.1%}**.")


if __name__ == "__main__":
    main()
