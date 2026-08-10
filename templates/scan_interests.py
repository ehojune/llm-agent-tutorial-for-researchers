#!/usr/bin/env python3
"""
scan_interests.py — Build a weighted research-interest profile from the llm-wiki.

Scans every wiki/**/*.md page's YAML frontmatter (tags, category,
source_collection, date/year) and aggregates tags into a ranked interest
profile. Active curiosity (chat questions) outweighs seminars, which outweigh
papers. Scores decay with age so recent interests dominate.

Outputs:
  - interests.json          (machine-readable ranked topics)
  - interests.md            (human-readable ranked list)
  - refreshes the AUTO block in briefing/interests.md (manual lines kept),
    which the daily paper briefing reads.

No third-party deps (no PyYAML required). Run:  python scan_interests.py
"""

import json
import re
from datetime import date, datetime
from pathlib import Path

# --- config ---------------------------------------------------------------
WIKI_ROOT = Path(__file__).resolve().parent
WIKI_DIR = WIKI_ROOT / "wiki"
BRIEFING_INTERESTS = WIKI_ROOT / "briefing" / "interests.md"

# Interest contribution per source type. Higher = stronger signal.
BASE_WEIGHT = {
    "chat": 2.0,             # curated chat question / insight (notes/)
    "external": 1.5,         # paper
    "seminar": 1.5,          # seminar / talk
    "project_meeting": 1.5,  # project meeting (active work)
    "textbook_study": 0.5,   # textbook chapter study + memo
    "news": 0.3,             # press coverage — a lead, not evidence
    "routine_meeting": 0.1,  # routine / recurring meeting (low signal)
    "conversation": 0.1,     # general conversation log (placeholder)
}
DEFAULT_WEIGHT = 1.5

# Readable label per source_collection for the per-topic source breakdown.
KIND_LABEL = {
    "external": "paper",
    "chat": "question",
    "seminar": "seminar",
    "project_meeting": "project_meeting",
    "routine_meeting": "routine_meeting",
    "textbook_study": "textbook_study",
    "conversation": "conversation",
    "news": "news",
}
HALFLIFE_YEARS = 3.0          # score halves every 3 years of age
TOP_QUERIES = 10              # how many topics to push into the briefing list

# Tags that mark the *kind* of entry or the wiki's own workflow, not a
# research topic. These never feed the interest profile / briefing queries.
STOP_TAGS = {
    "seminar", "question", "note",
    "project-meeting", "routine-meeting", "textbook-study", "conversation",
    "knowledge-management", "interests", "briefing", "workflow",
}

AUTO_START = "<!-- AUTO:wiki-interests START -->"
AUTO_END = "<!-- AUTO:wiki-interests END -->"


