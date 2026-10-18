# Toolchain — installing the oracle stack (CYTools)

The adapters are written; this is only about getting the dependencies onto a
suitable node. Status as of 2026-10-18.

## VERIFIED — Linux install works

On the harness-mesh `studio-linux` VM (Ubuntu 24.04, via `scripts/install_cytools.sh`
equivalent), CYTools **1.4.12** installed cleanly after `apt install libgmp-dev
libgmpxx4ldbl`, and the quintic Calabi-Yau threefold returned the correct results:

- `h11 = 1`, `h21 = 101` (the known Hodge numbers of the quintic)
- `second Chern class = [-250, 50, 50, 50, 50, 50]`
- triple intersection numbers including the degree-5 entries

The route is `mac → win-2 (100.86.50.6) → studio-linux (192.168.28.128)`, login
`rob`, NOPASSWD sudo. The Mac-only blockers below do **not** apply to Linux.

Also verified on the same VM, 2026-10-18:

- **JAXVacua** installed from PyPI and loads a bundled flux-EFT
  (`jvc.FluxEFT(h12=2, model_ID=1)`), exposing `scalar_potential`, `superpotential`,
  `W0`, `tadpole`, `n_fluxes`, `hessian`, `mass_matrix`. This is the flux-vacua
  engine — see `docs/tooling.md`.
- **`cytools.fetch_polytopes`** (Kreuzer–Skarke online query) fails on 1.4.12: the
  server redirects to a malformed URL. Workaround: JAXVacua's bundled models, or
  manual polytope lists.

## What was attempted on this machine (the Mac — no Linux, no Homebrew)

`pip install cytools` on this Mac (x86_64 Python 3.12, **no Homebrew**) failed on
two independent walls:

1. **`triangulumancer`** (a CYTools dependency) needs the GMP + GMPXX C++
   libraries, which are not installed and not findable without a package manager.
2. **`numba`/`llvmlite`** resolve to *source* builds — no macOS x86_64 wheels for
   the pinned versions — which is slow and fragile.

Building GMP from source was attempted (`gmp-6.3.0`); `./configure` **hung** on
this machine. Root cause: an Intel Mac with no package manager is the wrong node
for a C++ physics stack.

## The clean path: Linux

On a Debian/Ubuntu node (e.g. the harness-mesh `studio-linux`), GMP is an apt
package and numba/llvmlite publish wheels, so the whole thing is two commands —
see [`scripts/install_cytools.sh`](../scripts/install_cytools.sh):

```sh
sudo apt-get update && sudo apt-get install -y libgmp-dev libgmpxx4ldbl
python3 -m venv .venv && .venv/bin/pip install cytools
```

## Alternative: macOS with a package manager

If GMP is available (Homebrew or conda-forge), point CMake at it and retry:

```sh
brew install gmp                      # or: micromamba install -c conda-forge gmp
export CMAKE_ARGS="-DGMP_INCLUDE_DIR=$(brew --prefix gmp)/include \
  -DGMP_LIBRARY=$(brew --prefix gmp)/lib/libgmp.dylib \
  -DGMPXX_INCLUDE_DIR=$(brew --prefix gmp)/include \
  -DGMPXX_LIBRARY=$(brew --prefix gmp)/lib/libgmpxx.dylib"
python3 -m venv .venv && .venv/bin/pip install cytools
```

## Verify

The quintic Calabi-Yau threefold must return Hodge numbers `(1, 101)`:

```sh
.venv/bin/python -c "from cytools import Polytope; p=Polytope([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[-1,-1,-1,-1]]); cy=p.triangulate().get_cy(); print(cy.h11(), cy.h21())"
```

## Why this matters to PACLAND

CYTools supplies the *discrete* half of the genotype — Hodge numbers, triple
intersection numbers, and flux-vacua search — which is L1 encoding and L2 stages
2–4. The adapter is already wired in [`src/pacland/oracle/adapters.py`](../src/pacland/oracle/adapters.py);
once the dependency is installed, real CY topology data flows straight into the
certificate loop. License: CYTools is GPL-3.0 (fine for generating data; see
[`docs/tooling.md`](tooling.md)).
