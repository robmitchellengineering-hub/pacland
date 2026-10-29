"""The explicit formula: psi from a sieve validates the psi from the zeros."""
import unittest

from pacland.spectral import explicit as E


class TestPsi(unittest.TestCase):
    def test_psi_matches_the_known_values(self):
        for x, want in E.KNOWN_PSI.items():
            self.assertAlmostEqual(E.chebyshev_psi(x), want, places=3)

    def test_psi_counts_prime_powers(self):
        # prime powers <= 10 are 2, 4, 8 (= 2^3), 3, 9 (= 3^2), 5, 7, so
        # psi(10) = 3 ln2 + 2 ln3 + ln5 + ln7. The first version of this test said 4 ln2 and failed
        # against a correct implementation: the test was wrong, not the code.
        import math
        want = (math.log(2) * 3 + math.log(3) * 2 + math.log(5) + math.log(7))
        self.assertAlmostEqual(E.chebyshev_psi(10), want, places=9)


class TestFormula(unittest.TestCase):
    def test_the_zeros_reconstruct_psi(self):
        zs = E.find_zeros(t_to=400.0)
        c = E.convergence(100.0, zs)
        self.assertLess(c["best_error"], 1.0)

    def test_more_zeros_do_not_make_it_worse_at_low_x(self):
        zs = E.find_zeros(t_to=400.0)
        c = E.convergence(100.0, zs)
        self.assertLess(abs(c["rows"][-1]["error"]), abs(c["rows"][0]["error"]))


class TestAudit(unittest.TestCase):
    def test_all_checks_are_green(self):
        a = E.audit()
        self.assertTrue(a["all_pass"], [c for c in a["checks"] if not c["pass"]])
