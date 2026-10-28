# Model risk certificate — The landscape theorem tower (5 theorems)

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **VERIFIED**

Every theorem re-checked at issue time: the exact structure of the flux landscape is the D3 tadpole, it is unique, and it is complete. The failure mode here is a proof that does not compile, and all five compile.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Exact structure | Does Mitchell's Uniqueness hold when the checker is re-run? | the D3 tadpole F^T J H is the unique bilinear symplectic invariant of the flux | **satisfied** |
| Exact structure | Does Constraint-First (Weyl FFT) hold when the checker is re-run? | the constraint-first construction reproduces the Weyl FFT degrees of freedom | **satisfied** |
| Exact structure | Does Mitchell's Completeness hold when the checker is re-run? | the structure is complete: 6 exact and 2 numeric checks | **satisfied** |
| Exact structure | Does Full-duality completion hold when the checker is re-run? | the COMPLETE duality group, not just the monodromy subgroup | **satisfied** |
| Exact structure | Does Complete Exact Structure hold when the checker is re-run? | the assembly of the four theorems above | **satisfied** |

## Evidence

- Scripts: scripts/validate_*.py (re-run at issue time)
- Module: src/pacland/certify/dossiers.py::physics_theorems
- Doctrine: docs/oracles-without-oracles.md

## Limitations

- These are theorems about the *structure of the landscape*, not predictions of observable physics: nothing here is measured against a laboratory.
- The vacuum-energy prediction is not on this certificate; it is not verifiable and is recorded as such in the doctrine.

_5 findings: 5 satisfied._
