# Regulatory and Actuarial References — Korea Life Insurance

**Status:** Draft, 2026-09-03.

Curated reference library for the Korea section of the reference-product library. It covers the
prudential and supervisory (금융위원회 / 금융감독원 / 보험업법 / 시행령 / 보험업감독규정 /
보험업감독업무시행세칙), actuarial (보험개발원, 경험생명표), public-statistics,
legislation-and-conduct, public-scheme and tax-and-accounting sources that the reference
cash-flow-model implementations (whole_life / term_life / ci_insurance / child /
indemnity_medical / cancer / long_term_care / pension_savings / variable_annuity /
immediate_annuity) rely on. Product folders cite entries on this page as **[REG-R#]** (e.g.
`[REG-R1]`); the R1–R62 numbering below is **frozen** — never renumber an entry and never reuse
a number, because ten product document sets cite against it. Within this page, plain `[R#]`
refers to the same entries. Facts stated under an entry that was actually retrieved were read
from the fetched document; a claim taken from general knowledge, from a search-result summary,
or from a document that could not be opened is tagged **[unverified]** and is a to-verify item,
not an established fact. Every failed fetch is disclosed in the entry that needed it and again
in §7. No URL on this page is fabricated. All URLs accessed **2026-09-03**.

**Regulatory architecture in one line:** the **금융위원회** (*Geumnyung-wiwonhoe*, Financial
Services Commission, FSC) makes the rules and grants the licence, the **금융감독원**
(*Geumnyung-gamdogwon*, Financial Supervisory Service, FSS) examines and writes the
implementing 세칙, and a Korean actuary works down a five-rung ladder — 법률 → 시행령
(Presidential Decree) → 시행규칙 (Prime Ministerial Rule) → **보험업감독규정** (an FSC 고시) →
**보험업감독업무시행세칙** (an FSS 세칙) → 별표 (schedules to either) — in which nearly every
operative number lives on the last two rungs and not in the statute [R1] [R9] [R23].
**보험업법** (*Boheomeop-beop*, Insurance Business Act) governs the *undertaking*; **상법 제4편
보험** (Commercial Act, Part IV) governs the *contract*; the two have different sponsoring
ministries (금융위원회 and 법무부) and Korean practice keeps them strictly apart [R1] [R49].

**Four things make the Korean frame unlike every other library in this repository, and a
document that imports a `jplib` or `uklib` reflex will be wrong about all four.**

1. **IFRS 17 and K-ICS have both been live since 2023-01-01.** K-IFRS 제1117호 「보험계약」 is
   the Korean adoption of IFRS 17 [R60] and **K-ICS** (신지급여력제도, the Korean Insurance
   Capital Standard) is the economic-value solvency regime [R13]; both commenced in the same
   quarter, under the same 부칙 [R14]. Japan's economic-value regime commences 2026 and the
   EU's long predates IFRS 17. Korea switched liability measurement and capital measurement
   together, and is four years into living with the result.
2. **On top of them sits the 해약환급금준비금** (*haeyak-hwangeupgeum-junbigeum*, surrender
   value reserve) — a company-level appropriation inside 이익잉여금 whose whole purpose is to
   stop an IFRS 17 balance sheet from distributing earnings that the contractual
   surrender-value floor would later demand [R11]. It has no counterpart in `uslib`, `uklib`,
   `jplib`, `frlib` or `delib`. It is a **distributable-earnings** device, not a solvency
   device.
3. **제3보험** (*je-sam boheom*, "third insurance") is a statutory licence category, not a
   market label. 보험업법 제4조제1항제3호 names 상해보험, 질병보험 and 간병보험, and 제4조제3항
   deems a fully licensed life insurer *or* a fully licensed non-life insurer to hold it, so
   both sides of the market write the same 암보험 and the same 간병보험 [R1]. Four of the ten
   `krlib` products sit in it, and the surrender-value rules reach them by the *mutatis
   mutandis* cross-references of 감독규정 제7-69조 and 제7-70조 [R19].
4. **경험생명표 is an industry table that is not published in full.** 보험개발원 (Korea
   Insurance Development Institute, KIDI) releases only 평균수명 and 기대여명 summary
   statistics for the 제10회 경험생명표 applied from 2024-04; the qx table itself goes to
   member insurers [R33] [R34]. There is no Korean analogue of Japan's downloadable 標準生命表
   or of the DAV tables documented in German Fachgrundsätze. **Every `mort_table.csv` in
   `krlib` is therefore a `[std]` construction** anchored on the public 국가데이터처 생명표
   [R38] and on the two published KIDI summary figures [R33], carrying a `provenance` column on
   every row. **Morbidity is a different case, and the distinction is easy to get wrong.** The
   **life-side** 참조순보험요율 are filed with the FSC and never published — a carrier's
   상품요약서 prints only the notification's document number, and the rate itself reaches the
   public only as the *ratio* called the 보험가격지수 [R4] [R22]. But 보험개발원 **does**
   publish a numeric **장기손해보험** 참조순보험요율 display, including an 암 발생률 grid by
   age and sex applied from 2024-04-01 [R61]. A `krlib` morbidity or incidence rate is
   therefore `[std]` only where that display does not reach it.

**Scope note on capital and reserving.** This library projects **gross best-estimate liability
cash flows**. 책임준비금 [R3] [R10], 해약환급금준비금 [R11], 보증준비금 [R10] [R26],
비상위험준비금 [R8], the K-ICS 요구자본 and its seven life sub-risks [R13], the K-ICS 경과조치
[R35] and the IFRS 17 risk adjustment and CSM [R60] are **cited, not specified** — the entries
below tell a drafter exactly what the regime requires without the library implementing any of
it, the same way `uklib` treats the SCR and `jplib` the ESR. What `krlib` *does* compute is the
**계약자적립액 / 보험료적립금** and the **해약환급금**, because those are contractual
quantities defined by the (unpublished) 산출방법서 and **bounded by a published schedule**,
별표 14 [R20]. That bound is the sharpest single difference from the US and UK libraries: in
Korea the surrender charge has a statutory cap with a formula, and it is public.

**Host behaviour, because it determined what this page can say.** `law.go.kr` serves statutes
and 행정규칙 as a JavaScript shell; the body comes from
`LSW/lsInfoR.do?lsiSeq=<id>&efYd=<yyyymmdd>` (법령) and `LSW/admRulLsInfoR.do?admRulSeq=<id>`
(행정규칙), and the 별표 — images inside those pages — come as PDFs through
`admRulBylContentsInfoR.do?bylSeq=<id>` then `flDownload.do?flSeq=<pdfFlSeq>`. That three-step
route is the only way 별표 14 [R20], 별표 15 [R21], 별표 27 [R24] and the 492-page 표준약관
[R25] were obtained. `fsc.go.kr` serves server-rendered HTML and its attachments; `fss.or.kr`
refused one fetcher and served another — see §7-D. Where a formula in a regulation is rendered
as an image, this page records it as not retrieved rather than paraphrasing it; §7-B lists
every one.

**A convention every product document inherits.** 감독규정 제1-2조제2호 defines the **기준연령
요건** as "전기납 및 월납 조건으로 **남자가 만 40세**에 보험에 가입하는 경우" [R9] — the single
reference cell at which the 표준해약공제액 comparison, the 보장성/저축성 test and the
보험가입금액 scaling are all computed. `krlib` makes it model point 1 wherever the product
allows.

---

## Product-relevance matrix

`x` = load-bearing (a product's documents cite the entry for a specific parameter, definition
or constraint); `(x)` = qualified or background relevance (context, framing, or a mechanic the
product names but does not model); blank = not indicated. Column key: **WL** = whole_life,
**TL** = term_life, **CI** = ci_insurance, **CH** = child, **MED** = indemnity_medical, **CAN**
= cancer, **LTC** = long_term_care, **PEN** = pension_savings, **VA** = variable_annuity,
**IA** = immediate_annuity.

| R# | Reference (short name) | WL | TL | CI | CH | MED | CAN | LTC | PEN | VA | IA |
|----|------------------------|----|----|----|----|-----|-----|-----|-----|----|----|
| R1 | 보험업법 제2조·제4조 — 보험상품 and 제3보험 | x | x | x | x | x | x | x | x | x | x |
| R2 | 보험업법 제5조·제127조·제128조 — 기초서류 | x | x | x | x | x | x | x | x | x | x |
| R3 | 보험업법 제120조 — 책임준비금 | x | x | x | x | x | x | x | x | x | x |
| R4 | 보험업법 제176조 — 참조순보험요율 | x | x | x | x | x | x | x | x | x | x |
| R5 | 보험업법 제181조·제184조 — 선임계리사 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R6 | 보험업법 제108조 — 특별계정 | | | | | | | | x | x | |
| R7 | 시행령 제1조의2 — 보험상품의 범위 | x | x | x | x | x | x | x | x | x | x |
| R8 | 시행령 제63조·제65조·제71조 | x | x | x | x | x | x | x | x | x | x |
| R9 | 보험업감독규정 — 고시 제2026-16호, 제1-2조 정의 | x | x | x | x | x | x | x | x | x | x |
| R10 | 감독규정 제6-11조 계열 — 책임준비금·보증준비금 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R11 | 감독규정 제6-11조의6 — 해약환급금준비금 | x | (x) | (x) | (x) | (x) | (x) | (x) | x | x | (x) |
| R12 | 감독규정 제6-11조의7·제6-13조 — 계약자배당 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R13 | 감독규정 제7-1조·제7-2조 — K-ICS 지급여력 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | 감독규정 제7-17조~제7-19조 and 부칙 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R15 | 감독규정 제5-6조·제5-7조·제6-26조 — 특별계정 | | | | | | | | x | x | |
| R16 | 감독규정 제7-60조 — 생명보험 상품설계 | x | x | x | (x) | | x | | x | x | x |
| R17 | 감독규정 제7-63조 — 제3보험 상품설계, 실손 | | | x | x | x | x | x | | | |
| R18 | 감독규정 제7-64조·제7-65조 — 산출방법서, 공시이율 | x | x | x | x | x | x | x | x | x | x |
| R19 | 감독규정 제7-66조~제7-70조 — 해약환급금, 무·저해지 | x | x | x | x | x | x | x | x | x | x |
| R20 | 감독규정 [별표 14] 표준해약공제액 | x | x | x | x | x | x | x | x | x | x |
| R21 | 감독규정 [별표 15] 보험가입금액의 산정 | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R22 | 감독규정 제4-32조·제7-45조·제7-51조 | x | (x) | (x) | (x) | x | (x) | (x) | (x) | (x) | (x) |
| R23 | 보험업감독업무시행세칙 (본문) | x | x | x | x | x | x | x | x | x | x |
| R24 | 시행세칙 [별표 27] 공시기준이율 산출 기준 | x | (x) | x | (x) | (x) | (x) | (x) | x | (x) | x |
| R25 | 시행세칙 [별표 15] 표준약관 | x | x | x | x | x | x | x | x | x | x |
| R26 | 시행세칙 [별표 22]·[별표 24] — not retrieved | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R27 | 제4차 보험개혁회의 — 계리가정·할인율 (2024-11-07) | x | x | x | x | x | x | x | x | x | x |
| R28 | 무(저)해지환급금 보험 상품구조 개선 (2019–2020) | x | x | x | x | (x) | x | x | (x) | (x) | (x) |
| R29 | 사업비·모집수수료 개편 (2019-08-01) | x | x | x | x | (x) | x | x | (x) | x | (x) |
| R30 | 자본규제 고도화 and 지급여력비율 현황 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R31 | 실손의료보험 개혁방안 (2025-04-01) | | | | (x) | x | (x) | | | | |
| R32 | 예금보호한도 1억원 (2025-09-01) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R33 | 보험개발원 제10회 경험생명표 (via 보험매일) | x | x | x | x | x | x | x | x | x | x |
| R34 | 보험개발원 공개 채널 — negative evidence | x | x | x | x | x | x | x | x | x | x |
| R35 | 보험연구원 — K-ICS 경과조치 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R36 | 보험연구원 CEO Report 03호 — 건전성 제도 | x | x | x | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R37 | 보험연구원 — 사업비 및 모집수수료 개선 (2019-04) | x | x | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R38 | 국가데이터처 생명표 (2024년, 2023년) | x | x | x | x | x | x | x | x | x | x |
| R39 | KOSIS 완전생명표 — not retrieved | x | x | x | x | x | x | x | x | x | x |
| R40 | 국가암등록통계 (2023년, 발표 2026-01-20) | (x) | | x | x | (x) | x | | | | |
| R41 | 건강보험환자 진료비 실태조사 (2024년도) | | | (x) | (x) | x | (x) | (x) | | | |
| R42 | 장기요양 등급 판정 현황 (2026-06-30) | (x) | | (x) | | (x) | | x | | | |
| R43 | 노인장기요양보험 통계연보 2024 — not retrieved | | | | | (x) | | x | | | |
| R44 | 2024년 실손의료보험 사업실적(잠정) | | | (x) | (x) | x | (x) | (x) | | | |
| R45 | 생명보험협회 공시실, FACT BOOK, 금융통계월보 | x | x | x | x | x | x | x | x | x | x |
| R46 | 보험연구원 「2026년 보험산업 전망」 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R47 | 한국보험신문 — 2025년 보험사 경영실적 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R48 | 평균공시이율 and 공시기준이율 — carrier disclosure | x | (x) | (x) | (x) | (x) | (x) | (x) | x | x | x |
| R49 | 상법 제4편 제1장 통칙 (제638조~제664조) | x | x | x | x | x | x | x | x | x | x |
| R50 | 상법 제4편 인보험 (제727조~제739조의3) | x | x | x | x | x | x | x | x | x | x |
| R51 | 금융소비자보호법 제46조 — 청약철회 | x | x | x | x | x | x | x | x | x | x |
| R52 | 예금자보호법 시행령 제18조 — 1억원 | x | x | x | x | x | x | x | x | x | x |
| R53 | 국민건강보험법 제41조·제42조·제44조 | | | (x) | (x) | x | (x) | (x) | | | |
| R54 | 노인장기요양보험법 제2조·제15조 등 | (x) | | (x) | | (x) | | x | | | |
| R55 | 노인장기요양보험법 시행령 제7조 — 등급판정기준 | (x) | | (x) | | (x) | | x | | | |
| R56 | 소득세법 연금계좌 세액공제·연금소득 package | (x) | | | | | | | x | x | x |
| R57 | 소득세법 제59조의4 — 보장성보험료 세액공제 | x | x | x | x | x | x | x | | | |
| R58 | 저축성보험 보험차익 — 소득세법 제16조, 영 제25조 | x | | (x) | | | | | (x) | x | x |
| R59 | 상속세 및 증여세법 제8조·제34조 | x | x | (x) | (x) | | | | | (x) | (x) |
| R60 | K-IFRS 제1117호 「보험계약」 | x | x | x | x | x | x | x | x | x | x |
| R61 | 보험개발원 장기손해보험 참조순보험요율 공시 | | | (x) | (x) | x | x | (x) | | | |
| R62 | 손해보험협회 공시실 / e-보험시장 | (x) | | | x | x | x | x | (x) | | |

---

## 1. Prudential and supervisory — 보험업법, 시행령, 감독규정, 감독업무시행세칙

The five instruments in this section are the whole of Korean insurance supervision that `krlib`
touches. Read them in order: the Act says who may write what and what documents a filing
consists of; the Decree closes the product lists and sets the 100% solvency floor; the FSC's
고시 carries every operative reserving, design and surrender rule; the FSS's 세칙 carries the
표준약관 and the crediting-rate formula; and the 별표 to both carry the numbers.

(krlib-reg-r1)=

### R1 — 국가법령정보센터 (법제처), 보험업법 제2조 (정의) and 제4조 (보험업의 허가)

- Version: [시행 2025. 1. 31.] [법률 제20436호, 2024. 9. 20., 타법개정]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes — the whole Act, 127,346 characters of extracted text, through the
  `LSW/lsInfoR.do` body endpoint. The friendly URL `https://www.law.go.kr/법령/보험업법`
  returns only the navigation shell. Cross-checked article by article against the CaseNote
  mirror `https://casenote.kr/법령/보험업법/제4조` and `…/제2조`, which agreed in every
  particular.
- **What it establishes:**
  - **제2조제1호** defines 보험상품 as "위험보장을 목적으로 우연한 사건 발생에 관하여 금전 및
    그 밖의 급여를 지급할 것을 약정하고 대가를 수수(授受)하는 계약" and splits it three ways:
    **가. 생명보험상품** (survival or death of a person); **나. 손해보험상품** — indemnity for
    loss from a fortuitous event, expressly **excluding** "다목에 따른 질병ㆍ상해 및 간병"; and
    **다. 제3보험상품** — "위험보장을 목적으로 사람의 질병ㆍ상해 또는 이에 따른 간병에 관하여"
    a payment. 제2조제5호 then defines 제3보험업 as the business of dealing in them.
  - The carve-out in 나목 is the structural point: Korea does **not** treat sickness, injury
    and nursing care as a sub-species of indemnity insurance, it makes them a third category of
    their own. There is no US, UK, French or German parallel; the closest is Japan's 第三分野,
    which is a licence *scope* rather than a product *class*.
  - **제4조제1항** requires a licence 보험종목별로 and lists them: 제1호 생명보험업 — 가.
    생명보험 나. 연금보험(퇴직보험을 포함한다) 다. 그 밖에 대통령령으로 정하는 보험종목; 제2호
    손해보험업 — 화재, 해상(항공ㆍ운송 포함), 자동차, 보증, 재보험, and Decree additions;
    **제3호 제3보험업 — 가. 상해보험 나. 질병보험 다. 간병보험** 라. Decree additions.
  - **제4조제3항** is the provision that makes 제3보험 a shared field: a person licensed for
    *all* the 생명보험업 종목, or for *all* the 손해보험업 종목 excluding 보증보험 and 재보험,
    "제3보험업에 해당하는 보험종목에 대한 허가를 받은 것으로 본다". Both a life and a non-life
    insurer may therefore write the same 암보험 or 간병보험, and in practice both do.
  - 제4조제6항 restricts licensees to 주식회사, 상호회사 and 외국보험회사, and treats a
    licensed foreign branch as a 보험회사 under the Act.
- **Used by:** every product, for the taxonomy sentence in `product-spec.md`. whole_life,
  term_life, pension_savings, variable_annuity and immediate_annuity are **생명보험상품**;
  indemnity_medical, cancer and long_term_care are **제3보험상품**; ci_insurance and child are
  composites — a 생명보험 주계약 with 제3보험 특약, or the reverse — which 제4조제3항 is what
  makes possible. The market-overview paragraph in `index.md` cites 제4조제3항 for why Korean
  personal protection is written on both sides of the market.

(krlib-reg-r2)=

### R2 — 국가법령정보센터, 보험업법 제5조·제127조·제128조·제128조의2·제128조의3 (기초서류)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (same full-Act retrieval as [R1]; 제5조 additionally cross-checked at
  https://casenote.kr/법령/보험업법/제5조)
- **What it establishes:**
  - **제5조제3호** names the **기초서류** a licence application must attach: "**사업방법서,
    보험약관, 보험료 및 해약환급금의 산출방법서**" — three documents, alongside the 정관 and a
    three-year business plan with projected financial statements. That is what a Korean product
    filing consists of.
  - **제127조제1항**: "보험회사는 취급하려는 보험상품에 관한 기초서류를 작성하여야 한다."
    제127조제2항 makes prior notification to the FSC the **exception**, not the rule — required
    only where a new product is introduced or made compulsory by legislation (제1호) or where
    the Decree so provides for policyholder protection (제3호).
  - **제128조** lets the FSC require FSS verification of a filing and lets it require a
    verification certificate from the 보험요율 산출기관 or an 독립계리업자 on the 보험료 및
    해약환급금 산출방법서. **제128조의2** requires every insurer to maintain a
    **기초서류관리기준** covering drafting procedure, internal and external verification, error
    control and the 선임계리사's role. **제128조의3** sets the drafting principles: no
    illegality, no unjustified reduction of policyholder rights, conformity to FSC standards.
- **What follows for provenance, and it governs the whole library.** The **산출방법서** is
  where the 예정이율, the 예정위험률, the 예정사업비율 and the surrender-value formula actually
  live, and it is **not published**. Only the 약관, the 상품요약서 and the 공시 disclosures
  are. Every pricing-basis parameter in `krlib` is therefore `[std]`, and every contractual
  parameter is sourced from a public 약관 or 상품요약서 with an `[S#]` tag. This is the same
  position `jplib` reaches from 保険業法第4条 and for the same reason.
- **Used by:** every product, in the provenance paragraph of `sources.md` and in the assumption
  tables of `technical-notes.md`.

(krlib-reg-r3)=

### R3 — 국가법령정보센터, 보험업법 제120조 (책임준비금 등의 적립)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** 제120조제1항 — "보험회사는 결산기마다 보험계약의 종류에 따라
  대통령령으로 정하는 **책임준비금**과 **비상위험준비금**을 계상(計上)하고 따로 작성한 장부에
  각각 기재하여야 한다." 제2항 delegates the mechanics to a 총리령; 제3항 lets the FSC set
  accounting standards for their proper recognition. The statute carries **no method and no
  rate**: the whole content sits downstream, in 시행령 제63조 [R8] and 감독규정 제6-11조 [R10],
  and — for the Korea-specific overlay — in 감독규정 제6-11조의6 [R11]. This is the hook on
  which the entire post-2023 reserving chain hangs, and `krlib` cites the chain rather than
  stating a formula of its own.
- **Used by:** every product, in the "what this model does not compute" paragraph of
  `technical-notes.md`.

(krlib-reg-r4)=

### R4 — 국가법령정보센터, 보험업법 제176조 (보험요율 산출기관)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** insurers may, with FSC authorisation, establish a **보험요율
  산출기관** — in fact **보험개발원** (KIDI) — whose statutory tasks under 제176조제3항 are
  "순보험요율의 산출ㆍ검증 및 제공", the collection of insurance information and statistics,
  and research. A rate the bureau files with the FSC is a **참조순보험요율**, and an insurer
  applying it "순보험료에 대하여 제127조제2항 및 제3항에 따른 신고 또는 제출을 한 것으로 본다"
  — deemed to have filed (제176조제6항). 제176조제9항 lets the bureau publish "순보험요율
  산출에 관한 자료" where policyholder protection requires it.
- **What follows:** the deeming provision is why a small Korean insurer can write a full health
  portfolio without its own experience. There is no publication *obligation*, and on the
  **life** side the bureau does not publish: the notifications behind a carrier's 예정
  경험사망률 are identified in its 상품요약서 by document number only [R34]. The 제176조제9항
  permission **is** exercised for **장기손해보험**, where 보험개발원 publishes a numeric
  참조순보험요율 display [R61]. A `krlib` morbidity, incidence or disability rate is
  consequently `[std]` **only where that display does not carry it** — as for 실손 severity
  and for long-term-care inception,
  which are then built from public epidemiology [R40] [R41] [R42] — and is source-tagged to
  [R61] where it does, as for 암 발생률.
- **Used by:** every product, in the morbidity/mortality provenance note. cancer, ci_insurance,
  long_term_care and child lean on it hardest, because for them there is no public rate of any
  kind.

(krlib-reg-r5)=

### R5 — 국가법령정보센터, 보험업법 제181조 (보험계리) and 제184조 (선임계리사의 의무 등)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:**
  - **제181조제1항** requires an insurer to carry out 보험계리 — defined in the article itself
    as "기초서류의 내용 및 배당금 계산 등의 정당성 여부를 확인하는 것" — by employing
    보험계리사 or by outsourcing to a 보험계리업자. **제181조제2항** requires the appointment
    of a **선임계리사**, described since the 2022-12-31 amendment as the actuary who
    "보험계리에 관한 업무 전반을 관리하고 이를 검증 및 확인하는 등 보험계리 관련 업무를
    총괄하는" — a widening from verification to management of the whole actuarial function.
  - **제184조제1항**: "선임계리사는 기초서류의 내용 및 보험계약에 따른 배당금의 계산 등이
    정당한지 여부를 검증하고 확인하여야 한다." 제2항 adds duties to check compliance with the
    기초서류관리기준, to report breaches to the board, and to report any statutory breach in
    the 기초서류 **to the FSC**.
  - **제184조제4항** gives the office tenure: once appointed the 선임계리사 may not be
    dismissed until the end of three consecutive business years following the year of
    appointment, subject to four exceptions (leaking secrets, negligence causing loss, improper
    demands or pressure, an FSC dismissal demand under 제192조).
  - **제184조제7항**, new in 2022, bars the 선임계리사 from three jobs — direct product
    development (verification excepted), CEO and CFO, plus any conflicted role the Decree
    names. This is a hard separation of pricing from sign-off, and it is stricter than the UK
    Actuarial Function / Chief Actuary split.
