# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/long-term-care.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is per
product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md` runs
its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read
across.** The sharpest instance in this product is [R4], the 2024 노인장기요양보험 통계연보,
against [REG-R4], which is 보험업법 **제176조** (보험요율 산출기관); and [R12], 보험업법
제4조, against [REG-R12], which is 감독규정 제6-11조의7 (계약자배당). Access date for every
entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 상품요약서 (the statutory summary of the 기초서류),
  a 보험안내자료, a 약관 (*yakkan*, policy conditions) or a carrier release. These are what
  make a contractual mechanic *sourced* rather than assumed. On this product they carry the
  whole contractual specification and, unusually, **two quantitative anchors as well**: [S1]'s
  예정이율 and its 예정위험률 grid, and [S2]'s premium rate card and 환급률 progression.
- **[R#]** — a regulatory, statutory, statistical or market reference that only this product
  needs. The load-bearing one is [R4], the 2024 노인장기요양보험 통계연보, from which the
  entire morbidity basis is built; [R7] and [R11] carry the dementia rider and the post-onset
  survival evidence. Four of the seventeen — [R15] to [R18] — are **news or trade press**, one
  more ([R13]) is a vendor's restatement of a decree, and every entry says so.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Every tag used in the three documents has an entry here, and every entry here is used.** No
source was added at drafting. One research entry is **omitted as uncited**: `R5`, the
국민건강보험공단 경영공시 「장기요양 등급 판정 현황」, which was retrieved only in part and
whose three recovered figures agree exactly with [R4]. The same disclosure is a cross-product
entry, [REG-R42], and the documents cite that instead, which is why the gap exists rather than
a duplicate.

**Where the quantitative basis comes from, in one paragraph.** Nothing in this product's
decrement basis is a published insurance table, because none exists: 경험생명표 is not released
in full [REG-R33] [REG-R34], and **보험개발원 publishes neither a 장기요양 incidence table nor
a post-onset mortality table** — the 참조순보험요율 display that gives `Cancer_KR_S` its
incidence grid [REG-R61] carries nothing for this trigger. So the mortality table is a [std]
construction on a published 기대여명, the morbidity basis is converted in the open from the
public prevalence of [R4], the post-onset mortality multiple rests on [R11] and a duration
bracket derived from [R4] and [R18], and the one Korean long-term-care incidence rate anyone
publishes — [S1]'s 예정위험률 — is used for its gradient and as a cross-check, never as a
level. `model.md` lists every standardization with its rationale and whatever observed range
the documents bound.

Company and branded product names appear in this file and in `_research/long-term-care.md` and
**nowhere else** in the library: in `product-spec.md`, `technical-notes.md`, `model.md` and the
model docstrings a carrier is referred to by its tag alone, so a reader can always resolve who
said what — here — and never has to.

---

## Primary product sources

Five documents from five carriers, on **both sides of the market**: two life-side documents
[S1] [S2], two non-life 약관 [S3] [S4] and one life-side press release [S5]. That spread is a
product fact rather than a sampling choice — 간병보험 is a 제3보험 종목 that both licences may
write [R12] [REG-R1], and the non-life shelf is the larger one. Note where the documents
actually came from: [S3] from the carrier's own publication server and [S4] from a **bank's**
insurance-document mirror, not from the 손해보험협회 portal; no document in this set was
reached through an industry association.

**Retrieval method, common to the set.** Plain `curl` is blocked for every Korean host tried,
so everything was fetched with a summarising fetcher, which renders HTML but returns Korean
PDFs as undecodable binary; in every such case the saved binary was extracted locally with
`pypdf` and read directly. That is how the four PDFs below were obtained.

(krlib-long_term_care-s1)=

### S1 — 우정사업본부(우체국보험), 「무배당 우체국간병비보험 2309 상품요약서」 (statutory product summary)

- Publisher: 과학기술정보통신부 우정사업본부 (Korea Post Insurance), sold through 체신관서;
  product code family `P400059, P400060`, 36 pp.
- Doc type: **상품요약서** — a 기초서류 extract, not marketing copy
- URL: `https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/yoyak_P400059,P400060.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (323.7 kB PDF, 36 pp., text extracted with `pypdf`
  and read in full)
- **The richest single document in the set, and the only one disclosing a pricing basis.** What
  rests on it: the **예정이율 of 2.0% 연단위 복리**, which is `prem_int_rate` and the one
  retrieved pricing interest rate anywhere in this product; the **예정위험률 table —
  요양(1등급) and 요양(2등급) 발생률 at 만나이 40, 50 and 60 by sex** — which is
  `incidence_table.csv`, the sub-65 gradient `sub65_factor_at`, the sex ratio and the
  calibration target of `disclosed_inc_ratio_at`; the 간병자금 annuity shape — monthly
  instalments over ten years, **first twelve months guaranteed, 120-month cap**, the first
  instalment in the month of certification, the amount fixed by the grade at first
  certification and never re-rated, and the **annual 주민등록등본 proof of life** that makes
  `ann_tests` an annual count; the **freeze of the 감액 decision** at first certification,
  quoted verbatim in the notes; the **180-day 보장개시일 with its 재해 carve-back and a
  two-year 50% 감액** — the combination model point 9 carries; the bar on surrender once the
  annuity has started, which is why `pols_care` carries no lapse; the 가입나이 / 보험기간 /
  납입기간 grids; the 표준형 surrender-value form; the 12% 세액공제 statement; and the
  간병인사용일당 rate that `model.md` names as a **frequency, not a probability**.

