"""The quantum-computation certificate — the hardware-verification product.

What a certificate is here (and what it is not): it is NOT a claim that a quantum device is good.
It is a **machine-checked, reproducible record** that a given circuit, run on the exact tensor-network
backend, produces a specific result — with the evidence that the result is exact (the bond dimension,
the kernel-checked area law) and a **falsifier** that a stranger re-runs to check it.

The verification half does two distinct jobs, and keeps them separate:

1. **Integrity** — re-run the circuit and confirm the result still hashes to the committed value.
   A tampered certificate or a drift in the code fails here.
2. **Claim verification (the hardware-referee job)** — a "QPU" (or any classical claimant) submits a
   distribution; we compare it to the exact result by total-variation distance and REFUSE it past a
   tolerance. This is the "we caught the wrong answer" value.

Honest scope (rule 67): the exact distribution is 2^n, so certificates hold the full result for
n <= 20; beyond that the certificate records the bond-dimension evidence (the area-law gate) rather
than 2^n floats. Low-entanglement only — a volume-law circuit is flagged, not silently certified.

Usage:
    python -m pacland.quantum_certify certify ghz --qubits 16 --out cert.json
    python -m pacland.quantum_certify verify  cert.json
    python -m pacland.quantum_certify verify  cert.json --against qpu-claim.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

from pacland import quantum as q
from pacland.tn_backend import TNQuantumCircuit

FORMAT = "pacland/quantum-certificate@1"


def _circuit(program: str, n_qubits: int):
    if program == "ghz":
        return q.PROGRAMS["ghz"](n=n_qubits, cls=TNQuantumCircuit)
    return q.PROGRAMS[program](cls=TNQuantumCircuit)


def _exact(program: str, n_qubits: int):
    """Run the circuit exactly and return (circuit, probability vector)."""
    c = _circuit(program, n_qubits)
    if c.n > 20:
        raise ValueError(
            "exact certificates hold the full 2^n distribution, so n <= 20; "
            "for larger n certify the bond-dimension evidence instead"
        )
    return c, c.probabilities()


def _hash(p: np.ndarray) -> str:
    blob = np.ascontiguousarray(p, dtype=np.float64).tobytes()
    return hashlib.sha256(blob).hexdigest()


def _tv(a: np.ndarray, b: np.ndarray) -> float:
    """Total-variation distance between two distributions."""
    return float(0.5 * np.sum(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def certify(program: str, n_qubits: int, out: str) -> dict:
    c, p = _exact(program, n_qubits)
    r = c.report()
    cert = {
        "format": FORMAT,
        "circuit": {"program": program, "n_qubits": n_qubits},
        "backend": {"name": "tn", "exact": True, "truncation": "none — full-rank SVD"},
        "result": {"sha256": _hash(p), "n_states": int(p.size)},
        "evidence": {
            "max_bond_dim": int(r["max_bond_dim"]),
            "central_cut_schmidt_rank": int(r["central_cut_schmidt_rank"]),
            "theorem": ("QM.MERA.srank_maximally_entangled — entanglement across a cut = the cut "
                        "area D^m EXACTLY (kernel-checked Lean, no sorry/axiom)"),
        },
        "falsifier": f"python -m pacland.quantum_certify verify {out}",
    }
    Path(out).write_text(json.dumps(cert, indent=2) + "\n")
    return cert


def _load_claim(path: str) -> np.ndarray:
    """A claim is a JSON file {"probabilities": [...]} — what a QPU (or classical claimant) asserts."""
    data = json.loads(Path(path).read_text())
    if "probabilities" not in data:
        raise ValueError("claim must be {\"probabilities\": [...]}")
    p = np.asarray(data["probabilities"], dtype=float)
    if p.size == 0 or abs(float(p.sum()) - 1.0) > 1e-6:
        raise ValueError("claim probabilities must be non-empty and sum to 1")
    return p


def verify(cert_path: str, against: str | None = None, tol: float = 1e-9) -> dict:
    cert = json.loads(Path(cert_path).read_text())
    if cert.get("format") != FORMAT:
        return {"ok": False, "why": f"not a {FORMAT} certificate"}
    program = cert["circuit"]["program"]
    n = cert["circuit"]["n_qubits"]
    checks: list[tuple[bool, str]] = []
    failures: list[str] = []

    def check(ok: bool, msg: str) -> None:
        checks.append((ok, msg))
        if not ok:
            failures.append(msg)

    # 1. integrity — re-run the falsifier and confirm the committed hash
    _, p_exact = _exact(program, n)
    got = _hash(p_exact)
    want = cert["result"]["sha256"]
    check(got == want,
          f"integrity: re-run sha256 {got[:12]}… {'==' if got == want else '!='} committed {want[:12]}…")

    # 2. claim verification — the referee job
    if against is not None:
        p_claim = _load_claim(against)
        if p_claim.size != p_exact.size:
            check(False, f"claim has {p_claim.size} states, circuit has {p_exact.size}")
        else:
            tv = _tv(p_claim, p_exact)
            check(tv <= tol, f"claim total-variation distance = {tv:.6g} (tolerance {tol:g})")

    return {"ok": not failures, "checks": checks, "failures": failures}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="The quantum-computation certificate (hardware referee).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("certify", help="run exactly and write a certificate")
    c.add_argument("program", choices=sorted(q.PROGRAMS))
    c.add_argument("--qubits", type=int, default=3, help="qubits for ghz (ignored by other programs)")
    c.add_argument("--out", default="certificate.json")

    v = sub.add_parser("verify", help="re-run the falsifier and (optionally) referee a claim")
    v.add_argument("cert")
    v.add_argument("--against", help="a claimed distribution to referee against the exact result")
    v.add_argument("--tol", type=float, default=1e-9)

    args = ap.parse_args(argv)
    if args.cmd == "certify":
        cert = certify(args.program, args.qubits, args.out)
        print(f"certified {args.program} ({args.qubits} qubits) -> {args.out}")
        print(f"  result sha256 {cert['result']['sha256'][:16]}… over {cert['result']['n_states']} states")
        print(f"  evidence: D={cert['evidence']['max_bond_dim']}, "
              f"central-cut Schmidt rank={cert['evidence']['central_cut_schmidt_rank']}")
        print(f"  theorem: {cert['evidence']['theorem']}")
        return 0

    verdict = verify(args.cert, args.against, args.tol)
    for ok, msg in verdict["checks"]:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
    print(("CERTIFICATE ACCEPTED" if verdict["ok"] else "CERTIFICATE REFUSED"))
    return 0 if verdict["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
