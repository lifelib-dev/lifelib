# Sources

Sources for the tax-qualified pension savings product (*yeongeum jeochuk boheom*,
연금저축보험) — [`product-spec.md`](product-spec.md),
[`technical-notes.md`](technical-notes.md) and [`model.md`](model.md). **Access date for
every entry: 2026-09-03.**

**The numbering is per product.** `S1` and `R1` mean different documents in every other
product's `sources.md`, and they are carried verbatim from the numbering in
`_research/pension-savings.md`, which is frozen and is never renumbered — the product
documents cite against it, so a renumber would silently redirect every citation. Three tag
families are in use, and they mean different things:

| Tag | Resolves to | What it is |
|---|---|---|
| `[S#]` | this page, **Primary product sources** | A fact read off a carrier's own document — 약관 (policy conditions), 상품요약서 (statutory product summary), 상품안내장 (compliance-approved sales literature) or 공시자료 (regulatory rate disclosure). These are what the *contract* says |
| `[R#]` | this page, **Regulatory and actuarial references** | A statute, an enforcement decree, a supervisory 고시 or 별표, a tax-authority page or a statistical source that **only this product needs**. Mostly 소득세법 and its Decree, because the tax wrapper is what makes this product a distinct object |
| `[REG-R#]` | `references/regulatory-and-actuarial-references.md` | The **cross-product** Korean regulatory library, numbering frozen at R1–R62 and shared by all ten products. Reprinted in short form at the end of this page so a reader of this page alone can resolve them |

Two more tags resolve to definitions rather than to sources. **[std]** marks a
standardization introduced for the reference implementation: a value no retrieved document
gives, carried with a rationale and, where one exists, the observed range across insurers.
**[unverified]** marks a claim that could not be confirmed against a retrieved document.
`[derived]` is not a citation: it marks a figure computed here from published ones.

**Retrieval outcomes are recorded, never hidden.** Of the 18 primary sources, 14 were
retrieved in full and 4 in part; of the 22 regulatory references, 18 in full, 2 in part and
2 not at all. The two that failed — 소득세법 시행령 제187조의2 [R7] and 보험개발원's big-data
platform [R24] — are named at the point of use rather than papered over.

**Unused research numbers are omitted, so there are gaps**, on the same convention the
sister libraries follow. `_research/pension-savings.md` carries S1–S21 and R1–R25; six of
those are not cited by any of this product's documents and so have no entry here:

- **S17** and **S18**, the 손해보험협회 공시실 연금저축 비교공시 displays — the portal is
  [REG-R62], and no figure from either display reaches a document.
- **S21**, 한화생명 공시실 「적용이율」 — **not retrieved** (navigation shell only); that
  carrier's guarantee ladder came from its 약관 instead [S4].
- **R15**, 보험업감독규정 (본문) — **not retrieved**; the whole 고시 was retrieved in the
  cross-product pass as [REG-R9], which the documents cite instead.
- **R23**, a 2013 news item describing the pension-tax reform **as proposed**. Its 1/15 cap
  and 22% rate are not the law that was enacted, and nothing rests on it.
- **R25**, a carrier explainer on the 경험생명표 vintage question — **not retrieved**
  (DNS timeout). Its loss is why that question is answered from 약관 wording instead.
  Nothing was newly added at drafting: every entry below is already in the research file.

---

## Primary product sources

(krlib-pension_savings-s1)=

### S1 — 「무배당 우리WON인터넷연금저축보험 상품요약서」, ABL생명 (상품요약서)

- URL:
  <https://abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2026/07/09/NP_%EC%9A%B0%EB%A6%ACWON%EC%9D%B8%ED%84%B0%EB%84%B7%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C(260101).pdf>
- Publisher: 에이비엘생명보험주식회사 (ABL Life). Document: 판매 vintage 260101, 9 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** —
  downloaded and parsed locally with PyMuPDF and read in full; the markdown-converting
  fetcher returned only the binary stream.
- **The single most quantitatively complete document behind this product**, and the source of
  the composite's whole charge structure: 계약체결비용 **1.50%** of the monthly 기본보험료 for
  seven policy years, 계약관리비용 **3.00%** a month while premiums are due and **0.67%**
  after 납입완료, the 추가납입 charge of **2.00%** bearing 계약관리비용 only, the
  연금수령기간 관리비용 of **0.5%**, a 모집수수료율 table of **0.00% in every year** and a
  **해약공제액 table of all zeros**. It also gives the 최저보증이율 ladder 1.25 / 1.00 / 0.50,
  a 예정이율 of 2.50%, the 공시이율 with its month (2.40% at 2026-01), three 연금사망률 rates
  by sex at ages 50 / 60 / 70, a 해약환급금 예시 over twenty years on two interest bases, the
  연금수령한도 as a typeset equation, and the statement that 계약이전 is not a withdrawal.
- Rests on it: `pricing_table.csv`'s charge rows and `expense_table.csv`'s two commission
  rows; the nil `surr_chg_pp`; three of the six anchors in `mort_anchor_table.csv`; the
  guarantee ladder; and the finding that the composite's early-duration 환급률 is the
  direct-channel product's rather than the tied-channel product's.

(krlib-pension_savings-s2)=

### S2 — 「연금저축나이스플랜연금보험2601」 상품안내장, ABL생명 (보험안내자료)

- URL:
  <https://www.abllife.co.kr/cms/prdt/anutSav/__icsFiles/afieldfile/2026/01/06/%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%82%98%EC%9D%B4%EC%8A%A4%ED%94%8C%EB%9E%9C%EC%97%B0%EA%B8%882601_20260101.pdf>
- Publisher: 에이비엘생명보험주식회사. Document: 제작 2026-01-01, 준법감시인 심의필
  제2025-PA474호, 8 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded, parsed locally with PyMuPDF, read
  in full.
- A **participating** 연금저축보험 carrying three complete 연금액 예시표 on one model point —
  남자 40세, 기본보험료 월 50만원, 20년납, 연금개시나이 65세 — on three interest bases
  (최저보증이율, min(평균공시이율 2.50%, 공시이율 2.15%), and 공시이율 2.15%), each giving the
  fund at annuitisation and the monthly annuity under 종신연금형 10년 / 20년 보증 and
  확정연금형 10 / 15 / 20년, with the matching 해약환급금 예시표.
- Rests on it: **the anchor model point itself**; the 공시이율 of 2.15% and hence the whole
  `base` scenario; **all eight derived annuity factors** and therefore the calibration of
  `mort_table.csv` and the 0.5% annuity charge; the 100.1%-of-premiums floor at the
  연금개시일; the 2026 평균공시이율 of 2.50%; the 예금자보호 limit; and the fact that surrender
  is available up to the day before the 연금개시일. It is the one document in the set that
  fixes accumulation and annuitisation on a single consistent basis.

(krlib-pension_savings-s3)=

