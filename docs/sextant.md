# SEXTANT — the verified quantum referee (proof engine on a simulated quantum computer)

**One line:** SEXTANT reads where every quantum claim sits — **FORCED** (a theorem), **FREE**
(a label), or **IMPOSSIBLE** (a no-go) — and hands you the machine-checked proof, not just the
floating-point number.

## The headlines

1. **The simulator methods are *proved*, not just tested.** The three engines everyone uses each
   carry a kernel-checked theorem behind their algebraic core:
   - **Clifford/stabilizer** (Stim) → `QM.Stabilizer` (Clifford normalizes Pauli, so the class is polynomial — Gottesman–Knill).
   - **tensor-network / geometric** (Quimb) → `QM.MERA` (entanglement ≤ cut area `D^m` — the Ryu–Takayanagi core).
   - **full state vector** (QuEST) → the *free column* (`2ⁿ`), proved to be the only escape from the Clifford class.
2. **"Entanglement = geometry" is now a theorem.** The MERA causal cone is a proven **discrete
   hyperbolic space**: exponential volume, log depth, area law, and **Gromov 0-hyperbolicity**
   (the four-point condition) — machine-checked in `QM.MERA` + `QM.Hyperbolic`.
3. **Every claim carries a falsifier, written before the run.** `chsh` → "exceed 2√2";
   `no-cloning` → "a universal cloner"; `clifford-polynomial` → "a T-gate circuit blowing past 2ⁿ".

## Install

```bash
git clone https://github.com/robmitchellengineering-hub/pacland
cd pacland
pip install -e .          # installs the `sextant` command
pip install stim quimb numpy   # the simulator engines (numpy ships with it)
```

## Use

```bash
sextant --list             # all 21 claims, one verdict each
sextant chsh               # the CHSH bound, simulated and certified
sextant clifford-polynomial  # Stim runs 1000 qubits in ~3 ms, certified polynomial
sextant entanglement-area    # Quimb MPS: S ≤ log D, the area law, certified
```

Every verdict prints the **simulated value**, the **theorem** (kernel-checked), the **falsifier**,
and the **oracle class** (quantum-simulated / kernel-checked / exact-symbolic).

## The constraint it adds for research

Any claimed entanglement or geometry result must satisfy, on pain of being **wrong** (not just
unusual): (a) the **area law** `entanglement ≤ D^m`, and (b) the **four-point 0-hyperbolicity**
condition. SEXTANT is the machine-checked referee that enforces them.
