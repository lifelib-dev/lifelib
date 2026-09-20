# Sources

Source ids [S#] and [R#] are carried verbatim from `_research/whole-life.md` — the citation
ground truth for this product — and are **frozen: never renumber them.** Access date for every
entry: **2026-09-03**. No sources were newly added at drafting.

**Three tag families, and they mean different things here.**

- **[S#] — primary product sources.** A 약관 (*yakgwan*, policy conditions), a 상품요약서
  (*sangpum yoyakseo*, the statutory product summary), a 상품안내장 / 보험안내자료 (brochure)
  or a published rate disclosure, issued by a named carrier or by an industry disclosure
  portal. These are the documents that establish what the *contract* does. They render as
  bracketed text, never as links.
- **[R#] — regulatory and actuarial references specific to this product**, numbered in the same
  per-product sequence: FSC and FSS 보도자료, 보험연구원 research, and the two law-portal and
  two statistical endpoints this product's research pass tried. They render as links.
- **[REG-R#] — the cross-product reference library**,
  `references/regulatory-and-actuarial-references.md`, whose **R1–R62 numbering is a separate
  frozen sequence** and has nothing to do with the R-numbers on this page. `[R3]` and
  `[REG-R3]` are different documents. The entries this product cites are reprinted in short
  form at the end of this file so that a reader of this page alone can resolve them.

**Numbering is per product.** `S1` means a different source in each product's `sources.md`, and
this file's `R1` is not `term_life`'s `R1`.

**Gaps in the numbering, and why.** Unused sources are omitted, so the sequence has holes.
**S14** (손해보험협회 「보험계약대출금리」 비교공시) was retrieved and is a good bound on the
Korean policy-loan market, but it covers **non-life** insurers, so nothing in a 생명보험
종신보험 specification may rest on it and nothing does. **S19** (한화생명 상품공시실
「적용이율」) returned no rate data at all and establishes nothing. **R5** is the FSC's
2019-08-01 사업비·모집수수료 reform release; the cross-product library holds the same document
at [REG-R29] and the product documents cite it there, so the per-product number is unused.
**R10** and **R11** are the 국가법령정보센터 pages for 보험업감독규정 and
보험업감독업무시행세칙, both of which returned only site chrome in this product's own research
pass — the article body loads into an inner frame. The cross-product research pass later
retrieved both in full, so every 감독규정 and 시행세칙 fact in this product's documents is
cited to [REG-R9], [REG-R18], [REG-R19], [REG-R20], [REG-R21], [REG-R22], [REG-R23] and
[REG-R25] rather than to the unretrieved per-product entries. That is a strict improvement in
provenance, and it is the reason those two numbers are absent below rather than present and
empty.

**Read the `Retrieved:` line before relying on the entry above it.** `Retrieved: yes` means the
document was opened and the passage the entry rests on was read; a Korean sentence quoted in
such an entry is quoted from the document. `in part` and `no` leave the entry a **pointer, not
a certificate**, and every claim resting on one is tagged [unverified] where it matters.

**Company and branded product names appear in this file and in `_research/whole-life.md` and
nowhere else in the library.** In `product-spec.md`, `technical-notes.md`, `model.md` and the
model docstrings a carrier is referred to by its [S#] tag alone.

**Coverage.** Seventeen primary sources are cited, of which **thirteen are `Retrieved: yes`**
and four `in part`; ten product-specific regulatory references, of which **nine are
`Retrieved: yes`** and one `in part`. Eleven carriers appear in the cited set, plus two
industry disclosure portals. Five carriers publish
complete numeric surrender-value grids for both the suppressed form and its non-marketed
comparison twin [S1] [S2] [S4] [S6] [S8], which is what makes this product's signature mechanic
measurable rather than described; two publish the pricing interest rate, sample mortality rates
and the pricing lapse assumption in the 상품요약서 [S2] [S8], a level of disclosure with no
counterpart in `jplib`, `uklib` or `delib`. Against that, **exactly one full 약관 was
retrieved** [S5], and it is a 유니버셜 contract rather than a conventional level-premium one.

---

## Primary product sources

(krlib-whole_life-s1)=

### S1 — 「Chubb 더하고 채우는 종신보험 무배당 (해지환급금 일부지급형)」, 처브라이프생명보험 주식회사 (상품안내장 — product brochure with premium and surrender-value tables)

- Document: 4-page 상품안내장, `product_brochure_S1_AW21.pdf`; footer 「2022 MKT-105 /
  2022.04.01 / 준법감시인 심의필 제2022-105호」; the premium page is headed 「2022년 4월 계정」
- URL: https://www.chubblife.co.kr/assets/product_brochure_S1_AW21.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (PDF downloaded, 4 pp.; a plain text dump scrambles
  the 환급률 chart on p.1, which was recovered by positional word extraction with PyMuPDF)
- **What it establishes.** A **side-by-side 해지환급금 예시표** for the 해지환급금 일부지급형
  against the non-marketed 표준형 twin at eight durations, with both premium scales; the
  **50%** suppression factor; a disclosed **예정이율 연복리 2.3%**; a premium grid by age and
  sex; a 체증형 death benefit; 추가납입 and 추가계약자적립금 인출 mechanics; a 1.5% volume
  discount at 가입금액 ≥ 3,000만원; and a 보험료납입면제특약.
- **What rests on it.** The sentence the whole suppression mechanic turns on — 「"표준형"의
  경우는 … 동일한 보장내용으로 **해지율을 적용하지 않고** … 계산된 상품이며 … 비교안내를
  위한 종목으로 **실제로 판매하지 않습니다**」 — quoted in `product-spec.md`,
  `technical-notes.md` and `model.md`, and the reason the model runs **one** account and
  multiplies the twin rather than the sold form. Also the `k = 0.50` composite, the 0.900
  premium ratio standardized onto model point 1, the lower end of the 2.25%–2.75% 예정이율
  band, and the equality of the suppressed and 표준형 values from 납입완료 that
  `check_cv_cliff()` asserts.

(krlib-whole_life-s2)=

### S2 — 「무배당 하나로 연결된 든든한 종신보험(해지환급금 일부지급형)」 상품요약서, 하나생명보험 주식회사 (상품요약서 — the statutory summary of the 기초서류)

- Document: 10-page 상품요약서
- URL: https://www.hanalife.co.kr/home/download2.do?fileName=PROD%2F%28%EB%AC%B4%29%ED%95%98%EB%82%98%EB%A1%9C%EC%97%B0%EA%B2%B0%EB%90%9C%EB%93%A0%EB%93%A0%ED%95%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98%28%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%EA%B8%88+%EC%9D%BC%EB%B6%80%EC%A7%80%EA%B8%89%ED%98%95%29_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (served with `Content-Type:
  application/x-msdownload`; the bytes are a 10-page PDF and extract cleanly with PyMuPDF)
- **What it establishes.** The single most complete disclosure in the set: a **formula-based**
  해지환급률 (0% / `10% + 90% × 납입횟수/84` / 100%) whose cliff is at **seven years and not at
  납입완료**; a disclosed **적용이율 연복리 2.25%**; disclosed **적용위험률 (사망률) at ages
  20 / 40 / 60 by sex**; a disclosed **적용해지율 of 연 1%~10%** together with the explicit
  statement that the 일반형 comparison product carries none; full 해지환급금 예시표 for both
  sexes at fourteen durations for both forms; the 보험가격지수 (85.4% 남 / 86.2% 여); the
  납입면제 trigger and its deemed-paid rule; and a 연금전환특약 with a 최저보증이율 ladder.
- **What rests on it.** Half of every **ANCHOR** row of `mort_table.csv` — the male age-40 rate
  of 0.000780 and the female and age-20/60 counterparts, meaned with [S8]; the **10%**
  first-year rate of the `loglinear` lapse basis, as the top of a disclosed pricing envelope;
  the post-IFRS 17 surrender identity 「계약자적립액에서 미상각신계약비를 공제한 금액」 read
  against the pre-2023 wording; the 2.25% end of the 예정이율 band; the 납입면제 deemed-paid
  rule the waiver state implements; and the record, in the standardizations table, that **where
  the cliff falls is not universal**.

(krlib-whole_life-s3)=

### S3 — 「KB,시니어[약:속]종신보험 무배당 (해약환급금 과소지급형)」 상품안내장, KB라이프생명보험 주식회사 (상품안내장 — product brochure)

- Document: 16-page 상품안내장; 「준법감시인확인필-SM-2212368-1(2022.12.29~2023.12.28)」
- URL: https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1228983/44
- Accessed: 2026-09-03. **Retrieved: yes** (PDF downloaded, 16 pp., text extracted and read)
- **What it establishes.** A **third, arithmetically different** suppression design — the
  surrender value is a straight-line fraction of *premiums paid*, `납입보험료 누계 ×
  경과개월수 / ((납입기간+3년)×12)`, nil in year 1 and capped at 100% at **납입기간 + 3년**; a
  senior-market issue-age envelope (54–72 male); a 2형(Light형) with a reduced non-accident
  death benefit; the 납입면제 waiver and its "premiums deemed paid" rule; three 연금전환특약;
  선납 discounted at the 평균공시이율; and a 2-year suicide exclusion.
- **What rests on it.** The second of the two cliff-date counter-examples recorded in
  `model.md`'s standardizations table, which is why a model reproducing another carrier must
  expose the cliff date as a parameter; the deemed-paid waiver rule, corroborated with [S2] and
  [S8]; and the 표준형-comparison sentence, corroborating [S1].

(krlib-whole_life-s4)=

### S4 — 「무배당 알차고 행복한 종신보험(저해지환급형)(1607)」 상품안내장, DB생명보험 주식회사 (상품안내장 — product brochure with premium and surrender-value grids)

- Document: 5-page 상품안내장
- URL: https://www.idblife.com/notice/product/file/A020100001.pdf?fileName=DB%EC%83%9D%EB%AA%85-%EB%AC%B4%EB%B0%B0%EB%8B%B9+%EC%95%8C%EC%B0%A8%EA%B3%A0+%ED%96%89%EB%B3%B5%ED%95%9C+%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EC%A0%80%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%ED%98%95(1607(A020100001-%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (served as `application/octet-stream`, 3.6 MB; a
  5-page PDF; both surrender-value grids re-checked by positional word extraction)
- **What it establishes.** The only **30%** suppression factor in the set, stated in the
  유의사항 as 「1형(표준형) 해지환급금의 30%에 해당하는 금액」; **two complete 해지환급금 예시
  grids** (1종 기본형 and 2종 실속형) at eight durations each, for both forms; a premium grid
  by age, sex and form; the 납입기간 menu (5/7/10/15/20/25/30년납 and 50/55/60/65/70세납); a
  전환나이 design in which the death benefit steps at 55/60/65/70; and the phrase
  「사업비(미상각신계약비(해지공제액) 포함)」 naming the deduction.
- **What rests on it.** **The anchor cell's premium.** ₩3,084,600 is 12 × the published
  ₩257,050 monthly rate for exactly 남 40세 / 1억원 / 20년납, which prices `point_id = 2`, and
  the anchor is 0.900 of it. `prem_loading = 1.4642` is calibrated once against that number and
  applied unchanged everywhere. On the monthly grid that rate is collected directly: the
  twin's `premium_mth_pp()` is exactly ₩257,050. Also the `k = 0.30` model point, and the
  **0.899–0.923** calibration band of `cv_std_pp(12y)` against this carrier's printed 표준형
  grid at durations 3 to 20 — the one external check on the model's whole value construction,
  which the monthly account improves at every sourced duration. The grid's widening
  past duration 20 has a stated cause in this document (the 전환나이 step-up) and is recorded
  rather than tuned away.

(krlib-whole_life-s5)=

### S5 — 「희망드림 무배당 KDB유니버셜종신보험(보증비용부과형) 해지환급금 보증형」 보험약관, KDB생명보험 주식회사 (약관 — policy conditions; the only full 약관 retrieved)

- Document: 60-page 보험약관 with 부표 1–3 and 용어의 정의; 판매일자 2021.05.01; file
  `I40204_20210501_..._약관_V03.pdf`
- URL: https://www.kdblife.com/nKumhoFiles/data_pdf/product/2021/I40204_20210501_%ED%9D%AC%EB%A7%9D%EB%93%9C%EB%A6%BC(%EB%AC%B4)KDB%EC%9C%A0%EB%8B%88%EB%B2%84%EC%85%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EB%B3%B4%EC%A6%9D%EB%B9%84%EC%9A%A9%EB%B6%80%EA%B3%BC%ED%98%95)%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%EA%B8%88%EB%B3%B4%EC%A6%9D%ED%98%95_%EC%95%BD%EA%B4%80_V03.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (1.6 MB PDF, 60 pp., text extracted cleanly and the
  articles read in full)
- **What it establishes.** Articles 1–44 verbatim: **제20조(계약내용의 변경 등)** with the 감액
  formulas and worked examples; **제21조(보험나이 등)** with the six-month rule and two worked
  examples; 제24조 and **제25조(납입최고와 계약의 해지)** with the 14-day 납입최고기간;
  **제26조(부활)** with a **three-year** window; **제31조(해지환급금)**; **제32조(공시이율의
  적용 및 공시)** with the 신공시기준이율 mechanism and a **최저보증이율 연복리 0.75%**;
  **제33조(중도인출)**; **제34조(보험계약대출)**; and the 용어의 정의 giving 예정적립금 (at
  적용이율 연복리 2.3%), 계약자적립금, 월대체보험료, 부가보험료 and 해지공제액.
- **What rests on it.** `min_guar_rate = 0.75%` on the 금리연동형 model point, stated verbatim
  and not standardized; the policy-loan article behind the 80% limit; **감액 as a partial
  surrender** paying the 해약환급금 attaching to the reduced portion, which is what makes
  `claims_reduction` a benefit column rather than a negative premium; the three-year 부활
  window and the 「해지환급금이 없는 경우를 포함」 parenthesis that makes a 무해지 contract
  always reinstatable; and — as **negative** evidence — the absence of any 자동대출납입,
  감액완납 or 연장정기보험 article, which is why all three are [unverified] absences in this
  library rather than modelled mechanics. **Caveat that must travel with every citation:** this
  is a **유니버셜** contract, so 제24조's payment holidays and 제25조's 월대체보험료-driven
  lapse trigger belong to that chassis and not to the conventional level-premium composite. The
  chassis-independent articles (보험나이, 부활, 감액, 보험계약대출) are used; the rest are
  labelled where they appear.

(krlib-whole_life-s6)=

### S6 — 「(무)ABL건강하면THE소중한종신보험(해약환급금 일부지급형)2504」 상품안내장, ABL생명보험 주식회사 (상품안내장 — product brochure)

- Document: 20-page 상품안내장; 「준법감시인 심의필 제2025-PA349호 (2025.09.29~2026.09.28)」
- URL: https://www.abllife.co.kr/cms/prdt/wlifeFprd/__icsFiles/afieldfile/2025/09/29/(%EB%AC%B4)ABL%EA%B1%B4%EA%B0%95%ED%95%98%EB%A9%B4THE%EC%86%8C%EC%A4%91%ED%95%9C%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88_%EC%9D%BC%EB%B6%80%EC%A7%80%EA%B8%89%ED%98%95)2504_20251001.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (1.3 MB PDF, 20 pp., text extracted and read)
- **What it establishes.** The **most recent** product in the set (October 2025): a 50%
  일부지급형 with three 종 — 1종(평준형), 2종(체감형) and 3종(체증형) — each with its own
  surrender-value grid and premium scale; a **건강등급** premium discount of up to 8% on the
  주계약, recomputed annually; a 생활설계자금 drawdown that reduces the sum assured
  automatically; issue ages 만15세~70세 and 납입기간 5/7/10/15/20년납; the 납입면제 trigger at
  a **50% 장해지급률**; and the 2025 평균공시이율 quoted in-document as 연복리 2.75%.
- **What rests on it.** That the **평준형** level death benefit is the right composite shape
  when three shapes are on sale; the `k = 0.50` factor, corroborating [S1] and [S7]; the 50%
  장해지급률 waiver trigger, corroborating [S2] and [S8]; the issue-age and payment-term
  envelopes of the shipped model points; and the equality of the suppressed and 표준형 values
  from 납입완료.

(krlib-whole_life-s7)=

### S7 — 「삼성 더행복종신보험(2309)(무배당) [5년이후사망보험금100%형]」 상품안내장, 삼성생명보험 주식회사 (상품안내장 — product brochure, distributor-hosted copy)

- Document: 4-page 상품안내장; 「준법감시필 23-1888(FC지원팀, 2023.08.29 ~ 2024.08.28)」;
  발행일자 2023년 09월 04일
- URL: https://assets-global.website-files.com/638be8b99d4abb0bb101827b/64f9397cb1f729afb6cf4e2a_%EB%8D%94%ED%96%89%EB%B3%B5%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(2309)(%EB%AC%B4%EB%B0%B0%EB%8B%B9)(5%EB%85%84%EC%9D%B4%ED%9B%84%EC%82%AC%EB%A7%9D%EB%B3%B4%ED%97%98100%25%ED%98%95,%EC%A0%80%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88%ED%98%95).pdf
- Accessed: 2026-09-03. **Retrieved: yes** (PDF downloaded, 4 pp.; the 유지보너스 rate table
  recovered by positional extraction)
- **What it establishes.** The **단기납 저해약환급금형** design that dominated Korean life
  sales in 2023–24: 5년납 / 7년납, a **유지보너스 (persistency bonus)** credited to the
  계약자적립액 at 납입완료 at published rates, and a surrender-value grid running to 환급률
  **206.7% at duration 50**; 보험기간 이원화 (a reduced disease-death benefit for the first
  five years); a disclosed **해약환급금 적용이율 of 연복리 2.25% for the first ten years and
  1.75% thereafter**; and a 사망보험금 연금선지급 전환제도.
- **What rests on it.** `bonus_rate = 0.138` and the 7년납 payment term on `point_id = 8`,
  which together with the mandatory 30-point lapse spike of [REG-R27] is the only place in the
  library where a bonus and its supervisory counterweight are wired to each other. Also the
  2.25% end of the 예정이율 band. **Weight it accordingly:** this is a distributor-hosted copy
  on a Webflow CDN, complete with an individual consultant's contact details in the footer,
  rather than a 삼성생명 URL. It carries a 준법감시필 number and a 발행일자 and is on its face
  a compliance-approved 보험안내자료, but no carrier-hosted original was found.

(krlib-whole_life-s8)=

### S8 — 「무배당 우리가바라던 종신보험」 상품요약서, KDB생명보험 주식회사 (상품요약서)

- Document: 7-page 상품요약서; 판매일자 2024.01.01; file
  `I40414_20240101_(무)우리가바라던종신보험_상품요약서_V02.pdf`
- URL: https://www.kdblife.com/nKumhoFiles/data_pdf/product/2024/I40414_20240101_(%EB%AC%B4)%EC%9A%B0%EB%A6%AC%EA%B0%80%EB%B0%94%EB%9D%BC%EB%8D%98%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C_V02.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (139 KB PDF, 7 pp., text extracted and read in full)
- **What it establishes.** The **fully nil** form (해약환급금 미지급형Ⅳ) — zero surrender value
  for the whole of a 20-year payment period, then `이미 납입한 보험료 × max(기준상품
  해약환급률, 100%)`; a disclosed **적용이율 연복리 2.75% (금리확정형)**; **disclosed 예정
  경험사망률** at ages 20 / 40 / 60 by sex; the sharpest single number in the set, a disclosed
  **적용해약률 of 연 0%~13.4% during the payment period and 연 1.0%~11.3% after it**; the
  statement that 해약환급금 = 계약자적립액 − 미상각신계약비; 보험가격지수 110.3% / 110.9%; and
  full 해약환급금 예시 grids to duration 60 for two variants and both sexes.
- **What rests on it.** The other half of every **ANCHOR** row of `mort_table.csv` — the male
  age-40 rate of 0.00092 and its age-20/60 and female counterparts, meaned with [S2], the two
  differing by **up to 24%** — at five of the six published cells, and not at all at 여 20세,
  where both print 0.00018 — so that they bracket rather than fix a Korean insured
  mortality level. Also `k = 0.00` on `point_id = 3`, the 무해지 point at which the policy loan
  draws exactly nothing; the wider of the two disclosed lapse envelopes, inside which the
  `loglinear` first-year rate sits; the 2.75% top of the 예정이율 band; and the post-IFRS 17
  surrender identity read against the pre-2023 wording.

(krlib-whole_life-s9)=

### S9 — 「적용이율 공시 — 보험계약대출이율」, 하나생명보험 주식회사 (published rate disclosure, company web page)

- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab3_6.do
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200, server-rendered table read)
- **What it establishes.** The 보험계약대출이율 formula banded by contract date —
  「적용이율 + 1.5%」 (금리확정형) / 「공시이율 + 1.5%」 (금리연동형) from 2013-04-01, and
  「예정이율 + 2%」 for 2010-10-01~2012-03-31 — and the floor rule that a 금리연동형 loan is
  priced off the 최저보증이율 when the 공시이율 falls below it.
- **What rests on it.** `loan_spread = 0.015` and the definition `loan_int_rate() =
  acc_int_rate() + 1.5%`, which is 예정이율 + 1.5% on a 금리확정형 contract and 공시이율 + 1.5%
  on a 금리연동형 one. The date banding is the first of three independent statements that the
  Korean policy loan rate is a **vintage** rate.

(krlib-whole_life-s10)=

### S10 — 「적용이율 공시 — 표준이율 및 평균공시이율」, 하나생명보험 주식회사 (published rate disclosure, company web page)

- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** The **평균공시이율 series 2016–2026**, and the 표준이율 series for
  its last three years before it was superseded. This is the single citable time series of the
  Korean average declared rate found in this session, and it records the fall to **2.50%** for
  2026, the first since 2020.
- **What rests on it.** The cross-check that the [std] 예정이율 of 2.50% equals the 2026
  평균공시이율, which is the regulatory reference rate a product design is tested against
  [REG-R16] [REG-R48]. The same series is reprinted in the cross-product library.

(krlib-whole_life-s11)=

### S11 — 「보험계약대출」 상품안내, 교보생명보험 주식회사 (product page, company web site)

- URL: https://www.kyobo.com/dgt/web/insurance/policy-loan/PCLN_ALL_INTRO
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** 확정형 「예정이율 + 1.40 ~ 1.50%(변동가능)」 and 연동형 「공시이율 …
  + 1.50%」; a published live rate range of **연 3.5% ~ 10.5%** across the in-force book; the
  loan limit 「해약환급금의 **50% ~ 85%**」; a −0.10%p concession from 2025-11-27 on contracts
  whose 예정이율 is 7% or more; **no early-repayment fee**; and a loan term running to the
  contract's 만기일.
- **What rests on it.** The wider of the two published loan-limit ranges, inside which the
  composite's 80% sits; the 3.5%–10.5% spread that demonstrates the vintage-rate point in
  numbers; and **the no-fee repayment right**, which is why modelling no repayment at all is a
  named [std] simplification rather than an oversight.

(krlib-whole_life-s12)=

### S12 — 「보험계약대출이율」 공시, AIA생명보험 주식회사 (published rate disclosure, company web page)

- URL: https://www.aia.co.kr/ko/disclosure/our-products/interest-rate/policy-loan.html
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** A **complete historical 가산금리 schedule by contract-date band**,
  from 2003 to the present, with the 최고 적용 대출이율 cap at each band.
- **What rests on it.** The clearest evidence in the set that the Korean policy loan rate is a
  *vintage* rate and not a market rate, and the **9.90%** ceiling quoted in `model.md`. Nothing
  numeric in the projection depends on it; it bounds the rate the module uses.

(krlib-whole_life-s13)=

### S13 — 「보험계약대출」, 신한라이프생명보험 주식회사 (product page, company web site)

- URL: https://www.shinhanlife.co.kr/hp/cdhc0020.do
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** 「예정이율 + 가산금리(1.5%)」 / 「공시이율 + 가산금리(1.5%)」; the
  loan limit 「해약환급금의 **50 ~ 80%**이내」; no early-repayment fee; and a 0.1% concession
  for insureds aged 65+ on contracts with a 예정이율 of 5.5% or more.
- **What rests on it.** `loan_limit = 0.80`, taken as the **top of the narrower** of the two
  published ranges and inside the wider one [S11]; and the third independent statement of the
  +1.5% spread, which is what makes `loan_spread` a sourced parameter rather than a [std] one.

(krlib-whole_life-s15)=

### S15 — 「공시기준이율 적용현황」, 교보생명보험 주식회사 (published rate disclosure, company web page)

- URL: https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status
- Accessed: 2026-09-03. **Retrieved: in part** (WebFetch, HTTP 200; the page returned its
  default query result — 공시기준이율 3.19 / 적용률 3.19 / 적용이율 3.19 across 보장(무배당),
  연금(무배당), 연금(배당), 저축(무배당) and 연금저축(배당) — but **no as-of month rendered**,
  because the month is a form selection the fetch did not make)
- **What it establishes.** That 적용공시이율 = 공시기준이율 adjusted by a 조정률, confirmed in
  the page's own methodology text. The three numeric figures **have no date** and are recorded
  as undated.
- **What rests on it.** Only the description of the 공시이율 mechanism in `product-spec.md`.
  **Nothing in the model.** The 금리연동형 model point's declared rate is a model point column
  set to 2.75% **[std]**, not this figure.

(krlib-whole_life-s16)=

### S16 — 생명보험협회 공시실, 생명보험협회 (industry disclosure portal)

- URL: https://pub.insure.or.kr/
- Accessed: 2026-09-03. **Retrieved: in part** (WebFetch, HTTP 200; the navigation renders —
  상품제도 및 개요 / 상품비교공시 / 저축성 요약공시 / 경영공시 / 대출공시 / 기타공시, and the
  path 상품비교공시 → 보장성보험 → 종신보험 — but every comparison table opens through
  `javascript:void(0)` and **no product rows were obtained**)
- **What it establishes.** Structure only. The house brief calls this portal the best single
  source of quantitative Korean product data; it is, and it was not opened.
- **What rests on it.** Nothing quantitative. It is cited as **negative evidence** for the
  statement that the cross-carrier premium, 해지환급금 and 사업비 comparisons this product
  would otherwise use were not obtained, so that everything numeric comes from individual
  carriers' own PDFs instead.

(krlib-whole_life-s17)=

### S17 — 「종신보험」 비교공시, 손해보험협회 e-보험시장 (industry comparison disclosure)

- URL: https://www.e-insmarket.or.kr/wholeIns/wholeInsList.knia
- Accessed: 2026-09-03. **Retrieved: in part** (WebFetch, HTTP 200; the comparison basis
  rendered but the product table returned 「해당 상품이 없습니다」)
- **What it establishes.** The **standard comparison basis** Korean industry disclosure uses
  for 종신보험: **보험가입금액 1억원, 종신, 20년납, 월납**.
- **What rests on it.** The choice of the anchor cell. `point_id = 1` is that basis exactly, so
  the worked example is stated on the cell a Korean reader would compare products on. The
  document came through the **손해보험협회** portal and is attributed there, not to
  생명보험협회; the cross-product library records the same portal at [REG-R62], which this
  product does not otherwise cite.

(krlib-whole_life-s18)=

### S18 — 「종신/정기보험」 상품안내, 한화생명보험 주식회사 (product page, company web site)

- URL: https://www.hanwhalife.com/main/insurance/product/IN_SM00000_P30000.do
- Accessed: 2026-09-03. **Retrieved: in part** (WebFetch, HTTP 200; the product guide rendered
  but no premium, 환급률 or issue-age figures)
- **What it establishes.** The 종 menu for one 종신보험 — 1종(체증형) with 보험기간
  80/85/90/95세만기 and 2종(기본형) with 60/70/80/90/95세만기 — and a **납입기간 menu including
  3년납**.
- **What rests on it.** The payment-term envelope in `product-spec.md`, and nothing else. No
  quantitative parameter of the model depends on it.

---

## Regulatory and actuarial references

(krlib-whole_life-r1)=

### R1 — 「무(저)해지환급금 보험의 상품 구조를 개선하고, 보험약관 …」 (2020-11-18), 금융위원회 (보도자료 announcing the 보험업감독규정 amendment)

- URL: https://fsc.go.kr/no010101/74613
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** The amendment effective **2020-11-19** restricting products whose
  surrender value during the payment period is nil or under 50% of the 표준형, so that they
  must be designed 「전(全) 보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로」; and
  a **worked numeric comparison** on a 종신보험 (20년납, 1,000만원, 남 40세) of 표준형 against
  the 무해지 form before and after the amendment, the post-amendment design showing 62.2%.
- **What rests on it.** The press release's framing of the 환급률 restriction, which
  `product-spec.md` records **beside** the 고시's own 제7-66조제4항제2호나목 wording
  [REG-R19] because the two readings differ and neither is resolved here. `check_cv_cliff()`
  asserts the **value** test that both readings share and asserts neither ratio form.

(krlib-whole_life-r2)=

### R2 — 「높은 환급률만을 강조하며 판매되는 무(저)해지환급금 보험 …」 (2020-07-27), 금융위원회 (보도자료 — 보험업감독규정 개정안 입법예고)

- URL: https://www.fsc.go.kr/no010101/74468
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** The market count at that date — **20 life insurers and 11 non-life
  insurers** selling the form as a main line, against four and three not selling it — the
  mis-selling concern 「저축성보험처럼 환급률만을 강조하며 판매」, and the shape of the
  restriction later enacted as [R1].
- **What rests on it.** The market-context paragraphs of `product-spec.md` establishing that
  the suppressed form is the mainstream and not a niche, which is the justification for making
  it a **model point column** on the chassis rather than a separate model.

(krlib-whole_life-r3)=

### R3 — 「합리적인 계리가정과 단계적 할인율 조정을 …」 (2024-11-07), 금융위원회·금융감독원, 제4차 보험개혁회의 (보도자료)

- URL: https://www.fsc.go.kr/no010101/83351
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** The 2024 supervisory intervention on the 무·저해지 lapse assumption:
  the log-linear model designated the **원칙모형** with the lapse rate converging to **0.1%**
  at 납입완료; the post-완납 rate set at **0.8%** or a **20%** relative to the 표준형 product's
  rate; the strict conditions on using a non-principle model; a minimum **30%** additional
  lapse at a bonus payment point on 단기납 종신; and the discount-curve
  last-observable-maturity extension. Effective from the 2024 year-end close.
- **What rests on it.** Both endpoints of the `loglinear` row of `lapse_table.csv` and
  `lapse_bonus_spike = 0.30`. The same decision is entry [REG-R27] in the cross-product
  library, where the retrieval is of the 보도자료 PDF and its 별첨; the product documents cite
  [REG-R27] for the instrument and [R3] alongside it where the per-product research is what
  established the point. **Instrument-level gap:** the 「IFRS17 주요 계리가정 가이드라인」
  attachment was never converted from HWP, so the **values** are verified from the 보도자료 and
  the guideline's **functional form** is [unverified].

(krlib-whole_life-r4)=

### R4 — 「저해지환급금 보험상품에 대해 소비자 경보 발령」 (2019-10-23), 금융감독원 보험과 (소비자경보, published on the FSC site)

- URL: https://www.fsc.go.kr/no010101/73932
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200)
- **What it establishes.** The sales-start dates — life insurers from **July 2015**, non-life
  from **July 2016** — about **4 million** contracts written to March 2019; the warning that
  the form is a 보장성보험 and unsuitable for savings; and the operationally important point
  that **a 무해지환급금 contract cannot support a policy loan during the payment period**.
- **What rests on it.** `point_id = 3`, where `loan_util = 1.0` and `loan_draw(10)` is
  **exactly ₩0.00** because there is no payable value to lend against. That is this alert
  reproduced as arithmetic, and it is the single clearest demonstration in the model that the
  loan limit must be computed off `cv_pp` and never off `cv_std_pp`.

(krlib-whole_life-r6)=

### R6 — 「소비자보호를 위한 보험상품 사업비 및 모집수수료 개선」 (2019-04), 보험연구원 정원석 (research presentation, 사업비 및 모집수수료 부가체계 공청회)

- Document: 27-slide presentation, `KIRI_20190416_144027.pdf`
- URL: https://www.kiri.or.kr/pdf/전문자료/KIRI_20190416_144027.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (938 KB PDF, 27 pp., text extracted and read)
- **What it establishes.** The **표준해약공제액 formula, by product class**, with a worked
  arithmetic example; the framing of the surrender value as 적립금 less unrecovered 사업비
  bounded by the 표준해약공제액; and a 장기보장성보험 surrender-value example table.
- **What rests on it.** The definition of 해약공제액 as 미상각신계약비 capped by the
  표준해약공제액, corroborating the 약관 wording at [S5 제2조] and [S8], and the independent
  reading of the 별표 14 formula that `surr_chg_cap_pp()` implements. The instrument itself is
  [REG-R20]; this entry is the actuarial reading of it. The same presentation is [REG-R37] in
  the cross-product library.

(krlib-whole_life-r7)=

### R7 — 「보험개혁회의 내용과 과제: 건전성 제도」 (2025-04), 보험연구원 노건엽·이승주, CEO Report 03호 (research report)

- Document: 24-page report
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=671389
- Accessed: 2026-09-03. **Retrieved: yes** (594 KB PDF, 24 pp., text extracted and read)
- **What it establishes.** The **무·저해지 보장성 초회보험료 share time series** (2018 / 2021 /
  2023, at 11.4 / 30.4 / 47.0 per cent); a restatement of the [R3] lapse guidance with the
  exact model names; the **K-ICS 대량해지위험 shock table** for 표준형 and 저해지환급형,
  sourced in the report to 보험업감독업무시행세칙 [별표 22]; and the **해약환급금준비금**
  figures with the K-ICS-linked accumulation-ratio schedule for 2024–2029 set out in the
  감독규정 부칙.
- **What rests on it.** The 대량해지위험 discussion in `technical-notes.md`, in particular that
  the shock splits by whether surrender **reduces or increases** net assets — which is why the
  `flat` lapse basis producing a *better* undiscounted total is a trap and not a finding.
  **별표 22 itself was not retrieved** [REG-R26], so everything about the shock, including the
  고환급형 test, is second-hand through this report and carries [unverified]. That matters most
  to exactly this product. The same report is [REG-R36] in the cross-product library.

(krlib-whole_life-r8)=

### R8 — 「Ⅲ. 종신보험의 성장」, 보험연구원, 연구보고서 2018-5 (research report chapter — product history)

- Document: 28-page chapter, `nre2018-05_03.pdf`
- URL: https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2018-05_03.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (858 KB PDF, 28 pp., text extracted and read)
- **What it establishes.** The market history of 종신보험 in Korea — the 1959 attempt, the
  1990s false starts, the Life Planner channel breakthrough and the 1999 entry of the largest
  life insurer; a table of 종신보험 new business by carrier 2001–2009 sourced to 금융감독원
  금융통계정보시스템; the evolution sequence 변액종신 (2001) → CI 선지급 종신 (2002) →
  유니버셜 종신 (2004); and a **taxonomy table of the six Korean whole life shapes**.
- **What rests on it.** The scope decisions of the composite: which of the six shapes the
  reference product is (무배당, 금리확정형, 평준형) and which four are named and excluded, and
  the statement that this product is the chassis `CI_KR_S` and `Pension_KR_S` inherit.

(krlib-whole_life-r9)=

### R9 — 「2025년 보험산업 전망」 (2024-10-10), 보험연구원 황인창, 보험산업 전망과 과제 세미나 (research presentation)

- Document: 78-slide presentation, `smn_20241010.pdf`
- URL: https://www.kiri.or.kr/pdf/전문자료/smn_20241010.pdf
- Accessed: 2026-09-03. **Retrieved: yes** (2.1 MB PDF, 78 pp.; the Korean text extracts
  **without inter-word spaces**, a font-encoding artefact, so quotations are re-spaced and
  marked as such at the point of use)
- **What it establishes.** 보장성보험 수입보험료 2020–2024H1; the observation that 단기납 종신
  sales rose in 2024 Q1 and then tapered while 무·저해지환급형 건강보험 kept growing; a monthly
  초회보험료 chart for 무·저해지환급형 종신보험; and a forecast of a **9.2%** industry-wide
  초회보험료 decline for 2025.
- **What rests on it.** One sentence of market context in `product-spec.md`. The direction of
  the 단기납 종신 episode is sourced here; the specific carrier and 환급률 percentages
  circulating in the trade press are **[unverified]** and are marked so.

(krlib-whole_life-r12)=

### R12 — 보도자료 목록, 보험개발원 (press-release index page)

- URL: https://www.kidi.or.kr/user/nd11592.do
- Accessed: 2026-09-03. **Retrieved: yes** (WebFetch, HTTP 200; the ten most recent items
  listed, 2026-01 to 2026-08)
- **What it establishes.** **Negative evidence, which is why it is numbered.** No 경험생명표
  item appears in the current listing and no archive or search endpoint was reached, so the
  **제10회 경험생명표 was not sourced at all** in this product's research pass.
- **What rests on it.** The house position, stated in `product-spec.md`, in the `Data` Space
  docstring and in every `provenance` cell of `mort_table.csv`, that the table is not published
  in full and that the shipped file is therefore a **[std] construction** anchored on two
  carriers' disclosed grids [S2] [S8] and calibrated to public 완전생명표 statistics [REG-R38].
  The cross-product library records the same finding at [REG-R34].

(krlib-whole_life-r13)=

### R13 — 「금융통계월보(생명보험편)」, 생명보험협회 (industry statistics series)

- URL: https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do
- Accessed: 2026-09-03. **Retrieved: in part** (WebFetch, HTTP 200; the table catalogue and the
  note that the series is produced under a 2016-11 data agreement with 금융감독원 render, but
  the statistical tables themselves are drawn client-side and **no figure was obtained**)
- **What it establishes.** Structure only.
- **What rests on it.** Nothing quantitative. Cited as negative evidence that **no Korean
  industry lapse rate, 효력상실해약률 or 종신보험 신계약 series was obtained from a primary
  statistical source** — which is why the lapse assumption is bounded above by two disclosed
  *pricing* envelopes [S2] [S8] and below by the supervisor's *valuation* anchors [REG-R27],
  with the shape between them [std].

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, the Korea
reference library shared by all ten products. **Its R1–R62 numbering is its own and is
frozen**; it is not this page's R-numbering. Research provenance for those entries lives in
`_research/regulatory-actuarial.md`. The entries the whole life documents cite, in short form:

- **REG-R1** — 보험업법 제2조 (정의), 제4조 (보험업의 허가): the 생명보험 / 손해보험 / 제3보험
  licence split, and the 제1호가목 class this product is written under. Retrieved: yes.
- **REG-R2** — 보험업법 제5조·제127조 이하, **기초서류** (사업방법서, 보험약관, 보험료 및
  해약환급금의 산출방법서): the filing the 예정이율, 적용위험률 and 예정사업비율 actually live
  in, and which is not public. **This is why every pricing-basis parameter in this model is
  [std].** Retrieved: yes.
- **REG-R3** — 보험업법 제120조, 책임준비금 등의 적립, and its wholesale delegation to the
  감독규정. Retrieved: yes.
- **REG-R4** — 보험업법 제176조, 보험요율 산출기관 (보험개발원) and the 참조순보험요율 it
  files. Retrieved: yes.
- **REG-R5** — 보험업법 제181조 (보험계리), 제184조 (선임계리사의 의무 등). Retrieved: yes.
- **REG-R6** — 보험업법 제108조, 특별계정 — cited for the scope boundary: this is a 일반계정
  product and `VA_KR_S` is not. Retrieved: yes.
- **REG-R7** — 보험업법 시행령 제1조의2 (보험상품): the life list closes to 생명보험계약 and
  연금보험계약, which places 종신보험 outside 제3보험. Retrieved: yes.
- **REG-R8** — 시행령 제63조·제65조·제71조: 책임준비금 restated in IFRS 17 vocabulary
  (보험계약부채, 발생사고요소 / 잔여보장요소) and the three K-ICS solvency quantities.
  Retrieved: yes.
- **REG-R9** — 보험업감독규정 (금융위원회고시 제2026-16호), the whole 고시: 제1-2조's
  참조순보험요율, the **기준연령 요건** (남자 만 40세, 전기납, 월납) and the 보장성보험 /
  저축성보험 split that decides which 해약공제계수 applies. Retrieved: yes.
- **REG-R10** — 감독규정 제6-11조 등, 책임준비금 and 보증준비금: the IFRS 17 liability
  taxonomy, and the deletion of the old paragraphs that carried the 보험료적립금. Retrieved:
  yes.
- **REG-R11** — 감독규정 제6-11조의6, **해약환급금준비금**: a company-level reserve with no
  counterpart anywhere else in this repository. Cited and never computed. Retrieved: yes.
- **REG-R12** — 감독규정 제6-11조의7, 제6-13조, 계약자배당 — cited for the 무배당 scope
  boundary. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조, 제7-2조, 제7-2조의2, K-ICS 지급여력 and the 건전성감독기준
  balance sheet it is computed on. Retrieved: yes (the 기본요구자본 aggregation formula renders
  as an image and did not extract).
- **REG-R14** — 감독규정 제7-17조~제7-19조 (적기시정조치) and the 부칙 of 고시 제2022-53호,
  which is where **K-IFRS 1117 and K-ICS both commence on 2023-01-01**. Retrieved: yes.
- **REG-R16** — 감독규정 제7-60조, 생명보험의 상품설계: the **평균공시이율 accumulation test**
  a product design is measured against. Retrieved: yes.
- **REG-R17** — 감독규정 제7-63조, 제3보험의 상품설계 — cited only for the boundary this
  product sits outside. Retrieved: yes.
- **REG-R18** — 감독규정 제7-64조 (산출방법서 필수기재사항), 제7-65조 (계약자적립액), including
  **제2항's 「연납보험료를 기준으로 하여 산출할 수 있다」** — the permission that lets an
  annual grid carry a monthly-premium product's account. Retrieved: yes.
- **REG-R19** — 감독규정 제7-66조·제7-67조·제7-69조·제7-70조, 해약환급금: the identity
  「계약자적립액에서 … 해약공제액을 공제하여 계산한 금액 이상」, the **해약공제기간 capped at
  seven years** (제1항제2호), 해약공제액 = the 별표 14 표준해약공제액 (제1항제3호), the zero
  floor 「이를 영(零)으로 처리한다」, and 제4항제2호나목's post-완납 환급률 condition.
  Retrieved: yes (the 해약환급금 formula display and two tables render as images).
- **REG-R20** — 감독규정 **[별표 14] 표준해약공제액**: `연납순보험료 × 5% × 해약공제계수 +
  보험가입금액 × 10/1000`, with all seven notes, including the 보험기간-capped-at-20
  해약공제계수 and the **20년납 recomputation** of the 연납순보험료. The single most
  model-relevant page of Korean regulation for this product. Retrieved: yes (1-page PDF, full
  text).
- **REG-R21** — 감독규정 **[별표 15] 보험가입금액의 산정**: the 가입금액 that enters the cap is
  taken **before any 체증 or 체감**, and is the 일반사망보험금 for a 보장성보험 covering
  일반사망. Retrieved: yes (1-page PDF, full text).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조: first-year remuneration within the **first
  year's expected premium** (제4-32조제5항), and the **1.4 ×** 표준해약공제액 tolerance under
  which a 계약체결비용지수 need not be published (제7-45조제11항). Both are asserted by
  `check_acq_cost_cap()`. Retrieved: yes.
- **REG-R23** — 보험업감독업무시행세칙 as a whole: 제5-13조 (표준약관 = 별표 15), 제5-16조
  (공시기준이율). Retrieved: yes, with a version caveat that travels with the citation.
- **REG-R24** — 시행세칙 **[별표 27] 공시기준이율 산출 기준**: the four external index yields,
  the three-month weighted moving average and the 조정률. Retrieved: yes (two weight formulas
  render as images).
- **REG-R25** — 시행세칙 **[별표 15] 표준약관**, 492 pp.: **보험나이 제21조** and its six-month
  rule; 청약철회 제17조; 부활 제27조; 해지 제26조; 보험계약대출 제33조; and the 장해분류표 that
  defines the **50% 장해지급률** waiver trigger. Retrieved: yes.
- **REG-R26** — 시행세칙 **[별표 22] (K-ICS 지급여력) and [별표 24] (보증준비금)**.
  **Retrieved: no.** The **대량해지위험 shock, including the 고환급형 test**, is therefore
  second-hand through [REG-R36] and [R7] and every claim resting on it carries
  **[unverified]**. This is the instrument-level gap that matters most to this product and to
  `Term_KR_S`, because the 고환급형 test is about exactly their 무·저해지 forms.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (2024-11), 계리가정·할인율: the **원칙모형**, the
  **0.1% at 납입완료** convergence, the **0.8%** ultimate, and the **30% 이상** additional
  lapse at a bonus date. Retrieved: yes (the 보도자료 PDF and its 별첨; the 「IFRS17 주요
  계리가정 가이드라인」 HWP attachment was **not** converted, so the guideline's functional
  form is [unverified]).
- **REG-R28** — 무(저)해지환급금 보험 상품구조 개선 (2020 입법예고 and 개정), with the FSS
  소비자경보 (2019): the definition of the form, the market count, and the 「전(全) 보험기간
  동안 표준형 보험의 환급률 이내로」 framing recorded beside the 고시's own wording. Retrieved:
  yes.
- **REG-R29** — 금융위원회, 사업비·모집수수료 개편 (2019-08-01): the 표준해약공제액 stated as a
  multiple of the monthly premium — **보장성보험 13배** — used here only as a cross-check on
  the 별표 14 arithmetic. Retrieved: yes.
- **REG-R30** — 자본규제 고도화 (2025-03) and 금융감독원 지급여력비율 현황. Retrieved: in part.
- **REG-R32** — 예금보호한도 1억원 (2025-09-01). Retrieved: in part.
- **REG-R33** — **제10회 경험생명표**, as reported by 보험매일: 평균수명 남 86.3세 / 여 90.7세,
  65세 기대여명 남 23.7년 / 여 27.1년, applied to new business from April 2024. **This is a
  news article and it is the only retrieved source for the table**, which is why
  `mort_table.csv` is calibrated to these summary figures rather than built from rates.
  Retrieved: yes.
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 보험정보 빅데이터 플랫폼):
  **negative evidence** that the 경험생명표 is not published in full. Retrieved: in part.
- **REG-R36** — 보험연구원 CEO Report 03호 (2025-04): the **K-ICS 대량해지위험 shock table**
  quoted from 별표 22, and the 해약환급금준비금 schedule. Retrieved: yes. (The same document is
  this product's [R7].)
- **REG-R37** — 보험연구원 정원석 (2019-04-16): the **표준해약공제액 formula by product class**
  with a worked example. Retrieved: yes. (The same document is this product's [R6].)
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: the
  **완전생명표** and its 기대여명, published annually on **만나이** as public-sector open data.
  This is the public anchor the [std] mortality construction is calibrated to, and the reason
  the 보험나이 / 만나이 gap is a stated one-directional bias rather than a correction.
  Retrieved: yes.
- **REG-R45** — 생명보험협회 공시실, FACT BOOK and 금융통계월보(생명보험편). Retrieved: in
  part.
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier regulatory disclosure: the series, and
  the **2026 평균공시이율 of 2.50%** that the [std] 예정이율 is set equal to. Retrieved: in
  part.
- **REG-R49** — 상법 제4편 보험, 제1장 통칙 (제638조~제664조): contract formation, the 30-day
  acceptance rule, and 제649조's termination-at-any-time right, which is what makes surrender a
  contractual entitlement rather than an option the insurer grants. Retrieved: yes.
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): **제732조**, which voids a
  contract on the death of a person under 15 and sets the minimum issue age; and **제736조**,
  which obliges the insurer on a refused claim to pay 「보험수익자를 위하여 적립한 금액」 — so
  a refused claim is **not** a zero-payment event. Retrieved: yes.
- **REG-R51** — 금융소비자 보호에 관한 법률 제46조, 청약의 철회. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: the **₩100,000,000** payout limit. Retrieved: yes.
- **REG-R57** — 소득세법 제59조의4: the **12% 보장성보험료 세액공제** on up to ₩1,000,000 a
  year — a credit, not a deduction. Retrieved: yes.
- **REG-R58** — 소득세법 제16조제1항제9호 and 시행령 제25조, 저축성보험의 보험차익 — cited for
  the boundary this 보장성 product sits outside. Retrieved: yes.
- **REG-R59** — 상속세 및 증여세법 제8조·제34조: the death benefit as estate property, and the
  premium-payer attribution rule. Retrieved: yes.
- **REG-R60** — 한국회계기준원, K-IFRS 제1117호 제정 의결: the Korean adoption of IFRS 17,
  whose vocabulary the 감독규정 borrows and under which **no 보험료적립금 is booked as a
  separate statutory reserve** — the reason `pol_val_pp` is a 계약자적립액 and this model
  computes no reserve at all. Retrieved: in part (the 별첨 HWP carrying the standard's text was
  not opened).

---

## Provenance note

Every entry above traces to **`_research/whole-life.md`**, which is the citation ground truth
for this product: the fact extraction section by section, the carrier-by-carrier variation
table, the fetch failures and the gaps register. That file's source list is **never
renumbered**, and this page carries its ids verbatim; the [REG-R#] sequence belongs to
`references/regulatory-and-actuarial-references.md` and is a different, separately frozen
numbering that is likewise never renumbered. Where the two libraries hold the same document —
the 2024 계리가정 decision at [R3] and [REG-R27], the CEO Report at [R7] and [REG-R36], the
2019 사업비 presentation at [R6] and [REG-R37], the FSS 소비자경보 at [R4] and inside
[REG-R28] — both numbers are live and the product documents cite whichever pass established the
point, usually both.

The gaps register in the research file is not summarised here and should be read before this
product's numbers are relied on. Its load-bearing items, in order of how much they would
change: **no 자동대출납입 article was found in any retrieved Korean document**, so the absence
of a funded-lapse mechanic on this chassis is [unverified] and finding one would change the
chassis in kind; **별표 22 was not retrieved** [REG-R26], so the K-ICS 대량해지 shock is
second-hand; **no conventional level-premium 종신보험 약관 was retrieved** — the only full 약관
in the set is a 유니버셜 contract [S5] — which is the highest-value single document for the
next research pass; **no Korean expense rate as a percentage of premium was obtained from any
source**, so every 사업비 parameter in the model is [std] bounded above by the 표준해약공제액;
**no Korean lapse curve by duration is public**, so the shape between the two regulatory
endpoints is [std]; and **the 제10회 경험생명표 was not sourced at all** [R12] [REG-R34], so
`mort_table.csv` is a [std] construction and must never be presented as that table.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-whole_life-r1
[R12]: #krlib-whole_life-r12
[R3]: #krlib-whole_life-r3
[R4]: #krlib-whole_life-r4
[R6]: #krlib-whole_life-r6
[R7]: #krlib-whole_life-r7
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R37]: #krlib-reg-r37
[REG-R38]: #krlib-reg-r38
[REG-R48]: #krlib-reg-r48
[REG-R62]: #krlib-reg-r62
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
