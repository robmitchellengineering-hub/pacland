"""The impostor count: the coarse observables are degenerate, the spectrum is not."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("od", ROOT / "scripts" / "observable_degeneracy.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


def fake(nflux=7, v=1e-18, dw=5e21, masses=(1e-60, 1e-59, 1e-58)):
    return {"flux": [1.0] * 12, "Nflux": nflux, "V": v, "|DW|": dw, "eigenvalues": list(masses)}


class TestImpostorCount(unittest.TestCase):

    def test_the_same_observables_give_the_same_signature(self):
        m = _module()
        self.assertEqual(m.signature(fake(), False), m.signature(fake(), False))

    def test_a_different_nflux_gives_a_different_signature(self):
        m = _module()
        self.assertNotEqual(m.signature(fake(nflux=7), False), m.signature(fake(nflux=8), False))

    def test_masses_enter_the_signature_only_when_asked(self):
        m = _module()
        a = fake(masses=(1e-60, 1e-59, 1e-58))
        b = fake(masses=(1e-70, 1e-69, 1e-68))
        self.assertEqual(m.signature(a, False), m.signature(b, False))
        self.assertNotEqual(m.signature(a, True), m.signature(b, True))

    def test_a_small_relative_change_is_the_same_signature(self):
        # the bins are relative, so a 1e-6 change in V is not a new observation
        m = _module()
        self.assertEqual(m.signature(fake(v=1e-18), False), m.signature(fake(v=1.000001e-18), False))


if __name__ == "__main__":
    unittest.main()
