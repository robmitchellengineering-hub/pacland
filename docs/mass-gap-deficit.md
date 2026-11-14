# The mass gap is a value — using the n=10 wall (the deficit is the deliverable)

## The claim, now machine-checked

`PaclandProof/MassGap.lean` (PR #463) proves two things, on top of Mitchell's
Uniqueness (the tadpole `FᵀJH` is the *unique* bilinear symplectic invariant):

1. **`massScale_not_invariant`** — a symplectic transformation changes the mass scale,
   so the mass scale is not an invariant at all.
2. **`massScale_not_determined_by_tadpole`** — two flux pairs share the same tadpole but
   have different mass scale, so the unique invariant does not fix the mass scale.

Read together: **the mass gap is a *value*, not a *relation***. It is not one of the
exact symplectic invariants (which are exhausted by the tadpole), so no exact structure
can *predict* it — it is a free parameter.

## The wall, classified

The *actual* mass gap — the smallest eigenvalue of the moduli mass matrix — is not
computable at the current level. The wall is **unmeasurable** (the answer exists, the
computation is absent), with the precise cause already recorded:

- the ~96 GB OOM is the **vmapped Newton solver's JIT tracing**
  (`jax.vmap` + `while_loop` + `jnp.linalg.solve` → `broadcast_in_dim`);
- `solver="scipy"` bypasses it (sequential) but the ISD proposal degrades ~40× at
  h12=25 (0 critical points in 13,311 candidates).

## The move — use the wall, deliver the deficit

The four-wall rule says: **unmeasurable → compute the deficit**, not the value. That is
exactly what the repo already records:

```
DeficitObservable("mass spectrum", measured=True, computable=False, validated=False)
```

So the mass gap's honest deliverable is **the deficit** — the *gap* between "measured"
(True) and "computable ∧ validated" (False, False). The value is not the deliverable;
the distance-to-the-value is.

## Why the proof and the wall line up

The proof says the value is not a *relation* (not fixed by the constraint). The wall says
the value is not *computable* (not reachable by the current machinery). Both point to the
same conclusion: **the mass gap sits in the deficit `m`, not in the exact structure.** The
exact structure ends at the tadpole (the constraint); everything past it — W₀, g_s, the
mass spectrum — is a measured-but-unpredicted value, and for the mass spectrum, also
currently uncomputable.

This is the constraint-first "relations, never values" boundary, now with both halves in
place: the *value* side is a theorem (PR #463), and the *deficit* side is the classified
wall (this file).
