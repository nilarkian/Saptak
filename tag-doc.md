# Tagging System Documentation

## Overview

The Saptak portfolio uses a three-layer tagging architecture:

1. **Schema** (`_data/tags.yml`) — hierarchical tag vocabulary with parents and children
2. **Python Pipeline** (`yt.py`) — auto-tags video content using regex matching and fallback chains, stores normalized tags
3. **Jekyll Sidebar** (`_includes/tags.html`) — dynamically builds filterable tag sidebar on any page, reads tags from `data-tags` attributes

The system is **content-agnostic**: any page can display tags by emitting `data-tags` attributes, and the sidebar will auto-discover and filter them.

---

## Layer 1: Tag Schema (`_data/tags.yml`)

### Structure

Tags are stored in a flat YAML list. Each entry is a parent object with an optional `children` array:

```yaml
- name: energy
  children: [nuclear, fusion, battery]

- name: cure-boredom

- name: tech
  children: [ai, ar, gene editing, semiconductors, ...more...]
```

### Rules

- **Parent names** are single words, lowercase, hyphen-separated (e.g., `interests`, `tech`, `cure-boredom`).
- **Children** are strings, not objects. They have no additional metadata.
- A parent with no `children` key is a **standalone tag** — appears as a single pill in the sidebar, not a collapsible group.
- All tags are case-insensitive by convention; the YAML stores lowercase.
- A child tag can appear under only one parent (the system does not deduplicate).

### Adding New Tags

- **New standalone tag**: add `- name: your-tag` to the file.
- **New child of existing parent**: append to the parent's `children` array.
- **New parent with children**: add a full parent entry.

---

## Layer 2: Python Pipeline (`yt.py`)

### Tag Loading

**`load_tags_from_yaml()` (lines 25–39)**

Reads the YAML file and flattens the hierarchy into a single set of tag strings:

```python
def load_tags_from_yaml():
    with open("_data/tags.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tags = set()
    for item in data:
        tags.add(item["name"].lower())
        for child in item.get("children", []):
            tags.add(child.lower())

    return list(tags)

ALL_TAGS = load_tags_from_yaml()  # module-level constant
```

**`ALL_TAGS`** is a flat list — the hierarchy is discarded and used only during Jekyll rendering (Layer 3).

### Auto-Tagging

**`auto_tag(text)` (lines 112–121)**

Matches text against `ALL_TAGS` using whole-word regex:

```python
def auto_tag(text):
    text = text.lower()
    matched = []

    for tag in ALL_TAGS:
        pattern = r"\b" + re.escape(tag) + r"\b"
        if re.search(pattern, text):
            matched.append(tag)

    return list(set(matched))
```

- Multi-word tags like `"gene editing"` work because `\b` anchors apply to the outer word boundaries and `re.escape` preserves internal spaces.
- Whole-word anchors prevent matching "ai" in "train".
- Result is deduplicated and returned as a list.

### Fallback Tagging Chains

If auto-tagging yields no results, two fallbacks are tried:

**`fallback_from_yt_tags(tags_list)` (lines 124–128)**

- Takes raw YouTube tag strings, lowercases and strips them.
- Filters: rejects tags > 25 chars, tags containing digits, empty strings.
- Deduplicates and caps at 6 tags.

**`fallback_from_title(title)` (lines 130–132)**

- Splits title on `[\s\-:,|]+` and extracts words ≥ 4 chars.
- Filters stopwords.
- Caps at 5 tags.

### Category Assignment

**`CATEGORY_MAP` (lines 44–51) and `assign_category(tags)` (lines 138–142)**

Maps tag subsets to broad categories:

```python
CATEGORY_MAP = {
    "music": ["indian"],
    "tools-for-thought": ["ai", "writing", "tools"],
    "biology": ["biology"],
    "mindset": ["mindset"],
    "startup": ["startup"],
    "tech": ["ai", "semiconductors", "hardware"],
}

def assign_category(tags):
    for cat, tag_list in CATEGORY_MAP.items():
        if any(t in tags for t in tag_list):
            return cat
    return "uncategorized"
```

