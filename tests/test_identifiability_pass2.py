"""Identifiability must be a property of the space, not of the assumed Q."""
import io
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
import identifiability_pass2 as P  # noqa: E402
from pacland.spectral import em_modes as E  # noqa: E402


class TestStability(unittest.TestCase):
    def test_usable_count_does_not_move_with_q(self):
        a = b = d = 1.0
        counts = [E.usable_modes(a, b, d, 1.0e8, 1.0e9, probes=3, noise_db=-60.0,
                                 q_factor=q)["usable_10pct"] for q in (25.0, 50.0, 100.0)]
        self.assertEqual(len(set(counts)), 1, counts)

    def test_the_count_grows_with_the_space_then_saturates(self):
        small = E.usable_modes(0.5, 0.5, 0.5, 1.0e8, 1.0e9, probes=3, noise_db=-60.0, q_factor=50)["usable_10pct"]
        big = E.usable_modes(3.0, 4.0, 2.5, 1.0e8, 1.0e9, probes=3, noise_db=-60.0, q_factor=50)["usable_10pct"]
        self.assertGreater(big, small)
        self.assertLessEqual(big, 20)          # saturation: more modes is not more usable directions


class TestTheScript(unittest.TestCase):
    def test_it_reaches_a_verdict(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            P.main()
        out = buf.getvalue()
        self.assertTrue("VERDICT" in out)
        self.assertIn("x1.00", out)


if __name__ == "__main__":
    unittest.main()
