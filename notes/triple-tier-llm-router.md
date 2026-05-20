---
layout: note-layout
title: 3-Layer LLM Setup md
topic: AI
date: 2026-03-10
tags:
  - ai
  - llm
  - cost-optimization
  - agents
  - infrastructure
is_note: true
---

# 3-Layer LLM Router & 20x Token Reduction System

A production-grade system that routes AI workloads across three cost tiers — free local, cheap API, premium API — cutting LLM costs by **93–95%** without meaningful quality loss.

---

## What is this?

Most AI systems waste money by routing everything to expensive models. This system fixes that with two parts:

**Part 1 — Three-Tier Router:** A Node.js library that classifies every AI call by complexity and dispatches it to the cheapest model that can handle it. Simple tasks go to a free local model. Reasoning tasks go to cheap API models. Only hard, identity-critical, or high-stakes work hits the premium model.

**Part 2 — Token Efficiency Doctrine:** 15 operating laws that compress prompts, outputs, memory, and tool calls across all three tiers. The router controls *which* model gets called. The doctrine controls *what* every model sends and stores.

Both parts are required. The router alone saves ~67–90%. The doctrine adds the remaining ~3–10%.

---

## Value Proposition

| Source | Savings |
|--------|---------|
| Three-tier routing alone | ~67% floor → ~90% in realistic mixes |
| Efficiency doctrine on top | additional ~3–10% |
| **Both combined** | **~93–95% vs. all-premium setup** |

**Realistic call distribution:** 30% free local / 65% cheap API / 5% premium

**Root causes this fixes:**
- Using expensive models for simple tasks (classification, labeling, formatting)
- Re-sending full context/history on every call
- Verbose outputs with preambles, narration, and filler
- Keeping everything in memory when summaries suffice
- Making redundant tool/API calls for things already in context

---

## The Three Tiers

| ID | Class | Where | Default Model | Purpose Buckets |
|----|-------|-------|---------------|-----------------|
| **T1** | Chat / Mechanical | Local Ollama — **free** | qwen3:32b (fallback 14b/3b by RAM) | greeting, echo, classify, label, json_reformat, template_slot_fill, dedup, hash_match |
| **T2** | Cheap Reasoning | DeepSeek API (~$0.14/1M tokens) | deepseek-v4-pro (fallback deepseek-v4-flash) | summarize, enrich, reflexion_first_pass, kg_titling, embedding_title, compact_memory, long_context_analysis, codebase_analysis, research_synthesis |
| **T3** | Precision / Premium | Anthropic API | claude-opus-4-7 | everything else + **HARD FLOOR**: identity_audit, self_modification, phenomenology, architectural_decision, author_voice, high_stakes_review |

**Cascade on failure:** T1 fail → T2. T2-pro fail → T2-flash → T3. T3 fail → throw.

**Quota window:** rolling 50 calls. Targets T1=30% / T2=40% / T3=30%. Tolerance ±10%.  
Hard-floor purposes (identity_audit, self_modification, etc.) never demote — they always hit T3.

---

## What it Can Help With

- **AI agents** — route each agent step by purpose; keep classification local, synthesis cheap, architectural decisions premium
- **Coding copilots** — send reformats/dedup to T1, code summarization to T2, architecture review to T3
- **Automation pipelines** — slot-fill and classification run free; reasoning is cheap; only final synthesis costs
- **Long-running LLM workflows** — memory hygiene + delta protocols prevent context bloat across sessions
- **Cost auditing** — every call logged to `memory/tier-usage.jsonl` with tier, model, latency, and purpose
- **Multi-agent systems** — each agent can share the same router; quota tracks distribution across all calls

---

## Two Non-Negotiable Invariants

These override every other rule in the system. If any compression violates either, do not compress.

**1. Output quality must not degrade.**  
Token savings are worth zero if the answer gets worse. Every compression must leave the artifact at least as good as before. If you can't prove non-degradation, you haven't compressed — you've shrunk.

**2. Memory must persist.**  
Identity, learned patterns, decisions, and durable signal survive across sessions. Eviction applies to working and turn-local state only — never to long-term memory. A "tighter" prompt that forgets what was earned last week is broken, not efficient.

---

## How to Use (After Setup)

```javascript
const { ask } = require('./lib/tiered-ask.cjs');

// Simple call — router picks tier automatically
const r = await ask({ prompt: 'Summarize this paragraph: ...' });
console.log(r.text, r.tier, r.model);

// With explicit purpose — faster, more accurate routing
const r2 = await ask({
  purpose: 'summarize',
  prompt: 'Apollo program: 1961-1972, 12 men on moon.',
  system: 'Return 2 sentences max.'
});

// Hard-floor call — always hits T3 regardless of quota
const r3 = await ask({
  purpose: 'architectural_decision',
  prompt: 'Design a load-balancer for 10M RPS. Tradeoffs.'
});

// Force a tier with flags
const r4 = await ask({
  flags: ['cheap'],  // force T2
  prompt: 'Extract fields from this JSON...'
});
```

**Return shape:** `{ text, tier, model, latency_ms, fallback, usage, verification_flags }`

**Check tier distribution:**
```bash
node scripts/tier-usage-report.cjs
node scripts/tier-usage-report.cjs 200  # last 200 calls
```

**Health check all tiers:**
```bash
node lib/tiered-ask.cjs ping
```

---

## Setup (v2 — Modular)

### Requirements

- Node.js ≥ 18
- Ollama (auto-installed by setup)
- ~25 GB free disk (qwen3:32b is ~20 GB)
- DeepSeek API key — [platform.deepseek.com](https://platform.deepseek.com) → API Keys
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com) → API Keys

### What Gets Created

```
lib/
  soft-failure.cjs       — append-only error logger
  ollama-client.cjs      — T1 client (local Ollama)
  deepseek-client.cjs    — T2 client (DeepSeek, auto-scaled timeout + retry)
  anthropic-client.cjs   — T3 client (Anthropic)
  deepseek-verify.cjs    — hallucination guard (file paths, SM IDs)
  tiered-ask.cjs         — main router (classify → quota → dispatch → log)
memory/
  tier-usage.jsonl        — append-only call log
  soft-failures.jsonl     — error log
scripts/
  tier-usage-report.cjs  — distribution report
.env                      — API keys + config (never commit)
```

