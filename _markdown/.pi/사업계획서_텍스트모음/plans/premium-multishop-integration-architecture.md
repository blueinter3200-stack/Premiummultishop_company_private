---
source_path: ".pi/사업계획서_텍스트모음/plans/premium-multishop-integration-architecture.md"
source_filename: "premium-multishop-integration-architecture.md"
source_type: "text"
source_size_bytes: 17562
source_modified_at: "2026-08-13T15:47:45+09:00"
source_sha256: "8aebd061f041a6cde4d450d48b6d09220463d81dfa172b5e770164876966c673"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# Premium MultiShop: Cafe24–해외 공급처 통합 아키텍처

> 범위: Premium MultiShop 병행수입/직수입 사업의 Cafe24 자사몰과 다수 해외 공급처 연동. BELLOON 화장품 사업은 범위에서 제외한다. 외부 시스템에 실제 연결하거나 인증키를 수집하지 않는 논리 설계 문서다.

## 1. 한 줄 결론

**Cafe24를 판매 채널, 내부 Integration Hub를 단일 정합성 원장, 공급처별 Adapter를 변환 경계로 둔다.** 재고·가격은 공급처 능력에 따라 웹훅+폴링 또는 API 폴링으로 갱신하되, 주문 전에는 반드시 재확인/예약하고, 모든 외부 입력과 상태 변경은 idempotency key·outbox/inbox·감사로그로 추적한다.

## 2. 목표와 비목표

### 목표
- 상품/옵션/SKU, 원가·환율·판매가, 재고, 주문, 배송상태를 내부 표준 모델로 통합
- 여러 공급처의 API/CSV/XML/EDI를 같은 업무 흐름으로 처리
- Cafe24 품절·가격·주문·송장 상태를 안전하게 동기화
- 가격 급변, 품절, 중복 주문, 부분 실패, 재처리 이력을 보존
- 공급처별 SLA·데이터 신뢰도를 수치화해 발주/판매 중단 판단 지원

### 비목표
- 실제 Cafe24/공급처 API 호출, 계약, 인증키 수집
- 관세·부가세·통관 법률의 확정 판정
- 자동 대량 발주 승인(초기에는 사람 승인)

## 3. 논리 구성

```text
Cafe24 Web/Orders ──┐
Cafe24 Webhook/Poll ─┤
                    ▼
             [Ingress API]
                    │ raw payload + Inbox(idempotency)
                    ▼
        [Queue/Event Bus + Retry/DLQ]
                    ▼
 [Supplier Adapter Layer]
   API | CSV/SFTP | XML | EDI | Webhook receiver
                    │ canonical events
                    ▼
 [Integration Hub / Workflow Orchestrator]
   Catalog · Pricing · Inventory · Order · Fulfillment
       │                 │                 │
       ▼                 ▼                 ▼
 [Canonical DB]    [Outbox]          [Audit/Observability]
       │                 │
       └──────► Cafe24 Adapter / Supplier Adapters
```

- **Canonical DB**: 상품·SKU·가격·재고·주문·배송의 현재 상태와 이력.
- **Raw store**: 원문 CSV/XML/JSON/EDI, 파일 checksum, 수신시각, 공급처·배치 ID를 보존. 원문은 재처리 가능해야 한다.
- **Inbox**: 외부 이벤트/파일의 중복 수신 방지(`source + external_event_id` 또는 payload hash).
- **Outbox**: DB 커밋과 발행 이벤트를 원자적으로 묶어, DB에는 반영됐지만 메시지가 유실되는 문제 방지.
- **DLQ**: 재시도 한도를 넘은 건을 보관하고 운영자 승인 후 재처리.

## 4. 연동 방식 선택 기준

