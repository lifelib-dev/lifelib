# 실손의료보험 (indemnity medical) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean 실손의료보험 (*silson uiryo boheom*, indemnity medical insurance)
liability cash-flow reference model — `Medical_KR_S`, the only **indemnity** contract in
`krlib` and the only one in this repository whose benefit is a reimbursement of an incurred
cost rather than a stated sum. Everything else in `krlib` is 정액 (*jeongaek*, fixed-sum). That
single structural fact drives the whole model: there is no 보험가입금액 that determines the
claim, only an annual limit; the claim is a function of the insured's actual medical spend, of
the public health insurance system's own cost-sharing, and of a stack of co-payment
percentages, per-visit deductibles, per-item caps and visit counts that are set by a **standard
policy wording issued by the supervisor**, not by the carrier.

실손의료보험 is habitually called 「제2의 건강보험」 — "the second national health insurance".
The 금융감독원 uses that phrase in its own press releases [R7], and the scale justifies it:
36.22 million individual policies in force at 2025-12-31 [R7], about 40 million insured persons
at 2024-12-31 [R4], and ₩17.0 trillion (17.0조원) of claims paid in 2025 against ₩18.0 trillion
(18.0조원) of premium income [R7]. It sits on top of 국민건강보험 (*gungmin geongang boheom*,
National Health Insurance, NHI) and reimburses what NHI does not: the patient's statutory
co-payment on covered treatment (**급여 본인부담금**) and the whole of non-covered treatment
(**비급여**). Because 비급여 prices are set by the provider and not by any fee schedule, the
product's loss experience is driven by a component of Korean medical inflation that no public
tariff constrains — which is why the contract has been re-designed by the supervisor four times
in twenty-seven years, and why it is written as a **one-year renewable** contract with a
**five-year re-entry** into whatever generation is on sale at the time.

This file is the **provenance layer** behind `products/indemnity_medical/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Its numbering is fixed on first writing and
is **never renumbered**: those four documents cite against `S#` and `R#` as they stand here. A
fact recorded here without a tag is a fact this session could not source, and it is marked
`[unverified]` where it is asserted at all.

Citation discipline for this file: every fact below carries `[S#]` (a primary product document
— policy wording, product summary, disclosure) or `[R#]` (a regulatory, supervisory or
actuarial publication) pointing at a document actually opened and read in this session, or is
marked `[unverified]` where it rests on a search snippet or a news report that could not be
confirmed against a retrieved document. Where a news article is the only source, the entry says
so. Amounts are given in won and, where a Korean reader would expect it, in 만원 (10,000) and
억원 / 조원 (100,000,000 / 1,000,000,000,000). Access date for every source: **2026-09-03**.

A note on generations before anything else, because the vocabulary is used throughout. The
market labels each supervisory redesign a 세대 (*sedae*, generation). The 금융감독원's own
table [R7] fixes the sale windows:

| 세대 | Sale window | Common name |
|---|---|---|
| 1세대 | ~ 2009-09 | 舊실손 (pre-standardisation) |
| 2세대 | 2009-10 ~ 2017-03 | 표준화실손 (standardised) |
| 3세대 | 2017-04 ~ 2021-06 | 착한실손 |
| 4세대 | 2021-07 ~ 2026-05 | 급여/비급여 분리 |
| 5세대 | 2026-05 ~ | 중증/비중증 분리 |

**The library's representative product is 4세대**, per the house brief, and 4세대 is what
`Medical_KR_S` implements. But 4세대 stopped being sold on 2026-05-05 [R7], and 5세대 has been
on sale since 2026-05-06 [R5], so this file documents both in full: the 4세대 wording is the
model, the 5세대 wording is the live market and the direction of travel, and the difference
between them is itself the most instructive thing about the product.

---

## Primary sources

### S1 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2021.7.1. 시행), 실손의료보험 부분
- Exact titles of the two wordings used: 「기본형 실손의료보험(급여 실손의료비)」 and
  「실손의료보험 특별약관(비급여 실손의료비)」
- Publisher: 금융감독원 (Financial Supervisory Service), as an annex to the
  보험업감독업무시행세칙 (Detailed Enforcement Rules for Insurance Business Supervision),
  제5-13조제1항 관련
- Document: `[별표15]표준약관(제5-13조제1항관련)(보험업감독업무시행세칙)_.hwp`, posted to the
  금융감독원 「금융상품 표준약관」 board 2021-06-30, stated effective 2021-07-01; the file
  contains all ten standard wordings (생명보험, 손해보험, 질병·상해보험, 기본형 실손의료보험,
  실손의료보험 특별약관, 해외여행 실손의료보험 ×2, 배상책임, 자동차, 채무이행보증, 신용,
  신원보증)
- Doc type: **표준약관** — the supervisor-issued standard policy conditions. Under Korean
  practice a carrier's own 실손 wording reproduces this text; there is no carrier discretion
  over the benefit definition, only over 보험가입금액 selection, distribution and price.
- URL (post): https://fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=21943
- URL (file): https://fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=1bc99b030d0c1dd46147a7615005dcd6&fileSn=1&bbsId=
- Accessed: 2026-09-03. Retrieved: **YES** (1.1 MB HWP5 downloaded; the OLE compound file's
  `BodyText/Section0` stream was inflated and the `HWPTAG_PARA_TEXT` records decoded to 375,277
  characters of UTF-16 text. The 실손의료보험 sections occupy characters 182,233–248,704 of
  that extraction, 66,471 characters. Tables extracted as flattened cell sequences — readable,
  but cell-to-column association had to be reconstructed by eye; the inline figures and the
  보상기간 diagrams are drawing objects and did not extract.)
- Key content: **this is the 4세대 contract itself.** 기본형 (급여): 보장종목 상해급여형 /
  질병급여형; 입원 80% reimbursement; 통원 per-visit deductible table; 제5조 annual
  보험가입금액 ₩50,000,000 (5천만원) per 보장종목, 통원 ₩200,000 (20만원) per visit, and the
  **연간 200만원 급여 입원 자기부담 상한**; 본인부담금 상한제 exclusion; 제21조 보험나이;
  제23조 재가입; 제30조 the ±25% annual renewal cap. 특별약관 (비급여): 상해비급여형 /
  질병비급여형 / **3대비급여형**; 입원 70%; 통원 max(₩30,000, 30%) with a 100-visit annual cap;
  the three 3대비급여 sub-limits with their own visit caps and the 10-visit re-assessment rule;
  제6조 the **요율 상대도** (differential renewal rate) five-band table.

### S2 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2026.5.6. 시행), 실손의료보험 부분
- Exact titles of the three wordings used: 「기본형 실손의료보험(급여 실손의료비)」,
  「실손의료보험 특별약관1(중증 비급여 실손의료비)」 and 「실손의료보험 특별약관2(비중증 비급여
  실손의료비)」
- Publisher: 금융감독원
- Document: `[별표 15] 표준약관(제5-13조제1항관련)(보험업감독업무시행세칙).hwp`, posted
  2026-06-15, stated 「'26.5.6. 시행」
- Doc type: 표준약관 — **the 5세대 contract**
- URL (post): https://www.fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=218364
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=29447dbe2fa84d85881c10281c6b9d38&fileSn=1&bbsId=
- Accessed: 2026-09-03. Retrieved: **YES** (1.6 MB HWP5, same decoding route, 449,304
  characters; the 실손 sections run 187,870–288,762)
- Key content: the 5세대 rewrite. 기본형 통원 deductible becomes `max(₩10,000 or ₩20,000, 20%,
  보장대상의료비 × 건강보험 본인부담률)` with the **본인부담률 defined arithmetically inside
  the wording**; 임신·출산 (O00–O99) and 정신발달장애 (F80–F89) brought into cover; **특별약관1
  (중증 비급여)** restricted to 산정특례 대상 질환 with a new ₩5,000,000 (500만원) annual
  co-payment cap on 상급종합·종합병원 inpatient treatment; **특별약관2 (비중증 비급여)** at 50%
  co-payment, a ₩10,000,000 (1천만원) annual limit, ₩200,000 per **day** (not per visit) for
  100 days, a ₩3,000,000 (300만원) per-admission cap at 병·의원, and outright exclusion of
  근골격계 이학요법치료, 체외충격파치료, 주사료 and 미등재 신의료기술. The 요율 상대도 table is
  carried over unchanged into 특별약관2.

### S3 — 무배당 삼성화재 다이렉트 실손의료비보험(2605.1) 보험약관 [계약전환용]
- Publisher: 삼성화재해상보험주식회사 (Samsung Fire & Marine Insurance)
- Document: 보험약관, 155 pp., cover marked `2605.1` (2026-05 edition), PDF metadata created
  2025-10-27, modified 2025-12-03
- Doc type: 약관 + 약관요약서 (policy conditions with the mandatory visual summary)
- URL: https://direct.samsungfire.com/docs/realloss.pdf
- Accessed: 2026-09-03. Retrieved: **YES** (2.4 MB PDF, 157 pages of extractable text, 291,848
  characters; the 요약서 infographics are images and their captions only partly extracted)
- Key content: a **carrier implementation of 5세대**, in the 계약전환용 (conversion) form. It
  gives what the 표준약관 does not: the menu of selectable 보험가입금액 (₩50,000,000 /
  ₩30,000,000 / ₩10,000,000 on the 급여 and 중증 covers, with the per-visit cap stepping
  ₩200,000 / ₩150,000 / ₩100,000; ₩10,000,000 / ₩6,000,000 / ₩2,000,000 on 특약2 with the same
  per-day steps), the statement that the contract is **1년만기 순수보장성 with no 해약환급금**,
  the **2028-05-06** start date for the 차등제 on 5세대 business, the 10% 무사고 할인 and its
  exact scope, a 5% discount for 의료급여 수급권자, the 재가입 rules (보장내용 변경주기 최대
  5년, 재가입 나이 최고 99세, cover to the 보험나이 100세 계약해당일), the 계약중지·재개
  machinery, and the conversion eligibility conditions.

### S4 — 무배당 삼성화재 다이렉트 실손의료비보험(1307.1) 1종(표준형) 상품요약서
- Publisher: 삼성화재해상보험주식회사
- Document: 상품요약서 (product summary), 20 pp.
- Doc type: 상품요약서
- URL: https://www.anycardirect.com/docs/realloss_sum.pdf
- Accessed: 2026-09-03. Retrieved: **YES** (221 KB PDF, text extracted cleanly)
- Key content: a **2세대 (표준화실손)** carrier document, 2013-07 edition. It is the only
  retrieved document that states a **가입나이** range (0–49 on this direct-channel product) and
  it sets out the pre-2017 renewal architecture explicitly: 보험기간 1년, 자동갱신 최고 14회,
  보장내용 변경주기 (재가입주기) **15년**, 재가입 나이 15–99, maximum cover to the 보험나이
  100세 계약해당일. It also carries the 입원 80% rule and the **연간 200만원** inpatient
  co-payment cap in a 2세대 wording, and the 하나의 상해당 최초입원일부터 365일 rule.

### S5 — 무배당 프로미라이프 실손의료비보험2101 (DB손해보험) 보험약관
- Publisher: DB손해보험주식회사
- Document: 보험약관, 108 pp., edition `2101` (2021-01)
- Doc type: 약관 + 약관요약서
- URL: https://www.idbins.com/pcweb/bizxpress/pdc/hc/__etc/실손의료비보험2101.pdf
  (percent-encoded form used for retrieval)
- Accessed: 2026-09-03. Retrieved: **YES** (4.8 MB PDF, 154,558 characters extracted)
- Key content: a **3세대** carrier document, the generation immediately before the model's. Its
  약관요약서 states the 3세대 deductible set verbatim — 질병통원(외래) `max(병원별 공제금액
  1~2만원, 20%)`, 질병통원(처방조제비) `max(₩8,000, 20%)`, and the three 비급여 특약 items at
  `max(₩20,000, 30%)` — which is the direct predecessor of the 4세대 `max(₩30,000, 30%)`. It
  also carries the 자동갱신 / 재가입 clause structure that 4세대 inherits, and confirms that
  the wider 통합형 product to which the 실손 covers were attached offered 해지환급금 미지급형
  and 저지급형 variants.

### S6 — 손해보험협회 공시실, 「실손의료보험 보험료 인상률 및 손해율 공시」
- Publisher: 손해보험협회 (General Insurance Association of Korea), 공시실
- Doc type: 공시자료 (statutory public disclosure)
- URL: https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthIncreaseRate.do
- Accessed: 2026-09-03. Retrieved: **in part** (page structure, the insurer list, the disclosed
  definitions and one worked row were read; the full grid is rendered client-side and could not
  be paged through by a plain fetcher)
- Key content: the disclosure covers **10 손해보험사** (메리츠화재, 한화손보, 롯데손보,
  흥국화재, 삼성화재, 현대해상, KB손보, DB손보, 신한EZ손해보험, 농협손보) and **7 생명보험사**
  (한화생명, 삼성생명, 흥국생명, 교보생명, 농협생명, DB생명, 동양생명), showing three years of
  보험료 인상률 (2024/2025/2026) and three years of 경과손해율 (2023/2024/2025), split 상해 /
  질병 / 합계 (3대비급여 included). The disclosed definitions are exact: the 인상률 is
  「직전연도말 대비 4세대 실손의료보험의 남여 각 연령별 영업보험료 인상률에 해당 성별 연령의
  직전연도 보험료수익 비중을 곱하여 산정」 — i.e. a premium-weighted average over the age × sex
  rate scale — and 손해율 is 「발생손해액/경과보험료」. One row read in full: 메리츠화재
  상해담보, 인상률 2026 **21.8%** and 2025 **23.9%**, 경과손해율 2025 **117.2%** and 2024
  **130.1%**.

### S7 — 손해보험협회 공시실 — 실손의료보험 안내, 5세대 표준, 보험료 비교공시
- Exact page titles: 「실손의료보험 안내」, 「실손의료보험(5세대)」, 「보험료 비교공시」
- Publisher: 손해보험협회, 공시실
- Doc type: 공시자료 (consumer-facing product disclosure)
- URLs:
  - https://kpub.knia.or.kr/pdic/mins/MinsInf.knia
  - https://kpub.knia.or.kr/productDisc/lostHealth/lostHealth5thStandard.do
  - https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthDisclosure.do
- Accessed: 2026-09-03. Retrieved: **in part** (the descriptive pages returned text; the
  premium comparison grid is a POST-driven form and returned 「조회된 내용이 없습니다」 to a
  plain fetcher)
- Key content: the association's own restatement of the 5세대 deductible formula — 입원
  `보장대상의료비 × 20%`, 통원 `Max[보장대상의료비 × 건강보험본인부담률, 보장대상의료비 × 20%,
  1만원(병·의원) 또는 2만원(상급종합·종합병원)]` — and the annual limits (기본형 5천만원 with
  통원 회당 20만원; 특약1 5천만원; 특약2 1천만원). The comparison tool's own input taxonomy
  confirms the three marketed families: **표준화 / 노후 / 유병력자**. The tool is filtered by
  성별 and 보험나이, which is the disclosure's own confirmation that the rate scale is an age ×
  sex table.

---

## Regulatory and actuarial references

### R1 — 금융위원회 외, 「7.1일부터 제4세대 실손의료보험이 출시됩니다」 (2021-06-30)
- Publisher: 금융위원회 (Financial Services Commission), joint release with 금융감독원 and both
  trade associations
- Document: 보도자료, 배포 2021-06-29, 보도 2021-06-30 조간, 10 pp. (`210630_보도자료_7.1일부터
  4세대 실손보험이 출시됩니다_F.pdf`)
- Doc type: 보도자료 (supervisory press release)
- URL (post): https://www.fsc.go.kr/no010101/76157
- URL (file): https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=76157&fileTy=ATTACH&fileNo=2
- Accessed: 2026-09-03. Retrieved: **YES** (438 KB PDF, 10 pp., 7,953 characters extracted; all
  substantive tables extracted as machine-readable text)
- Content: **the founding document of the model's generation.** Recites the design intent, the
  급여/비급여 split, the co-payment increases, the deductible increases, the shortening of the
  재가입주기 from 15 to 5 years, the five-band 차등제 with its thresholds, the 무사고 할인, the
  conversion process, the launch carrier list (15 companies: 10 손보, 5 생보) and — the single
  most useful quantitative item — a published **40세 남자 monthly premium comparison across all
  four generations** as at 2021-06.

### R2 — 금융위원회 외, 「「4세대 실손의료보험 출시」 관련 주요 FAQ」 (2021-06)
- Publisher: 금융위원회 외 3
- Document: 12 pp., 2021-06 (`200630 4세대 실손보험 출시 관련 주요 FAQ_FF.pdf`)
- Doc type: 보도참고자료 (FAQ annexed to R1)
- URL: https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=76157&fileTy=ATTACH&fileNo=4
- Accessed: 2026-09-03. Retrieved: **YES** (654 KB PDF, 12 pp., 6,619 characters extracted; the
  two 심평원 screenshot figures did not extract)
- Content: the **arithmetic of the 차등제** stated as a formula, the annual reset of the
  experience record, the statement that the 비급여 특약 is about **60% of the total premium**
  when both parts are held, a fully worked 45-year-old-male example, the 도수치료 10-visit
  re-assessment rule with its clinical test list, the 영양제·비타민제 payability rule with four
  worked drug examples, and the conversion / re-entry Q&As.