(krlib-long_term_care-s2)=

### S2 — ABL생명, 「(무)ABL우리가족THE케어간병보험(해약환급금 미지급형)2504」 상품안내장

- Publisher: ABL생명보험주식회사; 16 pp., 제작 2025-09-01, 준법감시인 심의필 제2025-PA276호
- Doc type: **보험안내자료** — the regulated pre-sale disclosure document under 보험업법 제95조
- URL: `https://abllife.co.kr/cms/prdt/hlthInjry/__icsFiles/afieldfile/2025/08/28/` +
  `(무)ABL우리가족THE케어간병보험(해약환급금_미지급형)2504_20250901.pdf` (served
  percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (1.76 MB PDF, 16 pp., extracted with `pypdf` and
  read in full)
- **The most modern product in the set and the source of both published numeric series the
  model consumes.** What rests on it: the **월납 premium rate card at ages 40 / 50 / 60 by sex
  for 25 covers**, from which the anchor cell's ₩5,600 and the female ₩8,400 are built, and
  from which the market's own ≈ 4.5 : 1 threshold ladder and its opposite sex pricing on
  장기요양 and 치매 are derived; the **해약환급금 미지급형 환급률 progression** — 0.0% to year
  15, 48.7% at 20, 54.4% at 30, 50.5% at 40, 0.0% at 50 — which *is* `av_table.csv` and
  therefore `net_prem_ratio()`; the statement that the 기본형 comparator 「가입이 불가능하며 …
  해지율을 적용하지 않고 계산합니다」, which is the named weakness in that reconstruction; the
  **90-day 장기요양상태 보장개시일** and the **one-year 치매 보장개시일** with the 90-day
  persistence test inside each CDR definition, together `dementia_wait_mths = 15`; the
  utilisation-conditioned 재가/시설/주야간보호/복지용구 지원금 riders that the absorbing-state
  simplification would **not** survive; and the 간편심사 question set behind `uw_loading`.

(krlib-long_term_care-s3)=

### S3 — 삼성화재해상보험, 「무배당 삼성화재 간병보험 1808.2 (새시대 간병파트너)」 보험약관

- Publisher: 삼성화재해상보험주식회사, 장기상품개발2파트, printed 2018-08; 234 pp.
- Doc type: **policy conditions (약관)** — a full primary contract document, with the 가입자
  유의사항, the 주요내용 요약서, the 보통약관 and the 특별약관 집
- URL: `https://www.samsungfire.com/publication/pdf/ZPB214010_0_20180802_file1.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (8.4 MB PDF, 234 pp.; body text extracts cleanly,
  cover art and some marketing pages come out as mojibake and were skipped)
- A **non-life carrier's** grade-triggered design and the only document with a genuine
  multi-tier trigger menu — 기본계약 장기요양지원금(1~2등급) plus selectable 1등급 / 1~3등급 /
  1~4등급 tiers and a 5년간 매월 생활자금. What rests on it: the **납입면제 firing on the same
  event as the benefit and waiving every attached rider**, which is why `premiums` rides on
  `pols_act` and the waiver is not an independent decrement; 만기환급금 : 없음, which is why
  `claims_maturity` is a column of zeros; the absence of any general death benefit; the
  **statutory-amendment rewriting clause** — the contract-continuity answer to a trigger the
  insurer does not control; and the 두 번째 장기요양지원금 rider with its five-year 면책, the
  market's own acknowledgement that grades move.

(krlib-long_term_care-s4)=

### S4 — 한화손해보험, 「무배당 한화 골드클래스 간병보험」 약관 (policy conditions)

- Publisher: 한화손해보험주식회사; document revision date 2023-07-11 (PDF metadata); 173 pp.,
  four plans including 간병보장플랜(납입중50%해약환급금지급형)
- Doc type: **policy conditions (약관)**
- URL: `https://image.kebhana.com/cont/download/insdocument/provide/N02C14145_agree.pdf` — a
  **bank's** (하나은행) insurance-document mirror, not the carrier's own site
- Accessed: 2026-09-03, Retrieved: **yes** (6.6 MB PDF, 173 pp.; the 유의사항, the 감액/면책
  tables and the 장기요양진단비 and 치매진단비 articles read verbatim)
- What rests on it: the **verbatim 지급사유 articles** at each threshold from 1등급 to 1~5등급
  with the **one-year 50% 감액 table set out inside the article**, which fixes `red_fraction`
  and the fact that the test is on the **cause** — 질병 halved, 상해/재해 in full — behind
  `disease_share`; the CDR definitions of 경증이상 / 중등도이상 / 중증치매 each with a 90-day
  persistence test, and the **one-year full 면책** on the dementia riders against **no 면책**
  on the 장기요양 riders; the 「납입중50%해약환급금지급형」 mechanics, which are `cv_form =
  half_during`; and the exclusion referring to 노인장기요양보험법 제29조.

(krlib-long_term_care-s5)=

### S5 — 교보생명, 「교보더안심치매·간병보험」 출시 보도자료 (carrier press release)

- Publisher: 교보생명보험주식회사 (own newsroom); reported launch 2026-02-25
- Doc type: **carrier press release** — not a contract document; every fact from it is a
  carrier's summary of its own product and is weaker evidence than [S1] – [S4]
- URL: `https://news.kyobo.com/교보생명-교보더안심치매간병보험-출시/` (percent-encoded live)
- Accessed: 2026-09-03, Retrieved: **yes** (HTML rendered)
- Used for market spread only, never for a modelled parameter: a current whole-of-life
  치매·간병 design with 진단자금 at three CDR tiers plus a **매월 생활자금 for life with a
  36-instalment guarantee**, 1~5등급 and 인지지원등급 cover with separate 재가 / 시설 /
  방문요양 이용수당 riders, a premium refund on a 1~4등급 진단, 가입나이 30~75세 and 보험기간
  종신. It is the evidence that the 120-month cap the composite carries is a *choice* among
  observed shapes rather than the only one on sale.

---

## Regulatory and actuarial references

Seventeen entries: three statutory or official restatements [R1] [R2] [R3], four official
statistical or fiscal sources [R4] [R6] [R7] [R11], three research-institute or supervisory
documents [R8] [R9] [R10], two further legal entries [R12] [R13], one supervisory guideline
that was **not** retrieved in original [R14], and four news or trade-press items [R15] – [R18]
whose figures inherit that weakness and are labelled at every point of use.

(krlib-long_term_care-r1)=

### R1 — 노인장기요양보험법 (Act on Long-Term Care Insurance for the Aged)

- Publisher: 국가법령정보센터 (법제처). Doc type: statute
- URL: `https://www.law.go.kr/LSW/lsInfoP.do?lsId=010436&ancYnChk=0` (index); article text
  through the print form `https://www.law.go.kr/LSW//lsBdyPrint.do?…&joNo=<NNNN>:00&…`
- Accessed: 2026-09-03, Retrieved: **in part** — the index page returns only the site chrome
  and the currency line (현행 법률 제21690호, 시행 2026-05-26). The **per-article print form
  works**: 제2조, 제15조 and 제23조 were retrieved in full, but at the **2018-09-14
  consolidation**, so every article text quoted from it is the 2018 text and is flagged as
  such at the point of use
- Establishes the scheme the benefit trigger belongs to: 제2조's 「노인등」 and 장기요양급여,
  제15조's 등급판정 and the **delegation of the grade boundaries to 대통령령** — the
  basis-change risk the insurer does not control — and 제23조's exhaustive 급여 list. The
  시행령 detail is cited from [REG-R55], which was retrieved at current consolidation.

(krlib-long_term_care-r2)=

### R2 — 노인장기요양보험법 시행령 [별표 1] 「노인성 질병의 종류」 (제2조 관련)

- Publisher: 국가법령정보센터; 개정 2022-12-20. Doc type: annexe to a presidential decree
- URL: `https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=135370071&bylClsCd=110201`
- Accessed: 2026-09-03, Retrieved: **yes** (1-page PDF, extracted cleanly, full table read)
- The closed list of **25 diseases with KCD codes** that alone let a person under 65 be
  certified — four dementia codes, one Alzheimer, fourteen cerebrovascular, four
  Parkinson-family, plus 척수성 근위축, 다발경화증, 중풍후유증 and 진전. It is why the model
  has **no prevalence data at all below 65** and carries the two entry rates down on
  `sub65_factor_at` instead, and why no cancer, musculoskeletal or frailty route exists below
  that age.

(krlib-long_term_care-r3)=

### R3 — 찾기쉬운 생활법령정보, 「노인장기요양보험 > 등급판정 절차 및 기준」

- Publisher: 법제처 (easylaw.go.kr). Doc type: official plain-language restatement
- URL: `https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2038&ccfNo=2&cciNo=2&cnpClsNo=1`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML rendered)
- The **장기요양인정점수 band table** for 1등급 through 인지지원등급 with each grade's 심신
  기능상태, cited to 법 제15조 and 시행령 제7조제1항, and the **30-day determination deadline**
  with a 30-day extension (법 제16조제1항). The deadline is what fixes the model's claim-date
  convention at the **판정일**; the bands corroborate [REG-R55], read at first hand.

