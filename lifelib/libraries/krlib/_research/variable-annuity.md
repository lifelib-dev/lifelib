# 변액연금보험 (variable annuity) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean separate-account deferred annuity liability cash flow reference
model (`variable_annuity` / `VA_KR_S`) — a unit-linked accumulation chassis run inside a
**특별계정** (*teukbyeol gyejeong*, separate account) with a minimum death benefit
(최저사망보험금보증, GMDB), an optional minimum accumulation benefit at the annuity
commencement date (최저연금적립금보증, GMAB), the guarantee charges that pay for them
(최저보증비용), the front-loaded expense stack that every Korean savings product carries
(계약체결비용 / 계약관리비용 / 위험보험료), and a surrender charge (해지공제) that runs off
over at most seven years.

This file is the **provenance layer** behind `products/variable_annuity/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Its source numbering — `S#` for primary
product documents, `R#` for regulatory and actuarial references — is **frozen once written**
and is never renumbered: the four product documents cite against it. Where a fact could not
be confirmed against a document actually retrieved in this session it is marked
`[unverified]` here and must stay `[unverified]` downstream. Access date for every fetch
below: **2026-09-03**.

**What the product is.** 변액연금보험 (*byeonaek yeongeum boheom*) is a two-phase contract.
In the **연금개시 전 보험기간** (pre-annuitisation period) the premium, net of the expense
loading and the mortality charge, is paid into a separate account and buys units (좌) at a
daily unit price (기준가격); the policyholder's account value (계약자적립액) moves with the
funds. At the **연금지급개시나이 계약해당일** the accumulated value — or, where a guarantee
was bought, a guaranteed floor — becomes the annuity consideration, and the contract usually
transfers to the general account (일반계정) and pays a declared-rate annuity at the 공시이율.
A minority of designs keep the money in the separate account through the payout phase and
guarantee a lifetime withdrawal instead (실적배당 종신연금 / GLWB). The pre-annuitisation
death benefit is the account value with the paid premiums as a floor.

**Its place in the Korean market.** Variable life insurance arrived in Korea in 2001
(변액종신보험), the variable annuity in **October 2002**, and the variable universal contract
in 2003 [R1] [R2]. The line grew to ₩17.9 trillion (17.9조원) of premium income in 2021 and
has fallen every year since — ₩12.7tn (2022), ₩12.2tn (2023), ₩11.6tn expected (2024) and
₩10.1tn forecast (2025) [R9] — while *new* business turned sharply the other way: first-year
premium (초회보험료) was ₩1.97tn in 2024 and **₩2.89tn in 2025, up 46.2%** [R3]. The product
is therefore simultaneously a shrinking in-force block and a hot new-business line, which is
exactly the configuration that draws supervisory attention; the FSS ran a mystery-shopping
exercise on variable-insurance sales in September–November 2025 and published the result on
2026-03-24 [R3].

**Why it is structurally interesting for a model.** Three features have no counterpart
elsewhere in this repository. First, the guarantee is a **put option written by the insurer
on the policyholder's own fund**, paid for by an explicit basis-point charge deducted from
the separate account and credited to a general-account 보증준비금 (guarantee reserve) whose
statutory floor is a CTE(70) calculation [R1]. Second, since **April 2016** the GMAB is
*optional*: the policyholder chooses whether to pay for it, so the same chassis has to
support a guaranteed and an unguaranteed form [R1] [R2]. Third, the insurer manages the
guarantee not only by charging for it but by **constraining the fund mix** — mandatory bond
weights, automatic rebalancing, automatic de-risking on a target hit, and in one design a
CPPI multiplier that replaces the guarantee charge entirely [S6] [R1].

**A note on nomenclature.** The same quantity is called 계약자적립금 in some contracts and
계약자적립액 in others; 최저사망보험금 (minimum death benefit) is variously 최저사망지급금,
최저사망적립금 and 최저사망계약자적립액. This file quotes each carrier's own term and does
not harmonise; the product spec picks one and says so.

---

## Primary sources

### S1 — KB라이프생명보험, "무배당 VIP 변액연금보험" 상품안내장

- Publisher: 주식회사 KB라이프생명보험 (KB Life Insurance Co., Ltd.)
- Document: 상품안내장, 16 pp.; 준법감시인확인필-SM-2212005-1 (2022.12.16~2023.12.15);
  생명보험협회 심의필 제2022-05589호 (2022.12.27~2023.12.26); 인쇄일자 2023. 01. 01
- Doc type: product brochure (상품안내장 — the consumer-facing summary that carries the
  guarantee-charge disclosure, the fund table and the surrender-value illustration)
- URL: https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1819232770/44
- Accessed: 2026-09-03
- Retrieved: yes (PDF, 16 pp.; WebFetch's own text layer failed, the file was re-extracted
  locally with PyMuPDF and read in full)
- What it is good for: this is the **single most quantitatively explicit GMAB document
  retrieved**. It prints both guarantee charges as formulae — 최저사망적립액 보증비용
  0.07%/12 per month of the separate-account value, and 최저연금적립액 보증비용 0.25%/12 of
  the separate-account value **plus** 0.3%/12 of 보험료총액 charged for at most seven years —
  together with the eight-fund 특별계정 운용보수 table, the mandatory bond-weight ladder,
  the automatic bond rebalancing three years before annuitisation, the surrender-value
  illustration at three investment returns and the annuity-amount illustration.

### S2 — KDB생명보험, "무배당 더! 행복드림 변액연금보험" 상품요약서

- Publisher: KDB생명보험주식회사 (KDB Life Insurance Co., Ltd.)
- Document: 상품요약서, 18 pp., 판매일자 2025.01.01
- Doc type: **상품요약서** — the statutory product summary, which is the document the
  supervisory regime requires to carry the 수수료 안내표 (fee schedule) [R2]
- URL: http://www.kdblife.com/nKumhoFiles/data_pdf/product/2025/I40666_20250101_(무)더!행복
  드림변액연금보험_상품요약서_V01.pdf
  (the Korean path segment must be percent-encoded for the request to succeed; the host
  serves the file over plain HTTP)
- Accessed: 2026-09-03
- Retrieved: yes (the first attempt returned HTTP 503; the second returned the PDF, 18 pp.,
  re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **complete fee table** — 계약체결비용, 계약관리비용, 위험보험료,
  특별계정 운용보수 by fund, 증권거래비용 및 기타비용, 기초펀드 보수·비용, both guarantee
  charges, the annuity-phase management charge and the seven-year 해약공제 scale — plus the
  full **GLWB** apparatus: a 7%/6% simple roll-up 최저연금기준금액, sex- and age-banded
  기본지급률, a 장기유지 가산율 and an 투자실적 가산율. It is the reference document for
  what a Korean VA fee schedule actually looks like.

### S3 — KDB생명보험, "무배당 더! 행복드림 변액연금보험" 약관

- Publisher: KDB생명보험주식회사
- Document: 보험약관, 105 pp., 판매일자 2025.06.30 (V03)
- Doc type: policy conditions
- URL: https://www.kdblife.com/nKumhoFiles/data_pdf/product/2025/I40685_20250630_(무)더!행복
  드림변액연금보험_약관_V03.pdf
- Accessed: 2026-09-03
- Retrieved: in part (2.8 MB PDF downloaded and extracted locally with PyMuPDF, 105 pp.;
  the file was read selectively rather than in full, and **no fact in this file rests on
  S3 alone** — everything cited to the product is cited to S2)
- What it is good for: corroboration that the 상품요약서 figures in [S2] are the summary of a
  contract of the same date. Held in reserve for the drafting pass.

### S4 — AIA생명보험, "무배당 AIA 여유+ 변액연금보험" 상품요약서

- Publisher: AIA생명보험주식회사 (AIA Life Insurance Korea)
- Document: 상품요약서, 18 pp.; header states 「이 상품요약서는 2026년 1월 1일부터
  적용됩니다」
- Doc type: 상품요약서 (statutory product summary)
- URL: https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/saving/summary/AIA_kr_Form107_20260101.pdf
- Accessed: 2026-09-03
- Retrieved: yes (PDF, 18 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **current-generation unguaranteed shape**. It is explicit that
  「연금개시시점의 최저계약자적립액 미보증」 — there is no GMAB and no GMAB charge — while
  the GMDB survives at 연 0.05% of the separate-account value. It carries the highest
  retrieved 계약체결비용 (6.12% of the basic premium for ten years, then zero) and the
  highest retrieved first-year 해약공제 (28.1%), so it brackets the top of both ranges.

### S5 — ABL생명보험, "(무)투자에강한변액연금보험(최저연금적립액 미보증형)2404" 상품안내장

- Publisher: ABL생명보험주식회사 (ABL Life Insurance Co., Ltd.)
- Document: 상품안내장, 20 pp.; 생명보험협회 심의필 제2025-06233호 (2025-09-18~2026-09-17);
  「2025년 10월 1일 제작」
- Doc type: product brochure
- URL: https://www.abllife.co.kr/cms/prdt/vains/__icsFiles/afieldfile/2025/09/29/(무)투자에강한
  변액연금(최저연금적립액_미보증형)2404_20251001.pdf
- Accessed: 2026-09-03
- Retrieved: yes (693 KB PDF, 20 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **most recent retrieved document** and the fullest description of
  the fund-management options — a 49-fund menu with per-fund 운용보수 broken into 운영보수 /
  투자일임보수 / 수탁보수 / 사무관리보수, a **펀드자동전환옵션** (target-return de-risking at
  110–200% in 10% steps), a **펀드자동재배분** (3- or 6-month rebalancing with a 60% floor on
  bond + MMF while a 계약유지보장 is running), the 정기중도인출서비스, and a 해약공제 scale
  that runs off in exact sevenths. It also records the raised **예금자보호 limit of ₩100
  million (1억원)**.

### S6 — ABL생명보험, "(무)하모니변액연금보험2404" 상품안내장

- Publisher: ABL생명보험주식회사
- Document: 상품안내장, 32 pp.; 생명보험협회 심의필 제2025-06232호 (2025-09-18~2026-09-17);
  CXM부 제작 2025.10.01
- Doc type: product brochure
- URL: https://www.abllife.co.kr/cms/prdt/vains/__icsFiles/afieldfile/2025/09/29/(무)하모니변액
  연금2404_20251001.pdf
- Accessed: 2026-09-03
- Retrieved: yes (908 KB PDF, 32 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **monthly-ratchet GMAB with no guarantee charge**. The
  경과확정보증액 ratchets monthly, the guarantee ratio runs 100%→130% with the term, and the
  guarantee is funded not by a fee but by a CPPI-style Auto Balancing between a growth-asset
  fund and a safe-asset fund plus an **irreversible automatic transfer to the general
  account** at a 1.75% floor when the growth weight hits zero. This is the single most
  important counter-example to "the guarantee is a basis-point charge".

### S7 — 교보생명보험, "미리 보는 내 연금 무배당 교보First변액연금보험Ⅱ" 약관

- Publisher: 교보생명보험주식회사 (Kyobo Life Insurance Co., Ltd.), distributed through
  하나은행 (the copy retrieved is the bank's contract-document mirror)
- Document: 보험약관 booklet, 231 pp., comprising the main contract (pp. 16–114),
  무배당 연금전환특약Ⅲ, 무배당 교보장기간병연금전환특약, 지정대리청구서비스특약,
  변액보험 펀드추가서비스특약 and an appendix of the statutes the policy cites
- Doc type: **policy conditions** (약관) — the operative contract text
- URL: https://image.kebhana.com/cont/download/insdocument/provide/L05184361_agree.pdf
- Accessed: 2026-09-03
- Retrieved: yes (1.9 MB PDF, 231 pp., re-extracted locally with PyMuPDF; 제2조 (용어의 정의),
  제36조 (계약자적립금의 계산), 제37조 (펀드의 운용 및 평가), 제38조 (펀드의 유형),
  제39조–제41조 (펀드 선택·변경, 자동이전·자동재배분, 평균분할투자), 제42조–제46조
  (특별계정 자산평가, 좌수 및 기준가격, 제비용, 폐지, 공지), 제50조 (해지환급금),
  제51조 (계약자적립금의 인출) and 제63조 (예금보험에 의한 지급보장) read verbatim)
- What it is good for: this is the **only policy-conditions-grade document read in full** in
  this session, and it supplies the definitional and mechanical text that a model needs —
  the composition of the 월공제액, the definition of 계약자적립금, the 좌수/기준가격 formula
  reproduced verbatim, the roll-up definition of the 최저연금기준금액, the annual ratchet of
  the 연금기준금액 in the 보증강화형, the 기본지급률 / 투자실적 가산율 / 장기유지 가산율
  tables, the 주식형적립금 자동이전 rule and the statement that the surrender value carries
  no minimum guarantee.

### S8 — 교보생명보험, "교보변액연금보험(무배당)[B] 고객님을 위한 변액연금보험 설명서"

- Publisher: 교보생명보험주식회사, bancassurance channel (준법감시인확인필 1-2312-10
  방카슈랑스본부직속 2023.12.18~2024.12.17; 준법감시인 사전심사필 제2024-10744-5호
  2024.02.23~2025.02.20); the copy retrieved is hosted by 신한은행
- Document: 변액연금보험 설명서, 4 pp.
- Doc type: point-of-sale explanatory document required by the 금융소비자 보호에 관한 법률
- URL: https://img.shinhan.com/sbank2016/seol/20211227000001350004LC000030.PDF
- Accessed: 2026-09-03
- Retrieved: yes (296 KB PDF, 4 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: it prints the **실적배당 종신연금 월 지급률 as a closed-form formula**
  — the only closed-form annuity rate found in any retrieved Korean VA document — and the
  ratcheting definition of the 연금기준금액. It also lists, in the carrier's own words, the
  five deductions that stand between the premium and the fund.

### S9 — KB라이프생명보험, "투자의 힘 무배당 KB 변액연금보험Ⅱ" 상품안내장

- Publisher: 주식회사 KB라이프생명보험
- Document: 상품안내장, 16 pp.; PDF creation metadata 2022-11-18 to 2022-12-22
- Doc type: product brochure
- URL: https://www.kblife.co.kr/api/archive/archives/download/product-onelibrary/1228994/44
- Accessed: 2026-09-03
- Retrieved: yes (906 KB PDF, 16 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **elective, mid-term GMAB** — a design in which the contract is
  sold unguaranteed, converts automatically to 보증형(중도선택형) at the end of the premium
  period, and lets the policyholder switch the guarantee on and off an unlimited number of
  times, at 연 0.85% of the separate-account value, with the guaranteed floor set at the
  account value two business days after election and ratcheted up monthly thereafter. It
  also carries the 성과보너스 (performance bonus at 120/140/160/180/200% return) and the
  forced 채권형II 50% + EMP AI형 50% allocation on electing the guarantee.

### S10 — 미래에셋생명보험, "미래를 보는 변액연금보험(무)202004" 상품안내장

- Publisher: 미래에셋생명보험주식회사 (Mirae Asset Life Insurance Co., Ltd.)
- Document: 상품안내장, 20 pp., 제작일자 2020.04
- Doc type: product brochure
- URL: https://pdf.miraeassetlife.com/directDownloadDocFile.do?Ax=... (a one-time signed
  download token; the token used on 2026-09-03 is recorded in the session log and is not
  expected to remain valid)
- Accessed: 2026-09-03
- Retrieved: yes (664 KB PDF, 20 pp., re-extracted locally with PyMuPDF and read in full)
- What it is good for: the **three-variant chassis** — 최저연금미보증형 / 최저연금보증형 1+α
  / 최저연금보증형 2+α — with a roll-up guarantee base (최저연금 기준적립금) credited at 연복리
  1.0% or 2.0%, a GLWB rather than a GMAB, guarantee charges of 연 0.30% and 0.35% of the
  separate-account value on top of a 연 0.05% GMDB charge, and equity caps that tighten with
  the guarantee (80% unguaranteed, 60% for 1+α, a single 글로벌MVP30 fund for 2+α). It is
  the clearest retrieved statement that **the guarantee level and the investment freedom are
  traded against each other**.

### S11 — 미래에셋생명보험, 변액보험 공시 (변액펀드MAP)

- Publisher: 미래에셋생명보험주식회사
- Doc type: carrier fund disclosure page (변액보험공시실)
- URL: https://life.miraeasset.com/micro/disclosure/variable/PC-HO-080501-000000.do
- Accessed: 2026-09-03
- Retrieved: in part (server-rendered HTML read; the page is a fund browser and only the
  first fund's panel was returned)
- What it was good for: confirming the shape of the mandated daily disclosure — 기준가격,
  설정일 and 1/3/6-month, 1/3/5-year, cumulative and annualised returns per fund. The single
  fund panel returned was 가치주식형, 설정일 2012.12.26, 기준가격 904.24원 (previous-day
  change −0.02원), 1개월 −18.39%, 3개월 −23.48%, 6개월 −19.02%, 1년 −23.81%, 3년 −23.46%,
  5년 −19.58%, 누적 −24.47%, 연평균 −9.58%. **A unit price of 904.24 against the statutory
  1,000.00 opening price means this fund is below its launch value after fourteen years** —
  a fact worth keeping in view when calibrating a return assumption. No as-of date was
  returned with the panel, so the figures are dated only by the access date.

### S12 — 생명보험협회 공시실, 변액보험 상품비교공시 / 시장현황

- Publisher: 생명보험협회 (Korea Life Insurance Association)
- Doc type: industry comparative disclosure portal
- URLs: https://pub.insure.or.kr/ and
  https://pub.insure.or.kr/compareDis/variableInsrn/mrktStts/list.do
- Accessed: 2026-09-03
- Retrieved: in part (both pages returned server-rendered HTML; the menu structure and the
  list of quarterly statistics files were read, but the statistics themselves live in linked
  PDFs — 「26_2분기 상품유형별 통계.pdf」, 「26_2분기 펀드유형별 통계.pdf」, 「26_1분기 …」 —
  and a direct request for one of those files was refused with 「적절하지 않은 경로를 통한
  요청입니다」)
- What it is good for: establishing **what is public**. The portal carries, for 변액보험,
  보장성 상품비교 / 저축성 상품비교 / 시장현황 / 상품별 펀드운영현황 / 신상품정보 /
  상품별 과거수익률 / 펀드현황. [R2] confirms that a savings-type variable product must
  publish its 수수료 안내표 either through the portal's 공제금액구분공시 screen or inside the
  상품요약서. The quantitative market figures behind this file therefore come from [R3] and
  [R9], not from the portal.

---

## Regulatory and actuarial references

### R1 — 보험연구원, 「변액연금 최저보증 및 사업비 부과 현황 조사」, 조사자료집 2018-1

- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI); author 김세환;
  원장 한기정; 2018년 2월
- Document: 117 pp., with an English abstract titled "GMxB and Charges in Korean Variable
  Annuities Market"; survey base **all 36 variable annuity products on sale at 2017-05-31,
  from the 18 of Korea's 25 life insurers then writing the line**
- Doc type: research institute survey monograph
- URL: https://www.kiri.or.kr/pdf/전문자료/KIRI_20180427_111032.pdf
  (also served as chapter offprints, e.g. `.../연구자료/기타보고서/josa_18_01_03.pdf`)
- Accessed: 2026-09-03
- Retrieved: yes (1.9 MB PDF, 117 pp.; WebFetch's own text layer was unusable, the file was
  re-extracted locally with PyMuPDF and the 요약, Ⅱ 성장추이, Ⅲ 최저보증 운영 현황,
  Ⅳ 최저보증리스크의 통제와 관리 and Ⅴ 사업비 부과 및 모집수수료 지급 현황 read in full)
- Content: **the single richest quantitative source on this product.** It supplies the
  guarantee taxonomy (GMDB / GMAB / GMWB / GLWB / GMIB) with the 별표 24 reserve factors;
  the four ways a guarantee level is set (premium refund, step-up, ratchet, roll-up) with a
  fifteen-year worked example; a product-by-product census of which of the 36 products
  guaranteed what; the statutory basis of the compulsory GMDB (보험업감독규정 제7-60조
  제7호, quoted verbatim); the 2014 감사원 audit finding that led to the GMAB becoming
  optional in April 2016; the risk-control devices insurers actually use; the **full 별표 24
  보증준비금 산출기준 tables** and the 보증위험액 최저한도 table; and the 사업비 census
  across all 36 products including the industry mean/max/min 해지공제율 by duration and the
  모집수수료율 by policy year. It is dated — the census is 2017 — and every figure taken from
  it is labelled with that date below.
- **Caveat that matters.** The report's <표 Ⅲ-1> prints a column headed 「연간보증비용」 with
  ranges GMDB 0.04–0.07%, GMAB 기납입보험료 0.56–0.98%, GMAB step-up/ratchet/roll-up
  0.84–1.05%, GMWB 0.6–0.9%, GLWB 0.6–0.9%, under the note 「보증비용은 보험업감독규정시행
  세칙 <별표 24> 보증준비금 산출기준을 따름」. Reconstructing those numbers from the 별표 24
  tables reproduced later in the same report shows they are **exactly** the reserve
  standard's floors, not observed carrier charges: 0.7% × 0.4%/0.5% = 0.56%, 0.7% × 0.7%/0.5%
  = 0.98%, 0.7% × 0.6%/0.5% = 0.84%, 0.7% × 0.75%/0.5% = 1.05%, and the GMDB / GMWB / GLWB
  entries are the `Max{적립률, x%}` floors verbatim. **They must not be quoted as market
  guarantee charges.** The observed charges are in [S1] [S2] [S4] [S9] [S10].

### R2 — 생명보험협회, 「변액보험의 이해와 판매」 2024 (변액보험판매자격시험 교재)

- Publisher: 생명보험협회 (Korea Life Insurance Association), 자격시험센터
- Document: 변액보험판매자격시험 교재, 2024 edition, 280 pp.; four chapters —
  제1장 금융시장의 이해, 제2장 생명보험의 이해, 제3장 변액보험의 이해,
  제4장 보험공시 및 예금자보호제도
- Doc type: **industry-standard textbook** for the licence examination that a producer must
  pass before selling any variable product
- URL: https://exam.insure.or.kr/upload/attach/pbt/notice/20240105_1704444400640.pdf
- Accessed: 2026-09-03
- Retrieved: yes (2.3 MB PDF, 280 pp.; re-extracted locally with PyMuPDF; the 변액보험의
  이해 chapter (보증옵션, 상품종류, 변액연금보험의 구조·보장구조·예시, 변액보험의 현금흐름,
  특별계정의 종류, 자산 평가방법, 좌수와 기준가격), the 해약환급금 and 책임준비금 sections
  of 제2장, the 생명보험과 세금 section, and the whole of 제4장 (변액보험 공시, 판매시
  준수사항, 적합성 진단, 예금자보호제도) read)
- Content: the authoritative plain-language statement of the mechanics — the cash-flow
  identity 특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중 계약유지비용 +
  기타비용) = 순보험료 + 납입 후 계약유지비용; the order and timing of every deduction; the
  좌수/기준가격 arithmetic; the fund-allocation ratios actually observed for variable
  annuities by premium term; the guarantee taxonomy with diagrams; the April 2016 change
  making the GMAB optional; the three illustration returns mandated by the 보험업감독규정;
  the 평균공시이율 for 2024 (2.75%); the disclosure regime; the licence, refresher-training
  and 적합성 진단 requirements; and the deposit-protection carve-out.

### R3 — 금융감독원, 「변액보험 판매 미스터리쇼핑 결과 및 관련 소비자 유의사항을 안내합니다」

- Publisher: 금융감독원 (Financial Supervisory Service), 소비자피해예방국
- Document: 보도자료, 5 pp.; 보도 2026.3.24.(화) 석간, 배포 2026.3.23.(월)
- Doc type: supervisory press release
- URL: https://kiri.or.kr/PDF/weeklytrend/20260406/trend20260406_5.pdf (the release was
  retrieved as reproduced in the 보험연구원 주간보험동향 of 2026-04-06; the FSS's own
  `fss.or.kr` board was not opened — see the fetch-failure section)
- Accessed: 2026-09-03
- Retrieved: yes (479 KB PDF, 5 pp., re-extracted locally with PyMuPDF and read in full)
- Content: **the current market and conduct picture.** 2025 변액보험 초회보험료 ₩2.89조
  (2.89조원), up **46.2%** on 2024's ₩1.97조; H1 2025 ₩1.38조 against H1 2024 ₩0.84조,
  up 64.7%; 2025 변액보험 민원 **1,308건, about 9% of all life-insurance complaints**. The
  mystery-shopping exercise ran September–November 2025 over **9 of 22 life insurers**
  (ABL, 삼성, 교보, 미래에셋금융서비스, KDB, 메트라이프, KB라이프파트너스, 신한라이프,
  하나), about 38 branch samples each, scored on 5 sections and 24 items; overall grade
  「양호」, with 5 우수 / 1 양호 / 1 보통 / 2 미흡 by company. Weakest items: the explanation
  of **변액보험의 자산운용 방식** and of the **위법계약해지권** under the 금융소비자보호법.
  The consumer-guidance half states the four points a Korean regulator considers material:
  the principal is not protected; the whole premium does not go into the fund because the
  위험보험료 and 사업비 come out first and are front-loaded; the customer must take the
  적합성 진단 **before** being recommended a product; and the customer can manage the funds.

### R4 — 보험업법 제108조 (특별계정의 설정·운용)

- Publisher: 대한민국 국회 / 금융위원회 (statute)
- Doc type: statute
- URL: https://casenote.kr/법령/보험업법/제108조 (CaseNote's mirror of the 국가법령정보센터
  text; the 국가법령정보센터 friendly URL returned only the page shell)
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML, article text and amendment history read)
- Content, quoted verbatim from the retrieved page: 제1항 「보험회사는 다음 각 호의 어느
  하나에 해당하는 계약에 대하여는 대통령령으로 정하는 바에 따라 그 준비금에 상당하는
  자산의 전부 또는 일부를 그 밖의 자산과 구별하여 이용하기 위한 계정(이하 "특별계정"이라
  한다)을 각각 설정하여 운용할 수 있다.」 The four qualifying classes are (1) a
  연금저축계좌 contract under 소득세법 제20조의3제1항제2호, (2) a 보험계약 및 퇴직보험계약
  under 근로자퇴직급여보장법 제29조제2항, (3) **변액보험계약**, and (4) any contract the
  금융위원회 considers necessary. 제2항 「보험회사는 특별계정에 속하는 자산은 다른
  특별계정에 속하는 자산 및 그 밖의 자산과 구분하여 회계처리하여야 한다.」 제3항 permits
  the profits of a separate account to be distributed to its policyholders; 제4항 delegates
  the asset-management method, valuation, profit distribution and comparative disclosure to
  Presidential Decree. Amendment history shown: 2020.12.8 (in force 2021.6.9), 2015.7.24
  (2016.1.25), 2010.7.23 (2011.1.24), with earlier amendments in 2008, 2007, 2005, 2003,
  1998, 1997, 1978 and 1962.

### R5 — 보험업법 제106조 (자산운용의 방법 및 비율)

- Publisher: 국가법령정보센터
- Doc type: statute
- URL: https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=1000734924&chrClsCd=010202&lsId=001532&print=print
- Accessed: 2026-09-03
- Retrieved: yes (the `print=print` form of the 국가법령정보센터 URL returns text where the
  friendly `/법령/` form does not)
- Content: version **시행 2025-01-31, 법률 제20436호 (2024-09-20 타법개정)**. The article
  sets asset-concentration limits **separately for the general account and for special
  accounts**, the special-account limits being the higher of the two: credit exposure to one
  person or corporation 3% of assets for the general account, ownership of bonds and shares
  of one corporation 7%, real estate 25%. The retrieved summary reports the special-account
  limits as separate and generally higher percentages but did not return their exact values —
  see the gaps section.

### R6 — 생명보험협회 자격시험센터, 변액보험(PBT) 시험규정

- Publisher: 생명보험협회
- Doc type: examination regulations for the 변액보험판매관리사 qualification
- URL: https://exam.insure.or.kr/vrb/pbt/schd/legal
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML read)
- Content: the statutory hooks are **보험업법 제83조** (who may solicit), **보험업법 시행령
  제56조** and **보험업감독규정 제5-4조**. 제2조 limits candidates to solicitors defined in
  보험업법 제83조, excluding those handling only non-life or 제3보험 products. 제11조 sets
  the pass mark at 「100점 만점에 70점 이상」. Format: 40 questions, 60 minutes of working
  time (70 minutes for the paper-based sitting including instructions), true/false and
  four-option multiple choice. The regulations cover qualification management and
  disqualification but do **not** state the continuing-education requirement; that comes
  from [R2] instead.

### R7 — 금융위원회, 「불합리한 보험 사업비와 모집수수료를 개편하여 소비자의 환급률을
높이고 보험료 인하를 유도하겠습니다」

- Publisher: 금융위원회 (Financial Services Commission), 보험과
- Document: 보도자료, 2019년 8월 1일
- Doc type: policy press release
- URL: https://fsc.go.kr/no010101/73816
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML read)
- Content: the reform package that reshaped Korean expense loadings. Savings-level expenses
  applied to the savings component of protection products at about **70%** of then-current
  levels, expected to give a 2–3% premium cut and a 5–15 percentage-point improvement in
  surrender ratios; long-term-care and dementia products cut to 70%; renewal-period contract
  costs cut to 70% of the initial-contract level; the **추가납입 limit cut from 2× to 1×**;
  and commission controls effective **January 2021** requiring that first-year commission
  plus surrender value not exceed premiums paid, with split-payment commission structures
  offered as an alternative to front-loading. Regulatory amendments were to run to April
  2020. Note that the 추가납입 cut to 1× is **not** reflected in any variable-annuity
  document retrieved here — every one of [S1] [S4] [S5] [S6] [S7] [S10] still publishes a
  200% additional-premium limit — so the 2019 measure evidently did not carry across to
  variable annuities, or was reversed; this is flagged in the gaps section.

