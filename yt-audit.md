# Feed Generation Audit Report

## Intended Feed Model

The intended design is a pair of independent feeds:

* YouTube feed
* Music feed

Each feed maintains its own historical timeline.

The current day contains newly featured content.

Historical content starts from yesterday and moves backward.

Example (today = 2026-05-31):

```text
2026-05-31 → Today's featured items

2026-05-30 → Historical slot #1
2026-05-29 → Historical slot #2
2026-05-28 → Historical slot #3
...
```

The assignment of items to historical dates is randomized whenever the feed is regenerated.

Dates act as display positions rather than publication timestamps.

---

## Expected Historical Distribution

For each feed independently:

```text
Yesterday      → Item 1
Yesterday - 1  → Item 2
Yesterday - 2  → Item 3
...
```

Continue assigning one item per day until that feed runs out of items.

No gaps should exist while items remain available.

### Example

Inventory:

```text
34 YouTube items
12 Music items
```

Expected result:

```text
2026-05-30 → YT + MU
2026-05-29 → YT + MU
2026-05-28 → YT + MU
...
2026-05-19 → YT + MU
```

After Music inventory is exhausted:

```text
2026-05-18 → YT only
2026-05-17 → YT only
...
2026-04-27 → YT only
```

This is acceptable and expected.

The feeds are not required to have equal historical depth.

---

## What The Current Code Actually Does

### Only One New Item Is Featured

Current logic:

```python
distributions = [(1,0),(0,1)]
music_count, video_count = random.choice(distributions)
```

Result:

```text
Either:
  1 Music item

Or:
  1 YouTube item
```

Never:

```text
1 Music + 1 YouTube
```

Therefore the system surfaces only one new item per run.

---

### Historical Items Are Merged Together

Current logic:

```python
all_historical = music_historical + youtube_historical
random.shuffle(all_historical)
```

The two feeds are combined into one pool.

Dates are then assigned to the combined list.

Result:

```text
2025-11-01 → YouTube
2025-10-31 → YouTube
2025-10-30 → Music
2025-10-29 → Music
```

The system behaves as a single mixed timeline.

This conflicts with the intended design of two independent timelines.

---

### Dates Are Spread Across A Calculated Range

Current logic:

```python
days_offset = int(i * total_days / n)
```

Items are distributed proportionally across a date window.

Result:

```text
2025-01-01
2025-01-07
2025-01-14
2025-01-21
```

rather than:

```text
2026-05-30
2026-05-29
2026-05-28
2026-05-27
```

The intended model requires consecutive backward-filling days.

---

### Start Date Logic Is Based On Total Inventory

Current logic:

```python
start_date = today - timedelta(
    youtube_count + music_count
)
```

This assumes a single combined timeline.

The intended design does not require a calculated start date.

Instead:

```text
Yesterday
Yesterday - 1
Yesterday - 2
...
```

should be assigned directly until inventory is exhausted.

---

## Root Cause

The implementation currently optimizes for:

```text
One combined historical timeline
Maximum one item per day
```

The intended design is:

```text
Two independent timelines

Music:
  Yesterday → item
  Yesterday-1 → item
  Yesterday-2 → item

YouTube:
  Yesterday → item
  Yesterday-1 → item
  Yesterday-2 → item
```

Each feed should randomize item-to-date assignment independently.

---

## Recommended Feed Algorithm

### Step 1

Feature:

```text
1 Music item today
1 YouTube item today
```

---

### Step 2

Remove today's items from historical pools.

---

### Step 3

Randomize remaining Music items.

---

### Step 4

Randomize remaining YouTube items.

---

### Step 5

Assign dates independently.

Music:

```text
Yesterday      → item 1
Yesterday - 1  → item 2
Yesterday - 2  → item 3
...
```

YouTube:

```text
Yesterday      → item 1
Yesterday - 1  → item 2
Yesterday - 2  → item 3
...
```

---

## Desired End State

If a visitor opens:

```text
2026-05-30
```

they should ideally see:

```text
Music item
YouTube item
```

When both inventories still have content.

As one feed becomes shorter, older dates naturally become:

```text
YouTube only
```

or

```text
Music only
```

without introducing gaps or requiring artificial balancing.

This behavior matches the original feed concept.
