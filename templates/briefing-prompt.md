# Daily Paper Briefing — task instructions

Run from the wiki root. `{CHANNEL}` was set during setup. Web access is allowed for this task
only (PubMed E-utilities); it never overrides the wiki's other rules.

Aim for **about 5 papers, quickly**. This is a morning glance, not a literature review. Fast and
roughly right beats slow and exhaustive — judge from titles, and do not fetch abstracts.

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
   a field name rather than a query — skip it and record it as skipped in the briefing. Never
   sample from it.

   Sleep ~0.3 s between calls; NCBI asks for no more than 3 requests per second.

3. Pick ~5 papers overall. Dedupe by PMID, and also against PMIDs already reported in the last few
   `briefings/*.md` so the same paper does not return three mornings running. Drop
   correction/erratum/retraction notices. Prefer papers matching more than one topic.

   Relevance beats quantity — two good papers is a fine briefing, five padded ones is not. If
   everything comes back empty or off-topic, say that instead of filling the quota.

4. Write `briefings/{YYYY-MM-DD}.md`. Per paper: exact English title (verbatim, never
   translated), journal, date, PubMed link (`https://pubmed.ncbi.nlm.nih.gov/{PMID}/`), and one
   line on which interest it matches and why. If it relates to an existing wiki page, add the
   `[[wikilink]]`.

5. Deliver via **{CHANNEL}**:
   - **desktop**: send a push notification, e.g. "논문 브리핑: 5편 — 오늘의 pick: {top title}"
     (notification text in the user's language; paper titles stay English).
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
