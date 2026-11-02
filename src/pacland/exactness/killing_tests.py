"""H-E: are the survivors the ones a test could have killed?

The hypothesis, from cross-referencing the enumeration objection with the arithmetic null: **the results that survived
are the ones that were written so they could fail.**

The audit is two columns, recorded independently:

    FALSIFIER STATED AT PUBLICATION?   was a specific observation named that would have killed it, at the time it
                                       was claimed?
    CURRENT STATUS                     survives / demoted

and it separates two kinds of record, because conflating them is what makes the pattern look either stronger or weaker
than it is:

    RESULTS       things claimed as achievements; demotion is the failure mode
    HYPOTHESES    things proposed in order to be killed; a clean refutation is the SUCCESS mode

**What the audit found.** Among RESULTS, every demotion is a result published without a stated falsifier, and every
survivor had one. Among HYPOTHESES the pattern is the opposite of a failure: H-C stated its falsifier and died cleanly
in one run, which is the system working rather than failing.

So the honest form of H-E is narrower than "survivors are the killable ones":

    a RESULT published without a stated falsifier is the one that later gets demoted;
    a HYPOTHESIS with a stated falsifier gets a verdict either way, and both verdicts are useful.

Run:        python3 scripts/killing_tests.py
Guarded by: tests/test_killing_tests.py
"""
from __future__ import annotations

#: (record, kind, falsifier stated at publication, status now, what kind of test could kill it)
REGISTER = (
    ("max |N| = b3", "RESULT", True, "survives", "one pair with |N| > b3, or a missed attaining pair"),
    ("count(N) = [x^N] P(x)^(b3/2)", "RESULT", True, "survives", "one tadpole class whose count disagrees"),
    ("measure dimension = b3", "RESULT", True, "survives", "one invariant identifying two distinct |N| classes"),
    ("zeta zeros to 6.4e-13", "RESULT", True, "survives", "disagreement with the literature values"),
    ("A = 8.554 per unit b3", "RESULT", False, "demoted", "recompute at a wider window and see it move"),
    ("the accessibility minimum at b3 = 12", "RESULT", False, "demoted", "raise the work budget and re-measure"),
    ("measure-invariance = observability", "RESULT", False, "demoted", "find an invariant result that is not exact"),
    ("H-C: every exact quantity has a rational GF", "HYPOTHESIS", True, "refuted", "no low-order out-of-sample recurrence"),
    ("H-A: the exponential is combinatorial", "HYPOTHESIS", True, "supported", "a scaling faster than a polynomial power"),
    ("H-B: invariance equals exactness", "HYPOTHESIS", True, "refuted", "an invariant-but-inexact statistic"),
)


def results() -> list:
    return [r for r in REGISTER if r[1] == "RESULT"]


def hypotheses() -> list:
    return [r for r in REGISTER if r[1] == "HYPOTHESIS"]


def audit() -> dict:
    demoted = [r[0] for r in results() if r[3] == "demoted"]
    survived = [r[0] for r in results() if r[3] == "survives"]
    demoted_with_falsifier = [r[0] for r in results() if r[3] == "demoted" and r[2]]
    survived_without = [r[0] for r in results() if r[3] == "survives" and not r[2]]
    hyp_with = [r[0] for r in hypotheses() if r[2]]
    hyp_verdicts = {r[0]: r[3] for r in hypotheses()}
    pattern_holds = not demoted_with_falsifier and not survived_without
    return {
        "results": len(results()), "hypotheses": len(hypotheses()),
        "demoted": demoted, "survived": survived,
        "demoted_with_a_stated_falsifier": demoted_with_falsifier,
        "survived_without_one": survived_without,
        "hypotheses_with_a_stated_falsifier": len(hyp_with),
        "hypothesis_verdicts": hyp_verdicts,
        "pattern_holds": pattern_holds,
        "verdict": ("H-E SUPPORTED, in its narrow form: among results, every demotion lacked a stated falsifier at "
                    "publication and every survivor had one. Among hypotheses every entry states a falsifier, and all "
                    "of them reached a verdict — two refuted, one supported."
                    if pattern_holds else
                    "H-E FAILS: a demoted result had a stated falsifier, or a survivor had none"),
    }


__all__ = ["REGISTER", "results", "hypotheses", "audit"]
