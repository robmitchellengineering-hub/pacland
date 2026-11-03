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
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.energy import (  # noqa: E402
    BOUND_KINDS,
    CANDIDATES,
    CONSTRAINTS,
    EVIDENCE_CLASSES,
    MACHINES,
    MEASURED,
    PENDING_BOUNDS,
    PROCEDURE,
    Constraint,
    Evidence,
    measured_constraints,
    render,
    self_test,
    summarise,
    table,
    unverified_measured,
    verdict,
    verified_bounds,
)
from pacland.energy import vacuum as V  # noqa: E402
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


class TestNoVerdictYet(unittest.TestCase):
    def test_the_whole_table_is_still_unknown(self):
        """Seven bounds or four, a verified bound makes a condition evaluable — it decides nothing."""
        s = summarise(table())
        self.assertEqual(s[KILLED], 0)
        self.assertEqual(s[SURVIVES], 0)
        self.assertEqual(s[UNKNOWN], 78)


class TestSx0Bounds(unittest.TestCase):
    """SX-0: the bounds read, and the gap named rather than left blank."""

    def test_the_pending_list_is_exactly_the_unverified_measured(self):
        self.assertEqual(set(unverified_measured()), set(PENDING_BOUNDS))

    def test_six_bounds_are_read_and_one_is_not(self):
        self.assertEqual(len(measured_constraints()), 7)
        self.assertEqual(len(verified_bounds()), 6)
        self.assertEqual(set(verified_bounds()), {"C6", "C7", "C8", "C9", "C10", "C13"})

    def test_every_verified_bound_names_a_directory_source(self):
        for cid, rec in verified_bounds().items():
            self.assertTrue(rec["source"], cid)
            self.assertRegex(rec["source"], r"arXiv:|Nature|PRL|ApJ", cid)
            self.assertEqual(rec["verified_on"], "2026-11-03", cid)

    def test_a_procedure_cannot_claim_a_verified_bound(self):
        """Unitarity is not a number; a 'verified' one would be a category error."""
        with self.assertRaises(ValueError):
            Constraint("CX", "proc", "p", "f", DERIVATION, MACHINES[0],
                       bound_kind=PROCEDURE, source="a paper", verified_on="2026-11-03")

    def test_a_procedure_is_never_described_as_a_missing_measurement(self):
        """Unitarity has no number to read; saying 'bound not verified' about it is nonsense."""
        proc = [c for c in CONSTRAINTS if c.bound_kind == PROCEDURE]
        self.assertTrue(proc)
        for c in proc:
            self.assertNotIn("bound not verified", verdict(c, None)[1], c.id)

    def test_an_unknown_bound_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            Constraint("CX", "bogus", "p", "f", DERIVATION, MACHINES[0], bound_kind="vibes")

    def test_every_constraint_declares_a_bound_kind(self):
        for c in CONSTRAINTS:
            self.assertIn(c.bound_kind, BOUND_KINDS, c.id)

    def test_the_two_microlensing_halves_are_not_overclaimed(self):
        """C10 and C13 each verify one half of their condition and say which half is missing."""
        for cid in ("C10", "C13"):
            c = next(x for x in CONSTRAINTS if x.id == cid)
            self.assertIn("NOT", c.note, f"{cid} must name the half it does not claim")


class TestVacuumEnergy(unittest.TestCase):
    """C6: arithmetic on Planck's own constants, and the dimensional error it found."""

    def test_the_ratio_is_about_1e_minus_123(self):
        self.assertAlmostEqual(V.rho_lambda_over_planck4() / 1.134e-123, 1.0, delta=0.05)

    def test_the_two_dimensionless_forms_differ_by_8pi(self):
        """rho/M_Pl^4 and Lambda/M_Pl^2 are not the same number — v0 wrote the ratio that does not exist."""
        self.assertAlmostEqual(V.lambda_over_planck2() / V.rho_lambda_over_planck4(),
                               8.0 * math.pi, delta=1e-6)


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
                       bound_kind=MEASURED, source="a primary result", verified_on="2026-11-03")
        self.assertEqual(verdict(c, None)[0], UNKNOWN)

    def test_a_failing_verifier_kills(self):
        c = Constraint("C3", "unitarity-no-ghost", "p", "f", DERIVATION, MACHINES[0],
                       bound_kind=MEASURED, source="a primary result", verified_on="2026-11-03")
        v, why = verdict(c, Evidence(False, "propagating ghost in the spectrum"))
        self.assertEqual(v, KILLED)
        self.assertIn("ghost", why)

    def test_a_passing_verifier_survives(self):
        c = Constraint("C3", "unitarity-no-ghost", "p", "f", DERIVATION, MACHINES[0],
                       bound_kind=MEASURED, source="a primary result", verified_on="2026-11-03")
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
        self.assertEqual(rows[("strings-adscft", "C11")]["reason"], "no evaluator wired for this predicate")

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
