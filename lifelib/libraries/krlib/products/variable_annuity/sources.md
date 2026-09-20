# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/variable-annuity.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is
per product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md` runs
its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read
across**, and on this product the clash is unusually loud: this file's **[R4]** is
보험업법 **제108조** while the library's **[REG-R4]** is 보험업법 **제176조**; this file's
**[R11]** is 감독규정 **제7-60조** while [REG-R11] is 감독규정 **제6-11조의6**; this file's
**[R12]** is 시행세칙 **별표 24** while [REG-R12] is 감독규정 **제6-11조의7**. Access date
for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 약관 (*yakgwan*, policy conditions), a 상품요약서
  (*sangpum yoyakseo*, the statutory product summary), a 상품안내장 (brochure), a 변액연금보험
  설명서 (point-of-sale explanatory document), a carrier fund-disclosure page, or the
  생명보험협회's comparative disclosure portal. On this product the [S#] set is what makes
  the **fee stack, both guarantee charges, the 해약공제 scale and the 좌수/기준가격
  arithmetic** sourced rather than assumed — and it is also what shows how far Korean
  variable-annuity designs diverge from one another, which is why the composite has to
  argue which two carriers may be joined.
- **[R#]** — a regulatory, statutory or actuarial reference that only this product needs.
  Four of the fourteen were **not retrieved at first hand** and are recorded as such.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**One source in the research file is not cited and is not listed here.** `S3`, the KDB생명
「무배당 더! 행복드림 변액연금보험」 **약관** (105 pp., V03, 판매일자 2025.06.30), was
downloaded and read selectively as corroboration that the 상품요약서 figures of [S2] summarise
a contract of the same date. **No fact in either document rests on it**: every claim about
that carrier's contract is cited to [S2], and every claim needing 약관-grade text is cited to
[S7], the one policy-conditions document read in full. Listing it would imply a load it does
not carry. Nothing else was dropped, and **no tag was added**: the two documents between them
cite S1, S2, S4–S12, R1–R14 and forty of the library's [REG-R#] entries, and every one of
those has an entry below.

**Where a [R#] and a [REG-R#] cover the same instrument, that is corroboration and not
redundancy.** [R4] and [REG-R6] are both 보험업법 제108조, retrieved by different routes —
`casenote.kr`'s mirror against the 국가법령정보센터 full-Act retrieval — so the statutory basis
of the 특별계정 was read twice from two independent renderings. [R11] and [REG-R16] are both
감독규정 제7-60조 and the pair matters in the opposite direction: [R11] was **not** retrieved
and the compulsory-GMDB clause is quoted at second hand inside [R1], while [REG-R16]
retrieved the article text, so the two together are what turns a quotation into a citation.
[R12] and [REG-R26] are both 시행세칙 별표 24 and **neither was retrieved**, which is stated
at both entries rather than at one.

Company and branded product names appear in this file and in `_research/variable-annuity.md`
and nowhere else in the library. In `product-spec.md`, `technical-notes.md` and `model.md` a
carrier is its tag alone, so a reader can always resolve who said what — here — and never has
to.

---

## Primary product sources

**Six carriers and one industry portal**, eleven documents — KB라이프 [S1] [S9], KDB [S2],
AIA [S4], ABL [S5] [S6], 교보 [S7] [S8], 미래에셋 [S10] [S11] and the 생명보험협회 공시실
[S12]. Two are 상품요약서, the statutory product summary that
must carry the 수수료 안내표 [S2] [S4]; five are 상품안내장 [S1] [S5] [S6] [S9] [S10];
one is a full 231-page 약관 [S7]; one is the point-of-sale 변액연금보험
설명서 [S8]; and two are disclosure surfaces rather than contracts [S11] [S12]. Nine were
retrieved in full and two in part.

**The composite is built on two of them and says so.** [S2] supplies the whole fee stack,
the 해약공제 scale and the fund charges; [S1] supplies the guarantee design and both
guarantee charges. They may be joined because the 해약공제 **is** the unamortised
계약체결비용 [R2] and so must come from the same carrier as the 5.17%, while a guarantee
charge is a separate instrument priced separately. The other nine documents bound the
ranges, supply the mechanics the two do not print, and provide the counter-examples that
keep the composite from being read as "the" Korean variable annuity.

(krlib-variable_annuity-s1)=

### S1 — 「무배당 VIP 변액연금보험」 상품안내장, 주식회사 KB라이프생명보험 (product brochure)

- Document: 상품안내장, 16 pp.; 준법감시인확인필-SM-2212005-1; 생명보험협회 심의필
  제2022-05589호; 인쇄일자 2023.01.01
- URL: `https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1819232770/44`
- Accessed: 2026-09-03, Retrieved: **yes** (PDF, 16 pp.; WebFetch's own text layer failed and
  the file was re-extracted locally with PyMuPDF and read in full)
- **The single most quantitatively explicit GMAB document retrieved**, and one of the
  composite's two anchors. It prints both guarantee charges as formulae — 최저사망적립액
  보증비용 **0.07%/12** a month of the separate-account value, and 최저연금적립액 보증비용
  **0.25%/12** of the separate-account value **plus 0.3%/12 of 보험료총액 for at most seven
  years** — which is where `gmdb_charge`, `gmab_charge_asset` and `gmab_charge_prem` come
  from, and where the whole "the premium component is not basis points on the fund" argument
  starts. It also supplies the eight-fund 특별계정 운용보수 table, the **mandatory 채권형
  ladder** (80% / 70% / 50% by 연금개시 전 보험기간) that `bond_floor()` implements, the
  **automatic bond rebalancing three years before annuitisation** that `derisk_amount_pp`
  implements, the 최저보증이율 ladder 1.00 / 0.75 / 0.50% of `crediting_table.csv`, the
  가입나이 and 연금개시나이 envelopes, the statement that the 해약환급금 is not guaranteed,
  the voidness of the GMAB on early exit, the 추가납입 carrying no loading, and the surrender
  and annuity illustrations at three investment returns.

(krlib-variable_annuity-s2)=

### S2 — 「무배당 더! 행복드림 변액연금보험」 상품요약서, KDB생명보험주식회사 (statutory product summary)

- Document: 상품요약서, 18 pp., 판매일자 2025.01.01
- URL: `http://www.kdblife.com/nKumhoFiles/data_pdf/product/2025/I40666_20250101_(무)더!행복드림변액연금보험_상품요약서_V01.pdf`
  — the Korean path segment must be percent-encoded for the request to succeed, and the host
  serves the file over plain HTTP
- Accessed: 2026-09-03, Retrieved: **yes** (first attempt HTTP 503; second returned the PDF,
  18 pp., re-extracted locally with PyMuPDF and read in full)
