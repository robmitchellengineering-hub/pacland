"""The execution gate must catch the exact violation Rob reported."""
import unittest

from pacland.exactness import execution as X


class TestTheViolation(unittest.TestCase):
    def test_asking_the_operator_while_ssh_works_raises(self):
        # this is the 2026-10-31 incident: a wifi survey request with a working key on a radio:wifi node
        with self.assertRaises(X.ExecutionGateError):
            X.check({"local": False, "ssh": True, "mesh": True}, "asked_operator")

    def test_asking_the_operator_while_only_the_mesh_works_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check({"mesh": True}, "asked_operator")

    def test_asking_with_no_path_is_conformant(self):
        rec = X.check({}, "asked_operator")
        self.assertTrue(rec["conformant"])
        self.assertEqual(rec["gate"], "execution-attempt@1")


class TestTheHonestOutcomes(unittest.TestCase):
    def test_ran_via_mesh_is_conformant(self):
        self.assertTrue(X.check({"mesh": True}, "ran")["conformant"])

    def test_refused_by_the_environment_is_conformant(self):
        # the iw-not-installed case: tried, refused, exit 0 with the reason
        self.assertTrue(X.check({"ssh": True}, "refused_by_environment")["conformant"])

    def test_claiming_a_run_with_no_attempt_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check({}, "ran")

    def test_claiming_no_path_while_one_worked_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check({"local": True}, "no_path_exists")

    def test_an_unknown_outcome_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check({"local": True}, "tried_really_hard")


if __name__ == "__main__":
    unittest.main()


class TestOperatorAskGate(unittest.TestCase):
    """The second incident: asked to unplug Ethernet while the agent could reach the machine."""

    def test_asking_while_ssh_works_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check_operator_ask({"ssh": True}, "asked_operator", what="join the Legion to Wi-Fi")

    def test_asking_while_a_stored_credential_exists_raises(self):
        # the real case: a saved Wi-Fi profile needs no password to be typed by anyone
        with self.assertRaises(X.ExecutionGateError):
            X.check_operator_ask({"stored_cred": True}, "asked_operator", what="connect the Wi-Fi")

    def test_asking_while_the_mesh_can_run_the_job_raises(self):
        with self.assertRaises(X.ExecutionGateError):
            X.check_operator_ask({"mesh": True}, "asked_operator", what="read the link speed")

    def test_asking_with_every_channel_closed_is_conformant_and_must_say_so(self):
        rec = X.check_operator_ask({}, "asked_operator", what="plug in a cable")
        self.assertTrue(rec["conformant"])
        self.assertIn("no channel open", rec["note"])

    def test_not_asking_is_always_conformant(self):
        self.assertTrue(X.check_operator_ask({"ssh": True}, "ran")["conformant"])
