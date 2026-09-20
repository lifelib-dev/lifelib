# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/indemnity-medical.md`, the
citation ground truth for this product, and are **frozen — never renumber**. Numbering is
per product: `S1` in this file is a different document from `S1` in every other product's
`sources.md`, and the cross-product `references/regulatory-and-actuarial-references.md` runs
its own frozen R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read
across.** The sharpest instance is right here: this file's **[R19]** is
보험업감독규정 **제7-63조** (retrieved only in a superseded vintage), while the library's
**[REG-R19]** is 감독규정 **제7-66조 이하 (해약환급금)** and its **[REG-R17]** is the
제7-63조 entry that *was* retrieved in full. Where the two appear together — and they do,
repeatedly — that is deliberate corroboration and not redundancy. Access date for every
entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a primary product document. **On this product that phrase means something it
  does not mean anywhere else in the repository.** The benefit definition of a Korean 실손
  contract is not written by a carrier: it is the **표준약관** (*pyojun yakgwan*, standard
  policy conditions) annexed to the 보험업감독업무시행세칙 at 별표 15 under 제5-13조제1항, so
  [S1] is published subordinate legislation and every co-payment percentage, deductible,
  sub-limit, count cap, renewal corridor and rating band in the specification is a **clause
  reference** rather than a market observation. The carrier documents [S3] [S4] [S5] supply
  what the 표준약관 does not — the 보험가입금액 menu actually sold, the 가입나이 envelope,
  the confirmation that there is no 해약환급금 — and the two association disclosures [S6]
  [S7] the price and loss-ratio outturn.
