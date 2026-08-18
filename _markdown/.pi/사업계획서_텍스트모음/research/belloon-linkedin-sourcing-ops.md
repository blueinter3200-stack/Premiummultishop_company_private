---
source_path: ".pi/사업계획서_텍스트모음/research/belloon-linkedin-sourcing-ops.md"
source_filename: "belloon-linkedin-sourcing-ops.md"
source_type: "text"
source_size_bytes: 15463
source_modified_at: "2026-08-12T17:07:36+09:00"
source_sha256: "c91a372be57eb2c080788713aa5886b57279dbadb231a134ccb025255af684c2"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# BELLOON LinkedIn 바이어 소싱 — 운영·품질관리 표준

- 상태: 운영 초안 (외부 발송 금지, 대표 승인 전 검토용)
- 기준일: 2026-08-12
- 적용 범위: BELLOON의 해외 OEM·ODM, 한국 브랜드 수권 유통, PB, 자체 브랜드 기회
- 원칙: 회사와 사람을 분리 기록하고, 공개 출처만 사용하며, 모든 주장은 인용 가능한 근거와 함께 보관한다.

## 1. 산출물과 승인 게이트

에이전트는 `발견 → 회사 검증 → 사람 검증 → 기회 분류 → 점수 → 초안`까지만 수행한다. LinkedIn 연결·메시지 발송·이메일 발송·계약·샘플·견적 확정은 대표의 명시적 승인 없이는 실행하지 않는다.

필수 산출물:

1. 회사 레코드 1건 (`company-leads/`)
2. 사람 레코드 0~N건 (`people-leads/`) — 사람을 찾지 못하면 빈 상태를 명시
3. 회사-사람-기회의 연결 ID
4. 출처 URL, 조사일, 사실/추정 구분, 신뢰도
5. 승인 전 상태의 메시지 초안 (`message-drafts/`)
6. 다음 확인일과 후속 상태 (`follow-up/` 및 프로젝트 트래커)

## 2. 정규 리드 스키마

### 2.1 회사 레코드 (`company-leads/<slug>.md`)

```yaml
---
record_type: company_lead
lead_id: BL-C-YYYYMMDD-###
company_name: ""
legal_name: ""                 # 공개 확인 전 빈칸
country: ""
city: ""
regions_served: []
website: ""
linkedin_company_url: ""
company_size_public: ""
company_type: "distributor|importer|retailer|salon-spa-distributor|marketplace|brand|manufacturer|other"
channels: []                    # pharmacy, salon, department_store, ecommerce 등
portfolio_summary: ""
opportunity_types: []            # oem_odm, authorized_distribution, pb, own_brand
stage: "new|company_verified|person_needed|draft_ready|awaiting_approval|approved_to_contact|contacted|qualified|nurture|disqualified"
score_total: 0
score_band: "S|A|B|C|D"
confidence: 0.00
last_verified: "YYYY-MM-DD"
next_review: "YYYY-MM-DD"
owner: ""
source_ids: []
linked_people: []
---
```

본문 필수 섹션: `## 확인된 사실`, `## 미확인·검증 필요`, `## 기회 가설`, `## 점수 근거`, `## 리스크·하드스탑`, `## 다음 검증 액션`, `## 출처`.

### 2.2 사람 레코드 (`people-leads/<slug>.md`)

```yaml
---
record_type: person_lead
person_id: BL-P-YYYYMMDD-###
name: ""
company_lead_id: "BL-C-..."
linkedin_profile_url: ""
public_title: ""
role_bucket: "distributor|importer|brand_manager|purchasing|product_development|founder|unknown"
location_public: ""
public_work_context: ""
contact_channel: "linkedin|company_contact_form|public_business_email|unknown"
contact_value: ""              # 공개된 업무용 값만; 개인 연락처 금지
identity_confidence: 0.00
role_relevance_score: 0
status: "unverified|verified|drafted|approved|contacted|replied|not_relevant|do_not_contact"
last_verified: "YYYY-MM-DD"
source_ids: []
---
```

본문 필수 섹션: `## 확인된 공개 사실`, `## 역할 적합성`, `## 개인화에 사용할 사실`, `## 사용 금지 추정`, `## 출처`. 이름·직함·회사 소속은 공개 프로필에서 각각 확인하지 못하면 미확인으로 둔다. 이메일을 추정하거나 패턴 생성하지 않는다.

### 2.3 출처 객체

