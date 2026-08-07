# 패치노트

이 저장소의 변경 이력입니다. 최신순.

날짜·시간은 커밋 시각(KST)입니다. 커밋 해시를 누르면 실제 변경 내용을 볼 수 있습니다.

## 2026-08-07

| 시간 | 커밋 | 주요 변경사항 |
|---|---|---|
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
