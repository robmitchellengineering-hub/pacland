"""X8 — the control gate: no statistic is read against a constant, and no verdict below the sample size.

Twice this programme has read a statistic against a reference that was not the same object: the `|W|`
lattice (no fluctuations to report) and the 0.5307 scare (the **GOE** asymptotic value used as GUE's).
The fix is structural:

* every control is computed at **the same dimension**, **the same number of spectra** and the same
  pooling as the data;
* the gate refuses a verdict when the bands overlap — and says how many spectra it would take;
* an **authority test** runs the pipeline on objects whose class is known by construction: GOE matrices
  must read GOE, and a resampling that keeps the marginal but destroys repulsion must read Poisson.

The last part is not a formality. Measured at `dim = 6` (the corpus's spectrum), 40 spectra are **not
enough**: the GOE and Poisson bands sit 2.4 combined sd apart, so a correct pipeline returns
`undecidable`. The gate's job is to say that before a number is read, not after — and to turn it into a
sample-size requirement, which is the same shape of answer as "how many microphones identify how many
modes".

`ratio_statistic` is the zeros arm's estimator, imported rather than re-implemented.
"""
from __future__ import annotations

import numpy as np

from ..spectral import zeros as Z

#: asymptotic ratio for real-symmetric (GOE) matrices. Named because this repository used 0.5307 for
#: years under the name `RATIO_GUE`: the value is right, the ensemble was wrong.
RATIO_GOE_ASYMPTOTIC = 0.5307
RATIO_POISSON = 0.3863


def unfold(values: list[float]) -> list[float]:
    """Sort, difference, divide by the mean spacing. `[]` for fewer than two levels."""
    v = sorted(float(x) for x in values)
    if len(v) < 2:
        return []
    s = [b - a for a, b in zip(v, v[1:])]
    mean = float(np.mean(s))
    if mean <= 0:
        return []
    return [float(np.cumsum(s)[i] / mean) for i in range(len(s))]


def pooled_ratio(spectra: list[list[float]]) -> float:
    """The ratio statistic on per-spectrum unfolded spacings, pooled. `nan` if too small."""
    spacings: list[float] = []
    for s in spectra:
        u = unfold(s)
        spacings.extend(float(b - a) for a, b in zip(u, u[1:]))
    if len(spacings) < 4:
        return float("nan")
    return Z.ratio_statistic(spacings)


def _goe_matrix(dim: int, rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(dim, dim))
    return (a + a.T) / np.sqrt(2.0)


def _gue_matrix(dim: int, rng: np.random.Generator) -> np.ndarray:
    a = (rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))) / np.sqrt(2.0)
    return (a + a.conj().T) / np.sqrt(2.0)


