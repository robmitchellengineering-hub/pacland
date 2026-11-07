# The χ = ±6 scan — where the three-generation manifolds actually are

**Query: the Kreuzer–Skarke database (quark.itp.tuwien.ac.at CGI) for CY threefolds with Euler
number χ = ±6, i.e. `N_gen = |χ|/2 = 3`.**

## Result

1. **The (1,4)/(4,1) manifold is NOT a toric hypersurface.** `h11=1&h12=4` → 0 and `h11=4&h12=1`
   → 0. The toric manifolds with `h¹¹ = 1` have `h²¹ ∈ {21, 101, 103, 145, 149}` — so the smallest
   `h¹¹ = 1` toric CY has `χ = 2(1−21) = −40`, not −6. The (1,4) manifold is a *free quotient*
   (non-toric), which is how it reaches `h¹¹ + h²¹ = 5`.

2. **The minimal |χ| in the toric list is 0, not 6.** Smallest Hodge pairs:
   `χ = 0` → `(14,14)` · `χ = ±2` → `(15,16)` · `χ = ±4` → `(14,16)` · `χ = ±6` → `(13,16)`.
   So the toric three-generation manifolds start at `h¹¹ + h²¹ = 29`, not 5.

3. **χ = ±6 is abundant in the toric list:** the query exceeds 200,000 results for *each* of
   `χ = +6` and `χ = −6` (the limit hit, not the total). Three generations is *easy* to get
   topologically; the hard part is the small Hodge numbers the SM wants.

## What this means for the unification

`N_gen = |χ|/2 = 3 ⟹ χ = ±6` is **confirmed** (200k+ toric manifolds), but the naive "minimal
manifold" picture was wrong in one instructive way:

- the *toric* three-generation CYs carry ≥ 29 moduli (`h¹¹ + h²¹`), far from minimal;
- the famous minimal three-generation manifold `(1,4)/(4,1)` is **not** in the toric list — it is
  a quotient, i.e. the SM-favorable small-Hodge-number case *forces* the non-toric (quotient /
  CICY) step.

So the unification sharpens to: **three generations is a topological label (`|χ|/2`) that is
abundant; the SM's *minimality* (few moduli, `h¹¹ = 4` for the gauge group) is what selects the
quotient construction over the bare toric hypersurface.** The label is forced; the moduli economy
is the harder constraint.

## Method

`curl "https://quark.itp.tuwien.ac.at/cgi-bin/cy/cydata.cgi?<query>&L=<limit>"` (the CYTools
`fetch_polytopes` remote backend was unusable — it builds a malformed host
`quark.itp.tuwien.ac.atcgi-bin`, missing the `/`). Queries: `chi=±6, ±4, ±2, 0`, `h11=1`,
`h11=1&h12=4`, `h11=4&h12=1`. Each verified by the returned `#NF` count or the `H:h11,h12 [χ]`
lines.
