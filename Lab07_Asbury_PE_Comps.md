# FIN 439 Lab 07 — Asbury Automotive P/E Comparable Analysis

**Valuation date:** December 31, 2024 close  
**Target:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Method:** Trading P/E using FY2024 total GAAP diluted EPS  
**Scope:** This submission is a P/E analysis only. It does not calculate EV/EBITDA or use precedent transactions.

## Objective and metric consistency

This analysis estimates an ABG per-share value by applying peer trading P/E multiples to ABG's FY2024 total GAAP diluted EPS. The numerator is each peer's December 31, 2024 closing price; the denominator is the same peer's FY2024 total GAAP diluted EPS. Thus, each P/E pairs a per-share common-equity price with a diluted per-share equity-earnings measure.

Formulae:

```text
Peer P/E = December 31, 2024 closing price / FY2024 total GAAP diluted EPS
Implied ABG price = peer P/E × ABG FY2024 total GAAP diluted EPS
```

P/E is an equity multiple. The implied prices below are therefore direct per-share equity estimates: cash and debt are not added or subtracted. Adding a cash/debt bridge would double-count capital structure.

The calculation convention follows the course guidance on P/E and price/share-based metrics in [the Week 4 handout](lessons/week-04/student-handout.md#multiple-consistency). The course's [worked example](lessons/week-04/teach-comps-worked-example.md#step-4--apply-the-equity-multiple-no-bridge--and-thats-the-trap) likewise states that P/E is applied directly to equity earnings.

## Input ledger

The figures in this table were supplied for this Lab 07 analysis. No primary-source filing, historical-price record, or other independently verifiable source for these figures was included in the course folder or provided with the inputs; they are consequently identified as supplied inputs rather than independently source-verified facts.

| Company / role | December 31, 2024 closing price | FY2024 total GAAP diluted EPS | Input status |
| --- | ---: | ---: | --- |
| Asbury Automotive (ABG), target | $243.03 | $21.50 | Supplied input |
| AutoNation (AN), candidate peer | $169.84 | $16.92 | Supplied input |
| Group 1 Automotive (GPI), qualified candidate peer | $421.48 | $36.81 | Supplied input |

## Peer-selection policy

The following policy is applied consistently to this peer set. The evidence is the companies' FY2024 Form 10-K disclosures, which align with the valuation date and FY2024 EPS convention used in the calculation. An industry label alone is not sufficient.

| Dimension | Inclusion logic | Exclusion / qualification logic |
| --- | --- | --- |
| Business model and revenue drivers | Public franchised automotive retailer with a meaningful mix of new and used vehicles, parts/service, and F&I or related financing products. ABG operates 198 new-vehicle franchises at 152 locations in 14 states, plus collision centers and its TCA F&I-product provider. | Exclude companies whose principal business model or revenue drivers are materially different. [ABG FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm) |
| Geography / regulation | U.S. dealership operations are preferred because ABG's dealerships are in 14 U.S. states. | Qualify a peer with material non-U.S. operations or different regulatory exposure; do not silently treat it as a U.S.-only peer. [ABG FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm) |
| Scale and growth | Large multi-location dealership operator; a difference in location count is disclosed rather than treated as immaterial. | Qualify differences in scale or growth rather than silently treating them as equivalent. |
| Margins / capital intensity | Comparable dealership mix and fixed-operations exposure are required; no conclusion is drawn here that margins are identical. | Qualify a candidate if its reported segment mix or capital intensity differs materially. |
| Leverage / risk | P/E is used only as a trading cross-check because it embeds interest, taxes, financing activities, and other below-the-line effects. | Qualify material financial-services, leverage, cyclicality, or other risk differences; do not bridge P/E with cash or debt. |
| Metric availability / definition | December 31, 2024 closing price and FY2024 **total GAAP diluted EPS** are available and use matching per-share conventions. | Exclude a candidate with missing, nonpositive, non-GAAP, basic-share, or mismatched-period inputs unless the metric is normalized consistently. |
| Market and reporting dates | Price is measured at the December 31, 2024 close and EPS is FY2024. | Do not mix dates or fiscal-period definitions without explicit normalization and disclosure. |

## Peer evidence and disposition

| Candidate | Source-verified case evidence | Disposition | Consequence |
| --- | --- | --- | --- |
| AutoNation (AN) | AutoNation reported 325 new-vehicle franchises at 243 U.S. stores and 31 vehicle brands at December 31, 2024. Its products include new and used vehicles, parts and service, and finance and insurance—directly overlapping ABG's dealership, fixed-operations, and F&I revenue drivers. This is a larger U.S. dealership footprint than ABG's 152 locations, but it is within the same broad franchised-auto-retail model. [AutoNation FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/350698/000035069825000029/an-20241231.htm) · [ABG FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm) | **Appropriate peer, qualified.** The shared U.S. franchised-dealership model and overlapping revenue streams support inclusion. AutoNation also reported an auto finance company, so its P/E may reflect financial-services earnings and risk differently from ABG; the analysis therefore uses it as one observation, not proof that the companies warrant the same multiple. | Included in the two-peer P/E set; retain the qualification when interpreting the median and range. |
| Group 1 Automotive (GPI) | Group 1 reported that it sells/leases new and used cars and light trucks, arranges vehicle financing, sells service and insurance contracts, performs maintenance and repair, and sells parts—an operating model that overlaps ABG's dealership products and services. At December 31, 2024, Group 1 had 145 U.S. dealerships and 114 U.K. dealerships, while ABG operated 152 dealership locations in 14 U.S. states. | **Appropriate peer, more heavily qualified.** The core dealership model supports inclusion, but the 114 U.K. dealerships introduce a non-U.S. geographic and regulatory qualification that ABG's U.S.-only footprint does not share. This is genuine non-comparability to disclose, not a reason to discard inconvenient evidence without a consistent rule. | Included as a qualified observation; the two-peer range and peer-removal test show the effect of relying on it alone. [Group 1 FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1031203/000103120325000013/gpi-20241231.htm) · [ABG FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm) |

Both peers pass the business-model screen, but neither is identical to ABG. AN is qualified for its larger footprint and auto-finance activity; GPI is qualified more heavily for its material U.K. operations. These qualifications explain why the result is an implied range and cross-check rather than a point valuation.

## P/E calculation and implied ABG prices

All calculations retain full precision. Multiples are displayed to six decimal places and prices to cents.

| Peer | Calculation | Peer P/E |
| --- | --- | ---: |
| AutoNation (AN) | $169.84 / $16.92 | 10.037825x |
| Group 1 Automotive (GPI) | $421.48 / $36.81 | 11.450149x |

| Statistic | Peer P/E | Calculation using ABG FY2024 diluted EPS of $21.50 | Implied ABG price |
| --- | ---: | --- | ---: |
| Minimum | 10.037825x | 10.037825x × $21.50 | $215.81 |
| Median | 10.743987x | 10.743987x × $21.50 | $231.00 |
| Maximum | 11.450149x | 11.450149x × $21.50 | $246.18 |

With two peers, the median P/E is the arithmetic midpoint of the two unrounded P/E values. The P/E-implied ABG range is therefore **$215.81–$246.18 per share**, and the median reference estimate is **$231.00 per share**. This range is not mechanically averaged with another valuation method.

## Changed-peer test

The full-peer median-implied price is $231.00 (calculated from unrounded values). Removing either peer leaves one usable peer. Under the calculation convention, that remaining-peer price is a reference estimate, not a range.

| Peer removed | Remaining peer(s) | Remaining median-implied ABG price | Dollar change from full-peer median |
| --- | --- | ---: | ---: |
| AutoNation (AN) | Group 1 Automotive (GPI) | $246.18 | +$15.18 |
| Group 1 Automotive (GPI) | AutoNation (AN) | $215.81 | -$15.18 |

The two-peer set is sensitive: removing either peer shifts the median reference estimate by $15.18. That result is a reason to treat the observed range as a limited P/E cross-check, not a precise standalone valuation conclusion.

## Limitation, action, condition, and reversal trigger

**Limitation.** The analysis contains only two supplied peers and no source evidence in the course folder for their business comparability, the reported EPS figures, or the closing-price figures. P/E also embeds each company's leverage, interest expense, taxes, and other below-the-line items, so differences in those factors can drive the observed multiple spread.

**Action.** Use the $215.81–$246.18 P/E range and $231.00 median only as a provisional trading-comparables cross-check; do not treat it as a final ABG value or combine it mechanically with DCF or deal values.

**Condition for use.** Retain a peer only after its December 31, 2024 close, FY2024 total GAAP diluted EPS, and the policy criteria above are verified from appropriate source material using matching dates and definitions.

**Reversal trigger.** Remove or requalify the conclusion if source verification shows a mismatched/non-GAAP/basic-share EPS measure, an incorrect price date, a nonpositive input, or a material business-model, regulatory, scale, margin, capital-intensity, leverage, or risk difference inconsistent with the stated policy.

## AI-use record and submission checks

- **AI use in this work:** Codex created the standard-library calculation file and drafted this Markdown from the user-supplied inputs and the course materials in this repository. For the peer-selection explanation, it accessed the linked FY2024 SEC Form 10-K filings to verify business-model, footprint, and geographic facts. It did not fetch market-price data or replace the supplied price/EPS inputs.
- **Course materials consulted:** [Week 4 student handout](lessons/week-04/student-handout.md), [Lab 07 slides](lessons/week-04/slides-session-07.md), and [training-case worked example](lessons/week-04/teach-comps-worked-example.md).
- **Calculation file:** [`lab07_pe_comps.py`](lab07_pe_comps.py). Running `python3 lab07_pe_comps.py` reproduces the displayed results.
- **Before submitting:** Confirm the Brightspace Lab 07 instructions, complete any required in-person attendance declaration and submission receipt, and make a truthful personal attestation. Those items require the student's own confirmation and are not asserted by this file.

> This document is a FIN 43900 learning exercise, not investment research or financial advice.
