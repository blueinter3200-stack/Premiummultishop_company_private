---
source_path: ".pi/사업계획서_텍스트모음/plans/pms-9-agent-revenue-commerce-os-v1-2026-08-15.md"
source_filename: "pms-9-agent-revenue-commerce-os-v1-2026-08-15.md"
source_type: "text"
source_size_bytes: 7799
source_modified_at: "2026-08-15T21:39:48+09:00"
source_sha256: "ed0e2dd7fad6e398c00b60a52a0eade4f7950b6d88314eede260e7e25e1e3fec"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Revenue Commerce OS — 9-Agent Operating Model v1.0

- 기준일: 2026-08-15
- 사업: Premium MultiShop
- 상태: 운영 구조 확정 / 실제 연동은 별도 권한·데이터 검증 필요

## 1. 목적

PMS는 AI 기술 회사가 되는 것이 아니라 다음 폐쇄루프를 운영하는 수익 운영체계다.

```text
시장 데이터
→ 후보 SKU
→ 수익성·위험 검증
→ 대표 승인
→ 소량 테스트
→ 판매·재고·현금·고객 데이터 회수
→ 예측 vs 실제 비교
→ Agent 판단기준 수정
→ 다음 소싱 정확도 향상
```

## 2. 9-Agent 조직도

```text
대표
 ├─ Sourcing Pod
 │   ├─ Agent 1 Sourcing Lead
 │   ├─ Agent 2 Product Scout
 │   └─ Agent 3 Profit & Risk Reviewer
 │
 ├─ Sales/GTM Pod
 │   ├─ Agent 4 GTM Lead
 │   ├─ Agent 5 CRM/Outreach Agent
 │   └─ Agent 6 Conversion Reviewer
 │
 └─ Commerce Ops Pod
     ├─ Agent 7 Commerce Ops Lead
     ├─ Agent 8 Inventory & Pricing Agent
     └─ Agent 9 Order/Risk Auditor
```

## 3. 공통 Agent 계약

모든 Agent 출력에는 다음 필드를 포함한다.

- `run_id`
- `agent_id`
- `decision_id`
- `as_of_date`
- `data_freshness`
- `source_refs`
- `input_record_ids`
- `rule_version`
- `confidence_score`
- `recommendation`
- `hard_stop_flags`
- `human_approval_required`
- `expected_vs_actual_link`

AI는 다음을 직접 실행하지 않는다.

- 가격 변경
- 재고 조정
- 상품 공개
- 발주·결제
- 주문 취소·환불
- 대규모 CRM 발송
- 고객 병합
- 통관·정품·법적 판단

## 4. Agent별 역할과 산출물

### Agent 1 — Sourcing Lead

**목적:** 어디에서 어떤 시장기회를 찾을지 결정한다.

입력:

- 시장·검색·판매·고객·경쟁 데이터
- 기존 SKU별 기여이익·재고회전
- 공급처·카테고리별 과거 성과
- 대표의 현금·투자 제한

산출물:

- 조사 카테고리
- 고객 문제·수요 가설
- 후보 SKU 발굴 기준
- 가격대·브랜드·사이즈 범위
- 예상 테스트 수량
- Sourcing Brief

권한: 조사 범위 제안만. 공급처 연락·발주 불가.

### Agent 2 — Product Scout

**목적:** 후보 상품의 시장성·공급 가능성·가격 조건을 수집한다.

수집 필드:

- 브랜드·모델·스타일코드
- 색상·사이즈·시즌
- 국내·해외 판매가격
- 경쟁 SKU·가격·배송
- 검색·조회·장바구니·판매 신호
- 공급처 ID·재고·MOQ·리드타임
- 인보이스·정품·수입자료 유무
- 배송·통관·반품·A/S 조건
- 데이터 기준일·출처

산출물: `Product Candidate Card`

권한: 후보 등록. 가격·재고·상품 공개·발주 불가.

### Agent 3 — Profit & Risk Reviewer

**목적:** 후보 SKU를 수익·현금·법적·운영 위험으로 판정한다.

필수 계산:

```text
순매출
= 판매가 - 할인 - 고객환급·취소

주문당 기여이익
= 순매출
- 상품 매입원가
- 환율
- 국제운송·국내운송
- 관세·부가세·통관비
- 플랫폼·결제수수료
- 포장·검수·CS
- 반품·환불·정품분쟁 충당금
- 광고·콘텐츠·CRM 배부비

순마진율 = 주문당 기여이익 / 순매출

BEP 주문수
= 테스트 고정비 / 주문당 기여이익

회수기간
= 투입 현금 / 월 예상 회수현금
```

수치는 AI 암산 금지. `margin_check.py`, 워크북 또는 검증된 계산 원장을 사용한다.

위험 체크:

- 정품·상표
- 통관·수입자
- 공급처·재고
- 가격 급변·환율
- 배송·반품
- A/S
- 광고·플랫폼 정책
- 개인정보·CRM 동의

산출물:

