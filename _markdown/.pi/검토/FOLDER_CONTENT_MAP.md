---
source_path: ".pi/검토/FOLDER_CONTENT_MAP.md"
source_filename: "FOLDER_CONTENT_MAP.md"
source_type: "text"
source_size_bytes: 17633
source_modified_at: "2026-08-17T18:38:52+09:00"
source_sha256: "96d61bb8439aa0a5cce1af079329a51a7427e32861762c0ec9c9b702b44f5444"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 폴더별 실제 내용 지도

## BusinessVault/

### 이 폴더에는 무엇이 있나

Premium MultiShop과 BELLOON의 사업 아이디어, 시장조사, 사업모델 검토, AI·데이터 설계, 의사결정, 실행 추적을 모은 Obsidian 볼트다. 85개 파일 중 사람이 읽는 Markdown은 60개이고 나머지는 Obsidian·TaskNotes·Syncthing 운영 파일이다.

### 대표적인 파일

- `BusinessVault/index.md`
- `BusinessVault/04-decision-log.md`
- `BusinessVault/07-project-tracker.md`
- `BusinessVault/plans/pms-revenue-commerce-os-v3-canonical-2026-08-16.md`
- `BusinessVault/research/premium-multishop-market-scan-2026-08-13.md`

### 실제 내용의 특징

사업 이름, 조사일·기준일, 상태, 검증 한계, 승인 조건, 표와 위키링크가 자주 사용된다. Premium MultiShop 자료가 대부분이며 BELLOON은 해외 바이어와 화장품 B2B 중심이다. 현재 정본, 설계안, 검토 보고서, 실행 기록이 같은 계층에 공존한다.

### 현재 이 위치가 적절한가

애매함

### 이유

사업 지식 볼트라는 큰 경계는 좋지만 내부에서 사업, 문서 역할, 현재성의 우선순위가 충분히 드러나지 않는다.

## BusinessVault/research/

### 이 폴더에는 무엇이 있나

9개의 조사 문서가 있다. BELLOON 바이어 회사·인물 후보와 LinkedIn 소싱 운영 표준, Premium MultiShop 시장 수요·경쟁사·KREAM·해외 공급망·네이버 블로그 수익모델을 다룬다.

### 대표적인 파일

- `BusinessVault/research/belloon-buyer-sourcing-2026-08-12.md`
- `BusinessVault/research/belloon-buyer-person-sourcing-2026-08-12.md`
- `BusinessVault/research/premium-multishop-competitor-benchmark-2026-08-13.md`
- `BusinessVault/research/premium-multishop-sourcing-landscape-2026-08-13.md`

### 실제 내용의 특징

공개 출처, 조사일, 불확실성, 후보 등급, 표, 출처 목록을 보존한다. 일부는 조사 결과이고 `belloon-linkedin-sourcing-ops.md`는 리드 스키마·점수표·메시지 템플릿까지 포함한 운영 표준이다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

근거 조사와 운영 절차가 섞여 있다. 조사 보고서는 유지하되 운영 표준은 BELLOON의 `reference-and-templates/` 또는 `execution/`으로 분리하는 편이 의미상 맞다.

## BusinessVault/plans/

### 이 폴더에는 무엇이 있나

33개 Markdown으로 가장 큰 문서군이다. Premium MultiShop의 커머스 OS, 데이터맵, 9-Agent 구조, 수익 사다리, 자동화, 공급·Cafe24 연동, 상세페이지, SEO, 성장 로드맵, 사업모델 수익성 검토와 BELLOON 집중 결정, 계약 현황이 함께 있다.

### 대표적인 파일

- `BusinessVault/plans/pms-revenue-commerce-os-v3-canonical-2026-08-16.md`
- `BusinessVault/plans/pms-queryable-data-map-v1-2026-08-15.md`
- `BusinessVault/plans/premium-multishop-90-180-growth-roadmap-2026-08-15.md`
- `BusinessVault/plans/premium-multishop-resale-arbitrage-profitability-review-2026-08-16.md`
- `BusinessVault/plans/contracts.md`

### 실제 내용의 특징

