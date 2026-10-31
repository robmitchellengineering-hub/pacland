# Reverberation chambers: the usable frequency is not three times the fundamental

**Reproduce:** `python3 scripts/chamber.py 3.0,2.5,2.2 1.0`

A reverberation chamber is judged on its modes. Below some frequency it is **under-moded** — the field is a set
of isolated resonances, not a diffuse field — and a test result taken there carries an error nobody has bounded.
That boundary is the **lowest usable frequency**, and it is a mode-counting question: the thing this engine
computes exactly.

**The rule of thumb in use is `LUF ≈ 3 × c/(2·L_max)`.** It is a heuristic, it ignores the chamber's quality
factor, and **it is optimistic.**

## The measurement

A 3.0 × 2.5 × 2.2 m chamber, V = 16.5 m³, S = 39.2 m², band to 1 GHz:

| quantity | value |
|---|---|
| fundamental `c/(2·L_max)` | **50.0 MHz** |
| LUF, rule of thumb (3 × fundamental) | **149.9 MHz** |
| LUF, mode density (Q = 100) | **186.6 MHz** — 1.24× the rule |
| LUF, mode density (Q = 200) | **235.1 MHz** — 1.57× the rule |
| LUF, mode density (Q = 400) | **296.2 MHz** — 1.98× the rule |
| modes to 1 GHz, exact | 5,100 |
| Weyl prediction | 5,096 — **−0.08%** |
| distinct frequencies | 2,725 (**46.6% degenerate**) |

**The finding: LUF depends on Q, and the rule of thumb does not.** For a chamber with Q ≈ 400, the frequency at
which the field becomes diffuse is **twice** the rule-of-thumb figure. A chamber specified and used at the rule
is measuring in a field that is not diffuse.

## The criterion, stated so it can be argued with

A mode has width `f/Q`. The field is diffuse when at least one other mode sits **inside that width**:

```
density(f) · f/Q ≥ 1          density(f) = 8π f² V / c³   (Weyl volume term, two polarisations)
```

Solve for the first `f` where that holds, and that is `LUF_density`. It is **one criterion among several** in
use — different standards pick different thresholds (two modes inside the width, three, a stated field
uniformity). **What this engine adds is not the criterion; it is that the number is computed from the chamber's
own dimensions and its measured Q, with the criterion named.**

## Why this is the wedge for the RF work

1. **The market already judges chambers this way** — mode count and over-modedness are the vocabulary of EMC
   test houses, so there is nothing to teach.
2. **Measurement uncertainty is regulated there**, which is exactly what the certificate format is for: a
   chamber analysis can carry its falsifier and its bound, and no incumbent does.
3. **It is the same arithmetic as the room work** — Weyl, degeneracy, spacing — so the engine is already built
   and already validated to 0.08%.

## Honest limits

- **Q must be measured**, not assumed. `LUF_density` moves by 60% between Q = 100 and Q = 400, so an assumed Q
  gives a number that looks precise and is not. Q comes from the chamber's decay time: `Q = π f T₆₀ / ln 1000`.
- **One criterion among several**, named above. A test house will have its own; the engine should be able to
  run theirs as a parameter, and that is a small addition.
- **Rectangular, empty chamber.** Loading with a DUT raises the effective loss (lower Q) and lowers LUF — so
  this is a bound for the empty chamber, and the loaded case needs its own Q.

**Falsifier:** if a chamber's measured field uniformity becomes acceptable well below `LUF_density`, the
criterion is too strict and should be stated as such. If it stays unacceptable well above, the criterion is too
loose and chambers are being trusted too early. **Either way, one measurement of uniformity against frequency
settles it** — and that is the test worth proposing to a lab.
