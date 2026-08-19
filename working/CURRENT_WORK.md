# Current Work

- Repository: `https://github.com/jintonic1010/miracle_company_private`
- Updated: 2026-08-19
- Authority: current progress/discussion, not automatically official requirements

이 파일은 회사에서 **현재 실제로 진행·협의 중인 업무 전체의 최신판**이다. 부서별 자동 분류를 강제하지 않는다.

`/업무공유`는 기존 내용을 읽고 새 내용·수정·삭제·보류·완료를 반영해 **파일 전체를 최신 상태로 다시 정리**한다. 단, 같은 대화에서 직전 `/업무검토`가 `PASS / 공유 가능`이어야 한다.

## 진행 중

### 회사 OS 설계 및 대표님 보고 준비
- n8n을 회사 전체 OS의 뼈대로 두는 구조 정리 중.
- ERP/재고·물류, 시장리서치, 마케팅, CS, 세무·법률을 회사 부서 모듈로 연결하는 방향.
- 대표님과 관리자 ChatGPT가 같은 회사 기준과 진행상황을 공유할 수 있는 저장소/소스 구조를 구축 중.
- LLM 읽기 범위를 공식 소스 + CURRENT_WORK 중심으로 제한하고 원본·미반영 기록은 필요할 때만 읽도록 정리 중.

### ERP / API 연동
- ERPNext와 InvenTree 중 최종 선택 필요.
- Cafe24, Naver SmartStore, Google 관련 API, 해외 공급처 API의 정확한 IN/OUT 및 이벤트 범위 조사 필요.
- ERP 개발자와 n8n/API 개발자가 사용할 공통 식별자 및 데이터 계약 정의 필요.

### 마케팅 AI 이미지 생성 프리랜서 채용 / Virtual Try-On Pipeline 구축
- 마케팅팀에서 **AI Image Generation / ComfyUI / Virtual Try-On 전문 역할**을 초기 프리랜서 형태로 구성하는 진행안.
- 목적은 완성 이미지 몇 장을 외주 납품받는 것이 아니라, 회사가 반복 실행할 수 있는 **로컬 AI 이미지 생성 환경 + 재사용 가능한 ComfyUI Workflow + 운영/인수인계 자료**를 확보하는 것.
- 기본 처리 흐름은 `고객/모델 이미지 + 실제 상품 이미지 + 선택적 Reference/광고문구 → Virtual Try-On → Identity/Garment Fidelity 보정 → 광고 Creative → Variation 생성`으로 본다.
- 가상피팅 결과는 얼굴·전체 인물 특징을 최대한 유지하고, 실제 상품의 색상·패턴·로고·형태·실루엣 왜곡을 최소화하는 것을 핵심 품질 기준으로 본다.
- 상의뿐 아니라 하의·아우터 등으로 확장 가능한 구조를 검토하며, 특정 상품 하나에 Workflow를 Hard Coding하지 않는 방향.
- ComfyUI 실무 경험은 핵심 필수 조건으로 보며, 단순 Workflow 실행이 아니라 신규 Workflow 설계·수정, Custom Node/Dependency 관리, Debugging, VRAM OOM 및 CUDA 관련 기본 문제 대응이 가능한 인력을 우선한다.
- Local AI 환경은 NVIDIA GPU/CUDA 기반을 전제로 검토하며, Stable Diffusion, FLUX, ControlNet, IP-Adapter, Inpainting, Masking, Segmentation, Pose/Depth Control, LoRA 등은 **확정 기술스택이 아니라 지원자 역량 및 PoC에서 적합성을 판단할 후보 기술**로 둔다.
- 광고 결과물 범위는 SNS 광고, 신상품/프로모션 이미지, 배너, 썸네일, 텍스트 포함 Creative, 동일 상품 Multi-Variation 등을 포함한다.
- 필요 시 Ideogram 등 Typography에 강한 외부 AI 도구를 보조적으로 사용할 수 있으나, 핵심 이미지 생성/VTON Pipeline은 회사가 운영 가능한 형태로 남기는 것을 목표로 한다.
- 최종 인수 대상은 이미지 결과물뿐 아니라 ComfyUI Workflow/JSON, 사용 Model/LoRA/VAE 목록, Custom Node/Dependency 목록, Prompt 구조, 주요 Parameter/Seed 등 재현 정보, 설치·실행·입력 교체·수정·오류 확인·반복 제작 방법 문서를 포함하는 방향.
- 완료 기준은 프리랜서가 빠진 뒤에도 회사 PC에서 Workflow를 불러오고 `person_image`, `garment_image` 등을 회사가 직접 교체해 기본 반복 생성을 수행할 수 있는 상태로 본다.
- 향후 확장 구조는 `ERP/상품 데이터 소스 → n8n 또는 Generation Queue → ComfyUI API/이미지 생성 엔진 → Generated Assets → Marketing System` 방향으로 검토한다. ERP는 상품 운영 데이터 기준 원장, n8n은 연결/자동화, ComfyUI는 이미지 생성 엔진 역할을 유지한다.
- 본계약 전 소규모 PoC를 활용할 수 있다. 예시 입력은 모델/고객 사진 1장 + 의류 상품 사진 1~2장 + 광고 목적/문구이며, Virtual Try-On 결과, 광고 Creative, Style Variation, Workflow 구조/모델/주요 생성 방식 설명을 평가한다.
- 지원자 우선 선별은 ComfyUI Workflow 직접 설계 능력, Virtual Try-On/의류 합성 실결과, Local AI 환경 구축 능력, Identity/Garment Fidelity, 광고 Creative 완성도, Workflow 전체 인수인계 가능 여부 순으로 본다.
- 실제 고객 사진·개인정보·운영 DB·인증정보는 GitHub 업무 기록에 저장하지 않는다.