- The composite's other anchor and **the reference document for what a Korean variable-annuity
  fee schedule actually looks like**. It carries the complete 수수료 안내표 — 계약체결비용
  **5.17%** of the 기본보험료 for ten years, 계약관리비용 **3.50%** in payment and **1.33%**
  after 납입완료, 위험보험료 **0.004%–0.011%**, 특별계정 운용보수 by fund (0.40% / 0.60%),
  증권거래비용 및 기타비용, 기초펀드 보수·비용, both guarantee charges, the 연금수령기간 중
  계약관리비용, and the seven-year **해약공제 scale** — 71 / 59 / 47 / 36 / 24 / 12 / 0 만원,
  whose linear-in-the-amount fit `C × (7 − k) ÷ 7` gives the **C = ₩830,000** that is the
  `surr_charge` anchor. ₩830,000 is that fitted intercept and **not** a figure the document
  prints; the published first-year amount is ₩710,000. Everything in `charge_table.csv` that
  is not [S1], [S4] or [R1] is this document. It also prints the cumulative separate-account
  contribution falling from ₩32,877,360 at ten years to ₩32,393,520 at twenty — the
  observable that the 계약관리비용 for the post-premium period is collected *during* the
  premium period — and the full **GLWB**
  apparatus (7%/6% simple roll-up 최저연금기준금액, sex- and age-banded 기본지급률, 장기유지
  and 투자실적 가산율) which the model documents and does not implement.

(krlib-variable_annuity-s4)=

### S4 — 「무배당 AIA 여유+ 변액연금보험」 상품요약서, AIA생명보험주식회사 (statutory product summary)

- Document: 상품요약서, 18 pp.; 「이 상품요약서는 2026년 1월 1일부터 적용됩니다」
- URL: `https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/saving/summary/AIA_kr_Form107_20260101.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (PDF, 18 pp., re-extracted with PyMuPDF, read in
  full)
- **The current-generation unguaranteed shape**, and the top of two ranges. It is explicit
  that 「연금개시시점의 최저계약자적립액 미보증」 — no GMAB and no GMAB charge — while the
  GMDB survives at 연 0.05%, which is what model point 3 (미보증형) represents and what makes
  the elective GMAB a live design question rather than a historical one. It carries the
  highest retrieved 계약체결비용 (6.12% for ten years, then zero) and the highest retrieved
  first-year 해약공제 (28.1%, ₩1,010,000 on the anchor cell, fitting `C = ₩1,180,000`), so it
  brackets the top of both.
  Its **proportional 연금수령기간 중 계약관리비용 of 0.5% of the 연금 연액** is the form
  `annuity_charge_pp` takes, chosen over [S2]'s per-구좌 monthly form because it is scale-free.

(krlib-variable_annuity-s5)=

### S5 — 「(무)투자에강한변액연금보험(최저연금적립액 미보증형)2404」 상품안내장, ABL생명보험주식회사 (product brochure)

- Document: 상품안내장, 20 pp.; 생명보험협회 심의필 제2025-06233호; 「2025년 10월 1일 제작」
- URL: `https://www.abllife.co.kr/cms/prdt/vains/__icsFiles/afieldfile/2025/09/29/(무)투자에강한변액연금(최저연금적립액_미보증형)2404_20251001.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (693 KB PDF, 20 pp., re-extracted with PyMuPDF,
  read in full)
- **The most recent retrieved document** and the fullest description of the fund-management
  machinery: a 49-fund menu with per-fund 운용보수 broken into 운영보수 / 투자일임보수 /
  수탁보수 / 사무관리보수, a **펀드자동전환옵션** (target-return de-risking at 110–200% in 10%
  steps), a **펀드자동재배분** (3- or 6-month rebalancing with a 60% floor on bond + MMF), the
  정기중도인출서비스, and a 해약공제 scale running off in exact sevenths — which is the
  evidence that the run-off is linear **in the amount** and not in the ratio. It supplies the
  two-business-day pricing lag, the 연금개시 전/후 보험기간 definitions, the 보증기간
  instalments payable on death, and the raised **예금자보호 limit of ₩100,000,000 (1억원)**.
  Its ₩1,077,000 해약공제 is the middle of the three retrieved scales.

(krlib-variable_annuity-s6)=

### S6 — 「(무)하모니변액연금보험2404」 상품안내장, ABL생명보험주식회사 (product brochure)

- Document: 상품안내장, 32 pp.; 생명보험협회 심의필 제2025-06232호; 제작 2025.10.01
- URL: `https://www.abllife.co.kr/cms/prdt/vains/__icsFiles/afieldfile/2025/09/29/(무)하모니변액연금2404_20251001.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (908 KB PDF, 32 pp., re-extracted with PyMuPDF,
  read in full)
- **The single most important counter-example to "the guarantee is a basis-point charge."**
  Its 경과확정보증액 ratchets monthly, the guarantee ratio runs 100%→130% with the term, and
  the guarantee is funded not by a fee but by a CPPI-style Auto Balancing between a
  growth-asset fund and a safe-asset fund plus an **irreversible automatic transfer to the
  일반계정** at a 1.75% floor when the growth weight hits zero. The model documents this design
  and implements none of it, for the stated reason that a deterministic path cannot exercise
  a CPPI rule meaningfully. Two facts the model does use come from here: the 91.3% premium
  allocation on the anchor cell, one of the three independent readings the modelled 91.33%
  is corroborated by — `check_prem_alloc()` itself asserts the ratio against the model's own
  `1 − loading_rate()` and not against the published figures — and the **surrender-value
  illustration showing zero at three months on an account of ₩821,751**, which is the
  published shape `cv_pp(0) = cv_pp(1) = cv_pp(2) = 0` reproduces. It also states the
  transfer of the whole 계약자적립액 to the 일반계정 at 연금개시 that `av_transfer`
  implements.

(krlib-variable_annuity-s7)=

### S7 — 「미리 보는 내 연금 무배당 교보First변액연금보험Ⅱ」 보험약관, 교보생명보험주식회사 (full policy conditions)

- Document: 보험약관 booklet, **231 pp.**, comprising the main contract (pp. 16–114),
  무배당 연금전환특약Ⅲ, 무배당 교보장기간병연금전환특약, 지정대리청구서비스특약,
  변액보험 펀드추가서비스특약 and an appendix of the statutes the policy cites; the copy
  retrieved is 하나은행's contract-document mirror of the bancassurance edition
- URL: `https://image.kebhana.com/cont/download/insdocument/provide/L05184361_agree.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (1.9 MB PDF, 231 pp., re-extracted with PyMuPDF;
  제2조, 제36조–제46조, 제50조, 제51조 and 제63조 read verbatim, the list the research file's
  own entry records). The research file additionally pins **제3조** (보험금의 종류),
  **제6조** (성과보너스) and **제7조** (장기유지 운용보수 환급) in its body, and those three
  are cited here on that footing; **no other article of this document may be pinned to**.
