"""Bayesian optimization over expensive oracles — efficient exploration.

Zoubin Ghahramani's field, applied to our expensive black boxes (the flux sampler, the DMRG
bond-dimension sweep, the JAXVacua critical-point search): fit a Gaussian-process surrogate to the
few points we have, and evaluate next where the **expected improvement** is largest. This reaches
the optimum in far fewer evaluations than a grid, which is what makes an oracle that costs real
compute worth probing at all.

Usage:
    python -m pacland.bayesopt demo
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.stats import norm


def _rbf(X1: np.ndarray, X2: np.ndarray, length_scale: float) -> np.ndarray:
    """Squared-exponential kernel (1-D inputs)."""
    X1 = np.asarray(X1).reshape(-1)
    X2 = np.asarray(X2).reshape(-1)
    sq = (X1[:, None] - X2[None, :]) ** 2
    return np.exp(-0.5 * sq / length_scale ** 2)


def _gp_posterior(X, y, X_test, length_scale: float, noise: float = 1e-6):
    """Zero-mean GP posterior (mean, std) at X_test, given (X, y) observations."""
    K = _rbf(X, X, length_scale) + noise * np.eye(len(X))
    L = cho_factor(K)
    Ks = _rbf(X, X_test, length_scale)
    mu = Ks.T @ cho_solve(L, y)
    var = _rbf(X_test, X_test, length_scale) - Ks.T @ cho_solve(L, Ks)
    var = np.clip(np.diag(var), 1e-12, None)
    return mu, np.sqrt(var)


def expected_improvement(mu: np.ndarray, sigma: np.ndarray, best: float) -> np.ndarray:
    """Expected improvement of a candidate over the best observation so far."""
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (mu - best) / sigma
        ei = (mu - best) * norm.cdf(z) + sigma * norm.pdf(z)
    ei = np.where(sigma < 1e-12, 0.0, ei)
    return ei


def bayes_optimize(objective, bounds, n_init: int = 3, n_iter: int = 15, seed: int = 0,
                   length_scale: float = 0.5) -> dict:
    """Maximize a 1-D expensive black box by expected-improvement Bayesian optimization."""
    lo, hi = bounds
    rng = np.random.default_rng(seed)
    X = rng.uniform(lo, hi, n_init)
    y = np.array([float(objective(x)) for x in X])
    for _ in range(n_iter):
        xs = np.linspace(lo, hi, 400)
        mu, sigma = _gp_posterior(X, y, xs, length_scale)
        ei = expected_improvement(mu, sigma, float(y.max()))
        x_next = xs[int(np.argmax(ei))]
        X = np.append(X, x_next)
        y = np.append(y, float(objective(x_next)))
    i = int(np.argmax(y))
    return {"x": float(X[i]), "y": float(y[i]), "n_evals": int(len(X))}


def _demo_objective(x: float) -> float:
    """A multimodal black box with a known global maximum (near x = 0.76)."""
    return float(np.sin(3.0 * x) + 0.3 * np.sin(10.0 * x) + 0.05 * x)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Bayesian optimization over an expensive oracle.")
    ap.add_argument("cmd", choices=["demo"], default="demo", nargs="?")
    args = ap.parse_args(argv)

    # grid reference: the best of a dense grid, to show how few evaluations BO needs
    grid = np.linspace(0.0, 1.0, 400)
    grid_best = max((_demo_objective(x), x) for x in grid)
    res = bayes_optimize(_demo_objective, (0.0, 1.0), n_init=3, n_iter=15, seed=0)
    print("Bayesian optimization on a multimodal black box (bounds [0,1]):")
    print(f"  best found      : x={res['x']:.3f}, f={res['y']:.3f}  ({res['n_evals']} evaluations)")
    print(f"  dense-grid best : x={grid_best[1]:.3f}, f={grid_best[0]:.3f}  (400 evaluations)")
    print(f"  BO reached within {abs(res['y'] - grid_best[0]):.3f} of the grid optimum in "
          f"{res['n_evals']}/400 evaluations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
