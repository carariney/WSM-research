# Lab 12 — Williams-Sonoma Full Analysis and Review

**Company:** Williams-Sonoma, Inc. (NYSE: WSM)  
**Currency:** USD; financial-statement amounts are millions unless stated otherwise.  
**Supporting files:** [Research and DCF](Lab06_WSM.md) · [Peer P/E](Lab08_WSM_PE_Comps.md) · [Pro forma](Lab10_WSM_ProForma.md) · [Sensitivity](Lab11_WSM_Sensitivity.md) · [Model](wsm_proforma.py)

## 1. Target selection

I selected WSM because it had positive earnings, recognizable brands, understandable home-furnishings retail economics, and sufficient public disclosures to build a forecast and valuation. I wanted to learn how its brand portfolio—Williams Sonoma, Pottery Barn, West Elm, Pottery Barn Kids and Teen, Rejuvenation, and others—works across e-commerce, catalogs, stores, and B2B.

My initial view at the August 31, 2026 valuation date was **watch/defer**. Q2 FY2026 comparable-brand revenue grew 6.2% and WSM had $1.029 billion of cash with no revolving-credit borrowings, but Q2 GAAP EPS included a net $0.74-per-share tariff-refund-related benefit. I did not treat that benefit as sustainable earnings.

## 2. Company and evidence

WSM earns revenue by selling home furnishings, kitchenware, décor, furniture, and gifts through its brands and channels. Demand, comparable-brand sales, e-commerce conversion, store productivity, product mix, pricing, inventory, tariffs, and merchandise costs are the main operating drivers.

The historical evidence comes from WSM’s FY2023, FY2024, and FY2025 10-Ks, plus the Q2 FY2026 10-Q. The fiscal years ended January 28, 2024; February 2, 2025; and February 1, 2026. Relevant data are USD millions except ratios and per-share figures.

| Metric | FY2023 | FY2024 | FY2025 |
| --- | ---: | ---: | ---: |
| Revenue | $7,750.7 | $7,711.5 | $7,806.8 |
| Gross profit | $3,303.6 | $3,582.3 | $3,603.1 |
| Gross margin | 42.6% | 46.5% | 46.2% |
| Net earnings | $949.8 | $1,125.3 | $1,088.4 |
| Inventory days | 102.3 | 117.8 | 127.0 |

The Q2 FY2026 evidence is encouraging but needs normalization: company comparable-brand revenue was +6.2%, e-commerce comp was +6.5%, and retail comp was +5.5%. However, Q2 GAAP gross margin was 51.6%, versus 45.5% non-GAAP, because of tariff-refund-related items. I use the non-GAAP-like 45.5% level as a conservative forecast judgment rather than projecting the unusually high GAAP margin.

## 3. Pro forma

My FY2026E–FY2030E model begins with FY2025 audited revenue and WSM’s August 2, 2026 reported balance sheet. The main assumptions are 5.95%, 4.0%, 3.5%, 3.0%, and 3.0% revenue growth; 45.5% gross margin; 127 inventory days; $260 million annual capex; and $500 million annual share repurchases.

Share repurchases are the WSM-specific capital-allocation line. WSM has no floor-plan financing and no financial debt in the model’s equity bridge; operating leases remain aggregated in other liabilities under the model convention.

Revenue rises from $8,271.3 million in FY2026E to $9,445.5 million in FY2030E. FY2030E operating income is $1,713.1 million and FY2030E FCFE is $1,220.5 million. The statements are linked: revenue changes gross profit, cash SG&A, inventory, working capital, operating income, FCFE, cash, and equity. Assets less liabilities less equity is $0.0 million in every projected year within rounding, cash stays positive, and no revolver is required.

## 4. Valuation

I keep the following values separate because they use different dates, methods, and share bases. I do not average them.

