# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/term-life.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is
per product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md` runs
its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read
across.** The clearest instance is right here: this file's **[R9]** is 보험업감독규정
**[별표 14]**, while the library's **[REG-R9]** is the 보험업감독규정 **본문**. Access date
for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 약관 (*yakgwan*, policy conditions), a 상품요약서
  (statutory product summary), a 예상 갱신보험료 예시, a carrier product page, or the
  생명보험협회's statutory cross-carrier disclosure. These are what makes a contractual
  mechanic *sourced* rather than assumed, and — unusually for this repository — what makes
  the anchor premium a published figure rather than a standardization.
- **[R#]** — a regulatory, statutory or statistical reference that only this product needs.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Unused sources are omitted, so both schemes have gaps.** `S24` (오렌지라이프 「무) 스마트
정기보험」, HTTP 503 on both pages) is not cited and is not listed. `R5`, `R7`, `R10`, `R11`,
`R13`, `R14`, `R15`, `R17` and `R21` are not cited either, because the cross-product library
carries the same documents with fuller annotation and a better retrieval — 상법 제651조 and
제662조 as [REG-R49], the 보험업감독규정 본문 as [REG-R9], the 시행세칙 as [REG-R23], the
2024 계리가정 가이드라인 release as [REG-R27], the 제10회 경험생명표 report as [REG-R33], the
국가데이터처 생명표 as [REG-R38], and the 예금자보호한도 change as [REG-R32] beside the
statutory [REG-R52]. Nothing was newly retrieved at drafting; no tag was added.

**Where a [R#] and a [REG-R#] are cited together, that is deliberate corroboration and not
redundancy.** Nine of the twelve entries below were retrieved by a *different route* from
their cross-product counterparts — article text from `casenote.kr`, which serves plain
fetchers, against the full-Act and full-고시 retrievals behind the [REG-R#] entries — so a
statutory claim carrying both tags was read twice from two independent renderings. [R9] and
[REG-R20] are the one true duplicate: the same one-page 별표 14 PDF, downloaded in both
research passes.

Company and branded product names appear in this file and in `_research/term-life.md` and
nowhere else in the library. In `product-spec.md`, `technical-notes.md` and `model.md` a
carrier is its tag alone, so a reader can always resolve who said what — here — and never
has to.

---

## Primary product sources

Nine carriers and the 생명보험협회 — twenty-four documents in twenty-three entries. Three
are the 생명보험협회's own statutory disclosures and the basis table under them: the
정기보험 comparison [S4], its 대표계약 basis [S5], and the 종신보험 comparison read as
negative evidence [S22]. One is a full 190-page 약관 [S2]; twelve are 상품요약서 [S1] [S6]
[S8] [S9] [S10] [S11] [S12] [S15] [S17] [S18] [S19] [S20], with [S21] carrying two more;
two are the mandatory 예상 갱신보험료 예시 [S7] [S16]; three are carrier consumer or
quotation pages [S3] [S13] [S14]; and one could not be fetched at all [S23].

**Nine documents carry a published premium scale**, which is the single largest documentary
difference from every other library in this repository: [S1] [S4] [S6] [S7] [S8] [S11] [S12]
[S14] [S16]. Korea publishes term premiums because it is required to — every 상품요약서
prints a grid, and the 생명보험협회 publishes a like-for-like comparison of 45 products on
one prescribed basis. That is why the anchor cell's ₩15,080 a month is a **sourced** number
appearing twice independently and not a [std] one.

(krlib-term_life-s1)=

### S1 — 「한화생명 e정기보험 무배당 상품요약서」, 한화생명보험(주) (statutory product summary)

- Document: 상품요약서, file `한화생명 e정기보험 무배당_상품요약서_20260417.pdf`, 14 PDF pages
- URL: `https://static.hanwhalife.com/dynamic/direct/product/cms_I1gR8ivwtn8cVwbq_1776383286029.pdf`
  (linked from [S3])
- Accessed: 2026-09-03, Retrieved: **yes** (473 KB PDF fetched with a browser User-Agent and
  a referer header; all fourteen pages extracted cleanly as Korean text)
- The densest quantitative document in the set after [S12], and the second of the two
  carriers whose 적용해지율 endpoints the lapse basis rests on. It establishes: the
  순수보장형 / 만기환급형 split and the 해약환급금 미지급형 wording (납입기간 중 0%, 납입
  기간 후 50% of the 표준형) that the model's `claims_lapse` column of zeros and the
  uncomputed shortened-pay step-up both rest on; a 표준체 vs 건강체 premium grid at ages
  30/40/50 for both sexes; 최고가입나이 matrices by 보험기간 × 납입기간 × sex; 가입한도
  1,000만원~5억원; the 50% 장해 premium waiver; 적용이율 연복리 **2.50%**, which is
  `prem_int_rate`; 예정 경험사망률 at 20/40/60; the **적용해지율 연 0.1%~8.4% in payment and
  연 0.8% after 납입완료**, which are the `in_payment_start` upper observation and the
  `post_payment` row of `lapse_table.csv`; four 해약환급금 예시 tables printing **환급률
  0.0% at all eleven durations for both sexes**; the rule that the 만기환급형's maturity
  benefit is computed as if waived premiums had been paid; and the 보험가격지수 with its
  stated basis.

(krlib-term_life-s2)=

### S2 — 「한화생명 e정기보험 무배당 보험약관」, 한화생명보험(주) (full policy conditions)

- Document: 보험약관 — 약관 가이드북, 주계약 약관 for both product forms, 특별약관, 분류표
  and 부록; file `한화생명 e정기보험 무배당_약관_20260417.pdf`, **190 PDF pages**
