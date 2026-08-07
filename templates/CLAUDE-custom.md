# LLM Wiki — [YOUR FIELD]

A personal knowledge base of [YOUR FIELD] papers, following [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285),
extended for non-paper research life (seminars, meetings, study notes) and a daily paper briefing:

```
Original PDF → sources/*.md (LLM summary) → wiki/{category}/*.md (final page)
```

**Language policy**: All wiki content is in English. Conversation can be in any language.

---

## THE FOUR RULES (do not violate)

These rules are the core of the system. They prevent hallucination and keep every claim traceable.

1. **No web search.** Never use `WebSearch` or `WebFetch` to fill gaps. The point of this wiki is that every answer is grounded in papers we actually have. (Sole exception: the daily briefing task — see "Daily Paper Briefing" below.)
2. **Answer from the wiki first.** Use `sources/` and `wiki/` as the only sources of truth.
3. **If the wiki is insufficient, re-read the PDF.** Go to `papers/{author}-{year}-{words}.pdf` and extract more detail with `pypdf`. Then update the wiki.
4. **If the wiki has no paper on the topic, say so.** Tell the user *"I don't have a paper on this — please give me the PDF."* Do not improvise.

These rules apply to **every** response, including overview pages: cite only papers that exist in the wiki.

---

## Repository Structure

```
llm-wiki/
├── CLAUDE.md               # This file
├── index.md                # Page catalog
├── scan_interests.py       # Aggregates wiki tags into the interest profile
├── briefing/               # interests.md + PROMPT.md (daily briefing config)
├── briefings/              # Daily briefing output, {YYYY-MM-DD}.md
├── papers/                 # Original PDFs (cp, never symlink)
│   ├── textbooks/          #   textbook chapter PDFs
│   └── {author}-{year}-{title-5-words}.pdf
├── sources/                # PDF summaries (English)
│   └── {author}-{year}-{title-5-words}.md
└── wiki/                   # Wiki pages (English)
    ├── {category}/
    └── overviews/          # Synthesis pages (where compounding happens)
```

## File Naming Convention

All three tiers (PDF, source, wiki) share the same stem:

```
{first-author-lastname}-{year}-{title-5-words}.{ext}
```

- Lowercase, special chars stripped, spaces → `-`
- Year is 4 digits
- Consortium papers: use consortium name (e.g. `1000-genomes-project-2015-...`)

Example: `pollard-2006-an-rna-gene-expressed-during.pdf`

## Categories

> Filled in during setup: 5–10 categories matching the user's field, plus the fixed rows below.

| Category | Includes |
|---|---|
| `[your-category-1]` | [what goes here — and what deliberately does not] |
| `[your-category-2]` | [...] |
| `concepts` | Key methods, algorithms explained generically |
| `overviews` | Synthesis pages spanning multiple papers |
| `seminars` | Talk/seminar notes — see Non-Paper Content |
| `notes` | Chat questions & insights worth keeping — see Non-Paper Content |
| `project-meetings` | Project meeting notes (active work) — see Non-Paper Content |
| `routine-meetings` | Routine/recurring meeting notes — see Non-Paper Content |
| `textbook-study` | Textbook chapter study (chapter PDF + your memo) — see Non-Paper Content |
| `conversations` | General conversation logs (placeholder) — see Non-Paper Content |
| `other` | Cross-cutting, miscellaneous |

Tip: classify by **method**, not topic. A methylation paper studying a phenotype goes to the
methylation category, not the phenotype's category.

---

## Adding a New Paper

### Step 1 — Copy PDF to `papers/` and extract text

Use `pypdf` (pure Python, no Java required). Run it with the Python launcher that setup verified —
the examples say `python`, but on Windows it is often `py`:

```bash
python -m pip install pypdf

python -c "
import pypdf, sys, pathlib
reader = pypdf.PdfReader(sys.argv[1])
text = ''
for page in reader.pages[:15]:
    t = page.extract_text()
    if t: text += t + '\n'
    if len(text) > 12000: break
pathlib.Path(sys.argv[2]).write_text(text[:12000], encoding='utf-8')
" "/path/to/paper.pdf" extracted.txt
```

Write to a UTF-8 file rather than printing. On a non-UTF-8 console — Korean Windows defaults to
cp949 — `print()` dies with `UnicodeEncodeError` on the first accented author name or Greek
letter, and the extraction looks like a tooling failure rather than an encoding one.

For long or dense papers, widen the page range and character cap — a small cap truncates the
paper mid-Methods and still looks like success.

### Step 2 — Write `sources/{stem}.md`

```yaml
---
title: "Paper Title"
authors: Author List
year: YYYY
doi: DOI
category: [category]
pdf_path: /full/path/to/papers/{stem}.pdf
pdf_filename: {stem}.pdf
source_collection: external
---

## One-line Summary
## 1. Document Information
## 2. Key Contributions
## 3. Methodology and Architecture
## 4. Key Results and Benchmarks
## 5. Limitations and Future Work
## 6. Related Work
## 7. Glossary
```

### Step 3 — Write `wiki/{category}/{stem}.md`

