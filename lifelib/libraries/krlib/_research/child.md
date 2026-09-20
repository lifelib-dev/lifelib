# 어린이보험 (children's insurance) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean **어린이보험** (*eorini boheom*, children's insurance) liability
cash-flow reference model — `Child_KR_S`, a monthly-grid product stating its deltas against
the `Cancer_KR_S` fixed-benefit (정액) 제3보험 chassis.

어린이보험 has no counterpart in `uslib`, `uklib`, `jplib`, `frlib` or `delib`. It is not a
juvenile whole-life policy and it is not an education endowment, although it descends from
one. It is a **bundled child health and liability contract**, written on a 손해보험 (non-life)
chassis far more often than on a 생명보험 one, sold overwhelmingly **in utero** — the
태아보험 (*taea boheom*, "foetal insurance") of ordinary Korean speech is nothing but an
어린이보험 to which a 태아가입특약 has been attached [R3] — and, since 2011, sold to
**100세 만기** (and now 110세 만기) on a child of 0 to 5, so that the contract is a
ninety-to-hundred-year guarantee written on a life whose morbidity has barely begun [R5].

Four structural facts make it worth a model of its own.

1. **The insured does not legally exist at inception.** A 태아 has no legal personality and
   so cannot be the 피보험자 of a 인보험 contract; the 태아가입특약 (or 태아가입특칙) works
   round this by making the foetus the insured **at birth** [R3] [S8]. Cover therefore
   attaches at birth, not at the 계약일 — the supervisor forced sixteen insurers to stop
   advertising otherwise in 2016 [R2] — and if the pregnancy ends in 유산 or 사산 the
   contract is void and the premiums are returned [S8] [S9].
2. **The issue-age envelope was a supervisory battleground and the fight is datable.**
   Carriers pushed the maximum issue age from 15 to 30 and then to 35 to keep new business
   flowing against a collapsing birth rate; the 금융감독원 stopped it on **2023-07-19**, with
   existing products to be amended by the end of August 2023 [R1]. The current generation
   accepts 태아~15세 [S2] [S4], where the 2019 and 2022 generations accepted 0~30세 [S1]
   [S7].
3. **The premium waiver is doubled up.** The base waiver is on the *child* — 50% disability
   or diagnosis of one of a named disease set — and the parent's death or disability is
   handled by a separate 부양자 (dependant-supporter) rider stack written on the parent's
   own life, alongside a 임신·출산질환 stack written on the mother's [S2] [S5]. On the
   생명보험 chassis the two collapse into one clause: the waiver triggers on the
   **계약자's** death or 50% disability as well as the child's [S10].
4. **The product is sold in 무해지 form.** Every one of the ten non-life carriers on the
   손해보험협회 comparison board offers a 해약환급금 미지급형 variant beside the 표준형,
   at a premium 25%–33% lower, whose surrender value is nil for the whole payment period and
   then steps to 50% (or 5%–50% on a graded scale) of the 표준형 value [S11] [S1] [S2]. The
   lapse assumption behind that step was the subject of a supervisory guideline on
   **2024-11-07** [R11].

**What this file is.** It is the provenance layer behind `products/child/`'s four documents —
`product-spec.md`, `technical-notes.md`, `model.md` and `sources.md` — and behind the
`Child_KR_S` model's parameter files. Every quantitative claim in those documents should be
traceable to a numbered entry here. **The source numbering below is never renumbered**: the
product documents cite against it, so `S3` means the same document forever. Facts are tagged
`[S#]` where they come from a retrieved primary product document, `[R#]` where they come from
a retrieved regulatory, statutory, supervisory or research reference, and `[unverified]` where
they rest on a search snippet or a document that could not be opened. Where a source is a news
article or a summariser's rendering rather than a primary document, the entry says so and the
dependent facts inherit that weakness.

**Retrieval method.** Plain `curl` reached `kpub.knia.or.kr` (손해보험협회 공시실),
`www.fss.or.kr`, `fsc.go.kr`, `www.kiri.or.kr`, `casenote.kr`, `hi.co.kr`, `hanalife.co.kr`,
`brand.metlife.co.kr`, `image.kebhana.com` and — intermittently — `direct.samsungfire.com`.
It was reset by peer for `www.law.go.kr` (after one success) and for
`direct.samsungfire.com`'s HTML pages. Korean PDFs were downloaded with a browser
User-Agent and extracted locally with `pypdf`; the 금융감독원's 2008 release exists only as
HWP5 and was extracted by inflating the OLE `BodyText` stream and decoding the
`HWPTAG_PARA_TEXT` records. `WebFetch` was used where `curl` failed and where a page is
JavaScript-rendered; its output is a summariser's rendering, not raw text, and every entry
that rests on it says so. Access date for every source: **2026-09-03**.

The single most productive source in this file is **[S11]**, the 손해보험협회's
어린이보험 comparison board, which returns a machine-readable dataset of every non-life
어린이보험 on sale — product name, channel, 예정이율, 공시이율 and its floor, specimen
male and female monthly premium on a standardised basis, 보험가격지수, and a direct download
link to each product's 상품요약서. Five of those 상품요약서 were downloaded and read.

---

## Primary sources

### S1 — 메리츠화재, 「무배당 내Mom같은 어린이보험1910 상품요약서」

- Publisher: 메리츠화재해상보험주식회사 (Meritz Fire & Marine Insurance)
- Document: 상품요약서, 80 pp., product code `1910` (2019-10 edition)
- Doc type: 상품요약서 (product summary — the statutory pre-contract summary)
- URL: https://kpub.knia.or.kr/file/download/25184.knia
- Accessed: 2026-09-03
- Retrieved: **yes** (588,656-byte PDF, 80 pp., 118,078 characters extracted cleanly,
  including all rate and cash-value tables)
- What it is good for: the **pre-2023 generation**, and the sharpest single exhibit of the
  age creep the supervisor later stopped. It carries the full 가입나이 grid (0~30세 on the
  100세만기 forms), the 태아 sub-term (`1~10월만기 전기납 태아 월납`), the five 형
  (표준형 / 계약전환형 / 해지환급금미지급형 Ⅰ, Ⅱ, Ⅲ), the 적용해지율 actually used to
  price the 무해지 forms, the 보장부분 적용이율 and 공시이율, a 보험가격지수 table by
  sex and form, the 저체중아·선천이상·출생위험 benefit definitions, and a complete
  published surrender-value grid on a named specimen contract.

### S2 — 현대해상, 「무배당 현대해상굿앤굿어린이종합보험Q(Hi2607) 상품요약서」

- Publisher: 현대해상화재보험주식회사 (Hyundai Marine & Fire Insurance)
- Document: 상품요약서, 98 pp., product code `Hi2607` (2607 = 2026-07 edition)
- Doc type: 상품요약서
- URL: https://kpub.knia.or.kr/file/download/91540.do
- Accessed: 2026-09-03
- Retrieved: **yes** (1,406,799-byte PDF, 98 pp., 153,931 characters extracted cleanly)
- What it is good for: the **current generation of the market's archetypal product**. The
  굿앤굿어린이 line is the descendant of the 2004-07 굿앤굿어린이CI보험, the
  best-selling child policy ever written in Korea [R5]. It gives 가입나이 **태아~15세**
  across every 만기; the three 종 (표준형 / 해약환급금 미지급형 / 보험기간 연장형); the
  waiver trigger set and its **P-code carve-out**; the 태아보장기간 = 계약일~출생일
  construction with the list of covers that attach to it; the **태아전용 보장** list on a
  1년만기 term; the 부양자 and 임신·출산질환 rider stacks with the parent's and mother's
  issue-age ranges; and three complete cash-value grids, one per 종.

### S3 — 메리츠화재, 「(무) 내Mom같은 어린이보험2607(1종)(1형) 상품요약서」

- Publisher: 메리츠화재해상보험주식회사
- Document: 상품요약서, 149 pp., product code `2607` (2026-07 edition)
- Doc type: 상품요약서
- URL: https://kpub.knia.or.kr/file/download/92812.do
- Accessed: 2026-09-03
- Retrieved: **yes** (953,278-byte PDF, 149 pp., 206,285 characters extracted cleanly)
- What it is good for: the **면책기간 / 감액기간 matrix**, benefit by benefit, and the two
  notes that matter most for a child model — that the 90-day cancer waiting period applies
  **only where 보험나이 is 15 or over**, and that a 태아가입용 rider has no waiting period
  at all. It is the same product line as [S1] seven years later, so the two together give a
  clean before-and-after on the 2023 supervisory action.

### S4 — KB손해보험, 「KB 금쪽같은 자녀보험Plus(무배당)(26.07) 1종 1형 상품요약서」

- Publisher: KB손해보험주식회사 (KB Insurance)
- Document: 상품요약서, 207 pp., product code `26.07`
- Doc type: 상품요약서
- URL: https://kpub.knia.or.kr/file/download/92757.do
- Accessed: 2026-09-03
- Retrieved: **yes** (3,035,628-byte PDF, 207 pp., 344,997 characters extracted; the
  extraction interleaves Korean and Latin runs within table cells, so the 가입나이 grid had
  to be read carefully, but it is legible)
- What it is good for: the **110세만기** form — the longest term found anywhere in this
  research — with 가입나이 태아, 0~15세; the fact that the 일반상해사망 basic cover is
  written only from 만 15세, which is 상법 제732조 showing through into the product
  structure; and a 태아 obligatory-rider block on a 1년만기 전기납 term.

### S5 — 롯데손해보험, 「무배당 let:play 자녀보험(도담도담)(2604) 6종 상품요약서」

- Publisher: 롯데손해보험주식회사 (Lotte Insurance)
- Document: 상품요약서, 299 pp. (147 pp. of extractable text), product code `2604`
- Doc type: 상품요약서
- URL: https://kpub.knia.or.kr/file/download/91786.do
- Accessed: 2026-09-03
- Retrieved: **yes** (2,046,981-byte PDF, 169,450 characters extracted)
- What it is good for: the **gestational-week enrolment limits stated in a primary document**
  — 임신 22주 이내 for the neonatal rider block and 임신 15주 이내 for one dental rider —
  the rule that a 태아 contract must carry one of a named set of 부양자 death riders, the
  full 가족일상생활배상책임 wording with its three per-occurrence limits and two
  deductibles, and the 손해보험 design constraint on 질병사망 riders (80세만기 이내,
  개인당 2억원 이내).

### S6 — NH농협손해보험, 「(무)NH아이맘헤아림어린이보험[2종:표준형]2604 상품요약서」

- Publisher: NH농협손해보험주식회사 (NH Nonghyup Property & Casualty)
- Document: 상품요약서, 81 pp., product code `2604`
- Doc type: 상품요약서
- URL: https://kpub.knia.or.kr/file/download/88346.do
- Accessed: 2026-09-03
- Retrieved: **yes** (803,926-byte PDF, 89,976 characters extracted)
- What it is good for: a carrier that **still applies a 감액기간** — its 암진단비 pays 50%
  within the first year, and its 항암방사선치료비 / 항암약물치료비 likewise — against the
  market's drift to 감액없음. Used in the carrier-variation table.

### S7 — 현대해상, 「무배당 현대해상다이렉트굿앤굿어린이보험(Hi2204) 약관」

- Publisher: 현대해상화재보험주식회사
- Document: 보험약관 (policy conditions) with 약관 이용 가이드북, 시각화된 약관 요약서,
  상품 안내, 보통약관, 특별약관 and 별표; 366 pp. by the PDF page count, 265 pp. of
  extractable text
- Doc type: 약관
- URL: https://www.hi.co.kr/data/202204/(무)현대해상다이렉트굿앤굿어린이보험(Hi2204)_인쇄용약관3_페이지.pdf
  (fetched percent-encoded)
- Accessed: 2026-09-03
- Retrieved: **yes** (5,774,914-byte PDF, 558,560 characters extracted; some 별표 pages are
  image-only)
- What it is good for: the **pre-2023 direct-channel product at 가입나이 0~30세**, the
  갱신형 architecture in its clearest form (20년만기 / 30년만기 with automatic renewal and
  renewal-age ceilings expressed as `(100-보험기간)세`), 제27조 보험나이 verbatim with the
  worked example, 제28조 계약의 소멸 and 제29조 계약의 자동갱신. This is a **direct**
  (internet-only) product and does not offer 태아가입.

### S8 — 하나생명, 「무배당 하나1Q어린이보험 약관」

- Publisher: 하나생명보험주식회사 (Hana Life Insurance)
- Document: 보험약관 including 무배당 주산기질환입원특약, 특정 신체부위·질병 보장제한부
  인수특약 and 지정대리청구서비스특약; 93 pp.
- Doc type: 약관
- URL: https://hanalife.co.kr/home/download2.do?downFileName=(무)하나1Q어린이보험_계약자용약관.pdf&fileName=PROD/(무)하나1Q어린이보험_보험약관.pdf
  (fetched percent-encoded; the server declares `application/x-msdownload`, the file is a PDF)
- Accessed: 2026-09-03
- Retrieved: **yes** (1,860,906-byte PDF, 93 pp., 136,222 characters extracted cleanly)
- What it is good for: **the 태아가입특칙 in full and verbatim** — 제53조 to 제61조 — which
  is the single most important text in this file. Also the 주산기질환 rider definition tied
  to the KCD 출생전후기에 기원한 특정 병태 chapter, the statement that the 태아형 pays
  cancer benefits without 감액, and a published 민원 case explaining that a 태아 contract
  is priced on **male** rates and trued up at birth.

### S9 — 하나생명, 「무배당 하나어린이보험 약관」

- Publisher: 하나생명보험주식회사
- Document: 보험약관, 119 pp. (an older wording; it still refers to 호적등본 rather than
  가족관계등록부, so it predates the 2008 family-register reform)
- Doc type: 약관
- URL: https://www.hanalife.co.kr/anm/product/download.do?code=603427&seq=1
- Accessed: 2026-09-03
- Retrieved: **yes** (616,651-byte PDF, 119 pp., 136,652 characters extracted cleanly)
- What it is good for: a **second, independent 태아가입특칙** — 제44조 to 제51조 — whose
  substance matches [S8] article for article, which is the evidence that the 특칙 is a
  market-standard text and not one carrier's drafting. Also a 보험금 지급기준표 on a
  ₩10,000,000 (1,000만원) 보험가입금액 basis, with the school-accident disability annuity
  grid that the older 어린이보험 generation carried.

### S10 — 메트라이프생명, 「무배당 어린이 종합보장보험 약관」

