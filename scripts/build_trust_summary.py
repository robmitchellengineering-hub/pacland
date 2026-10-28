#!/usr/bin/env python3
"""Regenerate the trust-board summary line in web/index.html from `pacland.trust.board()`.

The line was hand-typed and had gone stale — it claimed 29 artifacts / 14 broken / 4 weak / 11 clean
while the board actually held 42 (14 broken, 9 weak, 19 clean). A count in a hand-written page is a
claim that rots; this makes the page quote the tool.

    python3 scripts/build_trust_summary.py
"""
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland import trust  # noqa: E402

PAGE = ROOT / "web" / "index.html"
START = "<!-- trust-summary:start -->"
END = "<!-- trust-summary:end -->"


def summary_line() -> str:
    board = trust.board()
    counts = Counter(e.tier for e in board)
    disciplines = Counter(e.discipline for e in board)
    return (f"{START}<code>pacland trust</code> ranks <strong>{len(board)} artifacts</strong> today — "
            f"{counts['broken']} broken, {counts['weak']} weak, {counts['clean']} clean — across "
            f"{len(disciplines)} disciplines ({', '.join(f'{d} {n}' for d, n in sorted(disciplines.items()))})."
            f"{END}")


def main() -> int:
    page = PAGE.read_text()
    start = page.find(START)
    end = page.find(END)
    if start == -1:
        # first run: wrap the hand-typed sentence so future runs can replace it
        needle = ("<code>pacland trust</code> ranks 29 artifacts today — "
                  "<strong>14 broken, 4 weak, 11 clean</strong>.")
        if needle not in page:
            raise SystemExit("could not find the trust summary line to replace")
        page = page.replace(needle, summary_line())
    else:
        page = page[:start] + summary_line() + page[end + len(END):]
    PAGE.write_text(page)
    print("trust summary:", summary_line().replace(START, "").replace(END, ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
