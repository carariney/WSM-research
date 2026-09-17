# FIN 439 Lab 08 — Williams-Sonoma P/E Comparable Analysis

**Target:** Williams-Sonoma, Inc. (NYSE: WSM)  
**Valuation / comparison date:** August 31, 2026 close  
**Method:** Trading P/E using annual reported GAAP diluted EPS  
**Currency and share basis:** USD per common share; closing price divided by total annual GAAP diluted EPS. No cash/debt bridge is applied to a P/E result.

## Peer policy

I will consider publicly traded companies with home-furnishings and home-goods economics similar to Williams-Sonoma. I will qualify or exclude candidates based on material differences in product mix, customer positioning, sales channels, growth, profitability, and earnings quality.

## Source and input ledger

All prices are the **August 31, 2026 regular-market close** in USD. All EPS values used in the calculator are **reported GAAP diluted EPS for the latest completed fiscal year that was public on or before August 31, 2026**. A full year is required; no quarterly EPS is annualized. `Adjusted` figures are recorded separately and are not substituted for reported EPS.

| Company / role | Aug. 31, 2026 close | Reported annual diluted EPS used | Fiscal year ended | Earnings publication date | Source locator | Adjusted earnings treatment |
| --- | ---: | ---: | --- | --- | --- | --- |
| Williams-Sonoma (WSM), target | $228.25 | $8.84 | February 1, 2026 | March 26, 2026 (FY2025 10-K) | Price: [StockAnalysis, WSM Historical Data — Aug. 31, 2026 row](https://stockanalysis.com/stocks/wsm/history/). EPS: [WSM FY2025 Form 10-K — Consolidated Statements of Earnings / Note G, Earnings Per Share](https://www.sec.gov/Archives/edgar/data/719955/000071995526000059/wsm-20260201.htm). | **Not used.** FY2026 Q2 non-GAAP diluted EPS was $2.10, but it is one quarter and is not annual earnings; the quarter also contained tariff-refund-related items. [WSM Q2 FY2026 earnings release — GAAP to non-GAAP reconciliation](https://ir.williams-sonomainc.com/investor-information/news-releases/news-release-details/2026/Williams-Sonoma-Inc--announces-strong-second-quarter-2026-results/default.aspx) |
| RH (RH), qualified peer | $149.15 | $6.31 | January 31, 2026 | March 31, 2026 results release; April 1, 2026 10-K filing | Price: [Yahoo Finance, RH Historical Data — Aug. 31, 2026 row](https://ca.finance.yahoo.com/quote/RH/history/). EPS: [RH FY2025 Form 10-K — Consolidated Statements of Income](https://ir.rh.com/financials-filings/sec-filings/content/0001104659-26-037992/rh-20260131x10k.htm). Publication: [RH FY2025 results release](https://ir.rh.com/news-events/detail/280/rh-reports-fourth-quarter-and-fiscal-year-2025-results). | **Not used.** RH disclosed adjusted diluted EPS of $6.29 separately; the calculator uses reported GAAP $6.31. [RH proxy — “Reconciliation of Diluted Net Income per Share to Adjusted Diluted Net Income per Share”](https://www.sec.gov/Archives/edgar/data/1528849/000110465926054988/rh-20260618xdef14a_c.pdf) |
| Arhaus (ARHS), qualified peer | $8.71 | $0.48 | December 31, 2025 | February 26, 2026 | Price: [StockAnalysis, ARHS Historical Data — Aug. 31, 2026 row](https://stockanalysis.com/stocks/arhs/history/). EPS and publication: [Arhaus FY2025 Form 10-K — Consolidated Statements of Comprehensive Income; signature date](https://www.sec.gov/Archives/edgar/data/1875444/000187544426000010/arhs-20251231.htm). | **Unresolved, not used.** No annual adjusted diluted-EPS figure has been verified in the reviewed annual filing; its reported GAAP EPS is used instead. |

The price providers are secondary historical-price sources; the annual EPS and publication dates are drawn from the companies' SEC filings or investor-relations releases. The closes and EPS amounts are all USD-per-share inputs, so the calculator does not mix currencies or basic/diluted share bases.

## Candidate investigation and disposition

| Candidate | Disposition | Business-model evidence and source locator | Reason under the policy |
| --- | --- | --- | --- |
| RH | **Qualify — included in calculator** | [RH FY2025 Form 10-K — Item 1, “Business—Overview,” “Sales Channels,” and “Gallery Transformation”](https://ir.rh.com/financials-filings/sec-filings/content/0001104659-26-037992/rh-20260131x10k.htm) describes a home-furnishings retailer selling through galleries, websites, Sourcebooks, trade/contract, and outlets. | The integrated home-furnishings and omni-channel sales model is relevant. RH is nonetheless a luxury lifestyle brand with hospitality in galleries and a different capital/growth profile, so it is qualified rather than treated as equivalent to WSM's broader multi-brand platform. |
| Arhaus | **Qualify — included in calculator** | [Arhaus FY2025 Form 10-K — Item 1, “Business—Overview” and “Highly Experiential, Integrated Omni-Channel Model”](https://www.sec.gov/Archives/edgar/data/1875444/000187544426000010/arhs-20251231.htm) describes direct design/sourcing of furniture and décor, showrooms, e-commerce, catalog, interior design, and direct-to-trade sales. | The premium home-furnishings, design/sourcing, and omni-channel economics are relevant. Arhaus is a principally single premium brand with materially smaller scale and potentially different growth/profitability economics, so it remains qualified. |

**Excluded candidates:** None investigated in this record. This is not a blank limitation: the two candidates investigated both meet the stated operating-model screen only with the qualifications above. A new candidate must be added to this table with a use/qualify/exclude decision and business evidence before it enters the calculator.

## WSM P/E calculation

```text
Peer P/E = August 31, 2026 closing price / reported annual GAAP diluted EPS
Implied WSM price = peer P/E × WSM FY2025 reported GAAP diluted EPS ($8.84)
```

| Peer | Calculation | P/E |
| --- | --- | ---: |
| RH | $149.15 / $6.31 | 23.637084x |
| Arhaus | $8.71 / $0.48 | 18.145833x |

| Statistic | Peer P/E | Implied WSM price |
| --- | ---: | ---: |
| Minimum | 18.145833x | $160.41 |
| Median | 20.891459x | $184.68 |
| Maximum | 23.637084x | $208.95 |

The peer-P/E-implied WSM range is **$160.41–$208.95 per share**, with a **$184.68 median reference**. It is traced only to WSM's $8.84 FY2025 reported diluted EPS and the two qualified WSM candidates above; no Asbury inputs are used.

## Valuation comparison and skeptical review

| Method | WSM result and date | Main assumption or limitation |
| --- | --- | --- |
| Week 3 DCF | **$119.94–$196.93 per diluted share** sensitivity range; base case **$147.54**. The saved DCF documents its valuation date as **September 9, 2026**. [Saved DCF analysis](Lab06_WSM.md#dcf-value-and-reasonableness) | The range depends on the five-year FCFF growth path, 10.0% WACC, and 2.0%–4.0% terminal-growth sensitivity. Terminal value is 72.4% of base-case enterprise value, making the long-run cash-flow and discount-rate assumptions especially consequential. |
| Peer P/E | **$160.41–$208.95 per share**; **$184.68 median reference**. Prices are as of **August 31, 2026**. | The result depends on retaining RH and Arhaus as qualified peers and applying their annual **reported GAAP diluted EPS** multiples to WSM's FY2025 reported GAAP diluted EPS of $8.84. The peer set is only two observations, and WSM's later Q2 FY2026 GAAP results contain tariff-refund-related effects that are not represented in the annual EPS denominator. |

### Skeptical colleague review

The weakest supported assumption is that two qualified peers—RH and Arhaus—can provide a stable P/E range for WSM despite material differences in luxury/premium positioning, scale, brand architecture, and potentially profitability. Their P/E spread alone produces a $48.54 implied-WMS price range. That is a supported limitation, not evidence that either endpoint is more defensible.

There is a **date mismatch**: the saved DCF is dated September 9, 2026, while the peer P/E uses August 31, 2026 prices. These results should be compared as separate dated observations, not treated as a single same-date valuation set until the date convention is reconciled. There is no company mismatch: both methods value WSM common equity on a per-diluted-share basis. There is, however, an **earnings-definition mismatch** across methods: the DCF values forecast FCFF (an enterprise cash-flow measure bridged to equity), while P/E applies peer market multiples to WSM's historical FY2025 reported GAAP diluted EPS. This is a normal cross-method difference, but it means the two outputs should not be averaged or treated as interchangeable evidence. The P/E denominator also deliberately excludes a one-quarter FY2026 non-GAAP figure rather than annualizing it.

**Decision-changing question:** After normalizing WSM's FY2026 tariff-refund effects, do you still expect sustainable earnings power above the FY2025 $8.84 GAAP diluted EPS used in the P/E analysis?

**Response:** **Unresolved.** I do not yet have sufficient normalized full-year FY2026 evidence to conclude that sustainable earnings power exceeds FY2025's $8.84 diluted EPS. I will reassess after additional results clarify whether the tariff-related effects are recurring.

## Validation and peer-removal test

| Validation check | Result |
| --- | --- |
| Price date and currency | Pass. WSM, RH, and Arhaus use August 31, 2026 USD closing prices. |
| Earnings definition and timing | Pass, subject to disclosed fiscal-year differences. Each denominator is the latest **completed annual reported GAAP diluted EPS** public by August 31, 2026; no quarterly or adjusted EPS is used in the calculation. |
| Equity-multiple consistency | Pass. Price per common share is divided by diluted EPS, and the resulting P/E is applied directly to WSM diluted EPS. No enterprise-value or net-debt bridge is added. |
| Positive and complete P/E inputs | Pass. WSM, RH, and Arhaus have positive reported annual diluted EPS and positive same-date prices. |
| Arithmetic reproduction | Pass. `python3 lab08_wsm_pe_comps.py` reproduces RH at 23.637084x, Arhaus at 18.145833x, and the $160.41–$208.95 WSM range. |
| Precedent-deal evidence | **Unresolved and not used.** The existing source set contains no qualified transaction with an announcement date, consideration, control context, and compatible earnings/operating denominator. No deal result is inserted or averaged into this analysis. |

Removing RH leaves the Arhaus-only reference of **$160.41**; removing Arhaus leaves the RH-only reference of **$208.95**. The $24.27 movement from the full-peer median in either direction shows that the conclusion depends materially on which qualified peer remains. With only one peer, the output is a reference estimate—not a range and not a sufficient basis to override the disclosed qualifications.

**Hand check:** RH P/E = $149.15 / $6.31 = **23.64x** when rounded, matching the calculator's unrounded **23.637084x**. Removing RH lowers the valuation because RH has the higher P/E. With only Arhaus remaining, its lower multiple is applied to WSM's $8.84 EPS, producing the **$160.41** reference estimate.

## Judgment of the AI criticism

I **accept** the criticism that the two-peer set is the weakest supported valuation input. The source-verified business-model overlap supports investigating RH and Arhaus, but it does not erase their differences from WSM in positioning, scale, and brand architecture. I therefore retain both as **qualified**, report the removal test, and do not elevate the median to a precise estimate.

I **accept** the date criticism. The DCF's September 9 valuation date and the P/E's August 31 price date are not identical. I will not describe them as a synchronized valuation or mechanically combine them. I **partly accept** the earnings-definition criticism: FCFF in the DCF and GAAP EPS in P/E are different but method-appropriate denominators. The limitation is comparability and normalization, not a formula error. The documented Q2 tariff-refund effects make that normalization question especially important.

## Final conditional call and reflection

**Call: watch / defer; do not initiate on this evidence set.** At the respective dates, WSM's August 31 market close of $228.25 exceeds the P/E range of $160.41–$208.95, and the September 9 market close of $227.52 exceeds the DCF sensitivity range of $119.94–$196.93. These are separate comparisons, not a blended target price.

**Condition to reconsider:** Reassess after evidence shows that post-tariff-refund earnings are sustainable and either (a) WSM's market price provides a margin of safety against a refreshed, same-date valuation or (b) normalized operating performance supports revising the forecast and peer-earnings basis.

**Reflection:** The spread between methods and within the two-peer P/E set is information about uncertainty, not a problem solved by averaging. The next useful research step is to normalize WSM's earnings after the tariff-related effects and refresh both methods to one shared valuation date; a qualified deal method remains unresolved until appropriate transaction evidence is researched.

## Required process confirmation — student action

The following are process requirements, not claims this Markdown can prove. Confirm each personally before submission:

- [ ] I wrote my **initial** target/date/peer policy before receiving AI peer suggestions.
- [ ] I independently sent that target, valuation date, and policy to **both required AI partners** and retained or can describe their separate outputs.
- [ ] I explained to a partner that `peer P/E = peer price / peer diluted EPS`, then `implied WSM price = selected peer P/E × WSM diluted EPS`; this is why P/E produces a per-share equity value without a cash/debt bridge.
- [ ] I completed required attendance, truth/AI-use attestation, and submission-receipt steps myself.

These boxes are intentionally unchecked: only the student can truthfully complete them. The WSM calculations and source review in this file do not substitute for the independent-partner or peer-explanation process.

## Reproduction

Run the saved calculator command from the repository root:

```bash
python3 lab08_wsm_pe_comps.py
```

The standalone Lab 08 script's editable inputs contain only WSM, RH, and Arhaus. It preserves unrounded Decimal calculations and prints the minimum, median, and maximum implied prices plus a one-peer removal sensitivity. The earlier Lab 07 calculator remains separate.

> This document is a FIN 43900 learning exercise, not investment research or financial advice.
