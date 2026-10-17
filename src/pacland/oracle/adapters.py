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
    """CYTools — Calabi-Yau topology, cohomology, and flux vacua.

    https://github.com/LiamMcAllisterGroup/cytools  (paper: arXiv:2211.03823)
    Maps to L1 encoding and L2 stages 2-4 (``docs/architecture.md``): polytope ->
    triangulation -> Hodge numbers, intersection numbers, flux vacua.
    """

    DOCS = "https://github.com/LiamMcAllisterGroup/cytools"
    LICENSE = "GPL-3.0 (copyleft — see docs/tooling.md)"

    def topology(self, polytope_points):
        """Return {h11, h21, intersection_numbers} for a CY hypersurface.

        Confirmed against the CYTools README quick example:
        ``Polytope(points).triangulate().get_cy()`` → ``cy.h11()``, ``cy.h21()``.
        """
        cytools = require_package("cytools", "cytools", self.DOCS)
        cy = cytools.Polytope(polytope_points).triangulate().get_cy()
        return {
            "h11": cy.h11(),
            "h21": cy.h21(),
            "intersection_numbers": cy.intersection_numbers(),
        }

    def fetch_polytopes(self, **kwargs):
        """Fetch reflexive polytopes from the Kreuzer-Skarke database."""
        cytools = require_package("cytools", "cytools", self.DOCS)
        return cytools.fetch_polytopes(**kwargs)

    def flux_vacua(self, polytope_points, **kwargs):
        """Enumerate flux vacua of a CY hypersurface.

        Method name to be confirmed against cy.tools after install.
        """
        cytools = require_package("cytools", "cytools", self.DOCS)
        cy = cytools.Polytope(polytope_points).triangulate().get_cy()
        return cy.get_flux_vacua(**kwargs)


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
