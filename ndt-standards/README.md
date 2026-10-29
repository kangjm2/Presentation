# 네트워크 디지털 트윈 표준 · 참조 구조

네트워크 디지털 트윈(NDT)을 다루는 표준과 참조 구조를 정리한 자료입니다. 우리 플랫폼을 남에게 설명할 때 쓸 **공통 어휘**를 얻고, 표준이 **정하지 않고 비워 둔 것**(정확도 기준 · 전파 모델 충실도 · 동기화 주기 · 검증 방법)을 찾는 것이 목적입니다. **2026년 10월까지 공개된 자료 기준**입니다.

다루는 내용은 다음과 같습니다.

- 표준 지도: 2022년부터 지금까지 기관별 문서와 날짜
- 뼈대: ITU-T Y.3090의 3층 · 3영역 · 이중 폐루프 구조와 네 요소(데이터 · 매핑 · 모델 · 인터페이스)
- IRTF NMRG 초안: 다섯째 요소(로직), 구성 요소 셋, 매핑 두 종류, 상태(RFC 전)
- 3GPP SA5: TR 28.915 → TS 28.561 → TR 28.883, 관리 서비스(NDTFunction · NDTJob · NDTReport), 동기화 입력
- ETSI ZSM(GR 015 · GS 018)과 O-RAN nGRG 보고서(RR-2024-07 · RR-2024-09)
- 두 사다리: ITU-T Y.3091 트윈 능력 레벨(L1~L5)과 TM Forum 자율 망 레벨(L0~L5)
- 표준 비교표, 용어 여섯(물리 트윈 · 트윈 개체 · 매핑 · 충실도 · 동기화 · 작업/세션)
- 우리 플랫폼을 Y.3090 그림 위에 얹은 예시
- 표준이 정하지 않는 것 → 같은 시리즈의 `twin-vv` · `twin-data-sync` 덱으로 연결

