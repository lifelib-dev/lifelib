# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/ci-insurance.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is
per product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md`
runs its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never
be read across.** The clearest instance in this product is [R4], which is 보험업법 제4조
from the CaseNote mirror, against [REG-R4], which is 보험업법 **제176조** (보험요율
산출기관). Access date for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 약관 (*yakgwan*, policy conditions), a 상품요약서
  (the statutory product summary), a 상품안내장, an industry-association product table, or
  a carrier product page. These are what make a contractual mechanic *sourced* rather than
  assumed. On this product they carry an unusually heavy load: **[S1] alone establishes the
  acceleration, its exact complement, the 105% residual floor, the 90-day 보장개시일, the
  first-year 감액, the premium waiver and the 장해분류표 gate**, and [S3] alone carries
  every disclosed rate in the model.
- **[R#]** — a regulatory, statutory, judicial, actuarial or market reference that only
  this product needs. Eleven of the sixteen are **secondary** — trade press, a practitioner
  column, a loss adjuster's case note — and every entry says so, because the dispute record
  of this product exists almost entirely in secondary form.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Every tag used in the three documents has an entry here, and every entry here is used.**
No source was added at drafting and none was dropped; the research file's S1–S8 and R1–R16
are cited in full, which is unusual — most products in this library leave some research
entries uncited. The reason is that the CI evidence base is small enough that nothing in
it was surplus.

**Nothing in this product's quantitative basis is [S#] except one grid and one premium.**
[S3]'s six 예정위험률 and three 예정 경험 사망률 at three ages, and [S4]'s published
monthly premium for exactly the anchor cell, are the whole of it. Everything else in
`mort_table.csv`, `ci_incidence_table.csv`, `lapse_table.csv` and the Projection's scalar
References is **[std]**, and `model.md` lists each one with its rationale and whatever
observed range the documents bound.

Company and branded product names appear in this file and in `_research/ci-insurance.md`
and **nowhere else** in the library: in `product-spec.md`, `technical-notes.md`,
`model.md` and the model docstrings a carrier is referred to by its tag alone, so a reader
can always resolve who said what — here — and never has to.

---

## Primary product sources

Eight documents from six carriers plus the 생명보험협회. Two are complete 약관 booklets of
over 1,200 pages each [S1] [S2]; one is a 상품요약서, the statutory summary that is the only
routinely public Korean document disclosing **pricing parameters** [S3]; one is a
상품안내장 carrying a 144-cell published premium grid [S4]; one is an industry-association
cross-carrier table [S5]; two are third-party mirrors of a second carrier's wordings
[S6] [S7]; and one could not be fetched at all [S8].

**Retrieval method, common to the set.** Plain `curl` is blocked for every Korean host
tried in this session (connection reset at the proxy), so everything below was fetched with
a summarising fetcher. That fetcher renders HTML but returns Korean PDFs as undecodable
binary; in every such case the binary it saved to disk was extracted locally with `pypdf`
and read directly. That is how the long 약관 were obtained.

(krlib-ci_insurance-s1)=

### S1 — ABL생명, 「(무)우리가족안심CI통합종신보험(보증비용부과형) 1904 약관」 (policy conditions, complete)

- Publisher: ABL생명보험주식회사 (ABL Life; formerly 알리안츠생명)
- Document: full 약관집 — 가이드편, 주요내용 요약서, 주계약 약관 and 34 특약 약관, 별표
  1–7, 법규 조항 정리, 신체부위 설명도; **1,207 PDF pages**, product form mark `1904`, in
  force from 2019-04-01
- URL: `https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2019/04/02/20190401_NP_우리가족안심CI통합종신보험(보증비용부과형)1904_약관.pdf`
  (served percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (7.6 MB PDF; the summarising fetcher reported it
  as unreadable binary but saved the file, and `pypdf` recovered all 1,207 pages of Korean
  text cleanly, including the annex tables)
- **The anchor document of this product, and the single heaviest-loaded source in it.**
  What rests on it: the 보험금 지급기준표 with both acceleration fractions and the exact
  complement [S1 별표1]; the **105% 계약자적립금 floor** under the residual death benefit,
  which is `resid_floor_mult` and the largest structural feature of the liability
  [S1 별표1 주8]; the 기본보험금 definition and its 중도인출 / 추가납입 arguments, held at
  zero in the model [S1 별표1 주7]; the **premium waiver on either a 50% 장해지급률 or any
  CI/LTC 지급사유** [S1 별표1 주4], which is why the waiver is two decrements and only one
  of them is modelled explicitly; the 90-day 중대한 암 보장개시일 and the 장기요양상태
  보장개시일 with its 재해 carve-out [S1 제7조] [S1 별표1 주1·주2]; the first-year
  breast-cancer 감액 [S1 별표1]; the 중대한 질병 definitions verbatim [S1 별표4], the
  중대한 수술 [S1 별표5] and the 중대한 화상 및 부식 [S1 별표6]; the **장해분류표** and its
  ADL schedule, including the **twelve-month deferral** on a 중대한 뇌졸중 assessment that
  the model's one-year lag between the two payments reflects [S1 별표3]; the 장기요양상태
  definition [S1 제6조]; the 보험나이 rule [S1 제26조]; the 2년 자살면책 [S1 제10조]; the
  interest-sensitive variant's 최저보증이율 ladder [S1 제36조]; and the whole standard
  contract apparatus — 계약 전 알릴 의무, 납입최고, 부활, 해지환급금, 보험계약대출.

(krlib-ci_insurance-s2)=

### S2 — ABL생명, 「무배당 걱정말아요CI통합종신보험(저해지환급형) 1705 약관」 (policy conditions, complete)

- Publisher: ABL생명보험주식회사 (the text still names 알리안츠생명's 공시실, so this is the
  transition-period edition)
- Document: full 약관집, form mark `1705`, in force from 2017-07-01; **1,339 PDF pages**
- URL: `https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2017/07/19/약관(20170701)NP_걱정말아요CI통합종신보험(저해지환급형)(20170701).pdf`
  (served percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (8.9 MB PDF, all pages extracted). **Extraction
  caveat, and it constrains what may be quoted:** `pypdf` warns
  `Advanced encoding /UniKS-UTF16-H not implemented yet` and reorders some characters within
  a line — Korean words come out with their trailing particles displaced — so only passages
  that read unambiguously are used, and **no annex definition is quoted from this document**
- The **저해지환급형** variant of the same family, in two forms (`30% 저해지환급형` and
  `50% 저해지환급형`), with the surrender-value rule stated in terms. What rests on it: the
  **carve-out that releases the suppression on a CI/LTC 지급사유** — the suppression applies
  only 「제7조 … 제2호의 CI/LTC보험금 지급사유가 발생하지 않은 경우」, which is the
  CI-specific delta on the whole life chassis and the reason `cv_pp_ci(t)` is the full
  표준형 value at every duration; the corroboration of the exact complement across four
  fraction pairs; the first-year 감액 [S2 별표1]; the statement that everything but 중대한
  암 and 장기요양상태 is covered from the 계약일 [S2 별표1 주1]; and a worked benefit
  illustration at ₩100,000,000 (1억원) on the 80% acceleration. It is the direct evidence
  that the Korean suppressed-surrender-value design reached CI business before it became
  universal.

(krlib-ci_insurance-s3)=

### S3 — KDB생명, 「무배당 베스트유니버셜CI보험 상품요약서」 (statutory product summary)

- Publisher: KDB생명보험주식회사
- Document: 상품요약서, 제작일자 2011년 1월; 32 PDF pages
- URL: `https://www.kdblife.co.kr/data_pdf/fp/2011/(무)베스트유니버셜CI보험_상품요약서20110103.pdf`
  (served percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (493 KB PDF, extracted cleanly)
- **The quantitative core of this product, and the only disclosed Korean CI morbidity
  table in public.** It publishes the **예정위험률 for 중대한 암, 중대한 급성심근경색증 and
  중대한 뇌졸중 by sex at ages 20 / 40 / 60**, together with 예정 경험 사망률 at the same
  ages. Those nine male numbers are the entire anchor set of both decrement files:
  `mort_table.csv` is a Makeham fit to three of them and `ci_incidence_table.csv` is
  log-linear interpolation and damped extrapolation around the other six. It also carries
  the 예정이율, 적용이율 and 최저보증이율; the **보험료지수 of 130.1%** that bounds the
  expense construction from above; the **보장위험별 연간보험료** split, from which the CI
  benefit's 50.6% share of the risk premium is read and the `other` limb's 10.5% loading
  derived; the **110%** residual floor multiple of the older universal design, which
  `point_id = 9` runs; four full 해지환급금 illustration tables; 가입나이 and 가입한도 by
  acceleration form; the 예정위험률 revision right from five years, which takes effect as a
  **benefit reduction**; and the 해약환급금 identity in a CI product's own words —
  「순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액」.
- **Two weaknesses, both recorded at the point of use.** Its vintage is January 2011, when
  the 최저보증이율 on this product was 4.0% p.a. compounded, so its interest basis is not
  transferable. And its **female mortality at ages 40 and 60 extracts identical to the
  male**, which is not plausible for a Korean life table and is almost certainly a PDF
  column-merge artefact; those two values are **[unverified]** and are not used, which is
  why the shipped female mortality is a flat ratio off the age-20 anchor and why the
  resulting female advantage is understated.

(krlib-ci_insurance-s4)=

### S4 — 미래에셋생명, 「건강담은 GI종신보험(무)1904 [해지환급금이 적은 유형]」 상품안내장 (product brochure with rate card)

- Publisher: 미래에셋생명보험주식회사
- Document: 상품안내장, 제작일자 2019년 8월; 16 PDF pages
- URL: `https://pdf.miraeassetlife.com/directDownloadDocFile.do?Ax=579e39c86d37ae718806f12af1f79d27b07b70d1786ca23d5683a184e905d64e524ebd66da8b940f095b0b06a5a35d10bd22f1ec7a0e3ae91036c9d4e123c908f35cad83ff9ac6434f13cc3a6f1c921065c519b83da76d25f8aec171de5e8ce8f55d3f852fd354789608dc6ff0f8b51b`
- Accessed: 2026-09-03, Retrieved: **yes** (791 KB PDF, extracted cleanly)
- **The single richest premium source found, and the origin of the anchor cell's price.**
  It carries a full age × sex × acceleration-form × cover-menu grid of monthly premiums at
  ₩100,000,000 (1억원), 20-year premium term, for both the 기본환급형 and the 해지환급금이
  적은 유형 — **144 published cells** for the main contract (three acceleration forms x four
  benefit menus x six age/sex columns on each of the two return forms), plus a rider card
  of comparable size.
  The anchor's **₩306,740 a month** is one of those cells, at 남 40세 / 1억원 / 20년납 /
  월납 / 80% 선지급형 / 저해지환급형, and the model's ₩3,680,880 is twelve times it
  **[std]**. What else rests on it: the published **1.085 ratio** of the 80% form to the 50%
  form at 남40, which the model's own pricing recursion reproduces at 1.0794 without being
  fitted to it; the **1.10224 기본환급형 form factor** used to price the non-anchor points;
  the **5.30% office-premium step from 3대보장형 to 17대보장형**, the numerator of the
  `other` limb's derivation; the 저해지 carve-out wording 「「선지급 진단보험금」 지급사유
  발생 전 납입기간 동안」; the **GI** answer to CI (code-based rather than definition-based
  triggers); the 100% 선지급플러스형 with its residual 유족위로금, which is not a pure
  acceleration and is out of scope; the 90-day 암 보장개시일; the **all-trigger** first-year
  50% reduction that `first_year_scope = all` models; the 건강인우대 criteria; the banded
  high-sum-assured discount; and a 종신 vs 연금 comparison built on the 생명보험협회
  상품공시시행세칙 basis with its 예정이율 stated at 「약 2.75%」.

(krlib-ci_insurance-s5)=

### S5 — 생명보험협회, 「생보사 주요 CI·GI보험상품 현황」 (별첨) (industry-association product table)

- Publisher: 생명보험협회 (Korea Life Insurance Association, KLIA)
- Document: a 5-page 별첨 tabulating, carrier by carrier, the CI and GI products then on
  sale with each product's headline benefit structure
- URL: `https://www.klia.or.kr/FileDown.do?fileNo=16793&seq=4`
- Accessed: 2026-09-03, Retrieved: **yes** (the server declares the file
  `application/x-msdownload`; it is in fact a 5-page PDF — magic bytes `%PDF-1.4` — and
  extracted cleanly once renamed)
- A market-wide cross-section in one table: 한화생명, ABL생명, 삼성생명 (two products),
  교보생명 (two), 미래에셋생명, KDB생명, 동양생명 (two), 메트라이프생명, AIA생명 (two),
  NH농협생명 and one further carrier. What rests on it: the range of acceleration fractions
  actually on sale, which is what makes the 80% choice a **[std]** selection from an
  observed set rather than an invention; the corroboration of the first-year 감액; one
  carrier's flat 30% residue, which is a different design from the acceleration modelled
  here; and the evidence for the CI → GI migration.
- **Caveat, recorded at the entry**: the file is served bare with no parent page reachable,
  so **its publication date could not be established**. Internal evidence — 삼성생명
  GI플러스종신보험 (launched 2020-01, [R11]), 미래에셋생명 건강담은 GI종신보험 (2019, [S4])
  and 동양생명 수호천사 알뜰한통합GI보험 — places it in or after 2020. It is treated as an
  **undated** source and no fact rests on its date.

(krlib-ci_insurance-s6)=

### S6 — 알리안츠생명, 「무배당 알리안츠유니버셜CI종신보험 약관」 (policy conditions, third-party mirror)

- Publisher: 알리안츠생명보험 (the predecessor of ABL생명); mirrored as HTML by Law Insider
- URL: `https://www.lawinsider.com/ko/contracts/4s3tMnNkSm6`
- Accessed: 2026-09-03, Retrieved: **in part** (the page renders and a summarising fetch
  returned the substance of the definitions and the benefit table; the mirror is a
  third-party reproduction, not the carrier's own file, so **nothing is quoted from it
  word-for-word**)
- Corroboration from a second carrier of the 중대한 암 / 중대한 급성심근경색증 / 중대한
  뇌졸중 definitions and of the 50% / 80% pair. The fact worth having, and the only one this
  product takes from it alone, is the **제1보험기간 / 제2보험기간 split at age 80**:
  제1보험기간 runs 계약일부터 80세 계약해당일 전일까지 and 제2보험기간 from the 80세
  계약해당일 종신토록. That is the original 2002 structure [R1] describes, it is named in
  `product-spec.md`, and `model.md` records why it is deliberately **not** modelled — a
  second discontinuity at 80 would collide with the 저해지 step.

(krlib-ci_insurance-s7)=

### S7 — 알리안츠생명, 「무배당 알리안츠어린이CI보험 약관」 (policy conditions, third-party mirror, redacted)

- Publisher: 알리안츠생명보험; mirrored as HTML by Law Insider
- URL: `https://lawinsider.com/ko/contracts/9SLRE7Bms1X`
- Accessed: 2026-09-03, Retrieved: **in part** — the mirror is **heavily redacted**, with
  blocks of ▇▇▇ replacing the definitional text and every benefit amount. Article headings
  and the existence of a 별표1 benefit table on a ₩20,000,000 (2,000만원) basis are legible;
  nothing else is
- Cited **once**, in `product-spec.md`'s statement of what the source set contains, as
  evidence only that a **children's CI variant existed on this chassis**. No number and no
  definition is taken from it, and nothing in the model depends on it. It is listed rather
  than dropped because a reader counting the primary set should be able to see that one of
  its members carries no facts.

(krlib-ci_insurance-s8)=

### S8 — 삼성생명, 「통합올인원CI보험(무배당, 보증비용부과형)」 상품 페이지 (carrier product page)

- Publisher: 삼성생명보험주식회사
- URL: `http://product.samsunglife.com/product/insu/family/univlivcare/insuPrdtUnivLivCareFeat.html?tloParam=bl_allinoneci`
- Accessed: 2026-09-03, Retrieved: **no** — HTTP 503 on both attempts, over `http` and
  `https`
- Recorded because the omission matters: **the market leader's current CI product is
  absent from the primary set.** It is present only through the KLIA table [S5] and through
  search snippets, so every fact about it is **[unverified]**. `product-spec.md` cites this
  entry at the point where it says so, and nowhere else. Nothing in the model rests on it.

---

## Regulatory and actuarial references

Sixteen entries. **Two are primary and substantial** — a KIRI research monograph [R1] [R2]
and a regulator's press release [R3] — one is a statute mirror [R4], one is a court
judgment [R5], and **eleven are secondary**: trade press, consumer press, a practitioner
column and a loss adjuster's case note. That balance is itself a finding about this
product. The 중대한 problem is the defining fact of Korean CI and it has generated no
retrievable statistic at all: no 부지급률, no CI-specific complaint series, no claim-denial
rate. What exists is anecdote, and the documents say so wherever they lean on it.

(krlib-ci_insurance-r1)=

### R1 — 보험연구원, 「보험상품 변천과 개발 방향: 생명보험 상품 중심」 Ⅳ. CI보험의 성장 (research monograph, chapter extract)

- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI), 연구보고서 2018-5;
  김석영·김세영·이선주; 발행 2018년 2월. **Chapter Ⅳ, 「CI보험의 성장」, pp. 80–119**,
  issued as a standalone 40-page PDF
