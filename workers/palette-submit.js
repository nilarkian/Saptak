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

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }
    if (request.method !== 'POST') {
      return err('Method not allowed', 405);
    }

    let body;
    try { body = await request.json(); }
    catch { return err('Invalid JSON', 400); }

    const { name: rawName, hexes, submitter, social } = body;

    // --- Identify owner: name field starts with OWNER_PAT (server-side only, never visible in UI) ---
    const pat      = env.OWNER_PAT || '';
    const isOwner  = pat.length > 0 && typeof rawName === 'string' && rawName.startsWith(pat);
    const palName  = isOwner ? rawName.slice(pat.length).trim() : (rawName || '').trim();

    // --- Validate hexes (both flows) ---
    if (!Array.isArray(hexes) || hexes.length < 2 || hexes.length > 8) {
      return err('Provide 2–8 hex colors', 400);
    }
    const HEX = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/;
    for (const h of hexes) {
      if (!HEX.test(h)) return err(`Invalid hex: ${h}`, 400);
    }

    // --- Owner flow: dispatch add-palette.yml ---
    if (isOwner) {
      if (!palName || !/^[a-zA-Z0-9 \-_]{1,50}$/.test(palName)) {
        return err('Invalid palette name', 400);
      }
      try {
        const res = await ghFetch(
          `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
          'POST',
          { ref: REF, inputs: { name: palName, mood: '', hexes: hexes.join(',') } },
          pat
        );
        if (res.status === 204) {
          return ok({ mode: 'owner', name: palName });
        }
        return err('Dispatch failed (' + res.status + ')', 500);
      } catch {
        return err('Network error', 500);
      }
    }

    // --- Visitor flow: validate name, append to inbox ---
    if (!palName || !/^[a-zA-Z0-9 \-_]{1,50}$/.test(palName)) {
      return err('Invalid palette name (letters, numbers, spaces, hyphens; max 50 chars)', 400);
    }

    const cleanSubmitter = sanitizeText(submitter, 50) || 'anonymous';
    const cleanSocial    = sanitizeSocial(social)      || '—';
    const date           = new Date().toISOString().split('T')[0];
    const hexDisplay     = hexes.map(h => `\`${h}\``).join(' ');

    const fileUrl = `https://api.github.com/repos/${REPO}/contents/${INBOX_PATH}`;
    let sha, current;
    try {
      const res  = await ghFetch(fileUrl, 'GET', null, pat);
      if (!res.ok) throw new Error(res.status);
      const data = await res.json();
      sha     = data.sha;
      current = atob(data.content.replace(/\n/g, ''));
    } catch {
      return err('Could not read inbox', 500);
    }

    // Count existing data rows (exclude header + separator)
    const dataRows = current.split('\n').filter(
      l => l.startsWith('|') && !/^\|[-| ]+\|$/.test(l.trim()) && !l.includes(' Name ')
    );
    const rowNum   = dataRows.length + 1;
    const newRow   = `| ${rowNum} | ${palName} | ${hexDisplay} | ${cleanSubmitter} | ${cleanSocial} | ${date} |`;
    const updated  = current.trimEnd() + '\n' + newRow + '\n';

    try {
      const res = await ghFetch(fileUrl, 'PUT', {
        message: `palette suggestion: ${palName}`,
        content: btoa(unescape(encodeURIComponent(updated))),
        sha,
      }, pat);
      if (!res.ok) return err('Failed to record suggestion', 500);
    } catch {
      return err('Failed to record suggestion', 500);
    }

    return ok({ mode: 'visitor' });
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
  if (/^https?:\/\/.+/.test(s))                              return s.slice(0, 200);
  if (/^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$/.test(s))         return s.slice(0, 200);
  return '';
}
