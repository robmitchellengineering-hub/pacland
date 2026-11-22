"""find K: the cluster-expansion bound is valid at strong coupling but fails at weak coupling."""
import unittest

from pacland import find_K as fk


class TestFindK(unittest.TestCase):
    def test_activity_increases_toward_one(self):
        self.assertLess(fk.activity(1.0), fk.activity(4.0))
        self.assertLess(fk.activity(8.0), 1.0)

    def test_cluster_bound_is_valid_at_strong_coupling(self):
        self.assertLessEqual(fk.cluster_bound(2.0), fk.referee(2.0))

    def test_cluster_bound_is_invalid_at_weak_coupling(self):
        # at β=8 the cluster bound exceeds the exponentially-small true gap
        self.assertGreater(fk.cluster_bound(8.0), fk.referee(8.0))

    def test_find_K_concludes_strong_coupling_only(self):
        r = fk.find_K()
        self.assertLess(r["n_valid"], len(r["rows"]))
        self.assertIn("strong coupling", r["conclusion"])


if __name__ == "__main__":
    unittest.main()
