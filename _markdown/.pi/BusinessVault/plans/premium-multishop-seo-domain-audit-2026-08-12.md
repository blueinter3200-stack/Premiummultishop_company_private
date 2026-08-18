---
source_path: ".pi/BusinessVault/plans/premium-multishop-seo-domain-audit-2026-08-12.md"
source_filename: "premium-multishop-seo-domain-audit-2026-08-12.md"
source_type: "text"
source_size_bytes: 10125
source_modified_at: "2026-08-13T14:05:29+09:00"
source_sha256: "e0405a87a44dfe649463f5163635d9ca836b07b6e6d7c9476432cbcc41b911d5"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# Premium MultiShop SEO·도메인 기술감사 및 관리자 실행안

> 범위: Premium MultiShop만. BELLOON 자료·도메인은 포함하지 않는다.
> 기준일: 2026-08-12. 공개 HTTP/HTML은 이 날짜에 재조회했다.

## 1. 한 줄 결론

공개 웹에서 직접 수정 가능한 리소스는 확인되지 않아 변경을 실행할 수 없었다. 다만 대표 도메인 canonical은 동작 중이고, `blue3200.cafe24.com`·`m.premiummultishop.com`·`www`의 공개 정규화와 오래된/없는 상품 URL 처리는 **권한 필요** 항목으로 분리해 Cafe24 관리자에서 적용해야 한다.

## 2. 확인된 공개 상태

| 검사 | 결과 | 판정 |
|---|---|---|
| `https://premiummultishop.com/` | HTTP 200, 최종 URL 동일, `<title>프리미엄멀티샵</title>`, canonical `https://premiummultishop.com/` | 정상(홈 기준) |
| `https://www.premiummultishop.com/` | HTTP 200, `www`가 비-www로 301/308 정규화되지 않음 | 권한 필요: 대표 도메인 강제 필요 |
| `https://blue3200.cafe24.com/` | HTTP 200, 기본 도메인이 살아 있고 HTML 제공 | 권한 필요: 기본 도메인 외부 공개 차단/대표 도메인 리다이렉트 필요 |
| `https://m.premiummultishop.com/` | HTTP 302 → `https://premiummultishop.com` | 부분 정상: 모바일 검색 잔존 방지를 위한 일관된 영구 정규화 재확인 필요 |
| `http://premiummultishop.com/` | HTTPS로 이동하지만 공개 헤더만으로 301 여부는 이 감사에서 확정하지 않음 | 권한 필요: HTTP→HTTPS 301 확인 |
| `robots.txt` | HTTP 200. `/admin`, `/api`, 주문/회원 등 차단. `Sitemap: https://premiummultishop.com/sitemap.xml`은 bingbot 블록에만 존재 | 개선 필요: Sitemap 선언을 전역 `User-agent: *` 아래로 이동 권장 |
| `sitemap.xml` | HTTP 200, 약 2,229 URL / 상품 URL 약 1,821개. 종료 이벤트·오래된 카테고리도 포함 | 권한 필요: 색인 가치 낮은 URL 정리 및 재생성 |
| 존재하지 않는 상품 URL | `https://premiummultishop.com/product/nonexistent-seo-audit/999999/`에서 HTTP 302 → 홈 | 문제 확인: 404/410 대신 soft redirect. 검색엔진에 잘못된 대체 페이지 신호 |
| 검색 URL | `/search.html?query=moncler`에서 HTTP 302 → 홈 | 문제 확인: 검색 결과 URL의 명시적 noindex 또는 410/적절한 차단 정책 필요 |
| 파라미터 URL | `/?sort=recent`, `/?foo=bar`는 HTTP 200, canonical은 홈 | canonical은 작동. 그러나 robots 차단만으로 색인 제거를 보장하지 않으므로 관리자 noindex 설정/검색콘솔 정리 필요 |
| 상품 canonical/robots | 실제 상품 1건은 HTTP 200, 상품 canonical은 정규 상품 URL, `robots=index,follow` | 개별 상품은 정상. 종료/품절 상품 처리 정책 필요 |
| placeholder | 홈에는 Cafe24 JS 주석과 빈 검색 input `placeholder` 속성이 존재. 상품 HTML에서 템플릿 토큰 1건 탐지(소스 코드 문맥 확인 필요) | 실제 고객 노출 여부 관리자/렌더링 검수 필요 |