### R8 — 금융위원회, 「보험자본건전성 선진화 추진단」 제10차 회의 보도자료

- Publisher: 금융위원회
- Document: 보도자료, 2022년 8월 25일; 담당 보험과 김경찬
- Doc type: policy press release
- URL: https://fsc.go.kr/po010101/78367
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML read)
- Content: the IFRS 17-era treatment of the two reserves that matter to this product.
  **해약환급금준비금** (surrender value reserve): where the fair-valued insurance liability
  falls below the contractual surrender obligation — which happens when interest rates rise —
  the shortfall must be reserved. **보증준비금** (guarantee reserve): built from the existing
  guarantee reserve carried as a liability **plus the guarantee fees still to be collected**.
  Both move from liability accounts into statutory reserves inside retained earnings, so they
  restrict distributable profit while protecting policyholders. Implementation from **2023**,
  after a third-quarter 2022 pre-announcement. The release does not name the amended article
  numbers — see the gaps section.

### R9 — 보험연구원, 「2025년 보험산업 전망」 (세미나: 보험산업 전망과 과제)

- Publisher: 보험연구원; 발표 황인창 (금융시장분석실장); 2024.10.10
- Document: seminar deck, 78 pp. (60 numbered slides plus appendix)
- Doc type: research institute market forecast
- URL: https://www.kiri.or.kr/pdf/전문자료/smn_20241010.pdf
- Accessed: 2026-09-03
- Retrieved: yes (2.1 MB PDF, 78 pp., re-extracted locally with PyMuPDF; the 연금 및 변액보험
  slide, the 종목별 초회보험료 slide and the 부록 변액보험 slide read)
- Content: **변액보험 수입보험료 (premium income), in 조원 with year-on-year growth**:
  2021 17.9 (+4.1%), 2022 12.7 (−29.0%), 2023 12.2 (−4.0%), 2024(E) 11.6 (−4.9%),
  2025(F) 10.1 (−12.7%). 2025 첫회보험료 forecast −45.9% on base effects. The stated drivers
  of the decline are market uncertainty and, explicitly, that **「최저보증이율의 하락」**
  reduces demand for guaranteed variable annuities; the stated drivers of growth are rate
  cuts pushing money into investment products and retirement-income demand. First-half 2024
  saw variable new business rise while premium income fell because of surrenders.

### R10 — 보험저널, 「변액보험 펀드 연환산 수익률, 국내형 71.32%·해외형 44.61% 최고」

- Publisher: 보험저널 (insjournal.co.kr) — **a trade news article, not a primary document**
- Document: article dated 2026-05-13, reporting 생명보험협회 disclosure data as at 2026-04-30
- Doc type: **secondary / news**
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=31404
- Accessed: 2026-09-03
- Retrieved: yes (article read)
- Content: annualised fund returns as at 2026-04-30 taken from the 생명보험협회 disclosure.
  Domestic equity: BNP파리바카디프생명 친환경에너지액티브 ETF재간접형 71.32%; 한화생명
  일반주식형V 49.01%; 메트라이프생명 혼합성장형 48.04%. Overseas equity: IBK연금보험
  미국 테마주식 ETF 재간접형 44.61%; BNP파리바카디프생명 나스닥 대형주 ETF재간접형 44.16%;
  메트라이프생명 미국주식형 43.08%. **This is the only source in this file for realised fund
  returns and it is a news article**; the underlying association disclosure was not opened.
  Any return assumption in the model must be `[std]`, not sourced to this.

### R11 — 보험업감독규정 제7-60조 (생명보험의 보험상품설계 등) 제7호

- Publisher: 금융위원회 (고시)
- Doc type: supervisory regulation
- URL: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196
- Accessed: 2026-09-03
- Retrieved: **no** (the 국가법령정보센터 page returned the navigation shell only; it did
  confirm the version on display as 시행 2023-03-02, 금융위원회고시 제2023-10호. The FSC's
  own attachment endpoint returned a different document — a 규제영향분석서 — and the
  easylaw.go.kr download and the ulex.co.kr mirror both failed to reach 제7편.)
- Content, **as quoted verbatim in [R1] at two places (footnotes 2 and 4)**: 「변액보험 및
  금리연동형보험(연금보험을 제외한다)의 경우 최저사망보험금 등을 설정하여야 한다」. This
  is the provision that makes the GMDB compulsory on every Korean variable contract, and it
  is why all 36 products in the 2017 census carried one [R1]. The quotation is
  double-sourced within [R1] but the regulation itself was **not** retrieved; treat the
  article number as sound and any wider reading of 제7-60조 as `[unverified]`.

### R12 — 보험업감독업무시행세칙 <별표 24> 보증준비금 산출기준

- Publisher: 금융감독원 (세칙)
- Doc type: supervisory implementation rules, annex
- URLs tried: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687 and
  https://lbox.kr/v2/statute-admin/보험업감독업무시행세칙
- Accessed: 2026-09-03
- Retrieved: **no** (law.go.kr returned the shell; lbox.kr returned HTTP 403)
- Content, **as reproduced in [R1] (tables Ⅳ-7(a), Ⅳ-7(b), Ⅳ-8)**: the guarantee reserve is
  the greater of a stochastic **CTE(70)** figure — 「사망률, 해지율, 자산이익률(1,000개)을
  이용하여 만기까지 장래 예상되는 순손실액을 현가로 환산한 상위 30% 평균 금액」 — and a
  standard factor tabulated by 보험종류 × 최저보증종류 × 보증수준 × 주식비중한도. The
  factor tables are reproduced in the fact-extraction section below. A search result also
  indicates that the annex is invoked by **보험업감독규정 제6-11조 제10호** and computed
  under **시행세칙 제4-15조**; neither article was retrieved, so those article numbers are
  `[unverified]`.

### R13 — 보험업법 시행령, 특별계정 관련 조문 (제52조·제53조)

- Publisher: 국가법령정보센터
- Doc type: Presidential Decree
- URL: https://www.law.go.kr/LSW//lsSideInfoP.do?lsiSeq=266041&joNo=0053&joBrNo=00&docCls=jo&urlMode=lsScJoRltInfoR
- Accessed: 2026-09-03
- Retrieved: **in part** — the page identified the instrument as 보험업법 시행령,
  **시행 2024-10-25, 대통령령 제34960호 (2024-10-22 일부개정)**, 소관 금융위원회 보험과, but
  returned the navigation frame rather than the article text.
- Content, from search-result summaries only and therefore `[unverified]`: 제52조 requires a
  separate account to be set per class of contract, with more than one permitted per class
  where the 금융위원회 accepts it is needed for efficient management; 제53조 governs
  special-account asset-management ratios, bars the insurer from exercising voting rights on
  shares held in a separate account, and bars borrowing against a 제108조제1항제2호 account;
  and the prohibitions include guaranteeing a return in advance on a 변액보험계약 and moving
  assets between the general account and a separate account. **None of this was read in the
  original**, and no fact in the extraction section rests on it alone.

### R14 — 금융소비자 보호에 관한 법률 제17조 (적합성원칙) and 제18조 (적정성원칙)

- Publisher: 대한민국 국회
- Doc type: statute
- URL: not fetched directly
- Accessed: n/a
- Retrieved: **no** — the statute is cited here only as reported in [R2] and [R3], both of
  which were retrieved. [R2] states that a producer recommending a variable contract to an
  일반금융소비자 must observe 제17조, that selling without recommending engages 제18조, and
  that the information gathered under 제17조 and 시행령 제11조 must include the customer's
  연령, 재산상황, 보험계약 체결의 목적, experience of acquiring and disposing of financial
  products, and understanding of financial products. [R3] adds that the 위법계약해지권 arises
  where the seller breaches 적합성원칙, 적정성원칙, 설명의무, 불공정영업행위 금지 or
  부당권유행위 금지. The article numbers are second-hand but come from two independently
  retrieved documents.

---

## Fact extraction

### 1. Product architecture — the two periods and the account that spans them

- A Korean variable annuity is written as two periods of one contract: the
  **연금개시 전 보험기간**, running 「계약일부터 연금개시나이 계약해당일의 전일까지」, and the
  **연금개시 후 보험기간**, running 「연금개시나이 계약해당일부터 종신까지」 for a life
  annuity or to the end of the fixed term for a 확정연금형. [S5] [S4] [S7]
- Through the accumulation period the policyholder's money is the **계약자적립금 /
  계약자적립액**, defined in the policy conditions as 「납입보험료에서 월공제액 및 인출금액
  등을 공제한 금액을 특별계정의 운용실적을 반영하여 계산한 금액」 which 「특별계정의 평가
  등에 따라 매일 변동할 수 있습니다」. [S7 제2조]
- At annuitisation the usual design **moves the money to the general account** and pays a
  declared-rate annuity: 「연금개시시점부터 계약자적립액 모두에 대하여 특별계정에서
  일반계정으로 자동전환하여 공시이율로 운용합니다」. [S6]
- The alternative design **keeps the money in the separate account through the payout phase**
  and guarantees a lifetime withdrawal — 실적배당 종신연금 [S2] [S7] [S8], 투자실적 종신연금
  [S10]. [R2] describes this as the GLWB and notes the consequence a modeller must not miss:
  「일반적인 변액연금과 다르게 연금개시 이후에도 특별계정 적립금에서 보증비용이 공제됨」.
- Death cover before annuitisation is small and sometimes absent. Observed forms:
  - **재해장해급여금 only, no death cover** — 「고도재해장해보험금 1,000만원(1구좌 기준),
    최초 1회한」, with the account value paid on death subject to the GMDB floor. [S1] [S2]
    [S6 1종(무사망형)] [S7 제3조]
  - **기본사망보험금 proportional to premium** — 적립형 기본보험료의 10배, 거치형
    기본보험료의 10%, plus the account value. [S5] [S6 2종(기본형)]
  - [R2] states the general design rule: 「사망보험금 = 기본사망보험금 + 사망 시점까지
    적립된 계약자적립금」 and that 「최근에는 환급률 제고를 위해 기본사망보험금 대신
    장해보험금을 지급하는 형태로 설계하는 상품이 더 많다」.
- Cover ceases at annuitisation on the general-account designs — [R2] 「일반적으로 연금개시
  후 보장은 소멸됨」 — but on the GLWB designs a residual 최저사망적립금 survives into the
  payout phase, running down by the annuity payments already made. [S2] [S7] [S10]
- 자살면책 is **2 years** on the two contracts that state it. [S5] [S6]

### 2. 특별계정 — the statutory basis and what separation actually means

- The separate account exists because **보험업법 제108조제1항제3호** lists 변액보험계약 as
  one of four contract classes for which an insurer may set up a 계정 「그 준비금에 상당하는
  자산의 전부 또는 일부를 그 밖의 자산과 구별하여 이용하기 위한」. [R4]
- **제108조제2항** requires the assets of one separate account to be accounted for separately
  from those of every other separate account **and** from all other assets. [R4]
- The policy conditions restate the statute and add the consequences: 「투자목적 및 대상에
  따라 구분된 변액보험의 펀드는 특별계정별로 일반보험의 자산과 분리하여 독립적으로
  운용되며, 자산운용실적이 계약자적립금에 즉시 반영될 수 있도록 매일 평가합니다」; 「제1항의
  특별계정에서 관리되는 자산의 운용실적에 따른 이익 및 손실은 다른 계정의 자산운용에 따른
  이익 및 손실에 관계 없이 이 계약으로 귀속됩니다」; and 「계약자는 특별계정의
  자산운용방법에 대해서는 일체의 관여를 할 수 없습니다」. [S7 제37조]
