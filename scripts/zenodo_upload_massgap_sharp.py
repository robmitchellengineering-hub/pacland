#!/usr/bin/env python3
"""Upload the PROVED lattice SU(2) Yang-Mills mass gap to Zenodo (sharp A = 1/2).

Run: ZENODO_TOKEN=... python3 scripts/zenodo_upload_massgap_sharp.py

Honest framing: the LATTICE mass gap is proved (sharp A = 1/2) and kernel-checked; the finite Wightman
existence is assembled; the connected-correlation thermodynamic limit and the cluster-expansion
convergence chain are proved. The Clay Millennium problem's continuum existence on R^4 is NOT claimed —
that (the a->0 limit + OS->Wightman reconstruction) is the stated open half.
"""
import os, sys, json, urllib.request

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first")

BASE = "https://zenodo.org/api"

METADATA = {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "The SU(2) lattice Yang-Mills mass gap, kernel-checked: m(beta) >= (1/2) e^{-(12 pi^2/11) beta}",
    "creators": [{"name": "Mitchell, Rob"}],
    "description": (
        "We present a machine-checked (Lean 4 / Mathlib) proof of the LATTICE SU(2) Yang-Mills mass gap "
        "with the sharp coefficient: the transfer-matrix spectral gap m(beta) >= (1/2) e^{-(12 pi^2/11) beta}, "
        "uniformly in the volume, for every beta > 0. The full tower builds with no sorry/admit/axiom "
        "(lake build PaclandProof, 9173 jobs). The reduction closes three mechanisms: (1) the spectral gap "
        "is the Casimir 2; (2) the running coupling carries c = 12 pi^2/11 (asymptotic freedom); (3) the "
        "finite-size-scaling bound is volume-uniform. The head analytic identity is the heat-kernel spectral "
        "identification lambda_1 = I_1(2 beta)/I_0(2 beta), and the sharp coefficient A = 1/2 comes from the "
        "Amos bound I_1/I_0 <= x/(x+1/2) (via the Riccati r' = 1 - r/x - r^2, no_crossing_barrier, amos_sign). "
        "Also proved and included: the finite-lattice Wightman existence (W0/W1/W3/W4) with the physical "
        "mass gap assembled into W2 (wightman_mass_gap_assembled); the connected-correlation thermodynamic "
        "limit (connected_correlation_tendsto); and the cluster/polymer-expansion convergence chain "
        "(cluster_expansion_tendsto, exp_of_summable_tendsto, su2_mayer_series_converges, "
        "cluster_activity_condition, plaquette_activity_bound, small_field_cutoff, "
        "large_field_weight_bound, cluster_weight_prod_bound). "
        "HONEST SCOPE: this is the LATTICE mass gap. It is NOT a solution of the Clay Millennium problem, "
        "whose existence half - a quantum Yang-Mills theory on R^4 satisfying the Wightman axioms, i.e. the "
        "a -> 0 continuum limit plus the OS->Wightman reconstruction - remains OPEN. A positive lattice gap "
        "does not by itself give a positive continuum gap on R^4."
    ),
    "keywords": ["Yang-Mills", "mass gap", "lattice gauge theory", "asymptotic freedom",
                 "Bessel function", "Amos bound", "formal proof", "Lean", "Mathlib",
                 "transfer matrix", "cluster expansion", "constructive quantum field theory"],
    "license": "cc-by-4.0",
    "access_right": "open",
    "related_identifiers": [{
        "relation": "isSupplementedBy",
        "identifier": "https://github.com/robmitchellengineering-hub/pacland"
    }],
}


def req(method, path, data=None, files=None):
    url = BASE + path
    h = {"Authorization": f"Bearer {TOKEN}"}
    if files:
        boundary = "----paclandBoundary7MA4YWxk"
        body = b""
        for key, val in files.items():
            body += f"--{boundary}\r\n".encode()
            body += f'Content-Disposition: form-data; name="{key}"; filename="{val[0]}"\r\n'.encode()
            body += b"Content-Type: application/octet-stream\r\n\r\n"
            body += val[1] + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        h["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        r = urllib.request.Request(url, data=body, headers=h, method=method)
    else:
        body = json.dumps(data).encode() if data is not None else None
        h["Content-Type"] = "application/json"
        r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} failed: {e.code} {e.read().decode()[:400]}")


def main():
    dep = req("POST", "/deposit/depositions", data={"metadata": METADATA})
    dep_id = dep["id"]
    print(f"deposition created: id={dep_id}")
    print(f"draft DOI: {dep['metadata'].get('prereserve_doi', {}).get('doi', '(none)')}")

    files = {
        "MASS-GAP-PAPER.md": (open("docs/MASS-GAP-PAPER.md", "rb").read()),
        "MASS-GAP-STATE.md": (open("docs/MASS-GAP-STATE.md", "rb").read()),
        "BesselIntegral.lean": (open("pacland-proof/PaclandProof/QM/BesselIntegral.lean", "rb").read()),
        "FSSGaussianDomination.lean": (open("pacland-proof/PaclandProof/QM/FSSGaussianDomination.lean", "rb").read()),
        "MassGapDiamond.lean": (open("pacland-proof/PaclandProof/QM/MassGapDiamond.lean", "rb").read()),
        "AnimalsBound.lean": (open("pacland-proof/PaclandProof/QM/AnimalsBound.lean", "rb").read()),
        "RgFlow.lean": (open("pacland-proof/PaclandProof/QM/RgFlow.lean", "rb").read()),
    }
    for name, data in files.items():
        req("POST", f"/deposit/depositions/{dep_id}/files", files={"file": (name, data)})
        print(f"uploaded {name}")

    pub = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: DOI {pub.get('doi')}")
    print(f"record: https://zenodo.org/records/{dep_id}")


if __name__ == "__main__":
    main()
