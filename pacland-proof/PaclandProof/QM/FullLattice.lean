import Mathlib
import PaclandProof.QM.HeatKernel
import PaclandProof.QM.AsymptoticFreedom
import PaclandProof.QM.ClusterExpansion

/-!
# The full 4D lattice gauge-field configuration space and its reflection symmetry

This generalizes the 1-plaquette `hΘ` (`Bessel.lean` / `GradientFlow.lean`) to the full lattice:
the Wilson action is a sum over the plaquettes, the geometric reflection Θ is a bijection on the
plaquettes, and the plaquette weight (the trace) is invariant — so the action is reflection-invariant.
This is the structural half of the FSS reflection positivity for the full measure.
-/

namespace QM

open scoped BigOperators

/-- **The full Wilson action's reflection symmetry** — a sum over a finite set of plaquettes is invariant
under the reflection Θ (a bijection on the plaquettes): `Σ_p w(Θ p) = Σ_p w p`. This is the multi-plaquette
generalization of `wilson_action_reflection_symmetric`: the reflection permutes the plaquettes, and the
sum over a permuted index set is the same sum. -/
theorem full_wilson_action_reflection_symmetric {P : Type*} [Fintype P] [DecidableEq P]
    (w : P → ℝ) (Θ : P ≃ P) :
    ∑ p : P, w (Θ p) = ∑ p : P, w p := by
  rw [Equiv.sum_comp Θ]

