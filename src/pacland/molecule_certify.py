"""The molecule certificate — a real molecule's ground energy, from integrals to a certified number.

This is the H2 milestone of wedge 2 (certified chemistry). The full pipeline, end to end:

    PySCF (integrals)  ->  OpenFermion (Jordan-Wigner)  ->  4-qubit Hamiltonian  ->  solve  ->  certify against FCI.

For H2 (4 qubits) the honest solver is exact diagonalization: 4 qubits is 16 states, so the answer
is exact to machine precision, and it must match PySCF's FCI reference. The DMRG sufficiency
certificate (`chemistry_certify.py`) is the solver that takes over for larger molecules; this module
wires the *molecule* half and proves the two ends agree.

Dependencies (optional, imported lazily): `pyscf`, `openfermion`, `openfermionpyscf`.

Usage:
    python -m pacland.molecule_certify certify --out h2.json
    python -m pacland.molecule_certify verify  h2.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

FORMAT = "pacland/molecule-certificate@1"

_I = np.eye(2)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULI = {"I": _I, "X": _X, "Y": _Y, "Z": _Z}


def h2_data():
    """Build H2 (STO-3G, R=0.7414 A) and return (qubit_hamiltonian_terms, fci_energy, n_qubits)."""
    from openfermion.chem import MolecularData
    from openfermionpyscf import run_pyscf
    from openfermion import jordan_wigner

    molecule = MolecularData([("H", (0, 0, 0)), ("H", (0, 0, 0.7414))], "sto-3g", 1)
    molecule = run_pyscf(molecule, run_mp2=False, run_cisd=False, run_ccsd=False, run_fci=True)
    qubit_ham = jordan_wigner(molecule.get_molecular_hamiltonian())
    return qubit_ham.terms, molecule.fci_energy, molecule.n_qubits


def pauli_matrix(terms, n: int) -> np.ndarray:
    """Build the 2^n x 2^n matrix of a QubitOperator term dict ({(q,'P'): coeff})."""
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for ops, coeff in terms.items():
        locals_ = [_PAULI["I"]] * n
        for q, p in ops:
            locals_[q] = _PAULI[p]
        M = locals_[0]
        for i in range(1, n):
            M = np.kron(M, locals_[i])
        H += coeff * M
    return H


def ground_energy(terms, n: int) -> float:
    return float(np.linalg.eigvalsh(pauli_matrix(terms, n))[0])


def certify(out: str) -> dict:
    terms, fci, n = h2_data()
    E = ground_energy(terms, n)
    cert = {
        "format": FORMAT,
        "molecule": {"name": "H2", "geometry": [[0, 0, 0], [0, 0, 0.7414]],
                     "basis": "sto-3g", "n_qubits": int(n), "n_electrons": 2},
        "hamiltonian": {"encoding": "jordan-wigner", "n_terms": len(terms)},
        "result": {"energy": E, "reference": "FCI (PySCF)", "reference_energy": fci,
                   "delta": abs(E - fci)},
        "falsifier": f"python -m pacland.molecule_certify verify {out}",
    }
    Path(out).write_text(json.dumps(cert, indent=2) + "\n")
    return cert


def verify(cert_path: str, tol: float = 1e-8) -> dict:
    cert = json.loads(Path(cert_path).read_text())
    if cert.get("format") != FORMAT:
        return {"ok": False, "checks": [(False, f"not a {FORMAT} certificate")], "failures": ["bad format"]}
    terms, fci, n = h2_data()
    E = ground_energy(terms, n)
    checks: list[tuple[bool, str]] = []
    failures: list[str] = []

    def check(ok: bool, msg: str) -> None:
        checks.append((ok, msg))
        if not ok:
            failures.append(msg)

    check(abs(E - cert["result"]["energy"]) <= tol,
          f"reproducibility: re-run energy {E:.12f} matches recorded {cert['result']['energy']:.12f} "
          f"(tol {tol:g})")
    check(abs(E - fci) <= tol,
          f"reference: |E - FCI| = {abs(E - fci):.2e} <= tol {tol:g}")
    return {"ok": not failures, "checks": checks, "failures": failures}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="The molecule certificate (H2 -> certified ground energy).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("certify", help="build H2, solve, write a certificate")
    c.add_argument("--out", default="h2.json")
    v = sub.add_parser("verify", help="rebuild and re-solve, check the certificate")
    v.add_argument("cert")
    v.add_argument("--tol", type=float, default=1e-8)
    args = ap.parse_args(argv)
    if args.cmd == "certify":
        cert = certify(args.out)
        print(f"certified {cert['molecule']['name']} ({cert['molecule']['n_qubits']} qubits, "
              f"{cert['hamiltonian']['n_terms']} JW terms) -> {args.out}")
        print(f"  E = {cert['result']['energy']:.12f}  (FCI reference {cert['result']['reference_energy']:.12f}, "
              f"delta {cert['result']['delta']:.2e})")
        return 0
    verdict = verify(args.cert, args.tol)
    for ok, msg in verdict["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print("CERTIFICATE ACCEPTED" if verdict["ok"] else "CERTIFICATE REFUSED")
    return 0 if verdict["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
