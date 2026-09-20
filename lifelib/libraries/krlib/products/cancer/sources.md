# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/cancer.md`, the citation
ground truth for this product, and are **frozen — never renumber**. Numbering is per
product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md` runs
its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read
across.** The sharpest instance in this product is [R5], which is the 보험개발원
참조순보험요율 display, against [REG-R5], which is 보험업법 **제181조·제184조** (보험계리);
the second is [R13], the 표준약관, against [REG-R13], which is the K-ICS 지급여력 articles of
the 감독규정. Access date for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 보험약관 (*boheom yakgwan*, policy conditions), a
  carrier product page, or a carrier consumer-education page. These are what make a
  contractual mechanic *sourced* rather than assumed, and on this product they carry the
  whole of the benefit definition: the 90일 면책기간 and the 유사암 carve-out from it, the
  감액기간, the four-tier ladder and its ratios, the 최초 1회한 form, the waiver's exclusions,
  the 180-day inpatient cap, the 5 : 1 surgery split and the 미지급형 surrender basis all
  rest on [S1]–[S8] and on nothing else.
- **[R#]** — a regulatory, statutory, statistical or actuarial reference that only this
  product needs. Two of them are load-bearing for the *numbers* rather than the words:
  **[R1]**, the national cancer registry annex, which every calibration target in
  `survival_table.csv` and every anchor in `tier_share_table.csv` traces to, and **[R5]**,
  the 보험개발원 참조순보험요율 display, which `incidence_table.csv` reproduces.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Every tag used in the three documents has an entry here, and every entry here is used.**
No source was added at drafting. Two research-file entries were **dropped** because neither
document cites them, so the numbering has a gap and the gap is deliberate: **R9**
(통계청 「2024년 사망원인통계 결과」) and **R14** (보험개발원 제10회 경험생명표). They are
named here **without their brackets deliberately**: a bare `[R9]` in this file has no local
anchor to resolve against, so the citation tooling would silently point it at the
cross-product [REG-R9], which is a different document altogether. R9's
headline figures — 악성신생물 24.8% of all Korean deaths at 174.3 per 100,000 — were
retrieved only in part and nothing in the model rests on them, because this product's
mortality basis is an all-cause table and its cancer decrement is an incidence rate rather
than a mortality one. R14 was **not retrieved at all** and the table it names is not
published in full in any case, so every statement about the 경험생명표 in these documents
cites the cross-product [REG-R33] and [REG-R34], and the shipped `mort_table.csv` is
calibrated to [REG-R38] instead. Their numbers are left vacant rather than reused: the
research file is never renumbered.

**What is sourced quantitatively, and it is more than in any other morbidity product in this
library.** The 「기타피부암 및 갑상선암 이외의 암 발생률」 grid of [R5] is a **published,
dated, insured-definition cancer incidence basis**, and `incidence_table.csv` reproduces it
verbatim for ages 0–80 with only the two rows per sex above 80 marked [std]. The five-year
relative survivals that calibrate `survival_table.csv` and the crude site rates that anchor
`tier_share_table.csv` come from [R1]. The tier ratios in `tier_table.csv` are read off
[S3 별표 1]. Everything else — the tier decomposition itself, the grading of the excess
hazard across select years, every row of `care_table.csv`, the lapse level, the expense and
commission scales, the notional 보험가입금액 and the premium — is **[std]**, and `model.md`
lists each with its rationale and whatever observed range the documents bound.

Company and branded product names appear in this file and in `_research/cancer.md` and
**nowhere else** in the library: in `product-spec.md`, `technical-notes.md`, `model.md` and
the model docstrings a carrier is referred to by its tag alone, so a reader can always
resolve who said what — here — and never has to.

---

## Primary product sources

Eleven documents from seven carriers. **Seven** are **보험약관** — the contractual
instrument itself, five of them over 150 pages and two over 500 — drawn deliberately from
**both sides of the 제3보험 licence** so that the composite can show that a 손해보험 writer
and a 생명보험 writer sell the identical cover [S1] [S2] against [S3]–[S7]. An eighth
non-life document is a **상품 페이지** rather than a 약관, and carries the session's only
published premium and surrender-value illustration [S8]. Two are consumer-education pages
rather than contractual documents [S9] [S10], and one could not be fetched at all [S11].

**Retrieval method, common to the set.** Plain `curl` is blocked for most Korean hosts in
this session, so everything below was fetched with a summarising fetcher; where that fetcher
returned a Korean PDF as undecodable binary it still saved the file, and the binary was
extracted locally with `pypdf` and read directly. That is how the long 약관 were obtained.
**One extraction artefact affects every 약관 below and constrains how they may be quoted:**
Korean policy PDFs set article headings in a doubled bold face, so `pypdf` extracts them as
`제제 55조조 ((암암 ,, ...))` rather than `제5조(암, ...)`, and body text frequently arrives
with a space between every syllable. Quotations in these documents are given in normalised
form — doubling collapsed, inter-syllable spaces removed — and nothing else has been altered;
article numbers are as printed.

(krlib-cancer-s1)=

### S1 — 삼성화재, 「무배당 삼성화재 건강보험 태평삼대(1811.6) 15년만기형 보험약관」 (policy conditions, complete)

- Publisher: 삼성화재해상보험주식회사 (Samsung Fire & Marine Insurance) — a **non-life**
  insurer writing this cover as 제3보험 under the deeming provision of 보험업법 제4조제3항
  [R8] [REG-R1]
- Document: 보험약관, file `ZPB205040_0_20180805_file1.pdf`, **382 pp.**, 2018 edition, with
  a front 상품요약 / 유의사항 section
- URL: `https://www.samsungfire.com/publication/pdf/ZPB205040_0_20180805_file1.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (full PDF downloaded; the text layer extracted
  cleanly at roughly 534,000 characters, including the 보통약관 body and the 특별약관 for
  every rider)
- **The single most complete retrieved statement of the 면책기간 / 감액지급 matrix**, benefit
  by benefit across 24 named covers — which is the evidence that the two timing devices are
  *per benefit* and not per contract, and therefore that the model needs a `wait_months`
  column on `tier_table.csv` rather than a scalar. What rests on it: 「유사암의 보장개시일은
  계약일임」 and the 면책기간 table marking 유사암 진단비 with a cross, which is
  `cover_similar(t) = 1` from `t = 0`; 제5조 (암, 기타피부암, 갑상선암 및 대장점막내암의 정의
  및 진단확정) and 제6조 (제자리암 및 경계성종양) verbatim, which is the five-member 유사암
  set; the 특정소액암 / 5대 주요암 / 10대 주요암 tiering with its KCD site lists; **제28조
  (계약의 무효)** with the pre-waiting-period diagnosis rule, which is `void_prob()` and the
  `void_adjust` switch; 재진단암 on a 2-year cycle, specified and not modelled; **암 직접치료
  입원일당 at 180 days per stay**, which is `hosp_day_cap_days = 180` and what
  `check_hosp_cap()` asserts against, with 유사암 paid at 20% of the daily amount — the basis
  for saying the model's zero 유사암 care benefit understates; 항암방사선·약물 치료비 with
  기타피부암·갑상선암 at 20%; **제9조 (보험료 납입면제)**, which is `waiver_trigger`; a
  15-year term with 재가입; and 최저보증이율 0.5% on the 적립부분, the lower observed anchor
  for `prem_int_rate`.

