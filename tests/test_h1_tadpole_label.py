"""H1 refuted on the full corpus: the tadpole does NOT label the vacuum.

H1 claimed flux vacua are classified completely by `(N, orbit)`, so nothing physical depends on `b3` at fixed `N`.
If true, the landscape collapses to a one-parameter family. The 5,965-row corpus says otherwise, and the fixed-`N`
comparison is what settles it.
"""
import unittest
from collections import defaultdict

from pacland.exactness import counterexample as C


def _by_b3():
    agg = defaultdict(lambda: [0, 0])
    for c in C.load_corpus():
        r = c["row"]
        b3 = len(r["flux"]) // 2
        agg[b3][0] += 1
        agg[b3][1] += bool(r.get("is_susy"))
    return agg


def _by_N():
    by = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for c in C.load_corpus():
        r = c["row"]
        b3 = len(r["flux"]) // 2
        by[r.get("Nflux")][b3][0] += 1
        by[r.get("Nflux")][b3][1] += bool(r.get("is_susy"))
    return by


class TestTheCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agg = _by_b3()
        cls.byN = _by_N()

    def test_the_corpus_is_the_recorded_one(self):
        self.assertEqual(sum(v[0] for v in self.agg.values()), 5965)

    def test_the_susy_fraction_falls_with_b3(self):
        # 0.279 -> 0.202 -> 0.012, monotone decreasing
        fr = {b3: s / n for b3, (n, s) in self.agg.items()}
        self.assertAlmostEqual(fr[6], 0.279, places=3)
        self.assertAlmostEqual(fr[8], 0.202, places=3)
        self.assertAlmostEqual(fr[10], 0.012, places=3)
        self.assertGreater(fr[6], fr[8])
        self.assertGreater(fr[8], fr[10])

    def test_at_fixed_tadpole_the_physics_differs(self):
        # H1's falsifier: the same N carries different SUSY fractions at different b3.
        # N = 5: b3=6 -> 27/157, b3=8 -> 1/34, b3=10 -> 0/64
        d = self.byN[5.0]
        self.assertEqual(d[6], [157, 27])
        self.assertEqual(d[8], [34, 1])
        self.assertEqual(d[10], [64, 0])
        fr = {b3: s / n for b3, (n, s) in d.items()}
        self.assertGreater(fr[6], 0.15)
        self.assertLess(fr[10], 0.02)

    def test_the_shared_classes_are_numerous(self):
        shared = [N for N, d in self.byN.items() if len(d) >= 2 and sum(v[0] for v in d.values()) >= 20]
        self.assertGreaterEqual(len(shared), 50)


if __name__ == "__main__":
    unittest.main()