### S3 — 「무배당 ABL인터넷연금저축보험 보험약관」, ABL생명 (약관 — policy conditions)

- URL:
  <https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2021/09/24/20210925_NP_ABL%EC%9D%B8%ED%84%B0%EB%84%B7%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%B3%B4%ED%97%98.pdf>
- Publisher: 에이비엘생명보험주식회사. Document: 약관 with 부록, 127 pp. PDF, posted
  2021-09-25.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded and parsed locally; the tax article,
  the annuity benefit table and the 부록 statute reproduction read in full.
- 제21조[계약의 세제혜택 등] verbatim: the 세액공제, the 16.5% 기타소득세, the three-limb
  연금수령 test, the 연금수령한도 equation, the six 부득이한 사유 with their caps and the
  spouse-succession rule. Critically its **부록 reproduces 소득세법 시행령 제40조의2제2항–제5항
  verbatim**, which is the cleanest retrieved copy of that provision, and it carries the three
  최소 연금지급기간 tables that translate the 연금수령한도 into a minimum payout term.
- Rests on it: `tax_table.csv`'s 연금수령 rows — `min_annuity_age`, `min_account_years`,
  `limit_denominator_base` and `limit_uplift` — and `annuity_limit_pp`, jointly with [R6].

(krlib-pension_savings-s4)=

### S4 — 「한화생명 e연금저축보험 무배당 약관」, 한화생명 (약관 + 가이드북)

- URL:
  <https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e연금저축보험%20무배당_1772-029_032_약관_20240401.pdf>
- Publisher: 한화생명보험주식회사 (Hanwha Life). Document: 문서번호 1772-029/032, 2024-04-01
  vintage, 122 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded and parsed locally; the rate, annuity,
  tax and surrender sections read.
- A direct-channel carrier with a **different 최저보증이율 ladder from every other retrieved
  document** — three bands stepping at 3 and 5 years rather than two stepping at 5 and 10 —
  which is what shows the ladder to be a product-vintage variable. It carries 제6조
  「공시이율의 적용 및 공시」 verbatim including the 공시기준이율 construction, a 별표1 benefit
  table with 종신연금형 at 10년 / 20년 / 100세 보증 and 확정기간연금형 at 10 / 15 / 20년, the
  **100.1% minimum guarantee with its two disapplication triggers** (별표1 주10), the
  annuity-mortality **ratchet clause** (주11), and the statement that a contract crediting the
  floor still bears its charges.
- Rests on it: the death benefit as the fund and nothing more; the floor's disapplication,
  which is model point 9's `min_fund_on = 0`; one of the six independent statements of the
  ratchet clause; and the rule that `charge_from_av_pp` does not consult the guarantee.

(krlib-pension_savings-s5)=

### S5 — 「삼성생명 연금저축골드연금보험 B1.4(무배당)」 상품안내장, 삼성생명 (보험안내자료)

- URL: <https://image.kebhana.com/cont/download/insdocument/leaflet/08L03014230_r.pdf>
- Publisher: 삼성생명보험주식회사 (Samsung Life), sold through KEB하나은행. Document:
  판매개시일 2016-04-01, 준법감시필 BA 제16-28호, 4 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded, parsed locally, read in full.
- An **older-vintage** contract, retained deliberately: it shows the tax parameters *before*
  the 2023 and 2026 reforms (₩4,000,000 credit cap, ₩12,000,000 threshold, 종신연금형 4.4%),
  and carries the fullest published 연금지급 예시 — 종신연금형 at four guarantee lengths and
  확정기간연금형 at five terms, each on three interest bases — plus a 해약환급금 예시 with a
  **세후지급 예상액 column uniformly 83.5% of the surrender value**, exactly 1 − 16.5%. It
  also publishes a **13-month 공시이율 history** falling 3.55% → 2.98% in steps of two to
  seven basis points without reversing, a 평균공시이율 of 3.5% for 2016, a 최저보증이율 of
  1.5% / 1.0%, and 「보험료 납입면제 사유 : 없음」.
- Rests on it: the treatment of the declared rate as a **slow-moving step function** rather
  than a market rate; the 0.67% paid-up charge as a market feature rather than one carrier's;
  the empirical confirmation of the 16.5% 기타소득세 bite; the absence of a premium waiver;
  and the top of the observed guarantee range.

(krlib-pension_savings-s6)=

### S6 — 「e-NH연금저축보험(무배당)_2404 약관」, NH농협생명 (약관 — policy conditions)

- URL: <https://image.kebhana.com/cont/download/insdocument/provide/L42014209M_agree.pdf>
- Publisher: NH농협생명보험주식회사. Document: 주계약 + 특약 + 별표, 88 pp. PDF, 판매월
  2026-01.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded and parsed locally; the benefit
  table, the age article, the contract-variation article and the rate notes read.
- The **widest annuity-form menu** of any retrieved contract — 종신연금형 at 10 / 20 / 30년
  보증, 확정기간연금형 at 10 to 30년, and a **자유설계연금형** splitting the fund between the
  two in 10% units. It is also **the only retrieved contract stating the 보험나이 / 만나이
  rule explicitly** (제20조): 보험나이 governs except the statutory 만 55세 test. Its annuity
  basis is 「무배당 경험 개인연금사망률」 and the ratchet appears as 별표1 주10.
- Rests on it: the age-basis convention of the whole model and the **[std]** simplification
  that reads both statutory tests off `age(t)`; the payout-form menu; and one more independent
  statement of the ratchet and of the death benefit.

(krlib-pension_savings-s7)=

### S7 — 「우체국연금저축보험 2504 상품요약서」, 우체국보험 (상품요약서 — statutory summary)

- URL: <https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/yoyak_P210061_202504.pdf>
- Publisher: 우체국예금·보험, 체신관서 (Korea Post Insurance). Document: 2504 vintage,
  14 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — the default
  extraction dropped the numerals because of the layout, so pages were re-extracted with
  `sort=True`, after which the document read cleanly.
- The **only retrieved 연금저축보험 with a non-zero 해지공제액** — ₩104,000 at year 1 falling
  to zero at year 5, published both in won and as a percentage of premiums paid
  (**8.7% → 0%**).
  It also gives a full 개인연금사망률 table at ages 40 / 60 / 80 for both sexes, a 예정이율 of
  2.5%, a 최저보증이율 of 1.0% / 0.5%, a five-year 계약자배당 history with its 기준율, a
  해약환급금 예시 at two premium sizes, 전건 무진단 underwriting, and a fee schedule split into
  판매보수 / 유지보수 / 계약관리비용 / **연금수령기간 관리비용** / 추가납입 비용.
- Rests on it: model point 8's front-end `surr_chg_rate`; the other three of the six anchors
  in `mort_anchor_table.csv`; the corroboration of the 0.5% annuity charge at a second
  carrier; and the corroboration that the 연금사망률 is handed to the policyholder **at
  inception**, which is the evidence for the `issue` vintage being the base reading.
