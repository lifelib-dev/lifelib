# Sources

Source ids [S#] and [R#] are carried **verbatim** from `_research/child.md`, the citation
ground truth for this product, and are **frozen — never renumber**. Numbering is per product:
`S1` in this file is a different document from `S1` in every other product's `sources.md`, and
the cross-product `references/regulatory-and-actuarial-references.md` runs its own frozen
R1–R62 scheme, cited here as [REG-R#]. **The two R schemes must never be read across.** The
clearest instance is right here: this file's **[R10]** is 보험업감독규정 **제7-63조** read from
a session copy, while the library's **[REG-R10]** is 감독규정 **제6-11조**, and the same
제7-63조 appears in the cross-product library as **[REG-R17]** with a better retrieval. Access
date for every entry: **2026-09-03**.

Three tag families do three different jobs in `product-spec.md`, `technical-notes.md` and
`model.md`:

- **[S#]** — a **primary product document**: a 보험약관 (*boheom yakgwan*, policy conditions),
  a 상품요약서 (*sangpum yoyakseo*, the statutory pre-contract product summary), the
  손해보험협회's regulated 상품비교공시 board, or a carrier product page. These are what make a
  contractual mechanic *sourced* rather than assumed. On this product they carry an unusually
  heavy load: the 태아가입특칙 is quoted verbatim from two independent 약관, and the one
  quantitative rate this file can offer — the single published 적용위험률 — comes from a
  상품요약서 rather than from any actuarial publication.
- **[R#]** — a supervisory, statutory or research reference that **only this product needs**.
  Five of the twelve are 금융감독원 or 금융위원회 보도자료, which is the shape of the evidence
  on 어린이보험: the supervisor has intervened in this product line repeatedly and datably —
  2008, 2012, 2016, 2023 and 2026 — and its releases are the only public documents that
  describe the product as a whole.
- **[REG-R#]** — the cross-product reference library, reprinted in short form at the end so
  that a reader of this page alone can resolve every tag on it.

**Unused sources are omitted, so both schemes have a gap.** `_research/child.md` runs to **S16
and R13**; this file lists **S1–S12, S14–S16 and R1–R12**. `S13` (a 2025-04 edition 약관 of the
same line as [S7]) is omitted because it downloaded and part-extracted but the 상품 안내
issue-age grid it was fetched for was not in the extracted text, so **no fact in the research
file or in the product documents rests on it**. `R13` (보험개발원's statistical services) is
omitted because **no KIDI page was opened and no KIDI table downloaded in this pass**; the
어린이보험 new-business series attributed to 보험개발원 comes second-hand through [R2], which
cites it, and the cross-product entries [REG-R33] [REG-R34] [REG-R61] carry what could be
retrieved from that publisher. Nothing was newly retrieved at drafting and **no tag was
added**.

**Three of the fifteen primary documents were not usable, and they are listed anyway.** [S14]
downloaded cleanly and then defeated text extraction; [S15] could not be fetched at all and its
two summariser renderings contradicted each other; [S16] is reachable only through a
summariser. An entry that records a failed retrieval is worth more than a silently dropped
source, and each says which facts it was *not* allowed to support. **Nothing is taken from
[S14] or [S15].** [S16] is used only as a marker of [unverified] figures, and **no parameter of
the reference product is set from it.**

Company and branded product names appear in this file and in `_research/child.md` and nowhere
else in the library. In `product-spec.md`, `technical-notes.md` and `model.md` a carrier is its
tag alone, so a reader can always resolve who said what — here — and never has to.

---

## Primary product sources

Fifteen documents. Six are 상품요약서 [S1] [S2] [S3] [S4] [S5] [S6]; six are 보험약관 — three
생명보험 [S8] [S9] [S10], two 손해보험 [S7] [S12], and one 생명보험 that could not be read
[S14]; one is the 손해보험협회's regulated comparison board [S11]; and two are carrier product
pages [S15] [S16].

**The 손해보험 side dominates, and that is a product fact rather than a sampling accident.**
어린이보험 is written on a 장기손해보험 chassis far more often than on a 생명보험 one, and the
comparison board this file leans on is the 손해보험협회's, reached through `kpub.knia.or.kr` —
not the 생명보험협회's portal, to which this product's documents must never be attributed. Five
of the six 상품요약서 were downloaded through the board's own `SUMMARY_SEQ` links [S11].

(krlib-child-s1)=

### S1 — 「무배당 내Mom같은 어린이보험1910 상품요약서」, 메리츠화재해상보험(주) (statutory product summary)

- Document: 상품요약서, 80 pp., product code `1910` (2019-10 edition)
- URL: `https://kpub.knia.or.kr/file/download/25184.knia`
- Accessed: 2026-09-03, Retrieved: **yes** (588,656-byte PDF, 80 pp., 118,078 characters
  extracted cleanly, including every rate and cash-value table)
- **The single most quantitatively load-bearing document in this set**, and the sharpest
  exhibit of the pre-2023 generation. It carries the full 가입나이 grid at **0~30세** on the
  100세만기 forms, which with [S7] evidences the age creep the supervisor stopped [R1]; the
  태아 sub-term `1~10월만기 전기납 태아 월납`; the five 형 (표준형 / 계약전환형 /
  해지환급금미지급형 Ⅰ, Ⅱ, Ⅲ) and the **published ten-step graded ladder** — 5% from M rising
  five points every two years to 50% from M+18 — that `cv_form = "graded"` implements; the
  **적용해지율 actually used to price the 무해지 forms**, 5.0% / 3.0% / 1.0% by duration band
  and 0.5% after 납입완료, which is `lapse_table.csv`'s `disclosed` basis and the anchor of the
  `loglinear` basis's 5.0% start; the note 「1형(표준형) 및 2형(계약전환형)에는 적용해지율이
  적용되지 않습니다」, which is why the 표준형 comparison is a synthetic one; the 보장부분
  적용이율 and 공시이율; a 보험가격지수 table by sex and form; the 저체중아·선천이상·출생위험
  benefit definitions and the incubator formula 「최고 60일을 한도로 실제 사용일수에서 2일을
  공제하고」 that `neonatal_table.csv` implements as written; and a complete published
  surrender-value grid on a named specimen contract.
- **It carries the only 적용위험률 published anywhere in this product's source set**:
  「일반상해 후유장해 발생률(3~100%), 기본계약, 5세, 상해 1급 — 남자 0.0001823, 여자
  0.0001163」. That single pair is the calibration point of `incidence_table.csv`'s
  `disability` cause, the origin of the shipped table's male-heavier direction (a ratio of
  1.57) and the only observation of a Korean child morbidity rate in the whole research pass.

(krlib-child-s2)=

### S2 — 「무배당 현대해상굿앤굿어린이종합보험Q(Hi2607) 상품요약서」, 현대해상화재보험(주) (statutory product summary)

- Document: 상품요약서, 98 pp., product code `Hi2607` (2026-07 edition)
- URL: `https://kpub.knia.or.kr/file/download/91540.do`
- Accessed: 2026-09-03, Retrieved: **yes** (1,406,799-byte PDF, 98 pp., 153,931 characters
  extracted cleanly)
- **The current generation of the market's archetypal product** — the 굿앤굿어린이 line
  descends from the 2004-07 굿앤굿어린이CI보험, the best-selling child policy ever written in
  Korea [R5] — and the most heavily cited document in `product-spec.md` and
  `technical-notes.md` after [S11]. It establishes: 가입나이 **태아~15세** across every 만기,
  which is the post-2023 envelope; the three 종 (표준형 / 해약환급금 미지급형 / 보험기간
  연장형) and their three complete cash-value grids, of which the 표준형 grid is
  `av_table.csv`'s `build` curve on a named specimen — 남자 5세, 상해 1급, 100세만기 20년납
  월납 at 월납 50,000원, 공시이율 1.7% (2026-07), 평균공시이율 2.5%, 최저보증이율 0.3%; the
  **premium-waiver trigger set** (7대질병, 50% 이상 후유장해, 중대한특정상해수술) and its
  **P코드 carve-out**, 「출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지
  않음」, which `waiver_rate_child()` implements; the **태아보장기간 = 계약일~출생일**
  construction with the list of covers that attach to it, and the **태아전용 보장** list on a
  1년만기 term, which are `neonatal_cost_pp("birth")` and `("block")`; the statement that the
  suppressed forms are 순수보장성 and show 「-」 for the 적립부분; and the 부양자 and
  임신·출산질환 rider stacks with the parent's and mother's issue-age ranges — the 20~47세 band
  from which the 계약자's [std] age of 만 33 is taken.

(krlib-child-s3)=

### S3 — 「(무) 내Mom같은 어린이보험2607(1종)(1형) 상품요약서」, 메리츠화재해상보험(주) (statutory product summary)

- Document: 상품요약서, 149 pp., product code `2607` (2026-07 edition)
- URL: `https://kpub.knia.or.kr/file/download/92812.do`
- Accessed: 2026-09-03, Retrieved: **yes** (953,278-byte PDF, 149 pp., 206,285 characters
  extracted cleanly)
- **The 면책기간 / 감액기간 matrix, benefit by benefit** — the document behind the whole
  waiting-period section of `product-spec.md` and behind `cover_open()` and `waiting_mths()` in
  the model. Two notes in it decide how the model behaves: 「최초계약과 부활계약의 면책기간은
  **보험나이 15세 이상인 경우에만 적용**」, which is why the test is applied at the 계약일 and
  never again, and the fact that a **태아가입용 rider has 「면책기간 없음」 at all**. It also
  carries the 누수사고 90-day 보장개시일 and its reset at renewal, behind `leak_share`; the
  market's drift to 감액없음, printed in the benefit names; and the note that waiting periods
  re-run from the 부활일, which is what makes the absorbing-lapse simplification larger on this
  product than on the chassis. Being the same product line as [S1] seven years later, the two
  together give a clean before-and-after on the 2023 supervisory action [R1].

(krlib-child-s4)=

### S4 — 「KB 금쪽같은 자녀보험Plus(무배당)(26.07) 1종 1형 상품요약서」, KB손해보험(주) (statutory product summary)

- Document: 상품요약서, 207 pp., product code `26.07`
- URL: `https://kpub.knia.or.kr/file/download/92757.do`
- Accessed: 2026-09-03, Retrieved: **yes** (3,035,628-byte PDF, 207 pp., 344,997 characters
  extracted; the extraction interleaves Korean and Latin runs inside table cells, so the
  가입나이 grid had to be read carefully, but it is legible)
- The **110세만기** form — the longest term found anywhere in this research — with 가입나이
  태아, 0~15세, which is model point 6 and the 1,320-month projection. It also establishes that
  the 일반상해사망 basic cover is written **only from 만 15세**, which is 상법 제732조 [R7]
  showing through into the product structure and part of the evidence that the market writes no
  death benefit on a child; and a 태아 obligatory-rider block on a 1년만기 전기납 term.

(krlib-child-s5)=

### S5 — 「무배당 let:play 자녀보험(도담도담)(2604) 6종 상품요약서」, 롯데손해보험(주) (statutory product summary)

- Document: 상품요약서, 299 pp. (147 pp. of extractable text), product code `2604`
- URL: `https://kpub.knia.or.kr/file/download/91786.do`
- Accessed: 2026-09-03, Retrieved: **yes** (2,046,981-byte PDF, 169,450 characters extracted)
- The **gestational-week enrolment limits stated in a primary document** — 임신 22주 이내 for
  the neonatal rider block, 임신 15주 이내 for one dental rider — which is the enrolment-window
  fact everywhere else attributed to a supervisor's briefing [R3]. It is also the document that
  makes a **부양자 death rider compulsory on any 태아 contract**, which is the 손해보험 form of
  the parent-side economics the composite instead carries as a *decrement*; the full
  가족일상생활배상책임 wording with its three per-occurrence limits and two deductibles, behind
  `liability_severity`; and the 손해보험 design constraint on 질병사망 riders (80세만기 이내,
  개인당 2억원 이내).

(krlib-child-s6)=

### S6 — 「(무)NH아이맘헤아림어린이보험[2종:표준형]2604 상품요약서」, NH농협손해보험(주) (statutory product summary)

- Document: 상품요약서, 81 pp., product code `2604`
- URL: `https://kpub.knia.or.kr/file/download/88346.do`
- Accessed: 2026-09-03, Retrieved: **yes** (803,926-byte PDF, 89,976 characters extracted)
- The carrier that **still applies a 감액기간** — 암진단비 at 50% within the first year, and
  likewise 항암방사선치료비 and 항암약물치료비 — against a market that has drifted to 감액없음.
  It is what makes `reduction_mths = 12` a real option rather than a legacy switch (model point
  7), and it is used in the carrier-variation table of `product-spec.md`. It also contributes
  to the 가입나이 태아~15세 evidence set.

(krlib-child-s7)=

### S7 — 「무배당 현대해상다이렉트굿앤굿어린이보험(Hi2204) 약관」, 현대해상화재보험(주) (policy conditions)

- Document: 보험약관 with 약관 이용 가이드북, 시각화된 약관 요약서, 상품 안내, 보통약관,
  특별약관 and 별표; 366 pp. by PDF page count, 265 pp. of extractable text
- URL: `https://www.hi.co.kr/data/202204/(무)현대해상다이렉트굿앤굿어린이보험(Hi2204)_인쇄용약관3_페이지.pdf`
  (fetched percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (5,774,914-byte PDF, 558,560 characters extracted;
  some 별표 pages are image-only)
- The **갱신형 architecture in its clearest form** — 20년만기 / 30년만기 blocks with automatic
  renewal and renewal-age ceilings expressed as `(100-보험기간)세` — which is the chassis
  `Child_KR_S` documents and deliberately does **not** implement. It also carries **제27조
  보험나이 verbatim with its worked example** (생년월일 1988-10-02 / 계약일 2014-04-13 ⇒ 25년
  6월 11일 ⇒ 26세), 제28조 계약의 소멸 and 제29조 계약의 자동갱신, and the pre-2023
  direct-channel 가입나이 **0~30세** that pairs with [S1] as the second age-creep exhibit. It
  is a direct (internet-only) product and does **not** offer 태아가입.

(krlib-child-s8)=

### S8 — 「무배당 하나1Q어린이보험 약관」, 하나생명보험(주) (policy conditions)

- Document: 보험약관 including 무배당 주산기질환입원특약, 특정 신체부위·질병 보장제한부
  인수특약 and 지정대리청구서비스특약; 93 pp.
- URL: `https://hanalife.co.kr/home/download2.do?downFileName=(무)하나1Q어린이보험_계약자용약관.pdf&fileName=PROD/(무)하나1Q어린이보험_보험약관.pdf`
  (fetched percent-encoded; the server declares `application/x-msdownload`, the file is a PDF)
- Accessed: 2026-09-03, Retrieved: **yes** (1,860,906-byte PDF, 93 pp., 136,222 characters
  extracted cleanly)
- **The 태아가입특칙 in full and verbatim, 제53조 to 제61조 — the single most important text
  behind this product.** Every structural fact of `Child_KR_S`'s pre-birth period is one of its
  articles: 제54조 「제53조의 태아는 출생시에 피보험자가 됩니다」 (cover attaches at birth, so
  `born(t)` gates every child-life cover); 제56조 「태아가 유산 또는 사산에 의해 출생하지 못한
  경우에는 계약을 무효로 합니다 … 이미 납입한 보험료를 돌려드립니다」 (`pols_void` and
  `claims(t, "VOID")`, a de-recognition and not a lapse); 제58조 「보험금 지급기준표에서
  적용하는 피보험자 나이는 피보험자가 출생한 날부터 계산합니다」 (the 만나이 clock); 제59조
  (the 태아 limbs pay **from the date of birth** even for an event preceding it, which is why
  the module is excluded from `check_cover_at_birth()`); 제60조 「계약일에 있어서의 피보험자의
  계약나이는 0세로 합니다」 (`issue_age() = 0`, and hence a 1,200-month horizon); and 제61조,
  which caps the pre-birth period. It also carries 제30조 보험나이, the 주산기질환 rider
  definition tied to the KCD 출생전후기에 기원한 특정 병태 chapter and its day-capped benefit
  formula, the statement that the 태아형 pays cancer benefits **without 감액**, the three-year
  부활 window, the 청약철회 window, the grace-period wording behind the monthly lapse grid, and
  a published 민원 case explaining that a 태아 contract is priced on **male** rates and trued
  up at birth.

(krlib-child-s9)=

### S9 — 「무배당 하나어린이보험 약관」, 하나생명보험(주) (policy conditions, older wording)

- Document: 보험약관, 119 pp.; an older wording — it still refers to 호적등본 rather than
  가족관계등록부, so it predates the 2008 family-register reform
- URL: `https://www.hanalife.co.kr/anm/product/download.do?code=603427&seq=1`
- Accessed: 2026-09-03, Retrieved: **yes** (616,651-byte PDF, 119 pp., 136,652 characters
  extracted cleanly)
- **A second, independent 태아가입특칙 — 제44조 to 제51조 — whose substance matches [S8]
  article for article.** That correspondence is the evidence that the 특칙 is a market-standard
  text rather than one carrier's drafting, and it is why `product-spec.md` states the foetal
  mechanics as market facts rather than as a single carrier's. It is cited beside [S8] on every
  load-bearing foetal claim, and in particular on the 무효-and-full-refund rule behind
  `claims(t, "VOID")`. It also carries a 보험금 지급기준표 on a ₩10,000,000 (1,000만원)
  보험가입금액 basis and the school-accident disability annuity grid the older generation
  carried.

(krlib-child-s10)=

### S10 — 「무배당 어린이 종합보장보험 약관」, 메트라이프생명보험(주) (policy conditions)

- Document: 보험약관, 55 pp.
- URL: `https://brand.metlife.co.kr/pn/mcvrgProd/mcvrgProdDownloadFile.do?insProdSeq=49&seq=6&fnum=03`
- Accessed: 2026-09-03, Retrieved: **yes** (525,870-byte PDF, 55 pp., 54,908 characters
  extracted; the extraction transposes trailing punctuation and parenthesised glosses to line
  ends, an artefact of the PDF's text ordering, but every clause is readable)
- **The 생명보험 form of the premium waiver, and the reason `Child_KR_S` carries two decrement
  lives.** 제22조 makes the waiver trigger on the child's cancer diagnosis or 50% disability
  **or on the 계약자's own death or 50% 이상 장해**, in one clause — which is
  `waiver_rate_payer()` and the model's second mortality read. 제3조 is what makes that lawful:
  it makes the 피보험자 of the contract 「계약자와 가입자녀」, so the policyholder is himself
  an insured and his death is a contractual event from the 계약일. 제21조 pays a 사망보험금
  only where the child dies **at or after 만 15세**, which is the 상법 제732조 boundary [R7]
  visible in a wording. The composite adopts this waiver in place of the 손해보험 부양자 rider,
  and that substitution is the one deliberate cross-chassis borrowing in the specification.

(krlib-child-s11)=

### S11 — 손해보험협회 공시실, 「어린이보험」 상품비교공시 (`tptyCode=PB24`) (industry comparison disclosure)

- Publisher: 손해보험협회 (General Insurance Association of Korea); board path 상품비교공시 >
  장기보장성 보험 > 어린이보험
- URL (landing): `https://kpub.knia.or.kr/productDisc/longTermGuarantee/juvenileInsurance.do`;
  (popup) `…/popup/disclosurePopup.do?tabType=1&tptyCode=PB24`; (data)
  `POST https://kpub.knia.or.kr/popup/disclosureList.do` with
  `tabType=1&tptyCode=PB24&detailYn=Y&pageIndex=1&pageUnit=100`
- Accessed: 2026-09-03, Retrieved: **yes** — the landing page and popup render as HTML and the
  table itself is loaded by AJAX; posting the form directly returned a 315,774-byte
  JavaScript-object payload covering **41 distinct products from 10 non-life carriers**, with
  89 distinct 담보 and their 지급사유
- **The quantitative spine of this product's documents.** Every published premium, every
  예정이율, every 공시이율 and 최저보증이율 and every 보험가격지수 quoted in `product-spec.md`
  and `technical-notes.md` comes from it, and so do four of the model's standardizations: the
  modal 보장부분 적용이율 of **2.75%** (observed 2.50–3.00), the 공시이율 of **1.70%**
  (observed 1.60–2.20), the 최저보증이율 of **0.30%** (observed 0.20–0.50), and the fact that
  the specimen premium for a male 5-year-old runs **₩21,502 to ₩148,250** — a factor of seven
  on a nominally standardised basis, which is why the model's shipped premiums are [std] inputs
  and the equivalence premium governs. It also establishes that **every one of the ten carriers
  offers a 해약환급금 미지급형 beside the 표준형**; that a 부양자 death rider is compulsory on
  a 태아 contract; the sex relativity with **no fixed sign** (four carriers price the female
  above the male, seven below, the spread 62% to 114%); the broad-versus-narrow
  뇌혈관질환/허혈성심장질환 definitions behind `broad_def_factor`; and a `SUMMARY_SEQ` per
  product from which [S2] [S3] [S4] [S5] and [S6] were downloaded.

(krlib-child-s12)=

### S12 — 「무배당 삼성화재 다이렉트 비갱신 어린이보험(납입면제·해약환급금 미지급형) 2404.17 보험약관」, 삼성화재해상보험(주) (policy conditions)

- Document: 보험약관, product code `2404.17`; 628,118 characters of extracted text
- URL: `https://direct.samsungfire.com/CR_MyAnycarWeb/mall/pdf/mykids_zero.pdf`
- Accessed: 2026-09-03, Retrieved: **yes** (4,762,616-byte PDF; `curl` succeeded on this static
  asset even though the same host's HTML pages were reset by peer)
- A **비갱신 (non-renewable) 무해지 어린이보험 in its pure form**, with the cover-page
  statement `0원 (납입기간 중 해지시) 해약환급금` — the cliff `cv_form = "susp"` implements,
  stated by a carrier on its own cover rather than inferred from a grid. It also carries 제30조
  보험나이 with the standard six-month rule, corroborating [S7 제27조] and [S8 제30조] on the
  age basis the whole model is indexed on, and the 제왕절개·다태아 definitions used in the
  mother-side riders the composite does not model. It carries **no 태아가입특칙**, which is
  itself the evidence that a 비갱신 무해지 form and 태아가입 are separable elections.

(krlib-child-s14)=

### S14 — 「무배당 흥국생명 드림어린이보험1701(보장성) 보험약관」, 흥국생명보험(주) (policy conditions — extraction failed)

- Document: 보험약관, 103 pp., 승인번호 상품개발 제16-AA1-0084호 (2017-01-01)
- URL: `https://image.kebhana.com/cont/download/insdocument/provide/08L04B24102_agree.pdf`
- Accessed: 2026-09-03, Retrieved: **no** — HTTP 200, 1,256,989-byte PDF, 103 pp. downloaded
  successfully, but the file uses non-embedded CID-keyed fonts from page 2 onward and `pypdf`
  returned mojibake for every substantive line. Only the cover page extracted (product name,
  insurer, approval number, and the line 「이 상품은 보장성보험으로 저축성보험(연금)이
  아닙니다」).
- **Nothing is taken from it.** It is listed because `product-spec.md` says in its opening
  paragraph that one 생명보험 약관 was unusable, and a reader is entitled to know which and
  why. The consequence is stated where it bites: the 생명보험 side of this product rests on
  [S8] [S9] and [S10] alone, so the 생명보험 waiver wording has **one** carrier behind it and
  not two.

(krlib-child-s15)=

### S15 — 삼성화재 다이렉트, 「어린이보험(태아가입)」 상품 페이지 (consumer product page — not fetched)

- URL: `https://direct.samsungfire.com/m/mall/baby.html`
- Accessed: 2026-09-03, Retrieved: **no** — `curl` was reset by peer at the proxy, and two
  `WebFetch` calls returned **mutually inconsistent** renderings, one naming a 삼성생명 product
  and one a 삼성화재 product, with different premium figures. The page is JavaScript-rendered
  and the summariser is evidently reconstructing rather than reading.
- **Nothing is taken from it.** The 태아~15세 issue-age fact it appeared to support is
  evidenced instead by [S2] and [S4], which are retrieved PDFs. It is listed as the clearest
  case in this product of why a summariser's rendering is not a source: two fetches of one URL
  disagreed about which company sells the product.

(krlib-child-s16)=

### S16 — 「우리아이지킴이NH통합어린이보험(무배당)」 상품 페이지, NH농협생명보험(주) (consumer product page — summariser only)

- URL: `https://www.nhlife.co.kr/ho/ig/HOIG0001M00.nhl?prodCd=N0000709`
- Accessed: 2026-09-03, Retrieved: **in part** — reached only through `WebFetch`, whose output
  is a summariser's rendering rather than raw text
- Reports 가입나이 0~15세 (1종, 30세만기) and 0~20세 (2종, 100세만기), the 태아 sub-term
  construction, and a 3대질병 납입면제 rider on the parent. It is used **only** in the
  issue-age table of `product-spec.md`, where its figures are explicitly marked
  **[unverified]**, and it is the sole 생명보험-side evidence that a 20세 issue age survived
  the 2023 action at one carrier. **No parameter of the reference product is set from it.**

---

## Regulatory and actuarial references

Twelve entries. Five are supervisory 보도자료 [R1] [R2] [R3] [R4] [R6], one is a
regulator-issued 표준약관 annex [R8], two are FSC releases on the 실손 boundary and the lapse
assumption [R9] [R11], one is a research chapter [R5], two are statutory or regulatory text
[R7] [R10], and one is the disclosure board's own standardised comparison basis [R12].

(krlib-child-r1)=

### R1 — 금융감독원, 「보험회사의 건전성 악화 및 소비자 피해 우려가 없도록 불합리한 보험상품 구조를 개선하였습니다」 (2023-07-19) (supervisory press release)

- Publisher: 금융감독원 보험감독국 특수보험2팀; 보도자료, 3 pp.; 배포 2023-07-19, 보도
  2023-07-20 조간
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=129212&menuNo=200218`;
  (file) `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=fa4f2c0a57b145c98c22c31aba142627&fileSn=2&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (283,196-byte PDF, 3 pp., extracted verbatim)
- **The datable supervisory action on 어린이보험**, quoted in full in `product-spec.md`. It is
  a 감독행정 rather than a rule change, announced for publication on 2023-07-20 with existing
  products to be amended by the end of **2023-08**. Its diagnosis — that extending 가입연령 to
  35 led adults to buy a child-specialised product, and that carriers were bolting
  adult-disease covers onto a child policy where their incidence is negligible — is why the
  composite's envelope is 태아~15세 and why the broad adult-disease definitions are a switch
  rather than a base setting. Its remedy bites on the **product name** and not on the issue
  age, which is what `product-spec.md` warns a reader about when reading current product names.

(krlib-child-r2)=

### R2 — 금융감독원, 「어린이보험 관련 불합리한 보험약관 개선」 (2016-07-13) (supervisory press release)

- Publisher: 금융감독원 보험감리실 / 금융혁신국; 보도자료, 8 pp., a 「제2차 국민체감 20大
  금융관행 개혁」 work item; 배포 2016-07-13, 보도 2016-07-14 조간
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=12634&menuNo=200218`;
  (file) `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=99a8ae3b7ea5edca3c2820c6835784be&fileSn=1&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (669,507-byte PDF, 8 pp., extracted verbatim
  including both annexes)
- **The definitive supervisory statement that cover under a 태아 contract attaches at birth**,
  with the sixteen insurers and nineteen products ordered to stop advertising otherwise. That
  is the authority behind `born(t)` and `check_cover_at_birth()`. It also carries the **2015
  변경권고 that removed the 감액 clause for contracts taken out while the insured was a
  foetus**, with the before-and-after 약관 wording set out side by side — which is why
  `reduction_mths()` returns zero on a 태아 contract *whatever the model point says*, the
  disapplication living in the cells rather than in a CSV. Its 2013–2015 market statistics, and
  the 어린이보험 definition it quotes (「… 가입연령 : 0세~15세」), are the market-size figures
  `product-spec.md` uses for the pre-2026 period, and are the second-hand route to 보험개발원's
  series.

(krlib-child-r3)=

### R3 — 금융감독원, 「태아보험 가입시 알아두면 유익한 사항」 (2008-06-24) (consumer-guidance briefing)

- Publisher: 금융감독원 보험계리실 손해보험팀/생명보험팀; 정례브리핑 자료, 9 매, the eighth in
  a 보험소비자 유의사항 series; 배포 2008-06-24, 보도 2008-06-27 조간
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=6703&menuNo=200218`;
  (file) `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=2576a0971b2b228016d400a6a24b1b65&fileSn=1&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** (137,216-byte HWP5; extracted by inflating the OLE
  `BodyText/Section0` stream and decoding the `HWPTAG_PARA_TEXT` records — 9 pp. of text plus
  both 참고자료)
- **The best single explanation of what a 태아보험 is and why**, and the source of the
  legal-personality argument that opens `product-spec.md`: a 태아 has no legal personality and
  cannot be the 피보험자 of an 인보험 contract, so the 특약 makes the foetus the insured at
  birth. It also gives the enrolment window, the treatment of foetal death, the **male-rate
  pricing convention and the true-up after delivery**, a **worked claim example with itemised
  amounts** — ₩16,836,420 on a birth at 32 weeks and 1.84 kg, of which ₩4,200,000 was neonatal
  day benefits, which is the datum showing the module is **day-capped rather than
  amount-capped** — and, in 참고자료2, 어린이보험 신계약건수 and 수입보험료 split between
  생명보험 and 손해보험 for FY05–FY07 with the 태아 share.

(krlib-child-r4)=

### R4 — 금융감독원, 「쌍둥이도 태아보험에 모두 가입할 수 있습니다」 (2012-09-11) (supervisory reference release)

- Publisher: 금융감독원 보험감독국 보험업무팀; 보도참고자료, 2 pp.
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=9460&menuNo=200218`
- Accessed: 2026-09-03, Retrieved: **in part** — the board page's own summary block was read in
  full from the HTML, but the attached 2-page PDF (273,602 bytes) is a **scanned image** and
  yielded 41 characters of text; the 문서뷰어 returns only a loading placeholder
- Used verbatim from the page summary for one dated fact: from **2012-10-01** all foetuses of a
  multiple pregnancy became insurable, where previously only one was covered. It is the 다태아
  entry in the product-history timeline and in the not-modelled register; the **pricing**
  consequences of a 다태아 plan (roughly 2× for twins, 3× for triplets, which the researcher
  notes probably understates the risk) are taken from [R5] instead, and nothing further from
  this release is used.

(krlib-child-r5)=

### R5 — 보험연구원, 「Ⅷ. 어린이보험의 성장」, 연구보고서 2018-5 『보험상품 변천과 개발 방향: 생명보험 상품 중심』 (research report chapter)

- Publisher: 보험연구원 (Korea Insurance Research Institute); 김석영·김세영·이선주, 2018-02;
  chapter Ⅷ, pp. 221–245
- URL: `https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2018-05_08.pdf` (fetched
  percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (1,100,236-byte PDF, 22,638 characters extracted;
  the figures are images and their captions only partly extracted, and two table cells lost a
  trailing character — 「뇌성마비진」, 「저체중아보」 — which is an extraction artefact)
- **The history of the product, with dates**, and the whole of the product-history section of
  `product-spec.md`: 1958-07 진학보험; the decline of 교육보험 after 1990; the 1997 arrival of
  어린이 보장성 상품; the **2000 introduction of the 태아가입특약**; 2003 and the 2004-07
  어린이 CI보험 that the archetypal current product descends from; the 2005 addition of
  high-cost critical-illness benefits; **the 2006 removal of the 90-day cancer waiting period
  for 어린이보험**, there being no evidence of anti-selection or of a 위험률차손 at child ages,
  which is the origin of the disapplication `waiting_mths()` implements; the 2011 move to 100세
  만기; the **2013 P-code neonatal-haemorrhage dispute** and its loss-ratio consequences, which
  is why `neonatal_table.csv`'s `neonatal_haem` frequency is flagged regime-dependent rather
  than stationary; the 2018-vintage view of the long-guarantee risk under IFRS 17; and a
  **premium-by-issue-age index** — a 0세 issue at 100 against a 30세 issue at 264 for the same
  cover — that `technical-notes.md` uses as a sanity check on the shipped basis. It is also the
  source for the liability limb being the one a non-life licence is needed to write, and for
  the rider count that makes the diagnosis benefits three riders among more than a hundred.

(krlib-child-r6)=

### R6 — 금융위원회, 「보험업권이 출산‧육아에 따른 보험료 부담을 덜어드립니다 — 4.1일 「저출산 극복 지원 3종 세트」 시행」 (2026-03-31) (press release)

- Publisher: 금융위원회 보험과; 보도자료, 6 pp.; 배포 2026-03-31 09:00, 보도 2026-04-01 조간
- URL (post): `https://fsc.go.kr/po010101/86598`; (file)
  `https://fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=86598&fileTy=ATTACH&fileNo=2`
- Accessed: 2026-09-03, Retrieved: **yes** (284,255-byte PDF, 6 pp., extracted verbatim)
- **The current market-size figure**, from a primary supervisory document: 어린이보험 annual
  premium **₩9.4조원** against about **₩42.7조원** for all 보장성 인보험, both as at 2026-03.
  It also describes the **1%–5% premium discount for one year** on a birth or on parental
  leave, effective 2026-04-01 at every insurer, which is the `prem_discount_rate` module (model
  point 10 at 5%); and it records that 어린이보험 is expressly **excluded** from the companion
  보험료 납입유예 scheme, so there is no deferral state for the model to carry. Whether the
  discount bites on the 영업보험료 or the 보장보험료 is not stated and is **[unverified]**; the
  model applies it to the whole office premium.

(krlib-child-r7)=

### R7 — 상법 제732조 (15세미만자등에 대한 계약의 금지) and 제739조 (준용규정) (statute, mirror)

- Publisher: 대한민국 법률, retrieved through CaseNote's statute mirror; the CaseNote page for
  제732조 shows [시행 2015. 3. 12.] [법률 제12397호, 2014. 3. 11., 일부개정]
- URL: `https://casenote.kr/법령/상법/제732조` (fetched percent-encoded)
- Accessed: 2026-09-03, Retrieved: **yes** (56,957-byte HTML; the article text is served in
  both 한글 and the original 한자 forms, with the amendment history and 25 citing judgments).
  `www.law.go.kr` served one request and then reset the connection on every subsequent attempt,
  so CaseNote is the retrieval route; the 제739조 text was read from a session copy of the 상법
  [시행 2026. 7. 23.] whose own retrieval this pass could not repeat.
- **The statute that removes the death benefit from this product.** 제732조 verbatim:
  「15세미만자, 심신상실자 또는 심신박약자의 사망을 보험사고로 한 보험계약은 무효로 한다 …」 —
  which is why `claims(t, "DEATH")` pays the 계약자적립액 and the 미경과보험료 rather than a
  sum assured, and why no `sa_death` exists in `model_point_table.csv`. 제739조 — 「상해보험에
  관하여는 제732조를 제외하고 생명보험에 관한 규정을 준용한다」 — is what makes an
  accidental-death cover on a child lawful even though a disease-death cover is not, which is
  the gap [S1] [S4] and [S11] show the market declining to fill below 만 15세. Every claim
  resting on it is corroborated by [REG-R50] and by the 표준약관 restatement at [REG-R25
  제19조](#krlib-reg-r25).

(krlib-child-r8)=

### R8 — 보험업감독업무시행세칙 [별표 15] 표준약관 (2026.5.6. 시행), 질병·상해보험 표준약관 (supervisor-issued standard conditions)

- Publisher: 금융감독원, as an annex to the 보험업감독업무시행세칙 (제5-13조제1항 관련); `[별표
  15] 표준약관(제5-13조제1항관련)(보험업감독업무시행세칙).hwp`, 1,717,248 bytes, posted
  2026-06-15, stated 「'26.5.6. 시행」
- URL (post): `https://www.fss.or.kr/fss/bbs/B0000115/view.do?menuNo=200504&nttId=218364`;
  (file) `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200504&atchFileId=29447dbe2fa84d85881c10281c6b9d38&fileSn=1&bbsId=`
- Accessed: 2026-09-03, Retrieved: **yes** for the file (1.7 MB HWP5 downloaded in this pass);
  the article text quoted was read from a decoded copy of the same annex held in the session's
  working directory, whose table of contents matches the downloaded file
- The 질병·상해보험 표준약관 is the wording an 어린이보험 is actually written on. Two
  provisions are load-bearing here: **제19조(계약의 무효) 제2호 and 제3호** — a contract on the
  death of a person under 만15세 is void, and the age-eligibility saving in 제3호 expressly
  does **not** extend to the under-15 death prohibition, which is 상법 제732조 [R7] made
  contractual — and **제21조(보험나이 등)**, the six-month rounding rule with its worked
  example, which is the age basis `age(t)` implements. The same annex is entry [REG-R25] in the
  cross-product library with a fuller retrieval and a wider article set; the documents cite
  [R8] where the extraction was done for this product and [REG-R25] where the cross-product
  reading governs.

(krlib-child-r9)=

### R9 — 금융위원회, 「4월부터 "유병력자 실손의료보험"이 출시되고, 실손의료보험 끼워팔기가 금지됩니다」 (2018-03-30) (press release)

- Publisher: 금융위원회; 보도자료, 2018-03-30
- URL: `https://www.fsc.go.kr/po010101/73088`
- Accessed: 2026-09-03, Retrieved: **yes** via `WebFetch` (the page renders; the output is a
  summariser's rendering of it, and the quoted sentence and the regulation citation are
  reproduced from that rendering)
- **Why a modern 어린이보험 has no 실손 rider.** From April 2018, 실손의료보험 — including
  유병력자실손 — must be sold as a **standalone product** consisting only of indemnity-medical
  cover: 「4월부터 유병력자 실손의료보험을 포함한 실손의료보험 상품은 실손의료 보장으로만
  구성된 단독상품으로 분리·판매토록 규정」, under 보험업감독규정 제7-63조제2항제1호 as amended
  2017-03-22 with a one-year transition. That is a statutory impossibility and not a design
  choice, and it is why `product-spec.md` lists 실손의료비 riders as unavailable rather than as
  out of scope. It corroborates [R10], which quotes the same article from a copy whose
  retrieval could not be repeated.

(krlib-child-r10)=

### R10 — 보험업감독규정 제7-63조 (제3보험의 보험상품설계 등) (supervisory regulation — retrieval not repeatable)

- Publisher: 금융위원회고시; 행정규칙
- URLs attempted: `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000246213` and
  `https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000246213`
- Accessed: 2026-09-03, Retrieved: **in part** — `curl` returned HTTP 000 (connection reset) on
  both forms and `WebFetch` on the first returned 「해당 행정규칙이 존재하지 않습니다」. The
  article text quoted was read from a copy of the 보험업감독규정 **[시행 2023. 3. 2.]
  [금융위원회고시 제2023-10호]** held in the session's working directory, whose own retrieval
  this pass could not repeat and whose URL is not known.
- Two provisions are used. **제7-63조제2항제1호** is the standalone-실손 rule quoted at [R9].
  **제7-63조제1항제1호** requires a 제3보험 contract to pay the **계약자적립액 and the
  미경과보험료 and terminate** on a death the 약관 does not cover — which is exactly what
  `claims(t, "DEATH")` computes, and the largest single benefit line on the anchor cell after
  hospital cash.
- **Because the retrieval could not be repeated, every fact resting only on this entry is
  additionally supported by [R9], which cites the same article, and by the cross-product entry
  [REG-R17], which carries the full article text from a successful retrieval of the current
  고시.** Where the documents cite [R10] alone the claim is marked accordingly.

(krlib-child-r11)=

### R11 — 금융위원회·금융감독원, 「합리적인 계리가정과 단계적 할인율 조정을 통해 보험회계의 신뢰도와 안정성을 높이겠습니다」 (2024-11-07) (press release, 제4차 보험개혁회의)

- Publisher: 금융위원회 and 금융감독원; 보도자료, 2024-11-07
- URL: `https://www.fsc.go.kr/no010101/83351`
- Accessed: 2026-09-03, Retrieved: **yes** via `WebFetch` (the page renders; the quoted
  fragments are reproduced from that rendering and were cross-checked against a decoded copy of
  the same release held in the session's working directory)
- **The 2024 intervention on the 무·저해지 lapse assumption**, and the authority behind
  `lapse_table.csv`'s `loglinear` basis: a **log-linear model as the 원칙모형**, with the lapse
  rate converging to **0.1% at 납입완료** and a post-completion ultimate of **0.8%** (or 20% of
  the 표준형 product's rate). It also gives the industry series behind the statement that the
  market is in the suppressed forms — 무·저해지 as a share of 보장성 초회보험료 running 11.4%
  (2018) → 30.4% (2021) → 47.0% (2023) → **63.8%** (2024 H1). 어린이보험 is not named in the
  release, but every 무해지 어린이보험 form on the board [S11] is inside its scope.
- **The gap is at instrument level and is stated wherever it bites.** The 「IFRS17 주요
  계리가정 가이드라인」 attachment was never converted from HWP, so the two endpoint *values*
  are verified from the 보도자료 while the **functional form is [unverified]** — which is why
  `technical-notes.md` ships the disclosed step function of [S1] beside the 원칙모형 rather
  than relying on the shape alone. [REG-R27] is the cross-product entry for the same release,
  with the 별첨 on the discount-rate transition.

(krlib-child-r12)=

### R12 — 손해보험협회 공시실, 「어린이보험」 비교공시 기준 (the standardised comparison basis)

- Publisher: 손해보험협회; the 가입기준 block printed on the 어린이보험 comparison page — a
  supervisor-sanctioned standard specification, reproduced because **every premium in [S11] is
  quoted on it**
- URL: `https://kpub.knia.or.kr/productDisc/longTermGuarantee/juvenileInsurance.do`
- Accessed: 2026-09-03, Retrieved: **yes** (HTML fetched with `curl` and converted to text)
- **The only specification of a Korean child policy the market itself publishes**, and
  therefore the specification `Child_KR_S`'s model points are drawn on. It defines 어린이보험
  as 「태아·어린이를 포함한 성장기 자녀에게 발생할 수 있는 질병과 상해위험을 보장하는 보험」
  and fixes the basis: 상해 1급; 보험가입금액 상해후유장해 **₩100,000,000 (1억원)**,
  질병후유장해 ₩10,000,000 (1천만원), 진단비 for 암(소액암 제외)·뇌출혈·급성심근경색증
  ₩10,000,000 each, the corresponding 수술비 ₩5,000,000 each, 입원비 **₩40,000**, 배상책임
  ₩100,000,000; term and payment **100세만기 / 20년납** for 세만기 covers and 최장만기 /
  Min(전기납, 20년납) for 년만기 and 갱신형 covers; and the quoted premium as the 보장보험료 of
  the compulsory covers only. Model point 1's whole cover schedule is this block. It is also
  the authority for the 기본계약 being a **percentage scale** (보험가입금액 × 장해지급률)
  rather than a lump sum, for the 수술비 limb paying per operation, and for the 1~180일
  per-stay hospital cap behind `hosp_cap_factor`.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R62 numbering is **distinct from this file's** and is likewise frozen; within that page
plain [R#] refers to its own entries. The **thirty-eight** entries the child documents cite,
all accessed 2026-09-03:

- **REG-R1** — 보험업법 제2조·제4조: 제3보험 as a statutory class (상해·질병·간병) and
  제4조제3항's deeming provision, which is why a life *and* a non-life insurer both write this
  product. Retrieved: yes (full Act, 127,346 characters).
- **REG-R2** — 보험업법 제5조·제127조 등 (기초서류): the **산출방법서 is filed with the FSC and
  never published**, which is why the 적용위험률, the 예정사업비율 and the 예정이율 are all
  [std] here. Retrieved: yes.
- **REG-R4** — 보험업법 제176조 (보험요율 산출기관): the statutory footing of 보험개발원 and of
  the 참조순보험요율 regime, filed under **제4항** with no *general* obligation to publish —
  **제9항** nonetheless permits publication where policyholder protection requires it, which is
  the footing of the 장기손해보험 display at [REG-R61]. Retrieved: yes.
- **REG-R9** — 보험업감독규정 (고시 제2026-16호), 본문: the 보장성보험 definition of
  제1-2조제3호, the **기준연령 요건 남자 만 40세** of 제1-2조제2호 at which [별표 15] 제9호 is
  evaluated, the 평균공시이율, and the fact that the word 예정이율 does not occur in the 고시
  at all. Retrieved: yes (226,083 characters, the whole 고시).
- **REG-R10** — 감독규정 제6-11조 등 (책임준비금, 보증준비금): the reserving layer this model
  does **not** compute. Retrieved: yes. **Not** this file's [R10].
- **REG-R11** — 감독규정 제6-11조의6 (**해약환급금준비금**): the company-level appropriation
  with no counterpart anywhere else in this repository; a 무해지 child policy is precisely the
  shape it was built to catch. Retrieved: yes.
- **REG-R12** — 감독규정 제6-11조의7·제6-13조 (계약자배당): cited only to record that this
  contract is 무배당 and distributes nothing. Retrieved: yes.
- **REG-R13** — 감독규정 제7-1조 등 (**K-ICS 지급여력**), in force from 2023-01-01. Retrieved:
  yes (article text; the 기본요구자본 aggregation renders as an image).
- **REG-R15** — 감독규정 제5-6조 등 (특별계정): cited only to record that this product has
  none. Retrieved: yes.
- **REG-R17** — 감독규정 제7-63조 (제3보험의 보험상품설계): **제1항제1호**, the 계약자적립액
  and 미경과보험료 payable on a death the 약관 does not cover — what `claims(t, "DEATH")` is —
  and **제2항제1호**, the standalone-실손 rule. Retrieved: yes (article text in full). This is
  the cross-product corroboration of this file's [R10].
- **REG-R18** — 감독규정 제7-64조·제7-65조 (산출방법서, 계약자적립액): **현금흐름방식**
  mandatory beyond three years with an adequacy analysis on 최적기초율 and projected cash flows
  — the regulatory use a liability projection like this one serves — and the 공시이율 reset
  machinery. Retrieved: yes.
- **REG-R19** — 감독규정 제7-66조 등 (**해약환급금**): the 해약공제기간 capped at **seven
  years** (제7-66조제1항제2호), the 계약자적립액 accrual and its 최저보증이율 floor
  (제1항제4호), the 미경과보험료 refund on termination (제5항), and 제4항's permission for the
  reduced value of a 무·저해지 form. Retrieved: yes (operative words in full; the formula
  display did not extract).
- **REG-R20** — 감독규정 **[별표 14] 표준해약공제액**: the formula `surr_chg_cap_pp()`
  implements — `5% × 연납순보험료 × 해약공제계수 + 보험가입금액 × 10/1000`, with
  「보험기간(최대 20년)」. Retrieved: yes (1-page PDF, full text including all seven notes).
- **REG-R21** — 감독규정 **[별표 15] 보험가입금액의 산정**: **제9호**, which is what a contract
  with no 일반사망보험금 must use — 「보험가입금액 = (위험보험료 / 정기보험의 위험보험료) ×
  정기보험의 보험가입금액」 — giving `sa_notional_pp()` = ₩132,306,409 on the anchor cell.
  Retrieved: yes (1-page PDF, full text).
- **REG-R22** — 감독규정 제4-32조·제7-45조·제7-51조: the **commission cap** (first-year
  remuneration within the first year's expected premium, instalments at no more than 60% of the
  표준해약공제액 a year) and the 보험가격지수 disclosure obligation. Retrieved: yes.
- **REG-R24** — 시행세칙 **[별표 27] 공시기준이율 산출 기준**: the formula behind the 공시이율
  reset this model carries by reference rather than implementing. Retrieved: yes (3-page PDF;
  two weight formulas render as images and did not extract).
- **REG-R25** — 시행세칙 **[별표 15] 표준약관**: the wording behind almost every contractual
  mechanic here — 제13조 (계약 전 알릴 의무), 제15조, 제17조 (청약철회), **제19조 (무효, with
  the under-15 death bar and the refusal to extend the age-correction saving)**, **제21조
  (보험나이)**, **제22조 (the 계약자적립액 on an uncovered death)**, 제26조 (납입최고),
  **제27조 (부활, three years, including where there is no surrender value)**, 제37조
  (소멸시효), 제43조 (예금자보호), and the definition of 장해 as a **settled** impairment,
  「치유된 후 신체에 남아 있는 영구적인」, which is why `disab_severity` is a severity and not
  a probability. Retrieved: yes (a 492-page PDF, 441,610 characters). The same annex is this
  file's [R8].
- **REG-R26** — 시행세칙 [별표 22] (K-ICS) and [별표 24] (보증준비금): Retrieved: **no**. The
  **대량해지 shock and its 고환급형 test** are therefore second-hand through [REG-R36] and
  everything resting on them carries **[unverified]** — which matters here because model points
  4 and 5 are 무해지 forms.
- **REG-R27** — 제4차 보험개혁회의 보도자료 (계리가정·할인율): the cross-product entry for the
  same release as this file's [R11], with the 별첨 on the discount-rate transition; the source
  of the 0.1% / 0.8% lapse endpoints and the 무·저해지 share series. Retrieved: yes (the 6-page
  보도자료 and the 6-page 별첨).
- **REG-R28** — 무(저)해지환급금 상품구조 개선 (2020) and FSS 소비자경보 (2019): why a
  suppressed form has **no 보험계약대출 and no automatic premium loan** to break a lapse, and
  the regulatory dispensation conditional on having priced with a 최적해지율. Retrieved: yes.
- **REG-R29** — 「불합리한 보험 사업비와 모집수수료를 개편하여 …」 (2019-08-01): the reading of
  the 표준해약공제액 cap as **thirteen months' premium** for a 보장성보험. On this product it
  is the reading that **binds** — the [별표 14] formula limb reaches 56.25 months — so it is
  carried as `surr_chg_cap_months` = 13.0 and `acq_cost_months()` = 11.70 is the 90% of it the
  model deducts. Retrieved: yes.
- **REG-R30** — 보험업권 자본규제 고도화 (2025-03-12) and 지급여력비율 현황: cited beside
  [REG-R13] for the K-ICS layer. Retrieved: **in part** (the FSC page in full; the FSS
  quarterly only partly).
- **REG-R31** — 실손의료보험 개혁방안 (2025-04-01) and the 5세대 launch (2026-05-06): why the
  실손 boundary that keeps this product free of an indemnity limb could move. Retrieved: yes.
- **REG-R33** — 제10회 경험생명표, as reported: the table is released only as 평균수명 and
  기대여명 summary statistics, which is why `mort_table.csv` is a [std] construction.
  Retrieved: yes (article text). **It is a news article, and the only retrieved source for the
  제10회 numbers.**
- **REG-R34** — 보험개발원 public channels (보도자료 listing, 보험정보 빅데이터 플랫폼):
  confirms that the 경험생명표 rates are not distributed. Retrieved: **in part**.
- **REG-R36** — 보험연구원 CEO Report 03호, 「보험개혁회의 내용과 과제: 건전성 제도」: the
  second-hand route to the 대량해지 shock and the 고환급형 test. Retrieved: yes (24 pp.).
- **REG-R38** — 「2024년 생명표 작성 결과」 (국가데이터처) and 「2023년 생명표」 (통계청): the
  완전생명표 age pattern `mort_table.csv` is shaped on, and the 만나이 basis every public
  Korean series is published on. Retrieved: yes (both briefing texts).
- **REG-R39** — KOSIS 완전생명표, single-year `qx` tables: Retrieved: **no** — distributed
  through KOSIS and not fetchable in this pass, which is why the shipped table is anchored at
  fourteen ages and graduated rather than copied.
- **REG-R40** — 「2023년 국가암등록통계 참고자료」 (보건복지부·중앙암등록본부): the 연령별
  발생률 whose *shape* the cancer rows of `incidence_table.csv` rest on. Retrieved: yes
  (41-page PDF, extracted in full).
- **REG-R41** — 「2024년도 건강보험환자 진료비 실태조사」 (국민건강보험공단): the utilisation
  authority behind the shape of the two `hosp_*` causes. Retrieved: yes (PDF, extracted in
  full).
- **REG-R48** — 평균공시이율 and 공시기준이율, carrier regulatory disclosure: the 금리연동형
  mechanics of the 적립부분, including a carrier's printed 공시기준이율 formula. Retrieved:
  **in part** (하나생명 in full; the 교보생명 grid only partly).
- **REG-R49** — 상법 제4편 제1장 통칙 (제638조~제664조): 제659조·제660조 (the statutory
  exclusions), 제662조 (소멸시효), and 제663조, which makes the whole Part one-way mandatory.
  Retrieved: yes (제4편 read in full).
- **REG-R50** — 상법 제4편 제3장 인보험 (제727조~제739조의3): **제732조** (the under-15
  nullity), **제736조** (the 적립금 the insurer must pay where it does not pay a 보험금), and
  **제739조** (제732조 disapplied to 상해보험). The cross-product corroboration of this file's
  [R7]. Retrieved: yes.
- **REG-R51** — 금융소비자보호법 제46조 (청약의 철회): 15 days from the 보험증권 or 30 from
  application, effective on despatch — a pre-inception decrement, out of scope for the model.
  Retrieved: yes.
- **REG-R52** — 예금자보호법 시행령 제18조: the **₩100,000,000** per person per insurer bucket,
  which expressly excludes benefits payable because the term has ended. Retrieved: yes.
- **REG-R57** — 소득세법 제59조의4 (특별세액공제 — 보장성보험료): the **12% credit** on
  premiums up to ₩1,000,000 a year, which is what makes this a 보장성보험 in the tax sense as
  well as the regulatory one. Retrieved: yes.
- **REG-R60** — K-IFRS 제1117호 「보험계약」 제정 의결: IFRS 17 mandatory in Korea from
  **2023-01-01**, which with [REG-R13] is why a hundred-year child contract's lapse assumption
  is a CSM question. Retrieved: **in part** (the release body; the 별첨 HWP carrying the
  standard's own text was not converted).
- **REG-R61** — 보험개발원, 「장기손해보험 참조순보험요율」 공시, published under 보험업법
  제176조제9항: the 「기타피부암 및 갑상선암 이외의 암 발생률」 grid on the insured definition
  excluding C44 and C73, a 질병입원율 grid in expected days per life-year, and 후유장해 rates,
  all by age and sex. Retrieved: yes. **They are net premium rates, not best estimates.** Two
  things must be said plainly here rather than implied. Its **age grid reaches 연령 0 and 10**,
  so it is not the case that no Korean child incidence rate is public. And **this product's
  research pass never opened it** — the `cancer` and `indemnity_medical` passes did, on the
  same day, and [REG-R61]'s own entry records the omission — so `incidence_table.csv` names it
  as the authority its *shape* rests on and remains [std] on every row **because those rows
  were never reconciled to it**, not because no grid exists. The shipped paediatric cancer
  anchors sit at about 0.6 (male) and 0.5 (female) of the published rate at 연령 0 and 10 while
  the adult anchors sit near or slightly above it, so the divergence has no single sign and a
  later pass should re-base rather than rescale.

The cross-product library also carries **REG-R62**, the 손해보험협회 공시실 / e-보험시장 portal
`kpub.knia.or.kr` through which [S1]–[S6] and [S11] were reached. It is **not** listed above
because the child documents cite the primary documents themselves rather than the portal; a
reader tracing a retrieval route should nonetheless know it is there.

---

## Provenance note

Every entry above traces to `_research/child.md`, which is the citation ground truth for this
product: the S# and R# numbering used here is that file's numbering, unchanged, and it is
**never renumbered** because these documents cite against it. **The research file's own
numbering is not this one's** — it runs to S16 and R13, and it carries `S13` and `R13`, which
this file omits as uncited, with the reasons given at the head of this page.

What lives there and not here: the per-source extraction record — which fact came from which
page of which PDF, article by article for the two 태아가입특칙; the nineteen fact-extraction
sections behind `product-spec.md`, including the verbatim quotation of the 2023 감독행정 and
the side-by-side before-and-after 약관 wording of the 2015 변경권고; the carrier-by-carrier
variation table; the full 41-product disclosure dataset behind [S11], with its 89 담보 and
their 지급사유; the retrieval method for each host, including the POST parameters that make
`kpub.knia.or.kr` answer, the HWP5 OLE-stream decoding that recovered [R3], and which
`law.go.kr` forms do and do not return text; and the register of fetch failures and
[unverified] claims.

That register is unusually long for this product and the documents do not hide it. **Nothing on
Korean child incidence — cancer, cerebrovascular disease, congenital anomaly, low birth weight,
NICU admission, paediatric length of stay — was retrieved** from 보험개발원, 국가암정보센터 or
통계청 in this pass, which is a gap in the pass and not in the public record: the
장기손해보험 참조순보험요율 display carries an 암 발생률 and a 질병입원율 grid reaching 연령 0
and 10 [REG-R61] and this pass did not open it; the 경험생명표 rates, any 참조순보험요율 for
mortality, the 산출방법서 behind any carrier's 적용위험률 and 예정사업비율, the K-ICS
대량해지 별표 22, the IFRS 17
계리가정 guideline's functional form, and every Korean expense, commission,
disability-incidence and foetal-loss figure are all outside what any retrieved document says.
That is why exactly one quantitative rate in this product's whole source set — the 일반상해
후유장해 발생률 at 5세 in [S1] — is a published Korean rate, and why every other quantitative
parameter in `Child_KR_S` is tagged **[std]** at the point of use.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-child-r1
[R10]: #krlib-child-r10
[R11]: #krlib-child-r11
[R12]: #krlib-child-r12
[R2]: #krlib-child-r2
[R3]: #krlib-child-r3
[R4]: #krlib-child-r4
[R5]: #krlib-child-r5
[R6]: #krlib-child-r6
[R7]: #krlib-child-r7
[R8]: #krlib-child-r8
[R9]: #krlib-child-r9
[REG-R10]: #krlib-reg-r10
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R50]: #krlib-reg-r50
[REG-R61]: #krlib-reg-r61
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
