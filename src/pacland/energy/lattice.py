"""The SEXTANT lattice — six candidate frameworks, thirteen conditions, one verdict per cell.

**Why a lattice and not a theory.** Graviton perturbation theory is non-renormalisable
(``[G_N] = -2``), so infinitely many ultraviolet completions reduce to Einstein gravity below the
Planck scale. That is not a gap in the literature; it is a degeneracy, and it is why no experiment has
discriminated between frameworks: below the Planck scale they are *all* general relativity. The only
discriminating information is (a) an observable where a completion must deviate, or (b) a condition a
framework must satisfy and does not. The field checks (b) one framework at a time, in its own
community, and never jointly. This module is the joint check.

**The verdict alphabet, and the one rule that matters.**

    KILLED    a verifier ran and the candidate provably fails the predicate
    SURVIVES  a verifier ran and the candidate satisfies it as far as the evidence goes
    UNKNOWN   no verifier has run against a verified bound

There is deliberately no path from "nothing found" to ``SURVIVES``. A cell with no evidence is
``UNKNOWN``, and the whole table is allowed to be ``UNKNOWN`` — that is the honest reading of the
field today, and reporting it as a pass would be the exact failure this repository exists to prevent.

**Oracle class.** Every condition names the class of its evidence — ``derivation`` (a computation),
``observation`` (a measurement), or ``argument`` (no oracle). A condition with no oracle is
``NOT-TESTABLE-IN-TRUNCATION`` and says so, in the vocabulary of ``pacland.swampland``.

**SX-0 is partly done (2026-11-03).** Four observational bounds have been read from their own primary
sources — GW170817's speed of gravity, Fermi's GRB 090510 dispersion limit, the EHT's M87* shadow
diameter, and BICEP/Keck's tensor-to-scalar ratio — and carry ``verified_on``. Three measured
constraints do not, and are named in ``PENDING_BOUNDS`` rather than left silently blank. Every verdict
is still ``UNKNOWN``: a verified bound is what makes a condition *evaluable*, not what decides it.
"""
from __future__ import annotations

from dataclasses import dataclass

from .evidence import class_for

# The machine classes are imported vocabulary, not invented: pacland.swampland classifies every
# conjecture the same three ways, and this module speaks it unchanged.
TESTABLE_NOW = "TESTABLE-NOW"
NEEDS_BIGGER_MACHINE = "NEEDS-BIGGER-MACHINE"
NOT_TESTABLE_IN_TRUNCATION = "NOT-TESTABLE-IN-TRUNCATION"
MACHINES = (TESTABLE_NOW, NEEDS_BIGGER_MACHINE, NOT_TESTABLE_IN_TRUNCATION)

DERIVATION, OBSERVATION, ARGUMENT = "derivation", "observation", "argument"
EVIDENCE_CLASSES = (DERIVATION, OBSERVATION, ARGUMENT)

# What kind of thing the `bound` field holds. SX-0 found one field doing three jobs, and
# "every constraint has a bound" is therefore a gate that cannot be met honestly:
#   measured   an external measurement — this is what "verify the bound" means
#   theorem    a proven result (S = A/4G, the T^6 saturation) — verified by the proof, not a reading
#   procedure  a derivation condition with no number at all (unitarity, degrees of freedom)
MEASURED, THEOREM, PROCEDURE = "measured", "theorem", "procedure"
BOUND_KINDS = (MEASURED, THEOREM, PROCEDURE)

KILLED, SURVIVES, UNKNOWN = "KILLED", "SURVIVES", "UNKNOWN"
VERDICTS = (KILLED, SURVIVES, UNKNOWN)


@dataclass(frozen=True)
class Candidate:
    """A named framework that claims to complete gravity at short distances."""

    id: str
    name: str
    claims_string_completion: bool = False  # C11 (swampland) applies only when true
    note: str = ""


