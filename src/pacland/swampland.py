"""Swampland connection — turn the constraint-first conjecture into per-conjecture
falsifiable tests against the data we already hold.

``docs/constraint-first-conjecture.md`` claims: *the landscape's only structure is
what it forbids; everything it produces is noise plus a weak scale.* The swampland
program is the same claim stated as theory ("consistency forbids X"). This module is
the bridge: it treats each major swampland conjecture as a *constraint* and asks,
on the samples we actually have, whether that constraint shows up as

  * exactly determined by flux (r ~ 1.0) when it is a pure charge/consistency
    condition — the tadpole control, or
  * statistically uniform in flux (r < 0.25) when it depends on moduli
    stabilization — the W0/gs/mass class.

Every quantity is run through the Rule of Three (single-coordinate MI, joint
ridge-quadratic CV r, permutation null z) — no "structured"/"random" call from one
test. Each conjecture is then classified TESTABLE-NOW / NEEDS-BIGGER-MACHINE /
NOT-TESTABLE-IN-TRUNCATION, and the whole sector's honest accounting is reported.

Pure stdlib, like ``structure.py``.
"""
from __future__ import annotations

import math
import random
from math import gcd

import numpy as np

from .structure import ridge_cv_predictability, mi_significance


# --------------------------------------------------------------------------
# Rule of Three (the three independent confirmations, from the repo AGENTS.md)
# --------------------------------------------------------------------------

def _poly_features(f, degree: int = 2):
    """[1, f_i, f_i^2, f_i f_j] — identical to structure._poly_features."""
    feats = [1.0]
    n = len(f)
    feats.extend(float(f[i]) for i in range(n))
    if degree >= 2:
        feats.extend(float(f[i]) * float(f[i]) for i in range(n))
        for i in range(n):
            for j in range(i + 1, n):
                feats.append(float(f[i]) * float(f[j]))
    return feats


def _ridge_cv_np(fluxes, y, lam: float = 1.0, n_folds: int = 5, seed: int = 0) -> float:
    """The same ridge-quad CV estimator as ``structure.ridge_cv_predictability``,
    vectorized with numpy. Same features, same lambda, same fold split (same
    ``random.Random(seed).shuffle``), so the number agrees with the canonical
    stdlib version to numerical precision — cross-checked on the tadpole anchor.
    """
    n = len(fluxes)
    rng = random.Random(seed)
    idx = list(range(n))
    rng.shuffle(idx)
    folds = [idx[i::n_folds] for i in range(n_folds)]
    X = np.array([_poly_features(list(f)) for f in fluxes], dtype=float)
    Y = np.array(list(y), dtype=float)
    preds = np.zeros(n)
    for fold in folds:
        train = [i for i in idx if i not in set(fold)]
        Xtr, Ytr = X[train], Y[train]
        Xte = X[fold]
        d = Xtr.shape[1]
        A = Xtr.T @ Xtr + lam * np.eye(d)
        beta = np.linalg.solve(A, Xtr.T @ Ytr)
        preds[fold] = Xte @ beta
    return float(_pearson(preds.tolist(), list(Y)))


def _ridge_permutation_z(fluxes, y, permutations: int = 200, seed: int = 0) -> dict:
    """z-score of the true ridge-quad CV r against a shuffled-y null distribution."""
    rng = random.Random(seed)
    true = _ridge_cv_np(fluxes, y, seed=seed)
    yl = np.array(list(y), dtype=float)
    null = []
    for _ in range(permutations):
        rng.shuffle(yl)
        null.append(_ridge_cv_np(fluxes, yl.tolist(), seed=seed))
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / len(null)
    std = var ** 0.5
    return {"r": true, "null_mean": mean, "z": (true - mean) / std if std > 0 else 0.0}


def rule_of_three(fluxes, y, permutations: int = 200, seed: int = 0) -> dict:
    """Three independent confirmations of structure in ``flux -> y``.

    Returns the joint ridge-quad CV r, its permutation z, the best single-coordinate
    MI z, and a verdict per the Rule of Three. ``structured`` needs the strong
    (joint quadratic) test to pass — it catches multi-coordinate structure that
    single-coordinate MI is blind to (the tadpole). ``random`` needs both the strong
    test and MI to fail. Anything in between is ``unresolved``, never "one test
    says X so X".
    """
    n = len(fluxes)
    if n < 3 or len(y) != n or n == 0:
        return {"ridge_r": float("nan"), "ridge_z": 0.0, "mi_z": 0.0,
                "verdict": "unresolved", "n": n}
    cols = [[f[i] for f in fluxes] for i in range(len(fluxes[0]))]
    mi_z = max(mi_significance(c, y, permutations=permutations, seed=seed)["z"]
               for c in cols)
    ridge = _ridge_permutation_z(fluxes, y, permutations=permutations, seed=seed)
    r, rz = ridge["r"], ridge["z"]
    # The joint quadratic test is the STRONG test: it catches multi-coordinate
    # structure (the tadpole's symplectic pairing F^T J H) that single-coordinate
    # MI is blind to. So MI is *sufficient* for structure (single-coordinate) but
    # not *necessary*. "structured" needs the strong test to pass; "random" needs
    # both the strong test AND MI to fail; anything else is unresolved.
    if r > 0.5 and rz >= 3.0:
        verdict = "structured"
    elif r < 0.25 and mi_z < 3.0:
        verdict = "random"
    else:
        verdict = "unresolved"
    return {"ridge_r": r, "ridge_z": rz, "mi_z": mi_z, "verdict": verdict, "n": n}


