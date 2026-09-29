# Lab 11 — Pro-Forma Sensitivity: Williams-Sonoma (WSM)

**Files submitted:** `Lab11_WSM_Sensitivity.md` and `wsm_proforma.py`  
**Units:** USD millions except percentages and per-share values.  
**Cash-flow measure:** FCFE.

## Base case and partner exchange 1 — prediction

The full base input set and visible FY2026E–FY2030E statements are in `wsm_proforma.py` and [Lab 10](Lab10_WSM_ProForma.md). The base case has FY2030 operating income of $1,713.1 million, FY2030 FCFE of $1,220.5 million, and value per share of $130.15; all annual balance-sheet gaps are $0.0 million within rounding.

**My prediction:** I expected the revenue-growth path to have the largest effect over my stated ranges because it compounds through all five forecast years. Revenue changes gross profit, cash SG&A, inventory, working capital, operating income, FCFE, and terminal value.

**Partner repeat and question:** My partner repeated that revenue growth changes WSM’s sales first, then linked margin, inventory, and cash-flow lines, rather than directly changing value. The partner asked what supports the revenue-growth range; my answer was that FY2026’s 5.95% base is management-guidance midpoint and the later fade is judgment, while the ±2.0-percentage-point annual change is a transparent sensitivity range rather than a probability estimate.

## Independent drivers and ranges

| Driver | Low | Base | High | Units and affected years | Range basis |
| --- | --- | --- | --- | --- | --- |
| Revenue-growth path | 3.95%, 2.00%, 1.50%, 1.00%, 1.00% | 5.95%, 4.00%, 3.50%, 3.00%, 3.00% | 7.95%, 6.00%, 5.50%, 5.00%, 5.00% | % by FY2026E–FY2030E | Each case is a 2.0-percentage-point shift in every year from the base path. FY2026 base is WSM guidance midpoint; later years are judgment. |
| Gross margin | 43.50% | 45.50% | 47.50% | % in each forecast year | A ±2.0-percentage-point judgment range around base. FY2023–FY2025 reported margins were 42.6%, 46.5%, and 46.2%; tariff-related effects make future margin uncertain. |

