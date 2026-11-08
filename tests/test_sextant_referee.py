"""The SEXTANT hardware referee: a quantum device is classified, never assumed.

The referee's whole job is to say CERTIFIED / REFUSED / UNKNOWN against kernel-checked bounds.
These tests are the falsifiers: the referee must be able to refuse a doctored device, certify a
genuinely quantum one, and stay silent (UNKNOWN) on absence — never pass by absence (rule 67).
"""
import math
import unittest

from pacland import phantom
from pacland import sextant_referee as sr


class TestRefuseImpossible(unittest.TestCase):
    def test_a_device_past_tsirelson_is_refused(self):
        """S = 3.0 exceeds 2√2; no quantum state does this. Must be REFUSED, never certified."""
        r = sr.referee(sr.probe_devices()["cheating"])
        self.assertEqual(r["verdict"], sr.REFUSED)
        self.assertTrue(any(c["verdict"] == sr.IMPOSSIBLE for c in r["certificates"]))

    def test_refusal_carries_the_exact_certificate(self):
        r = sr.referee(sr.probe_devices()["cheating"])
        c = r["certificates"][0]
        self.assertAlmostEqual(c["S"], 3.0, places=3)
        self.assertIn("QM.Tsirelson", c["theorem"])
        self.assertIn("fraud", c["why"])


class TestCertifyQuantum(unittest.TestCase):
    def test_a_device_at_the_quantum_max_is_certified(self):
        """S = 2√2 is the Tsirelson bound; a device at it demonstrates entanglement."""
        r = sr.referee(sr.probe_devices()["quantum"])
        self.assertEqual(r["verdict"], sr.CERTIFIED)
        self.assertTrue(any(c["verdict"] == sr.FORCED for c in r["certificates"]))

    def test_certification_rides_on_the_bell_wall(self):
        c = sr.referee(sr.probe_devices()["quantum"])["certificates"][0]
        self.assertAlmostEqual(c["S"], 2 * math.sqrt(2), places=3)
        self.assertIn("QM.CHSH", c["theorem"])


class TestAbsentIsUnknown(unittest.TestCase):
    def test_an_empty_record_is_unknown_never_certified(self):
        r = sr.referee(sr.probe_devices()["empty"])
        self.assertEqual(r["verdict"], sr.UNKNOWN)
        self.assertEqual(r["certificates"], [])

    def test_a_classical_device_is_not_certified_quantum(self):
        """S = 2.0 sits at the Bell wall: consistent with local hidden variables, no entanglement."""
        r = sr.referee(sr.probe_devices()["classical"])
        self.assertEqual(r["verdict"], sr.UNKNOWN)


class TestSignificanceModel(unittest.TestCase):
    def test_a_bare_excess_is_not_enough_without_significance(self):
        """A small S = 2.01 with few shots stays UNKNOWN (within 5 sigma of the wall)."""
        dev = {"circuits": {"chsh": {
            "expectations": {"00": .5025, "01": .5025, "10": .5025, "11": -.5025}, "shots": 100}}}
        self.assertEqual(sr.referee(dev)["verdict"], sr.UNKNOWN)

    def test_classify_chsh_returns_the_three_verdicts(self):
        self.assertEqual(sr.classify_chsh(3.0, 0.001, k=5.0)[0], sr.IMPOSSIBLE)
        self.assertEqual(sr.classify_chsh(2.83, 0.001, k=5.0)[0], sr.FORCED)
        self.assertEqual(sr.classify_chsh(2.0, 0.001, k=5.0)[0], sr.UNKNOWN)


class TestPhantomSelfTest(unittest.TestCase):
    def test_the_referee_certifies_phantoms_own_quantum_device(self):
        """Phantom computes S=2√2 from the Bell state; the referee must certify that device —
        the referee and the simulator agree, end to end, without a hand-coded constant."""
        dev = {"circuits": {"chsh": {"expectations": phantom.chsh_expectations(), "shots": 10**6}}}
        self.assertEqual(sr.referee(dev)["verdict"], sr.CERTIFIED)

    def test_the_referee_does_not_certify_phantoms_classical_wall(self):
        """Phantom's classical wall is S=2; a device there shows no entanglement and is UNKNOWN."""
        e = phantom.bell_classical() / 4.0  # E00=E01=E10=e, E11=-e  =>  S = 4e = 2
        dev = {"circuits": {"chsh": {
            "expectations": {"00": e, "01": e, "10": e, "11": -e}, "shots": 10**6}}}
        self.assertEqual(sr.referee(dev)["verdict"], sr.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
