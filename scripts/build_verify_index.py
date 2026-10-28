#!/usr/bin/env python3
"""Generate web/verify.html — the public verification index, from the certificates and the battery.

    python3 scripts/build_verify_index.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.causal import battery as B  # noqa: E402

OUT = ROOT / "web" / "verify.html"
CERTS = ROOT / "certificates"

# Rob, 2026-10-28: a qualified model is a pass with a caveat, so it reads green;
# only a refusal is red. Findings keep their own colours: satisfied green, failing red.
GRADE_CLASS = {"VERIFIED": "ok", "QUALIFIED": "ok", "RESTRICTED": "warn", "REFUSED": "bad"}

#: Findings have their own vocabulary — satisfied / partial / not demonstrated / failing — and their
#: own colours. They were silently falling through to the grade map's default, so every pill came out
#: amber; that is the bug this table fixes.
STATUS_CLASS = {"satisfied": "ok", "partial": "warn", "not demonstrated": "warn", "failing": "bad"}


def load_certificates() -> list[dict]:
    out = []
    for path in sorted(CERTS.glob("*.json")):
        out.append(json.loads(path.read_text()))
    return out


def cert_card(c: dict) -> str:
    cls = GRADE_CLASS.get(c["grade"], "warn")
    rows = "".join(
        f"<tr><td>{f['clause']}</td><td>{f['question']}</td><td class='ev'>{f['answer']}</td>"
        f"<td class='st'><span class='pill {STATUS_CLASS.get(f['status'], 'warn')}'>"
        f"{f['status']}</span></td></tr>"
        for f in c["findings"])
    return f"""
    <article class="card">
      <div class="cardhead">
        <h3>{c['subject']}</h3>
        <span class="grade {cls}">{c['grade']}</span>
      </div>
      <p class="headline">{c['headline']}</p>
      <table class="findings">
        <thead><tr><th>clause</th><th>question</th><th>what the evidence says</th><th class="st">status</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <p class="prov">evidence: {"; ".join(c['provenance'])}</p>
    </article>"""


def battery_table() -> str:
    res = B.run()
    rows = "".join(
        f"<tr><td>{c.dgp}</td><td>{c.estimator}</td>"
        f"<td class='num'>{c.estimate:+.3f}</td><td class='num'>{c.truth:.2f}</td>"
        f"<td class='num'>{c.recovery_rate:.0%}</td>"
        f"<td><span class='pill {'ok' if c.recovered else 'bad'}'>"
        f"{'recovers' if c.recovered else 'FAILS'}</span></td></tr>"
        for c in res["cells"])
    return (f"<table class='battery'><thead><tr><th>design</th><th>estimator</th>"
            f"<th>median</th><th>planted</th><th>recover</th><th></th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            f"<p class='note'>{res['n_recovered']} of {res['n_cells']} cells recover the planted "
            f"effect in at least half of {res['reps']} replications.</p>")


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Verification Index — Pacland</title>
<meta name="description" content="Institutional models and causal estimators, graded against evidence that was planted or measured rather than asserted.">
<style>
  :root {{ --ink:#1a1f2e; --muted:#5a6072; --accent:#142a5e; --line:#e3e6ee; --bg:#fbfbfd;
           --ok:#0f6b3a; --okbg:#e6f5ec; --warn:#8a5a00; --warnbg:#fdf3dc; --bad:#8c1d1d; --badbg:#fdeaea; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         color:var(--ink); background:var(--bg); line-height:1.6; }}
  .wrap {{ max-width:920px; margin:0 auto; padding:0 1.5rem; }}
  header {{ background:var(--accent); color:#fff; padding:3rem 0 2.4rem; }}
  header h1 {{ margin:0 0 .4rem; font-size:2rem; letter-spacing:-.02em; }}
  header p {{ color:#c7d2ee; margin:.3rem 0 0; }}
  header a {{ color:#fff; }}
  main {{ padding:2rem 0 4rem; }}
  h2 {{ font-size:1.35rem; color:var(--accent); margin:2.2rem 0 .5rem; }}
  .card {{ border:1px solid var(--line); border-radius:14px; padding:1.1rem 1.2rem; margin:1rem 0;
           background:#fff; }}
  .cardhead {{ display:flex; align-items:center; gap:.8rem; flex-wrap:wrap; }}
  .cardhead h3 {{ margin:0; font-size:1.1rem; flex:1 1 auto; min-width:14rem; }}
  .grade {{ font-weight:700; font-size:.8rem; letter-spacing:.04em; padding:.25rem .6rem;
            border-radius:999px; }}
  .grade.ok {{ color:var(--ok); background:var(--okbg); }}
  .grade.warn {{ color:var(--warn); background:var(--warnbg); }}
  .grade.bad {{ color:var(--bad); background:var(--badbg); }}
  .headline {{ margin:.6rem 0 .8rem; }}
  table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
  th,td {{ text-align:left; padding:.4rem .5rem; border-bottom:1px solid var(--line);
           vertical-align:top; }}
  th {{ font-weight:600; color:var(--muted); font-size:.8rem; text-transform:uppercase;
        letter-spacing:.03em; }}
  td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  td.ev {{ font-variant-numeric:tabular-nums; }}
  /* fixed layout so every card's columns land in the same place: without it each card sized its
     own columns by content and the status rail moved card to card */
  table.findings {{ table-layout:fixed; }}
  table.findings th:nth-child(1) {{ width:20%; }}
  table.findings th:nth-child(2) {{ width:28%; }}
  table.findings th:nth-child(3) {{ width:auto; }}
  /* 9rem, because 'not demonstrated' is wider than the other pills and overflowed the rail */
  td.st, th.st {{ width:9rem; text-align:right; white-space:nowrap; }}
  td.st .pill {{ display:inline-block; min-width:7rem; text-align:center; }}
  .pill {{ font-size:.75rem; font-weight:600; padding:.15rem .5rem; border-radius:999px;
           white-space:nowrap; }}
  .pill.ok {{ color:var(--ok); background:var(--okbg); }}
  .pill.warn {{ color:var(--warn); background:var(--warnbg); }}
  .pill.bad {{ color:var(--bad); background:var(--badbg); }}
  .prov {{ color:var(--muted); font-size:.78rem; margin:.7rem 0 0; }}
  .note {{ color:var(--muted); font-size:.9rem; }}
  .legend {{ display:flex; gap:1.2rem; flex-wrap:wrap; color:var(--muted); font-size:.85rem; }}
  footer {{ border-top:1px solid var(--line); padding:1.5rem 0 3rem; color:var(--muted);
            font-size:.85rem; }}
  @media (max-width:640px) {{
    table.findings th:nth-child(1), table.findings td:nth-child(1) {{ display:none; }}
    td.st, th.st {{ width:5.5rem; }}
    td.st .pill {{ min-width:0; }}
    table.battery th:nth-child(2), table.battery td:nth-child(2) {{ display:none; }}
  }}
</style>
</head>
<body>
<header><div class="wrap">
  <h1>The Verification Index</h1>
  <p>Models and methods, graded against evidence that was planted or measured — not asserted.</p>
  <p>Issued by Pacland · <a href="./index.html">pacland</a> · <a href="./all.html">find anything</a></p>
</div></header>
<main><div class="wrap">

<h2>Institutional models</h2>
<p>Each certificate answers five questions mapped to model-risk supervision (SR 11-7 concepts, PRA
SS1/23 lifecycle), and every number is regenerated from a script rather than transcribed. The grade is
the <strong>worst</strong> finding, not an average.</p>
<div class="legend">
  <span><span class="pill ok">satisfied</span> evidenced</span>
  <span><span class="pill warn">partial / not demonstrated</span> limited</span>
  <span><span class="pill bad">failing</span> the model cannot currently be relied on for this</span>
</div>
{certificates}

<h2>The known-truth battery for causal estimators</h2>
<p>Effects are <strong>planted</strong>, so recovering them is a checkable fact rather than an
opinion. Read it as a matrix, not a verdict: each estimator wins the design it was built for and
loses the others.</p>
{battery}

<footer>
  <p>Generated by <code>scripts/build_verify_index.py</code> from <code>certificates/*.json</code> and
  <code>src/pacland/causal/battery.py</code>. Reproduce every number:</p>
  <p><code>python3 scripts/issue_certificate.py --all</code><br>
     <code>python3 scripts/causal_battery.py</code></p>
</footer>
</div></main>
</body>
</html>
"""


def main() -> int:
    certs = load_certificates()
    cards = "".join(cert_card(c) for c in certs)
    OUT.write_text(HTML.format(certificates=cards, battery=battery_table()))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(certs)} certificates, battery table")
    return 0


if __name__ == "__main__":
    sys.exit(main())
