"""Build 3 — EIG ranking over the bold claims (the allocator)."""
import unittest

from pacland.allocator import BOLD_CLAIMS, HAND_ORDER, compare_to_hand, dispatch_order
from pacland.belief import Belief, Likelihood, Mode, detect_mode, eig, rank_by_eig


class TestDispatchOrder(unittest.TestCase):
    def test_space_is_convergence(self):
        # every claim carries a prior + likelihood + ground truth -> Mode C
        self.assertEqual(detect_mode(list(BOLD_CLAIMS)).mode, Mode.CONVERGENCE)

    def test_ranks_b4_first_then_b3_b2_b5(self):
        order = [name.split()[0] for name, _, _ in dispatch_order()]
        self.assertEqual(order, ["B4", "B3", "B2", "B5"])

    def test_b5_eig_matches_closed_form(self):
        # prior 0.5, tp 0.6, fp 0.4 -> P(+)=0.5, post(+)=0.6, post(-)=0.4
        # EIG = H(0.5) - H(0.6)
        b5 = next(b for b in BOLD_CLAIMS if b.name.startswith("B5"))
        self.assertAlmostEqual(eig(b5.prior, b5.likelihood), 0.6931471805599453 - 0.6730116670092565, places=3)

    def test_every_claim_has_positive_eig(self):
        for name, e, _ in dispatch_order():
            self.assertGreater(e, 0.0, name)


class TestCompareToHand(unittest.TestCase):
    def test_agrees_with_hand_order(self):
        self.assertIn("agrees", compare_to_hand())
        self.assertIn("['B4', 'B3', 'B2', 'B5']", compare_to_hand())


class TestAllocatorMutations(unittest.TestCase):
    def test_ranking_can_fail(self):
        # Make B4 non-discriminating: its EIG collapses to 0 and the order must change.
        claims = [
            Belief("B4 the wall is geometric, warm start multiplies reach",
                   prior=0.85, likelihood=Likelihood(0.5, 0.5), cost=0.5)
            if b.name.startswith("B4") else b
            for b in BOLD_CLAIMS
        ]
        ranked = rank_by_eig(claims)
        self.assertNotEqual([n.split()[0] for n, _ in ranked], list(HAND_ORDER))


if __name__ == "__main__":
    unittest.main()
