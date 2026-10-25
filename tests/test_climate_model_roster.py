"""Climate models scored on the shared bar — the transfer test."""
import unittest

from pacland.climate import model_roster as R


class TestRows(unittest.TestCase):
    def test_three_models(self):
        self.assertEqual(len(R.CLIMATE_ROSTER), 3)

    def test_no_unsupported_claim(self):
        self.assertEqual(R.audit_rows(), [])

    def test_all_are_weak_because_the_field_lacks_the_slots(self):
        rows = {r["name"]: r for r in R.summary_rows()}
        self.assertEqual(len(rows), 3)
        for row in rows.values():
            self.assertEqual(row["tier"], "weak")


class TestTheDiscriminator(unittest.TestCase):
    def test_the_clean_model_claims_the_conservation_checks(self):
        g = next(m for m in R.CLIMATE_ROSTER if m.name.endswith("GISS-E2-1-G"))
        self.assertIn("rule_of_three", g.done)
        self.assertIn("guard_suite", g.done)

    def test_the_leaking_model_cannot_claim_them(self):
        m = next(m for m in R.CLIMATE_ROSTER if "MPI" in m.name)
        self.assertNotIn("rule_of_three", m.done)
        self.assertNotIn("guard_suite", m.done)
        self.assertIn("rule_of_three", m.missing())

    def test_the_failing_model_claims_only_what_is_true_of_it(self):
        u = next(m for m in R.CLIMATE_ROSTER if "UKESM" in m.name)
        # scored on the board, reproduced, and now measured against the null — but NOT
        # credited with the conservation checks it fails
        self.assertEqual(set(u.done),
                         {"trust_entry", "reproduce", "benchmark", "out_of_sample",
                          "deficit"})


class TestTheFinding(unittest.TestCase):
    def test_the_same_two_slots_are_owed_by_every_model(self):
        f = R.transfer_finding()
        self.assertEqual(f["owed_by_every_model"],
                         ["exact_structure", "falsifiable_prediction"])

    def test_the_null_slots_are_now_claimed(self):
        for m in R.CLIMATE_ROSTER:
            self.assertIn("benchmark", m.done, m.name)
            self.assertIn("out_of_sample", m.done, m.name)

    def test_the_verdict_says_the_null_exists_and_wins(self):
        f = R.transfer_finding()
        self.assertIn("trend", f["verdict"])
        self.assertIn("per-model deficit", f["verdict"])

    def test_no_climate_row_is_clean(self):
        self.assertEqual(R.transfer_finding()["n_clean"], 0)


if __name__ == "__main__":
    unittest.main()
