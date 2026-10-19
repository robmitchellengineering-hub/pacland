"""Sample SUSY flux vacua at any h12 with the memory-safe ``scipy`` solver.

The vmapped Newton solver OOMs its JIT trace at ~96 GB for h12=25 (AGENTS.md);
the sequential ``scipy`` path runs in ~1.5 GB instead, so every truncation level
is now sampleable — just slowly.

Usage (on the JAXVacua host, studio-linux venv):

    /home/rob/cytools-venv/bin/python sample_h12.py <h12> <n_target> <output.json>

Emits ``DONE h12=.. n pts (.. SUSY)`` on completion.
"""
import json
import sys
import time

import jax

jax.config.update("jax_enable_x64", True)
import jaxvacua as jvc  # noqa: E402


def _plain(v):
    """Convert jax/numpy/complex values to plain JSON-serialisable Python."""
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    if hasattr(v, "tolist"):          # jax/numpy array
        return [_plain(x) for x in v.tolist()]
    if hasattr(v, "item"):            # jax/numpy scalar
        return _plain(v.item())
    if isinstance(v, complex):
        return [v.real, v.imag]
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float, str)):
        return v
    return str(v)


def main():
    h12 = int(sys.argv[1])
    n_target = int(sys.argv[2])
    out = sys.argv[3]

    model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=0)
    print(f"BUILT h12={h12}", flush=True)

    t0 = time.time()
    vacua = model.sample_critical_points(
        Q=None, n_target=n_target, n_batch=20,
        isd_mode="ISD-", solver="scipy", verbose=True,
    )
    dt = time.time() - t0

    rows = [_plain(v) for v in vacua]
    with open(out, "w") as f:
        json.dump({"h12": h12, "n": len(rows), "elapsed_s": dt, "vacua": rows}, f)

    n_susy = sum(1 for r in rows if r.get("is_susy"))
    print(f"DONE h12={h12} {len(rows)} pts ({n_susy} SUSY) in {dt:.1f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
