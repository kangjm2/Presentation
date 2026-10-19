# M-Plane과 YANG

O-RAN Open Fronthaul의 관리 평면(M-Plane)을 다루는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다. 다루는 내용은 다음과 같습니다.

- M-Plane이 왜 고안되었는지
- YANG 모델로 메시지를 주고받는 것의 의미
- 타이밍 규칙: 시작 절차, 감시 워치독, 동기 상태
- 권한 제어(NACM)
- 위 내용을 캐리어 활성화 시나리오 하나로 묶어 통합적으로 이해하기

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/9ze6UtY6g4vFMU1hhsU4UP, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/T1tRRK9qL7gcAfpaoTkSvX
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py m-plane-yang`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 배경: CPRI 시대 → 열린 프런트홀, 상호운용 · 자동화 · 안전 | 0:50 |
| 3 | arch | 계층형 vs 하이브리드, NETCONF 서버/클라이언트, Call Home (4334/4335) | 0:50 |
| 4 | netconf | CLI · SNMP vs NETCONF/YANG, 표준 흐름 | 0:50 |
| 5 | yang | YANG 읽는 법 (o-ran-uplane-conf 발췌) | 0:50 |
| 6 | message | YANG 형식 메시지의 의미: 계약 · 자기 소개 · 트랜잭션 · 자동화 | 0:55 |
| 7 | startup | 타이밍 ①: 시작 절차 시퀀스 | 0:55 |
| 8 | watchdog | 타이밍 ②: 감시 워치독 (60 s + 10 s), 감시 실패 처리, confirmed-commit 주의 | 0:55 |
| 9 | sync | 타이밍 ③: o-ran-sync 상태 (LOCKED · HOLDOVER · FREERUN)와 캐리어 | 0:50 |
| 10 | nacm | 권한 제어: 인증 → 그룹 → 모듈별 R/W/X (Table 6.5-1 발췌) | 1:00 |
| 11 | together | 통합: 캐리어 하나를 켤 때 YANG · 타이밍 · 권한이 만나는 순서 | 0:55 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[시험 대상 O-RU]`

참고할 점:
- 사양 값(감시 타이머 기본값, 그룹별 권한, 동기 상태와 캐리어 규칙)은 ETSI TS 104 023 V12.01(O-RAN WG4 M-Plane 기반)에서 확인했습니다. 버전에 따라 다를 수 있습니다.
- 5쪽 YANG과 6쪽 메시지는 실제 모델을 단순화한 예입니다.

## 출처

- O-RAN Alliance, [O-RAN.WG4.TS.MP.0 (M-Plane Specification)](https://specifications.o-ran.org/download?id=857) · ETSI, [TS 104 023 V12.01 (2024-05)](https://www.etsi.org/deliver/etsi_ts/104000_104099/104023/12.00.01_60/ts_104023v120001p.pdf) — 6장 시작 절차, 6.5절 NACM(Table 6.5-1), 6.7절 감시, 9장 설정 관리, 13장 동기, 14.1절 감시 실패 처리, 15.3.3절 동기 상실
- IETF RFC 6241 (NETCONF) · RFC 7950 (YANG 1.1) · RFC 8071 (NETCONF Call Home) · RFC 8341 (NACM) · RFC 6022 (NETCONF 모니터링, get-schema)
- Keysight, [O-RAN M-Plane Reference Guide](https://www.keysight.com/gr/en/assets/9921-01491/reference-guides/ORAN-M-Plane-Reference-Guide.pdf) · Benetel, [O-RAN RU, Architecture and Testing (OAI 워크숍 2022)](https://openairinterface.org/wp-content/uploads/2022/07/2022-07-13-BENETEL-SLIDES.pdf)
- [NETCONF and YANG — O-RAN WG4 M-Plane 정리 (HackMD)](https://hackmd.io/@saffanazyan/BkvwCtgGA) · [o-ran-supervision RPC 구조 예 (ConfD 커뮤니티)](https://discuss.tail-f.com/t/create-actionpoint-to-rpc/4042)
