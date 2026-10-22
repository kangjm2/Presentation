# M-Plane과 YANG

O-RAN Open Fronthaul의 관리 평면(M-Plane)을 다루는 세미나 자료입니다. 19장이고, 슬라이드마다 발표자 노트가 있습니다. 다루는 내용은 다음과 같습니다.

- M-Plane이 왜 고안되었는지
- YANG 모델로 메시지를 주고받는 것의 의미, uplane-conf가 만들어지는 순서, O-DU 입장의 YANG 활용, O1 YANG과의 차이
- 타이밍 규칙: 시작 절차, 감시 워치독, 동기 상태
- 권한 제어(NACM)
- 위 내용을 캐리어 활성화 시나리오 하나로 묶어 통합적으로 이해하기
- 운용 흐름 한눈에 보기: Call Home → RU 능력 보고 → 경보 발생 → 경보 이후 동작(자체 보호 · 복구 · 재시작)

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/9ze6UtY6g4vFMU1hhsU4UP, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/T1tRRK9qL7gcAfpaoTkSvX
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py m-plane-yang`로 뷰어를 다시 만듭니다.

## 구성 (≈ 16분 45초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 배경: CPRI 시대 → 열린 프런트홀, 상호운용 · 자동화 · 안전 | 0:50 |
| 3 | arch | SMO 정의, 계층형 vs 하이브리드, NETCONF 서버/클라이언트, Call Home (4334/4335) | 0:55 |
| 4 | netconf | CLI · SNMP vs NETCONF/YANG, 표준 흐름 | 0:50 |
| 5 | yang | YANG 읽는 법 (o-ran-uplane-conf 발췌) | 0:50 |
| 6 | message | YANG 형식 메시지의 의미: 계약 · 자기 소개 · 트랜잭션 · 자동화 | 0:55 |
| 7 | uplane | uplane-conf가 만들어지는 순서: 읽기 → 전송 → 끝점(eAxC) → 캐리어 → 링크, 구조 그림 | 0:55 |
| 8 | odu | O-DU 입장의 YANG 활용: 코드 생성 · 능력 기반 설정 · 사전 검증 · 안전한 변경 · 이벤트 자동화 · 시험, DU 안에서 YANG으로 다룰 것과 밖으로 뺄 것 | 1:05 |
| 9 | o1 | O1(WG10)과 M-Plane(WG4) 비교: 관리 대상 · 3GPP NRM 모델 · 등록 · VES 알림 · heartbeat · PM, O-DU가 두 모델 사이에 서는 구조 | 1:00 |
| 10 | startup | 타이밍 ①: 시작 절차 시퀀스 (DHCP · O-RU · O-DU) | 0:55 |
| 11 | watchdog | 타이밍 ②: 감시 워치독, 타이머가 두 개인 이유(양방향 생존 확인), 감시 실패 처리, confirmed-commit 주의 | 1:00 |
| 12 | sync | 타이밍 ③: o-ran-sync 상태 (LOCKED · HOLDOVER · FREERUN), HOLDOVER의 의미, 캐리어 | 0:55 |
| 13 | nacm | 권한 제어: 인증 → 그룹 → 모듈별 R/W/X (Table 6.5-1 발췌) | 1:00 |
| 14 | together | 통합: 캐리어 하나를 켤 때 YANG · 타이밍 · 권한이 만나는 순서 | 0:55 |
| 15 | lifecycle | 운용 흐름 한눈에: Call Home → 능력 보고 → 구독 → 경보 → 조치 → 해제, 리셋 시 처음부터 | 1:00 |
| 16 | capability | RU 능력 보고: hello · ietf-yang-library · o-ran-module-cap · hardware/operations/sync | 0:55 |
| 17 | alarm | 경보 발생: 감지 → active-alarm-list → alarm-notif → 해제, 심각도 규칙과 메시지 예 | 0:55 |
| 18 | recovery | 경보 이후 동작: 공통 경보별 RU 자체 동작 · 관리자 복구 · 해제 조건 (Annex A 발췌), 재시작 경로 | 0:55 |
| 19 | summary | 정리 | 0:35 |

10분에 맞추려면 7~9쪽(uplane-conf · O-DU 활용 · O1 비교)과 16~18쪽(능력 보고 · 경보 상세)을 질의응답용 백업으로 넘기세요. 그러면 약 11분입니다. 4쪽(NETCONF)이나 6쪽(메시지)을 짧게 말하면 10분 안팎으로 들어옵니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[시험 대상 O-RU]`