- **Used by:** every product, as background in `sources.md`; no model implements anything from
  it. Cited in the library index for the sentence about who signs a Korean product off.

(krlib-reg-r6)=

### R6 — 국가법령정보센터, 보험업법 제108조 (특별계정의 설정ㆍ운용)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** the statutory permission for an insurer to set up and operate a
  **특별계정** (separate account) for contract classes the Decree names, keeping their assets
  and results apart from the general account. The operative list, the permitted transfers and
  the 계약자적립금 rule are all in 감독규정 제5-6조, 제5-7조 and 제6-26조 [R15]; the statute is
  the enabling provision only.
- **Used by:** variable_annuity, for which the separate account is the product; and
  pension_savings, because a 연금저축계좌 established under 소득세법 제20조의3제1항제2호 is a
  **mandatory** 특별계정 class under 감독규정 제5-6조제1항제1호 [R15] — the single most
  important structural fact about `Pension_KR_S`.

(krlib-reg-r7)=

### R7 — 국가법령정보센터, 보험업법 시행령 제1조의2 (보험상품)

- Version: [시행 2026. 4. 21.] (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421
- Accessed: 2026-09-03
- Retrieved: yes (153,076 characters)
- **What it establishes:** the Decree closes the three lists the Act opened [R1].
  - **생명보험상품** is 생명보험계약 and 연금보험계약(퇴직보험계약을 포함한다) — **two**
    contract types only (제1조의2제2항).
  - **손해보험상품** is a list of fourteen: 화재, 해상, 자동차, 보증, 재보험, 책임, 기술, 권리,
    도난, 유리, 동물, 원자력, 비용, 날씨 (제3항).
  - **제3보험상품** is exactly three: **상해보험계약, 질병보험계약, 간병보험계약** (제4항).
  - **제1조의2제1항 excludes six public schemes from "보험상품" altogether**: 고용보험,
    **국민건강보험**, 국민연금, **노인장기요양보험**, 산업재해보상보험 and 선불식 할부계약.
- **Why the exclusion matters more than the lists.** Two of the six excluded schemes are
  precisely the public layers that `Medical_KR_S` and `LTC_KR_S` sit on top of. The Decree is
  explicit that the private product is a different animal from the public one — so a `krlib`
  document may describe 실손의료보험 as a reimbursement layer above 국민건강보험 [R53], and
  간병보험 as paying on a 노인장기요양보험 grade [R54], without any suggestion that the two are
  the same instrument.
- **Used by:** every product for the taxonomy; indemnity_medical and long_term_care for the
  public-scheme boundary paragraph.

(krlib-reg-r8)=

### R8 — 국가법령정보센터, 보험업법 시행령 제63조·제65조·제71조

- Version: [시행 2026. 4. 21.] (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제63조제1항, as amended 2022-12-27, restates the reserve in IFRS 17 vocabulary**: 1.
    **보험계약부채**, being the sum of 가. **발생사고요소** ("매 결산기 말 현재 보험계약상
    지급사유가 발생한 보험금등을 지급하기 위해 미래현금흐름에 대한 **현행추정치**를 적용하여
    적립한 금액") and 나. **잔여보장요소** (the same, for benefits whose trigger has not yet
    occurred); 2. **투자계약부채**, for contracts in the legal form of insurance that fall
    outside K-IFRS 1117 and are classified as investment contracts; 3. anything else the FSC
    prescribes on a current-estimate basis. 제63조제4항 keeps **비상위험준비금** for **non-life
    business only**, within 50% of the year's premiums (150% for 보증보험) — so it is not a
    life-side item and `krlib` does not model it.
  - **제65조제1항** defines the three solvency quantities: **지급여력금액** (available
    capital), **지급여력기준금액** (required capital) and **지급여력비율** = the first divided
    by the second. **제65조제2항제1호, as amended 2026-04-21, states the requirement in one
    line: "지급여력비율은 100분의 100 이상을 유지할 것".** 제65조제2항제3호 is the delegation
    under which the 해약환급금준비금 [R11] is required.
  - **제71조제1항** sends 법 제127조제2항제3호 to 별표 6; **제71조제2항** requires the
    보험상품신고서 to be filed **30 days before the sale-start date** (15 days where it follows
    an FSC recommendation), with two attachments — the 기초서류 verified by the **선임계리사**
    under 법 제184조제1항, and, where premiums, surrender values or 위험률 change, a
    verification certificate from the 보험요율 산출기관 or an 독립계리업자.
- **Used by:** every product. The 100% floor is quoted in each `product-spec.md` solvency note;
  the 30-day pre-filing is quoted in `sources.md` to explain why a Korean product's parameters
  become public at launch and not before.

(krlib-reg-r9)=

### R9 — 금융위원회, 보험업감독규정 (금융위원회고시 제2026-16호)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호, 2026. 5. 6., 일부개정]. Comparison
  version also retrieved: [시행 2023. 3. 2.] [금융위원회고시 제2023-10호] (admRulSeq
  2100000220196, 207,084 characters), used only to date 2023–2026 amendments.
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes — 226,083 characters of extracted text, the whole 고시, through the 행정규칙
  body endpoint. **Formulas that the page renders as images did not extract**; each is recorded
  as a gap at the entry that needed it and again in §7.
- **What it establishes (the definitions the rest of this page uses):** 제1-2조 —
  - **제1호 참조순보험요율**: "법 제176조제4항 및 영 제87조제1항에 따라 **보험요율산출기관이
    금융위에 신고한 위험률**".
  - **제2호 기준연령 요건**: "전기납 및 월납 조건으로 **남자가 만 40세**에 보험에 가입하는
    경우", with the mid-point issue age where a 40-year-old male cannot buy the product or the
    product is age-terminating (including 종신보험 and 연금보험), and the longest available
    payment term where whole-term pay is unavailable.
  - **제3호 보장성보험 / 제4호 저축성보험**, distinguished at the 기준연령 요건 by whether the
    maturity value exceeds premiums paid — the same economic test 소득세법 제59조의4 uses
    [R57].
  - **제6호 금리연동형보험** (the 계약자적립액 rate varies with the insurer's investment return
    and market rates) and **제7호 금리확정형보험** (it is fixed).
  - **제13호 평균공시이율**: the average of all insurers' 공시이율, computed as the FSS
    Governor prescribes.
  - **제17호 최적기초율** (best-estimate bases) and **제18호 참조순보험료**: "평균공시이율,
    **평균해지율** 및 참조순보험요율을 적용하여 계산한 순보험료… 참조순보험요율이 없는 경우에는
    제17호의 최적위험률을 보수적으로 할인ㆍ할증한 위험률을 사용한다" (신설 2012-02-28, 개정
    2023-06-27). The 2023 amendment **added 평균해지율 to the inputs** — a direct consequence
    of the lapse-assumption controversy of [R27] [R28].
  - **요구자본** and **충격시나리오방식**, the K-ICS vocabulary of [R13].
- **Drift worth recording** [comparison version]: the filing document is renamed from "보험료
  및 **책임준비금** 산출방법서" to "보험료 및 **해약환급금** 산출방법서" in 제7-69조 and
  제7-70조 between 2023 and 2026 — the visible trace of a regime in which the reserve is no
  longer a locked-in contractual quantity and the surrender value still is.
- **Used by:** every product. 기준연령 요건 is quoted in every `technical-notes.md` to justify
  model point 1; 보장성/저축성 in every `product-spec.md`.

(krlib-reg-r10)=

### R10 — 금융위원회, 보험업감독규정 제6-11조·제6-11조의4·제6-11조의5 (책임준비금, 보증준비금)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; the calculation itself is delegated and not in the 고시)
- **What it establishes:**
  - **제6-11조** splits 책임준비금 into 보험계약부채, 재보험계약부채 and 투자계약부채; 제2항
    splits each of the first two into 잔여보장요소 and 발생사고요소, with the rule that where a
    portfolio's two components sum below zero the balance is presented as a **보험계약자산**.
    제3항 defines 투자계약부채 as the measured value of contracts "보험계약의 법률적 형식을
    취하고 있으나, 한국채택국제회계기준 제1117호의 적용을 받지 않아 투자계약으로 분류된
    계약들". **제4항 delegates the detailed calculation to the FSS Governor** — i.e. to the
    시행세칙 and its 별표 [R23] [R26].
  - **Paragraphs ⑤ to ⑩ of the old 제6-11조 were deleted on 2022-12-21.** That deletion
    is the visible trace of the switch from a locked-in statutory reserve to a current-estimate
    one: before 2023 the 고시 itself carried accumulation rules, after 2023 it carries a
    taxonomy and a delegation.
  - **제6-11조의4** requires a **책임준비금 적정성 검증보고서** within six months of the
    financial-year end, on a form the FSS Governor sets.
  - **제6-11조의5** requires a **보증준비금** inside retained earnings for expected losses on
    benefit guarantees, and 제2항 makes it explicitly junior: "보증준비금은 제6-11조의6에 따른
    **해약환급금준비금을 적립한 후에** 적립하여야 하며, 이익잉여금에서 … 해약환급금준비금을
    차감한 금액을 한도로 한다."
- **Used by:** every product for the reserving-scope note; variable_annuity load-bearing,
  because the ordering in 제6-11조의5제2항 means the surrender-value reserve is taken **first**
  and the guarantee reserve second — which is the opposite of the intuition a drafter brings
  from a market where guarantee reserves are liabilities.

(krlib-reg-r11)=

### R11 — 금융위원회, 보험업감독규정 제6-11조의6 (해약환급금준비금)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제2항 단서 amended 2025-06-11
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text in full)
- **What it establishes.** The Korea-specific layer with no counterpart anywhere else in this
  repository, so it is given at length. **Legal chain**: 보험업법 제120조 [R3] → 시행령
  제65조제2항제3호 [R8] → 감독규정 제6-11조의6 (life) and 제6-18조의6 (non-life).
  - **제1항**: "보험회사는 영 제65조제2항제3호에 따라 보험계약 해지에 대한 위험을 고려하여
    **보험회사 전체단위로** 해약환급금준비금을 산출하여 적립 또는 환입한다" — a
    **company-level** calculation, not a contract-level or portfolio-level one.
  - **제2항 sets the test.** At each balance-sheet date, including quarterly interim closes,
    for in-force contracts, compare **제1호** — 책임준비금 restricted to the 잔여보장요소 of
    보험계약부채 and 재보험계약부채 plus 투자계약부채, net of the 잔여보장요소 of any
    보험계약자산 and 재보험계약자산 and of investment-contract policy loans, **plus**
    특별계정부채 limited to the 계약자적립금 of 제6-26조제1항제1호, grossed up for unrealised
    gains and losses on those contracts recognised in OCI before tax — against **제2호**, the
    **해약환급금 computed under 제7-66조제1항** (on that rule **even for the 제7-66조제4항
    products that may contractually pay less**) **plus** the 미경과보험료 of 제7-66조제5항,
    adjusted for policy-loan balances drawn and amounts to be settled with reinsurers on
    surrender. Where 제1호 < 제2호, the shortfall is appropriated to a **해약환급금준비금
    inside 이익잉여금**.
  - **제2항 단서, amended 2025-06-11**: "다만, 직전 분기말 경과조치 적용 전 지급여력비율이
    **130% 이상**인 경우 제3호의 금액을 적립한다", 제3호 being "그 차액에 **100분의 80**을
    곱하여 산출한 금액". A well-capitalised insurer — measured on the K-ICS ratio **before**
    transitional measures at the previous quarter-end — appropriates only 80% of the shortfall.
    This is a solvency-conditioned distributable-earnings rule and it is new; the 2023 text
    carried no such relief.
  - **제3항**: where the insurer carries an 미처리결손금 the appropriation starts only once
    that deficit is cleared, and any excess over the required balance is released. **제4항**:
    under a 공동재보험계약 cedant and reinsurer each hold the reserve in proportion to the
    ceded share.
  - **Transitional**: the 부칙 to 금융위원회고시 제2022-53호 (2022-12-22, in force 2023-01-01)
    lets insurers that adopted K-IFRS 1117 early compute the reserve for the first year of
    application **for corporate-tax purposes**, with an external audit-firm verification and a
    별지 제26호 「해약환급금준비금 산출명세서」 filed with the FSS and reported to the board.
- **Why it exists, stated plainly.** Under IFRS 17 a profitable in-force block can carry a
  liability materially below the aggregate contractual surrender value, because the CSM is a
  liability that unwinds into profit rather than a cash obligation. Distributing the resulting
  retained earnings would leave the insurer short if policyholders actually surrendered. The
  해약환급금준비금 quarantines the difference. It sits in 이익잉여금 and is therefore
  **inside** K-ICS 가용자본, unlike a genuine liability — a distributable-earnings device, not
  a solvency device. Its scale and the K-ICS-graded accumulation ratio are at [R36]; it stood
  at **₩23.7조 at end-2022 and ₩32.2조 at end-2023**.
- **Used by:** whole_life, pension_savings and variable_annuity load-bearing — in each the gap
  between 계약자적립액 and IFRS 17 liability is the whole point of the earnings profile, and
  the 무·저해지 forms [R19] [R28] make that gap negative in the early years and steeply
  positive after 납입완료, which is exactly the shape the reserve was built to catch. Every
  other product cites it once, in the scope note. **No `krlib` model computes it.**

(krlib-reg-r12)=

### R12 — 금융위원회, 보험업감독규정 제6-11조의7 and 제6-13조 (계약자배당)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제6-11조의7** splits the dividend-related reserves three ways — 계약자배당준비금,
    계약자이익배당준비금 and 배당보험손실보전준비금. The 2026 text subdivides 계약자배당준비금
    into **금리차보장준비금, 총괄배당준비금, 장기유지특별배당준비금** and **재평가특별배당
    준비금**; the 2023 text had a five-way subdivision naming **위험률차배당준비금,
    이자율차배당준비금 and 사업비차배당준비금** separately, since collapsed into
    총괄배당준비금. The Korean three-source vocabulary (위험률차 / 이자율차 / 사업비차 — the
    direct analogue of Japan's 三利源) was therefore **regulatory language until recently and
    is no longer**; it survives in practice and in older filings. `krlib` may use the
    vocabulary and must not attribute it to the current regulation.
  - **제6-13조제1항** is the surplus-sharing rule for life insurers: after setting the
    책임준비금 the residual (계약자배당준비금적립전잉여금) is split into 유배당보험손익,
    무배당보험손익 and 자본계정운용손익; the second and third go wholly to shareholders, and of
    the **유배당보험이익 the shareholder share is capped at 100분의 10**. 제3항 ring-fences the
    policyholder share to dividends and to the 배당보험손실보전준비금. **제6-13조제4항** makes
    a shareholder dividend conditional on the **지급여력비율 being 100% or more at the year
    end**.
  - Interest added to a declared but unpaid dividend must be at least the **prior year's
    평균공시이율** [R48].
- **Market fact carried with it:** Korean retail protection business is overwhelmingly
  **무배당** (non-participating). Every product name in the 표준약관 illustrations [R25] and in
  the carrier disclosures examined carries 무배당; 유배당 survives mainly in legacy annuity
  blocks. **`krlib` models no dividend, and each `product-spec.md` says so and cites this
  entry.**
- **Used by:** every product, one line each.

(krlib-reg-r13)=

### R13 — 금융위원회, 보험업감독규정 제7-1조, 제7-2조, 제7-2조의2 (K-ICS 지급여력)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; **the 기본요구자본 aggregation formula renders as an image and
  did not extract** — see §7)
- **What it establishes:**
  - **제7-2조의2** sets the balance sheet the ratio is computed on — the **건전성감독기준
    재무상태표**, which is (1) based in principle on the K-IFRS consolidated balance sheet and
    (2) measured "경제적이고 시장가격과 일관된 가치로", assets at exit price and liabilities at
    transfer or settlement price, with **no adjustment for the insurer's own credit standing**.
    That last exclusion is the standard economic-value convention and matches Solvency II.
  - **제7-1조** builds 지급여력금액 as 순자산 on that balance sheet plus loss-absorbing
    liability items, less non-loss-absorbing assets, and — 제2항, new in 2022 — classifies the
    total into **기본자본** (tier 1) and **보완자본** (tier 2) by loss-absorbing capacity, with
    제4항 capping 보완자본 at **50% of the 지급여력기준금액**.
  - **제7-2조제1항** builds 지급여력기준금액 as **기본요구자본 − 법인세조정액 + 기타요구자본**,
    where 기본요구자본 aggregates five risk amounts through a correlation formula the FSS
    Governor sets: **생명ㆍ장기손해보험위험액, 일반손해보험위험액, 시장위험액, 신용위험액,
    운영위험액**.
  - **제7-2조제2항 decomposes the life and long-term-health module into seven sub-risks**, each
    with its stated measurement method: 1. **사망위험액** (net asset value falls when mortality
    rises) — 충격시나리오방식; 2. **장수위험액** (falls when mortality *falls*) — shock; 3.
    **장해ㆍ질병위험액** — shock; 4. **장기재물ㆍ기타위험액** — shock; 5. **해지위험액** —
    "보험계약자의 옵션행사율 변화 또는 보험계약 대량해지", shock; 6. **사업비위험액** — shock;
    7. **대재해위험액** (epidemics, mass accidents) — **위험계수방식**.
  - 제7-2조제4항 decomposes 시장위험액 into 금리, 주식, 부동산, 외환 (all shock) plus
    **자산집중위험** (factor); 제5항 and 제6항 make 신용위험액 and 운영위험액 factor-based;
    제7항 permits either the **표준모형** or an approved **내부모형**.
- **Direct relevance to `krlib`:** sub-risks 1, 2, 3, 5 and 6 map one-for-one onto the
  decrements and expense assumptions the ten models carry. A `krlib` sensitivity section should
  name the K-ICS sub-risk its sensitivity corresponds to, because that is the vocabulary a
  Korean actuary uses. **해지위험액** in particular is why the 무·저해지 lapse assumption is a
  supervisory issue and not only an earnings issue — the shock magnitudes are in 시행세칙 별표
  22, which was not retrieved [R26] and is quoted only at second hand from [R36].
- **Used by:** every product, in the sensitivity paragraph of `technical-notes.md`. **No
  `krlib` model computes 요구자본.**

(krlib-reg-r14)=

### R14 — 금융위원회, 보험업감독규정 제7-17조~제7-19조 (적기시정조치) and 고시 제2022-53호 부칙

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 부칙 of 고시 제2022-53호 dated
  2022-12-22, in force 2023-01-01
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제7-17조제1항제1호**: the FSC **must** issue a 경영개선권고 where "지급여력비율이 **50%
    이상 100% 미만**인 경우", or on stated 경영실태평가 grade combinations. 제7-17조제2항's
    measures include capital increase or reduction, expense cuts, branch rationalisation,
    limits on fixed assets, disposal of impaired assets, staff and organisational change, and
    **a restriction on shareholder or policyholder dividends**. 제7-18조 (경영개선요구) and
    제7-19조 (경영개선명령) are the next two rungs.
  - **The commencement 부칙** is where K-IFRS 1117 and K-ICS both start: the 감독규정's IFRS 17
    articles commence **2023-01-01**. The same 부칙 carries the 해약환급금준비금 first-year
    corporate-tax provision [R11] and, at **제4조제1항**, the **five-year 적기시정조치
    deferral** — the FSC may defer 제7-17조제1항제1호, 제7-18조제1항제1호 or 제7-19조제1항제2호
    **until the 2027-12-31 closing** for an insurer whose post-transitional K-ICS ratio at the
    first post-commencement balance-sheet date was below 100%, provided the ratio under the
    **old** regime would not have triggered them, a 경영개선협약 is signed with the FSS
    Governor, and compliance is reported quarterly; 제2항 requires cancellation on breach.
  - The same 부칙 accumulates the transition-date 변액보험 guarantee reserve at the pricing
    interest rate and, for 변액보험, at "매 사업연도별 해당시점의 평균공시이율" [R48].
- **Used by:** every product, in the "both regimes commenced 2023-01-01" sentence;
  variable_annuity additionally for the guarantee-reserve roll-forward rate.

(krlib-reg-r15)=

### R15 — 금융위원회, 보험업감독규정 제5-6조, 제5-7조, 제6-26조 (특별계정)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제5-6조제1항 requires a 특별계정 for six contract classes**: 1. contracts establishing a
    **연금저축계좌** under 소득세법 제20조의3제1항제2호; 2. 근로자퇴직급여 보장법 제29조제2항
    retirement-pension contracts (other than 퇴직연금실적배당보험) and legacy 퇴직보험; 3.
    **변액보험계약 written by a life insurer**, and 퇴직연금실적배당보험; 4. (deleted); 5.
    **장기손해보험 written by a non-life insurer**; 6. **자산연계형보험** other than those
    applying the 공시이율.
  - **제5-6조제3항**: a life insurer's 변액보험 may be run as **two or more 집합투자기구**,
    excluding PEF-type vehicles — the legal form of the fund menu.
  - **제5-6조제5항**: what goes into the separate account is the **적립 보험료** — "영업보험료
    에서 위험보장에 필요한 부분과 사업비 등 기초서류에서 정한 사항을 차감한 금액" — and its
    investment return. This is precisely the `av_pp` recursion `VA_KR_S` implements: gross
    premium, less risk charge, less expense charge, accumulated at the fund return.
  - **제5-6조제6항**: for classes 1 and 5 the applied rate follows the **공시이율** machinery
    of 제7-65조제3항 [R18] — so a **연금저축보험 is a separate-account product whose account
    credits at the 공시이율**.
  - **제5-7조** lists the only permitted transfers between separate and general accounts:
    premium receipt and benefit/dividend/refund payment; transfer to the general account of
    amounts needed for risk cover and for acquisition, maintenance and administration;
    management fees, loans and repayments; bond settlement; **covering a separate-account
    deficit out of the general account's shareholder equity**; and anything else necessary to
    maintain the account.
  - **제6-26조**: the separate-account 계약자적립금 for 변액보험 is the **whole** profit or
    loss arising in that account in the year, appropriated to the contract; for 원리금보장형 it
    is the amount computed under the general account's 산출방법서.
- **Used by:** variable_annuity (the account recursion and the fund menu) and pension_savings
  (the mandatory separate account and the 공시이율 credit).

(krlib-reg-r16)=

### R16 — 금융위원회, 보험업감독규정 제7-60조 (생명보험의 보험상품설계 등)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제10호 신설 2022-12-22, 제3의2호
  신설 2023-06-27
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes** — the design rules a Korean life product must satisfy:
  - **제2호**: for a 저축성보험 the survival benefit must **exceed premiums paid**, except for
    an annuity paying a 생존연금 and for 변액보험.
  - **제3호 and 제4호** — the 평균공시이율 accumulation test: the 계약자적립액 accumulated at
    the 평균공시이율 must exceed premiums paid at 납입완료 (seven years where the payment term
    is seven years or more, fifteen months for single premium); for a whole-life 생존연금 or a
    연금저축보험 the test may be run at **평균공시이율 + 0.25%p**; and 제4호 requires the risk
    premium, guarantee charge and separate-account management fee to be set to **zero** in that
    test.
  - **제3의2호** (신설 2023-06-27) exempts an annuity product whose 계약자적립액 or annuity
    amount at the annuity commencement date, computed at the 평균공시이율, exceeds that of a
    제3호-compliant design, provided the two are compared and explained to the customer.
  - **제7호**: **변액보험 and 금리연동형보험 (other than annuities) must set a
    최저사망보험금**.
  - **제8호**: except where severe injury or disease makes cover impracticable, a contract must
    **not be extinguished** while the risk it covers remains effective. This is the rule behind
    Korean cancer and CI products that continue after a diagnosis payment rather than
    terminating.
  - **제9호**: the **death benefit must be at least cumulative premiums paid**, except after
    annuity payments have begun and except where the premium-paying period ends at age 80 or
    below.
  - **제10호** (신설 2022-12-22): **금리연동형보험 must set a 최저보증이율 or a 최저보증금액.**
    A Korean interest-sensitive product is therefore *required by regulation* to carry a
    guaranteed floor; its level is a company matter and is not published.
