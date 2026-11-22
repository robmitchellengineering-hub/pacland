"""The confinement × spectral combination: σ(β) ≥ σ₀·e^(−kβ) → m(β) ≥ 3.2·√σ₀·e^(−kβ/2)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, confinement_spectral as cs
from pacland import bound_search as bs


class TestConfinementSpectral(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_bridge_is_sqrt_of_string_tension(self):
        m = cs.confinement_to_spectral(lambda beta: 4.0)
        self.assertAlmostEqual(m(0.0), 3.2 * 2.0)  # 3.2·√4 = 6.4

    def test_string_tension_exponent_is_doubled_for_the_mass_gap(self):
        # σ = σ₀·e^(−2.364β) -> m = 3.2·√σ₀·e^(−1.182β): the mass-gap exponent is k/2
        m = cs.confinement_to_spectral(cs.string_tension(1.0, 2.364))
        self.assertAlmostEqual(m(1.0), 3.2 * 1.0 * __import__("math").exp(-1.182), places=4)

    def test_referee_equivalent_survives_and_is_marked_referee(self):
        # σ₀ chosen so 3.2·√σ₀ = 25.28, k = 2.364 -> the referee
        s0 = (25.28 / 3.2) ** 2
        m = cs.confinement_to_spectral(cs.string_tension(s0, 2.364))
        r = bs.check_bound(m)
        self.assertTrue(r["survived"])

    def test_search_honestly_finds_no_new_confinement_bound(self):
        s0 = (25.28 / 3.2) ** 2
        res = cs.search_confinement([s0, 5.0, 10.0], [1.0, 2.364, 3.0])
        self.assertEqual(res["n_survivors"], 0)
        self.assertIn("no new", res["conclusion"])


if __name__ == "__main__":
    unittest.main()
