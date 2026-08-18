---
source_path: ".pi/BusinessVault/plans/pms-revenue-commerce-os-v3-2026-08-14.md"
source_filename: "pms-revenue-commerce-os-v3-2026-08-14.md"
source_type: "text"
source_size_bytes: 11257
source_modified_at: "2026-08-15T17:09:47+09:00"
source_sha256: "39b6278f7ef0c365b18d50e0f7e5fa675e9c63a3e98c0a6a147c38d494c31e46"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Revenue Commerce OS v3.0

- 사업: Premium MultiShop
- 기준일: 2026-08-14
- 상태: 구조 고도화안 / 실제 연동·개발은 권한·데이터 확인 후 승인
- 범위: Trend-to-Repeat, Revenue SEO, 상품·공급·재고·주문·반품·CRM·기여이익 통합

## 1. 결론

PMS는 블로그·광고·CRM을 각각 운영하는 도구 묶음이 아니라 **무엇을 소싱하고, 어떤 고객에게, 어떤 채널에서, 얼마의 기여이익으로 판매할지 결정하는 Revenue Commerce OS**로 구축한다.

워크북 v2는 성과 기록층으로 유지한다. v3는 기록에 그치지 않고 다음을 통제한다.

- 상품 공개 전 공급·정품·DDP·원가·현금회수 검증
- 콘텐츠 발행 전 검색의도·상품 연결·사실·광고표시 검증
- 광고·CRM 실행 전 기여이익·동의·중복·예산 승인 검증
- 주문·출고·반품 후 예측과 실제의 차이 기록
- 실제 판매·반품·재구매 데이터를 다음 소싱·콘텐츠 결정에 환류

## 2. 현재 워크북의 한계와 보완

| 현재 상태 | 부족한 점 | v3 보완 |
|---|---|---|
| Google Ads CPC/CPA | 광고 이전 상품·공급·현금 검증 부족 | SKU/공급/완전원가 게이트 |
| SEO 콘텐츠 매출 | 콘텐츠→주문 귀속과 재구매 연결 제한 | 이벤트 ID·어트리뷰션 원장 |
| 키워드 상품 판정 | 점수 입력 주관성·근거 추적 부족 | 출처·기준일·신뢰도·승인로그 |
| CRM 재구매 | 동의·고객식별·반품 후 LTV 부족 | Customer Master·Suppression·LTV 원장 |
| 경영대시보드 | 수기 입력·실제 데이터 연결 미확정 | 데이터 품질 상태·예외 큐 |
| 승인 규칙 | 규칙은 있으나 실행 이력 부족 | Rule ID·승인자·시각·변경 전후 값 |
| 공급·재고 | 공급처 API·DDP·재고 Lock 미연결 | 공급처·SKU·재고 원장과 stale 차단 |
| 반품·A/S | 수익성·재구매 학습에 미반영 | RMA·정품·수선·고객가치 반영 |

## 3. 운영 계층

```text
L0. Source & Consent Layer
    Search Console·Naver·Google·Cafe24·카카오·POS·ERP·공급처·물류
    출처·기준일·동의·원본 ID 보존

L1. Master & Ledger Layer
    Customer·Product·Supplier·Inventory·Order·Content·Campaign Master
    Cost·Revenue·Attribution·RMA·Approval·Audit Ledger

L2. Decision Layer
    Data Quality Gate·Profit Agent·Sourcing Gate·Content QA·CRM Gate
    Rule Engine과 S/A/B/C/D Decision Engine

L3. Execution Layer
    Cafe24·광고·Merchant Center·Naver·카카오·물류·Realpacking
    초기에는 읽기·후보 생성·사람 승인 중심

L4. Learning Layer
    예측 vs 실제 차이·수요·가격·반품·재구매·공급 신뢰도 학습
```

AI는 L2의 후보·분류·초안만 만들고 L1 원장을 직접 변경하지 않는다.

## 4. 필수 Master와 원장

### 4.1 Customer Master

필수 필드:

- PMS 고객 ID
- 원천별 고객 ID(Cafe24·POS·카카오·Meta)
- 식별자 유형·매칭 신뢰도
- 브랜드·카테고리·사이즈·색상 선호
- 구매·반품·상담·재구매 이력
- 수신동의·철회·채널·일시·근거
- VIP·LTV·기여이익·휴면 상태

애매한 고객은 `MERGE_REVIEW`로 정지한다.

### 4.2 Product·SKU Master

- 브랜드·모델·시즌·성별·카테고리
- SKU·옵션·사이즈·색상·바코드
- 국내/글로벌 재고 유형
- 정품·인보이스·구성품·A/S 증빙
- 상품 페이지·콘텐츠·키워드 연결
- 판매상태: 후보/검증중/승인/공개/중단/재고회수

