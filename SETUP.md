# SETUP — instructions for the AI agent

You are reading this because a user asked you to set this tutorial up ("나도 이거 세팅해줘",
"set this up for me", or similar). Follow the steps in order. Converse in the user's language;
all wiki *content* — `sources/` and `wiki/` pages — is written in English. Anything the user
*reads* rather than retrieves (daily briefings, follow-up reports, summaries in chat) goes in the
user's language, with paper titles left in English.

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
4. **Make sure Python works** — PDF extraction and `scan_interests.py` both need it. Run
   `python --version` (`py --version` on Windows) and accept a launcher only when it prints a
   version string: on Windows without Python, the Microsoft Store alias answers `python` with a
   store prompt and exit code 9009. Remember which launcher works; later steps use its name.
   If neither answers, ask to install Python and do it — the user has to approve the command, so
   just ask. If they cannot install at all, offer the original version from Step 2a, which needs
   no Python.
5. Create an empty `index.md` with the category headings.

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
6. **Ask for the permissions the briefing needs, and ask now.** This step decides whether the
   briefing ever runs unattended. Put the question to the user in their own language, roughly:

   > 브리핑은 매일 아침 자리에 안 계실 때 도는 작업입니다. 그때 권한을 물어보면 아무도 답하지
   > 않아 그대로 멈추고, 파일도 알림도 남지 않습니다. **이 위키 폴더 안에서** 파일을 읽고 쓰고,
   > PubMed를 검색하고, `scan_interests.py`를 돌릴 권한을 미리 열어둘까요? 이 폴더에서만
   > 적용되고, 다른 작업에는 영향이 없습니다.

   On yes, write `{wiki}/.claude/settings.json`:

   ```json
   {
     "permissions": {
       "defaultMode": "acceptEdits",
       "allow": [
         "Bash",
         "Read",
         "Write",
         "Edit",
         "Glob",
         "Grep",
         "WebFetch",
         "PushNotification"
       ]
     }
   }
   ```

   **Grant `Bash` as a whole, not command patterns.** Rules like `Bash(curl *)` look tidier and do
   not work: the briefing builds compound commands (`cd … && cat > file <<'EOF'`, pipelines), the
   permission parser cannot parse those, and an unparseable command falls through to a prompt no
   matter what the allow list says. A pattern list produces a briefing that halts some mornings
   and not others, which is worse than either extreme.

   The grant is scoped to this folder, so it changes nothing anywhere else on the machine. If the
   user would rather not, say plainly that the briefing will then need them present to click
   through, and that "브리핑 해줘" on demand is the realistic mode.

   If the chosen channel is email/Slack/Notion, add that connector's tool to the list too.

7. Create a **scheduled task** (Claude Desktop scheduled-tasks feature): **recurring, daily** at
   the chosen time, working directory = the wiki folder, instruction:
   *"Open briefing/PROMPT.md in this folder and follow it."*
   - **Recurring, not one-shot — including when you are only testing.** A one-shot task disables
     itself the moment it fires, and its session goes with it — the user reads the notification,
     looks at something else, comes back, and cannot find the briefing conversation again. A
     recurring task stays in the sidebar, so the conversation is still there tomorrow. This holds
     for test runs too: a one-shot needs its own run-once-only configuration, which you then throw
     away along with it. Register the daily task and test *that*.
   - If your environment has no scheduled-task capability (e.g. plain CLI), say so and tell
     the user the schedule needs the Claude Desktop app; meanwhile "브리핑 해줘" runs it on
     demand.

8. **Run it once now, with the user watching**, and check that it wrote `briefings/{today}.md`,
   printed the briefing in the session, and fired the notification. Any tool the settings file
   missed will prompt during this run; approving it here stores the approval on the task. A
   schedule that has never completed once is not set up, it is only scheduled.

9. **Teach the daily "권한 무시" click, right here at setup.** The routine opens a *new
   conversation every day*, and the approvals from yesterday's conversation do not carry over —
   so `.claude/settings.json` alone does not guarantee a silent run. In that day's routine
   conversation the user clicks **권한 무시** (bypass permissions), bottom-left of the input box,
   once. **Be explicit about *which* conversation** — not the setup conversation you are in right
   now, but the briefing routine's own conversation, opened from **루틴** in the left sidebar. To a
   first-time user every panel looks alike, and this is the one instruction they will get wrong.
   Walk them through it: sidebar 루틴 → the briefing entry → 권한 무시 under the input box. The
   README has both screenshots (`images/routine-sidebar.png`, `images/routine-permission-bypass.png`).
   Say plainly why it is safe here: the briefing only scans the wiki folder, searches PubMed, and
   writes `briefings/{date}.md`. And say plainly that it is a daily chore for now — routing the
   briefing to Slack or email later removes the need to check in at all.

10. Tell the user plainly: the machine must be on at briefing time, and the run can start a few
    minutes late rather than on the dot. If the machine was off, the catch-up rule kicks in the
    next time they open Claude in the wiki folder.

## Step 4 — Korean humanizer skill

Only relevant if the user writes Korean. Skip the whole step otherwise.

### 4a. Install

```bash
git clone --depth 1 https://github.com/DaleSeo/korean-skills /tmp/korean-skills
cp -r /tmp/korean-skills/skills/humanizer ~/.claude/skills/humanizer
```