- URL: `https://static.hanwhalife.com/dynamic/direct/product/cms_odIN6hkhR1w3xURZ_1776383301736.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (3.82 MB PDF; all 190 pages extracted as clean
  Korean text, the only glyph loss being in two cover graphics)
- **The only full 약관 retrieved in this session**, and the source of every verbatim clause
  quoted in the product documents. Articles the documents pin to it: 제4조 (지급사유, and the
  선지급 cap and its 평균공시이율 discount), 제5조 (the 50% 장해 waiver and its cause-neutral
  trigger 「동일한 재해 또는 재해이외의 동일한 원인」), 제6조 (the two-year suicide bar),
  제8–9조 (the 3/10/30 영업일 claim timetable), 제14–15조 (contestability), 제18조 (청약
  철회), 제20조 (무효), **제22조 (보험나이)** — the age basis the whole model is indexed on —
  제23조 (소멸), 제26조 (자동대출납입), **제28조 (부활)**, which is where the sourced
  `reinstate_window = 3` and the words 「해약환급금이 없는 경우를 포함합니다」 come from,
  **제33조 (해약환급금, including the 미지급형 sub-article)**, 제34조 (보험계약대출), 제38조
  (소멸시효), 【별표3】 재해분류표, and the 선지급서비스특약 wording.

(krlib-term_life-s3)=

### S3 — 한화생명 다이렉트 「한화생명 e정기보험 무배당」 상품상세 페이지 (consumer product page)

- URL: `https://direct.hanwhalife.com/products/CM090101`
- Accessed: 2026-09-03, Retrieved: **yes** (190 KB HTML fetched raw and stripped; the
  graphics are SVG and carry no numbers the documents depend on)
- Establishes the consumer-facing framing of the same contract: 사망보험금 1천만~5억원, the
  순수보장형 / 만기환급형 choice, the statement that the 해약환급금 미지급형 is **14%
  cheaper** than the 표준형 on a stated basis, the 건강고객 0~20% discount and its three
  criteria, 가입가능연령 만19세~65세, the two-year suicide bar, the 예금자보호 ₩100,000,000
  notice, and the note that the premium changed with the April 2026 산출이율 revision.

(krlib-term_life-s4)=

### S4 — 생명보험협회 공시실, 상품비교공시 — 보장성보험 / **정기보험** (statutory cross-carrier disclosure)

- Publisher: 사단법인 생명보험협회, 공시실
- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/listNew.do` (POST with
  `search_prodGroup=024400010002`; eight pages at `pageUnit=30`)
- Accessed: 2026-09-03, Retrieved: **yes** (all eight result pages fetched raw and the result
  table parsed; **45 distinct 정기보험 products across 15 carriers** recovered with their
  가입금액, 남/여 보험료, 확정이율, 보험가격지수, 상품특징, 해약환급금 유형, 갱신여부,
  판매채널 and 판매일자)
- **The sharpest quantitative source in the Korean market, and it is public.** Because every
  product is disclosed on one prescribed 대표계약 basis [S5], the table is a genuine
  like-for-like comparison — something no other country library here has. The documents rest
  the following on it: the anchor premium's **second independent appearance** (₩15,080 male,
  ₩8,010 female, agreeing to the won with [S12]); the observed spread at the same cell
  (₩14,400 / ₩15,000 / ₩16,000 / ₩16,000 / ₩16,100 / ₩18,400); the female-to-male premium
  ratios of 52–56% across the six direct writers and 47% to 90% across the face-to-face and
  simplified-issue rows, which is the only handle on the per-policy fee no Korean rate card
  lets you decompose; and the
  **보험가격지수 dispersion of 51.6% to 239.1%**, which is the only public handle on an
  expense assumption. It also links each product's 상품요약서 PDF, which is how [S6] and
  [S8]–[S12] and [S15]–[S18] were obtained.

(krlib-term_life-s5)=

### S5 — 생명보험협회 공시실, 「상품비교공시 세부작성기준 (대표계약 기준) - 보장성」 (the disclosure's own basis table)

- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/informationPopup.do`
- Accessed: 2026-09-03, Retrieved: **yes** (12 KB HTML read in full)
- Establishes the 대표계약 basis without which [S4] would be uninterpretable: for 정기보험
  기본형 it is 남자/여자, **나이 40세, 보험기간 20년, 납입기간 전기납, 납입주기 월납,
  가입금액 1억원**, applied identically to 만기환급형, 순수보장형 and 무해지/저해지환급.
  This is the model's anchor model point, and it is the same cell as the 감독규정's
  기준연령 요건 [REG-R9] — which is what makes model point 1 doubly prescribed.

(krlib-term_life-s6)=

### S6 — 「무배당 흥국생명 온라인정기보험 상품요약서」, 흥국생명보험(주) (statutory product summary)

- Document: 상품요약서, 준법감시인 심의필 제26-CA1-0030호 (2026.02.08.), 8 numbered pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=15767&seq=14` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (96 KB PDF, extracted cleanly)
- **The only retrieved document that sets out a 갱신형 term product's renewal rules alongside
  the 비갱신형 alternative in the same product**, and therefore the single source behind most
  of the renewal machinery in `Term_KR_S`. It establishes: the ten-year 갱신 cycle and the
  **보험나이 80 ceiling**, which is `renew_ceiling()`; the truncation rule 「갱신일부터 최종
  갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 …」, which is `term_len(k)`; the
  clause that a **premium waiver already running does not carry into the renewed contract**,
  which is `check_waiver_reset()`; the 기본형 / 보장추가형 split paying **2× on 재해사망**,
  which is the `acc_death` module; the rule that a female life may buy only 보장추가형;
  적용이율 연복리 2.75%; **예정 경험사망률 and 예정 재해사망률 at 20/40/60**, the second of
  which is the whole `acc_mort_rate` column of `mort_table.csv`; four 해약환급금 예시 tables;
  and two 보험가격지수 tables.

(krlib-term_life-s7)=

### S7 — 「(무)흥국생명 온라인정기보험 예상 갱신보험료 예시」, 흥국생명보험(주) (mandatory renewal-premium projection)

- Document: 예상 갱신보험료 예시, 1 PDF page
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=15773&seq=10` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (31 KB PDF, extracted cleanly)
- **The single most useful quantitative document for the 갱신형 mechanic.** It is the whole
  published premium ladder the model reproduces to the won on model point 3 — **₩9,000 →
  ₩21,000 → ₩56,000 → ₩201,000** a month at attained 보험나이 40 / 50 / 60 / 70 for a male
  life, against ₩6,000 → ₩10,000 → ₩24,000 → ₩103,000 for a female one — together with the
  caveat that the projection **holds the rate scale at its issue-date level and reflects
  연령증가 alone**, which is why the fourth key model risk is a discretionary risk rather
  than a modelling one. It also establishes, negatively, that the
  disclosure requires the **price** path and never the **persistency** path, which is why
  `renewal_decline_base` is [std].