(krlib-cancer-s2)=

### S2 — 삼성화재 다이렉트, 「무배당 삼성화재 다이렉트 건강보험 2601.16 보험약관」 (policy conditions, complete)

- Publisher: 삼성화재해상보험주식회사 (direct channel)
- Document: 보험약관, file `health_insu.pdf`, **511 pp.**, 2601.16 edition (2026)
- URL: `https://direct.samsungfire.com/CR_MyAnycarWeb/mall/pdf/health_insu.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (511 pp.; roughly 931,000 characters extracted;
  the 유의사항 tables and the cancer 특별약관 read in full)
- **The current-market comparator to [S1], eight years later, and the single most valuable
  retrieved document for showing what has changed.** The 암 진단비(유사암 제외) rider now
  carries **no 감액 at all** — 100% from the day after the 90-day wait — while 유사암 진단비
  keeps a 1-year 50% reduction; that is the shape `reduction_months = 0` on model point 9
  prices. Three further carve-outs rest on it and two of them leave the product: the
  면책기간 does **not** apply to a life aged under 보험나이 15 (보장개시일 = 보험계약일),
  which is the delta `Child_KR_S` states against this chassis; a **갱신계약 carries neither
  면책기간 nor 감액**, which is model point 3; and a 다빈치로봇 수술비 with a **180-day /
  1-year two-step** reduction (25% then 50%) appears, a shape absent from every other
  retrieved contract and specified but not modelled. It is also the source, with [S8], for
  the 요양병원 limb being carried as a **separate 90-day rider** rather than inside the
  inpatient benefit.

(krlib-cancer-s3)=

### S3 — 한화생명, 「한화생명 e암보험(비갱신형) 무배당 약관」 (policy conditions, complete)

- Publisher: 한화생명보험주식회사 (Hanwha Life Insurance) — a **life** insurer
- Document: 보험약관, 166 pp., edition dated **2025-01-06**; 표준체형 / 비흡연체형 variants;
  주계약 + 제도성특약 + 별표
- URL: `https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e암보험(비갱신형)%20무배당_약관_20250106.pdf`
  (served with the query string `?docUrl=dynamic/direct/product/cms_K86hzsQGOOnVEFlC_1736169011449.pdf`)
- Accessed: 2026-09-03, Retrieved: **yes** (166 pp.; text extracted cleanly and read article
  by article)
- **The cleanest retrieved stand-alone cancer main contract, the anchor document of the
  composite, and the source of every shipped benefit ratio.** 별표 1 보험금 지급기준표 states
  every benefit as an **amount at 보험가입금액 1,000만원**, so the four tier ratios are read
  directly rather than inferred — which is the whole of `tier_table.csv`'s `benefit_ratio`
  column: 암진단자금 100%, 특정 고액치료비관련 암진단자금 a further 100%, 특정 소액암
  진단자금 60%, 소액질병 진단자금 20%. What else rests on it: 제2조 정의 with **암보장개시일
  = the 91st day counting the 보험계약일 as day 1**, which is `wait_months = 3` on the
  monthly grid; 제3조–제11조 defining 암 / 특정 고액치료비관련암 / 특정 소액암 / 중증
  갑상선암 / 기타피부암 / 갑상선암 / 대장점막내암 / 제자리암 / 경계성종양 with their KCD
  numbers; **제12조**, the contract-vs-diagnosis KCD-vintage rule, which cuts both ways;
  **제14조제1항**, which excludes 특정 소액암 from the premium waiver **by name** and is the
  reason `pols_minor` is a separate state that goes on paying; 제30조 보험나이 with a worked
  example, which is why `model.md` has to say the model runs on 만나이 instead; **제41조
  해약환급금 including the 해약환급금 미지급형 (납입기간중 0%, 납입기간후 50%)**, which is
  `cv_floor_ratio = 0.0` and `cv_post_pay_ratio = 0.5`; a **2-year** 감액기간 at 50%; 별표 5
  the full 악성 신생물 분류표 (24 rows of KCD codes); and 별표 10 특정 고액치료비관련암. It
  also carries a formal **비흡연체형** chapter with its own 보험요율 whose differential is
  not published, which is why the model has no smoker split.

(krlib-cancer-s4)=

### S4 — 한화생명, 「한화생명 e시그니처암보험 무배당 약관」 (policy conditions, complete)

- Publisher: 한화생명보험주식회사
- Document: 보험약관, **597 pp.**, edition dated **2024-04-01** (internal code 2063-A01_A02)
  — a modular product: one 공통사항 chapter plus **23 separate 주계약 약관**, each its own
  module, sold in any combination
- URL: `https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e시그니처암보험%20무배당_2063-A01_A02_약관_20240401_.pdf.pdf.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (597 pp.; roughly 887,000 characters extracted;
  the diagnosis, surgery, inpatient and chemotherapy modules read in full)
- **The 갱신형 chassis, and the modular architecture the Korean market has converged on** —
  which is why `Cancer_KR_S` carries four independently switchable benefit modules rather
  than one fixed benefit menu, and why model points 7 and 8 are configurations of one model
  rather than different models. 제2-11조의6 (계약의 갱신) verbatim: automatic renewal unless
  the policyholder objects 15 days before expiry, final renewal ending at the **100세
  계약해당일**, premium recalculated at the attained age on the rate basis in force at
  renewal, 보험가입금액 unchanged, and a module on which a benefit has been paid **does not
  renew**. On a 갱신계약 the 암보장개시일 is the **갱신일** — no fresh 90-day wait — and the
  감액 does not apply, which is model point 3's whole content. Its module schedules give
  항암약물치료자금 / 항암방사선치료자금 in two tiers, 상급종합병원 암입원급여금 at 1일 초과
  1일당 with a **120-day per-stay cap**, and **암수술자금 split 관혈 / 비관혈 at 5 : 1**,
  which is `surg_open_base` against `surg_closed_base`; 수술 is defined by a 수술분류표 with
  the standard exclusions.

(krlib-cancer-s5)=

### S5 — 한화생명, 「한화생명 e암치료비보험 무배당 약관」 (policy conditions, complete)

- Publisher: 한화생명보험주식회사
- Document: 보험약관, 216 pp., edition dated **2025-07-21** — modular again, but **비갱신형**
  modules only
