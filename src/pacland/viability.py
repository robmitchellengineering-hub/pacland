"""The viability polytope — the constraint-first answer, made an object.

Constraint-first says the answer to "which vacuum?" is *not* a point but the
*feasible region*: the intersection of verified constraints, each a half-space in
observable space. That intersection is a convex polytope. This module computes it.

The reframe this enables (the outside-the-box move):

    The landscape is not big; the constraint system is small.

10^500 is the cardinality of a *set*. But the viable class is described by k
inequalities — k numbers — regardless of how many points the landscape has. If k
independent constraints each eliminate fraction >= p, the survivor fraction is
(1-p)^k, independent of the set's size. So "search the landscape" is the wrong
problem; "solve the polytope" is the right one, and it is polynomial in k.

Everything here is 2D (the (log g_s, log W0) plane) so the polytope is a convex
polygon, computable in pure stdlib by Sutherland--Hodgman clipping. The
``elimination_compression`` function carries the general statement.
"""
from __future__ import annotations

from math import log


def clip_polygon(poly, a: float, b: float, c: float, eps: float = 1e-12):
    """Clip ``poly`` (list of (x,y), CCW or CW) to the half-plane ``a x + b y <= c``.

    Sutherland--Hodgman: keep vertices inside, emit the crossing point where an
    edge leaves/enters. Returns the clipped vertex list (possibly empty).
    """
    poly = list(poly)
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        inside_p = a * p[0] + b * p[1] <= c + eps
        inside_q = a * q[0] + b * q[1] <= c + eps
        if inside_p:
            out.append(p)
        if inside_p != inside_q:
            denom = a * (q[0] - p[0]) + b * (q[1] - p[1])
            if abs(denom) < eps:
                continue
            t = (c - a * p[0] - b * p[1]) / denom
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def polygon_area(pts) -> float:
    """Shoelace area (unsigned) of a vertex list."""
    pts = list(pts)
    if len(pts) < 3:
        return 0.0
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def viable_polytope(half_planes, box) -> dict:
    """Intersect a bounding ``box`` with ``half_planes`` -> the viable polygon.

    ``box`` = (xmin, xmax, ymin, ymax). ``half_planes`` = list of (a, b, c, name)
    meaning ``a x + b y <= c``. Returns vertices (counter-clockwise, normalized),
    the feasible area, the fraction of the box, and which constraints actually
    clipped (were *active*, i.e. reduced the area).
    """
    xmin, xmax, ymin, ymax = box
    poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    box_area = (xmax - xmin) * (ymax - ymin)
    active = []
    area = polygon_area(poly)
    for a, b, c, name in half_planes:
        clipped = clip_polygon(poly, a, b, c)
        new_area = polygon_area(clipped)
        if new_area < area - 1e-12:
            active.append(name)
        poly = clipped
        area = new_area
    return {
        "vertices": poly,
        "area": area,
        "box_area": box_area,
        "area_fraction": (area / box_area) if box_area > 0 else 0.0,
        "active_constraints": active,
        "n_constraints": len(half_planes),
    }


def elimination_compression(fractions) -> dict:
    """The exponential shrink: survivor fraction after independent eliminations.

    ``fractions`` = per-constraint elimination fractions p_i. Returns the survivor
    fraction ``prod(1 - p_i)``, the number of constraints, and the effective
    "constraint count" at 90%-each that would give the same survivor fraction
    (a way to read a chain of weaker constraints as a count of strong ones).
    """
    fractions = list(fractions)
    survivor = 1.0
    for p in fractions:
        survivor *= 1.0 - p
    # survivor = (1 - 0.9)^k  ->  k = ln(survivor) / ln(0.1)
    k90 = log(survivor) / log(0.1) if survivor > 0 else float("inf")
    return {
        "survivor": survivor,
        "n_constraints": len(fractions),
        "equivalent_90pct_constraints": k90,
    }