```yaml
---
title: "Paper Title"
authors: Author list
year: YYYY
doi: DOI
source: {stem}.md
category: [category]
pdf_path: /full/path/to/papers/{stem}.pdf
pdf_filename: {stem}.pdf
source_collection: external
tags: []
---

## Summary
## Key Contributions
## Methodology and Architecture
## Results
## Related Papers
- [[category/page]] — relationship
```

### Step 4 — Update `index.md`

Add a one-line entry under the right category.

(An automatic follow-up report after every ingest is required — see "PDF Ingest Follow-up"
appended below.)

---

## Non-Paper Content (seminars, meetings, study, notes)

Not all knowledge comes from a paper PDF. These content types are **single-tier**: create only a
`wiki/` page (no `sources/` entry). Most have no PDF; `textbook-study` is the exception (chapter
PDF + your memo). Distinguish them by `source_collection`.

| Kind | Folder | `source_collection` | PDF? | Origin | Required tags |
|---|---|---|---|---|---|
| Paper | `wiki/{category}/` | `external` | yes | PDF | topic tags |
| Seminar | `wiki/seminars/` | `seminar` | no | notes/PDF | `seminar` + topics |
| Project meeting | `wiki/project-meetings/` | `project_meeting` | no | notes/PDF | `project-meeting` + topics |
| Routine meeting | `wiki/routine-meetings/` | `routine_meeting` | no | notes/PDF | `routine-meeting` + topics |
| Textbook study | `wiki/textbook-study/` | `textbook_study` | **yes** | chapter PDF + memo | `textbook-study` + topics |
| Chat note | `wiki/notes/` | `chat` | no | chat | `question` + topics |
| Conversation | `wiki/conversations/` | `conversation` | no | chat log | `conversation` + topics |

**Naming**: all of these use `{YYYY-MM-DD}-{slug}.md` (date-first) instead of the author-year
stem. Textbook chapters: `{YYYY-MM-DD}-{book}-ch{NN}-{slug}.md`.

**Frontmatter**:
- **Seminar / meeting**: `title, date, speaker (or attendees), event, category,
  source_collection, tags`. Sections: `## Notes`, `## Key Takeaways`, `## Related Papers`.
- **Textbook study**: `title, date, book, chapter, category, source_collection, pdf_path,
  pdf_filename, tags`. Chapter PDF goes in `papers/textbooks/`. Sections: `## Chapter Summary`,
  `## My Notes`, `## Key Takeaways`, `## Related Papers`.
- **Note / conversation**: `title, date, category, source_collection, tags`. Sections:
  `## Question`, `## Answer / Insight`, `## Follow-ups`, `## Related`.

**Labeling rule (extends the Four Rules).** These entries are allowed sources, but they are
*not* substitutes for paper grounding. When you cite one, label it explicitly — *"(seminar
note)"*, *"(project meeting)"*, *"(textbook study)"*, *"(your prior question)"* — so
paper-grounded claims stay distinguishable from recorded personal knowledge.

## Interest Profile (feeds the daily briefing)

Every wiki page carries `tags`. The script `scan_interests.py` aggregates them into a weighted
interest profile:

```bash
python scan_interests.py
```

On Windows the launcher may be `py` instead. If neither runs, the Python that setup verified is
gone — repair it rather than hand-computing the profile or writing a throwaway replacement script.

- **Weights** (interest contribution per source type): chat question = 2.0 (active curiosity,
  strongest signal) > paper = seminar = project_meeting = 1.5 > textbook_study = 0.5 >
  routine_meeting = conversation = 0.1. Scores decay with age (3-year recency half-life).
- **Outputs**:
  - `interests.json` — machine-readable ranked topics (source of truth).
  - `interests.md` — human-readable ranked list.
  - Refreshes the auto-generated block (between `<!-- AUTO:wiki-interests -->` markers) in
    `briefing/interests.md`, which the daily briefing reads. **Manual keywords outside the
    markers are never touched.**

Re-run after ingesting any content so the briefing stays current.

## PDF Management Rules

- **Always copy, never symlink.** `cp` from external locations into `papers/`.
- `pdf_path` always points inside `papers/`. Never use `~/Downloads/` or other external paths.
- `pdf_filename` must match `basename(pdf_path)`.

## Knowledge Compounding

The most valuable pages are not individual paper summaries — they are `wiki/overviews/` pages
that synthesize across papers. When a question is answered well, save the answer:

> "Save this as an overview page in `wiki/overviews/`"

Over time the wiki becomes a searchable, cross-referenced knowledge graph that future
conversations draw from.

## Browsing with Obsidian

For visual navigation, install [Obsidian](https://obsidian.md/) (free) and open the wiki folder
as a Vault. Native support for `[[wikilinks]]`, graph view, and full-text search. Obsidian only
reads files, so it does not interfere with the agent's edits.

---

## Design Principles

- **3-tier**: Raw PDF (immutable) → sources/*.md → wiki/**/*.md
- **English only** in wiki content (RAG-friendly)
- **Obsidian compatible**: `[[wikilinks]]`, plain markdown
- **Consistent YAML**: every file has title, authors, year, doi, category, pdf_path,
  pdf_filename, source_collection
- **No web search**: rule #1 above

When in doubt, follow rule #1.