- URL: `https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e암치료비보험%20무배당_약관_20250721.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (216 pp.; text extracted; the 감액지급 table and
  the 다빈치로봇 module read)
- **The treatment-cost (치료비) chassis — no diagnosis lump sum at all**, only treatment-event
  benefits (다빈치로봇 수술자금, 암수술자금, 암주요치료자금, 항암약물·방사선 치료자금). That
  is model point 8, `diag_module = 0`, and it is why the diagnosis limb is a switch rather
  than a fixture. It carries a uniform **2-year 50% 감액** with a **180-day 25%** first step
  on the robot-surgery module, and — the point that matters most to the model — it **confirms
  that on treatment benefits the 감액 clock runs from the 보험계약일 to the treatment date,
  not to the 진단확정일**. That is the divergence `model.md` records and does not implement:
  the model applies the reduction to the four diagnosis lines **only**, and never to the
  inpatient, surgery or treatment limbs. It therefore gives the contract's own answer
  whenever the treatment date falls outside the 감액기간 — which includes every case in
  which the diagnosis itself does — and **overstates** the care limbs of a treatment that
  falls inside it.

(krlib-cancer-s6)=

### S6 — 라이나생명, 「무배당 첫날부터라이나암보험(갱신형) 약관」 (policy conditions, complete)

- Publisher: 라이나생명보험주식회사 (Chubb Life / LINA Life Insurance Korea)
- Document: 보험약관, 48 pp., file `B00370002_1_P.pdf` on the carrier's 공시 directory, with a
  front 시각화된 약관 요약
- URL: `https://www.lina.co.kr/cms/upload/upload/docs/disclosure/B00370002_1_P.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (48 pp.; text extracted and read)
- **The one retrieved contract with no waiting period at all** — the product name means "from
  the first day". 제26조 defines 보장개시일 as the day the first premium is received and adds
  「또한, 보장개시일을 계약일로 봅니다」; the 요약 table lists a 감액지급 block and **no
  면책기간 block**. It is the evidence that the 90 days is a near-universal market convention
  rather than a legal requirement, which is why `wait_months` is a model point column. It
  keeps a 1-year 50% 감액 on every benefit and pays 유방암/전립선암 at **20%** and
  갑상선암·기타피부암·제자리암·경계성종양 at **10%** of 보험가입금액 — **the lower bound of
  the observed 유사암 range** that `model.md`'s standardization table records.

(krlib-cancer-s7)=

### S7 — 라이나생명, 「무배당 라이나 퍼펙트케어암보험(갱신형) 약관」 (policy conditions, complete)

- Publisher: 라이나생명보험주식회사
- Document: 보험약관, 35 pp., file `B00179014_0_P.pdf`, with a 시각화된 약관 요약
- URL: `https://www.lina.co.kr/cms/upload/upload/docs/disclosure/B00179014_0_P.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (35 pp.; text extracted and read)
- **The same carrier's conventional shape, and therefore a controlled comparison against
  [S6]** — one variable changed, the waiting period, with the tier ratios and the carrier
  held fixed. It carries a 90-day 면책 on 암 and on 유방암/전립선암 but **none on the four
  유사암**, which is the second independent confirmation of the product's two start dates; a
  **2-year** 50% 감액 on everything; identical 20% / 10% tier ratios; renewal to a 100세 만기
  once the insured passes 가입나이 85; and 「갱신계약은 면책기간이 없습니다」 and 「갱신계약은
  감액지급이 없습니다」 stated as headline summary lines.

(krlib-cancer-s8)=

### S8 — AIG손해보험, 「(무)AIG 소문난NEW암보험2106」 상품 페이지 (product page with illustrations)

- Publisher: AIG손해보험주식회사 (AIG General Insurance Korea) — a **non-life** insurer
- Document: 상품 페이지 with 가입안내, 상품의 특이사항 and a 해약환급금(률) 예시 table
- URL: `https://www.aig.co.kr/wp/dpwpm400c.jsp?prodAlias=cancer01&menuId=MS1050&prodCd=L0216`
- Accessed: 2026-09-03, Retrieved: **yes, in part** (HTML retrieved and converted; **the
  보장내용 and 가입예시 tabs are rendered client-side and did not come through**, so the
  benefit schedule behind the illustration was not seen)
- **The only retrieved published premium and surrender-value illustration in this session**,
  at 남자 40세 / 월납 / 10년납 10년만기 / 순수보장형 for three plans. It carries the
  계약자적립액 적용이율 of **연복리 1.5%**, which is the lower observed anchor for
  `prem_int_rate = 0.025`; a **70%** 유사암 payout ratio, the highest observed and a pre-2022
  design, which is model point 10's `similar_ratio = 0.70`; the full 재진단암 definition
  (새로운 원발암 / 전이암 / 재발암 / 잔여암) on a 2-year cycle, specified and not modelled;
  the surrender value returning to nil at maturity, which is why `claims_maturity` is a column
  of zeros; and a **2종 만기환급형** variant returning 5% of 보험가입금액 at maturity, which
  is expressly out of scope. Because the tabs did not render, **the illustration's premium
  figures carry no stated 보험가입금액** — they are price points without a benefit
  denominator, which is why every premium in `model_point_table.csv` is [std].

(krlib-cancer-s9)=

### S9 — 교보생명, 「암의 종류와 보장 범위 (유사암 vs 소액암 vs 고액암)」 (consumer-education Q&A)

- Publisher: 교보생명보험주식회사 (Kyobo Life Insurance)
- Document: 금융정보 Q&A page, dated **2022-06-23**
- URL: `https://www.kyobo.com/dgt/web/customer/finance-information/finance-qna/8992`
- Accessed: 2026-09-03, Retrieved: **yes** (via the summarising fetcher; the page's
  substantive text returned, the surrounding navigation did not)
- A carrier's own **four-tier taxonomy** stated in one place — 유사암 (기타피부암, 갑상선암,
  제자리암, 경계성종양), 소액암 (자궁암, 유방암, 방광암, 전립선암), 고액암 (뼈암, 뇌암,
  혈액암, 식도암, 췌장암, 간암, 담낭암, 담도암, 기관지암, 폐암) and 일반암 — with the 10~20%
  payout band on the two low tiers and a stated 고액암 treatment cost averaging over
  ₩50,000,000. **This is consumer education, not a contractual document**, and it is used in
  `product-spec.md` for the taxonomy paragraph alone; no model parameter rests on it.

(krlib-cancer-s10)=

### S10 — KB손해보험 인사이트, 「암보험 가입할 때 알아야 할 몇 가지」 (carrier content article)

- Publisher: KB손해보험주식회사 (KB Insurance), corporate content site
- Document: 보험 상식 article, dated **2025-11-06**
- URL: `https://insight.kbinsure.co.kr/info_cancer/`
- Accessed: 2026-09-03, Retrieved: **yes**
- The most recent retrieved **carrier statement of where the market now is**: 유사암 진단비
  now written up to **₩30,000,000 (3천만원)**; the 감액기간 on 일반암 being shortened or
  removed, which corroborates [S2]; 3대 / 5대 / 10대 고액암 as alternative high-tier
  definitions, which is why the 고액암 tier is a *subset* parameter rather than a fixed site
  list; 재진단암 paid 「매 1~2년마다」; and the flat statement that the diagnosis date is the
  **조직검사 결과 보고일** and not the date the certificate is issued — which is what decides
  whether a claim falls inside the 면책기간 or the 감액기간. Again a content article, not a
  contractual document, and used for market context.

