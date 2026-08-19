---
source_path: ".pi/BusinessVault/plans/pms-queryable-data-map-v1-2026-08-15.md"
source_filename: "pms-queryable-data-map-v1-2026-08-15.md"
source_type: "text"
source_size_bytes: 9825
source_modified_at: "2026-08-15T21:41:28+09:00"
source_sha256: "3429e1e8be7f745ed60cfa7566d0ce1e6fef0ce5134da8d3698b53c7cbee4f97"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Queryable Data Map v1.0

- 기준일: 2026-08-15
- 사업: Premium MultiShop Revenue Commerce OS
- 상태: 논리 데이터맵 확정 / 실제 API 권한·필드·동기화는 미확인

## 1. 설계 원칙

- Master는 현재 승인된 상태, Event·Ledger는 변경·거래 사실을 보존한다.
- 내부 ID와 외부 시스템 ID를 분리한다.
- API가 불확실하면 CSV·수동 수집을 먼저 사용한다.
- 모든 수치와 Agent 판단에 기준일·출처·신뢰도·규칙버전을 붙인다.
- 쓰기 작업은 `pull/import → normalize → validate → quarantine → approve → publish` 순서다.
- 예외·불일치·stale 데이터는 숨기지 않고 Exception Queue로 보낸다.

## 2. 시스템 범위

```text
Cafe24 / 네이버 / 스마트스토어 / 카카오 / POS / ERP
공급처 / 홍콩창고 / 3PL / 택배 / 결제 / 광고 / Analytics
                         ↓
              Source & Consent Layer
                         ↓
             Master + Event + Ledger Layer
                         ↓
       Decision Engine + 9-Agent Recommendation Layer
                         ↓
        Approval / HOLD / Exception / Audit Layer
                         ↓
      사람 승인 후 채널·주문·재고·CRM 시스템 실행
                         ↓
             예측 vs 실제 학습 데이터
```

## 3. 내부 ID

| 내부 ID | 정의 | 외부 매핑 |
|---|---|---|
| `customer_id` | 고객 마스터 고정 ID | Cafe24·카카오·네이버·POS 고객키 |
| `sku_id` | 상품·옵션 고정 ID | Cafe24 product/option, 공급처 SKU |
| `supplier_id` | 공급처 법인·계약 단위 | 공급처 계정·법인번호 |
| `inventory_lot_id` | 실제 재고 로트 | 국내 창고·홍콩 창고·3PL 로트 |
| `order_id` | 내부 주문 고정 ID | Cafe24·네이버·결제 주문번호 |
| `order_line_id` | 주문상품 단위 | 외부 주문 라인 |
| `shipment_id` | 출고·운송 단위 | 택배·통관·운송장 |
| `rma_id` | 반품·환불·A/S 케이스 | 플랫폼 RMA·CS 번호 |
| `campaign_id` | 캠페인·발송 단위 | 카카오·광고·콘텐츠 캠페인 |
| `content_id` | 콘텐츠·상품페이지 단위 | Cafe24·블로그·광고 소재 |
| `approval_id` | 사람 승인 단위 | 승인자·정책·시각 |
| `decision_id` | Agent 판단 단위 | run·rule·버전 |
| `exception_id` | 오류·위험 단위 | 재처리·HOLD 상태 |

## 4. Master Data

### Product/SKU Master

- `sku_id`
- 브랜드·모델·스타일코드·옵션
- 상품군: 의류·신발·잡화
- 재고유형: READY·RARE
- 신품·전시·리퍼브 상태
- 원산지·조달국·수입유형
- 정품·상표·A/S 증빙상태
- 상품여권 상태
- owner·source_of_truth·valid_from·valid_to

### Supplier Master

- `supplier_id`
- 법인명·국가·연락처
- 계약상태·판매권
- 정품증빙 상태
- 인보이스·수출·통관자료
- MOQ·리드타임
- 반품·클레임 조건
- API/CSV/feed 상태
- 공급처 신뢰도·클레임률

### Customer/Consent Master