@dataclass(frozen=True)
class Constraint:
    """A condition every candidate must satisfy, with the observation that would break it."""

    id: str
    name: str
    predicate: str
    falsifier: str
    evidence_class: str
    machine: str
    bound: str | None = None       # the measured quantity, named
    bound_kind: str = PROCEDURE    # measured | theorem | procedure — see BOUND_KINDS
    source: str | None = None      # primary result — required before verified_on may be set
    verified_on: str | None = None  # None = the bound has not been read from its source
    fails_as: str = KILLED
    note: str = ""

    def __post_init__(self) -> None:
        if self.evidence_class not in EVIDENCE_CLASSES:
            raise ValueError(f"{self.id}: unknown evidence class {self.evidence_class!r}")
        if self.machine not in MACHINES:
            raise ValueError(f"{self.id}: unknown machine class {self.machine!r}")
        if self.fails_as not in VERDICTS:
            raise ValueError(f"{self.id}: unknown verdict {self.fails_as!r}")
        if self.bound_kind not in BOUND_KINDS:
            raise ValueError(f"{self.id}: unknown bound kind {self.bound_kind!r}")
        # A verified bound with no source is an unverified bound wearing a date.
        if self.verified_on and not self.source:
            raise ValueError(f"{self.id}: verified_on set without a primary source")
        # A procedure is not a bound; claiming to have verified one is a category error.
        if self.verified_on and self.bound_kind == PROCEDURE:
            raise ValueError(f"{self.id}: a procedure has no bound to verify")


@dataclass(frozen=True)
class Evidence:
    """What a verifier produced for one (candidate, constraint) pair."""

    passed: bool
    reason: str
    source: str = ""


CANDIDATES: tuple[Candidate, ...] = (
    Candidate("strings-adscft", "String theory / AdS-CFT", claims_string_completion=True),
    Candidate("lqg-spinfoam", "Loop quantum gravity / spin foams"),
    Candidate("asymptotic-safety", "Asymptotic safety (functional renormalisation group)"),
    Candidate("cdt", "Causal dynamical triangulations"),
    Candidate("causal-sets", "Causal sets"),
    Candidate("gft", "Group field theory / tensorial models"),
)

