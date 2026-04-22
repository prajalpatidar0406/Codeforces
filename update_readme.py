"""
README Auto-Updater for Codeforces Solutions
=============================================

Run:  python3 update_readme.py

HOW TO WRITE YOUR SOLUTION FILES
---------------------------------
1. Create a .py file with ANY name (e.g. watermelon.py, 4A.py, etc.)
2. Put the Codeforces problem link as the FIRST LINE with a # prefix:

   # https://codeforces.com/problemset/problem/4/A

   or

   # https://codeforces.com/contest/4/problem/A

3. Write your solution below it.
4. Run:  python3 update_readme.py

That's it. The script fetches problem name, rating, and tags
automatically from the Codeforces API.
"""

import os
import re
import json
import urllib.request
from collections import defaultdict
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(REPO_ROOT, "problems")

# Cache file so we don't hit the API every single run
CACHE_FILE = os.path.join(REPO_ROOT, ".cf_cache.json")
CACHE_MAX_AGE_HOURS = 24


def fetch_all_problems():
    """Fetch all problems from Codeforces API and return as dict keyed by (contestId, index)."""
    # Check cache first
    if os.path.exists(CACHE_FILE):
        mtime = os.path.getmtime(CACHE_FILE)
        age_hours = (datetime.now().timestamp() - mtime) / 3600
        if age_hours < CACHE_MAX_AGE_HOURS:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)

    print("   Fetching problems from Codeforces API (cached for 24h)...")
    url = "https://codeforces.com/api/problemset.problems"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CF-Readme-Updater"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"   ⚠️  API fetch failed: {e}")
        # Try loading stale cache
        if os.path.exists(CACHE_FILE):
            print("   Using stale cache instead.")
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    if data.get("status") != "OK":
        print("   ⚠️  API returned non-OK status.")
        return {}

    problems = {}
    for p in data["result"]["problems"]:
        key = f'{p["contestId"]}_{p["index"]}'
        problems[key] = {
            "name": p.get("name", "Unknown"),
            "rating": p.get("rating", "-"),
            "tags": p.get("tags", []),
            "contestId": p["contestId"],
            "index": p["index"],
        }

    # Save cache
    with open(CACHE_FILE, "w") as f:
        json.dump(problems, f)

    return problems


def parse_link_from_file(filepath):
    """Read the first line of a .py file and extract the Codeforces problem link."""
    with open(filepath, "r") as f:
        first_line = f.readline().strip()

    # Match:  # https://codeforces.com/...
    match = re.match(r"^#\s*(https?://codeforces\.com/\S+)", first_line)
    if not match:
        return None, None, None

    link = match.group(1)

    # Extract contestId and problem index from URL
    # Formats:
    #   /problemset/problem/4/A
    #   /contest/4/problem/A
    #   /gym/123/problem/A
    m = re.search(r"/(?:problemset/problem|contest|gym)/(\d+)/(?:problem/)?([A-Za-z]\d?)", link)
    if not m:
        return link, None, None

    contest_id = m.group(1)
    index = m.group(2).upper()
    return link, contest_id, index


def get_file_date(filepath):
    """Get the file's last modified date as YYYY-MM-DD."""
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def scan_solutions(problems_db):
    """Scan all .py files in problems/ folder, extract link, look up metadata."""
    solutions = []

    if not os.path.isdir(PROBLEMS_DIR):
        return solutions

    for fname in sorted(os.listdir(PROBLEMS_DIR)):
        if not fname.endswith(".py"):
            continue

        filepath = os.path.join(PROBLEMS_DIR, fname)
        link, contest_id, index = parse_link_from_file(filepath)

        if not link:
            continue

        # Look up in API data
        info = {}
        if contest_id and index:
            key = f"{contest_id}_{index}"
            info = problems_db.get(key, {})

        solutions.append({
            "filename": fname,
            "link": link,
            "name": info.get("name", fname.replace(".py", "").replace("_", " ")),
            "rating": info.get("rating", "-"),
            "tags": info.get("tags", []),
            "contest_id": contest_id or "-",
            "index": index or "-",
            "date": get_file_date(filepath),
        })

    return solutions