- **[R#]** — a regulatory, supervisory or actuarial reference only this product needs. Twelve
  of the nineteen are 금융위원회 or 금융감독원 보도자료, which for 실손의료보험 are not press
  coverage but the **operative record**: the generation launches, the 할인·할증 commencement,
  and the annual 사업실적 that is the only published experience statement for this line.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Unused sources are omitted, so the [R#] scheme has one gap.** `R18`, 금융위원회's
「실손보험 개혁방안 주요 정책문답」 (2025-04), is retrieved in the research file but is cited
by none of the three product documents: everything they take from the reform package — the
중증/비중증 boundary, the timetable, the industry profit decomposition — is carried by [R4]
and [R5], retrieved as complete PDFs where `R18` was read only as a page body. Nothing was
newly retrieved at drafting and **no tag was added or dropped** in writing `model.md`.

**Two retrieval facts govern how much of this product is [std], and both are positive
findings rather than fetch failures.** 보험개발원 is the statutory 보험요율 산출기관 [REG-R4]
and the 장기손해보험 참조순보험요율 it publishes covers 일반상해, 교통상해, 질병 사망률,
후유장해, 입원율, 암 발생률, 비용손해, 재물손해 and 배상책임 — **실손의료보험 is not among
them** [R20] [REG-R61]; and the 산출방법서 in which an insurer's 예정위험률 and 예정사업비율
live is a 기초서류 filed under 보험업법 제5조제3호 and never published [REG-R2]. There is
therefore **no public Korean indemnity-medical morbidity or severity basis at all**, and
that — not an unopened document — is why every frequency, severity, persistency and expense
parameter here is [std].

Company and branded product names appear in this file and in
`_research/indemnity-medical.md` and nowhere else in the library: in the three product
documents a carrier is its tag alone, so a reader can always resolve who said what — here —
and never has to.

---

## Primary product sources

Seven documents. Two are the supervisor's own **표준약관** — the 4세대 wording this product
models [S1] and the 5세대 wording that replaced it [S2] — and they are why this product's
contractual half is sourced clause by clause. Three are carrier 약관 or 상품요약서, one from
each adjacent generation [S3] [S4] [S5]. Two are 손해보험협회 statutory disclosures [S6]
[S7], reached through `kpub.knia.or.kr` [REG-R62] and not the 생명보험협회 portal, because
**the non-life market is the larger one for 실손**.

**No age × sex premium scale for 4세대 or 5세대 was obtained from any source**, a gap
recorded at [S6], [S7] and in the provenance note. The one published premium the model
calibrates on — ₩11,982 a month for a 40세 남자 — comes from a 보도자료 [R1].

(krlib-indemnity_medical-s1)=

### S1 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2021.7.1. 시행), 실손의료보험 부분 (standard policy conditions)

- Exact titles of the two wordings used: 「기본형 실손의료보험(급여 실손의료비)」 and
  「실손의료보험 특별약관(비급여 실손의료비)」
- Publisher: 금융감독원 (Financial Supervisory Service), annexed to the
  보험업감독업무시행세칙, 제5-13조제1항 관련
- Document: `[별표15]표준약관(제5-13조제1항관련)(보험업감독업무시행세칙)_.hwp`, posted to the
  금융감독원 「금융상품 표준약관」 board 2021-06-30, effective 2021-07-01; it carries all ten
  standard wordings
- Doc type: **표준약관** — supervisor-issued standard policy conditions. A carrier's own 실손
  wording reproduces this text; there is no carrier discretion over the benefit definition,
  only over 보험가입금액 selection, distribution and price.
- URL (post): `https://fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=21943`
- URL (file): `https://fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=1bc99b030d0c1dd46147a7615005dcd6&fileSn=1&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (1.1 MB HWP5; the OLE compound file's
  `BodyText/Section0` stream was inflated and the `HWPTAG_PARA_TEXT` records decoded to
  375,277 characters of UTF-16 text, of which the 실손의료보험 sections occupy 66,471. Tables
  extracted as flattened cell sequences, cell-to-column association reconstructed by eye; the
  inline figures and 보상기간 diagrams are drawing objects and did not extract)
- **This is the 4세대 contract itself, and the single most load-bearing document in this
  product** — cited 152 times in `product-spec.md` and 82 in `technical-notes.md`. Everything
  contractual rests on it: 기본형 (급여) 보장종목 상해급여형 / 질병급여형, the 입원 80%
  reimbursement and the 통원 deductible `max(₩10,000 clinic / ₩20,000 hospital, 20%)`
  (제3조 <표1>); 제5조 with its ₩50,000,000 annual 보험가입금액 per 보장종목, its ₩200,000
  per-visit cap and the **연간 200만원 급여 입원 자기부담 상한** (제5조제4항); the
  본인부담상한제 exclusion at 제4조제3항제1호 and 제5조제3항 that truncates the 급여 claim;
  제21조 보험나이; 제23조 재가입; and 제30조 the **±25% renewal corridor**, whose printed
  illustration 14,000 → 18,200 → 23,660 → 30,758 → 39,985 → 51,980 fixes `age_load = 0.04`
  and proves the corridor applies to the **age-adjusted** prior premium. On the 특별약관
  side: 상해비급여형 / 질병비급여형 / **3대비급여형**, the 입원 70% and the 상급병실료 50%
  capped at a ₩100,000 **daily average**, 통원 `max(₩30,000, 30%)` with a 100-visit cap, the
  three sub-limits with their counters and the 10-visit re-assessment rule, the
  항암제·항생제·희귀의약품 carve-out at 제3조(3)제2항, the asymmetric act-counting rules at
  제3조(3)제4항, and **제6조, the 요율 상대도** — five bands, the ₩1,000,000 surcharge floor,
  the 산정특례 and 장기요양 1·2등급 exemptions, and the neutrality requirement
  「상대도 적용 전·후의 총 보험료 수준이 일치하도록」 from which `reld_solved(y)` is solved.

(krlib-indemnity_medical-s2)=

### S2 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2026.5.6. 시행), 실손의료보험 부분 (standard policy conditions, 5세대)

- Exact titles of the three wordings used: 「기본형 실손의료보험(급여 실손의료비)」,
  「실손의료보험 특별약관1(중증 비급여 실손의료비)」 and
  「실손의료보험 특별약관2(비중증 비급여 실손의료비)」
- Publisher: 금융감독원
- Document: `[별표 15] 표준약관(제5-13조제1항관련)(보험업감독업무시행세칙).hwp`, posted
  2026-06-15, stated 「'26.5.6. 시행」
- Doc type: 표준약관 — **the 5세대 contract**
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=218364`
- URL (file): `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=29447dbe2fa84d85881c10281c6b9d38&fileSn=1&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (1.6 MB HWP5, same decoding route, 449,304
  characters; the 실손 sections run 187,870–288,762)
- The live market, and the direction of travel against which the modelled generation is
  read. It establishes the 5세대 rewrite that `product-spec.md` sets out in *The 5세대
  deltas*: the 기본형 통원 deductible becoming
  `max(₩10,000 or ₩20,000, 20%, 보장대상의료비 × 건강보험 본인부담률)`, with the 본인부담률
  defined **arithmetically inside the wording**; 임신·출산 (O00–O99) and 정신발달장애
  (F80–F89) brought into cover; **특별약관1 (중증 비급여)** restricted to 산정특례 대상 질환
  with a ₩5,000,000 annual co-payment cap on 상급종합·종합병원 inpatient treatment; and
  **특별약관2 (비중증 비급여)** at 50% co-payment, a ₩10,000,000 annual limit, ₩200,000 per
  **day** rather than per visit for 100 days, and the outright exclusion of 근골격계
  이학요법치료, 체외충격파치료 and 주사료 — the classes this model prices as
  `claims_np_three`. The 요율 상대도 table carries over unchanged into 특별약관2, which is
  why the experience-rating loop survives the generation change though the benefit does
  not.

(krlib-indemnity_medical-s3)=

### S3 — 무배당 삼성화재 다이렉트 실손의료비보험(2605.1) 보험약관 [계약전환용] (carrier policy conditions, 5세대)

- Publisher: 삼성화재해상보험주식회사 (Samsung Fire & Marine Insurance)
- Document: 보험약관, 155 pp., cover marked `2605.1` (2026-05 edition); PDF metadata created
  2025-10-27, modified 2025-12-03
- Doc type: 약관 + 약관요약서 (policy conditions with the mandatory visual summary)
- URL: `https://direct.samsungfire.com/docs/realloss.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (2.4 MB PDF, 157 pages of extractable text,
  291,848 characters; the 요약서 infographics are images, their captions only partly
  extracted)
- A **carrier implementation**, in the 계약전환 (conversion) form, and the source of what
  the 표준약관 does not say. It establishes: the menu of selectable 보험가입금액
  (₩50,000,000 / ₩30,000,000 / ₩10,000,000 with the per-visit cap stepping ₩200,000 /
  ₩150,000 / ₩100,000), which makes model point 7's lower rung a *sourced* configuration;
  the statement that the contract is **1년만기 순수보장성 with no 해약환급금** — the single
  citation behind the absence of `cv_pp`, `claims_lapse`, 보험계약대출 and
  보험료 자동대출납입, and behind the 표준해약공제액 machinery of [REG-R19] [REG-R20] not
  engaging at all; the **10% 무사고 할인** and its exact scope, which is why `noclaim_disc`
  applies to the whole office premium and not only to the rider; a 5% discount for
  의료급여 수급권자, excluded from the composite as **[std scope]**; the 재가입 rules
  (변경주기 최대 5년, 재가입 나이 최고 99세, cover to the 보험나이 100세 계약해당일) behind
  `reentry_period = 5` and `max_cover_age = 100`; the 계약중지·재개 machinery; and the
  **2028-05-06** commencement of the 차등제 on 5세대 business.

(krlib-indemnity_medical-s4)=

### S4 — 무배당 삼성화재 다이렉트 실손의료비보험(1307.1) 1종(표준형) 상품요약서 (statutory product summary, 2세대)

- Publisher: 삼성화재해상보험주식회사
- Document: 상품요약서, 20 pp., 2013-07 edition
- Doc type: 상품요약서
- URL: `https://www.anycardirect.com/docs/realloss_sum.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (221 KB PDF, text extracted cleanly)
- A **2세대 (표준화실손)** document, and the only retrieved source that states a **가입나이**
  range at all — 0–49 on this direct-channel product, the observed anchor under the
  composite's **[std]** 0–65 envelope. It also sets out the pre-2017 renewal architecture —
  보험기간 1년, 자동갱신 최고 14회, 보장내용 변경주기 **15년**, 재가입 나이 15–99, cover to
  the 보험나이 100세 계약해당일 — which makes the 4세대 shortening to five years legible as a
  supervisory decision rather than a drafting detail. It carries the 입원 80% rule and the
  **연간 200만원** inpatient cap in a 2세대 wording, corroborating [S1 제5조제4항], and the
  하나의 상해당 최초입원일부터 365일 rule.

(krlib-indemnity_medical-s5)=

### S5 — 무배당 프로미라이프 실손의료비보험2101 (DB손해보험) 보험약관 (carrier policy conditions, 3세대)

- Publisher: DB손해보험주식회사
- Document: 보험약관, 108 pp., edition `2101` (2021-01)
- Doc type: 약관 + 약관요약서
- URL: `https://www.idbins.com/pcweb/bizxpress/pdc/hc/__etc/실손의료비보험2101.pdf`
  (percent-encoded form used for retrieval)
- Accessed: 2026-09-03, Retrieved: **yes** (4.8 MB PDF, 154,558 characters extracted)
- A **3세대** carrier document — the generation immediately before the model's — whose
  약관요약서 states the 3세대 deductible set verbatim: 질병통원(외래)
  `max(병원별 공제금액 1~2만원, 20%)`, 질병통원(처방조제비) `max(₩8,000, 20%)`, and the three
  비급여 특약 items at `max(₩20,000, 30%)`, the direct predecessor of the 4세대
  `max(₩30,000, 30%)`. That is what lets `product-spec.md` show the deductible ratcheting
  generation by generation rather than assert it. It also carries the 자동갱신 / 재가입 clause
  structure 4세대 inherits — the basis, with [S3], for the statement that **the policyholder
  may decline a renewal and the insurer may not**, which is why `renewal_decline_rate` is a
  decrement of its own.

(krlib-indemnity_medical-s6)=

### S6 — 손해보험협회 공시실, 「실손의료보험 보험료 인상률 및 손해율 공시」 (statutory disclosure)

- Publisher: 손해보험협회 (General Insurance Association of Korea), 공시실
- Doc type: 공시자료 (statutory public disclosure)
- URL: `https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthIncreaseRate.do`
- Accessed: 2026-09-03, Retrieved: **in part** (the page structure, the insurer list, the
  disclosed definitions and one worked row were read; the full grid renders client-side and
  could not be paged through by a plain fetcher)
- The disclosure that makes carrier-level variation *measurable* — 10 손해보험사 and 7
  생명보험사, three years of 보험료 인상률 and three of 경과손해율, split 상해 / 질병 / 합계.
  Its definitions are exact and quoted in `product-spec.md`: 인상률 is 「직전연도말 대비
  4세대 실손의료보험의 남여 각 연령별 영업보험료 인상률에 해당 성별 연령의 직전연도
  보험료수익 비중을 곱하여 산정」 — a premium-weighted average over the age × sex rate scale,
  the disclosure's own confirmation that such a scale exists — and 손해율 is
  「발생손해액/경과보험료」. One row read in full: 메리츠화재 상해담보, 인상률 2026 **21.8%**
  and 2025 **23.9%**, 경과손해율 2025 **117.2%** and 2024 **130.1%**. **It is also the record
  of a gap:** the grid could not be paged, so no age × sex scale was obtained from it.

(krlib-indemnity_medical-s7)=

### S7 — 손해보험협회 공시실 — 「실손의료보험 안내」, 「실손의료보험(5세대)」, 「보험료 비교공시」 (consumer disclosure)

- Publisher: 손해보험협회, 공시실
- Doc type: 공시자료 (consumer-facing product disclosure)
- URLs: `https://kpub.knia.or.kr/pdic/mins/MinsInf.knia` ;
  `https://kpub.knia.or.kr/productDisc/lostHealth/lostHealth5thStandard.do` ;
  `https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthDisclosure.do`
- Accessed: 2026-09-03, Retrieved: **in part** (the descriptive pages returned text; the
  premium comparison grid is a POST-driven form and returned 「조회된 내용이 없습니다」 to a
  plain fetcher)
- The association's own restatement of the 5세대 deductible formula — 입원
  `보장대상의료비 × 20%`, 통원 `Max[보장대상의료비 × 건강보험본인부담률, 보장대상의료비 ×
  20%, 1만원(병·의원) 또는 2만원(상급종합·종합병원)]` — and the 5세대 annual limits,
  corroborating [S2] from a second publisher. Its comparison tool confirms the three marketed
  families (**표준화 / 노후 / 유병력자**) and is filtered by **성별 and 보험나이**, which is
  the disclosure's own confirmation that the rate scale is an age × sex table on 보험나이 —
  and therefore that the model's 만나이 basis differs from the pricing basis by construction.
  Like [S6] it is cited as a **gap**: the grid returned nothing to a plain fetcher, so the
  nine non-anchor model points' premiums are **[std]** rather than disclosed.

---

## Regulatory and actuarial references

Twenty entries in the research file; nineteen are cited here. Twelve are 금융위원회 or
금융감독원 보도자료 [R1]–[R8] [R13] [R14] [R16] [R17], which on this product carry the
operative record rather than commentary. Three describe the public layer the contract sits
on top of [R9] [R10] [R11]. One is a 보험연구원 seminar deck [R12], the only retrieved source
for several distributional facts the model's shape tables are calibrated on. One is the
supervisory regulation itself [R19], retrieved only in a superseded vintage. And one is the
negative result that fixes the whole model's basis boundary [R20].

(krlib-indemnity_medical-r1)=

### R1 — 금융위원회 외, 「7.1일부터 제4세대 실손의료보험이 출시됩니다」 (2021-06-30) (press release)

- Publisher: 금융위원회, joint with 금융감독원 and both trade associations
- Document: 보도자료, 배포 2021-06-29, 보도 2021-06-30 조간, 10 pp.
- URL (post): `https://www.fsc.go.kr/no010101/76157`
- URL (file): `https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=76157&fileTy=ATTACH&fileNo=2`
- Accessed: 2026-09-03, Retrieved: **yes** (438 KB PDF, 10 pp., 7,953 characters; all
  substantive tables extracted as machine-readable text)
- **The founding document of the modelled generation**, and the source of the one number the
  whole model calibrates on. It recites the design intent, the 급여/비급여 split, the
  co-payment and deductible increases, the shortening of the 재가입주기 from 15 to 5 years,
  the five-band 차등제 with its thresholds and its 「5% 내외」 discount — the upper half of the
  range behind `reld_disc_cap = 0.05` — the **10% 무사고 할인** and the launch carrier list.
  Its most useful item is a published **40세 남자 monthly premium comparison across all four
  generations** at 2021-06, from which the anchor cell's **₩11,982** comes and against which
  every frequency in `utilisation_table.csv` is solved. It also carries the tail statistic —
  0.005% of insureds above ₩50,000,000 of claims in 2019 — that `model.md` cites for why the
  annual limits read slack on an expected-value grid.

(krlib-indemnity_medical-r2)=

### R2 — 금융위원회 외, 「「4세대 실손의료보험 출시」 관련 주요 FAQ」 (2021-06) (FAQ annexed to R1)

- Publisher: 금융위원회 외 3
- Document: 12 pp., 2021-06
- URL: `https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=76157&fileTy=ATTACH&fileNo=4`
- Accessed: 2026-09-03, Retrieved: **yes** (654 KB PDF, 12 pp., 6,619 characters; the two
  심평원 screenshot figures did not extract)
- The **arithmetic** of the 차등제 stated as a formula, and four facts the model could not
  be built without: that the experience record **resets annually**
  (「보험금 지급(사고) 이력이 1년마다 초기화됩니다」), which is why `band_share(y, b)` reads
  only year `y − 1` and there is no bonus-malus chain; that the surcharge falls on the
  **rider premium alone** (「비급여 특약 보험료만 할증되며…」), which is why `reld_avg(y)`
  multiplies `prem_np_base(y)` and not `prem_gross_mth(y)`; that the 비급여 특약 is about
  **60% of the total premium**, which is `np_share = 0.60`; and the 도수치료 **10-visit
  re-assessment rule**, which `physio_cont_prob = 0.60` stands in for. It also carries the
  worked 45-year-old-male example — the policyholder cutting his claims 93% under a surcharge
  — that `model.md` names as the behavioural response the model does **not** capture, and the
  도수치료 price range **₩5,000–₩600,000** that justifies `severity_table.csv` existing.

(krlib-indemnity_medical-r3)=

### R3 — 금융위원회, 「'24.7.1일부터 4세대 실손의료보험은 비급여 이용량에 따라 비급여 보험료가 할인 또는 할증됩니다」 (2024-06-07) (press release)

- Publisher: 금융위원회
- Document: 보도자료, 2024-06-07
- URL: `https://www.fsc.go.kr/no010101/82406`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read; the attached PDF was not
  separately opened)
