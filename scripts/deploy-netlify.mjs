#!/usr/bin/env node
/**
 * deploy-netlify.mjs — publish `web/` to the PACLAND Netlify site, in one command.
 *
 * WHY THIS FILE EXISTS
 *
 * Rob, 2026-11-04: "the system works the problem is you keep forgetting how to do it."
 * It does work, and it was re-derived from scratch at least twice. The procedure lives in
 * docs/deployment.md, but the *credential retrieval* is the part that kept costing time, so it
 * is encoded here rather than described:
 *
 *   1. the Netlify token lives, encrypted, in the Morpheus PRODUCTION database —
 *      `user_settings.connections` for robmitchellengineering@gmail.com, key `netlify.token`
 *      (AES-256-GCM, `v1:<iv>:<tag>:<data>`, key = base64 `ENCRYPTION_KEY` from the Morpheus server .env)
 *   2. the production database URL is `PROD_DATABASE_URL` in `morpheus-self-hosted/server/.env.prodsql`
 *   3. `pg` is not a dependency of this repo, so it is required from the Morpheus server tree
 *
 * Usage:
 *   node scripts/deploy-netlify.mjs                    # deploy main's web/, wait, verify
 *   node scripts/deploy-netlify.mjs --ref HEAD         # deploy a different ref
 *   node scripts/deploy-netlify.mjs --site <id|name>   # override the site
 *   node scripts/deploy-netlify.mjs --dry-run          # build the zip only
 *
 * It never prints the token.
 *
 * THIS PUBLISHES A PREVIEW, NOT THE DOMAIN. pacland.morpheus.nz is served by GitHub Pages
 * (Cloudflare CNAME -> robmitchellengineering-hub.github.io, built from `gh-pages`) and is published
 * by `scripts/deploy-pages.sh`. Netlify site `29e7c912-…` (`pacland`) has no custom domain and cannot
 * claim one — the domain is held by two other Netlify sites. So this script is the fast preview path;
 * the domain path is deploy-pages.sh. See docs/deployment.md.
 */
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

const MORPHEUS = '/Users/mac/code/morpheus-self-hosted/server';
const DEFAULT_SITE = '29e7c912-9a79-4cb3-a7e8-f491dc385c0e'; // `pacland`, per docs/deployment.md
const MARKER = 'web/index.html';

const argv = process.argv.slice(2);
const opt = (name, fallback = null) => {
  const i = argv.indexOf('--' + name);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : fallback;
};
const flag = (name) => argv.includes('--' + name);

const ref = opt('ref', 'origin/main');
const site = opt('site', DEFAULT_SITE);
const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

function readEnv(file, key) {
  const p = path.join(MORPHEUS, file);
  if (!fs.existsSync(p)) throw new Error(`missing ${p}`);
  const line = fs.readFileSync(p, 'utf8').split('\n').find((l) => l.startsWith(key + '='));
  if (!line) throw new Error(`${key} not found in ${file}`);
  return line.slice(key.length + 1).trim().replace(/^"|"$/g, '');
}

async function netlifyToken() {
  const requireFromMorpheus = createRequire(path.join(MORPHEUS, 'package.json'));
  const pg = requireFromMorpheus('pg');
  const client = new pg.Client({
    connectionString: readEnv('.env.prodsql', 'PROD_DATABASE_URL'),
    ssl: { rejectUnauthorized: false },
  });
  await client.connect();
  const r = await client.query(
    `select s.connections from user_settings s
       join users u on u.id = s.created_by_id
      where u.email = 'robmitchellengineering@gmail.com'`,
  );
  await client.end();
  const enc = JSON.parse(r.rows[0].connections).netlify.token;
  if (!enc.startsWith('v1:')) return enc; // legacy plaintext
  const key = Buffer.from(readEnv('.env', 'ENCRYPTION_KEY'), 'base64');
  const [, iv, tag, data] = enc.split(':');
  const d = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'base64'));
  d.setAuthTag(Buffer.from(tag, 'base64'));
  return Buffer.concat([d.update(Buffer.from(data, 'base64')), d.final()]).toString('utf8');
}

function buildZip(refName) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pacland-deploy-'));
  const archive = execFileSync('git', ['-C', repoRoot, 'archive', refName, 'web'], { maxBuffer: 1 << 28 });
  const tarPath = path.join(tmp, 'site.tar');
  fs.writeFileSync(tarPath, archive);
  execFileSync('tar', ['-xf', tarPath, '-C', tmp]);
  const zipPath = path.join(tmp, 'site.zip');
  execFileSync('zip', ['-qr', zipPath, '.'], { cwd: path.join(tmp, 'web') });
  return { zipPath, bytes: fs.statSync(zipPath).size };
}

const api = (token, p, init = {}) =>
  fetch('https://api.netlify.com/api/v1' + p, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init.headers || {}) },
  });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const { zipPath, bytes } = buildZip(ref);
console.log(`zip: ${(bytes / 1048576).toFixed(2)} MB from ${ref}`);

if (flag('dry-run')) {
  console.log('--dry-run: built only, nothing posted');
  process.exit(0);
}

const token = await netlifyToken();
const info = await api(token, `/sites/${site}`);
if (!info.ok) throw new Error(`site ${site} not reachable with this token (${info.status})`);
const siteInfo = await info.json();
console.log(`site: ${siteInfo.name}  default: ${siteInfo.default_domain}  custom: ${siteInfo.custom_domain || '(none)'}`);

const post = await api(token, `/sites/${site}/deploys`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/zip' },
  body: fs.readFileSync(zipPath),
});
const deploy = await post.json();
if (!post.ok) throw new Error(`deploy rejected: ${post.status} ${JSON.stringify(deploy).slice(0, 200)}`);
console.log(`deploy: ${deploy.id}  state: ${deploy.state}`);

let state = deploy.state;
for (let i = 0; i < 60 && state !== 'ready' && state !== 'error'; i++) {
  await sleep(2000);
  const d = await (await api(token, `/sites/${site}/deploys/${deploy.id}`)).json();
  state = d.state;
}
console.log(`state: ${state}`);
if (state !== 'ready') process.exit(1);

const url = deploy.deploy_ssl_url || deploy.ssl_url;
const page = await fetch(`${url}/index.html`);
const html = await page.text();
const hasEnergy = html.includes('<h3>Energy</h3>');
console.log(`verified: ${url} -> HTTP ${page.status}, ${html.length} bytes, Energy card: ${hasEnergy}`);

const published = await (await api(token, `/sites/${site}`)).json();
console.log(`published on ${published.default_domain}${published.custom_domain ? ' / ' + published.custom_domain : ''}`);
if (!published.custom_domain) {
  console.log('NOTE: this site has no custom domain — it is a PREVIEW target. The canonical domain is');
  console.log('      published by scripts/deploy-pages.sh (GitHub Pages). See docs/deployment.md.');
}
