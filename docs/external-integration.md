# Giving SEXTANT your data

SEXTANT ingests *other people's* domain data into the same registry its discovery engine searches, so
a project can hand over its structures, properties, evidence and mappings and the engine becomes useful
on that project's specific problem — and can synthesise across it and everything else.

Two ways in, both namespaced so nothing external can ever overwrite the internal catalog:

| path | command | what it ingests |
|---|---|---|
| JSON | `python -m pacland.tool ingest-external <file>.json` | structures · properties · evidence · mappings |
| Python | `python -m pacland.tool ingest-library <file>.py` | the above **plus executable falsifiers** the engine can run |

## The contribution schema

```json
{
  "source": "a-slug-identifying-the-project-or-person",
  "description": "one line on what this is",
  "domain": "geology",
  "structures": [
    {"id": "darcy-flow", "type": "parabolic-pde",
     "definition": "confined-aquifer flow S ∂h/∂t = ∇·(K ∇h)", "domain": "geology"}
  ],
  "properties": [
    {"id": "darcy-law", "statement": "q = −K ∇h", "tier": 1, "domain": "geology"}
  ],
  "evidence": [
    {"id": "pumping-test", "test": "tests/test_darcy.py", "dataset": "Theis 1935"}
  ],
  "mappings": [
    {"from": "darcy-flow", "to": "heat-equation",
     "mapping": "aquifer flow is the heat equation with diffusivity K/S",
     "kind_of_yield": "proof-technique"}
  ]
}
```

Every field is optional except `source`. The `tier` of a property is the epistemic tier
(1 established · 2 follows-from-established · 3 conjecture · 4 tested-numerically · 5 unknown).

## How it lands

- Every entry is namespaced **`ext:<source>:<id>`** — an external `darcy-flow` never collides with an
  internal `darcy-flow`.
- Each entry carries **provenance** `{produced_by: "external", source: <source>}` — the scientific
  record stays auditable.
- A mapping's `from`/`to` resolve against the contribution's **own** structures (auto-namespaced) while
  an **internal** structure id is left as-is, so external data links straight into the library the
  engine already knows (`darcy-flow → heat-equation` connects geology to physics).

## The Python path adds executable checks

A library module can also expose falsifiers the engine will actually RUN:

```python
SOURCE = "hydrogeology-project"
DOMAIN = "geology"
CONTRIBUTION = { ...same schema... }
FALSIFIERS = {
    "darcy-diffusivity-positive": lambda: (True, "K/S is positive"),
}
```

Each `FALSIFIERS` entry becomes a runner falsifier namespaced `ext:<source>:<name>` (callable by any
candidate that names it) and is recorded as an evidence claim. Worked example:
[`examples/external_library.py`](../examples/external_library.py).
