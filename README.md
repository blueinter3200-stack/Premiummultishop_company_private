# Miracle Company Private

대표님·관리자 Jin·부사수가 사용하는 **회사 기준, 전처리 데이터, 업무, 근거, 품의·결재 기록** 저장소.

- Repository: `jintonic1010/miracle_company_private`
- Canonical branch: `main`
- Updated: 2026-09-06
- Release: `GOV-20260906-01`

## 가장 먼저

`FILE_MAP.json` → 자기 역할 → `llm-source/LLM_RUNTIME.md` → 회사 공식 기준 → `working/CURRENT_WORK.md`를 읽는다. 상세 자료는 현재 업무와 연결된 것만 읽는다.
프로젝트에 넣을 문장은 `chatgpt/admin/PROJECT_INSTRUCTIONS.md`, `chatgpt/representative/PROJECT_INSTRUCTIONS.md`, `chatgpt/assistant/PROJECT_INSTRUCTIONS.md`에 있다. 배포 방법은 `chatgpt/INSTALLATION.md`를 따른다.

## 바뀌지 않는 중심

원본 → 의미 보존 전처리 → 출처·주장 검증 → 분석·초안 → 품의 → 관리자 결재 → 승인 범위 내 실행 → 실제 결과 확인.

원본을 정제했다고 사실 검증이나 회사 승인이 끝난 것은 아니다. AI의 설명은 출처가 아니다. 업무 ID, 원본 위치·버전, 정보 기준일, 변환 이력, 결과물 버전, 결재 범위를 연결한다.

## 역할

대표님은 아이디어·방향·요청을 넣는다. 부사수는 전처리·조사·실무·초안·상신을 맡는다. 이 업무·품의 체계의 최종 결재권자는 관리자 Jin이다. 대표님 요청이나 부사수의 '승인받았다'는 전달만으로 승인 상태를 만들지 않는다.

## 저장 위치

| 위치 | 의미 |
|---|---|
| `llm-source/` | 승인된 회사 기준과 공통 규격 |
| `roles/`, `assistant/00-role/` | 역할과 권한 |
| `assistant/10-playbooks/` | 데이터·마케팅·콘텐츠·자동화의 반복 수행 방법 |
| `assistant/20-directives/` | 요청 원문·업무 지시, 업무 ID 연결 |
| `work/items/` | 개별 업무 상태의 유일한 원장 |
| `working/CURRENT_WORK.md` | 원장에서 생성하는 회사 현재 업무판 |
| `assistant/30-working/` | 부사수·관리자가 보는 원장 기반 조회판 |
| `assistant/40-handoff/` | 결과물·근거·검증 경로·결정 요청 |
| `approvals/` | 관리자 결재 기록; 실행 성공과 별개 |
| `records/` | 저장된 아이디어·문제; 저장만으로 공식화되지 않음 |
| `materials/normalized/` | 출처가 연결된 정제자료와 검색용 메타데이터 |
| `materials/originals/` | 실제 확보한 비민감 원본만 보존 |
| `archive/` | 과거판; 기본 읽기 금지 |

GitHub는 문서·지식·품의 기록의 원장이다. ERP는 운영 데이터 원장, n8n은 연결·자동화 기반이다. 영상·대형 파일은 승인된 Drive/자산 저장소의 파일 ID·버전으로 참조한다. 고객 개인정보·운영 DB·인증정보를 GitHub로 복사하지 않는다.

## 완료 기준

main 저장, 결과물 승인, 외부 게시, 도구 연결, 프로젝트 지침 설치는 서로 다른 완료 항목이다. 문서 배포만으로 계정 인증·경로별 권한·자동 알림·Higgsfield 연결이 구현됐다고 말하지 않는다.