## 3. 공개적으로 실행하지 못한 이유

- 공개 HTTP 응답에는 편집/업로드 인터페이스가 없고, `robots.txt`·`sitemap.xml`은 Cafe24가 생성하는 응답이다.
- Cafe24 관리자, DNS/도메인 관리, Google Search Console·네이버 서치어드바이저 권한이 제공되지 않았다.
- 따라서 파일 업로드, DNS 변경, 리다이렉트 규칙, URL 삭제 요청을 추측으로 실행하지 않았다.

## 4. 권한 필요 실행 절차

### A. 대표 도메인·기본/모바일 도메인

1. Cafe24 쇼핑몰 관리자 로그인.
2. **쇼핑몰 설정 → 기본 설정 → 쇼핑몰 정보 → 도메인 설정(또는 도메인 관리)**에서 연결 도메인 목록 확인.
3. `https://premiummultishop.com`을 대표 도메인으로 지정.
4. `blue3200.cafe24.com`, `m.premiummultishop.com`, `www.premiummultishop.com`은 대표 도메인으로 사용하지 않도록 설정하고, 가능하면 대표 도메인으로 301 리다이렉트하는 옵션을 적용.
5. 모바일 도메인이 별도 운영 대상이 아니면 `m.premiummultishop.com`을 PC 대표 도메인으로 301 정규화. 모바일 전용을 유지해야 한다면 모바일 canonical/alternate 정책을 먼저 확정하고 검색 노출용 URL을 하나로 선택.
6. DNS 관리자에서 `www`와 `m`의 A/CNAME 대상이 Cafe24에 연결되어 있는지 확인. DNS 권한이 없으면 도메인 소유자에게 요청.
7. 저장 후 아래 URL을 `curl -I --max-redirs 0`로 재검증: 각 비대표 URL이 대표 URL로 **301/308**, 경로와 query string 보존 여부, 최종 대표 URL의 200.

### B. SEO 메타·canonical·query URL

- 관리자 경로: **쇼핑몰 설정 → 기본 설정 → 쇼핑몰 정보 → 검색엔진 최적화(SEO)**. 사이트명/설명/기본 title을 설정하고 HTML 태그 우선순위를 확인.
- 상품별 경로: **상품관리 → 상품목록 → 상품 등록/수정 → 검색엔진 최적화(SEO)**. 상품명·description·검색 노출 여부를 확인.
- 주요 페이지/스킨 코드에 canonical이 중복 삽입되지 않도록 `<head>`에서 canonical 1개만 유지.
- 검색 결과·정렬·필터·세션·추적 파라미터 페이지는 `noindex,follow`를 우선 적용(robots.txt만으로 이미 색인된 URL을 제거하지 못함). 구매/회원/장바구니는 기존 차단 유지.
- 저장 후 홈, 상품, `?sort=recent`, 검색 URL에서 title/canonical/robots를 다시 조회.

### C. robots.txt·sitemap

- 관리자 경로(쇼핑몰 버전에 따라 명칭 차이): **쇼핑몰 설정 → 기본 설정 → 검색엔진 최적화(SEO) → robots.txt/검색로봇 설정** 또는 스킨/운영 설정의 robots.txt 편집.
- `Sitemap: https://premiummultishop.com/sitemap.xml`을 전역 `User-agent: *` 그룹에 둔다.
- sitemap에는 200으로 정상 서비스되고 색인할 가치가 있는 대표 URL만 남긴다. 종료 이벤트, 중복/구형 카테고리, 리다이렉트/품절 정책상 색인 제외 상품은 제외.
- 수정 후 `https://premiummultishop.com/robots.txt`, sitemap HTTP 상태와 XML 파싱을 재검증.

### D. 오래된 상품 URL

