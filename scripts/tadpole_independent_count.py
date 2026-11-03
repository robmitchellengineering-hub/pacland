#!/usr/bin/env python3
"""An independent count of the tadpole distribution — pure Python, no numpy, no polynomial.

    python3 scripts/tadpole_independent_count.py [--b3 6]

**Why this exists.** The closed form `count(N) = [x^N] P(x)^(b3/2)` is checked against full enumeration
inside `tadpole_distribution.verify()`. But that check, the closed form, and the enumeration all live in
the same numpy pipeline and share the block algebra — so agreement between them is weaker evidence than it
looks. This script computes the same distribution by a deliberately different route:

* nested loops over every `(F, H)` pair, in the order the integers come,
* `N = sum_i (f_i h_{i+n} - f_{i+n} h_i)` applied literally, one pair at a time,
* primitivity by `math.gcd` over the whole pair,
* no numpy, no polynomial, no caching, no convolution.

If this and the closed form agree at a rung, the agreement is a fact about the distribution rather than a
property of one implementation. It is the **PASS-2 path** for the `tadpole-count-b3-8` claim: the closed
form has one line of evidence from the enumeration; this is the second, independent line.

Cost: b3 = 6 is 531,441 pairs (seconds in Python); b3 = 8 is 43,046,721 (minutes — run it on a node, not
in CI).
"""
import argparse
import math
import sys
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def tadpole(f: tuple, h: tuple, n: int) -> int:
    """`N = sum_i (f_i h_{i+n} - f_{i+n} h_i)` — the definition, straight."""
    total = 0
    for i in range(n):
        total += f[i] * h[i + n] - f[i + n] * h[i]
    return total


def primitive(f: tuple, h: tuple) -> bool:
    g = 0
    for v in f:
        g = math.gcd(g, v)
    for v in h:
        g = math.gcd(g, v)
    return g == 1


def distribution(b3: int) -> tuple[dict[int, int], int]:
    """(counts per tadpole class, number of primitive orbits) for the window |component| <= 1."""
    if b3 % 2:
        raise ValueError("b3 must be even")
    n = b3 // 2
    span = (-1, 0, 1)
    counts: Counter = Counter()
    orbits = 0
    for f in product(span, repeat=b3):
        for h in product(span, repeat=b3):
            if not primitive(f, h):
                continue
            orbits += 1
            counts[tadpole(f, h, n)] += 1
    return dict(counts), orbits


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Independent tadpole distribution (no numpy, no polynomial).")
    ap.add_argument("--b3", type=int, default=6, help="half the flux dimension; must be even (default 6)")
    ap.add_argument("--no-compare", action="store_true", help="skip the closed-form comparison")
    args = ap.parse_args(argv[1:])
    b3 = args.b3

    print(f"Independent count at b3 = {b3} (nested loops, no numpy, no polynomial)")
    counts, orbits = distribution(b3)
    total = sum(counts.values())
    print(f"  primitive orbits : {orbits}")
    print(f"  classes          : {len(counts)}")
    print(f"  tadpole range    : [{min(counts)}, {max(counts)}]")
    print(f"  sum of classes   : {total}")
    print(f"  all pairs - 1    : {3 ** (2 * b3) - 1}")

    if args.no_compare:
        return 0

    from pacland.exactness import tadpole_distribution as T

    closed = T.counts(b3)
    same = dict(closed) == counts
    print()
    print(f"  closed form      : {len(closed)} classes, {sum(closed.values())} orbits")
    print(f"  agreement        : {'YES — exact match on every class' if same else 'NO — the closed form is wrong here'}")
    if not same:
        differing = sorted(set(closed) | set(counts))
        for key in differing:
            if closed.get(key) != counts.get(key):
                print(f"    N={key:>4}: closed {closed.get(key)}, independent {counts.get(key)}")
        return 1
    print()
    print("This is an independent line of evidence: the two implementations share no code path.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
