# 빔에서 SS-RSRP까지

RU의 안테나 배열과 빔 가중치, 채널을 거쳐 UE가 SS-RSRP를 측정 · 보고하기까지를 따라가는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **송신:** SSB 구조와 빔 스윕, TR 38.901 안테나 배열과 소자 패턴, 빔 가중치와 배열 인자, O-RAN의 빔 지정(beamId · 빔 조회 표), RE당 전력과 EIRP
- **채널:** 경로손실 · 섀도잉 · 다중 경로, 빔 이득을 경로의 출발 방향에서 읽는다는 것
- **수신:** TS 38.215의 SS-RSRP 정의(SSS RE 선형 평균), 빔별 값 → 셀 값 통합, L3 필터, 보고 범위
- **종합:** 17.8 dBm → −91 dBm 링크 버짓 폭포 그래프

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/AzBsYnen3EU6qyWfRe1GK2, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/HW3wDX1a2D1htpzCuPjWFC
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 용어 풀이: [`../sionna-rsrp-beam/glossary.md`](../sionna-rsrp-beam/glossary.md) — EPRE, 선형 평균, L3 필터, 빔 통합 등을 처음 보는 사람도 읽을 수 있게 정리
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py ss-rsrp`로 뷰어를 다시 만듭니다.
- 관련 덱: [`m-plane-yang`](../m-plane-yang/) (beamId · o-ran-beamforming) · [`sionna-rt-antenna`](../sionna-rt-antenna/) (배열 · 패턴 파라미터) · [`propagation-models`](../propagation-models/) (경로손실) · [`ue-kpi`](../ue-kpi/)

## 구성 (≈ 9분 30초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | 전체 지도: SSB → 빔 지정 → 가중치 → 배열 → 채널 → 측정, 단계별 dB와 개념식 | 0:50 |
| 3 | ssb | 송신 ①: SSB 격자(PSS · SSS · PBCH), SSS 127 RE, 빔 스윕(SSB 인덱스), 정의 | 0:50 |
| 4 | array | 송신 ②: TR 38.901 배열(M × N × P, TXRU 부배열), 소자 패턴 8 dBi · 65° | 0:55 |
| 5 | weight | 송신 ③: 빔 가중치 식, 배열 인자 그래프(0° · 30°), 이득 · 빔폭 · 부엽, 아날로그/디지털 | 0:55 |
| 6 | oran | 송신 ④: O-DU beamId → O-RU 빔 조회 표, 정적 · 동적(가중치 · 속성) 방식, 교정 | 0:50 |
| 7 | eirp | 송신 ⑤: 총 출력 → RE당 EPRE(ss-PBCH-BlockPower) → EIRP, UE의 경로손실 추정 | 0:50 |
| 8 | channel | 채널: 경로손실(UMa NLOS) · 섀도잉 · 다중 경로, 경로 출발 방향의 빔 이득 | 0:55 |
| 9 | measure | 수신 ①: 측정 절차, RE별 전력과 선형 평균, 기준점 · 다이버시티 | 0:50 |
| 10 | cell | 수신 ②: 빔 통합(상위 N개 선형 평균), L3 필터, 보고 범위 | 0:50 |
| 11 | budget | 종합: 링크 버짓 폭포 그래프, UE가 보는 경로손실, 민감도 | 0:55 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 셀]`

참고할 점:
- **예시 값:** 200 W, 100 MHz, 30 kHz, 8 × 8 × 2 배열, 500 m, 3.5 GHz, 빔별 RSRP 값은 설명용입니다. 실제 장비의 SSB 빔은 데이터 빔보다 넓게(이득을 낮게) 잡는 경우가 많고, 포트 · 편파 구성과 SSS 전력 부스팅도 장비 설정에 따라 다릅니다. 7쪽과 11쪽은 한 편파에 전체 전력을 싣는다고 단순화했습니다.
- **계산값:** 5쪽 배열 인자 그래프와 빔폭(12.7° · 14.8°)은 균일 선형 배열(N = 8, d = λ/2)을 직접 계산한 값입니다. 9쪽 RE별 전력은 세 경로 채널로 만든 예시이고, 선형 평균 −95 dBm과 dB 평균 −96.7 dBm도 그 데이터로 계산했습니다. 10쪽 셀 값 −94.7 dBm은 −93 · −95 · −97 dBm의 선형 평균입니다.
- **개념식:** 2쪽과 8쪽의 수식(SS-RSRP ≈ EPRE + 이득 − 손실, 수신 전력 ∝ |h · w|²)은 발표자가 정리한 개념식입니다. 4쪽 소자 패턴 식은 TR 38.901 Table 7.3-1의 수직 · 수평 감쇠를 한 줄로 합쳐 쓴 것입니다.
- **O-RAN 빔 지정:** 6쪽은 M-Plane 사양(ETSI TS 104 023 V12.01) 15.4절의 빔 조회 표 · 사전 정의 빔 · BEAM-TILT · 동적 빔포밍 설명을 따랐습니다. C-Plane 메시지 필드(beamId · 섹션 확장)의 세부 형식은 O-RAN CUS-Plane 사양에서 확인이 필요합니다.
- **L1 평균:** 9쪽의 시간 평균 방법은 UE 구현 사항이고, 표준은 측정 주기와 정확도 요구 사항(TS 38.133)만 정합니다.

## 출처

- 3GPP TS 38.215 5.1.1 SS-RSRP 정의 ([iTecSpec 사본](https://itecspec.com/3gpp/38.215/s/5.1.1)) · TS 38.211 7.4.3 (SS/PBCH 블록) · TS 38.213 4.1 (SSB 후보) · 7.1.1 (경로손실 기준)
- 3GPP TS 38.331 5.5.3.2 (L3 필터) · 5.5.3.3 (셀 품질 도출: absThreshSS-BlocksConsolidation · nrofSS-BlocksToAverage) · ServingCellConfigCommonSIB ss-PBCH-BlockPower
- 3GPP TS 38.133 10.1.6 보고 범위 (L3 −156 ~ −31 dBm, L1 −140 ~ −44 dBm) — [RAN4 CR 초안 (SS-RSRP · CSI-RSRP 보고 매핑)](https://3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_98bis_e/Inbox/Drafts/%5B98bis-e%5D%5B212%5D%20NR_CSIRS_L3meas_1/documents/R4-21XXXX%20revised%20CR%20on%20CSI-RSRP%20report%20mapping.docx)
- 3GPP TR 38.901 7.3 (안테나 배열 · 소자 패턴) · Table 7.4.1-1 (UMa 경로손실) · 7.5 (빠른 페이딩)
- ETSI, [TS 104 023 V12.01 (O-RAN M-Plane)](https://www.etsi.org/deliver/etsi_ts/104000_104099/104023/12.00.01_60/ts_104023v120001p.pdf) 15.4 (빔포밍 설정 · 사전 정의 빔 · BEAM-TILT · 동적 빔포밍) · 15.5 (안테나 교정)
- O-RAN WG4 CUS-Plane 사양 (C-Plane beamId · 빔포밍 섹션 확장) · 참고: [가중치 전송 방식 특허 (US 2021/0135722)](https://patents.justia.com/patent/20210135722)
