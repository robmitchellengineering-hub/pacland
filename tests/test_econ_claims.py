"""The finance claims dossier: the rule is stated, monotone, and every claim computes its own m."""
import math
import unittest

from pacland.economics import claims as C


class TestRadius(unittest.TestCase):
    def test_radius_is_the_hoeffding_bound(self):
        self.assertAlmostEqual(C.radius(8), math.sqrt(math.log(20) / 16), places=12)

    def test_no_constraints_is_vacuous(self):
        self.assertEqual(C.radius(0), math.inf)

    def test_radius_shrinks(self):
        rs = [C.radius(m) for m in (1, 4, 16, 64)]
        self.assertTrue(all(a > b for a, b in zip(rs, rs[1:])))


class TestWorth(unittest.TestCase):
    def test_extrapolation_is_never_act(self):
        c = C.Claim("t", "null", 100, False, "r", "e")
        self.assertEqual(c.worth, C.DO_NOT)

    def test_many_constraints_inside_the_region_act(self):
        self.assertEqual(C.Claim("t", "null", 40, True, "r", "e").worth, C.ACT)

    def test_few_constraints_hedge(self):
        self.assertEqual(C.Claim("t", "null", 8, True, "r", "e").worth, C.HEDGE)

    def test_a_definitional_claim_is_exact(self):
        c = C.Claim("t", "definitional", 0, True, "r", "e")
        self.assertEqual(c.worth, C.ACT)
        self.assertEqual(c.radius_label, "exact")


class TestClaims(unittest.TestCase):
    def test_the_dossier_covers_the_sector(self):
        s = C.summary()
        self.assertGreaterEqual(s["n"], 6)
        self.assertGreaterEqual(s["n_extrapolation"], 2)

    def test_sw_out_of_sample_is_refused(self):
        sw = next(c for c in C.claims() if "Smets" in c.text)
        self.assertTrue(sw.extrapolation)
        self.assertEqual(sw.worth, C.DO_NOT)

    def test_the_audit_is_green(self):
        self.assertTrue(C.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