| 방식 | 우선 사용 조건 | 장점 | 주의점/확인 필요 |
|---|---|---|---|
| REST/GraphQL API | 인증·rate limit·페이지네이션·변경분 조회·주문 생성/취소가 제공될 때 | 양방향, 구조화, 자동화 적합 | 실제 엔드포인트, scope, rate limit, 주문 중복키, 취소/반품 API는 공급처·Cafe24 확인 필요 |
| CSV | API가 없고 정기 파일 export/import 가능할 때 | 구현·검수 쉬움, 대량 상품에 유리 | 인코딩, 구분자, 헤더, 증분/전체 여부, 파일 전달(SFTP/S3/email), 삭제 의미, 수신 SLA 확인 필요 |
| XML | 공급처가 카탈로그/재고 XML feed를 제공할 때 | 계층형 상품·옵션 표현 | XSD, namespace, decimal/통화, 전체 스냅샷인지 증분인지 확인 필요 |
| EDI | 대형 공급처가 표준 거래문서(주문/확인/ASN/송장)를 요구할 때 | 업무 문서·추적성·확정 상태 강함 | 사용하는 표준(EDIFACT/X12), VAN/AS2/SFTP, 파트너 ID, ACK/재전송 규칙 확인 필요 |
| Webhook | 공급처/Cafe24가 재고·주문·배송 이벤트 push를 제공할 때 | 낮은 지연, 폴링 부하 감소 | 서명검증, 재전송, 순서 뒤바뀜, 누락 탐지, 이벤트 보존기간 확인 필요 |
| Polling | webhook이 없거나 신뢰성 보완이 필요할 때 | 보편적, 누락 보완 가능 | 호출량·지연·rate limit·시계 skew. `updated_since` 증분 우선, 주기적 전체 대조 필요 |

**권장 원칙:** Webhook은 빠른 알림, API 조회는 최종 사실 확인, 폴링은 누락 보완으로 조합한다. 웹훅만 신뢰하지 않는다. API가 없으면 SFTP CSV/XML을 원문 보존 후 배치 반영하고, EDI는 주문/ASN/송장 업무에만 별도 adapter를 둔다.

## 5. 공급처별 Adapter 계약

모든 Adapter가 내부적으로 다음 인터페이스를 제공하도록 한다.

- `pull_catalog(cursor|updated_since)`
- `pull_inventory(cursor|updated_since)`
- `pull_price(cursor|updated_since)`
- `receive_event(raw_request)`
- `create_order(canonical_order)`
- `cancel_order(external_order_id, reason)`
- `pull_order_status(cursor|updated_since)`
- `pull_shipment(cursor|updated_since)`
- `health_check()`

Adapter는 인증, pagination, rate limit, 서명, 포맷 파싱, 외부 상태→내부 상태 매핑만 담당한다. 가격 정책·재고 예약·주문 승인 규칙은 Hub에 둔다.

## 6. 기준 데이터 모델

관계형 DB(PostgreSQL 권장)와 JSON 원문 저장을 병행한다. 모든 테이블에 `created_at`, `updated_at`, `source_system`, `source_updated_at`, `version`을 둔다.

### 6.1 공급처/매핑

- `supplier`: `supplier_id`, 법인/국가/통화/타임존, integration_type, SLA, active, data_quality_score
- `external_mapping`: `supplier_id`, `object_type`, `external_id`, `internal_id`, `mapping_status`, `last_seen_at`
- `sync_cursor`: source/object, cursor 또는 last-success timestamp, watermark, run_id
- `raw_ingest`: raw_id, source, object_type, file/event ID, checksum, payload URI, received_at, parser_version

상품 식별은 `brand + model_code/style_code + color_code + size_code + season`를 보조키로 사용하되, 공급처 SKU와 바코드/GTIN이 우선이다. 자동 매칭 실패는 수동 매핑 큐로 보낸다.

### 6.2 상품·SKU

- `product`: 내부 `product_id`, brand, model/style, season, category, title/description, origin, authenticity_evidence_ref, status
- `sku`: `sku_id`, product_id, canonical_sku, barcode, size, color, condition, package/accessory spec, hazardous/restriction flags
- `supplier_sku`: supplier_id, sku_id, external_sku, external_product_id, supplier_title, supplier_cost, currency, MOQ, lead_time_days, availability_status
- `media_asset`: URL/hash, role, license/source, checksum, moderation/status

판매 단위는 `sku_id`로 고정하고, 공급처별 SKU·포장 단위·묶음 단위는 변환 규칙으로 저장한다. 사이즈/색상 표준화표와 매핑 버전을 반드시 보존한다.

