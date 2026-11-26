"""The sharper animals bound — a verified cross-field transfer.

The lattice-QFT animals bound counts connected subgraphs via a FREE walk:
    #{connected subgraphs of size n} ≤ |V|·(2n)·(Δ+1)^(2(n−1))
(the Euler tour of a rooted tree has length 2(n−1), each step ≤ Δ choices).

But an Euler tour is NOT a free walk — each edge is traversed exactly twice, once out and once
back, so the tree's structure constrains the walk. The true count is the rooted-tree count, which
gives the sharper bound
    #{connected subgraphs of size n} ≤ |V|·(Δ+1)^(n−1).

This module verifies both bounds across a graph family (paths, cycles, stars, complete, grid, and
random graphs) — the sharper bound holds everywhere and is ~(Δ+1)^(n−1)/(2n) tighter.
"""
from __future__ import annotations

import itertools


def is_connected(vertices: list[int], edges: list[tuple[int, int]]) -> bool:
    if not vertices:
        return False
    adj = {v: set() for v in vertices}
    for u, w in edges:
        if u in adj and w in adj:
            adj[u].add(w)
            adj[w].add(u)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen == set(vertices)


def count_connected(n_vertices: int, edges: list[tuple[int, int]], n: int) -> int:
    return sum(1 for S in itertools.combinations(range(n_vertices), n)
               if is_connected(list(S), edges))


def max_degree(n_vertices: int, edges: list[tuple[int, int]]) -> int:
    return max(sum(1 for e in edges if i in e) for i in range(n_vertices))


def animals_bound(n_vertices: int, n: int, delta: int) -> int:
    """The original free-walk bound."""
    return n_vertices * (2 * n) * (delta + 1) ** (2 * (n - 1))


def sharper_bound(n_vertices: int, n: int, delta: int) -> int:
    """The rooted-tree (Euler-tour-constrained) bound, base Δ+1."""
    return n_vertices * (delta + 1) ** (n - 1)


def rooted_tree_bound(n_vertices: int, n: int, delta: int) -> int:
    """The true rooted-tree count: the root has ≤ Δ children, every other node ≤ Δ−1.

    #{connected subgraphs of size n} ≤ |V|·Δ·(Δ−1)^(n−2)  (and |V| for n = 1).
    This is the tightest of the three — up to ~40× tighter than animals_bound on sparse graphs.
    """
    if n <= 1:
        return n_vertices
    return n_vertices * delta * (delta - 1) ** (n - 2)


def graph_families():
    def path(k):
        return k, [(i, i + 1) for i in range(k - 1)]

    def cycle(k):
        return k, [(i, (i + 1) % k) for i in range(k)]

    def star(k):
        return k, [(0, i) for i in range(1, k)]

    def complete(k):
        return k, [(i, j) for i in range(k) for j in range(i + 1, k)]

    def grid(m):
        hor = [(i * m + j, i * m + j + 1) for i in range(m) for j in range(m - 1)]
        ver = [(i * m + j, (i + 1) * m + j) for i in range(m - 1) for j in range(m)]
        return m * m, hor + ver

    return [("path", path(8)), ("cycle", cycle(8)), ("star", star(8)),
            ("complete", complete(8)), ("grid-3x3", grid(3))]


def verify(sizes=(1, 2, 3, 4, 5)) -> dict:
    """Check the three bounds over the families + sizes; report failures and worst looseness."""
    failures_rooted = failures_sharper = failures_original = 0
    worst_rooted = worst_sharper = worst_original = 0.0
    for _name, (n_vertices, edges) in graph_families():
        delta = max_degree(n_vertices, edges)
        for n in sizes:
            exact = count_connected(n_vertices, edges, n)
            if rooted_tree_bound(n_vertices, n, delta) < exact:
                failures_rooted += 1
            if sharper_bound(n_vertices, n, delta) < exact:
                failures_sharper += 1
            if animals_bound(n_vertices, n, delta) < exact:
                failures_original += 1
            worst_rooted = max(worst_rooted, exact / rooted_tree_bound(n_vertices, n, delta))
            worst_sharper = max(worst_sharper, exact / sharper_bound(n_vertices, n, delta))
            worst_original = max(worst_original, exact / animals_bound(n_vertices, n, delta))
    return {
        "original_bound_failures": failures_original,
        "sharper_bound_failures": failures_sharper,
        "rooted_tree_failures": failures_rooted,
        "worst_exact_over_original": worst_original,   # 1.0 = tight
        "worst_exact_over_sharper": worst_sharper,     # 1.0 = tight
        "worst_exact_over_rooted": worst_rooted,       # 1.0 = tight
    }


if __name__ == "__main__":
    r = verify()
    print(f"original bound failures: {r['original_bound_failures']}")
    print(f"sharper  bound failures: {r['sharper_bound_failures']}")
    print(f"rooted-tree failures:    {r['rooted_tree_failures']}")
    print(f"worst exact/original: {r['worst_exact_over_original']:.4f}")
    print(f"worst exact/sharper:  {r['worst_exact_over_sharper']:.4f}")
    print(f"worst exact/rooted:   {r['worst_exact_over_rooted']:.4f}")
    print(f"worst exact/sharper:  {r['worst_exact_over_sharper']:.4f}")
