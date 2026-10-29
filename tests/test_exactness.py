"""The exactness instruments — and the proofs that each one can go red.

An exactness check that cannot fail is decoration, so every check here has a mutation test beside it:
the thing it protects is broken on purpose and the check must notice.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pacland.exactness import controls as C
from pacland.exactness import identities as X
from pacland.exactness import invariance as I
from pacland.exactness import windows as W
from pacland.oracle import potential_t6 as P

ROOT = Path(__file__).resolve().parents[1]
TAUS = [0.3 + 1.1j, -0.2 + 0.9j, 0.1 + 1.4j, 0.4 + 0.8j]


def _flux():
    F = np.zeros(8)
    H = np.zeros(8)
    F[0], F[3], H[1], H[5] = 1.0, -2.0, 1.0, 3.0
    return F, H


class TestInvariance(unittest.TestCase):
    def test_the_f_term_is_covariant(self):
        F, H = _flux()
        r = I.f_term_covariance(F, H, TAUS)
        self.assertTrue(r["pass"], r["detail"])

    def test_a_constant_kaehler_transformation_is_invisible(self):
        F, H = _flux()
        self.assertTrue(I.phase_invariance(F, H, TAUS)["pass"])

    def test_v_is_quadratic_in_the_flux(self):
        F, H = _flux()
        self.assertTrue(I.homogeneity(F, H, TAUS)["pass"])

    def test_the_unfolded_spectrum_is_scale_free(self):
        F, H = _flux()
        r = I.spacing_invariance(F, H, TAUS)
        self.assertTrue(r["pass"], r["detail"])
        self.assertAlmostEqual(r["ratio_statistic"], r["ratio_statistic_scaled"], places=12)

    def test_a_supersymmetric_vacuum_here_is_ads(self):
        # the identity measured, not asserted: V = -3 e^K |W|^2 and V < 0
        r = I.susy_value_identity()
        self.assertTrue(r["pass"], r["detail"])
        self.assertLess(r["value"], 0.0)

    # ---- mutations: each check must fail when the thing it protects is broken ----
    def test_the_covariance_check_can_fail(self):
        # the real bug this guards: an F-term assembled without the K_i W piece
        original = P.f_terms

        def uncovariant(F, H, taus):
            _w, dw = P.superpotential_and_gradients(F, H, *taus[:4])
            return np.array(dw, dtype=complex)

        P.f_terms = uncovariant
        try:
            F, H = _flux()
            self.assertFalse(I.f_term_covariance(F, H, TAUS)["pass"])
        finally:
            P.f_terms = original

    def test_the_homogeneity_check_can_fail(self):
        original = P.potential
        P.potential = lambda F, H, *t: float(np.sum(np.abs(F) + np.abs(H)))   # degree 1, not 2
        try:
            F, H = _flux()
            self.assertFalse(I.homogeneity(F, H, TAUS)["pass"])
        finally:
            P.potential = original


class TestCorpusIdentities(unittest.TestCase):
    def test_the_pairing_convention_is_the_one_the_data_uses(self):
        # first row of h12_2_m1: naive sum gives -25, F^T J H gives the recorded 7
        flux = [3, -1, -4, 0, -2, 11, 0, -2, -1, 0, 0, 0]
        self.assertEqual(X.tadpole(flux), 7)

    def test_the_corpus_is_internally_consistent_except_the_pinned_rows(self):
        r = X.audit_corpus(ROOT / "data")
        self.assertTrue(r["all_pass"])
        self.assertEqual(r["rows"], 5885)
        self.assertEqual(r["n_known"], 5)          # 5 of 5,885: recorded Nflux is the negative
        self.assertEqual(r["n_unexplained"], 0)

    def test_a_new_sign_flip_goes_red(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            src = ROOT / "data" / "h12_2_m1_stats.json"
            doc = json.loads(src.read_text())
            doc["vacua"][0]["Nflux"] = -doc["vacua"][0]["Nflux"]     # a defect not in the pinned set
            (tmp / src.name).write_text(json.dumps(doc))
            r = X.audit_corpus(tmp)
            self.assertEqual(r["n_unexplained"], 1)
            self.assertFalse(r["all_pass"])
        finally:
            shutil.rmtree(tmp)


class TestControlGate(unittest.TestCase):
    def test_the_goe_constant_is_not_read_as_gue(self):
        # the value 0.5307 is GOE's; the GUE band must sit above it at the same size
        goe = C.control_band(20, 60, "goe", trials=12, seed=5)
        gue = C.control_band(20, 60, "gue", trials=12, seed=5)
        self.assertGreater(gue["mean"], goe["mean"] + 2.0 * goe["sd"])
        self.assertLess(goe["mean"], C.RATIO_GOE_ASYMPTOTIC + 3.0 * goe["sd"])

    def test_the_gate_refuses_a_verdict_it_cannot_support(self):
        # 40 spectra of dim 6 put the GOE and Poisson bands under 5 sd apart: no class may be assigned
        g = C.gate(C.synthetic_spectra(6, 40, "goe", seed=1), trials=40, seed=1)
        self.assertEqual(g["verdict"], "undecidable")
        self.assertGreater(g["required_count"], 40)

    def test_the_required_size_is_reachable_on_this_corpus(self):
        need = C.required_count(6)
        self.assertGreater(need, 40)
        self.assertLess(need, 3424)               # the h12=2 corpus holds 3,424 spectra

    def test_the_pipeline_recovers_classes_it_cannot_know(self):
        r = C.authority_check(available=3424, trials=20)
        self.assertTrue(r["all_pass"], [c for c in r["cells"] if not c["pass"]])


class TestWindows(unittest.TestCase):
    def test_the_window_census(self):
        r = W.window_report(6, 1)
        self.assertEqual(r["pairs"], 531441)                    # 3^12
        self.assertEqual(r["pairs_with_N_gt_0"], 201768)
        self.assertEqual((r["N_min"], r["N_max"]), (-6, 6))

    def test_the_two_measures_actually_differ(self):
        c = W.convergence(6, [1, 3, 6], 1)
        self.assertGreater(c["max_shift"], 0.5)                 # 0.62 measured
        self.assertFalse(c["measures_agree"])
        self.assertTrue(c["primitive_equals_flux"])             # and the all-vs-primitive pair is empty here

    def test_coverage_of_a_known_flux(self):
        # a single-pair corpus inside the window is found; one outside it is not
        inside = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        outside = [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     # primitive, but outside the window
        c = W.coverage([inside], 6, 1)
        self.assertEqual(c["corpus_orbits_in_window"], 1)
        c2 = W.coverage([outside], 6, 1)
        self.assertEqual(c2["corpus_orbits_in_window"], 0)


class TestReport(unittest.TestCase):
    def test_every_invariance_check_passes_together(self):
        r = I.report()
        self.assertEqual(r["n_pass"], r["n"], [c for c in r["checks"] if not c["pass"]])


if __name__ == "__main__":
    unittest.main()