13장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/7zxtU5wXsYkgevv3zqKrkk, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/SFMUL4ssnBpkh3KeTPWXxd
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py ndt-standards`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`network-digital-twin`](../network-digital-twin/): 업계 동향 · 트윈의 네 층 · AODT
  - [`knowledge-loop`](../knowledge-loop/): 보정 루프 · 운영 루프, 자율 레벨
  - [`twin-vv`](../twin-vv/): 트윈 검증 · 정확도 합격선 (12쪽에서 연결)
  - [`twin-data-sync`](../twin-data-sync/): 트윈 데이터 동기화 · 갱신 주기 (12쪽에서 연결)
  - [`dt-breakdown`](../dt-breakdown/) · [`debiased-rmse`](../debiased-rmse/): 충실도를 재는 지표
  - [`coord-registration`](../coord-registration/): 매핑의 기초인 좌표 정합

## 구성 (≈ 10분 15초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | why | 표준 어휘의 쓰임(설명 · 비교 · 빈칸 찾기), 트윈 ≠ 시뮬레이터, 순서 | 0:40 |
| 3 | landscape | 표준 지도(연표): ITU-T · IRTF · 3GPP · ETSI · O-RAN | 0:45 |
| 4 | y3090 | Y.3090 참조 구조: 3층 · 3영역 · 이중 폐루프 | 0:55 |
| 5 | elements | 네 요소 + IETF NMRG 초안(로직 · 구성 요소 · 매핑 종류 · 상태) | 0:50 |
| 6 | sa5 | 3GPP SA5: 문서 셋, NDT 관리 서비스, 동기화 입력, 범위 밖 | 0:55 |
| 7 | zsm-oran | ETSI ZSM(세션 · 충실도 · 정확도 용어) · O-RAN nGRG(사용 사례 · 요소 기술 · 보정 루프) | 0:55 |
| 8 | levels | Y.3091 트윈 능력 L1~L5 vs TM Forum 자율 망 L0~L5 | 0:50 |
| 9 | compare | 기관 · 문서 · 종류/상태 · 범위 비교표 | 0:50 |
| 10 | glossary | 용어 여섯과 우리 말 | 0:45 |
| 11 | mapping | 우리 플랫폼을 Y.3090 그림에 얹은 예시, Y.3091로 본 위치 | 0:55 |
| 12 | gaps | 표준이 정하지 않는 것 네 가지 → twin-vv · twin-data-sync | 0:55 |
| 13 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 9쪽(비교표)을 백업으로 돌리세요. 약 9분 25초가 됩니다. 3쪽 연표와 12쪽에서 같은 내용을 짚습니다.
- 표준 문서를 자주 읽는 청중이면 9쪽 대신 10쪽(용어)을 빼도 됩니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 11쪽(우리 플랫폼 대입)의 구성 요소와 판단: 데이터 · 모델 · 관리 영역에 실제로 있는 것, 남향 수집이 배치인지 자동인지, Y.3091 레벨 판단
- 10쪽 “우리 플랫폼에서” 열의 예
- `twin-vv` · `twin-data-sync` 덱이 머지되면 위 관련 덱 목록을 링크로 바꾸기

참고할 점:
- **문서 번호 · 날짜 · 상태:** 2026년 10월에 각 기관의 공식 페이지에서 확인했습니다.
  - ITU-T: Y.3090(2022.02.13 승인), Y.3091(12/2023), Y.3092(09/2024), Y.3093(2025.08.29 승인), Y.3094(2026.04.13 승인), 모두 시행 중(In force). Y.3091 · 3092의 정확한 승인일은 판 표기(월/년)만 확인했습니다.
  - IRTF NMRG: draft-irtf-nmrg-network-digital-twin-arch-13(2026.07.01), 정보성(Informational), datatracker 상태 “Waiting for IRTF Chair”(2026.09.24 갱신). RFC 번호는 없습니다.
  - 3GPP: TR 28.915 v19.0.0(SA#106, 2024.12), TS 28.561 v19.0.0(SA#109, 2025.10) → v20.2.0(SA#113, 2026.09), TR 28.883 v20.0.0(SA#111, 2026.03). TR 28.915의 ETSI 판 날짜는 자료마다 달라 3GPP 포털 기준으로 적었습니다.
  - ETSI: GR ZSM 015 V1.1.1(2024-02), GS ZSM 018 V1.1.1(2024-12).
  - O-RAN nGRG: RR-2024-07 “Digital Twin RAN Use Cases”(2024.07), RR-2024-09 “Digital Twin RAN: Key Enablers”(2024.10). 연구 보고서이며 규격이 아닙니다.
- **문구:** 슬라이드의 표준 문구는 모두 요약 · 번역입니다. 직접 인용이나 절 번호는 원문에서 확인한 것만 적었습니다(Y.3090 6 · 8절, Y.3091 표 7-1 · 8.2절, TS 28.561 4.3절, ZSM 015 4.3 · 5.14 · 6.3.10절).
- **ETSI ENI:** 트윈 관련 작업이 있는지 확인하지 못해 넣지 않았습니다.
- **TM Forum 레벨(8쪽):** 레벨 이름 · 설명은 TM Forum 원문(IG1218 · IG1252)이 아니라, IBM IBV와 TM Forum이 함께 낸 2025년 보고서 “Navigating autonomous networks”의 그림 1(정의 출처: TM Forum)을 따랐습니다. 평균 1.9도 같은 조사입니다. `knowledge-loop` 덱의 “대부분 L2~L3”(TM Forum 2026 조사)와는 조사가 다릅니다.
- **해석 · 예시(발표자 의견):**
  - 8쪽 “트윈이 L3 → L4를 받쳐 준다”는 해석입니다. 표준 문구는 3GPP의 “자동화의 빈칸은 망 행동 모델링”, ETSI의 “트윈 정보를 자동화 루프에 쓴다” 정도입니다.
  - 11쪽 우리 플랫폼 대입과 Y.3091 판단(엄밀히 L1)은 예시입니다. 내부 루프 · 외부 루프 구분은 `knowledge-loop` 15쪽의 두 루프를 Y.3090의 이중 루프에 맞춘 것입니다.
- **계산값 없음:** 이 덱의 그림은 모두 손으로 그린 구조도이며, 계산으로 만든 수치는 없습니다.

## 출처

ITU-T (SG13)
- Recommendation ITU-T Y.3090 (02/2022), Digital twin network – Requirements and architecture — https://www.itu.int/rec/T-REC-Y.3090
- ITU-T Y.3091 (12/2023), Digital twin network – Capability levels and evaluation methods — https://www.itu.int/rec/T-REC-Y.3091
- ITU-T Y.3092 (09/2024), Digital twin for management and orchestration in IMT-2020 networks and beyond — https://www.itu.int/rec/T-REC-Y.3092
- ITU-T Y.3093 (08/2025), Digital twin networks – Framework and functional requirements of the data domain in the network digital twin layer — https://www.itu.int/rec/T-REC-Y.3093
- ITU-T Y.3094 (04/2026), Digital twin networks – General technical requirements of the model domain in the digital twin layer — https://www.itu.int/rec/T-REC-Y.3094

IETF / IRTF
- C. Zhou et al., “Network Digital Twin (NDT): Concepts and Reference Architecture,” draft-irtf-nmrg-network-digital-twin-arch-13 (2026.07) — https://datatracker.ietf.org/doc/draft-irtf-nmrg-network-digital-twin-arch/

3GPP (SA5)
- TR 28.915, Study on management aspect of Network Digital Twin (Rel-19) — https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4263
- TS 28.561, Management and orchestration; Management aspects of Network Digital Twins (Rel-19 · 20) — https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4384 · ETSI TS 128 561 V19.0.0 (2025-10)
- TR 28.883, Study on management aspects of Network Digital Twin phase 2 (Rel-20) — https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4428
- Y. Hu, “The Network Digital Twin: Enabling Network Intelligence and Automation,” 3GPP Highlights (2025.12) — https://www.3gpp.org/technologies/digital-twin1

ETSI (ISG ZSM)
- ETSI GR ZSM 015 V1.1.1 (2024-02), Network Digital Twin — https://www.etsi.org/deliver/etsi_gr/ZSM/001_099/015/01.01.01_60/gr_ZSM015v010101p.pdf
- ETSI GS ZSM 018 V1.1.1 (2024-12), Network Digital Twin for enhanced zero-touch network and service management — https://www.etsi.org/deliver/etsi_gs/ZSM/001_099/018/01.01.01_60/gs_zsm018v010101p.pdf

O-RAN Alliance (nGRG)
- Digital Twin RAN Use Cases, RR-2024-07 — https://www.o-ran.org/research-reports/digital-twin-ran-use-cases
- Digital Twin RAN: Key Enablers, RR-2024-09 — https://mediastorage.o-ran.org/ngrg-rr/nGRG-RS01-RS03-Digital%20Twin%20Key%20Enabling%20Technologies%20Research%20Report.pdf

TM Forum
- IBM Institute for Business Value · TM Forum, “Navigating autonomous networks” (2025) — 그림 1 레벨 정의(출처 TM Forum), 평균 1.9
