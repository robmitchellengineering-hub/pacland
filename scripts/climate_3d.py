#!/usr/bin/env python3
"""3D graphs of the climate verification — interactive HTML (plotly).

Three scenes, easy to read and interpret:
  1. THE LEAK CUBE      — 19 models in energy x mass x salt drift space; the
                          leakers float out from the origin, the good ones cluster.
  2. THE TRUST GATE     — 53 models in ECS x forcing x conservation space, with
                          the verification box they must land inside.
  3. THE FIX            — the same 19 models before -> after drift-correction
                          (arrows collapse onto the conserved origin).

Outputs: PACLAND-climate-3d.html (open in any browser — rotate, zoom, hover).
"""
from __future__ import annotations

import json
import sys

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pacland.climate import trust_board
from pacland.climate.drift_correction import leak


def _drift_rows():
    d = json.load(open("data/climate/cmip6_drift.json"))
    return {m["model"]: leak(m["model"]) for m in d["models"]}


def _trust_rows():
    return trust_board.board()


def _energy_drift():
    """Energy drift for every model with data: Irving (19) + widened (27)."""
    out = {m: _drift_rows()[m]["energy_Wm2"] for m in _drift_rows()}
    z = json.load(open("data/climate/zonal_drift.json"))
    for m in z.get("models", []):
        out.setdefault(m["model"], m["netTOA_drift_Wm2"])
    return out


def leak_cube(fig, row, col):
    dr = _drift_rows()
    xs = [dr[m]["energy_Wm2"] for m in dr]
    ys = [dr[m]["mass_mm_per_yr"] for m in dr]
    zs = [dr[m]["salt_g_per_kg_per_yr"] for m in dr]
    colr = ["#e15759" if (dr[m]["energy_leaks"] or dr[m]["mass_leaks"] or dr[m]["salt_leaks"])
            else "#59a14f" for m in dr]
    labels = ["<b>leaks</b> (fails conservation)" if c == "#e15759"
              else "<b>conserves</b> (all three ledgers)" for c in colr]
    # one trace per group for the legend
    for c, name in (("#e15759", "leaks"), ("#59a14f", "conserves")):
        idx = [i for i in range(len(xs)) if colr[i] == c]
        fig.add_trace(go.Scatter3d(
            x=[xs[i] for i in idx], y=[ys[i] for i in idx], z=[zs[i] for i in idx],
            mode="markers", text=[list(dr)[i] for i in idx],
            marker=dict(size=8, color=c, opacity=0.9),
            name=name, hovertemplate="%{text}<br>energy %{x:.2f} W/m²<br>mass %{y:.2f} mm/yr<br>salt %{z:.2e} g/kg<extra></extra>",
        ), row=row, col=col)
    # the conserved origin
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                               marker=dict(size=7, color="black", symbol="diamond"),
                               name="conserved (0,0,0)", showlegend=False), row=row, col=col)


def trust_gate(fig, row, col):
    tb = _trust_rows()
    ed = _energy_drift()
    xs = [m["ecs_K"] for m in tb]
    ys = [m["erf2x_Wm2"] for m in tb]
    zs = [ed.get(m["model"], 0.0) for m in tb]
    trusted = [len(m["axes_failed"]) == 0 and m["axes_available"] == 3 for m in tb]
    colr = ["#f28e2b" if t else "#76b7b2" for t in trusted]
    for c, name in (("#f28e2b", "trusted (all 3 axes)"), ("#76b7b2", "fails ≥1 axis")):
        idx = [i for i in range(len(xs)) if colr[i] == c]
        fig.add_trace(go.Scatter3d(
            x=[xs[i] for i in idx], y=[ys[i] for i in idx], z=[zs[i] for i in idx],
            mode="markers", marker=dict(size=6, color=c, opacity=0.9),
            name=name, text=[tb[i]["model"] for i in idx],
            hovertemplate="%{text}<br>ECS %{x:.2f} K<br>ERF2x %{y:.2f} W/m²<br>drift %{z:.2f} W/m²<extra></extra>",
        ), row=row, col=col)
    # the verification gate: ECS 2.5-4.0, ERF2x 3.3-4.1 (conservation = drift 0)
    box_x = [2.5, 4.0, 4.0, 2.5, 2.5]
    box_y = [3.3, 3.3, 4.1, 4.1, 3.3]
    fig.add_trace(go.Scatter3d(
        x=box_x, y=box_y, z=[0, 0, 0, 0, 0], mode="lines",
        line=dict(color="#444444", width=4, dash="dash"),
        name="trust gate (ECS 2.5–4.0, ERF2x 3.3–4.1)", showlegend=False), row=row, col=col)


