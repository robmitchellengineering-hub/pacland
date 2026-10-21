"""Mutation tests for the drug guard-suite (playbook item #2).

Each test proves a guard passes on a valid case AND goes red on the seeded fault
it exists to catch (KNOWN-HAZARDS H17: a check that never runs reads as a pass).
"""
import unittest

from pacland.drugs.guards import (
    guard_lipinski,
    guard_synthesizable,
    guard_total_charge_neutral,
    guard_valence_bounds,
)


class TestDrugsGuards(unittest.TestCase):
    def test_charge_passes_when_neutral(self):
        ok, _ = guard_total_charge_neutral([0, 0, -1, +1])
        self.assertTrue(ok)

    def test_charge_fires_on_net_charge(self):
        ok, msg = guard_total_charge_neutral([0, 0, -1])
        self.assertFalse(ok)
        self.assertIn("net charge", msg)

    def test_valence_passes_when_sane(self):
        ok, _ = guard_valence_bounds([("C", 4), ("N", 3), ("O", 2), ("H", 1)])
        self.assertTrue(ok)

    def test_valence_fires_on_overvalent_carbon(self):
        ok, msg = guard_valence_bounds([("C", 5), ("O", 2)])
        self.assertFalse(ok)
        self.assertIn("over-valent", msg)

    def test_lipinski_passes_within_limits(self):
        ok, _ = guard_lipinski(mw=350, logp=3.0, hbd=3, hba=6)
        self.assertTrue(ok)

    def test_lipinski_fires_on_two_plus_violations(self):
        ok, msg = guard_lipinski(mw=620, logp=6.5, hbd=4, hba=8)
        self.assertFalse(ok)
        self.assertIn("Ro5 violations=2", msg)

    def test_synthesizable_passes_low_score(self):
        ok, _ = guard_synthesizable(3.2)
        self.assertTrue(ok)

    def test_synthesizable_fires_on_hard_score(self):
        ok, msg = guard_synthesizable(9.1)
        self.assertFalse(ok)
        self.assertIn("RAScore", msg)


if __name__ == "__main__":
    unittest.main()
