"""Why a cell is undecided — the column that makes an all-UNKNOWN table worth reading.

The verdict answers *what we know* (`KILLED` / `SURVIVES` / `UNKNOWN`). It does not answer **why not**,
and after SX-0 most cells are `UNKNOWN` because the derivations have not been run. A table of 78 blank
cells is a wall; a table that says *which kind* of blank each one is turns the wall into a map.

The classes are deliberately different in kind, because they imply different work:

    COMPUTED-HERE        an in-repo computation decides it            -> nothing to do
    COMPUTED-ELSEWHERE   a published computation decides it           -> read the paper, score the cell
    CONTESTED            the framework's literature disputes it       -> the cell cannot be scored today
    NOT-ESTABLISHED      the framework's own open problem, unsolved   -> a research programme, not a task
    NO-PREDICTION        the framework makes no such prediction       -> the condition does not apply
    NOT-RESEARCHED       nobody has entered a citation yet            -> **a task list, not a finding**

`NOT-RESEARCHED` exists to keep the last two honest. "We looked and the field has no answer" and "we
have not looked" must never share a cell value, or the table becomes an excuse.

Every entry below was read from the paper's own abstract (title + summary via the arXiv API) or computed
in this repository. An entry with no source is `NOT-RESEARCHED` — the constructor refuses one without.
"""
from __future__ import annotations

COMPUTED_HERE = "COMPUTED-HERE"
COMPUTED_ELSEWHERE = "COMPUTED-ELSEWHERE"
CONTESTED = "CONTESTED"
NOT_ESTABLISHED = "NOT-ESTABLISHED"
NO_PREDICTION = "NO-PREDICTION"
NOT_RESEARCHED = "NOT-RESEARCHED"

REASON_CLASSES = (
    COMPUTED_HERE,
    COMPUTED_ELSEWHERE,
    CONTESTED,
    NOT_ESTABLISHED,
    NO_PREDICTION,
    NOT_RESEARCHED,
)

# The work a class implies. Rendered beside the counts so the table says what to do next.
WORK = {
    COMPUTED_HERE: "nothing to do",
    COMPUTED_ELSEWHERE: "read the paper and score the cell",
    CONTESTED: "cannot be scored until the dispute resolves",
    NOT_ESTABLISHED: "a research programme, not a task",
    NO_PREDICTION: "the condition does not apply to this framework",
    NOT_RESEARCHED: "a task list - nobody has looked yet",
}


class Note:
    """One cell's evidence: which class, what it shows, and where it was read."""

    def __init__(self, reason_class: str, note: str, source: str = "") -> None:
        if reason_class not in REASON_CLASSES:
            raise ValueError(f"unknown reason class {reason_class!r}")
        if reason_class != NOT_RESEARCHED and not source:
            raise ValueError(f"{reason_class} needs a source; an unsourced note is NOT-RESEARCHED")
        if reason_class == NOT_RESEARCHED and source:
            raise ValueError("NOT-RESEARCHED cannot carry a source")
        self.reason_class = reason_class
        self.note = note
        self.source = source


EVIDENCE: dict[tuple[str, str], Note] = {
    ("lqg-spinfoam", "C12"): Note(
        CONTESTED,
        "the large-spin asymptotics of the new spin-foam models recover the Regge action, and vertex "
        "amplitudes exist with 'the correct semiclassical limit' - an asymptotic result, not the full "
        "general-relativity limit",
        "arXiv:1010.4886, arXiv:1201.2187, arXiv:1104.1384",
    ),
    ("asymptotic-safety", "C3"): Note(
        CONTESTED,
        "momentum-dependent field redefinitions are used to bring the graviton propagator into a "
        "ghost-free form, while a 2026 paper claims BRST-symmetry violation and 'fundamental "
        "limitations' of the program. Both sides are live",
        "arXiv:2311.12097, arXiv:2601.08886",
    ),
    ("causal-sets", "C2"): Note(
        CONTESTED,
        "Lorentz invariance is claimed to follow from the specific implementation (Poisson sprinkling), "
        "against the 'discreteness violates LI' misconception - but locality in a manifold-like causal "
        "set is still being defined",
        "arXiv:1309.3403, arXiv:1903.11544",
    ),
    ("lqg-spinfoam", "C1"): Note(
        CONTESTED,
        "perturbations of a spin-foam model on a flat background give LINEARISED gravity - not the "
        "Newtonian / post-Newtonian limit that C1's bound constrains",
        "arXiv:1812.02110",
    ),
    ("causal-sets", "C6"): Note(
        CONTESTED,
        "causal set theory predicts an 'everpresent Lambda' - a fluctuating, time-dependent "
        "cosmological constant of the right order of magnitude. It is the only one of the six with a "
        "prediction for the MAGNITUDE, and the prediction is strongly constrained by microwave-background "
        "isotropy (though not excluded)",
        "arXiv:astro-ph/0209274, arXiv:1210.2589, arXiv:gr-qc/0612128",
    ),
    ("asymptotic-safety", "C6"): Note(
        CONTESTED,
        "the FRG claim is that graviton fluctuations drive the cosmological constant towards zero, which "
        "solves the problem by predicting Lambda = 0 - so the observed Lambda > 0 is a tension rather "
        "than a success",
        "arXiv:1704.08040, arXiv:1501.05848",
    ),
    ("strings-adscft", "C11"): Note(
        COMPUTED_HERE,
        "in the T^6 model the distance conjecture (alpha = 1) and the WGC (z = 1) hold exactly and there "
        "is no de Sitter vacuum within the script's stated scope; the cell stays UNKNOWN because the "
        "predicate is about the framework, and the KKLT question is outside that scope",
        "scripts/validate_t6.py (21/21), scripts/validate_t6_sympy.py (8/8), scripts/no_ds_t6.py",
    ),
}


def note_for(candidate: str, constraint: str) -> Note:
    return EVIDENCE.get((candidate, constraint), Note(NOT_RESEARCHED, "no citation entered yet"))


def class_for(candidate: str, constraint: str) -> str:
    return note_for(candidate, constraint).reason_class


def counts() -> dict[str, int]:
    """How many cells of the table sit in each class."""
    from .lattice import CANDIDATES, CONSTRAINTS

    out = {c: 0 for c in REASON_CLASSES}
    for cand in CANDIDATES:
        for con in CONSTRAINTS:
            out[class_for(cand.id, con.id)] += 1
    return out
