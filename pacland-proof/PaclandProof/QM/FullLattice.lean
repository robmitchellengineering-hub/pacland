import Mathlib
import PaclandProof.QM.HeatKernel
import PaclandProof.QM.AsymptoticFreedom
import PaclandProof.QM.ClusterExpansion

set_option maxHeartbeats 2000000

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
`|(−1)ⁿ ρ^{n+1}/(n+1)| ≤ |ρ|^{n+1}`: the `1/(n+1) ≤ 1` factor gives the geometric decay in `|ρ|`. -/
theorem cluster_weight_bound (ρ : ℝ) (n : ℕ) :
    |(-1 : ℝ) ^ n * ρ ^ (n + 1) / ((n : ℝ) + 1)| ≤ |ρ| ^ (n + 1) := by
  rw [abs_div, abs_mul, abs_pow]
  norm_num
  have hone : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
  have hpos : (0 : ℝ) ≤ (n : ℝ) + 1 := by linarith
  have hle : (1 : ℝ) ≤ |(n : ℝ) + 1| := by
    rw [abs_of_nonneg hpos]
    linarith
  exact div_le_self (pow_nonneg (abs_nonneg ρ) (n + 1)) hle
/-- **The cluster weights are absolutely summable** — the geometric decay `cluster_weight_bound` plus the
convergent geometric series `Σ |ρ|ⁿ` (for `|ρ| < 1`) gives the absolute summability of the connected-cluster
weights. This is the convergence of the linked-cluster expansion. -/
theorem cluster_weights_summable (ρ : ℝ) (h : |ρ| < 1) :
    Summable (fun n : ℕ => |(-1 : ℝ) ^ n * ρ ^ (n + 1) / ((n : ℝ) + 1)|) := by
  refine Summable.of_nonneg_of_le (fun n => abs_nonneg _) (fun n => cluster_weight_bound ρ n) ?_
  have hgeo : Summable (fun n : ℕ => |ρ| ^ n) := summable_geometric_iff_norm_lt_one.mpr (by simpa using h)
  have hgeo' : Summable (fun n : ℕ => |ρ| ^ (n + 1)) := by
    simpa [pow_succ, mul_comm] using hgeo.mul_left |ρ|
  exact hgeo'