def synthetic_spectra(dim: int, count: int, kind: str, seed: int = 3) -> list[list[float]]:
    """`count` spectra of `dim` levels whose spacing class is known by construction.

    `goe` / `gue`: eigenvalue spectra of random matrices — repulsion, by construction.
    `poisson`: levels drawn i.i.d. from the *same marginal* as the GOE ensemble, which keeps the
    density and destroys the correlation. That is the honest null for a level-statistics test.
    """
    rng = np.random.default_rng(seed)
    if kind in ("goe", "gue"):
        make = _goe_matrix if kind == "goe" else _gue_matrix
        return [sorted(float(x) for x in np.linalg.eigvalsh(make(dim, rng))) for _ in range(count)]
    if kind == "poisson":
        seed_spectra = [np.sort(np.linalg.eigvalsh(_goe_matrix(dim, rng)))
                        for _ in range(max(count // 4, 1))]
        marginal = np.concatenate(seed_spectra)
        return [sorted(float(x) for x in rng.choice(marginal, size=dim, replace=True))
                for _ in range(count)]
    raise ValueError(f"unknown control kind {kind!r}")


def control_band(dim: int, count: int, kind: str, trials: int = 60, seed: int = 3) -> dict:
    """The ratio statistic's distribution for a synthetic class at *this* size and pooling."""
    vals = []
    for t in range(trials):
        r = pooled_ratio(synthetic_spectra(dim, count, kind, seed=seed + t))
        if r == r:                                    # not nan
            vals.append(r)
    if not vals:
        return {"kind": kind, "dim": dim, "count": count, "n": 0, "mean": float("nan"),
                "sd": float("nan")}
    return {"kind": kind, "dim": dim, "count": count, "n": len(vals), "trials": trials,
            "mean": float(np.mean(vals)), "sd": float(np.std(vals))}


def separation(dim: int, count: int, trials: int = 40, seed: int = 3) -> float:
    """How far apart the GOE and Poisson bands are, in combined standard deviations."""
    g = control_band(dim, count, "goe", trials, seed)
    p = control_band(dim, count, "poisson", trials, seed)
    return abs(g["mean"] - p["mean"]) / max(g["sd"] + p["sd"], 1e-12)


def required_count(dim: int, want_sd: float = 5.0, trials: int = 20, seed: int = 3,
                   c0: int = 32, cap: int = 8192) -> int:
    """The number of spectra at which GOE and Poisson separate by `want_sd`, estimated then verified.

    Bisection by simulation is the obvious method and the wrong one: each probe is thousands of
    eigendecompositions. The standard deviation of the estimator falls as `1/sqrt(count)`, so a
    measured separation at a small size predicts the size needed; the prediction is then **verified**
    at that size and at 1.3x it, and the smaller verified value is returned. `cap` means "not reachable
    at this dimension and budget", which is a statement about the question, not a bug.
    """
    s0 = separation(dim, c0, trials, seed)
    if s0 <= 1e-9:
        return cap
    est = int(np.ceil(c0 * (want_sd / s0) ** 2)) + 1
    for c in (min(est, cap), min(int(est * 1.3) + 1, cap)):
        if separation(dim, c, trials, seed) >= want_sd:
            return c
    return cap


def gate(spectra: list[list[float]], trials: int = 60, seed: int = 3) -> dict:
    """Measure a sample and place it against matched GOE / GUE / Poisson bands.

    `verdict` is `goe`, `gue`, `poisson`, `between`, or `undecidable` — the last when the bands overlap,
    in which case the sample carries no class and the report says so.
    """
    dims = {len(s) for s in spectra}
    if len(dims) != 1:
        raise ValueError(f"gate needs spectra of one dimension, got {sorted(dims)}")
    dim = dims.pop()
    count = len(spectra)
    measured = pooled_ratio(spectra)
    bands = {k: control_band(dim, count, k, trials, seed) for k in ("goe", "gue", "poisson")}
    sep = abs(bands["goe"]["mean"] - bands["poisson"]["mean"]) / max(
        bands["goe"]["sd"] + bands["poisson"]["sd"], 1e-12)
    if sep < 5.0:
        return {"measured": measured, "dim": dim, "count": count, "bands": bands,
                "separation_sd": sep, "verdict": "undecidable",
                "why": f"the GOE and Poisson bands are {sep:.1f} combined sd apart at this size, so "
                       "no class can be assigned; "
                       f"{required_count(dim)} spectra of dim {dim} would separate them",
                "required_count": required_count(dim)}
    best = min(bands, key=lambda k: abs(measured - bands[k]["mean"]) / max(bands[k]["sd"], 1e-12))
    z = abs(measured - bands[best]["mean"]) / max(bands[best]["sd"], 1e-12)
    return {"measured": measured, "dim": dim, "count": count, "bands": bands,
            "separation_sd": sep, "verdict": best if z < 3.0 else "between",
            "why": f"closest band {best} at {z:.2f} sd", "required_count": None}


def authority_check(available: int | None = None, trials: int = 40, seed: int = 11) -> dict:
    """Does the pipeline recover classes it cannot know the answer to? Then — and only then — is it used.

    Three cells with known answers, at the sample size the gate itself says is required:

    1. GOE spectra must read `goe`;
    2. the same marginal with the repulsion destroyed must read `poisson`;
    3. the required size must be reachable (`available` spectra, when the caller knows it).
    """
    need = required_count(6, 5.0, max(trials // 2, 12), seed)
    goe = synthetic_spectra(6, need, "goe", seed=seed)
    poi = synthetic_spectra(6, need, "poisson", seed=seed)
    g = gate(goe, trials=trials, seed=seed)
    p = gate(poi, trials=trials, seed=seed)
    cells = [
        {"cell": f"GOE spectra of dim 6 read as GOE ({need} of them)", "pass": g["verdict"] == "goe",
         "detail": f"measured {g['measured']:.4f}, band {g['bands']['goe']['mean']:.4f} +- "
                   f"{g['bands']['goe']['sd']:.4f} -> {g['verdict']}"},
        {"cell": f"the same marginal with the repulsion destroyed reads as Poisson ({need} spectra)",
         "pass": p["verdict"] == "poisson",
         "detail": f"measured {p['measured']:.4f}, band {p['bands']['poisson']['mean']:.4f} +- "
                   f"{p['bands']['poisson']['sd']:.4f} -> {p['verdict']}"},
        {"cell": "the two bands are separable at that size", "pass": g["separation_sd"] > 5.0,
         "detail": f"{g['separation_sd']:.1f} combined sd apart at {need} spectra"},
    ]
    if available is not None:
        cells.append({"cell": f"the required size is reachable ({available} spectra available)",
                      "pass": need <= available,
                      "detail": f"needs {need}, available {available}"})
    return {"cells": cells, "n_pass": sum(c["pass"] for c in cells), "n": len(cells),
            "all_pass": all(c["pass"] for c in cells), "required_count": need,
            "goe_gate": g, "poisson_gate": p}


__all__ = ["RATIO_GOE_ASYMPTOTIC", "RATIO_POISSON", "unfold", "pooled_ratio", "synthetic_spectra",
           "control_band", "separation", "required_count", "gate", "authority_check"]