- **Used by:** whole_life, term_life, ci_insurance, pension_savings, variable_annuity and
  immediate_annuity load-bearing; child in part. 제8호 is cited by ci_insurance and cancer for
  the continue-after-diagnosis design; 제10호 by whole_life and pension_savings for the
  최저보증이율.

(krlib-reg-r17)=

### R17 — 금융위원회, 보험업감독규정 제7-63조 (제3보험의 보험상품설계 등)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제2항제2의3호 신설 2026-05-06
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text in full; the co-payment amounts below were read from it and
  cross-checked against the 표준약관 [R25])
- **What it establishes:**
  - **제7-63조제1항제1호** — a 제3보험 product must be designed so that, **on death from a
    cause the policy does not cover**, the **계약자적립액** and the 미경과보험료 of
    제7-66조제5항 are paid and the contract terminates. This single rule is why `Cancer_KR_S`,
    `LTC_KR_S`, `Medical_KR_S` and `Child_KR_S` all need an account balance even though they
    are not savings products, and it is a **first-order modelling requirement**: a `krlib`
    제3보험 model must have a defined payment on non-covered death. 제7-61조 applies the whole
    of 제7-63조 to **장기손해보험**, so a non-life insurer's long-term health product is
    designed identically.
  - **제7-63조제2항 is the 실손의료보험 rule set**, and the 2026-05-06 amendment is the fifth
    generation:
    - **제2호 — 기본형 실손의료보험(급여)**. 입원: pay **80% of the 본인부담금** (a 20%
      co-payment), the deducted amount capped at **₩2,000,000 (200만원) a year**, the excess
      reimbursed within the sum insured. 통원, per visit: deduct the greater of **₩20,000
      (2만원)**, 20% of covered cost, or the **건강보험 본인부담률** at a 전문요양기관,
      상급종합병원 or 종합병원; and the greater of **₩10,000 (1만원)**, 20%, or the 건강보험
      본인부담률 elsewhere.
    - **제2의2호 — 실손의료보험 특별약관1 (중증 비급여)**. 입원: deduct **30%**; where the
      deduction on care at a 종합병원 or 상급종합병원 exceeds **₩5,000,000 (500만원) a year**,
      deduct only ₩5,000,000, with 근골격계질환 이학요법료, 체외충격파치료 and 비급여주사제
      excluded from that aggregation and deducted separately. 통원: the greater of **₩30,000
      (3만원)** and **30%**, per visit.
    - **제2의3호 — 실손의료보험 특별약관2 (비중증 비급여)** (신설 2026-05-06). 입원: deduct
      **50%**. 통원: the greater of **₩50,000 (5만원)** and **50%**, per visit. **제1호
      requires 비중증비급여 to be written as a separate 특약**, not inside the base contract.
    - **제3호 — the ±25% corridor**: "실손의료보험에서 **위험구분단위별로 보험료의 변경이 매년
      ±25%를 초과하지 않을 것**", except where the insurer is under, or likely to come under,
      제7-16조~제7-19조 measures. This is a hard bound on the annual re-rating a `Medical_KR_S`
      model may apply.
    - **제3의2호 and 제3의3호** (amended 2026-05-06) — the **비급여 할인·할증**: an insurer may
      apply a **요율 상대도** to the net premium of the 비중증 비급여 특약 on renewal, based on
      claims paid in the twelve months ending three months before the renewal date, with the
      ±25% corridor applying to the **pre-relativity** premium. The five-band table is in the
      표준약관 [R25].
    - **제5호 — 노후실손**: sum insured capped at the combined annual maximum of a normal 실손;
      outpatient per-visit limit **₩1,000,000 (100만원)**; a first-tier deduction of **₩300,000
      (30만원) inpatient / ₩30,000 (3만원) outpatient** before further co-payments of at least
      20% (급여) and at least 30% (비급여), the inpatient deduction capped at **₩5,000,000
      (500만원) a year**.
    - **제6호** — annual verification of the adequacy of the net rate from experience, with
      five years' grace for genuinely new cover (가목); the **benefit-change cycle of five
      years or less** — "보험기간 및 보장내용 **변경주기를 5년 이내**로 할 것" — three years
      for 노후실손 and 유병력자실손 (나목); and a requirement to sell or hold a 노후실손
      product if covering ages 75 and over (다목). 나목 is the **재가입** cycle: a Korean 실손
      contract renews annually at attained-age rates and **re-enters the then-current
      generation every five years**, a contract-boundary structure with no counterpart
      elsewhere in this repository.
    - **제7호 and 제8호** — a mandatory suspend-and-resume facility for policyholders doubly
      covered through a group scheme, and a mandatory conversion facility from group-only cover
      to an individual policy.
- **Used by:** indemnity_medical load-bearing throughout; cancer, long_term_care and child for
  제1항제1호 (the payment on non-covered death); ci_insurance for the 제3보험 design frame.

(krlib-reg-r18)=

### R18 — 금융위원회, 보험업감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; **the two 계약자적립액 accrual formulas of 제7-66조제1항제4호
  are images and did not extract** — recorded at [R19] and in §7)
- **What it establishes:**
  - **제7-64조 — the five 필수기재사항 of the 산출방법서**: 1. the premium calculation, and for
    contracts longer than three years that must use **현금흐름방식** (cash-flow pricing) an
    analysis of premium adequacy based on **최적기초율** with projected cash flows; 2. the
    reserve calculation, including the interest and morbidity/mortality rates used in the
    보험료적립금; 3. the **해약환급금** calculation, including the interest rate, the 위험률,
    the 해약공제액 and — where the 계약체결비용 exceeds the **표준해약공제액** at the 기준연령
    요건 — a comparison of the two; 4. the calculation where benefits or premiums change; 5.
    the calculation of any **보증비용**.
  - **제7-65조제1항**: "계약자적립액은 보험료 및 책임준비금 산출방법서에 따라 계산한 금액으로
    한다"; **제2항** permits it to be computed on an **annualised premium** basis
    ("연납보험료를 기준으로 하여 산출할 수 있다"). That permission is why a Korean
    monthly-premium product can carry an annual-recursion account, and it is directly how
    `Cancer_KR_S`, `Medical_KR_S`, `Child_KR_S`, `LTC_KR_S` and `VA_KR_S` reconcile a monthly
    grid with an annual reserve.
  - **제7-65조제3항 — the 공시이율**: "공시이율은 **공시기준이율**에 **조정률**을 반영하여 다음
    각호의 방법에 따라 결정하여야 한다": 1. 공시기준이율 is computed per the FSS Governor's
    rules as a weighted average of an objective external index rate and the **운용자산이익률**;
    2. **운용자산이익률 = 운용자산수익률 − 투자지출률**, on invested assets excluding
       unrealised gains and losses not passed through profit or loss, with 운용자산수익률 from
       the **preceding twelve months'** investment income excluding insurance finance income
       and the cost from the same period's investment expense excluding insurance finance
       expense; 3. the 공시이율 must be **uniform across a product class** the FSS Governor
       defines [R23], with four exceptions — 유배당 versus 무배당, timing mismatches from
       differing reset cycles, the 농협생명/농협손해보험 legacy 공제계약 versus post-2012-03-02
       products, and setting a rate **below the floor applying to existing contracts**; 4.
       items 1 and 2 must be written into the 기초서류.
- **Used by:** every product. The 연납보험료 permission of 제7-65조제2항 is quoted in the
  monthly-grid models' `technical-notes.md`; the 공시이율 chain is load-bearing for whole_life,
  pension_savings, immediate_annuity and ci_insurance.

(krlib-reg-r19)=

### R19 — 금융위원회, 보험업감독규정 제7-66조·제7-67조·제7-69조·제7-70조 (해약환급금)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제4항제1호 신설 2020-11-19, 제5항
  신설 2022-12-21
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (operative words in full; **the 해약환급금 formula display and the two
  계약자적립액 accrual formulas render as images and did not extract**)
