---
author_role: representative
author_name: 대표님
created_at: 2026-08-19
status: saved
source: conversation
---

# PMS 자사몰 코어 구축·자동화 개발 운영안

## 아이디어

PMS Automation Platform v1.0의 자사몰 코어 구축은 AI 기능을 먼저 만드는 방식이 아니라, **0차 데이터 파이프라인·측정 복구 → 1차 Customer/Product/Inventory/Order Master → 운영 자동화 → CRM → Intelligence/AI** 순서로 진행한다.

핵심은 실제 매출·재고·고객 데이터와 측정 기반이 없는 상태에서 AI Layer부터 개발해 재작업하는 것을 막고, Customer Master와 핵심 운영 원장을 중심으로 자동화 플랫폼의 기반을 먼저 구축하는 것이다.

첨부 문서는 개발사 킥오프에서 범위·순서·견적·책임·DoD를 결정하기 위한 업무계획서/지침서이며, Revenue SEO OS까지 개발 요구사항으로 연결한다. fileciteturn1file0

## 목적 / 기대효과

- Cafe24·POS·ERP·매장고객·카카오 접점을 Customer Master로 통합해 고객자산을 1인 1ID 구조로 관리
- 국내재고와 글로벌 공급재고를 분리한 Product/Inventory Master 구축
- OMS·WMS·Realpacking·RMA·CS를 연결해 주문·출고·반품·상담 운영의 수기 의존도를 축소
- CRM Trigger Engine이 고객·상품·재고·마진·동의 상태를 근거로 발송 후보를 만들고 사람 승인 후 실행
- 대표 Dashboard에서 고객·상품기회·주문·서비스·수익을 한 화면으로 확인
- SEO를 단순 유입이 아니라 상품 소싱·판매 판단용 데이터 센서로 운영하고, 주문·기여이익·CRM 재구매 데이터를 다시 소싱 판단에 환류
- AI가 금액·재고·환불·가격을 직접 변경하지 않고 Rule Engine과 승인 게이트를 거치는 통제 구조 확립

## 핵심 개발 원칙

1. 데이터 파이프라인과 Customer Master를 AI보다 먼저 구축한다.
2. 확인되지 않은 값을 실측 필드에 넣지 않고 UNVERIFIED로 관리한다.
3. 모든 상태 변화는 audit log로 남긴다.
4. 외부 API는 1차 읽기 전용으로 시작하고 쓰기는 3개월 무사고 후 재검토한다.
5. L1/L2/L3 권한을 분리하고 금액·고객·법적 위험이 있는 L3는 사람 승인을 필수로 한다.
6. 기능 제작 여부가 아니라 DoD 통과 여부로 완료를 판단한다.

## 개발 순서 후보

- 0차: 데이터 파이프라인 + GA4/픽셀/canonical/robots 등 측정 복구
- 1차: Customer / Product / Inventory / Order Master
- 2차: OMS / WMS / Realpacking / RMA / CS
- 3차: 고객등급 / Segment / CRM Trigger / First Access
- 4차: Customer Match / Value Engine / AI Buyer
- 5차: 공급처 선택·가격감지·추천학습·수요예측 고도화

문서상 목표 일정은 2026-08-19부터 2027년 상반기까지 단계별 초안으로 제시되어 있으나, **개발사 견적 수령 후 날짜를 확정**하도록 되어 있다. fileciteturn1file0

## 핵심 하드게이트

- Cafe24 Admin API 읽기 앱(Client ID) 증빙
- 매출·재고·고객 실데이터 적재
- GA4·픽셀 측정 복구 및 테스트 주문 검증
- 4개 매장 카카오톡 대화기록 백업과 계정 명의자 확인
- 대표 URL·canonical 통일
- 0차 견적 1,000,000원 상한
- 총 투자금 가용현금 30% 초과 시 중단
- 소스코드·DB 회사 명의 소유권 미확보 시 계약 보류

## 관련 업무

첨부 문서가 제시한 대표 우선 액션:

- 2026-08-19: Cafe24 개발자센터 읽기 전용 앱 등록 또는 위탁 진행 결정
- 2026-08-21: 개발사 견적 요청 10항목 발송
- 2026-08-24: 4개 매장 카카오톡 대화 전수 백업 완료
- 2026-09-05: 측정 복구 검증 + 1차 SRS 확정
- 2026-09-15: 이관율·채널톡 유료전환 판단

이 아이디어 기록을 저장하는 것 자체는 위 일정의 실행 완료나 회사 공식 요구사항 확정을 의미하지 않는다.

## 아직 미정인 부분

- 데이터 파이프라인 책임 주체: 내부 수행 vs 위탁
- 1차 개발의 실제 견적·기간·투입 인력·유지보수 조건
- 기존 Cafe24 코드 분석 계약 범위의 포함 여부
- Cafe24 API 쓰기 권한이 향후 실제로 필요한 범위
- SKU별 실원가·순마진율과 채널별 기여이익
- 매장별 카카오톡 활성 고객 수와 실제 수신동의율
- 실제 데이터 적재·측정 검증 결과

## 관련 자료

- original 예정 경로: `materials/originals/representative/ideas/2026-08-19/PMS_자사몰코어구축_자동화_개발미팅_업무계획서_지침서_v1.0_20260819.docx`
  - 저장 상태: **미저장** — 현재 연결된 GitHub 액션에 로컬 바이너리 파일을 원본 바이트 그대로 업로드할 file-parameter 기능이 없어 변형 저장을 하지 않음
  - 원본 SHA-256: `70775259c4a262821043c49d2feb5a74fcb74dc1f1875040d72037a2c846ac5d`
- normalized: `materials/normalized/representative/ideas/2026-08-19/PMS_자사몰코어구축_자동화_개발미팅_업무계획서_지침서_v1.0_20260819.docx.md`

## 상태 주의

`status: saved`는 대표님의 아이디어/자료가 보존되었다는 의미이며, `llm-source/`, `working/CURRENT_WORK.md`, 요구사항 changelog에는 자동 반영하지 않는다. 문서 내부에 ‘확정’이라고 표현된 항목도 본 `/아이디어저장`만으로 회사 공식 기준이 되지 않는다.