- The insurer may pool the assets of similar separate accounts across products, on notice by
  newspaper advertisement or individual notification, keeping each fund's accounts at head
  office for six months after the merger. [S7 제37조제4항]
- A separate account may be **wound up** only on stated grounds: a sharp fall in its assets
  or a change in asset values making efficient management impracticable; **원본액 below ₩5
  billion (50억원) at the first anniversary of establishment, or below ₩5 billion for a
  continuous month after the first year**; the disappearance of its investment universe; or
  a comparable cause. On winding up the insurer must write to policyholders with the reason,
  the account value to the closing date and a fund-switch notice, may move a silent
  policyholder to a similar fund, and must waive both the switching fee and the annual switch
  count. [S7 제45조]
- Valuation and management follow the 자본시장과 금융투자업에 관한 법률, applied fund by
  fund. [S7 제42조] [R2] adds that market valuation is the principle, with amortised cost
  plus accrued interest used for assets such as loans that have no observable price.
- Costs charged directly to separate-account assets are set by statute rather than by the
  contract: 「자본시장과 금융투자업에 관한 법률 제188조에 따른 보수, 그 밖의 수수료와 동법
  시행령 제265조에 따른 회계감사비용, 채권평가비용 및 유가증권매매수수료 등을
  특별계정자산에서 인출하여 부담합니다. 다만, 자산운용보고서를 작성·제공하는데 드는 비용은
  회사가 부담합니다」. [S7 제44조]
- Asset-concentration limits apply to special accounts on their own scale, separate from the
  general account's, under 보험업법 제106조. [R5]
- [R2] describes the special account as a 자본시장법 투자신탁 for reporting purposes, which is
  why an 자산운용보고서 must be produced quarterly and confirmed by the trustee.

### 3. 좌수 and 기준가격 — the daily unit mechanics, reproduced verbatim

The policy conditions and the industry textbook agree, and both are quoted because the model
implements this arithmetic directly.

- 「좌수: 특별계정을 설정할 때 **1원을 1좌**로 하며, 그 이후에는 매일 좌당 기준가격에 따라
  좌단위로 특별계정에 이체 또는 인출합니다.」 [S7 제43조제1호] [R2]
- 「좌당 기준가격 = 당일 특별계정의 순자산가치 ÷ 특별계정 총 좌수」, computed 「1,000좌
  단위로 원 미만 셋째 자리에서 반올림하여 원 미만 둘째 자리까지」, with the opening price on
  the first day of sale being **1,000원 per 1,000좌**. 「다만, 당일 특별계정의 순자산가치라
  함은 당일 특별계정의 총자산에서 **특별계정 운용보수를 차감한** 금액으로 합니다.」
  [S7 제43조제2호]
- The textbook gives the same three identities in the form a model uses [R2]:

      계약자 보유좌수 = (특별계정 투입보험료 ÷ 투입일 기준가격) × 1,000
      계약자적립금   = 해당일 기준가격 × (계약자 보유좌수 ÷ 1,000)
      해당일 기준가격 = (전일말 특별계정 순자산가치 ÷ 특별계정 총좌수) × 1,000

  and reconciles the "previous day" and "same day" wordings in a footnote: 「「보험업감독업무
  시행세칙」에서는 좌당 기준가격을 산정함에 있어 당일 특별계정 순자산가치를 특별계정
  총좌수로 나누어 산출하도록 규정하고 있다. 여기서 당일의 의미는 당일초의 순자산가치를
  반영해야 한다는 것으로 실제로는 전일말과 동일한 기준이다.」 [R2]
- Units increase when money enters the separate account (premium, repayment of a policy loan)
  and decrease when money leaves it (the monthly deduction, a policy loan, a withdrawal).
  The unit price moves only with investment performance. [R2]
- A price below 1,000 means the fund is below its launch value. [R2] The single fund panel
  retrieved from a live disclosure showed exactly that: 904.24원 on a fund set up
  2012-12-26. [S11]
- Transactions are priced with a lag. Switching between funds uses 「변경요구일 + 제2영업일」
  [S5] [S7 제39조]; withdrawals use 「신청일 + 제2영업일」 [S2] [S5]; a surrender following a
  reduction or a voluntary termination uses 「해지신청일 + 제2영업일」 [S7 제50조제2항] [S9].

### 4. Premium allocation — how much of the premium reaches the fund

- The textbook's identity, which every retrieved product document is consistent with [R2]:

      특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중 계약유지비용 + 기타비용)
                          = 순보험료 + 납입 후 계약유지비용

  The **납입 후 계약유지비용 is collected during the premium period and carried inside the
  account value**, then drawn back out month by month after the premium period ends. This is
  why the money that goes into the fund is more than the pure net premium, and why the
  monthly deduction jumps at 납입완료.
- The monthly deduction (월공제액) is defined in the contract as 「해당월의 위험보험료,
  계약관리비용(납입기간 종료 후 유지관련비용), 최저사망적립금 보증비용 및 실적배당 종신연금
  보증비용의 합계액」 for the accumulation period, and 「해당월의 계약관리비용(연금부분),
  최저사망적립금 보증비용 및 실적배당 종신연금 보증비용의 합계액」 for the payout period; it
  is taken from the account value on the **월계약해당일** (the monthly policy anniversary).
  「다만, 계약체결비용, 계약관리비용(납입기간 중 유지관련비용), 계약관리비용(기타비용)은
  보험료를 납입할 때 공제하며」. [S7 제2조] So there are two distinct deduction points: a
  front-end deduction at premium payment and a monthly deduction from the fund.
- One further asymmetry, contractual and worth modelling: 「연금개시후 보험기간 중
  최저사망적립금이 "0"이 되면, 이후 최저사망적립금 보증비용은 차감하지 않습니다」. [S7 제2조]
  [S10] states the same rule for its GLWB variant.
- 계약자적립금 is calculated as 「계약자적립금에서 월계약해당일에 월공제액을 차감한 금액과
  특별계정투입보험료에 해당하는 이체금액에 대하여 특별계정의 운용실적을 반영하여」, with the
  separate-account management fee taken **daily**: 「회사는 특별계정 계약자적립금에서 매일
  특별계정 운용보수를 차감합니다」. [S7 제36조]
- The textbook publishes the **actually observed allocation ratios for variable annuities**,
  as a percentage of premium reaching the fund before the monthly natural-premium mortality
  deduction, by premium term [R2]:

      성별  나이   일시납  3년납  7년납  10년납  15년납  20년납
      남자  20–45  94.4    96.6   90.9   90.0    90.0    90.0
      여자  20–45  94.4    96.6   90.9   90.0    90.0    90.0

  with a footnote that ages 40–45 fall to 90–89.9 and 96.6–96.5 / 90.9–90.8 in the shorter
  terms. The textbook explains the shape: a variable annuity carries so little mortality
  cover that the natural premium is immaterial, so the allocation is flat and then **rises**
  after ten years when the 계약체결비용 stops.
- The retrieved illustrations corroborate the ~90–91% figure directly. Cumulative
  separate-account contributions against cumulative premiums at the one-year point, for the
  common illustration point (male 40, ₩300,000 per month, 10-year premium term):

      Carrier   납입보험료 누계   특별계정 투입 누계   ratio
      [S2] KDB      3,600,000        3,287,736         91.3%
      [S6] ABL      3,600,000        3,286,496         91.3%
      [S1] KB       3,600,000 (360만) 3,290,000 (329만)  91.4%

  and at ten years [S2] 32,877,360 / 36,000,000 = 91.3%, [S1] 3,295만 / 3,600만 = 91.5%.
- Additional premium (추가납입보험료) attracts little or no loading, which is the single
  largest lever a policyholder has: 「추가납입시, 추가납입보험료에 대한 수수료가 없습니다」
  [S1]; 「추가납입 시 수수료는 없습니다」 [S6]; 「추가납입 시 사업비가 차감되지 않습니다」
  [S9]; 추가납입보험료 계약유지·관리비용 「없음」 [S4]. Only [S2] charges it, at **1.5% of
  the additional premium**, reduced to Min(0.5%, ₩10,000) within the cumulative amount
  previously withdrawn.

### 5. The fee stack, as three retrieved 상품요약서 actually print it

A Korean savings-type variable contract must publish a 수수료 안내표 covering 보험관계비용
(계약체결비용, 계약관리비용, 위험보험료), 특별계정운용비용 (특별계정 운용보수, 기초펀드
보수·비용, 증권거래비용 등), 보증비용, 연금수령 기간 중 비용 and 해약공제비용, either in the
association's 공제금액구분공시 screen or inside the 상품요약서, and must repeat it in the
상품설명서 given at the point of sale [R2]. Three such tables were retrieved.

**[S2] KDB생명 무배당 더! 행복드림 변액연금보험 — 상품요약서 판매일자 2025.01.01.**
Illustration basis: 남자 40세, 60세 연금개시, 기본보험료 30만원, 10년납, 월납.

      구분              시기        비용
      보험관계비용 계   매월        1~10년  26,022원 (8.7%)
                                    11~20년  4,032원 (1.3%)
      계약체결비용      매월        10년 이내: 기본보험료의 5.17% (15,510원)
      계약관리비용      매월        납입기간 이내: 기본보험료의 3.50% (10,500원)
                                    납입기간 이후: 기본보험료의 1.33% (4,000원)
      위험보험료        매월        기본보험료의 0.004%~0.011% (12원~32원)
      특별계정 운용보수 매일        채권형 연 0.4%; 가치주혼합성장형 연 0.6%;
                                    액티브배당성장70혼합형 연 0.6%;
                                    인덱스플러스알파70혼합형 연 0.5%;
                                    AI솔루션자산배분안정형 연 0.6%;
                                    AI솔루션자산배분적극형 연 0.7%;
                                    선진국주식형 연 0.6%; K-REITs혼합형 연 0.6%;
                                    미국고배당포커스주식형 연 0.6%
      증권거래비용 및   사유발생시  채권형 연 0.01%; 가치주혼합성장형 연 0.49%;
      기타비용                      액티브배당성장70혼합형 연 0.10%;
                                    인덱스플러스알파70혼합형 연 0.03%;
                                    AI솔루션자산배분안정형 연 0.79%;
                                    AI솔루션자산배분적극형 연 0.14%;
                                    선진국주식형 연 0.19%; K-REITs혼합형 연 0.09%
      기초펀드 보수·비용 매일       채권형 연 0.01% … 선진국주식형 연 0.21%
      최저사망적립액    매월        연금개시전 20년 중: 최저연금기준금액의 연 0.40%
      보증                          (월 0.03333333%)
                                    연금개시전 20년 후: 연 0.25% (월 0.02083333%)
                                    연금개시후: 연금기준금액의 연 0.25%
      실적배당 종신연금 매월        연금개시전 20년 중: 최저연금기준금액의 연 3.30%
      보증                          (월 0.275%)
                                    연금개시전 20년 후: 연 1.70% (월 0.14166667%)
                                    연금개시후: 연금기준금액의 연 1.70%
      연금수령기간중의  매월        구좌당 매월 min(영업보험료의 3.5%, 4,000원)
      관리비용          (개시후)
      해약공제          해지시      아래 §14

  The 증권거래비용 및 기타비용 figures are estimates from actual FY2023 spend
  (2023.1.1–2023.12.31); the 기초펀드 보수·비용 are estimated from the FY2023 investment
  mix; the 특별계정 운용보수 is 「운영보수, 투자일임보수, 수탁보수, 사무관리보수의 합계」
  applied as a maximum with the actual cost charged; and all three are 「해당 특별계정(펀드)
  계약자적립액에서 차감되며 특별계정(펀드) 기준가격에 반영됩니다」. [S2]

**[S4] AIA생명 무배당 AIA 여유+ 변액연금보험 — 상품요약서, effective 2026-01-01.**

      계약체결비용      매월   10년 이내: 기본보험료의 6.12% (18,360원)
                               10년 초과: 기본보험료의 0.00% (0원)
      계약관리비용      매월   납입기간 이내: 기본보험료의 2.34% (7,020원)
                               납입기간 이후: 기본보험료의 2.00% (6,000원)
      위험보험료        매월   기본보험료의 0.0040%~0.0107% (12~32원)
      특별계정 운용     매일   엘리트 자산배분적극형1 연 0.780% (일 0.002137%)
      수탁보수                 엘리트 자산배분중립형1 연 0.690% (일 0.001890%)
                               엘리트 자산배분안정형1 연 0.600% (일 0.001644%)
                               MMF형 연 0.200% (일 0.000548%)
                               글로벌 에코트렌드 신성장 연 0.780%
      증권거래비용 및   사유   위 4개 펀드 연 0.00%; 글로벌 에코트렌드 신성장 연 0.10%
      기타비용          발생시 (직전 회계연도 2024.01.01~2024.12.31 기준 추정)
      기초펀드 보수비용 매일   적극형1 연 0.45%; 중립형1 연 0.39%; 안정형1 연 0.33%;
                               MMF형 연 0.11%; 글로벌 에코트렌드 신성장 연 0.42%
      최저사망지급금    매월   특별계정 적립액의 0.00417% (연 0.05%)
      보증
      연금수령기간중의  연금   연금 연액의 0.5%
      관리비용          수령시
      추가납입보험료           없음
      계약유지·관리비용
      중도인출수수료    인출시 Min(인출금액의 0.2%, 2,000원), 연 4회 면제

  There is **no GMAB line** because the product does not offer one. [S4]

**[S1] KB라이프생명 무배당 VIP 변액연금보험 — 상품안내장 (2023-01 print).** The brochure
does not print 계약체결비용 or 계약관리비용, but it prints both guarantee charges as
formulae, which no other retrieved document does for a GMAB:

- 최저사망적립액 보증비용: 「특별계정계약자적립액의 **0.07%/12**를 매월 특별계정에서
  차감합니다」 — i.e. 연 0.07% of the separate-account value.
- 최저연금적립액 보증비용: 「특별계정계약자적립액의 **0.25%/12**와 **보험료총액의 0.3%/12**를
  매월 특별계정에서 차감합니다」, where 「보험료총액은 이미 납입한 보험료(특약보험료 제외)
  및 추후 납입할 기본보험료 합계(특약보험료 제외)」 and 「보험료총액대비 보증비용은
  납입기간(최대 7년) 동안 부과합니다」.
- 특별계정 운용보수, charged as 「특별계정계약자적립액의 "특별계정 운용보수"/365를 매일
  특별계정에서 차감」, split 운영보수 / 투자일임보수 / 사무관리보수 / 수탁보수:

      펀드                     합계     운영    투자일임  사무관리  수탁
      채권형                   0.465%   0.332%  0.100%    0.023%    0.010%
      단기안정채권형           0.345%   0.262%  0.050%    0.023%    0.010%
      플러스알파인덱스주식형   0.615%   0.432%  0.150%    0.023%    0.010%
      글로벌주식형             0.687%   0.454%  0.200%    0.023%    0.010%
      스마트주식형             0.755%   0.502%  0.220%    0.023%    0.010%
      배당주식형               0.765%   0.502%  0.230%    0.023%    0.010%
      롱텀밸류주식형           0.765%   0.452%  0.280%    0.023%    0.010%
      액티브주식형             0.815%   0.502%  0.280%    0.023%    0.010%

  with the standard caveat that a fund-of-funds structure adds the underlying fund's own
  charges. [S1]

**[S9] KB라이프생명 투자의 힘 무배당 KB 변액연금보험Ⅱ.** Guarantee charges only:
최저사망보험금 보증비용 「특별계정적립액의 연 0.05%」; 연금개시시점의 최저계약자적립액
보증비용 「특별계정적립액의 연 0.85%」, charged only while the elective guarantee is on.
특별계정 운용보수 (투자일임 / 운영 / 수탁 / 사무관리, summing to the totals shown):

      채권형Ⅱ                      0.250%   (0.010 / 0.200 / 0.025 / 0.015)
      글로벌채권형                  0.220%   (0.020 / 0.160 / 0.030 / 0.010)
      글로벌하이일드채권형          0.220%   (0.030 / 0.150 / 0.030 / 0.010)
      이머징국공채인컴형            0.220%   (0.010 / 0.170 / 0.030 / 0.010)
      글로벌인덱스주식형            0.370%   (0.030 / 0.300 / 0.030 / 0.010)
      코리아ESG지속성장 주식형      0.520%   (0.030 / 0.455 / 0.020 / 0.015)
      글로벌Commodity주식형         0.550%   (0.050 / 0.430 / 0.055 / 0.015)
      글로벌이머징마켓주식형        0.550%   (0.040 / 0.440 / 0.055 / 0.015)
      코리아리츠&인프라 자산배분형  0.640%   (0.200 / 0.405 / 0.020 / 0.015)

  「실제 지급하는 투자일임보수, 수탁보수 및 사무관리보수가 상기표에서 정한 비용을 초과하는
  경우에는 운영보수에서 충당합니다.」 [S9]

**[S10] 미래에셋생명 미래를 보는 변액연금보험.** 최저사망적립금 보증비용 「매년 특별계정
적립금의 0.05%」 on all three variants; 최저보증종신연금 보증비용 「매년 특별계정적립금의
0.30%」 for 최저연금보증형 1+α and 「0.35%」 for 2+α. [S10]

**[S5] ABL생명 (무)투자에강한변액연금보험** publishes the 49-fund 특별계정 운용보수 table
(운영 / 투자일임 / 수탁 / 사무관리, all as a percentage of the separate-account account value
per year). Representative totals: 채권형 0.3905% (0.3510 / 0.0100 / 0.0100 / 0.0195);
단기국공채재간접형 0.3860%; MMF재간접형 0.3155% (0.2805 / 0.0100 / 0.0100 / 0.0150);
성장형 0.7850% (0.5955 / 0.1600 / 0.0100 / 0.0195); 글로벌리츠형 0.8750% (0.2805 / 0.5500 /
0.0250 / 0.0195); 빅데이터국내주식형 0.7250%; 팀챌린지자산배분C형 0.8855%. 「투자일임보수,
수탁보수 및 사무관리보수의 경우, 위에서 정한 금액을 한도로 실제로 사용한 비용을
적용합니다.」 [S5]

**Two structural observations.** First, the 계약체결비용 is charged as a **percentage of the
basic premium, monthly, for a fixed ten years** — not as a percentage of the fund and not
amortised over the premium term. Second, the two carriers that publish it disagree on what
happens at year ten: [S4] drops it to exactly 0.00%, [S2] keeps a smaller 보험관계비용 total
of 1.3% running to year twenty. [R1]'s 2017 census found the same split: 「월납 적립식
변액연금의 경우 계약체결비용은 계약체결 후 10년 이내까지 부과되는 것이 일반적이며,
해지공제가 적용되지 않는 8년 이후에는 계약체결비용이 줄어드는 경우가 대부분이다」, with
5.58–6.91% charged through year 7, 2.33–3.6% from year 8, and 5.02–6.1% where a flat ten-year
charge is used.

### 6. 최저사망보험금보증 (GMDB) — compulsory, cheap, and defined off the premium

- The GMDB is **not optional**. 보험업감독규정 제7-60조 제7호: 「변액보험 및
  금리연동형보험(연금보험을 제외한다)의 경우 최저사망보험금 등을 설정하여야 한다」, quoted
  in [R1]; all 36 products in the 2017 census carried one [R1].
- The standard definition, from the textbook [R2]:

      사망보험금(최저보증 포함) = Max(기납입보험료, 계약자적립금 + 기본사망보험금)

- Contract wordings retrieved:
  - 「피보험자가 연금개시 전 보험기간 중 사망한 경우에는 … 계약자적립액과 이미 납입한
    보험료(단, 특약보험료 제외) 중 큰 금액을 계약자에게 지급합니다.」 [S1]
  - 「연금개시전 보험기간 중 피보험자가 사망한 경우 사망한 날의 계약자적립액을 지급하지만,
    사망한 날의 계약자적립액이 … "이미 납입한 보험료"보다 적은 경우 계약자적립액을 지급하지
    않고 "이미 납입한 보험료"를 지급하는 것」, where 「이미 납입한 보험료」 is the sum of the
    basic and additional premiums excluding rider premium. [S4]
  - 「보증기간 동안 피보험자가 사망한 경우 특별계정의 운용실적과 관계없이 사망시점의 "이미
    납입한 보험료(특약보험료 제외)의 100%"를 지급하여 드립니다.」 [S10]
  - 최저사망적립금 기본형 = 「사망시점의 "이미 납입한 보험료"」; 보증강화형 = 「사망시점의
    "최저연금기준금액"」. [S7 제2조]