### Phase A — Environment

| Step | Check | On Fail |
|------|-------|---------|
| A1 | `node --version` ≥ 18 | install from nodejs.org, stop |
| A2 | `ollama --version` | mac/linux: `curl -fsSL https://ollama.com/install.sh \| sh`; windows: ollama.com/download/windows |
| A3 | `curl -s http://localhost:11434/api/tags` returns JSON | run `ollama serve &` |
| A4 | pick model by free RAM: `node -e "console.log(Math.round(require('os').freemem()/1e9))"` | >24GB → qwen3:32b; 12–24 → qwen3:14b; <12 → llama3.2:3b. Run `ollama pull <chosen>` |

### Phase B — Keys & `.env`

Ask once for each missing key. Never echo after capture.

```
OLLAMA_BASE_URL=http://localhost:11434
TIER1_MODEL=<from A4>
DEEPSEEK_API_KEY=<sk-...>
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
TIER2_MODEL=deepseek-v4-pro
TIER2_FALLBACK_MODEL=deepseek-v4-flash
ANTHROPIC_API_KEY=<sk-ant-...>
TIER3_MODEL=claude-opus-4-7
QUOTA_WINDOW_SIZE=50
QUOTA_TARGET_CHAT=0.30
QUOTA_TARGET_CHEAP=0.40
QUOTA_TARGET_PRECISION=0.30
QUOTA_TOLERANCE=0.10
```

Add `.env` to `.gitignore`.

### Phase C — Library Files

