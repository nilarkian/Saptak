---
layout: note-layout
title: "RCM Master Cheat-Sheet"
topic: "RCM"
permalink: /notes/rcm/cheatsheet
series_index: /notes/1234
date: 2026-06-10
description: "Continuously-evolving quick-reference — every key RCM fact on one page. Blur answers to self-quiz."
---

> [!tip] How to use
> Click **🙈 Blur answers** to hide the right column — test yourself row by row, then click any cell to reveal it. Evolving = append a row to `_data/rcm_cheatsheet.yml` and rebuild.

<div style="margin:0 0 40px;">
  <button id="blur-toggle" style="font-family:'Syne',Arial,sans-serif;font-size:13px;font-weight:700;letter-spacing:.05em;border:2px solid #111;padding:9px 20px;border-radius:999px;background:transparent;cursor:pointer;transition:.2s;" onmouseover="this.style.background='#111';this.style.color='#f7f7f7'" onmouseout="if(!window._blurActive){this.style.background='transparent';this.style.color='inherit'}">🙈 Blur answers</button>
</div>

<style>
td.ans-col { transition: filter .18s; }
td.ans-col.blurred { filter: blur(6px); cursor: pointer; user-select: none; }
td.ans-col.blurred:hover { filter: blur(3px); }
</style>

{% for section in site.data.rcm_cheatsheet.sections %}
## {{ section.title }}

<table>
<thead><tr><th>Cue</th><th>Answer</th></tr></thead>
<tbody>
{% for row in section.rows -%}
<tr><td>{{ row.cue }}</td><td class="ans-col">{{ row.answer }}</td></tr>
{% endfor -%}
</tbody>
</table>

{% endfor %}

<script>
(function(){
  var BLUR_KEY = 'rcm-cheatsheet-blur';
  var btn = document.getElementById('blur-toggle');
  var active = localStorage.getItem(BLUR_KEY) === 'true';
  window._blurActive = active;

  function applyBlur(on) {
    active = on;
    window._blurActive = on;
    localStorage.setItem(BLUR_KEY, on);
    document.querySelectorAll('td.ans-col').forEach(function(td){ td.classList.toggle('blurred', on); });
    btn.textContent = on ? '👁 Show all answers' : '🙈 Blur answers';
    btn.style.background = on ? '#111' : 'transparent';
    btn.style.color = on ? '#f7f7f7' : '';
  }

  // Individual reveal on click
  document.querySelectorAll('td.ans-col').forEach(function(td){
    td.addEventListener('click', function(){
      if (td.classList.contains('blurred')) td.classList.remove('blurred');
    });
  });

  btn.addEventListener('click', function(){ applyBlur(!active); });

  if (active) applyBlur(true);
})();
</script>
