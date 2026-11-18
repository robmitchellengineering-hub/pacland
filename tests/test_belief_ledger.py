"""The belief ledger updates posteriors by evidence and converges, not flips."""
import unittest

from pacland import belief_ledger, hypotheses
from pacland.belief_ledger import BeliefLedger


class TestBeliefLedger(unittest.TestCase):
    def test_positive_evidence_raises_the_posterior(self):
        ledger = belief_ledger.BeliefLedger.from_stated()
        before = ledger.beliefs["ym-mass-gap"].prior
        after = ledger.record_result("ym-mass-gap", positive=True)
        self.assertGreater(after.prior, before)

    def test_negative_evidence_lowers_the_posterior(self):
        ledger = belief_ledger.BeliefLedger.from_stated()
        before = ledger.beliefs["ym-mass-gap"].prior
        after = ledger.record_result("ym-mass-gap", positive=False)
        self.assertLess(after.prior, before)

    def test_consistent_evidence_converges_toward_one(self):
        ledger = belief_ledger.BeliefLedger.from_stated()
        after = None
        for _ in range(5):
            after = ledger.record_result("ym-mass-gap", positive=True)
        self.assertGreater(after.prior, 0.99)

    def test_one_falsifier_hit_after_convergence_is_a_small_dip(self):
        ledger = belief_ledger.BeliefLedger.from_stated()
        for _ in range(5):
            ledger.record_result("ym-mass-gap", positive=True)
        before = ledger.beliefs["ym-mass-gap"].prior
        after = ledger.record_result("ym-mass-gap", positive=False)
        self.assertLess(after.prior, before)       # it moved down
        self.assertGreater(after.prior, 0.5)       # but did not flip-flop


class TestLedgerEig(unittest.TestCase):
    def test_rank_by_eig_covers_every_hypothesis_with_sensitivity(self):
        ledger = BeliefLedger.from_stated()
        ranked = ledger.rank_by_eig()
        self.assertEqual(len(ranked), len(hypotheses.HYPOTHESES))
        # every belief carries a likelihood (tp/fp), so EIG is sensitivity-aware, not raw entropy
        self.assertTrue(all(b.likelihood is not None for b in ledger.beliefs.values()))


if __name__ == "__main__":
    unittest.main()
