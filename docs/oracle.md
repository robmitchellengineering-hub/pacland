# L2 — the physics oracle and its error model (spec)

This is the engineering-facing contract for the layer that turns a genotype into
observables. It is the last unformalized layer, and the bridge from the math (`docs/`)
to a prototype.

Status: spec, no code. Everything here is a contract to build against, not an
implementation.

---

## 1. Place in the system

L2 sits between the encoding (L1) and the verifier (L3):

```
genotype (L1) ──► L2 oracle ──► observables + error model ──► L3 certificate
```

Its one job: given a vacuum encoding, return the observables **and a per-observable
error model**. Without the error model, L3's `p̂_e` term has no input and the certificate
is fiction (`verification-formal.md` §9.2). The error model *is* the product, as much as
the numbers are.

## 2. What the oracle is composed of

For the IIB flux corner (`encoding.md` §1), a pipeline of stages:

| Stage | Computes | Error character |
|---|---|---|
| 1. CY metric solve | Ricci-flat metric | systematic (approximation) |
| 2. Topology | `h^{1,1}`, `h^{2,1}`, intersection numbers | ≈0 (database lookup) |
| 3. Flux enumeration | flux vectors within tadpole bound | ≈0 (exact combinatorics) |
| 4. Moduli stabilization | stabilized moduli, potential | systematic (superpotential truncation) |
| 5. EFT extraction | gauge group, spectrum, Yukawas, Λ | systematic (α′, KK truncation) |

The dominant errors are **systematic, not random**: α′ corrections, non-perturbative
truncations, and the KK tower are *biases*, not noise. The error model must therefore
lead with bias, not dispersion.

## 3. Interface contract (schema)

The oracle's output is a structured document. Sketch (log-space per
`observable-measure.md` §2):

```json
{
  "vacuum": "<genotype id>",
  "observables": {
    "alpha_s_MZ": {
      "value": -2.14,
      "units": "ln(dimensionless)",
      "computable": true,
      "error_model": {
        "kind": "interval",
        "bias": 0.01,
        "scale": 0.005,
        "tail": { "beta": 0.02, "confidence": 0.95 },
        "validated": true
      }
    },
    "cosmo_constant": {
      "computable": false,
      "reason": "requires full non-perturbative moduli stabilization"
    }
  },
  "oracle_meta": {
    "pipeline_version": "0.1.0",
    "tool_versions": { "cymnet": "...", "ks_db": "..." },
    "validation": { "m": 12, "calibrated_observables": 8 }
  }
}
```

Contract rules:

1. **Every observable is either `computable` with an error model, or `computable: false`
   with a `reason`.** A silent `null` is forbidden — it is exactly the class of "looks
   clean but never computed" bugs this repo's philosophy guards against.
2. **`units` is mandatory** — everything is `ln(dimensionless)`; a bare number without
   the log-space convention is a bug.
3. **`error_model.tail` is a claim, not a guarantee** — see §6. It is the oracle's
   *assertion* that `|e| ≤ β` with confidence `confidence`, to be validated.

## 4. The error model, per observable

For observable `x`, the oracle error is `e(x) = Ô(x) − c*(x)`. The error model is a
claim about the distribution of `e(x)` over the oracle's own uncertainty:

- **bias** `b(x)` — systematic offset, the expected over/under-prediction.
- **scale** `σ(x)` — dispersion around the point estimate.
- **tail** `(β(x), 1−δ_β)` — the claim `Pr[ |e(x)| > β(x) ] ≤ δ_β`.

Three allowed `kind`s, to keep the contract minimal and implementable:

| kind | When to use |
|---|---|
| `interval` | you have a bias and a tail bound (preferred) |
| `empirical` | you have a validation set of (Ô, c*) pairs for this observable; the error model *is* that empirical distribution |
| `unknown` | no basis for a bound — treated as `computable: false` for certificate purposes |

`unknown` is the honest default for the hard observables (Λ, `m_u/m_d`): claiming a
bound you cannot defend is worse than reporting none.

## 5. Error propagation across stages

**Design decision, stated:** the certificate trusts the **end-to-end** error model, not
the stage-level error algebra.

- Stage error models exist for **debugging and attribution** — to answer "why is Λ off?"
  — not for the certificate.
