# Sionna RSRP와 실측 SS-RSRP

Sionna RT로 계산한 RSRP를 실측 SS-RSRP와 비교할 때 빔을 어떻게 만들어 넣어야 하는지 정리한 세미나 자료입니다. 핵심 질문은 이것입니다. common beam weight를 그대로 쓰면 되는가, 아니면 64개 부배열 패턴과 etilt를 반영해 빔을 합성해야 하는가. 15장이고, 슬라이드마다 발표자 노트가 있습니다.

- **결론:** 두 의견은 대립하지 않습니다. 빔 = Σ w × S입니다. common beam weight(w)는 *무엇을 곱할지*, etilt별 부배열 패턴(S)은 *어디에 곱할지*입니다. 실측과 비교하려면 현재 etilt의 부배열 패턴 위에 common beam weight를 곱해야 합니다(동료가 말한 방법).
- **Sionna 입력:** 합성 빔 패턴을 Sionna 밖에서 만들어 검증한 뒤, 단일 소자 패턴으로 등록해 SSB 빔마다 radio map을 계산합니다(R1). 정밀 검증은 측정 지점에서 부배열별 경로를 합성합니다(R3).
- **비교 정렬:** RE당 전력(64포트 합계)을 넣고, UE 안테나 이득 · 빔 통합 규칙 · 빈(bin) 처리를 실측과 맞춥니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/81gneTBaSKq81ovsUtxVpE, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/TXbSrFZa3fmQwE17msyDCS
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- **용어 풀이: [`glossary.md`](glossary.md)** — EPRE, 선형 평균, L3 필터, 부배열, path gain 등 전문 용어를 처음 보는 사람도 읽을 수 있게 숫자 예와 함께 풀었습니다
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sionna-rsrp-beam`로 뷰어를 다시 만듭니다.
- 관련 덱: [`ss-rsrp`](../ss-rsrp/) (빔에서 SS-RSRP까지) · [`sionna-rt-antenna`](../sionna-rt-antenna/) (Sionna 안테나 파라미터) · [`sionna-rt-inputs`](../sionna-rt-inputs/) · [`rf-modeling-tools`](../rf-modeling-tools/) (모델 보정)

## 구성 (≈ 13분 05초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | goal | 실측과 Sionna의 두 계산 사슬, 맞춰야 할 네 가지(빔 · 전력 · 수신 · 통계) | 0:50 |
| 3 | terms1 | 용어 풀이 ①: RE · SSB · SSS · EPRE · dBm (모눈종이 비유, 200 W → 17.8 dBm) | 0:50 |
| 4 | terms2 | 용어 풀이 ②: RE별 측정 → 선형 평균 → L1 평균 → 빔 통합 → L3 필터 → 보고 (숫자 예) | 0:55 |
| 5 | anatomy | 64T64R 해부: 소자 192개 → 부배열(아날로그 · etilt) → TXRU 64개 → 디지털 가중치(common beam weight) | 0:50 |
| 6 | formula | 빔 식 E_b = Σ w_b,k · S_k(etilt), 각 항의 출처, 데이터 양 · 편파 | 0:55 |
| 7 | verdict | 세 방법 비교(A 이상적 배열 / B 부배열 패턴 × w / C 합성 패턴 파일), 누구 말이 맞나 | 0:55 |
| 8 | plot | 세로 단면 계산 예: A · B · C(etilt 불일치) 비교, 사이트 근처 오차 | 0:55 |
| 9 | data | 벤더에게 받을 것과 확인할 것 체크리스트 | 0:50 |
| 10 | compose | 합성 패턴 만들기(오프라인)와 검증, Sionna 좌표 · 패턴 함수 규약 | 0:50 |
| 11 | sionna | Sionna 입력 경로 R1 · R2 · R3와 피할 방법 | 0:55 |
| 12 | code | R1 코드 뼈대 | 0:50 |
| 13 | power | RE당 전력(64포트 합계) → power_dbm, 단위와 정의 | 0:50 |
| 14 | measure | 실측 쪽 정렬: 빔별 · 셀 값, UE 이득, 빈 처리 | 0:50 |
| 15 | summary | 오차 모양별 진단과 결론 | 0:40 |

용어를 아는 청중이면 3 · 4쪽(용어 풀이)을 건너뛰세요(약 11분 20초). 10분에 맞추려면 여기에 12쪽(코드)까지 백업으로 넘기면 약 10분 30초이고, 9쪽(체크리스트)을 짧게 말하면 10분 안에 들어옵니다. 용어가 낯선 청중이면 반대로 3 · 4쪽을 살리고 9 · 12쪽을 백업으로 돌리세요(약 11분 25초). 발표 전에 [`glossary.md`](glossary.md)를 미리 읽게 하면 좋습니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 사이트]`

