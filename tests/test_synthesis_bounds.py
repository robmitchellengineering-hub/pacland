"""The synthesis step: harvested lemmas map to bound shapes and combine into referee-tested candidates."""
import unittest

from pacland import registry, synthesis_bounds as sb


class TestSynthesis(unittest.TestCase):
    def test_shape_maps_concepts(self):
        self.assertEqual(sb._shape("spectral gap bound")[0], "spectral-gap")
        self.assertEqual(sb._shape("exponential decay rate")[0], "exponential-decay")
        self.assertIsNone(sb._shape("unrelated algebra fact")[0])

    def test_synthesize_combines_singles_and_products(self):
        props = [
            {"payload": {"name": "a", "statement": "spectral gap", "tier": 1}},
            {"payload": {"name": "b", "statement": "exponential decay", "tier": 1}},
        ]
        cands = sb.synthesize_candidates(props)
        kinds = {c["shape"] for c in cands}
        self.assertIn("spectral-gap", kinds)
        self.assertIn("exponential-decay", kinds)
        self.assertIn("spectral-gap*exponential-decay", kinds)

    def test_generic_shapes_do_not_reach_the_mass_gap_scale(self):
        # the honest result: a constant gap or e^(-β) decay does not reach m(β)=25.28·e^(−1.182β)
        from pacland import bound_search as bs
        self.assertFalse(bs.check_bound(lambda b: 1.0)["survived"])
        self.assertFalse(bs.check_bound(lambda b: __import__("math").exp(-b))["survived"])


if __name__ == "__main__":
    unittest.main()
