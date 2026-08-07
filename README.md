# 연구자를 위한 LLM 에이전트 튜토리얼

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-D97757?logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![패치노트](https://img.shields.io/badge/%ED%8C%A8%EC%B9%98%EB%85%B8%ED%8A%B8-changelog-5B5BD6)](patch_notes/README.md)

논문 PDF를 개인 지식베이스(LLM Wiki)로 쌓고, 매일 정해진 시간에 관심사 기반 최신 논문
브리핑까지 받는 세팅을 Claude에게 한 줄로 맡기는 튜토리얼입니다.

바뀐 내용은 [패치노트](patch_notes/README.md)에서 확인하세요.

## 사용법 — 이게 전부입니다

[Claude Desktop](https://claude.com/download)을 설치하고, 새 대화에 아래를 붙여넣으세요.

```
https://github.com/ehojune/llm-agent-tutorial-for-researchers
나도 이거 세팅해줘
```

Claude가 이 저장소를 읽고 몇 가지를 물어본 뒤(연구 분야, 위키 버전, 브리핑 시간과 수신
방법) 폴더 생성부터 매일 브리핑 예약까지 알아서 끝냅니다. 위키 폴더를 따로 정하지 않으면
홈 폴더에 `llm-wiki`를 만들어 줍니다.

확장판은 Python이 필요합니다. 없으면 Claude가 세팅 중에 설치해도 되는지 물어보고, 허락하면
알아서 깔아 줍니다.

## 뭐가 세팅되나

1. **LLM Wiki** — `논문 PDF → 요약(sources/) → 위키 페이지(wiki/)` 3단 구조의 개인
   지식베이스. 모든 답이 "실제로 갖고 있는 논문"에 근거하도록 강제하는 4대 규칙(웹 검색
   금지 등)이 핵심입니다. PDF를 주고 "ingest 해줘" 하면 등록 + 요약 + 기존 논문과의 연결
   보고까지 한 번에 해줍니다.
2. **데일리 논문 브리핑** — 관심사를 바탕으로 매일 정해진 시간에 PubMed 최신 논문을 훑어
   브리핑합니다. Claude의 **루틴** 기능으로 돌아갑니다 — 세팅할 때 Claude가 루틴을 대신
   등록해 주고, 그 뒤로는 사이드바의 *루틴*에서 시간을 바꾸거나 잠시 꺼둘 수 있습니다. 수신
   방법은 데스크탑 알림(기본, 설정 불필요), 이메일, Slack, Notion 중 선택. 루틴은 **앱이 켜져
   있을 때** 돌기 때문에, 브리핑 시간에 컴퓨터가 꺼져 있었다면 다음에 위키 폴더에서 Claude를
   열었을 때 밀린 브리핑을 잡아서 해줍니다.
3. **한국어 humanizer 스킬** — [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills)의
   `humanizer`를 함께 설치합니다. AI가 쓴 한국어 특유의 패턴 40가지(쉼표 과다, 번역투 등)를
   찾아 자연스럽게 고쳐주는 스킬입니다. 설치 중에 **항상 적용할지, 어디까지 적용할지** 물어봅니다
   — 모든 대화에 적용(권장), 이 위키에서만, 아니면 부를 때만. 항상 적용을 골라도 매번 무거운
   분석을 돌리는 게 아니라 **한국어를 쓸 때 그 패턴들을 피해서 쓰는 기본값**이 되는 것이고,
   기존 글을 고칠 땐 "자연스럽게 해줘" 하면 전체 분석·재작성이 돕니다.

### 루틴 권한은 처음 한 번만

브리핑은 자리에 없을 때 도는 작업이라, 도중에 권한을 물으면 아무도 답하지 않아 그대로 멈춥니다.
설정 파일은 Claude가 알아서 넣어주니, 사용자가 볼 곳은 사이드바 **루틴** → 브리핑 → 상세
페이지 세 가지뿐입니다.

<img width="420" alt="루틴 상세 페이지 — 지금 실행 버튼, 폴더, 항상 허용됨 목록" src="images/routine-detail-page.png" />

1. **권한 모드가 `자동`인지.** 연필(편집)을 눌러 지침 입력창 옆 선택기에서 정합니다. 이게
   핵심입니다 — `수동`이나 `편집 자동 수락`이면 셸 명령마다 멈춰 섭니다. 자동은 안전장치를 끄는
   게 아니라, 사람 대신 분류기가 매 동작을 검사하고 위험한 것만 막는 모드입니다. 입력창 옆
   선택기에서 바꾸면 그 세션에만 걸리니, 반드시 **편집 폼**에서 바꾸세요.
2. **폴더가 위키 폴더인지.** 상위 폴더로 잡혀 있으면 명령마다 `cd`가 붙어 복합 명령이 되고,
   그러면 미리 허용해둘 방법이 없어 계속 물어봅니다.
3. **"지금 실행"으로 한 번 돌려보기.** 아무것도 묻지 않고 브리핑이 나오면 끝입니다. 중간에
   권한 창이 뜬다면 1·2번이 제대로 잡히지 않은 것이니, 그 창은 넘기고 다시 확인하세요.

**권한 무시**는 안전장치를 통째로 끄는 모드입니다. 매일 켜는 습관은 들이지 마세요.

## 두 가지 버전

세팅 중에 Claude가 물어봅니다.

| | 원본 (안준용 교수) | 확장판 (이호준) |
|---|---|---|
| 초점 | 논문 지식베이스 그 자체 | 논문 + 연구 생활 전반 |
| 논문 외 자료 | wiki 밖에 격리 (`materials/`, `agenda/`) | 세미나 노트, 프로젝트 미팅, 교과서 스터디, 질문 노트를 wiki에 정식 등록 |
| 브리핑 관심사 | 직접 적은 시드 키워드 | 위키 태그에서 자동 집계 (`scan_interests.py`) + 수동 키워드 |
| 규모 | 수만 편 운영으로 다듬어진 정식 시스템 (로그, 검증기, BM25 검색) | 가볍게 시작하는 개인용 |

원본: [joonan30 gist](https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959) ·
확장판 템플릿: [templates/](templates/)

## 세팅 후 추천 — 프로젝트 베이스 (GitHub 또는 Notion)

위키가 "알게 된 것"을 쌓는 곳이라면, 프로젝트 베이스는 "작업 그 자체"(README, 계획, 코드,
데이터 위치)를 두는 곳입니다. 세팅이 끝난 뒤 아무 때나 Claude에게 **"프로젝트 베이스
만들어줘"** 하면 됩니다.

- 가장 큰 효용: 대화가 길어지거나 다른 에이전트에게 넘길 때 "프로젝트 맥락 전부 README에
  정리해서 저장해줘" 한 뒤 링크만 던지면, 배경 설명을 반복하지 않아도 됩니다.
- **GitHub** — 변경 이력이 전부 남는 온라인 프로젝트 폴더. 에이전트가 연동 설정 없이 바로
  읽고 쓰며, git을 몰라도 "git에 저장해줘"가 곧 commit+push가 되도록 규칙을 넣어줍니다.
- **Notion** — 편집과 공유가 쉽고, 할일 트래커·Notion Calendar 연동이 큰 장점 (Notion MCP
  필요). 검증된 트래커 템플릿 구조가 [templates/project-base.md](templates/project-base.md)에
  들어 있습니다.
- 민감한 연구는 **private 권장** — 언제든 공개로 전환할 수 있고, private여도 지정한 사람을
  초대해 함께 볼 수 있습니다.

## 더 읽을거리

- 짧고 쉬운 소개 (10분): <https://joonan30.github.io/llm-wiki-labs/evolution/>
- 정식 가이드북 (무료 ebook, 긴 호흡): <https://github.com/chaek-union/llm-wiki-for-scientists>

## 위키 구경하기

그래프 뷰로 훑고 싶으면 [Obsidian](https://obsidian.md/)(무료)을 설치하고 wiki 폴더를
Vault로 여세요. 읽기만 하므로 에이전트 작업과 충돌하지 않습니다.

<img width="800" alt="Obsidian 그래프 뷰로 본 LLM Wiki — 논문 페이지들이 태그와 [[wikilink]]로 이어진 모습" src="https://github.com/user-attachments/assets/553c6c02-9ea7-4d8e-b9dc-81a220743670" />

---

## For AI agents

If a user pointed you at this repository and asked to set it up ("나도 이거 세팅해줘",
"set this up for me", or similar): fetch and follow
<https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/SETUP.md>.

## Credits

- LLM Wiki 방법론: [안준용 교수, 고려대](https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959) · 원안: [Andrej Karpathy](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)
- 확장판과 브리핑 시스템: 이호준 ([@ehojune](https://github.com/ehojune))
- 한국어 humanizer 스킬: [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills) (MIT)