- Publisher: 메트라이프생명보험주식회사 (MetLife Korea)
- Document: 보험약관, 55 pp.
- Doc type: 약관
- URL: https://brand.metlife.co.kr/pn/mcvrgProd/mcvrgProdDownloadFile.do?insProdSeq=49&seq=6&fnum=03
- Accessed: 2026-09-03
- Retrieved: **yes** (525,870-byte PDF, 55 pp., 54,908 characters extracted; the extraction
  transposes trailing punctuation and parenthesised glosses to line ends, an artefact of the
  PDF's text ordering, but every clause is readable)
- What it is good for: the **생명보험 form of the waiver**, which is the one the brief names
  — 제22조 makes the waiver trigger on the child's cancer diagnosis or 50% disability **or**
  on the **계약자's death or 50% disability**. Also 제3조, which makes the 피보험자 of the
  contract *both* the 계약자 and the 가입자녀, and 제21조, which pays a 사망보험금 only
  where the child dies at or after 만 15세.

### S11 — 손해보험협회 공시실, 「어린이보험」 상품비교공시 (`tptyCode=PB24`)

- Board path: 상품비교공시 > 장기보장성 보험 > 어린이보험
- Publisher: 손해보험협회 (General Insurance Association of Korea, KNIA)
- Doc type: industry comparison disclosure (a regulated 비교공시 board, not marketing)
- URL (landing): https://kpub.knia.or.kr/productDisc/longTermGuarantee/juvenileInsurance.do
- URL (table popup): https://kpub.knia.or.kr/popup/disclosurePopup.do?tabType=1&tptyCode=PB24
- URL (data): `POST https://kpub.knia.or.kr/popup/disclosureList.do` with
  `tabType=1&tptyCode=PB24&detailYn=Y&pageIndex=1&pageUnit=100`
- Accessed: 2026-09-03
- Retrieved: **yes** — the landing page and the popup render as HTML; the table itself is
  loaded by AJAX and was obtained by posting the form directly, returning a 315,774-byte
  JavaScript-object payload covering **41 distinct products from 10 non-life carriers**, with
  89 distinct 담보 and their 지급사유
- What it is good for: it is the **quantitative spine of this file**. Every published
  premium, every 예정이율, every 공시이율 and 최저보증이율, every 보험가격지수 and the
  whole 무해지-versus-표준형 price gap below comes from it. It also gives the standardised
  comparison basis on which those premiums are quoted, and a `SUMMARY_SEQ` per product from
  which [S2] [S3] [S4] [S5] and [S6] were downloaded.

### S12 — 삼성화재, 「무배당 삼성화재 다이렉트 비갱신 어린이보험 2404.17 약관」

- Full title: 「무배당 삼성화재 다이렉트 비갱신 어린이보험(납입면제·해약환급금
  미지급형) 2404.17 보험약관」
- Publisher: 삼성화재해상보험주식회사 (Samsung Fire & Marine Insurance)
- Document: 보험약관, product code `2404.17`; 628,118 characters of extracted text
- Doc type: 약관
- URL: https://direct.samsungfire.com/CR_MyAnycarWeb/mall/pdf/mykids_zero.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (4,762,616-byte PDF; `curl` succeeded on this static asset even though
  the same host's HTML pages were reset by peer)
- What it is good for: a **비갱신 (non-renewable) 무해지 어린이보험** in its pure form, with
  the cover-page statement `0원 (납입기간 중 해지시) 해약환급금`; 제30조 보험나이 with the
  standard 6-month rule; and 제왕절개·다태아 definitions used in the mother-side riders.
  It carries no 태아가입특칙.

### S13 — 현대해상, 「무배당 현대해상다이렉트굿앤굿어린이보험(Hi2504) 약관」

- Publisher: 현대해상화재보험주식회사
- Document: 보험약관, product code `Hi2504` (2025-04 edition), 239 pp. by PDF page count,
  275 pp. of extractable text
- Doc type: 약관
- URL: https://direct.hi.co.kr/dhNAS/terms/CM205J_20250401.pdf
- Accessed: 2026-09-03
- Retrieved: **in part** — the PDF downloaded (5,060,088 bytes) and the 보통약관 and 특별약관
  extracted (561,535 characters), but the 상품 안내 issue-age grid, which is what this source
  was fetched for, is not in the extracted text (the section is laid out as images or the
  heading text differs from the Hi2204 edition). No fact in this file rests on it.

### S14 — 흥국생명, 「무배당 흥국생명 드림어린이보험1701(보장성) 보험약관」

- Publisher: 흥국생명보험주식회사 (Heungkuk Life Insurance)
- Document: 보험약관, 103 pp., 승인번호 상품개발 제16-AA1-0084호 (2017-01-01)
- Doc type: 약관
- URL: https://image.kebhana.com/cont/download/insdocument/provide/08L04B24102_agree.pdf
- Accessed: 2026-09-03
- Retrieved: **no** — HTTP 200, 1,256,989-byte PDF, 103 pp. downloaded successfully, but the
  file uses non-embedded CID-keyed fonts from page 2 onward and `pypdf` returned mojibake for
  every substantive line. Only the cover page (product name, insurer, approval number, the
  line 「이 상품은 보장성보험으로 저축성보험(연금)이 아닙니다」) extracted.
- Consequence: no 생명보험 어린이보험 wording from this carrier is used. The 생명보험 side
  of this file rests on [S8] [S9] and [S10].

### S15 — 삼성화재 다이렉트, 「어린이보험(태아가입)」 상품 페이지

- Publisher: 삼성화재해상보험주식회사
- Doc type: consumer product page
- URL: https://direct.samsungfire.com/m/mall/baby.html
- Accessed: 2026-09-03
- Retrieved: **no** — `curl` was reset by peer at the proxy; two `WebFetch` calls returned
  **mutually inconsistent** renderings, one naming a 삼성생명 product and one a 삼성화재
  product, with different premium figures. The page is JavaScript-rendered and the
  summariser is evidently reconstructing rather than reading.
- Consequence: **nothing is taken from it.** The 태아~15세 issue-age fact that it appeared to
  support is instead evidenced by [S2] and [S4], which are retrieved PDFs.

### S16 — NH농협생명, 「우리아이지킴이NH통합어린이보험(무배당)」 상품 페이지

- Publisher: NH농협생명보험주식회사 (NH Nonghyup Life)
- Doc type: consumer product page
- URL: https://www.nhlife.co.kr/ho/ig/HOIG0001M00.nhl?prodCd=N0000709
- Accessed: 2026-09-03
- Retrieved: **in part** — reached only through `WebFetch`, whose output is a summariser's
  rendering. It reports 가입나이 0~15세 (1종, 30세만기) and 0~20세 (2종, 100세만기), the
  태아 sub-term construction, and a 3대질병 납입면제 rider on the parent.
- Consequence: the figures are treated as **[unverified]** wherever used, and no parameter of
  the reference product is set from them.

---

## Regulatory and actuarial references

### R1 — 금융감독원, 「… 불합리한 보험상품 구조를 개선하였습니다」 (2023-07-19)

- Full title: 「보험회사의 건전성 악화 및 소비자 피해 우려가 없도록 불합리한 보험상품
  구조를 개선하였습니다.」
- Publisher: 금융감독원 (Financial Supervisory Service), 보험감독국 특수보험2팀
- Document: 보도자료, 3 pp.; 배포 2023-07-19(수), 보도 2023-07-20(목) 조간
- Doc type: 보도자료 announcing an immediate 감독행정 (supervisory administration)
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=129212&menuNo=200218
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa4f2c0a57b145c98c22c31aba142627&fileSn=2&bbsId=
- Accessed: 2026-09-03. Retrieved: **yes** (283,196-byte PDF, 3 pp., extracted verbatim)
- Content: **this is the datable supervisory action on 어린이보험.** It covers three products
  — 운전자보험, 어린이보험 and 단기납 종신보험(무·저해지) — and is quoted in full in §3
  below. For 어린이보험 the diagnosis is that extending 가입연령 to 35 led adults to buy a
  child-specialised product, and that carriers were bolting adult-disease covers (뇌졸중,
  급성심근경색) onto a child policy where their incidence is negligible; the remedy is a
  restriction on the **product name**, not on the issue age itself. Also states the deadline:
  existing products to be amended by the end of 2023-08.

### R2 — 금융감독원, 「어린이보험 관련 불합리한 관행 개선」

- Publisher: 금융감독원, 보험감리실 / 금융혁신국
- Document: 보도자료, 8 pp., file `160714_조간_어린이보험 관련 불합리한 보험약관 개선.pdf`;
  배포 2016-07-13(수), 보도 2016-07-14(목) 조간
- Doc type: 보도자료 (a 「제2차 국민체감 20大 금융관행 개혁」 work item)
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=12634&menuNo=200218
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=99a8ae3b7ea5edca3c2820c6835784be&fileSn=1&bbsId=
- Accessed: 2026-09-03. Retrieved: **yes** (669,507-byte PDF, 8 pp., extracted verbatim
  including both annexes)
- Content: the definitive supervisory statement that **cover under a 태아 contract attaches
  at birth**, the sixteen insurers and nineteen products ordered to stop advertising
  otherwise, the market statistics for 2013–2015, and the 2015 변경권고 that removed the
  감액 (reduced-benefit) clause for contracts taken out while the insured was a foetus —
  with the before-and-after 약관 wording set out side by side.

### R3 — 금융감독원, 「태아보험 가입시 알아두면 유익한 사항」

- Publisher: 금융감독원, 보험계리실 손해보험팀/생명보험팀
- Document: 정례브리핑 자료, 총 9매, file
  `080627(태아보험 가입시 알아두면 유익한 사항)_2488.hwp`; 배포 2008-06-24,
  보도 2008-06-27(금) 조간
- Doc type: 보험소비자 유의사항 briefing (the eighth in a series)
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=6703&menuNo=200218
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=2576a0971b2b228016d400a6a24b1b65&fileSn=1&bbsId=
- Accessed: 2026-09-03. Retrieved: **yes** (137,216-byte HWP5; extracted by inflating the OLE
  `BodyText/Section0` stream and decoding the `HWPTAG_PARA_TEXT` records, 9 pp. of text plus
  both 참고자료)
- Content: **the best single explanation of what a 태아보험 is and why.** Definition, the
  legal-personality problem, the standard rider set and its definitions, the enrolment
  window, the treatment of foetal death, the male-rate pricing convention, a worked claim
  example with itemised amounts, and — 참고자료2 — 어린이보험 신계약건수 and 수입보험료
  **split between 생명보험 and 손해보험** for FY05–FY07 with the 태아 share.

### R4 — 금융감독원, 「쌍둥이도 태아보험에 모두 가입할 수 있습니다」

- Publisher: 금융감독원, 보험감독국 보험업무팀
- Document: 보도참고자료, 2 pp.; 등록일 2012-09-11
- Doc type: 보도참고자료
- URL (post): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=9460&menuNo=200218
- Accessed: 2026-09-03. Retrieved: **in part** — the board page's own summary block was read
  in full from the HTML, but the attached PDF (273,602 bytes, 2 pp.) is a **scanned image**
  and yielded 41 characters of text; the 문서뷰어 returns only a loading placeholder.
- Content used, verbatim from the page summary: 「현행 태아보험 쌍둥이를 임신(출산)할 경우,
  그 중 한명만을 보장대상으로 하고 나머지는 보장 대상에서 제외하고 있어 보험혜택의
  사각지대가 발생 ◦ 2012.10.1.부터 다태아 모두를 태아보험 피보험자로 가입할 수 있도록
  추진」. Nothing further from this release is used; the 다태아 pricing consequences are
  taken from [R5] instead.

### R5 — 보험연구원, 「Ⅷ. 어린이보험의 성장」, 연구보고서 2018-5

- Full title: 연구보고서 2018-5 『보험상품 변천과 개발 방향: 생명보험 상품 중심』,
  Ⅷ장
- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI); 김석영·김세영·이선주,
  2018-02
- Document: chapter Ⅷ, pp. 221–245 (25 pp. as extracted)
- Doc type: 연구보고서 chapter
- URL: https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2018-05_08.pdf (fetched
  percent-encoded)
- Accessed: 2026-09-03. Retrieved: **yes** (1,100,236-byte PDF, 22,638 characters extracted;
  the figures are images and their captions only partly extracted, and two table cells lost a
  trailing character — 「뇌성마비진」, 「저체중아보」 — which is an extraction artefact)
- Content: **the history of the product, with dates.** 1958-07 진학보험; the decline of
  교육보험 after 1990; the 1997 arrival of 어린이 보장성 상품; the 2000 introduction of the
  태아가입특약; 2003 신한생명 and 2004-07 현대해상 어린이 CI보험; the 2005 addition of
  high-cost critical-illness benefits; the **2006 removal of the 90-day cancer waiting period
  for 어린이보험**; the 2011 move to 100세 만기; the 2013 P-code neonatal-haemorrhage dispute
  and its loss-ratio consequences; the 2018-vintage view of the long-guarantee risk under
  IFRS 17; and a premium-by-issue-age index that is directly usable as a model sanity check.

### R6 — 금융위원회, 「저출산 극복 지원 3종 세트」 시행 (2026-03-31)

- Full title: 「보험업권이 출산‧육아에 따른 보험료 부담을 덜어드립니다 — 4.1일,
  「저출산 극복 지원 3종 세트」 시행」
- Publisher: 금융위원회 (Financial Services Commission), 보험과
- Document: 보도자료, 6 pp.; 배포 2026-03-31(화) 09:00, 보도 2026-04-01(수) 조간
- Doc type: 보도자료
- URL (post): https://fsc.go.kr/po010101/86598
- URL (file): https://fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=86598&fileTy=ATTACH&fileNo=2
- Accessed: 2026-09-03. Retrieved: **yes** (284,255-byte PDF, 6 pp., extracted verbatim)
- Content: **the market-size figure this file needed.** It states 어린이보험 annual premium
  as **₩9.4조원** and all 보장성 인보험 annual premium as about **₩42.7조원**, both as at
  2026-03. It also describes the 1%–5% 어린이보험 premium discount for a year on birth or
  parental leave, effective 2026-04-01 at every insurer, and — importantly for a lapse and
  premium model — the fact that 어린이보험 is **excluded** from the companion
  premium-deferral scheme.

### R7 — 상법 제732조 (15세미만자등에 대한 계약의 금지) and 제739조 (준용규정)

- Publisher: 대한민국 법률; retrieved through CaseNote's statute mirror
- Version shown on the CaseNote page for 제732조: [시행 2015. 3. 12.] [법률 제12397호,
  2014. 3. 11., 일부개정]
- Doc type: statute (mirror)
- URL: https://casenote.kr/법령/상법/제732조 (fetched percent-encoded)
- Accessed: 2026-09-03. Retrieved: **yes** (56,957-byte HTML; the article text is served in
  both 한글 and the original 한자 forms, together with the amendment history and 25 citing
  judgments)
- Content: 제732조 verbatim — 「15세미만자, 심신상실자 또는 심신박약자의 사망을 보험사고로
  한 보험계약은 무효로 한다. 다만, 심신박약자가 보험계약을 체결하거나 제735조의3에 따른
  단체보험의 피보험자가 될 때에 의사능력이 있는 경우에는 그러하지 아니하다.」 제739조,
  read from a copy of the 상법 [시행 2026. 7. 23.] [법률 제20991호, 2025. 7. 22., 일부개정]
  held in this session's working directory: 「상해보험에 관하여는 제732조를 제외하고
  생명보험에 관한 규정을 준용한다.」
- Note on retrieval: `www.law.go.kr` served one request and then reset the connection on
  every subsequent attempt; the friendly `/법령/상법/제732조` form and the DRF service both
  failed (connection reset and HTTP 500 respectively). CaseNote is therefore the retrieval
  route for the statute, and the 제739조 text above is from a session copy whose own
  retrieval this pass could not repeat — see **Fetch failures and gaps**.

### R8 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2026.5.6. 시행), 질병·상해보험 표준약관

- Publisher: 금융감독원, as an annex to the 보험업감독업무시행세칙 (제5-13조제1항 관련)
- Document: `[별표 15] 표준약관(제5-13조제1항관련)(보험업감독업무시행세칙).hwp`, 1,717,248
  bytes, posted 2026-06-15, stated 「'26.5.6. 시행」
- Doc type: **표준약관** — the supervisor-issued standard policy conditions, of which the
  질병·상해보험 wording (pp. 142–202 of the compiled annex) is the one an 어린이보험 is
  written on
- URL (post): https://www.fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=218364
- URL (file): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=29447dbe2fa84d85881c10281c6b9d38&fileSn=1&bbsId=
- Accessed: 2026-09-03. Retrieved: **yes** for the file (1.7 MB HWP5 downloaded in this pass);
  the article text quoted below was read from a decoded copy of the same annex held in this
  session's working directory, whose table of contents matches the downloaded file
  (Ⅰ.생명보험 / Ⅱ.손해보험 1.화재 2.자동차 3.질병·상해 4.실손의료보험 with the 5세대
  특별약관1·2 / 5.해외여행 실손 / 6.배상책임 …)
- Content used: 질병·상해보험 표준약관 제19조(계약의 무효) 제2호 and 제3호 — a contract on
  the death of a person under 만15세 is void, and the age-eligibility saving in 제3호
  expressly does **not** extend to the under-15 death prohibition; 제21조(보험나이 등) — the
  6-month rounding rule with its worked example. The 생명보험 표준약관 carries the same two
  provisions at 제19조 and 제21조.

### R9 — 금융위원회, 「… 실손의료보험 끼워팔기가 금지됩니다」 (2018-03-30)

- Full title: 「4월부터 "유병력자 실손의료보험"이 출시되고, 실손의료보험 끼워팔기가
  금지됩니다」
- Publisher: 금융위원회
- Document: 보도자료, 2018-03-30
- Doc type: 보도자료
- URL: https://www.fsc.go.kr/po010101/73088
- Accessed: 2026-09-03. Retrieved: **yes** via `WebFetch` (the page renders; the output is a
  summariser's rendering of it, and the quoted sentence and the regulation citation below are
  reproduced from that rendering)
