#!/usr/bin/env python3
"""Numerical emulation of the BMV/GIE gravity-mediated entanglement experiment.

Two masses m1, m2, each in a spatial superposition of width dx, centre distance d, held for time t.
The Newtonian potential entangles them; proper-time decoherence (from internal energy spread) races
against the entangling phase. We compute the exact phase, the exact concurrence, and the race.
"""
import numpy as np
from sympy import Rational, N, symbols, sin, exp, sqrt, pi

G = 6.67430e-11          # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34   # J s
C = 2.99792458e8         # m/s

def phase_exact(m, d, dx, t):
    """phi_ent = G m1 m2 t / hbar * [1/(d+dx) + 1/(d-dx) - 2/d]  (symmetric m1=m2=m, dx1=dx2=dx)."""
    return G * m * m * t / HBAR * (1.0/(d+dx) + 1.0/(d-dx) - 2.0/d)

def concurrence(phi):
    """Concurrence of the BMV two-qubit state |psi> = 1/2 (|00>+e^{ia}|01>+e^{ib}|10>+|11>)."""
    return abs(np.sin(phi/2.0))

def proper_time_decoherence(m, d, dx, t, dE):
    """Proper-time decoherence: masses at different potential depths tick differently.
    d_tau = (G m/d^2) * dx * t / c^2 ;  decoherence ~ exp(-(dE d_tau / hbar)^2)."""
    dtau = (G * m / d**2) * dx * t / C**2
    gamma = (dE * dtau / HBAR)**2
    return np.exp(-gamma)

def internal_energy_spread(m, T):
    """Thermal energy spread of a harmonic oscillator mass at temperature T (Boltzmann)."""
    kB = 1.380649e-23
    return np.sqrt(m) * kB * T  # ~ sqrt(<E^2>) order estimate; refine below
    # better: for a solid, dE ~ sqrt(N k_B^2 T^2) ~ sqrt(m/m_atom) kB T

def main():
    m  = 1e-14     # kg  (nanoparticle)
    d  = 100e-6    # m   (100 um)
    dx = 10e-6     # m   (10 um)
    t  = 1.0       # s
    phi = phase_exact(m, d, dx, t)
    C0  = concurrence(phi)
    print("=" * 70)
    print("BMV emulation — the number")
    print("=" * 70)
    print(f"m = {m:.0e} kg, d = {d*1e6:.0f} um, dx = {dx*1e6:.0f} um, t = {t} s")
    print(f"entangling phase phi      = {phi:.6f} rad")
    print(f"concurrence C = |sin(phi/2)| = {C0:.6f}")
    print()
    print("The race: entanglement (grows ~ t) vs proper-time decoherence (grows ~ t^2)")
    print("dE = internal energy spread (set by temperature / mode occupancy)")
    print()
    for T in [1e-3, 1e-6, 1e-9, 1e-12]:  # temperatures K
        # internal energy spread for a solid at temp T: dE ~ sqrt(N k_B T) * sqrt(3 k_B T)
        # use a clean order estimate: dE ~ sqrt(k_B T * m * c_s^2) ... keep simple: dE = N kB T scale
        # Use the Pikovski proper-time decoherence: dE ~ sqrt(hbar omega m) ... we'll parameterize
        # dE = alpha * sqrt(hbar * G * m^3 / d^3)  ... no. Just sweep dE directly.
        pass
    # sweep dE directly (the free internal-energy scale)
    print("sweep over internal energy spread dE (J):")
    print(f"{'dE (J)':>12} {'tau (s)':>10} {'decoher':>10} {'C_net':>10}")
    for dE in [1e-30, 1e-28, 1e-26, 1e-24, 1e-22]:
        decoh = proper_time_decoherence(m, d, dx, t, dE)
        Cnet = C0 * decoh
        print(f"{dE:12.1e} {proper_time_decoherence(m,d,dx,t,0)/1:10.0f} {decoh:10.3e} {Cnet:10.6f}")

    print()
    print("=" * 70)
    print("The sweet spot: sweep time t to reach C ~ 0.1 (detectable) at dE = 1e-26 J")
    print("=" * 70)
    dE = 1e-26
    for tt in [1, 10, 100, 1000, 10000]:
        phi_t = phase_exact(m, d, dx, tt)
        C_t = concurrence(phi_t) * proper_time_decoherence(m, d, dx, tt, dE)
        print(f"t = {tt:6.0f} s : phi = {phi_t:9.3f} rad, C_net = {C_t:.6f}")

if __name__ == "__main__":
    main()