(krlib-cancer-s11)=

### S11 — 삼성생명 다이렉트, 암보험 상품 페이지 (product page) — **not retrieved**

- Publisher: 삼성생명보험주식회사 (Samsung Life Insurance)
- Document: 상품 페이지 (direct channel)
- URL: `https://direct.samsunglife.com/ncancer.eds`
- Accessed: 2026-09-03, Retrieved: **NO** — HTTP 200, but the body is a 6,761-byte JavaScript
  shell containing 16 characters of text. **Nothing was taken from it.**
- It is numbered rather than dropped because the absence is itself a fact the documents cite:
  **Korea's largest life insurer is not represented in this product's evidence base by any
  document at all.** Every statement in `product-spec.md` about that carrier's cancer
  offering is therefore second-hand or absent, and the composite's claim to represent the
  market is bounded by it.

---

## Regulatory and actuarial references

Twelve entries, of which **nine were fully retrieved, two in part and one not at all**. Two
of the twelve carry the whole of this product's quantitative basis — [R1] and [R5] — and the
rest are the legal and historical frame. One is a **news article standing in for an
instrument that could not be found** [R12], and it is labelled as such at every use.

(krlib-cancer-r1)=

### R1 — 중앙암등록본부 / 보건복지부, 「2023년 국가암등록통계 참고자료」 (national registry annex)

- Publisher: 보건복지부 · 중앙암등록본부 (국립암센터), released **2026-01-20**
- Document: 2023년 국가암등록통계 참고자료, **41 pp.**, PDF
- URL: `https://www.cancer.go.kr/download.do?uuid=cfcd35c3-391f-4060-9688-641db3d86cbd.pdf`
  (index: `https://www.cancer.go.kr/lay1/bbs/S1T674C816/B/61/view.do?article_seq=85579`)
- Accessed: 2026-09-03, Retrieved: **yes** (41 pp. downloaded and fully text-extracted; every
  figure below was read off the extracted text)
- **The public statistical basis behind everything in this model that is not the incidence
  grid.** It carries 발생자수 / 조발생률 / 연령표준화발생률 by sex for 1999–2023; the 2023
  site ranking with 분율; 평생 암발생·사망 위험도 by site and sex; 암발생 현황 by 10-year age
  band × sex; the 요약병기 (localized / regional / distant) distribution 2005–2023; **5년
  상대생존율 by period and by 요약병기**; 암유병자수 by age band and **by elapsed time since
  diagnosis**; and a 별첨 giving **상피내암 발생률** 1999–2023 by sex and site. What rests on
  it: the calibration targets of `survival_table.csv` — 5년 상대생존율 excluding thyroid of
  남 65.9% / 여 74.0%, the 특정소액암 sites' own 75.6 / 94.7 / 96.9, and 갑상선 at **100.2%**
  with a lifetime 갑상선 mortality risk of **0.1%**, which is why the 유사암 tier appears in
  no row of that file; the **62.1%** of prevalent patients more than five years out, which is
  why the excess hazard is graded rather than flat; the all-ages crude site rates that anchor
  `tier_share_table.csv` (대장 63.8, 유방 58.4, 전립선 44.3, 갑상선 69.3, 상피내암 74.7
  against an excluding-thyroid base of 495.0); the crude-band deceleration above 80 that the
  [std] extrapolation rests on; the **161%** rise in crude incidence since 1999 that the
  absent trend loading is measured against; the **44.6%** lifetime male cancer risk the
  expected-payment counts are sanity-checked against; and the definition of relative survival
  itself — 「관찰생존율을 일반인구의 기대생존율로 나누어 구한 값」 — which is why the model
  adds a hazard rather than multiplying a survivorship.

(krlib-cancer-r2)=

### R2 — 국가암정보센터, 「통계로 보는 암 — 암 발생률」 및 「암종별 발생 현황」 (public statistics pages)

- Publisher: 국립암센터 국가암정보센터 (National Cancer Information Center)
- Document: public statistics pages, 최종수정일 **2026-01-27**
- URLs: `https://www.cancer.go.kr/lay1/S1T639C640/contents.do` (암 발생률) and
  `https://www.cancer.go.kr/lay1/S1T639C641/contents.do` (암종별 발생 현황)
- Accessed: 2026-09-03, Retrieved: **yes** (HTML retrieved and converted; the data tables came
  through, the charts did not)
- Corroborates [R1]'s headline 2023 figures independently — 288,613 발생자수, 조발생률 564.3,
  연령표준화발생률 522.9 — and carries the year-on-year commentary. **Used only as a
  cross-check: no figure in any of the three documents rests on it alone**, which is why it is
  cited once, in `product-spec.md`, beside [R1].

(krlib-cancer-r3)=

### R3 — 보험연구원, 「암보험 관련 주요 분쟁사례 연구」 (연구보고서 2019-4) (research monograph)

- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI); 저자 백영화·박정희,
  **2019년 10월**
- Document: 연구보고서 2019-4, **169 pp.** PDF
- URL: `https://www.kiri.or.kr/report/downloadFile.do?docId=44` (chapter II separately at
  `https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2019-04_2.pdf`)
- Accessed: 2026-09-03, Retrieved: **yes** (169 pp. downloaded and text-extracted; chapters
  I, II, III.5, III.6 and III.7 read in full)
- **The load-bearing legal and historical reference for this product**, and the only
  institutional source in the set. It gives the product's history with dates; the KCD
  행동양식 분류번호 mechanics (/0, /1, /2, /3, /6) and which D- and C-code ranges they map to,
  which is what makes the 유사암 boundary a *classification* boundary rather than a clinical
  one; the standard 약관 wording for 암의 정의, 진단확정, 암보장개시일 and 감액; the FSS
  금융분쟁조정위원회 decisions and the court judgments on 갑상선암 림프절 전이, on KCD
  reclassification and on 요양병원 입원비; the **2011-04-01** supervisory change on 이차성 암
  that put C77–C80 on the 원발부위 basis the shipped incidence grid already embodies; the
  statement of why the benefit is an income-and-incidentals benefit rather than a medical
  one; the 보험기간 「통상 80세 이하」 → 「100세 혹은 사망 시(종신)까지」 移動 that sets the
  composite's horizon; the **2,125 암입원비 complaints of 2018** behind the excluded 요양병원
  limb; and the finding, cited wherever a persistency figure would otherwise be asserted,
  that **no public Korean lapse or persistency figure for 암보험 exists**.

(krlib-cancer-r4)=

### R4 — 보험연구원, 「암보험 상품의 현황과 발전방향」 (김석영) (research note)