- URL: `https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2018-05_04.pdf` (served
  percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (778 KB PDF; the summarising fetcher declared it
  corrupt, `pypdf` extracted all 40 pages cleanly)
- **The definitive account of why CI보험 exists in Korea and how it was priced**, written
  by KIRI researchers with access to the product developers. It is the most-cited [R#] in
  this product and the one carrying the most modelling weight. What rests on it: that the
  supervisor **refused a survival period** on consumer-protection grounds, which is why the
  acceleration rather than the standalone form became the market default and why the shipped
  incidence rates already contain the lives who die of the CI cause; that the supervisor
  **required the overlap between CI causes to be reflected in the filed rate** —
  「CI 질병들 간 중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로 검증받고
  사용하였다」 — which is why the five shipped causes may be summed and why a table built by
  adding published site-specific incidences would be wrong; the **안전할증 regime** on the
  기초발생률, capped at 30% in the early 2000s, raised to 50% in 2015 and uncapped from
  2017, which is why `mort_be_factor` and `ci_be_factor` at 1.00 make the base run a
  **valuation-basis run and not a best estimate**; the decision to price on disease
  *definitions* rather than ICD codes; the 2002 launch, the reinsurer relationships and the
  new-business series for 2002–2004; the **thyroid- and breast-cancer experience shock**
  behind the first-year 감액; the extension of CI cover to the 100세 계약해당일; that a
  손해보험회사 may not write the 질병사망 main contract an acceleration requires; and the
  2003 → 2008 → 2010 → 2013 → 2016 product evolution. It also reproduces the three headline
  definitions against their ordinary-cover counterparts, an independent check on [S1].
- It is also the source of a **negative** fact the documents state repeatedly: **no CI
  lapse experience of any kind was retrieved**, from this or any other document, which is
  why `lapse_table.csv` is [std] throughout.

(krlib-ci_insurance-r2)=

### R2 — 보험연구원, 「보험상품 변천과 개발 방향: 생명보험 상품 중심」 (research monograph, complete)

- Publisher: 보험연구원, 연구보고서 2018-5; 김석영·김세영·이선주; 2018년 2월; 308 PDF pages
- URL: `https://kiri.or.kr/pdf/전문자료/KIRI_20180419_104228.pdf` (served percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (4.5 MB PDF; front matter, contents and Chapter
  Ⅶ extracted and read; the remaining chapters were not read)
- Two jobs. It fixes the **bibliographic identity** of [R1], which is a chapter of it. And
  **Chapter Ⅶ, 「간편심사보험의 성장」, pp. 189–220**, is what `product-spec.md`'s
  underwriting scope rests on: the taxonomy of 일반심사 / 간편심사 / 무심사, the three
  simplified-underwriting designs, the standard 10-question 계약전 알릴 의무 form, and the
  sidebar on **당뇨CI보험** — a CI product sold only to diabetics without complications
  (HbA1c ≤ 8%) that failed for want of a distribution route. The composite is written on
  일반심사 and that choice is **[std]**; this entry is what bounds the alternative.

(krlib-ci_insurance-r3)=

### R3 — 금융위원회, IFRS17 주요 계리가정 가이드라인 보도자료 (2024-11-07) (regulator press release)

- Exact title: 「합리적인 계리가정과 단계적 할인율 조정을 통해 보험회계의 신뢰도와
  안정성을 높이겠습니다」
- Publisher: 금융위원회 보험과, 보도자료, **2024-11-07**, issued out of the 제4차
  보험개혁회의 (2024-11-04)
- URL: `https://www.fsc.go.kr/no010101/83351`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML rendered and read)
- The live constraint on any lapse assumption a Korean 무·저해지 CI product carries, and
  the source of both endpoints of the model's `log_linear` basis: the **로그-선형 원칙모형**
  imposed for 무·저해지 lapse rates, with a convergence point at 납입완료 of **0.1%** and a
  post-completion ultimate of **0.8%**; the requirement that departure from the 원칙모형 be
  disclosed against the CSM, K-ICS and net-income differences, with FSS scrutiny — which is
  why this model ships the 표준형 `table` basis beside the 원칙모형 rather than instead of
  it; the **30% 이상** additional lapse at a 단기납 bonus date, which does **not** bite here
  because this composite carries no 유지보너스; and the 실손 손해율 move to 연령군단별
  analysis, which does not bite at all. **Cited beside [REG-R27]**, which is the same
  decision retrieved through the FSC and FSS release pair together with its 별첨; the
  guideline attachment itself was never converted from HWP, so **the functional form of the
  log-linear model is [unverified] at instrument level** and the interpolation between the
  two endpoints is this library's reading.

(krlib-ci_insurance-r4)=

### R4 — 보험업법 제4조 (보험업의 허가) — 제3보험업의 법정 정의 (statute, mirror)

- Publisher: 대한민국 법률; retrieved through CaseNote's statute mirror. Version shown on
  the page: 법률 제17636호, 2020-12-08 일부개정, 2021-06-09 시행
- URL: `https://casenote.kr/법령/보험업법/제4조`
- Accessed: 2026-09-03, Retrieved: **yes**
- 제4조제1항 licenses insurance business by 보험종목 in three groups, of which **제3호
  제3보험업 — 상해보험, 질병보험, 간병보험**. This is the statutory hook that lets a life
  insurer write the health element of a CI contract and, equally, prevents a 손해보험회사
  from writing the 질병사망 main contract that an acceleration requires — which is why the
  non-life market's answer to the same disease list is a 독립급부 특약 with no acceleration
  in it. **Caveat**: `law.go.kr` would not serve the statute to this session, so this is a
  mirror and the article text is paraphrased from it rather than quoted. Cited beside
  [REG-R1], which carries the same article from an independent full-Act retrieval. **Not**
  to be confused with [REG-R4], which is 보험업법 제176조.

(krlib-ci_insurance-r5)=

### R5 — 서울중앙지방법원 2016. 1. 14. 선고 2014가단242567 판결 [보험금] (judgment, first instance)

- Publisher: 서울중앙지방법원 (판사 김영수); retrieved through CaseNote
- URL: `https://casenote.kr/서울중앙지방법원/2014가단242567`
- Accessed: 2026-09-03, Retrieved: **yes**
- The cleanest judicial statement of the gap this product creates, and the only retrieved
  Korean court decision on a 중대한 암 claim. Plaintiff A against 교보생명 on two CI
  contracts (2005 and 2007); the insured was diagnosed in 2014 with a colorectal carcinoma
  **confined to the mucosa**. The court held the 약관's 중대한 암 definition — requiring
  침윤파괴적 증식 into surrounding tissue — **not** satisfied, and rejected the ₩53,000,000
  CI claim; it allowed the ordinary 암 rider claim, the diagnosis carrying KCD code C18, and
  the surgery benefit for the endoscopic polypectomy, awarding ₩13,000,000. **The same
  histology is 암 for the rider and not 중대한 암 for the main contract.** It is also the
  reason later Korean CI 약관 write 대장점막내암 out of 중대한 암 expressly [S1 별표4], and
  it is the concrete demonstration of the point the incidence basis rests on: [S3]'s rates
  are 중대한 암 rates, not cancer rates.

(krlib-ci_insurance-r6)=

### R6 — 조세금융신문, 「[전문가 칼럼] 중대한 뇌졸중은 왜 받기 어렵나요?」 (practitioner column, **secondary**)

- Publisher: 조세금융신문; 한규홍 (한결손해사정 손해사정사), 2023-12-25
- URL: `https://tfmedia.co.kr/mobile/article.html?no=154430`
- Accessed: 2026-09-03, Retrieved: **yes**
- A loss adjuster's account of the **25% 장해지급률 gate** and two declined claims: a
  confirmed 지주막하출혈 with ICU admission that fell below 25%, and a 뇌경색증 with
  demonstrated cognitive decline that likewise fell below it. Carries **no statistics**, and
  the documents cite it as one of five converging anecdotes rather than as evidence of a
  rate. It is one of the sources behind the specification's statement that the severity gate
  is where the narrowness of 중대한 actually lives.

(krlib-ci_insurance-r7)=

### R7 — 한국보험신문, 「'중대한' 문턱 높은 CI보험… 소비자 혼선 여전」 (trade press, **secondary**)

- Publisher: 한국보험신문; 주옥진 기자, 2026-04-06
- URL: `https://www.insnews.co.kr/news/articleView.html?idxno=90022`
- Accessed: 2026-09-03, Retrieved: **yes**
- The most recent evidence in the set that the 중대한 problem is still live: a claimant
  fifteen years into a CI policy, with a 뇌경색 diagnosis and a mobility aid, declined on the
  ground that 일상생활 remained possible at some level. Carries **no statistics**. Cited for
  currency — it is what lets `product-spec.md` say the dispute is a 2026 fact and not only a
  2015 one.

(krlib-ci_insurance-r8)=

### R8 — 투데이신문, 「'중대한' 조건에 막힌 CI보험, '불완전 판매' 온상되나」 (trade press, **secondary**)

- Publisher: 투데이신문; 이세미 기자, 2020-05-11
- URL: `https://www.ntoday.co.kr/news/articleView.html?idxno=72483`
- Accessed: 2026-09-03, Retrieved: **yes**
- Mis-selling allegations at the point of sale and — the point worth recording, and the
  reason this entry exists — a **금융감독원 statement that it had not identified a particular
  mis-selling problem in the CI sales process**. That is the only regulator statement on CI
  conduct recovered anywhere in the research pass, and `product-spec.md` cites it against
  the anecdote rather than with it, because a specification that reported only the
  complaints would be reporting one side of a record whose other side exists.

(krlib-ci_insurance-r9)=

### R9 — 보험저널, 「CIㆍGI 보험…나에게 유리한 상품은?」 (trade press comparison, **secondary**)

- Publisher: 보험저널; 최환의 기자, 2020-09-04 (updated 2020-09-07)
- URL: `https://www.insjournal.co.kr/news/articleView.html?idxno=2863`
- Accessed: 2026-09-03, Retrieved: **yes**
- The cleanest statement of the **CI / GI distinction**: CI uses the 약관 정의 방식, GI the
  한국표준질병·사인분류 (KCD) code; GI covers everything under the C codes where CI covers
  only 중대한 암; CI's 뇌졸중 reaches both 뇌출혈 and 뇌경색 but behind the 25% gate, whereas
  GI's cerebrovascular cover is often narrower in scope but unconditional. Its premium claim
  — that CI runs about **2% dearer** than GI for identical cover, often reversed on recent
  GI products — is a **secondary assertion with no published basis** and is tagged as such
  at the point of use; nothing in the model rests on it.

(krlib-ci_insurance-r10)=

### R10 — 소비자가만드는신문, 「CI보험 진단금 받기 '하늘의 별따기', 왜?」 (consumer press, **secondary**)

- Publisher: 소비자가만드는신문; 김문수 기자, 2015-09-14
- URL: `https://www.consumernews.co.kr/news/articleView.html?idxno=505280`
- Accessed: 2026-09-03, Retrieved: **yes**
- A declined 지주막하출혈 claim (Gwangju, ten-year policy) on the ground that no disability
  was diagnosed, and a clear statement of the **three-part CI test** — disease, severity,
  disability rating — which is the structure `product-spec.md` uses to organise the trigger
  set. **No denial-rate statistics.**

(krlib-ci_insurance-r11)=

### R11 — 전자신문, 「[보험 2020] 삼성생명, 보장요건 완화한 'GI플러스종신보험' 출시」 (trade press, product launch, **secondary**)

- Publisher: 전자신문, 2020-03-03 (print edition 2020-03-04)
- URL: `https://www.etnews.com/20200303000151`
- Accessed: 2026-09-03, Retrieved: **yes**
- The market leader's move from CI to GI, and the source of one number the model uses: the
  product advertises **25 distinct premium-waiver triggers**, which is what
  `model.md` cites for the finding that a modern accelerated product has **two trigger sets
  of different widths** — a narrow one for the money and a wide one for the waiver — and
  that a model using one rate for both is wrong on the second. It also documents the removal
  of the 중대한 qualifier, the three headline diseases plus 18 further conditions, 장기요양
  1·2등급 on the same chassis, and 삼성생명's first **저해지 30%형**. Its quoted acceleration
  of 130% of the sum assured before age 65 and 180% at 65 or later is **above 100% and
  therefore cannot be a pure acceleration**; it is recorded as reported and tagged
  **[unverified]** for its construction.

(krlib-ci_insurance-r12)=

### R12 — 스페셜경제, 「CI에서 GI로, SI에서 WI로…진화의 도마 위로 오른 '종신보험'」 (trade press, **secondary**)

- Publisher: 스페셜경제; 이정화 인턴기자, 2020-07-09
- URL: `http://www.speconomy.com/news/articleView.html?idxno=235502`
- Accessed: 2026-09-03, Retrieved: **yes**
- The four-generation taxonomy of the Korean accelerated whole-life product — **CI** (early
  2000s, severity definitions), **GI** (from 2010, KCD codes), **SI** (from 2017, staged
  payments), **WI** (from June 2020, wider cerebrovascular and cardiac scope) — and the
  carriers associated with each. `product-spec.md`'s generation account rests on it, with
  the caveat stated there: **the dates are the article's, not a regulator's, and the SI and
  WI labels are trade usage rather than defined terms.** The specification is explicit that
  no market-share series stands behind the account.

(krlib-ci_insurance-r13)=

### R13 — 뉴스1, 「삼성생명, 질병단계별로 보험금..통합 스테이지CI보험」 (trade press, product launch, **secondary**)

- Publisher: 뉴스1, 2014-01-02
- URL: `https://www.news1.kr/amp/finance/general-finance/1478797`
- Accessed: 2026-09-03, Retrieved: **yes**
- The **SI (staged) design** in its selling form: 50% acceleration on 중대한 암 stages I–III
  (20% for breast cancer), 100% on stage IV, blood and lymphatic cancers and the other
  최중증 states, with a further 50% if a stage I–III cancer progresses to stage IV; 11
  diseases and 8 surgeries; **가입나이 15–60**; cover extended to **age 100**. The last two
  are what this product takes from it: the issue-age envelope, which is invariant across
  every CI source retrieved, and the corroboration that CI cover runs to the 100세
  계약해당일 — which is `ci_cover_end()`. The staged design itself is named and **not**
  modelled.

(krlib-ci_insurance-r14)=

### R14 — 서울파이낸스, 「[신상품] 미래에셋생명 '건강담은 GI변액종신보험'」 (trade press, product launch, **secondary**)

- Publisher: 서울파이낸스, 2020-01-17
- URL: `https://www.seoulfn.com/news/articleView.html?idxno=369214`
- Accessed: 2026-09-03, Retrieved: **yes**
- The variable-account sibling of [S4]: 17 diseases with acceleration up to 100% of the sum
  assured; the 100% 선지급형 still paying **30%** of the main-contract sum assured to the
  family as an annuity on death; 중증갑상선암 and 남성유방암 pulled back into 일반암; 루게릭병
  and 다발경화증 in the main contract. Cited for the **100% form's residual**, which is the
  evidence that a "100% acceleration" in this market is not an acceleration of the whole
  benefit and is therefore out of this product's scope.

(krlib-ci_insurance-r15)=

### R15 — 보험저널, 「CI 보험 보장분석, 무조건 해지는 금물…"꼼꼼한 점검이 우선"」 (trade press, consumer advice, **secondary**)

- Publisher: 보험저널; 최은빈 기자, 2024-05-29
- URL: `https://www.insjournal.co.kr/news/articleView.html?idxno=23012`
- Accessed: 2026-09-03, Retrieved: **yes**
- Evidence only that a large block of legacy CI business remains in force and under review
  by its policyholders in 2024, and that **갱신형 riders attached to it terminate at 80** —
  which `product-spec.md` uses when it sets the rider perimeter of the composite. **No
  statistics.**

(krlib-ci_insurance-r16)=

### R16 — 로이즈손해사정, 「중대한 질병 CI보험 진단금 사정 사례」 (loss adjuster's case note, **secondary**)

- Publisher: 로이즈손해사정 (independent loss adjuster); date not stated on the page
- URL: `https://www.lloyds.co.kr/post/중대한-질병-ci보험-진단금-사정-사례`
- Accessed: 2026-09-03, Retrieved: **yes**
- A worked claim end to end: a main contract of ₩35,000,000 (3,500만원) issued October 2006
  with a 50% CI benefit of ₩17,500,000; a left lenticulostriate 뇌경색 with right-sided
  weakness, initially declined for want of a permanent deficit, then **paid in full** once a
  후유장해진단서 established a permanent ADL restriction. It is the only retrieved document
  showing an adjudication that succeeded, which is why the specification cites it beside the
  four that failed. The adjuster records the insurer's working rule as **six months or more
  of rehabilitation with an ADL-based rating of 25% or higher**; that six-month practice
  point is the adjuster's and **not the 약관's**, and is tagged accordingly wherever it
  appears.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose
own R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that
page plain [R#] refers to its own entries, so the two schemes must never be read across.
The forty-two entries the CI documents cite, all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: the 생명보험 / 손해보험 / **제3보험** licence split.
  This product is written under 제1항제1호 with its health element in 제3보험, and a
  손해보험회사 may not write the 질병사망 main contract the acceleration needs. Retrieved:
  yes (full Act, 127,346 characters). Cited beside this file's [R4].
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is a 기초서류 filed
  with the FSC and never published**, which is why every pricing-basis parameter in this
  model is [std] and why the 안전할증 inside [S3]'s 예정위험률 cannot be sized. Retrieved:
  yes.
- **REG-R3** — 보험업법 제120조: the statutory duty to accumulate 책임준비금, cited as a
  layer this model does not compute. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): the statutory footing of 보험개발원 and
  of the 참조순보험요율 regime, in which the rate is what the bureau **files** rather than
  what it publishes — and no CI item appears on its public channels at all. Retrieved: yes.
  **Not** this file's [R4].
- **REG-R5** — 보험업법 제181조·제184조: the 선임계리사 behind the 기초서류 and the
  reserving. Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), 본문: the **기준연령 요건** that makes
  만 40세 male on monthly premiums the prescribed disclosure cell — which is why the anchor
  is that cell — and the 계약자적립액 적용이율 with the 금리연동형 / 금리확정형 distinction
  that makes this composite a 금리확정형. Retrieved: yes (226,083 characters, the whole
  고시).
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the 잔여보장요소 /
  발생사고요소 taxonomy, with the calculation delegated to the FSS Governor. Retrieved: yes.
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart anywhere else in this repository. It measures against a surrender
  value computed on the 제7-66조제1항 basis **even for the 제7-66조제4항 products that may
  contractually pay less**, which is why `cv_std_pp(t)` is published: a CI event doubles the
  contractual surrender value and changes that reserve not at all. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**): the solvency layer and its
  sub-risks, of which **장해ㆍ질병위험액** is negligible on an ordinary 종신보험 and carries
  76.7% of this product's benefit stream. Retrieved: yes (article text; the 기본요구자본
  aggregation renders as an image and the 별표 22 detail was not retrieved).