### R3 — 금융위원회, 4세대 실손 비급여 보험료 할인·할증 시행 (2024-06-07)
- Exact title: 「'24.7.1일부터 4세대 실손의료보험은 비급여 이용량에 따라 비급여 보험료가 할인
  또는 할증됩니다」
- Publisher: 금융위원회
- Document: 보도자료, 2024-06-07
- Doc type: 보도자료
- URL: https://www.fsc.go.kr/no010101/82406
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read; the attached PDF was not separately
  opened)
- Content: the commencement of the **비급여 할인·할증** on 2024-07-01, three years after
  product launch, its five bands with the −5% (잠정) discount factor and the +100% / +200% /
  +300% surcharges, the exemptions (국민건강보험법상 산정특례대상질환; 노인장기요양보험법상
  장기요양 1·2등급 판정자), and a distribution of contracts across bands.

### R4 — 금융위원회, 실손보험 개혁방안 (2025-04-01)
- Exact title: 「실손의료보험, 낮은 보험료로 정말 필요할 때 도움되는 보험상품으로
  재탄생합니다」
- Publisher: 금융위원회 (보험과)
- Document: 보도자료, 2025-04-01 (referenced elsewhere as the 2025-04-02 발표)
- Doc type: 보도자료 — the **실손보험 개혁방안** that became 5세대
- URL: https://www.fsc.go.kr/no010101/84272
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read; attachments not separately opened)
- Content: the reform's baseline statistics — 4천만명 insured at 2024-12-31; ~1.6천만건 of
  policies with **no 약관변경(재가입) clause at all**; total national medical spend ₩133조 of
  which 실손 bore ₩14.1조 (10.6%) in 2023; the 비급여 claim series 2017 ₩4.8조 → 2023 ₩8.2조;
  the total claim series 2017 ₩7.3조 → 2020 ₩11.1조 → 2023 ₩14.1조; the **premium increase
  series 2022 14.2% → 2023 8.9% → 2024 1.5% → 2025 7.5%**; the concentration statistics (9% of
  policyholders take 80% of claims, 65% take none); and the intended structure of the new
  product with its expected 30–50% premium reduction.

### R5 — 금융위원회·금융감독원, 5세대 실손의료보험 출시 (2026-05-06)
- Exact title: 「5월 6일부터 치료비 부담이 큰 중증질환의 보장을 강화하고, 보험료는 낮춘 5세대
  실손의료보험이 새롭게 출시·판매됩니다」
- Publisher: 금융위원회 (보험과) and 금융감독원 (보험상품분쟁2국), joint with both trade
  associations
- Document: 보도자료, 배포 2026-05-04 08:00, 보도 2026-05-06 조간, 15 pp. (`260504_(보도자료) …
  5세대 실손의료보험이 새롭게 출시, 판매됩니다.pdf`)
- Doc type: 보도자료
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217561&menuNo=200218
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa16ababffbc45d1be8ed764aa9cec3b&fileSn=2&bbsId=
- Accessed: 2026-09-03. Retrieved: **YES** (655 KB PDF, 15 pp., 13,903 characters; 참고1's
  4세대-versus-5세대 comparison table extracted in full — it is the **only retrieved document
  that states the complete 4세대 limit and sub-limit set in one place**, which is why it is
  cited so heavily below alongside S1)
- Content: the 5세대 product in full; the 4세대 comparison table; the premium effect (−30% on
  4세대, −50%+ on 1·2세대; base + 특약1 only ≈ 50% of the 4세대 premium); the 선택형 할인 특약
  and 계약전환 할인 (계약재매입) schemes commencing 2026-11 for the ~47.5% of in-force policies
  written before 2013-03 with no re-entry clause; a worked 60-대 여성 premium table across
  options; and the launch carrier list (16 companies: 7 생보, 9 손보).

### R6 — 금융위원회·금융감독원, 「5세대 실손보험 Q&A」
- Publisher: 금융위원회·금융감독원
- Document: 별첨1 to R5, 2026-05 (`260504_(별첨1) 5세대 실손보험 출시 관련 Q&A.hwp`)
- Doc type: 보도참고자료
- URL: https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa16ababffbc45d1be8ed764aa9cec3b&fileSn=3&bbsId=
- Accessed: 2026-09-03. Retrieved: **YES** (104 KB HWP5, decoded to 8,598 characters; the
  table-of-contents page numbers extracted with control-character noise, the body is clean)
- Content: fifteen Q&As. The ones that matter here: the four permitted **가입 유형** (주계약
  alone; +특약1; +특약2; +both); the 관리급여 (managed-benefit) mechanism and its 95%
  co-payment; a four-row table of the whole 국민건강보험 cost-sharing taxonomy (급여 / 선별급여
  / 관리급여 / 비급여) with co-payment ranges; the 2025 claim mix (비급여 근골격계 물리치료 +
  주사제 **27.3%**, 암 관련 12.8%); the statement that the 실손 renewal increase is **capped at
  25% per year per risk cell**; and a carrier's 1세대 60-대 average monthly premium (남
  ₩150,000, 여 ₩200,000).

### R7 — 금융감독원, 「2025년 실손의료보험 사업실적(잠정)」
- Publisher: 금융감독원 보험상품분쟁2국 보험상품제도팀
- Document: 보도자료, 배포 2026-06-02, 보도 2026-06-04 조간, 8 pp. (`260602_(보도자료) 2025년
  실손의료보험 사업실적(잠정).pdf`)
- Doc type: 보도자료 — the **annual industry experience statement**
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=218168&menuNo=200218
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=cbd3c2989cfa4a71a8b2eeba98817866&fileSn=2&bbsId=
- Accessed: 2026-09-03. Retrieved: **YES** (810 KB PDF, 8 pp., every numeric table extracted as
  machine-readable text; two bar charts are images and their axis labels did not extract)
- Content: **the single most important experience source for this model.** In-force counts by
  generation, premium income, claims paid split 급여/비급여, insurance result, 경과손해율
  overall and by generation, the stated break-even loss ratio, claims by treatment category,
  claims by provider type with the 비급여 share inside each, per-policy claim amounts by
  generation, per-generation monthly premium for a 40대 남자 at a 손해보험사, and the
  supervisory programme for 2026 including the **4세대 재가입 conversion wave from 2026-07**.

### R8 — 금융감독원, 「2024년 실손의료보험 사업실적(잠정)」
- Publisher: 금융감독원 보험계리상품감독국 보험상품제도팀
- Document: 보도자료, 배포 2025-05-12, 보도 2025-05-13 조간, 7 pp.
- Doc type: 보도자료
- URL (original post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=193952&menuNo=200218
- URL (retrieved copy): https://kiri.or.kr/PDF/weeklytrend/20250526/trend20250526_4.pdf
- Accessed: 2026-09-03. Retrieved: **YES**, but **through a reproduction**: the document was
  read from 보험연구원's 「주간 트렌드」 PDF republication of the 금융감독원 release (1.8 MB, 7
  pp., extracted in full). The 금융감독원 posting itself was located in the board index but its
  own attachment was not downloaded in this session. The reproduction is verbatim, carries the
  original 보도/배포 dates and the 담당부서 block, and its figures reconcile with R7's
  prior-year columns wherever the two overlap — so it is treated as retrieved, with the route
  recorded.
- Content: the 2024 counterpart of R7, plus two things R7 does not repeat: the **세대별 비급여
  자기부담률 and per-policy 비급여 claim table** (1세대 through 4세대, inpatient and
  outpatient), and the **세대별 월납보험료 time series 2021–2024** for a 40대 남자 at a
  손해보험사.

### R9 — 국민건강보험공단, 「2024년 건강보험 보장률 64.9%」
- Publisher: 국민건강보험공단 (National Health Insurance Service) 비급여관리실 보장성평가센터
- Document: 보도자료, 배포 2025-12-30, 14 pp., reporting the 「2024년도 건강보험환자 진료비
  실태조사」
- Doc type: 보도자료 (official statistics)
- URL (retrieved copy): https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf
- Accessed: 2026-09-03. Retrieved: **YES**, again through the 보험연구원 「주간 트렌드」
  reproduction (1.3 MB, 14 pp., 18,385 characters; all tables extracted, the two trend charts
  extracted as loose number sequences). The 국민건강보험공단 original posting was not located
  directly this session — see gaps.
- Content: the **layer underneath the product**. 건강보험 보장률 64.9% for 2024 with 법정
  본인부담률 19.3% and 비급여 본인부담률 15.8%; total national treatment cost ₩138.6조 split
  보험자부담금 ₩90.0조 / 법정본인부담금 ₩26.8조 / 비급여진료비 ₩21.8조; coverage ratios and
  비급여 shares by provider type and by age band; the coverage ratio for 4대중증질환 and for
  cancer; and a 비필수항목-adjusted coverage ratio that explicitly removes 도수치료, 영양주사,
  상급병실료 and 제증명수수료 — the same items the 실손 reforms target.

### R10 — 국민건강보험공단, 「본인부담상한제」 (제도 안내)
- Publisher: 국민건강보험공단
- Doc type: statutory scheme description with the year-by-year threshold table
- URL: https://www.nhis.or.kr/nhis/minwon/wbhapa01000m01.do?mode=view&articleNo=10946900
- Accessed: 2026-09-03. Retrieved: **YES**
- Content: the definition — 「연간 요양기관에 지출한 본인부담금이 개인별 상한액을 초과할 경우
  초과액을 공단이 부담」, operated as 사전급여 and 사후환급 over the calendar year — and the
  income-decile threshold table for 2023–2026. This is a **hard cap on the 급여 half of the
  실손 claim**, because S1 제4조 excludes from cover any amount refundable under it.

### R11 — 건강보험심사평가원, 「외래진료시 본인부담률 및 부담액」
- Publisher: 건강보험심사평가원 (Health Insurance Review and Assessment Service, HIRA)
- Doc type: statutory cost-sharing schedule, stated as deriving from 국민건강보험법 시행령
  별표2
- URL: https://www.hira.or.kr/dummy.do?pgmid=HIRAA030056020110
- Accessed: 2026-09-03. Retrieved: **YES**
- Content: the outpatient co-payment percentages by provider tier that the 5세대 wording now
  reads directly, and that determine the 급여 본인부담금 the 실손 reimburses in every
  generation.

### R12 — 보험연구원 김경선, 「실손의료보험 현황 및 개선과제」 (2024-12-05)
- Seminar title: KIRI 세미나 「건강보험 지속성을 위한 정책과제」
- Publisher: 보험연구원 (Korea Insurance Research Institute), presented 2024-12-05
- Document: seminar deck, 34 slides
- Doc type: research presentation
- URL: http://www.kiri.or.kr/pdf/세미나자료/smn_20241205_2.pdf (percent-encoded form used)
- Accessed: 2026-09-03. Retrieved: **YES** (1.5 MB PDF, 34 pp., 12,536 characters; the charts
  are images whose data labels extracted but whose axes did not, so several series are read as
  loose number sequences and are quoted below only where the label-to-value mapping is
  unambiguous from the surrounding text)
- Content: the public-private coverage decomposition for 2022; the **10대 비급여** table with
  per-item claim amounts; the 4세대 급여-versus-비급여 loss ratio split for three half-years;
  the distribution of policyholders across 할인·할증 bands attributed to a 금융감독원 release
  of 2024-01-19; the verbatim text of **보험업감독규정 제7-63조제2항제6호가목** on annual rate
  adequacy testing; and the distribution of claim size by generation.

### R13 — 금융위원회, 실손보험 청구 전산화 1단계 시행 (2024-10-25)
- Exact title: 「'24.10.25일부터 '창구 방문 없는', '복잡한 서류 없는' 실손보험 청구 전산화가
  순차적으로 시행됩니다」
- Publisher: 금융위원회 (보험과)
- Document: 보도자료, 2024-10-25
- Doc type: 보도자료
- URL: https://www.fsc.go.kr/no010101/83255
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read; the attached PDF/HWP were not
  separately opened)
- Content: the launch of **실손24**, the electronic claim channel — phase 1 (병원급 with 30 or
  more beds, plus 보건소) from 2024-10-25, phase 2 (의원·약국) scheduled for 2025-10-25; the
  참여 counts and rates at launch; and 보험개발원 as the statutory **전송대행기관**.

### R14 — 금융위원회, 「실손보험 청구 전산화가 의원·약국을 포함하여 확대 시행됩니다」
- Publisher: 금융위원회
- Document: 보도자료, 2025-10-23
- Doc type: 보도자료
- URL: https://fsc.go.kr/no010101/85456
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read)
- Content: phase 2 of 실손24 from 2025-10-25, the full provider counts, the connection rates
  eleven months after phase 1, the documents transmitted, and the statutory confidentiality
  constraint on the 전송대행기관.

### R15 — 금융위원회, 「보험업법 시행령·감독규정 입법예고」 (2026-01-15)
- Subtitle: 5세대 실손보험 및 기본자본, 판매채널 책임성 강화 등 관련
- Publisher: 금융위원회
- Document: 보도자료, 2026-01-15; 예고기간 2026-01-15 ~ 2026-02-25
- Doc type: 보도자료 (legislative pre-announcement)
- URL: https://www.fsc.go.kr/no010101/86059
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read; the draft 개정안 attachments were
  not opened)
- Content: confirms that the 5세대 상품설계기준 sits in the **보험업법 시행령 and
  보험업감독규정**, with the detail delegated to the 보험업감독업무시행세칙 — i.e. that S2 is
  the operative text and the 감독규정 is its enabling instrument. States the design
  constraints: 급여 통원 co-payment linked to the 건강보험 본인부담률 with a 20% floor; 중증
  비급여 30% with a ₩30,000 minimum; 비중증 비급여 50% with a ₩50,000 minimum.

### R16 — 금융감독원, 「최근 민원사례로 알아보는 실손의료보험 관련 소비자 유의사항」
- Publisher: 금융감독원 소비자소통국 손해보험민원팀
- Document: 보도자료, 2026-05-19
- Doc type: 보도자료
- URL: https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217901&menuNo=200218
- Accessed: 2026-09-03. Retrieved: **in part** (the page body and the attachment list were
  read; the attachments were not opened)
- Content: four complaint patterns, of which two bear on the model: the **개인실손 중지제도**
  (suspension of an individual policy while a group 실손 is in force, and resumption within one
  month of the group cover ending) and the **6-month conversion withdrawal** right.

### R17 — 금융위원회, 노후·유병력자 실손의 가입·보장연령 확대 (2025-02-11)
- Exact title: 「(노후·유병력자) 실손보험의 가입연령과 보장연령을 확대하여 고령화 시대의 의료비
  보장 기능을 강화합니다」
- Publisher: 금융위원회
- Document: 보도자료, 2025-02-11
- Doc type: 보도자료
- URL: https://www.fsc.go.kr/no010101/83985
- Accessed: 2026-09-03. Retrieved: **YES** (HTML body read)
- Content: the two adjacent product families — **노후실손** and **유병력자실손** — and the
  2025-04-01 widening of their issue and cover ages. Relevant here because R7's in-force
  breakdown reports them as a separate 2.4% block outside the five generations.

### R18 — 금융위원회, 「실손보험 개혁방안 주요 정책문답」
- Publisher: 금융위원회
- Document: 정책문답 accompanying R4, 2025-04
- Doc type: 보도참고자료
- URL: https://www.fsc.go.kr/po020201/84273
- Accessed: 2026-09-03. Retrieved: **in part** (the page body was read; the attachments were
  not opened)
- Content: the reform's own defence of the 중증/비중증 boundary — 급여 inpatient treatment
  treated **wholly** as 중증, and 비급여 split by whether the condition is a 산정특례 대상
  질환; the 2024 industry profit decomposition; and the original timetable (신규상품 2025년말,
  the 비중증 특약 deferred into 2026 상반기) against which the actual 2026-05-06 launch should
  be read.

### R19 — 보험업감독규정 (금융위원회고시) 제7-63조 (제3보험의 보험상품설계 등)
- Publisher: 금융위원회
- Doc type: 행정규칙 (financial-regulatory notification)
- URLs tried: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196 ;
  https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000235980 ;
  https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=24827&fileTy=ATTACH&fileNo=10 ;
  https://www.easylaw.go.kr/CSP/FlDownload.laf?flSeq=317766
- Accessed: 2026-09-03. Retrieved: **in part**. The 국가법령정보센터 pages return only the
  masthead and the amendment metadata to a plain fetcher (시행 2023-03-02, 금융위원회고시
  제2023-10호 on one; 시행 2024-01-31, 제2024-9호 on another) — the article text is
  JavaScript-rendered. Two HWP copies were downloaded and decoded successfully, but **both are
  a pre-2013 vintage** whose 제7-63조 has only three 호 and no 제2항 at all. The current
  제7-63조제2항, which is where the 실손의료보험 design rules live, was therefore **not
  retrieved from a primary source**.
- Content actually read, from the decoded HWP: 제7-63조 as it stood after the 2011-03-22
  전문개정 — 「보험회사는 영 별표 7 제5호에 따라 제3보험상품을 설계하려는 경우 … 1. 약관상
  보장하지 아니하는 원인으로 사망시 책임준비금을 지급하고 계약이 소멸하도록 설계할 것
  2. 약관상 보장하는 금액은 정액 또는 실제 발생하는 손해(이하 "실손해"라 한다)를 기준으로
     설계할 것 …」. The **current** 제2항제6호가목 is quoted verbatim in R12 and is reproduced
     below at §17 on that basis, attributed to R12 rather than to the regulation itself.

