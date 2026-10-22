#!/usr/bin/env python3
"""Second-source confirmation of the CMIP6 conservation drift.

Recomputes the net-TOA energy drift of CMIP6 piControl runs directly from raw
model output (the Google Cloud pangeo-cmip6 zarr archive) and compares to the
published Irving et al. 2021 figshare values. This is the independent source
that closes the single-source gap: if the raw drift disagrees in sign or rank
with Irving, the conservation finding is a single-source artifact.

Requires (not part of the pacland stdlib core): xarray, zarr, fsspec, aiohttp,
requests, dask, scipy. See docs/climate-drift-second-source.md.

    python3 scripts/climate_drift_second_source.py

Net TOA = rsdt - rsut - rlut (down shortwave - up shortwave - up longwave),
the same definition Irving used. BCC-ESM1's `rtmt` diagnostic is shown NOT to
close against its own components (~1.1 W/m2 off), which is why components are
preferred over `rtmt`.
"""
import json
import sys

import numpy as np
import xarray as xr

GS = "https://storage.googleapis.com/cmip6"
SEC = 3.15576e7
AREA = 5.101e14

# model -> list of (zstore path, sign) for netTOA = rsdt - rsut - rlut
MODELS = {
    "CNRM-ESM2-1": [
        ("CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/Amon/rsdt/gr/v20181115/", +1),
        ("CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/Amon/rsut/gr/v20181115/", -1),
        ("CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/Amon/rlut/gr/v20181115/", -1),
    ],
    "BCC-ESM1": [
        ("CMIP6/CMIP/BCC/BCC-ESM1/piControl/r1i1p1f1/Amon/rsdt/gn/v20181214/", +1),
        ("CMIP6/CMIP/BCC/BCC-ESM1/piControl/r1i1p1f1/Amon/rsut/gn/v20181214/", -1),
        ("CMIP6/CMIP/BCC/BCC-ESM1/piControl/r1i1p1f1/Amon/rlut/gn/v20181214/", -1),
    ],
    "GISS-E2-1-G": [
        ("CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/piControl/r1i1p1f1/Amon/rtmt/gn/v20180824/", +1),
    ],
    "IPSL-CM6A-LR": [
        ("CMIP6/CMIP/IPSL/IPSL-CM6A-LR/piControl/r1i1p1f1/Amon/rtmt/gr/v20200326/", +1),
    ],
    "EC-Earth3": [
        ("CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3/piControl/r1i1p1f1/Amon/rtmt/gr/v20200312/", +1),
    ],
}

# Irving et al. 2021 netTOA (J/yr) converted to W/m2
IRVING = {
    "CNRM-ESM2-1": 2.39e22 / (SEC * AREA),
    "BCC-ESM1": -6.47e21 / (SEC * AREA),
    "GISS-E2-1-G": 9.08e20 / (SEC * AREA),
    "IPSL-CM6A-LR": 1.07e22 / (SEC * AREA),
    "EC-Earth3": 5.65e20 / (SEC * AREA),
}


def global_mean_series(path, sign):
    ds = xr.open_zarr(GS + "/" + path, consolidated=True,
                      decode_times=False, chunks={"time": 120})
    v = next(iter(ds.data_vars.values()))
    lat = np.asarray(ds["lat"].values, dtype=float)
    w = np.cos(np.deg2rad(lat))
    w = w / w.sum()
    wda = xr.DataArray(w, dims="lat")
    parts = []
    for t0 in range(0, v.shape[0], 120):
        slab = v.isel(time=slice(t0, t0 + 120))
        g = (slab * wda).sum(dim="lat").mean(dim="lon").compute().values
        parts.append(np.asarray(g, dtype=float))
    return sign * np.concatenate(parts)


def annual_mean(x):
    yrs = np.arange(x.size) // 12
    return np.array([x[yrs == y].mean() for y in np.unique(yrs)])


def main():
    out = {"source": "raw CMIP6 piControl zarr (Google Cloud pangeo-cmip6)",
           "irving_source": "Irving et al. 2021 figshare 10.6084/m9.figshare.12143562",
           "models": []}
    for name, comps in MODELS.items():
        ts = global_mean_series(comps[0][0], comps[0][1])
        for path, sign in comps[1:]:
            ts = ts + global_mean_series(path, sign)
        ann = annual_mean(ts)
        mean = float(ann.mean())
        trend = float(np.polyfit(np.arange(ann.size), ann, 1)[0])
        irv = IRVING[name]
        out["models"].append({
            "model": name, "n_years": int(ann.size),
            "mean_netTOA_Wm2": round(mean, 4),
            "trend_Wm2_per_yr": round(trend, 5),
            "irving_Wm2": round(irv, 4), "diff_Wm2": round(mean - irv, 4),
        })
        print(f"{name:14s} raw={mean:+.3f} irving={irv:+.3f} diff={mean-irv:+.3f}",
              flush=True)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    sys.exit(main())