모든 URL은 다음 형식으로 ID를 부여한다. `SRC-### | URL | 출처 유형 | 조사일 | 확인한 주장 | 접근 상태`. 출처 유형 우선순위는 공식 회사 웹사이트/공식 문서 > LinkedIn 회사 페이지 > 신뢰 가능한 제3자 자료 > 검색 결과 스니펫이다. 스니펫만으로 회사 규모·구매 의향·수권을 확정하지 않는다.

## 3. 점수 rubric (100점)

| 항목 | 배점 | 만점 조건 |
|---|---:|---|
| 카테고리 적합성 | 20 | 화장품/스킨케어 수입·유통이 공식적으로 확인됨 |
| 채널·시장 적합성 | 15 | 목표국가와 실제 채널/지역 커버리지가 확인됨 |
| 조달·브랜드 도입 신호 | 15 | 파트너/브랜드/문의/소싱·상품개발 기능이 공개 확인됨 |
| 기회 유형 적합성 | 15 | OEM·ODM, 수권, PB 또는 자체브랜드 가설을 뒷받침하는 사실이 있음 |
| 규모·실행력 | 10 | 직원 수, 매장·유통망·지역 커버리지 중 하나 이상 공개 확인됨 |
| 담당자 역할 적합성 | 10 | 구매·상품개발·브랜드·유통 의사결정 역할이 공개 확인됨 |
| 증거 품질·교차검증 | 10 | 독립된 공개 출처 2개 이상이 핵심 사실을 지지함 |
| 접근 가능성·개인화 안전성 | 5 | 공개 업무 채널과 검증 가능한 업무 맥락이 있음 |

판정: `A 80–100` 우선 검증/승인 요청, `B 60–79` 추가 검증 후 초안, `C 40–59` 보류/데이터 보강, `D 0–39` 제외. 단, 증거 품질이 5점 미만이거나 회사 적합성 근거가 없으면 총점과 무관하게 접촉 금지. BELLOON 스킬의 하드스탑(규제·수권·정품·책임 불명, 데이터 신뢰도 <0.70 등)은 점수 보정이 아니라 `D / hold`로 기록한다. 현재 브리핑 후보의 기본 신뢰도 0.65는 자동 접촉 기준 미달이다.

`opportunity_score`는 회사별로 따로 계산한다. 예: 한 회사가 유통에는 85점이지만 PB에는 45점일 수 있다. 레코드에 `score_by_opportunity: {oem_odm: 0, authorized_distribution: 0, pb: 0, own_brand: 0}`를 추가한다.

## 4. 증거·QC 규칙

- 회사 존재, 국가, 사업 유형, 채널, 포트폴리오는 가능한 한 공식 웹사이트와 공개 LinkedIn 회사 페이지를 교차 확인한다.
- "구매 의향", "예산", "한국 브랜드 도입 의사", "수권 가능", "독점"은 공개 회사 설명만으로 주장하지 않는다. 상태는 `미검증 가설`이다.
- 사람의 직함은 최신 공개 프로필에서 확인하고, 회사와의 현재 소속이 불명확하면 사람 레코드를 `unverified`로 둔다.
- 모든 사실 문장 끝에 `[SRC-###]`를 붙인다. 출처 없는 문장은 삭제하거나 `가설`로 명시한다.
- 검색 스니펫 단독 근거는 탐색용이며 A등급·연락 승인에 사용할 수 없다.
- 자동 QC 체크: (1) `record_type`, ID, URL, 조사일 존재 (2) 회사/사람 ID 연결 유효 (3) 각 핵심 주장 출처 존재 (4) 사실/가설 라벨 존재 (5) 점수 항목 합계 100점 이내·근거 기재 (6) 개인 이메일 추정·무단 수집 없음 (7) 금지 표현 없음 (8) 다음 액션과 재검토일 존재.
- 중복 기준: 회사명+국가+웹사이트 도메인. 사람은 LinkedIn URL을 우선 키로 사용한다. 중복 병합 시 원 출처를 버리지 않는다.

## 5. 안전한 개인화 규칙

허용: 공개된 직함·회사 역할, 회사가 공개한 시장/채널/브랜드 카테고리, 최근 공개된 회사의 제품·유통 페이지. 모든 개인화 문구는 해당 출처 URL을 내부 초안에 남긴다.

금지: 사적 생활·추정 성향·나이·가족·사진 기반 판단, 개인 이메일 추정, 연결망을 아는 척하기, 읽음/방문 추적, "당신이 찾고 있다"는 구매 의향 단정, 공개되지 않은 매출·예산·MOQ 추정, 계약 전 `공식 총판/독점/전 세계 수권` 표현, 제조사명·처방 원본·상세 원가·핵심 공급망 공개(NDA 전).

