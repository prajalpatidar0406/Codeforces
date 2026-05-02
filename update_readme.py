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

MARKING A PROBLEM AS UNSOLVED
-----------------------------
Add these comment lines right after the problem link:

   # https://codeforces.com/problemset/problem/4/A
   #unsolved
   #reason: "due to memory limit"

The script will:
- Fetch problem name, rating, and tags from the Codeforces API.
- Auto-rename your file to {contestId}{index}_{Problem_Title}.py
- Update README.md with clickable links to each solution file.
- Show unsolved problems in a separate section with the reason.
"""

import os
import re
import json
import subprocess
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
    """Read the first few lines of a .py file and extract:
    - Codeforces problem link (line 1)
    - unsolved flag (line 2, optional): #unsolved
    - reason (line 3, optional): #reason: "due to memory limit"

    Returns (link, contest_id, index, unsolved, reason).
    """
    with open(filepath, "r") as f:
        lines = [f.readline().strip() for _ in range(5)]

    # Line 1: problem link
    match = re.match(r"^#\s*(https?://codeforces\.com/\S+)", lines[0])
    if not match:
        return None, None, None, False, None

    link = match.group(1)

    # Extract contestId and problem index from URL
    # Formats:
    #   /problemset/problem/4/A
    #   /contest/4/problem/A
    #   /gym/123/problem/A
    m = re.search(r"/(?:problemset/problem|contest|gym)/(\d+)/(?:problem/)?([A-Za-z]\d?)", link)
    if not m:
        return link, None, None, False, None

    contest_id = m.group(1)
    index = m.group(2).upper()

    # Scan remaining lines for #unsolved and #reason tags
    unsolved = False
    reason = None
    for line in lines[1:]:
        if re.match(r"^#\s*unsolved\s*$", line, re.IGNORECASE):
            unsolved = True
        reason_match = re.match(r'^#\s*reason:\s*["\'](.+?)["\']\s*$', line, re.IGNORECASE)
        if reason_match:
            reason = reason_match.group(1)

    return link, contest_id, index, unsolved, reason


def get_file_date(filepath):
    """Get the file's last modified date as YYYY-MM-DD."""
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def make_filename(contest_id, index, problem_name):
    """Build a consistent filename: {contestId}{index}_{Problem_Title}.py

    Rules:
    - Replace spaces and hyphens with underscores
    - Remove any characters that aren't alphanumeric or underscores
    - Collapse multiple underscores into one
    - Strip leading/trailing underscores from the title part
    """
    title = problem_name.replace(" ", "_").replace("-", "_")
    title = re.sub(r"[^A-Za-z0-9_]", "", title)
    title = re.sub(r"_+", "_", title).strip("_")
    return f"{contest_id}{index}_{title}.py"


def rename_solution_file(old_path, new_name):
    """Rename a solution file and its .cph companion, then git-add both."""
    old_dir = os.path.dirname(old_path)
    old_name = os.path.basename(old_path)
    new_path = os.path.join(old_dir, new_name)

    if old_path == new_path:
        return new_path  # already correct

    os.rename(old_path, new_path)
    print(f"   📝 Renamed: {old_name} → {new_name}")

    # Rename matching .cph file (format: .{filename}_{hash}.prob)
    cph_dir = os.path.join(old_dir, ".cph")
    if os.path.isdir(cph_dir):
        old_prefix = f".{old_name}_"
        new_prefix = f".{new_name}_"
        for cph_file in os.listdir(cph_dir):
            if cph_file.startswith(old_prefix):
                old_cph = os.path.join(cph_dir, cph_file)
                new_cph = os.path.join(cph_dir, cph_file.replace(old_prefix, new_prefix, 1))
                os.rename(old_cph, new_cph)
                print(f"   📝 Renamed .cph: {cph_file} → {os.path.basename(new_cph)}")

    # Stage the rename in git
    try:
        subprocess.run(
            ["git", "add", "-A", old_dir],
            cwd=REPO_ROOT, capture_output=True, check=True,
        )
    except Exception:
        pass  # non-fatal

    return new_path


def scan_solutions(problems_db):
    """Scan all .py files in problems/ folder, extract link, look up metadata.

    Also renames files to the canonical {contestId}{index}_{Title}.py format.
    """
    solutions = []

    if not os.path.isdir(PROBLEMS_DIR):
        return solutions

    for fname in sorted(os.listdir(PROBLEMS_DIR)):
        if not fname.endswith(".py"):
            continue

        filepath = os.path.join(PROBLEMS_DIR, fname)
        link, contest_id, index, unsolved, reason = parse_link_from_file(filepath)

        if not link:
            continue

        # Look up in API data
        info = {}
        if contest_id and index:
            key = f"{contest_id}_{index}"
            info = problems_db.get(key, {})

        problem_name = info.get("name", "")

        # ── Auto-rename file to canonical format ──
        if problem_name and contest_id and index:
            canonical = make_filename(contest_id, index, problem_name)
            if fname != canonical:
                filepath = rename_solution_file(filepath, canonical)
                fname = canonical

        solutions.append({
            "filename": fname,
            "filepath": f"problems/{fname}",
            "link": link,
            "name": info.get("name", fname.replace(".py", "").replace("_", " ")),
            "rating": info.get("rating", "-"),
            "tags": info.get("tags", []),
            "contest_id": contest_id or "-",
            "index": index or "-",
            "date": get_file_date(filepath),
            "unsolved": unsolved,
            "reason": reason,
        })

    return solutions