- **REG-R16** — 감독규정 제7-60조 (생명보험의 보험상품설계): **제8호 forbids a contract to be
  extinguished while the risk it covers remains effective**, which is why the contract
  survives its own acceleration and why `pols_ci` is a transition rather than an exit;
  제10호 requires a 금리연동형 product to set a 최저보증이율, which is why [S1]'s
  interest-sensitive variant carries the 1.5% / 0.5% ladder. Retrieved: yes.
- **REG-R17** — 감독규정 제7-63조 (제3보험의 보험상품설계): 제1항제1호 requires a 제3보험
  product to pay the 계약자적립액 on **death from a cause the policy does not cover** and
  terminate. Cited here for what it does *not* do: it is a first-order requirement for the
  four 제3보험 products in this library and does **not** bite on this main contract, which
  covers death from any cause. It bites on the riders attached to it. Retrieved: yes.
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액): the analysis of
  premium adequacy on **최적기초율** with projected cash flows — the regulatory use of a
  liability cash-flow model in Korea, and the shape this projection takes — and the
  annualised-premium basis. Retrieved: yes (article text; the two 계약자적립액 accrual
  formulas did not extract).
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): the 해약환급금 as 순보험료식
  책임준비금 less 미상각신계약비, floored at zero (「이를 영(零)으로 처리한다」 — which is
  why `claims_lapse` is nil in policy year 1); the **해약공제기간 capped at seven years**,
  which puts `surr_chg_pp(t) = 0` from `t = 7` and proves the step at 납입완료 is not a
  surrender-charge effect; and 제4항, which permits the reduced surrender value of a
  무·저해지 form precisely *because* premiums were computed on a 최적해지율 — so the lapse
  vector is a condition of the product's legality. Retrieved: yes (operative words in full;
  the formula display did not extract).