CONSTRAINTS: tuple[Constraint, ...] = (
    Constraint(
        "C1", "low-energy-limit",
        "In the limit E << M_Pl the candidate reduces to Einstein-Hilbert gravity with the measured "
        "Newton constant, giving the Newtonian 1/r potential and the observed light bending.",
        "a computed long-distance limit that differs from general relativity at solar-system scales",
        DERIVATION, TESTABLE_NOW,
        bound="post-Newtonian gamma - 1 to solar-system precision (Cassini-class)",
        bound_kind=MEASURED,
    ),
    Constraint(
        "C2", "diffeomorphism-recovery",
        "Either diffeomorphism invariance is preserved, or the candidate states what replaces it and "
        "exhibits the mechanism by which it emerges as an effective long-distance symmetry.",
        "a discrete or foliated candidate with no stated recovery mechanism",
        DERIVATION, TESTABLE_NOW,
        note="the condition most often asserted and least often exhibited",
    ),
    Constraint(
        "C3", "unitarity-no-ghost",
        "The physical spectrum contains no propagating ghost, or a stated Lee-Wick / PT-symmetric "
        "resolution is given together with a proof that the S-matrix is unitary.",
        "a propagating ghost in the physical spectrum",
        DERIVATION, TESTABLE_NOW,
        note="positive control: Stelle quadratic gravity must be KILLED here",
    ),
    Constraint(
        "C4", "graviton-degrees-of-freedom",
        "The massless graviton carries exactly two physical polarisations, or the extra modes are "
        "shown to be screened below the stated scale.",
        "a third propagating polarisation below the screening scale",
        DERIVATION, TESTABLE_NOW,
    ),
    Constraint(
        "C5", "bekenstein-hawking-coefficient",
        "Black-hole entropy is recovered as S = A/4G with coefficient 1 — not 1/2, not 4, and not a "
        "free normalisation fitted to the answer.",
        "an entropy-area coefficient other than 1 with no stated correction",
        DERIVATION, TESTABLE_NOW,
        bound="S = A/4G_N (semiclassical theorem)",
        bound_kind=THEOREM,
    ),
    Constraint(
        "C6", "cosmological-constant-account",
        "The candidate predicts, or explicitly accounts for, the smallness of the vacuum energy — "
        "rho_Lambda/M_Pl^4 ~ 1e-123, equivalently Lambda/M_Pl^2 ~ 1e-122 — or states plainly that it "
        "has no account of it.",
        "a candidate that neither predicts the ratio nor admits it has no account of it",
        ARGUMENT, NOT_TESTABLE_IN_TRUNCATION,
        bound="rho_Lambda/M_Pl^4 = 1.1e-123; Lambda/M_Pl^2 = 2.9e-122 (computed, see energy.vacuum)",
        bound_kind=MEASURED,
        source="arXiv:1807.06209, A&A 641:A6 (2020) - H_0 = 67.4 +/- 0.5, Omega_m = 0.315 +/- 0.007, "
               "read from the abstract; the ratio is arithmetic on those in pacland.energy.vacuum",
        verified_on="2026-11-03",
        fails_as=UNKNOWN,
        note="failing this is UNKNOWN, not KILLED; passing it by tuning is recorded as tuning. The v0 "
             "text said 'Lambda/M_Pl^4', which is dimensionally wrong — see energy.vacuum",
    ),
    Constraint(
        "C7", "lorentz-violation-bound",
        "Any Planck-scale modification of the dispersion relation predicts a time-of-flight or "
        "birefringence effect smaller than the observed bounds.",
        "an energy-dependent time of flight larger than the observed bound",
        OBSERVATION, TESTABLE_NOW,
        bound="linear LIV: the quantum-gravity mass scale is significantly above M_Pl",
        bound_kind=MEASURED,
        source="arXiv:0908.1832, Nature 462:331 (2009) - abstract: a 31 GeV photon from GRB 090510 sets "
               "a linear-dispersion limit 'requiring for the first time a quantum-gravity mass scale "
               "significantly above the Planck mass'",
        verified_on="2026-11-03",
        note="the exact coefficient (the often-quoted 1.2 M_Pl) is NOT in the abstract and is not "
             "asserted here; read the paper before quoting a number",
    ),
    Constraint(
        "C8", "gravitational-wave-speed",
        "Gravitational waves propagate at c to the precision measured by multimessenger events.",
        "a speed differing from c by more than the multimessenger bound",
        OBSERVATION, TESTABLE_NOW,
        bound="-3e-15 <= (v_gw - c)/c <= +7e-16",
        bound_kind=MEASURED,
        source="arXiv:1710.05834, ApJL 848:L13 (2017) - abstract, from the +1.74 +/- 0.05 s delay of "
               "GRB 170817A behind GW170817",
        verified_on="2026-11-03",
    ),
    Constraint(
        "C9", "fifth-force-equivalence-principle",
        "Any new light scalar is screened, or its coupling is below the equivalence-principle and "
        "solar-system bounds.",
        "an unscreened fifth force above the equivalence-principle bound",
        OBSERVATION, TESTABLE_NOW,
        bound="eta(Ti,Pt) = [-1.5 +/- 2.3 (stat) +/- 1.5 (syst)]e-15 at 1 sigma",
        bound_kind=MEASURED,
        source="arXiv:2209.15487, PRL 129:121102 (2022) - abstract",
        verified_on="2026-11-03",
        note="the MICROSCOPE Eotvos parameter is verified; the solar-system half overlaps C1, which is "
             "still unread, so this verifies the laboratory half only",
    ),
    Constraint(
        "C10", "strong-field-consistency",
        "Predicted black-hole shadow size and ringdown frequencies lie inside the measured intervals.",
        "a shadow or ringdown prediction outside the measured interval",
        OBSERVATION, NEEDS_BIGGER_MACHINE,
        bound="M87* shadow diameter 42 +/- 3 micro-as",
        bound_kind=MEASURED,
        source="arXiv:1906.11238, ApJ 875:L1 (2019) - abstract",
        verified_on="2026-11-03",
        note="the shadow half is verified; the ringdown half of this condition is NOT, and is not "
             "claimed until a ringdown bound is read from its own source",
    ),
    Constraint(
        "C11", "swampland-consistency",
        "If the candidate claims a string ultraviolet completion, the de Sitter, distance and "
        "weak-gravity conditions hold, with slack or tightness stated exactly rather than as "
        "'of order one'.",
        "a string-derived candidate that violates a swampland condition in a controlled example",
        DERIVATION, TESTABLE_NOW,
        bound="T^6 exact oracle: alpha = 1.0000, z = 1.0000 — the bounds are saturated, not slack",
        bound_kind=THEOREM,
        note="applies only to candidates with claims_string_completion; the T^6 result is the control",
    ),
    Constraint(
        "C12", "semiclassical-limit-exists",
        "The framework's own defining equations possess a solution whose semiclassical expansion is "
        "general relativity — not merely a claim that such a solution should exist.",
        "a framework whose defining amplitude has no semiclassical limit",
        DERIVATION, NEEDS_BIGGER_MACHINE,
        note="the standing open problem for spin foams, and the condition most often assumed",
    ),
    Constraint(
        "C13", "cosmological-perturbations",
        "If the candidate makes early-universe predictions, they lie inside the measured bounds on the "
        "spectral index, its running, and the tensor-to-scalar ratio.",
        "a prediction outside the measured inflationary bounds",
        OBSERVATION, NEEDS_BIGGER_MACHINE,
        bound="r_0.05 < 0.036 at 95% confidence",
        bound_kind=MEASURED,
        source="arXiv:2110.00483, PRL 127:151301 (2021) - abstract",
        verified_on="2026-11-03",
        note="the tensor-to-scalar half is verified; the spectral-index and running halves are NOT, "
             "and are not claimed until read from Planck's own parameter paper",
    ),
)

