#!/usr/bin/env python3
"""Widen the CMIP6 conservation drift — recompute net-TOA energy drift for every
model that lacks Irving et al. 2021 data.

Runs on a Linux mesh node with xarray/zarr/dask. Discovers each model's piControl
rsdt/rsut/rlut zarr path from the pangeo-cmip6 catalog, computes the time-mean
net-TOA drift (rsdt - rsut - rlut), and writes JSON to stdout.

Requires: xarray, zarr, dask, fsspec, aiohttp, requests, numpy.
"""
import csv
import io
import json
import sys
import urllib.request

import numpy as np
import xarray as xr

try:
    import aiohttp
    _STORAGE = {"client_kwargs": {"timeout": aiohttp.ClientTimeout(total=1800)}}
except ImportError:
    _STORAGE = {}

CATALOG = "https://storage.googleapis.com/cmip6/pangeo-cmip6.csv"
CHUNK = 60          # months per zarr chunk (small enough for a slow network)
MAX_YEARS = 50      # the drift mean converges in ~50 years; no need for the full run


def _months():
    return MAX_YEARS * 12


def load_targets():
    """Models we score (ecs_K) minus the variants minus the ones with Irving data."""
    ecs = json.load(open("data/climate/cmip6_ecs.json"))
    drift = json.load(open("data/climate/cmip6_drift.json"))
    variants = set(ecs.get("approx_notes", {}))
    have = {m["model"] for m in drift["models"]}
    return [m for m in ecs["ecs_K"] if m not in variants and m not in have]


def catalog_paths():
    """(model, var) -> https zarr url, for piControl Amon rsdt/rsut/rlut r1i1p1f1."""
    req = urllib.request.urlopen(CATALOG, timeout=600)
    rows = csv.DictReader(io.TextIOWrapper(req, encoding="utf-8"))
    out = {}
    for r in rows:
        if (r["experiment_id"] == "piControl" and r["table_id"] == "Amon"
                and r["variable_id"] in ("rsdt", "rsut", "rlut")
                and r["member_id"] == "r1i1p1f1"):
            url = r["zstore"].replace("gs://cmip6/", "https://storage.googleapis.com/cmip6/")
            out.setdefault((r["source_id"], r["variable_id"]), url)
    return out


def global_mean_series(url):
    # Fetch the first 50 years in ONE slice (no re-chunk): matches the stored
    # chunks, so dask reads each chunk once instead of re-reading full chunks.
    ds = xr.open_zarr(url, consolidated=True, decode_times=False, storage_options=_STORAGE)
    v = next(iter(ds.data_vars.values())).isel(time=slice(0, _months()))
    lat = np.asarray(ds["lat"].values, dtype=float)
    w = np.cos(np.deg2rad(lat))
    w = w / w.sum()
    wda = xr.DataArray(w, dims="lat")
    return np.asarray((v * wda).sum(dim="lat").mean(dim="lon").compute().values)


def zonal_mean_series(url):
    """Time-mean zonal-mean flux -> (lat, flux): the SPATIAL pattern of the drift."""
    ds = xr.open_zarr(url, consolidated=True, decode_times=False, storage_options=_STORAGE)
    v = next(iter(ds.data_vars.values())).isel(time=slice(0, _months()))
    lat = np.asarray(ds["lat"].values, dtype=float)
    w = np.cos(np.deg2rad(lat))
    w = w / w.sum()
    wda = xr.DataArray(w, dims="lat")
    zonal = np.asarray((v * wda).mean(dim="lon").compute().values)  # (time, lat)
    return lat, zonal.mean(axis=0)                                   # (lat,)


def drift_of(model, paths):
    missing = [v for v in ("rsdt", "rsut", "rlut") if (model, v) not in paths]
    if missing:
        return None, f"missing {','.join(missing)}"
    net = global_mean_series(paths[(model, "rsdt")])
    net = net - global_mean_series(paths[(model, "rsut")]) - global_mean_series(paths[(model, "rlut")])
    yrs = np.arange(net.size) // 12
    ann = np.array([net[yrs == y].mean() for y in np.unique(yrs)])
    # zonal (spatial) drift
    lat, zrsdt = zonal_mean_series(paths[(model, "rsdt")])
    _, zrsut = zonal_mean_series(paths[(model, "rsut")])
    _, zrlut = zonal_mean_series(paths[(model, "rlut")])
    znet = zrsdt - zrsut - zrlut
    return {
        "mean_Wm2": float(ann.mean()),
        "zonal": {"lat": [round(float(x), 2) for x in lat],
                  "drift_Wm2": [round(float(x), 4) for x in znet]},
    }, None


def main():
    limit = None
    shard = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    if "--shard" in sys.argv:
        i = sys.argv.index("--shard")
        a, b = sys.argv[i + 1].split("/")
        shard = (int(a), int(b))
    targets = load_targets()
    if shard:
        shard_i, shard_n = shard
        targets = [m for j, m in enumerate(targets) if j % shard_n == shard_i]
    if limit:
        targets = targets[:limit]
    label = f"shard {shard[0]}/{shard[1]}" if shard else "without Irving drift"
    print(f"targets: {len(targets)} models ({label})", file=sys.stderr)
    paths = catalog_paths()
    print(f"catalog: {len(paths)} (model,var) rows", file=sys.stderr)
    out = []
    for m in targets:
        res, err = drift_of(m, paths)
        if err:
            out.append({"model": m, "status": "skipped", "reason": err})
            print(f"{m:24s} SKIP {err}", file=sys.stderr, flush=True)
        else:
            out.append({"model": m, "netTOA_drift_Wm2": round(res["mean_Wm2"], 4),
                        "zonal_drift_Wm2": res["zonal"], "status": "ok"})
            print(f"{m:24s} {res['mean_Wm2']:+.4f} W/m2 (zonal computed)", file=sys.stderr, flush=True)
    print(json.dumps({"source": "raw CMIP6 piControl zarr (pangeo-cmip6)",
                      "models": out}, indent=2))


if __name__ == "__main__":
    main()
