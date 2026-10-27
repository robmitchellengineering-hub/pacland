"""A second real-time archive: do the two agree, and does the check notice a stale vintage?"""
import unittest

from pacland.economics import second_archive as sa


class TestAgreement(unittest.TestCase):
    def test_the_two_archives_agree(self):
        a = sa.agreement()
        self.assertTrue(a["agree"], a["verdict"])
        self.assertGreater(a["n"], 100)

    def test_agreement_is_exact_not_approximate(self):
        a = sa.agreement()
        self.assertEqual(a["n_exact"], a["n"])
        self.assertEqual(a["worst"]["diff"], 0.0)

    def test_more_than_one_vintage_is_compared(self):
        self.assertGreaterEqual(sa.agreement()["vintages"], 3)


class TestSeededFault(unittest.TestCase):
    def test_a_stale_vintage_is_detected(self):
        ok, msg = sa.guard_stale_vintage()
        self.assertTrue(ok, msg)


class TestAudit(unittest.TestCase):
    def test_the_audit_is_green(self):
        self.assertTrue(sa.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
