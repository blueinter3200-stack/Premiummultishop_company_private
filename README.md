# Miracle Company Private

대표님·관리자 Jin·부사수 및 향후 등록되는 회사 협업자가 사용하는 **회사 기준, 전처리 데이터, 업무, 근거, 품의·결재 기록** 저장소.

- Repository: `jintonic1010/miracle_company_private`
- Canonical branch: `main`
- Updated: 2026-09-06
- Release: `GOV-20260906-04`

## 가장 먼저

명령 설명·추천과 대화 내 아이디어/문제 출력은 프로젝트 지침·`chatgpt/PROJECT_COMMON.md`·자기 ROLE로 안내한다. 이 단계에서 GitHub 조회를 먼저 요구하지 않는다.
최신 회사 사실을 답하거나 실제 검토·저장·결재를 할 때는 `FILE_MAP.json` → `llm-source/ACTOR_REGISTRY.json` → 자기 역할 → `llm-source/LLM_RUNTIME.md` → 회사 공식 기준·해당 워크플로 → `working/CURRENT_WORK.md`를 읽는다. 상세 자료는 현재 업무와 연결된 것만 읽는다.

## 사람·역할·기록 ID

- actor_id: 사람/행위자 고정 ID. 현재 `ACT-001` Jin, `ACT-002` 대표님, `ACT-003` 부사수.
- role: 현재 직무/권한. 역할이 바뀌어도 과거 actor_id를 다시 쓰거나 과거 기록의 소유자를 바꾸지 않는다.
- request/idea/problem/work/submission/decision은 각각 별도 ID를 가진다.
- 새 사람이 들어오면 관리자가 새 `ACT-NNN`을 발급하고 역할·프로젝트 소스를 연결한다.

기존 role 기반 아이디어 경로는 참조 안정성을 위해 이동하지 않는다. 새 아이디어·문제부터 actor_id 경로를 사용한다.

## 아이디어·문제·업무 구분

아이디어를 검토했다고 업무가 된 것은 아니다. `/업무검토`는 먼저 대상을 `idea / problem / work / mixed / policy_change`로 분류한다.

- idea → `/아이디어저장` 권장
- problem → `/문제저장` 권장
- 실제 실행 범위·다음 행동이 있는 work → `/업무공유`
- idea + 조사 지시 → 아이디어와 조사 업무를 서로 다른 ID로 연결

부사수도 자기 아이디어와 실무 중 발견한 문제를 저장할 수 있다. 문제 저장이 자동으로 업무 차단을 뜻하지 않으며 실제 업무 영향은 관련 work_id 상태로 따로 관리한다.
명확한 업무·지속 지시는 R-ID로 보존하되 단순 질문·읽기 전용 검토·저장 금지는 자동 기록하지 않는다.

## 역할과 쉬운 명령

대표님은 아이디어·방향·요청을 넣는다. 부사수는 전처리·조사·실무·초안·품의서 작성을 맡는다. 이 업무·품의 체계의 최종 결재권자는 관리자 Jin이다.
관리자 현황 조회는 `/업무점검 대표님`, `/업무점검 부사수`, `/업무점검 전체`다. 품의 문서는 `/품의서작성`, 관리자 결재는 `/품의서승인`이다. 구명령은 동일 권한 별칭으로만 호환한다.

## 저장 위치

| 위치 | 의미 |
|---|---|
| `llm-source/` | 승인된 회사 기준과 공통 규격 |
| `llm-source/ACTOR_REGISTRY.json` | 고정 actor_id와 현재 역할 매핑 |
| `llm-source/actors/<actor_id>/` | 각 actor의 역할·권한 소스 |
| `llm-source/TRIGGER_REGISTRY.json` | 명령·권한·실행 모드·워크플로 연결 |
| `llm-source/workflows/` | 기능별 상세 실행·검증·실패 처리 |
| `assistant/10-playbooks/` | 반복 수행 방법 |
| `assistant/20-directives/` | 기존 요청 원문·업무 지시 보존 |
| `records/requests/<actor_id>/` | 새 명확한 사용자 요청과 연결 ID |
| `records/REQUEST_INDEX.md` | 요청 선택 조회 목차 |
| `work/items/` | 개별 업무 상태 원장 |
| `working/CURRENT_WORK.md` | 회사 현재 업무판 |
| `assistant/40-handoff/` | 결과물·근거·결정 요청 |
| `approvals/` | 관리자 결재 기록 |
| `records/ideas/<actor_id>/` | 새 아이디어 기록 |
| `records/problems/<actor_id>/` | 새 문제 기록 |
| `materials/normalized/` | 출처가 연결된 정제자료 |
| `materials/originals/` | 실제 확보한 비민감 원본 |

GitHub는 문서·지식·품의 기록의 원장이다. ERP는 운영 데이터 원장, n8n은 연결·자동화 기반이다. 고객 개인정보·운영 DB·인증정보를 GitHub로 복사하지 않는다.

## 설치·검증

`chatgpt/INSTALLATION.md`를 따른다. 프로젝트 지침과 소스는 이번 판으로 교체해야 하며 GitHub 반영만으로 실제 프로젝트 설정이 바뀌지는 않는다.
`python scripts/validate_llm_sources.py`는 JSON·명령·역할·경로·manifest 구조를 검사한다. 실제 LLM 행동이나 외부 도구 실행을 검증하는 테스트가 아니다.
main 저장, 결과물 승인, 외부 게시, 도구 연결, 프로젝트 지침 설치는 서로 다른 완료 항목이다.

## 관리자 요청 변경추적

기존 R-ID의 관리자 요구가 의미 있게 바뀌면 RC-ID로 what/why/evidence/impact를 남긴다. 최초 원문·revision·supersedes는 보존하며 RC는 승인·완료가 아니다. 절차: `llm-source/workflows/REQUEST_CHANGE_WORKFLOW.md`. 정본은 `records/request-changes/ACT-001/<R-ID>/<RC-ID>.json`, 목차는 `records/REQUEST_CHANGE_INDEX.md`다.
대표님·부사수의 명령·역할·요청 revision 동작은 유지한다. `python -m unittest discover -s tests -v`로 A–H 등 RC 단위 테스트를 실행한다. `scripts/request_changes.py`는 계획·검증만 하며 실제 GitHub 쓰기는 COMMON_IO로 수행한다.
배포 ZIP 재생성: `python scripts/build_chatgpt_package.py --source-commit <실제 확인한 커밋> --output <출력 폴더>`.
