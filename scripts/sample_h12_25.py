"""Sample h12=25 SUSY flux vacua with the memory-safe ``scipy`` solver.

Why scipy: the vmapped Newton solver (``solver="newton"``) OOMs its JIT trace at
~96 GB for h12=25 (see AGENTS.md "bigger systems"); the sequential ``scipy`` path
(``scipy.optimize.root`` with the analytical Jacobian) runs in ~1.5 GB instead.

Run on the JAXVacua host (studio-linux venv):

    /home/rob/cytools-venv/bin/python scripts/sample_h12_25.py 30 /home/rob/h12_25_vacua.json
    /home/rob/cytools-venv/bin/python scripts/sample_h12_25.py 100 /home/rob/h12_25_vacua.json 800  # 16k candidates, ~overnight

Args: <n_target> <output.json> [max_batches]. max_batches bounds the candidate budget
(n_batch=20 candidates per batch); it defaults to 500. The first smoke run used the
previous default (20 batches = 400 candidates) and found 0 critical points, so an
overnight run must raise it explicitly.

Saves a JSON file with one entry per critical point (flux, moduli, tau, V, log W0,
eigenvalues, is_susy, Nflux). Emits ``DONE`` on completion so the caller can poll.
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
    n_target = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    out = sys.argv[2] if len(sys.argv) > 2 else "/home/rob/h12_25_vacua.json"
    # max_batches bounds the total candidate budget (n_batch=20 x max_batches).
    # The old default (20 batches = 400 candidates) sampled 0 critical points in the
    # first h12=25 smoke run; an overnight run must raise this to see a real number.
    max_batches = int(sys.argv[3]) if len(sys.argv) > 3 else 500

    model = jvc.FluxVacuaFinder(h12=25, model_ID=1, model_type="KS", maximum_degree=0)
    print("BUILT", flush=True)

    t0 = time.time()
    vacua = model.sample_critical_points(
        Q=None, n_target=n_target, n_batch=20, max_batches=max_batches,
        isd_mode="ISD-", solver="scipy", verbose=True,
    )
    dt = time.time() - t0

    rows = [_plain(v) for v in vacua]
    with open(out, "w") as f:
        json.dump({"h12": 25, "n": len(rows), "elapsed_s": dt, "vacua": rows}, f)

    n_susy = sum(1 for r in rows if r.get("is_susy"))
    print(f"DONE {len(rows)} critical points ({n_susy} SUSY) in {dt:.1f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
