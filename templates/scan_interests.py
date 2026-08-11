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
  - refreshes the AUTO block in briefing/interests.md (manual lines kept,
    excluded topics left out), which the daily paper briefing reads.

No third-party deps (no PyYAML required). Run:  python scan_interests.py
"""

import codecs
import json
import locale
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


# --- reading ---------------------------------------------------------------
def read_text_any(path):
    """Read a markdown file in whatever encoding Windows left it in.

    Tools on Windows do not agree, and the disagreement is silent:

      - PowerShell 5.1 `Out-File` (and `>`) defaults to UTF-16LE with a BOM
      - `-Encoding utf8` on 5.1 writes UTF-8 *with* a BOM
      - `Set-Content` defaults to the system ANSI codepage — cp949 on a Korean
        install — with no BOM at all
      - Notepad offers all of these

    Read as plain UTF-8, a BOM defeats parse_frontmatter's startswith("---")
    and the page drops out of the profile; UTF-16 is worse still, decoding to
    NULs and replacement characters that update_briefing() then writes back
    over the user's own queries. So sniff the BOM first, then try UTF-8, then
    fall back to the locale codepage.

    Files are always rewritten as UTF-8, so a wiki converges on one encoding.
    """
    raw = path.read_bytes()
    for bom, enc in (
        (codecs.BOM_UTF8, "utf-8-sig"),
        (codecs.BOM_UTF32_LE, "utf-32"),   # before UTF-16LE: shares its FF FE prefix
        (codecs.BOM_UTF32_BE, "utf-32"),
        (codecs.BOM_UTF16_LE, "utf-16"),
        (codecs.BOM_UTF16_BE, "utf-16"),
    ):
        if raw.startswith(bom):
            return raw.decode(enc)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode(locale.getpreferredencoding(False), errors="replace")


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
        text = read_text_any(path)
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


def parse_excluded(text):
    """Bullets under `## Excluded topics`, normalised to query form.

    The AUTO block lives inside that same section, so it is stripped first —
    otherwise every topic the last run generated would read as excluded and
    the block would empty itself on the next run.
    """
    manual = re.sub(
        re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END), "", text, flags=re.DOTALL
    )
    excluded = set()
    in_section = False
    for line in manual.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            in_section = stripped.lstrip("#").strip().lower() == "excluded topics"
            continue
        if in_section and stripped.startswith("- "):
            item = stripped[2:].strip().strip("`'\"")
            item = " ".join(item.replace("-", " ").split()).lower()
            if item:
                excluded.add(item)
    return excluded


def update_briefing(ranked):
    if not BRIEFING_INTERESTS.exists():
        print(f"[skip] Briefing interests file not found: {BRIEFING_INTERESTS}")
        return
    text = read_text_any(BRIEFING_INTERESTS)
    if "\x00" in text:
        # An encoding read_text_any did not recognise. Writing now would put the
        # mojibake back on disk and take the user's manual queries with it.
        print(f"[skip] {BRIEFING_INTERESTS} is not readable as text — left untouched.")
        print("       Re-save it as UTF-8 and run this again.")
        return

    # "그건 추천하지 마" must stick: a topic the user excluded stays out of the
    # AUTO block even while its tag keeps scoring high in the wiki. Without
    # this, excluded topics reappear every scan and hold top-N slots that the
    # briefing then filters away, shrinking what it actually searches.
    excluded = parse_excluded(text)
    top, skipped = [], 0
    for t, _ in ranked:
        if " ".join(t.replace("-", " ").split()) in excluded:
            skipped += 1
            continue
        top.append(t)
        if len(top) == TOP_QUERIES:
            break

    block_lines = [
        AUTO_START,
        f"<!-- regenerated {date.today().isoformat()} by scan_interests.py — edits inside this block are overwritten -->",
    ]
    for t in top:
        block_lines.append(f"- {t.replace('-', ' ')}")
    block_lines.append(AUTO_END)
    block = "\n".join(block_lines)

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
    note = f" ({skipped} excluded)" if skipped else ""
    print(f"[ok] Updated briefing AUTO block with {len(top)} topics{note}.")


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