### 마케팅 운영 / 퍼포먼스 인력
- 광고비 집행, Meta/Google 광고 운영, ROAS 분석 등 퍼포먼스 마케팅 업무는 위 AI 이미지 생성 역할의 범위에서 제외하고 별도 역할로 구성하는 방향.
- CRM, 커머스, ERP의 고객·상품·재고·매출 데이터를 활용하는 마케팅 운영 역할도 별도 인력 구성 범위로 계속 검토한다.
- 구체적인 직무명, 경력, 인원 구성, 채용 순서는 아직 확정하지 않음.

## 최근 확정된 운영 방식

- 회사 진행·협의 업무는 부서별 파일로 자동 분류하지 않고 `working/CURRENT_WORK.md` 하나의 최신판으로 관리한다.
- 대표님과 관리자 모두 `/업무검토`와 `/업무공유`를 사용할 수 있다.
- 업무공유 전에는 최신 `main`의 회사 공식 방향·확정 요구사항·CURRENT_WORK를 기준으로 `/업무검토`를 수행한다.
- `/업무검토`가 `PASS / 공유 가능`인 경우에만 `/업무공유`한다.
- 검토 PASS는 공식 요구사항 확정이 아니라 현재 업무판에 공유 가능하다는 의미다.
- 공식 회사 기준으로 승격하는 것은 관리자 `/업무확정`만 가능하다.
- 기존 확정안을 바꾸는 경우도 먼저 변경안을 업무검토 → 업무공유로 CURRENT_WORK에 올린 후 관리자 업무확정으로 교체한다.

## 협의 중 요구사항 후보

- ERP/API 구현 상세 범위와 우선순위.
- AI 이미지 생성 프리랜서의 실제 채용 조건, 계약 범위, 비용, 작업 기간 및 수정 범위.
- Virtual Try-On PoC에서 사용할 구체 모델/Workflow 조합과 품질 합격 기준의 수치화 여부.
- AI 이미지 Pipeline의 ComfyUI API/Batch/Queue/n8n 연동 상세 범위와 구현 시점.
- 퍼포먼스/CRM 마케팅 담당 인력의 구체적 직무·경력·인원 구성 및 채용 순서.
- 외부 판매·공급 채널별 실제 API 권한과 데이터 계약.

## 결정 대기

- ERPNext vs InvenTree
- 각 외부 API의 실제 읽기/쓰기/Webhook 범위
- AI 이미지 생성 프리랜서의 최종 계약 대상 및 PoC 결과
- Virtual Try-On/광고 이미지 제작에 사용할 최종 Model/Workflow 구성
- 퍼포먼스/CRM 마케팅 담당 인력의 구체적 직무·채용 기준

## 답변 규칙

이 파일의 내용은 `진행 중` 또는 `협의 중`으로 표현한다. `llm-source/`와 충돌하면 다음처럼 구분한다.

- `현재 확정 기준`: `llm-source/`
- `현재 협의/진행 중`: 이 파일

미반영 아이디어·문제는 사용자가 명시적으로 요청하지 않는 한 현재 결론에 자동 혼합하지 않는다.
