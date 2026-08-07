# Daily Paper Briefing — task instructions

Run from the wiki root. `{CHANNEL}` was set during setup. Web access is allowed for this task
only (PubMed E-utilities); it never overrides the wiki's other rules.

Aim for **5 papers, quickly**. This is a morning glance, not a literature review. Screen on titles
alone — that is what keeps it fast — then read the abstracts of the five finalists only, so the
lines you write about them are true. Five abstracts costs one request.

1. Refresh the interest profile: run `python scan_interests.py` if it exists (on failure, carry on
   with the existing file). Then read `briefing/interests.md` and build the topic list:
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

   **Read `count` in the esearch response.** More than ~150 hits in the window means that topic is
   a field name rather than a query — skip it. Never sample from it. Name the skipped topics in
   the one-line run note at the foot of the briefing (step 4), not in the body.

   Sleep ~0.3 s between calls; NCBI asks for no more than 3 requests per second.

3. Pick 5 papers overall — the count rule is in step 4. Dedupe by PMID, and also against PMIDs
   already reported in the last few `briefings/*.md` so the same paper does not return three
   mornings running. Drop
   correction/erratum/retraction notices. Prefer papers matching more than one topic.

   Once the five are chosen — and only then — fetch their abstracts in a single call:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={5 PMIDs}&retmode=xml&rettype=abstract
   ```

   Write the "what it is" line from the abstract, not the title. Titles overstate and omit; a
   one-line description guessed from a title is how a briefing ends up describing a paper that
   does not exist. If a finalist's abstract shows it is not what the title implied, drop it and
   promote the next candidate.

   Relevance still beats the count: if fewer than 5 clear the bar, report fewer and say why
   rather than filling the quota with padding.

4. Write `briefings/{YYYY-MM-DD}.md`.

   **Body language: the user's language** — the same language you converse in (Korean for a Korean
   user). The wiki's English-only policy covers `sources/` and `wiki/`; `briefings/` is reading
   material for the user, not wiki content, so do not default it to English. Paper titles,
   journal names, and technical terms stay English.

   **How many:** exactly **5** unless the user asked for a different number. Fewer only when
   fewer than 5 relevant papers exist — then say so in one line and do not pad.

   Required per paper — all five, each one short line, no paragraphs:

   | Field | Content |
   |---|---|
   | Title | exact English title, verbatim, never translated |
   | Journal · date | journal name + the paper's date |
   | Link | `https://pubmed.ncbi.nlm.nih.gov/{PMID}/` |
   | What it is | what the paper does, in one line, taken from the abstract you fetched |
   | Why it was picked | which interest topic matched, and the concrete tie: a wiki page (`[[wikilink]]`), an active project, or a question the user asked |

   Then close with an **overall read** — 3–5 lines across the whole set: what the week looks like,
   which paper to read first, what was thin or missing. This is the part the user acts on, so
   never skip it, and never replace it with a restatement of the list.

   **Keep the machinery out of it.** The reader came for papers, not for a run log. Never put any
   of this in the briefing or in the chat summary of it: how many pages `scan_interests.py`
   scanned, how many topics ranked, which query strings ran, hit counts per topic, `retmax` /
   `reldate` / `sort` or any other parameter, sleep intervals, how many PMIDs were deduped, or a
   restatement of these instructions ("all five fields included, Korean body, English titles").
   Doing the job correctly is not news; only the papers are.

   The one permitted exception is a **single closing line** naming topics dropped for being too
   broad and topics that returned nothing — because silently searching less than the user thinks
   is a real problem. One line, at the very bottom, e.g.
   *"메모: `human identification`, `whole genome sequencing`는 범위가 넓어 건너뛰었고,
   `microhaplotype forensic panel`은 이번 주 신규 논문이 없습니다."*

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

## When the wiki is still thin

Below roughly 10 tagged pages the AUTO block is not yet a real signal: few tags, all tied in
score, and often too broad to search. Say so in one line at the top of the briefing, lean on the
manual queries, and ask the user to add two or three of their own — rather than presenting an
uninformed selection as an informed one.

## Tuning

This is what makes the briefing fit over time, so mention it when the user reacts to a briefing:

- "그건 추천하지 마" / "not interested in X" → add X under `## Excluded topics`.
- "이런 것도 챙겨줘" / "track X too" → add a bullet under `## Manual queries`.
