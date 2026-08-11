# SETUP — instructions for the AI agent

You are reading this because a user asked you to set this tutorial up ("나도 이거 세팅해줘",
"set this up for me", or similar). Follow the steps in order. Converse in the user's language;
all wiki *content* — `sources/` and `wiki/` pages — is written in English. Anything the user
*reads* rather than retrieves (daily briefings, follow-up reports, summaries in chat) goes in the
user's language, with paper titles left in English.

Notes before you start:

- This setup itself needs web fetches (this repo's raw files, the upstream gist, PubMed later).
  The wiki's "no web search" rule applies to answering questions **after** setup, not to setup.
- Setup gets re-run — a second machine, a template update, a straight replay. On a folder that
  already holds a wiki the rule is **the user's data wins**: steps 2, 3.2, 3.4, 4a and 7 each say
  what to keep. Nothing below is safe to blindly redo.
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
     an OS notification and the briefing text is in the session + a file. If they pick this, tell
     them now that the briefing runs as a **루틴** and that its permissions are a one-time setup you
     will walk them through at the end (steps 7–9) — not a daily click.
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

   **First check that PubMed even covers the field.** PubMed is biomedicine and the life
   sciences; question 1 names "materials science" as a perfectly good field, and a materials
   scientist's PubMed briefing would be empty or noise every single morning. If the field lives
   elsewhere (materials, ML, physics, astronomy…), say so plainly, and swap the briefing's
   search to the arXiv API — the briefing prompt has a section for exactly this (apply it in
   step 3.3), and the seed queries then follow its syntax instead.

## Step 2 — Build the wiki

Create the wiki folder first if it doesn't exist. If it already holds a wiki — a `CLAUDE.md` or
`AGENTS.md` with the four rules — this is a re-run, and the writes below are guarded one by one:
the rulebook and `index.md` are kept, `scan_interests.py` is replaced. Follow those guards where
they are written; where a step says "only if it does not exist", that beats the habit of
building the folder from scratch.

### 2a. Original version

1. Fetch the gist and read **all** its files:
   `https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959`
2. Follow its own "Getting started" instructions: create the folder tree, write `AGENTS.md`
   from `AGENTS.md.template` filled in for the user's field and 5–10 categories (propose them,
   let the user edit). **Only if `AGENTS.md` does not already exist** — an existing one carries
   the user's categories and their own added rules, and the template has neither.
3. `CLAUDE.md` should mirror `AGENTS.md`. On macOS/Linux: `ln -s AGENTS.md CLAUDE.md`. On
   Windows symlinks usually fail without developer mode — instead write a `CLAUDE.md`
   containing only: *"Read `AGENTS.md` and follow it. That file is the single source of truth."*
4. Skip the BM25 retrieval-index setup for now and tell the user it becomes worthwhile past
   ~500 pages (the gist says the same).

### 2b. Custom version

1. **Find a Python 3 launcher — do this before creating any files.** PDF extraction and
   `scan_interests.py` both need it, and if it turns out to be unavailable the fallback is the
   original version in Step 2a. Falling back after writing `CLAUDE.md` leaves a half-built custom
   wiki in the folder that then collides with 2a, so check first.

   Try `python3 --version`, `python --version`, and on Windows `py -3 --version`. Accept the
   first that prints **3.6 or newer** — parse both numbers, since `scan_interests.py` uses
   f-strings and a 3.5 launcher passes a major-version check and then dies on a syntax error:
   - Ubuntu and most Linux distributions ship Python as `python3` only — a bare `python` is
     often absent there, which is not the same as Python being absent.
   - Some systems still answer `python` with a 2.x version. `scan_interests.py` uses f-strings,
     so a 2.x launcher fails after setup rather than during it.
   - On Windows without Python, the Microsoft Store execution alias answers `python` with a store
     prompt and exit code 9009 — no version line, so it fails this check as it should.

   Call the winner `{PYTHON}`. It is substituted into the files written below, so the user's wiki
   ends up with the launcher that actually works on their machine, not a generic `python`.

   If none answers, ask to install Python and do it — the user has to approve the command, so
   just ask. Re-run the probe afterwards to learn `{PYTHON}`. If they cannot install at all,
   switch to the original version in Step 2a, which needs no Python.
