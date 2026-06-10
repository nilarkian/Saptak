---
layout: blank
title: "RCM Drill"
permalink: /notes/rcm/drill
---
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Syne:wght@700;800&display=swap" rel="stylesheet">

<style>
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#f7f7f7;--fg:#111;--fg2:#555;--border:#ccc;--border-strong:#111;
  --accent:#4e9fd4;--success:#788C5D;--danger:#B04A3F;
  --card-bg:#fff;--pill-bg:#f0f0f0;
}
body.dark{
  --bg:#1e1e1e;--fg:#d4d4d4;--fg2:#888;--border:#3e3e42;--border-strong:#555;
  --card-bg:#252526;--pill-bg:#2d2d30;
}
body{
  font-family:'EB Garamond',Georgia,serif;
  background:var(--bg);color:var(--fg);
  min-height:100vh;
  transition:background .2s,color .2s;
}
a{color:var(--accent);text-decoration:none;}
button{cursor:pointer;font-family:'Syne',Arial,sans-serif;}

/* ── LAYOUT ── */
.wrap{max-width:700px;margin:0 auto;padding:40px 24px 80px;}

/* ── TOPBAR ── */
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:40px;
}
.topbar-left{display:flex;align-items:center;gap:12px;}
.back-link{
  font-family:'Syne',Arial,sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;color:var(--fg2);
  border:1px solid var(--border);border-radius:999px;padding:6px 14px;
  transition:.15s;
}
.back-link:hover{border-color:var(--fg);color:var(--fg);}
.page-title{
  font-family:'Syne',Arial,sans-serif;font-size:22px;font-weight:800;
  letter-spacing:-0.5px;
}
#theme-btn{
  width:32px;height:32px;border-radius:50%;
  border:1px solid var(--border);background:var(--card-bg);
  display:flex;align-items:center;justify-content:center;
  font-size:15px;transition:.15s;
}
#theme-btn:hover{border-color:var(--fg);}

/* ── CONTROLS ── */
.controls{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  margin-bottom:28px;
}
.pill-btn{
  font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  border:1.5px solid var(--border);border-radius:999px;
  padding:6px 14px;background:transparent;color:var(--fg2);
  transition:.15s;
}
.pill-btn:hover,.pill-btn.active{
  border-color:var(--fg);color:var(--fg);background:var(--pill-bg);
}
.pill-btn.active{background:var(--fg);color:var(--bg);}
select.pill-select{
  font-family:'Syne',Arial,sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;
  border:1.5px solid var(--border);border-radius:999px;
  padding:6px 14px;background:transparent;color:var(--fg2);
  outline:none;cursor:pointer;appearance:none;
  -webkit-appearance:none;
  padding-right:28px;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23888'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center;
}
select.pill-select:hover{border-color:var(--fg);color:var(--fg);}
.score-label{
  font-family:'Syne',Arial,sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;color:var(--fg2);
  margin-left:auto;
}
.score-label span{color:var(--fg);}

/* ── PROGRESS BAR ── */
.deck-progress{
  height:3px;background:var(--border);border-radius:2px;margin-bottom:28px;
  overflow:hidden;
}
.deck-progress-fill{
  height:100%;background:var(--accent);border-radius:2px;
  transition:width .3s ease;
}

/* ── CARD ── */
.card-wrap{perspective:1200px;margin-bottom:28px;}
.card{
  position:relative;
  min-height:200px;
  background:var(--card-bg);
  border:2px solid var(--border);
  border-radius:16px;
  padding:36px 32px;
  cursor:pointer;
  transition:border-color .2s,box-shadow .2s;
  transform-style:preserve-3d;
  transition:transform .4s ease, border-color .2s;
  user-select:none;
}
.card:hover{border-color:var(--border-strong);box-shadow:0 4px 20px rgba(0,0,0,.08);}
.card.flipped{transform:rotateY(180deg);}
.card-face{
  position:absolute;top:0;left:0;right:0;bottom:0;
  backface-visibility:hidden;
  -webkit-backface-visibility:hidden;
  display:flex;flex-direction:column;justify-content:center;
  padding:36px 32px;border-radius:14px;
}
.card-back{transform:rotateY(180deg);}
.card-cat{
  font-family:'Syne',Arial,sans-serif;font-size:10px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
  margin-bottom:14px;
}
.card-text{
  font-size:20px;line-height:1.7;
}
.card-hint{
  font-family:'Syne',Arial,sans-serif;font-size:11px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--fg2);
  margin-top:20px;
}
body.dark .card{background:var(--card-bg);border-color:var(--border);}

