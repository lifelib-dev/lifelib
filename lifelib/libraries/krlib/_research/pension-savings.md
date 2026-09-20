# 연금저축보험 (tax-qualified pension savings) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for the Korean tax-qualified individual pension contract, 연금저축보험
(*yeongeum jeochuk boheom*), and for the deferred-annuity accumulation chassis that
`Pension_KR_S` builds on. The product is one leg of a three-legged statutory wrapper —
연금저축신탁 (bank), 연금저축펀드 (asset manager) and 연금저축보험 (insurer) — all three
defined by the same article of the income tax code and distinguished only by who writes them
and what they credit. What makes the insurance leg an actuarial object rather than a savings
account is that it, alone among the three, can pay a **life annuity**: the accumulation runs on
a monthly-reset declared rate (공시이율) with a guaranteed floor (최저보증이율), and at
annuitisation the fund is divided by an annuity factor built from the insurer's own annuitant
mortality (연금사망률) and the then-current declared rate.

Korea's individual-pension tax design is unusual in this repository in two respects. First, the
relief on the way in is a **tax credit (세액공제)**, not a deduction: a flat 13.2% or 16.5% of
contributions up to a cap, so the after-tax value of a contribution does not rise with the
marginal rate — it *falls*, because the higher-income band gets the lower credit rate. Second,
the tax on the way out is a **withholding tax banded by the age at which the annuity is taken**
(5.5% / 4.4% / 3.3% including local income tax), with a further reduction to a flat 3.3% for a
contract that is a 종신계약 — a life annuity that cannot be surrendered. That is a tax code
that pays the policyholder to annuitise late and for life, and it is the single most important
behavioural driver in the product. Against it stands a punitive 16.5% 기타소득세 on any
withdrawal that misses the statutory 연금수령 conditions, which is what makes the lapse
assumption on this product different from a plain savings contract.

This file is the **provenance layer** behind `products/pension_savings/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Every fact below carries the tag of the
document it came from: `[S#]` for a primary product document (약관, 상품요약서, 상품안내장,
공시자료) and `[R#]` for a regulatory, statutory or statistical reference, both numbered
against the lists in this file. `[derived]` marks a figure I computed from published figures
rather than read; `[unverified]` marks a claim from general knowledge or a search snippet that
could not be confirmed against a retrieved document. **The source numbering in this file is
never renumbered** — the four product documents cite against it, and a renumber would silently
redirect every citation. New sources are appended, never inserted.

Access date for every fetch in this file: **2026-09-03**.

---

## Primary sources

### S1 — ABL생명, 「무배당 우리WON인터넷연금저축보험 상품요약서」
- Publisher: 에이비엘생명보험주식회사 (ABL Life)
- Document: 상품요약서, 판매 vintage 260101, 9 pp. PDF
- Doc type: 상품요약서 (statutory product summary — the filed-document digest a Korean insurer
  must publish in its 상품공시실)
- URL: https://abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2026/07/09/NP_%EC%9A%B0%EB%A6%ACWON%EC%9D%B8%ED%84%B0%EB%84%B7%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C(260101).pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 9 pp., text extracted with PyMuPDF and read in full; the
  markdown-converting fetcher returned only the binary stream, so the file was parsed locally)
- What was read, and what it is good for: the complete parameter set of a currently sold
  bancassurance-channel 연금저축보험 — issue-age and premium-term matrix, annuity forms, the
  연금사망률 the annuity factor uses (three ages, both sexes), the 보장부분 적용이율, the
  current 공시이율 with its month, the 최저보증이율 ladder, the full 계약체결비용 /
  계약관리비용 schedule with won amounts, the 해약공제액 table (all zeros on this product), the
  모집수수료율 table (all zeros — a direct channel), and a 해약환급금 예시 running from 3
  months to 20 years on both the 최저보증이율 and the 공시이율 bases. It also carries the
  clearest carrier-side statement of the tax rules, including the 연금수령한도 formula
  reproduced as an equation. **This is the single most quantitatively complete document in this
  file.**

### S2 — ABL생명, 「연금저축나이스플랜연금보험2601」 상품안내장
- Publisher: 에이비엘생명보험주식회사
- Document: 상품안내장 (product leaflet), 제작 2026년 1월 1일, 준법감시인 심의필 제2025-PA474호
  (유효기간 2025.12.29 ~ 2026.12.28), 8 pp. PDF
- Doc type: 보험안내자료 (compliance-approved sales literature)
- URL: https://www.abllife.co.kr/cms/prdt/anutSav/__icsFiles/afieldfile/2026/01/06/%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%82%98%EC%9D%B4%EC%8A%A4%ED%94%8C%EB%9E%9C%EC%97%B0%EA%B8%882601_20260101.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 8 pp., parsed locally with PyMuPDF and read in full)
- What was read, and what it is good for: a **participating** (배당) 연금저축보험 sold through
  the tied channel, with three complete 연금액 예시표 on one model point (남자 40세, 기본보험료
  월 50만원, 20년납, 연금개시나이 65세) on three interest bases — 최저보증이율,
  min(평균공시이율 2.50%, 공시이율 2.15%), and 공시이율 2.15% — each giving the fund at
  annuitisation and the monthly annuity under 종신연금형 10년보증, 종신연금형 20년보증 and
  확정연금형 10/15/20년. Together with the matching 해약환급금 예시표 this pins down both the
  accumulation and the annuity factor on a single consistent basis, and is the source of the
  derived annuity factors in §21. Also gives the 2026 평균공시이율 (2.50%) with its regulatory
  citation, the 100.1%-of-premiums floor at annuitisation, the 예금자보호 limit after the 2025
  increase, and the issue-age / premium-band matrix.

### S3 — ABL생명, 「무배당 ABL인터넷연금저축보험 보험약관」
- Publisher: 에이비엘생명보험주식회사
- Document: 보험약관 (policy conditions) with 부록, 127 pp. PDF, posted 2021-09-25
- Doc type: 약관 (verbatim contract wording)
- URL: https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2021/09/24/20210925_NP_ABL%EC%9D%B8%ED%84%B0%EB%84%B7%EC%97%B0%EA%B8%88%EC%A0%80%EC%B6%95%EB%B3%B4%ED%97%98.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 127 pp., parsed locally; the tax article, the annuity
  benefit table and the 부록 statute reproduction were read in full)
- What was read, and what it is good for: 제21조[계약의 세제혜택 등] verbatim — the 세액공제,
  the 기타소득세 16.5%, the 연금수령 three-limb test, the 연금수령한도 equation, the six
  부득이한 사유 with the ₩2,000,000 / medical / ₩1,500,000-per-month-of-leave caps, and the
  spouse-succession rule. Critically the **부록 reproduces 소득세법 시행령 제40조의2
  제2항–제5항 verbatim**, including the 연금수령한도 formula as a typeset fraction, which is
  the cleanest retrieved copy of that provision. It also carries the three 최소 연금지급기간
  tables (contract before 50 / after 50 / after 55 with 이연퇴직소득) that translate the
  연금수령한도 into a minimum payout term.

### S4 — 한화생명, 「한화생명 e연금저축보험 무배당 약관」
- Publisher: 한화생명보험주식회사 (Hanwha Life)
- Document: 보험약관 가이드북 + 주계약 약관 + 특약 + 부록, 문서번호 1772-029/032, 2024-04-01
  vintage, 122 pp. PDF
- Doc type: 약관 bound with the pre-contract disclosure gaidebuk
- URL: https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e연금저축보험%20무배당_1772-029_032_약관_20240401.pdf
  (the live link carries a `docUrl=` query string resolving to
  `dynamic/direct/product/cms_99rYZ05ZhDpfQ5BY_1715162660147.pdf`)
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 122 pp., parsed locally and the rate, annuity, tax and
  surrender sections read)
- What was read, and what it is good for: a direct-channel carrier with a **different
  최저보증이율 ladder** from every other retrieved document (three bands, not two, and stepping
  at 3 and 5 years rather than 5 and 10), the 제6조 공시이율의 적용 및 공시 article verbatim
  including the 공시기준이율 construction, the 별표1 benefit table giving 종신연금형 with
  10년/20년/100세 보증 and 확정기간연금형 10/15/20년, the **100.1%-of-premiums minimum
  guarantee at annuitisation** with its two disapplication triggers, and the annuity-mortality
  ratchet clause (note 11). Also a worked 민원 사례 pair that states the consumer-detriment
  mechanics plainly.

### S5 — 삼성생명, 「삼성생명 연금저축골드연금보험 B1.4(무배당)」 상품안내장
- Publisher: 삼성생명보험주식회사 (Samsung Life), sold through KEB하나은행 (금융기관보험대리점
  2003091001); 준법감시필 BA 제16-28호 (16-03-11)
- Document: 상품안내장, 판매개시일 2016-04-01, 4 pp. PDF
- Doc type: 보험안내자료 (bancassurance leaflet)
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L03014230_r.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 4 pp., parsed locally and read in full)
- What was read, and what it is good for: an **older-vintage** contract (2016), retained
  deliberately because it shows the tax parameters *before* the 2023 and 2026 reforms
  (₩4,000,000 credit cap, ₩12,000,000 separate-taxation threshold, 종신연금형 4.4%) and because
  it carries the fullest published **연금지급 예시**: 종신연금형 at four guarantee lengths
  (10회 / 20회 / 30회 / 100세) and 확정기간연금형 at five terms (5/10/15/20/30년), each on
  three interest bases, plus a 해약환급금 예시 with a 세후지급 예상액 column that shows the
  기타소득세 bite explicitly. It also publishes a **13-month history of the 공시이율** (3.55%
  down to 2.98%), a 평균공시이율 of 3.5% for 2016, and a 최저보증이율 of 1.5%/1.0% — the top of
  the observed guarantee range.

### S6 — NH농협생명, 「e-NH연금저축보험(무배당)_2404 약관」
- Publisher: NH농협생명보험주식회사 (NH NongHyup Life), distributed via KEB하나은행; 판매월
  2026.01
- Document: 약관 (주계약 + 특약 + 별표), 88 pp. PDF
- Doc type: 약관
- URL: https://image.kebhana.com/cont/download/insdocument/provide/L42014209M_agree.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 88 pp., parsed locally; the benefit table, the age
  article, the contract-variation article and the rate notes were read)
- What was read, and what it is good for: the widest **annuity-form menu** of any retrieved
  contract — 종신연금형 with 10 / 20 / 30년 보증, 확정기간연금형 at 10/15/20/25/30년, and a
  **자유설계연금형** that splits the fund between the two in 10% units summing to 100%. It is
  also the only retrieved contract that states the **보험나이 / 만나이 rule explicitly**
  (제20조): 보험나이 governs everywhere except the statutory 만 55세 test, which uses 만나이 —
  the single cleanest citation in the library for that distinction. Its annuity mortality is
  named "무배당 경험 개인연금사망률", and the same ratchet clause appears as note 10.

### S7 — 우체국보험(체신관서), 「우체국연금저축보험 2504 상품요약서」
- Publisher: 우체국예금·보험 (Korea Post Insurance; supervised by 과학기술정보통신부, not by
  the FSC — a statutory carve-out from 보험업법)
- Document: 상품요약서, 2504 vintage, 14 pp. PDF
- Doc type: 상품요약서
- URL: https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/yoyak_P210061_202504.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 14 pp.; the default extraction dropped the numerals
  because of the layout, so pages were re-extracted with `sort=True`, after which the whole
  document read cleanly)
- What was read, and what it is good for: the **only retrieved 연금저축보험 with a non-zero
  해지공제액** — ₩104,000 at year 1 falling to zero at year 5, published both in won and as a
  percentage of premiums paid (8.7% → 0%). It also gives a full 개인연금사망률 table at ages
  40/60/80 for both sexes on a 40-year-old issue, a 예정이율 of 2.5%, a 최저보증이율 of
  1.0%/0.5%, a five-year 계약자배당 history with the 기준율, a 해약환급금 예시 at two premium
  sizes, and a complete fee schedule split into 판매보수 / 유지보수 / 계약관리비용 /
  연금수령기간 관리비용 / 추가납입 비용.

### S8 — 현대해상, 「연금저축손해보험 현대해상다이렉트연금보험(Hi2504)」
- Publisher: 현대해상화재보험주식회사 (Hyundai Marine & Fire) — a **non-life** insurer
- Document: 약관 이용 가이드북 + 시각화된 약관 요약서 + 상품안내 + 주계약 약관, file CM106N
  dated 2025-09-01, 97 pp. PDF
- Doc type: 약관 bound with 상품안내
- URL: https://direct.hi.co.kr/dhNAS/terms/CM106N_20250901.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 97 pp., parsed locally and the product-envelope, rate,
  annuity and tax sections read)
- What was read, and what it is good for: the **non-life form of the same statutory wrapper**,
  which is the cleanest demonstration of what a 손해보험사 may and may not write. Its only
  연금지급형태 is 정액형 over a 연금지급기간 of **5년 ~ 25년** — there is no 종신연금형 at all,
  and therefore no annuity mortality anywhere in the contract. It names its crediting rate
  "연금저축 공시이율Ⅴ", gives a 1.25% / 1.0% / **0.3%** guarantee ladder (the lowest
  long-duration floor observed), defines 해약공제액 as 미상각 신계약비, and cites
  보험업감독규정 제1-2조's 저축성보험 definition as the reason the annuity start date is
  deferred when the fund would otherwise not exceed premiums paid.

### S9 — 교보생명, 「연금저축 교보First연금보험 약관」
- Publisher: 교보생명보험주식회사 (Kyobo Life)
- Document: 약관 (주계약 + 별표1 + 별표2), undated vintage, consulted through a third-party
  contract mirror
- Doc type: 약관
- URL: https://lawinsider.com/ko/contracts/aXubiP59oQE
- Accessed: 2026-09-03
- Retrieved: **in part** (fetched through a document-mirror site, not the carrier's own 공시실;
  the articles quoted below were returned, but the document's edition date and filing reference
  were not, so the vintage is unknown)
- What was read, and what it is good for: a **much higher guarantee ladder** than any other
  retrieved contract — 연복리 2.0% under 10 years and 1.5% at 10 years and over — which places
  it in an older product generation and brackets the top of the observed range. Also 종신연금형
  at 10/20/30년/100세 보증, 확정연금형 at 5/10/15/20/25/30년, 연금지급개시나이 만55세~80세, and
  the same annuity-mortality ratchet clause (별표2 주9).

### S10 — AIA생명, 「(무)AIA 여유+ 변액연금보험 상품요약서」
- Publisher: AIA생명보험주식회사 (AIA Life Korea)
- Document: 상품요약서, Form 107, 2026-01-01 vintage, 18 pp. PDF
- Doc type: 상품요약서
- URL: https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/saving/summary/AIA_kr_Form107_20260101.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 18 pp., parsed locally with `sort=True` and the
  annuitisation sections read)
- **Scope caution:** this is a **변액연금보험**, not a 연금저축보험. It is cited here only for
  the annuitisation machinery — the annuity-form menu and the mortality-vintage clause — which
  is shared across the Korean annuity book. **No accumulation, expense, tax or rate fact in
  this file is sourced to S10.** It belongs primarily to `_research/variable- annuity.md`.
- What it is good for: the fullest **annuity-form taxonomy** retrieved — 보증기간부 종신연금형
  (10년 / 20년 / 100세 보증, 정액형 and 5%/10% 체증형 over a 10-year escalation window),
  보증금액부 종신연금형, 확정연금형, 상속연금형 and 실적연금형 — plus the definition that
  "100세 보증" means "101세 계약해당일의 전일까지", i.e. a (101 − 연금개시나이)-year guarantee.
  Its mortality basis is named "예정 개인연금 생존·사망률" and carries the same ratchet clause.

### S11 — KDB생명 다이렉트, 「e원금보장 KDB하이브리드연금저축보험(무)」 상품 페이지
- Publisher: KDB생명보험주식회사
- Document: consumer product page, rates stated as at 2024년 10월
- Doc type: product page
- URL: http://direct.kdblife.co.kr/edirect/product/hybrsavingDetail.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, converted and read)
- What it is good for: a **hybrid rate design** absent from every other retrieved carrier — a
  fixed 연복리 3.5% 확정이율 for the first five contract years, then the ordinary
  신공시이율(무배당 연금저축Ⅳ) thereafter, with a 1.0%/0.5% floor. Also 가입나이 만19세 ~
  (연금개시나이 − 납입기간), 연금개시나이 만55~80세, 종신연금형 10/20/30년/100세 보증 as the
  default form, 확정연금형 10/15/20/25/30년, and a plain statement of the 16.5% / 13.2% credit
  rates with the resulting maximum refunds (₩990,000 and ₩792,000).

### S12 — DB생명, 「금리연동이율공시」
- Publisher: DB생명보험주식회사
- Document: monthly declared-rate disclosure, table dated **2026.09.01**
- Doc type: 공시이율 disclosure
- URL: https://www.idblife.com/notice/product/tmo_int
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, table read)
- What it is good for: the **current market level of the 연금저축 공시이율**, two days before
  the access date, with the prior month beside it — the only retrieved source that dates a
  declared rate to the current month.

### S13 — 하나생명, 「적용이율 공시 — 최저보증이율 및 경과기간별 중도해지율」
- Publisher: 하나생명보험주식회사 (Hana Life)
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab5.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, table read)
- What it is good for: a **by-vintage** 최저보증이율 table across one carrier's whole 연금저축
  shelf, keyed to each product's 판매개시일 — which is what shows that the guarantee ladder is
  a function of sale date, not of carrier.

### S14 — 하나생명, 「적용이율 공시 — 표준이율 및 평균공시이율」
- Publisher: 하나생명보험주식회사
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, both tables read)
- What it is good for: the **평균공시이율 time series 2016–2026** with the current year's
  value, and the definition of 평균공시이율 as the regulator-defined average of all insurers'
  declared rates. This is a supervisory parameter, published by carriers, that enters
  illustration rules directly.

### S15 — 교보라이프플래닛, 「적용이율공시 최저보증이율(연금저축상품)」
- Publisher: 교보라이프플래닛생명보험주식회사
- URL: https://www.lifeplanet.co.kr/disclosure/good/HPDA45S2.dev
- Accessed: 2026-09-03
- Retrieved: **in part** (the guarantee-ladder rows returned; the current-month declared rate
  and the 경과기간별 중도해지율 tab are rendered client-side and did not return)
- What it is good for: a third guarantee ladder shape (1.25% / 1.00% / **0.75%**) with the
  effective dates of the products it applies to.

