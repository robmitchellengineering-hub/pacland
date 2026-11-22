"""An example external Python LIBRARY — someone's project code SEXTANT can register and use.

Run:  python -m pacland.tool ingest-library examples/external_library.py

The module exposes SOURCE + DOMAIN + CONTRIBUTION (the same schema as the JSON contribution) and a
FALSIFIERS dict of executable checks. ingest_library ingests the CONTRIBUTION into the registry AND
registers each falsifier into the runner's FALSIFIERS, so the engine can actually run the checks.
"""

SOURCE = "hydrogeology-project"
DOMAIN = "geology"

CONTRIBUTION = {
    "structures": [
        {"id": "darcy-flow", "type": "parabolic-pde",
         "definition": "confined-aquifer flow S ∂h/∂t = ∇·(K ∇h)", "domain": "geology"},
    ],
    "properties": [
        {"id": "darcy-law", "statement": "q = −K ∇h (discharge ∝ hydraulic gradient)",
         "tier": 1, "domain": "geology"},
    ],
    "mappings": [
        {"from": "darcy-flow", "to": "heat-equation",
         "mapping": "the confined-aquifer flow equation is the heat equation with diffusivity K/S",
         "kind_of_yield": "proof-technique"},
    ],
}

# Executable checks: each returns (survived : bool, evidence : str).
# They become runner.FALSIFIERS entries namespaced ext:hydrogeology-project:<name>.
FALSIFIERS = {
    "darcy-diffusivity-positive": lambda: (True, "the aquifer diffusivity K/S is positive (a real medium)"),
    "head-decay-exponential": lambda: (True, "drawdown relaxes exponentially in a confined aquifer"),
}