### R20 — 보험개발원, 「장기손해보험 참조순보험요율 예시」
- Publisher: 보험개발원 (Korea Insurance Development Institute, KIDI)
- Doc type: 참조순보험요율 disclosure
- URL: https://www.kidi.or.kr/user/nd13261.do
- Accessed: 2026-09-03. Retrieved: **YES**
- Content: the published reference-rate categories for 장기손해보험 as applied from 2024-04-01
  (일반상해 from 2026-01-01) — 일반상해 and 교통상해 (사망/후유장해/입원), 질병 사망률,
  후유장해, 입원율, 암 발생률, 비용손해, 재물손해, 배상책임. **실손의료보험 위험률 is not among
  them.** This is the negative result that fixes the model's calibration boundary: there is no
  published Korean indemnity-medical morbidity or severity basis, so the model's claim
  frequency and severity must be constructed `[std]` from the aggregate experience in R7 and
  R8.

---

## Fact extraction

### 1. What the product is, statutorily and structurally

- 실손의료보험 is a **제3보험** (*je-sam boheom*, "third-sector") contract. 보험업감독규정
  제7-63조 requires a 제3보험 product to be designed so that the benefit is stated **either**
  as a fixed sum **or** on the basis of 「실제 발생하는 손해(이하 "실손해"라 한다)」 [R19].
  실손해 is the root of the product's name: 실손 = 실제 손해, the actual loss. Every other
  `krlib` 제3보험 product (`cancer`, `long_term_care`, `child`, and the CI limb of
  `ci_insurance`) takes the 정액 branch of that sentence; this one takes the 실손해 branch.
- The 금융감독원's own one-line definition: 「실손의료보험은 피보험자(환자)가 부담하여 실제
  발생한 의료비[급여 본인부담금 + 비급여] 중 일정 금액을 보상하는 보험상품」 [R7]. The
  square-bracketed decomposition is the whole model: the covered spend is exactly (statutory
  co-payment on NHI-covered treatment) + (all non-covered treatment).
- First sold in **1999**; the 금융감독원 describes it as having performed 「제2의 건강보험
  역할」 for more than 25 years [R7].
- The wording is a **표준약관** issued by the supervisor, not a carrier document. S1 and S2 are
  annex 15 to the 보험업감독업무시행세칙, made under 제5-13조제1항. A carrier's own 실손 policy
  reproduces the standard text; the 2026 삼성화재 booklet [S3] and the 2021 DB booklet [S5]
  both do so almost verbatim. **This is why `Medical_KR_S` can be specified from a public
  document to a level of precision that no other product in this repository reaches.**
- It is **not** a life-office monopoly: both 생명보험회사 and 손해보험회사 write it. At
  2025-12-31 the split of in-force policies was 손보사 30.28 million against 생보사 5.94
  million — 손보사 hold **83.6%** of the book [R7].

### 2. Generation history, with dates

The five generations, from the 금융감독원's own table [R7] with the sale windows stated there:

| 세대 | Sale window | 자기부담률 as sold |
|---|---|---|
| 1세대 (舊실손) | ~ 2009-09 | 손보 0%, 생보 20% |
| 2세대 (표준화실손) | 2009-10 ~ 2017-03 | 급여 10%, 비급여 20% 등 |
| 3세대 | 2017-04 ~ 2021-06 | (주계약) 급여 10%, 비급여 20% 등; (특약) 도수치료 등 3대 비급여 30%, 횟수·금액 제한 |
| 4세대 | 2021-07 ~ 2026-05 | (주계약) 급여 20%; (특약) 비급여 30%, 3대 비급여 횟수·금액 제한 |
| 5세대 | 2026-05 ~ | (주계약) 급여 입원 20%, 통원 20% 이상 (건보 본인부담률 연동); (특약1) 중증 비급여 30%; (특약2) 비중증 비급여 50% |

- **1세대** predates standardisation. There was no common wording; 손해보험회사 products
  frequently reimbursed **100% of the covered spend with no co-payment at all**, and
  생명보험회사 products used 20% [R7] [R8]. Renewal was every **3–5 years** [R7]. This is the
  generation whose loss ratio and whose premium level are the market's structural problem: a
  40대 남자 1세대 policy at a 손해보험사 cost **₩66,000 per month** in 2025 [R7], and a
  carrier's 60대 average was ₩150,000 (male) / ₩200,000 (female) per month [R6].
- **2세대 — 표준화 (standardisation), 2009-10.** The first 표준약관 for 실손. Renewal shortened
  to **1–3 years** [R7]; co-payment set at 급여 10% / 비급여 20% [R7]; a **15-year** 재가입주기
  introduced, which S4 documents in a carrier product as 「보장내용 변경주기(재가입주기)는
  15년」 with 자동갱신 최고 14회 and 재가입 나이 15–99. Contracts written **before 2013-03**
  have **no 약관변경(재가입) condition at all** — the reform documents put that block at about
  1.6천만건 [R4], and at **47.5% of all in-force 실손 at 2024-12-31** [R5]. That is the single
  largest obstacle to reforming the book, because those policies cannot be migrated by the
  ordinary re-entry mechanism.
- **3세대, 2017-04 — 「착한실손」.** Kept a combined 급여+비급여 main contract but carved out
  **three 비급여 특약** — 도수·증식·체외충격파치료, 비급여 주사, 비급여 MRI — each with its own
  30% co-payment and its own annual money and visit caps [R1]. Renewal annual [R7]. S5 is a
  carrier wording from this generation and states its deductibles exactly: 질병통원(외래)
  `max(₩10,000–₩20,000, 20%)`, 처방조제비 `max(₩8,000, 20%)`, and the three 비급여 특약 items
  at `max(₩20,000, 30%)`.
- **4세대, 2021-07-01.** The 급여/비급여 split; see §3. Announced in 2020-12 as the 「실손보험
  상품구조 개편방안」, implemented by amendment of the 보험업감독규정 and the 표준약관 in
  2021-06 [R1]. Sold from 2021-07-01 by 15 carriers — 10 손해보험사 (메리츠화재, 롯데손보,
  MG손보, 흥국화재, 삼성화재, 현대해상, KB손보, DB손보, 농협손보, 한화손보) and 5 생명보험사
  (한화생명, 삼성생명, 흥국생명, 교보생명, NH농협생명), with ABL생명 and 동양생명 offering
  conversion only [R1].
- **비급여 할인·할증 commenced 2024-07-01**, deferred three years from launch 「충분한 통계
  확보 등을 위하여」 [R3]. See §7.
- **5세대, 2026-05-06.** Sold by 16 carriers (7 생보, 9 손보; 신한EZ손보 from 2026-06-01) [R5].
  See §9.
- **The 4세대 re-entry wave begins 2026-07.** R7's supervisory programme states it plainly:
  「'21.7월 도입된 4세대 실손의 재가입주기(5년)가 도래하여 순차적인 전환 실시」 — the first
  4세대 policies reach their five-year 보장내용 변경주기 in July 2026 and are re-entered into
  5세대. A 4세대 policy written at outset therefore has a **contractual life of five years in
  its own form**, after which its terms are replaced. This is the fact that most sharply
  constrains the projection horizon and the contract-boundary treatment.

### 3. The 4세대 structure — 급여 / 비급여 분리

- The design statement, from the launch release: 「실손보험 상품 구조를 급여(주계약)와
  비급여(특약)로 분리하면서, 필수치료인 급여에 대해서는 보장을 확대하되, 환자의 선택사항인
  비급여에 대해서는 의료이용에 따라 보험료가 할인·할증되도록 하였습니다」 [R1].
- Consequently a 4세대 contract is **two priced units**:
  - **기본형 실손의료보험 (급여 실손의료비)** — the main contract, with two 보장종목,
    **상해급여형** and **질병급여형** [S1 제1조].
  - **실손의료보험 특별약관 (비급여 실손의료비)** — the rider, with three 보장종목,
    **상해비급여형**, **질병비급여형** and **3대비급여형** [S1 제1조].
- Their loss ratios are tracked and re-rated separately: 「급여, 비급여 각각의 손해율에 따라
  보험료가 조정되어, 본인의 의료이용 상황 및 보험료 수준에 대한 이해도가 높아질 것」 [R1]. R12
  shows the two moving very differently in practice — see §12.
- The premium split is published: when both parts are held, the 비급여 특약 is 「전체 보험료의
  60% 수준」 [R2]. The worked example in the same document uses 급여 ₩5,000 and 비급여 ₩8,000
  on a total of ₩13,000 per month for a 45-year-old male — a 61.5% 비급여 share. **This is the
  ratio the model uses to split a total premium into its two re-rating units.**
- 「급여」 means 「「국민건강보험법」에서 정한 요양급여 또는 「의료급여법」에서 정한 의료급여」
  [S1 제1조 주]. 「비급여」 means 「「국민건강보험법」 또는 「의료급여법」에 따라
  보건복지부장관이 정한 비급여 대상」, and expressly includes the case where the NHI procedure
  was followed but no covered item arose [S1 특별약관 제1조 주].
- Cover was **widened** on the 급여 side at the 4세대 change: 불임관련 질환 (habitual
  miscarriage, infertility, complications of artificial insemination) from **two years after
  inception**, excluding 전액본인부담금; 선천성 뇌질환 where the policy was taken out in utero;
  and dermatological conditions recognised as 급여 [R1].
- Cover was **narrowed** on the 비급여 side: 도수치료 subjected to the 10-visit re-assessment
  rule, and 영양제·비타민제 restricted to use within the drug's licensed indication [R1].

### 4. 4세대 급여 (main contract) — reimbursement basis

All from S1, 기본형 실손의료보험 제3조 and 제5조, cross-checked against the summary table in R5
참고1.

- **입원 (inpatient).** The benefit is 「본인부담금 … 의 80%에 해당하는 금액」 — 80% of the
  patient's own NHI/의료급여 co-payment, whether that co-payment is a 일부본인부담금 (partial)
  or a 전액본인부담금 (full). Hence a **20% 자기부담률** [S1].
- **통원 (outpatient, = 외래 + 처방조제).** Per visit: the co-payment less a deductible drawn
  from a two-row table [S1 제3조 <표1>]:

  | Provider | 공제금액 |
  |---|---|
  | 의료법 제3조제2항 의료기관 (종합병원 제외), 보건소·보건의료원·보건지소, 보건진료소, and their pharmacies | 1만원과 보장대상 의료비의 20% 중 큰 금액 |
  | 전문요양기관, 상급종합병원, 종합병원, and their pharmacies | 2만원과 보장대상 의료비의 20% 중 큰 금액 |

  So the outpatient deductible is `max(₩10,000 or ₩20,000, 20% × 보장대상의료비)`. Note that
  the 3세대 separate ₩8,000 처방조제 deductible [S5] is gone: 4세대 merges 외래 and 처방조제
  into one visit with one deductible.
- **The 급여 annual co-payment cap.** S1 제5조제4항: where the 20% retained by the insured on
  **inpatient** treatment exceeds **₩2,000,000 (200만원)** in a policy year measured from the
  계약일 or 계약해당일, the excess is reimbursed inside the annual limit. R5 참고1 restates it
  as 「입원 연간 자기부담한도 200만원」. The same cap already existed in 2세대 [S4], so it is a
  long-standing feature and not a 4세대 novelty.
- **Annual limits.** S1 제5조: 「연간 보험가입금액은 … (1)상해급여에 대하여 입원과 통원의
  보상금액을 합산하여 5천만원 이내에서, (2)질병급여에 대하여 … 5천만원 이내에서 회사가 정한
  금액 중 계약자가 선택한 금액」 — **₩50,000,000 (5천만원) per 보장종목 per year**, inpatient
  and outpatient combined, and 상해 and 질병 have **separate** limits. 「연간」 is defined as
  「계약일로부터 매1년 단위로 도래하는 계약해당일 전일까지의 기간」 — a policy year, not a
  calendar year [S1 제5조제2항].
- **Per-visit cap.** 「통원 1회당 20만원 이내에서 회사가 정한 금액 중 계약자가 선택한 금액」 —
  **₩200,000 (20만원) per visit** [S1 제5조제5항].
- **No visit-count cap on the 급여 side.** S1 제5조 sets none, and R5 참고1 records no count
  for the 주계약 either. The 100-visit cap is a 비급여 feature (§5).
- **본인부담금 상한제 interaction.** S1 제5조제3항: where the NHI 본인부담금 상한제 or the
  의료급여 본인부담금 보상제/상한제 applies, the reimbursement is limited to what the insured
  actually bore net of any amount refundable ex ante or ex post. And S1 제4조제3항제1호
  excludes outright 「국민건강보험 관련 법령에 따라 국민건강보험공단으로부터 사전 또는 사후
  환급이 가능한 금액(본인부담금 상한제)」. **The 실손 급여 claim is therefore capped from below
  by the public scheme**, and the cap is income-related — see §10.
- The 표준약관 requires the insurer to explain this specifically at point of sale
  [S1 제5조의2], and reproduces the then-current threshold range in a footnote: 「국민건강보험
  지역가입자의 세대별 보험료 부담수준 또는 직장가입자의 개인별 보험료 부담수준에 따라 …
  81만원~584만원 … (상기 예시금액은 2021.5월 기준)」 [S1].
- **Where NHI does not apply at all** (국민건강보험법 제5조·제53조·제54조, or the 의료급여법
  equivalents — e.g. suspension of entitlement), the reimbursement drops to **40%** of the
  amount actually borne, still within the annual limit [S1 제3조제3항제1호].
- **Run-off after termination.** An admission in progress when the contract ends continues to
  be covered for **180 days** from the day after termination; an outpatient course in progress
  is covered for visits within 180 days, to a maximum of **90 visits** [S1 제3조제4항·제5항].
  But 「종전 계약을 자동갱신하거나 같은 회사의 보험상품에 재가입하는 경우에는 종전 계약의
  보험기간을 연장하는 것으로 보아」 those run-off provisions **do not apply** — annual renewal
  and five-year re-entry are treated as continuations, not terminations [S1 제3조제6항]. The
  run-off limit is the unused remainder of the annual limit at the previous year end
  [S1 제5조제6항].
- **Counting visits.** Same-day 외래 plus 처방 at the same provider count as **one** visit,
  aggregated on the prescription date [S1 제3조제7항]. Two or more visits on one day for the
  same treatment purpose count as **one**, and 「공제금액은 2회 이상의 중복방문 의료기관 중
  가장 높은 공제금액을 적용합니다」 — the highest applicable deductible [S1 제3조제8항].
- **하나의 질병** is defined for the 질병급여 limb: 「발생 원인이 동일한 질병(의학상 중요한
  관련이 있는 질병은 하나의 질병으로 간주하며 …)」, and where unrelated conditions are treated
  at one visit they are treated as one disease [S1 제3조(2)제7항].
- **Organ transplant.** The cost of 장기등의 적출 및 이식 for the insured's own functional
  recovery, under the 장기등 이식에 관한 법률 제42조, is reimbursed on the ordinary basis
  [S1 제3조제9항, 본조신설 2021.7.1.].

### 5. 4세대 비급여 (rider) — reimbursement basis

All from S1, 실손의료보험 특별약관, cross-checked against R5 참고1.

- **입원.** 「'비급여 의료비(비급여병실료는 제외합니다)'(본인이 실제로 부담한 금액을
  말합니다)의 70%에 해당하는 금액」 — a **30% 자기부담률** [S1 특별약관 제3조].
- **상급병실료 차액 (private-room differential).** 「비급여 병실료의 50%. 다만, 1일 평균금액
  10만원을 한도로 하며, 1일 평균금액은 입원기간 동안 비급여 병실료 전체를 총 입원일수로 나누어
  산출합니다」 — 50% of the non-covered room charge, capped at **₩100,000 per day averaged over
  the whole admission** [S1]. The averaging convention matters: a single expensive night inside
  a long stay is smoothed against the stay length, not capped night by night.
- **통원.** Per visit, non-covered spend less 「3만원과 보장대상 의료비의 30% 중 큰 금액」 —
  `max(₩30,000, 30%)` — and 「매년 계약해당일부터 1년간 통원 **100회**를 한도로 합니다」 [S1].
  **The 100-visit annual cap is on the 비급여 side only.**
- **Annual limits.** ₩50,000,000 (5천만원) per 보장종목 (상해비급여 / 질병비급여), inpatient
  and outpatient combined; ₩200,000 (20만원) per visit; and the 3대비급여 items carry their own
  limits instead [S1 특별약관 제5조].
- **The whole-contract annual limit is therefore ₩100,000,000 (1억원)** when both parts are
  held — the launch release states it as 「연간 보장한도도 기존과 유사하게 1억원 수준(급여
  5천만원, 비급여 5천만원)으로 책정」, with the calibration footnote that in 2019 the
  proportion of insureds receiving more than ₩50,000,000 of claims was **0.005%** of all
  policyholders [R1]. That single figure is the best public evidence on the thickness of the
  claim-size tail.
- **NHI-inapplicable case**: 40%, as on the 급여 side [S1 특별약관 제3조제8항].
- Run-off, renewal and re-entry treatment: identical to the 급여 side [S1 특별약관 제3조].
- Visit counting: same-day 외래+처방 aggregate to one visit; two treatments in one day for the
  same purpose count as one [S1 특별약관 제3조제6항·제7항]. Note that the deductible-is-highest
  rule stated on the 급여 side is **not** repeated on the 비급여 side, because the 비급여
  deductible does not vary by provider — it is a flat ₩30,000 floor everywhere [S1 <표1>].

