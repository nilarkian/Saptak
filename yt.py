import json
import os
import subprocess
from datetime import datetime, UTC, date as date_cls, timedelta
import yaml
import re
import random

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
    data = sorted(
        data,
        key=lambda x: x.get("added_at", ""),
        reverse=True
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write("[\n")

        for i, item in enumerate(data):
            line = json.dumps(item, ensure_ascii=False, separators=(",", ":"))

            if i < len(data) - 1:
                f.write(line + ",\n")
            else:
                f.write(line + "\n")

        f.write("]")

def atomic_save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    temp_path = path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write("[\n")

        for i, item in enumerate(data):
            line = json.dumps(
                item,
                ensure_ascii=False,
                separators=(",", ":")
            )

            if i < len(data) - 1:
                f.write(line + ",\n")
            else:
                f.write(line + "\n")

        f.write("]")

    os.replace(temp_path, path)



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


def transform_video(v, date_value, last_featured_at=None):
    result = {
        "date": date_value,
        "url": f"https://youtu.be/{v['id']}",
        "title": v.get("title", ""),
        "tags": v.get("auto_tags", []),
        "desc": "",
    }

    if last_featured_at:
        result["last_featured_at"] = last_featured_at

    return result

# ---------- dynamic feed generator ----------

def generate_feeds(music_output, youtube_output):
    """Generate music and youtube feeds as two independent backward-filled timelines."""
    source = load_json("_data/all-yt.json")
    music_existing = load_json(music_output)
    youtube_existing = load_json(youtube_output)

    today = date_cls.today()
    today_str = today.isoformat()
    rng = random.Random(today_str)

    # canonical pools
    music_pool = [
        v for v in source
        if "mu" in v.get("source_playlists", [])
    ]
    youtube_pool = [
        v for v in source
        if "yt" in v.get("source_playlists", [])
    ]

    # unseen items only
    music_unseen = [
        v for v in music_pool
        if not v.get("music_seen", False)
    ]
    youtube_unseen = [
        v for v in youtube_pool
        if not v.get("yt_seen", False)
    ]

    # avoid yesterday's repeats
    yesterday_str = (today - timedelta(days=1)).isoformat()

    music_yesterday = {
        item["url"]
        for item in music_existing
        if item.get("last_featured_at") == yesterday_str
    }
    youtube_yesterday = {
        item["url"]
        for item in youtube_existing
        if item.get("last_featured_at") == yesterday_str
    }

    music_eligible = [
        v for v in music_unseen
        if f"https://youtu.be/{v['id']}" not in music_yesterday
    ] or music_unseen
    youtube_eligible = [
        v for v in youtube_unseen
        if f"https://youtu.be/{v['id']}" not in youtube_yesterday
    ] or youtube_unseen

    # feature 1 of each independently
    featured_music = rng.sample(music_eligible, 1) if music_eligible else []
    featured_youtube = rng.sample(youtube_eligible, 1) if youtube_eligible else []

    # persist seen-state
    for v in featured_music:
        v["music_seen"] = True
    for v in featured_youtube:
        v["yt_seen"] = True

    # build feeds: remove today's items from existing (they'll be readded fresh)
    music_final = [
        item for item in music_existing
        if item.get("date") != today_str
    ]
    youtube_final = [
        item for item in youtube_existing
        if item.get("date") != today_str
    ]

    for v in featured_music:
        music_final.append(
            transform_video(v, today_str, last_featured_at=today_str)
        )

    for v in featured_youtube:
        youtube_final.append(
            transform_video(v, today_str, last_featured_at=today_str)
        )

    # build one historical timeline containing both feeds

    music_historical = [
        it for it in music_final
        if it.get("date") != today_str
    ]

    youtube_historical = [
        it for it in youtube_final
        if it.get("date") != today_str
    ]

    rng.shuffle(music_historical)
    rng.shuffle(youtube_historical)


    def build_historical_timeline(
        music_items,
        youtube_items
    ):
        timeline = []

        music_items = music_items[:]
        youtube_items = youtube_items[:]

        music_remaining = len(music_items)
        youtube_remaining = len(youtube_items)

        while music_items or youtube_items:

            if not music_items:
                timeline.append(
                    ("yt", youtube_items.pop())
                )
                youtube_remaining -= 1
                continue

            if not youtube_items:
                timeline.append(
                    ("mu", music_items.pop())
                )
                music_remaining -= 1
                continue

            total = (
                music_remaining +
                youtube_remaining
            )

            choose_music = (
                rng.random()
                < (music_remaining / total)
            )

            if choose_music:
                timeline.append(
                    ("mu", music_items.pop())
                )
                music_remaining -= 1
            else:
                timeline.append(
                    ("yt", youtube_items.pop())
                )
                youtube_remaining -= 1

        return timeline


    historical = build_historical_timeline(
        music_historical,
        youtube_historical
    )

    music_final = [
    item for item in music_final
    if item.get("date") == today_str
    ]

    youtube_final = [
        item for item in youtube_final
        if item.get("date") == today_str
    ]

    for i, (feed_type, item) in enumerate(historical):

        item["date"] = (
            today - timedelta(days=i + 1)
        ).isoformat()

        if feed_type == "mu":
            music_final.append(item)
        else:
            youtube_final.append(item)

    # sort newest first
    music_final.sort(
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    youtube_final.sort(
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    # save
    atomic_save_json(music_output, music_final)
    atomic_save_json(youtube_output, youtube_final)
    save_json("_data/all-yt.json", source)

    print(
        f"Feeds updated: "
        f"+{len(featured_music)}M (+{len(featured_youtube)}V) | "
        f"{len(music_final)} music total, {len(youtube_final)} youtube total"
    )





















# ---------- main ----------
def main():
    existing = load_json(OUTPUT_FILE)
    existing_map = {v["id"]: v for v in existing}

    live_ids = {pl["name"]: set() for pl in PLAYLISTS}
    new_video_ids = []

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

            # new canonical item
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
                    "music_seen": name != "mu",
                    "yt_seen": name != "yt",
                }

                existing_map[vid] = norm
                new_video_ids.append(vid)

            # existing canonical item
            else:

                v_existing = existing_map[vid]

                if name not in v_existing.get("source_playlists", []):
                    v_existing.setdefault(
                        "source_playlists",
                        []
                    ).append(name)

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

    if new_video_ids:
         print(f"Added {len(new_video_ids)} new video(s)")
    final = list(existing_map.values())
    save_json(OUTPUT_FILE, final)

    print(f"\nDone. Total unique videos: {len(final)}")

    generate_feeds(
        "_data/inspo/music.json",
        "_data/inspo/youtube.json",
    )

if __name__ == "__main__":
    main()