# FIN 439 Lab 09 — Asbury Automotive Group Five-Year Pro Forma

**Target:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Forecast period:** FY2026E–FY2030E  
**Model:** Linked income statement, balance sheet, cash-flow statement, and FCFE equity valuation  
**Units:** USD millions, except per-share amounts

## Inputs, convention, and source boundary

The opening balance sheet is ABG's FY2025 reported balance sheet. The model separates cash, inventory, net PP&E, floor-plan debt, term debt, revolver, equity, and balancing aggregate `other assets`/`other liabilities` lines. Debt is current maturities plus long-term debt. The aggregate lines preserve the reported FY2025 opening balance while limiting the forecast to the lines specified in this lab. [ABG FY2025 Form 10-K — Consolidated Balance Sheets, Statements of Income, and Property and Equipment note](https://www.sec.gov/Archives/edgar/data/1144980/000114498026000051/abg-20251231.htm)

| Assumption | Model input | Label |
| --- | ---: | --- |
| Organic revenue growth | 1.8% annually | Judgment |
| Gross margin | 17.05% | Judgment |
| SG&A ÷ gross profit, FY2026E–FY2030E | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment |
| Depreciation ÷ opening PP&E | $82.4 ÷ $3,070.4 | History |
| Non-cash impairment | $120.0 annually | Judgment |
| Capital spending | $250.0 annually | Guidance |
| Tax rate | 25.5% | Judgment |
| Inventory days | $2,135.8 ÷ ($17,999.0 − $3,071.7) × 365 | History |
| Floor plan ÷ inventory | $2,027.0 ÷ $2,135.8 | History |
| Other working capital | 0.8% of annual revenue change | Judgment |
| Minimum cash / revolver limit / rate | $25.0 / $850.0 / 6.0% | History / judgment / judgment |
| Term-debt repayment / buyback | $150.0 / $150.0 annually | Judgment |
| Floor-plan / term-debt interest rate | 4.67% / 5.44% | History |
| Cost of equity / terminal growth | 10.0% / 2.5% | Judgment |
| Shares outstanding | 17.951349 million | Fact: June 30, 2026 10-Q |

`proforma.py` calculates each forecast year in the required order: income statement; all balance-sheet lines except cash; FCFE; then the cash/revolver sweep. Interest uses opening floor-plan debt, term debt, and revolver balances. The revolver draws only to maintain the $25.0 minimum cash balance and is repaid before excess cash accumulates.

## Forecast output and valuation

| Line | FY2026E | FY2030E |
| --- | ---: | ---: |
| Revenue | $18,323.0 | $19,678.3 |
| Operating income | $844.2 | $971.4 |
| Net income | $413.6 | $527.5 |
| Free cash flow to equity | $211.4 | $342.3 |
| Cash, year end | $101.8 | $719.8 |
| Assets − liabilities − equity | $0.0 | $0.0 |
| Equity value | $5,237.34 | — |
| Share of value after FY2030 | 79.8% | — |
| Value per share | $291.75 | — |

The terminal value uses `(FY2030 FCFE + FY2030 debt repayment) × (1 + terminal growth) ÷ (cost of equity − terminal growth)` and is discounted five years. Adding back scheduled repayment prevents the terminal calculation from assuming a perpetual annual paydown that is embedded in the explicit-period FCFE.

## Validation register

| Check | Result |
| --- | --- |
| Known-answer checkpoints | Pass. FY2026E and FY2030E revenue, operating income, net income, FCFE, cash, zero balance-sheet gap, and $291.75 per-share value match the provided answer. |
| Accounting identity | Pass. `assets − liabilities − equity` prints $0.0 in each forecast year. |
| Liquidity constraint | Pass. Ending cash is at or above the $25.0 minimum in each forecast year. |
| Required break test | Pass. Temporarily forcing FY2026 ending cash to $40.4 caused the script to raise `ValueError: 2026: balance sheet gap is -61.4.` The temporary change was removed; the saved model is balanced. |
| Revolver capacity | Pass in the base case. No revolver draw is required; the model would raise an error if a required draw exceeded the $850.0 limit. |
| Valuation precondition | Pass. `assert_balanced` is called for every forecast year before the valuation function runs. |

## Interpretation and limitation

The model is internally linked and mechanically validated, but that does not make the forecast correct. The primary judgment risk is that a constant 17.05% gross margin, 1.8% annual revenue growth, annual $120.0 impairment, and fixed capital-allocation assumptions remain appropriate for ABG through FY2030. In addition, 79.8% of estimated equity value is attributable to cash flow after FY2030, so the cost-of-equity and terminal-growth assumptions are material.

**Conditional conclusion:** The base case implies $291.75 per share. Treat this as a scenario outcome, not a standalone recommendation. Revisit the conclusion if vehicle demand, gross profit per vehicle, floor-plan rates, impairment charges, capital spending, or buyback/debt-repayment policy differs materially from the assumptions above.

## Reproduction

```bash
python3 proforma.py
```

The saved model is [proforma.py](proforma.py). The break test is intentionally not left in the saved file; keeping a known broken statement in the deliverable would invalidate the base-case model.
