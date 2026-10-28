# 지식을 쌓고 구조화하는 법

LLM이 잘 쓸 수 있도록 지식을 쌓고 구조화하는 방법을 연구 결과와 함께 정리한 자료입니다. 다루는 내용은 다음과 같습니다.

- 문서 조각 나누기와 맥락 붙이기
- 하이브리드 검색과 요약 트리(RAPTOR)
- 지식 그래프(GraphRAG · LightRAG · HippoRAG)와 스키마
- 에이전트 기억 연구(Generative Agents · MemGPT · A-MEM · Mem0)
- 시간 정보(Zep)와 새 지식의 통합 규칙
- 품질 평가, 질문 유형별 구조 선택, RF · KPI 지식 기반 설계 예

[`knowledge-loop`](../knowledge-loop/) 덱이 자율 개선 루프 전체를 다뤘다면, 이 덱은 그 바탕인 지식 층을 깊게 봅니다. 16장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/HWB8A2oFoT1NJrsRR7DDDV, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/Nw7ET4PnF16YdRPGegvPjP
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py knowledge-structuring`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`knowledge-loop`](../knowledge-loop/): 지식 기반 · 자율 개선 루프
  - [`ue-kpi-pipeline`](../ue-kpi-pipeline/): KPI 원천
  - [`upper-layers`](../upper-layers/): 용어

## 구성 (≈ 14분 35초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | problem | 쌓기만 한 지식의 네 가지 문제(못 찾음 · 묻힘 · 부딪힘 · 낡음), Lost in the Middle의 U자 경향, 긴 대화 기억 약 30% 하락 | 0:55 |
| 3 | lifecycle | 지식의 일생(수집 → … → 만료 · 폐기)과 구조의 다섯 수준(조각 · 요약 트리 · 그래프 · 스키마 · 기억/시간) | 0:50 |
| 4 | chunk | 조각 나누기 다섯 가지(고정 · 재귀 · 문서 구조 · 의미 · 늦은 조각내기), 베를린 예로 본 맥락 잃음과 맥락 덧붙임 | 0:55 |
| 5 | retrieve | 맥락 덧붙인 검색: 검색 실패율 5.7 → 3.7 → 2.9 → 1.9%, 키워드(BM25) · 재순위 | 0:55 |
| 6 | tree | RAPTOR 요약 트리(군집 → 요약 반복), 층을 섞어 검색, QuALITY +20%p | 0:55 |
| 7 | graph1 | 지식 그래프 만들기: 개체 · 관계 추출 → 개체 통합 → 스키마 → 근거 연결, RF 예시 그래프 | 0:55 |
| 8 | graph2 | GraphRAG · LightRAG · HippoRAG 비교, 그래프가 필요 없는 경우와 값을 하는 경우 | 0:55 |
| 9 | schema | RF · KPI 스키마 예(셀 · 파라미터 · KPI · 장애 · 규격), 기존 표준(3GPP NRM · TM Forum SID · YANG) | 0:50 |
| 10 | memory | 에이전트 기억 연구 네 가지 비교, Mem0 수치와 “짧으면 그냥 다 넣는 게 낫다” | 0:55 |
| 11 | time | 유효 기간 · 두 개의 시간(bi-temporal) · 무효화, Zep의 시간 추론 개선, 통신 분야의 시간 정보 | 0:55 |
| 12 | consolidate | 새 지식 처리(비교 → 추가 · 수정 · 무효화)와 주기적 정리, 통째 재작성 금지, 모순은 조건 차이, 잊기 | 0:55 |
| 13 | eval | 검색 · 답 · 지식 건강 · 쓰임 · 비용 지표, RAGAS, 골든셋 | 0:50 |
| 14 | choose | 질문 유형별 구조 선택 표, 작으면 다 넣기 | 0:55 |
| 15 | telecom | 자료별 그릇(규격 · KPI 정의서 · CM/PM · 장애 사례 · DT), Telco-RAG · TeleQnA, 우리만의 지식 | 0:55 |
| 16 | summary | 쌓기 · 엮기 · 고치기와 시작 다섯 단계 | 0:45 |

- 10분 안에 맞추려면 3 · 8 · 9 · 10 · 13쪽을 백업으로 돌리세요. 약 10분 15초가 됩니다.
- 14쪽(구조 선택 표)이 빠진 내용을 한 장으로 다시 묶어 주므로, 이 장들을 빼도 흐름이 이어집니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 자료]`

