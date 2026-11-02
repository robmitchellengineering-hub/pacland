"""The ingest gate is a domain check: the sampler's own bounds, reported loudly."""
import unittest

from pacland.exactness import ingest_gate as G


def row(moduli, susy=False, n=2):
    return {"flux": [0] * (2 * n), "moduli": moduli, "is_susy": susy}


def pair(re, im=0.0):
    return [re, im]


class TestTheBoundsAreTheModelsOwn(unittest.TestCase):
    def test_the_declared_bounds_are_the_sampler_defaults(self):
        # jaxvacua data_sampler default: moduli_bounds = (1.0, 5.0)
        self.assertEqual(G.MODULI_BOUNDS, (1.0, 5.0))

    def test_the_loose_band_is_wider(self):
        self.assertLess(G.LOOSE_BAND[0], G.MODULI_BOUNDS[0])
        self.assertGreater(G.LOOSE_BAND[1], G.MODULI_BOUNDS[1])


class TestClassification(unittest.TestCase):
    def test_a_modulus_inside_the_bounds_is_in_domain(self):
        self.assertEqual(G.classify(row([pair(1.0), pair(2.0)])), "in_domain")

    def test_a_runaway_is_rejected(self):
        # the corpus really contains |z| ~ 8.5e29; the sampler cannot place a modulus there
        self.assertEqual(G.classify(row([pair(8.5e29)])), "runaway")
        self.assertEqual(G.classify(row([pair(1e42)])), "runaway")

    def test_a_modulus_between_the_bands_is_loose_not_rejected(self):
        self.assertEqual(G.classify(row([pair(8.0)])), "loose")
        self.assertEqual(G.classify(row([pair(1e-2)])), "loose")

    def test_the_corpus_format_is_a_pair_not_a_complex(self):
        # the corpus stores complex numbers as [re, im]; reading them wrong made every row look runaway
        self.assertEqual(G.classify({"flux": [0]*4, "moduli": [[2.0, 3.0]]}), "in_domain")

    def test_an_unparseable_component_raises_rather_than_being_classified(self):
        # a parse failure must not be silently promoted to a data verdict
        with self.assertRaises(ValueError):
            G.modulus_scale({"flux": [0]*4, "moduli": [[1.0, 2.0, 3.0]]})


class TestTheReportFailsLoudly(unittest.TestCase):
    def test_it_counts_rejections_rather_than_dropping_them(self):
        rows = [row([pair(2.0)], susy=True), row([pair(1e30)]), row([pair(1e40)])]
        per = G.report(rows, b3_of=lambda r: 6)
        d = per[6]
        self.assertEqual(d["rows"], 3)          # nothing silently dropped
        self.assertEqual(d["in_domain"], 1)
        self.assertEqual(d["runaway"], 2)
        self.assertAlmostEqual(d["runaway_share"], 2 / 3)

    def test_the_two_rates_differ_where_composition_bites(self):
        rows = [row([pair(2.0)], susy=True), row([pair(1e30)]), row([pair(1e40)])]
        d = G.report(rows, b3_of=lambda r: 6)[6]
        self.assertAlmostEqual(d["susy_rate_all"], 1 / 3)
        self.assertAlmostEqual(d["susy_rate_in_domain"], 1.0)   # the only real point is SUSY

    def test_the_verdict_says_why_it_is_a_domain_check(self):
        v = G.verdict(G.report([row([pair(2.0)])], b3_of=lambda r: 6))
        self.assertIn("declared moduli bounds", v["statement"])
        self.assertIn("never silently", v["rule"])


if __name__ == "__main__":
    unittest.main()
