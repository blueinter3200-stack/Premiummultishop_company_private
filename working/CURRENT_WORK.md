# Current Work

- Updated: 2026-09-06
- Source of state: `work/items/*.json`
- Authority: 파생 현재 업무판; 공식 요구사항·결재 원장이 아님

원장을 먼저 수정하고 이 화면을 함께 갱신한다. 기존 상세 업무판은 `archive/migrations/2026-09-06/CURRENT_WORK.before.md`에 동일 원문으로 보존했다. 2026-08-27 보고의 이관은 2026-09-06 실제 진행 재검증이 아니다.

| 업무 ID | 업무 | 상태 | 담당 | 다음 행동 | 원장 |
|---|---|---|---|---|---|
| W-20260827-001 | 회사 OS 설계·보고 준비 | 진행 보고·재확인 필요 | 미정 | 실제 프로젝트 배포·운영 상태 확인 | `work/items/W-20260827-001.json` |
| W-20260827-002 | ERP/API 연동 | 진행 보고·결정 필요 | 미정 | ERP 선택·API 범위·데이터 계약 | `work/items/W-20260827-002.json` |
| W-20260827-003 | AI 매출개선 국책과제 | 협의·재확인 필요 | 미정 | 부처·기관·실증·예산·기간·KPI 조사 | `work/items/W-20260827-003.json` |
| W-20260827-004 | ComfyUI/VTON 인력·파이프라인 | 진행 보고·재확인 필요 | 미정 | 계약·PoC·워크플로 인수 기준 | `work/items/W-20260827-004.json` |
| W-20260827-005 | 퍼포먼스/CRM 인력 | 협의·미확정 | 미정 | 직무·경력·인원·채용 순서 | `work/items/W-20260827-005.json` |
| W-20260906-001 | 세 역할·전처리·품의 규격 배포 | 배포 검수 중 | admin | main 검증·프로젝트 설치·실제 동작 검사 | `work/items/W-20260906-001.json` |

## 현재 확정 기준

회사 정책은 llm-source, 업무 상태는 위 원장, 관리자 결재는 approvals에서 확인한다. 이번 배포는 ERP 후보 선택이나 예전 미반영 사업 수치·투자·광고 집행을 확정하지 않는다.

## 조회

- 관리자 결정/미정: `assistant/30-working/DECISION_NEEDED.md`
- 부사수 배정 업무: `assistant/30-working/ACTIVE.md`
- 미반영 아이디어: `records/PENDING_INDEX.md` (6건, 자동 업무 배정 아님)
- 자료 품질: `docs/DATA_QUALITY.md`
