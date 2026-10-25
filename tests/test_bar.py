"""The shared bar — generic tests, including the discipline-agnostic refusals."""
import unittest

from pacland.bar import Model, REQUIRED, SLOTS, audit, audit_model, build_order, summary


def _model(**kw):
    base = dict(name="probe", kind="forecast", role="probe", exact_content="c", free="f")
    base.update(kw)
    return Model(**base)


class TestKinds(unittest.TestCase):
    def test_every_kind_owes_only_real_slots(self):
        for kind, slots in REQUIRED.items():
            for s in slots:
                self.assertIn(s, SLOTS, f"{kind} owes unknown slot {s}")

    def test_a_forecast_owes_the_whole_bar(self):
        self.assertEqual(set(REQUIRED["forecast"]), set(SLOTS))

    def test_a_statistical_model_owes_no_exact_structure(self):
        self.assertNotIn("exact_structure", REQUIRED["statistical"])


class TestTier(unittest.TestCase):
    def test_missing_slots_mean_weak(self):
        self.assertEqual(_model().tier(), "weak")

    def test_every_slot_earned_means_clean(self):
        done = frozenset(REQUIRED["forecast"])
        ev = {s: "src/pacland/bar.py" for s in done}
        ev["out_of_sample"] = "ALFRED real-time vintages"
        self.assertEqual(_model(done=done, evidence=ev).tier(), "clean")

    def test_lost_run_is_never_clean(self):
        done = frozenset(REQUIRED["forecast"])
        ev = {s: "src/pacland/bar.py" for s in done}
        ev["out_of_sample"] = "ALFRED real-time vintages"
        self.assertEqual(_model(done=done, evidence=ev, outcome="loses_to_null").tier(), "weak")


class TestAudit(unittest.TestCase):
    def test_missing_evidence_is_caught(self):
        m = _model(done=frozenset({"deficit"}))
        self.assertIn("no evidence", " ".join(audit_model(m)))

    def test_missing_file_is_caught(self):
        m = _model(done=frozenset({"deficit"}), evidence={"deficit": "src/nope.py"})
        self.assertIn("does not exist", " ".join(audit_model(m)))

    def test_out_of_sample_needs_a_vintage_source(self):
        m = _model(done=frozenset({"out_of_sample"}),
                   evidence={"out_of_sample": "src/pacland/bar.py"})
        self.assertIn("vintage", " ".join(audit_model(m)))

    def test_a_citation_is_accepted_as_evidence(self):
        m = _model(done=frozenset({"falsifiable_prediction"}),
                   evidence={"falsifiable_prediction": "Meese & Rogoff 1983"})
        self.assertEqual(audit_model(m), [])

    def test_unknown_kind_is_refused(self):
        self.assertIn("unknown kind", " ".join(audit_model(_model(kind="mystery"))))


class TestHelpers(unittest.TestCase):
    def test_summary_and_order(self):
        a = _model(name="a", priority=1)
        b = _model(name="b", priority=0)
        self.assertEqual(build_order([a, b]), ["b", "a"])
        self.assertEqual([r["name"] for r in summary([a, b])], ["a", "b"])
        self.assertEqual(audit([a, b]), [])


if __name__ == "__main__":
    unittest.main()
