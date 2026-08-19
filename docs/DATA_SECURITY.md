# Data And Security Boundary

Repository: `https://github.com/jintonic1010/miracle_company_private`

## GitHub에 둘 수 있는 것

- 회사 OS 문서
- 요구사항과 변경 이력
- 부서 구조와 API 설계 문서
- DB schema 문서
- 비민감 샘플 데이터
- 아이디어/문제 요약

## GitHub에 두지 않는 것

- 고객 실명, 전화번호, 주소 등 원본 개인정보
- 실제 주문/결제 원본 데이터
- API key, token, password, `.env`
- SSH private key / 인증서 private key
- 운영 DB 원본
- 캐시, 인덱스, 로그, 브라우저 프로필
- Claude/ChatGPT 원시 대화 로그 중 민감정보가 포함될 수 있는 것

## ERP와 GitHub의 차이

고객·판매·주문 데이터가 회사 OS에 필요한 것은 맞지만, **실데이터 저장 위치는 ERP/운영 데이터 계층**이다. GitHub는 그 데이터의 구조·규칙·문서와 소스 관리에 사용한다.

## 기존 import 관련

과거 `_markdown/` 변환 import에는 인증/SSH/캐시/대화/시스템 상태 자료가 섞여 있었으므로 현재 정본 트리에서는 제거한다. Git history rewrite는 별도 고위험 작업이므로 이 정리 작업에서는 수행하지 않는다.
