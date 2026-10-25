"""Climate's constraint rank — written down versus independent."""
import unittest

from pacland.climate import constraint_set as C


class TestInventory(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(C.INVARIANTS), 5)
        self.assertEqual(len(C.GUARDS), 6)
        self.assertEqual(len(C.CALIBRATION), 3)
        self.assertEqual(len(C.STATE_CONSTRAINTS), 14)

    def test_process_constraints_are_named_not_counted(self):
        self.assertEqual(len(C.PROCESS_CONSTRAINTS), 5)
        self.assertTrue(any("y0" in p for p in C.PROCESS_CONSTRAINTS))


class TestRank(unittest.TestCase):
    def test_nine_independent_of_fourteen(self):
        ind = C.independence()
        self.assertEqual(ind["n_state"], 14)
        self.assertEqual(ind["rank"], 9)
        self.assertEqual(ind["dependent"], 5)

    def test_the_duplicates_are_the_guards(self):
        ind = C.independence()
        self.assertGreaterEqual(ind["dependent"], 5)
        # the invariants survive; the guards restating them collapse into them
        self.assertIn("energy", ind["independent"])

    def test_summary_states_the_inflation_risk(self):
        s = C.summary()
        self.assertIn("independent state rank  9 of 14", s)
        self.assertIn("inflating", s)


if __name__ == "__main__":
    unittest.main()