- Publisher note: 우체국보험 is supervised by 과학기술정보통신부 rather than by the FSC — a
  statutory carve-out from 보험업법 — so its schedule is quoted as a bracket on market
  practice, never as evidence of what 감독규정 requires.

(krlib-pension_savings-s8)=

### S8 — 「연금저축손해보험 현대해상다이렉트연금보험(Hi2504)」, 현대해상 (약관 + 상품안내)

- URL: <https://direct.hi.co.kr/dhNAS/terms/CM106N_20250901.pdf>
- Publisher: 현대해상화재보험주식회사 (Hyundai Marine & Fire), a **non-life** insurer.
  Document: file CM106N dated 2025-09-01, 97 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded and parsed locally; the
  product-envelope, rate, annuity and tax sections read.
- The **non-life form of the same statutory wrapper**, and the cleanest demonstration of what
  a 손해보험사 may and may not write: its only 연금지급형태 is 정액형 over 5년 ~ 25년, there is
  **no 종신연금형 at all**, and therefore no annuity mortality in the contract. It names its
  crediting rate 「연금저축 공시이율Ⅴ」, gives a 1.25% / 1.0% / **0.3%** ladder (the lowest
  long-duration floor observed), defines 해약공제액 as 미상각 신계약비, states 「공시이율이
  0.1%로 낮아지더라도 적립금은 … 최저보증이율로 적립됩니다」, and cites 감독규정 제1-2조's
  저축성보험 definition as the reason the annuity start date is deferred.
- Rests on it: the statement that the floor guarantees the **credited rate** and not the
  return; the bottom of the observed guarantee range; the 납입유예 shape; and the
  life/non-life scope boundary the specification draws.

(krlib-pension_savings-s9)=

### S9 — 「연금저축 교보First연금보험 약관」, 교보생명 (약관 — policy conditions)

- URL: <https://lawinsider.com/ko/contracts/aXubiP59oQE>
- Publisher: 교보생명보험주식회사 (Kyobo Life). Document: 주계약 + 별표1 + 별표2, vintage
  unknown.
- Accessed: 2026-09-03. Retrieved:
  **in part** — fetched through a third-party contract mirror rather than the carrier's own
  공시실; the articles quoted returned, but the edition date and filing reference did not, so
  the vintage is unknown and is treated as older-generation.
- A **much higher guarantee ladder** than any other retrieved contract — 연복리 2.0% under ten
  years and 1.5% at ten years and over — which brackets the top of the observed range. Also
  종신연금형 at 10 / 20 / 30년 / 100세 보증, 확정연금형 at 5 to 30년, 연금지급개시나이
  만55세~80세, the bar on surrender after the first instalment of a 종신연금형, and the same
  ratchet clause at 별표2 주9.
- Rests on it: the observed range of the guarantee ladder, and one more independent
  attestation of the ratchet. No composite parameter is taken from it.

(krlib-pension_savings-s10)=

### S10 — 「(무)AIA 여유+ 변액연금보험 상품요약서」, AIA생명 (상품요약서 — statutory summary)

- URL:
  <https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/saving/summary/AIA_kr_Form107_20260101.pdf>
- Publisher: AIA생명보험주식회사 (AIA Life Korea). Document: Form 107, 2026-01-01 vintage,
  18 pp. PDF.
- Accessed: 2026-09-03. Retrieved: **yes** — downloaded, parsed with `sort=True`, the
  annuitisation sections read.
- **Scope caution, carried from the research file:** this is a **변액연금보험**, not a
  연금저축보험. It is cited **only** for annuitisation machinery — the fullest annuity-form
  taxonomy retrieved (보증기간부 종신연금형 with 정액형 and 체증형, 보증금액부 종신연금형,
  확정연금형, 상속연금형, 실적연금형), the definition that 「100세 보증」 means a
  (101 − 연금개시나이)-year guarantee, and the same mortality-vintage ratchet clause at 주4.
  **No accumulation, expense, tax or rate parameter in this product rests on it.** It belongs
  primarily to `_research/variable-annuity.md`.

(krlib-pension_savings-s11)=

### S11 — 「e원금보장 KDB하이브리드연금저축보험(무)」 상품 페이지, KDB생명 (product page)

- URL: <http://direct.kdblife.co.kr/edirect/product/hybrsavingDetail.do>
- Publisher: KDB생명보험주식회사. Document: product page, rates stated as at 2024년 10월.
- Accessed: 2026-09-03. Retrieved: **yes** (HTML fetch, converted and read).
- A **hybrid rate design** absent from every other retrieved carrier: a fixed 연복리 **3.5%
  확정이율 for the first five contract years**, then the ordinary 신공시이율(무배당 연금저축Ⅳ),
  with a 1.0% / 0.5% floor. Also 가입나이 만19세 ~ (연금개시나이 − 납입기간), 연금개시나이
  만55~80세, the annuity-form menu, and a plain statement of the **16.5% / 13.2%** credit
  rates with the resulting maximum refunds of ₩990,000 and ₩792,000.
- Rests on it: the `hybrid` scenario of `decl_rate_table.csv`, which model point 8 runs; the
  2024-10 point in the observed declared-rate range; and the consumer-side corroboration of
  the grossed-up credit rates.

(krlib-pension_savings-s12)=

### S12 — 「금리연동이율공시」, DB생명보험주식회사 (공시이율 disclosure)

- URL: <https://www.idblife.com/notice/product/tmo_int>
- Document: monthly declared-rate disclosure, table dated **2026-09-01**. Accessed:
  2026-09-03. Retrieved: **yes** (HTML fetch, table read).
- The **current market level of the 연금저축 공시이율**, two days before the access date, with
  the prior month beside it: 3.01% and 2.82% on two 연금저축 vintages inside one carrier on
  one date. It is the only retrieved source that dates a declared rate to the current month.
- Rests on it: the top of the 2.1%–3.0% observed range against which the composite's 2.15% is
  described as the conservative arm, and the 19-basis-point intra-carrier spread `[derived]`.

(krlib-pension_savings-s13)=

### S13 — 「적용이율 공시 — 최저보증이율 및 경과기간별 중도해지율」, 하나생명 (공시자료)

- URL: <https://www.hanalife.co.kr/anm/interestRate/interestRate_tab5.do>
- Accessed: 2026-09-03. Retrieved: **yes** (HTML fetch, table read).
- A **by-vintage** 최저보증이율 table across one carrier's whole 연금저축 shelf, keyed to each
  product's 판매개시일 — the evidence that the ladder is a function of sale date rather than
  of carrier, with two ladders running side by side inside one shelf. Its second column is the
  **경과기간별 중도해지율**, and **every row of it reads 「적용안함」**.
- Rests on it: `guar_rate_table.csv`'s ladder; and, as **negative evidence**, the whole
  argument that `lapse_table.csv` must be **[std]** — this is the one regulatory disclosure in
  Korea that has a lapse-by-duration column, and the carrier declines to populate it.

