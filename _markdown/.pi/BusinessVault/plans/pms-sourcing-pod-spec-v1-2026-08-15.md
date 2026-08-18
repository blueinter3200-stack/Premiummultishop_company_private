---
source_path: ".pi/BusinessVault/plans/pms-sourcing-pod-spec-v1-2026-08-15.md"
source_filename: "pms-sourcing-pod-spec-v1-2026-08-15.md"
source_type: "text"
source_size_bytes: 6974
source_modified_at: "2026-08-15T21:40:30+09:00"
source_sha256: "ba5c09c4e9c38c6fcf831c7e9f40556b9cdc99bc327210216e96b431e9cd3a09"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Sourcing Pod — 데이터 필드·판단식·프롬프트 v1.0

- 기준일: 2026-08-15
- 대상: Agent 1 Sourcing Lead, Agent 2 Product Scout, Agent 3 Profit & Risk Reviewer
- 상태: 설계 완료 / 실제 계산·연동은 데이터 확보 후 테스트

## 1. 공통 Candidate ID

모든 후보는 `candidate_id`를 발급한다.

필수 연결:

- `candidate_id`
- `sku_id` 또는 `PENDING_SKU_ID`
- `supplier_id`
- `source_ref`
- `research_run_id`
- `decision_id`
- `approval_id`
- `test_id`

## 2. Product Scout 필드

### 상품 식별

- brand
- model_name
- style_code
- category
- season
- color
- size
- material
- condition
- country_of_origin
- official_or_parallel_import

### 시장 신호

- domestic_price
- overseas_price
- competitor_price
- price_as_of
- search_signal
- product_view_signal
- cart_signal
- order_signal
- review_signal
- trend_source
- demand_confidence
- demand_window

조회수·검색량만으로 수요 확정 금지. 구매·상담·재구매 신호를 우선한다.

### 공급·물류

- supplier_id
- supplier_legal_name
- supplier_country
- inventory_location
- stock_qty
- stock_checked_at
- stock_confidence
- moq
- lead_time_days
- inbound_cost
- hong_kong_storage_cost
- international_shipping_cost
- customs_cost_estimate
- ddp_status
- importer_of_record
- return_route
- return_cost
- supplier_api_or_feed_status

### 증빙·책임

- invoice_available
- authenticity_evidence
- import_evidence
- trademark_risk
- customs_risk
- aftercare_status
- evidence_completeness
- legal_review_status

### 데이터 품질

- source_type
- source_url_or_file
- source_collected_at
- data_freshness_hours
- duplicate_check
- missing_fields
- confidence_score
- quarantine_reason

## 3. Profit & Risk Reviewer 계산 필드

```text
gross_sales = selling_price × expected_units
net_sales = gross_sales - discount - expected_refund

unit_contribution_profit =
  net_unit_revenue
  - product_cost
  - fx_cost
  - inbound_shipping
  - storage_and_inspection
  - customs_and_tax
  - outbound_shipping
  - payment_and_platform_fee
  - expected_return_cost
  - expected_claim_cost
  - allocated_content_crm_cost

contribution_margin = unit_contribution_profit / net_unit_revenue

bep_units = test_fixed_cost / unit_contribution_profit

payback_months = invested_cash / expected_monthly_cash_recovery
```

수익 계산은 반드시 `/opt/data/skills/business/belloon-global-beauty/scripts/margin_check.py` 또는 검증된 워크북 결과로 수행한다. 입력값이 없으면 `검증 불가`로 종료한다.

## 4. 하드스톱

다음 중 하나라도 해당하면 발주·공개 금지 또는 보류다.

- 순마진율 < 12%
- 예상 월 순이익 < 500,000원
- 회수기간 > 6개월
- 데이터 신뢰도 < 0.70
- 법적 안전도 < 4/5
- 리드타임 > 45일
- 재고회전일 > 90일
- 투자금 > 가용현금 30%
- 정품·통관·A/S 증빙 불가
- 재고 stale·가격 급변·공급처 오류

## 5. 판정 카드

### S — 즉시 실행 후보

모든 핵심 증빙·수익·공급·현금 조건 통과. 대표 승인 후 실행.

### A — 샘플 테스트

경제성은 유효하나 수요·공급·배송 중 하나가 제한적. 3~5 SKU·SKU당 1~2개.

