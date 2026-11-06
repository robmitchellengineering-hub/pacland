# k=2 integer orbits: the content and the elementary divisors

**Status:** framework verified (necessary conditions, 5000-sample scan); completeness rests on
the classical elementary-divisor / Wall transitivity (cited, not re-proven).

The $\mathbb{C}$ classification (`docs/k3-joint-invariant-ring.md`) is the *algebraically-closed*
case. The physical group is $\mathrm{Sp}(2h,\mathbb{Z})\times\mathrm{SL}(2,\mathbb{Z})$, and over
$\mathbb{Z}$ the pairings are **not** a complete orbit classifier — the content enters.

## k=1 (known, Wall)

Two flux pairs $(F,H)$ are in the same $\mathrm{Sp}(2h,\mathbb{Z})$-orbit iff
$N=F^\top J H$ and the content $d=\gcd(F,H)$ agree, with $d^2\mid N$. Finitely many orbits per
tadpole (one per $d$ with $d^2\mid N$).

## k=2 (the conjecture)

The $\mathrm{Sp}(2h,\mathbb{Z})$-orbit of $(F_1,H_1,F_2,H_2)$ is classified by

1. the **Gram matrix** $G$ — the $4\times4$ alternating matrix of the six pairings
   $P,Q,N_{11},N_{12},N_{21},N_{22}$, and
2. the **content** $d=\gcd(F_1,H_1,F_2,H_2)$ (the gcd of all $8h$ entries),

subject to

- $d^2 \mid G_{ij}$ for every pairing, and
- the elementary divisors of $G$ are $(d_1,d_2)$ with $d_1\mid d_2$ and $d_1 d_2=\operatorname{Pf}(G)$.

The $\mathrm{SL}(2,\mathbb{Z})$ factor then acts on $G$ (and fixes $d$), so the *joint* orbits are
the $\mathrm{SL}(2,\mathbb{Z})$-classes of these $(G,d)$.

## Verification

`scripts/k2_integer.py` scans 5000 random 4-tuples over $\mathbb{Z}^4$ and checks both
relationships: **0 failures** on $d^2\mid G$ and on $d_1 d_2=\operatorname{Pf}(G)$.

## Honest scope

The elementary-divisor statement is the classical classification of alternating forms over
$\mathbb{Z}$; the content condition is Wall's theorem at $k=1$. The contribution here is the
**conjectured complete invariant $(G,d)$ for $k=2$** and its necessary conditions — the
*sufficiency* (that equal $(G,d)$ forces the same $\mathrm{Sp}(2h,\mathbb{Z})$-orbit) is cited
from the classical transitivity, not re-proven here.
