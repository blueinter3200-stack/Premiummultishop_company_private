---
source_path: ".pi/사업계획서_텍스트모음/plans/pms-external-ai-agent-adoption-v1-2026-08-13.md"
source_filename: "pms-external-ai-agent-adoption-v1-2026-08-13.md"
source_type: "text"
source_size_bytes: 10749
source_modified_at: "2026-08-15T07:48:49+09:00"
source_sha256: "504a7d701b67a6568bbc2cec9c4bf336a411014f455e256607cc975a71f24162"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# PMS 외부 AI 에이전트 라이브러리 선별 도입 지침 v1.0

- 사업: Premium MultiShop
- 기준일: 2026-08-13
- 원본: `msitarzewski/agency-agents` 공개 라이브러리, MIT 라이선스 표기
- 판정: **제한 도입 3개 / 나머지 기본 도입 금지**
- 실투입: 2026-08-16 이후 검토. 2026-08-15 P1 카카오 CRM 검수 마감 보호.

## 1. 한 줄 결론

외부 에이전트는 PMS의 정본을 대체하지 않고, 기존 설계에서 비어 있는 방법론만 보완한다. 모든 외부 에이전트는 Premium MultiShop 하드스탑·승인 매트릭스·한국 법규·최신 대표 지시에 종속된다. 충돌 시 PMS 정본이 항상 우선이다.

## 2. 채택 에이전트

### A. Tracking & Measurement Specialist

- 보완 영역: GTM 컨테이너, GA4 이벤트 스키마, Meta Pixel/CAPI, `event_id` 중복 제거, 서버사이드 태깅, 채널별 전환 정합성.
- 연결: PMS Revenue SEO OS의 SEO 유입→주문→기여이익 측정, 채널별 매출·마진 귀속.
- 담당: 개발자 + 광고 담당. 실제 담당자 지정은 대표 결정 필요.
- PMS 오버라이드:
  1. 성과 판정은 ROAS가 아니라 광고비 포함 기여이익이다.
  2. 실결제 주문과 Purchase 이벤트가 ±10% 이내로 일치하기 전에는 연결 완료로 표시하지 않는다.
  3. 광고 예산·전환 최적화 변경은 대표 승인 후 실행한다.
  4. Cafe24·네이버·카카오 이벤트는 해당 채널의 실제 스펙 확인 전 추정하지 않는다.
- 중단: 2회 검증 후 Purchase 오차가 개선되지 않거나 주문·매출 귀속이 불가능하면 연결 확대를 중단한다.

### B. Pricing Analyst

- 보완 영역: 경쟁가 분석, 가격탄력성, 원가구조 분해, 할인 시나리오, 가치기반 가격 판단.
- 연결: PMS의 6종 가격 체계와 Profit Agent.
- 담당: 대표 + 온라인 MD. 실제 담당자 지정은 대표 결정 필요.
- PMS 오버라이드:
  1. 정상·목표·VIP·최소허용·재고회수·손실중단 가격을 동시에 산출한다.
  2. 최소허용가격 이하 할인은 대표 승인 없이 제안하지 않는다.
  3. 5% 초과 가격 인하는 대표의 명시 승인을 받는다.
  4. 경쟁사 최저가를 자동 추종하지 않는다.
  5. 순마진율 12% 미만, 회수기간 6개월 초과, 재고회전일 90일 초과 등 하드스탑을 유지한다.
  6. 원가·수수료·배송·반품·광고비가 없으면 `검증 불가`로 표시한다.
- 산출물: 상위 10개 SKU 6종 가격표와 ±20% 민감도 분석. 단, 실제 SKU 원가가 없으면 작성 보류.

### C. Email Marketing Strategist의 제한적 전환

- 원래 역할: 이메일 세그먼트·라이프사이클·측정·딜리버러빌리티 설계.
- PMS 적용: 이메일 발송 시스템을 도입하지 않고, 세그먼트 데이터 구조와 라이프사이클 원칙만 카카오 알림톡·친구톡 CRM에 치환한다.
- 연결: Customer Master, CRM Trigger Engine, 카카오 CRM P1.
- 담당: CRM 담당. 실제 담당자 지정은 대표 결정 필요.
- PMS 오버라이드:
  1. 이메일 대신 카카오 채널의 수신동의·야간발송·발송단가·템플릿·정책을 적용한다.
  2. 전체 고객 일괄 발송을 금지한다.
  3. 캠페인 필수 필드 12종과 한국 정보통신망법·개인정보보호 기준을 우선한다.
  4. 고객 발송은 승인 후 실행한다.
  5. HubSpot·Klaviyo·Zapier 등 외부 유료 도구는 채택하지 않는다.
  6. 이메일 오픈율 등 이메일 특화 KPI는 PMS 기본 KPI로 사용하지 않는다. 클릭·상담·구매·기여이익·재구매를 사용한다.
