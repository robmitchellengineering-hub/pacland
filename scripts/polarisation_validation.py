"""Validate the vector mode fields — the two checks docs/polarisation.md promised and did not do.

The polarised stream table is PASS-2 across Q, but the FIELD MODEL behind it was never checked. Two properties are
checkable without a reference book:

  1. BOUNDARY CONDITIONS. On a conducting wall the tangential electric field is zero. A wrong factor or a swapped
     index breaks this immediately.
  2. POLARISATION ROTATION. The coupling of a linear element to a fixed field must follow |cos(theta)| as the
     element is rotated. Anything else means the projection is wrong.

    python3 scripts/polarisation_validation.py

FALSIFIER, stated before the run: if any tangential component is non-zero on a wall (beyond floating point), or the
coupling does not follow a cosine, the field model is wrong and every polarised number in the repository is void.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

A, B, D = 3.0, 4.0, 2.5
TOL = 1e-9


def tangential_residual(idx, kind):
    """Sum of |tangential E| over the six walls - should be zero everywhere."""
    m, n, p = idx
    worst = 0.0
    for x in (0.0, A):
        # walls normal to x: tangential are Ey, Ez
        for y in (0.3 * B, 0.7 * B):
            for z in (0.25 * D, 0.6 * D):
                e = E.mode_field(idx, kind, x, y, z, A, B, D)
                worst = max(worst, abs(e[1]), abs(e[2]))
    for y in (0.0, B):
        # walls normal to y: tangential are Ex, Ez
        for x in (0.3 * A, 0.7 * A):
            for z in (0.25 * D, 0.6 * D):
                e = E.mode_field(idx, kind, x, y, z, A, B, D)
                worst = max(worst, abs(e[0]), abs(e[2]))
    for z in (0.0, D):
        # walls normal to z: tangential are Ex, Ey
        for x in (0.3 * A, 0.7 * A):
            for y in (0.3 * B, 0.7 * B):
                e = E.mode_field(idx, kind, x, y, z, A, B, D)
                worst = max(worst, abs(e[0]), abs(e[1]))
    return worst


def coupling_vs_angle(idx, kind, pos, steps=181):
    """|E . u(theta)| for a linearly polarised element rotated in the x-y plane."""
    e = E.mode_field(idx, kind, pos[0], pos[1], pos[2], A, B, D)
    # the rotating element lives in the x-y plane, so the amplitude it can ever see is the IN-PLANE part. Comparing
    # against the full |E| (which includes Ez for TM modes) makes a correct model look like a failure. And the
    # amplitude has to be computed ANALYTICALLY: taking the max over a coarse sample grid under-reads it by up to
    # 0.1%, which is the same size as the tolerance and made the first version of this check fail.
    peak = math.hypot(e[0], e[1])
    if peak == 0:
        return [], 0.0
    out = []
    for i in range(steps):
        th = math.pi * i / (steps - 1)
        u = (math.cos(th), math.sin(th), 0.0)
        out.append((th, abs(sum(u[j] * e[j] for j in range(3)))))
    return out, peak


def main() -> int:
    print("=" * 78)
    print("VECTOR MODE FIELDS — boundary conditions and polarisation rotation")
    print("=" * 78)
    print(f"{'mode':>12} {'wall residual':>16} {'verdict':>10}")
    worst_all = 0.0
    for kind, idx in (("TE", (1, 1, 1)), ("TE", (2, 1, 3)), ("TE", (1, 3, 2)),
                      ("TM", (1, 1, 0)), ("TM", (1, 1, 1)), ("TM", (2, 3, 2))):
        r = tangential_residual(idx, kind)
        worst_all = max(worst_all, r)
        print(f"{kind}{idx!s:>9} {r:>16.2e} {'OK' if r < TOL else 'FAIL':>10}")
    print()
    print(f"{'mode':>10} {'max |cos dev|':>15} {'verdict':>10}")
    worst_cos = 0.0
    for kind, idx, pos in (("TE", (1, 1, 1), (0.37 * A, 0.41 * B, 0.29 * D)),
                           ("TM", (2, 1, 1), (0.61 * A, 0.23 * B, 0.44 * D))):
        rows, peak = coupling_vs_angle(idx, kind, pos)
        if not rows:
            continue
        # after removing the sign the coupling must equal peak * |cos(theta - phi)|, where phi is the field's own
        # in-plane angle. Searching a t0 grid instead of using phi puts a floor under the residual: a 0.25-degree
        # grid can only ever be within 2.2e-3, which is twice the tolerance and made a correct model fail.
        e = E.mode_field(idx, kind, pos[0], pos[1], pos[2], A, B, D)
        phi = math.atan2(e[1], e[0])
        best = max(abs(v - peak * abs(math.cos(th - phi))) for th, v in rows)
        worst_cos = max(worst_cos, best / peak)
        print(f"{kind}{idx!s:>7} {best/peak:>15.2e} {'OK' if best / peak < 1e-3 else 'FAIL':>10}")
    print()
    if worst_all >= TOL:
        print("VERDICT: FIELD MODEL WRONG — a tangential component survives on a wall.")
        print("         Every polarised number in the repository is void.")
        return 1
    if worst_cos >= 1e-3:
        print("VERDICT: FIELD MODEL WRONG — the coupling does not follow a cosine.")
        return 1
    print("VERDICT: both checks pass.")
    print("  - every tangential component vanishes on every wall, to floating point, for TE and TM modes;")
    print("  - the coupling of a linear element follows |cos(theta)| to better than 1e-3 of peak.")
    print()
    print("This does NOT validate the field MAGNITUDES (no normalisation is applied, and none is needed for a")
    print("stream count) - it validates the structure the projection depends on.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
