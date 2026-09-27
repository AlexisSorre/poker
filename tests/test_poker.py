"""Tests. Lancer avec :  python -m pytest"""

import pytest

from poker.cards import parse_cards
from poker.equity import compute_equity
from poker.evaluator import evaluate, hand_name


def score(text):
    return evaluate(parse_cards(text))


def test_categories():
    assert hand_name(score("As Ks Qs Js Ts 2d 3c")) == "Quinte flush"
    assert hand_name(score("9h 9d 9s 9c 2d")) == "Carré"
    assert hand_name(score("Kh Kd Ks 7c 7d")) == "Full"
    assert hand_name(score("2h 7h 9h Jh Kh")) == "Couleur"
    assert hand_name(score("5d 6c 7h 8s 9d")) == "Quinte"
    assert hand_name(score("Qh Qd Qs 2c 7d")) == "Brelan"
    assert hand_name(score("Jh Jd 4s 4c Ad")) == "Double paire"
    assert hand_name(score("Th Td 2s 5c 8d")) == "Paire"
    assert hand_name(score("Ah Jd 8s 5c 3d")) == "Hauteur"


def test_wheel_is_lowest_straight():
    assert score("Ah 2d 3s 4c 5d") == (4, 5)
    assert score("2d 3s 4c 5d 6h") > score("Ah 2d 3s 4c 5d")


def test_kicker():
    assert score("Ah Ad Ks 7c 2d") > score("Ah Ad Qs 7c 2d")


def test_two_full_houses_in_seven_cards():
    # deux brelans : on garde le meilleur full (KKK 77)
    assert score("Kh Kd Ks 7c 7d 7h 2s") == (6, 13, 7)


def test_split_pot_on_board():
    # quinte royale sur le board : tout le monde partage
    result = compute_equity(parse_cards("2c 3d"), parse_cards("As Ks Qs Js Ts"), simulations=500)
    assert result.tie == 1.0
    assert result.equity == pytest.approx(0.5)


def test_aces_preflop():
    # AA contre une main aléatoire : environ 85 %
    result = compute_equity(parse_cards("As Ah"), [], simulations=20_000, seed=1)
    assert result.equity == pytest.approx(0.852, abs=0.01)


def test_duplicate_card_raises():
    with pytest.raises(ValueError):
        compute_equity(parse_cards("As Kh"), parse_cards("As Qd Jc"))