- 중단: P1 카카오 CRM 검수가 지연되거나 동의·수신거부·발송 이력 관리가 불가능하면 도입을 중단한다.

## 3. 도입 금지·보류 영역

- 개발·게임·GIS·XR·보안 등 PMS 범위와 무관한 에이전트
- 중국 플랫폼 전담 에이전트: 현재 중국 크로스보더 사업 동결 원칙에 따름
- Supply Chain Strategist: 중국 제조·1688·SAP/Oracle ERP 전제와 PMS의 유럽 부티크 병행수입 구조가 불일치
- Legal Compliance Checker: 미국 규제 기준을 한국 개인정보보호·광고성 정보 규정의 판단 근거로 사용하지 않음
- 외부 에이전트의 미국 CAN-SPAM·GDPR 기준을 한국 법률 판단으로 대체하지 않음
- 유료 SaaS·유료 플랜·API 종량과금이 필요한 도구: 대표의 명시 승인 전 도입 금지
- PMS 정본이 이미 있는 영역을 대체하는 에이전트: 기본 도입 금지

## 4. 적용 위치

```text
PMS Revenue SEO OS
  ├─ Tracking Agent: SEO 유입·Purchase·기여이익 귀속 검증
  ├─ Pricing Agent: 6종 가격·민감도·할인 하드스탑 보완
  └─ CRM Segment Agent: 카카오 고객 세그먼트·라이프사이클 보완
```

외부 에이전트는 Trend Agent·Keyword Agent·Sourcing Agent·Profit Agent·Decision Engine·Content Agent의 정본이 아니다. 해당 역할을 확장할 때도 PMS Product Master·Inventory Master·Rule Engine·승인 로그를 통과해야 한다.

## 5. 실행 테이블

| 우선 | 액션 | 담당 | 마감 | 예상비용 | KPI | 중단 조건 | 상태 |
|---:|---|---|---|---:|---|---|---|
| 0 | 2026-08-15까지 외부 에이전트 실투입 0시간으로 P1 카카오 CRM 마감 보호 | 대표 | 2026-08-15 | 0원 | P1 검수조건 통과 | 1시간이라도 선투입 시 동결 | 대기 |
| 1 | 본 문서를 PMS 프로젝트 지식으로 연결 | 대표 | 2026-08-16 | 0원 | 연결 확인 | 링크 미확인 시 보류 | 기록 완료 |
| 2 | Tracking 에이전트로 GA4·Meta CAPI 이벤트 스키마 초안 1건 | 개발자 + 광고 담당 | 2026-08-24 | 0원 | 실주문 대비 Purchase 오차 ±10% 이내 | 2회 시도 후 개선 없음 | 검토 대기 |
| 3 | Pricing 에이전트로 상위 10개 SKU 6종 가격표 | 대표 + 온라인 MD | 2026-08-28 | 0원 | 최소허용가 산출 완료 | 원가 데이터 미확보 | 검토 대기 |
| 4 | CRM 세그먼트 속성·라이프사이클 설계표 | CRM 담당 | 2026-08-28 | 0원 | 세그먼트 11종 문서화 | P1 검수 지연 | 검토 대기 |
| 5 | 도입 효과 판정 | 대표 | 2026-09-04 | 0원 | 3건 중 2건 이상 실무 채택 | 1건 이하이면 전면 폐기 | 예정 |

마감은 대표 승인·실제 담당자 지정 전까지 실행 확정이 아니다.

## 6. 외부 에이전트 공통 안전규칙