- **The only policy-conditions-grade document read in full in this session**, and the source
  of every verbatim clause the documents quote. Articles the documents pin to it: **제2조
  (용어의 정의)**, which defines the 월공제액 and separates it from the charges deducted at
  premium payment — the two-deduction-point structure the whole model turns on; 제36조
  (계약자적립금의 계산); 제37조 (펀드의 운용 및 평가); 제38조 (펀드의 유형);
  제39조–제41조 (펀드 선택·변경, 자동이전·자동재배분, 평균분할투자), which is where the
  **two-business-day pricing lag** is stated; 제42조–제46조 (특별계정 자산평가, **좌수 및
  기준가격**, 제비용, 폐지, 공지), where 제43조제2호 puts the 운용보수 **inside the 기준가격**
  and so makes it a factor on the growth rather than a unit cancellation; **제50조
  (해지환급금)**, whose 제3항 states that the surrender value carries no minimum guarantee and
  that the GMAB is void on 해지; **제51조 (계약자적립금의 인출)**, whose 제8항 is the
  proportional guarantee re-basing on a 중도인출; and 제63조 (예금보험에 의한 지급보장).

(krlib-variable_annuity-s8)=

### S8 — 「교보변액연금보험(무배당)[B] 고객님을 위한 변액연금보험 설명서」, 교보생명보험주식회사 (point-of-sale explanatory document)

- Document: 변액연금보험 설명서, 4 pp.; 준법감시인확인필 1-2312-10; the copy retrieved is
  hosted by 신한은행
- URL: `https://img.shinhan.com/sbank2016/seol/20211227000001350004LC000030.PDF`
- Accessed: 2026-09-03, Retrieved: **yes** (296 KB PDF, 4 pp., re-extracted with PyMuPDF,
  read in full)
- The document required by the 금융소비자 보호에 관한 법률 at the point of sale. It prints the
  **실적배당 종신연금 월 지급률 as a closed-form formula** — the only closed-form annuity rate
  found in any retrieved Korean variable-annuity document, and the reason the specification
  can describe the GLWB payout precisely while declining to implement it — together with the
  ratcheting definition of the 연금기준금액 and, in the carrier's own words, the five
  deductions that stand between the premium and the fund. It is one of the four documents
  behind the statement that the GMAB is void on death before annuitisation.

(krlib-variable_annuity-s9)=

### S9 — 「투자의 힘 무배당 KB 변액연금보험Ⅱ」 상품안내장, 주식회사 KB라이프생명보험 (product brochure)

- Document: 상품안내장, 16 pp.; PDF creation metadata 2022-11-18 to 2022-12-22
- URL: `https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1228994/44`
- Accessed: 2026-09-03, Retrieved: **yes** (906 KB PDF, 16 pp., re-extracted with PyMuPDF,
  read in full)
- **The elective, mid-term GMAB.** The contract is sold unguaranteed, converts automatically
  to 보증형(중도선택형) at the end of the premium period, and lets the policyholder switch the
  guarantee on and off an unlimited number of times at 연 0.85% of the separate-account value,
  with the floor set at the account value two business days after election and ratcheted up
  monthly thereafter. It also carries the 성과보너스 at 120/140/160/180/200% return and the
  forced 채권형II 50% + EMP AI형 50% allocation on electing the guarantee. It is the clearest
  evidence that **the guarantee is an option the policyholder may hold or not**, which is why
  `gmab_flag` is a model-point column rather than a model-wide constant, and it is one of the
  documents establishing that 조기연금개시 is available only where the guarantee is out of the
  money.

(krlib-variable_annuity-s10)=

### S10 — 「미래를 보는 변액연금보험(무)202004」 상품안내장, 미래에셋생명보험주식회사 (product brochure)

- Document: 상품안내장, 20 pp., 제작일자 2020.04
- URL: `https://pdf.miraeassetlife.com/directDownloadDocFile.do?Ax=…` — a **one-time signed
  download token**; the token used on 2026-09-03 is recorded in the research session log and
  is not expected to remain valid
- Accessed: 2026-09-03, Retrieved: **yes** (664 KB PDF, 20 pp., re-extracted with PyMuPDF,
  read in full)
- **The three-variant chassis** — 최저연금미보증형 / 최저연금보증형 1+α / 최저연금보증형 2+α
  — with a roll-up guarantee base credited at 연복리 1.0% or 2.0%, a GLWB rather than a GMAB,
  guarantee charges of 연 0.30% and 0.35% on top of a 연 0.05% GMDB charge, and equity caps
  that tighten as the guarantee rises (80% unguaranteed, 60% for 1+α, a single 글로벌MVP30
  fund for 2+α). It is the clearest retrieved statement that **the guarantee level and the
  investment freedom are traded against each other**, which is the qualitative fact behind the
  mandatory 채권형 ladder the model does implement. It is also one of the two documents
  bounding the fund-menu size at 5 to 51 funds.

(krlib-variable_annuity-s11)=

### S11 — 변액보험 공시 (변액펀드MAP), 미래에셋생명보험주식회사 (carrier fund disclosure)