These are independent assumptions from the WSM input set, not calculated statement totals. The ranges and source support are retained in [Lab 10’s assumption table](Lab10_WSM_ProForma.md#forecast-assumptions).

## Locked Changed-Input Record

**Locked:** September 29, 2026, 13:45 EDT, before the exact changed case ran.

| Item | Record |
| --- | --- |
| Input change | Gross margin in FY2026E–FY2030E: 45.5% → 44.0%, a 1.5-percentage-point decrease in each year. |
| Inputs held at base | Revenue growth, cash SG&A ratio, depreciation rate, capex, tax rate, inventory days, other working capital, dividends, repurchases, cost of equity, terminal growth, and shares. |
| Prediction | FY2030 operating income down about $65 million; FY2030 FCFE down about $50 million; value per share down about $5–$7. |
| Actual | Operating income: $1,713.1M → $1,648.3M (−$64.7M using unrounded output); FCFE: $1,220.5M → $1,170.6M (−$49.9M); value/share: $130.15 → $124.44 (−$5.70). All annual accounting gaps stayed $0.0M within rounding and cash stayed positive. |
| Prediction reconciliation | Actual operating-income and FCFE changes were $0.3M and $0.1M smaller than the rough prediction; the $5.70 share-value change fell inside the predicted $5–$7 range. |

## Visible one-at-a-time sensitivity output

Every scenario begins with a fresh independent copy of `BASE_INPUTS`; only the named driver changes. Linked accounting items then recalculate.

| Driver / case | Actual input | FY2030 operating income | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base | Checks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Revenue growth — low | 3.95%, 2.00%, 1.50%, 1.00%, 1.00% | 1,531.2 | (181.9) | 1,121.3 | (99.2) | $121.16 | ($8.99) | Pass: all gaps $0.0; cash positive |
| Revenue growth — base | 5.95%, 4.00%, 3.50%, 3.00%, 3.00% | 1,713.1 | 0.0 | 1,220.5 | 0.0 | $130.15 | $0.00 | Pass: all gaps $0.0; cash positive |
| Revenue growth — high | 7.95%, 6.00%, 5.50%, 5.00%, 5.00% | 1,909.6 | 196.5 | 1,324.9 | 104.4 | $139.58 | $9.43 | Pass: all gaps $0.0; cash positive |
| Gross margin — low | 43.50% each year | 1,626.7 | (86.3) | 1,153.9 | (66.6) | $122.54 | ($7.60) | Pass: all gaps $0.0; cash positive |
| Gross margin — base | 45.50% each year | 1,713.1 | 0.0 | 1,220.5 | 0.0 | $130.15 | $0.00 | Pass: all gaps $0.0; cash positive |
| Gross margin — high | 47.50% each year | 1,799.4 | 86.3 | 1,287.1 | 66.6 | $137.75 | $7.60 | Pass: all gaps $0.0; cash positive |

The model restored the unchanged base input set after the six runs and reran it: FY2030 FCFE was $1,220.5 million, value per share was $130.15, and the balance-sheet gap was $0.0 million. This matches the starting base output within stated rounding.

**Selected-result trace:** In the revenue-growth low case, FY2030 revenue was $8,570.5 million, gross profit was $3,899.6 million, cash SG&A was $2,117.5 million, operating income was $1,531.2 million, net income was $1,146.8 million, FCFE was $1,121.3 million, cash was $2,247.3 million, and assets less liabilities less equity was $0.0 million.

## Check and partner exchange 2

I showed the base 45.5% margin case and the 44.0% changed case to my partner. The listener recomputed the reported differences from the model’s unrounded results, confirmed that only gross margin changed, and traced the lower gross profit through lower operating income, net income, FCFE, cash, and equity. The listener also confirmed the accounting check passed every year.

**Question received:** Why is cash SG&A linked to gross profit rather than revenue, and does that double-count depreciation?

**My response:** The model defines cash SG&A as FY2025 reported SG&A less D&A divided by gross profit, then forecasts depreciation separately. Therefore D&A is not counted twice, though the gross-profit linkage is an assumption to revisit rather than a reported WSM cost classification.

**Check I performed on the partner’s Tesla analysis:** I checked that Tesla revenue growth was framed as an independent input rather than a calculated revenue total and asked: “Why did you assume Tesla’s revenue growth stays at that level, and what would make you change it?” I also checked that percentage points in the growth assumption should not be confused with percent changes in revenue. No Tesla scenario table or numerical outputs were supplied, so I did not claim to have recomputed a Tesla output difference.

## Main driver over the tested ranges and partner exchange 3

| Driver | FY2030 operating-income span | FY2030 FCFE span | Value-per-share span |
| --- | ---: | ---: | ---: |
| Revenue-growth path | $378.42M | $203.65M | $18.42 |
| Gross margin | $172.66M | $133.15M | $15.21 |

Over these ranges, the revenue-growth path is the larger driver of FY2030 operating income, FCFE, and value per share. That ranking is conditional: its five-year compounded 2.0-percentage-point path may create a larger span partly because of the range selected, not because revenue growth is inherently more important than gross margin.

**Causal link explained:** Lower revenue growth reduces revenue and gross profit, changes inventory and working capital, and then reduces operating income and FCFE. The lower cash flow reduces the present value of the explicit period and terminal value.

**Question received:** Could the revenue-growth ranking reflect the selected ranges rather than revenue being WSM’s inherently dominant driver?

**My response:** Yes. I would test other evidence-based ranges before making a stronger claim because both the range width and five-year compounding influence the result.

**Partner summary:** Over the stated ranges, revenue growth has the largest spans, but WSM’s margin result remains material and the table does not prove a permanent ranking of economic importance.

WSM’s drivers reflect retail sales, merchandise margin, inventory, and pricing/cost recovery. Tesla may instead be driven by deliveries, pricing, manufacturing cost, and capacity utilization. I do not compare the companies by raw dollar changes.

## Learn on your own and reflection

**What is one-at-a-time sensitivity?** It changes one independent assumption while all other inputs remain at base case, isolating that driver’s linked effects on statements and value.

**How does the chosen range affect the ranking?** A wider input range or a range compounded over more years can create a larger output span. The ranking therefore applies only over the stated ranges.

**Why is a sensitivity table not a forecast probability?** Low, base, and high cases are selected assumptions, not statistically estimated likelihoods. The table answers “what happens if,” not “how likely is each result.”

**Reflection:** I was surprised that the 1.5-percentage-point locked margin reduction lowered value by $5.70 per share even though cash SG&A fell with gross profit. Over the stated ranges, revenue growth mattered most, but the margin test made tariff costs, merchandise costs, and pricing power a priority research question.
