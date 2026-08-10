# 패치노트

이 저장소의 변경 이력입니다. 최신순.

날짜·시간은 커밋 시각(KST)입니다. 커밋 해시를 누르면 실제 변경 내용을 볼 수 있습니다.

## 2026-08-10

| 시간 | 커밋 | 주요 변경사항 |
|---|---|---|
| 14:33 | [`8cc4c6d`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/8cc4c6d) | **MIT 라이선스 추가.** 라이선스 파일이 없으면 기본값이 저작권 전부 보유라, 템플릿을 가져다 쓰라는 저장소와 안 맞았습니다. 그리고 `.claude/settings.json`은 **승인 창을 띄우고 사용자가 승인하는** 방식으로 바꿨습니다 — 에이전트가 제 권한을 넓히는 동작이라 원래 한 번 멈춰 묻게 돼 있습니다. 어떤 창이 왜 뜨는지 미리 말해주고 쓰며, 아예 거부당하면 그때만 JSON을 보여드리고 직접 붙여넣게 합니다 |
| 14:33 | [`4c881dc`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/4c881dc) | **`briefing/interests.md`가 UTF-16으로 저장돼 있으면 수동 검색어가 통째로 깨지던 문제.** 앞 커밋의 `utf-8-sig`는 UTF-8 BOM만 처리하는데, 순정 PowerShell 5.1의 `Out-File`은 UTF-16LE로 씁니다. 그러면 파일이 NUL과 깨진 글자로 읽히고 AUTO 표식을 못 찾은 채 **그 상태로 다시 저장**됩니다 — 재현해 보니 NUL 835개에 `## Manual queries` 제목과 시드 검색어가 전부 날아가고 AUTO 블록만 하나 더 붙었는데, 화면에는 `[ok]`가 찍혔습니다. 이제 BOM을 보고 인코딩을 정하고, 그래도 NUL이 남으면 아예 안 씁니다. UTF-8·UTF-8+BOM·UTF-16LE·cp949 네 가지로 확인했습니다 |
| 14:21 | [`a1f3a1c`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/a1f3a1c) | **처음 세팅에서 실제로 걸린 세 곳.** 루틴은 만들어져도 폴더와 권한 모드는 Claude가 못 바꿉니다 — 예약 도구의 인자에 아예 없어서 사용자가 편집 폼에서 직접 눌러야 하는데, 그동안 문서는 Claude가 다 해주는 것처럼 읽혔습니다. humanizer 설치는 `~/.claude/skills`가 없는 새 컴퓨터에서 `cp -r`이 그대로 죽습니다(`mkdir -p` 추가). 그리고 **잠자기** — 앱이 켜져 있어도 컴퓨터가 자고 있으면 그날 브리핑은 건너뜁니다. 세팅을 다시 돌릴 때 루틴이 두 개 생기던 것도 막았습니다 |
| 14:21 | [`bb29dac`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/bb29dac) | **PubMed 검색어를 제목·초록(`[tiab]`)으로 좁힙니다.** 문서가 나쁜 예로 든 `forensic genetics`는 7일에 13건이라 150건 기준에 안 걸리는데, 그 13건에 폐고혈압·장내미생물·뇌허혈 논문이 섞여 나옵니다 — 저자 소속의 "Department of Forensic Medicine"까지 매칭되는 탓입니다. 건수로는 잡히지 않는 문제라 `[tiab]`로 바꿨고, 30일 기준 `degraded dna`가 1349건에서 17건으로 줄면서 좋은 검색어인 `Y-STR haplotype population`은 1건 그대로입니다. 0건인 주제는 `reldate=30`으로 한 번 더 봅니다 — 좁은 분야는 7일에 정말 아무것도 없습니다 |
| 14:20 | [`af65065`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/af65065) | **BOM 붙은 위키 페이지가 관심사 집계에서 통째로 빠지던 문제.** 메모장이나 PowerShell `-Encoding utf8`로 저장하면 파일 맨 앞에 BOM이 붙고, 그러면 frontmatter 인식이 실패해 그 페이지의 태그가 전부 사라집니다 — 오류 한 줄 없이 조용히. 5개 중 4개만 스캔되던 걸 확인하고 `utf-8-sig`로 고쳤습니다 |

## 2026-08-07

