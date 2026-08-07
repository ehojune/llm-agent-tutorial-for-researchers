# SETUP — instructions for the AI agent

You are reading this because a user asked you to set this tutorial up ("나도 이거 세팅해줘",
"set this up for me", or similar). Follow the steps in order. Converse in the user's language;
all wiki *content* is written in English.

Notes before you start:

- This setup itself needs web fetches (this repo's raw files, the upstream gist, PubMed later).
  The wiki's "no web search" rule applies to answering questions **after** setup, not to setup.
- Template raw URLs used below:
  - `https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/templates/CLAUDE-custom.md`
  - `https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/templates/wiki-extras.md`
  - `https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/templates/briefing-prompt.md`
  - `https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/templates/scan_interests.py`
  - `https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/templates/project-base.md`
    (post-setup module — do NOT run during setup; the wiki-extras rulebook points to it)

## Step 1 — Ask, in two short rounds

**Round 1 (the wiki):**

1. Research field (e.g. genomics, immunology, materials science).
2. Wiki folder location. Default: `~/llm-wiki` (Windows: `%USERPROFILE%\llm-wiki`). If the user
   doesn't care, use the default without further discussion.
3. Which version — present this honestly and let them pick:
   - **Original** (Prof. Joon-Yong An, Korea Univ.): a papers-only knowledge base, refined by
     running it past 15,000 papers. Includes synthesis requirements, daily logs, a validator,
     and BM25 retrieval. Non-paper material is kept *outside* the knowledge layer
     (`materials/`, `agenda/`). Heavier, but battle-tested for scale.
   - **Custom** (Hojune Lee): lighter personal variant. Papers **plus** research life —
     seminar notes, project meetings, textbook study, chat questions — are first-class wiki
     pages with tags, and those tags automatically feed the daily briefing's interest profile.
   If they can't decide: custom for a personal starter wiki, original for a lab-scale archive.

**Round 2 (the briefing):**

4. What time each day the paper briefing should run (e.g. 09:00).
5. How to receive it — explain the trade-offs briefly:
   - **Desktop notification** (recommended, zero setup): the Claude Desktop scheduled task fires
     an OS notification and the briefing text is in the session + a file.
   - **Email**: needs the user's own email connector (e.g. Gmail MCP); sent from their account.
     There is no built-in "no-reply" mail from Anthropic.
   - **Slack**: needs a Slack MCP connector.
   - **Notion**: needs the Notion MCP connector.
6. 5–10 seed PubMed **queries** (English) — not field names. Each needs two or three specific
   terms, or PubMed's automatic term mapping widens it into the entire field: `forensic genetics`
   expands to `"forensic"[All Fields] AND "genetics"[All Fields]` and returns cerebral ischemia
   and gut microbiome papers, while `forensic STR profiling` does not. Draft a list in that shape
   from their field and let them edit. Good shapes: `Y-STR haplotype population`,
   `RNA splicing variant pathogenic`, `rare variant burden association disease`.

## Step 2 — Build the wiki

Create the wiki folder first if it doesn't exist.

### 2a. Original version

1. Fetch the gist and read **all** its files:
   `https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959`
2. Follow its own "Getting started" instructions: create the folder tree, write `AGENTS.md`
   from `AGENTS.md.template` filled in for the user's field and 5–10 categories (propose them,
   let the user edit).
3. `CLAUDE.md` should mirror `AGENTS.md`. On macOS/Linux: `ln -s AGENTS.md CLAUDE.md`. On
   Windows symlinks usually fail without developer mode — instead write a `CLAUDE.md`
   containing only: *"Read `AGENTS.md` and follow it. That file is the single source of truth."*
4. Skip the BM25 retrieval-index setup for now and tell the user it becomes worthwhile past
   ~500 pages (the gist says the same).

### 2b. Custom version

1. Fetch `templates/CLAUDE-custom.md`, fill in `[YOUR FIELD]` and the category table (5–10
   categories proposed from the field, user-approved), and save it as `{wiki}/CLAUDE.md`.
2. Create the folders: `papers/`, `papers/textbooks/`, `sources/`,
   `wiki/{each-category}/`, `wiki/overviews/`, `wiki/concepts/`, `wiki/seminars/`,
   `wiki/notes/`, `wiki/project-meetings/`, `wiki/routine-meetings/`, `wiki/textbook-study/`,
   `wiki/conversations/`, `wiki/other/`.
3. Fetch `templates/scan_interests.py` and save it as `{wiki}/scan_interests.py`.
4. Create an empty `index.md` with the category headings.

## Step 3 — Briefing system (both versions)

