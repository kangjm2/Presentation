# 지식을 쌓고 스스로 고치는 AI

지식 기반(knowledge base)을 쌓고, 그 위에서 LLM이 점검 · 개선 루프를 돌려 시스템이 스스로 나아지게 하는 플랫폼을 정리한 자료입니다. 다음 내용을 다룹니다.

- 요소 기술
  - 지식 그릇
  - 컨텍스트 엔지니어링
  - 행동
  - 평가
  - 통제
- LLM이 지식을 로직으로 쌓는 방법
  - 기억 네 가지
  - 컨텍스트 진화
  - 스킬 · 코드
  - 탐색 · 진화
  - 가중치 학습
- 자율의 조건과 위험, 안전장치
- RF · KPI 업무에 적용하는 예

16장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/FosS4dHitWtcdihzySMG4a, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/JKA4xJYXTPwcBj7VAoxegg
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py knowledge-loop`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`knowledge-structuring`](../knowledge-structuring/): 지식 축적 · 구조화 심화
  - [`network-digital-twin`](../network-digital-twin/)
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 루프
  - [`taylor-diagram`](../taylor-diagram/): 보정 결과 평가 지표
  - [`ue-kpi-pipeline`](../ue-kpi-pipeline/): KPI 원천

## 구성 (≈ 13분 50초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | trend | 연표(RAG 2020 → LLM Wiki 2026), 왜 지식 · 루프인가, 피드백이 엔진, 통신 업계 자율 망 목표 | 0:55 |
| 3 | arch | 관측 → 검색 → 실행 → 평가 → 성찰 → 갱신 루프와 다섯 층(지식 · 실행 · 평가 · 학습 · 통제) | 0:55 |
| 4 | kb | 지식 그릇 여섯 가지(원문 · 벡터 RAG · 지식 그래프 · 구조화 DB · LLM 위키 · 스킬), 섞어 쓰기, 메타데이터 | 0:55 |
| 5 | context | 컨텍스트 엔지니어링: 검색 파이프라인, 컨텍스트 부패, 점진적 공개, 기억 계층 | 0:50 |
| 6 | act | ReAct 루프, 도구 호출 · MCP · 코드 실행, 워크플로 vs 에이전트, 권한 | 0:50 |
| 7 | eval | 피드백 원천 여섯 가지의 신뢰도 · 속도, 정답 없이 돌리면 나빠진 예, 관측 | 0:55 |
| 8 | memory | 기억 네 가지(작업 · 일화 · 의미 · 절차)와 사례 → 규칙 → 스킬 승격 | 0:50 |
| 9 | learn1 | 쌓는 법 ①: Reflexion, ACE(Generator · Reflector · Curator), 컨텍스트 붕괴, LLM 위키 | 1:00 |
| 10 | learn2 | 쌓는 법 ②: Voyager 스킬 라이브러리, Agent Skills, 스킬 승격 기준 | 0:55 |
| 11 | learn3 | 쌓는 법 ③: AlphaEvolve · 다윈 괴델 머신, 네 가지 방법 비교(속도 · 되돌리기 · 조건) | 1:00 |
| 12 | autonomy | 자율적으로 가능한가: 피드백 조건별 자율 수준, 자율 레벨 L0~L5, 업계 현황 | 1:00 |
| 13 | risks | 실패 모드 여덟 가지와 대응 | 0:55 |
| 14 | guard | 안전장치: 변경의 길(제안 → 검증 → 승인 → 단계 배포 → 롤백)과 여섯 원칙 | 0:50 |
| 15 | telecom | 우리 분야: 지식 기반 내용, 망 운영 루프(부분 자율) · 시뮬 보정 루프(높은 자율) | 0:55 |
| 16 | summary | 정리와 시작하는 다섯 단계 | 0:45 |

10분 안에 맞추는 방법:

| 백업으로 돌릴 슬라이드 | 발표 시간 |
|---|---|
| 5 · 6 · 8 · 14쪽 | 약 10분 30초 |
| 5 · 6 · 8 · 14쪽 + 4쪽 | 약 9분 35초 |

- 5 · 6쪽(컨텍스트 · 행동)은 3쪽 구조도에서 한 줄씩 짚으면 됩니다.
- 14쪽(안전장치)은 13쪽 표의 대응 열로 대신할 수 있습니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 업무]`