(krlib-long_term_care-r4)=

### R4 — 국민건강보험공단, 「2024 노인장기요양보험 통계연보」

- Publisher: 국민건강보험공단 빅데이터사업실, 발간 2025-06-30. Doc type: **official national
  statistics** (국가승인통계)
- URL (landing): `https://www.nhis.or.kr/nhis/together/wbhaec07200m01.do`; the attachment
  actually used: the same path with `?mode=download&articleNo=11003958&attachNo=368127`
- Accessed: 2026-09-03, Retrieved: **yes, in the form that matters.** The yearbook PDF
  (`attachNo=361507`) **failed** — the fetcher refused it at `maxContentLength size of
  10485760 exceeded` — and the 해설서 (`attachNo=364866`) is an HWP 5.0 compound document that
  was not decoded. The third attachment (5.6 MB) is a **ZIP of five `.xlsx` workbooks holding
  the yearbook's complete numerical tables**, which were read with `openpyxl`. Every figure is
  cited **by table number**, never by page, because the paginated PDF was never opened
- **The single most load-bearing source in this product.** 표2-9 (등급별 × 연령별 판정 현황)
  and 표1-2 (65세 이상 적용인구 by five-year band and sex) give the 연령별 인정률 that is
  `prevalence_table.csv` and the age-banded grade composition that is `grade_share_table.csv`;
  표2-5 (인정신청 구분별) gives the 13.3% / 69.8% first-application split behind
  `direct_entry_share` and the 107,365 등급변경신청 that bounds the absorbing-state
  simplification; 표2-1 and the 인정자 series give the stock growth and the duration bracket
  behind `care_mort_mult`. Everything in the morbidity basis traces here.