# --------------------------------------------------------------------------
# Conjecture 1 — Weak Gravity (electric): the magnetic scale Lambda_i = g_i M_pl
# --------------------------------------------------------------------------

def wgc_scales(vacua):
    """Per-vacuum electric-WGC scales (g_min, g_mean), each a scalar.

    ``log_g2_inv = log(1/g^2)``, so ``g = exp(-log_g2_inv / 2)``. A vacuum has a
    variable number of U(1) factors (1..3 across the sample), so the salient
    per-vacuum quantities are the *smallest* coupling g_min (the strongest electric
    WGC bound — the earliest tower) and the geometric mean g_mean. The WGC says a
    unit-charge state must exist at or below ``~ g * M_pl``; the scale itself is the
    testable-now half. The *existence* half (a super-extremal state in the spectrum)
    needs the full charged spectrum and is NEEDS-BIGGER-MACHINE.
    """
    rows = []
    for p in vacua:
        gs = [math.exp(-lg / 2.0) for lg in p["log_g2_inv"]]
        gmin = min(gs)
        gmean = math.exp(sum(math.log(g) for g in gs) / len(gs))
        rows.append((gmin, gmean))
    return rows


# --------------------------------------------------------------------------
# Conjecture 2 — No global symmetries: charge-lattice common divisor
# --------------------------------------------------------------------------

def charge_gcd(vacua) -> int:
    """Global gcd of every flux integer across the sample.

    If gcd > 1, every charge is a multiple of d and the theory carries a forced
    Z_d discrete global symmetry — which the no-global-symmetries conjecture forbids.
    gcd == 1 is the consistent (necessary-condition) result. The *complete* statement
    is not an SNF over the flux sample (the flux lattice is Z^{2b3} by quantization,
    so unimodular tautologically); it is the unimodularity of the *gauge* charge
    lattice, fixed by the intersection-form charge matrix inside the model — a
    model-internal quantity, classified NEEDS-MODEL-INTERNALS.
    """
    g = 0
    for p in vacua:
        for v in p["flux"]:
            g = gcd(g, abs(int(v)))
    return g


# --------------------------------------------------------------------------
# Conjecture 3 — Distance: lightest-mass scale vs field distance (proxy)
# --------------------------------------------------------------------------

def distance_proxy(points):
    """Distance-conjecture proxy on the SUSY slice.

    Returns (fluxes, log_m_light, log_distance) where ``log_m_light`` is the log of
    the lightest mass eigenvalue and ``log_distance`` is the log of the Euclidean
    distance of the (CS) moduli VEV from the sample centroid. The full conjecture
    runs on the Kaehler moduli (flat at degree-0) and the full tower, so this is
    NEEDS-BIGGER-MACHINE; the proxy is computed to show what the truncated slice
    can and cannot see.
    """
    susy = [p for p in points if p.get("is_susy") and p.get("eigs")]
    if not susy:
        return [], [], []
    coords = []
    for p in susy:
        coords.append([float(x) for x in (list(p["moduli_re"]) + list(p["moduli_im"]))])
    m = len(coords[0])
    centroid = [sum(c[i] for c in coords) / len(coords) for i in range(m)]
    fluxes, log_m, log_d = [], [], []
    for p, c in zip(susy, coords):
        eig0 = max(float(p["eigs"][0]), 1e-300)
        dist = math.sqrt(sum((c[i] - centroid[i]) ** 2 for i in range(m)))
        fluxes.append([float(x) for x in p["flux"]])
        log_m.append(0.5 * math.log(eig0))
        log_d.append(math.log(max(dist, 1e-300)))
    return fluxes, log_m, log_d


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------

