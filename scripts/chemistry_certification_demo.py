#!/usr/bin/env python3
"""The certified-chemistry demo — a DMRG ground-state energy with a sufficiency proof.

    python3 scripts/chemistry_certification_demo.py

The story: run DMRG at increasing bond dimension on the spin-1/2 Heisenberg chain, show the energy
converge, cross-check it against the exact Bethe-ansatz value, write a certificate, then refuse a
forged certificate. This is the wedge-2 product: the energy plus the sweep that proves the bond
dimension was sufficient.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland import chemistry_certify as cc


def main() -> int:
    d = Path(tempfile.mkdtemp(prefix="chem-cert-"))
    cert_path = d / "heisenberg.json"

    print("=== 1. Certify the Heisenberg chain (D-sweep) ===\n")
    cert = cc.certify(40, [10, 20, 40, 80], str(cert_path))
    for row in cert["sweep"]:
        print(f"  bond dim D={row['bond_dim']:>3}   E/L = {row['energy_per_site']:.6f}")
    print(f"\n  converged: delta = {cert['convergence']['delta']:.2e} "
          f"(sufficient={cert['convergence']['sufficient']})")
    print(f"  exact reference (Bethe ansatz, infinite chain): "
          f"E/L = {cert['exact_reference']['value_per_site']:.6f}")

    print("\n=== 2. Verify the certificate (fresh re-run) ===\n")
    v = cc.verify(str(cert_path))
    for ok, msg in v["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  -> {'ACCEPTED' if v['ok'] else 'REFUSED'}")

    print("\n=== 3. A forged certificate is refused ===\n")
    data = json.loads(cert_path.read_text())
    data["sweep"][-1]["energy"] += 0.5   # claim a lower energy than DMRG actually reached
    forged = d / "forged.json"
    forged.write_text(json.dumps(data))
    v = cc.verify(str(forged))
    for ok, msg in v["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  -> {'ACCEPTED' if v['ok'] else 'REFUSED — the certificate caught it'}")

    print("\nThat is the product: an energy, a convergence proof, and a re-run that catches a lie.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