(krlib-term_life-s8)=

### S8 — 「삼성 인터넷정기보험(2601)(무배당) 상품요약서」, 삼성생명보험(주) (statutory product summary)

- Document: 상품요약서, 9 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=42677&seq=4` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (230 KB PDF, extracted cleanly; running text on
  two pages loses inter-word spaces but is fully legible)
- Establishes the 1종 (순수보장형) / 2종 (만기환급형) × 1형 (일반형) / 2형 (**걷기할인형**)
  matrix and its 8,000-steps-on-20-days qualifying test; the 슈퍼우량체 criteria; a **표준체
  vs 슈퍼우량체 premium grid at ages 20/30/40/50 for both sexes**; 가입나이 20~64세; 가입한도
  5,000만원~3억원; the **적용이율 split — 순수보장형 2.5%, 만기환급형 2.25%** — which is the
  fact model point 6's negative undiscounted total turns on; 표준체 사망률 at 20/40/60,
  contributing to the observed 1.77x dispersion at male 40; and two 해약환급금 예시 tables.

(krlib-term_life-s9)=

### S9 — 「삼성 내리사랑정기보험(2501)(무배당) 상품요약서」, 삼성생명보험(주) (statutory product summary)

- Document: 상품요약서, 16 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=40924&seq=4` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (273 KB PDF, extracted; the same word-spacing loss)
- A **face-to-face-channel** product in a set otherwise dominated by direct writers, and the
  clearest statement of a **15-year 갱신형특약** cycle riding on a 비갱신 정기보험 주계약.
  It carries the two facts that make the contract-boundary question real and unsettled: the
  renewal is effected by the policyholder **not objecting 15 days before expiry** — the
  negative option that bounds `renewal_decline_base` from below — and the insurer may reprice
  the **whole 기초율 including 위험률** on a **new product code**, which is the argument for
  the short boundary reading. Also: the 고액할인 for 가입금액 ≥ 1억원, the 우량체 criteria,
  the 재가입형 특약 variant, 가입나이 20~65세, and 적용이율 2.5% / 2.0%.

(krlib-term_life-s10)=

### S10 — 「신한SOL정기보험(무배당) 상품요약서」, 신한라이프생명보험(주) (statutory product summary)

- Document: 상품요약서, 13 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=41655&seq=5` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (108 KB PDF, extracted cleanly)
- The **기본형 / 재해보장형** product split — 2× the sum assured on 재해사망 and 1× otherwise
  — is the cleanest evidence in the set that Korean accidental-death cover is sold as a
  *product variant* as often as a rider, and it is what model point 10 implements. Its second
  disclosed 예정 재해사망률 table is what makes the cross-carrier pairing in `mort_table.csv`
  defensible: the two carriers agree to three significant figures at age 20. Its 해약환급금
  예시 is the only one given at **every policy year from 1 to 10**, and is the source of the
  표준형 comparator reaching 46% of premiums paid by duration six — the number that makes the
  `claims_lapse` zeros an asserted fact rather than a product-class inference. Uniquely in
  this set it also prints **the 보험개발원 reference-rate document numbers** behind its
  예정 경험사망률 and 예정 재해사망률, which is [R19].

(krlib-term_life-s11)=

### S11 — 「KB 착한정기보험Ⅱ 무배당 상품요약서」, KB라이프생명보험(주) (statutory product summary)

- Document: 상품요약서, 11 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=34504&seq=9` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (379 KB PDF, extracted cleanly)
- One of the two carriers publishing a **full 예정 경험사망률 table per rate class**, which
  is what lets `rate_class_table.csv` be sourced rather than standardized. Four tiers
  (표준체 / 비흡연체 / 건강체 / 슈퍼건강체) with criteria including a **총콜레스테롤
  190mg/dL 미만** test seen at no other carrier; a premium grid at 30/40/50 for both sexes
  across all four classes; 가입한도 that **rises with the rate class**; 적용이율 연복리
  2.50%; and a 해약환급금 예시.

(krlib-term_life-s12)=

### S12 — 「무배당 교보라플 정기보험 상품요약서」, 교보라이프플래닛생명보험(주) (statutory product summary)

- Document: 상품요약서, 28 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=13489&seq=31` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (335 KB PDF, extracted cleanly)
- **The anchor carrier**, and the only document retrieved that prints the 무해지 form and its
  표준형 comparator side by side, premium and surrender value, in one table. Nearly every
  quantitative input to `Term_KR_S` traces here: the twenty published cells of
  `prem_rate_table.csv`, including the anchor `(pure, M, 40, 20) = ₩15,080` and its female
  twin ₩8,010; the four disclosed 예정 경험사망률 tables, one per rate class, whose 표준체
  values at 20/40/60 are the three Makeham anchors of `mort_table.csv` and whose ratios are
  `rate_class_table.csv`; the **적용해지율 연 0.1%~4.6%** that is `lapse_table.csv`'s
  `in_payment_start` and `in_payment_end`; 적용이율 (미지급형 2.50%, 만기환급형 2.25%), which
  is `prem_int_rate`; the **2026 평균공시이율 2.50%**, which is `accel_disc_rate`; the ₩10
  quotation granularity that `round_10` reproduces; the fullest rate-class definitions and
  보험기간 × 납입기간 × 가입나이 matrix in the set; 가입한도 1억원~10억원; and the five-way
  보험료납입면제보장특약 menu.

(krlib-term_life-s13)=

### S13 — 교보라이프플래닛, 「(무)교보라플 정기보험」 상품 페이지 (consumer product page)

- URL: `https://www.lifeplanet.co.kr/lpds2/insurance/term-life-insurance.dev`
- Accessed: 2026-09-03, Retrieved: **yes** (806 KB HTML fetched raw and stripped)
- The consumer framing of [S12]: 사망보험금 1억원~10억원, a headline 「최대 63% 인하된
  보험료」 with its stated basis, two 보험료 예시 at 70세만기, the three rate classes'
  consumer-facing criteria, the 납입면제 특약 restricted to 순수보장형, the 30-day 청약철회,
  the two-year suicide bar, and the 예금자보호 ₩100,000,000 notice. **A block of 가입 시
  유의사항 boilerplate on this page mixes several products' warnings**, and nothing in the
  product documents rests on that block.