- The commencement of the **비급여 할인·할증 on 2024-07-01**, three years after launch, which
  is `reld_start_year = 4`. It gives the five bands with the **−5% (잠정)** discount factor —
  the lower half of the range behind `reld_disc_cap` — and the +100% / +200% / +300%
  surcharges; the exemptions (산정특례대상질환; 장기요양 1·2등급 판정자) behind
  `reld_exempt_share`; and a **band distribution at commencement, 1등급 62.1 / 2등급 36.6 /
  3등급 1.3**. That is *not* the distribution `claim_shape_table.csv` is calibrated to: the
  five-band set 72.9 / 25.3 / 0.8 / 0.7 / 0.3 is [R12]'s, attributed there to a 금융감독원
  release of 2024-01-19, and the two published sets disagree. This entry is cited beside
  [R12] wherever the sensitivity matters, because on this release's own three-band mix the
  same neutrality identity gives `r₁ = 0.9791` — a 2.1% discount against [R12]'s 4.25%.

(krlib-indemnity_medical-r4)=

### R4 — 금융위원회, 「실손의료보험, 낮은 보험료로 정말 필요할 때 도움되는 보험상품으로 재탄생합니다」 (2025-04-01) (press release)

- Publisher: 금융위원회 (보험과)
- Document: 보도자료, 2025-04-01 — the **실손보험 개혁방안** that became 5세대
- URL: `https://www.fsc.go.kr/no010101/84272`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read; attachments not separately
  opened)