참고할 점:
- 사양 값(감시 타이머 기본값, 그룹별 권한, 동기 상태와 캐리어 규칙)은 ETSI TS 104 023 V12.01(O-RAN WG4 M-Plane 기반)에서 확인했습니다. 버전에 따라 다를 수 있습니다.
- 5쪽 YANG과 6쪽 메시지, 16쪽 module-cap과 17쪽 alarm-notif XML은 실제 모델을 단순화한 예입니다(값 · 이름 · 시각은 예시).
- 18쪽 경보 표는 Annex A Table A.1-1에서 대표 경보만 골라 우리말로 줄였습니다. “관리자 복구” 열은 사양에서도 참고용(informative)이라 실제 조치는 운영 정책을 따릅니다.
- 10쪽 시작 절차는 사양의 “O-RU 컨트롤러”를 O-DU로 표기했습니다(계층형 기준). 하이브리드에서는 SMO도 같은 절차로 붙습니다.
- 7쪽 uplane-conf 단계는 사양 15.2.4의 일반 설정 시나리오를 다섯 단계로 줄인 것입니다. 8쪽 O-DU 활용과 도구 예시, DU 내부 설계 원칙(YANG으로 다룰 것과 밖으로 뺄 것)은 발표자 정리입니다. 근거로 삼은 표준은 NMDA(RFC 8342)와 YANG-Push(RFC 8641)입니다.
- 9쪽: ‘YANG-O1’이라는 이름의 규격은 따로 없습니다. O-RAN WG10의 O1 인터페이스 사양(ETSI TS 104 043 = O-RAN.WG10.O1-Interface R003 v11)이 있고, 데이터 모델은 3GPP NRM YANG(TS 28.541 · 28.623의 `_3gpp-*` 모듈)에 O-RAN 확장(WG10 정보 · 데이터 모델 사양, WG5 O-DU · O-CU O1 사양)을 더한 것입니다. 객체 트리 예(ManagedElement → GNBDUFunction → NRCellDU)는 O-RAN SC 시험 환경에서 쓰는 모듈 기준입니다. O-RAN 확장 모듈의 정확한 이름 · 내용은 O-RAN이 배포하는 YANG 패키지에서 확인이 필요합니다.
- 12쪽 HOLDOVER 설명은 ITU-T G.810의 정의(잠겨 있던 동안 저장한 데이터로 출력을 유지하는 상태)를 풀어 쓴 것입니다. 유지 시간과 정확도는 장비마다 다릅니다.

## 출처

- O-RAN Alliance, [O-RAN.WG4.TS.MP.0 (M-Plane Specification)](https://specifications.o-ran.org/download?id=857) · ETSI, [TS 104 023 V12.01 (2024-05)](https://www.etsi.org/deliver/etsi_ts/104000_104099/104023/12.00.01_60/ts_104023v120001p.pdf) — 6장 시작 절차, 6.5절 NACM(Table 6.5-1), 6.7절 감시, 9장 설정 관리, 13장 동기, 14.1절 감시 실패 처리, 15.2.4절 U-Plane 설정 시나리오, 15.3.3절 동기 상실, 6.3절 Call Home, 6.6 · 9.2 · 15.1절 능력 조회, 9.5절 리셋, 11장 경보 관리, Annex A 공통 경보, Annex D.2.5 o-ran-fm · D.6.1 o-ran-module-cap
- ETSI, [TS 104 043 V11.0.0 (2024-06) — O-RAN O1 Interface Specification (O-RAN.WG10.O1-Interface R003 v11)](https://www.etsi.org/deliver/etsi_ts/104000_104099/104043/11.00.00_60/ts_104043v110000p.pdf) — 5장 O1 알림(SDO · VES 형식), 6.1 프로비저닝(NETCONF), 6.2 경보, 6.3 성능(PM 파일 · 스트리밍), 6.6 heartbeat, 6.7 PNF 등록 · M-Plane 사양 6.9절 PNF 등록, 10장 성능 관리, 12장 파일 관리
- 3GPP TS 28.541 (NR NRM) · TS 28.623 (일반 NRM YANG) · TS 28.532 (관리 서비스) · [O-RAN SC: O1 specifics (_3gpp 모듈 예)](https://lf-o-ran-sc.atlassian.net/wiki/spaces/IAT/pages/382959663/O1+specifics)
- IETF RFC 6241 (NETCONF) · RFC 7950 (YANG 1.1) · RFC 8071 (NETCONF Call Home) · RFC 8341 (NACM) · RFC 6022 (NETCONF 모니터링, get-schema) · RFC 5277 (NETCONF 알림, create-subscription) · RFC 8525 (YANG 라이브러리) · ITU-T X.733 (경보 심각도)
- Keysight, [O-RAN M-Plane Reference Guide](https://www.keysight.com/gr/en/assets/9921-01491/reference-guides/ORAN-M-Plane-Reference-Guide.pdf) · Benetel, [O-RAN RU, Architecture and Testing (OAI 워크숍 2022)](https://openairinterface.org/wp-content/uploads/2022/07/2022-07-13-BENETEL-SLIDES.pdf)
- [NETCONF and YANG — O-RAN WG4 M-Plane 정리 (HackMD)](https://hackmd.io/@saffanazyan/BkvwCtgGA) · [o-ran-supervision RPC 구조 예 (ConfD 커뮤니티)](https://discuss.tail-f.com/t/create-actionpoint-to-rpc/4042)
