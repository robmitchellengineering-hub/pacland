#!/bin/sh
# run-tests.sh — the test suite, as a gate, in a checkout that was never pip-installed.
#
# WHY. `python3 -m unittest discover -s tests` passes 557 tests on the author's machine because
# pacland is pip-installed there. The Valiant SDK runs a repo's gate in whatever checkout it is
# pointed at, and in a clean clone the package is not importable — so the gate reported
# "Ran 546 tests, FAILED (errors=1)" on a repo whose suite is green, and the adoption looked broken
# when nothing was. PYTHONPATH=src makes the gate independent of an install step nobody declared.
#
# exit 0 suite green · non-zero a real failure (unittest writes its summary to stderr, which is why
# the gate declares expectStderr).
set -eu
cd "$(dirname "$0")/.."
exec env PYTHONPATH=src python3 -m unittest discover -s tests -q
