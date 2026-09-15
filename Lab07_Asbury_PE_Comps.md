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

The following policy is the rule for including a peer in this P/E analysis. It should be applied consistently to any additional candidate; an industry label alone is insufficient.

| Dimension | Inclusion logic | Exclusion / qualification logic |
| --- | --- | --- |
| Business model and revenue drivers | Public company whose principal economics are sufficiently similar to ABG's automotive-retail/dealership model. | Exclude companies whose principal business model or revenue drivers are materially different. |
| Geography / regulation | Operates in markets with sufficiently comparable dealership regulation and market structure. | Qualify or exclude if geographic or regulatory differences could materially affect margins, risk, or valuation. |
| Scale and growth | Similar enough in scale and growth profile that the multiple is informative. | Qualify differences in size or growth rather than silently treating them as equivalent. |
| Margins / capital intensity | Comparable profitability and reinvestment characteristics. | Exclude or qualify a candidate when material margin or capital-intensity differences are identified. |
| Leverage / risk | Comparable enough financial-risk profile for P/E to be informative. | Qualify material leverage, cyclicality, or other risk differences because P/E embeds capital structure and below-the-line effects. |
| Metric availability / definition | December 31, 2024 closing price and FY2024 **total GAAP diluted EPS** are available and use matching per-share conventions. | Exclude a candidate with missing, nonpositive, non-GAAP, basic-share, or mismatched-period inputs unless the metric is normalized consistently. |
| Market and reporting dates | Price is measured at the December 31, 2024 close and EPS is FY2024. | Do not mix dates or fiscal-period definitions without explicit normalization and disclosure. |

## Candidate disposition

| Candidate | Basis available in this submission | Disposition | Consequence |
| --- | --- | --- | --- |
| AutoNation (AN) | Supplied as a candidate peer; price and FY2024 GAAP diluted EPS are positive and usable in the P/E calculation. No supporting business-comparability source was supplied. | Qualified candidate used for this mechanical P/E analysis. | Included, subject to later source verification under the policy above. |
| Group 1 Automotive (GPI) | Supplied as a qualified candidate peer; price and FY2024 GAAP diluted EPS are positive and usable in the P/E calculation. No supporting business-comparability source was supplied. | Qualified candidate used for this mechanical P/E analysis. | Included, subject to later source verification under the policy above. |

This document does not state that either company passes every policy criterion as a verified fact; the available inputs establish only their names, stated roles, and calculation fields.

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

- **AI use in this work:** Codex created the standard-library calculation file and drafted this Markdown from the user-supplied inputs and the course materials in this repository. It did not fetch market data, access external sources, or independently verify the supplied figures.
- **Course materials consulted:** [Week 4 student handout](lessons/week-04/student-handout.md), [Lab 07 slides](lessons/week-04/slides-session-07.md), and [training-case worked example](lessons/week-04/teach-comps-worked-example.md).
- **Calculation file:** [`lab07_pe_comps.py`](lab07_pe_comps.py). Running `python3 lab07_pe_comps.py` reproduces the displayed results.
- **Before submitting:** Confirm the Brightspace Lab 07 instructions, complete any required in-person attendance declaration and submission receipt, and make a truthful personal attestation. Those items require the student's own confirmation and are not asserted by this file.

> This document is a FIN 43900 learning exercise, not investment research or financial advice.
