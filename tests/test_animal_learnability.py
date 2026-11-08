"""Smoke tests for pacland.animal.learnability — the instrument self-checks.

Deterministic structure must come out LEARNABLE; pure noise must not. This positive +
negative control pair proves the instrument can fail as well as pass.
"""
import numpy as np

from pacland.animal.learnability import (
    winsorize,
    ridge_cv_pearson,
    referent_verdict,
    learnability_split,
)


def _deterministic(n=400, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = 2.0 * X[:, 0] - X[:, 1] + 0.1 * rng.normal(size=n)
    return X, y


def test_winsorize_clips_outliers():
    w = winsorize(np.array([1.0, 2.0, 3.0, 1000.0]), lo=1.0, hi=99.0)
    assert w.max() < 1000.0


def test_ridge_pearson_recovers_deterministic_structure():
    X, y = _deterministic()
    assert ridge_cv_pearson(X, y, seed=0) > 0.9


def test_deterministic_target_is_learnable():
    X, y = _deterministic()
    yc = (y > np.median(y)).astype(int)  # binary cut of a deterministic signal
    out = learnability_split(X, yc, ["a", "b", "c", "d"], n_perm=100, seed=0)
    assert out["joint"]["z"] >= 3


def test_noise_target_is_not_learnable():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(300, 4))
    y = rng.integers(0, 3, size=300)  # labels independent of X
    out = learnability_split(X, y, ["a", "b", "c", "d"], n_perm=100, seed=0)
    assert out["joint"]["z"] < 3


def test_referent_verdict_bands():
    assert referent_verdict(0.95, 5.0) == "REFUTED (Rosetta unit)"
    assert referent_verdict(0.60, 5.0) == "graded (no Rosetta unit)"
    assert referent_verdict(0.60, 1.0) == "uniform (within null)"
