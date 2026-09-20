# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/immediate-annuity.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is per
product: `S1` here is a different document from `S1` in every other product's `sources.md`,
and the cross-product `references/regulatory-and-actuarial-references.md` runs its own frozen
R1–R62 scheme, cited as [REG-R#]. **The two R schemes must never be read across** — the
clearest instance being right here, this file's **[R1]** being the 금융분쟁조정위원회
조정결정서 that decided the 즉시연금 dispute while the library's **[REG-R1]** is 보험업법
제2조·제4조. Access date for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document: a 약관 (*yakgwan*, policy conditions), a
  상품요약서 (*sangpum yoyakseo*, the statutory product summary), a 상품안내장 (sales
  leaflet), a 사업방법서 (*saeop bangbeopseo*, business method statement) or a carrier
  공시 page. These are what makes a contractual mechanic *sourced* rather than assumed, and
  on this product they carry something no other krlib [S#] set does: a **published
  개인연금사망률 table**, an expense breakdown by component *and* by payout shape, and a run
  of 예상연금액 illustrations the model's two mortality-free shapes can be checked against.
- **[R#]** — a regulatory, judicial, statutory or statistical reference that only this
  product needs. Here they are dominated by one thing: the **즉시연금 과소지급 분쟁**, whose
  determination [R1], supervisory press release [R2] and Supreme Court judgment [R6] are
  the three documents the whole 상속연금형 specification turns on.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Unused ids are omitted, so both schemes have gaps, and nothing is renumbered.** The
research file runs to S15 and R31. Not cited, and therefore not listed: **S15** (한화생명
다이렉트 product page, retrieved only in part — its numeric parameters sit behind a calculator
widget — and superseded by the full 약관 at [S7]); **R7** (the 판례속보 headline for [R6],
whose case number the fetcher rendered inconsistently); **R8** (a separate 2023 Supreme Court
decision on the character of a 상속형 death benefit claim, with no fact resting on it); **R9**
and **R10** (소득세법 시행령 제25조 and 소득세법 제16조제1항제9호, which the cross-product
library carries with a fuller retrieval as [REG-R58], cited instead); **R15** (a
consumer-education page corroborating [R14] and adding nothing); **R20** (경향신문, HTTP 301 to
the site root, not retrieved at all); and **R30** (the 예금보호한도 increase, which reaches the
documents through [REG-R32] beside the statutory [REG-R52]).

**No number in the drafting documents rests on a source recorded as not retrieved.** One entry
in this file's own [S#]/[R#] lists is `Retrieved: no` — **[R31]**, 보험업감독규정, whose
article text no route would return — and every claim resting on it is tagged
**[unverified]** at the point of use. Three more are `Retrieved: in part` ([R5], [R16],
[R28]) and each is cited only for what came back. The cited **[REG-R#]** entries are
**not** uniformly `Retrieved: yes` either, and their statuses are set out at the head of
the cross-product section below rather than left to be assumed. No new source was fetched
at drafting and no tag was added.

Company and branded product names appear in this file and in `_research/immediate-annuity.md`
and nowhere else in the library. In the three drafting documents a carrier is its tag alone,
so a reader can always resolve who said what — here — and never has to.

---

## Primary product sources

Fourteen documents from ten providers, all retrieved: one statutory product summary [S1],
four 방카슈랑스 상품안내장 [S2] [S3] [S4] [S5], one filed 사업방법서 [S6], three 약관 booklets
[S7] [S8] [S9] and five carrier 공시 or product pages [S10] [S11] [S12] [S13] [S14]. **Four
are deferred annuities and are cited for payout-phase machinery only** — [S8], [S9], [S13],
[S14] — never for an issue-age, premium or expense parameter, and the scope limit is restated
at each. **One caveat governs the whole set**: every 즉시연금-*specific* document here is of
2011–2017 vintage and no currently marketed product bearing that name was located at a major
carrier in this research pass, so the specification is written to the mechanism rather than to
a named live product and says so once at its head.

(krlib-immediate_annuity-s1)=

### S1 — 하나생명, 「무배당 행복knowhow즉시연금보험 상품요약서」 (statutory product summary)

- Publisher / type: 하나생명보험주식회사; 상품요약서, the statutory product summary handed over
  at inception; file stamped `20170403`, 11 PDF pages
- URL: https://www.hanalife.co.kr/home/download2.do?fileName=PROD/(%EB%AC%B4)%ED%96%89%EB%B3%B5knowhow%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C_20170403.pdf&downFileName=(%EB%AC%B4)%ED%96%89%EB%B3%B5knowhow%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (served as `application/x-msdownload` and rejected
  by the markdown fetcher; the bytes are a clean text-layer PDF, all 11 pages extracted)
- **The mechanics anchor of the whole product**, the only complete statutory product summary
  for an 즉시연금 retrieved, and the richest quantitative source in the corpus: four of the
  model's five parameter families rest on it.
  - **§IV-2, the 개인연금사망률 table** at 보험나이 50 / 60 / 70 by sex — 남자 0.00225 /
    0.00353 / 0.00728, 여자 0.00097 / 0.00118 / 0.00251 — the only carrier-published annuitant
    rates in the corpus, and the two fit anchors and one residual of `mort_table.csv`.
  - **§VIII, the expense breakdown by component and by payout shape** — 계약체결비용 and
    계약관리비용 on a 남자 60세 일시납 basis (종신 2.61 + 1.30%, 상속 20년만기 2.19 +
    1.30%), the three 위험보험료 levels (0.0000% for 종신연금형 1형, 1.4669% for 상속형
    20년만기, 4.9466% for 종신연금형 2형), the 연금수령기간 중 비용 of 0.80% of the
    연금연액, and the **해지공제액 schedule, nil at every duration**. Every row of
    `charge_table.csv` is this section.
  - **§VII, the 모집수수료율** — 2.08% on 종신연금형 and 1.75% on 상속연금형, first year
    only: the pair `comm_rate`'s round 2.00% sits inside, and what puts the commission
    below the 계약체결비용. **§IV-4, the 공시이율 of 2.50% at 2017-04**, which is
    `decl_rate`. **§VI**, the 15-row 해약환급금 illustration on three interest bases, from
    which the `min_guar` crediting basis comes.
  - The product taxonomy, the issue-age and premium-limit table including the age-banded
    상속형 cap of ₩1,500,000,000, the benefit table defining 생존연금 / 사망보험금 /
    만기보험금, and 주1–주7 on payment modes, the commutation rate and the guarantee period.

(krlib-immediate_annuity-s2)=

### S2 — 교보생명, 「바로받는 연금보험 무배당 Ⅱ」 방카슈랑스 상품안내장 (sales leaflet)

- Publisher / type: 교보생명보험주식회사 방카슈랑스본부, distributed by 하나은행; 상품안내장,
  「2016년 4월 개정」, 준법감시인 확인필 1-1603-17 (2016.03.14), 2 pp.
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L05024317_r.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (2 pp., text layer extracted in full)
- An earlier vintage of the same carrier's product as [S3], cited **because the two differ**: a
  12년(12회) minimum guarantee on the 종신연금형 where [S3] shows 10년, no 확정기간연금형 at
  all, 공시이율 2.83% at 2016-03, 평균공시이율 3.5%, and a two-step 최저보증이율 of 1.5% / 1.0%
  splitting at ten years. It supplies two points of the declared-rate and floor observation
  ranges in `model.md`'s standardization table, the ₩10,000,000 minimum premium, and its own
  상속연금형 annuity table.

(krlib-immediate_annuity-s3)=

### S3 — 교보생명, 「바로받는 연금보험」 방카슈랑스 상품안내장, SC제일은행 배포본 (sales leaflet)

- Publisher / type: 교보생명보험주식회사 교보방카슈랑스, distributed by SC제일은행; 상품안내장,
  illustrations dated 「2017년 12월 현재공시이율 2.52%」, 2 pp.
- URL: https://www.standardchartered.co.kr/hp/file/ap/pd/694895_baro_ad.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (2 pp., text layer extracted in full)
- **The illustration anchor**, and the second most load-bearing document here: the most
  complete single 예상연금액 table retrieved, one common model point (일시납 1억원, 남자 55세)
  priced across four 종신연금형 정액형 guarantees, three 집중보장형 options, five 상속연금형
  options and four 확정기간연금형 terms, each on three interest bases. Three results rest on it
  — the **확정기간연금형 load cross-check** (solving the annuity-certain identity against all
  four published terms reproduces every one within 1.4% on a 4.97% first-day deduction, the
  independent corroboration of the 3.50% load), the model's **90만원 comparison** at model
  point 9, and the **stepped 최저보증이율 of 1.25% / 1.00% / 0.75%** that `crediting_table.csv`
  adopts. It also gives the product envelope, the death-benefit definition, the guarantee
  wording that makes the obligation survive the annuitant, and the 선지급 right.

(krlib-immediate_annuity-s4)=

### S4 — 동양생명, 「무배당 Angel즉시연금보험」 방카슈랑스 상품안내장 (sales leaflet)

- Publisher / type: 동양생명보험주식회사, distributed by 하나은행; 상품안내장, 「2016. 4
  개정상품」, 준법감시필 01-1603-003, 2 pp.
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L74024315_r.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (2 pp., text layer extracted in full)
- A second carrier on the **same model point as [S3]** (남자 55세, 일시납 1억원), which is what
  lets the two implied gross annuity factors be compared directly; plus a 거치형 illustration
  on the same point that isolates the deferral effect, a 공시이율 of 2.95% at 2016-03, a
  three-step 최저보증이율 of 2.0% / 1.5% / 1.0%, and the clearest statement of the 상속연금형
  만기형 selling proposition — 「만기에 수령하는 만기보험금을 상속 및 상속세 재원으로 활용할 수
  있습니다」, the sentence that explains why three quarters of the market buys the shape the
  dispute was about.

(krlib-immediate_annuity-s5)=

### S5 — 삼성생명, 「에이스즉시연금보험 B2.2(무배당)」 방카슈랑스 상품안내장 (sales leaflet)

- Publisher / type: 삼성생명보험주식회사, distributed by KEB하나은행; 상품안내장, 판매개시일
  2016. 4. 1, 준법감시필 BA 제16-26호, 4 pp.
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L03024328_r.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (4 pp., text layer extracted in full)
- The most **tax-conscious** design retrieved, and the source of the guarantee-period menu: the
  보증지급횟수 is not a menu of round numbers but a rule — a minimum of ten years' payments (or
  the 기대여명 if shorter, floored at five), a middle option equal to the 기대여명, and a
  maximum of (100 − 연금개시나이) years — which is 소득세법 시행령 제25조제4항제3호 written
  straight into the product [REG-R58]. Also 주2, the no-surrender rule; 주8, the 선지급 right;
  「별도의 사망보험금은 지급되지 않습니다」, on which the life shape's `claims_death` column of
  zeros rests; a 12-month 공시이율 history running 3.40% down to 2.80%; a 브릿지연금형 variant;
  a 상속연금형 10년만기 surrender-value illustration; and the 연금선수익자 / 연금후수익자
  mechanism.

(krlib-immediate_annuity-s6)=

### S6 — ABL생명(구 알리안츠생명), 「무배당 알리안츠프리미어즉시연금보험 사업방법서 (별지)」 (filed 기초서류)

- Publisher / type: 에이비엘생명보험주식회사; **사업방법서 별지** — one of the three 기초서류
  under 보험업법 제5조제3호 [REG-R2] — filed vintage `120701_130331`, 6 pp.
- URL: https://abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2017/05/15/03_%EC%82%AC%EC%97%85%EB%B0%A9%EB%B2%95%EC%84%9C(120701_130331)_(%EB%AC%B4)%EC%95%8C%EB%A6%AC%EC%95%88%EC%B8%A0%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (6 pp., text layer extracted in full)
- **The only filed 기초서류 for an immediate annuity retrieved in this session**, and of the
  2012–2013 vintage — exactly the cohort at the centre of the dispute. §9 gives the 공시이율
  machinery in algebraic form: the 공시기준이율 as the mean of an internal and an external
  indicator, the external one a 국고채 / 회사채 blend weighted by the insurer's own bond book,
  a three-month weighted moving average, and the **80%–120% corridor** within which the
  declared rate may be set — one of the two carrier weightings the specification sets side by
  side to show that no model can derive a Korean declared rate. Also the 최저보증이율 schedule,
  the policy-loan rate (공시이율 + 1.5%), a large-contract discount (§10-나, recorded and not
  applied), 부부계약, the partial withdrawal surviving annuitisation (§8-나), and **§10-라, the
  annuitant-mortality ratchet confined expressly to the 거치형**.

(krlib-immediate_annuity-s7)=

### S7 — 한화생명, 「한화생명 e연금보험 무배당 약관」 (policy conditions)

- Publisher / type: 한화생명보험주식회사; 주계약 약관 with 특약 and 부록, edition dated 2024.
  4. 1, document code 1789-046, 150 pp.
- URL: https://direct.hanwhalife.com/products/downloadProxy/%ED%95%9C%ED%99%94%EC%83%9D%EB%AA%85%20e%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98%20%EB%AC%B4%EB%B0%B0%EB%8B%B9_1789-046_%EC%95%BD%EA%B4%80_20240401.pdf?docUrl=dynamic%2Fdirect%2Fproduct%2Fcms_LbOsZt9dvgKnqRcB_1715162604727.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (150 pp.; the annuity provisions, the definitions,
  제7조, 제11조, 제23조, 제31조 and 별표1 extracted and read)
- **The post-dispute drafting**, and the document that closes the story [R1] tells: its
  상속연금형 row in 별표1 now says, in the contract itself, that the annuity is the interest on
  the fund 「에서 소정의 사업비를 차감하여」 — the deduction the 2017 조정결정 held could not
  be asserted, because it was absent from the 약관, is now on the face of the 약관. It also
  supplies verbatim 제7조, the Max[공시이율, 최저보증이율] rule with a 최저보증이율 schedule of
  1.0% / 0.75% / 0.5%, the bottom of the observed range; 제11조제3항, the 선지급 discount at
  the 공시이율; **제23조, the 보험나이 six-month rule**, the age basis of the whole model;
  **제31조, 「종신연금이 지급개시된 이후에는 해지할 수 없습니다」**, on which the life shape's
  nil lapse rate rests; and 별표1, the annuity struck on 「연금개시시의 계약자적립액」, with
  주8's 100.1% floor recorded and not applied.

(krlib-immediate_annuity-s8)=

### S8 — 푸본현대생명, 「MAX 연금보험 하이파이브 무배당(B2001) 적립형/거치형 약관」 (policy conditions)

- Publisher / type: 푸본현대생명보험주식회사, distributed by 하나은행; 약관 booklet with
  연금전환특약(거치형) and 지정대리청구서비스특약, 107 pp.
- URL: https://image.kebhana.com/cont/download/insdocument/provide/L17014307_agree.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (107 pp.; the annuity-form pages, the surrender
  articles and the summary pages extracted and read)
