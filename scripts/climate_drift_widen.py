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

CATALOG = "https://storage.googleapis.com/cmip6/pangeo-cmip6.csv"


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
    ds = xr.open_zarr(url, consolidated=True, decode_times=False, chunks={"time": 120})
    v = next(iter(ds.data_vars.values()))
    lat = np.asarray(ds["lat"].values, dtype=float)
    w = np.cos(np.deg2rad(lat))
    w = w / w.sum()
    wda = xr.DataArray(w, dims="lat")
    parts = []
    for t0 in range(0, v.shape[0], 120):
        slab = v.isel(time=slice(t0, t0 + 120))
        parts.append(np.asarray((slab * wda).sum(dim="lat").mean(dim="lon").compute().values))
    return np.concatenate(parts)


def drift_of(model, paths):
    missing = [v for v in ("rsdt", "rsut", "rlut") if (model, v) not in paths]
    if missing:
        return None, f"missing {','.join(missing)}"
    net = global_mean_series(paths[(model, "rsdt")])
    net = net - global_mean_series(paths[(model, "rsut")]) - global_mean_series(paths[(model, "rlut")])
    yrs = np.arange(net.size) // 12
    ann = np.array([net[yrs == y].mean() for y in np.unique(yrs)])
    return float(ann.mean()), None


def main():
    targets = load_targets()
    print(f"targets: {len(targets)} models without Irving drift", file=sys.stderr)
    paths = catalog_paths()
    print(f"catalog: {len(paths)} (model,var) rows", file=sys.stderr)
    out = []
    for m in targets:
        mean, err = drift_of(m, paths)
        if err:
            out.append({"model": m, "status": "skipped", "reason": err})
            print(f"{m:24s} SKIP {err}", file=sys.stderr, flush=True)
        else:
            out.append({"model": m, "netTOA_drift_Wm2": round(mean, 4), "status": "ok"})
            print(f"{m:24s} {mean:+.4f} W/m2", file=sys.stderr, flush=True)
    print(json.dumps({"source": "raw CMIP6 piControl zarr (pangeo-cmip6)",
                      "models": out}, indent=2))


if __name__ == "__main__":
    main()
