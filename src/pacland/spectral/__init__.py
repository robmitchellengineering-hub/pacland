"""Spectral checks: where a number-theoretic object has a measurable spectrum.

The one lead worth chasing from Jason Padgett's "prime oscillations": the honest version of that idea
is the explicit formula, where the primes are an interference sum over the *Riemann zeros*. That is a
real spectral structure, and its spacing statistics are a cross-source check we can run ourselves.
"""
from __future__ import annotations

__all__ = ["zeros"]
