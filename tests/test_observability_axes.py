"""H-B: invariance and exactness are different axes, and the disagreements are the result."""
import unittest

from pacland.exactness import observability_axes as A


class TestTheTwoAxes(unittest.TestCase):
    def test_the_crosstab_is_populated(self):
        t = A.crosstab()
        self.assertGreaterEqual(len(t[(True, True)]), 4)
        self.assertGreaterEqual(len(t[(False, False)]), 3)

    def test_the_hypothesis_is_refuted_as_stated(self):
        v = A.verdict()
        self.assertFalse(v["coincide"])
        self.assertIn("REFUTED", v["verdict"])

    def test_the_invariant_but_inexact_cell_is_not_empty(self):
        # the zeta zeros: sampler-free, deterministic, and still a float
        v = A.verdict()
        self.assertTrue(any("zeta" in n for n in v["invariant_not_exact"]))

    def test_the_exact_but_dependent_cell_is_not_empty(self):
        # the 5.05x spread: computed exactly over measures and still not truth-apt
        v = A.verdict()
        self.assertTrue(any("measure-dependence" in n for n in v["exact_not_invariant"]))


class TestTheWeakerClaim(unittest.TestCase):
    def test_every_invariant_row_is_sampler_free(self):
        for name, inv, ex, why in A.ROWS:
            if inv:
                self.assertNotIn("sampler", why.lower().replace("sampler-free", ""), name)

    def test_the_surviving_claim_is_stated(self):
        self.assertIn("invariance implies no sampler", A.verdict()["surviving_weaker_claim"])


if __name__ == "__main__":
    unittest.main()
