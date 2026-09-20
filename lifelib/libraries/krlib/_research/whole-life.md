# 종신보험 (whole life) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose: the
source library behind a Korean whole life liability cash flow reference model — the
level-premium 종신보험 chassis (보험료적립금 / 계약자적립액 / 해지환급금 / 보험계약대출 /
보험료 납입면제), its dominant **무해지환급형 · 저해지환급형** suppressed-surrender-value
forms, and the neighbouring 유니버셜, 금리연동형, 체증형 and 단기납 shapes.

종신보험 is the flagship Korean protection product. It arrived in the market properly only in
the late 1990s — 푸르덴셜생명 built a male university-graduate Life Planner channel around it
and turned it into the life industry's biggest single seller of the early 2000s [R8] — and it
has since absorbed almost every product innovation the Korean market has produced: 변액종신
(2001), CI 선지급 종신 (2002), 유니버셜 종신 (2004), and from the mid-2010s the
무·저해지환급형 forms that now dominate protection sales [R8] [R7]. In `krlib` it is the
**savings/protection chassis**: `CI_KR_S` inherits it and adds accelerated critical-illness
payment, and `Pension_KR_S` inherits the accumulation half.

What makes the Korean product structurally different from its Japanese, French or German
cousins is not the death benefit — that is ordinary whole-of-life cover — but the **surrender
value**. Korean carriers sell a *suppressed* surrender value as the headline feature, in at
least five contractually distinct designs, and price the product on an **explicitly disclosed
lapse assumption** (적용해지율) that the suppression is meant to exploit. The surrender value
is nil or a stated fraction while premiums are being paid and steps up at 납입완료: a cliff,
not a curve. That cliff is the single most important thing a Korean whole life model must
reproduce, and it is also the thing that drew supervisory attention in 2024, because an IFRS
17 CSM computed on a lapse assumption that runs high right up to 납입완료 books profit the
insurer will never see [R3] [R7].

This file is the **provenance layer** behind `products/whole_life/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Every fact below is tagged `[S#]` (primary
product document) or `[R#]` (regulatory/actuarial reference) pointing at a document actually
retrieved and read during this session, or is tagged `[unverified]` where it is general
knowledge or a search-result snippet not confirmed against a retrieved document. The source
numbering here is **never renumbered**: the product documents cite against it.

Access date for all fetched sources: **2026-09-03**. Nine carriers are represented:
처브라이프생명, 하나생명, KB라이프생명, DB생명, KDB생명, ABL생명, 삼성생명, AIA생명 and
신한라이프, plus 교보생명 and 한화생명 for rate disclosure. Company and branded product names
appear here and in `sources.md` only.

---

## Primary sources

### S1 — 처브라이프생명, 「Chubb 더하고 채우는 종신보험 무배당 (해지환급금 일부지급형)」

- Publisher: 처브라이프생명보험 주식회사 (Chubb Life Insurance Korea)
- Document: 4-page 상품안내장 / 브로슈어, `product_brochure_S1_AW21.pdf`; footer 「2022
  MKT-105 / 2022.04.01 / 준법감시인 심의필 제2022-105호(심의필 유효기간:
  2022.03.30~2023.03.29)」; the premium page is headed 「2022년 4월 계정」
- Doc type: product brochure (보험안내자료) with published premium and surrender-value tables
- URL: https://www.chubblife.co.kr/assets/product_brochure_S1_AW21.pdf
- Retrieved: **yes** (PDF downloaded, 4 pp.; a plain text dump scrambles the chart on p.1, so
  the 환급률 chart was recovered by positional word extraction with PyMuPDF)
- Key content: a **side-by-side 해지환급금 예시표** for 해지환급금 일부지급형 against the
  non-marketed 표준형 twin, at 8 durations, with both premium scales; the **50%** suppression
  factor stated in the 약관-style footnote; a **disclosed 예정이율 of 연복리 2.3%**; a premium
  grid by age and sex; 체증형 death benefit (+5% of 가입금액 per year for 30 years);
  (무)추가납입특약 and 추가계약자적립금 인출 mechanics; a 1.5% volume discount at 가입금액 ≥
  3,000만원; a 보험료납입면제특약 on 암/급성심근경색증/뇌출혈.

### S2 — 하나생명, 「무배당 하나로 연결된 든든한 종신보험(해지환급금 일부지급형)」 상품요약서

- Publisher: 하나생명보험 주식회사 (Hana Life Insurance)
- Document: 10-page 상품요약서 (product summary — the statutory summary of the 기초서류)
- Doc type: 상품요약서
- URL:
  https://www.hanalife.co.kr/home/download2.do?fileName=PROD%2F%28%EB%AC%B4%29%ED%95%98%EB%82%98%EB%A1%9C%EC%97%B0%EA%B2%B0%EB%90%9C%EB%93%A0%EB%93%A0%ED%95%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98%28%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%EA%B8%88+%EC%9D%BC%EB%B6%80%EC%A7%80%EA%B8%89%ED%98%95%29_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C.pdf
- Retrieved: **yes** (served with `Content-Type: application/x-msdownload`; the bytes are a
  10-page PDF and extract cleanly with PyMuPDF)
- Key content: the single most complete disclosure in the set — a **formula-based** 해지환급률
  (0% / `10% + 90% × 납입횟수/84` / 100%), a **disclosed 적용이율 연복리 2.25%**, **disclosed
  적용위험률 (사망률) at ages 20/40/60 by sex**, a **disclosed 적용해지율 of 1%~10%** with the
  explicit statement that the 일반형 comparison product carries none, full 해지환급금 예시표
  for both sexes at 14 durations for both forms, the 보험가격지수 (85.4% 남 / 86.2% 여), the
  납입면제 trigger, and the 연금전환특약 with its 최저보증이율 ladder (1.25% / 1.0% / 0.5%).

### S3 — KB라이프생명, 「KB,시니어[약:속]종신보험 무배당 (해약환급금 과소지급형)」 상품안내장

- Publisher: KB라이프생명보험 주식회사 (KB Life Insurance)
- Document: 16-page 상품안내장; 「준법감시인확인필-SM-2212368-1(2022.12.29~2023.12.28)」
- Doc type: product brochure (보험안내자료)
- URL: https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1228983/44
- Retrieved: **yes** (PDF downloaded, 16 pp., text extracted and read)
- Key content: a **third, arithmetically different** suppression design — the surrender value
  is a straight-line fraction of *premiums paid*, `납입보험료 누계 × 경과개월수 /
  ((납입기간+3년)×12)`, nil in year 1 and capped at 100% at 납입기간+3년; a senior-market
  issue-age envelope (54–72 male); a 2형(Light형) with a reduced non-accident death benefit;
  the 납입면제 waiver and its "premiums deemed paid" rule; three 연금전환특약 with their
  eligibility conditions; 선납 discounted at the 평균공시이율; a 2-year suicide exclusion.

### S4 — DB생명, 「무배당 알차고 행복한 종신보험(저해지환급형)(1607)」 상품안내장

- Publisher: DB생명보험 주식회사 (DB Life Insurance)
- Document: 5-page 상품안내장
- Doc type: product brochure (보험안내자료)
- URL:
  https://www.idblife.com/notice/product/file/A020100001.pdf?fileName=DB%EC%83%9D%EB%AA%85-%EB%AC%B4%EB%B0%B0%EB%8B%B9+%EC%95%8C%EC%B0%A8%EA%B3%A0+%ED%96%89%EB%B3%B5%ED%95%9C+%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EC%A0%80%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%ED%98%95(1607(A020100001-%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98.pdf
- Retrieved: **yes** (served as `application/octet-stream`, 3.6 MB; a 5-page PDF; both
  surrender-value grids re-checked by positional word extraction)
- Key content: the only **30%** suppression factor in the set, stated in the 유의사항 as
  「1형(표준형) 해지환급금의 30%에 해당하는 금액」; **two complete 해지환급금 예시 grids**
  (1종 기본형 and 2종 실속형) at 8 durations each, both forms; a premium grid by age, sex and
  form; the 납입기간 menu (5/7/10/15/20/25/30년납 and 50/55/60/65/70세납); a 전환나이 design
  in which the death benefit steps at 55/60/65/70; the phrase 「사업비(미상각신계약비
  (해지공제액) 포함)」 naming the deduction.

### S5 — KDB생명, 「희망드림 무배당 KDB유니버셜종신보험(보증비용부과형) 해지환급금 보증형」

- Publisher: KDB생명보험 주식회사 (KDB Life Insurance)
- Document: 60-page 보험약관 (policy conditions) with 부표1–3 and 용어의 정의; 판매일자
  2021.05.01; file `I40204_20210501_..._약관_V03.pdf`
- Doc type: **policy conditions (약관)** — the only full 약관 retrieved in this session
- URL:
  https://www.kdblife.com/nKumhoFiles/data_pdf/product/2021/I40204_20210501_%ED%9D%AC%EB%A7%9D%EB%93%9C%EB%A6%BC(%EB%AC%B4)KDB%EC%9C%A0%EB%8B%88%EB%B2%84%EC%85%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EB%B3%B4%EC%A6%9D%EB%B9%84%EC%9A%A9%EB%B6%80%EA%B3%BC%ED%98%95)%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%EA%B8%88%EB%B3%B4%EC%A6%9D%ED%98%95_%EC%95%BD%EA%B4%80_V03.pdf
- Retrieved: **yes** (1.6 MB PDF, 60 pp., text extracted cleanly and the articles read in
  full)
- Key content: articles 1–44 verbatim — 제20조(계약내용의 변경 등) with the 감액 formulas and
  worked examples; **제21조(보험나이 등)** with the 6-month rule and two worked examples;
  제24조(제2회 이후 보험료의 납입) with the universal free-payment and payment-holiday rule;
  제25조(납입최고와 계약의 해지) with the 14-day 납입최고기간; 제26조(부활) with a **3-year**
  window; **제31조(해지환급금)**; **제32조(공시이율의 적용 및 공시)** with the 신공시기준이율
  mechanism and a **최저보증이율 연복리 0.75%**; **제33조(중도인출)** with the 50% cap, the
  12-per-year limit and the residual-account floor; **제34조(보험계약대출)**; and the 용어의
  정의 giving 예정적립금 (at 적용이율 **연복리 2.3%**), 계약자적립금 (at 신공시이율),
  월대체보험료, 부가보험료, 해지공제액 and 보험계약대출이율.

### S6 — ABL생명, 「(무)ABL건강하면THE소중한종신보험(해약환급금 일부지급형)2504」 상품안내장

- Publisher: ABL생명보험 주식회사 (ABL Life Insurance)
- Document: 20-page 상품안내장; 「준법감시인 심의필 제2025-PA349호 (2025.09.29~2026.09.28)」
- Doc type: product brochure (보험안내자료)
- URL:
  https://www.abllife.co.kr/cms/prdt/wlifeFprd/__icsFiles/afieldfile/2025/09/29/(%EB%AC%B4)ABL%EA%B1%B4%EA%B0%95%ED%95%98%EB%A9%B4THE%EC%86%8C%EC%A4%91%ED%95%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88_%EC%9D%BC%EB%B6%80%EC%A7%80%EA%B8%89%ED%98%95)2504_20251001.pdf
- Retrieved: **yes** (1.3 MB PDF, 20 pp., text extracted and read)
- Key content: the **most recent** product in the set (October 2025) — a 50% 일부지급형 with
  **three 종**: 1종(평준형), 2종(체감형) and 3종(체증형), each with its own surrender-value
  grid and premium scale; a **건강등급 (health-grade) premium discount** of up to 8% on the
  주계약 recomputed annually; a 생활설계자금 drawdown that reduces the sum assured
  automatically; issue ages 만15세~70세 and 납입기간 5/7/10/15/20년납; the 납입면제 trigger
  (50% 장해지급률); the 평균공시이율 quoted in-document as 연복리 2.75% for 2025.

### S7 — 삼성생명, 「삼성 더행복종신보험(2309)(무배당) [5년이후사망보험금100%형]」

- Publisher: 삼성생명보험 주식회사 (Samsung Life Insurance)
- Document: 4-page 상품안내장; 「준법감시필 23-1888(FC지원팀, 2023.08.29 ~ 2024.08.28)」;
  발행일자 2023년 09월 04일
- Doc type: product brochure (보험안내자료)
- URL:
  https://assets-global.website-files.com/638be8b99d4abb0bb101827b/64f9397cb1f729afb6cf4e2a_%EB%8D%94%ED%96%89%EB%B3%B5%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(2309)(%EB%AC%B4%EB%B0%B0%EB%8B%B9)(5%EB%85%84%EC%9D%B4%ED%9B%84%EC%82%AC%EB%A7%9D%EB%B3%B4%ED%97%98100%25%ED%98%95,%EC%A0%80%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88%ED%98%95).pdf
- Retrieved: **yes** (PDF downloaded, 4 pp.; the 유지보너스 rate table recovered by positional
  extraction). Note this is a distributor-hosted copy on a Webflow CDN, not a 삼성생명 URL.
- Key content: the **단기납 (short-pay) 저해약환급금형** design that dominated Korean life
  sales in 2023–24 — 5년납 / 7년납, a **유지보너스 (persistency bonus)** credited to the
  계약자적립액 at 납입완료 at published rates, and a surrender-value grid running to **환급률
  206.7% at duration 50**; 보험기간 이원화 (a reduced disease-death benefit for the first 5
  years); a **disclosed 해약환급금 적용이율 of 연복리 2.25% for the first 10 years and 1.75%
  thereafter**; a 사망보험금 연금선지급 전환제도.

### S8 — KDB생명, 「무배당 우리가바라던 종신보험」 상품요약서

- Publisher: KDB생명보험 주식회사
- Document: 7-page 상품요약서; 판매일자 2024.01.01; file
  `I40414_20240101_(무)우리가바라던종신보험_상품요약서_V02.pdf`
- Doc type: 상품요약서
- URL:
  https://www.kdblife.com/nKumhoFiles/data_pdf/product/2024/I40414_20240101_(%EB%AC%B4)%EC%9A%B0%EB%A6%AC%EA%B0%80%EB%B0%94%EB%9D%BC%EB%8D%98%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C_V02.pdf
- Retrieved: **yes** (139 KB PDF, 7 pp., text extracted and read in full)
- Key content: the **fully nil** form (해약환급금 미지급형Ⅳ) — zero surrender value for the
  whole of the 20-year payment period, then `이미 납입한 보험료 × max(기준상품 해약환급률,
  100%)`; a **disclosed 적용이율 연복리 2.75% (금리확정형)**; **disclosed 예정 경험사망률** at
  ages 20/40/60 by sex; the sharpest single number in this file — a **disclosed 적용해약률 of
  연 0%~13.4% during the payment period and 연 1.0%~11.3% after it**; the statement that
  해약환급금 = 계약자적립액 − 미상각신계약비; 보험가격지수 110.3% / 110.9%; full 해약환급금
  예시 grids to duration 60 for both product variants and both sexes.

### S9 — 하나생명, 「적용이율 공시 — 보험계약대출이율」

- Publisher: 하나생명보험 주식회사
- Doc type: published rate disclosure (company web page)
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab3_6.do
- Retrieved: **yes** (WebFetch, 200, server-rendered table read)
- Key content: the 보험계약대출이율 formula banded by contract date — 「적용이율 + 1.5%」
  (금리확정형) / 「공시이율 + 1.5%」 (금리연동형) from 2013-04-01; 「예정이율 + 2%」 for
  2010-10-01~2012-03-31 — and the floor rule that a 금리연동형 loan is priced off the
  최저보증이율 when the 공시이율 falls below it.

### S10 — 하나생명, 「적용이율 공시 — 표준이율 및 평균공시이율」

- Publisher: 하나생명보험 주식회사
- Doc type: published rate disclosure (company web page)
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Retrieved: **yes** (WebFetch, 200)
- Key content: the **평균공시이율 series 2016–2026** and the 표준이율 series for its last
  three years before it was superseded. This is the single citable time series of the Korean
  average declared rate found in this session.

### S11 — 교보생명, 「보험계약대출」 상품안내

