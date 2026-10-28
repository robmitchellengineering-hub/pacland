"""The certificate itself: findings, a grade, and the clause each finding answers.

The structure follows how model risk is actually supervised — the SR 11-7 concepts (conceptual
soundness, data quality, implementation, ongoing monitoring, outcomes analysis) and the PRA SS1/23
lifecycle — because a certificate that a supervisor cannot place is a certificate nobody uses.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

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
        return {"subject": self.subject, "issuer": self.issuer, "issued": self.issued,
                "grade": self.grade, "headline": self.headline,
                "score": self.score,
                "findings": [f.__dict__ for f in self.findings],
                "limitations": list(self.limitations),
                "provenance": list(self.provenance)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


__all__ = ["Certificate", "Finding", "SATISFIED", "PARTIAL", "NOT_DEMONSTRATED", "FAILING"]
