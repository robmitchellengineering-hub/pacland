"""Bayesian optimization reaches a known optimum in few evaluations."""
import unittest

from pacland import bayesopt


class TestBayesOptimize(unittest.TestCase):
    def test_finds_a_quadratic_maximum(self):
        # f(x) = -(x-0.3)^2, max at x=0.3 with value 0
        res = bayesopt.bayes_optimize(lambda x: -(x - 0.3) ** 2, (0.0, 1.0),
                                      n_init=3, n_iter=10, seed=0)
        self.assertLess(abs(res["x"] - 0.3), 0.1)
        self.assertEqual(res["n_evals"], 13)

    def test_beats_a_dense_grid_in_evaluations(self):
        objective = bayesopt._demo_objective
        grid = [objective(x) for x in __import__("numpy").linspace(0.0, 1.0, 400)]
        res = bayesopt.bayes_optimize(objective, (0.0, 1.0), n_init=3, n_iter=15, seed=0)
        # within a small tolerance of the grid optimum, using far fewer evaluations
        self.assertLess(res["n_evals"], 50)
        self.assertGreaterEqual(res["y"], max(grid) - 0.05)


if __name__ == "__main__":
    unittest.main()
