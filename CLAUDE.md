# Presentation

최대 10분 발표용 시각 자료를 만드는 리포지토리. 주제마다 폴더 하나 (예: `propagation-models/`).

## Git 기본 룰

- **작업이 끝나면 항상 main에 머지한다.** 지정된 작업 브랜치에 커밋·푸시 → main 대상 PR 생성 → merge commit 방식으로 머지. 사용자에게 따로 묻지 않는다.
- 이미 머지된 브랜치에서 후속 작업을 할 때는 브랜치를 최신 main에서 다시 시작한다 (`git fetch origin main && git checkout -B <branch> origin/main`).

## 폴더 구성 (주제별)

- `project/deck.json`, `project/slides/<id>.html`: Slides 아티팩트의 원본. 슬라이드 1장 = 파일 1개, `<aside>` = 발표자 노트
- `viewer/`: 내비게이션이 있는 단독 뷰어 템플릿과 빌드 스크립트. 슬라이드를 고친 뒤 `python3 viewer/build.py`로 `presentation.html`을 다시 만든다
- `README.md`: 아티팩트 링크, 슬라이드 구성과 시간 배분
- `qna.md`: 슬라이드별 예상 질문과 답변 (`qna-easy.md`: 신입 사원용 쉬운 요약본)