설계 문서는 목적·비목표·데이터·승인·중단 조건이 잘 구조화되어 있다. 반면 `review`, `audit`, `decision`, `master-prompt`, `contracts`가 모두 `plans`로 분류돼 실제 역할이 다르다. v1·v2·v3·canonical 버전군이 있지만 `supersedes` 관계는 없다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

`plans`가 사실상 모든 비리서치 문서를 받는 잡다한 상자가 됐다. 결정, 검토, 설계, 실행, 템플릿, 계약을 구분해야 현재 정본을 찾기 쉽다.

## BusinessVault/ideas/

### 이 폴더에는 무엇이 있나

BELLOON과 Premium MultiShop의 검증 전 아이디어와 인덱스가 있다. 각 사업에 대해 `ideas/belloon.md`와 `ideas/belloon/index.md`처럼 한 단계가 중복된다.

### 대표적인 파일

- `BusinessVault/ideas/belloon.md`
- `BusinessVault/ideas/belloon/index.md`
- `BusinessVault/ideas/premium-multishop.md`

### 실제 내용의 특징

사업 범위, 아이디어 묶음, 다음 검증 질문이 짧게 정리되어 있다. 검증 전 아이디어를 실행 확정으로 보지 말라는 규칙이 명확하다.

### 현재 이 위치가 적절한가

애매함

### 이유

아이디어 분리는 좋지만 파일과 동명 하위 폴더가 겹쳐 탐색이 불필요하게 두 단계다. 사업별 `ideas.md` 하나 또는 사업 폴더 안 `ideas/` 중 하나만 택하면 된다.

## BusinessVault/market/

### 이 폴더에는 무엇이 있나

사업별 시장 자료 자체보다 `research/`의 원자료를 연결하고 활용 맥락을 요약하는 인덱스 5개가 있다.

### 대표적인 파일

- `BusinessVault/market/belloon.md`
- `BusinessVault/market/belloon/index.md`
- `BusinessVault/market/premium-multishop.md`

### 실제 내용의 특징

원자료를 복제하지 않고 위키링크로 연결한다는 의도는 좋다. 다만 `market/premium-multishop/index.md`는 별도 시장 리서치가 없다고 적는데 `research/`에는 시장 스캔·경쟁사·공급망 자료가 이미 있다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

`market`은 독립 콘텐츠 폴더가 아니라 인덱스·요약 계층이다. 각 사업의 `evidence-and-research/index.md`로 통합하는 편이 간단하고 최신성 관리가 쉽다.

## BusinessVault/_archiv/ 및 BusinessVault/_archive/

### 이 폴더에는 무엇이 있나

`_archiv/`에는 보관 정책 안내와 빈 목록이 있고 `_archive/`는 비어 있다.

### 대표적인 파일

- `BusinessVault/_archiv/README.md`
- `BusinessVault/_archiv/index.md`

### 실제 내용의 특징

임의 이동·삭제 금지와 승인 후 보관 원칙이 적혀 있다. 실제 보관 문서는 아직 없다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

동일 목적의 철자가 다른 폴더가 둘이다. 표준 이름을 하나로 결정해야 한다. 현재 파일은 보관 정책이므로 유지 가치가 있다.

## BusinessVault/TaskNotes/ 및 BusinessVault/.obsidian/

### 이 폴더에는 무엇이 있나

TaskNotes 안내 문서와 7개 `.base` 뷰, Obsidian 설정, Dataview·Tasks·TaskNotes 플러그인 코드가 있다.

### 대표적인 파일

- `BusinessVault/TaskNotes/Start Here.md`
- `BusinessVault/TaskNotes/Views/tasks-default.base`
- `BusinessVault/.obsidian/plugins/tasknotes/data.json`

### 실제 내용의 특징

사용자 사업 지식이 아니라 앱 기능을 위한 설정·템플릿·플러그인 번들이다. `HermesWiki/`의 대응 파일과 대부분 정확히 같다.

### 현재 이 위치가 적절한가

적절함

### 이유

