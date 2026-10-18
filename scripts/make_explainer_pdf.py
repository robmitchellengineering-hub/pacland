#!/usr/bin/env python3
"""Generate the PACLAND explainer PDF (repo root).

Requires fpdf2:  python3 -m pip install --user fpdf2
"""
import os

from fpdf import FPDF

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "PACLAND-explainer.pdf")

# (kind, text)  — kinds: title, subtitle, h (section), p (paragraph), b (bullet), table
C = [
    ("title", "PACLAND"),
    ("subtitle", "What we are building, and why it matters — a plain-English brief for an engineer (basic physics only)"),

    ("h", "1 · What we are actually trying to do"),
    ("p", "String theory does not describe one universe. It describes a menu of roughly 10^500 possible universes — the “landscape” — each with different particles, forces, and constants. “Unified string theory” is the claim that exactly one of them — ours — is singled out, and the open problem is why."),
    ("p", "The catch, in two sentences. First, 10^500 is so large that no search can scan it — it is astronomically beyond any computer that will ever exist. Second, there is no experiment that distinguishes most of those universes, so even if you found a candidate, you could not verify it the way you would verify a piece of code against a test."),
    ("p", "The field is therefore stuck on two separate questions it keeps treating as one:"),
    ("b", "Verification — does some vacuum match the universe we actually observe?"),
    ("b", "Selection — why that vacuum, and not one of the other 10^500?"),
    ("p", "PACLAND is our attempt to make the verification half rigorous — and to name the selection half as the part we are deliberately not pretending to solve."),

    ("h", "2 · The key idea (borrowed from Leslie Valiant)"),
    ("p", "Leslie Valiant is a computer scientist who founded “PAC learning” — probably-approximately-correct learning. His lesson: when you cannot prove something exactly, you certify it instead — “with probability at least 1−δ, the answer is correct to within ε.”"),
    ("p", "We apply exactly that to string theory. Instead of the impossible “prove this vacuum is our universe,” we ask the checkable version:"),
    ("p", "“Certify that this vacuum’s physics matches observation within tolerance ε, with confidence δ.”"),
    ("p", "That is a certificate with explicit numbers — the kind of thing an engineer can build and test. And it is exactly what we built."),

    ("h", "3 · What we actually built (concrete, not just documents)"),
    ("b", "A specification — six layers (encoding → oracle → verifier → search → knowledge → selection), written down in a public repo."),
    ("b", "A verification library — pure Python, 30 passing tests — that computes the “Valiant certificate”: a probably-approximately-correct upper bound on how wrong a candidate vacuum is."),
    ("b", "A learnability rig — a VC-dimension estimator and a vacuum sampler, tested against synthetic cases with known answers, so we trust it before it touches real data."),
    ("b", "Real physics, wired in and verified — we installed the actual string-theory tools (CYTools for Calabi-Yau geometry, JAXVacua for flux vacua) on a Linux node and ran them. They work: the quintic Calabi-Yau returns its known Hodge numbers (1, 101), and JAXVacua found 37 real flux vacua in a test run."),
    ("p", "That last bullet is the one that matters most to an engineer: the project is no longer just theory on paper — the pipeline produces real numbers."),

    ("h", "4 · The two honest numbers to remember"),
    ("b", "~43% — the tightest certificate we can currently write. Verification is bounded by how many measured facts we have about our universe (about 19 free parameters of the Standard Model), not by how much we can compute. Money cannot buy this number down."),
    ("b", "<1% — the honest odds of literally “solving unified string theory.” That is not pessimism; it is what the framework itself shows: selection (“why this one”) is a separate, 40-year-unsolved physics problem that our verification framework deliberately does not touch."),
    ("p", "The realistic target is different: a citable result — most likely the learnability answer."),

    ("h", "5 · The question that could actually pay off"),
    ("p", "We ask: is the map from geometry to physics learnable? Formally, does the class of prediction functions induced by vacua have small VC / SQ dimension?"),
    ("p", "This is a genuine either/or, and both outcomes are results:"),
    ("b", "If yes — the landscape is navigable: an evolutionary search with provable guarantees can find our vacuum."),
    ("b", "If no — no search can find our vacuum, the same way no amount of data can learn certain functions. That is a real, publishable negative result about the whole program."),
    ("p", "That is the value of the reframe: we replaced “win the lottery” with “measure a property, and either answer is a finding.”"),

    ("h", "6 · Odds of success, tracked against what is built"),
    ("table", None),

    ("h", "7 · Why this matters beyond string theory (for you)"),
    ("p", "The pattern — huge search space, no ground truth, claims you cannot verify — is not exotic. It is exactly what an engineer faces with a complex system, an ML model, or a codebase too large to test exhaustively."),
    ("p", "The reusable ideas:"),
    ("b", "When you cannot prove, certify. Replace “it is correct” with “it is correct within ε with confidence δ” — and compute what that actually takes."),
    ("b", "Separate verification from selection. “Does it match?” and “why was it chosen?” are different questions; conflating them is how projects stall."),
    ("b", "Name what is uncomputable. Saying “this part cannot be solved by compute” is not giving up — it is the map that tells you where effort will actually pay."),

    ("h", "8 · Where we are"),
    ("p", "Repo: github.com/robmitchellengineering-hub/pacland (public). Specification + verification library + learnability rig + verified physics tooling, all committed and tested. Next step: run the vacuum sampler at scale and measure the learnability dimension for real."),
]

