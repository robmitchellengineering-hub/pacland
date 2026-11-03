"""The vacuum-energy ratio, computed from published constants rather than quoted.

C6 in the SEXTANT lattice asks whether a candidate accounts for the size of the cosmological
constant. Written as ``Lambda / M_Pl^4 ~ 1e-122`` it was **dimensionally wrong** — the cosmological
constant has mass dimension 2, so ``Lambda / M_Pl^2`` is the dimensionless statement, and
``rho_Lambda / M_Pl^4`` is the other one (energy density against the Planck density). Both numbers
are about 1e-122, which is exactly how the error survived: the number looked right.

This module computes both, from the Planck 2018 parameters read from the paper's own abstract
(arXiv:1807.06209, A&A 641, A6), so the bound in the lattice is arithmetic on published constants —
the same construction the energy claims use for the lithium ceiling.

    rho_crit   = 3 H_0^2 M_Pl^2 / (8 pi)      (with G = 1/M_Pl^2)
    rho_Lambda = (1 - Omega_m) rho_crit
    Lambda     = 8 pi G rho_Lambda

Pure stdlib. Every constant below names where it came from.
"""
from __future__ import annotations

import math

# --- published: Planck 2018 results VI, abstract (arXiv:1807.06209, A&A 641, A6) --------------
H0_KM_S_MPC = 67.4          # km/s/Mpc, +/- 0.5
OMEGA_M = 0.315             # +/- 0.007; flat LCDM => Omega_Lambda = 1 - Omega_m
PLANCK_CITE = "arXiv:1807.06209, A&A 641:A6 (2020) - abstract: H_0 = 67.4 +/- 0.5, Omega_m = 0.315 +/- 0.007"

# --- physical constants (SI / natural units) ---------------------------------------------------
MPC_M = 3.0856775814913673e22   # metres per megaparsec
KM = 1000.0                     # metres per kilometre
HBAR_GEV_S = 6.582119569e-25    # GeV seconds
M_PL_GEV = 1.220910e19          # unreduced Planck mass; G = 1/M_Pl^2 in these units


def h0_gev() -> float:
    """The Hubble constant in GeV."""
    return (H0_KM_S_MPC * KM / MPC_M) * HBAR_GEV_S


def rho_crit_gev4() -> float:
    """Critical density in GeV^4: rho = 3 H^2 M_Pl^2 / (8 pi)."""
    return 3.0 * h0_gev() ** 2 * M_PL_GEV ** 2 / (8.0 * math.pi)


def rho_lambda_gev4() -> float:
    return (1.0 - OMEGA_M) * rho_crit_gev4()


def rho_lambda_over_planck4() -> float:
    """Dimensionless: the vacuum energy density in Planck-density units. ~1.1e-123."""
    return rho_lambda_gev4() / M_PL_GEV ** 4


def lambda_over_planck2() -> float:
    """Dimensionless: the cosmological constant itself in Planck-mass-squared units. ~2.9e-122.

    Lambda = 8 pi G rho_Lambda, and the factor 8 pi is why this is not the same number as above.
    """
    return 8.0 * math.pi * rho_lambda_gev4() / M_PL_GEV ** 4


def as_bound() -> str:
    """The one-line bound the lattice quotes, with both dimensionless forms."""
    return (f"rho_Lambda/M_Pl^4 = {rho_lambda_over_planck4():.2e} and "
            f"Lambda/M_Pl^2 = {lambda_over_planck2():.2e}")


def main() -> int:
    print("Planck 2018 constants:")
    print(f"  H_0    = {H0_KM_S_MPC} km/s/Mpc -> {h0_gev():.4e} GeV")
    print(f"  Omega_m = {OMEGA_M}, so Omega_Lambda = {1 - OMEGA_M:.3f}")
    print(f"  rho_crit   = {rho_crit_gev4():.4e} GeV^4")
    print(f"  rho_Lambda = {rho_lambda_gev4():.4e} GeV^4")
    print()
    print(f"  rho_Lambda / M_Pl^4 = {rho_lambda_over_planck4():.3e}")
    print(f"  Lambda      / M_Pl^2 = {lambda_over_planck2():.3e}")
    print()
    print("The lattice's first text said 'Lambda/M_Pl^4 ~ 1e-122'. That ratio does not exist:")
    print("Lambda has mass^2 and M_Pl^4 has mass^4. The number was right by coincidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