(krlib-term_life-s14)=

### S14 — 교보라이프플래닛, 「(무)라이프플래닛e정기보험Ⅱ」 보험료 설계 페이지 (consumer quotation page)

- URL: `https://www.lifeplanet.co.kr/products/dth/HPPC61S0N.dev`
- Accessed: 2026-09-03, Retrieved: **yes** (840 KB HTML fetched raw and stripped, after a
  summarising fetch returned a garbled reading of the premium block)
- A second, older term product from the same carrier, still on sale, with a **선택형
  만기환급률 of 0% / 50% / 100%** — the only three-way return-of-premium menu in the set — a
  four-class premium comparison at one cell, a three-point 만기환급률 premium comparison at
  the same cell, and 일시납 among the payment modes. It is one of the five grids the
  documents use to establish that **every Korean rate card retrieved fixes the sum assured**,
  so no flat policy element can be decomposed the way `jplib` decomposes one.

(krlib-term_life-s15)=

### S15 — 「푸본현대 원패스 정기보험 무배당/갱신형(2404) 상품요약서」, 푸본현대생명보험(주) (statutory product summary)

- Document: 상품요약서, 12 PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=37829&seq=5` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (108 KB PDF, extracted cleanly)
- **The shortest-cycle renewable term in the set** — a 1년만기 contract renewing up to four
  times, sold through a mobile app, with the renewal effected by the policyholder *not*
  objecting 15 days before expiry. It prints the **상품코드 for the 최초계약 and the
  갱신계약 separately**, which is the direct evidence that a Korean renewal is a new contract
  on a new product code — the strongest single argument in the set for the short contract
  boundary, and the reason `comm_new_term_rate` exists as a switch at all.

(krlib-term_life-s16)=

### S16 — 「푸본현대 원패스 정기보험 예상 갱신보험료 예시」, 푸본현대생명보험(주) (mandatory renewal-premium projection)

- Document: 예상 갱신보험료 예시, 1 PDF page
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=37830&seq=2` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (22 KB PDF, extracted cleanly)
- A four-renewal premium path at ages 41–44, with the same rate-scale-frozen caveat as [S7].
  Its evidential role in the documents is the **second** confirmation that the mandatory
  renewal disclosure shows a price path and never a persistency path, which is what makes
  `renewal_decline_base = 0.20` a documented gap rather than a research failure. The
  document's own basis line is internally inconsistent and no figure in the product documents
  depends on the inconsistent part.

(krlib-term_life-s17)=

### S17 — 「미래에셋생명 헤리티지 정기보험 무배당 상품요약서」, 미래에셋생명보험(주) (statutory product summary)

- Document: 상품요약서, 20+ PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=43797&seq=2` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (2.72 MB PDF; extracted with a space after almost
  every syllable block, so the text was reflowed before reading and each figure re-checked)
- The **간편고지형** (simplified-issue) form and its **two-year 50% 감액지급 period** for
  non-accidental death — Korea's graded death benefit, which has no analogue in the level
  term products of `uklib` or `jplib`, and which the product specification scopes out of the
  composite. Also a 종신전환특약 and a 연금전환특약, 적용이율 연복리 2.00% (the low end of the
  observed 2.00–2.75% range), and mortality at 20/40/60 contributing to the 1.77x dispersion.

(krlib-term_life-s18)=

### S18 — 미래에셋생명, 「경영인을 위한 정기보험 무배당 [해약환급금이 적은 유형]」 상품요약서 (statutory product summary)

- Document: 상품요약서 (일반가입형 / 간편고지형), 20+ PDF pages
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=44327&seq=2` (linked from [S4])
- Accessed: 2026-09-03, Retrieved: **yes** (2.90 MB PDF; same reflow treatment as [S17])
- The **경영인정기보험** family in full: a 90세만기 전기납 contract, 가입금액 5천만원~30억원,
  whose sum assured **escalates** from year 10 by a printed formula (체증보험금 = 보험가입
  금액 × 체증률 × (계약경과년수 − 9), 체증률 10%), with a three-step 해약환급금이 적은 유형
  (0% / 30% / 95%) and a 해약환급금 중도지급옵션. It is the evidence for the corporate-market
  variant the specification names and excludes, and for the statement that a Korean term sum
  assured is not always level.

(krlib-term_life-s19)=

### S19 — 「한화생명 H종신보험 무배당 상품요약서」, 한화생명보험(주) (statutory product summary, whole life)

- Document: 상품요약서, 20 PDF pages, `2209-A01_A17`, dated 20251003
- URL: `https://static.hanwhalife.com/dynamic/direct/product/cms_6r7g9G9XxiX5MbrW_1762729381266.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (677 KB PDF, extracted cleanly)
- Cited only as **negative evidence**, and it is the strongest kind available: a current
  Korean 종신보험's rider menu lists 3대질병케어특약, 9대질병보험료납입면제특약 and eleven
  제도성특약, and **no 정기특약 at all**. That is what supports the finding that the Japanese
  and US pattern of a term rider on a whole life chassis has largely disappeared in Korea.

(krlib-term_life-s20)=

### S20 — 「무배당 AIA 더해주는 종신보험 상품요약서」, AIA생명보험(주) (statutory product summary, whole life)

- URL: `https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/life-protection/summary/AIA_kr_Form120_20260101.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (731 KB PDF; a summarising fetch reported it as
  binary, so the file was saved and extracted locally with `pymupdf`)