(krlib-pension_savings-s14)=

### S14 — 「적용이율 공시 — 표준이율 및 평균공시이율」, 하나생명 (공시자료 — rate disclosure)

- URL: <https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do>
- Accessed: 2026-09-03. Retrieved: **yes** (HTML fetch, both tables read).
- The **평균공시이율 time series 2016–2026** with the current year's value of **2.50%**, and
  the definition of the 평균공시이율 as the regulator-defined average of all insurers' declared
  rates — a supervisory parameter, published by carriers, that enters illustration and
  discounting rules directly.
- Rests on it, jointly with [REG-R48]: `pricing_table.csv`'s `avg_decl_rate`, which enters the
  model only inside `surr_chg_cap_pp` (별표 14 주6's discounting) and as the ceiling reference
  for the **[std]** policy-loan rate.

(krlib-pension_savings-s15)=

### S15 — 「적용이율공시 최저보증이율(연금저축상품)」, 교보라이프플래닛 (공시자료)

- URL: <https://www.lifeplanet.co.kr/disclosure/good/HPDA45S2.dev>
- Accessed: 2026-09-03. Retrieved: **in part** — the guarantee-ladder rows returned; the
  current-month declared rate and the 경과기간별 중도해지율 tab are rendered client-side and
  did not return.
- A third guarantee-ladder shape, 1.25% / 1.00% / **0.75%**, with the effective dates of the
  products it applies to. Cited only in the variation table of `product-spec.md`.

(krlib-pension_savings-s16)=

### S16 — 「연금저축 비교공시 — 가입시 유의사항」, 하나생명 (비교공시 boilerplate)

- URL: <https://www.hanalife.co.kr/anm/annuityProduct/annuityProduct_tab4.do>
- Accessed: 2026-09-03. Retrieved: **yes** (HTML fetch, read).
- The four-way comparison of 연금저축신탁 / 연금저축펀드 / 생보 연금저축보험 / 손보
  연금저축보험 across 납입방식, 연금수령기간, 원금보장 and 예금자보호 — the crispest single
  statement of what distinguishes the three statutory wrappers, and of the fact that only the
  life-insurer leg can pay a life annuity.
- Rests on it: the wrapper comparison in `product-spec.md`'s overview, and the 16.5%
  기타소득세 statement counted among the nine carrier documents that state it identically.

(krlib-pension_savings-s19)=

### S19 — 연금저축 비교공시 › 판매회사별 적립금, 금융감독원 (통합연금포털 display)

- URL: <https://www.fss.or.kr/fss/lifeplan/goodsCmpr/list.do?menuNo=200961>
- Accessed: 2026-09-03. Retrieved: **in part** — the page returned a **stale quarter
  ('22.2분기)** rather than the current one, because the quarter selector is a client-side
  control. The category list (수익률 / 수수료율 / 장기 수익률 / 장기 수수료율, each at 3 / 5 /
  7 / 10 years) was read and is reliable; the figures are four years out of date and are
  **not** used for any current parameter.
- Rests on it: nothing quantitative. It is cited as **negative evidence** in the lapse
  argument — the supervisor's own comparison display exists, and it did not yield a current
  behavioural series.

(krlib-pension_savings-s20)=

### S20 — 공시실 (pub.insure.or.kr), 생명보험협회 (industry disclosure portal)

- URL: <https://pub.insure.or.kr/>
- Accessed: 2026-09-03. Retrieved: **in part** — the landing page returned its category tree
  (상품비교공시 with a 저축성보험 › 연금 branch, 경영공시, 대출공시, 기타공시) but every leaf
  table is loaded client-side and none returned.
- Recorded because the house brief names this portal as the best single source of quantitative
  Korean product data. In this session it was reachable but not readable, and its role was
  filled by the carriers' own 상품요약서 [S1] [S7] and 상품안내장 [S2] [S5]. Cited only in the
  scope note of `product-spec.md`, and no parameter rests on it.

---

## Regulatory and actuarial references

(krlib-pension_savings-r1)=

### R1 — 소득세법 제59조의3 (연금계좌세액공제), 법제처 (primary legislation)

- URL: <https://casenote.kr/법령/소득세법/제59조의3> (consulted through CaseNote).
  Accessed: 2026-09-03. Retrieved: **yes**. Version returned: 법률 제19196호, 시행 2023-01-01.
- The credit itself: **12%** of amounts paid into a 연금계좌, or **15%** where 종합소득금액 is
  ₩45,000,000 or less (총급여액 ₩55,000,000 for employment income only); contributions to a
  연금저축계좌 above **₩6,000,000** a year disregarded, and 연금저축 plus 퇴직연금계좌 above
  **₩9,000,000** disregarded. The retrieved consolidation is the amendment that raised those
  caps and removed the age-and-income sub-cap; no later amendment was found, and the caps
  match every 2026-vintage carrier document [S2] [S11] and the tax authority's own page [R8].
- Rests on it: `tax_table.csv`'s `credit_*` rows and `tax_credit_pp`, and the statement that
  Korean relief is a **credit and not a deduction**.

(krlib-pension_savings-r2)=

### R2 — 소득세법 제20조의3 (연금소득), 법제처 (primary legislation)

- URL: <https://casenote.kr/법령/소득세법/제20조의3>. Accessed: 2026-09-03. Retrieved:
  **yes**. Version returned: 법률 제19933호, 시행 2024-01-01.
- 제1항제2호 makes an amount withdrawn from a 연금저축계좌 in a 연금형태 into 연금소득, split
  into 가목 untaxed 퇴직소득, 나목 contributions that received the credit, and 다목 investment
  return. **That 가/나/다 split is the whole architecture of the withdrawal tax**: money that
  never received a credit is outside the charge entirely.
- Rests on it: the wrapper definition in `product-spec.md` and the reason the 기타소득세 base
  is the payout less uncredited contributions rather than the whole payout.

(krlib-pension_savings-r3)=

### R3 — 소득세법 제14조 제3항 (분리과세 소득), 법제처 (primary legislation)

- URL: <https://casenote.kr/법령/소득세법/제14조>. Accessed: 2026-09-03. Retrieved: **yes**.
  Version returned: 법률 제19933호, 시행 2024-01-01.
- 제9호 defines 분리과세연금소득 and fixes the **₩15,000,000** threshold, raised from
  ₩12,000,000 for the 2023 tax year; 제8호나목 routes 연금외수령 기타소득 into separate
  taxation as well.
- Rests on it: `tax_table.csv`'s `aggregation_threshold` and the routing of the 16.5%
  기타소득세 as a final separate charge rather than an aggregated one.

(krlib-pension_savings-r4)=

### R4 — 소득세법 제64조의4 (분리과세연금소득 세액계산 특례), 법제처 (primary legislation)

- URL: <https://casenote.kr/법령/소득세법/제64조의4>. Accessed: 2026-09-03. Retrieved:
  **yes**. Version returned: 법률 제19196호, 시행 2023-01-01, 신설 2022-12-31.
- Where pension income exceeds the separate-taxation threshold, the tax may be computed by
  applying **100분의 15** to it — the statutory basis of the "16.5% including local income
  tax" election every carrier document describes for an above-threshold annuity.
- Rests on it: the above-threshold branch of the tax discussion in `product-spec.md`. Nothing
  in `net_cf` depends on it.

(krlib-pension_savings-r5)=

### R5 — 소득세법 제129조 (원천징수세율) 제1항제5호·제5호의2, 법제처 (primary legislation)

- URLs: <https://www.law.go.kr/LSW//lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000821176&lsId=001565&print=print>
  (the `print=print` article form is the law.go.kr shape that returns text) and
  <https://casenote.kr/법령/소득세법/제129조>. Accessed: 2026-09-03. Retrieved: **yes**, and in
  two versions, which is the point.
- CaseNote returned 법률 제19196호, 시행 2025-01-01, whose 제5호의2 다목 reads 「… **100분의
  4**」; 국가법령정보센터's print form returned 법률 **제21221호, 시행 2026-01-01**, in which
  the same 다목 reads 「… **100분의 3**」. 가목 taxes private pension income at 5% under 70,
  4% from 70 to under 80 and 3% at 80 and over. **The 종신계약 reduction from 4% to 3% with
  effect from 2026-01-01 is the most recent substantive change in this file.**
- Rests on it: `tax_table.csv`'s four `pension_tax_rate_*` rows and `pension_tax_rate(t)`, and
  the finding that the tax code pays a **2.2-percentage-point** standing premium for
  annuitising for life.

(krlib-pension_savings-r6)=

### R6 — 소득세법 시행령 제40조의2 (연금계좌 등), 법제처 (enforcement decree)

- URLs, three independent retrievals:
  <https://www.law.go.kr/LSW//lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000656323&lsId=003956&print=print>
  (대통령령 제36343호, 시행 2026-07-01);
  <https://www.nhis.or.kr/lm/lmxsrv/law/lawLinkContentView.do?SEQ=393&LINKCODE=c004000200>;
  and the 부록 of [S3], which reproduces 제2항–제5항 as filed contract wording. Accessed:
  2026-09-03. Retrieved: **yes**.
- 제2항 sets the **₩18,000,000** annual contribution ceiling and bars contributions once
  annuitisation has been requested. 제3항 sets the **three-limb 연금수령 test** and the
  **연금수령한도** formula. 제4항 defines 연금수령연차 and its **disapplication from 11**;
  제5항 deems any excess over the limit to be 연금외수령.
- Rests on it: `tax_table.csv`'s `contribution_ceiling`, `min_annuity_age`,
  `min_account_years`, `limit_denominator_base` and `limit_uplift`; `annuity_limit_pp`,
  `annuity_year_no` and `check_annuity_limit`; and the statutory constraints the projection is
  required to respect.

(krlib-pension_savings-r7)=

### R7 — 소득세법 시행령 제187조의2 (종신계약의 범위), 법제처 (enforcement decree)

- URLs tried: <https://www.taxcanvas.kr/core/law/0039562026052236343/history/2026-05-22/articles/0187021>;
  <https://www.nhis.or.kr/lm/lmxsrv/law/joHistoryContent.do?SEQ=393&SEQ_CONTENTS=4454757&DATE_START=20241112&DATE_END=20240702>;
  <https://elaw.klri.re.kr/kor_service/lawViewTitle.do?hseq=42184>. Accessed: 2026-09-03.
  Retrieved: **no** — the first two returned navigation only, and the KLRI site returned the
  article's **title in both languages** (「종신계약의 범위」 / "Scope of Life-Long Pension
  Agreement", 대통령령 제27829호, 2017-02-03) but not its body.
- **The existence, number and subject of the article are verified; its operative text is
  not.** Search snippets gloss it as 「사망일까지 연금수령하면서 중도 해지할 수 없는 계약」,
  and that gloss matches every retrieved 종신연금형 wording [S4] [S5] [S9] [S10], but the
  definition itself is **[unverified]**.
- Consequence carried in the documents: whether a **guarantee period of any length preserves
  종신계약 status** is [unverified], and with it the flat 3.3% withholding at the anchor cell
  and the 100%-life-form annuitisation election.

(krlib-pension_savings-r8)=

### R8 — 「연금계좌 세액공제」, 국세청 (National Tax Service) (tax authority guidance)

- URL: <https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7875>. Accessed:
  2026-09-03. Retrieved: **yes**.
- The administrative restatement of [R1] as a two-row table (≤ ₩45m → 15%, > ₩45m → 12%, both
  on ₩6,000,000 / ₩9,000,000), the account-type definitions, and the **ISA-conversion add-on
  of 10% of the transferred amount capped at ₩3,000,000**.
- Rests on it: corroboration of the credit rates and caps, and the ISA add-on noted as out of
  scope in `product-spec.md`.

(krlib-pension_savings-r9)=

### R9 — 「연금소득 원천징수 방법」, 국세청 (tax authority guidance)

- URL: <https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=6608&cntntsId=7888>. Accessed:
  2026-09-03. Retrieved: **yes**.
- The withholding table for private pension income — 70세 미만 5%, 70–80세 4%, 80세 이상 3% —
  and separately **종신계약 3%, footnoted as applying from 2026-01-01 (previously 4%)**, which
  corroborates [R5] from an administrative source. It also gives the 이연퇴직소득 rule and its
  2026 variants, and states the above-threshold 분리과세 15% election.
- Rests on it: the same `pension_tax_rate_*` rows as [R5], read twice from independent sources
  because the 2026 change is recent enough to be mis-stated in secondary material.

(krlib-pension_savings-r10)=

### R10 — 「연금세제 안내 › 연금저축 세제 › 세액공제」, 금융감독원 (supervisory guidance)

- URL: <https://fss.or.kr/fss/main/contents.do?menuNo=201007>. Accessed: 2026-09-03.
  Retrieved: **yes** (the rate table returned; the worked examples and the last-updated stamp
  did not).
- The supervisor's own statement of the credit **grossed up for local income tax**: ≤
  ₩45,000,000 → **16.5%**, above → **13.2%**, cap ₩6,000,000 in both rows. This is the
  document that ties the statutory 15% / 12% of [R1] to the rates every carrier quotes.
- Rests on it: `tax_credit_rate()`'s 16.5%. The grossing-up arithmetic itself remains
  **[unverified]** at instrument level because the 지방세법 imposing the surtax was not
  retrieved — see [REG-R56].

(krlib-pension_savings-r11)=

### R11 — 사적연금제도 › 개인연금제도 › 연금저축, 법제처 (plain-language consolidation)

- URL:
  <https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2056&ccfNo=3&cciNo=2&cnpClsNo=1>.
  Accessed: 2026-09-03. Retrieved: **yes**.
- The government's own consolidation with article pinpoints throughout: the 연금저축계좌
  definition, the three wrapper forms, the ₩18,000,000 ceiling, the three-limb 연금수령 test,
  the 세액공제, and — most usefully — the **current withholding table including the 2026
  change**: 70세 미만 확정형 5.5% / 종신형 3.3%, 70–80세 4.4% / 3.3%, 80세 이상 3.3%.
- Rests on it: the third independent statement of the withholding bands, and the wrapper
  taxonomy in `product-spec.md`.

(krlib-pension_savings-r12)=

### R12 — 「연금저축 길라잡이」, 금융감독원 (consumer guide, 12 pp. PDF)

- URL:
  <https://abllife.co.kr/cms/adm/attach/attach06/attach061/attach0611/연금저축_길라잡이(150401).pdf>
  (the guide is the FSS's; the copy retrieved is the one republished by ABL생명, whose file
  name and internal navigation are the FSS's). Accessed: 2026-09-03. Retrieved: **yes**
  (parsed locally with `sort=True`).
- **Vintage caution:** its tax figures are the 2015 ones (₩4,000,000 cap, 13.2%) and are
  superseded; it is cited for structural facts only. Content used: the four-column wrapper
  comparison; the statement that **생보사 products can pay a life annuity and 손보사 products
  for at most 25 years**; the fee-shape contrast (banks and securities firms charge on the
  balance, insurers on the premium); and a **worked 연금수령한도 calculation**.
- Rests on it: the fee-shape contrast that separates this product from its two sibling
  wrappers, and an independent worked example of the 연금수령한도 formula.

(krlib-pension_savings-r13)=

### R13 — 「2025년 우리나라 연금저축(PSA) 투자 백서」 보도자료, 금융감독원 (press release)

- URL: <https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=218674&menuNo=200218>, 등록일
  2026-06-18. Accessed: 2026-09-03. Retrieved: **in part** — the press-release body returned
  (title, issuer, headline statistics); **the attached hwpx and pdf, which hold the detailed
  tables including the payout-phase and behavioural statistics, did not convert**.
- Retrieved content: end-2025 적립금 **198.2조원** (+19.3조원, +10.8%); 가입자 840.3만명; by
  wrapper 연금저축보험 114.1조원, 연금저축펀드 61.3조원 (**+50.7%**), 연금저축신탁 13.8조원;
  2025 return 10.6%.
- Rests on it: the market context in `product-spec.md`, and — as the third strand of the lapse
  argument — the money moving from insurance to funds, which is 계좌이체 rather than surrender.
  The failure of its attachments is one of the two reasons `lapse_table.csv` is **[std]**.

(krlib-pension_savings-r14)=

### R14 — 보험업감독규정 [별표 14] 표준해약공제액 (제7-66조 관련), 금융위원회 (고시 별표)

- URL:
  <https://www.law.go.kr/LSW//flDownload.do?flSeq=137472119&flNm=%5B%EB%B3%84%ED%91%9C+14%5D+%ED%91%9C%EC%A4%80%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88%EA%B3%84%EC%82%B0%EC%8B%9C+%EC%A0%81%EC%9A%A9%EB%90%98%EB%8A%94+%ED%95%B4%EC%95%BD%EA%B3%B5%EC%A0%9C%EC%95%A1%28%EC%A0%9C7-66%EC%A1%B0%EA%B4%80%EB%A0%A8%29>
- Document: 개정 2011-01-24 / 2015-05-07 / 2020-01-15, 법제처 stamp 2024-02-01. Accessed:
  2026-09-03. Retrieved: **yes** — the whole table and all seven notes extract cleanly.
- The statutory cap on the surrender charge, including **주5's 연금저축보험-specific rule**:
  3% of the 연납순보험료 for a 무배당 연금저축보험 and 4% if 배당, against the general 5%, with
  주4's 6% concession expressly denied to this product. 주2 caps the coefficient at a
  twelve-year premium term, 주3 defines the 연납순보험료, 주6 subtracts the discounted loading.
- Rests on it: **the whole of `surr_chg_cap_pp`** and `check_surr_chg_cap`, the four
  coefficient rows of `pricing_table.csv`, the ₩1,421,988.72 at the anchor cell, and the
  reason the composite is written 무배당. Cited jointly with the cross-product copy of the
  same schedule at [REG-R20], which was retrieved separately.

(krlib-pension_savings-r16)=

### R16 — 보험업법 제176조 (보험요율 산출기관), 법제처 (primary legislation)

- URL: <https://casenote.kr/법령/보험업법/제176조>. Accessed: 2026-09-03. Retrieved: **yes**.
  Version returned: 법률 제17636호, 시행 2020-12-08.
- The statutory office of the 보험요율산출기관 — in fact 보험개발원 — covering 순보험요율의
  산출·검증 및 제공, the collection of insurance statistics, and research; 제5항 obliges it to
  accumulate industry statistics systematically. The retrieved page also carries commentary
  noting that an insurer is **not bound** by the 참조순보험요율 it files. **There is no
  publication obligation.**
- Rests on it: the legal frame for 경험생명표 and 개인연금사망률, and hence the central
  statement that `mort_table.csv` must be a **[std]** construction rather than a copy.

(krlib-pension_savings-r17)=

### R17 — 보도자료 목록, 보험개발원 (KIDI) (press-release index)

- URL: <https://www.kidi.or.kr/user/nd11592.do>. Accessed: 2026-09-03. Retrieved: **in part**
  — the list returned rows 740–746 (2026-05 to 2026-08) with titles and dates, but **no
  경험생명표 item appears in the visible window**, and every item link is a
  `javascript:goBoardView(...)` call, so no individual release could be opened. The 제10회
  경험생명표 announcement is older than the visible window and could not be reached by paging.
- Cited as **negative evidence**: the primary KIDI release could not be opened, which is why
  the 제10회 summary statistics are taken from trade reporting [R18] [R19] and from the
  cross-product entry [REG-R33], and why every quantitative mortality row in this product is
  **[std]**.

(krlib-pension_savings-r18)=

### R18 — 「제10회 경험생명표 개정…소비자에 미치는 영향은」, 보험매일 (news report)

- URL: <https://www.fins.co.kr/news/articleView.html?idxno=99460>, 김명재 기자, 2024-01-10.
  Accessed: 2026-09-03. Retrieved: **yes**. **News source**, used because the primary release
  could not be reached [R17].
- 제10회 경험생명표 평균수명 **남 86.3세, 여 90.7세** (+2.8 / +2.2 on the 제9회); pricing on it
  from April 2024; annuity premiums to rise and 종신보험 premiums to fall; and the operative
  limitation that **the revised table applies to new business only — existing policyholders'
  premiums do not change.**
- Rests on it: the size of the vintage step that `annuitant_revised` represents, and — jointly
  with [R20] — the corroboration that the base factor is struck on the **가입시점** table.

(krlib-pension_savings-r19)=

### R19 — 「4월부터 연금보험 수령액 줄어든다…」, 보험저널 (news report)

- URL: <https://www.insjournal.co.kr/news/articleView.html?idxno=21975>, 강성용 기자,
  2024-02-15 (수정 2024-02-20). Accessed: 2026-09-03. Retrieved: **yes**. **News source.**
- A three-generation comparison on a fixed ₩200,000,000 fund annuitising at 60: 6차 to 78.4세
  at ₩906,000 a month, 9차 to 85.3세 at ₩709,000, and 10차 to 86.3세 at "60만원 후반" — about
  **15%** off the monthly annuity. The article does **not** distinguish 가입시점 from
  개시시점 application.
- Rests on it: the magnitude used to argue that a revision normally **decreases** the annuity,
  so the ratchet is out of the money in the base run.

(krlib-pension_savings-r20)=

### R20 — 「2024년 개정 경험생명표 보험료 영향은」, 웰스매니지먼트 (opinion column)

- URL: <http://www.wealthm.co.kr/news/articleView.html?idxno=11407>, 김희정, 2024-07-03.
  Accessed: 2026-09-03. Retrieved: **yes**. **News/opinion source.**
- Quantified premium effects of the revision (종신보험 about −5%, 암보험 about +10%; the 2019
  revision cut 종신보험 premiums 3.8% on average) and the statement that 「기존 가입자는 가입
  당시 경험생명표를 바탕으로 이미 보험료가 결정돼 있어 영향을 받지 않는다」.
- Rests on it: the second corroboration that a table revision reaches new business only, which
  is the inference the `issue` vintage default is built on.

(krlib-pension_savings-r21)=

### R21 — 「근로·퇴직·이연퇴직소득 등 과세제도 개선」 (2025년 조세개정안), 조세일보 (news)

- URL: <https://m.joseilbo.com/news/view.htm?newsid=549483>, 2025-07-31. Accessed:
  2026-09-03. Retrieved: **yes**. **News source**, used to date and explain the amendment
  whose enacted text is [R5].
- The 2025 tax bill reduced the 종신계약 withholding rate to 3% and extended the 이연퇴직소득
  reduction to 50% for payouts running beyond 20 years, applying to pensions received on or
  after **2026-01-01**.
- Rests on it: the dating of `pension_tax_rate_life` = 3.3% and the description of the change
  as recent rather than settled.

(krlib-pension_savings-r22)=

### R22 — 「연금저축 적립금 198조 돌파…」, 뉴스핌 (news report)

- URL: <https://www.newspim.com/news/view/20260618000323>, 2026-06-18. Accessed: 2026-09-03.
  Retrieved: **yes**. **News source**, reporting [R13]; used for figures the press-release
  body did not carry.
- 계약건수 1,079.6만건 (+11.1%); 납입액 13.5조원 (+18.1%); 신규 계약건수 144.3만건 (+51.9%);
  wrapper shares 보험 57.6%, 펀드 30.9%, 신탁 6.4%; by seller 보험회사 114.3조원 (57.7%),
  금융투자회사 55.4조원 (27.9%), 은행 19.5조원 (9.8%), 공제기관 9.0조원 (4.6%).
- Rests on it: the market-size and mix figures in `product-spec.md`, and the second strand of
  the lapse argument — the direction and speed of the move to funds.

(krlib-pension_savings-r24)=

### R24 — 「경험생명표」, 보험개발원 빅데이터 플랫폼 (data portal)

- URL: <https://bigin.kidi.or.kr:9443/boarddetail/nd00017_6041>. Accessed: 2026-09-03.
  Retrieved: **no** — `connect ECONNREFUSED 61.107.27.12:9443`. The host resolves but refuses
  connections on that port from this session.
- Recorded as a **fetch failure**, not hidden. It is the second of the two channels through
  which a Korean industry mortality table might have become public, and its failure — with
  [R17] and [REG-R34] — is what closes the question and makes `mort_table.csv` **[std]**.

---

## Cross-product references ([REG-R#])

These resolve against `references/regulatory-and-actuarial-references.md`, whose own R1–R62
numbering is frozen and is **not** this page's. Reprinted in short form so a reader of this
page alone can resolve every tag, with a note on what this product uses each for.

- **REG-R3** — 보험업법 제120조 (책임준비금 등의 적립). The statutory hook for the reserve;
  cited in the paragraph saying what this model does **not** compute.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관). 보험개발원's statutory office and the
  absence of any publication obligation — the cross-product form of [R16].
- **REG-R5** — 보험업법 제181조·제184조 (보험계리, 선임계리사). The 선임계리사 owns the basis
  and verifies the reserve; why `result_cf()` is an input to a valuation rather than one.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), the whole 고시. 제1-2조's definitions of
  저축성보험, 금리연동형보험 and 평균공시이율, and the nil hit count for 예정이율.
- **REG-R10** — 감독규정 제6-11조·제6-11조의4·제6-11조의5 (책임준비금, 보증준비금). The
  post-2023 reserve taxonomy, and the 보증준비금 inside which the 100.1% floor would be valued.
- **REG-R11** — 감독규정 제6-11조의6 (해약환급금준비금). The Korea-specific surrender-value
  reserve, measured off `cv_pp` — which on this product is the entire account value.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당). The dividend reserve and its
  distribution; the composite is 무배당 and declares zero.
