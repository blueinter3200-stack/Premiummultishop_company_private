---
source_path: ".pi/BusinessVault/plans/pms-governance-data-ai-architecture-review-2026-08-16.md"
source_filename: "pms-governance-data-ai-architecture-review-2026-08-16.md"
source_type: "text"
source_size_bytes: 12878
source_modified_at: "2026-08-16T16:47:08+09:00"
source_sha256: "e54db47ed9bd0d93149405e283225e43e4ef0183ecb8a6f29554e63d3edcb9ae"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS 거버넌스·데이터·AI 구조 점검 및 Agent 10 통합안

- 기준일: 2026-08-16
- 범위: 9-Agent Revenue Commerce OS, Queryable Data Map v1, Learning Architecture v2, Revenue Commerce OS v2, Revenue Ladder L0~L4, 상세페이지 영업 Agent, Global Trend & Content Scout
- 판정: **설계는 실행 가능한 방향으로 수렴했으나, 현재는 `설계 완료 / 운영 MVP 미완료 / 외부 write 보류`**

## 1. 총평

현재 문서들은 이미 다음을 일관되게 정의한다.

- AI는 후보·분석·초안·이상탐지만 만들고 가격·재고·발주·주문·환불·대량 CRM·법률 판단은 실행하지 않는다.
- 내부 ID와 외부 ID를 분리하고, Master(현재 승인상태)와 Event/Ledger(불변 사실)를 구분한다.
- source/freshness/data quality/rule·prompt·model version, 예측-실제, 오류코드, 승인, HOLD를 학습 루프에 포함한다.
- READY 3 + RARE 2, 최대 5 SKU의 소량 테스트를 기준으로 D+7/D+14/D+30/D+90을 본다.

다만 **Agent 10의 공통 계약, 권리·약관 판정, 메모리의 조회권한/보존정책, HOLD 전파, 규칙 승격 승인, 예측 freeze**가 개별 문서에 흩어져 있어 구현 시 누락될 위험이 있다. 이를 별도 Control Plane으로 묶어야 한다.

## 2. Agent 10과 9-Agent 연결

### 권장 지위

Agent 10 `Global Trend & Content Scout`는 당분간 10번째 의사결정 Agent가 아니라 **외부 신호 수집·권리/증거 큐레이션 계층**이다. 9-Agent의 결정권을 갖지 않고 Agent 1·4에만 신호를 공급한다.

```text
공개 원천
  → Agent 10 수집/권리·약관 검사
  → Trend Signal Card (trend_signal_id)
  → Agent 1 Sourcing Lead: 후보화
  → Agent 2 Product Scout: 공급·증거 확인
  → Agent 3 Profit & Risk: 완전원가·위험 판정
  → 대표 승인
  → Agent 4 GTM / 상세페이지 Agent: 독창적 콘텐츠 초안
  → Agent 5·6: 동의 기반 CRM·전환 측정
  → Agent 7~9: 주문·재고·배송·반품·HOLD
  → 예측-실제 학습 원장
```

Agent 10 출력은 `trend_signal_id`, `candidate_id`를 새로 만들 수 있지만 `sku_id`, `supplier_id`, `content_id`, `customer_id`를 임의 확정하지 않는다. 기존 엔터티로의 연결은 ID Match Service를 거치며, 불확실하면 `UNMATCHED_ID`/`AMBIGUOUS_ID`로 남긴다.

Agent 10의 권장 출력 계약:

- 원천: `source_platform`, `source_url`, 계정/작성자, 수집시각, 원문 해시 또는 증거 참조
- 신호: 브랜드·모델·스타일·시장·가격·반응지표·한국 검색/경쟁 신호
- 증거: `evidence_id`, 기준일, 캡처/원본 위치, 사실·추정 구분, freshness
- 권리: `rights_status`, `terms_status`, 상업적 재사용 가능 여부, 출처표시 필요 여부, 보류 사유
- 연결: `candidate_id`, `sku_match_status`, `supplier_match_status`
- 실행: `recommended_action`, `hard_stop_flags`, `human_approval_required`, `rule_version`, `memory_refs`