- **Scope: a deferred annuity**, cited only for payout-phase machinery — the same machinery
  `Immediate_KR_S` needs — and never for an issue-age or premium parameter. The richest payout
  menu retrieved: 종신연금형 기본형 with 10/20/30년/100세/기대여명 guarantees, a 핵심기간집중형
  doubling the annuity for ten years, 확정연금형 out to fifty years, 상속연금형, a
  **proportional split across forms in 5% units**, and a 노후설계자금 lump sum of up to 50% of
  the fund — all recorded in `product-spec.md` as available and in `technical-notes.md` as not
  modelled. 주14 gives the instalment-frequency interest rule that makes the annual and monthly
  modes equal in value, which is the warrant for the monthly mode `Immediate_KR_S` projects
  and the basis of every annual-to-monthly comparison here; 제33조 gives the surrender
  article.

(krlib-immediate_annuity-s9)=

### S9 — 우체국보험(체신관서), 「우체국연금보험 2312 약관」 (policy conditions)

- Publisher / type: 우정사업본부 우체국보험; 약관 booklet, product code P200068, vintage 2312,
  108 pp.
- URL: https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/YAK_P200068_202312.pdf
- Accessed: 2026-09-03, Retrieved: **yes** (108 pp.; 제2조 정의, 제3조 지급사유, 별표1 and the
  annuity notes extracted and read)
