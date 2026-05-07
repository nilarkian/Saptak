---
id: 2026MayW1903Sun0316pm05
area:
tags: []
project:
  - "[[notes]]"
dateCreated: "[[2026-05-03]]"
source:
⬅️previous page:
---


[GitMastery - Master Git Through Play | Interactive Git Learning Platform](https://gitmastery.me/)
[Learn Git Branching](https://learngitbranching.js.org/) 
# Executive Summary  
A project to write **“How to Get Disgustingly Good at Git”** will blend theory, practice and interactive learning.  It will integrate games (like GitMastery’s levels【1†L11-L14】) and visual tools (Learn Git Branching), plus authoritative sources (the Pro Git book, official docs) and advanced tutorials (e.g. Atlassian’s articles【18†L1137-L1145】 and an advanced PDF tutorial【7†L13-L21】【7†L25-L34】).  The goal is an online, self-contained HTML playbook with step-by-step exercises, code snippets (with copy buttons), a progress checklist, and embedded interactive demos.  We will chart a **6-hour roadmap** of incremental tasks with clear checkpoints and learning goals, ensuring every minute adds insight.  

# Project Charter  
**Objective:** Create a self-contained, interactive guide to master Git, combining “learning by playing” (GitMastery, Learn Git Branching) with deep dives from official and advanced sources【18†L1137-L1145】【7†L13-L21】.  
**Scope:** Coverage from essential commands (init, commit, branch, merge) up to advanced topics (rebase vs merge, hooks, reflog, stash, submodules, internals)【18†L1152-L1161】【7†L25-L34】. We will write narrative explanations, embed exercises (Learn Git Branching), and provide runnable code examples.  **Out-of-scope:** Custom hosting or licensing beyond free resources, GUI tools, and enterprise server setup.  
**Stakeholders:** Developers (target users), tech writers, educators.  
**Timeline:** 6 hours of work, broken into focused blocks with deliverables per checkpoint.  

# Goals & Success Metrics  
- **Deliverables:** A polished HTML playbook with embedded interactive components (e.g. iframes to Learn Git Branching), code snippets (copyable), visuals (timeline, workflow flowchart), and a printable checklist.  
- **Educational Goals:** Each section teaches a Git concept, has an exercise, expected output, troubleshooting tip, and a challenge task. Learning objectives will be defined per checkpoint.  
- **Success Metrics:** 100% completion of all roadmap tasks within 6 hours; working interactive demos; positive review by a Git instructor (for correctness and clarity); readers can perform advanced Git tasks and articulate concepts (e.g. explain **plumbing vs porcelain**【17†L231-L239】).  

# Audience & Prerequisites  
**Target Audience:** Intermediate developers or computer science students who know basic version control (e.g. `git init`, `add`, `commit`) but want to level up. They should understand commits and branches.  
**Prerequisites:** Familiarity with command-line Git or willingness to learn interactively. No deep Git internals or network setups required beforehand, though comfort with a terminal and text editor is assumed.  

# Scope & Out-of-Scope  
**Included (Scope):**  
- **Basics Review:** Initializing repos, committing, branching, merging.  
- **Advanced Topics:** Rebasing vs merging, stash/cleanup, interactive rebase, cherry-pick, revert/reset, hooks, reflog, submodules, and Git internals (plumbing/porcelain)【17†L231-L239】.  
- **Interactive Components:** Use GitMastery for gamified practice【1†L11-L14】, LearnGitBranching demos for visualization, plus code walkthroughs.  
- **Documentation:** Links to Pro Git (official book) and Git’s reference manual (e.g. stashing【12†L207-L216】) for deeper reading.  
- **Assessment:** Challenge tasks (e.g. resolve a complex merge conflict) with hints.  

**Excluded (Out-of-Scope):**  
- GUI-based Git clients (only command-line).  
- In-depth server setup (e.g. GitLab admin).  
- Non-Git topics (e.g. CI/CD pipelines).  

# 6-Hour Roadmap (Tasks & Checkpoints)  
Each hour is divided into focused tasks with clear outcomes.  

| Time (min) | Task                                                                        | Checkpoint & Learning Objective                              |
|----------|----------------------------------------------------------------------------|--------------------------------------------------------------|
| 0–15     | **Plan outline:** Sketch sections; list concepts (branching, rebasing, etc.).  | CHK1: All topics planned; order set. *LO:* Understand key topics to cover. |
| 15–60    | **Basics Walkthrough:** Explain `git init`, `commit`, `branch`, `merge` with examples. Add an exercise (e.g. create and merge branches). Include expected outputs and a tip (e.g. resolve simple conflict). Code snippet with copy.  | CHK2: Basics section drafted. *LO:* User can initialize repo, make commits, and merge branches without conflicts. |
| 60–75    | **Interactive Demo:** Embed/link LearnGitBranching exercises for branching. Explain navigation. | CHK3: Interactive branching exercise embedded. *LO:* Visualize commit graph and branching in the browser. |
| 75–120   | **Intermediate Git:** Cover `rebase` (vs merge), `checkout vs switch`, `stash`, `tag`. Use narrative + examples. Include “Stash demo” citing Pro Git explanation【12†L207-L216】.  Challenge: use `rebase -i` to squash commits.  | CHK4: Intermediate section done. *LO:* User can rebase, stash changes, and know differences between reset/revert. |
| 120–150  | **Interactive Gaming:** Describe GitMastery platform and assign a level as exercise. Highlight its challenges (game context)【1†L11-L14】. | CHK5: Gamified exercise referenced. *LO:* Reinforce commands through a game environment. |
| 150–210  | **Advanced Topics:** Write about hooks, submodules, cherry-pick, bisect. Use Atlassian for context (e.g. explain hook scripts【18†L1193-L1201】, reflog【18†L1205-L1211】). Provide sample hook script.  Add troubleshooting tip (detached HEAD warning). | CHK6: Advanced topics drafted. *LO:* User understands how and why to use Git hooks, reflog, submodules. |
| 210–240  | **Git Internals (Optional):** Briefly outline .git structure (HEAD, objects, refs)【17†L271-L278】. Show `git cat-file` as example of plumbing.  Optional challenge: find a commit with `git log --graph`. | CHK7: Internals section ready. *LO:* User grasps underlying data model; can peek inside `.git/`. |
| 240–270  | **Finalizing Content:** Review narrative coherence. Ensure each section has intro, example commands (`$ git ...`), outputs, and a challenge. Draft narrative transitions. | CHK8: First draft complete. *LO:* All content flows logically with clear instructions. |
| 270–300  | **Styling & Interactive:** Build HTML template: embed CSS/JS in `<style>` and `<script>`, add copy buttons for code (sample below), add checklist (code snippet below). Ensure iframe for LearnGitBranching or link properly.  | CHK9: HTML skeleton ready with interactive elements. *LO:* Reader experiences hands-on elements. |
| 300–330  | **Resources Table:** Compile and fill table of recommended resources. (See “Resources Comparison” below.) Verify times.   | CHK10: Resource table done. *LO:* Users know which resources to use for self-study. |
| 330–360  | **Review & Polish:** Fact-check, cite sources (Atlassian【18†L1137-L1145】, Pro Git【12†L207-L216】【17†L231-L239】, PDF【7†L13-L21】). Check readability (short paragraphs, narrative style). Ensure no omitted instructions. | CHK11: Final review complete. *LO:* High-quality, concise, comprehensive content with references. |

**Learning Objectives (per Checkpoint):**  
- CHK2: Execute basic Git workflows (init, add, commit, push).  
- CHK3: Visually understand branching and merging.  
- CHK4: Safely use `rebase`, stash and reset without losing work.  
- CHK5: Reinforce knowledge via gamified practice.  
- CHK6: Use advanced features (hooks, reflog, bisect) to diagnose or streamline work.  
- CHK7: Recognize what’s inside `.git/` and use low-level plumbing commands.  
- Final: Be able to read and navigate the HTML playbook, use interactive demos, and apply Git in real projects.

# Interactive Walkthrough / Playbook Structure  
The guide will be a **single-page HTML** (self-contained CSS/JS) organized into sections.  At each step, we’ll alternate explanatory narrative with hands-on tasks:

1. **Narrative Explanation:** A short story/introduction to the concept (e.g. “Imagine you’re building a feature…”) using simple language.  
2. **Commands & Examples:** Show terminal steps in a code block, e.g.:  
   ```bash
   $ git init my-app
   $ cd my-app
   $ echo "print('Hello')" > hello.py
   $ git add hello.py
   $ git commit -m "Initial commit"
   ```
   with “Expected output” commentary below (e.g. “A commit is created with hash abc123”).  
3. **Interactive Task:** Embed or link to a Learn Git Branching level or GitMastery challenge. Provide clear instructions (“Complete Level 1 in GitMastery to practice branching【1†L11-L14】”).  
4. **Troubleshooting Tip:** e.g. “If you see *’detached HEAD’*, you likely checked out a commit instead of a branch” (common pitfall).  
5. **Challenge Task:** A quick puzzle (e.g. “Use `git rebase -i` to squash your last two commits. Then `git log` to verify.”).  
6. **Progress Checklist:** After each major section, an interactive checklist (implemented with checkboxes in HTML) lets users mark topics as done.

For example, a sample code block with a copy button (using embedded JS):  
```html
<pre><code id="cmd1">$ git branch feature\n$ git checkout feature\n$ echo '123' >> feature.txt\n$ git add feature.txt\n$ git commit -m "Add feature file"</code></pre>
<button onclick="navigator.clipboard.writeText(document.getElementById('cmd1').innerText)">Copy</button>
```  
This snippet shows commands and a “Copy” button (as per deliverable requirements).

# Recommended Resources (Comparison Table)  

| Resource                  | Purpose                    | Level              | Time to Complete     |
|---------------------------|----------------------------|--------------------|----------------------|
| **GitMastery (gitmastery.me)**【1†L11-L14】 | Gamified practice of Git basics and branching.      | Beginner/Intermediate (playful) | ~1–2 hours (levels)   |
| **Learn Git Branching** | Interactive branching simulator and puzzles. | Beginner/Intermediate | ~1 hour (multiple levels) |
| **Pro Git Book**【15†L79-L87】 | Authoritative reference and deep concepts (free online). | All (with advanced chapters) | ~8–10+ hours (read as needed) |
| **Atlassian Git Tutorials**【18†L1137-L1145】 | Practical guides (merging vs rebase, hooks, reflog, etc.). | Intermediate/Advanced | ~3–5 hours (select topics) |
| **Git – Advanced Tutorial (PDF)**【7†L13-L21】【7†L25-L34】 | Detailed advanced topics: detached HEAD, cherry-pick, bisect, rebasing history. | Advanced | ~2–3 hours (work through examples) |
| **(Optional)** Git Immersion or Atlassian’s interactive quiz | Supplement basics with hands-on exercises. | Beginner | ~1 hour |

Each resource adds value: the interactive sites for practice, the official book for deep dives, and advanced tutorials for mastery.

# HTML Template Snippet  
Below is a **simplified skeleton** of the HTML output with embedded style and script (excess detail omitted for brevity). In practice, this would be fleshed out and styled nicely.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>How to Get Disgustingly Good at Git</title>
  <style>
    /* Simple styles for code blocks and buttons */
    pre { background:#f4f4f4; padding:10px; }
    button { margin-top:5px; }
    /* Add more styles as needed */
  </style>
</head>
<body>
  <h1>How to Get Disgustingly Good at Git</h1>
  <div id="introduction">
    <p>Git is a powerful tool. In this guide, you'll learn by doing...</p>
  </div>

  <!-- Example section -->
  <h2>1. Creating a Repo and Committing</h2>
  <p>Imagine starting a new project…</p>
  <pre><code id="cmd-init">$ git init my-app
$ cd my-app
$ echo "print('Hello Git')" > hello.py
$ git add hello.py
$ git commit -m "Initial commit"</code></pre>
  <button onclick="navigator.clipboard.writeText(document.getElementById('cmd-init').innerText)">
    Copy Commands
  </button>
  <p><em>Expected output:</em> A commit is created (you’ll see a message with a commit hash).</p>
  <p><strong>Tip:</strong> If `hello.py` wasn't added, use <code>git status</code> to check untracked files.</p>

  <!-- Interactive Exercise -->
  <h3>Exercise:</h3>
  <p>Now try this in <a href="https://learngitbranching.js.org/?locale=en_US">Learn Git Branching</a>: initialize a repo and make your first commit.</p>
  
  <!-- Progress Checklist -->
  <h3>Checklist:</h3>
  <ul>
    <li><input type="checkbox"> Initialized a Git repo</li>
    <li><input type="checkbox"> Made first commit</li>
    <li><input type="checkbox"> Understand staging and `git status`</li>
  </ul>

  <!-- More sections follow... -->

  <script>
    // (Possible scripts for toggling answers, interactive UI)
    // Clipboard copying is handled inline via navigator.clipboard
  </script>
</body>
</html>
```

# Suggested Visuals  
- **Roadmap Timeline:** A mermaid Gantt chart showing the 6-hour plan and checkpoints (e.g. `gitgraph` or Mermaid timeline).  
- **Git Workflow Flowchart:** A flowchart (Mermaid or diagram) contrasting GitFlow vs trunk-based.  
- **Example:** Using Mermaid, a commit graph could be drawn, or a quick D3-based chart of commits. For instance:  
  ```mermaid
  gitGraph
     commit id: "Init"
     branch feature
     commit id: "Feature1"
     checkout main
     commit id: "Main2"
     merge feature tag:"Merged"
  ```  
  This shows branching and merging visually. Or use SVG/JS to plot a branching timeline.

# References  
This plan draws on authoritative sources: official Git docs and Pro Git book for correctness【12†L207-L216】【17†L231-L239】, Atlassian’s advanced Git articles for best practices【18†L1137-L1145】, and peer-reviewed tutorials (e.g. an advanced Git tutorial【7†L13-L21】). Interactive learning platforms are cited by their descriptions【1†L11-L14】 to ensure alignment with learning goals. All resources are English and open-access.