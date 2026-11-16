#!/usr/bin/env python3
"""The hardware-verification demo — the certificate catches a wrong answer.

    python3 scripts/quantum_verification_demo.py

The story, end to end: certify a circuit exactly, then referee three submitted results —
the true one (accepted), a forged one that dropped the entanglement (refused), and a tampered
certificate (refused). This is the wedge-1 product: "we hand you the answer and the
machine-checked theorem that says it is exact, and we catch the wrong one."
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from pacland import quantum_certify as qc


def main() -> int:
    d = Path(tempfile.mkdtemp(prefix="quantum-verify-"))
    cert_path = d / "certificate.json"

    print("=== 1. Certify GHZ(16) exactly (the tensor-network backend) ===\n")
    cert = qc.certify("ghz", 16, str(cert_path))
    print(f"  result sha256 {cert['result']['sha256'][:16]}… over {cert['result']['n_states']} states")
    print(f"  evidence: max bond dim D={cert['evidence']['max_bond_dim']} — "
          f"entanglement = cut area, exact (kernel-checked Lean)")

    print("\n=== 2. Integrity — re-run the falsifier against the certificate ===\n")
    v = qc.verify(str(cert_path))
    for ok, msg in v["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  -> {'ACCEPTED' if v['ok'] else 'REFUSED'}")

    print("\n=== 3. The forged QPU claim — a device that DROPPED the entanglement ===\n")
    n = 2 ** 16
    forged = d / "qpu-claim-uniform.json"
    forged.write_text(json.dumps({"probabilities": [1.0 / n] * n}))
    v = qc.verify(str(cert_path), against=str(forged))
    for ok, msg in v["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  -> {'ACCEPTED' if v['ok'] else 'REFUSED — the referee caught it'}")

    print("\n=== 4. The true claim — matches the exact result ===\n")
    _, p_exact = qc._exact("ghz", 16)
    true = d / "true-claim.json"
    true.write_text(json.dumps({"probabilities": p_exact.tolist()}))
    v = qc.verify(str(cert_path), against=str(true))
    for ok, msg in v["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  -> {'ACCEPTED' if v['ok'] else 'REFUSED'}")

    print("\nThat is the product: exact, machine-checked, and it refuses a wrong answer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
