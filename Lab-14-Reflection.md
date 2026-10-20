# Lab 14 - Portfolio Baselines Reflection

## 1. Why can two risky assets together be less risky?

Two risky assets can be less risky together because their returns are not perfectly correlated. When one performs poorly, the other may decline less or rise, reducing the combined portfolio's fluctuations.

## 2. What is diversification?

Diversification is spreading investments across assets with different return patterns to reduce portfolio-specific and overall risk.

## 3. Benchmark volatility

Using 40% investment-grade bonds, 60% global equity, and their 0.25 correlation in the portfolio-variance formula produces benchmark volatility of 10.46%.

## 4. Why does inverse volatility put so much into Treasury bills?

Inverse volatility gives the largest weight to Treasury bills because they have the lowest volatility (0.5%). Since weights are proportional to 1 divided by volatility, bills receive 84.3%.

## 5. Which baseline would you show the CIO first?

I would show the benchmark first because its 6.80% expected return clears the 6.5% objective. However, it is not mandate-compliant because its 0% reserve-eligible allocation fails Meridian's 3% reserve minimum.

## 6. What did the code demonstrate?

The code demonstrated that expected return and volatility change with portfolio weights and correlations. Raising the IG-bond/equity correlation from 0.25 to 0.50 increased benchmark volatility from 10.46% to 11.00%.

## 7. What did Candidate E demonstrate?

Candidate E showed that meeting the return target is not enough: it earns 6.80% but fails the reserve rule with 0% reserve-eligible assets.

## 8. Why does the code use covariance?

The code uses covariance because portfolio risk depends on how assets move relative to one another, not only on each asset's own volatility.

## Verified results

| Portfolio | Expected return | Volatility | Reserve-eligible weight | Meets 6.5% objective? |
|---|---:|---:|---:|---|
| Benchmark | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 3.77% | 1.05% | 90.3% | No |

The benchmark was added as Candidate E in `mandate.py`; it fails Meridian's 3.0% minimum reserve rule because its reserve-eligible weight is 0.0%.

## Funds for Thursday

| Ticker | Fund name | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income |
| VT | Vanguard Total World Stock ETF | Equity |
