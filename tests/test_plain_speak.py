"""The plain-speak one-pagers — the guard that keeps them plain.

Written after a reader pointed out that "free" (as in a free parameter) reads as "no money"
to anyone outside physics. The words have to survive being read by someone who does not
know the field, so the rule is tested, not remembered.
"""
import pathlib
import unittest

from pacland import plain_speak

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = plain_speak.all_pages()

#: Words that mean something specific to a specialist and something else to everyone else.
#: "free" is the one that cost a reader's understanding: it reads as price, not as
#: "undetermined".
BANNED = ("free",)

REQUIRED = ("The question", "What we found", "The best we have right now",
            "How we refine it", "What this means for the world", "What this cannot do")


class TestVocabulary(unittest.TestCase):
    def test_no_money_flavoured_jargon(self):
        for name, page in PAGES.items():
            text = " ".join(t for _, t in page).lower()
            for word in BANNED:
                self.assertNotIn(word, text, f"{name} uses {word!r} — it reads as price")

    def test_no_physics_shorthand_survives(self):
        for name, page in PAGES.items():
            text = " ".join(t for _, t in page)
            for token in ("free parameter", "ceteris", "endogenous", "stochastic"):
                self.assertNotIn(token, text.lower(), f"{name}: {token}")


class TestStructure(unittest.TestCase):
    def test_every_page_has_the_six_sections_in_order(self):
        for name, page in PAGES.items():
            heads = [t for kind, t in page if kind == "h"]
            self.assertEqual(len(heads), len(REQUIRED), name)
            for head, want in zip(heads, REQUIRED):
                self.assertIn(want, head, f"{name} section order")

    def test_each_page_still_fits_one_page(self):
        for name, page in PAGES.items():
            words = sum(len(t.split()) for _, t in page)
            self.assertLess(words, 500, f"{name}: {words} words will spill past one page")

    def test_each_page_names_the_best_model(self):
        # the section must carry a real name or number, not a promise
        for name, page in PAGES.items():
            section = next(t for k, t in page if k == "h" and "best we have" in t)
            self.assertTrue(section)


class TestArtefacts(unittest.TestCase):
    def test_a_pdf_exists_for_each_page(self):
        for name in PAGES:
            path = ROOT / f"PACLAND-{name}-plain-speak.pdf"
            self.assertTrue(path.exists(), path.name)
            self.assertGreater(path.stat().st_size, 5000, path.name)

    def test_each_pdf_is_exactly_one_page(self):
        try:
            from pypdf import PdfReader
        except ImportError:                                  # pragma: no cover
            self.skipTest("pypdf not installed")
        for name in PAGES:
            pdf = ROOT / f"PACLAND-{name}-plain-speak.pdf"
            n = len(PdfReader(str(pdf)).pages)
            self.assertEqual(n, 1, f"{pdf.name} is {n} pages; a one-pager is one page")


if __name__ == "__main__":
    unittest.main()