Windows equivalent — `/tmp` does not exist, so clone somewhere real:

```bash
git clone --depth 1 https://github.com/DaleSeo/korean-skills "$TEMP/korean-skills"
cp -r "$TEMP/korean-skills/skills/humanizer" "$USERPROFILE/.claude/skills/humanizer"
```

No git? Fetch the files under `skills/humanizer/` from the GitHub API instead. Skip the install
only if the folder already exists.

### 4b. Ask whether it should apply automatically, and how widely

Installing the skill only makes it *available*. Without a standing instruction it fires when the
user asks for it and never otherwise — which is not what most people expect from "설치했다".

Ask, and offer three scopes:

| Scope | Where the instruction goes | Effect |
|---|---|---|
| **모든 대화 (recommend this)** | `~/.claude/CLAUDE.md` (Windows: `%USERPROFILE%\.claude\CLAUDE.md`) | Korean written in any project follows the patterns |
| 이 위키에서만 | `{wiki}/CLAUDE.md` | applies only when working in the wiki folder |
| 부를 때만 | nowhere | "자연스럽게 해줘" still works; nothing automatic |

Recommend the global scope, and give the actual reason: the agent writes Korean in every
conversation — chat replies, briefings, commit messages, summaries — and only a small slice of
that happens inside the wiki. Wiki *content* is English by policy, so a wiki-only scope aims the
rule at the one place it least applies.

Append this block to the chosen file (translate the headings if you like; keep the substance):

```markdown
## 한국어 글쓰기 기본값 — humanizer

AI가 쓴 한국어에는 40가지 특징적 패턴이 있습니다: 쉼표 과다, 번역투(`에 대해` / `를 통해` /
`되어진다` / `에 의해`), 품사 다양성 부족, AI 상투어, 불필요한 복수형 `-들`, `~적 N` 연쇄,
단조로운 문장 리듬 등. 근거는 KatFishNet 논문(AUC 94.88%)이고, 전체 목록은
`~/.claude/skills/humanizer/SKILL.md`에 있습니다.

**기본 동작 — 한국어를 쓰는 모든 응답에 자동 적용:** 그 패턴들을 피해서 씁니다. 자연스러운 쉼표
밀도, 변화 있는 문장 길이, 딱딱한 한자어·번역투 대신 익은 우리말. 이때 humanizer 스킬의 전체
분석 워크플로는 **돌리지 않습니다** — 패턴을 알고 처음부터 그렇게 쓰면 됩니다. 매 응답마다
탐지·재작성을 돌리면 느리고, 짧은 대답까지 망가집니다.

**명시적 호출:** 사용자가 기존 한국어 글을 주면서 "자연스럽게 해줘", "AI 흔적 지워줘", "humanize"
같이 말하면 그때 `humanizer` 스킬을 불러 전체 워크플로(패턴 탐지, 심각도 S1/S2/S3, 전후 비교,
의미 보존 검증)를 돌립니다.

**고치기 전에 세어보기.** 실제 텍스트의 패턴 수를 먼저 세세요. 이미 사람 범위 안인데 길이가
문제인 경우가 많습니다. `되어진다`, `가지고 있다`, `에 있어서`는 0이어야 합니다.
```

If the user already has such a block (their own wording, or from a previous run), leave it alone
and say so rather than appending a second copy.

## Step 5 — Verify, then give the tour

Verify: folder tree exists · rulebook present with the extras appended · `briefing/interests.md`
and `briefing/PROMPT.md` written · permissions asked about, and `.claude/settings.json` written
if granted · scheduled task registered **as recurring** and **run once successfully** · the daily
**권한 무시** click explained · humanizer
installed, with its scope chosen and the block appended
(or automatic application explicitly declined).

When you mention the schedule to the user, call it by the name they see in the sidebar — **루틴**
in Korean. "scheduled task" is the internal name and will send them looking for a menu entry that
is not there.

Then close with a short tour **in the user's language**:

- **Adding papers**: put PDFs anywhere (e.g. Downloads) and say "이 논문 ingest 해줘". You'll
  register it *and automatically* report a short summary plus which existing wiki pages it
  links to.
- **Custom version only**: mention that ongoing projects, seminars, and textbook chapters can
  also be recorded — then ask: *"지금 정리해둘 진행 중인 프로젝트나 최근 세미나가 있나요?"*
  If yes, create the first entry right away.
- **Asking questions**: answers come only from ingested papers; if none exists, Claude says so
  and asks for the PDF. Good answers can be saved as overview pages ("이거 overview로 저장해줘").
- **The daily 권한 무시**: repeat it in the tour — each day's routine conversation is new, so one
  click on **권한 무시** *in that conversation* (사이드바 루틴 → 브리핑 항목) keeps the briefing
  from stalling on a prompt. Say again that it is the routine's conversation, not this one.
- **Tuning the briefing**: it is meant to be corrected out loud, not edited by hand. "그건 추천하지
  마" drops a subject for good; "이런 것도 챙겨줘" adds one. Tell the user this on day one — a
  briefing nobody corrects stays generic, and the first week is when it is furthest off.
- **Humanizer**: if they chose automatic application, tell them it is already on and that they do
  not need to ask each time — and that the scope is one line in the file you edited, so it can be
  narrowed or turned off later. Either way: 기존 글을 고칠 땐 "이 글 자연스럽게 해줘".
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