참고할 점:
- **연구 수치:** 모두 각 논문 · 발표의 저자 보고 수치이며, 독립 재현은 확인하지 않았습니다.

  | 연구 | 보고 수치 |
  |---|---|
  | Reflexion | HumanEval 91% |
  | ACE | 에이전트 +10.6% · 금융 +8.6%, 컨텍스트 붕괴 18,282 → 122 토큰 · 66.7 → 57.1%, 정답 신호 없는 FiNER 70.7 → 67.3% |
  | Voyager | 고유 아이템 3.3배 · 기술 단계 최대 15.3배 |
  | AlphaEvolve | 4×4 복소 행렬 곱셈 48번 · Borg 연산 자원 0.7% 회수 |
  | 다윈 괴델 머신 | SWE-bench 20.0 → 50.0% · Polyglot 14.2 → 30.7% |
- **LLM Wiki(4 · 9쪽):** 2026년 4월 Karpathy의 X 게시물과 gist에서 시작한 방식입니다. “약 100문서 · 40만 단어” 같은 규모는 2차 보도 기준입니다.
- **자율 레벨(12쪽):** TM Forum 자율 망 레벨(L0~L5)을 지식 루프에 맞게 옮긴 것으로, 공식 정의가 아닙니다.
- **업계 현황(2 · 12쪽):** 운영사 대부분이 L2~L3, 81%가 2030년까지 L4 목표라는 수치는 TM Forum 2026 조사(운영사 80곳) 기준입니다. Accenture 조사는 더 보수적으로 봅니다.
- **우리 분야 루프(15쪽):** 개념 설계 예시입니다. 통신 분야 LLM 에이전트(AgentRAN 등)는 대부분 연구 · 시험 단계이며, 운영 성과가 공개된 사례는 드뭅니다.
- **안전장치(14쪽) · 시작 순서(16쪽):** 소프트웨어 배포 관행을 옮긴 권장안입니다. 평가셋 50~100개는 출발점 예시입니다.

## 출처

지식 · 검색 · 컨텍스트
- P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” NeurIPS 2020
- D. Edge et al., “From Local to Global: A GraphRAG Approach to Query-Focused Summarization,” arXiv:2404.16130 (2024)
- Chroma, “Context Rot: How Increasing Input Tokens Impacts LLM Performance” (2025) — https://trychroma.com/research/context-rot
- C. Packer et al., “MemGPT: Towards LLMs as Operating Systems,” arXiv:2310.08560 (2023)
- A. Karpathy, “LLM Wiki” gist와 X 게시물 (2026.04). 2차 정리: https://implicator.ai/karpathys-llm-wiki-got-16-million-views-the-code-isnt-the-point-2/

행동 · 도구
- S. Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models,” arXiv:2210.03629 (2022)
- Anthropic, Model Context Protocol (2024.11)
- Anthropic, “Building effective agents” (2024)
- Anthropic, Agent Skills (2025). 2025.12에 오픈 표준이 됨 — https://agentskills.io

학습 · 개선 루프
- N. Shinn et al., “Reflexion: Language Agents with Verbal Reinforcement Learning,” NeurIPS 2023
- G. Wang et al., “Voyager: An Open-Ended Embodied Agent with Large Language Models,” arXiv:2305.16291 (2023)
- T. Sumers et al., “Cognitive Architectures for Language Agents (CoALA),” arXiv:2309.02427 (2023)
- Q. Zhang et al., “Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models,” arXiv:2510.04618 (ICLR 2026)
- A. Novikov et al., “AlphaEvolve: A coding agent for scientific and algorithmic discovery,” Google DeepMind (2025)
- J. Zhang et al., “Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents,” arXiv:2505.22954 (ICLR 2026)
- I. Shumailov et al., “AI models collapse when trained on recursively generated data,” *Nature* 631 (2024)

통신
- TM Forum, Autonomous Networks 보고서 · 2026 운영사 조사 — https://tmforum.org/news-insight/newsroom/autonomous-networks-leadership-forum-spotlights-level-4-shift
- “AgentRAN: An Agentic AI Architecture for Autonomous Control of Open 6G Networks,” arXiv:2508.17778
- O-RAN Alliance, SMO · Non-RT RIC · rApp 구조
