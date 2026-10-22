# Economics accounting closure — the real-data run (recipe step 6)

Status: **computed from FRED, 2026-10-22** — `scripts/economics_accounting_closure.py`.
The economics Rule of Three, run on actual US national-accounts data the way
`docs/climate-cmip6-drift.md` ran climate's three conservation ledgers on CMIP6.

## The headline, in one sentence

> **On real US data the two *measured* accounting ledgers leak — income and expenditure
> differ by 0.58% of GDP ($189.5B, the statistical discrepancy), and debt grew $236.9B
> more than the deficit (13.3% of the deficit, the stock-flow adjustment) — while the
> *definitional* ledger (sectoral balances) closes exactly.**

## The three ledgers, measured

| ledger | identity | measured residual | verdict |
|---|---|---|---|
| **circular flow** | income ≡ expenditure | GDI − GDP = **+$189.5B** = **0.58%** of GDP (2026 Q2) | **leaks** |
| **sectoral balances** | (S−I)+(T−G)+(M−X) = 0 | private +$2,020.7B + gov −$1,774.7B + foreign −$246.0B = **0** | **closes** (by definition) |
| **stock-flow** | Δ(debt) = deficit | Δdebt $2,011.6B − deficit $1,774.7B = **+$236.9B** = **13.3%** of deficit (FY2025) | **leaks** |

The pattern is the economics twin of climate's conservation drift: the ledgers that
close *by construction* (sectoral balances — double-entry) stay exact, while the ledgers
that close *by measurement* (GDP-vs-GDI from two independent surveys; debt-vs-deficit on
two different accounting bases) leak. Climate found the atmosphere-coupled ledgers leak
and the purely-ocean ledger (salt) closes; economics finds the measured ledgers leak and
the definitional ledger closes.

## Why each leaks (the root cause, not just the number)

- **Circular flow (0.58%).** GDP and GDI are built from *different* source data — GDP from
  the expenditure side, GDI from the income side. Their gap is BEA's own "statistical
  discrepancy": a genuine measurement gap between two estimates of the same aggregate, not
  a model error.
- **Stock-flow (13.3%).** The deficit (FYFSD) is a *cash-basis budget* number; the debt
  (FYGFDPUN) is *accrual-basis debt held by the public*. The stock-flow adjustment captures
  everything the deficit misses — accrued interest, Treasury/Federal-Reserve operations,
  asset purchases — so Δdebt ≠ deficit. This is the well-known "stock-flow adjustment" the
  SFC literature (Godley–Lavoie) insists a model must track, and the gap is its size.

## What this means for the discipline

The accounting identities are the *oracle* (always-true by construction), but a real
national-accounts dataset does **not** close them to zero — it closes them to 0.6% and
13%. So a model or a forecast that is "consistent with the accounting identities" is
compatible with a ~$237B drift in the stock-flow ledger alone. The guard-suite
(`src/pacland/economics/guards.py`) makes those gaps *measured* rather than assumed.

## Source

FRED (St. Louis Fed), downloaded 2026-10-22: `GDP`, `GDI`, `IEABC` (quarterly);
`FYFSD`, `FYGFDPUN` (fiscal year / quarterly end-of-period). Values embedded in
`scripts/economics_accounting_closure.py`.

## Reproduce

```
python3 scripts/economics_accounting_closure.py
```
