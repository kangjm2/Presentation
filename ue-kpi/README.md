# UE KPI로 읽는 RAN (XCAL5 기준)

UE DM 툴(Accuver XCAL5)이 수집하는 5G NR KPI의 의미를 다룹니다. 이어서 그 KPI를 **DU 최적화**(링크 적응·스케줄러·핸드오버 파라미터)와 **RU 배치**(틸트·방위각·출력·추가 배치)에 활용하는 방법을 설명합니다. 10분 세미나 자료이고 12장이며, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/FYSGgG8vvKoYbWVVfCUUPY, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/KhmQgNs6zYY9qmTyPRFDfk
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- KPI 값이 어떻게 만들어지는지(칩셋 로그 → DM 툴 → 후처리, KPI별 집계 방법)는 [`ue-kpi-pipeline`](../ue-kpi-pipeline/) 덱에 있습니다.
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py ue-kpi`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | dm | UE DM 툴이 수집하는 것, OSS 카운터와의 차이 | 0:50 |
| 3 | map | KPI 여섯 묶음과 층 구조 (무선 → 링크 적응 → 자원 → 체감) | 0:50 |
| 4 | radio | SS-RSRP · SS-RSRQ · SS-SINR · CSI-RS 측정의 정의와 해석 | 0:55 |
| 5 | beam | 셀·빔 식별: PCI, NR-ARFCN, SSB 인덱스, 이웃 셀, TA | 0:50 |
| 6 | linkadapt | 링크 적응 루프: CQI · RI · PMI → MCS → BLER · OLLA | 0:55 |
| 7 | throughput | 처리량 분해 (RB × 슬롯 비율 × 레이어 × MCS × (1−BLER)), 층별 처리량 | 0:55 |
| 8 | mobility | 핸드오버 타이밍 (A3 · TTT), 측정 이벤트, 실패 유형 | 0:55 |
| 9 | du | KPI 패턴 → 의심 원인 → DU 파라미터 | 1:00 |
| 10 | ru | RSRP × SINR 네 칸 진단, 오버슈팅 · 빔 방향 · UL 한계 · 신규 RU | 1:00 |
| 11 | workflow | 계획 → 수집 → 분석 → 판단 → 조치·검증 | 0:50 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 클러스터]`

참고할 점:
- KPI 이름은 3GPP 용어 기준입니다. XCAL5 화면·필드 이름은 버전과 칩셋에 따라 다를 수 있으니, 실제 화면과 한 번 맞춰 보세요.
- 해석 임계값(예: RSRP −90/−110 dBm, SINR 0/20 dB)과 DU 파라미터 대응표는 경험치 예시입니다. 사업자 기준과 벤더 파라미터 이름에 맞춰 바꾸세요.
- 7쪽의 처리량 표는 가상의 예입니다.

## 출처

- 3GPP TS 38.215 (물리 계층 측정: SS-RSRP, SS-RSRQ, SS-SINR, CSI-RSRP/SINR 정의)
- 3GPP TS 38.133 (측정 보고 범위와 매핑)
- 3GPP TS 38.214 (CQI·MCS 표, CSI 보고)
- 3GPP TS 38.211 · 38.213 (PCI, SSB 빔 개수, Timing Advance)
- 3GPP TS 38.331 (측정 이벤트 A2/A3/A5/B1, RRC 메시지)
- 3GPP TS 38.306 4.1.2 (최대 전송률 근사식)
- Accuver, [XCAL5 제품 소개](https://pr.www.ipros.com/en/accuver/product/detail/2000550295/)
- CEPT ECC, [5G NR coverage 측정 지표 관련 보고서](https://docdb.cept.org/download/4059) (SS-RSRP, SINR, 처리량, CQI, BLER, MCS를 커버리지 지표로 정리)