- The reform's baseline statistics, which are the market context in `product-spec.md`:
  **4천만명** insured at 2024-12-31; about **1.6천만건** of policies with **no 약관변경(재가입)
  clause at all**; national medical spend ₩133조 of which 실손 bore ₩14.1조 (10.6%) in 2023;
  the premium increase series **2022 14.2% → 2023 8.9% → 2024 1.5% → 2025 7.5%**; and the
  concentration statistics — **9% of policyholders take 80% of claims, 65% take none** — which
  are why `utilisation_table.csv` holds frequencies averaged over a population that mostly
  claims nothing, and why a single average cell cannot show what the experience rating does.

(krlib-indemnity_medical-r5)=

### R5 — 금융위원회·금융감독원, 「5월 6일부터 … 5세대 실손의료보험이 새롭게 출시·판매됩니다」 (2026-05-06) (press release)

- Publisher: 금융위원회 (보험과) and 금융감독원 (보험상품분쟁2국), joint with both trade
  associations
- Document: 보도자료, 배포 2026-05-04, 보도 2026-05-06 조간, 15 pp.
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217561&menuNo=200218`
- URL (file): `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa16ababffbc45d1be8ed764aa9cec3b&fileSn=2&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (655 KB PDF, 15 pp., 13,903 characters; 참고1's
  4세대-versus-5세대 comparison table extracted in full)
- 참고1 of this release is **the only retrieved document that states the complete 4세대 limit
  and sub-limit set in one place**, which is why it is cited beside [S1] throughout the
  benefit provisions: it corroborates the ₩50,000,000 annual limit, the ₩200,000 per-visit
  cap, the ₩2,000,000 inpatient co-payment cap and all three 3대비급여 money and count caps
  from a second publisher. It also gives the 5세대 premium effect (−30% against 4세대) and
  the 계약재매입 and 선택형 할인 schemes commencing 2026-11 for the ~47.5% of in-force
  policies written before 2013-03 with no re-entry clause.

(krlib-indemnity_medical-r6)=

### R6 — 금융위원회·금융감독원, 「5세대 실손보험 Q&A」 (2026-05) (annex to R5)

- Publisher: 금융위원회·금융감독원, 별첨1 to [R5]
- URL: `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa16ababffbc45d1be8ed764aa9cec3b&fileSn=3&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (104 KB HWP5, decoded to 8,598 characters; the
  table-of-contents page numbers extracted with control-character noise, the body is clean)
- Fifteen Q&As, four of which matter here: the four permitted **가입 유형** (주계약 alone;
  +특약1; +특약2; +both), the structure model points 5 and 6 exercise; a four-row table of the
  국민건강보험 cost-sharing taxonomy (급여 / 선별급여 / 관리급여 / 비급여) with co-payment
  ranges, where the 급여/비급여 boundary is pinned; the 2025 claim mix — **비급여 근골격계
  물리치료 + 주사제 27.3%**, 암 관련 12.8% — which bounds the 3대비급여 share; and that the
  renewal increase is **capped at 25% a year per risk cell**, corroborating [S1 제30조].

(krlib-indemnity_medical-r7)=

### R7 — 금융감독원, 「2025년 실손의료보험 사업실적(잠정)」 (2026-06-04) (annual experience statement)

- Publisher: 금융감독원 보험상품분쟁2국 보험상품제도팀
- Document: 보도자료, 배포 2026-06-02, 보도 2026-06-04 조간, 8 pp.
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=218168&menuNo=200218`
- URL (file): `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=cbd3c2989cfa4a71a8b2eeba98817866&fileSn=2&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (810 KB PDF, 8 pp., every numeric table extracted
  as machine-readable text; two bar charts are images whose axis labels did not extract)
- **The single most important experience source for this model**, cited 44 times in
  `product-spec.md`. In-force counts by generation (36.22 million individual policies at
  2025-12-31); premium income ₩18.0조 against ₩17.0조 of claims; claims split 급여/비급여 with
  the **57.1% 비급여 share**; 경과손해율 overall and by generation, including 4세대 at
  **115.1%** in 2025 against a stated break-even of 「약 85% 수준」; **손해조사비 plus
  사업비 of about ₩2.9조 — 16.1% of premium**, the one published expense datum, and the
  aggregate `check_expense_split()` ties the 6 / 7 / 3 split back to; claims by treatment
  category, including the 15.0% attributable to 암 and 뇌·심혈관질환 that anchors
  `reld_exempt_share`; the **3.3% fall in the 1–3세대 in-force block** in 2025, the only
  실손-specific persistency figure in existence and the anchor for both `lapse_table.csv` and
  `renewal_decline_rate`; and the supervisory programme for 2026 including the 4세대 재가입
  conversion wave from 2026-07.

(krlib-indemnity_medical-r8)=

### R8 — 금융감독원, 「2024년 실손의료보험 사업실적(잠정)」 (2025-05-13) (annual experience statement)

- Publisher: 금융감독원 보험계리상품감독국 보험상품제도팀
- Document: 보도자료, 배포 2025-05-12, 보도 2025-05-13 조간, 7 pp.
- URL (original post):
  `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=193952&menuNo=200218`
- URL (retrieved copy): `https://kiri.or.kr/PDF/weeklytrend/20250526/trend20250526_4.pdf`
- Accessed: 2026-09-03, Retrieved: **yes, but through a reproduction** — read from
  보험연구원's 「주간 트렌드」 republication of the 금융감독원 release (1.8 MB, 7 pp.,
  extracted in full); the 금융감독원 posting was in the board index but its attachment was not
  downloaded. The reproduction is verbatim, carries the original 보도/배포 dates and 담당부서
  block, and reconciles with [R7]'s prior-year columns, so it is treated as retrieved with
  the route recorded.
