# 연구자를 위한 LLM 에이전트 튜토리얼

논문 PDF를 개인 지식베이스(LLM Wiki)로 쌓고, 매일 정해진 시간에 관심사 기반 최신 논문
브리핑까지 받는 세팅을 Claude에게 한 줄로 맡기는 튜토리얼입니다.

## 사용법 — 이게 전부입니다

[Claude Desktop](https://claude.com/download)을 설치하고, 새 대화에 아래를 붙여넣으세요.

```
https://github.com/ehojune/llm-agent-tutorial-for-researchers
나도 이거 세팅해줘
```

Claude가 이 저장소를 읽고 몇 가지를 물어본 뒤(연구 분야, 위키 버전, 브리핑 시간과 수신
방법) 폴더 생성부터 매일 브리핑 예약까지 알아서 끝냅니다. 위키 폴더를 따로 정하지 않으면
홈 폴더에 `llm-wiki`를 만들어 줍니다.

## 뭐가 세팅되나

1. **LLM Wiki** — `논문 PDF → 요약(sources/) → 위키 페이지(wiki/)` 3단 구조의 개인
   지식베이스. 모든 답이 "실제로 갖고 있는 논문"에 근거하도록 강제하는 4대 규칙(웹 검색
   금지 등)이 핵심입니다. PDF를 주고 "ingest 해줘" 하면 등록 + 요약 + 기존 논문과의 연결
   보고까지 한 번에 해줍니다.
2. **데일리 논문 브리핑** — 관심사를 바탕으로 매일 정해진 시간에 PubMed 최신 논문을 훑어
   브리핑합니다. 수신 방법은 데스크탑 알림(기본, 설정 불필요), 이메일, Slack, Notion 중
   선택. 브리핑 시간에 컴퓨터가 꺼져 있었다면, 다음에 위키 폴더에서 Claude를 열었을 때
   밀린 브리핑을 잡아서 해줍니다.
3. **한국어 humanizer 스킬** — [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills)의
   `humanizer`를 함께 설치합니다. AI가 쓴 한국어 특유의 패턴 40가지(쉼표 과다, 번역투 등)를
   찾아 자연스럽게 고쳐주는 스킬로, 한국어로 글 쓸 일이 있을 때 "자연스럽게 해줘" 하면
   발동합니다.

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

## 더 읽을거리

- 짧고 쉬운 소개 (10분): <https://joonan30.github.io/llm-wiki-labs/evolution/>
- 정식 가이드북 (무료 ebook, 긴 호흡): <https://github.com/chaek-union/llm-wiki-for-scientists>

## 위키 구경하기

그래프 뷰로 훑고 싶으면 [Obsidian](https://obsidian.md/)(무료)을 설치하고 wiki 폴더를
Vault로 여세요. 읽기만 하므로 에이전트 작업과 충돌하지 않습니다.

---

## For AI agents

If a user pointed you at this repository and asked to set it up ("나도 이거 세팅해줘",
"set this up for me", or similar): fetch and follow
<https://raw.githubusercontent.com/ehojune/llm-agent-tutorial-for-researchers/main/SETUP.md>.

## Credits

- LLM Wiki 방법론: [안준용 교수, 고려대](https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959) · 원안: [Andrej Karpathy](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)
- 확장판과 브리핑 시스템: 이호준 ([@ehojune](https://github.com/ehojune))
- 한국어 humanizer 스킬: [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills) (MIT)