- Publisher: 교보생명보험 주식회사 (Kyobo Life Insurance)
- Doc type: product page (company web site)
- URL: https://www.kyobo.com/dgt/web/insurance/policy-loan/PCLN_ALL_INTRO
- Retrieved: **yes** (WebFetch, 200)
- Key content: 확정형 「예정이율 + 1.40 ~ 1.50%(변동가능)」, 연동형 「공시이율 … + 1.50%」,
  the published rate range 연 3.5% ~ 10.5%, the loan limit 「해약환급금의 50% ~ 85%」, a
  −0.10%p concession from 2025-11-27 on contracts whose 예정이율 is 7% or more, no
  early-repayment fee, and a loan term running to the contract's 만기일.

### S12 — AIA생명, 「보험계약대출이율」 공시

- Publisher: AIA생명보험 주식회사 (AIA Life Korea)
- Doc type: published rate disclosure (company web page)
- URL: https://www.aia.co.kr/ko/disclosure/our-products/interest-rate/policy-loan.html
- Retrieved: **yes** (WebFetch, 200)
- Key content: a **complete historical 가산금리 schedule by contract-date band**, from 2003 to
  the present, with the 최고 적용 대출이율 cap at each band. The clearest evidence in the set
  that the Korean policy loan rate is a *vintage* rate, not a market rate.

### S13 — 신한라이프, 「보험계약대출」

- Publisher: 신한라이프생명보험 주식회사 (Shinhan Life Insurance)
- Doc type: product page (company web site)
- URL: https://www.shinhanlife.co.kr/hp/cdhc0020.do
- Retrieved: **yes** (WebFetch, 200)
- Key content: 「예정이율+가산금리(1.5%)」 / 「공시이율+가산금리(1.5%)」; loan limit
  「해약환급금의 50 ~ 80%이내」; no early-repayment fee; a 0.1% concession for insureds aged
  65+ on contracts with a 예정이율 of 5.5% or more.

### S14 — 손해보험협회, 「보험계약대출금리」 비교공시

- Publisher: 손해보험협회 (General Insurance Association of Korea) — 보험다모아 공시 portal
- Doc type: industry comparison disclosure (비교공시)
- URL: https://kpub.knia.or.kr/etcDisc/loan/insContractLoan.do
- Retrieved: **yes** (WebFetch, 200; 산출기준월 26년 7월)
- Key content: an insurer-by-insurer grid of 기준금리 / 가산금리 / 대출금리 split by
  금리확정형 and 금리연동형. It covers **non-life** insurers, so it bounds the Korean policy
  loan market but is not itself evidence about a 생명보험 종신보험 contract.

### S15 — 교보생명, 「공시기준이율 적용현황」

- Publisher: 교보생명보험 주식회사
- Doc type: published rate disclosure (company web page)
- URL: https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status
- Retrieved: **in part** (WebFetch, 200; the page returned its default query result —
  공시기준이율 3.19 / 적용률 3.19 / 적용이율 3.19 across 보장(무배당), 연금(무배당),
  연금(배당), 저축(무배당), 연금저축(배당) — but **no as-of month was rendered**, because the
  month is a form selection). The methodology text confirming that 적용공시이율 = 공시기준이율
  adjusted by a 조정률 was present.

### S16 — 생명보험협회 공시실

- Publisher: 생명보험협회 (Korea Life Insurance Association)
- Doc type: industry disclosure portal
- URL: https://pub.insure.or.kr/
- Retrieved: **in part** (WebFetch, 200; the navigation renders — 상품제도 및 개요 /
  상품비교공시 / 저축성 요약공시 / 경영공시 / 대출공시 / 기타공시, and the path 상품비교공시 →
  보장성보험 → 종신보험 — but every comparison table opens through `javascript:void(0)` and no
  product rows were obtained)
- Key content: structure only. See "Fetch failures and gaps".

### S17 — 손해보험협회 e-보험시장, 「종신보험」 비교공시

- Publisher: 손해보험협회
- Doc type: industry comparison disclosure
- URL: https://www.e-insmarket.or.kr/wholeIns/wholeInsList.knia
- Retrieved: **in part** (WebFetch, 200). The comparison basis rendered — 보험가입금액 1억원,
  종신, 20년납, 월납 — but the product table returned 「해당 상품이 없습니다」.
- Key content: the **standard comparison basis** Korean industry disclosure uses for 종신보험
  (1억원 / 20년납 / 월납), which is a useful sanity check on the model point choice.

### S18 — 한화생명, 「종신/정기보험」 상품안내

- Publisher: 한화생명보험 주식회사 (Hanwha Life Insurance)
- Doc type: product page (company web site)
- URL: https://www.hanwhalife.com/main/insurance/product/IN_SM00000_P30000.do
- Retrieved: **in part** (WebFetch, 200; the product guide rendered but no premium, 환급률 or
  issue-age figures)
- Key content: the 종 menu for 하나로H종신보험(무) — 1종(체증형) with 보험기간
  80/85/90/95세만기 and 2종(기본형) with 60/70/80/90/95세만기 — and a 납입기간 menu including
  **3년납**. Used only for the payment-term envelope.

### S19 — 한화생명 상품공시실, 「적용이율」

- Publisher: 한화생명보험 주식회사
- Doc type: disclosure index page
- URL:
  https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do?MENU_ID1=DF_GDAR000
- Retrieved: **no** (WebFetch, 200, but the page returned only the disclosure-regime
  explanation and a departmental contact table; the rate data itself is loaded elsewhere)
- Key content: none. Recorded so the attempt is on the record.

---

## Regulatory and actuarial references

### R1 — 금융위원회, 「무(저)해지환급금 보험의 상품 구조를 개선하고, 보험약관 …」 (2020-11-18)

- Publisher: 금융위원회 (Financial Services Commission)
- Doc type: 보도자료 (press release) announcing the 보험업감독규정 amendment
- URL: https://fsc.go.kr/no010101/74613
- Retrieved: **yes** (WebFetch, 200)
- Content: the amendment effective **2020-11-19** restricting products whose surrender value
  during the payment period is nil or under 50% of the 표준형, so that they must be designed
  「전(全) 보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로」; and a **worked
  numeric comparison** on a 종신보험 (20년납, 1,000만원, 남 40세) of 표준형 against the 무해지
  form before and after the amendment. This is the sharpest published statement of what the
  rule actually does to the cash-value curve.

### R2 — 금융위원회, 「높은 환급률만을 강조하며 판매되는 무(저)해지환급금 보험 …」 (2020-07-27)

- Publisher: 금융위원회
- Doc type: 보도자료 — 보험업감독규정 개정안 입법예고
- URL: https://www.fsc.go.kr/no010101/74468
- Retrieved: **yes** (WebFetch, 200)
- Content: the market count at that date — 생명보험 20개사 and 손해보험 11개사 selling the
  form as a main line, against 4 and 3 not selling it; the mis-selling concern
  (「저축성보험처럼 환급률만을 강조하며 판매」); and the shape of the restriction later
  enacted as [R1].

### R3 — 금융위원회·금융감독원, 「합리적인 계리가정과 단계적 할인율 조정을 …」 (2024-11-07)

- Publisher: 금융위원회 and 금융감독원, 제4차 보험개혁회의
- Doc type: 보도자료
- URL: https://www.fsc.go.kr/no010101/83351
- Retrieved: **yes** (WebFetch, 200)
- Content: **the 2024 supervisory intervention on the 무·저해지 lapse assumption** — the
  log-linear model designated as the 원칙모형 with the lapse rate converging to **0.1%** at
  납입완료; the post-완납 rate set at **0.8%** or a **20%** relative to the 표준형 product's
  rate; the strict conditions on using a non-principle model (audit-report disclosure of the
  CSM / K-ICS / net income difference, external actuarial validation, quarterly reporting to
  the FSS); a minimum **30%** additional lapse at a bonus payment point on 단기납 종신, on
  industry data showing 10-year lapse of 29.4%~30.2% at policy year 11 for bancassurance
  single-premium savings; and the discount-curve last-observable-maturity extension from 20 to
  30 years phased over three years from January 2025. Effective from the 2024 year-end close.

### R4 — 금융감독원, 「저해지환급금 보험상품에 대해 소비자 경보 발령」 (2019-10-23)

- Publisher: 금융감독원 (Financial Supervisory Service), 보험과
- Doc type: 소비자경보 (consumer alert), published on the FSC site
- URL: https://www.fsc.go.kr/no010101/73932
- Retrieved: **yes** (WebFetch, 200)
- Content: the sales-start dates — life insurers from **July 2015**, non-life from **July
  2016** — and about **4 million** contracts written to March 2019; the warning that the form
  is a 보장성보험 and unsuitable for savings; and the operationally important point that **a
  무해지환급금 contract cannot support a policy loan during the payment period**.

### R5 — 금융위원회, 「불합리한 보험 사업비와 모집수수료를 개편하여 …」 (2019-08-01)

- Publisher: 금융위원회
- Doc type: 보도자료
- URL: https://fsc.go.kr/no010101/73816
- Retrieved: **yes** (WebFetch, 200)
- Content: the 표준해약공제액 limits expressed as a multiple of the monthly premium —
  **보장성보험 13배, 저축성보험 3배** — the rule that the savings element of a 보장성보험 must
  carry 저축성 expense and surrender-deduction levels at **70%** of the then-current amount,
  and the 모집수수료 분급 rule that the annual commission may not exceed **60% of the
  표준해약공제액** with the instalment total at least **5%** above the up-front total.
  Timetable: expense reform to April 2020, commission reform from January 2021.

### R6 — 보험연구원 정원석, 「소비자보호를 위한 보험상품 사업비 및 모집수수료 개선」 (2019-04)

- Publisher: 보험연구원 (Korea Insurance Research Institute); 사업비 및 모집수수료 부가체계
  공청회, 2019.4.16
- Document: 27-slide presentation, `KIRI_20190416_144027.pdf`
- Doc type: research presentation
- URL: https://www.kiri.or.kr/pdf/전문자료/KIRI_20190416_144027.pdf
- Retrieved: **yes** (938 KB PDF, 27 pp., text extracted and read)
- Content: **the 표준해약공제액 formula, by product class**, with a worked arithmetic example;
  the framing of the surrender value as 적립금 less unrecovered 사업비 bounded by the
  표준해약공제액; and a 장기보장성보험 surrender-value example table.

### R7 — 보험연구원 노건엽·이승주, 「보험개혁회의 내용과 과제: 건전성 제도」 (2025-04)

- Publisher: 보험연구원, CEO Report 03호, 2025.04
- Document: 24-page report
- Doc type: research report
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=671389
- Retrieved: **yes** (594 KB PDF, 24 pp., text extracted and read)
- Content: the **무·저해지 보장성 초회보험료 share time series** (2018 / 2021 / 2023); a
  restatement of the [R3] lapse guidance with the exact model names; the **K-ICS
  대량해지위험** shock table for 표준형 and 저해지환급형, sourced to 보험업감독업무 시행세칙
  [별표 22]; and the **해약환급금준비금** figures and the K-ICS-linked accumulation-ratio
  schedule for 2024–2029 set out in the 보험업감독규정 부칙.

### R8 — 보험연구원, 「Ⅲ. 종신보험의 성장」, 연구보고서 2018-5

- Publisher: 보험연구원, 연구보고서 2018-5
- Document: 28-page chapter, `nre2018-05_03.pdf`
- Doc type: research report chapter (product history)
- URL: https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2018-05_03.pdf
- Retrieved: **yes** (858 KB PDF, 28 pp., text extracted and read)
- Content: the market history of 종신보험 in Korea — the 1959 동방생명 attempt, the 1990s
  false starts, the 푸르덴셜생명 Life Planner breakthrough, 삼성생명's 1999 entry; a table of
  종신보험 new business by carrier 2001–2009 sourced to 금융감독원 금융통계정보시스템; the
  evolution sequence 변액종신 (2001) → CI 선지급 종신 (2002) → 유니버셜 종신 (2004); and a
  taxonomy table of the six Korean whole life shapes.

### R9 — 보험연구원 황인창, 「2025년 보험산업 전망」 (2024-10-10)

- Publisher: 보험연구원, 보험산업 전망과 과제 세미나, 2024.10.10
- Document: 78-slide presentation, `smn_20241010.pdf`
- Doc type: research presentation
- URL: https://www.kiri.or.kr/pdf/전문자료/smn_20241010.pdf
- Retrieved: **yes** (2.1 MB PDF, 78 pp., text extracted; the Korean text extracts without
  inter-word spaces, so quotations from it are re-spaced here and marked as such)
- Content: 보장성보험 수입보험료 2020–2024H1; the observation that 단기납 종신 sales rose in
  2024 Q1 and then tapered while 무·저해지환급형 건강보험 kept growing; a monthly 초회보험료
  chart for 무·저해지환급형 종신보험 and 질병보험; and the 2025 forecast of a 9.2%
  industry-wide 초회보험료 decline.

### R10 — 국가법령정보센터, 「보험업감독규정」

- Publisher: 법제처 국가법령정보센터 (Korea Law Information Center) / 금융위원회
- URL: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196 (also tried
  https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000235980)
- Retrieved: **no** (WebFetch, 200, but only the site chrome, revision history and share
  buttons render; the article body is loaded into a frame that WebFetch does not follow)
- Content: none obtained. Every 보험업감독규정 fact in this file therefore rests on the FSC
  press releases [R1] [R2] [R5] or on [R6] [R7], and is flagged where that matters.

### R11 — 국가법령정보센터, 「보험업감독업무시행세칙」

- Publisher: 법제처 국가법령정보센터 / 금융감독원
- URL: https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2200000106665&chrClsCd=010201
- Retrieved: **no** (same frame problem as [R10])
- Content: none obtained. The 시행세칙 matters here twice — 별표15 carries the 생명보험
  표준약관 and 별표22 the K-ICS 지급여력 standards — and neither was read directly.

### R12 — 보험개발원, 보도자료 목록

- Publisher: 보험개발원 (Korea Insurance Development Institute)
- URL: https://www.kidi.or.kr/user/nd11592.do
- Retrieved: **yes** (WebFetch, 200; the ten most recent items listed, 2026-01 to 2026-08)
- Content: **no 경험생명표 item appears in the current listing**, and no archive page was
  reached. This is consistent with the house position that the 경험생명표 is not published in
  full; see "Fetch failures and gaps".

### R13 — 생명보험협회, 「금융통계월보(생명보험편)」

- Publisher: 생명보험협회
- URL: https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do
- Retrieved: **in part** (WebFetch, 200; the table catalogue and the note that the series is
  produced under a 2016-11 data agreement with 금융감독원 render, but the statistical tables
  themselves are drawn client-side and no figure was obtained)
- Content: structure only.

---

## Fact extraction

### 1. Product architecture

- 종신보험 is whole-of-life cover: 보험기간 종신, a death benefit payable whenever the insured
  dies, and no maturity value. Every product in the set states 보험기간 종신 [S1] [S2] [S3]
  [S4] [S6] [S8]. 하나생명 classify it in the 상품요약서 as 「보장성보험 / 개인형」 [S2].
- All eight products in the set are **무배당** (non-participating). 하나생명 state the reason
  in terms: 「무배당 상품은 배당상품보다 상대적으로 저렴한 보험료로 가입하실 수 있습니다」
  [S2], and KDB생명 repeat it verbatim [S8]. This is not accidental — [R8] records that the
  first successful Korean 종신보험, 푸르덴셜생명's, was deliberately 무배당 at a time when
  most Korean products were 유배당, and that the lower premium was the selling point.
- Unlike the Japanese set, **no product here carries a 고도장해 (severe disability) benefit
  paid at the sum assured**. What Korea puts in that slot is a **보험료 납입면제** (premium
  waiver) triggered at a 50% 장해지급률 — the contract continues, the premiums stop, and the
  death benefit and surrender value are computed as if the premiums had been paid [S2] [S3]
  [S6] [S8]. This is a materially different liability shape and §13 sets it out.
- 사망보험금 shape is a menu, not a constant. Three shapes appear:
  - **평준형** (level) — 보험가입금액의 100% throughout [S6, 1종].
  - **체증형** (increasing) — ABL: 보험가입금액의 100% to duration 10, then +5% of 가입금액 a
    year for up to 10 years, then a flat **150%** from duration 20 [S6, 3종]. Chubb: +5% a
    year from duration 1, capped at 30 years, so 5,000만원 → 12,500만원 at duration 30 [S1].
  - **체감형** (decreasing) — ABL: 100% to age 60, then −5% of 가입금액 a year for up to 10
    years, then a flat **50%** from age 69 [S6, 2종].