- Publisher: 보험연구원; 저자 김석영 연구위원
- Document: KIRI 리포트 / 고령화 리뷰 note, **14 pp.** PDF
- URL: `https://www.kiri.or.kr/community/boardDownloadFile.do?bid=689&seq=2`
- Accessed: 2026-09-03, Retrieved: **yes** (fetched after plain `curl` was reset by the host;
  the returned PDF was saved locally and text-extracted in full)
- **The actuarial history of the product, and the only retrieved source that says how the
  risk basis was built.** It carries a 암보험 상품의 변천 table mapping the 경험생명표
  generations (2회 1992.8–1996.12, 3회 1997.1–2002.12, 4회 2003.1–2005.12, 5회 2006.1–) to the
  benefit menu and the risk-rate source of each era — 일본통계 → 국내통계 → 경험통계 — the
  2010 incidence and survival tables, and the four risk factors the institute identified.
  Two statements are load-bearing in the model: that Korean **예정위험률 carry no trend
  loading at all** — 「현재도 예정위험률 산출 시 미래의 추세를 반영하지 않고 있음」 — which is
  half of why `inc_be_factor` is left at 1.0; and that the **61–75 age band carries
  수준리스크 from an absence of experience**, which is why the composite's issue-age ceiling
  is 65 rather than the 75 that 간편심사 products reach.

(krlib-cancer-r5)=

### R5 — 보험개발원, 「장기손해보험 참조순보험요율 예시」 (statutory rate bureau, public display)

- Publisher: 보험개발원 (Korea Insurance Development Institute, KIDI), the statutory
  보험요율 산출기관 of 보험업법 제176조 [REG-R4]
- Document: 공시 page under 알림광장 → 참조 순보험요율 → 장기손해보험; the rates on display are
  those **적용시점 2024년 4월 1일 이후**
- URL: `https://www.kidi.or.kr/user/nd13261.do`
- Accessed: 2026-09-03, Retrieved: **yes** (the page renders as HTML and the rate tables came
  through as text)
- **The single most important actuarial source in this product, and the reason `krlib` can
  ship a sourced rather than an invented cancer decrement.** It publishes a
  「기타피부암 및 갑상선암 이외의 암 발생률」 table **by age (0 / 10 / 20 / … / 80) and sex**
  — a published, dated cancer-incidence basis matched to the **insured** definition of
  cancer, invasive disease excluding C44 and C73 on the 원발부위 basis, which is exactly the
  decrement a Korean 일반암 진단비 model needs and exactly the 유사암 boundary the 약관 draw.
  `incidence_table.csv` reproduces it verbatim for ages 0–80. The same page publishes
  질병사망률 and **질병입원율 (1일이상 180일한도)** on the same grid; the latter is cited in
  `care_table.csv`'s provenance as the *only* published Korean utilisation series and as
  evidence of what it is **not** — a rate for all disease, not for cancer. Read it for what
  it is: a **참조순보험요율 is a net premium rate**, with a safety loading inside it, not a
  최적기초율, which is why adjusting it to a best-estimate basis remains a [std] step.
  Cited jointly with [REG-R61], which is the same display entered in the cross-product
  library.

(krlib-cancer-r6)=

### R6 — 금융감독원, 「금융꿀팁 200선 — 암보험 가입자가 꼭 알아야 할 필수정보: 암진단비, 암입원비」

- Publisher: 금융감독원 (Financial Supervisory Service), 보도자료 **2017-11-03**
- Document: consumer-guidance press release
- URL retrieved: `https://www.samili.com/samilinews/ContentSer.asp?idx_no=26063` (삼일인포마인
  reproduction). **The FSS's own copy was not retrieved.**
