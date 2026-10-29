# 민감도 분석과 불확실성: 어떤 입력이 결과를 가장 흔드나

보정을 시작하기 전에 두 가지를 묻는 자료입니다. 어떤 입력(틸트 · 방위각 · 전력 · 건물 높이 · 재질 · 좌표 …)이 RSRP를 가장 흔드는가(민감도), 그리고 입력을 모르는 만큼 RSRP는 칸마다 얼마나 흔들리는가(불확실성, σ_sim)입니다. 손으로 계산할 수 있는 장난감 RSRP 모형에서 OAT · Morris · Sobol 지수와 몬테카를로 전파를 numpy로 직접 계산해 보여 주고, Breakdown 화면에서 비어 있는 σ_sim · 도달점과 연결합니다.

다루는 내용은 다음과 같습니다.

- 입력 9개와 불확실 범위(가정), 장난감 모형(38.901 패턴 모양 · UMa PL1 · P.526 칼날 회절 · 프레넬 벽 반사)
- 하나씩 바꿔 보기(OAT) 토네이도와 그 함정: 상호작용이 있으면 명목점의 기울기가 순위를 잘못 알려 준다
- Morris 요소 효과(μ* · σ)로 거르기
- Sobol 지수: 분산 나누기의 뜻(Sᵢ · STᵢ), 계산 결과, Saltelli 설계와 비용 N(k + 2), 대리 모델
- 몬테카를로 전파: 거리별 RSRP 분포와 σ_sim, 거리별 STᵢ 지도
- Breakdown 도달점과 잇기: σ_sim의 세 종류(수치 잡음 · 입력 불확실성 · 모형 구조)
- 결과 쓰기: 고정할 것(Factor fixing) · 잴 것 · 보정할 것, 동등 결과성(틸트 ↔ 전력)

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/WBo4jrEDhzcCRCYcJ2ZDB9, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/Led9tCoLJBfTXS54pjUqVo
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sensitivity-analysis`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`dt-breakdown`](../dt-breakdown/): σ_sim 미측정 · 도달점(reach) · 열린 질문
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 방법, OpenGERT 민감도(기하 > 재질), 재질 보정의 “답이 여럿”
  - [`coord-registration`](../coord-registration/): 좌표 어긋남은 보정이 아니라 정합으로
  - [`debiased-rmse`](../debiased-rmse/): 보정 전 · 후 오차 비교
  - [`sionna-rt-antenna`](../sionna-rt-antenna/): TR 38.901 소자 패턴(8 dBi · 65° · 30 dB)
  - [`surrogate-model`](../surrogate-model/): 실행이 비쌀 때 Sobol을 대리 모델 위에서 돌리기

## 구성 (≈ 11분 50초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 입력은 범위로만 안다: 160 m 칸 RSRP 분포(σ 4.5 dB), 두 질문, Breakdown 연결 | 0:50 |
| 3 | inputs | 입력 9개와 범위(가정), 어디서 틀어지나, 모형의 어느 자리에 들어가나 | 0:50 |
| 4 | toy | 장난감 모형의 식과 명목 RSRP 곡선(직접 · 반사 · 합), 대표 칸 160 m | 0:55 |
| 5 | oat | OAT 토네이도와 함정: 명목점에서 회절 0.0 dB, 건물 6.8 m면 6.1 dB | 0:55 |
| 6 | morris | Morris μ* · σ 산점도, 선형 · 얽힘 · 고정 후보, 비용 r(k + 1) = 200회 | 0:50 |
| 7 | variance | 분산 나누기: Sᵢ · STᵢ의 뜻, 조건부 평균 산점도, ΣSᵢ ≤ 1 ≤ ΣSTᵢ | 0:55 |
| 8 | sobol | 160 m 칸의 Sᵢ · STᵢ 막대(95% 구간)와 OAT 순위 비교 | 0:55 |
| 9 | cost | Saltelli 설계(A · B · A_B⁽ⁱ⁾), 추정식, 실행 수와 시간, 수렴, 대리 모델 | 0:55 |
| 10 | propagate | 몬테카를로 전파: 거리별 RSRP 띠와 σ_sim 곡선(0.9 ~ 4.8 dB) | 0:55 |
| 11 | bydist | 거리 9칸 × 입력 9개 STᵢ 열지도: 가까운 칸 · 전이 구간 · 먼 칸 | 0:55 |
| 12 | reach | σ_sim의 세 종류와 Breakdown 도달점, 잡음 상한 일반 식 예시 | 0:55 |
| 13 | calibrate | 고정 · 측정 · 보정 결정표, 틸트 ↔ 전력 동등 결과성 RMSE 지도 | 1:00 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 6쪽(Morris)과 9쪽(추정 · 비용)을 백업으로 돌리세요. 약 10분이 됩니다.
- 청중이 Sobol 지수에 익숙하면 7쪽(분산 나누기의 뜻)을 빼고 9쪽을 남기세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 셀]`
- 3쪽의 범위를 우리 장비 · 자료의 실제 오차로 바꾸기

