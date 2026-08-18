---
source_path: ".pi/사업계획서_텍스트모음/plans/premium-multishop-yesstyle-api-profitability-review-2026-08-15.md"
source_filename: "premium-multishop-yesstyle-api-profitability-review-2026-08-15.md"
source_type: "text"
source_size_bytes: 6872
source_modified_at: "2026-08-15T18:28:08+09:00"
source_sha256: "9d7b228bf0a6c42284e6a0414f938eb58bfe6fe3c8ba553e8b7bf386e7309f8e"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# YesStyle API·Premium MultiShop 연동 수익성 검토

- 기준일: 2026-08-15
- 사업 구분: Premium MultiShop 검토용. K-뷰티 직접 판매 확장 시 BELLOON과 상품·손익·CRM을 분리 기록해야 함.
- 상태: 공식 API·도매 공급권 확인 전 검증 보류

## 1. 한 줄 결론

**YesStyle API 연동 자체는 수익모델이 아니다.** 공개자료에서 확인되는 것은 글로벌 소매 플랫폼과 최대 10% 제휴 프로그램이며, Premium MultiShop이 공급가로 매입·재판매할 수 있는 공식 도매/드랍쉬핑 API는 확인되지 않았다.

## 2. 가능한 세 가지 모델

### A. Affiliate

```text
Premium MultiShop 콘텐츠
→ YesStyle 링크 클릭
→ 고객이 YesStyle에서 결제
→ Premium MultiShop 커미션
```

- 공식 공개자료에서 최대 10% 커미션 프로그램 확인
- 재고·배송·환불 책임은 상대적으로 낮음
- 고객 주문·상품 데이터·재구매 데이터를 직접 확보하기 어려움
- Premium MultiShop 자사몰 매출·CRM으로 잡히지 않을 가능성
- 명품 멀티샵 포지셔닝과 K-뷰티 소매 제휴가 혼재될 위험

**판정: 콘텐츠 수익화 테스트에는 가능, Premium MultiShop 핵심 판매모델로는 약함.**

### B. Product feed/API 주문중개

```text
YesStyle 상품·재고 피드
→ Premium MultiShop 상품 페이지
→ 고객 주문
→ YesStyle 또는 제3자 출고
```

필수 계약 확인:

- 공식 API 문서·인증 방식·호출제한
- 가격·재고·배송상태 실시간성
- 주문 생성·취소·부분취소·환불 API
- 한국 소비자 배송 가능 여부
- 상품 이미지·설명·리뷰 사용권
- 가격 재판매·마켓플레이스 판매 허용
- 반품 주소·반품비·환불주체
- 고객정보의 해외 이전·보관
- 품절·가격변동·API 오류 대응

**판정: API 문서·계약·샘플 주문 확인 전 검증 보류.**

### C. 도매·공급계약

```text
YesStyle 또는 관계 공급사
→ Premium MultiShop 공급가
→ Premium MultiShop 판매·CS·반품
```

필수 확인:

- 공급가와 최소주문수량
- 브랜드별 판매권·지역·채널 제한
- 정품·구매경로·상업송장
- 한국 화장품 수입·판매 요건
- 중국 판매·CBEC·일반무역 가능 여부
- 유통기한·로트·보관·리콜
- 반품·불량·고객 이상반응 책임
- 결제·환율·배송·통관 조건

**판정: 실제 공급계약과 완전원가 확인 후 3~5 SKU 테스트.**

## 3. 수익성이 낮아질 수 있는 이유

YesStyle은 이미 글로벌 소비자에게 직접 판매하며 가격·쿠폰·무료배송·프로모션을 운영하는 소매 플랫폼이다. Premium MultiShop이 같은 상품을 다시 판매하려면 다음 비용을 모두 부담할 수 있다.

```text
고객 판매가
- YesStyle 또는 공급처 실질 매입가
- 국제배송·통관·현지배송
- Cafe24·네이버·결제 수수료
- 환율·송금 수수료
- 할인·쿠폰
- 광고·콘텐츠 비용
- 고객상담
- 반품·환불·폐기 충당금
- 유통기한·재고손실
= 주문당 기여이익
```