def build_readme(solutions):
    """Rebuild README.md."""

    # ── Split solved / unsolved ──
    solved = [s for s in solutions if not s["unsolved"]]
    unsolved = [s for s in solutions if s["unsolved"]]

    # ── Collect stats (from solved only) ──
    topic_counts = defaultdict(int)
    rating_groups = defaultdict(list)

    for s in solved:
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
    total_solved = len(solved)
    total_unsolved = len(unsolved)
    total_all = len(solutions)
    unique_tags = len(topic_counts)
    easiest = min((int(s["rating"]) for s in solved if str(s["rating"]).isdigit()), default="-")
    hardest = max((int(s["rating"]) for s in solved if str(s["rating"]).isdigit()), default="-")

    # ── Build difficulty distribution bar ──
    dist_lines = []
    if sorted_buckets and total_solved > 0:
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
        if b == 0:
            rank = "Unrated"
            color = "555555"
            badge_label = "Unrated"
            section = f'### <img src="https://img.shields.io/badge/Unrated-{color}?style=flat-square"/> &nbsp; Unrated — {len(group)} solved\n\n'
        else:
            rank = RANK_LABELS.get(b, "Unknown")
            color = RANK_COLORS.get(rank, "555555")
            section = f'### <img src="https://img.shields.io/badge/{b}-{rank}-{color}?style=flat-square"/> &nbsp; Rating {b} — {len(group)} solved\n\n'
        section += "| # | Problem | CF | Tags | Date |\n"
        section += "|---|---------|:--:|------|------|\n"

        for s in group:
            global_idx += 1
            prob_id = f'{s["contest_id"]}{s["index"]}'
            display = f"{prob_id} - {s['name']}"
            cf_link = f'[🔗]({s["link"]})'
            tags_str = ", ".join(f"`{t}`" for t in s["tags"]) if s["tags"] else "-"
            section += f"| {global_idx} | [{display}]({s['filepath']}) | {cf_link} | {tags_str} | {s['date']} |\n"

        rating_sections.append(section)

    if not rating_sections:
        rating_sections.append("*No solutions yet — start solving!*\n")

    # ── Build unsolved section ──
    unsolved_section = ""
    if unsolved:
        unsolved.sort(key=lambda s: s["date"], reverse=True)
        unsolved_section = "## ❌ Unsolved Problems\n\n"
        unsolved_section += "| # | Problem | CF | Reason | Tags | Date |\n"
        unsolved_section += "|---|---------|:--:|--------|------|------|\n"
        for idx, s in enumerate(unsolved, 1):
            prob_id = f'{s["contest_id"]}{s["index"]}'
            display = f"{prob_id} - {s['name']}"
            cf_link = f'[🔗]({s["link"]})'
            reason_str = s["reason"] if s["reason"] else "-"
            tags_str = ", ".join(f"`{t}`" for t in s["tags"]) if s["tags"] else "-"
            unsolved_section += f"| {idx} | [{display}]({s['filepath']}) | {cf_link} | {reason_str} | {tags_str} | {s['date']} |\n"
        unsolved_section += "\n"

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
[![CF Rating](https://cp-logo.vercel.app/codeforces/prajal_patidar)](https://codeforces.com/profile/prajal_patidar)
&nbsp;&nbsp;
![Total](https://img.shields.io/badge/Solved-{total_solved}-success?style=for-the-badge)
&nbsp;&nbsp;
![Unsolved](https://img.shields.io/badge/Unsolved-{total_unsolved}-red?style=for-the-badge)
&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

<p align="center">
  <i>A collection of my <a href="https://codeforces.com">Codeforces</a> solutions with automated tracking, problem metadata, and a self-updating README.</i>
</p>

---

## ✨ Features

- 🔄 **Auto-updating README** — a pre-commit hook regenerates this file on every `git commit`
- 📛 **Auto file naming** — solution files are renamed to `{{contestId}}{{index}}_{{Title}}.py` automatically
- 📊 **Problem metadata** — rating, tags, and difficulty fetched live from the Codeforces API
- 🔗 **Clickable links** — click any problem name to view the solution; click 🔗 to open it on Codeforces
- ❌ **Unsolved tracking** — mark problems as `#unsolved` with a `#reason` to track what needs revisiting
- 📈 **[Interactive Stats Dashboard](stats.html)** — visual graphs: daily/weekly/monthly progress, rating distribution, topic radar, and activity heatmap

---

## 📈 Stats

| Metric | Value |
|--------|-------|
| ✅ Total Solved | **{total_solved}** |
| ❌ Unsolved | **{total_unsolved}** |
| 🏷️ Unique Topics | **{unique_tags}** |
| 🟢 Easiest Rating | **{easiest}** |
| 🔴 Hardest Rating | **{hardest}** |

**Difficulty Distribution:**

```
{chr(10).join(dist_lines) if dist_lines else "  No solutions yet."}
```

---

## 🏷️ Topics Covered

{topic_badges_str}

---

## 📊 Solutions

> Click on any **Problem** name to view the solution code. Click **🔗** to open the problem on Codeforces.

{chr(10).join(rating_sections)}
{unsolved_section}
---

## 🚀 How to Use This Repository

<details>
<summary><b>📥 Adding a New Solution</b></summary>

1. Create any `.py` file inside `problems/`
2. Paste the Codeforces problem link as the **first line** with a `#` prefix
3. Write your solution below
4. Commit — the README updates automatically!

```python
# https://codeforces.com/problemset/problem/4/A

def solve():
    n = int(input())
    print("YES" if n > 2 and n % 2 == 0 else "NO")

solve()
```

> **Note:** The file will be auto-renamed to `4A_Watermelon.py` on commit.

</details>

<details>
<summary><b>❌ Marking a Problem as Unsolved</b></summary>

Add `#unsolved` and optionally `#reason` after the problem link:

```python
# https://codeforces.com/problemset/problem/1873/E
#unsolved
#reason: "due to memory limit"

# your attempt below...
```

Unsolved problems appear in a separate section with the reason displayed.

</details>

<details>
<summary><b>📁 Repository Structure</b></summary>

```
Codeforces/
├── problems/              ← all solution files (auto-renamed)
│   ├── 4A_Watermelon.py
│   ├── 69A_Young_Physicist.py
│   └── ...
├── template.py            ← starter template for new problems
├── update_readme.py       ← README generator script
├── .gitignore
└── README.md              ← this file (auto-generated)
```

</details>

<details>
<summary><b>🔧 Manual README Update</b></summary>

```bash
python3 update_readme.py
```

Problem name, rating, and tags are fetched from the [Codeforces API](https://codeforces.com/apiHelp) and cached for 24 hours.

</details>

---

<div align="center">
  <sub>Built with ❤️ and automated with Python · Solutions in Python 3</sub>
</div>
"""

    with open(os.path.join(REPO_ROOT, "README.md"), "w") as f:
        f.write(readme)


def build_stats_page(solutions):
    """Generate stats.html from template with embedded solution data for interactive charts."""
    template_path = os.path.join(REPO_ROOT, "stats_template.html")
    output_path = os.path.join(REPO_ROOT, "stats.html")
    if not os.path.exists(template_path):
        print("   ⚠️  stats_template.html not found, skipping stats page.")
        return

    solved = [s for s in solutions if not s["unsolved"]]
    unsolved = [s for s in solutions if s["unsolved"]]

    stats_data = {
        "solved": [
            {
                "name": s["name"],
                "rating": s["rating"],
                "tags": s["tags"],
                "date": s["date"],
                "contest_id": s["contest_id"],
                "index": s["index"],
            }
            for s in solved
        ],
        "unsolved": [
            {
                "name": s["name"],
                "rating": s["rating"],
                "tags": s["tags"],
                "date": s["date"],
                "reason": s["reason"],
            }
            for s in unsolved
        ],
    }

    data_script = (
        "<script>window.STATS_DATA = "
        + json.dumps(stats_data, separators=(",", ":"))
        + ";</script>"
    )

    with open(template_path, "r") as f:
        html = f.read()

    html = html.replace("<!--STATS_DATA_PLACEHOLDER-->", data_script)

    with open(output_path, "w") as f:
        f.write(html)

    print(f"   ✅ stats.html updated with {len(solved)} solved, {len(unsolved)} unsolved.")


def main():
    print("🔍 Fetching Codeforces problem data...")
    problems_db = fetch_all_problems()
    print(f"   Loaded {len(problems_db)} problems from Codeforces.\n")

    print("📂 Scanning solution files...")
    solutions = scan_solutions(problems_db)
    solved = [s for s in solutions if not s["unsolved"]]
    unsolved = [s for s in solutions if s["unsolved"]]
    print(f"   Found {len(solved)} solved, {len(unsolved)} unsolved.\n")

    print("📝 Updating README.md...")
    build_readme(solutions)

    print("📊 Generating stats dashboard...")
    build_stats_page(solutions)

    print(f"\n✅ Done! README.md + stats.html updated with {len(solved)} solved, {len(unsolved)} unsolved.")

    if solutions:
        print(f"\n📊 Summary:")
        tags = defaultdict(int)
        for s in solved:
            for t in s["tags"]:
                tags[t] += 1
        top = sorted(tags.items(), key=lambda x: -x[1])[:5]
        if top:
            print(f"   Top tags: {', '.join(f'{t}({c})' for t,c in top)}")


if __name__ == "__main__":
    main()
