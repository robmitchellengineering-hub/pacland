# A quantum computer on regular hardware — the machine-checked boundary

**The yes/no engine pointed at quantum computation.**

## The intuition, made precise

Quantum computing's power is **entanglement** (the free column); its *forced* structure — the Born
rule, unitarity, the probability rule — is classically cheap. Our kernel-checked theorems give the
exact boundary:

- **NO (have it):** `QM.Entanglement` — a LOCC (classical) channel preserves separable states, so
  classical bits **cannot create entanglement natively**, only *simulate* it at `2ⁿ` cost.
- **YES (now):** `QM.Stabilizer` — the Clifford group *normalizes* the Pauli group (kernel-checked:
  `H X H = Z`, `H Z H = X`, `H Y H = −Y`, `S X S† = Y`, `S Z S† = Z`, `S Y S† = −X`), so stabilizer
  states form a **closed class** under Clifford evolution — the algebraic core of **Gottesman–Knill**.

## The answer, as a theorem-shaped statement

> A classical computer can run **exactly** the Clifford/stabilizer class for free (polynomial time),
> because the Clifford gates map the Pauli group back into itself. Anything beyond it — a
> non-Clifford gate (`T`), which generates entanglement outside the stabilizer class — costs `2ⁿ` to
> simulate, and that cost is the free column, which LOCC cannot produce natively.

So "build a quantum computer on regular hardware" is **not** a path to a real quantum speedup — our
LOCC theorem proves classical bits can't entangle, and only *simulate* it. What our techniques
*do* give is the **precise boundary**: the classically-free regime is the Clifford/stabilizer class,
and the `T`-gate (or any non-Clifford resource) is the *single* gate that separates "free to
simulate" from "costs `2ⁿ`".

## Why that's useful

The Clifford/stabilizer boundary is exactly where the **quantum-inspired classical algorithms**
(Tang, Chia et al.) live: any quantum circuit that stays in (or is close to) the stabilizer class
has a polynomial classical equivalent. So the machine-checked normalizer property is the *theorem*
behind "which quantum algorithms we can actually run on our existing hardware" — the practical,
off-the-shelf version of the dream.