| 시간 | 커밋 | 주요 변경사항 |
|---|---|---|
| 21:36 | [`07621af`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/07621af) | 리뷰 지적 세 건 반영. Python은 3.6 이상만 받습니다 — 3.5도 "3으로 시작"이라 통과한 뒤 f-string에서 죽습니다. 계정이 **자동** 모드를 못 쓰면 "편집 자동 수락"으로 물러서지 않고, 무인 브리핑이 불가능하다고 알린 뒤 "브리핑 해줘"를 기본으로 안내합니다 — 물러서봐야 첫 셸 명령에서 멈추니까요. 그리고 명령 작성 규칙의 예시에서 Python 전용 표현을 뺐습니다 (원본판은 Python이 없을 수 있음) |
| 21:25 | [`dd423b5`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/dd423b5) | 문구 세 곳 정리. 성공 기준을 **"자동 모드 + 지금 실행에서 아무것도 묻지 않고 완료"** 하나로 통일했습니다 — 앞선 커밋에 "처음엔 항상 허용을 누르라"와 "항상 허용에 기대지 말라"가 같이 남아 있었습니다. 그리고 "아무것도 밖으로 나가지 않는다"는 PubMed 조회와 이메일·Slack 전달을 빼먹은 말이라 범위를 좁혔고, 폴더 설정이 파일 접근을 폴더 안으로 가두는 샌드박스가 아니라는 점도 명시했습니다 |
| 21:12 | [`c1f1994`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/c1f1994) | **루틴 권한의 진짜 해법은 권한 모드를 `자동`으로 두는 것이었습니다.** 폴더의 `.claude/settings.json`은 직접 여는 세션에만 걸리고 예약 실행에는 안 걸립니다. "항상 허용"도 답이 아니었습니다 — 명령 문자열을 통째로 저장하는데 브리핑 명령에는 매번 바뀌는 임시 폴더 경로와 그날의 검색어가 박혀 있어서, 규칙만 하루에 여섯 개씩 쌓이고 다음 실행은 또 묻습니다. 이제 세팅할 때 루틴의 권한 모드를 자동으로 잡고, README에는 확인할 세 가지(권한 모드 자동 · 폴더가 위키 폴더 · 지금 실행)만 남겼습니다. 설정 파일은 Claude가 알아서 씁니다 |
| 20:37 | [`34e2e8c`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/34e2e8c) | **브리핑이 승인 가능한 형태로만 명령을 짭니다.** 힙독(`cat > x.py <<EOF`)으로 스크립트를 쓰면 명령 하나가 통째로 길어져 어떤 허용 규칙에도 안 걸리고, 따옴표를 품은 중괄호 `{"a","b"}`는 셸 보안 검사에 걸려 허용 목록과 무관하게 매번 물어봅니다. 이제 스크립트는 Write 도구로 만들고 `python x.py`로 따로 실행하며, `cd … &&` 접두사도 쓰지 않습니다 |
| 20:28 | [`8fbdcfd`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/8fbdcfd) | **Windows에서 권한 목록에 `PowerShell`을 넣습니다.** `Bash`만 열어두면 PubMed 검색 루프가 매번 권한을 묻습니다 — Windows에서 그 루프는 PowerShell 도구로 돌기 때문입니다. 여러 줄 스크립트라 "항상 허용"도 안 뜨고 "한 번만 허용"만 나옵니다 |
| 20:12 | [`5c701d0`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/5c701d0) | **루틴 권한은 처음 한 번만 잡으면 됩니다.** 매일 "권한 무시"를 누르라고 적었던 앞 커밋을 뒤집었습니다. 공식 문서대로 상세 페이지에서 **지금 실행**을 누르고 프롬프트마다 **항상 허용**을 고르면 다음 실행부터 안 묻습니다. 매번 묻던 진짜 원인은 루틴의 **폴더가 위키 폴더가 아니라 상위 폴더**였던 것 — 그러면 위키의 `.claude/settings.json`이 안 읽히고 명령마다 `cd`가 붙어 복합 명령이 되는 탓에 "항상 허용" 선택지 자체가 안 뜹니다 |
| 19:41 | [`9e1281d`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/9e1281d) | **루틴은 매일 "권한 무시"를 한 번 눌러야 합니다.** 루틴이 매일 새 대화창에서 도는 탓에 어제 준 허락이 오늘로 이어지지 않아서, 폴더 권한을 미리 열어둬도 그날 대화창에서 한 번은 눌러줘야 합니다. 누르는 곳은 **세팅을 시킨 대화창이 아니라 루틴 대화창** — 사이드바 *루틴*에서 브리핑 항목을 열고 입력창 왼쪽 아래를 누릅니다. 스크린샷 두 장과 함께 README에 넣고, 세팅 중에 이걸 안내하는 단계를 SETUP에 추가했습니다. 시험용 루틴도 일회성 대신 **매일 반복**으로 — 일회성은 그것만을 위한 설정을 따로 해야 하고, 한 번 돌면 대화창째 사라집니다 |
| 19:46 | [`5495c53`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/5495c53) | **Python 찾는 방법을 고쳤습니다.** `python`만 확인해서 우분투처럼 `python3`로만 깔린 환경을 "Python 없음"으로 잘못 판정했고, 반대로 2.x가 응답하면 통과시켜 세팅이 끝난 뒤에 깨졌습니다. 이제 `python3`·`python`·`py -3`을 차례로 보고 3으로 시작하는 버전만 받습니다. 확인도 파일을 만들기 **전에** 합니다 — 그전엔 `CLAUDE.md`를 이미 쓴 뒤라 원본판으로 돌아가면 반쯤 만들어진 확장판이 남아 충돌했습니다. 찾은 실행기 이름은 위키의 `CLAUDE.md`와 브리핑 프롬프트에 실제로 박아 넣습니다 |
| 19:01 | [`8a9a088`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/8a9a088) | **Python을 세팅에서 먼저 확인합니다.** 그전엔 있다고 치고 넘어가서, 없는 사람은 첫 논문을 넣을 때 `pip3 install pypdf`에서 처음 막혔습니다. 이제 세팅 중에 확인하고 없으면 물어본 뒤 깔아 줍니다. Windows에서는 버전이 실제로 찍혀야 통과로 봅니다 — Python이 없어도 스토어 별칭이 `python`에 응답하기 때문입니다. 논문 넣기 예제의 `pip3`·`python3`도 확인된 실행기를 쓰도록 고쳤습니다 |
| 18:50 | [`af9493e`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/af9493e) | **세팅할 때 브리핑 권한을 물어봅니다.** 무인 실행 중 권한을 물으면 아무도 답하지 않아 그대로 멈춥니다. 이제 "이 폴더 안에서 파일 읽기·쓰기, PubMed 검색, 스크립트 실행 권한을 미리 열까요?"를 세팅 중에 묻고, 허락하면 `Bash`를 통째로 엽니다 — `Bash(curl *)` 같은 패턴은 복합 명령을 파서가 못 읽어서 결국 물어봅니다. 예약도 일회성이 아니라 반복으로 만들어 대화가 사이드바에 남습니다 |
| 18:43 | [`1814a07`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/1814a07) | **브리핑을 표가 아니라 글로 씁니다.** 필수 항목을 표로 적어놨더니 그대로 라벨 붙은 불릿으로 나와서 읽기가 딱딱했습니다. 이제 제목 아래 저널·날짜·링크 한 줄, 그다음 "어떤 논문인가"와 "왜 골랐나"를 짧은 문단 두 개로 씁니다 |
| 18:19 | [`bd8e326`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/bd8e326) | **브리핑이 권한 프롬프트에서 멈추던 문제.** 예약 실행은 자리를 비운 사이에 도는데 권한을 물으면 아무도 답하지 않아 그대로 멈췄습니다 — 파일도 안 쓰고 알림도 안 가고 이유도 안 남습니다. 이제 세팅 중에 `{위키}/.claude/settings.json`으로 필요한 도구를 미리 허용하고, 사용자가 보는 앞에서 한 번 돌려 성공을 확인합니다 |
| 17:50 | [`4912357`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/4912357) | **브리핑 본문을 대화창에도 보여줍니다.** 그전엔 데스크탑 알림을 고르면 본문이 md 파일에만 남아서, 알림을 눌러 들어가도 "파일 썼습니다"만 있었습니다. 이제 알림은 신호이고 본문은 응답에 그대로 나옵니다. `briefings/{날짜}.md`는 보관용이라는 원칙을 네 가지 수신 방법 전체에 적용했습니다 |
| 17:42 | [`539b954`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/539b954) | **humanizer를 항상 켤지, 어디까지 켤지 물어봅니다.** 그전엔 스킬을 설치만 해서, 부르지 않으면 아무 일도 안 일어났습니다. 이제 모든 대화(권장) / 이 위키에서만 / 부를 때만 중에 고르고, 고른 위치의 `CLAUDE.md`에 규칙이 들어갑니다. 항상 켜도 매번 무거운 분석을 돌리는 게 아니라 **한국어를 쓸 때 그 패턴들을 피해 쓰는 기본값**입니다. README 스크린샷도 폭 800에 설명문 뒤로 옮기고 alt 텍스트를 채웠습니다 |
| 17:33 | [`65cdcf6`+`ae58857`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/compare/0203cb7...ae58857) | 브리핑이 Claude의 **루틴** 기능으로 돌아간다는 점을 README에 명시. 사이드바 *루틴*에서 직접 시간을 바꾸거나 꺼둘 수 있다는 것, 그리고 앱이 켜져 있어야 도는 이유까지 |
| 17:26 | [`b56a7ac`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/b56a7ac) | 브리핑이 최종 5편의 **초록을 읽고** 논문 설명을 씁니다. 그전엔 제목만 보고 추측했습니다. 스크리닝은 제목으로만 해서 속도는 그대로. 그리고 실행 로그(스캔 수, 검색 파라미터, 주제별 히트 수)를 브리핑 본문에서 **뺐습니다** — 너무 넓어 건너뛴 주제와 0건인 주제만 맨 아래 한 줄로 남깁니다 |
| 17:13 | [`2f4e59f`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/2f4e59f) | 브리핑에 무엇이 들어가야 하는지 명시. 논문마다 영문 제목·저널·날짜·PubMed 링크·**무슨 논문인지**·**왜 골랐는지**, 그리고 마지막에 **전체 총평** 3~5줄 |
| 17:11 | [`74bb504`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/74bb504) | 브리핑 본문을 **사용자 언어로** 씁니다. 위키의 영어 전용 규칙은 `sources/`와 `wiki/`에만 적용되고, 브리핑은 사람이 읽는 글이라 별개입니다. 논문 제목과 저널명은 영문 그대로 |
| 16:54 | [`f87eb37`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/f87eb37) | 뉴스 기사 가중치를 0.3으로. 그전엔 뉴스도 논문과 같은 1.5라, 기사 한 편이 논문급으로 관심사를 밀어올렸습니다 |
| 16:41 | [`71120f3`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/71120f3) | **브리핑 정확도 개선.** 검색어를 분야명이 아닌 2~3단어 구문으로 받고, 주제당 최신 4편만(`sort=date`), 3일 안에 150건 넘는 주제는 검색어가 아니라 분야명이므로 건너뛰기. `## Excluded topics` 추가 — "그건 추천하지 마"가 영구 반영됩니다 |
| 16:41 | [`25e6361`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/25e6361) | **세팅을 막는 버그 2개 수정.** (1) 블록형 YAML 태그가 조용히 무시돼 해당 페이지가 관심사 집계에서 통째로 빠지던 문제 (2) 한글 Windows에서 PDF 텍스트 추출이 cp949 인코딩 오류로 죽던 문제 |
| 14:07 | [`7fd12c8`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/7fd12c8) | 프로젝트 베이스 모듈 추가. 세팅 후 언제든 "프로젝트 베이스 만들어줘"로 GitHub 저장소나 Notion 페이지를 잡습니다 |
| 13:59 | [`b916a96`](https://github.com/ehojune/llm-agent-tutorial-for-researchers/commit/b916a96) | 최초 공개. LLM Wiki + 데일리 논문 브리핑 한 줄 세팅 |

---

## 읽는 법

- **16:41의 버그 2개**는 새로 세팅하는 사람만 밟습니다. 이미 쓰고 계신 위키에는 영향이 없습니다.
- **16:41 이후의 변경은 전부 브리핑 품질** 이야기입니다. 세팅 절차 자체는 그대로입니다.
- 이미 세팅을 마치셨다면, 브리핑 개선을 받으려면
  [`templates/briefing-prompt.md`](../templates/briefing-prompt.md)를 다시 받아
  `{위키폴더}/briefing/PROMPT.md`로 덮어쓰면 됩니다. Claude에게 "브리핑 프롬프트 최신으로
  업데이트해줘"라고 해도 됩니다.
- **8-10의 인코딩 문제는 쓰던 위키에도 해당됩니다.**
  [`templates/scan_interests.py`](../templates/scan_interests.py)를 새로 받아
  `{위키폴더}/scan_interests.py`를 덮어쓰세요. 위키 페이지를 메모장으로 열어 저장한 적이
  있다면 그 페이지가 관심사에서 빠져 있을지 모르고, `briefing/interests.md`를 PowerShell로
  저장한 적이 있다면 다음 스캔에서 수동 검색어가 날아갑니다. 이미 깨져 있다면 그 파일만
  UTF-8로 다시 저장하시면 됩니다.
