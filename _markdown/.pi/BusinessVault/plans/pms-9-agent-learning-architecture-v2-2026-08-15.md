---
source_path: ".pi/BusinessVault/plans/pms-9-agent-learning-architecture-v2-2026-08-15.md"
source_filename: "pms-9-agent-learning-architecture-v2-2026-08-15.md"
source_type: "text"
source_size_bytes: 17007
source_modified_at: "2026-08-15T21:53:28+09:00"
source_sha256: "4fddc49558429d952196ca653413e3a6ef65172a788bf26e6a9c97534661b630"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS 9-Agent Learning Architecture v2.0

- 기준일: 2026-08-15
- 사업: Premium MultiShop
- 상태: 설계안 / CSV·manual MVP 우선 / 실제 API·모델 학습은 검증 전 보류
- 상위 원칙: Agent는 사람을 대체하지 않고, 증거·수익·위험·예측오차를 정리해 대표의 승인 품질을 높인다.

## 1. 목표와 비목표

### 목표

기존 루프를 **재현 가능하고 중단 가능한 학습 루프**로 확장한다.

```text
원천 수집 → 품질검사·격리 → Agent 분석 → 독립 검토·합의
→ 대표 승인/HOLD → 제한된 테스트 → 예측·실제 확정
→ 오류 원인·신뢰도 갱신 → 규칙 후보 평가
→ 대표 승인된 규칙 버전만 다음 실행에 적용
```

학습의 대상은 우선 `규칙·데이터 필드·프롬프트·모델 선택`이며, 자동으로 모델 가중치나 하드스톱을 바꾸지 않는다.

### 비목표

- 실제 API 연동·쓰기 권한이 확인되지 않은 자동 실행
- 관측 데이터만으로 인과효과·진정한 수요를 주장하는 것
- 적은 표본에서 ML 모델을 운영 모델로 승격하는 것
- 법률·정품·통관·개인정보 판단을 AI 단독으로 하는 것

## 2. 9-Agent 계약과 공통 Envelope

기존 9개 역할은 유지한다.

| Agent | Pod | 핵심 학습 질문 |
|---|---|---|
| A1 Sourcing Lead | Sourcing | 어떤 카테고리·고객 문제를 조사할 것인가 |
| A2 Product Scout | Sourcing | 후보 상품·공급·증거가 실제로 존재하는가 |
| A3 Profit & Risk Reviewer | Sourcing | 완전원가·현금·법적·운영 위험 후에도 남는가 |
| A4 GTM Lead | Sales/GTM | 어떤 고객·채널·가치제안이 맞는가 |
| A5 CRM/Outreach | Sales/GTM | 동의된 고객에게 어떤 접점이 기여이익을 만드는가 |
| A6 Conversion Reviewer | Sales/GTM | 퍼널의 어느 단계가 실제 손익을 막는가 |
| A7 Commerce Ops Lead | Commerce Ops | 주문·출고·현금·예외가 정상인가 |
| A8 Inventory & Pricing | Commerce Ops | 가격·재고 조치가 마진과 회전을 함께 개선하는가 |
| A9 Order/Risk Auditor | Commerce Ops | 오류·사기·증빙·정책 위반을 사전에 막는가 |

모든 실행은 다음 공통 Envelope로 저장한다.

```yaml
run_id: RUN-YYYYMMDD-0001
agent_id: A1..A9
pod: sourcing|gtm|commerce_ops
entity_type: sku|offer|campaign|customer|order|inventory_lot|supplier
entity_id: internal_id
decision_id: DEC-...
run_at: ISO-8601
as_of_date: YYYY-MM-DD
input_record_ids: []
source_refs: [{source_id, file_name, row_or_range, captured_at}]
data_quality_id: DQ-...
model_id: model-or-manual
prompt_version: P-...
rule_version: R-...
policy_version: POL-...
memory_refs: [MEM-...]
forecast_ref: FC-...
confidence: {overall, evidence, freshness, identity, model, calibration}
recommendation: EXECUTE|TEST|HOLD|STOP|ESCALATE
hard_stop_flags: []
human_approval_required: true|false
approval_id: null|APR-...
output_hash: sha256:...
```

