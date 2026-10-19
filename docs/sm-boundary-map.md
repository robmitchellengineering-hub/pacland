# The four-wall map for the Standard Model

The boundary map (`docs/boundary-map.md`, `src/pacland/limits.py`) classified the *flux*
sector's uncomputability into four walls. This extends it one sector up, to the Standard
Model — so we know where the SM deficit can climb and where it cannot.

The headline up front: the SM's **exact structure is computable and validated** (that is
why the deficit climbed to m = 9). What *remains* a wall is the values, the UV completion,
and the non-perturbative tail — each a different wall with a different move.

## The map

| question | wall | justification | what remains computable (the move) |
|---|---|---|---|
| Predict the 19 parameter *values* | **underdetermined** | within the SM they are free inputs — no unique value exists; the rank test shows the floor is real (no known symmetry collapses them) | the set's invariants: 19 = orbit-space dimension, and the rank test (real floor) |
| Identify the UV completion (which CY/GUT) | **underdetermined** | many UV completions realize the same SM — the inverse problem has no fingerprint | the exact structure shared by all of them: anomaly cancellation, hypercharge uniqueness, N_gen = 3, 19 |
| Verify a candidate UV completion's SM predictions | **unmeasurable** | no experiment probes the UV scale — the compactification's ground truth is absent | the deficit (m = 9, climbing); anomaly 5/5 and hypercharge 4/4 are the first validated SM rungs |
| Non-perturbative QCD (hadron masses, muon g-2 hadronic) | **intractable** | lattice QCD is feasible but costly; some quantities need large Monte Carlo | lattice QCD — a working, validated tool |
| Why θ_QCD ≈ 0 (strong CP) | **underdetermined** | θ is a free parameter (1 of the 19); the SM gives no reason for its smallness | a mechanism (axion, …) is a concrete falsifiable target constrained by the measured θ ≈ 0 |

## What this tells us about where the SM deficit can climb

- The **constraints** (anomaly cancellation, hypercharge uniqueness) are computable and
  already climbed — they are *not* walls.
- The **labels** (N_gen = 3, the gauge group) are computable and climbed.
- The **count** (19 = orbit-space dimension) is computable and climbed.
- The **values** are underdetermined — so the SM deficit can never grow by "predicting"
  them; the growth is in validating the *exact structure*, which is now done (m = 9), and in
  the non-perturbative tail (lattice QCD, where more validated observables are available in
  principle but cost compute).

The SM is therefore the mirror image of the flux sector: the flux sector's exact content
saturates at 1 (the tadpole), while the SM's exact content saturates at 4 (constraints +
labels + count). The rest is, in the four-wall sense, underdetermined/unmeasurable — which
is exactly the constraint-first statement, now written as a map.
