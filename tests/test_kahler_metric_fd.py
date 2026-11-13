"""The hand-written finite-difference Kähler metric: reproduces the analytic STU metric, no autodiff."""
import unittest

import numpy as np

from pacland.oracle import potential_t6 as P
from pacland.oracle.kahler_metric_fd import kahler_metric_fd, real_hessian_of


def _K(z):
    return P.kahler_full(*z)


class TestKahlerMetricFD(unittest.TestCase):
    def test_reproduces_the_analytic_stu_metric(self):
        z = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
        g_analytic = P.kahler_metric(*z)
        g_fd = kahler_metric_fd(_K, z)
        self.assertLess(np.max(np.abs(g_fd - g_analytic)), 1e-6)

    def test_metric_is_hermitian(self):
        z = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
        g = kahler_metric_fd(_K, z)
        self.assertLess(np.max(np.abs(g - g.conj().T)), 1e-10)

    def test_off_diagonal_vanishes_for_separable_kahler(self):
        # the STU K is separable, so g_iȷ̄ is diagonal
        z = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
        g = kahler_metric_fd(_K, z)
        off = np.abs(g - np.diag(np.diag(g)))
        self.assertLess(np.max(off), 1e-6)


if __name__ == "__main__":
    unittest.main()
