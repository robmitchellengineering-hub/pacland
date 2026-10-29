"""Identifiability: the rank must not exceed the parameter count, and one mic must not suffice."""
import unittest

from pacland.spectral import identify as I


class TestRank(unittest.TestCase):
    def test_rank_cannot_exceed_the_parameter_count(self):
        r = I.identifiability(n_modes=4)
        for row in r["rows"]:
            self.assertLessEqual(row["rank"], row["params"])

    def test_a_single_microphone_does_not_identify_everything(self):
        r = I.identifiability(n_modes=5)
        self.assertLess(r["rows"][0]["rank"], r["n_params"])

    def test_identifiability_saturates_by_two_mics_in_one_dimension(self):
        r = I.identifiability(n_modes=5)
        self.assertEqual(r["rows"][1]["rank"], r["n_params"])

    def test_geometry_known_does_not_raise_the_fraction(self):
        a = I.identifiability(fit_freqs=True)
        b = I.identifiability(fit_freqs=False)
        self.assertAlmostEqual(a["rows"][0]["identifiable_fraction"],
                               b["rows"][0]["identifiable_fraction"], delta=0.10)


class TestAudit(unittest.TestCase):
    def test_all_checks_are_green(self):
        self.assertTrue(I.audit()["all_pass"])
