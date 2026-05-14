import re
import yaml

STOPWORDS = {
    "a","an","the","in","of","to","for","how","why","what","my","i","is",
    "are","was","and","or","but","it","this","that","on","at","by","with",
    "from","about","into","when","then","than","been","have","has","had",
    "will","can","do","did","not","so","if","its","your","his","her","we",
    "you","they","them","their","our","more","some","one","two","new","old",
}


def load_tags(yaml_path="_data/tags.yml"):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tags = set()

    for item in data:
        tags.add(item["name"].lower())
        for child in item.get("children", []):
            tags.add(child.lower())

    return list(tags)


def auto_tag(text, all_tags):
    text = text.lower()
    matched = []

    for tag in all_tags:
        pattern = r"\b" + re.escape(tag) + r"\b"
        if re.search(pattern, text):
            matched.append(tag)

    return list(set(matched))


def fallback_from_text(text, stopwords=STOPWORDS):
    words = re.split(r"[\s\-:,|]+", text.lower())
    return [w for w in words if len(w) >= 4 and w not in stopwords][:5]


def assign_category(tags, category_map):
    for cat, tag_list in category_map.items():
        if any(t in tags for t in tag_list):
            return cat
    return "uncategorized"
