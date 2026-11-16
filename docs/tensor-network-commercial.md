# Tensor networks on existing hardware — who pays for this, and why

**One page.** The answer to "is the tensor-network / deterministic-in-use methodology monetizable,
and by whom." Written against what is actually in the repo (not a pitch): the exact MPS backend
(`src/pacland/tn_backend.py`), the machine-checked area law (`pacland-proof/PaclandProof/QM/MERA.lean`),
and the deterministic-in-use ledger (`docs/deterministic-ledger.md`).

## The honest position first

The **raw simulator is a crowded, mostly-free capability.** Quimb, ITensor, TeNPy, DMRG++, NVIDIA
cuQuantum and Qiskit Aer are all open and faster than anything we will ship in a week. We are not
going to out-run ITensor on speed, and we should not try — that is a wall, and the way around it is
the whole point.

**What we uniquely have is the theorem.** Nobody else ships "a tensor-network simulator **plus a
machine-checked proof that low bond dimension is exact, not a heuristic**" (`srank = D` exactly,
the Ryu–Takayanagi "=", the forced emergence). The proof is what turns a fast-but-approximate method
into a fast-*and-exact* one, and that is the one thing an industrial buyer cannot get from an open
library. The moat is not the simulation; it is the certificate.

## Who pays, and why

### 1. Quantum-hardware verification — the referee (strongest fit, near-term)

As quantum vendors ship larger devices, the unsolved problem is **trust**: the device outputs a
bitstring, and nobody can check it classically once it is big enough — *except* tensor networks, on
the class of circuits that are still classically simulable. Cross-entropy benchmarking, spoofing a
supremacy claim, and certifying a VQE result are all "your QPU says X; here is the machine-checked
proof X is exact." That is SEXTANT's position, and it is a real, emerging market: the customer is a
quantum vendor who must prove correctness, or a user who must not be defrauded. **This is the one to
lead with**, because the certificate is the product and we already have it.

### 2. Quantum chemistry / materials — certified DMRG (mature market, we compete on the certificate)

DMRG/tensor networks are the standard fix for strongly-correlated electronic structure (transition
metals, catalysts, battery cathodes, enzyme active sites) where DFT and Hartree–Fock break. The
market is real (Schrödinger, ORCA, PySCF, pharma and materials). We do not compete on speed; we
compete on **"the ground-state energy, plus a proof the bond dimension was sufficient."** Correctness
is the expensive thing for industrial users — a wrong energy costs a failed synthesis, not a rerun.
That is exactly what a certificate sells.

### 3. Dev tooling / simulator SDK — on-ramp, not revenue

The simulator itself (a `--backend tn` on `quantum.py`) is a credible free on-ramp: developers run
and debug quantum circuits past 30 qubits before hardware exists. It is crowded and free, so it is
the funnel, not the billable line. It earns the conversation for (1) and (2).

## What is monetizable on the machines we already have

All of it — **no new hardware, no subscription.** Chemistry DMRG and hardware verification run on
`pacland-rog` and `win-2` today; GPU rental remains the standing exception only when a job genuinely
needs a large card. The cost is compute we already own, so the margin is the certificate, not the
cloud.

## The honest "not monetizable" list

- **Not a quantum speedup.** A classical simulation of a quantum computer is `2^n`; it never beats a
  classical algorithm for the same task. We sell *verification and exactness*, never "we made quantum
  computing fast on a laptop."
- **Not volume-law circuits.** The method only helps the low-entanglement class. We say so, because a
  customer who finds the wall undisclosed is a customer lost.
- **Not the free parameters.** Proofs force what is FORCED (counts, constraints, labels, arithmetic);
  the values (the 19 SM parameters, Λ, W₀) are measured dials and are not for sale. What we sell is
  the *floor and the deficit* — knowing exactly which numbers can be computed and which cannot.

## The one-line pitch

> "We hand you the answer **and the machine-checked theorem that says it is exact** — for verifying
> quantum hardware, and for the chemistry where being wrong is expensive. The simulator is free; the
> certificate is the product."

## Where this sits

Companion to `docs/deterministic-ledger.md` (what is exact) and `docs/sextant.md` (the referee).
The code it describes: `src/pacland/tn_backend.py`, `src/pacland/quantum.py --backend tn`.
