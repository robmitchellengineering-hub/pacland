import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.learnability import pseudo_dim_lower_bound, pseudo_shatters


def _linear_hypotheses(slopes, intercepts):
    return [lambda x, a=a, b=b: a * x + b for a in slopes for b in intercepts]


class TestPseudoShatters(unittest.TestCase):
    def test_linear_class_pseudo_dim_is_two(self):
        # The class {x -> a*x + b} has pseudo-dimension 2: it can pseudo-shatter
        # 2 points (two free parameters) but not 3 (a line cannot realize the
        # (high, low, high) pattern over collinear x1 < x2 < x3).
        hs = _linear_hypotheses([-2.0, -1.0, 0.0, 1.0, 2.0],
                                [-2.0, -1.0, 0.0, 1.0, 2.0])
        self.assertEqual(pseudo_dim_lower_bound(hs, [1.0, 2.0, 3.0]), 2)

    def test_single_function_pseudo_shatters_nothing(self):
        # one fixed function realizes only one value per point -> no shattering
        hs = [lambda x: 3.0]
        self.assertFalse(pseudo_shatters(hs, [1.0]))


if __name__ == "__main__":
    unittest.main()