def swampland_report(vacua, rich_points):
    """Classify each swampland conjecture against the data and return a report dict.

    ``vacua``: entries with ``flux``, ``log_g2_inv`` (the 107-vacua sample).
    ``rich_points``: entries with ``flux``, ``moduli_re/im``, ``eigs``, ``is_susy``.
    """
    fluxes = [[float(x) for x in p["flux"]] for p in vacua]

    report = {
        "n_vacua": len(vacua),
        "conjectures": {},
    }

    # 1 — Weak Gravity: magnetic scale structure (testable now)
    scales = wgc_scales(vacua)
    report["conjectures"]["weak_gravity"] = {
        "status": "TESTABLE-NOW (scale); NEEDS-BIGGER-MACHINE (existence)",
        "g_min_structure": rule_of_three(fluxes, [s[0] for s in scales]),
        "g_mean_structure": rule_of_three(fluxes, [s[1] for s in scales]),
    }

    # 2 — No global symmetries: common charge divisor
    report["conjectures"]["no_global_symmetries"] = {
        "status": "TESTABLE-NOW (gcd necessary condition); NEEDS-MODEL-INTERNALS (gauge lattice)",
        "charge_gcd": charge_gcd(vacua),
        "consistent": charge_gcd(vacua) == 1,
    }

    # 3 — Distance: full Rule-of-Three on the SUSY slice
    dc = distance_conjecture_test(rich_points)
    dc["status"] = "NEEDS-BIGGER-MACHINE (clean test: Kaehler moduli + geodesic distance)"
    report["conjectures"]["distance"] = dc

    # 4 — Gravity/tadpole consistency (the anchor, exact constraint)
    tad = [float(p["tadpole"]) for p in vacua if "tadpole" in p]
    if tad:
        report["conjectures"]["gravity_tadpole"] = {
            "status": "TESTABLE-NOW (the exact constraint, the anchor)",
            "rule_of_three": rule_of_three(
                [[float(x) for x in p["flux"]] for p in vacua if "tadpole" in p], tad),
        }

    return report


def _pearson(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def _rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for pos, i in enumerate(order):
        r[i] = float(pos + 1)
    return r


def _spearman(xs, ys):
    return _pearson(_rank(xs), _rank(ys))


def _perm_z(xs, ys, fn, permutations: int = 1000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    true = fn(xs, ys)
    yy = list(ys)
    null = []
    for _ in range(permutations):
        rng.shuffle(yy)
        null.append(fn(xs, yy))
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / len(null)
    std = var ** 0.5
    return {"r": true, "z": (true - mean) / std if std > 0 else 0.0,
            "null_mean": mean}


def distance_conjecture_test(points):
    """Full Rule-of-Three on the distance-conjecture proxy (CS-moduli slice).

    The distance conjecture predicts a tower of states whose mass falls
    exponentially with field distance, i.e. log(m) decreasing with distance. We
    measure that direction on the SUSY slice: log of the lightest mass eigenvalue
    against the Euclidean distance of the (CS) moduli VEV from the sample centroid.
    Two independent correlation estimators (Pearson and rank Spearman), each with a
    permutation null, plus a flux-controlled residual to check the signal is not
    just the already-known flux->mass-scale structure. Honest caveat: this runs on
    the CS moduli, not the Kaehler moduli where the conjecture actually lives, and
    the distance is centroid-Euclidean, not a field-space geodesic.
    """
    susy = [p for p in points if p.get("is_susy") and p.get("eigs")]
    n = len(susy)
    if n < 3:
        return {"verdict": "insufficient", "n": n}
    coords = [[float(x) for x in (list(p["moduli_re"]) + list(p["moduli_im"]))]
              for p in susy]
    fluxes = [[float(x) for x in p["flux"]] for p in susy]
    m = len(coords[0])
    centroid = [sum(c[i] for c in coords) / n for i in range(m)]
    log_m, dist = [], []
    for p, c in zip(susy, coords):
        eig0 = max(float(p["eigs"][0]), 1e-300)
        log_m.append(0.5 * math.log(eig0))
        dist.append(math.sqrt(sum((c[i] - centroid[i]) ** 2 for i in range(m))))

    pearson = _perm_z(dist, log_m, _pearson)
    spearman = _perm_z(dist, log_m, _spearman)

    # flux-controlled residual: remove the ridge-quadratic flux prediction of log_m
    X = np.array([_poly_features(list(f)) for f in fluxes], dtype=float)
    Y = np.array(log_m, dtype=float)
    A = X.T @ X + 1.0 * np.eye(X.shape[1])
    beta = np.linalg.solve(A, X.T @ Y)
    resid = (Y - X @ beta).tolist()
    residual_r = _pearson(resid, dist)

    strong = abs(pearson["z"]) >= 3.0 and abs(spearman["z"]) >= 3.0
    return {
        "verdict": "real-signal" if strong else "unresolved",
        "n": n,
        "pearson_logm_dist": pearson,
        "spearman_logm_dist": spearman,
        "flux_ridge_cv_r": ridge_cv_predictability(fluxes, log_m),
        "residual_vs_distance_pearson": residual_r,
    }


__all__ = [
    "rule_of_three",
    "wgc_scales",
    "charge_gcd",
    "distance_proxy",
    "distance_conjecture_test",
    "swampland_report",
]