| Method | Result | Valuation date, currency, and share basis | Main limitation |
| --- | ---: | --- | --- |
| FCFF DCF | $119.94–$196.93/share; $147.54 base | September 9, 2026; USD; 123.153M FY2025 diluted shares | Terminal value was 72.4% of base enterprise value. |
| Peer P/E | $160.41–$208.95/share; $184.68 median reference | August 31, 2026; USD/common share; WSM FY2025 reported GAAP diluted EPS of $8.84 | Two qualified peers only: RH and Arhaus. |
| Five-year FCFE pro forma | $130.15/share | Later pro-forma framework; USD; 117.779M August 2026 reported shares | Terminal-period value was 72.7% of total equity value. |

The DCF starts with FY2025 FCFF of $1,055.451 million, forecasts explicit growth of 8%, 6%, 5%, 4%, and 3%, uses a 10.0% WACC and 3.0% terminal growth, and produces enterprise value of $17,149.69 million. Adding $1,019.801 million cash and subtracting $0 financial debt produces equity value of $18,169.49 million, or $147.54 per diluted share. The September 9, 2026 market close was $227.52.

The peer P/E uses RH and Arhaus because both have home-furnishings, design/sourcing, and omni-channel economics, but each differs from WSM in scale, positioning, and brand architecture. The August 31, 2026 WSM market close was $228.25. The P/E method applies annual reported GAAP diluted EPS, not quarterly or adjusted EPS; it requires no enterprise-to-equity bridge because P/E is already an equity-per-share measure.

The reverse DCF returned **no solution** within a uniform −5 to +10 percentage-point explicit-growth shift while holding starting FCFF, WACC, terminal growth, cash, debt, and shares fixed. This means the September 9 market price required more explicit-period growth than that tested range. It is an implied expectation, not proof of mispricing.

## 5. Sensitivity and drivers

I tested two independent inputs one at a time, with all other inputs reset to base for each run.

| Driver | Tested range | FY2030 operating-income span | FY2030 FCFE span | Value-per-share span |
| --- | --- | ---: | ---: | ---: |
| Revenue-growth path | Base path ±2.0 percentage points in each forecast year | $378.42M | $203.65M | $18.42 |
| Gross margin | 43.5%, 45.5%, 47.5% in each forecast year | $172.66M | $133.15M | $15.21 |

Over these ranges, revenue growth has the larger effect on FY2030 operating income, FCFE, and value per share. The causal path is revenue growth → revenue → gross profit, inventory, and working capital → operating income → FCFE → value.

That does not prove revenue growth is inherently WSM’s most important driver. The revenue-growth path compounds over five years, and a different evidence-based range could change the ranking. The gross-margin link is also material: a separately locked change from 45.5% to 44.0% lowered FY2030 operating income by $64.7 million, FCFE by $49.9 million, and value per share by $5.70, from $130.15 to $124.44. All accounting checks still passed.

A sensitivity table is not a probability forecast. It shows what the model does when an input changes, not how likely that input change is.

## 6. Interpretation

My supported conclusion remains **watch/defer; do not initiate on this evidence set**. WSM’s brands, liquidity, positive earnings, and recent comparable-brand growth support continued research. But unusual tariff-related benefits cloud recent profitability, and the date-specific DCF and peer-P/E values were below the corresponding market prices.

I would reconsider if WSM shows sustained comparable-brand growth and non-GAAP margins after the tariff effects roll off, if it demonstrates pricing and sourcing discipline despite merchandise-cost pressure, and if refreshed same-date valuation work offers a margin of safety. My next research priority is normalizing post-tariff earnings, margins, and cash generation.

## Review of Tesla analysis

**Selection and evidence question:** Tesla’s automotive revenue declined 10% while energy revenue grew 27%. Which FY2025 filing table supports the segment revenue and energy gross-margin figures, and how much of the future revenue-growth path depends on energy rather than automotive recovery?

**Model and valuation question:** You describe R&D as a direct FCFE drag in the sensitivity. What evidence would show that incremental R&D is creating future revenue or margin rather than only expense, and where does that upside enter the base forecast?

**Sensitivity and interpretation question:** Over your stated ranges, R&D has the larger value-per-share effect. Could that ranking change if the revenue-growth range were widened or if revenue growth were modeled separately for automotive and energy?