- A fourth shape is Korea-specific and has no analogue elsewhere in this repository: the
  benefit defined as **the greater of the sum assured and a multiple of premiums paid**.
  하나생명: 「「보험가입금액」과 「사망시점까지 납입보험료 합계금액에 "추가설계사망보험금
  비율"을 곱한 금액」 중 큰 금액」, with the ratio published by issue age and sex — 남 30세
  240%, 40세 197%, 50세 163%; 여 30세 267%, 40세 218%, 50세 178% [S2]. KB라이프 use the same
  device with 경과개월수 in place of premiums paid, capped at 납입기간 × 12 months [S3].
  KDB생명's 기납입P 플러스형 pays 가입금액 **plus** premiums paid [S8].
- 삼성생명 add a **보험기간 이원화** design: for the first five years the disease-death
  benefit is 가입금액의 30%~90% while the accident-death benefit is 100%; from year five both
  are 100% [S7].
- 유니버셜 종신 is a distinct chassis, not an option: free premium payment within a 납입한도,
  monthly deduction of a 월대체보험료 from the 계약자적립금, 중도인출, and payment holidays
  once 24 premiums have been paid [S5]. §15 sets it out.

### 2. The 무해지 / 저해지 family — five contractually distinct designs

This is the product's signature and the thing a Korean model must not smooth. All five designs
share the same commercial logic — a lower premium bought by giving up the surrender value
during 납입기간 — but they are arithmetically different, and a model that assumes "70% like
Japan" would be wrong at every carrier in this set.

**The vocabulary is not standardised.** The same mechanic is marketed as 저해지환급형 [S4],
해지환급금 일부지급형 [S1] [S2] [S6], 해약환급금 과소지급형 [S3], 저해약환급금형 [S7] and
해약환급금 미지급형 [S8]. The supervisor's own term is **무(저)해지환급금 보험** [R1] [R2]
[R4]. `krlib` uses 무해지환급형 / 저해지환급형 as the generic pair, per the house brief, and
records the carrier's own wording at each citation.

**Design A — a fixed percentage of the 표준형 surrender value.** The commonest form. The
contract names a comparison product ("표준형" / "기본형" / "일반형") which is priced with the
same benefits but **without a lapse assumption**, and the sold product pays a stated fraction
of that product's surrender value during 납입기간 and the whole of it afterwards. The
fractions observed:

| Carrier | Wording | Fraction | Source |
|---|---|---|---|
| DB생명 | 「1형(표준형) 해지환급금의 30%에 해당하는 금액」 | **30%** | [S4] |
| 처브라이프 | 「"표준형" 해지환급금의 50%에 해당하는 해지환급금」 | **50%** | [S1] |
| ABL생명 | 「'기본형' 해약환급금의 50%에 해당하는 금액」 | **50%** | [S6] |
| 삼성생명 | 「납입기간 내 유해약환급금형의 50%」 | **50%** | [S7] |

The comparison product is explicitly **not sold**. 처브라이프: 「"표준형"의 경우는 "해지환급금
일부지급형"과 동일한 보장내용으로 해지율을 적용하지 않고 이 보험의 「보험료 및 책임준비금
산출방법서」에 따라 계산된 상품이며, "해지환급금 일부지급형"과 비교안내를 위한 종목으로 실제로
판매하지 않습니다」 [S1]. KB라이프 [S3], DB생명 [S4] and 하나생명 [S2] carry the same sentence
with their own product names. That single clause is the most important actuarial statement in
the whole set: **the 표준형 surrender value is the model's underlying reserve, computed on the
same basis but with the lapse assumption switched off, and the sold product's surrender value
is a haircut on it.**

**Design B — a formula on premiums paid, ramping to 100%.** 하나생명 publish the whole thing
in the 상품요약서, verbatim [S2]:

```
해지환급금 일부지급형의 해지환급금은 납입보험료 합계금액에 해지환급률을 곱하여 산출합니다.
  ① 1년 이내 : 0%
  ② 1년 초과 7년 이내 : 10% + [90% x 보험료 납입횟수 / 84회]
  ③ 7년 초과 : 100%
다만, 계약일로부터 7년이 초과했더라도 보험료 납입횟수가 84회를 초과하지 않으면
해지환급률 계산은 1년 초과 7년 이내의 방식으로 계산합니다.
```

Checked against the published grid: at 13 payments 10 + 90×13/84 = 23.929% against a printed
23.93%; at 24, 35.714% against 35.71%; at 36, 48.571% against 48.57%; at 60, 74.286% against
74.29% [S2]. From duration 7 the 환급률 is exactly 100.00% at every later duration in the
table, out to 40 years — this design gives back premiums and never more.

**Design C — straight-line on premiums paid to 납입기간 + 3년.** KB라이프 [S3], verbatim:

```
① 「납입기간 + 3년」 이내 이 계약을 해지할 경우
  가. 가입 후 계약일로부터 「만 1년이 지난 계약 해당일 전일」이내 … 해약환급금은 없습니다.
  나. 가입 후 … 1년이 경과하고 "보험료 납입 횟수"가 12회차 이상인 경우 …
      해약환급금 = 납입보험료 누계금액 × 경과개월수 / (「납입기간 + 3년」 × 12)
② 「납입기간 + 3년」 경과 후 … 해약환급금 = 납입보험료 누계금액
```

with 경과개월수 capped at (납입기간+3)×12. Note the two independent gates — one year elapsed
**and** twelve premiums paid — and that the ramp runs three years past 납입완료, so the cliff
is at 납입기간+3 rather than at 납입완료.

**Design D — nil throughout, then a floor of 100% of premiums.** KDB생명's 해약환급금
미지급형Ⅳ [S8], verbatim:

| 구분 | 해약환급금 |
|---|---|
| 보험료 납입기간 중 | 없음 |
| 보험료 납입기간 경과 후 | 이미 납입한 보험료 × 경과기간별 지급률 |

with 「지급률은 "기준상품의 해약환급률"과 100% 중 큰 비율을 적용합니다」 and 해약환급률
defined as the comparison product's surrender value over its premiums paid at the same
duration [S8]. So the payout is `max(표준형 환급률, 100%) × 이미 납입한 보험료`: a true zero
for twenty years and then a guaranteed return of premium, with upside. The published grid
confirms it — 0.0% at every duration to 15 years, then 100.0% (male) / 100.1% (female) at 20
years, rising to 161.1% / 177.6% at 60 years [S8].

**Design E — a suppression plus a persistency bonus.** 삼성생명's 단기납 design layers a
유지보너스 credited to the 계약자적립액 on top of the 50% suppression, which is what produces
the headline 환급률 above 100% shortly after a five- or seven-year payment period [S7]. §18
sets it out.

**Two clawback-style riders on the mechanic.** KB라이프 require that any unpaid premium be
made good before the post-cliff basis applies: 「[보험료 납입기간 경과 후]에도 납입하지 않은
보험료가 있는 경우, 미납된 보험료를 모두 납입하여야 … 해당하는 해약환급금을 지급합니다」 is
하나생명's wording of the same idea [S2]; KDB생명 [S8] carry it too. And where premiums have
been **waived**, the waived months count as paid for the surrender-value computation [S2] [S3]
[S6] [S8] — so a waiver does not push the policyholder back down the ramp.

### 3. Published surrender-value grids — the citable cash-value basis

These are the most valuable numbers in this file. Five carriers publish complete comparative
grids; the model's surrender-value scale is anchored on them.

**S1 — 처브라이프, 50% suppression, 남자 40세, 가입금액 5,000만원, 10년납, 월납.** Monthly
premium 475,263원 (일부지급형) against 528,453원 (표준형).

| 경과기간 | 일부지급형 납입보험료 | 일부지급형 해지환급금 | 환급률 | 표준형 납입보험료 | 표준형 해지환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 1년 | 5,703,156 | 1,164,500 | 20.4% | 6,341,436 | 2,329,000 | 36.7% |
| 2년 | 11,406,312 | 4,060,500 | 35.5% | 12,682,872 | 8,121,000 | 64.0% |
| 3년 | 17,109,468 | 7,017,250 | 41.0% | 19,024,308 | 14,034,500 | 73.7% |
| 5년 | 28,515,780 | 13,118,250 | 46.0% | 31,707,180 | 26,236,500 | 82.7% |
| 9년 | 51,328,404 | 25,640,000 | 49.9% | 57,072,924 | 51,280,000 | 89.8% |
| 10년 | 57,031,560 | 57,655,500 | 101.0% | 63,414,360 | 57,655,500 | 90.9% |
| 20년 | 57,031,560 | 71,366,000 | 125.1% | 63,414,360 | 71,366,000 | 112.5% |
| 30년 | 57,031,560 | 86,686,500 | 151.9% | 63,414,360 | 86,686,500 | 136.6% |

Internal checks, all pass: 475,263 × 12 = 5,703,156; × 120 = 57,031,560; 528,453 × 12 =
6,341,436. The suppression ratio is exact — 1,164,500 / 2,329,000 = 0.50000, 25,640,000 /
51,280,000 = 0.50000 — and at duration 10 (납입완료) the two surrender values are
**identical** at 57,655,500원, which confirms the suppression is a pure haircut on a common
underlying reserve run-off and not a different policy value [S1].

**The cliff.** From 25,640,000원 at duration 9 to 57,655,500원 at duration 10: a **2.25×**
step in one year, and the 환급률 goes from 49.9% to 101.0%. This is the single feature the
model must reproduce exactly.

**S1 — 처브라이프, 환급률 by 납입기간** (recovered by positional extraction from the p.1
chart; the four lines are 7년납 / 10년납 / 15년납 / 20년납 and the four x-positions are
납입완료시 / 5년 후 / 10년 후 / 20년 후):

| x-position | observed values across the four payment terms |
|---|---|
| 납입완료시 | 100.0% / 101.0% / 102.0% / 104.6% |
| 5년 후 | 111.5% / 112.6% / 113.3% / 115.7% |
| 10년 후 | 124.1% / 125.1% / 125.4% / 127.1% |
| 20년 후 | 147.8% / 149.4% / 151.9% / 151.9% |

The 10년납 line is pinned by the table above — 101.0% at 납입완료, 125.1% ten years later and
151.9% twenty years later — so the ordering at 납입완료시 and at 10년 후 is monotone in the
payment term. The chart's per-line labelling could not be resolved unambiguously at the 20년
후 column, where two lines both read 151.9%; the **range** (147.8%–151.9%) is what this file
relies on, not the per-term attribution [S1].

**S2 — 하나생명, formula design, 40세, 가입금액 5,000만원, 20년납, 월납, 남자.** Monthly
premium 392,000원 (일부지급형) against 415,500원 (일반형).

| 경과기간 | 일부지급형 납입보험료 | 해지환급금 | 환급률 | 일반형 납입보험료 | 해지환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 3개월 | 1,176,000 | 0 | 0.00% | 1,246,500 | 0 | 0.00% |
| 6개월 | 2,352,000 | 0 | 0.00% | 2,493,000 | 0 | 0.00% |
| 9개월 | 3,528,000 | 0 | 0.00% | 3,739,500 | 62,661 | 1.68% |
| 1년 | 4,704,000 | 0 | 0.00% | 4,986,000 | 1,292,714 | 25.93% |
| 1년 1개월 | 5,096,000 | 1,219,400 | 23.93% | 5,401,500 | 1,711,024 | 31.68% |
| 2년 | 9,408,000 | 3,360,000 | 35.71% | 9,972,000 | 6,312,429 | 63.30% |
| 3년 | 14,112,000 | 6,854,400 | 48.57% | 14,958,000 | 11,433,643 | 76.44% |
| 4년 | 18,816,000 | 11,558,400 | 61.43% | 19,944,000 | 16,659,857 | 83.53% |
| 5년 | 23,520,000 | 17,472,000 | 74.29% | 24,930,000 | 21,993,071 | 88.22% |
| 10년 | 47,040,000 | 47,040,000 | 100.00% | 49,860,000 | 48,674,500 | 97.62% |
| 15년 | 70,560,000 | 70,560,000 | 100.00% | 74,790,000 | 76,925,500 | 102.86% |
| 20년 | 94,080,000 | 94,080,000 | 100.00% | 99,720,000 | 107,769,000 | 108.07% |
| 30년 | 94,080,000 | 94,080,000 | 100.00% | 99,720,000 | 128,956,000 | 129.32% |
| 40년 | 94,080,000 | 94,080,000 | 100.00% | 99,720,000 | 149,651,500 | 150.07% |

The female grid runs on the same durations at a monthly premium of 282,500원 (일부지급형)
against 304,000원 (일반형), reaching 100.00% from duration 10 and 156.54% for the 일반형 at
duration 40 [S2]. Two observations that matter for a model:

- **The cliff here is at seven years, not at 납입완료**, and the payment period runs to
  twenty. From duration 7 to duration 40 the 환급률 is flat at exactly 100.00% while the
  comparison product's runs on to 150.07%. So this design has a cliff *and* a permanent
  ceiling: the policyholder never participates in the reserve above premiums paid.
- The 일반형 at 9 months already pays 62,661원 (1.68%) — the underlying reserve turns positive
  during the first year, and the surrender charge is what suppresses it, not the reserve.

**S4 — DB생명, 30% suppression, 남자 40세, 보험가입금액 1억원, 전환나이 60세, 20년 월납.** Two
grids, one per 종. Both re-checked by positional word extraction.

*1종(기본형)* — 표준형 monthly premium 257,050원, 저해지 209,520원:

| 경과기간 | 표준형 납입보험료 | 표준형 해지환급금 | 환급률 | 저해지 납입보험료 | 저해지 해지환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 1년 | 3,084,600 | 0 | 0.0% | 2,514,240 | 0 | 0.0% |
| 3년 | 9,253,800 | 5,087,095 | 55.0% | 7,542,720 | 1,526,128 | 20.2% |
| 5년 | 15,423,000 | 10,940,547 | 70.9% | 12,571,200 | 3,282,164 | 26.1% |
| 10년 | 30,687,000 | 25,283,000 | 82.4% | 25,012,800 | 7,584,900 | 30.3% |
| 15년 | 45,871,500 | 40,501,000 | 88.3% | 37,389,600 | 12,150,300 | 32.5% |
| 20년 | 60,976,500 | 57,838,000 | 94.9% | 49,701,600 | 57,838,000 | 116.4% |
| 40년 | 60,976,500 | 86,326,000 | 141.6% | 49,701,600 | 86,326,000 | 173.7% |
| 60년 | 60,976,500 | 104,604,000 | 171.5% | 49,701,600 | 104,604,000 | 210.5% |

*2종(실속형)* — 표준형 monthly premium 146,470원, 저해지 127,070원:

| 경과기간 | 표준형 납입보험료 | 표준형 해지환급금 | 환급률 | 저해지 납입보험료 | 저해지 해지환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 1년 | 1,757,640 | 0 | 0.0% | 1,524,840 | 0 | 0.0% |
| 3년 | 5,272,920 | 2,223,465 | 42.2% | 4,574,520 | 667,039 | 14.6% |
| 5년 | 8,788,200 | 5,255,732 | 59.8% | 7,624,200 | 1,576,720 | 20.7% |
| 10년 | 17,485,800 | 12,288,000 | 70.3% | 15,169,800 | 3,686,400 | 24.3% |
| 15년 | 26,138,100 | 19,272,000 | 73.7% | 22,676,100 | 5,781,600 | 25.5% |
| 20년 | 34,745,100 | 26,764,000 | 77.0% | 30,143,100 | 26,764,000 | 88.8% |
| 40년 | 34,745,100 | 39,462,000 | 113.6% | 30,143,100 | 39,462,000 | 130.9% |
| 60년 | 34,745,100 | 47,609,000 | 137.0% | 30,143,100 | 47,609,000 | 157.9% |

Suppression checks, all exact to rounding: 1,526,128 / 5,087,095 = 0.30000; 3,282,164 /
10,940,547 = 0.30000; 7,584,900 / 25,283,000 = 0.30000; 12,150,300 / 40,501,000 = 0.30000;
667,039 / 2,223,465 = 0.29999; 3,686,400 / 12,288,000 = 0.30000. At duration 20 (납입완료) the
two surrender values are identical in both grids [S4].

