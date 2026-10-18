"""The physics oracle (L2) seam.

The ``Oracle`` protocol is the plug point for build #3 (the real physics oracle).
Adapters to existing public software (CYTools, cymetric) live in ``adapters``;
``exact_toric`` is a zero-error toy oracle that seeds build #2 (the
exact-background pipeline).
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from .adapters import CyToolsAdapter, CymetricAdapter, JaxVacuaAdapter, require_package
from .exact_toric import ToricBackground, exact_toric_oracle, zero_error_model


@runtime_checkable
class Oracle(Protocol):
    """A callable mapping a genotype to log-space observable values.

    ``docs/oracle.md`` §3. The real oracle (build #3) satisfies this protocol;
    so does the toy ``exact_toric_oracle``.
    """

    def __call__(self, genotype: object) -> dict[str, float]: ...


__all__ = [
    "Oracle",
    "ToricBackground",
    "exact_toric_oracle",
    "zero_error_model",
    "CyToolsAdapter",
    "CymetricAdapter",
    "JaxVacuaAdapter",
    "require_package",
]
