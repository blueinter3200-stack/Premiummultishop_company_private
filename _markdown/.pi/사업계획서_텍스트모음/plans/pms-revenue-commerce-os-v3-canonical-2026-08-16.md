---
source_path: ".pi/사업계획서_텍스트모음/plans/pms-revenue-commerce-os-v3-canonical-2026-08-16.md"
source_filename: "pms-revenue-commerce-os-v3-canonical-2026-08-16.md"
source_type: "text"
source_size_bytes: 9987
source_modified_at: "2026-08-16T16:49:44+09:00"
source_sha256: "4c29cad9cbcce2aa949d5bcf50e61892e9809c86338efbdc20c666ad2550e618"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS Revenue Commerce OS v3.0 — Canonical Operating Design

- 기준일: 2026-08-16
- 사업: Premium MultiShop
- 문서 상태: **최종 정본(Canonical)**
- 실제 수익 개선 상태: 검증 전 / Cafe24·GA4·ERP·POS·카카오·공급처 데이터 미연결

## 0. 이 문서의 우선순위

이 문서는 다음 문서들의 상위 정본이다.

- 9-Agent Revenue Commerce OS
- 9-Agent Learning Architecture
- Revenue Ladder Profitability Redesign
- 계단형 상품·고객·수익 구조
- 상세페이지 전환 시스템
- 90/180일 성장 로드맵
- Queryable Data Map
- Trust Commerce·READY/RARE/CARE 문서

세부 문서와 충돌하면 이 문서의 **축 분리·하드스톱·승인·데이터 상태**를 우선한다.

## 1. PMS의 목적

PMS는 AI 기술 회사가 되는 것이 아니다.

> **시장 신호를 실제 구매·기여이익·현금회수·재구매로 전환하고, 예측과 실제의 차이로 다음 판단을 개선하는 Premium Commerce Revenue OS**다.

매출 증가만으로 성공을 판정하지 않는다.

- CM1·CM2·CM3
- 현금회수기간
- 재고회전일
- 반품·보상·A/S 비용
- 신규·기존 고객별 LTV
- 장기재고·최대손실
- 고객 신뢰·재구매

## 2. 반드시 분리해야 하는 5개 축

현재 문서의 혼동을 제거하기 위해 L0~L4를 모든 개념의 통합 계단으로 사용하지 않는다.

### 축 A — Customer Stage: 고객 관계 단계

| 단계 | 의미 | 고객에게 하는 일 |
|---|---|---|
| C0 | 익명 관심 | 콘텐츠·검색·가격·신뢰 정보 |
| C1 | 식별된 관심 | 회원·카카오·선호·상담 |
| C2 | 첫 구매 | 저위험 상품으로 신뢰·데이터 회수 |
| C3 | 주력 반복 구매 | Main Product·교차판매·재구매 |
| C4 | 고관여·고가 고객 | Premium·예약·상담 |
| C5 | VIP·B2B 관계 | 개인소싱·Pre-order·B2B |

### 축 B — Offer/Inventory: 상품·재고 운영 유형

| 유형 | 핵심 가치 | 기본 운영 |
|---|---|---|
| READY | 국내 실물·검수·속도 | 국내 창고·빠른 출고·국내 반품 |
| RARE | 가격·희소성·구색 | 해외 주문형·조달·통관 조건 공개 |
| CARE | 구매 후 관리 | A/S·수선·세탁·보관·분쟁 지원 오버레이 |

CARE는 별도 가격 레벨이나 재고유형이 아니라 READY·RARE·Premium·VIP에 붙는 **서비스 오버레이**다.

### 축 C — Value/Margin: 상품 경제성 단계

| 단계 | 가격대 | 역할 | 상태 |
|---|---:|---|---|
| Entry | 30,000~150,000원 | 첫 구매·신뢰·데이터 | 가설·실제 CM1 검증 필요 |
| Main | 300,000~1,500,000원 | 핵심 주문·CM2 | 가설·실제 손익 검증 필요 |
| Premium | 1,500,000~5,000,000원 | 객단가·상담·신뢰 프리미엄 | 가설·현금노출 검증 필요 |
| Concierge | 가격 고정 없음 | 예약·개인소싱·B2B·LTV | 주문별 조건·최대손실 검증 |

