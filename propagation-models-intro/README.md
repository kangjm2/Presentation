# 전파 모델 입문 (신입 사원용)

「전파 모델의 역사」(`../propagation-models/`)를 신입 사원 눈높이로 다시 만든 10분 발표 자료입니다. 수식은 링크 예산 하나만 남기고, 나머지는 그림과 비유로 설명합니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/5iVSX25WoBARAZx4zMSmRR, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/XvooMPLBZVXxfskcN6xFRx
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py propagation-models-intro`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | what | 링크 예산 = 신호의 가계부 (폭포 그림) | 0:50 |
| 3 | weaken | 신호가 약해지는 세 가지: 멀어짐 · 가려짐 · 겹침 | 0:50 |
| 4 | families | 두 갈래: 통계 계열 vs 결정론 계열 | 0:50 |
| 5 | questions | 질문이 바뀔 때마다 나온 모델 (1946 → 지금) | 1:00 |
| 6 | empirical | 경험식: Okumura 그래프 → Hata 계산식 | 0:50 |
| 7 | echoes | 메아리 비유: TDL과 클러스터 | 1:00 |
| 8 | ears | 안테나 사이의 상관: 두 귀 비유 | 0:50 |
| 9 | standard | 3GPP 표준 모델: 방향 목록 + 환경 세트장(UMa · UMi · InH) | 1:00 |
| 10 | raytracing | 레이 트레이싱: 지도 위에서 전파 추적 | 0:50 |
| 11 | choose | 언제 무엇을 쓰나 | 0:40 |
| 12 | takeaway | 기억할 한 가지: 질문이 바뀌면 모델이 바뀐다 | 0:20 |

표지의 `[발표자] · [날짜]`는 직접 채워 넣으세요.
