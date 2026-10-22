# Project 2 price data sources

## Dataset

`prices.csv` contains 60 monthly adjusted-close observations for BIL, IEF, AGG, and ACWI. The rows are oldest first and run from October 2021 through September 2026, the most recently completed month as of the October 22, 2026 download.

The data source is Yahoo Finance's historical chart service. Each ticker was retrieved at monthly frequency with adjusted-close values requested. The download date was October 22, 2026.

| Ticker | Fund | Source | Download date | Date range |
|---|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | [Yahoo Finance historical chart data](https://query2.finance.yahoo.com/v8/finance/chart/BIL?period1=1633046400&period2=1790812800&interval=1mo&events=history&includeAdjustedClose=true) | 2026-10-22 | 2021-10-01 to 2026-09-01 |
| IEF | iShares 7-10 Year Treasury Bond ETF | [Yahoo Finance historical chart data](https://query2.finance.yahoo.com/v8/finance/chart/IEF?period1=1633046400&period2=1790812800&interval=1mo&events=history&includeAdjustedClose=true) | 2026-10-22 | 2021-10-01 to 2026-09-01 |
| AGG | iShares Core U.S. Aggregate Bond ETF | [Yahoo Finance historical chart data](https://query2.finance.yahoo.com/v8/finance/chart/AGG?period1=1633046400&period2=1790812800&interval=1mo&events=history&includeAdjustedClose=true) | 2026-10-22 | 2021-10-01 to 2026-09-01 |
| ACWI | iShares MSCI ACWI ETF | [Yahoo Finance historical chart data](https://query2.finance.yahoo.com/v8/finance/chart/ACWI?period1=1633046400&period2=1790812800&interval=1mo&events=history&includeAdjustedClose=true) | 2026-10-22 | 2021-10-01 to 2026-09-01 |

Historical average returns calculated from these prices are estimates, not forecasts.
