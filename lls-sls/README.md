# LLS와 SLS

이동통신 연구·개발에서 쓰는 두 시뮬레이션을 다루는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **링크 레벨 시뮬레이션(LLS):** 링크 하나를 비트 단위로 깊게 봅니다.
- **시스템 레벨 시뮬레이션(SLS):** 망 전체를 슬롯 단위로 넓게 봅니다.

각각의 필요성, 발전 역사, 둘을 잇는 링크-시스템 매핑(L2S), 실무 활용법을 쉽게 설명합니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/6cJ2TKkggMETSV5Mv1CWhg, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/VnV964y7oLuExzMqrQKhy3
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py lls-sls`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 필요성: 왜 둘로 나누나 (엔진 시험대 vs 교통 시뮬레이션) | 0:50 |
| 3 | lls | LLS ①: 송신~복호 체인, BLER–SNR 곡선 | 0:50 |
| 4 | llshistory | LLS ②: 섀넌 → 터보 부호 → LTE · 5G 부호 선택 → GPU · AI | 0:50 |
| 5 | sls | SLS ①: 배치 · 채널 · 간섭 · MAC 동작 · 성공 판정 | 0:50 |
| 6 | slshistory | SLS ②: 스냅숏 → 동적 SLS → 평가 규칙 표준화 → 5G · 트윈 · AI | 0:50 |
| 7 | bridge | 링크-시스템 매핑: 유효 SINR(EESM · MIESM)과 BLER 표 | 0:55 |
| 8 | compare | LLS vs SLS 비교표, 대표 도구 | 0:45 |
| 9 | usells | LLS 활용: 언제 · 어떻게 · 함정 | 0:50 |
| 10 | usesls | SLS 활용: 언제 · 어떻게 · 함정 | 0:50 |
| 11 | together | 함께 쓰는 법: dB → % → 결정, 질문별 시작점 | 0:50 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 11쪽의 `[+__%]` (실제 SLS 결과)
- 마지막 장의 `[검토 중인 기능]`

참고할 점:
- 3쪽 BLER 곡선과 7쪽 L2S 그림은 개념도입니다.
- 역사 슬라이드의 연도는 대표 시점입니다.

## 출처

- Shannon, “A Mathematical Theory of Communication” (1948) · Berrou, Glavieux, Thitimajshima, 터보 부호 (ICC 1993)
- Gilhousen 외, “On the Capacity of a Cellular CDMA System” (IEEE TVT, 1991)
- Mehlführer, Ikuno, Wrulich, Rupp 외, [Vienna LTE simulators (EURASIP JASP 2011)](https://www.doi.org/10.1186/1687-6180-2011-29) · Rupp, Schwarz, Taranetz, [The Vienna LTE-Advanced Simulators (Springer, 2016)](https://www.springer.com/9789811006166) · [Vienna LTE-A uplink LLS (arXiv 1509.02351)](https://arxiv.org/pdf/1509.02351)
- ITU-R M.2135 (IMT-Advanced 평가 지침, 2008) · 3GPP TR 36.814 · ITU-R M.2412 (IMT-2020 평가 지침, 2017) · 3GPP TR 38.901
- PHY 추상화: EESM (Ericsson 3GPP 기고, 2003) · MIESM (Brueninghaus 외, PIMRC 2005) · [NR PHY abstraction for system-level simulation (arXiv 2001.10309)](https://arxiv.org/pdf/2001.10309) · [OAI PHY abstraction (EURECOM)](https://www.eurecom.edu/fr/node/4904012)
- 도구: MATLAB 5G Toolbox · ns-3 5G-LENA · Vienna 5G LLS/SLS · OpenAirInterface · Sionna (PHY 2022, SYS 2025) · [Sionna SYS 사용 연구 예 (arXiv 2605.29772)](https://arxiv.org/pdf/2605.29772)