- **REG-R13** — 감독규정 제7-1조·제7-2조·제7-2조의2 (K-ICS 지급여력). The economic-value
  solvency regime this product's cash flows feed.
- **REG-R14** — 감독규정 제7-17조~제7-19조 and 고시 제2022-53호 부칙. The commencement
  provisions that date both IFRS 17 and K-ICS to **2023-01-01**.
- **REG-R16** — 감독규정 제7-60조 (생명보험의 보험상품설계 등). 제2호 (a 저축성보험's survival
  benefits must **exceed** premiums paid — why 100.1% and not 100%), 제9호 (the death-benefit
  exemption for a premium term ending at 80 or below), 제10호 (a floor is compulsory).
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액). 제7-65조제1항's
  계약자적립액, **제2항's annualised-premium permission** — the licence the earlier annual grid
  ran under, and which the monthly grid no longer needs — and 제3항's 공시이율 construction.
- **REG-R19** — 감독규정 제7-66조 등 (해약환급금, 계약자적립액의 적립). 제1항제1호 is
  `check_cv_floor`'s identity; 제1항제2호 the seven-year 해약공제기간 cap; 제1항제3호 the
  reference to 별표 14; **제1항제4호 the monthly accrual of the account before 납입완료**,
  which is what the monthly grid follows directly.
