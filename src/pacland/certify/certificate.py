"""The certificate itself: findings, a grade, and the clause each finding answers.

The structure follows how model risk is actually supervised — the SR 11-7 concepts (conceptual
soundness, data quality, implementation, ongoing monitoring, outcomes analysis) and the PRA SS1/23
lifecycle — because a certificate that a supervisor cannot place is a certificate nobody uses.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

def _slug(text: str) -> str:
    keep = [c.lower() if c.isalnum() else "_" for c in text]
    out = "".join(keep)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")[:64]


SATISFIED = "satisfied"
PARTIAL = "partial"
NOT_DEMONSTRATED = "not demonstrated"
FAILING = "failing"

_ORDER = {SATISFIED: 3, PARTIAL: 2, NOT_DEMONSTRATED: 1, FAILING: 0}


@dataclass(frozen=True)
class Finding:
    clause: str
    question: str
    answer: str
    evidence: str
    status: str
    #: What a failure would have looked like. The Valiant Verification specification requires this
    #: field of every gate: "a gate that reports pass without evidence is a fail", and evidence of a
    #: *possible* failure is what separates a check from an assertion.
    falsifier: str = ""

    #: What to DO about it. Rob, 2026-10-28: "it's not just the verification, it's the analysis
    #: verification — and you keep forgetting to add a solution." A verdict without a remedy is a
    #: report; the leverage is in the fix.
    remedy: str = ""

    @property
    def gate(self) -> str:
        return _slug(f"{self.clause} {self.question}")

    @property
    def ok(self) -> bool:
        return self.status in (SATISFIED, PARTIAL)


@dataclass(frozen=True)
class Certificate:
    subject: str
    issuer: str
    issued: str
    findings: tuple[Finding, ...]
    headline: str
    limitations: tuple[str, ...]
    provenance: tuple[str, ...] = field(default_factory=tuple)
    sector: str = ""

    @property
    def grade(self) -> str:
        worst = min((_ORDER[f.status] for f in self.findings), default=0)
        if worst >= 3:
            return "VERIFIED"
        if worst >= 2:
            return "QUALIFIED"
        if worst == 1:
            return "RESTRICTED"
        return "REFUSED"

    @property
    def score(self) -> dict:
        counts = {k: 0 for k in _ORDER}
        for f in self.findings:
            counts[f.status] += 1
        return counts

    def to_markdown(self) -> str:
        lines = [f"# Model risk certificate — {self.subject}", "",
                 f"**Issued:** {self.issued}  ", f"**Issuer:** {self.issuer}  ",
                 f"**Grade:** **{self.grade}**", "", self.headline, "",
                 "| clause | question | what the evidence says | status |",
                 "|---|---|---|---|"]
        for f in self.findings:
            lines.append(f"| {f.clause} | {f.question} | {f.answer} | **{f.status}** |")
        lines += ["", "## Evidence", ""]
        lines += [f"- {e}" for e in self.provenance]
        lines += ["", "## Limitations", ""]
        lines += [f"- {l}" for l in self.limitations]
        lines += ["", f"_{len(self.findings)} findings: "
                      + ", ".join(f"{v} {k}" for k, v in sorted(self.score.items()) if v) + "._"]
        return "\n".join(lines) + "\n"

    def to_dict(self) -> dict:
        return {"subject": self.subject, "sector": self.sector, "issuer": self.issuer,
                "issued": self.issued,
                "grade": self.grade, "headline": self.headline,
                "score": self.score,
                "findings": [f.__dict__ for f in self.findings],
                "limitations": list(self.limitations),
                "provenance": list(self.provenance)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    # ---------------------------------------------------------------------------------
    # the Valiant Verification certificate format (spec.md §3, the named-gate contract)
    # ---------------------------------------------------------------------------------
    @property
    def vvs_gates(self) -> list[dict]:
        """One named gate per finding: name, result, evidence, producer, falsifier."""
        return [{
            "gate": f.gate,
            "clause": f.clause,
            "result": "pass" if f.ok else "fail",
            "evidence": f.answer,
            "evidence_path": f.evidence,
            "producer": self.producer,
            "falsifier": f.falsifier or _default_falsifier(f),
            "remedy": f.remedy or _default_remedy(f),
        } for f in self.findings]

    @property
    def producer(self) -> str:
        return "; ".join(self.provenance) if self.provenance else self.issuer

    def to_vvs(self) -> dict:
        """The certificate in the shape the VVS specification defines."""
        gates = self.vvs_gates
        n_pass = sum(1 for g in gates if g["result"] == "pass")
        return {
            "format": "valiant-verification/named-gate@1",
            "subject": self.subject,
            "sector": self.sector,
            "issuer": self.issuer,
            "issued": self.issued,
            "grade": self.grade,
            "gates_required": len(gates),
            "gates_passed": n_pass,
            "verified": n_pass == len(gates) and self.grade in ("VERIFIED", "QUALIFIED"),
            "gates": gates,
            "limitations": list(self.limitations),
        }

    def to_vvs_markdown(self) -> str:
        v = self.to_vvs()
        lines = [f"# Valiant Verification certificate — {v['subject']}", "",
                 f"**Format:** `{v['format']}`  ",
                 f"**Issuer:** {v['issuer']}  ",
                 f"**Issued:** {v['issued']}  ",
                 f"**Grade:** **{v['grade']}**  ",
                 f"**Gates:** {v['gates_passed']} of {v['gates_required']} pass  ",
                 f"**Verified:** {'yes' if v['verified'] else 'no'}", "",
                 "| gate | result | evidence | falsifier | remedy |",
                 "|---|---|---|---|---|"]
        for g in v["gates"]:
            lines.append(f"| `{g['gate']}` | **{g['result']}** | {g['evidence']} | {g['falsifier']} "
                         f"| {g['remedy']} |")
        lines += ["", "**Producer:** " + self.producer, "", "## Limitations", ""]
        lines += [f"- {l}" for l in self.limitations]
        return "\n".join(lines) + "\n"


def _default_remedy(f: Finding) -> str:
    """Every gate carries an action, even when the action is "none required"."""
    if f.ok:
        return "none — the check passes; keep the evidence and re-run on change"
    return "fix the failing check before relying on this claim; the falsifier names what to repair"


def _default_falsifier(f: Finding) -> str:
    """If a finding does not name its own falsifier, say so rather than inventing one.

    The specification calls a pass without a falsifier a weak pass; printing the gap is more honest
    than filling it with a sentence that sounds like a check.
    """
    return ("not stated — this finding records a measurement without naming the failure it rules out"
            if f.ok else "the failure is the finding")


__all__ = ["Certificate", "Finding", "SATISFIED", "PARTIAL", "NOT_DEMONSTRATED", "FAILING"]
