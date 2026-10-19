# Research fan-out — the reusable "compare notes" tool

Parallel independent passes are how this project avoids single-angle overreach (the
same discipline as the Rule of Three, applied to *ideas* rather than measurements).
This doc is the recipe; the first run is `research/sm-conjecture-fanout.js`.

## The pattern

1. **Pick a frontier question** with a sharp yes/no edge.
2. **Choose N independent attack angles** (different UV completions, different
   formalisms, different sectors). N ≤ 6 (the concurrent-agent ceiling).
3. **Fan out** — one agent per angle, each returning a *structured* verdict, not prose.
4. **Compare notes** — diff the verdicts. The spread (some falsify, some confirm, some
   unknown) *is* the result: it tells you where your claim is too strong, too weak, or
   genuinely open.

## The structured schema (what every agent returns)

| field | meaning |
|---|---|
| `claim` | the angle's main finding, 1–3 sentences |
| `evidence` | specific facts with source URLs |
| `confidence` | `low` / `medium` / `high` |
| `falsifies_conjecture` | `true` / `false` / `unknown` — does this angle break the claim? |
| `open_questions` | what's left unresolved |
| `next_step` | the concrete action if this angle is pursued |

The `falsifies_conjecture` field is the key: a real fan-out *must* be allowed to return
`true`. A fan-out that can only confirm is a rubber stamp.

## How to run it

Call the **`workflow` tool** with the script in `research/sm-conjecture-fanout.js`:

```
meta    = { name: "<question>-fanout",
            description: "<one line>",
            phases: [{ title: "research", detail: "<one line>" }] }
script  = <the contents of research/sm-conjecture-fanout.js>
```

It runs in the foreground and returns the aggregated array of structured verdicts. To
*adapt* it to a new question, edit only `directions` (the label + self-contained prompt
per angle) — the `parallel(...)` fan-out and the schema stay fixed.

For **live orchestration** (steer as results land, stay free to chat), use six
background `subagent` calls instead, one per angle, and synthesize when they settle.

## How to synthesize (the compare-notes step)

After the fan-out returns, write the synthesis around three questions:

1. **The pivot.** Is there one word or clause whose two readings split the `true` from
   the `false` verdicts? That pivot is usually the real finding (in the first run it
   was "unpredicable" = *no invariant relates them* vs *no unique value is derived*).
2. **The refined claim.** Restate the conjecture so it survives the `true` verdicts
   without overclaiming. Record the refinement — it is the actual product.
3. **The named next steps.** Collect the `next_step` fields that are concrete and
   checkable; they become the next fan-out's directions or the next build's targets.

A fan-out that *only* confirms your claim was not worth running. The value is in the
spread.