def build_readme(solutions):
    """Rebuild README.md."""

    # ── Collect stats ──
    topic_counts = defaultdict(int)
    rating_groups = defaultdict(list)

    for s in solutions:
        for tag in s["tags"]:
            topic_counts[tag] += 1
        # Group by rating bucket
        r = s["rating"]
        if isinstance(r, int) or (isinstance(r, str) and r.isdigit()):
            bucket = (int(r) // 100) * 100  # 800, 900, 1000, ...
            rating_groups[bucket].append(s)
        else:
            rating_groups[0].append(s)

    # Sort solutions within each bucket by date (newest first)
    for bucket in rating_groups:
        rating_groups[bucket].sort(key=lambda s: s["date"], reverse=True)

    sorted_buckets = sorted(rating_groups.keys())

    # ── Rating labels ──
    RANK_LABELS = {
        800: "Newbie", 900: "Newbie",
        1000: "Pupil", 1100: "Pupil",
        1200: "Specialist", 1300: "Specialist",
        1400: "Expert", 1500: "Expert",
        1600: "Candidate Master", 1700: "Candidate Master",
        1800: "Master", 1900: "Master",
        2000: "International Master", 2100: "International Master",
        2200: "Grandmaster", 2300: "Grandmaster",
        2400: "International Grandmaster",
        2500: "International Grandmaster",
        2600: "Legendary Grandmaster",
    }

    RANK_COLORS = {
        "Newbie": "808080",
        "Pupil": "008000",
        "Specialist": "03A89E",
        "Expert": "0000FF",
        "Candidate Master": "AA00AA",
        "Master": "FF8C00",
        "International Master": "FF8C00",
        "Grandmaster": "FF0000",
        "International Grandmaster": "FF0000",
        "Legendary Grandmaster": "FF0000",
    }

    # ── Stats overview ──
    total = len(solutions)
    unique_tags = len(topic_counts)
    easiest = min((int(s["rating"]) for s in solutions if str(s["rating"]).isdigit()), default="-")
    hardest = max((int(s["rating"]) for s in solutions if str(s["rating"]).isdigit()), default="-")

    # ── Build difficulty distribution bar ──
    dist_lines = []
    if sorted_buckets and total > 0:
        max_count = max(len(rating_groups[b]) for b in sorted_buckets)
        for b in sorted_buckets:
            count = len(rating_groups[b])
            bar_len = int((count / max_count) * 20) if max_count > 0 else 0
            bar = "█" * bar_len + "░" * (20 - bar_len)
            label = RANK_LABELS.get(b, "?")
            dist_lines.append(f"  {b:>4}  {bar}  {count:>3}  ({label})")

    # ── Build per-rating sections ──
    rating_sections = []
    global_idx = 0

    for b in sorted_buckets:
        group = rating_groups[b]
        rank = RANK_LABELS.get(b, "Unknown")
        color = RANK_COLORS.get(rank, "555555")

        section = f'### <img src="https://img.shields.io/badge/{b}-{rank}-{color}?style=flat-square"/> &nbsp; Rating {b} — {len(group)} solved\n\n'
        section += "| # | Problem | Tags | Date |\n"
        section += "|---|---------|------|------|\n"

        for s in group:
            global_idx += 1
            prob_id = f'{s["contest_id"]}{s["index"]}'
            display = f"{prob_id} - {s['name']}"
            tags_str = ", ".join(f"`{t}`" for t in s["tags"]) if s["tags"] else "-"
            section += f"| {global_idx} | [{display}]({s['link']}) | {tags_str} | {s['date']} |\n"

        rating_sections.append(section)

    if not rating_sections:
        rating_sections.append("*No solutions yet — start solving!*\n")

    # ── Topic badges ──
    topic_badges = []
    for tag, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
        tag_url = tag.replace(" ", "%20")
        topic_badges.append(f'![{tag}](https://img.shields.io/badge/{tag_url}-{count}-informational?style=flat-square)')

    topic_badges_str = " ".join(topic_badges) if topic_badges else "*No topics yet*"

    # ── Assemble README ──
    readme = f"""# 🏆 Codeforces Solutions

<div align="center">

[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/prajal_patidar)
&nbsp;&nbsp;
![Total](https://img.shields.io/badge/Solved-{total}-success?style=for-the-badge)
&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## 📈 Stats

| Metric | Value |
|--------|-------|
| ✅ Total Solved | **{total}** |
| 🏷️ Unique Topics | **{unique_tags}** |
| 🟢 Easiest Rating | **{easiest}** |
| 🔴 Hardest Rating | **{hardest}** |

**Difficulty Distribution:**

```
{chr(10).join(dist_lines) if dist_lines else "  No solutions yet."}
```

---

## 🏷️ Topics

{topic_badges_str}

---

## 📊 Solutions

{chr(10).join(rating_sections)}

---

## 🚀 Quick Start

**Add a solution** — create any `.py` file inside `problems/`, paste the problem link on line 1:

```
Codeforces/
├── problems/          ← put your solutions here
│   ├── 4A_Watermelon.py
│   └── 71A_Way_Too_Long_Words.py
├── template.py        ← starter template
├── update_readme.py   ← run this to update README
└── README.md          ← auto-generated
```

```python
# https://codeforces.com/problemset/problem/4/A

def solve():
    n = int(input())
    print("YES" if n > 2 and n % 2 == 0 else "NO")

solve()
```

**Update README** — just run:

```bash
python3 update_readme.py
```

Problem name, rating, and tags are fetched automatically from the Codeforces API. ✨
"""

    with open(os.path.join(REPO_ROOT, "README.md"), "w") as f:
        f.write(readme)


def main():
    print("🔍 Fetching Codeforces problem data...")
    problems_db = fetch_all_problems()
    print(f"   Loaded {len(problems_db)} problems from Codeforces.\n")

    print("📂 Scanning solution files...")
    solutions = scan_solutions(problems_db)
    print(f"   Found {len(solutions)} solution(s).\n")

    print("📝 Updating README.md...")
    build_readme(solutions)

    print(f"\n✅ Done! README.md updated with {len(solutions)} solution(s).")

    if solutions:
        print(f"\n📊 Summary:")
        tags = defaultdict(int)
        for s in solutions:
            for t in s["tags"]:
                tags[t] += 1
        top = sorted(tags.items(), key=lambda x: -x[1])[:5]
        if top:
            print(f"   Top tags: {', '.join(f'{t}({c})' for t,c in top)}")


if __name__ == "__main__":
    main()
