# The verified badge — the AI discipline (Valiant Verification)

The **ai** discipline is the **verified-badge lane**: the Valiant Verification SDK
applied to software, models, and AI systems. It is the same discipline the other fields
use — guards, mutation testing, an incident ledger, and the (ε,δ) certificate — aimed
at a repo or a model instead of a flux vacuum or a climate model. The SDK is the tool
(licensed, separate); this discipline is its home inside PACLAND, and the trust board
surfaces its results alongside every other field.

## What the badge is

A repo earns the badge when:

- its `valiant.json` **gates** pass by name — a missing gate, or an exit-0-with-no-output,
  is a fail (never a silent pass);
- every **guard** goes red under its seeded mutation (`valiant mutate`); a `survived`
  or `stale` mutation is a fail;
- the incident **ledger** names a RULE and a GUARD on every entry (`valiant ledger`).

"Done" then means "verified," machine-checked — which is the whole point of the
discipline and the property the badge sells.

## The adoptions (the real results)

The SDK deliberately does **not** validate itself (no dogfooding — a verifier that
verifies itself is circular). It is proven by driving real repos:

| repo | badge status |
|---|---|
| pacland (this repo) | unit-tests gate green (506 tests) |
| harness-mesh | 11 guards, 33 mutations, each proven to go red |
| morpheus-self-hosted | adopter (status not re-verified in this session) |

## Licensing — open spec, licensed SDK

The model is open-core:

- **Spec** — `github.com/robmitchellengineering-hub/valiant-verification` — **public,
  Apache-2.0.** The specification is open: what a gate, guard, and ledger are, and the
  portable contract a repo adopts.
- **SDK** — `github.com/robmitchellengineering-hub/valiant-verification-sdk` — **private,
  licensed.** It is the implementation layer (`valiant verify` / `mutate` / `ledger` /
  `status`) that enforces the spec. There is no open license file — access to the repo
  is the license.

The badge is minted by the licensed SDK; the spec is free for anyone to implement against.
That is the commercial seam: **the discipline is public, the machine that certifies it is
the product.**

## How it monetises

The badge is the product: a repo, a model, or a claim that carries it is *verifiably
what it says it is*. On the trust board this is one more discipline — a "clean" artifact
is a badge-earning repo, and a claim that fails its reality-guard (`"kind": "claim"`)
is a "broken" one. Certify, rank, or falsify: the three lanes from
`docs/expansion-map.md` all pass through here.
