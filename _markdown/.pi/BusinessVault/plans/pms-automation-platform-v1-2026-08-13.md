---
source_path: ".pi/BusinessVault/plans/pms-automation-platform-v1-2026-08-13.md"
source_filename: "pms-automation-platform-v1-2026-08-13.md"
source_type: "text"
source_size_bytes: 16357
source_modified_at: "2026-08-13T21:21:44+09:00"
source_sha256: "8a896d01b06cbc88f73ed75a72e0d8125030de8eddd0ca6cc385746065f7f7a7"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Automation Platform v1.0

- 사업: Premium MultiShop
- 기준일: 2026-08-13
- 상태: 구축 방향 확정 / 실제 개발·연동은 별도 승인 필요
- 목표: 상품 수가 많은 쇼핑몰이 아니라 **세계 공급망에서 지금 살 가치가 있는 상품을 찾아주는 쇼핑몰**의 운영 시스템 구축

## 1. 한 줄 결론

## 1.1 PMS 핵심 성장 루프
## 1.2 PMS Revenue SEO OS

SEO는 단순 유입 채널이 아니라 **무엇을 소싱하고 판매할지 알려주는 데이터 센서**로 운영한다. 최종 KPI는 조회수가 아니라 SEO 유입에서 발생한 주문·기여이익·재구매다.

```text
Google / Naver / 쇼핑몰 / 경쟁사 데이터
  ↓
AI Trend Agent — 뜨는 브랜드·상품 탐지
  ↓
Keyword Agent — 구매의도 키워드 발굴
  ↓
Sourcing Agent — PMS 재고·해외 공급처 API 매칭
  ↓
Profit Agent — 판매가·원가·수수료·광고비·마진 계산
  ↓
Decision Engine — S / A / B / C / D 판정
  ↓
Content Agent — 상품·카테고리·비교·가이드 콘텐츠 생성
  ↓
Cafe24 승인 등록
  ↓
Google Search · Merchant Center · Shopping · Images · Lens · Naver
  ↓
주문·매출·기여이익
  ↓
카카오 CRM·재구매
  ↓
판매 데이터가 다음 소싱·키워드 판단으로 환류
```

### SEO 전제조건

1. 중복 상품·카테고리·파라미터 URL을 대표 URL로 통일한다.
2. 내부링크·canonical·sitemap에서 동일한 대표 URL을 일관되게 사용한다.
3. Cafe24 상품·카테고리 구조를 검색 의도와 상품군에 맞게 정리한다.
4. Product·Breadcrumb 등 구조화 데이터를 정확한 실제 상품 데이터와 함께 제공한다.
5. sitemap과 Search Console 색인 상태를 상품 출시·종료 프로세스와 연결한다.
6. Merchant Center 상품 데이터와 자사몰 상품 DB의 가격·재고·배송·반품 정보를 일치시킨다.

