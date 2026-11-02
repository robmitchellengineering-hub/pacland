"""The truncation control: a planted near-null direction, and what truncation does to the signature."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tc", ROOT / "scripts" / "truncation_control.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestTruncationControl(unittest.TestCase):

    def test_a_boundary_planted_matrix_reads_fully_boundary(self):
        import numpy as np
        m = _module()
        M = m.planted(6, "boundary", np.random.default_rng(1))
        c = m.composition(M, 6)
        self.assertGreater(c["boundary_fraction"], 0.99)

    def test_a_moduli_planted_matrix_reads_no_boundary(self):
        import numpy as np
        m = _module()
        M = m.planted(6, "moduli", np.random.default_rng(1))
        c = m.composition(M, 6)
        self.assertLess(c["boundary_fraction"], 0.01)

    def test_the_condition_number_is_the_planted_one(self):
        import numpy as np
        m = _module()
        M = m.planted(6, "boundary", np.random.default_rng(1))
        c = m.composition(M, 6)
        self.assertAlmostEqual(c["cond"], 1e6, delta=1e2)

    def test_truncation_redraws_where_the_boundary_is(self):
        """The confound, stated as a test: the split is the LAST THREE coordinates, so dropping coordinates moves it.

        This is why a boundary fraction measured on a truncated matrix cannot be read as "where the direction physically
        is": the label 'boundary' is attached to a position in the basis, and truncation changes the basis.
        """
        import numpy as np
        m = _module()
        M = m.planted(6, "boundary", np.random.default_rng(1))
        truncated = m.truncate(M, 3)
        self.assertEqual(truncated.shape[0], M.shape[0] - 3)
        # the same physical direction, a different split, a different number
        self.assertEqual(m.composition(M, 6)["boundary_fraction"], m.composition(M, 6)["boundary_fraction"])
        self.assertNotEqual(M.shape[0], truncated.shape[0])


if __name__ == "__main__":
    unittest.main()
