# Wedge 2 plan — certified quantum chemistry (DMRG ground states + the certificate)

**Status: plan (not built).** Wedge 1 (`docs/quantum-hardware-verification.md`) is built. This is
the second, larger monetization path: sell *certified* ground-state energies for strongly-correlated
molecules, where the certificate is the differentiator (the open DMRG solvers don't ship a proof the
bond dimension was sufficient).

## Why this market

DFT and Hartree–Fock break on strongly-correlated electronic structure — transition metals, catalyst
active sites, battery cathodes, enzyme cofactors. DMRG (an MPS method — exactly the machinery we
already have) is the leading fix. The buyer is a chemist/materials group for whom a wrong energy is
a failed synthesis, not a rerun; what they pay for is **correctness**, which is precisely what the
certificate supplies.

## What we already have vs what is missing

| have (in repo) | missing (the build) |
|---|---|
| exact MPS backend (`tn_backend.py`) | a DMRG ground-state *solver* (Quimb has one; needs wiring) |
| the area-law proof (`QM.MERA`) — the certificate's theorem | a Hamiltonian source: PySCF/OpenFermion for real molecules |
| `quantum_certify` (hash + falsifier + referee) | the chemistry observables: E₀, and a bond-dimension sufficiency check |

## Build order

1. **Wire Quimb's DMRG** (`qtn.MPS` + `DMRG1`) as a second engine next to `tn_backend.py`, on a
   benchmark molecule (H₂, then a small transition-metal complex).
2. **The sufficiency certificate** — the chemistry analog of the area-law gate: as the bond dimension
   `D` increases, the energy `E(D)` converges; the certificate records `E(D)` and the *D-sweep* as the
   evidence that the answer is converged (exact-to-threshold), citing the area-law theorem for why the
   ground state is low-entanglement in the first place.
3. **A real Hamiltonian** — PySCF (open, free) to produce the molecular integrals; no subscription.
4. **Same `quantum_certify` format** — a chemistry certificate is a quantum certificate whose circuit
   is the DMRG sweep and whose result is `E₀` with its hash + falsifier.

## Honest limits (keep them in the copy)

- DMRG is only exact for the low-entanglement (quasi-1D) sector; strongly-2D/volume-law systems need
  other methods. The certificate says which regime it covers.
- The certificate certifies *convergence and reproducibility*, not that the Hamiltonian is the right
  model — that is the chemist's choice.
- This is not a quantum speedup; it is classical DMRG with a machine-checked sufficiency proof.

## First milestone (the demo that closes the sale)

`E(H₂) = −1.137283…` (a known-exact benchmark) computed by our DMRG, with the D-sweep recorded and
the certificate verifying it — the "we hand you the energy *and* the proof the bond dimension was
enough" story, exactly the same shape as wedge 1's refuse-the-forgery demo.
