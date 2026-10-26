#!/usr/bin/env python3
"""Build the climate figure page — charts drawn from the checked-in data.

Rob asked for "the climate graphs" on the climate card and there were none: the numbers
existed as JSON and as Python, and every claim was a sentence. This renders the four
claims as pictures, from the same modules that verify them, so a chart cannot disagree
with the text beside it.

    python3 scripts/build_climate_charts.py     # writes web/climate.html

Charts
  1  heat leak per model, against the measured Earth energy imbalance
  2  the three conservation ledgers, model by model
  3  how well each predictor actually did (the null included)
  4  the energy budget, and what closes it

`tests/test_climate_charts.py` fails if the committed page is stale.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.climate import baseline, cmip6_drift, energy_budget, model_deficit  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "climate.html"
DATA = ROOT / "data" / "climate"
EEI = 0.77                      # CERES 2005-2019, also in energy_budget.json
SECONDS_PER_YEAR = 3.155_76e7
EARTH_AREA_M2 = 5.100_72e14


def _wm2(j_per_year: float) -> float:
    """Convert a global energy rate in J/yr to W/m²."""
    return j_per_year / SECONDS_PER_YEAR / EARTH_AREA_M2


# ---------------------------------------------------------------------------------------
# a tiny bar chart. No chart library: an SVG a reader can scale and a reviewer can diff.
# ---------------------------------------------------------------------------------------
def bar_chart(rows, *, width=760, row_h=17, pad_left=150, pad_right=64, title="",
              unit="", reference=None, ref_label="", colour_pos="#c0392b", colour_neg="#1b4fd8"):
    """rows: [(label, value)] — horizontal bars, sorted by |value| by the caller."""
    height = row_h * len(rows) + 26
    span = max([abs(v) for _, v in rows] + ([abs(reference)] if reference else [0.0])) or 1.0
    scale = (width - pad_left - pad_right) / 2 / span        # half-width each side of zero
    mid = pad_left + (width - pad_left - pad_right) / 2
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{title}" class="chart">']
    out.append(f'<text x="0" y="12" class="ct">{title}</text>')
    rx = (mid + reference * scale) if reference is not None else None
    y = 22
    for label, value in rows:
        w = abs(value) * scale
        x = mid if value >= 0 else mid - w
        colour = colour_pos if value >= 0 else colour_neg
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 0.7):.1f}" height="{row_h - 5}" fill="{colour}" rx="1.5"/>')
        out.append(f'<text x="{pad_left - 6}" y="{y + row_h - 7}" text-anchor="end" class="lab">{label}</text>')
        tx = (mid + w + 5) if value >= 0 else (mid - w - 5)
        if reference is not None and abs(tx - rx) < 12:      # keep clear of the leader
            tx = rx + 12 if value >= 0 else rx - 12
        anchor = "start" if value >= 0 else "end"
        out.append(f'<text x="{tx:.1f}" y="{y + row_h - 7}" text-anchor="{anchor}" class="val">{value:+.2f}</text>')
        y += row_h
    out.append(f'<line x1="{mid}" y1="20" x2="{mid}" y2="{height - 4}" class="zero"/>')
    if reference is not None:
        rx = mid + reference * scale
        out.append(f'<line x1="{rx:.1f}" y1="20" x2="{rx:.1f}" y2="{height - 16}" '
                   'stroke="#ffffff" stroke-width="4.5" stroke-linecap="butt"/>')
        out.append(f'<line x1="{rx:.1f}" y1="20" x2="{rx:.1f}" y2="{height - 16}" class="ref"/>')
        out.append(f'<text x="{rx:.1f}" y="{height}" text-anchor="middle" class="reflab">{ref_label}</text>')
    out.append(f'<text x="{width}" y="{height}" text-anchor="end" class="unit">{unit}</text>')
    out.append("</svg>")
    return "\n".join(out)


def drift_rows():
    raw = json.loads((DATA / "cmip6_drift.json").read_text())["models"]
    rows = []
    for m in raw:
        # what the model claims to have taken in, minus what the ocean actually gained
        drift = _wm2(m["netTOA_J_per_yr"] - m["OHC_J_per_yr"])
        rows.append((m["model"], drift))
    rows.sort(key=lambda r: -abs(r[1]))
    return rows


def ledger_rows():
    raw = json.loads((DATA / "cmip6_drift.json").read_text())["models"]
    tol_mass_mm = 0.5
    kg_per_mm = json.loads((DATA / "cmip6_drift.json").read_text())["kg_per_mm_sl"]
    rows = []
    for m in raw:
        e = _wm2(m["netTOA_J_per_yr"] - m["OHC_J_per_yr"])
        mass_mm = abs(m["masso_kg_per_yr"]) / kg_per_mm
        salt = abs(m["soga_g_per_kg_per_yr"])
        failed = []
        if abs(e) > 0.1:
            failed.append("energy")
        if mass_mm > tol_mass_mm:
            failed.append("mass")
        if salt > 1e-3:
            failed.append("salt")
        rows.append((m["model"], failed))
    rows.sort(key=lambda r: (-len(r[1]), r[0]))
    return rows


def skill_rows():
    b = baseline.evaluate()
    label = {"persistence": "persistence (no change)", "trend": "the trend, continued (the ruler)"}
    rows = []
    for k, v in b["methods"].items():
        name = label.get(k, k.replace("emulator:", "emulator: "))
        rows.append((name, v["mae"]))
    rows.sort(key=lambda r: r[1])
    return rows


def budget_rows():
    c = energy_budget.closure()
    comps = json.loads((DATA / "energy_budget.json").read_text())["components_wm2"]
    rows = [(k.replace("_", " "), v) for k, v in comps.items()]
    return rows, c


def page() -> str:
    drift = drift_rows()
    ledgers = ledger_rows()
    skill = skill_rows()
    budget, closure = budget_rows()
    board = model_deficit.board_rows()
    summary = cmip6_drift.summary()

    n_fail = {k: sum(1 for _, f in ledgers if k in f) for k in ("energy", "mass", "salt")}

    parts = [
        '<!DOCTYPE html>',
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>Climate figures — PACLAND</title>',
        '<style>',
        '  :root{--ink:#15181f;--muted:#5a6072;--line:#e3e6ee;--accent:#1b4fd8;--bg:#fff}',
        '  *{box-sizing:border-box}',
        '  body{margin:0;background:var(--bg);color:var(--ink);',
        '       font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}',
        '  .wrap{max-width:860px;margin:0 auto;padding:1.6rem 1.2rem 3rem}',
        '  h1{font-size:1.55rem;margin:.2rem 0 .1rem}',
        '  .sub{color:var(--muted);margin:0 0 1.4rem}',
        '  h2{font-size:1rem;margin:2rem 0 .3rem}',
        '  p.note{color:var(--muted);font-size:.92rem;margin:.2rem 0 .8rem}',
        '  .chart{width:100%;height:auto;display:block;margin:.3rem 0 1rem}',
        '  .ct{font:600 12px system-ui;fill:var(--ink)}',
        '  .lab{font:11px ui-monospace,Menlo,monospace;fill:var(--muted)}',
        '  .val{font:11px ui-monospace,Menlo,monospace;fill:var(--ink)}',
        '  .zero{stroke:#b9c0cc;stroke-width:1}',
        '  .ref{stroke:#b45309;stroke-width:1.5;stroke-dasharray:4 3}',
        '  .reflab{font:10px system-ui;fill:#b45309}',
        '  .unit{font:10px system-ui;fill:var(--muted)}',
        '  .back{font-size:.9rem}',
        '  .back a{color:var(--accent);text-decoration:none}',
        '  table{border-collapse:collapse;width:100%;margin:.6rem 0 1rem;font-size:.9rem;table-layout:fixed}',
        '  col.c-model{width:200px} col.c-led{width:auto}',
        '  th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid var(--line)}',
        '  th{color:var(--accent);background:#f4f6fa}',
        '  .pass{color:#1e7b34;font-weight:600}.fail{color:#c0392b;font-weight:600}',
        '</style></head><body><div class="wrap">',
        '<p class="back"><a href="./index.html">← back to PACLAND</a></p>',
        '<h1>Climate, drawn from the data</h1>',
        '<p class="sub">Four pictures, each produced by the same code that verifies the claim. '
        'Nothing here is hand-drawn: regenerate with <code>scripts/build_climate_charts.py</code>.</p>',
    ]

    parts += [
        '<h2>1 · Heat leak, model by model</h2>',
        '<p class="note">What a model says it took in, minus what the ocean actually gained. '
        f'The orange line is the measured Earth energy imbalance, {EEI} W/m² — the signal these models '
        f'exist to predict. {summary["n_exceeding_eei"]} of {summary["n_models"]} leak faster than the real '
        'signal itself.</p>',
        bar_chart(drift, title="energy the model cannot account for", unit="W/m²",
                  reference=EEI, ref_label=f"measured imbalance {EEI}"),
        '<h2>2 · The three conservation ledgers</h2>',
        f'<p class="note">A model in a world with no forcing should be stationary. '
        f'{n_fail["energy"]} of {len(ledgers)} fail on energy, {n_fail["mass"]} on ocean mass, '
        f'{n_fail["salt"]} on salt. Salt is the ledger that only involves the ocean — it is conserved '
        'far better than the two that cross the air–sea boundary, which is how we know where the bug is.</p>',
        '<table><colgroup><col class="c-model"><col class="c-led"><col class="c-led"><col class="c-led"></colgroup>'
        '<thead><tr><th>model</th><th>energy</th><th>mass</th><th>salt</th></tr></thead><tbody>',
    ]
    for name, failed in ledgers:
        cells = "".join(
            f'<td class="{"fail" if k in failed else "pass"}">{"leaks" if k in failed else "holds"}</td>'
            for k in ("energy", "mass", "salt"))
        parts.append(f"<tr><td>{name}</td>{cells}</tr>")
    parts += ['</tbody></table>']

    parts += [
        '<h2>3 · How well each predictor actually did</h2>',
        '<p class="note">Mean absolute error on a real-time hindcast, lower is better. The trend — the '
        'warming so far, continued in a straight line — beats every emulator built from a published '
        'climate sensitivity. That is the whole finding of the null: the simplest guess is hard to beat.</p>',
        bar_chart([(n, v) for n, v in skill], title="mean absolute error (°C), lower is better",
                  unit="°C", pad_left=250),
        '<h2>4 · The energy budget, and what closes it</h2>',
        f'<p class="note">Every reservoir the Earth has, in W/m². The budget closes to '
        f'{closure["residual_full_wm2"]:.2f} W/m² with all of them — and misses by '
        f'{closure["residual_0_2000m_only_wm2"]:.2f} W/m² if only the upper ocean is counted. '
        'That gap is the argument for measuring the deep ocean.</p>',
        bar_chart(budget, title="2005–2020, global mean energy gain", unit="W/m²",
                  reference=EEI, ref_label=f"CERES {EEI}"),
        '<h2>5 · What each model is verified against</h2>',
        '<p class="note">A failed test costs an observable, not a fraction, so the count is the '
        'certificate. Radius = the error bound those observables buy at 95% confidence.</p>',
        '<table><thead><tr><th>model</th><th>verified against (m)</th><th>radius</th></tr></thead><tbody>',
    ]
    for r in board:
        parts.append(f"<tr><td>{r.model}</td><td>{r.m}</td><td>{r.radius:.2f}</td></tr>")
    parts += [
        '</tbody></table>',
        '<p class="back" style="margin-top:2rem">Sources: Irving et al. 2021 (drift), Loeb et al. 2021 '
        '(energy imbalance), Zelinka et al. 2020 (climate sensitivity), NASA GISTEMP v4 and NOAA GML '
        '(observations). Run <code>pacland climate</code> for the numbers behind these charts.</p>',
        '</div></body></html>',
    ]
    return "\n".join(parts) + "\n"


def main() -> int:
    html = page()
    OUT.write_text(html)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
