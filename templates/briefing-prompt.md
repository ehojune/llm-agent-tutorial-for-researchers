# Daily Paper Briefing — task instructions

Run from the wiki root. `{CHANNEL}` was set during setup. Web access is allowed for this task
only (PubMed E-utilities); it never overrides the wiki's other rules.

1. Read `briefing/interests.md`. Collect topics from the AUTO block and the manual lines; take
   the top ~8 (manual lines always included).
2. For each topic, search PubMed E-utilities for the last 3 days:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={TOPIC}&reldate=3&datetype=edat&retmax=10&retmode=json
   ```

   then fetch titles/journals/dates for the returned IDs:

   ```
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ID1,ID2,...}&retmode=json
   ```

3. Select 5–15 papers overall: dedupe by PMID, drop correction/erratum/retraction notices,
   prefer papers matching multiple interests. If every topic comes back empty, write that in the
   briefing instead of padding with loosely related papers.
4. Write `briefings/{YYYY-MM-DD}.md`. Per paper: exact English title (verbatim, never
   translated), journal, date, PubMed link (`https://pubmed.ncbi.nlm.nih.gov/{PMID}/`), and one
   line on which interest it matches and why. If it relates to an existing wiki page, add the
   `[[wikilink]]`.
5. Deliver via **{CHANNEL}**:
   - **desktop**: send a push notification, e.g. "논문 브리핑: 12편 — 오늘의 pick: {top title}"
     (notification text in the user's language; paper titles stay English).
   - **email**: send the briefing body to the user's address with the connected email tool.
   - **slack**: post the briefing to the agreed channel or DM.
   - **notion**: create a page in the agreed database.
   - Destination recorded at setup: `{DESTINATION}`
6. Never ingest papers into the wiki from this task. Briefing is discovery only — the user
   downloads the PDF and asks for ingest.
