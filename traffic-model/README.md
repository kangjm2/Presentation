# 가상 UE와 트래픽 모델

통신사가 장비 적합성을 평가할 때 쓰는 시뮬레이션을 다루는 10분 세미나 자료입니다. 이 시뮬레이션은 가상 UE를 배치하고, 각 UE의 성능을 고려해 트래픽을 부여합니다. 자료는 그 배경과 함께, **UE를 배치하는 원리**(표준 드롭, 트래픽 지도, 단말 속성)와 **트래픽을 부여하는 원리**(트래픽 모델, 부하–체감 이론, 수요 환산)를 설명합니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/YaLSdZi1qZGVjeSREfgbYC, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/9dLK4V2kCiGbwE4bG6ZFsV
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py traffic-model`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 배경: 실망 시험의 한계, 커버리지·용량·품질 세 질문 | 0:50 |
| 3 | framework | 시스템 레벨 시뮬레이션: 네 입력, 엔진, 세 출력 | 0:50 |
| 4 | drop | UE 배치 ①: 육각 격자 드롭, 38.901 시나리오 파라미터, 랩어라운드 | 1:00 |
| 5 | spatial | UE 배치 ②: 트래픽 지도 기반 비균일 배치 | 0:55 |
| 6 | profile | UE 배치 ③: 단말 능력·위치 속성·서비스 프로필, 단말 믹스 | 0:50 |
| 7 | models | 트래픽 부여 ①: Full buffer · FTP · VoIP · 비디오/XR | 0:55 |
| 8 | load | 트래픽 부여 ②: 부하율 ρ와 체감 C(1 − ρ) | 1:00 |
| 9 | demand | 트래픽 부여 ③: 월 사용량 → 최번시 제공 부하 → UE별 λ | 0:55 |
| 10 | evaluate | 판정 기준과 부하 스윕 | 0:55 |
| 11 | trust | 보정, 통계적 수렴, 실망 비교, 민감도 분석 | 0:45 |
| 12 | summary | 정리 | 0:30 |

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 6·9·10쪽의 `[__%]`, `[__ Mbps]` 같은 사업자 기준값
- 마지막 장의 `[대상 지역]`

참고할 점:
- 9·10쪽의 계산 예(월 30 GB, 셀 용량 400 Mbps, 스윕 결과)는 모두 설명용 가상 수치입니다.
- 8쪽의 C(1 − ρ)는 처리기 공유 큐 근사입니다. 경향을 설명하는 용도이며, 실제 값은 시뮬레이션으로 구합니다.

## 출처

- 3GPP TR 38.901 Table 7.2-1 (UMa/UMi/InH 배치 파라미터), 7.4.3 (건물 침투 손실)
- 3GPP TR 38.913 (Dense Urban 등 평가 시나리오: TRxP당 10 UE, 실내 80%·실외 20%) · [6.1.2 사본](https://itecspec.com/3gpp/38.913/s/6.1.2)
- 3GPP TR 36.814 Annex A (FTP·VoIP 트래픽 모델) · TR 36.825 A.7의 [FTP model 1 파라미터 요약](https://www.itecspec.com/3gpp/36.825/s/a.7) (파일 0.5 / 2 MB, Poisson 도착)
- MathWorks, [FTP 트래픽 패턴 생성 예제](https://www.mathworks.com/help/wireless-network/ug/generate-and-visualize-ftp-application-traffic-pattern.html) (FTP model 2/3 설명)
- 3GPP TR 38.838 (XR 트래픽 모델) · TS 38.306 (단말 능력) · TS 38.101-1 (전력 등급)
- ITU-R M.2412 (IMT-2020 평가 지침: 시험 환경, full buffer 평가)
- 처리기 공유(processor sharing) 큐에 기반한 flow-level 용량 모델: 셀 용량 C, 부하율 ρ일 때 평균 처리량 ≈ C(1 − ρ)