**One internal inconsistency, recorded and not resolved.** The 납입보험료 column is an exact
multiple of the quoted monthly premium at durations 1, 3 and 5 (257,050 × 12 = 3,084,600; × 36
= 9,253,800; × 60 = 15,423,000) but falls 0.5%–1.2% below it at 10, 15 and 20 years (257,050 ×
120 = 30,846,000 against a printed 30,687,000; × 240 = 61,692,000 against 60,976,500). The
brochure's only candidate explanation is its footnote 「상기 예시된 보험료 및 환급률 예시에는
고액계약할인 및 장기납입계약할인이 반영되었습니다」 [S4]; that is not enough to reconstruct
the arithmetic, so the discrepancy is flagged rather than explained. The **suppression
ratios**, which is what this file relies on, are exact at every duration.

**S6 — ABL생명, 50% suppression, 40세 남자, 보험가입금액 1억원, 10년납, 월납, 건강등급
미적용.** Three grids, one per 종. 1종(평준형): premium 407,000원 (일부지급형) against
431,000원 (기본형).

| 경과기간 | 일부지급형 납입보험료 | 해약환급금 | 환급률 | 기본형 납입보험료 | 해약환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 1년 | 4,884,000 | 666,000 | 13.6% | 5,172,000 | 1,332,000 | 25.8% |
| 2년 | 9,768,000 | 2,996,500 | 30.7% | 10,344,000 | 5,993,000 | 57.9% |
| 3년 | 14,652,000 | 5,377,000 | 36.7% | 15,516,000 | 10,754,000 | 69.3% |
| 5년 | 24,420,000 | 10,295,000 | 42.2% | 25,860,000 | 20,590,000 | 79.6% |
| 10년 | 48,840,000 | 45,772,000 | 93.7% | 51,720,000 | 45,772,000 | 88.5% |
| 20년 | 48,840,000 | 55,853,000 | 114.4% | 51,720,000 | 55,853,000 | 108.0% |

2종(체감형), premium 250,000 / 262,000: 1년 212,500 / 425,000 (7.1% / 13.5%); 5년 5,886,000 /
11,772,000 (39.2% / 74.9%); 10년 26,294,000 both (87.6% / 83.6%); 20년 30,074,000 both (100.2%
/ 95.7%). 3종(체증형), premium 580,000 / 617,000: 1년 1,164,000 / 2,328,000 (16.7% / 31.4%);
5년 15,134,000 / 30,268,000 (43.5% / 81.8%); 10년 67,148,000 both (96.5% / 90.7%); 20년
83,020,000 both (119.3% / 112.1%) [S6].

Every pre-완납 ratio is exactly 0.5 and every post-완납 pair is identical. Note that the
**체감형 cash value is much thinner** relative to premiums than the 평준형 — 100.2% at
duration 20 against 114.4% — because the benefit is running off.

**S8 — KDB생명, fully nil design, 40세, 보험가입금액 1억원, 20년납, 월납.** 남자 monthly
premium 218,000원 (654,000 / 3), 여자 191,000원.

| 경과기간 | 남 납입보험료 | 남 해약환급금 | 환급률 | 여 납입보험료 | 여 해약환급금 | 환급률 |
|---|---|---|---|---|---|---|
| 3개월 | 654,000 | 0 | 0.0% | 573,000 | 0 | 0.0% |
| 1년 | 2,616,000 | 0 | 0.0% | 2,292,000 | 0 | 0.0% |
| 3년 | 7,848,000 | 0 | 0.0% | 6,876,000 | 0 | 0.0% |
| 5년 | 13,080,000 | 0 | 0.0% | 11,460,000 | 0 | 0.0% |
| 7년 | 18,312,000 | 0 | 0.0% | 16,044,000 | 0 | 0.0% |
| 10년 | 26,160,000 | 0 | 0.0% | 22,920,000 | 0 | 0.0% |
| 15년 | 39,240,000 | 0 | 0.0% | 34,380,000 | 0 | 0.0% |
| 20년 | 52,320,000 | 52,320,000 | 100.0% | 45,840,000 | 45,900,000 | 100.1% |
| 30년 | 52,320,000 | 62,115,000 | 118.7% | 45,840,000 | 56,860,000 | 124.0% |
| 40년 | 52,320,000 | 72,650,000 | 138.9% | 45,840,000 | 68,931,000 | 150.4% |
| 50년 | 52,320,000 | 79,699,000 | 152.3% | 45,840,000 | 77,008,000 | 168.0% |
| 60년 | 52,320,000 | 84,273,000 | 161.1% | 45,840,000 | 81,402,000 | 177.6% |

This is the extreme case: **twenty years of exactly zero**, then a step to 100% of premiums
paid and a slow climb. A model of this form has no surrender cash flow at all until 납입완료,
which is precisely why the lapse assumption over that period is worth so much CSM and why [R3]
intervened.

**R1 — the supervisor's own worked comparison.** 종신보험, 20년납, 1,000만원, 남 40세 [R1]:

| 구분 | 표준형 | 무해지 (개정 전) | 무해지 (개정 후) |
|---|---|---|---|
| 월 보험료 | 23,300원 | 16,900원 | 14,500원 |
| 10년 환급률 | 86.5% | 0.0% | 0.0% |
| 20년 환급률 | 97.3% | **134.1%** | **97.3%** |

The 2020 rule bites exactly where it is aimed: the pre-amendment product paid 134.1% of
premiums at 납입완료 against the 표준형's 97.3%, and the amendment caps the 무해지 환급률 at
the 표준형's for the whole term. The premium falls a further ~14% as a consequence [R1]. Any
Korean model calibrated on a post-2020 product should therefore expect the post-cliff 환급률
to sit **at or below** the 표준형's, which is what [S2] (flat 100.00%) and [S8] (100.0% then
rising, but off a zero base) both show, and what [S1] [S4] [S6] — where the post-cliff values
are identical to the 표준형's by construction — also show.

### 4. Premium scales and the price of the suppression

Every carrier that publishes both premiums lets the discount be measured directly. It is
**not** the same across the market, and it is much smaller than the surrender-value haircut.

| Carrier | Model point | Suppressed | Comparison | Ratio | Source |
|---|---|---|---|---|---|
| 처브라이프 (50%) | 남 40세, 5,000만원, 10년납 | 475,263 | 528,453 | **89.9%** | [S1] |
| 하나생명 (formula) | 남 40세, 5,000만원, 20년납 | 392,000 | 415,500 | **94.3%** | [S2] |
| 하나생명 (formula) | 여 40세, 5,000만원, 20년납 | 282,500 | 304,000 | **92.9%** | [S2] |
| DB생명 1종 (30%) | 남 40세, 1억원, 20년납 | 209,520 | 257,050 | **81.5%** | [S4] |
| DB생명 2종 (30%) | 남 40세, 1억원, 20년납 | 127,070 | 146,470 | **86.8%** | [S4] |
| ABL생명 1종 (50%) | 남 40세, 1억원, 10년납 | 407,000 | 431,000 | **94.4%** | [S6] |
| ABL생명 2종 (50%) | 남 40세, 1억원, 10년납 | 250,000 | 262,000 | **95.4%** | [S6] |
| ABL생명 3종 (50%) | 남 40세, 1억원, 10년납 | 580,000 | 617,000 | **94.0%** | [S6] |
| FSC illustration | 남 40세, 1,000만원, 20년납 | 14,500 | 23,300 | **62.2%** | [R1] |

The observed range on real products is **81.5% – 95.4%**, with the deepest discount at the
deepest suppression (DB생명's 30%). The FSC's 62.2% [R1] is a much larger discount than any
sold product in the set and is best read as an illustration of a post-amendment design where
the whole of the surrender-value give-up is returned as premium, not as a market observation.

**Full published premium grids.** Three carriers publish grids that a model can calibrate a
rating scale against.

*처브라이프, 5,000만원, 10년납, 월납, 일부지급형* [S1]:

| 성별 | 20세 | 30세 | 40세 | 50세 |
|---|---|---|---|---|
| 남자 | 322,095 | 392,523 | 475,263 | 563,913 |
| 여자 | 288,605 | 353,123 | 432,415 | 524,513 |

Female/male at 40: 432,415 / 475,263 = **91.0%**; at 30, 89.9%; at 50, 93.0%. The female
discount narrows with age.

*DB생명, 1억원, 20년납, 월납* [S4] — the only grid in the set that crosses both 종 and both
forms:

| 성별 | 나이 | 1종 표준형 | 1종 저해지 | 2종 표준형 | 2종 저해지 |
|---|---|---|---|---|---|
| 남자 | 30세 | 200,790 | 163,930 | 119,310 | 102,820 |
| 남자 | 40세 | 257,050 | 209,520 | 146,470 | 127,070 |
| 남자 | 50세 | 330,770 | 270,630 | 197,880 | 171,690 |
| 여자 | 30세 | 177,510 | 146,470 | 101,850 | 90,210 |
| 여자 | 40세 | 224,070 | 181,390 | 123,190 | 106,700 |
| 여자 | 50세 | 289,060 | 231,830 | 159,080 | 135,800 |

*ABL생명, 1억원, 10년납, 월납, 건강등급 미적용* [S6]:

| 종 / form | 남 30세 | 남 40세 | 남 50세 | 여 30세 | 여 40세 | 여 50세 |
|---|---|---|---|---|---|---|
| 1종 평준 일부지급형 | 332,000 | 407,000 | 504,000 | 295,000 | 360,000 | 443,000 |
| 1종 평준 기본형 | 351,000 | 431,000 | 534,000 | 311,000 | 381,000 | 470,000 |
| 2종 체감 일부지급형 | 210,000 | 250,000 | 297,000 | 180,000 | 212,000 | 252,000 |
| 2종 체감 기본형 | 219,000 | 262,000 | 311,000 | 187,000 | 222,000 | 264,000 |
| 3종 체증 일부지급형 | 472,000 | 580,000 | 710,000 | 418,000 | 514,000 | 635,000 |
| 3종 체증 기본형 | 502,000 | 617,000 | 757,000 | 443,000 | 547,000 | 677,000 |

**Discounts on top of the scale.**

- **고액계약할인 (volume discount).** 처브라이프: 「주계약의 보험가입금액이 3,000만원 이상인
  계약에 대하여 주계약 영업보험료를 1.5% 할인하여 이를 영수합니다. (단, 부가특약은 제외)」,
  with the rule that a later change to the 가입금액 re-tests the threshold [S1]. DB생명 note
  their published scale already embeds it [S4].
- **건강등급 할인 (health-grade discount).** ABL생명 apply a grade computed at 청약 and
  **recomputed every year**, discounting the 주계약 영업보험료 by up to 8% and the 선택특약 by
  up to 10%; the published grid gives all four grades. At 남 40세 1종 일부지급형 the grades
  run 374,440 / 378,510 / 386,650 / 394,790 against an ungraded 407,000 — so grade 1 is a
  **8.0%** discount and grade 4 a **3.0%** one [S6]. A premium that is re-rated annually on a
  health measure has no analogue in the other libraries in this repository.
- **선납할인 (advance-payment discount).** 하나생명 discount 3+ months' advance premium at
  「이 보험의 보험료 산출시 적용한 이율」 [S2]; ABL생명 and KB라이프 discount at the
  **평균공시이율** instead [S6] [S3]. KDB생명's universal contract discounts at the 적용이율,
  allows up to 11 months excluding the current one, and accumulates the advance at the
  적용이율 until each due date [S5, art. 24(5)–(7)].

### 5. 예정이율 / 적용이율 — the pricing rate, and it is published

Unlike Japan, where the level-premium 予定利率 is essentially never disclosed, **Korean
carriers publish the pricing rate in the 상품요약서 and often in the brochure**. Five
disclosed values were recovered:

| Rate | Product | Carrier | Date | Source |
|---|---|---|---|---|
| **연복리 2.3%** | 주계약; the 납입면제특약 is 2.5% | 처브라이프 | 2022-04 | [S1] |
| **연복리 2.3%** | 예정적립금 (유니버셜 종신) | KDB생명 | 2021-05 | [S5] |
| **연복리 2.25%** | 「적용한 적용이율은 연복리 2.25%입니다」 | 하나생명 | (판매 2023-02 vintage) | [S2] |
| **연복리 2.25% / 1.75%** | 해약환급금 계산: 2.25% to 10 years, 1.75% after | 삼성생명 | 2023-09 | [S7] |
| **연복리 2.75%** | 「금리확정형 … 연복리 2.75%를 적용이율로」 | KDB생명 | 2024-01 | [S8] |
| **연복리 2.50%** | 추가납입특약 확정이율 | ABL생명 | 2025-09 | [S6] |

The observed level-premium range on retrieved documents is therefore **2.25% – 2.75%** over
2021–2025. 삼성생명's split rate is the interesting one: a **term structure inside the pricing
basis**, 2.25% for the first ten years and 1.75% thereafter [S7], which is not something the
other carriers in the set do and which a model wanting to reproduce their grid would need.

**The vocabulary.** Korean documents mostly say 적용이율 rather than 예정이율 in 상품요약서
prose — 하나생명 gloss it as 「보험료를 납입하는 시점과 보험금을 지급받는 시점 사이에는 시차가
발생하므로 이 기간동안 기대되는 수익을 미리 예상하여 일정한 비율로 보험료를 할인해주는데, 이
할인율」 [S2], KDB생명 identically [S8] — while 예정이율 survives in the policy-loan formulas
[S9] [S11] [S13]. Both mean the pricing interest rate; `krlib` uses 예정이율 as the term of
art and notes the carrier's own word at each cite.

**Direction of travel.** Search results attribute a market-wide 예정이율 cut in April 2025 and
a further one for 2026, and quote a 한화생명 product at 2.7% falling to 2.25% after ten years.
**No such figure was confirmed against a retrieved carrier document** and it is therefore
**[unverified]**; what *is* sourced is the 평균공시이율 series in §6, which moved 2.75% →
2.50% for 2026 [S10].

### 6. 공시이율, 공시기준이율, 최저보증이율, 평균공시이율

Korea runs three distinct declared-rate concepts and one industry average, and a whole life
model touches all four.

**공시이율 (declared crediting rate).** Reset monthly, applied to the 계약자적립금 of a
금리연동형 contract. KDB생명's 약관 gives the mechanism verbatim [S5, art. 32]:

> ① 이 계약의 계약자적립금 계산시 적용되는 이율은 매월 1일 회사가 정한 신공시이율(보장Ⅳ)
> (최저보증이율은 연복리 0.75%를 적용)로 합니다.
> ② 제1항의 신공시이율(보장Ⅳ)는 이 계약의 사업방법서에서 정하는 바에 따라 운용자산수익률과
> 외부지표금리를 가중평균하여 산출된 일반계정 신공시기준이율에서 향후 예상수익 등을 고려한
> 조정률을 가감하여 결정합니다.
> ③ 회사는 … 신공시이율(보장Ⅳ) 및 산출방법 등을 매월 회사의 인터넷 홈페이지 등을 통해
> 공시합니다.

So: **공시이율 = 공시기준이율 ± 조정률**, where the 공시기준이율 is a weighted average of the
insurer's 운용자산수익률 and an 외부지표금리 defined as 「국고채, 회사채, 통화안정증권,
양도성예금증서 수익률을 기준으로 산출」 [S5]. Search results state that the 조정률 is capped
at ±30% of the 공시기준이율 under the 보험업감독규정; that cap could **not** be confirmed
against a retrieved document and is **[unverified]**.

**공시기준이율, a published level.** 교보생명's disclosure page returned 공시기준이율 3.19 /
적용률 3.19 / 적용이율 3.19 across 보장(무배당), 연금(무배당), 연금(배당), 저축(무배당) and
연금저축(배당) — but **without an as-of month**, because the month is a form selection the
fetch did not make [S15]. The figure is recorded with that caveat and should not be presented
as current.

**최저보증이율 (the guaranteed floor).** Two shapes appear:

- A **flat floor**: KDB생명's 유니버셜 종신, 연복리 **0.75%**, with a worked example in the
  약관 — 「계약자적립금이 신공시이율(보장Ⅳ)에 따라 적립되며 신공시이율(보장Ⅳ)가 0.5%인
  경우(최저보증이율은 0.75%일 경우), 계약자적립금은 … 최저보증이율(0.75%)로 적립됩니다」 [S5,
  art. 31(3)].
- A **duration-stepped floor**: 하나생명's 연금전환특약 — 「전환일부터 5년 이내에는 연복리
  1.25%, 5년 초과 10년 이내인 경우에는 연복리 1.0%, 10년 초과인 경우에는 연복리 0.5%」 [S2].
  ABL생명 carry the identical ladder [S6]. That 1.25 / 1.00 / 0.50 ladder is the Korean market
  standard for annuity-conversion riders on this chassis.

**평균공시이율 (the industry average declared rate).** Set by the 금융감독원장 and applied for
the whole term of a contract concluded in that year; used for 선납 discounting [S3] [S6] and
as the reference in the 보험가격지수 [S2] [S8]. 하나생명's disclosure gives the whole series
[S10]:

| 적용기간 | 평균공시이율 |
|---|---|
| 2026-01-01 ~ 2026-12-31 | **2.50%** |
| 2025-01-01 ~ 2025-12-31 | 2.75% |
| 2024-01-01 ~ 2024-12-31 | 2.75% |
| 2023-01-01 ~ 2023-12-31 | 2.25% |
| 2022-01-01 ~ 2022-12-31 | 2.25% |
| 2021-01-01 ~ 2021-12-31 | 2.25% |
| 2020-01-01 ~ 2020-12-31 | 2.50% |
| 2019-01-01 ~ 2019-12-31 | 2.50% |
| 2018-01-01 ~ 2018-12-31 | 2.50% |
| 2017-01-01 ~ 2017-12-31 | 3.00% |
| 2016-01-01 ~ 2016-12-31 | 3.50% |

ABL생명's brochure independently corroborates the 2025 value: 「(2025년 현재 평균공시이율
연복리 2.75%)」 [S6]. The same page also carries the **표준이율** — 2013-04-01~2013-12-31 and
2014 at 3.50%, 2015 at 3.25% [S10] — which was the statutory valuation rate before the
economic-value regime; it is not maintained past 2015 on that page, consistent with its
replacement.

