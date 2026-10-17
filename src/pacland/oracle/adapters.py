"""Adapters to existing public software (the oracle stack).

Each adapter wraps a real, pip-installable library with a *lazy* import, so the
rest of PACLAND never hard-depends on heavy physics packages. Method bodies are
illustrative scaffolds: confirm the exact third-party API names against the
linked documentation before first use — these adapters cannot be exercised here
because the libraries are not installed.
"""
from __future__ import annotations

import importlib


def require_package(module_name: str, pip_name: str, docs_url: str):
    """Import a third-party package lazily, failing with an actionable message."""
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise ImportError(
            f"{module_name!r} is required for this adapter. "
            f"Install it with: pip install {pip_name}\nDocs: {docs_url}"
        ) from exc


class CyToolsAdapter:
    """CYTools — Calabi-Yau topology (Hodge numbers, intersection numbers, c2).

    https://github.com/LiamMcAllisterGroup/cytools  (paper: arXiv:2211.03823)
    Maps to L1 encoding and L2 stage 2 (``docs/architecture.md``): polytope ->
    triangulation -> Hodge numbers, triple intersection numbers, second Chern class.

    Verified live on the harness-mesh `studio-linux` VM (CYTools 1.4.12), 2026-10-18:
    the quintic returns h11=1, h21=101 and c2 = [-250, 50, 50, 50, 50, 50].
    Flux-vacua search is NOT in CYTools 1.4.12 (checked the CY and Triangulation
    namespaces); it would need a different tool — see docs/tooling.md.
    """

    DOCS = "https://github.com/LiamMcAllisterGroup/cytools"
    LICENSE = "GPL-3.0 (copyleft — see docs/tooling.md)"

    def topology(self, polytope_points):
        """Return {h11, h21, intersection_numbers, second_chern_class}.

        Confirmed against CYTools 1.4.12: ``cy.h11()``, ``cy.h21()`` and
        ``cy.intersection_numbers()`` are methods; ``cy.second_chern_class`` is a
        property.
        """
        cytools = require_package("cytools", "cytools", self.DOCS)
        cy = cytools.Polytope(polytope_points).triangulate().get_cy()
        return {
            "h11": cy.h11(),
            "h21": cy.h21(),
            "intersection_numbers": cy.intersection_numbers(),
            "second_chern_class": cy.second_chern_class,
        }

    def fetch_polytopes(self, **kwargs):
        """Fetch reflexive polytopes from the Kreuzer-Skarke database."""
        cytools = require_package("cytools", "cytools", self.DOCS)
        return cytools.fetch_polytopes(**kwargs)


class CymetricAdapter:
    """cymetric — neural Calabi-Yau metrics.

    https://github.com/kitft/cymetric  (Larfors et al., "Learning the Size and
    Shape of Calabi-Yau Manifolds"). Maps to L2 stage 1 (the metric solve).
    """

    DOCS = "https://github.com/kitft/cymetric"

    def compute_metric(self, polytope_points, **kwargs):
        """Approximate a Ricci-flat CY metric. Illustrative; confirm API."""
        cymetric = require_package("cymetric", "cymetric", self.DOCS)
        # cymetric's flow: PointGenerator -> PhiModel (NN ansatz) -> train on the
        # Donaldson/Monge-Ampere loss. Wire it here.
        raise NotImplementedError(
            "scaffold: wire cymetric's PointGenerator/PhiModel training loop; "
            "confirm against " + self.DOCS
        )