- The 2024 counterpart of [R7], plus two things [R7] does not repeat and the model needs: the
  **세대별 비급여 자기부담률 and per-policy 비급여 claim table** (1세대 through 4세대,
  inpatient and outpatient), which lets `product-spec.md` show the co-payment ratcheting
  across generations; and the **세대별 월납보험료 series 2021–2024** for a 40대 남자 at a
  손해보험사, the only multi-year premium series retrieved. It is also the source of the
  ₩2.81조 — **18.5% of all 2024 claims** — attributable to non-covered injections, which makes
  `inject_carve_share = 0.25` a first-order calibration question rather than a detail.

(krlib-indemnity_medical-r9)=

### R9 — 국민건강보험공단, 「2024년 건강보험 보장률 64.9%」 (2025-12-30) (official statistics)

- Publisher: 국민건강보험공단 비급여관리실 보장성평가센터
- Document: 보도자료, 14 pp., reporting the 「2024년도 건강보험환자 진료비 실태조사」
- URL (retrieved copy): `https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf`
- Accessed: 2026-09-03, Retrieved: **yes**, again through the 보험연구원 「주간 트렌드」
  reproduction (1.3 MB, 14 pp., 18,385 characters; all tables extracted, the two trend charts
  as loose number sequences). The 국민건강보험공단 original posting was not located directly.
- **The layer underneath the product.** 건강보험 보장률 **64.9%** for 2024 with 법정
  본인부담률 19.3% and 비급여 본인부담률 15.8%; national treatment cost ₩138.6조 split
  보험자부담금 ₩90.0조 / 법정본인부담금 ₩26.8조 / 비급여진료비 ₩21.8조. Two of its quantities
  go straight into the model: the **2024 growth rates by component — scheme outlay 4.3%,
  statutory co-payment 1.0%, 비급여 8.1%** — which are `med_trend_ge` and `med_trend_np` and
  therefore the whole re-rating rule; and the **coverage ratios by provider type and age
  band**, which are the [std] shape of the age curves in `utilisation_table.csv`. It also
  carries a 비필수항목-adjusted coverage ratio that removes 도수치료, 영양주사, 상급병실료 and
  제증명수수료 — the same items the 실손 reforms target and this model sub-limits.

(krlib-indemnity_medical-r10)=

### R10 — 국민건강보험공단, 「본인부담상한제」 (statutory scheme description)

- Publisher: 국민건강보험공단
- Doc type: statutory scheme description with the year-by-year threshold table
- URL: `https://www.nhis.or.kr/nhis/minwon/wbhapa01000m01.do?mode=view&articleNo=10946900`
- Accessed: 2026-09-03, Retrieved: **yes**
- The definition — 「연간 요양기관에 지출한 본인부담금이 개인별 상한액을 초과할 경우 초과액을
  공단이 부담」, operated as 사전급여 and 사후환급 over the **calendar** year — and the
  income-decile threshold table for 2023–2026. **This is a hard cap on the 급여 half of the
  실손 claim**, because [S1 제4조제3항제1호] excludes from cover any amount refundable under
  it, and it is the only place in the library where a public scheme reaches inside a private
  contract and truncates its benefit. Its 2026 scale — ₩900,000 at 1분위 to ₩8,430,000 at
  10분위 — is transcribed row for row into `oop_ceiling_table.csv`, the **only input file
  here that is a transcription rather than a construction**, and it is what `oop_trunc(y)`
  and `check_oop_ceiling()` are computed against.

(krlib-indemnity_medical-r11)=

### R11 — 건강보험심사평가원, 「외래진료시 본인부담률 및 부담액」 (statutory cost-sharing schedule)

- Publisher: 건강보험심사평가원 (Health Insurance Review and Assessment Service, HIRA)
- Doc type: statutory cost-sharing schedule, stated as deriving from 국민건강보험법 시행령
  별표2
- URL: `https://www.hira.or.kr/dummy.do?pgmid=HIRAA030056020110`
- Accessed: 2026-09-03, Retrieved: **yes**
- The outpatient co-payment percentages by provider tier — 상급종합 / 종합병원 / 병원 /
  의원, plus the pharmacy rate — that determine the **급여 본인부담금 the 실손 reimburses in
  every generation**, and that the 5세대 wording [S2] now reads directly into its own
  deductible formula. Cited once, beside [REG-R53].

(krlib-indemnity_medical-r12)=

### R12 — 보험연구원 김경선, 「실손의료보험 현황 및 개선과제」 (2024-12-05) (research presentation)

- Seminar: KIRI 세미나 「건강보험 지속성을 위한 정책과제」
- Publisher: 보험연구원 (Korea Insurance Research Institute), presented 2024-12-05
- Document: seminar deck, 34 slides
- URL: `http://www.kiri.or.kr/pdf/세미나자료/smn_20241205_2.pdf` (percent-encoded form used)
- Accessed: 2026-09-03, Retrieved: **yes** (1.5 MB PDF, 34 pp., 12,536 characters; the charts
  are images whose data labels extracted but whose axes did not, so several series are quoted
  only where the label-to-value mapping is unambiguous from surrounding text)
- The source of the two distributional facts the model is calibrated on, and the only
  retrieved document carrying either. First, the **4세대 급여-versus-비급여 loss ratio split
  for three half-years** — 급여 97.5% and 비급여 73.0% in 2022 H1 against 154.6% and 114.2% by
  2024 H1 — which is the target the utilisation level is solved to reproduce, and which
  establishes that **the 급여 unit is the worse half**, the opposite of what the 할인·할증
  publicity implies. Second, the **distribution of claim size by generation**, which is the
  shape of the six 2단계 buckets in `claim_shape_table.csv`. It also carries the **verbatim
  text of 보험업감독규정 제7-63조제2항제6호가목** on annual rate adequacy testing — which is
  why the five-year grace that left 4세대 unable to re-rate until 2025 is cited to [R12]
  rather than to the regulation, [R19] having failed to return the current article.