- **Scope: a deferred annuity, and the public-sector comparator** — 우체국보험 is written by
  the state under 우체국예금·보험에 관한 법률 rather than 보험업법, so its terms are the
  control case against the licensed market. Cited for payout-phase machinery only: a 종신연금형
  with **no 상속연금형 at all**, guarantees of 20년/30년/90세/100세 and no ten-year option, a
  조기집중연금형 paying 200% or 300%, 확정기간연금형 of 5/10/15/20/30년, the 신공시이율
  vocabulary, the 100.1% floor at annuitisation, 주7 on death not accelerating a certain term,
  and 주11's 「신공시이율로 계산한 이자를 가산합니다」 — the other half of the warrant for
  the monthly payment mode.

(krlib-immediate_annuity-s10)=

### S10 — 하나생명 공시실, 「적용이율 공시 — 최저보증이율 및 경과기간별 중도해지율」 (carrier disclosure)

- Publisher / type: 하나생명보험주식회사; 공시 web page, product-by-product table
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab5.do
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch; the annuity rows read)
- Two findings, both load-bearing. First, the **최저보증이율 of three of one carrier's own
  즉시연금 products by sales vintage** — (무)하나즉시연금보험, (무)넘버원즉시연금보험 and
  (무)행복knowhow즉시연금보험, covering 2007-10 to 2018-12, all opening at 2.5% / 2.0% and the
  last stepping to 1.5% / 1.0% — the **top of the observed floor range** in `model.md`'s
  standardization table. Second, that these products carry **no 중도해지율** at all, unlike the
  same carrier's savings contracts: the second document behind the finding that the 해약공제액
  is a published run of zeros, and hence that `cv_pp(t) = av_pp(t)` where surrender is
  permitted.

(krlib-immediate_annuity-s11)=

### S11 — 하나생명 공시실, 「적용이율 공시 — 표준이율 및 평균공시이율」 (carrier disclosure)

- Publisher / type: 하나생명보험주식회사; 공시 web page
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch, both tables read)
- The **평균공시이율 series 2016–2026** and its definition — 「감독원장이 정하는 바에 따라
  산정한 전체 보험회사 공시이율의 평균으로, 보험계약의 체결시점의 평균공시이율을 보험기간 동안
  적용합니다」. Cited for the definition, for the series (2.50% for 2026, 2.75% in 2024–2025,
  2.25% in 2021–2023), and for the rule that a carrier must show this rate beside its own —
  which gives the 2.50% of `decl_rate` two justifications.

(krlib-immediate_annuity-s12)=

### S12 — NH농협생명, 「공시기준이율」 (carrier disclosure)

- Publisher / type: 엔에이치농협생명보험주식회사; 공시 web page, figures as at 2025년 1월
- URL: https://www.nhlife.co.kr/ho/on/HOON0039M00.nhl
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch, formula and table read)
- A **second, different** 공시기준이율 weighting to set beside [S6] — 외부지표금리 × 40% +
  운용자산이익률 × 60%, the external indicator itself weighted 국고채 78.5% / 회사채 21.5% for
  the general account — with the 조정율 of 89.16% that converts it into a declared annuity rate
  of **2.55% at 2025-01**. [S6] and [S12], with a third weighting at [R1], are the evidence
  that **no model in this library derives a Korean declared rate and none should**, which is
  why `decl_rate` is a scalar.

(krlib-immediate_annuity-s13)=

### S13 — 하나생명, 「(무)The하나연금보험」 상품 페이지 (carrier product page)

