---
source_path: ".pi/.claude/projects/C--Users-user-Desktop-claude-test/memory/premiummultishop-seo.md"
source_filename: "premiummultishop-seo.md"
source_type: "text"
source_size_bytes: 4058
source_modified_at: "2026-06-08T14:46:36+09:00"
source_sha256: "f9c65ba2e553279bcfec394c3a00f33efaf238bf45daaf7f47d50f7d01ed8c15"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
---
name: premiummultishop-seo
description: Ongoing multi-pass technical SEO audit of premiummultishop.com (Cafe24 luxury store)
metadata: 
  node_type: memory
  type: project
  originSessionId: e7d255f2-02c9-446d-84b4-f1caec596bf8
---

User is running an ongoing, multi-pass (`/loop`) technical-SEO improvement of **https://www.premiummultishop.com/** — a Cafe24-based Korean luxury fashion multi-shop. Methodology: the `product-page-seo` skill from github.com/nexscope-ai/ecommerce-skills (Node/npx is NOT installed, so the skill markdown is fetched directly from raw.githubusercontent.com instead of `npx skills add`).

User's stated focus: **technical SEO foundation**, status = traffic plateaued, target = domestic Korea (so Naver/Yeti matters as much as Google). Wants product pages + whole site crawled corner by corner.

Deliverables saved under `C:\Users\user\Desktop\claude_test\premiummultishop-seo\` (raw HTML in `raw/`, report `SEO-진단리포트-1차.md`).

Key P0 findings from pass 1 (all sitewide in Cafe24 head template): (1) duplicate/broken Open Graph block — og:url points to an image on staging domain blue3200.cafe24.com; (2) GA4 installed twice (G-XVP0MPE74Y + G-CM2XVZ6X45) → corrupt traffic data; (3) JSON-LD @type:Person mistyped for the brand. P1: www/non-www mismatch, Product schema missing aggregateRating/sku/BreadcrumbList, generic/duplicate titles, missing image alt. Sitemaps hold ~2,710 URLs.

Pass 2 done (2026-06-08, report `SEO-진단리포트-2차.md`, data `pass2-crawl.csv`): confirmed broken OG on 50/50 pages; http→https 301 OK but **www & non-www both return 200 (no redirect)** = duplicate host; param URLs (?cate_no/?product_no/?sort_method) canonicalize correctly BUT pagination ?page=2 canonicals to page1 (anti-pattern); **NEW: category titles show unresolved literal "BRAND" placeholder**; product titles use 2 inconsistent suffixes & 17/26 exceed 60 chars; **no WebP, no lazy-load, no img width/height** (CWV/CLS/LCP risk, category page = 1018 imgs/901KB).

Pass 3 done (2026-06-08, report `SEO-진단리포트-3차.md`, data `pass3-sample100.csv`): 100-sample confirmed **15/30 (50%) category titles show literal "BRAND" placeholder** (now P0), 47/70 product titles >60 chars, 18 pages share duplicate meta descriptions (7 clusters, one 1-char desc). robots.txt: two conflicting Googlebot groups + /member/ disallowed yet in sitemap + Sitemap directive nested under bingbot. Breadcrumb visible but no BreadcrumbList schema; weak category interlinking. **PageSpeed Insights API rate-limited (429, no API key) — could not get LCP/CLS/INP; recommended manual PSI run.** Capstone deliverable written: **`작업지시서-Cafe24적용.md`** (12 prioritized Cafe24 fix tasks, P0 ①-④). Audit is now comprehensive — 4 P0 fixes all in head/category-settings.

Pass 4 done (2026-06-08, report `SEO-진단리포트-4차.md`): root-caused the duplicate meta descriptions — **category pages output the bare category name (1-4 chars) as meta description**, and many brand subcategories share names (아우터 at /547,/727,/1016,/1045 etc.) → thin + mass-duplicate across ~hundreds of the 1,508 category URLs (new P1, worksheet task ⑬). Also found **duplicate product listings** (same model code DMF248626-VWH at product_no 88360 & 89765 with identical content — worksheet ⑭). Product meta good but 2 templates. PSI still 429 (gave up — recommend manual). P0 re-verified NOT yet applied (blue3200 ×5, og:title ×2, both GA4 IDs, Person schema all still present).

**LOOP ENDED at pass 4 (diagnostic saturation).** Worksheet `작업지시서-Cafe24적용.md` now has 14 tasks (P0 ①-④, P1 ⑤-⑨+⑬⑭, P2 ⑩-⑫). Remaining work is user-side (apply fixes) + env-blocked (PSI). To resume: run a re-verification pass AFTER user applies P0 fixes (re-check homepage for blue3200/og:title/GA4/Person), and/or manual PageSpeed run.

**How to apply:** when resuming the loop, continue from the "다음 회차 예정 작업" section of the report; append pass-2 findings to the report folder.