(krlib-indemnity_medical-r13)=

### R13 — 금융위원회, 「'24.10.25일부터 … 실손보험 청구 전산화가 순차적으로 시행됩니다」 (2024-10-25) (press release)

- Publisher: 금융위원회 (보험과)
- URL: `https://www.fsc.go.kr/no010101/83255`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read; the attached PDF/HWP were not
  separately opened)
- The launch of **실손24**, the electronic claim channel: phase 1 (병원급 with 30 or more
  beds, plus 보건소) from 2024-10-25, phase 2 (의원·약국) scheduled 2025-10-25, and 보험개발원
  designated the statutory **전송대행기관**. Cited for the friction change and explicitly
  recorded as **not modelled**: lower claim friction is a plausible driver of future
  frequency, no published elasticity exists, and nothing in the basis is adjusted for it.

(krlib-indemnity_medical-r14)=

### R14 — 금융위원회, 「실손보험 청구 전산화가 의원·약국을 포함하여 확대 시행됩니다」 (2025-10-23) (press release)

- Publisher: 금융위원회
- URL: `https://fsc.go.kr/no010101/85456`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read)
- Phase 2 of 실손24 from 2025-10-25: the provider counts (104,541 in scope, 10,920 — 10.4% —
  connected at launch), the documents transmitted (계산서·영수증, 진료비 세부산정내역서,
  처방전) and the confidentiality constraint on the 전송대행기관. Cited with [R13] and, like
  it, recorded as a driver the model does **not** assume.

(krlib-indemnity_medical-r15)=

### R15 — 금융위원회, 「보험업법 시행령·감독규정 입법예고」 (2026-01-15) (legislative pre-announcement)

- Publisher: 금융위원회
- Document: 보도자료, 2026-01-15; 예고기간 2026-01-15 ~ 2026-02-25
- URL: `https://www.fsc.go.kr/no010101/86059`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read; the draft 개정안 attachments were
  not opened)
- Confirms the **instrument chain** this product's benefit definition hangs on: the 5세대
  상품설계기준 sits in the 보험업법 시행령 and the 보험업감독규정, with the detail delegated to
  the 시행세칙 — i.e. [S2] is the operative text and the 감독규정 [REG-R17] its enabling
  instrument. It also states the 5세대 design constraints: 급여 통원 co-payment linked to the
  건강보험 본인부담률 with a 20% floor; 중증 비급여 30% with a ₩30,000 minimum; 비중증 비급여
  50% with a ₩50,000 minimum.

(krlib-indemnity_medical-r16)=

### R16 — 금융감독원, 「최근 민원사례로 알아보는 실손의료보험 관련 소비자 유의사항」 (2026-05-19) (press release)

- Publisher: 금융감독원 소비자소통국 손해보험민원팀
- URL: `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217901&menuNo=200218`
- Accessed: 2026-09-03, Retrieved: **in part** (the page body and the attachment list were
  read; the attachments were not opened)
- Four complaint patterns, two of which bear on the model: the **개인실손 중지제도** —
  suspension while a group 실손 is in force, with resumption within one month of the group
  cover ending — which is `suspend_rate`, the fourth decrement, live on model point 9 and
  mandatory as a *facility* under 감독규정 제7-63조제2항제7호 [REG-R17]; and the **6-month
  conversion withdrawal** right. The resumption half is named in `model.md` as not modelled:
  the contract that resumes is a different projection.

(krlib-indemnity_medical-r17)=

### R17 — 금융위원회, 「(노후·유병력자) 실손보험의 가입연령과 보장연령을 확대하여 …」 (2025-02-11) (press release)

- Publisher: 금융위원회
- URL: `https://www.fsc.go.kr/no010101/83985`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML body read)
- The two adjacent families — **노후실손** and **유병력자실손** — and the 2025-04-01 widening
  of their issue and cover ages to 90. Relevant twice: [R7] reports them as a separate 2.4%
  block outside the five generations, and they carry their own co-payments, issue ages and
  **three-year** change cycles, so `product-spec.md` scopes them out explicitly. The 90-year
  issue age is the observed upper bound against which the **[std]** 0–65 envelope is set.

(krlib-indemnity_medical-r19)=

### R19 — 보험업감독규정 (금융위원회고시) 제7-63조 (제3보험의 보험상품설계 등) (financial-regulatory notification)

- Publisher: 금융위원회
- Doc type: 행정규칙 (고시)
- URLs tried: `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` ;
  `https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000235980` ;
  `https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=24827&fileTy=ATTACH&fileNo=10` ;
  `https://www.easylaw.go.kr/CSP/FlDownload.laf?flSeq=317766`
- Accessed: 2026-09-03, Retrieved: **in part, and the part that matters was not retrieved.**
  The 국가법령정보센터 pages return only the masthead and amendment metadata to a plain fetcher
  (시행 2023-03-02, 고시 제2023-10호 on one; 시행 2024-01-31, 제2024-9호 on another) — the
  article text is JavaScript-rendered. Two HWP copies were downloaded and decoded, but **both
  are a pre-2013 vintage** whose 제7-63조 has only three 호 and no 제2항 at all, so the current
  **제7-63조제2항**, where the 실손 design rules live, was not retrieved from this route.
- What *was* read is 제7-63조 as it stood after the 2011-03-22 전문개정, including
  **제1항제2호**: 「약관상 보장하는 금액은 정액 또는 실제 발생하는 손해(이하 "실손해"라 한다)를
  기준으로 설계할 것」. That single clause is the structural fact the whole product rests on —
  the branch of 제3보험 design that makes an indemnity benefit lawful, and the reason
  `Medical_KR_S` stands alone in `krlib`. Everything about the **current** 제2항 — the 5년
  재가입주기, the ±25% corridor, the 중지·재개 facility, the annual rate adequacy test — is
  cited to [REG-R17], which retrieved the article in full, and 제2항제6호가목 specifically to
  [R12], which quotes it verbatim.

(krlib-indemnity_medical-r20)=

### R20 — 보험개발원, 「장기손해보험 참조순보험요율 예시」 (reference net premium rate disclosure)

- Publisher: 보험개발원 (Korea Insurance Development Institute, KIDI)
- Doc type: 참조순보험요율 disclosure
- URL: `https://www.kidi.or.kr/user/nd13261.do`
- Accessed: 2026-09-03, Retrieved: **yes**
- **The negative result that fixes this model's basis boundary, and it is cited as such.**
  The published reference-rate categories for 장기손해보험 as applied from 2024-04-01 are
  일반상해 and 교통상해 (사망/후유장해/입원), 질병 사망률, 후유장해, 입원율, 암 발생률,
  비용손해, 재물손해 and 배상책임 — **실손의료보험 위험률 is not among them.** With the
  unpublished 산출방법서 [REG-R2] that is what makes every claim frequency, severity,
  persistency and expense parameter here [std] and constructed from the aggregate experience
  of [R7] [R8] [R12]. The same display carries a **질병입원율** grid usable as an external
  anchor for the *age slope* of `adm_rate` [REG-R61]; both `technical-notes.md` and
  `model.md` record that it is deliberately not used for the *level*, and why.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen. Within that page a
