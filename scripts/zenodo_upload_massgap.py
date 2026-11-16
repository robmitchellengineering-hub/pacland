#!/usr/bin/env python3
"""Upload the Yang-Mills mass-gap reduction paper to Zenodo.

Run: ZENODO_TOKEN=... python3 scripts/zenodo_upload_massgap.py

Honest framing: a methods + formalization + negative-results record, NOT a claim of the mass gap.
"""
import os, sys, json, urllib.request

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first")

BASE = "https://zenodo.org/api"

METADATA = {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "A falsifier-first, kernel-checked reduction of the Yang-Mills mass gap to the Gribov-Zwanziger horizon condition",
    "creators": [{"name": "Mitchell, Rob"}],
    "description": (
        "We present a machine-checked (Lean 4 / Mathlib) reduction of the 4D SU(2) Yang-Mills mass-gap "
        "problem to a single named statement: the positivity of the dimensionless ratio m/Lambda "
        "(equivalently m/sqrt(sigma) ~ 3.2), uniformly in the volume. The exponential e^{-c beta} is "
        "identified as the known one-loop beta function (Gross-Wilczek-Politzer), not the open content. "
        "Against a lattice referee (m(beta) = 25.28 e^{-1.182 beta}, m/sqrt(sigma) ~ 3.2) we falsify the "
        "candidate mechanisms that fail - the plaquette concentration (power law 1/beta), the cluster "
        "expansion (log beta), the Dobrushin coupling (dies), and the chessboard surface-tension bound "
        "(circular) - and we prove, kernel-checked with no sorry, the finite-dimensional Gribov-Zwanziger "
        "confinement mechanism: non-commutativity -> Cartan zero mode -> IR suppression G(0)=0 -> the "
        "1/p^4 singularity -> the linear Coulomb potential. We correct an earlier step by showing the "
        "Casimir mass is deconfining (Yukawa) while the IR suppression is the confining mechanism. "
        "We do NOT prove the mass gap. The remaining rung - the infinite-dimensional horizon condition "
        "(gamma > 0 for the full Faddeev-Popov operator) - is stated precisely and left open. This paper "
        "proves no new bound and no new theorem about the mass gap; it contributes a verified map of the "
        "problem, not a solution."
    ),
    "keywords": ["Yang-Mills", "mass gap", "asymptotic freedom", "Gribov-Zwanziger",
                 "Coulomb confinement", "formal proof", "Lean", "Mathlib", "transfer matrix",
                 "falsification"],
    "license": "cc-by-4.0",
    "access_right": "open",
    "related_identifiers": [{
        "relation": "isSupplementedBy",
        "identifier": "https://github.com/robmitchellengineering-hub/pacland"
    }],
}


def req(method, path, data=None, headers=None, files=None):
    url = BASE + path
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers:
        h.update(headers)
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

    # upload the four proof/record files
    files = {
        "MassGapDiamond.lean": (open("pacland-proof/PaclandProof/QM/MassGapDiamond.lean", "rb").read()),
        "GradientFlow.lean": (open("pacland-proof/PaclandProof/QM/GradientFlow.lean", "rb").read()),
        "MASS-GAP-METHODS.md": (open("docs/MASS-GAP-METHODS.md", "rb").read()),
        "ZENODO-PAPER.md": (open("docs/ZENODO-PAPER.md", "rb").read()),
    }
    for name, data in files.items():
        req("POST", f"/deposit/depositions/{dep_id}/files", files={name: (name, data)})
        print(f"uploaded {name}")

    # publish
    pub = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: DOI {pub.get('doi')}")
    print(f"record: https://zenodo.org/records/{dep_id}")


if __name__ == "__main__":
    main()