- Accessed: 2026-09-03, Retrieved: **in part** (the reproduction's substantive text returned;
  the original release's figures and diagrams were not seen)
- **The supervisor's own statement of the two timing devices**, which is what makes them
  market-wide facts rather than seven carriers' coincidence: 「암에 대한 책임개시일은
  계약일로부터 그 날을 포함하여 90일이 지난날의 다음날부터」, the exception for 갱신계약 and
  어린이암보험, the 「통상 보험계약일 이후 1~2년 이내에 암 진단확정시에는 암보험 가입금액의
  50%」 reduction, and a 유방암 90-day 10% variant. [R3] quotes the same release for its
  의학적 암의 진단 과정 diagram. Because the original was not retrieved, the wording above is
  quoted from a reproduction and is flagged where a verbatim quotation matters.

(krlib-cancer-r7)=

### R7 — 상법 제4편 「보험」 (Commercial Act, Part IV Insurance) (statute, transcription)

- Publisher: 대한민국 국회 / 법제처; text retrieved from 위키문헌 (Wikisource) transcription
- URL: `https://ko.wikisource.org/wiki/대한민국_상법`
- Accessed: 2026-09-03, Retrieved: **yes** (full text of Part IV extracted; individual
  articles read verbatim). **Caveat: this is a transcription, not 법제처's own copy** —
  `law.go.kr` was unreachable from this session. Article numbering and amendment annotations
  match the official text as far as could be checked, and the cross-product [REG-R49] and
  [REG-R50] carry the same Part from 국가법령정보센터, which is where the load-bearing
  statements cite.
- The contract-law furniture the 약관 rest on: 제638조의3 (약관 교부·설명 의무, three-month
  cancellation), **제644조 (보험사고의 객관적 확정의 효과)** — the statutory basis of the
  pre-waiting-period **무효** rule, and therefore of `void_prob()` being a de-recognition
  rather than a decrement — 제651조 (고지의무위반, 1개월 / 3년), 제656조 (보험료의 지급과
  보험자의 책임개시), 제662조 (소멸시효, 3년 on benefit claims), 제663조 (불이익변경금지) and
  **제739조의2 / 제739조의3 (질병보험자의 책임 / 준용규정, both 신설 2014-03-11)**, which are
  the whole of the private-law recognition of the disease-insurance contract that 암보험 is.

(krlib-cancer-r8)=

### R8 — 보험업법 제4조 (보험업의 허가) (statute, CaseNote mirror)

- Publisher: 대한민국 국회 / 법제처; text retrieved from CaseNote
- Document: 보험업법 [시행 2021. 6. 9.] [법률 제17636호, 2020. 12. 8., 일부개정]
- URL: `https://casenote.kr/법령/보험업법/제4조`
- Accessed: 2026-09-03, Retrieved: **yes** (article text returned verbatim with the amendment
  history). A mirror, not 법제처's own copy; the cross-product [REG-R1] carries the same
  article from 국가법령정보센터 at a **later** version, [시행 2025. 1. 31.], and the
  load-bearing taxonomy sentence cites that.
- The statutory definition of **제3보험업** and its 보험종목 — 가. 상해보험, 나. 질병보험,
  다. 간병보험 (제4조제1항제3호) — and **제4조제3항**, under which a licence for the whole of
  생명보험업, or of 손해보험업 excluding 보증보험 and 재보험, is deemed to carry the 제3보험
  licence. That deeming provision is why a life insurer [S3] and a non-life insurer [S1] can
  write the identical cancer contract, which is the composite's structural premise.

(krlib-cancer-r10)=

### R10 — 국가데이터처(통계청), 「제8차 한국표준질병·사인분류(KCD-8) 개정·고시」 (press release)

- Publisher: 통계청 (now 국가데이터처), 보도자료 **2020-07-01**
- URL: `https://mods.go.kr/board.es?mid=a10301010000&bid=246&act=view&list_no=383272`
- Accessed: 2026-09-03, Retrieved: **in part** (the release text returned; **the 고시 number
  itself and the code counts were not in the retrieved body**)
- KCD-8 was 고시 on **2020-07-01** and took effect **2021-01-01**, reflecting WHO's ICD-10 and
  ICD-O-3 updates. The 고시 number **통계청 고시 제2020-175호** is not in this release but *is*
  stated inside the retrieved 약관 themselves [S3] [S4], which is where the documents take it
  from — an instance of a contractual document being the better evidence of a public
  instrument than the instrument's own press release.

(krlib-cancer-r11)=

### R11 — 찾기쉬운 생활법령정보, 「암 예방 및 치료 지원 → 국민건강보험공단 의료비 지원」 (statutory guidance)

- Publisher: 법제처 (Ministry of Government Legislation), 생활법령 service
- URL: `https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=733&ccfNo=3&cciNo=1&cnpClsNo=2`
- Accessed: 2026-09-03, Retrieved: **yes**
- **The 산정특례 rule that shapes the whole product.** Under 국민건강보험법 제44조제1항, 동법
  시행령 제19조제1항 및 별표 2, and 「본인일부부담금 산정특례에 관한 기준」 제4조 및 별표 3, a
  registered cancer patient pays **5% of the 요양급여비용 총액** for **5 years** from
  registration, inpatient or outpatient alike, renewable where residual, metastatic or
  recurrent disease is under continuing chemotherapy. With the scheduled bill already capped
  at 5% there is very little bill left to indemnify, which is why Korea's cancer product is
  written 정액 rather than as a reimbursement — the single most important fact separating this
  product from `Medical_KR_S`. Cited beside [REG-R53], which carries the Act itself.

(krlib-cancer-r12)=

### R12 — 뉴시스, 「'착한 암' 유사암 진단비, 일반암의 20% 수준으로 축소」 (**secondary**, news report)

- Publisher: 뉴시스 (Newsis), **2022-08-01**
- URL: `https://v.daum.net/v/20220801150045941`
- Accessed: 2026-09-03, Retrieved: **yes** (article text)
- Reports that 금융감독원 sent insurers a **공문** setting out 유의사항 for 유사암 진단 보장
  products, with the effect from August 2022 that 유사암 benefits were cut to about **20%** of
  the 일반암 level, from a market in which they had reached ₩50,000,000 (5천만원); it names
  메리츠화재, DB손해보험 and 한화손해보험. **This is a secondary source and the underlying
  공문 was not retrieved**, so what these documents treat as established is the *effect* —
  which the 약관 themselves corroborate, [S8]'s 70% against [S3] [S4]'s 20% — and not the
  instrument. Model point 10 prices the pre-intervention design precisely so that the change
  is visible rather than asserted. Facts resting on this entry alone are marked [unverified].

(krlib-cancer-r13)=

### R13 — 금융감독원, 「질병·상해보험 표준약관」 (보험업감독업무시행세칙 [별표 15]) — **not retrieved**

- Publisher: 금융감독원
- Document: 표준약관 (standard policy conditions, the mandatory baseline every retail Korean
  policy is written on)
- URLs tried: `https://www.fss.or.kr/fss/bbs/B0000115/view.do?nttId=55845&menuNo=200504`;
  `https://www.insclaim.co.kr/19/8641153`; a mirrored PDF on `waf-e.dubudisk.com`
- Accessed: 2026-09-03, Retrieved: **NO** — the FSS board returned an empty reply to `curl`,
  the mirror failed TLS verification, and the third URL returned HTTP 404. **No verbatim
  표준약관 text was obtained under this entry.** The dates of its recent revisions (개정
  2022-02-16 시행 2022-04-01; 개정 2022-09-30 시행 2023-01-01) appear only in search-result
  summaries and are therefore **[unverified]**.
- It is kept because `product-spec.md` cites it twice to say what could not be read. **The
  gap is closed elsewhere and the reader should know where**: the cross-product [REG-R25]
  *is* 시행세칙 [별표 15] and **was** retrieved, as a 492-page PDF extracted in full, so every
  load-bearing 표준약관 statement in these documents — the 보험나이 rule of 제21조, the
  계약자적립액 on death of 제22조, the 납입최고 of 제26조, the 부활 of 제27조 — cites
  [REG-R25] and not this entry.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that page a
plain [R#] refers to its own entries, so the two schemes must never be read across. The
forty-three entries the cancer documents cite, all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: the 생명보험 / 손해보험 / **제3보험** split and the
  deeming provision, at the current [시행 2025. 1. 31.] version. Cancer insurance is
  질병보험 under 제4조제1항제3호. Retrieved: yes (whole Act, 127,346 characters). Cited beside
  this file's [R8].
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is a 기초서류 filed with
  the FSC and never published**, which is why every pricing-basis parameter here is [std] and
  why the safety loading inside [R5]'s 참조순보험요율 cannot be sized. Retrieved: yes.
- **REG-R3** — 보험업법 제120조: the statutory duty to accumulate 책임준비금, cited as a layer
  this model does not compute. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): the statutory footing of 보험개발원 and of
  the 참조순보험요율 regime — the rate is what the bureau **files**, which is why what [R5]
  publishes is a display and why it is a net premium rate rather than a best estimate.
  Retrieved: yes.
- **REG-R5** — 보험업법 제181조·제184조 (보험계리): the 선임계리사 behind the 기초서류 and the
  reserving. Retrieved: yes. **Not** this file's [R5].
- **REG-R7** — 보험업법 시행령 제1조의2 (보험상품): the Decree closing the three product lists
  the Act opens, and the exclusions from them. Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), 본문: the **기준연령 요건** of 제1-2조제2호 —
  「전기납 및 월납 조건으로 남자가 만 40세에 보험에 가입하는 경우」 — which is why model point
  1 is a male 40, and the 계약자적립액 적용이율 with the 금리확정형 / 금리연동형 distinction
  that makes this composite 금리확정형. A full-text search of it returns **zero occurrences of
  예정이율**. Retrieved: yes (226,083 characters, the whole 고시).
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the 잔여보장요소 / 발생사고요소
  taxonomy, with the calculation delegated to the FSS Governor. Retrieved: yes.
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart anywhere else in this repository. On a 미지급형 제3보험 product it
  measures against a surrender value computed on the 제7-66조제1항 basis **even though the
  contract pays nothing during the 납입기간**, which is why `cv_std_pp(t)` is published beside
  `cv_pp(t)`. Retrieved: yes.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당): cited only to record that this
  composite is **무배당** wherever the dividend basis is stated [S1] [S3] [S8], so the
  surplus-distribution machinery does not attach at all. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**): the solvency layer and its sub-risks,
  of which **장해ㆍ질병위험액** carries almost the whole of this product's benefit stream.
  Retrieved: yes (article text; the 기본요구자본 aggregation renders as an image and 별표 22
  was not retrieved). **Not** this file's [R13].
