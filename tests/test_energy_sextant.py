"""SEXTANT — the referee's wiring, and the three refusals it is built to make.

These are not physics tests. They are tests of a machine whose output is a verdict, and their job is to
prove the machine cannot produce the verdict the field produces too easily: "survives", from the
absence of anyone looking.

The three refusals, each with a test:
  * an unverified bound is UNKNOWN, never SURVIVES;
  * a condition with no evaluator is UNKNOWN, never SURVIVES;
  * a verified bound with no primary source cannot be constructed at all.

If any of those three ever pass silently, the table becomes decoration — so each is mutation-tested by
building the failure on purpose.
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.energy import (  # noqa: E402
    CANDIDATES,
    CONSTRAINTS,
    EVIDENCE_CLASSES,
    MACHINES,
    Constraint,
    Evidence,
    render,
    self_test,
    summarise,
    table,
    verdict,
)
from pacland.energy.lattice import ARGUMENT, DERIVATION, KILLED, SURVIVES, UNKNOWN  # noqa: E402


class TestLatticeShape(unittest.TestCase):
    def test_thirteen_conditions_six_frameworks(self):
        self.assertEqual(len(CONSTRAINTS), 13)
        self.assertEqual(len(CANDIDATES), 6)
        self.assertEqual(len(table()), 78)

    def test_ids_are_unique(self):
        self.assertEqual(len({c.id for c in CANDIDATES}), len(CANDIDATES))
        self.assertEqual(len({c.id for c in CONSTRAINTS}), len(CONSTRAINTS))

    def test_every_condition_carries_a_falsifier(self):
        for c in CONSTRAINTS:
            self.assertTrue(c.falsifier.strip(), f"{c.id} has no falsifier")

    def test_every_condition_speaks_the_repository_vocabulary(self):
        for c in CONSTRAINTS:
            self.assertIn(c.evidence_class, EVIDENCE_CLASSES, c.id)
            self.assertIn(c.machine, MACHINES, c.id)

    def test_the_six_named_frameworks_are_all_present(self):
        ids = {c.id for c in CANDIDATES}
        for expected in ("strings-adscft", "lqg-spinfoam", "asymptotic-safety", "cdt", "causal-sets", "gft"):
            self.assertIn(expected, ids)


class TestNothingIsVerifiedYet(unittest.TestCase):
    def test_the_whole_table_is_unknown_today(self):
        """The honest reading of the field, and the state this module ships in."""
        s = summarise(table())
        self.assertEqual(s[KILLED], 0)
        self.assertEqual(s[SURVIVES], 0)
        self.assertEqual(s[UNKNOWN], 78)

    def test_no_constraint_claims_a_verified_bound(self):
        for c in CONSTRAINTS:
            self.assertIsNone(c.verified_on, f"{c.id} claims a verified bound it has not read")


class TestTheThreeRefusals(unittest.TestCase):
    def test_a_verified_bound_with_no_source_cannot_exist(self):
        with self.assertRaises(ValueError):
            Constraint("CX", "bogus", "p", "f", DERIVATION, MACHINES[0],
                       source=None, verified_on="2026-11-03")

    def test_an_unverified_bound_never_survives(self):
        c = Constraint("CX", "unverified", "p", "f", DERIVATION, MACHINES[0])
        self.assertEqual(verdict(c, None)[0], UNKNOWN)

    def test_a_verified_bound_with_no_evaluator_never_survives(self):
        c = Constraint("CX", "no-evaluator", "p", "f", DERIVATION, MACHINES[0],
                       source="a primary result", verified_on="2026-11-03")
        self.assertEqual(verdict(c, None)[0], UNKNOWN)

    def test_a_failing_verifier_kills(self):
        c = Constraint("C3", "unitarity-no-ghost", "p", "f", DERIVATION, MACHINES[0],
                       source="a primary result", verified_on="2026-11-03")
        v, why = verdict(c, Evidence(False, "propagating ghost in the spectrum"))
        self.assertEqual(v, KILLED)
        self.assertIn("ghost", why)

    def test_a_passing_verifier_survives(self):
        c = Constraint("C3", "unitarity-no-ghost", "p", "f", DERIVATION, MACHINES[0],
                       source="a primary result", verified_on="2026-11-03")
        self.assertEqual(verdict(c, Evidence(True, "no ghost to one loop"))[0], SURVIVES)

    def test_an_unknown_evidence_class_is_rejected(self):
        with self.assertRaises(ValueError):
            Constraint("CX", "bogus", "p", "f", "vibes", MACHINES[0])


class TestTheHonestSpecialCases(unittest.TestCase):
    def test_the_cosmological_constant_is_not_a_kill_criterion(self):
        """No framework accounts for 1e-122; scoring it KILLED would kill all six by fiat."""
        c6 = next(c for c in CONSTRAINTS if c.id == "C6")
        self.assertEqual(c6.fails_as, UNKNOWN)
        self.assertEqual(c6.evidence_class, ARGUMENT)
        self.assertEqual(c6.machine, "NOT-TESTABLE-IN-TRUNCATION")

    def test_the_swampland_condition_is_only_asked_of_string_candidates(self):
        rows = {(r["candidate"], r["constraint"]): r for r in table()}
        self.assertIn("string", rows[("lqg-spinfoam", "C11")]["reason"])
        self.assertEqual(rows[("strings-adscft", "C11")]["reason"], "bound not verified from a primary source")

    def test_the_ghost_control_is_named(self):
        """C3 must name its own mutation control, or the kill is not demonstrable."""
        c3 = next(c for c in CONSTRAINTS if c.id == "C3")
        self.assertIn("Stelle", c3.note)


class TestRunner(unittest.TestCase):
    def test_self_test_passes(self):
        self.assertEqual(self_test(), 0)

    def test_render_names_the_cells(self):
        out = render(table())
        self.assertIn("78 cells", out)
        self.assertIn("Not a pass", out)


if __name__ == "__main__":
    unittest.main()
