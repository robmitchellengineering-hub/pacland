#!/usr/bin/env python3
"""Verify a certificate set offline — the check a stranger can run.

    python3 scripts/verify_certificates.py [path-to-repo]

Three things are checked, and each is reported whether it passes or not:

1. the manifest carries an OpenSSH signature that verifies against the committed
   ``allowed_signers`` (no network, no account, no trust in this machine);
2. every artifact on disk matches the sha256 the manifest records for it;
3. the manifest declares the format it claims to.

Exit 0 only when all three hold. This is the command a reviewer, a journal or a customer runs; it
does not need this repository's source, only the certificate directory and the ``ssh-keygen`` that
ships with every macOS and Linux system.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify.integrity import verify_set  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in ("-h", "--help")):
        print(__doc__)
        return 0 if len(argv) == 2 else 2
    root = pathlib.Path(argv[1]) if len(argv) == 2 else ROOT
    result = verify_set(root)
    for ok, message in result["checks"]:
        print(f"  {'ok  ' if ok else 'FAIL'} {message}")
    if result["ok"]:
        print(f"\nPASS: {len(result['checks'])} checks from {root} — verified offline")
        return 0
    print(f"\nFAIL: {len(result['failures'])} problem(s):")
    for failure in result["failures"]:
        print(f"  - {failure}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