- Content: from April 2018, 실손의료보험 — including 유병력자실손 — must be sold as a
  **standalone product** consisting only of indemnity-medical cover: 「4월부터 유병력자
  실손의료보험을 포함한 실손의료보험 상품은 실손의료 보장으로만 구성된 단독상품으로
  분리·판매토록 규정」, under 보험업감독규정 §7-63②1호 as amended 2017-03-22 with a
  one-year transition. **This is why a modern 어린이보험 has no 실손 rider** — see §11.

### R10 — 보험업감독규정 제7-63조 (제3보험의 보험상품설계 등)

- Publisher: 금융위원회고시
- Doc type: 행정규칙 (supervisory regulation)
- URL attempted: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000246213 and
  https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246213
- Accessed: 2026-09-03. Retrieved: **in part** — `curl` returned HTTP 000 (connection reset)
  on both forms and `WebFetch` on the first returned 「해당 행정규칙이 존재하지 않습니다」.
  The article text quoted below was read from a copy of the 보험업감독규정
  **[시행 2023. 3. 2.] [금융위원회고시 제2023-10호]** held in this session's working
  directory; its own retrieval could not be repeated in this pass and its URL is not known
  to me.
- Content used: 제7-63조제2항제1호 — 「실손의료보험은 영 제42조의5제1항에 따른
  실손의료보험계약으로만 구성된 보험상품으로 판매하고, 그 보험계약은 주계약과 주계약에서
  보장하지 않는 대상을 보장하는 특약으로 구성할 것. 다만, 단체보험상품 및 여행보험상품의
  경우에는 실손의료보험계약을 포함하여 판매할 수 있다.」 (개정 2017. 3. 22.) The same
  article's 제1항제1호 requires that a 제3보험 contract pay the 계약자적립액 and unearned
  premium and terminate on a death not covered by the 약관.
- Because the retrieval could not be repeated, every fact resting **only** on this entry is
  additionally supported by [R9], which cites the same article, and is otherwise marked.

### R11 — 금융위원회·금융감독원, 계리가정 및 할인율 보도자료 (2024-11-07)

- Full title: 「합리적인 계리가정과 단계적 할인율 조정을 통해 보험회계의 신뢰도와
  안정성을 높이겠습니다」
