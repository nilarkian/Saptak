# extract_missing_tags.py
# Run from project root: python extract_missing_tags.py

import json
import yaml
from pathlib import Path

INSPO_DIR = Path("_data/inspo")
TAGS_FILE = Path("_data/tags.yml")
MISSING_FILE = Path("_data/missing-tags.yml")


def collect_tags_from_json():
    all_tags = set()

    for file in INSPO_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            items = data if isinstance(data, list) else [data]

            for item in items:
                tags = item.get("tags", [])

                if isinstance(tags, list):
                    all_tags.update(tags)

        except Exception as e:
            print(f"Error reading {file}: {e}")

    return all_tags


def collect_registered_tags():
    registered = set()

    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []

    for entry in data:
        name = entry.get("name")

        if name:
            registered.add(name)

        children = entry.get("children", [])

        if isinstance(children, list):
            registered.update(children)

    return registered


def load_existing_missing_tags():
    if not MISSING_FILE.exists():
        return set()

    try:
        with open(MISSING_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        tags = data.get("missing_tags", [])

        return set(tags)

    except Exception:
        return set()

def save_missing_tags(tags):
    tags = sorted(tags)
    count = len(tags)

    with open(MISSING_FILE, "w", encoding="utf-8") as f:
        f.write(f"# missing tag count: {count}\n")
        f.write(f"missing_tags: [{', '.join(tags)}]\n")

    print(f"Saved {count} missing tags")


def main():
    json_tags = collect_tags_from_json()
    registered_tags = collect_registered_tags()

    current_missing = json_tags - registered_tags

    existing_missing = load_existing_missing_tags()

    # merge + auto-clean
    final_missing = (existing_missing | current_missing) - registered_tags

    save_missing_tags(final_missing)


if __name__ == "__main__":
    main()