Obsidian 볼트의 휴대성과 동작을 위해 볼트 안에 둘 수 있다. 다만 AI 코퍼스 색인에서는 제외해야 한다.

## BusinessVault 루트의 개별 파일

### 이 폴더에는 무엇이 있나

볼트 인덱스, 전체 결정 로그, 프로젝트 추적기, 빈 날짜 노트, 빈 무제 노트가 있다.

### 대표적인 파일

- `BusinessVault/04-decision-log.md`
- `BusinessVault/07-project-tracker.md`
- `BusinessVault/2026-08-14.md`
- `BusinessVault/무제.md`

### 실제 내용의 특징

결정 로그는 여러 사업·주제의 결정을 모으지만 첫 H2 아래에 다수 결정이 헤딩 없이 이어진다. 프로젝트 추적기는 진행·대기·완료 상태와 연결 문서를 모은다. 두 빈 파일은 내용이 없다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

전역 인덱스와 추적기는 루트에 둘 수 있지만, 결정은 사업별·결정별 식별자가 필요하다. 빈 날짜 노트는 개인 일지와 혼동될 가능성이 높다.

## HermesWiki/

### 이 폴더에는 무엇이 있나

개인 세컨브레인과 일일기록용 Obsidian 볼트다. 34개 파일 중 실제 사용자 Markdown은 인덱스, 변경 로그, 일일기록 6개다.

### 대표적인 파일

- `HermesWiki/index.md`
- `HermesWiki/log.md`
- `HermesWiki/journal/2026-08/2026-08-16.md`

### 실제 내용의 특징

사업 활동과 의사결정을 날짜별로 다시 요약한다. 사업 원문을 복사하기보다 `business-wiki/...` 링크로 연결하려는 구조다.

### 현재 이 위치가 적절한가

적절함

### 이유

사업 볼트와 개인·시간 기록을 분리한 큰 경계는 매우 좋다. 다만 실제 폴더명과 인덱스의 안내가 일치해야 한다.

## HermesWiki/journal/2026-08/

### 이 폴더에는 무엇이 있나

2026-08-11부터 2026-08-16까지 날짜별 일일기록 6개가 있다.

### 대표적인 파일

- `HermesWiki/journal/2026-08/2026-08-12.md`
- `HermesWiki/journal/2026-08/2026-08-15.md`

### 실제 내용의 특징

모든 파일이 `title`, `created`, `type`, `tags`, `mood` YAML을 갖고 `하루의 흐름`, `결정`, `진행`, `감상·상태`, `대화 하이라이트`, `내일 할 일` 순서를 따른다. 날짜별 1파일 원칙과 헤딩이 잘 유지된다.

### 현재 이 위치가 적절한가

애매함

### 이유

내용 구조는 좋지만 `HermesWiki/index.md`와 설치 스킬은 `logs/YYYY-MM/`를 표준으로 안내한다. `journal/`을 표준으로 삼을지 `logs/`로 맞출지 결정해야 한다.

## HermesWiki/inbox, profile, logs, areas, projects, concepts, _archive

### 이 폴더에는 무엇이 있나

현재 모두 비어 있다. 인덱스가 향후 개인 지식 분류를 위해 예약한 영역이다.

### 대표적인 파일

- 없음

### 실제 내용의 특징

폴더 이름만 있고 각 폴더의 `index.md`나 설명 파일은 없다. `HermesWiki/index.md`의 위키링크는 파일 링크로는 해석되지 않는다.

### 현재 이 위치가 적절한가

애매함

### 이유

분류 의도는 명확하지만 실제 콘텐츠와 운영 규칙이 없다. 빈 예약 폴더를 유지할지, 내용이 생길 때 만들지 결정하면 된다.

## HermesWiki/TaskNotes/ 및 HermesWiki/.obsidian/

### 이 폴더에는 무엇이 있나

BusinessVault와 같은 TaskNotes 안내·뷰와 같은 플러그인 번들이 있다.

### 대표적인 파일

- `HermesWiki/TaskNotes/Start Here.md`
- `HermesWiki/.obsidian/plugins/tasknotes/main.js`

### 실제 내용의 특징