### 6.3 가격·환율·원가

- `fx_rate`: base_currency, quote_currency, rate, provider, observed_at, valid_from/to, rate_type
- `cost_snapshot`: sku/supplier, purchase_cost, shipping_in, insurance, duty, import_vat, brokerage, DDP_fee, payment_fee, FX_rate_id, effective_cost, captured_at
- `price_rule`: channel, min_margin, fee assumptions, rounding, markdown, effective dates
- `price_snapshot`: sku, channel, list_price, sale_price, currency, rule_version, cost_snapshot_id, approved_by, valid_from/to

표시 가격은 내부 정책으로 계산한다.

```text
landed_cost = 매입가×적용환율 + 해외배송 + 보험 + 관세/통관 + DDP/대행료 + 국내입고 + 결제수수료
minimum_price = (landed_cost + expected_return_allowance + fixed_cost_alloc)
                 / (1 - channel_fee_rate - target_margin_rate)
```

- 환율은 `실시간` 하나를 쓰지 말고 공급처 결제용/회계용/판매가 산정용을 구분한다.
- 환율·원가·수수료가 없으면 마진 계산은 **검증 불가/판매가 승인 보류**.
- 가격 급변 guard: 마지막 승인 가격 대비 절대액·백분율 임계치, 원가 미수신, 통화 불일치, 음수/비정상 가격이면 자동 게시 금지→운영자 승인.
- 경쟁가 자동 추종은 금지하고 최소마진·최대할인·브랜드 정책을 우선한다.

### 6.4 재고·예약

- `inventory_balance`: sku, supplier/location, on_hand, available, reserved, inbound, damaged, last_confirmed_at, confidence, source_version
- `inventory_reservation`: reservation_id, sku, order_id, qty, state(held/confirmed/released/expired), expires_at
- `inventory_ledger`: immutable delta, reason, reference_type/id, before/after, actor

채널 게시 가능 수량:

```text
publishable = max(0, confirmed_available - safety_stock - pending_risk_buffer)
```

공급처가 예약 API를 지원하지 않으면 Cafe24 주문 접수 후 **재고 재확인→공급처 발주**를 순서대로 수행하며, 경합 위험을 고객에게 숨기지 않는다. 다수 채널이 있으면 Hub에서 안전재고를 먼저 차감하고 Cafe24에는 보수적으로 게시한다.

### 6.5 주문·배송

- `sales_order`: internal_order_id, cafe24_order_id, customer/redacted info, currency, totals, payment_state, fulfillment_state, idempotency_key
- `sales_order_line`: order_id, sku, qty, sold_price, allocated_supplier, cost_snapshot_id, tax/shipping allocation, line_state
- `supplier_order`: supplier_order_id, supplier, internal_order_id, external_order_id, submit_payload_hash, state, ack_at, cancel_deadline
- `shipment`: order/line, carrier, tracking_no, origin/destination, incoterm(DDP/DAP/etc.), shipped_at, delivered_at, tracking_state
- `order_status_history`: state transitions, source event, actor, reason, correlation_id

주문 상태는 `NEW → PAYMENT_CONFIRMED → INVENTORY_CHECKED → SUPPLIER_ORDERED → SUPPLIER_CONFIRMED → SHIPPED → DELIVERED`와 `CANCEL_REQUESTED/CANCELLED/FAILED/RETURNED`를 분리한다. 공급처 주문 성공 응답이 timeout이면 재전송 전 조회로 존재 여부를 확인한다.

## 7. 핵심 흐름

### 상품/재고/가격
1. 원문 수신 → checksum/Inbox 중복 검사 → parser validation.
2. 외부 ID 매핑 → canonical upsert(낮은 `source_updated_at`은 무시).
3. 재고/가격 검증 → policy engine → 승인 또는 quarantine.
4. Canonical DB 커밋과 outbox 발행 → Cafe24 update queue.
5. Cafe24 반영 결과 저장; 실패는 지수 백오프 재시도, DLQ, 현재 게시값 유지.
6. 매일/주기적으로 공급처·Hub·Cafe24 전체 대조 및 차이 리포트.

