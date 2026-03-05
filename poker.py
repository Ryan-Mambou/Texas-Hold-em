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