기본 파일 대부분이 두 볼트에서 바이트 단위로 동일하다. 볼트 기능용이지 개인 지식 본문이 아니다.

### 현재 이 위치가 적절한가

적절함

### 이유

각 볼트가 독립적으로 열리게 하는 선택이다. 코퍼스 중복으로 취급해 삭제하기보다 색인 제외 규칙을 두는 것이 안전하다.

## .agents/

### 이 폴더에는 무엇이 있나

SEO, 글쓰기, 카피라이팅, LinkedIn, X, TikTok, Reddit, YouTube 등 마케팅·콘텐츠 스킬 21개와 설치 잠금 파일이 있다.

### 대표적인 파일

- `.agents/.skill-lock.json`
- `.agents/skills/programmatic-seo/SKILL.md`
- `.agents/skills/gtm-positioning-strategy/SKILL.md`

### 실제 내용의 특징

각 `SKILL.md`는 YAML `name`, `description`과 실행 지침을 가진다. 잠금 파일에는 로컬 설치 출처, 설치일, 폴더 해시가 있다. 사업 사실 자료가 아니라 AI 행동 지침이다.

### 현재 이 위치가 적절한가

적절함

### 이유

에이전트 운영 자산으로는 적절하다. 사업 코퍼스와 같은 검색 인덱스에 넣으면 일반 지침이 사업의 사실처럼 검색될 수 있으므로 별도 색인이 필요하다.

## 다수의 비어 있는 에이전트 대상 폴더

### 이 폴더에는 무엇이 있나

`.adal/`, `.aider-desk/`, `.augment/`, `.continue/`, `.roo/`, `.qwen/` 등 49개 최상위 디렉터리가 비어 있다. 대부분 `skills/` 하위 폴더만 예약되어 있다.

### 대표적인 파일

- 없음

### 실제 내용의 특징

내용이 없고 코퍼스 역할도 없다. `.agents/.skill-lock.json`의 스킬 설치 구조와 시점이 비슷해 여러 코딩 에이전트용 배포 대상 자리로 추정되지만 정확한 생성 도구는 `Needs verification`이다.

### 현재 이 위치가 적절한가

애매함

### 이유

활성 도구가 사용한다면 유지해야 하지만, 문서 컬렉션 탐색에는 잡음이다. 감사 후 별도 운영 루트로 분리할 후보이며 즉시 삭제 대상은 아니다.

## .claude/

### 이 폴더에는 무엇이 있나

Claude 대화 JSONL, 하위 에이전트 기록, 작업 상태 JSON, 메모리 Markdown, 셸 스냅샷, 백업 설정, 자격증명 파일, Hermes 설치 스킬이 섞여 있다.

### 대표적인 파일

- `.claude/projects/.../*.jsonl`
- `.claude/tasks/.../7.json`
- `.claude/skills/hermes-vps-setup/SKILL.md`

### 실제 내용의 특징

JSONL은 사용자·assistant·tool result·attachment 등 대화 이벤트 원장이다. 작업 기록에는 BusinessVault의 결정 로그와 프로젝트 추적기 스캐폴드 작업이 명시되어 있어 생성 이력 증거가 된다. 동시에 개인 대화와 도구 출력이 포함될 수 있어 일반 코퍼스로 색인하면 안 된다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

설치 스킬 패키지는 재사용 자산이지만, 대화 이력·자격증명·백업은 민감한 런타임 상태다. 같은 `.claude/` 내부라도 보존·색인 정책이 달라야 한다.

## .claude/skills/hermes-vps-setup/

### 이 폴더에는 무엇이 있나

Hermes VPS 설치용 `SKILL.md`, 사용자 안내, 설정 템플릿, 9개 셸/Python 스크립트, 9페이지 PDF 가이드가 있다.

### 대표적인 파일

- `.claude/skills/hermes-vps-setup/SKILL.md`
- `.claude/skills/hermes-vps-setup/scripts/03-server-syncthing.sh`
- `.claude/skills/hermes-vps-setup/헤르메스_에이전트_설치_가이드.pdf`

### 실제 내용의 특징

