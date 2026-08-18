---
source_path: ".pi/사업계획서_텍스트모음/research/premium-multishop-sourcing-landscape-2026-08-13.md"
source_filename: "premium-multishop-sourcing-landscape-2026-08-13.md"
source_type: "text"
source_size_bytes: 17249
source_modified_at: "2026-08-13T15:47:45+09:00"
source_sha256: "472721907cc81b1d093604b2764c8fa7f509eca7d697e5539670ec6a069c0d31"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# Premium MultiShop 해외 B2B 명품·패션 공급망 후보군 조사

- **대상:** Premium MultiShop만 해당. BELLOON 화장품 사업은 제외.
- **조사일:** 2026-08-13 (UTC 기준 시스템 날짜)
- **목적:** 정품·인보이스·가격 경쟁력·DDP·실시간 재고/가격 연동·한국 배송 가능성을 검증할 수 있는 공개 후보군과 검증 파이프라인 설계
- **주의:** 아래는 공개 페이지/검색 결과에 기반한 후보 발굴이다. 업체 추천 확정, 계약, 구매, 연락을 수행하지 않았다. 공개 정보만으로 정품의 법적 보증, 한국 통관 성공, DDP 비용, 실제 공급가·재고를 확정할 수 없다.

## 1. 한 줄 결론

**실행이 아니라 검증 보류:** 후보는 충분하지만, 한국행 DDP·브랜드별 유통권한·상업 인보이스·실시간 재고/API·반품 책임을 한 업체의 공개 정보만으로 모두 충족하는 후보는 확인되지 않았다. 우선순위는 `유럽 B2B 정품/병행재고 플랫폼`과 `일본 pre-owned B2B`를 분리해 소량 샘플·서류·운송 견적으로 검증하는 것이다.

## 2. 후보군 구조

### A. 신품 디자이너 패션 도매·드롭쉬핑

| 후보/권역·유형 | 공개 브랜드 범위 | 정품·인보이스 | 반품·배송 | API/피드 | DDP·한국 배송 | 현재 판단 |
|---|---|---|---|---|---|---|
| **BrandsGateway (EU/글로벌)** — 신품 럭셔리 도매·드롭쉬핑 | 사이트가 디자이너 브랜드 의류·액세서리를 표방하나, 한국 판매용 전체 브랜드 목록·브랜드별 공급 경로는 별도 확인 필요.[1] | 100% authentic FAQ를 공개적으로 제시하지만, SKU별 원산지·구매증빙·상업 invoice 샘플은 미확인.[3] | DHL/FedEx/UPS, 전세계 배송, 공개 배송기간 2–10일.[1][3] 반품은 사유에 따라 자체/공급자 라벨 선택 가능.[4] | Shopify/WooCommerce 연동을 표방하고 WooCommerce API keys 요청 경로가 공개됨.[1][5] 실시간 재고·가격 SLA/웹훅은 미확인. | 기본은 **DAP**이며 대부분 국가에서 관세·세금은 수입자 부담. DDP는 일부 국가만 가능하다고 공개.[6] 한국이 DDP 대상인지 미확인. 국제 배송 자체는 가능성 높으나 한국 checkout 테스트 필요. | API와 국제 배송은 유력한 검증 후보이나, 한국 DDP·증빙을 우선 확인.
| **Brandsdistribution / BDroppy (EU/글로벌)** — 도매·드롭쉬핑 | 공개 FAQ 검색 결과 기준 120+ 디자이너 브랜드, 170개국, 1M+ 리테일러를 표방.[7] 브랜드별 한국 판매 가능·재고는 미확인. | branded fashion 유통 플랫폼을 표방하나 정품 보증 문구, SKU별 invoice/공급망 증빙은 미확인.[7] | DHL/FedEx/Boxberry 국제 배송, 170개국 배송 표방.[8] 배송비에 VAT 포함 여부·반품 비용은 주문/목적지별 확인 필요. | XLS/CSV/XML 카탈로그 export와 API 개발자 문서가 공개되어 있음.[9][10] API의 실시간성·재고 예약·가격 업데이트 주기는 미확인. | 한국 배송 가능 여부는 170개국 문구만으로 확정 불가. DDP·한국 관세 납부 주체는 미확인. | API/피드 후보. DDP와 invoice/정품 서류를 gate로 둔다.
| **GRIFFATI (이탈리아/EU)** — 신품 디자이너 의류 도매·드롭쉬핑 | 여성·남성·아동 의류, 신발, 액세서리, 핸드백 및 이탈리아/주요 브랜드를 공개.[11] 전체 브랜드·한국 판매권은 미확인. | B2B 디자이너 도매를 표방하지만 정품 보증·브랜드별 invoice 샘플은 미확인. | 드롭쉬핑 계약상 고객 불만 반품 15일 규정이 공개 검색 결과에 있음.[12] 한국 배송·반품 회수비·통관은 미확인. | API로 카탈로그 연동 및 판매 전송을 표방.[12] 재고/가격 실시간 SLA는 미확인. | DDP·한국 배송 모두 미확인. | API는 유력하나 한국향 운영조건이 비어 있어 서류 확인 전 보류.