- **What it establishes:**
  - **제1항제1호**: "해약환급금은 **계약자적립액에서 … 해약공제액을 공제하여 계산한 금액 이상**
    으로 산출할 수 있다. 다만, 계약자적립액에서 해약공제액을 공제한 금액이 **음(陰)의 값**인
    경우에는 이를 **영(零)으로** 처리한다." A floor of zero, not a negative value.
  - **제1항제2호**: "제1호에 따른 **해약공제기간**은 보험료 납입기간 또는 신계약비 부가기간으로
    하되, 보험료 납입기간 또는 신계약비 부가기간이 **7년 이상일 때에는 7년으로** 한다."
  - **제1항제3호**: "제1호에 따른 … 해약공제액은 **별표 14에서 정한 표준해약공제액으로** 한다"
    [R20].
  - **제1항제4호**: 계약자적립액 accrues **monthly before 납입완료** ("보험료 납입이 완료되기
    이전에는 … 월별 기간경과에 따라 산출한다") and **daily afterwards** ("일별 기간경과에 따라
    산출한다"). The two formulas themselves are images and did not extract.
  - **제3항**: for contracts on which no 해약공제액 is deducted, benefits may instead be
    differentiated on early surrender.
  - **제4항 — the 무해지 / 저해지 permission.** For a **순수보장성보험** or a whole-life
    생존연금 whose premiums or benefits were calculated using a **최적해지율**, the insurer
    "제1항에서 정한 해약환급금 **미만으로 지급할 수 있다**" — may pay less than the
    별표-14-floored value. That is the legal basis of the form: not a contractual gimmick but a
    **regulatory dispensation conditional on having used a best-estimate lapse rate in
    pricing**. Three exceptions: **제1호 변액보험인 경우** (신설 2020-11-19) — a variable
    product may never use it; **제2호**, where the surrender value during the payment period is
    **less than 50% of an otherwise identical 표준형 상품's**, both of 가. the post-payment
    surrender value **exceeds 50%** of the 표준형's, and 나. the post-payment **환급률**
    (surrender value over cumulative premiums at each point) **exceeds the greater of 100% and
    the 표준형's 환급률**, must hold; 제3호 (deleted).
  - Read carefully, 제2호 is the **환급률 cap**: it permits the deep-discount form only if the
    post-payment refund ratio clears 100% *and* the standard product's ratio. See [R28] for the
    FSC's worked example — a 20-year-pay 종신보험 with a 표준형 20-year 환급률 of **97.3%**
    against a then-current 무해지 환급률 of **134.1%**, the amendment limiting the latter to
    the former.
  - **제5항** (신설 2022-12-21): "보험회사는 보험계약이 해지되는 경우 해약환급금에 **미경과
    보험료 등을 가산한 금액**을 보험계약자에게 지급하여야 한다."
  - **제7-69조** applies the whole of 제7-65조~제7-68조 to **장기손해보험** (including
    연금저축손해보험 and 퇴직보험); **제7-70조** applies it to **제3보험** — "보험요율의 산출과
    보험료 및 해약환급금 산출방법서의 작성 등은 제7-65조, 제7-66조, 제7-67조 및 제7-68조를
    준용한다". **One surrender-value regime governs all ten `krlib` products.**
- **Used by:** every product. whole_life, term_life, ci_insurance, child, cancer and
  long_term_care cite 제4항 for the 무해지/저해지 forms; variable_annuity cites 제4항제1호 for
  why it may **not** use them and must carry a full 별표-14-floored surrender value.

(krlib-reg-r20)=

### R20 — 금융위원회, 보험업감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액

- Version marker on the schedule: <개정 2011.1.24, 2015.5.7., 2020.1.15.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240711 (PDF at
  https://www.law.go.kr/LSW/flDownload.do?flSeq=164927491)
- Accessed: 2026-09-03
- Retrieved: yes — 1-page PDF, text extracted cleanly and in full, including all seven notes
- **What it establishes.** The single most model-relevant page of Korean regulation in this
  library: the statutory cap on the surrender charge, with no US or UK analogue at this level
  of prescription. Reproduced in its operative parts:
  > **표준해약공제액 = 연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000**
  >
  > 주)
  > 1. 장기손해보험에서 연령에 관계없이 단일보험료를 적용하는 상품 및 비용손해담보상품의
  >    경우에는 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납위험보험료의
  >    45%**」로 적용 <개정 2020.1.15.>
  > 2. **해약공제계수**는 다음과 같이 적용함 — 보장성보험: **보험기간(최대 20년)**;
  >    저축성보험: **보험료 납입기간(최대 12년)**, 명칭을 불문하고 납입기간의 범위 내에서
  >    의무적으로 납입해야 하는 별도의 기간을 설정한 경우에는 당해 별도의 납입기간을 보험료
  >    납입기간으로 함, 다만 **일시납보험의 경우 납입기간을 1년**으로 함
  > 3. **연납순보험료 및 연납위험보험료**는 다음과 같이 적용함 — 보장성보험: **전기납(단,
  >    보험기간이 20년 이상인 경우 20년납)**으로 조정하여 산출한 연납순보험료 및 연납위험
  >    보험료, 다만 연납위험보험료 계산시 별표15 제9호 단서의 위험보험료 계산에 관한 규정을
  >    준용한다; 저축성보험: **납입기간(최대 10년)** 동안 동일하게 배분한 평균식 부가보험료를
  >    제외한 연간순보험료 <개정 2020.1.15.>
  > 4. **보험기간이 종신인 생존연금보험(연금저축보험은 제외)**의 경우에는 **연납순보험료의
  >    6%**를 적용하되, 연납순보험료의 5%와 **해약공제계수 12년**을 적용하여 산출한
  >    해약공제액을 초과할 수 없음
  > 5. **연금저축보험**의 경우에는 **연납순보험료의 4%(무배당 연금저축보험은 3%)**를 적용함
  >    <신설 2014.12.31>
  > 6. 보험계약 체결에 사용할 금액을 보험료 납입기간 동안 보험료에 부가하는 저축성보험의
  >    경우에는 보험료에 부가된 금액을 **평균공시이율로 할인**하여 표준해약공제액에서 차감하여
  >    적용함 <신설 2012.2.28, 개정 2014.12.31., 2020.1.15.>
  > 7. **실손의료보험**은 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납위험
  >    보험료의 15%**」로 적용한다 <신설 2015.5.7., 개정 2020.1.15.>
- **Reading it for `krlib`.** The cap is a **level** amount, not a schedule: one 표준해약공제액
  is computed once and deducted from the 계약자적립액 during the 해약공제기간, which is the
  premium-paying period capped at seven years [R19]. Product by product:
  - `Term_KR_S`, `WholeLife_KR_S`, `CI_KR_S`, `Child_KR_S` (protection portion), `Cancer_KR_S`,
    `LTC_KR_S` — 보장성보험. Coefficient = policy term capped at 20; annual net premium
    recomputed on a whole-term-pay basis (20-year pay where the term is 20 years or more); plus
    10/1000 of the sum assured.
  - `Medical_KR_S` — 보장성보험, but **note 7** replaces the sum-assured term with **15% of the
    annual risk premium**. This is the only product-specific override in the schedule, and it
    exists precisely because an indemnity product has no 보험가입금액 in the ordinary sense.
  - `Pension_KR_S` — 연금저축보험: **4% of the annual net premium (3% if 무배당)**, coefficient
    = premium-paying period capped at 12.
  - `Immediate_KR_S` — a whole-life 생존연금 that is not a 연금저축보험: **note 4's 6%**,
    subject to the 5% × 12-year ceiling, with a single-premium contract taking a coefficient of
    **1**. The interaction matters: a single-premium immediate annuity's cap is very small
    relative to premium.
  - `VA_KR_S` — 저축성보험 for the coefficient (payment period capped at 12, annual premium
    computed over a payment period capped at 10), and barred from the sub-cap surrender values
    by 제7-66조제4항제1호 [R19].
- **Used by:** every product, load-bearing, in `technical-notes.md`.

(krlib-reg-r21)=

### R21 — 금융위원회, 보험업감독규정 [별표 15] 보험가입금액의 산정 (제7-67조 관련)

- Version marker: <개정 2011.1.24., 2020.1.15.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240715 (PDF at
  https://www.law.go.kr/LSW/flDownload.do?flSeq=164927503)
- Accessed: 2026-09-03
- Retrieved: yes — 1-page PDF, full text
- **What it establishes.** The 보험가입금액 that enters the 표준해약공제액 formula [R20] is not
  simply "the face amount". The schedule caps it — "다음 각호에서 정한 방법에 의하여 계산된
  금액 **이하**로 하여야 한다" — and the operative items are:
  > 3. **일반사망을 보장하는 보장성보험은 일반사망보험금으로 한다.** <개정 2020.1.15.>
  > 6. 유족연금 등과 같이 보험금이 확정되지 아니하는 보험은 **기준연령 요건**으로 가입하여
  >    중간시점에 사망한 것으로 하여 지급되는 보험기간별 보험금액 중 **최저 보험금액**으로
  >    한다.
  > 8. 제3호는 **체증 또는 체감되기 이전의 금액**으로 한다. <개정 2020.1.15.>
  > 9. 제3호에 해당되지 아니한 경우에는 기준연령 요건에서 다음과 같이 산출한다.
  >    **보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의 보험가입금액**
  >    다만, 정기보험은 해당 보험상품과 동일한 보험기간 기준으로 적용하며, 위험보험료 계산시
  >    다음의 항목은 포함하지 아니한다 — 위험 발생여부와 관계없이 지급하는 보험금을 위한 부분;
  >    특정 위험이 발생하지 않을 경우 지급하는 보험금을 위한 부분; **치매 또는 일상생활장해 등
  >    타인의 간병을 필요로 하는 상태 및 이로 인한 치료 등의 위험 발생시 지급하는 보험금을 위한
  >    부분**.
- **Three things follow.** First, a 제3보험 product with **no death benefit** gets a *notional*
  보험가입금액 by scaling a term policy's face amount by the ratio of risk premiums — which is
  how 별표 14's "보험가입금액의 10/1000" term is given meaning for `Cancer_KR_S` and
  `Child_KR_S`. Second, the third bullet of 제9호 **excludes long-term-care risk premium** from
  that ratio, so `LTC_KR_S`'s notional 보험가입금액 is driven by whatever non-care risk the
  contract carries, not by the care benefit. Third, the whole computation is performed at the
  **기준연령 요건** [R9] — the 40-year-old-male, monthly, whole-term-pay cell.
- **Used by:** cancer, long_term_care, child and ci_insurance load-bearing (it is the only
  route to a 보험가입금액 for a benefit that is not a death benefit); whole_life and term_life
  for 제3호 and 제8호; indemnity_medical for the interaction with 별표 14 note 7.

(krlib-reg-r22)=

### R22 — 금융위원회, 보험업감독규정 제4-32조·제7-45조·제7-51조 (수수료, 공시, 신고)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes** — the expense-and-disclosure ring around the surrender-charge cap:
  - **제4-32조제5항**: for a 보장성보험 other than general non-life and motor, the commission
    and other remuneration paid in the **first year** must not exceed the premium the
    policyholder is expected to pay in that year; and where the contract deducts **80% or more
    of the 표준해약공제액** on surrender, the projected surrender value at the one-year point
    is added to the commission side of that test. **제6항**: if the contract lapses within a
    year, remuneration actually paid (again with the surrender value added in the 80%-plus
    case) must not exceed premiums actually received. **제8항**: where the 표준해약공제액
    exceeds one year's premiums, the insurer must offer distributors an instalment structure
    paying **no more than 60% of the 표준해약공제액 a year** (수수료 분할지급방식).
  - **제7-45조제7항**: a 보장성보험 other than general non-life must publish in its 상품요약서
    a **보험가격지수** — "보험료총액을 참조순보험료 총액과 보험회사 평균사업비총액을 합한
    금액으로 나눈 비율" — and a **보장범위지수**; for **실손의료보험 the 보험가격지수 must be
    explained on each renewal** as well. So a 보장성보험's own pricing is disclosed to the
    buyer only as a *ratio*, never as a rate — which is a different thing from the bureau's
    reference rates being unpublished, and only the life-side ones are [R4] [R61].
  - **제7-45조제11항**: a 보장성보험 whose **계약체결비용 exceeds the 표준해약공제액** must
    disclose a **계약체결비용지수** and a **부가보험료지수** — except that a whole-life
    death-benefit 보장성보험 need not, provided the 계약체결비용 is within **1.4 times** the
    표준해약공제액 (applied to the death-benefit portion only where the product covers both
    death and non-death risks). **That 1.4× tolerance is a useful outer bound for a `[std]`
    acquisition-cost assumption on `WholeLife_KR_S`**: an insurer may load up to 1.4 ×
    표준해약공제액 on a whole-life death product without triggering index disclosure, so a
    reference implementation that sets 계약체결비용 at or below the 표준해약공제액 is
    conservative and defensible.
  - **제7-51조** lists the three cases in which a 산출방법서 must be pre-notified: 1. a
    저축성보험 that does **not** spread at least 50% of the acquisition cost evenly over the
    premium-paying period (40% for a whole-life 생존연금, 70% bancassurance, 100% online), the
    period being at least seven years where the payment term is seven years or more and at
    least fifteen months for single premium; 2. a 보장성보험 that does not spread the
    acquisition cost evenly over the premium-paying period; 3. a renewable or re-entry product
    whose **계약체결비용 on renewal exceeds 70% of the first contract's 계약체결비용**.
- **Used by:** whole_life (the 1.4× bound) and indemnity_medical (the renewal-time 보험가격지수
  and the 70% renewal-cost test, which bites directly on a one-year renewable product) load-
  bearing; every other product cites 제4-32조 in the expense-assumption rationale.

(krlib-reg-r23)=

### R23 — 금융감독원, 보험업감독업무시행세칙 (금융감독원세칙)

- Version: [시행 2026. 9. 10.] [금융감독원세칙, 2026. 8. 28., 일부개정]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2200000108939
- Accessed: 2026-09-03
- Retrieved: yes (114,610 characters)
- **Caveat, and it must travel with every citation of this entry.** The version law.go.kr
  serves as current **takes effect 2026-09-10, one week after the access date**. Facts taken
  from it are facts about the imminent text, not about the text in force on 2026-09-03. Where
  that matters a product document must say so at the point of use.
- **What it establishes:**
  - **제5-13조** — the **표준사업방법서 and 표준약관** are 별표 14 and **별표 15** to the 세칙
    [R25]. Insurers write their own conditions against the 표준약관; it is not a model law to
    be adapted at will, and its clauses appear near-verbatim in every retail Korean policy.
  - **제5-16조제3항** — the **objective external index rates** entering the 공시기준이율 are
    the yields on **국고채(5년), 회사채(무보증 3년, AA-), 통화안정증권(1년)** and
    **양도성예금증서 (91일)**, with substitution allowed if a publisher discontinues one; the
    calculation itself is **별표 27** [R24]; and a newly established insurer, or one with a
    sharp fall in investment return, may use an alternative method notified to the FSS.
  - **제5-16조제4항** fixes the **product classes across which the 공시이율 must be uniform**:
    생명보험 — 보장성보험(순수보장성 및 기타보장성), 보장성보험(**종신보험**),
    생사혼합보험(만기 7년 이하), 생사혼합보험(만기 7년 초과), **연금보험**, 교육보험; 손해보험
    — 보장성보험(만기 15년 이하), 보장성보험(만기 15년 초과), 저축성보험(만기 7년 이하),
    저축성보험(만기 7년 초과), 개인연금보험.
  - **제5-17조의2** and the 부칙 dating the 계리적 가정 amendments were read for chronology.
- **Used by:** every product. The 공시이율 product-class list is load-bearing for whole_life
  (종신보험 is its own class), pension_savings and immediate_annuity (연금보험).

(krlib-reg-r24)=

### R24 — 금융감독원, 보험업감독업무시행세칙 [별표 27] 공시기준이율 산출 기준 (제5-16조 관련)

- Version markers: <신설 2012.9.26, 개정 2013.12.17., 2018.11.6., 2022.12.23., 2025.10.28.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295679 (PDF at
  https://www.law.go.kr/LSW/flDownload.do?flSeq=168885941)
- Accessed: 2026-09-03
- Retrieved: yes — 3-page PDF, full text; **two weight formulas render as images and did not
  extract**, noted below
- **What it establishes**, verbatim in its operative parts:
  > 공시기준이율 = 객관적인 외부지표금리 × α + 운용자산이익률 × (1−α)
  >
  > 객관적 외부지표금리 = 국고채(5년) 수익률 × β1 + 회사채(무보증 3년, AA-) 수익률 × β2
  > + 통화안정증권(1년) 수익률 × β3 + 양도성예금증서(91일) 유통수익률 × β4
  - the four yields are taken as a **three-month weighted moving average ending at the end of
    the month two months before the application date**;
  - **β1…β4** are the shares of the insurer's own prior-year average balances of domestic
    public bonds, corporate bonds, monetary stabilisation bonds and CDs, "직전년도" being the
    twelve months ending three months before the start of the business year; the weights are
    **rounded to 0.5 percentage points, constrained to [0%, 100%]** and held constant through
    the business year;
  - **α** is a function of the opening 계약자적립액, the prior year-end asset duration and the
    prior year's premium income — **the formula itself is an image and did not extract** — and
    is **rounded to 0.5 percentage points**, held constant through the business year, and **may
    not exceed 60%**;
  - the rate is computed **separately by account** (계정별) unless an account is too small;
  - added 2025-10-28: for a reinsurance treaty where the assuming insurer recognises the whole
    investment result on identified assets, those assets and their investment income enter the
    **assuming** insurer's 운용자산이익률, not the ceding insurer's.
- **What this is for.** The 공시기준이율 is the regulated *floor construction* under the
  **공시이율** a Korean interest-sensitive product actually credits [R18]; the insurer then
  applies a 조정률 to reach the 적용이율 it publishes monthly. Because α is capped at 60%, a
  Korean declared rate is **majority-weighted to the insurer's own realised 운용자산이익률**,
  not to market yields — which is why Korean 공시이율 move sluggishly against government bond
  yields and why a `krlib` crediting-rate assumption is modelled as a slow-moving `[std]`
  scalar rather than as a function of a yield curve.
- **Used by:** whole_life, pension_savings, immediate_annuity and ci_insurance load-bearing;
  every other product cites it once for the crediting-rate frame.

(krlib-reg-r25)=

### R25 — 금융감독원, 보험업감독업무시행세칙 [별표 15] 표준약관 (제5-13조제1항 관련)

- Version markers: 생명보험 표준약관 <개정 … 2024.12.20., 2025.3.31., 2025.6.30.>; 실손의료보험
  표준약관 amended **2026.5.6.**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295613 (PDF at
  https://www.law.go.kr/LSW/flDownload.do?flSeq=168885301)
- Accessed: 2026-09-03
- Retrieved: yes — a **492-page PDF**, 441,610 characters extracted. Read in full: the table of
  contents, **Ⅰ. 생명보험** (제1조~제43조 plus 부표), and, of **Ⅱ. 손해보험**, the 실손의료보험
  family — 기본형 실손의료보험(급여), 특별약관1(중증 비급여) and 특별약관2(비중증 비급여). The
  장해분류표 and 재해분류표 appendix tables extracted as running text with some tabular layout
  lost.
- **What it establishes** — the clauses every Korean retail policy carries:
  - **보험나이 (제21조)**, verbatim: "① 이 약관에서의 피보험자의 나이는 **보험나이**를 기준으로
    합니다. 다만, 제19조(계약의 무효) 제2호의 경우에는 실제 **만 나이**를 적용합니다. ② 제1항의
    보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의 끝수는 버리고
    6개월 이상의 끝수는 1년으로** 하여 계산하며, 이후 매년 계약 해당일에 나이가 증가하는 것으로
    합니다." The 약관 prints its own example — 생년월일 1988-10-02, 계약일 2014-04-13,
    difference 25년 6월 11일 ⇒ **26세**. Nearest-birthday age by a six-month rule; it differs
    from 만나이 for half of all issue dates. **Every `krlib` model declares which it uses:
    보험나이 for pricing, 만나이 for statistics**, because the 생명표 [R38] and the NHIS
    statistics [R41] [R42] are on 만나이.
  - **청약철회 (제17조)** — withdrawal within **15 days of receiving the 보험증권** and never
    after **30 days from the application date**; three exclusions (insurer-funded health
    examination, contracts of **90 days or less**, a 전문금융소비자); effective **on
    despatch**; premiums returned **within 3 business days**, late return carrying interest at
    the **보험계약대출이율 compounded annually**. Statutory source: 금융소비자보호법 제46조
    [R51].
  - **품질보증해지 (제18조제3항)** — non-delivery of the 약관 and the application copy, failure
    to explain the important content, or an unsigned application: cancellation **within three
    months of formation** with premiums returned plus 보험계약대출이율 interest. Source: 상법
    제638조의3제2항 [R49].
  - **계약 전 알릴 의무 (제13조, 제14조)** — the 약관 says this "상법상 '고지의무'와 같습니다".
    The insurer may **not** terminate where it knew or was negligent in not knowing at
    formation; **one month** has passed since it learned of the breach, or **two years** from
    the 보장개시일 without a claim event (**one year for disease in a 진단계약**); **three
    years** have passed since the contract date; it accepted on a health-examination document
    and the claim arises from a matter stated in it; or the 보험설계사 prevented truthful
    disclosure. 제14조제4항 carries the causation defence; 제14조제5항 bars termination for
    non-disclosure of **other insurance held**. **사기에 의한 계약 (제15조)** — proxy
    examination, forged certificates or concealment of a pre-application cancer or HIV
    diagnosis: cancellation **within five years of the 보장개시일 and one month of learning of
    the fraud**.
  - **납입최고 and 해지 (제26조)** — a demand period of **at least 14 days** (7 where the
    policy term is under a year), stating that the contract terminates the day after it ends
    and that **policy-loan principal and interest are immediately deducted from the surrender
    value**.
  - **부활 (제27조)** — where the contract terminated under 제26조 and **the surrender value
    has not been drawn** (including where a policy loan consumed it, and including where there
    is none — the 무해지 case), reinstatement may be applied for **within three years**, paying
    arrears with interest at a rate the insurer sets **within 평균공시이율 + 1%**; the insurer
    may **not** refuse because a claim event occurred before termination.
  - **해약환급금 (제32조)** — computed per the 산출방법서, paid **within 3 business days**,
    with interest per 부표 4-1; **the insurer must give the policyholder a table of surrender
    values by elapsed period** (제3항). On termination as a 위법계약 under 제29조의2 the
    **계약자적립액** is returned instead.
  - **보험계약대출 (제33조)** — borrowing within the surrender value on the insurer's terms,
    "그러나 **순수보장성보험 등** 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다";
    unpaid principal and interest deducted from any benefit or surrender value. **A 무해지
    protection product may therefore have no policy loan at all during the payment period** — a
    point `WholeLife_KR_S` and `Term_KR_S` must state, and one the FSS made explicitly in 2019
    [R28].
  - **계약의 소멸 (제22조)** — where death makes further benefits impossible and death is not
    itself an insured event, the insurer pays the "**사망 당시의 계약자적립액**" computed under
    the 산출방법서. This is the 표준약관's implementation of 감독규정 제7-63조제1항제1호 [R17]
    for 제3보험, and the statutory floor beneath it is 상법 제736조 [R50].
  - **보험금의 지급사유 (제3조)** — the five categories a Korean life policy pays on:
    중도보험금, 만기보험금, 사망보험금, **장해보험금** (on the 장해분류표 percentage scale),
    and **입원보험금 등** — "질병이 진단확정되거나 입원, 통원, 요양, 수술 또는 **수발**이
    필요한 상태가 되었을 때". The fifth is where 제3보험 benefits attach, and **수발** is the
    약관's word for the need of care a 간병보험 pays on. The **장해분류표 (부표 3)** defines
    장해 as "상해 또는 질병에 대하여 치유된 후 신체에 남아 있는 **영구적인** 정신 또는 육체의
    훼손상태 및 기능상실 상태", excluding temporary states during treatment: it is the common
    **percentage** scale behind 납입면제 in every Korean protection product, not a binary
    trigger.
  - **소멸시효 (제37조)** and **예금보험에 의한 지급보장 (제43조)** carry the 상법 제662조
    three-year period [R49] and the cross-reference to 예금자보호법 [R52].
  - **실손의료보험 표준약관** (2026-05-06) carries the fifth-generation design whose
    co-payments and limits are set out at [R17]. Additional to those: the 건강보험 본인부담률
    definition — `급여일부본인부담 항목의 본인부담금 ÷ (급여일부본인부담 항목의 본인부담금 +
    급여 공단부담금)`, with 100%-본인부담 items excluded from both ratio and cover; annual
    보험가입금액 up to **₩50,000,000 (5천만원)** for each of 상해급여 and 질병급여 with
    outpatient capped at **₩200,000 (20만원) per visit**; the 비중증 비급여 rider's annual
    ₩50,000,000 limits, its 3대비급여 sub-limit, its per-visit 비급여 cap of **₩3,000,000
    (300만원)** on certain items and its **50% of 비급여 병실료** rule with a daily average
    cap; the limitation of cover to "실제 본인이 부담한 금액 (관련 법령에서 사전 또는 사후
    환급이 가능한 금액은 제외한 금액)", which makes the **본인부담상한제** refund [R53] reduce
    the insured loss; and the **비급여 할인·할증 five-band table** (특별약관2 제6조제3항):
    | 단계 | 1단계 (할인) | 2단계 (유지) | 3단계 (할증) | 4단계 (할증) | 5단계 (할증) |
    |---|---|---|---|---|---|
    | 12-month claims paid | ₩0 (no claim) | >₩0, <₩1,000,000 | ₩1,000,000–<₩1,500,000 | ₩1,500,000–<₩3,000,000 | ≥₩3,000,000 |
    | 요율 상대도 | 할인 (balancing) | 100% | 200% | 300% | 400% |
    The surcharge applies only to contracts with **₩1,000,000 or more** of annual claims, the
    discount is set each year so total premium before and after the relativity is unchanged — a
    pure redistribution — and **장기요양 1등급 and 2등급 under 노인장기요양보험법 are
    excluded** from the claims count [R54], a direct statutory cross-reference between
    `Medical_KR_S` and `LTC_KR_S`.
- **Used by:** every product, load-bearing — the source of every contractual mechanic in
  `krlib` that is not carrier-specific.

(krlib-reg-r26)=

### R26 — 금융감독원, 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금 산출기준)

- URLs tried: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687 and
  https://lbox.kr/v2/statute-admin/보험업감독업무시행세칙
- Accessed: 2026-09-03
- Retrieved: **no**, but for two different reasons that a later drafter needs kept apart.
  **[별표 22] 지급여력금액 및 지급여력기준금액 산출기준 and [별표 22의 1] 내부모형 적용기준
  were located in the 별표 index at `bylSeq` 3295667 and 3295669**, so the three-step route
  that worked for 별표 14, 15 and 27 (`admRulBylContentsInfoR.do?bylSeq=…` →
  `flDownload.do?flSeq=…`) was available — the download was simply never made. **[별표 24]'s
  `bylSeq` was never obtained**; the two routes tried for it, the `admRulLsInfoP.do` 행정규칙
  page and `lbox.kr`, returned a navigation shell and HTTP 403 respectively. 별표 22 is
  therefore a **live task**, and only 별표 24 is a route failure.
- **What it would establish, quoted at second hand and therefore [unverified] here:**
  - **[별표 22]** carries the K-ICS 지급여력 standards, including the **대량해지위험 shock**,
    which [R36] reproduces as: 표준형 — 저축성보험 계약 **35%**, 보장성보험 계약 **25%**
    일시해지; 저해지환급형 고환급형 — 순자산 감소상품 향후 1년 해지율 **+35%p**, 순자산
    증가상품 향후 1년 해지율 **× (1 − 40%)**; 저해지환급형 비고환급형 — **+25%p** / **× (1 −
    40%)**; with 고환급형 defined as "경과기간 시점별 '기납입보험료 대비 해약환급금 비율'이
    '기납입보험료 대비 기납입보험료를 평균공시이율로 부리한 금액의 비율'보다 큰 시점이 존재하는
    상품". Note the direct dependence on the **평균공시이율** series [R48]: the same product
    can be 고환급형 in one issue year and not in another purely because the 평균공시이율 moved.
  - **[별표 24]** carries the **보증준비금 산출기준**: the guarantee reserve is the greater of
    a stochastic **CTE(70)** figure — "사망률, 해지율, 자산이익률(1,000개)을 이용하여 만기까지
    장래 예상되는 순손실액을 현가로 환산한 상위 30% 평균 금액" — and a standard factor
    tabulated by 보험종류 × 최저보증종류 × 보증수준 × 주식비중한도. A search result indicates
    the annex is invoked by 감독규정 제6-11조 제10호 and computed under 시행세칙 제4-15조;
    **neither article was retrieved, so those article numbers are [unverified]**.
- **Used by:** variable_annuity load-bearing (the 보증준비금 basis, which is why the product's
  보증비용 exists at all) with every dependent figure tagged [unverified]; whole_life,
  term_life and the other protection products cite 별표 22 only through [R36], and must say so.

(krlib-reg-r27)=

### R27 — 금융위원회·금융감독원, 제4차 보험개혁회의 보도자료 (계리가정·할인율)

- Publisher: 금융위원회 보험과 / 금융감독원 보험리스크관리국; meeting 2024-11-04, 배포
  2024-11-06, 보도 2024-11-07
- URL: https://www.fsc.go.kr/no010101/83351 (attachments at
  `…/comm/getFile?srvcId=BBSTY1&upperNo=83351&fileTy=ATTACH&fileNo=1` and `…fileNo=4`)
- Accessed: 2026-09-03
- Retrieved: yes — the 6-page 보도자료 PDF and the 6-page 별첨 「보험부채 할인율 현실화 연착륙
  방안」 PDF, both extracted in full. Attachments 2, 3 and 5 are HWP/HWPX and were not
  converted, and **the 별첨 「IFRS17 주요 계리가정 가이드라인」 is among them**. So everything
  below about the lapse models, the convergence points and the disclosure conditions is the
  **보도자료's description of the guideline**, read in full and quoted faithfully, and not the
  guideline's own text. The precise functional form of the log-linear model and the definition
  of the "실무상 수렴점" are therefore **[unverified]** at the level of the instrument, though
  the values are verified from the release.
- **What it establishes.** The most important single supervisory document for `krlib`'s lapse
  assumptions, and the reason the library's protection products can carry a defensible `[std]`
  lapse vector at all.
  - **The problem the FSS named:** with no experience on 무·저해지 business, insurers assumed
    **high lapse right up to 완납**, flattering profitability; the resulting switching out of
    표준형 products raised observed 표준형 lapse, which was fed back into the 무해지 assumption
    — "악순환".
  - **The ruling:** among models converging to zero lapse at 완납 the **로그-선형(log-linear)
    모형** is adopted as the **원칙모형**, with a practical convergence point of **0.1%**.
    Alternatives are permitted only within a closed list — **선형-로그모형** (converging to 0%
    at 완납) and **로그-로그모형** (converging to 0.1%) — and only if the insurer discloses, in
    the audit report and the management disclosure, the reason for the choice, an external
    actuarial verification, and the difference from the principle model in **CSM, best-estimate
    liability, K-ICS ratio (both required and available capital) and net income**, reports the
    difference to the FSS quarterly, and submits to an on-site inspection.
  - **Post-완납 ultimate lapse rate: 0.8%**, from overseas statistics, or alternatively a **20%
    relativity** to the overseas standard-form lapse rate.
  - **단기납 종신보험**: where a short-pay whole-life product (5–7 year pay) carries a bonus
    at, say, year 10 producing a refund ratio of e.g. **135%**, the insurer must assume an
    **additional lapse of at least 30%** at the bonus date, or back it out from the standard
    product's cumulative persistency. The 30% floor is calibrated to the ten-year average of
    the **11th-year lapse rate on single-premium bancassurance savings business, 29.4%–30.2%**
    — the duration at which the tax exemption [R58] is met and the refund ratio jumps.
  - **Loss ratios must be split by age cohort** where experience is sufficient and the split is
    statistically significant. The worked industry example is the 상해수술 cover: **30s 89% →
    40s 103% → 50s 140% → 60s 186%**.
  - **The 무·저해지 share of 보장성 초회보험료**: 2018 **11.4%** → 2021 **30.4%** → 2023
    **47.0%** → 2024 H1 **63.8%**. Nearly two-thirds of new Korean protection business by
    first-year premium is written in a form whose surrender value is nil or suppressed until
    납입완료. **Any Korean reference library that models only 표준형 products is modelling a
    minority of the market.**
  - **The IFRS 17 discount curve**: a risk-free term structure from 국고채 yields, with
    **관찰금리** used directly to the **최종관찰만기 (LOT/LLP), currently 20 years**, then
    interpolation to 60 years and a convergence segment beyond; the convergence point is the
    **장기선도금리 (LTFR)**, "실질이자율 장기평균 + 물가상승 목표", **currently 4.55%**; plus a
    **유동성프리미엄**, being the total risk spread less the credit spread unrelated to the
    contract, **currently 91bp**. The August 2023 phase-in raises the annual LTFR adjustment
    cap from 15bp to **25bp** (2024), realises the loan-yield input to the liquidity premium
    (2024), removes unexpected risk from it (2027), rationalises the 100% adjustment ratio
    (2026) and extends the LOT from **20 to 30 years from 2025** — the last of which the
    November 2024 decision then spread over **three years**.
  - **Government 10-year yields quoted as the reason for the slow-down**: **3.74%** (2022
    year-end) → **3.18%** (2023 year-end) → **3.40%** (2024-03) → **3.26%** (2024-06) →
    **2.99%** (2024-09). At a 10-year yield of 3.0% the industry K-ICS ratio was expected to
    fall about **20 percentage points** from the 2024-06-30 level of **217.3%**.
  - **Application**: from the **2024 year-end closing**, loss-ratio assumptions permitted to
    slip to 2025 Q1 where systems could not be changed in time; the discount-rate soft landing
    applies from **2025-01**.
- **Modelling consequence, in every protection product's technical notes.** The `lapse_rate`
  vector on a 무해지 or 저해지 form is **not free**. A `krlib` reference implementation uses a
  **log-linear decay to 0.1% at 납입완료 and 0.8% thereafter**, tagged `[std]` with this entry
  as its rationale, and carries a switch to the 표준형 assumption so the two can be compared —
  exactly the comparison the guideline requires an insurer to disclose.
- **Used by:** every product, load-bearing — the six protection products for the lapse vector,
  all ten for the discount-curve paragraph.

(krlib-reg-r28)=

### R28 — 금융위원회, 무(저)해지환급금 보험 상품구조 개선 (2020) and FSS 소비자경보 (2019)

- URLs: https://www.fsc.go.kr/no010101/74468 (입법예고, 2020-07-27);
  https://fsc.go.kr/no010101/74613 (확정, 2020-11-18); https://www.fsc.go.kr/no010101/73932
  (금융감독원 소비자경보, 2019-10-23)
- Accessed: 2026-09-03
- Retrieved: yes (all three, server-rendered HTML)
- **What it establishes:**
  - **The definition.** The 입법예고 defines a 무(저)해지환급금 보험 as "보험료 산출 또는
    보험금(연금액) 산출시 **해지율을 사용한 보험**" — an assumption-driven, not a
    contract-driven, class.
  - **The market count at July 2020**: **20 life insurers and 11 non-life insurers** were
    selling the form as a flagship product, against 4 and 3 not selling it. No market-share
    figure was given in the release.
  - **The mis-selling concern**: "저축성보험처럼 환급률만을 강조하며 판매".
  - **The arithmetic that became 감독규정 제7-66조제4항제2호** [R19]: on a 20년납 종신보험
    (1,000만원, 남 40세) the 표준형 20-year 환급률 was **97.3%** against a then-current 무해지
    20-year 환급률 of **134.1%**; the amendment, effective **2020-11-19**, requires the second
    to be designed "전(全) 보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로".
  - **The internal controls**: 시행세칙 제5-19조 was strengthened on lapse-rate derivation,
    verification and profitability sensitivity.
  - **From the 2019 FSS consumer alert**: life insurers began selling the form in **July 2015**
    and non-life insurers in **July 2016**; about **4 million contracts** had been written to
    March 2019; the form is a **보장성보험 and unsuitable as savings**; and — operationally
    important, and repeated in the 표준약관 제33조 [R25] — **a 무해지환급금 contract cannot
    support a policy loan during the payment period**.
- **Used by:** whole_life, term_life, ci_insurance, child, cancer and long_term_care
  load-bearing — the 환급률 cap is what shapes the surrender-value curve every one of them
  publishes, and the no-policy-loan point is a stated product limitation. variable_annuity
  cites it to explain why it is *excluded* from the form.

(krlib-reg-r29)=

### R29 — 금융위원회, 「불합리한 보험 사업비와 모집수수료를 개편하여 …」 (2019-08-01)

- Publisher: 금융위원회
- URL: https://fsc.go.kr/no010101/73816
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML)
- **What it establishes:** the 2019 expense-and-commission reform, and in particular the
  **표준해약공제액 expressed as a multiple of the monthly premium** — **보장성보험 13배,
  저축성보험 3배**; the rule that the savings element of a 보장성보험 must carry 저축성 expense
  and surrender-deduction levels at **70%** of the then-current amount; and the 모집수수료 분급
  rule that the annual commission may not exceed **60% of the 표준해약공제액** with the
  instalment total at least **5%** above the up-front total. Timetable: expense reform to April
  2020, commission reform from January 2021. The 60% figure is the same one that now sits in
  감독규정 제4-32조제8항 [R22].
- **Why the multiples matter.** 별표 14 [R20] states the cap as a formula in 연납순보험료 and
  보험가입금액; this release states the same cap as a **rule of thumb in monthly premiums**,
  which is how Korean practitioners actually carry it. A `krlib` acquisition-cost assumption
  that computes 별표 14 exactly and then sanity-checks it against "13 months' premium for a
  보장성보험" is doing what a Korean pricing actuary does.
- **Used by:** whole_life, term_life, ci_insurance, child, cancer, long_term_care and
  variable_annuity, in the expense-assumption rationale.

(krlib-reg-r30)=

### R30 — 금융위원회, 보험업권 자본규제 고도화 (2025-03-12) and 금융감독원, 지급여력비율 현황

- URLs: https://www.fsc.go.kr/no010101/84128 (FSC, 2025-03-12);
  https://eiec.kdi.re.kr/policy/materialView.do?num=275691 (FSS release of 2026-01-06, mirrored
  by KDI 경제교육·정보센터)
- Accessed: 2026-09-03
- Retrieved: **in part** — the FSC page returned in full; the FSS quarterly returned only the
  headline ratios through the KDI summary page, and the underlying PDF was not downloaded, so
  the component amounts (지급여력금액, 지급여력기준금액) are not available here.
- **What it establishes:**
  - **The size of the capital-regime shift** [FSC]: 요구자본 rose from **₩67.9조 under RBC at
    2022-12-31 to ₩118.9조 under K-ICS at 2024-09-30**; the **기본자본 K-ICS ratio** fell from
    **145.1%** (2023-03) to **132.6%** (2024-09); 2024 capital-securities issuance reached
    **₩8.7조, 272% of the prior year's ₩3.2조**; and the 비상위험준비금 was reformed.
  - **K-ICS ratios after 경과조치 at 2025-09-30** [FSS]: all insurers **210.8%**, 생명보험
    **201.4%**, 손해보험 **224.1%**. The regulatory minimum is **100%** [R8] and 경영개선권고
    begins below it [R14].
- **Used by:** every product, as one line of context in `product-spec.md`. Nothing is modelled
  from it. The quarterly series for 2025-03 and 2025-06 exists at
  `https://eiec.kdi.re.kr/policy/materialView.do?num=267710` and `…num=271247` and was **not**
  opened — recorded so a later drafter has it to hand.

(krlib-reg-r31)=

### R31 — 금융위원회, 실손의료보험 개혁방안 (2025-04-01) and the 5세대 launch (2026-05-06)

