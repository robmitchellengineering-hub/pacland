# The finance sector, claim by claim

The aggregate deficit says a macro model's decision surface is validated over about four backcast
series and its forecast is extrapolation. That is true and it is **not actionable**, because nobody
acts on "the model". They act on a claim.

So this is the same arithmetic applied where decisions are actually made — eight claims a finance desk
or central bank acts on, each with its deficit, whether it is extrapolation, the reference it is
checked against, and what it is worth.

| claim | m | radius | region | verified reference | worth |
|---|---|---|---|---|---|
| The first published GDP estimate is biased upward | 5 | ±0.55 | measured | the Fed's own First/Second/Third/Most-Recent ladder, 239 quarters | **act with a hedge** |
| That bias cannot be traded | 5 | ±0.55 | measured | AR(1) of the revision is −0.07 | **act with a hedge** |
| GDPNow beats a no-change forecast, one quarter | 4 | ±0.61 | measured | no-change benchmark on the same vintage, 37 quarters | **act with a hedge** |
| GDPNow beats a no-change forecast at the settled number | 0 | vacuous | **extrapolation** | none — the evaluation targets the advance estimate | **do not act** |
| Our own recorded "first release" is the first release | 4 | ±0.61 | measured | the Fed's First Release against our ALFRED advance | **act with a hedge** |
| Smets–Wouters can be scored out of sample on its own observables | 0 | vacuous | **extrapolation** | none — the state is 41% observable | **do not act** |
| The GDP expenditure identity closes exactly | 4 | exact | measured | BEA identity, checked to 1e-16 of GDP | **act** |
| A 37-quarter revision measurement generalises to the whole record | 0 | vacuous | **extrapolation** | the 239-quarter ladder, which disagrees | **do not act** |

**8 claims: 1 act, 4 act with a hedge, 3 do not act; 3 are extrapolation.**

## The rule, stated once so it cannot be tuned per claim

```
outside the measured region   -> do not act, whatever m is
inside, m = 0                 -> do not act
inside, radius > 0.25         -> act with a hedge its size
inside, radius <= 0.25        -> act
definitional (an identity)    -> act, by construction; no radius applies
```

The radius is the Hoeffding bound on `m` independent constraints,
`sqrt(ln(1/δ) / 2m)` at `δ = 0.05`. At that budget, `radius ≤ 0.25` needs about **24 independent
constraints** — which is why almost nothing in finance clears the bar to plain "act", and why the
honest answer for most claims is *act with a hedge sized by the radius*.

## Why the extrapolation column matters more than the radius

A radius computed on a region a claim does not live in is **not an error bar for that claim**. Two of
the three "do not act" verdicts have `m = 0` for exactly that reason:

- **GDPNow against the settled number** — the evaluation targets the advance estimate. Skill against
  the first print is not skill against the number that survives revision.
- **Smets–Wouters out of sample** — the state is 41% observable from its own series, so there is no
  filter and therefore no forecast to score.
- **The 37-quarter revision figure** — the cross-source check catches our own data (2020Q2 is 7.00 pp
  out) and the 239-quarter ladder gives a different, more stable answer.

## Reproduce

```
python3 scripts/finance_claims.py
```

Every `m` is computed at call time from the module that owns the evidence — the release ladder, the
GDPNow vintages, the observability rank, the minimum-distance fit. A claim whose evidence changes
changes its verdict. Tests: `tests/test_econ_claims.py` (10 tests), including that the decision rule is
monotone and that a definitional identity is exempt from the radius.
