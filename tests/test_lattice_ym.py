"""The lattice-YM Monte-Carlo: sanity checks only (the full run is the hypothesis falsifier)."""
import unittest

import numpy as np

from pacland.lattice_ym import plaquette_cos, action, plaquette_corr


class TestLatticeYM(unittest.TestCase):
    def test_plaquette_cos_shape(self):
        d, N = 4, 4
        links = np.zeros((d,) + (N,) * d)
        pc = plaquette_cos(links)
        self.assertEqual(pc.shape, (d * (d - 1) // 2,) + (N,) * d)

    def test_trivial_config_action_zero(self):
        # all links = 0 -> all plaquette angles 0 -> cos = 1 -> action 0
        d, N = 4, 4
        links = np.zeros((d,) + (N,) * d)
        self.assertAlmostEqual(action(links, beta=1.0), 0.0, places=10)

    def test_random_config_has_finite_positive_action(self):
        # a random (hot) configuration has positive action; the variance C(0)>0 is well-defined
        d, N = 4, 6
        rng = np.random.default_rng(0)
        links = rng.uniform(0, 2 * np.pi, size=(d,) + (N,) * d)
        self.assertGreater(action(links, beta=1.0), 0.0)
        self.assertGreater(plaquette_corr(links, max_r=1)[0], 0.0)


if __name__ == "__main__":
    unittest.main()