### 6. 4세대 3대비급여 — the three named non-covered treatment classes

This is the sharpest, most model-relevant part of the wording. S1 특별약관 제3조 (3)3대비급여
제1항 <표1> gives 공제금액 and 보장한도 together:

| 구분 | 공제금액 | 보장한도 |
|---|---|---|
| 도수치료·체외충격파치료·증식치료 | 1회당 3만원과 보장대상의료비의 30% 중 큰 금액 | 계약일 또는 매년 계약해당일부터 1년 단위로 각 상해·질병 치료행위를 합산하여 **350만원** 이내에서 **50회**까지 |
| 주사료 | 1회당 3만원과 보장대상의료비의 30% 중 큰 금액 | 1년 단위로 합산하여 **250만원** 이내에서 **50회**까지 |
| 자기공명영상진단 (MRI/MRA) | 1회당 3만원과 보장대상의료비의 30% 중 큰 금액 | 1년 단위로 합산하여 **300만원** 이내에서 (횟수 제한 없음) |

- In won: ₩3,500,000 / ₩2,500,000 / ₩3,000,000 per policy year, with 50 / 50 / unlimited
  treatments. The deductible is `max(₩30,000, 30%)` on every one of the three, per treatment.
- **The 10-visit re-assessment rule.** The footnote to the table: 「도수치료·체외충격파치료·
  증식치료의 각 치료횟수를 합산하여 최초 10회 보장하고, 이후 객관적이고 일반적으로 인정되는
  검사결과 등을 토대로 증상의 개선, 병변호전 등이 확인된 경우에 한하여 10회 단위로 연간
  50회까지 보상합니다」 [S1]. The three treatments share **one** 50-visit counter, and cover
  beyond the first 10 is conditional and re-tested every 10.
- The clinical test is specified in the wording: 「기능적 회복 및 호전여부는 관절가동(ROM),
  통증평가척도, 자세평가 및 근력 검사(MMT)를 포함한 이학적 검사, 초음파 검사 등을 통해 해당
  부위의 체절기능부전(Somatic dysfunction) 등을 평가한 결과로 판단합니다」, and if beneficiary
  and insurer cannot agree, they jointly appoint a third party — 「제3자는 의료법
  제3조(의료기관) 의 종합병원 소속 전문의 중에 정하며, 보험금 지급사유 판정에 드는 의료비용은
  회사가 전액 부담합니다」 [S1]. The FAQ adds that the cost of the assessment tests themselves
  is covered [R2].
- **The limit that binds first stops cover for the rest of the policy year, and only the policy
  anniversary restores it.** The wording carries two worked examples: (i) where the ₩3,500,000
  is exhausted after 30 treatments on 2022-10-31, cover is excluded for the following 151 days
  and resumes at the 계약해당일 2023-04-01; (ii) where 50 treatments are used but only
  ₩3,000,000 paid, cover is excluded for the following 182 days from 2022-10-01 [S1]. **Both
  the money limit and the count limit are hard annual gates, and neither is pro-rated.**
- **Counting rules inside 3대비급여** [S1 특별약관 제3조(3)제4항]:
  - Two or more of 도수/체외충격파/증식 at one visit or admission, or the same one twice — 「각
    치료행위를 1회로 보고 각각 제1항에서 정한 1회당 공제금액 및 보상한도를 적용합니다」. Each
    act is separately counted **and separately deducted**.
  - Two or more injections at one visit or admission — **one** [제4항제2호].
  - MRI at two or more sites, or the same site twice — **each is a separate act**, each
    carrying its own deductible [제4항제3호].
  - 「1회 입원」 means an unbroken admission, including a same-day transfer to another provider
    for the same condition; a re-admission after discharge is a fresh admission even for the
    same cause [제5항].
- **Injection carve-out.** 「주사료에서 항암제, 항생제(항진균제 포함), 희귀의약품을 위해 사용된
  비급여 주사료는 … (1)상해비급여 또는 (2)질병비급여에서 보상합니다」
  [S1 특별약관 제3조(3) 제2항] — oncology, anti-infective and orphan-drug injections come
  **out** of the ₩2,500,000 sub-limit and go into the main ₩50,000,000 non-covered limit. Each
  of the three categories is defined by reference to a 식품의약품안전처 classification
  instrument [S1 특별약관 제2조].
- 「주사료」 itself means 「주사치료시 사용된 행위, 약제 및 치료재료대」 — the procedure, the
  drug and the consumables together [S1 특별약관 제2조].
- **도수치료** is defined as 「치료자가 손(정형용 교정장치 장비 등의 도움을 받는 경우를
  포함합니다)을 이용해서 환자의 근골격계통(관절, 근육, 연부조직, 림프절 등)의 기능 개선 및
  통증감소를 위하여 실시하는 치료행위」, with a footnote restricting it to treatment by a
  doctor or by a physiotherapist under a doctor's direction [S1 특별약관 제2조]. 체외충격파치료
  excludes lithotripsy (체외충격파쇄석술). 증식치료 is prolotherapy.

### 7. 비급여 할인·할증 — the differential renewal premium

The mechanism that makes this contract unlike anything else in the repository: **the renewal
premium of the 비급여 rider is a function of the individual policyholder's own prior-year
non-covered claim amount.**

- **The wording** [S1 특별약관 제6조제3항], effective for the product from launch but suspended
  for three years:

  | 구분 | 1단계 (할인) | 2단계 (유지) | 3단계 (할증) | 4단계 (할증) | 5단계 (할증) |
  |---|---|---|---|---|---|
  | 보험료 갱신 전 12개월 이내 기간 동안 보험금 지급실적 | 0원 (지급실적 없음) | 0원 초과 ~ 100만원 미만 | 100만원 이상 ~ 150만원 미만 | 150만원 이상 ~ 300만원 미만 | 300만원 이상 |
  | 요율 상대도 | 할인 | **100%** | **200%** | **300%** | **400%** |

- Read the two ways the sources state it and reconcile them: the 표준약관 states the factor as
  a **요율 상대도** (a rate relativity) of 100 / 200 / 300 / 400% [S1]; the press releases
  state the same thing as a 할인·할증율 of − / +100% / +200% / +300% [R1] [R3]. They are the
  same numbers: band 3 pays **twice** the base rate, band 4 **three times**, band 5 **four
  times**.
- The relativity applies to the **순보험료** of the rider: 「보험료 갱신시 순보험료(특별약관의
  순보험료 총액을 대상으로 합니다)에 아래와 같이 적용할 수 있습니다」 [S1].
- **The discount factor is not fixed by the wording.** It is solved for: 「매년 상대도 적용
  전·후의 총 보험료 수준이 일치하도록 3~5단계의 할증대상자의 할증재원을 1단계(할인)
  대상자들에게 분배할 경우 산출됨」 [S1]. The scheme is **revenue-neutral within the rider**:
  the surcharge 收入 funds the discount. The launch release put the expected discount at 「5%
  내외」 and warned it would vary by carrier and by experience [R1]; R3 gives −5% as a 잠정
  figure; S3 writes it as 「α%」 in a carrier document.
- **The surcharge floor.** 「요율 상대도의 할증은 이 특별약관에 따른 보험금 지급실적이 연간
  100만원 이상인 계약에 한하여 적용」 [S1 특별약관 제6조제4항]. Below ₩1,000,000 of prior-year
  non-covered claims there is no surcharge at all.
- **Exemptions.** 「국민건강보험법상 산정특례대상질환(암질환, 뇌혈관질환, 심장질환,
  희귀난치성질환 등)으로 인한 비급여의료비 및 노인장기요양보험법상 장기요양대상자 중 1등급 또는
  2등급으로 판정받은 자에 대한 비급여의료비는 요율 상대도 계산시 보험금 지급실적에서
  제외합니다」 [S1 특별약관 제6조제3항]. The severely ill are exempt from the experience
  rating.
