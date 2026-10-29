# 빠른 대리 모델: AI 전파 지도

레이 트레이싱(RT) 한 번은 정확하지만 느려서, 수천 번 돌려야 하는 최적화 · 민감도 · 보정에는 그대로 쓰기 어렵습니다. 이 자료는 그 사이를 메우는 **대리 모델(surrogate model)** 과 학습한 전파 지도를 다룹니다. 무엇이 있는지, 얼마나 빠르고 얼마나 틀리는지, 어디서 깨지는지, 우리 파이프라인 어디에 넣고 어떻게 검증할지를 정리했습니다.

다루는 내용은 다음과 같습니다.

- 왜 필요한가: 최적화 · Sobol 민감도 · 보정에 드는 실행 수와 시간
- 대리 모델의 개념과 두 종류
  - 파라미터 → KPI: 다항식 응답 표면, 가우시안 과정(GP, 크리깅)
  - 지도 → 지도: RadioUNet(IEEE TWC 2021)과 RadioMapSeer 데이터
- 정확도와 일반화 위험: RadioUNet의 조건별 오차, ICASSP 2023 대회에서 처음 보는 도시로 시험한 결과
- 그 뒤의 흐름: PMNet, Sionna 미분 가능 RT(대리 모델 없이 기울기로 보정), NeRF²(신경 전파장)
- 우리 판으로 만들 때의 입력 · 출력, Sionna RT로 학습 데이터를 만드는 비용
- 계산 예시(numpy): 가짜 "비싼 모델"에서 RT 20회 + GP로 961회 격자 탐색을 대신해 보기, 실행 수에 따른 오차, 속도
- 두 층 검증(대리 오차 + RT 오차), 능동 학습, 파이프라인에 넣는 곳(twin-optimization · sensitivity-analysis · 보정)

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/RbwTW9UQRZyP961tq3rtMP, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/BwFq8yCSsvgTP1uCL7p7fj
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py surrogate-model`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`ray-tracing`](../ray-tracing/): 10쪽 학계 ②(미분 RT · 신경 대리 모델 · 신경 전파장)
  - `twin-optimization`: 최적화 루프 (같은 시리즈에서 함께 만드는 덱)
  - `sensitivity-analysis`: 민감도 분석 · Sobol 지수 (같은 시리즈에서 함께 만드는 덱)
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 방법
  - [`dt-breakdown`](../dt-breakdown/): Breakdown 화면, σ_sim(시뮬 잡음) 미측정
  - [`debiased-rmse`](../debiased-rmse/): 우리 보정 전 de-biased RMSE 6.41 dB

## 구성 (≈ 11분 15초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 실행 수와 시간: 격자 탐색 27,000회 · Sobol 12,000회 (30 s/회 가정), WinProp 1회 시간 | 0:50 |
| 3 | idea | 대리 모델의 정의, 흐름(설계 → RT N회 → 학습 → 질의 → 확인), 두 종류 | 0:45 |
| 4 | classic | 다항식 응답 표면 · GP(크리깅): 1차원 단면 그림(표본 5개, ±2σ 띠) | 0:50 |
| 5 | radiounet | RadioUNet 입력 · 출력, RadioMapSeer(700 지도 × 80 Tx), 조건, 속도 | 0:55 |
| 6 | generalize | 조건별 오차 1.6 · 2.3 · 3.1 · 5.9 dB, ICASSP 2023 대회(이스탄불 시험), 일반화 위험 넷 | 0:55 |
| 7 | later | 대회 · PMNet · Sionna 미분 RT · NeRF², 고르는 기준 | 0:50 |
| 8 | io | 우리 판의 입력 채널 다섯, 출력, 데이터 비용과 나누기 규칙 | 0:50 |
| 9 | toy-setup | 계산 예시 ①: 가짜 비싼 모델(틸트 · 방위각 → 목표 구역 SINR 중앙값), SINR 지도 | 0:50 |
| 10 | toy-map | 계산 예시 ②: 정답(961회) vs GP(20회) vs 오차 지도, 고른 최적점 | 0:50 |
| 11 | toy-curve | 계산 예시 ③: 실행 수에 따른 오차(다항식 · GP 무작위 · GP 능동 학습), 1회 시간 | 0:55 |
| 12 | validate | 두 층 오차(대리 + RT 6.41 dB), 검증 순서, 능동 학습, σ_sim | 0:55 |
| 13 | pipeline | twin-optimization · sensitivity-analysis · 보정에 넣는 곳, 쓰지 않는 곳, 기록할 것 | 0:50 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 4쪽(고전 대리 모델 — 9~11쪽 예시가 같은 내용을 보여 줌)과 7쪽(그 뒤의 흐름)을 백업으로 돌리세요. 약 9분 35초가 됩니다.
- 최적화보다 전파 지도 자체에 관심 있는 청중이면 4쪽 대신 11쪽을 백업으로 돌리세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 2쪽 `[우리 장면 1회 실측 시간을 채울 것]` — 우리 Sionna RT 장면 한 번(RadioMapSolver 등)의 실제 시간. 정하면 2쪽 표와 8쪽 데이터 비용의 "30 s/회" 가정도 바꾸세요(생성기의 `T_ASSUME`).

참고할 점:
- **2쪽 실행 수:** 30 s/회는 가정입니다. 격자 탐색은 섹터 3개 × (틸트 6단 × 방위각 5단) = 30³ = 27,000회, Sobol은 Saltelli 설계 N(k + 2)회(N 1,000, 입력 10개 → 12,000회), 보정 300회는 예입니다. "Sionna RT 1회 수 s ~ 수 분"은 장면 · 광선 수 · 반사 차수에 따른 일반적 경향입니다.
- **RadioUNet 수치(2 · 5 · 6 · 8 · 11쪽):** 논문 본문과 Fig. 3 표에서 옮겼습니다.
  - 속도: WinProp DPM이 Intel Core i7-8750H CPU에서 "약 1 s 차수", IRT2 "10 s 차수", IRT4 "10² s 차수", RadioUNet은 "10⁻³ ~ 10⁻² s 차수"(GPU Nvidia Quadro GP100). 학습 시간은 빠진 숫자라고 논문이 밝힙니다. 모두 차수(order of magnitude) 표현입니다.
  - 6쪽 dB 값은 RadioUNet_C(측정 입력 없는 판)의 회색 단계 RMSE에 논문이 밝힌 환산 "dB RMSE = 회색 단계 RMSE × 80"을 곱한 값입니다: 같은 시뮬(DPM) 0.02 → 1.6 dB, IRT4로 적응 0.0292 → 2.3 dB, IRT4 그대로(zero-shot) 0.0384 → 3.1 dB, 건물 4개 빠진 지도(결정적 DPM) 0.0742 → 5.9 dB. 경로손실 문턱 −127 dB로 잘라 낸 값입니다.
  - RadioMapSeer 조건: 5.9 GHz, 10 MHz, Tx · Rx 1.5 m, 건물 25 m(차량 간 통신 가정), 지도 분할 500 / 100 / 100.
- **ICASSP 2023 대회(6 · 7쪽):** 학습 데이터 RadioMap3DSeer(701 지도 × 옥상 Tx 80곳 = 56,080, WinProp IRT, 수신 높이 1.5 m), 시험은 공개한 적 없는 이스탄불 84 지도(6,720). 주최 측이 "제출한 모든 방법에서 큰 성능 저하"를 관찰했다고 썼습니다. 1위 PMNet(H/8 × W/8) RMSE 0.0383은 0~1 회색 단계 값이며, RadioMapSeer와 문턱 · 눈금이 달라 ×80으로 dB로 바꾸지 않았습니다. "약 10 ms"는 참가자들이 보고한 실행 시간입니다.
- **8쪽 데이터 비용:** 56,000 × 10² s ≈ 65일은 논문의 차수 값을 단순히 곱한 어림입니다(병렬화 없음). 우리 예(장면 200 × Tx 50 × 설정 4, 30 s/회 → 333 h)는 가정입니다.
- **계산 예시(4 · 9 · 10 · 11쪽):** 실제 장면 · 측정이 아닙니다. 생성기 안에서 numpy로 계산했습니다(시드 고정).
  - 모델: 2 km × 2 km, 10 m 화소, 경로손실 128.1 + 37.6 log₁₀ d[km](3GPP 거시 셀 식 형태, 2 GHz), 음영 σ 6 dB · 상관 50 m(좌표 정합 덱과 같은 조건), 섹터 높이 30 m, 수평 70° · 수직 10° 빔폭 · 감쇠 상한 25 / 20 dB(가정), 이웃 섹터 1개가 간섭, RE당 15.2 dBm + 이득 17 dBi(가정), 잡음 −125.2 dBm.
  - KPI: 반경 250 m 목표 구역의 SINR 중앙값. 정답 최적 틸트 2° · 방위각 36° · 17.3 dB.
  - 10쪽: 무작위 20점(시드 고정) GP — RMSE 0.86 dB, 최대 5.2 dB, 고른 최적점 (2°, 30°)의 정답 KPI 17.27 dB(차이 0.06 dB).
  - 11쪽: 무작위 설계 8벌 평균. GP 20회 1.06 dB · 50회 0.37 dB, 능동 학습(GP σ 최대점 추가) 20회 0.58 dB · 50회 0.16 dB, 2차 다항식은 80회에서도 1.61 dB.
  - GP는 RBF 커널, 길이 척도를 격자에서 주변 우도 최대로 고른 단순 구현입니다.
  - 시간(1회 약 2 ms vs GP 질의 약 1 µs, 약 2,000배)은 생성기를 실행한 컴퓨터에서 잰 값이라 실행마다 조금 다릅니다. 실제 RT와의 비교가 아닙니다.
  - 5쪽 그림은 개념도입니다(무작위 건물 지도에 간단한 가시선 계산).
- **12쪽 두 층 오차:** e_rt 6.41 dB는 우리 보정 전 de-biased RMSE(`debiased-rmse` 덱)입니다. 합 √(e_rt² + e_s²)는 두 오차가 독립이라는 가정의 계산이며, 실제로는 대리 오차와 RT 오차가 같은 곳(예: 복잡한 건물 뒤)에서 함께 커질 수 있습니다.

## 출처

- R. Levie, Ç. Yapar, G. Kutyniok, G. Caire, "RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks," IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 4001–4015, 2021 (doi 10.1109/TWC.2021.3054977, [arXiv 1911.09002](https://arxiv.org/abs/1911.09002)) — 3절(RadioMapSeer), Fig. 3, 5.1절(실행 시간)
- Ç. Yapar, F. Jaensch, R. Levie, G. Kutyniok, G. Caire, "The First Pathloss Radio Map Prediction Challenge," ICASSP 2023 ([arXiv 2310.07658](https://arxiv.org/abs/2310.07658)) — Table 1
- J.-H. Lee 외, "PMNet: Large-scale channel prediction system for ICASSP 2023 First Pathloss Radio Map Prediction Challenge," ICASSP 2023 · 관련 [arXiv 2211.10527](https://arxiv.org/abs/2211.10527)
- J. Hoydis 외, "Learning Radio Environments by Differentiable Ray Tracing," IEEE Trans. Mach. Learn. Commun. Netw., vol. 2, pp. 1527–1539, 2024 ([arXiv 2311.18558](https://arxiv.org/abs/2311.18558))
- X. Zhao, Z. An, Q. Pan, L. Yang, "NeRF²: Neural Radio-Frequency Radiance Fields," ACM MobiCom 2023 (doi 10.1145/3570361.3592527, [arXiv 2305.06118](https://arxiv.org/abs/2305.06118))
- J. Sacks, W. Welch, T. Mitchell, H. Wynn, "Design and Analysis of Computer Experiments," Statistical Science 4(4), 1989 · C. E. Rasmussen, C. K. I. Williams, *Gaussian Processes for Machine Learning*, MIT Press, 2006
- A. Saltelli, "Making best use of model evaluations to compute sensitivity indices," Computer Physics Communications 145, 2002 (N(k + 2) 설계)
- 3GPP TR 36.942 4.5.2절 거시 셀 전파 모델(128.1 + 37.6 log₁₀ R, 2 GHz) — 계산 예시의 경로손실 식 형태
