"""
TDD tests for Texas Hold'em hand evaluator.
Incremental development: small steps, one category at a time.
"""
import unittest
from poker import parse_card, Card, HandCategory, evaluate_hand

# ============== Card representation ==============
class TestCardRepresentation(unittest.TestCase):
    """Tests for card parsing and representation."""

    def test_parse_card_valid(self):
        """Parse standard card notation (e.g., 'AS', '10H', '2D')."""
        self.assertEqual(parse_card("AS"), Card(rank=14, suit="S"))
        self.assertEqual(parse_card("KH"), Card(rank=13, suit="H"))
        self.assertEqual(parse_card("10D"), Card(rank=10, suit="D"))
        self.assertEqual(parse_card("2C"), Card(rank=2, suit="C"))

    def test_parse_card_face_cards(self):
        """Parse Jack, Queen, King."""
        self.assertEqual(parse_card("JC").rank, 11)
        self.assertEqual(parse_card("QD").rank, 12)
        self.assertEqual(parse_card("KH").rank, 13)


# ============== High card ==============
class TestHighCard(unittest.TestCase):
    """Tests for high card hand detection."""

    def test_high_card_five_cards(self):
        """Five unrelated cards -> high card, chosen5 in descending order."""
        cards = [parse_card(c) for c in ["AS", "10H", "5D", "3C", "2H"]]
        category, chosen5, _ = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.HIGH_CARD)
        self.assertEqual(len(chosen5), 5)
        self.assertEqual([c.rank for c in chosen5], [14, 10, 5, 3, 2])

    def test_high_card_tiebreak_highest_wins(self):
        """When both have high card, higher ranks win."""
        hand1 = [parse_card(c) for c in ["AS", "KH", "10D", "5C", "2S"]]
        hand2 = [parse_card(c) for c in ["KS", "QH", "10D", "5C", "2S"]]
        _, _, tb1 = evaluate_hand(hand1)
        _, _, tb2 = evaluate_hand(hand2)
        self.assertGreater(tb1, tb2)
# ============== One pair ==============
class TestOnePair(unittest.TestCase):
    """Tests for one pair detection."""

    def test_one_pair_detection(self):
        """Two cards of same rank -> one pair."""
        cards = [parse_card(c) for c in ["AS", "AH", "KD", "10C", "2S"]]
        category, chosen5, _ = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.ONE_PAIR)
        # chosen5: pair first (by rank), then kickers descending
        ranks = [c.rank for c in chosen5]
        self.assertEqual(ranks[:2], [14, 14])
        self.assertEqual(sorted(ranks[2:], reverse=True), [13, 10, 2])

    def test_one_pair_beats_high_card(self):
        """One pair beats high card."""
        pair = [parse_card(c) for c in ["2S", "2H", "AS", "KD", "10C"]]
        high = [parse_card(c) for c in ["AS", "KH", "QD", "JC", "9S"]]
        c1, _, _ = evaluate_hand(pair)
        c2, _, _ = evaluate_hand(high)
        self.assertGreater(c1, c2)

    def test_one_pair_tiebreak_pair_rank_then_kickers(self):
        """Compare pair rank first, then kickers."""
        pair_high = [parse_card(c) for c in ["AS", "AH", "KD", "10C", "2S"]]
        pair_low = [parse_card(c) for c in ["KS", "KH", "AD", "10C", "2S"]]
        _, _, tb1 = evaluate_hand(pair_high)
        _, _, tb2 = evaluate_hand(pair_low)
        self.assertGreater(tb1, tb2)


if __name__ == "__main__":
    unittest.main()