- Same negative test as [S19], same answer: the string 정기특약 does not occur.

(krlib-term_life-s21)=

### S21 — 「한화생명 하나로H종신보험 무배당」 and 「한화생명 e종신보험 무배당」 상품요약서, 한화생명보험(주) (two statutory product summaries, whole life)

- URLs: `https://pub.insure.or.kr/FileDown.do?fileNo=45581&seq=3` and
  `https://pub.insure.or.kr/FileDown.do?fileNo=45532&seq=2` (both linked from the 종신보험
  view of the same disclosure as [S4], `search_prodGroup=024400010001`)
- Accessed: 2026-09-03, Retrieved: **yes** (753 KB and 553 KB PDFs, extracted cleanly)
- Same negative test, same answer, at two further products of the anchor 약관's own carrier.

(krlib-term_life-s22)=

### S22 — 생명보험협회 공시실, 상품비교공시 — 보장성보험 / **종신보험** (statutory cross-carrier disclosure)

- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/listNew.do` (POST with
  `search_prodGroup=024400010001`; first two pages fetched)
- Accessed: 2026-09-03, Retrieved: **in part** (pages 1–2 of the 종신보험 result set)
- The population-level version of the [S19]–[S21] test: across the two pages read, the
  substring 정기 occurs only in the page's own category label. Used for that one finding and
  nowhere else.

(krlib-term_life-s23)=

### S23 — 「삼성생명 자유설계보장보험(무배당) 약관」 (2014), republished by 인스클레임 (superseded policy conditions)

- URL: `https://www.insclaim.co.kr/39/8650566`
- Accessed: 2026-09-03, Retrieved: **no** (HTTP 404)
- Listed precisely because it could **not** be read. A search result named this superseded
  약관 as containing a 정기특약, which would date the disappearance of the term rider rather
  than merely observe it. The document did not return, so the claim rests on a search snippet
  and is tagged **[unverified]** wherever the product specification makes it. No quantitative
  parameter depends on it.

---

## Regulatory and actuarial references

Twelve entries. Nine were retrieved from `casenote.kr`, which serves statute article text to
a plain fetcher where `law.go.kr`'s friendly URLs return only site chrome; those nine are
also carried, from an independent full-Act retrieval, in the cross-product library, and the
product documents cite both.

(krlib-term_life-r1)=

### R1 — 보험업법 제2조 (정의) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 보험업법, 법률 제19211호, 시행 2023-01-01
- URL: `https://casenote.kr/법령/보험업법/제2조`, Accessed: 2026-09-03, Retrieved: **yes**
- The definition of 보험상품 and within it of **생명보험상품** and **제3보험상품**. This is
  the clause that puts 정기보험 squarely in the 생명보험 (first-sector) class and outside
  제3보험, which is the classification statement at the head of `product-spec.md` and the
  reason this product is the library's protection chassis rather than one of its four
  제3보험 products. Cited beside [REG-R1], which carries the same article from the full-Act
  retrieval.

(krlib-term_life-r2)=

### R2 — 보험업법 제4조 (보험업의 허가) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 보험업법, 법률 제17636호, 시행 2021-06-09
- URL: `https://casenote.kr/법령/보험업법/제4조`, Accessed: 2026-09-03, Retrieved: **yes**
- The three-way licence split — 생명보험업 / 손해보험업 / **제3보험업 (상해·질병·간병)** —
  and the restriction of the licence to 주식회사, 상호회사 및 외국보험회사. 정기보험 is
  written under 제1항제1호; 제1항제3호 is the statutory footing of the 제3보험 category four
  other krlib products sit in. Cited beside [REG-R1].

(krlib-term_life-r3)=