**금지:** 원본 이미지·영상·문구의 무단 복제/재게시, 약관을 우회한 대량 스크래핑, 공개 반응을 판매량으로 단정, 트렌드 신호만으로 자동 발주·자동 공개.

## 3. 공통 ID·Lineage 설계

현재 ID 목록에 아래 8개를 추가하면 10→9→거래→학습을 끊김 없이 추적할 수 있다.

| ID | 정체성/용도 |
|---|---|
| `trend_signal_id` | Agent 10이 수집한 개별 신호 |
| `evidence_id` | URL·파일·캡처·인보이스·검수 등 증거 단위 |
| `candidate_id` | 후보 SKU 카드. SKU 확정 전의 불변 ID |
| `experiment_id` | 5 SKU·콘텐츠·채널 테스트 단위 |
| `run_id` | 한 Agent 실행 단위; 입력 스냅샷과 출력 묶음 |
| `forecast_id` | 특정 decision/experiment에 대한 freeze된 예측 |
| `outcome_id` | 동일 예측기간의 실제 결과 |
| `rule_change_id` | 오류에서 생성된 규칙 후보·승격 이력 |

모든 산출물은 최소 다음 lineage를 가진다.

`run_id → input_record_ids → trend_signal_id/candidate_id/sku_id → decision_id → approval_id → experiment_id → forecast_id → outcome_id → error_id → rule_change_id`

외부 키는 `(source_system, account_id, external_id)`로 관리하고 내부 ID와 절대 혼합하지 않는다. 고객 식별자는 원문 노출을 줄이고 tokenized ID를 사용한다. 삭제·철회 요청과 보존 예외를 감사로그에 남긴다.

## 4. 메모리·예측/실제·규칙 버전

### 공통 Memory Record

메모리는 공유하되 append-only이며, 수정 대신 새 레코드를 추가한다.

`memory_id, memory_type, entity_refs, payload_ref, source_refs, observed_at, valid_from/to, confidence, data_quality, sensitivity_class, created_by, run_id, supersedes_id, retention_class`

유형은 기존 `FACT/EVIDENCE/DECISION/FORECAST/OUTCOME/ERROR/RULE_CANDIDATE/RULE_APPROVED/POLICY`를 유지한다. Agent별로 읽을 수 있는 메모리 범위를 분리한다. 특히 고객 개인정보·권리문서·법률 검토는 최소권한으로 제공하고, 프롬프트에 원문 전체를 복사하지 않는다.

### Forecast freeze

예측은 실행 전 `forecast_id`로 freeze한다. 이후 실제가 들어와도 예측값을 덮어쓰지 않는다.

- D+7: 초기 반응
- D+14: 판매 가능성
- D+30: CM1/CM2·재고회전
- D+90: 재구매·장기 수익

예측과 실제의 grain은 동일해야 한다: `experiment_id + sku_id + channel_id + period`. 실제 결과에는 환불·반품·보상·배송지연이 확정된 시점을 별도로 기록한다.

### 규칙 버전

`rule_set_id`, `rule_version`, `policy_version`, effective_from/to, 변경 diff, 근거 error IDs, 평가 결과, 승인자, rollback_version을 함께 저장한다. 규칙은

`DRAFT → SHADOW → CANARY(최대 5 SKU/제한 고객) → APPROVED → RETIRED`

로 승격한다. **하드스톱·법/약관·권리 규칙은 모델 점수나 Agent 다수결로 완화할 수 없다.** 규칙/프롬프트/모델 승격도 대표 승인 대상이다.

## 5. 승인·HOLD 통합

Decision Engine은 `ALLOW`, `REVIEW`, `HOLD`, `STOPPED`를 반환하며, 여러 Agent의 결과 중 **가장 강한 차단 상태가 전체 실행 상태를 지배**한다.