- **The guarantee base is adjusted for withdrawals and premium reductions.** 「계약자적립액의
  일부를 인출하거나 기본보험료를 감액하는 경우의 최저사망지급금 계산시 적용하는 "이미
  납입한 보험료"는 … 계산된 보험료와 해당 감액 또는 인출 이후 납입된 보험료의 합계」 [S4];
  the same rule in [S7 제2조]. Without this a policyholder could withdraw the fund and keep
  the guarantee.
- **Observed GMDB charges**, all as an annual rate deducted monthly or daily from the
  separate account:

      0.05% of 특별계정 적립액                       [S4] [S9] [S10]
      0.07% of 특별계정계약자적립액 (0.07%/12 월)     [S1]
      0.40% of 최저연금기준금액 (첫 20년), then 0.25% [S2]

  [S2] is dearer because its guarantee base is not the premiums paid but a **roll-up**
  amount that grows at 7%/6% simple (see §8), so the option is far deeper in the money.
- **Charging stops when the guarantee is worthless**: 「연금개시후 보험기간 중
  최저사망적립금이 "0"이 되면, 이후 최저사망적립금 보증비용은 차감하지 않습니다」 [S7];
  「이미 납입한 보험료에서 투자실적종신연금 지급액 합계를 차감한 금액이 0보다 작으면
  보증비용을 차감하지 않으며, 보증금액은 "0"으로 함」 [S10].
- Mechanically, [R2] states that the insurer 「매일(또는 매월) 특별계정 적립금에서 보증비용을
  공제하여 **일반계정 내에 최저사망보험금 보증준비금 항목으로 적립**하고 사망보험금이
  기납입보험료보다 적은 계약이 발생한 경우 그 부족분을 보전해주는데 사용한다」 — the charge
  leaves the separate account and lands in a general-account reserve.
- The GMDB survives into the payout phase on the GLWB designs, running down by the annuity
  paid: 「연금개시 후 보험기간에는 사망시점의 "연금기준금액"에서 연금개시 후 보험기간 중
  발생한 실적배당 종신연금 연지급액의 합계를 차감한 금액을 말하며, 이 금액이 '0'보다 적은
  경우 '0'으로 합니다」. [S2] [S7] [S10]
- One carrier caps the enhanced death guarantee by attained age. 최저사망적립금 보증강화종료
  나이, after which the 보증강화형 falls back to the plain premiums-paid base [S7 제2조]:

      연금지급개시나이   최저사망적립금 보증강화종료나이
      55 ~ 59세          (연금지급개시나이 + 21)세
      60 ~ 69세          (연금지급개시나이 + 19)세
      70 ~ 79세          (연금지급개시나이 + 17)세
      80세               (연금지급개시나이 + 15)세

### 7. 최저연금적립금보증 (GMAB) — the guarantee the product is named for

- Definition, from the textbook: 「피보험자가 연금개시시점에서 생존하였을 경우 특별계정의
  펀드수익률과 상관없이 연금개시시점의 연금재원으로 최소한 기납입보험료 이상으로 설정된
  일정수준을 보증해주는 옵션」, with the identity [R2]:

      연금개시시 계약자적립금(최저보증 포함) = Max(기납입보험료, 연금개시시 계약자적립금)

- [R1] states the boundary precisely, and it is the most important single fact about this
  guarantee: 「만기에 적립된 금액이 최소보증금액보다 클 경우 보험회사는 이 적립금을 연금에
  활용하거나 일시금을 지급하게 되는 것이다. 그러나 **만기 전에 사망 또는 해약이 발생하는
  경우 이 보증은 성립하지 않으며**, 따라서 보험회사는 약정된 금액만을 보험계약자에게
  지급하게 된다.」 It is a European option struck at one date, not a floor on the account.
- Every retrieved product document says the same thing in consumer language:
  「연금개시 전 보험기간 중 중도해지시 해약환급금은 최저보증되지 않습니다」 [S1];
  「해지환급금은 특별계정의 운용실적에 따라 변동되므로 최저보증이 이루어지지 않으며,
  원금손실이 발생할 수도 있습니다」 [S7 제50조제3항]; 「중도해지시에는 최저보증이 되지
  않습니다」 [S10]; 「중도해지시에는 경과확정보증액의 적용을 받지 않으며」 [S6];
  「변액보험을 중도에 해지하면 해약환급금에는 최저보증옵션이 적용되지 않습니다」 [S8].
- **Four ways the guaranteed level is set** [R1 <표 Ⅲ-2>]:

      Premium refund  연금 개시 시까지 납입하는 보험료 대비 일정비율에 해당하는 금액을
                      최저보증. 대부분의 상품은 일정비율을 100%로 설정. 연금 개시 시점까지의
                      거치기간이 길수록 일정비율이 증가하는 상품도 있음
      Step-up         계약자 적립금이 계약 시 정해진 일정 수준(기납입보험료의 110%, 120%,
                      130% 등)에 도달하면 보증수준도 이에 비례하여 증가
      Ratchet         일정주기로 계약자적립금을 파악하여 해당 시점에서의 계약자적립금이 직전
                      주기에 설정된 보증금액을 초과하면 그 시점 이후 보증금액이 이에 비례하여
                      증가
      Roll-up         기납입보험료를 특정 이율로 부리한 금액을 최저보증

- [R1] works the four against one common set of fund values — ₩1,000,000 a month for ten
  years then five years deferred, roll-up at 5% simple, step-up at 110/120/130% of premiums
  paid, ratchet every three years. The table is worth reproducing because it is the only
  retrieved numerical comparison of the four (단위: 만원):

      구분  경과  기납입보험료  계약자적립금  적립률  롤업   스텝업  래칫
      납입기 1년      120          109        90.6%    126     120     120
             2년      240          224        93.4%    264     240     240
             3년      360          346        96.2%    414     360     360
             4년      480          475        99.0%    576     480     480
             5년      600          612       102.0%    750     600     600
             6년      720          757       105.1%    936     720     757
             7년      840          909       108.2%  1,134     840     757
             8년      960        1,070       111.5%  1,344   1,070     757
             9년    1,080        1,240       114.8%  1,566   1,240   1,240
            10년    1,200        1,153        96.1%  1,800   1,240   1,240
      거치기 11년    1,200        1,121        93.4%  1,860   1,240   1,240
            12년    1,200        1,624       135.3%  1,920   1,624   1,240
            13년    1,200        1,112        92.6%  1,980   1,624   1,240
            14년    1,200        1,056        88.0%  2,040   1,624   1,240
            15년    1,200        1,003        83.6%  2,100   1,624   1,240

  The roll-up dominates uniformly at a 5% simple credit against a fund that ends below its
  premiums; the step-up locks in the year-12 spike; the ratchet, tested only every three
  years, misses it. This is the clearest available demonstration that the guarantee design,
  not the guarantee level, is what drives the option cost.
- **Census at 2017-05-31** [R1]: of 36 products, **27 guaranteed the annuity fund** either as
  standard or as an option; 3 of those let the policyholder decline it; **9 were designed
  with no GMAB at all**; and **22 set the guarantee above premiums paid** by step-up or
  roll-up. The report's summary text also gives 26 in one place and 27 in another for the
  count of guaranteeing products — the discrepancy is in the source and is recorded here
  rather than resolved.
- **Observed GMAB charges from retrieved product documents**:

      0.25% p.a. of 특별계정계약자적립액  +  0.30% p.a. of 보험료총액,
        the second component charged during the premium period, capped at 7 years   [S1]
      0.85% p.a. of 특별계정적립액, only while the elective guarantee is switched on [S9]
      none — the guarantee is funded by a CPPI overlay instead                       [S6]
      no GMAB offered                                                       [S4] [S5]
      GLWB instead of GMAB                                        [S2] [S7] [S8] [S10]

  The textbook's illustrative disclosure table uses **계약자적립금의 연 0.5%** for a
  보증형 against 없음 for a 미보증형 [R2]; that is a teaching figure, not a market rate.
- Note the shape of [S1]'s charge. A premium-based component levied for at most seven years
  on the **whole** premium the policyholder has undertaken to pay — past and future — front-
  loads the guarantee cost onto a fund that has barely accumulated. On the illustration
  point (₩300,000 × 12 × 10 = ₩36,000,000 of 보험료총액) that component alone is
  ₩36,000,000 × 0.3% = ₩108,000 a year for seven years, against a first-year fund of about
  ₩3.3 million.

### 8. Roll-up — the guarantee that grows on a fixed schedule

Two retrieved contracts define a roll-up base, and both use **simple** interest applied day
by day to each premium as it is paid.

- **[S2] KDB생명 최저연금기준금액.** 「기준 기본보험료 및 기준 추가보험료에 … 매년
  최저연금기준금액비율 해당액을 해당보험료 납입일 … 을 기준으로 **일자 계산하여** 더한
  금액」, with the ratio 「(가) 계약일부터 20년이 되는 계약해당일의 전일: **7/100(연단리
  7%기준)**; (나) 20년 이후부터 연금개시나이 계약해당일까지: **6/100(연단리 6%기준)**.
  다만, 계약일부터 연금지급개시나이 계약해당일까지의 기간이 20년 미만인 경우 (가)에 따라
  7/100로 적용합니다.」 The document then converts it for the representative contract:
  「(다) 대표계약기준(40세 남성, 10년납, 연금개시나이 65세) 복리이자율로 환산시 **연복리
  4.32%**」. That conversion is the number a model should target.
- **[S7] 교보생명 최저연금기준금액.** 「기준 기본보험료 및 기준 추가납입보험료에
  납입기간동안 … 매년 **5/100** 해당액을, 납입기간이 지난후부터 연금지급개시나이
  계약해당일까지 … 매년 **4/100** 해당액을 일자 계산하여 더한 금액」. Where a
  납입 일시중지 has extended the premium term, the 5% band still uses the **original**
  premium term.
- **[S10] 미래에셋생명 최저연금 기준적립금** is a compound roll-up on a net base:
  「납입보험료에서 해당월의 위험보험료 및 부가보험료 등을 공제한 금액을 '최저보증 종신연금
  기준이율(최저연금보증형 1+α **연복리 1.0%**, 최저연금보증형 2+α **연복리 2.0%**)'에 따라
  계약일 이후부터 연금개시나이 계약해당일까지 계산한 금액」, with the explicit carve-out
  「최저연금 기준 적립금 계산시 보증비용은 차감하지 않으며, 「계약자적립금」을 중도인출한
  경우에는 약관에서 정한 최저연금 기준적립금이 감소됩니다」. So the roll-up base is
  gross of the guarantee charge but net of the mortality and expense loadings.
- Both KDB and Kyobo reduce the roll-up base pro rata on a premium reduction or a withdrawal,
  by re-deriving 기준 기본보험료 and 기준 추가납입보험료 under the reduction and withdrawal
  articles and then re-starting the accrual from the reduced base. [S2] [S7 제2조]
- [R1]'s 2017 census found two roll-up designs. 교보생명 「미리 보는 내 연금 변액연금보험」
  used 5%/4% simple, exactly as [S7] still does. DGB생명 「평생소득보장 변액연금보험」 used
  「기납입보험료의 매년 5/100 해당액을 해당 보험료 납입일을 기준으로 일자 계산하여
  기납입보험료에 더한 금액(연단리 5% 기준)」 with the accrual period capped at **the lesser
  of 20 years from the contract date and the pre-annuitisation term**.
- [R2] describes a third roll-up shape not seen in any retrieved contract — a guarantee that
  fixes at 100% of premiums paid at a stated point (10 years, or the end of the premium
  term) and then steps up a fixed percentage every fixed period, its worked example being
  100% → 106% → 112% → 118% every three years, i.e. **6% per three years, simple** — with the
  warning that such designs typically restrict the fund menu, forbid fund switching, and use
  a structured payoff (bonds plus a KOSPI200 volatility option) rather than a conventional
  fund.

### 9. Step-up — the guarantee that ratchets on fund performance

- Textbook definition [R2]: 「연금개시 전 보험기간 중 계약자적립금이 특별계정 성과에 의해
  미리 약정한 수준(예: 기납입보험료의 120%, 140%, 160% 등)을 달성하는 경우 그 이후 특별계정
  성과에 관계없이 연금개시시점 적립금은 달성된 수준으로 최저보증하는 형태」, with the
  operational consequence the sales force must disclose: 「약정된 적립금 수준 달성시 안정적인
  운용을 위해 **채권형 펀드의 운용비율이 의무적으로 상향조정**되는 것이 일반적」.
- Retrieved step-up ladders, all from [R1]'s 2017 census unless marked:

      미래에셋생명 글로벌자산관리 변액연금보험 — 단계별 목표기준금액 = 기본보험료
        합계액의 120% / 150% / 180% / 200% (Step 1–4), the excess over the previously
        attained step being added to both the minimum death and the minimum annuity
        guarantee; 기본보험료 합계액 is the total basic premium contracted for over the
        premium term, excluding rider and additional premium
      DB생명 스텝플러스 변액연금보험 — 100 / 130 / 160 / 190 / 220 / 250 / 300 / 350 /
        400 / 450 / 500% of total basic premium paid before the premium-completion date,
        with additional premium paid after completion guaranteed at 100%; the 초과성과금액
        is the difference between the step just attained and the step previously attained,
        and **is compulsorily transferred to the bond fund**
      KDB생명 트리플에셋 변액연금보험 (스텝형) — the same 100–500% ladder, evaluated daily
        from the third policy anniversary to three years before annuitisation, requiring the
        target to be met **on three consecutive business days**
      ING생명 오렌지 변액연금보험 — monthly evaluation, 100% to 200% in five 20% steps
      삼성생명 빅보너스 변액연금보험 — premiums paid guaranteed during the premium period;
        thereafter, at each annual valuation, once the account first reaches **130% of
        premiums paid** that 130% becomes both the minimum death and the minimum annuity
        guarantee
      신한생명 Safe Plus 신한변액연금보험 — step-up over the period from the contract date to
        the policy anniversary three years before annuitisation, the cumulative 초과성과금액
        being added to 「사망 시점 또는 연금 개시 시점의 이미 납입한 보험료」; [R1] elsewhere
        describes it as stepping 100% to 200% in 20% units
      KB라이프생명 투자의 힘 KB 변액연금보험Ⅱ — a **continuous** monthly ratchet rather than
        a ladder: 「보증형(중도선택형) 선택 시점 이후 매월 계약해당일의 계약자적립액이 그
        시점의 연금개시시점의 최저계약자적립액을 초과할 경우, 자동으로 그 초과 분을
        연금개시시점의 최저계약자적립액에 추가」                                        [S9]

- Two design details a model must carry. The step is tested **at a stated frequency** —
  monthly [S9] [S6], annually [R1 삼성], daily with a three-day confirmation [R1 KDB], or over
  a window ending three years before annuitisation [R1 미래에셋, 신한] — and once attained it
  cannot fall. And the step **triggers a portfolio change**, so the fund return process is
  not independent of the guarantee.
- [S6] is the purest ratchet retrieved and is worth setting out in full, because it dispenses
  with the guarantee charge altogether. **ABL생명 (무)하모니변액연금보험2404**:

      경과확정보증액
        1차월도       계약일의 기본보험료(특약보험료 제외) × 보증비율
        2차월도 이후  Max( 이미 납입한 보험료 × 보증비율,
                           매월 계약해당일의 계약자적립액,
                           직전월도 계약해당일의 경과확정보증액 )
      최저연금적립액  = 연금개시전까지의 경과확정보증액 중 가장 큰 금액
                        (연금개시전 보험기간 종료일에 한하여 보증)

      보증비율, by 연금개시전 보험기간:
        15년 이하        100%
        16년 ~ 44년      85% + 1% × 연금개시 전 보험기간 연수
        45년 이상        130%

  「최저연금적립액보증수수료 … 가 부가되지 않습니다.」 The ratchet is monthly, on the
  monthly policy anniversary, and the policyholder cannot choose the valuation date. The
  guarantee is void on surrender or lapse before the end of the pre-annuitisation period.

### 10. How a guarantee is funded when there is no guarantee charge

[S6] and [R1] together document the alternative to a basis-point charge: constrain the assets
so the guarantee is rarely in the money.

- **Auto Balancing (펀드자동재배분).** The account is split between a 성장자산펀드 and a
  안전자산펀드 whose weights are reset on a formula, starting equity-heavy and de-risking as
  annuitisation approaches. [S6]
- **The formula**, as [R1] recorded it for the previous generation of the same product:

      성장자산펀드 편입비율 =
          Min(기준성장자산적립금 × 승수, 특별계정 계약자적립금 × 80%)
          ÷ 특별계정 계약자적립금
      안전자산펀드 편입비율 = 100% − 성장자산펀드 편입비율

  — a constant-proportion portfolio insurance rule with an 80% equity cap. The current
  brochure confirms the multiplier is still in use and gives its range: 「"펀드별 편입비율
  적용 공식"에 적용되는 승수는 성장자산펀드편입금액을 계산하기 위한 배수(범위: **1.0 ~
  4.0**)로 이 특약으로 전환할 때 계약자에게 별도 공지합니다」, and the insurer may change it
  on written notice. [S6]
- **The absorbing barrier.** 「성장자산펀드 편입비율이 0%이며, 특별계정계약자적립액이
  [기준경과확정보증액 × 평가비율 × **1.02**]보다 같거나 적은 경우에는 자동으로 특별계정에서
  일반계정으로 전환되어 공시이율(최저보증이율 **연복리 1.75%**)로 운용되며, 이럴 경우에는
  특별계정으로 다시 전환되지 않습니다.」 [S6] Once the CPPI cushion is exhausted the contract
  becomes a general-account declared-rate contract, irreversibly, with a 1.75% floor
  pre-annuitisation and 0.5% after.
- [S6]'s fund-platform generation, from [R1], paired one 채권형 안전자산 fund with one of five
  growth funds — 코리아인덱스형, 코-원자재인덱스형, 글로벌인덱스 리스크콘트롤형,
  밸류 고배당주식 재간접형, 글로벌다이나믹멀티에셋형 — chosen at issue and fixed for the
  whole pre-annuitisation period.
- [S6] also carries a 실적배당연금전환특약 that continues the pattern into the payout phase:
  「보험기간 동안 투자실적이 악화되더라도 최저실적배당연금액으로 보장되며, 전환일시금의
  **연복리 1.75%**까지 최저 보장합니다. 최저실적배당연금액 보증을 위한 **보증수수료가
  없습니다**.」
- [R1] catalogues the same logic in other carriers' hands: 미래에셋 글로벌자산관리 requires
  the bond fund to be at least 50% of the 32-fund menu and raises the required bond
  **balance** with each step (Step-up 0–5 → 납입예정 총 기본보험료의 50 / 70 / 90 / 110 /
  130 / 150%); 푸르덴셜 VIP 변액연금보험 sets the bond-fund input ratio at ≥80% where the
  pre-annuitisation term is under 12 years, ≥70% at exactly 12 years and ≥50% above 12
  years — **the same ladder [S1] still publishes today**.

### 11. The 2016 change — the GMAB became optional

- [R1] and [R2] agree on the history and on the reason:
  - 변액연금 was originally required to guarantee both the minimum death benefit **and** the
    minimum annuity fund. [R1]
  - The 감사원's 2014 regular audit of the 금융감독원 directed that a way be found to
    「변액보험 최저연금적립금의 보증수수료를 낮추거나 없애는 방안을 마련」. [R1]
  - 「2016년 4월 전에 판매한 변액연금에는 최저연금적립금 보증(GMAB)비용이 의무부과되었으나
    이는 계약자 선택권을 제한한다는 의견이 제시되어 이와 관련된 법령(「보험업감독규정」 및
    「보험업감독업무 시행세칙」)이 개정되었다. 이에 따라 **2016년 4월부터는 변액연금의
    최저연금적립금(GMAB) 보증비용 부담여부를 계약자가 선택할 수 있다**.」 [R2]
  - The stated motives were 「수익률 제고와 보증비용 부담 경감, 소비자의 선택권 보장」. [R1]
- The disclosure a carrier must then give, in the textbook's model form [R2]:

      구분                    최저연금적립금 보증형     최저연금적립금 미보증형
      최저연금적립금 보증유무  O                        X
      최저연금적립금 보증비용  계약자적립금의 연 0.5%   없음
      연금개시시점의 적립금    이미 납입한 주계약        실제 계약자적립금
                              보험료와 실제 계약자
                              적립금 중 큰 금액

  with the mandatory caveat 「최저연금적립금 미보증형의 경우 최저연금적립금 보증비용이
  부과되지 않는 대신 연금개시시점에 적립금이 이미 납입한 보험료보다 적을 수도 있음」.