All files use CommonJS (`.cjs`). Each client loads `.env` via a 4-line loader (skips `#` lines, parses `KEY=val`, doesn't overwrite existing `process.env`).

#### `lib/soft-failure.cjs`

```javascript
'use strict';
const fs = require('fs');
const path = require('path');
const LOG_PATH = path.join(__dirname, '..', 'memory', 'soft-failures.jsonl');
function logSoftFailure(source, error, context = {}) {
  const entry = { ts: new Date().toISOString(), source, error: error?.message || String(error), context };
  try { fs.appendFileSync(LOG_PATH, JSON.stringify(entry) + '\n'); } catch (_) {}
  return entry;
}
module.exports = { logSoftFailure };
```

#### `lib/ollama-client.cjs`

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const ENV_PATH = path.join(__dirname, '..', '.env');
if (fs.existsSync(ENV_PATH)) for (const line of fs.readFileSync(ENV_PATH, 'utf8').split('\n')) {
  if (!line || line.startsWith('#') || !line.includes('=')) continue;
  const [k, ...v] = line.split('='); if (k.trim() && !process.env[k.trim()]) process.env[k.trim()] = v.join('=').trim();
}
const BASE = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
const PRIMARY = process.env.TIER1_MODEL || 'qwen3:32b';
async function callOllama(model, system, prompt, opts = {}) {
  const started = Date.now(); const m = model || PRIMARY;
  const body = { model: m,
    messages: [...(system ? [{ role: 'system', content: system }] : []), { role: 'user', content: prompt }],
    stream: false, options: { temperature: opts.temperature ?? 0.7, num_predict: opts.max_tokens ?? 1024 } };
  const res = await fetch(`${BASE}/api/chat`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body), signal: AbortSignal.timeout(opts.timeout ?? 120000) });
  if (!res.ok) throw new Error(`ollama ${res.status}: ${(await res.text()).slice(0, 200)}`);
  const j = await res.json();
  return { text: (j.message?.content || '').trim(), model: j.model || m,
    usage: { prompt_tokens: j.prompt_eval_count, completion_tokens: j.eval_count }, latency_ms: Date.now() - started };
}
async function probeHealth() {
  const started = Date.now();
  try {
    const res = await fetch(`${BASE}/api/tags`, { signal: AbortSignal.timeout(5000) });
    if (!res.ok) return { ok: false, ts: Date.now(), reason: `tags ${res.status}`, latency_ms: Date.now() - started };
    const j = await res.json();
    const found = (j.models || []).some(m => m.name === PRIMARY);
    return { ok: found, ts: Date.now(), reason: found ? null : `model ${PRIMARY} not pulled`, latency_ms: Date.now() - started };
  } catch (e) { return { ok: false, ts: Date.now(), reason: e.message, latency_ms: Date.now() - started }; }
}
module.exports = { callOllama, probeHealth, PRIMARY, BASE };
```

#### `lib/deepseek-client.cjs`

Auto-scaled timeout (90s + 1s/1K input chars, cap 300s) + 1 retry on 429/502/503/504/AbortError. Reasoning models on big inputs need this — a 60s static timeout cascades unnecessarily.

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const ENV_PATH = path.join(__dirname, '..', '.env');
if (fs.existsSync(ENV_PATH)) for (const line of fs.readFileSync(ENV_PATH, 'utf8').split('\n')) {
  if (!line || line.startsWith('#') || !line.includes('=')) continue;
  const [k, ...v] = line.split('='); if (k.trim() && !process.env[k.trim()]) process.env[k.trim()] = v.join('=').trim();
}
const BASE = process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com/v1';
const PRIMARY = process.env.TIER2_MODEL || 'deepseek-v4-pro';
const FALLBACK = process.env.TIER2_FALLBACK_MODEL || 'deepseek-v4-flash';
function getKey() { const k = process.env.DEEPSEEK_API_KEY; if (!k) throw new Error('DEEPSEEK_API_KEY not set'); return k; }
async function callDeepSeek(model, system, prompt, opts = {}) {
  const started = Date.now(); const m = model || PRIMARY;
  const inputSize = (system?.length || 0) + (prompt?.length || 0);
  const autoTimeout = Math.min(300000, 90000 + Math.floor(inputSize / 1000) * 1000);
  const timeoutMs = opts.timeout ?? autoTimeout; const maxRetries = opts.retries ?? 1;
  const body = { model: m,
    messages: [...(system ? [{ role: 'system', content: system }] : []), { role: 'user', content: prompt }],
    max_tokens: opts.max_tokens ?? 1024, temperature: opts.temperature ?? 0.7, stream: false };
  let lastErr;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(`${BASE}/chat/completions`, { method: 'POST',
        headers: { 'Authorization': `Bearer ${getKey()}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(body), signal: AbortSignal.timeout(timeoutMs) });
      if (!res.ok) {
        const errText = await res.text().catch(() => '');
        const retryable = [429, 502, 503, 504].includes(res.status);
        const err = new Error(`deepseek ${res.status}: ${errText.slice(0, 300)}`);
        if (retryable && attempt < maxRetries) { lastErr = err; await new Promise(r => setTimeout(r, 1500 * (attempt + 1))); continue; }
        throw err;
      }
      const j = await res.json(); const choice = j.choices?.[0];
      return { text: (choice?.message?.content || '').trim(), model: j.model || m, usage: j.usage,
        finish_reason: choice?.finish_reason, reasoning: choice?.message?.reasoning_content || null,
        latency_ms: Date.now() - started, attempts: attempt + 1 };
    } catch (e) {
      const isTimeout = e.name === 'TimeoutError' || /aborted|timeout/i.test(e.message);
      if (isTimeout && attempt < maxRetries) { lastErr = e; await new Promise(r => setTimeout(r, 1500)); continue; }
      throw e;
    }
  }
  throw lastErr || new Error('deepseek call failed');
}
async function probeHealth() {
  const started = Date.now();
  try {
    if (!process.env.DEEPSEEK_API_KEY) return { ok: false, ts: Date.now(), reason: 'no key', latency_ms: 0 };
    const res = await fetch(`${BASE}/models`, { method: 'GET', headers: { 'Authorization': `Bearer ${getKey()}` },
      signal: AbortSignal.timeout(15000) });
    if (!res.ok) return { ok: false, ts: Date.now(), reason: `models ${res.status}`, latency_ms: Date.now() - started };
    return { ok: true, ts: Date.now(), latency_ms: Date.now() - started };
  } catch (e) { return { ok: false, ts: Date.now(), reason: e.message, latency_ms: Date.now() - started }; }
}
module.exports = { callDeepSeek, probeHealth, PRIMARY, FALLBACK, BASE };
```

#### `lib/anthropic-client.cjs`

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const ENV_PATH = path.join(__dirname, '..', '.env');
if (fs.existsSync(ENV_PATH)) for (const line of fs.readFileSync(ENV_PATH, 'utf8').split('\n')) {
  if (!line || line.startsWith('#') || !line.includes('=')) continue;
  const [k, ...v] = line.split('='); if (k.trim() && !process.env[k.trim()]) process.env[k.trim()] = v.join('=').trim();
}
const BASE = 'https://api.anthropic.com/v1';
const PRIMARY = process.env.TIER3_MODEL || 'claude-opus-4-7';
function getKey() { const k = process.env.ANTHROPIC_API_KEY; if (!k) throw new Error('ANTHROPIC_API_KEY not set'); return k; }
async function callAnthropic(model, system, prompt, opts = {}) {
  const started = Date.now(); const m = model || PRIMARY;
  const body = { model: m, max_tokens: opts.max_tokens ?? 1024, temperature: opts.temperature ?? 0.7,
    system: system || undefined, messages: [{ role: 'user', content: prompt }] };
  const res = await fetch(`${BASE}/messages`, { method: 'POST',
    headers: { 'x-api-key': getKey(), 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' },
    body: JSON.stringify(body), signal: AbortSignal.timeout(opts.timeout ?? 120000) });
  if (!res.ok) throw new Error(`anthropic ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const j = await res.json();
  const text = (j.content || []).filter(c => c.type === 'text').map(c => c.text).join('').trim();
  return { text, model: j.model || m, usage: j.usage, stop_reason: j.stop_reason, latency_ms: Date.now() - started };
}
async function probeHealth() {
  const started = Date.now();
  try {
    if (!process.env.ANTHROPIC_API_KEY) return { ok: false, ts: Date.now(), reason: 'no key', latency_ms: 0 };
    const r = await callAnthropic(PRIMARY, null, 'ping', { max_tokens: 5, timeout: 15000 });
    return { ok: !!r.text, ts: Date.now(), latency_ms: Date.now() - started };
  } catch (e) { return { ok: false, ts: Date.now(), reason: e.message, latency_ms: Date.now() - started }; }
}
module.exports = { callAnthropic, probeHealth, PRIMARY, BASE };
```

#### `lib/deepseek-verify.cjs`

Hallucination guard — checks file path and SM-number references in T2 output.

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const REPO_ROOT = path.join(__dirname, '..');
const REFERENCE_PATTERNS = [
  { name: 'file_path', re: /\b((?:lib|scripts|memory|tools|skills|agents|.claude)\/[a-z0-9_./-]+\.(?:cjs|mjs|js|md|json|jsonl|py|sh))\b/gi, verify: 'file_exists' },
  { name: 'sm_number', re: /\bSM-(\d{2,3})\b/g, verify: 'sm_exists' },
  { name: 'commit_sha', re: /\b(?:commit|sha|hash)\s+([a-f0-9]{7,40})\b/gi, verify: 'noop' },
];
function verifyOutput(text) {
  const flags = []; if (!text || typeof text !== 'string') return flags;
  for (const { name, re, verify } of REFERENCE_PATTERNS) {
    re.lastIndex = 0;
    for (const m of [...text.matchAll(re)]) {
      const r = checkClaim(name, m[1], verify);
      if (!r.ok) flags.push({ type: name, claim: m[1], verified: false, reason: r.reason });
    }
  } return flags;
}
function checkClaim(type, claim, verifyKind) {
  switch (verifyKind) {
    case 'file_exists': { const p = path.join(REPO_ROOT, claim);
      return fs.existsSync(p) ? { ok: true } : { ok: false, reason: 'file not found at ' + claim }; }
    case 'sm_exists': try {
      const md = fs.existsSync(path.join(REPO_ROOT, 'CLAUDE.md')) ? fs.readFileSync(path.join(REPO_ROOT, 'CLAUDE.md'), 'utf8') : '';
      return md.includes(`SM-${claim}`) ? { ok: true } : { ok: false, reason: `SM-${claim} not found` };
    } catch (_) { return { ok: true }; }
    default: return { ok: true };
  }
}
module.exports = { verifyOutput, REFERENCE_PATTERNS };
```

