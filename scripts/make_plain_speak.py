#!/usr/bin/env python3
"""Render the plain-speak one-pagers.

Two pages, one per discipline, written for a Year 10 student and readable by a specialist
in two minutes. Regenerate after changing src/pacland/plain_speak.py:

    python3 scripts/make_plain_speak.py

Outputs to the repo root as PACLAND-{discipline}-plain-speak.pdf, because the front-page
cards link to those exact filenames.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.explainer import render  # noqa: E402
from pacland import plain_speak  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for name, entries in plain_speak.all_pages().items():
        out = ROOT / f"PACLAND-{name}-plain-speak.pdf"
        render(entries, str(out), compact=True)
        words = sum(len(t.split()) for _, t in entries)
        print(f"wrote {out.name}  ({words} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