SSH, 환경 설정, Syncthing, Obsidian 위키 스캐폴드, 검증 순서를 가진 실행 패키지다. `logs/YYYY-MM/` 경로 규칙을 직접 정의한다. `setup.env`는 비밀값을 담을 가능성이 있어 코퍼스 제외가 필수다.

### 현재 이 위치가 적절한가

적절함

### 이유

스킬·스크립트·가이드는 한 패키지로 같이 유지해야 재현 가능하다. 단, 채워진 환경 파일은 패키지와 논리적으로 분리해 비밀 저장소에서 관리해야 한다.

## Claude/

### 이 폴더에는 무엇이 있나

Premium MultiShop 관련 DOCX 보고서 1개, HTML 아키텍처 1개, 썸네일 PNG 1개가 있다.

### 대표적인 파일

- `Claude/Projects/premium-multishop-website/PremiumMultiShop_벤치마킹_개선전략_2026_v2.docx`
- `Claude/Artifacts/premium-multishop-sourcing-architecture/index.html`

### 실제 내용의 특징

DOCX는 2026-06-08 상세페이지 벤치마크·문제 진단·즉시 실행안·제품 설명 초안을 담는다. HTML은 홍콩 보세창고, EU API 구매대행, 현지 드롭십핑 모델과 면세 라우팅을 시각화한다. 둘 다 이후 `BusinessVault/` 문서와 주제가 겹치지만 현재 정본인지 명시되지 않았다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

생성 도구 기준 폴더라 사업 맥락에서 찾기 어렵다. Premium MultiShop의 `source-artifacts/` 또는 `history/`로 개념상 연결하고 현재성·법률 검증 상태를 표시해야 한다.

## .cache/

### 이 폴더에는 무엇이 있나

octorunner용 Chromium 119 실행 번들 86개, 약 535MB가 있다.

### 대표적인 파일

- `.cache/octorunner/chromium/.../chrome.exe`
- `.cache/octorunner/chromium/.../chrome.dll`

### 실제 내용의 특징

실행 파일, DLL, locale PAK, 리소스 파일이다. 문서 코퍼스가 아니다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

캐시로서는 정상일 수 있지만 외부 텍스트 코퍼스 루트에는 포함되면 안 된다. AI 색인·백업·문서 통계에서 제외한다.

## .hermes-sync/

### 이 폴더에는 무엇이 있나

Syncthing 실행 파일, 인증서·키, 설정 XML, 로그, 임시 파일이 있다.

### 대표적인 파일

- `.hermes-sync/bin/syncthing.exe`
- `.hermes-sync/home/config.xml`
- `.hermes-sync/home/key.pem`

### 실제 내용의 특징

동기화 런타임 상태다. 개인키와 장치 식별 정보가 포함될 수 있다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

코퍼스와 분리하고 절대 AI 색인하지 않아야 한다. 볼트 내부의 `.stfolder`·`.stignore`만 동기화 경계 증거로 남기면 된다.

## .ssh/

### 이 폴더에는 무엇이 있나

SSH 개인키·공개키·설정·known_hosts가 있다.

### 대표적인 파일

- `.ssh/id_ed25519`
- `.ssh/config`

### 실제 내용의 특징

문서가 아니라 보안 자격증명과 접속 상태다. 내용은 감사에서 읽지 않았다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

코퍼스 루트에 존재하는 것 자체가 가장 큰 보안 경계 문제다. 검색·동기화·공유 대상에서 명시적으로 제외해야 한다.

## Intel/, Favorites/, dwhelper/

### 이 폴더에는 무엇이 있나

Intel 드라이버 설치 로그, Windows 즐겨찾기 시스템 파일, 빈 보조 폴더다.

### 대표적인 파일

- `Intel/Logs/IntelME_MSI.log`
- `Favorites/Bing.url`

### 실제 내용의 특징

일부 로그는 UTF-8이 아니며 사업이나 개인 지식과 무관하다.

### 현재 이 위치가 적절한가

재분류 권장

### 이유

운영체제 잔여물이며 코퍼스에서 제외해야 한다.