### S16 — 하나생명, 「연금저축 비교공시 — 가입시 유의사항」
- Publisher: 하나생명보험주식회사 (reproducing the standard 연금저축 비교공시 boilerplate)
- URL: https://www.hanalife.co.kr/anm/annuityProduct/annuityProduct_tab4.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, read)
- What it is good for: the four-way comparison table (연금저축신탁 / 연금저축펀드 / 생보
  연금저축보험 / 손보 연금저축보험) on 납입방식, 연금수령기간, 원금보장 and 예금자보호 — the
  crispest single statement of what distinguishes the three wrappers.

### S17 — 손해보험협회 공시실, 「연금저축 비교공시 — 상품별 수익률·수수료율」
- Publisher: 손해보험협회 (General Insurance Association of Korea)
- Document: comparison table, 작성기준일 **2026년 06월말**
- URL: https://kpub.knia.or.kr/productDisc/pensionSaving/pensionSavingProductProfit.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, table read)
- What it is good for: product-level 연평균수익률 and 누적 연평균 수수료율 for non-life
  연금저축 products. The **fee-rate column is the only public per-product expense figure**
  found in this session other than the carriers' own 상품요약서.

### S18 — 손해보험협회 공시실, 「연금저축 비교공시 — 판매회사별 적립금」
- Publisher: 손해보험협회
- Document: 판매회사별 적립금 table, 기준 2026년 6월
- URL: https://kpub.knia.or.kr/productDisc/pensionSaving/pensionSavingCompanyProfit.do
- Accessed: 2026-09-03
- Retrieved: **in part** (the page returned the 판매회사별 적립금 table rather than the
  수익률·수수료율 table named in the URL; company names and reserve amounts were read, the
  individual figures were not transcribed)

### S19 — 금융감독원 통합연금포털, 연금저축 비교공시 › 판매회사별 적립금
- Publisher: 금융감독원 (Financial Supervisory Service)
- URL: https://www.fss.or.kr/fss/lifeplan/goodsCmpr/list.do?menuNo=200961
- Accessed: 2026-09-03
- Retrieved: **in part** — the page returned a **stale quarter ('22.2분기)** rather than the
  current one, because the quarter selector is a client-side control. The category list (수익률
  / 수수료율 / 장기 수익률 / 장기 수수료율, each at 3/5/7/10 years) was read and is reliable;
  the figures are four years out of date and are **not** used for any current parameter.

### S20 — 생명보험협회 공시실 (pub.insure.or.kr)
- Publisher: 생명보험협회 (Korea Life Insurance Association)
- URL: https://pub.insure.or.kr/
- Accessed: 2026-09-03
- Retrieved: **in part** — the landing page returned its category tree (상품비교공시 with a
  저축성보험 › 연금 branch, 경영공시, 대출공시, 기타공시) but every leaf table is loaded
  client-side and none returned. Recorded because the house brief names this site as the best
  single source of quantitative Korean product data; in this session it was reachable but not
  readable, and its role was filled by the carriers' own 상품요약서 [S1] [S2] [S7] and the
  non-life association's mirror [S17].

### S21 — 한화생명 공시실, 「적용이율」
- Publisher: 한화생명보험주식회사
- URL: https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do?MENU_ID1=DF_GDAR000
- Accessed: 2026-09-03
- Retrieved: **no** — navigation shell only; the rate table is loaded client-side. The
  carrier's guarantee ladder was obtained from its 약관 instead [S4].

---

## Regulatory and actuarial references

### R1 — 소득세법 제59조의3 (연금계좌세액공제)
- Publisher: 대한민국 국회 / 법제처; consulted through CaseNote
- URL: https://casenote.kr/법령/소득세법/제59조의3
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch; 제1항 and the paragraph structure returned)
- Version returned: 법률 제19196호, 시행 2023. 1. 1., 개정 2022. 12. 31.
- Content: the credit itself — 12% of contributions to a 연금계좌, or 15% where 종합소득금액 ≤
  ₩45,000,000 (or 총급여액 ≤ ₩55,000,000 for employment income only); contributions to a
  연금저축계좌 above ₩6,000,000 a year excluded, and the 연금저축 (within that ₩6,000,000) plus
  퇴직연금계좌 total above ₩9,000,000 a year excluded. Paragraphs 2–5 delegate the definitions,
  the ISA-conversion inclusion and the procedure to the Enforcement Decree.
- **Note on the version:** the retrieved text is the 2023-01-01 consolidation, which is the
  amendment that raised the caps from ₩4,000,000 / ₩7,000,000 to ₩6,000,000 / ₩9,000,000 and
  removed the age-and-income-based sub-cap. No later amendment to this article was found in
  this session, and the caps it states match every 2026-vintage carrier document retrieved [S2]
  [S11] and the tax authority's own page [R8].

### R2 — 소득세법 제20조의3 (연금소득)
- Publisher: 대한민국 국회 / 법제처; consulted through CaseNote
- URL: https://casenote.kr/법령/소득세법/제20조의3
- Accessed: 2026-09-03
- Retrieved: **yes**
- Version returned: 법률 제19933호, 시행 2024. 1. 1., 개정 2023. 12. 31.
- Content: 제1항제2호 makes an amount withdrawn from a 연금저축계좌 or 퇴직연금계좌
  "대통령령으로 정하는 연금형태 등으로 인출하는 경우" into 연금소득, decomposed into 가목
  untaxed 퇴직소득, 나목 contributions that received the 제59조의3 credit, and 다목 investment
  return. 제3항 defines 연금소득금액 as the total less the 연금소득공제 of 제47조의2. **The
  가/나/다 split is the whole architecture of the withdrawal tax**: only 나목 and 다목 money is
  exposed to the 연금소득세 rates of R5, and money that never got a credit is outside the
  charge entirely.

### R3 — 소득세법 제14조 제3항 (분리과세 소득)
- Publisher: 대한민국 국회 / 법제처; consulted through CaseNote
- URL: https://casenote.kr/법령/소득세법/제14조
- Accessed: 2026-09-03
- Retrieved: **yes**
- Version returned: 법률 제19933호, 시행 2024. 1. 1.
- Content: 제9호 defines 분리과세연금소득 — 가목 퇴직소득 taken as an annuity, 나목 withdrawals
  for medical or 부득이한 사유 reasons, and **다목 "가목 및 나목 외의 연금소득의 합계액이 연
  1천500만원 이하인 경우 그 연금소득"**, with the taxpayer free to elect aggregation instead.
  제8호나목 routes 제21조제1항제21호 연금외수령 기타소득 into separate taxation as well. This
  is the article that fixes the **₩15,000,000 threshold** — raised from ₩12,000,000 for the
  2023 tax year onward.

### R4 — 소득세법 제64조의4 (분리과세연금소득에 대한 세액 계산의 특례)
- Publisher: 대한민국 국회 / 법제처; consulted through CaseNote
- URL: https://casenote.kr/법령/소득세법/제64조의4
- Accessed: 2026-09-03
- Retrieved: **yes**
- Version returned: 법률 제19196호, 시행 2023. 1. 1., 신설 2022. 12. 31.
- Content: where a resident's pension income *exceeds* the 분리과세 threshold, the tax may be
  computed as the lesser of the ordinary aggregate charge and a charge that applies **100분의
  15** to the non-separately-taxed pension income. This is the statutory basis of the "16.5%
  including local income tax" separate-taxation election that every carrier document describes
  for above-threshold annuities.

### R5 — 소득세법 제129조 (원천징수세율), 제1항 제5호 and 제5호의2
- Publisher: 대한민국 국회 / 법제처; consulted through 국가법령정보센터 and CaseNote
- URLs:
  - https://www.law.go.kr/LSW//lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000821176&lsId=001565&print=print
    (the `print=print` article form — **this is the law.go.kr URL shape that returns text**)
  - https://casenote.kr/법령/소득세법/제129조
- Accessed: 2026-09-03
- Retrieved: **yes**, and in two versions, which is the point:
  - CaseNote returned 법률 제19196호, **시행 2025. 1. 1.**: 제5호의2 다목 reads 「사망할 때까지
    연금수령하는 대통령령으로 정하는 종신계약에 따라 받는 연금소득에 대해서는 **100분의 4**」.
  - 국가법령정보센터's print form returned 법률 **제21221호, 개정 2025. 12. 23., 시행
    2026. 1. 1.**, in which the same 다목 reads 「… **100분의 3**」.
- Content: 제5호 taxes 공적연금소득 at the basic rates. 제5호의2 가목 taxes private pension
  income at 5% under 70, 4% from 70 to under 80, and 3% at 80 and over; 나목 was deleted on
  2014-12-23; 다목 applies the 종신계약 rate. **The reduction of the 종신계약 rate from 4% to
  3% with effect from 2026-01-01 is the most recent substantive change in this file** and is in
  force at the access date.

### R6 — 소득세법 시행령 제40조의2 (연금계좌 등)
- Publisher: 대한민국 정부 / 법제처
- URLs (three independent retrievals, deliberately):
  - https://www.law.go.kr/LSW//lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000656323&lsId=003956&print=print
    — returned **대통령령 제36343호, 일부개정 2026. 5. 22., 시행 2026. 7. 1.**
  - https://www.nhis.or.kr/lm/lmxsrv/law/lawLinkContentView.do?SEQ=393&LINKCODE=c004000200
    — the 국민건강보험공단 law mirror, returned the same provisions
  - the 부록 of [S3], which reproduces 제2항–제5항 verbatim as filed contract wording
- Accessed: 2026-09-03
- Retrieved: **yes**
- Content: 제2항 sets the ₩18,000,000 annual contribution ceiling and the ISA-conversion
  add-on, and bars further contributions once annuitisation has been requested. 제3항 sets the
  three-limb 연금수령 test and the 연금수령한도 formula. 제4항 defines 연금수령연차 and the ≥
  11 disapplication, with 기산연차 6 for accounts opened before 2013-03-01 and inheritance of
  the deceased's 연금수령연차 on spouse succession. 제5항 deems any excess over the
  연금수령한도 to be 연금외수령.

### R7 — 소득세법 시행령 제187조의2 (종신계약의 범위)
- Publisher: 대한민국 정부 / 법제처
- URLs tried:
  - https://www.taxcanvas.kr/core/law/0039562026052236343/history/2026-05-22/articles/0187021
  - https://www.nhis.or.kr/lm/lmxsrv/law/joHistoryContent.do?SEQ=393&SEQ_CONTENTS=4454757&DATE_START=20241112&DATE_END=20240702
  - https://elaw.klri.re.kr/kor_service/lawViewTitle.do?hseq=42184
- Accessed: 2026-09-03
- Retrieved: **no** — the first two returned navigation only, and the KLRI English-law site
  returned the article's **title in both languages** ("종신계약의 범위" / "Scope of Life-Long
  Pension Agreement", 대통령령 제27829호, 2017-02-03) but not its body.
- Consequence: **the existence, number and subject of the article are verified; its operative
  text is not.** Search snippets consistently gloss it as "사망일까지 연금수령하면서 중도
  해지할 수 없는 계약", and that gloss matches every retrieved carrier's 종신연금형 wording —
  which does forbid surrender after the first annuity payment [S4] [S5] [S9] [S10] — but the
  definition itself is `[unverified]` in this file. See §6 and the gap list.

### R8 — 국세청, 「연금계좌 세액공제」
- Publisher: 국세청 (National Tax Service)
- URL: https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7875
- Accessed: 2026-09-03
- Retrieved: **yes**
- Content: the administrative restatement of R1 as a two-row table (≤ ₩45m → 15%,
  > ₩45m → 12%, both on ₩6,000,000 / ₩9,000,000 including 퇴직연금), the account-type
  definitions, and the **ISA-conversion add-on: 10% of the transferred amount, capped at
  ₩3,000,000**, citing 소득세법 시행령 제40조의2제2항라목 as amended 2025-02-28.

### R9 — 국세청, 「연금소득 원천징수 방법」
- Publisher: 국세청
- URL: https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=6608&cntntsId=7888
- Accessed: 2026-09-03
- Retrieved: **yes**
- Content: the withholding-rate table for private pension income — 70세 미만 5%, 70세 이상 80세
  미만 4%, 80세 이상 3% — and separately **종신계약 3%, footnoted as applying from 2026-01-01
  (previously 4%)**, corroborating R5. It also gives the 이연퇴직소득 rule as (이연퇴직소득세 /
  이연퇴직소득) × 70%, with 60% and 50% variants applying from 2026-01-01 by length of payout
  period, and states the > ₩15,000,000 election of 분리과세 15%.

### R10 — 금융감독원 통합연금포털, 「연금세제 안내 › 연금저축 세제 › 세액공제」
- Publisher: 금융감독원
- URL: https://fss.or.kr/fss/main/contents.do?menuNo=201007
- Accessed: 2026-09-03
- Retrieved: **yes** (the rate table returned; the worked examples and the page's last-updated
  stamp did not)
- Content: the supervisor's own statement of the credit, **grossed up for local income tax**:
  종합소득 과세표준 ≤ ₩45,000,000 (총급여 ≤ ₩55,000,000) → **16.5%**; above → **13.2%**;
  세액공제 한도 ₩6,000,000 in both rows. This is the document that ties the statutory 15% / 12%
  of R1 to the 16.5% / 13.2% every carrier quotes.

### R11 — 법제처 찾기쉬운 생활법령정보, 사적연금제도 › 개인연금제도 › 연금저축
- Publisher: 법제처 (Ministry of Government Legislation)
- URL: https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2056&ccfNo=3&cciNo=2&cnpClsNo=1
- Accessed: 2026-09-03
- Retrieved: **yes**
- Content: the official plain-language consolidation, with article pinpoints throughout — the
  연금저축계좌 definition (소득세법 제20조의3제1항제2호, 시행령 제40조의2제1항제1호), the three
  wrapper forms and who may write each, the ₩18,000,000 ceiling (시행령 제40조의2제2항제1호 및
  제3항제2호), the three-limb 연금수령 test, the 세액공제, and — most usefully — the **current
  withholding table including the 2026 change**: 70세 미만 확정형 5.5% / 종신형 3.3%; 70–80세
  확정형 4.4% / 종신형 3.3%; 80세 이상 3.3%, with excess over the 연금수령한도 charged at 16.5%
  기타소득세 (citing 소득세법 제143조의2제2항 and 제14조제3항제8호나목).

### R12 — 금융감독원, 「연금저축 길라잡이」
- Publisher: 금융감독원 (the guide is the FSS's; the copy retrieved is the one republished by
  ABL생명 on its own site — the PDF's file name and internal navigation are the FSS's)
- Document: consumer guide, 12 pp. PDF, internal date stamp 150401
- URL: https://abllife.co.kr/cms/adm/attach/attach06/attach061/attach0611/연금저축_길라잡이(150401).pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 12 pp., parsed locally with `sort=True`)
- **Vintage caution:** the tax figures in this guide are the 2015 ones (₩4,000,000 cap, 13.2%)
  and are superseded; it is cited only for structural facts and for its fee comparison, never
  for a tax parameter.
- Content: the four-column comparison of 연금저축신탁 / 연금저축펀드 / 생보 연금저축보험 / 손보
  연금저축보험 across 납입방식, 적용금리, 연금수령기간, 원금보장 and 예금자보호; the statement
  that **생보사 products can pay a life annuity and 손보사 products can pay for at most 25
  years**; the fee-shape contrast (bank and securities charge on the accumulated balance,
  insurers charge on the premium); and a **worked 연금수령한도 calculation** — a 43-year-old
  joining on a 10-year term, starting at 55 with ₩50,000,000: 50,000,000 ÷ (11 − 1) × 1.2 =
  ₩6,000,000.

### R13 — 금융감독원, 「'2025년 우리나라 연금저축(PSA) 투자 백서' 연금저축 적립금 198조 원
(+19.3조원), 수익률 10.6%(+6.9%p) 달성」 (보도자료)
- Publisher: 금융감독원 연금감독실 (연금혁신팀), 등록일 2026-06-18
- URL: https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=218674&menuNo=200218
- Accessed: 2026-09-03
- Retrieved: **in part** — the press-release body returned (title, issuer, headline
  statistics); the attached hwpx and pdf, which hold the detailed tables including the
  payout-phase statistics, did not.
- Content retrieved: end-2025 적립금 198.2조원 (+19.3조원, +10.8%); 가입자 840.3만명
  (+76.1만명, +10.0%); by wrapper 연금저축보험 114.1조원, 연금저축펀드 61.3조원 (+50.7%),
  연금저축신탁 13.8조원; 2025 annual return 10.6%, 펀드·ETF 29.3%.

### R14 — 보험업감독규정 [별표 14] 「표준해약환급금 계산시 적용되는 해약공제액」(제7-66조 관련)
- Publisher: 금융위원회 (regulation); file served by 법제처 국가법령정보센터
- Document: 별표 14, 개정 2011.1.24 / 2015.5.7 / 2020.1.15, 1 p. PDF (법제처 stamp 2024-02-01)
- URL: https://www.law.go.kr/LSW//flDownload.do?flSeq=137472119&flNm=%5B%EB%B3%84%ED%91%9C+14%5D+%ED%91%9C%EC%A4%80%ED%95%B4%EC%95%BD%ED%99%98%EA%B8%89%EA%B8%88%EA%B3%84%EC%82%B0%EC%8B%9C+%EC%A0%81%EC%9A%A9%EB%90%98%EB%8A%94+%ED%95%B4%EC%95%BD%EA%B3%B5%EC%A0%9C%EC%95%A1%28%EC%A0%9C7-66%EC%A1%B0%EA%B4%80%EB%A0%A8%29
- Accessed: 2026-09-03
- Retrieved: **yes** (PDF downloaded, 1 p., parsed locally; the whole table and all seven notes
  extract cleanly)
- Content: the statutory cap on the surrender charge, and — in 주5 — the
  **연금저축보험-specific rule**. Quoted in full in §16. This is the single most directly
  model-relevant regulatory document in this file.

### R15 — 보험업감독규정 (본문)
- Publisher: 금융위원회; 국가법령정보센터 행정규칙 view
- URL: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196
- Accessed: 2026-09-03
- Retrieved: **no** — the page returns its metadata (시행 2023. 3. 2., 금융위원회고시
  제2023-10호) and its navigation tree, but the article bodies are rendered client-side.
  제1-2조 (정의) and 제7-66조 could not be read. What is known of them here comes from the 별표
  [R14] and from carrier documents citing them [S2] [S8].