첫 접촉은 회사와 역할에만 초점을 둔다. 이름을 쓸 때는 공개 프로필의 표기와 소속이 확인된 경우에만 사용한다. 불확실하면 `Hello [Company] team` 또는 직함 없는 정중한 호칭을 사용한다. 요청은 하나만 둔다: 15분 적합성 미팅, 포트폴리오 검토, 또는 샘플 검토 중 하나.

## 6. 승인 전 DM 템플릿 (영문 + 한국어 번역)

### A. OEM/ODM — 자사 상표 제조·공동개발

**EN**
> Subject: Korean OEM/ODM skincare for [Company]
>
> Hi [Name/Company] team — I saw that [Company] works with [verified channel/category] in [market]. BELLOON supports Korean skincare OEM/ODM projects, from concept and sampling to export documentation. We can start with 3–5 SKUs and discuss target cost, MOQ, lead time, and the regulatory responsibilities for [market]. Would a 15-minute fit call or a review of a short capability sheet be useful?

**KO**
> 제목: [회사]를 위한 한국 스킨케어 OEM/ODM 제안
>
> 안녕하세요 [이름/회사] 팀, [회사]가 [시장]에서 [확인된 채널/카테고리]를 운영하는 내용을 확인했습니다. BELLOON은 제품 콘셉트·샘플·수출서류까지 한국 스킨케어 OEM/ODM 프로젝트를 지원합니다. 우선 3~5개 SKU 기준으로 목표 원가, MOQ, 납기 및 [시장]의 규제 책임 범위를 논의할 수 있습니다. 15분 적합성 미팅 또는 간단한 역량 자료 검토가 가능하실까요?

### B. Authorized distribution — 한국 브랜드 수권 유통

**EN**
> Subject: Korean skincare portfolio for [Company]’s [market/channel]
>
> Hi [Name/Company] team — your public portfolio shows [verified category/channel]. BELLOON is exploring non-exclusive, market-specific introductions of selected Korean skincare brands. We would first like to understand your channels, registration/importer setup, and brand-fit criteria—not propose exclusivity before those points are verified. Would a portfolio-fit discussion be appropriate?

**KO**
> 제목: [회사]의 [시장/채널]을 위한 한국 스킨케어 포트폴리오
>
> 안녕하세요 [이름/회사] 팀, 공개된 포트폴리오에서 [확인된 카테고리/채널]을 확인했습니다. BELLOON은 일부 한국 스킨케어 브랜드의 국가·채널별 비독점 도입 가능성을 검토하고 있습니다. 우선 귀사의 채널, 수입자·제품등록 체계, 브랜드 선정 기준을 이해하고 싶으며, 확인 전 독점권을 제안하려는 것은 아닙니다. 포트폴리오 적합성 논의가 가능하실까요?

### C. PB — 자체상표 소량 검증

**EN**
> Subject: Small-batch Korean PB skincare test
>
> Hi [Name/Company] team — [verified fact about the company’s channel/customer] suggests a possible fit for a small Korean PB test. BELLOON can scope 1–3 concepts with samples, MOQ, target wholesale economics, and a defined test period. We would validate product, compliance, and loss limits before any production decision. May I send a one-page concept outline for review?

**KO**
> 제목: 소량 검증형 한국 PB 스킨케어 제안
>
> 안녕하세요 [이름/회사] 팀, [회사의 채널/고객에 관한 확인 사실]을 보면 소량 한국 PB 테스트와의 적합성을 검토해 볼 수 있을 것 같습니다. BELLOON은 1~3개 콘셉트의 샘플, MOQ, 목표 도매 수익성, 명확한 테스트 기간을 함께 설계할 수 있습니다. 생산 결정 전 제품·규제·손실 상한을 먼저 검증합니다. 1페이지 콘셉트 개요를 보내 검토받아도 될까요?

### D. Own-brand opportunity — BELLOON 자체 브랜드 협업/유통

**EN**
> Subject: Korean beauty collaboration for [Company]
>
> Hi [Name/Company] team — based on [verified category/market/channel], I wondered whether a focused Korean beauty collaboration could complement your current offer. BELLOON develops differentiated concepts and would begin with a limited validation, not a broad launch or exclusivity claim. If relevant, would you prefer a short market-fit call or a product concept review?