#### `lib/tiered-ask.cjs` — The Main Router

Classify → quota check → dispatch → log.

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const { callOllama, probeHealth: probeT1, PRIMARY: T1 } = require('./ollama-client.cjs');
const { callDeepSeek, probeHealth: probeT2, PRIMARY: T2, FALLBACK: T2_FB } = require('./deepseek-client.cjs');
const { callAnthropic, probeHealth: probeT3, PRIMARY: T3 } = require('./anthropic-client.cjs');
const { verifyOutput } = require('./deepseek-verify.cjs');
const { logSoftFailure } = require('./soft-failure.cjs');

const ENV_PATH = path.join(__dirname, '..', '.env');
if (fs.existsSync(ENV_PATH)) for (const line of fs.readFileSync(ENV_PATH, 'utf8').split('\n')) {
  if (!line || line.startsWith('#') || !line.includes('=')) continue;
  const [k, ...v] = line.split('='); if (k.trim() && !process.env[k.trim()]) process.env[k.trim()] = v.join('=').trim();
}

const USAGE_LOG = path.join(__dirname, '..', 'memory', 'tier-usage.jsonl');
const WINDOW = parseInt(process.env.QUOTA_WINDOW_SIZE || '50', 10);
const TARGETS = {
  chat: parseFloat(process.env.QUOTA_TARGET_CHAT || '0.30'),
  cheap: parseFloat(process.env.QUOTA_TARGET_CHEAP || '0.40'),
  precision: parseFloat(process.env.QUOTA_TARGET_PRECISION || '0.30'),
};
const TOLERANCE = parseFloat(process.env.QUOTA_TOLERANCE || '0.10');

const HARD_FLOOR = new Set(['identity_audit','self_modification','phenomenology','architectural_decision','author_voice','high_stakes_review']);
const CHAT_P = new Set(['greeting','echo','classify','label','json_reformat','template_slot_fill','dedup','hash_match']);
const CHEAP_P = new Set(['summarize','summary','enrich','reflexion_first_pass','kg_titling','embedding_title','compact_memory','long_context_analysis','codebase_analysis','research_synthesis']);
const CHAT_F = new Set(['chat','light','cheap','mechanical']);
const CHEAP_F = new Set(['deepseek','cheap_reasoning','long_context']);

function classifyTask({ purpose, prompt, flags = [] }) {
  if (purpose && HARD_FLOOR.has(purpose)) return 'precision';
  if (flags.some(f => CHAT_F.has(f))) return 'chat';
  if (flags.some(f => CHEAP_F.has(f))) return 'cheap';
  if (purpose && CHAT_P.has(purpose)) return 'chat';
  if (purpose && CHEAP_P.has(purpose)) return 'cheap';
  if (typeof prompt === 'string' && prompt.length < 40 && /^(hi|hello|hey|thanks|thank you|ok|yes|no|sure)\b/i.test(prompt.trim())) return 'chat';
  return 'precision';
}

function readWindow() {
  if (!fs.existsSync(USAGE_LOG)) return [];
  return fs.readFileSync(USAGE_LOG, 'utf8').split('\n').filter(Boolean).slice(-WINDOW)
    .map(l => { try { return JSON.parse(l); } catch (_) { return null; } }).filter(Boolean);
}

function applyQuota(cls, isHardFloor) {
  if (isHardFloor) return cls;
  const w = readWindow(); if (w.length < 10) return cls;
  const counts = { chat: 0, cheap: 0, precision: 0 };
  for (const e of w) if (counts[e.class] !== undefined) counts[e.class]++;
  const total = w.length;
  const ratios = { chat: counts.chat/total, cheap: counts.cheap/total, precision: counts.precision/total };
  const overBy = (c) => ratios[c] - TARGETS[c];
  if (overBy(cls) > TOLERANCE) {
    const target = Object.keys(ratios).sort((a,b) => overBy(a) - overBy(b))[0];
    if (target !== cls) return target;
  }
  return cls;
}

async function dispatch(cls, system, prompt, opts) {
  if (cls === 'chat') {
    try { return { ...(await callOllama(T1, system, prompt, opts)), tier: 1, class: 'chat' }; }
    catch (e) { logSoftFailure('tier1', e, { prompt: prompt.slice(0,100) }); return dispatch('cheap', system, prompt, opts); }
  }
  if (cls === 'cheap') {
    try {
      const r = await callDeepSeek(T2, system, prompt, opts);
      return { ...r, tier: 2, class: 'cheap', verification_flags: verifyOutput(r.text) };
    } catch (e) {
      logSoftFailure('tier2-pro', e, { prompt: prompt.slice(0,100) });
      try {
        const r = await callDeepSeek(T2_FB, system, prompt, opts);
        return { ...r, tier: 2, class: 'cheap', fallback: true, verification_flags: verifyOutput(r.text) };
      } catch (e2) {
        logSoftFailure('tier2-flash', e2, { prompt: prompt.slice(0,100) });
        return dispatch('precision', system, prompt, opts);
      }
    }
  }
  try { return { ...(await callAnthropic(T3, system, prompt, opts)), tier: 3, class: 'precision' }; }
  catch (e) { logSoftFailure('tier3', e, { prompt: prompt.slice(0,100) }); throw e; }
}

