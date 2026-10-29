"""The site's two honest claims, as guards that can fail.

WHY THIS FILE EXISTS. `mutations.json` recorded two proofs as prose — "replace 'seeking design partners'
with 'seeking customers'", "replace the verification link with '#'" — with no file, find, replace or check.
Nobody could re-run them, and the SDK's `sample-proofs` refused both, correctly: a proof that cannot be
re-executed is a claim.

These are the same two claims as checks. Break the site's honesty line or its climate evidence link and one
of these fails.
"""
import unittest
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "web" / "index.html"


class SiteClaims(unittest.TestCase):
    def setUp(self):
        self.html = SITE.read_text(encoding="utf-8")

    def test_states_design_partners_not_customers(self):
        """The honest line: pre-revenue, seeking design partners — not customers."""
        self.assertIn("seeking design partners", self.html)
        self.assertNotIn("seeking customers", self.html)

    def test_climate_evidence_links_to_the_cmip6_writeup(self):
        """The climate section links to the real write-up, and no link is a placeholder."""
        self.assertIn("docs/climate-cmip6-drift.md", self.html)
        self.assertNotIn('href="#"', self.html)


if __name__ == "__main__":
    unittest.main()
