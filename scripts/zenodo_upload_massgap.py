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
        "A verified MAP of the 4D Yang-Mills mass-gap problem, not a solution. Three anchors. "
        "(1) The strong-coupling mass gap (d >= 2) is PROVEN by Douglas-Rajasekaran's LGT library: "
        "ym_mass_gap_exponential_decay and ym_mass_gap_rate_exists, zero sorries, #print axioms = "
        "{propext, Classical.choice, Quot.sound}, independently FRO-kernel-verified - cited, not our "
        "result. (2) The existence half is CLAIMED by the yang-mills-group/OpenAI-YM-20261028 Lean "
        "construction (an AI-made proof the Gross committee reports checks in Lean but does not fully "
        "understand); our fidelity audit finds two weakenings: the public running slope is unpinned "
        "(the proof's internal slopeConstant = 11 casimir / 24 pi^2 is not surfaced), and the continuum "
        "limit is subsequence-only and non-unique. (3) We kernel-check the Casimir -> Faddeev-Popov "
        "constant-mode gap -> positive-semidefinite transport chain, MODEL the Gribov IR suppression "
        "(M(p) = p^2 chosen, not derived), and FALSIFY the single-scale geometric route (the bare Wilson "
        "Hessian beta cos theta is negative at the antipode) with its multiscale toy fix. The open "
        "content is the TWO located rungs: the Polchinski-equation multiscale Bakry-Emery criterion for "
        "gauge theory (the crossover) and the mass gap itself (spectral support away from 0). No "
        "mass-gap theorem is claimed."
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
        req("POST", f"/deposit/depositions/{dep_id}/files", files={"file": (name, data)})
        print(f"uploaded {name}")

    # publish
    pub = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: DOI {pub.get('doi')}")
    print(f"record: https://zenodo.org/records/{dep_id}")


if __name__ == "__main__":
    main()
