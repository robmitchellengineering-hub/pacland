# Using PACLAND

PACLAND is a **verification discipline for string-theory computation** — a
toolset, not a physics solver. You feed it flux-vacua data (or a candidate
computation), and it returns certified answers about what you can and cannot claim:
is this verifiable, is this structured, what constraints eliminate it, what is
uncomputable.

## Install

```sh
git clone https://github.com/robmitchellengineering-hub/pacland
cd pacland
pip install -e .          # installs the `pacland` command (pure stdlib, no deps)
```

Or run without installing (the library is pure stdlib):

```sh
PYTHONPATH=src python3 -m pacland.cli <subcommand>
```

## The four commands

### `pacland limits` — the boundary map

Prints the cartography of the computable/uncomputable: for each open question, which
sense of "uncomputable" applies (intractable / unmeasurable / underdetermined) and
what *remains* computable.

```sh
pacland limits
```

### `pacland certify "<question>"` — certify a boundary

```sh
pacland certify "flux landscape over W0"
# [intractable] ... W0 is log-uniform -> not learnable -> not evolvable ...
```

### `pacland mine <data.json>` — structure mining

Given flux-vacua data, classifies each observable as *structured* (carries geometric
information) or *random* (uniform), using non-linear mutual information plus a
self-validated quadratic learnability test.

```sh
pacland mine data/vacua_sample.json
```

### `pacland deficit` — the Mitchell Verification Deficit

Computes `m` (validated oracle outputs) and the resulting certificate radius.

```sh
pacland deficit
pacland deficit --observables my-observables.json --delta 0.025
```

### `pacland constrain <data.json>` — constraint elimination

Measures what fraction of vacua each physically-motivated constraint eliminates, and
tests the uniformity of |W₀|² (the Denef–Douglas prediction).

```sh
pacland constrain data/vacua_sample.json
```

## Input data format

`mine` and `constrain` accept either of:

```json
{ "model_name": { "flux": [[f1, f2, ...], ...],
                  "log_W0": [...], "log_gs": [...] } }
```

or the richer per-vacuum list form (see `data/vacua_observables.json`). Flux vectors
are integer flux quanta; observables are in log space.

## The library API

Everything the CLI does is importable:

```python
from pacland.certificate import two_level_certificate   # the (ε,δ) certificate
from pacland.structure import classify_observable       # structured vs random
from pacland.constraints import elimination_certificate # constraint elimination
from pacland.limits import boundary_map                 # the boundary map
from pacland.oracle import Oracle, CyToolsAdapter, JaxVacuaAdapter  # real tools
```

## Honest framing (read this before you use it)

- The **results depend on the sampling measure.** A uniform-in-a-box sample gives
  different numbers than the natural (ISD) measure. `constrain` reports whatever the
  data says; it is your job to know how the data was sampled. (Our natural-measure
  sample gives P(|W₀|<1) ≈ 43%; a biased box sample gives ≈ 5%.)
- `mine`'s "random" verdict only rules out structure *detectable by the tool*; it is
  self-validated on a known-structured control (the tadpole), but it cannot see
  structure beyond quadratic in the flux.
- PACLAND does **not** compute the vacuum or the measure. It tells you what can be
  verified, measured, and eliminated — and maps what cannot.
