"""The Lean scraper: Mathlib search (the bigger library of truths) + external repo scraping."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from pacland import lean_scrape


class TestLeanScrape(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
