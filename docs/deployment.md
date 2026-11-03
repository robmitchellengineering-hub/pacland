# Deployment — where PACLAND lives

Live surfaces (both serving `web/index.html`, the same static demo):

- **pacland.morpheus.nz (primary — the canonical address):** custom domain → Netlify
  (`pacland.netlify.app`).
  - site id `29e7c912-9a79-4cb3-a7e8-f491dc385c0e`, account `robmitchellengineering-hub`.
  - Deployed 2026-10-18 with Rob's own Netlify token (stored in the Morpheus
    production DB — `user_settings.connections` for `robmitchellengineering@gmail.com`,
    key `netlify.token`, AES-256-GCM encrypted; decrypted with the prod `ENCRYPTION_KEY`).
- **GitHub Pages (mirror):** https://robmitchellengineering-hub.github.io/pacland/
  - `gh-pages` branch, served from the repo root (`web/index.html` copied in).

## Republish after a `web/index.html` change

**One command (preferred — it does steps 1 and 2 for you and verifies the result):**

```
node scripts/deploy-netlify.mjs            # zip origin/main's web/, POST, wait for ready, verify
node scripts/deploy-netlify.mjs --dry-run  # build the zip only, post nothing
node scripts/deploy-netlify.mjs --site <id|name>   # target a different Netlify site
```

It reads the Netlify token from its documented home (the Morpheus production DB) and decrypts it in
process with the prod `ENCRYPTION_KEY`; it never prints the token, and it verifies the deployed bytes
rather than trusting the POST's status code.

By hand, if you prefer:

1. Re-zip: `(cd web && zip -r /tmp/pacland-site.zip .)`
2. `POST /api/v1/sites/29e7c912-9a79-4cb3-a7e8-f491dc385c0e/deploys` with `Content-Type: application/zip`
   and `Authorization: Bearer <token>`.
3. GitHub Pages: `scripts/deploy-pages.sh`.

### Where the domain actually points (measured 2026-11-04)

**`pacland.morpheus.nz` is served by GitHub Pages, not Netlify.** Cloudflare proxies the CNAME to
`robmitchellengineering-hub.github.io`, and Pages builds from the `gh-pages` branch — which
`scripts/deploy-pages.sh` mirrors from `web/`. A merge to `main` does **not** publish; the script does,
and Pages takes ~60-90 s.

Netlify is a *preview* path only: site `29e7c912…` is `pacland` with no custom domain, and the domain is
claimed by two other Netlify sites (`4bc468b4-…`, `a6870cad-…`) so attaching it is refused —
`must be unique`. The stored token belongs to the Valiant Music account and cannot touch
`pacland-main`, whose production deploys stopped landing anyway.

So `node scripts/deploy-netlify.mjs` publishes `pacland.netlify.app` (a preview);
`bash scripts/deploy-pages.sh` publishes the domain.

**Verification is not satisfiable by a green CI or a merge** — fetch the live URL and grep for a string
from the change. Measured on 2026-11-04: after the mirror ran, the live page went from 95,151 bytes
without the Energy card to 92,532 with it, `index.json` at 424 items.
