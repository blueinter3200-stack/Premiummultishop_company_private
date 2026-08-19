# PRODUCT_REQUIREMENTS.md

- Canonical repository: `https://github.com/jintonic1010/miracle_company_private`
- Baseline date: 2026-08-19
- Authority: approved company-OS direction captured from administrator discussion

이 문서는 현재 확정된 회사 OS 요구사항의 기준입니다. 아이디어/문제 저장만으로 이 문서가 자동 변경되지는 않습니다.

## Company Core

### CORE-001 — n8n company backbone
Miracle Company OS의 전체 연결·자동화 뼈대는 n8n을 사용한다.

### CORE-002 — department model
회사는 최소 다음 부서 시스템을 가진다.
- ERP / 재고·물류
- 시장리서치
- 마케팅
- CS
- 세무·법률

### CORE-003 — ERP as operational core
ERP는 회사의 상품·SKU·재고·주문·판매·고객·구매·물류 운영 데이터의 핵심 원장 역할을 한다.

## ERP / Commerce Integration

### ERP-001 — open-source ERP choice
ERP 기반은 `ERPNext` 또는 `InvenTree` 중 하나를 사용한다. 최종 선택은 비교 후 확정한다.

### ERP-002 — Cafe24 integration
카페24와 ERP는 필요한 판매·상품·재고·주문·고객·물류 데이터를 실제 API 허용 범위 안에서 IN/OUT 연결한다.

### ERP-003 — Naver SmartStore integration
네이버 스마트스토어와 ERP는 필요한 판매·상품·재고·주문·고객·물류 데이터를 실제 API 허용 범위 안에서 IN/OUT 연결한다.

### ERP-004 — Google integration
Google Shopping/Merchant/Ads 등 관련 Google API는 역할별 실제 기능을 조사한 뒤 ERP와 필요한 IN/OUT 연결을 구성한다.

### ERP-005 — foreign supplier integration
해외 공급처 API에서 필요한 상품·SKU·가격·재고·공급 데이터를 ERP로 입력한다.

### ERP-006 — customer data
판매 과정에서 획득되는 고객·주문·구매이력 데이터는 법적·보안 경계 안에서 ERP/운영 데이터 계층에 연결한다.

### ERP-007 — logistics data
입고, 출고, 배송, 취소, 반품, 교환 및 공급처 관련 운영 상태를 ERP에서 추적할 수 있어야 한다.

## Department Data Exchange

### DEPT-001 — market research bidirectional flow
ERP와 시장리서치 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-002 — marketing bidirectional flow
ERP와 마케팅 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-003 — CS bidirectional flow
ERP와 CS 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-004 — tax/legal bidirectional flow
ERP와 세무·법률 부서는 필요한 데이터를 양방향으로 교환한다.

## Data And Integration

### DATA-001 — common identifiers
상품, SKU/옵션, 주문, 고객, 공급처 등 핵심 엔티티는 채널별 ID와 내부 기준 ID의 매핑 구조를 가져야 한다.

### DATA-002 — API contract before implementation
카페24, 네이버 스마트스토어, Google, 해외 공급처, ERP의 정확한 읽기/쓰기/Webhook/인증/rate-limit 범위를 조사한 API IN/OUT 명세를 구현 전에 만든다.

### DATA-003 — n8n is orchestration, not ERP ownership
n8n은 회사 전체 워크플로와 연결을 담당하지만 ERP 운영 데이터의 기준 원장을 대체하지 않는다.

### DATA-004 — runtime customer data stays out of GitHub
실제 고객 개인정보, 운영 DB, 인증정보와 런타임 원본 데이터는 이 GitHub 저장소에 저장하지 않는다.

## Governance

### GOV-001 — administrator authority
관리자는 회사 OS 기준 소스인 `COMPANY_OS.md`, `PRODUCT_REQUIREMENTS.md`, 부서/아키텍처 문서를 관리한다.

### GOV-002 — saved ideas are non-authoritative
저장된 아이디어는 관리자가 반영을 결정하기 전까지 공식 요구사항이 아니다.

### GOV-003 — saved problems are non-authoritative
저장된 문제는 관리자가 해결 방향과 반영을 결정하기 전까지 공식 요구사항을 자동 변경하지 않는다.

### GOV-004 — meaningful requirement history
확정 요구사항의 추가·교체·삭제·중요한 의미 변경은 `docs/requirement-changelog.md`에 기록한다.
