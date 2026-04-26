# 🏆 Codeforces Solutions

<div align="center">

[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/prajal_patidar)
&nbsp;&nbsp;
[![CF Rating](https://cp-logo.vercel.app/codeforces/prajal_patidar)](https://codeforces.com/profile/prajal_patidar)
&nbsp;&nbsp;
![Total](https://img.shields.io/badge/Solved-6-success?style=for-the-badge)
&nbsp;&nbsp;
![Unsolved](https://img.shields.io/badge/Unsolved-1-red?style=for-the-badge)
&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

<p align="center">
  <i>A collection of my <a href="https://codeforces.com">Codeforces</a> solutions with automated tracking, problem metadata, and a self-updating README.</i>
</p>

---

## ✨ Features

- 🔄 **Auto-updating README** — a pre-commit hook regenerates this file on every `git commit`
- 📛 **Auto file naming** — solution files are renamed to `{contestId}{index}_{Title}.py` automatically
- 📊 **Problem metadata** — rating, tags, and difficulty fetched live from the Codeforces API
- 🔗 **Clickable links** — click any problem name to view the solution; click 🔗 to open it on Codeforces
- ❌ **Unsolved tracking** — mark problems as `#unsolved` with a `#reason` to track what needs revisiting

---

## 📈 Stats

| Metric | Value |
|--------|-------|
| ✅ Total Solved | **6** |
| ❌ Unsolved | **1** |
| 🏷️ Unique Topics | **7** |
| 🟢 Easiest Rating | **1000** |
| 🔴 Hardest Rating | **1100** |

**Difficulty Distribution:**

```
     0  ██████░░░░░░░░░░░░░░    1  (?)
  1000  ████████████████████    3  (Pupil)
  1100  █████████████░░░░░░░    2  (Pupil)
```

---

## 🏷️ Topics Covered

![implementation](https://img.shields.io/badge/implementation-4-informational?style=flat-square) ![greedy](https://img.shields.io/badge/greedy-3-informational?style=flat-square) ![strings](https://img.shields.io/badge/strings-2-informational?style=flat-square) ![math](https://img.shields.io/badge/math-2-informational?style=flat-square) ![*special](https://img.shields.io/badge/*special-1-informational?style=flat-square) ![binary search](https://img.shields.io/badge/binary%20search-1-informational?style=flat-square) ![dp](https://img.shields.io/badge/dp-1-informational?style=flat-square)

---

## 📊 Solutions

> Click on any **Problem** name to view the solution code. Click **🔗** to open the problem on Codeforces.

### <img src="https://img.shields.io/badge/Unrated-555555?style=flat-square"/> &nbsp; Unrated — 1 solved

| # | Problem | CF | Tags | Date |
|---|---------|:--:|------|------|
| 1 | [2225A - A Number Between Two Others](problems/2225A_A_Number_Between_Two_Others.py) | [🔗](https://codeforces.com/problemset/problem/2225/A) | `greedy`, `math` | 2026-04-23 |

### <img src="https://img.shields.io/badge/1000-Pupil-008000?style=flat-square"/> &nbsp; Rating 1000 — 3 solved

| # | Problem | CF | Tags | Date |
|---|---------|:--:|------|------|
| 2 | [58A - Chat room](problems/58A_Chat_room.py) | [🔗](https://codeforces.com/problemset/problem/58/A) | `greedy`, `strings` | 2026-04-24 |
| 3 | [69A - Young Physicist](problems/69A_Young_Physicist.py) | [🔗](https://codeforces.com/problemset/problem/69/A) | `implementation`, `math` | 2026-04-24 |
| 4 | [118A - String Task](problems/118A_String_Task.py) | [🔗](https://codeforces.com/problemset/problem/118/A) | `implementation`, `strings` | 2026-04-23 |

### <img src="https://img.shields.io/badge/1100-Pupil-008000?style=flat-square"/> &nbsp; Rating 1100 — 2 solved

| # | Problem | CF | Tags | Date |
|---|---------|:--:|------|------|
| 5 | [706B - Interesting drink](problems/706B_Interesting_drink.py) | [🔗](https://codeforces.com/problemset/problem/706/B) | `binary search`, `dp`, `implementation` | 2026-04-27 |
| 6 | [158B - Taxi](problems/158B_Taxi.py) | [🔗](https://codeforces.com/problemset/problem/158/B) | `*special`, `greedy`, `implementation` | 2026-04-26 |

## ❌ Unsolved Problems

| # | Problem | CF | Reason | Tags | Date |
|---|---------|:--:|--------|------|------|
| 1 | [1873E - Building an Aquarium](problems/1873E_Building_an_Aquarium.py) | [🔗](https://codeforces.com/problemset/problem/1873/E) | due to memory limit | `binary search`, `sortings` | 2026-04-25 |


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
