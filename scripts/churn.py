#!/usr/bin/env python3
"""churn — the autonomous verification-driven search loop.

Not generative discovery: it searches a bounded, falsifiable parameter space and lets the falsifier
kill the wrong answers. This is the honest version of "let it churn":

  1. propose  — candidate bounds for #{connected subgraphs of size n} ≤ |V|·c·(Δ+1)^(e·(n−1)),
                the parameters (c, e) drawn from a grid (and, if Ollama is reachable, an LLM guess);
  2. falsify  — search a family of graphs for one where the bound fails;
  3. record   — keep the survivors, drop the refuted, track the tightest valid bound.

Run it on the ROG (it has Ollama + the checkout); it prints a running tally and exits cleanly.
"""
from __future__ import annotations

import itertools
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.cross_field.connected_subgraphs import (  # noqa: E402
    count_connected, max_degree,
)


def _graphs():
    """The falsifier's test graphs: paths, cycles, stars, complete, a grid, and a few random ones."""
    def path(k):
        return k, [(i, i + 1) for i in range(k - 1)]

    def cycle(k):
        return k, [(i, (i + 1) % k) for i in range(k)]

    def star(k):
        return k, [(0, i) for i in range(1, k)]

    def complete(k):
        return k, [(i, j) for i in range(k) for j in range(i + 1, k)]

    def grid(m):
        h = [(i * m + j, i * m + j + 1) for i in range(m) for j in range(m - 1)]
        v = [(i * m + j, (i + 1) * m + j) for i in range(m - 1) for j in range(m)]
        return m * m, h + v

    return [path(14), cycle(8), star(8), complete(8), grid(3), grid(4)]


def bound(vertices, n, delta, c, e):
    return vertices * c * (delta + 1) ** (e * (n - 1))


def falsify(c, e, sizes=(2, 3, 4, 5, 6, 7, 8)) -> str | None:
    """Return the first counterexample (family, n, exact, bound) that breaks the bound, or None."""
    names = ["path", "cycle", "star", "complete", "grid-3x3", "grid-4x4"]
    for name, (v, edges) in zip(names, _graphs()):
        delta = max_degree(v, edges)
        for n in sizes:
            exact = count_connected(v, edges, n)
            if bound(v, n, delta, c, e) < exact:
                return f"{name} n={n}: exact={exact} > bound={bound(v, n, delta, c, e):.1f}"
    return None


def _llm_guess() -> list[tuple[float, float]]:
    """Ask the local Ollama for (c, e) guesses; empty if it isn't running."""
    endpoint = os.environ.get("SEXTANT_LLM_ENDPOINT", "http://localhost:11434/v1")
    model = os.environ.get("SEXTANT_LLM_MODEL", "qwen2.5-discovery")
    try:
        req = urllib.request.Request(
            f"{endpoint}/chat/completions",
            data=(f'{{"model":"{model}","messages":[{{"role":"user","content":'
                  f'"Propose 3 tight (constant, exponent) pairs for the bound '
                  f'#connected subgraphs of size n <= |V|·constant·(Δ+1)^(exponent·(n−1)). '
                  f'Reply with JSON only: [["c","e"], ...]. The known valid pair is 1,1; the known '
                  f'loose pair is 2n,2."}}],"temperature":0.7}}').encode(),
            headers={"Content-Type": "application/json"},
        )
        body = urllib.request.urlopen(req, timeout=30).read().decode()
        import json
        content = json.loads(body)["choices"][0]["message"]["content"]
        pairs = json.loads(content[content.index("["):content.rindex("]") + 1])
        return [(float(c), float(e)) for c, e in pairs]
    except Exception:
        return []


def main(iterations: int = 8) -> int:
    grid = [(c, e) for c in (1.0, 1.5, 2.0) for e in (0.5, 1.0, 1.5, 2.0)]
    candidates = grid + _llm_guess()
    survivors = []
    for c, e in candidates:
        refuted = falsify(c, e)
        if refuted is None:
            survivors.append((c, e))
            print(f"KEEP  c={c}, e={e}  (survived every test graph)")
        else:
            print(f"DROP  c={c}, e={e}  (refuted by {refuted})")
    # the tightest survivor: smallest bound on the largest tested graph
    print(f"\n{len(survivors)}/{len(candidates)} candidates survived.")
    if survivors:
        # smallest exponent is the tightest asymptotically; smallest constant breaks ties
        best = min(survivors, key=lambda ce: (ce[1], ce[0]))
        print(f"tightest survivor: c={best[0]}, e={best[1]}  "
              f"(bound |V|·{best[0]}·(Δ+1)^({best[1]}·(n−1)))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
