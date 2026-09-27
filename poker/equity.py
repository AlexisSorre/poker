"""Calcul de la probabilité de gagner (équité) par simulation Monte-Carlo.

Principe : on complète au hasard le board et les mains adverses des milliers
de fois, et on compte combien de fois notre main gagne. Plus il y a de
simulations, plus le résultat est précis (environ ±0,5 % avec 20 000).
"""

import random
from dataclasses import dataclass

from poker.cards import full_deck
from poker.evaluator import evaluate


@dataclass
class EquityResult:
    win: float      # probabilité de gagner seul
    tie: float      # probabilité de partager le pot
    lose: float     # probabilité de perdre
    equity: float   # part du pot gagnée en moyenne (victoires + parts d'égalités)
    simulations: int


def compute_equity(
    hero: list[tuple[int, str]],
    board: list[tuple[int, str]],
    num_opponents: int = 1,
    simulations: int = 20_000,
    seed: int | None = None,
) -> EquityResult:
    """Équité de `hero` contre `num_opponents` mains adverses inconnues.

    board : 0 carte (preflop), 3 (flop), 4 (turn) ou 5 (river).
    """
    if len(hero) != 2:
        raise ValueError("La main doit contenir exactement 2 cartes.")
    if len(board) not in (0, 3, 4, 5):
        raise ValueError("Le board doit contenir 0, 3, 4 ou 5 cartes.")
    if not 1 <= num_opponents <= 9:
        raise ValueError("Le nombre d'adversaires doit être entre 1 et 9.")
    known = hero + board
    if len(set(known)) != len(known):
        raise ValueError("Une même carte apparaît deux fois.")

    rng = random.Random(seed)
    known_set = set(known)
    deck = [c for c in full_deck() if c not in known_set]

    missing_board = 5 - len(board)
    cards_to_draw = missing_board + 2 * num_opponents

    wins = ties = 0
    pot_share = 0.0

    for _ in range(simulations):
        draw = rng.sample(deck, cards_to_draw)
        full_board = board + draw[:missing_board]
        others = draw[missing_board:]

        hero_score = evaluate(hero + full_board)
        opp_scores = [
            evaluate(others[2 * i : 2 * i + 2] + full_board)
            for i in range(num_opponents)
        ]
        best_opp = max(opp_scores)

        if hero_score > best_opp:
            wins += 1
            pot_share += 1
        elif hero_score == best_opp:
            ties += 1
            nb_winners = 1 + opp_scores.count(hero_score)
            pot_share += 1 / nb_winners

    return EquityResult(
        win=wins / simulations,
        tie=ties / simulations,
        lose=(simulations - wins - ties) / simulations,
        equity=pot_share / simulations,
        simulations=simulations,
    )
