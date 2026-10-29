# 망 데이터 파이프라인과 트윈 동기화: CM · PM · FM

네트워크 디지털 트윈이 실제 망과 같은 상태를 유지하려면 어떤 데이터를 어디서 받아, 얼마나 자주 맞추고, 자료끼리 어긋날 때 무엇을 믿어야 하는지 정리한 자료입니다. 시뮬레이션 결과를 다시 만들 수 있도록 실행마다 무엇을 남길지도 다룹니다.

다루는 내용은 다음과 같습니다.

- 데이터 네 갈래: CM(설정) · PM(성능) · FM(경보) · 인벤토리와 사이트 자료
- 받는 길
  - O-RAN O1: CM은 NETCONF/YANG과 변경 알림, PM은 파일(notifyFileReady)과 WebSocket 스트리밍, FM은 경보 알림, 공통 VES 형식
  - O-RU는 Open Fronthaul M-Plane (자세한 내용은 [`m-plane-yang`](../m-plane-yang/) 덱)
  - 업체 EMS · OSS 북향 내보내기
- 3GPP SA5 규격 지도: TS 28.541 · 28.552 · 28.550 · 28.532 · 28.545 · 28.622/28.623 · 32.692 · 37.320
- 신선도: CM 알림과 하루 덤프, PM 집계 주기와 파일 지연, FM 실시간 (예시 하루)
- 버전 · 시간 여행: 스냅숏 + 변경 기록, 적용 시각과 기록 시각, as-of 질의
- 변경 감지(알림 + diff)와 계보(lineage)
- 충돌: 틸트 6° 대 4° — 기계 · 전기 · 디지털 틸트, 틀린 틸트가 만드는 거리별 오차(예시 계산)
- 어디를 믿나: 속성별 출처 순위, 신뢰 표시 네 단계, 증거
- 트윈 모델 매핑(CM 입력 · PM 목표 · FM 마스크), 파이프라인 구조, 실행마다 남길 기록

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/EMgyJseuDFuH9KtYB6YVsL, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/FuPaTmx92eL8rN1TCQZxAW
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py twin-data-sync`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`m-plane-yang`](../m-plane-yang/): O-RU 관리(M-Plane), O1과 M-Plane 비교(9쪽)
  - [`coord-registration`](../coord-registration/): 좌표 · 높이 · 시간 정합
  - [`dt-breakdown`](../dt-breakdown/): 거리 경향 몫 · Shape(T0) · 패턴 몫
  - [`network-digital-twin`](../network-digital-twin/): 트윈의 네 층과 실망 동기화
  - [`sionna-rt-inputs`](../sionna-rt-inputs/): 시뮬레이터 입력

## 구성 (≈ 11분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 트윈은 “언제의 망”인가: 반영 지연 그림, 낡은 입력이 모델 오차처럼 보이는 이유, 재현 | 0:45 |
| 3 | kinds | 데이터 네 갈래(CM · PM · FM · 사이트): 무엇 · 바뀌는 방식 · 트윈에서의 쓰임 | 0:45 |
| 4 | sources | 받는 길: O1(SMO ↔ RIC · O-CU · O-DU), M-Plane(O-RU), 업체 덤프 | 0:50 |
| 5 | specs | 3GPP SA5 규격 지도와 속성 · 측정 이름 | 0:50 |
| 6 | cadence | 예시 하루: 10:17에 트윈이 아는 것 (CM 알림 · 덤프 · PM 15분 · FM) | 0:55 |
| 7 | versioning | 스냅숏 + 변경 기록, 적용 / 기록 두 시각, 변경 기록 예 | 0:50 |
| 8 | detect | 변경 감지(알림 · diff · 맞추기 · heartbeat)와 계보 예 | 0:50 |
| 9 | tilt | 틸트 6° 대 4°: 세 가지 틸트, 거리별 안테나 이득 차 (예시 계산) | 1:00 |
| 10 | reconcile | 속성별 출처 순위, 신뢰 표시 네 단계, 충돌 규칙 | 0:50 |
| 11 | mapping | CM → 시뮬 입력, PM → 검증 목표, FM → 마스크, 시간 창 · 단위 | 0:50 |
| 12 | pipeline | 수집 → 정규화 → 검증 → 버전 저장소 → 시뮬 · 분석, 증거 되먹임 | 0:50 |
| 13 | checklist | 실행마다 남길 것과 run manifest 예 | 0:45 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 8쪽(변경 감지 · 계보)과 12쪽(파이프라인 구조)을 백업으로 돌리세요. 약 9분 20초가 됩니다.
- 규격을 이미 아는 청중이면 5쪽을 짧게(20초) 넘기고 12쪽을 남겨도 됩니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 클러스터]`
- 6쪽의 PM 집계 주기 · 파일 지연 · 덤프 주기를 우리 망의 실제 값으로 바꾸기
- 13쪽 manifest의 `<도구> <버전>`과 공통 좌표계(예시 EPSG:5179)