TABLE_HEADER = ["Target", "Start", "Now", "Why it moved"]
TABLE_ROWS = [
    ["Certificate framework (paper)", "60–80%", "~90%", "library built + tested + real data"],
    ["Learnability answer", "25–45%", "~50–60%", "vacuum sampler now runs for real"],
    ["Solve string theory", "<1%", "<1%", "unchanged — physics-capped"],
]


def build() -> None:
    pdf = FPDF(format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.add_font("uni", "", FONT)
    pdf.set_auto_page_break(auto=True, margin=18)

    pdf.add_page()
    for kind, text in C:
        if kind == "title":
            pdf.set_font("uni", "", 22)
            pdf.set_text_color(20, 40, 90)
            pdf.multi_cell(0, 10, text, align="L")
            pdf.ln(1)
        elif kind == "subtitle":
            pdf.set_font("uni", "", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 5.5, text, align="L")
            pdf.ln(4)
        elif kind == "h":
            pdf.set_font("uni", "", 14)
            pdf.set_text_color(20, 40, 90)
            pdf.ln(3)
            pdf.multi_cell(0, 7, text, align="L")
            pdf.ln(1)
        elif kind == "p":
            pdf.set_font("uni", "", 10.5)
            pdf.set_text_color(25, 25, 25)
            pdf.multi_cell(0, 5.5, text, align="L")
            pdf.ln(1.5)
        elif kind == "b":
            pdf.set_font("uni", "", 10.5)
            pdf.set_text_color(25, 25, 25)
            pdf.set_x(20)
            pdf.multi_cell(0, 5.5, "•  " + text, align="L")
            pdf.ln(1)
        elif kind == "table":
            _table(pdf)

    _footer(pdf)
    pdf.output(_OUT)
    print(f"wrote {_OUT}  ({pdf.pages_count} pages)")


def _table(pdf: FPDF) -> None:
    widths = [58, 20, 20, 76]  # sum 174
    pdf.set_font("uni", "", 10)
    pdf.set_fill_color(20, 40, 90)
    pdf.set_text_color(255, 255, 255)
    for w, htxt in zip(widths, TABLE_HEADER):
        pdf.cell(w, 7, htxt, border=0, align="L", fill=True)
    pdf.ln(7)
    pdf.set_text_color(25, 25, 25)
    for row in TABLE_ROWS:
        pdf.set_fill_color(245, 246, 250)
        fill = row is TABLE_ROWS[1]  # highlight the learnability row lightly? keep simple
        for w, cell in zip(widths, row):
            pdf.cell(w, 6.5, cell, border=0, align="L", fill=fill)
        pdf.ln(6.5)
    pdf.ln(2)


def _footer(pdf: FPDF) -> None:
    for page in range(1, pdf.pages_count + 1):
        pdf.page = page  # fpdf2 exposes .page
        pdf.set_y(-14)
        pdf.set_font("uni", "", 8)
        pdf.set_text_color(140, 140, 140)
        pdf.cell(0, 5, f"github.com/robmitchellengineering-hub/pacland  ·  page {page}/{pdf.pages_count}", align="C")


if __name__ == "__main__":
    build()