### B. pre-owned 명품 B2B 마켓플레이스·경매

| 후보/권역·유형 | 공개 브랜드·정품 범위 | 인보이스·반품 | 배송·관세 | API/피드 | 한국 가능성·판정 |
|---|---|---|---|---|---|
| **LePrix (미국/프랑스 네트워크)** — 인증 중고 명품 B2B | 월 180,000+ authenticated pre-owned items 및 vetted suppliers/auction houses를 표방.[13] 브랜드별 재고는 회원/로그인 후 확인 필요. | pre-authenticated·authenticity policy·COA 경로 공개.[14] COA가 별도 구매일 수 있고, invoice 샘플·한국 판매용 서류는 미확인. 경매 교환에는 10% restocking fee 사례가 공개.[15] | 미국/프랑스 창고 출고 shipping이 invoice에 추가될 수 있음.[16] 미국·EU·캐나다 외 구매자는 수입세·관세를 전액 부담한다고 공개 검색 결과에 표시.[17] | 공개 API/재고 feed는 확인되지 않음. | 한국 배송 자체, DDP, 한국 반품은 미확인. 인증 중고는 신품과 별도 카테고리·상태등급/COA 검수 필요. |
| **The Brand Collector (프랑스/EU)** — authenticated luxury B2B | 30,000+ authenticated luxury items, Hermès·Chanel·Louis Vuitton 등을 공개.[18] | authenticated 표방. 상품별 감정/상태·구매 invoice 제공 범위는 미확인. | 전세계 배송, €1,000 이상 무료 배송 표방. 국제 주문은 DAP이며 관세·세금·통관비가 포함되지 않음.[19] 반품 조건·한국 회수비는 미확인. | 공개 API/실시간 feed는 미확인. | 한국 배송은 전세계 배송 문구상 가능성이 있으나, DDP는 아님. 비용 사전 견적과 한국 반품 주소를 확인해야 함. |
| **BrandLuxJP (일본)** — B2B luxury auction/도매 | 가방·시계·주얼리·액세서리 등 B2B 경매를 표방.[20] 브랜드별 진위 기준·상태 등급은 상품/회원 화면 확인 필요. | bulk order reserve invoice 발급 절차를 공개.[20] 정품 보증서·감정 리포트·일반 commercial invoice 여부는 미확인. | 글로벌 shipment, 배송 계산기·통관 정보·tracking 도구를 표방하며 통상 7–15영업일.[21] | 공개 API/feed 미확인. | 한국 배송 가능성은 글로벌 dealer portal로 확인할 후보이나 DDP·관세 납부 주체는 미확인. |
| **Jolijou Wholesale (일본)** — pre-owned 명품 핸드백 B2B | 일본 pre-owned handbags, wallets, accessories; authenticated, no minimums, worldwide shipping을 표방.[22] | 인증·B2B 도매를 표방하지만 감정 기준, invoice/COA 샘플, 브랜드별 공급망은 미확인. | worldwide shipping 문구만 확인; 한국 운송사·반품·관세·DDP는 미확인. | API/feed 미확인. | 소량 테스트 후보지만 한국행 DDP·서류 gate 미충족.

