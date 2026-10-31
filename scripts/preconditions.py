"""Guards for the instrument, not the result.

Three failures on 2026-10-29 share one shape: the measurement was fine and the *apparatus assumption* was wrong.

  1 `maximum_degree = 0` silently forced mirror instanton corrections OFF (jaxvacua/periods.py:205), so a
    "degree 0 baseline" was not the model at all.
  2 The sampler returns BOTH `|DW|` and `residual`; at h12 = 5 they reported 1.7e38 and 3.8e-37 at the same
    point. One of the two fields was not what it claimed to be.
  3 A ladder ran at ONE moduli point per h12; the answer moved by 88% when five were used.

So: assert the instrument's configuration before comparing against it, and assert that fields which should
agree DO agree, before believing either.
"""
from __future__ import annotations


class PreconditionError(AssertionError):
    """The apparatus was not in the state the measurement assumes."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreconditionError(message)


def require_corrections_on(model, degree: int) -> None:
    """`maximum_degree == 0` disables mirror worldsheet instanton corrections, silently."""
    if not hasattr(model, "include_mirror_wsi"):
        return
    on = bool(model.include_mirror_wsi)
    expect = degree > 0
    require(on == expect,
            f"corrections are {'ON' if on else 'OFF'} but degree={degree} implies "
            f"{'ON' if expect else 'OFF'} — the run is not measuring what it says")


def require_agree(a: float, b: float, names: tuple[str, str], orders: float = 3.0) -> float:
    """Two fields describing the same quantity must not disagree by orders of magnitude."""
    import math
    if a == 0 and b == 0:
        return 0.0
    la = math.log10(abs(a)) if a else float("-inf")
    lb = math.log10(abs(b)) if b else float("-inf")
    gap = abs(la - lb)
    require(gap <= orders,
            f"`{names[0]}` and `{names[1]}` disagree by {gap:.0f} orders of magnitude "
            f"({a:.3e} vs {b:.3e}) — neither can be read as the F-term residual")
    return gap


def require_multi_point(points: int, minimum: int = 3) -> None:
    """A statistic from one or two samples is a draw, and has already been wrong here."""
    require(points >= minimum,
            f"{points} moduli point(s): a ladder needs at least {minimum}, or the answer is one draw")