plain [R#] refers to its own entries, so the two schemes must never be read across. The
thirty-four entries the indemnity medical documents cite, all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: 제2조제1호나목 carves 질병·상해·간병 *out* of 손해보험
  and 제4조제1항제3호 makes them a category of their own, which places this contract in
  **제3보험** — 상해보험 and 질병보험 **at once**, the 표준약관 writing 상해 and 질병 as
  separate 보장종목 with separate limits. Retrieved: yes (full Act, 127,346 characters).
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is a 기초서류 filed with
  the FSC and never published**, which is why every pricing-basis parameter here is [std] and
  why the 가입나이 envelope is a 사업방법서 matter. Retrieved: yes.
- **REG-R3** — 보험업법 제120조: the statutory duty to accumulate 책임준비금 and
  비상위험준비금, carrying no method and no rate itself. Cited only to place the reserve
  outside this projection. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): the statutory footing of 보험개발원 and
  of the 참조순보험요율 regime — the instrument that makes [R20]'s omission of 실손의료보험 a
  legally meaningful fact rather than an editorial choice. Retrieved: yes.
- **REG-R5** — 보험업법 제181조·제184조: the 선임계리사 and the 제184조제7항 bar on holding
  the product-development, CEO or CFO role. Retrieved: yes.
- **REG-R6** — 보험업법 제108조 (특별계정): cited once, to record that a 특별계정 does not
  arise on this contract. Retrieved: yes.
- **REG-R7** — 보험업법 시행령 제1조의2 (보험상품): the Decree-level product taxonomy that
  puts 실손 in 질병보험 and 상해보험 simultaneously. Retrieved: yes (153,076 characters).
- **REG-R8** — 보험업법 시행령 제63조·제65조·제71조: the reserve taxonomy under 제120조.
  Cited as a layer this model does not compute. Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), 본문: among much else the **기준연령 요건**
  of 제1-2조제2호 making **male 40** the prescribed disclosure cell, which is why the anchor
  model point is a 40세 남자 and why [R1]'s premium for that life is the calibration target.
  Retrieved: yes (226,083 characters, the whole 고시).
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the appropriation with no
  counterpart anywhere else in this repository, cited for the reason it is *inert* here — a
  contract with no surrender value gives it nothing to bite on. Retrieved: yes.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당): cited once, to record that this
  순수보장성 contract distributes nothing. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**): the solvency layer, and the
  해지위험 and 대량해지 shocks in particular — a one-year renewable indemnity contract is the
  archetype of a product whose contract boundary decides its capital charge. Retrieved: yes
  (article text; 별표 22 was not retrieved).
- **REG-R15** — 감독규정 제5-6조·제5-7조·제6-26조 (특별계정): cited with [REG-R6], to record
  that it does not arise. Retrieved: yes.
- **REG-R17** — 감독규정 **제7-63조 (제3보험의 보험상품설계)**, retrieved in full, and
  therefore the entry carrying every current-vintage clause [R19] could not return. Cited 31
  times in `product-spec.md` and 20 in `technical-notes.md`: 제1항제1호 (nothing but the
  책임준비금 on death from a non-covered cause, hence no `claims_death`), 제1항제2호 (the
  실손해 design branch), 제2항제2호 (the ₩2,000,000 inpatient cap), 제2항제3호·제3의2호 (the
  **±25% corridor per 위험구분단위**), 제2항제5호 (the 노후·유병력자 families), 제2항제6호가목
  (the rate-adequacy test and its five-year grace), 제2항제6호나목 (the **5년 재가입주기**) and
  제2항제7호 (the mandatory **중지·재개** facility). Retrieved: yes.
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): cited once and only to record that the
  standard surrender-value machinery does not engage, there being no surrender value.
  Retrieved: yes (operative words in full; the formula display did not extract). **Not** this
  file's [R19].
- **REG-R20** — 감독규정 [별표 14] 표준해약공제액: likewise cited to record that the surrender
  charge cap has nothing to bite on. Retrieved: yes (1-page PDF, full text).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조: 제4-32조제5항 caps first-year commission
  on a 보장성보험 at one year's premium and is nowhere near binding at `comm_rate = 0.06`; and
  **제7-45조제7항** requires the **보험가격지수** to be explained **at every renewal** of a
  실손 contract, not only at sale — an obligation that exists because the price moves
  annually. Retrieved: yes.
- **REG-R23** — 보험업감독업무시행세칙 (금융감독원세칙): the instrument whose 제5-13조제1항
  makes 별표 15 the 표준약관, and therefore the reason [S1] is subordinate legislation rather
  than a carrier document. Retrieved: yes (114,610 characters).
- **REG-R25** — 시행세칙 [별표 15] **표준약관**: the same annex as [S1], retrieved
  independently as a 492-page PDF in the cross-product pass and cited 33 times where the
  load-bearing statement is the general one — 제21조 보험나이, 제22조 (death from a
  non-covered cause), 제17조 청약철회, and the general provisions the 실손 wordings inherit.
  Where the statement is specific to the 실손 text the documents cite [S1]. Retrieved: yes.
- **REG-R33** — 보험개발원 제10회 경험생명표, as reported by 보험매일: the industry table is
  released as **summary statistics only**, the first of the two reasons `mort_table.csv` is a
  construction. Retrieved: yes — **but it is a news article**, the KIDI announcement itself
  not being retrievable.
- **REG-R38** — 국가데이터처 「2024년 생명표 작성 결과」 and 통계청 「2023년 생명표」: the
  **public** national table, whose 기대수명, 기대여명 at 40 and 65 and survival to 80 are the
  four statistics the shipped Makeham fit reproduces. Retrieved: yes.
- **REG-R39** — KOSIS 완전생명표 (single-year `qx`): **Retrieved: no** — distributed through
  the KOSIS interface rather than as a fetchable file, which is the second reason
  `mort_table.csv` is a fit to summary statistics rather than a graduation of rates.
- **REG-R41** — 국민건강보험공단 「2024년도 건강보험환자 진료비 실태조사」: the survey behind
  [R9], cited beside it for the coverage ratios by provider class and age band that shape
  `utilisation_table.csv` and the component growth rates that are `med_trend_ge` and
  `med_trend_np`. Retrieved: yes (PDF, extracted in full).
- **REG-R44** — 금융감독원 「2024년 실손의료보험 사업실적(잠정)」: the same release as this
  file's [R8], retrieved through the KDI 경제교육·정보센터 mirror rather than the 보험연구원
  reproduction, and cited beside [R8] wherever a figure is load-bearing so the two
  independent retrievals corroborate. Retrieved: yes (7-page PDF, full text).
