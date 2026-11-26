"""The discovery graph: nodes deduplicate, edges are gated by evidence, and the seed
graph carries the mass-gap campaign with its pending transfer hypotheses."""
import unittest

from pacland.discovery_graph import DiscoveryGraph, seed_mass_gap


class TestDiscoveryGraph(unittest.TestCase):
    def test_add_node_deduplicates_by_id(self):
        g = DiscoveryGraph()
        g.add_node("x", "verified-theorem", "X")
        g.add_node("x", "methodology-discovery", "X again")
        self.assertEqual(len(g.nodes), 1)

    def test_add_node_rejects_unknown_kind(self):
        g = DiscoveryGraph()
        with self.assertRaises(ValueError):
            g.add_node("x", "not-a-kind", "X")

    def test_edge_without_evidence_is_rejected(self):
        g = DiscoveryGraph()
        g.add_node("a", "reusable-mechanism", "A")
        g.add_node("b", "transfer-hypothesis", "B")
        edge = g.add_edge("a", "b", "transfers-to", {})
        self.assertIsNone(edge)
        self.assertEqual(len(g.edges), 0)
        self.assertEqual(len(g.rejections), 1)

    def test_edge_with_evidence_is_added(self):
        g = DiscoveryGraph()
        g.add_node("a", "reusable-mechanism", "A")
        g.add_node("b", "transfer-hypothesis", "B")
        edge = g.add_edge("a", "b", "transfers-to",
                          {"target": "condensed matter", "falsifier": "no gap"})
        self.assertIsNotNone(edge)
        self.assertEqual(len(g.edges), 1)

    def test_edge_with_wrong_evidence_is_rejected(self):
        # transfers-to needs BOTH target and falsifier — a target alone fails the validator
        g = DiscoveryGraph()
        g.add_node("a", "reusable-mechanism", "A")
        g.add_node("b", "transfer-hypothesis", "B")
        edge = g.add_edge("a", "b", "transfers-to", {"target": "condensed matter"})
        self.assertIsNone(edge)
        self.assertEqual(len(g.edges), 0)

    def test_edge_rejects_wrong_type_pair(self):
        # proves needs verified-theorem -> original-result, not mechanism -> hypothesis
        g = DiscoveryGraph()
        g.add_node("a", "reusable-mechanism", "A")
        g.add_node("b", "transfer-hypothesis", "B")
        edge = g.add_edge("a", "b", "proves", {"theorem": "t", "sorry_free": True})
        self.assertIsNone(edge)
        self.assertEqual(len(g.rejections), 1)

    def test_pending_follows_the_full_chain(self):
        # a hypothesis with a verified-in edge on its application is NOT pending
        g = DiscoveryGraph()
        g.add_node("m", "reusable-mechanism", "M")
        g.add_node("h", "transfer-hypothesis", "H")
        g.add_node("app", "proposed-application", "APP")
        g.add_node("dest", "destination-verification", "DEST")
        g.add_edge("m", "h", "transfers-to", {"target": "X", "falsifier": "Y"})
        g.add_edge("h", "app", "applies-in", {"verifier": "V"})
        g.add_edge("app", "dest", "verified-in", {"passed": True})
        self.assertEqual(g.pending_hypotheses(), [])
        self.assertEqual(g.verified_hypotheses(), ["h"])

    def test_edge_endpoints_must_exist(self):
        g = DiscoveryGraph()
        with self.assertRaises(KeyError):
            g.add_edge("a", "b", "transfers-to", {})

    def test_seed_graph_is_wired(self):
        g = seed_mass_gap()
        self.assertEqual(len(g.nodes), 21)
        self.assertEqual(len(g.edges), 18)
        # the transfer hypotheses are pending — no destination has been verified yet
        self.assertEqual(len(g.pending_hypotheses()), 4)

    def test_directly_useful_vs_cross_field(self):
        g = seed_mass_gap()
        self.assertEqual(set(g.directly_useful_mechanisms()),
                         {"count_via_rooted_trees", "reduce_per_irrep", "rooted_tree_count"})
        self.assertEqual(g.non_directly_useful_mechanisms(),
                         ["locate_gap_via_positivity"])

    def test_cross_synthesize_rescues_only_non_direct_mechanisms(self):
        g = seed_mass_gap()
        mappings = [
            {"from": "markov-chain-monte-carlo", "to": "wright-fisher",
             "mapping": "a reversible Markov chain's spectral gap bounds mixing time"},
        ]
        emitted = g.cross_synthesize(mappings)
        # only the non-directly-useful mechanism gets a unification declaration
        self.assertEqual(len(emitted), 1)
        self.assertEqual(emitted[0].src, "locate_gap_via_positivity")
        self.assertEqual(emitted[0].relation, "transfers-to")

    def test_reusable_context_names_mechanisms_and_pending(self):
        g = seed_mass_gap()
        ctx = g.reusable_context()
        self.assertIn("Reusable mechanisms", ctx)
        self.assertIn("locate a gap in a spectrum via positivity", ctx)
        self.assertIn("Transfer hypotheses pending", ctx)
        self.assertIn("Anderson-model spectral gap", ctx)

    def test_save_load_round_trip(self):
        import os
        import tempfile
        g = seed_mass_gap()
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            g.save(path)
            g2 = DiscoveryGraph.load(path)
            self.assertEqual(len(g2.nodes), len(g.nodes))
            self.assertEqual(len(g2.edges), len(g.edges))
            self.assertEqual(g2.nodes["locate_gap_via_positivity"].name,
                             g.nodes["locate_gap_via_positivity"].name)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
