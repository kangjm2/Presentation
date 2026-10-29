# 공간 통계: 상관 거리 · 베리오그램 · 크리깅

시뮬레이션과 드라이브 테스트 실측의 잔차(E = sim − meas)는 칸마다 따로 노는 잡음이 아니라 이웃 칸끼리 닮아 있습니다. 이 자료는 그 닮음을 재는 도구(상관 거리 · 베리오그램)와, 닮음이 신뢰 구간 · 빈칸 채우기 · 보정/검증 나누기를 어떻게 바꾸는지를 예시 시뮬레이션으로 보여 줍니다. Breakdown 화면의 열린 질문 Q-AM-49(c₁ 구간이 좁게 나옴)에 대한 설명과 해결 방향을 담았습니다.

다루는 내용은 다음과 같습니다.

- 음영의 공간 상관: 지수 모델(Gudmundson 1991), 3GPP TR 38.901 Table 7.5-6의 SF 상관 거리, 20 m 칸 비교에 주는 뜻
- 베리오그램: nugget · sill · range, γ(h) = σ²(1 − ρ(h)), 경험 베리오그램 그리기와 지수 모델 적합, 모양 네 가지 읽기
- 유효 표본 수 n_eff: 면에서는 한 줄 AR(1) 식보다 훨씬 작다, Breakdown 식(Bretherton 외 1999)의 자리
- Q-AM-49: c₁ 95% 구간의 실제 포함률 예시 시뮬레이션과 베리오그램 공분산으로 고치는 길
- 빈칸 채우기: 보통 크리깅의 가중치와 크리깅 분산, 가우시안 과정, 모델 + 크리깅한 잔차 지도
- 검증: 무작위 vs 블록 교차 검증, 블록 크기 · 버퍼 · 나누는 단위 (Roberts 외 2017)
- 팀 레시피 다섯 단계와 scikit-learn 예시 코드

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/WUdJ8uodTK9k3xmN7jVJSe, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/TVmv5HFxjMP9h6k74RHj8H
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py spatial-statistics`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`dt-breakdown`](../dt-breakdown/): 20 m 칸 · n_eff · 열린 질문 Q-AM-49 (c₁ 구간)
  - [`debiased-rmse`](../debiased-rmse/): de-biased RMSE (= 베리오그램의 sill의 제곱근)
  - [`coord-registration`](../coord-registration/): 좌표 정합 — 같은 지수 상관 가정을 씀
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 방법
  - [`propagation-models`](../propagation-models/): 음영(shadow fading)과 경로손실 모델
  - [`twin-vv`](../twin-vv/): 공간으로 떼어 놓은 검증 · 합격선

## 구성 (≈ 10분 45초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 잔차는 칸마다 따로 놀지 않는다: 예시 잔차 지도, 닮음이 바꾸는 세 가지(구간 · 빈칸 · 나누기) | 0:45 |
| 3 | corr | 상관 거리: 지수 모델, 38.901 Table 7.5-6, 20 m 이웃 칸 상관 0.21 · 0.67 · 0.85, Gudmundson | 0:50 |
| 4 | variogram | 베리오그램 개념: nugget · sill · range, γ = σ²(1 − ρ), 실용 범위 3a | 0:50 |
| 5 | empirical | 도로 516칸으로 그린 경험 베리오그램과 지수 모델 적합, 그리는 순서와 주의 | 0:50 |
| 6 | patterns | 모양 네 가지: 평평 · range 차이 · 끝없이 오름(경향) · 방향별 차이 | 0:45 |
| 7 | neff | 유효 표본 수: 면 n_eff vs 한 줄 AR(1), 1 km²에 a 50 m면 약 72 | 0:50 |
| 8 | interval | Q-AM-49: c₁ 95% 구간 포함률 — n 그대로 · AR(1) · 베리오그램 공분산 | 0:55 |
| 9 | kriging | 보통 크리깅: 1 km 단면, 가중치, 크리깅 분산 | 0:50 |
| 10 | residual | 모델 + 크리깅한 잔차: 지도 셋, 도로까지 거리별 효과, GP = 크리깅 | 0:50 |
| 11 | cv | 무작위 vs 블록 CV vs 실제 오차, 자유도에 따른 차이, Roberts 2017 | 0:50 |
| 12 | split | 나누는 법: 블록 · 버퍼 · 단위 · 여러 날 · 보고 | 0:45 |
| 13 | recipe | 팀 레시피 다섯 단계와 scikit-learn 코드 | 0:45 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 6쪽(모양 네 가지)을 백업으로 돌리세요. 약 10분이 됩니다.
- Breakdown을 모르는 청중이면 8쪽(Q-AM-49)을 짧게 넘기고 7쪽에서 결론만 말해도 됩니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 13쪽 코드의 첫값(sill 25 · a 50 m · nugget 4)을 우리 잔차의 베리오그램 적합값으로 바꾸기

참고할 점:
- **예시 시뮬레이션(2 · 5 · 6 · 8 · 9 · 10 · 11쪽):** 실제 측정 자료가 아닙니다. 모두 numpy로 시드를 고정해 계산했고, 슬라이드 숫자는 생성기 계산값을 그대로 넣었습니다.
  - 공통 가정: 1 km × 1 km를 20 m 칸 50 × 50으로 나눔, 잔차 = 편향 +2 dB + 지수 상관 성분(σ 5 dB, a 50 m) + 칸마다 독립인 nugget(σ 2 dB). a 50 m는 38.901 UMa NLOS 값을 빌린 것입니다.
  - 측정 칸은 200 m 간격 격자 도로 + 대각선 도로 하나, 516칸입니다.
  - 상관 성분은 칸 중심에서 바로 뽑았습니다(점 지지). 실제 칸 평균값은 칸 안 평균으로 상관이 조금 달라집니다.
- **경험 베리오그램(5쪽):** 한 번 뽑은 장의 결과입니다(적합 a 43 m · sill 28.4 · nugget 2.4 dB², 참값 50 m · 29 · 4). 시드를 바꾸면 nugget 추정이 0에서 15 dB²까지 크게 흔들렸습니다. 20 m 칸만으로는 20 m보다 짧은 구조와 nugget을 가르기 어렵다는 것이 이 쪽의 요점입니다.
- **모양 네 가지(6쪽):** ① 독립 잡음 σ 5.4 dB, ② a 13 m · 120 m, ③ 2쪽 장에 동서 방향 1 dB / 100 m 기울기를 더함(경향 예시), ④ 동서 a 120 m · 남북 30 m 이방성. 모두 도로 칸으로 계산했습니다.
- **n_eff(7쪽):** 평균의 분산으로 정의한 n_eff = n²σ² / ΣΣC를 정사각 면에서 정확히 계산했습니다(nugget 없음). 10 m 칸으로 바꿔도 1 km²에 a 50 m면 72.3 → 72.5로 거의 같습니다. 넓은 면 근사 면적 / (2πa²)는 약 64입니다. Breakdown의 n(1 − φa·φb)/(1 + φa·φb)는 Bretherton 외(1999) 식 (31)로, 두 AR(1) 계열의 상관(2차 모멘트)용입니다. 평균용(1차) 식 n(1 − ρ)/(1 + ρ)와 다릅니다.
- **Q-AM-49 시뮬레이션(8쪽):** 도로 516칸, 참 c₁ = 0, 장마다 400회. 설명 변수는 RU가 영역 모서리 밖 (−100, −100) m에 있다고 둔 log₁₀ 거리입니다.
  - “한 줄 AR(1)”은 Breakdown 식을 흉내 낸 것입니다: φ = 20 m 이웃 칸 쌍의 상관(잔차와 log d 각각), n_eff = n(1 − φeφx)/(1 + φeφx), 구간 폭 × √(n/n_eff). Breakdown의 실제 계산(중앙값 · 칸 정의 · φ 계산 방식)과 다를 수 있습니다.
  - “베리오그램 공분산”은 매번 잔차로 지수 베리오그램을 적합해 Σ를 세우고 (XᵀX)⁻¹XᵀΣX(XᵀX)⁻¹로 분산을 낸 것입니다.
  - 결과(포함률): a 20 m(1칸) 78 · 92 · 96%, 40 m(2칸) 66 · 88 · 94%, 60 m(3칸) 44 · 80 · 93%, 100 m(5칸) 33 · 65 · 92%.
  - “까닭”은 가설입니다. 예시 시뮬레이션이 Breakdown 합성 시험(2칸 넘으면 약 80%)과 같은 모양을 보였다는 뜻이지, Breakdown의 원인을 확인한 것은 아닙니다.
- **크리깅(9 · 10쪽):** 9쪽은 참 모수(a 50 m · σ 5 · nugget 2 dB)를 안다고 두고, 10쪽은 5쪽 적합값으로 크리깅했습니다. 표의 “σ_K 예측”은 √(크리깅 분산 + nugget)입니다.
- **교차 검증(11쪽):** 도로 칸 5겹. 블록은 100 m · 200 m 네모를 무작위로 다섯 겹에 배정했고 버퍼는 두지 않았습니다. “새 지역”은 독립으로 뽑은 다른 장에 이 지역의 크리깅 보정을 그대로 적용한 결과이며, 편향 보정만 하면 5.4 dB입니다.
- **블록 크기 · 버퍼(12쪽):** “블록은 상관 범위보다 상당히 크게, 버퍼는 상관 범위 정도”는 blockCV 패키지 문서가 Roberts 외(2017)를 요약한 문장을 따랐습니다. “300~500 m”는 이 덱의 예시입니다.
- **sill = de-biased RMSE²(4쪽):** 잔차가 정상(stationary)이고 평균을 뺀 분산일 때의 관계입니다. Breakdown의 판정 숫자는 중앙값 중심이라 조금 다를 수 있습니다.
- **38.901 상관 거리(3쪽):** 모델 음영(SF)의 값입니다. 우리 잔차(sim − meas)의 상관 거리는 시뮬 음영 · 실측 음영 · 모델 구조 오차가 섞인 것이라 실측에서 따로 재야 합니다.
- **Gudmundson(3쪽):** 원문은 유료라 초록과 2차 문헌으로 내용(지수 근사, 큰 셀은 잘 맞고 마이크로셀은 덜 맞음)을 확인했습니다. 논문 속 측정값(상관 거리 수치)은 확인하지 못해 쓰지 않았습니다.

## 출처

- M. Gudmundson, “Correlation model for shadow fading in mobile radio systems,” Electronics Letters 27(23), 2145–2146, 1991 (doi:10.1049/el:19911328)
- 3GPP TR 38.901, §7.4.4 (shadow fading 자기상관: 지수 함수, ITU-R P.1816 인용), Table 7.5-6 (SF 상관 거리: UMi-Street Canyon 10/13/7 m, UMa 37/50/7 m, RMa 37/120/120 m, Indoor-Office 10/6 m)
- G. Matheron, “Principles of geostatistics,” Economic Geology 58(8), 1246–1266, 1963
- N. Cressie, Statistics for Spatial Data, revised ed., Wiley, 1993 (3장 크리깅)
- C. S. Bretherton 외, “The effective number of spatial degrees of freedom of a time-varying field,” J. Climate 12, 1990–2009, 1999 — 식 (31)
- C. E. Rasmussen, C. K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006 (GP 회귀 = 크리깅)
- D. R. Roberts 외, “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” Ecography 40(8), 913–929, 2017
- blockCV R 패키지 문서 `cv_spatial` (Roberts 외 2017 요약: 블록 · 버퍼 크기)
- scikit-learn 문서: `Matern` (ν = 0.5는 absolute exponential 커널)
- 지수 베리오그램 실용 범위 3a(sill 95%): SAS VARIOGRAM 절차 문서
- 관련: Breakdown 화면 설명서 — n_eff 식, 열린 질문 Q-AM-49 (c₁ 구간 포함률 약 80%)
