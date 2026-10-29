# 트윈 검증 · 인증 (V&V): 언제 믿어도 되나

무선망 디지털 트윈이 내놓는 숫자를 언제, 어디에 믿고 써도 되는지 정하는 틀을 정리한 자료입니다. 시뮬레이션 분야의 고전적인 **검증(verification) · 타당성 확인(validation) · 인증(accreditation)**, 줄여서 VV&A를 우리 트윈에 맞췄습니다. 오차 지표 자체는 앞선 자료(debiased-rmse · taylor-diagram · dt-breakdown)에서 다뤘으므로, 여기서는 그 숫자로 무엇을 결정할지, 즉 **판정 규칙**에 집중합니다.

다루는 내용은 다음과 같습니다.

- 질문 바꾸기: “6.41 dB는 좋은가” → “무엇에 · 어느 지역에 · 어느 버전까지 써도 되나”
- 용어: 검증 · 타당성 확인 · 인증, 보정 ≠ 확인, 확인은 합격 · 불합격이 아니다 (ASME V&V 20)
- 검증: 해석해(Friis · 2-ray · 칼날 회절) · 상반성 · 회귀 · 수렴 · σ_sim · 입력 대조
- 용도에 맞는 정확도: 커버리지 구멍 찾기 · 간섭/SINR · 처리량 · what-if 비교
- σ를 판정 오류로 바꾸기: 칸 하나의 오판 확률 Φ(−|m|/σ), 칸 전체의 오판율 · 구멍 재현율 곡선 (예시 계산)
- 합격선: 결정 요구에서 거꾸로 끌어내기 (예시 제안), 문헌의 보정 후 수준은 참고로만
- 보정 · 확인 자료를 공간으로 떼기 (예시 시뮬레이션)
- 클러스터별 · 구간으로 보고하기, 판정 규칙(합격 · 불합격 · 보류)
- 지표 자체의 불확실성: n_eff, 블록 부트스트랩
- 재확인 조건과 모델 카드(확인 보고서) 양식

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/GEXDLCWU8odk3hSXAprQMd, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/LKvm6u3WjA9nRjQmTdvD1q
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py twin-vv`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`debiased-rmse`](../debiased-rmse/): 영국 사례(보정 후 σ 2.57 dB)와 우리 결과(보정 전 6.41 dB)
  - [`dt-breakdown`](../dt-breakdown/): 판정 숫자 de-biased RMSE · n_eff · Q-AM-49 · σ_sim 미측정
  - [`taylor-diagram`](../taylor-diagram/): σ · R · E′
  - [`coord-registration`](../coord-registration/): 좌표 정합 (검증의 입력 대조)
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 방법과 보정 / 검증 자료 분리
  - [`spatial-statistics`](../spatial-statistics/): 공간 상관 · 블록 크기 (9쪽에서 넘김)

## 구성 (≈ 11분 40초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | question | 6.41 dB를 알려진 숫자와 줄 세우기(영국 2.57 · 5.71, Phillips RMSE 8~9 · 12~15), Sargent “목적에 대해 판단” | 0:50 |
| 3 | terms | 검증 · 타당성 확인 · 인증 정의, 보정 ≠ 확인, V&V 20 “합격 · 불합격이 아니다” | 0:55 |
| 4 | verify | 검증 시험 일곱(해석해 · 상반성 · 회귀 · 수렴 · σ_sim · 입력 대조), 코드 검증 vs 해 검증 | 0:50 |
| 5 | purpose | 용도 넷별로 맞아야 하는 것 · 볼 지표, what-if의 σ_Δ = σ√(2(1−ρ)), 커버리지에는 bias가 돌아온다 | 0:55 |
| 6 | onebin | 칸 하나의 오판 확률 곡선과 표(여유 3 · 6 · 10 dB × σ 2.57 · 6.41 · 8), bias +3 dB면 3 dB 구멍 50% | 0:55 |
| 7 | rate | 칸 전체 오판율 vs σ (bias 0 · ±3), 칸 1,000개당 혼동표, 거꾸로 읽은 σ 요구 | 0:55 |
| 8 | criteria | 용도별 예시 합격선, 문헌의 보정 후 수준(Phillips, 참고용), 정하는 순서 | 0:55 |
| 9 | split | 무작위 분할 vs 블록 분할 예시 시뮬레이션(보정 후 σ 3.3 vs 4.8 dB) | 0:55 |
| 10 | clusters | 클러스터별 σ와 95% 구간, 합격 · 불합격 · 보류 규칙 (예시) | 0:55 |
| 11 | uncertainty | σ 구간 vs n_eff, 무작위 · 블록 부트스트랩 · n_eff 근사의 구간 폭 비교 | 0:55 |
| 12 | revalidate | 재확인 조건: CM · 장면 · 계절(P.833) · 소프트웨어 · 측정 체계 · 감시 | 0:50 |
| 13 | card | 모델 카드 양식, NASA-STD-7009A 보고 다섯 · 신뢰도 8요인, Model Cards | 0:50 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 4쪽(검증)과 12쪽(재확인 조건)을 백업으로 돌리세요. 약 10분이 됩니다. 더 줄이려면 11쪽(지표의 불확실성)도 빼서 약 9분 5초로 맞춥니다.
- 통계에 익숙한 청중이면 6쪽을 짧게 넘기고 7쪽에 시간을 쓰세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 13쪽 모델 카드 양식의 `[지역]`, 대역, 날짜, 버전 (지금 값은 예시)
- 마지막 장의 `[대상 지역]`
- 8쪽 합격선 — 팀 합의로 정할 값입니다

참고할 점:
- **합격선 숫자는 모두 예시 제안입니다(8 · 10 · 13쪽).** 무선 트윈 · 전파 예측에 쓰는 공인 표준 합격선은 찾지 못했습니다. 4쪽의 “통과 예”(0.1 dB · 0.2 dB · 불일치 0건), 5쪽의 ρ = 0.9, 12쪽의 “분기” 주기도 예시입니다.
- **Phillips 외 2012(2 · 8쪽):** 경로 손실 모델 30개를 2.4 · 5.8 GHz · 900 MHz ISM/UNII 대역 실측과 비교해, 튜닝 전 최선이 RMSE 12~15 dB, 측정으로 튜닝하면 8~9 dB라고 보고했습니다. 셀룰러 대역 · RSRP가 아니고 지표도 RMSE(bias 포함)라 우리 σ와 직접 비교할 수 없습니다. 2쪽 그림과 8쪽 카드는 크기 감각을 주려는 것이며 합격선이 아닙니다.
- **영국 사례(2쪽):** arXiv 2510.09478의 10 m 구역 70개 평균 오차의 표준편차입니다. 집계 조건이 달라 6.41 dB와 직접 비교할 수 없다는 점은 debiased-rmse 덱에 정리되어 있습니다.
- **6 · 7쪽 계산:** 정규 오차 e ~ N(b, σ), 칸끼리 독립, 실측 칸 값을 참값으로 둔다는 가정입니다(실측 잡음 무시).
  - 6쪽은 해석식 Φ(−|m|/σ)입니다. 여유 3 dB: 12.2% · 32.0% · 35.4%(σ 2.57 · 6.41 · 8), 6 dB: 1.0% · 17.5% · 22.7%, 10 dB: 0.0% · 5.9% · 10.6%.
  - 7쪽은 실측 칸 RSRP ~ N(−100, 10) dBm, 문턱 −110 dBm(구멍 약 16%)을 가정한 20만 칸 몬테카를로(시드 3)입니다. σ 6.41 dB에서 오판 12.1%, 구멍 재현율 75%(bias +3 dB면 60%), σ 2.57에서 오판 5.0%, 재현율 87%. 일치율 90% → σ ≤ 5.2 dB, 95% → σ ≤ 2.6 dB(2.55), 재현율 80% → σ ≤ 4.4 dB.
  - bias +3 dB(낙관)일 때 전체 오판율은 bias 0보다 조금 낮게 나옵니다. 대부분 칸이 덮인 칸이라 그쪽 오판이 줄기 때문입니다. 대신 구멍 재현율이 떨어집니다.
  - −110 dBm 문턱과 RSRP 분포는 예시입니다. 우리 지역의 실측 분포와 실제 문턱으로 다시 계산하세요.
- **9쪽 예시 시뮬레이션:** 60 × 60칸 오차 장(상관 있는 σ 5 dB + 독립 3 dB, 시드 21)에 “반경 3칸 안 보정용 칸의 평균 오차를 빼는” 국소 보정을 적용했습니다. 확인 칸의 보정 후 σ는 무작위 50% 분할에서 3.3 dB, 12칸(20 m 칸이면 240 m) 바둑판 블록 분할에서 4.8 dB, 보정 전 약 5.8 dB입니다.
- **10쪽 클러스터 예시:** 클러스터별 정규 오차를 지어 만든 자료(시드 8)입니다. n_eff는 Breakdown 예시(1,204 → 312, φa·φb ≈ 0.59)의 비율 0.26을 빌려 n × 0.26으로 두었습니다. 구간은 정규 가정의 χ² 구간(Wilson–Hilferty 근사, 자유도 n_eff − 1)입니다. 클러스터별 σ는 각 클러스터의 bias를 뺀 값이고, “전체”는 전체 bias 하나만 뺀 값입니다. 판정 규칙(합격 · 불합격 · 보류)은 제안이며, Sargent 외 2016이 소개한 구간 가설 검정(허용 범위 L, U)과 같은 생각입니다.
- **11쪽:** 왼쪽 곡선은 σ = 6.41 dB에 대한 χ² 구간입니다(n_eff 312 → 5.9~7.0 dB, 명목 1,204 → 6.2~6.7 dB). 오른쪽 표는 35 × 35칸 합성 오차 장(이웃 상관 0.82, 시드 31 · 32)으로, 400회 반복의 실제 흩어짐(95% 범위의 반폭 ±0.74 dB)과 한 장에서 낸 구간 반폭(40장 평균, 재표본 400회)을 비교했습니다. 무작위 재표본 ±0.24, 7 × 7칸 블록 재표본 ±0.58, AR(1) n_eff 근사(242) ±0.58 dB. 블록 · n_eff 방식도 실제보다 조금 좁습니다.
  - Breakdown 화면은 n_eff를 α · r · c₁ 구간에만 쓰고 판정 숫자는 칸 전부로 계산합니다. “판정 숫자에도 구간을 붙이자”는 이 자료의 제안입니다.
- **12쪽 식생:** ITU-R P.833-10(2021)의 “1 GHz 부근에서 잎 있는 나무의 감쇠(dB/m)가 잎 없을 때보다 약 20% 크게 보인다”는 문장입니다. 대역 · 수종마다 다릅니다.
- **정의(3쪽):** 검증 · 확인 · 인증 정의는 Youngblood · Pace(1995)가 인용한 DoD M&S 지시의 정의를 옮긴 것입니다. 현행 DoDI 5000.61(2024년 9월 재발행)의 용어 정의 원문은 확인하지 못했습니다(사이트 접근 차단). NASA-STD-7009A의 정의도 확인과 같은 뜻입니다(“의도한 용도의 관점에서 실제 세계를 얼마나 정확히 나타내는지”).
- **ASME V&V 20(3쪽):** 표준 원문(유료)은 보지 못했습니다. “확인 = 모델 오차의 평가, 합격 · 불합격이 아니다”, “E = S − D가 모델 오차를 담는 구간의 중심”은 표준 위원들이 쓴 해설 논문(Eça · Dowding · Roache 2020)에서 확인했습니다.
- **검증 시험(4쪽):** 코드 검증 · 해 검증 구분과 회귀 · 단위 시험, 수렴 · 이산화 오차는 NASA-STD-7009A 부록 E의 설명입니다. 시험 항목(Friis · 2-ray · P.526 칼날 회절 · 상반성)은 일반적인 관행을 정리한 것입니다.

## 출처

- R. G. Sargent, “Verification and validation of simulation models,” *Journal of Simulation* 7(1), 12–24, 2013 (doi:10.1057/jos.2012.20)
- R. G. Sargent, D. M. Goldsman, T. Yaacoub, “A tutorial on the operational validation of simulation models,” *Proc. Winter Simulation Conference*, 2016 — 검증 · 확인 정의, “타당성은 목적에 대해”, 허용 정확도는 개발 전에, 조건마다 타당성이 다를 수 있음, 구간 가설 검정
- S. M. Youngblood, D. K. Pace, “An overview of model and simulation verification, validation, and accreditation,” *Johns Hopkins APL Technical Digest* 16(2), 1995 — DoD 정의 인용
- DoD Instruction 5000.61, “DoD Modeling and Simulation Verification, Validation, and Accreditation” (2024년 9월 17일 재발행)
- NASA-STD-7009A, “Standard for Models and Simulations” (2016-07-13 승인) — 보정 · 확인 · 검증 정의, 4.3.8 결과 보고, 부록 E 신뢰도 8요인(0~4 서열 점수)
- ASME V&V 10(고체역학) · V&V 20-2009(CFD · 열전달); L. Eça, K. Dowding, P. J. Roache, “On the interpretation and scope of the V&V 20 standard …,” ASME VVS2020-8826, 2020
- C. Phillips, D. Sicker, D. Grunwald, “Bounding the practical error of path loss models,” *International Journal of Antennas and Propagation*, 2012 (doi:10.1155/2012/754158)
- D. R. Roberts 외, “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” *Ecography* 40(8), 913–929, 2017
- ITU-R P.833-10 (2021), Attenuation in vegetation
- ITU-R P.526 (회절 — 단일 칼날)
- M. Mitchell 외, “Model Cards for Model Reporting,” FAT* 2019
- “Site-Specific RIS Deployment in Cellular Networks via Calibrated Ray Tracing,” arXiv:2510.09478 (2025)
- 관련: Breakdown 화면 설명서 — n_eff(AR(1) 근사), 열린 질문 Q-AM-49, σ_sim 미측정