- **REG-R15** — 감독규정 제5-6조 등 (특별계정): cited once, to record that this product has no
  separate account. Retrieved: yes.
- **REG-R17** — 감독규정 제7-63조 (**제3보험의 보험상품설계**): 제1항제1호 requires a 제3보험
  product to pay the **계약자적립액** on death from a cause the policy does not cover and
  terminate — which is the whole of the `claims_death` column on a contract with no death
  benefit, and the requirement `LTC_KR_S`, `Child_KR_S` and `Medical_KR_S` inherit. 감독규정
  제7-61조 applies the same design rule to 장기손해보험, which is why [S1] and [S3] are
  designed identically. Retrieved: yes.
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액): the analysis of premium
  adequacy on **최적기초율** with projected cash flows — the regulatory use of a liability
  cash-flow model in Korea — and the 연납보험료 permission of 제7-65조제2항 that lets the
  account accrue on an annualised basis. Retrieved: yes (the two accrual formulas did not
  extract).
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): the 해약환급금 as
  `max(계약자적립액 − 해약공제액, 0)` floored at zero; the **해약공제기간 capped at seven
  years** by 제7-66조제1항제2호, which puts `surr_chg_pp(t) = 0` from `t = 84` and proves the
  cliff at 납입완료 is a different mechanism; and **제4항**, which permits the 미지급형 form
  precisely *because* the premium was computed on a **최적해지율** — so the lapse vector is a
  condition of the product's legality. Retrieved: yes (operative words in full; the formula
  display did not extract).
- **REG-R20** — 감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액: the
  **표준해약공제액** by formula — 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000,
  the 계수 being 「보험기간(최대 20년)」 — which `surr_chg_cap_pp()` computes at **₩585,000**
  on the anchor, where the 13-month cap binds. Retrieved: yes (1-page PDF, full text including
  all seven notes).
- **REG-R21** — 감독규정 [별표 15] 보험가입금액의 산정: 제3호 covers only 일반사망을 보장하는
  보장성보험, so a cancer contract with no death benefit falls into **제9호** and takes a
  *notional* 보험가입금액 by ratio of risk premiums at the 기준연령 요건. That is the route by
  which a Korean 제3보험 product with no face amount acquires one, and it is what
  `notional_sa_ratio = 0.60` stands in for. Retrieved: yes (1-page PDF).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조 (수수료, 공시, 신고): the first-year
  commission cap of 제4-32조제5항, and **제7-45조제7항, the 보험가격지수** — 보험료총액 divided
  by (참조순보험료 총액 + 평균사업비총액), a ratio and never a rate, which is the only form in
  which a 참조순보험요율 reaches a Korean consumer and the reason every premium in
  `model_point_table.csv` is [std]. Retrieved: yes.
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the supervisor's model policy conditions, and
  the source of every contractual mechanic these documents state that no single 약관 was
  needed to establish — 보험나이 (제21조), the **계약자적립액 payable on death** (제22조),
  납입최고 (제26조) and 부활 with its re-running waiting period (제27조), 청약철회 (제17조),
  the 3-year 소멸시효. **This is the entry that closes the gap left by this file's
  unretrieved [R13].** Retrieved: yes — a 492-page PDF, 441,610 characters extracted.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (계리가정·할인율), 2024-11: the most important
  supervisory document for this library's lapse assumptions. Among models converging to zero
  lapse at 완납 the **로그-선형 모형** is the 원칙모형, converging to **0.1%**, with a
  post-완납 ultimate of **0.8%** — the two endpoints in `lapse_table.csv`, which are therefore
  sourced while its 4.6% start is [std]. **The 「IFRS17 주요 계리가정 가이드라인」 attachment
  was never converted from HWP**, so the values are verified from the 보도자료 and the
  functional form is **[unverified]** at instrument level. Retrieved: yes (the 6-page 보도자료
  and its 6-page 별첨).
- **REG-R28** — 무(저)해지환급금 보험 상품구조 개선 (2020) and the FSS 소비자경보 (2019): the
  supervisory history of the 미지급형 form this composite is written on. Retrieved: yes.
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여 …」 (2019-08-01): the FSC's
  statement of the [별표 14] cap as **13 months' premium for a 보장성보험**, which is the cap
  that binds at the anchor cell and the bound the ₩624,000 of acquisition cost and initial
  commission sits against. Retrieved: yes.
- **REG-R30** — 보험업권 자본규제 고도화 (2025-03-12) and the FSS 지급여력비율 현황: one line
  of solvency context in `technical-notes.md`; nothing is modelled from it. Retrieved: **in
  part** — the FSC page in full, the FSS quarterly only in summary.
- **REG-R33** — 제10회 경험생명표, as reported by 보험매일: the industry table applied from
  **2024-04**, and the evidence that **only 평균수명 and 기대여명 are released**. This and
  [REG-R34] are why `mort_table.csv` is a construction rather than a copy. Retrieved: yes.
  **This is a news article and it is the only retrieved source for the table's existence.**
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 보험정보 빅데이터 플랫폼):
  **negative evidence, which is why it is numbered** — the visible KIDI channels carry no
  downloadable 경험생명표 rate file. Retrieved: **in part**.
- **REG-R35** — 보험연구원, 「K-ICS 경과조치 주요 내용과 시사점」: the inventory of K-ICS
  경과조치, background only. Retrieved: yes.
- **REG-R36** — 보험연구원 CEO Report 03호, 「보험개혁회의 내용과 과제: 건전성 제도」: the
  second-hand route to 별표 22 and the 대량해지 shock, which was **not** retrieved directly;
  anything resting on it carries [unverified]. Retrieved: yes (24 pp.).
- **REG-R38** — 국가데이터처, 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: Korea's
  **public** life tables, and the anchor of the shipped `mort_table.csv` — the 2024 기대여명 at
  40 and 65 (남 41.9 / 19.5, 여 47.4 / 23.7) that the Makeham reproduces exactly, and the
  기대수명 at birth (80.8 / 86.6) it is checked against. Retrieved: yes.
- **REG-R40** — 보건복지부·중앙암등록본부, 「2023년 국가암등록통계 참고자료」: the same
  document as this file's [R1], entered in the cross-product library. Cited where the
  statement is the cross-product one — that this is the citable public cancer basis for the
  whole library, and that 갑상선암 is Korea's most common cancer, which is what the 유사암
  tier exists to hold. Retrieved: yes.
- **REG-R45** — 생명보험협회 공시실, FACT BOOK and 금융통계월보: the stated route to a Korean
  carrier's public product documents, and the market-size series. Retrieved: **in part** — the
  landing page in full, the statistical downloads not.