- **REG-R20** — 감독규정 [별표 14] 표준해약공제액. The cross-product retrieval of the same
  schedule as [R14]; 주2, 주3, 주5 and 주6 are what `surr_chg_cap_pp` implements.
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조 (수수료, 공시, 신고). The commission ring
  around the cap, and acquisition cost amortised over seven years at **100% online**.
- **REG-R24** — 시행세칙 [별표 27] 공시기준이율 산출 기준. The index the 공시이율 is set off,
  with the external weight **α capped at 60%** — why a declared rate is not a market rate.
- **REG-R25** — 시행세칙 [별표 15] 표준약관. 제21조 (보험나이), 제17조 (청약철회), 제26조
  (납입최고), **제27조 (부활, 평균공시이율 + 1%)**, 제33조 (대출), 제37조 (소멸시효).
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금 산출기준). **Not
  retrieved.** Everything resting on the 대량해지 shock or on the guarantee-reserve basis is
  second-hand and carries [unverified].
- **REG-R27** — 제4차 보험개혁회의 보도자료 (계리가정·할인율). The supervisory 무·저해지 lapse
  guidance, which this product **deliberately does not use** — it is 순수보장성 calibration.
- **REG-R29** — 금융위원회, 2019 사업비·모집수수료 개편 보도자료. The 표준해약공제액 as a
  multiple of the monthly premium — **저축성보험 3배** — which ₩1,421,988.72 passes.