**불변성:** 원본 파일, Agent 출력, 승인, 예측, 실제, 오류 분류는 append-only다. 수정은 새 버전·보정 행으로 남긴다.

## 3. Agent 간 메모리 설계

### 3.1 메모리 종류

| 메모리 | 내용 | 수명/갱신 | 읽기 권한 | 쓰기 권한 |
|---|---|---|---|---|
| `FACT` | SKU·주문·원가·재고·동의 등 검증된 사실 | 영구, 원장 append | 전 Agent(필터 적용) | Source/ETL만 |
| `EVIDENCE` | 인보이스·상품여권·스크린샷·CSV 행·출처 | 증거 유효기간 | 관련 Agent·대표 | Scout/Reviewer 제안, 사람 검증 |
| `DECISION` | 추천·근거·승인·HOLD·거절·예외 | 영구 | 전 Agent | 해당 Agent 제안, 사람 확정 |
| `FORECAST` | 시점별 판매·마진·배송·반품·재구매 예측 | 테스트 단위 | Reviewer·Conversion·Ops | Agent 제안, freeze 후 불변 |
| `OUTCOME` | 결제·환불·배송·재고·현금의 실제 결과 | 영구 | 전 Agent | 원장/수동 검수 |
| `ERROR` | 차이 원인·영향·재발·교정조치 | 영구 | 전 Agent | Conversion/Auditor 제안, 대표 확정 |
| `RULE_CANDIDATE` | 새 규칙·적용범위·시뮬레이션 결과 | 승인 전 임시 | 평가자·대표 | Learning Coordinator |
| `RULE_APPROVED` | 승인된 규칙 버전과 효력기간 | 영구 | Rule Engine/전 Agent | 대표 또는 지정 승인자 |
| `POLICY` | 금지·승인·하드스톱·개인정보·법률 정책 | 영구 | 모두 | 대표/전문가 |

### 3.2 메모리 경계

- Agent는 타 Agent의 **최종 사실과 승인된 결정**을 읽지만, 다른 Agent 메모리를 덮어쓰지 않는다.
- 추론·가설은 `FACT`로 승격할 수 없고 `HYPOTHESIS`로 남긴다.
- Customer PII는 토큰화된 `customer_id`만 Agent에 노출하며, CRM Agent도 동의·철회·보류 필드를 우회할 수 없다.
- `FACT`, `OUTCOME`, `APPROVED POLICY`가 충돌하면 최신 출처가 아니라 **source-of-truth·기준일·승인상태**로 해결하고 예외 큐에 남긴다.
- 모든 메모리는 `valid_from`, `valid_to`, `owner`, `status`, `confidence`, `supersedes_id`를 가진다.

### 3.3 교차 Agent 전달 계약

다음 Agent로 넘길 때 `handoff_id`, 입력 ID, 누락 필드, 하드스톱, confidence, 다음 담당자, 기한, 재개 조건을 필수로 한다. 누락 필드가 있으면 추천이 아니라 `HOLD_DATA_GAP`로 넘긴다.

- A1→A2: 조사 범위·수요 가설·금지 카테고리
- A2→A3: 후보 카드·공급 증거·기준일·대체 공급처
- A3→A4: 테스트 등급·가격·최대손실·법적 검토 필요
- A4→A5: 대상 세그먼트·채널·메시지 초안·예산 상한
- A5→A6: 노출/상담/발송 로그·동의 근거·제외군
- A6→A7/A8: 퍼널 오차·판매속도·가격/재고 가설
- A7/A8→A9: 주문·재고·가격 예외와 조치 후보
- A9→Learning Coordinator: 감사 결과·원인코드·재발 여부

## 4. 규칙·프롬프트·모델 버전 관리

### 4.1 Registry

`version_registry`에 다음을 저장한다.

| 필드 | 설명 |
|---|---|
| `version_id`, `artifact_type` | R/P/M/POL/DQ 스키마 버전 |
| `parent_version` | 바로 전 버전 |
| `effective_from/to` | 적용 기간 |
| `scope` | Agent·Pod·SKU군·채널 |
| `change_reason` | 오류·정책·데이터 개선 근거 |
| `test_set_ref` | 고정 회귀평가 세트 |
| `approval_id`, `approved_by` | 승인권자와 시각 |
| `rollback_to` | 즉시 원복할 버전 |
| `status` | DRAFT→SHADOW→CANARY→APPROVED→RETIRED |

