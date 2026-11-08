#!/usr/bin/env python3
"""Upload the QM falsification paper to Zenodo. Run: ZENODO_TOKEN=... python3 scripts/zenodo_upload_qm.py"""
import os, sys, json, urllib.request

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first")

BASE = "https://zenodo.org/api"

METADATA = {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "Machine-checked falsification of quantum foundations: Bell, Tsirelson, no-cloning, and Kochen-Specker in Lean 4",
    "creators": [{"name": "Mitchell, Rob"}],
    "description": (
        "Machine-checked (Lean 4 / Mathlib) certificates for the main falsification results of "
        "quantum foundations. Bell's theorem: the CHSH correlation satisfies S <= 2 for local hidden "
        "variables, in both the deterministic +/-1 form and the general local-realism form |a|,|b| <= 1. "
        "The Tsirelson bound: QM saturates S = 2*sqrt(2), so locality is violated. No-cloning: v -> v tensor v "
        "is not linear. Kochen-Specker: no non-contextual 0/1 value assignment in dimension >= 3 (the "
        "no_dispersion_free corollary of Gleason). Zero sorry/axiom; #print axioms = propext, Classical.choice, "
        "Quot.sound only."
    ),
    "keywords": ["quantum foundations", "Bell's theorem", "Tsirelson bound", "no-cloning",
                "Kochen-Specker", "formal verification", "Lean"],
    "license": "cc-by-4.0",
    "access_right": "open",
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
    with open("docs/papers/paper3-quantum-falsification.md", "rb") as f:
        content = f.read()
    req("POST", f"/deposit/depositions/{dep_id}/files",
        files={"file": ("paper3-quantum-falsification.md", content)})
    published = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: {published.get('doi')}")


if __name__ == "__main__":
    raise SystemExit(main())
