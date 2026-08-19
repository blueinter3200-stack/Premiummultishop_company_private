# Requirement Changelog

Repository: `https://github.com/jintonic1010/miracle_company_private`

이 문서는 모든 문구 수정이 아니라 **확정 요구사항의 추가·교체·삭제·중요한 의미 변경**만 기록합니다.

## 2026-08-19 — Initial Company OS Baseline

- `n8n`을 특정 부서가 아닌 회사 전체 연결·자동화 뼈대로 정의.
- ERP/재고·물류를 상품·SKU·재고뿐 아니라 주문·판매·고객·구매·배송·반품·공급처까지 포함하는 운영 Core로 정의.
- 카페24와 ERP의 IN/OUT 연결 방향을 확정.
- 네이버 스마트스토어와 ERP의 IN/OUT 연결 방향을 확정.
- Google 관련 API는 역할별 실제 기능을 조사한 뒤 ERP와 필요한 IN/OUT을 연결하는 방향으로 확정.
- 해외 공급처 API는 우선 ERP로 IN하는 방향을 확정.
- ERP ↔ 시장리서치, ERP ↔ 마케팅, ERP ↔ CS, ERP ↔ 세무·법률을 양방향 데이터 흐름으로 확정.
- 판매 과정에서 확보되는 고객/구매이력 데이터를 ERP/운영 데이터 계층에 연결하는 요구사항 추가.
- 관리자와 대표님 사용을 위해 아이디어/문제의 `저장`과 회사 공식 소스 `반영`을 분리하는 거버넌스 원칙 추가.
