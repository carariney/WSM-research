## Decision Boundary and Model Basis

This record supports a buy-side investment-committee decision on whether to initiate a position in Williams-Sonoma, Inc. (NYSE: WSM). The valuation date is **August 31, 2026**. Currency is USD, and financial-statement amounts are in millions unless stated otherwise; per-share amounts and ratios use their stated units.

The final model is `wsm_proforma.py`. It uses information publicly available by August 31, 2026 and values WSM using a five-year linked operating forecast and an FCFF DCF. The model uses **117.779173 million** common shares outstanding, disclosed as of August 23, 2026, for final per-share values. This record documents tests and evidence; it does not convert judgmental inputs into observed facts.

## Data and Convention Ledger

| Material input | Source and date | Treatment in the model | Definition risk or limitation |
| --- | --- | --- | --- |
| FY2025 revenue, EBIT, tax, and capex | WSM FY2025 Form 10-K, filed March 2026 | Base-year anchors: revenue $7,806.816M; EBIT $1,415.722M; capex $259.438M | FY2025 is a reported historical base, not a tariff-normalized FY2026 earnings run rate. |
| Q2 FY2026 tariff effects and guidance | WSM Q2 FY2026 Form 10-Q and earnings release, August 2026 | The tariff refund and related items are not projected as recurring. A 45.5% gross-margin judgment avoids projecting the Q2 GAAP uplift. | A full-year normalized FY2026 result was not available. |
| Cash and financial debt | WSM August 2, 2026 Form 10-Q | Cash is $1,028.936M and financial debt is $0. Operating leases are excluded under the stated convention. | Cash is seasonal; 0%/50%/100% excess-cash sensitivities are necessary. |
| Shares | WSM August 2026 Form 10-Q cover and EPS note | The bridge uses 117.779173M actual common shares outstanding, rather than the 118.892M Q2 weighted-average diluted shares. | Shares are held constant even though forecast repurchases could change future share count. |
| WACC and terminal growth | Student judgment retained from the prior model | Base assumptions are 10.0% WACC and 3.0% terminal growth; 9.0%-11.0% WACC and 2.0%-4.0% terminal-growth sensitivities are shown. | The repository does not contain a sourced CAPM build. These remain valuation judgments. |
| Peer prices and financial inputs | `Lab08_WSM_PE_Comps.md`, linked price sources, and peer filings public by August 31, 2026 | P/E uses annual reported GAAP diluted EPS. EV/EBIT uses market capitalization + interest-bearing debt - cash, divided by reported EBIT. | The qualified peer set has two companies. Lease treatment and different balance-sheet dates require disclosure. |

## Forecast Assumptions and Challenges

| Driver | Value and basis | Why it is challenged | Evidence that would change it |
| --- | --- | --- | --- |
| Revenue growth | 5.95%, 4.0%, 3.5%, 3.0%, and 3.0%; FY2026 begins at the guidance midpoint and then fades by judgment | One year of guidance does not establish five years of growth. | Post-tariff brand and channel growth; updated management guidance. |
| Gross margin | 45.5%; judgment near history and below Q2 GAAP margin | Pricing, sourcing, tariff costs, and mix can materially change margin. | Post-refund merchandise margin and tariff-cost evidence. |
| Cash SG&A / gross profit | 54.3%; derived from FY2025 history | The gross-profit linkage is a model convention, not a reported cost classification. | Updated SG&A classification or margin behavior. |
| D&A / opening PP&E | 21.1%; derived from FY2025 history | Capex mix could change depreciation timing. | Reported capex and depreciation trends. |
| Capex | $260M annually; near FY2025 capex of $259.438M | Growth, systems investment, or store activity could require more capital. | Management capex plan or cash-flow filings. |
| Tax rate | 25.1%; FY2025 effective tax rate | Discrete tax items may make the historical rate unrepresentative. | Updated tax-rate guidance or filings. |
| Inventory days and other working capital | 127 days and 0.5% of revenue change, respectively | Inventory, receivables, and payables may not move as assumed. | Inventory turns, markdowns, and detailed working-capital trends. |
| Dividends and repurchases | $325M dividends and $500M buybacks; judgments near history | Capital returns change cash and potentially future shares. | Board authorization and actual repurchase pace. |
| Excess cash | 100% in the base bridge; 50% alternative and 0% floor | WSM describes cash as seasonal, so the entire balance may not be distributable. | Minimum-operating-cash analysis. |