### R16 — 보험업법 제176조 (보험요율 산출기관)
- Publisher: 대한민국 국회 / 법제처; consulted through CaseNote
- URL: https://casenote.kr/법령/보험업법/제176조
- Accessed: 2026-09-03
- Retrieved: **yes**
- Version returned: 법률 제17636호, 시행 2020. 12. 8.
- Content: the statutory office of the 보험요율산출기관 — 순보험요율의 산출·검증 및 제공, 보험
  관련 정보의 수집·제공 및 통계의 작성, 조사·연구, and delegated work; 제5항 obliges it to
  integrate and accumulate industry statistics systematically. The retrieved page also carries
  case-law commentary noting that an insurer is **not bound** by the 참조순보험요율 it files.
  This is the legal frame for 보험개발원's 경험생명표 and 개인연금사망률.

### R17 — 보험개발원 보도자료 목록
- Publisher: 보험개발원 (Korea Insurance Development Institute, KIDI)
- URL: https://www.kidi.or.kr/user/nd11592.do
- Accessed: 2026-09-03
- Retrieved: **in part** — the list page returned rows 740–746 (2026-05 to 2026-08) with titles
  and dates, but **no 경험생명표 item appears in the visible window**, and every item link is a
  `javascript:goBoardView(...)` call, so no individual release could be opened. The 제10회
  경험생명표 announcement is older than the visible window and could not be reached by paging.

### R18 — 보험매일, 「제10회 경험생명표 개정…소비자에 미치는 영향은」
- Publisher: 보험매일 (fins.co.kr), 김명재 기자, 2024-01-10
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News source.** Used because the primary KIDI release could not be reached [R17].
- Content: 제10회 경험생명표 평균수명 남자 86.3세, 여자 90.7세 (+2.8 / +2.2 on 제9회); insurers
  to price on it "오는 4월부터"; annuity premiums to rise and 종신보험 premiums to fall; and
  the operative limitation that **the revised table applies to new business only — existing
  policyholders' premiums do not change.**

### R19 — 보험저널, 「4월부터 연금보험 수령액 줄어든다…10차 경험생명표 적용시 15% 하락」
- Publisher: 보험저널 (insjournal.co.kr), 강성용 기자, 2024-02-15 (수정 2024-02-20)
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=21975
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News source.**
- Content: a three-generation comparison on a fixed ₩200,000,000 fund annuitising at 60 — 6차
  to 78.4세 (18.4 years) at ₩906,000/month, 9차 to 85.3세 at ₩709,000/month, and 10차 to 86.3세
  (26.3 years) at "60만원 후반" per month. The article does **not** distinguish 가입시점 from
  개시시점 application.

### R20 — 웰스매니지먼트, 「2024년 개정 경험생명표 보험료 영향은 [WM 칼럼]」
- Publisher: 웰스매니지먼트 (wealthm.co.kr), 김희정 (부산은행 화명동금융센터 PB팀장),
  2024-07-03
- URL: http://www.wealthm.co.kr/news/articleView.html?idxno=11407
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News/opinion source.**
- Content: quantified premium effects (종신보험 about −5%, 암보험 about +10%; the 2019 revision
  cut 종신보험 premiums 3.8% on average), and the statement that 「기존 가입자는 가입 당시
  경험생명표를 바탕으로 이미 보험료가 결정돼 있어 영향을 받지 않는다」.

### R21 — 조세일보, 「[조세] 근로·퇴직·이연퇴직소득 등 과세제도 개선 [2025년 조세개정안]」
- Publisher: 조세일보 (joseilbo.com), 2025-07-31
- URL: https://m.joseilbo.com/news/view.htm?newsid=549483
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News source**, used to date and explain the amendment whose enacted text is R5.
- Content: the 2025 tax bill reduced the 종신계약 withholding rate to 3% and extended the
  이연퇴직소득 reduction to 50% for payouts running beyond 20 years, applying to pensions
  received on or after 2026-01-01.

### R22 — 뉴스핌, 「연금저축 적립금 198조 돌파…펀드 비중 급증에 '머니무브' 뚜렷」
- Publisher: 뉴스핌 (newspim.com), 2026-06-18
- URL: https://www.newspim.com/news/view/20260618000323
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News source**, reporting R13; used for the figures the press-release body did not carry.
- Content: 계약건수 1,079.6만건 (+107.9만건, +11.1%); 납입액 13.5조원 (+18.1%); 신규 계약건수
  144.3만건 (+51.9%); wrapper shares 보험 57.6%, 펀드 30.9%, 신탁 6.4%; and by seller 보험회사
  114.3조원 (57.7%), 금융투자회사 55.4조원 (27.9%), 은행 19.5조원 (9.8%), 공제기관 9.0조원
  (4.6%).

### R23 — 헤럴드경제, 「12년만에 연금저축 세제개편…연금수령 "늦을수록 유리해져요"」
- Publisher: 헤럴드경제 (biz.heraldcorp.com), 김양규 기자, 2013-01-10
- URL: https://biz.heraldcorp.com/article/3793400
- Accessed: 2026-09-03
- Retrieved: **yes**
- **News source, and a 2013 one** — retrieved while looking for the reform history and kept
  only for that. It describes the 2013 redesign as it was *proposed*: the separate-taxation
  ceiling rising from ₩6,000,000 to ₩12,000,000, the 5.5/4.4/3.3 age banding, a minimum payout
  period lengthening from 5 to 15 years, and an annual withdrawal cap of one fifteenth of the
  balance with a 22% 기타소득세 above it. **The 1/15 cap and the 22% rate are not the law that
  was enacted** — the enacted rule is the 11-year / 120% formula of R6 and the 15% (16.5%) rate
  of R5. Cited only for the fact that the reform happened and for the ₩12,000,000 threshold of
  that era.

### R24 — 보험개발원 보험정보 빅데이터 플랫폼, 「경험생명표」
- Publisher: 보험개발원
- URL: https://bigin.kidi.or.kr:9443/boarddetail/nd00017_6041
- Accessed: 2026-09-03
- Retrieved: **no** — `connect ECONNREFUSED 61.107.27.12:9443`. The host resolves but refuses
  connections on that port from this session.

### R25 — 푸르덴셜생명, 「경험생명표 적용 시점에 따라 평생 연금액이 달라진다?」
- Publisher: 푸르덴셜생명 (now KB라이프생명)
- URL: https://www.prudential.co.kr/plan-your-story/content/retirement/retirement-18.aspx
- Accessed: 2026-09-03
- Retrieved: **no** — `getaddrinfo ETIMEOUT www.prudential.co.kr`. This was the most directly
  on-point secondary source found for the 가입시점-versus-개시시점 question and its loss is the
  main reason that question is answered from 약관 wording instead.

---

## Fact extraction

### 1. What the product is, and the statutory frame

- 연금저축 is not a product but a **tax wrapper defined by the income tax code**. A
  연금저축계좌 is an account "설정하는 계약" with an authorised financial institution under
  소득세법 제20조의3제1항제2호 and 시행령 제40조의2제1항제1호 [R11] [R2]. The insurance form of
  it, 연금저축보험, is simply the wrapper written as an insurance contract.
- The three forms are 연금저축신탁 (a trust contract with an authorised 신탁업자, i.e. a bank),
  연금저축펀드 (a brokerage contract for collective-investment securities with an authorised
  투자중개업자), and 연금저축보험 (an insurance contract) [R11] [R12] [S16].
- Both **life insurers and non-life insurers** may write 연금저축보험 [R12] [S16] [S8]. The two
  are not equivalent: see §3 and §19.
- Every carrier document opens by insisting the contract is **not a bank deposit** — 「이
  보험은 저축성보험으로 은행의 예⋅적금 및 펀드 등과 다른 상품입니다. 이 보험은 중도에 해지할
  경우 원금 손실이 발생할 수 있습니다」 [S6], and 「본 상품은 저축성 보험으로 은행의
  예금·적금과는 다른 상품입니다」 [S2].
- The contract is a **금리연동형 보험**: 「이 보험의 계약자적립액 산출에 적용되는 이율은 매월
  변동됩니다」, and the rate applies only to what is left after expense and risk deductions —
  「동 이율은 납입한 주계약(또는 적립) 보험료에서 계약체결·유지관리에 필요한 경비 및 위험보장을
  위한 보험료를 차감한 금액에 대해서만 적용됩니다」 [S4] [S6].
- The product is **저축성보험** in the supervisory taxonomy, which under 보험업감독규정 제1-2조
  requires that the survival benefits exceed premiums paid. Two carriers state this and use it
  to explain why the annuity start date is **automatically deferred** if a payment holiday or a
  reinstatement would otherwise leave the fund below premiums paid at annuitisation [S8] [S7].
  The regulation's own text could not be read [R15].

### 2. History of the wrapper, in outline

- The present 연금저축계좌 regime dates from **2013-03-01**, when the 소득세법 rules replaced
  the 2001-vintage 연금저축 [R23] `[unverified]` as to the exact commencement date; the 2013
  date is corroborated by the 기산연차 rule in 시행령 제40조의2제4항제1호, which gives a 6-year
  starting count to accounts opened **before 2013년 3월 1일** [R6], and by the ABL transfer
  rule that treats a transfer from a post-2013-03-01 account into a pre-2013-03-01 account as a
  taxable withdrawal [S1].
- Relief on contributions moved from **소득공제 to 세액공제** in the 2014 tax year [R23]
  `[unverified]` — no retrieved statute or official page states the switch date.
- The separate-taxation ceiling for private pension income was **₩12,000,000** for the
  2013–2022 tax years [S1] [S5] [S2] [R23] and is **₩15,000,000** from the 2023 tax year [R3
  제14조제3항제9호다목].
- The credit caps were **₩4,000,000 (연금저축) / ₩7,000,000 (합산)** in the older generation
  [S5] [S3] and are **₩6,000,000 / ₩9,000,000** now [R1] [R8] [R10].
- The 종신계약 withholding rate fell from **4% to 3%** for pensions received on or after
  **2026-01-01**, by 법률 제21221호 of 2025-12-23 [R5] [R9] [R21].
- **Documents retrieved in this session straddle all of these changes.** A carrier document's
  tax paragraphs date it: [S5] (2016) states ₩4,000,000 / 13.2% / ₩12,000,000 / 종신형 4.4%;
  [S3] (2021) states ₩4,000,000 with a ₩3,000,000 high-income sub-cap; [S1] and [S2] (2026)
  state ₩6,000,000 but [S1]'s tax note is itself stamped 「'16년 12월 현재」 and still says
  ₩12,000,000. **Do not read a tax parameter off a carrier document.** The tax parameters in
  this file come from [R1]–[R11].

### 3. The three wrappers compared

From the standard 연금저축 비교공시 boilerplate [S16] and the supervisor's guide [R12]:

| | 연금저축신탁 (은행) | 연금저축펀드 (자산운용사) | 연금저축보험 (생보) | 연금저축보험 (손보) |
|---|---|---|---|---|
| 납입방식 | 자유납 | 자유납 | 정기납 | 정기납 |
| 적용금리 | 실적배당 | 실적배당 | 공시이율 | 공시이율 |
| 연금수령기간 | 확정기간 | 확정기간 | **종신, 확정기간** | 확정기간 (최대 25년) |
| 원금보장 | 보장 | 미보장 | 보장 | 보장 |
| 예금자보호 | 적용 | 미적용 | 적용 | 적용 |

- 자유납 means the amount and timing are at the saver's discretion; 정기납 means a set amount
  on a set cycle [R12].
- **Only a life insurer's 연금저축보험 can pay for life.** 「생명보험사의 연금저축보험은
  가입자가 연금을 종신으로 수령할 수 있도록 선택할 수 있으나, 손해보험사의 연금저축보험은 최대
  25년까지 연금수령이 가능합니다」 [R12]. The retrieved non-life contract bears this out
  exactly: its only 연금지급형태 is 정액형 over a 연금지급기간 of **5년 ~ 25년**, with no life
  contingency anywhere [S8].
- Fee **shape** differs by wrapper, not just level: 「(은행·증권사) 가입자의 납입금을 운용하여
  쌓아놓은 적립금에 비례하여 수수료를 부과(예: 누적적립금 대비 1%)하므로 매년 수수료가 증가하는
  구조 … (보험사) 보험료에 비례하여 수수료를 부과(예: 납입보험료 대비 9%)하므로 납입기간(예 :
  10년) 동안 매년 수수료가 부과되는 구조」 [R12]. This is why an insurance wrapper has a
  front-loaded negative return and a fund wrapper does not: 「연금저축보험은 납입하신
  보험료에서 사업비를 차감한 금액에 공시이율을 적용하여 적립되므로 계약 초기에는 마이너스(-)
  수익률이 발생하여 계약해지시 환급금이 납입금액보다 적을 수 있으니 유의하시기 바랍니다」
  [R12].

### 4. Contributions, the annual ceiling, and 세액공제

- **Annual contribution ceiling: ₩18,000,000 (1,800만원)** across *all* 연금계좌 the saver
  holds at every institution, excluding rider premiums other than the 연금저축추가납입특약 [R6
  제40조의2제2항제1호] [R11] [S1] [S2] [S8]. [S1] states it as 「납입보험료의 연간
  합계액(연금계좌를 취급하는 금융회사에 가입한 연금계좌의 합계액을 말하며, 특약보험료는 제외)은
  1,800만원 이내로 하며」.
- No contribution may be made after annuitisation has been requested [R6 제40조의2제2항제2호].
- **Credit-eligible contributions**: up to **₩6,000,000 (600만원)** a year to 연금저축계좌; and
  up to **₩9,000,000 (900만원)** a year counting 연금저축 (within its own ₩6,000,000) plus
  퇴직연금계좌 contributions [R1 제59조의3제1항] [R8] [R10] [S2] [S11].
- **Credit rate**, statutory: **12%**, or **15%** where 종합소득금액 ≤ ₩45,000,000 — or, for a
  taxpayer with employment income only, 총급여액 ≤ ₩55,000,000 [R1] [R8].
- **Credit rate including 지방소득세** — the figure every consumer document uses: **13.2%** and
  **16.5%** respectively [R10] [S5] [S11] [S16]. The 지방소득세 add-on is one tenth of the
  income-tax figure (1.2 and 1.5 percentage points) [S5].
- Maximum annual credit at the ₩9,000,000 cap: **₩1,485,000** at 16.5% and **₩1,188,000** at
  13.2% `[derived]`; on the ₩6,000,000 연금저축-only cap, **₩990,000** and **₩792,000**
  respectively [S11].
- **ISA conversion add-on**: where an 개인종합자산관리계좌 matures and its balance is paid into
  a 연금계좌, that amount is included, and the credit limit is enlarged by **10% of the
  converted amount, capped at ₩3,000,000** [R8, citing 소득세법 시행령 제40조의2제2항라목 as
  amended 2025-02-28] [R1 제59조의3제3항].
- **Contributions above the credit cap are not wasted but are not relieved.** A contract lets
  the saver ask, before requesting annuitisation, that previously uncredited contributions be
  reclassified into the current tax year — 「이전 과세기간에 납입한 보험료 중
  연금계좌세액공제를 받지 않은 금액이 있는 경우로서 … 전환하여 줄 것을 회사에 신청한 경우에는
  전환신청한 금액을 연금계좌에서 인출하여 그 신청을 한 날에 다시 해당 연금계좌에 납입한 것으로
  봅니다」 [S3 제21조①].
- Money that never received a credit is **outside the withdrawal charge entirely**:
  「세액공제를 받은 금액을 초과하여 납입한 금액은 과세되지 않습니다」 [S1], and the tax base is
  only 가목/나목/다목 money under 소득세법 제20조의3제1항제2호 [R2].
- **Additional premium (추가납입)** is written through a 제도성특약, the 연금저축추가납입특약,
  and is capped at **200% of the year's basic premiums** [S2] [S8] [S5], payable from a stated
  point after inception until a stated point before annuitisation — 「계약일 이후 [n]개월이
  지난 후부터 연금개시나이 [n]세 계약해당일까지」 [S7], 「「연금지급개시나이-2년」 까지」 [S5]
  — and always inside the ₩18,000,000 aggregate [S2] [S7] [S8].

### 5. 연금수령 — the three-limb statutory test

A withdrawal is 연금수령 (and therefore taxed as pension income rather than as 기타소득) only
if **all three** of the following hold. Verbatim, from 소득세법 시행령 제40조의2제3항 [R6],
reproduced identically in a filed 약관 부록 [S3]:

1. 「가입자가 55세 이후 연금계좌취급자에게 연금수령 개시를 신청한 후 인출할 것」
2. 「연금계좌의 가입일부터 5년이 경과된 후에 인출할 것」 — disapplied where the account holds
   이연퇴직소득
3. 「과세기간 개시일(연금수령 개시를 신청한 날이 속하는 과세기간에는 연금수령 개시를 신청한
   날로 한다) 현재 다음의 계산식에 따라 계산된 금액(이하 "연금수령한도"라 한다) 이내에서 인출할
   것」

- The **age test uses 만나이, not 보험나이**. One contract says so in terms: 「이 약관에서의
  피보험자의 나이는 보험나이를 기준으로 합니다. 다만, 연금개시나이가 만 55세 이상에 해당되는지
  여부의 판단은 실제 만 나이를 적용합니다」 [S6 제20조①]. See §22.
- **연금수령한도** (R6 제40조의2제3항제3호, reproduced at [S3] and [S1]):

  ```
                       연금계좌의 평가액          120
  연금수령한도  =  ────────────────────────  ×  ─────
                     (11 − 연금수령연차)          100
  ```

  [S1] renders it as 「과세기간개시일 현재 연금재원평가 총액 ÷ (11 − 연금수령연차) × 120%」.
- **연금수령연차** is 「최초로 연금수령할 수 있는 날이 속하는 과세기간을 기산연차로 하여 그
  다음 과세기간을 누적 합산한 연차」, and where it is **11 or more the formula does not apply
  at all** — the whole balance may be taken as pension income [R6 제40조의2제4항] [S1] [S3].
  Two exceptions to the starting count: an account opened before 2013-03-01 starts at
  **6년차**, and an account inherited under 제44조제2항 starts at the deceased's own
  연금수령연차 [R6].
- **Excess is deemed non-pension**: 「연금계좌에서 연금수령한도를 초과하여 인출하는 금액은
  연금외수령하는 것으로 본다」 [R6 제40조의2제5항].
