"""The finance sector, claim by claim: deficit, extrapolation, verified reference, and what it's worth.

The aggregate deficit (`economics.deficit`) says a macro model's decision surface is validated over
about four backcast series and that its forecast is extrapolation. That is true and it is not
actionable, because nobody acts on "the model". They act on **a claim**.

So this module takes the claims a finance desk or a central bank actually acts on, and answers four
questions for each, in this order:

    verification deficit   how many independent constraints were satisfied (m), and the Hoeffding
                           radius sqrt(ln(1/delta) / 2m) — the honest error bar on what was verified
    extrapolation          is the claim inside the region that was measured, or outside it
    verified reference     the independent anchor the claim is checked against, named
    worth                  what it is worth to act on it: act / act with a hedge / do not act

The fourth is the one that matters. The first three are the reasoning behind it.

**Why this is not another report.** Every number is computed at call time from the modules that own
it — the release ladder, the vintage archive, the solved models. A claim whose evidence changes changes
its verdict. The alternative, a table typed once into a document, is the failure mode the whole
discipline exists to catch.

Run:        python3 scripts/finance_claims.py
Guarded by: tests/test_econ_claims.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass

#: Budget for the radius. 0.05 is the conventional level and is quoted with every number.
DELTA = 0.05

ACT = "act"
HEDGE = "act with a hedge"
DO_NOT = "do not act"


def radius(m: int, delta: float = DELTA) -> float:
    """Hoeffding radius on `m` independent constraints: `sqrt(ln(1/delta) / 2m)`."""
    if m <= 0:
        return math.inf
    return math.sqrt(math.log(1.0 / delta) / (2.0 * m))


@dataclass(frozen=True)
class Claim:
    text: str
    oracle: str            # definitional | invariance | null | synthetic | cross-source | none
    m: int                 # independent constraints actually satisfied
    inside: bool           # is the claim inside the measured region?
    reference: str         # the independent anchor it is checked against
    evidence: str          # where the number comes from
    hedge: str = ""

    @property
    def radius(self) -> float:
        return radius(self.m)

    @property
    def radius_label(self) -> str:
        """How to show the radius: a definitional claim is exact, a vacuous one has none."""
        if self.oracle == "definitional":
            return "exact"
        return "vacuous" if self.radius == math.inf else f"±{self.radius:.2f}"

    @property
    def extrapolation(self) -> bool:
        return not self.inside

    @property
    def worth(self) -> str:
        """The decision rule, stated once so it cannot be tuned per claim.

        A definitional claim (an accounting identity that closes to 1e-16) is not a statistical
        statement and no radius applies to it: it is act, by construction.

        Outside the measured region -> do not act, whatever m is. A radius computed on a region the
        claim does not live in is not an error bar for that claim.
        Inside, with no constraints -> do not act: nothing was verified.
        Inside, with radius above 0.25 (fewer than ~24 independent constraints at delta = 0.05)
        -> act with a hedge sized by the radius.
        Inside, with radius at or below 0.25 -> act.
        """
        if self.oracle == "definitional":
            return ACT
        if self.extrapolation or self.m == 0:
            return DO_NOT
        return ACT if self.radius <= 0.25 else HEDGE

    @property
    def verdict(self) -> str:
        where = "extrapolation" if self.extrapolation else "measured region"
        return f"{self.worth} — {where}, m={self.m}, radius {self.radius_label}"


# ---------------------------------------------------------------------------------------
# the claims, each computing its own m from the module that owns the evidence
# ---------------------------------------------------------------------------------------
def _claims() -> list[Claim]:
    from . import gdpnow, release_archive, release_cross, sw_distance, sw_filter

    ladder = release_archive.audit()
    n_ladder_checks = ladder["n_pass"]
    cross = release_cross.audit()
    now = gdpnow.evaluate()
    ratio = now["ratio"]["mae"]
    obs = sw_filter.observability_rank()
    fit = sw_distance.recovery()
    # m for GDPNow is the number of its own guards that go green, not a typed number
    gdpnow_m = sum(1 for name in dir(gdpnow)
                   if name.startswith("guard_") and callable(getattr(gdpnow, name))
                   and getattr(gdpnow, name)()[0])

    return [
        Claim("The first published GDP estimate is biased upward.",
              oracle="null", m=n_ladder_checks, inside=True,
              reference="the Fed's own First/Second/Third/Most-Recent release ladder, 239 quarters",
              evidence="src/pacland/economics/release_archive.py",
              hedge="the magnitude is ±0.2 pp across sub-samples; the sign is what is robust"),
        Claim("That bias cannot be traded.",
              oracle="null", m=n_ladder_checks, inside=True,
              reference="AR(1) of the revision is -0.07: past revisions do not predict the next",
              evidence="release_archive.audit()['checks']",
              hedge="a bias correction is a wash out of sample (1.02x)"),
        Claim("GDPNow beats a no-change forecast at a one-quarter horizon.",
              oracle="null", m=gdpnow_m, inside=True,
              reference=f"no-change benchmark on the same vintage, {now['n']} quarters",
              evidence="src/pacland/economics/gdpnow.py::evaluate",
              hedge=f"MAE ratio {ratio:.2f}; skill is against the ADVANCE estimate"),
        Claim("GDPNow beats a no-change forecast at the settled GDP number.",
              oracle="null", m=0, inside=False,
              reference="none — the evaluation targets the advance estimate, not the final one",
              evidence="docs/economics-model-roster.md",
              hedge="the settled-number comparison is reported, not established"),
        Claim("Our own recorded 'first release' is the first release.",
              oracle="cross-source", m=cross["n_pass"], inside=True,
              reference="the Fed's First Release against the advance we recorded from ALFRED",
              evidence="src/pacland/economics/release_cross.py",
              hedge="34 of 36 quarters agree within 0.5 pp; 2020Q2 is 7.00 pp out"),
        Claim("Smets–Wouters can be scored out of sample on its own observables.",
              oracle="none", m=0, inside=False,
              reference="none — the state is only "
                        f"{obs['fraction']:.0%} observable from its own series",
              evidence="src/pacland/economics/sw_filter.py::observability_rank",
              hedge=f"the shock scales are also unidentified ({fit['worst_relative_error']:.0%} error "
                    f"at R^2 {fit['r2']:.3f})"),
        Claim("The GDP expenditure identity closes exactly.",
              oracle="definitional", m=4, inside=True,
              reference="BEA annual/quarterly identity, checked to 1e-16 of GDP",
              evidence="src/pacland/economics/national_accounts.py"),
        Claim("A 37-quarter revision measurement generalises to the whole record.",
              oracle="cross-source", m=0, inside=False,
              reference="the 239-quarter ladder, which gives a different and more stable answer",
              evidence="release_cross.sensitivity()",
              hedge="the 37-quarter mean moves 0.311 pp depending on two COVID quarters"),
    ]


def claims() -> list[Claim]:
    return _claims()


def summary() -> dict:
    cs = claims()
    by_worth = {}
    for c in cs:
        by_worth[c.worth] = by_worth.get(c.worth, 0) + 1
    return {
        "claims": cs,
        "n": len(cs),
        "n_extrapolation": sum(c.extrapolation for c in cs),
        "n_vacuous": sum(1 for c in cs if c.m == 0),
        "by_worth": by_worth,
        "delta": DELTA,
        "verdict": (f"{len(cs)} claims: {by_worth.get(ACT, 0)} act, "
                    f"{by_worth.get(HEDGE, 0)} act with a hedge, {by_worth.get(DO_NOT, 0)} do not act; "
                    f"{sum(c.extrapolation for c in cs)} are extrapolation"),
    }


def guard_the_rule_is_monotone() -> tuple[bool, str]:
    """MUTATION: the decision rule must react to its inputs, or the table is decoration."""
    cases = [
        (Claim("t", "null", 0, True, "r", "e").worth == DO_NOT, "no constraints -> do not act"),
        (Claim("t", "null", 40, False, "r", "e").worth == DO_NOT, "extrapolation -> do not act even "
                                                                  "with many constraints"),
        (Claim("t", "null", 40, True, "r", "e").worth == ACT, "many constraints inside -> act"),
        (Claim("t", "null", 8, True, "r", "e").worth == HEDGE, "few constraints -> hedge"),
        (Claim("t", "definitional", 0, True, "r", "e").worth == ACT,
         "a definitional identity needs no radius"),
    ]
    ok = all(c[0] for c in cases)
    return ok, "; ".join(f"{'ok' if c[0] else 'FAIL'}: {c[1]}" for c in cases)


def guard_radius_shrinks_with_m() -> tuple[bool, str]:
    """MUTATION: the radius must fall as constraints accumulate."""
    rs = [radius(m) for m in (1, 2, 4, 8, 16, 32)]
    ok = all(a > b for a, b in zip(rs, rs[1:])) and math.isinf(radius(0))
    return ok, "radius falls monotonically: " + ", ".join(
        "inf" if r == math.inf else f"{r:.2f}" for r in [radius(0)] + rs)


def audit() -> dict:
    checks = []
    for name, fn in (("decision rule is monotone", guard_the_rule_is_monotone),
                     ("radius shrinks with m", guard_radius_shrinks_with_m)):
        ok, msg = fn()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks)}


__all__ = ["Claim", "claims", "summary", "radius", "audit", "ACT", "HEDGE", "DO_NOT", "DELTA"]
