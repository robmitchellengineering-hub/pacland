"""The discipline registry — each discipline is its own thing within PACLAND.

The string landscape is the founding discipline; every expansion (climate, drug
discovery, epidemiology, AI safety, ...) is a *discipline* with its own
subpackage, its own docs, and its own CLI command — all sharing the one
verification spine (two-level certificate, verification deficit, constraint-first,
the four-walls map). This module is the single source of truth both the CLI and
the site read from, so a new discipline is added here, not hard-coded in two places.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Discipline:
    slug: str
    name: str
    status: str
    package: str | None   # python subpackage under pacland; None = not built yet
    docs: str             # primary doc (repo-relative) or "—"
    blurb: str


DISCIPLINES: tuple[Discipline, ...] = (
    Discipline(
        slug="landscape",
        name="String landscape",
        status="core (built)",
        package="pacland",
        docs="docs/",
        blurb="The founding discipline: PAC verification of the flux landscape and the Standard Model.",
    ),
    Discipline(
        slug="climate",
        name="Climate / Earth-system",
        status="built — deficit + guard-suite",
        package="pacland.climate",
        docs="docs/climate-verification-deficit.md",
        blurb="m = 4 on the historical record (≈68% radius), m = 0 for 2100 projections — extrapolation, not verification.",
    ),
    Discipline(
        slug="drugs",
        name="Drug discovery / protein science",
        status="built — deficit + guard-suite",
        package="pacland.drugs",
        docs="docs/drugs-verification-deficit.md",
        blurb="Chemical space as a landscape; falsification guards over docking and folding predictions.",
    ),
    Discipline(
        slug="epi",
        name="Epidemiology / disease modelling",
        status="queued",
        package=None,
        docs="—",
        blurb="The identifiability problem as the underdetermined wall.",
    ),
    Discipline(
        slug="ai",
        name="Valiant Verification (software & AI)",
        status="the verified-badge lane",
        package=None,
        docs="docs/ai-verified-badge.md",
        blurb="The SDK applied to repos and models — the badge is the product.",
    ),
)

__all__ = ["Discipline", "DISCIPLINES"]
