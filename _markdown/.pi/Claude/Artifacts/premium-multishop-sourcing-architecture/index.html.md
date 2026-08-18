---
source_path: ".pi/Claude/Artifacts/premium-multishop-sourcing-architecture/index.html"
source_filename: "index.html"
source_type: "text"
source_size_bytes: 8997
source_modified_at: "2026-07-20T16:22:02+09:00"
source_sha256: "a7794abc11420cc5ee7c700c6a4897d6fb5c6be1964cf963e29671ae559eb419"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
<!DOCTYPE html>
<script type="application/json" id="cowork-artifact-meta">
{
  "name": "Premium Multishop Sourcing Architecture",
  "schemaVersion": 1,
  "description": "프리미엄멀티샵 소액면세 직배송·구매대행·현지 드롭십핑 3-모델 아키텍처. origin별 면세한도($150 HK·EU / $200 미국특송), SKU 면세 라우팅 엔진, 컴플라이언스 가드레일, 병행수입 대비표, 부정면세 레드라인 포함.",
  "mcpTools": [],
  "mcpServerNames": []
}
</script>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>프리미엄멀티샵 — 면세 직배송·구매대행·드롭십핑 아키텍처</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"></script>
<style>
  :root{--bg:#0f1216;--panel:#171b21;--line:#2a313b;--ink:#e8ecf1;--sub:#9aa5b1;--acc:#4da3ff;--ok:#37d39a;--warn:#ffb454;--bad:#ff6b6b;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo','Malgun Gothic',sans-serif;line-height:1.6}
  .wrap{max-width:1180px;margin:0 auto;padding:32px 22px 60px}
  h1{font-size:24px;margin:0 0 4px}
  .sub{color:var(--sub);font-size:14px;margin-bottom:26px}
  h2{font-size:17px;margin:34px 0 12px;padding-left:10px;border-left:3px solid var(--acc)}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:16px}
  .mermaid{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px;overflow-x:auto}
  table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}
  th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
  th{background:#1e242c;color:var(--sub);font-weight:600}
  .tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:20px;font-weight:600}
  .t-ok{background:rgba(55,211,154,.15);color:var(--ok)}
  .t-warn{background:rgba(255,180,84,.15);color:var(--warn)}
  .t-bad{background:rgba(255,107,107,.15);color:var(--bad)}
  .t-acc{background:rgba(77,163,255,.15);color:var(--acc)}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}
  .card h3{margin:0 0 8px;font-size:15px;color:var(--acc)}
  .card p{margin:0;font-size:13px;color:var(--sub)}
  .legend{font-size:12.5px;color:var(--sub);margin-top:8px}
  code{background:#0b0e12;padding:1px 6px;border-radius:5px;color:var(--warn);font-size:12.5px}
  .foot{margin-top:30px;font-size:12px;color:var(--sub);border-top:1px solid var(--line);padding-top:14px}
  @media(max-width:760px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <h1>프리미엄멀티샵 — 소액면세 직배송 · 구매대행 · 현지 드롭십핑 아키텍처</h1>
  <div class="sub">병행수입 탈피 → 소비자 자가사용 개인수입 구조 · 2026-07-20 · 개시 전 관세사·세무사 자문 필수</div>

  <div class="panel">
    <b>법적 핵심 1줄:</b> 세 모델 모두 <b>한국 소비자가 수입 주체(개인통관고유부호·자가사용)</b>이고, 프리미엄멀티샵은 구매·배송을 <b>대행</b>한다.
    벌크 사입·상업수입이 아니므로 <span class="tag t-ok">병행수입 상표 리스크 소멸</span> <span class="tag t-ok">한도 내 관부가세 면제</span>.
    단 면세 수혜자는 법적으로 소비자 → 판매자 이익은 <b>관부가세를 안 얹어 생기는 가격경쟁력·전환·마진</b>에서 발생.
  </div>

  <h2>1. 경로별 소액면세 한도 (설계 1차 분기 기준)</h2>
  <div class="panel">
    <table>
      <tr><th>발송 origin / 방식</th><th>면세한도</th><th>판정 기준액</th><th>비고</th></tr>
      <tr><td>미국발 특송(FedEx/DHL/UPS)+목록통관</td><td><span class="tag t-acc">US$200</span></td><td rowspan="3">물품가＋현지배송비＋판매세<br>(국제운임·보험 제외)</td><td>한·미 FTA 특송 특례</td></tr>
      <tr><td><b>홍콩·이탈리아·EU·중국·일본발</b></td><td><span class="tag t-warn">US$150</span></td><td>홍콩 허브 실효 한도 = <b>$150</b></td></tr>
      <tr><td>일반통관(배제품목·상업용)</td><td>US$150</td><td>명품 패션은 목록통관 가능</td></tr>
    </table>
    <div class="legend">※ 대표님 지시 "200불"은 <b>미국발 특송 한정</b>. 홍콩 경유는 $150. 이 차이를 라우팅 엔진이 자동 분기.</div>
  </div>

  <h2>2. 3-모델 구조</h2>
  <div class="grid">
    <div class="card"><h3>A · 홍콩 보세창고 면세 직배송</h3><p>개당 ≤$150 SKU(SLG·지갑·티셔츠·소품·뷰티). HK 자유무역항 반입(무세) → 주문 시 소비자 명의 개별 소포 직배송(목록통관·면세). <b>자체 허브=리드타임·품질 통제↑</b></p></div>
    <div class="card"><h3>B · EU API 구매대행</h3><p>이탈리아 부티크 재고 API 연동 → 소비자 명의 현지구매·현지→한국 직발송. HOT 8 럭셔리. 저가=면세권/고가=과세 대행. <b>병행수입·상표 리스크 회피</b></p></div>
    <div class="card"><h3>C · 현지배송 드롭십핑</h3><p>중·홍·EU 무재고 카탈로그 API → 자사몰/스마트스토어 리스팅 → 공급사가 소비자 직발송. <b>SKU 폭 확장</b>, 검증 후 A→사입 승격</p></div>
  </div>

  <h2>3. 주문 → 면세 라우팅 → 물류 오케스트레이션</h2>
  <div class="mermaid">
flowchart TD
  C([한국 소비자 주문<br/>개인통관고유부호]) --> CH{채널}
  CH -->|카페24| R
  CH -->|스마트스토어| R
  R[["SKU 면세 라우팅 엔진<br/>현지가＋현지배송 × 환율"]]:::eng --> G{{"컴플라이언스 가드레일<br/>실거래가·합산·자가사용수량"}}:::guard
  G -->|위반| STOP[["차단·수동검토<br/>언더밸류/분할 방지"]]:::bad
  G -->|통과| D{한도 판정}
  D -->|≤ $150 HK·EU| MA[Model A/B<br/>면세 개별직배송]:::ok
  D -->|미국소싱 & ≤ $200| MUS[미국발 특송<br/>면세 경로]:::ok
  D -->|초과| TAX[과세 구매대행<br/>관부가세 투명고지]:::warn
  D -->|안정·고회전| DOM[국내사입 검토]:::warn
  MA --> SUP[[공급사 API<br/>현지구매/드롭십]]
  MUS --> SUP
  TAX --> SUP
  SUP --> LOG{{물류}}
  LOG -->|A| HK[홍콩 3PL 보세창고]
  LOG -->|B/C| LOCAL[현지 특송 직발송]
  HK --> TRK([통관·트래킹·CS])
  LOCAL --> TRK
  TRK --> DASH[[경로별 실마진·재고회전<br/>현금회수 대시보드]]:::eng
  classDef eng fill:#12354f,stroke:#4da3ff,color:#e8ecf1;
  classDef guard fill:#3a2f12,stroke:#ffb454,color:#e8ecf1;
  classDef ok fill:#12352a,stroke:#37d39a,color:#e8ecf1;
  classDef warn fill:#3a2f12,stroke:#ffb454,color:#e8ecf1;
  classDef bad fill:#3a1717,stroke:#ff6b6b,color:#e8ecf1;
  </div>

  <h2>4. 병행수입 vs 구매대행/현지배송</h2>
  <div class="panel">
  <table>
    <tr><th>구분</th><th>병행수입(기존)</th><th>구매대행·현지배송(신설)</th></tr>
    <tr><td>수입 주체</td><td>사업자</td><td><span class="tag t-ok">소비자 개인</span></td></tr>
    <tr><td>통관·세금</td><td>상업통관·관부가세 전액</td><td>목록통관·한도 내 <b>면세</b></td></tr>
    <tr><td>상표 리스크</td><td><span class="tag t-bad">병행수입 이슈 有</span></td><td><span class="tag t-ok">개인직구 → 소멸</span></td></tr>
    <tr><td>재고</td><td>사입 부담</td><td><span class="tag t-ok">무재고(주문분만)</span></td></tr>
    <tr><td>판매자 이익원</td><td>매입-판매 마진</td><td>면세로 최종가 경쟁력 → 전환·마진 + 대행마진</td></tr>
  </table>
  </div>

  <h2>5. 레드라인 — 이 선을 넘으면 부정면세</h2>
  <div class="panel">
    <span class="tag t-bad">금지</span> <b>언더밸류</b>(한도 맞추려 가격 낮춰 신고) — 관세법 §270, 3년 이하 징역 또는 포탈관세 5배 벌금.<br>
    <span class="tag t-bad">금지</span> <b>사입 위장</b> — 반복·대량·동일상품 구매대행은 "상업수입"으로 재분류 → 전액 과세+처벌.<br>
    <span class="tag t-bad">금지</span> <b>분할반입</b> — 같은 날·같은 판매자 쪼개기는 합산과세.<br>
    <span class="tag t-warn">필수</span> 실거래가 신고 · 소비자 본인 통관부호 · 자가사용 수량 · 개시 전 관세사 자문.
  </div>

  <div class="foot">
    연계 문서: 01_사업개요 · 05_소싱처대장 · 10_브랜드×소싱처매트릭스 · 11_면세직배송_구매대행_드롭십핑_설계 ·
    본 다이어그램은 설계 초안이며 실행(3PL·API 계약·송금)은 대표 승인 사항.
  </div>
</div>
<script>
  mermaid.initialize({startOnLoad:true,theme:'dark',flowchart:{curve:'basis'},securityLevel:'loose'});
</script>
</body>
</html>
