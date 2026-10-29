"""Identifiability: the rank must not exceed the parameter count, and one mic must not suffice."""
import unittest

from pacland.spectral import identify as I


class TestRank(unittest.TestCase):
    def test_rank_cannot_exceed_the_parameter_count(self):
        r = I.identifiability(n_modes=4)
        for row in r["rows"]:
            self.assertLessEqual(row["rank"], row["params"])

    def test_a_single_microphone_does_not_identify_everything(self):
        r = I.identifiability(n_modes=5)
        self.assertLess(r["rows"][0]["rank"], r["n_params"])

    def test_identifiability_saturates_by_two_mics_in_one_dimension(self):
        r = I.identifiability(n_modes=5)
        self.assertEqual(r["rows"][1]["rank"], r["n_params"])

    def test_geometry_known_does_not_raise_the_fraction(self):
        a = I.identifiability(fit_freqs=True)
        b = I.identifiability(fit_freqs=False)
        self.assertAlmostEqual(a["rows"][0]["identifiable_fraction"],
                               b["rows"][0]["identifiable_fraction"], delta=0.10)


class TestAudit(unittest.TestCase):
    def test_all_checks_are_green(self):
        self.assertTrue(I.audit()["all_pass"])


class TestBinaural(unittest.TestCase):
    """Rob's rig: a 17 cm pair walked around, sent over the wireless transport."""

    def test_one_binaural_position_beats_one_omni_position(self):
        r = I.binaural_conditioning(positions=(1,))
        row = r["rows"][0]
        self.assertGreater(row["binaural"]["usable"], row["omni"]["usable"])
        # and the weakest direction moves out of the noise floor
        self.assertLess(row["omni"]["weakest"], 1e-6)
        self.assertGreater(row["binaural"]["weakest"], 1e-4)

    def test_beyond_one_position_the_pair_adds_margin_not_parameters(self):
        r = I.binaural_conditioning(positions=(2,))
        row = r["rows"][0]
        self.assertEqual(row["omni"]["usable"], row["binaural"]["usable"])

    def test_both_receivers_are_used(self):
        r = I.binaural_conditioning(positions=(1, 2))
        for row in r["rows"]:
            self.assertEqual(row["binaural"]["receivers"], 2 * row["positions"])


class TestCramerRao(unittest.TestCase):
    """The noise model: with real measurement noise the parameter table does not survive, and the
    test says so rather than letting the rank result stand unqualified."""

    def _setup(self):
        box = I.Box3()
        triples = box.modes_below(100.0)
        params = []
        for i, (_, _, _, _f) in enumerate(triples):
            params += [0.06, 1.0 / (1.0 + 0.1 * i)]
        grid = [(box.lx * (0.15 + 0.23 * ix), box.ly * (0.17 + 0.22 * iy), box.lz * (0.22 + 0.45 * iz))
                for ix in range(4) for iy in range(4) for iz in range(2)]
        freqs = [40.0 + 60.0 * i / 59 for i in range(60)]
        return box, triples, params, grid, freqs

    def test_less_noise_never_hurts(self):
        box, triples, params, grid, freqs = self._setup()
        lo = I.cramer_rao(box, triples, params, grid[:2], freqs, False, noise=1e-4)
        hi = I.cramer_rao(box, triples, params, grid[:2], freqs, False, noise=1e-2)
        self.assertGreaterEqual(lo["usable_10pct"], hi["usable_10pct"])

    def test_more_microphones_never_hurt(self):
        box, triples, params, grid, freqs = self._setup()
        one = I.cramer_rao(box, triples, params, grid[:1], freqs, False, noise=1e-3)
        three = I.cramer_rao(box, triples, params, grid[:3], freqs, False, noise=1e-3)
        self.assertGreaterEqual(three["usable_10pct"], one["usable_10pct"])

    def test_complex_data_beats_magnitude_only(self):
        box, triples, params, grid, freqs = self._setup()
        mag = I.cramer_rao(box, triples, params, grid[:2], freqs, False, noise=1e-3, complex_data=False)
        cx = I.cramer_rao(box, triples, params, grid[:2], freqs, False, noise=1e-3, complex_data=True)
        self.assertLess(cx["median_dir_sd"], mag["median_dir_sd"])

    def test_at_ordinary_noise_the_parameter_table_does_not_survive(self):
        # the honest finding: at -50 dB nothing is usable to 10%. If this ever flips, the claim checked
        # in the doc has changed and the doc must change with it.
        box, triples, params, grid, freqs = self._setup()
        r = I.cramer_rao(box, triples, params, grid[:3], freqs, False, noise=3e-3)
        self.assertEqual(r["usable_10pct"], 0)


class TestBoxBehavingLikeARoom(unittest.TestCase):
    """Testing 'the real room' without leaving the box: break the symmetry, then randomise the spectrum."""

    def test_a_commensurate_box_really_is_degenerate(self):
        r = I.degeneracy_report(I.Box3(), 200.0)
        self.assertGreater(r["degenerate"], 20)

    def test_an_incommensurate_box_has_none(self):
        r = I.degeneracy_report(I.incommensurate_box(), 200.0)
        self.assertEqual(r["degenerate"], 0)

    def test_breaking_the_symmetry_does_not_rescue_identifiability(self):
        # the honest finding: degeneracy is not the limiting factor, the amplitude/damping trade-off is
        box = I.Box3()
        inc = I.incommensurate_box()

        def usable(b):
            triples = b.modes_below(100.0)
            params = []
            for i, (_, _, _, _f) in enumerate(triples):
                params += [0.06, 1.0 / (1.0 + 0.1 * i)]
            grid = [(b.lx * (0.15 + 0.23 * ix), b.ly * (0.17 + 0.22 * iy), b.lz * (0.22 + 0.45 * iz))
                    for ix in range(4) for iy in range(4) for iz in range(2)]
            freqs = [40.0 + 60.0 * i / 59 for i in range(60)]
            return I.cramer_rao(b, triples, params, grid[:3], freqs, False, noise=1e-3)["usable_10pct"]

        self.assertLessEqual(abs(usable(box) - usable(inc)), 2)

    def test_an_ensemble_of_chaotic_rooms_is_more_identifiable_than_one_box(self):
        r = I.ensemble_identifiability(rooms=4, mics=3)
        box = I.Box3()
        triples = box.modes_below(100.0)
        params = []
        for i, (_, _, _, _f) in enumerate(triples):
            params += [0.06, 1.0 / (1.0 + 0.1 * i)]
        grid = [(box.lx * (0.15 + 0.23 * ix), box.ly * (0.17 + 0.22 * iy), box.lz * (0.22 + 0.45 * iz))
                for ix in range(4) for iy in range(4) for iz in range(2)]
        freqs = [40.0 + 60.0 * i / 59 for i in range(60)]
        single = I.cramer_rao(box, triples, params, grid[:3], freqs, False, noise=1e-3)["usable_10pct"]
        self.assertGreater(r["median_usable"], single)

    def test_the_answer_is_a_spread_not_a_number(self):
        r = I.ensemble_identifiability(rooms=5, mics=3)
        self.assertIsInstance(r["p10"], int)
        self.assertLessEqual(r["p10"], r["p90"])
