/**
 * Cloudflare Worker — palette-submit
 *
 * SUBMIT FLOW (on every "Suggest" click):
 *   Validate → INSERT rows into D1 (atomic, no GitHub call, no race condition).
 *   Returns immediately with { ok: true, queued: N }.
 *
 * DRAIN FLOW (cron: 30 20 * * * = 02:00 IST daily):
 *   SELECT all pending rows → write to GitHub in two batched commits:
 *     - Owner rows  → _data/palettes.json
 *     - Visitor rows → _submissions/palette-inbox.md
 *   DELETE processed rows. If a GitHub write fails, rows stay for next night.
 *
 * SETUP (one-time):
 *   1. wrangler d1 create palette-submissions
 *   2. Add [[d1_databases]] binding to wrangler.toml (already done)
 *   3. wrangler d1 execute palette-submissions --remote --command "CREATE TABLE ..."
 *   4. wrangler secret put OWNER_PAT   (PAT: Contents + Actions read/write)
 *   5. wrangler secret put OWNER_SECRET (short memorable word)
 *   6. wrangler deploy
 *
 * OWNER AUTH:
 *   Put your OWNER_SECRET value in the "Your name" field.
 *   Palette queued as owner → committed to _data/palettes.json at 2am IST.
 */

const REPO           = 'nilarkian/Saptak';
const INBOX_PATH     = '_submissions/palette-inbox.md';
const PALETTES_PATH  = '_data/palettes.json';
const REF            = 'main';
const ALLOWED_ORIGIN = 'https://nilarkian.github.io';