- Publisher / type: 하나생명보험주식회사; product page, 공시이율 stated as at 2023년 1월
- URL: https://www.hanalife.co.kr/prd/personal/banca/theHana/theHanaJoinGuide.do
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- **Scope: a deferred annuity**; cited for the payout-form menu and rate levels only. A
  활동기집중형 with a 3× or 5× multiple over a five- or ten-year concentration period — the
  most aggressive front-loading in the corpus, and one of the six carrier names
  `product-spec.md` records for that shape — plus a 100세 option in the 확정연금형 menu, a
  공시이율 of 2.80% at 2023-01, and a 최저보증이율 of 1.25% / 1.00% / 0.50%.

(krlib-immediate_annuity-s14)=

### S14 — KB국민은행 방카슈랑스, 「(무)IBK e-연금보험(2601)」 상품 페이지 (bancassurance product page)

- Publisher / type: KB국민은행, as agent for IBK연금보험주식회사; product page, 공시이율 stated
  as at 2026년 9월
- URL: https://obank.kbstar.com/quics?QSL=F&cc=b033493%3Ab033492&page=C020712&prcode=BK09002747
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- **Scope: a deferred contract, not an 즉시연금**; cited for rate levels and menu breadth only.
  The **most current declared rate retrieved** — 연 2.56% as at 2026-09 — with a 최저보증이율
  of 1.25% / 1.00% / 0.50% and a payout menu from a monoline annuity writer, and the upper end
  of the three-observation band inside which the adopted 2.50% sits.

---

## Regulatory and actuarial references

Twenty-four entries — twenty retrieved in full, three in part and **one not at all**. Four
groups: the dispute record [R1]–[R6]; the market and product literature [R11] [R12] [R16]
[R27]–[R29]; the 경험생명표 reporting [R13] [R14]; and the news and trade coverage of the
litigation [R17]–[R25], cited only for the dispute's course and its aggregates. **No aggregate
about the dispute is stated by any supervisory document**, and `product-spec.md` says so.

(krlib-immediate_annuity-r1)=

### R1 — 금융감독원 금융분쟁조정위원회, 조정결정서 제2017-17호 (dispute-resolution determination)

- Publisher / type: 금융감독원 금융분쟁조정위원회; 조정결정서, 조정일자 **2017. 11. 14.**,
  안건명 「즉시연금(만기/상속형)에서 최저보증이율 적용의 적정성」, 12 pp. PDF, released as an
  attachment to [R2]
- URL: https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=e24e669336e894dd227d7b2d8b9ad652&fileSn=4&bbsId=
- Accessed: 2026-09-03, Retrieved: **yes** (served as `application/octet-stream` and rejected
  by the markdown fetcher; the bytes are a clean text-layer PDF, all 12 pages extracted)
- **The single most important document behind this product.** It is the determination
  itself, not a report of it, and five things in the specification rest on it:
  - **§1-가, the premium-split identity** A = 보장계약 보험료 B + 사업비 C + 연금계약
    순보험료 D, quoting the 약관 서두's own definition of the 연금계약적립액 — what
    `check_premium_split()` asserts.
  - **§1, the contract in numbers** — ₩1,000,000,000 single premium, ten-year term, monthly,
    written 2012-09-12; declared rate 4.5% at inception; floor 2.5% / 1.5%; death benefit 10%
    of premiums; **사업비 5.325%** — and the six annuity levels actually paid from 2012-10 to
    2017-10, a **fall of 55.4% in five years** reproduced as a mechanism at model point 8.
  - **§2, the insurer's own description of the retention**, the clearest statement of the
    mechanism in the corpus and the wording `retention_pp()` implements; and **§1-나 with
    별표1, the 약관 as it then stood** — the wording that does not mention the retention.
  - **§3, the reasoning** on objective construction of standard terms, on when a 산출방법서
    may and may not be incorporated into a 약관, and the 주문 ordering interest on the fund
    with no retention — which is `retention_basis = "as_ordered"`. It also carries the
    공시기준이율 formula verbatim on a 35/65 weighting, the third carrier weighting.

(krlib-immediate_annuity-r2)=

### R2 — 금융감독원, 보도자료 「금융분쟁조정위원회, 즉시연금 관련 분쟁에서 보험약관에 따라 산출한 연금을 지급하도록 결정」 (regulator press release)

- Publisher / type: 금융감독원 분쟁조정1국; 보도자료, 배포 2018. 4. 9., 3 pp. PDF
- URL (landing page): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=14077&menuNo=200218
- URL (PDF): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=e24e669336e894dd227d7b2d8b9ad652&fileSn=3&bbsId=
- Accessed: 2026-09-03, Retrieved: **yes** (landing page as HTML; PDF as bytes, 3 pp.,
  extracted with `pypdf`)
- The supervisor's own **structural exposition of 만기환급형 즉시연금** — premium, less
  commission and risk premium, credited at Max[공시이율, 최저보증이율], less the 만기보험금
  지급재원 — which is §1 of the source list for `technical-notes.md`'s crediting and retention
  recursions. It carries a worked ₩100,000,000 illustration on a round ₩6,000,000 of expense
  and risk premium (the 6.0% the specification's own reconstruction vindicates to two
  significant figures); the insurer's **acceptance** of the determination in February 2018;
  **§4, the January 2018 약관 amendment before and after**, with the finding that the offending
  sentence had been reused from a product with no maturity benefit; and the FSS's notification
  of **every life insurer** on 2018-03-15.

(krlib-immediate_annuity-r3)=

### R3 — 금융감독원, 보도참고자료 「즉시연금에 가입한 소비자가 「시효 중단」을 원하실 경우 …」 (regulator press release)

- Publisher / type: 금융감독원 분쟁조정1국; 보도참고자료, 배포 2018. 9. 4., 3 pp. PDF
- URL (landing page): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=14453&menuNo=200218
- URL (PDF): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=94c114d0270a3cd188e3b9c8e3e3e8a6&fileSn=1&bbsId=
- Accessed: 2026-09-03, Retrieved: **yes** (landing page as HTML; PDF as bytes, 3 pp.)
- Fixes the **two** 분조위 determinations at 「'17.11월, '18.6월」 — the only source for the
  second, and hence for the 2018-06 row of the chronology; records that insurers went to court
  notwithstanding; quotes 금융위원회의 설치 등에 관한 법률 제53조의2 on the interruption of
  limitation, which is the 2018-09-04 row; and announces the 즉시연금 corner on 파인.

(krlib-immediate_annuity-r4)=

### R4 — 금융감독원, 보도자료 목록 (검색어 「즉시연금」) (regulator index page)

- Publisher / type: 금융감독원; 보도자료 search listing
- URL: https://www.fss.or.kr/fss/bbs/B0000188/list.do?menuNo=200218&searchCnd=1&searchWrd=%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch, four rows returned)
- The **complete** set of FSS press releases whose titles contain 즉시연금 — 2012-09-26,
  2018-04-09, 2018-09-04, 2019-01-07 — which is what makes the supervisory chronology
  exhaustive rather than merely long, and the source of the nttIds behind [R2] and [R3]. Cited
  once, for the 2019-01-07 response about a revived comprehensive examination.