- **REG-R46** — 보험연구원, 「2026년 보험산업 전망」: the market-size tables behind the one
  paragraph of market context in `product-spec.md`. Retrieved: yes (91 pp.).
- **REG-R47** — 한국보험신문, 2025 outturn (수입보험료 ₩266.6595조, +11.1%): the market
  paragraph's figures, and the structural fact that Korean personal protection business is the
  larger of the two mixes. A news article standing in for an FSS release. Retrieved: yes.
- **REG-R48** — 평균공시이율 and 공시기준이율 (carrier regulatory disclosure): the **2.50%
  평균공시이율 for 2026** on which `prem_int_rate` is anchored, and the 감독규정 제1-2조제13호
  definition behind it. Retrieved: **in part** — the 하나생명 tables in full, the 교보생명 grid
  not.
- **REG-R49** — 상법 제4편 제1장 통칙 (제638조~제664조), from 국가법령정보센터 at [시행 2026.
  7. 23.]: the authoritative copy of the general insurance-contract provisions this file's
  [R7] carries in transcription. Retrieved: yes (631,670 characters).
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): **제736조**, the floor beneath
  the 계약자적립액 payment on death; **제732조**, the 15-year rule that `Child_KR_S` states its
  delta against; and 제739조의2·제739조의3, the 2014 recognition of the disease-insurance
  contract. Retrieved: yes.
- **REG-R51** — 금융소비자 보호에 관한 법률 제46조 (청약의 철회): the statutory cooling-off
  right the 표준약관 제17조 implements; one line in `product-spec.md`. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: the 예금자보호 limit and its calculation basis,
  which on a 제3보험 contract is the 해약환급금 — nil for the whole 납입기간 on the 미지급형
  form. Retrieved: yes.
- **REG-R53** — 국민건강보험법 제41조·제42조·제44조: the public scheme underneath the product —
  the **negative-list** definition of 요양급여, the 본인일부부담금 and the 본인부담상한제 of
  제44조제2항 that sits above the 산정특례 of this file's [R11]. It is why the private product
  is 정액 and why the residual belongs to `Medical_KR_S`. Retrieved: yes.
- **REG-R54** — 노인장기요양보험법 제2조 등: cited once, to mark the boundary with `LTC_KR_S` —
  that product replaces this chassis's KCD-keyed diagnosis trigger with a **statutory** one.
  Retrieved: yes.
- **REG-R55** — 노인장기요양보험법 시행령 제7조 and [별표 1] (등급판정기준): the 1–5등급 and
  인지지원등급 scale that is the same boundary, stated in its operative form. Retrieved: yes.
- **REG-R57** — 소득세법 제59조의4 (특별세액공제 — 보장성보험료): the **12% credit on up to
  ₩1,000,000** of premium — a credit, not a deduction, which is what changes the after-tax
  comparison against every other market in this repository. Retrieved: yes.
- **REG-R60** — 한국회계기준원, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」: the
  standard in force in Korea since **2023-01-01**, cited as the layer that consumes these cash
  flows and as the frame for the contract-boundary question the 갱신형 flag raises and this
  model does not answer. Retrieved: **in part** — the release body returned, the 별첨 HWP
  carrying the standard's own text did not.
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: the **published** morbidity
  reference rates — the 「기타피부암 및 갑상선암 이외의 암 발생률」 grid and the 질병입원율
  grid. The same display as this file's [R5], entered in the cross-product library; the two
  are cited together wherever the incidence basis is asserted, because the fact that it is
  published at all is a library-level fact and the numbers read off it are a product-level
  one. Retrieved: yes.

---

## Provenance note

Every entry above traces to `_research/cancer.md`, which is the citation ground truth for
this product: the S# and R# numbering used here is that file's numbering, unchanged, and it
is **never renumbered** because these documents cite against it. **The research file's own
numbering is not this one's** in the sense that matters — it runs S1–S11 and **R1–R14**,
where this file carries R1–R8 and R10–R13, the two vacant numbers being the uncited R9 and
the unretrieved R14 described in the orientation above. In other products of this library
the two lists diverge further, and a reader moving between them must resolve tags against the
product's own `sources.md` and never against a neighbour's.

What lives in the research file and not here: the section-by-section fact extraction — the
암 / 유사암 / 특정소액암 / 고액암 definitions quoted verbatim from the 약관 with their KCD
code lists, the 면책기간 and 감액기간 matrices benefit by benefit, the 원발부위 기준 and the
2011-04-01 supervisory change, the 재진단암 clock, the 요양병원 dispute record, the
carrier-by-carrier variation table, and the full derivation of the incidence basis from
국가암등록통계 including the reconciliation against [R5] that agrees to +1.6%; the retrieval
method per host, including which extractor recovered which PDF and where the doubled-glyph
artefact makes a quotation unsafe; and the register of fetch failures and [unverified] claims.

That register is short and every item in it is load-bearing, so it is worth naming here.
**The 제10회 경험생명표 rates**, released as summary statistics only [REG-R33] [REG-R34],
which is why `mort_table.csv` is a Makeham fitted to [REG-R38] rather than a table.
**The 표준약관's own text under [R13]**, unreachable at three URLs, with the gap closed by the
cross-product [REG-R25]. **The August 2022 유사암 공문** [R12], whose *effect* is corroborated
by the 약관 themselves and whose *instrument* was never seen. **The FSS's own copy of the
2017 금융꿀팁 release** [R6], read through a reproduction. **The KCD-8 고시 number** [R10],
taken from the 약관 rather than from the press release. **[S8]'s 보장내용 and 가입예시 tabs**,
rendered client-side, which is why the one retrieved premium illustration has no stated
보험가입금액 behind it. **[S11] entirely** — Korea's largest life insurer, an HTTP 200 that
was a JavaScript shell. **The 「IFRS17 주요 계리가정 가이드라인」 attachment** [REG-R27], whose
values were retrieved and whose functional form was not. **보험업감독규정 별표 22** and the
K-ICS 대량해지 shock, known only second-hand through [REG-R36]. And **every expense,
commission, lapse, cancer-utilisation and post-diagnosis-treatment figure in the Korean
market**: no carrier and no regulator publishes any of them, and [R1] publishes incidence,
survival and prevalence and nothing whatever about treatment volume. Those absences are why
`model.md`'s standardization table has an "Observed range" column that reads *none published*
on so many of its rows, and why `care_table.csv` says so on every one of its own.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-cancer-r1
[R10]: #krlib-cancer-r10
[R11]: #krlib-cancer-r11
[R12]: #krlib-cancer-r12
[R13]: #krlib-cancer-r13
[R3]: #krlib-cancer-r3
[R5]: #krlib-cancer-r5
[R6]: #krlib-cancer-r6
[R7]: #krlib-cancer-r7
[R8]: #krlib-cancer-r8
[REG-R1]: #krlib-reg-r1
[REG-R13]: #krlib-reg-r13
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R49]: #krlib-reg-r49
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R53]: #krlib-reg-r53
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