## Validation Results

The validation suite was rerun from the repository root on **October 16, 2026, at 11:30 EDT** with `python3 validate_wsm_model.py`. It passed the tests below. These checks establish internal consistency and reproducibility; they do not eliminate the investment uncertainty associated with the assumptions above.

| Test | What was tested and result | Why it matters | Evidence |
| --- | --- | --- | --- |
| Synthetic known-answer reconciliation | The Week 3 synthetic DCF reproduced $27.497370 per share and a 72.4014% terminal-value share. | Confirms discounting and enterprise-to-equity signs before WSM inputs are used. | `lessons/week-03/starter/dcf_case.csv`; `lessons/week-03/starter/dcf_expected_output.csv`; `known_answer_dcf_check()` in `validate_wsm_model.py`. |
| Base-year reconciliation | Revenue, gross profit, SG&A, EBIT, net income, and capex match the recorded FY2025 values. | Reduces the risk that the forecast begins from mistyped filing data. | `assert_base_year_reconciliation()` in `wsm_proforma.py`. |
| Five-year pro-forma articulation | Each forecast year has a balance-sheet gap within $0.05M and positive cash; the current run produced $0.0M gaps. | Demonstrates that projected income, cash flow, and balance-sheet lines are linked rather than separately estimated. | `project()` in `wsm_proforma.py`; `validate_wsm_model.py`. |
| FCFF/FCFE reconciliation | FCFF equals FCFE under the stated no-financial-debt and no-interest convention. | Prevents distributions or financing items from being double counted in the valuation. | `assert_valuation_reconciliation()` in `wsm_proforma.py`. |
| Enterprise-to-equity bridge | $15,328.48M enterprise value + $1,028.936M cash - $0 debt = $16,357.42M equity value. | Confirms the sign convention used to convert enterprise value to common equity value. | `validate_wsm_model.py`. |
| DCF monotonicity | Lower WACC increases value, and higher terminal growth increases value. | Detects sensitivity-table logic that moves in an economically implausible direction. | `assert_dcf_directionality()` in `wsm_proforma.py`. |
| Share-count definition | The model uses 117.779173M actual common shares outstanding, not 118.892M Q2 weighted-average diluted shares. | Keeps the valuation denominator aligned with the final equity-value bridge. | WSM Q2 FY2026 Form 10-Q cover and EPS note; `wsm_proforma.py`. |
| Peer-method consistency | P/E uses no cash/debt bridge; EV/EBIT applies a consistent enterprise-value bridge and lease convention across companies. | Avoids mixing equity and enterprise definitions across the comparable methods. | `Lab08_WSM_PE_Comps.md`; `lab08_wsm_pe_comps.py`. |
| Highest-risk financial claim | The 0%/50%/100% excess-cash cases produce $130.15/$134.51/$138.88 per share. | Shows that the full-cash bridge is a material judgment, not an established fact. | `value_with_excess_cash()` in `wsm_proforma.py`; `output/visible_final_results.json`. |

## Cold Run and Reproducibility

`output/cold-run-log.md` records a clean execution on October 15, 2026 in a fresh temporary directory using system Python 3.9.6 and only `wsm_proforma.py`, `validate_wsm_model.py`, and `lab08_wsm_pe_comps.py`. The first run failed at 09:37:04 EDT because Python 3.9 rejected a backslash inside an f-string expression. The code was corrected by assigning the header text to a standard string before formatting. The rerun passed at 09:37:21 EDT, an elapsed interval of 17 seconds from the recorded initial failure, and reproduced the $138.88 integrated base FCFF value per share.

This record retains the first failure because it identifies a genuine portability issue and its resolution. The log is a narrative record rather than a preserved raw terminal transcript.

## Directional Changed-Input Test and Locked Record

The historical `Lab11_WSM_Sensitivity.md` records a gross-margin test that lowered the FY2026E-FY2030E gross-margin assumption from **45.5% to 44.0%**, a **1.5-percentage-point decrease in each forecast year**. It identifies September 29, 2026, 13:45 EDT as the lock time and states that the case was locked before the exact changed case ran.