- The consequence for the illustration regime is concrete: an unguaranteed product must
  「해약환급금 예시를 제외하거나 (-)평균공시이율 가정을 포함하여 3개 이상의 수익률을
  가정하여 기재」 [R2]. [S9]'s illustration set of **−2.25% / 2.25% / 3.375%** is exactly
  that rule applied at a 평균공시이율 of 2.25%.
- Two of the six retrieved current products are unguaranteed by design ([S4] [S5]), one
  makes the guarantee an on/off election at any time ([S9]), one funds it without a fee
  ([S6]), and two charge for it ([S1] [S10]). [R1] predicted this: 「IFRS17이 도입되고
  보증리스크를 공정가치로 평가하여야 하는 보험회사의 입장에서 막대한 보증준비금을 적립하지
  않아도 되고 가입자 입장에서도 높은 보증수수료를 별도로 부담하지 않아도 되므로 연금적립금에
  대한 최저보증이 없는 변액연금상품의 출시와 판매가 늘어날 것으로 예상된다.」
- The counter-argument [R1] also makes, and which the product spec should record: 「최저보증이
  없는 변액연금상품은 펀드 등 유사한 금융상품과 차별성이 약하기 때문에 경쟁력 강화를 위한
  방안이 모색될 필요가 있다.」

### 12. GMWB and GLWB — the guarantee that survives annuitisation

- Taxonomy [R2]:
  - **GMWB (최저중도인출금 보증)** — 「보험기간 중 일정기간 동안 … 특별계정의 투자성과에
    관계없이 연금기준금액의 일정수준 이상을 인출할 수 있도록 보증」.
  - **GLWB (최저종신중도인출금 보증)** — 「연금개시 후 보험기간 중 연금재원을 특별계정에서
    운용할 경우 특별계정의 투자성과에 관계없이 연금재원의 일정수준을 종신토록 인출할 수
    있도록 보증」.
  - **GMIB (최저연금액 보증)** — 「연금개시 후 보험기간 중 지급될 연금액(적립금 ×
    연금지급률)을 보증. 통상 계약체결시점에 결정」. [R1]'s 2017 census found GMIB
    **미도입** in Korea; nothing retrieved in 2026 contradicts that, but nothing confirms it
    either — see the gaps section.
- [R1]'s 2017 census: GMWB was offered as an option on **5** of 36 products and GLWB on **7**,
  both usually packaged as a 선택특약 called 「실적배당보증연금」 or 「실적배당종신보증연금」
  alongside a conventional declared-rate annuity option. 「최저중도(종신)인출금을 보증하는
  변액연금상품의 경우 **최저연금적립금보증이라는 용어 대신 최저연금기준금액 보증이라는
  용어를 사용**하며, 연금 개시 직전의 연금적립금이 연금 개시 직후의 최초 연금기준금액이
  된다.」
- The GLWB payment identity, common to all retrieved GLWB contracts:

      실적배당 종신연금 지급액 = Max(연금기준금액, 계약자적립금) × 실적배당 종신연금 지급률

  [S2] [S7 제2조] [S8]
- **연금기준금액** is set at annuitisation and then, in the enhanced forms, ratcheted:
  - 「연금개시나이 계약해당일의 최저연금기준금액과 계약자적립액 중 큰 금액」 [S2] [S7 기본형]
  - 「이 후 매년 계약해당일에 직전 연금기준금액과 계약자적립금 중 큰 금액으로 연금기준금액을
    재설정합니다」 [S7 보증강화형]
  - 「연금개시 후 매년 계약해당일에 직전 연금기준금액과 계약자적립액 중 큰 금액을
    연금기준금액으로 재설정합니다」 [S8]
  - [R1] records a three-year reset cycle on 교보생명 「더 드림 교보변액연금보험」:
    「연금 지급기준금액 재설정일은 연금 지급개시 나이 계약해당일부터 매 3년 계약해당일이다」
  - 「연금기준금액 = max(연금개시시점의 계약자적립금, 최저연금기준적립금, 이미 납입한
    보험료)」 in effect at [S10], which takes the largest of three bases.
- **A withdrawal reduces the guarantee base proportionally**, and the formula is published:

      중도인출 이후의 연금기준금액
        = 중도인출 직전 연금기준금액
          × (중도인출 전 계약자적립액 − 중도인출금액) ÷ 중도인출 전 계약자적립액

  [S2] [S7 제51조제8항]
- **The GLWB is expensive.** [S2]'s 실적배당 종신연금 보증비용 is 연 3.30% of the
  최저연금기준금액 for the first 20 years and 연 1.70% thereafter and in the payout phase —
  an order of magnitude above every GMDB charge retrieved and four times the dearest GMAB
  charge. [S10] charges 연 0.30% (1+α) or 0.35% (2+α) of the separate-account value for its
  investment-linked lifetime annuity guarantee, which is far cheaper, but its guarantee base
  rolls up at only 1.0% or 2.0% compound against [S2]'s 7%/6% simple.
- The cost shows through in [S2]'s own illustration. The 상품요약서 prints
  「투자수익률 −1.0% 기준 (순수익률 **−4.7%**)」 and 「투자수익률 2.75% 기준 (순수익률
  **−1.0%**)」 — a gap of **3.7 and 3.75 percentage points** between gross fund return and
  net return to the account, which is the guarantee charges plus the asset-based charges.
  The consequence, on 남자 40세 / 기본보험료 30만원 / 10년납 / 60세 연금개시 (단위 원):

      경과   납입보험료    특별계정투입    −1.0% 해약   −1.0% 계약자   2.75% 해약
             누계          금액 누계       환급금       적립금         환급금
      3개월     900,000        821,934         28,015       817,765        33,105
      6개월   1,800,000      1,643,868        864,522     1,625,022       882,301
      9개월   2,700,000      2,465,802      1,690,400     2,421,650     1,728,421
      1년     3,600,000      3,287,736      2,505,532     3,207,532     2,571,299
      2년     7,200,000      6,575,472      5,656,231     6,241,231     5,906,997
      3년    10,800,000      9,863,208      8,625,561     9,093,561     9,177,129
      4년    14,400,000     13,150,944     11,406,062    11,757,062    12,370,431
      5년    18,000,000     16,438,680     13,990,349    14,224,349    15,475,328
      6년    21,600,000     19,726,416     16,371,111    16,488,111    18,479,925
      7년    25,200,000     23,014,152     18,541,110    18,541,110    21,372,003
      8년    28,800,000     26,301,888     20,376,180    20,376,180    24,022,005
      9년    32,400,000     29,589,624     21,986,226    21,986,226    26,534,029
      10년   36,000,000     32,877,360     23,364,227    23,364,227    28,894,817
      15년   36,000,000     32,635,440     12,072,407    12,072,407    21,971,449
      20년   36,000,000     32,393,520              0             0    11,542,988

  Three things fall out. The 해약환급금 and the 계약자적립금 coincide from year 7 onwards,
  which is where the 해약공제 reaches zero (§14) — and the year-1 difference, 3,207,532 −
  2,505,532 = **702,000**, reconciles to the published year-1 해약공제 of 71만원. The
  separate-account contribution stops growing after year 10 and then **falls** (32,877,360 →
  32,393,520) because the monthly deduction now comes out of the fund. And at a −1.0% gross
  return the account is **exhausted before year 20**, and even at the 평균공시이율 of 2.75%
  the surrender value at 20 years is ₩11.5 million against ₩36 million of premium — a 32.1%
  return of premium. A GLWB of this shape is not a savings product; it is a purchase of
  guaranteed lifetime income, and the technical notes must say so.

### 13. 지급률 — the published annuity rates

Three retrieved documents publish a payout rate, and they are the only closed-form annuity
factors found in this session.

**[S2] KDB생명 — annual rates.**

      실적배당 종신연금 지급률 = 기본지급률 × (1 + 장기유지 가산율 + 투자실적 가산율)

      기본지급률       연금개시나이   남자     여자
                       55~59세        4.00%    3.80%
                       60~64세        4.65%    4.45%
                       65~69세        5.10%    4.85%
                       70~80세        5.50%    5.30%

      장기유지 가산율  연금개시전 보험기간 (연금개시나이 − 가입나이)
                       10~19년   0%      20~24년   5%     25~29년  10%
                       30~39년  15%      40년 이상 25%

      투자실적 가산율  연금개시나이 계약해당일의 계약자적립액 ÷ 연금기준금액
                       60% 미만          0%
                       60% 이상 90% 미만 15%
                       90% 이상          30%

  「해당 지급률은 연금개시 후 보험기간 동안 동일하게 적용됩니다.」 [S2]

**[S7] 교보생명 — monthly rates, same structure, different bands.**

      기본지급률       연금지급개시나이   남자      여자
                       55~59세            0.29%     0.27%
                       60~69세            0.33%     0.31%
                       70~79세            0.37%     0.36%
                       80세               0.41%     0.41%

      투자실적 가산율  <60% 0% / 60~90% 15% / ≥90% 30%
      장기유지 가산율  5~19년 0% / 20~29년 10% / 30~39년 20% / 40년 이상 30%

      실적배당 종신연금 지급률 = 기본지급률 × (1 + 투자실적 가산율 + 장기유지 가산율)
      실적배당 종신연금 월지급액
          = Max(연금기준금액, 계약자적립금) × 실적배당 종신연금 지급률

  A 0.33% monthly rate is 3.96% a year, so the Kyobo and KDB scales are close once annualised.
  [R1] recorded the same carrier's earlier product at 0.30/0.29 (55–59), 0.35/0.33 (60–69),
  i.e. the scale has been **cut** between the 2017 census and the retrieved contract.

**[S8] 교보생명 방카슈랑스 — the rate as a closed-form formula.** This is the only algebraic
annuity factor retrieved and it is reproduced verbatim:

      일반형        : 연금지급개시나이 × (3 × 연금개시 전 보험기간 + 2 × 거치기간 + 100)
                      ÷ (365 × 365 × 12)
      10년 집중지급형: 위 값 × 1.4

  「거치기간(연단위)은 연금개시 전 보험기간(연단위)에서 납입기간(연단위)을 차감한 기간」;
  「실적배당 종신연금 월 지급률은 소수점 다섯째자리에서 반올림하여 소수점 넷째자리까지
  사용함」. Worked at 연금개시 65세, 연금개시 전 보험기간 25년, 납입기간 10년 (거치기간
  15년): 65 × (75 + 30 + 100) ÷ (365 × 365 × 12) = 65 × 205 ÷ 1,598,700 = **0.0083**; at
  연금개시 65세, 보험기간 20년, 납입기간 10년 it is 65 × 180 ÷ 1,598,700 = **0.0073**.
  **The unit of that number is not stated in the retrieved document** — whether 0.0083 is to
  be read as 0.83% a month or as 0.0083% a month is not resolvable from four pages — and the
  two readings differ by a factor of a hundred. Read as a percentage it is roughly 2.5 times
  the 기본지급률 in [S7]'s 약관 for the same age, which is implausible for a lifetime annuity;
  read as a decimal fraction of a percent it is implausibly small. **The formula's form is
  verified; its level is `[unverified]`.** A drafting pass that needs a payout rate should use
  [S2]'s annual scale or [S7]'s monthly scale and cite [S8] only for the shape of the
  age-and-term dependence.

**[R1]'s 2017 census** adds three more scales for context: 한화생명 「알고 받는
변액연금보험」, 흥국생명 「최저연금보증형 변액연금보험」 and 「행복한 선택 스텝업
변액연금보험」, 교보생명 「미리 보는 내 연금 교보변액연금보험Ⅱ」 (기본지급률 with 투자실적
and 장기유지 가산율 — the same three-factor structure), 교보생명 「더 드림
교보변액연금보험」 (실적배당 종신연금 지급률 0.30/0.29% at 55–59 and 0.35/0.33% at 60–69,
monthly), DGB생명 「평생소득보장 변액연금보험」 and 푸르덴셜생명 「평생소득 변액연금보험」
(노후소득보증금액 지급률). The **three-factor scale — a base rate by sex and annuity age,
uplifted by a persistency factor and by an in-the-moneyness factor — is therefore the Korean
market convention**, not one carrier's idea.

### 14. 해지공제 — the surrender charge and its seven-year run-off

- Statutory frame, from the textbook: 「해약공제액은 보험료납입기간(**납입기간이 7년 이상인
  경우 7년**) 이내에 계약을 해지할 경우 계약자적립액에서 차감하는 금액으로, 중도해지에 따른
  보험회사의 손해에 대한 패널티 성격이 있다」 [R2], and 「해약환급금의 경우 해지시점의
  적립금에서 해지공제액(**미상각신계약비, 최대 7년까지 적용**)을 차감한 후 지급」 [R2].
  So the charge is the unamortised acquisition cost, and seven years is the ceiling.
- **Three published scales, all on the same illustration point** (남자 40세, 기본보험료
  30만원, 10년납, 월납, 60세 연금개시), stated as a percentage of premiums paid to date:

      경과시점            1년     2년     3년     4년     5년     6년   7년  7년이상
      [S4] AIA 여유+     28.1%   11.7%    6.2%    3.5%    1.9%   0.8%   —      —
        금액 (만원)        101      84      67      51      34     17    —      —
      [S5] ABL 투자에강한 25.6%   10.7%    5.7%    3.2%    1.7%   0.7%  0.0%   0.0%
        금액 (원)      923,143 769,286 615,429 461,571 307,714 153,857   0      0
      [S2] KDB 행복드림  19.5%    8.2%    4.4%    2.5%    1.3%   0.6%  0.0%   0.0%
        금액 (만원)         71      59      47      36      24     12    0      0

  In every case 「해약공제비율 = 해약공제금액 ÷ 이미 납입한 보험료」.
- **The run-off is linear in the amount, not in the ratio, and all three scales are the same
  function.** Each fits `해약공제 = C × (7 − t) ÷ 7` for elapsed whole years `t = 1…7`:
  [S5]'s amounts decline by exactly ₩153,857 a year, giving `C = ₩1,077,000` with no
  rounding at all; [S2]'s 71 / 59 / 47 / 36 / 24 / 12 / 0 만원 are `C = 83만원` rounded to
  the 만원 (83 × 6/7 = 71.1, × 5/7 = 59.3, × 4/7 = 47.4, × 3/7 = 35.6, × 2/7 = 23.7,
  × 1/7 = 11.9); [S4]'s 101 / 84 / 67 / 51 / 34 / 17 만원 are `C = 118만원` on the same
  rounding (101.1 / 84.3 / 67.4 / 50.6 / 33.7 / 16.9). The published *ratio* falls much
  faster than the amount because its denominator — premiums paid — is growing.
- **A single-premium contract carries no surrender charge at all.** [S5]'s 거치형 table prints
  0 and 0.0% at every duration on a ₩50,000,000 single premium, because 「일시납 적립형
  변액연금의 경우 계약체결 직후 계약체결비용이 모두 부과되므로 보험기간 중 계약이
  해지되어도 해지공제비용이 부과되지 않는다」 [R1].
- **Market benchmark, 2017 census** [R1 <표 Ⅴ-2>], 「월납 변액연금의 평균 해지공제율」:

      경과시점  1년      2년     3년    4년    5년    6년
      최대      27.6%   11.5%   6.1%   3.5%   2.0%   1.0%
      평균      25.6%   10.7%   5.7%   3.2%   1.7%   0.7%
      최소      19.1%    7.9%   4.2%   2.4%   1.0%     —

  [S5]'s 2025 scale reproduces the 2017 industry **mean row exactly** — 25.6 / 10.7 / 5.7 /
  3.2 / 1.7 / 0.7 — [S4] sits above the 2017 maximum, and [S2] sits at the 2017 minimum. The
  distribution has not moved in eight years.
- The reform history behind the scale: 개인연금 활성화 방안 (2013-08) required a carrier to
  file its 산출방법서 unless it spread **at least 50% of the 계약체결비용 over seven years**
  (보험업감독규정 제7-51조), capped the deferrable share at 50% of the 계약체결비용, and cut
  bancassurance and online 계약체결비용 to **50% of the tied-agent channel** [R1]. [R1]
  reproduces the formula that regime implies:

      해약 시 공제액 = 판매보수(50%) × (7년 − 경과기간) ÷ 7년
        where 판매보수 = 연납순보험료 × 5% × 납입기간 − 유지보수

  which is exactly the linear-in-amount, seven-year run-off the three retrieved scales show.
- **Other transaction charges.** 중도인출수수료 Min(인출금액의 0.2%, ₩2,000) with 4 free a
  year [S4] [S5] [S6] [S10]; nil at [S1] [S2] [S9]. 펀드변경 (계약자적립금 이전) 수수료 ≤0.1%
  of the amount transferred, with any excess over ₩5,000 credited to the fund being left and
  4 free a year [S1], or ≤0.1% capped at ₩5,000 with 4 free and currently waived [S2], or
  Min(0.1%, ₩2,000) with 4 free [S10]; free at [S5] [S9].

### 15. 해지환급금 — computed daily, guaranteed never

- 「이 약관에 따른 해지환급금은 계약이 해지된 날의 기준가격을 적용하여 산출방법서에 따라
  계산합니다.」 On a voluntary surrender or a premium reduction the price used is
  「해지신청일 + 제2영업일」의 기준가격. 「해지환급금은 특별계정의 운용실적에 따라
  변동되므로 최저보증이 이루어지지 않으며, 원금손실이 발생할 수도 있습니다.」 Payment within
  three business days of the claim. [S7 제50조]
- The insurer must give the policyholder a table of surrender values by elapsed duration.
  [S7 제50조제6항]
- The published illustrations are the best model check available. **[S1] KB VIP 변액연금보험**,
  남자 40세 / 기본보험료 30만원 / 월납 / 10년납 / 60세 연금개시 / 채권형펀드 100%, 단위 만원:

      경과   납입보험료  특별계정   −1.00% (순 −1.32%)  2.25% (순 1.93%)  3.375% (순 3.055%)
             누계        투입누계   해약환급금  환급률  해약환급금 환급률 해약환급금  환급률
      1년        360        329          229     63%        235    65%       237     65%
      3년      1,080        988          879     81%        927    85%       944     87%
      5년      1,800      1,647        1,512     84%      1,644    91%     1,693     94%
      10년     3,600      3,295        3,014     83%      3,547    98%     3,755    104%
      15년     3,600      3,273        2,759     76%      3,821   106%     4,275    118%
      20년     3,600      3,252        2,523     70%      4,119   114%     4,871    135%

  The gross-to-net gap here is **0.32 pp** — the GMDB at 0.07% plus the GMAB's account-based
  0.25% — because the footnote is explicit that 「상기 순수익률은 보증비용이 차감(단,
  최저연금적립액 보증비용은 계약자적립액 기준 보증비용만 반영)된 후의 수익률」, i.e. the
  0.3%-of-total-premium component is **not** in the net return shown. That understates the
  drag in the first seven years, and a modeller reproducing this table must add it back.
- **[S6] ABL 하모니**, 1종(무사망형) 적립형, 남자 40세 / 60세 개시 / 10년납 / 월 30만원,
  단위 원, at 투자수익률 −1.0% (순 −1.01%), 2.75% (순 2.74%), 4.125% (순 4.115%):

      경과    납입보험료   −1.0% 계약자적립액  해약환급금  환급률
      3개월      900,000            821,751            0    0.0%
      6개월    1,800,000          1,640,435      640,364   35.6%
      9개월    2,700,000          2,456,065    1,494,458   55.4%
      1년      3,600,000          3,268,653    2,345,510   65.2%
      2년      7,200,000          6,488,801    5,719,515   79.4%
      3년     10,800,000          9,661,159    9,045,730   83.8%
      4년     14,400,000         12,786,438   12,324,867   85.6%

  The gross-to-net gap is **0.01 pp**, consistent with a product that charges no GMAB fee and
  has no death cover — the only charge inside the net return is the small 최저사망 element,
  and on the 무사망형 there is none. The zero surrender value at three months is the surrender
  charge exceeding the account.