- Publisher: 금융위원회 and 금융감독원, 제4차 보험개혁회의
- Document: 보도자료, 2024-11-07
- Doc type: 보도자료 announcing the IFRS 17 계리가정 guideline
- URL: https://www.fsc.go.kr/no010101/83351
- Accessed: 2026-09-03. Retrieved: **yes** via `WebFetch` (the page renders; the quoted
  fragments below are reproduced from that rendering, and were cross-checked against a decoded
  copy of the same release held in this session's working directory)
- Content: the **2024 intervention on the 무·저해지 lapse assumption** — a log-linear model
  as the 원칙모형 with the lapse rate converging to **0.1%** at 납입완료, a post-completion
  ultimate lapse of **0.8%** (or a 20% relative to the 표준형 product's rate), and the
  industry statistic that 무·저해지 products rose from **11.4%** of 보장성 초회보험료 in
  2018 to **30.4%** in 2021, **47.0%** in 2023 and **63.8%** in the first half of 2024.
  어린이보험 is not named in the release, but every 무해지 어린이보험 form in [S11] is
  inside its scope.

### R12 — 손해보험협회 공시실, 「어린이보험」 비교공시 기준 (the standardised comparison basis)

- Publisher: 손해보험협회
- Doc type: the 가입기준 block printed on the 어린이보험 comparison page — a
  supervisor-sanctioned standard specification, reproduced here because every premium in
  [S11] is quoted on it
- URL: https://kpub.knia.or.kr/productDisc/longTermGuarantee/juvenileInsurance.do
- Accessed: 2026-09-03. Retrieved: **yes** (HTML fetched with `curl` and converted to text)
- Content: 어린이보험 is defined as 「태아·어린이를 포함한 성장기 자녀에게 발생할 수 있는
  질병과 상해위험을 보장하는 보험」. The comparison basis is 상해 1급; 보험가입금액
  상해후유장해 ₩100,000,000 (1억원), 질병후유장해 ₩10,000,000 (1천만원), 진단비 담보 for
  암(소액암 제외)·뇌출혈·급성심근경색증 ₩10,000,000 (1천만원) each, the corresponding
  수술비 담보 ₩5,000,000 (500만원) each, 입원비 담보 ₩40,000 (4만원), 배상책임 담보
  ₩100,000,000 (1억원); term and payment 100세만기 / 20년납 for 세만기 covers and
  최장만기 / Min(전기납, 20년납) for 년만기 and 갱신형 covers; the quoted premium is the
  보장보험료 of the compulsory covers only.

### R13 — 보험개발원 (KIDI) statistics

- Publisher: 보험개발원 (Korea Insurance Development Institute)
- Doc type: statistical service
- URLs seen: https://www.kidi.or.kr/user/nd87617.do (보험통계 서비스),
  https://www.kidi.or.kr/user/nd11592.do (보도자료),
  https://incos.kidi.or.kr:5443/insInfo/selInfobookIncoList.do (INCOS)
- Accessed: 2026-09-03. Retrieved: **no** — the entry points were identified from search
  results only; no KIDI page was opened and no KIDI table was downloaded in this pass.
- Consequence: the 어린이보험 new-business and in-force series attributed to 보험개발원 in
  this file comes **second-hand, through [R2]**, which cites 보험개발원 as its source. The
  current-year equivalents are a gap.

---

## Fact extraction

### 1. What the product is, and the two chassis it is written on

- 어린이보험 is defined by the industry disclosure board as 「태아·어린이를 포함한 성장기
  자녀에게 발생할 수 있는 질병과 상해위험을 보장하는 보험」 [R12]. The supervisor's older
  formulation is 「자녀의 성장 과정 중 발생할 수 있는 질병·상해로 인한 의료비와 자녀의
  일상생활 중 발생하는 배상책임 등을 보장하는 보험상품(가입연령 : 0세~15세)」 [R2].
- Structurally it is a **basic contract plus a very large rider stack**. The basic contract at
  every non-life carrier examined is a 상해후유장해 (accidental disability) cover paying
  가입금액 × 장해지급률 [S1] [S2] [S4] [S5] [S11]; everything else — cancer diagnosis,
  cerebrovascular and ischaemic-heart diagnosis, surgery, hospital cash, fracture, burn,
  liability, the foetal covers, the parent covers — is a 특별약관.
- The rider count is extreme and is a deliberate competitive strategy. [R5] records that by
  2018 a child policy carried 「100여개 이상의 질병 및 상해사고에 대한 보장 담보」. [S1]'s
  eligibility section lists the riders in continuous prose over several pages; [S2]'s runs to
  roughly forty pages of tables.
- **It is written under both licences.** 제3보험 (상해·질병·간병) may be written by either a
  life or a non-life insurer, so 어린이보험 exists on both chassis. In practice the
  protection product is a non-life product: [R5] states that 「어린이 보장성 상품은
  손해보험회사를 중심으로 판매되고 있으며, 생명보험회사는 변액과 연금의 강점을 내세워
  어린이 저축성 상품 시장을 선점」, and attributes the split to the fact that only a
  non-life insurer may attach 배상책임담보 and 비용담보.
- The 손해보험협회 board lists **41 products from 10 non-life carriers** — 메리츠화재,
  한화손보, 롯데손보, 흥국화재, 삼성화재, 현대해상, KB손보, DB손보, 카카오페이손해보험,
  농협손보 [S11].
- On the 생명보험 chassis the contract is drafted differently: at one carrier the 피보험자 is
  **both the 계약자 and the 가입자녀** (「이 계약의 보험대상자(피보험자)는 계약자와
  가입자녀로 합니다」), which is what lets the same policy waive premiums on the parent's
  death without a separate rider [S10 제3조].
- Naming is not standardised. 어린이보험, 자녀보험, 아이보험, 태아보험 and branded names all
  appear; the 2023 restriction bites on the name rather than the design [R1], so a product
  sold to older children may be renamed rather than restructured.

### 2. Product history, with dates

All from [R5] unless otherwise marked.

- **1958-07** — 대한교육보험 (now 교보생명) launches 진학보험, Korea's first education
  endowment, at the company's foundation. A ₩1,000,000 sum bought ₩167,000 at university
  entry and seven further payments totalling ₩119,000; premiums were waived during military
  service or a leave of absence.
- **1960s–1980s** — 교육보험 is the dominant individual product; over half the individual
  market at its peak.
- **from 1990** — 교육보험 declines as tuition inflation outruns the benefit and household
  spending shifts to private tutoring.
- **1997** — the first true 어린이 보장성 상품, 삼성생명 「꿈나무 사랑보험」: 가입연령
  2~14세, 보험기간 15년/20년만기 or 18세/22세만기, with 사망위로금 (returning premiums if
  death occurs before 15), 장해치료비, 특수교육비, 질병재해입원비, 1~3종 수술비,
  응급치료비 and a cancer benefit set.
- **2000** — the **태아가입특약** is introduced and rapidly becomes standard; [R5] calls it
  the single largest contributor to the product's growth.
- **2003** — 신한생명 launches the market's first 어린이 CI보험.
- **2004-07** — 현대해상 launches 굿앤굿어린이CI보험, which [R5] describes as the
  best-selling child policy in the industry as at 2017. Its original specification is
  reproduced in the report: 주피보험자 **태아~15세**, 피부양자 20~50세, 보험기간
  15세/18세/20세만기, with 다발성 소아암, 중증 화상 및 부식, 3대 장애 (시각·청각·언어),
  5대 장기이식수술, 조혈모세포이식수술, 심장관련 소아특정질병, 어린이 12대 다발성 질병,
  일상상해·질병입원 실손의료비, 자녀안심 보험금 (약취·유인·폭행), 자녀 배상책임,
  저체중아(2.5kg 이하) 육아비용, 출생전후기질병 입원, 선천이상수술, 모성사망, and a
  자녀양육비 확정연금 on the 피부양자's death or 80% disability.
- **2005** — high-cost critical-illness benefits (말기신부전 진단, 재생불량성빈혈 진단,
  5대장기이식수술) are added, moving the product away from a leukaemia-and-childhood-cancer
  focus toward low-frequency, high-severity cover.
- **2006** — the **90-day cancer waiting period is removed for 어린이보험**, on the reasoning
  that there was no evidence of anti-selection or of a 위험률차손 at child ages. This is the
  origin of the rule still visible in current wordings — see §9.
- **2006** — 미래에셋생명 launches the first child variable-universal product, opening the
  life insurers' retreat into the savings half of the market.
- **2010** — outpatient (통원) riders are added and immediately produce poor experience:
  frequent infant colds and fevers, accumulated and claimed together with the 실손 rider,
  push the loss ratio up. The supervisor subsequently discourages further outpatient
  development outside serious disease.
- **2011** — 동양생명 leads the move to **100세 만기**; within a short period a
  hundred-year term becomes the market norm, with adult-disease covers bolted on for the
  post-30 段 of the term.
- **2012-09-11 → 2012-10-01** — the 금융감독원 requires that **all** foetuses of a multiple
  pregnancy be insurable, ending the practice of covering only the first-born [R4]. Carriers
  respond with 다태아플랜 riders priced at roughly a multiple of the single-foetus premium
  (2× for twins, 3× for triplets), which [R5] notes is probably an under-statement of the
  true risk.
- **2013-09** — the 금융감독원 requires that neonatal claims be paid on the diagnosis name
  rather than the KCD code, ending refusals of 뇌출혈 claims coded **P52** (신생아 뇌출혈)
  rather than in the I chapter. Claim frequency and the loss ratio rise sharply and carriers
  tighten 뇌졸중 진단비 underwriting limits on 태아·어린이 business.
- **2015-06-17 → 2016-04** — the 금융감독원 recommends, and carriers implement, removal of
  the first-year 50% 감액 for contracts written while the insured was a foetus; 17 carriers
  and 56 products were covered [R2].
- **2016-07** — sixteen carriers and nineteen products are ordered to correct advertising
  implying that cover attaches before birth [R2].
- **2023-07-19 → 2023-09** — the age-creep intervention [R1]; see §3.
- **2026-04-01** — an industry-wide 1%–5% 어린이보험 premium discount for a year on birth or
  parental leave [R6]; see §17.

### 3. The 2023 supervisory action — quoted, because it is easy to get wrong

The action is a **감독행정** (supervisory administration), not a rule change, announced by the
금융감독원 in a 보도자료 distributed **2023-07-19** for publication in the morning papers of
**2023-07-20**, with existing products to be amended by the end of **2023-08** [R1]. It is
therefore effective in practice from **September 2023**.

The 어린이보험 section reads, verbatim [R1]:

> **2 어린이보험**
> □ (현황 및 문제점) 가입연령을 35세까지 확대함에 따라 어린이 특화 상품에 성인이
> 가입하는 등 불합리한 상품 판매 심화
> ◦ 또한, 어린이에게 발생빈도가 극히 희박한 뇌졸중, 급성심근경색 등 성인질환 담보를
> 불필요하게 부가
> □ (추진방안) 최대 가입연령이 15세를 초과하는 경우 '어린이(자녀)보험' 등 소비자 오인
> 소지가 있는 상품명 사용 제한

and the implementation paragraph reads:

> □ 소비자 피해 방지 및 보험회사의 건전성 제고를 위해 어린이보험, 운전자보험, 단기납
> 종신보험의 상품구조 개선을 위한 감독행정을 즉시 시행하고,
> \* 단, 기존 판매상품은 '23.8월말까지 개정 필요

Three things follow that a specification must get right.

1. **The measure restricts the product name, not the issue age.** A carrier remains free to
   sell a policy at issue ages above 15; it may not call it an 어린이보험 or a 자녀보험. In
   practice every carrier chose to cut the age, and the current 상품요약서 show 태아~15세
   [S2] [S4].
2. **The stated motive is twofold** — adults buying a child-specialised product, *and* adult
   disease covers (뇌졸중, 급성심근경색) attached to a child policy where their incidence is
   negligible. The second limb matters for a morbidity basis: it is a supervisory statement
   that the adult-disease riders on a 100세만기 child policy are priced on an exposure that
   barely exists for the first three decades of the term.
3. **The release's framing is prudential, not only conduct.** The opening paragraph names
   「보험계약마진(CSM) 증대 등을 위한 불합리한 보험상품 개발·판매」 as the cause; the same
   release restricts 단기납 종신보험 유지보너스 and 운전자보험 terms, and flags that the
   무·저해지 lapse assumption would be dealt with separately 「금년 중」 — which it was, in
   [R11].

**The age creep itself, evidenced.** The pre-action generation of the same two product lines
carries these issue ages:

| Product | Edition | 가입나이 (100세만기 forms) | Source |
|---|---|---|---|
| 메리츠화재 내Mom같은 어린이보험1910 | 2019-10 | 0 ~ 30세 | [S1] |
| 현대해상다이렉트굿앤굿어린이보험(Hi2204) | 2022-04 | 0 ~ 30세 | [S7] |
| 현대해상굿앤굿어린이종합보험Q(Hi2607) | 2026-07 | 태아 ~ 15세 | [S2] |
| KB 금쪽같은 자녀보험Plus(26.07) | 2026-07 | 태아, 0 ~ 15세 | [S4] |

The 35 figure named in [R1] is not visible in any retrieved product document — the two
pre-action products retrieved both stop at 30. That two carriers went to 35 in 2023 is a
**[unverified]** claim resting on news reports (KB손해보험 and 롯데손해보험 are named), and
is not asserted anywhere in the product documents.

### 4. 태아가입 — the mechanism, verbatim

This is the part of the product with no analogue anywhere else in the repository, and it is
worth quoting rather than paraphrasing. The wording below is 하나생명's 태아가입특칙, 제53조
to 제61조 [S8]; 하나생명's older 어린이보험 carries the same 특칙 at 제44조 to 제51조 with
호적 references instead of 가족관계등록부 [S9].

- **제53조 (특칙의 적용)** 「이 특칙은 피보험자로 될 자가 계약체결시 태아(胎兒)인 계약에
  한하여 적용합니다.」
- **제54조 (피보험자)** 「제53조(특칙의 적용)의 태아(이하 "태아"라고 합니다)는 출생시에
  피보험자가 됩니다.」 — the insured comes into existence **at birth**.
- **제55조 (출생통지)** the policyholder must notify birth immediately, with a 통지서,
  the child's 가족관계등록부 or 주민등록등본, and the 보험증권; the fact is endorsed on the
  back of the policy.
- **제56조 (유산 또는 사산시의 처리)** 「① 태아가 유산 또는 사산에 의해 출생하지 못한
  경우에는 계약을 무효로 합니다. … ③ 제2항의 통지가 있는 경우 이미 납입한 보험료를 돌려
  드립니다.」 — the contract is **void**, not lapsed, and the whole premium is returned.
- **제57조 (복수(複數)출생의 경우)** on a multiple birth the policyholder may nominate each
  child as an insured; where only one contract was written, one child is nominated and the
  others may be made the insured of new contracts. If the nominated child dies within a year
  of birth and a twin survives, the policyholder may substitute the survivor within a month,
  with retroactive effect to the date of death — unless a benefit or reserve has already been
  paid or claimed, or the policyholder killed the child intentionally.
- **제58조 (보험금 지급기준 적용나이)** 「보험금 지급기준표에서 적용하는 피보험자 나이는
  피보험자가 출생한 날부터 계산합니다.」
- **제59조 (출생전 보험금 지급사유 발생)** 「피보험자의 출생전에 제12조(보험금의
  지급사유)에서 정한 보험금 지급사유가 발생한 경우에는 피보험자가 출생한 날부터
  제12조(보험금의 지급사유)에 따라 지급합니다.」 — an event occurring before birth is paid,
  but **from the date of birth**.
- **제60조 (계약나이의 계산 특례)** 「계약일에 있어서의 피보험자의 계약나이는 0세로
  합니다.」 — a foetus is priced as age 0.
- **제61조 (계약일 및 계약나이의 변경)** where the child is born **more than six months
  after the 계약일**, the 계약일 is moved back to the date six months before the birth, the
  계약나이 is re-set accordingly, and premiums and reserves are adjusted under the
  산출방법서. This is a real actuarial mechanic and not a formality: it caps the pre-birth
  exposure period at six months of policy age.

The supervisor's own explanation of why the 특칙 exists [R3]:

> 법규 상 '태아보험'이라는 별도의 보험상품은 없으나, 어린이보험에 태아가입특약(胎兒加入
> 特約)이 첨부되어 출생 전 태아 상태에서 보험가입이 가능한 상품을 실무적으로 '태아보험'
> 으로 지칭하고 있음
> \* 태아는 법적으로 인격(人格)을 갖지 못하므로 인보험의 보호대상이 될 수 없음. 따라서
> 태아의 출생을 조건으로 하는 '태아가입특약'을 통해 태아를 대상으로 한 보험계약을 체결

and, in one line: 「태아보험 = 어린이보험 + 출생시 위험보장」 [R3].

**When cover attaches.** [R3]: 「태아보험의 피보험자(보험보호의 대상)는 태아 그 자체가
아니라 출생 후 신생아이므로 … 태아보험의 보장은 일반적인 보험과는 달리 보험가입 시점이
아니라 태아의 출생 직후부터 시작됨.」 [R2] makes the same point and enforces it: sixteen
carriers were required in July 2016 to stop using phrases such as 「태아 때부터 보장」,
「엄마 뱃속에서부터 보장」, 「태어나기 전부터 보장」, 「태아 때부터 병원비 걱정이 없는」
and even the bare word 「태아보험」 in marketing material, under 보험업감독규정 제4-35조제3항
[R2].

**Foetal death is not covered.** [R3]: 「상법 제732조에서는 15세미만자의 사망을 보험사고로
한 보험계약은 무효로 하고 있으며, 또한 태아는 법적으로 인격을 갖지 못하여 인보험의
보호대상이 될 수 없으므로 … 태아보험에서는 태아의 사망을 직접적으로 보장하지는 아니함.」
What exists instead is mother-side cover — 유산 수술·입원일당·위로금 — and, in some
운전자보험, a 태아사산위로금특약 [R3].

**Multiple birth, before and after 2012.** [R3] (2008): 「태아보험에서는 쌍둥이 출생시
일반적으로 먼저 출생한 1인만을 보장하고 있으므로, 나중에 태어나는 자녀의 경우에는 출생 후
어린이보험에 가입하여야 함.」 [R4] (2012): from 2012-10-01 all foetuses of a multiple
pregnancy may be insured. [S8 제57조] is the post-2012 wording and [S9 제48조] the pre-2012
one (「태아가 복수로 출생한 경우에는 호적상 선순위로 기재된 자를 가입자녀로 합니다」) — a
clean before-and-after within one carrier's own book.

**Sex is unknown at inception, so the contract is priced male.** [R3]: 「보험료는 일반적으로
피보험자의 성별에 따라 다르지만, 태아보험 가입시 태아의 성별을 구별하기가 어려운 점
때문에, 일단 남자 아이를 기준으로 납입보험료가 산정되고 출산 후 성별대로 정산하는 구조로
이루어짐 \* 통상 여아의 경우 남아에 비해 보험료가 싸기 때문에 태아보험 가입 후 여아가
출생하는 경우 보험료 차액을 환급.」 The same convention appears in a carrier's published
민원 case: 「어린이보험을 태아로 가입할 때에는 자녀의 성별이 남자로 가입되며, 이후
여자아이가 태어난 경우 보험료 정산이 이루어집니다」 [S8]. Note that the current published
premium tables do **not** always show male below female — see §14 — so "male is cheaper" is
no longer reliably true and the direction of the true-up is product-specific.

### 5. The enrolment window

- **The supervisor's 2008 statement**: 「일반적으로 임신이 확인되는 순간부터 최장 임신
  24주까지만 가입이 가능하도록 운용 \* 태아보험의 가입가능기간은 회사별·상품별로 상이함」,
  and the reason: 「최근 의료기술의 발달로 임신 중 검사 등을 통해 태아의 기형이나 이상유무를
  확인할 수도 있으므로, 이에 따른 역선택을 방지하는 차원에서」 [R3].
- **KIRI's 2018 statement**: 「일반적으로 산모가 임신한 지 8주가 지난 후부터 24주까지만
  가입이 가능하도록 제한을 두고 있다」 [R5] — the same upper bound with a lower bound added.
- **A current primary document** gives a tighter bound. [S5] states, rider by rider:
  「저체중아육아비용 특별약관, 극소저체중아육아비용 특별약관, 출생위험보장 특별약관,
  신생아입원비(4일-120일) 특별약관, 신생아기흉진단비 특별약관, 신생아수두진단비 특별약관은
  **임신 22주 이내의 태아까지 가입 가능**」 and 「구순구개열치과교정및악정형치료비
  (급여,연간1회한) 특별약관은 **임신 15주 이내의 태아까지 가입 가능**」.
- So the window is **rider-specific, not contract-specific**: the contract may be written
  later, but the neonatal riders close at 22 weeks and at least one dental rider at 15 weeks
  [S5]. A widely repeated claim that 손해보험 accepts from confirmation of pregnancy to 22
  weeks while 생명보험 accepts only from 16 to 22 weeks appears in consumer guides and is
  **[unverified]** — no retrieved primary document states a lower bound.

### 6. 태아 covers — what they are and how they are termed

**The 태아보장기간 is a policy term in its own right.** [S2] states: 「아래의 계약은 계약을
체결할 때 피보험자가 될 자가 출생전자녀(태아)인 경우 계약체결일부터 출생시점(출산 또는
분만 과정에서 보험금 지급사유가 발생하는 경우 포함)까지의 기간을 보험기간으로 하여 아래의
보험기간 및 보험료 납입기간을 추가로 부가합니다」, and then tabulates a large block of
covers with 보험기간 = **태아보장기간 (계약일~출생일)**, 보험료 납입기간 = 전기납,
가입나이 = 태아. [S1] does the same with a fixed 보험기간 of **1~10월만기 전기납**.

So a 태아 contract is, mechanically, **two overlapping terms**: a short pre-birth term of at
most ten months (bounded to six by [S8 제61조] if birth is late), and the main term running
from birth to 30/80/90/100/110세만기.

**태아전용 보장** — covers that only a foetal contract may buy [S2]:

| Cover | 보험기간 | 납입 | 가입나이 |
|---|---|---|---|
| 저체중아출생 | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 저체중아입원일당(3-60일) | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 신생아질병입원일당(1-120일) | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 신생아질병입원일당(1-10/30/60일, 중환자실) | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 31주이내출생진단 | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 선천장해출생 | 1년만기 | 1~10개월납 / 전기납 | 태아 |
| 선천변형두상진단 | 1년만기 | 1~10개월납 / 전기납 | 태아 |

**A one-year term is the market convention for the neonatal block**, matching KIRI's
description of the 주산기 rider as 「출생 전후에 발생하는 질환에 대한 보장을 강화하려는
목적으로 출생 후 1년까지만 보장」 [R5].

**Benefit definitions actually retrieved.**

- 저체중아육아비용 및 신생아입원일당 [S1]: 「저체중아로 출생하여 인큐베이터를 사용했을
  경우 **최고 60일을 한도로 실제 사용일수에서 2일을 공제하고** 인큐베이터 사용 1일당
  보험가입금액 지급」; and 「출생 전후기 질병으로 4일이상 계속 입원하여 치료를 받은 경우
  **4일째 입원일로부터** 입원 1일당 1만원 지급(1회 입원당 120일 한도)」.
- 출생위험(Ⅱ) [S1]: 저체중아 출생 → 가입금액 × 10%; 장해 출생 → × 20%; 심한 장애 출생 →
  가입금액 100%.
- 출생위험(Ⅲ) [S1]: 저체중아(2.5kg 이하) → × 5%; 저체중아 → × 10%; 장해 출생 → × 20%;
  심한 장애 출생 → 100%. The two versions differ only in adding a lower low-birth-weight
  tier.
- 임신27주이내 조산치료비 [S1]: 「임신 27주 이내에 출생한 경우 가입금액」. [S2]'s
  equivalent is 31주이내출생진단.
- 선천이상진단비 [S1]: 「출산후 선천성기형, 변형 및 염색체 이상으로 진단시 가입금액
  지급(최초 1회한)」; 특정선천이상진단비 the same on a named subset.
- 선천이상수술비 [S1]: 「출산후 선천성 기형, 변형 및 염색체 이상으로 진단 확정 되고 수술을
  받은 경우 가입금액」; variants exclude 혀유착증 (tongue-tie) and 선천성모반, which are the
  two high-frequency, low-severity conditions in the class.
- 선천이상입원일당(1일이상) [S1]: 「보험기간 중에 190 이상으로 진단확정되고 그 치료를
  직접적인 목적으로 입원시 입원1일당 가입금액 지급(지급일수 120일 한도)」 — the KCD range
  is truncated in the extraction; read as the Q chapter.
- 신생아뇌출혈 [S1]: 「보험기간 중에 약관에서 정한 신생아뇌출혈 진단시(최초 1회한) 가입금액
  × 20%」 — this is the cover at the centre of the 2013 P52 dispute [R5].
- 주산기질환 입원비 [S8]: 「'주산기질환'이라 함은 제7차 개정 한국표준질병사인분류 중
  **출생전후기에 기원한 특정 병태** 대상 분류표에서 정한 질병을 말합니다」, paid where the
  insured is hospitalised for at least 4 consecutive days, **3일 초과 1일당**, **1회 입원당
  120일 한도**.
- The supervisor's 2008 rider table [R3] gives the same three archetypes in their original
  form: 출생전후기 질환 보장특약 (「일반적으로 임신 28주에서 생후 1주까지의 기간」),
  선천성질환 수술특약, and 미숙아(또는 저체중아) 육아비용보장특약 (「태아의 출생시 몸무게가
  2kg(또는 2.5kg) 미만으로서 인큐베이터를 **3일 이상** 사용했을 경우 1일당 약정금액」).
- **A worked claim, with amounts** [R3]. 무배당XX어린이보험, 계약자 한OO / 피보험자 태아,
  보험기간 2007-09-13 ~ 2025-12-07. Birth on 2007-12-07 at 32 weeks, 1.84 kg, congenital
  atresia and stenosis of the small intestine, enterostomy, incubator, in hospital
  2007-12-07 to 2008-05-01. Total paid **₩16,836,420 (약 1,684만원)**: 신생아육아비용
  ₩3,000,000 (2일초과 1일당 5만원 × 60일한도); 신생아입원급여금 ₩1,200,000 (3일초과 1일당
  1만원 × 120일한도); 선천이상수술위로금 ₩1,000,000; 질병입원급여금 ₩4,410,000 (1일초과
  1일당 3만원 × 147일); 질병입원의료비 ₩7,226,420 (사고일로부터 365일한도). This single
  case is the most useful severity datum in this file: the neonatal block is capped by
  **days**, not by amount, and the indemnity element (then still attachable as a rider —
  see §11) is 43% of the total.

### 7. Issue ages, terms and payment terms

**The current envelope**, from [S2] (현대해상 Hi2607, 1종 표준형; the 기본계약 is
상해후유장해):

| 보험기간 | 보험료 납입기간 | 가입나이 |
|---|---|---|
| 10세만기 | 5년납 | 태아 ~ 4세 |
| 10세만기 | 전기납 | 태아 ~ 5세 |
| 20세만기 | 10년납 / 15년납 | 태아 ~ (19−납입기간)세 |
| 20세만기 | 전기납 | 태아 ~ 15세 |
| 30세만기 | 10년납 | 태아 ~ 15세 |
| 30세만기 | 15년납 | 태아 ~ 14세 |
| 30세만기 | 20년납 | 태아 ~ 9세 |
| 30세만기 | 25년납 | 태아 ~ 4세 |
| 30세만기 | 전기납 | 태아 ~ 15세 |
| 80세 / 90세 / 100세만기 | 10 / 15 / 20 / 25 / 30년납 | 태아 ~ 15세 |

Two obligatory riders, 보험료납입면제대상 and 보험료납입지원(유사암진단Ⅱ), run 5~30년 전기납
at 태아~15세 [S2].

[S4] (KB, 자녀보험Plus) has the same shape with a longer maximum term:

| 보험기간 | 보험료 납입기간 | 가입나이 |
|---|---|---|
| 20세만기 | 10년납 | 태아, 0 ~ 10세 |
| 20세만기 | 15년납 | 태아, 0 ~ 5세 |
| 20세만기 | 20세납 | 태아, 0 ~ 15세 |
| 30세만기 | 10 / 15년납 | 태아, 0 ~ 15세 |
| 30세만기 | 20년납 | 태아, 0 ~ 10세 |
| 30세만기 | 25년납 | 태아, 0 ~ 5세 |
| 30세만기 | 30세납 | 태아, 0 ~ 15세 |
| **90세 / 100세 / 110세만기** | 10 / 15 / 20 / 25 / 30년납 | 태아, 0 ~ 15세 |

and the 일반상해사망 basic cover, uniquely, is available only at **만 15세** [S4].

**The pre-2023 envelope** [S1] (메리츠 1910). The same 만기 ladder, but the ages run to 30:
5년만기 전기납 0~20세; 10년만기 3년납/5년납/전기납 0~20세; 20년만기 10년납/전기납 0~20세;
30세만기 5년납 0~19세, 10년납 0~9세 and 11~19세, 20년납 0~9세, 25년납 0~5세; **80세만기 /
90세만기 / 100세만기, 10·20·25·30년납, 0~30세**. Some rider groups run to 0~30세 even on the
short terms. The 태아 sub-term is `1~10월만기 전기납 태아 월납` [S1].

**Renewal.** [S7] is the clearest example of the 갱신형 architecture. The whole product is
built of 20년만기 / 30년만기 renewable blocks, with 최초 가입나이 0~30세 and 갱신 age ranges
written as `(보험기간)세 ~ (100−보험기간)세`, and shorter 1~19년/21~29년 blocks renewing to
`(100−보험기간)세`. Different cover groups carry different renewal ceilings — 80, 70, 98 and
30 appear in place of 100 for 중증화상, 장기이식, 재진단암 and 다발성소아암 respectively —
and 재진단암 has a 1년만기 renewal at 97, 98, 99세 [S7]. 제29조(계약의 자동갱신) requires the
company to notify the renewal premium and ask whether the contract is to continue **15 days
before** the term ends [S7].

**Premium frequency.** 월납 and 연납 at [S7]; 월납 throughout [S1] [S2] [S11]. One product on
the board is 일시납 (카카오페이손해보험 (무)선물하는자녀보험2601, 보험기간 3년, 일시납)
[S11].

**Minimum premium.** The board publishes a 최저가입 보험료 per product: ₩20,000 at
메리츠화재, 흥국화재, 삼성화재 (one form ₩10,000), 롯데손보 and 농협손보; ₩25,000 at
현대해상 (대면); ₩15,000 at KB (CM); ₩10,000 at KB (대면) and 삼성화재 (한 form);
보장보험료 ₩5,000 at 한화손보; ₩0 or 없음 on two 삼성화재 direct forms; ₩6,882 and ₩86,492
at 카카오페이손해보험 [S11].

### 8. 보험나이 — and how a foetus has one

- The standard wording, identical in the 생명보험 and 질병·상해보험 표준약관 and reproduced
  by every carrier: 「보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월
  미만의 끝수는 버리고 6개월 이상의 끝수는 1년으로** 하여 계산하며, 이후 매년 계약해당일에
  나이가 증가하는 것으로 합니다」 [R8 제21조] [S7 제27조] [S8 제30조] [S12 제30조].
- The 표준약관's worked example: 생년월일 1988-10-02, 계약일 2014-04-13 → 25년 6월 11일 →
  **26세** [R8]. A carrier's own: 생년월일 1994-03-03, 계약일 2023-10-13 → 29년 7개월 10일
  → **30세** [S7].
- 보험나이 is used for everything except the 만15세 nullity test, where 실제 만 나이 applies
  [R8 제21조제1항 단서] [S7 제27조제1항].
- **For a foetus** the 계약나이 is fixed at **0세** at the 계약일 [S8 제60조], and the
  benefit-scale age runs from the date of birth [S8 제58조]. If the birth falls more than six
  months after the 계약일, the 계약일 is re-set to six months before the birth and the
  premium and reserve are adjusted [S8 제61조]. On the non-life chassis the same effect is
  achieved by re-rating: 「태아보장기간에 태아위험보장을 위한 보장보험료를 적용하며, 출생일
  이후의 보장보험료는 **보험나이 0세 기준**으로 변경하여 적용함. 다만, 출생통지가 이루어지지
  않은 경우에는 계약전환일(출생예정일이 포함된 다음 달의 계약해당일)에 보험료를 변경하여
  적용」 [S1].
- A model must therefore hold **two ages**: a policy age that starts at 0 on the 계약일, and
  an attained age that starts at 0 at birth, the two differing by up to ten months (and by up
  to six under [S8 제61조]).

### 9. 면책기간 (waiting periods) and 감액기간 (reduced-benefit periods)

**The rule that defines the product.** Cancer cover in Korea normally carries a 90-day
면책기간 running from the 계약일. In an 어린이보험 it does not, and the carrier says so
explicitly in the 상품요약서 footnote:

> 주1) 최초계약과 부활계약의 면책기간은 **보험나이 15세 이상인 경우에만 적용** [S3]

and, in a benefit definition on the comparison board:

> 피보험자가 보장개시일(계약일로부터 90일이 지난날의 다음날, **계약일 현재 보험나이 15세
> 미만 피보험자의 경우 1회 보험료를 받은 때**) 이후에 암(유사암제외)으로 진단확정시 …
> — DB손보, 암진단비Ⅱ(유사암 제외) [S11]

This is the 2006 change described by [R5]: 「2006년부터 어린이보험의 경우 암에 대한 위험률이
낮아 역선택 우려가 있다거나 이로 인한 위험률차손이 크다는 근거가 없기 때문에 암 보장에
대한 90일 부담보 기간이 삭제되었다.」 For a model, the practical statement is: **on a child
policy the cancer benefit is in force from the first premium, and the 90-day waiting period
switches on at 보험나이 15.**

**태아가입 removes the remaining waiting periods too.** [S3]: 「주7) 태아가입용의 경우
면책기간 없음」, applied to the 10-day waiting periods on 특정9대감염병진단비 and
독감 항바이러스제 치료비.