(krlib-long_term_care-r6)=

### R6 — 국회예산정책처, 「2018~2027년 노인장기요양보험 재정전망」 (2018-12)

- Publisher: 국회예산정책처 추계세제분석실 사회비용추계과. Doc type: legislature budget-office
  fiscal projection, 94 pp.
- URL: `https://www.nabo.go.kr/board/file/down.do?fid=33315305`
- Accessed: 2026-09-03, Retrieved: **yes** (1.5 MB PDF, extracted and read)
- The clearest published description of the **assessment instrument** — 12개 영역 90개 항목
  surveyed, **52개 항목** entering the 장기요양인정점수 across ADL, IADL, 인지기능, 행동변화,
  간호처치 and 재활 — and of the **creation of the 인지지원등급 on 2018-01-01**, which is the
  library's standing example of a trigger enlarged by decree at no additional premium, and the
  level shift that contaminates any Korean experience series crossing that date.

(krlib-long_term_care-r7)=

### R7 — 보건복지부, 「2023년 치매역학조사 및 실태조사 결과 발표」 보도자료

- Publisher: 보건복지부 (배포 2025-03-13); survey by 중앙치매센터, 한국보건사회연구원 and
  한국갤럽. Doc type: government press release announcing an official epidemiological survey
- URL: `https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&act=view&list_no=1484959`
- Accessed: 2026-09-03, Retrieved: **yes** for the release body (HTML). The two 별첨
  attachments and the `attachPreview.es` viewer returned chrome only, so **the survey's
  diagnostic instrument is [unverified]** — which matters because the private trigger is the
  CDR and a prevalence measured on another instrument is not directly transferable
- The dementia rider's whole basis: 65세 이상 유병률 **9.25%**, the **five band prevalences**
  (65-69 4.99%, 70-74 5.03%, 75-79 10.70%, 80-84 15.57%, 85+ 21.18%) that are
  `dementia_table.csv`, and the sex split (남 8.85%, 여 9.57%) that is `dem_factor_m` /
  `dem_factor_f` — including the 65-79 / 80+ crossover the model's flat-in-age factors do not
  reproduce, which `model.md` names as a weakness.

(krlib-long_term_care-r8)=

### R8 — 보험연구원, 「최근 치매보험시장의 이슈와 과제」 (KIRI 이슈분석, 2019-05-13)

- Publisher: 보험연구원 (정성희, 문혜정). Doc type: research-institute analysis, 4 pp.
- URL: `https://www.kiri.or.kr/pdf/전문자료/KIRI_20190510_9467.pdf` (percent-encoded live)
- Accessed: 2026-09-03, Retrieved: **yes** (272 kB PDF, read in full)
- The definitive account of the **2018–2019 치매보험 boom** — 초회보험료 약 233억 원 in 2018,
  3.5× the prior year — the CDR scale with its seven points, the 약관 defect that produced the
  supervisory intervention, the industry's self-imposed ₩30,000,000 aggregate limit, and the
  epidemiology behind the tier ladder: **경증치매 is 67% of all dementia cases**, which is what
  the product-spec checks the market's own ≈ 3 : 1 tier pricing against.

(krlib-long_term_care-r9)=

### R9 — 보험연구원, 연구보고서 2019-11, Ⅱ장 「우리나라 장기요양서비스/보험의 현황 및 평가」

- Publisher: 보험연구원. Doc type: research report chapter, 30 pp. in the retrieved extract
- URL: `https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2020-0129_2.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (651 kB PDF, extracted and read)
- The **three benefit-trigger archetypes** taken from a 2012 금융감독원 release — ① 회사기준, ②
  **공적기준**, ③ 혼합형 — with the finding that 「일반적으로 간병보험에서는 공적기준을
  적용하는 경향이 있다」, which is the taxonomy this product's design sits in and the reason
  the composite is a type ②. Also the public/private comparison (근거법, 도입시기 2003-08
  against 2008-07, 현물 against 정액), the 2019 product count (99 products, 생보 46 / 손보 53),
  the 간병보험 가입률 of **2.5%**, and the statement that 보험개발원 publishes no
  long-term-care incidence table — the negative result the whole basis construction follows
  from.

(krlib-long_term_care-r10)=

### R10 — 금융감독원, 「치매보험금 분쟁을 선제적으로 예방할 수 있도록 보험약관을 개선하겠습니다」

- Publisher: 금융감독원, 2019-07-02. Doc type: supervisory press release announcing a 약관
  변경권고
- URL (as retrieved): `https://eiec.kdi.re.kr/policy/materialView.do?num=190159` — the KDI
  경제교육·정보센터 **mirror**; the FSS original was not located
