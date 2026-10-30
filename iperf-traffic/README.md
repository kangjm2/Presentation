# iperf3와 트래픽 시험: ping · TCP · UDP · FTP

드라이브 테스트나 단말 시험에서 흘리는 트래픽을 정리한 자료입니다. ping, iperf3, FTP가 어떤 길로 오가고 누가 응답하는지, TCP와 UDP는 무엇이 다른지, iperf3 숫자와 무선 처리량이 왜 서로 다른지를 다룹니다.

다루는 내용은 다음과 같습니다.

- 트래픽이 오가는 길: UE → RU → DU → CU → UPF → 서버
  - 응답하는 쪽은 서버입니다.
  - KPI는 세 곳에서 잡힙니다: UE DM 로그, 기지국 PM 카운터, 서버
- 구간별 패킷 모양: TCP/UDP/IP, 무선 머리말(PDCP · RLC · MAC), GTP-U 터널(F1-U · N3)
- 시험 트래픽 다섯 가지: ping · iperf3 TCP · iperf3 UDP · FTP · HTTP/영상
- ping(ICMP 에코), TCP(ACK · 창 · 혼잡 제어, 상한 ≈ 창 ÷ RTT), UDP(정한 속도 · 손실 · 지터)
- iperf3 구조(제어 연결 + 데이터 스트림), 방향(-R · --bidir), 명령과 결과 읽기
- FTP(제어 · 데이터 연결, 액티브 · 패시브)와 웹
- 앱 처리량과 무선 처리량의 차이, 시험 점검표

14장이고, 슬라이드마다 발표자 노트가 있습니다.