- URL: `https://life.miraeasset.com/micro/disclosure/variable/PC-HO-080501-000000.do`
- Accessed: 2026-09-03, Retrieved: **in part** (server-rendered HTML read; the page is a fund
  browser and only the first fund's panel was returned)
- Establishes the shape of the mandated daily disclosure — 기준가격, 설정일 and 1/3/6-month,
  1/3/5-year, cumulative and annualised returns per fund. The one panel returned was
  가치주식형, 설정일 2012.12.26, **기준가격 904.24원** against the statutory 1,000.00 opening
  price, 연평균 −9.58%: a fund **below its launch value after fourteen years**. Together with
  [R10] it is the whole of the retrieved evidence on realised Korean variable-fund returns,
  and it is cited in `return_scenario.csv` and in the key-sensitivity list to establish
  precisely that **no return assumption in this model can be sourced** — no as-of date came
  back with the panel, so even the figures returned are dated only by the access date.

(krlib-variable_annuity-s12)=

### S12 — 변액보험 상품비교공시 / 시장현황, 생명보험협회 공시실 (industry comparative disclosure portal)

- URLs: `https://pub.insure.or.kr/` and
  `https://pub.insure.or.kr/compareDis/variableInsrn/mrktStts/list.do`
- Accessed: 2026-09-03, Retrieved: **in part** (both pages returned server-rendered HTML and
  the menu structure and the list of quarterly statistics files were read; the statistics
  themselves live in linked PDFs — 「26_2분기 상품유형별 통계.pdf」 and others — and a direct
  request for one was refused with 「적절하지 않은 경로를 통한 요청입니다」)
- **Establishes what is public**, which on this product is a load-bearing negative. The portal
  carries 보장성/저축성 상품비교, 시장현황, 상품별 펀드운영현황, 신상품정보, 상품별
  과거수익률 and 펀드현황 for 변액보험, and [R2] confirms that a savings-type variable product
  must publish its 수수료 안내표 either here or in the 상품요약서. What it does **not** carry
  is any 적용해지율, any unit expense cost or any lapse table: the 사업비 disclosure is of
  *charges*, not of *costs*. Those two absences are why `lapse_table.csv` and the two expense
  rows of `charge_table.csv` are [std], and this entry is the citation for the absence.

---

## Regulatory and actuarial references

Fourteen entries. **Ten were retrieved at first hand, one in part and three not at all** —
[R11], [R12] and [R14] are known only as quoted inside documents that were retrieved, and each
says so at its own entry. That distribution is itself a finding about this product: the
instruments that govern the **guarantee** — 제7-60조제7호 and 별표 24 — are the two that could
not be opened.

(krlib-variable_annuity-r1)=

### R1 — 「변액연금 최저보증 및 사업비 부과 현황 조사」, 조사자료집 2018-1, 보험연구원 (research monograph)

- Author 김세환; 2018년 2월; 117 pp., with an English abstract "GMxB and Charges in Korean
  Variable Annuities Market"; survey base **all 36 variable annuity products on sale at
  2017-05-31, from the 18 of Korea's 25 life insurers then writing the line**
- URL: `https://www.kiri.or.kr/pdf/전문자료/KIRI_20180427_111032.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (1.9 MB PDF, 117 pp.; WebFetch's text layer was
  unusable and the file was re-extracted with PyMuPDF; 요약, Ⅱ 성장추이, Ⅲ 최저보증 운영 현황,
  Ⅳ 최저보증리스크의 통제와 관리 and Ⅴ 사업비 부과 및 모집수수료 지급 현황 read in full)
- **The single richest quantitative source on this product.** It supplies the guarantee
  taxonomy (GMDB / GMAB / GMWB / GLWB / GMIB); the four ways a guarantee level is set —
  premium refund, step-up, ratchet, roll-up — with a fifteen-year worked example; the
  product-by-product census of which of the 36 guaranteed what; the 2014 감사원 finding that
  led to the GMAB becoming **optional in April 2016**; the risk-control devices insurers
  actually use, including the **동적해지율** convention the model deliberately does not
  implement; the 별표 24 보증준비금 tables and the 보증위험액 최저한도 table at second hand;
  the industry premium-allocation band 「납입보험료의 5~15%를 … 차감한 후 85~95%만 투자」 that
  `check_prem_alloc()` is bounded by; the market-mean 해지공제율 by duration [R1 <표 Ⅴ-2>](#krlib-variable_annuity-r1);
  the **모집수수료율 by policy year [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1)** that is `comm_yr1`–`comm_yr5`; the
  seven-year-persistency-below-30% sentence that `lapse_table.csv` is calibrated to; and the
  130%-of-premiums 일반계정 전환 offer. It is dated — the census is 2017 — and every figure
  taken from it is labelled with that date.
- **Caveat that matters, and that the documents observe.** Its <표 Ⅲ-1> prints a column headed
  「연간보증비용」 with ranges GMDB 0.04–0.07%, GMAB 기납입보험료 0.56–0.98% and so on.
  Reconstructing them from the 별표 24 tables reproduced later in the same report shows they
  are **exactly the reserve standard's floors, not observed carrier charges**. They must not
  be quoted as market guarantee charges, and are not: the observed charges in this model come
  from [S1] [S2] [S4] [S9] [S10].

(krlib-variable_annuity-r2)=

### R2 — 「변액보험의 이해와 판매」 2024 (변액보험판매자격시험 교재), 생명보험협회 (industry textbook)

- 자격시험센터, 2024 edition, 280 pp.; 제1장 금융시장의 이해, 제2장 생명보험의 이해,
  제3장 변액보험의 이해, 제4장 보험공시 및 예금자보호제도
- URL: `https://exam.insure.or.kr/upload/attach/pbt/notice/20240105_1704444400640.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (2.3 MB PDF, 280 pp., re-extracted with PyMuPDF;
  the 변액보험의 이해 chapter, the 해약환급금 and 책임준비금 sections of 제2장, the tax
  section and the whole of 제4장 read)
- The **authoritative plain-language statement of the mechanics**, and the textbook every
  Korean variable-annuity seller must pass an examination on. It gives the cash-flow identity
  the model is built on — 특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중
  계약유지비용 + 기타비용) = 순보험료 + **납입 후 계약유지비용** — whose second line is the
  reason the monthly deduction *rises* at 납입완료; the order and timing of every deduction;
  the 좌수/기준가격 arithmetic; the fund-allocation ratios observed by premium term; the
  April 2016 change making the GMAB optional; the **three illustration returns** a Korean
  variable illustration must show, which fix `return_scenario.csv`'s three scenarios; the
  statement that the GMDB top-up is met from the 일반계정 보증준비금 and not from the fund;
  the extinguishment of death cover at 연금개시; the disclosure regime; the licence and
  적합성 진단 requirements; and the deposit-protection carve-out.

(krlib-variable_annuity-r3)=

### R3 — 「변액보험 판매 미스터리쇼핑 결과 및 관련 소비자 유의사항을 안내합니다」, 금융감독원 (supervisory press release)

- 소비자피해예방국; 보도 2026.3.24.; 5 pp.
- URL: `https://kiri.or.kr/PDF/weeklytrend/20260406/trend20260406_5.pdf` — retrieved as
  reproduced in the 보험연구원 주간보험동향 of 2026-04-06; the FSS's own board was not opened
- Accessed: 2026-09-03, Retrieved: **yes** (479 KB PDF, 5 pp., re-extracted with PyMuPDF, read
  in full)
- **The current market and conduct picture**, and the freshest quantitative datum in the file:
  2025 변액보험 초회보험료 **₩2.89조, up 46.2%** on 2024's ₩1.97조; 2025 변액보험 민원
  **1,308건, about 9%** of all life-insurance complaints. The mystery-shopping exercise ran
  September–November 2025 over 9 of 22 life insurers, overall grade 「양호」, with the weakest
  items being the explanation of **변액보험의 자산운용 방식** and of the 위법계약해지권. Its
  consumer-guidance half states the four points a Korean regulator considers material — the
  principal is not protected, the whole premium does not reach the fund, the 적합성 진단 must
  precede any recommendation, and the customer manages the funds — which is the framing
  `product-spec.md` adopts for the whole product.

