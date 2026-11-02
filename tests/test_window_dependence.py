"""H-A: the per-unit-b3 growth factor is the WINDOW's combinatorics, not a law of physics.

If the same "law" changes when the window changes, it was never a law. The content factor A = 8.554 at
|component| <= 1 is compared against the window's own size factor (2*max_abs+1)^2 = 9 at max_abs=1 and 25 at
max_abs=2. The factor tracks the window.
"""
import numpy as np
import unittest

from pacland.exactness import windows as W


def _content(b3, max_abs):
    f = W.enumerate_window(b3, max_abs)
    N = W.tadpoles(f)
    prim = np.array([W.primitive(r) for r in f])
    return int(((N > 0) & (N <= 1))[prim].sum())


class TestTheWindowSetsTheBase(unittest.TestCase):
    def test_the_factor_tracks_the_window_not_a_law(self):
        for ma, expected in ((1, 9.0), (2, 25.0)):
            k0, k1 = _content(2, ma), _content(4, ma)
            factor = (k1 / k0) ** 0.5
            self.assertAlmostEqual(factor, expected, delta=2.0, msg=f"max_abs={ma}: {factor}")

    def test_the_two_windows_give_different_laws(self):
        f1 = (_content(4, 1) / _content(2, 1)) ** 0.5
        f2 = (_content(4, 2) / _content(2, 2)) ** 0.5
        self.assertGreater(f2 - f1, 10.0)   # 8.6 vs 24.4

    def test_the_recorded_numbers(self):
        self.assertEqual(_content(2, 1), 20)
        self.assertEqual(_content(4, 1), 1480)
        self.assertEqual(_content(2, 2), 52)
        self.assertEqual(_content(4, 2), 30984)


class TestTheConsequence(unittest.TestCase):
    def test_the_content_law_is_window_determined(self):
        # A = 8.554 at max_abs=1 is close to 9 = (2*1+1)^2, the window's own per-b3 factor
        f1 = (_content(4, 1) / _content(2, 1)) ** 0.5
        self.assertAlmostEqual(f1, 9.0, delta=0.5)
        # so 'content grows 8.55x per unit b3' restates the window size, it does not measure the landscape


if __name__ == "__main__":
    unittest.main()
