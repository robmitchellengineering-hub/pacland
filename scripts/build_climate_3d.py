#!/usr/bin/env python3
"""Build the 3D view of the climate verification.

The first version of this page lived on a branch that never merged, so the site never had
it. It was also three scenes side by side in one 680px box — about 380px each, with the
only labels on hover. This rebuilds it from the current data and gives each scene a full
row of its own, a real heading, and a caption that says what to look for.

    python3 scripts/build_climate_3d.py     # writes web/climate-3d.html

Drawn with Plotly because 3D needs WebGL — vendored at web/vendor/plotly-2.35.2.min.js, not
pulled from a CDN: a figure that needs someone else's server is a figure that breaks. When the
library is missing the page says so and links the 2D figures, which need no JavaScript at all. `tests/test_climate_charts.py` checks the committed page is current.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.climate import cmip6_drift, energy_budget  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "climate-3d.html"
DATA = ROOT / "data" / "climate"
EEI = 0.77
SECONDS_PER_YEAR = 3.155_76e7
EARTH_AREA_M2 = 5.100_72e14


def _wm2(j_per_year: float) -> float:
    return j_per_year / SECONDS_PER_YEAR / EARTH_AREA_M2


def _models():
    raw = json.loads((DATA / "cmip6_drift.json").read_text())
    kg_per_mm = raw["kg_per_mm_sl"]
    rows = []
    for m in raw["models"]:
        energy = _wm2(m["netTOA_J_per_yr"] - m["OHC_J_per_yr"])
        mass_mm = m["masso_kg_per_yr"] / kg_per_mm
        salt = m["soga_g_per_kg_per_yr"]
        leaks = abs(energy) > 0.1 or abs(mass_mm) > 0.5 or abs(salt) > 1e-3
        rows.append({"model": m["model"], "energy": round(energy, 3),
                     "mass": round(mass_mm, 3), "salt": round(salt * 1e6, 2), "leaks": leaks})
    return rows


def _ecs():
    d = json.loads((DATA / "cmip6_ecs.json").read_text())
    return d["ecs_K"], d["erf2x_Wm2"], d["likely_range_K"]


def _trace_scatter3d(rows, *, name, colour, key_energy="energy", key_mass="mass", key_salt="salt", extra=""):
    return {
        "type": "scatter3d", "mode": "markers", "name": name,
        "text": [r["model"] for r in rows],
        "x": [r[key_energy] for r in rows],
        "y": [r[key_mass] for r in rows],
        "z": [r[key_salt] for r in rows],
        "marker": {"size": 9, "color": colour, "opacity": 0.95,
                   "line": {"width": 1.2, "color": "#ffffff"}},
        "hovertemplate": "%{text}<br>energy %{x:.2f} W/m²<br>mass %{y:.2f} mm/yr"
                          "<br>salt %{z:.1f} µg/kg" + extra + "<extra></extra>",
    }


def scenes() -> list[dict]:
    models = _models()
    leaks = [m for m in models if m["leaks"]]
    keeps = [m for m in models if not m["leaks"]]
    ecs, erf, likely = _ecs()

    # panel 2: only models that have a conservation test can pass the gate — a model with
    # no drift data has not been tested, which is not the same as passing.
    drift_by = {m["model"]: m for m in models}
    trust, fails = [], []
    for name, k in ecs.items():
        d = drift_by.get(name)
        if d is None:
            continue
        point = {"model": name, "ecs": k, "erf": erf.get(name, 0.0), "drift": d["energy"]}
        within = (likely[0] <= k <= likely[1] and 3.3 <= point["erf"] <= 4.1
                  and not d["leaks"] and abs(d["energy"]) <= 0.1)
        (trust if within else fails).append(point)

    return [
        {
            "id": "leak",
            "title": "1 · The leak",
            "caption": "Axes are the three conservation ledgers, each in its own units. A model in a "
                       "world with no forcing should sit at the origin. Red dots are the ones that "
                       "drift away — 14 of 19; green ones hold.",
            "traces": [
                _trace_scatter3d(leaks, name="leaks", colour="#c0392b"),
                _trace_scatter3d(keeps, name="conserves", colour="#1e7b34"),
                {"type": "scatter3d", "mode": "markers", "name": "conserved (0,0,0)", "showlegend": False,
                 "x": [0], "y": [0], "z": [0],
                 "marker": {"size": 6, "color": "#15181f", "symbol": "diamond"}},
            ],
            "axes": ["energy drift (W/m²)", "ocean mass (mm/yr)", "salt drift (µg/kg/yr)"],
        },
        {
            "id": "gate",
            "title": "2 · The trust gate",
            "caption": "Climate sensitivity against heat trapping, with conservation drift as the "
                       "third axis — the 19 models that have a conservation test, since a model with no "
                       "drift data has not been tested. The dashed box is where a model has to land: "
                       "plausible sensitivity is not enough, it has to survive all three axes.",
            "traces": [
                {"type": "scatter3d", "mode": "markers", "name": "passes all three",
                 "text": [p["model"] for p in trust],
                 "x": [p["ecs"] for p in trust], "y": [p["erf"] for p in trust], "z": [p["drift"] for p in trust],
                 "marker": {"size": 7, "color": "#1e7b34"},
                 "hovertemplate": "%{text}<br>ECS %{x:.2f} K<br>ERF2x %{y:.2f} W/m²"
                                   "<br>energy drift %{z:.2f} W/m²<extra></extra>"},
                {"type": "scatter3d", "mode": "markers", "name": "fails at least one",
                 "text": [p["model"] for p in fails],
                 "x": [p["ecs"] for p in fails], "y": [p["erf"] for p in fails], "z": [p["drift"] for p in fails],
                 "marker": {"size": 5, "color": "#8a93a6", "opacity": 0.75},
                 "hovertemplate": "%{text}<br>ECS %{x:.2f} K<br>ERF2x %{y:.2f} W/m²"
                                   "<br>energy drift %{z:.2f} W/m²<extra></extra>"},
                {"type": "scatter3d", "mode": "lines", "name": "the gate", "showlegend": False,
                 "x": [likely[0], likely[1], likely[1], likely[0], likely[0]],
                 "y": [3.3, 3.3, 4.1, 4.1, 3.3], "z": [0, 0, 0, 0, 0],
                 "line": {"color": "#b45309", "width": 4, "dash": "dash"}},
            ],
            "axes": ["ECS (K)", "ERF2x (W/m²)", "energy drift (W/m²)"],
        },
        {
            "id": "fix",
            "title": "3 · The fix",
            "caption": "Drift correction subtracts each model's own leak: every red dot returns to the "
                       "origin. That is what a repaired model looks like — and it is why the repair is "
                       "computable instead of a research programme.",
            "traces": [
                _trace_scatter3d(leaks, name="before (leaking)", colour="#c0392b"),
                {"type": "scatter3d", "mode": "markers", "name": "after (corrected)",
                 "text": [m["model"] for m in leaks],
                 "x": [0] * len(leaks), "y": [0] * len(leaks), "z": [0] * len(leaks),
                 "marker": {"size": 5, "color": "#1e7b34"}},
            ] + [
                {"type": "scatter3d", "mode": "lines", "showlegend": False, "hoverinfo": "skip",
                 "x": [m["energy"], 0], "y": [m["mass"], 0], "z": [m["salt"], 0],
                 "line": {"color": "#b9c0cc", "width": 2}}
                for m in leaks
            ],
            "axes": ["energy drift (W/m²)", "ocean mass (mm/yr)", "salt drift (µg/kg/yr)"],
        },
    ]


def _scene_json(scene: dict) -> str:
    layout = {
        "margin": {"l": 60, "r": 60, "t": 10, "b": 30},
        "paper_bgcolor": "#ffffff",
        "scene": {
            "xaxis": {"title": {"text": scene["axes"][0], "font": {"size": 12}}, "backgroundcolor": "#f7f9fc",
                      "gridcolor": "#ffffff"},
            "yaxis": {"title": {"text": scene["axes"][1], "font": {"size": 12}}, "backgroundcolor": "#f7f9fc",
                      "gridcolor": "#ffffff"},
            "zaxis": {"title": {"text": scene["axes"][2], "font": {"size": 12}}, "backgroundcolor": "#f7f9fc",
                      "gridcolor": "#ffffff"},
            "camera": {"eye": {"x": 1.55, "y": 1.55, "z": 1.15}, "center": {"x": 0, "y": 0, "z": 0}},
            "aspectmode": "cube", "aspectratio": {"x": 1, "y": 1, "z": 0.85},
        },
        "legend": {"orientation": "h", "y": 0.02, "x": 0.5, "xanchor": "center", "font": {"size": 12}},
        "font": {"family": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif", "size": 13},
    }
    return json.dumps({"data": scene["traces"], "layout": layout}, separators=(",", ":"))


def page() -> str:
    ss = scenes()
    body = []
    for scene in ss:
        body.append(f'''
  <section class="scene">
    <h2 id="{scene["id"]}">{scene["title"]}</h2>
    <p class="note">{scene["caption"]}</p>
    <div class="plot" id="plot-{scene["id"]}" data-plot='{_scene_json(scene)}'></div>
  </section>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Climate in 3D — PACLAND</title>
<style>
  :root{{--ink:#15181f;--muted:#5a6072;--line:#e3e6ee;--accent:#1b4fd8;--bg:#fff}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
       font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
  .wrap{{max-width:960px;margin:0 auto;padding:1.6rem 1.2rem 3rem}}
  h1{{font-size:1.55rem;margin:.2rem 0 .1rem}}
  .sub{{color:var(--muted);margin:0 0 1.2rem}}
  h2{{font-size:1.05rem;margin:2rem 0 .2rem}}
  p.note{{color:var(--muted);font-size:.93rem;margin:.1rem 0 .5rem;max-width:60ch}}
  .plot{{width:100%;height:560px;border:1px solid var(--line);border-radius:10px;background:#fff}}
  .back{{font-size:.9rem}}
  .back a{{color:var(--accent);text-decoration:none}}
  @media (max-width:640px){{ .plot{{height:420px}} }}
</style>
</head>
<body><div class="wrap">
  <p class="back"><a href="./index.html">← back to PACLAND</a></p>
  <h1>Climate — the verification, in 3D</h1>
  <p class="sub">Same data as <a href="./climate.html">the 2D figures</a>, drawn as three scenes you can
  rotate: drag to turn, scroll to zoom, hover a dot for the model. Each scene says what to look for.</p>
{"".join(body)}
  <p class="back" style="margin-top:2rem">Generated by <code>scripts/build_climate_3d.py</code> from
  <code>data/climate/*.json</code>. The 2D version needs no JavaScript: <a href="./climate.html">the figures</a>.</p>
</div>
<script src="./vendor/plotly-2.35.2.min.js"></script>
<script>
(function () {{
  if (!window.Plotly) {{
    document.querySelectorAll('.plot').forEach(function (el) {{
      el.innerHTML = '<p style="padding:1rem;color:#5a6072">The 3D view needs the Plotly library, ' +
                     'which did not load. The 2D figures work without it: <a href="./climate.html">see the figures</a>.</p>';
    }});
    return;
  }}
  var opts = {{responsive: true, displayModeBar: false}};
  document.querySelectorAll('.plot').forEach(function (el) {{
    var spec = JSON.parse(el.getAttribute('data-plot'));
    Plotly.newPlot(el, spec.data, spec.layout, opts);
  }});
}})();
</script>
</body></html>
'''


def main() -> int:
    html = page()
    OUT.write_text(html)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html.splitlines())} lines, "
          f"{len(scenes())} scenes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