- Three illustration returns are mandatory and their level is set by regulation: 「−1%,
  평균공시이율, 평균공시이율의 1.5배」 [R2]. 평균공시이율 is 「금융감독원장이 정하는 바에
  따라 산정한 전체 보험회사 공시이율의 평균으로 전년도 9월말 기준 직전 12개월간 보험회사
  평균공시이율」 [R2] [S10]. Observed values, which date each document:

      2.50%   [S7] (약관 제2조 「이 계약 체결 시점의 이율(2.5%)」), [S10] (−1.0 / 2.5 / 3.75)
      2.25%   [S1] (−1.00 / 2.25 / 3.375), [S9] (−2.25 / 2.25 / 3.375)
      2.75%   [R2] (2024년 적용), [S2] (−1.0 / 2.75), [S6] (−1.0 / 2.75 / 4.125)

  and 「2009년 4월 1일부터 공시규정 강화에 의해 저축성 변액보험의 경우 투자수익률과 함께
  **순수익률**을 예시하도록 되어 있다. 순수익률은 투자수익률에서 최저보증관련 비용 등이
  차감된 후의 수익률을 말한다.」 [R2]
- Where a contract has no GMAB the low illustration return must be **negative and at least
  three returns must be shown**, or the surrender-value illustration must be omitted:
  「최저연금적립금을 미보증하는 상품의 경우에는 … 해약환급금 예시를 제외하거나
  (-)평균공시이율 가정을
  포함하여 3개 이상의 수익률을 가정하여 기재하도록 하고 있다」 [R2]. [S9]'s −2.25% low case
  is that rule in operation.

### 16. 추가납입 and 중도인출 — the flexibility, and the guarantee leakage it creates

- **추가납입보험료** is capped at **200% of the basic premium** in every retrieved contract:
  「해당월까지 납입한 기본보험료(특약보험료 제외) 총액의 200% 이내」 [S1]; 「해당 월까지
  납입할 기본보험료(선납포함)의 200%」 with a per-month cap of 「기본보험료 × 200% ×
  해당 경과월수(선납포함) − 이미 납입한 추가보험료의 합계」 [S2]; 「해당월까지 납입한
  기본보험료 총액의 200% − 이미 납입한 추가납입보험료의 합계」 [S4]; 「(기본보험료 ×
  가입경과월수 + 선납보험료) × 200% − 이미 납입한 추가납입보험료의 합계」 [S7 제2조];
  200% of the contracted basic premium total, or of the single premium with an annual cap of
  20% of it, at [S5]; 200% at [S6].
- **A withdrawal restores additional-premium headroom**: 「계약자적립액의 인출이 있을 경우에는
  인출금액의 누계만큼 추가납입한도가 늘어납니다」 [S1], and the same rule in [S2] [S4] [S5]
  [S6] [S7].
- **중도인출** is uniformly 12 times a policy year, opening one month (occasionally one year)
  after the contract date:

      한도 50% of 해약환급금, residual ≥ ₩5,000,000 per 구좌            [S1]
      한도 50% of 기본보험료 해약환급금 + 추가보험료 적립액,
        residual ≥ ₩3,000,000 per 구좌                                  [S2]
      한도 50% of 해약환급금, residual ≥ 기본보험료의 1200%, opens at 1년 [S4]
      한도 50% of 해약환급금, residual ≥ ₩5,000,000 (적립형) or
        ≥ 30% of 기본보험료 (거치형), minimum ₩100,000 per withdrawal    [S5]
      한도 60% of 해약환급금, no fee                                     [S9]

- **A ten-year cap on cumulative withdrawals** appears in every retrieved contract and is the
  tax rule showing through into the policy conditions: 「계약일 이후 10년 이내에는 인출금
  총액이 실제 납입한 보험료 총액(단, 특약보험료 제외)을 초과할 수 없습니다」 [S1] [S2] [S5].
- Withdrawals come **out of the additional-premium account first**: 「중도인출은 추가납입
  보험료에 대한 계약자적립액에서 우선적으로 인출하며, 추가납입보험료에 대한 계약자적립액이
  부족한 경우에 한하여 기본보험료에 대한 계약자적립액에서 인출합니다」 [S5] [S2].
- **A programmed-withdrawal service** exists on one contract: 정기중도인출서비스, monthly, for
  a period of at least six months, at 「적립형: 납입한 보험료 총액의 0.1%~3.0% 이내;
  거치형: 0.1%~0.5% 이내」, free of charge and outside the 12-a-year count, stopping
  automatically when the residual falls below the floor. [S5] [S1] has a simpler
  자동인출서비스, 12 months per request, available from the second policy anniversary.
- [R1] identifies the withdrawal facility as a **guarantee-risk mitigant**, not only a
  convenience: 「국내 보험회사는 최저보증리스크 경감과 가입자의 편의를 위해 중도인출을
  허용하고 있다. 중도인출은 정해진 한도하에서 연 12회까지 허용되며, **중도인출금은
  최저보증한도에서 차감된다**.」 Every retrieved contract does deduct it, either from the
  guarantee base directly [S4] [S7] or proportionally [S2] [S7 제51조제8항].

### 17. Premium flexibility, waiver and early annuitisation

- **보험료 납입 일시중지** (premium holiday). [S1]: available after five years, 12 months per
  request, up to three requests; during the holiday the 위험보험료, both guarantee charges,
  the 부가보험료 excluding 기타비용 and the rider premium are deducted from the surrender
  value, and the holiday ends if they cannot be met; the premium term is extended, and if the
  extension leaves less than the minimum deferral period the annuity age is deferred. [S4]:
  not available on the 5-year-premium form; available after five years on the 10- and
  20-year forms. [S10]: the same charges are deducted from the surrender value during the
  holiday and the annuity date is deferred if the minimum deferral would be breached.
  [S7 제31조] carries the same institution.
- **보험료 납입중지** (permanent cessation). [S1]: after ten years, and only if
  「계약자적립액이 납입중지시의 이미 납입한 보험료(단, 특약보험료 제외)의 100% 이상」.
- **보험료 납입종료** (early termination of the premium obligation on a life event). [S1]:
  available on 퇴직, 폐업 or an accident or illness requiring three months or more of
  hospitalisation or convalescence, applied for within six months of the event and only after
  half the premium term has run; separately available after five years where the surrender
  value is at least ₩5,000,000 per 구좌; the minimum deferral period still applies afterwards.
- **보험료 납입면제.** Variable annuities normally have none — [R2] 「변액연금에는 변액종신보험
  등 보장성 보험과 달리 특정 장해상태시 제공되는 납입면제기능은 없는 것이 일반적이나 일부
  보험회사는 장해 또는 특정질병 진단시 납입면제를 해주는 곳도 있다」 — but it is offered as a
  rider: (무)보험료납입면제특약 on a 50%-or-more disability [S5] [S6]; 무배당 신보험료납입
  면제특약(3대질병형) on cancer (excluding 기타피부암, 갑상선암, 대장점막내암, 비침습
  방광암), 뇌출혈 or 급성심근경색증, with a **90-day cancer waiting period** [S2];
  납입면제특약Ⅱ(무)1904 in an 80%-disability and an 80%-disability-plus-three-major-illness
  form [S10]. Retrieved rider premiums, ₩500,000 monthly main premium, 20-year term,
  단위 원 [S5] [S6]: 남 30세 615, 40세 1,498, 50세 4,802; 여 30세 179, 40세 524, 50세 2,346.
- **조기연금개시** (early annuitisation) is common and its conditions are informative because
  they are all in-the-moneyness tests:
  - [S1]: the anniversary must be at least 7 years after issue (10 if 납입종료 was used),
    premiums must be complete, and the account must be **≥110% of premiums paid**; from age
    45; the account is moved wholly to the bond fund on application; and — decisively —
    「조기연금개시 신청시, **최저연금적립액은 보증되지 않습니다**」.
  - [S9]: premiums complete or 10 years elapsed, and 해약환급금 ≥ 100% of premiums paid;
    ages 45–80 (48–80 for a male joint life), or 35–80 if switching to a 확정연금형 or
    상속연금형.
  - [S10]: 해지환급률 ≥ 100% and 해약환급금 ≥ ₩5,000,000; ages 30–85 (45–85 for the
    조기집중 종신연금형); available on the **최저연금미보증형 only**; the menu of payout forms
    narrows if fewer than ten years have elapsed.
  The pattern is uniform: the insurer will let a policyholder annuitise early **only where
  the guarantee is out of the money**, which is a policyholder-behaviour lever a stochastic
  model has to respect.
- **일반계정 전환** (transfer to the general account before annuitisation) is the other side
  of the same coin, and [R1] documents it as an explicit risk-control device: 삼성생명
  빅보너스 permits conversion to a 공시이율형 once the account first reaches **130% of
  premiums paid**, irreversibly; 동양생명 수호천사 리셋 플러스 permits it two years after
  issue where the surrender value is at least premiums paid (plus cumulative step-up excess
  on the step-up form) and there is no outstanding policy loan, again irreversibly and with
  the performance-linked payout options withdrawn. [S6]'s CPPI barrier (§10) is an
  *automatic* version of the same transfer.
- **보험계약대출** is available and interacts with the separate account. [S5] offers a rider
  letting the loan be paid from the general account instead of the separate account, in which
  case 「보험계약대출금액은 일반계정에서 대출신청일에 지급되며 … 특별계정에서
  보험계약대출적립액은 발생하지 않습니다」; the loan rate is the 공시이율 of the insurer's
  then-current declared-rate product of the same class plus a spread. [R1] records DB생명
  스텝플러스 transferring the loan amount to the general account at 「대출신청일 + 제2영업일」
  and **deducting any unrepaid loan from the guaranteed amount at annuitisation**.

### 18. Fund selection, mandatory bond weights and automatic de-risking

- **How many funds.** 49 [S5], 51 [S10], 32 in the earlier generation of one product [R1],
  9 [S9], 8 [S1], 5 [S4], 9 [S2]. The menu size is itself a product decision: [R2] notes that
  the roll-up designs 「일반적으로 선택 가능한 펀드의 수가 적게 구성될 수 있으며 다른
  펀드로 변경이 안 되고」.
- **Selection at issue.** 「기본보험료 납입펀드를 채권형 펀드를 포함하여 3개까지 선택하실 수
  있습니다」, in 5% increments, with the short-duration bond fund not selectable at issue and
  capped at 25% thereafter [S1]. 「계약을 체결할 때 펀드 중 1개 이상을 선택할 수 있으며,
  복수로 선택한 경우에는 펀드별로 기본보험료의 투입비율을 선택하여야 합니다. 다만, 각
  펀드별 기본보험료는 5만원 이상으로 합니다」 [S5].
- **The mandatory bond weight is a function of the deferral period**, and the same ladder
  appears at two carriers eight years apart [S1] [R1 푸르덴셜 VIP]:

      연금개시 전 보험기간   채권형(및 단기안정채권형) 최소 투입·편입비율
      12년 미만              80% 이상
      12년                   70% 이상
      12년 초과              50% 이상

  It binds both the premium allocation and the account-value mix, and it survives every later
  switch. [S1]
- **Automatic rebalancing into bonds before annuitisation.** 「「연금지급개시일−3년」시점부터
  매년 연계약해당일에 … 채권형 및 단기안정채권형 계약자적립액의 합계가 펀드 전체
  계약자적립액의 80%(또는 70%) 미만인 경우: 연계약해당일의 기준가격을 적용하여 … 채권형
  계약자적립액이 자동 조정됩니다.」 [S1] [S7 제40조] does the same on a different trigger:
  「계약일부터 2년이 지난 후 … 매년 계약해당일에 채권형(단기채권형 포함) 이외 펀드의
  계약자적립금 합계액 중 **전체 계약자적립금의 30%를 초과하는 금액**은 … 채권형으로
  이전됩니다」.
- **펀드자동재배분** (periodic rebalancing to the chosen weights). Cycle 3 or 6 months [S5],
  6 or 12 months [S7 제40조], with the bond-plus-MMF floor of 60% enforced while a
  계약유지보장 is running [S5], and the 채권형 최소적립금 excluded from the reallocation [S7].
  Automatically cancelled at annuitisation [S7] and on electing the GMAB [S9].
- **펀드자동전환옵션** (target-return de-risking), the mechanic [R1] calls a
  ターゲット-type feature in the Japanese market. [S5]:
  1. The policyholder picks a 목표수익률 from **110% to 200% in 10% steps**, defined as
     「이미 납입한 보험료(특약보험료 제외) 대비 특별계정 적립액의 비율」.
  2. On reaching it, **the whole balance of every fund other than the chosen 채권형 or
     MMF재간접형 is transferred automatically** into that fund.
  3. The insurer must notify the policyholder in writing or by telephone within 30 days.
  4. The option is then released; a re-application must be at least the previously attained
     target plus one 10% step.
  5. Selectable or cancellable up to four times a year, and mutually exclusive with
     펀드자동재배분.
- **평균분할투자** (dollar-cost averaging on additional premium only): the additional premium
  goes wholly into the short-duration bond fund and is then fed into the chosen funds in
  equal monthly instalments over 3, 6 or 12 months, the last month sweeping the residue.
  [S7 제41조]
- **Fund choice is constrained by the suitability diagnosis**: 「보험계약자의 '변액보험
  가입성향 진단'에 따라 펀드의 선택이 제한될 수 있습니다」 [S5], and [S5] publishes its
  49-fund menu mapped onto five 투자성향 bands (위험선호형 / 적극투자형 / 위험중립형 /
  안정추구형 / 위험회피형) and six 위험등급 (2등급 높은위험 … 6등급 매우 낮은위험).
- **Electing a guarantee overrides fund choice.** [S9]: 「계약자가 연금개시시점의 최저계약자
  적립액 보증 신청시(납입기간 종료 후 자동으로 전환된 경우 포함) 회사가 정하는 방법에 따라
  계약자적립액을 "채권형II" 펀드 50%와 "EMP AI형"펀드 50%로 자동 펀드 변경하여 운용합니다.」
  [S10]: the 1+α form transfers everything to 글로벌MVP30 at the day before the
  (연금개시나이−1)세 anniversary, after which no fund choice remains; the 2+α form runs on
  글로벌MVP30 alone from the outset; and the equity cap is 80% unguaranteed, 60% for 1+α.
