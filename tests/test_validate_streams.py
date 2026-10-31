"""The validation harness must be able to say FALSIFIED, or it is decoration."""
import io
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
import validate_streams as V  # noqa: E402


def write(rows):
    p = pathlib.Path(tempfile.mkdtemp()) / "v.csv"
    p.write_text("x,y,z,nss,snr_db\n" + "\n".join(rows) + "\n")
    return p


def run(path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        V.main(["--room", "3,4,2.5", "--band", "5.18", "--ap", "1.5,2.0,2.4", "--data", str(path)])
    return buf.getvalue()


class TestValidation(unittest.TestCase):
    def test_a_measurement_beating_the_ceiling_falsifies(self):
        # 4 of 4 measured where the model tops out at 3 is the low-side failure
        out = run(write(["0.5,1.2,0.9,4,20.0", "2.6,3.4,0.9,4,20.0", "1.5,2.0,1.2,4,20.0"]))
        self.assertIn("FALSIFIED", out)

    def test_hardware_far_below_the_ceiling_falsifies_the_high_side(self):
        out = run(write(["0.5,1.2,0.9,1,20.0", "2.6,3.4,0.9,1,20.0", "1.5,2.0,1.2,1,20.0"]))
        self.assertIn("FALSIFIED", out)

    def test_a_small_shortfall_is_consistent(self):
        out = run(write(["0.5,1.2,0.9,3,20.0", "2.6,3.4,0.9,3,20.0", "1.5,2.0,1.2,3,20.0"]))
        self.assertIn("CONSISTENT", out)

    def test_an_empty_table_is_refused(self):
        p = pathlib.Path(tempfile.mkdtemp()) / "v.csv"
        p.write_text("x,y,z,nss,snr_db\n")
        self.assertIn("REFUSED", run(p))


if __name__ == "__main__":
    unittest.main()
