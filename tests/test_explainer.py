"""Explainer content is generated from live data — not hard-coded prose."""
import unittest

from pacland.climate.explainer import content as climate_content
from pacland.drugs.explainer import content as drugs_content


def _text(entries):
    return " ".join(t for _, t in entries)


class TestExplainerContent(unittest.TestCase):
    def test_climate_pulls_real_deficit_numbers(self):
        t = _text(climate_content())
        self.assertIn("4 of 12 historical observables", t)
        self.assertIn("68%", t)

    def test_climate_pulls_real_drift_numbers(self):
        t = _text(climate_content())
        self.assertIn("12 of 19 CMIP6 models leak energy", t)
        self.assertIn("CNRM-ESM2-1", t)
        self.assertIn("1.485", t)

    def test_climate_pulls_energy_budget_numbers(self):
        t = _text(climate_content())
        self.assertIn("0.15", t)
        self.assertIn("0.01", t)

    def test_drugs_pulls_real_deficit_numbers(self):
        t = _text(drugs_content())
        self.assertIn("4 of 10 benchmark endpoints", t)
        self.assertIn("68%", t)

    def test_drugs_names_the_four_guards(self):
        t = _text(drugs_content())
        self.assertIn("4 guards", t)
        self.assertIn("Lipinski", t)


if __name__ == "__main__":
    unittest.main()