### C. 일본 종합 도매 플랫폼·공급자 디렉터리

| 후보/권역·유형 | 공개 정보 | 한국·통관·연동 | 판정 |
|---|---|---|---|
| **SUPER DELIVERY (일본)** — 자격 심사 일본 공급자 도매 플랫폼 | qualified Japanese vendors, 해외 구매자용 패션/상품 카탈로그를 공개.[23] 명품 브랜드의 진품 보증은 플랫폼 공통으로 확정할 수 없고 판매자별 확인 필요. | 한국 배송 옵션으로 ECMS·Pantos가 명시됨.[24] 공개 안내는 수입 통관·관세를 구매자가 부담하는 구조(CIF 예시 포함)를 설명하므로 DDP로 보지 않음.[25] | API/실시간 가격·재고 feed 미확인. 판매자별 브랜드·invoice·반품을 개별 검증해야 함. 명품보다는 일본 브랜드/셀렉트 패션 소싱에 적합할 수 있으나 확정 추천 아님.
| **NETSEA (일본)** — 일본 도매·공급자 마켓플레이스 | 제조사·도매회사·공급자가 도매가격과 상품정보를 게재하는 일본 B2B 사이트.[26] | 해외 배송, 정품, commercial invoice, API, DDP, 한국 배송은 플랫폼 공통으로 미확인. | 판매자 단위 due diligence가 필수인 탐색용 후보. |

### D. 직접 브랜드 도매 주문·B2B SaaS 마켓플레이스 (공급업체라기보다 접근 인프라)

| 후보 | 공개 범위/기능 | Premium MultiShop 적용상 미확인 사항 |
|---|---|---|
| **JOOR (글로벌 B2B SaaS/marketplace)** | 브랜드와 리테일러를 연결·주문관리하는 B2B 플랫폼, 14,000+ 브랜드·700,000+ 구매자를 표방.[27] | 특정 명품 브랜드가 한국 사업자에게 도매 계정을 열어주는지, 공급가·MOQ·한국 수출·invoice·DDP·재고 API는 브랜드별 미확인. 플랫폼이 물류/정품 보증을 대신한다는 근거 없음.
| **NuORDER by Lightspeed (글로벌 B2B SaaS)** | 120+ ERP/PLM/POS 연동, API·FTP, 상품·재고·주문 데이터를 한 곳에서 관리한다고 공개.[27] | 주로 브랜드/리테일러 wholesale workflow 인프라다. 한국 배송·DDP·정품은 각 브랜드/3PL 계약의 문제이며, 공급처로 직접 간주하면 안 됨.
| **Flence (유럽 B2B fashion marketplace)** | 유럽·그 외 지역 브랜드의 디지털 쇼룸, line sheet, wholesale order를 표방.[28] | 명품 정품 보증, 한국 배송, 관세·DDP, API/feed, invoice는 미확인. 신진/셀렉트 패션과 럭셔리 병행수입 후보를 분리해야 함.

## 3. 요구조건별 공개 확인 현황

| 요구조건 | 공개조사 결과 | 운영상 의미 |
|---|---|---|
| 정품 보증 | BrandsGateway, LePrix, The Brand Collector, Jolijou 등은 authentic/authenticated를 표방하지만, 표현 자체가 브랜드별 유통권한·한국에서의 증거력까지 보장하지 않음.[3][13][18][22] | 샘플 SKU마다 원 구매처, serial/tag, 상태사진, 감정/COA, supplier invoice를 받아 내부 검수.
| 상업 invoice | BrandLuxJP는 reserve invoice 절차를 공개하고 LePrix는 COA 관련 invoice 경로를 공개하지만, 이것이 한국 통관용 commercial invoice·실제 결제자/수출자 정보와 같은지는 미확인.[14][20] | Proforma가 아닌 commercial invoice, HS code, 원산지, 거래조건, 수출자/수입자 명의를 서면 확인.
| 한국 배송 | BrandsGateway/Brandsdistribution는 글로벌 또는 다국가 배송을, SUPER DELIVERY는 한국 운송 옵션을 공개.[1][8][24] | 한국 주소 checkout/배송료/운송사/통관 연락처까지 실제 테스트 전에는 확정 금지.
| DDP | BrandsGateway는 기본 DAP, 일부 국가만 DDP라고 공개.[6] The Brand Collector는 국제 DAP.[19] SUPER DELIVERY는 구매자 통관·관세 부담 구조.[25] | 한국 DDP 후보로 표시할 업체는 현재 없음. `DDP 가능`과 `한국 DDP 견적 발행`을 분리.
| API/feed | BrandsGateway WooCommerce API, Brandsdistribution XML/API, GRIFFATI API가 공개.[5][9][10][12] | 공개 API가 있어도 한국 판매가능 SKU 필터·재고예약·가격/환율·주문취소·반품 feed가 되는지 별도 기술 검증.
| 반품 | BrandsGateway 반품 라벨 선택, GRIFFATI 15일, LePrix 경매 restocking fee 등 일부 공개.[4][12][15] | 국제 반품은 고객 변심/하자/진위 분쟁별 비용부담과 회수 주소를 계약서로 확정.

