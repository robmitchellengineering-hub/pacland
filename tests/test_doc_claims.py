"""Doc-claim guards — a published number must equal the number the repo computes.

The rule (operating manual 43/45): *done means verified*, and a claim gets checked
against reality before it is published. The docs had rotted in exactly that way — a
"140 tests" figure from three test-file generations ago, "178" in the badge table, a
`m = 0` deficit after the deficit had been climbed to 9 — because nothing failed when
they fell behind the code.

Each test below recomputes a number from the code or the committed data and fails when
a doc quotes a different one:

  1. **`m`**, the Mitchell Verification Deficit — recomputed from the
     measured/computable/validated flags in ``pacland.observables`` across the
     TOPOLOGY, FLUX and SM sectors. Historical values are allowed only on an
     explicitly marked history line (see ``HISTORY_MARKERS``).
  2. **the test count** quoted beside ``unittest discover -s tests`` — compared with
     the number of tests the loader actually collects (so this file counts itself).
  3. **the landscape totals** (critical points / SUSY vacua / models) — recomputed
     from ``data/h12_*_stats.json``.

Sector-scoped zeros are deliberately *not* covered: a discipline's own docs
(climate, drugs, economics) legitimately carry their own `m`, and the values sector is
legitimately unvalidated. This guard is about the string-landscape deficit's headline
value, which is what rotted.

Fast (<5 s) and dependency-free: stdlib only, no network, no sampling.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.observables import (  # noqa: E402
    FLUX_OBSERVABLES,
    SM_OBSERVABLES,
    TOPOLOGY_OBSERVABLES,
)

# Docs that make a claim about the string-landscape deficit itself. A discipline doc
# is deliberately absent: its `m` is its own sector's, not this one's.
DEFICIT_DOCS = (
    "README.md",
    "docs/narrowing-the-field.md",
    "docs/verification-deficit-explainer.md",
    "docs/verification-deficit.md",
    "docs/sm-frontier.md",
    "docs/complete-exact-structure.md",
    "docs/boundary-map.md",
    "docs/two-sessions-synthesis.md",
    "docs/swampland-connection.md",
    "docs/t6-exact-oracle.md",
    "docs/new-approach.md",
    "docs/orbit-space-unification.md",
    "docs/sm-boundary-map.md",
)

# Docs that quote a total for the full h12 landscape sample (not a sub-sample:
# `docs/ds-conjecture-test.md`'s 2683 is a different run on `data/ds_test.json`).
LANDSCAPE_DOCS = (
    "docs/orbit-space-unification.md",
    "docs/sampling-frontier.md",
)

# Docs that quote how many tests the suite has.
TEST_COUNT_DOCS = (
    "README.md",
    "docs/arxiv-submission.md",
    "docs/t6-exact-oracle.md",
    "docs/ai-verified-badge.md",
    "docs/swampland-connection.md",
)

# A line that quotes a historical value must say so. Markers, not a whitelist of
# numbers: the point is that a stale number has to be labelled stale.
HISTORY_MARKERS = ("Correction", "was 5 before", "history:", "History:")

M_PATTERN = re.compile(r"\bm\s*=\s*(\d+)")
M_STAYS_PATTERN = re.compile(r"\bm\s+stays\s+\**(\d+)")
TESTS_PATTERN = re.compile(r"(\d+)\s+tests")
BADGE_TESTS_PATTERN = re.compile(r"gate green \((\d+) tests\)")
CRITICAL_POINTS_PATTERN = re.compile(r"([\d,]{4,})\s+critical points")
VACUA_TOTAL_PATTERN = re.compile(r"([\d,]{4,})\s+vacua")
SUSY_TOTAL_PATTERN = re.compile(r"([\d,]{4,})\s+SUSY")
MODELS_PATTERN = re.compile(r"(\d+)\s+models")


def deficit_m() -> int:
    """The Mitchell Verification Deficit: measured AND computable AND validated."""
    return sum(
        1
        for group in (TOPOLOGY_OBSERVABLES, FLUX_OBSERVABLES, SM_OBSERVABLES)
        for obs in group
        if obs.measured and obs.computable and obs.validated
    )


def collected_test_count() -> int:
    """How many tests `unittest discover -s tests` actually collects."""
    tests_dir = ROOT / "tests"
    loader = unittest.TestLoader()
    suite = loader.discover(str(tests_dir), top_level_dir=str(tests_dir))
    return suite.countTestCases()


def landscape_totals():
    """(files, critical points, SUSY vacua) recomputed from the committed stats."""
    paths = sorted((ROOT / "data").glob("h12_*_stats.json"))
    points = susy = 0
    for path in paths:
        vacua = json.loads(path.read_text(encoding="utf-8")).get("vacua", [])
        points += len(vacua)
        susy += sum(1 for v in vacua if v.get("is_susy"))
    return len(paths), points, susy


def doc_lines(rel: str):
    """Yield (line number, line) for a doc, 1-based."""
    text = (ROOT / rel).read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
        yield number, line


def _is_history(line: str) -> bool:
    return any(marker in line for marker in HISTORY_MARKERS)


class TestDocClaims(unittest.TestCase):
    def test_deficit_claims_match_observables(self):
        m = deficit_m()
        # The pin: if this moves, the climb moved, and the docs must move with it.
        self.assertEqual(
            m,
            9,
            f"the deficit recomputes to m={m}, not 9 — update README + the docs "
            "(and this pin) in the same change, never one without the other",
        )

        claims = 0
        for rel in DEFICIT_DOCS:
            for number, line in doc_lines(rel):
                if _is_history(line):
                    continue
                for quoted in M_PATTERN.findall(line) + M_STAYS_PATTERN.findall(line):
                    claims += 1
                    self.assertEqual(
                        int(quoted),
                        m,
                        f"{rel}:{number} claims m = {quoted}, the code recomputes "
                        f"m = {m}: {line.strip()}",
                    )

        self.assertGreater(claims, 0, "no m claim found — the doc list is stale")

    def test_quoted_test_count_matches_suite(self):
        collected = collected_test_count()

        claims = 0
        for rel in TEST_COUNT_DOCS:
            for number, line in doc_lines(rel):
                if "unittest discover -s tests" in line:
                    found = TESTS_PATTERN.findall(line)
                else:
                    found = BADGE_TESTS_PATTERN.findall(line)
                for quoted in found:
                    claims += 1
                    self.assertEqual(
                        int(quoted),
                        collected,
                        f"{rel}:{number} quotes {quoted} tests, the suite collects "
                        f"{collected}: {line.strip()}",
                    )

        self.assertGreater(claims, 0, "no test-count claim found — the doc list is stale")

    def test_landscape_totals_match_data(self):
        files, points, susy = landscape_totals()
        self.assertEqual(files, 14, f"data/ holds {files} h12_*_stats.json files, not 14")
        self.assertEqual(points, 5885, f"data/ holds {points} critical points, not 5885")
        self.assertEqual(susy, 1245, f"data/ holds {susy} SUSY vacua, not 1245")

        claims = 0
        for rel in LANDSCAPE_DOCS:
            for number, line in doc_lines(rel):
                for quoted in (
                    CRITICAL_POINTS_PATTERN.findall(line)
                    + VACUA_TOTAL_PATTERN.findall(line)
                ):
                    claims += 1
                    self.assertEqual(
                        int(quoted.replace(",", "")),
                        points,
                        f"{rel}:{number} quotes {quoted} critical points, the data "
                        f"recomputes {points}: {line.strip()}",
                    )
                for quoted in SUSY_TOTAL_PATTERN.findall(line):
                    claims += 1
                    self.assertEqual(
                        int(quoted.replace(",", "")),
                        susy,
                        f"{rel}:{number} quotes {quoted} SUSY, the data recomputes "
                        f"{susy}: {line.strip()}",
                    )
                for quoted in MODELS_PATTERN.findall(line):
                    claims += 1
                    self.assertEqual(
                        int(quoted),
                        files,
                        f"{rel}:{number} quotes {quoted} models, data/ holds "
                        f"{files}: {line.strip()}",
                    )

        self.assertGreater(claims, 0, "no landscape-total claim found — list is stale")

    def test_every_guarded_doc_exists_and_is_nonempty(self):
        # A renamed/moved doc must fail loudly here, not silently stop being checked.
        for rel in set(DEFICIT_DOCS) | set(LANDSCAPE_DOCS) | set(TEST_COUNT_DOCS):
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"guarded doc {rel} does not exist")
            self.assertGreater(
                len(path.read_text(encoding="utf-8")), 0, f"guarded doc {rel} is empty"
            )


if __name__ == "__main__":
    unittest.main()
