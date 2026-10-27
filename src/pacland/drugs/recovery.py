"""Synthetic recovery and invariance for drug discovery — classes 4 and 2, third discipline.

The oracles doctrine is only a method if it transfers. It reached physics (exact structure),
climate (conservation + invariance) and economics (identities + invariance + recovery). This
takes it to drug discovery, where the ground truth that *would* verify a claim — does the
compound work in humans? — is the thing nobody can measure cheaply.

Two classes, both cheap and both usable before a single patient is dosed:

  class 4 (synthetic)   invent a dose-response curve whose IC50 and Hill slope we chose, then
                        demand the fit recover them. If it cannot recover a truth that is
                        definitely there, it is not measuring potency.
  class 2 (invariance)  change the concentration units (nM -> uM): the Hill slope must not move
                        at all, and the IC50 must move exactly with the unit. Anything else means
                        the "potency" was partly an artefact of how the plate was written down.

The seeded fault is the assay trap that actually bites in practice: fitting with the asymptotes
**fixed** at the textbook 0 and 100 when the real curve is, say, 10 and 90. The IC50 then comes
out biased — and looks perfectly precise while doing so.

Run:        python3 scripts/drugs_recovery.py
Guarded by: tests/test_drugs_recovery.py
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

from ..economics.estimate import nelder_mead

#: Noiseless recovery tolerance. The fit is iterative, so this is round-off plus simplex tol.
EXACT = 1e-4


@dataclass(frozen=True)
class Curve:
    """The four-parameter logistic every assay is fitted with."""

    top: float = 100.0
    bottom: float = 10.0
    ic50: float = 50.0
    hill: float = 1.0

    def response(self, x: float) -> float:
        return self.bottom + (self.top - self.bottom) / (1.0 + (x / self.ic50) ** self.hill)


def sample(curve: Curve, xs: list[float], noise: float = 0.0, seed: int = 5) -> list[float]:
    rng = random.Random(seed)
    return [curve.response(x) + (rng.gauss(0.0, noise) if noise else 0.0) for x in xs]


def concentrations(decades: float = 4.0, per_decade: int = 4,
                   centre: float = 50.0) -> list[float]:
    """A typical dilution series, log-spaced around the expected IC50."""
    n = int(decades * per_decade) + 1
    lo = math.log10(centre) - decades / 2
    return [10.0 ** (lo + i * decades / (n - 1)) for i in range(n)]


def fit(xs: list[float], ys: list[float], *, fixed_bottom: float | None = None,
        fixed_top: float | None = None) -> Curve:
    """Fit the four parameters; optionally pin an asymptote (the trap the guard tests)."""
    free = []
    if fixed_top is None:
        free.append("top")
    if fixed_bottom is None:
        free.append("bottom")
    free += ["ic50", "hill"]

    start = [100.0, 10.0, sorted(xs)[len(xs) // 2], 1.0]
    if fixed_top is not None:
        start[0] = fixed_top
    if fixed_bottom is not None:
        start[1] = fixed_bottom

    def unpack(params: list[float]) -> Curve:
        vals = dict(zip(free, params))
        return Curve(top=fixed_top if fixed_top is not None else vals["top"],
                     bottom=fixed_bottom if fixed_bottom is not None else vals["bottom"],
                     ic50=vals["ic50"], hill=vals["hill"])

    def loss(params: list[float]) -> float:
        c = unpack(params)
        if c.ic50 <= 0.0 or c.hill <= 0.0 or c.top <= c.bottom:
            return 1e12
        return sum((c.response(x) - y) ** 2 for x, y in zip(xs, ys))

    x0 = [start[free.index(k)] for k in free]
    best, _ = nelder_mead(loss, x0, step=0.5, iters=4000, tol=1e-14)
    return unpack(best)


def recovery(truth: Curve = Curve(), noise: float = 0.0) -> dict:
    xs = concentrations()
    ys = sample(truth, xs, noise)
    est = fit(xs, ys)
    return {"truth": truth, "estimate": est,
            "ic50_error_rel": abs(est.ic50 - truth.ic50) / truth.ic50,
            "hill_error_rel": abs(est.hill - truth.hill) / truth.hill,
            "pass": (abs(est.ic50 - truth.ic50) / truth.ic50 < EXACT
                     and abs(est.hill - truth.hill) / truth.hill < EXACT)}


def guard_fixed_asymptotes(truth: Curve = Curve()) -> tuple[bool, str]:
    """MUTATION: pin the asymptotes at 0 and 100 when the truth is 10 and 90, and the IC50
    must come out biased by a visible margin — the guard fires when the bias is detected."""
    xs = concentrations()
    ys = sample(truth, xs)
    honest = fit(xs, ys)
    trapped = fit(xs, ys, fixed_bottom=0.0, fixed_top=100.0)
    bias_rel = abs(trapped.ic50 - truth.ic50) / truth.ic50
    detected = bias_rel > 0.05
    ok = detected and abs(honest.ic50 - truth.ic50) / truth.ic50 < EXACT
    return ok, (f"asymptotes: honest fit IC50 {honest.ic50:.3f} (truth {truth.ic50:.1f}); "
                f"pinned-at-0/100 fit IC50 {trapped.ic50:.3f} — bias {bias_rel:.1%} "
                f"detected = {detected}")


def units_invariance(truth: Curve = Curve(), factor: float = 1000.0) -> dict:
    """Class 2: express the concentrations in a finer unit. IC50 must scale exactly; the Hill
    slope must not move at all."""
    xs = concentrations()
    ys = sample(truth, xs)
    scaled = fit([x * factor for x in xs], ys)
    return {"factor": factor,
            "ic50_ratio": scaled.ic50 / fit(xs, ys).ic50,
            "hill": scaled.hill,
            "pass": (abs(scaled.ic50 / (fit(xs, ys).ic50 * factor) - 1.0) < 1e-3
                     and abs(scaled.hill - truth.hill) / truth.hill < 1e-3)}


def guard_units() -> tuple[bool, str]:
    """MUTATION: if the units did NOT scale the IC50, the test would be blind to a unit error.
    Confirm the scaled IC50 really moved (a factor of 1000) while the slope did not."""
    r = units_invariance()
    moved = abs(r["ic50_ratio"] - 1000.0) < 1.0
    ok = r["pass"] and moved
    return ok, (f"units: IC50 ratio {r['ic50_ratio']:.2f} at factor 1000 (moved = {moved}), "
                f"Hill slope {r['hill']:.6f} (truth 1.0)")


def audit() -> dict:
    checks = []
    for name, run in (("dose-response recovery", lambda: (recovery()["pass"],
                                                          f"IC50 {recovery()['estimate'].ic50:.4f}, "
                                                          f"Hill {recovery()['estimate'].hill:.4f}")),
                      ("asymptotes", guard_fixed_asymptotes),
                      ("units", guard_units)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["Curve", "fit", "sample", "concentrations", "recovery", "guard_fixed_asymptotes",
           "units_invariance", "guard_units", "audit", "EXACT"]