### HOLD를 발생시키는 최소 조건

- `MISSING/STALE/UNMATCHED_ID/AMBIGUOUS_ID/QUARANTINED` 핵심 데이터
- 완전원가·재고·결제·반품·배송 증거 불충분
- 정품·통관·A/S·상표·광고표현 검토 미완료
- 권리 또는 플랫폼 약관 상태가 `UNKNOWN/RESTRICTED`
- CRM 동의 없음/철회/빈도·중복 규칙 미통과
- CM1 또는 CM2 계산 불가/비양수, 기존 하드스톱 위반
- 승인 토큰·원복 계획·손실상한 없음

HOLD는 해당 `entity_id`뿐 아니라 연결된 `offer_id`, `content_id`, `campaign_id`, `order_line_id`로 전파한다. 해제는 `exception_id`에 원인·교정·재검증 증거·재개조건·승인자를 기록하고, 기존 승인으로 자동 재개하지 않는다.

승인 레코드 필수값: `approval_id, requested_by, approver, scope/entity_refs, before_after, reason, evidence_refs, rule/policy_version, max_loss, expires_at, rollback_plan, decision, decided_at`.

## 6. 권리·약관·법적 리스크 통합

권리 상태를 부가 메모가 아닌 **실행 게이트**로 둔다.

| 영역 | 최소 판정 | 실패 시 |
|---|---|---|
| 공개 콘텐츠 | 내부 분석 가능/상업 재사용 가능/출처표시/금지 범위 구분 | 원본 복제·게시 HOLD |
| 플랫폼 약관 | API·수집빈도·자동화·상업 이용·계정 권한 확인 | 수집 방식 중단, 수동/공식 export 전환 |
| 이미지·영상·문구 | 라이선스·허가·자체 제작 여부 | 상세페이지/광고 사용 HOLD |
| 상표·셀럽·비교표현 | 사실성·출처·광고표시·혼동 가능성 검토 | 표현 삭제/전문가 검토 |
| 병행수입·구매대행·DDP | 판매자·수입자·통관명의·반품/환불 책임 확정 | 상품 공개·발주 HOLD |
| 개인정보·CRM | 수집 목적·동의·철회·보유기간·채널별 수신 가능 | 발송·매칭·학습 사용 HOLD |
| 약속·보상·공식성 | 실제 이행능력·상한·법률/약관 검토 | 카피 게시 HOLD |

법률/통관/정품 판단은 AI 확정값이 아니라 `EXPERT_REVIEW_REQUIRED`로 기록하고 관세사·법률전문가·대표의 승인으로 닫는다.

## 7. 실제 MVP 순서

### MVP-0 (최우선): Control Plane, 1주

- 데이터 사전·ID Registry·외부 ID mapping
- 원본 등록/해시/기준일/담당자/신선도
- 공통 Agent envelope·Memory record·권리 상태
- Exception/HOLD/Approval ledger
- CSV/manual import 및 quarantine

**완료:** 5개 샘플 SKU와 20개 Trend Signal Card를 중복 없이 등록하고, 모든 레코드가 내부 ID·출처·기준일·상태·owner를 가진다. 승인 없는 write가 0건이어야 한다.

### MVP-1: 거래·증거 정본, 1주

- Product/SKU·Supplier·Offer·Inventory·Customer/Consent master
- Order/Refund/Shipment/RMA·Cost·Inventory ledger
- 정품/통관/권리/반품 증거 연결

**완료:** 5 SKU에 landed cost/CM1 계산, 재고 불변 이력, 주문-출고-반품 연결이 가능하고 누락은 계산 대신 HOLD로 표시된다.

### MVP-2: Agent 10 → Sourcing 3, 1주

- Trend Signal Card → Candidate Card → Product Scout → Profit & Risk Reviewer
- 국내 수요·공급·마진 매칭
- 대표 승인 요청 생성

