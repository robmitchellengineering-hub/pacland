#!/usr/bin/env python3
"""Sign the certificate manifest with an OpenSSH (ed25519) key, and publish the public key.

    python3 scripts/sign_manifest.py [--key ~/.ssh/vvs-manifest]

Writes ``certificates/vvs/MANIFEST.json.sig`` and ``certificates/vvs/allowed_signers`` (and the
copies under ``web/vvs/``, which is what the site publishes). The private key never enters the
repository — only the public key and the signature do, which is what makes the certificate
verifiable by someone who does not trust this machine.

Signing is a deliberate act, separate from issuing: ``issue_vvs.py`` regenerates content and this
script attests to it. If the content moves without a new signature, verification fails — which is
the property that makes the signature worth having.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify.integrity import (  # noqa: E402
    CERT_DIR, MANIFEST_NAME, NAMESPACE, PRINCIPAL, SIG_NAME, SIGNERS_NAME, verify_set,
)


def die(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Sign the certificate manifest (OpenSSH SSHSIG).")
    ap.add_argument("--key", default=str(pathlib.Path.home() / ".ssh" / "vvs-manifest"),
                    help="private key (default ~/.ssh/vvs-manifest); never committed")
    ap.add_argument("--cert-dir", default=str(ROOT / CERT_DIR))
    args = ap.parse_args(argv[1:])

    cert = pathlib.Path(args.cert_dir)
    key = pathlib.Path(args.key)
    manifest = cert / MANIFEST_NAME
    if not manifest.is_file():
        die(f"no manifest to sign: {manifest}")
    if not key.is_file():
        die(f"no signing key at {key} — generate one with: "
            f"ssh-keygen -t ed25519 -N '' -f {key}")
    pub = pathlib.Path(str(key) + ".pub")
    if not pub.is_file():
        die(f"public key missing: {pub}")
    keygen = shutil.which("ssh-keygen")
    if keygen is None:
        die("ssh-keygen not found")

    blob = manifest.read_bytes()
    proc = subprocess.run([keygen, "-Y", "sign", "-f", str(key), "-n", NAMESPACE],
                          input=blob, capture_output=True)
    if proc.returncode != 0:
        die(f"ssh-keygen refused: {proc.stderr.decode('utf-8', 'replace').strip()}")

    fields = pub.read_text().split()
    if len(fields) < 2:
        die(f"unreadable public key: {pub}")
    signers_line = f"{PRINCIPAL} {fields[0]} {fields[1]}\n"

    targets = [cert]
    web = ROOT / "web" / "vvs"
    if web.is_dir() and web.resolve() != cert.resolve():
        targets.append(web)
    for directory in targets:
        (directory / SIG_NAME).write_bytes(proc.stdout)
        (directory / SIGNERS_NAME).write_text(signers_line)
    print(f"signed {MANIFEST_NAME} ({len(blob)} bytes) → {SIG_NAME} in "
          f"{', '.join(str(t.relative_to(ROOT)) for t in targets)}")
    print(f"principal: {PRINCIPAL} · key {fields[0]} · fingerprint "
          f"{fields[1][:16]}…")

    result = verify_set(ROOT)
    for ok, message in result["checks"]:
        print(f"  {'ok  ' if ok else 'FAIL'} {message}")
    if not result["ok"]:
        print("\nFAIL: the set does not verify after signing", file=sys.stderr)
        return 1
    print("\nPASS: the signed set verifies offline")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
