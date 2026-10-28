# Valiant Verification certificate — The landscape theorem tower (5 theorems)

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **VERIFIED**  
**Gates:** 5 of 5 pass  
**Verified:** yes

| gate | result | evidence | falsifier |
|---|---|---|---|
| `exact_structure_does_mitchell_s_uniqueness_hold_when_the_checker` | **pass** | the D3 tadpole F^T J H is the unique bilinear symplectic invariant of the flux | scripts/validate_mitchell_uniqueness.py exits non-zero — a single failing symbol fails the theorem |
| `exact_structure_does_constraint_first_weyl_fft_hold_when_the_che` | **pass** | the constraint-first construction reproduces the Weyl FFT degrees of freedom | scripts/validate_constraint_first.py exits non-zero — a single failing symbol fails the theorem |
| `exact_structure_does_mitchell_s_completeness_hold_when_the_check` | **pass** | the structure is complete: 6 exact and 2 numeric checks | scripts/validate_mitchell_completeness.py exits non-zero — a single failing symbol fails the theorem |
| `exact_structure_does_full_duality_completion_hold_when_the_check` | **pass** | the COMPLETE duality group, not just the monodromy subgroup | scripts/validate_full_duality.py exits non-zero — a single failing symbol fails the theorem |
| `exact_structure_does_complete_exact_structure_hold_when_the_chec` | **pass** | the assembly of the four theorems above | scripts/validate_all_theorems.py exits non-zero — a single failing symbol fails the theorem |

**Producer:** Scripts: scripts/validate_*.py (re-run at issue time); Module: src/pacland/certify/dossiers.py::physics_theorems; Doctrine: docs/oracles-without-oracles.md

## Limitations

- These are theorems about the *structure of the landscape*, not predictions of observable physics: nothing here is measured against a laboratory.
- The vacuum-energy prediction is not on this certificate; it is not verifiable and is recorded as such in the doctrine.