1. Create `{wiki}/briefing/` and `{wiki}/briefings/`.
2. Write `{wiki}/briefing/interests.md`:

   ```markdown
   # Briefing interests

   ## Manual queries

   Yours — never overwritten. Two or three specific terms each, not a field name.

   - query one
   - query two

   ## Excluded topics

   Subjects never to suggest. Grows as you tell the agent a topic is not interesting.

   <!-- AUTO:wiki-interests START -->
   <!-- Regenerated by scan_interests.py from wiki tags. Do not edit inside this block. -->
   <!-- AUTO:wiki-interests END -->
   ```

   with the user's seed queries as the manual bullets, and `## Excluded topics` left empty. The
   manual queries are the backbone of the briefing — wiki tags only supplement them, and on a new
   wiki they are all there is. (Original version: the AUTO block stays empty, which is fine.)
3. Fetch `templates/briefing-prompt.md`, fill `{CHANNEL}` with the chosen channel and
   `{DESTINATION}` with the address/channel/database (`n/a` for desktop), and save it as
   `{wiki}/briefing/PROMPT.md`.
4. Fetch `templates/wiki-extras.md`, fill `{BRIEFING_TIME}`, and **append it** to the rulebook
   (`CLAUDE.md` for custom, `AGENTS.md` for original). This adds three things: the automatic
   ingest follow-up report, the briefing web-access exception, and the catch-up rule for
   missed briefings.
5. If the channel needs a connector (email/Slack/Notion), walk the user through connecting it
   now, and record the destination (address / channel / database) inside `briefing/PROMPT.md`.
6. Create a **scheduled task** (Claude Desktop scheduled-tasks feature): daily at the chosen
   time, working directory = the wiki folder, instruction:
   *"Open briefing/PROMPT.md in this folder and follow it."*
   - If your environment has no scheduled-task capability (e.g. plain CLI), say so and tell
     the user the schedule needs the Claude Desktop app; meanwhile "브리핑 해줘" runs it on
     demand.
7. Tell the user plainly: the machine must be on at briefing time; if it wasn't, the catch-up
   rule kicks in the next time they open Claude in the wiki folder.

## Step 4 — Korean humanizer skill

Install the `humanizer` skill from DaleSeo/korean-skills (MIT) into the user's skills folder:

```bash
git clone --depth 1 https://github.com/DaleSeo/korean-skills /tmp/korean-skills
cp -r /tmp/korean-skills/skills/humanizer ~/.claude/skills/humanizer
```

(Windows: `%USERPROFILE%\.claude\skills\humanizer`. No git? Fetch the files under
`skills/humanizer/` from the GitHub API instead.) Skip only if the folder already exists.

## Step 5 — Verify, then give the tour

Verify: folder tree exists · rulebook present with the extras appended · `briefing/interests.md`
and `briefing/PROMPT.md` written · scheduled task registered · humanizer installed.

Then close with a short tour **in the user's language**:

- **Adding papers**: put PDFs anywhere (e.g. Downloads) and say "이 논문 ingest 해줘". You'll
  register it *and automatically* report a short summary plus which existing wiki pages it
  links to.
- **Custom version only**: mention that ongoing projects, seminars, and textbook chapters can
  also be recorded — then ask: *"지금 정리해둘 진행 중인 프로젝트나 최근 세미나가 있나요?"*
  If yes, create the first entry right away.
- **Asking questions**: answers come only from ingested papers; if none exists, Claude says so
  and asks for the PDF. Good answers can be saved as overview pages ("이거 overview로 저장해줘").
- **Tuning the briefing**: it is meant to be corrected out loud, not edited by hand. "그건 추천하지
  마" drops a subject for good; "이런 것도 챙겨줘" adds one. Tell the user this on day one — a
  briefing nobody corrects stays generic, and the first week is when it is furthest off.
- **Humanizer**: 한국어 글을 다듬고 싶을 때 "이 글 자연스럽게 해줘".
- **Recommended next step — project base**: for each ongoing research project, a GitHub repo or
  Notion page can hold the *work itself* (README, plans, code, data locations) — the wiki holds
  what you learned, the project base holds the work. Its killer use: when a conversation runs
  long or you switch agents, "프로젝트 맥락 전부 README에 정리해서 저장해줘" then hand the new
  agent just the link. GitHub gives native agent access and full history ("git에 저장해줘" =
  commit+push, no git knowledge needed); Notion is easier to edit/share and can later hook into
  a to-do tracker and Notion Calendar. Sensitive research → private (toggleable anytime;
  collaborators can still be invited). Don't set it up now — tell the user to ask
  **"프로젝트 베이스 만들어줘"** whenever they're ready, in any future session.
- **Graph view**: install Obsidian (free) and open the wiki folder as a vault whenever they
  want a visual map.
- **Reading**: short intro <https://joonan30.github.io/llm-wiki-labs/evolution/> · full free
  ebook <https://github.com/chaek-union/llm-wiki-for-scientists>.

Do not ingest any sample papers yourself; wait for the user's first PDF.