(krlib-variable_annuity-r4)=

### R4 — 보험업법 제108조 (특별계정의 설정·운용) (statute)

- URL: `https://casenote.kr/법령/보험업법/제108조` — CaseNote's mirror of the 국가법령정보센터
  text; the 국가법령정보센터 friendly URL returned only the page shell
- Accessed: 2026-09-03, Retrieved: **yes** (server-rendered HTML; article text and amendment
  history read)
- The statutory basis of the whole model. 제1항 permits a 특별계정 「그 준비금에 상당하는
  자산의 전부 또는 일부를 그 밖의 자산과 구별하여 이용하기 위한」, and names **변액보험계약**
  as one of four qualifying classes; **제2항** requires separate-account assets to be
  accounted for separately from other special accounts **and** from all other assets, which is
  the legal fact `net_cf_gen` / `net_cf_sep` exist to represent; 제3항 permits distribution of
  separate-account profits; 제4항 delegates asset management, valuation and comparative
  disclosure to Presidential Decree. Corroborated by [REG-R6], retrieved by a different route.

(krlib-variable_annuity-r5)=

### R5 — 보험업법 제106조 (자산운용의 방법 및 비율) (statute)

- URL: `https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=1000734924&chrClsCd=010202&lsId=001532&print=print`
  — the `print=print` form returns text where the friendly `/법령/` form does not
- Accessed: 2026-09-03, Retrieved: **yes** (시행 2025-01-31, 법률 제20436호)
- The asset-concentration limits, set **separately for the general account and for special
  accounts**, the special-account limits being the higher of the two. The general-account
  figures came back (3% credit exposure to one person, 7% of one corporation's bonds and
  shares, 25% real estate); **the special-account values did not**, so every statement in
  `product-spec.md` about the separate-account limits themselves is tagged **[unverified]**
  against this entry. Nothing in the model depends on them.

(krlib-variable_annuity-r6)=

### R6 — 변액보험(PBT) 시험규정, 생명보험협회 자격시험센터 (examination regulations)

- URL: `https://exam.insure.or.kr/vrb/pbt/schd/legal`
- Accessed: 2026-09-03, Retrieved: **yes** (server-rendered HTML read)
- The statutory hooks for the sales licence — **보험업법 제83조**, **시행령 제56조** and
  **감독규정 제5-4조** — and the mechanics of the qualification: candidates limited to
  solicitors under 제83조, pass mark 「100점 만점에 70점 이상」, 40 questions in 60 minutes.
  It supports the specification's statement that this product may be sold only by a
  변액보험판매관리사, which [S1] prints on its own cover. It does **not** state the
  continuing-education requirement; that comes from [R2].

(krlib-variable_annuity-r7)=

### R7 — 「불합리한 보험 사업비와 모집수수료를 개편하여 소비자의 환급률을 높이고 보험료 인하를 유도하겠습니다」, 금융위원회 (policy press release)

- 보험과, 2019년 8월 1일
- URL: `https://fsc.go.kr/no010101/73816`
- Accessed: 2026-09-03, Retrieved: **yes** (server-rendered HTML read)
- The 2019 reform that reshaped Korean expense loadings: savings-level expenses on the savings
  component of protection products cut to about 70%, renewal-period contract costs to 70% of
  the initial level, the **추가납입 limit cut from 2× to 1×**, and commission controls from
  **January 2021** requiring that first-year commission plus surrender value not exceed
  premiums paid. The 추가납입 cut is the one live conflict in the file: **every** variable
  annuity retrieved here — including three produced in 2025 — still publishes a 200%
  additional-premium limit, so either the measure did not carry across to variable annuities
  or it was reversed. The model uses `addl_prem_cap_ratio = 2.0` and the documents record the
  conflict rather than resolving it. Corroborated by [REG-R29].

(krlib-variable_annuity-r8)=

### R8 — 「보험자본건전성 선진화 추진단」 제10차 회의 보도자료, 금융위원회 (policy press release)

- 2022년 8월 25일
- URL: `https://fsc.go.kr/po010101/78367`
- Accessed: 2026-09-03, Retrieved: **yes** (server-rendered HTML read)
- The IFRS 17-era treatment of the two reserves this product turns on. **해약환급금준비금**:
  where the fair-valued liability falls below the contractual surrender obligation, the
  shortfall is reserved. **보증준비금**: built from the existing guarantee reserve carried as a
  liability **plus the guarantee fees still to be collected** — which is the construction that
  makes the model's `gmab_charges` stream a reserve input rather than income, and the reason
  the documents refuse to read the charge/cost gap as profit. Both move into statutory reserves
  inside retained earnings from **2023**, restricting distributable profit. The release does
  not name the amended article numbers; [REG-R10] and [REG-R11] do.

(krlib-variable_annuity-r9)=

### R9 — 「2025년 보험산업 전망」, 보험연구원 (research institute forecast)

- 발표 황인창; 2024.10.10; seminar deck, 78 pp.
- URL: `https://www.kiri.or.kr/pdf/전문자료/smn_20241010.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (2.1 MB PDF, 78 pp., re-extracted with PyMuPDF; the
  연금 및 변액보험, 종목별 초회보험료 and 부록 변액보험 slides read)
- **변액보험 수입보험료 in 조원 with year-on-year growth**: 2021 17.9 (+4.1%), 2022 12.7
  (−29.0%), 2023 12.2 (−4.0%), 2024(E) 11.6 (−4.9%), 2025(F) 10.1 (−12.7%), with a −45.9%
  첫회보험료 forecast for 2025. It names **「최저보증이율의 하락」** as a driver of falling
  demand for guaranteed variable annuities. The specification cites it beside [R3] as a
  standing warning against any Korean variable-annuity volume projection: the forecast of a
  45.9% fall was followed by a 46.2% rise.

(krlib-variable_annuity-r10)=

### R10 — 「변액보험 펀드 연환산 수익률, 국내형 71.32%·해외형 44.61% 최고」, 보험저널 (news article)

- 2026-05-13, reporting 생명보험협회 disclosure data as at 2026-04-30
- URL: `https://www.insjournal.co.kr/news/articleView.html?idxno=31404`
- Accessed: 2026-09-03, Retrieved: **yes** (article read). **Secondary — a trade news article,
  not a primary document**; the underlying association disclosure was not opened.
