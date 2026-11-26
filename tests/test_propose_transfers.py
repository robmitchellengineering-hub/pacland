"""The cross-field generator: proposes type-matched transfers with falsifiers + novelty ranking."""
import unittest

from pacland.cross_field.propose import PROBLEMS, propose_transfers


class TestProposeTransfers(unittest.TestCase):
    def test_matches_by_type_not_keyword(self):
        # connected-subgraph-count mechanism -> network-reliability (same type), not the others
        self.assertEqual([t.mechanism for t in propose_transfers("network-reliability")],
                         ["count_via_rooted_trees"])
        # spectral-gap mechanism -> the spectral-gap problems
        self.assertEqual([t.mechanism for t in propose_transfers("markov-mixing-time")],
                         ["locate_gap_via_positivity"])

    def test_known_pairs_rank_zero_novelty(self):
        ts = propose_transfers("network-reliability",
                               known_pairs={("count_via_rooted_trees", "network-reliability")})
        self.assertEqual(ts[0].novelty, 0.0)

    def test_every_proposal_carries_a_falsifier(self):
        for problem in PROBLEMS:
            for t in propose_transfers(problem):
                self.assertTrue(t.falsifier, problem)
                self.assertTrue(t.predicted_property, problem)

    def test_unknown_problem_raises(self):
        with self.assertRaises(ValueError):
            propose_transfers("not-a-problem")


if __name__ == "__main__":
    unittest.main()
