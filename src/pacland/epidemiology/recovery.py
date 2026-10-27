"""The identifiability wall, measured — epidemiology's classes 1, 2 and 4.

Epidemiology's problem is not a shortage of data. It is that the quantity you want (the effect
of an exposure) is entangled with the quantity that decides who gets exposed. So the discipline
is the right place to test whether the oracles method survives its hardest case.

Three checks, each with a seeded fault:

  class 4  a cohort where the true relative risk is KNOWN (we wrote it), with a confounder that
           makes the crude estimate lie. The stratified estimator must recover the truth; the
           crude one must not.
  class 1  persons are conserved: every case is counted in exactly one stratum, and the strata
           rebuild the whole cohort. A table that loses or double-counts a person is refused.
  class 2  the wall itself: with a *homogeneous* effect the adjusted estimate is invariant to how
           finely the population is binned; with a *heterogeneous* one it is not, and the size of
           that movement is the honest uncertainty of an observational estimate.

That third check is why the discipline is hard, and it is the one number a reader should be given
instead of a confidence interval on an estimate whose definition depends on the analyst's binning.

Run:        python3 scripts/epidemiology_identifiability.py
Guarded by: tests/test_epidemiology_identifiability.py
"""
from __future__ import annotations

from dataclasses import dataclass

#: Adjusted estimates must agree across binnings to this relative tolerance when the effect is
#: homogeneous. Real epidemiologic data is never exactly homogeneous, so the tolerance is set by
#: what the arithmetic can achieve on a homogeneous synthetic cohort, not by hope.
INVARIANCE_TOL = 1e-9


@dataclass(frozen=True)
class Stratum:
    """One contingency-table row: exposed and unexposed, cases and totals."""

    exposed_cases: float
    exposed_total: float
    unexposed_cases: float
    unexposed_total: float

    @property
    def exposed_rate(self) -> float:
        return self.exposed_cases / self.exposed_total

    @property
    def unexposed_rate(self) -> float:
        return self.unexposed_cases / self.unexposed_total


def stratum(n: float, exposed_fraction: float, baseline_risk: float, rr: float) -> Stratum:
    """Expected counts for a stratum — exact arithmetic, so recovery can be exact."""
    exposed = n * exposed_fraction
    unexposed = n - exposed
    return Stratum(exposed_cases=exposed * baseline_risk * rr, exposed_total=exposed,
                   unexposed_cases=unexposed * baseline_risk, unexposed_total=unexposed)


def cohort(rr: float = 2.0) -> list[Stratum]:
    """Two strata with different baseline risk AND different exposure: the confounder."""
    return [stratum(n=120_000, exposed_fraction=0.20, baseline_risk=0.010, rr=rr),   # young
            stratum(n=80_000, exposed_fraction=0.80, baseline_risk=0.050, rr=rr)]    # old


def crude_rr(strata: list[Stratum]) -> float:
    cases_e = sum(s.exposed_cases for s in strata)
    total_e = sum(s.exposed_total for s in strata)
    cases_u = sum(s.unexposed_cases for s in strata)
    total_u = sum(s.unexposed_total for s in strata)
    return (cases_e / total_e) / (cases_u / total_u)


def mantel_haenszel_rr(strata: list[Stratum]) -> float:
    """The stratified estimator: weight each stratum's rates by the *unexposed* person-time."""
    num = sum(s.exposed_cases * s.unexposed_total / (s.exposed_total + s.unexposed_total)
              for s in strata)
    den = sum(s.unexposed_cases * s.exposed_total / (s.exposed_total + s.unexposed_total)
              for s in strata)
    return num / den


# ---------------------------------------------------------------------------------------
# class 4 — the truth is known
# ---------------------------------------------------------------------------------------
def recovery(rr: float = 2.0) -> dict:
    strata = cohort(rr)
    crude = crude_rr(strata)
    adjusted = mantel_haenszel_rr(strata)
    return {"truth": rr, "crude": crude, "adjusted": adjusted,
            "crude_bias": crude - rr, "adjusted_bias": adjusted - rr,
            "crude_relative_error": abs(crude - rr) / rr,
            "adjusted_relative_error": abs(adjusted - rr) / rr,
            "pass": abs(adjusted - rr) / rr < INVARIANCE_TOL}


def guard_confounding(rr: float = 2.0) -> tuple[bool, str]:
    """MUTATION: remove the confounder (make both strata share a baseline risk) and the crude
    estimate must become correct — if it does not, the crude bias was coming from somewhere
    else and the demonstration is not showing what it claims."""
    r = recovery(rr)
    flat = [stratum(n=120_000, exposed_fraction=0.20, baseline_risk=0.020, rr=rr),
            stratum(n=80_000, exposed_fraction=0.80, baseline_risk=0.020, rr=rr)]
    crude_flat = crude_rr(flat)
    confounder_removed = abs(crude_flat - rr) / rr < 1e-9
    ok = r["pass"] and confounder_removed and r["crude_relative_error"] > 0.10
    return ok, (f"confounding: truth RR {rr:.2f}, crude {r['crude']:.4f} "
                f"(+{r['crude_relative_error']:.0%} wrong), adjusted {r['adjusted']:.6f}; "
                f"with the baseline risk levelled the crude estimate is right = "
                f"{confounder_removed}")


