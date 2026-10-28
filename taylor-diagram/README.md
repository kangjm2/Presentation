# Taylor diagram 읽는 법

시뮬레이션이 실측과 얼마나 닮았는지를 표준편차 · 상관계수 · 중심 RMS 차이로 한 점에 보여 주는 Taylor diagram을 정리한 자료입니다. 다음 순서로 다룹니다.

- 그림의 원리(코사인 법칙)와 구조
- 읽는 순서와 숫자 예
- 바이어스가 보이지 않는 함정
- RSRP 시뮬레이션 검증에 쓰는 법
- 그리는 코드

11장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/1PvtTa28Nk4dX1ZtXnQVFe, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/WrsUsQZRnxtifm3qtRXt9P
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py taylor-diagram`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`dt-breakdown`](../dt-breakdown/): Breakdown 화면의 정규화 Taylor diagram
  - [`debiased-rmse`](../debiased-rmse/): 영국 사례와 우리 결과의 de-biased RMSE 비교
  - [`sim-real-alignment`](../sim-real-alignment/): 시뮬레이션을 실측에 맞추는 법
  - [`sionna-rsrp-beam`](../sionna-rsrp-beam/)
  - [`ue-antenna`](../ue-antenna/): 단말 효과

## 구성 (≈ 8분 40초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | RMSE가 같은(≈ 4 dB) 세 시뮬레이션(S1 전체가 4 dB 낮음 · S2 너무 매끈함 · S3 잡음)과 통계량 표 | 0:50 |
| 3 | stats | 바이어스 · σ · R · E′ 정의, E′² = σ_f² + σ_r² − 2σ_fσ_rR (코사인 법칙), RMSE² = 바이어스² + E′² | 0:55 |
| 4 | anatomy | 그림의 네 가지 선: 동심원(σ) · 방사선(R) · ★과 σ_r 원호 · ★ 둘레 원(E′) | 0:50 |
| 5 | read | 2쪽 시뮬을 찍어 거리 → 각도 → 원호 순서로 읽기, S1은 ★과 같은 자리 | 0:55 |
| 6 | example | σ_r = 8, σ_f = 7, R = 0.8 → E′ ≈ 4.8 dB, 바이어스 −3 dB면 RMSE ≈ 5.7 dB | 0:45 |
| 7 | bias | 함정 ①: 바이어스는 보이지 않는다, 표시하는 네 가지 방법 | 0:50 |
| 8 | rsrp | RSRP 검증에 쓰기: 보정 단계별 궤적, E′ = de-biased RMSE, 표본 맞추기, 셀별 점 | 0:55 |
| 9 | pitfalls | 함정 ②: 거리 효과로 높은 R · 같은 E′ 다른 원인 · 표본 · 정규화 · 눈금 · 음의 상관, σ · R과 원인의 연결 | 0:55 |
| 10 | code | numpy · matplotlib로 계산하고 그리기, 검산, 패키지 | 0:45 |
| 11 | summary | 정리와 다음 단계 제안 | 0:40 |

- 10분 안에 들어갑니다.
- 시간이 더 모자라면 6쪽(숫자 예)과 10쪽(코드)을 빼서 약 7분 10초로 줄일 수 있습니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 지역]`

참고할 점:
- **예시 데이터(2 · 4 · 5 · 7쪽):** 구역 200개의 RSRP를 만든 설명용 데이터입니다. 실측 σ = 8 dB이고, 생성 시드는 7입니다. 표의 값은 그 데이터로 직접 계산했습니다.

  | 시뮬 | 바이어스 | σ | R | E′ | RMSE |
  |---|---|---|---|---|---|
  | S0 | −0.7 dB | 8.3 dB | 0.96 | 2.4 dB | 2.5 dB |
  | S1 | −4.0 dB | 8.0 dB | 1.00 | 0 dB | 4.0 dB |
  | S2 | −0.1 dB | 4.0 dB | 0.996 | 4.0 dB | 4.0 dB |
  | S3 | +0.1 dB | 8.3 dB | 0.88 | 3.9 dB | 3.9 dB |

- **보정 궤적(8쪽):** 설명용 값입니다.

  | 단계 | σ | R | E′ |
  |---|---|---|---|
  | 보정 전 | 7.0 dB | 0.65 | 6.3 dB |
  | 기하 수정 | 7.5 dB | 0.82 | 4.7 dB |
  | 재질 보정 | 7.8 dB | 0.94 | 2.7 dB |

  영국 사례 수치(구역 평균 오차의 표준편차 5.71 → 2.57 dB)는 arXiv:2510.09478 기준입니다. 그 논문은 σ와 R을 따로 보고하지 않았으므로 그림의 위치로 옮기지 않았습니다.
- **E′와 de-biased RMSE:** 오차 f − r의 표준편차와 같은 값입니다. 표준편차를 N으로 나누는지 N − 1로 나누는지(ddof)를 모든 값에서 같게 해야 코사인 법칙이 정확히 맞습니다.
- **원인 연결(9쪽):** σ가 작으면 섀도잉 · 산란 · 재질 쪽, R이 낮으면 기하 · 위치 · 안테나 설정 쪽을 의심합니다. 일반적인 진단 순서이며 단정은 아닙니다.
- **패키지(10쪽):**
  - Python: SkillMetrics
  - R: plotrix의 `taylor.diagram`, openair의 `TaylorDiagram`

  정규화 여부 같은 기본값은 패키지마다 다릅니다.

## 출처

- K. E. Taylor, “Summarizing multiple aspects of model performance in a single diagram,” *Journal of Geophysical Research* 106(D7), 7183–7192, 2001
- 영국 도시 Sionna 디지털 트윈 보정 사례: “Site-Specific RIS Deployment in Cellular Networks via Calibrated Ray Tracing,” arXiv:2510.09478 (2025)
