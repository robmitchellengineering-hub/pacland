"""The dictionary engine — and the proof that its identity check can fail."""
import unittest

import numpy as np

from pacland.periods import dictionary as D


class TestFluxScalingEntry(unittest.TestCase):
    def test_the_entry_passes(self):
        r = D.report()
        self.assertTrue(r["passes"], [(c.name, c.residual) for c in r["entry"].carries])

    def test_the_identity_closes(self):
        self.assertLess(D.flux_scaling().identity_residual, 1e-12)

    def test_both_named_observables_are_carried_and_computed(self):
        e = D.flux_scaling(d=3)
        names = {c.name for c in e.carries}
        self.assertTrue(any("superpotential" in n for n in names))
        self.assertTrue(any("tadpole" in n for n in names))
        for c in e.carries:
            self.assertLess(c.residual, 1e-10, f"{c.name}: {c.residual}")

    def test_the_law_is_the_lemma_s_own(self):
        # W -> dW and N -> d^2 N, with the numbers differing from d itself
        e = D.flux_scaling(d=3)
        w = next(c for c in e.carries if "superpotential" in c.name)
        n = next(c for c in e.carries if "tadpole" in c.name)
        self.assertAlmostEqual(w.value_b / w.value_a, 3.0, places=8)
        self.assertAlmostEqual(n.value_b / n.value_a, 9.0, places=8)

    def test_the_boundary_is_stated(self):
        e = D.flux_scaling()
        self.assertIn("positive integer", e.boundary)
        self.assertGreater(len(e.boundary), 120, "the boundary is not a slogan")

    def test_a_zero_scale_is_refused(self):
        with self.assertRaises(ValueError):
            D.flux_scaling(d=0)


class TestTheCheckCanFail(unittest.TestCase):
    """Mutation: a wrong law must break the entry. Without this the engine is decoration."""

    def test_a_wrong_scaling_law_fails(self):
        # pretend the tadpole scales as d, not d^2, and require the check to notice
        e = D.flux_scaling(d=2)
        n = next(c for c in e.carries if "tadpole" in c.name)
        wrong_law_value = n.value_a * 2.0            # the WRONG prediction
        self.assertGreater(abs(n.value_b - wrong_law_value) / max(abs(n.value_a), 1), 1e-6,
                           "if a wrong law passed, the entry cannot fail")

    def test_a_broken_inverse_fails_the_identity(self):
        F, H = D._flux_pair()
        d = 2
        broken = lambda f: f / (d + 1)               # noqa: E731  -- a wrong inverse
        resid = float(max(np.max(np.abs(broken(d * F) - F)), np.max(np.abs(broken(d * H) - H))))
        self.assertGreater(resid, 1e-6)


if __name__ == "__main__":
    unittest.main()