## 4. 검증 파이프라인 (추천 확정 전 필수)

### Gate 0 — 공급망 유형과 SKU 경계
1. 신품 도매/드롭쉬핑, pre-owned 인증품, 일본 셀렉트 도매를 별도 pool로 관리한다.
2. 브랜드·모델·시즌·색상·사이즈·상태·구성품 단위로 SKU를 고정한다.
3. 플랫폼 마케팅 문구는 `공개 주장`, 실제 서류는 `검증된 사실`로 분리한다.

### Gate 1 — 법인·거래상대·정품
- 법인 등록, VAT/EORI 또는 수출자 정보, 실제 출고 법인, 결제 수취 법인을 확인.
- 최근 샘플 3–5 SKU에 대해 supplier invoice/매입증빙, serial/tag, 구성품, 상태 등급, COA/감정 프로토콜을 확보.
- 브랜드별로 병행수입·상표·재판매 제한과 한국 플랫폼(KREAM/네이버 등) 증빙 수용 여부를 법률/플랫폼 정책으로 확인.
- 미제출·이미지 워터마크만 제공·invoice 명의 불일치는 즉시 보류.

### Gate 2 — 한국행 DDP·통관
- 동일 SKU/수량에 대해 `DAP`와 `DDP` 각각 견적을 받고 Incoterms 2020, 관세·부가세·통관수수료·disbursement fee·반송 비용 포함 여부를 문서화.
- 한국 수입자 명의, HS code, 원산지, 과세가격, 수출자/운송사, 관세납부 주체를 확정.
- 배송 시뮬레이션: 한국 사업자 주소로 샘플 1건, 운송장/통관서류/최종 landed cost를 기록. 샘플 구매 전에는 계약·결제하지 않는다.

### Gate 3 — 반품·품질·진위 분쟁
- 고객 변심, 사이즈, 하자, 오배송, 진품 분쟁을 분리해 RMA SLA와 비용 부담을 표로 받는다.
- 반품 주소가 한국인지 해외인지, 국제 왕복 운임·관세 환급·재입고/감정비 부담 주체를 확인.
- pre-owned는 상태등급·사진·냄새/수선/부속품 기준과 감정 이의제기 절차를 추가.

### Gate 4 — API/피드 기술검증
- 인증 방식, API rate limit, SKU/variant ID, 재고 예약/hold, 가격·통화·VAT, 이미지 사용권, webhook/폴링 주기, 주문·취소·반품 endpoint를 문서로 수령.
- 50개 이하 시험 SKU로 Cafe24/자체 middleware에 sandbox 또는 read-only feed 연결.
- 실제 테스트: 품절 반영시간, 가격 변경, 중복 주문, 부분출고, tracking, 반품 status, 장애 알림.
- API가 없는 후보는 CSV/XLS 수동 검증 pool로 분리하고 실시간 판매 약속을 하지 않는다.

