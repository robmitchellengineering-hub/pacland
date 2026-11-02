"""The measure space has dimension b3; every tadpole is attained; nothing reduces the dimension."""
import unittest

from pacland.exactness import underdetermination as U


class TestTheClassStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = U.verdict()

    def test_the_counts_reproduce(self):
        rows = {r["b3"]: r for r in self.v["rows"]}
        self.assertEqual(rows[2]["orbits"], 80)
        self.assertEqual(rows[4]["orbits"], 6560)
        self.assertEqual(rows[6]["orbits"], 531440)
        self.assertEqual(rows[6]["distinct_N"], 13)
        self.assertEqual(rows[6]["distinct_absN"], 7)

    def test_every_tadpole_from_minus_b3_to_plus_b3_is_attained(self):
        self.assertTrue(self.v["every_tadpole_attained"])
        for r in self.v["rows"]:
            self.assertEqual(r["distinct_N"], 2 * r["b3"] + 1)

    def test_the_measure_dimension_is_b3(self):
        for r in self.v["rows"]:
            self.assertEqual(r["measure_dimension"], r["b3"])
        self.assertEqual(self.v["measure_dimensions"], {2: 2, 4: 4, 6: 6})


class TestTheStatement(unittest.TestCase):
    def test_it_says_underdetermined_and_cites_albert(self):
        v = U.verdict()
        self.assertIn("underdetermined", v["statement"])
        self.assertIn("01:39:47", v["citation"])

    def test_it_names_a_falsifier(self):
        self.assertIn("reduce the dimension", U.verdict()["falsifier"])

    def test_the_max_tadpole_matches_the_theorem(self):
        # cross-check against the proven bound: |N| <= b3, attained
        for r in U.ladder():
            self.assertEqual(max(abs(x) for x in r["n_values"]), r["b3"])


if __name__ == "__main__":
    unittest.main()