- **REG-R32** — 금융위원회, 예금보호한도 1억원 (2025-09-01). Dates the increase in the
  deposit-protection limit.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported. 평균수명 남 86.3 / 여 90.7, 65세
  기대여명 남 23.7 / 여 27.1 — the only public figures the **[std]** table is judged against.
- **REG-R34** — 보험개발원 public channels. **Negative evidence**: the visible listing carries
  no 경험생명표, 참조순보험요율 or 보험통계 item — so the qx table is not public.
- **REG-R36** — 보험연구원 CEO Report 03호. The K-ICS 대량해지 shock table, sourced there to
  the unretrieved 별표 22 [REG-R26], and the 해약환급금준비금 at ₩23.7tn / ₩32.2tn.
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」. 65세 기대여명 남 **19.5** / 여 23.7 —
  the population anchor against which the fitted annuitant table's 33.31 is reported.
- **REG-R39** — KOSIS 완전생명표 (single-year qx). **Not downloaded** in this session; recorded
  as a live task for any rebuild of the mortality file rather than as a closed gap.
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier disclosure. The series 2016–2026 with
  **2.50% for 2026**, and the finding that 예정이율 is not a supervisory parameter.
- **REG-R49** — 상법 제4편 보험, 제1장 통칙. 제638조의3's duty to deliver and explain the 약관,
  and 제662조's three-year 소멸시효.