- Accessed: 2026-09-03, Retrieved: **yes**, through the mirror
- The two reforms that fixed the current dementia design: a 치매진단 must rest on a
  **comprehensive clinical assessment** rather than on imaging as a gate, and 특정 치매질병코드
  and 약제투약 conditions were deleted from 약관. Revised products went on sale from **October
  2019**, which is why `dementia_wait_mths` is a market answer and not a carrier choice — and
  why a Korean dementia experience series spanning 2019 is contaminated at the level of the
  benefit **definition**.

(krlib-long_term_care-r11)=

### R11 — 한은정·황라일·이정석, 「장기요양 인정자의 사망 전 의료 및 요양서비스 이용 양상 분석」

- Publisher: 한국사회정책 제25권 제1호 (2018), pp. 99–123; authors at 국민건강보험공단
  건강보험정책연구원 and 신한대학교. Doc type: peer-reviewed journal article on the NHIS claims
  census
- URL: `https://journal.kci.go.kr/kasp/archive/articlePdf?artiId=ART002331210`
- Accessed: 2026-09-03, Retrieved: **yes** (1.8 MB PDF; abstract, methods and results read)
- **The only post-onset survival evidence retrieved anywhere.** 271,474 people certified
  2008-07 to 2012-12 who also died inside that window: mean time from 등급인정 to death
  **516.2 days**, 8.7% inside one month, 45.6% inside one year; 74.7% aged 75 or over; mean
  장기요양인정점수 at death **82.1**, inside 2등급. **The sample is truncated by construction**
  — only people who died inside a 4.5-year window are in it — so 516.2 days is a lower bound
  on duration, which is why `care_mort_mult = 3.0` takes its *shape* from this study and its
  *level* from the yearbook duration bracket, and why `light_mort_mult` is bounded below the
  care multiple by the 82.1 mean score.

(krlib-long_term_care-r12)=

### R12 — 보험업법 제4조 (보험업의 허가)

- Publisher: 국가법령정보센터. Doc type: statute
- URL: `https://www.law.go.kr/LSW/lsSideInfoP.do?lsiSeq=265389&joNo=0004&docCls=jo&…`
- Accessed: 2026-09-03, Retrieved: **in part** — the article's structure and 제1항제3호 were
  returned, but not the full sub-paragraph 목 lettering; the identical article is retrieved
  from a mirror in `_research/ci-insurance.md` and as [REG-R1] here
- 제3호 **제3보험업** comprises 상해보험, 질병보험 and **간병보험**: long-term care is a
  statutory 보험종목 in its own right and not a sub-species of 질병보험, writable by both
  licences — which is why the two life-side and two non-life documents in this file describe
  the same benefit.

(krlib-long_term_care-r13)=

### R13 — 노인장기요양보험법 시행령 제8조 (장기요양인정 유효기간), 2025-07-01 개정

- Publisher: 보건복지부 / 국민건강보험공단, retrieved through a long-term-care software
  vendor's customer notice restating the amendment. Doc type: **secondary** — a vendor notice,
  not the decree
- URL: `https://www.carefor.co.kr/cs/view_notice.php?calmgno=45794&…`
- Accessed: 2026-09-03, Retrieved: **yes**, but as a restatement. **The decree text itself was
  not retrieved**, so the values are [unverified]
- The base 유효기간 of **two years**, extended on renewal at the same grade — 1등급 4 → 5
  years, 2~4등급 3 → 4, 5등급 and 인지지원 unchanged. Used in `technical-notes.md` **only
  inside the duration estimator's sensitivity**, never as a load-bearing input, precisely
  because it is a restatement.

(krlib-long_term_care-r14)=

### R14 — 금융위원회·금융감독원, 「IFRS17 주요 계리가정 가이드라인」 (2024-11-07)

- Publisher: 금융위원회 / 금융감독원. Doc type: supervisory guideline — **not retrieved in
  original**
- URL (release index): `https://www.fsc.go.kr/no010101/83351`
- Accessed: 2026-09-03, Retrieved: **no.** The content comes from contemporaneous press
  accounts surfaced in search and is **secondary**; the same guideline is cited from a
  retrieved 보도자료 as [REG-R27]
- The **log-linear lapse model converging to 0% at the premium-completion point** as the
  원칙모형 for 무·저해지 business, with 선형-로그 and 로그-로그 permitted by exception subject
  to quarterly disclosure of the difference. The two endpoint values are verified from
  [REG-R27]; **the functional form is [unverified] at instrument level**, and `lapse_rate(t)`
  says so.

(krlib-long_term_care-r15)=

### R15 — 헤럴드경제, 「금융당국, 간병인보험 구조 진단 착수」

- Publisher: 헤럴드경제 (biz.heraldcorp.com). Doc type: **news article**
- URL: `https://biz.heraldcorp.com/article/10797305`
- Accessed: 2026-09-03, Retrieved: **yes**
- The 간병인사용일당 loss-ratio record — life sector near **100% at August 2024** against 18.7%
  two years earlier, non-life 83.1%, premium at the five largest non-life carriers up roughly
  twenty-fold in four years. Cited **only to scope that product out**: it is a hospital-days
  frequency-severity cover that shares nothing with this one but the word 간병, and a reader
  comparing Korean market commentary against this library would otherwise conflate the two.

(krlib-long_term_care-r16)=

### R16 — 보험신보, 「이슈 — 장기요양등급 인증자 증가하는데」

