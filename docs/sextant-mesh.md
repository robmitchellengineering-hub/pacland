# SEXTANT on the robmesh — parallel formalization

The constraint-first ToE is found faster by running SEXTANT on every mesh node at once: one
yes/no engine per machine, each attacking a different open hypothesis. This is the "parallel
formalization" that institutions would bring — built on our own mesh instead of rented.

## The instance

`scripts/sextant_bootstrap.sh` (POSIX) and `scripts/sextant_bootstrap.ps1` (Windows / PowerShell 5.1)
put a SEXTANT instance on a node: clone/pull pacland, install `numpy` + `stim` (quimb optional), run
the guard (`scripts/validate_sextant.py` — the falsifier suite + the exact CHSH control 2√2), and
report `catalog OK`. A node that reports OK has a working yes/no engine.

## The node map — who attacks what

| node | machine | SEXTANT role |
|---|---|---|
| `mac` | Rob's Mac (Intel) | the Lean proof arm — `cayley-even-n`, `t-count-boundary` (formalization is a thinking job) |
| `win-2` | Legion Go, Ryzen Z1 Extreme, AMD GPU + NPU | `npu-contraction` — benchmark the tensor-network contraction on the NPU vs CPU |
| `studio-linux2` | Ubuntu VM (win-2) | a SEXTANT instance + falsifier runs (Linux worker) |
| `pacland-rog` | GL752VW (Linux) | a SEXTANT instance (pacland-registered node; stalls intermittently) |
| `win` | laptop | `morpheos-rust-service` build (Rust) + a SEXTANT instance |

## The loop (same ratchet, now parallel)

1. bootstrap puts an engine on each node;
2. each node attacks one hypothesis (measurement = shell job, formalization = agent job);
3. each answer lands as a claim + a native falsifier in the registry;
4. re-run — the next (harder) question goes to the freed node.

## Status (2026-11-08)

- `scripts/sextant_bootstrap.sh` + `sextant_bootstrap.ps1` committed (branch `foundations/qf0-hinge-ledger`).
- First dispatch: bootstrap → `studio-linux2` (job `2026-11-08T1052Z-studio-linux2-sextant-bootstrap-…`).
- `mac` already runs SEXTANT (the proof arm lives here).
- Next: the `npu-contraction` benchmark → `win-2`, and the PowerShell bootstrap → `win`.
