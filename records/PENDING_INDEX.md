# Pending Idea / Problem Index

- Updated: 2026-09-09
- Release: GOV-20260906-02
- 기준: main의 실제 status=saved 아이디어 7건·문제 2건 대조
- 용도: 관련 기록을 선택하기 위한 경량 인덱스; 업무 배정·공식 반영 목록이 아님

일반 검토에서는 관련 제목·요약·키워드로 필요한 원문과 정제본만 읽는다. 기록과 인덱스는 함께 저장하며 관리자 공식 채택 없이 항목을 제거하거나 reflected로 바꾸지 않는다.

형식: `record_id | 제목 | actor_id | role | 날짜 | keywords | path`

## Ideas

- I-20260819-001 | 트렌드 검증형 AI 쇼핑쇼츠 자동 생산 시스템 | ACT-001 | admin | 2026-08-19 | keywords: 쇼츠, 광고소재, 실험, 성과 환류 | path: `records/ideas/admin/2026-08-19-ai-shopping-shorts-test-engine.md`
  - summary: 상품 데이터·타깃·다양한 광고소재·검수·성과 환류를 연결하는 실험 엔진 제안. 3상품×10소재는 계획 예시이지 실적이 아니다.
- I-20260819-002 | PMS 자사몰 코어 구축·자동화 개발 운영안 | ACT-002 | representative | 2026-08-19 | keywords: 데이터 파이프라인, Customer Master, 코어 개발, DoD | path: `records/ideas/representative/2026-08-19-pms-core-automation-development-plan.md`
  - summary: 데이터·측정 복구부터 핵심 원장·운영 자동화·CRM·AI로 진행하는 개발 순서 제안. 일정·비용은 원문 제안이며 원본 DOCX는 저장소 미확보.
- I-20260820-001 | PMS Sourcing OS — Evidence-to-Revenue Buying Desk | ACT-001 | admin | 2026-08-20 | keywords: sourcing, buying, SKU, 증거, CM1, CM2, Cafe24, READY, RARE, CARE | path: `records/ideas/admin/2026-08-20-pms-sourcing-os.md`
  - summary: 상품 URL부터 동일 SKU·공급처·권리·수익·승인·임시등록·CARE 환류를 연결하는 바잉 OS 제안. 자동 결제·발주·공개 등의 금지를 포함.
- I-20260831-001 | 업무 설명 시 약어·전문용어 쉬운 풀이 원칙 | ACT-002 | representative | 2026-08-31 | keywords: 업무설명, 약어, 쉬운풀이 | path: `records/ideas/representative/2026-08-31-explain-acronyms-and-technical-terms.md`
  - summary: 영문 약어·전문용어에 한국어 뜻과 쉬운 설명을 붙이는 제안. 기록 자체는 미반영 상태 유지.
- I-20260831-002 | PMS Meta 광고 Creative Factory — 승자 소재 반복 생산 구조 | ACT-002 | representative | 2026-08-31 | keywords: Meta 광고, 콘텐츠 실험, 기여이익 | path: `records/ideas/representative/2026-08-31-pms-meta-creative-factory.md`
  - summary: 고객 문제·광고소재·한 변수 테스트·성과 판정·변형 확대를 반복하는 제안. 실제 집행·전환·성과는 확인되지 않음.
- I-20260905-001 | 프리미엄멀티샵 Revenue OS v7.0 — Codex 상시 작업 규칙 | ACT-002 | representative | 2026-09-05 | keywords: Codex, AGENTS.md, 하드스탑, 승인 | path: `records/ideas/representative/2026-09-05-codex-revenue-os-v7-agents-rules.md`
  - summary: 데이터·계산·위험 중단·승인·노트·보고 규칙 제안. 수치 기준과 스크립트·명령 구현은 미확정/미검증.
- I-20260909-001 | 상품 수익 운영 책임자 — 상품을 현금이익으로 전환하는 전 과정 책임자 | ACT-002 | representative | 2026-09-09 | keywords: 상품 수익 운영, 기여이익, 재고회전, 현금회수, CRM, AI 자동화 | path: `records/ideas/ACT-002/2026-09-09-product-revenue-operator.md`
  - summary: 팔릴 상품 발견부터 가격·채널 노출·광고/CRM·재고 회수·기여이익 확인까지 전 과정을 책임지는 역할 제안. 성과는 매출 단독보다 기여이익·재고회전·현금회수 속도를 중심으로 보고, 직접 모든 일을 하는 인재보다 AI·자동화·협업을 지휘하는 역할로 정의한다. 직무명·권한·성과 수치·채용조건은 미확정이다.

## Problems

- P-20260908-001 | Meta 픽셀 외부 자산 연결·계정 침해 의심 보안 이슈 | ACT-002 | representative | 2026-09-08 | keywords: Meta, Meta Pixel, 광고계정, 보안, 외부 데이터 세트, 계정 침해 의심 | path: `records/problems/ACT-002/2026-09-08-meta-pixel-security-incident-suspected.md`
  - summary: 대표님 제공 자료를 근거로 CĐ-HN/Z799 등 외부 자산 연결 및 권한 위험 정황을 문제로 저장. 계정 탈취·무단 광고비 사용은 독립 검증되지 않았으며, 회사 광고계정 식별·권한·지출·연결 경로 확인이 필요함.
- P-20260908-002 | 이미지 생성 시 텍스트 라인·의류 주름·명암 대비 품질 문제 | ACT-003 | assistant | 2026-09-08 | keywords: 이미지 생성, 텍스트 라인, 타이포그래피, 의류 주름, 명암 대비, 화보 현실감 | path: `records/problems/ACT-003/2026-09-08-image-generation-text-folds-contrast-quality.md`
  - summary: 이미지 생성 시 텍스트 라인이 어색하고 의류 주름·명암 대비가 부족하다는 품질 문제를 저장. 구체 원인은 미확인으로, 타이포그래피 제약·원단 물리 묘사·조명 조건을 비교 확인할 필요가 있음.

## 정비 이력

- 2026-09-06 GOV-20260906-01: 누락된 기존 아이디어 2건을 인덱스에 복원.
- 2026-09-06 GOV-20260906-02: 기존 6개 아이디어에 안정적인 record_id/actor_id 매핑을 추가. 원문 경로는 이동하지 않음. 신규 기록부터 actor_id 경로 사용.
- 2026-09-08: ACT-002 첫 문제 기록 P-20260908-001 추가. 문제 저장 자체는 업무 배정·차단·해결 확정이 아님.
- 2026-09-08: ACT-003 문제 기록 P-20260908-002 추가. 이미지 생성 품질 문제를 독립 기록으로 저장했으며 기존 업무 상태는 변경하지 않음.
- 2026-09-09: ACT-002 아이디어 I-20260909-001 추가. 상품 수익 운영 책임자 역할 제안을 저장했으며 기존 업무·승인·회사 기준은 변경하지 않음.
