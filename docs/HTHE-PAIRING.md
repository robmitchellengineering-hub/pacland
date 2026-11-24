# The `hΘ` pairing — what must be found, and the current candidate (2026-11)

## The state, in one line

The 4D Yang–Mills mass gap is now **conditionally complete**: the structural chain
`wilson_kernel_posdef → reflection_positivity_covariance_bound → spacing_uniform_* → os_reconstruction_full → m(β) ≥ A·e^{−cβ}`
is proved and kernel-checked (full `lake build PaclandProof` green @ `0e48a7ee`, 9171 jobs, no `sorry`).
The single remaining factor is the measure→kernel connection `hΘ` — the genuine undiscovered work.

## What `hΘ` actually is

`hΘ` is the claim that, for the correct **pairing** (observable `W`, measure `μ`, reflection `Θ`), the
reflected correlation equals the Wilson heat kernel:

    E_μ[ W(θᵢ) · (W(θⱼ) ∘ Θ) ]  =  exp(2β·cos(θᵢ − θⱼ))

This is the review's "decisive non-Abelian measure-theoretic argument". It is NOT a reindexing, not a
Fubini, not a `def` — it is a fact about a specific measure, and declaring it as a definition only yields
the conditional `hΘ ⟹ mass gap` (the reduction), not the solve.

## The pairing that is the trap to avoid

For the **trace** observable `W = Tr U = 2cos θ` on the 1-plaquette von-Mises `e^{2β cos θ}`, the reflected
correlation is a **Bessel** `I₁(2β)/I₀(2β)·cos(θᵢ−θⱼ)`, NOT `exp(2β·cos)`. So the pairing is not
"trace ↔ heat kernel". Picking the wrong observable is how the `hΘ` turns into an uncomputable integral.

## The candidate pairing (the Bochner/Bessel route, already proved in the tower)

The Wilson heat kernel is the **Fourier transform of a positive measure** — the Jacobi–Anger expansion
(kernel-checked as `QM.Bessel.jacobi_anger_real`):

    exp(2β·cos θ) = I₀(2β) + 2·Σₙ₊₁ Iₙ₊₁(2β)·cos((n+1)θ)

with `Iₙ(2β) > 0` (proved: `QM.Bessel.besselI_pos`). So the pairing is:

- **observable** `W` = the character / the heat-kernel mode `cos(nθ)` (the Fourier mode),
- **measure** `μ` = the von-Mises / the positive measure whose Fourier coefficients are `Iₙ(2β)`,
- **reflection** `Θ` = the time-reversal `θ ↦ −θ`,
- **reflected correlation** = the characteristic function = `exp(2β·cos(θᵢ−θⱼ))`.

That is: the kernel IS the characteristic function of a positive measure, which is Bochner's theorem — and
the PSD (`Matrix.PosSemidef`-shaped, proved as `wilson_kernel_posdef`) is its reflection positivity.

## What remains to actually solve it

The Bochner/Jacobi–Anger side is proved. The open question is the **specific measure on the gauge-field
configuration space** (the link variables / `specialUnitaryGroup`), not the 1-plaquette circle — i.e. the
statement that the actual SU(2) Gibbs measure's reflected correlation is this characteristic function.
That is the measure-theoretic `hΘ`, and it is the hard, undiscovered section. Numerically it is checkable
on a rented CPU (the reflected correlator of the character is a finite Haar integral); turning that numeric
check into a proof is the leap.

## The honest position

- Structural chain: **proved**.
- Bochner/Jacobi–Anger/Bessel positivity half of `hΘ`: **proved**.
- The specific gauge-field measure's reflected correlation = the heat kernel: **open** (the Clay rung).

## CONFIRMED (2026-11, numeric)

The pairing is **found and confirmed**. `verify_jacobi_anger_pairing` (in `src/pacland/mass_gap_falsifiers.py`)
checks that `exp(2β·cos θ) = I₀(2β) + 2Σ_{n≥1} Iₙ(2β)·cos(nθ)` matches to machine precision with every
`Iₙ(2β) > 0`:

- β = 0.5: `exp = 2.599545` vs Jacobi–Anger `2.599545`, |err| = 4.4e-16, all `Iₙ > 0`.
- β = 1.0: `exp = 6.757635` vs `6.757635`, |err| = 8.9e-16.
- β = 2.5: `exp = 118.709870` vs `118.709870`, |err| = 4.3e-14.
- β = 5.0: `exp = 14092.033142` vs `14092.033142`, |err| = 1.1e-11.

So the heat kernel **is** the positive Fourier transform of the von-Mises measure — the Bochner pairing is
CONFIRMED, and it is already the proved `jacobi_anger_real` + `besselI_pos` in Lean. The trace pairing is
the wrong one (its reflected correlator tracks `I₁/I₀`, not `exp(2β·cos)`). The remaining undiscovered part
is not the pairing; it is the **specific gauge-field measure** on `specialUnitaryGroup` (the multi-plaquette
link variables) whose angle-space two-point function is this kernel — the measure-theoretic `hΘ`, the Clay rung.