A video is assigned to the first matching category. This is a **separate layer** from the YAML hierarchy.

### Record Structure

**Lines 233–245:**

```python
norm = {
    "id": vid,
    "title": title,
    "description": "",
    "tags": "",                          # raw YouTube tags (unused)
    "tags_list": [],                    # raw tags list (fallback source)
    "auto_tags": auto_tags_list,        # ← LIVE TAGS (list of strings)
    "category": assign_category(auto_tags_list),
    "added_at": now(),
    "updated_at": now(),
    "first_seen_position": position_map.get(vid),
    "source_playlists": [name],
}
```

The `auto_tags` field is the normalized tag list. This is what gets exported to the JSON and rendered in HTML.

### Output Transform

**`transform_youtube(v)` (lines 178–185)**

Maps the raw video record to the final JSON shape:

```python
def transform_youtube(v):
    return {
        "date": v.get("added_at", "")[:10],
        "tags": v.get("auto_tags", []),       # ← list of tag strings
        "title": v.get("title", ""),
        "url": f"https://youtu.be/{v['id']}",
        "desc": ""
    }
```

Output is written to `_data/inspo/youtube.json` via `build_feed()`.

---

## Layer 3: Jekyll/JS Sidebar (`_includes/tags.html`)

### TAG_TREE Injection

**Line 289:**

```javascript
const TAG_TREE = {{ site.data.tags | jsonify }};
```

At Jekyll build time, the full YAML structure (with parents and children hierarchy) is serialized into JavaScript. This is the **single source of truth** for sidebar structure.

### Context Detection

The include is included on multiple pages with different tag sources. It detects the page context by looking for a specific container element ID:

| Context | Container ID | Tag Source | Read From |
|---------|--------------|-----------|-----------|
| Watchlist/Timeline | `#timeline-body` | Parsed from Markdown `tags: [a, b]` syntax | Text nodes |
| Notes index | `#note-list` | From `.note-row` elements | `data-tags` attribute |
| Inspo cards | `#inspo-body` | From `.inspo-card` elements | `data-tags` attribute |
| Scripts catalogue | `#catalogue` | From `.script-card` elements | `data-tags` attribute |

**Example (notes, lines 454–468):**

```javascript
const rows = document.querySelectorAll('.note-row');
rows.forEach(row => {
  const tags = row.dataset.tags ? row.dataset.tags.split(',').filter(Boolean) : [];
  tags.forEach(t => usedTags.add(t.trim().toLowerCase()));
});
```

**Example (inspo cards, lines 470–556):**

```javascript
const cards = document.querySelectorAll('.inspo-card');
cards.forEach(card => {
  const tags = card.dataset.tags ? card.dataset.tags.split(',').filter(Boolean) : [];
  tags.forEach(t => usedTags.add(t.trim().toLowerCase()));
  // ... category handling ...
});

filterFn = (activeTag, activeIsParent, parentToChildren) => {
  cards.forEach(card => {
    let show = !activeTag; // show all if no filter
    if (activeTag) {
      const cardTags = card.dataset.tags ? card.dataset.tags.split(',').map(t => t.trim().toLowerCase()) : [];
      if (activeIsParent) {
        const kids = parentToChildren[activeTag] || [];
        show = cardTags.includes(activeTag) || kids.some(c => cardTags.includes(c));
      } else {
        show = cardTags.includes(activeTag);
      }
    }
    card.hidden = !show;
  });
};
```

### Sidebar Pruning

**Lines 576–597:**

The sidebar only shows tags that **actually appear in the page data**. Parents are included if they or any of their children are used:

