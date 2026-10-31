"""A bound for two-state ambient-thermal-noise communication.

The Stanford result (PNAS, Oct 2026) switches a load between ABSORBING and REFLECTING ambient thermal noise
and reads the difference at a receiver: ~1000x less energy than conventional RF, and their channel model
bought 100x rate. This asks the question a demonstration does not: **how much of that is room left on the
table, and on which side of the link is the energy actually spent?**

Model
-----
A resistor at temperature T presents available noise power `P = k_B T B` in bandwidth B (Nyquist). The
switch changes the power the receiver sees by a contrast `eta`:

    P_0 = k_B T B          (reflecting: the receiver sees the ambient field)
    P_1 = k_B T B (1+eta)  (absorbing: the load takes power, changing the field the receiver samples)

A radiometer integrates for `tau`, giving `m = B*tau` independent samples. For thermal (Gaussian) noise the
power estimate is exponentially distributed, so its relative standard deviation is `1/sqrt(m)`.

Per-sample Fisher information for the state, from the difference of means over the standard deviation:

    I = (P_1 - P_0)^2 / var  =  (eta * P)^2 / (P^2 / m)  =  eta^2 * m

For a binary decision the error probability is `eps = Q(sqrt(I/2))`, and the achievable spectral efficiency
is `C/B = 1 - H2(eps)` bits per sample-pair (Shannon, binary input, one observation per sample).

FALSIFIER: if `eta^2 * m` must exceed ~1 for any usable rate, then the 1000x energy saving is bought with
integration TIME, not with information — and the claim must state its rate to mean anything.
"""
import math


def q(x: float) -> float:
    """Upper tail of the standard normal."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def q_inv(p: float) -> float:
    """Inverse of the upper tail, by bisection (no scipy on the node needed)."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if q(mid) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def h2(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def error_rate(eta: float, m: float) -> float:
    return q(math.sqrt(eta * eta * m / 2.0))


def spectral_efficiency(eta: float, m: float) -> float:
    return 1.0 - h2(error_rate(eta, m))


def samples_for(eta: float, target_ber: float) -> float:
    """How many independent noise samples are needed to reach a target bit error rate."""
    return 2.0 * q_inv(target_ber) ** 2 / (eta * eta)


def main() -> int:
    kB = 1.380649e-23
    T = 300.0          # kelvin
    B = 1.0e6          # 1 MHz
    P = kB * T * B
    print("=" * 96)
    print("A bound for two-state ambient-thermal-noise communication")
    print(f"T = {T:.0f} K, B = {B/1e6:.0f} MHz -> available noise power P = k_B T B = {P:.3e} W")
    print("=" * 96)

    print("\n1. samples needed for a target BER, as a function of contrast eta")
    print(f"{'eta':>6} {'BER 1e-3':>10} {'BER 1e-6':>10} {'tau @1MHz for 1e-3':>22} {'C/B @1e-3':>11}")
    for eta in (1e-3, 1e-2, 0.1, 0.5, 1.0):
        m3 = samples_for(eta, 1e-3)
        m6 = samples_for(eta, 1e-6)
        tau = m3 / B
        c = spectral_efficiency(eta, m3) if m3 < 1e12 else 0.0
        print(f"{eta:>6.3g} {m3:>10.3e} {m6:>10.3e} {tau:>22.3e}s {c:>11.3f}")

    print("\n2. what the 1000x claim costs in TIME (eta = 0.1, the contrast a matched load can plausibly give)")
    eta = 0.1
    m = samples_for(eta, 1e-3)
    print(f"   {m:.0f} samples at B = 100 Hz  -> tau = {m/100:.1f} s")
    print(f"   {m:.0f} samples at B = 1 kHz   -> tau = {m/1e3:.2f} s")
    print(f"   {m:.0f} samples at B = 1 MHz   -> tau = {m/1e6:.3f} s")

    print("\n3. where the energy is spent")
    E_recv = P * m / B * 0  # placeholder for clarity: receiver integration draws its own power
    print(f"   transmitter: switching only, so E_tx per bit can be ~0 (that is the source of the claim)")
    print(f"   receiver:    integration of m = {m:.0f} samples at ~P per sample is the real cost")
    print(f"   -> '1000x less energy' is a claim about the TRANSMITTER unless the receiver's integration")
    print(f"      energy is counted, which the reported figure must state to be comparable")

    print("\n4. the falsifier")
    for eta in (1e-3, 1e-2, 0.1):
        m = samples_for(eta, 1e-3)
        print(f"   eta={eta:.0e}: eta^2 * m = {eta*eta*m:.1f} "
              f"({'needs a lot of time' if eta*eta*m > 100 else 'cheap'})")
    print("\n   eta^2*m ~ 2 ln(1/BER): the product is fixed, so a small contrast is bought with integration,")
    print("   never with cleverness. Any rate claim is a claim about that product.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