### 4.2 변경 원칙

1. 정책·하드스톱·금지영역은 규칙 후보가 자동 변경할 수 없다.
2. 새 버전은 과거 결정 데이터의 **고정 회귀세트**와 최근 테스트 세트에서 기존 버전과 비교한다.
3. `SHADOW`에서는 추천만 만들고 실행·대표 화면의 정본을 바꾸지 않는다.
4. `CANARY`는 대표가 승인한 1~2개 저위험 테스트에만 적용한다.
5. 성능·안전·공정성·데이터 품질 기준을 모두 통과한 뒤 대표가 `APPROVED`한다.
6. 오차 급증, 하드스톱 누락, 데이터 스키마 변경 시 즉시 이전 승인 버전으로 롤백하고 HOLD한다.

### 4.3 규칙 우선순위

`법률/개인정보/정품·통관 정책 > 현금·손실 하드스톱 > 대표 승인 정책 > 데이터 품질 게이트 > 단위경제 규칙 > 최적화·추천 규칙 > LLM 문장 생성`.

## 5. 예측 vs 실제 원장

### 5.1 예측 고정 시점

예측은 `PREDICTED_AT`에 freeze한다. 실제가 쌓인 뒤 예측을 수정하지 않고, 새 예측은 새 `forecast_id`를 만든다.

최소 예측 항목:

- 기간: D+7 / D+14 / D+30 / D+90
- 판매수량, 순매출, 주문당 기여이익, 총 기여이익
- 할인율, 반품·취소율, 배송 SLA, 재구매율
- 현금 유입일, 회수기간, 최대손실
- 확률구간(P50/P80), 예측 근거와 confidence

### 5.2 실제 확정 규칙

- 주문: 결제·취소·환불·반품 확정 후 순매출을 확정
- 비용: 매입·운송·관세·수수료·CS·반품·광고/CRM 배부 원장과 대조
- 재고: 실사/이동/판매/반품/손상 조정 후 로트 기준 확정
- 배송: 실제 인계·도착·지연을 운송장/수동 증빙과 대조
- 재구매: 동일 customer_id의 확정 주문만 계산
- 미확정 데이터는 `PROVISIONAL`로 두고 평가에 섞지 않는다.

### 5.3 차이 계산과 원인 코드

`variance = actual - predicted`; 상대오차는 실제가 0인 경우 `N/A`로 표시한다. 원인 코드는 복수 선택 가능하다.

`DEMAND_OVER`, `DEMAND_UNDER`, `PRICE`, `COST_OMISSION`, `FX_TAX`, `SUPPLY_STOCK`, `LEAD_TIME`, `CONTENT`, `CHANNEL`, `TARGET`, `CONSENT`, `EXECUTION_DELAY`, `DATA_DUPLICATE`, `DATA_STALE`, `ID_MATCH`, `MODEL_DRIFT`, `EXTERNAL_MARKET`, `COMPLIANCE`, `UNKNOWN`.

각 오류는 `evidence_refs`, 영향금액, 통제 실패 지점, 재발횟수, 교정조치, owner, due_date, 재검증 결과를 가진다. 같은 원인 2회 반복 시 프롬프트 수정이 아니라 데이터 필드·규칙·승인 절차를 우선 재검토한다.

## 6. 신뢰도와 중단 조건

### 6.1 신뢰도는 단일 LLM 점수가 아니다

`overall_confidence`는 다음 구성요소와 근거를 함께 보여준다.

- `evidence`: 증빙 완전성·독립 출처
- `freshness`: 기준일·stale 여부
- `identity`: SKU/고객/주문 매칭 확실성
- `unit_economics`: 완전원가·현금 계산 완전성
- `model`: 모델의 과거 calibration/회귀 성능
- `execution`: 공급·재고·배송 실행 가능성

가중 평균은 MVP에서 **계산 규칙으로 고정**하고, 표본이 쌓인 뒤에만 calibration을 검토한다. 데이터 부족 시 점수를 억지로 채우지 않고 `UNKNOWN`/`HOLD`다.

### 6.2 공통 하드스톱