**금리확정형 vs 금리연동형.** KDB생명's 우리가바라던 종신보험 is explicitly 금리확정형 at a
fixed 2.75% [S8]; the 유니버셜 종신 is 금리연동형 on the 신공시이율 with a 0.75% floor [S5].
[R8]'s taxonomy table describes the pair in the same terms and adds 실적배당 (변액) and 보험료
수정 (stepped-premium) shapes [R8]. `krlib`'s representative product is **금리확정형**,
because that is what the retrieved 상품요약서 with published cash values are.

### 7. 보험료적립금 / 계약자적립액 and the contractual definition of 해지환급금

The 약관 itself is short here: 「이 약관에 따른 해지환급금은 산출방법서에 따라 계산합니다」
[S5, art. 31(1)]. The substance lives in the 상품요약서, and two carriers state it in one
sentence each — differently, and both are worth quoting because the difference is the whole
IFRS 17 transition.

하나생명 (a pre-2023 wording): 「보험료 계산시 적용한 위험률로 산출한 **순보험료식
책임준비금**에서 **해지공제액**을 공제한 금액을 해지환급금으로 지급합니다」 [S2].

KDB생명 (2024-01): 「보험료 계산시 적용한 위험률로 산출한 **계약자적립액**에서
**미상각신계약비**를 공제한 금액을 해약환급금으로 지급합니다」 [S8].

So the identity is, in both wordings,

```
해지환급금 = 적립금 − 해지공제액
```

where the 적립금 is a net-level-premium reserve (순보험료식 책임준비금 / 계약자적립액) and the
deduction is unamortised acquisition cost (미상각신계약비), bounded above by the
표준해약공제액 (§8). DB생명's brochure names the same object in one breath: 「사업비(미상각
신계약비(해지공제액) 포함)」 [S4]. The 계약자적립액 wording is the post-IFRS-17 one — under
K-IFRS 1117 the insurer no longer books a 보험료적립금 and a 미경과보험료적립금 as separate
statutory reserves, so the surrender basis had to be re-anchored on a contractually defined
policyholder account rather than on a balance-sheet reserve; search results state this
explicitly but no retrieved document confirms the reasoning, so that causal claim is
**[unverified]**. The *wording difference itself* is sourced [S2] [S8].

KDB생명's 약관 defines the account machinery in full, and it is the cleanest statement of the
Korean account-value convention anywhere in this file [S5, art. 2]:

- **예정적립금** — 「영업보험료 및 이전 예정적립금에서 예정월대체보험료 및 중도인출금액을
  공제한 금액을 이 계약의 적용이율(연복리 2.3%)로 납입일 … 부터 일자계산에 의하여 적립한
  금액」. The *pricing-basis* account.
- **계약자적립금** — the same recursion but 「신공시이율(보장Ⅳ)로」 and net of the actual
  월대체보험료. The *credited* account.
- **월대체보험료** — for a monthly contract in its first 24 months, 「해당 월의 위험보험료,
  부가보험료, 최저사망보험금 보증비용, 최저해지환급금 보증비용 및 … 특약보험료의 합계액」,
  deducted from the 계약자적립금 when the basic premium is paid; after 24 months the same less
  the 기타비용 component of the 계약관리비용, deducted from **「계약자적립금에서 해지공제액을
  차감한 금액」** at each monthly anniversary.
- **부가보험료** — 「이 계약에 부가된 계약체결비용 및 계약관리비용(유지관련비용 및
  기타비용)」.
- **해지공제액** — 「이미 지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라
  계산한 금액」.

That last definition is the load-bearing one: the surrender charge is *unrecovered acquisition
cost*, defined by reference to what was spent, and the 표준해약공제액 caps it.

Two further 약관 provisions that a model must respect [S5]:

- 「회사는 경과기간별 해지환급금에 관한 표를 계약자에게 제공하여 드립니다」 [art. 31(6)] — the
  duration-by-duration surrender table is a **contractual deliverable**, which is why every
  document in §3 carries one.
- Surrender proceeds are payable 「청구를 접수한 날부터 3영업일 이내」 with interest to the
  payment date per 부표3 [art. 31(2)].

### 8. 해지공제 and the 표준해약공제액 cap

The surrender charge is capped by regulation. The formula, from the 보험연구원 public hearing
presentation [R6]:

| 상품 구분 | 표준해약공제액 |
|---|---|
| **보장성보험** | 연납순보험료의 5% × 보험기간(최대 20년) + 보장성보험의 보험가입금액의 10/1000 |
| **저축성보험** | 연납순보험료의 5% × 납입기간(최대 12년) |

with 연납순보험료 defined in the same slide as 「가입자가 연간 납입한 보험료에서 사업비를
차감한 금액」, and a worked example on a 연납순보험료 of 100 and a 보험가입금액 of 1,000:
(보장) 100 × 5% × 20년 + 1,000 × 1% = **110**; (저축) 100 × 5% × 12년 = **60** [R6].

Read against a 종신보험: on a 보험기간 종신 the 보험기간 term hits its 20-year cap, so the
보장성 formula reduces to `0.05 × 20 × 연납순보험료 + 0.01 × 보험가입금액` = **한 해
순보험료의 1배 + 가입금액의 1%**. On the [R1] model point (1,000만원, 남 40세, 20년납, 표준형
premium 23,300원/month) that is of the order of a full year's premium plus 10만원. `krlib`
treats this as the **cap on the model's surrender charge**, not as the charge itself.

Two supervisory overlays sit on top [R5]:

- The **13배 / 3배 rule** — 「표준해약공제액 한도: 보장성보험 월 보험료의 13배 수준,
  저축성보험 월 보험료의 3배 수준」, and the requirement that the savings-like portion of a
  보장성보험 carry 저축성-level 사업비 and 해약공제 「해약공제액 등을 현행의 70% 수준으로
  적용」.
- The **모집수수료 분급 rule** — 「연간 수수료는 표준해약공제액의 60%이하, 분급수수료 총액이
  선지급방식 총액 대비 5%이상」, with an illustration of 900/100 up-front against 600/450
  instalment [R5]. Timetable: expense reform to April 2020, commission reform from January
  2021.

[R6] also records that competition had pushed carriers past the cap — 「보험회사 간 경쟁심화로
표준해약공제액을 초과하는 사업비를 부가하는 상품 존재」 — and that the policy answer was a
disclosure obligation on such products rather than a hard prohibition [R6].

**The exact 보험업감독규정 / 시행세칙 article and 별표 number for the 표준해약공제액 was not
retrieved** ([R10] [R11] both returned only site chrome), so the formula above rests on [R6],
a research presentation to a public hearing, and the caps on [R5], a press release. Both are
authoritative secondary statements of the rule but neither is the rule text. Flag any
downstream use accordingly.

### 9. 사업비 — 계약체결비용, 계약관리비용, and the 보험가격지수

Korea splits acquisition and maintenance expense into two named contractual categories, and
both appear inside the 약관's own definitions [S5, art. 2]:

- **계약체결비용** — [R5]: 「설계사의 보험계약 모집노력에 대한 수수료, 영업점포 운영비용, 건강
  진단비, 광고비 등 계약체결에 사용되는 비용」.
- **계약관리비용** — [R5]: 「보험사 임직원 급여, 전산비 등 보험회사 운영에 필요한 경비」,
  subdivided in the 약관 into **유지관련비용** and **기타비용**, with a further split of
  유지관리비용 into 납입중 and 납입후 [S5].

Both 상품요약서 in the set define the pair identically and then **decline to give a number**:
「계약체결비용 및 계약관리비용이란 보험회사가 보험계약의 체결, 유지 및 관리 등에 필요한 경비로
사용하기 위하여 보험료 중 일정비율을 책정한 것을 말합니다」 — and that is the whole of the
section in both [S2] [S8]. **No expense rate as a percentage of premium was obtained from any
document in this session.** This is the single largest quantitative gap in the file and every
사업비 parameter in `krlib`'s whole life model is therefore **[std]**, bounded by the
표준해약공제액 (§8) and by the 보험가격지수 (below).

**보험가격지수 (price index).** This *is* published, per product, and it is the closest thing
to an expense disclosure Korea provides. Definition, quoted from [S8] (re-spaced; the source
extracts without inter-word spaces):

> 해당상품의 보험료총액(보험금지급을 위한 보험료 및 보험회사의 사업경비 등을 위한 보험료)을
> 참조순보험료 총액*과 평균사업비총액**을 합한 금액으로 나눈 비율
> \* 감독원장이 정하는 바에 따라 산정한 전체 보험회사 공시이율의 평균(평균공시이율),
>   평균해지율 및 참조순보험요율을 적용하여 산출한 보험금 지급을 위한 보험료
> \*\* 상품군별 생명보험상품 전체의 평균 사업비율을 반영하여 계산(역산)한 값

하나생명's wording is the same but its denominator note omits 평균해지율 [S2] — a small but
real difference, since the index for a 무해지 product is sensitive to whether the reference
premium is computed with a lapse assumption.

Published values, 40세 기준, 월납 [S2] [S8]:

| 상품 | 보험기간 | 납입기간 | 가입금액 | 남자 | 여자 |
|---|---|---|---|---|---|
| (무)하나로 연결된 든든한 종신보험 (해지환급금 일부지급형) | 종신 | 20년 | 1억원 | **85.4%** | **86.2%** |
| (무)우리가바라던 종신보험 — 가입금액형 미지급형Ⅳ | 종신 | 20년 | 1억원 | **110.3%** | **110.9%** |
| (무)우리가바라던 종신보험 — 기납입P플러스형 미지급형Ⅳ | 종신 | 20년 | 1억원 | **107.6%** | **106.9%** |

An index of 100% means the product's total premium equals the reference net premium plus the
industry-average expense allowance. 하나생명's product at 85.4% is priced roughly 15% below
that reference; KDB생명's at 110.3% roughly 10% above. The observed range across two carriers
is **85.4% – 110.9%**, which is a usable — if very loose — bound on how far a Korean whole
life product's total loading can sit from the industry mean.

### 10. 적용해지율 — the pricing lapse assumption, and it is disclosed

This is the most surprising disclosure in the Korean set and has no analogue in the other
libraries in this repository: **the 상품요약서 publishes the lapse assumption used to price
the product**, and states that the comparison product carries none.

하나생명 [S2], verbatim:

> Q : 적용해지율이란 무엇인가요?
> A : 한 개인이 보험료 납입기간 중 계약을 해지할 확률을 예측한 것을 말합니다. 일반적으로
> 적용해지율이 높으면 보험료는 내려가고, 낮으면 보험료는 올라갑니다.
> 「무배당 하나로 연결된 든든한 종신보험(해지환급금 일부지급형)」에 적용한 해지율은
> **1%~10%**이며, **일반형에는 적용해지율이 적용되지 않습니다.**

KDB생명 [S8], verbatim:

> 무배당 우리가바라던 종신보험 해약환급금 미지급형Ⅳ에 적용한 적용해약률은 보험료 납입기간
> 및 경과기간별로 상이하며, 보험료 납입기간 중 **연 0%~연 13.4%**를 적용합니다. 보험료
> 납입기간 이후에는 **연 1.0%~연 11.3%**의 해약률을 적용합니다.

Three things follow directly:

1. **The comparison ("표준형") product's surrender value is a zero-lapse computation.** Every
   carrier in the set says so in the same words [S1] [S2] [S3] [S4]. So the 표준형 curve in §3
   is the reserve run-off with no lapse-supported profit at all, and the sold product's
   suppressed curve is that curve times a haircut. A model that reproduces the 표준형 curve
   and applies the carrier's stated fraction reproduces both.
2. **The disclosed range is wide and duration-shaped.** 0% to 13.4% during the payment period
   at KDB생명 [S8], 1% to 10% at 하나생명 [S2]. Neither publishes the shape, only the
   envelope, so a duration-by-duration lapse curve is a **[std]** construction bounded by
   these envelopes.
3. **The post-payment lapse assumption is not zero.** KDB생명 price 1.0%–11.3% after 납입완료
   [S8] — materially above the 0.8% the supervisor later set as the reference ultimate rate
   [R3]. That gap is exactly the subject of §11.

Note also that KDB생명's post-완납 lapse assumption reaching 11.3% is interesting on a design
whose surrender value at that point is 100%+ of premiums paid: high lapse on a policy that is
worth more dead than alive to the insurer is a *cost*, not a profit source, which is why the
K-ICS shock in §11 splits by whether surrender reduces or increases net assets.

### 11. The 2024 supervisory intervention on the 무·저해지 해지율 assumption

The single most consequential regulatory event for this product, and the reason `krlib`'s
lapse basis is documented rather than assumed.

**The problem, stated by the supervisor** [R3] and restated by [R7]: 「무·저해지 상품은
납입기간 중 해지 시 환급금이 없거나 적은 상품임에도 완납 직전까지 해지가 발생한다고 가정하여
낮은 보험료로 인해 상품의 쏠림현상이 심화됨」. Carriers assumed lapse right up to the day
before 납입완료 on contracts where lapsing pays nothing — which under IFRS 17 books CSM the
insurer will never realise, and under the pricing basis produces a premium low enough to
distort the whole market toward the form.

**The scale of the distortion** [R7]: 「무·저해지 보장성상품의 초회보험료 비중이 2018년
**11.4%**에서 2021년 **30.4%**, 2023년 **47.0%**로 급증함」. A widely reported 2024 H1 figure
of 63.8% appears in search results but **could not be confirmed** against [R3] or [R7] as
retrieved, and is **[unverified]**.

**The remedy** [R3] [R7]:

- Where experience is sufficient, use it. Where it is not, apply a **log-linear model** whose
  lapse rate **converges to 0.1% at 납입완료** — 「완납시점 해지율이 0.1%에 수렴하도록
  로그-선형모형을 적용하는 원칙」 [R7]. This is designated the 원칙모형.
- **After 납입완료**, apply either **0.8%** (from overseas statistics) or a **20%** relative
  to the 표준형 product's rate — 「해외통계의 0.8% 또는 해외 표준형 대비 저해지 상품 해지율
  상대도 20%를 적용함」 [R7].
- A carrier using a non-principle model (선형-로그 or 로그-로그) must (i) describe the model
  choice and its difference from the 원칙모형 in the audit report and 경영공시 including the
  CSM, K-ICS ratio and net income impact, (ii) obtain external actuarial validation, and (iii)
  report quarterly to the FSS [R3] [R7].
