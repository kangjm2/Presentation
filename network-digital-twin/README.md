# 네트워크 디지털 트윈 동향

네트워크 디지털 트윈(NDT)을 둘러싼 경쟁·협력 구도, NVIDIA Aerial Omniverse Digital Twin(AODT)의 장점과 한계, 그리고 VIAVI TM500/E500 같은 UE 시뮬레이션 도구를 다루는 10분 세미나 자료입니다. 12장이고, 슬라이드마다 발표자 노트가 있습니다. **2026년 10월까지 공개된 자료 기준**입니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/9xcMPHaixBfRQx4WGivwB9, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/QXpT8THoXdp2bmoUQYUYrd
- 두 링크 모두 비공개 — 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py network-digital-twin`로 뷰어를 다시 만듭니다.

## 구성 (≈ 10분)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | concept | 트윈의 네 층 (환경·망·단말·운영)과 실망 동기화 | 0:50 |
| 3 | whynow | 왜 지금: AI-RAN, 6G, GPU 가속 · 2025.10–2026.10 주요 사건 | 0:50 |
| 4 | landscape | 층별 지도: 누가 어느 층을 맡나 | 0:50 |
| 5 | aodt | NVIDIA AODT 구성과 최근 버전 | 0:50 |
| 6 | strengths | NVIDIA의 강점 4가지 | 0:50 |
| 7 | limits | AODT 한계 (RAN·UE 스택, EM 모델, 규모, 하드웨어, 데이터) | 0:55 |
| 8 | players | 회사별 움직임과 NVIDIA와의 관계 | 1:00 |
| 9 | ue | UE 에뮬레이터: TM500, E500, UeSIM, UE Simbox | 0:55 |
| 10 | combo | 사례: KDDI RAN Digital Twin의 4사 조합 | 0:50 |
| 11 | choose | 목적별 조합과 위험 요인 | 0:50 |
| 12 | summary | 정리 | 0:30 |

표지의 `[발표자] · [소속] · [날짜]`, 마지막 장의 `[검토할 시나리오]`는 직접 채워 넣으세요. 분류(4쪽)와 목적별 조합(11쪽)은 발표자 의견입니다.

## 출처

- NVIDIA, [Open Sources Aerial Software to Accelerate AI-Native 6G](https://blogs.nvidia.com/blog/open-source-aerial-ai-native-6g/) (2025.10)
- NVIDIA Developer Blog, [5 New Digital Twin Products Developers Can Use to Build 6G Networks](https://developer.nvidia.com/blog/5-new-digital-twin-products-developers-can-use-to-build-6g-networks/) (2026.2)
- NVIDIA AODT 문서: [설치·요구 사항](https://docs.nvidia.com/aerial/aerial-dt/text/installation.html?), [Additional Information (제약 사항)](https://docs.nvidia.com/aerial/aerial-dt/text/additional_info.html), [NGC 카탈로그](https://catalog.ngc.nvidia.com/orgs/nvidia/aerial/collections/aerial-omniverse-digital-twin/-)
- NVIDIA 포럼, [AI Aerial FAQ: Simulating 6G with AODT](https://forums.developer.nvidia.com/t/ai-aerial-faq-6-6-simulating-6g-with-nvidia-aerial-omniverse-digital-twin/373039)
- Nokia, [Nokia launches Nokia RAN Digital Twin … powered by NVIDIA AODT](https://www.nokia.com/blog/nokia-launches-nokia-ran-digital-twin-to-turbo-charge-ai-native-6g-powered-by-nvidia-aerial-omniverse-digital-twin/) (2026.2)
- KDDI, [News Release: RAN Digital Twin](https://newsroom.kddi.com/english/news/detail/kddi_nr-1068_4588.html) (2026.6) · [DCD 보도](https://www.datacenterdynamics.com/en/news/nvidia-and-samsung-to-power-6g-ready-digital-twin-for-japan-telecom-giant)
- Keysight·Samsung·NVIDIA, [End-to-End AI-RAN Validation Workflow](https://www.microwavejournal.com/articles/45435-keysight-and-samsung-demonstrate-end-to-end-ai-ran-validation-workflow-with-nvidia) (MWC 2026)
- Keysight, [Completes Acquisition of Spirent](https://www.businesswire.com/news/home/20251015993071/en/Keysight-Technologies-Completes-Acquisition-of-Spirent-Communications-PLC) (2025.10) · [UeSIM 제품 페이지](https://go.keysight.com/au/en/product/P8800S/uesim-ue-emulation-ran-solutions.html)
- VIAVI, [IMC 2026: 6G, AI-RAN, Digital Twins](https://www.bisinfotech.com/architecting-next-gen-telecommunications-viavi-on-6g-ai-ran-and-digital-twins-at-imc-2026/) · [TeraVM AI RAN Scenario Generator](https://www.telecomtv.com/content/ai/viavi-introduces-teravm-ai-ran-scenario-generator-52134/) · [Network Digital Twin](https://viavisolutions.com/fr-fr/node/123306) · [E500 Data Center Cabinet](https://www.viavisolutions.com/en-uk/literature/e500-data-center-cabinet-brochures-en.pdf) · [E500 카탈로그 요약](https://pdf.directindustry.com/pdf/viavi-solutions-uk-ltd/e500-data-center-cabinet/196288-1118156.html)
- Rohde & Schwarz·NVIDIA, [Digital twin testbed for AI-RAN at MWC 2026](https://satnews.com/2026/02/24/rohde-schwarz-nvidia-unveil-digital-twin-testbed-for-ai-ran-at-mwc-2026)
- Ericsson, [Site Digital Twin](https://ericsson.com/en/network-services/deployment/site-digital-twin)
- Huawei, [RAN Digital Twin System wins GSMA GLOMO](https://www.huawei.com/en/news/2024/2/ran-digital-twin-system-glomo) (2024)
- Amarisoft, [AMARI UE Simbox](https://amarisoft.com/products/test-measurements/amari-ue-simbox)
- O-RAN nGRG, [Digital Twin RAN: Key Enabling Technologies](https://mediastorage.o-ran.org/ngrg-rr/nGRG-RS01-RS03-Digital%20Twin%20Key%20Enabling%20Technologies%20Research%20Report.pdf) (2024)