다음 중 하나면 `STOP/HOLD`이며 높은 예측점수로 우회하지 못한다.

- 정품·통관·법적 책임 증빙 불가
- 완전원가 또는 현금회수 계산 불가
- 순마진·기여이익 하드스톱 위반
- stale 재고·중복·미매칭 ID
- 고객 동의 불명·철회 고객·보류 고객 CRM 대상
- 최대손실·재고 Lock·원복 방법 미정
- 승인 없는 외부 쓰기·발주·결제·발송
- 모델/규칙 버전·입력 출처·예측 freeze 누락
- 오류 큐 미해결 또는 동일 오류 재발 후 안전통제 미적용

### 6.3 중단과 재개

모든 테스트는 `RUNNING→PAUSE→STOPPED→REVIEWED→RESUMED` 상태를 가진다.

- `PAUSE`: 데이터 지연, 목표 판매속도 미달, 배송/재고 이상. 신규 노출·발주를 멈추고 기존 고객 처리를 계속한다.
- `STOPPED`: 기여이익 적자, 법률/정품/동의 위반, 최대손실 도달, 중대한 가격·재고 오류. 재고회수·고객보호를 우선한다.
- `RESUMED`: 원인·조치·재검증·대표 승인·새 버전이 모두 기록된 경우에만 가능.

기존 PMS 하드스톱(SKU 5개 이하, 테스트 투자 300만원 이하, 순마진 12% 미만 등)은 이 아키텍처가 대체하지 않으며 상위 정책으로 유지한다.

## 7. 모델·Agent 평가 체계

### 7.1 평가 대상

- A1/A2: 후보 증거의 정확성·누락률·중복률
- A3: 완전원가 계산 일치율·하드스톱 재현율·위험 누락률
- A4/A5: 승인된 메시지의 사실성·동의 준수·기여이익
- A6: 퍼널 병목 진단의 hit rate·테스트 승률
- A7/A8: 예외 탐지 precision/recall·가격/재고 오탐 비용
- A9: 위험 탐지 recall·중대 누락 0 목표·복구 가능성
- 전체: 예측 calibration, 대표 override율, override 후 결과, 손실 회피액, 추적 가능성

### 7.2 최소 평가 프로토콜

1. **오프라인 회귀:** 과거 승인/거절 사례와 금지 사례를 고정 세트로 평가
2. **블라인드 비교:** Agent/모델 이름을 숨기고 동일 입력을 평가
3. **Shadow:** 실제 쓰기 없이 현재 규칙과 차이를 기록
4. **Canary:** 저위험·소량·대표 승인 테스트
5. **Outcome:** D+7/D+14/D+30/D+90 실제와 비교
6. **승격:** 정확도만이 아니라 손실·안전·데이터 품질·설명가능성 기준을 동시 통과

LLM의 유창성·자신감은 성능 지표가 아니다. 수치 계산은 스프레드시트/코드/원장이 정본이다.

## 8. 데이터 품질 게이트

### 8.1 CSV/manual MVP 필수 메타데이터

`file_id`, 원천 시스템, 담당자, 수집일시, 기준일, checksum, schema_version, 행 수, 개인정보 포함 여부, 내부 ID 매핑 상태, 비용 통화, quarantine 사유를 원본 등록부에 남긴다.

### 8.2 품질 규칙

| 차원 | 검사 | 실패 시 |
|---|---|---|
| 완전성 | 필수 ID·원가·재고·동의·기준일 | 해당 Agent HOLD |
| 유효성 | 날짜·통화·수량·상태·가격 범위 | quarantine |
| 유일성 | event_id·source key·주문 중복 | 중복 행 격리 |
| 일관성 | 주문/환불/재고/원가 합계 | reconcile 실패 |
| 적시성 | 재고·가격·공급 feed freshness | stale 차단 |
| 매칭성 | 내부-외부 ID mapping | UNMATCHED/AMBIGUOUS |
| 증거성 | 정품·통관·배송·수신동의 출처 | 실행 금지 |
| 편향/대표성 | 채널·고객·SKU 표본 편중 | 평가 범위 제한 |

품질 점수는 결과 요약용이며, 하드스톱을 상쇄하지 않는다. 실패 행은 삭제하지 않고 `QUARANTINED`와 원인으로 보존한다.

