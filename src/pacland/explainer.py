"""Reusable plain-English explainer-PDF renderer.

Each discipline exposes a ``content()`` function returning a list of
``(kind, text)`` tuples — kinds: ``title``, ``subtitle``, ``h`` (section),
``p`` (paragraph), ``b`` (bullet). ``render()`` turns them into the same
A4 PDF the physics explainer uses, and the content is generated from the
discipline's own modules (deficit, guards, findings) — so the PDF is always
current, never hand-written prose that drifts from the code.

Requires fpdf2.
"""
from __future__ import annotations

import os

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
DEFAULT_FOOTER = "github.com/robmitchellengineering-hub/pacland"


#: A one-page sheet needs smaller type than a multi-page brief, and it must not spill.
#: ``compact`` scales every size and gap by this factor (tuned to keep ~500 words on A4).
COMPACT_SCALE = 0.82


def render(entries: list[tuple[str, str]], out_path: str,
           footer: str = DEFAULT_FOOTER, compact: bool = False) -> str:
    """Render ``entries`` to ``out_path`` (A4). Returns ``out_path``.

    ``compact=True`` is for one-pagers: everything scales by ``COMPACT_SCALE`` so the page
    still fits when the text is aimed at a general reader rather than a specialist.
    """
    from fpdf import FPDF

    k = COMPACT_SCALE if compact else 1.0
    margin = 18 * k
    pdf = FPDF(format="A4")
    pdf.set_margins(margin, margin, margin)
    pdf.add_font("uni", "", FONT)
    pdf.set_auto_page_break(auto=True, margin=14 * k)

    pdf.add_page()
    for kind, text in entries:
        if kind == "title":
            pdf.set_font("uni", "", 22 * k)
            pdf.set_text_color(20, 40, 90)
            pdf.multi_cell(0, 10 * k, text, align="L")
            pdf.ln(1)
        elif kind == "subtitle":
            pdf.set_font("uni", "", 11 * k)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 5.5 * k, text, align="L")
            pdf.ln(4)
        elif kind == "h":
            pdf.set_font("uni", "", 14 * k)
            pdf.set_text_color(20, 40, 90)
            pdf.ln(3 * k)
            pdf.multi_cell(0, 7 * k, text, align="L")
            pdf.ln(1)
        elif kind == "headline":
            pdf.set_font("uni", "", 12.5)
            pdf.set_text_color(20, 40, 90)
            pdf.ln(1)
            pdf.multi_cell(0, 7, "▸  " + text, align="L")
            pdf.ln(1.5)
        elif kind == "p":
            pdf.set_font("uni", "", 10.5 * k)
            pdf.set_text_color(25, 25, 25)
            pdf.multi_cell(0, 5.5 * k, text, align="L")
            pdf.ln(1.5)
        elif kind == "b":
            pdf.set_font("uni", "", 10.5 * k)
            pdf.set_text_color(25, 25, 25)
            pdf.set_x(20 * k)
            pdf.multi_cell(0, 5.5 * k, "•  " + text, align="L")
            pdf.ln(1)
        else:
            raise ValueError(f"unknown explainer kind: {kind!r}")

    # stamping a footer must not trigger a page break: at the bottom margin every write
    # counts as overflow, which added a phantom final page to any full sheet (2026-10-26)
    pdf.set_auto_page_break(auto=False)
    for page in range(1, pdf.pages_count + 1):
        pdf.page = page
        pdf.set_y(-12 * k)
        pdf.set_font("uni", "", 8)
        pdf.set_text_color(140, 140, 140)
        pdf.cell(0, 5, f"{footer}  ·  page {page}/{pdf.pages_count}", align="C")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    pdf.output(out_path)
    return out_path


__all__ = ["render", "FONT", "DEFAULT_FOOTER"]