- **REG-R49** — 상법 제4편 제1장 통칙: **제649조**, the right to terminate before a claim
  event and recover the **미경과보험료** — on a one-year contract with no surrender value,
  the whole of what a lapse returns. Retrieved: yes (제4편 read in full).
- **REG-R50** — 상법 제4편 제3장 인보험: cited to record that the 인보험 suicide provisions
  have **no benefit to withhold** on a contract that pays nothing on death, and for the
  치료비 exclusions that already net off 자동차보험 and 산재보험 recoveries. Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (**청약의 철회**): the statutory cooling-off — 15 days
  from receipt of the 보험증권, never later than 30 from application, effective on despatch —
  that the 표준약관 implements verbatim, and the bar on withdrawal after a claim event.
  Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: ₩100,000,000 per person per insurer on 보험금, in
  a bucket separate from retirement-pension and 연금저축 claims. Cited here for a structural
  point: **the 해약환급금 leg of that bucket is empty on this contract.** Retrieved: yes.
- **REG-R53** — 국민건강보험법 제41조·제42조·제44조: the 요양급여 list, the 요양기관 tiers
  and the **본인일부부담금** — the definition of the 급여 half of the insured loss and the
  footing of the 본인부담상한제 that truncates it. Retrieved: yes (98,719 characters).
- **REG-R54** — 노인장기요양보험법 제2조·제15조 등: the 장기요양 등급 판정 whose **1·2등급**
  holders are exempt from the 비급여 experience rating — **the only direct statutory
  cross-reference between this model and `LTC_KR_S`**, and part of what `reld_exempt_share`
  stands for. Retrieved: yes (133,932 characters).
- **REG-R57** — 소득세법 제59조의4 (보장성보험료): the **12% credit on up to ₩1,000,000** of
  premium a year; on the anchor's ₩143,784 the credit is capped by the premium, not the
  ceiling. Retrieved: yes.
- **REG-R60** — 한국회계기준원, K-IFRS 제1117호: the standard **mandatory in Korea since
  2023-01-01**, not voluntary as in Japan, which is why the contract-boundary question on a
  one-year renewable is live rather than academic here. **Retrieved: in part** — the release
  body returned, the 별첨 HWP carrying the standard's own text did not, so the boundary
  readings the documents publish both of are **[unverified]** at instrument level.
- **REG-R61** — 보험개발원 「장기손해보험 참조순보험요율」 공시: the **published** morbidity
  reference rates — a cancer incidence grid and a **질병입원율** grid. The latter is available
  as an external anchor for the *age slope* of `adm_rate` and is deliberately not used for
  the *level*, being a fixed-benefit insured-event rate on a net-premium footing rather than
  an indemnity claim frequency. Retrieved: yes.
- **REG-R62** — 손해보험협회 공시실 / e-보험시장 (`kpub.knia.or.kr`): the portal through which
  [S6] and [S7] were reached, named in the documents because attributing a 손해보험 product
  disclosure to the 생명보험협회 would be wrong and because its POST-driven grids are where
  two of this product's gaps sit. **Retrieved: in part** — landing pages rendered; the
  comparison grids did not.

---

## Provenance note

Every entry above traces to `_research/indemnity-medical.md`, which is the citation ground
truth for this product: the S# and R# numbering used here is that file's numbering,
unchanged, and it is **never renumbered** because these documents cite against it. The
research file's own numbering is not this one's — it runs to S7 and R20 and carries
**`R18`**, which this file omits as uncited, with the reason given at the head of this
page.
The [REG-R#] scheme is a third, separate numbering, frozen at R1–R62 in
`references/regulatory-and-actuarial-references.md`.

What lives in the research file and not here: the eighteen-section fact extraction — which
figure came from which page of which release, the generation-by-generation co-payment and
deductible tables, the full 요율 상대도 worked example, the in-force and loss-ratio series by
generation, and the claim mix by treatment category and provider class; the
variation-across-carriers table; the decoding routes that made the HWP files readable at
all; and the register of fetch failures.

**The gaps register, restated because it decides what is [std] in this product.** No Korean
실손 morbidity or severity basis is published in any form — the 참조순보험요율 does not cover
the line [R20] [REG-R61] and the 산출방법서 is never disclosed [REG-R2] — so every frequency,
severity, persistency and expense parameter is a construction on aggregate experience. No
**age × sex premium scale** for 4세대 or 5세대 was obtained: [S6]'s and [S7]'s grids are
client-side or POST-driven and returned nothing to a plain fetcher, so nine of the ten model
point premiums are [std] and only the anchor's ₩11,982 is published [R1]. No 상품요약서 with
a **사업비 disclosure** was obtained for any generation, so the 6 / 7 / 3 expense split is a
[std] decomposition of one published 16.1% aggregate [R7]. The **current 보험업감독규정
제7-63조제2항** was not retrieved from the 국가법령정보센터 route [R19]; it is carried by
[REG-R17], retrieved in full, and its 제6호가목 text by the verbatim quotation in [R12]. The
**K-IFRS 1117 standard text** did not extract [REG-R60], so the contract-boundary readings
this product publishes both of are [unverified] at instrument level. And the single-year
**완전생명표 `qx` tables** live behind KOSIS and were not downloaded [REG-R39], which with the
unpublished 제10회 경험생명표 [REG-R33] is why `mort_table.csv` is a Makeham fit to four
published summary statistics [REG-R38] rather than a table.

Two entries were read through a **reproduction** rather than from the publisher: [R8], the
2024 사업실적, through 보험연구원's 「주간 트렌드」 republication — corroborated by [REG-R44],
which reached the same release through a different mirror — and [R9], likewise through
보험연구원, with its underlying survey retrieved directly as [REG-R41]. Both routes are
recorded at the entries rather than hidden, and in both cases a second independent retrieval
of the same content exists in the cross-product library.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-indemnity_medical-r1
[R10]: #krlib-indemnity_medical-r10
[R11]: #krlib-indemnity_medical-r11
[R12]: #krlib-indemnity_medical-r12
[R13]: #krlib-indemnity_medical-r13
[R14]: #krlib-indemnity_medical-r14
[R16]: #krlib-indemnity_medical-r16
[R17]: #krlib-indemnity_medical-r17
[R19]: #krlib-indemnity_medical-r19
[R20]: #krlib-indemnity_medical-r20
[R4]: #krlib-indemnity_medical-r4
[R5]: #krlib-indemnity_medical-r5
[R7]: #krlib-indemnity_medical-r7
[R8]: #krlib-indemnity_medical-r8
[R9]: #krlib-indemnity_medical-r9
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R33]: #krlib-reg-r33
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R41]: #krlib-reg-r41
[REG-R44]: #krlib-reg-r44
[REG-R53]: #krlib-reg-r53
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R62]: #krlib-reg-r62
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