(krlib-immediate_annuity-r5)=

### R5 — 금융감독원, 「"즉시연금보험 절판마케팅 주의하세요" 소비자경보 발령」 (regulator press release)

- Publisher / type: 금융감독원 소비자보호총괄국; 보도자료, 2012. 9. 26.
- URL: https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=9501&menuNo=200218
- Accessed: 2026-09-03, Retrieved: **in part** (landing page HTML; the body summary came back,
  the attachment was not opened)
- The **demand shock that created the disputed cohort**: the tax announcement of **2012-08-08**
  removing the interest-income exemption for 즉시연금 held ten years or more from the following
  year, and the end-of-line selling push the FSS warned against. Two rows of the chronology and
  one paragraph of the tax section rest on it, and nothing else.

(krlib-immediate_annuity-r6)=

### R6 — 대법원 2025. 10. 16. 선고 2022다225897 판결 [보험금] (Supreme Court judgment)

- Publisher / type: 대법원; 판결, 원심 서울동부지방법원 2022. 2. 9. 선고 2020나32079 판결
- URLs: https://casenote.kr/%EB%8C%80%EB%B2%95%EC%9B%90/2022%EB%8B%A4225897 ·
  https://lx.scourt.go.kr/search/detail/precedent/0/2025000024727 ·
  https://www.law.go.kr/LSW/precInfoP.do?mode=0&precSeq=612847
- Accessed: 2026-09-03, Retrieved: **yes** (all three mirrors fetched; 판시사항, 판결요지 and
  주문 read; **the full 이유 was not reproduced by any of the three**)
- **The end of the dispute, and the reason `retention_basis` carries two settings rather than
  one.** Four holdings on the 명시·설명의무: that a pointer clause 「그 문서에 따라 계산한다」
  to an undelivered document containing only formulae does **not** discharge the duty; that
  breach severs the offending term rather than voiding the contract; that the remainder is
  construed by the understanding of an average customer; and that severance **does not change
  the annuity payable**. 주문: 「원심판결을 파기하고, 사건을 서울동부지방법원에 환송한다」. The
  statement that neither reading of the retention is "the" right one is this judgment set
  against [R1].

(krlib-immediate_annuity-r11)=

### R11 — 법제처 찾기쉬운 생활법령정보, 「노후준비와 연금제도 › 사적연금제도 › 개인연금제도 › 연금보험」 (government plain-language restatement)

- Publisher / type: 법제처; 생활법령 page, content stated as current at 2026-08-15
- URL: https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2056&ccfNo=3&cciNo=2&cnpClsNo=2
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The state's own restatement of the three tax-exemption routes (ten-year lump sum with a
  ₩100,000,000 cap from 2017-04-01, 월적립식 with a ₩1,500,000 monthly cap, and 종신형 with
  annuitisation from 55, no lump-sum option and a guarantee period within life expectancy), and
  the definition of 연금보험 by reference to 보험업감독규정 제1-2조제5호. Cited once, in the
  regulatory-class sentence, beside [REG-R1].

(krlib-immediate_annuity-r12)=

### R12 — 이경희, 「즉시연금보험의 특성과 가입자 선택행동 분석」, 보험금융연구 제23권 제1호 (2012. 2), pp. 101–132 (peer-reviewed article)

- Publisher / type: 보험연구원, 보험금융연구; 32 pp. PDF hosted by KCI
- URL: https://journal.kci.go.kr/kiri/archive/articlePdf?artiId=ART001640411
- Accessed: 2026-09-03, Retrieved: **yes** (32 pp., text layer extracted; §§I–IV and 표1–표9
  read)
- **The only micro-level empirical picture of the Korean immediate-annuity market that is
  public**, and after [S1] and [S3] the most-cited source in these documents: 1,414 contracts
  written by one insurer over FY2008–FY2009, about 30% of the market's premium. It carries the
  **split across payout options** — 73.6% of contracts and 75.1% of premium 상속형 against
  18.2% 종신형 — which is what makes the retention switch the most important thing in the
  model; **표7**, the guarantee periods chosen, 97.3% of life-shape buyers taking ten years,
  which is the anchor's `annuity_term`; **그림3**, the premium distribution whose median is the
  anchor's ₩100,000,000; **§III-1**, 「옵션 중 사망(생존) 위험률이 적용되는 것은 종신형에
  한정된다 … 확정형과 상속형은 사망률을 사용하지 않는다」, on which the three-shape
  architecture rests; and **§III-2-라**, citing 보험업감독규정 제7-60조 4 for the rule that a
  pure life annuity with no guarantee period may not be sold in Korea — **[unverified]** as to
  the article text. It is fifteen to eighteen years old and the specification says so.

(krlib-immediate_annuity-r13)=

### R13 — 보험저널, 「4월부터 연금보험 수령액 줄어든다…10차 경험생명표 적용시 15% 하락」 (news article)

- Publisher / type: 보험저널, 강성용 기자; 입력 2024. 2. 15, 수정 2024. 2. 20
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=21975
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch, body and table read)
- The **only source retrieved that quantifies the effect of a 경험생명표 revision on an annuity
  in payment**: a 6th / 9th / 10th table comparison on a fixed ₩200,000,000 fund annuitising at
  60, and the ~15% fall from the 9th to the 10th. Cited once, in the longevity-sensitivity
  discussion. **Secondary; the underlying KIDI release was not retrieved**, and the dependent
  sentence says so.

(krlib-immediate_annuity-r14)=

### R14 — 보험매일, 「제10회 경험생명표 개정…소비자에 미치는 영향은」 (news article)

- Publisher / type: 보험매일 (fins.co.kr)
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The 제10회 평균수명 (남 86.3세, 여 90.7세) and the **65세 기대여명 (남 23.7년, 여 27.1년)** —
  the third fit constraint of `mort_table.csv`, reaching this library through trade press
  because 보험개발원 publishes no more than that [REG-R33] [REG-R34]. Also the April 2024
  application date and the statement that in-force policyholders are unaffected, which makes
  the ratchet a pricing question and not a projection one. **Secondary**, and the two dependent
  sentences say so.

(krlib-immediate_annuity-r16)=

### R16 — 미래에셋투자와연금센터, 「가입 다음 달부터 바로 연금 받는 보험, 어떤 종류가 있나?」 (consumer-education page)

- Publisher / type: 미래에셋투자와연금센터
- URL: https://investpension.miraeasset.com/contents/view.do?idx=21314
- Accessed: 2026-09-03, Retrieved: **in part** (HTML fetch; the taxonomy and the
  minimum-premium sentence returned, nothing else)