참고할 점:
- **모든 그림과 수치는 예시입니다.** 생성기 안에서 numpy로 계산한 장난감 모형(시드 고정)의 결과이며, 실제 레이 트레이싱이나 실측이 아닙니다. 슬라이드 꼬리말에 “예시 · 장난감 모형”으로 적었습니다.
- **장난감 모형의 구성(4쪽):**
  - RSRP = 직접 경로와 벽 반사 경로의 전력 합(mW). 3.5 GHz, P0 11 dBm/RE, 빔 이득 17 dBi, 반사 경로 추가 손실 6 dB는 가정입니다.
  - 안테나: 3GPP TR 38.901 Table 7.3-1의 식 모양 `−min(12((θ−90°)/θ3dB)², SLA_V)`, `−min(12(φ/φ3dB)², A_max)`. 표준 소자 값은 θ3dB = φ3dB = 65°, SLA_V = A_max = 30 dB, 최대 8 dBi입니다(Sionna RT `v_tr38901_pattern` 소스로 확인). 이 덱에서는 패널 빔을 흉내 내려고 **수직 빔폭만 10°로 좁혔습니다(가정).** 소자 65°를 그대로 쓰면 틸트 ±1°의 영향이 거의 사라집니다.
  - 거리 감쇠: 38.901 UMa LOS의 첫 식 PL1 = 28 + 22 log10 d + 20 log10 fc를 모양만 빌렸습니다. 브레이크포인트(PL2)와 NLOS 식은 쓰지 않았습니다.
  - 지붕 회절: ITU-R P.526-16 §4.1 식 (31) J(ν) = 6.9 + 20 log(√((ν−0.1)² + 1) + ν − 0.1), ν > −0.78. 건물(명목 6 m)은 UE 앞 30 m에 있다고 두었습니다.
  - 벽 반사: TE 프레넬 반사 계수. 전도율은 ITU-R P.2040 콘크리트 값 0.0462 · f^0.7822 ≈ 0.123 S/m(3.5 GHz)로 고정했습니다.
  - UE는 RU 방위 30° 방향의 칸들에 있습니다.