### 주문
1. Cafe24 webhook 수신 즉시 raw 저장; webhook 누락 대비 주문 API polling.
2. 결제 완료·배송지·재고·금지상품 검증.
3. SKU별 공급처 라우팅(가격, 가용재고, 리드타임, 정품증빙, DDP 가능 여부).
4. 공급처 예약/주문 생성. 멱등키 `PM-{cafe24_order_id}-{line_id}-{attempt_group}`.
5. ACK/주문번호 저장 후 고객에게 처리상태 반영. 실패 시 자동 재고 확정 금지, 운영자 큐.
6. ASN/배송 이벤트 또는 polling으로 송장·상태 수집→Cafe24 fulfillment update.

## 8. 예외·정합성·롤백

- **중복:** 외부 이벤트 ID, 파일 checksum, 주문 멱등키, DB unique constraint. 같은 이벤트 재수신은 no-op.
- **순서 역전:** `source_updated_at`/sequence를 비교하고 오래된 이벤트는 상태를 덮어쓰지 않되 감사로그에는 기록.
- **품절:** 신규 판매 즉시 `OUT_OF_STOCK` 또는 보수적 0 게시. 이미 결제된 주문은 대체 SKU 제안/취소/환불 정책을 운영자 승인으로 처리.
- **가격 급변:** 임계치 초과 가격은 quarantine; 기존 판매가 유지 또는 판매중지 정책을 사전 결정. 잘못 게시된 가격은 주문 자동취소가 아니라 법무/CS 정책 확인 후 처리.
- **부분 성공:** 한 주문의 여러 line을 독립 상태로 관리. 공급처 A 성공/B 실패를 전체 성공으로 기록하지 않는다.
- **롤백:** 외부 시스템은 트랜잭션 롤백이 불가하므로 보상 작업(가격 원복, 재고 재게시, 공급처 취소)을 사용한다. 모든 workflow에 `compensation_action`을 정의.
- **장애:** retryable(429/5xx/network)과 non-retryable(인증/스키마/상품매핑)을 분리. circuit breaker로 장애 공급처를 격리하고 마지막 확정 재고의 유효시간 만료 시 판매 중지.
- **감사:** append-only `audit_log`에 actor, action, before/after hash 또는 diff, reason, correlation_id, source raw_id, approval_id 저장. 개인정보는 최소화/마스킹.

## 9. DDP·통관·반품 비용

- 주문/배송에 `incoterm`을 필수화하고 DDP와 DAP를 혼용하지 않는다.
- DDP는 공급처가 부담한다고 가정하지 말고 `DDP_fee`, 관세, VAT, 통관수수료, 반품 재수출비를 각각 필드로 분해한다.
- 공급처가 비용을 단일 합계로만 제공하면 구성요소 불명으로 표시하고, 원가·마진에 보수적 allowance를 적용하거나 판매 승인 보류.
- 배송비·관세가 주문 후 확정되는 경우 `estimated_cost`와 `actual_cost`를 분리하고 차이를 원가/공급처별로 분석한다.
- 한국 소비자 고지, 병행수입 통관, 반품·환불, 상표/정품 증빙 책임은 계약·관세사·법률 전문가 확인 필요.

## 10. 운영·보안·관측성

- 공급처별 secret은 Secret Manager/환경변수로만 보관; 문서·로그에 키/개인정보 금지.
- 지표: sync latency, 성공률, stale inventory age, mapping failure, price quarantine, oversell, order ACK latency, shipment delay, DLQ count, supplier data quality.
- 알림: 재고 stale 임계치, 급격한 가격변화, oversell 위험, 주문 ACK timeout, 반복 인증 실패, DLQ 증가.
- 모든 job은 `run_id`, correlation ID, adapter version, input checksum, output count, error count를 기록한다.
- 운영 화면에는 공급처별 마지막 성공시각·현재 cursor·실패 건·재처리 버튼·수동 승인 이력을 제공한다.

## 11. 단계별 MVP

