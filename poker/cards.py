"""Représentation des cartes.

Une carte est un tuple (valeur, couleur) :
- valeur : entier de 2 à 14 (11 = Valet, 12 = Dame, 13 = Roi, 14 = As)
- couleur : 's' (pique), 'h' (cœur), 'd' (carreau), 'c' (trèfle)

Exemple : "As" -> (14, 's'), "Th" -> (10, 'h')
"""

RANKS = "23456789TJQKA"
SUITS = "shdc"
RANK_VALUES = {r: v for v, r in enumerate(RANKS, start=2)}
VALUE_TO_RANK = {v: r for r, v in RANK_VALUES.items()}


def parse_card(text: str) -> tuple[int, str]:
    """Convertit un texte comme "As" ou "10h" en carte."""
    text = text.strip()
    if text.startswith("10"):
        text = "T" + text[2:]
    if len(text) != 2:
        raise ValueError(f"Carte invalide : {text!r}")
    rank, suit = text[0].upper(), text[1].lower()
    if rank not in RANK_VALUES or suit not in SUITS:
        raise ValueError(f"Carte invalide : {text!r}")
    return (RANK_VALUES[rank], suit)


def parse_cards(text: str) -> list[tuple[int, str]]:
    """Convertit "As Kh" en liste de cartes. Une chaîne vide donne []."""
    return [parse_card(t) for t in text.split()]


def card_to_str(card: tuple[int, str]) -> str:
    value, suit = card
    return VALUE_TO_RANK[value] + suit


def full_deck() -> list[tuple[int, str]]:
    """Renvoie les 52 cartes du paquet."""
    return [(v, s) for v in range(2, 15) for s in SUITS]