- Publisher: 보험신보 (insweek.co.kr). Doc type: **news / trade-press feature**
- URL: `https://www.insweek.co.kr/news/articleView.html?idxno=64798`
- Accessed: 2026-09-03, Retrieved: **yes**
- The 인정자 and 노인인구 대비 인정률 series 2018–2023, whose 2020-onward values agree with
  [R4] and which give the **71.8% six-year stock growth** behind the stationarity caveat;
  private-market penetration at 2023; the 생명보험협회 2022 survey in which **40.8%** named
  간병보험 as the cover they would buy next; and a survey of 2024–2025 product launches. Every
  figure inherits the source's weakness and is labelled a news figure at each use.

(krlib-long_term_care-r17)=

### R17 — 생생비즈, 「치매 환자 100만명 시대 커지는 치매·간병보험 시장…작년 70% 급성장」

- Publisher: 생생비즈 (livebiz.today). Doc type: **news article**
- URL: `https://www.livebiz.today/news/articleView.html?idxno=6054`
- Accessed: 2026-09-03, Retrieved: **yes**
- 치매·간병보험 초회보험료 of **₩88.4bn for January–November 2024, +70.2%** year on year, the
  계속보험료 series, and a product survey naming the CDR 검사지원비 and lecanemab covers that
  `product-spec.md` records as out-of-scope market features. Market context only; no modelled
  parameter rests on it.

(krlib-long_term_care-r18)=

### R18 — 헬스코리아뉴스 and 백세시대, 2024 통계연보 launch coverage

- Publisher: 헬스코리아뉴스 (hkn24.com); 백세시대 (100ssd.co.kr). Doc type: **news articles**
  reporting the yearbook's release
- URLs: `https://www.hkn24.com/news/articleView.html?idxno=345333` ;
  `https://www.100ssd.co.kr/news/articleView.html?idxno=123152`
- Accessed: 2026-09-03, Retrieved: **yes** (both)
- Used as a **cross-check on [R4]** and for the five-year 인정자 series 857,984 (2020) →
  1,165,030 (2024) that gives the roll-forward estimator its **+67,117 net increase** and hence
  the 4-to-5.5-year duration bracket behind `care_mort_mult`. Every figure that also appears in
  [R4] agrees with it, which is the point of carrying a news source here at all.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that page
plain [R#] refers to its own entries, so the two schemes must never be read across. The
forty-one entries this product's documents cite, all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: the 생명보험 / 손해보험 / **제3보험** split and the
  제4조제3항 deeming provision that lets both licences write 간병보험. Retrieved: yes. Cited
  beside this file's [R12].
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is filed with the FSC and
  never published**, which is why the office premium is a model-point input and every pricing
  parameter not in [S1] is [std]. Retrieved: yes.
- **REG-R3** — 보험업법 제120조: the statutory duty to accumulate 책임준비금, cited as a layer
  this model does not compute. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): 참조순보험요율 are **filed, not
  published** — the statutory reason a Korean morbidity basis is not simply looked up.
  Retrieved: yes. **Not** this file's [R4].
- **REG-R5** — 보험업법 제181조·제184조: the 선임계리사 who owns the basis and its
  verification. Retrieved: yes.
- **REG-R7** — 보험업법 시행령 제1조의2 (보험상품): the closed product scope, cited in the
  boundary paragraph that separates this private contract from the public scheme. Retrieved:
  yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호): the **기준연령 요건** 「남자가 만 40세」 that
  makes the anchor cell the prescribed disclosure cell, and the finding that a full-text search
  of the 고시 returns **zero occurrences of 예정이율**. Retrieved: yes (226,083 characters).
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the reserve taxonomy, cited and
  not computed. Retrieved: yes.
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the Korea-only appropriation that
  measures against a 제7-66조제1항 surrender value **even for 제4항 products that contractually
  pay less** — which is exactly this product's 미지급형 form. Retrieved: yes.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당): what a **무배당** contract switches
  off. Retrieved: yes. **Not** this file's [R12].
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS**): in force from 2023-01-01, cited in the
  measurement-basis paragraph; no 요구자본 is computed. Retrieved: yes (the 별표 22 detail was
  not).
- **REG-R14** — 감독규정 제7-17조~제7-19조 (적기시정조치) and the 고시 transition: the
  thresholds behind the "both regimes commenced together" statement. Retrieved: yes.
- **REG-R17** — 감독규정 제7-63조 (제3보험의 보험상품설계): **제1항제1호** requires payment of
  the **계약자적립액** on death from a cause the policy does not cover, and termination. It is
  the whole of `claims_death` — a third of premium income on the anchor cell — and it is the
  single most load-bearing cross-product entry for this product. Retrieved: yes.
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액): the 필수기재사항, the
  현금흐름방식 requirement, and the accrual of the 계약자적립액 **monthly before 납입완료 and
  daily after**, which is the timing `av_pp` implements. Retrieved: yes (the accrual formulas
  did not extract).
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): the 계약자적립액 − 해약공제액 floor at
  zero, the **해약공제기간 capped at seven years** that bounds `surr_chg_pp`, and **제4항**,
  which permits the 미지급형's reduced value precisely because premiums were computed on a
  최적해지율 — so the lapse vector is a condition of the form's legality. Retrieved: yes.