2. Fetch `templates/CLAUDE-custom.md`, fill in `[YOUR FIELD]`, the category table (5–10
   categories proposed from the field, user-approved), and `{PYTHON}`, and save it as
   `{wiki}/CLAUDE.md` — **only if `{wiki}/CLAUDE.md` does not already exist.** On a re-run it
   does, and it holds the categories the user has been filing under plus whatever rules they
   added; the fresh template holds neither. Leave it and move on. (If they explicitly asked to
   reset the rulebook, show them what is about to be lost first.)

   One thing in a kept rulebook can still be wrong: the launcher baked into it. A re-run from a
   second machine — the case step 7 names — inherits the *first* machine's `{PYTHON}`, so a wiki
   set up on Windows says `py -3` inside a rulebook now being read on Ubuntu. If the launcher in
   the file is not the one the probe just found, edit those occurrences to `{PYTHON}` and leave
   the rest of the file alone. Same for `{wiki}/briefing/PROMPT.md` in step 3.3.
3. Create the folders: `papers/`, `papers/textbooks/`, `sources/`,
   `wiki/{each-category}/`, `wiki/overviews/`, `wiki/concepts/`, `wiki/seminars/`,
   `wiki/notes/`, `wiki/project-meetings/`, `wiki/routine-meetings/`, `wiki/textbook-study/`,
   `wiki/conversations/`, `wiki/other/`.
4. Fetch `templates/scan_interests.py` and save it as `{wiki}/scan_interests.py`. This one
   **does** get overwritten on a re-run — it is generated code with no user content, and picking
   up its fixes is the whole point of re-running after a template update.
5. Create an empty `index.md` with the category headings — **only if `index.md` does not already
   exist.** It is the page catalog: every ingest adds a line to it, so on a re-run "create an
   empty one" means deleting the table of contents for every paper in the wiki. If it exists but
   is missing headings for newly added categories, append those headings rather than rewriting
   the file.

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

   **If this file already exists, leave it alone.** Its manual queries and excluded topics are the
   user's, grown through use — rewriting it from the template deletes exactly the part that made
   their briefing fit. Check the AUTO markers are present, append the marker block if missing, and
   move on.
3. Fetch `templates/briefing-prompt.md`, fill `{CHANNEL}` with the chosen channel and
   `{DESTINATION}` with the address/channel/database (`n/a` for desktop), and save it as
   `{wiki}/briefing/PROMPT.md`. Custom version: also fill `{PYTHON}` with the launcher found in
   Step 2b. Original version: there is no scanner, so delete that clause of step 1 instead.
   Non-biomedical field (step 1.6): apply the prompt's "Fields PubMed does not cover" section
   while saving — swap step 2's URLs for the arXiv call, with the field's `cat:` filter filled
   in.

   Like `scan_interests.py`, this file **is** overwritten on a re-run — it holds no user content
   (the tuning lives in `interests.md`), and a refreshed prompt is the main thing a re-run
   delivers. Carry over the `{CHANNEL}` / `{DESTINATION}` / arXiv choices already in the old
   copy rather than asking again.
4. Fetch `templates/wiki-extras.md`, fill `{BRIEFING_TIME}`, and **append it** to the rulebook
   (`CLAUDE.md` for custom, `AGENTS.md` for original). This adds three things: the automatic
   ingest follow-up report, the briefing web-access exception, and the catch-up rule for
   missed briefings.

   The block is delimited by `<!-- SETUP-EXTRAS START -->` and `<!-- SETUP-EXTRAS END -->`. On a
   re-run, **replace what is between those markers with the freshly fetched version** — do not
   append a second copy, and do not leave the old one sitting there. This block is generated,
   so unlike the rest of the rulebook it is meant to be refreshed: a re-run that only edits the
   time leaves an existing wiki on an old copy of these rules, which is precisely how a wiki
   switched to arXiv ends up with a rulebook that still permits PubMed only, and a briefing that
   then refuses its own search.

   Wikis set up before this branch have the opening comment but no markers. There the block runs
   from that comment to the end of the file — replace that span, but read what is there first
   and carry over anything the user wrote themselves after it (their own rules, if any), placing
   it below the new `SETUP-EXTRAS END`.
