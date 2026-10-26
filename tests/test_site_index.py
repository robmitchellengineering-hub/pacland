"""The site index cannot drift from the repo."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bsi", ROOT / "scripts" / "build_site_index.py")


def _builder():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestIndexIsCurrent(unittest.TestCase):
    def test_committed_index_matches_the_repo(self):
        committed = json.loads((ROOT / "web" / "index.json").read_text())
        built = _builder().build()
        self.assertEqual(committed["items"], built["items"],
                         "web/index.json is stale — run python3 scripts/build_site_index.py")
        self.assertEqual(committed["start"], built["start"])
        self.assertEqual(committed["commands"], built["commands"])

    def test_every_item_has_a_title_and_a_destination(self):
        for item in json.loads((ROOT / "web" / "index.json").read_text())["items"]:
            self.assertTrue(item["title"].strip(), item)
            # docs/scripts/pdfs live on GitHub; site pages are relative to this site
            self.assertTrue(item["href"].startswith(("http", "./")), item)

    def test_the_kinds_are_the_ones_the_page_filters(self):
        kinds = {i["kind"] for i in json.loads((ROOT / "web" / "index.json").read_text())["items"]}
        self.assertEqual(kinds, {"doc", "script", "pdf", "page"})

    def test_start_here_points_at_real_paths(self):
        for entry in json.loads((ROOT / "web" / "index.json").read_text())["start"]:
            self.assertTrue((ROOT / pathlib.Path(entry["path"])).exists(), entry["path"])

    def test_no_shebang_leaks_into_a_summary(self):
        for item in json.loads((ROOT / "web" / "index.json").read_text())["items"]:
            self.assertFalse(item["summary"].startswith("!"), item["title"])
            self.assertNotIn("usr/bin/env", item["summary"], item["title"])

    def test_truncated_summaries_say_they_were_truncated(self):
        for item in json.loads((ROOT / "web" / "index.json").read_text())["items"]:
            self.assertLessEqual(len(item["summary"]), 191, item["title"])
            if item["summary"].endswith("…"):
                self.assertFalse(item["summary"].endswith(" …"), item["title"])

    def test_the_page_exists_and_loads_the_index(self):
        page = (ROOT / "web" / "all.html").read_text()
        self.assertIn("index.json", page)
        self.assertIn('id="q"', page)


if __name__ == "__main__":
    unittest.main()