Google 공식 가이드상 canonical은 중복 URL의 대표 URL 신호이며, 내부 링크·sitemap·canonical의 URL 일관성이 중요하다. Product 구조화 데이터와 Merchant Center 피드는 상품 가격·재고·배송 등 검색 노출 정보를 정확하게 전달하는 기반이다. 출처: [Google canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [Google ecommerce URL](https://developers.google.com/search/docs/specialty/ecommerce/designing-a-url-structure-for-ecommerce-sites), [Google Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product), [Google Merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing).

### 상품페이지 SEO 자산화

상품이 승인되면 Content Agent가 다음 산출물을 만들고, 사람 또는 Rule Engine 검수 후 Cafe24에 반영한다.

- SEO 상품명
- Meta Title
- Meta Description
- 상품 설명
- 구매 전 FAQ
- 이미지 ALT
- 관련상품
- 카테고리·비교·가이드 내부링크
- Product·Offer·Breadcrumb Schema용 데이터
- 가격·재고·배송·반품 정보

AI가 만든 상품 정보는 공급처 원문을 복사하지 않고, 검증된 Product Master와 승인된 사실만 사용한다. 가격·재고·배송·정품·구성품을 추측해 생성하지 않는다.

### 콘텐츠 허브와 상품 연결

```text
2026 여성 명품 스니커즈 추천
  → 비교 콘텐츠
  → Golden Goose vs Maison Margiela
  → 브랜드 카테고리
  → 상품 상세
  → 구매
  → 카카오 CRM·재구매
```

콘텐츠 KPI는 노출·조회에 머물지 않는다. `SEO 유입 매출`, `SEO 유입 기여이익`, `상품 상세 전환율`, `콘텐츠→상품 클릭률`, `CRM 재구매율`을 함께 기록한다.

### Google Shopping 연결

```text
PMS Product DB / API
  → Cafe24
  → Google Merchant Center
  → Google Search
  → Google Shopping / Images / Lens
```

Merchant Center 전송 전 가격·재고·배송·반품·이미지·상품 식별자 검사를 통과해야 한다. API 오류, 가격 불일치, 품절, 승인 거절, 정책 위반 가능성이 있으면 자동 전송·광고를 보류한다.

### 일일 의사결정 산출물

| 산출물 | 내용 | 실행 상태 |
|---|---|---|
| Trend Brief | 뜨는 브랜드·상품·검색 신호 | AI 분석 후 검토 |
| Keyword Opportunity | 구매의도·경쟁·공급가능성·마진 후보 | 검증 필요 |
| Sourcing Match | PMS 재고·해외 공급처·API 매칭 | 증빙 필요 |
| Profit Sheet | 판매가·원가·수수료·광고비·기여이익 | 코드 계산 |
| Decision Queue | S/A/B/C/D 등급과 중단 사유 | 사람 승인 |
| Content Queue | 상품·카테고리·비교·가이드 초안 | 사실 검수 |
| SEO Revenue Report | 유입·주문·순매출·기여이익·재구매 | 데이터 연결 필요 |

### 결정 규칙

```text
키워드 기회 점수
= 검색수요 × 구매의도 × 예상기여이익 × 공급가능성 × 재고회전
  ÷ 경쟁강도·가격리스크·반품리스크
```

위 식은 방향을 나타내는 모델이며, 실제 점수·순이익·순마진·회수기간은 SKU별 입력값을 코드로 계산한다. 입력값이 부족하면 발주가 아니라 `검증 보류`다.


Premium MultiShop은 내부 운영 자동화만 하는 시스템이 아니라, 시장의 변화를 실제 매출과 재구매로 연결하는 **Trend-to-Repeat Commerce Loop**를 구축한다.

```text
트렌드
  → 키워드
  → 상품발굴
  → 해외소싱
  → AI 콘텐츠
  → 검색노출
  → 판매
  → CRM
  → 재구매
  → 판매·고객 데이터가 다음 트렌드 분석으로 환류
```

| 단계 | PMS가 하는 일 | 핵심 통제지표 |
|---|---|---|
| 트렌드 | 브랜드·카테고리·검색·소셜·고객문의 신호 수집 | 출처·기준일·신호 강도 |
| 키워드 | 검색어·상품명·브랜드·시즌 키워드 구조화 | 검색의도·경쟁도·상업성 |
| 상품발굴 | 후보 SKU와 공급처·경쟁가·수요 비교 | 가격·재고·정품·DDP·마진 |
| 해외소싱 | 정품·인보이스·한국 배송·DDP·반품 검증 | 공급처 신뢰도·리드타임·총원가 |
| AI 콘텐츠 | 상품의 ‘지금 살 가치’를 설명하는 콘텐츠 생성 보조 | 사실성·출처·승인상태·중복률 |
| 검색노출 | 자사몰 SEO·콘텐츠·검색 유입 운영 | 노출·클릭·상품조회·전환 |
| 판매 | Cafe24·매장·KREAM 등 채널별 판매 실행 | 기여이익·재고회전·현금회수 |
| CRM | 관심·구매·사이즈·브랜드·휴면 고객 매칭 | 동의·발송빈도·상담·전환 |
| 재구매 | 구매 후 관리·재입고·유사상품·VIP 선공개 | 재구매율·LTV·CRM 기여이익 |

AI는 트렌드 해석·키워드 묶음·상품 후보·콘텐츠 초안을 만들 수 있지만, 정품·가격·재고·DDP·상품 공개·CRM 발송은 Rule Engine과 사람 승인을 통과해야 한다. 판매·재구매 데이터는 다시 트렌드와 키워드 판단에 환류시킨다.

반복 업무는 자동화하고, 고객·가격·재고·주문·환불·법적 책임에 위험이 생기는 순간 자동 차단 후 사람에게 넘기는 **Human-in-the-loop 운영 플랫폼**으로 구축한다.

## 2. 기준 아키텍처

```text
고객 / 상품 / 재고 / 주문 / 상담 / 배송 / 반품
                    ↓
                PMS Core
 Customer Master · Product Master · Order Master · Inventory Master
                    ↓
                Rule Engine
 가격 · 재고 · 고객등급 · 배송 · 반품 · CRM 규칙
                    ↓
             Automation Engine
 CRM · 주문 · 출고 · 재고 · 반품 · 카카오 업무 자동화
                    ↓
                  AI Layer
 고객추천 · AI Buyer · 상담지원 · 상품선별
                    ↓
      Cafe24 · 카카오 · 물류 · Realpacking · 관리자
```

AI는 핵심 값을 직접 변경하지 않는다. AI는 판단 후보·요약·추천을 만들고, Rule Engine이 정책을 적용하며, 위험 작업은 사람 승인 후 실행한다.

## 3. 자동화 권한 수준

| 수준 | 의미 | 예시 |
|---|---|---|
| L1 자동 | 위험이 낮고 되돌릴 수 있음 | 재고 원장 기록, 고객등급 계산, 로그 생성 |
| L2 자동+예외검토 | 정상 흐름은 자동, 예외는 보류 | 추천대상 생성, 배송상태 동기화, 출고 라우팅 |
| L3 사람승인 | 금액·법적·고객 영향이 큼 | 최초 상품 공개, 판매가격 변경, 고액 환불, 대규모 CRM, 고객 병합 |

## 4. PMS Core 우선순위

### Customer Master

Cafe24·POS·ERP·매장 고객·카카오 접점을 고객 단위로 연결한다. 전화번호·회원번호·이메일 등 확실한 식별자가 일치할 때만 자동 연결하고, 애매한 경우 `MERGE_REVIEW`로 사람에게 보낸다. AI의 임의 고객 병합은 금지한다.

보유 예시 필드:

- 고객 ID
- 구매 횟수·누적 구매액·최근 구매일
- 브랜드·카테고리·사이즈·색상 선호
- 평균 구매가·반품률·기여이익
- 매장·상담·카카오 접점
- 광고·메시지 수신 동의 및 철회 상태
- 세그먼트·등급·마지막 갱신 시각

### Product Master

브랜드·모델·시즌·품번·색상·사이즈·공급처 SKU·정품/통관 증빙·이미지 권한·판매채널·DDP/DAP·원가·최저 판매가를 통합한다.

### Inventory Master

- `PMS_DOMESTIC_STOCK`: 창고·매장에 실제 보유한 재고
- `PMS_GLOBAL_SUPPLY_STOCK`: 해외 공급처 재고

상태:

```text
입고 → 판매가능 → 예약 → 피킹 → 포장 → 출고
```

재고 0, stale inventory, API 불일치, 품질 보류 시 판매를 자동 차단한다. 국내 즉시출고와 글로벌 배송을 고객에게 구분 표시한다.

### Order Master

Cafe24 주문과 공급처 주문을 하나의 내부 주문으로 연결한다.

```text
Cafe24 결제완료
→ PMS 주문 생성
→ 상품·옵션 검증
→ 재고 Lock
→ 국내/글로벌 라우팅
→ 출고 또는 공급처 예약
→ 송장 수집
→ Cafe24 상태 업데이트
→ 고객 안내
```

중복 주문·중복 차감·품절 후 주문을 방지하고 모든 상태 변경을 이력화한다.

## 5. 핵심 자동화 모듈

### CRM Trigger Engine

| 이벤트 | 자동 처리 | 승인 수준 |
|---|---|---|
| 관심 브랜드 신상품·재고 입고 | 적합 고객 후보 생성 | L2 |
| 고객 사이즈 재입고 | 사이즈 적합 고객 매칭 | L2 |
| 가격 하락 | Price Opportunity 후보 생성 | L2 |
| 장바구니 이탈 | 리마인드 후보 생성 | L2/L3 발송 |
| 90일 미구매 | 재활성화 후보 생성 | L3 발송 |
| VIP 신규 진입 | Benefit 후보 적용 | L2/L3 혜택 |
| 구매 완료 | 리뷰·관리 안내 후보 | L2 |
| 반품 완료 | 사유 코드 기반 추천 조정 | L1/L2 |

수신동의·발송빈도·중복캠페인·수신거부를 먼저 확인한다. 전체 고객 일괄 발송을 기본값으로 만들지 않는다.

### Customer Tier

구매금액·구매빈도·최근구매일·기여이익·재구매·브랜드 충성도를 매일 계산한다.

예시:

`ACTIVE / LOYAL / BRAND_VIP / HIGH_VALUE / POTENTIAL_VIP / LAPSED`

등급은 혜택과 CRM 우선순위에 사용하되, 고객 차별·법적 문제가 발생하지 않도록 정책을 별도로 검토한다.

### OMS/WMS·Realpacking

출고는 다음 순서를 강제한다.

```text
주문 Scan → 상품 Barcode Scan → 주문 일치 확인 → 검수
→ Realpacking 촬영 → 포장 완료 → 송장 Scan → 출고
```

단계 누락, 바코드 불일치, 검수 실패 시 `SHIPMENT_HOLD`로 전환한다. Realpacking은 선택 기능이 아니라 출고 품질관리 절차로 운영한다.

### RMA

```text
RETURN_REQUESTED → 회수 → 입고검수 →
재판매 / 불량 / 공급처반품 / 폐기 → 환불·교환 → Customer Master 반영
```

반품 사유는 코드화한다. 예: 사이즈·상품설명 불일치·단순변심·하자·배송파손·구성품 누락·정품/검수 이슈.

### CS 통합

고객 화면에 고객정보·구매이력·현재 주문·배송·Realpacking·반품·관심브랜드·추천 후보를 함께 표시한다. 초기 AI는 고객에게 직접 답변하지 않고 상담직원 보조로 제한한다.

## 6. AI Buyer·Customer Match

AI Buyer는 공급처 상품을 다음 순서로 평가한다.

```text
상품 발견 → 동일 SKU 공급처 비교 → 가격·재고·정품·배송·DDP
→ 국내 경쟁가 → PMS 고객 적합성 → 기여이익 → 지금 살 가치
```

두 조건이 모두 충족되어야 CRM 후보가 된다.

- `BUY_OPPORTUNITY`: 상품 자체의 가격·공급·수익 조건이 통과
- `CUSTOMER_OPPORTUNITY`: 적합하고 연락 가능한 고객군 존재

예시 흐름:

```text
AI Buyer가 상품 후보 생성
→ Rule Engine이 증빙·가격·재고·마진 검증
→ Customer Master에서 브랜드·카테고리·사이즈·가격대·활성도 필터
→ CRM 발송 후보 생성
→ 사람 승인
→ 카카오/Meta/자사몰 캠페인
```

AI가 판매가격·주문·재고·환불·고객 병합을 직접 실행하지 않는다.

## 7. 대표 Dashboard

### 오늘의 고객

- 재구매 후보
- 신규 VIP
- 휴면 재활성화 후보
- 추천 성공·실패

### 오늘의 상품기회

- AI Buyer 발견상품
- 가격기회
- 재입고
- 판매중단

### 오늘의 운영

- 정상 주문
- 출고대기
- 글로벌 주문
- 배송지연
- 반품
- CS 미해결
- Realpacking 누락

### 오늘의 수익

- 매출
- CM1: 상품·배송·플랫폼 등 직접비 차감 후 기여이익
- CM2: 광고·CRM 비용 차감 후 기여이익
- CX Cost
- CM3: 운영·고정비 배부 후 수익

데이터가 연결되지 않은 지표는 임의로 채우지 않고 `데이터 미연결`로 표시한다.

## 8. 개발 순서

### 1차: Foundation

- Customer Master
- Product Master
- Central Inventory
- Order Master

### 2차: Operation

- OMS
- WMS
- Realpacking
- RMA
- CS 통합

### 3차: CRM

- 고객등급
- Customer Segment
- CRM Trigger
- First Access

### 4차: Intelligence

- Customer Match
- PMS Value Engine
- AI Buyer

### 5차: 고도화

- 공급처 자동 선택
- 자동 가격 감지
- 추천 학습
- 수요예측
- CRM 발송 최적화

AI Buyer는 Foundation·Operation 데이터가 쌓인 후 연결한다.

## 9. 1차 개발 수용 기준

1. 고객 중복 자동연결은 확실한 식별자 일치만 허용한다.
2. 애매한 고객 병합은 `MERGE_REVIEW`에 남는다.
3. 재고 상태 변경은 불변 이력으로 남는다.
4. 재고 Lock과 중복 주문 방지가 동작한다.
5. 상품·가격·환불·고객 병합은 Rule Engine 또는 승인 없이는 변경되지 않는다.
6. 출고 바코드 불일치와 Realpacking 누락은 `SHIPMENT_HOLD`가 된다.
7. 반품 사유가 코드로 저장된다.
8. 모든 CRM 발송 후보는 수신동의·빈도·중복 규칙을 통과해야 한다.
9. 예외·실패·재처리·승인 로그를 조회할 수 있다.
10. 대표 Dashboard의 미연결 지표를 허위 수치로 표시하지 않는다.

## 10. 하드스톱·범위 제한

- Cafe24·POS·ERP·카카오·물류 API 스펙과 권한이 확인되기 전 실제 연결을 완료했다고 보고하지 않는다.
- 고객 데이터 동의·보관·매칭 가능 범위가 확인되기 전 일괄 CRM을 실행하지 않는다.
- 공급처 정품·DDP·API·반품 책임이 확인되기 전 AI Buyer의 자동 공개·자동주문을 허용하지 않는다.
- 개발자에게 계정 비밀번호·인증번호·API 키를 채팅으로 받지 않는다.
- 초기에는 자동주문·자동가격변경·고액환불·대규모 메시지 발송을 허용하지 않는다.

## 관련 문서

- [[plans/premium-multishop-digital-positioning|디지털 전환 포지셔닝]]
- [[plans/premium-multishop-real-time-supply-sales-funnel-2026-08-13|글로벌 공급·실시간 연동·판매 퍼널]]
- [[plans/premium-multishop-integration-architecture|Cafe24·공급처 연동 아키텍처]]
- [[research/premium-multishop-sourcing-landscape-2026-08-13|해외 공급처 후보·검증 지형도]]