- **REG-R20** — 감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액: the
  **표준해약공제액** by formula — 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000,
  the 계수 being the 보험기간 capped at 20 for a 보장성보험, so on a 종신 contract it is one
  year's net premium plus 1% of the sum assured. `surr_chg_cap_pp()` computes it at
  **₩3,944,704** on the anchor. Retrieved: yes (1-page PDF, full text including all seven
  notes).
- **REG-R21** — 감독규정 [별표 15] 보험가입금액의 산정: 제3호 read with 제8호 takes the
  **일반사망보험금 before any 증감**, so the 보험가입금액 entering the cap is the
  pre-acceleration ₩100,000,000 and not the ₩20,000,000 residual. Using the residual would
  under-state the cap by 20%. Retrieved: yes (1-page PDF).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조 (수수료, 공시, 신고): **제7-45조제7항**,
  the 보험가격지수, which exists precisely because a Korean consumer cannot see the pricing
  basis — the framing of the whole assumption section. Retrieved: yes.
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the supervisor's model policy conditions,
  and the reason the carrier 약관 in this set agree almost word for word. Cited by article —
  제21조 (**보험나이**, the model's age basis), 제22조, 제26조·제27조 (부활), 제33조 (the
  **보험계약대출** on the payable 해약환급금, which is why the loan room doubles at a CI
  event), 부표 3 (the 장해분류표 the 25% gate reads against). Retrieved: yes (a 492-page
  PDF, 441,610 characters, read in full).
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금): **Retrieved: no.** The
  K-ICS **대량해지 shock**, including the 고환급형 test, is therefore known only at second
  hand through [REG-R36], and everything resting on it is **[unverified]** — which matters
  here because the representative form is a 저해지 one.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (2024-11-07, 계리가정·할인율): the **IFRS17 주요
  계리가정 가이드라인**, retrieved as the release pair with its 별첨. It is the source of
  the model's `log_linear` lapse endpoints — 0.1% at 납입완료, 0.8% ultimate — of the
  disclosure requirement that makes carrying the `table` basis beside it the right thing to
  do, and of the ≥ 30% additional-lapse floor at a discrete contractual event, which does
  not bite on a composite with no 유지보너스. Retrieved: yes; **the guideline attachment
  itself was never converted from HWP, so its functional form is [unverified] at instrument
  level.** Cited beside this file's [R3].
