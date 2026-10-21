# RF 모델링 툴

RF 모델링 툴에 어떤 것이 있고 어떻게 활용하는지 정리한 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **무엇이 있나:** 다루는 규모에 따라 다섯 층으로 나눴습니다.
  1. EM · 회로 (HFSS · CST · Feko · ADS)
  2. 전파 · 채널 (경험 모델 · 레이 트레이싱 · 확률 채널)
  3. 링크 · 시스템 시뮬레이터 (MATLAB · Sionna · ns-3)
  4. 망 설계 (Atoll · Planet · iBwave · Ranplan)
  5. 디지털 트윈 (NVIDIA AODT · VIAVI AI RSG)
- **어떻게 쓰나:** 다음 네 가지를 다룹니다.
  - 입력 데이터
  - 망 설계 프로젝트의 흐름 (데이터 → 보정 → 예측 → 분석 → 최적화 → 검증)
  - 모델 보정
  - 망의 일생 단계별 활용
- **고르는 기준:** 규모 · 주파수, 정확도와 속도, 데이터 수준, 연동, 비용 · 지원, 검증 근거

“RF 모델링 툴”을 안테나 설계용 EM 툴부터 망 설계 툴, 디지털 트윈까지 포함하는 넓은 뜻으로 잡았습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/VsywSCvh9urMV3dem87bY2, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/1yfFkf94UTq8sbZXohFxGa
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py rf-modeling-tools`로 뷰어를 다시 만듭니다.
- 관련 덱: [`propagation-models`](../propagation-models/) · [`ray-tracing`](../ray-tracing/) · [`lls-sls`](../lls-sls/) · [`network-digital-twin`](../network-digital-twin/) · [`traffic-model`](../traffic-model/) · [`ue-kpi`](../ue-kpi/)

## 구성 (≈ 9분 50초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | 툴 지도: 다섯 층 · 답하는 질문 · 대표 툴 · 위층으로 넘기는 것 | 0:55 |
| 3 | em | ① EM · 회로: FEM · FDTD/FIT · MoM · 회로, HFSS · CST · Feko · ADS · Microwave Office | 0:50 |
| 4 | propagation | ② 전파 · 채널: 경험 모델 · 우세 경로 · 레이 트레이싱 · 확률 채널 | 0:55 |
| 5 | planning | ④ 망 설계: Atoll · Planet · iBwave · Ranplan, 예측 · 용량 · 자동 최적화 · 파라미터 계획 · 측정 연동 | 0:55 |
| 6 | simtwin | ③ 시뮬레이터(MATLAB · Sionna · ns-3 5G-LENA · Vienna)와 ⑤ 디지털 트윈(AODT · AI RSG) | 0:55 |
| 7 | data | 활용 ①: 입력 데이터 7종과 틀렸을 때의 영향 | 0:50 |
| 8 | workflow | 활용 ②: 망 설계 프로젝트 흐름과 보정 되먹임 | 0:55 |
| 9 | calibration | 활용 ③: 모델 보정 절차와 지표 (평균 오차 · 표준편차) | 0:55 |
| 10 | usecases | 활용 ④: 장비 개발 → 기술 평가 → 사전 · 상세 설계 → 최적화 → 간섭 · 공존 → 전자파 안전 | 0:55 |
| 11 | choose | 고르는 기준 6가지와 실무 조합 예 | 0:50 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 지역]`

참고할 점:
- **제품 기능:** 각사 공개 자료 수준으로 요약했습니다. 기능은 버전과 라이선스 모듈에 따라 다릅니다. 내부 알고리즘(예: Planet의 AI 3D 모델 AIM)은 제조사 설명을 옮긴 것입니다.
- **발표자 정리:** 다섯 층 분류(2쪽), 단계별 활용(10쪽), 고르는 기준(11쪽)은 발표자 정리입니다. 한 툴이 여러 층에 걸치는 경우도 많습니다(예: MATLAB, Sionna, Feko · WinProp).
- **보정 그림:** 9쪽 산점도는 임의 데이터로 만든 개념도입니다. 목표 오차 수치는 사업자 기준에 따르므로 넣지 않았습니다.

## 출처

- 망 설계 · 보정: Forsk Atoll 측정 · 보정 교육 자료 ([Atoll 3.1.2 Measurement & Calibration, SlideShare](https://www.slideshare.net/slideshow/atoll-3-12measurementcalibration/164460956)) · [SPM 보정 사례 (telecomHall)](https://telecomhall.net/t/calibration-of-the-standard-propagation-model-with-atoll-software/14437) · [Infovista Planet 개요 (TrustRadius)](https://tr-web.dev.trustradius.com/products/infovista-planet/details) · [Infovista · iBwave 협력 발표](https://totaltele.com/infovista-and-ibwave-collaborate-to-deliver-unified-solution-for-indoor-and-outdoor-wireless-design/) · [iBwave 제품 비교표](https://ibwave.com/storage/app/media/pdf/comparison-charts/Comparison-Chart-Master.pdf) · [무선 설계 툴 목록 (UBC RSL)](https://rsl.ece.ubc.ca/planning.html)
- 전파 · 채널: 레이 트레이싱 세미나 출처(Remcom Wireless InSite, Altair WinProp, Forsk Aster, Sionna RT) · 3GPP TR 38.901 · [NYUSIM (arXiv 1703.08232)](https://arxiv.org/abs/1703.08232) · [QuaDRiGa 비교 (arXiv 2211.12601)](https://arxiv.org/pdf/2211.12601)
- 시뮬레이터 · 트윈: LLS · SLS 세미나와 네트워크 디지털 트윈 세미나 출처(MATLAB 5G Toolbox, Sionna, ns-3 5G-LENA, Vienna 5G 시뮬레이터, NVIDIA AODT, VIAVI TeraVM AI RSG)
- EM 해석 방법: 각 툴 제품 문서(Ansys HFSS · Dassault Systèmes CST Studio Suite · Altair Feko · Keysight ADS · Cadence AWR Microwave Office) 및 일반 전산전자기 교재