- On **단기납 종신** specifically, where a 유지보너스 pushes the surrender value above
  premiums paid at a point in time, the model must carry an **additional lapse spike** at that
  point, either back-solved from the 표준형 product's cumulative lapse or set at a floor of
  **30%** and documented [R3] [R7]. The industry evidence quoted is a 10-year lapse of
  **29.4%~30.2%** at policy year 11 on bancassurance single-premium savings [R3].
- Effective from the **2024 year-end** close, with the loss-ratio assumptions and the
  discount-curve extension following in Q1 2025 [R3].

**The K-ICS side.** 해지위험액 is the greater of 옵션행사위험액 and 대량해지위험액, and the
대량해지 shock was re-cut to distinguish the two forms [R7, sourced to 보험업감독업무 시행세칙
별표 22]:

| 구분 | 산출 방법 |
|---|---|
| 표준형 | 저축성보험 계약 **35%**, 보장성보험 계약 **25%** 일시해지 |
| 저해지환급형 — 고환급형 | 순자산 감소상품: 향후 1년 해지율 **+ 35%p**; 순자산 증가상품: 향후 1년 해지율 **× (1 − 40%)** |
| 저해지환급형 — 비고환급형 | 순자산 감소상품: 향후 1년 해지율 **+ 25%p**; 순자산 증가상품: 향후 1년 해지율 **× (1 − 40%)** |

with 고환급형 defined as 「경과기간 시점별 '기납입보험료 대비 해약환급금 비율'이 '기납입
보험료 대비 기납입보험료를 평균공시이율로 부리한 금액의 비율'보다 큰 시점이 존재하는 상품」
[R7] — i.e. a product that at some duration returns more than premiums rolled up at the
평균공시이율. Note the **직접적 dependence on the 평균공시이율 series in §6**: the same
product can be 고환급형 in one issue year and not in another purely because the 평균공시이율
moved.

**The 해약환급금준비금 overlay.** A distributable-earnings reserve with no counterpart
elsewhere in this repository: 「시가평가된 IFRS17 보험부채가 해약환급금보다 작은 경우 그
부족액을 자본의 이익잉여금 내에 적립하여 계약자 보호를 위해 사외유출을 방지함」 [R7]. It stood
at **23.7조원 at end-2022** and **32.2조원 at end-2023**, a 8.5조원 (36%) rise in one year
[R7]. From the 2024 close the accumulation ratio is graded by K-ICS ratio, per the
보험업감독규정 부칙 [R7]:

| 적립비율 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 |
|---|---|---|---|---|---|---|
| 80% 적립 | K-ICS 200% 이상 | 190% 이상 | 180% 이상 | 170% 이상 | 160% 이상 | 150% 이상 |
| 90% 적립 | 150~200% 미만 | 150~190% 미만 | 150~180% 미만 | 150~170% 미만 | 150~160% 미만 | — |

This matters to a whole life model only indirectly — it is a capital and distribution
constraint, not a liability measure — but it is the reason a Korean insurer's economics on a
무해지 product depend on the *surrender value* and not only on the fair-valued liability.

### 12. 보험계약대출 (policy loan)

Universal on this chassis, and the mechanics are unusually uniform across carriers.

**The 약관 text** [S5, art. 34]:

> ① 계약자는 이 계약의 해지환급금(다만, 보험계약대출의 원금과 이자를 차감한 금액) 범위
> 내에서 회사가 정한 방법에 따라 대출(이하 "보험계약대출"이라 합니다)을 받을 수 있습니다.
> 그러나, 순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수 있습니다.
> ② 계약자는 … 언제든지 상환할 수 있으며 상환하지 않은 때에는 회사는 보험금, 해지환급금 등의
> 지급사유가 발생한 날에 지급금에서 보험계약대출의 원금과 이자를 차감할 수 있습니다.
> ③ 회사는 제25조 … 에 따라 계약이 해지되는 때에는 즉시 해지환급금에서 보험계약대출의
> 원금과 이자를 차감합니다.

**The rate is a vintage rate, not a market rate.** The formula is the same at every carrier
retrieved:

| Carrier | 금리확정형 | 금리연동형 | Source |
|---|---|---|---|
| 하나생명 (2013-04-01~) | 적용이율 + 1.5% | 공시이율 + 1.5% | [S9] |
| 하나생명 (2012-04~2013-03) | 예정이율 + 1.5% | 공시이율 + 1.5% | [S9] |
| 하나생명 (2010-10~2012-03) | 예정이율 + 2% | 공시이율 + 1.5% | [S9] |
| 교보생명 | 예정이율 + 1.40~1.50% | 공시이율 + 1.50% | [S11] |
| 신한라이프 | 예정이율 + 1.5% | 공시이율 + 1.5% | [S13] |
| KDB생명 (약관) | — | 신공시이율(보장Ⅳ) + 회사가 정하는 이율 | [S5] |

Because the base is the **contract's own** 예정이율, a policy written in a high-rate era
carries a high loan rate for life. AIA생명 publish the whole historical 가산금리 schedule
[S12]:

| 적용기간 | 가산금리 | 최고 적용 대출이율 |
|---|---|---|
| 2026-01-01 ~ | +1.50% | 최고 9.90% |
| 2025-12-01 ~ | +1.50% | 최고 9.90% |
| 2024-02-01 ~ 2025-11-30 | +1.50% | 최고 9.90% |
| 2020-12-01 ~ 2024-01-31 | +1.90% | 최고 9.90% |
| 2018-11-01 ~ 2020-11-30 | +2.00% | 최고 9.90% |
| 2013-12-01 ~ 2018-10-31 | +2.50% | 최고 9.90% |
| 2011-07-01 ~ 2012-06-24 | +2.80% | — |
| 2010-10-01 ~ 2011-06-30 | +2.80% | 최고 8.50% |
| 2005-02-01 ~ 2010-09-30 | fixed 8.50% | — |
| 2003-07-01 ~ 2005-01-31 | fixed 10.00% | — |

with concessions of −0.1% for 자동대출납입 and for insureds aged 65+ from 2025-12 / 2026-01
[S12]. 교보생명 and 신한라이프 carry structurally identical concessions — 교보 −0.10%p on
contracts with 예정이율 ≥ 7% from 2025-11-27 [S11], 신한 −0.1% for insureds 65+ on contracts
with 예정이율 ≥ 5.5% [S13].

**Loan limit as a fraction of the surrender value**, and this is where Korea differs sharply
from Japan's uniform 9/10–8/10:

| Carrier | Limit | Source |
|---|---|---|
| 교보생명 | 「해약환급금의 50% ~ 85%까지 (주계약 및 특정특약의 해약환급금 범위 내에서 보험상품에 따라 변동)」 | [S11] |
| 신한라이프 | 「해약환급금의 50 ~ 80%이내」 | [S13] |
| KDB생명 (약관) | the whole 해지환급금 net of existing loan, with 「순수보장성보험 등 … 제한될 수 있습니다」 | [S5] |

**Published rate levels.** 교보생명 quote a live range of **연 3.5% ~ 10.5%** [S11]; AIA cap
at **9.90%** [S12]. The 손해보험협회 comparison grid for 산출기준월 2026-07 gives, for
non-life insurers [S14]:

| 보험회사 | 상품구분 | 기준금리 | 가산금리 | 대출금리 |
|---|---|---|---|---|
| 메리츠화재 | 금리확정형 | 4.17% | 1.20% | 5.37% |
| 메리츠화재 | 금리연동형 | 3.06% | 1.20% | 4.26% |
| 한화손보 | 금리확정형 | 2.84% | 1.50% | 4.34% |
| 한화손보 | 금리연동형 | 2.36% | 1.50% | 3.86% |
| 삼성화재 | 금리확정형 | 6.35% | 1.16% | 7.51% |
| 삼성화재 | 금리연동형 | 2.77% | 1.50% | 4.27% |
| DB손보 | 금리확정형 | 5.37% | 1.39% | 6.76% |
| DB손보 | 금리연동형 | 2.50% | 1.49% | 3.99% |

These are **non-life** insurers and therefore bound the market rather than evidence the life
product; the equivalent 생명보험협회 grid was not obtained (see "Fetch failures"). Note how
far apart the 금리확정형 base rates are — 2.84% to 6.35% — which is the vintage effect made
visible.

**The interaction with the suppression.** The FSS state it plainly: a 무해지환급금 contract
**cannot support a policy loan during the payment period**, because there is no surrender
value to lend against [R4]. That is a real consumer-detriment finding and a real modelling
consequence: on Design D [S8] the policy loan simply does not exist for twenty years.

**No 자동대출납입 (automatic premium loan) provision was found in any retrieved 약관** for a
conventional 종신보험. The 생명보험 표준약관 is known to contain a 보험료의 자동대출납입
article and search results describe it, but the 표준약관 text itself was **not retrieved**
(see "Fetch failures"), and KDB생명's universal 약관 handles non-payment through the
월대체보험료 mechanism instead [S5]. Treating APL as a standard Korean whole life feature
would be **[unverified]**.

### 13. 보험료 납입면제 (premium waiver)

The Korean substitute for Japan's 高度障害保険金, and structurally different from it: the
contract continues, the premiums stop, and **the benefit and surrender value are computed as
if the premiums had been paid**.

**The base trigger is disability**, and it is worded almost identically at four carriers:
「보험료 납입기간 중 피보험자가 장해분류표 중 동일한 재해 또는 재해 이외의 동일한 원인으로
여러 신체 부위의 장해지급률을 더하여 **50% 이상**의 장해상태가 되었을 경우에는 다음 회 이후의
보험료 납입을 면제」 [S2] [S3] [S6] [S8]. Note the aggregation rule — several body parts, one
cause — and that it covers both 재해 and non-accident causes.

**The "deemed paid" rule is what makes it a modelling problem.** 하나생명: 「그러나 이
경우에도 보험료가 보험료 납입기간 종료일까지 월계약해당일에 정상적으로 납입된 것으로 하여
사망보험금 및 해지환급금을 계산합니다」 [S2]; KB라이프 [S3] and KDB생명 [S8] carry it
verbatim. So a waived policy accrues surrender value on the full premium scale while paying
nothing — it is a genuine option with value, and on a Design B or D contract it is the *only*
way to reach the cliff without paying.

**Disease riders extend the trigger.** Three shapes appear:

- **3대질병** — 암 (excluding 기타피부암, 갑상선암 and 대장점막내암), 뇌출혈, 급성심근경색증:
  하나생명's (무)3대질병 납입면제특약 [S2]; KB라이프's (무)3대질병보험료납입면제특약Ⅱ, whose
  cancer exclusion list is the narrower 「기타피부암, 중증갑상선암 이외의 갑상선암 및
  대장점막내암 제외」 [S3]; 처브라이프's 더하고 채우는 보험료납입면제특약(무) on the same
  three [S1].
- **6대질병** — ABL생명's (무)6대질병보험료납입면제특약 [S6].
- KDB생명's universal contract offers 2종(장해50%), 3종(재해장해50%), a 3대질병형 and a
  6대질병형 as separate riders [S5].

**A 90-day 면책기간 applies to the cancer trigger.** KB라이프: 「암 … 에 대한 보장개시일은
계약일로부터 그 날을 포함하여 90일이 지난날의 다음 날부터입니다」 [S3]; KDB생명 note it in the
rider summary as 「암의 경우 가입 후 90일간 납입면제 제외」 [S5]. 처브라이프 add the two rules
that go with it: a policyholder diagnosed before the 암보장개시일 may cancel the rider within
90 days of diagnosis and have the premiums returned; if they do not, a later recurrence or
metastasis of that same cancer never triggers the waiver — unless the 암보장개시일 has passed
by five years with no further diagnosis or treatment, in which case the waiver revives [S1].

**Rider attachment conditions.** 처브라이프 require that the 주계약 and every attached rider
share the same 납입기간, bar mid-term attachment, cap the combined monthly premium at 50만원,
bar the annual mode, and bar the rider alongside five named 진단특약 [S1]. 하나생명's rider
runs 20년 만기 / 20년납 to match the 주계약 [S2].

### 14. 감액, and the two options Korea does *not* have

**감액 (partial surrender by reducing the sum assured) is universal**, and the 약관 treats it
as a partial termination [S5, art. 20(2)]:

> 회사는 계약자가 … 보험가입금액을 감액하고자 할 때에는 그 감액된 부분은 해지된 것으로
> 보며, 이로써 회사가 지급하여야 할 해지환급금이 있을 때에는 제31조(해지환급금) 제1항에 의한
> 해지환급금을 계약자에게 지급합니다.

with a warning that 「보험가입금액을 감액하면 해지환급금이 없거나 최초 가입할 때 안내한
해지환급금보다 적어질 수 있습니다」 — which on a suppressed contract is not a caveat but the
main event. The 약관 then gives three pro-rata restatement formulas with worked examples, and
they matter because the death benefit on several designs depends on premiums paid [S5, art.
20(4)]:

```
감액 후 이미 납입한 보험료
  = 감액 전 이미 납입한 보험료 × (감액 후 계약자적립금 / 감액 전 계약자적립금)
감액 후 중도인출 누적액
  = 감액 전 중도인출 누적액 × (감액 후 보험가입금액 / 감액 전 보험가입금액)
감액 후 초과납입액
  = 감액 전 초과납입액 × (감액 후 보험가입금액 / 감액 전 보험가입금액)
```

Worked example from the 약관: 감액 전 이미 납입한 보험료 1,000만원, 계약자적립금 1,200만원 →
600만원 gives 감액 후 이미 납입한 보험료 = 1,000 × 600/1,200 = **500만원** [S5]. KDB생명's
우리가바라던 종신보험 applies the corresponding 보험가입금액-ratio version to the 기납입P
플러스형 death benefit [S8].

**ABL생명 turn 감액 into a product feature.** Their **생활설계자금** pays an annual income by
automatically reducing the sum assured and paying out the resulting surrender value, for 2 to
20 years, from 납입완료 to age 90, in either a 정액지급 or a 정액감액 mode, subject to the
remaining sum assured staying at least the greater of 20% of the pre-application amount and
2,000만원; a policy loan must be repaid first, and no 감액 or new loan is possible during the
payment period [S6]. This is a decumulation option built out of partial surrender and it has
no analogue in the other libraries here.

**감액완납 (reduced paid-up) and 연장정기보험 (extended term) do not appear in any retrieved
Korean 약관.** The 60-article KDB생명 약관 [S5] has no such article: 제20조 offers only
보험가입금액, 계약자 and 「기타 계약의 내용」 as variables, and the 상품요약서 in the set are
silent. Search results describe both as maintenance options available in the Korean market
generally — 감액완납 as stopping premiums and using the accumulated value to pay up a reduced
sum assured, typically requiring about half the payment period elapsed, and 연장정기보험 as
converting whole life into term for the period the surrender value will fund — but **neither
was confirmed against any retrieved primary document**, so both are **[unverified]** as
features of a Korean 종신보험 contract. The equivalent Japanese options (払済保険,
延長定期保険) *are* in the Japanese 約款 [see jplib]; treating them as universal across Asia
would be wrong. What Korea offers instead, and what *is* sourced, is the payment holiday on a
universal chassis (§15) and 감액 (above).

### 15. 중도인출 and the 유니버셜 chassis

KDB생명's universal 약관 is the only full statement of this machinery retrieved, and it is
worth setting out because `Pension_KR_S` and `VA_KR_S` inherit it.

**Free premium payment and payment holidays** [S5, art. 24(1)]: for the first 24 monthly
premiums the basic premium must be paid on time; thereafter 「「계약자적립금에서 해지공제액을
차감한 금액」 … 에서 해당 월의 월대체보험료를 충당할 수 있을 경우에 한하여 보험료의 납입을
일시적으로 중지할 수 있습니다」. Any premium paid beyond the scheduled basic premium becomes
추가보험료 once cumulative payments exceed the 기본보험료 총액 [art. 24(2)].

**추가보험료 한도** [S5, art. 2]: total limit 100% of the 월납 기본보험료 총액 (기본보험료 ×
12 × 납입기간); annual limit 「월납 기본보험료 × 12 × 경과년수 × 100% − 이미 납입한
추가보험료의 합계」, with 경과년수 counting the year of issue as 1 and capped at the payment
period. A 중도인출 restores headroom: 「중도인출이 있으면 인출한 금액만큼 추가로 보험료 납입이
가능합니다」.

