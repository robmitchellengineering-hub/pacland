#!/usr/bin/env python3
"""Generate the PACLAND headline PDF (repo root) — "what it is, and why it matters".

One pretty document for someone who has heard none of the story: answers "so what is
it?" and "but how?", states the five results that changed the field, and says what it
means for research. fpdf2 + Arial Unicode, a dark-blue cover band, blue section
headings, bold result lead-ins, and a footer.

Requires fpdf2:  python3 -m pip install --user fpdf2
"""
import os

from fpdf import FPDF

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUT = os.path.join(_ROOT, "PACLAND-what-and-why.pdf")

ACCENT = (20, 42, 94)       # the front-page ink blue
BODY = (26, 29, 38)
MUTED = (95, 100, 115)

# (kind, text) — kinds: title, subtitle, h, p, b, rtitle (result lead-in), rbody
C = [
    ("title", "PACLAND"),
    ("subtitle", "What it is, and why it matters — for people who have heard none of the story."),

    ("h", "So what is it?"),
    ("p", "PACLAND is a verification discipline, applied one field at a time — physics first, then "
          "climate, economics, medicine. It does one thing relentlessly: it measures how much of a "
          "claim can actually be checked, and refuses the rest."),
    ("p", "That used to be the whole story. It is not anymore. On top of verification we have now built "
          "a belief layer — the part that answers what verification cannot: how much should I believe "
          "each unproven claim, which one do I test next, and how honest has my confidence been?"),
    ("p", "The result is a clean, honest split for any claim, anywhere:"),
    ("b", "exact — proven by a machine-checked proof, or counted exactly with no sampler and no run-to-run variance"),
    ("b", "calibrated belief — a number with a stated margin, scored against how often it turned out right"),
    ("b", "unknown — reported as unknown, never dressed up as a result"),

    ("h", "But how?"),
    ("p", "Three moves, and they transfer to any field:"),
    ("b", "Ask for the constraints, the count and the deficit — never the values. A theory of everything "
          "predicts relations, never values."),
    ("b", "Make the computable part exact. 43,046,720 string-theory vacua counted exactly — twice, by two "
          "programs that share no code — no sampler, no probability, no run-to-run variance."),
    ("b", "Make the uncomputable part honest. Three gates stop a bad number reaching a decision; the belief "
          "layer scores what is still open."),

    ("h", "The five results that changed the field"),
    ("rtitle", "1 · “A theory of everything predicts relations, never values” — now a theorem"),
    ("rbody", "The exact content of the physics is constraints and labels, and nothing else. The tadpole "
              "is the unique invariant (machine-checked); the whole invariant ring is one generator. "
              "Masses, couplings and the cosmological constant are provably not exact."),
    ("rtitle", "2 · The Standard Model's charges are forced, not chosen"),
    ("rbody", "Anomaly cancellation pins the hypercharges uniquely (5/5), and three generations fall out "
              "as a topological index. The charge assignment we observe is the consistent one."),
    ("rtitle", "3 · The 19 floor — no completion derives the values"),
    ("rbody", "The 19 free parameters of particle physics are exactly the orbit-space dimension of the "
              "theory's own symmetry, and no tested completion derives more than two of them correctly."),
    ("rtitle", "4 · Deterministic in use"),
    ("rbody", "A field everyone assumed needed sampling returns an exact count — 43 million vacua, "
              "verified twice. The right question turns “intractable” into “exact”."),
    ("rtitle", "5 · The belief layer"),
    ("rbody", "What is still open is now handled honestly: calibrated belief, ranked by what to test next, "
              "with a probably-approximately-correct guarantee."),

    ("h", "So what does it mean for research?"),
    ("b", "Physics gets a falsifiable target: derive a value from a deeper theory, and the “relations, never "
          "values” thesis dies. Progress, with a way to be wrong."),
    ("b", "The method transfers: the same discipline already runs on climate, economics, medicine and — "
          "through Ask Alice — historical research. The physics results are the proof of concept; the "
          "discipline is the product."),
    ("b", "A new standard for uncertainty: “here is what is proven, here is what I believe and how calibrated "
          "that is” — a label nobody issues today, and the SDK behind it is live."),

    ("h", "The bottom line"),
    ("p", "We did not solve string theory. We changed what it means to work on it: the exact part is now "
          "provable, and the open part is now a measured, calibrated, guaranteed belief instead of an "
          "adjective. That is the difference between believing and knowing."),
]


def _header(pdf: FPDF) -> None:
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, 210, 46, style="F")
    pdf.set_xy(18, 13)
    pdf.set_font("uni", "", 27)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "PACLAND", align="L")
    pdf.set_xy(18, 28)
    pdf.set_font("uni", "", 10.5)
    pdf.set_text_color(199, 210, 238)
    pdf.cell(0, 6, "What it is, and why it matters — for people who have heard none of the story.", align="L")
    pdf.set_y(52)


class PDF(FPDF):
    """Footer via the canonical hook, so every page gets the same size and alignment."""

    def footer(self):
        self.set_y(-12)
        self.set_font("uni", "", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 5, "github.com/robmitchellengineering-hub/pacland  ·  PACLAND-what-and-why  ·  "
                        "page " + str(self.page_no()) + "/{nb}", align="C")


def build() -> None:
    pdf = PDF(format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.add_font("uni", "", FONT)
    pdf.add_font("unib", "", FONT_BOLD)
    pdf.alias_nb_pages("{nb}")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    _header(pdf)

    for kind, text in C:
        if kind == "title" or kind == "subtitle":
            continue  # rendered in the header band
        if kind == "h":
            pdf.set_font("unib", "", 13.5)
            pdf.set_text_color(*ACCENT)
            pdf.ln(3)
            pdf.multi_cell(0, 7.5, text, align="L")
            pdf.set_draw_color(*ACCENT)
            pdf.set_line_width(0.4)
            pdf.line(18, pdf.get_y() + 0.5, 192, pdf.get_y() + 0.5)
            pdf.ln(3)
        elif kind == "rtitle":
            # keep the lead-in with its first body line
            if pdf.get_y() > 240:
                pdf.add_page()
            pdf.set_font("unib", "", 11)
            pdf.set_text_color(*ACCENT)
            pdf.multi_cell(0, 6, text, align="L")
            pdf.ln(0.5)
        elif kind == "rbody":
            pdf.set_font("uni", "", 10.5)
            pdf.set_text_color(*BODY)
            pdf.set_x(24)
            pdf.multi_cell(168, 5.6, text, align="L")
            pdf.ln(1.6)
        elif kind == "p":
            pdf.set_font("uni", "", 10.5)
            pdf.set_text_color(*BODY)
            pdf.multi_cell(0, 5.6, text, align="L")
            pdf.ln(1.6)
        elif kind == "b":
            pdf.set_font("uni", "", 10.5)
            pdf.set_text_color(*BODY)
            pdf.set_x(20)
            pdf.cell(5, 5.6, "•")
            pdf.set_x(26)
            pdf.multi_cell(166, 5.6, text, align="L")
            pdf.ln(1)

    pdf.output(_OUT)
    print(f"wrote {_OUT}  ({pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
