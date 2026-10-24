#!/usr/bin/env python3
"""Retrospective test: does drift-correction improve the model's historical match?

Fetches HadGEM3-GC31-LL surface temperature (tas) from CMIP6 (historical +
piControl), computes the drift-corrected historical warming, and compares it to
HadCRUT5 (the observed global temperature). The drift-correction is the field's
own: subtract the control-run temperature drift from the historical run.

Requires: xarray, zarr, dask, fsspec, aiohttp, numpy. Runs on the Mac (xarray
installed). Prints JSON to stdout.
"""
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

GS = "https://storage.googleapis.com/cmip6/"
TAS_HIST = (GS + "CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/historical/r1i1p1f3/"
            "Amon/tas/gn/v20190624/")
TAS_PIC = (GS + "CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/"
           "Amon/tas/gn/v20211103/")
HADCRUT5 = ("https://hadleyserver.metoffice.gov.uk/hadobs/hadcrut5/data/"
            "HadCRUT.5.1.0.0/analysis/diagnostics/"
            "HadCRUT.5.1.0.0.analysis.summary_series.global.annual.csv")


def global_mean_tas(url):
    """Area-weighted global-mean surface temperature -> (years, tas) annual series."""
    ds = xr.open_zarr(url, consolidated=True, decode_times=False, storage_options=_STORAGE)
    v = next(iter(ds.data_vars.values()))   # (time, lat, lon), K
    lat = np.asarray(ds["lat"].values, dtype=float)
    w = np.cos(np.deg2rad(lat))
    w = w / w.sum()
    wda = xr.DataArray(w, dims="lat")
    # time axis: Amon monthly; decode_times=False -> integer index; convert to year
    t = np.asarray(ds["time"].values)
    gm = np.asarray((v * wda).sum(dim="lat").mean(dim="lon").compute().values)  # (time,)
    return t, gm


def annual_mean(t, gm):
    yrs = np.asarray(t)
    # CMIP6 Amon time is days-since-1850-01-01; year = 1850 + days/365.2425
    year = 1850.0 + yrs / 365.2425
    yi = year.astype(int)
    ann = np.array([gm[yi == y].mean() for y in np.unique(yi)])
    return np.unique(yi), ann


def hadcrut5_annual():
    """HadCRUT5 global annual mean temperature anomaly, rebased to 1850-1900."""
    req = urllib.request.urlopen(HADCRUT5, timeout=120)
    rows = [l.split(",") for l in req.read().decode().splitlines()[1:]]
    year = [int(r[0]) for r in rows if r[0].strip().isdigit()]
    anom = [float(r[1]) for r in rows if r[0].strip().isdigit()]
    base = np.mean([a for y, a in zip(year, anom) if 1850 <= y <= 1900])
    return {"year": year, "anomaly": [a - base for a in anom]}


def main():
    print("fetching HadGEM3-GC31-LL tas (historical)...", file=sys.stderr, flush=True)
    th, gmh = global_mean_tas(TAS_HIST)
    print("fetching HadGEM3-GC31-LL tas (piControl)...", file=sys.stderr, flush=True)
    tp, gmp = global_mean_tas(TAS_PIC)

    hy, ha = annual_mean(th, gmh)
    py, pa = annual_mean(tp, gmp)

    # piControl drift: linear trend (K/yr) of the control-run temperature
    drift = np.polyfit(py - py[0], pa, 1)[0]   # K per year

    # historical baseline = 1850-1900 mean
    base_mask = (hy >= 1850) & (hy <= 1900)
    base = ha[base_mask].mean()
    hist_anom = ha - base

    # drift-corrected: remove the control-run spurious trend (rel 1850)
    corrected_anom = hist_anom - drift * (hy - 1850)

    # observed: HadCRUT5 1850-1900 baseline
    obs = hadcrut5_annual()

    # common years 1850-2014
    common = np.intersect1d(hy, obs["year"], assume_unique=True)
    h = hist_anom[np.isin(hy, common)]
    c = corrected_anom[np.isin(hy, common)]
    o = np.array([obs["anomaly"][list(obs["year"]).index(y)] for y in common])

    def rmse(a, b):
        return float(np.sqrt(np.mean((a - b) ** 2)))

    end = common[-1]
    out = {
        "model": "HadGEM3-GC31-LL",
        "piControl_tas_drift_K_per_century": round(drift * 100, 4),
        "period": f"{common[0]}-{end}",
        "end_warming_K": {
            "uncorrected": round(float(h[-1]), 3),
            "corrected": round(float(c[-1]), 3),
            "observed": round(float(o[-1]), 3),
        },
        "rmse_vs_hadcrut5_K": {
            "uncorrected": round(rmse(h, o), 3),
            "corrected": round(rmse(c, o), 3),
        },
        "verdict": (
            f"HadGEM3-GC31-LL piControl drifts {drift * 100:+.2f} K/century. "
            f"End-of-period warming: uncorrected {h[-1]:+.2f} K, corrected {c[-1]:+.2f} K, "
            f"observed {o[-1]:+.2f} K. RMSE vs HadCRUT5: uncorrected {rmse(h, o):.2f} K, "
            f"corrected {rmse(c, o):.2f} K."
        ),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