/* ── MCQ OPTIONS ── */
.mcq-options{display:none;flex-direction:column;gap:10px;margin-bottom:24px;}
.mcq-options.visible{display:flex;}
.mcq-opt{
  font-size:16px;line-height:1.5;
  background:var(--card-bg);border:1.5px solid var(--border);
  border-radius:10px;padding:12px 18px;text-align:left;
  transition:.15s;color:var(--fg);
}
.mcq-opt:hover:not([disabled]){border-color:var(--accent);background:rgba(78,159,212,.06);}
.mcq-opt.correct{border-color:var(--success);background:rgba(120,140,93,.08);color:var(--success);}
.mcq-opt.wrong{border-color:var(--danger);background:rgba(176,74,63,.06);color:var(--danger);}
.mcq-opt[disabled]{cursor:not-allowed;opacity:.75;}

/* ── FLIP ACTIONS ── */
.flip-actions{
  display:none;gap:12px;margin-bottom:28px;
}
.flip-actions.visible{display:flex;}
.action-btn{
  flex:1;padding:12px;border-radius:10px;
  font-size:13px;font-weight:700;letter-spacing:.04em;
  border:2px solid;transition:.15s;
}
.btn-known{border-color:var(--success);color:var(--success);background:transparent;}
.btn-known:hover{background:var(--success);color:#fff;}
.btn-unknown{border-color:var(--danger);color:var(--danger);background:transparent;}
.btn-unknown:hover{background:var(--danger);color:#fff;}

/* ── NEXT / NAV ── */
.nav-row{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:40px;gap:12px;
}
.nav-btn{
  font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  border:2px solid var(--border-strong);border-radius:999px;
  padding:9px 22px;background:transparent;color:var(--fg);
  transition:.15s;
}
.nav-btn:hover{background:var(--fg);color:var(--bg);}
.nav-btn:disabled{opacity:.3;cursor:not-allowed;}
.card-counter{
  font-family:'Syne',Arial,sans-serif;font-size:13px;
  color:var(--fg2);
}

/* ── COPY PROMPT ── */
.copy-section{
  border:2px solid var(--border);border-radius:14px;padding:24px 28px;
  margin-top:12px;
}
.copy-section h3{
  font-family:'Syne',Arial,sans-serif;font-size:14px;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;margin-bottom:8px;
}
.copy-section p{font-size:15px;line-height:1.6;color:var(--fg2);margin-bottom:16px;}
.copy-btn-main{
  font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  border:2px solid var(--border-strong);border-radius:999px;
  padding:10px 22px;background:transparent;color:var(--fg);
  transition:.15s;
}
.copy-btn-main:hover{background:var(--fg);color:var(--bg);}

/* ── DONE STATE ── */
.done-banner{
  text-align:center;padding:48px 24px;
  border:2px solid var(--border);border-radius:16px;
  margin-bottom:28px;
}
.done-banner h2{
  font-family:'Syne',Arial,sans-serif;font-size:24px;font-weight:800;
  margin-bottom:12px;
}
.done-banner p{font-size:17px;color:var(--fg2);line-height:1.7;}
</style>

<div class="wrap">

  <!-- TOPBAR -->
  <div class="topbar">
    <div class="topbar-left">
      <a class="back-link" href="{{ '/notes/1234' | relative_url }}">← Index</a>
      <a class="back-link" href="{{ '/notes/rcm/cheatsheet' | relative_url }}">📋 Cheat-sheet</a>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <div class="page-title">Drill</div>
      <button id="theme-btn" aria-label="toggle theme">🌙</button>
    </div>
  </div>

  <!-- CONTROLS -->
  <div class="controls">
    <button class="pill-btn active" id="btn-flip">Flashcard</button>
    <button class="pill-btn" id="btn-quiz">Quiz (MCQ)</button>
    <select class="pill-select" id="cat-select" aria-label="category filter">
      <option value="all">All topics</option>
      <option value="Participants">Participants</option>
      <option value="HIPAA">HIPAA</option>
      <option value="Payers">Payers</option>
      <option value="ManagedCare">Managed Care</option>
      <option value="Providers">Providers</option>
      <option value="Coding">Coding</option>
      <option value="Claims">Claims</option>
      <option value="PatientResp">Patient Resp.</option>
    </select>
    <button class="pill-btn" id="btn-shuffle">⟳ Shuffle</button>
    <button class="pill-btn" id="btn-reset" style="color:#B04A3F;border-color:#B04A3F;">Reset</button>
    <div class="score-label" id="score-label" style="display:none">Score: <span id="score-val">0/0</span></div>
  </div>

  <!-- PROGRESS BAR -->
  <div class="deck-progress"><div class="deck-progress-fill" id="deck-fill" style="width:0%"></div></div>

  <!-- CARD -->
  <div class="card-wrap" id="card-wrap">
    <div class="card" id="card">
      <div class="card-face card-front">
        <div class="card-cat" id="card-cat"></div>
        <div class="card-text" id="card-front-text"></div>
        <div class="card-hint" id="card-hint">Click card to flip</div>
      </div>
      <div class="card-face card-back">
        <div class="card-cat" id="card-cat-b"></div>
        <div class="card-text" id="card-back-text" style="white-space:pre-line;font-size:18px;"></div>
      </div>
    </div>
    <div class="done-banner" id="done-banner" style="display:none">
      <h2>Deck complete 🎉</h2>
      <p id="done-msg"></p>
    </div>
  </div>

  <!-- MCQ OPTIONS -->
  <div class="mcq-options" id="mcq-options"></div>

  <!-- FLIP ACTIONS -->
  <div class="flip-actions" id="flip-actions">
    <button class="action-btn btn-known" id="btn-known">✓ Known</button>
    <button class="action-btn btn-unknown" id="btn-unknown">✗ Unknown</button>
  </div>

  <!-- NAV ROW -->
  <div class="nav-row">
    <button class="nav-btn" id="btn-prev" disabled>← Prev</button>
    <div class="card-counter" id="card-counter">1 / 1</div>
    <button class="nav-btn" id="btn-next">Next →</button>
  </div>

  <!-- COPY PROMPT -->
  <div class="copy-section">
    <h3>📋 Study prompt for weak areas</h3>
    <p>Marks cards you haven't mastered (Unknown or quiz misses) and builds a targeted Claude prompt.</p>
    <button class="copy-btn-main" id="btn-copy-prompt">Copy prompt to clipboard</button>
  </div>

</div><!-- /wrap -->

<script>
// ── DATA (emitted by Liquid at build time) ──────────────────────────────────
var ALL_CARDS = {{ site.data.rcm_quiz | jsonify }};

// ── STATE ───────────────────────────────────────────────────────────────────
var PROG_KEY  = 'rcm-drill-progress';
var THEME_KEY = 'note-theme';

var mode      = 'flip';   // 'flip' | 'quiz'
var cat       = 'all';
var deck      = [];       // current filtered/shuffled subset
var idx       = 0;        // position in deck
var flipped   = false;
var mcqLocked = false;    // MCQ answered, waiting for Next
var sessionRight = 0;
var sessionTotal = 0;

// progress: { [id]: { status: 'known'|'unknown'|null, seen: n, wrong: n, cat: string } }
var progress  = {};
try { progress = JSON.parse(localStorage.getItem(PROG_KEY) || '{}'); } catch(e){}

// ── THEME ───────────────────────────────────────────────────────────────────
var isDark = localStorage.getItem(THEME_KEY) === 'dark';
function applyTheme(dark){
  isDark = dark;
  document.body.classList.toggle('dark', dark);
  document.getElementById('theme-btn').textContent = dark ? '☀️' : '🌙';
  localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light');
}
applyTheme(isDark);
document.getElementById('theme-btn').addEventListener('click', function(){ applyTheme(!isDark); });

// ── DECK BUILD ──────────────────────────────────────────────────────────────
function buildDeck(){
  var filtered = cat === 'all' ? ALL_CARDS.slice() : ALL_CARDS.filter(function(c){ return c.cat === cat; });
  deck = filtered;
  idx = 0; flipped = false; mcqLocked = false;
  sessionRight = 0; sessionTotal = 0;
  render();
}

function shuffle(arr){
  for(var i = arr.length - 1; i > 0; i--){
    var j = Math.floor(Math.random() * (i+1));
    var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
  }
  return arr;
}

// ── RENDER ──────────────────────────────────────────────────────────────────
var card      = document.getElementById('card');
var cardWrap  = document.getElementById('card-wrap');
var doneBanner= document.getElementById('done-banner');
var cardCat   = document.getElementById('card-cat');
var cardCatB  = document.getElementById('card-cat-b');
var cardFront = document.getElementById('card-front-text');
var cardBack  = document.getElementById('card-back-text');
var cardHint  = document.getElementById('card-hint');
var mcqOpts   = document.getElementById('mcq-options');
var flipActs  = document.getElementById('flip-actions');
var counter   = document.getElementById('card-counter');
var deckFill  = document.getElementById('deck-fill');
var scoreLabel= document.getElementById('score-label');
var scoreVal  = document.getElementById('score-val');
var btnPrev   = document.getElementById('btn-prev');
var btnNext   = document.getElementById('btn-next');

function render(){
  var isDone = deck.length === 0 || idx >= deck.length;

  // progress bar
  var pct = deck.length ? Math.round(Math.min(idx, deck.length) / deck.length * 100) : 0;
  deckFill.style.width = pct + '%';
  counter.textContent = deck.length ? (Math.min(idx + 1, deck.length) + ' / ' + deck.length) : '0 / 0';

  // buttons
  btnPrev.disabled = (idx <= 0);
  btnNext.disabled = isDone;

  if(isDone){
    card.style.display = 'none';
    mcqOpts.classList.remove('visible');
    flipActs.classList.remove('visible');
    doneBanner.style.display = '';
    var knownCount = Object.values(progress).filter(function(p){ return p.status === 'known'; }).length;
    var totalSeen  = Object.keys(progress).length;
    document.getElementById('done-msg').textContent =
      mode === 'quiz'
        ? 'Score: ' + sessionRight + ' / ' + sessionTotal + ' correct.'
        : knownCount + ' of ' + totalSeen + ' cards marked Known.';
    return;
  }

  doneBanner.style.display = 'none';
  card.style.display = '';

  var c = deck[idx];
  var p = progress[c.id] || {};
  cardCat.textContent  = c.cat;
  cardCatB.textContent = c.cat;

  if(mode === 'flip'){
    cardFront.textContent = c.front;
    cardBack.textContent  = c.back;
    cardHint.textContent  = flipped ? '' : 'Click card to flip';
    card.classList.toggle('flipped', flipped);
    mcqOpts.classList.remove('visible');
    flipActs.classList.toggle('visible', flipped);
    scoreLabel.style.display = 'none';
  } else {
    // MCQ
    cardFront.textContent = c.q || c.front || '';
    card.classList.remove('flipped');
    cardHint.textContent = mcqLocked ? '' : 'Select an answer';
    flipActs.classList.remove('visible');
    scoreLabel.style.display = '';
    scoreVal.textContent = sessionRight + '/' + sessionTotal;

    // Build options
    mcqOpts.innerHTML = '';
    var choices = (c.choices || [c.back]).slice();
    choices.forEach(function(ch){
      var btn = document.createElement('button');
      btn.className = 'mcq-opt';
      btn.textContent = ch;
      if(mcqLocked){
        btn.disabled = true;
        if(ch === c.answer) btn.classList.add('correct');
        else if(ch === mcqLocked) btn.classList.add('wrong');
      } else {
        btn.addEventListener('click', function(){ answerMcq(ch, c); });
      }
      mcqOpts.appendChild(btn);
    });
    mcqOpts.classList.add('visible');
  }
}

function answerMcq(chosen, c){
  var correct = chosen === c.answer;
  sessionTotal++;
  if(correct) sessionRight++;
  else {
    // mark unknown on wrong answer
    var p = progress[c.id] || {status:null, seen:0, wrong:0, cat:c.cat};
    p.seen++; p.wrong++;
    if(p.status !== 'known') p.status = 'unknown';
    progress[c.id] = p;
    saveProgress();
  }
  mcqLocked = chosen;
  render();
}

function saveProgress(){
  try { localStorage.setItem(PROG_KEY, JSON.stringify(progress)); } catch(e){}
}

// ── FLIP CARD ───────────────────────────────────────────────────────────────
card.addEventListener('click', function(){
  if(mode !== 'flip' || idx >= deck.length) return;
  flipped = !flipped;
  render();
});

// ── KNOWN / UNKNOWN ──────────────────────────────────────────────────────────
document.getElementById('btn-known').addEventListener('click', function(){
  if(idx >= deck.length) return;
  var c = deck[idx];
  var p = progress[c.id] || {status:null, seen:0, wrong:0, cat:c.cat};
  p.seen++; p.status = 'known';
  progress[c.id] = p;
  saveProgress();
  advance();
});

document.getElementById('btn-unknown').addEventListener('click', function(){
  if(idx >= deck.length) return;
  var c = deck[idx];
  var p = progress[c.id] || {status:null, seen:0, wrong:0, cat:c.cat};
  p.seen++; if(p.status !== 'known') p.status = 'unknown';
  progress[c.id] = p;
  saveProgress();
  advance();
});

function advance(){
  idx++;
  flipped = false;
  mcqLocked = false;
  render();
}

// ── NAV ──────────────────────────────────────────────────────────────────────
btnNext.addEventListener('click', function(){
  if(mode === 'quiz' && !mcqLocked && idx < deck.length) return; // must answer first
  advance();
});
btnPrev.addEventListener('click', function(){
  if(idx > 0){ idx--; flipped = false; mcqLocked = false; render(); }
});

// ── MODE TOGGLE ──────────────────────────────────────────────────────────────
document.getElementById('btn-flip').addEventListener('click', function(){
  mode = 'flip';
  document.getElementById('btn-flip').classList.add('active');
  document.getElementById('btn-quiz').classList.remove('active');
  buildDeck();
});
document.getElementById('btn-quiz').addEventListener('click', function(){
  mode = 'quiz';
  document.getElementById('btn-quiz').classList.add('active');
  document.getElementById('btn-flip').classList.remove('active');
  buildDeck();
});

// ── CATEGORY FILTER ──────────────────────────────────────────────────────────
document.getElementById('cat-select').addEventListener('change', function(){
  cat = this.value;
  buildDeck();
});

// ── SHUFFLE ──────────────────────────────────────────────────────────────────
document.getElementById('btn-shuffle').addEventListener('click', function(){
  shuffle(deck);
  idx = 0; flipped = false; mcqLocked = false;
  render();
});

// ── RESET ────────────────────────────────────────────────────────────────────
document.getElementById('btn-reset').addEventListener('click', function(){
  if(!confirm('Reset all progress?')) return;
  progress = {};
  saveProgress();
  sessionRight = 0; sessionTotal = 0;
  buildDeck();
});

// ── COPY PROMPT ──────────────────────────────────────────────────────────────
document.getElementById('btn-copy-prompt').addEventListener('click', function(){
  var btn = this;
  // Gather weak cards (unknown status or wrong > 0)
  var weakBycat = {};
  ALL_CARDS.forEach(function(c){
    var p = progress[c.id];
    if(!p) return; // never seen
    if(p.status === 'unknown' || p.wrong > 0){
      if(!weakBycat[c.cat]) weakBycat[c.cat] = [];
      var label = c.front || c.q || c.id;
      weakBycat[c.cat].push(label);
    }
  });

  var lines = ['I\'m studying US Healthcare Revenue Cycle Management (RCM) for a customer support rep role.',
               'I\'m weak on the following topics — please quiz me with harder follow-up questions, then explain each:', ''];

  var cats = Object.keys(weakBycat);
  if(!cats.length){
    lines.push('[No weak areas flagged yet — mark some cards Unknown first, or miss some Quiz answers]');
  } else {
    cats.forEach(function(cat){
      lines.push('[' + cat + '] ' + weakBycat[cat].slice(0,6).join(' · '));
    });
    lines.push('');
    lines.push('Focus on practical scenarios a customer support rep would handle. After drilling each, give a one-sentence summary I can memorize.');
  }

  var prompt = lines.join('\n');

  var copyDone = function(){
    btn.textContent = '✓ Copied!';
    setTimeout(function(){ btn.textContent = 'Copy prompt to clipboard'; }, 2000);
  };

  if(navigator.clipboard){
    navigator.clipboard.writeText(prompt).then(copyDone).catch(function(){
      fallbackCopy(prompt); copyDone();
    });
  } else {
    fallbackCopy(prompt); copyDone();
  }
});

function fallbackCopy(text){
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;opacity:0;';
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
}

// ── INIT ─────────────────────────────────────────────────────────────────────
buildDeck();
</script>
