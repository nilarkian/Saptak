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


# ---------- date scheduling ----------

# def get_occupied_dates():
#     yt = load_json("_data/inspo/youtube.json")
#     mu = load_json("_data/inspo/music.json")
#     return {e["date"][:10] for e in yt + mu if e.get("date")}


# def next_free_dates(n, occupied):
#     if not n:
#         return []
#     if occupied:
#         parsed = [date_cls.fromisoformat(d) for d in occupied]
#         cursor = max(parsed) + timedelta(days=1)
#     else:
#         cursor = date_cls.today()
#     used = set(occupied)
#     result = []
#     while len(result) < n:
#         ds = cursor.isoformat()
#         if ds not in used:
#             result.append(ds)
#             used.add(ds)
#         cursor += timedelta(days=1)
#     return result


# ---------- music date randomizer ----------




# -------------- music feed ------------------


def transform_music(v, date_value, last_featured_at=None):
    result = {
        "url": f"https://youtu.be/{v['id']}",
        "date": date_value
    }

    if last_featured_at:
        result["last_featured_at"] = last_featured_at

    return result

def transform_youtube(v):
    return {
        "date": v.get("added_at", "")[:10],  # 👈 first now
        "tags": v.get("auto_tags", []),
        "title": v.get("title", ""),
        "url": f"https://youtu.be/{v['id']}",
        "desc": ""
    }

# ---------- dynamic music feed generator ----------



def generate_music_feed(output_file, start_date_str):
    source = load_json("_data/all-yt.json")
    existing_feed = load_json(output_file)

    today = date_cls.today()
    today_str = today.isoformat()

    start_date = date_cls.fromisoformat(start_date_str)
    historical_limit = today - timedelta(days=1)

    # canonical music universe
    music_pool = [
        v for v in source
        if "mu" in v.get("source_playlists", [])
    ]

    if not music_pool:
        print("No music items found.")
        return

    # unseen songs only
    unseen_pool = [
        v for v in music_pool
        if not v.get("music_seen", False)
    ]

    # avoid immediate repeats from yesterday
    yesterday_str = (
        today - timedelta(days=1)
    ).isoformat()

    recently_featured_urls = {
        item["url"]
        for item in existing_feed
        if item.get("last_featured_at") == yesterday_str
    }

    eligible_pool = [
        v for v in unseen_pool
        if f"https://youtu.be/{v['id']}"
        not in recently_featured_urls
    ]

    if not eligible_pool:
        eligible_pool = unseen_pool

    # how many new songs today
    featured_count = min(
        random.randint(0, 2),
        len(eligible_pool)
    )

    featured = random.sample(
        eligible_pool,
        featured_count
    ) if featured_count > 0 else []

    # persist canonical seen-state
    for v in featured:
        v["music_seen"] = True

    # start from existing archive
    final = existing_feed.copy()

    # append only new surfaced songs
    for v in featured:
        final.append(
            transform_music(
                v,
                today_str,
                last_featured_at=today_str
            )
        )

    # reshuffle historical archive only
    total_days = (
        historical_limit - start_date
    ).days

    if total_days > 0:
        
        sorted_items = sorted(
            final,
            key=lambda _: random.random() ** 1.8
        )

        for item in sorted_items:

            ds = item.get("date")

            if not ds:
                continue

            try:
                item_date = date_cls.fromisoformat(
                    ds[:10]
                )
            except ValueError:
                continue

            # never move today's surfaced songs
            if item_date >= today:
                continue

            # recent bias
            bias = 1 - (
                random.random() ** 0.8
            )

            random_days = int(
                total_days * bias
            )

            random_date = (
                start_date +
                timedelta(days=random_days)
            ).isoformat()

            item["date"] = random_date

    # newest first
    final.sort(
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    atomic_save_json(output_file, final)

    # persist canonical DB updates
    save_json(OUTPUT_FILE, source)

    print(
        f"{output_file}: "
        f"+{len(featured)} appended, "
        f"{len(final)} total archive items"
    )















# -------------- generic feed builder ------------------

def build_feed(
    playlist_name,
    output_file,
    transform_fn
):
    source = load_json("_data/all-yt.json")
    existing_feed = load_json(output_file)

    existing_urls = {
        item["url"]
        for item in existing_feed
    }

    final = existing_feed.copy()

    appended = 0

    for v in source:

        if playlist_name not in v.get(
            "source_playlists",
            []
        ):
            continue

        entry = transform_fn(v)

        if not entry:
            continue

        if entry["url"] in existing_urls:
            continue

        final.append(entry)
        existing_urls.add(entry["url"])
        appended += 1

    final.sort(
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    atomic_save_json(
        output_file,
        final
    )

    print(
        f"{output_file}: "
        f"+{appended} appended, "
        f"{len(final)} total items"
    )


def get_existing_feed_urls():
    urls = set()

    for path in [
        "_data/inspo/music.json",
        "_data/inspo/youtube.json"
    ]:
        items = load_json(path)

        for item in items:
            url = item.get("url")

            if url:
                urls.add(url)

    return urls










# ---------- main ----------
def main():
    existing = load_json(OUTPUT_FILE)
    existing_map = {v["id"]: v for v in existing}

    existing_feed_urls = get_existing_feed_urls()

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

            
            video_url = f"https://youtu.be/{vid}"

            # skip creating duplicate canonical items
            if (
                vid not in existing_map
                and video_url in existing_feed_urls
            ):
                continue

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

    # 👇 ADD THIS
    generate_music_feed(
    "_data/inspo/music.json",
    "2025-01-01"
    )

    build_feed("yt", "_data/inspo/youtube.json", transform_youtube)

if __name__ == "__main__":
    main()