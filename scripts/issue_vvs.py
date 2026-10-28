#!/usr/bin/env python3
"""Issue Valiant Verification certificates for every part that PASSES, and a freshness manifest.

    python3 scripts/issue_vvs.py

The VVS specification (spec.md §3, the named-gate contract) says a build may claim "verified" only
when it presents, per required gate: the gate name, the result, the evidence, the producer, and the
falsifier. This writes that shape — plus `MANIFEST.json`, which records the sha256 of every artifact
so a third party can tell whether the certificate they are reading is the one this repository produces.
"""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify import dossiers as D  # noqa: E402

OUT = ROOT / "certificates" / "vvs"
WEB = ROOT / "web" / "vvs"   # the site needs its own copy: deploy mirrors web/


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    manifest = {"format": "valiant-verification/manifest@1", "artifacts": {}}
    issued = 0
    for name in sorted(D.DOSSIERS):
        cert = D.DOSSIERS[name]()
        vvs = cert.to_vvs()
        payload = json.dumps(vvs, indent=2) + "\n"
        markdown = cert.to_vvs_markdown()
        target = OUT / f"{name}.json"
        target.write_text(payload)
        (OUT / f"{name}.md").write_text(markdown)
        (WEB / f"{name}.json").write_text(payload)
        (WEB / f"{name}.md").write_text(markdown)
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
    (OUT / "MANIFEST.json").write_text(blob)
    (WEB / "MANIFEST.json").write_text(blob)
    print(f"\n{issued} of {len(D.DOSSIERS)} parts verified under the named-gate contract")
    print(f"manifest: certificates/vvs/MANIFEST.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
