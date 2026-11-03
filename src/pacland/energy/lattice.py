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

**Nothing here has been run.** Every ``verified_on`` is ``None`` on purpose: the bounds are named but
not yet read from their primary sources, so every cell is ``UNKNOWN``. Filling them is the first task,
and the schema refuses to let a filled lattice skip it.
"""
from __future__ import annotations

from dataclasses import dataclass

# The machine classes are imported vocabulary, not invented: pacland.swampland classifies every
# conjecture the same three ways, and this module speaks it unchanged.
TESTABLE_NOW = "TESTABLE-NOW"
NEEDS_BIGGER_MACHINE = "NEEDS-BIGGER-MACHINE"
NOT_TESTABLE_IN_TRUNCATION = "NOT-TESTABLE-IN-TRUNCATION"
MACHINES = (TESTABLE_NOW, NEEDS_BIGGER_MACHINE, NOT_TESTABLE_IN_TRUNCATION)

DERIVATION, OBSERVATION, ARGUMENT = "derivation", "observation", "argument"
EVIDENCE_CLASSES = (DERIVATION, OBSERVATION, ARGUMENT)

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
        # A verified bound with no source is an unverified bound wearing a date.
        if self.verified_on and not self.source:
            raise ValueError(f"{self.id}: verified_on set without a primary source")


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
        bound="G_N measured; post-Newtonian gamma = 1 to solar-system precision",
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
        bound="S = A/4G_N (semiclassical)",
    ),
    Constraint(
        "C6", "cosmological-constant-account",
        "The candidate predicts, or explicitly accounts for, the smallness of Lambda/M_Pl^4, or states "
        "plainly that it has no account of it.",
        "a candidate that neither predicts the ratio nor admits it has no account of it",
        ARGUMENT, NOT_TESTABLE_IN_TRUNCATION,
        bound="Lambda_obs / M_Pl^4 ~ 1e-122",
        fails_as=UNKNOWN,
        note="failing this is UNKNOWN, not KILLED; passing it by tuning is recorded as tuning",
    ),
    Constraint(
        "C7", "lorentz-violation-bound",
        "Any Planck-scale modification of the dispersion relation predicts a time-of-flight or "
        "birefringence effect smaller than the observed bounds.",
        "an energy-dependent time of flight larger than the observed bound",
        OBSERVATION, TESTABLE_NOW,
        bound="no Lorentz-invariance violation observed at the Planck scale",
    ),
    Constraint(
        "C8", "gravitational-wave-speed",
        "Gravitational waves propagate at c to the precision measured by multimessenger events.",
        "a speed differing from c by more than the multimessenger bound",
        OBSERVATION, TESTABLE_NOW,
        bound="|v_gw/c - 1| at the GW170817-class precision",
    ),
    Constraint(
        "C9", "fifth-force-equivalence-principle",
        "Any new light scalar is screened, or its coupling is below the equivalence-principle and "
        "solar-system bounds.",
        "an unscreened fifth force above the equivalence-principle bound",
        OBSERVATION, TESTABLE_NOW,
        bound="equivalence-principle, Cassini and MICROSCOPE classes",
    ),
    Constraint(
        "C10", "strong-field-consistency",
        "Predicted black-hole shadow size and ringdown frequencies lie inside the measured intervals.",
        "a shadow or ringdown prediction outside the measured interval",
        OBSERVATION, NEEDS_BIGGER_MACHINE,
        bound="EHT shadow; LIGO-Virgo ringdown",
        note="few-percent data today; order-one deviations are already excluded",
    ),
    Constraint(
        "C11", "swampland-consistency",
        "If the candidate claims a string ultraviolet completion, the de Sitter, distance and "
        "weak-gravity conditions hold, with slack or tightness stated exactly rather than as "
        "'of order one'.",
        "a string-derived candidate that violates a swampland condition in a controlled example",
        DERIVATION, TESTABLE_NOW,
        bound="T^6 exact oracle: alpha = 1.0000, z = 1.0000 — the bounds are saturated, not slack",
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
        bound="spectral index, running, and tensor-to-scalar ratio bounds",
    ),
)

# A stage-2 condition is only asked of candidates that claim a string completion.
STAGE_TWO_ONLY = {"C11": "claims_string_completion"}


def verdict(constraint: Constraint, evidence: Evidence | None) -> tuple[str, str]:
    """One cell of the table.

    The ordering *is* the discipline:
      1. a verifier that ran and failed   -> the candidate's own failure verdict
      2. a verifier that ran and passed   -> SURVIVES
      3. no verifier, or no verified bound -> UNKNOWN
    """
    if evidence is None:
        if not constraint.verified_on:
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
                    "machine": con.machine,
                })
                continue
            v, why = verdict(con, evidence.get((cand.id, con.id)))
            rows.append({
                "candidate": cand.id, "constraint": con.id, "name": con.name,
                "verdict": v, "reason": why, "machine": con.machine,
            })
    return rows
