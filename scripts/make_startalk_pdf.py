#!/usr/bin/env python3
"""Generate the PACLAND StarTalk-style explainer PDF (repo root).

Same visual theme as make_explainer_pdf.py (fpdf2 + Arial Unicode, blue headings,
numbered sections, table, footer) but written in a Neil deGrasse Tyson / StarTalk
voice: what it means, why it matters, and what it could do for researchers.

Requires fpdf2:  python3 -m pip install --user fpdf2
"""
import os

from fpdf import FPDF

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "PACLAND-startalk.pdf")

# (kind, text) — kinds: title, subtitle, h (section), p (paragraph), b (bullet), table
C = [
    ("title", "PACLAND"),
    ("subtitle", "Why the smartest theory in physics can't tell us where we are — and the surprising thing we learned by asking it to show its work. (A StarTalk-style brief for the curious, not the credentialed.)"),

    ("h", "1 · The universe handed us a menu with 10⁵⁰⁰ dishes"),
    ("p", "String theory is our best shot at a \"theory of everything.\" And here is the part nobody puts on the poster: it does not describe one universe. It describes about 10⁵⁰⁰ of them — a 1 followed by 500 zeros, more universes than there are atoms in our own. Each one has its own particles, its own forces, its own version of the laws of nature. Physicists call this the \"landscape.\""),
    ("p", "So \"unified string theory\" is not one question. It is two, and we keep smashing them together:"),
    ("b", "Verification — is there a universe on that menu that matches the one we actually live in?"),
    ("b", "Selection — why THAT one, and not one of the other 10⁵⁰⁰?"),
    ("p", "The first one is hard. The second one has been open for forty years. And you cannot solve the second by pretending you are solving the first."),

    ("h", "2 · The move we borrowed from a computer scientist"),
    ("p", "Enter Leslie Valiant, a computer scientist who asked a very Neil-ish question: when you cannot know something exactly, what can you honestly say? His answer, from 1984, became the field of PAC learning — \"probably approximately correct.\""),
    ("p", "The idea is beautiful in its honesty. You do not say \"this is right.\" You say: \"with confidence at least 1−δ, this is right to within ε.\" Two numbers, one promise — and you can actually compute those numbers."),
    ("p", "PACLAND is what happens when you point that at string theory. Instead of the impossible \"prove this vacuum is our universe,\" we ask the checkable version:"),
    ("p", "\"Certify that this candidate's physics matches what we observe, within a tolerance ε, with confidence δ.\""),
    ("p", "That is a certificate — a birth certificate for a universe — and it is the kind of thing you can build and test."),

    ("h", "3 · So we built it — and the universe talked back"),
    ("p", "We did not just write documents. We built a verification library (pure Python) that computes the certificate, a learnability rig that measures how hard the landscape is to \"learn,\" and we wired in the real string-theory tools — CYTools and JAXVacua — and ran them for real: 380 actual flux vacua, sampled on a real machine."),
    ("p", "Then the numbers came back. Three of them knocked us over."),

    ("h", "4 · The three \"wait, what?\" results"),
    ("p", "Result 1 — the search cannot work. (A negative result, and the best kind.)"),
    ("p", "We measured the flux superpotential W₀ — the number that picks the vacuum — across 380 real vacua. Its distribution came out log-uniform: a straight line on a log plot, R² = 0.92. That means the map from \"the geometry you chose\" to \"the number that matters\" carries essentially zero information. And by Valiant's own theorem — anything evolvable must be learnable — a zero-information map cannot be learned, so no evolutionary search can ever converge on it. The search dies. The verifier survives. That is a citable result about the whole program: stop building faster searches for W₀; it is provably not there."),
    ("p", "Result 2 — right now, string theory is barely verifiable at all."),
    ("p", "Our certificate's binding limit is a single number, m: the count of observables that are simultaneously measured (we know the real answer), computable (our tools can predict it), and validated (we have checked the tools against reality). Here is the gut punch: that intersection is empty today. m = 0. We can measure our universe, but we do not know which compactification it came from; we can compute exact backgrounds, but they are not our universe. With m = 0 the certificate radius is infinite — it certifies nothing. That is not failure; that is a measurement. It tells you exactly what to go build: the missing oracles."),
    ("p", "Result 3 — \"uncomputable\" is a map, not a wall."),
    ("p", "We wanted to know where computation ends, so we classified the ways a problem can be impossible — and then certified seven of our open questions against that map. The table is the map:"),
    ("table", None),
    ("p", "Not one of them is undecidable. That is the headline: string theory's wall is not a Turing limit. It is a shortage of oracles and a surplus of underdetermination. Which means the path forward is not \"invent a faster computer.\" It is \"build the missing instruments\" and \"compute the invariants of the set of possibilities.\" That is doable — and it is where the field is already heading."),

    ("h", "5 · Why any of this matters to you (yes, you)"),
    ("p", "You will probably never compute a flux vacuum. But you have absolutely met this problem before: a search space too big to scan, no ground truth, and a claim nobody can check. That is an AI model you cannot fully test. That is a codebase too large to verify. That is a prediction you cannot falsify."),
    ("p", "The three moves we used are portable:"),
    ("b", "When you cannot prove, certify. Swap \"it is correct\" for \"it is correct within ε, with confidence δ\" — and compute what that actually costs."),
    ("b", "Separate verification from selection. \"Does it match?\" and \"why was it chosen?\" are different questions. Fusing them is how projects stall for forty years."),
    ("b", "Name what is uncomputable. Saying \"this part cannot be brute-forced\" is not surrender — it is the map that tells you where effort will actually pay."),

    ("h", "6 · What this could do for researchers"),
    ("p", "This is the part that should make a theorist sit up. Independently of us, the field is converging on exactly the gap we built into. Michael Douglas — the landscape's leading statistician — is formalizing quantum field theory in the Lean proof assistant. PhysProver is the first AI theorem-prover trained for physics. A 2025 line is formalizing how to falsify string theory at a collider. Everyone is circling the same hole: the theory has no verification layer."),
    ("p", "What PACLAND hands them is a template:"),
    ("b", "A negative result that saves careers — proof that some searches provably cannot converge, so funding and grad students stop chasing them."),
    ("b", "A measured prior (log-uniform W₀) they can cite instead of assume."),
    ("b", "A boundary map that turns \"impossible\" into a to-do list."),
    ("b", "A certificate framework that generalizes to any approximate computation — climate models, fusion simulations, AI systems — anywhere the verifier is itself imperfect."),
    ("p", "We did not solve string theory, and we did not claim to. We built the missing verification layer and measured the size of the hole. In a field where \"the theory has no way to check itself\" was the unspoken problem, that is not a small thing. That is the difference between believing and knowing."),

    ("h", "7 · The cosmic bottom line"),
    ("p", "String theory has spent forty years trying to win a lottery it could not even describe. We changed the bet. We cannot yet tell you which universe is ours — but we can now tell you, with numbers, why nobody else could either, exactly where the wall is, and what to go build to move it."),
    ("p", "The universe does not owe us an answer. But it does respond to better questions. Stay curious."),
]

