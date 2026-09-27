"""Affiche la probabilité de gagner à chaque étape : preflop, flop, turn, river.

Lancer avec :  python main.py
Modifie les variables ci-dessous pour tester d'autres situations.
"""

from poker.cards import parse_cards
from poker.equity import compute_equity
from poker.evaluator import evaluate, hand_name

HERO = "As Kh"               # ta main
BOARD = "Qs Js 2d Th 3c"     # flop (3 cartes) + turn + river
NUM_OPPONENTS = 1
SIMULATIONS = 20_000

STREETS = [("Preflop", 0), ("Flop", 3), ("Turn", 4), ("River", 5)]


def main() -> None:
    hero = parse_cards(HERO)
    full_board = parse_cards(BOARD)

    print(f"Main : {HERO}   |   Adversaires : {NUM_OPPONENTS}\n")
    print(f"{'Street':<8} {'Board':<16} {'Victoire':>9} {'Égalité':>9} {'Équité':>9}   Main actuelle")
    print("-" * 75)

    board_text = BOARD.split()
    for name, n in STREETS:
        board = full_board[:n]
        result = compute_equity(hero, board, NUM_OPPONENTS, SIMULATIONS)
        current = hand_name(evaluate(hero + board)) if n else "-"
        print(
            f"{name:<8} {' '.join(board_text[:n]) or '-':<16} "
            f"{result.win:>9.1%} {result.tie:>9.1%} {result.equity:>9.1%}   {current}"
        )


if __name__ == "__main__":
    main()
