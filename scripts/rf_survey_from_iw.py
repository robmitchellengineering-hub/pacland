"""Turn an access point into the survey instrument — no extra hardware.

An AP already measures everything the survey needs except the impulse response:

    iw dev wlan0 survey dump     ->  frequency, noise, channel active/busy/receive time
    iw dev wlan0 station dump    ->  per-client signal, bitrate, MCS/NSS in use
    iw list                      ->  what the radio can do (bandwidths, max streams)

`survey dump` gives the **noise floor** and the **duty cycle** directly: busy/active is the occupancy, and
noise is in dBm per frequency. `station dump` gives the **number of spatial streams actually in use**, which is
the number our engine predicts — so a mesh of a few APs is a real test of it, tonight, with nothing bought.

    iw dev wlan0 survey dump > survey.txt
    iw dev wlan0 station dump > stations.txt
    python3 scripts/rf_survey_from_iw.py survey.txt stations.txt

CAVEAT, stated because it decides how to read the answer: the AP reports the NSS it NEGOTIATED, which is capped
by the client's radio as well as by the channel. A 2x2 client shows 2 streams in a room that could carry 4. So
compare stream counts WITHIN one client across positions, never across clients, and never against the engine as
an absolute.
"""
import json
import re
import sys
from pathlib import Path


def parse_survey(text: str) -> list[dict]:
    """One record per frequency block from `iw dev <if> survey dump`."""
    out, cur = [], {}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Survey data from"):
            if cur:
                out.append(cur)
            cur = {"interface": line.split("from", 1)[1].strip() if "from" in line else ""}
            continue
        m = re.match(r"(frequency|noise|channel active time|channel busy time|channel receive time):\s*([\-\d.]+)", line)
        if m and cur is not None:
            key = m.group(1).replace(" ", "_")
            cur[key] = float(m.group(2))
    if cur:
        out.append(cur)
    return out


def parse_stations(text: str) -> list[dict]:
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"Station\s+([0-9a-f:]{17})", line.strip())
        if m:
            if cur:
                out.append(cur)
            cur = {"mac": m.group(1)}
            continue
        if cur is None:
            continue
        m = re.match(r"(signal|signal avg|tx bitrate|rx bitrate|tx failed|connected time):\s*(.+)", line.strip())
        if m:
            cur[m.group(1).replace(" ", "_")] = m.group(2).strip()
    if cur:
        out.append(cur)
    return out


def summarise(survey: list[dict], stations: list[dict]) -> dict:
    busy = []
    for r in survey:
        if "channel_active_time" in r and "channel_busy_time" in r and r["channel_active_time"] > 0:
            busy.append({"frequency": r.get("frequency"), "noise_dbm": r.get("noise"),
                         "occupancy": r["channel_busy_time"] / r["channel_active_time"]})
    return {
        "channels": sorted(busy, key=lambda c: c["occupancy"]),
        "quietest": min(busy, key=lambda c: c["occupancy"]) if busy else None,
        "busiest": max(busy, key=lambda c: c["occupancy"]) if busy else None,
        "stations": stations,
        "note": "occupancy = channel_busy_time / channel_active_time; noise is dBm as the AP reports it",
    }


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    survey = parse_survey(Path(argv[1]).read_text())
    stations = parse_stations(Path(argv[2]).read_text())
    out = summarise(survey, stations)
    print(json.dumps(out, indent=2))
    with open("survey.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote survey.json  ({len(survey)} frequency blocks, {len(stations)} stations)")
    if out["quietest"] and out["busiest"]:
        print(f"quietest channel {out['quietest']['frequency']:.0f} MHz at "
              f"{out['quietest']['occupancy']:.1%} busy; busiest "
              f"{out['busiest']['frequency']:.0f} MHz at {out['busiest']['occupancy']:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
