"""Learnability measurement rig (build #4).

Tools to estimate the VC dimension of a hypothesis class and to sample the search
space. The physics oracle (build #3) plugs in later through the label-callable
interface; until then, tests use synthetic concept classes with known VC dimension.
"""
from __future__ import annotations

from .sampler import Vacuum, sample_flux_vacua
from .vc import (
    finite_class_radius,
    pseudo_dim_lower_bound,
    pseudo_shatters,
    sample_complexity,
    shatters,
    vc_lower_bound,
)

__all__ = [
    "shatters",
    "vc_lower_bound",
    "sample_complexity",
    "finite_class_radius",
    "pseudo_shatters",
    "pseudo_dim_lower_bound",
    "Vacuum",
    "sample_flux_vacua",
]
