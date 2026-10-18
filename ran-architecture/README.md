# 기지국 분리 구조와 인터페이스 (USM · CU · DU · RU · UE)

5G 기지국이 USM, CU, DU, RU로 나뉜 구조와, UE까지 포함해 이들을 잇는 인터페이스(Uu, 프런트홀, F1, E1, NG, Xn, O1·M-plane)를 다루는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/5zGukBbuNGCXm3jA2pWQo3, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/5qVFpj4sGxmN9CDD6YXsCv
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py ran-architecture`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | overview | 전체 구조도: UE–RU–DU–CU–5G 코어, USM 관리선 | 1:00 |
| 3 | why | 일체형 → BBU+RRH → CU+DU+RU → O-RAN·vRAN, 나누는 이유 | 0:50 |
| 4 | stack | 프로토콜 스택과 분할 지점 (Option 2 = F1, 7.2x = 프런트홀, 8 = CPRI) | 1:00 |
| 5 | roles | 다섯 장비의 역할 · 위치 · 시간 감각 | 0:50 |
| 6 | fronthaul | 프런트홀: C/U/S/M-plane, CPRI vs 7.2x, 요구 조건 | 1:00 |
| 7 | f1e1 | F1-C · F1-U · E1, CP/UP 분리 | 0:55 |
| 8 | ngxn | NG-C · NG-U · Xn, NAS 투명 전달, NSA | 0:50 |
| 9 | mgmt | USM 관리: O1, RU M-plane 계층형 vs 혼합형, FCAPS | 0:50 |
| 10 | flow | 단말 접속 메시지 흐름 (단순화한 9단계) | 1:00 |
| 11 | table | 인터페이스 요약표 | 0:40 |
| 12 | summary | 정리: 지연 요구가 경계를 정한다 | 0:30 |

**용어 가정:** USM은 CU·DU·RU를 관리하는 망 관리 시스템(EMS·OAM)으로 다뤘습니다. O-RAN 구조에서는 SMO의 관리 기능에 해당합니다. 실제 USM의 관리 프로토콜과 모델은 벤더 구현에 따라 다를 수 있습니다. 지연·거리 값은 대략적인 규모입니다. 표지의 `[발표자] · [소속] · [날짜]`는 직접 채워 넣으세요.