**중도인출** [S5, art. 33]: available after 「보험료 납입경과기간 2년(24회 납입)」, up to **12
times per 보험년도**; a single withdrawal may not exceed **50%** of 「기본보험료
계약자적립금에서 해지공제액을 차감한 금액」 plus the whole of the 추가보험료 계약자적립금;
cumulative withdrawals may not exceed total premiums paid; the order is 추가보험료 account
first; and after any withdrawal the residual basic account net of the surrender charge must be
at least 「보험가입금액의 10%해당액과 이미 납입한 기본보험료의 10%해당액 중 **적은** 금액」.
The 약관 gives two worked examples, including one where the 50% rule would allow 50만원 but
the residual floor cuts it to 40만원 [S5].

**처브라이프 run a lighter version on a non-universal chassis**: 추가계약자적립금 인출 with
「인출에 대한 수수료는 없고, 인출금액은 10만원이상 만원단위로 합니다. 다만, 총 인출 가능
최대횟수는 연 12회입니다」, cumulative withdrawals capped at total 주계약 + 추가납입 premiums,
and 추가납입 및 중도인출 수수료 **없음** [S1]. Their 추가납입 limit is 「이미 납입하기로
약정한 주계약 보험료(선납보험료 포함) × 100% − 이미 납입한 "무배당 추가납입특약"의
납입보험료의 합계 + … 인출금액의 합계」 with a 5만원 minimum [S1].

**연금전환 (annuity conversion)** is offered on nearly every product and always as a
제도성특약, i.e. attachable without extra premium. Eligibility conditions vary widely —
하나생명 impose none beyond company procedure [S2]; KB라이프 require 7 years elapsed and age
45–80 (45–70 for the 종신연금형), a 계약자적립액 of at least 1,000만원 for the 종신연금형, and
no outstanding loan, for one of three riders, with 10 years and age 45–80 for a second [S3];
처브라이프 allow conversion to a 저축성 변액보험 (excluding 변액연금) after 7 years [S1].
Conversion is irreversible everywhere it is stated [S3], and every carrier warns that a
종신보험 converted to an annuity pays less than a purpose-built annuity [S3]. The annuity
rider's own basis — 연금사망률, 계약관리비용 and 공시이율 — is the **rider's at conversion,
not the base contract's at issue** [S2].

### 16. Mortality basis — 적용위험률, disclosed at three ages

Korean 상품요약서 publish sample mortality rates. Two were recovered, and they are the only
directly citable Korean insured mortality figures in this file.

**하나생명, (무)하나로 연결된 든든한 종신보험 (해지환급금 일부지급형)** [S2]:

| 구분 | 남자 | 여자 |
|---|---|---|
| 20세 | 0.000310 | 0.000180 |
| 40세 | 0.000780 | 0.000470 |
| 60세 | 0.004550 | 0.001730 |

**KDB생명, 무배당 우리가바라던 종신보험 (2024-01-01), labelled 「무배당 예정 경험사망률」**
[S8]:

| 구분 | 남자 | 여자 |
|---|---|---|
| 20세 | 0.00038 | 0.00018 |
| 40세 | 0.00092 | 0.00057 |
| 60세 | 0.00560 | 0.00214 |

Observations:

- The two carriers differ by **10%–23%** at every age and sex (male 40: 0.00092 against
  0.000780; female 60: 0.00214 against 0.001730). These are **carrier pricing bases**, not a
  common table — so they bracket rather than fix a Korean insured mortality level.
- KDB생명's label — 「무배당 **예정 경험**사망률」 — is the giveaway: the pricing table is
  derived from the 경험생명표 with a 무배당 loading, not the 경험생명표 itself.
- Female/male ratios are 0.58 / 0.60 / 0.38 (하나생명) and 0.47 / 0.62 / 0.38 (KDB생명): a
  very large female advantage at 60, consistent with the Korean population pattern.

**The 경험생명표 itself was not obtained.** The current edition is the 제10회, applied from
April 2024, and the reported headline summary statistics are 평균수명 남 86.3세 / 여 90.7세
and 65세 기대여명 남 23.7년 / 여 27.1년, up 2.8–2.9 and 2.2 years and 2.3 and 1.9 years
respectively on the 제9회. Those figures come from **news reports of a 보험개발원 release**,
not from a retrieved 보험개발원 document — the KIDI press-release index [R12] as fetched
carries no 경험생명표 item — so they are **[unverified]**. This is exactly the position the
house brief anticipates: every `mort_table.csv` in `krlib` is a **[std]** construction with a
`provenance` column, anchored on published summary statistics and 통계청 완전생명표, and
sanity-checked against the two carrier grids above.

### 17. 보험나이 (insurance age), grace, lapse and reinstatement

**보험나이** is defined in the 약관 and the definition is uniform market practice [S5, art.
21]:

> ① 이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다. …
> ② 제1항의 보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의 끝수는
> 버리고 6개월 이상의 끝수는 1년으로** 하여 계산하며, 이후 **매년 계약해당일에 나이가
> 증가**하는 것으로 합니다. 다만, 해당연도의 계약해당일이 없는 경우에는 해당 월의 마지막 날을
> 계약해당일로 합니다.

with two worked examples on a birth date of 1988-10-02: a 2016-04-13 issue gives 만 27년 6월
11일 → **보험나이 28세**, while a 2016-03-13 issue gives 만 27년 5월 11일 → **보험나이 27세**
[S5]. So Korean insurance age is **nearest birthday**, and it increments on the **policy
anniversary**, not the birthday — which means an annual projection stepped on policy
anniversaries steps the rating age correctly by construction. A misstatement of age or sex is
corrected to the true one and the benefit and premium restated, with the surrender value
settled per the 산출방법서 [S5, art. 21(3)–(4)].

**납입최고(독촉) and lapse** [S5, art. 25]: the 납입최고기간 is **14일 이상** (7일 if the
보험기간 is under a year), running from the day after the monthly anniversary, extended to the
next business day if it would end on a non-business day; the contract is 해지 on the day after
it ends. The notice must state the arrears and that 「납입최고(독촉)기간이 끝나는 날까지
보험료를 납입하지 않을 경우 … 계약이 해지된다는 내용(이 경우 계약이 해지되는 때에는 즉시
해지환급금에서 보험계약대출의 원금과 이자가 차감된다는 내용을 포함합니다)」. Electronic notice
requires the policyholder's prior consent and a confirmed receipt, failing which the insurer
must re-notify by post or recorded call [S5, art. 25(6)].

Note that **14 days is far shorter than Japan's one to two months** [see jplib]. Korean lapse
timing is correspondingly tighter.

**부활 (reinstatement)** [S5, art. 26]: available within **3년** of the termination date,
provided the surrender value has not been taken — 「해지환급금을 받지 않은 경우(보험계약대출
등에 따라 해지환급금이 차감되었으나 받지 않은 경우 또는 **해지환급금이 없는 경우를
포함**합니다)」. That parenthesis is the 무해지 case, and it means a nil-surrender-value
contract is *always* reinstatable within three years. On reinstatement the policyholder pays
the arrears with interest at the 사업방법서 rate; for a universal contract the arrears are the
연체된 기본보험료 up to month 24 and thereafter the 연체된 월대체보험료 및 계약관리비용 중
기타비용 [S5].

**Suicide exclusion: 2 years, not 3.** 「'고의적 사고 및 2년 이내 자살'의 경우 보험금 지급이
제한될 수 있습니다」 [S1]; 「사망보험금의 경우 피보험자가 보험계약일로부터 **2년** 이내 자살한
경우에는 지급되지 않습니다」 [S3]; ABL생명 [S6] and 삼성생명 [S7] carry the same 2-year rule.
This is a genuine Korea/Japan difference — Japan's is uniformly 3 years — and it comes from
상법 rather than from carrier practice, though the 상법 article itself was **not retrieved**
and that attribution is **[unverified]**.

**계약 전 알릴 의무 and contestability**: rescission within **2년** of the 보장개시일, or
**1년** for disease on a 진단계약 [S2]. **사기에 의한 계약**: cancellable within **5년** of
the 보장개시일, or one month from discovery [S2] [S8]. **청약철회**: 15 days from delivery of
the 보험증권 or 30 days from application, whichever comes first — 45 days for a distance sale
to a policyholder aged 65+ [S1]. **위법계약 해지권** under the 금융소비자보호법: within one
year of learning of the breach and within five years of the contract [S1].

### 18. 단기납 종신 and the 유지보너스 — the 2023–24 market event

The design that made 종신보험 the centre of Korean supervisory attention, and the one whose
cash values a model most needs to be able to reproduce.

**The mechanic.** A short payment period (5년 or 7년) plus a **유지보너스** credited to the
계약자적립액 at 납입완료, on top of a 50% suppression. 삼성생명 publish the bonus rates [S7]:

| 발생시점 | 5년납 | 7년납 | 10년/15년납 |
|---|---|---|---|
| 주보험, 보험료 납입완료시점 | 10.8% | 13.8% | 15.0% |
| 체증형보장특약, 보험료 납입완료시점 | 9.5% | 12.6% | 31.5% |
| 10년 시점 (특약 5/7년납에 한하여) | 18.5% | 18.5% | — |

with the rule 「유지보너스 발생일에 주보험 보험료 총액의 최대 15.0%, 체증형보장특약 보험료
총액의 최대 31.5%를 계약자적립액에 더해드립니다. (단, 납입기간에 따라 상이)」 and the 발생일
defined as 「보험료 납입기간 경과시점 및 특약 5/7년납에 한하여 계약일부터 10년 경과시점의
연계약해당일」 [S7].

**The resulting cash values** — 남자 40세, 표준체, 주보험 2,700만원 + 체증형보장특약 1억
800만원, 7년납, 월납, 월보험료 990,900원 [S7]:

| 경과년도 | 납입보험료 누계 | 해약환급금 | 환급률 |
|---|---|---|---|
| 1년 | 11,890,800 | 3,148,440 | 26.4% |
| 3년 | 35,672,400 | 13,702,300 | 38.4% |
| 5년 | 59,454,000 | 24,701,120 | 41.5% |
| **7년** | 83,235,600 | 83,026,180 | **99.7%** |
| **10년** | 83,235,600 | 100,380,610 | **120.5%** |
| 30년 | 83,235,600 | 136,015,230 | 163.4% |
| 50년 | 83,235,600 | 172,099,880 | 206.7% |

The same page's 5년납 alternative is 주보험 2천만원 + 체증형보장특약 8천만원 at
993,600원/month [S7]. Note the **two** steps: the 유지보너스 at duration 7 takes the 환급률
from 41.5% to 99.7%, and a second bonus at duration 10 takes it to 120.5%. That second step is
exactly the "bonus payment point" [R3] requires an additional lapse spike at [R3] [R7].

**The 2024 competition and its ending.** Search results record that 10-year 환급률 above 130%
appeared across the market in early 2024 (농협생명 133%, 푸본현대생명 and 동양생명 130%), that
the FSS demanded 환급률 simulations on 2024-01-15 and conducted on-site and desk reviews, and
that by April the range had been pulled back to 113%–124.5% (신한라이프 135.0% → 122.0%,
농협생명 133.0% → 123.0%). **None of this was confirmed against a retrieved primary document**
— the numbers come from trade-press reporting only — and it is therefore **[unverified]**.
What *is* sourced is [R9]'s statement that 「2024년 1분기 환급률이 높은 단기납종신보험 판매가
증가하였으나, 이후 판매가 점진적으로 축소」 (re-spaced) [R9], and [R3]'s 30% additional-lapse
floor at the bonus point [R3].

### 19. Envelopes — issue age, payment term, sum assured

| Carrier | 납입기간 options | 가입나이 | 가입한도 | Source |
|---|---|---|---|---|
| 처브라이프 | 7 / 10 / 15 / 20년납, 전기납 | 만15세~52세 (7년납, 남) up to 만15세~63세 (15년납, 여) | 1,000만원 ~ 10억원 | [S1] |
| 하나생명 | 20년납 only | 만15세~62세 (남), 만15세~67세 (여) | — | [S2] |
| KB라이프 | 5 / 7 / 10년납 | **54세~72세** (1형, 남), 61세~76세 (1형, 여); 51세~78세 across 2형 | — | [S3] |
| DB생명 | 5/7/10/15/20/25/30년납 and 50/55/60/65/70세납 | 만15세 ~ 최고 65세 | — | [S4] |
| ABL생명 | 5 / 7 / 10 / 15 / 20년납 | 만15세 ~ 최대 70세 | — | [S6] |
| KDB생명 (우리가바라던) | 10 / 12 / 15 / 20년납 | 만15세~58세 (남, 10년납) to 만15세~66세 (여) | 100만 ~ 30억, 최저보험료 1만원 | [S8] |
| 한화생명 (하나로H) | 3/5/7/10/15/20년납, 80/90세납, 전기납 | — | — | [S18] |

Two things stand out against the Japanese comparison:

- **The maximum issue age is much lower.** 65–70 is the market ceiling for a mainstream design
  [S4] [S6] [S8], against 80 in Japan. KB라이프's product is the exception and is explicitly a
  senior product with a **minimum** issue age of 51–54 [S3].
- **납입기간 menus are shorter and denser at the front.** 3년납 [S18], 5년납 and 7년납 appear
  everywhere; 종신납 / 전기납 appears at 처브라이프 [S1] and 한화생명 [S18] but is not the
  default anywhere. This is the 단기납 market structure showing through.
- **Issue ages are consistently 3–8 years higher for women** at the same payment term [S1]
  [S2] [S8], reflecting the mortality difference in §16.
- 처브라이프's 납입면제특약 attaches only where 「주계약보험료 + 특약보험료 합산하여 50만원
  이내」 on a monthly basis, aggregated across the insured's existing waiver riders [S1] — an
  anti-selection control with no parallel in the other libraries.

### 20. Market context

- 종신보험 arrived in Korea long before it sold. 동방생명 (now 삼성생명) offered one in
  **March 1959** and a 10-year-pay variant was sold in the same era, but neither succeeded;
  the product's real start was **푸르덴셜생명's** late-1990s Life Planner channel, which built
  the sales method and the university-graduate male agent force around it, and which 삼성생명
  benchmarked on entry in **1999** [R8].
- New business by carrier, 2001–2009, sourced to 금융감독원 금융통계정보시스템 [R8] — 업계
  전체 2001 2,484,741; 2002 2,286,604; 2003 1,829,195; 2004 1,526,483; 2005 962,968; 2006
  1,060,509; 2007 1,181,861; 2008 975,020. The units are not labelled in the extracted table
  and are **not established**; the *shape* — a peak in 2001 and a halving by 2005 — is what
  this file relies on.
- Product evolution: **변액종신 2001, CI 선지급 종신 2002, 유니버셜 종신 2004** [R8]. [R8]
  reads the whole arc as a response to falling rates: 「저금리 상황에서 이차역마진 해소와
  보험가격 인상 억제를 위한 방향으로 전개 … 금리연동형, 투자연계형 상품의 개발, 변액종신보험,
  우량체 할인, **저해지 종신보험**의 개발이 이에 해당한다」 [R8]. The 저해지 form is, in the
  research institute's own framing, an interest-rate-margin device.
- The 무·저해지 form entered the market in **July 2015** (life) and **July 2016** (non-life),
  with about **4 million contracts** written by March 2019 [R4]. By July 2020 **20 of 24 life
  insurers and 11 of 14 non-life insurers** were selling it as a main line [R2].
- Its share of protection first-year premium: **11.4% (2018) → 30.4% (2021) → 47.0% (2023)**
  [R7].
- 보장성보험 수입보험료: 44.3조원 (2020), 44.3조원 (2021), 46.5조원 (2022), 48.0조원 (2023),
  26.5조원 (2024 상반기), with year-on-year growth of 4.2 / −0.1 / 5.0 / 3.2 / 13.4 per cent
  [R9]. 초회보험료 grew 36.6% year on year in 2024 H1 on 무·저해지환급형 건강보험, 단기납
  종신보험, 일시납 연금보험 and 변액보험 [R9]. For 2025 [R9] forecast a 9.2% industry-wide
  초회보험료 decline, with life down 10.0% on shrinking 단기납 종신 and 일시납 연금 demand.
