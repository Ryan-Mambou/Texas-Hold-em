# Texas Hold'em Hand Evaluator

A hand comparison module for Texas Hold'em poker. Given 5 community cards (the board) and 2 hole cards per player, it determines each player's best 5-card hand, compares all players, and returns the winner(s). No betting logic is included.

---

## What Is Implemented

### Core functionality

- **Card representation**: `Card` dataclass with rank (2–14, Ace=14) and suit (S, H, D, C)
- **Card parsing**: `parse_card()` and `parse_cards()` for strings like `"AS"`, `"10H"`
- **Hand evaluation**: `evaluate_hand()` for 5 or 7 cards, returning best category, chosen5 (the 5 cards forming the hand), and tiebreak values
- **Best-of-7 selection**: Chooses the best 5-card hand from 7 cards (board + hole), including “board plays” when the board alone is best
- **Multi-player evaluation**: `evaluate_players()` compares all players and returns winner(s), with support for split pots

### Hand categories (9 total)

| Category        | Value | Description                          |
|----------------|-------|--------------------------------------|
| Straight flush | 9     | 5 consecutive cards, same suit       |
| Four of a kind | 8     | Four cards of same rank              |
| Full house     | 7     | Three of a kind + pair               |
| Flush          | 6     | 5 cards same suit                    |
| Straight       | 5     | 5 consecutive ranks                  |
| Three of a kind| 4     | Three cards of same rank             |
| Two pair       | 3     | Two pairs of different ranks         |
| One pair       | 2     | Two cards of same rank               |
| High card      | 1     | No other hand                        |

### Special rules

- **Wheel (A-2-3-4-5)**: Valid straight, treated as 5-high
- **No wrap-around**: Q-K-A-2-3 is not a valid straight
- **Suits**: Only used for flush/straight flush; no suit-based tie-breaking

---

## Usage

```python
from poker import parse_cards, evaluate_hand, evaluate_players

# Evaluate a single hand (5 or 7 cards)
cards = parse_cards("AS", "KH", "10D", "5C", "2S")
category, chosen5, tiebreak = evaluate_hand(cards)
# category: HandCategory enum
# chosen5: list of 5 Card objects forming the best hand
# tiebreak: tuple for comparison

# Evaluate multiple players
board = parse_cards("AS", "KH", "10D", "5C", "2S")
player1_hole = parse_cards("AH", "AD")
player2_hole = parse_cards("2H", "3D")
result = evaluate_players(board, [player1_hole, player2_hole])
# result["winners"]: list of winning player indices (e.g. [0] or [0, 1] for split)
# result["player_results"][i]: dict with "category", "chosen5", "hand_category_name"
```

---

## Card notation

- **Suits**: S (spades), H (hearts), D (diamonds), C (clubs)
- **Ranks**: 2–10, J, Q, K, A
- Examples: `AS`, `10H`, `2D`, `JC`

---

## Tie-break rules

When two hands share the same category:

- **Straight / Straight flush**: Compare highest card of the straight (wheel = 5)
- **Four of a kind**: Quad rank, then kicker
- **Full house**: Trips rank, then pair rank
- **Flush**: Five cards in descending rank order
- **Three of a kind**: Triplet rank, then kickers
- **Two pair**: Higher pair, lower pair, kicker
- **One pair**: Pair rank, then kickers
- **High card**: Five cards in descending order

---

## Chosen5

The evaluator returns the exact 5 cards chosen as each player's best hand (`chosen5`). Requirements:

- **Exactly 5 distinct cards**: Must contain 5 cards, no duplicates
- **Subset of available**: Must be a subset of the player's 7 cards (board + hole)
- **Consistent ordering** (for deterministic tests):
  - **Straight / Straight flush**: Highest to lowest in straight order (wheel: 5,4,3,2,A)
  - **Four of a kind**: Quad cards first, then kicker
  - **Two pair**: Higher pair, lower pair, kicker
  - **One pair**: Pair first, then kickers descending
  - **Flush / High card**: Descending ranks

---

## Input validity

The implementation assumes there are **no duplicate cards**. Duplicate cards are not validated; behavior is undefined if duplicates are present.

---

## Project structure

```
Texas-Hold-em/
├── poker.py      # Main module: Card, HandCategory, parse_card, parse_cards,
│                 # evaluate_hand, evaluate_players
├── test_poker.py # Unit tests (26 tests)
├── .gitignore    # __pycache__/
└── README.md     # This file
```

---

## Running tests

```bash
python3 -m unittest test_poker -v
```

Or run the test file directly (if it includes `if __name__ == "__main__": unittest.main()`):

```bash
python3 test_poker.py
```

### Test coverage

- Card parsing
- All 9 hand categories
- Tie-break rules
- Best-of-7 selection (including board plays)
- Ace-low straight (wheel)
- No wrap-around straight
- Single winner and split pot (multi-player)
- Chosen5: exactly 5 cards, subset of 7, ordering (straight, wheel, four of a kind, two pair), evaluate_players includes chosen5