**KO**
> 제목: [회사]와의 한국 뷰티 협업 검토
>
> 안녕하세요 [이름/회사] 팀, [확인된 카테고리/시장/채널]을 바탕으로 현재 제안에 집중형 한국 뷰티 협업을 더할 수 있을지 검토해 보고 싶습니다. BELLOON은 차별화된 콘셉트를 개발하며, 대규모 출시나 독점 주장이 아니라 제한적 검증부터 시작합니다. 관련성이 있다면 시장 적합성 미팅과 제품 콘셉트 검토 중 어느 쪽이 편하실까요?

초안에는 `personalization_source_ids`, `approval_status: pending`, `do_not_send: true`, `target_action`, `created_at`을 포함한다. 자동화는 초안 생성·중복 제거·QC 리포트까지만 허용한다.

## 7. 볼트 파일 구조 및 정확한 섹션

현재 볼트에는 `research/`, `plans/`, `market/`, `07-project-tracker.md`, `04-decision-log.md`가 있으나 리드 전용 폴더는 없다. 다음을 새로 만든다.

```text
business-wiki/
├── sales/belloon-linkedin/
│   ├── README.md
│   ├── company-leads/<lead-id>-<slug>.md
│   ├── people-leads/<person-id>-<slug>.md
│   ├── opportunities/<lead-id>-<type>.md
│   ├── message-drafts/<draft-id>-<person-id>.md
│   ├── follow-ups.md
│   └── qc-log.md
└── research/belloon-linkedin-sourcing-YYYY-MM-DD.md
```

- `README.md`: 상태값, 스키마, 점수표, 승인 권한, 금지 표현, 링크 규칙.
- `company-leads/`: frontmatter + `확인된 사실 / 미확인·검증 필요 / 기회 가설 / 점수 근거 / 리스크·하드스탑 / 다음 검증 액션 / 출처`.
- `people-leads/`: frontmatter + `확인된 공개 사실 / 역할 적합성 / 개인화에 사용할 사실 / 사용 금지 추정 / 출처`.
- `opportunities/`: 회사 하나의 기회 유형별로 `가설 / 필요한 상업정보 / Gate 0~2 질문 / 경제성 입력 / 다음 단계`를 분리한다. OEM/ODM과 수권 유통을 한 레코드에서 섞지 않는다.
- `message-drafts/`: `목표 / 수신자 ID / 기회 유형 / 개인화 근거 / 영어 원문 / 한국어 번역 / 요청 행동 1개 / 금지·민감정보 점검 / 승인 상태 / 발송 기록`.
- `follow-ups.md`: 한 행에 한 접촉 시도. `followup_id | company_id | person_id | opportunity | draft_id | status | last_action | next_action | next_due(절대날짜) | owner | approval | outcome | source_ids`.
- `qc-log.md`: `run_id | run_date | agent | records_checked | errors | duplicates | unsupported_claims | unsafe_personalization | disposition | reviewer` 및 수정 이력.
- `research/`: 날짜별 원자료·검색 범위·신뢰도 0.65를 보존하고, 정규 레코드에서 링크한다.
- `07-project-tracker.md`: 실제 승인된 검증·미팅·샘플 등 실행 항목만 추가한다. 담당자·절대 마감일·KPI·중단 조건을 필수로 한다.
- `04-decision-log.md`: 대표의 접촉 승인, 보류, 등급 변경, 독점/수권/규제 판단을 날짜·근거·결정자와 기록한다.
- `plans/contracts.md`: 계약서 확인 사항만 기록하며 미확인은 계속 `미확인`으로 둔다.

### 권장 follow-up 상태

`not_approved → approved_to_draft → draft_ready → approved_to_contact → contacted → replied → meeting_scheduled → qualified → sample_or_data_requested → nurture → disqualified`. 각 변경은 날짜·담당자·근거를 남긴다. `contacted`는 실제 발송 후에만 사용할 수 있다.

## 8. 최초 후보 적용 순서

Najafi Cosmetics, Multiplex International LLC, Beauty Solutions Trading부터 공식 웹사이트·LinkedIn 회사 페이지를 교차검증한다. 이어서 공개된 `Distributor / Importer / Brand Manager / Purchasing / Product Development` 역할을 확인한다. 현재 브리핑 신뢰도 0.65와 구매 의향 미검증 상태에서는 모두 `company_verified` 또는 `person_needed`까지만 두고 `approved_to_contact`로 올리지 않는다.

> 외부 발송·연결·계약·결제는 이 문서만으로 승인되지 않는다.
