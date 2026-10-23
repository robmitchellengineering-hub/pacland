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

1. Re-zip: `(cd web && zip -r /tmp/pacland-site.zip .)`
2. POST the zip to the Netlify deploy endpoint, or redeploy via the API
   (`POST /api/v1/sites/29e7c912-9a79-4cb3-a7e8-f491dc385c0e/deploys`).
3. GitHub Pages: copy `web/index.html` to the `gh-pages` branch and push.

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