- **REG-R20** — 감독규정 [별표 14] 표준해약공제액: the statutory cap the 13-months rule of
  thumb stands in for. Retrieved: yes (1-page PDF, full text).
- **REG-R21** — 감독규정 [별표 15] 보험가입금액의 산정: **제9호 excludes** 「치매 또는
  일상생활장해 등 타인의 간병을 필요로 하는 상태」 risk premium from the ratio that gives a
  contract with no death benefit its notional 보험가입금액 — read literally, the schedule
  cannot be applied to a care-only contract, which is why `surr_chg_ratio` uses [REG-R29]'s
  rule of thumb instead. Retrieved: yes (1-page PDF).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조: the commission cap behind `comm_init_mths`
  and the 보험가격지수, the ratio that exists because a Korean consumer cannot see the pricing
  basis. Retrieved: yes.
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the supervisor's model conditions, and why the
  four carrier documents here agree almost word for word. Cited by article — 제21조 (보험나이,
  against which the model's 만나이 basis is stated), 제22조 (the 계약자적립액 on non-covered
  death), 제26조 (부활), 제33조 (보험계약대출, which this form has nothing to lend against),
  제17조 (청약철회). Retrieved: yes (a 492-page PDF read in full).
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금): **Retrieved: no.** The
  **대량해지 shock**, including the 고환급형 test, is known only at second hand and anything
  resting on it is **[unverified]** — which matters here because the representative form is a
  무해지 one.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (2024-11-07, 계리가정·할인율): the source of
  `lapse_completion = 0.001` and `lapse_ultimate = 0.008`, of the log-linear 원칙모형 shape, of
  the disclosure requirement that makes shipping the `pyojun` comparison vector the right thing
  to do, and of the **63.8% 무·저해지 share of 2024 H1 보장성 초회보험료**. Retrieved: yes (the
  보도자료 and its 별첨; the guideline attachment itself is [R14], not retrieved).
- **REG-R28** — 무(저)해지환급금 상품구조 개선 (2020) and the FSS 소비자경보 (2019): the
  환급률 cap that shapes the published progression, and the **no-policy-loan** consequence that
  is a stated product limitation here. Retrieved: yes.
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여…」 (2019-08-01): the
  **13-months-of-premium** rule of thumb for a 보장성보험's 표준해약공제액 and the **60% cap**
  on annual commission — together `expense_acq_mths = 5.2` and `comm_init_mths = 7.8`.
  Retrieved: yes.
- **REG-R32** — 예금자보호한도 1억원 (2025-09-01): the protection sentence 표준약관 제43조
  requires the 약관 to carry. Retrieved: **in part**.
- **REG-R33** — 제10회 경험생명표, as reported: the **65세 기대여명 23.7 / 27.1** that
  calibrates `mort_table.csv` and the 평균수명 86.3 / 90.7 the construction reproduces without
  being asked to. Retrieved: yes — **a news article, and the only retrieved source for these
  figures**.
- **REG-R34** — 보험개발원 public channels: the evidence that the 경험생명표 is **not published
  in full**, which is why the mortality table is a construction rather than a copy. Retrieved:
  **in part**.
- **REG-R35** — K-ICS 경과조치 (KIRI): background for why a ratio quoted after 경과조치 is not
  comparable with one quoted before. Retrieved: yes.
- **REG-R38** — 「2024년 생명표 작성 결과」 / 「2023년 생명표」: the **public** 기대여명 anchor
  the insured-lives construction is compared against, and the 만나이 basis every public series
  here shares. Retrieved: yes.
- **REG-R39** — KOSIS 완전생명표 (single-year `qx`): **Retrieved: no** — distributed through
  KOSIS, which redirected to an SSO endpoint. The named to-do in the table-build note.
- **REG-R42** — 국민건강보험공단 「장기요양 등급 판정 현황」 (경영공시): the **2026-06-30**
  cross-check on the grade composition — 1등급 3.8% / 2등급 7.1% of all assessed — at a later
  as-of date and a wider denominator than [R4], with the same shape. Retrieved: yes.
- **REG-R43** — the 2024 통계연보 as reported by 메디칼월드뉴스: **Retrieved: no** (search
  summary only). Cited once, for a figure used **nowhere** in the model, and tagged
  [unverified] where it appears.
- **REG-R48** — 평균공시이율 / 공시기준이율 carrier disclosure: the evidence that **the
  예정이율 of a specific Korean product is not a published number**, which is what makes [S1]'s
  disclosure of 2.0% unusual enough to be worth naming. Retrieved: **in part**.
- **REG-R49** — 상법 제4편 제1장 통칙: the statutory floor under the contract — 제638조의3
  (약관교부·설명), 제651조 (고지의무), the three-year claim prescription. Quoted, not modelled.
  Retrieved: yes.
- **REG-R50** — 상법 제4편 제3장 인보험: **제736조 (보험적립금반환의무)**, the statutory floor
  beneath 감독규정 제7-63조제1항제1호's payment on a non-covered death. Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (청약의 철회): the 15/30-day withdrawal right, out of
  scope because the model starts from the point cover is in force. Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: the calculation basis behind the ₩100,000,000
  limit. Retrieved: yes.