# ---------------------------------------------------------------------------------------
# class 1 — persons are conserved
# ---------------------------------------------------------------------------------------
def persons_conserved(strata: list[Stratum], total: float | None = None) -> tuple[bool, str]:
    """Every person is in exactly one stratum, and the strata rebuild the cohort."""
    people = sum(s.exposed_total + s.unexposed_total for s in strata)
    cases = sum(s.exposed_cases + s.unexposed_cases for s in strata)
    expected_total = total if total is not None else 200_000.0
    ok = abs(people - expected_total) < 1e-6 and 0.0 < cases < people
    return ok, (f"persons conserved: {people:,.0f} in strata vs cohort {expected_total:,.0f}; "
                f"cases {cases:,.1f} is a fraction of them")


def guard_conservation() -> tuple[bool, str]:
    """MUTATION: double-count one stratum and the conservation check must refuse it."""
    strata = cohort()
    ok_honest, msg = persons_conserved(strata)
    doubled = strata + [strata[0]]
    ok_doubled, _ = persons_conserved(doubled)
    ok = ok_honest and not ok_doubled
    return ok, f"{msg}; a table that repeats a stratum is refused = {not ok_doubled}"


# ---------------------------------------------------------------------------------------
# class 2 — the wall: does the answer depend on the binning?
# ---------------------------------------------------------------------------------------
def _split(s: Stratum, share: float, effect_ratio: float) -> list[Stratum]:
    """Split one stratum into two whose *effects* differ by `effect_ratio`.

    Baseline risk is held equal across the halves, so the only thing the finer binning reveals
    is effect modification: the first half carries relative risk RR, the second RR*effect_ratio.
    """
    first = Stratum(exposed_cases=s.exposed_cases * share,
                    exposed_total=s.exposed_total * share,
                    unexposed_cases=s.unexposed_cases * share,
                    unexposed_total=s.unexposed_total * share)
    rest = 1.0 - share
    second = Stratum(exposed_cases=s.exposed_cases * rest * effect_ratio,
                     exposed_total=s.exposed_total * rest,
                     unexposed_cases=s.unexposed_cases * rest,
                     unexposed_total=s.unexposed_total * rest)
    return [first, second]


def binning_invariance(rr: float = 2.0, heterogeneity: float = 1.0) -> dict:
    """Re-bin the population more finely and see whether the adjusted estimate moves.

    ``heterogeneity = 1.0`` means the effect and the baseline risk are the same everywhere, so
    the estimate must not move. Above that, the finer binning reveals real effect modification —
    a genuine difference, not an artefact — which is why no single adjusted number is *the*
    answer.
    """
    base = cohort(rr)
    fine = []
    for s in base:
        fine.extend(_split(s, 0.5, heterogeneity))
    coarse_est = mantel_haenszel_rr(base)
    fine_est = mantel_haenszel_rr(fine)
    drift = abs(fine_est - coarse_est) / coarse_est
    return {"coarse": coarse_est, "fine": fine_est, "drift": drift,
            "heterogeneity": heterogeneity,
            "invariant": drift < INVARIANCE_TOL,
            "pass": (drift < INVARIANCE_TOL) if heterogeneity == 1.0 else (drift > 0.01)}


def guard_binning() -> tuple[bool, str]:
    """MUTATION: with a homogeneous effect the estimate must be invariant (drift ~ 0); with a
    heterogeneous one it must move. Both directions are tested, because a check that passes on
    one and cannot fail on the other is not measuring binning at all."""
    flat = binning_invariance(heterogeneity=1.0)
    skewed = binning_invariance(heterogeneity=2.0)
    ok = flat["invariant"] and not skewed["invariant"]
    return ok, (f"binning: homogeneous drift {flat['drift']:.1e} (invariant), "
                f"heterogeneous drift {skewed['drift']:.3f} (moves) — the wall is "
                f"{skewed['drift']:.1%} of the estimate")


# ---------------------------------------------------------------------------------------
def audit() -> dict:
    checks = []
    for name, run in (("class 4 confounding", guard_confounding),
                      ("class 1 conservation", guard_conservation),
                      ("class 2 binning", guard_binning)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["Stratum", "stratum", "cohort", "crude_rr", "mantel_haenszel_rr", "recovery",
           "persons_conserved", "binning_invariance", "guard_confounding",
           "guard_conservation", "guard_binning", "audit", "INVARIANCE_TOL"]
