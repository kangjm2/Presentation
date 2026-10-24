# Sionna RSRP와 실측 SS-RSRP

Sionna RT로 계산한 RSRP를 실측 SS-RSRP와 비교할 때 빔을 어떻게 만들어 넣어야 하는지 정리한 세미나 자료입니다. 핵심 질문은 이것입니다. common beam weight를 그대로 쓰면 되는가, 아니면 64개 부배열 패턴과 etilt를 반영해 빔을 합성해야 하는가. 본편 18장과 부록 4장, 모두 22장이고, 슬라이드마다 발표자 노트가 있습니다.

- **결론:** 두 의견은 대립하지 않습니다. 빔 = Σ w × S입니다. common beam weight(w)는 *무엇을 곱할지*, 부배열 패턴(S, sub-array gain)은 *어디에 곱할지*입니다. 실측과 비교하려면 현재 etilt 설정과 짝이 맞는 w와 S를 복소수로 곱해 더해야 합니다(동료가 말한 방법). etilt 설정이 w를 바꾸는 장비(구조 ①, AAU에서 흔함)라면 S는 한 벌이고 w가 etilt마다 다릅니다.
- **Sionna에 넣는 것:** 가중치(숫자 64개)가 아니라 그 결과인 *공통 빔 패턴*(3D 패턴 하나)입니다. “부배열 패턴과 가중치로 공통 빔을 만들어 Sionna 입력으로 쓴다”는 생각이 맞습니다(7 · 8쪽). 틀린 것은 가중치만 Sionna 기본 배열에 넣는 경우입니다.
- **Sionna 입력:** 합성 빔 패턴을 Sionna 밖에서 만들어 검증한 뒤, 단일 소자 패턴으로 등록해 SSB 빔마다 radio map을 계산합니다(R1). 정밀 검증은 측정 지점에서 부배열별 경로를 합성합니다(R3).
- **tilt:** 기계 tilt와 e-tilt는 따로 정하는 독립된 값이지만 방사되는 빔에서는 합쳐집니다. e-tilt(와 디지털 tilt)는 공통 빔 패턴 안에, 기계 tilt는 Sionna `orientation`에 한 번씩만 넣습니다. 그러면 공통 빔을 e-tilt별로 미리 계산해 표로 두고, 측정 시점의 e-tilt에 맞는 것을 골라 쓸 수 있습니다(10쪽). 디지털 tilt는 넓은 뜻으로는 전기 tilt에 포함되지만, 바꾸는 대상이 S_k가 아니라 가중치 w라서 이 덱에서는 따로 다룹니다(11쪽).
- **비교 정렬:** RE당 전력(64포트 합계)을 넣고, UE 안테나 이득 · 빔 통합 규칙 · 빈(bin) 처리를 실측과 맞춥니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/81gneTBaSKq81ovsUtxVpE, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/TXbSrFZa3fmQwE17msyDCS
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- **용어 풀이: [`glossary.md`](glossary.md)** — EPRE, 선형 평균, L3 필터, 부배열, path gain 등 전문 용어를 처음 보는 사람도 읽을 수 있게 숫자 예와 함께 풀었습니다
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별, 부록 포함)
- 가중치 파일 · 안테나 데이터 설명을 읽을 때: [`glossary.md` 13절](glossary.md#13-가중치-파일-설명을-읽을-때) (자주 나오는 문장 → 뜻 → 쪽)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sionna-rsrp-beam`로 뷰어를 다시 만듭니다.
- 관련 덱: [`ss-rsrp`](../ss-rsrp/) (빔에서 SS-RSRP까지) · [`sionna-rt-antenna`](../sionna-rt-antenna/) (Sionna 안테나 파라미터) · [`sionna-rt-inputs`](../sionna-rt-inputs/) · [`rf-modeling-tools`](../rf-modeling-tools/) (모델 보정)

## 구성 (본편 ≈ 15분 · 부록 ≈ 3분 35초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | goal | 실측과 Sionna의 두 계산 사슬, 맞춰야 할 네 가지(빔 · 전력 · 수신 · 통계) | 0:50 |
| 3 | terms1 | 용어 풀이 ①: RE · SSB · SSS · EPRE · dBm (모눈종이 비유, 200 W → 17.8 dBm) | 0:50 |
| 4 | terms2 | 용어 풀이 ②: RE별 측정 → 선형 평균 → L1 평균 → 빔 통합 → L3 필터 → 보고 (숫자 예) | 0:55 |
| 5 | anatomy | 64T64R 해부: 소자 192개 → 부배열(아날로그 가중치, 공장 고정 또는 RET) → TXRU 64개 → 디지털 가중치(common beam weight, etilt 설정마다 다른 벌일 수 있음) | 0:50 |
| 6 | formula | 빔 식 E_b = Σ w_b,k · S_k(복소수 합, a_m은 S_k 안에)와 신호 흐름도, etilt 설정이 바꾸는 것: ① w 또는 ② S_k: SSB 신호 → 디지털 가중치 w → TXRU → 아날로그 가중치 a_m → 부배열 패턴 S_k(넓음, 12.7 dBi) → 공간 합 E_b(좁음, 18.7 dBi) | 0:55 |
| 7 | words | 말부터 맞추기: 부배열 패턴 S_k(sub-array gain) · 부배열 가중치 w(= common beam weight) · 공통 빔 F_b — Sionna에는 F_b | 0:55 |
| 8 | verdict | Sionna에 무엇을 넣나: B(부배열 패턴 × 가중치 → 공통 빔 패턴 → Sionna) · C(벤더 공통 빔 패턴 파일) · A(가중치만 넣기, 피함), 재료 · 조리법 · 요리 비유 | 0:55 |
| 9 | plot | 세로 단면 계산 예: A · B · C(부배열 패턴과 가중치의 짝 어긋남) 비교, 사이트 근처 오차 | 0:55 |
| 10 | tilt | tilt 세 층: 기계(패널 회전 → orientation) · e-tilt(S_k가 바뀜 → F_b) · 디지털(w → F_b), 방위각별 하향각 비교, e-tilt별 공통 빔 표 | 0:55 |
| 11 | tilt2 | e-tilt(좁은 뜻: 부배열 안 아날로그, S_k를 바꿈) vs 디지털 tilt(가중치 w, 창 안에서 빔을 옮김), 넓은 뜻의 전기 tilt와의 관계, 디지털만 12° 숙일 때 위쪽 부엽 8.9 dBi 계산 예 | 0:55 |
| 12 | data | 벤더에게 받을 것과 확인할 것 체크리스트 | 0:50 |
| 13 | compose | 합성 패턴 만들기(오프라인)와 검증, Sionna 좌표 · 패턴 함수 규약 | 0:50 |
| 14 | sionna | Sionna 입력 경로 R1 · R2 · R3와 피할 방법 | 0:55 |
| 15 | code | R1 코드 뼈대 | 0:50 |
| 16 | power | RE당 전력(64포트 합계) → power_dbm, 단위와 정의 | 0:50 |
| 17 | measure | 실측 쪽 정렬: 빔별 · 셀 값, UE 이득, 빈 처리 | 0:50 |
| 18 | summary | 오차 모양별 진단과 결론 | 0:40 |
| 19 | names | 부록 ①: 같은 물건, 다른 이름 — AE · 서브어레이 weight · 포트 패턴 · 포트 위치 · 빔 weight · 빔 패턴 대응표 | 0:50 |
| 20 | factor | 부록 ②: 패턴 곱셈(빔 = 포트 패턴 × 배열 인자), 그레이팅 로브가 포트 패턴 영점에 지워지는 계산 예, 고정 tilt를 잘못 가정할 때 | 0:55 |
| 21 | geometry | 부록 ③: 가중치에서 포트 간격 추정(Δφ ≈ 107° → 2.84λ), 4V × 16H, 포트 번호 순서와 틀릴 때 생기는 일 | 0:55 |
| 22 | files | 부록 ④: 받는 파일별로 채워지는 것과 남는 가정, “common-beam 파일만 있으면 되나?” | 0:55 |

용어를 아는 청중이면 3 · 4쪽(용어 풀이)을 건너뛰세요(약 13분 15초). 여기에 15쪽(코드)과 12쪽(체크리스트)까지 백업으로 넘기면 약 11분 35초이고, 10 · 11쪽(tilt)까지 넘기면 약 9분 45초입니다. 용어가 낯선 청중이면 3 · 4쪽을 살리고 12 · 15쪽을 백업으로 돌리세요(약 13분 20초). 7 · 8쪽(말 맞추기 · Sionna에 넣을 것)은 이 덱의 핵심이므로 줄이지 않는 것을 권합니다. 10 · 11쪽은 etilt가 사이트마다 다르거나 운용 중 바뀌는 경우, 또는 장비의 tilt 설정이 무엇을 바꾸는지 논의할 때 특히 중요합니다. 발표 전에 [`glossary.md`](glossary.md)를 미리 읽게 하면 좋습니다. 부록(19~22쪽)은 본편 시간에 넣지 않았습니다. 질의응답이나 벤더 데이터를 놓고 하는 실무 회의에서 꺼내 쓰세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 사이트]`

참고할 점:
- **용어 풀이(3 · 4쪽, glossary.md):** 비유(모눈종이 · 물감)와 숫자 예(−90 · −100 dBm의 선형 평균 −92.6 dBm, L3 필터 −90 · −100 · −90 → −90 · −95 · −92.5)는 설명용입니다. L3 필터는 기본 계수(k = 4, a = ½) 기준이며 RSRP는 dB 값에 필터를 겁니다(TS 38.331 5.5.3.2).
- **용어 대응(7쪽):** “sub-array gain = 부배열 패턴 S_k”, “sub-array weight = common beam weight”로 대응시켰습니다. 벤더 · 팀에 따라 sub-array weight가 부배열 *안쪽* 소자 가중치(etilt가 정함)를 뜻할 수도 있으며, 그 경우 S_k를 만드는 재료입니다. 어느 쪽이든 Sionna에 넣는 것은 공통 빔 패턴 F_b라는 결론은 같습니다.
- **안테나 구성:** 192소자 = 12 × 8 × 2, 부배열 = 세로 3소자, TXRU 64개는 대표 예시입니다. 실제 소자 수 · 부배열 크기 · 간격은 장비 사양으로 확인해야 합니다.
- **6쪽 그림:** 신호 흐름은 64갈래 중 3갈래만 그렸고, 오른쪽 패턴(S_k · E_b)은 9쪽과 같은 조건으로 계산한 세로 단면을 극좌표로 그린 것입니다(최대 이득 기준 −20 dB까지 표시).
- **9쪽 계산:** 세로 한 열(12소자)을 직접 계산한 예입니다(소자 TR 38.901 8 dBi · 65°, 소자 간격 0.7λ, 부배열 3소자, 디지털 틸트 6°, ‖w‖ = 1, 상호 결합 무시). A의 그레이팅 로브는 TXRU 간격 2.1λ에서 생기고, 실제 부배열 패턴(B)은 그 방향에 영점을 만들어 이를 지웁니다. C는 RET가 12°인데 6°용 가중치를 쓴 경우입니다. 수치는 개념 설명용이며 실제 장비 값이 아닙니다.
- **tilt(10쪽):** 하향각 곡선은 패널 기준 주빔 능선(e-tilt만큼 숙인 원뿔)을 기계 tilt만큼 회전해 계산한 기하학적 예입니다. 기계 tilt의 하향각은 방위각 φ에서 대략 asin(cos φ · sin M)으로 줄어듭니다. 실제 패턴의 모양 변화(부엽 · 영점)는 반영하지 않았습니다. 벤더 패턴 파일이 e-tilt를 포함하고 기계 tilt는 빠진 패널 기준 좌표계인지 반드시 확인하세요. e-tilt를 바꿀 때 가중치 w도 함께 바뀌는지(BEAM-TILT 등)는 장비마다 다릅니다.
- **e-tilt와 디지털 tilt(11쪽):** 이 덱의 e-tilt는 3GPP TR 38.901 7.3의 θ_etilt처럼 부배열 안쪽 아날로그 위상(좁은 뜻)입니다. 넓은 뜻의 “전기 tilt”는 디지털 tilt까지 포함하며, 장비 설정의 tilt가 어느 쪽을 바꾸는지는 벤더마다 다릅니다. Massive MIMO AAU에서 부배열 안쪽 tilt가 공장 고정(preset)인 경우가 많다는 점, 디지털 tilt 범위가 위쪽 부엽 때문에 몇 도로 제한된다는 점은 일반적인 경향이며 장비 사양으로 확인해야 합니다. 그래프는 9쪽과 같은 조건(세로 한 열, 2.1λ TXRU 간격)의 계산입니다.
- **etilt 구조 ① · ②(5 · 6 · 11쪽):** etilt 설정이 디지털 가중치를 바꾸는지(구조 ①, Massive MIMO AAU에서 흔함, 부배열 패턴 한 벌 + etilt별 가중치), 부배열 안쪽 아날로그 위상을 바꾸는지(구조 ②, 부배열 패턴이 etilt마다)는 장비마다 다릅니다. 덱의 결론(짝이 맞는 w와 S_k로 공통 빔을 만들어 넣는다)은 두 구조 모두 같습니다.
- **부록(19~22쪽):** 예시 배열 값(4행 × 8열 × 2편파, 포트당 AE 4개, AE 간격 0.712λ, 포트 간격 2.848λ, 열 간격 0.541λ, 빔 틸트 6°)은 별도 작업에서 나온 값입니다. 20쪽 그래프는 그 값으로 세로 한 열을 계산한 것입니다(AE는 TR 38.901 근사 8 dBi · 65°, ‖w‖ = 1). 고정 tilt 6°에서 19.9 dBi @ 6°, 고정 tilt를 0°로 잘못 두면 위 13°에 12.1 dBi 로브가 남습니다. 21쪽의 포트 번호 순서는 그 작업이 *가정한* 순서이며 실제 순서는 벤더 확인이 필요합니다.
- **Sionna API:** Sionna RT 1.x 문서 기준입니다. `scene.tx_array`는 모든 송신기가 공유하고, 배열 안 소자는 같은 패턴을 씁니다. `RadioMapSolver`의 `precoding_vec`는 켤레 없이(전치) 곱합니다. radio map의 path gain은 경로 계수 크기 제곱의 합(비결맞음)입니다. 15쪽 코드는 의사 코드이므로 인자 이름과 기본값은 사용하는 버전의 문서로 확인하세요.
- **전력:** 200 W, 100 MHz, 30 kHz는 예시입니다. ss-PBCH-BlockPower가 포트당 값인지 합계인지, SSB 전력 부스팅이 있는지는 장비 · 망 설정마다 다릅니다.
- **실측 정렬:** 빈 크기 20~50 m와 18쪽의 오차 진단 표는 경험적 출발점입니다.

## 출처

- Sionna RT 문서: [RadioMapSolver (precoding_vec, 비결맞음 path gain)](https://nvlabs.github.io/sionna/rt/api/radio_map_solvers.html) · [Antenna patterns (AntennaPattern, register_antenna_pattern, PolarizedAntennaPattern, compute_gain)](https://nvlabs.github.io/sionna/rt/api/antenna_pattern.html) · [Scene (tx_array · rx_array는 모든 송신기 · 수신기 공통)](https://nvlabs.github.io/sionna/rt/api/scene.html) · [PathSolver (synthetic_array)](https://nvlabs.github.io/sionna/rt/api/paths_solvers.html) · [Radio devices (Transmitter: position · orientation · power_dbm)](https://nvlabs.github.io/sionna/rt/api/radio_devices.html)
- O-RAN M-Plane 사양 (ETSI TS 104 023) 15.4: BEAM-TILT 기능(predefined-beam-tilt-offset, run-time-tilt-offset-supported) · MODIFY-BF-CONFIG
- [Sionna RT: Technical Report (arXiv 2504.21719)](https://arxiv.org/abs/2504.21719) · [배열 소자가 같은 패턴을 써야 한다는 제약 언급 (arXiv 2604.14869)](https://arxiv.org/pdf/2604.14869)
- 디지털 tilt 범위와 위쪽 부엽: [Hybrid remote electrical tilt (US12289149B2)](https://patents.google.com/patent/US12289149) · 부배열 preset 하향각: [CEPT IMT-2020 wiki — Beamforming subarray AAS](https://wiki.cept.org/books/9a-imt-2020-module/page/beamforming-subarray-active-antenna-systems/export/markdown)
- 3GPP TR 38.901 7.3 (안테나 소자 패턴 · 패널 · TXRU 가상화, 부배열 θ_etilt) · TR 38.803 (AAS 부배열의 고정 전기 하향각) · TS 38.215 5.1.1 (SS-RSRP 정의) · TS 38.331 (ss-PBCH-BlockPower, 5.5.3 빔 통합 · L3 필터)
- 배열 안테나 일반: 배열 인자 · 그레이팅 로브 · 부배열(서브어레이) 구조 — 안테나 교재 (예: Balanis, *Antenna Theory*; Mailloux, *Phased Array Antenna Handbook*)