참고할 점:
- **O1 내용(4 · 8쪽):** ETSI TS 104 043 V11.0.0 (O-RAN.WG10.O1-Interface R003 v11)에서 확인했습니다.
  - 6.1 프로비저닝: NETCONF(get · get-config · edit-config 등)로 읽고 쓰며, 변경은 notifyMOIChanges 알림(HTTP/TLS, JSON)으로 알린다.
  - 6.2 경보: 발생 · 심각도 변경 · 해제 알림, 경보 목록 읽기, 목록 재구성(alarm list rebuilt) 알림.
  - 6.3 성능: 파일 보고(notifyFileReady → 보안 파일 전송)와 WebSocket 스트리밍, 측정 이름 접두사 OR.(O-RAN) · VS.(업체).
  - 6.5 파일 전송: SFTP · FTPeS · HTTPS. 6.6 heartbeat.
  - 5장 알림 형식: SDO(3GPP) 형식 또는 VES 형식(VES Event Listener 7.2.1). VES는 3GPP 알림을 stndDefined 이벤트로 감싸는 “harmonized VES”를 권하며, 옛 형식(legacy VES)은 PNF 등록만 지원.
  - O1은 SMO와 O1을 지원하는 관리 대상(Near-RT RIC · O-CU-CP/UP · O-DU) 사이의 인터페이스입니다. O-RU는 M-Plane으로 관리됩니다(M-Plane 사양 5.1.2: 계층형은 O-DU가, 하이브리드는 관리 시스템이 직접).
- **3GPP 규격(5쪽):**
  - 28.541 = 5G NRM (stage 2 · 3), 28.552 = 5G 성능 측정, 28.550 = 성능 보증, 28.532 = 공통 관리 서비스, 28.545 = 경보 감시(FS), 28.622 · 28.623 = 공통 NRM IS · SS, 32.432 = PM 파일 형식, 37.320 = MDT 전체 설명, 32.422 = 추적 제어 · 설정(MDT 활성화 포함). SA5 = Management, Orchestration and Charging.
  - 속성 이름: NRCellDU의 nRPCI(0~1007) · arfcnDL · ssbFrequency, NRSectorCarrier의 configuredMaxTxPower(mW), AntennaFunction의 retTiltValue(0.1°, TS 37.466의 “Tilt value”) · bearing, CommonBeamformingFunction의 digitalTilt(0.1°, −900~900, 양수 = 아래). 3GPP Forge의 YANG 모듈과 규격 미러(iTecSpec)에서 확인했습니다. 릴리스마다 모듈 이름 · 위치가 바뀌기도 합니다(안테나 기능은 28.662에 정의되고 NR NRM이 가져다 씀).
  - mechanicalOffset: “설치로 생긴 조정할 수 없는 틸트”, “실제 틸트 = mechanicalOffset + retTiltValue” (TS 32.692 인벤토리 NRM). 이 값이 Iuant(TS 37.466)로는 전달되지 않는다는 설명은 3GPP YANG 모듈 설명에서 봤습니다(2차 확인).
  - granularityPeriod: 파일 보고 5 · 15 · 30분 · 1 · 12 · 24시간(그 밖의 값도 협의 가능), 스트리밍은 초 단위 정수, reportingPeriod는 granularityPeriod의 배수 (TS 28.550 6.1.1.2).
  - 측정 이름: L1M.SS-RSRP.Bin(SSB별 SS-RSRP 분포, 구간 수 · 범위는 구현 몫) · RRU.PrbUsedDl(데이터용 DL PRB 평균) (TS 28.552 5.1.1.22.1 · 5.1.1.2.5).
  - RET 원격 조정: O-RU의 ALD 포트로 AISG 2.0(Iuant 응용 계층을 고친 것)을 쓴다 (M-Plane 사양 14.4).
