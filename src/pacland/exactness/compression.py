"""The compression engine — is there structure, or is the data a list? (D17)

A body of facts "compresses" if a model predicts held-out cases better than the base rate. That is a
falsifiable claim about structure, and it is the one way to test "the universe is structured" without a
laboratory: predict, hold out, compare.

**The model class is a recorded decision, not a search.** One prespecified logistic model on
`[1, log(|Nflux|), degree, h12]` — no feature search, no tuning on the holdout, no model zoo. Anything
selected by looking at the held-out score is not a held-out score.

**The baseline is the marginal.** Train the SUSY rate on the other families, predict the held-out family
with that constant, and compare log-loss and Brier. If the model cannot beat a constant, the features carry
no structure that generalises — and *that is a full result*, reported as such.

**The honest boundary:** 16 families spanning three `h12` values, so a leave-one-family-out fold at
`h12 = 4` asks the model to extrapolate a category it has never seen. That is stated, not hidden.

Run:        python3 scripts/compression.py
Guarded by: tests/test_compression.py
"""
from __future__ import annotations

import math
import re


def _features(row, degree: int, h12: int) -> list:
    n = abs(float(row.get("Nflux") or 0.0))
    return [1.0, math.log1p(n), float(degree), float(h12)]


def _family_meta(name: str) -> tuple:
    m = re.match(r"h(\d+)_(\d+)", name)
    if not m:
        return 0, 0
    return int(m.group(1)), int(m.group(2))


def _sigmoid(z: float) -> float:
    if z > 35:
        return 1.0
    if z < -35:
        return 0.0
    return 1.0 / (1.0 + math.exp(-z))


def _fit(xs: list, ys: list, l2: float = 1.0, iters: int = 400, lr: float = 0.1) -> list:
    """Plain gradient descent on the logistic loss with an L2 term — small, prespecified, no library."""
    w = [0.0] * len(xs[0])
    m = len(xs)
    for _ in range(iters):
        g = [0.0] * len(w)
        for x, y in zip(xs, ys):
            p = _sigmoid(sum(wi * xi for wi, xi in zip(w, x)))
            r = p - y
            for i in range(len(w)):
                g[i] += r * x[i]
        for i in range(len(w)):
            w[i] -= lr * (g[i] / m + l2 * w[i] / m)
    return w


def _logloss(ps: list, ys: list) -> float:
    eps = 1e-12
    return -sum(math.log(max(min(p, 1 - eps), eps)) if y else math.log(max(min(1 - p, 1 - eps), eps))
                for p, y in zip(ps, ys)) / max(len(ys), 1)


def _brier(ps: list, ys: list) -> float:
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / max(len(ys), 1)


def compression(data_dir=None) -> dict:
    """Leave-one-family-out: does `[1, log|N|, degree, h12]` beat the marginal on unseen families?"""
    from . import counterexample as C

    corpus = C.load_corpus(data_dir)
    fams = sorted({c["file"] for c in corpus})
    rows = []
    for c in corpus:
        h12, degree = _family_meta(c["file"])
        rows.append((c["file"], _features(c["row"], degree, h12), 1 if c["row"].get("is_susy") else 0))

    base_ps, model_ps, ys = [], [], []
    for fam in fams:
        train = [(x, y) for f, x, y in rows if f != fam]
        test = [(x, y) for f, x, y in rows if f == fam]
        if not test or not train:
            continue
        base = sum(y for _, y in train) / len(train)
        w = _fit([x for x, _ in train], [y for _, y in train])
        for x, y in test:
            base_ps.append(base)
            model_ps.append(_sigmoid(sum(wi * xi for wi, xi in zip(w, x))))
            ys.append(y)

    ll_base, ll_model = _logloss(base_ps, ys), _logloss(model_ps, ys)
    br_base, br_model = _brier(base_ps, ys), _brier(model_ps, ys)
    improvement = (ll_base - ll_model) / ll_base if ll_base else 0.0
    if improvement > 0.02:
        verdict = "structure"
    elif improvement < -0.02:
        verdict = "no structure (the model is worse than the marginal)"
    else:
        verdict = "no structure"
    return {
        "folds": len(fams), "rows": len(ys),
        "logloss_marginal": ll_base, "logloss_model": ll_model,
        "brier_marginal": br_base, "brier_model": br_model,
        "improvement": improvement, "verdict": verdict,
        "boundary": ("16 families across three h12 values, so the h12 = 4 fold is extrapolation of a "
                     "category the model never saw; and the model class was fixed before the score was seen."),
    }


__all__ = ["compression"]
