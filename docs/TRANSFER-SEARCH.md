# Structure-transfer search — four under-used disciplines vs the 4D mass gap

Fan-out result (2026-11-18), four disciplines searched for a theorem that bounds the 4D Yang–Mills mass
gap. **None does.** What each actually delivers, honestly:

## The four disciplines

| discipline | the specific tool | what it bounds | verdict for 4D YM |
|---|---|---|---|
| Spectral graph theory | Cheeger `λ₂ ≥ h²/2`; Garland method; high-dim expanders | the *spatial* graph's Laplacian gap | **wrong object** — the mass gap is the transfer-matrix gap over the gauge *configuration space*, not the lattice Laplacian; finite-volume/combinatorial only |
| Thermodynamic formalism | Ruelle spectral gap; Ionescu–Tulcea–Marinescu quasi-compactness | gap of a transfer operator | ITM is the *right mechanism*, but only at **strong coupling / finite volume** (Osterwalder–Seiler); Ruelle needs hyperbolic dynamics the YM matrix lacks |
| Coarse geometry / K-theory | Roe's coarse spectral gap; Baum–Connes assembly map | a *fixed-space* gap preserved under coarse equivalence | **framework only** — and the essential spectrum is **not lower-semicontinuous**, so the gap can *close* in `a→0`; Baum–Connes is index/obstruction theory, false without Property A, no numeric gap |
| Optimal transport | CD(K,N) (Lott–Villani–Sturm); CD→LSI→spectral-gap chain | a metric-measure spectral gap, stable under measured Gromov–Hausdorff limits | **most promising** — could hold on the gauge quotient where pointwise BE fails — but proven nowhere for the Wilson measure, and only gives the lattice gap, not `K > 0` uniform in `a→0` |

## The two things this teaches

1. **CD(K,N) is Rung A in the right language.** The multiscale Bakry–Émery fix is exactly the CD(K,N)
   route: replace the pointwise Hessian (which fails) with a metric-measure curvature that survives
   coarse-graining. The transfer search independently converged on the same target — corroboration, not
   a detour.

2. **The coarse-geometry result names the precise obstacle to the continuum limit.** "The essential
   spectrum is not lower-semicontinuous, so a finite-volume gap can close in the limit" is the technical
   reason `Δ > 0` at finite volume does not automatically give `Δ > 0` in the continuum.

## Honest bottom line

No untouched discipline secretly bounds the 4D gap — that hope is falsified. What remains: (a) CD(K,N)
as the correct framing of the crossover (Rung A), and (b) the lower-semicontinuity obstruction as the
named difficulty of the continuum limit.

## Key references

- Cheeger: Alon–Milman (1985); Chung, *Four proofs of the Cheeger inequality*. Garland (Ann. Math. 1973); Lubotzky, *High Dimensional Expanders*.
- Transfer operators: Ruelle (CMP 9, 1968; *Thermodynamic Formalism* 1978); Ionescu–Tulcea–Marinescu (Ann. Math. 52, 1950); Osterwalder–Seiler (1978).
- Coarse geometry: Roe (1988/93); Baum–Connes (1982); Higson–Lafforgue–Skandalis (2002, expanders break coarse BC).
- CD(K,N): Sturm (Acta Math. 196, 2006); Lott–Villani (Ann. Math. 169, 2009); Ambrosio–Gigli–Savaré (Ann. Probab. 43, 2015, weak BE ⇔ RCD).
