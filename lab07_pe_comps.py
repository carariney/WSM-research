"""FIN 439 Lab 07: P/E comparable-company implied-price analysis.

Edit only TARGET and PEERS below.  Values may be strings, ints, floats, or
None; strings are preferred so the entered decimal precision is preserved.
"""

from decimal import Decimal, InvalidOperation
from statistics import median


# ---------------------------- EDITABLE INPUTS ---------------------------- #
# December 31, 2024 closing prices and FY2024 total GAAP diluted EPS.
TARGET = {
    "name": "Asbury Automotive (ABG)",
    "diluted_eps": "21.50",
}

# A peer's price and diluted EPS must use matching per-share conventions.
# Peer names are used to deduplicate the list (case-insensitively).
PEERS = [
    {"name": "AutoNation (AN)", "price": "169.84", "diluted_eps": "16.92"},
    {"name": "Group 1 Automotive (GPI)", "price": "421.48", "diluted_eps": "36.81"},
]
# ------------------------------------------------------------------------- #


def as_decimal(value):
    """Return a Decimal, or None for a missing/non-numeric input."""
    if value is None or isinstance(value, bool) or str(value).strip() == "":
        return None
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None


def valid_positive(value):
    value = as_decimal(value)
    return value if value is not None and value > 0 else None


def money(value):
    """Format only for display; all calculations retain the original Decimal."""
    return f"${value:,.2f}"


def signed_money(value):
    """Format a signed dollar change for display only."""
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def multiple(value):
    return f"{value:,.6f}x"


def clean_peers(target_name, peers):
    """Deduplicate by name and exclude a peer whose name is the target's name."""
    target_key = str(target_name).strip().casefold()
    seen = set()
    cleaned = []
    notes = []

    for peer in peers:
        name = str(peer.get("name", "")).strip() or "Unnamed peer"
        key = name.casefold()
        if key == target_key:
            notes.append(f"{name}: excluded (target).")
        elif key in seen:
            notes.append(f"{name}: excluded (duplicate peer).")
        else:
            seen.add(key)
            cleaned.append((name, peer))
    return cleaned, notes


def peer_multiple(name, peer):
    price = valid_positive(peer.get("price"))
    eps = valid_positive(peer.get("diluted_eps"))
    if price is None or eps is None:
        return None, f"{name}: P/E not meaningful (missing or nonpositive price or diluted EPS)."
    return price / eps, None


def implied_price(pe, target_eps):
    return pe * target_eps


def main():
    target_name = TARGET.get("name", "Target")
    target_eps = valid_positive(TARGET.get("diluted_eps"))
    peers, notes = clean_peers(target_name, PEERS)

    print("FIN 439 Lab 07 — P/E Comparable Analysis")
    print(f"Target: {target_name}")
    if target_eps is None:
        print("Target diluted EPS: not meaningful (missing or nonpositive).")
    else:
        print(f"Target diluted EPS: {target_eps}")
    print()

    for note in notes:
        print(note)
    if notes:
        print()

    usable = []
    print("Peer P/E multiples")
    for name, peer in peers:
        pe, note = peer_multiple(name, peer)
        if note:
            print(note)
        else:
            usable.append((name, pe))
            print(f"{name}: {multiple(pe)}")
    print()

    if not usable:
        print("Peer summary: no usable peers; no implied-price estimate.")
        return

    multiples = [pe for _, pe in usable]
    low_pe, median_pe, high_pe = min(multiples), median(multiples), max(multiples)
    print(f"Minimum peer P/E: {multiple(low_pe)}")
    print(f"Median peer P/E:  {multiple(median_pe)}")
    print(f"Maximum peer P/E: {multiple(high_pe)}")

    if target_eps is None:
        print("Implied prices: not meaningful (target diluted EPS is missing or nonpositive).")
        print()
        print("Peer-removal sensitivity (median-implied price vs. full-peer estimate)")
        for removed_name, _ in usable:
            print(
                f"Remove {removed_name}: not meaningful "
                "(target diluted EPS is missing or nonpositive)."
            )
        return

    low_price = implied_price(low_pe, target_eps)
    median_price = implied_price(median_pe, target_eps)
    high_price = implied_price(high_pe, target_eps)
    print(f"Implied price at minimum P/E: {money(low_price)}")
    print(f"Implied price at median P/E:  {money(median_price)}")
    print(f"Implied price at maximum P/E: {money(high_price)}")
    if len(usable) == 1:
        print("One valid peer: the median implied price is a reference estimate, not a range.")
    print()

    print("Peer-removal sensitivity (median-implied price vs. full-peer estimate)")
    for removed_name, _ in usable:
        remaining = [pe for name, pe in usable if name != removed_name]
        if not remaining:
            print(f"Remove {removed_name}: no estimate (no usable peers remain).")
            continue
        remaining_price = implied_price(median(remaining), target_eps)
        change = remaining_price - median_price
        print(
            f"Remove {removed_name}: {money(remaining_price)} "
            f"(change: {signed_money(change)})"
        )


if __name__ == "__main__":
    main()
