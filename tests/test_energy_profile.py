"""The evaluability profile — the programme's claim, as a computation that can fail.

The claim: **every one of the six frameworks has at least one condition it cannot be evaluated on.**
This file tests that claim against the evidence record, and tests the test: if the C6 entries were
removed, two frameworks would become unblocked and the claim would fail. A check that cannot fail is
not a check.

The distinction the profile rests on:
  blocked       CONTESTED / NOT-ESTABLISHED / NO-PREDICTION — a finding about the FRAMEWORK
  computable    COMPUTED-* — a computation exists that could score the cell
  unresearched  NOT-RESEARCHED — a gap in THIS REPO, which must never be used as a blocker
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.energy import profile as P  # noqa: E402
from pacland.energy.evidence import (  # noqa: E402
    CONTESTED,
    NO_PREDICTION,
    NOT_RESEARCHED,
    class_for,
)
from pacland.energy.lattice import CANDIDATES, CONSTRAINTS  # noqa: E402


class TestTheClaim(unittest.TestCase):
    def test_every_framework_is_blocked(self):
        self.assertTrue(P.every_framework_is_blocked())

    def test_the_summary_says_six_of_six(self):
        s = P.summary()
        self.assertEqual(s["frameworks"], 6)
        self.assertEqual(s["blocked"], 6)
        self.assertEqual(s["unblocked"], [])
        self.assertTrue(s["claim_holds"])

    def test_each_framework_names_a_blocking_condition(self):
        for row in P.profile():
            self.assertTrue(row.is_blocked, row.candidate_id)
            cid, cls = row.blocker()
            self.assertIn(cls, P.BLOCKING, row.candidate_id)
            self.assertIn(cid, [c.id for c in CONSTRAINTS])


class TestTheClaimCannotBeSatisfiedByThisRepoMarkingItsOwnHomework(unittest.TestCase):
    def test_no_blocker_is_a_not_researched_cell(self):
        """'We have not looked' is not a property of the framework and must never count."""
        for row in P.profile():
            for cid, cls in row.blocked:
                self.assertNotEqual(cls, NOT_RESEARCHED, f"{row.candidate_id} x {cid}")

    def test_a_framework_with_only_unresearched_gaps_is_not_blocked(self):
        """If a framework's only non-scores were NOT-RESEARCHED, the profile must not claim it is blocked."""
        row = next(r for r in P.profile() if r.candidate_id == "strings-adscft")
        self.assertEqual(len(row.unresearched), 10)
        self.assertTrue(row.is_blocked, "strings is blocked - but by C6, a real finding, not by the gaps")

    def test_the_blocked_cells_match_the_evidence_record(self):
        expected = sum(
            1 for c in CANDIDATES for k in CONSTRAINTS
            if class_for(c.id, k.id) in P.BLOCKING
        )
        self.assertEqual(sum(len(r.blocked) for r in P.profile()), expected)


class TestTheMutation(unittest.TestCase):
    def test_without_the_c6_and_c5_entries_two_frameworks_would_be_unblocked(self):
        """The claim depends on real entries, not on the default.

        Drop the C6 *and* C5 notes for `cdt` and `gft` and those two rows become unblocked — so the
        claim would be false. That is what makes the assertion above meaningful. (Move 1's first pass
        scored C5 and added a second blocker to each, so the mutation must drop both.)
        """
        from pacland.energy import evidence as E

        reinstated = {}
        for cand in ("cdt", "gft"):
            for con in ("C6", "C5"):
                key = (cand, con)
                reinstated[key] = E.EVIDENCE.pop(key)
        try:
            self.assertFalse(P.every_framework_is_blocked())
            unblocked = [r.candidate_id for r in P.profile() if not r.is_blocked]
            self.assertEqual(sorted(unblocked), ["cdt", "gft"])
        finally:
            E.EVIDENCE.update(reinstated)
        self.assertTrue(P.every_framework_is_blocked(), "restored")


class TestRendering(unittest.TestCase):
    def test_the_table_names_all_six(self):
        out = P.render()
        for cand in CANDIDATES:
            self.assertIn(cand.id, out)

    def test_the_headline_is_six_of_six(self):
        self.assertIn("6/6 frameworks are blocked", P.render())

    def test_the_rule_about_not_researched_is_stated(self):
        self.assertIn("never counts", P.render())


if __name__ == "__main__":
    unittest.main()