const CORS = {
  'Access-Control-Allow-Origin':  ALLOWED_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const HEX     = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/;
const NAME_RE = /^[a-zA-Z0-9 \-_]{1,50}$/;

export default {
  // ── SUBMIT HANDLER ─────────────────────────────────────────────────────────
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (request.method !== 'POST')    return err('Method not allowed', 405);

    let body;
    try { body = await request.json(); }
    catch { return err('Invalid JSON', 400); }

    const { submitter, social } = body;

    const secret  = env.OWNER_SECRET || '';
    const isOwner = secret.length > 0 && typeof submitter === 'string' && submitter.trim() === secret;

    // Normalize to array — accept {name, colors:[{hex,name?}]} or legacy {name, hexes:[str]}
    let palettes;
    if (Array.isArray(body.palettes) && body.palettes.length > 0) {
      palettes = body.palettes;
    } else if (body.colors || body.hexes) {
      palettes = [{ name: body.name, colors: body.colors, hexes: body.hexes }];
    } else {
      return err('No palettes provided', 400);
    }

    if (palettes.length > 20) return err('Max 20 palettes per submission', 400);

    // Normalize each palette's colors field
    for (let i = 0; i < palettes.length; i++) {
      const p = palettes[i];
      p.name = (p.name || '').trim();
      if (Array.isArray(p.colors)) {
        // new format: [{hex, name?}]
      } else if (Array.isArray(p.hexes)) {
        p.colors = p.hexes.map(h => ({ hex: h }));
      } else {
        return err(`Palette ${i + 1}: provide colors array`, 400);
      }
    }

    // Validate each palette
    for (let i = 0; i < palettes.length; i++) {
      const { name, colors } = palettes[i];
      if (name && !NAME_RE.test(name)) {
        return err(`Palette ${i + 1}: invalid name (letters, numbers, spaces, hyphens; max 50 chars)`, 400);
      }
      if (colors.length < 2 || colors.length > 8) {
        return err(`Palette ${i + 1} (${name}): provide 2–8 hex colors`, 400);
      }
      for (const c of colors) {
        if (!HEX.test(c.hex)) return err(`Palette ${i + 1} (${name}): invalid hex "${c.hex}"`, 400);
      }
    }

    const cleanSubmitter = sanitizeText(submitter, 50) || 'anonymous';
    const cleanSocial    = sanitizeSocial(social)      || '';
    const createdAt      = new Date().toISOString();

    // Batch INSERT — store colors as JSON in the hexes column
    const stmts = palettes.map(p =>
      env.DB.prepare(
        'INSERT INTO submissions (name, hexes, submitter, social, is_owner, created_at) VALUES (?, ?, ?, ?, ?, ?)'
      ).bind(p.name, JSON.stringify(p.colors), cleanSubmitter, cleanSocial, isOwner ? 1 : 0, createdAt)
    );

    try {
      await env.DB.batch(stmts);
    } catch (e) {
      return err('Failed to queue submission: ' + (e && e.message ? e.message : String(e)), 500);
    }

    return ok({ queued: palettes.length });
  },

  // ── DRAIN HANDLER (cron 30 20 * * * = 02:00 IST) ──────────────────────────
  async scheduled(_event, env, _ctx) {
    const pat = env.OWNER_PAT || '';

    // Fetch all pending rows
    const { results } = await env.DB.prepare('SELECT * FROM submissions ORDER BY id').all();
    if (!results || results.length === 0) return;

    const maxId = results[results.length - 1].id;

    const ownerRows   = results.filter(r => r.is_owner === 1);
    const visitorRows = results.filter(r => r.is_owner === 0);

    // ── Owner rows → _data/palettes.json ──────────────────────────────────────
    if (ownerRows.length > 0) {
      const fileUrl = `https://api.github.com/repos/${REPO}/contents/${PALETTES_PATH}`;
      try {
        const res = await ghFetch(fileUrl, 'GET', null, pat);
        if (!res.ok) throw new Error('GET palettes.json: GitHub ' + res.status);
        const data     = await res.json();
        const sha      = data.sha;
        const existing = JSON.parse(atob(data.content.replace(/\n/g, '')));
        const names    = new Set(existing.map(p => p.name));

        let added = 0;
        for (const row of ownerRows) {
          if (row.name && names.has(row.name)) continue;
          const colors = parseStoredColors(row.hexes);
          existing.unshift({ name: row.name, mood: '', colors });
          names.add(row.name);
          added++;
        }

        if (added > 0) {
          const putRes = await ghFetch(fileUrl, 'PUT', {
            message: `Add palette${added > 1 ? 's' : ''}: ${ownerRows.map(r => r.name).join(', ')}`,
            content: btoa(unescape(encodeURIComponent(JSON.stringify(existing, null, 2)))),
            sha,
          }, pat);
          if (!putRes.ok) throw new Error('PUT palettes.json: GitHub ' + putRes.status);
        }

        await env.DB.prepare('DELETE FROM submissions WHERE is_owner=1 AND id<=?').bind(maxId).run();
      } catch (e) {
        // Leave rows in D1 — will retry next night
        console.error('Owner drain failed:', e && e.message ? e.message : String(e));
      }
    }

    // ── Visitor rows → _submissions/palette-inbox.md ──────────────────────────
    if (visitorRows.length > 0) {
      const fileUrl = `https://api.github.com/repos/${REPO}/contents/${INBOX_PATH}`;
      try {
        const res = await ghFetch(fileUrl, 'GET', null, pat);
        if (!res.ok) throw new Error('GET inbox: GitHub ' + res.status);
        const data    = await res.json();
        const sha     = data.sha;
        const current = atob(data.content.replace(/\n/g, ''));

        const dataRows = current.split('\n').filter(
          l => l.startsWith('|') && !/^\|[-| ]+\|$/.test(l.trim()) && !l.includes(' Name ')
        );
        let rowNum  = dataRows.length + 1;
        let newRows = '';
        for (const row of visitorRows) {
          const colors     = parseStoredColors(row.hexes);
          const hexDisplay = colors.map(c => `\`${c.hex}${c.name ? ' ' + c.name : ''}\``).join(' ');
          const social     = row.social || '—';
          const date       = row.created_at.split('T')[0];
          newRows += `| ${rowNum++} | ${row.name} | ${hexDisplay} | ${row.submitter} | ${social} | ${date} |\n`;
        }
        const updated = current.trimEnd() + '\n' + newRows;

        const putRes = await ghFetch(fileUrl, 'PUT', {
          message: `palette suggestion${visitorRows.length > 1 ? 's' : ''}: ${visitorRows.map(r => r.name).join(', ')}`,
          content: btoa(unescape(encodeURIComponent(updated))),
          sha,
        }, pat);
        if (!putRes.ok) throw new Error('PUT inbox: GitHub ' + putRes.status);

        await env.DB.prepare('DELETE FROM submissions WHERE is_owner=0 AND id<=?').bind(maxId).run();
      } catch (e) {
        console.error('Visitor drain failed:', e && e.message ? e.message : String(e));
      }
    }
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

function parseStoredColors(raw) {
  try {
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed) && parsed.length && typeof parsed[0] === 'object') return parsed;
  } catch {}
  // legacy: comma-separated hex strings
  return raw.split(',').map(h => ({ hex: h }));
}

function sanitizeSocial(s) {
  if (!s || typeof s !== 'string') return '';
  s = s.trim();
  if (/^https?:\/\/.+/.test(s))                       return s.slice(0, 200);
  if (/^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$/.test(s))  return s.slice(0, 200);
  return '';
}
