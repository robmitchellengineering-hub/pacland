"""The tadpole distribution is a closed form: a fixed polynomial to the power b3/2."""
import unittest

from pacland.exactness import tadpole_distribution as T


class TestTheBlock(unittest.TestCase):
    def test_the_block_distribution(self):
        self.assertEqual(T.BLOCK, {-2: 4, -1: 20, 0: 33, 1: 20, 2: 4})
        self.assertEqual(sum(T.BLOCK.values()), 81)      # 3^4 component combinations


class TestAgainstEnumeration(unittest.TestCase):
    def test_all_three_rungs_match_exactly(self):
        v = T.verdict()
        self.assertTrue(v["all_match"])
        for r in v["rows"]:
            self.assertTrue(r["matches"], r)

    def test_the_totals_are_right(self):
        for b3 in (2, 4, 6):
            self.assertEqual(sum(T.counts(b3).values()), T.total(b3))
        self.assertEqual(T.total(2), 80)
        self.assertEqual(T.total(4), 6560)
        self.assertEqual(T.total(6), 531440)

    def test_the_recorded_class_counts(self):
        self.assertEqual(T.counts(2), {-2: 4, -1: 20, 0: 32, 1: 20, 2: 4})
        c6 = T.counts(6)
        self.assertEqual(c6[0], 127904)
        self.assertEqual(c6[-6], 64)


class TestItScales(unittest.TestCase):
    def test_it_is_available_at_large_b3_without_enumeration(self):
        # the point of a closed form: no search, no budget
        c = T.counts(20)
        self.assertEqual(sum(c.values()), T.total(20))
        self.assertGreater(sum(c.values()), 10 ** 18)

    def test_the_statement_names_the_polynomial(self):
        self.assertIn("4x^2 + 20x + 33", T.closed_form(6))
        self.assertIn("P(x)", T.verdict()["statement"])


if __name__ == "__main__":
    unittest.main()
