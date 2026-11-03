# Certificate integrity — how to check one without trusting us

A certificate is only evidence if someone who does not trust the issuer can check it. This page is
the check, and it is deliberately short: three files and a command that ships with every macOS and
Linux system.

## What is checked

| check | what it proves | what it does **not** prove |
|---|---|---|
| the manifest's OpenSSH signature (`MANIFEST.json.sig`, `allowed_signers`) | the manifest was signed by the holder of the published key, and has not changed since | that the issuer is right |
| the sha256 of each artifact against the manifest | the certificate you are reading is the file that was signed | that the numbers in it are correct |
| a fresh issue, byte-for-byte (`check_certificates_current.py`) | the committed certificates are what the current evidence produces, deterministically | that the evidence is complete |

The signature makes a certificate **tamper-evident**. It does not make a verdict **true** — that is
the falsifier's job, and every finding names one.

## Verify from the repository

```
git clone https://github.com/robmitchellengineering-hub/pacland
cd pacland
python3 scripts/verify_certificates.py
```

It prints each check and exits non-zero if any fails. No network, no account, no key of your own.

## Verify with the files alone

The certificate directory is self-contained; this needs nothing from the repository's source:

```
ssh-keygen -Y verify -f certificates/vvs/allowed_signers \
  -I vvs@pacland -n vvs -s certificates/vvs/MANIFEST.json.sig \
  < certificates/vvs/MANIFEST.json
sha256sum certificates/vvs/*.json
```

The first line must print `Good "vvs" signature for vvs@pacland`. The hashes must match the
`sha256` recorded for each artifact in the manifest.

## Reproduce it

```
python3 scripts/check_certificates_current.py
```

Two and a half minutes: it re-issues every certificate into a temporary directory, compares the
result with what is committed byte-for-byte, verifies the signature, and verifies every hash. It
never writes over the bytes it is testing — that was the bug it replaces.

## What is not claimed yet

Stated here rather than left for a reviewer to find:

- **One issuer.** The key is a single ed25519 key held by the maintainer. The VDS specification's
  layer 3 (an auditor distinct from the subject) is specified and not built.
- **No revocation list.** A compromised key would need a new key and a note in this file; there is
  no mechanism that makes a stolen key stop verifying.
- **Three of the five dossiers type their verdicts.** `gdpnow`, `smets-wouters` and `riemann-zeros`
  carry statuses written by hand; `cmip6` computes all but one; `physics` computes all. A typed
  verdict does not move when the number moves, so it is not yet a gate. Making them computed is the
  next change, and until it lands this paragraph is the honest reading of those certificates.
- **The signature binds a manifest, not a claim.** If the falsifier a finding names is weak, the
  signature faithfully attests to a weak check. That is why the falsifier is a field and not prose.

## Why it is built this way

The failure this replaces was not a missing feature, it was a gate that could not fail:
`scripts/check_certificates_current.py` used to re-issue into the directory it was about to compare,
discard the comparison, and print PASS. A gate that cannot fail is worse than no gate, because it
launders a claim. Each check here has a test that proves it can fail — a tampered manifest, a
tampered artifact, a one-byte difference between a fresh issue and the committed set.