- **예시 · 가정:**
  - 2쪽 그림, 6쪽 하루(변경 시각, PM 파일 지연 5분, 하루 1회 02:00 덤프, 경보 시각), 7쪽 변경 기록, 8쪽 계보, 13쪽 manifest는 모두 예시입니다. “알림 지연은 초 단위 예상”도 일반적 기대이며 측정값이 아닙니다.
  - 6쪽 계산: as-of 10:17, 주기 15분 + 지연 5분이면 받은 마지막 구간 끝은 10:00(17분 전), 가장 낡을 때 20분. 02:00 덤프만 쓰면 8시간 17분 전 상태.
  - 9쪽 계산: RU 높이 30 m, UE 1.5 m, 수직 패턴 −min(12(Δθ/θ3dB)², 20 dB), θ3dB 8°(가정). 틸트 6°와 4°의 이득 차는 150 m에서 +4.3 dB, 112 m 부근 최대 +7.0 dB, 약 326 m에서 0, 2 km에서 −3.1 dB. 주빔이 땅에 닿는 거리 271 m · 408 m. 경로 손실 · 수평 패턴은 같다고 보고 수직 패턴만 비교한 것입니다.
  - 10쪽 출처 순위 · 신뢰 표시 네 단계, 12쪽 파이프라인 구조는 발표자 제안입니다.
  - 4쪽 “업체 덤프가 흔하다”는 일반적 경향입니다.
- **11쪽 dBm:** 40000 mW = 46.0 dBm.

## 출처

- ETSI, [TS 104 043 V11.0.0 (2024-06) — O-RAN O1 Interface Specification](https://www.etsi.org/deliver/etsi_ts/104000_104099/104043/11.00.00_60/ts_104043v110000p.pdf) — 5장 알림 형식, 6.1 · 6.2 · 6.3 · 6.5 · 6.6절
- ETSI, [TS 104 023 V12.01 — O-RAN M-Plane](https://www.etsi.org/deliver/etsi_ts/104000_104099/104023/12.00.01_60/ts_104023v120001p.pdf) — 5.1.2절 계층형 · 하이브리드, 14.4절 ALD(AISG 2.0)
- ONAP, VES Event Listener Specification V7.2.1 (O1 사양의 참조 [18])
- 3GPP [28 계열 목록](https://www.3gpp.org/DynaReport/28-series.htm) · [SA WG5 소개](https://www.3gpp.org/specifications-groups/sa-plenary/sa5-telecom-management)
- 3GPP TS 28.550, [6.1.1.2 Input parameters (granularityPeriod)](https://itecspec.com/3gpp/28.550/s/6.1.1.2)
- 3GPP TS 28.552, [5.1.1.22.1 SS-RSRP distribution per SSB](https://itecspec.com/3gpp/28.552/s/5.1.1.22.1) · [5.1.1.2.5 DL PRB used for data traffic](https://www.itecspec.com/3gpp/28.552/s/5.1.1.2.5)
- 3GPP TS 28.541, [CommonBeamformingFunction (4.3.39)](https://itecspec.com/3gpp/28.541/s/4.3.39.1) · [NRSectorCarrier (4.3.6)](https://itecspec.com/3gpp/28.541/s/4.3.6.1)
- 3GPP Forge SA5 MnS YANG: [_3gpp-nr-nrm-nrcelldu.yang](https://forge.3gpp.org/rep/sa5/MnS/-/raw/0032d2835382c47bc402c077b40ef71d77c9a3c9/yang-models/_3gpp-nr-nrm-nrcelldu.yang) · [_3gpp-nr-nrm-nrsectorcarrier.yang](https://forge.3gpp.org/rep/sa5/MnS/-/raw/0032d2835382c47bc402c077b40ef71d77c9a3c9/yang-models/_3gpp-nr-nrm-nrsectorcarrier.yang) · [AntennaFunction 모듈 커밋](https://forge.3gpp.org/rep/sa5/MnS/-/commit/90f94f3cea94609138b9f16cd924143cf251989e)
- 3GPP TS 32.692, [6.5.1 mechanicalOffset](https://www.itecspec.com/3gpp/32.692/s/6.5.1)
- 3GPP TS 37.320 (MDT 전체 설명, [Rel-19 PDF](https://www.3gpp.org/ftp/specs/PDF/2026-09/Rel-19/37_series/37320-j40.pdf)) · TS 32.422 (추적 제어 · 설정)
- W3C, PROV-DM: The PROV Data Model (2013)