- Worked example, from the supervisor's guide [R12]: a 43-year-old on a 10-year term starting
  at 55 with a ₩50,000,000 balance has 연금수령연차 = 1 in the first year (the five-year test
  is met at 48 but 만 55세 is not, so 만 55세 is year 1), giving 50,000,000 ÷ (11 − 1) × 1.2 =
  **₩6,000,000**. The guide adds 「연금을 만55세부터 수령할 경우 10년이상 연금을 수령하셔야
  세제상 불이익이 없습니다」.
- Because 연금수령연차 climbs by one each tax year, the limit is a **rising fraction of the
  balance** — 12% in year 1, 13.33% in year 2, … 60% in year 9, 120% in year 10, unlimited from
  year 11 `[derived]` from [R6]. In practice this makes ten years the shortest payout the tax
  code will tolerate without penalty for a contract annuitised as soon as it can be.
- One carrier tabulates the same thing as a **최소 연금지급기간** by the gap between joining
  and annuitising [S3]. For a contract taken out before age 50 with no 이연퇴직소득:

  | 연금개시시점 | 55세 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 | 64 | 65세 이후 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | 최소 연금지급기간 | 10년 이상 | 9년 | 8년 | 7년 | 6년 | 5년 | 4년 | 3년 | 2년 | 1년 | 요건 없음 |

  For a contract taken out at 50 or later the same ladder is keyed to years since joining (5년
  → 10년 이상, 6년 → 9년 이상, … 15년 이후 → 요건 없음); for one taken out at 55 or later with
  이연퇴직소득 it runs from 가입 즉시 → 10년 이상 down to 10년 이후 → 요건 없음. All three
  tables are footnoted 「균등수령방식 기준, 만나이 기준」 [S3].
- Every retrieved contract makes the default election the tax-efficient one: 「계약자의 특별한
  의사 표시가 없는 경우 매년 지급하는 연금액은 관련 세법에서 정한 바에 따라 연금소득으로
  인정받을 수 있는 범위 이내로 합니다」 [S3 제21조②] [S5] [S7] [S8].

### 6. 연금소득세 — the age bands and the 1,500만원 threshold

**Withholding rates on private pension income**, 소득세법 제129조제1항제5호의2 [R5]:

| Basis | Statutory rate | Including 지방소득세 |
|---|---|---|
| 연금소득자 70세 미만 | 100분의 5 | 5.5% |
| 70세 이상 80세 미만 | 100분의 4 | 4.4% |
| 80세 이상 | 100분의 3 | 3.3% |
| 종신계약에 따라 받는 연금소득 | 100분의 3 (2026-01-01 이후; 이전 100분의 4) | 3.3% (이전 4.4%) |

- The age bands are on the **연금소득자's age**, and the lowest applicable rate governs, so the
  effective schedule for a fixed-term annuity is 5.5% / 4.4% / 3.3% by age, and for a life
  annuity a flat **3.3% at every age from 55** [R9] [R11].
- Before the 2026 change the life-annuity rate was 4.4%, so the schedule for a 종신연금형 was
  4.4% until 80 and 3.3% thereafter. [S5] (2016) prints exactly that: 「55세 이상 70세 미만 —
  확정기간연금형 5.5%, 종신연금형 4.4% / 70세 이상 80세 미만 4.4% / 80세 이상 3.3%」.
- The current schedule, as the legislation office states it [R11]: 70세 미만 확정형 5.5% ·
  종신형 3.3%; 70–80세 확정형 4.4% · 종신형 3.3%; 80세 이상 3.3%.
- **The 3.3% life-annuity rate is now a 2.2-percentage-point standing advantage over a
  fixed-term annuity for a 55-to-70-year-old**, where before 2026 it was 1.1 points. This is a
  direct, dated, quantified incentive to annuitise for life and is a first-order input to any
  annuitisation-election assumption.
- 종신계약 is defined by 소득세법 시행령 제187조의2, whose **text could not be retrieved**
  [R7]. Its title is verified ("종신계약의 범위" / "Scope of Life-Long Pension Agreement",
  대통령령 제27829호, 2017-02-03), and 국세청 glosses the condition as a contract under which
  the pension is received until death and which **cannot be surrendered mid-term** — 「사망할
  때까지 중도해지 불가」 [R9]. The gloss is consistent with every retrieved 종신연금형 wording:
  「종신연금형의 경우 연금 지급이 개시된 후에는 이 계약을 해지할 수 없습니다」 [S10],
  「종신연금형을 선택하신 경우에는 연금지급개시 이후 계약을 해지할 수 없으며」 [S4 제5조③],
  「종신연금형은 연금이 지급된 이후에는 계약 해지가 불가합니다」 [S5], 「종신연금형의 경우
  연금지급개시 이후에는 해지할 수 없습니다」 [S2]. **Treat the precise statutory conditions of
  종신계약 as `[unverified]`; treat the no-surrender feature of 종신연금형 as fully sourced.**
- **Aggregation threshold.** Private pension income (excluding 공적연금소득, 이연퇴직소득 and
  부득이한 사유 withdrawals) of **₩15,000,000 (1,500만원) or less in a year** is
  분리과세연금소득: the withholding settles the liability, and the taxpayer may nonetheless
  elect to aggregate [R3 제14조제3항제9호다목].
- Above the threshold the income enters 종합소득 at the ordinary graduated rates, **or** the
  taxpayer may elect the special computation of 소득세법 제64조의4, which applies **100분의
  15** to that pension income — the "16.5% 분리과세" of the trade press [R4] [R9] [R11]. The
  election is annual and is made on the return.
- The threshold was **₩12,000,000** for the 2013–2022 tax years, which is what the older
  documents state [S5] [S2] [S1] [S3].
- **연금소득공제** applies to the aggregate 총연금액 before the graduated rates, on the
  following scale [S5]:

  | 총 연금액 | 공제액 |
  |---|---|
  | 350만원 이하 | 총 연금액 전액 |
  | 350만원 초과 ~ 700만원 이하 | 350만원 + 350만원 초과금액 × 40% |
  | 700만원 초과 ~ 1,400만원 이하 | 490만원 + 700만원 초과금액 × 20% |
  | 1,400만원 초과 | 630만원 + 1,400만원 초과금액 × 10% |

  The statutory basis is 소득세법 제47조의2 [R2 제3항]; the article's own text, and in
  particular whether an overall ceiling applies to the deduction, were **not retrieved**
  [unverified].

### 7. 연금외수령 — the 16.5% 기타소득세

- Any amount withdrawn that is not 연금수령 — a surrender, a lump sum, or the part of a
  withdrawal above the 연금수령한도 — is 기타소득 under 소득세법 제21조제1항제21호, taxed
  separately under 제14조제3항제8호나목 [R3] and withheld at **100분의 15** under
  제129조제1항제6호 [R5, article located but the sub-item text was not read — the 15% figure is
  `[unverified]` at statute level and fully sourced at contract level below].
- Every retrieved carrier document states the grossed-up rate identically as **16.5%
  (지방소득세 포함)**: [S1], [S2], [S3 제21조②], [S4], [S5], [S7], [S8], [S11], [S16]. [S3]
  verbatim: 「연금수령에 해당하지 않는 금액은 기타소득세(16.5%, 지방소득세 포함) 또는
  이연퇴직소득세(이연퇴직소득에 한함)를 납입하여야 합니다」.
- The **base** of the charge is the credited money and its return, not the whole fund. The
  non-life contract states the base most precisely: 「[해약환급금 − 실제 세액공제 받은 보험료를
  초과하여 납입한 보험료의 누계액과 연금수령액 중 큰 금액]의 16.5%(지방소득세 포함)를
  기타소득세로 원천징수」 [S8].
- One carrier's surrender illustration carries a **세후지급 예상액** column computed on exactly
  that basis, described as 「해지환급금에서 세액공제 혜택을 받은 보험료를 초과하여 납입한
  금액을 차감한 후 기타소득세(16.5%, 지방소득세 포함)를 부과한 금액」 [S5]. On its model point
  the after-tax surrender value at 20 years is **₩86,869,520 against a ₩104,003,740 surrender
  value** — an effective haircut of **16.5%** `[derived]` from [S5], confirming that on a fully
  credited contract the charge falls on essentially the whole balance.
- The consumer-detriment mechanism is stated plainly in a 민원 사례: 「고객(계약자)은 연금수령
  이전까지는 언제든지 가입한 보험을 중도에 해지할 수 있으나 소득세법 등에서 정한 법령에 따라
  기타소득세가 발생되며, 원금 손실이 발생할 수 있음」 [S4].
- **Modelling consequence.** A Korean 연금저축보험 lapse carries a tax cost of about 16.5% of
  the fund *on top of* the 해약공제 and the unrecovered acquisition expense. This is the
  clearest reason to expect a lapse curve materially flatter than on a non-qualified savings
  contract, and it is why the product-spec's lapse basis must be argued rather than borrowed.

### 8. 부득이한 사유 and 의료비인출 — the escape hatches

Where the contract is surrendered or paid otherwise than as a pension **for one of the
following reasons**, the amount is excluded from aggregation and taxed at the 연금소득세 rates
instead of the 기타소득세 rate. Verbatim list [S3 제21조④], corroborated at [S1] [S7]:

1. 계약자의 사망
2. 천재·지변
3. 계약자 또는 그 부양가족(소득세법상 기본공제 대상자, 소득의 제한은 받지 않음)의 질병·부상에
   따라 **3개월 이상의 요양**이 필요한 경우 — and here the relieved amount is capped at the sum
   of 가. **₩2,000,000**, 나. 의료비와 간병인 비용, and 다. 「연금계좌 가입자 본인의 휴직 또는
   휴업 월수(1월 미만의 기간이 있는 경우에는 이를 1월로 봅니다) × **150만원**」
4. 계약자가 「채무자 회생 및 파산에 관한 법률」에 따른 파산의 선고 또는 개인회생절차개시의
   결정을 받은 경우
5. 회사의 영업정지, 영업 인·허가의 취소, 해산결의 또는 파산선고
6. 계약자의 해외이주

- The claim must be made **within six months of the triggering event** — 「제4항 각 호에
  해당하는 경우에는 사유발생일부터 6개월 이내에 신청해야 연금소득세를 적용 받을 수 있으며」 [S3
  제21조⑥] [S5].
- **의료비인출** is a separate hatch: an amount withdrawn to meet the saver's own medical costs
  (excluding cosmetic surgery and health-promotion medicines) from a designated 의료비연금계좌
  is **taxed as pension income even where it exceeds the 연금수령한도** — 「관련 세법에서
  정하는 의료비인출에 해당하는 금액은 연금수령한도를 초과하더라도 연금소득으로 분리과세합니다」
  [S3 제21조②] [S1] [S7] [S8].
- On one contract 의료비인출 is available only after annuitisation and only up to the
  계약자적립액 backing the remaining guaranteed instalments, with an allowance for policy-loan
  principal and interest and for the withholding tax that a 연금외수령 would attract, and the
  claim must be filed within six months of paying the medical cost [S2] [S4].

### 9. Death, spouse succession, and 계약이전

- **Death before annuitisation** terminates the contract and pays the 계약자적립액 at the date
  of death — 「피보험자가 연금개시전 보험기간 중 사망한 경우에는 사망 당시의 계약자적립액을
  지급하여 드리고 이 계약은 더는 효력이 없습니다」 [S1] [S2] [S4] [S6]. Korea Post adds a
  return-of-premium floor: 「사망시 지급금액이 이미 납입한 보험료보다 적은 경우에는 이미 납입한
  보험료를 계약자에게 지급합니다」 [S7]. **There is no death cover in excess of the fund on any
  retrieved 연금저축보험** — the product carries no mortality risk before annuitisation beyond
  that floor.
- **Spouse succession.** Where the policyholder dies and the heir is the spouse, the spouse may
  take over the contract; **the spouse's 가입일 becomes the date of the deceased's death**, but
  the two dates that matter for the tax test are carried over from the deceased: 「연금수령을
  개시할 때 최소납입요건 경과 판정을 위한 가입일 및 연금수령한도 산정을 위한 연금수령연차
  기산일은 피상속인(사망한 계약자) 기준으로 적용합니다」 [S1] [S3 제21조⑤] [S6] [S7] [S8]. The
  request must be made within six months of the end of the month of death [S2] [S5] [S6] [S7],
  or within six months of the date of death on one contract [S4].
- **계약이전 (계좌이체).** The saver may move the contract to another 연금저축 at the same or a
  different institution, or to an 개인형퇴직연금 (IRP) [S1]. A transfer is **not** a withdrawal
  and attracts no income tax — 「계좌이체하는 경우 관련세법에 따라 연금계좌의 인출로 보지
  않으므로 소득세가 부과되지 않습니다」 — **except** that moving a post-2013-03-01 연금저축
  into a pre-2013-03-01 연금저축 *is* treated as a withdrawal and is taxed [S1].
- A lapsed contract whose surrender value has not been taken may be transferred **without first
  being reinstated** [S1].
- Five transfers are refused [S1]: where the receiving institution's per-person annual
  contribution ceiling would be breached; where the contract would be split by amount; where
  the contract is under attachment, provisional attachment or pledge; where the contract is a
  종신연금형 already in payment, or has a 장해연금 in payment or a premium waiver running, or
  has an unresolved claim; and where a transfer to an IRP is attempted from a contract whose
  holder is under 만 55세 or which is less than five years old.
- The carrier may charge a fee on the transfer of 해약환급금, 미경과보험료 등 제지급금 [S1].

### 10. Product envelope — issue age, terms, and premium bands

| Item | [S1] ABL 우리WON | [S2] ABL 나이스플랜 | [S6] NH e-NH | [S7] 우체국 | [S8] 현대해상 (손보) | [S11] KDB |
|---|---|---|---|---|---|---|
| 가입나이 | 0세 ~ (Y−납입기간) | (per premium term) | not extracted | 0세 ~ (연금개시나이−5) | 0세 ~ (연금개시나이−납입기간) | 만19세 ~ (연금개시나이−납입기간) |
| 연금개시나이 Y | 만 55 ~ 80세 | 65 in all illustrations | not extracted | 만 55 ~ 80세 | 만 55 ~ 80세 | 만 55 ~ 80세 |
| 납입기간 | 5 / 10 / 15 / 20년, 전기납 | 5 / 6 / 7년 이상 / 10 / 15 / 20년, 전기납 | ≥ 10년 to change | 5년 ~ 전기납 | 15 / 20년납, 전기납 (55~80세납, 최소 5년) | 5 / 7 / 10 / 20년, 전기납 |
| 기본보험료 | 월 3만원 ~ 50만원 | 월 12만 ~ 150만원 (by term) | not extracted | 월 10~75만원 (<10년납), 5~75만원 (≥10년납) | not extracted | 월 7만 ~ 150만원 |
| 납입주기 | 월납 | 월납 | not extracted | 월납 | 월납, 연납 | 월납 |
| 건강진단 | 인수지침에 따라 실시 가능 | 건강상태·직업에 따라 제한 가능 | not extracted | **전건 무진단** | 인수지침에 따라 제한 가능 | not extracted |

- [S1]'s issue-age matrix is stated as a function of the chosen annuity age Y: 5년납 → 0세 ~
  (Y−5)세, 10년납 → 0세 ~ (Y−10)세, 15년납 → 0세 ~ (Y−15)세, 20년납 → 0세 ~ (Y−20)세, 전기납 →
  0세 ~ (Y−5)세 「다만, 가입나이 (Y−9세)에서 (Y−6세)는 가입불가」.
- [S1] adds 「다만, 피보험자가 55세 계약해당일에 만55세 이상이 아닌 경우에는 연금개시나이를
  56세부터 선택할 수 있음」 — the 보험나이/만나이 gap again, this time as a product rule.
- [S2]'s premium minimum falls with the term: 5년납 월 50만원 이상, 6년납 월 15만원 이상, 7년납
  이상 월 12만원 이상, all capped at 월 150만원.
- Underwriting is light or absent. Korea Post writes the product **전건 무진단** [S7]; the
  others reserve a right to underwrite but describe no medical requirement [S1] [S2] [S8]. This
  is consistent with the absence of any death benefit above the fund (§9), and means
  **selection at issue is not a material feature of this product**.
- **Issue age can be zero.** Four retrieved contracts write from 0세 [S1] [S7] [S8] and one
  from 만19세 [S11]. A 연금저축보험 on a child is a real, sold shape, not a theoretical one —
  the tax credit accrues to the contributing adult.

### 11. The accumulation chassis — 계약자적립액 and 공시이율

- **계약자적립액** is the fund. Definition, from a 2026 document: 「「계약자적립액」이란
  순보험료(기본보험료에서 계약체결비용 및 계약관리비용을 뺀 금액)를 「공시이율」로 납입일부터
  일자계산을 하여 적립한 금액으로, 산출방법서에서 정한 바에 따라 계산합니다」 [S1] [S2].
- The non-life form splits it: 「적립순보험료 : 기본보험료에서 계약체결비용 및 계약관리비용을
  공제한 보험료와 추가납입보험료에서 계약관리비용을 공제한 보험료」 [S8] — i.e. the additional
  premium bears only the management charge, not the acquisition charge.
- **Interest accrues by day from the payment date** (「납입일부터 일자계산을 하여」) [S1] [S2],
  not from the policy anniversary. A monthly-premium contract therefore earns a partial year's
  interest on each instalment.
- **공시이율 is set monthly and fixed for the calendar month**: 「공시이율은 매월 1일에 회사가
  정한 이율로 하며, 매월 1일부터 당월 마지막 날일까지 1개월간 확정 적용합니다」 [S1] [S2] [S4
  제6조①] [S5] [S6].
- **How it is set.** Verbatim [S4 제6조②]: 「제1항의 공시이율은 이 보험의 사업방법서에서 정하는
  바에 따라 운용자산이익률과 객관적인 외부지표금리를 가중평균하여 산출된 공시기준이율에서 향후
  예상수익 등을 고려한 조정률을 가감하여 결정합니다」. So the chain is **외부지표금리 +
  운용자산이익률 → (weighted average) → 공시기준이율 → (± 조정률) → 공시이율**.
- The two inputs are defined by carriers as: 「객관적인 외부지표금리는 국고채, 회사채,
  통화안정증권 및 양도성예금증서 등을 고려하여 산출」 and 「운용자산이익률은 직전 12개월간의
  운용자산에 대한 투자영업수익과 투자영업비용 등을 고려하여 산출」 [S1]; the non-life carrier
  gives the same list and specifies 「직전 1년간 … 투자영업수익(보험금융수익 제외)과
  투자영업비용(보험금융비용 제외)」 [S8].