- Cited once, for one fact: minimum premiums run from ₩10,000,000 upward and differ by carrier,
  「M사는 1천만원, S사는 3천만원 등」. **Secondary**, tagged as such where used.

(krlib-immediate_annuity-r17)=

### R17 — 뉴스타파, 「즉시연금사태 : 또다시 가동된 보험사의 '탈출 마술'」 (investigative journalism)

- Publisher / type: 뉴스타파
- URL: https://newstapa.org/article/bh-br
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch, body read)
- The case study of the ₩1,000,000,000 contract that became 조정번호 제2017-17호, with quoted
  약관 wording; the per-carrier shortfall estimates (55,000 contracts / ₩430,000,000,000 at one
  carrier, ₩85,000,000,000 at another, about ₩1 trillion industry-wide); one board's decision
  to pay ₩37,000,000,000 instead; and another carrier's refusal of the determination on
  2018-08-10. **Investigative journalism, and every figure taken from it is flagged as
  news-sourced** in `product-spec.md`.

(krlib-immediate_annuity-r18)=

### R18 — 서울신문, 「'16만명의 1조원' 즉시연금 소송, 소비자 다시 승소…삼성생명 패소」 (news article)

- Publisher / type: 서울신문, 2022-01-19
- URL: https://www.seoul.co.kr/news/newsView.php?id=20220119500177
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- 서울중앙지방법원 민사45부, 2022-01-19, 18 plaintiffs organised by 금융소비자연맹; the
  aggregate scope of about 160,000 policyholders and ₩800bn–₩1tn, and one carrier's share of
  50,000 policyholders and ₩400,000,000,000. Two rows of the chronology and the head-note
  figure rest on it. **News article.**

(krlib-immediate_annuity-r19)=

### R19 — 아시아경제, 「그때 그때 다른 소송 결과…즉시연금 소송 향방은」 (news article)

- Publisher / type: 아시아경제, 2022-01-21
- URL: https://www.asiae.co.kr/article/2022012111425045120&mobile=Y
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The docket as at January 2022 — four class actions all won by consumers at first instance, an
  individual action lost by the consumer in October 2021, and the per-carrier exposures (₩400bn
  / ₩85bn / ₩70bn). The source for the statement that the outcome differed by action, which is
  what makes the two-setting switch a faithful model rather than an evasion. **News article.**

(krlib-immediate_annuity-r21)=

### R21 — 리걸타임즈, 「[보험] '삼성생명' 즉시연금보험 가입자들 최종 패소」 (legal trade press)

- Publisher / type: 리걸타임즈
- URL: https://www.legaltimes.co.kr/news/articleView.html?idxno=89743
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The **companion Supreme Court case numbers 2022다308747 and 2022다308754**, 57 plaintiffs,
  appeals dismissed, and the reasoning that the deduction method could be severed while the
  remainder of the contract stood. The second document behind the 2025-10-16 row, and the only
  one carrying the companion dockets. **Legal trade press.**

(krlib-immediate_annuity-r22)=

### R22 — 머니투데이, 「대법원 "'즉시연금' 설명 부족하나 계약 유효…미지급금 안 줘도 된다"」 (news article)

- Publisher / type: 머니투데이, 2025-10-17
- URL: https://www.mt.co.kr/society/2025/10/17/2025101711452448769
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- 대법원 2부, 주심 엄상필 대법관; 51 plaintiffs; the first-instance win, the appellate reversal
  and the final outcome; and the reasoning that voiding the contracts outright would leave
  policyholders worse off — the practical rationale of the severance holding. The plaintiff
  count of 51 here against 57 at [R21] is left unresolved and both are recorded. **News
  article.**

(krlib-immediate_annuity-r23)=

### R23 — 보험저널, 「즉시연금보험 분쟁이 남긴 숙제…'설명 부족'은 잘못, '계약 무효'는 아냐」 (news article carrying law-firm commentary)

- Publisher / type: 보험저널, 강성용 기자, 2025-11-05
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=28805
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The practical reading of [R6] for insurers: the deduction structure must be set out **in
  outline in the 약관**, and a bare pointer to the 산출방법서 is not enough. That is the
  drafting rule the 2024 약관 at [S7] already complies with, and what connects the judgment to
  the current market's wording. **News article carrying law-firm commentary.**

(krlib-immediate_annuity-r24)=

### R24 — EBN, 「대법 "설명 부족" 판결에…금감원, 즉시연금 불완전판매 점검」 (news article)

- Publisher / type: EBN 뉴스센터, 2025-10-19
- URL: https://www.ebn.co.kr/news/articleView.html?idxno=1682654
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The FSS's stated intention, after the Supreme Court ruling, to run a consumer-protection
  inspection into the selling of 즉시연금 — the last row of the chronology — and the 2018
  industry estimate restated. **News article**; no supervisory document states the aggregate,
  and the specification says so.

(krlib-immediate_annuity-r25)=

### R25 — 한국금융신문, 「[주간 보험 이슈] 생보사 즉시연금 소송 승소…」 (trade press)

- Publisher / type: 한국금융신문, 2025-10-19
- URL: https://www.fntimes.com/html/view.php?ud=2025101912240396138a55064dd1_18
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The same outcome from a second trade title, giving the bench and the 51 plaintiffs. **Used
  only to cross-check [R22]**, and cited beside it wherever the plaintiff count or the FSS
  follow-up is stated.

(krlib-immediate_annuity-r26)=

### R26 — 日刊NTN, 「[쟁점 예규] 즉시연금보험 상속 평가액은 '상속 개시 당시 해지환급금'」 (tax trade press)

- Publisher / type: 日刊NTN (intn.co.kr)
- URL: https://www.intn.co.kr/news/articleView.html?idxno=2015014
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- 국세청 예규 상증 사전-2019-법령해석재산-0378, 결정일 2021-01-19, holding that an 즉시연금
  falling into an estate is valued at the **해약환급금 at the date of death**; the underlying
  상속세 및 증여세법 제8조 [REG-R59]; and the facts of the ruling. Cited once, in the
  estate-tax paragraph, expressly as a trade report of a ruling **not itself retrieved**.

(krlib-immediate_annuity-r27)=

### R27 — KDI 경제교육·정보센터, 「우체국에서 가입즉시 연금 받으세요!」 (government release, reproduced)