- 매출이 아니라 순이익·기여이익으로 판단한다.
- 데이터가 없으면 숫자를 만들지 않고 `검증 불가`로 표시한다.
- 담당·절대 마감·KPI·중단조건 없는 제안은 실행안으로 채택하지 않는다.
- 고객·상품·가격·재고·주문·환불·광고예산을 외부 에이전트가 직접 변경하지 못한다.
- 고객 발송·계약·결제·유료 도구 사용은 대표 승인 없이 실행하지 않는다.
- 외부 에이전트 출력은 원문 출처·적용 범위·PMS 오버라이드·검토자를 기록한다.
- MIT 라이선스 원문을 재사용·재배포할 경우 원저작권·라이선스 고지를 보존한다. 실제 저작권 표기는 원 저장소의 LICENSE 원문으로 재확인한다.

## 7. 효과 판정

2026-09-04에 다음을 확인한다.

- 산출물 3건의 실무 채택 여부
- GA4·Meta 이벤트와 실결제 주문의 정합성
- 상위 10개 SKU의 6종 가격표 완성 여부
- 카카오 CRM 세그먼트의 동의·중복·수신거부 처리 가능 여부
- PMS 하드스탑 위반 발생 여부
- 외부 에이전트가 기존 정본과 충돌했는지

3개 중 2개 미만이 실무에 채택되면 외부 에이전트 도입을 전면 폐기한다.

## 관련 문서

- [[plans/pms-automation-platform-v1-2026-08-13|PMS Automation Platform v1.0]]
- [[plans/pms-automation-platform-v1-2026-08-13#1.2-pms-revenue-seo-os|PMS Revenue SEO OS]]
- [[04-decision-log|의사결정 로그]]
- [[07-project-tracker|실행 추적]]


## 8. Claude for Small Business 링크 검증 결과 (2026-08-14)

### 확인된 내용

사용자가 제공한 Notion 문서는 **「자영업·1인 사업을 위한 클로드 스킬 31개 완전 정리」**이며, Claude Cowork용 Small Business 플러그인의 설치·사용 흐름을 설명한다.

Anthropic 공식 페이지와 대조한 결과 다음은 확인된다.

- Small Business 플러그인은 Claude Cowork에서 사용하는 공식 제품이다.
- 데스크톱 앱에서 사용하며, `/smb-onboard`로 사업 맥락을 설정하는 흐름이 안내된다.
- 공식 안내의 대표 연결 서비스는 QuickBooks·PayPal·HubSpot이며, Canva·DocuSign·Gmail/Outlook·Slack·Stripe·Square 등을 추가할 수 있다.
- 주요 기능 범위는 현금흐름·영업·고객응대·마케팅·보고·계약 검토 등이다.

### PMS 적용 판정

**제품의 실재성: 확인됨 / PMS 직접 도입: 보류**

이 플러그인은 외부 AI 에이전트 선별 도입 지침의 검토 대상이 될 수 있지만, 다음 이유로 PMS의 운영 코어를 대체하지 않는다.

- Cafe24·카카오 알림톡/친구톡·Meta·POS·ERP·Realpacking 연결은 공식 페이지에서 확인되지 않았다.
- 해외 회계·결제·CRM 서비스 중심이며, Premium MultiShop의 국내 커머스·병행수입·정품·DDP·재고 운영에 특화되지 않았다.
- `/smb-onboard` 결과가 PMS의 Customer/Product/Inventory/Order Master가 되지 않는다.
- 계약서·현금흐름·고객응대 초안은 보조할 수 있지만, 가격·재고·환불·주문·고객 병합을 직접 실행하게 두지 않는다.
- Claude 유료 플랜과 데스크톱 앱 사용이 필요하므로 대표의 기존 원칙인 무승인 유료 플랜·종량과금 제외에 걸린다.

### 제한적 활용 후보

PMS 정본을 대체하지 않는 비실행형 보조 업무만 후보로 둔다.

- 주간 사업 브리핑 초안
- 현금흐름 자료 요약
- 계약서 위험 조항 후보 표시 후 법률 검토 전달
- 콘텐츠 아이디어와 초안 생성
- 고객 불만 응대 초안

### 사용 금지 범위

- Cafe24 주문·재고·가격 직접 변경
- 카카오 대량 발송
- 환불·고객 병합·공급처 발주
- 계약 승인·법률 판단 확정
- PMS의 공식 손익·재고 원장으로 사용
- 외부 유료 플랜 또는 서비스 연결 무승인 실행

### 공식 출처

- Anthropic Small Business: https://www.anthropic.com/news/claude-for-small-business
- Claude 공식 플러그인: https://claude.com/plugins/small-business
- Claude 설치·사용 안내: https://claude.com/resources/tutorials/how-to-install-the-claude-for-small-business-plugin