- The 조정률 is a discretionary carrier margin. The 사업방법서 that fixes the weights and the
  adjustment is filed with the supervisor and is referred to but not published: 「이에 대한
  보다 자세한 내용은 인터넷홈페이지 상품공시실에서 … 사업방법서를 참조하시기 바랍니다」 [S1]
  [S8]. **The weighting between 외부지표금리 and 운용자산이익률 was not retrieved** —
  보험업감독업무시행세칙 별표 27 is said to carry it, and that could not be read (see the
  fetch-failure list).
- Carriers name their crediting rate by series. Observed names: **「연금저축 공시이율Ⅴ」**
  [S8], **「신공시이율Ⅳ」** [S7], **「신공시이율(무배당 연금저축Ⅳ)」** [S11]. A carrier runs
  several parallel declared rates and assigns each product to one; a rate is not a
  carrier-level constant.
- The rate is published monthly on the carrier's website: 「회사는 … 공시이율 및 산출방법 등을
  매월 회사의 인터넷 홈페이지 등을 통해 공시합니다」 [S4 제6조③].

### 12. Observed 공시이율 levels

| Date | Carrier / product | 공시이율 | Source |
|---|---|---|---|
| 2026-09-01 | DB생명, 연금저축 강력추천 연금보험 | **3.01%** (전월 2.94%) | [S12] |
| 2026-09-01 | DB생명, 연금저축 강력추천 연금보험 ('09.10월 이후계약) | **2.82%** (전월 2.77%) | [S12] |
| 2026-09-01 | DB생명, 연금저축 동부 프리미엄 연금보험 | **2.82%** (전월 2.77%) | [S12] |
| 2026-09-01 | DB생명, 연금저축 동부 웰컴연금보험(1209) | **2.82%** (전월 2.77%) | [S12] |
| 2026-09-01 | DB생명, (무)백년친구 내생애든든연금보험(2601) — *not* 연금저축 | 2.30% | [S12] |
| 2026-01 | ABL생명, 무배당 우리WON인터넷연금저축보험 | **2.40%** | [S1] |
| 2025-12 | ABL생명, 연금저축나이스플랜연금보험2601 | **2.15%** | [S2] |
| 2024-10 | KDB생명, 신공시이율(무배당 연금저축Ⅳ) | 2.3% | [S11] |
| 2016-03 | 삼성생명, 연금저축골드연금보험 B1.4 | 2.98% | [S5] |

- [S5] publishes a **13-month history** on one product, which shows how smoothly the rate
  moves: '15.3 3.55%, '15.4 3.50%, '15.5 3.43%, '15.6 3.39%, '15.7 3.34%, '15.8 3.29%, '15.9
  3.25%, '15.10 3.20%, '15.11 3.13%, '15.12 3.07%, '16.1 3.05%, '16.2 3.02%, '16.3 2.98%. That
  is **57 basis points over twelve months, in steps of 2–7 bp**, never reversing. A declared
  rate is a managed, heavily smoothed series, not a market rate.
- The **spread between vintages within one carrier is material**: DB생명's pre-2009 and
  post-2009 books differ by 19 bp on the same date [S12].
- Current market level for a 연금저축보험 declared rate, September 2026: **roughly 2.1% to
  3.0%**, with older books at the top [S12] [S1] [S2] `[derived]` from the spread above.

### 13. 평균공시이율 — the supervisory average

- Definition: 「평균공시이율은 감독원장이 정하는 바에 따라 산정한 전체 보험회사 공시이율의
  평균으로, 전년도 8월말 기준 직전 12개월간 보험회사 평균공시이율입니다」 [S2]. An older
  document gives the reference date as 전년도 9월말 [S5] — **the reference date moved, and the
  current documents say 8월말** [S2].
- It is defined in 보험업감독규정 제1-2조 제13호, which [S2] cites by number (「감독규정
  제1-2조 제13호에 따른 현재(2026년) 평균공시이율 2.50%」). The regulation's own text was not
  retrieved [R15].
- **Time series** [S14]:

  | Year | 평균공시이율 |
  |---|---|
  | 2026 | **2.50%** |
  | 2025 | 2.75% |
  | 2024 | 2.75% |
  | 2023 | 2.25% |
  | 2022 | 2.25% |
  | 2021 | 2.25% |
  | 2020 | 2.50% |
  | 2019 | 2.50% |
  | 2018 | 2.50% |
  | 2017 | 3.00% |
  | 2016 | 3.50% |

- It is not a crediting rate: it is an **illustration constraint**. Carriers must show the fund
  on the lesser of the 평균공시이율 and their own 공시이율 alongside the two other bases —
  「상기 예시금액은 최저보증이율, 감독규정 제1-2조 제13호에 따른 현재(2026년) 평균공시이율
  2.50%와 공시이율 2.15% 중 작은 값, 2025년 12월 공시이율 2.15%를 기준으로 계산한 금액입니다」
  [S2], and 「생명보험 상품공시 작성지침에 따라 예시합니다」 [S5]. In 2026 the carrier's own
  rate is below the average, so the middle basis collapses onto the third and the illustrations
  Ⅱ and Ⅲ of [S2] are numerically identical.
- The related **표준이율**, the reserving rate, is given in the same disclosure as 3.50% for
  2013-04 to 2014, 3.50% for 2014 and 3.25% for 2015 [S14]. The series **stops at 2015**, which
  is consistent with the standard-reserve regime having been superseded — but no retrieved
  document says so, so treat the discontinuation as `[unverified]` here and settle it in
  `_research/regulatory-actuarial.md`.

### 14. 최저보증이율 — the guaranteed floor

Definition: 「최저보증이율은 운용자산이익률 및 시장금리가 하락하여도 회사에서 보증해드리는
적립이율의 최저한도」 [S1]; 「운용자산이익률 및 시중금리가 하락되더라도 회사에서 보증하는
최저한도의 적용이율을 말합니다」 [S4]. All observed ladders are **compound annual** (연복리 /
연단위 복리) and step **down** with elapsed contract duration.

| Carrier / product | Vintage | Ladder | Source |
|---|---|---|---|
| 교보생명, 교보First연금보험 | (unknown) | **2.0%** < 10년, **1.5%** ≥ 10년 | [S9] |
| 삼성생명, 연금저축골드연금보험 B1.4 | 2016-04 | 1.5% ≤ 10년, 1.0% > 10년 | [S5] |
| 하나생명, (무)행복knowhow연금저축보험 | 2015-10 ~ 2017-10 | 1.5% ≤ 10년, 1.0% > 10년 | [S13] |
| ABL생명, 우리WON / 나이스플랜 | 2026 | 1.25% ≤ 5년, 1.0% 5–10년, **0.5%** > 10년 | [S1] [S2] |
| 하나생명, 하나원큐/세테크/세테크e/하나로 | 2022-01 ~ | 1.25% ≤ 5년, 1.0% 5–10년, 0.5% > 10년 | [S13] |
| 교보라이프플래닛, (무)교보라플 연금저축보험 (유니버셜 / 이체계좌용) | 2025-04 | 1.25% < 5년, 1.00% 5–10년, **0.75%** ≥ 10년 | [S15] |
| 교보라이프플래닛, 교보라이프플래닛(무)b연금저축보험 | 2021-05 | same ladder | [S15] |
| NH농협생명, e-NH연금저축보험 | 2404 | 1.0% ≤ 10년, 0.5% > 10년 | [S6] |
| 우체국, 우체국연금저축보험 | 2504 | 1.0% ≤ 10년, 0.5% > 10년 | [S7] |
| KDB생명, e원금보장 KDB하이브리드 | (current) | 1.0% ≤ 10년, 0.5% > 10년 | [S11] |
| 한화생명, e연금저축보험 | 2024-04 | **1.0% ≤ 3년, 0.75% 3–5년, 0.5% > 5년** | [S4] |
| 현대해상, 다이렉트연금보험 (Hi2504) — 손보 | 2025-09 | 1.25% ≤ 5년, 1.0% 5–10년, **0.3%** > 10년 | [S8] |

- **Observed range**: first-band floor **1.0% to 2.0%**; long-duration floor **0.3% to 1.5%**.
  The modal current shape is **1.25% / 1.0% / 0.5%** at 5 and 10 years.
- The floor is a **hard guarantee on the credited rate, not on the return**: 「공시이율을
  적용하여 적립하는 금액은 공시이율이 0.25%인 경우, 공시이율(0.25%)이 아닌 최저보증이율 … 로
  적립됩니다」 [S4]; 「최저보증이율이 0.3%인 경우 공시이율이 0.1%로 낮아지더라도 적립금은
  공시이율(0.1%)이 아닌 최저보증이율(0.3%)로 적립됩니다」 [S8]. Expenses are still deducted.
- The ladder is a function of **sale date, not of carrier** [S13] — one carrier's shelf carries
  two ladders side by side depending on when each product opened.
- One carrier prices the accumulation with an explicit **보장부분 적용이율** distinct from the
  crediting rate: 「무배당 우리WON인터넷연금저축보험의 보장부분에 적용한 적용이율은 연복리
  2.50%이며, 동 이율은 적립액 및 해약환급금을 보증하는 이율은 아닙니다」 [S1]. Korea Post calls
  the same thing 예정이율 and gives it as **연단위 복리 2.5%** [S7]; Samsung gives 「본 상품의
  계약체결비용 계산시 적용한 이율은 연복리 2.5%입니다」 [S5]. **2.5% is the observed pricing
  rate for the expense and benefit structure across three carriers**, and it is not a
  guarantee.
- **One hybrid design**: a fixed 연복리 **3.5% 확정이율** for the first five contract years,
  then the ordinary declared rate, floored at 1.0%/0.5% [S11]. This is the only retrieved
  departure from a pure declared-rate accumulation.

### 15. Expenses — 계약체결비용, 계약관리비용, 해약공제액

**Full published schedules.** Both are stated as a percentage of the **기본보험료** and
deducted **monthly**.

[S1] ABL 우리WON, basis 남자 30세, 60세 연금개시, 기본보험료 월 300,000원, 20년납:

| 구분 | 목적 | 시기 | 비용 |
|---|---|---|---|
| 보험관계비용 | 계약체결비용 | 매월 | 7년 이내: 기본보험료의 **1.50%** (4,500원) |
| | 계약관리비용 | 매월 | 20년 이내: 기본보험료의 **3.00%** (9,000원); 20년 초과: **0.67%** (2,000원) |
| 연금수령기간 중 비용 | 연금수령기간 중의 관리비용 | 연금수령시 | **연금연액의 0.5%** |
| 해약공제 | 해지에 따른 패널티 | 해지시 | **0 at every duration (0.0%)** |
| 추가납입보험료 | 계약관리비용 | 납입시 | 추가납입보험료의 **2.0%** |

  The same page summarises the total loading as **1년~7년 4.50%, 8년~20년 3.00%, 20년 이후
  0.67%**, and publishes a **모집수수료율 of 0.00% in every year** — a direct-channel product
  that pays no acquisition commission at all [S1].

[S7] 우체국연금저축보험 2504, basis 기본보험료 월 100,000원 (implied by the won amounts
`[derived]`), 남자, 연금개시나이 and term not recovered from the layout:

| 구분 | 목적 | 시기 | 비용 |
|---|---|---|---|
| 보험관계비용 | 계약체결비용 — 판매보수 | 매월 | 10년 이내: 기본보험료의 **1.22%** (1,221원); 10년 초과: **0%** |
| | 계약체결비용 — 유지보수 | 매월 | 7년 이내: 기본보험료의 **1.8%** (1,800원); 7년 초과: **0%** |
| | 계약관리비용 | 매월 | 기본보험료의 **3.0%** (3,000원) |
| 연금수령기간 중 비용 | 관리비용 | 연금수령시 | **연금연액의 0.5%** |
| 해지공제 | | 해지시 | 1년 **₩104,000** (8.7%), 2년 ₩78,000 (3.3%), 3년 ₩52,000 (1.4%), 4년 ₩26,000 (0.5%), 5년 **0**, 이후 0 |
| 추가납입보험료 | 계약관리비용 | 추가납입시 | 추가납입보험료의 **0.8%** |

- **Total first-year loading: 4.50% of premium [S1] and 6.02% [S7]** `[derived]` by addition.
  The market-level rule of thumb the supervisor gives is 「납입보험료 대비 9%」 over a ten-year
  payment term [R12] — a 2015 figure, and above both of the 2026 schedules here.
- The 해약공제비율 in [S7] checks out arithmetically: ₩104,000 ÷ (₩100,000 × 12) = **8.67%**,
  published as 8.7% `[derived]`.
- Note the **direction of the two schedules**: [S1] charges more per month (4.50%) but no
  surrender penalty at all; [S7] charges less per month (6.02% in year 1 but 3.0% from year 8)
  and adds a front-end surrender penalty that runs off over four years. **The choice between a
  level monthly loading and a 미상각신계약비 recovered on surrender is a live design variable
  in this market**, and the product spec must state which one the reference implementation
  adopts.
- 해약공제액 is defined as unamortised acquisition cost: 「신계약을 청약하고 승낙하는 과정에서
  소요되는 비용을 계약체결비용이라 하며, 일정기간 동안 보험료에서 균등하게 공제함. 그러나
  계약을 중도에 해지하게 될 경우, 공제하지 못한 계약체결비용을 한꺼번에 공제하게 되는데 이를
  해약공제액(미상각 신계약비)라 함」 [S8].
- 해약환급금 = 계약자적립액 − 해약공제액 [S8]; 「보험료 계산시 적용한 위험률로 산출한
  계약자적립액에서 해약공제액을 공제한 금액을 해약환급금으로 지급합니다」 [S1].
- **Post-payment maintenance.** After the premium term ends the maintenance charge continues,
  taken from the fund: 「보험료 납입 완료 후에는 월계약해당일에 계약관리비용 중
  유지관련비용(납입후)을 적립액에서 차감합니다」 [S5]; and [S1] prices it at 0.67% of the
  (notional) 기본보험료 per month beyond 20 years.
- Non-life product-level fee rates, as a **누적 연평균 수수료율** on premiums paid, 2026-06
  [S17]: 현대해상 노후사랑보험 0.02%, 롯데손해보험 새실버피아보험 1.2%, 삼성화재 소득공제단체
  1.53%, 메리츠화재 노후생활지킴이보험 1.71%, 한화손해보험 실버드림보험 1.85%. These are
  **cumulative-average** figures on legacy closed books and are not comparable with the
  first-year loadings above.

### 16. 표준해약공제액 — the statutory cap on the surrender charge

**Verbatim, 보험업감독규정 [별표 14] (제7-66조 관련)** [R14]:

> 표준해약공제액 = **연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의
> 10/1000**

with the notes that matter here:

> 2. 해약공제계수는 다음과 같이 적용함 — 보장성보험: 보험기간(최대 **20년**); **저축성보험:
> 보험료납입기간(최대 12년)**. 명칭을 불문하고 납입기간의 범위 내에서 의무적으로 납입해야
> 하는 별도의 기간을 설정한 경우에는 당해 별도의 납입기간을 보험료납입기간으로 함. 다만,
> 일시납보험의 경우 납입기간을 1년으로 함
>
> 3. … **저축성보험: 납입기간(최대 10년) 동안 동일하게 배분한 평균식 부가보험료를 제외한
> 연간순보험료**
>
> 4. 보험기간이 종신인 **생존연금보험(연금저축보험은 제외)** 표준해약공제액의 경우에는
> 연납순보험료의 **6%**를 적용하되, 연납순보험료의 5%와 해약공제계수 12년을 적용하여 산출한
> 해약공제액을 초과할 수 없음.
>
> 5. **연금저축보험 표준해약공제액의 경우에는 연납순보험료의 4%(무배당 연금저축보험은
> 3%)를 적용함** <신설 2014.12.31>
>
> 6. 보험계약 체결에 사용할 금액을 보험료 납입기간 동안 보험료에 부가하는 저축성보험의
> 경우에는 보험료에 부가된 금액을 평균공시이율로 할인하여 표준해약공제액에서 차감하여 적용함

- **연금저축보험 has its own coefficient, and a lower one.** The general savings rate is 5%; a
  participating 연금저축보험 gets 4% and a **non-participating (무배당) 연금저축보험 gets 3%**
  — note 5, inserted 2014-12-31. The 6% concession for a whole-of-life survival annuity in note
  4 is expressly **denied to 연금저축보험**.
- **Cap for a 무배당 연금저축보험 on a 20-year premium term** `[derived]`: 3% × min(20, 12) =
  **36% of one year's 연납순보험료**. For a participating one, 4% × 12 = **48%**.
- Against that cap, the two observed charges are far inside it: [S1] charges **nothing**, and
  [S7]'s first-year ₩104,000 on a ₩1,200,000 annual premium is **8.7% of the annual gross
  premium** — under a quarter of the cap even before the 연납순보험료 (rather than gross) basis
  and note 6's deduction are applied `[derived]`. The 연납순보험료 is not published, so the
  exact headroom cannot be computed.
- **Note 6 matters for the model**: where the acquisition cost is loaded into the premium
  across the payment term (which is exactly what [S1] and [S7] both do — a level monthly
  계약체결비용 rather than a front-end one), that loaded amount, **discounted at the
  평균공시이율**, is subtracted from the standard deduction. A product that recovers its
  acquisition cost through a level monthly charge therefore has very little standard deduction
  left to draw on — which is a coherent explanation for [S1]'s zero 해약공제표.
- The 별표's own amendment history is 2011-01-24, 2015-05-07 and 2020-01-15, with note 5
  inserted 2014-12-31 and notes 1/3/6/7 touched in 2020 [R14]. The copy retrieved carries a
  법제처 stamp of 2024-02-01; **no later amendment was located, and none was ruled out.**

### 17. 해약환급금 — the published illustrations

**[S1]** ABL 우리WON — 주계약 월보험료 300,000원, 남자 30세, 60세 연금개시, 20년납. Under
최저보증이율 (1.25 / 1.0 / 0.5) and under 공시이율 2.40% (2026년 1월); on this product
해약환급금 equals 적립액 at every duration because 해약공제 is zero [S1]:

| 경과기간 | 납입보험료 | 최저보증: 해약환급금 | 환급률 | 2.40%: 해약환급금 | 환급률 |
|---|---|---|---|---|---|
| 3개월 | 900,000 | 861,291 | 95.7% | 862,938 | 95.9% |
| 6개월 | 1,800,000 | 1,725,267 | 95.8% | 1,731,033 | 96.2% |
| 9개월 | 2,700,000 | 2,591,930 | 96.0% | 2,604,285 | 96.5% |
| 1년 | 3,600,000 | 3,461,278 | 96.1% | 3,482,694 | 96.7% |
| 2년 | 7,200,000 | 6,965,822 | 96.7% | 7,048,973 | 97.9% |
| 3년 | 10,800,000 | 10,514,173 | 97.4% | 10,700,842 | 99.1% |
| 4년 | 14,400,000 | 14,106,878 | 98.0% | 14,440,356 | **100.3%** |
| 5년 | 18,000,000 | 17,744,493 | 98.6% | 18,269,619 | 101.5% |
| 6년 | 21,600,000 | 21,378,560 | 99.0% | 22,190,784 | 102.7% |
| 7년 | 25,200,000 | 25,048,968 | 99.4% | 26,206,056 | 104.0% |
| 8년 | 28,800,000 | 28,810,373 | 100.0% | 30,372,398 | 105.5% |
| 9년 | 32,400,000 | 32,609,391 | 100.6% | 34,638,731 | 106.9% |
| 10년 | 36,000,000 | 36,446,400 | 101.2% | 39,007,457 | 108.4% |
| 15년 | 54,000,000 | 55,049,956 | 101.9% | 62,475,068 | 115.7% |
| 20년 | 72,000,000 | 74,123,274 | 102.9% | 88,897,250 | 123.5% |

- **Break-even is at 4 years on the declared-rate basis and 8 years on the guaranteed-rate
  basis** `[derived]` from the table. On a product with no surrender charge and a 4.50% monthly
  loading, that is the shape to expect.

**[S2]** ABL 나이스플랜 — 남자 40세, 기본보험료 월 500,000원, 20년납, 60세 완납, 65세 개시.
Under 최저보증이율, under min(평균공시이율 2.50%, 공시이율 2.15%), and under 공시이율 2.15%
(the second and third columns coincide in 2026, since 2.15% < 2.50%):

| 경과기간 | 납입보험료 | 2.15%: 해약환급금 | 환급률 | 최저보증: 해약환급금 | 환급률 |
|---|---|---|---|---|---|
| 3개월 | 1,500,000 | 651,477 | **43.4%** | 649,394 | 43.3% |
| 6개월 | 3,000,000 | 2,080,420 | 69.3% | 2,073,128 | 69.1% |
| 9개월 | 4,500,000 | 3,516,829 | 78.2% | 3,501,203 | 77.8% |
| 1년 | 6,000,000 | 4,960,704 | 82.7% | 4,933,619 | 82.2% |
| 3년 | 18,000,000 | 16,787,246 | 93.3% | 16,551,491 | 92.0% |
| 5년 | 30,000,000 | 29,118,235 | 97.1% | 28,456,091 | 94.9% |
| 10년 | 60,000,000 | 62,220,046 | 103.7% | 58,880,326 | 98.1% |
| 15년 | 90,000,000 | 99,427,916 | 110.5% | 89,353,054 | 99.3% |
| 20년 | 120,000,000 | 140,811,363 | **117.3%** | 120,595,257 | **100.5%** |

- **This is a materially different early-duration shape from [S1]** — 43.4% at three months
  against 95.9% — on a product from the *same carrier* in the *same year*. The tied-channel
  participating product carries a real front-end acquisition charge; the direct-channel
  non-participating one does not. Its fee schedule was not published in the leaflet, so the
  charge cannot be decomposed, but the surrender pattern is unambiguous.
- Break-even on the declared-rate basis is between 5 and 10 years; on the guaranteed basis the
  contract never reaches 100% before the end of the premium term, arriving at 100.5% at 20
  years — which is essentially the **100.1%-of-premiums floor** doing the work [S2].

**[S5]** 삼성생명 골드연금 B1.4 — 여자 40세, 전기납 월 334,000원, 60세 연금지급개시, 공시이율
2.98% (2016-03), 최저보증 1.5%/1.0%. Columns: 해약환급금, 환급률, and 세후지급 예상액:

| 경과 | 납입보험료 | 최저보증 환급금 | 환급률 | 세후 | 2.98% 환급금 | 환급률 | 세후 |
|---|---|---|---|---|---|---|---|
| 1년 | 4,008,000 | 3,670,920 | 91.5% | 3,066,530 | 3,701,180 | 92.3% | 3,091,800 |
| 3년 | 12,024,000 | 11,498,820 | 95.6% | 9,605,480 | 11,763,830 | 97.8% | 9,826,750 |
| 5년 | 20,040,000 | 19,561,980 | 97.6% | 16,340,850 | 20,311,460 | 101.3% | 16,966,670 |
| 7년 | 28,056,000 | 27,867,480 | 99.3% | 23,278,580 | 29,373,400 | 104.6% | 24,536,030 |
| 10년 | 40,080,000 | 40,911,060 | 102.0% | 34,173,930 | 44,118,220 | 110.0% | 36,851,920 |
| 15년 | 60,120,000 | 62,752,210 | 104.3% | 52,417,890 | 71,866,780 | 119.5% | 60,028,560 |
| 20년 | 80,160,000 | 85,707,470 | 106.9% | 71,592,140 | 104,003,740 | 129.7% | 86,869,520 |

- The **세후 column is uniformly 83.5% of the 해약환급금 column** at every duration and on both
  bases `[derived]`: 86,869,520 / 104,003,740 = 0.8352; 3,091,800 / 3,701,180 = 0.8353. That is
  exactly 1 − 16.5%, confirming that on a contract whose contributions were all within the
  credit cap the 기타소득세 falls on the whole surrender value.

**[S7]** 우체국연금저축보험 2504 — 20년납, two premium sizes:

| 경과기간 | 납입보험료 (월 10만원) | 해약환급금 | 납입보험료 (월 20만원) | 해약환급금 |
|---|---|---|---|---|
| 1년 | 1,200,000 | 1,038,710 | 2,400,000 | 2,089,570 |
| 3년 | 3,600,000 | 3,460,800 | 7,200,000 | 6,958,990 |
| 5년 | 6,000,000 | 6,000,450 | 12,000,000 | 12,064,760 |
| 7년 | 8,400,000 | 8,611,490 | 16,800,000 | 17,314,630 |
| 10년 | 12,000,000 | 12,840,160 | 24,000,000 | 25,816,240 |
| 15년 | 18,000,000 | 20,685,430 | 36,000,000 | 41,588,120 |
| 20년 | 24,000,000 | 29,540,010 | 48,000,000 | 59,389,070 |

- 1년 환급률 **86.6%**, 5년 **100.0%**, 20년 **123.1%** on the smaller premium `[derived]`. The
  gap between the two premium sizes at year 1 (86.6% against 87.1%) is the **fixed component of
  the charge structure** showing through `[derived]`.

### 18. The 연금개시시점 minimum guarantee

Three of the retrieved contracts guarantee a **floor on the fund at annuitisation**, and the
floor is stated as a fraction of premiums paid, not as a rate:

- **100.1% of premiums paid** — 「연금개시시의 계약자적립액은 이미 납입한 보험료의 100.1%를
  최저보증 합니다」 [S4 별표1 주10]; 「본 상품은 연금개시시점까지 유지시 최저보증금액이 설정된
  상품입니다. … 연금개시시점의 계약자적립액은 이미 납입한 보험료의 100.1%를 최저 한도로
  합니다」 [S2]; 「연금지급개시일의 적립금액(계약자배당준비금 포함)이 이미 납입한 보험료 이하일
  경우 … 이미 납입한 보험료의 100.1%로 합니다」 [S7].
- **이미 납입한 보험료 + ₩1,000** — a functionally identical formulation: 「연금지급개시시의
  적립액이 「이미 납입한 보험료 + 1,000원」 이하일 경우 연금지급개시시의 적립액은 「이미 납입한
  보험료 + 1,000원」으로 합니다」 [S5]; 「연금지급개시 시점의 계약자적립액이 "이미 납입한
  보험료 + 1,000원" 이하일 경우 …」 [S6 별표1 주4].
- **The guarantee is disapplied, and the annuity date deferred instead**, where the shortfall
  is caused by a payment holiday or by a one-instalment reinstatement [S4] [S6] [S7]. Verbatim
  [S4]: 「다만, 다음 각각의 경우에는 연금개시시의 계약자적립액을 이미 납입한 보험료의 100.1%로
  최저보증 하지 않고 연금개시시점이 추가로 연기될 수 있습니다」.
- Why 100.1% and not 100%: 보험업감독규정 제1-2조's 저축성보험 definition requires the survival
  benefits to **exceed** premiums paid, so a nominal one-tenth of one per cent discharges the
  definition. Two carriers make the link explicit — 「보험업감독규정 제1-2조 (정의) 제4조의
  저축성 보험 요건을 충족하기 위해 연금개시시점이 추가로 연기될 수 있습니다」 [S8], 「저축성
  보험 요건(생존시 지급되는 보험금의 합계액이 이미 납입한 보험료를 초과)을 충족하기 위해
  연금개시시점이 추가로 연기될 수 있습니다」 [S7].
- **Modelling consequence.** This is a genuine, if shallow, guarantee on the accumulation:
  under the 최저보증이율 basis [S2]'s illustration reaches only 100.5% of premiums at the end
  of the payment term, so the 100.1% floor is close to binding on a low-rate scenario. It is a
  maturity guarantee of a form absent from the other savings products in this repository and
  belongs in the model.

### 19. Annuitisation — the forms on offer

| Carrier | 종신연금형 보증지급기간 | 확정(기간)연금형 | Other | Source |
|---|---|---|---|---|
| ABL생명 (both products) | 10년, 20년 | 10 / 15 / 20년 | — | [S1] [S2] |
| 한화생명 | 10년, 20년, **100세** | 10 / 15 / 20년 | proportional split, ratio set before annuitisation | [S4] |
| 삼성생명 (2016) | 10회, 20회 (leaflet illustrates 30회 and 100세 too) | 5 / 10 / 15 / 20 / 30년 | — | [S5] |
| NH농협생명 | 10년, 20년, **30년** | 10 / 15 / 20 / 25 / 30년 | **자유설계연금형** — split in 10% units summing to 100% | [S6] |
| 우체국 | **20년만** | 10 / 15 / 20년 | — | [S7] |
| 교보생명 | 10년(10회), 20년(20회), 30년(30회), 100세 | 5 / 10 / 15 / 20 / 25 / 30년 | — | [S9] |
| KDB생명 | 10 / 20 / 30년 / 100세 | 10 / 15 / 20 / 25 / 30년 | 종신연금형 is the default form | [S11] |
| 현대해상 (손보) | **none** | 정액형, 연금지급기간 **5년 ~ 25년** | — | [S8] |

- **상속연금형 is absent from every retrieved 연금저축보험.** It appears only in the variable
  annuity taxonomy [S10] and in general market descriptions. The reason is structural: an
  inheritance annuity pays interest only and returns the fund on death, which is a form of 하락
  없는 원금 유지 that sits badly with the 연금수령한도 test. **Treat "상속연금형 is available
  on 연금저축보험" as `[unverified]` and, on this evidence, probably false.**
- **"100세 보증" is not a century**: 「종신연금형의 경우 100세 보증은 피보험자 나이를 기준으로
  합니다」 [S4 별표1 주8], and more precisely 「종신연금형의 보증지급기간 중 "100세"란 "101세
  계약해당일의 전일까지"를 말합니다. 즉, "100세 보증형"이란 "101세-연금개시나이"년
  보증형입니다」 [S10]. For a 65-year-old that is a **36-year guarantee**.
- **Splitting the fund** across forms is available on three carriers: 「계약자가 두 가지의
  연금지급형태를 원할 경우 회사가 정한 방법에 따라 연금지급형태의 구성비율을 결정하여야
  합니다」 [S4 별표1 주7] [S2]; and NH's 자유설계연금형 with 「연금분할비율은 10%단위로 선택이
  가능하며, 연금분할비율의 합은 100%가 되어야 합니다」 [S6 제19조⑤].
- **When the election is made** differs by carrier and is a real design variable:
  - form is set **at issue** and may be changed up to the day before annuitisation [S6 제16조,
    제19조④] [S11] [S10 주9];
  - form is set **at issue as 종신연금형 only**, with a change to 확정기간연금형 permitted at
    the annuity start date — 「최초 가입시 종신연금형으로 가입 가능하고, 연금지급개시 전일
    (또는 최초 연금수령시점)에 확정기간연금형으로 변경 가능합니다」, and 「가입시에는
    종신연금형만 선택 가능. 이후 연금지급개시시에 연금형태 변경 가능(단, 연금지급개시전에는
    변경불가)」 [S5] — the two statements on the same leaflet are in tension about *when* the
    change may be made, and neither is a 약관;
  - form may be changed **only once the premiums are fully paid** — 「계약자는 보험료납입이
    완료된 계약에 한하여 연금개시전에 연금지급형태를 변경할 수 있습니다」 [S2];
  - the annuity age itself is elected up to the day before — 「계약자는 연금개시일 전일까지
    연단위 계약해당일로 연금지급 개시시점을 선택하여야 하며」 [S2] [S8 제3조④].
- **Instalment frequency.** The 연금연액 may be taken 매월 / 매3개월 / 매6개월, with the
  deferred instalments credited with interest at the 공시이율 — 「이 경우 나중에 지급할 금액에
  대하여는 공시이율로 계산한 금액을 더하여 지급하여, 공시이율이 변동되면 분할 연금액도
  변동됩니다」 [S6 별표1 주9] [S1] [S2] [S5] [S7].
- **Death in the guarantee / certain period.** For 종신연금형, unpaid guaranteed instalments
  are paid on death, with the caveat that they may total less than the fund: 「보증지급기간
  동안 지급된 연금총액은 "연금개시시점의 계약자적립액" 보다 적을 수 있습니다」 [S1] [S2];
  「보증지급횟수까지 지급된 연금액의 총합계는 이미 납입한 보험료보다 적을 수 있습니다」 [S6].
  For 확정연금형 the remaining instalments are paid to the count (10회 / 15회 / 20회) [S1] [S2]
  [S4] [S6].
- The unpaid instalments may be **commuted**: 「보증지급기간(확정된 연금지급기간)안에
  피보험자가 사망할 때에는 … 지급되지 않은 연금액을 회사의 승낙을 얻어 … 공시이율로 할인하여
  계산한 금액을 일시에 지급할 수 있습니다」 [S2], and on one contract the annuitant may commute
  prospectively — 「보증지급기간 … 까지 지급되지 않은 연금액을 … 공시이율로 할인하여 선지급할
  수 있습니다」 [S10 주7].
- **No surrender after annuitisation on 종신연금형** (§6). 확정기간연금형 remains surrenderable
  on some contracts and not on others; [S4]'s pre-contract disclosure says flatly 「다만,
  연금지급이 개시된 이후에는 이 계약을 해지할 수 없습니다」 for the product as a whole.

### 20. 연금사망률 and the 경험생명표 — vintage, ratchet, and published rates

**What the annuity factor uses.** Every retrieved life-insurer contract computes the annuity
from the fund at annuitisation using **two** bases — an annuitant mortality table and the
declared rate:

> 종신연금형(정액형) … 연금개시시점의 계약자적립액을 기준으로 **연금사망률 및 공시이율**을
> 적용하여 산출방법서에 따라 나누어 계산 후 공시이율의 변동을 반영한 연금연액 [S1] [S2]

> 종신연금 … 연금지급개시 시점의 계약자적립액을 기준으로 산출방법서에 정한 바에 따라
> **연금사망률과 공시이율**을 적용하여 나누어 계산한 연금액을 지급 [S6]

The 확정(기간)연금형 uses **only** the declared rate — 「연금개시시점의 계약자적립액을 기준으로
**공시이율**을 적용하여 산출방법서에 따라 계약자가 선택한 확정된 연금지급기간 동안 나누어
계산」 [S1] [S2] [S6]. **Mortality enters only the life-annuity form.** A market commentary
puts the same point generally: 「연금보험의 경우 경험생명표는 종신연금형과 확정연금형,
상속연금형 중 종신연금형에서만 적용합니다」 `[unverified]` — a search snippet; the source page
timed out (R25).

**What the table is called.** Carriers name it differently, and the naming is informative:
- 「연금사망률」 [S1] [S2] [S6 별표1] [S4 별표1 주11]
- 「무배당 경험 개인연금사망률」 [S6 별표1 주10]
- 「경험 연금사망률」 [S5]
- 「연금생명표」 [S9 별표2 주9] [S10 주4]
- 「예정 개인연금 생존·사망률」 [S10 별표]
- 「개인연금사망률」 [S7]
The industry reference table 보험개발원 files under 보험업법 제176조 is one of the 사망률 in
its 참조순보험요율 alongside the 경험생명표 and the 재해사망률 `[unverified]` — this taxonomy
comes from a secondary page that returned 404 on retry; the statutory office of the
보험요율산출기관 is verified at [R16].

**Whether it is fixed at 가입시점 or at 연금개시시점 — the material question.** Six
independently retrieved life contracts carry the **same clause**. Verbatim from the most
recent of them:

> 종신연금형의 경우 연금개시전에 **연금사망률의 개정 등에 따라 연금연액이 증가하게 되는
> 경우** 연금개시시점의 연금사망률 및 계약자적립액을 기준으로 산출방법서에 따라 계산한
> 연금연액을 지급합니다. [S1 주6] [S2]

> 종신연금형 … 의 경우 연금개시 당시 회사의 **무배당 경험 개인연금사망률의 개정** 등에 따라
> 연금액이 증가하게 되는 경우 연금개시 당시의 무배당 경험 개인연금사망률 및 계약자적립액을
> 기준으로 산출한 연금액을 지급합니다. [S6 별표1 주10]

The other four say the same thing with the carrier's own name for the table substituted:
「연금사망률」 [S4 별표1 주11], 「경험 연금사망률」 [S5], 「연금생명표」 [S9 별표2 주9], and —
on a variable annuity, machinery only — 「연금생명표」 [S10 주4]. All six share the same two
operative elements: the trigger is a revision that **increases** the annuity, and the
substituted basis is the table **연금개시 당시**.

**Reading.** The clause is a **one-way ratchet in the policyholder's favour**. The base annuity
factor is the one in the 산출방법서 filed for the product — i.e. the annuitant mortality **as
at issue**, which is why [S1] and [S7] publish the 연금사망률 in the product summary handed
over at inception. If the table is revised before annuitisation and the revision would
*increase* the annuity, the at-annuitisation table is used instead. Since successive 경험생명표
revisions have lightened mortality (§below), a revision normally *decreases* the annuity, the
ratchet does not bite, and the annuitant keeps the issue-date factor. **So the practical answer
is: fixed at 가입시점, with an option to the 연금개시시점 basis if that is better.**

This reading is **an inference from the clause plus the direction of past revisions**, not a
statement any retrieved document makes. Mark it `[derived]`. What is fully sourced is: the
clause itself; that the 산출방법서 basis is disclosed at issue [S1] [S7]; and that a table
revision applies to **new business only** — 「개정된 생명표는 신규 가입자에만 적용되며,
기가입자는 보험료 변동 영향을 받지 않음」 [R18], 「기존 가입자는 가입 당시 경험생명표를
바탕으로 이미 보험료가 결정돼 있어 영향을 받지 않는다」 [R20]. **Note that R18 and R20 speak
about the premium, not about the annuity factor**, so they corroborate the reading without
settling it.

**The 경험생명표 itself.**
- Produced by 보험개발원 under its 보험요율산출기관 office [R16], revised on roughly a
  five-year cycle. The current edition is the **제10회**, applied from **2024년 4월** [R18]
  [R19] [R20].
- 평균수명 on the 제10회: **남자 86.3세, 여자 90.7세**, up **2.8세 and 2.2세** on the 제9회
  [R18] [R19]. Female life expectancy passed 90 for the first time [R18].
- Effect on annuities, on a fixed ₩200,000,000 fund annuitising at 60 [R19]:

  | 경험생명표 | 수령 종료 연령 | 수령 기간 | 월 수령액 |
  |---|---|---|---|
  | 6차 | 78.4세 | 18.4년 | 90.6만원 |
  | 9차 | 85.3세 | — | 70.9만원 |
  | 10차 | 86.3세 | 26.3년 | "60만원 후반" |

  From 9차 to 10차 that is a fall of roughly **15%** in the monthly annuity [R19 headline].
- Effect on other lines [R18] [R20]: 종신보험 premiums down (about 5%; the 2019 revision cut
  them 3.8% on average), 정기보험 down, 암·건강보험 up (about 10%).
- **The full 제10회 table is not published.** No qx-by-age table was located in this session:
  the KIDI press-release page is JavaScript-driven and the release itself could not be opened
  [R17], and the KIDI big-data portal refused connections [R24]. This confirms the house
  position stated in the brief: **every `mort_table.csv` in krlib is a `[std]` construction**,
  anchored on what *is* public — the summary life expectancies above and the carrier-published
  annuitant rates below.

**Published 연금사망률 — the anchor points.** Two carriers publish actual rates in their
statutory product summaries. These are the only annuitant-mortality numbers retrieved in this
session and are the anchors the `[std]` table must reproduce.

[S1] ABL생명 — 적용위험률 「연금사망률」, tabulated by **연금지급개시나이**, 「※ 가입연령 40세
기준」:

| 연금지급개시나이 | 남자 | 여자 | M/F ratio |
|---|---|---|---|
| 50세 | 0.00094 | 0.00044 | 2.14 |
| 60세 | 0.00150 | 0.00052 | 2.88 |
| 70세 | 0.00291 | 0.00097 | 3.00 |

[S7] 우체국 — 예정위험률 「개인연금사망률」, 「기준 40세 가입」:

| 나이 | 남자 | 여자 | M/F ratio |
|---|---|---|---|
| 40세 | 0.00077 | 0.00048 | 1.60 |
| 60세 | 0.00164 | 0.00056 | 2.93 |
| 80세 | 0.01346 | 0.00622 | 2.16 |

- The two carriers agree closely where they overlap: at 60, **0.00150 vs 0.00164 for men (ratio
  1.09) and 0.00052 vs 0.00056 for women (ratio 1.08)** `[derived]`. Two carriers independently
  disclosing annuitant mortality within 9% of each other is strong evidence that both are the
  보험개발원 참조 개인연금사망률 with different safety margins.
- Implied mortality improvement across the age range in [S7]: q80/q60 = **8.21 for men and 11.1
  for women** `[derived]`, i.e. an ageing gradient of about **11.1% p.a. for men and 12.8% p.a.
  for women** over ages 60–80 on a constant-force fit `[derived]`.
- **These rates are extremely light.** A male annuitant rate of 0.00164 at exactly age 60 and
  0.01346 at 80 is far below any plausible Korean population level, which is what one expects
  from a table loaded on the *survival* side for a longevity product. `mort_table.csv` for
  `Pension_KR_S` must be built on the annuitant basis, not the assurance basis, and the two
  cannot be shared with `WholeLife_KR_S`.

### 21. Derived annuity factors — reading the basis off the illustrations

[S2] gives, on one model point (남자 40세, 월 500,000원, 20년납, 연금개시 65세), the fund at
annuitisation and the annuity under five forms on two interest bases. Dividing gives the factor
the insurer actually used. All figures below are `[derived]` from [S2].

**Basis: 공시이율 2.15%. 연금개시시점 fund ₩156,420,000 (15,642만원).**

| Form | Published annuity | Annualised | Implied factor (fund ÷ annual) |
|---|---|---|---|
| 종신연금형 10년보증 | 월 55만원 | 660만원 | **23.70** |
| 종신연금형 20년보증 | 월 54만원 | 648만원 | **24.14** |
| 확정연금형 10년 | 월 143만원 (총 17,263만원) | 1,726.3만원 | **9.06** |
| 확정연금형 15년 | 월 100만원 (총 18,164만원) | 1,210.9만원 | **12.92** |
| 확정연금형 20년 | 월 79만원 (총 19,093만원) | 954.7만원 | **16.39** |

**Basis: 최저보증이율 (0.5% at these durations). 연금개시시점 fund ₩123,460,000.**

| Form | Published annuity | Annualised | Implied factor |
|---|---|---|---|
| 종신연금형 10년보증 | 월 33만원 | 396만원 | **31.18** |
| 종신연금형 20년보증 | 월 32만원 | 384만원 | **32.15** |
| 확정연금형 10년 | 월 104만원 (총 12,590만원) | 1,259.0만원 | **9.81** |
| 확정연금형 15년 | 월 70만원 (총 12,747만원) | 849.8만원 | **14.53** |
| 확정연금형 20년 | 월 53만원 (총 12,904만원) | 645.2만원 | **19.13** |

**Checks against textbook annuity-due factors** `[derived]`:

| n | ä(n) at 2.15% | Implied factor | Ratio |
|---|---|---|---|
| 10 | 9.104 | 9.06 | 0.995 |
| 15 | 12.978 | 12.92 | 0.995 |
| 20 | 16.464 | 16.39 | 0.995 |

The ratio is **0.995 at all three terms**, which is precisely the **연금수령기간 중의 관리비용
of 연금연액의 0.5%** disclosed by the same carrier on its other product [S1] and by Korea Post
[S7]. So, for the 확정기간연금형:

```
annual annuity  =  계약자적립액  ÷  ä_n(공시이율)  ×  (1 − 0.005)
```

is an exact reconstruction of the published figures to three significant digits. **This is
directly implementable and should be the payout-phase formula in the model.**

At the 최저보증이율 basis the same check gives ä(10) at 0.5% = 9.779 against an implied 9.806
(ratio 1.003), ä(15) = 14.492 against 14.528 (1.002), and ä(20) = 19.082 against 19.135 (1.003)
`[derived]`. The ratio is again uniform, but it runs the **other way** — a small uplift rather
than the 0.5% charge. The 0.5% deduction therefore cannot be recovered from this basis, and the
difference between the two constants (0.995 against 1.003) is unexplained by anything
published. Do not over-read it.

**Accumulation cross-check** `[derived]`. Rolling the year-20 surrender value forward the five
years from 60 to 65 at the stated rate reproduces the fund at annuitisation:
- 2.15% basis: ₩140,811,363 × 1.0215⁵ = ₩156,600,000, against the published ₩156,420,000 — a
  residual of ₩180,000, of the order of five years of a post-payment maintenance charge at the
  0.67%-of-기본보험료-per-month rate [S1] discloses (0.67% × ₩500,000 × 60 = ₩201,000).
- 최저보증 basis: ₩120,595,257 × 1.005⁵ = ₩123,640,000 against ₩123,460,000 — the same
  residual.
**The accumulation is a plain daily-accrual roll-forward at the declared rate, net of a small
level maintenance charge, with no other moving parts.**

**Implied longevity of the annuitant basis** `[derived]`. Solving ä_n = 23.70 at 2.15% gives
**n ≈ 32.5 years**, i.e. a 65-year-old male's life annuity is priced like a certain annuity
running to about **age 97**. On the 최저보증 basis, ä_n = 31.18 at 0.5% gives n ≈ 33.8, i.e. to
about age 99. This is consistent with the very light published 연금사망률 of §20 and is the
sanity check any `[std]` annuitant table must pass.

**Second carrier, second model point** [S5], 여자 40세, 전기납 월 334,000원, 60세 개시,
공시이율 2.98%, fund at annuitisation ₩104,000,000:

| Form | Published annuity | Implied factor | ä(n) at 2.98% | Ratio |
|---|---|---|---|---|
| 종신 10회보증 | 457만원 | **22.76** | — | — |
| 종신 20회보증 | 454만원 | 22.91 | — | — |
| 종신 30회보증 | 446만원 | 23.32 | — | — |
| 종신 100세(=40회)보증 | 422만원 | 24.64 | — | — |
| 확정 5년 | 2,193만원 | 4.742 | 4.719 | 1.005 |
| 확정 10년 | 1,176만원 | 8.844 | 8.794 | 1.006 |
| 확정 15년 | 840만원 | 12.381 | 12.311 | 1.006 |
| 확정 20년 | 674만원 | 15.430 | 15.349 | 1.005 |
| 확정 30년 | 511만원 | 20.352 | 20.237 | 1.006 |

- Ratio **1.006 at all five terms** — a uniform *uplift*, not a charge. This carrier's leaflet
  discloses no annuity-phase management charge, and the uplift is consistent with the
  instalment-interest addition on monthly payment [S6 별표1 주9]. **So the annuity-phase charge
  is a carrier choice, not a market convention**, and the product spec must pick one and say
  so.
- The **cost of lengthening the guarantee** on a life annuity is small and readable directly:
  going from a 10-instalment to a 40-instalment guarantee costs **7.7% of the annuity** (457 →
  422만원) for a 60-year-old female `[derived]` from [S5]; going from 10 to 20 years costs
  **1.8%** for a 65-year-old male `[derived]` from [S2]: 660 → 648만원.
- A 65-year-old male's 종신연금형 10년보증 pays **38.2%** of what a 10-year certain annuity
  pays on the same fund (660 vs 1,726만원) `[derived]` from [S2] — the number a policyholder is
  actually choosing between.

### 22. 보험나이 vs 만나이

- The contract's ages are **보험나이** except where the tax statute demands otherwise. Verbatim
  [S6 제20조]:
  > ① 이 약관에서의 피보험자의 나이는 **보험나이**를 기준으로 합니다. 다만, **연금개시나이가
  > 만 55세 이상에 해당되는지 여부의 판단은 실제 만 나이**를 적용합니다.
  > ② 제1항의 보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의
  > 끝수는 버리고 6개월 이상의 끝수는 1년**으로 하여 계산하며, 이후 매년 연계약해당일에
  > 나이가 증가하는 것으로 합니다.
- The 6-month rule means 보험나이 exceeds 만나이 for issue dates in the second half of the age
  year, i.e. for **half of all issue dates**. On a product whose annuity age is a statutory
  threshold this is not a rounding detail: [S1] states the consequence as a product rule —
  「다만, 피보험자가 55세 계약해당일에 만55세 이상이 아닌 경우에는 연금개시나이를 56세부터
  선택할 수 있음」.
- The 연금소득세 age bands of §6 are on the **연금소득자's age**, and the 최소 연금지급기간
  tables are footnoted 「만나이 기준」 [S3]. **Tax ages are 만나이 throughout; pricing ages are
  보험나이.** The model must declare which it uses and, for a product whose annuity date is
  fixed by a statutory age, must be explicit that the two differ.
- 「보험나이 : 계약자 또는 피보험자의 출생일부터 보험계약일까지의 기간을 따진 나이로 보험료
  산정의 기준이 됨」 [S6 약관용어].

### 23. Payment holidays, lapse, reinstatement, and policy loans

- **납입유예 / 납입일시중지** is standard and generous. [S8]: up to **3 times**, each for **1
  year**, during the premium term, with the acquisition and maintenance charges still deducted
  monthly from the fund and the premium due dates and the annuity date deferred by the length
  of the holiday. [S7]: the same shape, available after **3 years** from inception. [S5]:
  available after 3 years.
- The holiday ends prematurely if the fund cannot bear the monthly deduction, at which point
  the ordinary 납입최고 process starts [S7] [S8].
- **Grace and lapse.** 「보험계약자가 제2회 이후 보험료를 납입기일까지 납입하지 않아 보험료
  납입이 연체 중인 경우에 회사는 **14일**(보험기간이 1년 미만인 경우에는 7일) 이상의 기간을
  납입최고(독촉)기간으로 정하여 … 그 때까지 보험료를 납입하지 않을 경우 납입최고(독촉)기간이
  끝나는 날의 다음날 계약이 해지됩니다」 [S2]. Korea Post uses a longer window: 「기본보험료
  납입유예기간은 납입기일부터 납입기일이 속하는 달의 **다음 다음달의 마지막 날**까지」 [S7].
- **Reinstatement (부활/효력회복) within 3 years** of lapse, on payment of the arrears with
  interest at the 공시이율 [S7] [S8]. A **simplified one-instalment reinstatement** is
  available: pay one month's basic premium, and the charges for the lapsed months are taken
  from the fund; if the fund is short, the difference must be paid in [S1] [S5] [S7] [S8]. The
  premium due dates and the annuity date shift by the lapsed period, and where the resulting
  annuity date would fall after the agreed one it is deferred [S5] [S8].
- **Policy loan (보험계약대출)** exists on the product and interacts with the tax rules — the
  medical-withdrawal limit is set 「보험계약대출이 있는 경우, 원금과 이자 상환 및
  연금외수령으로 일시에 인출할 때 기타소득세 원천징수액을 고려하여 회사가 정하는 범위 내로」
  [S2]. The 보험계약대출이율 is used as the interest rate on refunds of premium on a void
  contract [S1]. **No retrieved document gives a numeric 보험계약대출이율** for this product.
- Late-payment interest on benefits is laddered: 보험계약대출이율 for the first 30 days after
  the due date, then **+4.0%**, **+6.0%** and **+8.0%** 가산이율 in the following 30-day bands
  [S4 별표2].
- 청약철회 within **15 days** of receiving the policy (and within 30 days of application) [S2]
  [S5]; 품질보증해지 within **3 months** where the 약관 was not delivered or explained or the
  application was not signed [S2] [S5] [S7]; 사기에 의한 계약 cancellable within **5 years** of
  the cover start (1 month from discovery) [S1] [S7].
- **Contestability**: a 계약전 알릴 의무 breach lets the insurer terminate within **2 years**
  of the cover start (1 year where a medical examination was taken) [S1].
- **No premium waiver.** 「보험료 납입면제 사유 : 없음」 [S5]. One carrier's transfer
  restrictions contemplate a 장해연금 and a 납입면제 on *some* 연금저축 contracts [S1], so the
  feature exists in the market, but it is absent from every retrieved product's own terms.

### 24. 계약자배당

- The market is split between 무배당 and 배당 forms of the same product. [S1] is 무배당 —
  「무배당 우리WON인터넷연금저축보험은 무배당 상품으로서 계약자배당을 하지 않습니다」. [S2],
  from the same carrier, is 배당 — 「이 상품은 배당 보험으로 보험료 산출시 예정률(이율, 위험률,
  계약체결비용 및 계약관리비용율)과 실제 운영결과의 차이에 따른 금액중 일부는 계약자에게 배당해
  주고 있습니다」.
- Where a dividend arises it is applied as an **increase to the annuity or an addition to the
  instalment**: 「보험기간 중 발생한 배당금은 계약소멸할 때 계약자에게 지급하거나 연금 지급개시
  이후에 증액연금으로 수익자에게 지급합니다」 [S2].
- The distinction has a direct regulatory consequence: the 표준해약공제액 coefficient is **4%
  for a participating and 3% for a non-participating 연금저축보험** [R14 주5] (§16).
- Korea Post publishes a **five-year dividend history** with the 기준율 and the aggregate [S7]:

  | | 2020년 | 2021년 | 2022년 | 2023년 | 2024년 |
  |---|---|---|---|---|---|
  | 기준율 | 4.3 | 4.3 | 4.3 | 3.6 | **3.5** |
  | 금액 (억원) | 1,630 | 1,763 | 1,838 | 753 | 549 |

  The 기준율 fell from 4.3 to 3.5 and the amount by **70%** over 2022–2024 `[derived]`.
- 계약자배당 is computed 「「보험업감독규정」 및 「보험업감독업무시행세칙」에서 정하는 방식에
  따라」 [S8]; for Korea Post, 「과학기술정보통신부장관이 정하는 방법에 따라」 [S7] — a
  reminder that Korea Post insurance sits outside 보험업법.

### 25. 예금자보호

- A 연금저축보험 is protected **separately from the carrier's other protected products**, and
  aggregated with the carrier's other protected 연금저축: 「이 연금저축보험계약은
  예금자보호법에 따라 다른 보호상품과는 별도로 1인당 "**1억원** 까지"(본 보험회사의 여타
  보호대상 연금저축과 합산) 보호됩니다」 [S2] [S6] [S11].
- The older documents state the limit as **5천만원** [S4] [S5]. **The increase to ₩100,000,000
  is visible in the 2026-vintage documents and absent from the 2024 ones**; the amending
  legislation and its commencement date were not retrieved [unverified].
- A contract whose policyholder or premium payer is a corporation is **not** protected [S4]
  [S5].
- 연금저축펀드 is **not** covered by 예금자보호 at all; 신탁 and 보험 are [S16] [R12].

### 26. Market size and behaviour

From the supervisor's 2025 whitepaper and its press coverage, as at **end-2025** [R13] [R22]:

| Measure | Value | Change on 2024 |
|---|---|---|
| 적립금 총계 | **198.2조원** (₩198.2tn) | +19.3조원 (+10.8%) |
| — 연금저축보험 | **114.1조원** (57.6%) | −1.2% |
| — 연금저축펀드 | 61.3조원 (30.9%) | +50.7% |
| — 연금저축신탁 | 13.8조원 (6.4%) | −6.4% |
| 가입자 수 | **840.3만명** | +76.1만명 (+10.0%) |
| 계약건수 | 1,079.6만건 | +107.9만건 (+11.1%) |
| 신규 계약건수 | 144.3만건 | +51.9% |
| 납입액 | 13.5조원 | +2.1조원 (+18.1%) |
| 연간 수익률 (전체) | **10.6%** | +6.9%p |
| — 펀드·ETF | 29.3% (펀드 31.3%, ETF 27.4%) | |

By seller [R22]: 보험회사 114.3조원 (57.7%), 금융투자회사 55.4조원 (27.9%), 은행 19.5조원
(9.8%), 공제기관 9.0조원 (4.6%).

- **The insurance wrapper is still the majority of the market by reserves but is shrinking in
  absolute terms** — 114.1조원, down 1.2% on the year, while funds grew 50.7% [R13] [R22]. On a
  ₩198tn market with 8.4m savers, the average balance per saver is **₩23,600,000 (2,360만원)**
  and per contract **₩18,360,000 (1,836만원)** `[derived]`. A fund of that size drawn down over
  the ten years the 연금수령한도 effectively imposes yields well under ₩15,000,000 a year,
  which is why the aggregation threshold of §6 binds on very few savers `[derived]`.
- 연금저축보험's 2025 return was **0.8%** against 29.3% for funds and ETFs `[unverified]` —
  this split appeared in the press summary of [R13] but not in the retrieved press-release body
  nor in [R22].
- The behavioural picture that matters for the model — how many savers annuitise rather than
  surrender, how many choose 종신 rather than 확정, the lapse rate by duration, the average age
  at annuitisation — is **in the whitepaper's attachments, which could not be opened**. See the
  gap list.

### 27. Scope boundaries

- **연금보험 (non-qualified) is a different product** and is not covered here. It sits outside
  the 연금저축 wrapper, gets no 세액공제, and instead enjoys the 보험차익 비과세 of 소득세법
  시행령 제25조 on a contract held 10 years and meeting the payment conditions. No document on
  it was retrieved in this session; it is out of the krlib product set.
- **변액연금보험 is a separate library product** (`VA_KR_S`, `_research/variable-annuity.md`).
  [S10] is cited here only for annuitisation machinery (§19, §20).
- **즉시연금 (single-premium immediate annuity)** is a separate library product
  (`Immediate_KR_S`, `_research/immediate-annuity.md`). Nothing in this file is about the
  payout phase standing alone.
- **IRP (개인형퇴직연금)** shares the ₩9,000,000 credit envelope and the 연금수령 rules, and a
  연금저축 may be transferred into one (§9), but it is a 퇴직연금 product under
  근로자퇴직급여보장법 and is not in the krlib product set.
- **이연퇴직소득** — retirement money rolled into a pension account — changes the five-year
  test and the withholding formula (§5, §6). A 연금저축보험 written as pure individual savings,
  which is the reference implementation, holds none of it, and the reference model does not
  need to carry it.
- **IFRS 17 / K-ICS treatment** of this product — the contract boundary of a monthly-resetting
  declared-rate contract, the CSM, and the 해약환급금준비금 — belongs in
  `_research/regulatory-actuarial.md`. Nothing on it was researched in this session.

---

## Variation across carriers

| Feature | ABL생명 [S1] [S2] [S3] | 한화생명 [S4] | 삼성생명 [S5] | NH농협생명 [S6] | 우체국 [S7] | 교보생명 [S9] | KDB생명 [S11] | 현대해상 (손보) [S8] |
|---|---|---|---|---|---|---|---|---|
| 최저보증이율 | 1.25 / 1.0 / 0.5 at 5, 10 yrs | **1.0 / 0.75 / 0.5 at 3, 5 yrs** | 1.5 / 1.0 at 10 yrs | 1.0 / 0.5 at 10 yrs | 1.0 / 0.5 at 10 yrs | **2.0 / 1.5 at 10 yrs** | 1.0 / 0.5 at 10 yrs | 1.25 / 1.0 / **0.3** at 5, 10 yrs |
| 공시이율 (as retrieved) | 2.40% (2026-01) / 2.15% (2025-12) | not published on retrieved doc | 2.98% (2016-03) | not published | 신공시이율Ⅳ, level not published | not published | 2.3% (2024-10), 3.5% fixed for 5 yrs | 연금저축 공시이율Ⅴ, level not published |
| 배당 | 무배당 [S1] / 배당 [S2] | 무배당 | 무배당 | 무배당 | 배당 (기준율 3.5%, 2024) | not stated | 무배당 | 배당 |
| 종신연금형 보증 | 10, 20년 | 10, 20년, 100세 | 10, 20회 (30회·100세 illustrated) | 10, 20, 30년 | **20년만** | 10, 20, 30년, 100세 | 10, 20, 30년, 100세 | **none** |
| 확정연금형 | 10 / 15 / 20년 | 10 / 15 / 20년 | 5 / 10 / 15 / 20 / 30년 | 10 / 15 / 20 / 25 / 30년 | 10 / 15 / 20년 | 5 / 10 / 15 / 20 / 25 / 30년 | 10 / 15 / 20 / 25 / 30년 | 정액형, 5~25년 |
| Split election | yes, ratio at 연금개시 [S2] | yes, 구성비율 | not stated | **자유설계연금형, 10% units** | not stated | not stated | not stated | n/a |
| Fund floor at 연금개시 | **100.1%** of premiums [S2] | **100.1%** of premiums | 이미 납입한 보험료 + ₩1,000 | 이미 납입한 보험료 + ₩1,000 | **100.1%** of premiums | not stated | not stated | 저축성 요건 by deferral |
| 계약체결비용 | 1.50%/월, 7년 [S1] | not published | not published | not published | 판매 1.22%/월 10년 + 유지 1.8%/월 7년 | not published | not published | not published |
| 계약관리비용 | 3.00%/월 20년, 0.67% 이후 [S1] | not published | not published | not published | 3.0%/월 | not published | not published | not published |
| 해약공제액 | **0 at every duration** [S1] | not published | not published | not published | **₩104,000 → 0 over 5 yrs** | not published | not published | 미상각신계약비, table not extracted |
| 연금수령기간 비용 | 연금연액의 0.5% [S1] | not published | none disclosed | not published | 연금연액의 0.5% | not published | not published | not published |
| 추가납입 비용 | 2.0% of the additional premium [S1] | not published | not published | not published | 0.8% | not published | not published | 계약관리비용 only |
| 모집수수료율 | **0.00% every year** [S1] | not published | not published | not published | not published | not published | not published | not published |
| 예금자보호 | ₩100,000,000 [S2] | ₩50,000,000 (2024 doc) | ₩50,000,000 (2016 doc) | ₩100,000,000 | not extracted | not stated | ₩100,000,000 | not extracted |
| 건강진단 | 인수지침에 따라 | not extracted | not extracted | not extracted | **전건 무진단** | not extracted | not extracted | 인수지침에 따라 |
| Annuity-mortality ratchet | yes | yes | yes | yes | not stated | yes | not extracted | n/a (no life annuity) |

**What does not vary.** Every retrieved life-insurer contract: accumulates 순보험료 at a
monthly-reset 공시이율 with a stepped compound floor; deducts 계약체결비용 and 계약관리비용
monthly as a percentage of the basic premium; pays the fund on death before annuitisation and
nothing more; offers a 종신연금형 with a guarantee period and a 확정(기간)연금형, computing the
first with 연금사망률 and 공시이율 and the second with 공시이율 alone; carries the
annuity-mortality ratchet clause; forbids surrender once a life annuity is in payment; defaults
the annuity to the tax-recognised maximum; and states the 세액공제 / 연금소득세 / 기타소득세
trio in materially the same words. Every one allows 추가납입 up to 200% of basic premium within
the ₩18,000,000 aggregate, a payment holiday, a three-year reinstatement window, and a
simplified one-instalment reinstatement.

**Most representative design for a reference implementation.** A **무배당, level monthly
premium, non-participating 연금저축보험**: 보험나이 40 at issue, 20-year premium term to 60,
annuity from 65 (a five-year deferral gap), 기본보험료 ₩500,000 a month; 계약자적립액
accumulating at a 공시이율 of **2.15%** with a **1.25% / 1.00% / 0.50%** floor at 5 and 10
years; 계약체결비용 **1.50%** of basic premium a month for 7 years and 계약관리비용 **3.00%** a
month for 20 years then **0.67%**; **no 해약공제** (with the 표준해약공제액 cap of 3% × 12 =
36% of 연납순보험료 stated as the binding constraint that is not reached); a
**100.1%-of-premiums floor** on the fund at annuitisation; annuitisation as a **종신연금형 with
a 10-year guarantee** by default, with **확정기간연금형 at 10 / 15 / 20 years** as the
election, the certain form priced as fund ÷ ä_n(공시이율) × 0.995 and the life form on a
`[std]` annuitant table anchored on the §20 rates; a **0.5% of 연금연액** charge in payment;
and the tax layer of §4–§7 applied in full. That design is [S1] and [S2] in combination, which
is why they are the anchor sources.

---

## Fetch failures and gaps

**URLs tried and not opened, or opened and unusable**

- `https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do?MENU_ID1=DF_GDAR000`
  [S21] — HTTP 200, navigation shell only; the 적용이율 table is client-side. **Lost:** the
  carrier's current 공시이율. Substituted by its 약관's guarantee ladder [S4].
- `https://pub.insure.or.kr/` [S20] — HTTP 200, category tree only; every leaf table is
  client-side. **Lost:** the 생명보험협회's cross-carrier 연금 comparison, which the house
  brief names as the best single quantitative source for Korea. Substituted by carrier
  상품요약서 [S1] [S2] [S7] and the non-life association mirror [S17].
- `https://www.fss.or.kr/fss/lifeplan/goodsCmpr/list.do?menuNo=200961` [S19] — returned the
  **'22.2분기** table; the quarter selector is client-side. **Lost:** current per-carrier
  연금저축 reserves and returns from the supervisor's own portal. Not used for any figure.
- `https://kpub.knia.or.kr/productDisc/pensionSaving/pensionSavingCompanyProfit.do` [S18] —
  returned the 판매회사별 적립금 table instead of the 수익률·수수료율 table the URL names. Read
  but not transcribed.
- `https://www.lifeplanet.co.kr/disclosure/good/HPDA45S2.dev` [S15] — the guarantee rows
  returned; the 당월이율 and 경과기간별 중도해지율 tabs did not. **Lost:** a fourth
  current-month 공시이율 observation.
- `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` [R15] — 보험업감독규정,
  HTTP 200, metadata and navigation only (시행 2023-03-02, 금융위원회고시 제2023-10호); article
  bodies are client-side. **Lost:** 제1-2조 (정의, including the 저축성보험 definition and the
  제13호 평균공시이율 definition) and 제7-66조 (표준해약환급금) in their own words. The 별표
  [R14] was obtained by direct file download instead, and the two definitions are known only
  through carrier documents citing them [S2] [S7] [S8].
- `https://www.law.go.kr/행정규칙/보험업감독업무시행세칙` and
  `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687` — 보험업감독업무시행세칙;
  not opened in this session beyond search snippets. **Lost:** 별표 27 「외부지표금리와
  운용자산이익률의 가중치」, which is the numeric specification of the 공시기준이율 weighting.
  **The 공시기준이율 weighting is therefore `[unverified]`** and the model must treat the
  declared rate as an exogenous input, not as a derived one.
- `https://law.go.kr/flDownload.do?flSeq=46939241&...` — an older HWP copy of 별표 14; the
  file downloaded (50 KB, `application/hwp`) but is a WordPerfect-family binary that neither
  the fetcher nor a local parser could read. The current PDF copy [R14] was used instead.
- `https://bigin.kidi.or.kr:9443/boarddetail/nd00017_6041` [R24] — `ECONNREFUSED` on port
  9443. **Lost:** 보험개발원's own 경험생명표 page.
- `https://www.kidi.or.kr/user/nd11592.do` [R17] — list page returned rows 740–746
  (2026-05 to 2026-08) only, and every item is a `javascript:goBoardView(...)` link. **Lost:**
  the 제10회 경험생명표 press release itself. Its content is known only through news reports
  [R18] [R19] [R20].
- `https://www.prudential.co.kr/plan-your-story/content/retirement/retirement-18.aspx` [R25]
  — `getaddrinfo ETIMEOUT`. **Lost:** the most on-point secondary treatment of the
  가입시점-versus-개시시점 question found in this session.
- `https://www.insclaim.co.kr/19/9616822` — HTTP **404** on a page that search results
  described as listing 보험개발원's 참조순보험요율 components (경험생명표, 개인연금사망률,
  재해사망률). **Lost:** confirmation that 개인연금사망률 is a distinct filed 참조위험률.
