import json
import os
import subprocess
from datetime import datetime, UTC
import yaml
import re

OUTPUT_FILE = "_data/all-yt.json"


PLAYLISTS = [
    {
        "name": "yt",
        "url": "https://youtube.com/playlist?list=PLPAwgJxRv7VRQn4_bhuhyFC6f-e2MEltT"
    },
    {
        "name": "mu",
        "url": "https://youtube.com/playlist?list=PLPAwgJxRv7VTXSUvZspuHt7GF3NaqV0oI"
    }
]


# ---------- load tags from YAML ----------

def load_tags_from_yaml():
    with open("_data/tags.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tags = set()

    for item in data:
        tags.add(item["name"].lower())
        for child in item.get("children", []):
            tags.add(child.lower())

    return list(tags)


ALL_TAGS = load_tags_from_yaml()


# ---------- category map (you control this) ----------

CATEGORY_MAP = {
    "music": ["indian"],
    "tools-for-thought": ["ai", "writing", "tools"],
    "biology": ["biology"],
    "mindset": ["mindset"],
    "startup": ["startup"],
    "tech": ["ai", "semiconductors", "hardware"],
}


# ---------- utils ----------

def now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        return {}
    return json.loads(result.stdout)




def load_json(path):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 👇 add this line HERE
    data = sorted(data, key=lambda x: x.get("added_at", ""), reverse=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write("[\n")

        for i, item in enumerate(data):
            line = json.dumps(item, ensure_ascii=False, separators=(",", ":"))

            if i < len(data) - 1:
                f.write(line + ",\n")
            else:
                f.write(line + "\n")

        f.write("]")



# ---------- tagging ----------

STOPWORDS = {
    "a","an","the","in","of","to","for","how","why","what","my","i","is",
    "are","was","and","or","but","it","this","that","on","at","by","with",
    "from","about","into","when","then","than","been","have","has","had",
    "will","can","do","did","not","so","if","its","your","his","her","we",
    "you","they","them","their","our","more","some","one","two","new","old",
}

def auto_tag(text):
    text = text.lower()
    matched = []

    for tag in ALL_TAGS:
        pattern = r"\b" + re.escape(tag) + r"\b"
        if re.search(pattern, text):
            matched.append(tag)

    return list(set(matched))


def fallback_from_yt_tags(tags_list):
    result = []
    for t in tags_list:
        t = t.lower().strip()
        if t and len(t) <= 25 and not any(c.isdigit() for c in t):
            result.append(t)
    return list(dict.fromkeys(result))[:6]


def fallback_from_title(title):
    words = re.split(r"[\s\-:,|]+", title.lower())
    return [w for w in words if len(w) >= 4 and w not in STOPWORDS][:5]


def assign_category(tags):
    for cat, tag_list in CATEGORY_MAP.items():
        if any(t in tags for t in tag_list):
            return cat
    return "uncategorized"


# -------------- music feed ------------------
def build_feed(playlist_name, output_file, transform_fn):
    source = load_json("_data/all-yt.json")
    existing = load_json(output_file)

    existing_urls = {e["url"] for e in existing}
    new_items = []

    for v in source:
        if playlist_name not in v.get("source_playlists", []):
            continue

        entry = transform_fn(v)
        if not entry:
            continue

        if entry["url"] in existing_urls:
            continue

        new_items.append(entry)

    final = new_items + existing  # prepend

    save_json(output_file, final)

    print(f"{output_file}: +{len(new_items)} new, total {len(final)}")

def transform_music(v):
    return {
        "url": f"https://youtu.be/{v['id']}",
        "date": v.get("added_at", "")[:10]
    }

def transform_youtube(v):
    return {
        "date": v.get("added_at", "")[:10],  # 👈 first now
        "tags": v.get("auto_tags", []),
        "title": v.get("title", ""),
        "url": f"https://youtu.be/{v['id']}",
        "desc": ""
    }


# ---------- main ----------
def main():
    existing = load_json(OUTPUT_FILE)
    existing_map = {v["id"]: v for v in existing}

    live_ids = {pl["name"]: set() for pl in PLAYLISTS}

    for playlist in PLAYLISTS:
        name = playlist["name"]
        url = playlist["url"]

        print(f"\nProcessing → {name}")

        flat = run([
            "yt-dlp",
            "--extractor-args", "youtube:player_client=android",
            "--flat-playlist",
            "-J",
            url
        ])
        entries = flat.get("entries", []) if isinstance(flat, dict) else flat

        position_map = {}

        for i, v in enumerate(entries):
            vid = v.get("id")
            if vid:
                position_map[vid] = i
        
        for v in entries:
            vid = v.get("id")
            if not vid:
                continue

            live_ids[name].add(vid)

            if vid not in existing_map:

                title = v.get("title", "")
                text = title

                auto_tags_list = auto_tag(text)
                if not auto_tags_list:
                    auto_tags_list = fallback_from_title(title)

                norm = {
                    "id": vid,
                    "title": title,
                    "description": "",
                    "tags": "",
                    "tags_list": [],
                    "auto_tags": auto_tags_list,
                    "category": assign_category(auto_tags_list),
                    "added_at": now(),
                    "updated_at": now(),
                    "first_seen_position": position_map.get(vid),
                    "source_playlists": [name],
                }

                existing_map[vid] = norm

            else:
                v_existing = existing_map[vid]

                if name not in v_existing.get("source_playlists", []):
                    v_existing.setdefault("source_playlists", []).append(name)

                v_existing["updated_at"] = now()

    
    # remove videos no longer in any of their source playlists
    removed_count = 0
    for vid_id, entry in list(existing_map.items()):
        still_in = [pl for pl in entry.get("source_playlists", []) if vid_id in live_ids.get(pl, set())]
        if not still_in:
            del existing_map[vid_id]
            removed_count += 1
        elif still_in != entry.get("source_playlists", []):
            entry["source_playlists"] = still_in
            entry["updated_at"] = now()
    if removed_count:
        print(f"Removed {removed_count} video(s) no longer in any playlist.")

    # re-tag existing videos that have empty auto_tags
    retagged = 0
    for v in existing_map.values():
        if not v.get("auto_tags"):
            tl = v.get("tags_list") or []
            t = f"{v.get('title', '')} {v.get('description', '')}"
            tags = auto_tag(t)
            if not tags:
                tags = fallback_from_yt_tags(tl)
            if not tags:
                tags = fallback_from_title(v.get("title", ""))
            v["auto_tags"] = tags
            v["category"] = assign_category(tags)
            retagged += 1

    if retagged:
        print(f"Re-tagged {retagged} existing videos")

    final = list(existing_map.values())
    save_json(OUTPUT_FILE, final)

    print(f"\nDone. Total unique videos: {len(final)}")

    # 👇 ADD THIS
    build_feed("mu", "_data/inspo/music.json", transform_music)
    build_feed("yt", "_data/inspo/youtube.json", transform_youtube)

if __name__ == "__main__":
    main()