#!/usr/bin/env python3
import os, sys, json, urllib.request

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first")
BASE = "https://zenodo.org/api"

METADATA = {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "Constraint-First Unification, machine-checked: the exact content of a theory of everything is constraints, labels, and parameters",
    "creators": [{"name": "Mitchell, Rob"}],
    "description": (
        "Machine-checked (Lean 4 / Mathlib) forced/free split across all four sectors of physics. "
        "The Born rule is the unique non-contextual probability rule (Gleason); the SM hypercharges are "
        "forced by anomaly cancellation (N_gen free); the flux tadpole is the unique duality invariant "
        "(Mitchell/FFT); the Einstein equation is the unique divergence-free theory (Lovelock). The "
        "measurement problem and 'why these 19' are provably the free column. Falsifiable: a hidden "
        "symmetry fixing the 19, a second divergence-free gravity theory, or a non-contextual "
        "deterministic completion of QM would each kill it. Zero sorry/axiom."
    ),
    "keywords": ["constraint-first", "unification", "Born rule", "Standard Model", "Lovelock",
                "invariant theory", "formal verification", "Lean"],
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
    with open("docs/papers/paper4-constraint-first-unification.md", "rb") as f:
        content = f.read()
    req("POST", f"/deposit/depositions/{dep_id}/files",
        files={"file": ("paper4-constraint-first-unification.md", content)})
    published = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: {published.get('doi')}")


if __name__ == "__main__":
    raise SystemExit(main())
