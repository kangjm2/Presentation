# 시뮬레이션을 실측에 맞추는 법

Sionna 같은 채널 시뮬레이터(레이 트레이싱 · 시스템 레벨 시뮬레이터)의 결과를 실측에 가깝게 맞추려는 연구와 실무 노력을 정리한 자료입니다. **KPI · Scene · 망 설정 · 트래픽 · 단말**의 다섯 관점으로 나누고, 마지막에 방법 비교와 작업 순서로 묶었습니다. 16장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/NzRLtpiToboSdTdHFXFPvK, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/5t1L9KqeWiM8FqHzC6BpPy
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sim-real-alignment`로 뷰어를 다시 만듭니다.
- 관련 덱: [`sionna-rsrp-beam`](../sionna-rsrp-beam/) (빔 · 틸트를 Sionna에 넣는 법) · [`ue-kpi-pipeline`](../ue-kpi-pipeline/) (실측 KPI가 만들어지는 과정) · [`rf-modeling-tools`](../rf-modeling-tools/) (모델 보정 도구) · [`network-digital-twin`](../network-digital-twin/) · [`ray-tracing`](../ray-tracing/) · [`ue-antenna`](../ue-antenna/) (단말 다중 안테나와 DM 수집) · [`taylor-diagram`](../taylor-diagram/) (보정 결과를 σ · R · E′로 비교하는 그림)

## 구성 (≈ 13분)

| # | id | 관점 | 내용 | 시간 |
|---|----|------|------|------|
| 1 | cover | | 표지 | 0:20 |
| 2 | errmap | 개요 | 오차가 생기는 여섯 군데(KPI 정의 · 기하 · 재질/엔진 · 망 설정 · 트래픽 · 단말)와 오차 모양, 보정 순서 | 0:55 |
| 3 | sota | 개요 | 최근 연구의 수준 (영국 도시 Sionna 보정 −5.7 → −0.3 dB · Geo2SigMap · AIRMap · Atoll 경험 모델 · TU Wien) | 0:55 |
| 4 | kpi1 | KPI | KPI 계단(경로 이득 → RSRP → SINR → CQI/MCS/BLER → 처리량 → 이동성)과 계단마다 필요한 모델 | 0:50 |
| 5 | kpi2 | KPI | 오차 모양별 진단, 구역 집계, 보정 / 검증 데이터 분리, 지표 묶음 | 0:50 |
| 6 | scene1 | Scene | 기하: 데이터 출처별 장단점, OpenGERT 민감도(기하 > 재질), 식생 · 움직이는 물체 | 0:50 |
| 7 | scene2 | Scene | 재질 보정: 미분 가능한 레이 트레이싱 루프, 출발점(ITU-R P.2040), 답이 여럿, 베이지안 최적화 | 0:55 |
| 8 | scene3 | Scene | 전파 엔진 설정: 반사 횟수 · 회절 · 산란 · O2I · 광선 수 · 근접장 | 0:50 |
| 9 | netcfg | 망 설정 | 위치 · 방위 · 틸트 · 빔 · 전력 · 패턴 · 급전 손실, 추정값과 설정 이력 | 0:50 |
| 10 | traffic1 | 트래픽 | 부하 → 간섭 → SINR (이웃 부하 100% 1.9 dB ~ 0% 20 dB 예), OSS PRB 사용률, full buffer의 의미 | 0:55 |
| 11 | traffic2 | 트래픽 | 측정 시각 · 측정 단말 자신의 부하 · 사용자 분포 · 스케줄러 · 트래픽 모델 · 자동 보정 | 0:50 |
| 12 | ue1 | 단말 | 안테나 패턴 · 수신 안테나 수 · 높이 · 차량 손실(평균 9 dB) · O2I · 측정 정확도 | 0:50 |
| 13 | ue2 | 단말 | 단말 측정 · 이동성 · 링크 적응 흉내 내기, 하드웨어 인 더 루프 사례, 스캐너 vs 단말 | 0:50 |
| 14 | methods | 방법 | 미분 RT · BO · 경험 모델 튜닝 · ML 잔차 보정 · MDT 비교, 공개 데이터 · 도구 | 0:50 |
| 15 | workflow | 정리 | 7단계 작업 순서와 통과 기준 | 0:50 |
| 16 | summary | 정리 | 관점별 요약과 다음 단계 제안 | 0:40 |

10분 안에 맞추려면 5쪽(진단 · 검증) · 8쪽(엔진 설정) · 11쪽(트래픽 ②) · 13쪽(단말 ②)을 백업으로 돌리세요(약 9분 40초). 14쪽(방법 비교)까지 빼면 약 8분 50초입니다. 각 관점의 첫 장(4 · 6 · 7 · 9 · 10 · 12쪽)만으로도 흐름이 이어집니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 클러스터]`

참고할 점:
- **연구 수치(3쪽):** 각 연구의 측정 조건 · 주파수 · 환경이 달라 수치끼리 직접 비교할 수 없습니다. 영국 도시 결과는 이상치 구역을 제외한 70개 구역(10 m × 10 m, 표본 20개 이상) 기준입니다. AIRMap의 “시스템 KPI 오차 거의 0”은 논문 초록의 정성적 표현입니다.
- **부하 예시(10쪽):** 신호 −90 dBm, 이웃 2셀 각 −95 dBm, 잡음 −110 dBm으로 덱에서 직접 계산한 값입니다. 실제 간섭 셀 수 · 세기에 따라 다릅니다.
- **단말(12쪽):** 차량 침투 손실(평균 9 dB, 표준편차 5 dB, 금속 코팅 유리 20 dB)은 TR 38.901 7.4.3.2의 기본값입니다. Rel-19 휴대폰 안테나 · 가림 모델의 세부 수치는 규격 원문으로 확인하세요. 측정 정확도는 TS 38.133의 조건별 표를 따릅니다.
- **2026년 논문:** 일부 출처는 2026년 arXiv 사전 공개본이며 동료 심사 전일 수 있습니다.
- **작업 순서(15쪽):** 오차 크기와 단계 간 의존 관계에 따른 권장안입니다.