- The **only** source in the file for realised Korean variable-fund returns, and it reports
  only the top of a cross-sectional distribution: domestic equity 71.32% / 49.01% / 48.04%,
  overseas equity 44.61% / 44.16% / 43.08%, annualised. It is cited in `return_scenario.csv`
  and in the key-sensitivity list for exactly one purpose — to establish that **any return
  assumption in this model must be [std] and cannot be sourced to it**.

(krlib-variable_annuity-r11)=

### R11 — 보험업감독규정 제7-60조 (생명보험의 보험상품설계 등) 제7호 (supervisory regulation)

- URL: `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196`
- Accessed: 2026-09-03, Retrieved: **no.** The 국가법령정보센터 page returned the navigation
  shell only, though it did confirm the version on display as 시행 2023-03-02, 금융위원회고시
  제2023-10호. The FSC's own attachment endpoint returned a different document (a
  규제영향분석서); the easylaw.go.kr download and the ulex.co.kr mirror both failed to reach
  제7편.
- The clause that makes the **GMDB compulsory**: 「변액보험 및 금리연동형보험(연금보험을
  제외한다)의 경우 최저사망보험금 등을 설정하여야 한다」, quoted verbatim at two places in
  [R1] and double-sourced within it. It is why all 36 products in the 2017 census carried a
  GMDB and why `gmdb_charge` has no switch beside `gmab_flag`. **The article number is sound
  and any wider reading of 제7-60조 is [unverified] against this entry** — [REG-R16] retrieved
  the article text and is the citation that closes the gap.

(krlib-variable_annuity-r12)=

### R12 — 보험업감독업무시행세칙 <별표 24> 보증준비금 산출기준 (supervisory rules, annex)

- URLs tried: `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687` and
  `https://lbox.kr/v2/statute-admin/보험업감독업무시행세칙`
- Accessed: 2026-09-03, Retrieved: **no** (law.go.kr returned the shell; lbox.kr returned
  HTTP 403)
- The 보증준비금 standard, known **only as reproduced in [R1]** (tables Ⅳ-7(a), Ⅳ-7(b), Ⅳ-8):
  the reserve is the greater of a stochastic **CTE(70)** figure — 「사망률, 해지율,
  자산이익률(1,000개)을 이용하여 만기까지 장래 예상되는 순손실액을 현가로 환산한 상위 30%
  평균 금액」 — and a standard factor tabulated by 보험종류 × 최저보증종류 × 보증수준 ×
  주식비중한도. This is the instrument the model's guarantee section measures itself against
  and explicitly does **not** compute; every factor figure in `product-spec.md`'s regulatory
  section is at second hand and tagged **[unverified]**. Search results indicate the annex is
  invoked by 감독규정 제6-11조 제10호 and computed under 시행세칙 제4-15조; neither article was
  retrieved. **[REG-R26] also failed to retrieve it**, from the other research pass.

(krlib-variable_annuity-r13)=

### R13 — 보험업법 시행령, 특별계정 관련 조문 (제52조·제53조) (Presidential Decree)

- URL: `https://www.law.go.kr/LSW//lsSideInfoP.do?lsiSeq=266041&joNo=0053&joBrNo=00&docCls=jo&urlMode=lsScJoRltInfoR`
- Accessed: 2026-09-03, Retrieved: **in part** — the page identified the instrument (시행
  2024-10-25, 대통령령 제34960호) but returned the navigation frame rather than the article
  text
- From search-result summaries only, and therefore **[unverified]**: 제52조 requires a separate
  account per class of contract; 제53조 governs special-account asset-management ratios, bars
  the insurer from exercising voting rights on shares held in a separate account, and includes
  prohibitions on **guaranteeing a return in advance on a 변액보험계약** and on moving assets
  between the general account and a separate account. That last pair would matter to this model
  if it were relied on; it is not, and `product-spec.md` tags every statement about 제53조
  [unverified] rather than dropping it, because the prohibition on advance return guarantees is
  the doctrinal reason a Korean minimum guarantee is a **benefit floor** and not a
  credited-rate floor.

(krlib-variable_annuity-r14)=

### R14 — 금융소비자 보호에 관한 법률 제17조 (적합성원칙) and 제18조 (적정성원칙) (statute)

- URL: not fetched directly
- Accessed: n/a, Retrieved: **no** — cited here only as reported in [R2] and [R3], both of
  which were retrieved
- [R2] states that recommending a variable contract to an 일반금융소비자 engages 제17조, that
  selling without recommending engages 제18조, and that the information gathered must include
  연령, 재산상황, 보험계약 체결의 목적, product experience and understanding. [R3] adds that
  the **위법계약해지권** arises where the seller breaches 적합성원칙, 적정성원칙, 설명의무,
  불공정영업행위 금지 or 부당권유행위 금지 — the right that returns the **계약자적립액** rather
  than the 해약환급금, which is the one place in this contract where a conduct rule changes a
  benefit amount. The article numbers are second-hand but come from two independently retrieved
  documents. [REG-R51] carries 제46조 of the same Act at first hand.

---

## Cross-product references ([REG-R#])

The forty entries of `references/regulatory-and-actuarial-references.md` that
`product-spec.md` and `technical-notes.md` cite, in short form, so a reader of this page alone
can resolve every tag. The full entries — publisher, URL, retrieval method, quoted text —
are in that file, whose numbering is frozen and is **not** this file's.

- **REG-R2** — 보험업법 제5조 등 (기초서류): the 산출방법서 is a filed 기초서류 and is **not
  published**, which is the hard boundary on how far a public-source reconstruction of the
  account recursion can go. Retrieved: yes.
- **REG-R3** — 보험업법 제120조 (책임준비금): the reserve requirement and its delegation to the
  FSS Governor. Retrieved: yes.
- **REG-R5** — 보험업법 제181조·제184조 (보험계리, 선임계리사): the professional frame the
  기초서류 verification sits in. Retrieved: yes.
- **REG-R6** — 보험업법 제108조 (특별계정): the statute enabling the separate account. **The
  same instrument as this file's [R4]**, retrieved by a different route. Retrieved: yes.
- **REG-R7** — 보험업법 시행령 제1조의2 (보험상품): places 연금보험계약 in 생명보험상품, which
  is this product's regulatory class. Retrieved: yes.
