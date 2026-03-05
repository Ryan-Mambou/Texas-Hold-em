"""
TDD tests for Texas Hold'em hand evaluator.
Incremental development: small steps, one category at a time.
"""
import unittest
from poker import parse_card, Card

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

if __name__ == "__main__":
    unittest.main()