가격대는 전략 가설이지 시장 사실이나 마진 보장이 아니다. 실제 원가·수요·반품·현금 데이터를 확보하기 전 확정값으로 사용하지 않는다.

### 축 D — Operating Agents: 업무 조직

기존 9-Agent는 유지한다.

- Sourcing: Sourcing Lead / Product Scout / Profit & Risk Reviewer
- Sales/GTM: GTM Lead / CRM-Outreach / Conversion Reviewer
- Commerce Ops: Commerce Ops Lead / Inventory-Pricing / Order-Risk Auditor

### 축 E — Time Gates: 검증 시간

- D+7: 초기 반응
- D+14: 판매 가능성
- D+30: CM1·CM2·재고회전
- D+90: 재구매·장기 수익
- 180일: 채널·매장·공급 포트폴리오

## 3. 고객·상품 매트릭스

고객 단계와 상품 단계는 같은 것이 아니다.

```text
C0/C1 관심 고객
→ Entry 상품 또는 콘텐츠·상담

C2 첫 구매 고객
→ Entry·Main READY

C3 반복 구매 고객
→ Main READY/RARE + CARE

C4 고관여 고객
→ Premium READY/RARE + CARE

C5 VIP/B2B
→ Concierge·예약·개인소싱·Pre-order
```

고객을 가격만으로 승급시키지 않는다. 실제 구매·수령·반품·재구매·서비스비용·동의 상태를 함께 본다.

## 4. 수익 판단 계층

```text
CM0 = 순판매금액 - 상품·운송·통관·입고 원가
CM1 = CM0 - 주문·결제·포장·배송·반품·상담비
CM2 = CM1 - 광고·콘텐츠·CRM·제휴비
CM3 = CM2 - CAC·A/S·VIP·서비스 비용 + 실제 검증 재구매 기여이익
```

- 최초 주문 승인: CM1·CM2 중심
- 고객 투자 승인: 실제 코호트 LTV·CM3 중심
- 미래 재구매를 최초 주문에 선반영하지 않음
- 계산 누락은 0원이 아니라 `검증 불가`

## 5. L0 콘텐츠의 최적 정의

L0는 상품 레벨이 아니라 **수요 신호·고객 식별 계층**이다.

Premium MultiShop 주제:

- 해외 명품 가격차
- 유럽 신상품
- 정품 확인법
- 국내·유럽 가격 비교
- 셀럽 착용상품의 출처·모델 분석
- 병행수입·해외 주문형·국내재고 차이
- 통관·반품·A/S 체크리스트

K-Beauty는 BELLOON으로 분리한다.

L0 성공식:

```text
콘텐츠 증분 CM2
= 콘텐츠 귀속 주문 CM1
- 콘텐츠·광고·CRM 비용
```

콘텐츠가 직접 주문을 만들지 않아도 C1 회원·카카오·상담으로 이어질 수 있으나, 이후 구매 코호트의 실제 증분 CM2·LTV로 검증해야 한다.

## 6. Global Trend & Content Scout의 위치

Global Trend & Content Scout는 당분간 10번째 의사결정 Agent가 아니다.

> **외부 신호·증거·권리 큐레이션 계층**

흐름:

```text
공개 해외 신호
→ trend_signal_id
→ 권리·약관 상태 확인
→ Sourcing Lead
→ Product Scout
→ Profit/Risk Reviewer
→ 대표 승인
→ GTM·상세페이지·CRM
→ Ops·실제 성과
```

필수 ID:

- `trend_signal_id`
- `source_ref`
- `rights_status`
- `evidence_id`
- `candidate_id`
- `decision_id`
- `approval_id`
- `experiment_id`
- `forecast_id`
- `outcome_id`
- `error_id`
- `rule_change_id`

금지:

- 무단 복제·재게시
- 약관 우회 스크래핑
- 상업적 이미지·영상의 권리 미확인 사용
- 셀럽·인기·판매량의 무근거 사실화
- 반응 데이터만으로 자동 발주

`rights_status = UNKNOWN`이면 콘텐츠·상품 공개·광고를 HOLD한다.

## 7. 상세페이지 영업 구조

모든 Entry·Main·Premium 페이지에 다음 순서를 적용한다.