- **발표용 뷰어 (내비게이션 포함):** https://claude.ai/artifact/LoGJjVTuxLK9ZBZWALRmKY, 또는 로컬에서 `presentation.html`을 브라우저로 열기
- 편집용 Slides 덱: https://claude.ai/artifact/LDme7ykiqo4z9AmegeSsR5
- 두 링크 모두 비공개입니다. 다른 사람에게 보여주려면 페이지의 Share 메뉴에서 공유하세요.
- 예상 질문과 답변: [`qna.md`](qna.md) (슬라이드별)
- 뷰어 조작법은 [`../propagation-models/README.md`](../propagation-models/README.md#뷰어-조작)와 같습니다. 슬라이드를 고친 뒤 리포 루트에서 `python3 viewer/build.py iperf-traffic`로 뷰어를 다시 만듭니다.
- 관련 덱:
  - [`ue-kpi-pipeline`](../ue-kpi-pipeline/): 층별 처리량 · DM 로그가 KPI가 되는 과정
  - [`ue-kpi`](../ue-kpi/): 처리량 분해(RB · MCS · BLER)
  - [`upper-layers`](../upper-layers/): PDCP · RLC · MAC · RRC 상태
  - [`ran-architecture`](../ran-architecture/): RU · DU · CU · F1 · NG 인터페이스
  - [`traffic-model`](../traffic-model/): 시뮬레이션의 트래픽 모델
  - [`coord-registration`](../coord-registration/): 측정 위치 · 시각 정합

## 구성 (≈ 11분 20초)

| # | id | 내용 | 시간 |
|---|----|------|------|
| 1 | cover | 표지 | 0:20 |
| 2 | path | 트래픽이 오가는 길 (UL · DL), 응답은 서버, KPI는 세 곳 | 0:50 |
| 3 | stack | 구간별 패킷 모양: 단말 IP 패킷 · GTP-U 터널 · 무선 머리말, 프로토콜 번호 | 0:50 |
| 4 | kinds | 시험 트래픽 다섯 가지 비교 표 | 0:50 |
| 5 | ping | ICMP 에코, RTT에 들어가는 것, 첫 ping이 긴 이유 | 0:50 |
| 6 | tcp | 연결 3단계 · ACK · 흐름 제어 · 혼잡 제어 (개념도) | 0:55 |
| 7 | tcplimit | 처리량 상한 = 창 ÷ RTT (계산 그래프), BDP, Mathis 식 | 0:55 |
| 8 | udp | 보낸 속도 vs 받은 속도 (개념 계산), 손실 · 지터 | 0:50 |
| 9 | iperf | iperf3 구조, 방향(기본 · -R · --bidir), UE를 클라이언트로 두는 이유 | 0:50 |
| 10 | commands | 명령 예와 결과 읽기, 주요 옵션 | 0:55 |
| 11 | ftp | FTP 제어 · 데이터 연결, 액티브 · 패시브, 웹 · 영상 | 0:50 |
| 12 | layers | 앱 처리량과 무선 처리량이 다른 이유, KPI를 세는 곳 | 0:55 |
| 13 | checklist | 트래픽 시험 점검표 | 0:50 |
| 14 | summary | 정리와 다음 단계 | 0:40 |

- 10분 안에 맞추려면 3쪽(패킷 모양)과 13쪽(점검표)을 백업으로 돌리세요. 약 9분 40초가 됩니다.
- TCP를 잘 아는 청중이면 6쪽을 빼고 7쪽만 남겨도 됩니다.

직접 채워 넣을 부분:
- 표지의 `[발표자] · [소속] · [날짜]`
- 마지막 장의 `[대상 셀]`
- 10쪽 명령의 `SRV`(서버 주소)를 실제 시험 서버로

참고할 점:
- **사용자 질문의 구조 정리(2쪽):** 트래픽은 RU · CU에서 되돌아오지 않습니다. UPF를 지나 트래픽 서버까지 갔다가 서버가 응답합니다. 기지국은 패킷을 나르면서 무선 KPI를 남기고, UE의 DM 로그와 기지국 PM 카운터, 서버의 iperf3 결과가 각각 따로 숫자를 냅니다.
- **iperf3 사실(4 · 8 · 9 · 10쪽):** iperf3 공식 문서를 기준으로 했습니다.
  - 기본 포트 5201, 기본 방향은 클라이언트 → 서버, -R은 서버가 보냄
  - -u여도 제어 연결은 TCP, UDP 기본 속도 1 Mbit/s, -t 기본 10초
  - -l 기본: TCP 128 KB, UDP는 경로 MTU 기준(실패 시 1,460 B)
  - --bidir는 3.7(2019) 릴리스 노트, 지터 식은 iperf3 소스(iperf_udp.c, RFC 1889 방식)
  - 서버 하나가 한 번에 한 시험만 받는다는 점은 iperf3의 알려진 동작입니다(서버를 포트별로 여러 개 띄워 해결).
- **계산 · 예시:**
  - 7쪽 그래프는 창 ÷ RTT를 계산한 것입니다. Mathis 식 예는 MSS 1,448 B · RTT 20 ms · 손실률 10⁻⁴입니다.
  - 8쪽은 무선 용량 350 Mbps를 가정한 개념 계산입니다.
  - 6쪽 혼잡 창 그림은 개념도입니다.
  - 10쪽 출력의 숫자는 형식을 보여 주는 가상의 값입니다.
- **머리말 몫(12쪽):** MTU 1,500 B 기준입니다.
  - TCP는 IPv4 20 B + TCP 20 B + 타임스탬프 옵션 12 B를 뺀 1,448 B, UDP는 IPv4 20 B + UDP 8 B를 뺀 1,472 B입니다.
  - 무선 머리말 약 9 B는 PDCP · RLC · MAC 머리말을 각 3 B 정도로 본 예입니다. 순번 길이 · 설정에 따라 다릅니다.
  - 망이 단말에 내려 주는 MTU는 1,500보다 작을 수 있습니다.
- **기지국 처리량 카운터(12쪽):** DRB.UEThpDl은 TS 28.552 5.1.1.3.1의 평균 DL UE 처리량입니다. 큰 버스트를 대상으로, 보낼 데이터가 있던 시간 기준으로 셉니다. 세부 식은 릴리스마다 바뀌었으니 장비의 정의를 확인하세요.
- **점검표(13쪽):** 일반적인 시험 관행을 정리한 것입니다.

## 출처

- iperf3 문서, “Invoking iperf3” (software.es.net/iperf) · iperf3 3.7 릴리스 노트 · iperf3 소스 `iperf_udp.c`
- RFC 792 (ICMP), RFC 9293 (TCP), RFC 768 (UDP), RFC 7323 (TCP 창 크기 조절 · 타임스탬프), RFC 959 (FTP), RFC 9114 (HTTP/3)
- M. Mathis 외, “The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm,” ACM CCR, 1997
- 3GPP TS 28.552 5.1.1.3.1 (DRB.UEThpDl), TS 29.281 (GTP-U, UDP 포트 2152)