- 상품이 영구 삭제되어 대체 상품이 없으면 Cafe24 상품 상태를 비공개/삭제한 뒤 해당 URL이 404 또는 410이 되는지 확인한다. 현재처럼 홈 302로 보내지 않는다.
- 명확한 후속 상품이 있는 경우에만 해당 후속 상품으로 301. 무관한 홈 302/301은 금지.
- 관리자에서 개별 URL 리다이렉트 기능이 제공되지 않으면 Cafe24 고객센터/제작 담당자에게 “구 URL → 관련 신상품 301, 대체 없음 → 404/410” 규칙을 요청. 입력값: 구 URL 목록, 대응 신상품 URL(있을 때), 적용일, 기대 상태코드.
- Search Console의 **색인 생성 → 삭제**는 이미 노출된 URL의 임시 제거용이며 근본적인 404/410·301 수정 후 사용한다.

### E. 템플릿 placeholder

- **디자인(스킨) → 편집 → HTML 편집 → 공통 레이아웃(head)/상품 상세**에서 실제 화면에 보이는 토큰을 검색.
- 주석·Cafe24 정상 변수와 고객 노출 토큰을 구분한다. 고객 화면에 출력되는 미치환 변수는 정상 Cafe24 변수로 교체하거나 해당 블록을 삭제.
- 저장 전 스킨 복사/백업, 모바일·PC 각각 미리보기, 홈/카테고리/상품/검색에서 텍스트 노출 재검증.

## 5. Search Console 후속(권한 필요)

1. Google Search Console에서 `https://premiummultishop.com/` 도메인/URL 속성의 소유권 확인.
2. **색인 생성 → 페이지**에서 `m.premiummultishop.com`, `blue3200.cafe24.com`, `www` 및 홈으로 리다이렉트되는 구상품 URL을 샘플링.
3. 대표 도메인·상태코드 수정 후 **사이트맵**에 `https://premiummultishop.com/sitemap.xml` 제출.
4. **URL 검사**에서 대표 홈/상품은 색인 생성 요청, 구 URL은 수정된 404/410 또는 관련 301 확인.
5. 기존 모바일/기본 도메인 URL은 즉시 삭제보다 리다이렉트·canonical·상태코드 수정 후 재크롤을 기다린다.

## 6. 재검증 명령

```bash
curl -I --max-redirs 0 https://blue3200.cafe24.com/
curl -I --max-redirs 0 https://m.premiummultishop.com/
curl -I --max-redirs 0 https://www.premiummultishop.com/
curl -s https://premiummultishop.com/robots.txt
curl -s https://premiummultishop.com/sitemap.xml | xmllint --noout -
```

## 7. 상태

### 7.1 Screaming Frog 1차 점검 결과 (대표님 제공 자료)

- 대상: `https://premiummultishop.com`
- 도구: Screaming Frog SEO Spider 무료 버전
- 검사 범위: 무료 버전 한도 500개 URL
- External URL: 44개
- `blue3200.cafe24.com` 검색 결과: 0건
- **확인된 사실**: 검사된 500개 URL 범위에서는 `premiummultishop.com`에서 `blue3200.cafe24.com`으로 직접 연결되는 링크가 발견되지 않음.
- **범위 제한**: 무료 버전 500개 URL 제한으로 자사몰 전체 페이지에 문제가 없다고 확정할 수 없음.
- **별도 과제**: `blue3200.cafe24.com`으로 직접 접속한 뒤 이후 페이지에서도 해당 호스트가 유지되는 현상은 대표 도메인에서 구 도메인으로 연결되는 링크 여부와 별개인 호스트 정규화 문제임.
- **다음 검증**: 구 도메인 샘플 URL의 HTTP 상태코드·최종 URL·canonical·내부 링크 호스트를 대표 도메인과 비교하고, Search Console·네이버 색인 잔존 여부를 별도 확인함.

- 공개 점검: 완료(확인된 사실).
- 공개 수정: 미실행(권한 필요).
- 해결 주장 가능 항목: 대표 홈 canonical, 모바일 도메인의 현재 302 이동, 파라미터 URL의 홈 canonical이 공개 응답에서 확인됨.
- 미해결 핵심: 기본 도메인 공개 200, `www` 비정규화, 구상품 홈 302, 검색 URL 홈 302, robots 전역 sitemap 선언, Sitemap 품질, Search Console 색인 제거, placeholder 실제 노출 여부.
- 다음 검토: Cafe24 변경 직후 URL 재조회. 담당자·마감은 대표 지정 필요.