TABLE_HEADER = ["Sense", "What it means", "The move"]
TABLE_ROWS = [
    ["intractable", "an answer exists, no feasible algorithm", "prove intractability"],
    ["unmeasurable", "an answer exists, data / ground truth absent", "compute the deficit"],
    ["underdetermined", "no unique answer exists", "compute the set's invariants"],
    ["undecidable", "provably no algorithm", "prove undecidability"],
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
    widths = [44, 76, 54]  # sum 174
    pdf.set_font("uni", "", 10)
    pdf.set_fill_color(20, 40, 90)
    pdf.set_text_color(255, 255, 255)
    for w, htxt in zip(widths, TABLE_HEADER):
        pdf.cell(w, 7, htxt, border=0, align="L", fill=True)
    pdf.ln(7)
    pdf.set_text_color(25, 25, 25)
    for i, row in enumerate(TABLE_ROWS):
        pdf.set_fill_color(245, 246, 250)
        fill = (i % 2 == 1)
        for w, cell in zip(widths, row):
            pdf.cell(w, 6.5, cell, border=0, align="L", fill=fill)
        pdf.ln(6.5)
    pdf.ln(2)


def _footer(pdf: FPDF) -> None:
    for page in range(1, pdf.pages_count + 1):
        pdf.page = page
        pdf.set_y(-14)
        pdf.set_font("uni", "", 8)
        pdf.set_text_color(140, 140, 140)
        pdf.cell(0, 5, f"github.com/robmitchellengineering-hub/pacland  ·  page {page}/{pdf.pages_count}", align="C")


if __name__ == "__main__":
    build()
