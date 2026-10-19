# Rule of Three on the Standard-Model results

Each SM exact result was one confirmation (sympy). The Rule of Three requires three
independent confirmations that agree. This note records the three arms for the two
headline SM results (the "19" was already three-way checked by the rank test — Jacobian
rank + orbit-dimension formula + Bento–Silva–Trautner).

## 1. Anomaly cancellation — three arms agree (5/5)

| arm | method | result |
|---|---|---|
| 1 — exact | `scripts/validate_sm_anomaly.py` (Python `Fraction`, zero float) | all five coefficients vanish |
| 2 — independent | `scripts/crosscheck_sm_float.py` (float, different data layout) | all five `≈ 0` within `1e-9` |
| 3 — literature | standard SM anomaly cancellation (the hypercharges `1/6, 2/3, −1/3, −1/2, −1` are the textbook anomaly-free assignment) | matches |

The five coefficients are `[SU(3)]³`, `[SU(3)]²U(1)`, `[SU(2)]²U(1)`, `[U(1)]³`,
`[grav]²U(1)`. Arms 1 and 2 are different arithmetic paths (exact rational vs float) over
the same fermion content, so they catch transcription/arithmetic bugs; arm 3 catches a
wrong *equation* (it is the field's standard statement).

## 2. Hypercharge uniqueness — three arms agree (scoped)

| arm | method | result |
|---|---|---|
| 1 — exact | `scripts/validate_sm_hypercharge_uniqueness.py` (sympy) | cubic factors `−18·Y_Q·(Y_u−4Y_Q)(Y_u+2Y_Q)` → two physical branches |
| 2 — independent | `scripts/crosscheck_sm_float.py` (numeric root-scan) | roots of `[U(1)]³(r)` at `r = 4` and `r = −2` |
| 3 — literature | the standard result: anomaly cancellation **does not uniquely fix** hypercharge — it fixes the *ratios* up to an overall normalization and discrete ambiguities | matches |

The honest scope, agreed by all three arms: the anomaly conditions determine the
hypercharges **up to (a) an overall normalization and (b) the discrete u↔d swap** — and
the third, unphysical branch `Y_Q = 0` (`0, t, −t, 0, 0`) is excluded by the physical
assumption `Y_Q ≠ 0` (the correct electric-charge assignment). The literature's phrasing
— "cannot be uniquely fixed by anomaly cancellation alone" ([PRD 2019/2020, hypercharge
quantisation](https://ui.adsabs.harvard.edu/abs/2019arXiv190700514L/abstract)) — is
exactly this scoping: it is *not* a unique value, it is a unique *ratio structure* times a
free normalization, plus a discrete swap. That is the "relations, never values" lesson
one sector up.

## Verdict

Both SM headline results now have three independent confirmations that agree. The only
result still at a single confirmation is the GUT-shuffle tabulation
(`validate_gut_parameter_count.py`), which is a counting exercise rather than a physics
claim — it can stay one-arm.
