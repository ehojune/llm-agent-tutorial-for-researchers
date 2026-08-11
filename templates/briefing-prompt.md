# Daily Paper Briefing — task instructions

Run from the wiki root. `{CHANNEL}` was set during setup. Web access is allowed for this task
only (PubMed E-utilities — or the arXiv API, if setup applied "Fields PubMed does not cover"
below); it never overrides the wiki's other rules.

## Keep every command approvable

This task runs while nobody is watching, so a permission prompt is a stall. Shape the commands so
they can be pre-approved:

- **Never write a file through a shell heredoc.** No `cat > x.py <<'EOF'`. Build the file with the
  Write tool, then run it as its own plain command. A heredoc carrying a script is
  one long compound command that no allow rule can match, and a brace holding quoted strings —
  `{"a","b"}` — trips the shell's expansion-obfuscation check, which prompts regardless of what the
  allow list says.
- **One plain command per call, and no `cd` prefix.** The task already starts in the wiki root.
  `cd … && …` and `…; …` are compound: their permission prompt offers only "allow once", so an
  approval for them never carries to the next run.

Aim for **5 papers, quickly**. This is a morning glance, not a literature review. Screen on titles
alone — that is what keeps it fast — then read the abstracts of the five finalists only, so the
lines you write about them are true. Five abstracts costs one request.

1. Refresh the interest profile: run `{PYTHON} scan_interests.py` if it exists. On failure, carry
   on with the existing file, but say so in the closing note (step 4) — the custom version needs a
   working Python, so this is a repair to flag, not something to work around by recomputing the
   profile by hand. Then read `briefing/interests.md` and build the topic list:
   - every bullet under **`## Manual queries`** — always included, these are the backbone
   - the top ~6 from the AUTO block, in score order
   - drop anything matching a bullet under **`## Excluded topics`**, both as a query and later as
     a title filter

2. Per topic, take the 4 newest:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={TOPIC}&reldate=7&datetype=edat&sort=date&retmax=4&retmode=json
   ```

   Keep `datetype=edat` (PubMed entry date), not `pdat`. A paper published weeks ago but indexed
   yesterday is new *to the reader*, and `pdat` silently misses exactly those.

   then titles/journals/dates for the returned IDs:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ID1,ID2,...}&retmode=json
   ```

   `sort=date&retmax=4` is doing real work. Without it you get an arbitrary handful out of
   however many matched, presented as though it were a selection.

   **Tag every term `[tiab]`.** Build `{TOPIC}` by suffixing each word with `[tiab]` and joining
   with `AND` — `forensic genetics` becomes `forensic[tiab] AND genetics[tiab]`, URL-encoded as
   `forensic%5Btiab%5D+AND+genetics%5Btiab%5D`. Bare terms go through PubMed's automatic term
   mapping into `[All Fields]`, which matches author affiliations and explodes MeSH headings: a
   cardiology paper out of a Department of Forensic Medicine is a `forensic genetics` hit, and so
   is a gut-microbiome paper. Restricting to title/abstract cuts that without costing real
   papers — measured over a 30-day window: `forensic genetics` 91 → 21, `degraded dna` 1349 → 17,
   `RNA splicing variant pathogenic` 19 → 14, and `Y-STR haplotype population` 1 → 1. Do **not**
   quote the whole topic as one phrase (`"forensic genetics"[tiab]`); that demands the exact
   wording and takes the last two of those to 0.

   **Read `count` in the esearch response.**
   - **Over ~150** — a field name rather than a query. Skip it; never sample from it. If it is a
     line from the AUTO block and it has been skipped on several consecutive mornings, it will
     keep being regenerated, so move it under `## Excluded topics` in `briefing/interests.md` and
     tell the user in the closing note that you did. Editing inside the AUTO markers does
     nothing — the block is rewritten on the next run.
   - **Zero** — retry that one topic once at `reldate=30` before giving up. A specific query in a
     small field is legitimately empty most weeks (`Y-STR haplotype population`: 0 over 7 days,
     0 over 14, 1 over 30), and a briefing built only from 7-day windows in such a field has
     nothing to report on most mornings. Say which topics needed the wider window only if that is
     what kept the briefing short.

   Sleep ~0.3 s between calls; NCBI asks for no more than 3 requests per second.