**감액기간.** The market has largely moved to 감액없음 — the benefit names themselves carry
the qualifier (암진단비(유사암제외)**(감액없음)**, 뇌혈관질환진단비**(감액없음)**) at
메리츠화재, 흥국화재, 삼성화재, KB손보 and 현대해상 [S1] [S11]. Where a 감액 survives it is
first-year 50%: 농협손보's 암진단비(유사암제외) is published as 「1천만원(1년이내 50%지급)」
and its 항암방사선치료비 / 항암약물치료비 as 「100만원(1년미만 50%지급)」 [S11] [S6].
메리츠화재's current matrix applies 감액 only to dental benefits — 「최초계약일부터 2년
경과시점 전일 이전 감액지급」 at 25% or 50% of 가입금액 depending on the procedure — with
cancer at 「-」 throughout [S3].

**A foetal contract is never subject to 감액.** This is the 2015–2016 supervisory action
[R2], which sets out the before-and-after wording:

| 종전 | 개선 |
|---|---|
| 제4조 ④ 피보험자에게 암보장개시일 이후 계약일부터 1년 이내에 … 보험금 지급사유가 발생한 경우 회사는 계약일부터 1년 초과시에 지급하는 보험금의 50%를 지급합니다. | 제4조 ④ (동일) **단, 피보험자가 보험가입 당시 태아(胎兒)인 경우에는 보험금의 100%를 지급합니다.** |

The reasoning given is that 「태아는 보험가입시 역선택 가능성이 거의 없는데도 성인과 동일한
기준을 적용하여」 the reduction was being applied; the trigger case was a newborn with a
cerebral haemorrhage paid at 50% [R2]. 17 carriers and 56 products were covered, the
recommendation was made 2015-06-17 and the wordings were amended between January and April
2016 [R2]. A current carrier confirms it still holds: 「암진단일이 보험계약일로부터 1년
미만인 경우 보험금이 삭감될 수 있습니다.(**태아형의 경우 삭감없이 보험금이 지급됩니다**)」
[S8].

**Other waiting periods that do apply.** 누수사고 under the 가족일상생활배상책임 rider has a
90-day 보장개시일 running from the 계약일, resetting to the renewal date on renewal [S5]
[S3]. Cancer-treatment hospital-cash and outpatient riders carry the ordinary 90-day
책임개시일 [S5].

### 10. 보험료 납입면제 — the child trigger and the parent trigger

**On the non-life chassis the waiver is on the child.** [S2] states the trigger set on the
cover page of the 상품요약서:

> 보장보험료 납입면제 — 상해 및 질병으로 50%이상후유장해 발생시 또는 7대질병으로 진단시
> 또는 중대한특정상해수술 받은 경우
> \* 7대질병 : 암(유사암 제외), 뇌혈관질환, 중대한재생불량성빈혈, 양성뇌종양,
> 심혈관질환(특정Ⅰ, I49제외), 심혈관질환(I49), 심혈관질환(특정Ⅱ)
> \* 중대한특정상해수술 : 상해로 뇌손상, 내장손상을 입고 사고일로부터 180일 이내에 받은
> 개두·개흉·개복수술

and, in the detailed section, five operative rules [S2]:

1. the waiver applies to 보장보험료 from the next instalment;
2. **출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지 않음** — a carve-out
   aimed squarely at the neonatal block, and the sharpest interaction in the product between
   the foetal covers and the waiver;
3. on the 1종 표준형, a waiver granted in one renewal cycle **does not carry into the renewed
   contract**: 「새롭게 갱신되는 계약에서는 갱신전 보험사고로 인한 보험료 납입면제를
   적용하지 않으며, 해당보험료를 계속 납입하여야 합니다」;
4. once the 보장보험료 is waived, payment of the 적립보험료 stops as well;
5. a long list of riders is **excluded** from the waiver — the whole 부양자 and 모성 block,
   and a second list (추간판장애수술, 시력교정, 시력치료, ADHD진단, 부정교합치료, 성조숙증,
   중증틱장애, 대상포진, 원형탈모증, 특정언어장애 및 말더듬증, 틱장애약물치료,
   질병악안면수술) for which the waiver applies only to events after that rider's own
   보장개시일 [S2].

[S1]'s formulation is narrower and is sold as an optional 종: 「2종(보험료 납입면제형) 가.
보장개시일 이후 「암(유사암포함)」,「뇌졸중」 또는 「급성심근경색증」으로 진단확정되거나,
일반상해50%이상후유장해 또는 질병50%이상후유장해 발생시 보장보험료를 납입면제함」, with its
own exclusion list of some 130 riders [S1]. 삼성화재 publishes the waiver as a **benefit in
its own right**, 보험료 납입면제대상 with a 가입금액 of ₩100,000 (10만원), whose 지급사유 is
the occurrence of a waiver event [S11].

**The parent's death and disability are handled by a separate rider stack.** [S2] lists a
부양자 관련 특별약관 block whose insured is the supporter, not the child:

| Rider | 보험기간 | 납입기간 | 가입나이 (the parent) |
|---|---|---|---|
| 상해사망(부양자) | 5 / 6~10 / 11~15 / 16~20 / 21~30년만기 | 1~10개월납 … 전기납 | 만15세 ~ (77−보험기간)세 |
| 상해후유장해(80%이상)(부양자) | 같음 | 같음 | 만15세 ~ (77−보험기간)세 |
| 상해후유장해(부양자) | 같음 | 같음 | 만15세 ~ (77−보험기간)세 |
| **질병사망(부양자)** | 같음 | 같음 | 만15세 ~ (77−보험기간)세 |
| 질병후유장해(80%이상)(부양자) | 같음 | 같음 | 만15세 ~ (77−보험기간)세 |
| 보험료납입지원(6대질병진단)(부양자) | 5 ~ 30년만기 | 5/10/15/20년납, 전기납 | 만15세 ~ (77−보험기간)세 |
| 암·유사암·심뇌혈관 주요치료비(부양자) | 20 / 30년만기 | 5/10/15/20년납, 전기납 | 만15세 ~ (77−보험기간)세 |
| 간병인사용 상해·질병 입원일당Ⅷ(부양자) | 20 / 30년만기 | 같음 | 만15세 ~ (77−보험기간)세 |

The Korean market's name for the economic effect is 교육자금 or 자녀양육비: 롯데손보 sells
상해사망(교육자금)(부양자), 상해80%이상후유장해(교육자금)(부양자) and
질병사망(교육자금)(부양자), 「보험증권에 기재된 피보험자의 부양자가 상해로 각각 사망 또는
80%이상의 장해상태가 되었을 때 **자녀나이에 따라 교육자금을 지급**」 [S5]; 삼성화재 sells
「엄마 상해 사망 자녀양육비(5년지급형) — 5년간 매년 2천만원」 [S11].

**On a 태아 contract the parent-death rider is compulsory.** 롯데손보: 「태아 가입 시에는
상해사망(부양자) 특별약관, 질병사망(부양자) 특별약관 **중 1개의 특별약관을 의무가입**」
[S11] [S5].

**On the 생명보험 chassis the two triggers are one clause.** [S10 제22조제1항]:

> 보험료 납입기간 중 가입자녀가 암(단, 상피내암, 기타피부암 및 경계성종양은 제외)으로
> 진단확정되거나 장해분류표 중 동일한 재해 또는 재해이외의 동일한 원인으로 여러 신체부위의
> 합산 장해지급률이 50% 이상인 장해상태가 되었거나 **계약자가 사망** 또는 장해분류표 중
> 동일한 재해 또는 재해이외의 동일한 원인으로 여러 신체부위의 합산 장해지급률이 50%
> 이상인 장해상태가 되었을 때에는 차회 이후의 보험료 납입을 면제하여 드립니다.

This is the clause the brief describes. It works because the 생명보험 wording makes the
피보험자 of the contract 「계약자와 가입자녀」 [S10 제3조] — the policyholder is himself an
insured, so his death is a contractual event and not a third party's.

A rider inherits the main contract's waiver automatically: 「이 특약의 보험료 납입기간 중
주계약의 보험료 납입이 면제되었을 때에는 이 특약의 차회 이후의 보험료 납입을 면제하여
드립니다」 [S8].

### 11. The rider stack, and the 실손 rider that is no longer there

**What the stack contains.** Grouped from [S1] [S2] [S3] [S4] [S5] [S11], with the KNIA
comparison amounts where published:

- **후유장해** — 일반상해후유장해 at 3~100%, 20~100%, 3~79%, 50%이상, 80%이상, each paid as
  가입금액 × 장해지급률 on a ₩100,000,000 (1억원) basis [R12]; 질병후유장해 3~100% on a
  ₩10,000,000 (1천만원) basis; 50%이상 and 80%이상 생활지원금 forms paying an annuity for 20
  years [S11].
- **암 진단비** — 암(유사암제외) ₩10,000,000 (1천만원) on the comparison basis [R12], with
  carriers publishing ₩10,000,000 to ₩100,000,000 (1억원) [S11]; 유사암 (기타피부암,
  갑상선암, 대장점막내암, 제자리암, 경계성종양) at ₩2,000,000–₩20,000,000; 다발성소아암,
  16대특정암, 5대고액치료비암, 전이암, 재진단암 (1년/2년 대기형) as separate riders [S1]
  [S3] [S11].
- **뇌·심혈관 진단비** — 뇌혈관질환, 뇌졸중, 뇌출혈, 허혈성심장질환, 심혈관질환(특정Ⅰ/Ⅱ)
  at ₩10,000,000–₩50,000,000 [S11]. These are the covers [R1] criticised as
  「어린이에게 발생빈도가 극히 희박한 … 성인질환 담보」.
- **수술비** — 질병수술, 상해수술, 암수술, 유사암수술, 1~5종 수술, 64대/120대 질병수술,
  질병수술Ⅱ(선천포함) variants, 뇌혈관질환수술, 허혈성심장질환수술, 5대기관질병수술 [S1]
  [S2]. The comparison basis prices 수술비 at ₩5,000,000 (500만원) per named disease [R12].
- **입원일당** — 상해 and 질병 입원일당 on 1-180일, 1-120일, 1-30일, 1-10일 and 4일이상
  bases, with 종합병원 / 상급종합병원 / 중환자실 / 1인실 variants and 암직접치료 and
  요양병원 sub-limits [S1] [S2]. The comparison basis is ₩40,000 (4만원) per day [R12].
- **골절 · 화상 · 깁스** — 골절진단비 (치아파절 제외), 5대골절, 골절수술비, 성장판손상골절,
  화상진단비, 화상수술비, 중증화상/부식진단, 깁스치료비. Published amounts are small:
  ₩100,000–₩400,000 (10만~40만원) [S1] [S11].
- **배상책임** — see below.
- **Child-specific and adolescent covers** — ADHD진단비 (6세 계약해당일 이후),
  진성성조숙증진단비 (태아~4세), 중증틱장애진단비 (태아~2세), 중증아토피진단비 (OSI 40점
  이상, 태아 only), 시력치료비, 부정교합치료비, 유치보존치료비, 소아탈장수술비,
  어린이심장시술비, 모야모야병개두수술, 수족구·중이염·폐렴·독감 진단비, 학교폭력피해치료비,
  청소년폭력상해후유장해(일상생활중), 유괴납치피해일당 [S1] [S2] [S5] [S11].
- **부양자 and 모성** — see §10 and §12.

**배상책임, in full** [S5]:

> 가족일상생활배상책임(대물20만원, 누수50만원공제)Ⅲ(갱신형) — 피보험자 및 배우자, 자녀,
> 동거중 친족(8촌 이내의 혈족(모계8촌 포함), 4촌 이내의 인척 및 배우자)이 아래에 열거한
> 사고로 타인의 신체의 장해 또는 재물의 손해에 대한 법률상의 배상책임을 부담시 1사고당
> **대인배상, 대물(누수사고)배상, 대물(누수사고제외)배상 각각 1억원 한도** 내에서 보상
> (단, 자기부담금 누수사고인 대물사고시 **50만원** 공제, 누수외사고인 대물사고시 **20만원**
> 공제)
> 1. 피보험자가 살고 있는 주택 … 의 소유, 사용 또는 관리로 인한 우연한 사고
> 2. 피보험자의 일상생활(주택 이외의 부동산의 소유, 사용 및 관리는 제외)로 인한 우연한 사고
> ※ 단, 누수사고에 대한 보장개시일은 계약일의 첫날로부터 그 날을 포함하여 90일이 지난
> 날의 다음날에 시작(갱신후 계약의 경우 갱신일 첫날에 시작)

The rider's 보험가입금액 is fixed at ₩100,000,000 (1억원) and is not selectable [S5]. It is
a **3년만기 갱신형** at 현대해상 (가입나이 태아~15세, renewing on 1~3년만기 blocks) [S2] and
a 갱신형 at 롯데손보 and 메리츠화재 [S5] [S3]. Two forms — 누수사고포함 and 누수사고제외 —
are offered and only one may be taken [S2].

**The 실손 rider is gone, and that is a regulatory fact, not a design choice.** KIRI's 2018
description of the product structure still reads 「主보험 + 태아가입특약 + 유자녀생활자금특약
+ 산모보장특약 + 각종 선택특약 + **실손특약**」 [R5], and the 2004 굿앤굿어린이CI보험
specification includes 「일상상해 실손의료비 / 질병입원 실손의료비」 [R5]. From April 2018
that is no longer possible: 실손의료보험 must be sold as a standalone product consisting only
of indemnity-medical cover, under 보험업감독규정 제7-63조제2항제1호 as amended 2017-03-22,
with a one-year transition [R9] [R10].

What survives inside an 어린이보험 is **not** a 실손의료보험. [S2] carries a single
indemnity-shaped rider, 임신·출산질환실손입원의료비(통상분만일수제외), which is written on
the **mother** for pregnancy and childbirth disease and expressly excludes the ordinary
delivery stay [S2]. No child-side 실손 rider appears in any of the five current 상품요약서
retrieved [S2] [S3] [S4] [S5] [S6]. The general proportional-contribution clause survives in
older wordings — 「보험계약에서 보장하는 의료비는 동비용을 보장하는 다수의 보험계약이
체결되어 있는 경우, 약관에 따라 비례하여 보상합니다」 [S1] — which is a reminder that the
2019 generation still carried indemnity elements.

**Consequence for the library.** A Korean family buys the indemnity layer as `Medical_KR_S`
(실손의료보험) and the fixed-benefit layer as `Child_KR_S` (어린이보험), as two contracts.
The reference `Child_KR_S` therefore models **fixed benefits only**, and the split is a
statutory one.

### 12. The mother — 임신·출산질환 riders

These sit alongside the 부양자 riders, are written on the mother, and are terminated at or
shortly after delivery. [S2] tabulates them with their terms and the mother's issue ages:

| Rider | 보험기간 | 가입나이 (the mother) |
|---|---|---|
| 모성사망 | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 임신·출산질환입원일당(1-120일) | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 임신·출산관련 고혈압·당뇨병 입원일당(1-120일) | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 임신·출산질환수술 | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 분만전후출혈·수혈진단 | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 고위험임산부집중치료실입원치료급여금(최초1회한) | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 유산진단 / 유산수술 / 유산입원일당(1-120일) | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| 임신중독증진단Ⅱ, 태반조기분리진단, 특정고위험산모질환진단, 특정임신중당뇨병진단 | 계약일 ~ 분만일 | 20세 ~ 47세 |
| 여성산과자궁적출수술, 응급실내원진료비Ⅲ(응급) | 계약일 ~ 분만 후 42일 | 20세 ~ 47세 |
| **출산전특정태아이상진단** | 계약일 ~ 분만일 | 20세 ~ 39세 |
| 선별검사이상소견후융모막및양수검사지원비(최초1회한) | 계약일 ~ 분만일 | 20세 ~ 40세, 단 임신 12주 이내 |
| 다운증후군출산 | — | 20세 ~ 45세 |
| 치핵수술(임신 및 산후기 포함) | 계약일 ~ 1년 | 20세 ~ 45세 |
| 양수색전증진단 | 계약일 ~ 분만일 | 20세 ~ 47세 |

Note **출산전특정태아이상진단** — a benefit paid on antenatal diagnosis of a foetal
abnormality, written on the mother precisely because the foetus cannot be an insured. It is
the only cover in the whole product that pays before birth, and it pays the mother.

롯데손보 offers the same block plus 산후우울증치료비(부양자), all restricted to 「임신한
여성에 한하여 가입 가능」 [S5]. 삼성화재 markets a whole product on this basis
(무배당 삼성화재 다이렉트 임산부ㆍ아기보험(2601.5)) at 0세, 30세만기 20년납, published
premium ₩5,170 male / ₩5,100 female [S11].

The 제왕절개 boundary is worth stating because it is the commonest misunderstanding [R3]:
「태아보험은 앞으로 출생할 자녀에 대한 보험이지, 제왕절개를 한 산모에 대한 보험이 아니기
때문에 제왕절개수술은 보장받지 못함.」

### 13. 무해지환급형 — the forms, the discount and the cliff

**The forms on sale.** Every carrier on the comparison board offers at least one
해약환급금 미지급형 beside the 표준형 [S11]. The naming and the post-completion fraction
differ:

| Carrier | 표준형 | Suppressed forms |
|---|---|---|
| 메리츠화재 [S3] | 1형 | 3형 해약환급금미지급형(납입후 50%) |
| 메리츠화재 (2019) [S1] | 1형 표준형; 2형 계약전환형 | 3형 미지급형 (납입후 = 표준형 100%); 4형 미지급형Ⅱ (납입후 50%); 5형 미지급형Ⅲ (납입후 5~50%, graded) |
| 한화손보 [S11] | 1종 기본형 | 2종 납입후 50% 해약환급금지급형 |
| 롯데손보 [S11] | 6종 일반형 | 9종 해약환급금 미지급형Ⅱ (납입후 50%) |
| 흥국화재 [S11] | 1종 해약환급금지급형 | 2종 납입후 50%; 3종 납입후 표준형환급률 동일지급형 |
| 삼성화재 [S11] | 1종 일반형 / 납입면제형 | 2·3종 납입면제·해약환급금 미지급형Ⅱ |
| 현대해상 [S2] | 1종 표준형 | 2종 해약환급금 미지급형 (납입후 50%); 3종 보험기간 연장형 |
| KB손보 [S11] | 1종 1형 환급형 / 1종 2형 기본형 | 2종 표준형 해약환급금의 50% |
| 농협손보 [S11] | 2종 표준형 | 1종 미지급형Ⅱ (납입중 0%, 납입후 50%) |

**The graded form, verbatim** [S1] — 5형(해지환급금미지급형Ⅲ), where M is the payment term
in years:

| 경과기간 | 1형(표준형) 대비 해지환급금 비율 |
|---|---|
| M년 종료일의 다음날 ~ M+2년 계약해당일 전일 | 5% |
| M+2 ~ M+4 | 10% |
| M+4 ~ M+6 | 15% |
| M+6 ~ M+8 | 20% |
| M+8 ~ M+10 | 25% |
| M+10 ~ M+12 | 30% |
| M+12 ~ M+14 | 35% |
| M+14 ~ M+16 | 40% |
| M+16 ~ M+18 | 45% |
| M+18 ~ 보험기간 종료일 | 50% |

**The comparison base is a synthetic product.** [S1]: 「해지환급금을 계산할 때 기준이 되는
2종(표준형)의 해지환급금은 "보험료 및 책임준비금 산출방법서"에서 정한 방법에 따라 산출된
금액으로 **해지율을 적용하지 않고** 계산함」; [S3] names it 「해약환급금미지급형 비교상품」
and says 「3형과 동일한 보장내용으로 해지율을 적용하지 않은 상품이며, 비교안내를 위한
종목으로 **실제로 판매하지 않음**」. So the 50% is 50% of a hypothetical cash value computed
without the lapse assumption, not 50% of a product anyone can buy.

**The pricing lapse assumption is disclosed.** [S1] publishes the 적용해지율 used for each
suppressed form:

| 형 | 기간 | 적용해지율 |
|---|---|---|
| 3형 (미지급형) | 납입기간 중, 10년 이하 | 연 5.0% |
| 3형 | 납입기간 중, 10년 초과 15년 이하 | 연 3.0% |
| 3형 | 납입기간 중, 15년 초과 | 연 1.0% |
| 4형 (미지급형Ⅱ) | 납입기간 중 | 5.0% / 3.0% / 1.0% as above |
| 4형 | 보험료 납입기간 이후 | 연 0.5% |
| 5형 (미지급형Ⅲ) | 납입기간 중 | 5.0% / 3.0% / 1.0% as above |
| 5형 | 보험료 납입기간 이후 | 연 0.65% |

and states that 「1형(표준형) 및 2형(계약전환형)에는 적용해지율이 적용되지 않습니다」 [S1].
That is a published, product-specific decrement basis and it is directly usable.

**Set beside the 2024 supervisory guideline** [R11]: a log-linear model converging to **0.1%**
at 납입완료 and an ultimate post-completion lapse of **0.8%** (or 20% of the 표준형 rate).
[S1]'s 2019 basis — a step function at 5%/3%/1% during payment and 0.5%–0.65% afterwards —
is of the shape the guideline replaced, and the guideline's direction of travel is to a lower
in-payment rate. The 2019 disclosure is therefore historic evidence of the practice the
supervisor moved against, and any [std] lapse basis in the reference product should say which
of the two it follows.

**Scale of the phenomenon** [R11]: 무·저해지 products were 11.4% of 보장성 초회보험료 in
2018, 30.4% in 2021, 47.0% in 2023 and 63.8% in the first half of 2024. 어린이보험 is not
broken out, but every carrier on the board sells the form [S11].

**The cash-value cliff, published.** [S2], 현대해상 Hi2607, 가입기준 남자 5세, 상해1급,
100세만기 20년납, 기본계약 상해후유장해 ₩150,000,000 (15,000만원), 의무부가
보험료납입면제대상 ₩100,000 (10만원), 선택계약 상해입원일당(1-180일) ₩20,000,
질병입원일당Ⅱ(1-180일) ₩20,000, 암진단Ⅱ(유사암제외) ₩20,000,000 (2,000만원),
유사암진단Ⅱ ₩1,000,000, 뇌혈관질환 ₩10,000,000, 허혈심장질환진단 ₩10,000,000:

| 경과 | 1종 표준형 (월납 ₩50,000) | | 2종 미지급형 (월납 ₩37,420) | |
|---|---|---|---|---|
| | 납입보험료 | 환급금 (환급률, 공시이율) | 납입보험료 | 환급금 (환급률) |
| 1년 | 600,000 | 0 (0.0%) | 449,040 | 0 (0.0%) |
| 3년 | 1,800,000 | 820,910 (45.6%) | 1,347,120 | 60 (0.0%) |
| 5년 | 3,000,000 | 1,876,960 (62.5%) | 2,245,200 | 280 (0.0%) |
| 10년 | 6,000,000 | 4,422,580 (73.7%) | 4,490,400 | 550 (0.0%) |
| 15년 | 9,000,000 | 7,050,220 (78.3%) | 6,735,600 | 420 (0.0%) |
| 20년 | 12,000,000 | 9,923,370 (82.6%) | 8,980,800 | 0 (0.0%) |
| 30년 | 12,000,000 | 12,149,980 (101.2%) | 8,980,800 | **5,752,590 (64.0%)** |
| 40년 | 12,000,000 | 14,709,200 (122.5%) | 8,980,800 | 6,973,000 (77.6%) |
| 50년 | 12,000,000 | 17,298,680 (144.1%) | 8,980,800 | 8,197,680 (91.2%) |
| 60년 | 12,000,000 | 19,072,270 (158.9%) | 8,980,800 | 9,001,530 (100.2%) |
| 95년 | 12,000,000 | 1,928,830 (16.0%) | 8,980,800 | **0 (0.0%)** |

Three features a model must reproduce. (i) The suppressed form's value is **nil through the
whole payment period** and jumps to 64.0% of premiums paid ten years after completion — a
cliff, not a curve. (ii) The 표준형's value **exceeds premiums paid** from about year 30,
because the 적립부분 accumulates at the 공시이율 while the 보장부분 reserve is still
building. (iii) **Both forms collapse to (almost) nothing at maturity** — there is no
만기환급금 on the protection part, and at 95 years the 표준형 retains only the residual
적립부분. Interest basis for the table: 공시이율 1.7% (2026-07), 평균공시이율 2.5% capped at
the selling-date 공시이율, 최저보증이율 0.3%, and for the 2종 a flat 보장부분 적용이율 2.7%
「적립한 금액으로 변동 없음」 because the 2종 is 순수보장성 with no 적립보험료 [S2].

The 3종(보험기간연장형), 30세만기 20년납, 월납 ₩30,000, shows a different and instructive
shape — 환급률 rises to 76.0% at 20년 and then **falls** to 76.5%/61.8% (공시/최저보증) at
25년, because the 적립부분 is being consumed by the cover extension [S2].

[S1]'s 2019 grid on a comparable specification (남자 5세, 상해1급, 100세만기 20년납, 월납
₩65,430 표준형 / ₩50,860 미지급형) shows 표준형 환급률 3.0% at 1년, 51.1% at 3년, 66.3% at
5년, 76.6% at 10년, 86.8% at 20년, 125.8% at 40년, 155.7% at 60년 and 0.0% at 만기; and for
3형 미지급형 0.0% throughout the payment period, 111.7% at 20년, 161.8% at 40년, 200.3% at
60년 and 0.0% at 만기 [S1]. That the 미지급형's 환급률 exceeds the 표준형's after completion
is arithmetic, not generosity: the denominator is a smaller premium.

**Surrender-value basis.** 「회사는 금융감독원장이 인가한 산출기준에 따라 계산한 이 보험의
**순보험료식 계약자적립액에서 해약공제액을 공제한 금액**을 해약환급금으로 지급하여 드립니다」
[S2]; [S1] words it as 「순보험료식 책임준비금에서 해지공제액을 공제한 금액」.

### 14. Premiums — the published rate cards

All premiums below are from [S11] and are quoted on the standardised comparison basis [R12] —
**보험나이 5세, 상해1급, 100세만기 20년납, 월납, 보장보험료 of the compulsory covers only**,
unless the product's own note says otherwise. They are as at the board's 2026 refresh.

