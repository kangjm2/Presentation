# L1 위의 세계: L2 · L3 입문

RSRP · SINR · BLER 같은 물리 계층(L1) KPI는 익숙하지만 RRC · PDCP · RLC 같은 말이 낯선 사람을 위한 상위 계층 입문 자료입니다. 다음 순서로 정리했습니다.

- L2(MAC · RLC · PDCP · SDAP), L3(RRC), NAS가 각각 하는 일과 자주 막히는 용어
- 연결 상태와 핸드오버 · 끊김이 일어나는 원리
- 접속 · 유지 · 이동 KPI가 어디서 나오는지

16장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/8gC5FPfaapZCrvWQoquCQq, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/MAEGzh46PiUZa7SC9eryuq
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py upper-layers`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`du-ue-flow`](../du-ue-flow/): DU와 단말 사이의 데이터 흐름
  - [`ran-architecture`](../ran-architecture/): CU · DU · RU 분리
  - [`ue-kpi-pipeline`](../ue-kpi-pipeline/): 단말 KPI가 만들어지는 과정, 접속 · 핸드오버 이벤트 정의
  - [`ue-kpi`](../ue-kpi/): KPI의 의미와 활용

## 구성 (≈ 14분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | 일곱 층(NAS · RRC · SDAP · PDCP · RLC · MAC · PHY)이 하는 일, 택배 비유, CU · DU 위치 | 0:55 |
| 3 | terms | 자주 막히는 용어 아홉 개: 평면 · SDU/PDU · SRB/DRB · 채널 세 종류 · RNTI · PDU 세션/QoS flow/5QI · AS/NAS · MAC CE · 타이머 | 0:50 |
| 4 | datapath | IP 패킷 하나가 SDAP → PDCP → RLC → MAC을 지나 두 슬롯의 TB가 되는 그림, 층별 헤더 크기 | 0:55 |
| 5 | mac | MAC의 여섯 가지 일(스케줄링 · HARQ · 다중화/LCP · SR/BSR/PHR · RA/TA · DRX/BWP), 업링크 한 번 보내기 | 0:55 |
| 6 | rlc | TM · UM · AM, HARQ vs ARQ 두 겹의 재전송, 최대 재전송 → RLF | 0:50 |
| 7 | pdcp | SDAP 매핑(IP 흐름 → QoS flow → DRB → RLC), PDCP의 번호 · 보안 · 압축 · 복제/폐기 | 0:55 |
| 8 | rrcstate | RRC 상태 IDLE · INACTIVE · CONNECTED와 상태를 바꾸는 메시지, 비교 표 | 0:55 |
| 9 | rrcmsg | 자주 보는 RRC 메시지(시스템 정보 · 연결 설정 · 보안 · 능력 · 재설정 · 측정 보고 · 재수립 · 해제/재개 · NAS 전달) | 0:55 |
| 10 | meas | 측정 설정 · 이벤트 A1~A5 · B1/B2, A3와 TTT 그림, 핸드오버 순서 | 1:00 |
| 11 | failure | RLF 판정(N310 · T310 · N311)과 재수립(T311), 그 밖의 RLF 원인, MRO 세 유형 | 1:00 |
| 12 | nas | RM · CM 상태와 RRC 상태의 짝, NAS 절차 다섯 가지, AMF · SMF · UPF | 0:55 |
| 13 | flow | 전원 켜기부터 첫 패킷까지 열 단계와 단계별 계층 | 1:00 |
| 14 | kpi | 상위 계층 KPI(접속성 · 유지성 · 이동성 · 무결성 · 사용률)와 카운터 예 | 0:55 |
| 15 | symptoms | “무선은 좋은데…” 증상별로 의심할 층과 먼저 볼 것 | 0:55 |
| 16 | summary | 층별 한 줄 정리, 다음 단계 제안 | 0:40 |

10분 안에 맞추는 방법:

| 백업으로 돌릴 슬라이드 | 발표 시간 |
|---|---|
| 3 · 6 · 9 · 15쪽 | 약 10분 25초 |
| 3 · 6 · 9 · 15쪽 + 7쪽 | 약 9분 30초 |

- 3쪽(용어)은 백업으로 돌려도 배포 자료로 나눠 주면 좋습니다.
- 9쪽(RRC 메시지)의 내용은 13쪽(열 단계)에 대부분 다시 나오므로 빼도 흐름이 끊기지 않습니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 로그]`