### R3 — 상법 제731조 (타인의 생명의 보험) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 상법, 시행 2020-12-10, 법률 제17354호
- URL: `https://casenote.kr/법령/상법/제731조`, Accessed: 2026-09-03, Retrieved: **yes**
- Verbatim: 「타인의 사망을 보험사고로 하는 보험계약에는 보험계약 체결시에 그 타인의 서면에
  의한 동의를 얻어야 한다.」 This is the rule every 약관 in the set reproduces as a ground of
  계약의 무효, and it is why the specification's three-role table (계약자 / 피보험자 /
  수익자) states written consent as a formation requirement. Cited beside [REG-R50 제731조](#krlib-reg-r50).

(krlib-term_life-r4)=

### R4 — 상법 제732조 (15세미만자등에 대한 계약의 금지) and 제732조의2 (중과실로 인한 보험사고) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 상법
- URLs: `https://casenote.kr/법령/상법/제732조` and
  `https://glaw.scourt.go.kr/wsjo/lawod/sjo192.do?lawodNm=상법&jomunNo=732&jomunGajiNo=2`
- Accessed: 2026-09-03, Retrieved: **in part** — the article text was returned by a search of
  those pages rather than by a direct fetch of each; the wording matches the paraphrase every
  retrieved 약관 gives, so it is treated as reliable and the pinpoint is marked accordingly
- Two facts the product documents rest on it. 제732조 voids a contract on the death of a
  person under **만 15**, which is **the one place in this product where 만나이 and not
  보험나이 is the operative age** — stated in `model.md` because importing that basis into
  the projection is a live modelling error. 제732조의2 preserves the death benefit where the
  event arose from **gross negligence**, which is why a Korean life 약관's exclusion list
  contains only intent. Cited beside [REG-R50].

(krlib-term_life-r6)=

### R6 — 상법 제659조 (보험자의 면책사유) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 상법
- URL: `https://casenote.kr/법령/상법/제659조`, Accessed: 2026-09-03, Retrieved: **yes**
- Verbatim: 「보험사고가 보험계약자 또는 피보험자나 보험수익자의 고의 또는 중대한 과실로
  인하여 생긴 때에는 보험자는 보험금액을 지급할 책임이 없다.」 Read together with [R4]
  제732조의2 it explains the shape of the exclusion list in the specification — intent only —
  and the treatment of the benefit where one of several beneficiaries is the killer. Cited
  beside [REG-R49].

(krlib-term_life-r8)=

### R8 — 소득세법 제59조의4 (특별세액공제) (statute)

- Publisher: 국가법령정보센터 / 법제처 — 소득세법, 법률 제19196호, 시행 2024-01-01
- URL: `https://casenote.kr/법령/소득세법/제59조의4`, Accessed: 2026-09-03, Retrieved: **yes**
- 제1항: **「그 금액의 100분의 12(제1호의 경우에는 100분의 15)」** of 보장성보험료, capped at
  **연 100만원** of premium per basket. This is a **tax credit, not a deduction**, which is
  the structural difference from Japan's 生命保険料控除 and from every other market in this
  repository. The cap is on the **premium**, not on the credit, so the anchor cell's
  ₩180,960 annual premium sits well inside the basket and the credit is 12% of the whole of
  it — ₩21,715, against the ₩120,000 a full basket would give. Cited beside [REG-R57].

(krlib-term_life-r9)=

### R9 — 보험업감독규정 【별표14】 표준해약환급금 계산시 적용되는 해약공제액 (제7-66조 관련) (annex to the supervisory regulation)

- Publisher: 금융위원회 — 개정 2011-01-24, 2015-05-07, 2020-01-15
- URL: `https://www.law.go.kr/LSW//flDownload.do?flSeq=137472119&flNm=[별표 14] 표준해약환급금계산시 적용되는 해약공제액(제7-66조관련)`
- Accessed: 2026-09-03, Retrieved: **yes** (111 KB PDF downloaded through a summarising fetch
  that reported it as binary, extracted locally with `pymupdf`, read in full including all
  seven notes)
- The **statutory cap on the surrender charge**: 「연납순보험료의 5% × 해약공제계수 +
  보장성보험의 보험가입금액의 10/1000」, with 해약공제계수 the 보험기간 capped at 20 years
  for a 보장성보험 and the 연납순보험료 recomputed on a 전기납 (20년납 if longer) basis. The
  documents use it to show that the cap is **nowhere near binding on this product** — its
  sum-assured limb alone is ₩1,000,000 at the anchor against a modelled year-1 acquisition
  charge of ₩228,576 — which is why `model.md` computes no 표준해약공제액. **This is the same
  document as [REG-R20]**, retrieved independently in both research passes; and it is not the
  same document as [REG-R9], which is the 감독규정 본문.

(krlib-term_life-r12)=

### R12 — 금융위원회 보도자료 (2021-11-08), 「무·저해지보험의 지속가능성 제고를 위해 … 상품설계를 합리적으로 개선하겠습니다.」 (regulator press release)

- Publisher: 금융위원회 보험과
- URL: `https://www.fsc.go.kr/no010101/76830`, Accessed: 2026-09-03, Retrieved: **yes**
  (fetched through a summarising fetcher; plain `curl` to `fsc.go.kr` was reset by the host)
- The 2021 supervisory intervention in 무·저해지 product design, and the earlier of the two
  Korean lapse-assumption interventions the product documents lean on. It supplies: the
  growth of 무·저해지 new business (신계약건수 30.4만건 in 2016 → 443.5만건 in 2020); the
  해지율 산출기준 then imposed — 「해지환급금 수준이 낮으면(10%, 50%) 해지율을 더 낮게(0.2%,
  1%) 적용」 and a lapse rate declining with duration; and the worked table of premium against
  post-완납 해약환급금 level (0% / 30% / 50%) that the specification reproduces as the
  −25.2% premium discount for the 무해지 form. Distinct from [REG-R28], which is the 2020
  상품구조 개선 and the 2019 FSS 소비자경보, and from [REG-R27], which is the 2024 guideline.

(krlib-term_life-r16)=

### R16 — 보험연구원, 「2026년 보험산업 전망」, 노건엽 (2025-10-21 세미나 자료) (industry outlook deck)

- URL: `http://www.kiri.or.kr/pdf/세미나자료/smn_20251021_1.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (3.35 MB PDF extracted; chart data labels extract
  as bare numbers and were read against their axis labels)
- Cited for the market-context finding that **term life is not where the Korean life market
  is growing**: 보장성보험 수입보험료 2021–2024 of ₩44.9 / 47.1 / 48.6 / 55.0조 and 2025 H1
  of ₩30.3조 (+13.0%), with the growth concentrated in **무·저해지환급형 질병보험과
  상해보험** rather than in death cover. A **different document** from [REG-R46], which is
  황인창's 91-page deck from the same seminar series; the two are cited together and agree.

(krlib-term_life-r18)=

### R18 — 보험저널, 「금융당국 해지율 예측 한참 빗나가… 저해지 종신보험 3년차 해지율 '50%' 돌파」 (2025-05-14) (news article)

- Publisher: 보험저널 (insjournal.co.kr)
- URL: `https://www.insjournal.co.kr/news/articleView.html?idxno=26597`
- Accessed: 2026-09-03, Retrieved: **yes**. The underlying supervisory data was **not**
  retrieved, so the figures are second-hand
- The only Korean lapse-experience datum available anywhere in this product's research: for
  5·7년납 저해지 단기납 종신보험, an actual **37회차 유지율 of 50.2% against an assumed
  71.5%**. It is a whole-life datum and not a term one, and the documents use only its
  **direction** — that the industry's 무·저해지 lapse assumption has been too low — which is
  why `lapse_be_factor = 1.0` is presented with a sensitivity rather than as a best estimate.

(krlib-term_life-r19)=

### R19 — 보험개발원 참조순보험요율, cited by document number inside [S10] (reference-rate notifications)

- Numbers as printed in [S10]: 예정 경험사망률 「보험개발원 생명장기 제2024-0250호
  (2024.01.23.)」; 예정 재해사망률 「보험개발원 생명장기 제2023-2072호(2023.12.06.)」
- Accessed: 2026-09-03, Retrieved: **no** — the notifications are not public documents; only
  their identifiers were recovered, from a carrier's own 상품요약서
- Recorded because it establishes the **provenance chain** for a Korean carrier's pricing
  mortality: 보험개발원 issues a 참조순보험요율, the carrier adjusts it, and the adjusted
  예정 경험사망률 is what the 상품요약서 prints. That the chain's middle link is not public is
  the reason `mort_table.csv` is a [std] construction and the reason no 50%-plus 장해
  incidence could be sourced for `wop_inc_rate`. It is a **life** reference rate and is
  therefore not the 장기손해보험 참조순보험요율 of [REG-R61], which **is** published and which
  `Cancer_KR_S` and `Medical_KR_S` use.

(krlib-term_life-r20)=

### R20 — 보험개발원 (KIDI) website — 참조순보험요율 / 보험통계 pages (institutional pages)

- URLs: `https://www.kidi.or.kr/` (index, retrieved), `/user/nd78654.do` (참조순보험요율,
  retrieved as an HTML shell), `/user/nd87617.do` (보험통계 서비스, not opened)
- Accessed: 2026-09-03, Retrieved: **in part** — the index and the 참조순보험요율 landing page
  returned HTTP 200 and were fetched, but neither carries the 제10회 경험생명표 announcement
  or any numeric table
- Cited only for what it does **not** contain. It is the record of the attempt: the documents
  state that neither the 경험생명표 nor a life 참조순보험요율 was retrievable from any public
  source, and this entry is what that statement is made against. No quantitative parameter
  rests on it. Compare [REG-R34], which reached the publisher's 보도자료 listing and its
  빅데이터 platform and reached the same conclusion by a different route.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that page
plain [R#] refers to its own entries, so the two schemes must never be read across. The
entries the term life documents cite, all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: the 생명보험 / 손해보험 / 제3보험 licence split and the
  definition of a 생명보험상품. Retrieved: yes (full Act, 127,346 characters).
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is a 기초서류 filed
  with the FSC and never published**, which is why every pricing-basis parameter here is
  [std] and why the margin inside a 예정 경험사망률 cannot be sized. Retrieved: yes.
- **REG-R3** — 보험업법 제120조: the statutory duty to accumulate 책임준비금, cited as a
  layer this model does not compute. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): the statutory footing of 보험개발원 and
  of the 참조순보험요율 regime whose life rates are not public. Retrieved: yes.
- **REG-R5** — 보험업법 제181조·제184조: the 선임계리사 behind the 기초서류 and the reserving.
  Retrieved: yes.
- **REG-R8** — 보험업법 시행령 제63조·제65조·제71조. Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), 본문: among much else the **기준연령 요건**
  that makes male 40 / 20년 / 1억원 the prescribed disclosure cell. Retrieved: yes (226,083
  characters, the whole 고시). **Not** this file's [R9].
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the 잔여보장요소 /
  발생사고요소 taxonomy, with the calculation delegated to the FSS Governor. Retrieved: yes.
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart anywhere else in this repository, and the reason a 무해지 lapse
  assumption is a reserve question and not only a cash-flow one. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**): the solvency layer, including the
  sub-risks the key-sensitivity list is ordered against. Retrieved: yes (article text; the
  기본요구자본 aggregation renders as an image and the 별표 22 detail was not retrieved).