- S/A/B/C/D 등급
- 예상 순마진·BEP·회수기간
- 최대손실
- 하드스톱
- 조건부 승인 조건
- 추가 증빙 목록

판정:

- S: 즉시 실행 후보
- A: 대표 승인 후 샘플 테스트
- B: 5 SKU 이하 소량 테스트
- C: 모니터링·추가 데이터 수집
- D: 진입 금지·보류

## 5. Sales/GTM Pod

### Agent 4 — GTM Lead

질문:

- 어떤 상품을
- 어떤 고객에게
- 어떤 채널에서
- 어떤 가치제안으로
- 어떤 가격·배송조건으로
- 어떤 신뢰증거와 함께 팔 것인가

산출물:

- GTM Brief
- 고객 세그먼트
- READY/RARE 상품 약속
- 채널별 가격·콘텐츠·상담 전략
- 테스트 예산·최대손실

상품 공개·가격변경은 대표 승인 필요.

### Agent 5 — CRM/Outreach Agent

입력:

- 고객 ID·동의 상태
- 구매·조회·상담·장바구니·휴면
- 브랜드·가격대·사이즈·지역
- 반품·클레임·정품분쟁 제외 상태

산출물:

- 세그먼트 후보
- CRM 대상 후보
- 메시지 초안
- 발송 빈도·제외 규칙
- 예상 기여이익

대규모 발송·개인정보 처리·동의 불명 고객은 자동 보류.

### Agent 6 — Conversion Reviewer

분석 단계:

```text
노출 → 클릭 → 상품조회 → 상담 → 장바구니 → 결제
→ 배송 → 반품 → 재구매
```

산출물:

- 퍼널 단계별 이탈
- 메시지·가격·배송·신뢰요소별 가설
- 캠페인별 기여이익
- 예측 vs 실제 차이
- 다음 테스트안

CTR·조회수만으로 성공 판정하지 않는다.

## 6. Commerce Ops Pod

### Agent 7 — Commerce Ops Lead

감독 범위:

- 주문·결제·출고
- 재고·공급처·가격
- 배송·반품·A/S
- 현금회수
- 예외 큐·HOLD

산출물:

- 일일 운영 요약
- 예외·중단 큐
- 현금·출고 위험
- 대표 승인 대기

### Agent 8 — Inventory & Pricing Agent

분석:

- 판매속도
- 재고일수
- 재고가치
- 경쟁가격
- 할인 후 마진
- 장기재고 위험
- 공급처 가격변동

산출물:

- 가격 조정 후보
- 재고 이동 후보
- VIP·묶음판매 후보
- 발주 보류 후보
- 최대 할인 한도

직접 가격 변경·재고 조정·발주 불가.

### Agent 9 — Order/Risk Auditor

탐지:

- 주문 오류
- 중복·오가격
- 공급처 오류
- 재고 stale
- 마진 훼손
- 장기재고
- 배송·반품 이상
- 정품·통관·A/S 증빙 공백
- 환불·CRM 동의 문제

산출물:

- 위험 이벤트
- 거래 HOLD
- 원인코드
- 담당자·기한
- 재개 조건

## 7. 승인 매트릭스

| 행위 | Agent | 사람 승인 |
|---|---|---|
| 시장·후보 조사 | 제안 | 불필요 |
| 공급처 후보 등록 | Scout | 소싱 담당 |
| 신규 상품 공개 | GTM | 대표 또는 지정 승인자 |
| 가격 변경 | Pricing | 대표 승인 |
| 발주·결제 | Sourcing/Finance | 대표 승인 |
| CRM 소규모 테스트 | CRM | 동의·Rule 통과 후 담당 승인 |
| 대규모 CRM | CRM | 대표 승인 |
| 환불·고액 보상 | Ops/Auditor | 승인권자 |
| 주문·재고 상태 동기화 | Ops | 예외 시 사람 검토 |
| 통관·정품·법률 판단 | Reviewer | 관세사·전문가·대표 |

## 8. 학습 루프

각 후보와 테스트에 다음을 저장한다.

- 예측 판매량
- 예측 순매출·기여이익
- 예측 배송·반품·재구매
- 실제 주문·순매출·기여이익
- 실제 배송·반품·보상
- 차이 원인
- 다음 Agent 규칙 변경안

같은 오류가 2회 반복되면 Agent 프롬프트가 아니라 평가기준·데이터 필드·하드스톱을 재검토한다.

## 9. 구축 순서

1. 데이터 사전·내부 ID·승인 상태
2. Sourcing 3-Agent와 수동 원장
3. 5 SKU 소량 테스트
4. 주문·재고·반품·현금 원장
5. GTM·CRM·퍼널 분석
6. Commerce Ops 이상탐지
7. 검증된 API·읽기 전용 연동
8. 제한적 쓰기 자동화

## 최종 운영 원칙

PMS의 Agent는 사람을 대체하는 조직이 아니라, 대표가 더 빠르고 정확하게 승인할 수 있도록 **후보·증거·수익·위험·예외를 정리하는 운영체계**다.