- `customer_id`
- 채널별 외부 ID 매핑
- 지역·선호 브랜드·사이즈·가격대
- 구매·조회·상담·장바구니 상태
- VIP·휴면·재구매 후보
- 수신동의·동의일·철회일·채널별 수신가능
- 클레임·환불·마케팅 보류 상태
- 데이터 신뢰도·매칭 근거

### Inventory Master

- `inventory_lot_id`
- `sku_id`
- 국내 창고·매장·홍콩·3PL 위치
- 소유권 유형
- 수량: available·reserved·inbound·hold·damaged
- 재고 확인시각
- 재고 원가·로트
- Lock 상태
- 장기재고일수
- 실사·조정 기록

### Offer/Pricing Master

- `offer_id`
- `sku_id`
- 채널
- 정상가·판매가·할인가
- 가격 유효기간
- 환율·세금·배송 포함 여부
- 플랫폼·결제수수료
- 최소 마진·최대 할인
- 가격 승인상태
- 경쟁가격 기준일

## 5. Event Envelope

모든 이벤트 공통 필드:

- `event_id`
- `event_type`
- `occurred_at`
- `source_system`
- `source_event_id`
- `entity_type`
- `entity_id`
- `schema_version`
- `payload_ref`
- `ingested_at`
- `data_freshness`
- `idempotency_key`
- `validation_status`

핵심 이벤트:

- `product_candidate_created`
- `supplier_evidence_verified`
- `inventory_snapshot_received`
- `price_snapshot_received`
- `sku_approved`
- `offer_published`
- `customer_viewed`
- `consultation_started`
- `cart_created`
- `order_paid`
- `order_cancelled`
- `shipment_created`
- `customs_status_changed`
- `order_delivered`
- `return_requested`
- `refund_completed`
- `as_started`
- `compensation_approved`
- `agent_run_completed`
- `human_approval_granted`
- `exception_opened`
- `hold_applied`
- `hold_released`

## 6. Ledger

### Order/Revenue Ledger

- 주문·주문라인
- 결제·취소·환불
- 순매출
- 채널·캠페인·콘텐츠
- 주문상태·배송상태

### Cost Ledger

- 매입원가
- 환율
- 관세·부가세·통관
- 국제·국내배송
- 플랫폼·결제수수료
- 검수·포장·CS
- 광고·콘텐츠·CRM 배부비
- 반품·분쟁·A/S·보상

### Inventory Ledger

- 입고
- 이동
- 예약
- 판매
- 반품
- 폐기·손상
- 조정
- 재고 Lock·해제

### Approval/Audit Ledger

- 요청자
- 승인자
- 요청시각·승인시각
- 대상 ID
- 변경 전·후 값
- 근거·규칙버전
- 예상 최대손실
- 원복 방법
- 실제 결과

## 7. Query View

Agent가 직접 읽는 뷰는 원장을 직접 계산하지 않고 승인된 Query View를 사용한다.

### `vw_sourcing_candidate_profit_risk`

- candidate·SKU·supplier
- market signals
- landed cost
- unit contribution profit
- margin
- BEP
- payback
- evidence completeness
- risk flags
- S/A/B/C/D
- data freshness

### `vw_ready_rare_inventory`

- SKU
- READY/RARE
- available·reserved·hold
- location
- stock checked at
- promised ship date
- actual ship rate
- age days
- return rate

### `vw_customer_crm_eligibility`

- customer
- consent
- segment
- last purchase
- preferred brand/size
- claim/refund suppression
- expected contribution profit
- contact frequency

### `vw_order_risk_queue`

- order
- payment
- inventory mismatch
- price anomaly
- supplier error
- stale stock
- shipping delay
- return/refund issue
- hold status
- owner·due date

### `vw_forecast_vs_actual`

- decision/test/order
- predicted units/revenue/margin/delivery/returns/repeat
- actual units/revenue/margin/delivery/returns/repeat
- variance
- root cause
- next rule change

## 8. Cafe24·ERP·고객·재고·가격·공급처 매핑

