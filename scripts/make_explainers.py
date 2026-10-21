#!/usr/bin/env python3
"""Auto-generate the plain-English explainer PDF for every discipline.

Each discipline's content() pulls its real numbers from its modules, so these
PDFs are always current — regenerate after any discipline changes:

    python3 scripts/make_explainers.py

Outputs to the repo root as PACLAND-{discipline}-explainer.pdf.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.explainer import render  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    disciplines = ["climate", "drugs"]
    for name in disciplines:
        mod = __import__(f"pacland.{name}.explainer", fromlist=["content"])
        out = ROOT / f"PACLAND-{name}-explainer.pdf"
        render(mod.content(), str(out))
        print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