- **REG-R28** — 무(저)해지환급금 보험 상품구조 개선 (2020) and FSS 소비자경보 (2019): the
  supervisor's own statement of the 환급률 structure and of the fact that a 무해지 policy has
  nothing to lend against. Retrieved: yes.
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여…」 (2019-08-01): the **1,200%
  rule** capping first-year 모집수수료 at twelve times the monthly premium — i.e. at one
  annual premium, which is what `comm_init_rate = 0.80` sits below — and the FSC's
  **보장성보험 rule of thumb sizing the 표준해약공제액 at 13 months' premium**, which gives
  ₩3,987,620 against the model's ₩3,944,704, a **1.1%** agreement between two independent
  statements of the same cap. Retrieved: yes.
- **REG-R32** — 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」 (2025-09-01): the
  ₩100,000,000 protection limit, cited beside the operative [REG-R52]. Retrieved: in part.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported by 보험매일: 평균수명 남 86.3 /
  여 90.7 and 65세 기대여명 남 23.7 / 여 27.1, applied from April 2024. **The record that
  the table is released as summary statistics only**, which is the first reason
  `mort_table.csv` is a construction and ω = 110 is [std]. Retrieved: yes — **but it is a
  news article**, the KIDI announcement itself not being retrievable.
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 빅데이터 platform): the same
  record from the bureau's own side, and the evidence that **no CI item appears there at
  all**. Retrieved: in part.