공급가가 소비자 가격에 가까우면 API를 연결해도 수익이 생기지 않는다. 공개된 제휴 커미션 10%를 도매마진으로 오인하지 않는다.

## 4. Premium MultiShop 적합성

### 긍정적 측면

- 별도 선매입 없이 K-뷰티 수요를 테스트할 가능성
- 한국·중국·해외 고객 대상 콘텐츠 소재 확보
- 브랜드·성분·루틴 중심 SEO 콘텐츠 확장
- 화장품 롱테일 상품 수요 탐색

### 부정적 측면

- Premium MultiShop의 명품 패션 포지셔닝과 불일치 가능성
- 상품 수가 늘어도 가격·재구매·CRM이 YesStyle에 귀속될 수 있음
- 국내 화장품 판매와 중국 판매 규제가 별도 적용
- 정품·유통기한·로트·피부 이상반응·리콜 책임 불명확
- API 오류·품절·가격변동 시 고객 약속을 지키기 어려움
- BELLOON의 K-뷰티 사업과 데이터·손익이 섞일 위험

## 5. 권장 구조

### 1단계: 제휴 콘텐츠 테스트

- YesStyle 상품을 그대로 대량 등록하지 않음
- 대표님이 선정한 K-뷰티 루틴·문제해결 콘텐츠 5~10개 제작
- 제휴 링크로 수요·클릭·전환·커미션 측정
- Premium MultiShop 명품 고객과 BELLOON 후보 고객 데이터를 분리

### 2단계: 공급권 확인

YesStyle에 다음을 서면 문의한다.

1. Affiliate 외 공식 API가 있는가?
2. API가 제휴용인가, 주문·재고·상품등록용인가?
3. 도매·드랍쉬핑·재판매 계약이 가능한가?
4. 한국·중국 판매가 허용되는가?
5. 상품 이미지·상세설명·리뷰 재사용 권한은 무엇인가?
6. 한국·중국 배송과 반품 주소는 어디인가?
7. 유통기한·로트·정품·상업송장 자료를 받을 수 있는가?
8. 품절·가격변동·주문취소를 API로 통제할 수 있는가?
9. 고객 개인정보의 국외 이전·보관 범위는 무엇인가?
10. 최소주문·수수료·정산주기는 무엇인가?

### 3단계: 공식 공급계약이 확인될 때만 판매 테스트

- 3~5 SKU
- SKU당 1~2개 또는 무재고 주문형
- 14일 초기반응·30일 손익
- 한국 판매와 중국 판매 분리
- 상품별 완전원가 입력
- 반품·환불·유통기한·품절 기록
- Premium MultiShop과 BELLOON 손익을 별도 기록

## 6. 하드스탑

다음 중 하나라도 해당하면 API 개발·대량등록·광고를 중단한다.

- 공식 API 문서가 없음
- 도매·재판매 권한이 서면으로 확인되지 않음
- 공급가가 확정되지 않음
- 한국·중국 판매권이 불명확함
- 정품·상업송장·유통기한·로트 증빙 불가
- 반품·환불 주체 불명확
- API 재고가 실시간이 아니거나 품절 동기화 불가
- 순마진율 12% 미만
- 월 순이익 50만원 미만
- 데이터 신뢰도 0.70 미만
- 법적·규제 안전도 4/5 미만

## 최종 판정

- **Affiliate:** 콘텐츠 수익화용 제한 테스트 가능
- **공식 API 주문중개:** API·계약 확인 전 보류
- **도매 재판매:** 공급가·판매권·화장품 책임 확인 후 소량 테스트
- **Premium MultiShop 핵심사업 편입:** 현재 보류
- **BELLOON과의 관계:** K-뷰티 상품이면 별도 사업·SKU·손익·CRM으로 관리

## Sources

[1] YesStyle Affiliate Program: https://app.yesstyle.com/en/affiliate-program.html

[2] YesStyle 공식 홈페이지: https://www.yesstyle.com/

[3] YesStyle About Us: https://shop.yesstyle.com/en/about-us.html

*공개자료에서 API·도매공급권을 확인하지 못한 것이 API가 존재하지 않는다는 뜻은 아니다. 공식 파트너 문서·계약서·샘플 주문을 확인하기 전에는 검증 보류로 처리한다.*