| 원천 | 우선 수집 | 1차 방식 | 쓰기 권한 |
|---|---|---|---|
| Cafe24 | 상품·옵션·주문·결제·배송·환불 | API 스펙 확인 후 CSV/API | 미확인·승인 전 없음 |
| ERP | 매입·원가·입고·회계 | CSV/DB export 우선 | 미확인 |
| POS/매장 | 판매·고객·재고·예약 | CSV export 우선 | 미확인 |
| 네이버/스마트스토어 | 상품·주문·배송·정산 | 공식 API/CSV 확인 | 미확인 |
| 카카오 | 상담·동의·발송·클릭 | 동의·권한 확인 후 export/API | 대량 발송 금지 |
| 공급처 | 가격·재고·MOQ·리드타임 | 1곳 읽기 전용 feed/CSV | 쓰기 금지 |
| 홍콩창고/3PL | 입고·보관·출고·실사 | CSV/운영 리포트 | 쓰기 미확인 |
| 택배·통관 | 운송장·상태·통관 | 이벤트/CSV | 쓰기 금지 |
| 광고/Analytics | 비용·클릭·전환 | export/API | 예산 변경 금지 |

현재 API 권한·필드·계정 소유권은 확인되지 않았다. 따라서 실제 연결 완료로 보고하지 않는다.

## 9. 데이터 신뢰·예외 상태

- `VERIFIED`
- `PROVISIONAL`
- `STALE`
- `MISSING`
- `UNMATCHED_ID`
- `AMBIGUOUS_ID`
- `QUARANTINED`
- `HOLD`
- `APPROVED`

`STALE`, `MISSING`, `UNMATCHED_ID`, 정품·통관 증빙 불가, 동의 불명, 순마진 하드스톱 위반은 실행을 차단한다.

## 10. Agent Query 예시

```sql
-- Sourcing: 공급·수익·증빙 통과 후보
SELECT *
FROM vw_sourcing_candidate_profit_risk
WHERE data_freshness <= 24
  AND evidence_completeness >= 0.90
  AND contribution_margin >= 0.12
  AND hard_stop_flag = FALSE
  AND approval_status = 'PENDING_REVIEW';
```

```sql
-- Pricing: 가격 변경 후보만 조회, 실제 변경은 금지
SELECT *
FROM vw_ready_rare_inventory
WHERE age_days > 60
  AND contribution_margin_after_discount >= 0.12
  AND pricing_approval_status = 'PENDING';
```

```sql
-- CRM: 동의·클레임 보류·기여이익 조건을 통과한 후보
SELECT *
FROM vw_customer_crm_eligibility
WHERE consent_status = 'ACTIVE'
  AND claim_suppression = FALSE
  AND expected_contribution_profit > 0
  AND frequency_guard = TRUE;
```

## 11. MVP-0~MVP-4

### MVP-0: 수동 Queryable Data Map

- 데이터 사전
- 내부 ID
- 원본 파일 등록
- 기준일·담당자·출처
- 예외·quarantine

### MVP-1: 상위 SKU 마스터

- Product·Offer·Inventory·Supplier·Evidence
- READY·RARE 구분
- 5 SKU 테스트

### MVP-2: 주문·원가·재고 원장

- 주문·환불·배송
- 완전원가
- 재고 Lock
- 기여이익 재계산

### MVP-3: Sourcing 3-Agent

- 후보 카드
- 수익·위험 판정
- 대표 승인
- 예측 vs 실제

### MVP-4: GTM·CRM·Ops

- 상담·퍼널·CRM 동의
- 재고·가격 후보
- 주문·위험 예외 큐

## 12. 검증 조건

- 원본·내부 ID 매핑 중복 없음
- 주문 합계 = 결제 - 취소 - 환불 정합성
- 재고: 기초 + 입고 - 판매 + 반품 ± 조정 = 현재고
- 가격·원가·수수료 기준일 존재
- 모든 Agent 산출물에 source·freshness·confidence 존재
- 승인 없는 쓰기 작업 없음
- stale·불일치·동의 불명 데이터가 발송·공개·가격변경으로 넘어가지 않음
- API 미확인 시스템은 CSV/manual fallback으로 작동