### 4.3 Supplier Master

- 법인·국가·공급처 ID
- 브랜드 공급 증빙
- SKU별 상업 인보이스
- 한국행 DDP 조건
- 관세·부가세·통관·반품·진위분쟁 책임
- API/feed·갱신시각·오류율
- 샘플통관 상태

공개 웹사이트·NDA만으로 공식 수권·독점·총판을 확정하지 않는다.

### 4.4 Inventory Ledger

재고 유형:

- 국내 실재고
- 매장 보유재고
- 창고 보유재고
- 공급처 확인 재고
- 예약·Lock 재고
- 검수·반품·보류 재고

공급처 재고는 API 오류·stale·가격 급변·정품 증빙 미확인 시 판매 가능 재고로 간주하지 않는다.

### 4.5 Order·RMA Ledger

주문·출고·취소·반품·환불·교환·수선 상태를 불변 이력으로 보존한다.

```text
결제완료
→ 주문검증
→ 재고 Lock
→ 국내 출고/공급처 예약
→ 검수·포장
→ 송장
→ 배송
→ 구매확정
→ 반품/수선
→ 최종 기여이익
```

## 5. Revenue Decision Engine

### 5.1 의사결정 7단계

1. **Trend Signal**: 신호 출처·기준일·중복 확인
2. **Keyword Intent**: 정보/비교/상품/가격/재입고 의도 분류
3. **Product Match**: PMS SKU·공급처·고객군 매칭
4. **Landed Cost**: 원가·환율·DDP·관세·배송·수수료·반품충당금
5. **Profit & Cash**: 기여이익·회수기간·최대손실·재고회전
6. **Decision**: S/A/B/C/D와 승인자·재평가일
7. **Execute & Learn**: 공개·판매·반품·재구매 실제값과 예측 차이 기록

### 5.2 하드스탑

- 순마진율 12% 미만
- 월 예상 순이익 500,000원 미만
- 회수기간 6개월 초과
- 데이터 신뢰도 0.70 미만
- 법적 안전성 4/5 미만
- 리드타임 45일 초과
- 재고회전일 90일 초과
- 투자금이 가용현금의 30% 초과
- 정품·통관·A/S 입증 불가

하나라도 확인되면 발주·공개가 아니라 **보류·중단**이다.

## 6. Revenue SEO OS 고도화

### 콘텐츠 유형

- 트렌드·가이드: 관심 형성
- 비교: 구매 고려
- 상품: 구매 전환
- 가격·재입고·사이즈: 구매 직전·CRM
- 관리·A/S: 구매 후·재구매

### 콘텐츠 공개 게이트

- 원출처·기준일 확인
- 상위 콘텐츠 복사·유사 재작성 여부 확인
- 실제 상품·재고·가격·배송·반품 연결
- Product·Breadcrumb 데이터 일치
- 광고·제휴·판매 이해관계 표시
- 의료·법률·금융·세금 고위험 주제 별도 검토
- 담당자·승인자·게시일·수정일 기록

AI는 제목·초안·FAQ·ALT·내부링크 후보를 만들 수 있지만 허위 경험·근거 없는 숫자·최저가·정품 단정을 만들지 않는다.

### 어트리뷰션 이벤트

모든 콘텐츠·캠페인에 다음 ID를 붙인다.

- Content ID
- Keyword ID
- Product/SKU ID
- Campaign ID
- Customer Segment ID
- Order ID

기본 경로:

```text
Content → Product View → Inquiry → Cart → Order → Paid → Return → Repeat Order
```

## 7. 승인 매트릭스

| 작업 | 자동 | 예외 검토 | 대표 승인 |
|---|---|---|---|
| 데이터 수집·리포트 | 가능 | 오류 시 | - |
| 키워드 후보 생성 | 가능 | 점수·근거 검토 | - |
| 콘텐츠 초안 | 가능 | 사실·표시 검수 | 최초 공개 |
| 검색어 제외·입찰 인하 | 가능 | 주간 검토 | - |
| 광고 예산 증액 | - | 안건 생성 | 필요 |
| 신규 상품 공개 | - | 검수 대기 | 필요 |
| 가격 인상·인하 | - | 시나리오 생성 | 필요 |
| 재고·주문·환불 | - | 예외 큐 | 고액·예외 필요 |
| 카카오 CRM 발송 | - | 동의·중복·기여이익 검토 | 대규모·신규 캠페인 |
| 고객 병합 | 확실한 식별자만 | `MERGE_REVIEW` | 애매한 건 승인 |

