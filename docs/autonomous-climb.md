# The autonomous deficit climber — "run it and it hones in"

`pacland climb` runs the whole compute→validate→count loop in one command, over the
mesh, and reports the Mitchell Verification Deficit as it closes.

## What it does

1. Reads `data/cy_corpus.json` — a corpus of Calabi-Yau manifolds with *known exact*
   topological invariants (the answer key).
2. Dispatches `scripts/climb_deficit.py` to `studio-linux` (the only node with
   CYTools), base64-encoded so nothing breaks across the `mac → win-2 → studio-linux`
   hop.
3. For each manifold, CYTools computes `h11`, `h21`, `chi`, `c2`; each is compared to
   the known value.
4. Accumulates **m** (the number of *independent* observables validated — the rungs
   that shrink the certificate) and **n** (total validation points), and reports the
   radius `sqrt(ln(1/delta)/2m)`.
5. Exits 0 iff every known value matches — a self-asserting result.

```
$ pacland climb
Deficit climb report — CYTools on studio-linux
  quintic P4[5]: PASS
    h11 got=1 expected=1 ok        h21 got=101 expected=101 ok
    chi got=-200 expected=-200 ok  c2 got=[-250,50,50,50,50,50] expected=... ok
  m = 3  (validated: c2, h11, h21)
  n = 3 validation points
  certificate radius = 0.7841
  all passed: True
```

## How it hones in

Two levers, both in the corpus:

- **Add a manifold** → grows `n`, tightening the oracle's empirical error model
  (more evidence that CYTools is exact, across more examples).
- **Add an observable** to `known` (and to `counted`) → grows `m`, shrinking the
  certificate radius directly.

The honest discipline is encoded in the `counted` list: `chi` is *derived*
(`chi = 2(h11-h21)`) and the triple intersection is *basis-dependent*, so neither is
counted toward `m` — only independent invariants climb the ladder.

## Extending it

Add a manifold to `data/cy_corpus.json` (polytope + known values), then re-run
`pacland climb`. The next rungs beyond topology — gauge couplings, the mass
spectrum — get added the same way once an oracle can compute them: that is the
path the whole project is climbing.

Files: `scripts/climb_deficit.py` (the self-asserting climber),
`src/pacland/climb.py` (the mesh dispatch), `data/cy_corpus.json` (the answer key).
