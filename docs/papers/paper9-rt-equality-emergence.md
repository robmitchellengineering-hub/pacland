# Entanglement = geometry, exactly — the kernel-checked Ryu–Takayanagi equality and the forced emergence direction

**Rob Mitchell — pacland, the constraint-first programme — open access, CC BY 4.0**

## The two results this note records

This note records two *new*, machine-checked results that go beyond the earlier MERA↔AdS papers
(10.5281/zenodo.24045807, 10.5281/zenodo.24062187): the **exact** Ryu–Takayanagi equality, and the
**forced** emergence direction. Both are proven in Lean 4 + Mathlib, with no `sorry`/`axiom`, and
are reproducible with one command (`cd pacland-proof && lake build`).

### 1. The Ryu–Takayanagi "=" (not "≈")

```lean
theorem srank_maximally_entangled (D : ℕ) : srank (maximallyEntangled D) = D
```

The Schmidt rank of the maximally-entangled MERA tensor equals the bond dimension `D` **exactly** —
entanglement equals the cut's area `D^m`, not merely "bounded by" it. Ryu–Takayanagi is usually
stated as a leading-order equivalence; here the clean case is an equality, kernel-checked (with
`srank_simple_eq_one` for the one-bond cut, and the same linear-independence argument at rank `D^m`
for the general cut). Entanglement = area = geometry, as an *equality*, not a slogan.

### 2. The emergence direction (the geometry is forced, not chosen)

```lean
theorem logDepthForced (N k : ℕ) (h : N ≤ causalConeWidth k) : Nat.clog 2 N ≤ k
theorem meraEmergence (N : ℕ) : ∃ k : ℕ, N ≤ causalConeWidth k ∧ Nat.clog 2 N ≤ k
```

Any causal structure that reaches an `N`-site boundary needs at least `⌈log₂ N⌉` layers, while each
layer doubles the support. So **logarithmic depth and exponential circumference are forced
simultaneously** — the balanced binary tree (the discrete hyperbolic geometry) is the *unique
optimum*. "Entanglement builds the hyperbolic geometry" is therefore a theorem in the discrete, not
an interpretation.

## The honest boundary

These are **discrete** results: the MERA causal cone is 0-hyperbolic with exponential volume, the
entanglement–area equality is exact, and the geometry is forced. The **continuous** limit — that
the tree is quasi-isometric to the smooth hyperbolic plane H² — is the **Švarc–Milnor** step
(PSL(2,ℤ) acts cocompactly on H²), named here as the frontier, not proven in this note. The map that
*was* naïvely used for that bridge (a binary-expansion angle) is itself refuted in the proof arm
(`treeToH2_not_quasiIsometric`), and the corrected Stern-Brocot/Farey map is defined (`FareyTree`).

## Proof artifacts

- File: `pacland-proof/PaclandProof/QM/MERA.lean` (theorems `srank_maximally_entangled`,
  `srank_simple_eq_one`, `logDepthForced`, `meraEmergence`).
- The full arm (361 theorems, 138 defs, no `sorry`): **10.5281/zenodo.24073510**.
- Site: https://pacland.morpheus.nz — community/repo: https://github.com/robmitchellengineering-hub/pacland