- **REG-R36** — 보험연구원 CEO Report 03호, 노건엽·이승주 (건전성 제도): the second-hand
  source for the 대량해지 shock calibration that [REG-R26] would have carried first-hand.
  Retrieved: yes (24 pp.).
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: the
  **public** national table, whose survival to age 80 of 남 64.4% / 여 82.2% is the
  cross-check that shows the shipped female mortality construction **understates the female
  advantage** — a 15-to-80 death-probability ratio of 0.560 against an implied 0.500.
  Retrieved: yes.
- **REG-R39** — KOSIS 완전생명표 (single-year qx tables): **Retrieved: no** — distributed
  through the KOSIS interface rather than as a fetchable file, so the graduation check uses
  the briefing figures of [REG-R38] and not single-year rates.
- **REG-R40** — 「2023년 국가암등록통계 참고자료」 (보건복지부·중앙암등록본부): the national
  cancer registry. Three things rest on it: the **breast share of the female cancer burden**
  behind `breast_share_f = 0.268` (유방 29,871 cases, against the burden less the 19.0% that
  is 갑상선); the registry shares — 갑상선 12.3%, 전립선 7.8% — that show how much of
  registered incidence the 중대한 암 exclusions remove before the rest are taken out; and
  the **69.6% five-year survival excluding thyroid** that anchors `mort_ci_factor = 3.00`
  qualitatively. Retrieved: yes (41-page PDF, read in full).
