"""The Lean scraper: Mathlib search (the bigger library of truths) + external repo scraping."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from pacland import registry, lean_scrape


class TestLeanScrape(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_mathlib_is_present_and_huge(self):
        d = lean_scrape.mathlib_dir()
        if d is None:
            self.skipTest("Mathlib not present locally")
        n = lean_scrape.count_mathlib_theorems(d)
        self.assertGreater(n, 100_000)  # the library of empirical truths is genuinely large

    def test_search_mathlib_finds_spectral_gap(self):
        d = lean_scrape.mathlib_dir()
        if d is None:
            self.skipTest("Mathlib not present locally")
        hits = lean_scrape.search_mathlib("spectral gap", dir=d, limit=5)
        if not hits:  # "spectral gap" may be written as one word
            hits = lean_scrape.search_mathlib("spectral", dir=d, limit=5)
        self.assertTrue(hits)
        self.assertTrue(all(h["name"] for h in hits))

    def test_ingest_mathlib_hits_registers_tier1_properties(self):
        d = lean_scrape.mathlib_dir()
        if d is None:
            self.skipTest("Mathlib not present locally")
        r = lean_scrape.ingest_mathlib_hits("spectral", limit=3)
        self.assertEqual(r["ingested"], 3)
        for name in r["names"]:
            p = registry.get("property", f"ext:mathlib:lean-{name}")
            self.assertIsNotNone(p)
            self.assertEqual(p["payload"]["tier"], 1)

    def test_scrape_local_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            # build a tiny local git repo with one .lean file
            repo = Path(tmp) / "repo"
            repo.mkdir()
            (repo / "T.lean").write_text("theorem my_theorem : True := by trivial\n"
                                          "lemma my_lemma : True := by trivial\n")
            for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "t@t"],
                        ["git", "config", "user.name", "t"], ["git", "add", "-A"],
                        ["git", "commit", "-q", "-m", "x"]):
                subprocess.run(cmd, cwd=str(repo), check=True)
            r = lean_scrape.scrape_github_lean(f"file://{repo}", source="local-test", tmp=tmp)
            self.assertEqual(r["lean_theorems"], 2)
            self.assertEqual(r["source"], "local-test")

    def test_scrape_github_search_harvests_multiple_repos(self):
        with tempfile.TemporaryDirectory() as tmp:
            repos = []
            for i, name in enumerate(("researcher-a", "researcher-b")):
                repo = Path(tmp) / name
                repo.mkdir()
                (repo / f"T{i}.lean").write_text(f"theorem t_{name}_{i} : True := by trivial\n")
                for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "t@t"],
                            ["git", "config", "user.name", "t"], ["git", "add", "-A"],
                            ["git", "commit", "-q", "-m", "x"]):
                    subprocess.run(cmd, cwd=str(repo), check=True)
                repos.append((f"file://{repo}", name))
            # inject the search so the test runs offline
            r = lean_scrape.scrape_github_search("test", limit=2, tmp=tmp,
                                                 _search=lambda q, n: repos)
            self.assertEqual(r["total_theorems"], 2)
            self.assertEqual(len(r["repos"]), 2)


if __name__ == "__main__":
    unittest.main()
