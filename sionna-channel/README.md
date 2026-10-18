# Sionna 채널 데이터: CIR·CFR·FIR과 검증

Sionna로 만든 채널 데이터(CIR, CFR, FIR 탭)의 정의와 변환, 그리고 3GPP TR 38.901 통계 모델과 비교해 데이터를 검증하는 방법을 다루는 10분 발표 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/Wc2z7FTYMbejQPj6k2R6p5, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/J4zkPWSaHj4nqwPLa9DP9S
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py sionna-channel`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | pipeline | Scene → Ray tracing → CIR → CFR / FIR → 시뮬레이션 | 0:45 |
| 3 | cir | CIR: h(t,τ) = Σ a_i δ(τ − τ_i), a·τ 배열 모양 | 0:50 |
| 4 | cfr | CFR: H[k] = Σ a_i e^(−j2π f_k τ_i), 주파수 선택성 그림 | 0:50 |
| 5 | fir | FIR 탭: h[ℓ] = Σ a_i sinc(ℓ − Wτ_i), 탭 번짐 그림 | 0:55 |
| 6 | convert | 세 표현의 변환 관계 (정확 / 근사 / 역변환 불가) | 0:50 |
| 7 | code | Sionna RT 1.x 코드: `paths.cir()`, `paths.cfr()`, `paths.taps()` | 0:50 |
| 8 | pitfalls | 자주 하는 실수 여섯 가지 (정규화, 기준 지연·주파수, 탭 범위, CP, 시변) | 0:50 |
| 9 | sanity | 검증 ① 기본 점검: FSPL, LOS 지연, 에너지 일관성, 위상 기울기 | 0:50 |
| 10 | stats | 검증 ② 38.901 통계 비교: PL·SF, LOS 확률, DS, AS, K의 CDF | 1:00 |
| 11 | compare | 검증 ③ 공정한 비교 조건과 차이의 해석 | 0:55 |
| 12 | summary | 정리 | 0:30 |

그림의 경로·분포는 개념을 보여 주기 위한 모의 값입니다. 코드는 Sionna RT 1.x 기준이며, 함수·인자 이름과 기본값은 사용하는 버전의 문서로 확인하세요. 표지의 `[발표자] · [소속] · [날짜]`는 직접 채워 넣으세요.