# --- frontmatter parsing --------------------------------------------------
def parse_frontmatter(text):
    """Minimal YAML frontmatter parser for the fields we need.

    Accepts both tag spellings, since either is valid YAML and agents write both:

        tags: [a, b]        # inline
        tags:               # block
          - a
          - b
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm = {}
    in_tag_block = False  # collecting "- item" lines under a bare "tags:"
    for line in block.splitlines():
        line = line.rstrip()
        if not line:
            continue
        stripped = line.lstrip()
        if in_tag_block and stripped.startswith("- "):
            item = stripped[2:].strip().strip("'\"")
            if item:
                fm["tags"].append(item)
            continue
        in_tag_block = False
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key == "tags":
            if val:
                # inline list form: [a, b, c]
                val = val.strip("[]")
                fm["tags"] = [t.strip().strip("'\"") for t in val.split(",") if t.strip()]
            else:
                # block list form: items follow on the next lines
                fm["tags"] = []
                in_tag_block = True
        else:
            fm[key] = val.strip("'\"")
    return fm


def entry_date(fm):
    """Best-effort date for recency weighting."""
    for key in ("date",):
        if fm.get(key):
            try:
                return datetime.strptime(fm[key][:10], "%Y-%m-%d").date()
            except ValueError:
                pass
    if fm.get("year"):
        m = re.search(r"\d{4}", str(fm["year"]))
        if m:
            return date(int(m.group()), 1, 1)
    return None


def recency_factor(d, today):
    if d is None:
        return 0.5  # unknown date: mild down-weight
    age_years = (today - d).days / 365.0
    if age_years < 0:
        age_years = 0.0
    return 0.5 ** (age_years / HALFLIFE_YEARS)


# --- aggregation ----------------------------------------------------------
def scan():
    today = date.today()
    topics = {}  # tag -> {score, counts: {kind: n}, last_seen}
    files = 0
    for path in WIKI_DIR.rglob("*.md"):
        # utf-8-sig, not utf-8: a leading BOM would otherwise defeat the
        # `startswith("---")` check in parse_frontmatter and drop the whole page
        # from the profile without a word. Windows produces BOMs by default —
        # Notepad, and PowerShell 5.1's Set-Content / Out-File.
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        fm = parse_frontmatter(text)
        tags = fm.get("tags") or []
        if not tags:
            continue
        files += 1
        sc = fm.get("source_collection", "external")
        base = BASE_WEIGHT.get(sc, DEFAULT_WEIGHT)
        d = entry_date(fm)
        weight = base * recency_factor(d, today)
        kind = KIND_LABEL.get(sc, sc)
        for tag in tags:
            t = tag.strip().lower()
            if not t or t in STOP_TAGS:
                continue
            rec = topics.setdefault(t, {"score": 0.0, "counts": {}, "last_seen": None})
            rec["score"] += weight
            rec["counts"][kind] = rec["counts"].get(kind, 0) + 1
            iso = d.isoformat() if d else None
            if iso and (rec["last_seen"] is None or iso > rec["last_seen"]):
                rec["last_seen"] = iso
    ranked = sorted(topics.items(), key=lambda kv: kv[1]["score"], reverse=True)
    return files, ranked


# --- outputs --------------------------------------------------------------
def write_json(ranked, files):
    out = {
        "generated": date.today().isoformat(),
        "source": "scan_interests.py",
        "files_scanned": files,
        "weights": {
            "question": BASE_WEIGHT["chat"],
            "paper": BASE_WEIGHT["external"],
            "seminar": BASE_WEIGHT["seminar"],
            "project_meeting": BASE_WEIGHT["project_meeting"],
            "textbook_study": BASE_WEIGHT["textbook_study"],
            "routine_meeting": BASE_WEIGHT["routine_meeting"],
            "conversation": BASE_WEIGHT["conversation"],
            "halflife_years": HALFLIFE_YEARS,
        },
        "topics": [
            {
                "tag": t,
                "score": round(r["score"], 3),
                "from": r["counts"],
                "last_seen": r["last_seen"],
            }
            for t, r in ranked
        ],
    }
    (WIKI_ROOT / "interests.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def write_md(ranked, files):
    lines = [
        "# Research Interests (auto-generated)",
        "",
        f"Generated {date.today().isoformat()} from {files} wiki pages by `scan_interests.py`.",
        "Weights: question 2.0 > paper 1.5 = seminar 1.5 = project_meeting 1.5 "
        "> textbook_study 0.5 > routine_meeting 0.1 = conversation 0.1, with a "
        f"{HALFLIFE_YEARS:.0f}-year recency half-life. **Do not edit by hand.**",
        "",
        "| Rank | Topic | Score | Sources | Last seen |",
        "|---|---|---|---|---|",
    ]
    for i, (t, r) in enumerate(ranked, 1):
        srcs = ", ".join(f"{k}×{n}" for k, n in sorted(r["counts"].items())) or "—"
        lines.append(
            f"| {i} | {t} | {r['score']:.2f} | {srcs} | {r['last_seen'] or '—'} |"
        )
    lines.append("")
    (WIKI_ROOT / "interests.md").write_text("\n".join(lines), encoding="utf-8")


def update_briefing(ranked):
    if not BRIEFING_INTERESTS.exists():
        print(f"[skip] Briefing interests file not found: {BRIEFING_INTERESTS}")
        return
    top = [t for t, _ in ranked[:TOP_QUERIES]]
    block_lines = [
        AUTO_START,
        f"<!-- regenerated {date.today().isoformat()} by scan_interests.py — edits inside this block are overwritten -->",
    ]
    for t in top:
        block_lines.append(f"- {t.replace('-', ' ')}")
    block_lines.append(AUTO_END)
    block = "\n".join(block_lines)

    text = BRIEFING_INTERESTS.read_text(encoding="utf-8-sig", errors="replace")
    if AUTO_START in text and AUTO_END in text:
        text = re.sub(
            re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END),
            block,
            text,
            flags=re.DOTALL,
        )
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    BRIEFING_INTERESTS.write_text(text, encoding="utf-8")
    print(f"[ok] Updated briefing AUTO block with {len(top)} topics.")


def main():
    files, ranked = scan()
    write_json(ranked, files)
    write_md(ranked, files)
    update_briefing(ranked)
    print(f"[ok] Scanned {files} tagged pages, ranked {len(ranked)} topics.")
    for t, r in ranked[:TOP_QUERIES]:
        print(f"    {r['score']:6.2f}  {t}")


if __name__ == "__main__":
    main()
