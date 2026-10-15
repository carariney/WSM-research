# Lab 13 — Portfolio Mandate Defense

## Files and commands

- Checker: `mandate.py`
- Run the candidates: `python3 mandate.py`
- Run the required long-only probe: `python3 mandate.py --probe-long-only`

## S1–S10 sorting

| Statement | Type: objective, hard constraint, preference, unverifiable promise, or missing | One-line reason |
| --- | --- | --- |
| S1 | Hard constraint | Seven-year investment horizon and annual rebalancing. |
| S2 | Objective | CPI + 4% annually, net of costs, over rolling five-year periods. |
| S3 | Hard constraint | Maintain a 3% reserve for twelve months of distributions. |
| S4 | Preference / reference benchmark | 60% global equities and 40% U.S. investment-grade bonds; these are benchmark weights, not mandatory allocation weights. |
| S5 | Hard constraint | Long-only, with no borrowing, short sales, or derivatives. |
| S6 | Hard constraint | Maximum 8% combined exposure to any nonexempt issuer. |
| S7 | Hard constraint | Annual turnover cannot exceed 25% without committee approval. |
| S8 | Hard constraint | At least 90% of the portfolio must be redeemable within five business days. |
| S9 | Unverifiable promise | The calendar-year loss limit lacks a defined measure and breach procedure. |
| S10 | Missing | The CIO has not defined what the portfolio should optimize. |

The static holdings table permits checks of weights, long-only status, reserve assets, redemption
timing, and issuer concentration. It cannot test the seven-year horizon, rolling CPI-plus-4%
performance net of costs, benchmark-relative performance, turnover without a trade history, or
an undefined calendar-loss rule. `mandate.py` therefore prints “requires CIO clarification” for
S9 instead of inventing a pass/fail test.

## Known-answer validation

`python3 mandate.py` computes the required reserve minimum of **3.0%**.

| Rule | A | B | C |
| --- | --- | --- | --- |
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only, lowest weight | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve at least 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable within five business days at least 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company at most 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

The issuer calculation combines Acme Corp bonds and Acme Corp stock. Cash, the U.S. Treasury,
and diversified funds are exempt from the issuer limit.

## Required probe

Command run: `python3 mandate.py --probe-long-only`

Expected and observed result: the A probe has a lowest weight of **-2.0** and fails only the
long-only rule. Its reserve-eligible weight remains **10.0%**, so the reserve rule still passes.
The probe operates on a copy of A, so the original A weights are restored for the normal run.

## AI-partner attack candidate D

**AI-partner proposal:** Candidate D holds 3% cash and 97% of the global equity index fund.
It passes every coded rule: weights sum to 100%, no weight is negative, the reserve is 3%, the
entire portfolio is redeemable inside five business days, and it has no non-exempt single-company
exposure.

Verified D result: D passes every checkable rule. Its reserve-eligible weight is 3.0%, liquid
weight is 100.0%, and largest nonexempt single-company exposure is 0.0%.

**AI-closed student judgment:**

The concern is reasonable because Candidate D invests 97% in equities, which could lead to losses
greater than the foundation is comfortable with even though it passes all the checks. This relates
to S9 because the CIO has not clearly explained how the 10% annual loss limit should be measured
or handled.

**Partner swap role:** As the sceptical colleague, I would cite **S9** against candidate D and
ask the portfolio proposer to define the loss measure, measurement frequency, and action after a
breach. Record your own response to a real partner's D if one is supplied.

## Question for the CIO — AI-closed response

Write one question that blocks optimization, and state the answer that would change your portfolio.

**Question for the CIO:** Should the portfolio prioritize higher returns or tighter risk limits?

If the CIO wants higher returns, I would invest more in equities. If limiting risk is more
important, I would invest more in Treasury securities and investment-grade bonds. This decision
would determine how the portfolio is built.

## Investment policy statement — student AI-off reflection

An Investment Policy Statement, or IPS, is the governing document that translates a client's
purpose, return objective, risk tolerance, liquidity needs, legal restrictions, and decision
authority into rules for managing a portfolio. Objectives describe the outcome the portfolio is
meant to pursue. Constraints restrict how the manager may pursue it, such as liquidity, issuer,
turnover, and long-only limits. A benchmark gives a comparison reference but does not by itself
require the portfolio to hold the benchmark weights.

In Meridian's IPS, S2 is the return objective. S1, S3, S5, S6, S7, and S8 are implementation or
risk constraints. S4 is the reference benchmark. S9 is an incomplete risk statement because it
does not define how loss is measured or what happens after a breach. S10 is a missing mandate
choice because the CIO has not selected an optimization priority. Together, these statements
show why a checker can test some limits while still being unable to decide whether a portfolio is
appropriate.

### Personal AI-closed reflection

1. **Why can a portfolio pass every coded rule yet still be unsuitable for Meridian?**

   A portfolio can pass every check and still not be the right choice because the rules do not
   cover every risk or goal the client has. For example, Candidate D passes all the checks, but
   having 97% invested in equities could lead to losses that the foundation is not willing to
   accept. This shows that meeting the rules does not always mean a portfolio is suitable for the
   client.

2. **Which S1–S10 type were you least sure of, and why?**

   S9 was the hardest for me to classify because the 10% annual loss limit initially seemed like
   a hard constraint. However, the CIO did not explain exactly how losses should be measured or
   what happens if the limit is exceeded. I learned that a rule needs clear definitions before it
   can be properly tested.

## Submission

Push this Markdown file and `mandate.py` to GitHub. Submit the two file links individually in the
Lab 13 quiz after completing the marked AI-off sections yourself.