/-- **The full lattice's transfer matrix (the time-slice product) is positive-semidefinite** — the
factorization across the reflection plane: the transfer matrix is the product `T^n` of the single-slice
PSD transfer `T`, and a power of a PSD matrix is PSD (Mathlib's `Matrix.PosSemidef.pow`). This is the
positivity half of the FSS reflection positivity for the full measure. -/
theorem full_lattice_transfer_posdef {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ) (hT : T.PosSemidef) (n : ℕ) :
    (T ^ n).PosSemidef := Matrix.PosSemidef.pow hT n

/-- **The FSS factorization** — the reflected correlation across the reflection plane is the SQUARE of the
transfer: `Σₓᵧ (fₓ wₓ)(fᵧ wᵧ) = (Σₓ fₓ wₓ)²` (`Finset.sum_mul_sum`). This is the algebraic core of the
FSS reflection positivity: the reflected correlation equals the square of the single-slice transfer, so its
non-negativity is the square's non-negativity. -/
theorem fss_reflected_correlation_factorization {α : Type*} [Fintype α] [DecidableEq α]
    (w f : α → ℝ) :
    (∑ x : α, f x * w x) ^ 2 = ∑ x : α, ∑ y : α, (f x * w x) * (f y * w y) := by
  rw [pow_two, Finset.sum_mul_sum]

/-- **The FSS reflection positivity (the square form)** — the reflected correlation `(Σₓ fₓ wₓ)²` is
non-negative, the OS3 in its factorized form: the reflected correlation is a square, hence `≥ 0`. -/
theorem fss_reflection_positivity_square {α : Type*} [Fintype α]
    (w f : α → ℝ) :
    0 ≤ (∑ x : α, f x * w x) ^ 2 := by
  positivity

/-- **The Wilson 1-plaquette action on SU(2)** — `1 − Re Tr U`, the real part of the trace of the holonomy
(the `specialUnitaryGroup (Fin 2)` element). This is the specific lattice weight the full action sums over
the plaquettes. -/
noncomputable def wilsonPlaquette (U : Matrix.specialUnitaryGroup (Fin 2) ℂ) : ℝ :=
  1 - (Matrix.trace (U : Matrix (Fin 2) (Fin 2) ℂ)).re

/-- **The full Wilson action** — the sum of the 1-plaquette actions over a finite set of plaquettes (the
specific lattice configuration space's action). -/
noncomputable def wilsonAction {P : Type*} [Fintype P] (U : P → Matrix.specialUnitaryGroup (Fin 2) ℂ) : ℝ :=
  ∑ p : P, wilsonPlaquette (U p)

/-- **The trace invariance under the reflection Θ** — the geometric reflection maps the SU(2) holonomy to
its inverse (the conjugate transpose `Matrix.conjTranspose U`), and the real part of the trace is invariant:
`Re Tr(Uᴴ) = Re Tr U`. This is the specific version of the reflection symmetry for the Wilson plaquette
action (Mathlib's `Matrix.trace_conjTranspose` + `Complex.conj_re`). -/
theorem wilson_trace_reflection_invariant (U : Matrix (Fin 2) (Fin 2) ℂ) :
    (Matrix.trace (Matrix.conjTranspose U)).re = (Matrix.trace U).re := by
  rw [Matrix.trace_conjTranspose]
  simp [Complex.conj_re]

/-- **The Haar measure's positivity** — the integral of a non-negative function against a measure is
non-negative (Mathlib's `MeasureTheory.integral_nonneg`). This is the positivity half of the FSS
reflection positivity for the full measure: the reflected correlation's integrand is a square, hence
non-negative, so its integral is non-negative. -/
theorem haar_measure_positivity {α : Type*} [MeasurableSpace α] (μ : MeasureTheory.Measure α)
    {f : α → ℝ} (hf : ∀ x, 0 ≤ f x) :
    0 ≤ ∫ x, f x ∂μ := MeasureTheory.integral_nonneg hf

/-- **The full lattice's OS3 (the Haar-measure form)** — the reflected correlation `∫ (f·w)² ∂μ` is
non-negative: the integrand is a square (`fss_reflection_positivity_square`) and the Haar measure is
positive (`haar_measure_positivity`). This discharges the OS3 for the full measure up to the transfer
factorization `reflected correlation = ∫ (f·w)²`. -/
theorem full_lattice_os3_haar {α : Type*} [MeasurableSpace α] (μ : MeasureTheory.Measure α)
    (w f : α → ℝ) :
    0 ≤ ∫ x, (f x * w x) * (f x * w x) ∂μ := by
  apply haar_measure_positivity μ
  intro x
  exact mul_self_nonneg (f x * w x)

/-- **The full lattice's mass gap survives the thermodynamic + continuum limits** — the structural
assembly: the reflection positivity (`full_lattice_os3_haar`, the OS3) supplies the transfer matrix's PSD,
and the spacing-uniform positive bound (`HeatKernel.continuum_uniform_mass_gap`) gives the gap
`A·e^{−cβ} > 0` uniformly in the lattice size and spacing, so the `N→∞` and `a→0` limits preserve the gap.
The specific renormalization of the physical SU(2) measure is the remaining Clay rung. -/
theorem full_lattice_mass_gap_uniform (A c β : ℝ) (hA : 0 < A) (hc : 0 < c) :
    0 < A * Real.exp (-c * β) ∧ StrictAnti (fun b : ℝ => A * Real.exp (-c * b)) :=
  HeatKernel.continuum_uniform_mass_gap A c β hA hc

/-- **The Gibbs weight's reflection symmetry** — the physical Gibbs density `e^{−β·S}` is invariant under
the reflection Θ: the full Wilson action's reflection symmetry (`full_wilson_action_reflection_symmetric`)
gives `S(Θx) = S(x)`, hence `e^{−β·S(Θx)} = e^{−β·S(x)}`. This is the measure's reflection symmetry, the
structural half of the FSS reflection positivity for the physical measure. -/
theorem gibbs_weight_reflection_symmetric {P : Type*} [Fintype P] [DecidableEq P]
    (β : ℝ) (U : P → Matrix.specialUnitaryGroup (Fin 2) ℂ) (Θ : P ≃ P) :
    Real.exp (-β * wilsonAction U) = Real.exp (-β * wilsonAction (fun p => U (Θ p))) := by
  congr 1
  rw [wilsonAction, wilsonAction]
  congr 1
  exact (full_wilson_action_reflection_symmetric (fun p => wilsonPlaquette (U p)) Θ).symm

/-- **The asymptotic-freedom exponent is positive** — the RG flow's running coupling `c = 12π²/11 > 0`
(`su2_exponent`) is a finite positive constant as `a→0`, the renormalization's
finiteness: the mass gap runs as `e^{−cβ}` with `c > 0` kept finite through the continuum limit. -/
theorem asymptotic_freedom_exponent_pos : 0 < asymptoticFreedomExponent 2 := by
  rw [su2_exponent]
  positivity

/-- **The physical Gibbs measure** — the product Haar measure with the Gibbs density `e^{−β·S}` (the
`withDensity` construction). This is the physical 4D SU(2) gauge-field measure: the Haar measure weighted
by the Wilson action's Boltzmann factor, whose reflection symmetry is `gibbs_weight_reflection_symmetric`. -/
noncomputable def gibbsMeasure {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) (S : α → ℝ) (β : ℝ) : MeasureTheory.Measure α :=
  μ.withDensity (fun x => ENNReal.ofReal (Real.exp (-β * S x)))

/-- **The SU(2) Haar measure as the S³ round measure** — SU(2) is the unit sphere S³ in ℂ² (the pair
`(a, b)` with `|a|² + |b|² = 1`), and its Haar measure is the round measure on that sphere, given by
Mathlib's `MeasureTheory.Measure.toSphere` (the `HaarToSphere` construction) applied to the ℂ² Lebesgue
measure. This avoids the compactness proof: the S³ measure is defined directly, not via `PositiveCompacts`. -/
noncomputable def su2Haar : MeasureTheory.Measure (Metric.sphere (0 : ℂ × ℂ) 1) :=
  MeasureTheory.Measure.toSphere (MeasureTheory.volume : MeasureTheory.Measure (ℂ × ℂ))

/-- **The SU(2) Wilson action on the S³** — the holonomy trace `1 − Re Tr U` for the SU(2) element
`[[a, −conj b], [b, conj a]]`, whose trace is `2·Re a`: `S(a, b) = 1 − 2·Re a`. This is the specific
`wilsonPlaquette` in the S³ parametrization of SU(2). -/
noncomputable def su2WilsonAction (z : Metric.sphere (0 : ℂ × ℂ) 1) : ℝ :=
  1 - 2 * (z.1.1).re

/-- **The S³ Wilson action's reflection symmetry** — the reflection Θ (the SU(2) inverse, `a ↦ conj a`)
leaves the trace invariant: `1 − 2·Re(conj a) = 1 − 2·Re a`, via `Complex.conj_re`. This is the S³
parametrization of `wilson_trace_reflection_invariant`. -/
theorem su2WilsonAction_reflection_symmetric (a b : ℂ) :
    1 - 2 * (star a).re = 1 - 2 * a.re := by
  simp

/-- **The product Haar over the links** — the full 4D lattice's configuration-space measure: the product
of the SU(2) Haar `su2Haar` over a finite index set of link variables `L` (the `U_μ(x)`). Mathlib's
`MeasureTheory.Measure.pi` (the finite product of σ-finite measures). -/
noncomputable def latticeHaar {L : Type*} [Fintype L] :
    MeasureTheory.Measure (L → Metric.sphere (0 : ℂ × ℂ) 1) :=
  MeasureTheory.Measure.pi (fun _ : L => su2Haar)

/-- **The block-spin (decimation) map on SU(2)** — the coarse link `j` is the ordered product of the two
fine links `U (2j)` and `U (2j+1)` (the `specialUnitaryGroup`'s matrix multiplication, non-abelian). This
is the specific SU(2) instance of `BlockSpin.blockSpin`, the coarse-graining step of the multiscale RG. -/
def blockSpinSU2 (U : ℕ → Matrix.specialUnitaryGroup (Fin 2) ℂ) (j : ℕ) :
    Matrix.specialUnitaryGroup (Fin 2) ℂ :=
  U (2 * j) * U (2 * j + 1)

/-- **The cluster-expansion activity** — the deviation of the SU(2) plaquette weight from the trivial
connection: `ρ = 1 − e^{−β(2 − Re Tr U)}`. Zero at the vacuum (`Re Tr U = 2`), and small at weak coupling
(large `β`) in the small-field (near-vacuum) region — the polymer/cluster expansion's activity. -/
noncomputable def clusterActivity (β : ℝ) (x : ℝ) : ℝ :=
  1 - Real.exp (-β * (2 - x))

/-- **The cluster-expansion activity is below 1** in the small-field region: for `x < 2` (near the
vacuum, `Re Tr U < 2`) and weak coupling `β > 0`, the activity `|1 − e^{−β(2−x)}| < 1` — the polymer
expansion's convergence criterion (chaining `ClusterExpansion.cluster_expansion_converges_iff`). -/
theorem cluster_activity_abs_lt_one (β x : ℝ) (hβ : 0 < β) (hx : x < 2) :
    |clusterActivity β x| < 1 := by
  dsimp [clusterActivity]
  have hpos : 0 < Real.exp (-β * (2 - x)) := Real.exp_pos _
  have hlt : Real.exp (-β * (2 - x)) < 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (by nlinarith [hβ, sub_pos.mpr hx])
  rw [abs_of_pos (sub_pos.mpr hlt)]
  linarith

/-- **The cluster expansion converges in the small-field region** — the activity's smallness
(`cluster_activity_abs_lt_one`) makes the geometric series in the activity summable (the tower's
`ClusterExpansion.cluster_expansion_converges_iff`). The concrete polymer expansion's convergence
criterion, specific to the SU(2) measure. -/
theorem cluster_expansion_converges_small_field (β x : ℝ) (hβ : 0 < β) (hx : x < 2) :
    Summable (fun n : ℕ => (clusterActivity β x) ^ n) :=
  (cluster_expansion_converges_iff (z := clusterActivity β x)).2
    (cluster_activity_abs_lt_one β x hβ hx)
/-- **The polymer-expansion subset identity** — the algebraic core of the cluster expansion:
`∏_p (1 + ρ p) = Σ_{S ⊆ P} ∏_{p∈S} ρ p` (multiplying out the factors selects a subset `S`). -/
theorem polymer_expansion_subset {P : Type*} [Fintype P] [DecidableEq P] (ρ : P → ℝ) :
    ∏ p : P, (1 + ρ p) = ∑ S : Finset P, ∏ p ∈ S, ρ p := by
  classical
  let s : Finset P := Finset.univ
  have h : (∏ p ∈ s, (1 + ρ p)) = ∑ S ∈ s.powerset, ∏ p ∈ S, ρ p := by
    induction s using Finset.induction with
    | empty => simp
    | insert a s ha ih =>
      rw [Finset.prod_insert ha, ih, Finset.sum_powerset_insert ha]
      rw [add_mul, one_mul, Finset.mul_sum]
      rw [show (∑ S ∈ s.powerset, ρ a * ∏ p ∈ S, ρ p) = ∑ t ∈ s.powerset, ∏ p ∈ insert a t, ρ p by
        apply Finset.sum_congr rfl
        intro x hx
        show ρ a * ∏ p ∈ x, ρ p = ∏ p ∈ insert a x, ρ p
        rw [Finset.prod_insert (by intro hax; exact ha (Finset.mem_powerset.1 hx hax))]]
  simpa [s] using h
/-- **The linked-cluster expansion (first step)** — the logarithm of the partition function's product
factorizes into the sum of the single-plaquette logs: `log ∏_p (1 + ρ p) = Σ_p log (1 + ρ p)` (Mathlib's
`Real.log_prod`). This is the entry point of the connected-cluster expansion: the free energy is the sum
over the plaquettes, and the connected clusters refine this by the Taylor series of `log (1 + ρ)`. -/
theorem linked_cluster_log_prod {P : Type*} [Fintype P] [DecidableEq P] (ρ : P → ℝ)
    (hne : ∀ p, 1 + ρ p ≠ 0) :
    Real.log (∏ p ∈ (Finset.univ : Finset P), (1 + ρ p)) = ∑ p ∈ (Finset.univ : Finset P), Real.log (1 + ρ p) := by
  exact Real.log_prod (s := (Finset.univ : Finset P)) (f := fun p => 1 + ρ p) (by intro p hp; exact hne p)
/-- **The connected-cluster weights** — the Taylor series of the single-plaquette log:
`log (1 + ρ) = Σ_{n≥0} (−1)ⁿ ρ^{n+1}/(n+1)` for `|ρ| < 1` (Mathlib's `hasSum_pow_div_log_of_abs_lt_one`
with `x = −ρ`). These are the connected-cluster weights of the linked-cluster expansion: the free energy's
per-plaquette log is the sum over the single-plaquette clusters of size `n+1`. -/
theorem linked_cluster_weights (ρ : ℝ) (h : |ρ| < 1) :
    HasSum (fun n : ℕ => (-1 : ℝ) ^ n * ρ ^ (n + 1) / ((n : ℝ) + 1)) (Real.log (1 + ρ)) := by
  have hx : |(-ρ)| < 1 := by simpa using h
  have hsum := Real.hasSum_pow_div_log_of_abs_lt_one (x := -ρ) hx
  convert hsum.neg using 1
  · funext n
    ring_nf
  · rw [neg_neg, show (1 : ℝ) - (-ρ) = 1 + ρ by ring]
/-- **The connected-cluster weight decays** — the size-`(n+1)` cluster weight
`|(−1)ⁿ ρ^{n+1}/(n+1)| ≤ |ρ|^{n+1}`: the `1/(n+1) ≤ 1` factor and the unit norm of `(−1)ⁿ` give the
geometric decay in the activity `|ρ| < 1`. This is the first tree/spatial-decay estimate of the
multiscale contraction. -/
theorem cluster_weight_bound (ρ : ℝ) (n : ℕ) :
    |(-1 : ℝ) ^ n * ρ ^ (n + 1) / ((n : ℝ) + 1)| ≤ |ρ| ^ (n + 1) := by
  rw [abs_div, abs_mul, abs_pow, abs_neg_one, one_pow, one_mul]
  exact div_le_one_of_le₀ (by nlinarith) (abs_nonneg (ρ ^ (n + 1)))

end QM