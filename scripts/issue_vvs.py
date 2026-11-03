#!/usr/bin/env python3
"""Issue Valiant Verification certificates for every part that PASSES, and a freshness manifest.

    python3 scripts/issue_vvs.py [--out DIR]

The VVS specification (spec.md §3, the named-gate contract) says a build may claim "verified" only
when it presents, per required gate: the gate name, the result, the evidence, the producer, and the
falsifier. This writes that shape — plus `MANIFEST.json`, which records the sha256 of every artifact
so a third party can tell whether the certificate they are reading is the one this repository produces.

``--out DIR`` writes a complete set under a different root, which is how the reproducibility gate
(`scripts/check_certificates_current.py`) compares a fresh issue with the committed one without
overwriting the bytes it is about to test. Issuing is content; `scripts/sign_manifest.py` is
attestation, and runs separately so a signature is a deliberate act.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify import dossiers as D  # noqa: E402


def out_dirs(argv: list[str]) -> tuple[pathlib.Path, pathlib.Path]:
    """(certificates, site copy) for this run. ``--out DIR`` re-issues elsewhere."""
    base = ROOT
    if "--out" in argv:
        index = argv.index("--out")
        if index + 1 >= len(argv):
            raise SystemExit("--out needs a directory")
        base = pathlib.Path(argv[index + 1])
    return base / "certificates" / "vvs", base / "web" / "vvs"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    out, web = out_dirs(argv)
    out.mkdir(parents=True, exist_ok=True)
    web.mkdir(parents=True, exist_ok=True)
    manifest = {"format": "valiant-verification/manifest@1", "artifacts": {}}
    issued = 0
    for name in sorted(D.DOSSIERS):
        cert = D.DOSSIERS[name]()
        vvs = cert.to_vvs()
        payload = json.dumps(vvs, indent=2) + "\n"
        markdown = cert.to_vvs_markdown()
        target = out / f"{name}.json"
        target.write_text(payload)
        (out / f"{name}.md").write_text(markdown)
        (web / f"{name}.json").write_text(payload)
        (web / f"{name}.md").write_text(markdown)
        manifest["artifacts"][name] = {
            "subject": cert.subject, "sector": cert.sector, "grade": cert.grade,
            "verified": vvs["verified"],
            "gates_passed": vvs["gates_passed"], "gates_required": vvs["gates_required"],
            "sha256": sha256(target),
        }
        if vvs["verified"]:
            issued += 1
        print(f"{name:16} {cert.grade:10} verified={str(vvs['verified']):5} "
              f"gates {vvs['gates_passed']}/{vvs['gates_required']}")
    blob = json.dumps(manifest, indent=2) + "\n"
    (out / "MANIFEST.json").write_text(blob)
    (web / "MANIFEST.json").write_text(blob)
    print(f"\n{issued} of {len(D.DOSSIERS)} parts verified under the named-gate contract")
    print("next: python3 scripts/sign_manifest.py   (issuing is content; signing is attestation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
