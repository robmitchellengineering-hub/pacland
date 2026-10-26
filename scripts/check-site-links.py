#!/usr/bin/env python3
"""Guard the claims the pacland site makes about itself.

Each assertion below exists because the page once made a claim nobody checked:
  * it names Valiant Verification and an adoption, so the verification page must be reachable;
  * it describes a verification discipline, so the honest "pre-revenue / design partners" line
    must not vanish (that line is what stops the page reading as a product claim);
  * it carries the trust badge once certified, and the badge must state a scope.

exit 0 all present · 1 a claim is present without its support · 2 could not check
"""
from __future__ import annotations
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "web" / "index.html"


def main() -> int:
    try:
        html = PAGE.read_text(encoding="utf-8", errors="replace")
    except OSError as e:  # could not check
        print(f"cannot read {PAGE}: {e}", file=sys.stderr)
        return 2

    # The first check used to be "vvs.morpheus.nz" in html. That is true if ANY of the page's three
    # links to the verification site survives, so when the SDK sabotaged one of them the guard still
    # passed — a mutation that SURVIVED, which means the guard was proving nothing. It now names the
    # exact anchor, so removing or breaking THAT link fails the check.
    checks = {
        "the page carries the named Valiant Verification link":
            '<a href="https://vvs.morpheus.nz">Valiant Verification Systems &rarr;</a>' in html,
        "the page states the verification discipline": "Valiant Verification" in html,
        "the page keeps its honest, pre-revenue line": "design partner" in html.lower(),
    }
    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print(("ok    " if ok else "FAIL  ") + name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
