import PaclandProof.Tactic.CayleyRuleSet
import PaclandProof.QM.CayleyGeneral

/-! The Cayley permutation lemmas as `aesop` rules, so `aesop (rule_sets := [Cayley])`
(and the `complete` battery) can use the project's own lemmas mechanically. -/

attribute [aesop (rule_sets := [Cayley]) norm] QM.reverseZeroCycle_support
attribute [aesop (rule_sets := [Cayley]) norm] QM.reverseZeroCycle_cycleOf_zero
attribute [aesop (rule_sets := [Cayley]) norm] QM.reverseZeroCycle_involution
attribute [aesop (rule_sets := [Cayley]) norm] QM.sign_inv_eq_sign
attribute [aesop (rule_sets := [Cayley]) norm] QM.sign_odd_cycle_eq_one
