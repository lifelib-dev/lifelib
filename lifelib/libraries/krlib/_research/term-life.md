# 정기보험 (term life) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean 정기보험 (*jeonggi boheom*, level term life) liability cash flow
reference model — the **protection chassis** of `krlib`, on which `ci_insurance` and the
fixed-benefit 제3보험 products state their decrement and premium-recursion deltas.

정기보험 is the simplest contract in the Korean individual life market and, by new-business
count, one of the smallest. It pays a 사망보험금 (death benefit) if the 피보험자 (life assured)
dies inside a stated 보험기간 (policy term) and, on the dominant 순수보장형 (pure protection)
form, pays nothing at all otherwise. Its economic role is to be the cheap alternative to
종신보험 (whole life) — every carrier's own consumer material frames it that way, in the same
words — and its structural role in this library is to isolate the decrement and premium
mechanics that the savings chassis (`WholeLife_KR_S`) then wraps a 계약자적립액 around.

Three things make the Korean version of this product worth a library of its own rather than a
translation of `jplib`'s 定期保険. First, the **무해지환급형 / 저해지환급형** forms — the
no-surrender-value and low-surrender-value designs that now dominate Korean protection sales,
in which the 해약환급금 (surrender value) is nil, or a stated fraction, during the
premium-paying period and steps up at 납입완료. Second, the **갱신형 / 비갱신형** split, in
which a renewable contract reprices at attained age on each renewal date at the rate scale then
in force, with **no fresh 고지 (disclosure) and no new underwriting**, up to a stated maximum
renewal age. Third, and most usefully for a reference model, **Korea publishes its premium
rates**: the 생명보험협회 공시실 (Korea Life Insurance Association disclosure site) carries a
cross-carrier 상품비교공시 for 정기보험 on a single prescribed 대표계약 basis, and every
carrier's 상품요약서 (product summary) discloses its 적용이율 (pricing interest rate), its 예정
경험사망률 (assumed experience mortality) at ages 20/40/60, its 적용해지율 (assumed lapse rate)
where the 무해지 form is sold, and a 해약환급금 예시 (surrender-value illustration) by elapsed
duration. Nothing in `uklib`, `frlib` or `delib` comes close to that level of public
disclosure, and `jplib` only matches it at the direct writers.

**In scope.** The individual, retail, 무배당 (non-participating) level term contract on one
life, written 순수보장형 or 만기환급형 (return-of-premium at maturity), on a 비갱신형 or 갱신형
basis, with a 세만기 (to a stated age) or 년만기 (a fixed number of years) term shape, sold
either 표준형 or 무해지/저해지환급형, with rate classes for 비흡연체 / 건강체 / 슈퍼건강체, the
보험료 납입면제 (waiver of premium) on a 50%-plus 장해 (disability) state, the 재해사망
(accidental death) uplift where a carrier offers it as a product variant, and the 제도성특약
(administrative riders) that ride on every contract — 선지급서비스특약, 지정대리청구서비스특약,
단체취급특약, 장애인전용보험전환특약, 보험료납입유예특약.

**Also covered, because it is a large and genuinely different part of the same 정기보험 product
class:** the **경영인정기보험** (key-person / corporate term), a 90세만기 전기납 contract with
a 10% 체증 (escalating) sum assured from year 10, sums assured to 30억원, and a three-step
해약환급금이 적은 유형 schedule. It is priced and disclosed as 정기보험 and it accounts for
most of the high-premium rows in the disclosure table, so a file that ignored it would misread
the market's price dispersion.

**Out of scope, and said so where it matters.** 단체정기보험 (group term); 신용생명보험 /
대출안심보험 (creditor life, which appears in the disclosure table and is noted only for its
decreasing-cover shape); 변액정기보험; the 정기특약 written as a rider on a 종신보험 (§16); and
every 제3보험 rider — 암, 뇌출혈, 급성심근경색증 진단 riders and 입원·수술 riders — which
belong to `cancer`, `ci_insurance` and `indemnity_medical`.

**What this file is.** It is the provenance layer behind the `term_life` product's four
documents — `product-spec.md`, `technical-notes.md`, `model.md` and `sources.md` — and behind
the `Term_KR_S` model's input CSVs. Source ids **S1..S24** and **R1..R21** below are **frozen
and are never renumbered**: the product documents cite against them, unused ids are simply
omitted downstream leaving gaps, and `sources.md` records which are absent and why.

Access date for every citation: **2026-09-03**.

---

## Retrieval method and citation discipline

Every fact below is tagged `[S#]` (a primary product document) or `[R#]` (a product-specific
regulatory, statutory or statistical reference) pointing at a document actually retrieved and
read during this session, or is tagged `[unverified]` where it is general knowledge or a
search-result snippet that could not be confirmed against a retrieved document. A number that
was invented for the reference implementation is `[std]` and carries a rationale; there are
none in this file, because this file records evidence rather than choices — the `[std]`
parameters live in `product-spec.md` and `technical-notes.md` and are justified against the
observed ranges in **Variation across carriers** below.

**How things were fetched.** Three routes worked and one did not.

1. **Carrier sites and the 생명보험협회 공시실 answered plain `curl`** with a browser
   User-Agent. `pub.insure.or.kr` serves its 상품비교공시 through a POST to
   `/compareDis/prodCompare/assurance/listNew.do` carrying `search_prodGroup=024400010002`
   (정기보험) plus the full checkbox set for carrier, channel, universal flag,
   interest-crediting basis, renewal flag and product feature; the eight result pages were
   fetched that way and the result table parsed out of the raw HTML. The linked 상품요약서 PDFs
   come from `/FileDown.do?fileNo=<n>&seq=<m>`, whose ids are embedded in the row markup as
   `fn_fileDown('<n>','<m>')`.