- `https://www.taxcanvas.kr/core/law/0039562026052236343/history/2026-05-22/articles/0187021`
  and `https://www.nhis.or.kr/lm/lmxsrv/law/joHistoryContent.do?SEQ=393&SEQ_CONTENTS=4454757&...`
  and `https://elaw.klri.re.kr/kor_service/lawViewTitle.do?hseq=42184` [R7] — all three
  returned navigation or title-only. **Lost:** the operative text of 소득세법 시행령 제187조의2
  (종신계약의 범위).
- `https://casenote.kr/법령/소득세법 시행령/제40조의2` — CaseNote does not carry the
  Enforcement Decree under that path and returned the parent Act instead. The provision was
  obtained from 국가법령정보센터's `print=print` article form and the 국민건강보험공단 mirror
  [R6] instead.
- `https://www.law.go.kr/법령/소득세법 시행령/제40조의2` — the friendly law.go.kr URL form
  returns only the page header. **Recorded as a general finding: on `law.go.kr` the friendly
  `/법령/<name>/<article>` form and the `admRulLsInfoP.do` form return chrome; the
  `lsLawLinkInfo.do?...&print=print` article form and direct `flDownload.do` file links return
  text.**
- `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=218674&menuNo=200218` [R13] — the
  press-release body returned but its hwpx and pdf attachments did not. **Lost:** the
  whitepaper's detailed tables, which are where the payout-phase behavioural statistics live.