- **REG-R51** — 금융소비자보호법 제46조 (청약의 철회). The 15-day / 30-day cooling-off right
  the 표준약관 implements; scoped out of the model, which begins where cover is in force.
- **REG-R52** — 예금자보호법 시행령 제18조. The **₩100,000,000** limit and its four buckets,
  the second being **연금저축계좌** claims — separate from the saver's other claims.
- **REG-R56** — 소득세법 제59조의3·제20조의3·제129조 and 시행령 제40조의2. The whole 연금저축
  tax package, cited beside [R1] [R2] [R5] [R6]; it carries the 지방소득세 [unverified] note.
- **REG-R58** — 소득세법 제16조제1항제9호 and 시행령 제25조 (저축성보험의 보험차익). The
  **non-qualified** 종신형 연금보험 route — a different product, cited at the scope boundary.
- **REG-R60** — 한국회계기준원, K-IFRS 제1117호 「보험계약」. The Korean adoption of IFRS 17,
  **mandatory** for Korean insurers rather than voluntary.
- **REG-R61** — 보험개발원, 「장기손해보험 참조순보험요율」 공시. Retrieved: yes. Cited on this
  page and in `product-spec.md` for one purpose only, and it is a **boundary**: the bureau
  does publish reference **morbidity** rates — the 「기타피부암 및 갑상선암 이외의 암 발생률」
  and 질병입원율 grids by age and sex — on a numeric display of its own site, which is why
  [REG-R34]'s negative finding is about the 보도자료 channel and the **life** side and must
  not be read as "보험개발원 publishes nothing". No life-side 참조순보험요율 and no mortality
  table appears there, so nothing in this product's mortality basis is sourced from it and
  `mort_table.csv` stays **[std]**.
- **REG-R62** — 손해보험협회 공시실 (kpub.knia.or.kr). Cited on this page only, at the two
  omitted research sources in the orientation; no fact in the three documents rests on it.

---

## Provenance note

Every entry above traces to `_research/pension-savings.md`, the citation ground truth for
this product: the fetch record, the fact extraction, the carrier-by-carrier variation table
and the full gaps register live there, and this page is the reader-facing digest of its
source lists. **Its numbering is frozen and never renumbered** — S1–S21 and R1–R25 there, of
which S1–S16, S19, S20 and R1–R14, R16–R22, R24 are cited by this product's documents and
reprinted here, the six unused numbers being accounted for in the orientation above.

The gaps these documents inherit, in order of how much they matter: **no Korean industry
mortality table** at any level of detail [R17] [R24] [REG-R34] — and the boundary matters,
because the bureau *does* publish a 장기손해보험 참조순보험요율 display [REG-R61], but it
carries **morbidity** and no life-side rate, so nothing on this page is reachable through
it — so the annuitant basis is a **[std]** construction shipped with its recipe; **no lapse
statistic by policy year** from any public source [S13] [S19] [R13], so the lapse vector is
argued rather than fitted; **no
operative text for 소득세법 시행령 제187조의2** [R7], so the 종신계약 withholding status of a
guaranteed life annuity is [unverified]; **no published 보험계약대출이율** [S1] [S2] [S4]
[S5], so that module is off in the base run; and **no cash expense basis** from any carrier,
the published 사업비 figures being contractual loadings rather than the insurer's own costs
[S1] [S7]. Each is stated at the point of use, and each is why a parameter carries **[std]**
rather than a citation.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-pension_savings-r1
[R13]: #krlib-pension_savings-r13
[R14]: #krlib-pension_savings-r14
[R16]: #krlib-pension_savings-r16
[R17]: #krlib-pension_savings-r17
[R18]: #krlib-pension_savings-r18
[R19]: #krlib-pension_savings-r19
[R2]: #krlib-pension_savings-r2
[R20]: #krlib-pension_savings-r20
[R24]: #krlib-pension_savings-r24
[R5]: #krlib-pension_savings-r5
[R6]: #krlib-pension_savings-r6
[R7]: #krlib-pension_savings-r7
[R8]: #krlib-pension_savings-r8
[REG-R20]: #krlib-reg-r20
[REG-R26]: #krlib-reg-r26
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R48]: #krlib-reg-r48
[REG-R56]: #krlib-reg-r56
[REG-R61]: #krlib-reg-r61
[REG-R62]: #krlib-reg-r62
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