3. Pick 5 papers overall — the count rule is in step 4. Dedupe by PMID, and also against PMIDs
   already reported in the last few `briefings/*.md` so the same paper does not return three
   mornings running. Drop
   correction/erratum/retraction notices. Prefer papers matching more than one topic.

   **Spread them across topics — take one per topic per round.** Go through the topics that
   returned anything, newest first within each, taking one paper each; then go round again, and
   again, until you have five. Interests differ wildly in publication volume, so taking the
   newest five outright hands the whole briefing to the busiest one: a run of four
   materials-science seed queries put four of its five papers under a single topic, and the
   reader then sees a single-subject digest with no sign the others were searched at all.

   Rounds settle the awkward splits by themselves — four productive topics give 2/1/1/1, two
   give 3/2, one gives all five — so there is no cap to deadlock against.

   **If the rounds run dry before five, go back for more before reporting a short briefing.**
   Only four papers per topic reach this step (`retmax=4`; on the arXiv path, the newest four
   in the window), which is plenty when several topics deliver and short when a single topic is
   carrying the day. Re-query the productive topics with a larger `retmax`, and keep widening
   until you have five or the topic's `count` is exhausted — a fixed second number does not do,
   because dedupe against recent briefings, dropped errata, and title screening all eat into
   whatever you fetch. On the arXiv path the 30 entries already retrieved usually cover it, so
   look there first; if they do not, keep paging — `&start=30`, then `60`, and on — at the same
   3-second cadence, stopping when you have five or an entry falls outside the window. A topic
   can hold well over 30 papers inside the 30-day retry window (measured: one seed query had 45
   across two pages), and the earlier breadth rule deliberately allows that. Neither path has a
   fixed ceiling, on purpose: step 4's "fewer than 5" line is for when the papers do not exist,
   not for when they were not asked for.

   Once the five are chosen — and only then — fetch their abstracts in a single call:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={5 PMIDs}&retmode=xml&rettype=abstract
   ```

   Write the "what it is" line from the abstract, not the title. Titles overstate and omit; a
   one-line description guessed from a title is how a briefing ends up describing a paper that
   does not exist. If a finalist's abstract shows it is not what the title implied, drop it and
   promote the next candidate — and when there is no next candidate, because the pool held
   exactly five, widen again as above rather than reporting four. Abstract rejections are the
   normal way this loop ends, not an exception to it.

   Relevance still beats the count: if fewer than 5 clear the bar, report fewer and say why
   rather than filling the quota with padding.

4. Write `briefings/{YYYY-MM-DD}.md`.

   **Body language: the user's language** — the same language you converse in (Korean for a Korean
   user). The wiki's English-only policy covers `sources/` and `wiki/`; `briefings/` is reading
   material for the user, not wiki content, so do not default it to English. Paper titles,
   journal names, and technical terms stay English.

   **How many:** exactly **5** unless the user asked for a different number. Fewer only when
   fewer than 5 relevant papers exist — then say so in one line and do not pad.

   Every paper needs five things: the **exact English title** (verbatim, never translated), the
   **journal and date**, the **PubMed link**, **what the paper does** (from the abstract you
   fetched), and **why it was picked** — which interest matched, and the concrete tie: a wiki
   page (`[[wikilink]]`), an active project, or a question the user asked.

   On the arXiv path, two of those read differently: the link is the `abs` URL, and only the
   **date** is required — a preprint has no journal until someone publishes it. Use the entry's
   `journal_ref` when it is there; otherwise write *arXiv preprint* and the primary category,
   e.g. *arXiv preprint · cond-mat.mtrl-sci · 2026-08-05*. Never call arXiv itself the journal,
   and never drop a paper for lacking one — in a 7-day window almost none will have it
   (measured: 0 of the 8 newest perovskite entries carry `journal_ref`, against 5 of the 10
   oldest, which have had a decade to be published).

   **Write it as prose, not as a form.** Those five are what must be present, not a layout to
   reproduce. A briefing that renders them as labelled bullets — `- **저널·날짜** — …`,
   `- **어떤 논문인가** — …` — reads like a database dump and is the single fastest way to make a
   good briefing unpleasant. Heading, then a short paragraph or two that happen to contain
   everything. Like this:

   ```markdown
   ## 1. Assessing the influence of different alignment tools on the accuracy of a forensic epigenetic clock

   *Bioinformatics* · 2026-08-04 · https://pubmed.ncbi.nlm.nih.gov/42550240/

   검증된 forensic epigenetic clock 데이터를 bisulfite 정렬 도구 네 가지로 각각 돌려 예측
   연령을 비교했습니다. 원래 쓰던 Bwa-meth를 이긴 도구는 없었지만 도구마다 나이가 달라졌고,
   같은 비교를 직접 해볼 Shiny 앱도 함께 냈습니다.

   `DNA methylation age estimation forensic` 매칭입니다. 위키의 `epigenetics-age` 칸이 아직
   비어 있는데, 첫 페이지로 앉히기 좋은 방법론 논문입니다.
   ```

   Two short paragraphs: what it is, then why you are seeing it. That is the whole format.

   Then close with an **overall read** — 3–5 lines across the whole set: what the week looks like,
   which paper to read first, what was thin or missing. This is the part the user acts on, so
   never skip it, and never replace it with a restatement of the list.

   **Keep the machinery out of it.** The reader came for papers, not for a run log. Never put any
   of this in the briefing or in the chat summary of it: how many pages `scan_interests.py`
   scanned, how many topics ranked, which query strings ran, hit counts per topic, `retmax` /
   `reldate` / `sort` or any other parameter, sleep intervals, how many PMIDs were deduped, or a
   restatement of these instructions ("all five fields included, Korean body, English titles").
   Doing the job correctly is not news; only the papers are.

   The one permitted exception is a **single closing note** covering only what made the briefing
   narrower than the user expects — because silently searching less than they think is a real
   problem. Three things qualify, nothing else: topics dropped for being too broad, topics that
   returned nothing, and `scan_interests.py` failing to run (which means the interest profile is
   stale and needs repair). Keep it to a line, at the very bottom, e.g.
   *"메모: `human identification`, `whole genome sequencing`는 범위가 넓어 건너뛰었고,
   `microhaplotype forensic panel`은 이번 주 신규 논문이 없습니다."*
   With a scanner failure, add: *"관심사 스캐너가 돌지 않아 기존 목록으로 진행했습니다 — Python
   확인이 필요합니다."*

   Everything else about the run stays available on request — if the user asks how it searched,
   tell them then.

5. Deliver via **{CHANNEL}**. Whichever channel it is, **the briefing body has to reach the user
   somewhere other than the file** — `briefings/{YYYY-MM-DD}.md` is the archive, not the delivery.

   - **desktop**: the session is the delivery. Write the briefing out in your reply — the same
     five entries and the overall read, not a report that a file was written — because that reply
     is what the user sees when they open the task from the notification. Then fire the push
     notification as the ping, e.g. "논문 브리핑: 5편 — 오늘의 pick: {top title}" (notification
     text in the user's language; paper titles stay English). A one-line notification plus a reply
     saying the file is ready leaves the user two clicks from what they asked for.
   - **email**: send the briefing body to the user's address with the connected email tool.
   - **slack**: post the briefing to the agreed channel or DM.
   - **notion**: create a page in the agreed database.
   - Destination recorded at setup: `{DESTINATION}`

6. Never ingest papers into the wiki from this task. Briefing is discovery only — the user
   downloads the PDF and asks for ingest.

## Fields PubMed does not cover

PubMed is biomedicine and the life sciences. When the wiki's field lives elsewhere (materials
science, ML, astronomy, …), setup swaps step 2's URLs for the arXiv API, and the same
discipline applies — screen on titles, read only the finalists' abstracts:

```
https://export.arxiv.org/api/query?search_query={QUERY}&sortBy=submittedDate&sortOrder=descending&max_results=30
```

- `{QUERY}` shape: **one `abs:` term per word, joined with `AND`**, plus `cat:` pinning the
  subject area. `perovskite solar cells` becomes
  `abs:perovskite+AND+abs:solar+AND+abs:cells+AND+cat:cond-mat.mtrl-sci`. `[tiab]` and
  `reldate` are PubMed syntax and mean nothing here; `abs:` is what restricts a term to the
  abstract, so it is the direct equivalent of tagging each term `[tiab]`.

  **Do not quote the whole topic** (`abs:"solid state electrolyte interface"`) — same trap as
  on the PubMed side, and it bites harder here. A quoted phrase demands that exact wording in
  that exact order, so a topic phrased slightly differently than authors phrase it returns
  nothing *at all* — not a thin week, an empty corpus. Measured over four materials-science
  seed queries: quoted, two of the four returned 0 results ever; per-term, the same two return
  30 and have a paper inside 30 days. The other two were unchanged or slightly better.
- Each Atom entry already carries title, abstract, dates, and link, so the esummary and efetch
  calls fall away — one call per topic covers steps 2 and 3's fetches.
- **There is no date window, so `max_results` is 30, not 4.** The filtering PubMed does with
  `reldate` you do yourself: keep entries whose `published` is within 7 days (30 on the
  zero-result retry), then take the newest 4 of those. Asking for 4 outright returns the newest
  4 *ever* — for the perovskite query above, four entries reaching back two months, of which one
  is actually recent.
- **Ignore `totalResults`; the ~150 rule in step 2 does not apply here.** That count is
  corpus-wide, not windowed, so it says 299 for the focused perovskite query — a topic with
  exactly one new paper this week would be thrown out as "too broad". The arXiv equivalent of
  that rule is: if **all 30** entries are still inside the **7-day** window, there are more than
  30 papers a week on it, so it is a category and not a topic — skip it, and treat it like the
  over-150 case. (Measured: `cat:cond-mat.mtrl-sci` alone returns 30 of 30 inside the window;
  the same category with `perovskite`, `solar` and `cells` AND-ed on returns 1.)

  **Do not apply that cutoff to the 30-day retry.** 30 entries inside 30 days is about seven a
  week, which is a healthy topic, not a category — and the retry only runs for topics that
  returned *nothing* over 7 days, so it cannot be one anyway. arXiv makes this concrete:
  submissions bunch around conference deadlines, so a quiet week followed by a heavy three
  weeks is ordinary here. Throwing that topic away would discard exactly what the retry went
  back to find.
- Dedupe by arXiv id; link entries as `https://arxiv.org/abs/{id}`.
- **Sleep ~3 s between calls, one at a time — not the 0.3 s above.** That figure is NCBI's;
  arXiv's terms ask for "no more than one request every three seconds, and … a single
  connection at a time". Ten times slower, but this path also makes one call per topic instead
  of three, so a ten-topic briefing still runs in well under a minute.

Everything else — five papers, prose body, the closing note — is unchanged.

## When the wiki is still thin

Below roughly 10 tagged pages the AUTO block is not yet a real signal: few tags, all tied in
score, and often too broad to search. Say so in one line at the top of the briefing, lean on the
manual queries, and ask the user to add two or three of their own — rather than presenting an
uninformed selection as an informed one.

## Tuning

This is what makes the briefing fit over time, so mention it when the user reacts to a briefing:

- "그건 추천하지 마" / "not interested in X" → add X under `## Excluded topics`.
- "이런 것도 챙겨줘" / "track X too" → add a bullet under `## Manual queries`.
