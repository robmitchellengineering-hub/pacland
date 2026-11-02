"""The check half of the certificate set: hashes, a signature, and reproducibility.

The manifest has always recorded a sha256 per artifact. Until now nothing checked the hash, and
nothing bound the manifest to an issuer — the same script wrote the hash and then called it
evidence. This module is the other half:

* an artifact on disk must match the hash the manifest records for it;
* the manifest must carry an OpenSSH signature that verifies against a published key;
* a fresh issue of every certificate must reproduce the committed bytes.

Verification is offline by construction. ``ssh-keygen -Y verify`` reads three local files — the
manifest, its ``.sig``, and ``allowed_signers`` — and needs no network, no account, and no trust in
whatever served them. That is the difference between a certificate and a memo.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

#: SSHSIG namespace. A signature made for another purpose must not verify here.
NAMESPACE = "vvs"
#: The principal the allowed_signers file grants this namespace to.
PRINCIPAL = "vvs@pacland"

SIG_NAME = "MANIFEST.json.sig"
SIGNERS_NAME = "allowed_signers"
MANIFEST_NAME = "MANIFEST.json"
MANIFEST_FORMAT = "valiant-verification/manifest@1"

CERT_DIR = Path("certificates") / "vvs"
WEB_DIR = Path("web") / "vvs"

#: Files a fresh issue writes. The signature and allowed_signers are attestation, not generated
#: content, and are deliberately excluded: a fresh issue cannot produce a signature it did not make.
GENERATED_SUFFIXES = (".json", ".md")


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def sha256_file(path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def _ssh_keygen() -> str | None:
    return shutil.which("ssh-keygen")


def verify_signature(manifest_bytes: bytes, sig_path, signers_path,
                     principal: str = PRINCIPAL, namespace: str = NAMESPACE) -> tuple[bool, str]:
    """Verify ``manifest_bytes`` against an SSHSIG file. Returns ``(ok, message)``.

    Offline: three local files and the ``ssh-keygen`` binary. A missing signature is a failure, not
    a skip — a certificate set without one is the state this module exists to end.
    """
    sig_path, signers_path = Path(sig_path), Path(signers_path)
    for path, what in ((sig_path, "signature"), (signers_path, "allowed_signers")):
        if not path.is_file():
            return False, f"missing {what}: {path}"
    keygen = _ssh_keygen()
    if keygen is None:
        return False, "ssh-keygen not found — offline verification needs OpenSSH"
    proc = subprocess.run(
        [keygen, "-Y", "verify", "-f", str(signers_path), "-I", principal,
         "-n", namespace, "-s", str(sig_path)],
        input=manifest_bytes, capture_output=True,
    )
    if proc.returncode != 0:
        out = (proc.stderr or proc.stdout).decode("utf-8", "replace").strip().splitlines()
        return False, (out[-1] if out else f"ssh-keygen exited {proc.returncode}")
    return True, f"signature verifies ({principal}, namespace {namespace})"


def load_manifest(path) -> dict:
    return json.loads(Path(path).read_text())


def verify_artifacts(root, manifest: dict) -> list[str]:
    """Every artifact named in the manifest must be present and match its recorded hash."""
    problems: list[str] = []
    cert = Path(root) / CERT_DIR
    for name, rec in sorted(manifest.get("artifacts", {}).items()):
        path = cert / f"{name}.json"
        if not path.is_file():
            problems.append(f"{name}: artifact missing ({path})")
            continue
        got = sha256_file(path)
        want = rec.get("sha256")
        if got != want:
            problems.append(f"{name}: hash mismatch — manifest {str(want)[:12]}…, file {got[:12]}…")
    return problems


def verify_set(root) -> dict:
    """Verify a whole certificate set. Returns ``{"ok", "checks", "failures"}``.

    ``checks`` is every check performed in order, ``(ok, message)``, so a caller can show what was
    and was not tested rather than only the verdict.
    """
    root = Path(root)
    cert = root / CERT_DIR
    checks: list[tuple[bool, str]] = []
    failures: list[str] = []

    def check(ok: bool, message: str) -> None:
        checks.append((ok, message))
        if not ok:
            failures.append(message)

    manifest_path = cert / MANIFEST_NAME
    if not manifest_path.is_file():
        check(False, f"manifest missing: {manifest_path}")
        return {"ok": False, "checks": checks, "failures": failures}

    blob = manifest_path.read_bytes()
    check(True, f"manifest present ({len(blob)} bytes, sha256 {sha256_bytes(blob)[:12]}…)")

    ok, why = verify_signature(blob, cert / SIG_NAME, cert / SIGNERS_NAME)
    check(ok, f"signature: {why}")

    try:
        manifest = json.loads(blob.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 — any parse failure is the same finding
        check(False, f"manifest is not valid JSON: {exc}")
        return {"ok": False, "checks": checks, "failures": failures}

    check(manifest.get("format") == MANIFEST_FORMAT,
          f"manifest format is {MANIFEST_FORMAT!r}"
          if manifest.get("format") == MANIFEST_FORMAT
          else f"manifest format is {manifest.get('format')!r}, expected {MANIFEST_FORMAT!r}")

    artifacts = manifest.get("artifacts", {})
    check(bool(artifacts), f"manifest lists {len(artifacts)} artifact(s)")
    problems = verify_artifacts(root, manifest)
    for problem in problems:
        check(False, problem)
    if not problems:
        check(True, f"every artifact matches its recorded hash ({len(artifacts)})")

    return {"ok": not failures, "checks": checks, "failures": failures}


def compare_trees(committed, fresh, suffixes=GENERATED_SUFFIXES) -> list[str]:
    """Byte differences between a committed certificate directory and a fresh issue of it."""
    committed, fresh = Path(committed), Path(fresh)
    problems: list[str] = []
    names: set[str] = set()
    for directory in (committed, fresh):
        if not directory.is_dir():
            problems.append(f"missing directory: {directory}")
            continue
        names |= {p.name for p in directory.iterdir() if p.suffix in suffixes}
    for name in sorted(names):
        a, b = committed / name, fresh / name
        if not a.is_file():
            problems.append(f"not committed: {name}")
        elif not b.is_file():
            problems.append(f"not produced by a fresh issue: {name}")
        elif a.read_bytes() != b.read_bytes():
            problems.append(f"differs from a fresh issue: {name}")
    return problems


__all__ = [
    "CERT_DIR", "GENERATED_SUFFIXES", "MANIFEST_NAME", "NAMESPACE", "PRINCIPAL",
    "SIG_NAME", "SIGNERS_NAME", "WEB_DIR",
    "compare_trees", "load_manifest", "sha256_bytes", "sha256_file",
    "verify_artifacts", "verify_set", "verify_signature",
]
