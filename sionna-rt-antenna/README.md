# Sionna RT 안테나의 물리적 특성

Sionna RT에서 안테나의 물리적 특성을 정하는 파라미터를 설명하는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다. 세 층으로 나눠 설명합니다.

- **소자:** `pattern`(방사 패턴), `polarization` · `polarization_model`(편파)
- **배열:** `num_rows` · `num_cols` · `vertical_spacing` · `horizontal_spacing`(소자 수와 간격), 임의 배치는 `AntennaArray`
- **설치:** 송수신기의 `position` · `orientation` · `look_at`(정면 방향과 틸트)
- **공통:** `scene.frequency`(간격의 실제 길이), `PathSolver`의 `synthetic_array`(소자별 계산 여부)

마지막에 실제 안테나를 Sionna로 옮길 때 생기는 단순화를 정리했습니다. 배열 축소(소자 수를 줄임)와 상세 손실(측정 패턴 · 틸트 · 결합 등을 내장 수식으로 대체)입니다. 이 두 용어는 Sionna API 이름이 아니라 변환 과정을 설명하려고 쓴 개념입니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/DDGLy8CqcBftjHxNitdDUP, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/3bjwWMN2inzHhAc3dCLkBv
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sionna-rt-antenna`로 뷰어를 다시 만듭니다.
- 입력 전체 지도는 [`../sionna-rt-inputs/`](../sionna-rt-inputs/) 덱, 그중 5쪽(안테나 배열)을 자세히 푼 자료입니다.

## 구성 (≈ 9분 40초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | map | 파라미터 지도: 소자 · 배열 · 설치 · 공통 | 0:50 |
| 3 | frame | 안테나 좌표계: 정면 x축, 배열은 y–z 평면, column-first 번호, θ · φ | 0:50 |
| 4 | pattern | pattern: 정의, 내장 네 가지(iso · dipole · hw_dipole · tr38901)와 이득, compute_gain | 0:55 |
| 5 | tr38901 | tr38901 패턴 식과 수평 단면 극좌표 그림 (8 dBi · 65° · 30 dB) | 0:50 |
| 6 | polarization | polarization: V · H · VH · cross 기울기 각, array_size와 num_ant | 0:55 |
| 7 | polmodel | polarization_model 두 가지와 편파 불일치 · 반사 · 산란의 효과 | 0:50 |
| 8 | spacing | spacing: 파장 배수, 3.5 / 28 GHz 실제 길이, 빔폭 · 격자 엽 · 상관 | 0:55 |
| 9 | orientation | orientation (α, β, γ) · look_at, 3섹터 · 기계적 틸트, 전기적 틸트는 가중치로 | 0:50 |
| 10 | code | 설정 코드와 확인(compute_gain · show · positions), synthetic_array | 0:55 |
| 11 | limits | Sionna 안테나 모델이 생략하는 것: 배열 축소 · 상세 손실과 메우는 방법 | 0:55 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 장비]`

참고할 점:
- 파라미터 이름 · 기본값 · 내장 패턴 상수는 Sionna RT 문서와 소스(`sionna-rt` 2.2.0)에서 확인했습니다. 편파 기울기 각: V 0, H π/2, VH [0, π/2], cross [−π/4, π/4]. tr38901 상수: 65° · 30 dB · 8 dBi. 다이폴 계수: √1.5 · √1.643.
- 4쪽 compute_gain 값(지향성 9.83 dB · 이득 8.0 dB · 효율 65.7%)은 문서의 예제 출력입니다.
- 8쪽 빔폭(약 13°)은 균일 선형 배열 근사식 0.886 λ / (N·d)로 계산했습니다. 10쪽 44 m는 원역장 거리 2D²/λ(32열 × 0.5λ, 3.5 GHz)입니다.
- 9쪽 기울기 부호(β > 0이면 아래로)는 문서의 회전 정의에서 따른 것입니다. 실제 장면에서는 미리보기로 한 번 확인하기를 권합니다.
- 11쪽 소자 · 포트 수(192 → 64 → 1)는 예시입니다.

## 출처

- Sionna RT API 문서: [Antenna Arrays](https://nvlabs.github.io/sionna/rt/api/antenna_array.html) · [Antenna Patterns](https://nvlabs.github.io/sionna/rt/api/antenna_pattern.html) · [Radio Devices](https://nvlabs.github.io/sionna/rt/api/radio_devices.html) · [Path Solvers](https://nvlabs.github.io/sionna/rt/api/paths_solvers.html) · [Custom Antenna Patterns (개발자 가이드)](https://nvlabs.github.io/sionna/rt/developer/dev_custom_antenna_patterns.html)
- Sionna RT 소스: [antenna_pattern.py](https://github.com/NVlabs/sionna-rt/blob/main/src/sionna/rt/antenna_pattern.py) · [antenna_array.py](https://github.com/NVlabs/sionna-rt/blob/main/src/sionna/rt/antenna_array.py)
- 3GPP TR 38.901 — 7.3절 안테나 모델(Table 7.3-1, 편파 모델 식 7.3-3 · 7.3-4/5)
- C. A. Balanis, *Antenna Theory* — 짧은 다이폴 · 반파장 다이폴 패턴, 배열 빔폭