### Gate 5 — 단위경제와 소량 테스트
- `매입가 + 국제운임 + 보험 + 관세/부가세 + 통관수수료 + DDP fee + 결제/환전 + 국내배송 + 플랫폼 수수료 + 반품충당`으로 landed cost를 계산.
- Premium MultiShop 하드스톱 적용: 순마진율 12% 미만, 리드타임 45일 초과, 재고회전 90일 초과, 정품·통관·A/S 입증 불가 시 진입 금지/검증 보류.
- 신규 공급사는 SKU 5개 이하 또는 총투자 300만원 이하의 14일 테스트만 허용(대표 승인 전제). D+7/D+14/D+30에서 판매·반품·실제 통관·기여이익을 재평가.

## 5. 후보 평가용 데이터 시트 필드

`공급사명 | 국가/출고창고 | 유형 | 브랜드/SKU | 신품/pre-owned | 상태/구성품 | 정품증빙 | invoice 샘플 | MOQ | 매입가/통화 | 재고 feed 주기 | API 문서 | 한국 배송 | DAP/DDP | 관세/부가세 포함 | 리드타임 | 반품 주소/비용 | 샘플 통관 결과 | landed cost | 목표 판매가 | 기여이익 | 증거 URL | 조사일 | 미확인/다음 확인`

## 6. 다음 검증 우선순위 (추천이 아닌 조사 순서)

1. **BrandsGateway / Brandsdistribution / GRIFFATI:** 공개 API·국제 배송 후보이므로 한국행 DDP 가능 여부와 SKU별 invoice·정품증빙을 먼저 서면 확인.
2. **The Brand Collector / LePrix / BrandLuxJP / Jolijou:** 인증 중고 pool로 분리하고 COA·상태등급·반품·한국 통관을 소량 샘플로 검증.
3. **SUPER DELIVERY / NETSEA / JOOR / NuORDER / Flence:** 공급사 직접 후보와 연결 인프라를 혼동하지 말고, 판매자/브랜드 단위로 한국 수출과 서류를 확인.

## 7. 제한사항

- 사이트 일부는 로그인/회원 전용이라 실제 브랜드별 가격·재고·거래조건을 열람하지 못했다.
- `web_extract` 백엔드가 현재 검색 전용으로 설정되어 공식 페이지 본문 자동 추출이 실패했다. 따라서 일부 항목은 공식 검색 결과에 노출된 문구와 공개 페이지 URL을 근거로 삼았고, 반드시 업체 서류/샘플로 재검증해야 한다.
- DDP는 상품 페이지의 국제배송 문구와 다르다. 본 조사에서는 한국 DDP 견적·통관 완료를 확인한 업체가 없으므로 모두 `미확인` 또는 `DAP`로 표시했다.

## Sources

[1] https://brandsgateway.com
[2] https://brandsgateway.com/shipping-and-returns
[3] https://brandsgateway.com/intro-video
[4] https://helpdesk.brandsgateway.com/en/article/how-to-request-a-return-55z1wx
[5] https://brandsgateway.com
[6] https://brandsgateway.com/terms-conditions
[7] https://faq.brandsdistribution.com
[8] https://support.brandsdistribution.com/en-us/article/50-which-countries-do-you-ship-to-and-how-much-does-shipping-cost
[9] https://www.brandsdistribution.com/de/cms/dropshipping-guide
[10] https://www.brandsdistribution.com/it/cms/api-per-programmatori
[11] https://www.griffati.com/en
[12] https://www.griffati.com/en/dropshipping.html
[13] https://leprix.com/en
[14] https://leprix.com/en/help
[15] https://leprix.com/en/question/13
[16] https://leprix.com/en/question/37
[17] https://leprix.com/en/f9bb044f-d11d-44ac-51-c75583a6436e
[18] https://wholesale.thebrandcollector.com
[19] https://wholesale.thebrandcollector.com/faq
[20] https://brandluxjp.com/wholesale-b-to-b
[21] https://brandluxjp.com/Shipping-estimation
[22] https://lp.jolijou-jp.com
[23] https://www.superdelivery.com/en
[24] https://www.superdelivery.com/en/entry/mail.do?lang=en
[25] https://findjapan.superdelivery.com/import-export/18026.html
[26] https://www.netsea.jp
[26] https://www.joor.com
[27] https://www.nuorder.com
[28] https://flence.com/for-brands
