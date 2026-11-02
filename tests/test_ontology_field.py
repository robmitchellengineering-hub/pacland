"""Maudlin's test, made mechanical: every recorded claim names what it postulates, and "none" is first class."""
import unittest

from pacland.exactness.observability import Reading


def _reading(**kw):
    base = dict(quantity="x", estimate=0.5, ci_low=0.4, ci_high=0.6, n_used=10, n_total=10,
                parameter_spread=None, coverage=None, verdict="measured", why="because")
    base.update(kw)
    return Reading(**base)


class TestTheFieldExists(unittest.TestCase):
    def test_it_defaults_to_none(self):
        # a claim that does not state its ontology is recorded as such, not left ambiguous
        self.assertEqual(_reading().postulates, "none")
        self.assertEqual(_reading().ontology, "none")

    def test_a_stated_postulate_is_classified_as_stated(self):
        r = _reading(postulates="a universal quantum state and a spacetime with a preferred foliation")
        self.assertEqual(r.ontology, "stated")

    def test_whitespace_and_case_do_not_smuggle_an_empty_ontology(self):
        self.assertEqual(_reading(postulates="   ").ontology, "none")
        self.assertEqual(_reading(postulates="NONE").ontology, "none")


class TestThePoint(unittest.TestCase):
    def test_a_claim_with_no_ontology_is_marked_not_hidden(self):
        # Maudlin [01:22:16]: "First you want to understand what is it you're postulating... The evidence for what?"
        # A framework with no postulate cannot be refuted; this makes that visible at the record level.
        r = _reading()
        self.assertEqual(r.ontology, "none")
        self.assertIn(r.verdict, {"measured", "sample-limited", "parameter-limited"})


if __name__ == "__main__":
    unittest.main()
