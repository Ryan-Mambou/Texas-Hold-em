"""
TDD tests for Texas Hold'em hand evaluator.
Incremental development: small steps, one category at a time.
"""
import unittest
from poker import parse_card, Card, HandCategory, evaluate_hand, parse_cards

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

# ============== Two pair ==============
class TestTwoPair(unittest.TestCase):
    def test_two_pair_detection(self):
        cards = [parse_card(c) for c in ["AS", "AH", "KS", "KH", "10D"]]
        category, chosen5, tb = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.TWO_PAIR)
        self.assertEqual(tb[0], 14)  # high pair
        self.assertEqual(tb[1], 13)  # low pair
        self.assertEqual(tb[2], 10)  # kicker


# ============== Straight ==============
class TestStraight(unittest.TestCase):
    def test_straight_ace_high(self):
        """10-J-Q-K-A is Ace-high straight (mixed suits for plain straight)."""
        cards = [parse_card(c) for c in ["10S", "JH", "QD", "KC", "AS"]]
        category, chosen5, tb = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.STRAIGHT)
        self.assertEqual(tb[0], 14)

    def test_straight_ace_low_wheel(self):
        """A-2-3-4-5 is wheel (5-high straight)."""
        cards = [parse_card(c) for c in ["AS", "2H", "3D", "4C", "5S"]]
        category, chosen5, tb = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.STRAIGHT)
        self.assertEqual(tb[0], 5)  # wheel is 5-high

    def test_no_wrap_around_straight(self):
        """Q-K-A-2-3 is NOT a valid straight."""
        cards = [parse_card(c) for c in ["QS", "KH", "AD", "2C", "3S"]]
        category, _, _ = evaluate_hand(cards)
        self.assertNotEqual(category, HandCategory.STRAIGHT)

# ============== Straight flush ==============
class TestStraightFlush(unittest.TestCase):
    def test_straight_flush_detection(self):
        cards = parse_cards("9S", "10S", "JS", "QS", "KS")
        category, chosen5, tb = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.STRAIGHT_FLUSH)
        self.assertEqual(tb[0], 13)

# ============== Best of 7  ==============
class TestBestOfSeven(unittest.TestCase):
    """Tests for selecting best 5 from 7 cards."""

    def test_board_plays(self):
        """When board has straight flush, player can play board (zero hole cards)."""
        board = [parse_card(c) for c in ["9S", "10S", "JS", "QS", "KS"]]  # straight flush
        hole = [parse_card(c) for c in ["2H", "3D"]]  # irrelevant
        cards = board + hole
        category, chosen5, _ = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.STRAIGHT_FLUSH)
        self.assertEqual(set(c.rank for c in chosen5), {13, 12, 11, 10, 9})

    def test_one_hole_card_improves(self):
        """One hole card can improve hand (e.g. pair on board + one pair in hole)."""
        board = [parse_card(c) for c in ["AS", "KH", "10D", "5C", "2S"]]
        hole = [parse_card(c) for c in ["AH", "3D"]]
        cards = board + hole
        category, chosen5, _ = evaluate_hand(cards)
        self.assertEqual(category, HandCategory.ONE_PAIR)
        self.assertIn(14, [c.rank for c in chosen5])

if __name__ == "__main__":
    unittest.main()