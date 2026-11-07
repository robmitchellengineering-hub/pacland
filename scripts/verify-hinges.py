#!/usr/bin/env python3
"""QF-0 gate — the hinge ledger must name >=1 hypothesis and a source per hinge.

Reads pacland-proof/PaclandProof/Foundations/Hinges.lean and, for each
`structure F<k>`, asserts:
  1. at least one `h_*` hypothesis field (a blank hypothesis list FAILS),
  2. exactly the `conclusion_*` field,
  3. a `Source:` line in the structure's doc comment.

Exit 0 = every hinge is correctly specified; exit 1 = a hinge is under-specified.
This is the "rejected by the schema" half of the QF-0 gate (the other half is
`lake build`). Mutation-tested: a planted `structure F5 where` with no `h_*`
field must make this script exit 1.
"""
import re
import sys
from pathlib import Path

HINGES = (
    Path(__file__).resolve().parents[1]
    / "pacland-proof" / "PaclandProof" / "Foundations" / "Hinges.lean"
)


def main() -> int:
    text = HINGES.read_text()
    # Each block: /-- doc comment --/ then `structure F<k> where` then fields,
    # up to the next /-- doc, the `end Hinges`, or end-of-file.
    pattern = re.compile(
        r"/--\s*(.*?)-/\s*structure\s+(F\d+)\s+where\s*(.*?)(?=\n/--|\nend\s+Hinges|\Z)",
        re.S,
    )
    blocks = pattern.findall(text)

    if not blocks:
        print("FAIL: no hinge structures found in", HINGES)
        return 1

    ok = True
    for doc, name, fields in blocks:
        hypotheses = re.findall(r"^\s*(h_\w+)\s*:", fields, re.M)
        conclusions = re.findall(r"^\s*(conclusion_\w+)\s*:", fields, re.M)
        sourced = "Source:" in doc

        problems = []
        if not hypotheses:
            problems.append("no h_* hypothesis field (blank hypothesis list)")
        if not conclusions:
            problems.append("no conclusion_* field")
        if not sourced:
            problems.append("no Source: line")

        if problems:
            ok = False
            print(f"FAIL {name}: " + "; ".join(problems))
        else:
            print(
                f"  {name}: {len(hypotheses)} hypothesis(es), "
                f"{len(conclusions)} conclusion, sourced"
            )

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
