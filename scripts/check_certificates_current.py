#!/usr/bin/env python3
"""Reproducibility and integrity, checked mechanically.

    python3 scripts/check_certificates_current.py

This is the claim "PACLAND is reproducible" turned into a gate. It does three things and refuses to
pass unless all three hold:

1. **Reproduce** — re-issues every certificate into a temporary directory (never over the committed
   bytes it is about to test) and compares the result byte-for-byte with what is committed. A
   certificate that no longer matches its own evidence means the evidence moved without the artefact
   being regenerated, or the generation is not deterministic; both make the certificate worthless.
2. **Bind** — verifies the manifest's OpenSSH signature against the committed ``allowed_signers``,
   offline, with no key of its own.
3. **Match** — verifies that every artifact on disk is the file the signed manifest records.

Exit 1 on any difference, naming the file. It writes nothing outside its own temp directory.
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify.integrity import (  # noqa: E402
    CERT_DIR, WEB_DIR, compare_trees, verify_set,
)


def main() -> int:
    env = {"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
    with tempfile.TemporaryDirectory(prefix="pacland-certificates-") as tmp:
        tmp_root = pathlib.Path(tmp)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "issue_vvs.py"), "--out", str(tmp_root)],
            capture_output=True, env=env, cwd=ROOT,
        )
        if proc.returncode != 0:
            print("FAIL: a fresh issue did not complete — nothing below can be compared")
            print(proc.stdout.decode("utf-8", "replace")[-2000:])
            print(proc.stderr.decode("utf-8", "replace")[-2000:])
            return 1
        problems = (compare_trees(ROOT / CERT_DIR, tmp_root / CERT_DIR)
                    + compare_trees(ROOT / WEB_DIR, tmp_root / WEB_DIR))

    result = verify_set(ROOT)
    for ok, message in result["checks"]:
        print(f"  {'ok  ' if ok else 'FAIL'} {message}")

    if problems:
        print(f"\nFAIL: the committed certificates are not what a fresh issue produces "
              f"({len(problems)} file(s)):")
        for problem in problems:
            print(f"  - {problem}")
        print("\n  fix: python3 scripts/issue_vvs.py && python3 scripts/sign_manifest.py, then commit")
        return 1
    if not result["ok"]:
        print(f"\nFAIL: {len(result['failures'])} integrity problem(s)")
        return 1

    artifacts = len(list((ROOT / CERT_DIR).glob("*.json"))) - 1
    print(f"\nPASS: {artifacts} artifacts reproduce byte-for-byte and the set verifies offline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
