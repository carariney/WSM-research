"""Point-in-time signal example using publication dates and revisions.

Run: python3 asof.py
"""

from datetime import date


# Editable inputs
DECISION_DATE = date.fromisoformat("2026-03-31")
ROWS = (
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published_on": "2026-03-10", "index": 111.0},
)


def publication_date(row):
    """Return a row's publication date as a date object."""
    return date.fromisoformat(row["published_on"])


def report_funnel(rule, removed):
    """Print one ordered cleaning-rule result."""
    row_numbers = ", ".join(str(row["row"]) for row in removed) or "none"
    print(f"{rule}: removed {len(removed)} row(s): {row_numbers}")


def quarantine_missing_ticker(rows):
    """Rule 1: separate rows with missing tickers from usable rows."""
    removed = [row for row in rows if not row["ticker"]]
    kept = [row for row in rows if row["ticker"]]
    return kept, removed


def remove_exact_duplicates(rows):
    """Rule 2: retain the first copy of otherwise identical data rows."""
    seen = set()
    kept = []
    removed = []
    for row in rows:
        key = (row["ticker"], row["month"], row["published_on"], row["index"])
        if key in seen:
            removed.append(row)
        else:
            seen.add(key)
            kept.append(row)
    return kept, removed


def remove_late_publications(rows, decision_date):
    """Rule 3: remove information not published by the decision date."""
    removed = [row for row in rows if publication_date(row) > decision_date]
    kept = [row for row in rows if publication_date(row) <= decision_date]
    return kept, removed


def keep_latest_revision(rows):
    """Rule 4: keep the latest publication for each ticker-month pair."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or publication_date(row) > publication_date(latest[key]):
            latest[key] = row
    kept = [row for row in rows if latest[(row["ticker"], row["month"])] is row]
    removed = [row for row in rows if latest[(row["ticker"], row["month"])] is not row]
    return kept, removed


def as_of_panel(rows, decision_date):
    """Apply the four rules in the required order and return panel plus funnel."""
    remaining, missing_ticker = quarantine_missing_ticker(list(rows))
    remaining, duplicates = remove_exact_duplicates(remaining)
    remaining, late_publications = remove_late_publications(remaining, decision_date)
    remaining, older_revisions = keep_latest_revision(remaining)
    funnel = (
        ("1. Missing ticker", missing_ticker),
        ("2. Exact duplicate", duplicates),
        ("3. Published after decision date", late_publications),
        ("4. Older revision", older_revisions),
    )
    return sorted(remaining, key=lambda row: (row["ticker"], row["month"])), funnel


def latest_revision_panel(rows):
    """Build the look-ahead-biased panel, ignoring the publication-date cutoff."""
    remaining, _ = quarantine_missing_ticker(list(rows))
    remaining, _ = remove_exact_duplicates(remaining)
    panel, _ = keep_latest_revision(remaining)
    return sorted(panel, key=lambda row: (row["ticker"], row["month"]))


def signals(panel):
    """Return each ticker's latest-month percentage change from its prior month."""
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row["ticker"], []).append(row)

    output = []
    for ticker, ticker_rows in sorted(by_ticker.items()):
        ordered = sorted(ticker_rows, key=lambda row: row["month"])
        if len(ordered) < 2:
            continue
        prior, latest = ordered[-2:]
        change = (latest["index"] / prior["index"] - 1) * 100
        output.append((ticker, latest["month"], change))
    return output


def print_panel(panel):
    """Print the rows available for the calculation."""
    print("Row  Ticker  Month measured  Published on  Index")
    for row in panel:
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  {row['published_on']:<12}  {row['index']:.1f}")


def print_signals(title, panel):
    """Print one signal set from a supplied panel."""
    print(title)
    for ticker, month, change in signals(panel):
        print(f"  {ticker}: {change:+.2f}% to {month}")


def main():
    panel, funnel = as_of_panel(ROWS, DECISION_DATE)
    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print("Row funnel")
    for rule, removed in funnel:
        report_funnel(rule, removed)
    print("\nAs-of panel")
    print_panel(panel)
    print()
    print_signals("As-of signals", panel)
    print()
    print_signals("Naive signals (ignores publication date)", latest_revision_panel(ROWS))


if __name__ == "__main__":
    main()
