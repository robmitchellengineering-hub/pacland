#!/usr/bin/env python3
"""Regenerate or verify the hypothesis cross-reference.

    python3 scripts/hypotheses.py            # write docs/hypotheses.md
    python3 scripts/hypotheses.py --check    # exit 1 on drift or a broken wall link
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import hypotheses as H  # noqa: E402

TARGET = ROOT / "docs" / "hypotheses.md"


def main(argv) -> int:
    link = H.check_links()
    if not link["ok"]:
        print(f"broken wall links: {link['missing']} too few walls: {link['too_few_walls']}", file=sys.stderr)
        return 1
    art = H.check_artefacts()
    if not art["ok"]:
        print(f"claims-registry rule: decided without a script {art['decided_without_a_script']}; "
              f"named script missing {art['named_script_missing']}", file=sys.stderr)
        return 1
    text = H.render()
    if "--check" in argv:
        current = TARGET.read_text(encoding="utf-8") if TARGET.is_file() else ""
        if current != text:
            print(f"drift: {TARGET.relative_to(ROOT)} does not match the register", file=sys.stderr)
            return 1
        print("hypothesis register is up to date and every wall link resolves")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    c = H.counts()
    print(f"wrote {TARGET.relative_to(ROOT)}: {c['total']} hypotheses ({c['open']} open)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