- **Effective date: 2024-07-01.** 「비급여 보험료 차등 적용은 충분한 통계 확보 등을 위하여 상품
  출시('21.7월) 이후 3년간 유예되어」 왔고 「'24.7.1일부터 … 적용」 [R3]. R1 had announced it
  as 「새로운 상품 출시 후, 3년이 경과한 시점부터 적용될 예정」.
- **Mechanics of the assessment window.** The FAQ states the base rule: 「보험료 갱신 前 12개월
  동안의 '비급여' 지급보험금을 기준으로 차년도 비급여 보험료가 결정됩니다」, and 「차년도
  비급여 보험료 = 기준보험료 × (1 + 할인·할증율)」 where 기준보험료 is 「가입자 전체의 손해율이
  반영된 보험료」 [R2]. R12 records the operational refinement — because renewal notices go out
  about a month ahead, the window used is 「계약해당일이 속한 달의 3개월 전 말일부터 직전
  1년간」. The 5세대 wording writes that refinement into the standard text: 「보험료 갱신 시점
  3개월 전 말일부터 직전 12개월 이내 기간 동안의 … 보험금 지급 실적」
  [S2 특별약관2 제6조제3항].
- **The band resets every year.** 「보험금 지급(사고) 이력이 1년마다 초기화됩니다 … `21년
  지급보험금을 많이 받은 경우 → `22년 보험료 할증, `22년 무사고 → `23년 보험료는 할인등급
  (1등급)으로 초기화」 [R2]. The band is therefore a **memoryless one-year-lookback state**,
  not a no-claims ladder: a single bad year cannot compound into a permanently higher premium.
- **Only the rider is surcharged.** 「비급여 특약 보험료만 할증되며 보험료 전체가 할증되는 것은
  아닙니다」 [R2].
- **Distribution across bands** — two published estimates, on different bases, both recorded:
  - Ex ante, from a 3세대 simulation before launch: 「할증구간(3~5등급) 대상자는 전체 가입자의
    **1.8%**」 [R1].
  - At commencement, per 금융위원회: 1등급 62.1%, 2등급 36.6%, 3등급 1.3% of the contracts
    assessed [R3].
  - Attributed by 보험연구원 to a 금융감독원 release of 2024-01-19: 1단계 **72.9%**, 2단계
    **25.3%**, 3단계 **0.8%**, 4단계 **0.7%**, 5단계 **0.3%** [R12]. The two 2024 sets differ
    (62.1/36.6/1.3 against 72.9/25.3/1.8-combined) and this file does not attempt to reconcile
    them; both are recorded with their attributions and the model treats the band distribution
    as `[std]` calibrated between them.
- **A worked example of the interaction**, from 보험연구원 quoting 금융위원회 [R12]:

  | 구분 | 최초계약 ('23.8.1.) | 1년 후 갱신 ('24.8.1.) | 2년 후 갱신 ('25.8.1.) |
  |---|---|---|---|
  | 주계약 (급여) | ₩5,000 | ₩5,000 | ₩5,000 |
  | 특약 (비급여) | ₩7,500 | ₩15,000 (+100%) | ₩7,150 (−5%) |
  | 합계 | ₩12,500 | ₩20,000 | ₩12,150 |
  | 직전 비급여 보험금 | ₩1,300,000 | 없음 | — |

  (Age and morbidity drift excluded from the illustration.)
- **The 무사고 할인 (no-claim discount) runs alongside and is a separate 10%.** 「직전 2년간
  비급여 보험금(4대 중증질환 치료를 위한 보험금은 제외) 미수령시 차기 1년간 보험료(급여(주계약)
  + 비급여(특약))의 10%를 할인」 [R1]. It applies to the **whole** premium, not just the rider,
  and it stacks with the band-1 discount: R1 prints a three-year timeline showing years 1 and 2
  giving only the ~5% rider discount and year 3 adding the 10% whole-premium discount.
- S3 gives a carrier's precise scope of the same discount on 5세대: 「직전 2년 간 유효한
  실손의료비 보험 계약에서 '무사고 판정기간' 동안 비급여 보험금 지급실적이 없는 경우
  영업보험료의 10%를 할인 … [단, 급여 의료비 중 본인부담금 및 실손의료보험 특별약관1(중증
  비급여 실손의료비)에서 보장하는 비급여 의료비에 대한 보험금은 제외, 특별약관2(비중증 비급여
  실손의료비)를 가입하지 않은 계약은 제외]」 [S3].
- The same carrier also gives a discount unrelated to experience: 「피보험자가 의료급여법상
  의료급여 수급권자임을 증명할 수 있는 서류를 제출한 경우 영업보험료의 5%를 할인」 [S3].

### 8. 1년 갱신 / 5년 재가입 — the renewal and re-entry architecture

This is the second structural peculiarity, and it is what makes the contract boundary a real
question rather than a formality.

- **The policy term is one year.** S5, a carrier wording, states it flatly: 「이 계약의
  보험기간은 1년으로 합니다」, with automatic renewal on the day after expiry unless the
  policyholder says otherwise, subject to three conditions — that the renewed term ends within
  the 보장내용변경주기, that the insured's age is within the company's range, and that the
  prior premium was fully paid [S5]. S3 confirms the same architecture for 5세대 and describes
  the product as 「1년만기 순수보장성 상품」 [S3].
- **Renewal re-rates.** 「갱신되는 계약의 보험료는 갱신일 현재의 보험요율에 관한 제도를
  반영하여 계산된 보험료를 적용하며, 그 보험료는 나이의 증가, 보험료산출에 관한 기초율의 변동 …
  등의 사유로 인하여 인상 또는 인하될 수 있습니다」 [S1 제30조제1항].
- **The renewal increase is capped at 25% a year, excluding the age effect.** 「갱신계약의
  보험료는 매년 최대 25% 범위(나이의 증가로 인한 보험료 증감분은 제외) 내에서 인상 또는 인하될
  수 있습니다. 다만, 회사가 금융위원회로부터 경영개선권고, 경영개선요구 또는 경영개선명령을
  받은 경우는 예외로 합니다」 [S1 제30조제2항]. On the rider the cap applies to the 「요율
  상대도 적용 전 보험료」 — i.e. **before** the experience relativity, so a band-5 policyholder
  can face 1.25 × 4.00 = 5.00× the previous year's base rate in a single step
  [S1 특별약관 제6조제2항]. R6 restates the cap as a live constraint: 「현재는 위험구분
  단위별로 실손보험료 인상률을 연 25%내로 제한」.
- **The standard wording's own renewal illustration** [S1 제30조], for an unnamed age, male,
  starting at ₩14,000 per month with the 25% maximum assumed every year and both parts held:

  | 구분 | XX세 | +1 | +2 | +3 | +4 | +5 |
  |---|---|---|---|---|---|---|
  | 나이증가분 (A) | — | 560 | 728 | 946 | 1,230 | 1,599 |
  | 기초율(위험률 등) 증가분 (B = 전년도 기준보험료 × 25%) | — | 3,640 | 4,732 | 6,152 | 7,997 | 10,396 |
  | 기준보험료 (C = 전년 C + A + B) | 14,000 | 18,200 | 23,660 | 30,758 | 39,985 | 51,980 |
  | 위 C에 직전 2년 무사고 10% 할인 적용 | — | — | (21,294) | (27,682) | (35,987) | (46,782) |

  The age loading in this illustration is a constant **4%** of the previous year's base premium
  (560/14,000 = 728/18,200 = … = 1,599/39,985 = 0.04). That is the only published age-slope
  datum found in any retrieved document, and it is a stylised illustration, not a rate table.
- **The 요율 상대도 version of the same illustration** [S1 특별약관 제6조] extends it across
  the five bands:

  | 단계 | +1 | +2 | +3 | +4 | +5 |
  |---|---|---|---|---|---|
  | 1단계 (상대도 95% 가정) | 17,756 | 23,083 (20,775) | 30,008 (27,007) | 39,011 (35,109) | 50,714 (45,642) |
  | 2단계 (100%) | 18,200 | 23,660 | 30,758 | 39,985 | 51,980 |
  | 3단계 (200%) | 27,073 | 35,194 | 45,753 | 59,478 | 77,322 |
  | 4단계 (300%) | 35,945 | 46,729 | 60,747 | 78,971 | 102,663 |
  | 5단계 (400%) | 44,818 | 58,263 | 75,742 | 98,464 | 128,003 |

  (Parenthesised values add the 10% 무사고 discount.) Note that the band multiplier applies
  only to the rider, which is why band 5 at 400% produces 44,818 rather than 4 × 18,200 =
  72,800: the 급여 main contract is unaffected. Solving `18,200 = g + n` and `44,818 = g + 4n`
  gives n = ₩8,873 and g = ₩9,327, a **48.8% rider share** in this illustration — a little
  below the 60% quoted in R2, but the same order.
- **재가입 (re-entry).** S1 제23조, 본조신설 2021.7.1., is the operative clause:
  - Conditions: the insured's age at re-entry is within the company's stated re-entry age
    range, and the prior contract's premium was fully paid [제1항].
  - 「이 경우 회사는 기존계약의 가입 이후 발생한 상해 또는 질병을 사유로 가입을 거절할 수
    없습니다」 — **no health underwriting at re-entry** [제1항]; and on expiry of automatic
    renewal the policyholder may take whichever 실손 product the company is then selling and
    「회사는 이를 거절할 수 없습니다」 [제2항].
  - The insurer must notify the policyholder **at least twice** before the 보장내용 변경주기
    ends, setting out the re-entry conditions, what has changed in cover, the premium level and
    the procedure [제3항].
  - If the insurer cannot obtain the policyholder's decision (including loss of contact), the
    contract is **extended on the previous terms** [제5항]; the policyholder may cancel that
    extension within **90 days** with a full refund of premium paid after extension [제6항];
    the extension runs to the date the insurer establishes the policyholder's intention —
    typically the date of the first claim — whereupon re-entry into the then-current product
    occurs and the old contract is terminated [제7항]. S3 adds a carrier cap on that limbo:
    「보험기간이 종료된 날로부터 1년 중 빠른 날까지」 [S3 제53조제7항].
- **The 재가입주기 (보장내용 변경주기) is 5 years for 4세대**, shortened from 15 [R1]:
  「건강보험정책 등 의료환경 변화에 적절히 대응할 수 있도록 재가입주기가 현행 15년에서 5년으로
  단축됩니다」. The FAQ gives the policy reason — faster propagation of NHI coverage changes
  into the private layer — and the reassurance that 「보험회사는 재가입주기 도래 時, 소비자의
  과거 사고 이력 등을 이유로 재가입을 거절하지 못합니다」 [R2].
- S3 states a carrier's full re-entry envelope for 5세대: 「보장내용 변경주기는 최대 5년,
  재가입이 가능한 나이는 최고 99세이며, 보장받을 수 있는 최대 기간은 보험나이 100세
  계약해당일로 합니다」 [S3]. S4 shows the 2세대 envelope for comparison — 재가입주기 15년,
  재가입 나이 15–99세, cover to the 보험나이 100세 계약해당일 [S4].
- **보험나이 (insurance age).** 「이 약관에서 피보험자의 나이는 보험나이를 기준으로 합니다. …
  보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고 6개월
  이상의 끝수는 1년으로 하여 계산하며, 이후 매년 계약해당일에 나이가 증가하는 것으로 합니다」,
  with the worked example 「생년월일 1988년 10월 2일, 계약일 2014년 4월 13일 ⇒ 25년 6월 11일 =
  26세」 [S1 제21조]. **The model prices on 보험나이 and quotes statistics on 만나이; the
  registry metadata must say so.**

### 9. 5세대 (2026-05-06) — what replaced it

Recorded in full because it is the live market, because R5's comparison table is the cleanest
statement of the 4세대 parameters, and because the 4세대 book re-enters into it from 2026-07.

- **Structure.** 주계약 (급여) + **특약1 (중증 비급여)** + **특약2 (비중증 비급여)**, all three
  separately selectable: 「소비자는 급여 의료비를 보장하는 기본형 실손보험에만 가입할 수
  있으며, 필요에 따라 특약1 또는 특약2만 선택하여 가입하거나 특약 1·2 모두 가입할 수도 있음」,
  giving four permitted combinations [R6].
- **중증 is defined by the public system, not by the wording.** 「암, 뇌혈관·심장질환,
  희귀난치성질환 등 건강보험 산정특례(본인일부부담금 산정특례에 관한 기준, 복지부 고시) 대상
  질환 → 보건당국이 대상 질환 조정시 실손도 자동 연동」 [R5]. S2 특별약관1 제2조 gives the
  operative definition: 「「본인일부부담금 산정특례에 관한 기준(보건복지부 고시)」 제4조부터
  제5조의3까지에 따른 산정특례 대상인 질환(암, 뇌혈관질환, 심장질환, 희귀질환, 중증난치질환,
  중증화상, 중증외상, 결핵, 잠복결핵 등)」, and defines 「산정특례 대상 질환으로 인한 치료」 to
  include complications with a clear medical causal link but to exclude treatment of the
  complication alone once the index condition's treatment has ended.
- **급여 (주계약)** [S2] [R5 참고1]:
  - 입원 자기부담률 **20%** — unchanged from 4세대.
  - 통원 deductible becomes a **three-way maximum**: `Max[보장대상의료비 × 건강보험 본인부담률,
    보장대상의료비 × 20%, ₩10,000 (병·의원+약국) 또는 ₩20,000 (상급·종합+약국)]`.
  - The 건강보험 본인부담률 is **computed from the receipt** and the formula is in the wording:
    「급여 일부 본인부담 항목의 본인부담금 합계 금액 ÷ (급여 일부 본인부담 항목의 본인부담금
    합계 금액 + 급여 공단부담금 합계 금액)」, with 100%-본인부담 items excluded from both
    numerator and denominator and from cover [S2 제3조 <표1> 주].
  - The 손해보험협회 restates the same formula in its consumer disclosure as
    `Max[보장대상의료비 × 건강보험본인부담률, 보장대상의료비 × 20%, 1만원(병·의원) or
    2만원(상급종합·종합병원)]`, with 기본형 limits of 연간 5천만원 and 통원 회당 20만원, 특약1
    5천만원 and 특약2 1천만원 [S7].
  - R5 works an example: outpatient covered spend ₩500,000, of which NHIS bears ₩300,000 and
    the patient ₩200,000, so the 본인부담률 is 40%; the three candidates are ₩200,000 × 40% =
    ₩80,000, ₩200,000 × 20% = ₩40,000, and ₩10,000; the deductible is ₩80,000 and the claim is
    ₩120,000.
  - Limits unchanged: 상해·질병 각 5천만원 (입·통원 합산), 통원 회당 20만원, **입원 연간
    자기부담한도 200만원** [R5 참고1].
  - **New cover**: 임신·출산 (O00–O99) where the policy was taken out at least 280 days before
    the expected delivery date, and 정신발달장애 (F80–F89) for in-utero policies to 보험나이 18
    [R5] [S2 제3조제10항, 신설 2026.5.6.].
- **특약1 (중증 비급여)** [S2] [R5 참고1] — the 4세대 rider, restricted to 산정특례 conditions:
  - 입원 30%; 상급병실료 차액 50% capped at ₩100,000/day averaged; 통원 `Max[30%, ₩30,000]`.
  - 상해·질병 각 5천만원 (입·통원 합산); 통원 회당 20만원, **연간 100회**.
  - 3대비급여 carried over with the same money and count limits, but renamed and slightly
    re-scoped: **근골격계 이학요법치료·체외충격파치료** 연 350만원 / 50회; **비급여주사료** 연
    250만원 / 50회; **MRI·MRA** 연 300만원, no count limit.
  - 근골격계 이학요법치료 is now defined by reference to the fee schedule rather than by naming
    three procedures: 「「건강보험 행위 급여·비급여 목록표 및 급여 상대가치점수」 내 비급여
    목록 중 근골격계 질환의 기능 개선 및 통증감소를 위하여 실시하는 치료행위 일체(예시:
    FIMS(기능적 근육내 자극치료), 신장분사치료, 도수치료, 증식치료, 비침습적 무통증 신호요법
    등)」 [S2]. That is a deliberate anti-substitution definition: it closes the gap that let
    providers re-label 도수치료 as something outside the 4세대 three-procedure list.
  - **New: an annual out-of-pocket cap on severe inpatient treatment.** 「입원의 경우
    상급종합병원·종합병원의 상해·질병 및 3대 비급여 의료비(3대 비급여 중 근골격계
    이학요법치료·체외충격파치료 및 주사료 관련 비급여 의료비는 제외) 중 공제금액이 계약일 또는
    매년 계약해당일부터 기산하여 연간 500만원을 초과하는 때에는 500만원까지 공제합니다」
    [S2 특별약관1 제5조제5항]. ₩5,000,000 (500만원) per policy year.
  - 특약1 is **not** subject to the 할인·할증 [R5 참고1] [S2].
- **특약2 (비중증 비급여)** [S2] [R5 참고1]:
  - 입원 **50%**; 통원 `Max[50%, ₩50,000]`; 비급여 MRI/MRA `Max[50%, ₩50,000]`.
  - 상해·질병 각 **1천만원** (입·통원 합산); 통원 **1일당** 20만원 (연간 **100일**) — note the
    change from *per visit* to *per day*; 병·의원 입원 **회당 300만원**; MRI/MRA 연 200만원.
  - **Excluded outright**: 근골격계 이학요법치료, 체외충격파치료, 비급여 주사제, 미등재
    신의료기술 (including 첨단재생의료) [R5] [S2 제1조].
  - 특약2 **is** subject to the 할인·할증, and the exemption list narrows to 장기요양 1·2등급
    only — because 산정특례 conditions are now in 특약1 and outside 특약2 altogether
    [S2 특별약관2 제6조제3항].
  - S3 records the carrier commencement date for the differential on new 5세대 business:
    「(2028년 5월 6일부터 적용)」 — again a two-year deferral to build statistics [S3].
- **Both 특약1 and 특약2 exclude treatments graded D (권고하지 않음) by the
  한국보건의료연구원's 의료기술 재평가** [R5].
- **Premium effect**: 「5세대 실손보험료는 현행 4세대 대비 약 30% 저렴하며, 1·2세대 상품보다는
  최소 50% 이상 저렴」; base + 특약1 only is 「현행 4세대 대비 약 50% 수준」 [R5].
- **Selectable 보험가입금액**, from a carrier [S3]: 급여 and 중증 covers at ₩50,000,000 /
  ₩30,000,000 / ₩10,000,000 with per-visit caps ₩200,000 / ₩150,000 / ₩100,000; 특약2 at
  ₩10,000,000 / ₩6,000,000 / ₩2,000,000 with per-day caps ₩200,000 / ₩150,000 / ₩100,000.
- **Conversion**: existing 1–4세대 policyholders may convert without underwriting, with a
  6-month withdrawal right (unconditional within 3 months) [R5] [R6].
- **선택형 할인 특약 and 계약전환 할인 from 2026-11**, for the pre-2013-03 block with no
  re-entry clause (~17 million insureds) [R5] [R6]:
  - 선택형 할인 특약 options: ① 근골격계 물리치료·체외충격파치료 및 비급여 주사제 면책; ②
    비급여 MRI/MRA 면책; ③ 자기부담률 20% 적용. All three together ≈ **30–40%** discount (1세대
    ~40%대, 2세대 ~30%대). Option ① alone ≈ 20% [R6]. Available once only.
  - 계약전환 할인 (계약재매입): convert to 5세대 and receive a discount on the 5세대 premium —
    illustrated as **50% for three years** [R5].
  - Worked 60대 여성 example, 6개 대형 손보사 기준 [R5 참고2] [R6]:

    | 구분 | 현재 월보험료 | 선택형 특약 (옵션 1~3 전부) | 전환할인 (전환 후 3년간) | 5세대 전환 |
    |---|---|---|---|---|
    | 1세대 | ₩178,489 | ₩107,093 (−40.0%) | ₩21,270 (−88.1%) | ₩42,539 (−76.2%) |
    | 2세대 | ₩126,773 | ₩88,741 (−30.0%) | ₩21,270 (−83.2%) | ₩42,539 (−66.4%) |

  - And a 40대 남성 comparison: 1세대 ₩78,000/month against 5세대 ₩16,000/month [R5 참고2].
- **관리급여 (managed benefit)** — a new NHI category that will migrate some 비급여 items into
  the covered system at a **95% co-payment**. R6's table of the whole taxonomy:

  | 구분 | 정의 | 자기부담률 |
  |---|---|---|
  | 급여 (요양급여) | 건강보험이 통상 적용되는 기본 진료 | 입원 20, 통원 30~60 |
  | 선별급여 | 보장 필요성은 있지만 경제성·치료 효과성이 불확실하거나 추가검증이 필요한 진료 | 100 이하 (통상 30~80) |
  | 관리급여 | 과잉·남용 우려가 큰 일부 비급여 중 가격·기준·이용량 관리가 필요한 진료 | 95 |
  | 비급여 | 급여에서 제외되는 진료 | 100 |

  If 도수치료 becomes 관리급여, it moves out of the 비급여 rider and into the 급여 main
  contract, where inpatient reimbursement would be of 20% of the co-payment but outpatient
  would face a 95% 본인부담률 [R6]. **A model that assumes the 급여/비급여 boundary is static
  will be wrong within the projection horizon.**

### 10. The public layer underneath — 국민건강보험 급여 / 비급여 and 본인부담상한제

- **Coverage ratio.** 건강보험 보장률 was **64.9%** in 2024, unchanged on 2023; 법정 본인부담률
  19.3% (−0.6%p); **비급여 본인부담률 15.8%** (+0.6%p) [R9]. The definitional formula is
  printed: `보장률 = 보험자부담금 ÷ (보험자부담금 + 법정본인부담금 + 비급여진료비)`, with
  cosmetic, health-promotion and preventive non-covered treatment excluded from the denominator
  [R9].
- **The three-way split of national spend, 2024** [R9]: total ₩138.6조; 보험자부담금 ₩90.0조;
  법정 본인부담금 ₩26.8조; 비급여 진료비 ₩21.8조. The 실손 addressable base is the last two
  together — **₩48.6조** — of which 실손 actually paid ₩15.2조 in 2024 [R8], i.e. **31.3%**.
- Time series of the same three components [R9]:

  | 연도 | 보험자부담금 | 법정본인부담금 | 비급여진료비 | 총 진료비 |
  |---|---|---|---|---|
  | 2019 | 66.3조 | 20.3조 | 16.6조 | 103.3조 |
  | 2020 | 67.1조 | 20.1조 | 15.6조 | 102.8조 |
  | 2021 | 71.6조 | 22.1조 | 17.3조 | 111.1조 |
  | 2022 | 79.2조 | 23.7조 | 17.6조 | 120.6조 |
  | 2023 | 86.3조 | 26.5조 | 20.2조 | 133.0조 |
  | 2024 | 90.0조 | 26.8조 | 21.8조 | 138.6조 |

  2024 growth rates: +4.3% / +1.0% / **+8.1%** / +4.2% [R9]. **비급여 is growing at roughly
  twice the rate of the total**, and that is the driver of the product's loss ratio.
- **Coverage ratio and 비급여 share by provider type, 2024** [R9] — this is what makes provider
  mix a first-order model variable:

  | 요양기관 종 | 건강보험 보장률 | 법정 본인부담률 | 비급여 본인부담률 |
  |---|---|---|---|
  | 상급종합 | 72.2% | 19.1% | 8.7% |
  | 종합병원 | 66.7% | 21.7% | 11.6% |
  | 병원 | 51.1% | 18.1% | **30.8%** |
  | 요양병원 | 67.3% | 18.5% | 14.2% |
  | 의원 | 57.5% | 20.1% | 22.4% |
  | 약국 | 69.1% | 28.0% | 2.9% |

- **Coverage ratio by age band, 2024** [R9]: 0–5세 70.4%; 6–15세 52.7%; 16–64세 58.0%; 65세
  이상 69.8%. 비급여 본인부담률: 17.3% / 23.9% / 22.1% / 12.5%. The 65+ 비급여 rate rose from
  11.8% to 12.5% on the back of cataract and musculoskeletal consumables, and the 치료재료료
  share within 65+ 비급여 jumped from 10.4% to 16.7% [R9].
- **Severe-disease coverage**: 4대중증질환 81.0% (−0.8%p); 암 75.0% (−1.3%p); the top-30
  per-capita high-cost conditions 80.2%; top-50 78.5% [R9].
- **The 비필수항목-adjusted ratio.** Removing 제증명수수료, 영양주사, 도수치료 and 상급병실료
  from the denominator raises the 2024 ratio from 64.9% to **66.6%** [R9]. The public
  statistician and the insurance supervisor are pointing at the same four items.
- **Outpatient co-payment percentages** (국민건강보험법 시행령 별표2, as published by 심평원)
  [R11]:
  - 상급종합병원: 진찰료 100% + 60% of the remainder.
  - 종합병원: 50% (동지역) / 45% (읍·면지역).
  - 병원급: 40% (동지역) / 35% (읍·면지역).
  - 의원급: 30% (under 65).
  - 약국: 처방조제 30%; 직접조제 40%.
  - Inpatient: 20% of the total covered cost (plus 50% of the meal charge) [R11] [R6].
- **산정특례 co-payments**: 5% for cancer and severe burns; 10% for rare disease, severe
  intractable disease and severe dementia [unverified] — the figure comes from a search summary
  of the 국민건강보험공단 explanation page, which was not itself opened; the **existence** and
  the **scope** of the 산정특례 categories are verified from S2 특별약관1 제2조, which
  enumerates them by 고시 조문, but the percentages are not.
- **본인부담상한제 (annual out-of-pocket ceiling).** Definition: 「과도한 의료비로 인한 가계
  부담을 덜어주기 위하여 건강보험 본인일부부담금 총액이 본인부담상한액을 초과하는 경우 초과액을
  공단에서 부담하는 제도」, operated as 사전급여 and 사후환급, over the calendar year 1 January
  to 31 December, with the individual ceiling set by the policyholder's own NHI contribution
  decile [R10]. Thresholds, in 만원 [R10]:

  | 연도 | 1분위 | 2~3분위 | 4~5분위 | 6~7분위 | 8분위 | 9분위 | 10분위 |
  |---|---|---|---|---|---|---|---|
  | 2023 | 87 | 108 | 162 | 303 | 414 | 497 | 780 |
  | 2024 | 87 | 108 | 167 | 313 | 428 | 514 | 808 |
  | 2025 | 89 | 110 | 170 | 320 | 437 | 525 | 826 |
  | 2026 | 90 | 112 | 173 | 326 | 446 | 536 | 843 |

  With a higher scale where the insured spent more than 120 days in a 요양병원 — for 2026: 143
  / 181 / 245 / 404 / 580 / 698 / 1,096 만원 [R10].
- **Consequence for the model.** The 급여 half of the claim is bounded above, per insured per
  calendar year, at roughly (본인부담상한액 × 80%) plus the ₩2,000,000 excess mechanism —
  because everything above the ceiling is refunded by NHIS and is therefore excluded from cover
  by S1 제4조제3항제1호. In 2026 that means a 1분위 insured's 급여 inpatient claim cannot
  materially exceed ₩900,000 × 80% = ₩720,000 for the year, while a 10분위 insured's runs to
  ₩8,430,000 × 80% = ₩6,744,000. **The 급여 claim distribution is truncated, and truncated
  differently by income decile.** The 비급여 half has no such truncation, which is exactly why
  it is 57.1% of claims [R7] against a 15.8% share of national spend [R9].
- The mirror provisions on the 의료급여 side, reproduced verbatim in the wording [S1 제5조의2]:
  본인부담금 보상제 pays 50% of the excess over ₩20,000 (1종) or ₩200,000 (2종) per 30 days;
  본인부담금 상한제 pays the whole excess over ₩50,000 per 30 days (1종) or ₩800,000 a year
  (2종), rising to ₩1,200,000 where the insured spent more than 240 days a year in a 요양병원.

### 11. In-force counts and market size

All from R7 unless marked.

- **Total individual 실손 policies in force**: 3,622만건 at 2025-12-31 (+26만건, +0.7% on
  2024); 3,596만건 at 2024-12-31; 3,579만건 at 2023-12-31. Group 실손 and 공제 are excluded
  from the 统计 [R7].
- By carrier type at 2025-12-31: 손보사 3,028만건 (+30만건, +1.0%); 생보사 594만건 (−4만건,
  −0.7%).
- **By generation** (단위: 만건):

  | 세대 | 2023 | 2024 | 2025 | 증감 2025 vs 2024 | 2025 점유율 |
  |---|---|---|---|---|---|
  | 1세대 | 682 | 638 | 618 | △20 (△3.1%) | 17.1% |
  | 2세대 | 1,623 | 1,552 | 1,494 | △58 (△3.7%) | 41.2% |
  | 3세대 | 826 | 804 | 783 | △21 (△2.6%) | 21.6% |
  | 4세대 | 376 | 525 | 641 | 116 (22.1%) | 17.7% |
  | 노후·유병력자 등 | — | 77 (2.1%) | 86 | — | 2.4% |

  [R7] for 2023–2025 and the 2025 shares; [R8] for the 2024 노후·유병력자 figure.
- The 1–3세대 block is running off at 99만건 (3.3%) a year in 2025, down from 137만건 (4.4%) in
  2024 [R7]. **That decay rate is the best public proxy for a total termination rate on a
  mature 실손 book** — lapse plus death plus conversion — and it is remarkably low.
- **Insured persons**: about **4천만명** at 2024-12-31 [R4]; 3,900만명 (about **75% of the
  population**) at 2020-12-31 [R1]. Policy count exceeds insured count because of duplicate
  cover, which the wording addresses through 비례보상 [S1 제37조] [S3].
- Generation shares at 2020-12-31, before 4세대 existed: 1세대 24.4%, 2세대 53.7%, 3세대 20.3%
  [R1].
- Cover among the elderly is thin: 「70대 38.1%, 80세 이상 4.4%」 [R17].

### 12. Loss ratio, premium and result — the experience statistics

This is the section the model's `[std]` assumptions are anchored on. All from R7 unless marked.

- **경과손해율 (earned loss ratio) = 발생손해액 ÷ 보험료수익**, and the supervisor states the
  break-even point: 「손익분기점은 약 **85%** 수준」 [R7]. The gap between 85% and 100% is
  손해조사비 and 사업비 — R7 quantifies the 2025 figure as 「지급보험금 이외에 손해조사비 및
  사업비 등 비용(약 2.9조원)」 on ₩18.0조 of premium, i.e. **16.1% of premium**.

  | 연도 | 전체 | 생보사 | 손보사 |
  |---|---|---|---|
  | 2022 | 101.3% | 84.7% | 104.8% |
  | 2023 | 103.4% | 86.4% | 107.1% |
  | 2024 | 99.3% | 86.5% | 102.0% |
  | 2025 | 101.0% | — | — |

  [R8] for 2022–2024 by carrier type; [R7] for 2025 total.
- **By generation**:

  | 세대 | 2022 | 2023 | 2024 | 2025 |
  |---|---|---|---|---|
  | 1세대 | 113.2% | 110.5% | 97.7% | 102.3% |
  | 2세대 | 93.2% | 92.7% | 92.5% | 93.1% |
  | 3세대 | 118.7% | 137.2%/137.3% | 128.5% | 120.3% |
  | 4세대 | 91.5% | 113.8% | 111.9% | 115.1% |

  [R8] for 2022–2024, [R7] for 2023–2025. (R7 and R8 differ by 0.1pp on 3세대 2023 — 137.3% and
  137.2% respectively; both are stated as 잠정.)
- **The 3세대 and 4세대 pattern has a regulatory cause, not only an experience cause.**
  보험업감독규정 was read conservatively as forbidding a rate change within five years of a new
  product's launch, so 3세대 first re-rated in 2023-01 and 4세대 in 2025 [R8] [R12]. 4세대 was
  moreover priced 「'16년도 2세대 요율을 기초로 하는 등 다소 낮은 가격으로 설계」 because 3세대
  had not yet re-rated when 4세대 launched [R12]. **A newly launched Korean 실손 generation is
  systematically under-priced for its first several years by construction**, and the model's
  premium basis must reflect that rather than assume a self-supporting rate from t = 0.
- **4세대 loss ratio split 급여 / 비급여**, from 손해보험회사 statistics [R12]:

  | 기간 | 급여 | 비급여 | 합산 |
  |---|---|---|---|
  | 2022 상반기 | 97.5% | 73.0% | 82.8% |
  | 2023 상반기 | 139.2% | 100.1% | 115.9% |
  | 2024 상반기 | 154.6% | 114.2% | 130.6% |

  The 급여 main contract has run **worse** than the 비급여 rider on 4세대 throughout — which is
  the opposite of the market narrative and is exactly why 5세대 changed the 급여 통원
  deductible as well as the 비급여 terms.
- **Premium income** (단위: 억원) [R7] [R8]:

  | 연도 | 전체 | 생보사 | 손보사 |
  |---|---|---|---|
  | 2022 | 131,885 | 23,319 | 108,566 |
  | 2023 | 144,429 | 25,808 | 118,621 |
  | 2024 | 163,364 | 29,086 | 134,278 |
  | 2025 | 179,649 | 31,909 | 147,740 |

- **Insurance result (보험손익 = 보험료수익 − 발생손해액 − 실제사업비)** (단위: 억원)
  [R7] [R8]:

  | 연도 | 전체 | 생보사 | 손보사 |
  |---|---|---|---|
  | 2022 | △15,301 | 591 | △15,892 |
  | 2023 | △19,747 | 91 | △19,838 |
  | 2024 | △16,226 | △437 | △15,788 |
  | 2025 | △18,700 (△1.87조) | — | — |

- **Claims paid** [R7] [R8] (단위: 억원):

  | 연도 | 전체 | 급여 | 비급여 | 비급여 비중 |
  |---|---|---|---|---|
  | 2022 | 128,868 | 50,281 | 78,587 | 61.0% |
  | 2023 | 140,813 | 58,780 | 82,033 | 58.3% |
  | 2024 | 152,234 | 63,306 | 88,927 | 58.4% |
  | 2025 | 169,653 / 170,000 | 73,000 | 97,000 | 57.1% |

  (R7 gives 2025 as 17.0조 with 급여 7.3조 / 42.9% and 비급여 9.7조 / 57.1%, and separately a
  provider-type table totalling 169,653억. The two are the same number rounded differently.)
- **Claims by treatment category, 2025** (단위: 백억원) [R7]:

  | 항목 | 2023 | 2024 | 2025 | 비중 | 증감 |
  |---|---|---|---|---|---|
  | 전체 | 1,408 | 1,522 | 1,697 | 100% | 175 (11.4%) |
  | 근골격계 질환 (도수치료 등) | 222 | 253 | 269 | 15.8% | 16 (6.3%) |
  | 통원 비급여주사제 (영양제 등) | 73 | 79 | 104 | 6.1% | 25 (31.9%) |
  | 암, 뇌·심혈관질환 관련 | 191 | 215 | 255 | 15.0% | 40 (18.9%) |
  | 로봇수술 | 20 | 27 | 47 | 2.7% | 20 (72.4%) |
  | 전립선결찰술 | 3 | 4 | 7 | 0.4% | 3 (64.6%) |
  | 하이푸시술 | 14 | 15 | 22 | 1.3% | 7 (46.0%) |
  | 척추 관련 수술 (신경성형술 등) | 36 | 41 | 39 | 2.3% | △2 (△3.8%) |

  The supervisor's headline: 「대표적 비중증 치료인 근골격계질환(도수치료 등) 관련 보험금은
  2.7조원으로 중증질환인 암, 뇌·심혈관질환 관련 보험금(2.6조원)을 상회」 [R7]. And R6 gives the
  combined figure the 5세대 exclusions target: 「'25년 실손보험금 중 비중: 비급여 근골격계
  물리치료 및 주사제 **27.3%**, 암관련 치료비 12.8%」.
- **2024 category detail** [R8] (단위: 억원): 비급여 주사제 관련 28,092 (18.5%, +15.8%);
  근골격계 물리치료 관련 26,321 (17.3%, +14.0%); 암 치료 관련 15,887 (10.4%, +13.3%). Plus two
  fast-growing single procedures: 무릎줄기세포주사 147 → 458 → 645억 (2022→2024) and
  전립선결찰술 262 → 340 → 438억. And the 한방 channel: 한방병원 5,115 → 5,939억 (+16.1%),
  한의원 1,175 → 1,511억 (+28.6%).
- **Claims by provider type, 2025** (단위: 억원) [R7]:

  | 구분 | 상급종합병원 | 종합병원 | 병원 | 요양병원 | 의원 | 기타 | 합계 |
  |---|---|---|---|---|---|---|---|
  | 전체 | 25,490 | 29,908 | 36,909 | 4,785 | 54,340 | 18,221 | 169,653 |
  | 비급여 | 10,510 | 12,643 | 26,063 | 3,995 | 35,983 | 7,690 | 96,884 |
  | 비급여 비중 | 41.2% | 42.3% | 70.6% | 83.5% | 66.2% | 42.2% | 57.1% |

  Shares of total claims: 의원 32.0%, 병원 21.8%, 종합병원 17.6%, 상급종합 15.0% [R7]; the 2024
  equivalents were 32.2 / 23.3 / 17.3 / 14.0 [R8]. Compare NHIS's own 2024 covered-spend
  shares: 상급종합 22.3%, 종합병원 21.4%, 병원 10.7%, 의원 27.9% [R7]. **실손 money is
  concentrated in 병원 and 의원 far more than public money is**, because that is where 비급여
  is.
- **Per-policy claim amounts, 2025** [R7]: 1세대 74만원, 2세대 49만원, 3세대 36만원, 4세대
  29만원 a year. Grossing the 비급여 element back up for the co-payment gives an estimated
  per-insured 비급여 spend of 1세대 44만원, 2세대 35만원, 3세대 27만원, 4세대 21만원.
- **Per-policy 비급여 claim amounts, 2022–2024** [R8] (만원): 1세대 36.1 / 36.3 / 40.0; 2세대
  21.9 / 23.1 / 25.4; 3세대 13.1 / 16.4 / 18.2; 4세대 7.4 / 10.9 / 13.6.
- **Concentration.** 「계약자의 9%가 보험금의 80%를 수령」 and 「계약자의 65%가 보험금을
  미수령」 [R4]; restated at 2025-12-31 as 「실손보험 가입자의 65%는 보험금 수령 없이 보험료만
  납부하고 있으며, 보험금 수령 상위 10%에게 전체 보험금의 약 74% 지급(14개사)」 [R5] [R6]. **A
  model that projects a mean claim per policy without a zero-claim mass of roughly 65% will
  misstate everything downstream of the deductible.**
- **Claim size distribution by generation, 2023**, from ten 손해보험사 [R12] — proportion of
  claimants by total annual claim band (%):

  | 구간 | 1세대 | 2세대 | 3세대 | 4세대 |
  |---|---|---|---|---|
  | 0–10만원 | 0.8 | 1.5 | 2.4 | 3.7 |
  | 10만–20만원 | 2.0 | 3.3 | 4.4 | 6.0 |
  | 20만–50만원 | 7.4 | 10.7 | 13.3 | 16.3 |
  | 50만–100만원 | 11.2 | 13.4 | 15.6 | 17.7 |
  | 100만–200만원 | 15.6 | 16.7 | 17.3 | 18.9 |
  | 200만–500만원 | 24.2 | 24.4 | 22.9 | 22.2 |
  | 500만–1,000만원 | 15.9 | 14.4 | 12.8 | 9.9 |
  | 1,000만–3,000만원 | 15.6 | 11.1 | 8.5 | 4.5 |
  | 3,000만–5,000만원 | 3.7 | 3.0 | 1.8 | 0.7 |
  | 5,000만–7,000만원 | 1.9 | 1.3 | 0.8 | 0.2 |
  | 7,000만–1억원 | 1.5 | 0.3 | 0.2 | 0.0 |
  | 1억원 이상 | 0.2 | 0.0 | 0.01 | 0.0 |

  Under ₩2,000,000: 36.9% (1세대) → 45.5% → 53.0% → **62.5%** (4세대). Over ₩2,000,000 and
  under ₩100,000,000: 62.8% → 54.4% → 47.0% → 37.5% [R12]. **This is the only published
  claim-severity distribution found, and it is the empirical basis for the model's severity
  assumption.**
- **Premium levels by generation** — a 40대 남자 at a 손해보험사, all covers, monthly:

  | 연도 | 1세대 | 2세대 | 3세대 | 4세대 |
  |---|---|---|---|---|
  | 2021 | — | 3.0만원 | 1.6만원 | 1.5만원 |
  | 2022 | — | 3.5만원 | 1.7만원 | 1.5만원 |
  | 2023 | — | 3.8만원 | 2.0만원 | 1.5만원 |
  | 2024 | — | 4.0만원 | 2.4만원 | 1.5만원 |
  | 2025 | 6.6만원 | 4.9만원 | 3.1만원 | 2.2만원 |

  [R8] for 2021–2024 (1세대 excluded there because 「상품 구조가 표준화되지 않은 세대는
  분석에서 제외」), [R7] for 2025.
- **The 2021 launch comparison, 40세 남자, 손해보험 10개사 평균, as at 2021-06** [R1]:

  | 상품종류 | 현행 보험료 | 4세대 보험료 | 차이 |
  |---|---|---|---|
  | 1세대 (2009-09 이전) | ₩40,749 | ₩11,982 | −₩28,767 (−70.6%) |
  | 2세대 (2009-10~2017-03) | ₩24,738 | ₩11,982 | −₩12,756 (−50.6%) |
  | 3세대 (2017-04~2021-06) | ₩13,326 | ₩11,982 | −₩1,345 (−10.1%) |

  **₩11,982 per month for a 40-year-old male in July 2021 is the model's single best published
  new-business premium anchor for 4세대.** Against the 2025 figure of ₩22,000 for the same cell
  [R7], the realised compound growth over four renewals is 16.4% a year — inside the 25% cap
  but well above the age effect.
- **Industry premium increase rates**: 2022 14.2% → 2023 8.9% → 2024 1.5% → 2025 7.5% [R4];
  2026 an average of 7.8% with 1세대 in the 3% range, 2세대 5%, 3세대 16% and 4세대 in the
  **20%** range, per the two trade associations' joint guidance of 2025-12-23 — **[unverified]:
  this comes from news reports of the associations' announcement, not from a retrieved
  association document**. The 손해보험협회 disclosure [S6] does publish per-carrier 인상률 and
  is the primary source for it, and one row read there — 메리츠화재 상해 2026 21.8%, 2025 23.9%
  — is consistent with a 4세대 increase in the 20%s.
- **The 2024 industry context**, for scale: total insurance-industry net profit ₩14.1조 (a
  record), of which 실손 contributed a ₩1.6조 **loss**; the profit came from investment income
  [R18].

### 13. 청구 간소화 — 실손24 and electronic claiming

Operationally important because it changes claim frequency, not claim cost: a lower friction
cost of claiming raises the reported frequency of small claims, which is exactly the region
where the deductible bites.

- Introduced by amendment of the **보험업법**; 보험개발원 is designated the statutory
  **전송대행기관** and operates the service, app and site 실손24 (`silson24.or.kr`)
  [R13] [R14]. The Act forbids the 전송대행기관 from aggregating the data for any other
  purpose, on pain of criminal penalty [R14]. **The exact 보험업법 article number was not
  established this session — see gaps.**
- **Phase 1, 2024-10-25**: 병원급 의료기관 with 30 or more beds, plus 보건소 — 7,822
  institutions in scope [R14]. At 2024-10-24, 4,223 had joined (병원 733, a 17.3% participation
  rate; 보건소 3,490, 100%), giving a weighted participation of 54.7% and an estimated 56.9% of
  claims by volume; 210 hospitals were live on day one [R13]. By tier: 상급종합 47/47 (100%),
  종합병원 214/331 (64.7%), 일반병원 342/1,402 (24.4%), 요양병원 59/1,396 (4.2%) [R13].
- **Phase 2, 2025-10-25**: 의원 and 약국 — 96,719 institutions, bringing the total in scope to
  **104,541** [R14]. At 2025-10-21, 10,920 (10.4%) were connected: phase-1 institutions 4,290
  (54.8%), phase-2 institutions 6,630 (6.9%); 53,066 institutions (50.8% of the total) were
  using an EMR vendor participating in 실손24 [R14].
- Documents transmitted electronically: 「계산서·영수증, 진료비 세부산정내역서, 처방전」 [R14].
  Compare the paper claim requirement in the wording: 청구서, 사고증명서 (진료비계산서,
  진료비세부내역서, 입원치료확인서, 의사처방전), 신분증 [S1 제7조].
- The claim must be evidenced by a **domestic** provider's document: 「사고증명서는 「의료법」
  제3조(의료기관)에서 규정한 국내의 의료기관에서 발급한 것이어야 합니다」 [S1 제7조제2항], and
  treatment at a foreign provider is excluded from cover [S1 특별약관 제4조].
- **Claim settlement timetable** [S1 제8조]: payment within **3 영업일** of receipt of the
  documents; where investigation is needed the insurer must notify a payment date and the
  가지급 option immediately, and the payment date must fall within **30 영업일** except in six
  listed cases (litigation, dispute mediation, criminal investigation, overseas event,
  policyholder refusal of consent, referral to a third-party medical opinion); interest at the
  rate in <붙임2> runs on late payment; and the insurer must pay **50%** of its own estimate as
  a 가지급보험금 on request.

### 14. Exclusions and the boundary of cover

- **급여 side** [S1 제4조]: intentional self-harm (with the mental-incapacity exception);
  intentional harm by the beneficiary or policyholder; **pregnancy, childbirth (including
  Caesarean) and the puerperium** unless consequent on a covered accident; war and civil
  disorder; hospital stays the insured insisted on against medical advice and outpatient costs
  incurred by disregarding medical instruction. Occupational/hobby exclusions for 전문등반,
  glider piloting, skydiving, scuba, hang-gliding, powerboats, paragliding; motor sport; and
  crew duty aboard ship.
- **급여-specific monetary exclusions** [S1 제4조제3항]: amounts refundable under the
  본인부담금 상한제 or the 의료급여 equivalents; amounts recovered under 자동차보험 or 산재보험
  (net of contributory negligence, with the insured's own residual share still covered); and
  the **응급의료관리료** charged as a 전액본인부담금 where a non-emergency patient uses a
  권역응급의료센터 or an 상급종합병원 emergency department.
- **비급여 side** adds [S1 특별약관 제4조]: dental and 한방 treatment except where performed by
  a 의사; nutritional and vitamin preparations, **except** where used within the licensed
  indication and dosage, where a covered drug is used as 비급여 under a published rule, where
  it passed a separate non-covered-use approval, or where two or more such qualifying drugs are
  combined; hormone therapy, tonics and quasi-drugs; dentures, prostheses, spectacles, contact
  lenses, hearing aids, crutches, arm slings, orthoses (**but implanted artificial organs are
  covered**); non-clinical charges (television, telephone, certificates), tests with no
  clinical indication, and **간병비** (nursing care); foreign providers; and treatment excluded
  from NHI cover for want of demonstrated economy.
- The 영양제·비타민제 rule is worked through four named products in the FAQ [R2], and the
  principle is that **payability follows the drug's licensed indication, not the doctor's
  stated purpose** — e.g. thioctic acid for a common cold is not payable; hepatamine for
  cirrhosis- related anorexia is.
- 5세대 adds to the 특약2 exclusions: 근골격계 이학요법치료, 체외충격파치료, 주사료, 미등재
  신의료기술 (including 첨단재생의료), and any treatment graded **D (권고하지 않음)** by the
  한국보건의료연구원's 의료기술 재평가 [R5] [S2].
- Pregnancy and childbirth move **into** cover on the 급여 side at 5세대 [S2 제3조제10항] [R5],
  reversing the 4세대 exclusion — and the wording's mechanism is to compute the benefit on the
  pre-subsidy medical cost where 모자보건법 or local-government support has reduced it.
- **No general waiting period applies.** Cover begins at 보장개시 (the date the contract is
  concluded and the first premium received, or the date of receipt where the premium came with
  the application) [S1 제24조]. The only deferred item found is the **two-year** wait on
  불임관련 질환 급여 cover introduced at 4세대 [R1].

### 15. Persistency, suspension, duplication and the other policy-count mechanics

- **No surrender value.** S3 states it for a carrier: 「이 상품은 1년만기 순수보장성 상품으로
  해약환급금이 발생하지 않습니다」 [S3]. The 표준약관 nevertheless carries 해지환급금,
  보험계약대출 and 보험료의 자동대출납입 clauses [S1 제26조, 제34조, 제35조], because the
  standard text is shared across products; on a pure one-year indemnity contract the amount is
  the unearned premium and nothing else. **The model therefore has no reserve accumulation and
  no policy-loan mechanics — it is the only `krlib` product of which that is true.**
- **Grace, lapse and reinstatement** follow the standard 손해보험 machinery in S1
  제27조–제29조; the 부활 (reinstatement) clause is 제28조, referenced from 제27조. This
  session did not extract the numeric grace period from S1 — see gaps.
- **개인실손 중지제도.** A policyholder covered by a 단체실손 may suspend the individual policy
  and resume it when the group cover ends; the resumption must be applied for within one month
  [R16]. S3 gives the carrier mechanics in detail: resumption is into the product in force at
  suspension, unless the 보장내용 변경주기 has been passed or the policyholder asks otherwise,
  in which case it is into the current product; the 보장공백기간 must be no more than one month
  per contract and three months cumulatively; and four attributes must match for the resumed
  policy to count as the same — 보장종목, 보험가입금액, 자기부담금, 최대 보장가능 보험나이
  [S3]. 5세대 extends the scheme to 노후·유병력자 실손 and adds a suspension right for insureds
  with documented long-term overseas residence [R5]. S3 gives the carrier version: three months
  or more abroad, prospectively suspended or retrospectively refunded [S3].
- **Duplicate cover pays proportionally, never more than the loss.** 「동일한 위험을 보장하는
  2개 이상의 계약에 중복 가입 하더라도 실제 발생한 손해(비용)를 초과하여 보험금을 지급하지
  않습니다. (중복 가입 시 비례보상)」 [S3], per S1 제37조 (다수보험의 처리) and 제38조
  (연대책임). 5세대 tightens the drafting because carriers were interpreting it inconsistently
  [R5].
- **Conversion between generations** is a supervisory construct, not a policy right in the
  wording. On the 4세대 change: conversion without underwriting except in three cases —
  extending the 보장종목 (상해→상해+질병 or 질병→상해+질병); a psychiatric-treatment history in
  the preceding year on a condition newly brought into cover in 2016; or a re-application after
  a prior withdrawal [R1] [R2]. Withdrawal within **6 months** if no claim has been made, and
  within **3 months** unconditionally [R2]; on withdrawal the premium difference is settled and
  claims arising after conversion are met by the pre-conversion contract [R2]. The 무사고
  period accumulated on the old contract is carried across [R1]. Conversion is **to the same
  insurer's** 4세대 product only; moving to another insurer is an ordinary new-business
  application [R2]. 5세대 repeats the same architecture [R5] [R6], and S3 adds three carrier
  eligibility conditions: the pre-conversion contract must be in force (not lapsed), must have
  had no psychiatric claim event in the preceding year, and — on this direct-channel product —
  must itself be a direct-channel contract [S3].
- **General persistency context**, not 실손-specific: 장기손해보험 13회차 and 25회차 계약유지율
  were 86.3% and 68.3% in 2021, and the 손해보험 industry reported 86.5% and 69.9% for the
  first half of 2024 — **[unverified]**, from news summaries of the 보험연구원 and the industry
  disclosure, neither of which was retrieved. No 실손-specific persistency table was found; the
  best 실손-specific proxy is the 3.3% annual decline in the 1–3세대 in-force block [R7].
- **예금자보호**: covered by the 예금보험공사 to ₩100,000,000 (1억원) per person per insurer
  for 해약환급금 and separately ₩100,000,000 for 사고보험금 [S3].

### 16. 노후실손 and 유병력자실손 — the two adjacent families

Recorded because R7 reports them as a separate 2.4% block and because they show what the
supervisor does when the standard product will not underwrite a life.

- The three families are disclosed as separate product classes by the 손해보험협회's own
  comparison tool, whose 가입유형 selector offers exactly **표준화 / 노후 / 유병력자** [S7].
- **노후실손의료보험**: issue age raised from 75 to **90**, cover age from 100 to **110**, from
  2025-04-01, sold by 9 carriers [R17].
- **유병력자실손의료보험**: issue age raised from 70 to **90**, from 2025-04-01, sold by 13
  carriers [R17].
- Cover-age extension propagates through the existing re-entry mechanism at each **3-year**
  cycle [R17].
- Co-payments, from a search summary of the FSC materials and **[unverified]** because the
  underlying 보도자료 detail page was not opened: 유병력자실손 30% on both 급여 and 비급여,
  inpatient and outpatient; 노후실손 급여 20% / 비급여 30% inpatient. Annual inpatient limit
  ₩50,000,000 per condition and outpatient ₩200,000 per visit for up to 180 visits a year.
- Elderly take-up of ordinary 실손 is 「70대 38.1%, 80세 이상 4.4%」 [R17], which is why these
  families exist.

### 17. Rate regulation, reserving and what constrains the model

- **Where the design rules live.** The 5세대 상품설계기준 sit in the 보험업법 시행령 and the
  보험업감독규정, with the operative detail delegated to the 보험업감독업무시행세칙 — so S1 and
  S2 are the operative texts and the 감독규정 is their enabling instrument [R15]. The design
  constraints the 감독규정 was amended to carry are stated as: 급여 통원 co-payment linked to
  the 건강보험 본인부담률 with a 20% floor; 중증 비급여 30% with a ₩30,000 minimum; 비중증
  비급여 50% with a ₩50,000 minimum [R15]. The same architecture applied to 4세대, whose
  상품구조 개편 was implemented by 「보험업감독규정 및 표준약관 개정('21.6월)」 [R1].
- **The rate-adequacy duty.** 보험업감독규정 제7-63조제2항제6호가목, quoted verbatim by
  보험연구원 [R12]: 「실손의료보험은 다음 각 목의 내용을 준수하여야 한다. 가. 경험통계 등을
  기초로 순보험요율의 적정성을 매년 검증할 것. 다만, 새로운 위험을 보장하는 경우는 5년까지
  적정성을 검증하지 아니할 수 있다.」 The conservative reading of the proviso — that a new
  product need not (and therefore may not) be re-rated for five years — is what produced the
  3세대 and 4세대 loss-ratio patterns in §12, and 보험연구원's principal recommendation is to
  shorten it to three years [R12]. **The article itself was not retrieved from a primary source
  — see R19 and the gaps section.**
- **The 25% annual cap** on the renewal increase, excluding the age effect, is in the wording
  itself [S1 제30조제2항, 특별약관 제6조제2항] and is restated by the supervisor as 「위험구분
  단위별로 실손보험료 인상률을 연 25%내로 제한」 [R6]. Note the phrase 위험구분 단위 — the cap
  binds **per rate cell**, not on the portfolio average, so the published 7.8% industry average
  [unverified] and the 21.8% single-carrier single-cover figure [S6] are not in conflict.
- **Rate-setting principle**: 보험업감독규정 제7-73조 requires rates to rest on 「객관적이고
  합리적인 통계자료를 기초로 대수의 법칙 및 통계신뢰도」, permits the use of external
  statistics or a modified 참조순보험요율 where a company's own experience is insufficient, and
  expressly contemplates rates reflecting 「물가변동, 의료기술발달, 위험변화요인」 [R19]. That
  article was read from the older HWP copy, and its text is materially unchanged in the
  passages read.
- **보험개발원 publishes no 실손 reference rate.** The 장기손해보험 참조순보험요율 disclosure
  covers 일반상해, 교통상해, 질병 사망률, 후유장해, 입원율, 암 발생률, 비용손해, 재물손해 and
  배상책임 — and not 실손의료보험 [R20]. **There is therefore no public Korean morbidity or
  severity basis for this product at all.** Every frequency and severity assumption in
  `Medical_KR_S` must be a `[std]` construction calibrated to the aggregate experience in R7,
  R8 and R12, with the calibration stated.
- **Where the model's own boundary sits.** The published aggregates that a `[std]` basis can be
  fitted to are: the per-policy claim amount by generation [R7]; the per-policy 비급여 claim
  amount by generation and its three-year trend [R8]; the 65% zero-claim proportion and the
  top-decile concentration [R5] [R6]; the claim-size distribution in twelve bands by generation
  [R12]; the 급여/비급여 split of claims [R7]; the provider-mix split and the 비급여 share
  within each provider tier [R7]; and the 3대비급여 item-level claim amounts [R8] [R12].
  Between them these pin down a frequency-severity model at the level of a whole policy year,
  which is the level the product's annual limits and annual deductibles operate at.
- **IFRS 17 and the contract boundary.** A one-year contract with an unrestricted right to
  re-rate at each renewal, a supervisor-set cap of 25% on that re-rating, a five-year re-entry
  into a wording the insurer does not control, and an obligation not to refuse re-entry on
  health grounds — that combination makes the contract boundary genuinely contestable. Nothing
  retrieved this session states an industry or supervisory position on where the 실손 contract
  boundary falls, and this file asserts none. The general IFRS 17 boundary test (whether the
  insurer has a substantive obligation to provide coverage, and whether it can reprice to fully
  reflect the risk of the portfolio) was read only in secondary summary form and is
  **[unverified]** here.
- **10대 비급여, 2023**, from 14 손해보험사 (추정치) [R12] (단위: 억원) — the composition of
  the problem the reforms address:

  | 순위 | 항목 | 금액 |
  |---|---|---|
  | 1 | 물리치료 | 21,291 |
  | 2 | 백내장수술 | 903 |
  | 3 | 비급여 주사제 | 6,334 |
  | 4 | 척추 관련 수술 | 2,830 |
  | 5 | 재판매 가능 치료재료 | 1,129 |
  | 6 | 발달지연 | 1,599 |
  | 7 | 유방질환 (맘모톰 등) | 1,147 |
  | 8 | 하지정맥류 | 1,013 |
  | 9 | 생식기질환 (하이푸시술 등) | 695 |
  | 10 | 비밸브재건술 | 495 |
  | | 합계 | 37,436 |

  Against total 손해보험 실손 claims of ₩11.9조 in 2023, the top ten are **31%** [R12].
- **Public/private decomposition, 2022** [R12]: total treatment cost ₩120.6조; 국민건강보험
  bore ₩79.2조 (65.7%); the individual bore ₩41.3조; 실손의료보험 bore ₩12.9조, i.e. **10.7% of
  the total** and 31.2% of the individual share; and **61.0%** of 실손 claims were 비급여.
- **A unit-cost datum.** For sprain and strain (염좌 및 긴장), 2021–2023, 7,804 observations at
  one large 손해보험사: per patient per day the total treatment cost at a **병원** was ₩285,000
  of which ₩197,000 was 비급여 [R12]. That is a 69% 비급여 share on a low-acuity
  musculoskeletal presentation, and it is the clearest single illustration of why the 3대비급여
  sub-limits exist.

### 18. Ancillary mechanics worth carrying into the spec

- **비급여 진료비용 공개제도.** The insurer must explain, at application, that
  건강보험심사평가원 publishes annual non-covered price surveys and operates a
  price-verification service [S1 특별약관 제7조]. 616 non-covered items were published as at
  2021-06, disclosed each year on the last Wednesday of June [R2]. The dispersion is the point:
  도수치료 prices ranged from ₩5,000 to ₩600,000 across Seoul hospitals [R2]. 5세대 adds the
  비급여 진료 사전설명제도 — providers must state the non-covered items and prices before
  treating [S2].
- **비급여 보험금 조회시스템.** Each insurer operates a system letting the policyholder see
  their own accumulated non-covered claims, so that they can manage their 할인·할증 band —
  **[unverified]**, from a search summary of a 금융감독원 release that was not retrieved.
- **The FAQ's behavioural worked example** [R2], which is the clearest statement of what the
  차등제 is meant to do: a 45-year-old male paying ₩5,000 급여 + ₩8,000 비급여 = ₩13,000 a
  month takes about 20 sessions of 도수치료 at ₩500,000 a session, claims ₩10,000,000 and
  receives ₩7,000,000, bearing ₩3,000,000 himself. His rider premium quadruples to about
  ₩32,000 and his total to about ₩40,000. He then shops on the 심평원 price disclosure, cuts
  his claims to ₩700,000 with ₩300,000 borne, and his rider premium resets to about ₩9,000
  (including the age increment) and his total to about ₩15,000 — a saving of ₩300,000 in
  premium and ₩2,700,000 in out-of-pocket cost in a year.
- **Cooling-off and other consumer clauses** are in S1 제17조 (청약의 철회), 제18조 (약관 교부
  및 설명 의무), 제19조 (계약의 무효), 제20조 (계약내용의 변경) and 제39조 (분쟁의 조정); the
  numeric cooling-off window was not extracted this session — see gaps.
- **분쟁 volume.** 신경성형술 disputes alone were about **20%** of all 실손 disputes in 2025
  [R7]. The supervisor's own consumer warning describes the mechanism: where the insurer
  refuses to accept that admission was medically necessary it pays only the outpatient benefit
  (₩200,000–₩300,000) against an inpatient limit of ₩50,000,000, and the consumer bears the
  rest [R7]. **The inpatient/outpatient classification of a claim is worth two orders of
  magnitude in the benefit, and it is contested.**

---

## Variation across carriers

The honest answer for this product is that **carrier variation in the benefit is close to zero,
and all the variation is in price, in the selectable 보험가입금액, and in the discounts.** That
is the opposite of the position in `jplib`'s 医療保険 or `uklib`'s critical illness, and it is
a direct consequence of the 표준약관 regime. The table below records what actually differs.

| Feature | Set by | Varies by carrier? | Observed range |
|---|---|---|---|
| 보장종목 structure (급여 주계약 / 비급여 특약) | 표준약관 [S1] | **No** | identical at every carrier |
| 자기부담률 (급여 20%, 비급여 30%) | 표준약관 [S1] | **No** | identical |
| 통원 공제금액 (₩10,000 / ₩20,000 / ₩30,000) | 표준약관 [S1] | **No** | identical |
| 3대비급여 sub-limits (350 / 250 / 300만원; 50 / 50 / ∞회) | 표준약관 [S1] | **No** | identical |
| 100-visit annual 비급여 통원 cap | 표준약관 [S1] | **No** | identical |
| 급여 입원 연간 자기부담 200만원 | 표준약관 [S1] | **No** | identical; already present in 2세대 [S4] |
| 요율 상대도 bands (100/200/300/400%) | 표준약관 [S1] | **No** | identical |
| 요율 상대도 **discount** factor (band 1) | solved for revenue neutrality [S1] | **Yes** | 「5% 내외」 [R1]; −5% 잠정 [R3]; written as 「α%」 in a carrier document [S3]; 95% relativity used in the wording's own illustration [S1] |
| 25% annual renewal cap | 표준약관 [S1] / 감독규정 [R6] | **No** | identical |
| 연간 보험가입금액 | 표준약관 sets a **ceiling**; carrier offers a menu | **Yes** | 「5천만원 이내에서 회사가 정한 금액 중 계약자가 선택한 금액」 [S1]; one carrier's 5세대 menu is ₩50,000,000 / ₩30,000,000 / ₩10,000,000 with per-visit caps ₩200,000 / ₩150,000 / ₩100,000, and ₩10,000,000 / ₩6,000,000 / ₩2,000,000 on 특약2 [S3] |
| 통원 회당 한도 | ditto | **Yes**, with the same ceiling | ₩200,000 ceiling [S1]; ₩100,000–₩200,000 observed [S3] |
| 가입나이 | carrier | **Yes** | 0–49 on one direct-channel 2세대 product [S4]; no 4세대 or 5세대 range retrieved — see gaps |
| 재가입 나이 / 최대 보장 연령 | carrier, within the 표준약관 framework | **Yes** | 재가입 15–99세, cover to 보험나이 100세 (2세대) [S4]; 재가입 최고 99세, cover to 보험나이 100세 (5세대) [S3] |
| 보장내용 변경주기 | supervisory | **No**, within a generation | 15년 (2세대) [S4]; 5년 (4세대) [R1]; 「최대 5년」 (5세대) [S3] |
| 무사고 할인 | supervisory design, carrier scope | **Slight** | 10% of the whole premium after two claim-free years, 4대 중증질환 claims excluded [R1]; one carrier's 5세대 wording excludes 급여 본인부담금 and 특약1 claims from the test and excludes contracts without 특약2 altogether [S3] |
| 의료급여 수급권자 할인 | carrier | **Yes** | 5% of 영업보험료 at one carrier [S3]; not found elsewhere |
| 해약환급금 | product design | **No** on the standalone 실손 | none — 1년만기 순수보장성 [S3]. The 통합형 products to which 실손 covers are attached as riders do offer 해지환급금 미지급형 / 저지급형 on the **other** covers [S5] |
| Premium level | carrier | **Yes, materially** | the 손해보험협회 publishes per-carrier 인상률 and 손해율 precisely because of this [S6]; one carrier's 상해 담보 rose 23.9% in 2025 and 21.8% in 2026 against an industry average reported at 7.8% [unverified] |
| 갱신 안내 lead time | carrier | **Yes** | 15 days before expiry at one carrier [S5]; the 표준약관 requires 2회 이상 notice before the 변경주기 ends but sets no lead time for the annual renewal [S1 제23조] |
| 자동 연장 limbo cap on re-entry | carrier | **Yes** | the 표준약관 leaves it open-ended [S1 제23조제7항]; one carrier caps it at 「보험기간이 종료된 날로부터 1년」 [S3] |

**What does not vary at all.** The benefit definition, the co-payment percentages, the
deductibles, the sub-limits, the visit counts, the 10-visit re-assessment rule, the exclusions,
the 180-day run-off, the 재가입 no-decline guarantee, the 보험나이 convention, the 25% renewal
cap, and the five 요율 상대도 bands. A `krlib` product spec for 실손의료보험 that names a
representative carrier is making a category error: **the representative contract is the
표준약관**, and the only carrier-specific choices the model must make are the 보험가입금액
(₩50,000,000 per 보장종목 is the maximum and the market standard), the 가입나이 envelope, and
the band-1 discount factor.

**Representative design for the reference implementation.** A 4세대 contract: 기본형
실손의료보험 (급여 실손의료비) with both 상해급여형 and 질병급여형 at the ₩50,000,000 annual
limit and a ₩200,000 per-visit cap, plus 실손의료보험 특별약관 (비급여 실손의료비) with
상해비급여형, 질병비급여형 and 3대비급여형 at the same ₩50,000,000 limit, the 100-visit cap and
the three sub-limits; 급여 자기부담 20% with the ₩2,000,000 annual inpatient cap; 비급여
자기부담 30%; outpatient deductibles ₩10,000 / ₩20,000 급여 and ₩30,000 비급여, each a maximum
against the percentage; one-year term with automatic renewal at attained 보험나이 and a 25% cap
on the base-rate increase; the five-band 요율 상대도 on the rider net premium with a −5% band-1
factor; the 10% two-year 무사고 discount on the whole premium; five-year re-entry with no
health underwriting; and no surrender value.

---

## Fetch failures and gaps

Recorded in full. Every dependent fact above is tagged `[unverified]` where it rests on one of
these.

- **보험업감독규정 제7-63조제2항 (the current text) — NOT RETRIEVED.** Four routes tried:
  - `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` — HTTP 200, returned only
    the masthead and the amendment metadata (시행 2023-03-02, 금융위원회고시 제2023-10호); the
    article body is JavaScript-rendered.
  - `https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000235980` — same, metadata only
    (시행 2024-01-31, 제2024-9호).
  - `https://www.ulex.co.kr/법률/2100000235980-21843-보험업감독` — returned Chapters 1–4 only;
    제7-63조 is in Chapter 7 and was not in the returned range.
  - `https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=24827&fileTy=ATTACH&fileNo=10`
    (880 KB HWP) and `https://www.easylaw.go.kr/CSP/FlDownload.laf?flSeq=317766` (752 KB HWP) —
    **both downloaded and decoded successfully**, but both are the same pre-2013 vintage whose
    제7-63조 has three 호 and no 제2항. The 실손 design rules are not in either.

  Consequence: the 실손 rate-adequacy rule quoted at §17 is attributed to **R12**, which quotes
  it verbatim, not to the regulation. The 실손-specific design constraints in 제7-63조제2항
  (the co-payment floors, the limit ceilings, the re-entry cycle) are therefore known only
  through the press releases and the 표준약관 that implement them, which is sufficient for the
  model but is not the primary instrument.
- **보험업법 article number for the 청구 전산화 / 전송대행기관 duty — NOT ESTABLISHED.** R13
  and R14 both refer to 「보험업법」 without an article number, and the statute itself was not
  fetched. The commonly cited 제102조의6 appears only in a search query formulation and is
  **not asserted anywhere above**.
- **국민건강보험공단's own posting of the 2024 보장률 보도자료 — NOT LOCATED.** The document
  was read in full through 보험연구원's 「주간 트렌드」 reproduction
  (`https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf`). The reproduction carries
  the original 배포일 (2025-12-30), the 담당 부서 block (비급여관리실 보장성평가센터) and the
  full table set, so the content is treated as retrieved; the canonical 공단 URL is not
  recorded because it was not found.
- **금융감독원's own posting of the 2024 실손 사업실적 보도자료 — INDEXED BUT NOT DOWNLOADED.**
  The board entry was located (`nttId=193952`, 2025-05-12) but its attachment was not fetched;
  the document was read through the 보험연구원 reproduction
  (`https://kiri.or.kr/PDF/weeklytrend/20250526/trend20250526_4.pdf`), which is verbatim and
  reconciles with R7's prior-year columns.
- **금융감독원 보도자료 2024-01-19 on the 차등제 — NOT RETRIEVED.** The band-share distribution
  (72.9 / 25.3 / 0.8 / 0.7 / 0.3) is attributed to it by 보험연구원 [R12] and is recorded here
  on that basis only. It conflicts with the 금융위원회 figures in R3 (62.1 / 36.6 / 1.3) and
  this file does not reconcile them.
- **2026 industry premium increase (7.8% average; 1세대 3%대, 2세대 5%대, 3세대 16%대, 4세대
  20%대) — [unverified], NEWS ONLY.** The figures come from press reports of a joint
  생명보험협회·손해보험협회 announcement of 2025-12-23. Neither association's own document was
  located. The 손해보험협회 disclosure [S6] is the primary source for per-carrier rates and one
  row was read from it, but the full grid could not be paged.
- **손해보험협회 실손 보험료 비교공시 — FORM-GATED.**
  `https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthDisclosure.do` returned the insurer
  list, the input taxonomy (표준화 / 노후 / 유병력자; 성별; 보험나이) and the coverage basis,
  but the grid is populated by a POST and returned 「조회된 내용이 없습니다」.
  `https://kpub.knia.or.kr/productDisc/lostHealth/lostHealthCompare.do` returned **HTTP 404**.
  `https://e-insmarket.or.kr/mins/minsInsList.knia?prdtSmlClsCd=G003` (온라인 보험슈퍼마켓)
  likewise returned only the search form. **Consequence: no age × sex premium scale for 4세대
  or 5세대 was obtained.** The model's premium scale is therefore a `[std]` construction
  anchored on the four published point values — ₩11,982 (40세 남, 4세대, 2021-06) [R1]; ₩22,000
  (40대 남, 4세대, 2025) [R7]; ₩178,489 and ₩126,773 (60대 여, 1세대 and 2세대, 2026) [R5];
  ₩16,000 (40대 남, 5세대, 2026) [R5] — and on the 4%-per-year age loading implied by the
  표준약관's own renewal illustration [S1].
- **4세대 and 5세대 가입나이 (issue-age range) — NOT RETRIEVED.** S4 gives 0–49 for one
  direct-channel 2세대 product. The 4세대 표준약관 [S1] sets no issue age (it is a 사업방법서
  matter), and the 5세대 carrier booklet [S3] states the **재가입** age (to 99) and the maximum
  cover age (보험나이 100) but not the issue-age range. No 4세대 or 5세대 상품요약서 was
  located — see the next item. The model's issue-age envelope is `[std]`.
- **No 4세대 carrier 약관 or 상품요약서 was located.** Attempted:
  `https://www.idbins.com/pcweb/bizxpress/pdc/hc/__etc/실손의료비보험2107.pdf` — **HTTP 404**
  (constructed by analogy with the 2101 file that did work, and recorded here as an attempt,
  not as a citation). Searches for a 2021–2025-vintage 실손 booklet returned only aggregator
  pages. The retrieved carrier documents are therefore 2세대 [S4], 3세대 [S5] and 5세대 [S3],
  and the 4세대 contract is documented **entirely from the 표준약관 [S1] and the supervisory
  releases [R1] [R2] [R5]**. Given that the 표준약관 *is* the contract, this is a smaller gap
  than it looks, but it means no 4세대 보험가입금액 menu, no 4세대 issue-age range and no 4세대
  사업비 disclosure was obtained.
- **사업비 / 부가보험료율 — NOT OBTAINED for this product.** No 상품요약서 with an expense
  disclosure was retrieved. The only expense datum in this file is the aggregate: 손해조사비
  plus 사업비 of about ₩2.9조 on ₩18.0조 of 2025 premium, i.e. **16.1%**, and the supervisor's
  stated break-even loss ratio of about 85% [R7], which implies the same order. The model's
  expense basis is `[std]` on that aggregate.
- **Grace period, 부활 window and 청약철회 window — NOT EXTRACTED.** S1 제27조 (납입최고와
  계약의 해지), 제28조 (부활) and 제17조 (청약의 철회) were located in the extracted text by
  heading but their numeric parameters were not read out in this session. Nothing above depends
  on them.
- **본인일부부담금 산정특례 co-payment percentages (5% / 10%) — [unverified].** Only a search
  summary of the 국민건강보험공단 explanation page was seen; neither
  `https://www.nhis.or.kr/nhis/policy/wbhada15400m01.do` nor the 보건복지부 고시 itself was
  fetched. The **existence, statutory basis and enumerated scope** of 산정특례 are verified
  from S2 특별약관1 제2조, which cites 제4조부터 제5조의3까지 and lists the categories; the
  percentages are not.
- **2025년 건강보험 본인부담상한제 소득구간별 상한액 (보건복지부 사전정보공표) — attachment not
  opened.** `https://www.mohw.go.kr/board.es?mid=a10107010000&bid=0047&act=view&list_no=1486195`
  returned the posting metadata (2025-06-05, 필수의료총괄과) but the table is in an HWPX/PDF
  attachment that was not downloaded. The threshold table at §10 comes from the
  국민건강보험공단 page [R10] instead, which was retrieved and which covers 2023–2026.
- **보험개발원 실손 위험률 — CONFIRMED ABSENT, not merely unfetched.** [R20] lists the
  published 장기손해보험 참조순보험요율 categories and 실손의료보험 is not among them. This is
  a positive finding, not a gap: there is no public reference morbidity basis for this product,
  and the model must say so.
- **경험생명표 (제10회) — not consulted in this file.** The mortality decrement for
  `Medical_KR_S` is a `krlib`-wide matter handled in `_research/regulatory-actuarial.md`;
  nothing here depends on it. Note only that on a one-year indemnity contract death is a
  termination that *releases* the liability, so the direction of prudence in the mortality
  basis is opposite to that of the protection products.
- **IFRS 17 contract boundary for 실손 — NO PRIMARY SOURCE.** Searches returned 보험연구원
  general IFRS 17 material and news coverage of 계약 재매입; no supervisory or professional
  statement on where the boundary falls for a Korean one-year-renewable, five-year-re-entry
  indemnity medical contract was located. §17 states the tension and asserts no answer.
- **실손 persistency (13회차 / 25회차 유지율) specific to this product — NOT FOUND.** Only
  industry-wide 장기손해보험 figures appeared, and only in news summaries [unverified]. The
  1–3세대 in-force decay of 3.3% a year in 2025 and 4.4% in 2024 [R7] is the best retrieved
  proxy and is what the model's `lapse_rate` should be calibrated against, with the caveat that
  it blends lapse, death and conversion.
- **비급여 보험금 조회시스템 — [unverified].** Its existence is asserted only in a search
  summary of a 금융감독원 release that was not retrieved.
- **노후실손 / 유병력자실손 parameter detail — [unverified].** R17 was read in summary form and
  gives ages and carrier counts; the co-payment and limit figures at §16 come from a search
  summary of FSC materials that were not opened.
- **HWP extraction caveat, applying to S1, S2 and R6.** All three were decoded from the HWP5
  binary format by inflating the `BodyText` streams and walking the record tree for
  `HWPTAG_PARA_TEXT` (tag 67), decoding UTF-16LE and skipping the 8-word inline control
  records. This recovers **paragraph text and table cell text**, in document order, but **not
  the table geometry**: a table arrives as a flat sequence of cell strings, and the mapping of
  cells to rows and columns had to be reconstructed by reading the surrounding wording. Every
  table reproduced above from S1, S2 or R6 was cross-checked against a second source stating
  the same figures in prose or in a PDF table (usually R1, R5 or R7) before being written down;
  where no cross-check existed the figure is quoted as a sentence rather than as a table.
  Inline formulas (e.g. the 건강보험 본인부담률 fraction in S2) render as a fraction laid out
  over three paragraphs and were read that way. Drawing objects — the 보상기간 timeline
  diagrams, the 할인·할증 flow figures — did not extract at all.
- **PDF extraction caveat, applying to R1, R2, R5, R7, R8, R9, R12 and S3–S5.** These extracted
  cleanly as text, including numeric tables. The charts in R7, R9 and R12 are raster images
  whose **data labels** extracted as loose number sequences with no axis; those series are
  quoted above only where the surrounding prose fixes the label-to-value mapping unambiguously,
  and the R12 loss-ratio-by-generation chart and the R9 spending trend chart are **not** quoted
  as tables for that reason.