### B — 소량 테스트

후보 가치는 있으나 추가 데이터 필요. 테스트 상한 5 SKU 또는 내부 승인 투자 한도.

### C — 모니터링

발주·공개 없이 데이터 수집. 수요·가격·공급 변화 관찰.

### D — 진입 금지

하드스톱 위반·증빙 불가·손실 상한 불명.

## 6. Agent Prompt — Sourcing Lead

```text
역할: Premium MultiShop Sourcing Lead
목표: 매출이 아니라 실제 기여이익과 현금회수 가능성이 있는 조사 범위를 결정한다.

입력:
- 시장·검색·상담·주문·재고·경쟁 데이터
- 과거 SKU별 예측 vs 실제
- 공급처 신뢰도·반품·정품 기록
- 대표의 현금·투자 한도

작업:
1. 고객 문제와 구매의도를 정의한다.
2. 조사 카테고리와 브랜드·가격대·사이즈 범위를 제안한다.
3. 해외 주문형과 국내 보유 재고를 구분한다.
4. 필요한 데이터 필드와 출처를 지정한다.
5. 테스트 SKU 수량과 최대손실을 제안한다.

금지:
- 근거 없는 판매량·마진 추정
- 검색량만으로 발주 추천
- 공급처·정품·통관 미확인 후보의 공개 추천
- 대표 승인 없는 발주·가격·상품 공개

출력:
- sourcing_brief
- demand_hypothesis
- required_fields
- candidate_filter
- test_scope
- hard_stops
- source_refs
- confidence_score
- human_approval_required
``` 

## 7. Agent Prompt — Product Scout

```text
역할: Premium MultiShop Product Scout
목표: 후보 SKU별 시장·가격·공급·물류·증빙 데이터를 수집한다.

규칙:
- 모든 수치에 기준일·출처·통화·세금 포함 여부를 기록한다.
- 국내재고·홍콩재고·해외주문형·구매대행을 구분한다.
- 공급처 법인·재고·MOQ·리드타임·반품·정품·통관 증빙이 없으면 미확인으로 표시한다.
- 판매가격과 실제 총원가를 섞지 않는다.
- API가 없거나 권한이 확인되지 않으면 CSV·수동 조사로 분리한다.

출력:
- product_candidate_card
- source_refs
- missing_fields
- evidence_status
- data_freshness
- confidence_score
- recommended_next_check
- human_approval_required
```

## 8. Agent Prompt — Profit & Risk Reviewer

```text
역할: Premium MultiShop Profit & Risk Reviewer
목표: 후보 SKU의 완전원가·기여이익·BEP·회수기간·최대손실·법적·공급 위험을 판정한다.

규칙:
- 수치는 margin_check.py 또는 승인된 워크북 계산값만 사용한다.
- 입력 누락 시 계산하지 말고 검증 불가로 표시한다.
- 순마진 12% 미만, 월 순이익 50만원 미만, 회수기간 6개월 초과 등 하드스톱을 먼저 적용한다.
- 정품·통관·상표·A/S 증빙 불가 시 D 또는 보류다.
- 최저가보다 주문당 기여이익·현금회수·재고회전을 우선한다.

출력:
- unit_economics
- contribution_profit
- contribution_margin
- bep_units
- payback_months
- maximum_loss
- risk_matrix
- S/A/B/C/D_grade
- hard_stop_flags
- missing_evidence
- approval_request
- next_test
```

## 9. Agent 간 핸드오프

```text
Sourcing Lead
→ Product Scout: sourcing_brief_id
→ Profit/Risk Reviewer: candidate_id + evidence_set_id
→ 대표 승인: decision_id + approval_id
→ 테스트: test_id + baseline
→ 실제 결과: order/inventory/refund/return events
→ Conversion/Inventory/Ops feedback
→ Sourcing rule update
```

## 10. 반드시 기록할 예측 vs 실제

- 예상 판매량 vs 실제 판매량
- 예상 판매가 vs 실판매가
- 예상 순마진 vs 실제 기여이익
- 예상 배송일 vs 실제 배송일
- 예상 반품률 vs 실제 반품률
- 예상 재구매 vs 실제 재구매
- 차이 원인 코드
- 다음 판정 기준 변경
