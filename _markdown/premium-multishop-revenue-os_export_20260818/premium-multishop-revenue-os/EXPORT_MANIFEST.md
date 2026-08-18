---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/EXPORT_MANIFEST.md"
source_filename: "EXPORT_MANIFEST.md"
source_type: "text"
source_size_bytes: 9553
source_modified_at: "2026-08-18T05:49:18+09:00"
source_sha256: "8f70a19cbd95c9024cb6515710a8592f279d71b64d82aa5f241366b94fa51113"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# EXPORT_MANIFEST

- 반출 실행일: 2026-08-18
- 실행 주체: Claude (claude.ai 웹 인터페이스, Opus 4.6 계열)
- 목적: 이 Claude 프로젝트의 자산을 정리·개선 없이 **1차 원본 수집**하여 별도 AI가 재분석할 수 있게 확보
- 대상 저장소: `https://github.com/blueinter3200-stack/success_build_up.git`
- **GitHub 실제 반영 여부: 실패 / 미완료** (사유는 §5)

---

## 1. 프로젝트 식별

- 자체 결정한 프로젝트 폴더명: **`premium-multishop-revenue-os`**
- 선택 이유:
  - 프로젝트 지침 문서의 정식 제목이 "PREMIUM MULTISHOP — CLAUDE REVENUE EXECUTION INSTRUCTIONS v3.0"이고, 지침 §0에서 자신의 정체성을 "Revenue Execution OS"로 정의한다.
  - 사용자 개인설정(userPreferences)의 소속 표기도 "Premium MultiShop AI Revenue OS"다.
  - 프로젝트 지식 44개 문서 전체가 단일 사업체(프리미엄멀티샵)의 매출·마진·현금흐름 운영에 집중되어 있어, 브랜드명 + 기능(revenue OS) 조합이 타 프로젝트와 혼동되지 않는다.
  - `business-planning`, `ai-sales-system` 같은 일반명은 다른 프로젝트와 충돌할 수 있어 배제했다.
- **주의:** claude.ai 시스템상 이 프로젝트의 **공식 프로젝트 이름은 확인할 수 없다.** 위 이름은 Claude가 접근 가능한 지침·메모리·지식 문서에서 추론해 직접 정한 것이다.

---

## 2. 폴더 구조

```
premium-multishop-revenue-os/
├─ EXPORT_MANIFEST.md
├─ instructions/
│  ├─ original__PROJECT_INSTRUCTIONS_v3.0.md
│  └─ original__USER_PREFERENCES_agent_template.md
├─ memory/
│  └─ reconstructed__project_memory_as_injected.md
├─ context/
│  ├─ 00_CONTEXT_INVENTORY.md            (파일별 크기 + SHA256)
│  └─ claude_01 ~ claude_43 (총 44개 .md 원본)
├─ external-documents/
│  ├─ original__프리미엄멀티샵_소싱처_마스터__gsheet_export.md
│  └─ reference__google_drive_inventory.md   (Drive 50건 인벤토리)
├─ generated-documents/
│  └─ README.md                          (산출물 ↔ context/ 매핑)
└─ conversations/
   └─ reconstructed__conversation_index_and_handoff.md
```

파일 접두어 규칙: `original__` / `reconstructed__` / `reference__`.

---

## 3. 반출 성공 자료

