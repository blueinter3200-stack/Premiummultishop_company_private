# Miracle Company Private

대표님·관리자 Jin·부사수 및 향후 등록되는 회사 협업자가 사용하는 **회사 기준, 전처리 데이터, 업무, 근거, 품의·결재 기록** 저장소.

- Repository: `jintonic1010/miracle_company_private`
- Canonical branch: `main`
- Updated: 2026-09-06
- Release: `GOV-20260906-02`

## 가장 먼저

`FILE_MAP.json` → `llm-source/ACTOR_REGISTRY.json` → 자기 역할 → `llm-source/LLM_RUNTIME.md` → 회사 공식 기준 → `working/CURRENT_WORK.md`를 읽는다. 상세 자료는 현재 업무와 연결된 것만 읽는다.

## 사람·역할·기록 ID

- actor_id: 사람/행위자 고정 ID. 현재 `ACT-001` Jin, `ACT-002` 대표님, `ACT-003` 부사수.
- role: 현재 직무/권한. 역할이 바뀌어도 과거 actor_id를 다시 쓰거나 과거 기록의 소유자를 바꾸지 않는다.
- idea/problem/work/decision은 각각 별도 ID를 가진다.
- 새 사람이 들어오면 관리자가 새 `ACT-NNN`을 발급하고 역할·프로젝트 소스를 연결한다.

기존 role 기반 아이디어 경로는 참조 안정성을 위해 이동하지 않는다. 새 아이디어·문제부터 actor_id 경로를 사용한다.

## 아이디어·문제·업무 구분

아이디어를 검토했다고 업무가 된 것은 아니다. `/업무검토`는 먼저 대상을 `idea / problem / work / mixed / policy_change`로 분류한다.

- idea → `/아이디어저장` 권장
- problem → `/문제저장` 권장
- 실제 실행 범위·다음 행동이 있는 work → `/업무공유`
- idea + 조사 지시 → 아이디어와 조사 업무를 서로 다른 ID로 연결

부사수도 자기 아이디어와 실무 중 발견한 문제를 저장할 수 있다. 문제 저장이 자동으로 업무 차단을 뜻하지 않으며 실제 업무 영향은 관련 work_id 상태로 따로 관리한다.

## 역할

대표님은 아이디어·방향·요청을 넣는다. 부사수는 전처리·조사·실무·초안·상신을 맡는다. 이 업무·품의 체계의 최종 결재권자는 관리자 Jin이다.

## 저장 위치

| 위치 | 의미 |
|---|---|
| `llm-source/` | 승인된 회사 기준과 공통 규격 |
| `llm-source/ACTOR_REGISTRY.json` | 고정 actor_id와 현재 역할 매핑 |
| `roles/`, `assistant/00-role/` | 역할과 권한 |
| `assistant/10-playbooks/` | 반복 수행 방법 |
| `assistant/20-directives/` | 요청 원문·업무 지시 |
| `work/items/` | 개별 업무 상태 원장 |
| `working/CURRENT_WORK.md` | 회사 현재 업무판 |
| `assistant/40-handoff/` | 결과물·근거·결정 요청 |
| `approvals/` | 관리자 결재 기록 |
| `records/ideas/<actor_id>/` | 새 아이디어 기록 |
| `records/problems/<actor_id>/` | 새 문제 기록 |
| `materials/normalized/` | 출처가 연결된 정제자료 |
| `materials/originals/` | 실제 확보한 비민감 원본 |

GitHub는 문서·지식·품의 기록의 원장이다. ERP는 운영 데이터 원장, n8n은 연결·자동화 기반이다. 고객 개인정보·운영 DB·인증정보를 GitHub로 복사하지 않는다.

## 완료 기준

main 저장, 결과물 승인, 외부 게시, 도구 연결, 프로젝트 지침 설치는 서로 다른 완료 항목이다.
