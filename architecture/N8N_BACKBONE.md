# n8n Company Backbone

## 정의

n8n은 Miracle Company OS의 전체 뼈대다. ERP 앞에 붙는 단순 중계기 한 개가 아니라 부서, 외부 API, AI 에이전트, 반복 업무를 연결하는 전사 오케스트레이션 계층이다.

## 담당

- API 호출과 Webhook 처리
- 부서 간 워크플로 연결
- 일정/이벤트 기반 자동화
- 데이터 변환과 라우팅
- 실패 재시도와 알림
- AI 에이전트 호출
- 필요한 경우 사내 custom node 사용

## 비담당

- ERP의 상품/재고/주문/고객 운영 원장 역할을 대체하지 않는다.
- 모든 회사 원문 문서를 n8n 내부에 저장하지 않는다.

## 개발 경계

통합/n8n 개발자는 API 연결, workflow, custom node, webhook, 인증과 변환을 담당하고, ERP 개발자는 ERP 데이터 모델과 재고/주문/고객/물류 운영을 담당한다. 두 개발자는 공통 ID와 ERP API 계약에서 만난다.
