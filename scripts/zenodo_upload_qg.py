#!/usr/bin/env python3
import os, sys, json, urllib.request

TOKEN = os.environ.get("ZENODO_TOKEN")
if not TOKEN:
    sys.exit("set ZENODO_TOKEN=<token> first")
BASE = "https://zenodo.org/api"

METADATA = {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "Constraint-First Quantum Gravity, machine-checked: the unification is the constraint algebra",
    "creators": [{"name": "Mitchell, Rob"}],
    "description": (
        "Machine-checked (Lean 4 / Mathlib) constraint-first theory of quantum gravity. The forced "
        "content is the union of the Born rule (Gleason) and the Einstein equation (Lovelock), joined "
        "by the constraint ∇·T = 0, quantized as the Wheeler-DeWitt equation H|ψ⟩ = 0, and closed as "
        "the Dirac algebra. Three sharpened, falsifiable statements: SM minimality selects π₁ ≠ 0 (the "
        "(1,4) three-generation manifold is a Z₁₂ quotient, not toric; toric χ=±6 starts at h¹¹+h²¹=29); "
        "the coupling G is free (not derivable); the BMV entangling phase oscillates with period T=496 s, "
        "requiring < 0.1 K. Honest accounting of what is new (the certified chain + three statements) "
        "versus textbook (Lovelock, WdW, Dirac, Atiyah-Singer, BMV)."
    ),
    "keywords": ["quantum gravity", "constraint-first", "Wheeler-DeWitt", "Dirac algebra",
                "Born rule", "Lovelock", "BMV", "formal verification", "Lean"],
    "license": "cc-by-4.0",
    "access_right": "open",
}

def req(method, path, data=None, headers=None, files=None):
    url = BASE + path
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers: h.update(headers)
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
    with open("docs/papers/paper5-constraint-first-qg.md", "rb") as f:
        content = f.read()
    req("POST", f"/deposit/depositions/{dep_id}/files",
        files={"file": ("paper5-constraint-first-qg.md", content)})
    published = req("POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"PUBLISHED: {published.get('doi')}")

if __name__ == "__main__":
    raise SystemExit(main())