| Carrier | Product | Form | 남자 | 여자 |
|---|---|---|---|---|
| 메리츠화재 | 내Mom같은 어린이보험2607(1종) | 1형 표준 | ₩31,708 | ₩36,289 |
| 메리츠화재 | 내Mom같은 어린이보험2607(1종) | 3형 무해지 | ₩22,313 | ₩25,831 |
| 메리츠화재 | 내Mom같은 어린이보험2607(3종) | 1형 표준 | ₩31,908 | ₩36,381 |
| 메리츠화재 | 내Mom같은 어린이보험2607(3종) | 3형 무해지 | ₩22,383 | ₩25,902 |
| 한화손보 | 건강쑥쑥 어린이보험 (무)2608 | 1종 기본 | ₩28,700 | ₩27,290 |
| 한화손보 | 건강쑥쑥 어린이보험 (무)2608 | 2종 납입후50% | ₩20,830 | ₩20,190 |
| 롯데손보 | let:play 자녀보험(도담도담)(2604) | 6종 일반 | ₩21,502 | ₩19,615 |
| 롯데손보 | let:play 자녀보험(도담도담)(2604) | 9종 미지급Ⅱ | ₩17,138 | ₩16,064 |
| 흥국화재 | 흥Good 뉴키즈 자녀보험(26.05) | 1종 환급 | ₩68,900 | ₩58,860 |
| 흥국화재 | 흥Good 뉴키즈 자녀보험(26.05) | 2종 납입후50% | ₩50,030 | ₩42,130 |
| 흥국화재 | 흥Good 뉴키즈 자녀보험(26.05) | 3종 | ₩56,670 | ₩48,760 |
| 삼성화재 | 자녀보험 NEW 마이 슈퍼스타(2601.6) | 1종 일반 | ₩148,250 | ₩120,650 |
| 삼성화재 | 자녀보험 NEW 마이 슈퍼스타(2601.6) | 2종 납입면제 | ₩153,528 | ₩125,359 |
| 삼성화재 | 자녀보험 NEW 마이 슈퍼스타(2601.6) | 3종 미지급Ⅱ | ₩115,679 | ₩95,785 |
| 삼성화재 | 건강보험 마이스타0515(2608.9) | 납입면제형 | ₩148,299 | ₩120,421 |
| 삼성화재 | 건강보험 마이스타0515(2608.9) | 미지급Ⅱ | ₩114,970 | ₩95,148 |
| 현대해상 | 굿앤굿어린이종합보험Q(Hi2607) | 1종 | ₩26,841 | ₩21,019 |
| 현대해상 | 굿앤굿어린이종합보험Q(Hi2607) | 2종 | ₩21,171 | ₩16,798 |
| KB손보 | 금쪽같은 자녀보험Plus(26.07) 110세만기 | 1종1형 환급 | ₩24,524 | ₩18,442 |
| KB손보 | 금쪽같은 자녀보험Plus(26.07) 110세만기 | 1종2형 기본 | ₩23,488 | ₩17,748 |
| KB손보 | 금쪽같은 자녀보험Plus(26.07) 110세만기 | 2종 50% | ₩17,974 | ₩13,824 |
| KB손보 | 다이렉트 자녀보험(26.07) 1종 | — | ₩30,440 | ₩29,610 |
| DB손보 | 다이렉트자녀보험2607(CM) | — | ₩27,480 | ₩24,600 |
| DB손보 | 아이(I)러브(LOVE)플러스건강보험2607 | 2종 | ₩67,130 | ₩64,640 |
| DB손보 | 아이(I)러브(LOVE)플러스건강보험2607 | 8종 | ₩67,990 | ₩65,570 |
| DB손보 | 아이(I)러브(LOVE)플러스건강보험2607 | 9종 무해지 | ₩51,970 | ₩50,430 |
| 농협손보 | NH아이맘헤아림어린이보험2604 | 2종 표준 | ₩26,999 | ₩16,730 |
| 농협손보 | NH아이맘헤아림어린이보험2604 | 1종 미지급Ⅱ | ₩18,202 | ₩11,407 |

Shorter-term products on the same board, quoted on their own bases [S11]: 현대해상
다이렉트 굿앤굿어린이종합보험Q(Hi2601), 5세, **30세만기 20년납** — ₩2,562 / ₩2,354;
현대해상 굿앤굿어린이종합보험Q(Hi2607) 3종, 30세만기 20년납 — ₩3,722 / ₩3,026; 삼성화재
자녀보험 꿈나무(2601.7), **0세, 18년만기 18년납** — ₩5,200 / ₩5,910; 삼성화재 다이렉트
어린이보험(2601.19) 자동갱신형, 5세, 30년만기 30년납 — ₩4,700 / ₩4,960; 롯데손보
베이비보험(2604), 5세, **15세만기 전기납(10년납)** — ₩1,033 / ₩722; 롯데손보
청소년보험(2604) 2종, **7세, 20세만기 전기납(13년납)** — ₩6,012 / ₩6,122; KB
신생아지원프로젝트자녀보험(26.01), 5세, 10년만기 전기납 — ₩850 / ₩950; 카카오페이
영유아보험2601, 남자 5세, **7년만기 든든형** — ₩13,079 / ₩12,337.

**What the table shows.**

- **The 무해지 discount is 25%–33% of the 표준형 premium.** Ratios: 메리츠 70.4% (M) /
  71.2% (F); 한화 72.6% / 74.0%; 롯데 79.7% / 81.9%; 흥국 72.6% / 71.6%; 삼성화재
  (마이 슈퍼스타 3종 vs 1종) 78.0% / 79.4%; 현대해상 78.9% / 79.9%; KB (2종 vs 1종2형)
  76.5% / 77.9%; DB (9종 vs 8종) 76.4% / 76.9%; 농협 67.4% / 68.2%. The observed range is
  **67%–82% of the 표준형 premium**, i.e. a 18%–33% discount.
- **The sex relativity has no fixed sign.** 메리츠, 한화 (partly), 삼성화재 (자녀보험
  꿈나무), KB 신생아지원 and 삼성화재 다이렉트 어린이보험 price the **female higher**; 롯데,
  흥국, 삼성화재 (마이 슈퍼스타), 현대해상, KB, DB and 농협 price the **male higher**. The
  spread is wide — 농협's female premium is 62% of its male, 메리츠's is 114%. This is a
  benefit-mix effect, not a pure morbidity effect: the products differ in whether the
  compulsory set is dominated by accident (male-heavy) or by cancer and thyroid (female-heavy)
  benefits. **A [std] morbidity basis for the reference product must state which of the two
  it reproduces and why.**
- **The absolute level varies by a factor of seven** on a nominally standardised basis —
  롯데 ₩21,502 against 삼성화재 ₩148,250 for a male 5-year-old — because carriers include
  different compulsory rider sets in the quoted 보장보험료. The 보험가격지수 below is the
  normalising statistic, not the premium.

**보험가격지수** (the ratio of total premium to the sum of the 참조순보험료 total and the
average expense total, in per cent) [S11], male / female: 메리츠 80.4 / 112.6 (1형), 89.0 /
121.2 (3형); 한화 101.3 / 113.4, 110.8 / 123.3; 롯데 79.6 / 72.4, 95.5 / 83.4; 흥국 83.5 /
89.2, 93.2 / 97.0, 94.7 / 101.4; 삼성화재 88.1 / 90.8 (1종), 88.5 / 91.1 (2종), 102.0 /
103.8 (3종), 87.6 / 90.3 and 104.1 / 106.1 (마이스타); 현대해상 98.2 / 101.1 (1종), 116.0 /
119.0 (2종), 113.5 / 118.6 (3종); KB 89.5 / 86.9, 88.6 / 86.2, 104.9 / 102.7, 103.4 / 106.1
(다이렉트); DB 81.6 / 98.5 (2종), 81.8 / 98.3 (8종), 96.0 / 115.3 (9종), 101.4 / 117.6
(다이렉트); 농협 96.4 / 83.2 (2종), 89.5 / 78.3 (1종). Note that the **무해지 form's price
index is consistently higher than the 표준형's** — 3 to 16 points — at every carrier. The
index divides by a reference net premium computed on the 평균공시이율 and the
참조순보험요율 without the suppressed-lapse credit, so the suppression shows up as an
apparent loading. [S1]'s 2019 disclosure shows the same pattern at a higher level: 표준형
156.7 / 134.7, 미지급형 162.0 / 149.7, 미지급형Ⅱ 162.7 / 154.7, 미지급형Ⅲ 166.6 / 150.2.

**Discounts published on the board** [S11]: 형제자매 3명 이상 → 영업보험료 3% (메리츠);
2명 → 1%, 3명 이상 → 3% (현대해상); 출산할인 — 피보험자(자녀·태아)의 형제·자매가 출산된
경우 보험료의 2% (KB, DB); 국가유공자 3%, 당사 장기보험 기가입자 1%, 다자녀 (롯데);
아침밥먹기동참할인 (농협).

**A published premium-by-issue-age index** [R5], on a simulation of 암진단 ₩40,000,000
(4천만원), 20년 납입, 100세 만기:

| 가입연령 | 0세 | 20세 | 30세 | 60세 |
|---|---|---|---|---|
| 잔여보장기간 | 100년 | 80년 | 70년 | 40년 |
| 0세 가입 대비 총 납입보험료 | 100% | 189% | 264% | 625% |

KIRI's own caveat is that the comparison ignores interest to the later entry date. It is
nonetheless the marketing logic of the 100세만기 child policy stated arithmetically, and it
is a usable sanity check on a level-premium model.

### 15. Interest bases

From [S11], per product, 보장부분 적용이율 (the pricing rate) and 적립부분 적용이율
(the declared crediting rate, with 최저보증이율 in brackets):

| Carrier | 보장부분 적용이율 | 적립부분 (최저보증) |
|---|---|---|
| 메리츠화재 | 2.65% | 2.20% (0.3%) |
| 한화손보 | 2.75% | 1.60% (0.3%) |
| 롯데손보 | 3.00% | 1.60% (0.3%) |
| 흥국화재 | 3.00% | 1.60% (0.3%) |
| 삼성화재 | 2.75% | 1.90% (0.25%) |
| 현대해상 | 2.70% | 1.70% (0.3%) |
| KB손보 | 2.75% / 2.50% | 1.65% (0.2%) |
| DB손보 | 2.75% / 2.50% | 1.75% (0.2%) |
| 카카오페이손해보험 | 2.75% | — (순수보장성) |
| 농협손보 | 3.00% | 1.75% (0.5%) |

The suppressed forms show 「-」 for the 적립부분 because they are 순수보장성 with no
적립보험료 [S11] [S2].

**Observed range: 보장부분 2.50%–3.00%; 공시이율 1.60%–2.20%; 최저보증이율 0.20%–0.50%.**

[S2] names its crediting rate 「보장성 공시이율Ⅴ」 and puts it at **1.7% as at 2026-07**,
with 평균공시이율 **2.5%** under 보험업감독규정 제1-2조제18호, itself capped at the
selling-date 공시이율 [S2]. [S1] (2019-10) gives 보장부분 2.5%, 공시이율 2.0% and
최저보증이율 0.3%, with the 공시기준이율 formula printed in full:

> 공시기준이율(%) = 외부지표금리수익률 × α + 운용자산이익률 × (1−α), α = (A/B + C) / (A + C)
> A : 직전년도초 보험료적립금; B : 자산의 직전년도말 듀레이션; C : 직전년도 수입보험료

(the α expression is reproduced as extracted and its bracketing is uncertain — see gaps).

### 16. The market

**Size, current.** 어린이보험 annual premium is **₩9.4조원**; all 보장성 인보험 annual
premium is about **₩42.7조원**; 보험계약대출 balance is ₩70.5조원 — all as stated by the
금융위원회 at 2026-03-31 [R6]. So 어린이보험 is roughly **22% of all Korean protection
personal-lines premium**. That is the market-share figure this file exists to establish, and
it comes from a primary supervisory document.

**Size and split, historic** [R3], 참고자료2, in 억원 and contracts:

| | 신계약건수 ('07, 태아가입건수) | 수입보험료 FY05 | FY06 | FY07 |
|---|---|---|---|---|
| 생명보험 | 583,888 (138,965) | 23,947 | 24,888 | 23,995 |
| 손해보험 | 1,038,751 (196,170) | 3,936 | 5,888 | 8,406 |
| 합계 | 1,622,639 (335,135) | 27,883 | 30,776 | 32,401 |

and the note 「어린이보험의 수입보험료 중 약 20% 정도가 태아일 때 가입한 어린이보험의
수입보험료로 추정(FY07 기준 약 6,500억원)」 [R3]. Three readings. (i) In FY07 the market was
₩3.24조원 and **74% of it was 생명보험** — the reverse of today. (ii) The 손해보험 side
**doubled in two years** (₩3,936억 → ₩8,406억) while the 생명보험 side was flat; this is the
굿앤굿어린이CI보험 effect [R5]. (iii) **About one contract in five was written in utero**
(335,135 of 1,622,639 = 20.7%), and the same fraction of premium.

**In-force, 2013–2015** [R2], sourced by the FSS to 보험개발원, in 만건 and 억원:

| | 2013.4–12 (9 months) | 2014 | 2015 (잠정) |
|---|---|---|---|
| 보유계약건수 (만건) | 1,141 | 1,182 | 1,162 |
| 수입보험료 (억원) | 33,385 | 45,611 | 44,906 |

and 신계약건수 88만건 (2013.4–12) → 127만건 (2014) → 123만건 (2015 잠정), against 출생자수
(통계청) of 43.7만명 (2013), 43.5만명 (2014), 43.9만명 (2015) [R2]. New child contracts
therefore ran at roughly **three times the birth count**, which is what a multi-rider,
multi-contract product looks like in a count statistic — and a warning that "contracts" in
Korean insurance statistics are not "insured children".

**Growth against a falling birth rate.** [R5] observed in 2018 that 「출산율 저하에 따라
15세 미만 인구 수가 지속적으로 줄어들어 어린이보험의 시장규모가 앞으로 크게 성장할
가능성은 낮다」 and was wrong: the FY07 ₩3.24조원 [R3] and the 2015 ₩4.49조원 [R2] became
₩9.4조원 by 2026 [R6]. The mechanism [R5] itself identified is the term extension — a
100세만기 policy written at age 0 collects premiums for twenty years and stays in force for a
hundred, so the in-force premium grows even as the cohort shrinks. Claims that 어린이보험
premium rose from ₩3.29조원 (2019) to ₩5.32조원 (2023), and that 2024 new business rose 40.7%
year on year, appear in trade press summaries and are **[unverified]** — no primary source for
them was retrieved.

**Loss ratio.** [R5], writing in 2018: 「어린이보험의 손해율은 보험회사 평균 손해율(약 80%
수준) 미만인 것으로 알려져 있어 우려할 만한 수준은 아니지만, 이러한 담보경쟁은 향후
어린이보험의 손해율이 높아질 가능성이 매우 높다」, with the two documented deteriorations
being the 2010 outpatient riders and the 2013 P-code decision. No current loss-ratio figure
for 어린이보험 was retrieved — see gaps.

### 17. The 2026 premium discount

From 2026-04-01 every Korean insurer operates a 「저출산 극복 지원 3종 세트」 [R6]:

1. **어린이보험 보험료 할인** — 1%–5% for one year, the rate and period set by each insurer,
   on 보장성 어린이보험. Eligibility: the policyholder or spouse is within one year of a
   birth, or on 육아휴직, or on 육아기 근로시간 단축 (for a child of 12 or under, or in
   primary year 6, under 남녀고용평등법 §19조의2). On the birth limb, the discount applies to
   the **sibling's** policy, not the newborn's own: 「(출산) 형제, 자매 출산 시 보험료 할인
   가능(피보험자 출산사유 할인은 제외)」 [R6].
2. **보험료 납입유예** — 6 or 12 months, interest-free, on all 보장성 인보험 — but
   **어린이보험 is expressly excluded** from this limb, along with 해약환급금-short contracts,
   금리연동형 and 변액 [R6].
3. **보험계약대출 이자상환유예** — up to a year, interest-free.

Limited to one use per contract; the three may be combined; pre-existing contracts qualify.
Expected total consumer benefit about **₩1,200억원 a year** [R6]. The scheme was announced at
a 금융위원장 CEO round table on 2025-10-16 and forms part of a five-year ₩2조원
「포용금융 추진계획」 announced 2026-03-16 [R6].

This matters to a model in two ways: it is a **1%–5% premium haircut with a one-year duration
on a subset of the in-force book**, and it is evidence that the supervisor treats 어린이보험
as a distinct, identifiable product class with its own premium aggregate.

### 18. Statutory constraints that shape the product

- **상법 제732조** — 「15세미만자, 심신상실자 또는 심신박약자의 사망을 보험사고로 한
  보험계약은 무효로 한다」 [R7]. The 표준약관 restates it at 제19조제2호 and adds, at
  제19조제3호, that the saving for an age misstatement discovered after the insured has
  reached the contractual age 「제2호의 만 15세 미만자에 관한 예외가 인정되는 것은
  아닙니다」 [R8].
- **The product-design consequences are visible everywhere.** 일반상해사망 is fixed on only
  「기본계약 최초가입시 피보험자의 나이가 15세 이상인 경우」 [S1]; KB writes its
  일반상해사망 basic cover only at 만 15세 [S4]; 메리츠's board note reads 「15세이상 가입시
  일반상해사망 특약 고정부가」 [S11]; the 생명보험 wording pays a 사망보험금 only where the
  child dies 「만 15세 계약해당일 이후」 [S10 제21조]; and the 1997 삼성생명 꿈나무사랑보험
  paid a 사망위로금 that was 「15세 전 사망 시에는 납입보험료 환급」 [R5]. [R3] states the
  general rule: 「15세 미만의 미성년자를 피보험자로 하는 보험상품에서도 피보험자의 사망시
  사망보험금이 아니라 기납입보험료가 지급됨」.
- **상법 제739조** — 「상해보험에 관하여는 제732조를 제외하고 생명보험에 관한 규정을
  준용한다」 [R7]. Read literally this disapplies the under-15 prohibition to 상해보험, and
  the market's practice of writing 상해사망 only from 15 is therefore more conservative than
  the statute strictly requires. That reading is **[unverified]** as a matter of Korean law —
  no judgment or commentary on the point was retrieved — and no fact in this file depends on
  it; what is verified is the uniform market practice.
- **보험업감독규정 제7-63조제2항제1호** — 실손의료보험 must be a standalone product [R10]
  [R9]; see §11.
- **A 손해보험 design rule on 질병사망 riders**, from a carrier's own summary of its
  사업방법서 [S5]: 「질병을 원인으로 하는 사망을 특약으로 보장하고자 하는 경우에는 …
  (1) 보험기간은 80세만기 이내로 함 (2) 질병사망보험금의 한도는 개인당 2억원 이내로 함
  (3) 만기시에 지급하는 환급금은 납입 보험료 합계액의 범위 이내로 함.」 This is why the
  질병사망(부양자) rider on a non-life child policy stops at 80 while the child's own cover
  runs to 100 or 110.
- **계약의 소멸** — 「피보험자가 사망한 경우, 이 계약은 그 때부터 효력이 없습니다」
  [S7 제28조]; on the life chassis, 「가입자녀가 사망하였을 때에는 이 계약은 그 때로부터
  효력을 가지지 아니합니다」 [S10].

### 19. Contract mechanics inherited from the 표준약관

Recorded once, because `Child_KR_S` states deltas against `Cancer_KR_S` and these are the
same at both.

- **청약철회** — 15 days from receipt of the policy, and not more than 30 days from
  application; excluded for 진단계약, contracts of under a year and professional
  policyholders [S8].
- **계약의 취소** — 3 months from conclusion where the 약관 was not delivered, the important
  terms were not explained, or the 청약서 was not signed [S8].
- **납입최고(독촉)기간** — at least 14 days (7 days for a term under a year); one carrier
  operates it as 「납입기일 다음날부터 납입기일이 속하는 달의 다음달 마지막 날까지」, so a
  premium due on the 15th of September is in grace to 31 October and the contract lapses on
  1 November [S8].
- **부활(효력회복)** — within **3 years** of lapse, where no surrender value has been taken,
  subject to fresh underwriting [S8]. Waiting periods re-run from the 부활 date [S3].
- **자살면책** — 2 years [S8].
- **보험나이** — §8.
- **지정대리청구서비스특약** is standard [S8]; [S5] sets out the 대리청구인 eligibility
  (the insured's spouse on the family register, or a relative within the third degree, with
  an unnamed designation defaulting to a direct ascendant or descendant) and the requirement
  to offer it wherever 계약자 = 피보험자 = 보험수익자.
- **예금자보호** — up to ₩50,000,000 (5천만원) per person per insurer, counting surrender
  values and other payables [S8].

---

## Variation across carriers

| Feature | 메리츠화재 [S1] [S3] | 현대해상 [S2] [S7] | KB손보 [S4] | 롯데손보 [S5] | 농협손보 [S6] | 생명보험 [S8] [S9] [S10] |
|---|---|---|---|---|---|---|
| Maximum 만기 | 100세 | 100세 | **110세** | 100세 | 100세 | 100세 [S16 unverified] |
| 가입나이, current | 태아~15세 (2607) | **태아~15세** | 태아, 0~15세 | 태아~15세 | 태아~15세 | 0~15/20세 [unverified] |
| 가입나이, pre-2023 | **0~30세** (1910) | **0~30세** (Hi2204) | — | — | — | — |
| 태아가입 | yes | yes | yes (예약가입) | yes | yes | yes, via 태아가입특칙 |
| 태아 sub-term | 1~10월만기 전기납 | 태아보장기간 (계약일~출생일) | 1년만기 전기납 | — | — | 특칙, no separate term |
| 태아 rider window | not stated | not stated | not stated | **임신 22주 이내** (15주 for one) | not stated | not stated |
| Suppressed forms | 3형 (납입후 100%), 4형 (50%), **5형 (5~50% graded)** | 2종 (납입후 50%) | 2종 (50%) | 9종 (50%) | 1종 (50%) | not examined |
| 적용해지율 disclosed | **yes** (5/3/1%, 0.5%, 0.65%) | no | no | no | no | no |
| Waiver trigger (child) | 암(유사암포함)·뇌졸중·급성심근경색 진단 or 50% 후유장해 (2종 only) | 50% 후유장해 or **7대질병** or 중대한특정상해수술 | 자녀 납입면제 (obligatory rider) | obligatory rider | 납입면제대상 특별약관 | 암 or 50% 후유장해 |
| Waiver on the parent | 부양자 riders | 부양자 riders incl. 보험료납입지원(6대질병) | 부양자 riders | 부양자 riders, **obligatory on 태아** | not examined | **계약자 사망 or 50% 후유장해, in the main clause** |
| P-code waiver carve-out | not stated | **yes** — 출생전후기 병태 excluded | not stated | not stated | not stated | not stated |
| Waiver survives renewal | not stated | **no** on 1종 | not stated | not stated | not stated | n/a (비갱신) |
| 암 면책기간 | 90일, **15세 이상만** | not located in extract | not located | 90일 책임개시일 on cancer riders | not located | not located |
| 태아 면책기간 | **none** | — | — | — | — | — |
| 암 감액 | none (감액없음) | none | none | none | **1년 이내 50%** | 1년 미만 삭감, **태아형 제외** |
| 배상책임 | 갱신형 가족일상생활배상책임 Ⅲ/Ⅳ | 일상생활중배상책임Ⅳ(가족), 3년만기 갱신, 누수 포함/제외 | not examined | **1억원 fixed**, 대인/대물(누수)/대물(비누수) each, 자기부담 50만/20만원 | not examined | none (life licence) |
| 실손 rider | none (2607) | mother-side only | none | none | none | none |
| 보장부분 적용이율 | 2.65% | 2.70% | 2.75% / 2.50% | 3.00% | 3.00% | not published |
| 공시이율 (최저보증) | 2.20% (0.3%) | 1.70% (0.3%) | 1.65% (0.2%) | 1.60% (0.3%) | 1.75% (0.5%) | not published |
| Renewal architecture | 갱신형 riders on 1~3년 and longer blocks | **whole product 20/30년 갱신** on the direct form | mixed | 갱신형 riders | 갱신형 riders | 비갱신 |

**What does not vary.** The insured comes into existence at birth and cover attaches then;
유산 or 사산 voids the contract and returns the premium; a 태아 contract is priced at
계약나이 0 and re-rated at birth; the death benefit is unavailable below 만 15세; the
neonatal covers run on a one-year term; the 무해지 form exists at every carrier and is priced
18%–33% below the 표준형; the surrender value on the suppressed form is nil for the whole
payment period and steps up at 납입완료; the product is 무배당; and there is no 만기환급금 on
the protection part.

**Most representative design for a reference implementation.** A 무배당 어린이보험 issued at
보험나이 0 (with a 태아가입 variant), 보험기간 **100세만기**, 보험료 납입기간 **20년납**,
monthly premiums, 비갱신 on the core covers; a 상해후유장해 basic contract of ₩100,000,000
(1억원) paid as 가입금액 × 장해지그률; riders for 암진단비(유사암제외) ₩10,000,000 (1천만원),
유사암진단비 ₩2,000,000 (200만원), 뇌혈관질환진단비 ₩10,000,000, 허혈성심장질환진단비
₩10,000,000, 질병·상해 수술비 ₩5,000,000 each, 질병·상해 입원일당 ₩40,000/day capped at 180
days per stay, 골절진단비 ₩400,000, 화상진단비 ₩200,000 and 가족일상생활배상책임
₩100,000,000 with a ₩200,000 deductible — i.e. the 손해보험협회 comparison basis [R12], which
is the only standardised specification the market itself publishes; a 태아 module carrying
저체중아 인큐베이터 일당 (2일 공제, 60일 한도), 주산기질환 입원일당 (4일 이상, 3일 초과
1일당, 120일 한도) and 선천이상 진단·수술 on a one-year term from birth; a premium waiver on
the child for 50% disability or a named-disease diagnosis, with a 계약자-death switch for the
생명보험 form; **no cancer waiting period below 보험나이 15 and none at all on the 태아
form**; no 감액; a 표준형 / 무해지(납입후 50%) switch with the 무해지 premium at about 78% of
the 표준형; 보장부분 적용이율 2.75%, 공시이율 1.70%, 최저보증이율 0.30%; and no 만기환급금.

---

## Fetch failures and gaps

**Documents downloaded but not readable.**

- **[S14] 흥국생명 「무배당 흥국생명 드림어린이보험1701(보장성) 보험약관」** —
  https://image.kebhana.com/cont/download/insdocument/provide/08L04B24102_agree.pdf returned
  HTTP 200 and a 1,256,989-byte, 103-page PDF, but the file uses non-embedded CID-keyed fonts
  and `pypdf` returned mojibake for every line after the cover. This was the only
  생명보험 어린이보험 **currently sold** that a download URL could be found for, so the
  생명보험 side of this file rests on two 하나생명 wordings [S8] [S9] and one 메트라이프
  wording [S10], none of which is a current product. **The current 생명보험 어린이보험
  product design is therefore not directly evidenced here.**
- **[R4] 금융감독원 2012-09-11 「쌍둥이도 태아보험에 모두 가입할 수 있습니다」** — the PDF
  attachment (273,602 bytes, 2 pp.) is a **scanned image**; text extraction returned 41
  characters, and the FSS 문서뷰어 (`/fss/etc/docView/view.do`) returns only a loading
  placeholder. Only the board page's own summary paragraph was read. The detail of the
  다태아 measure — how the second and later foetuses are covered, and on what premium basis —
  is therefore **unverified**, and the 2× / 3× 다태아 pricing described in §2 rests on [R5],
  a research report, not on the supervisory document.
- **[S13] 현대해상 Hi2504 direct 약관** — the PDF downloaded and the 약관 body extracted, but
  the 상품 안내 issue-age grid, which is what the document was fetched for, is not present in
  the extracted text. No fact rests on it.
- **삼성생명 booklet at `image.kebhana.com/.../08L03014231_agree.pdf`** — downloaded (7.5 MB,
  35 pp.) and extracted cleanly, but it is a **연금보험** booklet, not a child product. Not
  used.

**Pages that would not serve to a fetcher.**

- **[S15] 삼성화재 다이렉트 「어린이보험(태아가입)」** — `curl` reset by peer;
  two `WebFetch` calls returned mutually contradictory product names and premium figures.
  Nothing is taken from it. The consequence is that **삼성화재's own statement of its
  어린이보험 issue ages and 태아 window is not in this file**; its premiums are taken from
  the 손해보험협회 board [S11] instead.
- **[S16] NH농협생명 product page** — reachable only through `WebFetch`. Its figures
  (0~15세 / 0~20세, a 3대질병 parent waiver rider) are recorded as **[unverified]** and no
  parameter is set from them.
- **`www.law.go.kr`** — served one `lsInfoP.do` request (a different statute) and then reset
  the connection on every subsequent attempt, over both the `LSW/lsInfoP.do` and the friendly
  `/법령/<법령명>/<조문>` forms; `DRF/lawService.do` returned HTTP 500; the 행정규칙 form
  `admRulLsInfoP.do` returned 「해당 행정규칙이 존재하지 않습니다」 to `WebFetch`. **No
  statute or 고시 was retrieved from law.go.kr in this pass.** 상법 제732조 came from
  CaseNote [R7]; 상법 제739조 and 보험업감독규정 제7-63조 were read from copies held in this
  session's working directory whose own retrieval this pass could not repeat, and both are
  flagged at their entries [R7] [R10].
- **생명보험협회 공시실 (`pub.insure.or.kr`)** — the site was reached and its menu read, but
  the 상품비교공시 → 보장성보험 comparison tables open through `javascript:void(0)` and no
  어린이보험 rows were obtained. There is consequently **no 생명보험 counterpart to [S11]**
  in this file: every published premium, 예정이율 and 보험가격지수 here is a **non-life**
  figure. This is the single largest gap.
- **보험개발원 (KIDI)** [R13] — not opened. The 어린이보험 새 계약 and in-force series for
  any year after 2015 is therefore missing; §16 relies on the 금융위원회's 2026 aggregate
  [R6] and the 금융감독원's 2008 and 2016 tables [R3] [R2].

**Facts left unverified.**

- **That two carriers extended the issue age to 35 in 2023.** [R1] says 「가입연령을 35세까지
  확대」 without naming carriers; news reports name KB손해보험 and 롯데손해보험 and date the
  KB change to 2023-03. Neither is corroborated by a retrieved product document, and the two
  pre-action 상품요약서 obtained both stop at 30 [S1] [S7]. **[unverified]**.
- **The gestational lower bound for 태아가입.** [R5] gives 8 weeks and [R3] gives "from
  confirmation of pregnancy"; no retrieved primary product document states a lower bound. The
  frequently repeated 손해보험 22주 / 생명보험 16~22주 split is a consumer-guide claim.
  **[unverified]**.
- **어린이보험 premium ₩3.29조원 (2019) → ₩5.32조원 (2023)**, and 2024 new-business growth of
  40.7% / 45.7%. Trade-press summaries only. **[unverified]**. The primary figures in §16 are
  FY05–FY07 [R3], 2013–2015 [R2] and 2026 [R6].
- **Current loss ratio for 어린이보험.** [R5]'s 「보험회사 평균 손해율(약 80% 수준) 미만」 is
  a 2018 statement, itself hedged as 「알려져 있어」. No current figure was retrieved. The
  손해보험협회 publishes a 손해율 board for 실손의료보험 only.
- **어린이보험 as a share of 손해보험 장기인보험 신계약**, on a 월납환산초회보험료 basis.
  Not obtained. The nearest verified statement is the premium ratio implied by [R6]
  (₩9.4조원 of ₩42.7조원 보장성 인보험 = 22.0%), which is an **in-force premium** share, not
  a new-business share, and spans both licences.
- **The α formula in the 공시기준이율 definition** [S1] extracted as
  `α = A/ B + C` on one line and `A + C` on the next, which is a two-line fraction flattened
  by the extractor. It is read as α = (A/B + C) / (A + C) on the basis of the definitions
  given for A, B and C, but the bracketing is **[unverified]** and no calculation in the
  reference product depends on it.
- **암보장개시일 in the 현대해상 and KB wordings.** The 면책기간 tables were located in the
  메리츠 상품요약서 [S3] and in the DB benefit definition on the board [S11], but the
  equivalent tables in [S2] and [S4] were not found in the extracted text. The under-15
  disapplication is nonetheless evidenced twice, by two different carriers, in two different
  document types.
- **The 감액기간 position at 삼성화재, 한화손보, 흥국화재, 롯데손보 and KB손보.** Inferred
  from the presence of 「(감액없음)」 in their published benefit names [S11], which is strong
  but is not the same as reading the clause.
- **Whether the 어린이보험 discount of [R6] is applied to the 영업보험료 or the
  보장보험료.** The release says 「어린이보험 보험료를 할인한다」 without specifying, and the
  per-insurer discount tables it points to (on each insurer's own website) were not fetched.
- **KIDI 경험생명표 and any child morbidity table.** Nothing on child incidence rates —
  cancer, cerebrovascular, congenital anomaly, low birth weight, NICU admission — was
  retrieved from 보험개발원, 국가암정보센터 or 통계청 in this pass. **Every incidence
  assumption in `Child_KR_S` will therefore be a [std] construction**, and must say so. The
  only anchors this file provides are the published premium levels (§14), the disclosed
  적용위험률 for a single benefit at [S1] (일반상해 후유장해 발생률(3~100%) at 기본계약,
  5세, 상해1급: **남자 0.0001823, 여자 0.0001163**), and the 보험가격지수, which bounds the
  total premium against the 참조순보험요율.
- **참조순보험요율 for the child covers.** 보험개발원 files these with the 금융위 under
  보험업법 제176조제4항 and they are the denominator of the 보험가격지수 [S1], but they are
  not public and were not obtained.