def the_fix(fig, row, col):
    dr = _drift_rows()
    xs = [dr[m]["energy_Wm2"] for m in dr]
    ys = [dr[m]["mass_mm_per_yr"] for m in dr]
    zs = [dr[m]["salt_g_per_kg_per_yr"] for m in dr]
    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs, mode="markers", marker=dict(size=5, color="#e15759", opacity=0.7),
        name="before (leak)", text=list(dr),
        hovertemplate="%{text}<br>before: %{x:.2f}, %{y:.2f}, %{z:.2e}<extra></extra>"), row=row, col=col)
    fig.add_trace(go.Scatter3d(
        x=[0] * len(xs), y=[0] * len(ys), z=[0] * len(zs), mode="markers",
        marker=dict(size=6, color="#59a14f"), name="after (corrected)"), row=row, col=col)
    # arrows before -> after
    for m in dr:
        fig.add_trace(go.Scatter3d(
            x=[dr[m]["energy_Wm2"], 0], y=[dr[m]["mass_mm_per_yr"], 0],
            z=[dr[m]["salt_g_per_kg_per_yr"], 0], mode="lines",
            line=dict(color="#999999", width=2), showlegend=False,
            hoverinfo="skip"), row=row, col=col)


def main():
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}]],
        subplot_titles=(
            "<b>1 · The leak</b> — red dots float OUT of the conserved origin; green stays put",
            "<b>2 · The trust gate</b> — orange passes all 3 axes; the dashed box is where a model must land",
            "<b>3 · The fix</b> — drift-correction pulls every red dot back to (0,0,0)",
        ),
    )
    leak_cube(fig, 1, 1)
    trust_gate(fig, 1, 2)
    the_fix(fig, 1, 3)
    axes = dict(
        scene=dict(xaxis_title="energy drift (W/m²)", yaxis_title="mass drift (mm/yr)", zaxis_title="salt drift (g/kg/yr)"),
        scene2=dict(xaxis_title="ECS (K)", yaxis_title="ERF2x (W/m²)", zaxis_title="energy drift (W/m²)"),
        scene3=dict(xaxis_title="energy drift (W/m²)", yaxis_title="mass drift (mm/yr)", zaxis_title="salt drift (g/kg/yr)"),
    )
    fig.update_layout(
        title=dict(text="<b>PACLAND · Climate — the verification, in 3D</b><br>"
                        "<span style='font-size:12px'>rotate · zoom · hover a dot for the model name — "
                        "each scene's title says what to look for</span>"),
        height=680, margin=dict(l=10, r=10, t=90, b=10), **axes,
        legend=dict(orientation="h", y=-0.02),
    )
    fig.write_html("PACLAND-climate-3d.html", include_plotlyjs="cdn")
    try:
        fig.write_image("PACLAND-climate-3d.png", width=2000, height=720, scale=2)
        print("wrote PACLAND-climate-3d.png")
    except Exception as e:
        print(f"PNG skipped ({type(e).__name__})", file=sys.stderr)
    print("wrote PACLAND-climate-3d.html")


if __name__ == "__main__":
    main()
