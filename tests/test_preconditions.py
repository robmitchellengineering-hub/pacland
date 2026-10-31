"""The guards must be able to fire. Each test breaks the apparatus on purpose."""
import unittest

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import preconditions as pre  # noqa: E402


class FakeModel:
    def __init__(self, corrections: bool):
        self.include_mirror_wsi = corrections


class TestCorrectionsGuard(unittest.TestCase):
    def test_degree_zero_with_corrections_on_is_a_contradiction(self):
        with self.assertRaises(pre.PreconditionError):
            pre.require_corrections_on(FakeModel(True), 0)

    def test_degree_two_with_corrections_off_is_the_2026_10_29_failure(self):
        with self.assertRaises(pre.PreconditionError):
            pre.require_corrections_on(FakeModel(False), 2)

    def test_matching_configuration_passes(self):
        pre.require_corrections_on(FakeModel(True), 2)
        pre.require_corrections_on(FakeModel(False), 0)


class TestFieldAgreement(unittest.TestCase):
    def test_the_measured_1e38_against_1e37_disaster_raises(self):
        with self.assertRaises(pre.PreconditionError):
            pre.require_agree(1.71e38, 3.77e-37, ("|DW|", "residual"))

    def test_agreeing_fields_pass(self):
        self.assertLess(pre.require_agree(1.0e-9, 2.0e-9, ("a", "b")), 1.0)


class TestMultiPoint(unittest.TestCase):
    def test_one_point_is_a_draw(self):
        with self.assertRaises(pre.PreconditionError):
            pre.require_multi_point(1)

    def test_five_points_pass(self):
        pre.require_multi_point(5)


if __name__ == "__main__":
    unittest.main()
