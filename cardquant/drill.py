"""Minimal mental-math drill harness for the CardValuation engine.

Run with:  python -m cardquant.drill

Each round draws a random card-valuation scenario, asks you to estimate the
CALL option's Theo and Delta in your head, then reveals the engine's exact
values and your error. Leave an estimate blank to just "reveal". Stop with
Ctrl-C or end-of-input.
"""
import random

from cardquant import CardValuation

STANDARD_DECK = list(range(1, 14)) * 4
MEAN_RANK = 7  # mean rank of a standard 1-13 deck, used only to pick a sensible strike


def _ask_number(prompt: str) -> float | None:
    """Read a float from stdin; blank or unparseable input returns None (skip)."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        print("  (not a number -- skipping this estimate)")
        return None


def _random_scenario() -> CardValuation:
    """Build a random, valid CardValuation on a standard deck (no replacement)."""
    n = random.randint(8, 12)
    num_seen = random.randint(0, n - 3)
    seen = random.sample(STANDARD_DECK, num_seen)
    rough_future = sum(seen) + MEAN_RANK * (n - num_seen)
    strike = rough_future + random.randint(-12, 12)
    return CardValuation(
        n=n,
        seen_cards=seen,
        strike_list=[strike],
        deck=list(STANDARD_DECK),
        with_replacement=False,
        calculate_all_greeks=False,
    )


def _round() -> None:
    cv = _random_scenario()
    strike = cv.strike_list[0]
    seen = sorted(cv.seen_cards)

    print("\n" + "=" * 52)
    print("Deck:      standard (ranks 1-13, 4 of each)")
    print(f"Cards (n): {cv.n} total | {len(seen)} seen | {cv.n - len(seen)} still to draw")
    print(f"Seen:      {seen if seen else '(none)'}")
    print(f"Strike:    {strike}   -- estimate the CALL option")
    print("-" * 52)

    theo_guess = _ask_number("Your Theo estimate  (blank to skip): ")
    delta_guess = _ask_number("Your Delta estimate (blank to skip): ")

    call = cv.options[strike].call
    print("-" * 52)
    print(f"Expected final sum (future): {cv.future:.2f}")

    theo_line = f"Theo:   {call.theo:.4f}"
    if theo_guess is not None:
        theo_line += f"   (your error: {abs(call.theo - theo_guess):.4f})"
    print(theo_line)

    delta_line = f"Delta:  {call.delta:.4f}"
    if delta_guess is not None:
        delta_line += f"   (your error: {abs(call.delta - delta_guess):.4f})"
    print(delta_line)


def main() -> None:
    print("CardValuation drill -- Ctrl-C to stop.")
    try:
        while True:
            _round()
            input("\nPress Enter for the next round...")
    except (KeyboardInterrupt, EOFError):
        print("\nDone. Good drilling.")


if __name__ == "__main__":
    main()
