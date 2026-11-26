"""The sharper animals bound holds across the graph family (the first cross-field verification)."""
import unittest

from pacland.cross_field.connected_subgraphs import (
    animals_bound,
    count_connected,
    graph_families,
    sharper_bound,
    verify,
)


class TestSharperAnimalsBound(unittest.TestCase):
    def test_sharper_bound_holds_everywhere(self):
        r = verify()
        self.assertEqual(r["sharper_bound_failures"], 0,
                         "the sharper bound failed on a tested graph")
        self.assertEqual(r["original_bound_failures"], 0)

    def test_sharper_is_tighter_than_original(self):
        # on a path, the sharper bound sits between the exact count and the original bound
        n_vertices, edges = 8, [(i, i + 1) for i in range(7)]
        exact = count_connected(n_vertices, edges, 4)
        self.assertLess(exact, sharper_bound(8, 4, 2))
        self.assertLess(sharper_bound(8, 4, 2), animals_bound(8, 4, 2))

    def test_exact_counts_are_reproducible(self):
        # a path's connected subgraphs of size n are the contiguous segments: V - n + 1
        n_vertices, edges = 8, [(i, i + 1) for i in range(7)]
        self.assertEqual(count_connected(n_vertices, edges, 3), 6)

    def test_families_are_well_formed(self):
        for name, (v, e) in graph_families():
            self.assertGreater(v, 0, name)
            self.assertTrue(all(0 <= a < v and 0 <= b < v for a, b in e), name)


if __name__ == "__main__":
    unittest.main()