- **REG-R54** — 노인장기요양보험법 제2조·제15조·제23조·제39조·제40조, at **current
  consolidation**: the statutory definition of 「노인등」 — the 만 65세 test that is *inside*
  the benefit definition and one of the two reasons this model runs on 만나이 — the 등급판정
  machinery and the 급여 list. Load-bearing, and the entry to prefer over this file's [R1],
  which is the 2018 text. Retrieved: yes.
- **REG-R55** — 노인장기요양보험법 시행령 제7조 (등급판정기준) and [별표 1]: the **점수 bands
  that are the statutory definition of this product's trigger** and the source of its
  grade-severity split, plus the 노인성 질병 list. Retrieved: yes (Decree text and the 별표 as
  a 1-page PDF).
- **REG-R57** — 소득세법 제59조의4 (보장성보험료 세액공제): the **12% credit on up to
  ₩1,000,000** of premium — a credit, not a deduction — inside which the anchor's ₩67,200
  annual premium sits comfortably. Not modelled. Retrieved: yes.
- **REG-R60** — K-IFRS 제1117호 제정 의결: IFRS 17 mandatory in Korea since **2023-01-01**,
  cited in the measurement-basis paragraph. **No `krlib` model computes a CSM or a risk
  adjustment.** Retrieved: **in part** (the standard text itself was not).
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: cited here for the
  **contrast** it draws. The display carries a published 암 발생률 grid, which is why
  `Cancer_KR_S` sources its incidence rather than standardizing it; it carries **nothing for
  장기요양**, which is why this product's basis has to be converted from a prevalence in the
  open. Retrieved: yes.

---

## Provenance note

Every entry above traces to `_research/long-term-care.md`, which is the citation ground truth
for this product: the S# and R# numbering used here is that file's numbering, unchanged, and it
is **never renumbered** because these documents cite against it. The research file's numbering
is not this one's — it runs to S5 and R18 and carries `R5`, which this file omits as uncited
for the reason given at the head of this page.

What lives there and not here: the per-document extraction record, table by named table for the
yearbook workbooks; the full arithmetic of the prevalence-to-incidence conversion and of the
two independent duration estimators; the carrier-by-carrier variation tables behind the
threshold, waiting-period, 감액 and surrender-value spreads; and the register of fetch failures
and their consequences. The last is worth summarising, because several of its entries are why
figures in these documents carry [unverified]:

- The **2024 통계연보 PDF itself** exceeded the fetcher's size limit and the **해설서** is an
  undecoded HWP, so the yearbook's own definitions of 인정자, 판정 and 수급자 are **inferred
  from the tables' totals** rather than quoted from the compiler — sound, because the totals
  reconcile, and stated rather than hidden. Citations are by table number, never by page.
- The **중앙치매센터 「대한민국 치매현황」** report was blocked by a web application firewall
  in every vintage, and the 보건복지부 별첨 viewer returned chrome only. So the dementia basis
  rests on the press release [R7] alone, and the survey's **diagnostic instrument is
  [unverified]**.
- **KOSIS** redirected to an SSO endpoint [REG-R39] and the **노인장기요양보험법 index page**
  returns only chrome, so the statute was read article by article at the 2018 consolidation
  [R1] with the current text taken from [REG-R54] and [REG-R55]; the 유효기간 comes from a
  vendor restatement [R13] and is used only inside a sensitivity.
- The **IFRS17 계리가정 가이드라인** attachment was never converted from HWP [R14], so the
  lapse model's functional form is [unverified] at instrument level while its two endpoint
  values are verified from the 보도자료 [REG-R27]; and **보험업감독규정 별표 22** was not
  retrieved [REG-R26], so the K-ICS 대량해지 shock is second-hand.
- Two carrier documents were lost: a fifth carrier's 간편심사 간병보험 약관 (HTTP 503) and a
  major non-life carrier's current disclosure, which is a **scanned image PDF with no text
  layer**. No 삼성생명 product parameter appears anywhere in this product, the largest life
  carrier being represented only by its non-life affiliate [S3] and by secondary mentions.

**What no source in this file provides, and no amount of further searching would.** There is no
published Korean long-term-care incidence table, no post-onset mortality table by grade, no
recovery or grade-transition matrix, no durational persistency series for a 보장성 contract, no
expense or commission scale, and no 질병 / 상해 split of certifications. Every one of those is
a **[std]** parameter in `model.md`, each with its rationale and whatever observed range the
retrieved documents bound — and for several of them, the honest answer recorded there is that
the documents bound nothing at all.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-long_term_care-r1
[R10]: #krlib-long_term_care-r10
[R11]: #krlib-long_term_care-r11
[R12]: #krlib-long_term_care-r12
[R13]: #krlib-long_term_care-r13
[R14]: #krlib-long_term_care-r14
[R15]: #krlib-long_term_care-r15
[R18]: #krlib-long_term_care-r18
[R2]: #krlib-long_term_care-r2
[R3]: #krlib-long_term_care-r3
[R4]: #krlib-long_term_care-r4
[R6]: #krlib-long_term_care-r6
[R7]: #krlib-long_term_care-r7
[R8]: #krlib-long_term_care-r8
[R9]: #krlib-long_term_care-r9
[REG-R1]: #krlib-reg-r1
[REG-R12]: #krlib-reg-r12
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R42]: #krlib-reg-r42
[REG-R54]: #krlib-reg-r54
[REG-R55]: #krlib-reg-r55
[REG-R61]: #krlib-reg-r61
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
