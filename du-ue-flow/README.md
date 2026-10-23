# DU와 UE의 대화

DU와 UE가 주고받는 전 과정을 따라가는 10분 세미나 자료입니다. O-RAN 구조에서 무선 쪽 대부분을 맡는 DU의 시점으로 셀 찾기부터 데이터 송수신, 연결 해제까지 다룹니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **찾기 · 접속 · 연결:** SSB → MIB → SIB1, 4단계 랜덤 액세스, RRC 연결과 F1(UE Context Setup) · 보안 · 재설정
- **데이터:** 패킷 하나가 SDAP → PDCP → F1-U → RLC → MAC → PHY를 지나는 길, 하향 DCI · PDSCH · HARQ, 상향 SR · BSR · 그랜트
- **유지 · 쉬기:** 여섯 개의 폐루프(링크 적응 · 재전송 · 빔 · TA · 전력 · BWP), DU 스케줄러와 FAPI, DRX와 연결 해제(INACTIVE)

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/45EqVS7dGqiVMtD4RkZdMz, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/8Y7nrxX5ZEkKc4SEyDdSFy
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py du-ue-flow`로 뷰어를 다시 만듭니다.
- 관련 덱: [`ran-architecture`](../ran-architecture/) (CU · DU · RU 분리) · [`ss-rsrp`](../ss-rsrp/) (SSB · 빔 · 측정) · [`m-plane-yang`](../m-plane-yang/) (O-DU의 RU 관리) · [`ue-kpi`](../ue-kpi/)

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | CU · DU · RU · UE 역할과 계층, 인터페이스(F1 · 7.2x · Uu), 여섯 단계, RNTI 변화 | 0:50 |
| 3 | search | ① 찾기: SSB → MIB → CORESET#0 PDCCH → SIB1, MIB · SIB1은 DU가 만든다, SIB1의 접속 설정 | 0:45 |
| 4 | rach | ② 접속: 4단계 랜덤 액세스와 F1 RRC 전달(UE · DU · CU 시퀀스) | 0:55 |
| 5 | setup | ③ 연결: NGAP · UE Context Setup · 보안 · RRCReconfiguration, DU가 내주는 것과 CU가 정하는 것 | 0:55 |
| 6 | datapath | ④ 데이터 경로: SDAP → PDCP → F1-U → RLC → MAC → PHY, TB 모양, 두 층의 재전송 | 0:50 |
| 7 | dl | ④ 하향 한 번: DCI 1_1 · PDSCH · K1 · NACK · 재전송 · 소프트 결합 (슬롯 그림) | 0:50 |
| 8 | ul | ④ 상향 한 번: SR → 작은 그랜트 → BSR → 그랜트 → 데이터, 5 ms 지연, configured grant | 0:50 |
| 9 | loop | ⑤ 여섯 폐루프: 링크 적응 · 재전송(OLLA) · 빔 · TA · 전력 · BWP | 0:50 |
| 10 | scheduler | ⑤ DU 스케줄러의 0.5 ms: 입력 → 우선순위 → PF → 배분 → FAPI, PF 예시 | 0:50 |
| 11 | idle | ⑥ 쉬기: DRX 타임라인, 비활성 감지 → 해제(F1AP), INACTIVE 재개 | 0:45 |
| 12 | summary | 정리 | 0:30 |

10분보다 짧게 하려면 9쪽(폐루프)이나 10쪽(스케줄러)을 질의응답용 백업으로 넘기세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 셀]`

참고할 점:
- **예시 값:** 30 kHz(슬롯 0.5 ms), TDD DDDSU, K1 = 4, SR → 데이터 10 슬롯, DRX 160 ms, PF 표의 속도는 설명용입니다. 실제 값은 망 설정과 장비에 따라 다릅니다.
- **대표 흐름:** 4쪽 · 5쪽 시퀀스는 TS 38.401의 초기 접속 흐름을 줄인 것입니다. NAS 인증 · 보안, 일부 응답 메시지는 하나로 묶거나 생략했습니다.
- **구현 사항:** 스케줄러 정책(우선순위 · PF), OLLA 보정 폭, DU의 비활성 판단 기준은 표준이 아니라 구현입니다. 10쪽 PF 지표와 표는 개념 설명용입니다.
- **헤더 크기:** 6쪽의 MAC · RLC · PDCP 헤더 크기는 SN 길이 등에 따른 대표값입니다. SDAP 헤더는 설정했을 때만 붙습니다.
- **용어:** “DU”는 O-RAN의 O-DU(DU-high + DU-low)를 가리킵니다. 10쪽의 FAPI 메시지는 DU-high(MAC)와 DU-low(High-PHY) 사이의 인터페이스입니다.

## 출처

- 3GPP TS 38.300 (NR 전체 구조 · L2) · TS 38.401 (NG-RAN 구조, CU · DU 분리, 8.1 초기 접속 흐름)
- 3GPP TS 38.473 (F1AP: F1 Setup의 gNB-DU System Information, Initial UL / DL RRC Message Transfer, UE Context Setup · Release, UE Inactivity Notification) · TS 38.425 (NR 사용자 평면 프로토콜, F1-U 흐름 제어)
- 3GPP TS 38.211 · 38.212 (DCI 형식) · 38.213 (셀 찾기 · CORESET#0, 랜덤 액세스, HARQ-ACK 시점, 전력 제어) · 38.214 (PDSCH · PUSCH 시점 K0 · K2, CSI · CQI 정의)
- 3GPP TS 38.321 (MAC: 랜덤 액세스, SR · BSR, HARQ, DRX, TA, configured grant, TCI MAC CE) · TS 38.322 (RLC) · TS 38.331 (RRC: MIB · SIB1, RRCSetup · RRCReconfiguration · RRCRelease)
- Small Cell Forum, 5G FAPI: PHY API Specification (SCF 222) · O-RAN WG4 7.2x 분할