- **REG-R42** — 국민건강보험공단 「장기요양 등급 판정 현황」: **154,688 1·2등급 인정자**, the
  order-of-magnitude anchor for the `ltc` incidence limb — the weakest number in the model,
  and a placeholder for the construction `LTC_KR_S` owns. Retrieved: yes (table).
- **REG-R43** — 「2024 노인장기요양보험 통계연보」, as reported by 메디칼월드뉴스:
  **Retrieved: no** — returned only as a search-result summary. Cited beside [REG-R42] to
  record where the fuller series would be, and to mark that this product takes its 1·2등급
  inception from `LTC_KR_S` rather than rebuilding it.
- **REG-R45** — 생명보험협회 공시실, FACT BOOK and 금융통계월보(생명보험편): the industry
  statistical series, built from insurers' 업무보고서. Cited for a **negative** finding: it
  reports 보유계약, the 보장성/저축성 split and 지급유형별 보험금, and **carries no CI
  line**, which is why the displacement of CI by 진단비 중심 건강보험 is a qualitative claim
  in this library and never a market-share series. Retrieved: in part.
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier regulatory disclosure: the **2026
  평균공시이율 of 2.50%**, down from 2.75% and its first fall since 2020, which is the level
  `prem_int_rate` takes. Retrieved: in part.