| 자료명 | 종류 | 저장 경로 | 원본 여부 | 변환 여부 | 설명 |
|---|---|---|---|---|---|
| 프로젝트 지침 v3.0 | 지침 | `instructions/original__PROJECT_INSTRUCTIONS_v3.0.md` | original | 없음 | 17개 장 전문. 축약·개선 없음 |
| userPreferences | 지침 | `instructions/original__USER_PREFERENCES_agent_template.md` | original | 없음 | 서브에이전트 표준 템플릿. 미기입 플레이스홀더도 그대로 보존 |
| 프로젝트 메모리 | 메모리 | `memory/reconstructed__project_memory_as_injected.md` | **reconstructed** | 해당없음 | 원본 DB 접근 불가. 컨텍스트에 주입된 메모리 요약문 전문을 그대로 옮김. 문서 상단에 "원본 직접 추출 불가" 명시 |
| 프로젝트 지식 44개 문서 | 컨텍스트 | `context/claude_*.md` | original | 없음 | `/mnt/project/`에서 바이트 단위 복사, 총 432KB |
| 컨텍스트 인벤토리 | 목록 | `context/00_CONTEXT_INVENTORY.md` | Claude 생성 | - | 파일별 크기·SHA256 해시(무결성 검증용) |
| 소싱처 마스터 시트 | 외부문서 | `external-documents/original__프리미엄멀티샵_소싱처_마스터__gsheet_export.md` | original | **변환됨** | Google Sheets → Markdown 표. 6개 시트탭(소싱처 53건 / 범례 / B2B·API 공급사 18건 / 드랍쉬핑 9건 / 전 바이어 컨택 123건 / 요약) 포함. 셀 서식·수식·색상 손실. 마지막 인사이트 문장 truncated |
| Google Drive 인벤토리 | 외부문서 | `external-documents/reference__google_drive_inventory.md` | reference | - | 최근 활동 50건의 제목·형식·fileId·URL·수정일. 본문 미확보 |
| 산출물 매핑 | 목록 | `generated-documents/README.md` | Claude 생성 | - | 대화 산출물 33종이 context/ 어느 파일인지 매핑 |
| 대화 인덱스·핸드오프 | 대화 | `conversations/reconstructed__conversation_index_and_handoff.md` | **reconstructed** | - | 조회된 대화 7건(2026-07-15~08-06)의 요약 + 링크 + 핸드오프 노트 |

---

## 4. 확인했지만 반출하지 못한 자료

| 자료 | 존재 확인 방법 | 미반출 사유 | 사용자 조치 필요 |
|---|---|---|---|
| Google Docs/Sheets 본문 49건 (사업계획서 v4, 중기부 R&D 계획서, GoogleAds 지침서·워크북, 네이버 광고 지침서, 유럽API공급사 100리스트, 파트너십 v2, 자사몰 일정관리, claude_32 외부에이전트 등) | Drive API `list_recent_files`로 제목·ID·크기 확인 | Drive 문서를 GitHub 파일로 옮기려면 Claude가 전문을 컨텍스트로 읽고 다시 써야 함. 총 용량이 단일 세션 컨텍스트 한도를 초과 | **예.** Drive에서 직접 .docx/.xlsx 다운로드 후 업로드(서식 보존) 또는 새 세션에서 1~2건씩 재추출 |
| `블루계정정보` 시트 (39KB, 타 계정 소유) | Drive 인벤토리 42번 | **의도적 미반출.** 계정·인증정보로 추정되어 공개 저장소 반출 부적합 | 예. 반출 필요 여부를 사용자가 직접 판단 |
| 2026-08-07 ~ 2026-08-18 대화 | 프로젝트 지식에 해당 기간 산출물 존재(주간점검 8/7~8/12, 사업계획서 8/13, NIPA·중기부 8/14, GoogleAds 8/15, 통합CRM 8/18) | `recent_chats` 조회 결과 최신 대화가 2026-08-06. 해당 기간 대화가 반환되지 않음 | 예. 원인 확인 필요(인덱싱 지연 / 다른 프로젝트 소속 / 조회범위 제한) |
| 대화 원문(raw transcript) 전체 | - | claude.ai는 대화 원문 export 도구를 Claude에게 제공하지 않음. `recent_chats`는 모델 생성 요약문만 반환 | 예. 설정 > 데이터 내보내기(계정 export)로 사용자가 직접 받아야 함 |
| Drive 폴더 `대표님 `(blueuropesrl 소유), `hermes-agent-kit-mirror`(hanzoom2000 소유) 내부 파일 | Drive 인벤토리 17·50번 | 폴더만 확인, 내부 파일 목록 미조회 | 예 |
| Drive 최근활동 50건 이외 파일 | - | `list_recent_files` 2페이지(50건)까지만 수집. 그 이전 파일은 미조회 | 예 |

