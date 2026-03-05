"""
Texas Hold'em hand evaluator.
Given 5 community cards and 2 hole cards per player,
determines best 5-card hand, compares players, and returns winner(s).
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple


@dataclass(frozen=True)
class Card:
    """A playing card. rank: 2-14 (Ace=14). suit: S, H, D, C."""
    rank: int
    suit: str

    def __str__(self) -> str:
        rank_str = {11: "J", 12: "Q", 13: "K", 14: "A"}.get(self.rank, str(self.rank))
        return f"{rank_str}{self.suit}"

class HandCategory(IntEnum):
    """Texas Hold'em poker hand categories, highest to lowest."""
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def parse_card(s: str) -> Card:
    """Parse card from string like 'AS', '10H', '2D'."""
    suit = s[-1].upper()
    rank_str = s[:-1].upper()
    rank_map = {"J": 11, "Q": 12, "K": 13, "A": 14}
    rank = rank_map[rank_str] if rank_str in rank_map else int(rank_str)
    return Card(rank=rank, suit=suit)


def parse_cards(*strings: str) -> List[Card]:
    """Parse multiple cards from strings."""
    return [parse_card(s) for s in strings]

def evaluate_hand(cards: List[Card]) -> Tuple[HandCategory, List[Card], tuple]:
    """
    Evaluate best 5-card hand from given cards (must be 5-7 cards).
    Returns: (category, chosen5, tiebreak_values) where tiebreak_values
    is a tuple for lexicographic comparison.
    """
    if len(cards) == 5:
        return _evaluate_five(cards)
    if len(cards) == 7:
        return _best_of_seven(cards)
    raise ValueError(f"Need 5 or 7 cards, got {len(cards)}")

def _evaluate_five(cards: List[Card]) -> Tuple[HandCategory, List[Card], tuple]:
    """Evaluate exactly 5 cards. Returns best category with chosen5 and tiebreak."""
    return _high_card(cards)

def _high_card(cards: List[Card]) -> Tuple[HandCategory, List[Card], tuple]:
    sorted_cards = sorted(cards, key=lambda c: c.rank, reverse=True)
    tiebreak = tuple(c.rank for c in sorted_cards)
    return HandCategory.HIGH_CARD, sorted_cards, tiebreak

def _best_of_seven(cards: List[Card]) -> Tuple[HandCategory, List[Card], tuple]:
    """Find best 5-card hand from 7 cards."""
    from itertools import combinations
    best_category = HandCategory.HIGH_CARD
    best_chosen = None
    best_tiebreak = ()
    for five in combinations(cards, 5):
        cat, chosen, tb = _evaluate_five(list(five))
        if cat > best_category or (cat == best_category and tb > best_tiebreak):
            best_category, best_chosen, best_tiebreak = cat, chosen, tb
    return best_category, best_chosen, best_tiebreak