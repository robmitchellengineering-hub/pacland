# pacland-proof — the machine-checked theorem arm

Lean 4 + Mathlib formalization of the constraint-first tower's core. The sympy
scripts in `../scripts/` give *exact symbolic* proofs at fixed cases (b₃ = 6,
degrees 1–5); this directory is the **machine-checked** proof — the statement is
verified by Lean's kernel, not by a computation.

## Status

| theorem | file | status |
|---|---|---|
| **Mitchell's Uniqueness Theorem** (n = 1) | `PaclandProof/Mitchell.lean` | ✅ proven |
| shear `fromBlocks 1 X 0 1` is symplectic (symmetric `X`) | `PaclandProof/General.lean` | ✅ proven |
| diagonal `fromBlocks U 0 0 V` symplectic (`UᵀV = 1`) | `PaclandProof/General.lean` | ✅ proven |
| pairing `(Sx)ᵀ J (Sy) = xᵀ J y` is Sp-invariant | `PaclandProof/General.lean` | ✅ proven |
| full uniqueness, general n | same argument in every dimension | next |

`Mitchell.lean` proves, machine-checked, that for the `2×2` symplectic form
`J = [[0,1],[-1,0]]` the only matrices `M` with `Sᵀ M S = M` for *every*
symplectic `S` (`Sᵀ J S = J`) are the scalar multiples of `J`. That is the
degree-2 core of Mitchell's Uniqueness Theorem: the tadpole pairing is the *only*
symplectic invariant bilinear form.

The proof instantiates two generators of `Sp(2) = SL(2)` — the shear `[[1,1],[0,1]]`
and the dilation `[[2,0],[0,1/2]]` — extracts the entry constraints, and shows
`M = c · J`. It also proves `J` is antisymmetric (`J + Jᵀ = 0`), the reason the
"diagonal" flux candidates `FᵀJF = HᵀJH = 0` vanish.

`General.lean` proves the machinery the general-n uniqueness argument rests on, in
**abstract** form (any finite index type `l`, any field `R`): the symplectic
generators (shear, diagonal, and the swap `J` itself, via
`SymplecticGroup.fromBlocks_mem_iff`) and the pairing-invariance identity
`(Sx)ᵀ J (Sy) = xᵀ J y` — the reason the tadpole is *an* invariant.

## Reproduce

```
# one-time: install Lean (elan) — https://lean-lang.org/lean4/doc/setup.html
cd pacland-proof
lake build          # downloads the mathlib cache on first run, then builds
```

A green `lake build` means Lean's kernel accepted every theorem. No `sorry`, no
`axiom`, no `native_decide` — every theorem is kernel-checked.

## The honest boundary

- The **full uniqueness** is proven for **n = 1** (2×2); the general-n statement is
  the next target. The generator facts and the pairing invariance are already proven
  in abstract form (`General.lean`); the block-matrix extraction for the full
  general-n theorem is the remaining step.

### The general-n proof sketch (what the formalization must encode)

The argument is worked out in full; it is mechanical to encode, not to re-derive.
Decompose `M = fromBlocks P Q R S` (with `l×l` blocks) and use three symplectic
generators against the invariance hypothesis `Sᵀ M S = M`:

1. **Shear** `fromBlocks 1 X 0 1` (symmetric `X`, symplectic by `shear_mem`):
   invariance gives `P·X = 0` and `X·P·X + S·X + X·Q = 0` for every symmetric `X`.
2. Take `X = 1`: **`P = 0`** and **`S = −Q`**.
3. General symmetric `X`, with `P = 0`, `S = −Q`: `X·Q = Q·X` for every symmetric `X`.
4. Lemma (`scalar_of_commute_all_symm`): a matrix commuting with every symmetric
   matrix is scalar, so **`Q = λ·1`** (proof: `single j j` forces `Q` diagonal;
   `single i j + single j i` forces the diagonal entries equal).
5. **Swap** `J` itself (symplectic by `J_mem`): invariance gives `S = P = 0`
   (consistent) — done already in step 2, but re-derivable.
6. Assemble: `M = fromBlocks 0 (λ·1) (−λ·1) 0 = −λ · (fromBlocks 0 1 (−1) 0) = c·J`.

So `M` is a scalar multiple of `J`. Steps 1, 2, 5 are `fromBlocks_multiply` /
`fromBlocks_transpose` / `fromBlocks_inj` bookkeeping; steps 3–4 are the scalar
lemma. These are the exact lemmas the next formalization pass adds.

- The **all-degrees** statement (Constraint-First / FFT) is Weyl's 1939 theorem,
  taken as a citation (with the sympy degree 1–5 verification as evidence), not
  re-proven here.
- **Mitchell's Completeness Theorem** (transitivity of `Sp` on each tadpole level
  set) is the next formalization target after general-n uniqueness.
