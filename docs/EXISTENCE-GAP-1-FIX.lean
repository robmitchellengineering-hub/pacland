import PublicTheory
import ChallengeSpec

/-!
# REFINED — close Gap 1 by surfacing the Casimir-pinned slope the construction already proves

STRIP-MINE UPDATE (2026-11-18). The committee's *proof* already pins the running slope: the internal
`YM.Gauge` has `slopeConstant := 11·casimir/(24π²)` (`YM/Gauge/Colors.lean:184`), `casimir_pos : 0 < casimir`
proved from `G.Simple` alone (`YM/Gauge/Casimir.lean:160`), and `Running.slope : slopeConstant = 2·b₀` with
`b₀ = 11·C_A/(48π²)`. Only the PUBLIC `WilsonRegularity.running` weakens this to "some positive slope".

So the correct fix is NOT to invent `c·C₂` with a free `c` (the earlier draft was too weak). It is to
surface the construction's own `slopeConstant` in the public statement: the slope IS `11·casimir/(24π²)`,
the specific Casimir-pinned value the proof already establishes.

This file DRAFTS that public strengthening. Statement only, not compiled here (needs the committee checkout).
-/

set_option autoImplicit false
noncomputable section

namespace YangMills

open Function Filter Set
open scoped Topology BigOperators

/-- **Add the quadratic Casimir to the public `GaugeGroup`.** The committee's internal `YM.Gauge` derives
this from the Lie algebra (`casimir := −(Σᵢ trace(ad bᵢ ∘ ad bᵢ))/lieDim`) and proves it positive for simple
groups (`casimir_pos`). The public statement should carry the same field so the slope can be pinned. -/
-- (To be added as a field on the committee's public `GaugeGroup`, or as a typeclass for the groups that
--  supply it. The construction already proves: IsSimple ⟹ 0 < casimir.)
class HasCasimir (g : GaugeGroup) where
  casimir : ℝ
  casimir_pos : 0 < casimir

/-- **The specific slope the construction proves**: `11·casimir/(24π²)` — the Casimir-pinned one-loop
running slope (matches the committee's `slopeConstant`, and `= 2·b₀` with `b₀ = 11C_A/(48π²)`). -/
def slopeConstant (g : GaugeGroup) [HasCasimir g] : ℝ :=
  11 * HasCasimir.casimir g / (24 * Real.pi ^ 2)

/-- **The strengthened running condition**: `β/log(1/mesh) → slopeConstant` (the SPECIFIC value), not
"some positive slope". This is what the proof already establishes; the public statement should state it. -/
structure WilsonRegularityPinned {g : GaugeGroup} [HasCasimir g] (C : WilsonFamily g) : Prop where
  running : ∀ ε : ℝ, 0 < ε →
    ∀ᶠ N : ℕ in atTop, ∀ p,
      |C.beta N p / Real.log (C.mesh N)⁻¹ - slopeConstant g| < ε
  continuous (N p v x) : Continuous (C.insertion N p v x)
  invariant (N p v x) (t : Site (C.period p * C.denominator N) → g.image) (U) :
    C.insertion N p v x (fun e => t e.1 * U e * (t (e.1 + Pi.single e.2 1))⁻¹) =
      C.insertion N p v x U
  localSupport (v : C.Token) : ∃ stencil : Finset (Axis → ℤ), ∀ N p (x : Site (C.period p * C.denominator N)),
    let sites := stencil.image fun z => (fun i => (z i : ZMod (C.period p * C.denominator N).val)) + x
    ∀ U V, (∀ e, e.1 ∈ sites → e.1 + Pi.single e.2 1 ∈ sites → U e = V e) →
      C.insertion N p v x U = C.insertion N p v x V

/-- The strengthened joint target. -/
def JointExistencePinned : Prop :=
  ∀ g : GaugeGroup, g.IsSimple → ∀ hCasimir : HasCasimir g,
    ∃ C : WilsonFamily g, @WilsonRegularityPinned g hCasimir C ∧
      ∀ p : ℕ → ℕ, StrictMono p → ∃ q : ℕ → ℕ, StrictMono q ∧
        ∃ T : Hierarchy C, T.Properties (p ∘ q)

end YangMills

/-!
## REVIEW QUESTIONS (updated after strip-mine)

1. CONFIRMED: `IsSimple` ⟹ `0 < casimir` — the construction proves `casimir_pos`. No axiom needed.
2. The slope should be the SPECIFIC `11·casimir/(24π²)` (= the construction's `slopeConstant` = `2·b₀`),
   not "c·C₂ with free c" (the earlier draft was too weak) and not "some positive slope" (the public
   statement's current weakening).
3. Should `HasCasimir` be a field on `GaugeGroup` (forcing every instance) or a typeclass (as drafted)?

NOTE: Gap 2 (subsequence-only, non-unique limit) remains the open existence clause — not addressed here.
-/