# A stage-2 condition is only asked of candidates that claim a string completion.
STAGE_TWO_ONLY = {"C11": "claims_string_completion"}


def verdict(constraint: Constraint, evidence: Evidence | None) -> tuple[str, str]:
    """One cell of the table.

    The ordering *is* the discipline:
      1. a verifier that ran and failed   -> the candidate's own failure verdict
      2. a verifier that ran and passed   -> SURVIVES
      3. no verifier                      -> UNKNOWN, and *why* matters:
           a measured bound that was never read is a missing number;
           a procedure that was never run is a missing derivation.
         Conflating the two would say "we are missing a measurement" about unitarity, which is
         nonsense — SX-0 found exactly that conflation in the reason string.
    """
    if evidence is None:
        if constraint.bound_kind == MEASURED and not constraint.verified_on:
            return UNKNOWN, "bound not verified from a primary source"
        return UNKNOWN, "no evaluator wired for this predicate"
    if not evidence.passed:
        return constraint.fails_as, evidence.reason
    return SURVIVES, evidence.reason


def table(evidence: dict[tuple[str, str], Evidence] | None = None) -> list[dict]:
    """The full candidate x constraint table, one row per cell."""
    evidence = evidence or {}
    rows: list[dict] = []
    for cand in CANDIDATES:
        for con in CONSTRAINTS:
            # a string-only condition is not a failing condition for a non-string candidate
            gate = STAGE_TWO_ONLY.get(con.id)
            if gate and not getattr(cand, gate):
                rows.append({
                    "candidate": cand.id, "constraint": con.id, "name": con.name,
                    "verdict": UNKNOWN, "reason": "does not claim a string completion - condition not asked",
                    "machine": con.machine, "reason_class": class_for(cand.id, con.id),
                })
                continue
            v, why = verdict(con, evidence.get((cand.id, con.id)))
            rows.append({
                "candidate": cand.id, "constraint": con.id, "name": con.name,
                "verdict": v, "reason": why, "machine": con.machine,
                "reason_class": class_for(cand.id, con.id),
            })
    return rows


# --------------------------------------------------------------------------------------------
# SX-0: the bounds, and the gap.
# --------------------------------------------------------------------------------------------

# Every `measured` constraint whose bound has NOT been read from its primary source. This list is
# the honest gap, and it is named so it cannot be forgotten: a test asserts that it is exactly the
# set of measured constraints lacking `verified_on`. Fill one and the test demands you delete it
# from here — a bound cannot be quietly upgraded.
#
#   C1  Cassini's post-Newtonian gamma: Nature 425, 374 (2003). Two routes were tried and both
#       refused the abstract — nature.com redirects to a paywall, and the Semantic Scholar API
#       returns "abstract": null with the publisher's elision notice. The bound is quoted
#       everywhere second-hand; quoting it without reading the paper is what this gate prevents.
PENDING_BOUNDS: frozenset[str] = frozenset({"C1"})


def measured_constraints() -> tuple[Constraint, ...]:
    return tuple(c for c in CONSTRAINTS if c.bound_kind == MEASURED)


def unverified_measured() -> tuple[str, ...]:
    """The measured constraints that still have no source-read bound."""
    return tuple(c.id for c in measured_constraints() if not c.verified_on)


def verified_bounds() -> dict[str, dict]:
    """The bounds that have actually been read, with the source they were read from."""
    return {
        c.id: {"bound": c.bound, "source": c.source, "verified_on": c.verified_on}
        for c in CONSTRAINTS
        if c.verified_on
    }
