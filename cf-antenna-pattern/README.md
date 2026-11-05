# 안테나 패턴은 CIR · CFR에 어떻게 들어가나

Antennas 페이지에 올린 안테나 패턴이 CF 빌드에서 CIR과 CFR에 어떻게 쓰이는지 정리한 자료입니다. 패턴은 Sionna RT 안에서 **소자 하나의 방사 패턴**이 되고, 경로마다 송신 출발각(AoD) · 수신 도착각(AoA)에서의 값이 경로 계수 a에 곱해집니다. 그 뒤 CF는 a를 다시 조정하지 않고, **빔포밍과 배열 이득도 더하지 않습니다**. 내용은 내부 문서 “안테나 패턴이 빌드(CIR/CFR)에 쓰이는 방식”을 옮긴 것입니다.

다루는 내용은 다음과 같습니다.

- 전체 흐름 ①–⑥: 등록 → 요청 → worker 계산 → CIR → CFR
- 등록
  - 형식 셋: MSI/Planet 2D 단면, NGMN BASTA 3D 격자, 벤더 가중치 파일
  - dBd → dBi(+2.15), BASTA Co + Cross 합치기
  - 계산이 쓰는 값 일곱 개와 읽지 않는 값(주파수 · 편파 · 전기 틸트)
  - 개정판 pattern_rev와 캐시 키
- 요청: AntennaConfig(pattern · polarization · rows · cols · spacing), 섹터 필드, 수신 안테나, 빌드 전 거부 조건
- 계산
  - 패턴 함수(전계 진폭 10^(G/20)), MSI dB 합 근사와 38.901의 30 dB 바닥
  - PlanarArray와 synthetic_array
  - 방향(yaw = 90° − 방위각, pitch = +기계 틸트, ADR 0070) — 전기 틸트는 더하지 않음
  - 섹터마다 안테나가 다를 때 묶어서 추적(ADR 0079)
- CIR: a에 들어 있는 것, h5 데이터셋(/cir/a · a_served · tau · /paths), 이득과 전력(/meta)
- CFR: H = Σ a·exp(−j2πf·tau), 대역 안에서 일정한 패턴, 보정 레이어
- CF가 하지 않는 것: 빔포밍 · 배열 이득(지점 전력 = 안테나 쌍 평균), 커버리지 맵 예외
- 가중치 파일: 빔 패턴 `<id>-b<k>` · 포트 패턴 `<id>-port` · H @ w · SSB 빔
- 세미나 포인트 다섯

15장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/NdCjeXark9L7xB3hzRBbVf, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/LPWz5At8TTbey8PF6xfcAT
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py cf-antenna-pattern`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`sionna-rt-antenna`](../sionna-rt-antenna/): Sionna RT 안테나 파라미터(PlanarArray · 패턴 · 편파)
  - [`sionna-rsrp-beam`](../sionna-rsrp-beam/): Sionna에서 빔과 RSRP
  - [`ss-rsrp`](../ss-rsrp/): 빔에서 SS-RSRP까지
  - [`antenna-basics`](../antenna-basics/): 안테나 입문(이득 · 빔폭 · 틸트)
  - [`dt-breakdown`](../dt-breakdown/): 실측과 비교할 때 잔차 해석

## 구성 (≈ 11분 50초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | flow | 전체 흐름 ①–⑥과 한 줄 요약 | 0:50 |
| 3 | register | 등록 형식 셋, dBd → dBi, BASTA 편파, 쓰는 값 7개 · 안 읽는 값 | 0:55 |
| 4 | revision | pattern_rev → 캐시 키, 개정판 0, 계산 시점 검사 | 0:40 |
| 5 | request | AntennaConfig 표, 섹터 필드, 수신 안테나, 빌드 전 거부 | 0:50 |
| 6 | pattern | 패턴 함수(전계 진폭), MSI dB 합 vs 38.901 30 dB 바닥 열지도 | 0:55 |
| 7 | array | PlanarArray, 소자 수, synthetic_array | 0:45 |
| 8 | orient | yaw · pitch · roll 그림, 전기 틸트는 더하지 않음 | 0:50 |
| 9 | group | ADR 0079: 같은 안테나끼리 묶어 추적 → 순서대로 합치고 채움 | 0:45 |
| 10 | cir | a = 경로 손실 × 송신 패턴 × 수신 패턴 × 위상, h5 데이터셋, 이득 vs 전력 | 0:55 |
| 11 | cfr | CIR 막대와 \|H(f)\| 예시, 합성 식, 보정 레이어 | 0:50 |
| 12 | nobf | 빔포밍 · 배열 이득 없음: 막대 셋(0 · 0 · +18.1 dB), 커버리지 맵 예외 | 0:55 |
| 13 | weights | 빔 패턴 · 포트 패턴, 빔 패턴 식, H @ w, SSB 빔 | 0:55 |
| 14 | points | 세미나 포인트 다섯 | 0:45 |
| 15 | summary | 정리 | 0:40 |

- 10분 안에 맞추려면 4쪽(개정판), 9쪽(묶음 추적), 14쪽(포인트 — 정리와 겹침)을 백업으로 돌리세요. 약 9분 40초가 됩니다.
- 시간이 더 모자라면 7쪽(배열)을 빼고 12쪽에서 “소자마다 따로”만 짚으세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 15쪽 “확인할 것”을 팀의 실제 다음 단계로 바꾸기

참고할 점:
- **출처:** 슬라이드 내용(필드 이름 · 기본값 · ADR 번호 · 데이터셋 축 · “0.5 dB 이내” 테스트 결과)은 모두 내부 문서를 옮긴 것이고 따로 확인하지 않았습니다. 코드가 바뀌면 문서와 함께 고쳐야 합니다.
- **예시 그림(생성기에서 numpy로 계산):**
  - 6쪽 열지도: 38.901 모양 단면(빔폭 65°, 단면 바닥 30 dB, 12·(각/65)²)으로 만든 예시이며 실제 측정 패턴이 아닙니다. 방위 100° · 앙각 48°에서 dB 합 34 dB, 30 dB 바닥이면 30 dB.
  - 8쪽: 방위 120° → yaw −30°, 틸트 6°는 예시. 옆 그림의 기울기는 보이게 키워 그렸습니다.
  - 9쪽: 섹터 다섯(A · A · B · A · B)과 경로 수 37 · 22는 예시.
  - 11쪽: 경로 넷(|a| 1.0 · 0.55 · 0.35 · 0.20, 지연 300 · 420 · 610 · 880 ns)을 100 MHz · 부반송파 400개로 합성. |H|는 −24.5 ~ +6.4 dB.
  - 12쪽: 단일 경로 · 소자 64개 · 위상만 다른 경우. 쌍 평균은 소자 하나와 같고(0 dB), 정합 가중치 H @ w는 10·log10 64 ≈ 18.1 dB.
- 2쪽의 “한 줄 요약”과 14쪽 포인트는 문서 §1 · §9의 문장을 줄인 것입니다.

## 출처

- 내부 문서 “안테나 패턴이 빌드(CIR/CFR)에 쓰이는 방식” (§1–§9), ADR 0070(방향 · pitch 부호), ADR 0079(섹터별 안테나 묶음), `configs/h5_schema.yaml`
- Sionna RT 문서 — PlanarArray, 안테나 패턴, `synthetic_array`: https://nvlabs.github.io/sionna/rt/
- 3GPP TR 38.901 §7.3 — 안테나 소자 패턴(수평 · 수직 감쇠 합, 30 dB 바닥)
- NGMN BASTA (Base Station Antenna Standards) — 3D 패턴 파일 형식