- Widely reported figures for 2024 종신보험 new business (217만 건 / 58조원) and for the
  2018–2023 trajectory of 종신보험 신계약 금액 (80–89조원 in 2018–2020, 53조원 in 2021, 65조원
  in 2023) come from trade-press reporting and were **not** confirmed against [R9], [R13] or
  any 생명보험협회 table. They are **[unverified]**.
- Deposit protection: 예금자보호법 covers 해지환급금 (or maturity/claim proceeds) plus other
  amounts to **5천만원 per person per insurer**, and corporate policyholders and premium
  payers are not protected [S1] [S2]. A contract converted to a 저축성 변액보험 loses the
  protection except for the guaranteed 최저사망보험금 and the riders [S1].

---

## Variation across carriers

| Feature | 처브라이프 [S1] | 하나생명 [S2] | KB라이프 [S3] | DB생명 [S4] | KDB생명 유니버셜 [S5] | ABL생명 [S6] | 삼성생명 [S7] | KDB생명 우리가바라던 [S8] |
|---|---|---|---|---|---|---|---|---|
| Marketing name for the form | 해지환급금 일부지급형 | 해지환급금 일부지급형 | 해약환급금 과소지급형 | 저해지환급형 | 해지환급금 보증형 | 해약환급금 일부지급형 | 저해약환급금형 | 해약환급금 미지급형Ⅳ |
| Suppression design | A: % of 표준형 | B: formula on premiums | C: straight-line on premiums | A: % of 표준형 | (universal; 해지공제 only) | A: % of 표준형 | A + bonus | D: nil, then max(표준형률, 100%) |
| Fraction / formula | **50%** | 0% / 10%+90%·n/84 / 100% | 납입보험료 × 경과월/((납입기간+3)×12) | **30%** | — | **50%** | **50%** | 0, then ≥100% of premiums |
| Cliff at | 납입완료 | **7년** (not 납입완료) | **납입기간 + 3년** | 납입완료 | — | 납입완료 | 납입완료 (+10년 bonus) | 납입완료 |
| Post-cliff ceiling | none (tracks 표준형) | **flat 100%** | flat 100% of premiums | none (tracks 표준형) | — | none (tracks 표준형) | none | none |
| Published CV grid | **yes**, 8 durations, both forms | **yes**, 14 durations, both sexes, both forms | no (formula only) | **yes**, 8 durations × 2 종 | no | **yes**, 6 durations × 3 종 | **yes**, 7 durations | **yes**, 12 durations × 2 sexes × 2 variants |
| Published premium grid | **yes**, 4 ages × 2 sexes | one model point per sex | one model point (3 ages, 2 형) | **yes**, 3 ages × 2 sexes × 4 cells | no | **yes**, 3 ages × 2 sexes × 3 종 × 5 grades | one model point | one model point per sex |
| Disclosed 예정이율 / 적용이율 | **2.3%** (2022-04) | **2.25%** | not stated | not stated | **2.3%** (예정적립금) | 2.50% (추가납입특약) | **2.25% / 1.75%** split | **2.75%** (2024-01) |
| Disclosed 적용해지율 | no | **1%~10%** | no | no | no | no | no | **0%~13.4% / 1.0%~11.3%** |
| Disclosed 사망률 | no | **yes**, 3 ages × 2 sexes | no | no | no | no | no | **yes**, 3 ages × 2 sexes |
| 보험가격지수 | no | **85.4% / 86.2%** | no | no | no | no | no | **110.3% / 110.9%** |
| Benefit shape | 체증 (+5%/yr, 30yr cap) | 평준 or max(가입금액, 납입보험료×비율) | 평준 or max(가입금액, 기본보험료×경과월×비율) | 전환나이 step (1종 up, 2종 down) | 평준 (universal) | 평준 / 체감 / 체증 (3종) | 보험기간 이원화 + 체증특약 | 평준 or 가입금액 + 납입보험료 |
| 납입면제 trigger | 3대질병 rider | 장해 50% + 3대질병 rider | 장해 50% + 3대질병 rider Ⅱ | not stated | 2종/3종/3대/6대 riders | 장해 50% + 6대질병 rider | not stated | 장해 50% |
| 중도인출 | 추가계약자적립금, 연 12회, 수수료 없음 | not stated | not stated | 있음 (detail not stated) | **연 12회, 50% cap, residual floor** | not stated | not stated | not stated |
| 연금전환 | 저축성 변액 after 7년 | 연금전환특약 | 3 riders, 7/10년 gates | not stated | not stated | 4 riders + 생활설계자금 | 사망보험금 연금선지급 | not stated |
| Volume / other discount | **1.5%** at ≥3,000만원 | 선납 discount at 적용이율 | 선납 at 평균공시이율 | 고액계약할인 + 장기납입할인 (embedded) | 선납 at 적용이율, ≤11개월 | **건강등급 up to 8%**, re-rated annually | not stated | not stated |
| Suicide exclusion | 2년 | not stated in this file | **2년** | 2년 | not stated in this file | **2년** | **2년** | not stated in this file |
| Distinctive | 체증 + 추가납입 chassis | the fullest disclosure in the set | senior market, 51–78 | the only **30%** factor | the only full **약관** | 3 종 + health grading + 생활설계자금 | 단기납 + **유지보너스** | the only **fully nil** form |

**Most representative design for the reference implementation.** A **무배당, 금리확정형,
level-premium 종신보험** with (i) 보험기간 종신 and a menu of 년만기 payment terms centred on
10년납 and 20년납 [S1] [S2] [S4] [S6] [S8]; (ii) a level 평준형 death benefit at the
보험가입금액 [S6]; (iii) a **해지환급금 일부지급형 switch at 50%** of a non-marketed 표준형
computed on the same basis with the lapse assumption switched off, stepping to the full value
at 납입완료 — the design used by three of the five carriers that publish a comparison grid,
and the one the FSC's own illustration is drawn on [S1] [S6] [S7] [R1]; (iv) 해지환급금 =
계약자적립액 − 미상각신계약비, with the deduction capped by the 표준해약공제액 [S2] [S8] [R6];
(v) a **보험료 납입면제** at a 50% 장해지급률 with premiums deemed paid thereafter [S2] [S3]
[S6] [S8]; (vi) a **보험계약대출** at 예정이율 + 1.5% within 50%–85% of the surrender value,
unavailable while the surrender value is suppressed to nil [S9] [S11] [S13] [R4]; (vii)
**감액** treated as partial surrender, with **no 감액완납 and no 연장정기** [S5]; (viii) a
**2-year** suicide exclusion, a **14-day** 납입최고기간 and a **3-year** 부활 window [S1]
[S5]; (ix) **보험나이** on the nearest-birthday 6-month rule, incrementing on the policy
anniversary [S5]; and (x) a 연금전환특약 available as a 제도성특약 with the annuity basis set
at conversion [S2] [S3]. The 하나생명 grid [S2] and the 처브라이프 grid [S1] are the natural
worked-example anchors: both are internally consistent, both publish both forms, and both
exhibit the cliff.

---

## Fetch failures and gaps

- **`https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` (보험업감독규정) and
  `https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2200000106665&chrClsCd=010201`
  (보험업감독업무시행세칙)** — both returned HTTP 200 but only the site chrome: title,
  revision history, share buttons and navigation. The article body is loaded into an inner
  frame that WebFetch does not follow. A second 보험업감독규정 sequence
  (`admRulSeq=2100000235980`) behaved identically. **Consequence:** every 보험업감독규정 and
  시행세칙 fact in this file is second-hand — the 표준해약공제액 formula from [R6], its caps
  from [R5], the K-ICS 대량해지 shocks from [R7] quoting 별표 22, the 해약환급금준비금
  schedule from [R7] quoting the 부칙, the 2020 환급률 restriction from [R1] [R2]. **No
  article number is asserted anywhere in this file**, because none was read.
- **The 생명보험 표준약관 (보험업감독업무시행세칙 별표15) was not retrieved.** Three routes
  tried: `https://www.insclaim.co.kr/19/8641083` (404),
  `https://www.insclaim.co.kr/19/11075797` (404), and
  `https://exam.insure.or.kr/upload/attach/under/notice/20160202_1454394178948.pdf` (제6장
  생명보험 표준약관 및 해설 — HTTP 503). **Consequence:** the standard-form articles on
  해지환급금, 보험계약대출, **보험료의 자동대출납입**, 납입최고, 부활 and 계약내용의 변경 are
  known here only as they appear in one carrier's 약관 [S5]. In particular, **자동대출납입
  (the Korean automatic premium loan) is not evidenced by any retrieved document** and is
  marked **[unverified]** wherever it matters. Since Japan's APL is a load-bearing feature of
  that library's whole life model, its Korean status must be settled before `WholeLife_KR_S`
  claims either way.
- **`https://pub.insure.or.kr/` (생명보험협회 공시실) — reached but not usable.** The
  navigation renders and the path 상품비교공시 → 보장성보험 → 종신보험 is visible, but every
  comparison table opens through `javascript:void(0)` and no product rows, premiums,
  해지환급금 or 사업비 figures were obtained. The house brief calls this "the best single
  source of quantitative product data in Korea"; it is, and it was **not** opened. Everything
  §3 and §4 rest on came from individual carriers' own PDFs instead.
- **`https://www.e-insmarket.or.kr/wholeIns/wholeInsList.knia` — reached, empty.** The
  comparison basis rendered (1억원 / 종신 / 20년납 / 월납) and is used in §19, but the product
  table returned 「해당 상품이 없습니다」. No cross-carrier premium comparison was obtained.
- **`https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do` (금융통계월보) —
  reached, no data.** The table catalogue renders; the tables are drawn client-side.
  **Consequence: no Korean industry lapse rate, 효력상실해약률, 종신보험 신계약 건수 or
  보유계약 금액 was obtained from a primary statistical source.** The market figures in §20
  come from [R7] and [R9], which are research publications, and the 2024 종신보험 new-business
  figures circulating in the trade press are marked [unverified].
- **`https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status` — reached,
  undated.** The page returned 공시기준이율 3.19 / 적용률 3.19 / 적용이율 3.19 for five
  product categories, but the as-of month is a form selection the fetch did not make, so **the
  figure has no date** and is recorded as such at [S15].
- **`https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do` —
  reached, no data.** Returned only the disclosure-regime explanation and a departmental
  contact table. No 한화생명 공시이율, 예정이율 or 최저보증이율 was obtained [S19].
- **`http://www.moj.go.kr/bbs/moj/166/414252/download.do`** (황원재, 「생명보험계약에서
  해약환급금과 관련된 문제점」, a law-journal article that search results indicate discusses
  the 표준해약공제액 and 미상각신계약비 in legal terms) — **too many redirects (>10)**, not
  retrieved. It would have been the best independent check on the [R6] formula.
- **`https://www.kidi.or.kr/user/nd11592.do` — reached, wrong content.** The 보도자료 index
  lists only the ten most recent items (2026-01 to 2026-08) and carries **no 경험생명표
  item**; no archive or search endpoint was reached. **Consequence: the 제10회 경험생명표 was
  not sourced at all.** Its headline summary statistics (평균수명 남 86.3세 / 여 90.7세; 65세
  기대여명 남 23.7년 / 여 27.1년; applied from April 2024) are known here only from news
  reporting and are **[unverified]**. This is the expected position — the brief anticipates
  that the table is not published in full — but it means `mort_table.csv` cannot be anchored
  on a retrieved KIDI document and must be a **[std]** construction, sanity-checked against
  the two carrier pricing grids in §16.
- **`https://www.insclaim.co.kr/19/9616822`** (참조순보험요율 / 경험생명표 / 개인연금사망률
  summary) — **404**. A second route to Korean insured mortality closed.
- **No Korean expense rate as a percentage of premium was obtained from any source.** Both
  상품요약서 in the set define 계약체결비용 and 계약관리비용 and then give no number [S2]
  [S8]; the 약관 defines 부가보험료 and 해지공제액 by reference to the 산출방법서, which is
  not a public document [S5]. The 보험가격지수 (§9) and the 표준해약공제액 (§8) are the only
  quantitative handles, and both are indirect. **Every 사업비 parameter in `WholeLife_KR_S` is
  therefore [std].**
- **No Korean lapse curve by duration was obtained.** What exists is (i) two disclosed
  *pricing* envelopes — 1%~10% [S2] and 0%~13.4% / 1.0%~11.3% [S8] — with no shape, and (ii)
  the supervisor's *valuation* anchors — convergence to 0.1% at 납입완료 and 0.8% (or a 20%
  relative) after it [R3] [R7]. The two are different bases for different purposes and cannot
  be reconciled from public data. **The duration-shaped lapse assumption, and in particular
  the surrender spike at the cliff and at a 유지보너스 point, is a [std] modelling choice**,
  bounded above by the pricing envelopes and below by the supervisory anchors. This is the
  single largest assumption gap for this product, exactly as it is in Japan.
- **The 2024 H1 무·저해지 share of 63.8%** that appears in search results could not be traced
  into [R3] or [R7] as retrieved; only the 2018 / 2021 / 2023 points (11.4 / 30.4 / 47.0 per
  cent) are sourced [R7]. The 63.8% figure is **[unverified]**.
- **The 단기납 종신 환급률 competition of 2024** — the 130%+ products, the 2024-01-15 FSS
  simulation request, and the April pullback to 113%–124.5% — is trade-press reporting only.
  Only the direction ([R9]) and the supervisory remedy ([R3]) are sourced. The specific
  carrier and percentage claims are **[unverified]**.
- **The ±30% cap on the 조정률 in the 공시이율 formula** appears in search results attributed
  to the 보험업감독규정; the 약관 [S5] gives the mechanism (공시기준이율 ± 조정률) but not the
  cap. **[unverified]**.
- **The 2-year suicide exclusion's statutory basis (상법 제4편) was not retrieved.** The rule
  is confirmed at four carriers [S1] [S3] [S6] [S7]; its attribution to 상법 rather than to
  carrier practice is **[unverified]**.
- **감액완납 and 연장정기보험 are not evidenced.** Neither appears in the only full 약관
  retrieved [S5] nor in any 상품요약서 in the set. Search results describe both as generally
  available Korean maintenance options. Until a 약관 article is retrieved, treating either as
  a feature of a Korean 종신보험 is **[unverified]**, and `WholeLife_KR_S` should not model
  them.
- **The DB생명 cumulative-premium column does not reconcile at durations 10, 15 and 20** to
  the quoted monthly premium (§3), and the brochure's 「고액계약할인 및 장기납입계약할인」
  footnote is not enough to reconstruct the difference. The grid is quoted as printed; the
  suppression ratios, which is what is relied on, are exact.
- **The DB생명 premium table's column header reads 「2종(저해지환급형)」 while the 해지환급금
  table on the next page reads 「2종(실속형)」** for what the arithmetic shows to be the same
  종 (146,470원 × 12 = 1,757,640원 matches). This is treated as a typographical inconsistency
  in the brochure and the 종 is called 2종(실속형) throughout this file, on the strength of
  the positional check.
- **The 처브라이프 환급률 chart's per-payment-term line labels could not be resolved at the
  20년 후 column**, where two lines both read 151.9% (§3). The 10년납 line is pinned by the
  table; the file relies on the observed range, not the per-term attribution.
- **[R9] extracts without inter-word spaces** (a font-encoding artifact of that deck).
  Quotations from it in this file are re-spaced and marked as such at the point of use.
- **[S7] is a distributor-hosted copy on a Webflow CDN**, complete with an individual
  consultant's name and contact details in the footer, rather than a 삼성생명 URL. The
  document carries a 준법감시필 number and a 발행일자 and is on its face a compliance-approved
  보험안내자료, but a 삼성생명-hosted original was not found. Weight it accordingly.
- **Only one full 약관 was retrieved** [S5], and it is a **유니버셜** contract, not a
  conventional level-premium one. So the contractual articles in §§7, 12, 14, 15 and 17 are
  evidenced from a chassis that differs from the representative design in exactly the places
  where universal products differ. Where a fact is chassis-independent (보험나이, 부활, 감액,
  보험계약대출 wording) that is fine; where it is not (제24조's payment holidays, 제25조's
  월대체보험료-driven lapse trigger, 제33조's withdrawal rules) the fact belongs to the
  universal variant and is labelled as such above. **A conventional 종신보험 약관 remains
  unretrieved and is the highest-value single document for the next research pass.**