- **REG-R8** — 보험업법 시행령 제63조·제65조·제71조: the 지급여력비율 100% floor and the
  **30-day pre-sale filing of the 보험상품신고서** with 기초서류 verified by the 선임계리사.
  Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), full text: the 고시 whose full-text search
  returns **zero occurrences of 예정이율**, which is the evidence behind the model's decision
  not to carry a `prem_int_rate`. Retrieved: yes (226,083 characters).
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, **보증준비금**): 제6-11조의5 requires a
  guarantee reserve inside retained earnings for expected losses on benefit guarantees, with
  the calculation delegated to 시행세칙 별표 24. This is the reserve the model does not compute
  and says so. Retrieved: yes (article text; the calculation is delegated and not in the 고시).
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart anywhere else in this repository; its 제2항 test explicitly brings in
  **특별계정부채 limited to the 계약자적립금 of 제6-26조제1항제1호** — that is, this product's
  account value. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**): the solvency layer, whose
  life-and-long-term-health module carries **해지위험액** and **사업비위험액** among seven
  shock-based sub-risks. Retrieved: yes (the 기본요구자본 aggregation renders as an image).
- **REG-R14** — 감독규정 제7-17조~제7-19조 and 고시 제2022-53호 부칙: the **2023-01-01**
  commencement of the present regime, and the 적기시정조치 ladder below 100%. Retrieved: yes.
- **REG-R15** — 감독규정 제5-6조, **제5-7조**, 제6-26조 (**특별계정**): 제5-6조제1항제3호 makes
  a 변액보험계약's separate account **mandatory**, and **제5-7조 lists exhaustively the
  transfers permitted across the boundary** — the article `net_cf_gen` and `net_cf_sep` are
  written against and `check_net_cf()` asserts. The most load-bearing [REG-R#] on this product.
  Retrieved: yes.
- **REG-R16** — 감독규정 제7-60조 (생명보험의 보험상품설계): **제7호 makes the GMDB
  compulsory** on every variable contract. Retrieved: yes — and it is the entry that closes the
  gap left by this file's unretrieved [R11].
- **REG-R18** — 감독규정 제7-64조·제7-65조 (**산출방법서, 계약자적립액**): 제7-64조 is why the
  recursion's exact form is not public; **제7-65조제2항 expressly permits an annualized-premium
  basis** for the 계약자적립액, a permission the model does not use and says so. Retrieved: yes
  (the two 계약자적립액 accrual formulas did not extract).
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): 제1항제1호 floors the surrender value at
  **zero**, which is the statutory floor `cv_pp` applies; 제1항제2호 caps the 해약공제기간 at
  **seven years**; and **제4항제1호 excludes 변액보험 from the 무·저해지 dispensation**, so the
  cliff-shaped surrender curve of this library's protection products cannot appear here.
  Retrieved: yes (operative words in full; the formula display did not extract).
- **REG-R20** — 감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액: the
  **표준해약공제액** that `surr_chg_cap_pp()` computes — 5% of the 연납순보험료 times a
  해약공제계수 equal to the premium term capped at 12. ₩1,643,940 on the anchor cell, binding
  on model points 6, 7 and 10. Retrieved: yes (1-page PDF, full text including all seven
  notes).
- **REG-R21** — 감독규정 [별표 15] 보험가입금액의 산정: cited for what it does **not** settle —
  the notional sum assured of a variable annuity for 별표 15 purposes was not worked in any
  retrieved document, and Note 6 to 별표 14's netting of the discounted acquisition cost off
  the cap was not worked either, so the exact residual cap is **[unverified]**. Retrieved: yes.
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조 (수수료, 공시, 신고): **제7-51조** requires
  pre-notification of a 저축성보험 that does not spread at least 50% of its acquisition cost
  evenly over the premium term (70% bancassurance, 100% online) — the rule that bounds how
  front-loaded this product's 계약체결비용 may be. Retrieved: yes.
- **REG-R23** — 보험업감독업무시행세칙: the delegation the 표준약관 and the reserve detail run
  through. Retrieved: yes (114,610 characters).
- **REG-R24** — 시행세칙 [별표 27] 공시기준이율 산출 기준: the formula behind the **공시이율**
  the payout phase credits, parameterized by each carrier off its own 운용자산이익률 — which is
  why holding the rate level in `crediting_table.csv` is a [std] simplification. Retrieved: yes
  (two weight formulas render as images).
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the supervisor's model policy conditions, and
  therefore why the carrier 약관 in this set agree almost word for word. Cited by article
  throughout: **제21조 (보험나이)** — the age basis the whole model is indexed on —
  제13조·제14조 (계약 전 알릴 의무), 제15조, 제17조 (청약철회), 제18조제3항 (품질보증해지),
  제22조, 제26조·제27조 (실효·부활), 제29조의2 (위법계약해지), 제32조, 제33조. Retrieved: yes
  (a 492-page PDF read in full).
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and **[별표 24] (보증준비금 산출기준)**:
  **Retrieved: no.** Every 보증준비금 factor in `product-spec.md` is therefore second-hand
  through [R1] and carries [unverified] — **the same failure as this file's [R12]**, recorded
  in both research passes. On this product that is the most consequential retrieval gap in the
  file, the annex being the instrument the guarantee is actually reserved under.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (계리가정·할인율): the IFRS17 계리가정 가이드라인,
  whose lapse-model functional form is **[unverified]** at instrument level, the 별첨 never
  having been converted from HWP. Cited here for the limit, not for a parameter. Retrieved: yes
  (the 보도자료 and its 별첨).
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여…」 (2019-08-01): the FSC expense
  and commission reform. **The same release as this file's [R7]**, retrieved in both passes;
  cited together wherever the 추가납입 2×→1× conflict is discussed. Retrieved: yes.
- **REG-R32** — 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」 (2025-09-01): the raised
  deposit-protection limit the two 2025 product documents state. Retrieved: **in part** — the
  operative rule is [REG-R52], retrieved in full.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported by 보험매일: 평균수명 남 86.3 / 여
  90.7 and **65세 기대여명 남 23.7 / 여 27.1**, applied from April 2024. Those two 기대여명
  figures are the exact fit targets of `mort_table.csv`'s Makeham construction. Retrieved: yes
  — **but it is a news article**, the KIDI announcement itself not being retrievable, which is
  the second reason the table is a construction.
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 빅데이터 platform): the record
  that the 경험생명표 is released as **summary statistics only**, and that the published rate
  display does not reach the life side. This is the citation for "the table is not a
  transcription" and for the absence of any Korean 장해 incidence rate. Retrieved: in part.
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: the
  **public** national table, whose 완전생명표 `e(40)` of 41.9 (M) and 47.4 (F) is what the
  shipped table's implied complete `e(40)` on the **연금사망률** basis — **46.425 (M) and
  50.292 (F)**, the figures `mort_table.csv`'s provenance column rounds to 46.4 and 50.3 —
  must sit above by a selection margin. Also the
  reminder that population statistics are **만나이** while the model is 보험나이. Retrieved:
  yes.
