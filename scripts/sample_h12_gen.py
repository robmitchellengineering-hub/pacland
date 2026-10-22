"""Sample SUSY flux vacua at a given h12 + model_ID (memory-safe scipy + ISD-).

Args: <h12> <model_ID> <n_target> <output.json> [max_batches]

Why this exists: the frontier measurement (2026-10-22) showed the sampler only
works for h12 <= 4. ``sample_h12.py`` hardcodes ``model_ID=1``, which is BROKEN
at h12=3 (missing Kaehler-cone hyperplanes -> the moduli sampler crashes in
``find_interior_points``), so a parametrised script that lets you pick a valid
``model_ID`` is the tool for the frontier.

The ISD matrix is ill-conditioned for h12 >= 5 (see docs/h12-25-sampling-wall.md),
so ``scipy``+``ISD-`` stalls there; keep max_batches explicit for the longer runs.
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
    model_ID = int(sys.argv[2])
    n_target = int(sys.argv[3])
    out = sys.argv[4]
    max_batches = int(sys.argv[5]) if len(sys.argv) > 5 else 300

    model = jvc.FluxVacuaFinder(h12=h12, model_ID=model_ID, model_type="KS", maximum_degree=0)
    print(f"BUILT h12={h12} model_ID={model_ID} Q={model.Q()}", flush=True)

    t0 = time.time()
    vacua = model.sample_critical_points(
        Q=None, n_target=n_target, n_batch=20, max_batches=max_batches,
        isd_mode="ISD-", solver="scipy", verbose=True,
    )
    dt = time.time() - t0

    rows = [_plain(v) for v in vacua]
    with open(out, "w") as f:
        json.dump({"h12": h12, "model_ID": model_ID, "n": len(rows), "elapsed_s": dt, "vacua": rows}, f)

    n_susy = sum(1 for r in rows if r.get("is_susy"))
    print(f"DONE {len(rows)} critical points ({n_susy} SUSY) in {dt:.1f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