- Publisher / type: 한국개발연구원 경제교육·정보센터, reproducing a 우정사업본부 release
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=116191
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The launch of 우체국즉시연금보험 on **2011-09-23**: issue ages 45–80 (the lower bound of the
  composite's band), premium ₩5,000,000 to ₩250,000,000, 종신형 with a twenty-year guarantee
  and 상속형, **공시이율 4.8% at 2011-09** — the top of the observed declared-rate range, and
  the high-rate-era datum that makes the 2.50% adoption a choice rather than an inevitability —
  최저보증이율 2%, and the 0.5% large-contract discount recorded and not applied.

(krlib-immediate_annuity-r28)=

### R28 — 뱅크샐러드, 「즉시연금 총정리 | 1억 넣으면 얼마 받을까?」 (commercial content site)

- Publisher / type: 뱅크샐러드
- URL: https://www.banksalad.com/articles/보험-즉시연금-1억
- Accessed: 2026-09-03, Retrieved: **in part** (HTML fetch; the taxonomy and a worked example
  returned, the tables only in summary)
- Cited twice and for one thing only: a **2026년 4월 공시이율 of 2.67%**, the upper observation
  in the band inside which the adopted 2.50% sits. **Commercial content site**, tagged as such
  at both points of use.

(krlib-immediate_annuity-r29)=

### R29 — KB의 생각, 「즉시 연금보험이란? — 뜻 & 정의」 (bank glossary entry)

- Publisher / type: KB국민은행
- URL: https://kbthink.com/dictionary/view.html?dictId=KED-00009822
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetch)
- The three-way taxonomy, the pre-2013 exemption and the **February 2013 amendment cutting
  the exempt threshold to ₩100,000,000 per person**, and the estate-valuation point. It
  corroborates [R5] on the 2012-08-08 announcement, but on the cap it **conflicts** with the
  retrieved 시행령, which puts ₩200,000,000 in force to 2017-03-31 and ₩100,000,000 only from
  2017-04-01 [REG-R58]. The amendment text was not retrieved, the conflict is unresolved, and
  `product-spec.md` records the pre-2017 figure as **[unverified]** rather than choosing
  between them. Its further claim of a 2016 amendment is **[unverified]** on the same
  footing, neither the article nor the amendment having been retrieved.

(krlib-immediate_annuity-r31)=

### R31 — 보험업감독규정 (금융위원회 고시) — **not retrieved**

- Publisher / type: 금융위원회 / 법제처 국가법령정보센터; 고시
- URLs attempted: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196 ·
  https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000250658&chrClsCd=010201 ·
  https://www.ulex.co.kr/법률/2100000214154-21843-보험업감독 ·
  https://www.fsc.go.kr/po040301/view?noticeId=3864 ·
  https://www.fsc.go.kr/comm/getFile?srvcId=RULENOTICE&upperNo=4076&fileTy=ATTACH&fileNo=8
- Accessed: 2026-09-03, Retrieved: **no**, for the article text. The 국가법령정보센터
  administrative-rule viewer is JavaScript-rendered and returns navigation chrome only; the
  U-LEX mirror timed out at 60 s; the FSC 입법예고 page returned notice metadata and put the
  text in an unretrieved `.hwp`; and the FSC file endpoint served a 규제영향분석서 instead.
- Everything obtained is second-hand and every dependent claim is tagged **[unverified]**: that
  제7-60조 governs 생명보험 상품설계; that 제7-60조제3호 requires a savings contract's
  net-premium reserve at the 평균공시이율 to exceed cumulative premiums, **15 months for a
  single premium**; and that 제7-60조 4 forbids a life annuity without a guarantee period of at
  least five years [R12 §III-2-라](#krlib-immediate_annuity-r12). **Note the split**: the *provisions themselves* were
  retrieved by a different route as [REG-R16] and [REG-R18], which the documents cite wherever
  the article text matters; this entry survives only because three claims rest on paragraphs
  that retrieval does not reach.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that page
plain [R#] refers to its own entries, so the two schemes must never be read across. Research
provenance: `_research/regulatory-actuarial.md`. The entries the immediate annuity documents
cite were all accessed 2026-09-03. **Their retrieval status is not uniform and is stated
here rather than assumed**: two are `Retrieved: no` — **REG-R26** (시행세칙 별표 22 and
별표 24) and **REG-R39** (the KOSIS single-year 완전생명표 qx tables) — and four are
`Retrieved: in part` — **REG-R32**, **REG-R34**, **REG-R48** and **REG-R60**. The rest are
`Retrieved: yes`. Nothing in the drafting documents rests on either `no` entry for a number:
REG-R26 is reached only by two sentences of `technical-notes.md` that carry [unverified],
and REG-R39 is cited only as the named to-do behind the mortality build and beside
**REG-R38**, which is the entry the 완전생명표 figures actually come from. Of the four
partials, REG-R48 is load-bearing — the 2026 평균공시이율 of 2.50% — and what came back from
it was the 하나생명 평균공시이율 series in full; the part that did not was the 교보생명 rate
grid's as-of month, on which nothing here rests.

- **REG-R1** — 보험업법 제2조·제4조: the 생명보험 / 손해보험 / 제3보험 licence split. 즉시연금
  is a **생명보험상품**, 제4조제1항제1호나목 naming 연금보험 as a 종목 of its own.
- **REG-R2** — 보험업법 제5조 등 (기초서류): the **산출방법서 is filed with the FSC and never
  published** — the fact the whole dispute turns on, and why no annuity formula here was read
  from a basis document.
- **REG-R3** — 보험업법 제120조: the duty to accumulate 책임준비금, cited and not computed.
- **REG-R5** — 보험업법 제181조·제184조: the 선임계리사 behind the 기초서류.
- **REG-R9** — 보험업감독규정, 본문: the 저축성보험 / 연금보험 classes of 제1-2조, and the
  **기준연령 요건**, whose annuity limb takes the mid-point of the issue-age range.
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the reserve taxonomy.
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart elsewhere in this repository.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당): cited once, no participating
  즉시연금 rate scale having been retrieved and the composite being 무배당.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS**): the solvency layer the key sensitivities are
  ordered against. (Article text; 별표 22 not retrieved — see REG-R26.)
- **REG-R16** — 감독규정 제7-60조 (생명보험 상품설계): **제10호**, making a 최저보증이율 or
  최저보증금액 compulsory on a 금리연동형보험 — why the floor exists at all; and **제7호 and
  제9호**, whose exceptions for annuities in payment are why the 사망보험금 here may be 10%.
- **REG-R18** — 감독규정 제7-64조·제7-65조: the **공시이율 chain**, 제7-65조제3항 making the
  declared rate a 공시기준이율 times a 조정률 — why `decl_rate` is a scalar.
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): 제1항제1호, the 해약환급금 as the
  계약자적립액 less the 해약공제액; and 제5항, for the absence of unearned premium here.
- **REG-R20** — 감독규정 [별표 14] 표준해약공제액: the cap on the surrender charge, which
  **binds nothing here**, the published 해약공제액 run being a run of zeros.
- **REG-R22** — 감독규정 제4-32조 등: the standard for the recovery period of 모집수수료, whose
  single-premium limb makes a first-year-only commission unremarkable.
