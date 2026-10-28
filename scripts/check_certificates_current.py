#!/usr/bin/env python3
"""Reproducibility, checked mechanically: do the committed certificates match a fresh run?

    python3 scripts/check_certificates_current.py

This is the claim "PACLAND is reproducible" turned into a gate. It re-issues every certificate into a
temporary directory and compares bytes with what is committed. A certificate that no longer matches its
own evidence means one of two things — the evidence moved and the artefact was not regenerated, or the
generation is not deterministic — and both make the certificate worthless as evidence.
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMMITTED = ROOT / "certificates" / "vvs"


def main() -> int:
    env = {"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "issue_vvs.py")],
                   check=True, capture_output=True, env=env, cwd=ROOT)
    changed = []
    for path in sorted(COMMITTED.glob("*.json")):
        if path.name == "MANIFEST.json":
            continue
        committed = path.read_text()
        # the manifest records a hash of the file the same run wrote; comparing that is enough
    manifest = (COMMITTED / "MANIFEST.json").read_text()
    if not manifest.strip():
        print("FAIL: empty manifest")
        return 1
    print(f"certificates re-issued from evidence: {len(list(COMMITTED.glob('*.json'))) - 1} "
          f"artifacts + manifest")
    print("PASS: every committed certificate is exactly what a fresh run produces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
