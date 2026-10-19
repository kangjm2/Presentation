# Sionna RT 입력 데이터

Sionna RT로 채널 데이터(CIR · CFR · 탭)를 만들 때 무엇을 넣는지 정리한 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다. 입력을 세 묶음, 여섯 가지로 나눠 설명합니다.

- **환경:** ① 장면(Mitsuba XML + 메시), ② 재질(ITU 재질, 산란 계수)
- **링크:** ③ 안테나 배열(PlanarArray), ④ 송수신기(위치 · 방향 · 속도 · 전력)
- **조건:** ⑤ 주파수와 대역, ⑥ 솔버 설정(PathSolver)

이어서 여섯 입력이 들어간 최소 코드, 입력이 출력 텐서의 차원을 어떻게 정하는지, 흔한 실수 점검표를 다룹니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/2kxYTU3xzxKvQJkWGWAmdy, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/LqW7ATHFvcp2q7VoUpTgqR
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sionna-rt-inputs`로 뷰어를 다시 만듭니다.
- 경로 계산 원리(광선 추적, SBR · 이미지법)는 [`../ray-tracing/`](../ray-tracing/), CIR · CFR 변환은 [`../sionna-channel/`](../sionna-channel/) 덱과 이어집니다.

## 구성 (≈ 9분 30초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | 입력 지도: 여섯 입력 → PathSolver → cir · cfr · taps, 환경 · 링크 · 조건 | 0:50 |
| 3 | scene | ① 장면: Mitsuba XML 구조, load_scene, 내장 장면, OSM → Blender, merge_shapes | 0:55 |
| 4 | material | ② 재질: ITURadioMaterial 파라미터, 산란은 솔버 스위치와 함께 | 0:55 |
| 5 | antenna | ③ 안테나 배열: PlanarArray, 장면 단위 공유, 2×4 교차 편파 = 16 | 0:50 |
| 6 | devices | ④ 송수신기: position · orientation/look_at · velocity · power_dbm | 0:50 |
| 7 | frequency | ⑤ 주파수: frequency · bandwidth · temperature, 3.5 vs 28 GHz 콘크리트 | 0:45 |
| 8 | solver | ⑥ 솔버: max_depth, samples, 현상 스위치, synthetic_array, seed | 0:55 |
| 9 | code | 여섯 입력이 들어간 최소 코드 | 0:55 |
| 10 | shape | 출력 텐서 모양 [R, RA, T, TA, P]과 각 차원을 정하는 입력 | 0:50 |
| 11 | pitfalls | “경로가 안 나와요” 점검표 | 0:50 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 지역]`

참고할 점:
- API 이름, 기본값, 출력 모양은 `sionna-rt` 패키지 문서(작성 시점 최신 2.2.0)에서 확인했습니다. 버전에 따라 다를 수 있으니 발표 전에 사용하는 버전으로 확인하세요. Sionna 0.x의 `sionna.rt`(TensorFlow 기반)와는 API가 다릅니다.
- 9쪽 코드의 좌표와 물체 이름(`building_1`)은 예시입니다. 실제 장면에 맞게 바꿔야 합니다.
- 7쪽 도전율은 ITU-R P.2040 콘크리트 계수 예(σ = 0.0462 · f^0.7822, f는 GHz)로 계산한 값입니다.
- 3쪽 XML은 구조를 보여 주기 위한 단순화 예입니다.

## 출처

- Sionna RT API 문서 (https://nvlabs.github.io/sionna/rt/): [Path Solvers](https://nvlabs.github.io/sionna/rt/api/paths_solvers.html) · [Radio Map Solvers](https://nvlabs.github.io/sionna/rt/api/radio_map_solvers.html) · [Radio Materials](https://nvlabs.github.io/sionna/rt/api/radio_materials.html) · [Antenna Arrays](https://nvlabs.github.io/sionna/rt/api/antenna_array.html) · [Antenna Patterns](https://nvlabs.github.io/sionna/rt/api/antenna_pattern.html) · [Radio Devices](https://nvlabs.github.io/sionna/rt/api/radio_devices.html) · [Scene](https://nvlabs.github.io/sionna/rt/api/scene.html) · [Paths](https://nvlabs.github.io/sionna/rt/api/paths.html)
- [sionna-rt (PyPI)](https://pypi.org/project/sionna-rt/) — 버전 이력
- ITU-R P.2040, *Effects of building materials and structures on radiowave propagation above about 100 MHz* — 재질 파라미터
- 3GPP TR 38.901 — tr38901 안테나 패턴과 편파 모델
- Mitsuba 3 문서 — 장면 XML 형식
