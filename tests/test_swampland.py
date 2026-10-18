import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.swampland import (
    charge_gcd,
    rule_of_three,
    swampland_report,
    wgc_scales,
)

ROOT = Path(__file__).resolve().parents[1]


def _load_vacua():
    with open(ROOT / "data" / "vacua_observables.json") as fh:
        d = json.load(fh)
    return [p for mk in d for p in d[mk]
            if "flux" in p and "log_g2_inv" in p and p["log_g2_inv"]]


class TestWGCScales(unittest.TestCase):
    def test_gmin_le_gmean(self):
        vacua = _load_vacua()
        self.assertTrue(vacua)
        for gmin, gmean in wgc_scales(vacua):
            self.assertLessEqual(gmin, gmean + 1e-12)
            self.assertGreater(gmin, 0.0)

    def test_scale_is_positive(self):
        vacua = _load_vacua()
        for gmin, gmean in wgc_scales(vacua):
            self.assertGreater(gmin, 0.0)
            self.assertGreater(gmean, 0.0)


class TestChargeGcd(unittest.TestCase):
    def test_common_divisor_detected(self):
        # every flux integer is a multiple of 2 -> forced Z_2 global symmetry
        vacua = [{"flux": [2, -4, 6, 8, -2, 4, 0, 2, 6, -8, 10, 2]}]
        self.assertEqual(charge_gcd(vacua), 2)

    def test_real_sample_coprime(self):
        self.assertEqual(charge_gcd(_load_vacua()), 1)


class TestRuleOfThree(unittest.TestCase):
    def _bilinear_fluxes(self, n=80, dim=6):
        import random
        rng = random.Random(1)
        fluxes, y = [], []
        h = dim // 2
        for _ in range(n):
            f = [rng.randint(-3, 3) for _ in range(dim)]
            fluxes.append([float(x) for x in f])
            y.append(sum(f[i] * f[h + i] for i in range(h)))  # symplectic-like pairing
        return fluxes, y

    def test_bilinear_is_structured(self):
        fluxes, y = self._bilinear_fluxes()
        r = rule_of_three(fluxes, y, permutations=40)
        self.assertEqual(r["verdict"], "structured", r)

    def test_random_y_is_random(self):
        import random
        fluxes, _ = self._bilinear_fluxes()
        rng = random.Random(7)
        y = [rng.random() for _ in fluxes]
        r = rule_of_three(fluxes, y, permutations=40)
        self.assertEqual(r["verdict"], "random", r)


class TestSwamplandReport(unittest.TestCase):
    def test_report_keys_and_anchor(self):
        vacua = _load_vacua()
        with open(ROOT / "data" / "rich_sample.json") as fh:
            rich = json.load(fh)["points"]
        rep = swampland_report(vacua, rich)
        for name in ("weak_gravity", "no_global_symmetries", "distance", "gravity_tadpole"):
            self.assertIn(name, rep["conjectures"])
        self.assertEqual(rep["conjectures"]["no_global_symmetries"]["consistent"], True)
        self.assertEqual(rep["conjectures"]["gravity_tadpole"]["rule_of_three"]["verdict"],
                         "structured")


if __name__ == "__main__":
    unittest.main()
