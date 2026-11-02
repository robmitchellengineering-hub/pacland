"""Gated minima-only reporting: over genuine rows the minima rate is flat, and the N/b3 climb survives."""
import unittest

from pacland.exactness import counterexample as C
from pacland.exactness import ingest_gate as G


class TestTheGatedRates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = [c["row"] for c in C.load_corpus()]
        cls.per = G.report(rows)
        cls.gated = [r for r in rows if G.classify(r) == "in_domain"]

    def test_the_corpus_is_half_outside_the_bounds(self):
        tot = sum(d["rows"] for d in self.per.values())
        run = sum(d["runaway"] for d in self.per.values())
        self.assertGreater(run / tot, 0.4)
        self.assertLess(run / tot, 0.6)

    def test_the_raw_minima_rate_looks_like_a_decline(self):
        rates = [self.per[b]["minima_rate_all"] for b in sorted(self.per)]
        self.assertGreater(rates[0], rates[-1])          # 49.4% -> 7.5%

    def test_the_gated_minima_rate_is_flat(self):
        # over genuine in-domain rows the minima rate sits near 80% at EVERY b3
        rates = [self.per[b]["minima_rate_in_domain"] for b in sorted(self.per)]
        for r in rates:
            self.assertGreater(r, 0.7, rates)
            self.assertLess(r, 0.9, rates)
        self.assertLess(max(rates) - min(rates), 0.10, rates)

    def test_the_susy_decline_survives_the_gate_but_flattens(self):
        raw = [self.per[b]["susy_rate_all"] for b in sorted(self.per)]
        gated = [self.per[b]["susy_rate_in_domain"] for b in sorted(self.per)]
        self.assertGreater(gated[0], raw[0])             # 43.3% vs 27.9%
        self.assertGreater(gated[0], gated[-1])          # still declines

    def test_the_n_b3_climb_survives_the_gate(self):
        for b3 in sorted(self.per):
            sel = sorted((float(r["Nflux"]), bool(r.get("is_susy")))
                         for r in self.gated
                         if len(r["flux"]) // 2 == b3 and r.get("Nflux") and float(r["Nflux"]) > 0)
            if len(sel) < 8:
                continue
            k = len(sel) // 4
            q1 = sum(1 for _, s in sel[:k] if s) / k
            q4 = sum(1 for _, s in sel[3 * k:] if s) / len(sel[3 * k:])
            self.assertGreater(q4, q1, f"b3={b3}")


if __name__ == "__main__":
    unittest.main()


class TestTheIntervalVerdict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = [c["row"] for c in C.load_corpus()]
        cls.per = G.report(rows)

    def test_the_intervals_overlap_so_flat_is_consistent_not_proven(self):
        iv = G.interval_verdict(self.per)
        self.assertTrue(iv["intervals_overlap"])
        self.assertIn("CONSISTENT", iv["statement"])
        self.assertIn("not proven", iv["statement"])

    def test_the_thin_rungs_are_named(self):
        iv = G.interval_verdict(self.per)
        self.assertIn(10, iv["under_two_hundred_rows"])
