"""The well-posedness audit must cite real modules and populate BOTH classes.

This guards the reply to Woit's charge: a page that claims some results are theorems and others are demoted is only
worth anything if the cited modules exist and if neither list is empty (an empty "demoted" list would mean we had
not actually conceded anything).
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "well-posedness-reply.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


class TestTheReplyExists(unittest.TestCase):
    def test_the_doc_is_present(self):
        self.assertTrue(DOC.is_file())

    def test_it_answers_woit_by_name_and_timestamp(self):
        t = _text()
        self.assertIn("Woit", t)
        self.assertIn("01:06:35", t)
        self.assertIn("01:05:56", t)

    def test_it_states_the_criterion(self):
        t = _text()
        self.assertIn("theorem or an exact count", t)
        self.assertIn("sampling with a budget", t)


class TestTheTwoListsAreReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _text()

    def test_every_cited_module_path_exists(self):
        cited = set(re.findall(r"`((?:exactness|periods|spectral)/[a-z_]+\.py)`", self.text))
        self.assertGreaterEqual(len(cited), 4, f"too few module citations: {cited}")
        for rel in cited:
            self.assertTrue((ROOT / "src" / "pacland" / rel).is_file(), rel)

    def test_the_well_posed_list_names_a_theorem(self):
        self.assertIn("max |N| = b3", self.text)
        self.assertIn("theorem", self.text)

    def test_the_demoted_list_is_not_empty(self):
        # a concession list is the point; an empty one means nothing was conceded
        self.assertIn("NOT claim is well-posed", self.text)
        self.assertIn("accessibility minimum", self.text)
        self.assertIn("measure-dependence", self.text)
        self.assertIn("demoted", self.text)

    def test_it_names_a_reproduced_measured_number(self):
        self.assertIn("6.4e-13", self.text)


if __name__ == "__main__":
    unittest.main()
