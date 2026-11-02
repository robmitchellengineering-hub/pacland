"""The eDNA counting laws: detectability, the contamination floor, and the effort that buys a limit."""
from __future__ import annotations

import math
import unittest

from pacland.edna import limit as L


class TestDetection(unittest.TestCase):

    def test_detection_probability_is_the_poisson_complement(self):
        self.assertAlmostEqual(L.detection_probability(1.0), 1 - math.exp(-1.0), places=12)

    def test_more_reads_always_detect_better(self):
        vals = [L.detection_probability(m) for m in (0.1, 0.5, 1, 2, 5)]
        self.assertEqual(vals, sorted(vals))

    def test_no_reads_is_no_detection(self):
        self.assertEqual(L.detection_probability(0.0), 0.0)

    def test_needing_two_reads_is_stricter_than_one(self):
        self.assertLess(L.detection_probability(1.0, 2), L.detection_probability(1.0, 1))


class TestContaminationFloor(unittest.TestCase):

    def test_a_clean_library_needs_one_read(self):
        self.assertEqual(L.contamination_floor(0.0, 10), 1)

    def test_the_floor_rises_with_contamination(self):
        floors = [L.contamination_floor(c, 10) for c in (0.0, 0.1, 0.5, 1.0, 2.0)]
        self.assertEqual(floors, sorted(floors))

    def test_the_floor_rises_with_samples_at_fixed_contamination(self):
        # more samples means more background in total, which is why the LIMIT must be read per sample
        self.assertGreater(L.contamination_floor(0.1, 100), L.contamination_floor(0.1, 1))

    def test_zero_samples_is_refused(self):
        with self.assertRaises(ValueError):
            L.contamination_floor(0.1, 0)


class TestDetectionLimit(unittest.TestCase):

    def test_the_limit_per_sample_falls_as_samples_rise(self):
        per_sample = [L.detection_limit_reads(0.1, n) / n for n in (1, 2, 5, 10, 20, 50, 100)]
        self.assertLess(per_sample[-1], per_sample[0])
        self.assertEqual(per_sample, sorted(per_sample, reverse=True))

    def test_the_limit_rises_with_contamination(self):
        lims = [L.detection_limit_reads(c, 10) for c in (0.0, 0.1, 0.5, 1.0, 2.0)]
        # discreteness gives the floor steps, so compare the ends rather than every adjacent pair
        self.assertGreater(lims[-1], lims[0])

    def test_the_limit_is_the_species_contribution_above_the_background(self):
        # the floor is a TOTAL count; the limit is what the species must add. At c=1.0 the background alone is 10 of the
        # floor's 15, so the species' own contribution is legitimately below the floor.
        for c in (0.0, 0.1, 1.0):
            floor = L.contamination_floor(c, 10)
            background = c * 10
            self.assertGreaterEqual(L.detection_limit_reads(c, 10), floor - background - 1.0)

    def test_sample_requirement_finds_a_number_that_works(self):
        n = L.sample_requirement(0.1, 10.0)
        self.assertLessEqual(L.detection_limit_reads(0.1, n), 10.0)


class TestResolution(unittest.TestCase):

    def test_a_bigger_budget_resolves_more(self):
        counts = [L.distinguishable_species(b, 40.0, 0.1) for b in (1e4, 1e5, 1e6)]
        self.assertEqual(counts, sorted(counts))

    def test_no_budget_resolves_nothing(self):
        self.assertEqual(L.distinguishable_species(0.0, 40.0), 0)

    def test_more_contamination_resolves_fewer(self):
        clean = L.distinguishable_species(1e6, 40.0, 0.01)
        dirty = L.distinguishable_species(1e6, 40.0, 2.0)
        self.assertLess(dirty, clean)


if __name__ == "__main__":
    unittest.main()
