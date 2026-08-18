---
source_path: ".pi/검토/CURRENT_TO_PROPOSED_MAPPING.md"
source_filename: "CURRENT_TO_PROPOSED_MAPPING.md"
source_type: "text"
source_size_bytes: 11350
source_modified_at: "2026-08-17T18:43:40+09:00"
source_sha256: "ec4b5995e93604f78ab05e641b8424dab24709599180e9e3a84868698aea653d"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 현재 → 권장 구조 매핑

이 표는 개념적 이동안이다. 실제 파일을 이동·이름 변경하지 않았다.

| Current path/group | Current meaning | Recommended destination | Action | Reason |
| --- | --- | --- | --- | --- |
| `BusinessVault/index.md` | 사업 볼트 전체 인덱스 | `knowledge-corpus/business/index.md` 또는 각 사업 index | split | 현재는 공통·PMS·BELLOON 탐색이 한 파일에 있음 |
| `BusinessVault/04-decision-log.md` | 여러 사업 결정의 누적 원장 | `business/*/02-decisions/` + `shared/portfolio-tracking/decision-index.md` | split | 첫 H2 아래 여러 결정이 섞여 헤딩 청킹 불가 |
| `BusinessVault/07-project-tracker.md` | 사업 포트폴리오 실행 추적 | `business/shared/portfolio-tracking/project-tracker.md` | move | 사업 간 실행 상태를 함께 보는 전역 원장 |
| `BusinessVault/2026-08-14.md` | 빈 날짜 노트 | `needs-decision` | needs-decision | 개인 일지와 혼동되며 내용 없음 |
| `BusinessVault/무제.md` | 빈 무제 노트 | `needs-decision` | needs-decision | 의미·소유 사업을 판정할 근거 없음 |
| `BusinessVault/research/premium-multishop-*.md` | PMS 시장·경쟁·채널·공급망 조사 | `business/premium-multishop/01-evidence-and-research/market-and-sourcing/` | move | 조사 근거를 PMS 사업 아래 모음 |
| `BusinessVault/research/premium-multishop-naver-blog-ai-income-review-*.md` | 콘텐츠 수익모델 검토 | `business/premium-multishop/01-evidence-and-research/feasibility-and-audits/` | move | 시장 원자료보다 사업성 검토 성격 |
| `BusinessVault/research/belloon-buyer-*.md` | 회사·인물 후보 조사 스냅샷 | `business/belloon/01-evidence-and-research/research-snapshots/` | move | 조사 시점과 방법을 보존하는 보고서 |
| `BusinessVault/research/belloon-linkedin-sourcing-ops.md` | 리드 스키마·점수·메시지 운영 표준 | `business/belloon/05-reference-and-templates/linkedin-sourcing-ops.md` | move | 조사 결과보다 운영 규칙·템플릿 |
| `BusinessVault/research/belloon-buyer-person-sourcing-*.md`의 갱신형 후보 | 여러 사람 레코드 | `business/belloon/01-evidence-and-research/people-leads/<slug>.md` | split | 사람별 최신 검증과 출처 갱신 필요 |
| `BusinessVault/research/belloon-buyer-sourcing-*.md`의 갱신형 회사 | 여러 회사 후보 | `business/belloon/01-evidence-and-research/company-leads/<slug>.md` | split | 회사와 사람을 분리하라는 기존 운영 표준 준수 |
| `BusinessVault/plans/belloon-b2b-beauty-focus-decision-*.md` | BELLOON 집중 결정 | `business/belloon/02-decisions/` | move | 계획보다 확정 결정 |
| `BusinessVault/plans/contracts.md` | 두 사업 계약 상태 | `business/shared/contracts/contracts.md` | move | 사업 공통 상태 원장 |
| `BusinessVault/plans/pms-revenue-commerce-os-v3-canonical-*.md` | 명시된 PMS 정본 설계 | `business/premium-multishop/03-strategy-and-design/` | keep | canonical 표기를 살려 기본 검색 정본으로 사용 |
| `BusinessVault/plans/pms-revenue-commerce-os-v1-*.md` | 9-Agent 운영 모델 초기 버전 | `business/premium-multishop/99-history/revenue-commerce-os/` | move | 최신 정본과 구분 필요 |
| `BusinessVault/plans/pms-revenue-commerce-os-v2-master-*.md` | 중간 통합 버전 | `business/premium-multishop/99-history/revenue-commerce-os/` | needs-decision | master와 later canonical의 관계 확인 필요 |
| `BusinessVault/plans/pms-revenue-commerce-os-v3-2026-08-14.md` | v3 구조 고도화안 | `business/premium-multishop/99-history/revenue-commerce-os/` | needs-decision | v3 canonical보다 앞선 초안으로 추정되나 확인 필요 |
| `BusinessVault/plans/pms-revenue-ladder-level0-level4-v1-*.md` | 수익 사다리 v1 | `business/premium-multishop/99-history/revenue-ladder/` | move | v2 재설계와 구분 |
| `BusinessVault/plans/pms-revenue-ladder-profitability-redesign-v2-*.md` | 수익 사다리 v2 검증 설계 | `business/premium-multishop/03-strategy-and-design/` | needs-decision | 현재 active인지 별도 확인 필요 |
| `BusinessVault/plans/pms-automation-platform-*.md` | 자동화 플랫폼 설계 | `business/premium-multishop/03-strategy-and-design/` | move | 현재 구조 설계군 |
| `BusinessVault/plans/pms-queryable-data-map-*.md` | 데이터 식별자·관계 설계 | `business/premium-multishop/03-strategy-and-design/` | move | PMS 기술·데이터 설계 |
| `BusinessVault/plans/pms-9-agent-learning-architecture-*.md` | Agent 학습·평가 설계 | `business/premium-multishop/03-strategy-and-design/` | move | 현재 설계군, 정본 관계 메타데이터 필요 |
| `BusinessVault/plans/pms-sourcing-pod-spec-*.md` | 소싱 Agent 필드·판단식 | `business/premium-multishop/03-strategy-and-design/` | move | 운영 아키텍처의 구성 문서 |
| `BusinessVault/plans/premium-multishop-integration-architecture.md` | Cafe24·공급처 통합 설계 | `business/premium-multishop/03-strategy-and-design/` | move | 기술 설계 |
| `BusinessVault/plans/pms-product-detailpage-conversion-system-*.md` | 상세페이지 전환 시스템 | `business/premium-multishop/03-strategy-and-design/` | move | 전략·운영 설계 |
| `BusinessVault/plans/pms-ai-detailpage-agent-master-prompt-*.md` | AI 상세페이지 프롬프트 | `business/premium-multishop/05-reference-and-templates/` | move | 사실 문서가 아닌 반복 사용 템플릿 |
| `BusinessVault/plans/premium-multishop-90-180-growth-roadmap-*.md` | 실행 로드맵 | `business/premium-multishop/04-execution/` | move | 기간·단계·KPI 중심 실행 문서 |
| `BusinessVault/plans/pms-execution-control-*.md` | 실행 통제·판정 구조 | `business/premium-multishop/04-execution/` | needs-decision | 설계와 실행 운영의 경계 판단 필요 |
| `BusinessVault/plans/*review*.md` | 사업성·수익성·거버넌스 검토 | `business/premium-multishop/01-evidence-and-research/feasibility-and-audits/` | move | 확정 계획과 분리 |
| `BusinessVault/plans/*audit*.md` | SEO·도메인 감사 | `business/premium-multishop/01-evidence-and-research/feasibility-and-audits/` | move | 진단 결과와 관리자 실행안 |
| `BusinessVault/plans/premium-multishop-digital-positioning.md` | 핵심 포지셔닝 | `business/premium-multishop/03-strategy-and-design/` | move | 현재 전략 방향 |
| `BusinessVault/plans/premium-multishop-ecommerce-transition.md` | 온라인 전환 계획 | `business/premium-multishop/03-strategy-and-design/` 또는 `04-execution/` | needs-decision | 전략과 실행 항목을 모두 포함 |
| `BusinessVault/ideas/belloon.md` + `ideas/belloon/index.md` | BELLOON 아이디어와 인덱스 | `business/belloon/05-reference-and-templates/ideas.md` | merge-group | 중복 탐색 계층 제거, 검증 전 아이디어 유지 |
| `BusinessVault/ideas/premium-multishop.md` + 하위 index | PMS 아이디어와 인덱스 | `business/premium-multishop/05-reference-and-templates/ideas.md` | merge-group | 동명 파일·폴더 중복 제거 |
| `BusinessVault/market/belloon.md` + 하위 index | BELLOON 조사 링크·요약 | `business/belloon/01-evidence-and-research/index.md` | merge-group | 실제 조사와 한 인덱스로 최신성 관리 |
| `BusinessVault/market/premium-multishop.md` + 하위 index | PMS 조사 링크·요약 | `business/premium-multishop/01-evidence-and-research/index.md` | merge-group | “자료 없음” 등 낡은 인덱스 제거 필요 |
| `BusinessVault/_archiv/` + `_archive/` | 보관 정책과 빈 중복 폴더 | 각 사업 `99-history/` 또는 공통 `archive/` | rename | 표준 이름 하나 필요 |
| `BusinessVault/TaskNotes/` | 작업관리 안내·뷰 | `app-state-no-index/tasknotes-views/business-vault/` 또는 볼트 내 유지 | keep | 기능상 볼트와 함께 유지 가능, 지식 색인 제외 |
| `BusinessVault/.obsidian/` | Obsidian 설정·플러그인 | `app-state-no-index/obsidian-vault-state/business-vault/` 또는 볼트 내 유지 | keep | 앱 기능용, 본문 코퍼스 아님 |
| `HermesWiki/journal/` | 실제 날짜별 일지 | `knowledge-corpus/personal/journal/` | keep | 날짜별 1파일과 YAML 구조가 좋음 |
| `HermesWiki/index.md`의 `logs/` 규칙 | 문서화된 표준 경로 | `knowledge-corpus/personal/journal/` | rename | 실제 자료가 있는 journal을 기본 추천, 사용자 결정 필요 |
| `HermesWiki/log.md` | 일지 생성 변경 로그 | `knowledge-corpus/personal/journal/change-log.md` | rename | daily log와 이름 충돌 방지 |
| `HermesWiki/inbox`, `profile`, `areas`, `projects`, `concepts` | 비어 있는 예약 분류 | `knowledge-corpus/personal/<same>/` | needs-decision | 향후 사용 의사가 있을 때만 유지 |
| `HermesWiki/TaskNotes/`, `.obsidian/` | 앱 설정·기본 뷰 | `app-state-no-index/.../personal-wiki/` 또는 볼트 내 유지 | keep | AI 색인 제외 |
| `.agents/skills/*` | 설치된 범용 마케팅 스킬 | `ai-operating-assets/marketing-skills/` | move | AI 지침, 사업 사실과 별도 검색 |
| `.agents/.skill-lock.json` | 스킬 설치 출처·해시 | `ai-operating-assets/marketing-skills/manifest.json` | keep | 유용한 provenance |
| `.claude/skills/hermes-vps-setup/` | 설치 스킬·스크립트·PDF | `ai-operating-assets/hermes-vps-setup/` | move | 한 패키지로 같이 유지 |
| `.claude/skills/hermes-vps-setup/setup.env` | 채워질 수 있는 비밀 설정 | 공유 루트 밖 비밀 저장소 | move | 코퍼스·패키지 배포에서 제외 |
| `.claude/projects/**/*.jsonl` | 대화·도구 이벤트 원장 | `app-state-no-index/conversation-history/` | move | 민감하고 잡음이 많아 RAG 제외 |
| `.claude/tasks/**/*.json` | 작업 상태·생성 이력 | `app-state-no-index/conversation-history/tasks/` | move | provenance에는 유용하나 지식 정본 아님 |
| `.claude/backups/`, `.credentials.json` | 설정 백업·자격증명 | 공유 루트 밖 비밀 저장소 | move | 보안 경계 |
| `Claude/Projects/...docx` | 2026-06 상세페이지 벤치마크 보고서 | `business/premium-multishop/01-evidence-and-research/source-artifacts/` | needs-decision | 이후 문서와 겹치며 공식성 확인 필요 |
| `Claude/Artifacts/.../index.html` + `thumbnail.png` | 구매대행·면세 아키텍처 시각자료 | `business/premium-multishop/01-evidence-and-research/source-artifacts/` | move | 한 산출물로 함께 유지, 검증 상태 표시 |
| `.cache/` | Chromium 실행 캐시 | `machine-cache-no-index/browser-runtime/` 또는 코퍼스 밖 | move | 문서가 아니며 535MB 잡음 |
| `.hermes-sync/` | Syncthing 실행·키·설정 | `app-state-no-index/sync-state/`와 비밀 저장소 | split | 실행 상태와 개인키의 보안 수준이 다름 |
| `.ssh/` | SSH 키·접속 설정 | 공유 루트 밖 OS 보안 위치 | move | 절대 색인·공유 금지 |
| `Intel/`, `Favorites/`, `dwhelper/` | OS 로그·바로가기·빈 폴더 | `machine-cache-no-index/installer-logs/` 또는 코퍼스 밖 | move | 지식 코퍼스와 무관 |
| 비어 있는 49개 에이전트 대상 폴더 | 설치 대상 자리로 추정 | `app-state-no-index/agent-target-placeholders/` | needs-decision | 활성 도구 의존성 확인 전 삭제 금지 |

