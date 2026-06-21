---
title: How to Get Disgustingly Good at Git
tags:
  - git
  - engineering
  - mental-models
  - longform
dateCreated: 2026-05-15
layout: note-layout
is_note: true
date: 2026-05-14
---

There are two kinds of developers.

The ones who fear rebase. And the ones who use it before breakfast.

The difference isn't experience. It's one mental model. Commit fear isn't a skill gap. It's an abstraction gap. Once you see Git as a predictable graph, both evaporate.

---

## Part 1 — The Day Git Stopped Being Scary

The first time I ran `git reset --hard`, my chest tightened. Twenty minutes later I was convinced I had destroyed weeks of work.

That's commit fear: the feeling that Git is one wrong command from catastrophe. It keeps most developers trapped at five safe commands for their entire careers.

Here's the exercise that kills it. Break a test repo intentionally:

```bash
git init test-fear && cd test-fear
echo "hello" > file.txt && git add . && git commit -m "first"
echo "more" >> file.txt && git commit -am "second"
git reset --hard HEAD~2
```

Commits appear gone. Now:

```bash
git reflog
```

```
abc1234 HEAD@{0}: reset: moving to HEAD~2
def5678 HEAD@{1}: commit: second
9ab0123 HEAD@{2}: commit: first
```

The commits aren't deleted; they're unreachable from the current HEAD. Reflog is Git's complete activity log stored in `.git/logs/`. It is the foundation of recovery mechanics: systematic knowledge of every undo path in Git.

Restore everything: `git reset --hard def5678`.

Git almost never permanently deletes anything. Objects stay in the repository until garbage collection, typically 30+ days after becoming unreachable. Once you know recovery mechanics exist, the threat model changes. "Destructive" commands are navigation tools. They move HEAD. They don't erase history.

Detached HEAD follows the same logic. `git checkout abc1234` puts HEAD on a commit instead of a branch: navigation, not damage. Recovery: `git switch -c rescue-branch`.

---

## Part 2 — The Mental Model That Explains All of Git

Commands are the interface. The model underneath is what you need.

Git is a directed acyclic graph of commit objects. Every commit points to its parent. Branches are movable pointers to commits. HEAD marks your current location in the graph.

| Git Object | Mental Model |
|---|---|
| commit | immutable snapshot of the full repository state |
| branch | a movable pointer, a named label on one commit |
| HEAD | your current location in the graph |
| merge | join two graph lines into one commit with two parents |
| rebase | replay commits from one branch onto another |
| reset | relocate HEAD (and optionally the index and working tree) |
| cherry-pick | transplant a single commit to a new graph position |

This table builds graph intuition faster than any tutorial. Seven vague concepts become seven precise mechanical descriptions. Test any row against a real operation; the prediction holds.

| Graph Thinker | Command Memorizer |
|---|---|
| Knows what rebase does before running | Avoids rebase, unsure what it will do |
| Reads `git log --graph` to verify state | Types `git status` five times hoping the answer changes |
| Uses `git reset` as deliberate navigation | Treats `git reset` as a dangerous unknown |
| Recovers detached HEAD in ten seconds | Opens Stack Overflow for twenty minutes |
| Has pointer literacy, follows HEAD and refs | Thinks in filenames, not graph positions |

Pointer literacy is the specific skill that separates these groups: look at `git log --oneline --graph` and immediately see where HEAD is, where each branch points, what the graph shape reveals about merge history.

```bash
git log --oneline --graph --decorate --all
```

Run this after every significant operation until it's automatic. The picture it builds is what graph intuition feels like once it's internalized.

---

## Part 3 — The Four Git States

Commands move content between four areas; they don't "save files."

| Command | State Affected |
|---|---|
| `git add` | Working Directory → Staging Area |
| `git commit` | Staging Area → Local Repository |
| `git push` | Local Repository → Remote |
| `git restore` | Reverts Working Directory only |
| `git restore --staged` | Reverts Staging Area to last commit |
| `git reset --soft HEAD~1` | Moves commit pointer; keeps changes staged |
| `git reset --mixed HEAD~1` | Moves commit pointer; unstages changes |
| `git reset --hard HEAD~1` | Moves commit pointer; discards all changes |

Most developers think in two states: local and remote. Commit fear lives in this gap. When the three reset modes seem arbitrarily different, you're missing the state layer. Graph intuition without state awareness is half the model.

---

## Part 4 — Branching Without Confusion

A branch is a sticky note on a commit.

Move the sticky note, the commits don't move. main and feature-x share history at commit A. One commit on feature-x moves its pointer to B. main stays on A. The graph has diverged.

Integration decision: merge or rebase?

**Merge** creates a new commit with two parents: fork-and-join graph shape, explicit history. **Rebase** replays commits onto main's tip; B becomes B', linear history, original stays in reflog.

Commit fear drives most developers to merge-always because rebase feels unpredictable. Once you can predict the graph change before running the command, the choice becomes deliberate. Predict the shape, run, compare. That loop builds pointer literacy. Before any PR, history surgery on the branch turns the messy work log into something a reviewer can follow.

---

## Part 5 — History Surgery

Most developers treat commit history as fixed once it's written. It isn't.

History surgery (intentional reshaping of commits before anyone else sees them) is one of the most underrated skills in professional engineering. Almost no tutorial teaches it explicitly.

The simplest form: `git commit --amend`. Wrong message, forgot a file. Amend replaces the last commit. Old commit stays in reflog.