| Item | Documented historical record |
| --- | --- |
| Inputs held constant | Revenue growth, cash SG&A ratio, depreciation rate, capex, tax rate, inventory days, other working capital, dividends, repurchases, cost of equity, terminal growth, and shares. |
| Expected direction and magnitude | FY2030 operating income down about $65M; FY2030 FCFE down about $50M; value per share down about $5-$7. |
| Actual result | FY2030 operating income fell from $1,713.1M to $1,648.3M (-$64.7M); FCFE fell from $1,220.5M to $1,170.6M (-$49.9M); historical FCFE-only value fell from $130.15 to $124.44 per share (-$5.70). |
| Prediction reconciliation | The actual operating-income and FCFE changes were $0.3M and $0.1M smaller than the rough prediction; the $5.70 per-share decline fell within the predicted range. |
| Decision implication | `Lab10_WSM_ProForma.md` records no change to the directional conclusion: $124.44 remained below the September 24, 2026 reference price of $228.62. The test increased the priority of researching tariff costs, merchandise costs, and pricing power. |

### Evidence Limitation

The repository does **not** contain a pre-run commit, immutable snapshot, or other contemporaneous artifact that verifies the prediction was authored by the student with AI off before execution. The historical operating deltas remain reproducible, but this record cannot establish the required precommit or AI-off condition. This gap must not be backdated or reconstructed.

## AI Assistance: Evidence, Disposition, and Disclosure

The repository identifies both ChatGPT and Codex as tools used during the project. `Lab06_WSM.md`, a report dated September 3, 2026, states that ChatGPT and Codex assisted with drafting and that the student gathered and verified sources and retained the investment judgments. The record does not preserve a separate interaction date, exposed model/version, or prompt/output transcript for either tool. `Lab07_Asbury_PE_Comps.md` separately states that Codex created the standard-library calculator and drafted that lab's Markdown from user-supplied inputs and course materials; it did not replace the supplied market-price or EPS inputs.

**Specific AI-assisted output — qualified.** The Codex-created `lab07_pe_comps.py` is a preserved, identifiable output. On October 16, 2026, it was rerun and reproduced its displayed $231.00 median P/E-implied price. The script's arithmetic is accepted only as a reproducible historical lab calculation. It is qualified because the Lab 07 record itself identifies provisional input-source limitations, and it was not used in the final WSM valuation or the Watch/Defer recommendation. This disposition is supported by the rerun, `Lab07_Asbury_PE_Comps.md`, and the fact that the final WSM model uses `wsm_proforma.py` and `lab08_wsm_pe_comps.py` instead.

For the final WSM work, Codex assistance is documented for code review, model integration, documentation, and deck preparation during October 14-15, 2026. The final WSM numerical outputs were independently checked on October 16, 2026 by rerunning the synthetic known-answer, base-year, articulation, bridge, monotonicity, and peer-calculation tests. AI-assisted drafting, coding, validation support, and documentation did not substitute for filing-linked evidence, source selection, normalization, WACC and cash-treatment judgments, or the student's Watch/Defer conclusion.

The exposed Codex and ChatGPT model/version information, complete interaction dates, and the complete list of any other material AI tools cannot be recovered from the repository. No preserved ChatGPT or Codex prompt/output maps a discrete final WSM calculation or recommendation directly to either tool. These limits are disclosed rather than filled with reconstructed evidence.

## Limitations and Monitoring Triggers

The valuation supports **Watch/Defer; do not initiate at $228.25** on the dated evidence. The most important limitations are tariff-refund normalization, the 10.0% WACC judgment, seasonal-cash treatment, the two-peer comparable set, and terminal value representing 72.7% of enterprise value.

Reassess if post-refund comparable-brand demand and normalized margin support a stronger operating case, if a refreshed same-date valuation provides a margin of safety, or if minimum-operating-cash analysis materially changes the equity bridge. Move from Watch/Defer to Do Not Initiate if sustained tariff or sourcing pressure weakens normalized margins in a manner consistent with the downside case.

## Outstanding Verification Items

1. **Highest priority — Locked Changed-Input Record:** Attach genuine contemporaneous pre-run evidence, if it exists, showing the human-authored AI-off prediction and immutable timestamp or commit. If it does not exist, retain the disclosure above and obtain instructor direction; do not create replacement evidence.
2. **High priority — Named AI-use disclosure:** From the student's records, verify the exposed Codex and ChatGPT model/version, interaction date or dates, and whether any other material AI tool was used. Add only facts the student can personally confirm.
3. **Submission control:** Confirm that the tool roles and limitations stated above accurately reflect the student's work before freezing the PDF. The cold-run log is a narrative record, not a raw terminal transcript.
