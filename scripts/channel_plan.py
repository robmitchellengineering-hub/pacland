"""Which channel should the access point actually be on? Answered from the scans, not from folklore.

The phone's scans give every BSS it heard, with frequency and level. This turns that into an interference budget per
candidate channel: for each channel, sum the power of every OTHER network whose occupied spectrum overlaps it, and
report the margin against the house's own network.

    python3 scripts/channel_plan.py [runs/phone]

FALSIFIER, stated before the run: if the recommended channel is anywhere within 6 dB of the current one, the
difference is inside the fading the same instrument measured (16 dB at a fixed spot), and the recommendation is noise.
The tool says so rather than presenting a 3 dB difference as a finding.
"""
from __future__ import annotations

import glob
import json
import math
import os
import pathlib
import sys

BANDS = {
    "2.4 GHz": {"channels": [(c, 2407 + 5 * c) for c in range(1, 14)], "width": 20},
    "5 GHz": {"channels": [(c, 5000 + 5 * c) for c in [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112,
                                                       116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165]],
              "width": 20},
}
OURS = ("Pretty fly", "Forest", "Telstra3696")


def load(root):
    seen = {}
    for d in glob.glob(os.path.join(root, "user-*")):
        try:
            p = json.load(open(os.path.join(d, "stdout.txt")))
        except Exception:
            continue
        for b in p.get("bss") or []:
            k = (b.get("bssid"), b.get("frequency_mhz"))
            lvl = b.get("rssi_dbm", b.get("rssi", -127))
            if k not in seen or lvl > seen[k]["rssi"]:
                seen[k] = {"ssid": b.get("ssid") or "", "freq": b.get("frequency_mhz"),
                           "ch": b.get("channel"), "band": b.get("band"), "rssi": lvl}
    return list(seen.values())


def is_ours(b):
    return any(o.lower() in b["ssid"].lower() for o in OURS)


def interference(bss, band, centre_mhz, width_mhz):
    """Sum of interfering power (linear) from other networks overlapping this channel."""
    total = 0.0
    for b in bss:
        if b["band"] != band or is_ours(b):
            continue
        if abs(b["freq"] - centre_mhz) <= (width_mhz / 2 + 10):     # adjacent-channel overlap allowance
            total += 10 ** (b["rssi"] / 10.0)
    return total


def main(argv) -> int:
    root = argv[1] if len(argv) > 1 else os.path.expanduser("~/harness-mesh/runs/phone")
    bss = load(root)
    print(f"{len(bss)} networks seen across {len(glob.glob(os.path.join(root, 'user-*')))} scans\n")

    for band, spec in BANDS.items():
        rows, unobserved = [], []
        for ch, centre in spec["channels"]:
            p = interference(bss, band, centre, spec["width"])
            anyseen = any(b["band"] == band and abs(b["freq"] - centre) <= (spec["width"] / 2 + 10) for b in bss)
            if not anyseen:
                unobserved.append(ch)
                continue
            rows.append((ch, 10 * math.log10(p) if p > 0 else -120.0))
        rows.sort(key=lambda r: r[1])
        ours = [b for b in bss if b["band"] == band and is_ours(b)]
        ours_ch = ours[0]["ch"] if ours else None
        ours_lvl = max((b["rssi"] for b in ours), default=None)
        print(f"== {band} ==   our network: ch {ours_ch} at {ours_lvl} dBm" if ours_ch else f"== {band} ==")
        print(f"{'rank':<5}{'ch':>4}{'interference':>14}{'margin vs ours':>17}   (observed channels only)")
        for i, (ch, lvl) in enumerate(rows[:5], 1):
            margin = (ours_lvl - lvl) if ours_lvl is not None else float("nan")
            print(f"{i:<5}{ch:>4}{lvl:>12.1f} dB{ours_lvl - lvl:>15.1f} dB")
        if unobserved:
            print(f"  no network was observed on ch {', '.join(str(c) for c in unobserved[:8])}"
                  f"{' ...' if len(unobserved) > 8 else ''} - unverified, not necessarily clear")
        best = rows[0]
        if ours_ch is not None:
            cur = next((lvl for ch, lvl in rows if ch == ours_ch), None)
            if cur is not None:
                gain = cur - best[1]
                verdict = "RECOMMEND" if gain >= 6.0 else "not a finding (inside the measured fading)"
                print(f"  -> best ch {best[0]} would cut interference by {gain:.1f} dB: {verdict}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
