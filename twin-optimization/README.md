# 트윈으로 최적화하기: CCO · MLB · MRO와 what-if

네트워크 디지털 트윈을 실제 망 최적화에 쓰는 법을 정리한 자료입니다. 3GPP SON 사용 사례 세 가지(CCO · MLB · MRO)에서 무엇을 바꾸고 무엇을 보며 트윈이 무엇을 그려야 하는지 살펴봅니다. 이어서 트윈 안에서 후보를 고르는 what-if 루프와 탐색 방법(격자 · 탐욕 · 베이즈 최적화 · Pareto)을 다룹니다. 마지막으로 트윈의 오차(σ)가 어떤 이득까지 믿을 수 있게 하는지 봅니다. 핵심은 **절대 정확도와 상대(차이) 정확도의 구분**입니다.

다루는 내용은 다음과 같습니다.

- 왜 실망보다 트윈에서 먼저 시험하나, 그리고 이 시리즈에서 이 덱의 위치
- SON 세 사용 사례: 바꾸는 것 · 보는 KPI · 트윈이 그릴 것 (TR 36.902 · TS 28.313 · TS 38.300)
- CCO 예시 계산: 셀 3개 장난감 지역에서 틸트에 따라 구멍과 겹침이 달라지는 모습
- MLB(CIO와 A3 조건, 경계 이동)와 MRO(too-late · too-early · wrong-cell · ping-pong)
- what-if 루프: 후보 → 트윈 → 목적 함수 → 고르기 → 단계적 적용 → PM · DT 검증 → 보정
- 목적 함수와 제약: 커버리지 % · 겹침 % · 가중치, 면적 가중과 트래픽 가중
- 탐색: 격자 · 탐욕(좌표 하강), 베이즈 최적화(GP + EI), 강화 학습은 짧게
- 여러 목표: Pareto 앞선, 가중 합과 제약
- 신뢰: σ_Δ = σ√(2(1 − ρ)), +0.5 dB를 보는 데 필요한 n_eff, 공통 오차와 설정 따라 바뀌는 오차의 예시 계산
- 실망 적용과 검증: 되돌릴 기준 · 단계적 적용 · 비교군(A/B), TS 28.313 C-SON CCO 절차, O-RAN rApp · SMO

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/VUyEAvjuMdF8xXZiu4fA4w, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/NBkPd1M7wC6GiVx19N7ASX
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py twin-optimization`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`debiased-rmse`](../debiased-rmse/): σ 6.41 dB(우리, 보정 전) · 2.57 dB(영국, 보정 후)
  - [`dt-breakdown`](../dt-breakdown/): n_eff(유효 표본 수) · 패턴 몫
  - [`sim-real-alignment`](../sim-real-alignment/): 보정 방법, 망 설정(틸트 · 방위각) 입력
  - [`coord-registration`](../coord-registration/): 비교 전 좌표 정합
  - [`upper-layers`](../upper-layers/): RLF 판정(T310 · N310)과 MRO 세 유형
  - [`antenna-basics`](../antenna-basics/): 틸트와 수직 빔
  - [`network-digital-twin`](../network-digital-twin/): 트윈 동향
  - [`surrogate-model`](../surrogate-model/): 실행이 비쌀 때 대리 모델 위에서 탐색
  - [`twin-vv`](../twin-vv/): 용도별 합격선 (상대 비교 what-if)

## 구성 (≈ 10분 55초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 실망 시험 vs 트윈에서 먼저, 시리즈에서의 자리 | 0:45 |
| 3 | son | SON 세 사용 사례 표: 바꾸는 것 · 보는 것 · 그릴 것 · 3GPP 문서 | 0:55 |
| 4 | cco | CCO 예시 지도 두 장(기준 vs 트윈이 고른 설정), 28.313 CCO 파라미터 · PM | 0:50 |
| 5 | mobility | A3 조건과 CIO, 경계 이동 예시(83 m), MRO 네 유형, 트윈에 필요한 것 | 0:55 |
| 6 | loop | what-if 루프(안쪽 트윈 · 바깥 실망 · 되먹임) | 0:50 |
| 7 | objective | 목적 함수 J = 커버리지% − λ · 겹침%, 예시 결과, 가중 · 기준값 주의 | 0:45 |
| 8 | grid | 격자 열지도와 탐욕 경로, 손잡이가 늘면 몇 번, 지역 최대 9개 | 0:45 |
| 9 | bo | 베이즈 최적화: 1-D GP · EI 그림, 3-D 수렴 비교(BO 중앙값 12번 vs 격자 2,197번) | 0:55 |
| 10 | pareto | 커버리지 vs 겹침 산점도와 Pareto 앞선, 가중 합 · 제약 해 | 0:45 |
| 11 | trust | σ_Δ(ρ) 곡선, +0.5 dB를 보는 데 필요한 n_eff | 0:50 |
| 12 | commonmode | 예시 계산: 공통 오차는 차이에서 지워지고, 틸트 기록 3°는 이득의 방향까지 바꾼다 | 0:50 |
| 13 | rollout | 실망 적용 · 검증, TS 28.313 C-SON CCO 절차, O-RAN rApp | 0:50 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 2쪽(왜 트윈에서 먼저)과 10쪽(Pareto)을 백업으로 돌리세요. 약 9분 25초가 됩니다.
- 청중이 SON에 익숙하면 3쪽을 짧게(30초) 넘기고 11 · 12쪽에 시간을 더 주세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 7쪽 기준값(−105 dBm · 3 dB · λ = 1)을 실제 운영 기준으로 바꾸려면 생성기의 `THR`, `OVDB`, `LAM`을 바꾸고 다시 생성

참고할 점:
- **예시 계산(4 · 5 · 7~12쪽)은 실제 망이 아닙니다.** 생성기(numpy, 시드 고정)로 계산한 장난감 예입니다.
  - 지역: 2.4 × 1.6 km, 20 m 칸. 셀 3개(A 서쪽 → 동, B 동쪽 → 서, C 남쪽 가장자리 → 북), 높이 30 m, 단말 1.5 m.
  - 경로 손실: 128.1 + 37.6 log₁₀ d[km] (TR 36.814 매크로 식을 빌림).
  - 안테나: 3GPP식 포물선 패턴(수평 65° · 수직 10°, 이득 14 dBi). 상한 값은 가정입니다.
  - 송신: RE당 46 dBm − 10 log 1200.
  - 음영: 셀마다 σ 6 dB, 상관 거리 약 50 m의 장.
  - 기준값: 커버리지 RSRP ≥ −105 dBm, 겹침 = 1 · 2위 차이 3 dB 이하, J = 커버리지% − 1 × 겹침%. 모두 예시이며 표준 값이 아닙니다.
- **예시 결과:**
  - 기준 (6°, 6°, 6°): 커버리지 75.9% · 겹침 22.1% · J 53.8
  - 격자 최대 (2°, 3°, 12°): 77.8% · 18.2% · J 59.6. C의 최적이 범위 끝(12°)이라 범위 제약이 걸린 해입니다.
  - SINR 하위 5%(전 부하 가정)는 −0.8 → 0.0 dB입니다.
- **탐색 비교(9쪽):** 기준은 “3-D 격자 최대에서 0.5 %p 안”입니다.
  - BO: Matérn 5/2 GP(길이 척도는 주변 우도 최대), EI(ξ = 0.01), 무작위 시작점 4개, 후보 0.5° 격자. 시드 20개 중앙값 11.5번(슬라이드 12번), 최대 19번
  - 탐욕: (6, 6, 6)에서 출발해 64번. 출발점 2,197곳 전체로는 54%만 최대에 닿습니다(지역 최대 9개).
  - 무작위: 시드 60개 중앙값 79.5번(슬라이드 80번). 18개는 150번 안에 닿지 못했습니다.
  - 이 숫자는 이 장난감 표면에 대한 것이며, BO가 늘 이만큼 빠르다는 뜻이 아닙니다.
- **MLB(5쪽):** 경계 이동 83 m는 음영 없이 A–B 직선 위에서 계산했습니다. 면적 몫 36.7 → 44.5%는 음영을 포함한 지역 전체 값으로, 균일 사용자를 가정하면 부하 몫이 됩니다. 히스테리시스 · TTT는 무시했습니다.
- **신뢰(11 · 12쪽):**
  - σ_Δ = σ√(2(1 − ρ))는 두 오차의 분산이 같다는 가정의 일반식입니다. 필요한 n_eff = (2σ_Δ / 0.5)²은 칸 오차가 n_eff개만큼 독립이라는 가정입니다.
  - “차이 예측이 절대 예측보다 정확하다”는 오차가 설정 사이에 공통일 때의 **일반적 경향**으로 제시했습니다. 늘 성립하는 것은 아닙니다.
  - 12쪽 “실제 망”은 트윈 음영과 상관 0.5인 다른 음영 장(칸별 오차 σ 6.0 dB)에, A · B의 실제 틸트가 기록보다 3° 작은 상황입니다.
  - 평균 편향 −5.69 dB는 영국 사례(arXiv 2510.09478)의 보정 전 평균 오차를 빌렸습니다. 셀 C는 6°로 고정하고 A · B 169개 조합에서 골랐습니다.
  - 결과(J 예측 이득 → 실제): ① +0.2 → −0.3, ② +0.2 → −0.3(기준 커버리지 예측 61.1% vs 실제 79.3%), ③ +3.8 → −0.7.
- **표준 문서에서 확인한 것과 일반적 용법:**
  - TS 28.313의 CCO 제어 파라미터 다섯 가지(최대 송신 전력 · 최대 EIRP · 커버리지 모양 · 디지털 틸트 · 디지털 방위각)와 CCO PM 목록(SSB별 SS-RSRP 분포 등)은 표 7.2.3.2.1-1 · 7.2.3.3.1-1에서 확인했습니다.
  - MRO 목표(HO 실패율)와 PM(too-late · too-early · wrong-cell 횟수, 시스템 간 ping-pong 횟수)은 28.313 7.1.2절에서 확인했습니다.
  - 커버리지 “구멍 · 겹침(pilot pollution) · 오버슈트”는 업계에서 흔히 쓰는 분류이며, 표준 본문에서 이 낱말을 확인하지는 못했습니다.
  - ping-pong의 “짧은 시간 안에 A → B → A” 정의는 일반적 용법입니다.
  - 3쪽의 MLB 손잡이 가운데 TR 36.902 §4.6.5.2가 명시하는 것은 “HO trigger threshold”입니다. CIO · 재선택 오프셋은 이를 구현하는 흔한 손잡이로 적었습니다.
- **MLB가 CIO를 키우면 MRO 실패가 늘 수 있다(5쪽):** SON 기능 간 충돌로 흔히 거론되는 일반적 경향입니다.
- **적용 · 검증(13쪽):** 단계적 적용 · 비교군 · 되돌릴 기준은 일반적 운영 방법으로 제시했습니다. 기간 · 기준 수치는 정하지 않았습니다.

## 출처

- 3GPP TR 36.902, *Self-configuring and self-optimizing network (SON) use cases and solutions* (Rel-9). §4.1 CCO, §4.5 MRO(too late · too early · wrong cell · 불필요한 HO), §4.6 MLB(§4.6.5.2 HO trigger threshold) — [itecspec 요약](https://www.itecspec.com/3gpp/36.902/s/4), [ETSI TR 136 902](https://www.etsi.org/deliver/etsi_tr/136900_136999/136902/09.00.00_60/tr_136902v090000p.pdf)
- 3GPP TS 32.500, *Self-Organizing Networks (SON); Concepts and requirements* — [itecspec](https://itecspec.com/3gpp/32.500/s/root)
- 3GPP TS 28.313, *Self-Organizing Networks (SON) for 5G networks*. §7.1.2 MRO(목표 · 파라미터 · PM), §7.1.5 LBO, §7.2.3 C-SON CCO(파라미터 표 7.2.3.2.1-1, PM 표 7.2.3.3.1-1), §8.3.4 CCO 절차 — [itecspec](https://itecspec.com/3gpp/28.313/s/8)
- 3GPP TS 38.300 §15.5.1(MLB), §15.5.2(MRO: too late · too early · wrong cell 정의) — [itecspec 15.5.2.2.2](https://itecspec.com/3gpp/38.300/s/15.5.2.2.2)
- 3GPP TS 38.331 §5.5.4.4 Event A3(Mn + Ofn + Ocn − Hys > Mp + Ofp + Ocp + Off, Ocn = cellIndividualOffset) — [itecspec](https://itecspec.com/3gpp/38.331/s/5.5.4.4)
- J. Snoek, H. Larochelle, R. P. Adams, “Practical Bayesian Optimization of Machine Learning Algorithms,” NIPS 25 (2012), [arXiv:1206.2944](https://arxiv.org/abs/1206.2944). EI 획득 함수, ARD Matérn 5/2 커널
- B. Shahriari, K. Swersky, Z. Wang, R. P. Adams, N. de Freitas, “Taking the Human Out of the Loop: A Review of Bayesian Optimization,” *Proc. IEEE* 104(1), 148–175 (2016), doi:10.1109/JPROC.2015.2494218
- O-RAN SC Non-RT RIC 문서: SMO의 일부, rApp 호스팅, R1 인터페이스, A1 정책 — [docs.o-ran-sc.org](https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric/en/latest/overview.html)
- 3GPP TR 36.814 Annex A (매크로 경로 손실 128.1 + 37.6 log₁₀ R, 예시 계산에 빌림)
- “Site-Specific RIS Deployment in Cellular Networks via Calibrated Ray Tracing,” arXiv:2510.09478 (2025): 평균 오차 −5.69 dB, σ 5.71 → 2.57 dB (debiased-rmse 덱)