## 9. Human-in-the-loop 및 권한 경계

### 자동화 가능(부작용 없는 영역)

- CSV 등록·checksum·schema 검사·중복 탐지
- 내부 ID 후보 매핑(AMBIGUOUS는 사람 큐)
- 원장 합계·마진·BEP·회수기간 계산
- 시장/경쟁 자료 수집 및 후보 카드 초안
- 예측 계산·예측 freeze·D+7/14/30/90 리포트
- 예외 우선순위·stale/가격/재고 이상 탐지
- CRM 세그먼트 **후보**와 메시지 초안 생성
- 승인된 템플릿의 내부 리포트·알림 생성

### 대표 또는 지정 승인 필요

- 신규 SKU 공개·테스트 범위·예산·최대손실
- 가격·할인·재고 이동·발주·결제
- 대규모 CRM 발송·새 세그먼트·빈도 변경
- 환불·고액 보상·정책 예외
- 규칙/프롬프트/모델 버전 승격·하드스톱 변경
- 해외 주문형·DDP·통관·정품 책임 문구
- API write 권한·외부 업체·개인정보 처리 변경

승인 기록: `approval_id`, 대상, 변경 전/후, 근거, 예상 손실, 원복 방법, 승인자, 시각, 만료일.

### 금지 영역

- AI 단독 발주·결제·가격 변경·상품 공개·환불·주문 취소
- 동의 불명/철회 고객에게 CRM 발송 또는 고객 자동 병합
- 증빙 없는 정품·통관·법률 보증
- 관측 데이터만으로 수요·증분매출 보장
- 승인 없이 하드스톱·중단 조건·규칙 버전 변경
- 데이터 오류·stale 상태를 숨기거나 수동으로 정답화
- 대표 승인 전 대량 발주·대량 발송·대규모 쓰기

## 10. CSV/manual MVP 구현 순서

### MVP-0: 학습 원장

`source_registry`, `data_quality_issue`, `agent_run`, `memory_item`, `version_registry`, `approval_ledger`를 CSV/SQLite로 만든다.

### MVP-1: 5 SKU 테스트 연결

기존 Product/Supplier/Inventory/Offer/Cost/Order/RMA 원장과 `decision_id`, `forecast_id`, `outcome_id`를 연결한다. READY 3개·RARE 2개 이내, D+7/D+14/D+30을 필수로 한다.

### MVP-2: 오류·평가 대시보드

SKU/Agent/규칙 버전별로 forecast bias, absolute error, hard-stop 위반, 대표 override, 데이터 실패, 손실·회피액을 표시한다.

### MVP-3: Shadow/Canary

신규 규칙은 먼저 shadow, 이후 대표가 선택한 저위험 1~2개에 canary 적용한다. 실제 API는 읽기 전용·권한 확인 후에만 별도 검토한다.

### MVP-4: 제한 자동화

검증된 범위에서만 내부 알림·리포트·quarantine 자동화. 외부 시스템 write는 승인 토큰·idempotency key·rollback/compensating action이 모두 존재할 때만 별도 승인한다.

## 11. 주간 학습 회의 산출물

1. 상위 10개 예측오차와 원인코드
2. 데이터 품질 실패·미매칭·stale 목록
3. 대표 override와 결과
4. 중단/재개 테스트 및 최대손실 대비 실제
5. 규칙 후보의 회귀·shadow·canary 결과
6. 다음 주 승인 요청 3개 이하
7. 유지·수정·폐기할 메모리와 만료 증거

## 12. 완료 정의

- 모든 Agent run이 출처·기준일·데이터 품질·rule/model/prompt 버전을 가진다.
- 예측은 freeze되고 실제는 원장과 대조되며 오차 원인이 분류된다.
- 메모리·규칙·승인은 append-only/audit 가능하다.
- 하드스톱·중단·재개 조건이 실행 상태와 연결된다.
- CSV/manual에서도 5 SKU의 D+7/D+14/D+30 폐쇄루프가 재현된다.
- 대표 승인 없이 외부 쓰기·발주·결제·CRM 대량발송이 불가능하다.
- API·ML 고도화는 이 조건을 통과한 뒤에만 진행한다.
