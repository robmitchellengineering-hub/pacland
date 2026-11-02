"""One row per access point: what the phone heard, and which APs deserve a look.

Design 38 says the product is the RESIDUAL between what the map predicts and what the phone measured. This is the first
half of that, and it works **without room positions**: across all the spot scans already on the hub, an AP that is heard
loudly in one place and not at all 3 m away is saying something about itself, and a steady AP is not.

    python3 scripts/ap_health.py [--root DIR] [--write]

WHAT THIS DOES **NOT** DO YET, and the table says so in its own footer: without a room geometry it cannot say "this AP
should be -55 here and you measured -72". That needs the ARCore dimensions and the arranged map (design 37). What it can do
today is rank the APs by how oddly they behave, which is what an installer would do by walking round with a laptop.

FALSIFIER, stated before the run: if the "suspect" verdicts are dominated by APs from the FURTHEST rooms, the metric is
measuring distance rather than health, and the verdict is noise. The table prints each AP's best and worst room so that can
be judged rather than argued.
"""
from __future__ import annotations

import glob
import json
import os
import statistics
import sys

# THE SPREAD METRIC FAILED ITS OWN FALSIFIER AND IS GONE. The first version called any AP with a 20 dB spread across spots
# "suspect" - and the first real run made Rob's own two working access points the top two suspects, at 37 dB and 33 dB,
# because a working AP in a house IS strong nearby and weak far away. The docstring said that outcome would mean the
# metric was measuring distance rather than health; it was, immediately, so the verdict was removed rather than tuned.
WEAK_EVERYWHERE_DBM = -80


def load(root: str) -> list[dict]:
    """Every scan on the hub, with its room label and every BSS it heard."""
    scans = []
    for d in sorted(glob.glob(os.path.join(root, "user-*"))):
        try:
            p = json.load(open(os.path.join(d, "stdout.txt")))
        except Exception:
            continue
        label = ((p.get("diagnostics") or {}).get("spot") or "").strip() or "unlabelled"
        bss = []
        for b in p.get("bss") or []:
            lvl = b.get("rssi_dbm", b.get("rssi"))
            if lvl is None:
                continue
            bss.append({
                "ssid": b.get("ssid") or "",
                "bssid": b.get("bssid") or "",
                "channel": b.get("channel"),
                "band": b.get("band"),
                "rssi": int(lvl),
            })
        if bss:
            scans.append({"spot": label, "bss": bss, "source": os.path.basename(d)})
    return scans


def table(scans: list[dict]) -> list[dict]:
    """One row per BSSID: sightings, levels, the spread, and where it was loudest and quietest."""
    by_bssid: dict[str, dict] = {}
    for scan in scans:
        # one sighting per scan, the strongest that scan heard of it
        best: dict[str, dict] = {}
        for b in scan["bss"]:
            key = b["bssid"] or f"{b['ssid']}|{b['channel']}"
            if key not in best or b["rssi"] > best[key]["rssi"]:
                best[key] = dict(b, spot=scan["spot"])
        for key, b in best.items():
            row = by_bssid.setdefault(key, {
                "bssid": b["bssid"], "ssid": b["ssid"], "band": b["band"], "channel": b["channel"],
                "levels": [], "spots": [],
            })
            row["levels"].append(b["rssi"])
            row["spots"].append((scan["spot"], b["rssi"]))

    out = []
    for row in by_bssid.values():
        levels = row["levels"]
        loudest = max(row["spots"], key=lambda s: s[1])
        quietest = min(row["spots"], key=lambda s: s[1])
        spread = max(levels) - min(levels)
        # ONLY what the data supports: coverage, range, and whether an AP is quiet everywhere.
        verdict, why = "heard", ""
        if max(levels) <= WEAK_EVERYWHERE_DBM:
            verdict, why = "weak everywhere", f"never above {max(levels)} dBm - far away, or failing, and one scan at " \
                                              f"its own position would tell which"
        elif len(levels) == 1:
            verdict, why = "one sighting", "heard at a single spot; no pattern to judge from"
        out.append({
            "ssid": row["ssid"] or "(hidden)", "bssid": row["bssid"],
            "band": row["band"], "channel": row["channel"],
            "sightings": len(levels),
            "best": max(levels), "median": int(statistics.median(levels)), "worst": min(levels),
            "spread": spread,
            "loudest": loudest, "quietest": quietest,
            "verdict": verdict, "why": why,
        })
    out.sort(key=lambda r: (r["verdict"] != "weak everywhere", -r["sightings"], -r["best"]))
    return out


def main(argv) -> int:
    root = os.path.expanduser("~/harness-mesh/runs/phone")
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    scans = load(root)
    if not scans:
        print("no spot scans on the hub yet")
        return 0
    rows = table(scans)
    print(f"{len(rows)} access points across {len(scans)} spot scans\n")
    print(f"{'verdict':<15}{'ssid':<24}{'ch':>4}{'seen':>6}{'best':>6}{'med':>6}{'worst':>7}{'spread':>8}  why")
    for r in rows:
        print(f"{r['verdict']:<15}{r['ssid'][:23]:<24}{str(r['channel']):>4}{r['sightings']:>6}"
              f"{r['best']:>6}{r['median']:>6}{r['worst']:>7}{r['spread']:>7}dB  {r['why']}")

    weak = [r for r in rows if r["verdict"] == "weak everywhere"]
    print(f"\n{len(weak)} of {len(rows)} APs are weak everywhere")
    print("\nNO FAULT VERDICTS HERE, DELIBERATELY. The first version called a large spread 'suspect' and made the two "
          "WORKING access points the top suspects - a spread is what distance looks like. A diagnosis needs the "
          "residual (predicted - measured), which needs the ARCore dimensions and the arranged map (design 37). Until "
          "then this table is an inventory: what was heard, how often, how loud, and which APs are quiet everywhere.")
    if "--write" in argv:
        out = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "ap-health.json")
        with open(out, "w") as fh:
            json.dump({"scans": len(scans), "aps": rows}, fh, indent=1)
        print(f"wrote {os.path.relpath(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