참고할 점:
- **연구 수치:** 모두 저자 · 회사가 보고한 값이며, 조건(모델 · 데이터)이 서로 달라 직접 비교할 수 없습니다.
  - **Contextual Retrieval:** Anthropic 내부 벤치마크 기준입니다.
    - 상위 20개 검색 실패율: 기본 5.7%, 맥락 임베딩 3.7%, 맥락 BM25 추가 2.9%, 재순위 추가 1.9%(−67%)
    - 1.9%라는 숫자는 −67%에서 역산한 값입니다.
    - 분야별 편차(약 41~84%)는 2차 분석 기준입니다.
  - **RAPTOR:** QuALITY에서 GPT-4와 함께 썼을 때 기존 최고보다 +20%p입니다.
  - **HippoRAG:** 다단계 QA에서 최대 +20%, 반복 검색(IRCoT)보다 10~20배 저렴하고 6~13배 빠릅니다. arXiv판은 10~30배로 표기합니다.
  - **Mem0(LOCOMO):** OpenAI 기억 기능보다 정확도가 상대적으로 +26%입니다. 전체 대화를 넣는 것보다 p95 지연 −91%, 토큰 −90%입니다. 다만 30턴 이하의 짧은 대화에서는 전체를 넣는 편이 더 정확했습니다.
  - **Zep(LongMemEval, gpt-4o-mini):** 시간 추론 36.5 → 54.1%, 여러 세션 40.6 → 47.4%입니다. 지식 갱신과 단일 세션 일부 질문은 조금 낮아졌습니다.
  - **Telco-oRAG:** 3GPP 질문 정확도가 최대 +17.6%입니다.
- **U자 그림(2쪽):** Lost in the Middle의 경향을 그린 개념도이며, 실제 측정값이 아닙니다.
- **LightRAG 비교(8쪽):** 비용 · 갱신의 장점은 주로 2차 분석에 근거합니다. 정량 비교는 원 논문을 확인하세요.
- **스키마 · 설계 예(9 · 15쪽):** RF · KPI 업무를 기준으로 만든 예시입니다. 실제 개체 · 속성은 보유 데이터에 맞춰 정합니다.
- **골든셋 50~100개(13 · 16쪽):** 출발점으로 제안하는 규모입니다.

## 출처

조각 · 검색
- Anthropic, “Introducing Contextual Retrieval” (2024.09) — https://www.anthropic.com/engineering/contextual-retrieval
- M. Günther et al., “Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models,” arXiv:2409.04701 (Jina AI, 2024)
- N. F. Liu et al., “Lost in the Middle: How Language Models Use Long Contexts,” TACL 12 (2024)
- P. Sarthi et al., “RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval,” ICLR 2024 (arXiv:2401.18059)

그래프 · 스키마
- D. Edge et al., “From Local to Global: A GraphRAG Approach to Query-Focused Summarization,” arXiv:2404.16130 (2024)
- Z. Guo et al., “LightRAG: Simple and Fast Retrieval-Augmented Generation,” arXiv:2410.05779 (2024)
- B. J. Gutiérrez et al., “HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models,” NeurIPS 2024 (arXiv:2405.14831)
- 3GPP TS 28.541 (5G 네트워크 자원 모델) · TM Forum Information Framework (SID) · O-RAN / 장비 YANG 모델

기억 · 시간
- J. S. Park et al., “Generative Agents: Interactive Simulacra of Human Behavior,” UIST 2023 (arXiv:2304.03442)
- C. Packer et al., “MemGPT: Towards LLMs as Operating Systems,” arXiv:2310.08560 (2023)
- W. Xu et al., “A-MEM: Agentic Memory for LLM Agents,” NeurIPS 2025 (arXiv:2502.12110)
- P. Chhikara et al., “Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory,” arXiv:2504.19413 (2025)
- P. Rasmussen et al., “Zep: A Temporal Knowledge Graph Architecture for Agent Memory,” arXiv:2501.13956 (2025)
- D. Wu et al., “LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory,” ICLR 2025 (arXiv:2410.10813)
- Q. Zhang et al., “Agentic Context Engineering,” arXiv:2510.04618 (ICLR 2026)

평가 · 통신
- S. Es et al., “RAGAS: Automated Evaluation of Retrieval Augmented Generation,” arXiv:2309.15217 (2023)
- A.-L. Bornea et al., “Telco-RAG: Navigating the Challenges of Retrieval-Augmented Language Models for Telecommunications,” arXiv:2404.15939 (2024)
- “Telco-oRAG: Optimizing Retrieval-augmented Generation for Telecom Queries via Hybrid Retrieval and Neural Routing,” arXiv:2505.11856 (2025)
- A. Maatouk et al., “TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge,” arXiv:2310.15051 (2023)