```text
3초 이해
→ Persona Problem
→ Solution Preview
→ Benefit
→ Proof
→ Risk Reversal
→ 실제 Scarcity
→ Feature
→ CTA
→ FAQ
```

- READY: 실물·검수·구성품·출고·국내 반품
- RARE: 조달·리드타임·통관·관부가세·해외 반품
- Premium: 증거·상담·CARE·책임·보상 조건
- Concierge: 예약금·조달 실패·환불·B2B 조건

AI는 상품 원장·증거·정책에 있는 사실만 초안에 사용한다. 사람이 승인하기 전 Cafe24·광고·CRM에 게시하지 않는다.

## 8. Control Plane

### 공통 상태

```text
ALLOW → REVIEW → APPROVED → PUBLISHED
                   ↓
                 HOLD
                   ↓
                STOPPED
                   ↓
  교정 → 재검증 → 대표 승인 → RESUMED
```

HOLD는 다음 대상에 전파된다.

- SKU
- Offer
- Content
- Campaign
- Order Line
- Supplier

### 공통 HOLD 조건

- stale 데이터
- 내부 ID 불일치
- 완전원가 누락
- CM1·CM2 계산 불가
- 정품·통관·A/S 증거 공백
- 권리·약관 상태 미확인
- 고객 수신동의 불명
- 승인·원복 계획 부재
- 재고·가격 오류
- 반품·분쟁·보상 위험 미평가

## 9. MVP 순서

### MVP-0 Control Plane

- 내부 ID
- source registry
- evidence registry
- rights status
- approval/HOLD
- memory·rule version

완료 정의: 한 건의 signal이 `signal→candidate→decision→approval→experiment`로 추적된다.

### MVP-1 거래·증거 정본

- SKU·공급처·재고·주문·원가·배송·RMA
- READY·RARE·CARE 필드

완료 정의: 주문·재고·원가 정합성 검증 통과.

### MVP-2 Trend→Sourcing 연결

- 20개 Trend Signal Card
- 5개 이하 후보 SKU
- 권리·증거·공급·마진 검토

완료 정의: 자동 발주 없이 후보→승인 대기까지 연결.

### MVP-3 5 SKU 전환 테스트

- READY 3
- RARE 2
- 상세페이지 전환 구조
- D+7·D+14·D+30 forecast/outcome

완료 정의: CVR·장바구니율·매출/세션·CM1·CM2·반품·문의가 같은 ID로 연결.

### MVP-4 제한적 read-only 연동

- Cafe24·GA4·ERP·POS·카카오·공급처
- CSV 우선
- API는 읽기 전용
- Shadow·Canary 규칙 평가

완료 정의: 승인 없는 외부 write 0건, HOLD 전파·재개 테스트 통과.

## 10. 90일·180일 의사결정 게이트

### 30일

- 데이터 정합성
- 5 SKU 상세페이지
- 콘텐츠·상담·주문 귀속
- CM1·CM2

### 90일

- 고객 단계 이동률
- 실제 LTV
- 재고회전
- 반품·A/S·보상 비용
- 채널별 CM2
- 예약 쇼룸·매장별 기여이익

### 180일

- 매장 유지·축소·예약제·통합
- READY·RARE 포트폴리오
- 공급처·3PL·홍콩 운영
- 검증된 가격·재고 자동화 범위

## 11. 최종 하드스톱

다음 중 하나라도 충족하지 못하면 확대하지 않는다.

- 실제 주문당 CM1·CM2 계산 불가
- 데이터 신뢰도 0.70 미만
- 순마진율 12% 미만
- 월 순이익 500,000원 미만
- 회수기간 6개월 초과
- 리드타임 45일 초과
- 재고회전일 90일 초과
- 투자금이 가용현금의 30% 초과
- 정품·통관·A/S·보상 책임 입증 불가
- 권리·약관 상태 UNKNOWN
- 승인 없는 write·대량 발송·발주

## 12. 최종 원칙

```text
신호를 수집한다.
상품·고객·서비스·Agent를 섞지 않는다.
수익과 현금을 계산한다.
증거와 권리를 확인한다.
대표가 승인한다.
소량 테스트한다.
예측과 실제를 비교한다.
오류를 기록한다.
검증된 규칙만 승격한다.
```
