#!/usr/bin/env python3
"""Render a PACLAND markdown doc to PDF (fpdf2 + Arial Unicode).

Handles the subset used in this repo: #/##/### headings, paragraphs, fenced
math blocks, bullet lists, blockquotes, and pipe tables.

Usage: python scripts/render_pdf.py <in.md> <out.pdf>
"""
import re
import sys

from fpdf import FPDF

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"  # full glyph coverage (no bold, but no missing glyphs)


def _clean_inline(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s


def _is_separator(line: str) -> bool:
    s = line.strip()
    return bool(s) and set(s) <= {"-", "|", ":", " "}


def render(md_path: str, out_path: str) -> None:
    with open(md_path) as f:
        lines = f.read().split("\n")

    pdf = FPDF(format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.add_font("uni", "", FONT)
    pdf.add_font("unib", "", BOLD)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            pdf.ln(1)
            continue
        if in_code:
            pdf.set_font("uni", "", 9)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(24)
            pdf.multi_cell(0, 4.5, line.rstrip(), align="L")
            continue
        if line.startswith("# "):
            pdf.set_font("unib", "", 16)
            pdf.set_text_color(15, 35, 80)
            pdf.multi_cell(0, 9, line[2:], align="L")
            pdf.ln(1)
        elif line.startswith("## "):
            pdf.set_font("unib", "", 12.5)
            pdf.set_text_color(15, 35, 80)
            pdf.ln(3)
            pdf.multi_cell(0, 7, line[3:], align="L")
            pdf.ln(1)
        elif line.startswith("### "):
            pdf.set_font("unib", "", 11)
            pdf.set_text_color(15, 35, 80)
            pdf.ln(2)
            pdf.multi_cell(0, 6, line[4:], align="L")
        elif line.startswith("- "):
            pdf.set_font("uni", "", 9.5)
            pdf.set_text_color(25, 25, 25)
            pdf.set_x(22)
            pdf.multi_cell(0, 5.2, "•  " + line[2:], align="L")
            pdf.ln(0.4)
        elif line.startswith("> "):
            pdf.set_font("uni", "", 9.5)
            pdf.set_text_color(60, 60, 60)
            pdf.set_x(24)
            pdf.multi_cell(0, 5.2, line[2:], align="L")
        elif _is_separator(line):
            continue
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            pdf.set_font("uni", "", 9)
            pdf.set_text_color(25, 25, 25)
            w = 174 / max(len(cells), 1)
            for c in cells:
                pdf.cell(w, 5.5, _clean_inline(c), border=0, align="L")
            pdf.ln(5.5)
        elif line.strip() == "":
            pdf.ln(1.5)
        else:
            pdf.set_font("uni", "", 9.5)
            pdf.set_text_color(25, 25, 25)
            pdf.multi_cell(0, 5.2, _clean_inline(line), align="L")
            pdf.ln(0.8)

    pdf.output(out_path)
    print(f"wrote {out_path} ({pdf.pages_count} pages)")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
