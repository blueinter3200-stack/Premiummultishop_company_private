# Current State

- Repository: `https://github.com/jintonic1010/miracle_company_private`
- Updated: 2026-08-19

## 확정된 것

- n8n = 회사 전체 OS 뼈대
- 핵심 부서 = ERP/재고·물류, 시장리서치, 마케팅, CS, 세무·법률
- ERP = 회사 운영 데이터 Core
- 카페24 ↔ ERP
- 네이버 스마트스토어 ↔ ERP
- Google 관련 채널 ↔ ERP (정확한 API 역할은 조사 필요)
- 해외 공급처 API → ERP
- ERP와 각 주요 부서는 필요한 데이터를 양방향 교환
- 고객·주문·구매이력 데이터도 ERP/운영 계층에 포함

## 아직 결정하지 않은 것

- ERPNext vs InvenTree 최종 선택
- 각 외부 API의 정확한 endpoint/권한/Webhook/rate-limit 범위
- 내부 canonical SKU/product/customer/order ID 규격
- 실제 전사 분석 DB/데이터 레이크 선택

## 다음 작업

1. ERPNext vs InvenTree 비교
2. Cafe24/Naver/Google/foreign supplier API IN/OUT matrix 조사
3. ERP ↔ n8n 데이터 계약 정의
4. 대표님 보고용 회사 OS 아키텍처 정리
