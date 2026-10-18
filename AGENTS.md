# PACLAND — operating rules (read before working in this repo)

## The one rule that matters: USE the wall, don't hit it

"Uncomputable" is **four different walls**, each with a *way around*. A wall is
not a place to stop — the way around IS the result.

| wall | meaning | the move (use this, don't just report the wall) |
|---|---|---|
| **intractable** | answer exists, no feasible algorithm | prove intractability (a theorem), or find structure that shortcuts it |
| **unmeasurable** | answer exists, ground truth / data absent | compute the **deficit** — how far we are from measuring it |
| **underdetermined** | no unique answer exists | compute the **set's invariants** (constraints, boundary), not the nonexistent point |
| **undecidable** | provably no algorithm | prove undecidability (an impossibility certificate) |

Rob's rule, verbatim: *"you hit a wall instead of using the wall."* When a
computation fails (OOM, too slow, no known value), classify which wall it is and
apply the move. Example that already happened: the mass spectrum is killed even at
n=10 → that is the **unmeasurable** wall → the deliverable is the *deficit* (m), not
the spectrum. Documenting the wall is not the result; using it is.

## Hard physics rule: mirror symmetry is a free validation target

For a Calabi-Yau threefold and its mirror (the polar dual polytope):

    h11_m = h21,   h21_m = h11,   chi_m = -chi    (chi = 2(h11 - h21))

This is an always-true theorem, so **any CY's mirror gives a known-exact answer to
validate the oracle against, for free** — no external database needed. Encoded as
`pacland.guards.guard_mirror_symmetry` (mutation-tested). Verified pair:
quintic (1,101,−200) ↔ mirror quintic (101,1,+200). Use it whenever the corpus needs
more known-answer manifolds.

## State (durable facts)

- The **Mitchell Verification Deficit** is the count `m` of observables that are
  simultaneously measured + computable + validated. Today **m = 5**: topology
  (CYTools: h11, h21, c2, κ) = 4, flux (JAXVacua: tadpole = exact symplectic
  pairing FᵀJH) = 1. SM physics = 0 (the real frontier).
- `pacland climb` runs the deficit climber on the mesh (studio-linux via
  `mac → win-2 → studio-linux`); `data/cy_corpus.json` is the answer key.
- Live site: https://pacland.netlify.app (Netlify) + GitHub Pages mirror.
- The four-wall map is `src/pacland/limits.py` and `docs/boundary-map.md`.
