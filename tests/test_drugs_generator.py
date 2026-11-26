"""The molecule generator: propose → falsify, and the validity oracle rejects a bad molecule."""
import unittest

from pacland.drugs.generator import extract_features, falsify, generate_candidates


class TestMoleculeGenerator(unittest.TestCase):
    def test_valid_molecule_survives(self):
        ok, _ = falsify(extract_features("CC(=O)Oc1ccccc1C(=O)O"))  # aspirin
        self.assertTrue(ok)

    def test_pentavalent_carbon_is_dropped(self):
        ok, evidence = falsify(extract_features("C(C)(C)(C)(C)(C)"))
        self.assertFalse(ok)
        self.assertIn("invalid", evidence)

    def test_generate_candidates_is_deterministic(self):
        a = generate_candidates(6, seed=0)
        b = generate_candidates(6, seed=0)
        self.assertEqual([c.smiles for c in a], [c.smiles for c in b])
        self.assertEqual(len(a), 6)


if __name__ == "__main__":
    unittest.main()