More powerful: interactive rebase.

```bash
git rebase -i HEAD~5
```

An editable list of the last five commits. `pick` keeps, `reword` changes the message, `squash`/`fixup` merge into the previous commit, `drop` deletes, `edit` stops for amending during replay.

"fix", "fix 2", "PLEASE WORK" become one coherent commit. The reviewer sees a clean story, not a transaction log. This is history surgery as professional courtesy.

The mental model: rebase creates new commit objects replaying the same changes. Originals persist in reflog. History surgery is safe because recovery mechanics are always underneath it.

Cherry-pick transplants a specific commit: `git cherry-pick abc1234`. A hotfix on a feature branch can reach main without merging the whole branch; pointer literacy tells you which SHA from `git log --graph`.

Rebase goes wrong mid-operation: `git rebase --abort`. Resets cleanly to before it started. History surgery is reversible. Do it aggressively.

---

## Part 6 — Conflict Mastery

Conflicts aren't Git failures. They're competing graph states.

Two developers changed the same lines on diverged branches. Git can't decide which wins. So it stops and presents both. Correct behavior.

Resolution: `git status` to find conflicted files, locate `<<<<<<<` markers, pick or combine, `git add <resolved-file>`, then `git commit` or `git rebase --continue`. With rebase: multiple rounds, one per replayed commit, same mechanics each round.

`git merge --abort` or `git rebase --abort` resets cleanly to before the operation. Recovery mechanics apply; no work lost.

---

## Part 7 — Real World Git

Command knowledge gets you to competent. Operational habits get you to reliable.

**Commit discipline**: every commit is one complete, coherent unit of work. One logical change, completed correctly, with a message explaining why. This is what makes `git bisect` work: binary search through commit history locates the exact commit that introduced a bug in O(log n) checks. Non-atomic commits make bisect useless.

**Branch hygiene**: short-lived, focused, deleted after merge. Long-lived branches accumulate divergence silently.

**Git smells**:

| Smell | Signal |
|---|---|
| Giant commits | Weak commit discipline, changes aren't atomic |
| Long-lived branches | Integration risk, divergence accumulates |
| "WIP" commits in shared history | No history surgery before PR |
| Merge commit spam | Rebase before merge would keep history linear |
| Force-pushing shared branches | Breaks collaborators' local graphs |

**Force push etiquette**: force-push personal feature branches freely; it's the history surgery mechanism for clean history. Use `--force-with-lease` not `--force`: it refuses if someone else pushed since your last fetch. Never force-push shared branches.

Pointer literacy makes all of this navigation, not anxiety. Commit fear developers avoid these patterns and produce harder-to-review, harder-to-debug codebases as a direct result.

---

## Part 8 — Recovery and Debugging Mastery

Elite Git users are fearless because they know every recovery path before they need it.

Reflog holds every HEAD position for 90 days:

```bash
git reflog show --all
```

`git bisect` runs binary search through commit history:

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out a middle commit, test it, then:
git bisect good   # or: git bisect bad
git bisect reset
```

For any bug that "wasn't happening before," bisect beats manual code inspection every time.

**Recovery mechanics reference**:

| Disaster | Recovery |
|---|---|
| Detached HEAD with commits made | `git branch rescue HEAD` then `git switch rescue` |
| Deleted commit | `git reflog`, find SHA, then `git cherry-pick <sha>` |
| Broken rebase in progress | `git rebase --abort` |
| Force-pushed over your work | `git reset --hard ORIG_HEAD` |
| Deleted branch | `git reflog`, find last SHA, then `git branch recovered <sha>` |
| Lost stash | `git fsck --lost-found` |

The pattern: orientation before action. Where is HEAD? What does reflog show? Recovery mechanics is systematic forensics. The data is almost always there.

---

## Part 9 — Git Speed Workflows

Senior Git users inspect before they act.

```bash
git status
git log --oneline --graph --decorate --all
git diff --staged
```

Running these before committing, before rebasing, before merging builds graph intuition through repetition. See before. Act. See after. The model sharpens with every cycle.

**Aliases**:

```bash
git config --global alias.glog "log --oneline --graph --decorate --all"
git config --global alias.ap "add -p"
```

`git add -p` stages hunk-by-hunk, forcing review of exactly what enters the commit. Atomic commits come from `git add -p`.

**Fixup workflow, history surgery on autopilot**:

```bash
git commit --fixup abc1234
git rebase -i --autosquash HEAD~5
```

Work, create fixup commits, autosquash before PR. Clean history without manual rebase editing.

```bash
git switch -   # back to previous branch instantly
```

Every speed habit encodes graph intuition and pointer literacy into muscle memory. Fast developers always know where they are. That's the whole difference.

---

## What the Graph Thinker Looks Like

"Git feels dangerous" to "I think in commit graphs now."

The distance between those states is smaller than it looks. It's one mental model: commits as immutable snapshots, branches as movable pointers, history as a manipulable graph with recovery mechanics underneath every operation.

Once you have graph intuition, commit fear stops making sense. Detached HEAD is a navigation position, not a catastrophe. Rebase is commit replay. History surgery is how senior engineers write reviewable code. Almost nothing is truly lost; reflog holds everything for 90 days.

The developers who are disgustingly good at Git aren't the ones who never make mistakes. They're the ones who know exactly what to do when they do.

What's the last Git disaster you recovered from, and how long did it take to find the path back?
