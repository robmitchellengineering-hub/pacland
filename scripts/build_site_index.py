#!/usr/bin/env python3
"""Build the site's searchable index — one place to find everything.

92 docs, 92 scripts, 5 explainer PDFs and six scored models do not belong in a wall of
cards. This script reads the repo and writes:

  web/index.json   every doc / script / PDF / command, with a title, a one-line summary,
                   a kind and a path
  web/all.html     a standalone searchable page that renders index.json (vanilla JS, no
                   build step at deploy time — Netlify publishes web/ as-is)

Run after adding or renaming anything:

    python3 scripts/build_site_index.py

`tests/test_site_index.py` fails if the committed index.json is stale, so the index cannot
silently drift from the repo the way the Pages mirror did.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "web" / "index.json"

#: Hand-curated entry points. The generated list is for finding things; these are for
#: starting, and they say why they matter rather than what they are called.
START_HERE = [
    ("The bar — nine slots, three refusals", "docs/verify-bar.md", "the method, and the climate transfer test"),
    ("How a field gets figured out", "docs/SOP-FIGURING-SYSTEMS-OUT.md", "the general method, learned the hard way"),
    ("Economics — the model roster", "docs/economics-model-roster.md", "six models scored; four clean; what each owes"),
    ("Climate — the trust board", "docs/climate-trust-board.md", "53 CMIP6 models scored; 14 trusted"),
    ("The verification deficit", "docs/economics-verification-deficit.md", "m = 4 backcast, m = 0 forecast"),
    ("Economics explainer (PDF)", "PACLAND-economics-explainer.pdf", "plain English, for sending to someone"),
    ("Climate explainer (PDF)", "PACLAND-climate-explainer.pdf", "plain English, for sending to someone"),
]

#: The CLI, described by what it answers. Someone looking for a number should find the
#: command that prints it, not a module path.
COMMANDS = [
    ("pacland economics", "the verification deficit (unchanged default)"),
    ("pacland economics --models", "the roster, scored, with what each row owes"),
    ("pacland economics --constraints", "the constraint set and its measured independent rank"),
    ("pacland economics --realtime", "every model against its null, on published data"),
    ("pacland climate", "the climate verification deficit"),
    ("pacland trust", "the trust board — every artifact, ranked"),
    ("pacland disciplines", "the discipline registry"),
]


def _clip(text: str, limit: int = 190) -> str:
    """Cut on a word boundary and mark the cut — never mid-word, never silently."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return cut + "…"


def _title_and_summary(md: pathlib.Path) -> tuple[str, str]:
    """Title from the first H1; summary from the first real paragraph, joined whole.

    The first paragraph is gathered across its wrapped lines and only then clipped — a
    per-line summary ends mid-sentence ("...five laws specifying how the") and reads like a
    bug, because it is one.
    """
    text = md.read_text(errors="ignore")
    title = md.stem.replace("-", " ")
    lines = text.splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    para: list[str] = []
    started = False
    for line in lines[1:]:
        stripped = line.strip()
        if not started:
            if (not stripped or stripped.startswith(("#", "|", ">", "-", "*", "`", "["))
                    or stripped.startswith("Status") or stripped.startswith("**Status")):
                continue
            started = True
        if not stripped:
            break
        para.append(stripped)
    summary = _clip(re.sub(r"[*_`]", "", " ".join(para)))
    return title[:110], summary


def docs() -> list[dict]:
    out = []
    for md in sorted((ROOT / "docs").glob("*.md")):
        title, summary = _title_and_summary(md)
        out.append({"kind": "doc", "title": title, "summary": summary,
                    "path": f"docs/{md.name}", "href": f"https://github.com/robmitchellengineering-hub/pacland/blob/main/docs/{md.name}"})
    return out


def scripts() -> list[dict]:
    out = []
    for p in sorted((ROOT / "scripts").iterdir()):
        if p.suffix not in {".py", ".mjs", ".sh"}:
            continue
        doc = ""
        try:
            lines = p.read_text(errors="ignore").splitlines()
            # a shebang is not documentation — skip it and every other noise line
            for line in lines[:12]:
                line = line.strip()
                if line.startswith("#!"):
                    continue
                if line.startswith('"""'):
                    doc = line.strip('"').strip()
                    if not doc and len(lines) > 1:
                        doc = lines[1].strip().strip('"').strip()
                    break
                if line.startswith("#") and len(line) > 3:
                    doc = line.lstrip("# ").strip()
                    break
        except OSError:
            pass
        doc = _clip(doc)
        out.append({"kind": "script", "title": p.name, "summary": doc[:200],
                    "path": f"scripts/{p.name}", "href": f"https://github.com/robmitchellengineering-hub/pacland/blob/main/scripts/{p.name}"})
    return out


def pdfs() -> list[dict]:
    return [{"kind": "pdf", "title": p.stem.replace("PACLAND-", "").replace("-", " "),
             "summary": "explainer PDF", "path": p.name,
             "href": f"https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/{p.name}"}
            for p in sorted(ROOT.glob("PACLAND-*.pdf"))]


def build() -> dict:
    return {
        "generated_from": "scripts/build_site_index.py",
        "start": [{"title": t, "path": p, "summary": s,
                   "href": (f"https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/{p}"
                            if p.endswith(".pdf")
                            else f"https://github.com/robmitchellengineering-hub/pacland/blob/main/{p}")}
                  for t, p, s in START_HERE],
        "commands": [{"title": c, "summary": s} for c, s in COMMANDS],
        "items": docs() + scripts() + pdfs(),
    }


def main() -> int:
    data = build()
    OUT_JSON.write_text(json.dumps(data, indent=1, sort_keys=True))
    n = {k: sum(1 for i in data["items"] if i["kind"] == k) for k in ("doc", "script", "pdf")}
    print(f"wrote {OUT_JSON.relative_to(ROOT)}: {n['doc']} docs, {n['script']} scripts, "
          f"{n['pdf']} pdfs, {len(data['start'])} start-here, {len(data['commands'])} commands")
    return 0


if __name__ == "__main__":
    sys.exit(main())
