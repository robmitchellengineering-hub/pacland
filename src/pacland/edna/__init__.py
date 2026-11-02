"""eDNA detection theory — a methods-only discipline.

**What this is not.** It makes no biological claim: no species is named, no ecosystem is classified, no abundance is asserted
about a real sample. Every number here is a property of a *counting process* — samples, reads, and a contamination rate — and
it would be the same mathematics for any mixture of distinguishable items in a noisy count.

**What it is for.** Environmental-DNA surveys are cheap enough to scale and noisy enough not to be trusted, and the field's
own reviews name the weak points: false positives from contamination, false negatives from low concentration, and reference
databases that are incomplete for most taxa. The missing piece is not another pipeline — it is **the limit**: given N
samples and a sequencing depth D, **how many species can be distinguished, and at what error rate?**

That question is the one this estate has answered three times already, in other media:

    a room      how many modes below f, and how many of them can the measurement resolve
    a chamber   how many modes, how many streams
    a landscape how many structures an observable set identifies

The eDNA version is the same shape: **a counting law, a resolution limit, and a noise floor that decides what counts as a
detection.**

**The directives this discipline holds itself to** (Rob, 2026-11-02):

1. **Methods only.** No biological claim. The deliverable is a limit and its error bar, not a finding about a species.
2. **Enter through the control.** The first artefact is a known-composition synthetic community through the real pipeline —
   `truth_bench.py` for DNA — not a survey.
3. **The falsifier first.** If the field already has a standardised known-composition control with published thresholds, the
   contribution is zero and this discipline should not exist. That pass is recorded in `docs/edna-detection-limit.md`.
"""

from .limit import (
    contamination_floor,
    detection_probability,
    detection_limit_reads,
    distinguishable_species,
    sample_requirement,
)

__all__ = [
    "contamination_floor",
    "detection_probability",
    "detection_limit_reads",
    "distinguishable_species",
    "sample_requirement",
]