**Claims left `[unverified]`, and why**

- **The operative definition of 종신계약** (소득세법 시행령 제187조의2). The article's
  existence, number, title and both language versions are verified [R7]; its text is not. The
  국세청 gloss ("사망할 때까지 연금수령 … 중도해지 불가") [R9] is consistent with every
  retrieved 종신연금형 wording, but the precise conditions — in particular whether a guarantee
  period of any length is compatible with 종신계약 status — are not established. **This
  matters**: if a 100세 보증 (36 years for a 65-year-old) disqualifies a contract from the 3.3%
  rate, the annuitisation-election economics change materially. Do not assert the answer.
- **The 15% statutory rate on 연금외수령.** 소득세법 제129조제1항제6호나목 was located but its
  text was not read; the 16.5% grossed-up figure is sourced at contract level from nine
  independent documents and is not in doubt as a matter of practice.
- **The 연금소득공제 ceiling.** The band table is retrieved [S5]; whether 소득세법 제47조의2
  caps the deduction overall was not established.
- **The commencement dates of the 2014 소득공제→세액공제 switch and of the 2025 예금자보호
  increase to ₩100,000,000.** Both changes are visible in the document record (the older and
  newer carrier documents differ), but neither amending instrument was retrieved.
- **The 공시기준이율 weighting** between 외부지표금리 and 운용자산이익률, and the permitted
  range of the 조정률. The construction is verified verbatim [S4 제6조②]; the numbers are in
  the 사업방법서 (not public) and in 보험업감독업무시행세칙 별표 27 (not retrieved).