## 8. 일간·주간·월간 운영 루프

### 일간

- stale 재고·가격 오류·주문 예외
- 공급처 API 실패·판매중지
- Realpacking 누락·배송지연
- 신규 문의·VIP·반품 알림

### 주간

- 검색어 감사
- 콘텐츠별 상품 클릭·상담·주문·기여이익
- 광고 캠페인 손익
- CRM 세그먼트·수신거부·재구매
- 예측 vs 실제 차이
- S/A/B/C/D 재평가

### 월간

- 채널별 순매출·기여이익
- 공급처 신뢰도·배송·반품·진위분쟁
- 재고회전·장기재고·현금회수
- 고객 LTV·재구매·CRM 기여이익
- 규칙 변경·예외·승인 감사

## 9. KPI 체계

### 재무

- CM1: 상품·결제·배송·반품 등 직접 변동비 후
- CM2: 광고·콘텐츠·CRM 비용 후
- 월 순이익
- 현금회수기간
- SKU별 최대손실

### 운영

- 재고 정확도
- 재고 Lock 실패율
- 출고 리드타임
- 반품률·반품 사유
- 정품·통관 증빙 완성률
- 공급처 SLA·API 오류율

### 성장

- 키워드→상품 클릭률
- 상품→상담·주문 전환율
- SEO 유입 CM2
- CRM 재구매율
- 고객 LTV
- 콘텐츠별 30/60/90일 기여이익

조회수·팔로워·ROAS는 보조지표이며 단독 승인 근거가 아니다.

## 10. 최소 구축 순서

### Phase 0 — 데이터·권한 확인

Cafe24·POS·ERP·카카오·Meta·물류·공급처 API 접근권한, 식별자, 데이터 형식, 담당자, 보안정책 확인. 미확인 상태에서는 연동 개발을 시작하지 않는다.

### Phase 1 — 수동 원장 MVP

- SKU·공급처·완전원가
- 키워드·콘텐츠·상품 연결
- 주문·반품·CRM 결과
- 승인·예외·감사로그
- 워크북 v2 기반 주간 운영

### Phase 2 — 읽기 전용 연동

공급처 1곳·SKU 20~50개·읽기 전용 가격/재고만 연결한다. 공개·주문·가격변경은 사람 승인.

### Phase 3 — OMS·RMA·Customer Master

주문·재고 Lock·출고·반품·고객 식별을 연결한다. 각 이벤트의 원장과 재처리 기준을 확정한다.

### Phase 4 — CRM·Content Agent

동의 기반 카카오 세그먼트와 승인된 콘텐츠·상품 연결을 운영한다.

### Phase 5 — AI Buyer·예측

최소 30일 이상의 실제 판매·반품·가격·재구매 데이터가 쌓인 후 사용한다. AI 자동 발주·자동 가격변경은 후순위다.

## 11. 구현 보류 조건

다음 정보가 없으면 개발·발주·공개를 보류한다.

- Cafe24 API 권한·필드·rate limit
- POS/ERP 데이터 형식·바코드·매장 재고 실시간성
- 카카오 수신동의·세그먼트·발송 API
- 공급처 API/feed·재고 기준시각·주문/취소/배송/반품
- SKU별 landed cost
- 고객 식별자와 병합 기준
- RMA·환불·고액 승인권한
- 데이터 보존·접근권한·개인정보 처리 기준

## 12. 구현 후 검증

- 주문 1건의 전체 이벤트 추적
- 고객 1건의 매칭·동의·CRM 제외 추적
- SKU 1건의 원가·가격·재고·콘텐츠·주문·반품 연결
- 실패·중복·재시도·수동승인·롤백 테스트
- 실제 주문 대비 Purchase 이벤트 ±10% 이내
- 오류·예외·승인 로그 재현성

## 관련 산출물

- `/opt/data/Premium_MultiShop_Revenue_SEO_Workbook_v2.xlsx`
- `/opt/data/Premium_MultiShop_Revenue_SEO_Workbook_v3_Architecture.xlsx` — Master·이벤트·식별자·원장·승인·예외·어트리뷰션·MVP·기술아키텍처 확장판
- [[plans/pms-revenue-seo-os-workbook-v2-critical-review-2026-08-15|워크북 v2 사업모델 비판적 검토]]
- [[plans/pms-execution-control-v1-2026-08-15|PMS 실행 운영·통제 고도화 구조]]
- [[plans/pms-automation-platform-v1-2026-08-13|PMS Automation Platform v1.0]]
- [[plans/pms-external-ai-agent-adoption-v1-2026-08-13|PMS 외부 AI 에이전트 도입 정책]]
