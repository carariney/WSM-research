"""FIN 439 Lab 08: WSM P/E comparable-company calculation.

Inputs are August 31, 2026 USD closing prices and annual reported GAAP diluted
EPS that was public by that date.  Sources and peer dispositions are in
Lab08_WSM_PE_Comps.md.
"""

from decimal import Decimal, InvalidOperation
from statistics import median


TARGET = {"name": "Williams-Sonoma (WSM)", "diluted_eps": "8.84"}
PEERS = [
    {"name": "RH (RH)", "price": "149.15", "diluted_eps": "6.31"},
    {"name": "Arhaus (ARHS)", "price": "8.71", "diluted_eps": "0.48"},
]


def positive_decimal(value):
    """Return a positive Decimal input, or None when it is missing/invalid."""
    if value is None or isinstance(value, bool) or str(value).strip() == "":
        return None
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    return number if number > 0 else None


def money(value):
    return f"${value:,.2f}"


def multiple(value):
    return f"{value:,.6f}x"


def main():
    target_eps = positive_decimal(TARGET["diluted_eps"])
    print("FIN 439 Lab 08 — WSM P/E Comparable Analysis")
    print(f"Target: {TARGET['name']}")
    print(f"Target reported annual GAAP diluted EPS: {target_eps}")
    print()

    usable = []
    print("Qualified-peer P/E multiples")
    for peer in PEERS:
        price = positive_decimal(peer.get("price"))
        eps = positive_decimal(peer.get("diluted_eps"))
        if price is None or eps is None:
            print(f"{peer.get('name', 'Unnamed peer')}: excluded (missing or nonpositive price/EPS).")
            continue
        pe = price / eps
        usable.append((peer["name"], pe))
        print(f"{peer['name']}: {multiple(pe)}")

    if target_eps is None or not usable:
        print("\nNo implied WSM price: target EPS or peer inputs are unusable.")
        return

    multiples = [pe for _, pe in usable]
    low, middle, high = min(multiples), median(multiples), max(multiples)
    print("\nImplied WSM price using $8.84 reported annual GAAP diluted EPS")
    print(f"Minimum peer P/E: {multiple(low)} -> {money(low * target_eps)}")
    print(f"Median peer P/E:  {multiple(middle)} -> {money(middle * target_eps)}")
    print(f"Maximum peer P/E: {multiple(high)} -> {money(high * target_eps)}")

    print("\nPeer-removal sensitivity")
    for removed_name, _ in usable:
        remaining = [pe for name, pe in usable if name != removed_name]
        if not remaining:
            print(f"Remove {removed_name}: no estimate (no peer remains).")
            continue
        reference = median(remaining) * target_eps
        print(f"Remove {removed_name}: {money(reference)} reference estimate")


if __name__ == "__main__":
    main()