참고할 점:
- **용어 풀이(3 · 4쪽, glossary.md):** 비유(모눈종이 · 물감)와 숫자 예(−90 · −100 dBm의 선형 평균 −92.6 dBm, L3 필터 −90 · −100 · −90 → −90 · −95 · −92.5)는 설명용입니다. L3 필터는 기본 계수(k = 4, a = ½) 기준이며 RSRP는 dB 값에 필터를 겁니다(TS 38.331 5.5.3.2).
- **안테나 구성:** 192소자 = 12 × 8 × 2, 부배열 = 세로 3소자, TXRU 64개는 대표 예시입니다. 실제 소자 수 · 부배열 크기 · 간격은 장비 사양으로 확인해야 합니다.
- **8쪽 계산:** 세로 한 열(12소자)을 직접 계산한 예입니다(소자 TR 38.901 8 dBi · 65°, 소자 간격 0.7λ, 부배열 3소자, 디지털 틸트 6°, ‖w‖ = 1, 상호 결합 무시). A의 그레이팅 로브는 TXRU 간격 2.1λ에서 생기고, 실제 부배열 패턴(B)은 그 방향에 영점을 만들어 이를 지웁니다. C는 RET가 12°인데 6°용 가중치를 쓴 경우입니다. 수치는 개념 설명용이며 실제 장비 값이 아닙니다.
- **Sionna API:** Sionna RT 1.x 문서 기준입니다. `scene.tx_array`는 모든 송신기가 공유하고, 배열 안 소자는 같은 패턴을 씁니다. `RadioMapSolver`의 `precoding_vec`는 켤레 없이(전치) 곱합니다. radio map의 path gain은 경로 계수 크기 제곱의 합(비결맞음)입니다. 12쪽 코드는 의사 코드이므로 인자 이름과 기본값은 사용하는 버전의 문서로 확인하세요.
- **전력:** 200 W, 100 MHz, 30 kHz는 예시입니다. ss-PBCH-BlockPower가 포트당 값인지 합계인지, SSB 전력 부스팅이 있는지는 장비 · 망 설정마다 다릅니다.
- **실측 정렬:** 빈 크기 20~50 m와 15쪽의 오차 진단 표는 경험적 출발점입니다.

## 출처

- Sionna RT 문서: [RadioMapSolver (precoding_vec, 비결맞음 path gain)](https://nvlabs.github.io/sionna/rt/api/radio_map_solvers.html) · [Antenna patterns (AntennaPattern, register_antenna_pattern, PolarizedAntennaPattern, compute_gain)](https://nvlabs.github.io/sionna/rt/api/antenna_pattern.html) · [Scene (tx_array · rx_array는 모든 송신기 · 수신기 공통)](https://nvlabs.github.io/sionna/rt/api/scene.html) · [PathSolver (synthetic_array)](https://nvlabs.github.io/sionna/rt/api/paths_solvers.html) · [Radio devices (Transmitter: position · orientation · power_dbm)](https://nvlabs.github.io/sionna/rt/api/radio_devices.html)
- [Sionna RT: Technical Report (arXiv 2504.21719)](https://arxiv.org/abs/2504.21719) · [배열 소자가 같은 패턴을 써야 한다는 제약 언급 (arXiv 2604.14869)](https://arxiv.org/pdf/2604.14869)
- 3GPP TR 38.901 7.3 (안테나 소자 패턴 · 패널 · TXRU 가상화) · TS 38.215 5.1.1 (SS-RSRP 정의) · TS 38.331 (ss-PBCH-BlockPower, 5.5.3 빔 통합 · L3 필터)
- 배열 안테나 일반: 배열 인자 · 그레이팅 로브 · 부배열(서브어레이) 구조 — 안테나 교재 (예: Balanis, *Antenna Theory*; Mailloux, *Phased Array Antenna Handbook*)