- **REG-R14** — 감독규정 제7-17조~제7-19조 and 고시 제2022-53호 부칙: the commencement of the
  present regime on **2023-01-01**. Retrieved: yes.
- **REG-R16** — 감독규정 제7-60조 (생명보험의 보험상품설계): 제9호's floor requiring the death
  benefit to be at least cumulative premiums paid, **except where the premium-paying period
  ends at age 80 or below** — the exception this product falls in. Retrieved: yes.
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액): the analysis of premium
  adequacy on **최적기초율** with projected cash flows. That is the regulatory use of a
  liability cash-flow model in Korea, and it is the shape this projection takes. Retrieved:
  yes.
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): the 해약공제기간 **capped at seven
  years**, and 제4항, which permits the reduced surrender value of a 무·저해지 form precisely
  *because* premiums were calculated on a 최적해지율. Retrieved: yes (operative words in full;
  the formula display did not extract).
- **REG-R20** — 감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액: the surrender
  charge cap by formula. Retrieved: yes (1-page PDF, full text). **The same document as this
  file's [R9]**, retrieved twice independently.
- **REG-R21** — 감독규정 [별표 15] 보험가입금액의 산정: 제3호 makes a 일반사망 보장성보험 the
  **base case** of the whole schedule, against which a 제3보험 product's notional sum assured
  is scaled. Retrieved: yes (1-page PDF).
- **REG-R23** — 보험업감독업무시행세칙 (금융감독원세칙): the delegation the 책임준비금 detail
  runs through. Retrieved: yes (114,610 characters).
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the supervisor's model policy conditions, and
  therefore the reason the carrier 약관 in this set agree almost word for word. Cited by
  article throughout the specification — 제13–14조 (contestability), 제15조, 제17조 (청약
  철회), 제18조제3항 (품질보증해지), **제21조 (보험나이)**, 제26–27조, 제29조의2, 제32조,
  제33조, 부표 3. Retrieved: yes (a 492-page PDF, 441,610 characters, read in full).
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금): **Retrieved: no.** The
  K-ICS **대량해지 shock**, including the 고환급형 test, is therefore known only at second
  hand through [REG-R36] and everything resting on it is [unverified] — which matters
  precisely here, the 무·저해지 form being what the test is about.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (2024-11-07, 계리가정·할인율): the **IFRS17 주요
  계리가정 가이드라인** — a 로그-선형 lapse model converging to **0.1%** as the 원칙모형 for
  무·저해지 business, a **완납 후 최종해지율 0.8%**, and a **30% additional-lapse floor** at a
  discrete contractual event. This is the shape of `lapse_table.csv` and the upper bound on
  `renewal_decline_base`. Retrieved: yes (the 보도자료 and its 별첨). The guideline attachment
  itself was never converted from HWP, so its functional form is [unverified] at instrument
  level.