```javascript
const visibleParents  = new Set();
const visibleChildren = {};

TAG_TREE.forEach(p => {
  const usedKids = (p.children || []).filter(c => usedTags.has(c));
  if (usedTags.has(p.name) || usedKids.length > 0) {
    visibleParents.add(p.name);
    visibleChildren[p.name] = usedKids;
  }
});

const orphanTags = [...usedTags].filter(t => !allKnownTags.has(t)).sort();
```

**Orphan tags** — tags in the data but not in `tags.yml` — are collected separately and rendered under an "Other" section.

### Filter State Machine

**`setActive(tag, isParent, parentRow)` (lines 608–619)**

Manages which tag is currently active:

```javascript
function setActive(tag, isParent, parentRow) {
  activeTag = tag; activeIsParent = isParent;
  clearActive();
  if (!tag) {
    allBtn.classList.add('active');
  } else if (isParent && parentRow) {
    parentRow.classList.add('active');
  } else {
    const btn = tagList.querySelector(`.child-tag-btn[data-tag="${tag}"], .standalone-tag-btn[data-tag="${tag}"]`);
    if (btn) btn.classList.add('active');
  }
  filterFn(activeTag, activeIsParent, parentToChildren);
}
```

Calls `filterFn` to show/hide items based on the new active tag.

### Filter Logic (Parent vs. Child)

When a **parent tag** is clicked, show all items tagged with that parent **OR any of its children**:

```javascript
show = cardTags.includes(activeTag) || kids.some(c => cardTags.includes(c));
```

When a **child or standalone tag** is clicked, show only exact matches:

```javascript
show = cardTags.includes(activeTag);
```

### Sidebar DOM Construction

**Lines 641–724:**

For each parent in `TAG_TREE`:

1. If parent is not in `visibleParents`, skip it.
2. Get the list of used children for this parent.
3. If children exist:
   - Create a `.parent-filter-btn` with a chevron that expands/collapses children.
   - Create a `.child-tag-btn` for each used child.
4. If no children:
   - Create a `.standalone-tag-btn` for the parent.
5. Add click handlers that call `setActive()`.

Orphan tags are rendered as standalone pills at the end.

### Delegation Pattern: `window.applyInspoFilter`

**Lines 481, 490:**

For complex filter logic, the sidebar calls a **hook function** on the page:

```javascript
filterFn = (activeTag, activeIsParent, parentToChildren) => {
  if (window.applyInspoFilter) {
    window.applyInspoFilter(activeTag, activeIsParent, parentToChildren);
  }
};
```

The page (e.g., `inspo.html`) defines `window.applyInspoFilter` to handle category-aware filtering. The sidebar is decoupled from content-specific logic.

---

## Replication Guide: Adding Tags to a New Content Type

To add auto-tagging and a filterable sidebar to a new content type (e.g., articles, books), follow these steps:

### 1. Add Tag Vocabulary (if needed)

Edit `_data/tags.yml`:

```yaml
- name: your-parent-name
  children: [tag1, tag2, tag3]
```

Reuse existing tags if they fit your content.

### 2. Python: Auto-Tag and Transform

In `yt.py` (or a similar pipeline script):

1. **Auto-tag** each item:
   ```python
   auto_tags = auto_tag(item["title"])  # or description, or body text
   ```

2. **Store** in the item record:
   ```python
   item["auto_tags"] = auto_tags
   ```

3. **Write a transform function**:
   ```python
   def transform_articles(a):
       return {
           "date": a.get("date", ""),
           "tags": a.get("auto_tags", []),       # ← required
           "title": a.get("title", ""),
           "url": a.get("url", ""),
           "desc": a.get("description", ""),
       }
   ```

4. **Export to JSON**:
   ```python
   build_feed("articles", "_data/inspo/articles.json", transform_articles)
   ```

### 3. HTML: Emit data-tags Attributes

In the template that renders each item (e.g., `inspo/articles.html`), emit `data-tags`:

```liquid
{% for article in site.data.inspo.articles %}
  <div class="article-card" data-tags="{{ article.tags | join: ',' }}">
    <h3>{{ article.title }}</h3>
    <p>{{ article.desc }}</p>
  </div>
{% endfor %}
```