- **REG-R49** — 상법 제4편 제1장 통칙 (제638조~제664조): 제638조의3 (품질보증해지) and 제662조
  (the **3년 소멸시효** on a 보험금청구권), both of which the specification's
  contract-mechanics table states. Retrieved: yes (제4편 read in full).
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): **제736조**, under which an
  insurer refusing a claim must still pay 「보험수익자를 위하여 적립한 금액」 — the reason a
  refused CI claim on this chassis is not a nil event. Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (**청약의 철회**): the statutory cooling-off the
  표준약관 implements, including that it does **not** apply to a 진단계약 — which is the
  common underwriting route for this product. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: 제7항 gives 사고보험금 a separate and additional
  ₩100,000,000 limit beside 해약환급금, and excludes benefits payable because the policy term
  has ended. Retrieved: yes.
- **REG-R54** — 노인장기요양보험법 제2조 등: the statutory definition of the 장기요양 state —
  「일상생활을 혼자서 수행하기 어렵다고 인정되는 자」 — which is the trigger the `ltc` limb of
  the CI benefit points at, and the frame for the 90-day wait and its 재해 carve-out.
  Retrieved: yes.
- **REG-R55** — 노인장기요양보험법 시행령 제7조 and [별표 1] (등급판정기준): the **1·2등급**
  boundary the CI 약관 adopts, with 3–5등급 and 인지지원등급 below it, and the **노인성 질병
  route below 65** that this model does not implement at all. Retrieved: yes (Decree text;
  별표 1 as a 1-page PDF).
- **REG-R57** — 소득세법 제59조의4 (특별세액공제 — 보장성보험료): the **12% credit on up to
  ₩1,000,000** of premium — a credit, not a deduction. Retrieved: yes.
- **REG-R59** — 상속세 및 증여세법 제8조·제34조: a death benefit as estate property where the
  deceased was in substance the payer. **The acceleration changes this in a way the chassis
  has no occasion to state**: the CI payment is a living benefit received by the insured, so
  what falls into the estate under 제8조 is the residual. Retrieved: yes.
- **REG-R60** — 한국회계기준원, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」: the
  standard in force in Korea since **2023-01-01**, cited as the layer that consumes these
  cash flows. **Retrieved: in part** — the release body returned, the 별첨 HWP carrying the
  standard's own text did not.
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: the **published** morbidity
  reference rates — a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid and a 질병입원율 grid.
  Cited here for one contrast only, and it is an important one: this is the basis
  `Cancer_KR_S` sources from, and it **does not reach this product**, because the
  insured-cancer definition it is stated on is not the 중대한 암 definition. Retrieved: yes.

---

## Provenance note

Every entry above traces to `_research/ci-insurance.md`, which is the citation ground truth
for this product: the S# and R# numbering used here is that file's numbering, unchanged,
and it is **never renumbered** because these documents cite against it. **The research
file's own numbering is not this one's** — it is the same S1–S8 and R1–R16 here only
because the CI evidence base is small enough that every entry earned a citation. In other
products of this library the two lists diverge, and a reader moving between them must
resolve tags against the product's own `sources.md` and never against a neighbour's.

What lives in the research file and not here: the section-by-section fact extraction — the
중대한 암 / 급성심근경색증 / 뇌졸중 definitions quoted verbatim from [S1 별표4] with their
exclusion lists, the 중대한 수술 and 화상 definitions, the 장해분류표 gate as the 약관 states
it, and the full 보험금 지급기준표; the four published premium grids and the arithmetic that
recovers the monthly premium from [S3]'s 해지환급금 illustrations; the carrier-by-carrier
variation table; the retrieval method per host, including which PDF extractor recovered
which file and where `pypdf`'s `/UniKS-UTF16-H` warning makes a quotation unsafe; and the
register of fetch failures and [unverified] claims.

That register is short and every item in it is load-bearing, so it is worth naming here:
**the 경험생명표 rates** (released as summary statistics only [REG-R33] [REG-R34]); **any
life 참조순보험요율** and any CI item at all on the bureau's public channels [REG-R4];
**[S3]'s female mortality at ages 40 and 60**, a PDF column-merge artefact and expressly
unused; **[S8]**, the market leader's product page, HTTP 503 on both attempts, so every
fact about that product is second-hand; **the K-ICS 대량해지 별표 22** [REG-R26], known only
through [REG-R36]; **the IFRS17 계리가정 가이드라인's functional form** [REG-R27] [R3],
whose values were retrieved and whose HWP attachment was not; **the K-IFRS 1117 standard
text** [REG-R60]; **[R11]'s 130% / 180% acceleration figures**, which cannot be a pure
acceleration as reported; and **every expense, commission, lapse, waiver-incidence,
policy-loan take-up, post-CI mortality and CI claim-denial figure in the Korean market**,
none of which any carrier or regulator publishes. Those absences are why `model.md`'s
standardization table has an "Observed range" column that reads *none published* on so many
of its rows.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-ci_insurance-r1
[R11]: #krlib-ci_insurance-r11
[R2]: #krlib-ci_insurance-r2
[R3]: #krlib-ci_insurance-r3
[R4]: #krlib-ci_insurance-r4
[R5]: #krlib-ci_insurance-r5
[REG-R1]: #krlib-reg-r1
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R42]: #krlib-reg-r42
[REG-R52]: #krlib-reg-r52
[REG-R60]: #krlib-reg-r60
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
