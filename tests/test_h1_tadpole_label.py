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


class TestTheTwoParameterStructure(unittest.TestCase):
    """The successor to H1: BOTH `b3` and `N` matter, and each is monotone.

    H1 died because the tadpole alone does not label the vacuum. But the tadpole is not irrelevant either — inside a
    fixed `b3` the SUSY fraction climbs steeply with `N`, while at fixed `N` it falls with `b3`. So the vacuum is
    labelled by `(b3, N)` with a monotone dependence on each, which is a law rather than a null.
    """

    @classmethod
    def setUpClass(cls):
        rows = []
        for c in C.load_corpus():
            r = c["row"]
            rows.append((len(r["flux"]) // 2, r.get("Nflux"), bool(r.get("is_susy"))))
        cls.quartiles = {}
        for b3 in (6, 8, 10):
            sel = sorted((N, s) for (bb, N, s) in rows if bb == b3 and N is not None)
            k = len(sel) // 4
            frs = []
            for q in range(4):
                chunk = sel[q * k:(q + 1) * k] if q < 3 else sel[3 * k:]
                frs.append(sum(1 for _, x in chunk if x) / len(chunk))
            cls.quartiles[b3] = frs

    def test_the_fraction_climbs_with_N_inside_each_b3(self):
        for b3, frs in self.quartiles.items():
            self.assertGreater(frs[-1], frs[0], f"b3={b3}: {frs}")
            self.assertGreater(frs[2], frs[1], f"b3={b3}: {frs}")

    def test_the_recorded_quartiles(self):
        self.assertAlmostEqual(self.quartiles[6][0], 0.076, places=3)
        self.assertAlmostEqual(self.quartiles[6][3], 0.447, places=3)
        self.assertAlmostEqual(self.quartiles[10][3], 0.033, places=3)

    def test_a_similar_N_different_b3_differs(self):
        # b3=6's N 14-30 quartile is 0.345; b3=8's N 19-41 quartile is 0.258 -- so N alone is not enough
        self.assertGreater(self.quartiles[6][2], self.quartiles[8][2])

    def test_the_whole_range_shrinks_with_b3(self):
        self.assertGreater(self.quartiles[6][3], self.quartiles[8][3])
        self.assertGreater(self.quartiles[8][3], self.quartiles[10][3])