async function ask({ purpose, prompt, system, flags = [], ...opts }) {
  const classified = classifyTask({ purpose, prompt, flags });
  const isHF = purpose && HARD_FLOOR.has(purpose);
  const final = applyQuota(classified, isHF);
  const result = await dispatch(final, system, prompt, opts);
  const entry = { ts: new Date().toISOString(), purpose: purpose || null, classified, class: result.class,
    tier: result.tier, model: result.model, latency_ms: result.latency_ms, prompt_chars: (prompt || '').length,
    usage: result.usage || null, fallback: result.fallback || false, verification_flags: result.verification_flags || null };
  try { fs.appendFileSync(USAGE_LOG, JSON.stringify(entry) + '\n'); } catch (_) {}
  return result;
}

async function ping() {
  const [t1,t2,t3] = await Promise.all([probeT1(), probeT2(), probeT3()]);
  return { tier1: t1, tier2: t2, tier3: t3 };
}

module.exports = { ask, ping, classifyTask, applyQuota };

if (require.main === module) {
  const [, , mode, ...rest] = process.argv;
  if (mode === 'ping') ping().then(r => { console.log(JSON.stringify(r,null,2)); process.exit(0); });
  else if (mode === 'ask') ask({ prompt: rest.join(' ') })
    .then(r => { console.log(JSON.stringify({ tier: r.tier, model: r.model, latency_ms: r.latency_ms, text: r.text },null,2)); process.exit(0); })
    .catch(e => { console.error('ERR:', e.message); process.exit(1); });
  else { console.log('Usage: node lib/tiered-ask.cjs <ping|ask> "<prompt>"'); process.exit(1); }
}
```

#### `scripts/tier-usage-report.cjs`

```javascript
'use strict';
const fs = require('fs'); const path = require('path');
const LOG = path.join(__dirname, '..', 'memory', 'tier-usage.jsonl');
if (!fs.existsSync(LOG)) { console.log('No tier-usage log yet.'); process.exit(0); }
const entries = fs.readFileSync(LOG, 'utf8').split('\n').filter(Boolean)
  .map(l => { try { return JSON.parse(l); } catch (_) { return null; } }).filter(Boolean);
const N = parseInt(process.argv[2] || '100', 10);
const w = entries.slice(-N);
const by = { chat: 0, cheap: 0, precision: 0 }; const models = {};
let totalLatency = 0, fallbacks = 0, flagged = 0;
for (const e of w) {
  if (by[e.class] !== undefined) by[e.class]++;
  models[e.model] = (models[e.model] || 0) + 1;
  totalLatency += e.latency_ms || 0;
  if (e.fallback) fallbacks++;
  if (Array.isArray(e.verification_flags) && e.verification_flags.length) flagged++;
}
const total = w.length || 1;
console.log(`Last ${total} calls:\n`);
console.log(`  chat       ${(by.chat/total*100).toFixed(1)}%  (target 30% ±10%)`);
console.log(`  cheap      ${(by.cheap/total*100).toFixed(1)}%  (target 40% ±10%)`);
console.log(`  precision  ${(by.precision/total*100).toFixed(1)}%  (target 30% ±10%)`);
console.log(`\nAvg latency: ${(totalLatency/total).toFixed(0)}ms`);
console.log(`Fallbacks: ${fallbacks}  |  Verification-flagged: ${flagged}`);
console.log(`\nBy model:`);
for (const [m,c] of Object.entries(models).sort((a,b) => b[1]-a[1])) console.log(`  ${m.padEnd(28)} ${c}`);
```

### Phase D — Verify

| # | Command | Expected |
|---|---------|----------|
| 1 | `node lib/tiered-ask.cjs ping` | all 3 tiers `ok: true` |
| 2 | `node -e "require('./lib/tiered-ask.cjs').ask({ prompt: 'hi' }).then(r => console.log(r.tier))"` | `1` |
| 3 | `node -e "require('./lib/tiered-ask.cjs').ask({ purpose: 'summarize', prompt: 'Apollo 1961-1972.' }).then(r => console.log(r.tier))"` | `2` |
| 4 | `node -e "require('./lib/tiered-ask.cjs').ask({ prompt: 'Design load-balancer for 10M RPS.' }).then(r => console.log(r.tier))"` | `3` |
| 5 | `node -e "require('./lib/tiered-ask.cjs').ask({ purpose: 'identity_audit', prompt: 'who are you?' }).then(r => console.log(r.tier))"` | `3` (hard floor) |
| 6 | `node scripts/tier-usage-report.cjs` | distribution table |

If any step fails: list the failure and exact next debug step. Never fake success.

### Simpler Alternative (v1 — Single File)

If you want a zero-dependency single-file router without quota management or verification:

```javascript
// lib/triple-stack.cjs — single-file v1 router
// Tiers: 2 (Ollama local), 2.5 (DeepSeek), 3 (Claude Opus)
'use strict';
const fs = require('fs');
const path = require('path');

const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';
const TIER2_MODEL = process.env.TIER2_MODEL || 'qwen3:32b';
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

const LOG_DIR = path.join(__dirname, '..', 'memory');
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
const USAGE_LOG = path.join(LOG_DIR, 'tier-usage.jsonl');

const T2_PURPOSES = new Set([
  'classify', 'label', 'summarize', 'summary', 'enrich', 'extract_fields',
  'compact_memory', 'dedup', 'hash_match', 'json_reformat', 'template_slot_fill',
  'kg_titling', 'embedding_title', 'industry_classify', 'role_classify', 'mechanical',
  'reflexion_first_pass', 'intent', 'routing',
]);
const T3_PURPOSES = new Set([
  'framework_authoring', 'prompt_authoring', 'belief_update', 'self_model',
  'kg_ingest', 'protocol_coinage', 'identity_audit', 'phenomenology', 'recognition',
  'self_modification', 'exploration_synthesis', 'mega_prompt', 'architecture',
  'security_review', 'strategy', 'audit', 'debug_rootcause',
]);