- Composing stage models analytically (adding biases, convolving scales) is unreliable
  because stage errors are correlated and truncation errors are systematic. So the
  number that enters `p̂_e` is the **end-to-end validated** error model, measured
  directly against `c*` on the validation set.

The one thing stages *must* do is **not silently drop error**: a stage that truncates a
series must report the truncation as a bias, not absorb it into a "result."

## 6. Calibration — the meta-PAC validation protocol

The oracle's error model is itself a **hypothesis**, validated exactly as
`verification-formal.md` §4 describes:

1. Collect a **validation set** `S_val` of `m` observables where `c*` is known
   (measurement, or exact computation on tractable cases).
2. For each observable, compare the *claimed* tail `(β(x), δ_β)` against the *empirical*
   exceedance rate `p̂_e(x) = (1/m_x) Σ 1[|e| > β(x)]`.
3. Emit a **calibration report** per observable: `well-calibrated` / `miscalibrated` /
   `insufficient data`.

**Definition (well-calibrated).** The oracle's error model for `x` is well-calibrated if
the empirical exceedance rate does not exceed the claimed rate within the confidence
radius — i.e. `p̂_e(x) + sqrt(ln(1/δ_e)/(2m_x)) ≤ δ_β`.

A well-calibrated error model is the only thing that makes `p̂_e` a valid estimate of
`p_e`, and therefore the only thing that makes the certificate mean what it claims.

## 7. The validated / extrapolated split — the honesty rule

Calibration is only possible in the **verification zone** (computable *and* measurable).
Outside it, the error model is an **extrapolation**, not a validation.

**Rule: a certificate may use only `validated: true` error models.** An observable whose
error model is extrapolated is excluded from the certificate and reported in the
**prediction zone** (`observable-measure.md` §6, top-right cell). Its prediction is
falsifiable *later*, and contributes nothing *now*.

This rule is what stops the system from quietly using an unvalidated error model for the
exact observables (Λ) that dominate the science. It is the L2-level enforcement of the
"no certificate, no claim" principle.

## 8. Failure modes, and how each must surface

| Failure | Must surface as |
|---|---|
| Observable not computable | `computable: false` + `reason` |
| No basis for an error bound | `error_model.kind: "unknown"` |
| Claimed bound exceeded on validation | calibration report: `miscalibrated` |
| Too few validation points | calibration report: `insufficient data` |
| Stage truncates and doesn't say so | a stage-level error field that is **not** absorbed |

Each of these is a *reported state*, not an exception to swallow — the class of bug this
whole repo exists to avoid is "the pipeline printed a number with no error and everyone
believed it."

## 9. Boundary: what the oracle does NOT do

- It does **not** emit a certificate — that is L3. The oracle emits an *error model*;
  L3 turns it into a bound.
- It does **not** decide `D` — the weight vector is chosen above the oracle
  (`observable-measure.md` §4).
- It does **not** validate its own error model against unmeasured physics — it can only
  calibrate where `c*` is known (§7).
- It is **not** the same as a learned surrogate. A fast surrogate of the
  compactification→observables map is permitted *inside* the oracle, but only if it
  still emits a calibratable error model; a surrogate with no error model is a speedup,
  not a verifier (README non-goal).

## 10. Build order

1. **One observable, one tool.** Wrap a single existing solver (say, `α_s(M_Z)` from a
   flux vacuum) and have it emit `{value, units, error_model}` end to end. Nothing else
   until this round-trips with an `empirical` error model.
2. **Calibration harness.** The validation protocol (§6) on the few observables where
   `c*` is known, producing calibration reports.
3. **Add observables** one at a time, keeping the `computable: false` + `reason`
   contract honest for the hard ones.
4. **Wire to L3.** The certificate consumes `validated` error models only, and L3's
   `p̂_e` is computed from the calibration report.

The measure of progress is not "more observables computed" but "more observables
**well-calibrated**."

## 11. Open items

1. **A shared validation-set format** so L2's calibration reports and L5's knowledge
   base store the same object.
2. **End-to-end bias measurement** on a tractable exact case — the single most valuable
   data point for calibrating the systematic (α′, truncation) biases.
3. **Whether `empirical` error models should be updated** as the validation set grows —
   this is the L5 revision problem reappearing at the oracle level.