- **REG-R28** — 무(저)해지환급금 보험 상품구조 개선 (2020) and FSS 소비자경보 (2019): the
  supervisor's own statement that a 무해지 policy has nothing to lend against, which is why
  the 보험계약대출 the 약관 grants is inoperative in fact. Retrieved: yes.
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여…」 (2019-08-01): the 표준해약
  공제액 as **13 months' premium for a 보장성보험** — a rule of thumb calibrated on a
  different premium-to-cover ratio, which the documents state does **not** transfer to a
  ₩100,000,000 term policy. Retrieved: yes.
- **REG-R30** — 보험업권 자본규제 고도화 (2025-03-12) and FSS 지급여력비율 현황: K-ICS
  요구자본 ₩118.9조 at 2024-09-30 and an industry ratio of 210.8% at 2025-09-30 against a
  100% minimum. Retrieved: in part.
- **REG-R32** — 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」 (2025-09-01). Retrieved:
  in part — but the operative rule is [REG-R52], which was retrieved in full.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported by 보험매일: 평균수명 남 86.3 / 여
  90.7 and **65세 기대여명 남 23.7 / 여 27.1**, applied from April 2024. These four numbers
  are the tilt target of `mort_table.csv`. Retrieved: yes — **but it is a news article**, the
  KIDI announcement itself not being retrievable, which is the second reason the table is a
  construction.
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 빅데이터 platform): the record
  that the 경험생명표 is released as summary statistics only. Retrieved: in part.
- **REG-R36** — 보험연구원 CEO Report 03호, 노건엽·이승주 (건전성 제도): the second-hand
  source for the 대량해지 shock calibration that [REG-R26] would have carried first-hand.
  Retrieved: yes (24 pp.).
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: the
  **public** national table, whose 65세 기대여명 of 19.5 (male) and 23.7 (female) is what the
  shipped insured-lives table must sit above by a selection margin. Retrieved: yes.
- **REG-R39** — KOSIS 완전생명표 (single-year qx tables): **Retrieved: no** — distributed
  through the KOSIS interface rather than as a fetchable file, so the graduation check uses
  the briefing figures of [REG-R38] and not single-year rates.
- **REG-R46** — 보험연구원 「2026년 보험산업 전망」, 황인창 (91 pp.): 보장성보험 premium income
  ₩48.6조 (2023) → ₩55.0조 (2024) → about ₩66.2조 (2026E), against a 저축성 book in slow
  decline. Retrieved: yes. A different deck from this file's [R16].
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier regulatory disclosure: the **2026
  평균공시이율 of 2.50%** that the 약관 itself names as the discount rate for a 선지급 payment,
  and hence `accel_disc_rate`. Retrieved: in part.
- **REG-R49** — 상법 제4편 제1장 통칙 (제638조~제664조): 제638조의3 (품질보증해지), 제651조
  (고지의무위반), 제659조 (면책), 제662조 (**3년 소멸시효**). Retrieved: yes (제4편 read in
  full).
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): 제731조 (written consent),
  제732조 (the 만 15 voidness rule), 제732조의2 (gross negligence). Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (**청약의 철회**): the statutory cooling-off the
  표준약관 implements verbatim. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: 제7항 gives 사고보험금 a **separate and
  additional** ₩100,000,000 limit beside 해약환급금 and 기타지급금, and corporate
  policyholders no protection at all. Retrieved: yes.
- **REG-R57** — 소득세법 제59조의4 (특별세액공제 — 보장성보험료): the **12% credit on up to
  ₩1,000,000** of premium, and 15% for a 장애인전용보장성보험. Retrieved: yes. Cited beside
  this file's [R8].
- **REG-R59** — 상속세 및 증여세법 제8조·제34조: a death benefit as estate property where the
  deceased was in substance the payer, and as a **gift** where the premiums were another's.
  No Korean carrier document in this set addresses that triangle. Retrieved: yes.
- **REG-R60** — 한국회계기준원, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」: the
  standard in force in Korea since **2023-01-01**. **Retrieved: in part** — the release body
  returned, the 별첨 HWP carrying the standard's own text did not, so **the contract-boundary
  question this product publishes both readings of is [unverified] at instrument level.**
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: the **published** morbidity
  reference rates — a cancer incidence grid excluding C44 and C73, and a 질병입원율 grid.
  Retrieved: yes. Cited here for one contrast only: `Cancer_KR_S` can source its incidence
  basis, and this product's **mortality** cannot, the life 참조순보험요율 [R19] being
  unpublished.

---

## Provenance note

Every entry above traces to `_research/term-life.md`, which is the citation ground truth for
this product: the S# and R# numbering used here is that file's numbering, unchanged, and it
is **never renumbered** because these documents cite against it. The research file's own
numbering is not this one's — it runs to S24 and R21, and it carries `R5`, `R7`, `R10`,
`R11`, `R13`, `R14`, `R15`, `R17`, `R21` and `S24`, which this file omits as uncited, with
the reasons given at the head of this page.

What lives there and not here: the per-carrier extraction record — which fact came from
which page of which PDF; the six comparison tables behind **Variation across carriers**,
including the seven-carrier 예정 경험사망률 spread at male 40 (0.000480–0.000850), the
45-product 보험가격지수 distribution and the full 45-row disclosure table; the fetch method
for each host, including the POST parameters that make `pub.insure.or.kr` answer and the
`law.go.kr` open-API routes that do and do not return text; and the register of fetch
failures and [unverified] claims — the 경험생명표 rates, any life 참조순보험요율, the
보험업감독규정 제7-66조 body text as read at first hand, the K-IFRS 1117 standard text, the
K-ICS 대량해지 별표 22, the 정기특약 claim resting on [S23], and every expense, commission,
disability-incidence, acceleration-take-up and reinstatement figure in the Korean market,
none of which any carrier publishes.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R16]: #krlib-term_life-r16
[R19]: #krlib-term_life-r19
[R4]: #krlib-term_life-r4
[R8]: #krlib-term_life-r8
[R9]: #krlib-term_life-r9
[REG-R1]: #krlib-reg-r1
[REG-R20]: #krlib-reg-r20
[REG-R23]: #krlib-reg-r23
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R46]: #krlib-reg-r46
[REG-R49]: #krlib-reg-r49
[REG-R50]: #krlib-reg-r50
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
