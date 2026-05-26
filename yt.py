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
        "desc": ""
    }

    if last_featured_at:
        result["last_featured_at"] = last_featured_at

    return result

# ---------- dynamic music feed generator ----------

def calculate_start_date(youtube_count, music_count, today):
    """Calculate start date to spread items at ≤1 per day.

    Spreads youtube_count + music_count items across equal number of days,
    ensuring balanced distribution over time.

    Args:
        youtube_count: Number of unseen youtube videos
        music_count: Number of unseen music videos
        today: date object for current day

    Returns:
        ISO format date string for start_date
    """
    total_items = youtube_count + music_count
    if total_items == 0:
        return today.isoformat()

    start_date = today - timedelta(days=total_items)
    return start_date.isoformat()



def generate_feeds(
    music_output,
    youtube_output,
    start_date_str
):
    """Generate both music and youtube feeds with mixed distributions."""
    source = load_json("_data/all-yt.json")
    music_existing = load_json(music_output)
    youtube_existing = load_json(youtube_output)

    today = date_cls.today()
    today_str = today.isoformat()

    start_date = date_cls.fromisoformat(start_date_str)
    historical_limit = today - timedelta(days=1)

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
    yesterday_str = (
        today - timedelta(days=1)
    ).isoformat()

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

    # pick distribution: 1M0V or 0M1V to enforce ≤1 item per day
    distributions = [(1, 0), (0, 1)]
    music_count, video_count = random.choice(distributions)

    # cap by pool size
    music_count = min(music_count, len(music_eligible))
    video_count = min(video_count, len(youtube_eligible))

    # sample
    featured_music = random.sample(music_eligible, music_count) if music_count > 0 else []
    featured_youtube = random.sample(youtube_eligible, video_count) if video_count > 0 else []

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

    # reshuffle historical: unified shuffle across both feeds to enforce ≤1 item per day
    def shuffle_historical_unified(music_feed, youtube_feed):
        total_days = (historical_limit - start_date).days
        if total_days > 0:
            # collect all historical items from both feeds
            music_historical = [
                item for item in music_feed
                if item.get("date")
                and date_cls.fromisoformat(item["date"][:10]) < today
            ]
            youtube_historical = [
                item for item in youtube_feed
                if item.get("date")
                and date_cls.fromisoformat(item["date"][:10]) < today
            ]

            # combine and shuffle
            all_historical = music_historical + youtube_historical
            random.shuffle(all_historical)

            # assign dates: each item gets a unique date slot
            n = len(all_historical)
            for i, item in enumerate(all_historical):
                days_offset = int(i * total_days / n) if n > 1 else 0
                item["date"] = (start_date + timedelta(days=days_offset)).isoformat()

    shuffle_historical_unified(music_final, youtube_final)

    # sort newest first
    music_final.sort(key=lambda x: x.get("date", ""), reverse=True)
    youtube_final.sort(key=lambda x: x.get("date", ""), reverse=True)

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

    # Calculate dynamic start date based on unseen items
    today = date_cls.today()
    youtube_unseen_count = sum(
        1 for v in final
        if "yt" in v.get("source_playlists", []) and not v.get("yt_seen", False)
    )
    music_unseen_count = sum(
        1 for v in final
        if "mu" in v.get("source_playlists", []) and not v.get("music_seen", False)
    )
    start_date_str = calculate_start_date(
        youtube_unseen_count,
        music_unseen_count,
        today
    )

    print(
        f"Feed generation: {youtube_unseen_count} unseen youtube, "
        f"{music_unseen_count} unseen music → start_date={start_date_str}"
    )

    generate_feeds(
        "_data/inspo/music.json",
        "_data/inspo/youtube.json",
        start_date_str
    )

if __name__ == "__main__":
    main()