- **REG-R23** — 보험업감독업무시행세칙: the 공시이율 **product-class list**, on which 연금보험
  is one class — so an insurer may not declare a different rate here than on its other annuity
  business.
- **REG-R24** — 시행세칙 [별표 27] 공시기준이율 산출 기준: `외부지표금리 × α + 운용자산이익률 ×
  (1 − α)` with α ≤ 60%, i.e. **majority-weighted to the insurer's own realised return** — the
  strongest single reason no model here derives a Korean declared rate.
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: cited by article — **제21조 (보험나이)**, the
  age basis of the whole model; 제17조; and **제26조·제27조 (납입최고, 부활)**, for the
  negative finding that neither can operate on a single premium.
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금): **Retrieved: no.** Known
  only at second hand, and the two sentences in `technical-notes.md` reaching them carry
  [unverified].
- **REG-R27** — 제4차 보험개혁회의 보도자료: the supervisory discount curve and the state of
  the 계리가정 guidelines — the layer `disc_factor` is **not**.
- **REG-R32** — 예금보호한도 1억원 (2025-09-01): the increase from ₩50,000,000, which bites
  harder here than elsewhere, a single premium being able to exceed it twentyfold on day one.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported: the 평균수명 and **65세 기대여명**,
  the third fit constraint of `mort_table.csv`. **The table itself is not published.**
- **REG-R34** — 보험개발원 public channels: the evidence that KIDI releases summary statistics
  and not the table — what makes every krlib `mort_table.csv` a [std] construction.
- **REG-R38** — 국가데이터처 생명표: the public **완전생명표** anchor on 만나이, and the 65세
  기대여명 of 19.5 / 23.7 years against which the table's selection gap is measured.
- **REG-R39** — KOSIS 완전생명표: the to-do behind the table-build note, and the second half of
  the 만나이 / 보험나이 warning.
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier disclosure: the **평균공시이율 series**,
  which makes the adopted 2.50% the 2026 supervisory average, not one carrier's 2017 rate.
- **REG-R49** — 상법 제4편 제1장 통칙: 제638조의3 (명시·설명의무), the provision the
  determination and the judgment both turn on; and 제662조, the three-year prescription.
- **REG-R50** — 상법 제4편 제3장 인보험: **제727조제2항, added in 2014**, the first provision
  of Korean insurance law to contemplate an income stream.
- **REG-R51** — 금융소비자 보호에 관한 법률 제46조: the 15-day / 30-day 청약철회 pair.
- **REG-R52** — 예금자보호법 시행령 제18조제7항: the ₩100,000,000 limit per person per insurer
  from 2025-09-01, protected on the 해약환급금 measure.
- **REG-R56** — 소득세법 제59조의3 등 (연금계좌): the **3% 종신계약 rate** and the 연금수령
  conditions — the regime an 즉시연금 written as an ordinary 저축성보험 is **outside**.
- **REG-R57** — 소득세법 제59조의4 (보장성보험료 세액공제): the boundary this product sits on.
- **REG-R58** — 소득세법 제16조제1항제9호 and 시행령 제25조: **the tax provision that shapes
  the product** — the ten-year route with its ₩100,000,000 cap from 2017-04-01, exactly the
  anchor's premium, and 제25조제4항's conditions for a 종신형 연금보험, of which 제3호's
  guarantee-within-기대여명 test is written into [S5]'s design.
- **REG-R59** — 상속세 및 증여세법 제8조·제34조: the estate treatment of an annuity in payment,
  behind the 국세청 예규 at [R26].
- **REG-R60** — K-IFRS 제1117호 (IFRS 17): the measurement basis this projection feeds.

---

## Provenance note

Every entry above traces to `_research/immediate-annuity.md`, the citation ground truth for
this product: the S# and R# numbering used here is that file's numbering, unchanged, and it is
**never renumbered** because these documents cite against it. **The research file's own
numbering is not this one's** — it runs to S15 and R31 and carries S15, R7, R8, R9, R10, R15,
R20 and R30, which this file omits as uncited, for the reasons given at the head of this page.
Omission is not renumbering: the gaps stay.

What lives there and not here: the per-document extraction record; the full 예상연금액 tables
from [S2] through [S5] and the annuity factors derived from them; the reproduction of the
만기보험금 지급재원 arithmetic against the disputed contract's own published annuity levels;
the twelve-point chronology of the dispute with its per-carrier aggregates; the 공시이율
observation series and the three carrier weightings side by side; the 최저보증이율 schedules
by vintage; the tax and estate material in full; the 보험나이 rule and the issue-age, premium
and market-size envelopes; and the register of fetch failures.

That register is the part a reader checking this page should know about: the **보험업감독규정
article text**, which no route returned [R31]; the **제10회 경험생명표 itself**, not published
at all and reaching this library only through trade press [REG-R33] [REG-R34]; **no filed
산출방법서 for an 즉시연금**, so no annuity formula here was read from a basis document; **no
carrier-published annuity factor**, so the life shape's factor is checked instead through the
two shapes that carry no mortality; **no surrender rate for 즉시연금 at all**; **no expense
rate other than [S1]'s**; the full 이유 of the Supreme Court judgment, which none of the three
mirrors reproduced [R6]; the 경향신문 first-instance report, whose URL no longer resolves; and
that **no currently marketed product bearing the name 즉시연금 was located** at a major
carrier, which is why the specification is written to the mechanism.

The cross-product regulatory bibliography lives in
`references/regulatory-and-actuarial-references.md`, with its own research provenance in
`_research/regulatory-actuarial.md`. Neither is renumbered by anything on this page.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-immediate_annuity-r1
[R11]: #krlib-immediate_annuity-r11
[R12]: #krlib-immediate_annuity-r12
[R13]: #krlib-immediate_annuity-r13
[R14]: #krlib-immediate_annuity-r14
[R16]: #krlib-immediate_annuity-r16
[R17]: #krlib-immediate_annuity-r17
[R2]: #krlib-immediate_annuity-r2
[R21]: #krlib-immediate_annuity-r21
[R22]: #krlib-immediate_annuity-r22
[R25]: #krlib-immediate_annuity-r25
[R26]: #krlib-immediate_annuity-r26
[R27]: #krlib-immediate_annuity-r27
[R28]: #krlib-immediate_annuity-r28
[R29]: #krlib-immediate_annuity-r29
[R3]: #krlib-immediate_annuity-r3
[R31]: #krlib-immediate_annuity-r31
[R5]: #krlib-immediate_annuity-r5
[R6]: #krlib-immediate_annuity-r6
[REG-R1]: #krlib-reg-r1
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R2]: #krlib-reg-r2
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R52]: #krlib-reg-r52
[REG-R58]: #krlib-reg-r58
[REG-R59]: #krlib-reg-r59
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
