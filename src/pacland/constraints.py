"""Constraint verification (Q2 of ``docs/new-approach.md``).

The second pillar of constraint-first string theory: turn a swampland /
consistency constraint into a measurable, certifiable statement — "this constraint
eliminates fraction p of the sampled vacua, with confidence 1-delta." A chain of
verified constraints is what narrows the landscape by elimination, without search.
"""
from __future__ import annotations

import random

from .certificate import hoeffding_radius


def elimination_fraction(sample, keep) -> float:
    """Fraction of ``sample`` that FAILS ``keep`` (i.e. is eliminated by it)."""
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    kept = sum(1 for v in sample if keep(v))
    return (len(sample) - kept) / len(sample)


def elimination_certificate(sample, keep, delta: float = 0.05) -> dict:
    """Hoeffding interval on the elimination fraction.

    Reuses the same one-sided Hoeffding radius as the verification certificate
    (``docs/verification-formal.md``), applied to a *constraint* over a
    distribution of vacua rather than to a single candidate.
    """
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    p = elimination_fraction(sample, keep)
    r = hoeffding_radius(len(sample), delta)
    return {
        "eliminated": p,
        "lower": max(0.0, p - r),
        "upper": min(1.0, p + r),
        "n": len(sample),
        "delta": delta,
    }


def elimination_curve(values, thresholds) -> list:
    """Empirical CDF: for each threshold t, the fraction of values <= t.

    For a constraint "observable <= t", this is the *survivor* fraction as t
    varies — the elimination curve. Its shape is the distribution's signature:
    linear in |W0|^2 would confirm Denef-Douglas uniform-area distribution.
    """
    values = list(values)
    if not values:
        raise ValueError("values must be non-empty")
    return [sum(1 for v in values if v <= t) / len(values) for t in thresholds]


def joint_elimination(sample, constraints, delta: float = 0.05,
                      permutations: int = 500, seed: int = 0) -> dict:
    """Compose constraints: the fraction eliminated by *at least one*.

    ``constraints`` is an iterable of ``(name, keep)`` pairs. This is the
    "intersection of verified constraints" of ``docs/new-approach.md`` — the
    mechanism that narrows the landscape by elimination, measured as one object:

      - ``per``             — per-constraint elimination fractions, in order;
      - ``joint``           — fraction failing at least one constraint;
      - ``independent``     — what ``joint`` would be if the constraints failed
        independently (``1 - prod(1 - p_i)``);
      - ``interaction``     — ``joint - independent``, the signed departure from
        independence: **negative = redundant** (constraints overlap, so ``joint``
        is *below* the independent-product benchmark), **positive = complementary**
        (they bite disjoint subsets, so ``joint`` is *above* it);
      - ``interaction_z``   — permutation z-score of ``interaction`` against the
        null "the constraints are independent" (each constraint's keep-labels are
        shuffled, preserving the marginals while destroying association);
      - ``interaction_verdict`` — ``independent`` / ``redundant`` / ``complementary``
        at ``|z| >= 2``;
      - ``n_survive_all``   — the raw count of vacua passing every constraint
        (the number whose single-vacuum resolution sets the noise floor);
      - ``certificate``     — the Hoeffding interval on ``joint``.

    The joint fraction is itself a Bernoulli parameter over the sample, so it gets
    the same one-sided Hoeffding radius as a single constraint — the composition
    loses nothing in confidence, only in the breadth of what it rules out. The
    permutation test answers the question the single number cannot: whether an
    apparent non-zero ``interaction`` is structure or one-vacuum noise.
    """
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    named = [(n, k) for n, k in constraints]
    n = len(sample)
    per = []
    keepers = []
    for name, keep in named:
        ks = [keep(v) for v in sample]
        p = sum(1 for k in ks if not k) / n
        per.append({"name": name, "eliminated": p})
        keepers.append(ks)
    passes_all = [all(ks[i] for ks in keepers) for i in range(n)]
    n_survive_all = sum(passes_all)
    joint = 1.0 - n_survive_all / n
    independent = 1.0 - _prod(1.0 - p["eliminated"] for p in per)
    interaction = joint - independent

    # Permutation null on the interaction: shuffle each constraint's keep-labels
    # independently, recompute joint -> interaction. Marginals are preserved,
    # association is destroyed, so this is exactly the independence null.
    rng = random.Random(seed)
    null = []
    for _ in range(permutations):
        shuffled = [rng.sample(ks, len(ks)) for ks in keepers]
        passes = [all(ss[i] for ss in shuffled) for i in range(n)]
        j = 1.0 - sum(passes) / n
        null.append(j - independent)
    mean = sum(null) / len(null)
    var = sum((x - mean) ** 2 for x in null) / len(null)
    std = var ** 0.5
    z = (interaction - mean) / std if std > 0 else 0.0
    verdict = "independent" if abs(z) < 2.0 else ("complementary" if z > 0 else "redundant")

    radius = hoeffding_radius(n, delta)
    return {
        "per": per,
        "joint": joint,
        "independent": independent,
        "interaction": interaction,
        "interaction_z": z,
        "interaction_verdict": verdict,
        "n_survive_all": n_survive_all,
        "n": n,
        "certificate": {
            "eliminated": joint,
            "lower": max(0.0, joint - radius),
            "upper": min(1.0, joint + radius),
            "delta": delta,
        },
    }


def _prod(xs) -> float:
    out = 1.0
    for x in xs:
        out *= x
    return out


def linearity_r2(xs, ys) -> float:
    """R^2 of ys against the best-fit line — 1.0 means perfectly linear."""
    n = len(xs)
    if n < 2 or len(xs) != len(ys):
        raise ValueError("need equal-length inputs of length >= 2")
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx == 0:
        return 0.0
    slope = sxy / sxx
    intercept = my - slope * mx
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
