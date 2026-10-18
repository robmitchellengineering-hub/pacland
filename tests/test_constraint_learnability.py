import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.structure import ridge_cv_predictability

DATA = Path(__file__).resolve().parents[1] / "data" / "vacua_observables.json"


class TestConstraintLearnability(unittest.TestCase):
    """The real-data split: the constraint is learnable, observables are not."""

    @classmethod
    def setUpClass(cls):
        with open(DATA) as f:
            raw = json.load(f)
        cls.records = [r for d in raw.values() for r in d]
        cls.fluxes = [r["flux"] for r in cls.records]

    def test_tadpole_is_learnable(self):
        y = [r["tadpole"] for r in self.records]
        self.assertGreater(ridge_cv_predictability(self.fluxes, y), 0.9)

    def test_w0_is_not_learnable(self):
        y = [r["log_W0"] for r in self.records]
        self.assertLess(ridge_cv_predictability(self.fluxes, y), 0.3)

    def test_gs_is_not_learnable(self):
        y = [r["log_gs"] for r in self.records]
        self.assertLess(ridge_cv_predictability(self.fluxes, y), 0.3)


if __name__ == "__main__":
    unittest.main()
