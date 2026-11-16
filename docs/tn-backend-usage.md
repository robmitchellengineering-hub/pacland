# Using the tensor-network backend

The quantum computer has two backends: **statevector** (the default, `2^n` amplitudes, ~30-qubit
ceiling) and **tn** (an exact matrix-product state, `~n·D²` memory, past 30 qubits for
low-entanglement circuits). Both run the *same* circuit model, so a program written on one runs
unchanged on the other — and on a real QPU when one exists.

## One-liners

```sh
python -m pacland.quantum bell --backend tn --shots 1000
python -m pacland.quantum grover --backend tn
python -m pacland.quantum ghz --backend tn --qubits 64 --shots 8     # past the 30-qubit wall
python -m pacland.quantum teleport --backend tn
python -m pacland.quantum qec --backend tn
```

Programs: `bell`, `superposition`, `grover`, `ghz`, `qft2`, `teleport`, `qec`. `--qubits` sets the
GHZ size (default 3). Every `tn` run prints the **area-law gate**: the bond dimension `D`, the
central-cut Schmidt rank, and the MPS memory vs the state-vector memory.

## As a library

```python
from pacland.tn_backend import TNQuantumCircuit

c = TNQuantumCircuit(64)
c.apply_gate("H", 0)
for q in range(1, 64):
    c.apply_cnot(0, q)          # GHZ(64)

bits, _ = c.measure(5)          # ['000…0', '111…1', …]
r = c.report()                  # max_bond_dim=2, ~8 KB vs 2^64·16 bytes
```

Gates: `apply_gate("H"|"X"|"Y"|"Z"|"S"|"T", q)`, `apply_cnot(c,t)`, `apply_cz(a,b)`,
`apply_cphase(c,t,angle)`, `measure(shots)`, `amplitude(bits)`, `probabilities()` (n ≤ 20),
`probability_of(bits)`.

## The honest boundary

- **Exact, not approximate.** Every gate is applied by a full-rank SVD (no truncation); the TN
  backend matches the state vector bit-for-bit. `report()` is the gate that shows when the bond
  dimension is growing, so a volume-law circuit is visible instead of silently truncating.
- **Low-entanglement only.** Area-law circuits (GHZ, shallow circuits, stabilizer) stay small and
  exact past 30 qubits. Volume-law circuits grow `D → 2^(n/2)` and hit the same wall — the gate says so.
- **Not a speedup.** This is a classical simulation. The machine-checked area law (`QM.MERA`) is
  what certifies that low `D` is exact, not heuristic.

## The deterministic-in-use side

```sh
python3 scripts/deterministic_vs_sampling.py   # closed form vs Monte Carlo, and 3^200 − 1
python -m pacland.sextant --list               # the referee: all claims, one verdict each
python -m pacland.sextant entanglement-area    # the area law behind the tn backend
```
