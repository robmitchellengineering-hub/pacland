"""The belief layer — correctness, the C/P detector, and its mutation behaviour."""
import math
import unittest

from pacland.belief import (
    Belief,
    Likelihood,
    Mode,
    ModeRefusal,
    bayes_factor,
    brier_score,
    detect_mode,
    eig,
    log_score,
    mean_brier,
    posterior,
    rank_by_eig,
    require_convergence,
    update,
)


def _belief(name="h", prior=0.5, tp=0.9, fp=0.1, **kw):
    kw.setdefault("ground_truth_available", True)
    return Belief(name=name, prior=prior, likelihood=Likelihood(tp, fp), **kw)


class TestBayesFactor(unittest.TestCase):
    def test_positive_is_tp_over_fp(self):
        self.assertAlmostEqual(bayes_factor(Likelihood(0.9, 0.1), True), 9.0)

    def test_negative_is_miss_over_specificity(self):
        # (1-tp)/(1-fp) = 0.1/0.9
        self.assertAlmostEqual(bayes_factor(Likelihood(0.9, 0.1), False), 0.1 / 0.9)

    def test_degenerate_denominator_refuses(self):
        with self.assertRaises(ValueError):
            bayes_factor(Likelihood(1.0, 0.0), True)  # fp=0 -> division by zero


class TestPosterior(unittest.TestCase):
    def test_hand_example(self):
        # prior 0.5, B=9 -> post odds 9 -> 0.9
        self.assertAlmostEqual(posterior(0.5, Likelihood(0.9, 0.1), True), 0.9)

    def test_negative_evidence_moves_down(self):
        self.assertAlmostEqual(posterior(0.5, Likelihood(0.9, 0.1), False), 0.1)

    def test_extreme_priors_are_absorbing(self):
        self.assertEqual(posterior(0.0, Likelihood(0.9, 0.1), True), 0.0)
        self.assertEqual(posterior(1.0, Likelihood(0.9, 0.1), False), 1.0)


class TestEig(unittest.TestCase):
    def test_non_discriminating_test_has_zero_eig(self):
        self.assertAlmostEqual(eig(0.5, Likelihood(0.5, 0.5)), 0.0)

    def test_perfect_test_gains_the_whole_entropy(self):
        # a perfect test (tp=1, fp=0) resolves all uncertainty -> EIG = H(prior)
        p = 0.3
        h = -(p * math.log(p) + (1 - p) * math.log(1 - p))
        self.assertAlmostEqual(eig(p, Likelihood(1.0, 0.0)), h)

    def test_closed_form_matches_definition(self):
        # Rule of Three arm 1: the closed form vs an independent brute-force
        # definition computed inline (no reuse of posterior()/eig()).
        for prior, tp, fp in [(0.3, 0.95, 0.05), (0.5, 0.8, 0.3), (0.9, 0.7, 0.6)]:
            p_pos = prior * tp + (1 - prior) * fp
            # P(H|+) and P(H|-) via Bayes' theorem, coded independently here
            post_pos = (tp * prior) / p_pos
            post_neg = ((1 - tp) * prior) / (1 - p_pos)
            ent = lambda q: 0.0 if q <= 0 or q >= 1 else -(q * math.log(q) + (1 - q) * math.log(1 - q))
            h0 = ent(prior)
            expected = h0 - (p_pos * ent(post_pos) + (1 - p_pos) * ent(post_neg))
            self.assertAlmostEqual(eig(prior, Likelihood(tp, fp)), expected, places=12)


class TestScoring(unittest.TestCase):
    def test_brier_known_values(self):
        self.assertAlmostEqual(brier_score(0.7, True), 0.09)
        self.assertAlmostEqual(brier_score(0.7, False), 0.49)

    def test_log_score_lower_for_truth_side(self):
        self.assertAlmostEqual(log_score(0.7, True), -math.log(0.7))
        self.assertLess(log_score(0.7, True), log_score(0.7, False))

    def test_biased_forecaster_scores_worse(self):
        # Rule of Three arm 3: a synthetic forecaster with known overconfidence.
        truths = [True, True, False, False]  # base rate 0.5
        overconfident = mean_brier([(0.8, t) for t in truths])
        calibrated = mean_brier([(0.5, t) for t in truths])
        self.assertAlmostEqual(overconfident, 0.34)
        self.assertLess(calibrated, overconfident)

    def test_empty_record_refuses(self):
        with self.assertRaises(ValueError):
            mean_brier([])


class TestDetectMode(unittest.TestCase):
    def test_all_convergent(self):
        v = detect_mode([_belief("a"), _belief("b")])
        self.assertEqual(v.mode, Mode.CONVERGENCE)
        self.assertEqual(v.reasons, ())

    def test_empty_space_is_underdetermined(self):
        self.assertEqual(detect_mode([]).mode, Mode.UNDERDETERMINED)

    def test_empty_likelihood_is_underdetermined(self):
        b = _belief("a")
        no_lik = Belief(name="b", prior=0.5, likelihood=None, ground_truth_available=True)
        v = detect_mode([b, no_lik])
        self.assertEqual(v.mode, Mode.UNDERDETERMINED)

    def test_missing_ground_truth_is_pluralism(self):
        b = _belief("a")
        no_gt = _belief("b", ground_truth_available=False)
        v = detect_mode([b, no_gt])
        self.assertEqual(v.mode, Mode.PLURALISM)


class TestGating(unittest.TestCase):
    def test_require_convergence_passes_in_mode_c(self):
        require_convergence(Mode.CONVERGENCE)  # must not raise

    def test_require_convergence_refuses_outside_mode_c(self):
        for m in (Mode.PLURALISM, Mode.UNDERDETERMINED):
            with self.assertRaises(ModeRefusal):
                require_convergence(m)

    def test_rank_refuses_in_mode_p(self):
        with self.assertRaises(ModeRefusal):
            rank_by_eig([_belief("a"), _belief("b", ground_truth_available=False)])

    def test_rank_orders_by_eig_over_cost(self):
        hi = _belief("hi", prior=0.5, tp=0.99, fp=0.01, cost=1.0)   # near-perfect
        lo = _belief("lo", prior=0.5, tp=0.5, fp=0.5, cost=1.0)     # non-discriminating
        ranked = rank_by_eig([lo, hi])
        self.assertEqual([name for name, _ in ranked], ["hi", "lo"])

    def test_update_refuses_empty_likelihood(self):
        b = Belief(name="x", prior=0.5, likelihood=None)
        with self.assertRaises(ModeRefusal):
            update(b, True)

    def test_update_moves_the_prior(self):
        updated = update(_belief("h", prior=0.5), True)
        self.assertAlmostEqual(updated.prior, 0.9)


class TestDetectorMutations(unittest.TestCase):
    """The detector must be able to fail — flipping one input changes the regime."""

    def _convergent(self):
        return [_belief("a"), _belief("b")]

    def test_flipping_ground_truth_breaks_convergence(self):
        self.assertEqual(detect_mode(self._convergent()).mode, Mode.CONVERGENCE)
        mutated = self._convergent()
        mutated[1] = _belief("b", ground_truth_available=False)
        self.assertEqual(detect_mode(mutated).mode, Mode.PLURALISM)

    def test_dropping_a_likelihood_breaks_convergence(self):
        mutated = self._convergent()
        mutated[1] = Belief(name="b", prior=0.5, likelihood=None, ground_truth_available=True)
        self.assertEqual(detect_mode(mutated).mode, Mode.UNDERDETERMINED)


if __name__ == "__main__":
    unittest.main()
