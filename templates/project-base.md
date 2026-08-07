# Project Base — optional module

A home for a research project's *working* content — README, plans, code, data locations —
separate from the llm-wiki. Boundary, stated to the user in one line: **the wiki holds what you
learned (papers, seminar/meeting notes); the project base holds the work itself.**

This is a **post-setup module**: it is not part of the initial wiki setup. Run it whenever the
user asks — "프로젝트 베이스 만들어줘", "이 프로젝트 관리 좀 도와줘", or similar — and let them
choose GitHub or Notion then.

## Why (tell the user, in their language)

- **Agent handoff.** When a conversation runs long or they want another agent to take over:
  "이 프로젝트의 전체 맥락을 README에 정리해서 저장해줘" — then the new agent needs only the
  link. No re-explaining the background.
- **Effortless file/version management.**
- **Showing others later.** A clean README doubles as the explanation. For sensitive or
  unpublished research, recommend **private** — and make sure they know: private/public can be
  toggled anytime, and private does not mean alone — designated collaborators can be invited.

## GitHub path

1. For non-git users, explain GitHub in one plain sentence: *an online project folder that
   keeps every past version, which both you and AI agents can read and write.*
2. Check `gh auth status`; if not set up, walk them through account creation and
   `gh auth login` (browser flow).
3. Ask the project name; create a **private** repo by default (see privacy note above).
4. Scaffold `README.md`: project background, goal, current status, data locations, how to run.
5. Create a `CLAUDE.md` in the project folder (or append if one exists):

   ```markdown
   ## Git convention
   When the user says "git에 저장해줘", "git에 업데이트해줘", "save this to git", or similar,
   that means: stage the relevant changes, commit with a concise message describing what
   changed, and push. Never force-push. If the remote has new commits, pull/rebase first and
   report any conflict instead of overwriting.

   ## Handoff
   When asked to prepare a handoff, rewrite README.md so a new agent (or person) can pick the
   project up from the README alone, then commit and push.
   ```

6. **Copyright warning.** Publisher PDFs must never go into a public repo. This also applies if
   the user ever wants the llm-wiki itself on GitHub: papers/ makes it private-only.

## Notion path

1. Connect the Notion MCP connector if not already connected.
2. Create a project home page with the same content as the GitHub README: background, goal,
   current status, data locations.
3. Same handoff convention: "프로젝트 내용 정리해서 Notion에 저장해줘" updates the page; the
   page link is the handoff token.
4. The two big later advantages — mention them, build only if asked:
   - **To-do tracker**: a Notion database the agent reads and updates ("이번 주 할일에
     추가해줘", "끝난 것 체크해줘"). Build it from this proven template (the author's own
     "[kobic] 우선순위 트래커") — a single database, suggested name "[{lab}] 우선순위 트래커":

     | Property | Type | Notes |
     |---|---|---|
     | `task` | Title | one actionable item per row |
     | `project` | Select | one colored option per active project (e.g. STR, splicing, Kinship) plus `life` / `career` for non-research tasks |
     | `Status` | Status | Not started / In progress / Done. The Notion API may refuse to create a status-type property — fall back to a Select with the same three options |
     | `Progress %` | Number | 0–100, optional per task |
     | `Due` | Date | this is what Notion Calendar picks up |
     | `Notes` | Rich text | progress notes, blockers, who you're waiting on |

     The API cannot create views. After creating the database, tell the user to add these in
     the Notion UI (takes a minute): **By status** (board grouped by Status), **Calendar**
     (by Due), **Timeline**, plus the default Table. Then teach the conventions:
     "○○ 할일 추가해줘 (project: splicing, due 금요일)" / "끝난 걸로 체크해줘" /
     "이번 주 남은 할일 보여줘".
   - **Notion Calendar**: any database with a date property shows up in Notion Calendar, so
     deadlines the agent writes into the tracker become calendar entries automatically.

## Handoff (both paths)

Teach the user this loop during the tour:

1. Before ending a long conversation: "지금까지의 프로젝트 맥락을 전부 README(프로젝트 페이지)에
   정리해서 저장해줘".
2. To resume anywhere, with any agent: give the repo/page link and say "이 프로젝트 이어서 하자".