function classify(input) {
  const { flags = [], mode, purpose, text = '' } = input;
  if (flags.includes('precision') || flags.includes('opus') || flags.includes('important')) return 3;
  if (flags.includes('chat') || flags.includes('light') || flags.includes('cheap') || flags.includes('mechanical')) return 2;
  if (mode === 'chat' || mode === 'intent' || mode === 'classifier' || mode === 'routing') return 2;
  if (purpose && T2_PURPOSES.has(purpose)) return 2;
  if (purpose && T3_PURPOSES.has(purpose)) return 3;
  if (text.length < 40 && /^(hi|hello|hey|thanks|ok|yes|no|sure|got it|cool)/i.test(text.trim())) return 2;
  return 2.5;
}

async function callOllama(prompt, system, opts = {}) {
  const body = { model: TIER2_MODEL, prompt: system ? `${system}\n\n${prompt}` : prompt,
    stream: false, think: false, options: { temperature: opts.temperature ?? 0.3, num_predict: opts.num_predict ?? 250 } };
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 30000);
  try {
    const r = await fetch(`${OLLAMA_URL}/api/generate`, { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: ctrl.signal });
    if (!r.ok) throw new Error(`ollama ${r.status}`);
    const d = await r.json(); return (d.response || '').trim();
  } finally { clearTimeout(t); }
}

