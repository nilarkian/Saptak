/**
 * Cloudflare Worker — palette-submit
 *
 * DEPLOY (one-time, ~15 min):
 *   1.  npm install -g wrangler
 *   2.  wrangler login
 *   3.  Create wrangler.toml in repo root:
 *
 *         name = "palette-submit"
 *         main = "workers/palette-submit.js"
 *         compatibility_date = "2024-01-01"
 *
 *   4.  wrangler secret put OWNER_PAT
 *         → paste your fine-grained PAT for nilarkian/Saptak
 *           Permissions needed: Contents: read & write, Actions: read & write
 *   5.  wrangler deploy
 *         → copy the Worker URL shown
 *   6.  Replace WORKER_URL in notes/palettes.html with that URL
 *   7.  git add workers/ wrangler.toml notes/palettes.html && git commit
 *
 * OWNER AUTH:
 *   Put your PAT in the "Your name" field of the form.
 *   The palette name field stays clean — just the palette name.
 *
 * MULTI-PALETTE:
 *   Body: { palettes: [{name, hexes}], submitter, social }
 *   Owner: dispatches one add-palette.yml run per palette (parallel).
 *   Visitor: appends one inbox row per palette in a single file write.
 */

const REPO           = 'nilarkian/Saptak';
const INBOX_PATH     = '_submissions/palette-inbox.md';
const WORKFLOW       = 'add-palette.yml';
const REF            = 'main';
const ALLOWED_ORIGIN = 'https://nilarkian.github.io';

const CORS = {
  'Access-Control-Allow-Origin':  ALLOWED_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const HEX = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/;
const NAME_RE = /^[a-zA-Z0-9 \-_]{1,50}$/;

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (request.method !== 'POST')    return err('Method not allowed', 405);

    let body;
    try { body = await request.json(); }
    catch { return err('Invalid JSON', 400); }

    const { submitter, social } = body;

    // --- Identify owner: submitter field equals OWNER_PAT (server-side only) ---
    const pat     = env.OWNER_PAT || '';
    const secret  = env.OWNER_SECRET || '';
    const isOwner = secret.length > 0 && typeof submitter === 'string' && submitter.trim() === secret;

    // --- Normalize to array ---
    let palettes;
    if (Array.isArray(body.palettes) && body.palettes.length > 0) {
      palettes = body.palettes;
    } else if (body.name && body.hexes) {
      palettes = [{ name: body.name, hexes: body.hexes }];
    } else {
      return err('No palettes provided', 400);
    }

    if (palettes.length > 20) return err('Max 20 palettes per submission', 400);

    // --- Validate each palette ---
    for (let i = 0; i < palettes.length; i++) {
      const { name, hexes } = palettes[i];
      if (!name || !NAME_RE.test(name)) {
        return err(`Palette ${i + 1}: invalid name (letters, numbers, spaces, hyphens; max 50 chars)`, 400);
      }
      if (!Array.isArray(hexes) || hexes.length < 2 || hexes.length > 8) {
        return err(`Palette ${i + 1} (${name}): provide 2–8 hex colors`, 400);
      }
      for (const h of hexes) {
        if (!HEX.test(h)) return err(`Palette ${i + 1} (${name}): invalid hex "${h}"`, 400);
      }
    }

    // --- Owner flow: dispatch one workflow run per palette (parallel) ---
    if (isOwner) {
      const results = await Promise.all(palettes.map(p =>
        ghFetch(
          `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
          'POST',
          { ref: REF, inputs: { name: p.name, mood: '', hexes: p.hexes.join(',') } },
          pat
        )
      ));
      const failed = results.find(r => r.status !== 204);
      if (failed) return err('Dispatch failed (' + failed.status + ')', 500);
      return ok({ mode: 'owner', names: palettes.map(p => p.name) });
    }

    // --- Visitor flow: read inbox once, append N rows, write once ---
    const cleanSubmitter = sanitizeText(submitter, 50) || 'anonymous';
    const cleanSocial    = sanitizeSocial(social)      || '—';
    const date           = new Date().toISOString().split('T')[0];
    const fileUrl        = `https://api.github.com/repos/${REPO}/contents/${INBOX_PATH}`;

    let sha, current;
    try {
      const res  = await ghFetch(fileUrl, 'GET', null, pat);
      if (!res.ok) {
        const body = await res.text().catch(() => '');
        return err('Could not read inbox: GitHub ' + res.status + ' ' + body.slice(0, 200), 500);
      }
      const data = await res.json();
      sha     = data.sha;
      current = atob(data.content.replace(/\n/g, ''));
    } catch (e) {
      return err('Could not read inbox: ' + (e && e.message ? e.message : String(e)), 500);
    }

    const dataRows = current.split('\n').filter(
      l => l.startsWith('|') && !/^\|[-| ]+\|$/.test(l.trim()) && !l.includes(' Name ')
    );
    let rowNum = dataRows.length + 1;
    let newRows = '';
    for (const p of palettes) {
      const hexDisplay = p.hexes.map(h => `\`${h}\``).join(' ');
      newRows += `| ${rowNum++} | ${p.name} | ${hexDisplay} | ${cleanSubmitter} | ${cleanSocial} | ${date} |\n`;
    }
    const updated = current.trimEnd() + '\n' + newRows;

    try {
      const commitMsg = palettes.length === 1
        ? `palette suggestion: ${palettes[0].name}`
        : `palette suggestions: ${palettes.map(p => p.name).join(', ')}`;
      const res = await ghFetch(fileUrl, 'PUT', {
        message: commitMsg,
        content: btoa(unescape(encodeURIComponent(updated))),
        sha,
      }, pat);
      if (!res.ok) return err('Failed to record suggestion', 500);
    } catch {
      return err('Failed to record suggestion', 500);
    }

    return ok({ mode: 'visitor', count: palettes.length });
  },
};

// ── Helpers ────────────────────────────────────────────────────────────────

function ok(body) {
  return new Response(JSON.stringify({ ok: true, ...body }), {
    status: 200,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}

function err(message, status = 400) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}

function ghFetch(url, method, body, token) {
  return fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json',
      'User-Agent': 'palette-submit-worker/1.0',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
}

function sanitizeText(s, maxLen) {
  if (!s || typeof s !== 'string') return '';
  return s.replace(/[<>&"']/g, '').trim().slice(0, maxLen);
}

function sanitizeSocial(s) {
  if (!s || typeof s !== 'string') return '';
  s = s.trim();
  if (/^https?:\/\/.+/.test(s))                        return s.slice(0, 200);
  if (/^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$/.test(s))   return s.slice(0, 200);
  return '';
}