2. **PDFs were extracted with `pymupdf`.** Every 상품요약서 in this file extracted cleanly as
   Korean text; the 한화생명 190-page 약관 also extracted cleanly. Two documents
   (미래에셋생명's two) extract with a space after almost every syllable block and required
   reflowing before reading; the figures were checked character by character after reflow.
3. **`law.go.kr` needed its open API, not its friendly URLs.**
   `https://www.law.go.kr/법령/<name>` returns only site chrome to a plain fetcher, and the
   same is true of `admRulLsInfoP.do?admRulSeq=...` for 행정규칙.
   `DRF/lawSearch.do?OC=test&target=admrul&...` returns real XML metadata; `DRF/lawService.do`
   with `target=admrul` returned nothing usable for the 행정규칙 detail (see **Fetch failures
   and gaps**). Statute text was therefore taken from **casenote.kr**, which serves article
   text to a plain fetcher, and the one 별표 that mattered came as a direct PDF download from
   `law.go.kr/LSW//flDownload.do`.
4. **Numeric tables were cross-checked against a second source wherever possible.** The
   cross-carrier disclosure table `[S4]` was verified against six carriers' own 상품요약서
   `[S1] [S6] [S8] [S9] [S10] [S11] [S12]`: in every one of those cases the disclosed premium
   reproduces the carrier's own illustration to the won. That agreement is what licenses using
   `[S4]` as the anchor for the model's premium basis.

---

## Primary sources

Fourteen carriers appear below: 한화생명, 삼성생명, 교보라이프플래닛생명, 신한라이프생명,
KB라이프생명, 흥국생명, 미래에셋생명, 푸본현대생명, DB생명, 메트라이프생명, NH농협생명,
교보생명, 처브라이프생명, KDB생명, AIA생명.

### S1 — 「한화생명 e정기보험 무배당 상품요약서」, 한화생명보험(주)

- Publisher: 한화생명보험 주식회사
- Document: 상품요약서, file `한화생명 e정기보험 무배당_상품요약서_20260417.pdf`, 14 PDF pages
- Doc type: 상품요약서 (statutory product summary)
- URL:
  `https://static.hanwhalife.com/dynamic/direct/product/cms_I1gR8ivwtn8cVwbq_1776383286029.pdf`
  (linked from `https://direct.hanwhalife.com/products/CM090101` as
  `/products/downloadProxy/한화생명 e정기보험 무배당_상품요약서_20260417.pdf`)
- Accessed: 2026-09-03
- Retrieved: yes (473 KB PDF downloaded with a browser User-Agent and a referer header; all
  fourteen pages extracted cleanly as Korean text)
- What was read, and what it is good for: this is the single densest quantitative document in
  the set. It carries the 순수보장형 / 만기환급형 split and the exact wording of the 해약환급금
  미지급형(납입기간중 0%, 납입기간후 50%) form; a 표준체 vs 건강체 premium grid at ages
  30/40/50 for both sexes on two different bases; the 건강체 criteria; the 단체취급 1.5%
  discount; complete 최고가입나이 matrices by 보험기간 × 납입기간 × sex for both product forms;
  the 가입한도 1,000만원~5억원; the 보험금 지급사유 and the 50% 장해 waiver; the **적용이율
  연복리 2.50%**; the **무배당 예정 경험 사망률** at ages 20/40/60; the **적용해지율** for the
  무해지 form (납입기간 이내 연 0.1%~8.4%, 납입기간 이후 연 0.8%); four 해약환급금 예시 tables;
  and the 보험가격지수 with its stated basis.

### S2 — 「한화생명 e정기보험 무배당 보험약관」, 한화생명보험(주)

- Publisher: 한화생명보험 주식회사
- Document: 보험약관 (약관 가이드북 + 주계약 약관 for both 만기환급형 and 순수보장형 + 특별약관
  + 분류표 + 부록), file `한화생명 e정기보험 무배당_약관_20260417.pdf`, **190 PDF pages**
- Doc type: 보험약관 (full policy conditions)
- URL:
  `https://static.hanwhalife.com/dynamic/direct/product/cms_odIN6hkhR1w3xURZ_1776383301736.pdf`
- Accessed: 2026-09-03
- Retrieved: yes (3.82 MB PDF downloaded; all 190 pages extracted as clean Korean text — the
  only glyph loss is in two cover graphics)
- What was read, and what it is good for: the **only full 약관 retrieved in this session**, and
  the source for every verbatim clause quoted below. Read in full for the 주계약 약관 and in
  part for the 특별약관. Articles used: 제3조 (한국표준질병·사인분류 적용기준), 제4조 (보험금의
  지급사유), 제5조 (보험금 지급에 관한 세부규정 — the 50% 장해 waiver), 제6조 (보험금을
  지급하지 않는 사유 — the 2-year suicide clause), 제8–9조 (청구·지급절차 with the 3/10/30
  영업일 timetable), 제10조 (보험금 받는 방법의 변경), 제12조 (보험수익자의 지정), 제14–15조
  (계약 전 알릴 의무 and its 위반 효과 — the contestability windows), 제16조 (사기에 의한
  계약), 제18조 (청약의 철회), 제20조 (계약의 무효), 제22조 (**보험나이**), 제23조 (계약의
  소멸), 제24–29조 (보장개시, 납입, 자동대출납입, 납입최고와 해지, 부활, 특별부활),
  제30조·제30조의2 (임의해지, 위법계약의 해지), 제31–32조, **제33조 (해약환급금 — including the
  미지급형 sub-article)**, 제34조 (보험계약대출), 제35조 (배당금의 지급), 제38조 (소멸시효),
  제39–41조; 【별표3】**재해분류표** in full; and the 건강체서비스특약Ⅱ, 단체취급특약,
  **선지급서비스특약(K3.10)** and 출산육아휴직 보험료 납입유예특약 wordings.

### S3 — 한화생명 다이렉트 「한화생명 e정기보험 무배당」 상품상세 페이지

- Publisher: 한화생명보험 주식회사 (다이렉트 채널)
- Doc type: 상품상세 (consumer product page), 준법감시인 확인필 `CS 26-08-109
  ('26.08.20~'27.08.19)`, 관리 디지털사업부 ('26.08)
- URL: `https://direct.hanwhalife.com/products/CM090101`
- Accessed: 2026-09-03
- Retrieved: yes (190 KB HTML fetched raw with `curl` and stripped; the graphics are SVG and
  carry no numbers this file depends on)
- What was read: the 사망보험금 1천만~5억원 range; the 순수보장형/만기환급형 choice; the
  statement that the 해약환급금 미지급형 is **14% cheaper** than the 표준형 on a stated basis;
  the 건강고객 0~20% discount and its three criteria; 가입가능연령 최대 만19세~65세; the 2-year
  suicide bar; the 예금자보호 1억원 notice; and the note that 「'26년 4월 산출이율 변경으로
  보험료가 변경되었습니다.」

### S4 — 생명보험협회 공시실, 상품비교공시 — 보장성보험 / **정기보험**

- Publisher: 사단법인 생명보험협회 (Korea Life Insurance Association), 공시실
- Doc type: 상품비교공시 (statutory cross-carrier product comparison disclosure)
- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/listNew.do` (POST with
  `search_prodGroup=024400010002`; eight pages at `pageUnit=30`)
- Accessed: 2026-09-03
- Retrieved: yes (all eight result pages fetched raw and the result table parsed; 45 distinct
  정기보험 products across 15 carriers were recovered with their 가입금액, 남/여 보험료,
  확정이율, 보험가격지수(남/여), 상품특징, 해약환급금 유형, 갱신여부, 판매채널 and 판매일자)
- What it is good for: **this is the sharpest quantitative source in the Korean market and it
  is public.** Because every product is disclosed on one prescribed 대표계약 basis `[S5]`, the
  table is a genuine like-for-like premium comparison — something no other country library in
  this repository has. It is the anchor for the model's premium basis and the evidence for
  every "observed range" in **Variation across carriers**. It also links each product's
  상품요약서 PDF, which is how [S6] and [S8]–[S12] and [S15]–[S18] were obtained.

### S5 — 생명보험협회 공시실, 「상품비교공시 세부작성기준 (대표계약 기준) - 보장성」

- Publisher: 사단법인 생명보험협회, 공시실
- Doc type: 공시 작성기준 (the disclosure's own basis table)
- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/informationPopup.do`
- Accessed: 2026-09-03
- Retrieved: yes (12 KB HTML fetched raw and read in full)
- What was read: the 대표계약 basis for every 상품군. For **정기보험 기본형** it is 성별
  남자/여자, **나이 40세, 보험기간 20년, 납입기간 전기납, 납입주기 월납, 가입금액 1억원**,
  applied identically to 만기환급형, 순수보장형 and 무해지/저해지환급; for the 무진단 무심사
  sub-class it is **65세, 최장만기(3/5년 등), 1천만원**; the same 40세/20년/1억원 basis applies
  to the 체증형 and 체감형 rows. For contrast the 종신보험 basis is 40세, 종신, 20년납, 월납,
  1억원. Without this document [S4] would be uninterpretable.

### S6 — 「무배당 흥국생명 온라인정기보험 상품요약서」, 흥국생명보험(주)

- Publisher: 흥국생명보험 주식회사
- Document: 상품요약서, 준법감시인 심의필 제26-CA1-0030호 (2026.02.08.), 8 numbered pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=15767&seq=14` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (96 KB PDF, extracted cleanly)
- What it is good for: **the only retrieved document that sets out a 갱신형 term product's
  renewal rules alongside the 비갱신형 alternative in the same product.** It carries the
  10년만기 갱신 cycle, the 80세 renewal ceiling, the truncation rule for a final renewal
  shorter than ten years, the statement that a **premium waiver already running does not carry
  into the renewed contract**, the 기본형/보장추가형 split (the latter paying 2× on 재해사망),
  the rule that a female life may only buy 보장추가형, full 보험기간 × 납입기간 × 가입나이
  matrices for both forms, the 위험등급-banded 가입한도, the 건강진단 thresholds by age band,
  the 적용이율 연복리 2.75%, 예정 경험사망률 **and 예정 재해사망률** at 20/40/60, four
  해약환급금 예시 tables (비갱신형 and 갱신형 × sex), and two 보험가격지수 tables.

### S7 — 「(무)흥국생명 온라인정기보험 예상 갱신보험료 예시」, 흥국생명보험(주)

- Publisher: 흥국생명보험 주식회사
- Doc type: 예상 갱신보험료 예시 (the disclosure's mandatory renewal-premium projection), 1 PDF
  page
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=15773&seq=10` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (31 KB PDF, extracted cleanly)
- What it is good for: **the single most useful quantitative document for the 갱신형
  mechanic.** A four-point attained-age premium path at 40/50/60/70 for both sexes on a stated
  basis, plus the caveat that the projection holds the rate scale at its issue-date level and
  reflects age increase only. §8 reproduces it in full.

### S8 — 「삼성 인터넷정기보험(2601)(무배당) 상품요약서」, 삼성생명보험(주)

- Publisher: 삼성생명보험 주식회사
- Document: 상품요약서, 9 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=42677&seq=4` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (230 KB PDF, extracted cleanly; the running text on two
  pages extracts with the inter-word spaces dropped but is fully legible)
- What was read: the 1종(순수보장형)/2종(만기환급형) × 1형(일반형)/2형(**걷기할인형**) matrix;
  the 슈퍼우량체 criteria; a **표준체 vs 슈퍼우량체 premium grid at ages 20/30/40/50 for both
  sexes** on the disclosure basis; the 보험기간 and 납입기간 menus; 가입나이 20~64세; 가입한도
  5,000만원~3억원; the 걷기할인형's 10% first-year discount and its 8,000-steps-on-20-days
  qualifying test; the 적용이율 (순수보장형 2.5%, 만기환급형 2.25%); 표준체 사망률 at 20/40/60;
  and two 해약환급금 예시 tables.

### S9 — 「삼성 내리사랑정기보험(2501)(무배당) 상품요약서」, 삼성생명보험(주)

- Publisher: 삼성생명보험 주식회사
- Document: 상품요약서, 16 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=40924&seq=4` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (273 KB PDF, extracted; the same word-spacing loss)
- What it is good for: a **face-to-face-channel** 정기보험 in a set otherwise dominated by
  direct writers, and the clearest statement of the **15-year 갱신형특약** cycle riding on a
  비갱신 정기보험 주계약. It carries the 고액할인 for 가입금액 ≥ 1억원, the 우량체 criteria,
  the 15-year renewal rule with its 15-days-before-expiry opt-out, the 재가입형 특약 variant,
  the 보험기간 menu (10년, 20년, 70/80/90세만기), 가입나이 20~65세, 가입한도 3,000만원~5억원,
  the 적용이율 (주보험·비갱신형특약 2.5%, 갱신형특약 2.0%), a 해약환급금 예시, and the
  보험가격지수 with its stated 가입기준.

### S10 — 「신한SOL정기보험(무배당) 상품요약서」, 신한라이프생명보험(주)

- Publisher: 신한라이프생명보험 주식회사
- Document: 상품요약서, 13 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=41655&seq=5` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (108 KB PDF, extracted cleanly)
- What it is good for: the **기본형 / 재해보장형** product split (the latter paying 2× the sum
  assured on 재해사망 and 1× otherwise) — the cleanest evidence in the set that Korean
  accidental-death cover is sold as a *product variant* as often as a rider. It also carries
  the widest 납입기간 menu retrieved (5년 through 전기납, plus 일시납 at 80세만기), 가입나이
  만15세~60세 (70세 for the 일시납 전환 case), banded 가입한도, the 신한단체취급보험료할인특약Ⅱ
  5% discount, 적용이율 연복리 2.1%, and — uniquely in this set — **the 보험개발원
  reference-rate document numbers behind its 예정 경험사망률 and 예정 재해사망률**. Its
  해약환급금 예시 is the only one given at **every policy year from 1 to 10**, which is what
  makes it usable as a shape check on a modelled reserve.

### S11 — 「KB 착한정기보험Ⅱ 무배당 상품요약서」, KB라이프생명보험(주)

- Publisher: KB라이프생명보험 주식회사
- Document: 상품요약서, 11 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=34504&seq=9` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (379 KB PDF, extracted cleanly)
- What was read: a **four-tier rate class** (표준체 / 비흡연체 / 건강체 / 슈퍼건강체) with
  criteria including a **총콜레스테롤 190mg/dL 미만** test not seen at any other carrier; a
  premium grid at 30/40/50 for both sexes across all four classes; a 보험기간 × 납입기간 ×
  가입나이 matrix; **가입한도 that rises with the rate class** (3,000만원 minimum for 표준체,
  1억원 minimum for 슈퍼건강체); 적용이율 연복리 2.50%; **four** mortality tables, one per rate
  class, at 20/40/60; and a 해약환급금 예시 at 60세만기 20년납 for both sexes.

### S12 — 「무배당 교보라플 정기보험 상품요약서」, 교보라이프플래닛생명보험(주)

- Publisher: 교보라이프플래닛생명보험 주식회사
- Document: 상품요약서, 28 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=13489&seq=31` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (335 KB PDF, extracted cleanly)
- What it is good for: **the only document retrieved that prints the 무해지 form and its 표준형
  comparator side by side, premium and surrender value, in one table.** It also carries the
  fullest rate-class definitions in the set (슈퍼건강체 / 건강체 / 비흡연자, with a 당뇨
  진단이력 definition given as four alternative tests), premium grids at 30/40/50 for both
  sexes across four classes and both product forms, the fullest 보험기간 × 납입기간 × 가입나이
  matrix retrieved (nine 만기 options × up to five 납입기간), 가입한도 1억원~10억원 in
  1,000만원 units, the five-way 무배당 보험료납입면제보장특약 menu (1종~5종), the 선납 rule,
  the **2026 평균공시이율 2.50%**, 적용이율 (미지급형 2.50%, 만기환급형 2.25%), **four**
  mortality tables one per rate class, and the 적용해지율 for the 무해지 form.

### S13 — 교보라이프플래닛, 「(무)교보라플 정기보험」 상품 페이지

- Publisher: 교보라이프플래닛생명보험 주식회사
- Doc type: 상품 페이지 (consumer)
- URL: `https://www.lifeplanet.co.kr/lpds2/insurance/term-life-insurance.dev`
- Accessed: 2026-09-03. Retrieved: yes (806 KB HTML fetched raw with `curl` and stripped)
- What was read: the 사망보험금 1억원~10억원 range; the 순수보장형 vs 만기환급형 framing; a
  headline "최대 63% 인하된 보험료" with its stated basis; two 보험료 예시 at 70세만기; the
  three rate classes' consumer-facing criteria; the 납입면제 특약 restricted to 순수보장형; the
  30-day 청약철회 and full refund; the 2-year suicide bar; and the note that the product was
  revised 「2026년 6월 보험료 변경에 따라」. **A block of 가입 시 유의사항 boilerplate on this
  page mixes several products' warnings** — see **Fetch failures and gaps**.

### S14 — 교보라이프플래닛, 「(무)라이프플래닛e정기보험Ⅱ」 보험료 설계 페이지

- Publisher: 교보라이프플래닛생명보험 주식회사
- Doc type: 상품 설계 페이지 (consumer quotation page)
- URL: `https://www.lifeplanet.co.kr/products/dth/HPPC61S0N.dev`
- Accessed: 2026-09-03. Retrieved: yes (840 KB HTML fetched raw with `curl` and stripped, after
  a summarising fetch of the same page returned a garbled reading of the premium block)
- What was read: a **second, older 정기보험 from the same carrier**, still on sale, with a
  선택형 만기환급률 of **0% / 50% / 100%** — the only three-way return-of-premium menu in the
  set; a four-class premium comparison at one cell; a three-point 만기환급률 premium comparison
  at the same cell; 사망보험금 3천만원~5억; 보험기간 10/15/20년 and 60/65/70/80세; 납입기간
  5/10/15/20년 and 55/60/65/70/80세, 월납·연납·**일시납**; and the rule that a 5-year term may
  only be written at 만기환급률 0%.

### S15 — 「푸본현대 원패스 정기보험 무배당/갱신형(2404) 상품요약서」, 푸본현대생명보험(주)

- Publisher: 푸본현대생명보험 주식회사
- Document: 상품요약서, 12 PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=37829&seq=5` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (108 KB PDF, extracted cleanly)
- What it is good for: **the shortest-cycle renewable term in the set** — a 1년만기 contract
  renewing up to four times for five years' total cover, sold through a mobile app, with the
  renewal effected by the policyholder *not* objecting 15 days before expiry. It also prints
  the 상품코드 for the 최초계약 and the 갱신계약 separately, which is direct evidence that a
  Korean renewal is a **new contract on a new product code**, not a continuation.

### S16 — 「푸본현대 원패스 정기보험 예상 갱신보험료 예시」, 푸본현대생명보험(주)

- Publisher: 푸본현대생명보험 주식회사
- Doc type: 예상 갱신보험료 예시, 1 PDF page
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=37830&seq=2` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (22 KB PDF, extracted cleanly)
- What was read: the four-renewal premium path at ages 41–44 on a 1,000만원 / 남자 40세 /
  10년만기 / 전기납 basis, with the same rate-scale-frozen caveat as [S7]. Note the internal
  inconsistency in the document's own basis line — see **Fetch failures and gaps**.

### S17 — 「미래에셋생명 헤리티지 정기보험 무배당 상품요약서」, 미래에셋생명보험(주)

- Publisher: 미래에셋생명보험 주식회사
- Document: 상품요약서, 20+ PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=43797&seq=2` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (2.72 MB PDF; extracted, but with a space after almost
  every syllable block, so the text was reflowed before reading and each figure re-checked)
- What it is good for: the **간편고지형** (simplified-issue) form and its **2-year 50% 감액지급
  period** for non-accidental death — Korea's graded death benefit, which has no analogue in
  the level-term products of `uklib` or `jplib`. It also carries a **종신전환특약** (conversion
  to whole life) and a **연금전환특약** (conversion to an annuity), the 납입면제특약Ⅱ with its
  [특약유형 W]/[특약유형 S] split on whether the rider's 계약자적립액 is paid on death, a
  80세/90세만기-only term menu, 가입한도 2천만원~2억원 (1억원 for 간편고지형), 적용이율 연복리
  2.00%, and mortality at 20/40/60.

### S18 — 미래에셋생명, 「경영인을 위한 정기보험 무배당」 상품요약서

- Publisher: 미래에셋생명보험 주식회사
- Document: 「경영인을 위한 정기보험 무배당 [해약환급금이 적은 유형]」 상품요약서 (일반가입형 /
  간편고지형), 20+ PDF pages
- Doc type: 상품요약서
- URL: `https://pub.insure.or.kr/FileDown.do?fileNo=44327&seq=2` (linked from [S4])
- Accessed: 2026-09-03. Retrieved: yes (2.90 MB PDF; same reflow treatment as [S17])
- What it is good for: the **경영인정기보험** family in full — a 90세만기 전기납 contract,
  가입금액 5천만원~30억원, whose sum assured escalates from year 10 by a printed formula
  (체증보험금 = 보험가입금액 × 체증률 × (계약경과년수 − 9), 체증률 10%), with a worked
  사망보험금 schedule, a **three-step 해약환급금이 적은 유형** (0% to year 3, 30% of the 기본형
  to year 5, 95% thereafter) and a **해약환급금 중도지급옵션** (partial surrender, from year 7,
  up to twelve times a policy year).

### S19 — 「한화생명 H종신보험 무배당 상품요약서」, 한화생명보험(주)

- Publisher: 한화생명보험 주식회사
- Document: 상품요약서, 20 PDF pages, `2209-A01_A17`, dated 20251003
- Doc type: 상품요약서 (whole life — used here only for the rider menu)
- URL:
  `https://static.hanwhalife.com/dynamic/direct/product/cms_6r7g9G9XxiX5MbrW_1762729381266.pdf`
- Accessed: 2026-09-03. Retrieved: yes (677 KB PDF, extracted cleanly)
- Why it is here: to test whether a current Korean 종신보험 still carries a **정기특약** in its
  rider menu. It does not. Its 상품의 구성 lists 3대질병케어특약, 9대질병보험료납입면제특약 and
  eleven 제도성특약 — and **no term rider at all** (§16).

### S20 — 「무배당 AIA 더해주는 종신보험 상품요약서」, AIA생명보험(주)

- Publisher: AIA생명보험 주식회사; the summary states 「이 상품요약서는 2026년 1월 1일부터
  적용됩니다.」
- Doc type: 상품요약서 (whole life — same purpose as [S19])
- URL:
  `https://www.aia.co.kr/content/dam/kr-wise/ko/docs/products/life-protection/summary/AIA_kr_Form120_20260101.pdf`
- Accessed: 2026-09-03. Retrieved: yes (731 KB PDF; a summarising fetch reported it as binary,
  so the saved file was extracted locally with `pymupdf`, which recovered it cleanly)
- Why it is here: same test as [S19], same answer — the string 정기특약 does not occur.

### S21 — 「한화생명 하나로H종신보험 무배당」 and 「한화생명 e종신보험 무배당」 상품요약서

- Publisher: 한화생명보험 주식회사
- Doc type: 상품요약서 (whole life — same purpose as [S19])
- URLs: `https://pub.insure.or.kr/FileDown.do?fileNo=45581&seq=3` and
  `https://pub.insure.or.kr/FileDown.do?fileNo=45532&seq=2` (both linked from the 종신보험 view
  of the same disclosure as [S4], `search_prodGroup=024400010001`)
- Accessed: 2026-09-03. Retrieved: yes (753 KB and 553 KB PDFs, extracted cleanly)
- Why they are here: same test, same answer — neither rider menu contains a 정기특약.

### S22 — 생명보험협회 공시실, 상품비교공시 — 보장성보험 / **종신보험**

- Publisher: 사단법인 생명보험협회, 공시실
- Doc type: 상품비교공시
- URL: `https://pub.insure.or.kr/compareDis/prodCompare/assurance/listNew.do` (POST with
  `search_prodGroup=024400010001`; first two pages fetched)
- Accessed: 2026-09-03. Retrieved: yes, in part (pages 1–2 of the 종신보험 result set)
- Why it is here: to check the disclosed 특약 text of current 종신보험 for a 정기특약. Across
  the two pages read, the substring 정기 occurs only in the page's own category label. Used in
  §16 as negative evidence and nowhere else.

### S23 — 「삼성생명 자유설계보장보험(무배당) 약관」 (2014), via insclaim.co.kr

- Publisher: 삼성생명보험 주식회사, republished by 인스클레임
- Doc type: 과거약관 (superseded policy conditions), named in a search result as containing a
  정기특약
- URL: `https://www.insclaim.co.kr/39/8650566`
- Accessed: 2026-09-03. **Retrieved: no** (HTTP 404). See **Fetch failures and gaps**; the
  정기특약 claim in §16 rests on a search snippet and is tagged `[unverified]`.

### S24 — 오렌지라이프, 「무) 스마트 정기보험」 상품 페이지

- Publisher: 오렌지라이프생명보험 (now part of 신한라이프)
- Document: 「무) 스마트 정기보험 1종 (순수보장형)」 and 「2종 (만기환급형)」
- Doc type: 상품 페이지
- URLs: `https://www.orangelife.co.kr/bizxpress/home/ap/wt/scwapwt070m.shtm` and
  `.../scwapwt100m.shtm`
- Accessed: 2026-09-03. **Retrieved: no** (HTTP 503 on both; plain `curl` was reset by the
  host). No fact below rests on them.

---

## Regulatory and actuarial references

### R1 — 보험업법 제2조 (정의)

- Publisher: 국가법령정보센터 / 법제처 — 보험업법, 법률 제19211호, 2022-12-31 일부개정, 시행
  2023-01-01
- Doc type: statute
- URL (retrieved): `https://casenote.kr/법령/보험업법/제2조`
- Accessed: 2026-09-03. Retrieved: yes (casenote.kr serves article text to a plain fetcher; the
  equivalent `law.go.kr/법령/...` URL returns only site chrome — see gaps)
- Content used: the definition of 보험상품 and, within it, of **생명보험상품** — 「위험보장을
  목적으로 사람의 생존 또는 사망에 관하여 약정한 금전 및 그 밖의 급여를 지급할 것을 약속하고
  대가를 수수하는 계약」 — and of **제3보험상품**, 「위험보장을 목적으로 사람의 질병·상해 또는
  이에 따른 간병에 관하여…」. This is the clause that puts 정기보험 squarely in the 생명보험
  (first-sector) class and outside 제3보험.

### R2 — 보험업법 제4조 (보험업의 허가)

- Publisher: 국가법령정보센터 / 법제처 — 보험업법, 법률 제17636호, 2020-12-08 일부개정, 시행
  2021-06-09 (the article's own last-amended stamp on the retrieved page)
- Doc type: statute
- URL (retrieved): `https://casenote.kr/법령/보험업법/제4조`
- Accessed: 2026-09-03. Retrieved: yes
- Content used: the three-way licence split — **생명보험업** (생명보험, 연금보험(퇴직보험
  포함), 그 밖에 대통령령으로 정하는 보험종목), **손해보험업**, and **제3보험업** (상해보험,
  질병보험, 간병보험, 그 밖에 대통령령으로 정하는 보험종목) — and the restriction of the
  licence to 주식회사, 상호회사 및 외국보험회사. 제4조제1항제3호 is the statutory footing of
  the 제3보험 category that four other krlib products sit in; 정기보험 is written under
  제1항제1호.

### R3 — 상법 제731조 (타인의 생명의 보험)

- Publisher: 국가법령정보센터 / 법제처 — 상법, 시행 2020-12-10, 법률 제17354호
- Doc type: statute
- URL (retrieved): `https://casenote.kr/법령/상법/제731조`
- Accessed: 2026-09-03. Retrieved: yes
- Content, verbatim: 제1항 「타인의 사망을 보험사고로 하는 보험계약에는 보험계약 체결시에 그
  타인의 서면에 의한 동의를 얻어야 한다.」 제2항 「보험계약으로 인하여 생긴 권리를 피보험자가
  아닌 자에게 양도하는 경우에도 제1항과 같다.」 This is the rule every 약관 in this set
  reproduces as a ground of 계약의 무효.

### R4 — 상법 제732조 (15세미만자등에 대한 계약의 금지) and 제732조의2 (중과실로 인한 보험사고)

- Publisher: 국가법령정보센터 / 법제처 — 상법
- Doc type: statute
- URLs: `https://casenote.kr/법령/상법/제732조` and
  `https://glaw.scourt.go.kr/wsjo/lawod/sjo192.do?lawodNm=상법&jomunNo=732&jomunGajiNo=2`
- Accessed: 2026-09-03. **Retrieved: in part** — the article text below was returned by a
  search of those pages rather than by a direct fetch of each; the wording matches the
  paraphrase that every retrieved 약관 gives, so it is treated as reliable, but the pinpoint
  citation is marked accordingly wherever it is used.
- Content: 제732조 「15세미만자, 심신상실자 또는 심신박약자의 사망을 보험사고로 한 보험계약은
  무효로 한다. 다만, 심신박약자가 보험계약을 체결하거나 제735조의3에 따른 단체보험의 피보험자가
  될 때에 의사능력이 있는 경우에는 그러하지 아니하다.」 제732조의2 「사망을 보험사고로 한
  보험계약에는 사고가 보험계약자 또는 피보험자나 보험수익자의 중대한 과실로 인하여 생긴
  경우에도 보험자는 보험금액을 지급할 책임을 면하지 못한다.」

### R5 — 상법 제651조 (고지의무위반으로 인한 계약해지)

- Publisher: 국가법령정보센터 / 법제처 — 상법, 시행 1993-01-01, 법률 제4470호, 1991-12-31
  일부개정
- Doc type: statute
- URL (retrieved): `https://casenote.kr/법령/상법/제651조`
- Accessed: 2026-09-03. Retrieved: yes
- Content, verbatim: 「보험계약당시에 보험계약자 또는 피보험자가 고의 또는 중대한 과실로 인하여
  중요한 사항을 고지하지 아니하거나 부실의 고지를 한 때에는 보험자는 그 사실을 안 날로부터
  1월내에, 계약을 체결한 날로부터 3년내에 한하여 계약을 해지할 수 있다. 그러나 보험자가
  계약당시에 그 사실을 알았거나 중대한 과실로 인하여 알지 못한 때에는 그러하지 아니하다.」 The
  1개월 / 3년 pair is exactly what [S2] 제15조 reproduces, with a tighter 2-year (1-year for
  진단계약 질병) contractual bar added on top.

### R6 — 상법 제659조 (보험자의 면책사유)

- Publisher: 국가법령정보센터 / 법제처 — 상법
- URL (retrieved): `https://casenote.kr/법령/상법/제659조`
- Accessed: 2026-09-03. Retrieved: yes
- Content, verbatim: 「보험사고가 보험계약자 또는 피보험자나 보험수익자의 고의 또는 중대한
  과실로 인하여 생긴 때에는 보험자는 보험금액을 지급할 책임이 없다.」 Read together with [R4]
  제732조의2, this is why a Korean life 약관's exclusion list contains **only intent** and
  never gross negligence.

### R7 — 상법 제662조 (소멸시효)

- Publisher: 국가법령정보센터 / 법제처 — 상법, 시행 2015-03-12, 법률 제12397호
- URL (retrieved): `https://casenote.kr/법령/상법/제662조`
- Accessed: 2026-09-03. Retrieved: yes
- Content, verbatim: 「보험금청구권은 3년간, 보험료 또는 적립금의 반환청구권은 3년간,
  보험료청구권은 2년간 행사하지 아니하면 시효의 완성으로 소멸한다.」

### R8 — 소득세법 제59조의4 (특별세액공제)

- Publisher: 국가법령정보센터 / 법제처 — 소득세법, 법률 제19196호, 2022-12-31 일부개정, 시행
  2024-01-01
- Doc type: statute
- URL (retrieved): `https://casenote.kr/법령/소득세법/제59조의4`
- Accessed: 2026-09-03. Retrieved: yes
- Content used: 제1항 — 「그 금액의 100분의 12(제1호의 경우에는 100분의 15)에 해당하는 금액을
  해당 과세기간의 종합소득산출세액에서 공제한다」, subject to 「다음 각 호의 보험료별로 그
  합계액이 각각 연 100만원을 초과하는 경우 그 초과하는 금액은 각각 없는 것으로 한다」; 제1호 is
  장애인전용보장성보험료 (15%), 제2호 the general 보장성보험료 (12%). This is a **tax credit,
  not a deduction**, which is the structural difference from Japan's 生命保険料控除 and from
  every other market in this repository.

### R9 — 보험업감독규정 【별표14】 표준해약환급금 계산시 적용되는 해약공제액 (제7-66조 관련)

- Publisher: 금융위원회 — 보험업감독규정 별표, 개정 2011-01-24, 2015-05-07, 2020-01-15
- Doc type: 고시 별표 (annex to the supervisory regulation)
- URL (retrieved): `https://www.law.go.kr/LSW//flDownload.do?flSeq=137472119&flNm=[별표 14]
  표준해약환급금계산시 적용되는 해약공제액(제7-66조관련)`
- Accessed: 2026-09-03. Retrieved: yes (111 KB PDF downloaded through a summarising fetch that
  reported it as binary, then extracted locally with `pymupdf`; the text came out complete,
  with inter-word spacing lost, and was read in full)
- Content, verbatim (spacing restored): the **표준해약공제액** is 「연납순보험료의
  5%×해약공제계수 + 보장성보험의 보험가입금액의 10/1000」, with 주2 「해약공제계수는 다음과
  같이 적용함 — 보장성보험: 보험기간(최대20년); 저축성보험: 보험료납입기간(최대12년)…」 and 주3
  「연납순보험료 및 연납위험보험료는 다음과 같이 적용함 — 보장성보험: 전기납(단, 보험기간이
  20년 이상인 경우 20년납)으로 조정하여 산출한 연납순보험료 및 연납위험보험료…」. Notes 4–7
  carry the 생존연금보험 6% rule, the 연금저축보험 4% (무배당 3%) rule, the 저축성보험 offset,
  and the 실손의료보험 substitution of 「보장성보험의 연납위험보험료의 15%」 for the
  sum-assured term. This is the **statutory cap on the surrender charge** and has no US, UK,
  French or German analogue at this level of prescription.

### R10 — 보험업감독규정 (금융위원회고시), 본문

- Publisher: 금융위원회 — 보험업감독규정, 행정규칙일련번호 **2100000279112**, 발령일자
  **2026-05-06**, 발령번호 **2026-16**, 제개정구분 일부개정, 현행
- Doc type: 고시 (supervisory regulation)
- URLs tried: `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` (chrome only);
  `https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000279112&type=HTML`
  (empty); the same with `type=JSON` and with `LID=`/`MST=` (500 or empty);
  `https://www.law.go.kr/DRF/mobileAdmRulInfoR.do` POST (connection reset)
- Accessed: 2026-09-03. **Retrieved: no** for the body text; **Retrieved: yes** for the
  identifying metadata above, which came from
  `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&query=보험업감독규정`.
- Consequence: **제7-66조 (해약환급금) itself was never read.** Its 별표 [R9] was, and the
  carriers' own 상품요약서 restate the rule in their own words ("순보험료식 계약자적립액에서
  미상각신계약비(해약공제액)를 공제한 금액") — but the article's own text, the 해약공제기간 and
  the amortisation schedule of the deduction are **[unverified]** in this file. See gaps.

### R11 — 보험업감독업무시행세칙 (금융감독원세칙)

- Publisher: 금융감독원 — 보험업감독업무시행세칙, 행정규칙일련번호 **2200000108939**, 발령일자
  **2026-08-28**, 시행일자 **2026-09-10**
- Doc type: 세칙 (supervisory enforcement rules; its 별표 carry the 보험료 및 해약환급금
  산출방법서 작성기준 and the 표준약관)
- URL:
  `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&query=보험업감독업무시행세칙`
- Accessed: 2026-09-03. **Retrieved: in part** — search metadata only; the body was not
  reachable by any route tried (same failure mode as [R10]).
- Consequence: the 표준약관 wording is cited in this file only through the carrier 약관 [S2]
  that reproduces it, never directly.

### R12 — 금융위원회 보도자료 (2021-11-08), 무·저해지보험의 상품설계 개선

- Publisher: 금융위원회 보험과, 2021-11-08
- Document, full title: 「무·저해지보험의 지속가능성 제고를 위해 소비자 보호와 보험사 건전성
  유지 측면에서 상품설계를 합리적으로 개선하겠습니다.」
- Doc type: 보도자료 (regulator press release)
- URL: `https://www.fsc.go.kr/no010101/76830`
- Accessed: 2026-09-03. Retrieved: yes (fetched and read; plain `curl` to `fsc.go.kr` was reset
  by the host, so the retrieval was through the summarising fetcher)
- Content used: the growth of 무·저해지 new business — 신계약건수 ('16) 30.4만건 → ('18)
  171.7만건 → ('20) 443.5만건 → ('21.1~8) 279.8만건, and 신계약비중 ('16) 1.4% → ('18) 6.8% →
  ('20) 14.7% → ('21.8) 13.7%; the 해지율 산출기준 then imposed — 「해지환급금 수준이
  낮으면(10%, 50%) 해지율을 더 낮게(0.2%, 1%) 적용」 and 「보험료 납입중 해지율은 기간이
  경과할수록 하락(예: 5차년도 5%, 10차년도 2%)」; and a worked table of premium against
  post-completion 해약환급금 level (§11). The measures were to take effect in 2022.

### R13 — 금융위원회 보도자료 (2024-11-07), IFRS17 계리가정 가이드라인

- Publisher: 금융위원회 / 금융감독원 (제4차 보험개혁회의), 2024-11-07
- Document, full title: 「합리적인 계리가정과 단계적 할인율 조정을 통해 보험회계의 신뢰도와
  안정성을 높이겠습니다」
- Doc type: 보도자료 — announcing the 「IFRS17 주요 계리가정 가이드라인」 and the 「보험부채
  할인율 현실화 연착륙 방안」
- URL: `https://www.fsc.go.kr/no010101/83351`
- Accessed: 2026-09-03. Retrieved: yes
- Content used: the **무·저해지 해지율 원칙모형** is a 「로그-선형(log-linear) 모형 원칙(수렴점
  0.1%)」; the permitted 예외모형 are limited to 선형-로그모형 (수렴점 0%) and 로그-로그모형
  (수렴점 0.1%), and only on strict disclosure conditions — 「감사보고서·경영공시에 他모형
  선정의 특별한 근거와 원칙모형과의 차이(CSM, K-ICS, 당기순이익 등)를 상세히 공시」 plus
  quarterly reporting and on-site inspection; the **완납 후 최종해지율 0.8%**; a 30%
  additional-lapse floor for 단기납 종신보험; and the extension of the discount curve's
  최종관찰만기 to 30 years phased over three years. The guideline applies from the 2024
  year-end close (loss-ratio assumptions deferred to 2025 Q1); the discount-rate measures from
  January 2025.

### R14 — 보험개발원 제10회 경험생명표 개정 (as reported by 보험매일)

- Publisher: report by 보험매일 (fins.co.kr), 김명재 기자, 2024-01-10; the underlying work is
  보험개발원 (Korea Insurance Development Institute)
- Doc type: **news article** — the KIDI announcement itself was not retrieved (see gaps), so
  every figure here is second-hand and is tagged accordingly wherever used
- URL: `https://www.fins.co.kr/news/articleView.html?idxno=99460`
- Accessed: 2026-09-03. Retrieved: yes (the article body was fetched raw and read)
- Content used: 평균수명 남자 **86.3세**, 여자 **90.7세**, up **2.8년** and **2.2년** on the
  ninth table; 65세 기대여명 남자 **23.7년**, 여자 **27.1년**, up 2.3 and 1.9; the table is
  prepared **every five years** under 보험업법 from life-insurance policyholder statistics; it
  runs above the 국민생명표 because of underwriting selection; carriers may use it where their
  own experience is thin; it feeds the **보험가격지수** calculation; and the industry expected
  to apply it **from April 2024**. The article also notes the direction of effect — 사망보험
  premiums down, 연금보험 premiums up.

### R15 — 국가데이터처(통계청), 「2024년 생명표 작성 결과」

- Publisher: 국가데이터처 (formerly 통계청), published 2025-12-03
- Doc type: 보도자료 with the 완전생명표
- URL: `https://mods.go.kr/board.es?mid=a10301010000&bid=208&act=view&list_no=439533`
- Accessed: 2026-09-03. Retrieved: yes (the release page was fetched and read; the attached
  full table files were not opened)
- Content used: 기대수명 전체 **83.7년**, 남자 **80.8년**, 여자 **86.6년**, each +0.2년 on
  2023; 60세 기대여명 남자 **23.7년**, 여자 **28.4년**; 유병기간 제외 기대수명 65.5년; the
  leading-cause death probabilities for a 2024 birth (암 19.5%, 폐렴 10.2%, 심장질환 10.0%,
  뇌혈관질환 6.9%). This is the **public** national table against which the **non-public**
  경험생명표 [R14] has to be anchored.

### R16 — 보험연구원, 「2026년 보험산업 전망」

- Publisher: 보험연구원 (Korea Insurance Research Institute), 노건엽, 2025-10-21 세미나 자료
- Doc type: 세미나 자료 (industry outlook deck)
- URL: `http://www.kiri.or.kr/pdf/세미나자료/smn_20251021_1.pdf`
- Accessed: 2026-09-03. Retrieved: yes (3.35 MB PDF downloaded and extracted; the charts' data
  labels extract as bare numbers and were read against their axis labels)
- Content used: 2025 H1 생명보험 수입보험료 (퇴직연금 제외) **51조원**, +6.1% year on year;
  생명보험 연납화초회보험료 2024 **19.3조원** and 2025 H1 **10.2조원**, +3.4%; 보장성보험
  수입보험료 2021–2024 **44.9 / 47.1 / 48.6 / 55.0조원** and 2025 H1 **30.3조원** (+13.0%); and
  the qualitative finding that growth is concentrated in **무·저해지환급형 질병보험과
  상해보험** rather than in death cover.

### R17 — 예금자보호한도의 1억원 상향

- Publisher: 예금보험공사 / 금융위원회; the change was announced by 예금보험공사 and relayed by
  금융투자협회
- Doc type: 안내사항 (public notice)
- URL: `https://www.kofia.or.kr/brd/m_212/view.do?seq=172`
- Accessed: 2026-09-03. **Retrieved: in part** — the fact was confirmed by search across the
  예금보험공사, 금융투자협회 and 대한민국 정책브리핑 results, but no primary page was fetched.
  The same 1억원 figure appears verbatim in three retrieved carrier documents ([S3] [S11]
  [S13]), which is what makes it usable.
- Content: the deposit-protection limit rose from 5천만원 to **1억원 with effect from
  2025-09-01**, and for an insurance contract it covers 해약환급금 / 만기보험금 / 기타지급금 up
  to 1억원 per person, with a **separate** 1억원 limit for 사고보험금.

### R18 — 보험저널, 저해지 종신보험 3년차 해지율 '50%' 돌파

- Publisher: 보험저널 (insjournal.co.kr), published 2025-05-14, updated 2025-05-15
- Document, full title: 「금융당국 해지율 예측 한참 빗나가… 저해지 종신보험 3년차 해지율 '50%'
  돌파」
- Doc type: **news article** — the underlying supervisory data was not retrieved
- URL: `https://www.insjournal.co.kr/news/articleView.html?idxno=26597`
- Accessed: 2026-09-03. Retrieved: yes
- Content used: for 5·7년납 저해지 단기납 종신보험, the actual **37회차 유지율 50.2%** (i.e. a
  three-year lapse rate of 49.8%) against a **가정 유지율 71.5%** (assumed lapse 28.5%), with
  conventional 종신보험 at 46.0% persistency. It is a whole-life datum, not a term one, and is
  used in this file only to make the point that the 무·저해지 lapse assumption is the parameter
  Korean supervision is least confident about.

### R19 — 보험개발원 참조순보험요율 (문서번호, via [S10])

- Publisher: 보험개발원
- Doc type: reference-rate notifications, cited by document number inside a carrier's
  상품요약서 rather than published as documents this session could open
- Numbers as printed in [S10]: 예정 경험사망률 「보험개발원 생명장기 제2024-0250호
  (2024.01.23.)」; 예정 재해사망률 「보험개발원 생명장기 제2023-2072호(2023.12.06.)」
- Accessed: 2026-09-03. **Retrieved: no** — the notifications themselves are not public
  documents; only their identifiers were recovered, from [S10]. They are recorded here because
  they establish the *provenance chain* for a Korean carrier's pricing mortality: 보험개발원
  issues a 참조순보험요율, the carrier adjusts it, and the adjusted 예정 경험사망률 is what the
  상품요약서 prints.

### R20 — 보험개발원 (KIDI) website — 참조순보험요율 / 보험통계 pages

- Publisher: 보험개발원
- URLs: `https://www.kidi.or.kr/` (index, retrieved), `/user/nd78654.do` (참조순보험요율,
  retrieved as an HTML shell), `/user/nd87617.do` (보험통계 서비스, not opened)
- Accessed: 2026-09-03. **Retrieved: in part** — the index and the 참조순보험요율 landing page
  returned HTTP 200 and were fetched, but neither carries the 제10회 경험생명표 announcement or
  any numeric table. Nothing in this file rests on them.

### R21 — 금융감독원 (FSS) website

- Publisher: 금융감독원
- URL: `http://www.fss.or.kr/`
- Accessed: 2026-09-03. **Retrieved: no** — the host returned a 「금융감독원 홈페이지 중단
  안내」 interstitial to search, and plain `curl` was reset. The FSS-side material used in this
  file (the IFRS17 계리가정 가이드라인) was therefore taken from the joint 금융위원회 release
  [R13].

---

## Fact extraction

### 1. Where 정기보험 sits in Korean insurance law

- 정기보험 is **생명보험**, not 제3보험. 보험업법 제2조 defines a 생명보험상품 as a contract
  「위험보장을 목적으로 사람의 생존 또는 사망에 관하여 약정한 금전 및 그 밖의 급여를 지급할
  것을 약속하고 대가를 수수하는 계약」, and a 제3보험상품 as one 「…사람의 질병·상해 또는 이에
  따른 간병에 관하여…」 [R1]. 보험업법 제4조제1항 splits the licence three ways — 생명보험업
  (생명보험, 연금보험(퇴직보험 포함), 그 밖에 대통령령으로 정하는 보험종목), 손해보험업, and
  제3보험업 (상해보험, 질병보험, 간병보험, 그 밖에 대통령령으로 정하는 보험종목) [R2]. Only a
  생명보험회사 (or a 제3보험 licensee, for the third-sector part) may write it; every one of
  the fifteen carriers in [S4] is a 생명보험회사.
- The 재해사망 uplift that several 정기보험 carry ([S6] 보장추가형, [S10] 재해보장형) is
  **still 생명보험**, because it is a fixed sum payable 「사람의…사망에 관하여」 — the trigger
  is refined, not the class. It is not the 상해보험 of 제4조제1항제3호. This matters for the
  library: 재해사망 cover on this chassis does **not** put the product into 제3보험, which is
  the boundary `cancer`, `long_term_care`, `child` and `indemnity_medical` live on.
- **Contractual ground rules imposed by 상법 제4편 (보험).** Every 약관 in this set reproduces
  them:
  - 제731조제1항 — a policy on another's death requires that person's **written consent at the
    time the contract is concluded** [R3]; absence of it makes the contract void, and every
    retrieved 약관 lists that as the first ground of 계약의 무효 [S2 제20조] [S8] [S10] [S11]
    [S17].
  - 제732조 — a contract on the death of a person **under 15**, or of a 심신상실자 or
    심신박약자, is void, with a narrow capacity exception for the latter [R4]; again reproduced
    verbatim in every 약관.
  - 제732조의2 — for a death contract the insurer is **not** discharged where the event arose
    from gross negligence [R4]. Read with 제659조, which discharges the insurer for 「고의 또는
    중대한 과실」 generally [R6], this is why a Korean life 약관's exclusion list contains
    **only three intent-based limbs** and no negligence limb at all (§14).
  - 제651조 — rescission for 고지의무위반 within **1개월 of learning the fact** and **3년 of
    contracting** [R5]; 제662조 — a **3-year** limitation on 보험금청구권 and on 보험료/적립금
    반환청구권, **2 years** on 보험료청구권 [R7].
- The library's practical consequence: on this chassis the *benefit definition* is short (§5),
  the *exclusion set* is fixed by statute and identical across carriers (§14), and all the
  product variation lives in the **premium**, the **surrender-value form** and the **renewal
  structure**. That is the opposite of `jplib`'s 定期保険, where the 高度障害保険金 schedule
  does a lot of definitional work, and of `uklib`, where the critical-illness definitions do.

### 2. The product taxonomy — six independent axes

Korean 정기보험 is not one shape with options; it is a small grid. Six axes appear in the
retrieved documents, and a carrier's product name usually encodes three or four of them.

1. **순수보장형 vs 만기환급형.** 순수보장형 (pure protection) pays only the 사망보험금 and
   nothing at maturity. 만기환급형 (return of premium) additionally pays a 만기보험금 equal to
   **이미 납입한 주계약 보험료의 100%** if the life survives to the end of the term [S1] [S8]
   [S12] [S17]. The split is offered by every carrier that sells retail term.
   교보라이프플래닛's older 라이프플래닛e정기보험Ⅱ generalises it to a **선택형 만기환급률 of
   0% / 50% / 100%** [S14] — the only three-way menu retrieved.
2. **비갱신형 vs 갱신형.** See §8. 비갱신형 is the default in every carrier's flagship product;
   흥국생명 sells both as 1종/2종 of the same product [S6], and 푸본현대 sells a 갱신-only
   product [S15].
3. **세만기 vs 년만기.** 세만기 runs to a stated attained age (60/65/70/75/80/85/90/100세만기);
   년만기 runs a fixed number of years (10/15/20/25/30년만기). Both are on sale everywhere and
   a single carrier normally offers both menus in one product [S1] [S8] [S10] [S12]. See §3.
4. **표준형 vs 무해지환급형 / 저해지환급형.** See §9–§10. The industry's formal names for the
   suppressed-value forms are, verbatim: 「해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)」
   [S1] [S2], 「해약환급금 미지급형」 [S12], 「해약환급금이 적은 유형」 [S18], and 「해약환급금
   일부지급형」 as it appears in the disclosure's product names [S4].
5. **표준체 / 비흡연체 / 건강체 / 슈퍼건강체 (or 우량체 / 슈퍼우량체).** See §7. One to four
   classes, sold either as a 종 of the main contract [S11] or as a 할인특약 riding on it [S2
   건강체서비스특약Ⅱ] [S12 무배당 비흡연자할인특약Ⅲ, 건강체할인특약, 슈퍼건강체할인특약Ⅱ].
6. **일반가입형 vs 간편고지형 (or 일반심사형 / 간편심사형).** 간편고지형 is a simplified-issue
   form for 유병력자 and older lives, with fewer 계약 전 알릴 의무 questions, no medical, a
   higher premium, and — the point that matters for a model — a **graded death benefit**: at
   미래에셋 「계약일로부터 2년 미만에 재해 이외의 원인으로 지급사유가 발생한 경우에는
   '보험가입금액의 50%' 지급」 [S17] [S18].

Two further shapes are sold under the same 정기보험 heading and are recorded here because they
dominate the top of the disclosed premium range:

- **체증형 (escalating)** — the 경영인정기보험 family. 미래에셋's version prints the formula:
  「체증보험금 = 보험가입금액 × 체증률 × (계약경과년수 － 9)」 with 체증률 10%, so the sum
  assured is level for the first ten years and then rises by 10% of the original sum each year
  [S18]. Its worked schedule, for 가입나이 40세 / 1억원 / 90세만기: 10년 미만 10,000만원;
  10–11년 11,000만원; 11–12년 12,000만원; 12–13년 13,000만원; 13–14년 14,000만원, and so on
  [S18]. The disclosure marks 체증형 for 한화생명 경영인H정기보험, 교보경영인정기보험, KB
  경영인정기보험III, 메트라이프 The Classic 경영인정기보험, DB생명 간편한 경영인 정기보험, AIA
  안심+ 경영인 정기보험 and 행복한NH경영인정기보험 [S4].
- **체감형 (decreasing)** — a category the disclosure recognises [S4] [S5] but for which no
  retail product appeared in the 정기보험 result set. The nearest retrieved products are the
  loan-linked 대출안심보험 (삼성 인생금융 / 상생금융 대출안심보험), which are classed 기본형
  and whose sums assured shadow a loan [S4]; no 대출안심보험 document was retrieved and no fact
  about its amortisation schedule is asserted.

### 3. Issue age, term and premium-paying-period envelopes

**Per carrier, as published.** "전기납" means the premium-paying period equals the policy term.

| Carrier / product | 가입나이 | 보험기간 | 납입기간 | 납입주기 |
|---|---|---|---|---|
| 한화생명 e정기보험 [S1] | 만19세~65세 (건강체 20세; 순수보장형 10년만기 전기납 남 30세·여 40세 minimum) | 순수보장형 10년만기 + 60/65/70/80/90/100세만기; 만기환급형 65/70/80/90/100세만기 | 10년, 20년, 전기납 | 월납 |
| 삼성 인터넷정기보험 [S8] | 20세~64세 | 순수보장형 10/20년 + 60/65/70/80세만기; 만기환급형 20년 + 60/65/70/80세만기 | 10년납, 20년납, 전기납 (10년만기는 10년납만) | 월납 |
| 삼성 내리사랑정기보험 [S9] | 20세~65세 | 10년, 20년, 70/80/90세만기 | 15년납, 20년납, 전기납 | 월납 |
| 신한SOL정기보험 [S10] | 만15세~60세 (80세만기 일시납은 ~70세) | 10/15/20/25/30년만기, 60/70/80세만기 | 5·10·15·20·25·30년납, 60세납, 70세납, 전기납, 일시납 (80세만기) | 월납 |
| KB 착한정기보험Ⅱ [S11] | 만19세~70세 (by 보험기간·납입기간) | 10년만기, 60/65/70/80세만기 | 5·7·10·15·20년납, 55세납, 60세납, 전기납 | 월납·3개월납·6개월납·연납 |
| 교보라플 정기보험 [S12] | 만19세~70세 (순수보장형 10년만기 전기납: 남 33세~70세, 여 26세~70세) | 10/20/30년만기, 60/65/70/75/80/85/90세만기 | 20년납, 30년납, 60세납, 70세납, 전기납 | 월납 |
| 라이프플래닛e정기보험Ⅱ [S14] | not published on the retrieved page | 10/15/20년, 60/65/70/80세 | 5/10/15/20년, 55/60/65/70/80세 | 월납·연납·일시납 |
| 흥국생명 온라인정기보험 (비갱신형) [S6] | 만19세~60세 (60세만기 ~55세, 50세 제외; 80세만기 ~70세) | 20년, 60세만기, 80세만기 | 10년납, 20년납, 전기납 | 월납 |
| 흥국생명 온라인정기보험 (갱신형) [S6] | 최초계약 만19세~60세; 갱신계약 29세~79세 | 최초 10년만기; 갱신 1~10년만기 | 전기납 | 월납 |
| 푸본현대 원패스 정기보험 (갱신형) [S15] | 최초계약 20세~60세; 갱신계약 21세~64세 | 1년만기 | 전기납 | 월납·연납 |
| 미래에셋 헤리티지 정기보험 [S17] | 만15세~70세 (일반가입형); 30세~70세 (간편고지형); several cells start later for one sex | 80세만기, 90세만기 (만기환급형은 80세만기만) | 10년납, 15년납, 20년납, 전기납 | 월납 |
| 미래에셋 경영인을 위한 정기보험 [S18] | 일반가입형 남 20~70세, 여 38~70세; 간편고지형 남 30~70세, 여 38~70세 | 90세만기 only | 전기납 only | 월납 |

Observations a product spec has to answer to:

- **Minimum issue age.** Observed 만15세 [S10] [S17] to 30세 [S18 간편고지형]; the modal retail
  minimum is **만19세** [S1] [S6] [S11] [S12], with 20세 at 삼성생명 [S8] [S9] and 푸본현대
  [S15]. 만15세 is not accidental: 상법 제732조 makes a death contract on a life under 15 void
  [R4], so 15 is the statutory floor and two carriers sit exactly on it.
- **Maximum issue age.** Observed **60세** [S6] [S10] [S15] to **70세** [S11] [S12] [S17]
  [S18], with 64/65세 at 삼성생명 [S8] [S9] and 한화생명 [S1]. Nothing in this set issues above
  70.
- **Term menu.** From a single option (90세만기 only [S18]; 1년만기 only [S15]) to eleven
  (교보라플: three 년만기 and eight 세만기 [S12]). Every carrier that offers a menu offers
  **both** 년만기 and 세만기, and the 세만기 ceiling has crept up: 80세 was the old ceiling and
  **90세** [S12] [S17] and even **100세** [S1] are now on sale.
- **Premium-paying period.** 전기납 is available everywhere and is the disclosure's
  representative basis [S5]. Shortened-pay (10년납/20년납) is available almost everywhere; the
  widest menu is 신한라이프's, which reaches down to **5년납** and up to a **일시납** at
  80세만기 [S10]. KB's is the only one with a non-monthly frequency menu (3개월납·6개월납·연납)
  [S11]; every other retail product retrieved is **월납 only**.
- **The 최고가입나이 matrix is the real constraint, not the headline 가입나이.** 한화생명
  publishes it in full: for 순수보장형 남자, 10년납 gives a maximum issue age of
  49/54/55/60/65/65 at 60/65/70/80/90/100세만기, 20년납 gives 39/44/49/59/65/65, and 전기납
  gives 60 at 10년만기 and 50/55/55/60/65/**56** at the 세만기 options [S1]. The 56 at
  100세만기 전기납 (against 65 for a female life) is the sort of asymmetry that only a
  published matrix reveals.

### 4. Sum assured envelopes, units and banding

| Carrier | 가입한도 | 가입단위 | Notes |
|---|---|---|---|
| 한화생명 [S1] [S3] | 1,000만원 ~ 5억원 | not published | consumer page states 1천만~5억원 |
| 삼성 인터넷정기보험 [S8] | 5,000만원 ~ 3억원 | not published | 회사 기준에 따라 조정 가능 |
| 삼성 내리사랑정기보험 [S9] | 3,000만원 ~ 5억원 | not published | 고액할인 at ≥ 1억원 |
| 신한SOL정기보험 [S10] | 보험기간 10년 이하 3,000만~1억; 10년 초과 3,000만~3억 | not published | banded by term |
| KB 착한정기보험Ⅱ [S11] | 표준체 3,000만~5억; 비흡연체 5,000만~5억; 건강체 7,000만~5억; 슈퍼건강체 1억~5억 | not published | **minimum rises with the rate class** |
| 교보라플 정기보험 [S12] | 1억원 ~ 10억원 | 1,000만원 | highest retail ceiling in the set |
| 라이프플래닛e정기보험Ⅱ [S14] | 3천만원 ~ 5억원 | not published | |
| 흥국생명 온라인정기보험 [S6] | 1,000만원 ~ 2억원 | 1,000만원 | banded by 위험등급: 위험1급 1억, 위험2급 2억, 위험3·4급·비위험직 2억 |
| 푸본현대 원패스 [S15] | 100만원 ~ 1,000만원 | 100만원 | the 1년갱신 product |
| 미래에셋 헤리티지 [S17] | 일반가입형 2천만~2억; 간편고지형 2천만~1억 | not published | |
| 미래에셋 경영인 [S18] | 5천만원 ~ **30억원** | not published | corporate |

- Observed retail ceiling: **1,000만원 (₩10,000,000)** [S15] to **10억원 (₩1,000,000,000)**
  [S12]; the modal retail ceiling is **5억원 (₩500,000,000)**. The corporate ceiling is
  **30억원 (₩3,000,000,000)** [S18].
- Observed retail floor: **100만원** [S15] to **1억원** [S12]; the modal floor is **3,000만원
  (₩30,000,000)**.
- **KB's floor-by-rate-class rule is a genuine anti-selection control**: a 슈퍼건강체 policy
  cannot be written below 1억원, because the underwriting cost (a medical and a cotinine test)
  is only worth incurring above that size [S11].
- 흥국생명's 위험등급 banding is the only explicit **occupational-class** limit retrieved:
  위험1급 caps the sum assured at 1억, everything else at 2억 [S6].
- **건강진단 thresholds.** 흥국생명 publishes the age × amount grid at which a medical is
  required [S6]: 일반진단 20~39세 1.2억~3억, 40~49세 7천~2억, 50~54세 3천~1.5억, 55세이상
  1천~1억; 특별진단 A 3억~7억 / 2억~4억 / 1.5억~3억 / 1억~2억; 특별진단 B 7억초과 / 4억초과 /
  3억초과 / 2억초과. It also prints the 건강진단보험금산출기준 as 「일반사망보험금 [(주보험금 ×
  1) × 0.3]」. No other carrier publishes its non-medical limits; the rest say only that a
  건강진단 「기존 다른 보험상품의 가입유무, 나이, 청약서의 계약 전 알릴 의무 사항 등에 따라」
  may be required [S1] [S8] [S10] [S11] [S12] [S17].

### 5. The benefit definition, and how short it is

The main contract's benefit article is two lines. 한화생명's 만기환급형 주계약 약관 제4조,
verbatim [S2]:

> 제 4 조 보험금의 지급사유
> 회사는 피보험자에게 다음 중 어느 하나의 사유가 발생한 경우에는 보험수익자에게 약정한
> 보험금(별표 1 '보험금 지급기준표' 참조)을 지급합니다.
> 1. 보험기간이 끝날 때까지 살아 있을 경우: 만기보험금
> 2. 보험기간 중 사망한 경우: 사망보험금

The 순수보장형 주계약 약관 carries only limb 2. Termination is immediate and automatic [S2
제23조]: 「보험기간 중 피보험자에게 제4조(보험금의 지급사유) 제2호에서 정한 보험금의 지급사유가
발생한 경우에는 이 계약은 그때부터 효력이 없습니다.」

- **There is no Korean analogue of Japan's 高度障害保険金.** A Korean term policy does *not*
  pay the sum assured on a defined permanent-total-disability list. What the 장해 state does
  instead is trigger the **premium waiver** (§13). This is the single largest structural
  difference between `Term_KR_S` and `jplib`'s term chassis, and it simplifies the decrement
  model: there is one decrement to the benefit (death) and a second, smaller one that switches
  the premium off without terminating the contract.
- **Amounts.** 사망보험금 = 보험가입금액 [S1] [S8] [S10] [S11] [S12] [S17]. 만기보험금 = 「이미
  납입한 주계약 보험료의 100%」 [S1] [S8] [S17], and where the premium has been waived the
  maturity value is computed **as if the waived premiums had been paid**: 「보험료의 납입이
  면제된 경우 보험료 납입기간 종료일까지 보험료가 납입된 것으로 간주하여 만기보험금의 이미
  납입한 주계약 보험료를 계산합니다」 [S1] [S12].
- **What counts as 사망** [S2 제5조제2항]: death includes 실종선고 (deemed to occur when the
  court-recognised 실종기간 ends) and a 관공서 disaster notification (the date recorded in the
  가족관계등록부). And, expressly, a withdrawal of life-sustaining treatment under the
  연명의료결정법 does **not** affect the cause of death or the payment: 「연명의료중단등결정 및
  그 이행은…'사망'의 원인, '사망보험금' 지급에 영향을 미치지 않습니다」 [S2 제5조제3항].
- **Beneficiary default.** Where no 보험수익자 is named, the 만기보험금 goes to the 계약자 and
  the 사망보험금 to the 피보험자의 법정상속인 [S2 제12조].
- **Instalment settlement.** The 계약자 (or, after the event, the 보험수익자) may switch the
  death benefit between lump sum and instalments; deferred amounts accrue at the
  **평균공시이율** on an annual-compound basis, and accelerated amounts are discounted at the
  same rate [S2 제10조]. The 약관's worked example uses 평균공시이율 2.0% on a 9천만원 benefit
  split over three years: 3천만원 / 30,600,000원 / 31,212,000원, total 91,812,000원 [S2].
- **Claim timetable** [S2 제9조]: **3영업일** from receipt of complete documents; **10영업일**
  where investigation is needed; a 지급예정일 within **30영업일** except in six named cases
  (소송제기, 분쟁조정신청, 수사기관의 조사, 해외 보험사고 조사, the claimant refusing consent
  to enquiries, and referral to a third-party physician). Where the deadline will be missed the
  insurer must pay a **가지급보험금 of up to 50%** of its estimate on request. 해약환급금 is
  likewise payable within **3영업일** of claim [S2 제33조].

### 6. The published premium grids

This is the section the model's premium basis comes from.

#### 6.1 The cross-carrier disclosure — one basis, forty-five products

Basis, prescribed by [S5] and applying to every row: **남자/여자, 보험나이 40세, 보험기간 20년,
납입기간 전기납, 납입주기 월납, 보험가입금액 1억원 (₩100,000,000)**. Premiums are monthly, in
won. 확정이율 is the product's disclosed 적용이율. 보험가격지수 is defined in §12. Sorted by
male premium; retail 기본형 products first.

| 회사 | 상품명 | 남 | 여 | 확정이율 | 가격지수 남/여 | 해약환급금 | 갱신 | 채널 | 판매일자 |
|---|---|---|---|---|---|---|---|---|---|
| 신한라이프 | 신한SOL정기보험(무배당) | 14,400 | 7,900 | 2.10% | 82.0 / 83.1 | 순수보장 | 비갱신 | CM | — |
| 흥국생명 | (무)흥국생명 온라인정기보험_1종(비갱신형) | 15,000 | — | 2.75% | 84.8 / 74.5 | 순수보장 | 비갱신 | CM | 2026-02-08 |
| 교보라이프플래닛 | (무)교보라플 정기보험(해약환급금 미지급형, 표준체) | 15,080 | 8,010 | 2.50% | 88.1 / 85.5 | 순수보장 | 비갱신 | CM | — |
| 한화생명 | 한화생명 e정기보험 무배당[순수보장형] | 16,000 | 8,400 | 2.50% | 100.4 / 94.4 | 순수보장 | 비갱신 | CM | 2026-04-01 |
| 삼성생명 | 삼성 인터넷정기보험(2601)(무배당) 순수보장형 | 16,000 | 9,000 | 2.50% | 90.4 / 97.8 | 순수보장 | 비갱신 | CM | 2026-01-01 |
| KB라이프 | KB 착한정기보험Ⅱ 무배당 | 16,100 | 9,000 | 2.50% | 91.7 / 94.6 | 순수보장 | 비갱신 | CM | — |
| DB생명 | (무)e로운 장해Plus정기보험(2601) | 18,400 | 9,600 | 2.75% | 100.6 / 92.0 | 순수보장 | 비갱신 | CM | — |
| 푸본현대 | 푸본현대 정기보험 스마트픽 무배당(2604) | 20,360 | 11,710 | 2.60% | 115.9 / 122.6 | 순수보장 | 비갱신 | 대면 | — |
| 삼성생명 | 삼성 내리사랑정기보험(2501)(무배당,순수보장형) | 23,000 | 16,000 | 2.50% | 130.0 / 173.9 | 순수보장 | 비갱신 | 대면 | 2025-01-01 |
| 푸본현대 | ZERO 정기보험 무배당(2404) 순수보장형 | 28,000 | 17,000 | 2.60% | 146.0 / 158.3 | 순수보장 | 비갱신 | 대면 | — |
| 메트라이프 | 무배당 더해주고채워주는정기보험(간편가입형) | 29,000 | 22,000 | 2.30% | 163.9 / 239.1 | 순수보장 | 비갱신 | 대면 | — |
| NH농협생명 | 행복나눔NH정기보험(무배당)_2404 1종(순수보장형) | 30,690 | 20,790 | 2.50% | 175.2 / 228.2 | 순수보장 | 비갱신 | 대면·방카·TM | — |
| 푸본현대 | 푸본현대 정기보험 스마트픽 간편가입 무배당(2604) | 33,280 | 16,760 | 2.60% | 104.6 / 113.0 | 순수보장 | 비갱신 | 대면 | — |
| 처브라이프 | Chubb 간편가입 패밀리케어정기보험 무배당 | 50,000 | 45,000 | 2.50% | 125.6 / 122.3 | 순수보장 | 비갱신 | 대면 | — |
| 미래에셋생명 | 헤리티지 정기보험 무배당 [일반가입형/순수보장형] | 100,000 | 47,000 | 2.00% | 114.9 / 113.5 | 순수보장 | 비갱신 | 대면·기타 | — |
| DB생명 | (무)AI 라이프케어 정기보험(2606)(3종:표준체) | 109,200 | 55,800 | 2.75% | 166.9 / 195.6 | 순수보장 | 비갱신 | 대면 | — |
| 미래에셋생명 | 헤리티지 정기보험 무배당 [간편고지형/순수보장형] | 131,000 | 69,000 | 2.00% | 112.4 / 109.7 | 무진단무심사 | 비갱신 | 대면·기타 | — |
| KDB생명 | CEO 프리미엄 정기보험(간편심사)(기본형)(무) | 157,000 | 118,000 | 1.75% | 106.4 / 106.9 | 순수보장 | 비갱신 | 대면 | — |

Renewable rows (same 1억원 basis unless stated):

| 회사 | 상품명 | 남 | 여 | 확정이율 | 가격지수 남/여 | 갱신 |
|---|---|---|---|---|---|---|
| 흥국생명 | (무)흥국생명 온라인정기보험_2종(갱신형) 1형(기본형) | 9,000 | — | 3.00% | 72.8 / 74.4 | 갱신형 |
| 흥국생명 | 같은 상품, 2형(보장추가형) 재해사망보험금 | — | 6,000 | 3.00% | — | 갱신형 |
| 푸본현대 | 푸본현대 원패스 정기보험 무배당 갱신형(2404) *(1,000만원 기준)* | 900 | 560 | 2.60% | 113.0 / 96.8 | 갱신형 |

만기환급형 rows:

| 회사 | 상품명 | 남 | 여 | 확정이율 | 가격지수 남/여 |
|---|---|---|---|---|---|
| 한화생명 | 한화생명 e정기보험 무배당[만기환급형] | 114,000 | 60,400 | 2.50% | 100.6 / 95.7 |
| 교보라이프플래닛 | (무)교보라플 정기보험(만기환급형, 표준체) | 142,000 | 87,340 | 2.25% | 106.4 / 106.5 |
| 삼성생명 | 삼성 인터넷정기보험(2601)(무배당) 만기환급형 | 171,000 | 118,000 | 2.25% | 116.0 / 119.3 |
| 미래에셋생명 | 헤리티지 정기보험 무배당 [일반가입형/만기환급형] | 191,000 | 120,000 | 2.00% | 122.9 / 128.3 |

경영인정기보험 (체증형) rows — all 1억원, and note that these products are **90세만기 전기납
only**, so their disclosed figures cannot be on the 20-year basis of [S5]:

| 회사 | 상품명 | 남 | 여 | 확정이율 | 가격지수 남/여 | 해약환급금 |
|---|---|---|---|---|---|---|
| 교보생명 | 교보경영인정기보험 [2501](무배당) | 295,000 | 225,000 | 2.25% | 141.8 / 161.5 | 순수보장 |
| NH농협생명 | 행복한NH경영인정기보험(해약환급금 일부지급형)_2601 | 309,000 | 246,000 | 2.75% | 136.0 / 160.4 | 무해지/저해지 |
| NH농협생명 | 행복한NH경영인정기보험(표준형)_2502 | 321,000 | 253,000 | 2.75% | 137.5 / 159.5 | 순수보장 |
| 교보생명 | 교보간편경영인정기보험 [2501](무배당) | 360,000 | 288,000 | 2.25% | 127.1 / 145.6 | 순수보장 |
| 메트라이프 | 무배당 The Classic 경영인정기보험(저해약환급금형) | 367,000 | 269,000 | 2.50% | 99.9 / 107.6 | 무해지/저해지 |
| 미래에셋생명 | 경영인을 위한 정기보험 [해약환급금이 적은 유형] 일반가입형 | 430,000 | 251,000 | 2.50% | 121.5 / 104.2 | 무해지/저해지 |
| AIA생명 | (무) AIA 안심+ 경영인 정기보험 (해약환급금 일부지급형) 2형 | 450,000 | 292,000 | **4.00%** | 129.8 / 124.4 | 무해지/저해지 |
| KB라이프 | KB 경영인정기보험III 무배당(해약환급금 일부지급형)(일반심사형) | 479,000 | 409,000 | 2.70% | 133.6 / 168.8 | 순수보장 |
| 미래에셋생명 | 경영인을 위한 정기보험 [해약환급금이 적은 유형] 간편고지형 | 529,000 | 328,000 | 2.50% | 118.4 / 103.3 | 무해지/저해지 |
| 한화생명 | 간편가입 경영인H정기보험 무배당_2종(10%체증형, 일부지급형) | 551,000 | 396,000 | 2.50% | 159.6 / 168.8 | 순수보장 |
| KB라이프 | KB 경영인정기보험III 무배당(간편심사형) | 562,000 | 494,000 | 2.70% | 160.8 / 207.8 | 순수보장 |
| DB생명 | (무) 간편한 경영인 정기보험(일부지급형)(2601)(2형:10%체증형) | 613,800 | 470,700 | 2.50% | 168.8 / 190.1 | 무해지/저해지 |

Loan-linked rows, for completeness (not modelled): 삼성 상생금융 대출안심보험(2403)
1종(담보대출 플랜) 1억원 8,600 / 5,100 at 2.50%; 삼성 인생금융 대출안심보험(2403) 2종(신용대출
플랜) 1,000만원 4,090 / 4,120 at 2.50% [S4].

**What the table says.**

- The **retail 20-year level-term market clears in a narrow band**: eight carriers price a male
  40 at ₩100m between **14,400원 and 18,400원 a month**, a spread of 28% between the cheapest
  and dearest of the direct writers. The face-to-face products sit 40–90% above that band
  (23,000 / 28,000 / 30,690원) and the simplified-issue products above again (33,280 /
  50,000원). The channel, not the carrier, is the first-order price driver.
- **Female premiums run at 52–58% of male** on the same basis for the direct writers
  (7,900/14,400 = 54.9%; 8,010/15,080 = 53.1%; 8,400/16,000 = 52.5%; 9,000/16,000 = 56.3%;
  9,000/16,100 = 55.9%; 9,600/18,400 = 52.2%). The ratio widens sharply on the face-to-face and
  simplified products (16,000/23,000 = 69.6%; 45,000/50,000 = 90.0%), which is what a flat
  per-policy expense loading does to a small risk premium.
- **만기환급형 costs 7.1× to 9.4× the 순수보장형** on the same 20-year basis at the same
  carrier: 한화 114,000 / 16,000 = 7.13×; 교보라플 142,000 / 15,080 = 9.42×; 삼성 171,000 /
  16,000 = 10.69×; 미래에셋 191,000 / 100,000 = 1.91× (but on an 80세만기 basis, so not
  comparable). For a female life the multiple is higher still (60,400 / 8,400 = 7.19×; 87,340 /
  8,010 = 10.90×; 118,000 / 9,000 = 13.11×), because the savings element is the same size while
  the risk element is half. This ratio is the cleanest single statement of how little of a
  Korean term premium is risk premium.
- 미래에셋's retail rows and every 경영인 row are on a **90세만기 or 80세만기** contract, not a
  20-year one, so they are **not** like-for-like with the rest of the table however the
  disclosure presents them. [S5] prescribes a 20-year basis for 기본형 정기보험 but those
  products do not sell a 20-year term at all. This is a real limitation of the disclosure and
  is recorded again in the gaps section.
- 확정이율 (the disclosed 적용이율) ranges **1.75% to 3.00%** across retail products, and
  **4.00%** appears on one 경영인 row [S4]. See §11.

#### 6.2 한화생명 — 표준체 vs 건강체, ages 30/40/50, both sexes [S1]

순수보장형, 주계약 가입금액 1억원, **60세만기**, 전기납, 월납, 단위 원. Note the term length is
not constant down the column: for a 30-year-old this is a 30-year contract, for a 40-year-old a
20-year one, and for a 50-year-old a 10-year one.

| 나이 | 표준체 남 | 표준체 여 | 건강체 남 | 건강체 여 | 건강체 할인 남 | 여 |
|---|---|---|---|---|---|---|
| 30세 | 11,900 | 6,700 | 9,900 | 6,300 | −16.8% | −6.0% |
| 40세 | 16,000 | 8,400 | 13,200 | 7,900 | −17.5% | −6.0% |
| 50세 | 23,900 | 11,400 | 20,100 | 10,600 | −15.9% | −7.0% |

만기환급형, 주계약 가입금액 1억원, **65세만기**, 전기납, 월납 (35, 25 and 15 years of term
respectively):

| 나이 | 표준체 남 | 표준체 여 | 건강체 남 | 건강체 여 |
|---|---|---|---|---|
| 30세 | 53,600 | 29,400 | 45,900 | 27,600 |
| 40세 | 114,000 | 60,400 | 99,100 | 56,900 |
| 50세 | 475,900 | 274,100 | 434,400 | 259,800 |

The 만기환급형 row for age 50 is the diagnostic one: 475,900원 a month for fifteen years
returns 85,662,000원 of premium at maturity on a 1억원 sum assured. A return-of-premium term
over a short term is a savings contract with a small amount of insurance stapled to it, and the
premium says so.

#### 6.3 삼성생명 — 표준체 vs 슈퍼우량체, ages 20/30/40/50 [S8]

주보험(순수보장형) 1억, 20년만기, 20년납, 월납, 단위 원:

| 나이 | 표준체 남 | 표준체 여 | 슈퍼우량체 남 | 슈퍼우량체 여 | 할인 남 | 할인 여 |
|---|---|---|---|---|---|---|
| 20세 | 5,000 | 4,000 | 4,000 | 4,000 | −20.0% | 0.0% |
| 30세 | 8,000 | 6,000 | 5,000 | 5,000 | −37.5% | −16.7% |
| 40세 | 16,000 | 9,000 | 10,000 | 7,000 | −37.5% | −22.2% |
| 50세 | 35,000 | 17,000 | 24,000 | 13,000 | −31.4% | −23.5% |

This grid is on **exactly the disclosure basis** at age 40, and 16,000 / 9,000 reproduces the
[S4] row to the won. The rates are rounded to 1,000원, which limits what can be inferred about
a per-policy fee. The male 20 → 30 → 40 → 50 progression is 5,000 → 8,000 → 16,000 → 35,000,
i.e. roughly a doubling per decade from 30 onwards.

#### 6.4 KB라이프 — four rate classes, ages 30/40/50 [S11]

보험가입금액 1억원, **10년만기**, 전기납, 월납, 단위 원:

| | 표준체 | 비흡연체 | 건강체 | 슈퍼건강체 |
|---|---|---|---|---|
| 남 30세 | 5,700 | 4,800 | 4,100 | 3,600 |
| 남 40세 | 10,400 | 8,600 | 7,600 | 6,200 |
| 남 50세 | 23,800 | 20,300 | 17,700 | 14,300 |
| 여 30세 | 3,600 | 3,400 | 3,200 | 3,000 |
| 여 40세 | 6,400 | 6,200 | 5,800 | 5,500 |
| 여 50세 | 12,500 | 12,100 | 11,100 | 10,600 |

Maximum discount, 표준체 → 슈퍼건강체: male **−36.8% / −40.4% / −39.9%** at 30/40/50; female
**−16.7% / −14.1% / −15.2%**.

#### 6.5 교보라이프플래닛 — four rate classes × two product forms [S12]

순수보장형(해약환급금 미지급형), 1억원, 20년만기, 20년납, 월납, 단위 원:

| | 표준체(흡연) | 비흡연자 | 건강체 | 슈퍼건강체 |
|---|---|---|---|---|
| 남 30세 | 7,430 | 6,230 | 5,480 | 4,400 |
| 남 40세 | 15,080 | 13,040 | 11,500 | 8,840 |
| 남 50세 | 34,850 | 31,270 | 28,010 | 21,450 |
| 여 30세 | 4,580 | 4,360 | 4,120 | 3,880 |
| 여 40세 | 8,010 | 7,720 | 7,130 | 6,780 |
| 여 50세 | 15,590 | 15,170 | 13,740 | 13,100 |

만기환급형, same basis:

| | 표준체(흡연) | 비흡연자 | 건강체 | 슈퍼건강체 |
|---|---|---|---|---|
| 남 30세 | 82,640 | 72,560 | 66,140 | 56,770 |
| 남 40세 | 142,000 | 126,260 | 114,890 | 94,240 |
| 남 50세 | 271,640 | 250,870 | 231,500 | 189,420 |
| 여 30세 | 58,270 | 56,350 | 54,230 | 52,110 |
| 여 40세 | 87,340 | 85,020 | 80,140 | 77,210 |
| 여 50세 | 147,500 | 144,090 | 132,670 | 127,980 |

Every one of these sixteen 40-year-old cells appears **independently in the cross-carrier
disclosure** [S4] as its own product row (교보라플 정기보험 is disclosed once per rate class
per form), and the two sources agree exactly. Maximum discount 표준체 → 슈퍼건강체: male
**−40.8% / −41.4% / −38.5%** on 순수보장형 and **−31.3% / −33.6% / −30.3%** on 만기환급형;
female **−15.3% / −15.4% / −16.0%** and **−10.6% / −11.6% / −13.2%**.

#### 6.6 흥국생명 — 표준체 vs 우량체 (비흡연체), ages 30/40/50 [S6]

남자, **갱신형_기본형**, 10,000만원, 10년만기, 전기납, 월납, 단위 원:

| 나이 | 표준체 | 우량체 | 할인 |
|---|---|---|---|
| 30세 | 5,000 | 4,000 | −20.0% |
| 40세 | 9,000 | 8,000 | −11.1% |
| 50세 | 21,000 | 19,000 | −9.5% |

The 40세 표준체 figure of 9,000원 is the same number the disclosure gives for this product [S4]
and the same number the renewal projection [S7] uses as its 가입시 premium — three independent
appearances of one rate.

#### 6.7 교보라이프플래닛 라이프플래닛e정기보험Ⅱ — rate class and 만기환급률 [S14]

보험가입금액 1억원, 남자 40세, 20년만기, 전기납, 월납, 순수보장형:

| 등급 | 보험료 | 표준체 대비 |
|---|---|---|
| 표준체 | 17,000원 | — |
| 비흡연체 | 14,100원 | −17.0% |
| 건강체 | 12,600원 | −25.8% |
| 슈퍼건강체 | 9,700원 | −42.9% |

Same cell, varying only the 만기환급률 (표준체):

| 만기환급률 | 보험료 |
|---|---|
| 0% (순수보장형) | 17,100원 |
| 50% | 29,800원 |
| 100% (만기환급형) | 110,100원 |

The page prints **17,000원** in the rate-class block and **17,100원** in the 만기환급률 block
for what is described as the same 표준체 cell. The discrepancy is 0.6% and is recorded rather
than reconciled — see gaps. The 0% → 50% → 100% progression is strongly convex (17,100 → 29,800
→ 110,100), which is what a 만기환급률 above the natural reserve level does to a level premium.

#### 6.8 What can and cannot be inferred about a policy fee

Unlike `jplib`'s オリックス生命 grid, **no Korean grid in this set varies the sum assured**, so
the per-mille rate and any flat policy fee cannot be separated. Every published grid is
sum-assured-fixed and varies age, sex, rate class or product form instead. The one weak signal
is 흥국생명's female rows in [S4], where the 기본형 is simply not on sale to women and the
disclosure prints 0원 — a structural gap, not a price.

### 7. Rate classes — and the mechanic that has no analogue anywhere else in this repository

**The class definitions, verbatim.** Four carriers publish their criteria in full.

| Test | 교보라플 슈퍼건강체 [S12] | 교보라플 건강체 [S12] | KB 슈퍼건강체 [S11] | KB 건강체 [S11] | 한화 건강체 [S2] | 삼성 슈퍼우량체 [S8] | 흥국 우량체 [S6] | 삼성 우량체 [S9] |
|---|---|---|---|---|---|---|---|---|
| 흡연 | 평생 흡연한적 없음 | 평생 없거나 최근 1년 이상 금연 | 평생 흡연한적 없음 | 평생 없거나 1년이상 금연 | 최근 1년간 비흡연 | 최근 1년 이상 비흡연 | 직전 1년간 비흡연 | 1년이상 비흡연 |
| 수축기혈압 | < 120 mmHg | < 140 mmHg | < 120 mmHg | < 140 mmHg | ≤ 139 mmHg | < 120 mmHg | — | < 140 mmHg |
| 이완기혈압 | < 80 mmHg | < 90 mmHg | < 80 mmHg | < 90 mmHg | ≤ 89 mmHg | < 80 mmHg | — | < 90 mmHg |
| BMI (kg/m²) | 20.0 ≤ · < 25.0 | 18.5 ≤ · < 26.5 | 20.0 ≤ · < 25.0 | 18.5 ≤ · < 26.5 | 18.5 ≤ · < 25 | 20.0 ≤ · < 25.0 | — | 17 ~ 26 |
| 혈당 | 당뇨 진단이력 없음 & 혈당 < 110 ㎎/㎗ | — | 당뇨 유병이력 없음 & 공복혈당 < 110 mg/dL | 당뇨 유병이력 없음 | — | 공복혈당 < 100 mg/dL | — | — |
| 총콜레스테롤 | — | — | < 190 mg/dL | — | — | — | — | — |

- 교보라플 defines 당뇨 진단이력 exhaustively [S12]: 「1. 공복혈당이 126㎎/dL 이상인 사람
  2. 당뇨병 진단을 받은 사람 3. 혈당강하제 복용 또는 인슐린 주사를 사용하는 사람
  4. 당화혈색소 6.5% 이상인 사람」. That is the only HbA1c threshold in the set.
- Every carrier requires the life to be **만19세/20세 이상** to take a preferred class [S2
  건강체서비스특약Ⅱ 제3조] [S11] [S12], and to be acceptable **without** a 표준하체인수특약 /
  특별조건부인수특약 / 표준미달체조건부인수특약 — i.e. preferred classes are layered on top of
  standard acceptance, never used to rescue a substandard life [S2] [S11] [S12].
- Evidence is a 건강검진결과지 or a 방문진단; 교보라이프플래닛's consumer page adds that the
  검진결과지 must be **within 2 years** and the 흡연 검사(소변검사) **within 1 month** [S13].
  한화생명 offers the medical free through its call centre and returns the result by SMS
  **within 5 days** [S3].

**The mechanic with no analogue.** In `jplib`, メットライフ's rate class is fixed at issue and
carried unchanged through every renewal to 80 regardless of later health. In Korea the class is
a **rider that tracks the insured's smoking status for the life of the contract**. 한화생명's
건강체서비스특약Ⅱ 제4조, verbatim [S2]:

> ① 보험기간 중 피보험자가 계속하여 30일 이상 흡연을 한 경우에는 계약자 또는 피보험자는
> 지체 없이 회사에 이 사실을 서면으로 알리고 보험증권에 확인을 받아야 합니다.
> ② 회사는 제1항의 서면통지를 받은 날부터 1개월 이내에 …계산된 금액(이하 '정산차액')을
> 계약자가 추가 납입하도록 하며, 계약자는 …'건강체보험료'와 동일한 기준…으로 산출된
> …'표준체보험료'를 향후 납입보험료로 적용하고, 이 특약은 장래에 향하여 해지됩니다.
> ③ 계약자가 제2항에서 정한 정산차액 및 표준체보험료를 납입하지 않았을 경우 회사는
> 건강체보험료의 표준체보험료에 대한 비율에 따라 해당계약의 보험가입금액을 감액합니다.
> ④ 계약자 또는 피보험자가 정당한 이유없이 제1항의 통지의무를 30일 이상 지체하였을 경우에
> 회사는 보험금 지급사유의 발생 여부에 관계없이 그 사실을 안 날부터 1개월 이내에 제2항 및
> 제3항에 준용하여 보험가입금액을 감액하고 이 특약을 해지할 수 있습니다.
> ⑤ 해당계약의 보험기간 중 피보험자가 제3조…에서 정한 피보험자의 자격이 있고 계약자의
> 청약이 있을 때에는 회사는 …보장을 합니다. 이 경우 계약자는 청약한 날 이후의 해당
> 보험료부터 할인된 보험료를 납입하며, 보험료 변동시점의 계약자적립액을 정산한 잔여액이
> 있을 경우 회사는 이를 계약자에게 지급합니다.

So the class moves **in both directions during the term**: a smoker's relapse claws back the
discount already taken (정산차액) and reverts the premium, or reduces the sum assured in
proportion if the arrears are not paid; a standard life who quits and passes the tests may
**upgrade mid-term** and receive a refund of the excess reserve. KB and 교보라이프플래닛 make
the upgrade path explicit in the same way, by allowing a life originally accepted under a
특별조건부/표준미달체 rider to move into a preferred class once the health condition improves
[S11] [S12]. `Term_KR_S` does not model class movement, but the product spec has to say that
the Korean class is not a fixed attribute of the policy.

**Observed range of the maximum preferred discount** (표준체 → best class, male 40, on each
carrier's own published basis):

| Carrier | classes | male 40 discount | female 40 discount |
|---|---|---|---|
| 흥국생명 [S6] | 2 (표준체 / 우량체) | −11.1% | not published |
| 한화생명 [S1] | 2 (표준체 / 건강체) | −17.5% | −6.0% |
| 삼성 인터넷 [S8] | 2 (표준체 / 슈퍼우량체) | −37.5% | −22.2% |
| KB라이프 [S11] | 4 | −40.4% | −14.1% |
| 교보라플 [S12] | 4 | −41.4% (순수보장형) | −15.4% |
| 라이프플래닛e정기보험Ⅱ [S14] | 4 | −42.9% | not published |
| DB생명 AI 라이프케어 [S4] | 3 (표준체/건강체/슈퍼건강체) | −30.5% (109,200→75,900) | −21.5% (55,800→43,800) |

So the observed class count is **1 to 4** and the observed maximum male discount is **11% to
43%** — the same order as `jplib`'s 30–54% but reached with a narrower medical test set (no
cotinine assay is mentioned by any Korean carrier retrieved; 교보라이프플래닛's consumer page
mentions a 흡연 검사(소변검사) [S13] but the 상품요약서 does not [S12]).

**A second, unrelated discount is worth recording because it is genuinely novel.** 삼성생명's
**2형(걷기할인형)** applies where the life has used an approved step-counting app and achieved
**1일 8천보 이상을 20일 이상** in the calendar month before the application; the discount is
**10% of the 1형 영업보험료 for the first twelve premiums only**, after which the 1형 rate
applies [S8]. It is a first-year acquisition discount dressed as a wellness feature, and it is
the only behaviour-linked pricing in the retrieved set.

### 8. 갱신형 — renewal mechanics and attained-age repricing

**How a Korean renewal works.** Three carriers' rules, verbatim or close to it.

- **흥국생명** [S6]: 「(무)흥국생명 온라인정기보험 중 갱신형은 10년만기 갱신으로 운영하며,
  갱신일부터 최종 갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의
  보험기간 종료일까지 이 계약의 보험기간으로 합니다. 또한 갱신계약은 갱신일 현재의 보험료율을
  적용하며, 나이의 증가, 위험률의 변동 등의 사유로 최초계약 당시보다 인상될 수 있습니다.
  최종갱신계약의 보험기간 종료일은 80세까지로 합니다.」
- **푸본현대생명** [S15]: 「…보험계약자가 계약의 보험기간 종료일 15일전까지 갱신하지 않겠다는
  의사표시를 하지 않으면 갱신되며, 최대 4회(최초계약의 보험기간을 포함하여 최대 5년까지
  보장)까지 갱신 가능한 상품입니다. 갱신계약의 보험료는 갱신일 현재 피보험자의 나이에 따라
  계산하고, 보험나이증가, 기초율(적용이율, 계약체결비용, 계약관리비용 및 위험률) 등의 변동에
  따라 갱신시 보험료가 변동(특히, 인상)될 수 있습니다.」
- **삼성생명** (갱신형특약 on a 비갱신 정기보험 주계약) [S9]: 「갱신형특약은 보험계약자가
  특약의 보험기간 만료일 15일전까지 갱신하지 않겠다는 의사표시를 하지 않으면 갱신됩니다.
  갱신형특약은 특약별로 15년 단위로 갱신되며, 갱신시마다 보험나이 증가 및 기초율(적용이율,
  계약체결비용, 계약관리비용, 위험률) 등의 변동에 따라 갱신시 보험료가 변동(특히, 인상)될 수
  있습니다.」 Plus the warning 「보험료가 갱신됨에 따라 고령시점에 부담하는 보험료가 큰 폭으로
  인상될 수 있습니다.」

Assembling the common structure:

1. **Renewal is automatic and negative-option.** The contract renews unless the policyholder
   says otherwise; the notice period observed is **15일** [S9] [S15]. No carrier in this set
   requires a positive election. (Contrast `jplib`, where the notice period runs from 2 weeks
   to 2 months.)
2. **No 고지 and no underwriting at renewal.** Nothing in [S6], [S9] or [S15] conditions the
   renewal on health, a 계약 전 알릴 의무 or a 건강진단; the only conditions are the age and
   term ceilings. The 갱신계약's 가입나이 band in [S6] (29세~79세) exists to describe who *can
   be* in a renewed contract, not to re-underwrite them. **This is the defining feature of the
   Korean 갱신형 and the reason it is a real contract-boundary question under IFRS 17.**
3. **Repricing is at attained 보험나이, on the rate scale in force at the renewal date**, and
   every named basis element may move — 적용이율, 계약체결비용, 계약관리비용, 위험률 [S9] [S15]
   — not only mortality. So a renewal is repriced on the *whole* pricing basis, not just the
   age.
4. **The renewal is a new contract on a new product code.** 푸본현대 prints them separately:
   주계약 최초계약 `LO01011`, 갱신계약 `LO01012`; and for each 선택특약 likewise (암진단특약Ⅲ
   1046061 / 1046062; 뇌출혈진단특약Ⅲ 1045691 / 1045692; 급성심근경색증진단특약 1045681 / …)
   [S15]. 삼성 adds 「갱신형특약은 매 갱신시마다 갱신시점의 상품코드를 적용합니다」 [S9].
5. **Renewal cycle length varies by an order of magnitude**: **1년** [S15], **10년** [S6] [S13,
   unverified], **15년** [S9].
6. **The ceiling truncates rather than refuses.** Where the remaining run to the ceiling is
   shorter than a full cycle, the renewed term is cut to the remainder: 흥국 「갱신일부터 최종
   갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의 보험기간
   종료일까지」 [S6]; 삼성's 갱신형특약 the same at 15 years [S9].
7. **Observed ceiling: 80세** [S6]; **최대 5년 총 보장** [S15]; **주계약의 보험기간 만료일**
   for a 갱신 rider on a term chassis [S9].
8. **A premium waiver already running does not survive the renewal.** 흥국생명, verbatim [S6]:
   「피보험자가 50%이상 장해시 차회 이후의 보험료를 납입면제 해드립니다. 다만, 새로이 갱신되는
   계약에서는 갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를 적용하지 않고, 보험료를
   계속 납입하여야 합니다.」 This is a material cash-flow rule and the sharpest evidence that a
   Korean renewal really is a fresh contract: the disabled life must resume paying.

**The quantitative anchor — 흥국생명's 예상 갱신보험료 예시** [S7], verbatim. Basis:
2종(갱신형), 가입금액 10,000만원, 40세, 10년만기, 전기납, 월납, 1형(기본형) (단, 여자의 경우
2형(보장추가형)), 표준체.

| 구분 | 가입시 | 1회갱신 | 2회갱신 | 3회갱신 |
|---|---|---|---|---|
| 갱신시 나이 | 40세 | 50세 | 60세 | 70세 |
| 남자 | 9,000원 | 21,000원 | 56,000원 | 201,000원 |
| 여자 | 6,000원 | 10,000원 | 24,000원 | 103,000원 |

Index against the issue premium: male **1.00 → 2.33 → 6.22 → 22.33**; female **1.00 → 1.67 →
4.00 → 17.17**. The document's own caveat, verbatim: 「상기 예시는 최대갱신 가능 연령의
보험료를 포함하여 예시한 것으로 최초계약 가입 당시의 보험료율을 기준으로 산출(연령증가만
반영)하였으므로, 갱신시 보험료율이 변동될 경우 갱신시점의 보험료는 상기 예시와 크게 달라질 수
있습니다.」 — i.e. the path holds the rate scale frozen at its issue level and reflects **age
only**. A projection that also moved 위험률 and 적용이율 would differ.

**푸본현대's 1-year path** [S16], basis 보험가입금액 1,000만원, 남자 40세, 10년만기, 전기납
(the document's basis line says 10년만기 while the product is 1년만기 — see gaps):

| 구분 | 1회갱신 | 2회갱신 | 3회갱신 | 4회갱신 |
|---|---|---|---|---|
| 갱신시 나이 | 41세 | 42세 | 43세 | 44세 |
| 보험료 | 950원 | 990원 | 1,090원 | 1,180원 |

Against the 900원 issue premium disclosed for the same product at 1,000만원 [S4], the annual
step-ups are +5.6%, +4.2%, +10.1%, +8.3%.

**Renewable vs non-renewable at the same carrier.** 흥국생명 is the only carrier in this set
selling both forms of one product, so it is the only clean comparison available. On the
disclosure basis (male 40, 1억원): 비갱신형 20년만기 전기납 = **15,000원**; 갱신형 10년만기
전기납 = **9,000원** [S4] [S6]. The renewable form is **40% cheaper at issue** and, on its own
projection [S7], costs 21,000원 from age 50 — 40% *more* than the level 20-year premium — for
the second half of the same twenty years. Average monthly outlay over 20 years: level 15,000원;
renewable (9,000 × 120 + 21,000 × 120)/240 = **15,000원**. The two are, on the carrier's own
frozen-scale projection, almost exactly equivalent in undiscounted total cost over twenty years
— which is a clean way to say what the 갱신형 actually is: the same risk, financed differently,
with the repricing risk moved onto the policyholder.

### 9. 무해지환급형 / 저해지환급형 — the suppressed-surrender-value forms

**The clause, verbatim.** 한화생명 e정기보험 무배당[순수보장형] 주계약 약관 제33조 (해약환급금)
제2항 and its explanatory box [S2]:

> ② 회사는 '해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)' 계약이 보험료 납입기간 중
> 해지될 경우 해약환급금을 지급하지 않으며, 보험료 납입기간이 경과된 이후 해지될 경우
> '표준형' 해약환급금의 50%에 해당하는 금액을 지급합니다. 다만, 보험료 납입이 면제된 이후
> 보험료 납입기간이 경과되기 이전에 해지할 경우에는 해약환급금을 지급하지 않으며, 보험료
> 납입기간이 보험기간과 동일한 계약(이하 '전기납 계약'이라 합니다)의 경우에는 보험기간 중
> 계약이 해지될 경우 해약환급금을 지급하지 않습니다.
>
> 【'해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)'의 해약환급금에 관한 사항】
> 1. …보험료 납입기간 중 계약이 해지될 경우 해약환급금을 지급하지 않으며, 보험료 납입기간이
>    경과된 이후 해지될 경우 '표준형'의 해약환급금 대비 적은 해약환급금을 지급하는 대신
>    '표준형'보다 낮은 보험료로 가입할 수 있도록 한 상품입니다.
> 2. '표준형'은 보험료 및 해약환급금(환급률 포함)의 비교 안내만을 위한 상품으로 가입이
>    불가능하며, '표준형'의 해약환급금은 산출방법서에 정한 방법에 따라 계산한 금액으로
>    해지율을 적용하지 않고 계산합니다.
>
> ③ 제2항의 보험료 납입기간 중이라 함은 계약일로부터 보험료 납입기간이 경과하여 최초로
> 도래하는 계약해당일 전일까지의 기간을 말합니다. 다만, 보험료 납입기간 중 보험료 총액의
> 납입이 완료되지 않은 경우, 납입이 완료된 날의 전일까지를 보험료 납입기간으로 합니다.
> ④ 회사는 계약체결시 해약환급금 미지급형…상품과 표준형 상품의 보험료 및 해약환급금(환급률
> 포함) 수준을 비교∙안내하여 드립니다.

Five things follow that a model has to respect.

1. **The 표준형 is a phantom.** It cannot be bought — 「가입이 불가능」 — and exists only as
   the comparator the insurer must disclose. It is nonetheless a fully specified quantity: its
   해약환급금 is 「산출방법서에 정한 방법에 따라 계산한 금액으로 **해지율을 적용하지 않고**
   계산」. So the 표준형 CV is the ordinary net-premium reserve less the surrender charge, and
   the 무해지 CV is a *contractual override* of it, not a different reserve. 교보라이프플래닛
   uses exactly the same construction and the same phrase [S12], as does 미래에셋 for its
   기본형 [S18].
2. **On a 전기납 contract the 무해지 form has no surrender value at any time**, because the
   premium-paying period never ends before the term does [S2 제33조제2항 단서]. This is why
   한화생명's 해약환급금 예시 for 순수보장형 40세 60세만기 전기납 is **zero at every duration**
   (§10).
3. **The step-up at 납입완료 is 50% of the 표준형** at 한화생명 [S1] [S2] and at
   교보라이프플래닛 [S12], and **95% of the 기본형** at 미래에셋's 경영인 product [S18]. The
   FSC's 2021 measures contemplated a menu at 10 / 20 / 30 / 40 / 50% [R12].
4. **A waiver kills the step-up.** 「보험료 납입이 면제된 이후 보험료 납입기간이 경과되기
   이전에 해지할 경우에는 해약환급금을 지급하지 않으며」 [S2] — a life whose premiums have been
   waived and who then surrenders before the nominal 납입완료 date gets nothing, even though a
   paying policyholder at the same duration would get the 50%. Same rule at 교보라이프플래닛
   [S12].
5. **The 납입기간 중 window is defined to the day**, and it *shortens* if the premiums are paid
   up early [S2 제33조제3항]; the 약관's own example: 계약일 2018-09-01, 20년납 ⇒ 보험료
   납입기간 중 = 2018-09-01 ~ 2038-08-31.

**The multi-step form.** 미래에셋's 경영인 product is the only three-step schedule retrieved
[S18]: 「계약일부터 3년 경과시점 계약해당일의 전일까지는…해약환급금을 지급하지 않고,
계약일로부터 3년 경과시점 계약해당일부터 5년 경과시점 계약해당일의 전일까지는…[기본형]의
해약환급금의 **30%**를 지급합니다. 다만, 5년 경과시점 계약해당일 이후에 계약이 해지될 경우에는
[기본형]의 해약환급금의 **95%**를 지급합니다.」 The same product carries a **해약환급금
중도지급옵션**: after seven years the policyholder may, up to **twelve times a policy year**
and with the insurer's consent, draw part of the surrender value, the 해지가입금액 being
deducted from the sum assured [S18].

**What the suppression is worth in premium.** Three independent measurements, and they differ
by an order of magnitude:

| Basis | 무해지/저해지 | 표준형/기본형 | Saving |
|---|---|---|---|
| 교보라플, 남 40세, 1억원, 20년만기, 20년납 [S12] | 15,080원 | 15,320원 | **−1.57%** |
| 교보라플, 여 40세, 1억원, 20년만기, 20년납 [S12] | 8,010원 | 8,120원 | **−1.35%** |
| 한화생명, 남 40세, 1억원, **100세만기**, 전기납 [S3] | — | — | **−14%** (as stated) |
| FSC illustration, 납입완료 후 환급 50% vs 100% [R12] | 24,000원 | 32,100원 | **−25.2%** |

The reason the term product's saving is so small is structural and worth stating in the product
spec: **on a twenty-year level term the 표준형 reserve is itself tiny**, peaking around a third
of cumulative premiums and running to zero at maturity (§10), so suppressing it releases almost
nothing. On a 100세만기 contract — which is a whole-life contract wearing a term product's name
— the reserve is large and the saving is real. The 무해지 form is therefore a *savings-product*
device that has been carried across to term, and its economics on term are marginal. That is a
finding, not an aside: it is why 한화생명 quotes its 14% headline on a 100세만기 basis and not
on the disclosure's 20-year one.

**The FSC's 2021 illustration** [R12], reproduced verbatim — premium against the
post-completion surrender-value level, on an unstated product basis:

| 납입완료 후 해지환급금 | 10% | 20% | 30% | 40% | 50% | 표준형(100%) |
|---|---|---|---|---|---|---|
| 보험료 (원) | 26,400 | 25,200 | 24,300 | 24,000 | 24,000 | 32,100 |

Two features matter. The saving is **not linear in the suppressed value** — it saturates by the
30–40% step, and 40% and 50% price identically. And the whole span from 10% to 50% is worth
only 2,400원 out of 32,100원, while the step from 표준형 to *any* suppressed form is worth
between 5,700원 and 8,100원. The pricing gain is in **applying a 해지율 at all**, not in how
deep the suppression goes.

**Market scale.** 무·저해지 신계약건수 went ('16) 30.4만건 → ('18) 171.7만건 → ('20) 443.5만건,
and 신계약비중 1.4% → 6.8% → 14.7%, with 2021 Jan–Aug at 279.8만건 and 13.7% [R12]. No
term-specific split was retrieved. In the current disclosure only **6 of the 45 정기보험 rows**
are flagged 무해지/저해지환급, and **all six are 경영인정기보험** [S4]; every retail 순수보장형
row is flagged 순수보장, including 교보라플's 해약환급금 미지급형 and 한화생명's 해약환급금
미지급형 forms. That is a **disclosure-taxonomy artefact, not a product fact** — the 해약환급금
column carries the product's headline 환급 type (순수보장 / 만기환급 / 무해지·저해지환급 /
무진단무심사), and a 순수보장 term product whose surrender value is suppressed is still tagged
순수보장. Recorded here so that a later reader does not mistake the column for a census of
무해지 term.

### 10. Surrender-value curves, as published

Every 상품요약서 must print a 해약환급금 예시. These are the **shape** evidence for the model's
reserve, and they are the only published reserve data in the Korean retail market.

**(a) 표준형-equivalent 순수보장형, male 40, ₩100m, 20-year term.** The classic term reserve:
nil for the first year, a peak near duration 5–7 at 33–46% of premiums paid, then a run-off to
exactly zero at maturity.

| 경과 | 흥국 남 [S6] | 흥국 여 [S6] | 삼성 인터넷 남 [S8] | 삼성 내리사랑 남 [S9] | 교보라플 표준형 남 [S12] | 신한 기본형 남 [S10] |
|---|---|---|---|---|---|---|
| 월납보험료 | 15,000 | 8,000 | 16,000 | 23,000 | 15,320 | 14,400 |
| 3개월 | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% | 0.0% |
| 6개월 | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% | 0.0% |
| 9개월 | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% | 0.0% |
| 1년 | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% | 4.0% |
| 2년 | 28.9% | 3.2% | 20.3% | 0.0% | 23.20% | 31.9% |
| 3년 | 38.8% | 17.4% | 27.9% | 0.0% | 31.42% | 40.6% |
| 5년 | 45.1% | 27.7% | 33.4% | 9% | 36.73% | 45.8% |
| 7년 | 45.6% | 31.1% | — | — | 37.25% | 45.6% |
| 10년 | 39.4% | 27.0% | 30.3% | 21% | 32.36% | 38.9% |
| 15년 | 24.1% | 16.4% | 18.7% | 13% | 19.57% | 23.0% |
| 20년 | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% | 0.0% |

(흥국's female column is on the 보장추가형; 삼성 내리사랑's basis is 전기납; 교보라플's column
is the phantom 표준형 comparator; 신한's is 20년납. Percentages are 환급률 = 해약환급금 ÷
누적납입보험료 as each document prints them.)

신한라이프's table is the only annual one, and is worth having in full — male, 주계약 1억원,
40세, 20년만기, 20년납, 월납 [S10]: 1년 7,057원 (4.0%); 2년 110,414 (31.9%); 3년 210,871
(40.6%); 4년 306,529 (44.3%); 5년 395,786 (45.8%); 6년 477,943 (**46.0%**, the peak); 7년
552,400 (45.6%); 8년 603,900 (43.6%); 9년 644,500 (41.4%); 10년 673,100 (38.9%); 15년 597,400
(23.0%); 20년 0 (0.0%). Female on the same basis: 0 at 1년; 21,229 (11.1%); 68,043 (23.9%);
112,457 (29.6%); 153,871 (32.4%); 191,786 (33.7%); 226,100 (**34.0%**); 245,700 (32.3%);
261,000 (30.5%); 271,700 (28.6%); 15년 239,900 (16.8%); 20년 0.

Note the **absolute** value peaks later than the ratio: 신한's male 해약환급금 peaks at
673,100원 at duration 10 while the 환급률 peaks at duration 6. A model that checks its reserve
against these tables must compare the amount, not the ratio.

**(b) 무해지 (해약환급금 미지급형) vs its 표준형 comparator, side by side** — 교보라플, 1억원,
표준체, 40세 가입, 20년만기, 20년납, 월납, 단위 원 [S12]:

| 경과 | 미지급형 납입보험료 | 미지급형 환급금 | 지급형 납입보험료 | 지급형 환급금 | 지급형 환급률 |
|---|---|---|---|---|---|
| 3개월 | 45,240 | — | 45,960 | — | 0.00% |
| 1년 | 180,960 | — | 183,840 | — | 0.00% |
| 2년 | 361,920 | — | 367,680 | 85,300 | 23.20% |
| 3년 | 542,880 | — | 551,520 | 173,270 | 31.42% |
| 4년 | 723,840 | — | 735,360 | 258,060 | 35.09% |
| 5년 | 904,800 | — | 919,200 | 337,600 | 36.73% |
| 7년 | 1,266,720 | — | 1,286,880 | 479,350 | 37.25% |
| 10년 | 1,809,600 | — | 1,838,400 | 594,900 | 32.36% |
| 15년 | 2,714,400 | — | 2,757,600 | 539,630 | 19.57% |
| 20년 | 3,619,200 | — | 3,676,800 | — | 0.00% |

Monthly premiums 15,080원 (미지급형) against 15,320원 (지급형). The female table is on the same
pattern: 8,010원 against 8,120원, with the 지급형 peaking at 28.82% at duration 7 [S12].

**(c) 무해지 on a 전기납 contract — nil throughout.** 한화생명, 순수보장형(해약환급금
미지급형), 주계약 1억원, 40세, 60세만기, 전기납, 월납, 표준체 [S1]: male 납입보험료 48,000원 at
3개월 rising to 3,840,000원 at 20년, 해약환급금 **"–" and 환급률 0.0% at every one of the
eleven durations shown**; female 25,200원 to 2,016,000원, likewise all zero. This is the
제33조제2항 단서 in numbers.

**(d) 만기환급형.** 한화생명, 주계약 1억원, 40세, 65세만기, 전기납, 월납, 표준체, male (월납
114,000원) [S1]: 3개월 342,000 → 255,500 (74.7%); 6개월 77.7%; 9개월 78.7%; 1년 79.2%; 2년
80.6%; 3년 81.6%; 5년 83.4%; 7년 85.1%; 10년 87.6%; 15년 91.8%; 20년 96.0%; **25년 34,200,000 →
34,200,000 (100.0%)**. Female (월납 60,400원): 72.7% at 3개월 rising to 100.0% at 25년. The
약관's note 4: 「만기환급형의 경우 만기시점의 해약환급금은 만기보험금이 포함된 금액입니다」
[S1]. 삼성's 만기환급형, 1억원, 표준체 남 40세, 20년만기, 전기납, 월납 (월납 171,000원) [S8]:
0.0% at 3개월 and 6개월, then 25.8% / 41.6% / 66.2% / 75.0% / 83.1% / 90.4% / 95.1% / 100.0% at
9개월 / 1년 / 2년 / 3년 / 5년 / 10년 / 15년 / 20년.

The two 만기환급형 shapes are quite different — 한화's starts at 74.7% of a small cumulative
premium and creeps to 100%, 삼성's starts at 0% and climbs steeply — which is a
surrender-charge-amortisation difference, not a reserve difference.

**(e) 갱신형.** 흥국생명, 최초계약 1억원, 40세, 10년만기, 전기납, 월납, 표준체 [S6]: male (월납
9,000원) 0.0% at 3/6/9개월; **0.1% at 1년**; 15.5% at 2년; 19.1% at 3년; 18.4% at 5년; 13.4% at
7년; **0.0% at 10년**. Female on 보장추가형 (월납 6,000원): nil to 2년, then 4.9% / 7.8% / 6.9%
/ 0.0%. A ten-year renewable term therefore builds and unwinds a reserve **inside each cycle**
and hands the policyholder nothing at the renewal date. Modelling a 갱신형 as a single long
contract would misstate this completely.

**(f) KB's early-duration shape is different from everyone else's.** KB 착한정기보험Ⅱ, 1억원,
40세, 60세만기, 20년납, 월납, 표준체 [S11]: male 3월 0.0%; **6월 9,200원 (9.5%)**; 9월 35,950
(24.8%); 1년 62,700 (**32.5%**); 2년 166,000 (43.0%); 3년 264,900 (45.7%). Female: 3월 0.0%;
6월 1,450 (2.7%); 9월 14,525 (17.9%); 1년 27,600 (25.6%); 2년 78,000 (36.1%). Where every other
carrier pays nothing for a full year, KB is paying a quarter to a third of premiums back at
duration 1. That is a different 해약공제 amortisation, and it is the widest cross-carrier
variation in the whole file.

### 11. The pricing basis, as disclosed

Korean 상품요약서 are required to print the 적용이율, the 적용위험률 at three ages, and — where
a 해지율 is used in pricing — the 적용해지율. That is more disclosure of the pricing basis than
any other market in this repository offers for a protection product.

**적용이율 (the pricing interest rate), 연복리:**

| Carrier / product | 적용이율 |
|---|---|
| KDB생명 CEO 프리미엄 정기보험 [S4] | 1.75% |
| 미래에셋생명 헤리티지 정기보험 [S17] | 2.00% |
| 삼성 내리사랑정기보험, 갱신형(재가입형 포함) 특약 [S9] | 2.00% |
| 신한SOL정기보험 [S10] | 2.10% |
| 삼성 인터넷정기보험 만기환급형 [S8]; 교보라플 만기환급형 [S12]; 교보경영인정기보험 [S4] | 2.25% |
| 메트라이프 더해주고채워주는정기보험 [S4] | 2.30% |
| 한화생명 e정기보험 [S1]; 삼성 인터넷정기보험 순수보장형 [S8]; 삼성 내리사랑 주보험 [S9]; KB 착한정기보험Ⅱ [S11]; 교보라플 순수보장형 [S12] | 2.50% |
| 푸본현대 (three products) [S4] | 2.60% |
| KB 경영인정기보험III [S4] | 2.70% |
| 흥국생명 온라인정기보험 비갱신형 [S6]; DB생명 (two products) [S4] | 2.75% |
| 흥국생명 온라인정기보험 갱신형 [S4] | 3.00% |
| AIA 안심+ 경영인 정기보험 2형 [S4] | 4.00% |

Observed range **1.75% – 4.00%**; the retail mode is **2.50%**. Two internal patterns are
consistent across carriers: the **만기환급형 is priced at a lower 적용이율 than the 순수보장형
of the same product** (삼성 2.25% vs 2.50% [S8]; 교보라플 2.25% vs 2.50% [S12]) — because the
savings element carries a longer duration and a tighter guarantee — and a **갱신형 or
갱신형특약 is priced at a different rate again** (흥국 3.00% renewable vs 2.75% non-renewable
[S4] [S6]; 삼성 2.00% for 갱신형특약 vs 2.50% for the 주보험 [S9]).

한화생명 states the concept in the standard words [S1]: 「보험료를 납입하는 시점과 보험금 지급
사이에는 시차가 발생하므로 이 기간 동안 기대되는 수익을 미리 예상하여 일정한 비율로 보험료를
할인해 주는데, 이 할인율을 보장부분 적용이율이라고 합니다.」 It is a **pricing** rate; it is
not the 공시이율 (there is none on a protection product), and no carrier discloses a
최저보증이율 for 정기보험 — the disclosure's 최저보증 columns are empty for every 정기보험 row
[S4].

**적용위험률 — 무배당 예정 경험사망률, annual q at ages 20 / 40 / 60:**

| Carrier | 남 20 | 남 40 | 남 60 | 여 20 | 여 40 | 여 60 |
|---|---|---|---|---|---|---|
| 미래에셋생명 [S17] | 0.000210 | 0.000480 | 0.002710 | 0.000170 | 0.000360 | 0.001380 |
| 신한라이프 [S10] | 0.000278 | 0.000708 | 0.003703 | 0.000176 | 0.000491 | 0.001660 |
| 교보라이프플래닛 [S12] | 0.000280 | 0.000650 | 0.003390 | 0.000200 | 0.000430 | 0.001390 |
| 삼성생명 [S8] | 0.000290 | 0.000830 | 0.003500 | 0.000220 | 0.000520 | 0.001640 |
| 흥국생명 [S6] | 0.000310 | 0.000510 | 0.003940 | 0.000230 | 0.000310 | 0.001610 |
| 한화생명 [S1] | 0.000320 | 0.000850 | 0.003770 | 0.000200 | 0.000500 | 0.001500 |
| KB라이프 [S11] | 0.000336 | 0.000839 | 0.004165 | 0.000235 | 0.000540 | 0.002035 |

Observed spread at male 40: **0.000480 to 0.000850**, a factor of **1.77**. At female 40:
0.000310 to 0.000540, a factor of 1.74. At male 60: 0.002710 to 0.004165, a factor of 1.54.
Male 40 / female 40 ratio by carrier: 1.33 (미래에셋), 1.44 (신한), 1.51 (교보라플), 1.60
(삼성), 1.65 (흥국·1.65 KB), 1.70 (한화). The rates are **carrier-specific adjustments of the
보험개발원 참조순보험요율**, not a common table — which is exactly the opposite of Japan, where
every carrier prices off the same publicly downloadable 標準生命表.

**Rate-class mortality.** Two carriers publish a full table per class.

| 교보라플 [S12] | 남 20 | 남 40 | 남 60 | 여 20 | 여 40 | 여 60 |
|---|---|---|---|---|---|---|
| 무배당 (표준체) | 0.000280 | 0.000650 | 0.003390 | 0.000200 | 0.000430 | 0.001390 |
| 비흡연자 | 0.000233 | 0.000538 | 0.002993 | 0.000187 | 0.000411 | 0.001347 |
| 건강체 | 0.000201 | 0.000470 | 0.002642 | 0.000180 | 0.000390 | 0.001218 |
| 슈퍼건강체 | 0.000196 | 0.000379 | 0.002003 | 0.000173 | 0.000368 | 0.001166 |

| KB라이프 [S11] | 남 20 | 남 40 | 남 60 | 여 20 | 여 40 | 여 60 |
|---|---|---|---|---|---|---|
| 예정 경험사망률 (표준체) | 0.000336 | 0.000839 | 0.004165 | 0.000235 | 0.000540 | 0.002035 |
| 비흡연자 | 0.000285 | 0.000689 | 0.003601 | 0.000222 | 0.000520 | 0.001979 |
| 우량체II | 0.000248 | 0.000597 | 0.003166 | 0.000213 | 0.000490 | 0.001791 |
| 초우량체 | 0.000243 | 0.000501 | 0.002519 | 0.000205 | 0.000465 | 0.001729 |

Best-class to standard-class mortality ratio at male 40: **0.583** (교보라플) and **0.597**
(KB) — i.e. the assumed mortality saving is around **41%**, which lines up closely with the
observed male-40 premium discounts of 41.4% and 40.4% (§7). Female at 40: **0.856** and
**0.861**, against premium discounts of 15.4% and 14.1% — so for a female life the premium
discount is *smaller* than the mortality saving would justify, because the fixed expense
loading is a larger share of a small premium.

**예정 재해사망률** (accidental-death, annual q), published by two carriers:

| Carrier | 남 20 | 남 40 | 남 60 | 여 20 | 여 40 | 여 60 |
|---|---|---|---|---|---|---|
| 흥국생명 [S6] | 0.000097 | 0.000110 | 0.000355 | 0.000042 | 0.000035 | 0.000086 |
| 신한라이프 [S10] | 0.000097 | 0.000121 | 0.000332 | 0.000042 | 0.000033 | 0.000084 |

These two carriers agree to three significant figures at male 20 and female 20 and are within
10% everywhere — strong evidence that both are using the **보험개발원 참조 재해사망률** almost
unadjusted, in contrast to the all-cause rates above. 신한 names the source documents:
경험사망률 「보험개발원 생명장기 제2024-0250호(2024.01.23.)」 and 재해사망률 「보험개발원
생명장기 제2023-2072호(2023.12.06.)」 [S10] [R19]. Accidental death is **3–4% of all-cause
mortality at male 60 and 15–25% at male 20** on these tables, which is the right order for a
doubled-benefit rider to be cheap.

**적용해지율 (the pricing lapse rate) — disclosed only where a 무해지 form is sold:**

- 한화생명, 10년납 basis, 해약환급금 미지급형(납입기간중 0%, 납입기간후 50%) [S1]: 「납입기간
  이내에 대하여 경과기간별로 **연 0.1%~8.4%**, 납입기간 이후에 대하여 경과기간별로 **연
  0.8%**이며, '표준형'에는 적용해지율이 적용되지 않습니다.」
- 교보라이프플래닛, 10년납 basis, 해약환급금 미지급형 [S12]: 「납입기간 이내에 대하여
  경과기간별로 **연 0.1% ~ 4.6%**, 납입기간 이후에 대하여 경과기간별로 **연 0.7% ~ 1.6%**이며,
  …만기환급형에는 적용해지율이 적용되지 않습니다.」

Both start at **0.1%** and 한화's post-completion rate is **0.8%** — which are precisely the
convergence point and the terminal rate the 2024 IFRS17 계리가정 가이드라인 prescribes:
로그-선형 원칙모형 with 「수렴점 0.1%」 and 「완납 후 최종해지율 0.8%」 [R13]. The chain from
supervisory guideline to disclosed pricing parameter is therefore **complete and verifiable**,
and it is the single most useful thing in this file for setting `Term_KR_S`'s lapse basis.

Note what the disclosure does **not** say: the 적용해지율 is the rate used **in pricing the
무해지 form**, which is deliberately conservative (low), and is not the carrier's best-estimate
lapse experience. Actual short-payment 저해지 종신 experience has run at **49.8% cumulative
over three years against a 28.5% assumption** [R18] — a whole-life datum, but the direction of
the error is the point.

**계약체결비용 및 계약관리비용.** Every 상품요약서 defines these — 「보험회사가 보험계약의
체결, 유지 및 관리 등에 필요한 경비로 사용하기 위하여 보험료 중 일정비율을 책정한 것」 [S1]
[S6] [S8] [S10] [S11] [S12] — and **not one of them publishes a rate**. The expense basis has
to be inferred from the 보험가격지수 (§12) or standardised. `[std]` territory.

**계약자배당.** Every product in this file is **무배당**: 「이 계약은 무배당보험이므로 계약자
배당금이 없습니다」 [S2 제35조], and the same sentence in every 상품요약서 [S1] [S6] [S8] [S9]
[S10] [S11] [S12] [S15] [S17] [S18]. No 유배당 정기보험 appears anywhere in the 45-product
disclosure [S4]. This is a cleaner position than Japan's, where 日本生命's term product is
still 有配当.

### 12. 보험가격지수 — a published expense-and-margin ratio

Korea publishes, per product and per sex, a **보험가격지수**: the ratio of the product's total
premium to the sum of a 참조순보험료 총액 and an industry-average 평균사업비 총액. 한화생명's
definition, verbatim [S1]:

> 해당 상품의 보험료총액(보험금 지급을 위한 보험료 및 보험회사의 사업경비 등을 위한 보험료)을
> "참조순보험료 총액"과 "평균사업비 총액"을 합한 금액으로 나눈 비율을 "보험가격지수"라고
> 합니다. 보험가격지수는 '생명보험 상품공시 시행세칙'에서 정한 기준에 따라 작성되었습니다.
> ※ 참조순보험료 총액 : 금융감독원장이 정하는 바에 따라 산정한 전체 보험회사 공시이율의
> 평균(평균공시이율), 평균해지율 및 참조순보험요율을 적용하여 산출한 보험금 지급을 위한 보험료
> ※ 평균사업비 총액 : 상품군별 생명보험상품 전체의 평균 사업비율을 반영하여 계산(역산)한 값

100% therefore means "priced at the industry-average net premium plus the industry-average
expense loading". Observed values on the 정기보험 disclosure basis [S4], male/female:

- Cheapest retail: 신한SOL 82.0 / 83.1; 흥국 비갱신 84.8 / 74.5; 교보라플 미지급형 표준체 88.1
  / 85.5; 삼성 인터넷 순수보장형 90.4 / 97.8; KB 착한 91.7 / 94.6.
- Around par: 한화 e정기보험 순수보장형 100.4 / 94.4 and 만기환급형 100.6 / 95.7; DB e로운
  장해Plus 100.6 / 92.0; 메트라이프 The Classic 경영인 99.9 / 107.6.
- Expensive: 삼성 내리사랑 130.0 / 173.9; 푸본현대 ZERO 146.0 / 158.3; 메트라이프 간편가입
  163.9 / **239.1**; NH 행복나눔 175.2 / **228.2**; DB AI 라이프케어 표준체 166.9 / 195.6; KB
  경영인III 간편심사형 160.8 / 207.8.
- 교보라플's rate classes span **51.6 to 106.4** on one product, because the index is computed
  against a 참조순보험료 that does not know about preferred underwriting; the 슈퍼건강체 form's
  51.6 (남) is the lowest number in the whole 정기보험 table [S4].

한화생명 publishes its own index with its exact basis [S1]: 40세, 60세만기, 전기납, 순수보장형
표준체 → 남 100.4% / 여 94.4%, 가입금액 10,000만원; and 65세만기, 만기환급형 표준체 → 남 100.6%
/ 여 95.7%. 흥국생명 publishes an eight-cell grid across 비갱신/갱신 × 기본형/보장추가형 ×
표준체/우량체, at 40세, 최초계약 [S6]: 비갱신형 기본형 60세 전기납 84.8/76.1 (표준체) and
73.5/65.2 (우량체); 갱신형 기본형 10년 전기납 72.8/62.0 (both classes). 삼성 내리사랑 publishes
130 / 173.9 at 40세, 20년, 20년, 1억원, 표준체, 월납 [S9].

Two uses for the library. First, the index is the **only published handle on the expense
loading**: an index of 100% with a known 참조순보험료 would pin the total expense load, and
even without the 참조순보험료 the *dispersion* (82% to 239%) bounds what a `[std]` expense
basis may plausibly assume. Second, it is a direct measure of the **channel effect** identified
in §6: every CM (online) product sits between 72% and 101%, and every 대면 (face-to-face)
retail product sits between 104% and 239%.

### 13. 보험료 납입면제 (waiver of premium)

**The trigger is identical at every carrier in the set**, and is a 50%-plus disability, not an
accident test. 한화생명's 주계약 약관 제5조제1항, verbatim [S2]:

> ① 보험료 납입기간 중 피보험자가 장해분류표(별표 4 참조) 중 동일한 재해 또는 재해이외의
> 동일한 원인으로 여러 신체부위의 장해지급률을 더하여 50% 이상인 장해상태가 되었을 경우에는
> 차회 이후의 보험료 납입을 면제하여 드립니다. 보험료의 납입이 면제된 경우 보험료 납입기간
> 종료일까지 보험료가 납입된 것으로 간주하여 만기보험금의 이미 납입한 주계약 보험료를
> 계산합니다.

The same sentence, to the word, appears in [S1] [S6] [S8] [S9] [S10] [S11] [S12]. Key features:

- **Cause-neutral**: 「동일한 재해 또는 재해이외의 동일한 원인으로」 — sickness qualifies
  equally with accident. Only 미래에셋's 간편고지형 rider narrows it to accident alone (「재해
  50% 장해 납입면제형」) [S17] [S18].
- **Additive across body parts**, subject to the 장해분류표's own combination rules [S2 제5조
  제9항]: separate disabilities from one cause are added; two disabilities in the *same* body
  part take the higher rate, not the sum.
- **Determination at 180 days**: 「장해지급률이 재해일 또는 질병의 진단 확정일부터 180일 이내에
  확정되지 않은 경우에는 재해일 또는 진단 확정일부터 180일이 되는 날의 의사 진단에 기초하여
  고정될 것으로 인정되는 상태를 장해지급률로 결정합니다」, with a look-back window if the state
  worsens later — **2년** where the term is 10 years or more, **1년** where it is shorter [S2
  제5조제4항·제5항].
- **A temporary disability lasting 5 years or more counts at 20% of its rate** [S2 제5조제8항].
- Effect: 「차회 이후의 보험료 납입을 면제」 — future premiums only, no refund of past ones. On
  a 만기환급형 the maturity benefit is computed **as if they had been paid** [S1] [S2] [S8]
  [S12] [S17].
- **The waiver is switched off by the same three intent limbs as the death benefit** [S2
  제6조]: 「…보험금을 지급하지 않으며 보험료의 납입면제 사유가 발생한 때에는 납입을 면제하지
  않습니다.」
- **It does not survive a renewal** [S6] — see §8.
- **It kills the 무해지 step-up** [S2 제33조제2항 단서] [S12] — see §9.

**Optional waiver riders.** 교보라이프플래닛 sells a five-way 무배당 보험료납입면제보장특약
whose triggers are diagnosis-based rather than disability-based [S12]: 1종 (일반암, 뇌출혈,
급성심근경색증), 2종 (뇌출혈, 급성심근경색증), 3종 (일반암, 급성심근경색증), 4종 (일반암,
뇌출혈), 5종 (일반암 only) — each 최초 1회한. The rider's own 가입금액 is defined as **the
premium it waives**: 「이 특약의 가입금액은 이 특약이 부가된 종형별 주계약 및 그 주계약에
부가된 특약의 보험료 합계액」 [S12]. It is available on the 순수보장형 only [S13], and its
보험기간 and 납입기간 track the main contract's 납입기간, with 가입나이 만19~70세 [S12].
한화생명 sells the same idea as a 9대질병보험료납입면제특약 on its whole-life chassis [S19].

미래에셋 splits its waiver rider by whether the rider's own 계약자적립액 is paid on death:
**[특약유형 W]** (미지급형) is cheaper; **[특약유형 S]** (지급형) pays the accumulated rider
reserve to the policyholder if the life dies before a waiver event [S17] [S18]. That is a
mini-version of the 무해지 device applied to a rider, and it is unique to this carrier in the
retrieved set.

### 14. Exclusions, contestability, grace, lapse, reinstatement, policy loan

**면책사유 — three limbs, and only three.** 한화생명 제6조, verbatim [S2], and reproduced
almost word for word in [S1] [S6] [S8] [S10] [S11] [S17]:

> 1. 피보험자가 고의로 자신을 해친 경우
>    다만, 다음 중 어느 하나에 해당하여 보험금지급사유가 발생한 때에는 보험금을 지급하며
>    보험료 납입면제 사유가 발생한 때에는 납입을 면제하여 드립니다.
>    가. 피보험자가 심신상실 등으로 자유로운 의사결정을 할 수 없는 상태에서 자신을 해친 경우…
>    나. 계약의 보장개시일(부활(효력회복)계약의 경우는 부활(효력회복)청약일)부터 **2년**이
>        지난 후에 자살한 경우에는 …사망보험금을 지급합니다.
> 2. 보험수익자가 고의로 피보험자를 해친 경우
>    다만, 그 보험수익자가 보험금의 일부 보험수익자인 경우에는 다른 보험수익자에 대한 보험금은
>    지급합니다.
> 3. 계약자가 고의로 피보험자를 해친 경우

- **The suicide window is 2 years** and it restarts only on 부활, never on renewal. Every
  carrier in the set says 2년: [S1] [S2] [S3] [S6] [S8] [S10] [S11] [S13] [S17]. This is **one
  year shorter than Japan's three** and one year longer than the UK's twelve months, and it is
  invariant across the whole Korean market — 「고의적 사고 및 2년 이내 자살」 is even the
  phrase carriers use in consumer copy [S3] [S13].
- **심신상실 is an exception to limb 1 with no time bar at all**, and the 약관 defines it:
  「정신병, 정신박약, 심한 의식장애 등의 심신장애로 인하여 사물을 변별할 능력 또는 의사를
  결정할 능력이 없거나 부족한 상태」 [S2].
- **There is no war clause, no aviation clause and no dangerous-pursuits clause** in any 약관
  or 상품요약서 retrieved. Korea handles occupational risk through the **위험등급** at
  underwriting (§4) and through 직업 or 직종별 가입한도 [S2 제24조제4항] [S3], not through
  policy exclusions. Nor is there any war-emergency **reduction power** of the kind
  オリックス生命 and ライフネット生命 carry in `jplib`. This is a real difference and the
  product spec should say so.
- **There is no pre-existing-condition restriction on the death benefit**, and no 감액기간 —
  except on the **간편고지형**, where 미래에셋 pays only 「보험가입금액의 50%」 for a
  non-accidental death 「계약일로부터 2년 미만」 [S17] [S18].
- **재해 is defined by 별표3 재해분류표**, verbatim [S2]: 보장대상 = 「① 한국표준질병·사인
  분류상의 (S00~Y84)에 해당하는 우발적인 외래의 사고 ② 「감염병의 예방 및 관리에 관한 법률」
  제2조 제2호에서 규정한 제1급감염병」. Excluded from 재해: pre-existing disease aggravated by
  a minor external cause; 과잉노력 및 격심한 또는 반복적 운동(X50); 무중력환경 장기체류(X52);
  식량부족(X53); 물부족(X54); 상세불명의 결핍(X57); **고의적 자해(X60~X84)**; 법적 처형(Y35.5);
  medical misadventure (Y60~Y69) absent fault; dehydration within 자연의 힘에 노출(X30~X39);
  respiratory/swallowing failure of disease origin within W65~W84 and W44; and U00~U99. The
  classification in force is the **제9차 개정 한국표준질병·사인분류 (통계청 고시 제2025-299호,
  2026.1.1. 시행)**, judged as at the date of diagnosis or occurrence and never re-judged
  afterwards [S2 제3조].

**계약 전 알릴 의무 (contestability)** [S2 제14–15조]. The insurer may 해지 or restrict cover
where the 계약자 or 피보험자, intentionally or by gross negligence, misstated a material
matter. It may **not** do so where:

1. it knew, or negligently did not know, the fact at the time of contracting;
2. **1개월** has passed since it learned the ground, **or 2년 has passed from the 보장개시일
   without a claim event arising (1년 for 질병 on a 진단계약)**;
3. **3년** have passed since the contract date;
4. it accepted on the basis of a 건강진단서 사본 and the claim arises from something recorded
   there.

Limbs 2 and 3 track 상법 제651조's 1개월 / 3년 [R5]; the **2년 / 1년 no-claim window is a
contractual improvement on the statute** and is the operative contestability period. On
rescission the insurer pays the 해약환급금; where it restricts cover instead, 「보험료,
보험가입금액 등이 조정될 수 있습니다」 [S1] [S2] [S11].

**사기에 의한 계약** is separate and much longer: where the insurer proves 뚜렷한 사기의사 —
proxy medical, drugs to pass a test, a forged certificate, or concealing a pre-application
cancer or HIV diagnosis — it may **취소** the contract 「보장개시일부터 **5년** 이내(사기사실을
안 날부터는 1개월 이내)」 and returns the premiums paid [S1] [S2 제16조] [S6] [S8] [S10] [S11]
[S17]. So the effective outer limit on unwinding a Korean life policy is **five years**, not
two or three.

**계약의 무효** [S2 제20조]: no written consent of the life assured (상법 제731조 [R3]); a life
under 15, 심신상실자 or 심신박약자 (상법 제732조 [R4]); or an issue age outside the product's
range. Premiums are returned; where premiums had been waived, only those actually paid are
returned.

**Grace, lapse, reinstatement** [S2 제27–29조]:

- **납입최고(독촉)기간 is 14일** (7일 where the term is under a year), extended to the next
  business day if it ends on a non-business day. The insurer must notify in writing, by
  recorded telephone or by electronic document, stating both the arrears and the fact that the
  contract will be 해지 on the day after the period ends.
- **A claim arising before the 해지 is paid**: 「다만 해지 전에 발생한 보험금 지급사유에 대하여
  회사는 보상하여 드립니다.」
- On 해지 the insurer pays the 해약환급금 (nil on the 무해지 form during the paying period) and
  immediately deducts any 보험계약대출 principal and interest.
- **부활 (reinstatement) within 3년** of the lapse date, provided the 해약환급금 was **not**
  taken — and 「해약환급금이 없는 경우를 포함합니다」, so a 무해지 policy is always eligible.
  The arrears must be paid with interest 「평균공시이율+1% 범위 내에서 회사가 정하는 이율로」.
  Reinstatement re-runs 계약 전 알릴 의무, its violation effects, 사기에 의한 계약, acceptance
  and the start of cover — but 「회사는 해지 전 발생한 보험금 지급사유를 이유로 부활을 거절하지
  않습니다」. A 고지 violation at the **original** application still bites after reinstatement.
- **특별부활** where the contract was terminated by 강제집행, 담보권실행 or a tax seizure of
  the surrender-value claim: the insurer must notify the 보험수익자 **within 7일**, and the
  beneficiary may, with the policyholder's consent, repay what the insurer paid the creditor,
  become the policyholder and revive the contract **within 15일** of notice [S2 제29조].

**보험계약대출 (policy loan) and 자동대출납입 (automatic premium loan)** [S2 제26조·제34조]:

- The policyholder may borrow within the 해약환급금, 「그러나 **순수보장성보험 등 보험상품의
  종류에 따라 보험계약대출이 제한될 수도 있습니다**」. On a 무해지 term in its paying period
  the surrender value is nil, so the loan facility is nil in fact even where it is not excluded
  in terms.
- **자동대출납입 is available on this chassis** — unlike `jplib`'s 定期保険, where 日本生命
  states twice that 自動振替貸付 does not apply. The Korean rules: it must be requested before
  the 납입최고기간 ends; it stops once loan plus interest would exceed the surrender value; it
  runs for **1년 at a time** and must be re-applied for; the policyholder may unwind it by
  asking to 해지 within **1개월** of the end of the original grace period, in which case the
  insurer treats the APL as never having happened and pays the ordinary 해약환급금; and the
  insurer must notify the policyholder **within 15일** of the APL ending [S2 제26조].
- Again the 무해지 form makes this mostly theoretical during the paying period.

**청약철회 (cooling-off)** [S2 제18조]: **15일 from receipt of the 보험증권**, and in any event
not more than **30일 from the application date** (45일 where a policyholder aged 65 or over
contracted by telephone). Not available where the insurer paid for a health examination, where
the term is 90일 or less, or for a 전문금융소비자. Refund in full **within 3영업일**, with
interest at the 보험계약대출이율 if late. 교보라이프플래닛's consumer page markets the same
right as 「100% 무료 반품 … 가입일로부터 30일 이내」 [S13].

**위법계약의 해지** [S2 제30조의2], under 금융소비자보호법 제47조: where the insurer breached
the selling rules, the policyholder may demand termination **within 1년 of learning of the
breach and within 5년 of the contract date**; the insurer must answer within **10일**; and on
termination it returns 「회사가 적립한 해지 당시의 **계약자적립액**」 — the full reserve, with
**no surrender charge**. This is a materially better outcome than an ordinary 해지 and it has
no analogue in any other library here.

**중대사유로 인한 해지** [S2 제31조]: claim-provoking, or forging/altering claim documents; the
insurer may 해지 within **1개월** of learning, and pays the 해약환급금. **소멸시효 3년** on
보험금청구권, 보험료 반환청구권, 해약환급금청구권 and 계약자적립액 반환청구권 [S2 제38조],
matching 상법 제662조 [R7].

**Interpretation rules** [S2 제39조]: good faith; **contra proferentem** — 「회사는 약관의 뜻이
명백하지 않은 경우에는 계약자에게 유리하게 해석합니다」; and no expansive reading of
exclusions. Where a sales document contradicts the 약관, 「계약자에게 유리한 내용으로 계약이
성립된 것으로 봅니다」 [S2 제40조].

### 15. Riders and options

**선지급서비스특약 (accelerated death benefit) — Korea's terminal-illness cover.** It is a
제도성특약 (an administrative rider carrying no separate premium in any retrieved document),
attached as standard. 한화생명's 선지급서비스특약(K3.10) 제3–4조, verbatim [S2]:

> 제 3 조 보험금의 지급사유
> 회사는 …특약의 보험기간 중에 「의료법」 제3조의3(종합병원)의 규정에 따른 국내의 종합병원
> 또는 국외의 의료관련법에서 정한 의료기관에서 전문의 자격증을 가진 자가 실시한 진단결과
> 피보험자의 남은 생존기간이 **12개월 이내**라고 판단한 경우에 …주계약 사망보험금액의 일부를
> 선지급 사망보험금…으로 피보험자에게 지급합니다.
> 제 4 조 ① 이 특약에 의한 보험금 한도는 주계약 사망보험금액의 **50% 이내**에서 피보험자별로
> 통산하여 최고 **5,000만원**까지로 합니다. 다만, **1,000만원까지는 주계약 사망보험금액의
> 100% 이내**로 할 수 있습니다.
> ② …지급한 보험금액에 해당하는 주계약의 보험가입금액이 지급일에 감액된 것으로 봅니다. 다만,
> 그 감액부분에 해당하는 해약환급금이 있어도 이를 지급하지 않습니다…
> ⑥ …보험금을 남은 생존기간 동안 평균공시이율로 할인한 금액에서 『선지급 사망보험금에 대한
> 남은 생존기간 동안 평균공시이율로 할인된 보험료』와 『주계약에 보험계약대출금이 있는 경우에는
> 그 원금과 이자 합계액』을 뺀 금액을 지급합니다.

Compared with Japan's リビング・ニーズ特約 (`jplib` §9): the **trigger is 12 months, not 6**;
the cap is **50% of the sum assured to a maximum of 5,000만원**, not the whole benefit to
3,000만円; there is **no one-year-before-expiry bar**; and the discount is the same in kind —
present-valuing the benefit and netting off the premiums that would have been paid, here at the
**평균공시이율** (2.50% for calendar 2026 [S12]) rather than at a contractual rate. One payment
per contract; the beneficiary of the accelerated payment is the **피보험자** [S2 제4조제4항].
**미래에셋 narrows the trigger for term specifically**: 「…남은 생존기간이 12개월 이내(다만,
**정기보험의 경우 6개월 이내**)라고 판단한 경우」 [S17] — the only carrier in the set to do so.

**Other 제도성특약 present on nearly every product** [S1] [S2] [S9] [S10] [S11] [S12] [S17]:

- **지정대리청구서비스특약** — where 계약자, 피보험자 and 보험수익자 are the same person, a
  pre-nominated agent may claim on the insured's behalf. Universal.
- **단체취급특약 / 신한단체취급보험료할인특약Ⅱ** — a group-administration discount for a
  **5-or-more** affinity group: **영업보험료의 1.5%** at 한화생명 [S1], **5% of 영업보험료 from
  the second premium onwards** at 신한라이프 [S10] (excluding 일시납). 교보라이프플래닛 markets
  the same thing as a workplace referral discount [S13].
- **장애인전용보험전환특약** — converts the policy into a 장애인전용보장성보험 so that the
  **15%** credit of 소득세법 제59조의4 제1호 applies instead of the 12% [R8]; present at every
  carrier [S1] [S10] [S11] [S12] [S17].
- **특정 신체부위·질병 보장제한부 인수특약** and **표준하체인수특약 / 특별조건부인수특약 /
  표준미달체조건부인수특약 / 보험료할증·보험금감액가입특약** — the substandard-acceptance
  toolkit. 미래에셋 names the three methods in one line: 「할증보험료법, 보험금감액법,
  나이가산법」 [S17]. The Japanese pair 保険金削減支払法 / 特定部位不担保法 maps onto the first
  two of these; **나이가산법** (rating up the age) is the third and has no `jplib` counterpart.
- **출산육아휴직 보험료 납입유예특약** — a premium holiday of **6 or 12 months, once per
  contract**, where the policyholder or their spouse is within a year of childbirth or on
  parental leave [S1] [S12] [S17] [S18]. A genuinely Korean policy response to the birth rate,
  and present at four of the carriers retrieved.
- **사후정리특약 / 사후 사망보험금 신속지급특약** — an advance of part of the death benefit for
  funeral costs [S10] [S12] [S17].
- **양육자금(사망보험금분할지급설정)서비스특약** — pays the death benefit to a child in annual
  instalments with interest [S12] [S13].
- **연금전환특약** and **종신전환특약**. 미래에셋 offers both on its term product: the annuity
  conversion, with 종신연금형 (20년·30년·기대여명 보증지급, 정액형 or 5%/10% 체증형),
  확정연금형 (5/10/15/20년) and 상속연금형, credited at a 공시이율 with a floor of 「주계약
  계약일 이후 10년 미만에는 연복리 1.0%, 10년 이상에는 연복리 0.5% 최저보증」; and the
  **whole-life conversion**, 「보험계약자는 보험기간이 종료되기 전 이 보험계약을 '종신전환특약
  무배당'을 통해 종신보험으로 변경할 수 있습니다. 이 경우 전환 후 보험계약의 보험가입금액은
  전환 전 보험계약의 사망보험금을 한도로 합니다」, on the terms and rates in force at
  conversion and subject to the then-current issue-age rules [S17] [S18]. **This is the Korean
  conversion option**, and `jplib` has nothing like it — the nearest thing there is FWD生命's
  one-month post-expiry re-entry window.

**재해사망 cover is a product variant more often than a rider.** 신한SOL sells 기본형 and
**재해보장형**, the latter paying 「보험가입금액의 2배」 on 재해사망 and 「보험가입금액」
otherwise [S10]; 흥국생명 sells 1형(기본형) and **2형(보장추가형)** on exactly the same
structure — 재해사망보험금 2,000만원 and 일반사망보험금 1,000만원 per 1,000만원 of cover [S6];
and 흥국restricts female lives to 보장추가형 [S6]. The disclosure shows 삼성The라이트
간편건강보험 splitting its 주계약 into 재해사망보험금 and 일반사망보험금 rows the same way
[S4]. Given the published 예정 재해사망률 (§11) the accidental uplift costs a few per cent of
the base premium, which is why it is bundled rather than sold.

**What is absent from every product retrieved**: an indexation or increasing-cover option on a
retail contract (the 체증 designs are corporate-only); a guaranteed-insurability option on life
events; joint-life or first-death cover; and any 배당. There is also **no 감액완납 (reduced
paid-up) and no 연장정기 (extended term)** option in any retrieved 약관 or 상품요약서 — a
Korean term policyholder in difficulty has 자동대출납입, 보험료납입유예, 감액 or lapse, and
nothing else.

### 16. 정기특약 — the term rider on a 종신보험

The 정기특약 — a level-term rider attached to a 종신보험 so that the household can carry a
large sum assured through the child-rearing years on top of a smaller permanent base — is a
standard part of the Korean traditional agency proposition and appears in secondary material,
including a rule that 「무배당 정기특약의 경우 보장내용이 동일한 특약에 대하여 갱신형과
비갱신형을 함께 부가할 수 없습니다」 [unverified — a search-result snippet from a 하나생명
product page whose rider list could not be retrieved].

**The evidence retrieved runs the other way for current products.** The string 정기특약 does
not occur in the rider menu of any current 종신보험 document opened this session:

- 한화생명 H종신보험 무배당 [S19]: 선택특약Ⅱ = 3대질병케어특약, 9대질병보험료납입면제특약;
  제도성특약 = 3대질병연금전환, CI연금전환, LTC연금전환, 건강체서비스특약Ⅱ, 계약분리특약,
  단체취급특약, 사망보험금조기지급특약, 선지급서비스특약, 스마트연금전환특약, 양육자금전환특약,
  장애인전용 세제전환특약, 지정대리청구서비스특약, 특정 신체부위·질병 보장제한부 인수특약,
  표준하체인수특약. **No term rider.**
- 무배당 AIA 더해주는 종신보험 [S20]: no occurrence of 정기특약.
- 한화생명 하나로H종신보험 무배당 and 한화생명 e종신보험 무배당 [S21]: no occurrence.
- The 종신보험 view of the 상품비교공시, pages 1–2 [S22]: across every disclosed 특약 name and
  benefit description on those pages, the substring 정기 appears only in the page's own
  category labels.

The honest reading is that the 정기특약 is a **legacy and traditional-channel structure that
has been displaced** in the current product set by (a) standalone online 정기보험 and (b)
health and CI riders on the whole-life chassis. `product-spec.md` should treat the standalone
contract as the market form and mention the rider form only as an alternative packaging, tagged
[unverified], with this negative evidence recorded. A future pass with an older 약관 in hand —
[S23] was the intended source and returned 404 — could settle it.

### 17. 보험나이, tax and policyholder protection

**보험나이 (insurance age).** 한화생명 제22조, verbatim [S2]:

> ① 이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다. 다만, 제20조(계약의 무효)
> 제1항 제2호의 경우에는 실제 만 나이를 적용합니다.
> ② 제1항의 보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의 끝수는
> 버리고 6개월 이상의 끝수는 1년으로 하여** 계산하며, 이후 매년 계약 해당일에 나이가 증가하는
> 것으로 합니다.
> 【매년 계약 해당일】 제2차년도 이후 매년의 계약일과 동일한 월, 일. 다만, 해당 월에 동일한
> 일이 없는 경우에는 해당 월의 말일
> ③ 청약서류상 피보험자의 나이 또는 성별에 관한 기재사항이 신분증에 기재된 사실과 다른
> 경우에는 신분증에 기재된 나이 또는 성별로 정정하고, 정정된 나이 또는 성별에 해당하는 보험금
> 및 보험료로 변경합니다.
> 【보험나이 계산 예시】 생년월일: 1988년 10월 2일, 현재(계약일): 2018년 4월 13일
> ⇒ 2018년 4월 13일 - 1988년 10월 2일 = 29년 6월 11일 = **보험나이 30세**

So 보험나이 is **age nearest birthday** computed by the six-month rule, it **increments on the
policy anniversary and not on the birthday**, and the one place it does not apply is the
under-15 voidness test, which uses 만나이 [S2 제22조제1항 단서, cross-referring
제20조제1항제2호]. 삼성생명 flags the same point in its 상품요약서: 「만나이가 아닌 나이는
보험나이입니다」 [S8] [S9], as does 신한라이프 [S10]. Every premium and every 가입나이 limit in
this file is in 보험나이 unless it is written 만19세 / 만15세, which are 만나이. **Every
statistic in §19 and [R15] is in 만나이.** The distinction is real: the six-month rule means
보험나이 differs from 만나이 for half of all issue dates.

**Tax.** Premiums on a 보장성보험 attract a **세액공제 (tax credit), not a deduction**:
소득세법 제59조의4 제1항 gives 「그 금액의 100분의 12(제1호의 경우에는 100분의 15)에 해당하는
금액을 해당 과세기간의 종합소득산출세액에서 공제한다」, capped at 「연 100만원」 of premium per
category [R8]. So the maximum annual benefit on an ordinary 정기보험 is **₩1,000,000 × 12% =
₩120,000**, and on a 장애인전용보장성보험 **₩1,000,000 × 15% = ₩150,000**. The
장애인전용보험전환특약 present at every carrier (§15) exists precisely to move a policy into
the 15% basket. A 정기보험 qualifies as a 보장성보험 because 「만기에 환급되는 금액이
납입보험료를 초과하지 않는」 — which is true of the 순수보장형 by construction and of the
만기환급형 by design, since it returns exactly 100% of premiums and no more.

No retrieved document addresses the taxation of the **death benefit** in the hands of the
beneficiary — 상속세 및 증여세법 and its treatment of a policy where 계약자, 피보험자 and
수익자 differ. `jplib`'s term-life file carries the equivalent Japanese triangle from a carrier
booklet; no Korean carrier document in this set does, and no 국세청 page was retrieved. That is
a gap.

**예금자보호.** Every retrieved consumer document carries the same notice [S3] [S11] [S13]:
「이 보험계약은 예금자보호법에 따라 해약환급금(또는 만기 시 보험금)에 기타지급금을 합한 금액이
1인당 "**1억원까지**"(본 보험회사의 여타 보호상품과 합산) 보호됩니다. 이와 별도로 본 보험회사
보호상품의 **사고보험금**을 합산한 금액이 1인당 "1억원까지" 보호됩니다. 다만, 보험 계약자 및
보험료납부자가 법인인 보험계약의 경우에는 보호되지 않습니다.」 The limit doubled from 5천만원
to 1억원 with effect from **2025-09-01** [R17, in part]. Two features are worth carrying into
the product spec: the **사고보험금 (claim) limit is separate from and additional to** the
surrender/maturity limit — so a ₩100,000,000 term policy is protected in full on the claim side
— and **corporate policyholders are not protected at all**, which bears directly on the
경영인정기보험 market.

### 18. Valuation, supervision and the actuarial basis

**해약환급금 and 표준해약공제액.** Every carrier states the surrender-value formula in the same
words: 「보험료 계산시 적용한 위험률로 산출한 **순보험료식 계약자적립액**에서 **해약공제액**
(미상각신계약비)을 공제한 금액을 해약환급금으로 지급합니다」 [S6] [S10] [S11] [S12], or
「계약자적립액에서 해약공제금액을 공제한 금액」 [S8] [S9]. 한화생명 words it as 「순보험료식
계약자적립액에서 해약공제액을 공제한 금액」 [S1].

The deduction is capped by 보험업감독규정 제7-66조 and its 별표14. The cap, verbatim [R9]:

> **표준해약공제액 = 연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000**
>
> 주2. 해약공제계수는 다음과 같이 적용함
>   - 보장성보험: 보험기간(최대 20년)
>   - 저축성보험: 보험료납입기간(최대 12년)…
> 주3. 연납순보험료 및 연납위험보험료는 다음과 같이 적용함
>   - 보장성보험: **전기납(단, 보험기간이 20년 이상인 경우 20년납)으로 조정하여 산출한
>     연납순보험료** 및 연납위험보험료…
>   - 저축성보험: 납입기간(최대 10년) 동안 동일하게 배분한 평균식 부가보험료를 제외한 연간
>     순보험료

For a 보장성보험 the 해약공제계수 is therefore the **policy term in years, capped at 20**, and
the sum-assured term is **1% of the sum assured** (10/1000). On the library's anchor contract —
₩100,000,000, 20-year term — the sum-assured component alone is **₩1,000,000 (100만원)**, which
is more than five months of gross premium. That is why every 표준형 term product in §10 shows a
nil surrender value for the whole of the first year and a low one for the second.

**What could not be established**: 별표14 gives the *cap*, not the amortisation. The
해약공제기간 and the schedule by which the unamortised 신계약비 runs off live in 제7-66조
itself, whose text could not be retrieved [R10]; a search snippet describes a 해약공제기간
equal to the premium-paying or acquisition-cost period **capped at 7 years**, with the
deduction reducing by elapsed months over that period, but no primary text confirms it and the
claim is **[unverified]**. `technical-notes.md` must therefore either standardise the
amortisation or calibrate it to the published 해약환급금 tables in §10 — the latter is
preferable and is possible, because §10 gives eleven to seventeen points per curve for six
carriers.

**IFRS 17 / K-ICS assumption guidance.** Korea has run K-IFRS 1117 and K-ICS together since
2023-01-01. For this product the operative guidance is the 「IFRS17 주요 계리가정 가이드라인」
announced 2024-11-07 [R13]:

- 무·저해지 **해지율 원칙모형** = 「로그-선형(log-linear) 모형 원칙(**수렴점 0.1%**)」, i.e. a
  lapse rate declining log-linearly to 0.1% at the completion of premium payment;
- **완납 후 최종해지율 0.8%** (or, alternatively, a 20% relativity of a 저해지 product's lapse
  rate to a foreign standard-form benchmark);
- permitted **예외모형** limited to 선형-로그모형 (수렴점 0%) and 로그-로그모형 (수렴점 0.1%),
  and only on strict conditions — 「감사보고서·경영공시에 他모형 선정의 특별한 근거와
  원칙모형과의 차이(CSM, K-ICS, 당기순이익 등)를 상세히 공시」, quarterly reporting to the FSS
  and exposure to on-site inspection;
- 단기납 종신보험 must assume **30% 이상의 추가해지** at the point the return rate peaks;
- discount curve: **최종관찰만기 extended to 30 years**, phased over three years;
- effective from the **2024 year-end close** (loss-ratio assumptions deferred to 2025 Q1), and
  from January 2025 for the discount-rate measures.

The 2021 predecessor [R12] had already imposed a product-design rule — 「해지환급금 수준이
낮으면(10%, 50%) 해지율을 더 낮게(0.2%, 1%) 적용」 and 「보험료 납입중 해지율은 기간이
경과할수록 하락(예: 5차년도 5%, 10차년도 2%)」 — which is visibly what the carriers' disclosed
적용해지율 in §11 implement.

**Mortality tables.** The industry table is the **경험생명표**, produced by 보험개발원 every
five years under 보험업법 from life-insurance policyholder statistics; the current edition is
the **제10회**, applied from **April 2024** [R14]. Its headline outputs — 평균수명 남 86.3세,
여 90.7세; 65세 기대여명 남 23.7년, 여 27.1년 — are public, and it feeds the 보험가격지수
calculation [R14]. **The table itself is not published**: no numeric 경험생명표 was retrievable
from 보험개발원's site or anywhere else in this session (see gaps), and this is the single
sharpest contrast with `jplib`, whose 標準生命表2018 is a free public PDF with qx by single
year of age.

What *is* public is (a) the **통계청 완전생명표** — 2024 기대수명 전체 83.7년, 남 80.8년, 여
86.6년; 60세 기대여명 남 23.7년, 여 28.4년 [R15] — and (b) the **carriers' own 예정 경험사망률
at three ages** (§11). Note that the 경험생명표's 65세 male 기대여명 of 23.7년 [R14] happens to
equal the 통계청 table's **60세** male 기대여명 of 23.7년 [R15]: an insured Korean male at 65
has the life expectancy of a general-population male at 60, which is a five-year selection
effect and a usable sanity check on any constructed table.

**Consequence for krlib, stated plainly.** Because the 경험생명표 is not published in full,
**every `mort_table.csv` in this library is a `[std]` construction** anchored on the published
summary statistics [R14], the 통계청 완전생명표 [R15] and the carriers' disclosed three-point
예정 경험사망률 (§11), with a `provenance` column on every row. For `Term_KR_S` specifically
the three-point disclosures are the best available anchor, because they are *pricing* rates for
*this product* at *these ages* from seven carriers, and their dispersion (§11) is itself the
uncertainty measure.

### 19. Market context

- **Life industry size.** 2025 H1 생명보험 수입보험료 (excluding 퇴직연금) **51조원**, +6.1%
  year on year; 연납화초회보험료 **10.2조원**, +3.4% [R16].
- **Protection business.** 보장성보험 수입보험료 2021–2024: **44.9 / 47.1 / 48.6 / 55.0조원**;
  2025 H1 **30.3조원**, +13.0% [R16]. Growth rates 2021–2024: −0.1% / 4.9% / 3.2% / 13.1%.
- **Where the growth is.** 보험연구원's reading: 「2025년 상반기 생명보험 보장성보험은 질병 및
  상해보험 중심으로 높은 성장세를 유지함 — 신계약CSM 측면에서 상대적으로 유리한
  **무·저해지환급형 질병보험과 상해보험**의 판매가 증가함」, with 치매·장기간병보험 and
  어린이보험 also expanding, and 단기납 종신보험 competition easing after the 환급률 was reined
  in [R16]. **Death cover is not the growth story**; the 제3보험 products are.
- **New-business outlook.** 2026 industry premium growth forecast **2.3%** against 7.4% in
  2025, on total premium of about **265조원**; life 수입보험료 +1.0%, life 초회보험료 **−0.9%**
  [R16].
- **무·저해지 penetration.** 신계약비중 1.4% (2016) → 6.8% (2018) → 14.7% (2020), 13.7% in 2021
  Jan–Aug, on 443.5만건 of new business in 2020 [R12]. No later or term-specific figure was
  retrieved.
- **Market structure for this product.** 45 정기보험 products across 15 carriers appear in the
  current disclosure [S4]. Of those, roughly **19 are retail** (기본형, 순수보장형 or
  만기환급형) and **12 are 경영인정기보험**; only **three are 갱신형**; only **two carriers**
  (흥국생명, 푸본현대) sell a renewable term at all; and **9 of the 19 retail rows are CM
  (online)** — a far higher online share than the Korean life market as a whole. Term life is,
  in Korea, substantially a direct-channel product.

No Korean equivalent of Japan's 生命保険文化センター 全国実態調査 — household penetration,
average sum assured, product mix of the most recent purchase — was retrieved in this session,
so this file carries no household-level context. That is a gap and `whole-life.md` will have to
close it for the library.

---

## Variation across carriers

The drafting pass turns this into the product spec's "Variations across insurers" section. The
observed range is given wherever more than one carrier states the parameter; where only one
does, the entry says so.

| Feature | Observed positions | Range |
|---|---|---|
| 가입나이 (min) | 만15세 [S10] [S17]; 만19세 [S1] [S6] [S11] [S12]; 20세 [S8] [S9] [S15]; 24/26/29/30/33/38/46세 in particular cells [S12] [S17] [S18] | **만15세–만19세**, mode 만19세 |
| 가입나이 (max) | 60세 [S6] [S10] [S15]; 64세 [S8]; 65세 [S1] [S9]; 70세 [S11] [S12] [S17] [S18] | **60–70세**, mode 65–70 |
| 보험기간 menu | 90세만기 only [S18]; 1년만기 only [S15]; 10년만기 갱신 only [S6 2종]; 80/90세만기 [S17]; 20년·60세·80세만기 [S6 1종]; 10년+60/65/70/80세 [S8] [S11]; 10/20년+70/80/90세 [S9]; 10/15/20/25/30년+60/70/80세 [S10]; 10년+60/65/70/80/90/100세 [S1]; 10/20/30년+60/65/70/75/80/85/90세 [S12] | one option to eleven |
| 세만기 ceiling | 80세 [S6] [S8] [S11]; 90세 [S9] [S12] [S17] [S18]; **100세** [S1] | **80–100세** |
| 납입기간 menu | 전기납 only [S15] [S18]; 10/20/전기납 [S1] [S8]; 15/20/전기납 [S9]; 10/20/전기납 [S6]; 20/30/60세/70세/전기납 [S12]; 5/7/10/15/20/55세/60세/전기납 [S11]; 5–30년/60세/70세/전기납/일시납 [S10] | 전기납 always; shortest 5년납 [S10] [S11]; 일시납 at one carrier [S10] [S14] |
| 납입주기 | 월납 only [S1] [S6] [S8] [S9] [S12] [S17] [S18]; 월납·연납 [S15]; 월납·3개월·6개월·연납 [S11]; 월납·연납·일시납 [S14] | monthly always |
| 가입한도 (retail ceiling) | 1,000만원 [S15]; 1억원 [S17 간편]; 2억원 [S6] [S17]; 3억원 [S8] [S10]; 5억원 [S1] [S9] [S11] [S14]; **10억원** [S12] | **1,000만원–10억원** |
| 가입한도 (retail floor) | 100만원 [S15]; 1,000만원 [S6]; 2,000만원 [S17]; 3,000만원 [S9] [S10] [S11] [S14]; 5,000만원 [S8]; 1억원 [S12] | **100만원–1억원** |
| 가입단위 | 100만원 [S15]; 1,000만원 [S6] [S12]; unpublished elsewhere | 100만–1,000만원 |
| 만기환급 form | 없음 (순수보장형 only) [S9] [S10] [S15] [S18]; 0% / 100% [S1] [S8] [S11] [S12] [S17]; **0% / 50% / 100%** [S14] | binary at all but one carrier |
| 무해지/저해지 step-up | 전기납 계약 nil throughout [S1] [S2]; **50%** of 표준형 after 납입완료 [S1] [S2] [S12]; **0% / 30% / 95%** at 3 and 5 years [S18]; a 10–50% menu contemplated by the regulator [R12] | **nil to 95%** |
| 무해지 premium saving | **1.35–1.57%** on a 20-year 전기납 term [S12]; **14%** on a 100세만기 term [S3]; **25.2%** on the regulator's unnamed illustration [R12] | **1.4%–25%**, strongly increasing in term |
| Rate classes | 1 (표준체 only) [S15] [S17] [S18]; 2 [S1] [S6] [S8] [S9]; 3 [S4 DB생명]; 4 [S11] [S12] [S14] | **1–4** |
| Max preferred discount (male 40) | −11.1% [S6]; −17.5% [S1]; −30.5% [S4 DB]; −37.5% [S8]; −40.4% [S11]; −41.4% [S12]; −42.9% [S14] | **−11% to −43%** |
| Preferred criteria: BMI ceiling | 25.0 [S2] [S8] [S11 슈퍼] [S12 슈퍼]; 26.0 [S9]; 26.5 [S11 건강] [S12 건강] | 25.0–26.5 |
| Preferred criteria: SBP/DBP | 120/80 [S8] [S11 슈퍼] [S12 슈퍼]; 139/89 [S2]; 140/90 [S9] [S11 건강] [S12 건강] | two tiers, consistently |
| Preferred criteria: extra tests | 공복혈당 <100 [S8]; 혈당 <110 + 당뇨 이력 [S11] [S12]; **총콜레스테롤 <190** [S11 only] | cholesterol at one carrier |
| Rate class fixed at issue? | **No** — smoking-status notification duty, clawback and mid-term upgrade [S2 건강체서비스특약Ⅱ 제4조]; mid-term upgrade also at [S11] [S12] | uniform, and unlike `jplib` |
| 갱신 cycle | **1년** [S15]; **10년** [S6]; **15년** (rider) [S9] | **1–15년** |
| 갱신 opt-out notice | 15일 [S9] [S15]; not published [S6] | 15일 where published |
| 갱신 ceiling | 80세 [S6]; 최초계약 포함 최대 5년 [S15]; 주계약 만기 [S9] | **5년 total to 80세** |
| 고지 at 갱신 | not required anywhere [S6] [S9] [S15] | **no variation** |
| Waiver survives 갱신? | **No** [S6] | one carrier states it |
| 납입면제 trigger | 장해지급률 합산 50% 이상, 재해 또는 재해 이외 [S1] [S2] [S6] [S8] [S9] [S10] [S11] [S12]; **재해 only** on 간편고지형 riders [S17] [S18] | **no variation** on the standard form |
| Optional waiver rider | none [S1] [S8] [S9] [S10] [S11]; 5-way 진단형 (일반암/뇌출혈/급성심근경색증) [S12]; 납입면제특약Ⅱ with W/S 유형 [S17] [S18] | absent at five of nine |
| 재해사망 uplift | absent [S1] [S8] [S9] [S11] [S12] [S17]; **2× as a product 형** [S6] [S10] | present at two of nine |
| Accelerated death benefit | 선지급서비스특약 at every carrier [S2] [S10] [S12] [S17] [S18]; trigger **12개월** [S2], **6개월 for 정기보험** [S17]; cap 사망보험금의 50%, 통산 5,000만원, 100% up to 1,000만원 [S2] | trigger 6–12 months |
| 종신전환 / 연금전환 option | present [S17] [S18]; absent from every other term product retrieved | two of nine |
| Suicide exclusion | **2년** from 보장개시일 (or 부활청약일) [S1] [S2] [S3] [S6] [S8] [S10] [S11] [S13] [S17] | **no variation** |
| Exclusion list | intent of 피보험자 / 보험수익자 / 계약자, and nothing else [S1] [S2] [S6] [S8] [S10] [S11] [S17] | **no variation** |
| War / aviation / hazardous-pursuit clause | **absent everywhere** | **no variation** |
| Contestability | 2년 no-claim (1년 질병 on 진단계약), 1개월 from discovery, 3년 absolute [S2] [S11]; 상법 floor 1개월 / 3년 [R5] | **no variation** |
| 사기 취소 window | **5년** from 보장개시일 [S1] [S2] [S6] [S8] [S10] [S11] [S17] | **no variation** |
| 감액지급 (graded benefit) | none on 일반가입형; **50% for 2년** on 간편고지형 [S17] [S18] | simplified-issue only |
| 납입최고기간 | **14일** (7일 if 보험기간 < 1년) [S2] | one 약관 retrieved |
| 부활 | **3년**, arrears at 평균공시이율+1% 범위 내 [S2] | one 약관 retrieved |
| 자동대출납입 (APL) | **present**, 1년 renewable, unwindable within 1개월 [S2] | present, unlike `jplib` |
| 보험계약대출 | permitted within the 해약환급금, 「순수보장성보험 등…제한될 수도 있습니다」 [S2] | restricted in fact by the 무해지 form |
| 청약철회 | 증권 수령일부터 15일, 청약일부터 30일 (65세 이상 전화계약 45일) [S2]; marketed as 30일 [S13] | **no variation** |
| 단체취급 할인 | **1.5%** of 영업보험료 [S1]; **5%** from the 2nd premium [S10]; present without a rate [S11] [S12] | **1.5%–5%** |
| 고액할인 | present at 가입금액 ≥ 1억원, rate not published [S9]; absent elsewhere | one carrier |
| Behavioural discount | **걷기할인형** −10% for 12 months [S8]; absent elsewhere | one carrier |
| 적용이율 | 1.75% [S4] to **4.00%** [S4]; retail mode **2.50%**; 만기환급형 always ≤ 순수보장형 at the same carrier [S8] [S12] | **1.75%–4.00%** |
| 예정 경험사망률, 남 40 | 0.000480 [S17] to 0.000850 [S1] | **×1.77** |
| 예정 경험사망률, 여 40 | 0.000310 [S6] to 0.000540 [S11] | **×1.74** |
| 적용해지율 (무해지) | 납입기간 내 연 0.1%–4.6%, 이후 0.7%–1.6% [S12]; 납입기간 내 연 0.1%–8.4%, 이후 0.8% [S1] | start 0.1% at both |
| 보험가격지수 (남) | 51.6% [S4 교보라플 슈퍼건강체] to 175.2% [S4 NH]; CM channel 72–101%, 대면 104–175% | **52%–175%** |
| 배당 | 무배당 at every one of the 45 disclosed products [S4] | **no variation** |
| 감액완납 / 연장정기 | **absent from every document retrieved** | **no variation** |

**What does not vary.** Seven things are identical across every carrier examined and should be
treated as the product's fixed spine, not as choices: (1) the benefit is the 보험가입금액 on
death and nothing else, and payment terminates the contract; (2) the suicide bar is **2년**
from 보장개시일, restarting on 부활 and never on renewal; (3) the exclusion list is the three
intent limbs of 상법 제659조/제732조의2 and contains no negligence, war, aviation or
hazardous-pursuit limb; (4) the premium waiver triggers on a **50%-plus 장해지급률** from any
cause and waives future premiums only; (5) the 사기 취소 window is **5년**; (6) every product
is **무배당**; and (7) the surrender value is defined as 순보험료식 계약자적립액 less the
해약공제액, capped by 보험업감독규정 별표14 [R9], and runs to **exactly zero at maturity** on
every 순수보장형 curve published.

---

## Fetch failures and gaps

**URLs tried and not opened, or opened and not usable:**

- `https://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=2100000279112&type=HTML`
  (and the `LID=` / `MST=` / `type=JSON` / `mobileYn=Y` variants, and a POST to
  `/DRF/mobileAdmRulInfoR.do`) — the 보험업감독규정 detail endpoint returned HTTP 500, an empty
  body, or a connection reset on every attempt. `admRulLsInfoP.do?admRulSeq=2100000220196`
  returned only site chrome. **What was lost: 제7-66조 (해약환급금) itself** — the article that
  the 별표14 cap [R9] hangs off. Its 해약공제기간 and the amortisation of the unamortised
  신계약비 are therefore **[unverified]** (§18), and the reported "최대 7년" amortisation
  window rests on a search snippet only and is not used as a fact anywhere above.
- The same failure applies to **보험업감독업무시행세칙** [R11], whose 별표 carry the 보험료 및
  해약환급금 산출방법서 작성기준 and the 생명보험 표준약관. Only the rule's identifying
  metadata was recovered. **What was lost:** the statutory template against which [S2]'s
  article numbering could have been checked, and the official reserve-calculation rules.
- `https://www.law.go.kr/법령/상법/제731조` — the friendly 국가법령정보센터 URL returns only
  site chrome to a plain fetcher, confirmed by fetching it and comparing with casenote.kr.
  **Recovered** via `casenote.kr`, which serves article text; every statute in [R1]–[R8] is
  from that mirror and each entry records it.
- `https://www.insclaim.co.kr/39/8650566` [S23] — HTTP 404. This was the intended source for a
  **정기특약** on a 종신보험 (§16); the 정기특약 claim is consequently **[unverified]** and is
  reported alongside four pieces of negative evidence [S19]–[S22].
- `https://www.orangelife.co.kr/bizxpress/home/ap/wt/scwapwt070m.shtm` and
  `.../scwapwt100m.shtm` [S24] — HTTP 503 on both, and plain `curl` was reset by the host.
  **What was lost:** a fifteenth carrier's 순수보장형/만기환급형 term spec. No fact rests on
  them.
- `http://www.fss.or.kr/` [R21] — the 금융감독원 site served a 「홈페이지 중단 안내」
  interstitial and refused plain `curl`. **What was lost:** the FSS side of the IFRS17 계리가정
  가이드라인 and the 평균공시이율 publication the 약관 points at (「평균공시이율은 금융감독원
  홈페이지(www.fss.or.kr)에서 확인할 수 있습니다」 [S2]). **Partly recovered**: the guideline
  through the joint 금융위원회 release [R13], and the 2026 평균공시이율 of **2.50%** through
  교보라이프플래닛's 상품요약서 [S12].
- `https://www.kidi.or.kr/user/nd78654.do` [R20] — HTTP 200 but the 참조순보험요율 page is an
  HTML shell with no document list and no numbers. **What was lost:** the 제10회 경험생명표
  announcement in primary form, and any numeric 참조순보험요율. **Not recovered**: §18's
  경험생명표 figures are from a news article [R14] and are tagged as such; the 참조순보험요율
  is known only by the two 보험개발원 document numbers printed in [S10] [R19].
- `https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/yoyak_P400065_202504.pdf` — the
  우체국든든한종신보험 상품요약서, tried as a public-sector 종신보험 for the 정기특약 test;
  connection reset by the host. **What was lost:** one more negative-evidence data point in
  §16.
- `https://www.hanalife.co.kr/prd/personal/ga/linkedSingleLifeInsuOneTwo/linkedSingleLifeInsuOneTwoIntro.do`
  — retrieved, but the page is an introduction only and its 약관 downloads are behind a
  JavaScript control. **What was lost:** the 하나생명 rider list, which is where the 「무배당
  정기특약…갱신형과 비갱신형을 함께 부가할 수 없습니다」 snippet in §16 came from.
- `https://direct.samsunglife.com/term.eds` — HTTP 200 but a 6.7 KB JavaScript shell containing
  only the title 「삼성생명 다이렉트」. **Recovered** by taking 삼성생명's product data from
  its 상품요약서 [S8] via the 생명보험협회 disclosure instead.
- `https://www.lifeplanet.co.kr/products/pg/PG01000S.dev` and
  `https://www.lifeplanet.co.kr/disclosure/good/HPDA01S0.dev` — connection reset mid-exchange
  on two attempts (the host served two other pages on the same session without trouble). **What
  was lost:** 교보라이프플래닛's own 상품공시실 index. **Recovered**: its 상품요약서 [S12] came
  through the 생명보험협회 disclosure instead.
- `https://www.klia.or.kr/consumer/stats/fiftyYear/list.do` — connection reset;
  `https://www.klia.or.kr/consumer/stats/statHomSta/monthStats.do` — retrieved, but it is a
  year/month selector shell over 금융통계월보 files rather than a data page. **What was lost:**
  a 정기보험-specific new-business series. §19 therefore has industry-level figures from
  보험연구원 [R16] and none at product level.
- `https://www.aia.co.kr/.../AIA_kr_Form120_20260101.pdf` [S20] — a summarising fetch reported
  it as unreadable binary. **Recovered** by saving the returned bytes and extracting them
  locally with `pymupdf`; the file is intact.
- `https://www.law.go.kr/LSW//flDownload.do?flSeq=137472119...` [R9] — same symptom, same
  recovery. Both are recorded because the pattern matters: a fetcher's "corrupt PDF" report
  should be re-tested locally before the document is written off.

**Claims left [unverified], and why:**

- **보험업감독규정 제7-66조's 해약공제기간 and the amortisation schedule of the 해약공제액.**
  The cap is sourced [R9]; the run-off is not. See above.
- **The 정기특약 as a live rider on a current 종신보험** (§16). Four current whole-life
  documents were checked and none carries one [S19] [S20] [S21] [S22]; the affirmative claim
  rests on one search snippet and the intended primary source 404'd [S23].
- **교보라이프플래닛's 정기보험 being 갱신형.** [S13]'s 가입 시 유의사항 block contains the
  lines 「이 상품은 갱신형 상품으로 갱신 시 보험료가 인상될 수 있습니다」 and 「이 상품은
  10년만기, 10년납 상품이며, 갱신을 통해 최대 100세(질병사망특약은 최대 80세)까지 보장됩니다」
  — but the **same block** also carries 「이 상품은 가입심사 기준이 완화된 간편심사 상품으로
  보험료가 높으며…」, which is plainly not true of this product, and an inline editorial
  comment (`250617 : 뇌심장 추가`). It is generic boilerplate covering several of the carrier's
  products. Against it: the 상품요약서 [S12] describes only 비갱신 terms and the disclosure
  [S4] flags the product **비갱신형**. The renewal statements on [S13] are therefore
  **[unverified]** and are not used; §8's Korean renewal mechanics rest on [S6], [S9] and
  [S15].
- **푸본현대's 예상 갱신보험료 basis.** [S16]'s basis line reads 「보험가입금액 1,000만원, 남자
  40세, **10년만기**, 전기납」 while [S15] states the product is **1년만기** with at most four
  renewals, and the table's own renewal ages (41/42/43/44) are annual. One of the two lines is
  wrong. The premium path is quoted as printed and the term is not asserted.
- **교보라이프플래닛's 표준체 40세 premium on the older product**: [S14] prints **17,000원** in
  one block and **17,100원** in another for what it describes as the same cell (§6.7). Both are
  quoted; neither is preferred.
- **The 예금자보호 1억원 effective date of 2025-09-01** [R17]. Confirmed by search across three
  official sources and by the 1억원 figure appearing in three retrieved carrier documents, but
  no primary 예금보험공사 or 금융위원회 page was fetched.
- **제10회 경험생명표's figures** [R14] — a news article, not the KIDI announcement. The
  평균수명 increase is reported as **2.8년 / 2.2년** by the article read; a different search
  summary gave 2.9년 for males. The article's own numbers are used.
- **The taxation of the death benefit** in the hands of a Korean beneficiary — the
  계약자/피보험자/수익자 triangle under 상속세 및 증여세법. No carrier document in this set
  addresses it and no 국세청 page was retrieved. `jplib` has the equivalent; krlib does not
  yet.
- **Expense loadings.** Every 상품요약서 defines 계약체결비용 and 계약관리비용 and **none
  publishes a rate** (§11). The only handle is the 보험가격지수 (§12). Any expense basis in
  `technical-notes.md` will be `[std]`.
- **Best-estimate lapse experience for term.** The 적용해지율 disclosures (§11) are *pricing*
  rates for the 무해지 form only, and no lapse rate at all is disclosed for a 표준형 term. The
  only experience datum retrieved is a whole-life one [R18]. A best-estimate term lapse basis
  will have to be `[std]`.
- **The numeric 경험생명표.** Not public; not retrieved; the library's mortality tables are
  `[std]` constructions (§18).

**Deliberate scope limits (not gaps):**

- 단체정기보험 (group term) and 신용생명보험 / 대출안심보험 were not researched. The latter's
  two 삼성생명 products appear in the disclosure table in §6 and are quoted for their premium
  level only; no document for either was retrieved and nothing is asserted about their
  decreasing-cover schedules.
- 변액정기보험 was not researched; the `variable_annuity` product covers the 특별계정
  machinery.
- The 제3보험 riders that ride on a Korean 정기보험 — 암진단특약, 뇌출혈진단특약,
  급성심근경색증진단특약, 입원·수술 특약 — are named where a 상품요약서 lists them and are
  researched in `cancer.md`, `ci-insurance.md` and `indemnity-medical.md`.
- 경영인정기보험's corporate tax treatment (손금산입 and the well-publicised mis-selling
  history) is out of scope; the product is covered here for its 체증 mechanism, its three-step
  저해지 schedule and its price level only.
- Reinsurance terms, commission scales and 사업비 by duration: nothing public was found, and
  nothing is asserted.
