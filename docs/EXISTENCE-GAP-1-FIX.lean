import PublicTheory
import ChallengeSpec

/-!
# DRAFT — strengthen the running-coupling condition (closes existence Gap 1)

The committee's `WilsonRegularity.running` (ChallengeSpec.lean) only requires
`β/log(1/mesh) → slope` for SOME positive `slope`. That leaves the slope free, so the continuum limit is
not tied to Yang–Mills — Clay's clause 2 ("short-distance correlations agree with asymptotic freedom")
demands the slope be the beta-function coefficient, whose group-theoretic factor is the quadratic
Casimir `C₂(G)`.

This file DRAFTS the strengthened statement, for expert review. It is NOT a proof and is NOT compiled
here (it needs the committee checkout, Lean v4.32). The scheme-dependent numeric coefficient is left as
a free `c`; only the GROUP-theoretic factor (the Casimir) is pinned, because that is what is
scheme-independent and what distinguishes one gauge group from another.

STATUS: statement draft only. The three fields `continuous`/`invariant`/`localSupport` are copied
verbatim from the committee's `WilsonRegularity`; only `running` is strengthened.
-/

set_option autoImplicit false
noncomputable section

namespace YangMills

open Function Filter Set
open scoped Topology BigOperators

/-- The quadratic Casimir of a compact simple gauge group — the group-theoretic factor in the
one-loop beta function. For pure Yang–Mills, `b₀ = (11/3)·C₂(adjoint)`; in the fundamental
representation `C₂(SU(n)) = (n²−1)/(2n)`. This is what pins the running to the gauge group. -/
class HasCasimir (g : GaugeGroup) where
  casimir : ℝ
  casimir_pos : 0 < casimir

/-- **The strengthened running condition.** The slope is `c·C₂(g)` for some scheme-dependent `c > 0`:
the group-theoretic factor is pinned (it is `C₂(g)`, the Casimir), while the scheme-dependent numeric
coefficient `c` stays free — because "MS-bar matching" is out of scope and the *numeric* slope is
scheme-dependent. This is the honest strengthening that ties the limit to Yang–Mills without
over-committing to a scheme. -/
structure WilsonRegularityPinned {g : GaugeGroup} [HasCasimir g] (C : WilsonFamily g) : Prop where
  running : ∃ c : ℝ, 0 < c ∧ ∀ ε : ℝ, 0 < ε →
    ∀ᶠ N : ℕ in atTop, ∀ p,
      |C.beta N p / Real.log (C.mesh N)⁻¹ - c * HasCasimir.casimir g| < ε
  continuous (N p v x) : Continuous (C.insertion N p v x)
  invariant (N p v x) (t : Site (C.period p * C.denominator N) → g.image) (U) :
    C.insertion N p v x (fun e => t e.1 * U e * (t (e.1 + Pi.single e.2 1))⁻¹) =
      C.insertion N p v x U
  localSupport (v : C.Token) : ∃ stencil : Finset (Axis → ℤ), ∀ N p (x : Site (C.period p * C.denominator N)),
    let sites := stencil.image fun z => (fun i => (z i : ZMod (C.period p * C.denominator N).val)) + x
    ∀ U V, (∀ e, e.1 ∈ sites → e.1 + Pi.single e.2 1 ∈ sites → U e = V e) →
      C.insertion N p v x U = C.insertion N p v x V

/-- The strengthened joint target: `JointExistence` with the running pinned to the Casimir. -/
def JointExistencePinned : Prop :=
  ∀ g : GaugeGroup, g.IsSimple → ∀ hCasimir : HasCasimir g,
    ∃ C : WilsonFamily g, @WilsonRegularityPinned g hCasimir C ∧
      ∀ p : ℕ → ℕ, StrictMono p → ∃ q : ℕ → ℕ, StrictMono q ∧
        ∃ T : Hierarchy C, T.Properties (p ∘ q)

end YangMills

/-!
## REVIEW QUESTIONS (for the committee)

1. Is "slope = c·C₂(g), c scheme-dependent" the right Clay-faithful strengthening, or must the slope be
   pinned to the specific `11C₂/(48π²)` (which would re-include MS-bar matching)?
2. Should `HasCasimir` be a field on `GaugeGroup` (forcing every instance to supply it) or a typeclass
   (as drafted) so only the groups that need it carry it?
3. Does `IsSimple` alone guarantee a positive Casimir, or must `casimir_pos` be an axiom for some groups?

NOTE: this draft does NOT touch Gap 2 (the subsequence-only limit). That remains the open existence
clause and is not addressed here.
-/