5. If the channel needs a connector (email/Slack/Notion), walk the user through connecting it
   now, and record the destination (address / channel / database) inside `briefing/PROMPT.md`.
6. **Ask for the permissions the briefing needs, and ask now.** This settings file covers sessions
   the user opens in the wiki folder themselves ("브리핑 해줘", ingesting a PDF). What the
   *scheduled* runs do is governed by the task's own permission mode in step 7 — the two are
   separate, and this file alone will not make an unattended run silent. Put the question to the
   user in their own language, roughly:

   > 브리핑은 매일 아침 자리에 안 계실 때 도는 작업입니다. 그때 권한을 물어보면 아무도 답하지
   > 않아 그대로 멈추고, 파일도 알림도 남지 않습니다. **이 위키 폴더 안에서** 파일을 읽고 쓰고,
   > 논문 검색을 하고, `scan_interests.py`를 돌릴 권한을 미리 열어둘까요? 이 폴더에서만
   > 적용되고, 다른 작업에는 영향이 없습니다.

   On yes, write `{wiki}/.claude/settings.json` — **or merge into it, if it already exists.**
   Read it first and add only the missing `permissions.allow` entries, keeping every other key
   as it is. That file is not necessarily yours: it may carry the user's own `deny` rules, hooks,
   or connector permissions, and a re-run that replaces it wholesale deletes those — including
   restrictions, which is the one direction a permissions file must never move by accident. If
   the existing file already grants what the briefing needs, say so and write nothing.

   ```json
   {
     "permissions": {
       "defaultMode": "acceptEdits",
       "allow": [
         "Bash",
         "PowerShell",
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

   **Include `PowerShell`, not just `Bash`.** On Windows the briefing's PubMed work runs through
   the PowerShell tool, so a `Bash`-only list leaves it prompting.

   **Grant each tool as a whole, not command patterns.** Rules like `Bash(curl *)` look tidier and
   do not work: the briefing builds compound commands and pipelines, and a rule has to match every
   subcommand independently, so a pattern list halts some mornings and not others.

   **What this scopes, and what it doesn't.** The file only decides which tool calls skip the
   prompt while working in this folder — no other folder's sessions are affected. It is not a
   sandbox: an approved `Bash` or `PowerShell` call can still reach any path the user's account
   can. Say that plainly rather than implying the grant confines Claude to the wiki.

   **Let the approval prompt happen, and warn the user it is coming.** A settings file that grants
   `Bash` is the agent widening its own permissions, so this write — alone among the writes in
   this setup — is supposed to stop and ask. Do not try to slip it past: no shell redirect, no
   rewriting it in a different shape, no other tool. Say what is about to appear and what
   approving it means, then write the file and let them press the button:

   > 방금 여쭤본 권한을 `{위키}/.claude/settings.json`에 적겠습니다. 이 파일을 쓰려고 하면
   > 승인 창이 한 번 뜹니다 — 제가 제 권한을 넓히는 동작이라 자동으로는 통과되지 않게 돼
   > 있어서요. 내용은 방금 설명드린 그대로고, 승인해 주시면 그대로 저장됩니다.

   If the classifier refuses outright instead of prompting, stop there rather than looking for a
   way around it: show them the JSON and the path and let them paste it themselves. Either way
   the briefing does not depend on this file — the task's own permission mode in step 7 does that
   job — so do not stall the setup over it.

   If the chosen channel is email/Slack/Notion, add that connector's tool to the list too.

7. Create a **scheduled task** (Claude Desktop scheduled-tasks feature): **recurring, daily** at
   the chosen time, working directory = **the wiki folder itself**, instruction:
   *"Open briefing/PROMPT.md in this folder and follow it."*

   First check whether a briefing task already exists (`list_scheduled_tasks`) and reuse it.
   Setup gets re-run — from a second machine, or after a template update — and a second daily
   task means two briefings every morning, each unaware of the other's file.

   - **You can create the task, but you cannot finish it. Hand the last two settings to the
     user and watch them do it.** The scheduled-task tool takes an id, a prompt, a description
     and a schedule — **the folder and the permission mode are not among its parameters**, and
     they are not in the task's `SKILL.md` either. The official docs say the same: *"Schedule,
     folder, model, and enabled state are not in this file: change them through the Edit form."*
     These two are exactly the settings step 9 lists as the causes of a stalling briefing, so a
     task you create and never hand over is a task that stops on its first shell command.

     Say so plainly rather than reporting the routine as done: *"루틴은 만들어 뒀는데, 폴더와
     권한 모드 두 가지는 제가 못 바꿉니다. 사이드바 **루틴** → 브리핑 → **편집**을 열어
     주시면 어디를 눌러야 하는지 짚어 드릴게요."* Then walk them through it and confirm what
     they see before moving on. A folder has to be picked before the form will save, and if
     that folder has never been trusted, Desktop asks them to trust it first — tell them that
     prompt is expected.
   - **Set the task's permission mode to 자동 (auto)** in the same form, next to the model picker.
     This is what makes unattended runs actually run. In Manual or 편집 자동 수락 the task stops at
     a permission prompt on every shell command, and step 9 explains why the other workarounds
     don't hold. Auto mode isn't a bypass: a classifier vets each action in the background and
     blocks the dangerous ones. If the picker doesn't offer 자동, this account or model can't use
     it. Do not quietly settle for 편집 자동 수락 — that task stops at the first shell command and
     cannot pass step 8. Tell the user the unattended briefing isn't available on this account,
     leave the task in place as a reminder if they want it, and make "브리핑 해줘" on demand the
     real mode.
   - **Recurring, not one-shot — including when you are only testing.** A one-shot task disables
     itself the moment it fires, and its session goes with it — the user reads the notification,
     looks at something else, comes back, and cannot find the briefing conversation again. A
     recurring task stays in the sidebar, so the conversation is still there tomorrow. This holds
     for test runs too: a one-shot needs its own run-once-only configuration, which you then throw
     away along with it. Register the daily task and test *that*.
   - If your environment has no scheduled-task capability (e.g. plain CLI), say so and tell
     the user the schedule needs the Claude Desktop app; meanwhile "브리핑 해줘" runs it on
     demand.

8. **Run it once with the user watching**, using **Run now** (지금 실행) on the task's detail page,
   and check that it asked for nothing, wrote `briefings/{today}.md`, printed the briefing in the
   session, and fired the notification. A schedule that has never completed once is not set up, it
   is only scheduled. If it does prompt, fix it here — step 9 lists what to check.

9. **When a scheduled run keeps prompting**, work through these in order. Every one of them was a
   real cause on a real setup.
   - **The task's permission mode is not 자동.** This is the fix; the rest are refinements. Set it
     in the task's Edit form, not in the session's mode selector — the selector applies to that one
     session, so a mode set there looks fixed and is back to Manual tomorrow.
   - **The task's folder is a parent of the wiki**, not the wiki itself. Then every command needs a
     `cd …;` prefix, which makes it compound, and compound commands can't be pre-approved.
   - **Do not lean on "항상 허용" for this workload.** It saves the command string verbatim, and the
     briefing's commands carry a per-run scratchpad path and the day's PubMed query inside the URL.
     Tomorrow's command is a different string, so the list grows by half a dozen entries a day and
     never covers the next run.
   - **Do not tell the user to click 권한 무시 daily.** It disables the safety checks entirely and
     the docs reserve it for containers and VMs.
   - Reference: <https://code.claude.com/docs/en/desktop-scheduled-tasks#permissions-for-scheduled-tasks>.

   Tell the user what the routine actually does: it scans the wiki folder, queries the literature
   API named in `briefing/PROMPT.md` (PubMed, or arXiv for fields PubMed does not cover), and
   writes `briefings/{date}.md`. The only thing it sends out is that search — plus the briefing
   itself, if they chose email, Slack, or Notion. Wiki files are never uploaded anywhere.

10. Tell the user plainly: the app must be open at briefing time, and the run can start a few
    minutes late rather than on the dot.

    **Say the word "sleep" out loud.** "The app is open" is not the condition — a sleeping
    machine skips the run outright, and for a 09:00 briefing on a laptop that closed the night
    before, sleep is the likeliest reason a morning comes up empty. Point them at
    **설정 → 데스크탑 앱 → 일반 → 컴퓨터 깨어 있게 유지**. Closing the lid still sleeps it.

    Missed runs are then covered twice, and it is worth naming both so nobody waits on the wrong
    one. Desktop itself starts **one** catch-up run on wake for the most recent missed time
    (older ones are discarded, and it looks back seven days). The rulebook's catch-up rule is the
    backstop for what that misses, and it no-ops when today's `briefings/` file already exists.

    If they want a briefing that lands whether or not the machine is on, mention that a **cloud
    routine** runs server-side — but only as a pointer, not as part of this setup: it gets a
    fresh clone rather than their wiki folder, so the interest profile and `briefings/` archive
    would need somewhere else to live.

## Step 4 — Korean humanizer skill

Only relevant if the user writes Korean. Skip the whole step otherwise.

### 4a. Install

**Skip the whole step if `~/.claude/skills/humanizer` already exists** (previous run, or the
user installed it themselves). This is not just to save time: `cp -r` onto an existing folder
does not fail or overwrite — it nests a second copy *inside*, leaving
`humanizer/humanizer/` behind, silently.

```bash
mkdir -p ~/.claude/skills
rm -rf /tmp/korean-skills
git clone --depth 1 https://github.com/DaleSeo/korean-skills /tmp/korean-skills
cp -r /tmp/korean-skills/skills/humanizer ~/.claude/skills/humanizer
```

Windows equivalent — `/tmp` does not exist, so clone somewhere real:

```bash
mkdir -p "$USERPROFILE/.claude/skills"
rm -rf "$TEMP/korean-skills"
git clone --depth 1 https://github.com/DaleSeo/korean-skills "$TEMP/korean-skills"
cp -r "$TEMP/korean-skills/skills/humanizer" "$USERPROFILE/.claude/skills/humanizer"
```

**Do not drop the `mkdir -p`.** On a machine that has never installed a skill, `~/.claude`
exists but `~/.claude/skills` does not, and `cp -r` will not create a missing parent — it fails
with `cp: cannot create directory …: No such file or directory` and the step reads as a broken
repository URL rather than a missing folder.

**Do not drop the `rm -rf` either.** `/tmp` survives until reboot and `%TEMP%` effectively
forever, so on any re-run the last clone is still sitting there and `git clone` dies with
`fatal: destination path … already exists and is not an empty directory`.

No git? Fetch the files under `skills/humanizer/` from the GitHub API instead.

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
if granted · scheduled task registered **as recurring**, pointed at the wiki folder, and **run
once successfully** via Run now **with no permission prompt at all** · humanizer
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
- **Routine permissions**: one-time setup, not a daily chore. Show them the task's detail page and
  name the three things to check if a morning ever comes up empty: the permission mode is 자동
  (set in the Edit form, not the session selector), the folder is the wiki folder, and **지금 실행**
  runs it on demand. A run that stops to ask means one of the first two slipped. Say plainly that
  you already wrote the settings file for them and they never need to edit JSON.
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