- URLs: https://www.fsc.go.kr/no010101/84272 (개혁방안, 2025-04-01);
  https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217561&menuNo=200218
  (금융위원회·금융감독원 joint release, 배포 2026-05-04, 보도 2026-05-06, 15 pp.)
- Accessed: 2026-09-03
- Retrieved: yes — the 2025 개혁방안 page text, and the 2026 launch 보도자료 as a 655 KB,
  15-page PDF (13,903 characters) whose 참고1 comparison table extracted in full
- **What it establishes:**
  - **The 5세대 design before it became regulation** [2025-04-01]: the 급여 co-payment formula,
    the 중증/비중증 비급여 split with their co-payments and limits, the **₩5,000,000 annual
    co-payment cap** on 중증 비급여 inpatient care at tertiary and general hospitals, the
    illustrative premium reductions, the **계약재매입** offer to first- and early-second-
    generation policyholders — about **16 million** of them — and the **2026-07 to 2036-06**
    ten-year conversion window. The FSC's own framing of the 급여 co-payment change is
    "건보정책과의 연계성 강화": the private co-payment now tracks the public one [R53].
  - **The launch** [2026-05-06]: the product in full; the **4세대-versus-5세대 comparison
    table**, which is the only retrieved document stating the complete 4세대 limit and
    sub-limit set in one place; the premium effect — **−30% against 4세대**, **−50% or more
    against 1·2세대**, with base plus 특약1 only at roughly **50% of the 4세대 premium**; the
    선택형 할인 특약 and the 계약전환 할인 (계약재매입) schemes commencing **2026-11** for the
    ~**47.5%** of in-force policies written before 2013-03 with no re-entry clause; a worked
    60-대 여성 premium table across options; and the launch carrier list of **16 companies (7
    생보, 9 손보)**.
- **Used by:** indemnity_medical load-bearing; child and cancer for the generation frame. The
  operative rules themselves are cited to 감독규정 제7-63조 [R17] and the 표준약관 [R25], not
  to the release.

(krlib-reg-r32)=

### R32 — 금융위원회, 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」 (2025-09-01)

- Publisher: 금융위원회; release dated 2025-08-29, published on the commencement date
- URL: https://www.fsc.go.kr/no010101/85200
- Accessed: 2026-09-03
- Retrieved: **in part** — title, dates and the general statement returned; the release as
  summarised does not itemise the insurance-specific buckets
- **What it establishes:** it dates the increase of the deposit-protection limit to
  **₩100,000,000 (1억원)**, in force **2025-09-01**. **The per-bucket mechanics come from
  예금자보호법 시행령 제18조제7항 [R52], which is authoritative and was retrieved in full**;
  this entry is cited only for the date and the public framing.