## 출처

Scene · 재질 보정
- J. Hoydis et al., “Learning Radio Environments by Differentiable Ray Tracing,” arXiv:2311.18558 (2023) — 재질 · 산란 · 안테나 패턴을 미분 가능 레이 트레이싱으로 학습, 실내 분산 MIMO 채널 측정으로 검증
- J. Hoydis et al., “Sionna RT: Differentiable Ray Tracing for Radio Propagation Modeling,” arXiv:2303.11103
- “Site-Specific RIS Deployment in Cellular Networks via Calibrated Ray Tracing,” arXiv:2510.09478 (2025) — 영국 도시 Sionna 디지털 트윈, 유전율 · 전도율 · 표면 산란 보정(전부 콘크리트로 시작, Adam 600스텝), 평균 오차 −5.69 → −0.32 dB, 표준편차 5.71 → 2.57 dB
- S. Tadik et al., “OpenGERT: Open Source Automated Geometry Extraction with Geometric and Electromagnetic Sensitivity Analyses for Ray-Tracing Propagation Models,” arXiv:2501.06945 (2025) — 재질 소변화는 영향 작고, 건물 높이 1 m · 위치 0.4 m 오차는 채널 통계를 크게 바꿈
- Y. Li et al., “Geo2SigMap: High-Fidelity RF Signal Mapping Using Geographic Databases,” arXiv:2312.14303 (2024) — OSM + Blender + Sionna, 측정 4.5만 개 · LTE 6셀 · 단말 3종, RSRP RMSE 6.04 dB
- TU Wien 연구 데이터: Material Parameter Estimation for Sionna RT (도시 철도 시나리오, 신호 세기 평균 절대 오차 최소화) — https://researchdata.tuwien.ac.at/records/ycw2e-xyw13
- ITU-R P.2040 (건물 재질의 전기적 특성)

KPI · 시스템 레벨
- A. Saeizadeh et al., “AIRMap: AI-Generated Radio Maps for Wireless Digital Twins,” arXiv:2511.05522 (2025) — 경로 이득 RMSE 4 dB 미만, 측정 20%로 보정, Sionna SYS와 결합 시 스펙트럼 효율 · BLER 오차 거의 0
- F. Rauf et al., “Quantifying System Level KPI Deviations of Sionna RT: Material and Near-Field Error Analysis Using a 5G OAI Testbed,” arXiv:2605.10352 (2026) — Sionna RT vs VNA 채널을 에뮬레이터로 OAI 기지국 + 상용 모듈에 주입, RSRP · PUCCH SNR · SINR 비교, 재질 불일치 · 근접장 전이가 오차 원인
- K. Koutlia et al., “Calibration of the 5G-LENA System Level Simulator in 3GPP reference scenarios,” arXiv:2205.03278 (2022)
- A. Fastenbauer et al., “Comparison of Large-Scale Fading Models with RSRP Measurements,” IEEE VTC2024-Spring — 1.855 GHz 저층 도심, 모든 모델이 손실 과소평가, 환경 정보 증가가 늘 정확도를 높이지 않음
- 오울루 대학 석사 논문, Atoll에서 드라이브 테스트로 전파 모델 보정 (3.5 GHz, 표준편차 6.446 dB) — https://oulurepo.oulu.fi/handle/10024/63585

트래픽 · 디지털 트윈 보정
- “Analysis and Optimization of Cellular Network with Burst Traffic,” arXiv:1408.3942 — 간헐 트래픽의 SINR이 full buffer보다 높고 부하가 오르면 수렴
- 3GPP TR 36.897 (평가 가정: FTP 모델 1, 자원 사용률 20 · 50 · 70%)
- A. Konar et al., ICC 2024 — RAN 디지털 트윈 보정을 지난 보정으로 웜스타트하는 순차 베이지안 최적화, 여러 사이트 1주일 시험
- 알토 대학 석사 논문, AI-driven digital twin for traffic prediction and calibration in 5G NR networks — 측정으로 트윈 보정, TCP 측정이 혼잡 모델링을 어렵게 함
- NVIDIA Aerial Omniverse Digital Twin FAQ — 릴리스 1.5부터 SS-RSRP로 EM 솔버 보정, 경로당 회절 1회

단말
- 3GPP TR 38.901 7.4.3 (O2I 건물 · 차량 침투 손실), Rel-19 개정(휴대폰 안테나 패턴 · 손 / 머리 가림) — S. Svendsen et al., “Realistic UE Antennas for 6G in the 3GPP Channel Model,” arXiv:2509.10357; “Overview of 3GPP Release 19 Study on Channel Modeling Enhancements to TR 38.901 for 6G,” arXiv:2507.19266
- 3GPP TS 38.133 (측정 정확도), TS 38.331 (측정 · 이동성 절차)

데이터 · 대규모 측정
- W. Wiedner et al., “The Vienna 4G/5G Drive-Test Dataset,” arXiv:2603.02638 (2026) — 스캐너 · 단말 로그, 추정 기지국 정보, 건물 · 지형 모델, 레이 트레이싱 보정용
- MDT 기반 전파 모델 보정과 위치 오차 필터링 — 말라가 대학 연구 (riuma.uma.es)