참고할 점:
- **헤더 크기(4쪽):** 일반적인 설정 기준의 대략값입니다. 실제 크기는 설정에 따라 다릅니다.

  | 층 | 헤더 |
  |---|---|
  | SDAP | 1 B |
  | PDCP | 데이터 2 B(12비트 SN) 또는 3 B(18비트 SN) + 선택 MAC-I 4 B |
  | RLC | UM 1~2 B · AM 2~3 B, 조각이면 위치(SO) 2 B 추가 |
  | MAC | 서브헤더 1~3 B |

  SDAP 헤더는 암호화하지 않습니다(TS 38.323).
- **기지국 배치(2쪽):** RRC · PDCP · SDAP를 CU, RLC · MAC · PHY를 DU에 두는 것은 3GPP의 CU-DU 분리(F1, 옵션 2) 기준입니다. 장비에 따라 한 박스에 모두 들어 있기도 합니다.
- **SDAP 매핑(7쪽):** 음성 = 5QI 1, 기본 데이터 = 5QI 9, 음성 DRB = RLC UM은 흔한 설정 예입니다. 매핑과 RLC 모드는 사업자 설정입니다.
- **A3 그림(10쪽):** 개념 그림입니다. 시간 축과 TTT 폭은 실제 비율이 아닙니다. 진입 조건 Mn + Ofn + Ocn − Hys > Mp + Ofp + Ocp + Off에서 주파수 · 셀별 오프셋(Ofn · Ocn · Ofp · Ocp)은 0으로 보고 그렸습니다.
- **A6 이벤트(10쪽 표):** 보조 셀 교체용이라 표에서는 뺐습니다(이웃 > SCell + 오프셋).
- **INACTIVE의 데이터(8쪽):** Rel-17부터 INACTIVE 상태에서도 소량 데이터 전송(SDT)이 가능합니다.
- **열 단계(13쪽):** 5G 단독(SA) 초기 등록 기준으로 단순화했습니다. 실제로는 기지국-코어 사이 NGAP 메시지(Initial Context Setup 등)가 사이에 끼고, 망 설정에 따라 순서가 조금 다를 수 있습니다. NSA(EN-DC)는 LTE RRC로 접속한 뒤 NR을 추가합니다.
- **KPI 정의(14쪽):** 계산식은 개념입니다. 카운터 이름(RRC.ConnEstabAtt · RRC.ConnEstabSucc)은 TS 28.552에 있습니다. 어떤 접속 원인을 넣고 빼는지, 재시도를 어떻게 세는지는 사업자 · 장비사 정의서를 따르세요.
- **증상별 진단(15쪽):** 일반적인 권장 순서입니다. 정답표는 아닙니다.

## 출처

- 3GPP TS 38.300: NR 전체 구조, 프로토콜 스택, 이동성
- 3GPP TS 38.321 (MAC) · TS 38.322 (RLC) · TS 38.323 (PDCP) · TS 37.324 (SDAP)
- 3GPP TS 38.331 (RRC): 상태, 메시지, 측정 · 이벤트(5.5), RLF(5.3.10), 재수립(5.3.7)
- 3GPP TS 38.304: idle · inactive 상태의 셀 선택 · 재선택
- 3GPP TS 23.501: 5G 시스템 구조, RM · CM 상태, QoS flow · 5QI
- 3GPP TS 23.502: 등록 · 서비스 요청 · PDU 세션 · 페이징 절차
- 3GPP TS 24.501: 5G NAS
- 3GPP TS 28.552 (성능 카운터) · TS 28.554 (5G 종단 KPI)
