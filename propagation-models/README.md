# 전파 모델의 역사 (Propagation Models in Mobile Communications)

10분 발표용 슬라이드 (12장, 한국어, 슬라이드마다 발표자 노트 포함).

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/TosTPbda3dgsiJiYYG26LV, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/5NYpFjEa1nbEc3ShmzzKid
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 소스: `project/deck.json` (슬라이드 순서·섹션·폰트), `project/slides/<id>.html` (슬라이드 1장당 파일 1개, `<aside>` = 발표자 노트)

## 뷰어 조작

| 동작 | 키 / 버튼 |
|------|-----------|
| 다음 / 이전 | `→` `↓` `Space` `PageDown` / `←` `↑` `Shift+Space` `PageUp`, 하단 버튼, 슬라이드 클릭(왼쪽 30% = 이전), 스와이프 |
| 처음 / 끝 | `Home` / `End` |
| 번호로 이동 | 숫자 입력 후 `Enter`, 하단 목록에서 선택, 진행 막대 클릭 |
| 개요 (전체 썸네일) | `G` 또는 "개요" 버튼, `Esc`로 닫기 |
| 발표자 노트 | `N` 또는 "노트" 버튼 |
| 전체화면 | `F` 또는 "전체화면" 버튼 (하단 막대는 마우스를 멈추면 숨겨짐) |

주소 끝의 `#5`처럼 번호를 붙이면 해당 슬라이드에서 열립니다.

## 뷰어 다시 만들기

슬라이드 파일을 수정한 뒤:

```
python3 viewer/build.py
```

`viewer/template.html`(뷰어 UI)과 `project/`의 슬라이드를 합쳐 `presentation.html`을 다시 만듭니다.

## 구성 (≈ 9분 45초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 왜 전파 모델이 필요한가: 경로손실 · 쉐도잉 · 페이딩 | 0:50 |
| 3 | timeline | 1946–2025 계보: 경험적 / 확률적 / 결정론적 / 융합 | 1:00 |
| 4 | friis | ERA 1 자유공간(Friis)과 그 한계: 경로손실 지수 | 0:45 |
| 5 | hata | ERA 2 Okumura–Hata: 측정을 공식으로 | 1:00 |
| 6 | cost231 | ERA 3 COST 231: 2 GHz, 마이크로셀, Walfisch–Ikegami | 0:50 |
| 7 | fading | ERA 4 확률적 다중경로: Clarke/Jakes, TDL, Saleh–Valenzuela | 0:55 |
| 8 | gscm | ERA 5 MIMO와 GSCM: SCM → WINNER → 38.901 | 1:00 |
| 9 | raytracing | ERA 6 레이 트레이싱: GO + UTD, 위치 특정 채널 | 1:00 |
| 10 | compare | 세 계열 비교표 | 0:45 |
| 11 | fusion | 현재: 하이브리드 · 미분 가능 RT · 신경망 전파맵 · 6G | 0:50 |
| 12 | summary | 정리: 질문이 바뀌면 모델이 바뀐다 | 0:30 |

표지의 `[발표자] · [소속] · [날짜]`는 직접 채워 넣으세요.
