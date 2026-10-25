"""Economics model-roster tests — the bar, and the refusal of the overclaim."""
import pathlib
import unittest

from pacland.economics.model_roster import (
    REQUIRED,
    ROSTER,
    SLOTS,
    SW_OBSERVABLES,
    Model,
    audit,
    audit_model,
    build_order,
    models_sorted,
    summary,
)

ROOT = str(pathlib.Path(__file__).resolve().parents[1])


class TestRosterIntegrity(unittest.TestCase):
    def test_every_model_is_described(self):
        for m in ROSTER:
            self.assertTrue(m.name and m.role and m.exact_content and m.free, m.name)

    def test_kinds_are_known_and_owed_slots_are_real(self):
        for m in ROSTER:
            self.assertIn(m.kind, REQUIRED, m.name)
            for slot in REQUIRED[m.kind]:
                self.assertIn(slot, SLOTS, f"{m.name}: owed slot {slot} not in the bar")

    def test_build_order_is_a_permutation(self):
        order = build_order()
        self.assertEqual(sorted(order), sorted(m.name for m in ROSTER))
        self.assertEqual(len(order), len(set(order)))

    def test_summary_covers_every_model(self):
        rows = summary(root=ROOT)
        self.assertEqual(len(rows), len(ROSTER))
        self.assertTrue(all(r["tier"] in {"broken", "weak", "clean"} for r in rows))


class TestNoOverclaim(unittest.TestCase):
    def test_roster_carries_no_violation(self):
        self.assertEqual(audit(ROSTER, root=ROOT), [])

    def test_clean_always_means_every_owed_slot_done(self):
        for m in ROSTER:
            if m.tier(ROOT) == "clean":
                self.assertEqual(m.missing(), (), f"{m.name} is clean but owes {m.missing()}")

    def test_claim_with_a_missing_script_is_broken(self):
        fake = Model(
            name="overclaimer",
            kind="forecast",
            role="probe",
            exact_content="asserted",
            free="none",
            done=frozenset({"exact_structure"}),
            evidence={"exact_structure": "scripts/validate_no_such_model.py"},
        )
        self.assertIn("does not exist", " ".join(audit_model(fake, ROOT)))
        self.assertEqual(fake.tier(ROOT), "broken")

    def test_claim_with_no_evidence_is_broken(self):
        fake = Model(
            name="unsupported",
            kind="oracle",
            role="probe",
            exact_content="asserted",
            free="none",
            done=frozenset({"exact_structure"}),
            evidence={},
        )
        self.assertEqual(fake.tier(ROOT), "broken")

    def test_out_of_sample_needs_a_vintage_source(self):
        # A current-vintage backtest is not an out-of-sample test (Meese–Rogoff).
        fake = Model(
            name="current-vintage",
            kind="forecast",
            role="probe",
            exact_content="none",
            free="none",
            done=frozenset({"out_of_sample"}),
            evidence={"out_of_sample": "scripts/validate_economics_forecast.py"},
        )
        self.assertIn("real-time vintage", " ".join(audit_model(fake, ROOT)))

    def test_out_of_sample_accepts_a_named_vintage_source(self):
        fake = Model(
            name="vintage-ok",
            kind="forecast",
            role="probe",
            exact_content="none",
            free="none",
            done=frozenset({"out_of_sample"}),
            evidence={"out_of_sample": "ALFRED real-time vintages, 1992–2025"},
        )
        self.assertEqual(audit_model(fake, ROOT), [])


class TestStartingSet(unittest.TestCase):
    def test_we_start_with_the_benchmark_the_oracle_and_the_small_forecast_model(self):
        self.assertEqual(
            build_order()[:3],
            [
                "random walk (no change)",
                "Godley–Lavoie SFC (SIM/SIMEX)",
                "New Keynesian 3-equation (Taylor 1993; Clarida–Galí–Gertler)",
            ],
        )

    def test_control_and_oracle_are_at_the_bar(self):
        by_name = {m.name: m for m in ROSTER}
        self.assertEqual(by_name["random walk (no change)"].tier(ROOT), "clean")
        self.assertEqual(by_name["Godley–Lavoie SFC (SIM/SIMEX)"].tier(ROOT), "clean")

    def test_nk3_earns_its_proven_slots(self):
        nk = next(m for m in ROSTER if m.name.startswith("New Keynesian"))
        for slot in ("exact_structure", "deficit", "rule_of_three", "guard_suite",
                     "falsifiable_prediction", "reproduce"):
            self.assertIn(slot, nk.done, f"NK3 does not claim {slot}")
        # ...and it does not claim what it has not done.
        self.assertEqual(set(nk.missing()), {"out_of_sample", "benchmark", "trust_entry"})

    def test_the_workhorse_forecast_model_owes_the_bar(self):
        sw = next(m for m in ROSTER if m.name.startswith("Smets–Wouters"))
        self.assertEqual(sw.kind, "forecast")
        self.assertEqual(sw.missing(), SLOTS)
        self.assertEqual(sw.tier(ROOT), "weak")


class TestSmetsWoutersObservables(unittest.TestCase):
    def test_seven_series_as_published(self):
        self.assertEqual(len(SW_OBSERVABLES), 7)

    def test_series_ids_are_unique(self):
        self.assertEqual(len(set(SW_OBSERVABLES.values())), 7)

    def test_the_published_observation_set(self):
        self.assertEqual(
            set(SW_OBSERVABLES.values()),
            {"GDPC1", "PCECC96", "GPDIC1", "HOANBS", "COMPRNFB", "CPIAUCSL", "FEDFUNDS"},
        )

    def test_the_model_records_its_own_m(self):
        sw = next(m for m in ROSTER if m.name.startswith("Smets–Wouters"))
        self.assertEqual(len(sw.observables), 7)


class TestTrustBridge(unittest.TestCase):
    def test_board_entries_are_emitted_per_model(self):
        from pacland.economics.model_roster import trust_entries

        es = trust_entries(ROOT)
        self.assertEqual(len(es), len(ROSTER))
        self.assertEqual({e.artifact for e in es}, {m.name for m in models_sorted()})
        self.assertTrue(all(e.discipline == "economics" for e in es))


if __name__ == "__main__":
    unittest.main()
