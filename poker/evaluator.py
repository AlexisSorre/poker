"""Évaluation d'une main de poker (5 à 7 cartes).

evaluate() renvoie un tuple "score". Plus le tuple est grand, meilleure est la main.
Python compare les tuples élément par élément, donc on peut écrire directement
    evaluate(main_a) > evaluate(main_b)

Le premier élément est la catégorie de la main (0 = hauteur ... 8 = quinte flush),
les suivants servent à départager deux mains de même catégorie (kickers).
"""

from collections import Counter

HAND_NAMES = [
    "Hauteur",       # 0
    "Paire",         # 1
    "Double paire",  # 2
    "Brelan",        # 3
    "Quinte",        # 4
    "Couleur",       # 5
    "Full",          # 6
    "Carré",         # 7
    "Quinte flush",  # 8
]


def _best_straight(values: set[int]) -> int | None:
    """Renvoie la carte la plus haute de la meilleure quinte, ou None."""
    values = set(values)
    if 14 in values:
        values.add(1)  # l'As peut aussi valoir 1 : quinte A-2-3-4-5
    for high in range(14, 4, -1):
        if all(high - k in values for k in range(5)):
            return high
    return None


def evaluate(cards: list[tuple[int, str]]) -> tuple:
    """Renvoie le score de la meilleure main de 5 cartes."""
    values = [v for v, _ in cards]

    # --- Couleur et quinte flush ---
    suit_counts = Counter(s for _, s in cards)
    flush_suit = next((s for s, n in suit_counts.items() if n >= 5), None)
    if flush_suit:
        flush_values = sorted((v for v, s in cards if s == flush_suit), reverse=True)
        straight_flush = _best_straight(set(flush_values))
        if straight_flush:
            return (8, straight_flush)

    # Groupes de valeurs, triés par (nombre d'exemplaires, valeur) décroissants
    # ex : K K K 7 7 2 -> [(13, 3), (7, 2), (2, 1)]
    groups = sorted(Counter(values).items(), key=lambda g: (g[1], g[0]), reverse=True)

    # --- Carré ---
    if groups[0][1] == 4:
        quad = groups[0][0]
        kicker = max(v for v in values if v != quad)
        return (7, quad, kicker)

    # --- Full (brelan + paire, ou deux brelans) ---
    if groups[0][1] == 3 and groups[1][1] >= 2:
        return (6, groups[0][0], groups[1][0])

    # --- Couleur ---
    if flush_suit:
        return (5, *flush_values[:5])

    # --- Quinte ---
    straight = _best_straight(set(values))
    if straight:
        return (4, straight)

    # --- Brelan ---
    if groups[0][1] == 3:
        trips = groups[0][0]
        kickers = sorted((v for v in values if v != trips), reverse=True)[:2]
        return (3, trips, *kickers)

    # --- Double paire ---
    if groups[0][1] == 2 and groups[1][1] == 2:
        high_pair, low_pair = groups[0][0], groups[1][0]
        kicker = max(v for v in values if v not in (high_pair, low_pair))
        return (2, high_pair, low_pair, kicker)

    # --- Paire ---
    if groups[0][1] == 2:
        pair = groups[0][0]
        kickers = sorted((v for v in values if v != pair), reverse=True)[:3]
        return (1, pair, *kickers)

    # --- Hauteur ---
    return (0, *sorted(values, reverse=True)[:5])


def hand_name(score: tuple) -> str:
    return HAND_NAMES[score[0]]