**완료:** 20개 신호에서 5개 이하 후보가 생성되고, 후보마다 권리·증거·공급·원가·risk·추천/보류 사유가 있다. Agent 10이 SKU 확정/발주/게시를 직접 하지 않는다.

### MVP-3: 5 SKU 운영 테스트, 30일

- READY 3·RARE 2
- 상세페이지/콘텐츠 초안은 사실·권리 통과 후 사람 승인
- 주문·재고·배송·반품·CRM 동의·CM1/CM2 연결

**완료:** 각 SKU/채널/실험에 forecast freeze와 D+7/D+14/D+30 outcome이 있고, 예측-실제 variance와 오류코드가 100% 기록된다. CM1/CM2가 양수인지 여부를 데이터로 판정할 수 있어야 한다.

### MVP-4: 제한된 학습·읽기 전용 연동

- 1개 공급처/Cafe24/ERP의 read-only CSV/API 중 검증된 것만
- 오류 반복 → RULE_CANDIDATE → shadow/canary → 대표 승인
- CRM은 소수 동의 고객으로만 제한 테스트

**완료:** 재처리·원복·권한 만료·실패 큐를 시험했고, 승인 전 규칙/모델이 운영결과를 바꾸지 않는다.

## 8. 완료 정의(Definition of Done)

전체 MVP 완료는 문서/코드 존재가 아니라 다음 증거를 모두 통과한 상태다.

1. **ID 정합성:** 핵심 외부 키 매핑 중복 0, 미매칭/모호 매칭은 숨김 없이 큐에 존재.
2. **원장 정합성:** 주문 = 결제 - 취소 - 환불, 재고 = 기초 + 입고 - 판매 + 반품 ± 조정.
3. **Lineage 100%:** Agent 결과가 원본·메모리·결정·승인·예측/실제·규칙 버전으로 역추적 가능.
4. **권리/약관:** 20개 신호 전부 rights/terms 상태가 있고 UNKNOWN은 HOLD.
5. **HOLD 안전성:** stale·증빙·동의·CM1·승인 실패를 실제 publish/send/write 전에 차단.
6. **Human approval:** 가격·공개·발주·환불·대량 CRM·정책/규칙 승격에 유효한 approval_id와 만료/원복 계획 존재.
7. **예측 학습:** 5 SKU에 D+7/D+14/D+30 freeze forecast와 outcome, variance, root cause가 존재.
8. **재현성:** 동일 입력 스냅샷+동일 rule/prompt/model 버전으로 동일 판정 또는 차이를 설명 가능.
9. **보안/개인정보:** 고객 원문 최소 노출, 역할별 접근, 철회/보존/삭제 처리 경로 검증.
10. **운영 시험:** import 실패, ID 모호, stale 재고, 권리 미확인, 동의 철회, 가격 오류, 배송 지연을 각각 발생시켜 HOLD→교정→재검증→승인→재개를 성공시킴.

## 9. 즉시 결정할 3가지

1. `Agent 10 = 외부 신호 계층` 지위를 30일 동안 고정하고, 모든 출력은 Trend Signal Card/권리 게이트를 통과시킨다.
2. MVP-0의 단일 Control Plane 스키마와 `HOLD` 우선순위를 먼저 구현한다. 9-Agent별 별도 메모리·승인 DB를 만들지 않는다.
3. 2026-08-29 완료 목표는 **실제 API 연동 완료가 아니라 CSV/manual 기반 20 신호·5 후보·5 SKU의 추적·승인·예측/실제·HOLD 검증 완료**로 정의한다.

### 확인 불가/보류

현재 문서상 Cafe24·ERP·POS·카카오·공급처 API 권한/필드/계정 소유권, 실제 고객 동의 범위, 법률·통관 전문가 검토 결과, 실제 5 SKU의 원가·재고·주문 데이터는 확인되지 않았다. 따라서 위 설계는 운영 준비 기준이며, 실제 write·대량 발주·대량 발송·자동 가격변경의 완료를 의미하지 않는다.