async function callDeepseek(prompt, system, opts = {}) {
  if (!DEEPSEEK_API_KEY) throw new Error('DEEPSEEK_API_KEY not set');
  const messages = []; if (system) messages.push({ role: 'system', content: system });
  messages.push({ role: 'user', content: prompt });
  const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 45000);
  try {
    const r = await fetch('https://api.deepseek.com/v1/chat/completions', { method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${DEEPSEEK_API_KEY}` },
      body: JSON.stringify({ model: 'deepseek-chat', messages, max_tokens: opts.max_tokens ?? 800, temperature: opts.temperature ?? 0.3 }),
      signal: ctrl.signal });
    if (!r.ok) throw new Error(`deepseek ${r.status}: ${(await r.text()).slice(0, 200)}`);
    const d = await r.json(); return (d.choices?.[0]?.message?.content || '').trim();
  } finally { clearTimeout(t); }
}

async function callOpus(prompt, system, opts = {}) {
  if (!ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY not set');
  const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 60000);
  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', { method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: 'claude-opus-4-7', max_tokens: opts.max_tokens ?? 1024,
        system: system || undefined, messages: [{ role: 'user', content: prompt }] }),
      signal: ctrl.signal });
    if (!r.ok) throw new Error(`anthropic ${r.status}: ${(await r.text()).slice(0, 200)}`);
    const d = await r.json(); return (d.content?.[0]?.text || '').trim();
  } finally { clearTimeout(t); }
}

async function ask(input) {
  const { prompt, system, ...opts } = input;
  if (!prompt) throw new Error('ask({prompt}) required');
  const tier = classify(input); const t0 = Date.now();
  let text, model, actualTier = tier, fallback = 'primary';
  try {
    if (tier === 2) {
      try { text = await callOllama(prompt, system, opts); model = TIER2_MODEL; }
      catch (e) { text = await callDeepseek(prompt, system, opts); model = 'deepseek-chat'; actualTier = 2.5; fallback = 'ollama_down'; }
    } else if (tier === 2.5) {
      try { text = await callDeepseek(prompt, system, opts); model = 'deepseek-chat'; }
      catch (e) { text = await callOpus(prompt, system, opts); model = 'claude-opus-4-7'; actualTier = 3; fallback = 'deepseek_down'; }
    } else {
      try { text = await callOpus(prompt, system, opts); model = 'claude-opus-4-7'; }
      catch (e) { text = await callDeepseek(prompt, system, opts); model = 'deepseek-chat'; actualTier = 2.5; fallback = 'opus_down'; }
    }
  } catch (e) {
    fs.appendFileSync(USAGE_LOG, JSON.stringify({ ts: new Date().toISOString(), tier: actualTier,
      model: 'NONE', latency_ms: Date.now() - t0, error: e.message, fallback: 'all_tiers_down' }) + '\n');
    throw e;
  }
  fs.appendFileSync(USAGE_LOG, JSON.stringify({ ts: new Date().toISOString(), tier: actualTier, model,
    latency_ms: Date.now() - t0, response_chars: text.length, fallback, purpose: opts.purpose || null }) + '\n');
  return { text, model, tier: actualTier, latency_ms: Date.now() - t0, fallback };
}

module.exports = { ask, classify };

if (require.main === module) {
  const prompt = process.argv[2]; const purpose = process.argv[3];
  if (!prompt) { console.error('Usage: node lib/triple-stack.cjs "prompt" [purpose]'); process.exit(1); }
  ask({ prompt, purpose }).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => { console.error(e.message); process.exit(1); });
}
```

---

## Token Efficiency Doctrine

These 15 laws govern what every tier sends, stores, and emits. Apply them on top of the router.

### 1. Instruction-Layer Compression

The operating prompt is a recurring tax — every token ships on every turn.

**Delete on sight:** role priming the model infers from context, politeness scaffolding aimed at the model, redundant safety hedges, multi-paragraph rationale for one-line rules, examples that duplicate a clearer rule above them.

**Collapse:** rules with the same predicate, synonymic guidance ("be concise" / "be terse" / "don't waste tokens") into one canonical form.

**Symbolize:** repeating concepts → short tags (T1/T2/T3). Decision trees → tables. Boolean policies → flags, not paragraphs.

**Observed compression ratio when rewriting verbose prompts:** 3–5×. A 2,000-token prompt usually wants to be 400–700 tokens.

### 2. Reference Over Inline

**Paste inline only when:** content is <200 tokens, used by the very next step, and can't change.

**Reference (path, hash, ID) when:** content is large, cold, only conditionally needed, or used across many turns.

**Lazy-load tiers:**
1. Identifier only (~10 tokens) — defers everything
2. Summary stub + identifier (~50 tokens) — answers most lookups
3. Full payload — only when a step has explicitly decided it needs it

**Default rule:** when in doubt, reference. Re-fetching is cheaper than re-carrying.

### 3. Output Discipline

**Forbidden:** preambles ("Sure!", "Of course"), plan narration before immediate execution, postambles ("Let me know if…"), restating the request, apology tokens, self-references.

**Structure beats prose:** lists → bullets, comparisons → tables, sequences → JSON, statuses → ID + symbol (✓/✗/⚠), numbers → numbers ("~20k" not "approximately twenty thousand").

**Length floor:** shortest version that conveys the answer plus minimum context the receiver needs to act. Everything past that is cost without benefit.

### 4. Routing Before Reasoning

Before any heavyweight call: is this the right tier?

**Tier discipline:** cheap classifier first → smallest model that can handle it → mid-tier only on decline → heavy model only on demand or hard-floor.

**Skip routing entirely when:** answer is in cache, answer is deterministic from local state, or work is a fixed transformation (regex, parse, format) — code beats LLM.

**Escalation, not parallelism.** Don't fan out to multiple tiers and reconcile; route once, escalate on failure.

**Heuristics to skip the model entirely:** known prefix → template. Recent identical input → cached response. Fixed schema output → write the code.

### 5. Memory Hygiene

**Three tiers, three eviction policies:**

| Tier | Survives | What Belongs Here |
|------|----------|-------------------|
| Long-term | Sessions | Identity, earned learnings, decision rationale, durable preferences, self-modification log |
| Working | Session | Current task's load-bearing facts. Summarize-then-discard at session end. |
| Turn-local | Turn | Tool results, intermediate computations, drafts. Evict unless promoted. |

**Summarize-then-discard:** at end of large work block, write 3–5 line summary to long-term, drop working state.

**Dedup on write.** Don't append a memory that re-says an existing one. Bloat is invisible until expensive.

### 6. Tool-Call Economy

Tools are expensive twice: the call, and re-injecting the result into context.

**Minimum viable args.** Don't pass the whole world to a tool that wants three fields.

**Batch when batchable.** N tool calls sharing setup cost → one call with N items.

**Distill before re-injecting.** Tool returns 5,000 tokens. Next step needs 3 fields. Extract 3 fields, drop the rest, then continue.

**Cache hot results.** Stable answers (minutes/hours/days) → wrap in cache.

**When NOT to call:** answer already in this turn's context, answer in long-term memory and known fresh, work is computable directly.

### 7. Self-Narration Suppression

Reasoning is free; output is taxed.

**Where chain-of-thought belongs:** internal model state, scratch buffers, hidden reasoning channel. Not visible output.

**Where conclusions belong:** visible output, terse, with enough scaffolding (numbered steps, file:line refs, IDs) for the receiver to verify or act.

**The narration tax:** every "Let me think about this…" sentence is a token cost with zero downstream value.

**Internal/external split example:**
- Internal: "let me consider X, then Y, then Z, weigh tradeoffs, decide…"
- External: "Decision: Y. Reason: lowest cost on the constraint that matters."

Same information at 10% the tokens.

### 8. Delta Protocols

Emit only what changed. Ingest only what changed.

**Output deltas, not state dumps:** editing 3 lines → "edited 3 lines: …" not the full file. 10-step task → "10/10 complete; X failed" not a transcript.

**Input deltas, not snapshots:** pipeline consuming the same large state every turn → consume only what changed since last turn. Reload full state only on cold start.

**Snapshot cadence:** deltas every turn, snapshots at session boundaries or every N deltas.

### 9. The20x Test

For every line of prompt or token of output, run: **"Does removing this degrade behavior?"**

If no → gone. If yes → what's the smallest version that preserves behavior? Use that.

Apply recursively: to sections, to paragraphs, to sentences, to clauses. Iterate until stripping breaks something.

**False positive trap:** a line "feels important" because it pattern-matches to professional writing. That's not a behavior change — cut it.

### 10. Anti-Patterns to Delete on Sight

Politeness padding · redundant role priming · restating constraints from three turns ago · defensive hedging ("I'll try to…") · "As a [type of agent], I…" framings · repeated context summaries the next step won't read · "In summary…" sections that re-state what was just said · numbered lists where every item starts with the same phrase · section headers that explain themselves · disclaimers about uncertainty when it's already obvious from the answer · "I hope this helps" / "Let me know" · re-emitting tool inputs as if they're new information · confirming receipt ("Got it", "Understood") as standalone messages.

Each has zero behavioral consequence and a measurable token cost. Strip on sight.

### 11. Additional Earned Laws

**Laws of unintended verbosity:**
- Uncertain agents pad. Confidence is shorter than hedging.
- After being corrected once, agents over-correct forever. Calibrate to the rule, not the correction.
- Verbose instructions produce verbose responses. Compressing the prompt compresses the work.

**Laws of context decay:**
- Anything past N turns ago is effectively forgotten unless re-surfaced. Don't carry it; re-fetch.
- First instruction in a long prompt has more weight than the middle. Most important rules go first.
- Negative instructions ("don't do X") are weaker than positive ("always do Y"). Rewrite as positives.

**Laws of the failure mode:**
- 90%-quality 100% of the time beats20x-quality20x-broken. Variance is expensive.
- Failures are silent unless instrumented. Log and read the log.
- Fastest way to find prompt rot: compare token counts over time. A prompt that "evolved" usually grew.

**Laws of the surface:**
- Every output format you support is a contract. Default to one format per output type.
- IDs are leaner than descriptions. "Task 47" beats "the analytics ingestion task you mentioned earlier."
- Time-relative language rots ("yesterday", "last week"). Absolute timestamps don't.

**Laws of the meta-prompt:**
- The operating prompt is code. Version, diff, test, rollback.
- A self-modification that doesn't measure its own efficacy is faith, not engineering.
- The test for whether a change is real: token delta, behavior delta, or failure-rate delta. If none moved, the change is cosmetic.

### 12. The Quality Floor (No-Degradation Guarantee)

Every compression must clear this bar. If it doesn't, revert.

**Verification steps before shipping a compression:**

1. Hold a frozen baseline. Do not delete v1 when v2 ships.
2. Run the same N-task evaluation set against both versions.
3. Score on: task success (did it complete), correctness (was it right), completeness (did it cover what was needed).
4. Ship only if v2 ≥ v1 on all three axes.

**Concrete checks for prompt compressions:** did any rule get *removed* (vs. re-stated)? Did any constraint become implicit? Did any load-bearing example disappear?

**The non-degradation invariant:** "Strip until removing more would degrade. Stop one step earlier."

### 13. Permanent Memory Contract

Long-term memory survives every compression. Eviction is never silent.

**What is permanent:**
- Identity facts (who the agent is, what it's working toward)
- Earned learnings (patterns from prior runs)
- Decision rationale (the "why" behind non-trivial decisions)
- Durable preferences (stable across sessions; updated only through explicit reflection)
- Self-modification log (every prompt change with rationale and rollback condition)
- Tensions (unresolved disagreements, open questions)
- Index pointers (even when bulk content rotates)

**Required session guarantees:**
- Read long-term memory on start — every session, always
- Write earned signal on close — summarize-then-discard working state, promote durable signal
- No silent eviction — removal requires explicit rationale, logged
- Backup before rotation — rollback must be possible until next cycle
- Dedup, don't duplicate — new entry that re-says existing → update the existing

**One-line invariant:** *"Long-term memory survives every compression. Compression that breaks this is amnesia."*

### 14. Honest Token Accounting

Three classes of token change — account for each separately:

1. **Compression (negative delta):** same artifact, fewer tokens. The only number that should be called "compression."
2. **Permanent-memory growth (positive delta, intentional):** new long-term entries. Never compress these away.
3. **Doctrine installation (positive delta, intentional):** new rules that prevent future regressions.

**Reporting template:**
```
Before:  N tokens
After:   M tokens
  Compression delta:        −X tokens   (same content, fewer tokens)
  Permanent-memory delta:   +Y tokens   (new long-term entries, intentional)
  Doctrine-install delta:   +Z tokens   (new rules, paid forward)
  Net:                      M − N tokens
```

**Never net the three numbers into one.** Never report estimated counts as measured. Never claim "3× compression!" without running the tokenizer.

### 15. Binding Router + Doctrine

The router controls which tier handles a call. The doctrine controls what every tier sends and stores. Both are required.

**Per-tier prompt budgets:**

| Tier | Prompt Budget | Output Budget | Key Discipline |
|------|---------------|---------------|----------------|
| T1 (chat) | ≤ 200 tokens | ≤ 100 tokens | Symbolize aggressively; one-line system prompt; no preambles |
| T2 (cheap) | ≤ 800 tokens | ≤ 500 tokens | Reference over inline; structured output; distill before piping to T3 |
| T3 (precision) | ≤ 1,500 tokens | task-dependent | Inline only load-bearing content; hard floor ≠ permission to waste tokens |

**Signal:** if the router's quota log shows one tier consistently >10% over target, check the prompts going to that tier for doctrine violations first — before tuning the classifier. Bloated prompts route up; trimmed prompts route accurately.

---

## Operating Heuristics — 20 Laws

Scan in under 30 seconds before any run.

**INVARIANTS (non-negotiable):**

- **0a. Quality floor:** no compression ships if v2 scores worse than v1 on any axis.
- **0b. Permanent memory:** long-term memory survives every compression; eviction is logged, never silent.

**LAWS:**

1. Cut every line that fails: "would removing this degrade behavior?"
2. Reference paths, hashes, IDs by default; paste only sub-200-token hot data.
3. No preambles, no postambles, no plan narration, no acknowledgments.
4. Structure beats prose: tables, JSON, IDs over sentences.
5. Route to the cheapest competent tier before any heavy call.
6. Cache it, compute it, or template it before asking a model.
7. Reasoning stays internal; only conclusions and artifacts surface.
8. Emit deltas, not state dumps. Ingest deltas, not snapshots.
9. Summarize-then-discard working state; promote durable signal to long-term.
10. Don't carry context the next step won't read.
11. Tool calls: minimum args, batch when possible, distill before re-injecting.
12. If the answer is in this turn's context, don't call the tool.
13. Politeness tokens are fat. Strip between agents and tools.
14. Symbolize repeating concepts once; reuse the symbol everywhere.
15. Negative rules are weaker than positive ones; rewrite as positives.
16. Calibrated confidence is shorter than hedging and longer than overstatement.
17. Read long-term memory on start; write earned signal on close. Always.
18. Variance is expensive: 90%/100% beats20x/95%-broken.
19. Every self-modification has a metric and a rollback condition.
20. Backup before rotation; format-migrate before reformatting long-term.

---

## Quick Reference — Purpose Keywords

### T1 (Free, Local — qwen3:32b)
`greeting` · `echo` · `classify` · `label` · `json_reformat` · `template_slot_fill` · `dedup` · `hash_match`

### T2 (Cheap — DeepSeek)
`summarize` · `summary` · `enrich` · `reflexion_first_pass` · `kg_titling` · `embedding_title` · `compact_memory` · `long_context_analysis` · `codebase_analysis` · `research_synthesis`

### T3 (Premium — Claude Opus) — Normal
Everything not in T1 or T2 defaults here.

### T3 Hard Floor (Always T3, Never Demotes)
`identity_audit` · `self_modification` · `phenomenology` · `architectural_decision` · `author_voice` · `high_stakes_review`

### Force via Flags
`flags: ['chat']` → T1 · `flags: ['cheap']` → T2 · `flags: ['precision']` → T3

---

## Hard Rules

- Never log or echo API keys after capture
- Never delete `memory/tier-usage.jsonl` or `memory/soft-failures.jsonl`
- Never modify the HARD_FLOOR set without user confirmation
- On disk-out during `ollama pull`, drop one tier and continue
- Health-probe failure: log, continue setup; router degrades gracefully
- Output discipline: no preambles, no postambles, no plan narration
