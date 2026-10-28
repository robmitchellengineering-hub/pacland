"""An outside claim, put through the machine: the three checks must keep their numerical content."""
import math
import unittest

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("padgett", ROOT / "scripts" / "check_padgett_claims.py")
padgett = importlib.util.module_from_spec(spec)
spec.loader.exec_module(padgett)


class TestInterference(unittest.TestCase):
    def test_the_sum_cancels_at_a_generic_phase(self):
        r = padgett.claim1()
        self.assertTrue(r["cancels_like_random_walk"], r["rows"])

    def test_parity_does_all_the_work(self):
        r = padgett.claim1()
        self.assertTrue(r["parity_does_all_the_work"], r["theta_pi_per_term"])
        # the control is the point: odd composites and primes are indistinguishable at theta = pi
        self.assertAlmostEqual(r["theta_pi_per_term"]["odd composites"],
                               r["theta_pi_per_term"]["primes"], places=1)


class TestPrimeFraction(unittest.TestCase):
    def test_the_prime_fraction_falls_towards_zero(self):
        r = padgett.claim2()
        self.assertTrue(r["tends_to_zero"])
        fractions = [row["prime_fraction"] for row in r["rows"]]
        self.assertTrue(all(a > b for a, b in zip(fractions, fractions[1:])))

    def test_it_cannot_match_a_constant_cosmic_fraction(self):
        r = padgett.claim2()
        self.assertGreater(r["dark_over_baryon"], 5.0)     # 5.47, and constant
        self.assertLess(r["rows"][-1]["prime_fraction"], 0.08)


class TestDefinitional(unittest.TestCase):
    def test_hf_equals_hbar_omega_by_definition(self):
        r = padgett.claim3()
        self.assertTrue(r["identical_by_definition"])


if __name__ == "__main__":
    unittest.main()