---

## 5. 접근 자체가 불가능했던 영역 (추측하지 않고 명시)

| 항목 | 상태 |
|---|---|
| 프로젝트 공식 이름 | **확인 불가.** 폴더명은 Claude가 추론해 결정 |
| 프로젝트 메모리 원문(저장소 raw 데이터) | **확인 불가.** 컨텍스트 주입 요약본만 확보 |
| 프로젝트 지침 설정 필드 원본 | **직접 읽기 불가.** 단, 이번 세션에서 사용자가 지침 전문을 직접 전달했으므로 내용은 100% 동일 |
| 과거 전체 대화 원문 | **확인 불가.** 요약 7건만 확보 |
| GitHub 저장소 현재 상태(기존 파일·브랜치) | **확인 불가.** 인증 실패로 저장소 내용을 읽지 못함 |

### GitHub 반영 실패 사유 (정확한 원인)

컨테이너에서 실제로 실행한 결과:

```
$ git ls-remote https://github.com/blueinter3200-stack/success_build_up.git
fatal: could not read Username for 'https://github.com': No such device or address

$ curl -o /dev/null -w "%{http_code}" https://github.com/blueinter3200-stack/success_build_up
404

$ curl -o /dev/null -w "%{http_code}" https://api.github.com/repos/blueinter3200-stack/success_build_up
403
```

- 컨테이너에 GitHub **인증정보(PAT·SSH 키·gh CLI 로그인)가 전혀 없다.** 환경변수에도 토큰이 없다.
- 저장소가 비공개이거나 이름이 다를 가능성이 있다(웹 404). 어느 쪽이든 **인증 없이는 push 불가**다.
- Claude에게는 GitHub 커넥터도 연결되어 있지 않다.
- 따라서 **저장소에 아무것도 쓰지 않았고, 기존 다른 프로젝트 자료도 전혀 건드리지 않았다.**

### 사용자가 해야 할 일

1. 아래 zip을 내려받아 압축을 푼다.
2. 로컬에서 저장소를 클론한 뒤 `premium-multishop-revenue-os/` 폴더를 통째로 넣고 커밋·푸시한다.
   ```bash
   git clone https://github.com/blueinter3200-stack/success_build_up.git
   cd success_build_up
   # 압축 푼 premium-multishop-revenue-os 폴더를 여기로 복사
   git add premium-multishop-revenue-os
   git commit -m "Add Claude project export: premium-multishop-revenue-os (2026-08-18)"
   git push
   ```
   (같은 이름 폴더가 이미 있으면 덮어쓰지 말고 `premium-multishop-revenue-os-20260818/` 로 이름을 바꿔 넣을 것)
3. `§4`의 Drive 문서 7건을 Drive에서 직접 다운로드해 `external-documents/`에 추가한다.
4. 계정 설정 > 데이터 내보내기로 대화 원문을 받아 `conversations/`에 추가한다.

---

## 6. 이번 반출에서 하지 않은 일 (1차 반출 원칙 준수 확인)

- 중복·구버전이라는 이유로 삭제하지 않았다 (Drive 중복본 5건도 인벤토리에 그대로 기록).
- 여러 원본을 하나의 요약으로 합치지 않았다.
- 기존 지침을 개선하거나 수정하지 않았다.
- 서로 충돌하는 내용(예: 네이버 광고 지침서 vs 2026-07-16 광고 축소 결정)을 임의로 한쪽만 택하지 않았다. 충돌 사실만 기록했다.
- 사업 아이디어의 채택/폐기를 판단하지 않았다.
- 다른 프로젝트 폴더를 읽거나 수정하지 않았다.