Use a **consistent class name** for cards so the sidebar can locate them.

### 4. Page: Include the Sidebar + Add Context Detection

At the bottom of the page template, include the sidebar:

```liquid
{% include tags.html %}
```

Add a **unique container ID** around the card grid:

```liquid
<div id="articles-body">
  <div class="article-card" data-tags="...">...</div>
  <div class="article-card" data-tags="...">...</div>
</div>
```

### 5. Update tags.html: Add Context Branch

Edit `_includes/tags.html`. Add a new `else if` branch **after line 556** (after the inspo context) and **before line 573** (before the scripts context):

```javascript
// Articles context (new)
else if (document.getElementById('articles-body')) {
  const articlesBody = document.getElementById('articles-body');
  const cards = articlesBody.querySelectorAll('.article-card');

  cards.forEach(card => {
    const tags = card.dataset.tags ? card.dataset.tags.split(',').filter(Boolean) : [];
    tags.forEach(t => usedTags.add(t.trim().toLowerCase()));
  });

  filterFn = (activeTag, activeIsParent, parentToChildren) => {
    cards.forEach(card => {
      let show = !activeTag;
      if (activeTag) {
        const cardTags = card.dataset.tags ? card.dataset.tags.split(',').map(t => t.trim().toLowerCase()) : [];
        if (activeIsParent) {
          const kids = parentToChildren[activeTag] || [];
          show = cardTags.includes(activeTag) || kids.some(c => cardTags.includes(c));
        } else {
          show = cardTags.includes(activeTag);
        }
      }
      card.hidden = !show;
    });
  };
}
```

Alternatively, use the delegation pattern if filtering needs to be smarter (e.g., category-aware):

```javascript
else if (document.getElementById('articles-body')) {
  const articlesBody = document.getElementById('articles-body');
  const cards = articlesBody.querySelectorAll('.article-card');

  cards.forEach(card => {
    const tags = card.dataset.tags ? card.dataset.tags.split(',').filter(Boolean) : [];
    tags.forEach(t => usedTags.add(t.trim().toLowerCase()));
  });

  filterFn = (activeTag, activeIsParent, parentToChildren) => {
    if (window.applyArticlesFilter) {
      window.applyArticlesFilter(activeTag, activeIsParent, parentToChildren);
    }
  };
}
```

Then define `window.applyArticlesFilter` in the page template.

### 6. (Optional) Add Category Assignment

If your content needs broad categorization (like YouTube videos), extend `yt.py`:

```python
ARTICLE_CATEGORY_MAP = {
    "learning": ["research", "tutorial", "howto"],
    "inspiration": ["design", "writing", "art"],
}

def assign_article_category(tags):
    for cat, tag_list in ARTICLE_CATEGORY_MAP.items():
        if any(t in tags for t in tag_list):
            return cat
    return "uncategorized"
```

Store as `"category"` in the JSON and use in filtering if needed.

---

## Implementation Checklist

- [ ] Tags exist in `_data/tags.yml` or reuse existing ones
- [ ] Python script calls `auto_tag()`, stores in `auto_tags` field
- [ ] Transform function written; exports to `_data/inspo/X.json` with `"tags"` key
- [ ] HTML cards emit `data-tags="tag1,tag2"` and use a unique card class
- [ ] Page template has a unique container element ID (`id="X-body"`)
- [ ] tags.html updated with new context branch
- [ ] Page includes `{% include tags.html %}` at the bottom
- [ ] Sidebar detects and filters the new content correctly

---

## Files to Reference

- `_data/tags.yml` — tag hierarchy (source of truth for sidebar structure)
- `yt.py` — auto-tagger, record structure, transform functions
- `_includes/tags.html` — sidebar include, context detection, filter logic
- `inspo.html` — example of delegation pattern (`window.applyInspoFilter`)
- `_includes/inspo/youtube.html` — example of card template with `data-tags`
