"""The durable research supervisor: decomposition, allocation, retry, stopping, and durable state."""
import tempfile
import unittest
from pathlib import Path

from pacland import research_state as rs


class TestResearchState(unittest.TestCase):
    def test_decompose_creates_tasks(self):
        s = rs.ResearchState("ym-mass-gap").decompose([
            ("sub-a", "bound the string tension", 1.0),
            ("sub-b", "prove the gap survives the limit", 1.0),
        ])
        self.assertEqual(len(s.tasks), 2)
        self.assertEqual(s.next_task().id, "sub-a")

    def test_retry_exhausts_after_max_attempts(self):
        s = rs.ResearchState("p").decompose([("a", "do a", 1.0)])
        s.next_task()
        s.record_attempt("a", False, "nope")
        s.record_attempt("a", False, "nope")
        s.record_attempt("a", False, "nope")
        self.assertEqual(s.tasks[0].status, "exhausted")
        self.assertEqual(s.tasks[0].attempts, 3)

    def test_retry_retries_once_then_resolves(self):
        s = rs.ResearchState("p").decompose([("a", "do a", 1.0)])
        s.next_task()
        s.record_attempt("a", False, "first try")
        self.assertEqual(s.tasks[0].status, "pending")   # retry on a later round
        s.record_attempt("a", True, "second try")
        self.assertEqual(s.tasks[0].status, "resolved")

    def test_stops_when_all_resolved(self):
        s = rs.ResearchState("p").decompose([("a", "do a", 1.0)])
        s.next_task()
        s.record_attempt("a", True, "done")
        stopped, reason = s.should_stop()
        self.assertTrue(stopped)
        self.assertEqual(reason, "all tasks resolved")

    def test_stops_on_budget(self):
        s = rs.ResearchState("p", budget=0.1).decompose([("a", "do a", 1.0)])
        s.next_task()
        s.record_attempt("a", False, "expensive fail")
        stopped, reason = s.should_stop()
        self.assertTrue(stopped)
        self.assertEqual(reason, "budget exhausted")

    def test_state_survives_a_round_trip(self):
        s = rs.ResearchState("p").decompose([("a", "do a", 1.0)])
        s.next_task()
        s.record_attempt("a", True, "done")
        with tempfile.TemporaryDirectory() as tmp:
            p = s.save(Path(tmp) / "state.json")
            s2 = rs.ResearchState.load(p)
        self.assertEqual(s2.problem, "p")
        self.assertEqual(s2.tasks[0].status, "resolved")
        self.assertEqual(s2.tasks[0].attempts, 1)


if __name__ == "__main__":
    unittest.main()