- **A performance bonus** is one carrier's answer to the same problem from the other
  direction — reward persistency instead of buying an option. [S9]: 「「연금개시전
  보험기간」 중 매월 계약해당일에 각 성과수익률(120%, 140%, 160%, 180%, 200%)에
  도달하였을 경우 … 각각 최초 1회에 한하여 **기본보험료의 100%**를 계약자적립액에 추가로
  투입해 드립니다」, 수익률 being 해약환급금 ÷ 이미 납입한 보험료. [S7 제6조] has an
  analogous 장기유지 보너스 funded from a general-account 장기유지 보너스 준비금 which is
  **forfeited on surrender** (「해지시점의 장기유지 보너스 준비금은 계약자에게 지급되지
  않습니다」, except on the insurer's bankruptcy) [S7 제50조제5항], and a 장기유지 운용보수
  환급 [S7 제7조].

### 19. The payout phase

- **The default is a transfer to the general account and a declared-rate annuity.** 「대부분의
  변액연금상품은 연금개시 이후 일반계정의 공시이율을 반영하여 계산된다는 점이다. 즉, 연금은
  연금개시시점의 계약자적립금을 기준으로 연금지급개시 후의 공시이율이 적용되므로 상대적으로
  안정적인 연금을 수령할 수 있다.」 [R2]
- **The 공시이율 floors** are published per contract, and they step down with elapsed
  duration:

      경과 5년 이하 1.25% / 5~10년 1.00% / 10년 초과 0.50% 연복리          [S5]
      경과 5년 미만 1.00% / 5~10년 0.75% / 10년 이상 0.50% 연복리          [S1]
      전환 후 10년 이하 1.00% / 10년 초과 0.50% 연복리 (연금전환특약)      [S2]
      연금개시전 1.75% / 연금개시후 0.50% 연복리 (일반계정 자동전환분)     [S6]

- **Payout forms.** The menu is uniform across carriers:
  - **종신연금형 보증기간부** — guarantee periods of 10 / 15 / 20 years, to age 100, or
    「기대여명보증」; 정액형 or 체증형 (3% [S1], 5% or 10% [S5] [S2] [S4], 5% [S9]); a
    소득보장형 paying an extra 50% or 100% during the guarantee period [S5]. Where the
    insured dies inside the guarantee period the remaining instalments are still paid on
    their due dates, or may be commuted at the 공시이율 [S5] [S2].
  - **종신연금형 보증금액부** — pays for life, and on death before the total paid reaches the
    annuity consideration the shortfall is paid as a lump sum [S5] [S2] [S4]. A 자유형 variant
    lets the policyholder set a 제1연금연액 over a 제1연금기간 of 5–10 years totalling 10–80%
    of the consideration, then reverts to a computed lifetime amount [S5].
  - **확정연금형** — 5 / 10 / 15 / 20 years [S1], plus 25 [S2], plus 30 / 50 / 60 [S5].
  - **상속연금형** — the interest only, with the account paid on death [S1] [S5] [S2].
  - **노후설계자금 / 선지급행복자금** — a front-loaded slice of the consideration: 「연금개시
    시점의 연금계약 계약자적립액에 노후설계자금 선택비율을 곱한 금액」 [S1] [S5] [S6], or
    10–30% in 10-point steps taken as a lump sum or over 5 or 10 years [S2].
  - Two payout forms may be combined, in 10% steps [S1].
- **The annuity factor is not locked at issue.** 「보증기간부 종신연금의 경우 연금지급개시전
  연금생명표의 개정 등에 따라 연금액이 증가하게 되는 경우에는 연금개시 당시의 연금생명표 및
  계약자적립액을 기준으로 산출한 연금액을 지급하여 드립니다」 [S1], and the same one-way
  ratchet at [S5] and [S2]. So the mortality basis is re-struck at annuitisation but only in
  the policyholder's favour — which is a real option and is why [R1] classifies 사망률리스크 as
  a guarantee risk in its own right.
- **The annuity amount moves with the 공시이율 after it starts**: 「연금개시후 보험기간의
  공시이율이 한번이라도 변경된 경우 해당 연도의 연금연액은 과거 '해당 연도와 동일한
  공시이율이 적용된 연도'의 연금연액과 차이가 있을 수 있습니다」 [S5]. A charge is taken from
  each payment — 「연금연액은 … "연금연액에 부과되는 계약관리비용"을 차감하여 계산됩니다」
  [S5]; 연금 연액의 0.5% [S4]; 구좌당 매월 min(영업보험료의 3.5%, 4,000원) [S2].
- **Where the payout stays in the separate account**, [R2] warns that 「이 상품은 공시이율적용
  연금형태에 비해 연금액의 증감이 크게 나타난다」 and that the guarantee charge continues to
  be deducted from the separate account for life.

### 20. 보증준비금 and 보증위험액 — how the guarantee is reserved and capitalised

- Statutory hook: 「책임준비금의 일종으로 적립되는 보증준비금은 보험금 등을 일정 수준 이상으로
  보증하기 위해 장래 예상되는 손실액 등을 고려하여 적립하는 금액이다(보험업감독규정시행세칙
  <별표 24>)」 [R1]. A search result additionally attributes the requirement to 보험업감독규정
  제6-11조 제10호 and the calculation to 시행세칙 제4-15조; **neither article was retrieved**
  and both numbers are `[unverified]`.
- The measure: 「보증준비금은 평가단위별로 「사망률, 해지율, 자산이익률(1,000개)을 이용하여
  만기까지 장래 예상되는 순손실액을 현가로 환산한 상위 30% 평균 금액(**CTE(70)**)」과
  「보험종류별·최저보증별·보증수준별·주식비중한도별 **표준 적립기준**」 중 큰 금액으로
  한다」 [R1].
- **The standard factor tables, as reproduced in [R1]**. For 변액연금 GMAB:

      주식비중한도      기납입보험료 보증, by 보증수준                   스텝업
                        95% 미만  95–105%  105–115%  115% 이상          롤업 등
      40% 미만          0.7%×Max{적립률,0.40%}÷0.5%  … 0.55%÷0.5%       0.60%÷0.5%
      40% 이상 50% 미만 0.7%×Max{적립률,0.45%}÷0.5%  … 0.60%÷0.5%       0.65%÷0.5%
      50% 이상 60% 미만 0.7%×Max{적립률,0.50%}÷0.5%  … 0.65%÷0.5%       0.70%÷0.5%
      60% 이상          0.7%×Max{적립률,0.55%}÷0.5%  … 0.70%÷0.5%       0.75%÷0.5%

  The four 보증수준 columns for each equity band step the inner floor by 0.05 percentage
  points, so the full grid runs from `0.7% × Max{적립률, 0.40%} ÷ 0.5%` in the bottom-left
  cell to `0.7% × Max{적립률, 0.75%} ÷ 0.5%` in the top-right. For the other guarantee types
  the factor is a plain floor:

      주식비중한도       변액연금       변액연금        변액연금       변액보험(연금 제외)
                         GMDB           GMWB            GLWB           저축성    보장성
                                                                       GMDB      GMDB
      40% 미만           Max{적립률,     Max{적립률,     Max{적립률,    Max{적립률, Max{적립률,
                          0.04%}          0.6%}           0.6%}          0.04%}     0.2%}
      40% 이상 50% 미만   0.05%           0.7%            0.7%           0.05%      0.3%
      50% 이상 60% 미만   0.06%           0.8%            0.8%           0.06%      0.4%
      60% 이상            0.07%           0.9%            0.9%           0.07%      0.5%

  with the notes 「기타 최저보증의 경우 최저보증 성격에 따라 상기 적립기준을 준용함」;
  「**적립률 = 직전 1년간 최저보증비용 합계 ÷ {(기시 계약자 적립금 + 기말 계약자 적립금) ÷
  2}** (단, 최저보증비용은 상품별로 적용함)」; and 「주식비중한도는 기초서류상 최대 주식투자
  비중을 적용함. 다만, 기초서류상 최대 주식투자 비중이 실질적인 보증리스크를 반영하지 못할
  경우 예외적으로 처리할 수 있음」. [R1]

  **This is why the mandatory bond weight matters to the insurer and not only to the
  policyholder**: the reserve factor is indexed to the maximum equity weight permitted by the
  filed basis, so lowering the equity cap lowers the reserve floor directly.
- **보증위험액** (required capital) is 「장래 예상되는 순손실액의 상위 5% 평균 금액」 —
  a CTE(95) — 「과 다음 구분단위별 최저한도 중 큰 금액에서 보증준비금을 차감하여 산출하되,
  산출결과가 영(0)보다 작은 경우 영(0)으로 한다」, with the floors [R1 <표 Ⅳ-8>]:

      저축성최저사망보험금   계약자적립금의 0.15%
      보장성최저사망보험금   계약자적립금의 1%
      최저연금적립금         계약자적립금의 2%
      기타                   계약자적립금의 2%

- **Fair-value phase-in.** 「변액보험 보증부채에 대한 공정가치평가는 IFRS17 시행에 대비하여 …
  2017년 5월 시행되었다」, replacing fixed risk factors with a stochastic method, and the
  capital increase was phased: 「2017년 12월 말에 요구자본 증가액 중 **35%**를 반영하며,
  2018년 12월 말에는 **70%**, 2019년 12월 말에는 **100%**를 반영」. [R1]
- **Hedging is recognised.** 「변액보험의 최저보증리스크 헤지를 위한 파생상품거래는
  한도규제예외파생금융거래에 해당하며, 위기상황을 가정한 해당 파생상품 가치에서 보유하고
  있는 파생상품 가치를 차감한 금액을 보증위험액과 상계할 수 있다. 이때, 위기상황을 가정한
  보증준비금 및 파생상품 가치는 **주식가격 12% 상승·금리 90bp 상승, 주식가격 12%
  상승·금리 90bp 하락, 주식가격 12% 하락·금리 90bp 상승, 주식가격 12% 하락·금리 90bp
  하락**을 각각 적용한 4가지 경우 중 가장 큰 금액이다.」 [R1] Those four corners are the
  only explicit guarantee stress scenario retrieved.
- **IFRS 17 / K-ICS layer.** Under the 2023 regime both reserves become statutory reserves
  inside retained earnings rather than liabilities, restricting distributable profit: the
  **해약환급금준비금** captures the excess of the contractual surrender obligation over the
  fair-valued liability (which arises when rates rise), and the **보증준비금** is 「기존
  보증준비금 + 장래 수취할 보증수수료」. [R8]
- **Risk taxonomy for the guarantee** [R1]: 시장리스크 (「리스크 노출량을 합하여도 리스크가
  감소하지 않는다. 모든 보험계약자들이 같은 입장에 있어 동시에 보증을 이용하려고 하기
  때문이다」 — the law of large numbers does not apply); 사망률리스크 (longevity raises the
  value of GMAB/GMIB/GMWB, mortality raises the cost of GMDB; this one *does* diversify);
  계약자행동리스크 (persistency, fund choice and option take-up — 「헤징이 불가능하며」);
  and 운영리스크. The report is explicit that **dynamic lapses are the market convention**:
  「동적해지율이란 최저보증 발생률(In-the-moneyness)에 따라 해지율을 달리 적용하는 방법으로,
  최저보증 발생률이 높을수록 해지율을 감소시키고, 최저보증 발생률이 낮을수록 해지율을
  증가시켜야 한다」.
- **Hedging practice** [R1]: 무헤지 자본금 충당 (self-insurance, suitable where the guarantee
  level is low and behaviour risk small); 재보험 (「소형사에게 있어서 재보험은 보증리스크
  관리를 위한 가장 실용적인 방법」, but reinsurers cap liability and decline behaviour risk);
  정적헤징 (bought long options — 「장외시장이라 하더라도 만기 10년 이상인 옵션을 구입하기
  어려우며」); and 동적헤징 (delta and rho hedging with futures and swaps, gamma and vega with
  options — 「변액보험이 전체 상품 포트폴리오에서 큰 부분을 차지하는 보험사에 적합」).

### 21. Sales regulation — the licence, the diagnosis and the monitoring

- **The licence.** A producer must pass the 생명보험협회 변액보험판매자격시험 before selling
  any variable product and must tell the customer they hold it; after passing, 「4시간 이상
  판매 전 교육을 이수하여야 하며 **매년 1회 4시간 이상 보수교육**을 이수하여야 한다」 [R2].
  Statutory basis 보험업법 제83조, 시행령 제56조, 보험업감독규정 제5-4조; candidates must be
  solicitors under 보험업법 제83조 excluding those handling only non-life or third-sector
  products; 40 questions, 60 minutes, pass mark 70/100 [R6]. [S1] states it on the product:
  「이 상품은 생명보험협회에서 실시하는 자격시험에 합격한 모집 종사자에 한하여 판매할 수
  있는 상품입니다」.
- **적합성 진단.** 「보험회사 또는 모집종사자가 보험계약자의 변액보험계약 체결 전에 면담 또는
  질문을 통해 보험계약자로부터 파악한 정보를 바탕으로 보험계약 성향 분석을 실시하고
  보험계약자에게 적합한 보험계약 목록을 제공하는 것」 [R2]. It is compulsory for an
  일반금융소비자 under 금융소비자보호법 제17조; selling without recommending engages 제18조
  (적정성원칙) [R2] [R14]. The information gathered must include 연령, 재산상황, 보험계약
  체결의 목적, experience of acquiring and disposing of financial products, and understanding
  of financial products [R2].
- **취약금융소비자.** 「만 65세 이상 고령자, 미성년자, 정신적 장애로 일상이나 사회생활에서
  제약을 받는 자 등」 may be judged 부적합자 under a separate standard — 「다만, 만 65세 이상
  고령자 중 변액보험 계약체결 경험이 있거나 금융투자상품에 가입(투자)한 경험이 있는 자는
  취약금융소비자로 판단하지 않는다」 [R2].
- **The governing codes** are the 「변액보험 표준계약 권유준칙」 and the 「변액보험
  모범판매규준」, under which the seller must explain the main terms, the possibility of loss
  and the material loss on early surrender, and must hand over a 변액보험 주요내용 확인서;
  a post-sale completeness monitoring call (해피콜) is separately required by the
  보험업감독규정 [R2].
- **What the supervisor found in 2025** [R3]: overall grade 「양호」, unchanged from the
  previous exercise in 2019; by section, 적합성원칙 and 설명의무 rated 우수 or 양호; the two
  weakest items were **「변액보험의 자산운용 방식」** and **「위법계약해지권」**; 청약철회
  안내 rated 보통. Of nine insurers, five 우수 (삼성, 하나, 교보, KDB, ABL), one 양호
  (미래에셋금융서비스), one 보통 (메트라이프), two 미흡 (신한라이프, KB라이프파트너스).
  The FSS said it would strengthen monitoring of aggressive selling into a rising equity
  market, require improvement plans from the two 미흡 companies, and hold meetings with the
  largest sellers.

### 22. Disclosure — what must be published, and where

- **Carrier disclosure.** Every insurer selling variable products must run a 변액보험공시실
  inside its 상품공시실 and publish, **daily**, 「특별계정 운용현황(기준가격, 기간별 수익률 및
  연환산수익률, 매월 말 자산구성내역, 특별계정보수 및 비용 등)」, post the 변액보험
  운용설명서, and let a logged-in policyholder see 「개인별 적립금, 해약환급금, 특별계정 펀드
  보유좌수, 펀드변경 내역 및 방법」 and the 수수료 안내표. [R2] [S1] names both its own
  변액보험공시실 and the association's 「공시실 > 상품비교공시 > 변액보험 > 펀드현황」 as the
  places to check the 기준가격.
- **변액보험 운용설명서** must be handed over on application, must carry a risk warning on its
  cover, and must cover the product outline, the flow diagram, the fund list, the
  특별계정보수 및 비용 and the asset-management options. [R2]
- **보험계약관리내용** must be provided in writing at least once a year for contracts in force
  a year, and **quarterly** for variable contracts, showing for a savings-type variable
  contract 「납입보험료와 납입보험료에서 사업비, 위험보험료를 차감한 특별계정 투입금액 및
  계약자적립금」. Because the separate account is treated as a 자본시장법 투자신탁, an
  자산운용보고서 confirmed by the trustee must also go out quarterly. [R2]
- **Association comparative disclosure.** The 생명보험협회 publishes daily unit prices and
  returns by fund with asset composition, fees and manager, and lets a consumer compare
  carriers; the returns shown are 「조회일자 기준 1년, 3년, 5년, 7년, 10년, 15년 또는 전체
  운용기간 동안의 펀드 전체의 수익률이므로 … 개별 계약자에게 실제 적용되는 수익률은
  아니다」. For savings-type variable products it also publishes 사업비율, 위험 보장비율 and
  **최저보증비용비율**, and an expected-return comparison over 1–20 years. [R2] The portal's
  variable-insurance section carries 보장성/저축성 상품비교, 시장현황, 상품별 펀드운영현황,
  신상업정보, 상품별 과거수익률 and 펀드현황. [S12]
- **수수료 안내표.** Compulsory before sale (in the 상품설명서), after sale (on the insurer's
  site, per contract) and always (in the association's 공제금액구분공시 screen or the
  상품요약서), and must contain 보험관계비용 (계약체결비용, 계약관리비용, 위험보험료),
  특별계정운용비용 (특별계정 운용보수, 기초펀드 보수·비용, 증권거래비용 등), 보증비용
  (최저연금적립금 및 최저사망보험금 보증비용 등), 연금수령 기간 중 비용 and 해약공제비용.
  [R2] This is precisely the table reproduced in §5 from [S2] and [S4].

### 23. 예금자보호 — the carve-out that applies only to the guarantee

- The general rule: a variable contract is **outside** the 예금자보호법. 「이 상품의
  해약환급금 등 지급금은 '예금자보호법'에 의해 보호받지 않습니다」 [S8].
- The carve-out, dated by the textbook: 「**2016년 6월**부터 변액보험의 「예금자보호법」과
  관련된 내용이 변경되었다. 변액보험은 「예금자보호법」의 적용대상에서 제외되지만 **최저보증
  옵션에 따른 최저보증보험금에 한해서는** 「예금자보호법」에 따라 예금보험공사가 보호하는
  것으로 변경되었다.」 [R2]
- Contract wordings: 「약관에서 보험회사가 최저보증하는 최저사망적립액, 최저연금적립액 및
  특약에 한하여 예금자보호법에 따라 예금보험공사가 보호하되, 보호 한도는 … 1인당 "최고
  5천만원"」 [S1]; 「약관에서 보험회사가 최저보증하는 보험금 및 특약에 한하여 … 1인당
  "5천만원까지"」 [S2]; 「실적배당 종신연금 보증 및 최저사망적립금은 예금…」 [S7 제63조].
- **The limit was raised to ₩100 million (1억원).** [S5] and [S6], both produced 2025-10-01:
  「보호 한도는 해약환급금(또는 만기 시 보험금)에 기타지급금을 합하여 1인당 "**1억원까지**"
  (본 보험회사의 여타 보호상품과 합산)이며, 이와 별도로 본 보험회사 보호상품의 사고보험금을
  합산하여 1인당 "1억원까지" 입니다. 다만, 보험계약자 및 보험료납부자가 법인인 보험계약의
  경우에는 보호되지 않습니다.」 The date and instrument of the increase were not retrieved —
  see the gaps section — but the change is directly evidenced by two 2025 documents against
  the ₩50 million figure in the 2023–2025 documents [S1] [S2] [R2].

### 24. Tax

- 변액연금보험 is a **non-qualified** annuity: it earns no contribution-stage tax credit, and
  its benefit is 이자소득 rather than 연금소득. [S8] sets the two side by side:

      구분              연금저축                    연금보험
      소득구분          연금소득                    이자소득
      세제혜택 적용요건 보험료 납입 및 인출요건     일시납·월적립식 저축성보험 계약요건
                        충족                        또는 종신형연금보험 계약요건 충족
      보험료 납입시     연금계좌 세액공제           없음
      보험금 수령시     연금소득 분리과세(3~5%)     보험차익 비과세(이자소득세 비과세)

- The three routes to exemption of the 보험차익, from [R2] (which restates 소득세법
  시행령 요건):
  1. **일시납 저축성보험** — at least ten years from first payment to maturity or surrender,
     and total premiums per policyholder across all such policies not exceeding **₩200
     million (2억원)** for contracts written to 2017-03-31 and **₩100 million (1억원)** for
     contracts written from 2017-04-01. Excluded where the premiums are drawn down as an
     annuity over a fixed period ending inside ten years.
  2. **월적립식 저축성보험** — at least ten years to maturity or surrender; a premium term of
     at least five years; level monthly basic premium with advance payment of no more than
     six months; and, for contracts written from 2017-04-01, **total monthly premium per
     policyholder not exceeding ₩1.5 million (150만원)**, computed as the annual average
     `(해당연도의 기본보험료 + 추가납입보험료) ÷ 경과 개월 수`. Additional premium of up to
     ₩18 million a year still qualifies.
  3. **종신형 연금보험** — annuity from age 55 to death after the premium term; no benefit
     paid other than as an annuity; the contract and the annuity fund extinguish on death
     (or at the end of a guarantee period set inside the 통계청 life expectancy); policyholder,
     insured and beneficiary the same and no surrender after the first annuity payment; and
     the annual annuity not exceeding `연금계좌 평가액 ÷ 기대여명 연수 × 3`.
- A contract may be **elected as taxable** at issue or later, in which case its premiums do
  not count against the caps; the reverse election is not permitted. Where an exemption
  condition fails, the tests are applied in order 종신형 → 월적립식 → 일시납. Changing the
  policyholder's name, converting a protection contract to a savings contract, or increasing
  the basic premium by more than one times the original all **re-start the ten-year clock**.
  [R2]
- Rider premium on a variable annuity qualifies for the 보장성보험료 credit: 「납입한
  특약보험료 연간 100만원 한도로 납입금액의 100분의 12를 세액공제」 [S5] [S6].
- A 장애인전용보험전환특약 is offered under 소득세법 제59조의4 제1항 제2호 and 시행령 제107조
  제1항. [S5]
- Payout-phase taxation of a 실적배당 종신연금 was not established by any retrieved document
  and is `[unverified]`.

### 25. Market size, persistency and consumer experience

- **Premium income (수입보험료), 변액보험 as a whole, 조원** [R9]: 2021 17.9 (+4.1%),
  2022 12.7 (−29.0%), 2023 12.2 (−4.0%), 2024(E) 11.6 (−4.9%), 2025(F) 10.1 (−12.7%).
- **First-year premium (초회보험료), 변액보험 as a whole** [R3]: 2024 ₩1.97조, 2025 ₩2.89조
  (**+46.2%**); H1 2024 ₩0.84조, H1 2025 ₩1.38조 (+64.7%). [R9] had forecast a 45.9% fall in
  2025 first-year premium on base effects — **the outturn was the opposite sign and a similar
  magnitude**, which is worth remembering before treating any Korean VA volume forecast as
  reliable.
- **Complaints** [R3]: 1,308 variable-insurance complaints in 2025, about **9%** of all
  life-insurance complaints.
- **Stock, at the last retrieved measurement** [R1]: 변액보험 적립금 **₩109.1조 (109.1조원)**
  at 2016-09-30 across about **8.3 million policies**, which the report characterises as
  「국민 약 6명당 1건」. 변액보험 초회보험료 for Q1 2017 was ₩5,455억 against ₩2,152억 a year
  earlier.
- **Persistency** [R1]: 「변액보험의 **7년 평균 유지율은 30% 미만**으로 알려져 있다」, citing
  a 2016-11-16 금융감독원 press release. This is the single most important behavioural fact in
  the file and it is second-hand within [R1]; treat the 30% as indicative.
- **Time to break even** [R1]: 「계약체결 후 적립금이 납입한 보험료인 원금에 도달하기 위해서는
  약 **7~10년**의 기간이 걸릴 수 있으므로 중도 해지 시에는 원금에 미달할 가능성도 있다.」
  The retrieved illustrations bear this out: [S1] crosses 100% between years 10 and 15 at
  2.25% and between 5 and 10 at 3.375%; [S2] never crosses it in twenty years at either
  return, because of the GLWB charge.
- **Where the money goes** [R1]: 「선취상품은 납입보험료의 **5~15%**를 계약체결비용(신계약비)과
  계약관리비용(유지비)으로 차감한 후 **85~95%**만 투자하므로 펀드수익률에 비해 납입보험료
  대비 수익률이 낮게 되는 특성이 있다.」 The 91.3–91.5% observed in §4 sits squarely inside
  that band.
- **Distribution economics, 2017 census** [R1 <표 Ⅴ-3>], 월납 변액연금 모집수수료율 as a
  percentage of total premiums the policyholder will pay:

      연차        1년     2년     3년     4년     5년     합계
      최대       2.38%   0.73%   0.70%   0.48%   0.11%   3.13%
      평균       1.34%   0.41%   0.28%   0.25%   0.11%   2.11%
      최저       0.63%   0.19%   0.13%   0.12%   0.11%   1.10%
      상품 수     21종    38종    14종     3종

  and for single-premium products 「계약 체결과 동시에 모집수수료가 전액 선취되며, 27종
  상품의 평균 모집수수료율은 **2.47%**로 조사되었다」. 일시납 거치식 계약체결비용 averaged
  **4.19%** of the single premium, charged at once. Monthly 계약관리비용 ran 4.15–9% of the
  basic premium inside the first 7/10/13/15 years or the premium term and 0.3–2% thereafter,
  「월납 기본보험료에 부과되는 것이 일반적이나 납입기간 이후에는 월납기본보험료와
  계약자적립금을 기준으로 혼합부과되는 하이브리드 방식과 계약자적립금만을 기준으로
  부과되는 방식도 사용되고 있다」; single-premium 계약관리비용 averaged 0.77% at inception
  and 0.198% of the single premium monthly thereafter.
- **The cheapest channel.** [R1] found exactly one variable annuity buyable directly online
  — 미래에셋생명 「온라인변액연금」 — with **no acquisition commission at all** and
  보험관계비용 of 「초기 10년간 3%, 11~20년간 1% 초반」, itemised as 계약체결비용 10년 이내
  기본보험료의 **1.3%** (3,900원), 계약관리비용 납입기간 이내 **1.70%** (5,100원) and
  납입기간 이후 **1.00%** (3,000원), 위험보험료 0.0217%~0.0397% (65원~119원). Against the
  5.17–6.12% 계약체결비용 of the tied-channel products retrieved here, the online form is
  roughly **a quarter of the price**. Bancassurance and online 계약체결비용 were capped at
  50% of the tied-agent level from 2016 [R1].
- **Realised fund returns.** The only figures retrieved are from a **trade news article**
  reporting the association's disclosure as at 2026-04-30 [R10]: domestic equity leaders
  71.32% / 49.01% / 48.04% annualised, overseas equity leaders 44.61% / 44.16% / 43.08%.
  These are the *top* of a distribution and cannot support a central assumption. The one
  live fund panel retrieved directly [S11] tells the opposite story — a unit price of 904.24
  against 1,000.00 after fourteen years, 연평균 −9.58%. **Any return assumption in the model
  must be `[std]`.**

---

## Variation across carriers

Carrier identity below is by `[S#]` tag. Where a row is bracketed by a single source that is
said, because a range of one is not a range.

### Issue and term envelopes

      Source  가입나이            납입기간              최소거치기간   연금개시나이
      [S1]    만15세~70세         5/7/10/12/15/20년납,  5년납 5년;     45~80세
                                  (개시나이−7)세납      기타 7년
      [S2]    만15세~70세         5/7/10/12/15/20년납   5년            55~80세
      [S4]    0~70세 (5년납)      5/10/20년납           5년 / 1년 /    MAX(45,
              0~66세 (10년납)                           (20년납 미기재) A+B+C)~80세
              0~56세 (20년납)
      [S5]    만15세~(개시나이−   5/7/10/11~(기간−5)    (기간에 내재)  45~80세
              연금개시전기간)세   년납; 거치형 일시납
      [S6]    0세 또는 만15세~    5/7/10/11~(기간−7)    (기간에 내재)  45~80세
              (개시나이−기간)세   년납; 거치형 일시납
      [S9]    0~[개시나이−12/15/  7/10/12/15/20년납     5년            45~80세
              17/20/25]세, 최대
              가입나이 70세
      [S10]   0~[A−(납입기간+3)]  3/5/7/10/12/15/20/    3년 (미보증형) 45~85세 (미보증)
              세 (미보증형);      25/30년납; 일시납     5년 (보증형)   55~80세 (보증형)
              0~[A−(납입기간+5)]                        7년 (3년납
              세 (보증형); 최대                          보증형)
              75세

  **Range:** issue age 0–75; premium terms 3–30 years plus single premium; minimum deferral
  1–7 years; annuity age 45–85 with the guaranteed forms starting later (55) and ending
  earlier (80). The minimum deferral period is the insurer's first line of defence against
  the GMAB and it lengthens with the guarantee, exactly as [R1] describes:
  「연금적립금을 보증하는 상품의 경우 일반적으로 **최소거치기간을 5년 또는 7년** 정도
  설정하고 있다.」 [R1] records ABL 하모니's earlier generation at 「적립형의 경우 7년 이상,
  거치형의 경우 10년 이상」, and [S6]'s current pre-annuitisation term floors of 14 years
  (적립형) and 10 years (거치형) are the same device expressed differently.

### Premium size

      최소 기본보험료  ₩300,000/월 [S1] · ₩50,000/월 [S2] · ₩100,000/월 [S4] [S10] ·
                       ₩200,000/월 [S5] [S6] · ₩500,000/월 (<10년납) or ₩200,000 (≥10년납) [S9]
      최대 기본보험료  ₩1,000,000/구좌 [S1] [S2] [S9] · ₩100,000,000 [S4] ·
                       ₩5,000,000/구좌 [S10] · ₩150,000,000 [S2 가입한도]
      일시납 최소      ₩15,000,000 [S5] [S6] · ₩5,000,000 [S10]
      보험료 할인      >₩1,000,000 초과분의 2.0%; >₩2,000,000 초과분의 2.5% + ₩20,000,
                       기본보험료의 2% 한도 [S5] [S6]

### The guarantee

      Feature              Observed values                                    Range
      GMDB base            이미 납입한 보험료 [S1][S4][S9][S10];               premium ↔
                           최저연금기준금액 (roll-up) [S2][S7 보증강화형]       roll-up
      GMDB charge          0.05% p.a. of AV [S4][S9][S10];                     0.05–0.40%
                           0.07% p.a. of AV [S1];
                           0.40%/0.25% p.a. of 최저연금기준금액 [S2]
      GMAB present         yes, charged [S1][S9];                              charged ↔
                           yes, unfunded (CPPI) [S6];                          absent
                           no [S4][S5]; GLWB instead [S2][S7][S8][S10]
      GMAB charge          0.25% p.a. of AV + 0.30% p.a. of 보험료총액          0 ↔ 0.85%
                           (≤7년) [S1]; 0.85% p.a. of AV [S9]; none [S6]
      GMAB level rule      premiums paid [S1][S9 at election];                 100% ↔ 130%
                           100–130% by term, monthly ratchet [S6];             ↔ 500%
                           step ladder to 500% of premium [R1 DB, KDB]
      GLWB charge          3.30%/1.70% p.a. of 최저연금기준금액 [S2];           0.30–3.30%
                           0.30% (1+α) / 0.35% (2+α) p.a. of AV [S10]
      Roll-up rate         7%/6% simple, ≈4.32% compound on the                1.0% ↔ 7%
                           representative contract [S2];
                           5%/4% simple [S7]; 1.0% or 2.0% compound [S10];
                           6% per 3 years [R2 illustrative]
      Ratchet frequency    monthly [S6][S9]; annual [S7 보증강화형][S8];        monthly ↔
                           3-yearly [R1 교보 더드림]; daily with 3-day          3-yearly
                           confirmation [R1 KDB 트리플에셋]
      Guarantee optional   fixed at issue [S1][S10];                           issue-only ↔
                           electable and revocable any number of times [S9];   any time
                           not offered [S4][S5]
      Equity cap           80% [S10 미보증]; 60% [S10 1+α]; single fund         single fund
                           [S10 2+α]; 채권형 ≥80/70/50% by term [S1][R1 푸르덴셜] ↔ 80%

### The fee stack

      Item                    Observed values                                Range
      계약체결비용            5.17% of 기본보험료 for 10 years [S2];          1.3% ↔ 6.12%
                              6.12% for 10 years then 0.00% [S4];
                              1.3% for 10 years (online) [R1 미래에셋]
      계약관리비용 납입 중    3.50% [S2]; 2.34% [S4]; 1.70% (online) [R1]     1.7% ↔ 3.5%
      계약관리비용 납입 후    1.33% [S2]; 2.00% [S4]; 1.00% (online) [R1]     1.0% ↔ 2.0%
      위험보험료              0.004–0.011% [S2]; 0.0040–0.0107% [S4];         essentially
                              0.0217–0.0397% (online, 보장 포함) [R1]         nil
      특별계정 운용보수       0.20–0.78% [S4]; 0.25–0.64% [S9];               0.20% ↔ 0.89%
                              0.32–0.89% [S5]; 0.345–0.815% [S1];
                              0.4–0.7% [S2]
      증권거래·기타비용       0.00–0.10% [S4]; 0.01–0.79% [S2]                0.00% ↔ 0.79%
      기초펀드 보수·비용      0.11–0.45% [S4]; 0.01–0.21% [S2]                0.01% ↔ 0.45%
      연금수령기간중 비용     연금 연액의 0.5% [S4];                          0.5% of income
                              min(영업보험료의 3.5%, ₩4,000)/월/구좌 [S2]     ↔ a capped fee
      추가납입 loading        없음 [S1][S4][S5][S6][S9][S10]; 1.5% [S2]       0% ↔ 1.5%
      중도인출 수수료         없음 [S1][S2][S9];                              0 ↔ ₩2,000
                              Min(0.2%, ₩2,000), 연 4회 면제 [S4][S5][S6][S10]
      펀드변경 수수료         없음 [S5][S9]; ≤0.1% capped ₩5,000, 연 4회       0 ↔ ₩5,000
                              면제 [S1][S2]; Min(0.1%, ₩2,000) [S10]
      해약공제 1년차          28.1% [S4]; 25.6% [S5]; 19.5% [S2];             19.1% ↔ 28.1%
                              2017 census 19.1–27.6%, mean 25.6% [R1]
      해약공제 window         7 years, linear in amount, zero from year 7      uniform
                              [S2][S4][S5][R1][R2]; none on 일시납 [S5][R1]

### Options and services

      중도인출 limit        50% of 해약환급금 [S1][S2][S4][S5]; 60% [S9]
      중도인출 residual     ₩5,000,000/구좌 [S1][S5]; ₩3,000,000/구좌 [S2];
                            기본보험료의 1200% [S4]; 기본보험료의 30% (거치형) [S5]
      중도인출 opens        1개월 [S1][S2][S5][S6][S7]; 1년 [S4]
      10-year withdrawal    cumulative withdrawals ≤ premiums paid — universal
        cap                 [S1][S2][S5]
      추가납입 한도         200% of basic premium — universal [S1][S2][S4][S5][S6][S7][S10]
      납입 일시중지         after 5 years, 12개월 × 3회 [S1]; after 5 years on 10/20년납,
                            not on 5년납 [S4]; present [S7][S10]
      조기연금개시          ≥7년 and AV ≥110% of premiums, guarantee forfeited [S1];
                            ≥10년 or paid-up and CV ≥100% [S9];
                            CV ≥100% and ≥₩5m, 미보증형 only [S10]
      일반계정 전환         at 130% of premiums, irreversible [R1 삼성];
                            after 2 years at CV ≥ premiums, irreversible [R1 동양];
                            automatic at the CPPI barrier, irreversible [S6]
      펀드자동전환옵션      110–200% in 10% steps, to 채권형 or MMF, 연 4회 [S5]
      펀드자동재배분        3/6개월 [S5]; 6/12개월 [S7]; present [S6][S9]
      성과보너스            기본보험료의 100% at each of 120/140/160/180/200% [S9];
                            장기유지 보너스 from a general-account reserve, forfeited on
                            surrender [S7]

### What does not vary

Across every retrieved product: the separate account is set up under 보험업법 제108조제1항
제3호 and accounted for separately [R4] [S7]; the unit is ₩1 at establishment and the unit
price opens at ₩1,000 per 1,000좌 and is published to two decimals [S7] [R2]; the account is
valued **daily** and the separate-account management fee is deducted **daily** while the
mortality charge and the guarantee charges are deducted **monthly on the 월계약해당일**
[S7 제36조] [R2]; a GMDB is compulsory [R1 quoting 보험업감독규정 제7-60조 제7호]; **the
surrender value carries no guarantee whatever** [S1] [S6] [S7] [S8] [S10]; the surrender
charge runs off to zero within seven years [S2] [S4] [S5] [R2]; additional premium is capped
at 200% and a withdrawal restores the headroom [S1]–[S7] [S10]; withdrawals are limited to
twelve a policy year and, within ten years, to the premiums paid [S1] [S2] [S5]; the
guarantee base is reduced pro rata for withdrawals and premium reductions [S2] [S4] [S7];
the annuity factor may be re-struck at annuitisation but only upward [S1] [S2] [S5]; the
product may be sold only by a licensed 변액보험판매관리사 who has done four hours of
refresher training in the year [R2] [R6] [S1]; a 적합성 진단 must precede the recommendation
[R2] [R3] [S5]; three illustration returns must be shown with a 순수익률 beside each [R2];
and the contract is outside the 예금자보호법 except for the guaranteed amounts [R2] [S1]
[S2] [S5] [S6] [S8].

---

## Fetch failures and gaps

### URLs tried and not opened, or opened and empty

- **국가법령정보센터 (law.go.kr) — the friendly and the administrative-rule forms return the
  page shell only.** `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196`
  (보험업감독규정) returned HTTP 200 with navigation chrome and the version banner
  (시행 2023-03-02, 금융위원회고시 제2023-10호) but no article text;
  `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687` (보험업감독업무시행세칙)
  behaved the same way; `https://www.law.go.kr/LSW//lsSideInfoP.do?lsiSeq=266041&joNo=0053…`
  (보험업법 시행령) returned the instrument's identity — **시행 2024-10-25, 대통령령
  제34960호** — and its administering division, but again no article text. **What did work**
  was the `print=print` variant of `lsLawLinkInfo.do`, which returned 보험업법 제106조 in
  substance [R5]. Record for the library: on law.go.kr, prefer
  `lsLawLinkInfo.do?...&print=print`; expect `admRulLsInfoP.do` and `lsSideInfoP.do` to give
  only the shell.
- **`https://lbox.kr/v2/statute-admin/보험업감독업무시행세칙` — HTTP 403.** No retry with a
  different form was attempted.
- **`https://www.ulex.co.kr/법률/2100000235980-21843-보험업감독` — truncated.** The mirror
  serves 보험업감독규정 but the returned document stopped around 제4-20조, well short of
  제7-60조.
- **`https://www.easylaw.go.kr/CSP/FlDownload.laf?flSeq=317766` — downloaded but unreadable.**
  A 752 KB binary that is not a well-formed PDF; local extraction produced only fragments and
  dates spanning 2003–2008, so it is an obsolete edition in any case.
- **`https://www.fsc.go.kr/comm/getFile?srvcId=RULENOTICE&upperNo=3507&fileTy=ATTACH&fileNo=8`
  — wrong document.** Downloaded and extracted cleanly (39 pp.) but it is a 규제영향분석서 on
  독립손해사정사 selection and 자산건전성 classification, not 보험업감독규정 text.
- **`https://pub.insure.or.kr/upload/26_1분기 상품유형별 통계.pdf` — refused.** The
  생명보험협회 portal returned 「적절하지 않은 경로를 통한 요청입니다」 to a direct request for
  a statistics file whose name the index page itself supplies. The four quarterly files named
  on the index — 26_2분기 상품유형별 통계.pdf, 26_2분기 펀드유형별 통계.pdf, 26_1분기
  상품유형별 통계.pdf, 26_1분기 펀드유형별 통계.pdf — were therefore **not** opened.
- **`https://www.klia.or.kr/consumer/stats/yearBook/list.do` — HTTP 503.** The 생명보험협회
  통계연보 index was unavailable at the access time.
- **`https://i-kiin.net/…/新지급여력제도K-ICS-해설서_게시.pdf` — page, not document.** The URL
  returned a blog post announcing the 금융감독원 K-ICS 해설서 (2022.12) with a link, not the
  manual itself. The FSS's own copy was not located.
- **`https://www.fss.or.kr/fss/bbs/B0000188/list.do?menuNo=200218` — not opened.** The FSS
  press-release board was identified in search results but not fetched; the 2026-03-24 release
  was obtained instead from the 보험연구원 주간보험동향 reproduction, which is what [R3] cites.
- **WebFetch cannot read Korean PDFs.** Every Korean PDF attempted in this session — without
  exception — came back to WebFetch as raw stream data. All of them were re-extracted locally
  with **PyMuPDF**, which handled the Adobe-Korea1 CMaps correctly. Every figure quoted from
  [S1]–[S6], [S9], [S10], [R1], [R2], [R3] and [R9] therefore rests on a local text extraction
  rather than on a rendered page. The extractions were spot-checked by reconciling arithmetic
  that the documents themselves publish — [S2]'s year-1 surrender charge against the
  difference between its printed 계약자적립금 and 해약환급금 (702,000 ≈ 71만원), [S5]'s
  해약공제 amounts against exact sevenths, [R1]'s 별표 24 factors against the ranges printed in
  its own summary table — and all three reconciled.

### Facts left [unverified], and why

- **보험업감독규정 제7-60조 제7호 itself.** The clause making the GMDB compulsory is quoted
  verbatim twice inside [R1], but the regulation was **not retrieved**. The article number and
  the quoted sentence may be relied on; any broader statement about what 제7-60조 contains is
  `[unverified]`.
- **보험업감독업무시행세칙 <별표 24> and 보험업감독규정 제6-11조 제10호 / 시행세칙 제4-15조.**
  The reserve tables in §20 are reproduced from [R1], not from the rule. The article numbers
  come from a search-result summary only and are `[unverified]`. The tables are also **as at
  2018** and the reserving regime changed materially with IFRS 17 in 2023 [R8]; whether 별표
  24 survives in its 2018 form was not established.
- **보험업법 시행령 제52조 and 제53조.** Identified and dated (시행 2024-10-25, 대통령령
  제34960호) but not read. The summary in [R13] — one separate account per contract class,
  more than one permitted with FSC agreement, no voting rights on separate-account shares, no
  borrowing against a 제108조제1항제2호 account, no advance guarantee of a return on a
  변액보험계약, no transfers between the general and separate accounts — is from search-result
  text and is **entirely `[unverified]`**. No fact in the extraction section depends on it.
- **The special-account asset-concentration limits.** [R5] confirms that 보험업법 제106조 sets
  separate and generally higher limits for special accounts than for the general account, but
  the retrieved summary did not return their values. `[unverified]`.
- **The current text of 보험업감독규정 on the illustration returns.** [R2] states the
  −1% / 평균공시이율 / 1.5× 평균공시이율 rule and attributes it to the 보험업감독규정, and [S9]
  cites 「감독규정 제1-2조 제13호」 for the definition of 평균공시이율, but the regulation was
  not retrieved. The rule is well-evidenced by six independent product documents; the article
  numbers are `[unverified]`.
- **The date and instrument that raised the 예금자보호 limit to ₩100 million.** Two 2025
  documents [S5] [S6] state ₩1억원 where 2023–2025 documents [S1] [S2] [R2] state ₩5천만원.
  The change is certain; **its effective date and legal basis were not retrieved** and are
  `[unverified]`.
- **Whether the 2019 cut of the 추가납입 limit from 2× to 1× [R7] ever applied to variable
  annuities.** Every retrieved variable annuity, including three produced in 2025 and 2026,
  publishes a **200%** limit. Either the measure did not extend to this line, or it was
  reversed, or it was never implemented. Not established; the 200% figure is well-evidenced
  and the 2019 announcement is recorded beside it.
- **[S8]'s closed-form 지급률 formula.** The formula is reproduced exactly as printed, and its
  *form* is verified. Its *level* — about 1% a year on the worked example — is an order of
  magnitude below the same carrier's 약관 scale in [S7] and below [S2]'s scale, which means the
  two products define the rate against different bases. The discrepancy is real and is
  reported rather than resolved; **the level is `[unverified]`**.
- **GMIB.** [R1] found 최저연금액보증 **미도입** in Korea as at 2017-05-31 and [R2] lists it in
  the taxonomy without giving a Korean example. Nothing retrieved in 2026 shows a GMIB on
  sale, but nothing rules it out either. `[unverified]` as a current statement.
- **The 30% seven-year persistency figure.** [R1] reports it as 「알려져 있다」 with a citation
  to a 2016-11-16 금융감독원 press release that was **not retrieved**. It is the most
  load-bearing behavioural number in the file and it is second-hand and ten years old. Any
  lapse assumption in the model must be `[std]` with this cited only as an order of magnitude.
- **Dynamic lapse parameters.** [R1] establishes that dynamic (in-the-moneyness-dependent)
  lapse rates are the market and reserving convention and states the direction of the effect,
  but **no retrieved document publishes a functional form or any parameter**. A dynamic lapse
  formula in the model is a `[std]` construction.
- **Fund return distributions.** The only realised returns retrieved are the top of a
  cross-sectional distribution reported in a trade news article [R10] and one live fund panel
  showing a 14-year loss [S11]. **No volatility, no correlation, no time series was
  retrieved.** Every return and volatility assumption in the model is `[std]`.
- **The 경험생명표 basis for the annuity factors.** [S1] [S2] [S5] all say the annuity is
  computed 「연금사망률 및 공시이율을 적용하여 산출방법서에 따라」, and [S1] says the
  연금생명표 may be re-struck at annuitisation, but **no retrieved document publishes a single
  mortality rate**. The 제10회 경험생명표 is not published in full to the public — see
  `_research/regulatory-actuarial.md` — so the model's `mort_table.csv` is `[std]`.
- **Payout-phase taxation of a 실적배당 종신연금.** The accumulation-phase exemption tests are
  well-evidenced [R2] [S8]. How a lifetime withdrawal paid out of a separate account is taxed
  was not addressed by any retrieved document. `[unverified]`.
- **Current 보증준비금 and 보증위험액 magnitudes.** [R8] gives the IFRS 17 construction in
  words; no retrieved document gives an amount, a company figure or an industry total. The
  library **cites** the reserving regime and does not reproduce it; the model projects gross
  cash flows.
- **The 산출방법서.** Every contract defers the actual arithmetic of the account value, the
  annuity amount, the surrender value and the roll-up to the 「보험료 및 해약환급금
  산출방법서」, which is a filed document and is **not public**. This is the hard limit on how
  far a public-source reconstruction of a Korean variable annuity can go, and it is why the
  model's recursions are `[std]` constructions consistent with — not derived from — the
  retrieved documents.

### Carriers identified and not fetched

삼성생명, 한화생명, 신한라이프, 메트라이프생명, 동양생명, 흥국생명, DB생명, DGB생명,
푸르덴셜생명 and IBK연금보험 all appear in [R1]'s 2017 census or in [R3]'s 2025
mystery-shopping list, and none of their current product documents was opened. Their 2017
designs are recorded here through [R1]. Nine current carriers' documents were retrieved
([S1]/[S9] KB라이프, [S2]/[S3] KDB, [S4] AIA, [S5]/[S6] ABL, [S7]/[S8] 교보, [S10]/[S11]
미래에셋), spanning the unguaranteed, the charged-GMAB, the elective-GMAB, the unfunded-ratchet
and the GLWB shapes, which was judged sufficient to bracket every parameter the model needs.
Adding a tenth would mainly tighten the ranges in the variation section.