### Phase 0 — 사전 검증(연결 전)
- Cafe24와 공급처별 실제 문서 수집: 인증/endpoint, rate limit, webhook, CSV/XML schema, EDI 표준, 주문·취소·예약·배송 API, SLA.
- 대표 공급처 1곳과 SKU 20개 이하로 샘플 파일/샌드박스 확보.
- SKU 매칭키, 최소마진, 안전재고, 가격 급변 임계치, 취소/품절 CS 정책을 대표 승인.
- **완료 기준:** 샘플 원문으로 매핑·원가·재고·주문 상태 전환을 재현.

### Phase 1 — 읽기 전용 Catalog/Inventory
- 단일 공급처 API 또는 CSV 하나 선택. raw store, Inbox, parser, canonical SKU, 재고 ledger, stale guard 구축.
- Cafe24에는 수동 승인 후 상품/재고 일부 반영. 가격은 계산·리포트만.
- **게이트:** 7일 연속 중복 0, 매핑 실패율 기준 설정, stale 재고 자동 판매중지 검증.

### Phase 2 — 가격·다수 공급처
- 2~3개 Adapter, FX/cost snapshot, pricing rules, quarantine, Cafe24 가격 반영.
- 가격 이력과 승인 workflow를 운영.
- **게이트:** 모든 게시 가격이 원가 snapshot과 rule version으로 역추적 가능.

### Phase 3 — 주문·공급처 발주(사람 승인)
- Cafe24 주문 수집, 재고 재확인, 공급처 주문 생성/ACK, 부분주문, 취소 보상, idempotency.
- 자동 발주가 아니라 운영자 승인 큐로 시작.
- **게이트:** 테스트 주문/취소/timeout 재조회/중복 webhook/품절 케이스 통과.

### Phase 4 — 배송·대조·제한적 자동화
- ASN/송장/배송상태, Cafe24 고객 상태 반영, 일일 전체 대조, DLQ 재처리, 공급처 scorecard.
- SLA가 입증된 공급처·SKU만 자동 주문/가격 반영; 나머지는 승인 유지.

### Phase 5 — 확장
- EDI, 예약재고, 다중 창고/채널, 반품·환불, 실제원가 정산, 자동 라우팅을 추가. 자동화 권한은 공급처별 데이터 품질·oversell·ACK 성과에 따라 단계적으로 부여.

## 12. 실제 확인이 필요한 항목

### Cafe24 확인 필요
- 상품/옵션/재고/가격/주문/송장 API의 현재 버전·scope·rate limit·페이지네이션
- 주문 webhook 이벤트 목록, 서명·재전송·순서·누락 보완 방법
- 재고 차감 시점(결제/주문/배송), 옵션 SKU 식별자, 부분취소/부분배송 모델
- 대량 업데이트 한도, 실패 응답, sandbox와 production 차이

### 공급처별 확인 필요
- 제공 채널(API/CSV/XML/EDI/SFTP), 인증과 IP allowlist, rate limit, SLA
- 재고의 의미(on-hand/available/예약 포함), 업데이트 주기, oversell 보상
- 가격의 통화·세금 포함 여부·유효기간·할인/MOQ
- 상품 이미지/상세 콘텐츠 사용권, 정품 증빙, 바코드·사이즈 체계
- 주문 예약/취소/수정/부분출고/반품/환불 및 멱등성
- 배송사·송장 발급 시점·DDP/DAP·관세/VAT/반품비 부담
- API 장애 시 CSV 대체, 전체 스냅샷/증분 기준, 삭제·품절 표현

## 13. 권장 의사결정 원칙

- 초기에는 **단순하고 되돌릴 수 있는 읽기 전용 동기화**부터 시작한다.
- 자동 발주는 공급처별 실제 ACK·취소·배송 성과가 검증된 뒤 제한적으로 허용한다.
- 데이터가 없거나 오래됐으면 재고를 0 또는 판매중지로 보수 처리한다.
- 공급처가 제공하지 않는 필드는 임의로 채우지 않고 `검증 불가/공급처 확인 필요`로 표시한다.
- 가격·재고 자동화의 성공 기준은 매출이 아니라 oversell 0에 가까운 운영, 실제 마진 추적, 현금회수기간 단축이다.
