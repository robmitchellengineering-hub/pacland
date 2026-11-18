"""The finite-T Polyakov loop: correct on a cold config and a positive screening mass near Tc."""
import unittest

import numpy as np

from pacland import polyakov as pk


class TestPolyakov(unittest.TestCase):
    def test_cold_polyakov_loop_is_three(self):
        # all links = identity => P = Tr(I) = 3
        links = np.zeros((4, 2, 4, 4, 4, 3, 3), dtype=complex)
        for i in range(4):
            for j in range(2 * 4 ** 3):
                idx = np.unravel_index(j, (2, 4, 4, 4))
                links[i][idx] = np.eye(3)
        self.assertAlmostEqual(pk.polyakov_loop(links, (0, 0, 0)), 3.0)

    def test_correlator_is_connected(self):
        # a correlator is connected: C = <PP> - <P>^2, so it is exactly 0 when P is constant
        links = np.zeros((4, 2, 4, 4, 4, 3, 3), dtype=complex)
        for i in range(4):
            for j in range(2 * 4 ** 3):
                idx = np.unravel_index(j, (2, 4, 4, 4))
                links[i][idx] = np.eye(3)
        self.assertAlmostEqual(pk.polyakov_correlator(links, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
