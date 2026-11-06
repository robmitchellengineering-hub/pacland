#!/usr/bin/env python3
"""Zenodo upload for the two SM proof-arm papers. Run:  ZENODO_TOKEN=... python3 scripts/zenodo_upload_sm.py

Uploads the two markdown papers as preprints, publishes them (minting DOIs), and prints the DOIs.
Requires a Zenodo personal access token with `deposit:write` scope (https://zenodo.org/account/settings/applications/).
"""
import os, sys, json, urllib.request, urllib.parse

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first (deposit:write scope)")

BASE = "https://zenodo.org/api"

PAPERS = [
    {
        "filename": "docs/papers/paper1-machine-checked-foundations.md",
        "metadata": {
            "upload_type": "preprint",
            "title": "Machine-checked foundations of quantum theory and the Standard Model: Gleason's theorem and the gauge-sector uniqueness, kernel-checked in Lean 4",
            "creators": [{"name": "Mitchell, Rob"}],
            "description": (
                "Machine-checked (Lean 4 / Mathlib) certificates for two foundational results. "
                "(1) Gleason's theorem (finite, dim>=3): every non-contextual additive probability on "
                "projectors is the Born rule Tr(rho P), proven via the Cooke-Keane-Moran descent-chain "
                "route (no continuity needed). (2) The Standard Model gauge-sector uniqueness: the "
                "anomaly-cancellation conditions force the hypercharges uniquely up to normalization and "
                "the u<->d swap, and the five anomaly coefficients vanish for (1/6, 2/3, -1/3, -1/2, -1). "
                "Zero sorry/axiom; #print axioms = propext, Classical.choice, Quot.sound only."
            ),
            "keywords": ["formal verification", "Lean", "Gleason's theorem", "Born rule",
                        "Standard Model", "anomaly cancellation", "hypercharge"],
            "license": "cc-by-4.0",
            "access_right": "open",
        },
    },
    {
        "filename": "docs/papers/paper2-flavor-invariant-ring.md",
        "metadata": {
            "upload_type": "preprint",
            "title": "The Standard Model flavor invariant ring: an independent Molien-Weyl computation confirming Bento-Silva-Trautner",
            "creators": [{"name": "Mitchell, Rob"}],
            "description": (
                "We recompute the Hilbert series of the SM quark-sector flavor invariant ring by the "
                "Molien-Weyl formula (torus constant-term + Weyl averaging), independently of the "
                "literature. For two 3x3 matrices under U(3): H(t) = (1-t^12)/((1-t)^2(1-t^2)^3(1-t^3)^4"
                "(1-t^4)(1-t^6)), i.e. 10 CP-even primary + 1 CP-odd secondary (Jarlskog) invariant. For "
                "the SM Yukawa sector H_Y(t) = (1-t^24)/((1-t^2)^3(1-t^4)^4(1-t^6)^5(1-t^8)(1-t^12)), "
                "Krull dimension 13. Agrees with Bento-Silva-Trautner (arXiv:2308.00019); adds the GUT "
                "dimension drop 19 -> 14 (SU(5)) -> 7 (SO(10))."
            ),
            "keywords": ["Standard Model", "flavor", "invariant theory", "Hilbert series",
                        "Molien-Weyl", "CKM", "Jarlskog invariant"],
            "license": "cc-by-4.0",
            "access_right": "open",
        },
    },
]


def req(method, path, data=None, headers=None, files=None):
    url = BASE + path
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers:
        h.update(headers)
    if files:
        # multipart upload
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


def upload(paper):
    dep = req("POST", "/deposit/depositions", data={"metadata": paper["metadata"]})
    dep_id = dep["id"]
    with open(paper["filename"], "rb") as f:
        content = f.read()
    req("POST", f"/deposit/depositions/{dep_id}/files",
        files={"file": (os.path.basename(paper["filename"]), content)})
    published = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    return published.get("doi")


def main():
    for p in PAPERS:
        doi = upload(p)
        print(f"PUBLISHED: {doi}  <- {p['metadata']['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