- **REG-R39** — KOSIS 완전생명표 (single-year qx tables): **Retrieved: no** — distributed
  through the KOSIS interface rather than as a fetchable file, so the graduation cross-check
  uses the briefing figures of [REG-R38] and not single-year rates. The named to-do at
  `mort_table.csv`.
- **REG-R45** — 생명보험협회 공시실, FACT BOOK and 금융통계월보: the disclosure surface on
  which a variable product's 사업비율, 위험 보장비율 and **최저보증비용비율** are published,
  beside this file's [S12]. Retrieved: in part.
- **REG-R46** — 보험연구원 「2026년 보험산업 전망」, 황인창: the cross-product forecast series
  putting 변액보험 at ₩12.4조 for 2026, against this file's [R9] deck of a year earlier.
  Retrieved: yes (91 pp.).
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier regulatory disclosure: the **2026
  평균공시이율 of 2.50%**, which is simultaneously the base run's blended 투자수익률 target,
  the middle mandated illustration return, the payout-phase declared rate and the reason
  `prem_int_rate` does not exist on this product. Retrieved: in part.
- **REG-R49** — 상법 제4편 제1장 통칙 (제638조~제664조): 제638조의3 (품질보증해지), 제650조의2,
  **제662조 (3-year 소멸시효)**, and 제663조's one-way mandatory rule. Retrieved: yes (제4편
  read in full).
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): 제736조, the floor where a
  benefit becomes impossible — the 계약자적립액 **without** the GMDB top-up — and the rule that
  where one of several beneficiaries intentionally kills the insured the others are still paid.
  Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (**청약의 철회**): the statutory 15/30-day cooling-off
  the 표준약관 implements verbatim, and the rule that it is unavailable where the insured event
  has already occurred unless the policyholder withdrew knowing it had. Beside this file's
  [R14], which is the same Act's 제17조·제18조 at second hand. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: the operative deposit-protection rule. On a
  variable contract only the **contractually guaranteed amounts** — 최저사망적립액,
  최저연금적립액 and riders — are protected, to ₩100,000,000 (1억원) per person per insurer:
  the one carve-out in Korean law that applies to the guarantee and not to the account.
  Retrieved: yes.
- **REG-R57** — 소득세법 제59조의4 (특별세액공제 — 보장성보험료): the **12% credit on up to
  ₩1,000,000** of 특약보험료, which two product documents state. Retrieved: yes.
- **REG-R58** — 소득세법 제16조제1항제9호 and 시행령 제25조 (**저축성보험의 보험차익**): the
  tax treatment that makes this a savings contract rather than a protection one — the 월적립식
  route requiring 선납 of not more than six months, and the 종신형 route requiring any
  guarantee period to sit **within the published 기대여명 연수**, which is a direct constraint
  on the 10-year 보증기간 this model pays. Retrieved: yes (one ceiling formula renders as an
  image).
- **REG-R60** — 한국회계기준원, K-IFRS 제1117호 제정 의결: the standard in force in Korea since
  **2023-01-01**, alongside K-ICS. Retrieved: **in part** — the 별첨 HWP carrying the
  standard's own text did not return, so instrument-level readings of it are [unverified].
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: the **published** morbidity
  reference rates. Cited here for one contrast only, and it is a negative: the display is a
  **장기손해보험** display, covering 일반상해·교통상해 (사망 / 후유장해 / 입원), 질병 사망률,
  후유장해, 입원율 and 암 발생률 on the non-life side and **not reaching the life side**, and
  the entry reproduces only its 암 발생률 and 질병입원율 grids. So neither this product's
  mortality nor a 고도재해장해 incidence on this contract's own basis was retrieved from it.
  Retrieved: yes.

---

## Provenance note

Every entry above traces to `_research/variable-annuity.md`, which is the citation ground truth
for this product: the S# and R# numbering used here is that file's numbering, unchanged, and it
is **never renumbered** because `product-spec.md` and `technical-notes.md` cite against it. The
research file's own numbering is not this one's — it runs to S12 and R14, and it carries
**S3**, the KDB생명 약관, which this file omits as uncited, with the reason given at the head
of this page. Nothing was newly retrieved at drafting and no tag was added.

What lives there and not here: the **fact-extraction record** — twenty-five numbered sections
reproducing, page by page and document by document, the 좌수/기준가격 formula verbatim, the
five fee tables as three 상품요약서 actually print them, the guarantee census, the roll-up and
step-up worked examples, the 지급률 tables, the 해지공제 scales and the 별표 24 factor tables
as [R1] reproduces them; the **variation-across-carriers tables**, including the issue and term
envelopes, the premium-size limits, the guarantee designs, the fee-stack spreads and the option
menus across those six carriers, which is what makes the composite's every parameter choice
traceable to a range rather than to a document; and the **register of fetch failures and
[unverified] claims** — every URL tried and not opened, the 제7-60조 and 별표 24 failures, the
special-account asset-management ratios of [R5], the 시행령 제52조·제53조 text, the
금융소비자보호법 articles, and the carriers identified and not fetched.

The gaps that matter most on this product are recorded in both places, because they bound what
the model can claim rather than merely what the documents can cite: **the 경험생명표 rates**,
which are not published, so both columns of `mort_table.csv` are a construction; **any Korean
변액연금 적용해지율**, which no carrier publishes, so the lapse basis is calibrated to one
second-hand sentence; **any Korean variable-fund return series, volatility or correlation**,
none of which was retrieved, so every return assumption is [std] and the guarantees can be
valued at intrinsic only; **the 산출방법서**, a filed 기초서류 that is not public, so the
account recursion is consistent with rather than derived from the retrieved documents;
**시행세칙 별표 24**, which neither research pass could open, so the 보증준비금 this product is
actually reserved under is known only at second hand; and **any Korean unit expense cost**,
which the 사업비 disclosure does not contain, the disclosure being of charges and not of costs.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-variable_annuity-r1
[R10]: #krlib-variable_annuity-r10
[R11]: #krlib-variable_annuity-r11
[R12]: #krlib-variable_annuity-r12
[R14]: #krlib-variable_annuity-r14
[R2]: #krlib-variable_annuity-r2
[R3]: #krlib-variable_annuity-r3
[R4]: #krlib-variable_annuity-r4
[R5]: #krlib-variable_annuity-r5
[R7]: #krlib-variable_annuity-r7
[R9]: #krlib-variable_annuity-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R16]: #krlib-reg-r16
[REG-R26]: #krlib-reg-r26
[REG-R29]: #krlib-reg-r29
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R6]: #krlib-reg-r6
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