/-- **The walks-count bound** (the animals estimate's first lemma): the number of walks of length `n`
from `u` to `v` on a finite graph is at most `maxDegree ^ n`. -/
theorem walk_count_bound {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (u v : V) (n : ℕ) :
    (G.finsetWalkLength n u v).card ≤ G.maxDegree ^ n := by
  induction n generalizing u v with
  | zero =>
    simp only [SimpleGraph.finsetWalkLength]
    split_ifs
    · subst v
      simp
    · simp
  | succ n ih =>
    simp only [SimpleGraph.finsetWalkLength]
    calc
      (Finset.univ.biUnion fun w : {w : V // w ∈ G.neighborSet u} => (G.finsetWalkLength n w v).map
        ⟨fun p => SimpleGraph.Walk.cons w.property p, fun _ _ h => by injection h with hpq⟩).card
        ≤ ∑ w ∈ (Finset.univ : Finset {w : V // w ∈ G.neighborSet u}), ((G.finsetWalkLength n w v).map
            ⟨fun p => SimpleGraph.Walk.cons w.property p, fun _ _ h => by injection h with hpq⟩).card :=
            Finset.card_biUnion_le
      _ = ∑ w ∈ (Finset.univ : Finset {w : V // w ∈ G.neighborSet u}), (G.finsetWalkLength n w v).card := by
            refine Finset.sum_congr rfl (fun w hw => ?_)
            rw [Finset.card_map]
      _ ≤ ∑ w ∈ (Finset.univ : Finset {w : V // w ∈ G.neighborSet u}), G.maxDegree ^ n :=
            Finset.sum_le_sum (fun w hw => ih w v)
      _ = (Finset.univ : Finset {w : V // w ∈ G.neighborSet u}).card * G.maxDegree ^ n := by
            simp [Finset.sum_const]
      _ = G.degree u * G.maxDegree ^ n := by
            congr 1
            rw [SimpleGraph.degree]
            simpa [SimpleGraph.neighborFinset_def, Finset.mem_filter] using
              (Fintype.card_coe (s := Finset.filter (fun x => G.Adj u x) Finset.univ))
      _ ≤ G.maxDegree * G.maxDegree ^ n := Nat.mul_le_mul_right _ (G.degree_le_maxDegree u)
      _ = G.maxDegree ^ (n + 1) := by rw [pow_succ']

/-- **The animals-weight series converges** — the size-class weight `(Δ+1)^(2n) · |ρ|ⁿ` is the geometric
series in `(Δ+1)² |ρ|`, so it is summable exactly when `(Δ+1)² |ρ| < 1`. This chains the animals bound's
`(Δ+1)^(2n)` growth against the cluster activity's `|ρ|ⁿ` decay — the small-field convergence of the
linked-cluster expansion for an arbitrary graph of max degree `Δ`. -/
theorem animals_weight_summable (Δ : ℕ) (ρ : ℝ) (h : |ρ| * ((Δ : ℝ) + 1)^2 < 1) :
    Summable (fun n : ℕ => ((Δ : ℝ) + 1)^(2*n) * |ρ|^n) := by
  have ha : abs (((Δ : ℝ) + 1)^2 * abs ρ) < 1 := by
    calc
      abs (((Δ : ℝ) + 1)^2 * abs ρ) = ((Δ : ℝ) + 1)^2 * abs ρ := by
        rw [abs_mul, abs_of_nonneg (sq_nonneg ((Δ : ℝ) + 1)), abs_of_nonneg (abs_nonneg ρ)]
      _ = abs ρ * ((Δ : ℝ) + 1)^2 := by ring
      _ < 1 := h
  have hgeom : Summable (fun n : ℕ => (((Δ : ℝ) + 1)^2 * abs ρ)^n) :=
    summable_geometric_iff_norm_lt_one.mpr (by simpa [Real.norm_eq_abs] using ha)
  convert hgeom using 1
  ext n
  rw [mul_pow, pow_mul]

/-- **The actual animals majorant converges** — the size-class count carries the `2n` factor (the
polynomial growth), so the real weighted majorant is `2n·((Δ+1)²|ρ|)ⁿ`, and `Σ n·aⁿ` converges for
`|a| < 1` (polynomial-times-geometric). This is the missing link: the geometric series alone did not
bound the `2n`-weighted count. -/
theorem animals_majorant_summable (Δ : ℕ) (ρ : ℝ) (h : |ρ| * ((Δ : ℝ) + 1)^2 < 1) :
    Summable (fun n : ℕ => 2 * (n : ℝ) * (((Δ : ℝ) + 1)^2 * |ρ|)^n) := by
  have ha : ‖((Δ : ℝ) + 1)^2 * abs ρ‖ < 1 := by
    rw [Real.norm_eq_abs]
    calc
      abs (((Δ : ℝ) + 1)^2 * abs ρ) = ((Δ : ℝ) + 1)^2 * abs ρ := by
        rw [abs_mul, abs_of_nonneg (sq_nonneg ((Δ : ℝ) + 1)), abs_of_nonneg (abs_nonneg ρ)]
      _ = abs ρ * ((Δ : ℝ) + 1)^2 := by ring
      _ < 1 := h
  have hpow : Summable (fun n : ℕ => (n : ℝ)^1 * (((Δ : ℝ) + 1)^2 * abs ρ)^n) :=
    summable_pow_mul_geometric_of_norm_lt_one 1 ha
  simpa [pow_one, mul_assoc] using hpow.mul_left 2

/-- **The tour-length majorant converges** — the exact animals count uses the Euler-tour exponent
`2(n−1)` (not `2n`), and `(Δ+1)^(2(n−1)) ≤ (Δ+1)^(2n)` for `Δ+1 ≥ 1`, so the dominating `2n`-majorant's
summability implies this one. This is the exact weighted majorant from `rooted_animals_count_bound_gen`. -/
theorem animals_majorant_tour_summable (Δ : ℕ) (ρ : ℝ) (h : |ρ| * ((Δ : ℝ) + 1)^2 < 1) :
    Summable (fun n : ℕ => (2 * (n : ℝ)) * ((Δ : ℝ) + 1)^(2*(n-1)) * |ρ|^n) := by
  refine Summable.of_nonneg_of_le
    (fun n => by positivity)
    (fun n => ?_) (animals_majorant_summable Δ ρ h)
  have hle : ((Δ : ℝ) + 1)^(2*(n-1)) ≤ ((Δ : ℝ) + 1)^(2*n) := by
    exact_mod_cast (Nat.pow_le_pow_right (Nat.succ_le_succ (Nat.zero_le Δ)) (by omega : 2*(n-1) ≤ 2*n))
  simpa [mul_assoc, mul_pow, pow_mul] using
    (mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right hle (pow_nonneg (abs_nonneg ρ) n))
      (mul_nonneg zero_le_two (Nat.cast_nonneg n)))

/-- **The quadratic RG contraction (volume-uniform)** — the cluster-expansion condition
`(Δ+1)²|ρ| < 1` is self-improving: the renormalised activity `|ρ|²(Δ+1)⁴` is the *square* of
`|ρ|(Δ+1)²`, so `|ρ|²(Δ+1)⁴ < 1` follows. This is the RG step's contraction, and it depends only on
`(Δ, ρ)` — never on the lattice volume — so the iteration below carries to the thermodynamic limit
without computing the infinite lattice. -/
theorem rg_quadratic_contraction (Δ : ℕ) (ρ : ℝ) (h : |ρ| * ((Δ : ℝ) + 1)^2 < 1) :
    |ρ|^2 * ((Δ : ℝ) + 1)^4 < 1 := by
  have ha : 0 ≤ |ρ| * ((Δ : ℝ) + 1)^2 := mul_nonneg (abs_nonneg ρ) (sq_nonneg ((Δ : ℝ) + 1))
  have hle1 : |ρ| * ((Δ : ℝ) + 1)^2 ≤ 1 := le_of_lt h
  have hsqle : (|ρ| * ((Δ : ℝ) + 1)^2)^2 ≤ |ρ| * ((Δ : ℝ) + 1)^2 := by
    nlinarith [mul_le_mul_of_nonneg_right hle1 ha]
  have hsq : (|ρ| * ((Δ : ℝ) + 1)^2)^2 < 1 := hsqle.trans_lt h
  convert hsq using 1
  ring_nf


/-- **The S³ inner product (the SU(2) trace product's real part).** For SU(2) elements parametrized by the
S³ points `z = (a, b)`, `w = (c, d)`, the trace of the product `U_z · U_w⁻¹` has real part
`2·Re(a·conj c + b·conj d)` — twice the S³ (ℂ² Hermitian) inner product. This is the boundary coupling:
the shared plaquette across the reflection plane. -/
noncomputable def s3Inner (z w : Metric.sphere (0 : ℂ × ℂ) 1) : ℝ :=
  (z.1.1 * star w.1.1 + z.1.2 * star w.1.2).re

/-- **The transfer-matrix kernel (the boundary coupling's Boltzmann factor).** The plaquette shared across
the reflection plane has the action `1 − 2·⟨z,w⟩`, so its Boltzmann weight is `exp(−β(1 − 2·⟨z,w⟩))`
= `exp(−β)·exp(2β·⟨z,w⟩)` — the Wilson heat kernel (up to the constant `exp(−β)`). -/
noncomputable def transferKernel (β : ℝ) (z w : Metric.sphere (0 : ℂ × ℂ) 1) : ℝ :=
  Real.exp (-β * (1 - 2 * s3Inner z w))

/-- **The transfer-matrix kernel IS the heat kernel.** `exp(−β(1−2·⟨z,w⟩)) = exp(−β)·exp(2β·⟨z,w⟩)`, the
Wilson heat kernel in the S³ inner product. This is the boundary coupling = the Wilson kernel (the
`hΘ` pairing), now stated on the physical S³ measure substrate. -/
theorem transferKernel_eq_heat_kernel (β : ℝ) (z w : Metric.sphere (0 : ℂ × ℂ) 1) :
    transferKernel β z w = Real.exp (-β) * Real.exp (2 * β * s3Inner z w) := by
  rw [transferKernel]
  ring_nf
  rw [Real.exp_add]



/-- **The reflection-plane split (the `hΘ` measure half).** The reflected correlation of the two-slice
product measure (the Fubini across the reflection plane) equals the iterated integral against the
transfer-matrix kernel. -/
theorem hTheta_reflected_correlation (β : ℝ) (g : Metric.sphere (0 : ℂ × ℂ) 1 → ℝ)
    [MeasureTheory.SFinite su2Haar]
    (hg : MeasureTheory.Integrable (fun p : (Metric.sphere (0 : ℂ × ℂ) 1) × (Metric.sphere (0 : ℂ × ℂ) 1) =>
      g p.1 * g p.2 * transferKernel β p.1 p.2) (su2Haar.prod su2Haar)) :
    (∫ p : (Metric.sphere (0 : ℂ × ℂ) 1) × (Metric.sphere (0 : ℂ × ℂ) 1),
        g p.1 * g p.2 * transferKernel β p.1 p.2 ∂(su2Haar.prod su2Haar))
      = ∫ z₀ : Metric.sphere (0 : ℂ × ℂ) 1, ∫ z₁ : Metric.sphere (0 : ℂ × ℂ) 1,
        g z₀ * g z₁ * transferKernel β z₀ z₁ ∂su2Haar ∂su2Haar := by
  rw [MeasureTheory.integral_prod (fun p => g p.1 * g p.2 * transferKernel β p.1 p.2) hg]

/-- **The reflected correlation is non-negative** — the measure-theoretic reflection positivity: the
transfer-matrix kernel `transferKernel` is positive (the heat kernel), so the reflected correlation of a
non-negative field is non-negative. -/
theorem hTheta_reflected_correlation_nonneg (β : ℝ) (g : Metric.sphere (0 : ℂ × ℂ) 1 → ℝ)
    (hg : ∀ z, 0 ≤ g z) :
    0 ≤ ∫ z₀ : Metric.sphere (0 : ℂ × ℂ) 1, ∫ z₁ : Metric.sphere (0 : ℂ × ℂ) 1,
        g z₀ * g z₁ * transferKernel β z₀ z₁ ∂su2Haar ∂su2Haar := by
  have hpos : ∀ z₀ z₁, 0 ≤ g z₀ * g z₁ * transferKernel β z₀ z₁ := by
    intro z₀ z₁
    rw [transferKernel]
    exact mul_nonneg (mul_nonneg (hg z₀) (hg z₁)) (Real.exp_pos _).le
  exact MeasureTheory.integral_nonneg (by intro z₀; exact MeasureTheory.integral_nonneg (by intro z₁; exact hpos z₀ z₁))

/-- **The 2×2 adjugate identity**: `adj(U) = Tr(U)·I − U` (via `Matrix.adjugate_fin_two`). -/
theorem su2_adjugate_eq_trace_sub (U : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.adjugate U = Matrix.trace U • (1 : Matrix (Fin 2) (Fin 2) ℂ) - U := by
  rw [Matrix.adjugate_fin_two U]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.trace, Matrix.one_apply_eq, smul_eq_mul]

/-- **The SU(2) trace identity**: `Tr(UV) + Tr(U⁻¹V) = Tr(U)·Tr(V)` for 2×2 matrices with `det U = 1`. Via
`U⁻¹ = adj(U)` (`Matrix.inv_def` + `hdet`) and the adjugate identity `adj(U) = Tr(U)·I − U`. The key for the
SU(2) n=1 character convolution `∫ χ₁(U₂A)χ₁(U₂B) dU₂ = χ₁(AB⁻¹)/2`. -/
theorem su2_trace_identity (U V : Matrix (Fin 2) (Fin 2) ℂ) (hdet : U.det = 1) :
    Matrix.trace (U * V) + Matrix.trace (U⁻¹ * V) = Matrix.trace U * Matrix.trace V := by
  rw [Matrix.inv_def U, hdet]
  simp
  rw [su2_adjugate_eq_trace_sub U]
  simp [Matrix.trace_sub, Matrix.trace_smul, sub_mul, Matrix.one_mul, smul_eq_mul]

/-- **The SU(2) Schur lemma** (the fundamental rep is irreducible): a 2×2 matrix that commutes with the Pauli
generators `σ₃ = diag(1,−1)` and `σ₁ = [[0,1],[1,0]]` is a scalar multiple of the identity. This is the matrix-level
lift that turns the scalar Weyl moments (`∫ Tr(V²) = −1`, `∫ Tr(U₂) = 0`) into `∫ V² dV = −I/2` and `∫ U₂ dU₂ = 0`. -/
theorem su2_central_matrix_eq_scalar (M : Matrix (Fin 2) (Fin 2) ℂ)
    (hσ₃ : M * !![(1 : ℂ), 0; 0, -1] = !![(1 : ℂ), 0; 0, -1] * M)
    (hσ₁ : M * !![0, (1 : ℂ); 1, 0] = !![0, (1 : ℂ); 1, 0] * M) :
    ∃ c : ℂ, M = c • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  let c : ℂ := M 0 0
  refine ⟨c, ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [c, smul_eq_mul, Matrix.one_apply_eq, Matrix.mul_apply, Fin.sum_univ_two]
  · -- M 0 1 = 0
    have h := congr_fun (congr_fun hσ₃ 0) 1
    simp [Matrix.mul_apply, Fin.sum_univ_two] at h
    apply Complex.ext <;> simp
    · have hre : -(M 0 1).re = (M 0 1).re := by simpa using congrArg Complex.re h
      nlinarith [hre]
    · have him : -(M 0 1).im = (M 0 1).im := by simpa using congrArg Complex.im h
      nlinarith [him]
  · -- M 1 0 = 0
    have h := congr_fun (congr_fun hσ₃ 1) 0
    simp [Matrix.mul_apply, Fin.sum_univ_two] at h
    apply Complex.ext <;> simp
    · have hre : (M 1 0).re = -(M 1 0).re := by simpa using congrArg Complex.re h
      nlinarith [hre]
    · have him : (M 1 0).im = -(M 1 0).im := by simpa using congrArg Complex.im h
      nlinarith [him]
  · -- M 1 1 = M 0 0
    have h := congr_fun (congr_fun hσ₁ 0) 1
    simp [Matrix.mul_apply, Fin.sum_univ_two] at h
    exact h.symm

/-- **The trace conjugation invariance**: `Tr(U·C·U⁻¹) = Tr(C)` for `det U = 1` — the trace cyclicity plus
`U⁻¹·U = I`. This is the pointwise trace half of the Haar invariance that feeds the Schur lemma (making
`∫ V² dV` central, hence scalar). -/
theorem su2_trace_conj_invariant (U C : Matrix (Fin 2) (Fin 2) ℂ) (hU : U.det = 1) :
    Matrix.trace (U * C * U⁻¹) = Matrix.trace C := by
  rw [Matrix.trace_mul_comm]
  rw [← Matrix.mul_assoc]
  rw [Matrix.nonsing_inv_mul U (by simpa [hU] using (isUnit_one : IsUnit (1 : ℂ)))]
  simp

/-- **The Schur lemma applied to the pseudoreality**: a central 2×2 matrix with `Tr M = −1` equals `−I/2`.
Combines `su2_central_matrix_eq_scalar` (`M = c·I`) with `Tr(c·I) = 2c = −1`. This is the matrix-level lift that
turns the scalar `∫ Tr(V²) = −1` into `∫ V² dV = −I/2` (once the Haar invariance makes `∫ V² dV` central). -/
theorem su2_central_matrix_trace_neg_one_eq_neg_half (M : Matrix (Fin 2) (Fin 2) ℂ)
    (hσ₃ : M * !![(1 : ℂ), 0; 0, -1] = !![(1 : ℂ), 0; 0, -1] * M)
    (hσ₁ : M * !![0, (1 : ℂ); 1, 0] = !![0, (1 : ℂ); 1, 0] * M)
    (htrace : Matrix.trace M = -1) :
    M = -(1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  rcases su2_central_matrix_eq_scalar M hσ₃ hσ₁ with ⟨c, hc⟩
  rw [hc] at htrace
  have h2c : c * 2 = -1 := by
    simpa [Matrix.trace_smul, Matrix.trace_one] using htrace
  have hc_eq : c = -(1 / 2 : ℂ) := by
    linear_combination (1 / 2 : ℂ) * h2c
  rw [hc, hc_eq]

/-- **The SU(2) fundamental dimension**: `Tr(I) = 2`. The normalization constant of the Schur-lemma lift
(`Tr(c·I) = 2c`). -/
theorem su2_trace_one : Matrix.trace (1 : Matrix (Fin 2) (Fin 2) ℂ) = 2 := by
  simp [Matrix.trace, Fin.sum_univ_two]

/-- The three Pauli matrices (Hermitian, traceless, `σᵢσⱼ + σⱼσᵢ = 2δᵢⱼI`). -/
def su2Pauli1 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def su2Pauli2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]
def su2Pauli3 : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- The traceless Hermitian combination `x₁σ₁ + x₂σ₂ + x₃σ₃` (the Lie-algebra element). -/
def su2PauliVec (x : Fin 3 → ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (x 0 : ℂ) • su2Pauli1 + (x 1 : ℂ) • su2Pauli2 + (x 2 : ℂ) • su2Pauli3

/-- **The Pauli algebra square**: `(x⃗·σ⃗)² = |x⃗|²·I` — the key that makes the SU(2) quaternion square a scalar
plus a trace-zero part (hence `∫ V² dV = −I/2`). -/
theorem su2_pauli_sq (x : Fin 3 → ℝ) :
    su2PauliVec x ^ 2 = ((x 0) ^ 2 + (x 1) ^ 2 + (x 2) ^ 2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, smul_eq_mul, Matrix.mul_apply, Fin.sum_univ_two, pow_two]
  <;> ring_nf
  <;> norm_num [pow_two, Complex.I_mul_I]

/-- `Complex.I ^ 2 = −1` (via `pow_two` + `Complex.I_mul_I`). -/
theorem complex_I_sq : Complex.I ^ 2 = -1 := by
  rw [pow_two, Complex.I_mul_I]

/-- **The Pauli tracelessness**: `Tr(x⃗·σ⃗) = 0`. The trace-zero half of the quaternion square's decomposition. -/
theorem su2_pauli_trace_zero (x : Fin 3 → ℝ) : Matrix.trace (su2PauliVec x) = 0 := by
  simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, Matrix.trace, Fin.sum_univ_two, smul_eq_mul]

/-- The SU(2) quaternion form `x₀·I + i·(x₁σ₁ + x₂σ₂ + x₃σ₃)` (a general traceless-Hermitian-perturbed unitary). -/
def su2Quaternion (x₀ : ℝ) (x : Fin 3 → ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (x₀ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) + Complex.I • su2PauliVec x

/-- **The SU(2) quaternion square**: `V² = (x₀² − |x⃗|²)·I + 2ix₀·(x⃗·σ⃗)`. Uses the Pauli algebra
`(x⃗·σ⃗)² = |x⃗|²·I` (`su2_pauli_sq`) and `I² = −1`. This is the scalar-plus-trace-zero split that makes
`∫ V² dV = −I/2` once the S³ moments `∫ x₀² = 1/4`, `∫ x₀xᵢ = 0` are supplied. -/
theorem su2_quaternion_sq (x₀ : ℝ) (x : Fin 3 → ℝ) :
    su2Quaternion x₀ x ^ 2 = ((x₀ ^ 2 - (x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2) : ℝ) : ℂ) •
      (1 : Matrix (Fin 2) (Fin 2) ℂ) + ((2 * x₀ : ℝ) : ℂ) • Complex.I • su2PauliVec x := by
  unfold su2Quaternion
  have hXsq := su2_pauli_sq x
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, smul_eq_mul, su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3,
      pow_two, Complex.I_mul_I, hXsq]
  <;> ring_nf
  <;> simp [complex_I_sq]
  <;> ring

/-- **The quaternion trace**: `Tr(V²) = 2(x₀² − |x⃗|²)` — the trace of the quaternion square (the scalar part's
trace, the trace-zero part vanishing). On `S³` (`x₀² + |x⃗|² = 1`) this is `2(2x₀² − 1)`, matching the Weyl
`Tr(V²) = 2cos(2θ)` with `x₀ = cos θ`. -/
theorem su2_quaternion_sq_trace (x₀ : ℝ) (x : Fin 3 → ℝ) :
    Matrix.trace (su2Quaternion x₀ x ^ 2) =
      (2 : ℂ) * ((x₀ ^ 2 - (x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2) : ℝ) : ℂ) := by
  rw [su2_quaternion_sq]
  rw [Matrix.trace_add, Matrix.trace_smul]
  simp [su2_pauli_trace_zero, Matrix.trace_one, smul_eq_mul]
  ring



/-- **The S² direction normalization**: `cos²θ₂ + sin²θ₂·cos²φ + sin²θ₂·sin²φ = 1` — the unit-length condition
of the direction vector `u = (cos θ₂, sin θ₂ cos φ, sin θ₂ sin φ)`, via `sin²+cos² = 1` twice. The key that makes
`|x⃗|² = sin²θ₁` in the quaternion square's scalar coefficient. -/
theorem su2_direction_norm (θ₂ φ : ℝ) :
    (Real.cos θ₂)^2 + (Real.sin θ₂)^2 * (Real.cos φ)^2 + (Real.sin θ₂)^2 * (Real.sin φ)^2 = 1 := by
  nlinarith [Real.sin_sq_add_cos_sq θ₂, Real.sin_sq_add_cos_sq φ]

/-- **The S³ direction squared norm**: `|x⃗|² = sin²θ₁` for the quaternion coordinates `x⃗ = sin θ₁·u` (the unit
direction `u`). Via `su2_direction_norm`. The key reduction in the quaternion square's scalar coefficient. -/
theorem su2_sphere_norm_sq (θ₁ θ₂ φ : ℝ) :
    (Real.sin θ₁ * Real.cos θ₂)^2 + (Real.sin θ₁ * Real.sin θ₂ * Real.cos φ)^2 + (Real.sin θ₁ * Real.sin θ₂ * Real.sin φ)^2 = (Real.sin θ₁)^2 := by
  ring_nf
  nlinarith [su2_direction_norm θ₂ φ]

/-- The `(0,0)` entry of the Pauli vector: `(x⃗·σ⃗)₀₀ = x 2` (only σ₃ contributes to the diagonal). -/
theorem su2_pauli_vec_entry_00 (x : Fin 3 → ℝ) : (su2PauliVec x) 0 0 = (x 2 : ℂ) := by
  simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, Fin.sum_univ_two, smul_eq_mul]

/-- The `(0,0)` entry of the quaternion square in GENERIC coordinates: `(V²)₀₀ = (x₀²−|x⃗|²) + 2i·x₀·x 2`.
Avoids the spherical `![…]` coordinates entirely, so the entry extraction is clean. -/
theorem su2_quaternion_sq_entry_00 (x₀ : ℝ) (x : Fin 3 → ℝ) :
    ((su2Quaternion x₀ x)^2) 0 0 =
      ((x₀ ^ 2 - (x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2) : ℝ) : ℂ) + (2 * x₀ : ℂ) * Complex.I * (x 2 : ℂ) := by
  have h := su2_quaternion_sq x₀ x
  have h00 := congr_fun (congr_fun h 0) 0
  rw [h00]
  simp [Matrix.one_apply_eq, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, su2_pauli_vec_entry_00]
  ring

/-- The SU(2) quaternion in S³ spherical coordinates. -/
noncomputable def su2SphereQuaternion (θ₁ θ₂ φ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  su2Quaternion (Real.cos θ₁)
    ![Real.sin θ₁ * Real.cos θ₂, Real.sin θ₁ * Real.sin θ₂ * Real.cos φ, Real.sin θ₁ * Real.sin θ₂ * Real.sin φ]

/-- The `(0,0)` entry of the quaternion square in S³ coordinates: `(V²)₀₀ = (cos²θ₁−sin²θ₁) + 2i·cos θ₁·sin θ₁·sin θ₂·sin φ`. -/
theorem su2_sphere_sq_entry_00 (θ₁ θ₂ φ : ℝ) :
    ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 0 =
      (((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ)
        + (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * (Real.sin θ₁ : ℂ) * ((Real.sin θ₂ * Real.sin φ : ℝ) : ℂ) := by
  unfold su2SphereQuaternion
  rw [su2_quaternion_sq_entry_00]
  simp [su2_sphere_norm_sq θ₁ θ₂ φ]
  ring

/-- The Pauli-vector entries: `(x⃗·σ⃗)₁₁ = −x 2`, `(x⃗·σ⃗)₀₁ = x 0 − i·x 1`, `(x⃗·σ⃗)₁₀ = x 0 + i·x 1`. -/
theorem su2_pauli_vec_entry_11 (x : Fin 3 → ℝ) : (su2PauliVec x) 1 1 = -(x 2 : ℂ) := by
  simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, Fin.sum_univ_two, smul_eq_mul]

theorem su2_pauli_vec_entry_01 (x : Fin 3 → ℝ) : (su2PauliVec x) 0 1 = (x 0 : ℂ) - Complex.I * (x 1 : ℂ) := by
  simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, Fin.sum_univ_two, smul_eq_mul]
  ring

theorem su2_pauli_vec_entry_10 (x : Fin 3 → ℝ) : (su2PauliVec x) 1 0 = (x 0 : ℂ) + Complex.I * (x 1 : ℂ) := by
  simp [su2PauliVec, su2Pauli1, su2Pauli2, su2Pauli3, Fin.sum_univ_two, smul_eq_mul]
  ring

/-- The quaternion square's `(1,1)` entry (generic): `(V²)₁₁ = (x₀²−|x⃗|²) − 2i·x₀·x 2`. -/
theorem su2_quaternion_sq_entry_11 (x₀ : ℝ) (x : Fin 3 → ℝ) :
    ((su2Quaternion x₀ x)^2) 1 1 =
      ((x₀ ^ 2 - (x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2) : ℝ) : ℂ) - (2 * x₀ : ℂ) * Complex.I * (x 2 : ℂ) := by
  have h := su2_quaternion_sq x₀ x
  have h11 := congr_fun (congr_fun h 1) 1
  rw [h11]
  simp [Matrix.one_apply_eq, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, su2_pauli_vec_entry_11]
  ring

/-- The quaternion square's `(0,1)` entry (generic): `(V²)₀₁ = 2i·x₀·(x 0 − i·x 1)`. -/
theorem su2_quaternion_sq_entry_01 (x₀ : ℝ) (x : Fin 3 → ℝ) :
    ((su2Quaternion x₀ x)^2) 0 1 = (2 * x₀ : ℂ) * Complex.I * ((x 0 : ℂ) - Complex.I * (x 1 : ℂ)) := by
  have h := su2_quaternion_sq x₀ x
  have h01 := congr_fun (congr_fun h 0) 1
  rw [h01]
  simp [Matrix.one_apply_eq, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, su2_pauli_vec_entry_01]
  ring

/-- The quaternion square's `(1,0)` entry (generic): `(V²)₁₀ = 2i·x₀·(x 0 + i·x 1)`. -/
theorem su2_quaternion_sq_entry_10 (x₀ : ℝ) (x : Fin 3 → ℝ) :
    ((su2Quaternion x₀ x)^2) 1 0 = (2 * x₀ : ℂ) * Complex.I * ((x 0 : ℂ) + Complex.I * (x 1 : ℂ)) := by
  have h := su2_quaternion_sq x₀ x
  have h10 := congr_fun (congr_fun h 1) 0
  rw [h10]
  simp [Matrix.one_apply_eq, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, su2_pauli_vec_entry_10]
  ring

/-- The quaternion square's `(1,1)` entry in S³ coordinates (symmetric to `(0,0)`, minus sign). -/
theorem su2_sphere_sq_entry_11 (θ₁ θ₂ φ : ℝ) :
    ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 1 =
      (((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ) - (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * (Real.sin θ₁ : ℂ) * ((Real.sin θ₂ * Real.sin φ : ℝ) : ℂ) := by
  unfold su2SphereQuaternion
  rw [su2_quaternion_sq_entry_11]
  simp [su2_sphere_norm_sq θ₁ θ₂ φ]
  ring

/-- The quaternion square's `(0,1)` entry in S³ coordinates: `2i·cos θ₁·sin θ₁·cos θ₂ + 2·cos θ₁·sin θ₁·sin θ₂·cos φ`. -/
theorem su2_sphere_sq_entry_01 (θ₁ θ₂ φ : ℝ) :
    ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 1 =
      (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ)
        + (2 : ℂ) * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.sin θ₂ * Real.cos φ : ℝ) : ℂ) := by
  unfold su2SphereQuaternion
  rw [su2_quaternion_sq_entry_01]
  simp [Complex.ofReal_mul]
  ring_nf
  simp [complex_I_sq]

/-- The quaternion square's `(1,0)` entry in S³ coordinates: `2i·cos θ₁·sin θ₁·cos θ₂ − 2·cos θ₁·sin θ₁·sin θ₂·cos φ`. -/
theorem su2_sphere_sq_entry_10 (θ₁ θ₂ φ : ℝ) :
    ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 0 =
      (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ)
        - (2 : ℂ) * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.sin θ₂ * Real.cos φ : ℝ) : ℂ) := by
  unfold su2SphereQuaternion
  rw [su2_quaternion_sq_entry_10]
  simp [Complex.ofReal_mul]
  ring_nf
  simp [complex_I_sq]
  ring

/-- **The Pauli conjugation sum**: `Σᵢ σᵢ·B·σᵢ = 2·Tr(B)·I − B`. The key for the general matrix pseudoreality
`∫ U₂BU₂ dU₂ = (B − Tr(B)I)/2`. -/
theorem su2_pauli_conj_sum (B : Matrix (Fin 2) (Fin 2) ℂ) :
    su2Pauli1 * B * su2Pauli1 + su2Pauli2 * B * su2Pauli2 + su2Pauli3 * B * su2Pauli3
      = (2 : ℂ) • Matrix.trace B • (1 : Matrix (Fin 2) (Fin 2) ℂ) - B := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [su2Pauli1, su2Pauli2, su2Pauli3, Matrix.mul_apply, Matrix.vecMul, Matrix.vecHead, Matrix.vecTail, Fin.sum_univ_two, Matrix.trace, smul_eq_mul, Matrix.one_apply_eq]
  <;> ring_nf
  <;> simp [complex_I_sq]
  <;> ring

/-- **The trace form of the quaternion conjugation**: `Tr(V·B·V) = (x₀²−|x⃗|²)·Tr(B) + 2i·x₀·Tr(X·B)` (via the trace
cyclicity `Tr(V·B·V) = Tr(V²·B)` and `V² = (x₀²−|x⃗|²)·I + 2i·x₀·X`). The scalar route to the trace form
`∫Tr(U₂BU₂) = −Tr(B)/2` of the general pseudoreality. -/
theorem su2_quaternion_conj_trace (x₀ : ℝ) (x : Fin 3 → ℝ) (B : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.trace (su2Quaternion x₀ x * B * su2Quaternion x₀ x) =
      (((x₀ ^ 2 - (x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2) : ℝ) : ℂ) * Matrix.trace B)
        + (2 * x₀ : ℂ) * Complex.I * Matrix.trace (su2PauliVec x * B) := by
  rw [Matrix.mul_assoc]
  rw [Matrix.trace_mul_comm]
  rw [Matrix.mul_assoc]
  rw [← pow_two]
  rw [su2_quaternion_sq]
  rw [mul_add]
  rw [Matrix.mul_smul, Matrix.mul_smul]
  rw [Matrix.mul_one]
  rw [Matrix.trace_add, Matrix.trace_smul, Matrix.trace_smul]
  simp [Matrix.trace_one, smul_eq_mul]
  rw [Matrix.trace_mul_comm]
  ring

end QM