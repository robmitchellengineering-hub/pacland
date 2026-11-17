# Quantum hardware verification — the certificate is the product

**Wedge 1 of the monetization plan** (`docs/tensor-network-commercial.md`). This is the concrete
product, built and runnable: a machine-checked, reproducible certificate for a quantum computation,
plus the referee that refuses a wrong answer.

## What it is

`python -m pacland.quantum_certify` runs a circuit **exactly** on the tensor-network backend, records
the result's hash, the area-law evidence, and the kernel-checked theorem, and writes a certificate
whose **falsifier** anyone can re-run to check it. The verify half does two separate jobs:

1. **Integrity** — re-run the circuit; a drift in the code or a tampered certificate fails the hash.
2. **Claim verification (the referee)** — a QPU (or any classical claimant) submits a distribution;
   we compare it to the exact result by total-variation distance and **refuse** it past a tolerance.

## The one-line pitch

> *"We hand you the answer **and the machine-checked theorem that says it is exact**, and we catch
> the wrong one."*

## Run it

```sh
python -m pacland.quantum_certify certify ghz --qubits 16 --out cert.json
python -m pacland.quantum_certify verify  cert.json
python -m pacland.quantum_certify verify  cert.json --against qpu-claim.json
python3 scripts/quantum_verification_demo.py     # the full refuse-the-forgery story
```

The demo's forged claim (a device that *dropped* the entanglement) is refused at total-variation
distance ≈ 1.0; the true claim is accepted at ≈ 0.

## Honest scope (what the certificate covers, and what it does not)

- **Exact for n ≤ 20** — the certificate holds the full `2^n` distribution. Beyond that it records the
  bond-dimension evidence (the area-law gate), not `2^n` floats.
- **Low-entanglement only.** A volume-law circuit is flagged by the area-law gate, not silently certified.
- **This is a classical referee, not a quantum speedup.** The value is *verification and exactness*,
  never "we made the QPU faster."

## Who pays, and what closes the sale

The buyer is anyone who cannot trust a quantum device's output (or a classical claim dressed up as
quantum). To turn this from a library into revenue, the next two pieces are:

1. **A signer identity** — reuse `src/pacland/certify/integrity.py` (OpenSSH `ssh-keygen -Y sign`)
   so each certificate carries a verifiable issuer, not just a hash.
2. **A demo customer target** — a public "we will certify your VQE/sampling result" page with one
   concrete certified example, so the first paid verification has a place to land.
