# Lab 10 — Williams-Sonoma (WSM) Five-Year Pro Forma

**Units:** USD millions except ratios and per-share amounts.  **Forecast years:** FY2026E–FY2030E.  The forecast begins with FY2025 audited revenue and the August 2, 2026 reported balance sheet.

## Sources and three-year history

- [FY2023 Form 10-K, Item 8](https://www.sec.gov/Archives/edgar/data/719955/000162828024012221/wsm-20240128.htm) (year ended January 28, 2024)
- [FY2024 Form 10-K, Item 8](https://www.sec.gov/Archives/edgar/data/719955/000162828025015037/wsm-20250202.htm) (year ended February 2, 2025)
- [FY2025 Form 10-K, Item 8](https://www.sec.gov/Archives/edgar/data/719955/000071995526000059/wsm-20260201.htm) (year ended February 1, 2026)
- [Q2 FY2026 Form 10-Q, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/719955/000071995526000208/wsm-20260802.htm) (August 2, 2026 opening balance sheet)

| Line | FY2023 | FY2024 | FY2025 |
| --- | ---: | ---: | ---: |
| Revenue | 7,750.652 — FY23 10-K, Statements of Earnings | 7,711.541 — FY24 10-K, Statements of Earnings | 7,806.816 — FY25 10-K, Statements of Earnings |
| Gross profit | 3,303.601 — FY23 10-K, Statements of Earnings | 3,582.299 — FY24 10-K, Statements of Earnings | 3,603.051 — FY25 10-K, Statements of Earnings |
| SG&A | 2,059.408 — FY23 10-K, Statements of Earnings | 2,152.115 — FY24 10-K, Statements of Earnings | 2,187.329 — FY25 10-K, Statements of Earnings |
| Net earnings | 949.762 — FY23 10-K, Statements of Earnings | 1,125.251 — FY24 10-K, Statements of Earnings | 1,088.437 — FY25 10-K, Statements of Earnings |
| Merchandise inventory, net | 1,246.369 — FY23 10-K, Balance Sheets | 1,332.429 — FY24 10-K, Balance Sheets | 1,462.849 — FY25 10-K, Balance Sheets |
| PP&E, net | 1,013.189 — FY23 10-K, Balance Sheets | 1,033.934 — FY24 10-K, Balance Sheets | 1,095.158 — FY25 10-K, Balance Sheets / Note B |
| Stockholders’ equity | 2,127.861 — FY23 10-K, Balance Sheets | 2,142.419 — FY24 10-K, Balance Sheets | 2,082.559 — FY25 10-K, Statements of Stockholders’ Equity |

I verified in the FY2025 filing the reported revenue and net earnings and in the FY2023 filing the reported inventory and PP&E. No data-provider field was supplied, so the data-provider capex field is unresolved rather than substituted with an unverified number.

## Historical ratios

Inventory days = ending inventory / reported COGS × 365. D&A / PP&E uses cash-flow-statement D&A divided by ending net PP&E; this follows the filing’s reported D&A convention.

| Ratio / metric | FY2023 | FY2024 | FY2025 | Source / calculation |
| --- | ---: | ---: | ---: | --- |
| Gross margin | 42.6% | 46.5% | 46.2% | Gross profit / revenue; each 10-K Statements of Earnings |
| SG&A / gross profit | 62.3% | 60.1% | 60.7% | SG&A / gross profit; each 10-K Statements of Earnings |
| Inventory days | 102.3 | 117.8 | 127.0 | Ending inventory / COGS × 365; each 10-K |
| D&A / PP&E | 23.0% | 22.2% | 21.1% | Cash-flow D&A / ending PP&E; each 10-K |
| Capital spending, filing line | 188.458 | 221.567 | 259.438 | “Purchases of property and equipment,” Statements of Cash Flows |
| Capital spending, data-provider field | Unresolved | Unresolved | Unresolved | No provider or field was supplied |
| Effective tax rate | 25.4% | 24.3% | 25.1% | Income taxes / earnings before income taxes |
| Reported revenue growth | (10.6%) | (0.5%) | 1.2% | MD&A annual net-revenue comparison |
| Comparable-brand revenue growth | (9.9%) | (1.6%) | 3.5% | MD&A “Comparable Brand Revenue” table |

Comparable-brand growth is an organic operating measure, not the same as reported revenue growth. WSM’s measure captures comparable e-commerce, catalog, and store sales while excluding specified non-comparable operations; it also has 52-week/53-week comparison conventions. See [FY2025 10-K, MD&A—Comparable Brand Revenue](https://www.sec.gov/Archives/edgar/data/719955/000071995526000059/wsm-20260201.htm). I use reported revenue as the forecast base and use comparable-brand growth as context for the growth judgment, rather than treating the two measures as interchangeable.

## Forecast assumptions

| Assumption | Value | Label | Reason |
| --- | --- | --- | --- |
| Revenue growth | 5.95%, 4.0%, 3.5%, 3.0%, 3.0% | FY2026 guidance midpoint / judgment | FY2026 is the midpoint of [management’s 4.7%–7.2% guidance](https://ir.williams-sonomainc.com/investor-information/news-releases/news-release-details/2026/Williams-Sonoma-Inc--announces-strong-second-quarter-2026-results/default.aspx). I then fade growth as the company matures rather than assume the one-year guidance persists. |
| Gross margin | 45.5% | Judgment | It is near recent history but below FY2025’s 46.2%; I chose it to avoid projecting a tariff-refund-affected margin as normal. |
| Cash SG&A / gross profit | 54.3% | History | FY2025 reported SG&A less D&A, divided by FY2025 gross profit. Cash SG&A prevents D&A from being counted twice. |
| Depreciation / opening PP&E | 21.1% | History | FY2025 reported D&A / ending PP&E, applied to opening PP&E in each forecast year. |
| Capital spending | 260.0 annually | Judgment | Held close to FY2025 reported capex of 259.438. |
| Tax rate | 25.1% | History | FY2025 income taxes / pretax earnings. |
| Inventory days | 127.0 days | History | FY2025 ending inventory / COGS × 365; I retain the latest, higher level rather than assume an immediate reversal. |
| Other working capital | 0.5% of revenue change | Judgment | A modest incremental working-capital investment avoids assuming all growth is cash-free. |
| Dividends | 325.0 annually | Judgment | Near FY2025 cash dividend level; held constant for a transparent capital-return assumption. |
| **Share repurchases** | **500.0 annually** | **Judgment / WSM-specific line** | WSM’s company-specific financing/capital-allocation line is repurchases. It is set below FY2025’s unusually large repurchase level. |
| Floor-plan financing | None | History | WSM has no floor-plan financing: it is a home-products retailer rather than an auto dealer. [FY2025 10-K, Note C—Borrowing Arrangements](https://www.sec.gov/Archives/edgar/data/719955/000071995526000059/wsm-20260201.htm#BorrowingArrangements) reports no credit-facility borrowing, so no floor-plan or revolver balance is projected. |
| Financial debt | 0.0 | History / model convention | The existing equity bridge contains no financial debt; operating leases remain in aggregated other liabilities. |
| Cost of equity / terminal growth | 10.0% / 3.0% | Judgment | These preserve the existing WSM DCF convention. The terminal-growth assumption requires care because it drives much of the result. |
| Shares outstanding | 117.779173 million | Fact | Common shares outstanding reported August 23, 2026 in the Q2 FY2026 10-Q. |

## Pro forma statements

### Income statement

| $ millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| Revenue | 8,271.3 | 8,602.2 | 8,903.3 | 9,170.3 | 9,445.5 |
| Gross profit | 3,763.5 | 3,914.0 | 4,051.0 | 4,172.5 | 4,297.7 |
| Cash SG&A | 2,043.6 | 2,125.3 | 2,199.7 | 2,265.7 | 2,333.6 |
| Depreciation | 236.7 | 241.6 | 245.5 | 248.5 | 251.0 |
| Operating income | 1,483.2 | 1,547.1 | 1,605.8 | 1,658.3 | 1,713.1 |
| Taxes | 372.3 | 388.3 | 403.1 | 416.2 | 430.0 |
| Net income | 1,110.9 | 1,158.8 | 1,202.8 | 1,242.1 | 1,283.1 |

### Balance sheet

| $ millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cash | 1,168.2 | 1,419.1 | 1,723.8 | 2,077.4 | 2,472.9 |
| Inventory | 1,568.5 | 1,631.2 | 1,688.3 | 1,739.0 | 1,791.1 |
| PP&E, net | 1,145.0 | 1,163.4 | 1,177.9 | 1,189.4 | 1,198.4 |
| Other assets | 1,910.6 | 1,912.2 | 1,913.8 | 1,915.1 | 1,916.5 |
| Total assets | 5,792.2 | 6,126.0 | 6,503.8 | 6,920.8 | 7,378.9 |
| Other liabilities | 3,365.4 | 3,365.4 | 3,365.4 | 3,365.4 | 3,365.4 |
| Equity | 2,426.8 | 2,760.6 | 3,138.4 | 3,555.4 | 4,013.5 |
| Liabilities + equity | 5,792.2 | 6,126.0 | 6,503.8 | 6,920.8 | 7,378.9 |

### Cash flow / FCFE bridge

| $ millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| Net income | 1,110.9 | 1,158.8 | 1,202.8 | 1,242.1 | 1,283.1 |
| Depreciation | 236.7 | 241.6 | 245.5 | 248.5 | 251.0 |
| Capital spending | (260.0) | (260.0) | (260.0) | (260.0) | (260.0) |
| Change in inventory | (121.1) | (62.7) | (57.1) | (50.6) | (52.2) |
| Change in other working capital | (2.3) | (1.7) | (1.5) | (1.3) | (1.4) |
| FCFE | 964.2 | 1,076.0 | 1,129.6 | 1,178.6 | 1,220.5 |
| Dividends | (325.0) | (325.0) | (325.0) | (325.0) | (325.0) |
| Share repurchases | (500.0) | (500.0) | (500.0) | (500.0) | (500.0) |

WSM has positive FCFE in every forecast year. If FCFE became negative, I would build and label that year as **negative FCFE**, but would not calculate a Gordon-growth terminal value from a negative cash-flow base because it is not a meaningful sustainable positive-cash-flow input.

## Validation and value

I ran `python3 wsm_proforma.py` after preparing this file. `assert_balanced()` remains in the model and raises a year-specific error when the absolute balance-sheet gap exceeds $0.05 million. The run produced a **$0.0 million assets − liabilities − equity gap in every forecast year**, cash of $1,168.2 million to $2,472.9 million, and therefore positive cash in every year. No revolver is modeled or required.

At a 10.0% cost of equity and 3.0% terminal growth, the model produces equity value of $15,328.48 million, with 72.7% of value after FY2030, or **$130.15 per share**. WSM traded at **$228.62 per share on September 24, 2026** (intraday quote; [price source](https://www.investing.com/equities/williams-sonoma-inc)). Given $130.15 from this model versus that market price, what assumptions about durable margins, growth, capital returns, or discount rate would have to change before I would view the difference differently?

## Reflection

The model is mechanically sound, but that does not make its assumptions true. The key judgment is whether WSM can sustain a roughly 45.5% gross margin while growth fades and repurchases remain meaningful. The 72.7% terminal-value share makes the result particularly sensitive to the cost of equity and terminal-growth assumptions, so I would not treat the output as a stand-alone answer.

## Partner Review — complete after the actual exchange

**Partner’s attack on my model:** “Why did you assume a 45.5% gross margin for all five years? What would make you change that?”

**My two-sentence response:** I used 45.5% because it is close to Williams-Sonoma’s recent margins, but avoids assuming some of the unusual tariff benefits will continue. I would lower it if costs or tariffs increased and WSM was not able to offset them through pricing.

**My attack on the partner’s model:** “Why did you assume Tesla’s revenue growth stays at that level, and what would make you change it?”
