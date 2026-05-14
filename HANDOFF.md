# Handoff: tweet automation pipeline

**Goal**: Automate fetching, tagging, and saving tweets into `_data/inspo/tweets.json` via Python scripts.

**Done**: `tweet.py` (fetch from Twitter API + write JSON), `tagger.py` (auto-tag by keyword), tweets.json reformatted with `id` field and no manual tags

**Next**: Commit untracked files (`tagger.py`, `tweet.py`, `_data/MD-tweets.json`) and wire up a cron/automation to run `tweet.py` on schedule

**Watch out**: `tweet.py` hardcodes a Bearer token — rotate or move to env var before committing publicly
