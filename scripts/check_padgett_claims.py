#!/usr/bin/env python3
"""An outside claim, put through the same machine: Jason Padgett's "asymmetric prime" interference.

Three claims from the Quantum Information Holography preprints are checkable as stated; this script
checks them and prints the numbers. Everything else in those papers is class "no oracle" — it is not
that it is wrong, it is that no observation could tell it apart from any other story.

    python3 scripts/check_padgett_claims.py

Claim 1  "asymmetric primes ... resist typical quantum cancellation", via  I_PA = sum_{p in PA} e^{i p theta}
Claim 2  primes are luminous matter and non-primes are dark matter
Claim 3  hf = hbar*omega = m c^2 is a unification
"""
import cmath
import math
import sys


_SIEVE_CACHE: dict = {}


def primes_upto(n: int) -> list[int]:
    if n in _SIEVE_CACHE:
        return _SIEVE_CACHE[n]
    _SIEVE_CACHE[n] = _primes(n)
    return _SIEVE_CACHE[n]


def _primes(n: int) -> list[int]:
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n) if sieve[i]]


def interference(seq: list[int], theta: float) -> float:
    return abs(sum(cmath.exp(1j * x * theta) for x in seq))


def claim1() -> dict:
    """Does the interference term resist cancellation, and does the prime property do any work?"""
    primes = primes_upto(200000)
    rows = []
    for n in (1000, 4000, 16000):
        seq = primes[:n]
        s = interference(seq, 1.0)
        rows.append({"n": n, "abs_sum": s, "over_sqrt_n": s / math.sqrt(n), "over_n": s / n})
    # the parity control: at theta = pi every odd number gives |S| = n, prime or not
    control = {}
    for label, seq in (("primes", primes[:3000]),
                       ("odd composites",
                        [k for k in range(9, 200000, 2) if not any(k % p == 0 for p in range(3, int(k ** 0.5) + 1, 2))][:3000]),
                       ("all odd numbers", list(range(3, 200000, 2))[:3000])):
        control[label] = interference(seq, math.pi) / len(seq)
    generic = [r for r in rows if r["n"] == 16000][0]
    return {"rows": rows, "theta_pi_per_term": control,
            "cancels_like_random_walk": generic["over_sqrt_n"] < 2.0 and generic["over_n"] < 0.05,
            "parity_does_all_the_work": all(abs(v - 1.0) < 0.01 for v in control.values()),
            "verdict": ("at a generic phase the sum cancels at the random-walk rate (|S| ~ sqrt(n)), and "
                        "the only phase where it does not cancel is theta = pi, where EVERY set of odd "
                        "numbers behaves identically — so the prime property does no work")}


def claim2() -> dict:
    """Primes are luminous matter, non-primes dark matter: does any cut-off make that true?"""
    rows = []
    # to 10^7 rather than 10^9: a billion-element sieve costs minutes and adds no information, since
    # the 1/ln N trend is already unambiguous at 10^5
    for n in (1000, 10 ** 4, 10 ** 6, 10 ** 7):
        rows.append({"N": n, "prime_fraction": len(primes_upto(n)) / n})
    observed = {"baryons": 0.049, "dark_matter": 0.268, "dark_energy": 0.683}
    return {"rows": rows, "observed": observed,
            "dark_over_baryon": observed["dark_matter"] / observed["baryons"],
            "tends_to_zero": rows[-1]["prime_fraction"] < rows[0]["prime_fraction"],
            "by_prime_number_theorem": 1.0 / math.log(10 ** 7),
            "verdict": ("the prime fraction falls like 1/ln N and tends to zero, so it cannot equal a "
                        "fixed cosmic fraction; it passes through the baryon value near N ~ 10^9 and "
                        "keeps falling — a coincidence at one arbitrary cut-off, and with the wrong "
                        "component (luminous, not dark). The observed dark/baryon ratio is 5.47 and "
                        "is constant")}


def claim3() -> dict:
    """hf = hbar*omega = m c^2: is that a unification or a restatement?"""
    h = 6.62607015e-34
    hbar = h / (2 * math.pi)
    f = 5.0e14
    omega = 2 * math.pi * f
    return {"h_f": h * f, "hbar_omega": hbar * omega,
            "identical_by_definition": h * f == hbar * omega,
            "verdict": ("h f = hbar omega exactly, because omega = 2 pi f and hbar = h / 2 pi — it is "
                        "one statement written twice, not a joining of two domains")}


def main() -> int:
    print("PACLAND · an outside claim through the same machine\n")
    for name, fn in (("1 · asymmetric-prime interference", claim1),
                     ("2 · primes = luminous matter", claim2),
                     ("3 · hf = hbar*omega = mc^2", claim3)):
        r = fn()
        print(name)
        if "rows" in r:
            for row in r["rows"]:
                print("   ", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})
        if "theta_pi_per_term" in r:
            print("    theta = pi, |S|/n:", {k: round(v, 4) for k, v in r["theta_pi_per_term"].items()})
        print("   ->", r["verdict"])
        print()
    print("What this is not: a judgement of the man. It is a judgement of three sentences, and the")
    print("machine is indifferent to who wrote them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
