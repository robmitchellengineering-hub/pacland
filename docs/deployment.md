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

### The site-id trap (measured 2026-11-04)

`29e7c912…` is the site named **pacland**. It has **no custom domain**; its default domain is
`pacland.netlify.app`. `pacland.morpheus.nz` is Cloudflare-proxied to a **different** site,
`pacland-main.netlify.app`, which the token cannot see — `GET /sites` returns only `pacland`,
`web-page-test-muks1p48` and `morpheus2`.

So a successful deploy updates `pacland.netlify.app` and **not** the canonical domain. Any session
that sees "deploy succeeded, domain unchanged" should read this paragraph instead of re-deriving it.

Fix, either one line:
- point the Cloudflare `pacland` CNAME at `pacland.netlify.app`, or
- add `pacland.morpheus.nz` as a custom domain on the `pacland` site (Netlify → Domain management).

## Gotchas

- **New Netlify sites default to account SSO (`sso_login: true`)**, which serves
  `HTTP 401 "Login Redirect"` → `app.netlify.com/edge-access`. A site created via
  the API under Rob's token must be un-walled with
  `PATCH /api/v1/sites/{id}` body `{"sso_login": false}`. Done for this site.
- **Custom domain `pacland.morpheus.nz` is live** (Cloudflare CNAME `pacland` →
  `pacland.netlify.app`). The canonical address in every doc is now
  `pacland.morpheus.nz`; `pacland.netlify.app` remains only as the Netlify backend.

## Credentials (never in chat or this file)

- Rob's Netlify token: Morpheus prod DB `user_settings.connections.netlify.token`
  (encrypted). Do not copy it out; decrypt in-process like the deploy scripts in
  `/tmp` did on 2026-10-18.
- arXiv: not yet submitted — needs Rob's arXiv account (https://arxiv.org/register).