- **Used by:** pension_savings load-bearing (the 연금저축계좌 bucket is separate from the
  ₩100,000,000 covering the policyholder's other insurance claims); every other product for the
  one-line 예금자보호 sentence that 표준약관 제43조 [R25] requires the 약관 to carry.

---

## 2. Actuarial — 보험개발원, 한국보험계리사회, 경험생명표

Korea has a statutory rate bureau [R4] and an actuarial profession. The bureau publishes
**one** numeric table set — the 장기손해보험 참조순보험요율 [R61] — and publishes **neither**
the 경험생명표 nor any life-side reference rate [R33] [R34]. Several entries below are
therefore about what is *not* available, and the mortality figures that are available are
available at second hand. **No 한국보험계리사회 (Institute of Actuaries of
Korea) practice standard was retrieved in this research pass**, and none is listed here: there
is no `krlib` analogue of `jplib`'s 保険計理人の実務基準 [R22 of `jplib`](#krlib-reg-r22) or `frlib`'s NPA 1
and NPA 2. That absence is recorded as a gap in §7, not papered over with a URL. Where a Korean
actuarial convention is used in this library and cannot be traced to a retrieved standard, the
product document says "market practice" and tags the claim `[unverified]`.

(krlib-reg-r33)=

### R33 — 보험개발원, 제10회 경험생명표 — as reported by 보험매일, 「제10회 경험생명표 개정…」

- Publisher of the underlying table: **보험개발원** (Korea Insurance Development Institute,
  KIDI). Publisher of the retrieved document: **보험매일** (fins.co.kr), a trade newspaper.
- Date: article 2024-01-10, reporting the KIDI release of early January 2024
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03
- Retrieved: yes (article text). **This is a news article, and it is the only retrieved source
  for the 제10회 경험생명표 summary figures.** KIDI's own 보도자료 listing carries no
  경험생명표 item in the range served, and the KIDI 빅데이터 플랫폼 page refused connection
  [R34]. Every figure below is therefore news-sourced and must be tagged as such at the point
  of use.
- **What it establishes:**

  | Statistic | 제10회 (applied 2024-04) | Change vs 제9회 |
  |---|---|---|
  | 평균수명, 남 | **86.3세** | +2.8 years |
  | 평균수명, 여 | **90.7세** | +2.2 years |
  | 65세 기대여명, 남 | **23.7년** | +2.3 years |
  | 65세 기대여명, 여 | **27.1년** | +1.9 years |

  This was the first edition in which female 평균수명 exceeded 90. The table is applied to
  **new business from April 2024**. Uses stated for it: an insurer may use the 경험생명표 where
  its own experience is insufficient; it is used in computing the **보험가격지수** published
  for consumer comparison [R22]; and it serves alongside the 통계청 국민생명표 as a national
  mortality indicator. Directional pricing effect of the revision, as reported: **death
  products (종신보험, 정기보험) cheaper; annuity and health products dearer** — the expected
  sign.
- **The consequence for `krlib`, stated once and cross-referenced everywhere.** Because the
  industry table is not public, **every `mort_table.csv` in `krlib` is a `[std]`
  construction**. The construction anchors on (1) the public 국가데이터처 생명표 [R38], which
  gives qx-equivalent survivorship for the whole population by single year of age and sex; (2)
  the two published 경험생명표 summary statistics above, which bracket the level of *insured*
  mortality against the population; and (3) the gap the pair implies — population 기대수명 at
  birth in 2024 was 남 80.8 / 여 86.6 [R38] against insured 평균수명 남 86.3 / 여 90.7, and
  population 65세 기대여명 was 남 19.5 / 여 23.7 against insured 남 23.7 / 여 27.1, i.e. about
  **4.2 years for males and 3.4 years for females at age 65**. Every row of every `krlib`
  mortality table carries a `provenance` column, and **the library's tables must never be
  presented as the 경험생명표**.
- **Used by:** every product, load-bearing, in the mortality-basis section of
  `technical-notes.md`.

(krlib-reg-r34)=

### R34 — 보험개발원, public channels — 보도자료 listing and 보험정보 빅데이터 플랫폼

- URLs: https://www.kidi.or.kr/user/nd11592.do (보도자료 listing); the 보험정보 빅데이터 플랫폼
  page indexing 경험생명표
- Accessed: 2026-09-03
- Retrieved: **in part** — the 보도자료 listing returned (items 742–746, dated 2026-06-02 to
  2026-08-18, and separately the ten most recent items 2026-01 to 2026-08 in a second pass);
  the 빅데이터 플랫폼 page **refused connection on port 9443**. No archive page was reached.
- **What it establishes — negative evidence, which is why it is numbered.** The visible KIDI
  listing carries **no 경험생명표 item, no 참조순보험요율 item and no 보험통계 item**. Together
  with 감독규정 제1-2조제1호, which defines the 참조순보험요율 as the 위험률 the bureau *files
  with the FSC* rather than as a published table [R9], this establishes that:
  1. the **qx table of the 경험생명표 is not public** — only the summary statistics of [R33]
     are;
  2. **no life-side 참조순보험요율 value reaches the public through this channel** — for
     생명보험 the rates become visible only as the 보험가격지수 ratio [R22]. **This is not a
     statement about the bureau as a whole.** It publishes the **장기손해보험**
     참조순보험요율 as a numeric display on a different page of the same site [R61]; the
     negative evidence here is about the 보도자료 channel, the 경험생명표 and the life side,
     and nothing wider;
  3. consequently **every `krlib` mortality table is `[std]`**, as is every morbidity,
     incidence and disability rate that the [R61] display does **not** carry — each
     constructed from public sources and marked at every point of use. This is the
     sharpest single contrast with `jplib`, where the IAJ's 標準生命表 numeric tables are
     downloadable, and with `delib`, where DAV tables are documented in published
     Fachgrundsätze.
- **Used by:** every product, in the one-paragraph provenance statement that opens each
  `technical-notes.md` assumption section.

(krlib-reg-r35)=

### R35 — 보험연구원, 「K-ICS 경과조치 주요 내용과 시사점」 (KIRI 리포트 이슈 분석), 노건엽

- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI); date 2022-03-07
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=139489
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- **What it establishes** — the complete inventory of K-ICS 경과조치, settled at the 보험 자본
  건전성 선진화 추진단's 9th meeting on 2022-02-24:
  - **Available capital.** Capital securities issued before commencement are recognised for
    **ten years**: pre-existing 신종자본증권 count as 기본자본 within the capital-securities
    limit of **15% of total 요구자본** even where they carry a step-up, the excess reclassified
    to 보완자본; pre-existing 후순위채 count as 보완자본 even beyond the **50% of total
    요구자본** tier-2 limit [R13]. **Reporting** deadlines are extended by one month over the
    normal two (quarterly) and three (annual) for the first **three years**.
  - **Four optional ten-year phase-ins**, each conditional. **(1) 보험부채 증가분** — available
    only where the K-ICS liability exceeds the old-regime liability, the old basis being
    해약환급금 + 계약자배당 관련 준비금 + 보증준비금 − 보험계약대출 잔액 − 재보험자산 중
    미경과보험료 and the K-ICS basis 보험료부채 + 계약자배당 관련 부채 + 위험마진 −
    보험계약대출 − 재보험자산 중 출재보험료부채; the 2023-03-31 in-force book is recognised at
    **10% a year from 2024, reaching 100% in 2033**. **(2) 금리리스크** and **(3) 주식리스크**
    — available only where the RBC risk amount is **60% or less** of the K-ICS risk amount,
    with 60% of the risk recognised in 2023 rising **4 percentage points a year** to 100% from
    2033. **(4) 신규 도입리스크** — the sub-risks RBC did not measure: **장수, 해지, 사업비,
    대재해** [R13].
  - **Re-measurement.** The 보험부채 증가분 transitional is recalculated every two years, or
    whenever the 10-year government-bond yield moves **50bp or more** from the previous
    measurement, restricted to 보증준비금 and the LAT 적립액.
  - **Conditions on users.** Quarterly adequacy-verification reports to the FSS, with an
    additional independent-actuary or rate-bureau verification for the 보험부채 증가분; and a
    **dividend-payout brake** — if the payout ratio exceeds max{50% of the company's own
    five-year average, 50% of the industry's five-year average}, the remaining transitional
    period is **halved**. An insurer wishing to apply had to notify the FSS Governor **within
    two months of 2023-01-01**.
  - **Comparison with Solvency II.** The EU phases the liability increase over 16 years and new
    risks over 4, and defers early intervention by 2 years; Korea uses a uniform 10 years for
    all four and defers intervention by **5** [R14].
  - Two asset-side reliefs touch this library: a long-held-equity shock cut from **35% to 20%**
    for qualifying developed-market listed equity held on average five years with a documented
    ten-year holding plan, and a mandatory-holding-property shock cut from **25% to 20%** where
    the property is held because 노인장기요양법 or 사회복지사업법 obliges the insurer to own it
    — a direct regulatory link between an insurer's long-term-care operations and its capital
    charge.
- **Used by:** every product, background only. It is why a Korean K-ICS ratio quoted "after
  경과조치" [R30] is not comparable with one quoted before, and `krlib` says which is which.

(krlib-reg-r36)=

### R36 — 보험연구원 노건엽·이승주, CEO Report 03호 「보험개혁회의 내용과 과제: 건전성 제도」

- Publisher: 보험연구원, CEO Report 2025년 03호 (2025-04), 24 pp.
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=671389
- Accessed: 2026-09-03
- Retrieved: yes (594 KB PDF, 24 pp., extracted and read)
- **What it establishes:**
  - A restatement of [R27]'s lapse guidance with the exact model names, used here as the
    cross-check that the primary release was read correctly.
  - The **무·저해지 보장성 초회보험료 share** series (2018 / 2021 / 2023), agreeing with [R27].
  - **The K-ICS 대량해지위험 shock table** for 표준형 and 저해지환급형, sourced in the report
    to **보험업감독업무시행세칙 [별표 22]** — which was **not** retrieved [R26], so this report
    is the only route to the numbers and they are `[unverified]` as regulatory text.
  - **The 해약환급금준비금 in numbers**: **₩23.7조 at end-2022** and **₩32.2조 at end-2023**, a
    **₩8.5조 (36%)** rise in one year; and the report's one-line statement of purpose,
    "시가평가된 IFRS17 보험부채가 해약환급금보다 작은 경우 그 부족액을 자본의 이익잉여금 내에
    적립하여 계약자 보호를 위해 사외유출을 방지함" [R11].
  - **The K-ICS-graded accumulation ratio** from the 감독규정 부칙, which is the operative form
    of the 130%/80% rule of 제6-11조의6제2항 단서 [R11] over time:

    | 적립비율 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 |
    |---|---|---|---|---|---|---|
    | 80% 적립 | K-ICS 200% 이상 | 190% 이상 | 180% 이상 | 170% 이상 | 160% 이상 | 150% 이상 |
    | 90% 적립 | 150~200% 미만 | 150~190% 미만 | 150~180% 미만 | 150~170% 미만 | 150~160% 미만 | — |

- **Used by:** whole_life, term_life, ci_insurance and variable_annuity load-bearing; every
  other product for the 해약환급금준비금 context sentence. **Where a `krlib` document quotes a
  별표 22 shock it must name this report as the route and tag the figure [unverified].**

(krlib-reg-r37)=

### R37 — 보험연구원 정원석, 「보험상품 사업비 및 모집수수료 개선」 (2019-04-16)

- Publisher: 보험연구원; 사업비 및 모집수수료 부가체계 공청회, 2019-04-16; 27-slide
  presentation (`KIRI_20190416_144027.pdf`)
- URL: https://www.kiri.or.kr/pdf/전문자료/KIRI_20190416_144027.pdf
- Accessed: 2026-09-03
- Retrieved: yes (938 KB PDF, 27 pp., extracted and read)
- **What it establishes:** the **표준해약공제액 formula set out by product class with a worked
  arithmetic example** — the clearest published exposition of what 별표 14 [R20] actually does;
  the framing of the surrender value as **적립금 less unrecovered 사업비, bounded by the
  표준해약공제액**, which is the sentence a `krlib` technical note should use; and a
  장기보장성보험 surrender-value example table. It is the analytical companion to the FSC
  release [R29] that carried the reform through.
- **Used by:** whole_life, term_life and pension_savings load-bearing, in the derivation of the
  surrender-value curve; every other product for the framing sentence.

(krlib-reg-r61)=

### R61 — 보험개발원, 「장기손해보험 참조순보험요율」 공시 (알림광장 → 참조 순보험요율)

- Publisher: 보험개발원 (KIDI), the statutory 보험요율 산출기관 of 보험업법 제176조 [R4]
- URL: https://www.kidi.or.kr/user/nd13261.do
- Version: the rates on display are those 적용시점 **2024년 4월 1일 이후** (일반상해 from
  2026-01-01)
- Accessed: 2026-09-03
- Retrieved: yes — the page renders as HTML and the rate tables came through as text. **This
  entry corrects the cross-product research pass**, which concluded from the 보도자료 listing
  [R34] that no 참조순보험요율 value is public; the `cancer` and `indemnity_medical` passes
  opened this page on the same day. The correction is recorded at §7-D.
- **What it establishes.** 제176조제9항 lets the bureau publish "순보험요율 산출에 관한 자료"
  where policyholder protection requires it [R4], and for **장기손해보험** it does. The
  published 구성 covers 일반상해 and 교통상해 (사망 / 후유장해 / 입원), 질병 사망률, 후유장해,
  입원율, **암 발생률**, 비용손해, 재물손해 and 배상책임. Two tables reach `krlib` directly:
  - **「기타피부암 및 갑상선암 이외의 암 발생률」**, by age and sex. Its definition is the
    **insured** one — invasive cancer excluding C44 and C73 — so the 유사암 carve-out of
    [R40] is already inside it rather than something the modeller must impose:

    | 연령 | 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 |
    |---|---|---|---|---|---|---|---|---|---|
    | 남자 | 0.000297 | 0.000148 | 0.000230 | 0.000531 | 0.001343 | 0.003567 | 0.008540 | 0.019206 | 0.027892 |
    | 여자 | 0.000318 | 0.000152 | 0.000250 | 0.001005 | 0.003382 | 0.004962 | 0.006239 | 0.008626 | 0.011452 |

    The sex crossover sits at about **age 55–60**: at 40 the female rate is 2.52× the male, at
    60 the male is 1.37× the female, and at 80 the male is 2.44× the female.
  - **질병입원율 (1일 이상, 180일 한도)** on the same age grid, stated as **expected days per
    life-year** rather than as a probability — 남 / 여 0.727696 / 0.934549 at 40, 2.529219 /
    3.276503 at 60, 8.646292 / 10.597399 at 80. That is the natural quantity for a daily
    inpatient benefit and not a rate that may be used as an incidence probability.
- **Read it for what it is.** A 참조순보험요율 is a **net premium rate**, not a 최적기초율 —
  감독규정 제1-2조 keeps the two apart, and 제18호 reaches for a discounted or loaded
  최적위험률 only "참조순보험요율이 없는 경우" [R9]. It therefore carries a safety loading; the
  size of that loading was not retrieved and any figure for it is **[unverified]**.
- **What it does not carry**, and the boundary is as load-bearing as the tables: **실손의료보험
  위험률 is not among the published categories**, and neither is any long-term-care inception
  rate. Those two stay `[std]` constructions built from public epidemiology [R41] [R42].
- **Used by:** cancer load-bearing — it is the anchor for `Cancer_KR_S`'s incidence table, and
  the reason that table is **source-tagged rather than `[std]`**; indemnity_medical for the
  negative result that fixes its calibration boundary. ci_insurance and child did not reach
  this page in their own research passes and should: it carries 암 발생률, 질병입원율 and
  후유장해 on one grid.

---

## 3. Statistics and experience data — public and citable

Everything in this section is public, citable and free of licence obstacles, and everything in
it is on **만나이** (age last birthday) rather than 보험나이 [R25]. That distinction is real —
the six-month rule means the two differ for half of all issue dates — and a `krlib` model that
anchors a `[std]` table on a public statistic must convert or must say it has not.

(krlib-reg-r38)=

### R38 — 국가데이터처, 「2024년 생명표 작성 결과」 and 통계청, 「2023년 생명표」

- Publisher: 국가데이터처 인구동향과 (the renamed 통계청)
- URLs: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156732935 (2024년 결과);
  https://www.korea.kr/briefing/policyBriefingView.do?newsId=156664008 (2023년)
- Accessed: 2026-09-03
- Retrieved: yes (both briefing texts)
- **What it establishes.** Korea's official life tables come in two forms — the **완전생명표**
  (complete, single year of age, from vital registration and the population register) and the
  **간이생명표** (abridged) — published annually with a two-year lag.

  | | 전체 | 남자 | 여자 |
  |---|---|---|---|
  | 기대수명 at birth, 2024 | **83.7년** | **80.8년** | **86.6년** |
  | change on 2023 | +0.2 | +0.2 | +0.2 |
  | 40세 기대여명, 2024 | — | 41.9년 | 47.4년 |
  | 65세 기대여명, 2024 | — | **19.5년** | **23.7년** |
  | survival to age 80, 2024 | — | 64.4% | 82.2% |

  Korea's 기대수명 exceeds the OECD average by 2.3 years (male) and 2.9 years (female), ranking
  11th and 3rd. The 2023 table gives 기대수명 전체 83.5년, 남 80.6년, 여 86.4년 (+0.8, +0.7,
  +0.8 on the COVID-affected 2022 fall of 0.9); 65세 기대여명 남 19.2년 / 여 23.6년; sex gap
  5.9 years. The definition the release gives is the standard period-table one: "연령별 사망
  수준이 그대로 유지될 경우 향후 몇 세까지 생존할 수 있는지를 추정한 결과".
- **Licensing:** 국가데이터처 statistics are public-sector open data.
- **Used by:** every product with a mortality decrement, load-bearing — this is the **public
  anchor** for every `[std]` `mort_table.csv` in the library [R33]. long_term_care and
  immediate_annuity additionally use the 65세 기대여명 figures as the longevity anchor;
  pension_savings uses them because 소득세법 시행령 제25조제4항 makes the **국가데이터처
  기대여명 연수** the statutory cap on a guarantee period in a tax-exempt 종신형 연금보험
  [R58].

(krlib-reg-r39)=

### R39 — 국가데이터처, KOSIS 국가통계포털 — 완전생명표 (single-year qx tables)

- Publisher: 국가데이터처 / 통계청
- URL: https://kosis.kr/
- Accessed: 2026-09-03
- Retrieved: **no** — the single-year 완전생명표 qx tables are distributed through KOSIS and
  **were not downloaded in this session**. Only the summary briefings [R38] were read.
- **Consequence, and it is a live task rather than a closed gap.** `krlib`'s mortality-table
  build must fetch the 완전생명표 separately and **record the KOSIS table id in each product's
  `sources.md`**. Until it does, any single-year qx quoted in a `krlib` document is `[std]`
  interpolation from [R38]'s summary statistics and must say so. No qx value is asserted on
  this page.
- **Used by:** every product with a mortality decrement, as the named to-do in the table-build
  note of `model.md`.

(krlib-reg-r40)=

### R40 — 보건복지부·중앙암등록본부(국립암센터), 「2023년 국가암등록통계 참고자료」

- Publisher: 중앙암등록본부 / 국가암정보센터; date on the document **2026-01-20**
- URL: https://www.cancer.go.kr/download.do?uuid=cfcd35c3-391f-4060-9688-641db3d86cbd.pdf
- Accessed: 2026-09-03
- Retrieved: yes (41-page PDF, extracted in full and read)
- **What it establishes** — everything a Korean cancer or CI product needs that is public:
  - **Incidence 2023**: **288,613** new cancers (남 151,126, 여 137,487); 조발생률 **564.3**
    per 100,000 (남 593.4, 여 535.5); **연령표준화발생률 522.9** (남 587.0, 여 488.9),
    standardised on the 2020 주민등록연앙인구. Excluding thyroid: 253,173 cases, 표준화발생률
    454.0.
  - **Series** (발생자수 / 연령표준화발생률): 1999 101,854 / 402.7; 2010 222,664 / 565.1; 2019
    258,629 / 518.0; 2020 251,329 / 489.5; 2021 280,042 / 531.4; 2022 281,317 / 521.3; **2023
    288,613 / 522.9**.
  - **Top ten, both sexes, 2023** (cases / share / 표준화발생률): 갑상선 35,440 / 12.3% / 68.9;
    폐 32,953 / 11.4% / 57.5; 대장 32,610 / 11.3% / 58.7; 유방 29,871 / 10.3% / 56.8; 위 28,943
    / 10.0% / 51.4; 전립선 22,640 / 7.8% / 39.2; 간 14,707 / 5.1% / 26.1; 췌장 9,748 / 3.4% /
    17.1; 담낭 및 기타담도 7,997 / 2.8% / 13.8; 신장 7,367 / 2.6% / 13.5.
  - **Lifetime risk of developing cancer, 2023**: all cancers **41.2%** overall — **남 44.6%,
    여 38.2%**; lifetime risk of dying of cancer 19.6% (남 24.2%, 여 15.6%).
  - **Five-year relative survival, 2019–2023 diagnoses**: all cancers **73.7%** (남 68.2, 여
    79.4); excluding thyroid 69.6%. By site: **갑상선 100.2%**, 전립선 96.9%, 유방 94.7%, 위
    78.6%, 대장 75.6%, 폐 42.5%, 간 40.4%, 담낭 및 기타담도 29.0%, 췌장 17.0%, 신장 87.9%. The
    1993–95 comparison for all cancers was 42.9%.
  - **Prevalence at 2024-01-01**: **2,732,906** persons diagnosed 1999–2023 and alive — **5.3%
    of the population**; 조유병률 5,343.4 per 100,000.
- **Why 갑상선암 matters to `krlib`.** Thyroid cancer is the single most common cancer in Korea
  (12.3% of all cases; 19.0% of female cases) and has a five-year relative survival of
  **100.2%** — statistically indistinguishable from the general population. Korean cancer
  policies therefore place it, with carcinoma in situ and certain skin and borderline tumours,
  in a reduced **유사암** tier paying a small fraction of the 진단급여금. **Any `Cancer_KR_S`
  incidence table that does not separate 갑상선 from the rest will misprice the product by a
  wide margin.** The registry gives the split; the tier definition comes from each carrier's
  약관 and belongs in the product folder as `[S#]`.
- **Used by:** cancer and ci_insurance load-bearing; child for the 소아암 framing;
  indemnity_medical for the 암 치료 share of claims [R44].

(krlib-reg-r41)=

### R41 — 국민건강보험공단, 「2024년도 건강보험환자 진료비 실태조사」

- Publisher: 국민건강보험공단; date 2025-12-30. Retrieved through the 보험연구원 weekly-trend
  reprint of the NHIS 보도자료.
- URL: https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- **What it establishes** — the public-scheme underlay that 실손의료보험 sits on:

  | | 2023 | 2024 |
  |---|---|---|
  | 건강보험 보장률 | 64.9% | **64.9%** |
  | 법정 본인부담률 | 19.9% | **19.3%** (−0.6%p) |
  | 비급여 본인부담률 | 15.2% | **15.8%** (+0.6%p) |

  with 보장률 defined as 보험자부담금 ÷ (보험자부담금 + 법정본인부담금 + 비급여진료비),
  excluding cosmetic, health-promotion and preventive 비급여. **Total treatment cost 2024 was
  ₩138.6조** — **₩90.0조 보험자부담금, ₩26.8조 법정본인부담금, ₩21.8조 비급여진료비** — on a
  series (조 원) of 83.7 (2017), 103.3 (2019), 111.1 (2021), 120.6 (2022), 133.0 (2023),
  **138.6 (2024)**. 보장률 by institution class 2024: 상급종합 **72.2%**, 종합병원 **66.7%**,
  병원 **51.1%**, 요양병원 **67.3%**, 의원 **57.5%**, 약국 **69.1%**; by age, 5세 이하
  **70.4%**, 65세 이상 **69.8%**; 4대 중증질환 **81.0%**.
- **The cross-check worth making, computed here from two retrieved primary sources.** Private
  실손 claims of **₩15.2조** in 2024 [R44] against NHIS-measured 비급여 of **₩21.8조** and
  법정본인부담금 of **₩26.8조** — i.e. private indemnity insurance reimburses roughly **31%**
  of the combined ₩48.6조 the patient nominally bears. That ratio is the cleanest one-line
  justification for calling 실손 "the second national health insurance".
- **Used by:** indemnity_medical load-bearing (the claim-severity anchor and the 보장률 by
  institution class that the co-payment table keys off); cancer, child and long_term_care for
  context.

(krlib-reg-r42)=

### R42 — 국민건강보험공단, 「장기요양 등급 판정 현황」 (자율공시 / 경영공시)

- Publisher: 국민건강보험공단; as-of date on the retrieved table **2026-06-30 (2026년
  2/4분기)**
- URL: https://www.nhis.or.kr/announce/wbhaec11503m01.do
- Accessed: 2026-09-03
- Retrieved: yes (table)
- **What it establishes** — the grade distribution `LTC_KR_S`'s incidence basis must reproduce
  in aggregate:

  | | Persons | Share of all assessed |
  |---|---|---|
  | 총 등급판정 | 1,411,466 | 100% |
  | **인정자** | **1,275,370** | **90.4%** |
  | 등급외자 | 136,096 | 9.6% |
  | 1등급 | 53,844 | 3.8% |
  | 2등급 | 100,844 | 7.1% |
  | 3등급 | 333,143 | 23.6% |
  | 4등급 | 604,307 | 42.8% |
  | 5등급 | 151,681 | 10.7% |
  | 인지지원등급 | 31,551 | 2.2% |

  The shares are of **all assessed**, not of recognised claimants; on the recognised base the
  4등급 share is about 47%.
- **The modelling consequence, and it is a hard one.** The grade *stock* is public; the
  **incidence** is not. An LTC inception basis must therefore be constructed `[std]` from the
  stock and the population, and the construction must be shown row by row in `model.md`. The
  benefit trigger is a *public administrative determination*, not a policy definition [R54]
  [R55], so the model's inception rate is the rate of being recognised at or above a stated
  등급 — the natural policy designs being "1–2등급" (severe) and "1–5등급" (broad).
- **Used by:** long_term_care load-bearing; indemnity_medical for the 할인·할증 exclusion of
  1등급 and 2등급 [R25].

(krlib-reg-r43)=

### R43 — 국민건강보험공단, 「2024 노인장기요양보험 통계연보」, as reported by 메디칼월드뉴스

- Publisher of the underlying yearbook: 국민건강보험공단. Publisher of the item: 메디칼월드뉴스
  (medicalworldnews.co.kr).
- URL: https://www.medicalworldnews.co.kr/m/view.php?idx=1510968457
- Accessed: 2026-09-03
- Retrieved: **no** — returned only as a search-result summary; the article page itself was not
  opened, and the yearbook was not obtained
- **What it would establish, and every figure here is [unverified]:** 2024 인정자 **1,165천명**
  (+6.1%), 신청자 **1,478천명** (+3.4%), 판정 대비 인정률 **89.5%** (+0.9%p), the grade split
  (4등급 46.0%, 3등급 26.7%, 5등급 11.6%, 2등급 8.5%, 1등급 4.8%, 인지지원 2.4%), 급여비용
  **₩16조1,762억** (+11.6%) with a 공단부담률 of **91.3%**.
- **Why it is listed at all:** the grade *distribution* it reports is independently
  corroborated by [R42], which **was** retrieved, and the agreement is close. That
  corroboration is the only reason these figures are recorded; none of them may be used as a
  load-bearing input.
- **Used by:** long_term_care, in a sensitivity only, every figure tagged [unverified].

(krlib-reg-r44)=

### R44 — 금융감독원, 「2024년 실손의료보험 사업실적(잠정)」

- Publisher: 금융감독원 보험계리상품감독국 보험상품제도팀; 보도 2025-05-13, 배포 2025-05-12
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=266435 (PDF via
  https://eiec.kdi.re.kr/policy/callDownload.do?num=266435&filenum=1)
- Accessed: 2026-09-03
- Retrieved: yes (7-page PDF, full text), through the KDI 경제교육·정보센터 mirror
- **What it establishes** — the definitive quantitative picture of 실손의료보험, and the FSS's
  own description of it as "**제2의 건강보험 역할**", dated from 1999:
  - **Generations and co-payment rates**: 1세대 (to 2009-09) 손보 0% / 생보 20%; 2세대
    (2009-10–2017-03) 표준형 20%, 선택형Ⅰ 10%, 선택형Ⅱ 급여 10% / 비급여 20%; 3세대
    (2017-04–2021-06) 급여 10% or 20%, 비급여 특약 30%; 4세대 (2021-07–) 주계약(급여) 20%,
    특약(비급여) 30%. Renewal cycles: 1세대 1–5 years, 2세대 3 years then 1 year, **3세대 and
    4세대 1 year**.
  - **Contracts in force, individual business, 만건**: total 3,565 (2022) → 3,579 → **3,596**
    (2024); 생보사 598, 손보사 2,998 in 2024. By generation: 1세대 731 → 682 → **638**; 2세대
    1,705 → 1,623 → **1,552**; 3세대 852 → 826 → **804**; 4세대 208 → 376 → **525** (+39.6%);
    plus **77만건 (2.1%)** 유병력자실손 and 노후실손. So **35.96 million** individual contracts
    against a population near 51 million, and **43.2%** still second-generation, sold before
    2017.
  - **Premium income (억원)**: 131,885 → 144,429 → **163,364** (+13.1%). **Underwriting result
    (억원)**: −15,301 → −19,747 → **−16,226**.
  - **경과손해율**: total 101.3% / 103.4% / **99.3%**; 1세대 113.2 / 110.5 / **97.7**; 2세대
    93.2 / 92.7 / **92.5**; 3세대 118.7 / 137.2 / **128.5**; 4세대 91.5 / 113.8 / **111.9**.
    3세대 first repriced in 2023 and 4세대 first in 2025.
  - **Monthly premium, male aged 40, all covers, non-life basis (만원)**, 2021→2024: 2세대 3.0
    / 3.5 / 3.8 / **4.0**; 3세대 1.6 / 1.7 / 2.0 / **2.4**; 4세대 1.5 / 1.5 / 1.5 / **1.5**. A
    4세대 policy at ₩15,000 a month against a 2세대 policy at ₩40,000 for the same insured is a
    **2.7× spread** — the whole economics of the 계약재매입 offer [R31].
  - **Claims paid (억원)**: 128,868 → 140,813 → **152,234**; **급여 63,306**, **비급여
    88,927**. Three largest treatment groups: **비급여 주사제 28,092억원 (18.5% of all
    claims)**, **근골격계 물리치료 26,321억원 (17.3%)**, **암 치료 15,887억원 (10.4%)**. By
    institution class, claims paid split 의원 32.2%, 병원 23.3%, 종합병원 17.3%, 상급종합병원
    14.0% — against NHIS 2023 treatment-cost shares of 의원 28.1%, 상급종합 22.9%, 종합병원
    20.9%, 병원 10.4%.
  - **Average 비급여 claim per contract per year (만원)**: 1세대 36.1 → 36.3 → **40.0**; 2세대
    21.9 → 23.1 → **25.4**; 3세대 13.1 → 16.4 → **18.2**; 4세대 7.4 → 10.9 → **13.6**. 1세대
    runs at **two to three times** 3세대 and 4세대 — a clean demonstration that the co-payment
    structure, not the insured population, drives the claim.
- **Used by:** indemnity_medical load-bearing throughout; cancer, child and long_term_care for
  the claims-mix context.

(krlib-reg-r45)=

### R45 — 생명보험협회, 공시실 (pub.insure.or.kr), FACT BOOK and 금융통계월보(생명보험편)

- Publisher: 생명보험협회 (Korea Life Insurance Association, KLIA), with 보험개발원 preparing
  tables 5–9 of the monthly series
- URLs: https://pub.insure.or.kr/ ; https://www.klia.or.kr/consumer/stats/factbook/list.do ;
  https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do
- Accessed: 2026-09-03
- Retrieved: **in part** — the 공시실 landing page and category description returned in full;
  the FACT BOOK edition list and contents description returned but **the 2025 edition PDF was
  not downloaded**; the 금융통계월보 structure and provenance returned but **the monthly tables
  sit behind a query form and were not retrieved**
- **What it establishes:**
  - **The 공시실 is the best single source of quantitative Korean product data, and it is
    public.** It carries 상품비교공시 across eleven protection classes plus savings, variable,
    retirement and 실손; 경영공시; and 기타공시 (민원, 불완전판매비율, 소송). It is the public
    route to 약관, 상품요약서 and 해약환급금 illustrations, and **it is a large part of the
    reason `krlib`'s product research files can cite real Korean product parameters at all**.
    It is not the whole reason and must not be cited as though it were: it covers **life
    insurers only**, and the `[S#]` sources of the four 제3보험 products came as often through
    the 손해보험협회 portal [R62] or a carrier's own 공시실.
  - **FACT BOOK** editions run 2001–2025; the 2025 edition covers FY2024 with contract,
    financial, reserve, asset, distribution and **생명표** sections. Recorded as the standard
    annual reference; **no number on this page is taken from it**.
  - **금융통계월보(생명보험편)** is a 통계청 국가승인통계 built from insurers' 업무보고서, with
    보유계약, the 보장성/저축성 split, 지급유형별 보험금·환급금·배당금, 경과기간별 보험료수익
    and 부문별 손익, the last prepared by KIDI.
- **Used by:** every product, as the stated route to its `[S#]` sources; the library index for
  the disclosure-architecture paragraph.

(krlib-reg-r46)=

### R46 — 보험연구원, 「2026년 보험산업 전망」 (2026년 보험산업 전망과 과제 세미나), 황인창

- Publisher: 보험연구원 금융시장분석실; date 2025-10-21; 91-slide presentation
- URL: http://www.kiri.or.kr/report/downloadFile.do?docId=778039
- Accessed: 2026-09-03
- Retrieved: yes (91-page PDF, extracted in full)
- **What it establishes** — the market-size tables behind the library index's market
  paragraphs:

  | 생명보험 (조원, %) | 2023 | 2024 | 2025(E) | 2026(E) |
  |---|---|---|---|---|
  | 전체 | 112.4 (−15.3) | 113.4 (+0.9) | 124.0 (+9.3) | **125.3 (+1.0)** |
  | 보장성보험 | 48.6 (+3.2) | 55.0 (+13.1) | 61.5 (+11.8) | **66.2 (+7.6)** |
  | 저축성보험 | 28.1 (−38.0) | 28.8 (+2.7) | 27.4 (−4.9) | **26.1 (−4.8)** |
  | 변액보험 | 12.2 (−4.0) | 12.3 (+0.4) | 12.7 (+3.3) | **12.4 (−2.3)** |
  | 퇴직연금 | 23.5 (−14.7) | 17.3 (−26.2) | 22.4 (+29.1) | **20.6 (−7.8)** |

  | 손해보험 (조원, %) | 2023 | 2024 | 2025(E) | 2026(E) |
  |---|---|---|---|---|
  | 전체 | 125.2 (+4.2) | 127.6 (+1.9) | 135.0 (+5.8) | **139.6 (+3.5)** |
  | 장기손해보험 | 64.3 (+4.0) | 68.0 (+5.8) | 72.3 (+6.3) | **75.9 (+4.9)** |
  | 개인연금 | 1.9 (−10.7) | 1.7 (−13.0) | 1.4 (−15.5) | **1.2 (−15.0)** |
  | 자동차보험 | 21.1 (+1.4) | 20.7 (−1.8) | 20.3 (−2.0) | **20.3 (−0.2)** |
  | 일반손해보험 | 13.9 (+8.6) | 14.9 (+7.4) | 15.6 (+4.9) | **16.5 (+5.9)** |
  | 퇴직연금 | 24.0 (+6.6) | 22.3 (−7.2) | 25.3 (+13.5) | **25.7 (+1.7)** |

  The report's own summary is that industry premium growth falls to about **2.3% in 2026** from
  7.4% in 2025, and that "성장성 둔화, 수익성 약화, 건전성 악화" is the sequence from 2024
  through 2026. On the 2026 forecast **보장성 is 52.8% of life premium against 저축성 at
  20.8%**, and non-life 개인연금 is in outright run-off at −15% a year. **The Korean life
  market is a protection market with a shrinking savings tail — the opposite of the French and
  German mixes in `frlib` and `delib`.**
- **[unverified] within this entry:** the CSM forecasts sometimes attributed to the same
  seminar — 생명보험 CSM ₩64.7조 (2025E) → ₩64.3조 (2026E), 손해보험 ₩70.3조 → ₩71.8조 — were
  read from a **search summary**, not from the retrieved deck, whose CSM slide did not extract
  cleanly.
- **Used by:** every product, for the one-paragraph market context in `product-spec.md`, and
  the library index.

(krlib-reg-r47)=

### R47 — 한국보험신문, 「2025년 보험사 당기순이익 12.2조원… 생·손보 보험손익 동반 하락」

- Publisher: 한국보험신문 (insnews.co.kr); the figures are attributed in the article to
  금융감독원's 2025년 보험회사 경영실적; date 2026-03-30
- URL: https://www.insnews.co.kr/news/articleView.html?idxno=89914
- Accessed: 2026-09-03
- Retrieved: yes (article text). **This is a news article standing in for an FSS release that
  the cross-product research pass could not open** — see the correction in §7. Every figure
  from it is news-sourced and must be tagged as such.
- **What it establishes:** 2025 outturn — 수입보험료 **₩266.6595조**, +11.1% (생보 ₩127.5061조
  +12.4%, 손보 ₩139.1533조 +10.0%); 당기순이익 **₩12.2172조**, −14.5% (생보 ₩4.9680조, 손보
  ₩7.2492조); ROA 0.94%, ROE 7.86%; 총자산 **₩1,344.2조**, 부채 ₩1,175.6조, 자본 ₩168.5조. Life
  mix (조원): 보장성 **62.0192** (+12.7%), 저축성 27.4763 (−4.6%), 퇴직연금 및 기타 25.3979
  (+46.4%), 변액 12.6128 (+2.8%). Non-life mix: **장기보험 73.3402** (+7.0%), 퇴직연금 및 기타
  29.7187, 자동차 20.3681, 일반 15.7264. The FSS attributed the profit fall to "손실계약 증가,
  예실차 손실 등 보험손익 악화".
- **The structural fact those two mixes carry.** Korean *personal protection* insurance is
  written on **both** sides of the market — 생명보험 보장성보험 at ₩62.0조 and 손해보험
  장기보험 at ₩73.3조 — and **the non-life figure is the larger**. 장기손해보험 is
  overwhelmingly 장기인보험 (health, cancer, care, accident), written under the 제3보험 deeming
  provision of 보험업법 제4조제3항 [R1] and reserved under the same rules by 감독규정 제7-69조
  [R19]. A Korea library that looked only at life insurers would miss more than half of the
  protection market. **`krlib` models the life-insurer form throughout, and each product
  document says where a non-life carrier's version differs.**
- **Used by:** every product, in the market paragraph; the library index, load-bearing.

(krlib-reg-r48)=

### R48 — 평균공시이율 and 공시기준이율 — carrier regulatory disclosure (하나생명, 교보생명)

- Publishers: 하나생명보험주식회사, 「적용이율 공시 — 표준이율 및 평균공시이율」;
  교보생명보험주식회사, 「공시기준이율 적용현황」
- URLs: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do ;
  https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status
- Accessed: 2026-09-03
- Retrieved: **in part** — the 하나생명 tables returned in full; the 교보생명 rate grid
  returned but **the month selector's value did not return**, so the as-of date of its figures
  is unknown
- **Why a carrier page is listed on a cross-product regulatory page.** The **평균공시이율** is
  a *regulatory* figure — 감독규정 제1-2조제13호 defines it and the FSS Governor computes it
  [R9] — but it reaches the market through carriers' regulatory disclosure rather than through
  any single FSC page this session could locate. It is cited as the route to a regulatory
  number, not as product documentation; no product parameter is taken from it, and no carrier
  is identified anywhere else in this file.
- **What it establishes — the 평균공시이율 series:**

  | Period | 평균공시이율 | | Period | 평균공시이율 |
  |---|---|---|---|---|
  | 2026 | **2.50%** | | 2020 | 2.50% |
  | 2025 | 2.75% | | 2019 | 2.50% |
  | 2024 | 2.75% | | 2018 | 2.50% |
  | 2023 | 2.25% | | 2017 | 3.00% |
  | 2022 | 2.25% | | 2016 | 3.50% |
  | 2021 | 2.25% | | | |

  with the predecessor **표준이율** at 3.25% for 2015 and 3.50% for 2014 and from 2013-04-01.
  The disclosure adds that the rate is "0.25%포인트 단위로 반올림하여 산출" and applies for the
  whole policy term of a contract concluded in that year. **The 2026 cut from 2.75% to 2.50% is
  the first fall since the 2.50% → 2.25% cut that took effect for 2021.**
- **Where the 평균공시이율 bites** — the first five verified from the regulation or the
  표준약관, the sixth **only at second hand**: the **저축성보험 design test** and its +0.25%p
  variant, and the alternative comparison test [R16 제7-60조제3호·제3의2호·제4호](#krlib-reg-r16); the **부활
  interest ceiling** of 평균공시이율 + 1% [R25]; the **계약자배당 interest floor** [R12]; the
  **변액보험 보증준비금 roll-forward** [R14]; the 별표 14 note 6 discount [R20]; and — through
  a research report quoting a schedule that was not retrieved, so **[unverified]** as
  regulatory text — the **고환급형 test** inside the K-ICS 대량해지 shock [R26] [R36].
- **The 교보생명 grid** shows a **공시기준이율 of 3.19%** with an 적용률 of 3.19% and hence an
  적용이율 of 3.19% across 보장(무배당), 연금(무배당), 연금(배당), 저축(무배당) and
  연금저축(배당) — a worked example of the 공시기준이율 / 적용률 / 적용이율 triple that 별표 27
  defines [R24]. **Because the as-of month did not return, the level is illustrative only and
  is not used as a dated fact anywhere in `krlib`.**
- **[unverified] and deliberately not asserted:** trade reporting places 보장성 공시이율 at
  2.2%, 연금 at 2.29% and 저축 at 2.22% shortly before the 2026 평균공시이율 cut, and reads the
  cut as producing a 2–5% rise in protection premiums. Those articles
  (`https://www.insjournal.co.kr/news/articleView.html?idxno=29000` and `…?idxno=29053`) were
  seen only as search-result summaries and **were not opened**.
- **Used by:** whole_life, pension_savings, variable_annuity and immediate_annuity load-bearing
  — the 평균공시이율 series is the anchor and the rationale for every `[std]` 예정이율 and
  공시이율 in the library, because **the 예정이율 of a specific Korean product is not a
  published number** [R2]. A full-text search of the retrieved 감독규정 returns **zero**
  occurrences of 예정이율 [R9]: the regulation speaks only of the **계약자적립액 적용이율** and
  of the 금리연동형 / 금리확정형 distinction.

(krlib-reg-r62)=

### R62 — 손해보험협회, 공시실 / e-보험시장 (kpub.knia.or.kr)

- Publisher: 손해보험협회 (General Insurance Association of Korea, KNIA/GIAK)
- URLs: https://kpub.knia.or.kr/ (공시실); 상품비교공시 boards beneath it, e.g.
  `…/productDisc/longTermGuarantee/juvenileInsurance.do` (어린이보험),
  `…/productDisc/lostHealth/lostHealthIncreaseRate.do` (실손 보험료 인상률·손해율),
  `…/etcDisc/loan/insContractLoan.do` (보험계약대출금리)
- Accessed: 2026-09-03
- Retrieved: **in part** — the landing pages and board structures render as HTML and were read;
  the comparison grids themselves are loaded by AJAX and come back only to a fetcher that
  posts the board's own form, which the `child` research pass did successfully and the
  `indemnity_medical` pass did not.
- **Why a second association appears on this page.** [R45] covers the **life** side. Korea's
  personal protection market is written on both sides and **the non-life side is the larger of
  the two** — 손해보험 장기보험 ₩73.3조 against 생명보험 보장성보험 ₩62.0조 in 2025 [R47] —
  because 제3보험 is a shared licence field [R1 제4조제3항](#krlib-reg-r1). Four of the ten `krlib` products
  (child, indemnity_medical, cancer, long_term_care) are written predominantly by non-life
  carriers, and their public disclosure sits here at least as often as at [R45]. A page that
  listed only the life association would misdescribe where half of `krlib`'s product evidence
  comes from.
- **What it establishes:** the same statutory 비교공시 architecture as [R45], on the non-life
  side — 상품비교공시 by 장기보장성 class (어린이보험 among them), the 실손의료보험
  보험료 인상률 and 경과손해율 disclosure covering **10 손해보험사 and 7 생명보험사**, and the
  insurer-by-insurer **보험계약대출금리** grid split by 금리확정형 and 금리연동형. It is a
  regulated disclosure board, not marketing.
- **Used by:** child, indemnity_medical, cancer and long_term_care, as the stated route to
  their `[S#]` sources; pension_savings for the 연금저축 비교공시 boards, which run across both
  associations; whole_life for the policy-loan rate comparison. **No number on this page is
  taken from it** — every figure it carries belongs in a product folder as `[S#]`.

---

## 4. Legislation, conduct and consumer protection — 상법, 금융소비자보호법, 예금자보호법

보험업법 supervises the undertaking; **상법 제4편 보험** governs the contract, and it is
**one-way mandatory** — 제663조 forbids any special agreement varying the Part to the
disadvantage of the policyholder, insured or beneficiary (reinsurance and marine excepted).
Every clause of the 표준약관 [R25] is drafted against it.

(krlib-reg-r49)=

### R49 — 국가법령정보센터, 상법 제4편 보험, 제1장 통칙 (제638조~제664조)

- Version: [시행 2026. 7. 23.] [법률 제20991호, 2025. 7. 22., 일부개정]
- URL: https://www.law.go.kr/법령/상법 (body from `LSW/lsInfoR.do?…&efYd=20260723`)
- Accessed: 2026-09-03
- Retrieved: yes (631,670 characters; 제4편 보험 read in full)
- **What it establishes**, in the operative words:
  - **제638조** — the contract takes effect on the promise of premium against the promise of
    "일정한 보험금이나 그 밖의 급여" on an uncertain event affecting property, life or body.
    **제638조의2** — the insurer must accept or decline **within 30 days** of receiving the
    application with premium (running from the medical examination where one is required);
    silence is acceptance; and if the insured event occurs before acceptance the insurer is
    liable unless it had grounds to decline. **제638조의3** — the insurer must deliver the 약관
    and explain its important content; on breach the policyholder may **cancel within three
    months of formation**, which is the statutory source of the 표준약관's **품질보증해지**
    [R25]. **제640조** — a 보험증권 must be issued without delay.
  - **제649조** — the policyholder may terminate **at any time** before the insured event, and
    on termination may claim the **미경과보험료** absent other agreement. **제650조 /
    제650조의2** — non-payment of the first premium voids the contract two months after
    formation absent other agreement; for renewal premiums the insurer must give reasonable
    notice before terminating; and where a contract has been terminated under 제650조제2항 and
    **the surrender value has not been paid**, the policyholder may pay the arrears with agreed
    interest and demand **부활**.
  - **제651조 / 제651조의2** — 고지의무위반: on intentional or grossly negligent misstatement
    or omission of a material fact the insurer may terminate **within one month of learning of
    it and within three years of formation**, but not if it knew or was grossly negligent in
    not knowing; and a matter the insurer asked about **in writing is presumed material**.
    **제652조 / 제653조** — the duty to notify a material increase in risk, and the one-month
    window to demand an increased premium or terminate. **제655조** — the **causation
    defence**: the insurer must still pay where it is proved that the non-disclosure or the
    change in risk "보험사고 발생에 영향을 미치지 아니하였음".
  - **제656조 / 제657조 / 제658조** — liability begins on receipt of the first premium absent
    other agreement; notification of the event; payment **within 10 days** of the amount being
    determined where no period is agreed. **제659조 / 제660조** — 면책 for the intention or
    gross negligence of policyholder, insured or beneficiary, and no liability for war or civil
    disturbance absent agreement.
  - **제662조 (소멸시효)** — "보험금청구권은 **3년**간, 보험료 또는 적립금의 반환청구권은
    **3년**간, 보험료청구권은 **2년**간 행사하지 아니하면 시효의 완성으로 소멸한다."
    **제663조** — the whole Part is **one-way mandatory**: no special agreement may vary it to
    the disadvantage of the policyholder, insured or beneficiary (reinsurance and marine
    excepted).
- **Used by:** every product, in the contract-mechanics section of `product-spec.md`. The
  3-year claim prescription and the 30-day acceptance window are quoted verbatim; nothing is
  modelled.

(krlib-reg-r50)=

### R50 — 국가법령정보센터, 상법 제4편 제3장 인보험 (제727조~제739조의3)

- Version: [시행 2026. 7. 23.] [법률 제20991호]
- URL: https://www.law.go.kr/법령/상법 (body from `LSW/lsInfoR.do?…&efYd=20260723`)
- Accessed: 2026-09-03
- Retrieved: yes (same full-Part retrieval as [R49])
- **What it establishes:**
  - **제727조** — the 인보험 insurer pays on an event affecting the life or body of the
    insured; 제2항 (2014) permits **instalment payment** by agreement, the statutory hook for
    Korean products that pay a lump sum as an income stream. **제729조** — **no subrogation**
    against third parties in 인보험, except that an 상해보험 contract may agree subrogation so
    far as it does not prejudice the insured.
  - **제730조 / 제731조** — the life insurer pays on death, survival or both; a policy on
    **another's death requires that person's written consent** at formation (electronic
    signature admitted since 2017) and again on assignment.
  - **제732조** — a policy on the death of a person **under 15**, or of a person of unsound
    mind, is **void**, with a narrow exception for a 심신박약자 with capacity at formation or
    when becoming an insured under a group policy. **This is why `Child_KR_S` cannot carry a
    meaningful death benefit below age 15**; 제739조 applies the life rules to 상해보험
    **except 제732조**, so a child under 15 *may* be insured against injury. **제732조의2** —
    gross negligence of policyholder, insured or beneficiary does **not** exclude a death
    benefit, and where one of several beneficiaries intentionally kills the insured the others
    are still paid.
  - **제733조 / 제734조 / 제735조의3** — designation and change of beneficiary; and 단체보험,
    where 제731조 does not apply if the group insures its members under a 규약, but naming a
    beneficiary who is neither the insured nor the insured's heir needs the insured's written
    consent unless the 규약 says otherwise.
  - **제736조 (보험적립금반환의무)** — where the contract is terminated under 제649조, 제650조,
    제651조 or 제652조~제655조, or the insurer is discharged under 제659조 or 제660조, it must
    pay "보험수익자를 위하여 적립한 금액". **This is the statutory floor beneath the
    계약자적립액 that 감독규정 제7-63조제1항제1호 makes explicit for 제3보험** [R17].
  - **제739조의2** (2014) — 질병보험: "질병보험계약의 보험자는 피보험자의 질병에 관한
    보험사고가 발생할 경우 보험금이나 그 밖의 급여를 지급할 책임이 있다." **제739조의3** —
    질병보험 borrows the life and accident rules so far as consistent.
- **Note what 상법 does not contain: there is no 간병보험 chapter.** Long-term care is a
  제3보험 종목 under 보험업법 제4조 [R1] but reaches the contract law only through 제739조의3's
  borrowing. `LTC_KR_S`'s benefit definition therefore comes from 노인장기요양보험법 [R54]
  [R55] and from the 약관, **not** from 상법 — a structural point every LTC document must make.
- **Used by:** every product; child load-bearing (제732조), long_term_care load-bearing (the
  absence), cancer and indemnity_medical for 제739조의2 and 제736조.

(krlib-reg-r51)=

### R51 — 국가법령정보센터, 금융소비자 보호에 관한 법률 제46조 (청약의 철회)

- Version: [시행 2026. 1. 2.] (lsiSeq 277247, efYd 20260102)
- URL: https://www.law.go.kr/법령/금융소비자 보호에 관한 법률
- Accessed: 2026-09-03
- Retrieved: yes (62,444 characters; 제46조 read in full)
- **What it establishes:** the statutory cooling-off right the 표준약관 제17조 [R25]
  implements. **제46조제1항제1호** gives a 일반금융소비자 "「상법」 제640조에 따른 보험증권을
  받은 날부터 **15일**과 청약을 한 날부터 **30일** 중 먼저 도래하는 기간" to withdraw.
  **제46조제4항** bars any damages or penalty on withdrawal. **제46조제5항** makes the
  withdrawal ineffective if a claim event has already occurred, unless the policyholder
  withdrew knowing it had.
- **Used by:** every product, one line in `product-spec.md`. The 15/30-day pair is the only
  statutory number in the library that a policyholder can act on directly, and it is quoted
  rather than modelled.

(krlib-reg-r52)=

### R52 — 국가법령정보센터, 예금자보호법 시행령 제18조 (보험금의 계산방법의 예외 등)

- Version: [시행 2025. 9. 1.] (lsiSeq 273001, efYd 20250901), amended 2025-07-29
- URL: https://www.law.go.kr/법령/예금자보호법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (46,515 characters)
- **What it establishes:** **제18조제7항** — "법 제32조제2항에 따른 보험금의 지급한도는
  **1억원** (이하 '보험금 지급한도'라 한다)으로 한다." **The limit is ₩100,000,000, not
  ₩50,000,000.** The ₩50,000,000 figure survives only in the 부칙 of an earlier amendment and
  in pre-2025 consumer material; the FSC publicised the change on the commencement date [R32].
  The article then applies the limit **separately to four buckets** (제18조제7항제1호): 가. DC
  and IRP-type retirement-pension claims, **per member**; 나. the combined total of
  **연금저축계좌** claims (소득세법 시행령 제40조의2제1항제1호가목 and 다목) and legacy
  개인연금저축 / 연금저축 claims against a trustee or an insurer; 다. claims against an insurer
  that are **보험금**, expressly **excluding** benefits payable because the policy term has
  ended ("보험기간이 종료되어 지급되는 보험금은 제외"); 라. everything else. ISA claims are
  combined with bucket 라 per account holder (제18조제7항제2호).
- **Two consequences for `krlib`:** a `Pension_KR_S` policyholder's protection is in bucket 나
  and is **separate** from the ₩100,000,000 covering their other insurance claims; and **a
  maturity benefit is expressly outside bucket 다**, so a maturing 저축성 contract falls into
  bucket 라 with the depositor's other claims. Neither is modelled; both are worth a line in
  the product specs.
- **Used by:** pension_savings load-bearing; every other product for the 예금자보호 sentence
  that 표준약관 제43조 [R25] requires.

---

## 5. Public schemes the private products sit on — 국민건강보험법, 노인장기요양보험법

보험업법 시행령 제1조의2제1항 excludes both of these schemes from "보험상품" altogether [R7],
so the private product and the public scheme are different instruments in law. What the private
product does is sit *on top of* the public one: `Medical_KR_S` reimburses what 국민건강보험
leaves the patient to bear, and `LTC_KR_S` pays on a determination that 노인장기요양보험 makes.

(krlib-reg-r53)=

### R53 — 국가법령정보센터, 국민건강보험법 제41조, 제42조, 제44조

- Version: [시행 2026. 1. 2.] (lsiSeq 276651, efYd 20260102)
- URL: https://www.law.go.kr/법령/국민건강보험법
- Accessed: 2026-09-03
- Retrieved: yes (98,719 characters)
- **What it establishes:**
  - **제41조제1항** lists the seven **요양급여**: 진찰·검사, 약제·치료재료의 지급, 처치·수술 및
    그 밖의 치료, 예방·재활, 입원, 간호, 이송.
  - **제41조제2항**, added 2016, defines the scope: for everything but drugs, 요양급여 covers
    "제4항에 따라 보건복지부장관이 **비급여대상**으로 정한 것을 제외한 일체의 것" — **a
    negative list**; drugs are on a positive list. **제41조제4항** lets the Minister designate
    as 비급여 "업무나 일상생활에 지장이 없는 질환에 대한 치료 등". **비급여 is therefore a
    residual defined by ministerial designation, and it is that residual which 실손 pays.** The
    whole design problem of `Medical_KR_S` follows: the insured loss is defined by exclusion
    from a public list that the insurer does not control and that moves.
  - **제42조제1항** lists the **요양기관** classes — 의료법 institutions, pharmacies, the
    한국희귀·필수의약품센터, 보건소·보건의료원·보건지소, and 보건진료소 — which are exactly the
    classes the 실손 표준약관 keys its outpatient deductible table to [R25] [R17].
  - **제44조제1항** imposes the **본인일부부담금** and lets it be raised for 선별급여;
    **제44조제2항** creates the **본인부담상한제**, under which the NHIS refunds the excess of
    a member's annual 본인일부부담금 over an income-graded 본인부담상한액. The 실손 표준약관
    expressly makes that refund **reduce the insured loss**: cover is limited to "실제 본인이
    부담한 금액 (관련 법령에서 사전 또는 사후 환급이 가능한 금액은 제외한 금액)" [R25]. **The
    per-band 본인부담상한액 amounts sit in a 시행령 별표 that was not retrieved** — see §7.
- **Used by:** indemnity_medical load-bearing; cancer, child, ci_insurance and long_term_care
  for the 급여/비급여 boundary sentence.

(krlib-reg-r54)=

### R54 — 국가법령정보센터, 노인장기요양보험법 제2조, 제15조, 제23조, 제39조, 제40조

- Version: [시행 2026. 5. 26.] [법률 제21690호, 2026. 5. 26., 일부개정]
- URL: https://www.law.go.kr/법령/노인장기요양보험법
- Accessed: 2026-09-03
- Retrieved: yes (133,932 characters)
- **What it establishes:**
  - **제2조제1호** defines "노인등" as a person **65 or over**, or under 65 with a **노인성
    질병** the Decree lists [R55].
  - **제2조제2호** defines 장기요양급여 as services or cash for a person "제15조제2항에 따라
    **6개월 이상 동안 혼자서 일상생활을 수행하기 어렵다고 인정되는 자**에게 신체활동·가사활동의
    지원 또는 간병 등". **The six-month duration test is statutory**, and it is the natural
    definition of the disability inception a three-state LTC model needs.
  - **제15조제2항** — the 등급판정위원회 recognises a claimant meeting the 제12조 eligibility
    and the six-month test "심신상태 및 장기요양이 필요한 정도 등 대통령령으로 정하는
    등급판정기준에 따라" [R55].
  - **제23조** lists the benefit types: **재가급여** (방문요양, 방문목욕, 방문간호,
    주·야간보호, 단기보호, 기타재가급여), **시설급여**, and **특별현금급여** (가족요양비,
    특례요양비, 요양병원간병비). **제39조** has the Minister set the 급여비용 annually by
    benefit type and grade after 장기요양위원회 review. **제40조** imposes a 본인부담금, waived
    for 의료급여 제3조제1항제1호 recipients, with reductions of up to **60%** for listed
    low-income groups.
- **Why this is the LTC benefit definition.** The trigger for a Korean private 간병보험 is a
  **public administrative determination**, not a policy definition — and no Korean carrier
  abandons the statutory language, because the 등급 is what a claimant can evidence.
  `LTC_KR_S`'s benefit therefore attaches to a grade, and the private product's own
  definitional freedom is limited to which grades it pays on and how much.
- **Used by:** long_term_care load-bearing; indemnity_medical for the 1·2등급 exclusion from
  the 비급여 할인·할증 claims count [R25]; whole_life and ci_insurance for the 간병 rider
  framing.

(krlib-reg-r55)=

### R55 — 국가법령정보센터, 노인장기요양보험법 시행령 제7조 (등급판정기준 등) and [별표 1]

- Version: [시행 2026. 5. 12.] (lsiSeq 286011, efYd 20260512); 별표 1 개정 2022-12-20
- URLs: https://www.law.go.kr/법령/노인장기요양보험법 시행령 ;
  https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=135370071&bylClsCd=110201 ([별표 1])
- Accessed: 2026-09-03
- Retrieved: yes (42,367 characters for the Decree; 별표 1 as a 1-page PDF, extracted cleanly)
- **What it establishes — 제7조제1항, the grades, verbatim:**
  > 1. 장기요양 **1등급**: 심신의 기능상태 장애로 일상생활에서 **전적으로** 다른 사람의 도움이
  >    필요한 자로서 **장기요양인정 점수가 95점 이상**인 자
  > 2. 장기요양 **2등급**: … **상당 부분** … **75점 이상 95점 미만**
  > 3. 장기요양 **3등급**: … **부분적으로** … **60점 이상 75점 미만**
  > 4. 장기요양 **4등급**: … **일정부분** … **51점 이상 60점 미만**
  > 5. 장기요양 **5등급**: **치매**(제2조에 따른 노인성 질병에 해당하는 치매로 한정한다)
  >    환자로서 **45점 이상 51점 미만**
  > 6. 장기요양 **인지지원등급**: 치매(같은 한정)환자로서 **45점 미만**

  제7조제2항 sends the 장기요양인정 점수 itself to a 보건복지부 고시 measuring functional
  decline; **that 고시 was not retrieved** — see §7. **[별표 1]** carries the closed list of
  **25 diseases with KCD codes** that alone let a person under 65 be certified: four dementia
  codes, one Alzheimer code, fourteen cerebrovascular codes, four Parkinson-family codes, plus
  척수성 근위축, 다발경화증, 중풍후유증 and 진전. It is the Korean analogue of Japan's 16
  特定疾病, materially narrower in scope but broader in code coverage.
- **[unverified] and used only in a sensitivity:** the 장기요양인정 **유효기간** of 제8조 —
  base 2 years, extended on a same-grade renewal to 1등급 **5 years**, 2~4등급 **4 years**,
  5등급 and 인지지원등급 **2 years**, effective 2025-07-01 — was read from a **long-term-care
  software vendor's customer notice restating the amendment**
  (`https://www.carefor.co.kr/cs/view_notice.php?calmgno=45794`), **not from the decree text**.
- **Used by:** long_term_care load-bearing — the point bands are the statutory definition of
  the `LTC_KR_S` trigger and the source of its grade-severity split; indemnity_medical for the
  1·2등급 cross-reference.

---

## 6. Tax and accounting — 소득세법, 상속세및증여세법, K-IFRS 1117, K-ICS

Korea taxes insurance through **세액공제 — a credit against tax, not a deduction from income**.
That single word changes the after-tax comparison against every other market in this
repository: a Japanese 生命保険料控除 or a German Sonderausgabenabzug is worth more to a
high-rate taxpayer than to a low-rate one, whereas a Korean credit is worth the same to both,
and is worth *more* to the low-rate taxpayer as a fraction of the premium.

(krlib-reg-r56)=

### R56 — 국가법령정보센터, 소득세법 제59조의3·제20조의3·제129조 and 시행령 제40조의2

- Version: 소득세법 [시행 2026. 7. 1.] (lsiSeq 280405); 시행령 [시행 2026. 7. 1.] (lsiSeq
  286211)
- URLs: https://www.law.go.kr/법령/소득세법 ; https://www.law.go.kr/법령/소득세법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (356,757 and 624,319 characters). **The 연금소득 withholding-rate age table in
  제129조제1항제5의2호가목 renders as an image and did not extract**, as does the 연금수령한도
  formula in 시행령 제40조의2.
- **What it establishes — the 연금저축 package:**
  - **제59조의3제1항**: a **credit against tax** of **12%** of the amount paid into a 연금계좌
    — **15%** where 종합소득금액 for the year is **₩45,000,000 or less** (₩55,000,000 총급여
    for the employment-income-only case). Caps, in the 단서: contributions to a **연금저축계좌
    above ₩6,000,000 (600만원) a year are disregarded**, and 연금저축 (within that ₩6,000,000)
    plus 퇴직연금계좌 contributions above **₩9,000,000 (900만원) a year** are disregarded.
    제3항 and 제4항 add ISA-conversion amounts, capped at the lesser of 10% of the converted
    amount and **₩3,000,000 (300만원)**.
  - **The 13.2% / 16.5% rates the Korean market quotes are the statutory 12% and 15% grossed up
    by the 10% 지방소득세 surtax.** The surtax is imposed by the **지방세법, which was not
    retrieved**, so **13.2 and 16.5 are [unverified] arithmetic on a verified base** and any
    `krlib` document using them must say so.
  - **시행령 제40조의2제2항제1호** caps total contributions at **₩18,000,000 (1,800만원) a
    year** across all 연금계좌 (with separate cumulative ₩100,000,000 head-room for the
    연금주택 and 연금부동산 downsizing routes added in 2025) and bars contributions once
    연금수령 has begun; for an insurance-form account, arrears may be paid up to **three years
    and two months** after the last payment. **제40조의2제3항** defines **연금수령**: the
    holder must be **55 or over** and have applied to begin drawing; the account must have been
    open **five years or more** (waived where deferred retirement income is in it); and
    withdrawals must be within the **연금수령한도**, whose formula is an image — but 제4항
    states that the 연금수령연차 runs from the first year in which drawing was possible and
    that **from year 11 the limit does not apply**.
  - **제20조의3제1항제2호** makes withdrawals in 연금 form from a 연금계좌 **연금소득**,
    covering (가) untaxed retirement income, (나) **amounts on which the 제59조의3 credit was
    taken**, and (다) investment growth. **제129조제1항제5의2호** sets the withholding rate by
    the pensioner's age, and **다목 sets 3% for a 종신계약**. The age-band table is an image,
    so the commonly quoted **5% / 4% / 3% by age band is [unverified]** here; what **is**
    verified is that a **lifetime annuity attracts the lowest band, 3%** — a real
    product-design incentive for `Pension_KR_S` and `Immediate_KR_S`.
- **Used by:** pension_savings load-bearing throughout; immediate_annuity for the 종신계약 3%
  rate and the 연금수령 conditions; variable_annuity where written as a 연금저축 form;
  whole_life for the 연금전환 interaction [R58].

(krlib-reg-r57)=

### R57 — 국가법령정보센터, 소득세법 제59조의4 (특별세액공제 — 보장성보험료)

- Version: [시행 2026. 7. 1.] (lsiSeq 280405)
- URL: https://www.law.go.kr/법령/소득세법
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:** **제59조의4제1항** — an employee who pays premiums on a contract
  "만기에 환급되는 금액이 **납입보험료를 초과하지 아니하는** 보험" gets a credit of **12%** of
  the premium — **15%** for a **장애인전용보장성보험** — with each basket capped at
  **₩1,000,000 (100만원) a year**. The 12% credit on up to ₩1,000,000 is worth at most
  **₩120,000 a year** before the local surtax; grossed up at 13.2% it is ₩132,000,
  **[unverified]** as at [R56].
- **The definitional point worth carrying.** The qualifying test — *maturity value ≤ premiums
  paid* — is the **same economic test** 감독규정 제1-2조제3호 uses to define a 보장성보험 at
  the 기준연령 요건 [R9]. Tax law and supervisory law draw the line in the same place, which is
  why Korean products are designed to sit cleanly on one side of it and why the 저축성/보장성
  split is a real product-design boundary rather than a labelling convention.
- **Used by:** term_life, whole_life, ci_insurance, child, cancer, long_term_care and
  indemnity_medical, in the tax paragraph of `product-spec.md`.

(krlib-reg-r58)=

### R58 — 국가법령정보센터, 소득세법 제16조제1항제9호 and 시행령 제25조 (저축성보험의 보험차익)

- Version: 소득세법 [시행 2026. 7. 1.]; 시행령 [시행 2026. 7. 1.], 제25조제9항·제10항 신설
  2025-06-30
- URLs: https://www.law.go.kr/법령/소득세법 ; https://www.law.go.kr/법령/소득세법 시행령
- Accessed: 2026-09-03
- Retrieved: yes. **The annual-annuity ceiling formula in 시행령 제25조제4항제5호 is an image
  and did not extract.**
- **What it establishes:** 제16조제1항제9호 makes the **보험차익** of a 저축성보험 interest
  income, **except** (가) a policy meeting the Decree's conditions and held **10 years or
  more** from first premium to maturity or surrender, and (나) a **종신형 연금보험** meeting
  the Decree's conditions. 시행령 제25조제1항 defines 보험차익 as benefits or refunds received
  (excluding those paid for death, disease, injury or loss of property) **less premiums paid**.
  - **제25조제3항, the 10-year route**, sets **two alternative** condition sets: (1) a
    저축성보험 where the **aggregate premiums payable per policyholder across all such
    policies** do not exceed **₩100,000,000 (1억원)** for contracts made from 2017-04-01
    (₩200,000,000 to 2017-03-31) — but **not** where the premiums are drawn down as a
    fixed-term annuity beginning before the tenth anniversary; or (2) a **월적립식** policy
    meeting all three of: payment term **5 years or more**; **level basic premium** monthly (an
    increase up to 1× the original allowed) with advance payment of no more than 6 months; and
    **aggregate monthly premiums per policyholder across all 월적립식 policies of ₩1,500,000
    (150만원) or less** for contracts from 2017-04-01.
  - **제25조제4항, the 종신형 연금보험 route**, sets five conditions: 1. annuity paid **from
    age 55 after the payment term ends until death**; 2. **no payment in any form other than an
    annuity**; 3. the contract and the annuity fund must **extinguish on death**, and where a
    guarantee period is set it must be **within the sex- and age-specific 기대여명 연수
    published by the 국가데이터처** (rounded down) [R38], the contract extinguishing at the end
    of the guarantee period where the annuitant dies within it; 4. **policyholder, insured and
    beneficiary must be the same person**, and the contract may not be surrendered after the
    first annuity payment and before death; 5. the annual annuity must not exceed a stated
    formula (image, not extracted).
  - **제25조제6항** resets the "first premium date" on three changes: a change of policyholder
    other than by death; conversion of a 보장성 policy to a 저축성 one; and an increase of the
    basic premium beyond 1× the original.
  - **제25조제9항 and 제10항** (신설 2025-06-30) bear directly on a Korean whole-life product's
    late-life options: where a 보장성보험's sum insured is reduced by agreement and the
    released amount is drawn as an annuity, that is **treated as conversion to a 저축성보험**,
    with the first annuity date as the new first-premium date — **unless** the original
    보장성보험 was a 월적립식 policy with a sum insured of **₩900,000,000 (9억원) or less**,
    premiums were fully paid before the first annuity date, policyholder, insured and
    beneficiary are the same, and the annuity starts at **55 or later**, in which case the
    original first-premium date is preserved. **That provision is the tax basis of the Korean
    연금전환 feature many 종신보험 carry**, and `WholeLife_KR_S`'s product spec records it.
- **Note the connection to [R27].** Condition set (1)'s ten-year test is why the FSS calibrates
  its **30% 단기납 종신 additional-lapse floor** to the 11th-year lapse rate on single-premium
  bancassurance savings (29.4%–30.2%): that is the duration at which the tax exemption is met
  and the refund ratio jumps. Tax design and lapse assumption are one question in Korea.
- **Used by:** whole_life load-bearing (연금전환 and the 보장성 test); variable_annuity and
  immediate_annuity for the 종신형 연금보험 route; pension_savings for the boundary against the
  연금계좌 regime [R56]; ci_insurance for the 저축성 element of a 종신 chassis.

(krlib-reg-r59)=

### R59 — 국가법령정보센터, 상속세 및 증여세법 제8조·제34조 (보험금의 상속·증여)

- Version: [시행 2026. 1. 2.] (lsiSeq 276123, efYd 20260102)
- URL: https://www.law.go.kr/법령/상속세 및 증여세법
- Accessed: 2026-09-03
- Retrieved: yes (148,788 characters)
- **What it establishes:** **제8조제1항** — "피상속인의 사망으로 인하여 받는 생명보험 또는
  손해보험의 보험금으로서 **피상속인이 보험계약자인 보험계약에 의하여 받는 것은 상속재산으로
  본다**." **제8조제2항** — where the policyholder is someone else but **the deceased in
  substance paid the premiums**, the deceased is treated as the policyholder and 제1항 applies.
  **제34조제1항** — where beneficiary and premium payer differ, the benefit attributable to the
  other person's premiums is a **gift** to the beneficiary; and where the beneficiary paid
  premiums out of property received as a gift, the gift is the benefit less those premiums.
  **제34조제2항** disapplies 제34조 where 제8조 already treats the benefit as estate property.
- **The practical Korean planning point** — that a policy taken out and paid for by the
  *beneficiary* on the life of a parent falls outside 제8조 — follows from 제8조제2항 read with
  제34조, and is why Korean 종신보험 is sold as an inheritance-tax vehicle. **No numeric
  threshold or rate is asserted here**: the 상속세 rate schedule and the 일괄공제 were not
  extracted.
- **Used by:** whole_life load-bearing (the inheritance-planning framing that drives Korean
  종신보험 sales); term_life; ci_insurance and child in passing.

(krlib-reg-r60)=

### R60 — 한국회계기준원 회계기준위원회, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」

- Publisher: 한국회계기준원 (Korea Accounting Institute), mirrored by KDI 경제교육·정보센터;
  date of the resolution **2018-05-25**
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=177159
- Accessed: 2026-09-03
- Retrieved: **in part** — the release body returned; **the 별첨 HWP carrying the standard's
  substance was not converted**
- **What it establishes:** the Korean adoption of IFRS 17 as **기업회계기준서 제1117호
  「보험계약」**. The release states an effective date of **2021-01-01**, which was the
  pre-deferral date; **the operative commencement of 2023-01-01** is established not from this
  release but from the 부칙 to 금융위원회고시 제2022-53호 [R14] and from the FSC's own framing
  [R30]. **Unlike Japan, where IFRS applies as 指定国際会計基準 on a voluntary basis, K-IFRS
  1117 is mandatory for Korean insurers**; there is no adopter list to consult, because the
  answer is "all of them".
- **How the regulation borrows the standard's vocabulary**, which is the practical reason this
  entry is cited from every product: 시행령 제63조 speaks of **현행추정치** and of the
  **발생사고요소 / 잔여보장요소** split [R8]; 감독규정 제6-11조제3항 defines 투자계약부채 as
  contracts "보험계약의 법률적 형식을 취하고 있으나, 한국채택국제회계기준 제1117호의 적용을
  받지 않아 투자계약으로 분류된 계약들" [R10]; and the whole 해약환급금준비금 [R11] exists only
  because IFRS 17 measurement can fall below the contractual surrender value.
- **Used by:** every product, in the measurement-basis paragraph of `technical-notes.md`. **No
  `krlib` model computes a CSM, a risk adjustment or a fulfilment cash flow.**

### The three measurement bases one projection feeds

`jplib` sits under three bases because Japan runs a locked-in statutory reserve, a prospective
ESR and voluntary IFRS 17. **Korea also has three, but they are different three, they are all
live now, and two of them are the same set of cash flows discounted differently.** A `krlib`
document that conflates them will be wrong about which assumptions are fixed and which are
re-set at every valuation date.

**IFRS 17 — the earnings measure.** K-IFRS 제1117호 has been mandatory since 2023-01-01 [R60].
The liability is fulfilment cash flows — a current, unbiased, probability-weighted estimate of
future cash flows, discounted on the prescribed 국고채-based curve with **관찰금리 to a 20-year
LOT, an LTFR of 4.55% and a liquidity premium of 91bp** [R27] — plus a risk adjustment, plus
the **CSM**, which is unearned profit released as service is provided. **Everything is re-set
at every reporting date**; nothing is locked in at issue. This is where a Korean insurer's
reported earnings come from, and it is why the lapse assumption on a 무해지 product became a
supervisory matter [R27]: the CSM on that form is extraordinarily sensitive to it.

**K-ICS — the capital measure.** The 건전성감독기준 재무상태표 [R13] starts from the K-IFRS
consolidated balance sheet and re-measures it "경제적이고 시장가격과 일관된 가치로", assets at
exit price and liabilities at transfer or settlement price, with **no own-credit adjustment**.
The liability is a **best-estimate liability plus a 위험마진**, and against it stands a
**지급여력기준금액** built from five risk modules, of which the life-and-long-term-health
module alone carries **seven shock-based sub-risks** including **해지위험액** and
**사업비위험액** [R13]. The floor is **100%** [R8]; below it the 적기시정조치 ladder starts
[R14]; and the whole thing is phased in over ten years by four optional 경과조치 [R35]. **It is
a regulatory measurement, not an accounting standard** — the distinction matters because the
natural reflex is to treat IFRS 17 as the economic frame, and in Korea the *capital* frame is a
separate re-measurement of the same cash flows.

**The 해약환급금준비금 — the distributable-earnings measure, and Korea's own.** At each
balance-sheet date, company-wide, the insurer compares the IFRS 17 잔여보장요소 (plus certain
separate-account and investment-contract liabilities, grossed up for OCI) against the aggregate
**contractual 해약환급금 computed under 감독규정 제7-66조제1항 — on that rule even for products
that may contractually pay less** — and appropriates the shortfall inside 이익잉여금 [R11]. A
well-capitalised insurer (K-ICS ≥ 130% before transitionals at the previous quarter-end)
appropriates only **80%** of it. This is neither an accounting liability nor a capital
requirement: it is a **brake on dividends**, sitting inside K-ICS 가용자본 while being
unavailable for distribution. It stood at **₩32.2조 at end-2023** [R36]. Nothing in `uslib`,
`uklib`, `jplib`, `frlib` or `delib` corresponds to it, and it is the reason a Korean insurer's
economics on a 무해지 product depend on the **surrender value** and not only on the fair-valued
liability.

**One set of gross cash flows feeds all three.** The premiums, claims, expenses, surrenders,
policy-loan flows and options-and-guarantees streams are common; what differs is the
discounting, the margin (risk adjustment plus CSM under IFRS 17, 위험마진 under K-ICS, none at
all in the surrender-value comparison), the aggregation level (portfolio and cohort for IFRS
17, module and correlation for K-ICS, **the whole company** for the 해약환급금준비금) and the
purpose. That is why `krlib`'s reference implementations keep product cash flows
basis-agnostic, publish `result_cf()` as a gross best-estimate stream, and **stop deliberately
before any of the three** — exactly the design `uklib`, `jplib`, `frlib` and `delib` use,
reached here from the most crowded regulatory starting point in the repository. What the models
*do* compute beyond the cash flows — the **계약자적립액** and the **해약환급금** — they compute
because both are contractual quantities with a published bound [R19] [R20], and because the
third basis above cannot be discussed at all without them.

---

## 7. Gaps, fetch failures and every claim left unverified

Disclosed in full, as the research standard requires. Nothing here is a formality: each item is
a place where a product document must tag **[unverified]** rather than assert, or must derive a
value and tag the derivation **[std]**.

**A. Not retrieved at all**

1. **The 경험생명표 qx table** — [R33] [R34]. The single largest gap in the library. No
   mortality rate from any edition of the industry table was located in any public KIDI
   channel; the 보도자료 listing served no 경험생명표 item and the 빅데이터 플랫폼 page refused
   connection on port 9443. **Only 평균수명 and 65세 기대여명 are public, and only through a
   trade newspaper.** Consequence: **every `mort_table.csv` in `krlib` is `[std]`**, anchored
   on [R38] and bracketed by [R33]'s two statistics, with a `provenance` column on every row.
2. **참조순보험요율 — the life side only** — [R4] [R34]. The 생명보험 notifications are not
   published: the bureau files with the FSC and the public sees the rate only as the
   보험가격지수 ratio [R22], while a carrier's 상품요약서 identifies the notification behind
   its 예정 경험사망률 by document number alone. **This gap does not extend to 장기손해보험**,
   whose 참조순보험요율 the bureau publishes as a numeric display [R61] — see the correction at
   §7-D. So a `krlib` morbidity, incidence or disability rate is `[std]` where [R61] does not
   carry it (실손 severity, long-term-care inception) and source-tagged where it does
   (암 발생률, 질병입원율).
3. **보험업감독업무시행세칙 [별표 22] and [별표 24]** — [R26]. **[별표 22] and [별표 22의 1]
   were located in the 별표 index at `bylSeq` 3295667 and 3295669 and simply were not
   downloaded**; the 별표 route that worked for 별표 14, 15 and 27 was available and unused, so
   this is a live task and not a closed gap. 별표 24's `bylSeq` was never obtained, and the two
   other routes tried for it returned a navigation shell and HTTP 403 respectively. **The
   K-ICS 대량해지위험 shocks (35% / 25% / +35%p / +25%p / ×(1−40%)) and the 보증준비금 CTE(70)
   basis are [unverified]**, quoted only through [R36] and the `variable_annuity` research
   file. The article numbers said to invoke 별표 24 — 감독규정 제6-11조제10호 and 시행세칙
   제4-15조 — are likewise [unverified].
4. **국민건강보험법 시행령 별표 — the per-band 본인부담상한액** — [R53]. The 본인부담상한제
   exists and reduces the insured loss under the 실손 표준약관 [R25]; **its amounts are not in
   this file** and `Medical_KR_S` may not assert one.
5. **The 보건복지부 고시 defining the 장기요양인정 점수** — [R55]. 시행령 제7조제2항 delegates
   the scoring instrument and it was not retrieved. The **point bands are verified**; how a
   claimant scores against them is not, so `LTC_KR_S` cannot map a functional state to a grade
   from a retrieved source and must construct the mapping `[std]`.
6. **노인장기요양보험법 시행령 제8조 (유효기간)** — [R55]. Read only from a software vendor's
   customer notice. The 5/4/2-year same-grade renewal extensions are **[unverified]** and are
   used in a sensitivity only.
7. **지방세법** — [R56] [R57]. Not retrieved. **The 13.2% and 16.5% 연금저축 rates and the
   ₩132,000 보장성보험료 figure are [unverified] arithmetic on a verified 12% / 15% / 12%
   base.**
8. **KOSIS 완전생명표 single-year qx tables** — [R39]. Not downloaded. This is a live task, not
   a closed gap: the table build must fetch them and record the KOSIS table id in each
   product's `sources.md`.
9. **생명보험협회 FACT BOOK 2025 edition and the 금융통계월보 tables** — [R45]. Structure and
   contents read; **no number is taken from either**.
10. **보험연구원 「2025년 보험산업 주요 이슈: ② IFRS17 및 K-ICS」**
    (`https://www.kiri.or.kr/report/downloadFile.do?docId=618289`) — identified in search, not
    downloaded. It would carry the 2023–2025 supervisory-guideline chronology in one place,
    including the 2023 실손의료보험 계리가정 산출기준 that [R27] supersedes only in part.
11. **FSS 지급여력비율 현황 for 2025-03 and 2025-06**
    (`https://eiec.kdi.re.kr/policy/materialView.do?num=267710`, `…num=271247`) — [R30]. Not
    opened; only the September 2025 figures are used, and the component amounts behind them
    were not obtained either.
12. **The 2024 노인장기요양보험 통계연보** — [R43]. Search summary only.
13. **No 한국보험계리사회 (Institute of Actuaries of Korea) document of any kind.** There is no
    `krlib` counterpart to `jplib`'s 保険計理人の実務基準 [R22 of `jplib`](#krlib-reg-r22) or `frlib`'s NPA 1 /
    NPA 2, and none is claimed. Where a `krlib` document describes a Korean actuarial
    convention that is not in a retrieved regulation — the three-source 위험률차 / 이자율차 /
    사업비차 framing is the clearest case, now **deleted from 감독규정** [R12] — it says
    "market practice" and tags the claim [unverified].

**B. Retrieved, but rendered as an image and therefore not readable**

Korean regulation renders many formulas as images inside the HTML or the PDF. Every one of
these was located and **could not be extracted**; none is reproduced anywhere in `krlib`:

14. the **해약환급금 formula display** and the **two 계약자적립액 accrual formulas** of
    감독규정 제7-66조제1항 [R19] — the operative *words* extracted, the *formulas* did not;
15. the **α weight formula and one β formula** in 시행세칙 별표 27 [R24] — so the α input set
    is known (opening 계약자적립액, prior year-end asset duration, prior-year premium income)
    and the caps are known (0.5%p rounding, 60% maximum) but the functional form is not;
16. the **기본요구자본 correlation formula** of 감독규정 제7-2조제1항 [R13];
17. the **연금소득 원천징수 age-band table** of 소득세법 제129조제1항제5의2호가목, the
    **연금수령한도 formula** of 시행령 제40조의2 [R56], and the **annual-annuity ceiling
    formula** of 시행령 제25조제4항제5호 [R58].

**C. Retrieved only through a mirror, a trade newspaper or a research report**

18. **The 제10회 경험생명표 summary statistics** — [R33]. A trade newspaper (보험매일) is the
    only retrieved source. Every figure is news-sourced and must be tagged.
19. **The 2025 industry outturn** — 수입보험료 ₩266.6595조, 당기순이익 ₩12.2172조, the line
    splits, ROA, ROE and 총자산 [R47]. A trade newspaper reporting an FSS release. Every figure
    is news-sourced.
20. **The FSS 실손 사업실적 [R44] and the 지급여력비율 현황 [R30]** reached `krlib` through the
    **KDI 경제교육·정보센터 mirror**, not through fss.or.kr.
21. **The K-ICS 대량해지 shocks and the 해약환급금준비금 accumulation-ratio schedule** [R36] —
    a 보험연구원 CEO Report quoting 별표 22 and the 감독규정 부칙 respectively. The **₩23.7조 /
    ₩32.2조** reserve balances are the report's own figures and were not traced to a
    supervisory release.
22. **The CSM forecasts** sometimes attributed to [R46]'s seminar (생명보험 ₩64.7조 → ₩64.3조;
    손해보험 ₩70.3조 → ₩71.8조) were read from a **search summary**, not from the retrieved
    deck. **[unverified].**

**D. Two corrections, recorded rather than quietly fixed**

23. **`fss.or.kr` is not unreachable.** The cross-product research pass recorded that a plain
    HTTPS request to `https://www.fss.or.kr` returned "Empty reply from server" and that the
    site "did not respond to the fetcher at all", and every FSS release in that pass was
    consequently taken through the KDI mirror [R44] [R30] or through a trade newspaper [R47].
    **That conclusion was too strong.** The `indemnity_medical` research pass, on the same day,
    fetched the joint FSC/FSS 5세대 실손 launch 보도자료 **directly from `fss.or.kr`** — both
    the post (`/fss/bbs/B0000188/view.do?nttId=217561&menuNo=200218`) and a 655 KB, 15-page PDF
    through `/fss/cmmn/file/fileDown.do` [R31]. As on the ACPR host in `frlib`, **the
    discriminator is the fetcher and the path, not the host.** A later drafter should re-try
    `fss.or.kr` directly before falling back to a mirror, and should treat the news-sourced
    figures in [R47] as **replaceable with a primary FSS release**, not as the best available
    evidence.
30. **The 참조순보험요율 are not uniformly unpublished, and this page said they were.** The
    cross-product research pass reasoned from the KIDI 보도자료 listing, which carries no
    reference-rate item [R34], and from 감독규정 제1-2조제1호, which defines the rate as one
    *filed with the FSC* [R9], to the conclusion that "no 참조순보험요율 value was retrieved
    and none exists in public". **The second half of that is wrong.** On the same day the
    `cancer` and `indemnity_medical` passes opened `https://www.kidi.or.kr/user/nd13261.do` and read a
    published, dated **장기손해보험** 참조순보험요율 display carrying an 암 발생률 grid and a
    질병입원율 grid by age and sex [R61]. The conclusion held for the **life** side only, where
    it stands. The error runs in the expensive direction — it would have had ten products tag
    `[std]` a table they can source — and its shape is exactly item 23's: **a negative inferred
    from one channel was generalised to a publisher.** Neither the 경험생명표 finding [R33]
    [R34] nor the life-side finding is disturbed by the correction.

**E. The single most consequential unresolved number**

24. **The 예정이율 of any specific Korean product.** A full-text search of the retrieved
    2026-05-06 감독규정 returns **zero** occurrences of 예정이율 [R9]: the regulation names
    only the **계약자적립액 적용이율** and the 금리연동형 / 금리확정형 split. The rate lives in
    the 산출방법서, which is **not public** [R2]. The **평균공시이율 is published** and is
    verified (2.50% for 2026, from 3.50% in 2016) [R48]; carrier **공시이율 by product class is
    published** monthly; **예정이율 is neither.** Consequently:
    - **every 예정이율 in `krlib` is `[std]`**, with the [R48] 평균공시이율 series as its
      anchor and its stated rationale;
    - trade reporting that places 보장성 공시이율 at 2.2%, 연금 at 2.29% and 저축 at 2.22%
      before the 2026 cut, and that expects a 2–5% rise in protection premiums, is
      **[unverified]** — those articles were seen only as search summaries;
    - the one retrieved carrier 공시기준이율 (3.19% across five classes) has an **unknown as-of
      month** and is illustrative only [R48].

**F. Retrieval notes worth carrying into every Korean research pass**

25. `law.go.kr` serves statutes and 행정규칙 only through the inner endpoints
    `LSW/lsInfoR.do?lsiSeq=<id>&efYd=<yyyymmdd>` (법령) and
    `LSW/admRulLsInfoR.do?admRulSeq=<id>` (행정규칙). The friendly
    `https://www.law.go.kr/법령/<name>` URL returns navigation chrome only, and the
    `admRulLsInfoP.do` / `admRulInfoP.do` **P**-suffixed forms return the shell with the body
    in a frame that plain fetchers do not follow. **Two `krlib` product research passes
    recorded 보험업감독규정 and 시행세칙 as "not retrieved" for exactly that reason before the
    R-endpoint route was found**; their 감독규정 facts therefore rest on FSC press releases and
    KIRI reports, and this page's do not.
26. A 별표 is a three-step fetch: `admRulBylContentsInfoR.do?bylSeq=<id>` →
    `flDownload.do?flSeq=<pdfFlSeq>` → PDF. Without the `bylSeq` there is no route, which is
    why 별표 24 was not reached [R26] and [R20], [R21], [R24] and [R25] were. **별표 22 is a
    different case**: its `bylSeq` (3295667, and 3295669 for 별표 22의 1) *was* recovered from
    the index and the fetch was simply never made. `flSeq` is a **global file id and not the
    `bylSeq`** — guessing `flDownload.do?flSeq=<bylSeq>` returns an unrelated document, as one
    attempt on 별표 14 did.
27. `ko.wikisource.org`'s 보험업법 mirror is **법률 제8902호, 시행 2008-06-15 — seventeen years
    out of date**. It was tried, nothing is cited from it, and it must not be used.
28. `casenote.kr` returns article text reliably and was the first route that worked for
    보험업법 제2조, 제4조 and 제5조; its 제2조 view compressed the 가/나/다 sub-items, so it is
    a cross-check and never the authoritative retrieval [R1] [R2].
29. The version of the **시행세칙** law.go.kr serves as current takes effect **2026-09-10, one
    week after the access date** [R23]. Facts from it are facts about the imminent text.

**G. What is not in scope here, and where it lives instead**

This page carries only the cross-product references. Product-specific regulatory and actuarial
sources — a single product's litigated benefit definition, a 태아보험 supervisory notice, a
carrier's disclosure of its own policy-loan rate schedule, an epidemiological study behind one
incidence table — are numbered `R#` inside that product's `sources.md`, carried verbatim from
its `_research/<slug>.md`, and are cited as `[R#]` rather than `[REG-R#]`. Primary product
documentation (약관, 상품요약서, 보험안내자료, 사업방법서 extracts, 공시자료) is never listed
here; it is `[S#]` in the product folder, and the product folder is the only place an
individual carrier is identified at all — with the deliberate exception of [R48], where a
carrier page is the only located route to a **regulatory** figure and is cited as such.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-reg-r1
[R10]: #krlib-reg-r10
[R11]: #krlib-reg-r11
[R12]: #krlib-reg-r12
[R13]: #krlib-reg-r13
[R14]: #krlib-reg-r14
[R15]: #krlib-reg-r15
[R17]: #krlib-reg-r17
[R18]: #krlib-reg-r18
[R19]: #krlib-reg-r19
[R2]: #krlib-reg-r2
[R20]: #krlib-reg-r20
[R21]: #krlib-reg-r21
[R22]: #krlib-reg-r22
[R23]: #krlib-reg-r23
[R24]: #krlib-reg-r24
[R25]: #krlib-reg-r25
[R26]: #krlib-reg-r26
[R27]: #krlib-reg-r27
[R28]: #krlib-reg-r28
[R29]: #krlib-reg-r29
[R3]: #krlib-reg-r3
[R30]: #krlib-reg-r30
[R31]: #krlib-reg-r31
[R32]: #krlib-reg-r32
[R33]: #krlib-reg-r33
[R34]: #krlib-reg-r34
[R35]: #krlib-reg-r35
[R36]: #krlib-reg-r36
[R38]: #krlib-reg-r38
[R39]: #krlib-reg-r39
[R4]: #krlib-reg-r4
[R40]: #krlib-reg-r40
[R41]: #krlib-reg-r41
[R42]: #krlib-reg-r42
[R43]: #krlib-reg-r43
[R44]: #krlib-reg-r44
[R45]: #krlib-reg-r45
[R46]: #krlib-reg-r46
[R47]: #krlib-reg-r47
[R48]: #krlib-reg-r48
[R49]: #krlib-reg-r49
[R50]: #krlib-reg-r50
[R51]: #krlib-reg-r51
[R52]: #krlib-reg-r52
[R53]: #krlib-reg-r53
[R54]: #krlib-reg-r54
[R55]: #krlib-reg-r55
[R56]: #krlib-reg-r56
[R57]: #krlib-reg-r57
[R58]: #krlib-reg-r58
[R60]: #krlib-reg-r60
[R61]: #krlib-reg-r61
[R62]: #krlib-reg-r62
[R7]: #krlib-reg-r7
[R8]: #krlib-reg-r8
[R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