- **입력 범위(3쪽)는 모두 가정**이고 균등분포입니다. 회절 켬/끔은 반반으로 섞었습니다. 실제로 이것은 모형 선택이라 따로 비교하는 것이 맞습니다(12 · 13쪽). 반사 횟수 · 산란 · 식생은 모형에 넣지 않았습니다.
- **계산 방법:**
  - Sobol: Saltelli 설계(A · B · A_B⁽ⁱ⁾), 1차 지수는 Saltelli et al.(2010)의 식, 전체 지수는 Jansen(1999)의 식. 출력은 평균을 빼고 계산했습니다(1차 지수 추정의 잡음을 줄이려고). 160 m 칸은 N = 8,192(90,112회), 거리별 지도는 N = 4,096. 95% 구간은 붓스트랩 300회.
  - Morris: 4수준 격자, 궤적 20개(200회), μ*는 Campolongo et al.(2007)의 평균 절댓값.
  - 몬테카를로 전파: 거리마다 같은 입력 표본 4,000개.
  - 9쪽 “RT 30 s/회”는 시간 감을 주려는 가정입니다. 오른쪽 열은 N마다 20번 다시 뽑아 얻은 STᵢ(건물 높이)의 2.5 ~ 97.5% 범위입니다.
  - 13쪽: 참값 틸트 6.8° · 전력 +0.5 dB로 만든 가짜 실측에 칸마다 1 dB 잡음을 더하고, 다른 입력은 명목으로 안다고 가정했습니다. “최소 + 0.2 dB 안”을 골짜기 폭으로 표시했습니다.
- **도달 상한 식(12쪽):** r_max = σt² / √((σt² + σsim²)(σt² + σmeas²))는 서로 독립인 잡음을 가정한 상관 감쇠의 일반 식입니다. σt 6 dB · σmeas 2 dB는 예시 가정입니다. **Breakdown 설명서의 도달점 식과 같은지는 확인하지 못했습니다.** σ_sim을 수치 잡음 · 입력 불확실성으로 나누자는 것은 이 덱의 제안입니다.
- **“Factor fixing / Factor prioritization”:** Saltelli et al.의 Primer(2008)가 쓰는 두 설정 이름입니다. 각각 STᵢ ≈ 0이면 고정, Sᵢ로 순위를 매긴다는 뜻으로 썼습니다.
- **SALib 등 외부 라이브러리는 쓰지 않았습니다.** 추정식은 생성기에 직접 구현했습니다.

## 출처

- A. Saltelli, M. Ratto, T. Andres, F. Campolongo, J. Cariboni, D. Gatelli, M. Saisana, S. Tarantola, *Global Sensitivity Analysis: The Primer*, Wiley, 2008 (ISBN 978-0-470-05997-5) — Factor prioritisation · Factor fixing
- I. M. Sobol′, “Sensitivity analysis for non-linear mathematical models,” *Mathematical Modeling & Computational Experiment* 1, 407–414 (1993; 러시아어 원문 1990)
- I. M. Sobol′, “Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates,” *Mathematics and Computers in Simulation* 55(1–3), 271–280 (2001)
- T. Homma, A. Saltelli, “Importance measures in global sensitivity analysis of nonlinear models,” *Reliability Engineering & System Safety* 52, 1–17 (1996) — 전체 효과 지수
- M. D. Morris, “Factorial sampling plans for preliminary computational experiments,” *Technometrics* 33(2), 161–174 (1991)
- F. Campolongo, J. Cariboni, A. Saltelli, “An effective screening design for sensitivity analysis of large models,” *Environmental Modelling & Software* 22, 1509–1518 (2007) — μ*
- M. J. W. Jansen, “Analysis of variance designs for model output,” *Computer Physics Communications* 117(1–2), 35–43 (1999)
- A. Saltelli, P. Annoni, I. Azzini, F. Campolongo, M. Ratto, S. Tarantola, “Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index,” *Computer Physics Communications* 181, 259–270 (2010)
- SALib 문서 — Sobol 표본 수 N(D + 2) (2차 지수까지 N(2D + 2))
- 3GPP TR 38.901, Table 7.3-1 (소자 패턴) · Table 7.4.1-1 (UMa PL1); Sionna RT 소스 `antenna_pattern.py` (`v_tr38901_pattern`: 65° · 30 dB · 8 dBi)
- ITU-R P.526-16 (2025), §4.1 식 (31) 칼날 회절 근사
- ITU-R P.2040 재질 계수(콘크리트 5.24 · 0.0462 · 0.7822, 벽돌 3.91) — Sionna RT `radio_materials/itu.py`
- 관련: Breakdown 화면 설명서 — 도달점(Reachable α · r), σ_sim 미측정
