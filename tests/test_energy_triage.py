"""Move 1 — the triage that turns "67 NOT-RESEARCHED" into an ordered task list.

These are tests of a decision machine, not physics. Their job is to prove the machine does the one
thing it exists for — order the unresearched cells by a *named, documented* rubric — and that it does
not smuggle in the thing it explicitly refuses: a Bayesian EIG over a space with no honest likelihood.

The honesty contract, each with a test:
  * the cell space is UNDERDETERMINED, so a full EIG ranking is refused (the C/P detector says so);
  * the order that runs instead is a structural triage with three documented inputs, all in range;
  * the head of the triage is today the C5 row (clean binary oracle, known answers) — current truth,
    to be updated the moment C5 is researched, exactly like the reason-class counts.
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.belief import Mode  # noqa: E402
from pacland.energy.lattice import CANDIDATES, CONSTRAINTS, PENDING_BOUNDS  # noqa: E402
from pacland.energy.triage import (  # noqa: E402
    COST,
    DECIDABILITY,
    DISCRIMINATION,
    LITERATURE,
    mode_c_slice,
    mode_verdict,
    researchable,
    triage,
    unresearched,
)


class TestTheTaskList(unittest.TestCase):
    def test_the_researchable_cells_exclude_the_five_not_asked(self):
        # 78 cells minus the 5 string-only C11 cells asked of no non-string candidate.
        self.assertEqual(len(researchable()), 73)

    def test_fifty_six_researchable_cells_are_unresearched(self):
        # 73 researchable minus the 17 carrying a citation (1 computed-here + 1 computed-elsewhere
        # + 11 contested + 3 no-prediction + 1 not-established).
        self.assertEqual(len(unresearched()), 56)

    def test_the_triage_covers_every_unresearched_cell_exactly_once(self):
        rows = triage()
        self.assertEqual(len(rows), 56)
        self.assertEqual({(r.candidate, r.constraint) for r in rows},
                         set(unresearched()))

    def test_the_triage_is_deterministic(self):
        self.assertEqual(triage(), triage())


class TestTheHonestyContract(unittest.TestCase):
    def test_the_cell_space_is_underdetermined_not_convergence(self):
        """No honest per-cell likelihood exists a priori, so rank_by_eig would refuse. The verdict
        is the guard that keeps the triage from pretending to be a posterior."""
        self.assertEqual(mode_verdict(), Mode.UNDERDETERMINED)

    def test_the_mode_c_slice_is_convergent_and_complete(self):
        """C3 and C5 have a clean binary oracle and a known answer: the one slice where a
        likelihood is honestly stateable. ``rank_by_eig`` raises outside Mode C, so returning
        12 results is itself the proof the slice is convergent."""
        names = [n for n, _ in mode_c_slice()]
        # C5 is now fully researched (Move 1's first pass), so only the 5 unresearched C3 cells
        # remain in the slice (asymptotic-safety/C3 is already CONTESTED).
        self.assertEqual(len(names), 5)
        self.assertTrue(all(n.endswith("C3") for n in names))

    def test_the_rubric_covers_every_constraint(self):
        ids = {c.id for c in CONSTRAINTS}
        self.assertEqual(set(DISCRIMINATION), ids)
        self.assertEqual(set(DECIDABILITY), ids)
        self.assertEqual(set(COST), ids)

    def test_the_rubric_covers_every_candidate(self):
        self.assertEqual(set(LITERATURE), {c.id for c in CANDIDATES})

    def test_the_rubric_values_are_in_range(self):
        for cid, v in DISCRIMINATION.items():
            self.assertGreaterEqual(v, 1, cid)
            self.assertLessEqual(v, 10, cid)
        for cid, v in DECIDABILITY.items():
            self.assertGreaterEqual(v, 0.0, cid)
            self.assertLessEqual(v, 1.0, cid)
        for cid, v in COST.items():
            self.assertGreater(v, 0, cid)
        for cid, v in LITERATURE.items():
            self.assertGreater(v, 0, cid)


class TestTheHeadOfTheList(unittest.TestCase):
    def test_the_head_is_the_cheapest_decisive_row_today(self):
        """Current truth: C5 was researched first (Move 1's first pass), so the head has moved to C3
        (unitarity/ghost — the constraint whose positive control, Stelle, can actually kill). The
        triage is meant to move exactly like this; update the pin each time the head is researched."""
        head = {(r.candidate, r.constraint) for r in triage()[:3]}
        self.assertEqual(head, {(c, "C3") for c in ("causal-sets", "cdt", "gft")})

    def test_the_head_is_the_self_consistent_argmax(self):
        """The ordering is by score, so the first row must be the maximum score. A regression in
        the sort would break this before it broke the current-truth pin."""
        rows = triage()
        self.assertEqual(rows[0].score, max(r.score for r in rows))

    def test_the_blocked_flag_names_the_unread_bounds(self):
        """A cell whose measured bound was never read (PENDING_BOUNDS) must be flagged, never
        silently ordered as if it could be scored."""
        for r in triage():
            self.assertEqual(r.blocked, r.constraint in PENDING_BOUNDS, (r.candidate, r.constraint))
        self.assertTrue(any(r.blocked for r in triage()), "C1 is in PENDING_BOUNDS, so someone is flagged")

    def test_the_result_is_recorded_where_it_can_be_read(self):
        doc = pathlib.Path(__file__).resolve().parents[1] / "docs" / "energy-sextant.md"
        self.assertIn("The head of the list is the next cell to research.", doc.read_text())


if __name__ == "__main__":
    unittest.main()