**Evidence check performed:** I recomputed the supplied FY2025 ratios: automotive revenue of $69.5B is 73.3% of $94.8B total revenue; energy revenue of $12.8B is 13.5%; operating cash flow of $14.7B is 15.5%; and capex of $8.5B is 9.0%. These match the supplied rounded percentages. The supplied information does not include a source locator, so the filing section remains to be opened during the live exchange.

**My explanation back:** Tesla’s conventional automotive and FCFE approaches value it at about $28–$39 per share versus the supplied $356.09 market price. The analysis does not say the share price must fall; it says the conventional forecast does not capture enough value to explain the market price unless energy, AI, autonomy, robotics, or stronger future cash flow adds substantial economic value. Over the tested ranges, R&D had the larger value impact, but that ranking is range-dependent.

**Strength:** The analysis separates automotive weakness from energy growth and does not treat higher R&D as automatically bad.

**Improvement:** Add source locators for the FY2025 segment data and document an actual reverse-DCF result when available; do not infer one from the gap to market price.

## Review of Walmart analysis

**Selection and evidence question:** Walmart is described as stable because of scale and operating history. Which FY2024–FY2026 10-K line best supports the historical revenue-growth or operating-margin assumption, and how does e-commerce or membership income change that assumption?

**Model and valuation question:** Why do Target and Costco provide a useful peer range despite their different membership, category, margin, and growth economics? What is the actual Walmart DCF result, discount rate, terminal-growth rate, and reverse-DCF conclusion?

**Sensitivity and interpretation question:** Over the tested ranges, did revenue growth or SG&A as a percent of revenue have the larger impact? Please show the lower/base/higher inputs and outputs before treating the ranking as evidence.

**Evidence check performed:** From the supplied figures, Walmart’s $112.34 market price divided by its 41.147619x P/E implies approximately $2.73 of EPS. Applying that implied EPS to Target’s 18.167531x, the 34.948812x peer median, and Costco’s 51.730093x produces approximately $49.60, $95.42, and $141.23, respectively. Those recomputations match the supplied low, median, and high values within rounding.

**My explanation back:** Walmart’s peer valuation range is wide because Target and Costco have very different P/E multiples. The analysis supports the idea that Walmart is stable but still sensitive to small changes in revenue growth and SG&A because it operates at large scale with relatively thin margins. The exact DCF result and sensitivity ranking are unresolved from the supplied material, so they should not be claimed until shown.

**Strength:** The analysis identifies the peer-dispersion limitation instead of treating the median as precise.

**Improvement:** Add the actual DCF assumptions and result, reverse-DCF result if completed, and the lower/base/higher sensitivity table with output changes.

## Questions received and response as WSM presenter

**Question on evidence:** Why did I use a 45.5% gross margin rather than the unusually high Q2 GAAP margin?  
**Response:** The Q2 GAAP margin included tariff-refund-related items. The 45.5% figure is closer to the reported non-GAAP measure and recent FY2024–FY2025 history, so it avoids projecting a one-time uplift as recurring.

**Question on valuation:** Why do the DCF and P/E methods differ?  
**Response:** The DCF forecasts FCFF and discounts it using WACC and terminal growth, while P/E applies peer market multiples to historical GAAP EPS. They also use different valuation dates, so they are separate evidence rather than inputs to an average.

**Question on sensitivity:** Could revenue growth rank first only because of the range selected?  
**Response:** Yes. The revenue-growth range is compounded across five years, so the ranking applies only over these stated ranges and does not establish permanent economic importance.

## Keep, revise, and investigate after review

- **Keep:** The watch/defer conclusion, because the existing methods remain below their respective dated market prices and tariff normalization remains unresolved.
- **Revise:** I will reconcile future DCF, P/E, and pro-forma comparisons to one common valuation date and state the share basis beside each value.
- **Investigate:** I will focus on post-tariff comparable growth, non-GAAP gross margin, cash conversion, pricing power, and merchandise-cost pressure.
- **Question that made me reconsider:** The question about the 45.5% margin made clear that the margin assumption is not only an input; it is a summary of pricing, sourcing, tariffs, and product mix. I understand better that the forecast needs evidence on each of those mechanisms, not just a historical average.
