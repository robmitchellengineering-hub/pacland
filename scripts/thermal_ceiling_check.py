"""Check the thermal bound against a simulation — the second path that makes it PASS-2 or not.

docs/thermal-noise-bound.md derives `eta^2 m = 2 [Q^-1(eps)]^2`: the samples per bit a two-state ambient link needs
at contrast `eta` for a target BER. A derivation is one path; a Monte Carlo of the same receiver is a second.

    python3 scripts/thermal_ceiling_check.py

The receiver simulated here is the one the bound describes: integrate `m` samples, decide which state, count errors.

FALSIFIER, stated before the run: if the simulated BER at the derived `m` is worse than the target by more than the
statistical error, the bound is unreachable and the derivation is wrong. If it is much BETTER, the bound is loose
and is not a bound.
"""
import math
import random
import sys


def q_inv(p: float) -> float:
    """Inverse standard normal CDF by bisection - no scipy, and checkable."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1.0 + math.erf(mid / math.sqrt(2.0))) < p:
            lo = mid
        else:
            hi = mid
    return hi


def samples_per_bit(contrast: float, target_ber: float) -> float:
    """Two equally likely states, equal variance, integrate m samples, decide at the midpoint.

    With separation `eta*m` and noise sd `sqrt(m)`, the deflection is `d = eta*sqrt(m)` and the error is `Q(d/2)`,
    so `m = 4 [Q^-1(eps)]^2 / eta^2`. The published derivation used a constant of 2, which came from writing the
    error as `Q(sqrt(I/2))` instead of `Q(sqrt(I)/2)` - a factor of two in m, and 2x too optimistic. Found by this
    simulation, which is the point of having a second path.
    """
    return 4.0 * q_inv(target_ber) ** 2 / (contrast ** 2)


def simulate(contrast: float, m: int, trials: int, rng: random.Random) -> float:
    """Two equally likely states, unit-variance noise, contrast between their means; integrate m samples."""
    sd = math.sqrt(m)
    mu = contrast * m
    errors = 0
    for _ in range(trials):
        bit = rng.random() < 0.5
        mean = mu if bit else 0.0
        obs = rng.gauss(mean, sd)
        decided = obs > mu / 2.0
        if decided != bit:
            errors += 1
    return errors / trials


def main() -> int:
    rng = random.Random(4)
    print(f"{'contrast':>9} {'target':>8} {'m (bound)':>10} {'simulated BER':>14} {'trials':>8}")
    worst_ratio = 0.0
    for contrast, target in ((0.05, 1e-2), (0.1, 1e-3), (0.1, 1e-2), (0.2, 1e-4)):
        m = int(math.ceil(samples_per_bit(contrast, target)))
        trials = 400000 if target >= 1e-3 else 120000
        ber = simulate(contrast, m, trials, rng)
        ratio = ber / target
        worst_ratio = max(worst_ratio, ratio)
        print(f"{contrast:>9.2f} {target:>8.0e} {m:>10} {ber:>14.2e} {trials:>8}")
    print()
    if worst_ratio > 2.0:
        print(f"VERDICT: FALSIFIED — the simulated BER is {worst_ratio:.1f}x the target at the derived m.")
        print("         The bound is unreachable, so the derivation is wrong.")
    elif worst_ratio < 0.5:
        print(f"VERDICT: LOOSE — the simulation heavily BEATS the bound ({worst_ratio:.2f}x the target),")
        print("         so it is not a bound. It would be a conservative rule of thumb at best.")
    else:
        print(f"VERDICT: PASS-2 — the simulation lands within {worst_ratio:.2f}x of the target at the derived m,")
        print("         so the bound is reachable and tight, by two independent paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
