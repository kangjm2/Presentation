# 레이 트레이싱: Sionna RT와 상용 툴

레이 트레이싱을 주제로 한 10분 세미나 자료입니다. 14장이고, 슬라이드마다 발표자 노트가 있습니다. 다루는 내용은 다음과 같습니다.

- 물리·전자기적 원리: 기하광학 근사, 반사·투과·회절·확산 산란, 재질, 경로 탐색 알고리즘
- **Sionna RT**의 처리 방식
- **Atoll · VIAVI** 등 상용 툴의 방식과 차이
- 학계에서 제안된 방식: 경로 탐색 가속·정확도 개선, 미분·학습 기반 방법
- Sionna의 한계와 개선 여지

**2026년 10월까지 공개된 자료 기준**입니다. Sionna RT는 2.2를 기준으로 했습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/KCkCGVJFK7unpn3zd7QbY4, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/NWxKLv1LReZ3LHg8rCaZaH
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py ray-tracing`로 뷰어를 다시 만듭니다.

## 구성 (≈ 11분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | geo | 원리 ①: 기하광학 근사, 거울상, 경로 합 = CIR | 0:45 |
| 3 | interact | 원리 ②: 정반사 · 투과 · 회절(UTD) · 확산 산란, ITU-R P.2040 재질 | 0:50 |
| 4 | search | 원리 ③: 이미지법 · SBR · 하이브리드 | 0:50 |
| 5 | sionna | Sionna RT ①: PathSolver 파이프라인, RadioMapSolver | 0:50 |
| 6 | diff | Sionna RT ②: 미분 가능성, 버전 흐름 (0.x → 2.2) | 0:45 |
| 7 | tools | 상용 툴: Atoll(Aster · CrossWave), VIAVI AI RSG, Wireless InSite X3D, WinProp IRT · DPM | 0:55 |
| 8 | compare | 비교표: 경로 탐색 · 출력 · 보정 · 규모 · 회절 · 미분 · 성격 | 0:45 |
| 9 | academic | 학계 ①: 빔 트레이싱, 광선 밀도 정규화, 가시성 전처리, GPU 가속, Min-Path-Tracing, 학습한 후보 생성 | 0:50 |
| 10 | learning | 학계 ②: 미분 RT 보정, 불연속 처리, 신경 대리 모델, 신경 레이 트레이싱, 신경 전파장(NeRF · 3DGS) | 0:55 |
| 11 | limits | Sionna의 한계: 물리 · 알고리즘 · 입력 · 운영 | 0:45 |
| 12 | improve | 개선 여지: 미분 기반 자동 보정, 장면 품질, 물리 보강, 하이브리드 규모 | 0:50 |
| 13 | choose | 목적별 선택과 교차 검증 | 0:35 |
| 14 | summary | 정리 | 0:30 |

10분에 맞추려면 9쪽(학계 ①)을 짧게 넘기거나, 7·8쪽을 함께 설명하세요.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 지역]`

참고할 점:
- **상용 툴 내부 알고리즘:** 공개 범위가 제한적이라 제품 자료 수준으로만 설명했습니다(특히 Atoll Aster, VIAVI).
- **발표자 의견:** 비교표(8쪽), 학계 연구 분류(9·10쪽), 목적별 선택(13쪽)은 발표자 정리입니다.

## 출처

- Sionna RT Technical Report, [arXiv 2504.21719](https://arxiv.org/abs/2504.21719) (PathSolver · RadioMapSolver 알고리즘, 제약 사항)
- [NVlabs/sionna-rt 릴리스 노트](https://github.com/NVlabs/sionna-rt/releases) (1.0 ~ 2.2) · [Sionna 1.0 발표](https://github.com/NVlabs/sionna/discussions/776) · [회절 복귀 논의 #838](https://github.com/NVlabs/sionna/discussions/838)
- Forsk, [Aster Propagation Model](https://www.forsk.com/aster-propagation-model) · [Atoll 5G NR](https://www.forsk.com/4g5g) · Aster 설명 [요약](https://www.azymuth.ru/en/suppliers/forsk/aster.html) · 사전 보정 언급 [arXiv 2201.12899](https://ar5iv.labs.arxiv.org/html/2201.12899)
- Orange, [Orange’s radio propagation model](https://hellofuture.orange.com/en/oranges-radio-propagation-model-an-essential-element-in-mobile-network-development) (CrossWave 배경)
- VIAVI, [TeraVM AI RSG](https://www.viavisolutions.com/en-uk/products/teravm-ai-rsg) · [Network Digital Twin](https://www.viavisolutions.com/en-us/solutions/network-digital-twin) · [AI RSG와 NVIDIA AODT 연동](https://blog.viavisolutions.com/2025/03/18/integrating-viavi-ai-rsg-with-nvidia-aerial-omniverse-digital-twin/)
- Remcom, [Wireless InSite high-fidelity ray tracing (X3D, exact path)](https://www.remcom.com/wireless-insite-em-propagation-software/high-fidelity-ray-tracing) · [Diffuse scattering](https://www.remcom.com/wireless-insite-em-propagation-software/diffuse-scattering)
- Altair WinProp, [Intelligent Ray Tracing](https://help.altair.com/Winprop/topics/winprop/user_guide/propagation_methods/propgation_models_urban_ray_models_irt.htm) · [3D IRT](https://help.altair.com/winprop/topics/winprop/user_guide/proman/propagation_models/proman_prop_projects_urban_3d_intel_model.htm)
- ITU-R P.2040 (건축 재료의 전파 특성) · UTD: Kouyoumjian & Pathak (1974) · 확산 산란: Degli-Esposti et al.
- 학계: Hoydis 외, [Learning Radio Environments by Differentiable Ray Tracing](https://arxiv.org/abs/2311.18558) · [NVlabs/diff-rt-calibration](https://github.com/NVlabs/diff-rt-calibration) · [학습 기반 전파 지도 튜토리얼 (arXiv 2603.17499)](https://arxiv.org/html/2603.17499v3) · [WRF-GS (arXiv 2412.04832)](https://arxiv.org/pdf/2412.04832) · [미분·동적 RT 비교 (arXiv 2410.14535)](https://arxiv.org/pdf/2410.14535)
- 학계 (서지 정보): Zhao 외, NeRF2 (MobiCom 2023) · Orekondy 외, WiNeRT (ICLR 2023) · Levie 외, RadioUNet (IEEE TWC 2021) · Eertmans 외, Min-Path-Tracing (EuCAP 2023), 불연속 스무딩 기반 미분 RT · DiffeRT (2024), 생성 모델 기반 경로 샘플링 (2025) · Didascalou 외, 광선 밀도 정규화 (IEEE TAP 2000) · Hoppe 외, Intelligent Ray Tracing (Stuttgart) · Egea-López 외, Opal GPU ray launching (2021)