- **Whether the base annuity factor uses the 가입시점 or the 연금개시시점 mortality.** The
  ratchet clause is verified across six carriers; the reading that the *base* is the issue-date
  table is `[derived]` (§20), supported by the fact that the rates are disclosed at issue [S1]
  [S7] and by the new-business-only statements [R18] [R20], but not stated by any retrieved
  document.
- **The full 제10회 경험생명표.** Not published; not retrieved; not obtainable in this session.
  Every krlib mortality table remains a `[std]` construction with a `provenance` column,
  anchored on the summary life expectancies [R18] [R19] and the six carrier-published annuitant
  rates of §20.
- **상속연금형 on a 연금저축보험.** Absent from all eight retrieved 연금저축보험 documents and
  present only on a variable annuity [S10]. Treat as not offered on this product until a
  contract shows otherwise.
- **Lapse and surrender rates by duration.** No public Korean statistic for 연금저축보험 lapse
  by policy year was found. [S13] shows a 중도해지이율 column on one carrier's disclosure, but
  every row reads 「적용안함」. The 유지율 category exists in the supervisor's comparison
  disclosure [S19] [R12] but the table could not be opened. **The lapse basis in the product
  spec will have to be `[std]`, argued from the 16.5% tax cost of a surrender (§7) and the
  surrender-value shape (§17) rather than from data.**
- **Annuitisation take-up and form mix.** How many savers annuitise rather than take the money
  as a series of scheduled withdrawals, and how many choose 종신 over 확정, is the single most
  important behavioural parameter for this model and **no retrieved source gives it**. The
  whitepaper attachments [R13] are the obvious place and could not be opened.
- **The 보험계약대출이율** on a 연금저축보험. Referenced in four contracts [S1] [S2] [S4] [S5];
  not quantified in any of them.
- **연금저축보험's 2025 return of 0.8%.** Appeared in a press summary of [R13] but not in the
  retrieved press-release body nor in [R22].
- **Whether the 표준이율 series ending at 2015 [S14] reflects the abolition of the
  standard-reserve rate or merely a disclosure that stopped being updated.** Settle this in
  `_research/regulatory-actuarial.md`.
- **The 사업비 / 해약공제 reform of the 2024–2025 보험개혁회의.** Search results describe a
  commission-payment-period extension from 3 to 7 years, a new 유지관리수수료 capped at 0.8% of
  계약체결비용 a year for up to 7 years, and a proposal to shrink the 표준해약공제액; none of
  the underlying 금융위원회 releases was retrieved, and the 별표 14 copy in hand [R14] shows no
  amendment after 2020-01-15. **Any statement that the surrender-charge cap has changed since
  2020 is `[unverified]`.**
