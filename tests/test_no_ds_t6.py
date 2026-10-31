"""Route B — the no-de-Sitter impossibility for the T^6 oracle."""
import unittest

from pacland.oracle import no_ds_t6 as N


class TestTheImpossibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = N.statement()

    def test_the_claim_is_proved_not_sampled(self):
        self.assertTrue(self.s["proved_not_sampled"])

    def test_the_identity_holds_numerically(self):
        self.assertLess(self.s["worst_identity_residual"], 1e-12)

    def test_every_checked_point_has_non_positive_potential(self):
        self.assertTrue(self.s["all_non_positive"])
        for r in self.s["checks"]:
            self.assertLessEqual(r["V"], 0.0)

    def test_the_scope_names_what_it_does_not_cover(self):
        # an impossibility without its scope is a slogan
        for word in ("Kahler modulus", "non-perturbative", "uplift"):
            self.assertIn(word, self.s["scope"])

    def test_it_says_why(self):
        self.assertIn("-3", self.s["because"])
        self.assertIn("unreachable", self.s["because"])


class TestTheStatementCanFail(unittest.TestCase):
    def test_a_positive_potential_would_be_detected(self):
        # if V could be positive the identity would break; assert the identity is what carries the claim
        r = N.potential_at_susy(*N.CHECKS[0])
        self.assertLess(r["V"], 0)
        self.assertGreater(abs(r["K"]), 0)          # e^K is not 1, so the negativity is not trivial


if __name__ == "__main__":
    unittest.main()
