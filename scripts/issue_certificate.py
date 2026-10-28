#!/usr/bin/env python3
"""Issue model-risk certificates from this repository's own evidence.

    python3 scripts/issue_certificate.py --all
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify import dossiers as D  # noqa: E402

OUT = ROOT / "certificates"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("subject", nargs="?", choices=sorted(D.DOSSIERS) + ["all"], default="all")
    ap.add_argument("--all", action="store_true", help="issue every dossier (the default)")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    names = sorted(D.DOSSIERS) if (args.all or args.subject == "all") else [args.subject]
    for name in names:
        cert = D.DOSSIERS[name]()
        (OUT / f"{name}.md").write_text(cert.to_markdown())
        (OUT / f"{name}.json").write_text(cert.to_json())
        print(f"{name:16} {cert.grade:10} {len(cert.findings)} findings")
        print(f"  {cert.headline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
