# Discovery harvest — transfer-matrix methodologies and renormalisation schemes

Status: 2026-11-22, the first SEXTANT harvest on the re-orientated question. What is real, what is
claimed, and what each route is falsified by.

## The question (what the engine is now pointed at)

Find a **transfer-matrix methodology that reaches the weak-coupling exponential** and a
**renormalisation scheme** (the running coupling / beta function) that carries `e^{−cβ}` — the two
ingredients the finite-dimensional spectral machinery provably lacks.

## What the harvest found, sorted by trust

### Real, rigorous methodologies (the candidates)

| route | what it is | falsifier |
|---|---|---|
| **Polchinski flow equation** (exact RG) | decomposes the YM measure into scales via the exact flow; the scale-by-scale coupling running | does the integrated flow reach `e^{−cβ}` uniformly in volume? |
| **Block-spin / decimation RG** (Kadanoff–Wilson) | the block-spin transformation + the renormalisation of the coupling | does the blocked transfer matrix's gap track the running coupling? |
| **Gradient flow / trivialising maps** (Lüscher) | the Wilson flow as a change of measure toward a Gaussian; a flow-time bound | does a flow-time lower bound reach `e^{−cβ}`? |
| **Constructive RG** (Balaban's multi-scale cluster expansion) | the actual route worked for decades; multi-scale expansions + renormalisation | the known gaps (never fully closed to a complete proof) |
| **Transfer matrix + reflection positivity** (the bridge) | clustering ⟺ spectral gap — KERNEL-CHECKED, but no β-dependence | the spectral gap's weak-coupling behaviour is not derivable from it alone |

### Claimed, unverified (treat as candidates, not settled)

Several Zenodo / OSF preprints claim a complete constructive proof (e.g.
["A Constructive Solution to the Clay Millennium Yang-Mills Problem with a Mass Gap in Four Dimensions"](https://osf.io/hnw5p_v1/download/?format=pdf)
and an "Irreversible-Action Augmented" proof). There is also a
[critique of one such claim](https://zenodo.org/records/23591906/preview/CRITIQUE_yang_mills_jesse.md). These
are **preprints, not peer-reviewed, and at least one is explicitly critiqued** — they are pointers to
methodology, not evidence the rung is crossed. Per the falsifier-before-belief rule, none is recorded
as surviving.

## The honest synthesis

1. The **transfer-matrix spectral bridge** is the correct *container* for the gap — kernel-checked,
   no `sorry`. It does not, by itself, carry β.
2. The **renormalisation schemes** (Polchinski, block-spin, gradient flow/trivialising maps,
   constructive RG) are the real candidates for the running coupling. They are the *right* place to
   point the engine.
3. **None of them has a complete, verified proof of the weak-coupling exponential** — the claimed
   proofs are unverified preprints with a critique. This is the actual state of the frontier: the
   methodology family is known, the complete proof is not.

## What the engine does next (the search, not the manufacture)

File each scheme above as a SEXTANT hypothesis with its falsifier (`does the scheme's bound reach
`e^{−cβ}` uniformly in volume?`), and run the harvest/synthesis loop to pull the *specific* lemma or
estimate from each scheme that would carry the running coupling — the transfer of structure across
the renormalisation schemes, judged by `bound_search.check_bound`.
