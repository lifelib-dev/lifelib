# 즉시연금 (immediate annuity) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for the Korean single-premium immediate annuity, 즉시연금 (*jeuksi
yeongeum*), and for `Immediate_KR_S`, the library's annuity-in-payment model. Unlike every
other product in krlib, this one has no accumulation phase to speak of: a lump sum is paid,
the insurer deducts an acquisition and administration load once, and the residue — the
연금계약 적립액 — is credited monthly at a declared rate and drawn down as an annuity from
the month after inception. Everything interesting about the product happens on the payout
side.

Korea writes the product in three shapes, and the shapes are not variants of one design but
three genuinely different liabilities. **종신연금형** (*jongsin yeongeum-hyeong*, life
annuity) divides the fund by an annuity factor built from an annuitant mortality table and
the declared rate, and pays for life with a guarantee period of 10 or 20 years, or to age
100, or for the annuitant's statutory life expectancy; it cannot be surrendered once in
payment. **상속연금형** (*sangsok yeongeum-hyeong*, inheritance annuity) pays interest only
and returns the fund on death or at maturity; it uses no mortality at all and remains
surrenderable throughout. **확정기간연금형** (*hwakjeong-gigan yeongeum-hyeong*,
annuity-certain) divides the fund over a fixed term, also without mortality. In the Korean
market the middle shape dominates: on the only micro-dataset published for this product,
73.6% of contracts by count and 75.1% by premium were 상속형, against 18.2% 종신형 [R12].
The buyer is not, in the main, hedging longevity; the buyer is parking a large sum in a
tax-free wrapper and preserving the principal for an heir.

That commercial fact produced the single most consequential episode in recent Korean life
insurance: the **즉시연금 과소지급 사태**. The 만기환급형 (maturity-refund) variety of
상속연금형 promises both a monthly annuity and the return of the whole single premium at
maturity — but the premium net of expenses is *less* than the maturity benefit, so part of
each period's interest has to be held back to rebuild the fund. That retention was set out
in the 산출방법서 (the filed premium and reserve calculation basis) and **not** in the 약관
(the policy conditions handed to the policyholder). In November 2017 the 금융감독원's
금융분쟁조정위원회 held that the retention could not be asserted against the policyholder
[R1]; the supervisor extended the ruling to the whole industry in April 2018 [R2]; the
insurers refused a blanket remediation, litigated, lost at first instance across four
carriers, won on appeal, and were finally upheld by the Supreme Court on 16 October 2025
[R6] [R21] [R22]. The disputed sum was put at up to ₩1 trillion (1조원) across about
160,000 contracts [R18] [R19]. No other product in this repository carries a dispute of that
shape — a mismatch between the actuarial basis and the contract wording, adjudicated on the
law of standard-form contracts — and any Korean immediate-annuity model that does not carry
the deduction as an explicit, switchable term is modelling the wrong liability.

This file is the **provenance layer** behind `products/immediate_annuity/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Every fact below carries the tag of the
document it came from: `[S#]` for a primary product document (약관, 상품요약서, 상품안내장,
사업방법서, 공시자료) and `[R#]` for a regulatory, statutory, judicial or statistical
reference, both numbered against the lists in this file. `[derived]` marks a figure I
computed from published figures rather than read; `[unverified]` marks a claim from general
knowledge or a search snippet that could not be confirmed against a retrieved document.
**The source numbering in this file is never renumbered** — the four product documents cite
against it, and a renumber would silently redirect every citation. New sources are appended,
never inserted.

Access date for every fetch in this file: **2026-09-03**.

---

## Primary sources

### S1 — 하나생명, 「무배당 행복knowhow즉시연금보험 상품요약서」
- Publisher: 하나생명보험주식회사 (Hana Life)
- Document: 상품요약서, file stamped `20170403`, 11 pp. PDF
- Doc type: 상품요약서 (statutory product summary handed over at inception)
- URL: https://www.hanalife.co.kr/home/download2.do?fileName=PROD/(%EB%AC%B4)%ED%96%89%EB%B3%B5knowhow%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C_20170403.pdf&downFileName=(%EB%AC%B4)%ED%96%89%EB%B3%B5knowhow%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** — served as `application/x-msdownload` and rejected by the markdown
  fetcher, but the bytes are a clean text-layer PDF and all 11 pages extracted with `pypdf`
- What was read, and what it is good for: the **only full statutory product summary for an
  즉시연금 retrieved in this session**. It carries the product taxonomy (종신연금형 1형/2형,
  종신상속연금형, 정기상속연금형), the issue-age and premium-limit table, the benefit table
  with the 생존연금 / 사망보험금 / 만기보험금 definitions, the 적용이율 and — decisively —
  a **published 개인연금사망률 table** at three ages by sex, the expense breakdown by
  component and by annuity form, the 해지공제액 schedule (nil at every duration), a 15-row
  surrender-value illustration on three interest bases, and the 모집수수료율. This is the
  single richest quantitative source in the file.

### S2 — 교보생명, 「바로받는 연금보험 무배당 Ⅱ」 방카슈랑스 상품안내장
- Publisher: 교보생명보험주식회사 (Kyobo Life), 방카슈랑스본부; distributed by 하나은행
- Document: 상품안내장 (leaflet), 「2016년 4월 개정」, 준법감시인 확인필 1-1603-17
  (2016.03.14), 2 pp.
- Doc type: 보험안내자료 / 상품안내장
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L05024317_r.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (2 pp., text layer extracted in full)
- What it is good for: an earlier vintage of the same carrier's product as [S3], useful
  because the two differ. It shows a **12년(12회) minimum guarantee** on the 종신연금형
  where [S3] shows 10년, no 확정기간연금형 at all, 공시이율 2.83% at 2016-03, 평균공시이율
  3.5%, and 최저보증이율 of 1.5%/1.0% split at ten years. Its 상속연금형 annuity table
  (종신형 and 만기형 10/15/20/30년) extracted cleanly.

### S3 — 교보생명, 「바로받는 연금보험」 방카슈랑스 상품안내장 (SC제일은행 배포본)
- Publisher: 교보생명보험주식회사, 교보방카슈랑스; distributed by SC제일은행
- Document: 상품안내장, illustrations dated 「2017년 12월 현재공시이율 2.52%」, 2 pp.
- Doc type: 보험안내자료 / 상품안내장
- URL: https://www.standardchartered.co.kr/hp/file/ap/pd/694895_baro_ad.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (2 pp., text layer extracted in full)
- What it is good for: **the most complete single 예상연금액 table retrieved** — a common
  model point (일시납 1억원, 남자 55세, 즉시연금형) priced across four 종신연금형 정액형
  guarantee options, three 집중보장형 options, five 상속연금형 options and four
  확정기간연금형 terms, each on three interest bases. It also carries the full product
  envelope (가입나이, 최저보험료, 추가납입, 중도인출), the death-benefit definition, the
  no-surrender rule for 종신연금형, the commutation right, and a **stepped 최저보증이율**
  (1.25% / 1.00% / 0.75%) different from every other retrieved carrier.

### S4 — 동양생명, 「무배당 Angel즉시연금보험」 방카슈랑스 상품안내장
- Publisher: 동양생명보험주식회사 (Dongyang Life); distributed by 하나은행
- Document: 상품안내장, 「2016. 4 개정상품」, 준법감시필 01-1603-003, 2 pp.
- Doc type: 보험안내자료 / 상품안내장
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L74024315_r.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (2 pp., text layer extracted in full)
- What it is good for: a second carrier on the **same model point as [S3]** (남자 55세,
  일시납 1억원), which lets the two be compared directly, plus a 거치형 (5-year deferral to
  age 60) illustration on the same point that isolates the deferral effect. Also the
  clearest statement of the 상속연금형 만기형 selling proposition — 「만기에 수령하는
  만기보험금을 상속 및 상속세 재원으로 활용할 수 있습니다」 — and a three-step
  최저보증이율 (2.0% / 1.5% / 1.0%).

### S5 — 삼성생명, 「에이스즉시연금보험 B2.2(무배당)」 방카슈랑스 상품안내장
- Publisher: 삼성생명보험주식회사 (Samsung Life); distributed by KEB하나은행
- Document: 상품안내장, 판매개시일 2016. 4. 1, 준법감시필 BA 제16-26호, 4 pp.
- Doc type: 보험안내자료 / 상품안내장
- URL: https://image.kebhana.com/cont/download/insdocument/leaflet/08L03024328_r.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (4 pp., text layer extracted in full)
- What it is good for: the most **tax-conscious** product design retrieved. Its 보증지급횟수
  is not a menu of round numbers but a rule — a minimum of 10 years' payments (or the
  annuitant's 기대여명 if shorter, floored at 5 years), a middle option equal to the
  기대여명, and a maximum of (100 − 연금개시나이) years — which is the 소득세법 시행령
  제25조 제4항 제3호 condition written straight into the product [R9]. It also gives a
  bridge/front-loaded variant (브릿지연금형), a 12-month 공시이율 history, a
  surrender-value illustration for 상속연금형 10년만기 on both 즉시 and 거치 bases, and the
  연금선수익자 / 연금후수익자 mechanism.

### S6 — ABL생명(구 알리안츠생명), 「무배당 알리안츠프리미어즉시연금보험 사업방법서 (별지)」
- Publisher: 에이비엘생명보험주식회사 (ABL Life; then 알리안츠생명)
- Document: 사업방법서 별지, filed vintage `120701_130331`, 6 pp.
- Doc type: **사업방법서** (business method statement — one of the three 기초서류 under
  보험업법 제5조 제3호)
- URL: https://abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2017/05/15/03_%EC%82%AC%EC%97%85%EB%B0%A9%EB%B2%95%EC%84%9C(120701_130331)_(%EB%AC%B4)%EC%95%8C%EB%A6%AC%EC%95%88%EC%B8%A0%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (6 pp., text layer extracted in full)
- What it is good for: **the only filed 기초서류 for an immediate annuity retrieved in this
  session.** It gives the 공시이율 machinery in algebraic form — the 공시기준이율 as the
  arithmetic mean of an internal and an external indicator, the external indicator as a
  國庫債 / 회사채 blend weighted by the insurer's own bond book, the three-month weighted
  moving average, and the 80%–120% corridor within which the declared rate may be set — plus
  the 최저보증이율 schedule, the policy-loan rate formula (공시이율 + 1.5%), a
  large-contract discount scale, the annuity-type taxonomy including 부부계약, and the
  annuitant-mortality ratchet clause. It is the 2012–2013 vintage, i.e. exactly the cohort
  at the centre of the dispute.

### S7 — 한화생명, 「한화생명 e연금보험 무배당 약관」
- Publisher: 한화생명보험주식회사 (Hanwha Life)
- Document: 주계약 약관 with 특약 and 부록, edition dated 2024. 4. 1, document code
  1789-046, 150 pp.
- Doc type: **약관** (policy conditions) — verbatim contract wording
- URL: https://direct.hanwhalife.com/products/downloadProxy/%ED%95%9C%ED%99%94%EC%83%9D%EB%AA%85%20e%EC%97%B0%EA%B8%88%EB%B3%B4%ED%97%98%20%EB%AC%B4%EB%B0%B0%EB%8B%B9_1789-046_%EC%95%BD%EA%B4%80_20240401.pdf?docUrl=dynamic%2Fdirect%2Fproduct%2Fcms_LbOsZt9dvgKnqRcB_1715162604727.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (150 pp.; the annuity provisions, the definitions, the 공시이율 article,
  the surrender and 중도인출 articles and 별표1 extracted and read)
- What it is good for: **the post-dispute drafting.** This is a current (2024) 약관 whose
  상속연금형 row in 별표1 now says, in the contract itself, that the annuity is the
  interest on the fund 「에서 소정의 사업비를 차감하여」 — the deduction the 2017 조정결정
  said could not be asserted because it was absent from the 약관 is now on the face of the
  약관. It also gives verbatim: the 보증지급기간 menu including 기대여명, the 100세 guarantee
  arithmetic, the 100.1%-of-premiums floor on the fund at annuitisation, the annuitant
  mortality ratchet, the commutation right, the 보험나이 six-month rule, the no-surrender
  rule for 종신연금, and a 최저보증이율 schedule far below the older cohorts (1.0% / 0.75%
  / 0.5%).

### S8 — 푸본현대생명, 「MAX 연금보험 하이파이브 무배당(B2001) 적립형/거치형 약관」
- Publisher: 푸본현대생명보험주식회사 (Fubon Hyundai Life); distributed by 하나은행
- Document: 약관 booklet with 연금전환특약(거치형) and 지정대리청구서비스특약, 107 pp.
- Doc type: 약관 bound with 약관의 요약 및 가이드
- URL: https://image.kebhana.com/cont/download/insdocument/provide/L17014307_agree.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (107 pp.; the annuity-form pages, the surrender articles and the
  summary pages extracted and read)
- Note on scope: this is a **deferred** annuity, not an 즉시연금. It is cited only for its
  payout-phase machinery, which is the same machinery `Immediate_KR_S` needs, and never for
  an issue-age or premium parameter.
- What it is good for: the richest payout-phase menu retrieved — 종신연금형 기본형 with
  10/20/30년/100세/기대여명 guarantees, a 핵심기간집중형 that doubles the annuity for ten
  years, 확정연금형 out to 50 years, 상속연금형, a **proportional split across forms in 5%
  units**, and a 노후설계자금 lump-sum option of up to 50% of the fund. Its notes give the
  기대여명 definition, the annuitant-mortality ratchet, the commutation right and the
  instalment-frequency interest rule.

### S9 — 우체국보험(체신관서), 「우체국연금보험 2312 약관」
- Publisher: 우정사업본부 우체국보험 (Korea Post Insurance)
- Document: 약관 booklet, product code P200068, vintage 2312, 108 pp.
- Doc type: 약관
- URL: https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/YAK_P200068_202312.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (108 pp.; 제2조 정의, 제3조 지급사유, 별표1 and the annuity notes
  extracted and read)
- Note on scope: again a **deferred** annuity, cited for payout-phase machinery only. It is
  also the public-sector comparator: 우체국보험 is written by the state, not by a licensed
  insurer, and its terms are set by 우체국예금·보험에 관한 법률 rather than 보험업법.
- What it is good for: a **종신연금형 with no 상속연금형 at all**, guarantee periods of
  20년/30년/90세/100세 (note: no 10-year option), a 조기집중연금형 paying 200% or 300% for
  five or ten years, 확정기간연금형 of 5/10/15/20/30년, the 신공시이율 vocabulary, the
  **100.1% floor** on the fund at annuitisation, and the commutation and instalment rules.

### S10 — 하나생명 공시실, 「적용이율 공시 — 최저보증이율 및 경과기간별 중도해지율」
- Publisher: 하나생명보험주식회사
- Document: 공시 web page, product-by-product table
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab5.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch; the annuity rows read)
- What it is good for: **the 최저보증이율 of three of one carrier's own 즉시연금 products by
  sales vintage** — (무)하나즉시연금보험 (2007-10-01 ~ 2009-12-30), (무)넘버원즉시연금보험
  (2009-12-31 ~ 2014-12-31) and (무)행복knowhow즉시연금보험 (2015-01-01 ~ 2018-12-31) —
  all opening at 2.5% / 2.0% and the last stepping down to 1.5% / 1.0%. It also confirms
  that these products carry **no 중도해지율** (no early-surrender rate adjustment), unlike
  the same carrier's savings contracts.

### S11 — 하나생명 공시실, 「적용이율 공시 — 표준이율 및 평균공시이율」
- Publisher: 하나생명보험주식회사
- Document: 공시 web page
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, both tables read)
- What it is good for: the **평균공시이율 series 2016–2026** and the definition
  (「감독원장이 정하는 바에 따라 산정한 전체 보험회사 공시이율의 평균으로, 보험계약의
  체결시점의 평균공시이율을 보험기간 동안 적용합니다」). The 평균공시이율 is the rate the
  illustration rules make carriers show alongside the current declared rate, so it is a
  direct input to reading every illustration in [S2]–[S5].

### S12 — NH농협생명, 「공시기준이율」
- Publisher: 엔에이치농협생명보험주식회사 (NH Nonghyup Life)
- Document: 공시 web page, figures as at 2025년 1월
- URL: https://www.nhlife.co.kr/ho/on/HOON0039M00.nhl
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, formula and table read)
- What it is good for: a **second, different** 공시기준이율 weighting to set beside [S6] —
  외부지표금리 × 40% + 운용자산이익률 × 60%, with the external indicator itself weighted
  국고채 78.5% / 회사채 21.5% for the general account — together with the 조정율 that
  converts the reference rate into the declared rate, product line by product line.

### S13 — 하나생명, 「(무)The하나연금보험」 상품 페이지
- Publisher: 하나생명보험주식회사
- Document: product page, 공시이율 stated as at 2023년 1월
- URL: https://www.hanalife.co.kr/prd/personal/banca/theHana/theHanaJoinGuide.do
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Note on scope: a deferred annuity; cited for the payout-form menu and rate levels only.
- What it is good for: a **활동기집중형** with a 3× or 5× multiple over a 5- or 10-year
  concentration period — the most aggressive front-loading observed — plus a 100세 option in
  the 확정연금형 menu, and a 최저보증이율 of 1.25% / 1.00% / 0.50%.

### S14 — KB국민은행 방카슈랑스, 「(무)IBK e-연금보험(2601)」 상품 페이지
- Publisher: KB국민은행 (agent) for IBK연금보험주식회사
- Document: bancassurance product page, 공시이율 stated as at 2026년 9월
- URL: https://obank.kbstar.com/quics?QSL=F&cc=b033493%3Ab033492&page=C020712&prcode=BK09002747
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- What it is good for: the **most current declared rate retrieved** — 연 2.56% as at
  2026-09 — with a 최저보증이율 of 1.25% / 1.00% / 0.50%, and a payout menu (종신 10/20/30
  년/100세; 확정 5/10/15/20/25/30/60년/100세; 상속 종신) from a monoline annuity writer.
  Cited for rate levels and menu breadth; it is a deferred contract, not an 즉시연금.

### S15 — 한화생명 다이렉트, 「한화생명 e연금보험 무배당」 상품 페이지
- Publisher: 한화생명보험주식회사
- URL: https://direct.hanwhalife.com/products/CM090901
- Accessed: 2026-09-03
- Retrieved: **in part** — the page rendered, but the numeric parameters sit behind a
  calculator widget and did not come back. Only the three-form menu, the 45세 minimum
  annuity age and the marketing claims were readable.
- What it is good for: confirming that the 약관 at [S7] is a currently sold product and that
  its annuity age floor is 45.

---

## Regulatory and actuarial references

### R1 — 금융감독원 금융분쟁조정위원회, 조정결정서 제2017-17호
- Publisher: 금융감독원 (Financial Supervisory Service), 금융분쟁조정위원회
- Document: 조정결정서, 조정일자 **2017. 11. 14.**, 조정번호 **제2017-17호**, 안건명
  「즉시연금(만기/상속형)에서 최저보증이율 적용의 적정성」, 12 pp. PDF, released as an
  attachment to [R2]
- URL: https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=e24e669336e894dd227d7b2d8b9ad652&fileSn=4&bbsId=
- Accessed: 2026-09-03
- Retrieved: **yes** — served as `application/octet-stream`, rejected by the markdown
  fetcher, but the bytes are a clean text-layer PDF and all 12 pages extracted with `pypdf`
- What it is good for: **the single most important document in this file.** It is the
  determination itself, not a report of it. It sets out the applicant's contract in numbers
  (₩1,000,000,000 single premium, ten-year term, monthly annuity, 2012-09-12), the six
  successive annuity levels actually paid from 2012-10 to 2017-10, the expense load
  (5.325%), the death benefit (10% of premiums), the declared rate at inception (4.5%), the
  guaranteed floor (2.5% / 1.5%), the 약관 provisions verbatim (제3조, 제13조, 제16조,
  제17조 and 별표1), the 공시기준이율 formula verbatim, the parties' arguments — including
  the insurer's own description of the retention mechanism — and the committee's reasoning
  on when a 산출방법서 may and may not be incorporated into a 약관.

### R2 — 금융감독원, 보도자료 「금융분쟁조정위원회, 즉시연금 관련 분쟁에서 보험약관에 따라
  산출한 연금을 지급하도록 결정」
- Publisher: 금융감독원 분쟁조정1국
- Document: 보도자료, 배포 2018. 4. 9.(월), 3 pp. PDF
- URL (landing page): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=14077&menuNo=200218
- URL (PDF): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=e24e669336e894dd227d7b2d8b9ad652&fileSn=3&bbsId=
- Accessed: 2026-09-03
- Retrieved: **yes** (landing page as HTML; PDF as bytes, 3 pp., extracted with `pypdf`)
- What it is good for: the supervisor's own **structural description of 만기환급형 즉시연금**
  — premium, less commission and risk premium, credited at Max[공시이율, 최저보증이율], less
  the 만기보험금 지급재원 — a worked ₩100,000,000 illustration assuming ₩6,000,000 of
  expense and risk premium, the fact that the insurer **accepted** the determination in
  February 2018, the **text of the 약관 amendment** made in January 2018 (before and after,
  side by side), and the fact that on 15 March 2018 the FSS notified **every life insurer**
  to handle their own cases the same way.

### R3 — 금융감독원, 보도참고자료 「즉시연금에 가입한 소비자가 「시효 중단」을 원하실 경우
  금융감독원에 분쟁조정 신청하시기 바랍니다」
- Publisher: 금융감독원 분쟁조정1국
- Document: 보도참고자료, 배포 2018. 9. 4.(화), 3 pp. PDF
- URL (landing page): https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=14453&menuNo=200218
- URL (PDF): https://www.fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=94c114d0270a3cd188e3b9c8e3e3e8a6&fileSn=1&bbsId=
- Accessed: 2026-09-03
- Retrieved: **yes** (landing page as HTML; PDF as bytes, 3 pp., extracted with `pypdf`)
- What it is good for: it fixes the **two** 분조위 decisions at 「'17.11월, '18.6월」, records
  that insurers went to court notwithstanding, quotes 금융위원회의 설치 등에 관한 법률
  제53조의2 on the interruption of limitation by a dispute-resolution application, and
  announces the dedicated 즉시연금 corner on the FSS's 파인 portal (opened 2018-09-05).

### R4 — 금융감독원, 보도자료 목록 (검색어 「즉시연금」)
- Publisher: 금융감독원
- URL: https://www.fss.or.kr/fss/bbs/B0000188/list.do?menuNo=200218&searchCnd=1&searchWrd=%EC%A6%89%EC%8B%9C%EC%97%B0%EA%B8%88
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, four rows returned)
- Content: the complete set of FSS press releases whose titles contain 즉시연금 — 2012-09-26
  (소비자경보, nttId 9501), 2018-04-09 (nttId 14077), 2018-09-04 (nttId 14453) and
  2019-01-07 (nttId 14756, a response to press reports about a revived comprehensive
  examination). Used to enumerate the supervisory record and to obtain the nttIds behind
  [R2] and [R3].

### R5 — 금융감독원, 「"즉시연금보험 절판마케팅 주의하세요" 소비자경보 발령」
- Publisher: 금융감독원 소비자보호총괄국
- Document: 보도자료, 2012. 9. 26.
- URL: https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=9501&menuNo=200218
- Accessed: 2026-09-03
- Retrieved: **in part** (landing page HTML; the body summary came back but the attachment
  was not opened)
- Content: the government's tax announcement of **2012-08-08**, which removed the
  interest-income exemption for 즉시연금 held ten years or more from the following year,
  and the resulting end-of-line selling push by insurers and banks that the FSS warned
  against. This is the demand shock that created the 2012 cohort at the centre of the
  dispute.

### R6 — 대법원 2025. 10. 16. 선고 2022다225897 판결 [보험금]
- Publisher: 대법원 (Supreme Court of Korea)
- Document: 판결; 원심 서울동부지방법원 2022. 2. 9. 선고 2020나32079 판결
- URLs: https://casenote.kr/%EB%8C%80%EB%B2%95%EC%9B%90/2022%EB%8B%A4225897 ·
  https://lx.scourt.go.kr/search/detail/precedent/0/2025000024727 ·
  https://www.law.go.kr/LSW/precInfoP.do?mode=0&precSeq=612847
- Accessed: 2026-09-03
- Retrieved: **yes** (all three mirrors fetched; 판시사항, 판결요지 and 주문 read; the full
  이유 was not reproduced by any of the three)
- Content: the four holdings on 명시·설명의무 and on what happens when it is breached; the
  finding that a pointer clause 「그 문서에 따라 계산한다」 to an undelivered document
  containing only formulae does **not** discharge the duty; the principle that the contract
  survives with the offending term severed and is then construed objectively by the
  understanding of an average customer; and the conclusion that severance does not change
  the annuity payable. 주문: 「원심판결을 파기하고, 사건을 서울동부지방법원에 환송한다」.

### R7 — 대법원 판례속보, 「상속만기형 즉시연금보험상품에 가입한 보험계약자들이 연금산출
  방식에 대한 명시·설명의무 위반을 주장하며 미지급 생존연금액의 지급을 청구하는 사건」
- Publisher: 대법원
- Document: 판례속보, 2025. 10. 16. 선고 중요판결
- URL: https://scourt.go.kr/portal/news/NewsViewAction.work?gubun=4&searchOption=&searchWord=&seqnum=10690
- Accessed: 2026-09-03
- Retrieved: **in part** — the page returned, but the fetcher rendered the case number as
  「2022마225897」, which is inconsistent with the 「2022다225897」 given by all three
  sources at [R6]. **The 다 form is taken as correct**; the 마 rendering is treated as a
  fetch artefact.
- Content: the court's own headline description of the case, which is the source for calling
  the disputed shape **상속만기형**.

### R8 — 대법원 2023. 6. 29. 선고 2019다300934 판결 (상속형 즉시연금보험계약에 따른
  사망보험금청구권의 법적 성질)
- Publisher: 대법원
- URL: https://www.scourt.go.kr/supreme/news/NewsViewAction2.work?seqnum=9286&gubun=4&searchOption=&searchWord=
- Accessed: 2026-09-03
- Retrieved: **in part** (판례속보 page fetched; case number and date confirmed; the
  판시사항 and 판결요지 came back only in paraphrase, and the attempt to open the judgment
  on CaseNote returned HTTP 503)
- Content: a separate Supreme Court decision on the legal character of the death-benefit
  claim under a 상속형 즉시연금 where the policyholder nominated a third party as insured.
  Recorded for completeness; **no fact in this file rests on it.**

### R9 — 소득세법 시행령 제25조 (저축성보험의 보험차익)
- Publisher: 법제처 국가법령정보센터 (소득세법 시행령, 대통령령)
- URL: https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=1000316648&lsId=003956&chrClsCd=010202&print=print
  (cross-checked against https://www.nhis.or.kr/lm/lmxsrv/law/lawFullContent.do?SEQ=393&SEQ_HISTORY=48036)
- Accessed: 2026-09-03
- Retrieved: **yes** for the structure and for 제4항 각 호 verbatim; **in part** for 제4항
  제5호, whose 계산식 is typeset as an image and could not be transcribed
- Content: 제3항 (the requirements for a savings contract to escape interest-income tax:
  premium caps of ₩200,000,000 before 2017-03-31 and ₩100,000,000 from 2017-04-01, the
  ten-year rule and its carve-out, the 월적립식 conditions with a ₩1,500,000 monthly cap)
  and **제4항** (the five conditions for a 종신형 연금보험), which is the provision that
  shapes the 종신연금형 guarantee-period menu.

### R10 — 소득세법 제16조 제1항 제9호 (이자소득 — 저축성보험의 보험차익)
- Publisher: 법제처 / CaseNote mirror
- URL: https://casenote.kr/법령/소득세법/제16조
- Accessed: 2026-09-03
- Retrieved: **in part** — the two 목 were returned in paraphrase with the operative phrases
  quoted; the full article text was not transcribed
- Content: the enabling provision. Interest income includes the 보험차익 of a savings
  contract prescribed by Presidential Decree, **except** (가) a contract of ten years or
  more meeting the decree's conditions and (나) a 종신형 연금보험 meeting the decree's
  conditions. Everything in [R9] hangs off this.

### R11 — 법제처 찾기쉬운 생활법령정보, 「노후준비와 연금제도 › 사적연금제도 ›
  개인연금제도 › 연금보험」
- Publisher: 법제처 (Ministry of Government Legislation)
- Document: 생활법령 page, content stated as current at 2026-08-15
- URL: https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2056&ccfNo=3&cciNo=2&cnpClsNo=2
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the state's own plain-language restatement of the three exemption routes (ten-year
  lump-sum with a ₩100,000,000 cap from 2017-04-01, 월적립식 with a ₩1,500,000 monthly cap,
  and 종신형 with annuitisation from 55, no lump-sum option and a guarantee period not
  exceeding life expectancy), plus a side-by-side comparison of 연금보험 and 연금저축보험,
  and the definition of 연금보험 by reference to 보험업감독규정 제1-2조제5호.

### R12 — 이경희, 「즉시연금보험의 특성과 가입자 선택행동 분석」, 보험금융연구 제23권 제1호
  (2012. 2), pp. 101–132
- Publisher: 보험연구원 (Korea Insurance Research Institute), 보험금융연구
- Document: peer-reviewed article, 32 pp. PDF, hosted by KCI
- URL: https://journal.kci.go.kr/kiri/archive/articlePdf?artiId=ART001640411
- Accessed: 2026-09-03
- Retrieved: **yes** (32 pp., text layer extracted; §§I–IV and 표1–표9 read)
- Content: **the only micro-level empirical picture of the Korean immediate-annuity market
  that is public.** 1,414 contracts written by one insurer over FY2008–FY2009, said to be
  about 30% of the market's premium; the buyer profile; the split across payout options; the
  guarantee periods actually chosen; the premium distribution by percentile; the annuity
  amounts by premium band; and — uniquely — a citation of 보험업감독규정 제7-60조 4 for the
  rule that a pure life annuity with no guarantee period may not be sold in Korea.

### R13 — 보험저널, 「4월부터 연금보험 수령액 줄어든다…10차 경험생명표 적용시 15% 하락」
- Publisher: 보험저널 (insjournal.co.kr), 강성용 기자; 입력 2024. 2. 15, 수정 2024. 2. 20
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=21975
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, body and table read)
- Content: a **news article**, and the only source retrieved that quantifies the effect of a
  경험생명표 revision on an annuity in payment. It gives the 6th / 9th / 10th table
  comparison on a fixed ₩200,000,000 fund annuitising at 60 — payment-end age, payment
  period and monthly annuity — and the ~15% fall from the 9th to the 10th. **Secondary
  source; the underlying KIDI release was not retrieved.**

### R14 — 보험매일, 「제10회 경험생명표 개정…소비자에 미치는 영향은」
- Publisher: 보험매일 (fins.co.kr)
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the 제10회 평균수명 (남 86.3세, 여 90.7세; +2.8 and +2.2) and the **65세 기대여명
  (남 23.7년, 여 27.1년; +2.3 and +1.9)**, the direction of the premium effect by line, the
  April application date, and the statement that in-force policyholders are unaffected.
  **Secondary source.**

### R15 — 미래에셋투자와연금센터, 「5년만에 새 경험생명표 적용! 보험료 절약하는 보험가입
  요령은?」
- Publisher: 미래에셋투자와연금센터
- URL: https://investpension.miraeasset.com/contents/view.do?idx=20815
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: corroborates [R14] on the April 2024 application and the life-expectancy figures,
  and states the annuity effect as a premium increase for a given annuity. **Secondary
  source (an asset manager's consumer education page).**

### R16 — 미래에셋투자와연금센터, 「가입 다음 달부터 바로 연금 받는 보험, 어떤 종류가 있나?」
- Publisher: 미래에셋투자와연금센터
- URL: https://investpension.miraeasset.com/contents/view.do?idx=21314
- Accessed: 2026-09-03
- Retrieved: **in part** (HTML fetch; the taxonomy and the minimum-premium sentence returned,
  nothing else)
- Content: the three-way taxonomy in plain Korean, and the observation that minimum premiums
  run from ₩10,000,000 upward and differ by carrier (「M사는 1천만원, S사는 3천만원 등」).
  **Secondary source.**

### R17 — 뉴스타파, 「즉시연금사태 : 또다시 가동된 보험사의 '탈출 마술'」
- Publisher: 뉴스타파 (Newstapa)
- URL: https://newstapa.org/article/bh-br
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch, body read)
- Content: the case study of the ₩1,000,000,000 contract that became 조정번호 제2017-17호,
  quoted 약관 wording, the per-carrier shortfall estimates (삼성생명 55,000 contracts /
  ₩430,000,000,000; 한화생명 ₩85,000,000,000; industry about ₩1 trillion), the
  삼성생명 board's decision to pay ₩37,000,000,000 rather than ₩430,000,000,000, and
  한화생명's refusal of the determination on 2018-08-10. **Investigative journalism; every
  figure taken from it is flagged as such below.**

### R18 — 서울신문, 「'16만명의 1조원' 즉시연금 소송, 소비자 다시 승소…삼성생명 패소」
- Publisher: 서울신문, 2022-01-19
- URL: https://www.seoul.co.kr/news/newsView.php?id=20220119500177
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: 서울중앙지방법원 민사45부, 2022-01-19, 18 plaintiffs organised by
  금융소비자연맹 against 삼성생명, consumers won; the aggregate scope (about 160,000
  policyholders, ₩800bn–₩1tn) and 삼성생명's share (50,000 policyholders,
  ₩400,000,000,000). **News article.**

### R19 — 아시아경제, 「그때 그때 다른 소송 결과…즉시연금 소송 향방은」
- Publisher: 아시아경제, 2022-01-21
- URL: https://www.asiae.co.kr/article/2022012111425045120&mobile=Y
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the docket as at January 2022 — four class actions (교보생명, 동양생명,
  미래에셋생명, 삼성생명) all won at first instance by consumers; an individual action lost
  by the consumer against 삼성생명 and 한화생명 in October 2021; and the per-carrier
  exposures (삼성 ₩400bn, 한화 ₩85bn, 교보 ₩70bn). **News article.**

### R20 — 경향신문, 「삼성생명 즉시연금 소송 패소…"판매원도 제대로 파악 못해"」
- Publisher: 경향신문, 2021-07-21
- URL: https://m.khan.co.kr/national/court-law/article/202107211640001
- Accessed: 2026-09-03
- Retrieved: **no** — HTTP 301 to `https://www.khan.co.kr/` (the site root), i.e. the article
  path no longer resolves. The first-instance particulars below come from search-result
  snippets and are marked accordingly.

### R21 — 리걸타임즈, 「[보험] '삼성생명' 즉시연금보험 가입자들 최종 패소」
- Publisher: 리걸타임즈 (legaltimes.co.kr)
- URL: https://www.legaltimes.co.kr/news/articleView.html?idxno=89743
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the **companion Supreme Court case numbers 2022다308747, 2022다308754**, 57
  plaintiffs, appeals dismissed, and the reasoning that the deduction method could be severed
  while the remainder of the contract stood. **Legal trade press.**

### R22 — 머니투데이, 「대법원 "'즉시연금' 설명 부족하나 계약 유효…미지급금 안 줘도 된다"」
- Publisher: 머니투데이, 2025-10-17
- URL: https://www.mt.co.kr/society/2025/10/17/2025101711452448769
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: 대법원 2부, 주심 엄상필 대법관; 51 plaintiffs against 삼성생명; the
  first-instance win, the appellate reversal and the final outcome; the reasoning that
  voiding the contracts outright would leave policyholders worse off. **News article.**

### R23 — 보험저널, 「즉시연금보험 분쟁이 남긴 숙제…'설명 부족'은 잘못, '계약 무효'는 아냐」
- Publisher: 보험저널, 강성용 기자, 2025-11-05
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=28805
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the practical reading of [R6] for insurers — that the deduction structure must be
  set out in outline in the 약관 and that a bare pointer to the 산출방법서 is not enough.
  **News article carrying a law-firm commentary.**

### R24 — EBN, 「대법 "설명 부족" 판결에…금감원, 즉시연금 불완전판매 점검」
- Publisher: EBN 뉴스센터, 2025-10-19
- URL: https://www.ebn.co.kr/news/articleView.html?idxno=1682654
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the FSS's stated intention, after the Supreme Court ruling, to run a
  consumer-protection inspection into the selling of 즉시연금; and the 2018 industry
  estimate restated (up to ₩1 trillion, 삼성생명 ₩400,000,000,000). **News article.**

### R25 — 한국금융신문, 「[주간 보험 이슈] 생보사 즉시연금 소송 승소…설명 의무 미흡했지만
  계약은 유효에 금감원 점검 外」
- Publisher: 한국금융신문 (fntimes.com), 2025-10-19
- URL: https://www.fntimes.com/html/view.php?ud=2025101912240396138a55064dd1_18
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the same outcome from a second trade title, giving the bench (대법원 2부, 엄상필)
  and 51 plaintiffs, and the FSS follow-up. Used only to cross-check [R22]. **News article.**

### R26 — 日刊NTN, 「[쟁점 예규] 즉시연금보험 상속 평가액은 '상속 개시 당시 해지환급금'」
- Publisher: 日刊NTN (intn.co.kr)
- URL: https://www.intn.co.kr/news/articleView.html?idxno=2015014
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: 국세청 예규 상증 사전-2019-법령해석재산-0378 (법령해석과-183), 결정일
  2021-01-19, holding that an 즉시연금 falling into an estate is valued at the surrender
  value at the date of death; the underlying statute 상속세 및 증여세법 제8조; and the
  facts of the ruling (a 확정형 즉시연금 of ₩195,000,000 written 2016-05 with a 2021-05
  maturity). **Tax trade press reporting a ruling; the ruling itself was not retrieved.**

### R27 — KDI 경제교육·정보센터, 「우체국에서 가입즉시 연금 받으세요!」
- Publisher: 한국개발연구원 경제교육·정보센터, reproducing a 우정사업본부 release
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=116191
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: the launch of 우체국즉시연금보험 on **2011-09-23**: issue ages 45–80, premium
  ₩5,000,000 to ₩250,000,000, 종신형 with a **20-year** guarantee and 상속형, 공시이율
  4.8% at 2011-09, 최저보증이율 2%, a 0.5% discount for premiums of ₩100,000,000 or more,
  and the ten-year exemption. A useful high-rate-era datum and the state provider's entry.

### R28 — 뱅크샐러드, 「즉시연금 총정리 | 1억 넣으면 얼마 받을까? 수령액·비과세·장단점 비교」
- Publisher: 뱅크샐러드 (banksalad.com)
- URL: https://www.banksalad.com/articles/보험-즉시연금-1억
- Accessed: 2026-09-03
- Retrieved: **in part** (HTML fetch; the taxonomy and a worked example returned, the tables
  only in summary)
- Content: a current-market consumer explainer citing a **2026년 4월 공시이율 of 2.67%** and
  a ₩100,000,000 확정형 worked example. **Commercial content site; used only as a
  cross-check on the current rate level.**

### R29 — KB의 생각, 「즉시 연금보험이란? — 뜻 & 정의」
- Publisher: KB국민은행
- URL: https://kbthink.com/dictionary/view.html?dictId=KED-00009822
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML fetch)
- Content: a bank's glossary entry giving the three-way taxonomy, the pre-2013 exemption and
  the February 2013 amendment that cut the exempt threshold to ₩100,000,000 per person, and
  the estate-valuation point. **Secondary; corroborates [R5] and [R9].**

### R30 — 금융위원회 / 예금보험공사, 예금보호한도 상향 (₩50,000,000 → ₩100,000,000)
- Publisher: 금융위원회 보도자료 (2025-05-15 and the 2025-07-22 국무회의 의결)
- URLs: https://www.fsc.go.kr/no010107/84605 · https://www.fsc.go.kr/no010101/84974
- Accessed: 2026-09-03
- Retrieved: **no** — neither release was opened; the effective date and the amount come from
  search-result snippets and from the 금융투자협회 notice they quote. Treated as
  `[unverified]` below.

### R31 — 보험업감독규정 (금융위원회 고시)
- Publisher: 금융위원회 / 법제처 국가법령정보센터
- URLs attempted: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196 ·
  https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000250658&chrClsCd=010201 ·
  https://www.ulex.co.kr/법률/2100000214154-21843-보험업감독 ·
  https://www.fsc.go.kr/po040301/view?noticeId=3864 ·
  https://www.fsc.go.kr/comm/getFile?srvcId=RULENOTICE&upperNo=4076&fileTy=ATTACH&fileNo=8
- Accessed: 2026-09-03
- Retrieved: **no** for the article text. The 국가법령정보센터 administrative-rule viewer is
  JavaScript-rendered and returns navigation chrome only; the U-LEX mirror timed out at 60 s;
  the FSC 입법예고 landing page returned only the notice metadata (예고기간 2023-02-14 ~
  2023-03-27, 보험과) and put the article text in an unretrieved .hwp attachment; and the
  FSC file endpoint served a **규제영향분석서** dated 2025-06-12 rather than the regulation.
- Content actually obtained (all second-hand, and marked `[unverified]` where used): that
  제7-60조 governs 생명보험 상품설계; that 제7-60조 제3호 requires a savings contract's
  net-premium reserve at the 평균공시이율 to exceed cumulative premiums at the end of
  premium payment (7 years where the term is 7 years or more; **15 months for a single
  premium**); that the 2018-01-01 commencement applied to 생존연금 with a whole-of-life
  term; and that 제7-60조 4 forbids a life annuity without a guarantee period of at least
  five years [R12].

---

## Fact extraction

### 1. What the product is, and where it sits

- **Definition.** 「즉시연금은 보험을 가입할 때 보험료 전액을 일시에 납입하고, 그 다음달부터
  매월 연금이 지급되는 보험상품」 — the supervisor's own words [R2 §1]. There is no
  premium-paying period and no accumulation phase; the first annuity falls due one month
  after the 보장개시일 [S1] [S3] [S4].
- Contractually the product is **two contracts in one**. 「계약자는 다음에 정하는 보장계약과
  연금계약을 동시에 체결하여야 합니다」 — a 보장계약 that funds the death benefit and a
  연금계약 that funds the 생존연금 and, where applicable, the 만기보험금 [R1, quoting the
  약관 제3조]. The premium splits three ways: 보장계약 보험료 (B), 사업비 (C) and the
  residue D = A − B − C, which becomes the 연금계약 적립액 [R1 §1-가 table].
- The vocabulary is unusually stable across carriers. The periodic payment is **생존연금**
  (survival annuity), the fund is the **연금계약 적립액** or **계약자적립액**, the annual
  amount is the **연금연액** and the monthly amount the **연금월액** [S1] [S3] [S7] [R1].
- **Two selling modes** are offered on almost every product: 1종/즉시형, which annuitises a
  month after inception, and 2종/거치형, which defers by 1–5 years (교보, 삼성, 동양) or up
  to the annuitant's chosen 연금개시나이 (ABL) [S3] [S4] [S5] [S6]. `Immediate_KR_S`
  models the 즉시형 only; the 거치형 is the accumulation chassis and belongs to
  `Pension_KR_S`.
- **Sales channel.** Every retrieved 즉시연금 document is a **방카슈랑스** (bancassurance)
  leaflet or a bank-channel summary — 하나은행 [S2] [S4] [S5], SC제일은행 [S3], 우체국
  [R27]. The product is sold across a bank counter to a customer with a large deposit,
  which is consistent with the premium distribution at [R12] and with the very low
  commission rates at [S1].

### 2. The payout shapes — taxonomy across carriers

Every retrieved carrier offers a menu of the same three families, with a fourth
(front-loaded) variant of the life-annuity family under different names.

| Carrier / product | 종신연금형 | 상속연금형 | 확정(기간)연금형 | Source |
|---|---|---|---|---|
| 하나생명 행복knowhow즉시연금 | 1형 (10년, 20년 보증), 2형 (10년, 20년 보증) | 종신상속연금형; 정기상속연금형 10/15/20년 | — (none) | [S1] |
| 교보생명 바로받는연금보험 Ⅱ (2016-04) | 정액형 12년/20년/30년/100세; 집중보장형 12년/20년/30년 | 종신형; 만기형 10/15/20/30년 | — (none) | [S2] |
| 교보생명 바로받는연금보험 (2017-12 예시) | 정액형 10년/20년/30년/100세; 집중보장형 10년/20년/30년 | 종신형; 만기형 10/15/20/30년 | 10/15/20/30년 | [S3] |
| 동양생명 Angel즉시연금 | 개인형 10년/20년/30년 보증 | 종신형; 만기형 10년/20년 | — (none) | [S4] |
| 삼성생명 에이스즉시연금 B2.2 | 순수종신연금형 기본형 및 브릿지연금형, 보증지급횟수 = 최소 / 기대여명 / 최대 | 종신형; 만기형 10/15/20/30년 | — (none) | [S5] |
| ABL 알리안츠프리미어즉시연금 (2012) | 개인계약/부부계약, 정액형 10년/20년/100세, 소득보장형 10년/20년 | 종신플랜; 환급플랜 10/15/20년 | 5/10/15/20/30년 | [S6] |
| 한화생명 e연금보험 (2024, 거치) | 10년/20년/100세/기대여명 | 종신 | 10/15/20년 | [S7] |
| 푸본현대 MAX 하이파이브 (거치) | 기본형 10/20/30년/100세/기대여명; 핵심기간집중형 10/20/30년/100세 | 종신 | 5/10/20/30/40/50년 | [S8] |
| 우체국연금보험 2312 (거치) | 정액형 및 조기집중연금형, 20년/30년/90세/100세 | — (none) | 5/10/15/20/30년 | [S9] |
| 하나생명 The하나연금보험 (거치) | 정액형 10/20/30년/100세/기대여명; 활동기집중형 20년 | 개인연금형 (종신) | 5/10/15/20/30년/100세 | [S13] |
| IBK e-연금보험 2601 (거치) | 10/20/30년/100세 | 종신 | 5/10/15/20/25/30/60년/100세 | [S14] |

- **The 상속연금형 is not universal but is close to it** on 즉시연금 specifically: seven of
  the seven immediate-annuity products above carry it. The one clear exception among all
  retrieved products is 우체국연금보험, which has none [S9] — a state provider declining to
  sell the estate-planning shape.
- Conversely, **확정기간연금형 is often absent from an 즉시연금** — 하나생명 [S1], 동양생명
  [S4], 삼성생명 [S5] and the 2016 교보 vintage [S2] all omit it, while the 2017 교보
  vintage [S3] and ABL [S6] carry it. Where it is absent, the 상속연금형 만기형 (which pays
  interest for a term and then returns the principal) does the same job in a different
  shape.
- **The 상속연금형 splits in two.** 「종신형에서는 가입자가 살아 있을 경우 운용이자를
  연금급여로 지급하며, 사망 시에는 동 시점의 책임준비금을 지급한다. 만기형에서는 운용이자를
  확정기간(예: 10년, 20년 등) 동안 지급하며, 동 기간 중 사망하면 그 시점의 책임준비금을
  지급한다. 만약 가입자가 만기 시점까지 생존하면 만기보험금을 지급한다」 [R12 §III-1]. It
  is the **만기형** that generated the dispute; the 종신형 has no maturity benefit to fund.
- Names for the same thing differ and must be normalised. The interest-only shape is
  「상속연금형」 [S1]–[S5] [S7]–[S8], 「종신플랜 / 환급플랜」 [S6], 「즉시상속형」 [R1],
  「만기환급형 즉시연금」 [R2] and 「상속만기형」 in the Supreme Court's own headline [R7].
  The front-loaded life annuity is 「집중보장형」 [S2] [S3], 「브릿지연금형」 [S5],
  「소득보장형」 [S6], 「핵심기간집중형」 [S8], 「조기집중연금형」 [S9] and
  「활동기집중형」 [S13].

### 3. 종신연금형 — the life annuity and its guarantee period

- Definition, verbatim from a current 약관: 「연금개시시의 계약자적립액을 기준으로 피보험자가
  생존한 기간 동안(연금개시시점부터 계약자가 선택한 보증지급기간(10년, 20년, 100세,
  기대여명)동안 보증) 산출방법서에서 정한 방법에 따라 연금액을 분할 계산하여 매년
  보험계약해당일에 지급」 [S7 별표1].
- **A pure life annuity cannot be sold in Korea.** 「우리나라는 종신형이라 하더라도
  순수종신형은 허용되지 않으며 적어도 5년 이상 보증기간을 설정해야 한다(보험업감독규정
  제7-60조 4)」 [R12 §III-2-라]. The regulation text itself could not be retrieved [R31], so
  the citation is recorded on the authority of the paper; the *effect* is corroborated by
  every retrieved product, none of which offers a life-only option.
- **Observed guarantee-period menus.** 10년 and 20년 are near-universal; 30년 appears at
  교보 [S2] [S3], 동양 [S4], 푸본현대 [S8], 하나 [S13] and IBK [S14]; 12년 appears once, on
  the 2016 교보 vintage [S2]; 90세 appears only at 우체국 [S9]; **100세** appears at 교보,
  ABL, 한화, 푸본현대, 하나, IBK and 우체국; **기대여명** appears at 한화 [S7], 푸본현대
  [S8] and 하나 [S13], and in rule form at 삼성 [S5].
- **"100세 보증" is not a hundred years.** 「보증지급기간이 100세인 경우에는
  [보증지급기간-연금개시나이+1]년을 보증지급」 [S7 별표1 주6]; 우체국 puts it as 「연금지급
  보증지급기간(90세 또는 100세)은 연금지급개시일부터 90세 또는 100세 계약해당일의
  전일까지입니다」 [S9]. For an annuity starting at 55 the 100세 option is therefore a
  **46-year guarantee** `[derived]`.
- **삼성's rule-based menu is the clearest statement of what drives the design.** The
  보증지급횟수 is a multiple of 12 chosen by the policyholder between a minimum and a
  maximum: 「"최소보증지급횟수"란 10[단, 피보험자의 기대여명이 10보다 작은 경우에는
  기대여명으로 하며 최소 5로 함]년 동안의 연금월액 지급횟수를 말하며, "최대보증지급횟수"란
  100에서 연금지급개시나이를 차감한 년수 동안의 연금월액 지급횟수를 말함」 [S5 주4], with
  기대여명 defined by the statutory table 「관련세법에 따라 통계표(통계법 제18조에 따라
  통계청장이 고시)에 따른 성별·연령별 기대여명 연수(소수점 이하는 버림)」 [S5 주5]. The
  minimum of 5, the ten-year default and the tie to 기대여명 are all the shape of
  소득세법 시행령 제25조 제4항 제3호 [R9] (§18 below).
- **The 기대여명 definition in a 약관**, verbatim: 「기대여명은 피보험자의 '성별∙연령별
  기대여명 연수'를 말하며, 피보험자의 연금개시나이를 기준으로 산출합니다. … 관련세법에 따라
  통계법 제18조(통계작성의 승인)에 의해 통계청장이 승인하여 고시하는 **가입시점 통계표**의
  성별∙연령별 기대여명 연수(소수점 이하는 버립니다)를 말합니다. … 기대여명이 5년 미만일
  경우 기대여명은 5년으로 하며, 이 경우에는 관련 세제혜택이 제한될 수 있습니다」 [S7 제2조
  제6호 가목]. Note the basis is the **table at inception**, not at annuitisation, and note
  the express warning that the five-year floor can break the exemption.
- **Death inside the guarantee period.** The unpaid guaranteed instalments continue on their
  original dates, or may be commuted: 「종신연금형의 경우 연금지급 개시 후 보증지급기간안에
  사망시에는 잔여보증지급기간 동안, 미지급된 연금월액을 매월 연금지급일에 드립니다. 또한
  미지급된 연금월액을 공시이율로 할인하여 일시금으로 선 지급할 수 있습니다」 [S3]; 「보증
  지급기간(10년, 20년) 중에 피보험자가 사망한 경우에는 보증지급기간(10년, 20년)까지 지급
  되지 않은 생존연금을 생존연금지급일에 드리거나 보험료 및 책임준비금 산출방법서에 따라
  공시이율로 할인하여 선지급할 수 있습니다」 [S1 주5].
- **No death benefit at all after annuitisation on a 종신연금형** at one carrier: 「순수종신
  연금형(기본형, 브릿지연금형)은 연금개시후에는 해지가 불가하며, 연금개시후 사망시 별도의
  사망보험금은 지급되지 않습니다」 [S5]. Others pay 「사망당시의 연금계약 책임준비금 +
  1,000만원(기본보험료의 10%)」 only **before** annuitisation on a 종신연금형, and both
  before and after on a 상속연금형 [S3].

### 4. The front-loaded life annuity (집중보장형 / 브릿지 / 조기집중 / 활동기집중)

- Purpose: pay more in the early years, when the annuitant is active and before the state
  pension starts, and less later. [R12 §III-1] frames the demand — 「은퇴 후 국민연금 수령
  전까지 가교연금이 필요할 경우」.
- **교보's 집중보장형**: 「연금지급 개시시점부터 보증지급기간(10년, 20년, 30년)까지 연금액의
  100%를 추가로 지급하도록 설계한 연금지급형태입니다」 [S3] — i.e. double for the guarantee
  period, then the base amount.
- **삼성's 브릿지연금형**: a 브릿지횟수 chosen between 5 years (60 payments) and the
  보증지급횟수, over which the annuity is a stated multiple (the illustrated case is 2×) of
  the later amount [S5 주6].
- **우체국's 조기집중연금형**: 조기집중기간 5년 or 10년, 연금액비율 200% or 300%, with a
  worked diagram — 「조기집중기간 10년, 연금액비율 200% 신청시 : 연금개시나이 계약해당일부터
  10년간 연금액(100만원)은 조기집중기간 종료 후 연금액(50만원) 대비 200%를 지급」 [S9].
- **푸본현대's 핵심기간집중형**: fixed 10-year 핵심기간 at 2× — 「핵심기간(10년)까지는
  핵심기간(10년) 이후 연금액의 2배가 되도록 계산된 연금액」 [S8].
- **하나's 활동기집중형**: the widest range — 집중지급기간 5년 or 10년 at **3배 or 5배**,
  with a 20-year guarantee [S13].
- Observed multiples across carriers: **2×, 3×, 5× (and 200%/300%)**; observed concentration
  periods: **5 and 10 years**, or the whole guarantee period [S3] [S5] [S8] [S9] [S13].

### 5. 상속연금형 — the interest-only shape

- **종신형** (whole-of-life): 「연금지급 개시시점의 연금계약 책임준비금을 기준으로 공시이율로
  계산한 이자를 생존연금으로 지급하고, 사망시에는 해당 시점의 연금계약 책임준비금에
  기본보험료의 10%를 더하여 일시금으로 지급하며, 만기형의 경우 만기생존시에 만기환급금을
  지급하는 형태」 [S3].
- The **current** 약관 wording adds the deduction that the 2017 determination said was
  missing: 「「연금개시시의 계약자적립액을 기준으로 공시이율에 의해 계산한 이자 상당액」에서
  **소정의 사업비를 차감하여** 매년 보험계약 해당일에 지급(단, 피보험자 사망시에는 사망시점
  계약자적립액 지급)」 [S7 별표1]. Compare the 2012-vintage wording at §14.
- **만기형** (term): the maturity benefit is 「연금계약 적립액(기본보험료 해당액)」 [S1
  정기상속연금형], i.e. an amount equal to the single premium; and 「상속연금 만기형
  거치연금형의 만기환급금은 만기시점의 적립액[이미 납입한 보험료(기본보험료+추가납입보험료
  −적립액 인출금액)해당액]을 지급합니다」, with the caveat that declared-rate movement in
  the final month can make the two differ slightly [S3].
- **This is the shape at the centre of the dispute.** Its defining property — that the
  maturity benefit equals the *gross* premium while the fund starts at the *net* premium —
  is what forces a retention out of each interest payment. See §§13–17.
- **It uses no mortality.** 「옵션 중 사망(생존) 위험률이 적용되는 것은 종신형에 한정된다」
  [R12 §III-1]; 「확정형과 상속형은 사망률을 사용하지 않는다」 (same). This is the single
  most important modelling consequence in this file: two of the three shapes are pure
  interest arithmetic and only 종신연금형 needs `mort_table.csv`.
- **It remains surrenderable.** 「확정기간 연금형 및 상속연금형(종신형, 만기형)의 경우
  언제든지 계약을 해지할 수 있으나, 종신연금형(정액형, 집중보장형)의 경우 연금지급개시
  이후에는 계약을 해지할 수 없습니다」 [S3]; 「상속연금형의 경우 보험계약이 소멸하기 전에
  언제든지 해지가 가능합니다」 [S1].
- One carrier permits **partial withdrawal even after annuitisation** on the 종신 shape:
  「'가'에도 불구하고 상속연금형 종신플랜의 경우 연금이 개시된 이후에도 연금계약 계약자
  적립금의 일부를 인출할 수 있다」 [S6 §8-나].

### 6. 확정기간연금형 — the annuity-certain

- 「연금지급 개시시점의 연금계약 책임준비금을 기준으로 계산한 연금액을 일정 기간동안
  지급받는 형태 [10년, 15년, 20년, 30년]」 [S3]; 「연금지급개시시점의 적립금액을 기준으로
  계약자가 선택한 연금지급기간동안 나누어 계산한 금액을 연금지급기간동안 매년 지급」 [S9
  별표1].
- Payment does **not** depend on survival: 「확정형에서는 가입자가 선택한 지급기간 동안
  가입자의 생존여부에 관계없이 연금급여를 지급한다」 [R12 §III-1], and death inside the
  term leaves the remaining instalments payable on their dates or commutable [S9 주7].
- The 교보 product also pays 1,000만원 (10% of the premium) on death both before and after
  annuitisation under this shape [S3].
- Observed term menus: 10/15/20/30년 [S3]; 5/10/15/20/30년 [S6] [S9]; 10/15/20년 [S7];
  5/10/20/30/40/50년 [S8]; and out to **60년 and 100세** at [S14]. A 50- or 60-year certain
  term at issue age 45–60 is longer than any plausible lifetime and is effectively a
  drawdown wrapper.

### 7. Contract architecture and the accumulation identity

- **연금계약 적립액**, verbatim from the 약관 front matter: 「연금계약적립액이란 연금개시
  전에는 연금계약순보험료(사망보장이 있는 경우 납입하신 보험료중 보장을 위한 보험료 및
  예정사업비를 차감한 금액)를 공시이율로 납입일부터 일자계산에 의하여 적립한 금액이며,
  연금개시후에는 생존연금 발생분을 차감한 금액입니다」 [R1, quoting the 약관 서두].
- The same identity in the 상품요약서: 「「연금계약 적립액」은 연금계약 순보험료(기본보험료
  에서 보장계약 순보험료, 계약체결비용 및 계약관리비용을 뺀 금액)를 기준으로 공시이율을
  적용하여 계산한 금액으로 보험료 및 책임준비금 산출방법서에서 정한 바에 따라 계산됩니다」
  [S1 주2].
- So the recursion the model must implement is, per month,
  `V(t+1) = V(t) × (1 + i_m) − annuity(t)` with `i_m` the monthly equivalent of
  Max[공시이율, 최저보증이율], `V(0) = P × (1 − loading)`, and the annuity itself a function
  of `V` at annuitisation and of the payout shape.
- **The fund at annuitisation carries a floor** on deferred contracts: 「연금개시시의
  계약자적립액은 이미 납입한 보험료(중도인출에 의한 인출금액이 있는 경우에는 이를 차감한
  금액)의 **100.1%**를 최저보증 합니다」 [S7 별표1 주8]; the state provider says the same
  — 「연금지급개시일의 적립금액이 이미 납입한 보험료 … 이하일 경우 연금지급개시일의
  적립금액은 이미 납입한 보험료 … 의 **100.1%**로 합니다」 [S9]. Two independent carriers
  at exactly 100.1% is strong evidence of a supervisory floor rather than a commercial
  choice; the regulation was not retrieved, so the *reason* is `[unverified]` while the
  *fact* is sourced twice.
- 「생존연금의 계산은 공시이율을 적용하여 계산되므로 공시이율이 변경되면 생존연금도
  변경됩니다」 [S1 주3] [S4] [R1 별표1 주1] — the annuity in payment is **not** level. It
  moves with the declared rate every month.
- The recursion is stated symmetrically for the payout phase: 「제2보험기간 이후의
  신공시이율이 연금지급개시시점의 신공시이율과 계속 동일한 경우의 해당년도 생존연금은
  직전년도 생존연금과 동일하나, 제2보험기간 이후의 신공시이율이 변경될 경우에는 직전년도의
  생존연금과 차이가 있을 수 있습니다」 [S9 주13].

### 8. 공시이율 — how the crediting rate is set

Two carriers publish the machinery in full, and they differ.

**ABL (알리안츠), 2012 vintage** [S6 §9]:

> 공시기준이율 산출식 = (내부지표 + 외부지표) ÷ 2
> 외부지표 산출식 = B1 × r + B2 × (1 − r)
> B1 : 국고채 수익률의 직전 3개월 가중이동평균이율 … 한국금융투자협회가 매일 공시하는
> 국고채권(3년만기)의 시가평가기준 수익률(YTM)
> B2 : 회사채 수익률의 직전 3개월 가중이동평균이율 … 무보증 AA−(3년만기)
> r : 산출시점 전월말 기준 당사 보유 채권의 장부가액 중 국고채권의 비율로 하며, 5% 포인트
> 단위로 반올림하여 산출한다

- The internal indicator is 「운용자산수익률에서 투자지출률을 차감」 [S6], i.e. investment
  return net of investment expense over the trailing 12 months.
- **The declared rate is bounded**: 「공시이율은 산출공시기준이율의 **80% ~ 120%** 범위내에서
  정한다」 [S6 §9-다].
- Fixed for a month: 「이 계약의 공시이율은 매월 1일 회사가 정한 이율로 하며, 당월 말일까지
  1개월간 확정 적용한다」 [S6 §9-나]; identically [S1 주6], [S3], [S5], [S7 제7조].
- Par products must not be favoured: 「'다'의 공시이율은 동종상품의 배당보험 공시이율보다
  높게 적용한다」 [S6 §9-라].

**The disputed 2012 contract** [R1, quoting 약관 제16조] used a different weighting again:

> ※ 공시기준이율 = 운용자산이익률 × 0.65 + 외부지표금리 × 0.35

with the external indicator 「직전 3개월간의 국고채수익률(5년), 회사채수익률(AAA,3년),
통화안정증권수익률(1년)을 혼합한 이율」 and the same 80%–120% corridor.

**NH농협생명, 2025** [S12]:

> 공시기준이율 = 외부지표금리 × 40% + 운용자산이익률 × 60%
> 적용이율 = 공시기준이율 × 조정율

with the external indicator weighted 국고채 78.5% / 회사채 21.5% / 통안증권 0.0% for the
general account, and, at 2025-01, 공시기준이율 2.86% with 조정율 89.16% giving an annuity
적용이율 of **2.55%** (against 2.35% for protection business and 2.40% for savings).

- So the internal/external split ranges over **50/50 [S6], 65/35 [R1] and 60/40 [S12]**, and
  the corridor is expressed either as a band (80–120%) or as a published 조정율. Any model
  that treats 공시이율 as an exogenous scalar is defensible; any model that claims to derive
  it is not, on this evidence.
- 하나생명 states the same construction in prose and adds that the detail lives in the
  사업방법서: 「회사의 운용자산수익률에서 투자지출률을 차감한 내부지표와 회사채 수익률,
  국고채 수익률 및 통화안정증권 수익률을 반영한 외부지표를 가중평균하여 산출된
  공시기준이율에서 장래 운용수익률, 향후 예상수익 등을 고려한 공시이율에 연동되는 상품」
  [S1 §IV-4].

**Observed declared rates on annuity business, with their dates:**

| Rate | As at | Product / carrier | Source |
|---|---|---|---|
| 4.8% | 2011-09 | 우체국즉시연금보험 | [R27] |
| 4.5% | 2012-09 | the disputed 즉시연금 contract at inception | [R1 §1-라] |
| 4.7% | (design illustration, same carrier) | 즉시연금 상속연금형 10년만기 | [R1 fn.3] |
| 3.40% → 2.80% | 2015-03 → 2016-03 | 삼성 에이스즉시연금 (12-month history) | [S5] |
| 2.95% | 2016-03 | 동양 Angel즉시연금 | [S4] |
| 2.83% | 2016-03 | 교보 바로받는연금보험 Ⅱ | [S2] |
| 2.50% | 2017-04 | 하나 행복knowhow즉시연금 (적립이율) | [S1 §IV-4] |
| 2.52% | 2017-12 | 교보 바로받는연금보험 | [S3] |
| 2.80% | 2023-01 | 하나 The하나연금보험 | [S13] |
| 2.55% | 2025-01 | NH농협생명 (무)연금 적용이율 | [S12] |
| 2.67% | 2026-04 | market figure quoted by a consumer site | [R28] |
| 2.56% | 2026-09 | IBK e-연금보험(2601) | [S14] |

The full arc is a fall from about **4.8% in 2011 to about 2.6% in 2026** on annuity money
`[derived from the table above]`.

### 9. 최저보증이율 — the guaranteed floor, and its collapse by vintage

The floor is stepped by elapsed duration, and the steps have moved down sharply. Observed
schedules, ordered by vintage:

| Vintage | Carrier / product | Schedule | Source |
|---|---|---|---|
| 2007-10 ~ 2009-12 | 하나 (무)하나즉시연금보험 | 10년 이내 2.5%, 10년 초과 2.0% | [S10] |
| 2009-12 ~ 2014-12 | 하나 (무)넘버원즉시연금보험 | 10년 이내 2.5%, 10년 초과 2.0% | [S10] |
| 2011-09 | 우체국즉시연금보험 | 2% | [R27] |
| 2012-07 ~ 2013-03 | ABL 알리안츠프리미어즉시연금 | 5년 이하 2.5%, 5년 초과 15년 이하 2.0%, 15년 초과 1.0% | [S6 §9-마] |
| 2012-09 (disputed contract) | ○○생명 즉시연금 | 10년 이내 2.5%, 10년 초과 1.5% | [R1] |
| ~2008–2010 (sample) | industry, per KIRI | 10년 이내 2.5%, 10년 초과 2.0% | [R12 표2 주1] |
| 2015-01 ~ 2018-12 | 하나 행복knowhow즉시연금 | opens 10년 이내 2.5% / 초과 2.0%, later 1.5% / 1.0% | [S10] |
| 2016-03 | 동양 Angel즉시연금 | 5년 이내 2.0%, 5년 초과 10년 이내 1.5%, 10년 초과 1.0% | [S4] |
| 2016-03 | 삼성 에이스즉시연금 | 10년 이내 1.5%, 10년 초과 1.0% | [S5] |
| 2016-04 | 교보 바로받는연금보험 Ⅱ | 10년 미만 1.5%, 10년 이상 1.0% | [S2] |
| 2017-04 | 하나 행복knowhow즉시연금 (요약서) | 10년 이내 1.5%, 10년 초과 1.0% | [S1 §V] |
| 2017-12 | 교보 바로받는연금보험 | 5년 미만 1.25%, 10년 미만 1.00%, 10년 이상 0.75% | [S3] |
| ~2020 | 푸본현대 MAX 하이파이브 | 5년 이내 1.25%, 5~10년 1.15%, 10년 초과 0.75% | [S8] |
| 2023-01 | 하나 The하나연금보험 | 5년 이내 1.25%, 5~10년 1.00%, 10년 초과 0.50% | [S13] |
| 2024-04 | 한화생명 e연금보험 | **3년 이내 1.0%, 3년 초과 5년 이내 0.75%, 5년 초과 0.50%** | [S7 제7조] |
| 2026-09 | IBK e-연금보험(2601) | 5년 이내 1.25%, 10년 이내 1.00%, 10년 초과 0.50% | [S14] |

- The 2024 한화 schedule is the most aggressive retrieved: it reaches its terminal 0.5% after
  only **five** years, where the older cohorts took ten and terminated at 2.0%.
- The 약관 explains the floor with a worked example: 「예를 들어, 공시이율을 적용하여
  적립하는 금액은 공시이율이 0.25%인 경우, 공시이율(0.25%)이 아닌 최저보증이율(계약일로부터
  3년 이내에는 연복리 1.0%, …)로 적립됩니다」 [S7 제7조].
- The floor is **not** a rate on the annuity; it is a rate on the fund. The annuity moves
  because the fund's credit moves. That is the whole substance of 조정번호 제2017-17호 [R1].

### 10. 평균공시이율 — the supervisory average and its role in illustrations

- Definition: 「감독원장이 정하는 바에 따라 산정한 전체 보험회사의 공시이율의 평균으로,
  전년도 9월말 기준 직전 12개월간 보험회사 평균공시이율」 [S1 주6]; 「보험계약의 체결시점의
  평균공시이율을 보험기간 동안 적용합니다」 [S11].
- Published series [S11]:

  | Calendar year | 평균공시이율 |
  |---|---|
  | 2016 | 3.50% |
  | 2017 | 3.00% |
  | 2018 | 2.50% |
  | 2019 | 2.50% |
  | 2020 | 2.50% |
  | 2021 | 2.25% |
  | 2022 | 2.25% |
  | 2023 | 2.25% |
  | 2024 | 2.75% |
  | 2025 | 2.75% |
  | 2026 | **2.50%** |

  The same page gives 표준이율 for 2013-04–2015 (3.50%, 3.50%, 3.25%) and then stops, the
  standard rate having been superseded.
- **Why it matters for reading an illustration.** The disclosure rules make carriers show
  three columns: the current declared rate, **Min[평균공시이율, 공시이율]**, and the
  guaranteed floor — 「보험계약에 적용하는 실제이율은 공시이율이나, 본 상품안내장에서는
  최저보증이율, 평균공시이율(단, 공시이율 상한) 및 공시이율을 가정하여 생명보험 상품공시
  작성지침에 따라 예시합니다」 [S5]. In every retrieved illustration from 2016 onward the
  declared rate is **below** the average, so the middle column equals the first and carries
  no extra information [S2] [S3] [S4] [S5].
- **An inconsistency to record.** [S3] states its 평균공시이율 as 「이 계약 체결 시점의
  이율(2.5%)」 while illustrating a 공시이율 「2017년 12월 현재 2.52%」. The published series
  puts 2017 at 3.00% and 2018 at 2.50% [S11]. The most likely reading is that the leaflet
  was reprinted in 2018 or later while retaining a December-2017 declared rate; the leaflet
  carries no print date. Both numbers are recorded as printed and neither is corrected.

### 11. Expenses — the full load, by component

The 하나생명 상품요약서 is the only retrieved document giving the whole load by component and
by annuity form. Basis: 남자, 60세, 일시납 5,000만원 [S1 §VIII].

| Form | 계약체결비용 | 계약관리비용 | 위험보험료 | one-off total | 연금수령기간 중 비용 |
|---|---|---|---|---|---|
| 종신연금형 1형 | 2.61% (₩1,305,000) | 1.30% (₩650,000) | 0.00% (₩0) | **3.9100%** | 연금연액의 0.80% |
| 종신연금형 2형 | 2.61% (₩1,305,000) | 1.30% (₩650,000) | 4.9466% (₩2,473,300) | **8.8566%** | 연금연액의 0.80% |
| 상속연금형 (20년만기) | 2.19% (₩1,095,000) | 1.30% (₩650,000) | 1.4669% (₩733,450) | **4.9569%** | 연금연액의 0.80% |

- All of it is taken **once, at inception**: 「계약체결시 일시납보험료의 …%」, and 「위험
  보험료는 가입시점부터 보험기간 동안의 사망을 보장하기 위한 보장계약 순보험료로서
  계약체결시 일시에 차감합니다」 [S1].
- **해지공제액 is nil at every duration** on all three forms: 「경과시점 1년 … 7년이상 /
  해지공제금액(만원) 0 … 0 / 해지공제비율 0.0% … 0.0%」 [S1 §VIII]. A single-premium annuity
  has no unamortised acquisition cost to recover, because the cost was taken up front.
- **모집수수료율** [S1 §VII], basis 남자 60세 일시납 1억원: 종신연금형 **2.08%** in year 1
  and nil thereafter; 상속연금형 **1.75%** in year 1 and nil thereafter. Very low by the
  standards of Korean protection business, and consistent with a bank-counter sale.
- The disputed 2012 contract's load is stated in the determination as **사업비 C = 납입
  보험료의 5.325%** plus a separate 보장계약 보험료 B [R1 §1-가]. The supervisor's own
  worked example assumes 「사업비와 위험보험료가 6백만원」 on a ₩100,000,000 premium, i.e.
  **6.0%** [R2 참고].
- Reconciliation `[derived]`: solving the maturity-refund recursion (§17) against the
  published first-year annuity of the disputed contract gives a total load of **6.054%** —
  5.325% of 사업비 plus about 0.73% of 보장계약 보험료 — which reproduces the supervisor's
  6% assumption almost exactly.
- Additional charges on the deferred variants: 추가납입보험료 carries 「추가납입보험료의
  1%」 plus a monthly 「추가납입보험료 기준금액의 0.015%」 at 삼성 [S5]; withdrawal costs
  「인출금액의 0.2% (2,000원 한도)」 with four free withdrawals a year at 교보 [S3], ABL
  [S6 §8-마], 삼성 [S5], 한화 [S7 제35조] and 우체국 [S9 주10] alike — the most uniform
  parameter in the whole file.
- **A large-contract discount** exists at one carrier and is worth recording because it is
  the only retrieved place where a Korean annuity price varies with size [S6 §10-나]:

  | 일시납보험료 | 할인금액 |
  |---|---|
  | 1억원 미만 (8천만원 초과 1억원 미만 is not written at all) | 0% |
  | 1억원 이상 ~ 2억원 이하 | 일시납보험료의 0.3% |
  | 2억원 초과 ~ 3억원 이하 | 2억 초과금액의 0.7% + 60만원 |
  | 3억원 초과 ~ 4억원 이하 | 3억 초과금액의 1.0% + 130만원 |
  | 4억원 초과 ~ 5억원 이하 | 4억 초과금액의 1.2% + 230만원 |
  | 5억원 초과 | 5억 초과금액의 1.5% + 350만원 |

  and 「계약자가 원할 경우 할인된 금액을 연금계약 순보험료에 더하여 적립한다」 [S6]. 우체국
  gives a flat 0.5% for premiums of ₩100,000,000 or more [R27].

### 12. The published annuity illustrations

**[S3] 교보생명, 일시납 기본보험료 1억원, 남자 55세, 즉시연금형, 공시이율 2.52% (2017-12),
최저보증이율 basis as stated.** Monthly amounts in 만원.

| Form | 공시이율 2.52% | Min[평균, 공시] | 최저보증이율 |
|---|---|---|---|
| 종신 정액형 10년(10회)보증 | 35 | 35 | 28 |
| 종신 정액형 20년(20회)보증 | 34 | 34 | 28 |
| 종신 정액형 30년(30회)보증 | 33 | 33 | 27 |
| 종신 정액형 100세 보증 | 29 | 29 | 22 |
| 종신 집중보장형 10년보증 | 51 내 / 25 후 | 51 / 25 | 43 / 21 |
| 종신 집중보장형 20년보증 | 41 내 / 20 후 | 41 / 20 | 34 / 17 |
| 종신 집중보장형 30년보증 | 35 내 / 17 후 | 35 / 17 | 29 / 14 |
| 상속연금형 종신형 | 19 | 19 | 9 |
| 상속연금형 만기형 10년 | 17 | 17 | 7 |
| 상속연금형 만기형 15년 | 18 | 18 | 8 |
| 상속연금형 만기형 20년 | 18 | 18 | 8 |
| 상속연금형 만기형 30년 | 18 | 18 | 8 |
| 확정기간연금형 10년 | 90 | 90 | 85 |
| 확정기간연금형 15년 | 64 | 64 | 58 |
| 확정기간연금형 20년 | 50 | 50 | 45 |
| 확정기간연금형 30년 | 37 | 37 | 31 |

만기환급금 on every 상속 만기형 row: **1억원** [S3].

**[S4] 동양생명, 일시납 1억원, 남자 55세, 공시이율 2.95% (2016-03).** Monthly, 만원:

| Form | 즉시형 (개시 55) | 최저보증 | 거치형 5년 (개시 60) | 최저보증 |
|---|---|---|---|---|
| 종신 10년보증지급 | 36 | 31 | 45 | 35 |
| 종신 20년보증지급 | 36 | 31 | 44 | 34 |
| 종신 30년보증지급 | 34 | 30 | 41 | 32 |
| 상속 10년만기 | 19 | 12 | 32 | 16 |
| 상속 20년만기 | 21 | 13 | 28 | 13 |

만기보험금 = 이미 납입한 보험료 1억원. **Caveat**: the two blocks were laid out as graphics
and the reading order in the extracted text is ambiguous. The assignment above is checked
arithmetically — a fund of ₩100,000,000 accumulated five years at 2.95% net of about 3.5%
expense supports about ₩450,000/month at age 60 on a ~20.5 factor `[derived]`, which matches
the 45만원 row — but it remains an inference from layout plus arithmetic, not a printed
label.

**[S5] 삼성생명 에이스즉시연금 B2.2, 일시납 1억원, 여자 40세, 공시이율 2.80% (2016-03),
평균공시이율 3.5% (2016).** Monthly, 만원:

| Form | 1종 즉시 (개시 40): 최저보증 / 2.80% | 2종 거치 5년 (개시 45): 최저보증 / 2.80% |
|---|---|---|
| 상속 종신·기본형 | 11 / 21 | 12 / 24 |
| 상속 만기형 10년 | 8 / 18 | 11 / 30 |
| 상속 만기형 20년 | 8 / 20 | 9 / 26 |
| 상속 만기형 30년 | 8 / 20 | 9 / 25 |
| 순수종신 기본형 120회 보증 | 20 / 27 | 23 / 32 |
| 순수종신 기본형 552회 보증 (1종) / 492회 (2종) | 20 / 27 | 22 / 32 |
| 순수종신 기본형 720회 보증 (1종) / 660회 (2종) | 19 / 26 | 21 / 30 |
| 브릿지 120회 보증 (120회, 2배) | 33 / 42 | 36 / 49 |
| 브릿지 552회 (2배) / 492회 (2배) | 21 / 28 | 24 / 34 |
| 브릿지 720회 (2배) / 660회 (2배) | 19 / 26 | 21 / 31 |

Reading the 보증지급횟수 `[derived]`: for a 40-year-old woman, 120회 = the ten-year minimum;
**552회 = 46 years = her 기대여명**; **720회 = 60 years = 100 − 40**, the maximum. For the
2종 at annuity age 45, 492회 = 41 years (기대여명) and 660회 = 55 years = 100 − 45. The two
menus are therefore the same rule evaluated at two ages, exactly as [S5 주4]–[주5] describe.

**[S2] 교보생명 바로받는연금보험 Ⅱ, 일시납 1억원, 남자 55세, 즉시연금형, 공시이율 2.83%
(2016-03).** The 상속연금형 block extracted cleanly; the 종신연금형 block did not (§ fetch
failures). Monthly, 만원:

| Form | 공시이율 2.83% | Min[평균, 공시] | 최저보증이율 |
|---|---|---|---|
| 상속연금형 종신형 | 21 | 21 | 11 |
| 상속연금형 만기형 10년 | 18 | 18 | 8 |
| 상속연금형 만기형 15년 | 19 | 19 | 9 |
| 상속연금형 만기형 20년 | 20 | 20 | 9 |
| 상속연금형 만기형 30년 | 20 | 20 | 10 |

**[R1 fn.3] the 가입설계서 of a parallel dispute**, 상속연금형(10년만기): **617** at a
공시이율 of 4.7% against **279** at the 최저보증이율 (2.5% / 1.5%). Units are as printed
(만원 per month) and the premium is not stated in the extract.

### 13. Derived annuity factors

All of the following are `[derived]` — I computed them from the published illustrations; no
carrier publishes a factor.

**[S3], 남자 55세, 즉시, factor = ₩100,000,000 ÷ 12 × monthly annuity:**

| Form | 공시이율 2.52% | 최저보증이율 |
|---|---|---|
| 종신 10년보증 | 23.81 | 29.76 |
| 종신 20년보증 | 24.51 | 29.76 |
| 종신 30년보증 | 25.25 | 30.86 |
| 종신 100세보증 | 28.74 | 37.88 |
| 확정 10년 | 9.26 | 9.80 |
| 확정 15년 | 13.02 | 14.37 |
| 확정 20년 | 16.67 | 18.52 |
| 확정 30년 | 22.52 | 26.88 |

**[S4], 남자 55세, 즉시, 2.95%:** 종신 10년보증 23.15; 20년보증 23.15; 30년보증 24.51.
The 동양 factor at 55 on a 10-year guarantee (23.15) sits **2.8% below** the 교보 factor on
the same age and shape (23.81), which is what one expects from a declared rate 0.43 pp
higher.

**[S5], 여자 40세, 즉시, 2.80%:** 기본형 120회 30.86; 552회 30.86; 720회 32.05. A female
annuitant fifteen years younger carries a factor about 30% higher than the male-55 factors
above, which is the joint effect of age and sex on a longevity table.

**Back-solving the 확정기간연금형 for the credit rate** is the sharpest available test of the
expense load, because the shape has no mortality in it. Solving
`PV(monthly-in-advance, n years, i) = P × (1 − load)` against [S3]:

| Term | implied `i` on the gross ₩100,000,000 | net of 3.0% | net of 3.5% | net of 4.0% |
|---|---|---|---|---|
| 10년 | 1.585% | 2.232% | 2.343% | 2.454% |
| 15년 | 1.964% | 2.405% | 2.481% | 2.557% |
| 20년 | 1.909% | 2.244% | 2.301% | 2.359% |
| 30년 | 2.039% | 2.272% | 2.311% | 2.352% |

Against a stated 공시이율 of **2.52%**, a load of **3.0%–3.5%** reproduces the four published
annuities to within about 0.2 pp of rate — and 3.49% is exactly the 하나생명 상속연금형
one-off load of 계약체결비용 2.19% + 계약관리비용 1.30% [S1]. Two carriers, two documents,
one number. This is the strongest internal cross-check in the file and it is the basis on
which `product-spec.md` may take a single-premium load of about 3.5% as representative.

### 14. The 즉시연금 과소지급 사태 — chronology

| Date | Event | Source |
|---|---|---|
| 2011-09-23 | 우체국즉시연금보험 launched; 공시이율 4.8%, 최저보증 2% | [R27] |
| 2012-08-08 | Government announces the removal of the ten-year exemption for 즉시연금 from the following year | [R5] |
| 2012-08-09 ~ 09-09 | Surge of new business ahead of the change | [R17] |
| 2012-09-12 | The applicant in 제2017-17호 writes a ₩1,000,000,000 즉시상속형, ten-year term | [R1] |
| 2012-09-26 | FSS issues a **소비자경보** against 절판마케팅 of 즉시연금 | [R5] |
| 2013-02 | Tax law amended; the lump-sum exempt threshold set at ₩100,000,000 per person | [R29] |
| 2017-10 | The applicant's monthly annuity has fallen to about ₩1,360,000 from about ₩3,050,000 | [R1] |
| **2017-11-14** | **금융분쟁조정위원회 조정결정 제2017-17호**: pay the fund times Max[공시, 최저보증] as the 생존연금 | [R1] |
| 2018-01 | The insurer amends the 약관 so that the 약관 and the 산출방법서 agree | [R2 §4] |
| 2018-02 | The insurer accepts the determination; acceptance has the force of a 재판상의 화해 under 금융위 설치법 제55조 | [R2 §3] |
| 2018-03-15 | FSS notifies **every life insurer** to handle its own cases the same way | [R2 §4] |
| 2018-04-09 | FSS press release publishing the determination and the structural explanation | [R2] |
| 2018-06 | **A second 분조위 determination** to the same effect | [R3 §1] |
| 2018-07 | FSS announces an intention to provide 일괄구제 (blanket remediation) in H2 2018 | [R17]; news reporting |
| 2018-08 | 삼성생명's board declines blanket payment of about ₩430,000,000,000 to about 55,000 policyholders and offers about ₩37,000,000,000 instead; 한화생명 refuses the determination on 2018-08-10 | [R17] |
| 2018-09-04 | FSS advises policyholders to file a dispute-resolution application to interrupt the three-year limitation, and says it will hold those applications until final judgment | [R3] |
| 2018-09-05 | Dedicated 즉시연금 corner opens on the 파인 portal | [R3 §2] |
| 2021-10 | An individual action against 삼성생명 and 한화생명 is lost by the consumer | [R19] |
| **2021-07-21** | 서울중앙지방법원 finds for 57 plaintiffs against 삼성생명, ₩598,000,000-odd | [R20], search snippet — see fetch failures |
| **2022-01-19** | 서울중앙지방법원 민사45부 finds for 18 plaintiffs (금융소비자연맹) against 삼성생명 — reported as the consumers' fifth consecutive win | [R18] |
| 2022 (by January) | Four class actions — 교보, 동양, 미래에셋, 삼성 — all won by consumers at first instance; all appealed | [R19] |
| **2022-11 (reported 2022-11-23)** | 서울고등법원 reverses: 「산출방법서도 약관의 내용으로 봐야 한다」 | search snippet — see fetch failures |
| **2025-10-16** | 대법원 2022다225897 (파기환송) and 2022다308747·308754 (상고기각) | [R6] [R21] |
| 2025-10 (following) | FSS announces a consumer-protection inspection into 즉시연금 selling | [R24] [R25] |

### 15. The determination itself — 조정결정서 제2017-17호, in its own words

**Facts** [R1 §1]. 「신청인은 2012. 9. 12. 피신청인과의 사이에 자신을 보험계약자, 피보험자
및 보험수익자로 하여 보험가입금액은 10억원, 보험기간은 10년, 납입기간 및 주기는 일시납,
보험형태는 즉시상속형, 연금지급주기는 1개월로 하는 이 사건 (무)〇〇즉시연금계약 … 을
체결하였다.」

The annuity actually paid, verbatim [R1 §1-가]:

| Period | Monthly 생존연금 |
|---|---|
| 2012-10 ~ 2013-09 | 약 305만원 |
| 2013-10 ~ 2014-09 | 약 259만원 |
| 2014-10 ~ 2015-09 | 약 250만원 |
| 2015-10 ~ 2016-09 | 약 184만원 |
| 2016-10 ~ 2017-09 | 약 138만원 |
| 2017-10 | 약 136만원 |

plus 「이 사건 보험계약 만기인 2022. 9. 11. 납입 보험료 총액 … 10억원을 지급받는다」. So
the annuity fell by **55.4% in five years** while the guaranteed floor was unchanged
`[derived]`.

**The premium split**, from the determination's own table [R1 §1-가 각주2]:

| 구분 | 납입 보험료 총액 (A) | 보험금 |
|---|---|---|
| 보장계약 | 사망보험금 산출에 필요한 보험료 (B) | 사망보험금 : 납입보험료의 10% |
| 연금계약 | 사업비 (C = 납입보험료의 **5.325%**); 만기보험금 및 생존연금 재원 (D = A − B − C) | 만기보험금 : 납입 보험료 총액; 생존연금 |

**The 약관, as it then stood** [R1 §1-나, 별표1]:

> 상속연금형 — 피보험자가 보험기간(10년, 15년, 20년, 30년)중 매년 계약 해당 일에 살아있을 때
> — 보장개시일로부터 만1개월 이후 계약해당일부터 연금지급개시시의 연금계약의 적립액을
> 기준으로 계산한 연금월액을 매월 계약해당일에 지급

with 주1 「생존연금의 계산은 공시이율을 적용하여 계산되기 때문에 공시이율이 변경되면
생존연금도 변경됩니다」, 주6 「연금계약적립액은 이 보험의 산출방법서에서 정한 바에 따라
계산한 금액으로 합니다」 and 주7 「공시이율(가입후 10년 이내에는 연복리 2.5%, 10년을 초과한
경우에는 연복리 1.5%를 최저보증)은 매월 1일 회사가 정한 이율로 합니다」. **Nowhere does the
약관 mention the retention.**

**The applicant's claim** [R1 §2]: at least ₩2,080,000 a month, being 10억 × 2.5% ÷ 12 =
₩2,083,333, which the committee notes is computed on the gross premium without allowing for
the risk premium and expenses — 「그러나 신청인 주장은 보장보험료 및 사업비 공제를 용인할 수
없다는 취지라기보다는 연금액 산출시 최저보증이율 약정이 제대로 이행되고 있는지를 판단해
달라는데 있는 것으로 선해 된다」 [R1 §2 각주4].

**The insurer's own description of the mechanism** [R1 §2], which is the clearest statement
of it anywhere in the retrieved corpus:

> 동 상품은 계약체결 당시 일시납 보험료에서 공제(보장계약보험료와 예정사업비)한 연금계약
> 순보험료(2차년도 이후는 연금계약 적립액으로 부른다)를 공시이율(가입후 10년 이내에는
> 연복리 2.5%, 10년을 초과한 경우에는 연복리 1.5%를 최저보증)로 적용하여 산출한 운용수익으로
> 만기보험금(일시납보험료 상당액) 지급을 위해 일정액을 충당하고 잔여액은 생존연금으로
> 지급된다. 공시이율이 높은 경우에는 만기보험금 지급을 위한 충당액이 적게 설정되어
> 상대적으로 고액의 생존연금이 지급될 수 있지만, 공시이율이 하락할 경우에는 만기보험금
> 지급을 위해 유보하여야 할 금액이 커지게 되므로 생존연금이 줄어들 수 있다.

**The committee's reasoning** [R1 §3], in three moves:

1. *Objective construction.* 「약관의 내용은 개개 계약체결자의 의사나 구체적 사정을 고려함이
   없이 평균적 고객의 이해가능성을 기준으로 하여 객관적·획일적으로 해석하여야 한다.」 On
   that basis 「연금계약 적립액에 공시이율을 적용하여 지급되는 생존연금이 변동되거나 줄어들
   수 있다는 정도까지는 비교적 명확하게 나타나 있으나, 그 줄어드는 정도가 약관에 명기한
   최저보증이율을 하회하는 것이 가능하다는 결론은 도출해 낼 수 없다.」
2. *The status of the 산출방법서.* 「약관이 보험계약자를 향하고 있는데 비하여 산출방법서는
   보험회사 내부의 계리적 서류에 지나지 않는 것으로 보험회사가 보험감독당국으로부터 감독이나
   명령 등을 받는 공법관계의 근거가 될 뿐이다. 따라서 원칙적으로 보험계약자를 구속하는 등
   사법(私法)관계인 보험계약관계에 적용될 수는 없다.」 It may be incorporated only where (i)
   a pointer clause specifies the content, (ii) the content concerns rights and duties, and
   (iii) the insurer has discharged its duty of explanation. Here 주6 incorporated **only**
   the calculation of the 연금계약 적립액, not the 연금연액 formula: 「그 외 피신청인 주장의
   근거로 제시하고 있는 산출방법서상의 '연금연액에 관한 사항' 등 여타 수식은 약관의
   지시조항 등을 통해 약관으로 편입된 바 없고 … 따라서 피신청인의 주장은 약관상 근거가 없는
   것이다.」
3. *Duty of explanation.* Even if incorporated, the insurer had not shown it explained the
   core of the mechanism, citing 상법 제638조의3, 약관규제법 제3조 제4항, and 대법원 2015.
   11. 17. 선고 **2014다81542** 판결 — 「연금보험계약의 체결에 있어 보험자 등은 보험계약자
   등에게 수학식에 의한 복잡한 연금계산방법 자체를 설명하지는 못한다고 하더라도, 대략적인
   연금액과 함께 그것이 변동될 수 있는 것이면 그 변동 가능성에 대하여 설명하여야 한다.」

**주문** [R1]: 「피신청인은 신청인에게 연금계약적립액에 공시이율(계약 후 10년 이내는 연복리
2.5%, 10년 초과 기간은 1.5%를 최저보증)을 곱하여 산출한 수익을 생존연금으로 지급하라.
* 최초의 연금계약 적립액은 순보험료(납입한 보험료 총액에서 보장계약 보험료 및 사업비를
차감한 금액)」 — i.e. interest on the fund with **no** retention, but on the fund net of
expenses, so the applicant's ₩2,080,000 claim was not granted in full either.

### 16. The supervisor's structural exposition and the 약관 amendment

[R2] is the FSS's own restatement, and it is the cleanest specification of the liability
anywhere:

> 만기환급형 즉시연금은 보험계약자가 낸 보험료*에 일정한 이율**을 곱하여 산출한 금액 중에서
> … 만기보험금 지급을 위한 재원(이하 '만기보험금지급재원')을 공제한 금액을 매월 연금으로
> 지급하는 구조
> \* 보험설계사에게 지급되는 수당 및 위험 보장을 위한 보험료 등을 제외한 순보험료
> \*\* Max [공시이율, 최저보증이율]

with the worked example 「보험료 1억원을 일시에 납입하여 가입한 경우(사업비와 위험보험료가
6백만원이라고 가정)」 and the ledger ⓐ (annuity) + ⓑ (maturity funding) = ⓒ (interest on the
fund), ⓓ (the fund itself), maturity benefit = ⓑ accumulated + ⓓ.

**The 약관 amendment made in January 2018** [R2 §4], printed side by side:

| 개정 전 | 개정 후 |
|---|---|
| 연금계약의 적립액을 기준으로 계산한 연금월액 | 연금계약의 연금재원을 기준으로 **만기보험금 지급을 위한 재원을 제외하여** 계산한 연금월액 |

with the footnote that the pre-amendment wording had been 「만기보험금을 지급하지 않는
즉시연금 약관(순수종신연금형의 기본형, 부부형)과 동일하게 사용」 — the drafting error was
that the same sentence had been reused for a product where it did not fit.

**The same repair, six years later, in a live 약관**: 「「연금개시시의 계약자적립액을 기준으로
공시이율에 의해 계산한 이자 상당액」에서 소정의 사업비를 차감하여 매년 보험계약 해당일에
지급」 [S7 별표1]. The current market therefore states the deduction on the face of the
contract. That is the disclosure state a 2026 reference product should model.

### 17. The arithmetic of the maturity-refund deduction — reproduced

All of this section is `[derived]`, from the figures at [R1], [R2] and [S3].

**Model.** Let `P` be the single premium, `k` the total one-off load, `V0 = P(1 − k)` the
opening fund, `i` the credited rate, `i_m = (1+i)^(1/12) − 1`, `N = 12n` the number of
monthly payments in advance, and `A` the level monthly annuity. The 만기환급형 condition is
that the fund grows from `V0` to `P` over the term while paying `A` each month:

```
A = ( V0 (1+i_m)^N  −  P ) / s(N)          where  s(N) = ((1+i_m)^N − 1) / i_m
```

**Test 1 — the disputed contract.** `P = ₩1,000,000,000`, `n = 10`, `i = 4.5%` (the declared
rate at inception [R1]). Published first-year annuity: **약 305만원**.

| Assumed load `k` | Opening fund `V0` | Model `A` |
|---|---|---|
| 5.325% (사업비 alone) | ₩946,750,000 | ₩3,125,248 (312.5만원) |
| 6.000% (the FSS assumption [R2]) | ₩940,000,000 | ₩3,055,585 (305.6만원) |
| 6.054% (solved) | ₩939,460,000 | ₩3,050,000 (305.0만원) |
| 6.500% | ₩935,000,000 | ₩3,003,983 (300.4만원) |

The load that reproduces the published annuity exactly is **6.054%**, i.e. 사업비 5.325%
[R1] plus a 보장계약 보험료 of about **0.73%** for a death benefit of 10% of premiums over
ten years — a figure the determination does not state, and which this reconstruction
recovers. The supervisor's round 6% assumption [R2] is vindicated to two significant figures.

**Test 2 — what the applicant was arguing about.** On the same contract at the guaranteed
floor of 2.5%:

- the annuity actually payable under the product design: **₩1,489,337 / month**;
- the annuity under the determination's 주문 (interest on the net fund, no retention):
  **₩1,957,083 / month**, a **31.4% uplift**;
- the applicant's own claim (interest on the *gross* premium): ₩2,083,333 / month.

So the determination sat between the two positions, and the gap it closed is worth about a
third of the annuity.

**Test 3 — the parallel 가입설계서** at [R1 fn.3], which quotes 617 at 4.7% and 279 at 2.5%
for a 상속연금형 10년만기 without stating the premium. Solving the same recursion at
`k = 6.06%`:

| Assumed `P` | model at 4.7% | model at 2.5% |
|---|---|---|
| 18.0억 | 577만원 | 268만원 |
| **18.7억** | **599만원** | **279만원** |
| 19.0억 | 609만원 | 283만원 |
| 20.0억 | 641만원 | 298만원 |

A premium of about **₩1,870,000,000** reproduces the guaranteed-basis figure exactly and the
declared-rate figure to within 3%. The design illustration is therefore internally
consistent with the same mechanism.

**Test 4 — the 교보 illustration at [S3]**, `P = ₩100,000,000`, `i = 2.52%`:

| Term | model at `k` = 3.91% | published [S3] |
|---|---|---|
| 10년 | 17.1만원 | 17만원 |
| 15년 | 18.2만원 | 18만원 |
| 20년 | 18.7만원 | 18만원 |
| 30년 | 19.2만원 | 18만원 |

and, for the 상속연금형 종신형 (no maturity benefit to fund), the pure interest-only figure
is 19.9만원 against a published 19만원 — the ~5% shortfall being the risk premium for the
₩10,000,000 death benefit and the 0.8% annuity-management charge [S1].

**Test 5 — 동양생명 [S4]** at 2.95%, `k` = 3.5%: 10년만기 model 20.9만원 vs published
19만원; 20년만기 model 22.3만원 vs published 21만원. Consistent to within about 6%, the
residual again being risk premium and management charge.

**Conclusion for the model.** The 상속연금형 만기형 annuity is *not* `V × i`. It is
`V × i − (maturity funding)`, and the funding term rises as `i` falls, which is why the
applicant's annuity fell 55% while the floor never moved. `Immediate_KR_S` must implement
the deduction as an explicit term with a switch, because the whole legal history of the
product is about whether that term is part of the contract.

### 18. 비과세 — the tax exemption and how it shapes the product

- **The enabling provision.** Interest income includes the 보험차익 of a savings contract
  prescribed by decree, **except** (가) a contract of ten years or more meeting the decree's
  conditions and (나) 「대통령령으로 정하는 요건을 갖춘 종신형 연금보험」 [R10, 소득세법
  제16조 제1항 제9호].
- **Route 1 — the ten-year rule** [R9, 시행령 제25조 제3항 제1호]. Premium caps: ₩200,000,000
  for contracts to 2017-03-31, **₩100,000,000 from 2017-04-01**. And, verbatim, the
  carve-out that matters most here: 「다만, 최초로 보험료를 납입한 날 … 부터 만기일 또는
  중도해지일까지의 기간은 **10년 이상**이지만 납입한 보험료를 최초납입일부터 **10년이
  경과하기 전에** 확정된 기간 동안 연금형태로 분할하여 지급받는 경우는 제외한다.」 A
  ten-year 확정기간연금형 즉시연금 therefore fails route 1, because it pays the premium out
  in instalments inside ten years. [R12 §III-1 각주4] states the same conclusion.
- **Route 2 — 월적립식** [R9, 제25조 제3항 제2호]: five years' payment, ten years' duration,
  level monthly premiums, ₩1,500,000 a month per person from 2017-04-01. Irrelevant to a
  single premium; recorded for completeness.
- **Route 3 — 종신형 연금보험** [R9, 제25조 제4항], and this is the route a 종신연금형
  즉시연금 uses. Verbatim, the chapeau and the five conditions:

  > ④ 법 제16조제1항제9호나목에서 "대통령령으로 정하는 요건을 갖춘 종신형 연금보험"이란
  > 보험계약 … 체결시점부터 다음 각 호의 요건을 모두 갖춘 종신형 연금보험을 말한다.
  > <신설 2017. 2. 3., 2025. 2. 28., 2025. 10. 1.>
  > 1. 계약자가 보험료 납입 계약기간 만료 후 **55세 이후부터 사망시까지** 보험금ㆍ수익 등을
  >    연금으로 지급받을 것
  > 2. 연금 외의 형태로 보험금ㆍ수익 등을 지급하지 아니할 것
  > 3. 사망시[「통계법」 제18조에 따라 국가데이터처장이 승인하여 고시하는 통계표에 따른
  >    성별ㆍ연령별 기대여명 연수(소수점 이하는 버리며, 이하 이 조에서 "기대여명연수"라
  >    한다) 이내에서 보험금ㆍ수익 등을 연금으로 지급하기로 보증한 기간(이하 이 조에서
  >    "보증기간"이라 한다)이 설정된 경우로서 계약자가 해당 보증기간 이내에 사망한 경우에는
  >    해당 보증기간의 종료시를 말한다] 보험계약 및 연금재원이 소멸할 것
  > 4. 계약자와 피보험자 및 수익자가 동일하고 최초 연금지급개시 이후 중도해지 불가
  > 5. 매년 수령하는 연금액[연금수령 개시 후에 금리변동에 따라 변동된 금액과 이연(移延)하여
  >    수령하는 연금액은 포함하지 아니한다]이 다음의 계산식에 따라 계산한 금액을 초과하지
  >    아니할 것

  The 제5호 계산식 is typeset as an image on every mirror tried. One retrieval rendered it as
  「연금수령 개시일 현재 연금계좌 평가액 ÷ 기대여명연수」; whether a multiplier (commonly
  stated as ×3) applies could not be confirmed and is **`[unverified]`**.
- **The product design is the statute.** Condition 3 is why 삼성's maximum 보증지급횟수 is
  bounded and why the middle option *is* the 기대여명 [S5 주4–주5]; why 한화, 푸본현대 and
  하나 all offer a 「기대여명」 guarantee at all [S7] [S8] [S13]; and why 한화's 약관
  defines 기대여명 by reference to 통계법 제18조 and warns 「기대여명이 5년 미만일 경우
  기대여명은 5년으로 하며, 이 경우에는 관련 세제혜택이 제한될 수 있습니다」 [S7 제2조 제6호
  가목]. Condition 4 is why 종신연금형 cannot be surrendered after annuitisation — a
  contractual term written to satisfy a tax condition, not (only) to prevent anti-selection.
- The plain-language restatement by the state [R11]: annuitisation at 55 or later, no
  lump-sum option, and a guarantee period not exceeding life expectancy.
- **A carrier's own summary** ties condition 4 to the contract: 「순수종신연금형을 선택한
  경우, 연금지급이 개시된 이후 해지 불가」 [S5 주2]; 「종신연금형(정액형, 집중보장형)의 경우
  연금지급개시 이후에는 계약을 해지할 수 없습니다」 [S3]; 「계약자는 계약이 소멸하기 전에
  언제든지 계약을 해지할 수 있으며(다만, **종신연금이 지급개시된 이후에는 해지할 수
  없습니다**)」 [S7 제31조] and, word for word, [S8 제33조].
- **Anti-selection is the other reason.** 「종신형에서는 연금지급이 개시된 후 해지를 허용하지
  않는다. 이는 사망률이 높은 계약자가 해지함으로써 발생할 수 있는 역선택 위험을 방지하기
  위한 장치이다」 [R12 §III-1].
- **The tax exemption applies only to some shapes.** 「즉시연금의 세제혜택은 비과세 혜택과
  상속세 절세이다. 즉시연금의 비과세 혜택은 종신형에 대해서만 적용된다」 [R12 §III-1] — but
  the same paragraph adds 「보험기간이 종신인 상속형 가입자는 비과세 혜택을 받을 수 있으며,
  금융소득이 4천만 원을 초과하면 종합과세 대상에서 제외된다」, i.e. a whole-of-life 상속형
  qualified on the pre-2013 ten-year route. [R12] is a 2012 paper and its tax statements
  predate the 2013 and 2017 amendments; treat them as historical.
- The universal carrier formula is deliberately vague: 「관련세법에서 정하는 요건에 부합하는
  경우에 보험차익 비과세 혜택이 가능합니다」 [S2] [S3] [S4] [S5]. No retrieved carrier
  document asserts the exemption unconditionally.

### 19. 상속세 — the estate-tax treatment

- 상속세 및 증여세법 제8조 makes a death benefit received on the deceased's death part of the
  estate [R26]. The article text itself was **not** retrieved (CaseNote returned HTTP 503);
  the statement rests on the tax trade report.
- 국세청 예규 **상증 사전-2019-법령해석재산-0378 (법령해석과-183), 2021-01-19**: where an
  즉시연금 in payment falls into an estate, it is valued at 「상속개시 당시 해지환급금
  상당액」 [R26]. Annuities received *before* death are separately assessable to gift tax on
  the 유기정기금 basis in 상속세 및 증여세법 시행령 제62조.
- The competing rule reported elsewhere is that the **higher** of the 정기금 valuation and
  the surrender value is used [R29], and search results indicate that 시행령 제62조's
  discount rate was cut from 6.5% to **3%** in the 2016 tax amendment. Neither the article
  nor the amendment was retrieved: **both are `[unverified]`**.
- This is why the shape exists at all. 「상속연금형(만기형)을 선택하시면 만기에 수령하는
  만기보험금을 상속 및 상속세 재원으로 활용할 수 있습니다」 [S4]; 「연금을 수령하면서
  상속세 납부재원을 마련할 수 있는 방법을 제시해드립니다. (상속연금형 선택시)」 [S5]; and
  [R12 §III-1] 「상속형 가입 후 계약자가 사망하면 계약자를 피상속인으로 변경해 세대 간
  연금을 이전시킬 수 있고, 중도해지하면 상속세 재원으로 활용할 수 있어 자산관리의 효율성
  측면에서 활용 여지가 크다」, with 「상속시킨 원금에 대해서는 금융재산 상속공제에 따라
  2억 원까지 상속세가 면제된다」.

### 20. Annuitant mortality — 연금사망률 / 개인연금사망률

- **What the factor uses.** Only 종신연금형 uses mortality [R12 §III-1]; the 확정 and 상속
  shapes do not. The 약관 words it as 「산출방법서에서 정한 방법에 따라 연금액을 분할 계산」
  [S7], with the mortality named separately in the ratchet clause.
- **The published rates.** [S1 §IV-2] is the only 즉시연금 document retrieved that prints
  actual annuitant rates. 「적용위험률 … ※ 개인연금사망률의 경우 가입나이 50세 기준입니다.」

  | 기준나이 | 남자 | 여자 | M/F ratio `[derived]` |
  |---|---|---|---|
  | 50세 | 0.00225 | 0.00097 | 2.32 |
  | 60세 | 0.00353 | 0.00118 | 2.99 |
  | 70세 | 0.00728 | 0.00251 | 2.90 |

- `[derived]` gradient: q70/q50 = **3.24 for men and 2.59 for women**, i.e. a constant-force
  ageing gradient of about **5.97% p.a. for men and 4.86% p.a. for women** over ages 50–70.
- `[derived]` comparison with the annuitant rates published in the sister file for
  `Pension_KR_S` (ABL: 남 0.00150 / 여 0.00052 at 60; 우체국: 남 0.00164 / 여 0.00056 at 60):
  the 하나생명 즉시연금 rate at 60 is **2.2× the ABL rate for men and 2.3× for women**. The
  two are not the same table. A plausible reading is that the 즉시연금 table is loaded on the
  *mortality* side because the contract also carries a death benefit of 10% of premiums,
  while a pure deferred-annuity table is loaded on the *survival* side — but no retrieved
  document says so and the comparison is `[unverified]` as an explanation. The **numbers**
  are sourced; the reason is not.
- **The naming varies** and matters when reading a 약관: 「개인연금사망률」 [S1],
  「연금사망률」 [S7] [S8], 「연금생명표」 [S6 §10-라].
- **The ratchet clause**, present on every retrieved carrier, verbatim in three forms:
  - 「종신연금형의 경우 연금지급 개시전에 연금사망율의 개정 등에 따라 연금액이 증가하게
    되는 경우에는 연금개시 당시의 연금사망율 및 적립액을 기준으로 산출한 연금액을 지급하여
    드립니다」 [S3];
  - 「종신연금형의 경우 연금지급 개시전 연금사망률의 개정 등에 따라 연금액이 증가하게 되는
    경우 연금개시 당시의 연금사망률 및 계약자적립액을 기준으로 산출한 연금액을 지급합니다」
    [S7 별표1 주9];
  - 「거치형에 한하여, 종신연금형의 경우 연금개시전에 연금생명표의 개정 등에 따라 연금액이
    증가하게 되는 경우에는 연금개시시점의 연금생명표 및 연금계약 계약자적립금을 기준으로
    산출한 연금액을 지급하며, 이 경우 회사는 연금개시 3개월전까지 연금액 변동내역 및
    연금지급형태 선택방법 등을 안내한다」 [S6 §10-라];
  - and the generic form 「종신연금형과 같이 연금사망률에 따라 연금액이 달라지는
    연금지급형태는 …」 [S8 주15].
- **The ratchet is inert on an 즉시형.** [S6] confines it expressly to the 거치형, and on an
  immediate annuity there is no interval between issue and annuitisation for a revision to
  land in. `Immediate_KR_S` therefore fixes the annuitant basis at issue and needs no
  ratchet logic; the sister deferred model does. `[derived from [S6 §10-라]]`
- **The 경험생명표 is not public.** No qx-by-age table for the 제10회 was located in this
  session, and the house position stated in the brief holds: every `mort_table.csv` in krlib
  is a `[std]` construction anchored on published summary statistics plus the carrier-published
  annuitant rates above.

### 21. 제10회 경험생명표 and its effect on annuities

- Produced by 보험개발원; the **제10회** applied from **2024년 4월**, five years after the
  제9회 [R13] [R14] [R15].
- 평균수명: **남 86.3세, 여 90.7세**, up **2.8** and **2.2** years on the 제9회 [R13] [R14].
  (One outlet's headline gives 남성 86.7세; that figure was seen only in a search snippet and
  is **`[unverified]`** — 86.3 is used, being carried by two retrieved articles.)
- **65세 기대여명: 남 23.7년, 여 27.1년**, up **2.3** and **1.9** years [R14]. This is the
  figure a life-annuity factor actually responds to.
- Effect on an annuity, on a fixed ₩200,000,000 fund annuitising at 60 [R13]:

  | 경험생명표 | 수령 종료 연령 | 수령 기간 | 월 수령액 |
  |---|---|---|---|
  | 6차 | 78.4세 | 18.4년 | 90.6만원 |
  | 9차 | 85.3세 | — | 70.9만원 |
  | 10차 | 86.3세 | 26.3년 | "60만원 후반" |

  The 9차 → 10차 fall is headlined at about **15%** [R13].
- Direction of effect by line [R14] [R15]: 종신보험 premiums down, 정기보험 down,
  암·건강보험 up, 연금보험 premiums up for a given annuity — the last being the same
  statement as "the annuity falls for a given fund".
- **In-force contracts are unaffected**: 「기가입자는 보험료 변동 영향을 받지 않는다」 [R14].
  For an 즉시연금 in payment this is unambiguous, because the factor was fixed the month the
  premium was paid.

### 22. Surrender, and the asymmetry between shapes

- **종신연금형: no surrender after annuitisation.** [S3] [S5 주2] [S7 제31조] [S8 제33조],
  quoted at §18 above. On an 즉시연금 the annuity starts one month after inception, so this
  amounts to: **the contract is irreversible from month one**.
- **상속연금형 and 확정기간연금형 remain surrenderable throughout** [S1] [S3] [S6].
- **Surrender values are computed on the fund, and the deduction is nil.** 「우리
  하나생명보험회사는 보험료 계산시 적용한 위험률로 산출한 순보험료식 책임준비금에서
  해지공제액을 공제한 금액을 해지환급금으로 지급합니다」 [S1 §VI-1], with the 해지공제액
  table showing **0 at every duration** [S1 §VIII]. [S10] independently confirms that the
  carrier's three 즉시연금 products carry no 중도해지율.
- **The published surrender-value illustration** [S1 §VI-2], basis 정기상속연금형 (20년지급),
  가입나이 60세, 일시납보험료 ₩50,000,000, 최저보증이율 basis (1.5% / 1.0%), 남자:

  | 경과기간 | 해지환급금 | 환급률 |
  |---|---|---|
  | 3개월 | ₩48,281,616 | 96.6% |
  | 1년 | ₩48,358,082 | 96.7% |
  | 3년 | ₩48,566,495 | 97.1% |
  | 5년 | ₩48,776,782 | 97.6% |
  | 7년 | ₩48,985,946 | 98.0% |
  | 10년 | ₩49,289,993 | 98.6% |
  | 15년 | ₩49,748,341 | 99.5% |
  | 20년 | ₩50,000,000 | 100.0% |

  with the female column 0.0–0.3 pp lower at every duration and identical at 20 years. On the
  **Min[평균공시이율 3.0%, 공시이율 2.50%]** basis the same rows run 96.6% → 98.5% → 100.0%.
  Note the shape: this is a 만기형, so the fund *rises* toward the premium and the surrender
  value converges on ₩50,000,000 exactly at maturity — the deduction mechanism visible from
  the other side.
- The 삼성 illustration on 상속연금형 10년만기 [S5], 여자 40세, ₩100,000,000, shows the same
  convergence on the 1종 (즉시) basis — 96.0% at 1 year, 96.8% at 3, 97.7% at 5, 98.5% at 7,
  100.0% at 10 — but on the 2종 (5-year deferral) basis the ratio **overshoots**, reaching
  108.2% at 5 years before falling back to exactly 100.0% at maturity, because the fund
  accumulates for five years before the annuity starts drawing it down.
- **A surrender after annuitisation needs the beneficiary's consent**: 「제1항에 따라
  연금지급개시 이후에 계약을 해지하는 경우에는 보험수익자의 동의를 얻어야 합니다」 [S8
  제33조 제2항].
- **위법계약의 해지** under 금융소비자 보호에 관한 법률 제47조 returns the **계약자적립액**
  rather than the surrender value: 「위법계약이 해지되는 경우 회사가 적립한 해지 당시의
  계약자적립액을 반환하여 드립니다」 [S7 제34조 제5항]. On a product with nil surrender
  deduction the two coincide, but the distinction is real on other krlib products.

### 23. Death benefits

| Shape | Before annuitisation | After annuitisation | Source |
|---|---|---|---|
| 종신연금형 (교보) | 사망당시의 연금계약 책임준비금 + 1,000만원 (기본보험료의 10%) | unpaid guaranteed instalments only | [S3] |
| 종신연금형 (삼성, 순수종신) | 거치형만: 사망보험금 후 계약 소멸 | 「별도의 사망보험금은 지급되지 않습니다」 | [S5] |
| 상속연금형 (교보) | 책임준비금 + 1,000만원 | 책임준비금 + 1,000만원 | [S3] |
| 상속연금형 (하나, 종신) | — | 기본보험료의 10% **plus** 사망 당시 연금계약 적립액 | [S1] |
| 상속연금형 (하나, 정기) | — | 기본보험료의 10% plus 적립액; 만기 시 만기보험금 | [S1] |
| 상속연금형 (한화, 2024) | — | 「피보험자 사망시에는 사망시점 계약자적립액 지급」 | [S7 별표1] |
| 확정기간연금형 (교보) | 책임준비금 + 1,000만원 | 1,000만원 plus the remaining instalments | [S3] |
| 거치 phase (한화, 2024) | Max[이미 납입한 보험료, 사망당시의 계약자적립액] | — | [S7 제24조 제2항] |
| The disputed contract | — | 「이미 납입한 보험료의 10% + 사망 당시 연금계약적립액」 | [R1 별표1(2)] |

- **The 10%-of-premium death benefit is the near-universal Korean design** on 즉시연금: it
  appears at 교보 [S2] [S3], 하나 [S1], 동양 (implicitly, via the same architecture) and in
  the disputed contract [R1]. It is small enough not to disturb the annuity and large enough
  to make the contract an insurance contract.
- **Exclusions**: 「고의적 사고 또는 2년 이내의 자살의 경우 사망보험금 지급이 제한될 수
  있습니다」 [S3]; the 약관 form is 「피보험자가 고의로 자신을 해친 경우 … 다만, 피보험자가
  심신상실 등으로 자유로운 의사결정을 할 수 없는 상태에서 자신을 해침으로 인하여 보험금
  지급사유가 발생한 때에는 보험금을 지급합니다」 [S7 제6조]. The suicide exclusion period
  is **two years**, not three as in Japan [S4] [S3].
- **사기에 의한 계약**: cancellable within five years of the 보장개시일 (one month from
  discovery) [S1 §III-3-다] [S7 제17조].
- **계약 전 알릴 의무 위반**: the insurer may cancel within two years of the 보장개시일 (one
  year for disease on a 진단계약), or one month from discovery, or not at all after three
  years from conclusion [S1] [S7 제16조].
- **Underwriting is light but not absent**: 「기존 다른 보험상품의 가입유무, 나이, 청약서의
  계약 전 알릴 의무사항에 따라 건강진단을 시행할 수 있으며, 그 결과에 따라 보험가입
  가능여부를 판정할 수 있습니다」 [S1 §II-6], and 표준하체인수특약 is offered as a 제도성특약
  [S1 §III-1].

### 24. Commutation, instalment frequency, and the deferral of instalments

- **Commutation of the unpaid guaranteed instalments is available on every retrieved
  product**, both on death and — importantly — **on survival**:
  - 「종신연금형의 보증지급기간 안에 보험수익자가 신청한 경우 잔여보증지급기간의 전부 또는
    일부(연단위)에 해당하는 연금액을 보험료 및 책임준비금 산출방법서에 따라 공시이율로
    할인하여 선지급 할 수 있습니다.(연 1회)」 [S3] — note the annual limit and the
    year-granularity;
  - 「보험수익자는 종신연금형의 경우 보증지급기간(10년, 20년, 100세, 기대여명) 동안의
    지급되지 않은 연금액, 확정기간연금형의 경우 연금지급기간(10년, 15년, 20년) 동안의
    지급되지 않은 연금액을 산출방법서에 따라 공시이율로 할인하여 일시금으로 선지급 받을 수
    있으며, 피보험자가 사망한 경우 또한 같습니다」 [S7 제11조 제3항, 별표1 주7];
  - 「순수종신연금형의 경우 보험수익자는 생존연금 지급개시 후 보증지급횟수까지의 지급되지
    않은 생존연금을 계약자의 동의를 얻어 산출방법서에 따라 공시이율로 할인하여 일시금으로
    선지급 받을 수 있음」 [S5 주8];
  - and one carrier allows a whole policy year's twelve instalments to be taken in advance:
    「해당 보험년도의 연금월액(12회분)을 선지급받기를 원하는 경우 회사는 … 공시이율로
    할인하여 일시금으로 선지급 받을 수 있음」 [S5 주9].
- **The discount rate for commutation is the 공시이율**, uniformly [S1 주4] [S3] [S5] [S7]
  [S9]. No retrieved document uses a separate commutation rate.
- **Instalment frequency.** The 연금연액 may be split monthly, quarterly or half-yearly, with
  interest on the deferred portions: 「연금을 매월, 3개월, 6개월로 분할하여 지급하는 경우
  신공시이율로 계산한 이자를 가산합니다」 [S9 주11]; 「연금액을 매월, 3개월, 6개월로
  분할하여 지급할 경우에는 "보험료 및 책임준비금 산출방법서"에 따라 공시이율로 적립한 금액을
  지급합니다」 [S8 주14]. On 즉시연금 the monthly frequency is the default and often the only
  one offered [S1 주1] [S3].
- **Annual vs monthly.** [S1 주1] gives both: 연단위 pays from the first policy anniversary,
  월단위 from one month after the 보장개시일. `Immediate_KR_S` is an **annual-grid** model
  per the library's product table, so it projects the 연금연액 and treats the monthly split
  as a presentational sub-division; the technical notes must say so.

### 25. 보험나이 — insurance age

- Verbatim from a current 약관 [S7 제23조]:

  > ① 이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다.
  > ② 제1항의 보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는
  > 버리고 6개월 이상의 끝수는 1년으로 하여 계산하며, 이후 매년 계약 해당일에 나이가 증가하는
  > 것으로 합니다.
  > 【보험나이 계산 예시】 생년월일 : 1988년 10월 2일, 현재(계약일) : 2018년 4월 13일
  > ⇒ 2018년 4월 13일 − 1988년 10월 2일 = 29년 6월 11일 = 30세

- So 보험나이 is age nearest birthday computed on a six-month rule, and it differs from 만나이
  for half of all issue dates. The model and the registry metadata must state which is used;
  for `Immediate_KR_S` the pricing age is **보험나이** and any population statistic quoted
  against it is 만나이.
- 「청약서류상 피보험자의 나이 또는 성별에 관한 기재사항이 신분증에 기재된 사실과 다른
  경우에는 신분증에 기재된 나이 또는 성별로 정정하고, 정정된 나이 또는 성별에 해당하는
  보험금 및 보험료로 변경합니다」 [S7 제23조 제3항] — a misstatement-of-age clause that
  adjusts benefits rather than voiding.
- Age outside the permitted range voids the contract, with a saving: 「계약을 체결할 때
  계약에서 정한 피보험자의 나이에 미달되었거나 초과되었을 경우(다만, 회사가 나이의 착오를
  발견하였을 때 이미 계약나이에 도달한 경우에는 유효한 계약으로 봅니다)에는 계약을 무효로
  하며, 계약자에게 이미 납입한 보험료 … 를 돌려 드립니다」 [S7 제21조].

### 26. Issue-age, premium and size envelopes

| Carrier / product | 가입나이 (즉시) | 연금개시나이 | Premium range | Unit | Source |
|---|---|---|---|---|---|
| 하나 행복knowhow즉시연금 | 45–80세 | 45–80세 | 종신형 4,000만원 ~ 100억원; 상속형 4,000만원 ~ 50억/30억/15억 by age band | 100만원 | [S1] |
| 교보 바로받는연금보험 (both vintages) | 45–80세 (즉시); 40–80세 (거치) | 45–80세; 거치 = 가입나이+1 ~ +5 | 기본보험료 1,000만원 이상 | 100만원 | [S2] [S3] |
| 동양 Angel즉시연금 | 45–80세 (즉시); 만15세~(개시−1)세 (거치) | 45–80세 | 1,000만원 이상 | 100만원 | [S4] |
| 삼성 에이스즉시연금 B2.2 | 40–85세 (1종); 개시나이−(5~1)세 (2종) | — | 1,000만원 ~ 50억원 | 원 단위 | [S5] |
| ABL 알리안츠프리미어즉시연금 | 45–75세 (즉시); 만15세~(Y−1)세 (거치) | 45–75세 (부부계약 남자 주피보험자 최저 48세) | **5,000만원 이상** | — | [S6] |
| 우체국즉시연금보험 (2011) | 45–80세 | — | 500만원 ~ 2억 5,000만원 | — | [R27] |

- The **modal envelope is 45–80 and ₩10,000,000 minimum**; 삼성 opens at 40 and closes at 85,
  ABL demands ₩50,000,000, and the state provider caps at ₩250,000,000.
- [R12 §III-2-가] reports the market-wide position for 2008–2010: 「대부분의 생명보험회사들은
  즉시연금의 최저 가입금액을 1천만 원으로 제한하며, 가입연령도 45세~85세로 한정하고 있다」,
  and the sample's realised range was **45–85 with a minimum of ₩10,000,000 and a maximum of
  ₩4,000,000,000**.
- [R16] reports minimum premiums differing by carrier — 「M사는 1천만원, S사는 3천만원 등」.
- The 상속형 premium caps step **down** with age at 하나생명 (₩5bn / ₩3bn / ₩1.5bn for ages
  45–60 / 61–70 / 71–80) [S1 §II-5], which is an anti-selection and estate-planning control,
  not a mortality one.
- **추가납입 and 중도인출 are 거치형-only** on the immediate products [S2] [S3] [S5] [S6]. On
  an 즉시연금 there is no accumulation phase in which to pay more in or take money out. The
  single exception noted is 상속연금형 종신플랜, where partial withdrawal survives
  annuitisation [S6 §8-나].

### 27. Market size, buyer profile, and option choice

All from [R12] unless stated; the dataset is 1,414 contracts written by one insurer over
FY2008–FY2009 (2008-04-01 to 2010-03-31), said to be about 30% of the market's premium. It
is old, and it is the only such dataset that is public.

- **The market formed late**: 「즉시연금은 2007년 이후에야 시장이 형성되기 시작하였기
  때문」; as at January 2011, **16 of 23 life insurers** wrote it — 「즉시연금 수입보험료의
  시장집중도는 타 종목에 비해 매우 높은 특징을 보인다」.
- **The typical buyer is a woman in her late sixties.** 70% female; mean issue age 66.6,
  median 68 (range 45–85); mean premium **₩185,000,000**, median **₩100,000,000**, range
  ₩10,000,000 to ₩4,000,000,000 [R12 표2].

  | Statistic | Mean | Median | SD | Min | Max | n |
  |---|---|---|---|---|---|---|
  | Female share | 0.70 | 1.00 | 0.46 | 0 | 1 | 1,414 |
  | 가입연령 | 66.6 | 68.0 | 9.7 | 45.0 | 85.0 | 1,414 |
  | 보험료 (천원) | 185,000 | 100,000 | 262,000 | 10,000 | 4,000,000 | 1,414 |
  | 연금급여 월 (천원) | 1,170 | 613 | 1,839 | 55 | 24,400 | 373 |

- **Age distribution** [R12 표4]: 45–49 7%, 50–54 7%, 55–59 9%, 60–64 14%, 65–69 18%, 70–74
  22%, 75–79 15%, 80+ 7%. 63% are 65 or over; 44% are 70 or over.
- **Premium distribution by percentile** [R12 그림3], in 백만원: 1% 10, 5% 22, 10% 30, 25% 50,
  50% 100, 75% 200, 90% 488, 95% 500, 99% 1,000. **38.5% of contracts are ₩100,000,000 or
  more.**
- **Option choice — the central finding** [R12 표5]:

  | Option | By contract count | By premium |
  |---|---|---|
  | 종신형 | 18.2% | 18.6% |
  | 확정형 | 8.2% | 6.3% |
  | **상속형** | **73.6%** | **75.1%** |

  「종신형(72%) 즉시연금이 주류를 이루는 미국과 달리 우리나라는 상속형 중심으로 즉시연금에
  가입하고 있다.」 That is the single most important market fact in this file: the Korean
  immediate annuity is predominantly **not** a longevity product.
- **Mean issue age by option** [R12 §III-2-라]: 종신형 67.5, 확정형 65.1, 상속형 66.6. Mean
  premium: 종신형 ₩186,000,000, 상속형 ₩189,000,000, 확정형 ₩139,000,000.
- **Guarantee periods actually chosen** [R12 표7]: on 종신형, **97.3% chose 10 years** and
  2.7% chose 20, a mean of **10.3 years**; on 확정형, 10년 77.6%, 15년 13.8%, 20년 8.6%. The
  US comparator is a mean guarantee of 13 years.
- **Lifetime-coverage ratio** of the 확정형 buyers (payment term ÷ life expectancy) [R12 표8]:
  **47.5% overall**, 50.1% for men and 45.7% for women, rising with premium size from 40.4%
  (₩10–30m) to 50.4% (₩100m+). Half of a 확정형 buyer's expected remaining lifetime is
  uncovered.
- **Annuity by premium band** [R12 표9], 천원 per month, 종신형 and 확정형 only: mean 148 for
  ₩10–30m, 322 for ₩30–50m, 645 for ₩50–100m, 2,387 for ₩100m+; overall mean 1,170, median
  609.
- **No myopia in aggregate**: 「우리나라의 즉시연금 판매량은 주식시장 성과와는 관련성이 낮은
  것으로 나타났다」, unlike the US result of a 5.3 pp fall in sales per 1 pp of equity return
  [R12 요약, §II].
- **A current market-size figure for 즉시연금 specifically was not obtained.** The
  생명보험협회 statistical yearbook and 통계월보 do not break the line out in any page
  retrieved, and no aggregate for 2024–2026 could be sourced. See fetch failures.

### 28. 예금자보호 (policyholder protection)

- Every retrieved leaflet from 2016–2017 states the ₩50,000,000 limit: 「이 보험계약은
  예금자보호법에 따라 예금보험공사가 보호하되, 보호 한도는 본 보험회사에 있는 귀하의 모든
  예금보호대상 금융상품의 해지환급금(또는 만기보험금이나 사고보험금)에 기타지급금을 합하여
  1인당 "최고5천만원"이며, 5천만원을 초과하는 나머지 금액은 보호하지 않습니다. (다만,
  보험계약자와 보험료 납부자가 법인이면 보호되지 않습니다.)」 [S2] [S3] [S4] [S5]; the
  상품요약서 says the same [S1 §I].
- **The limit was raised to ₩100,000,000 with effect from 2025-09-01** [R30] — but neither
  FSC release was actually opened, so this is `[unverified]`.
- The point matters more here than anywhere else in krlib: the **median** 즉시연금 premium is
  ₩100,000,000 and 38.5% of contracts exceed it [R12], so the great majority of the money in
  this product sits **outside** the protection limit on either the old or the new figure.

### 29. Scope boundaries — what this file does not cover

- **The 거치형 (deferred) selling mode.** Several sources here are deferred contracts cited
  for payout-phase machinery only ([S7]–[S9], [S13], [S14]). Anything about premium payment,
  추가납입, 중도인출 before annuitisation or the accumulation of a fund over years belongs to
  `_research/pension-savings.md` and `Pension_KR_S`, not here.
- **변액즉시연금** (a separate-account immediate annuity). Not retrieved and not modelled;
  `VA_KR_S` covers separate-account business.
- **연금저축 즉시연금.** The tax-qualified wrapper cannot be written as a single-premium
  immediate annuity in any retrieved product, and the 연금수령한도 test would bite; see
  `_research/pension-savings.md`.
- **부부형 / 연생 (joint-life) annuities.** [S6] offers 부부계약 with a minimum annuity age
  of 48 for a male principal insured, and [S5] contemplates 부부형 in passing, but no
  retrieved document gives the joint-life mechanics or a factor. Anything beyond "one carrier
  offers it and raises the minimum age by three years for a male principal insured" is
  `[unverified]`.
- **IFRS 17 / K-ICS treatment.** The measurement of an immediate-annuity liability under
  K-IFRS 1117 and the longevity sub-module of K-ICS belong to
  `_research/regulatory-actuarial.md`; nothing here was retrieved on either.
- **Reinsurance, expense analysis and the 삼리원 decomposition.** No retrieved document
  discloses a 사차/이차/비차 split for this line.

---

## Variation across carriers

| Feature | 하나생명 [S1] [S10] | 교보생명 [S2] [S3] | 동양생명 [S4] | 삼성생명 [S5] | ABL/알리안츠 [S6] | 한화생명 [S7] (2024, 거치) | 우체국 [S9] (거치) |
|---|---|---|---|---|---|---|---|
| 종신 guarantee menu | 10년, 20년 | 10년/12년, 20년, 30년, 100세 | 10년, 20년, 30년 | rule-based: 10년 min / 기대여명 / (100−개시나이) max | 10년, 20년, 100세 | 10년, 20년, 100세, 기대여명 | 20년, 30년, 90세, 100세 |
| Front-loaded variant | none | 집중보장형 (100% uplift) | none | 브릿지연금형 (2×) | 소득보장형 | none in 별표1 | 조기집중연금형 (200%/300%, 5/10년) |
| 상속연금형 | 종신 + 정기 10/15/20년 | 종신 + 만기 10/15/20/30년 | 종신 + 만기 10/20년 | 종신 + 만기 10/15/20/30년 | 종신플랜 + 환급플랜 10/15/20년 | 종신 only | **none** |
| 확정기간연금형 | none | none (2016) / 10·15·20·30년 (2017) | none | none | 5/10/15/20/30년 | 10/15/20년 | 5/10/15/20/30년 |
| 가입나이 (즉시) | 45–80 | 45–80 | 45–80 | **40–85** | 45–75 | n/a | n/a |
| Minimum premium | 4,000만원 | 1,000만원 | 1,000만원 | 1,000만원 | **5,000만원** | n/a | n/a |
| 최저보증이율 (as sold) | 2.5%/2.0% → 1.5%/1.0% | 1.5%/1.0% → 1.25%/1.0%/0.75% | 2.0%/1.5%/1.0% | 1.5%/1.0% | 2.5%/2.0%/1.0% | **1.0%/0.75%/0.5%** | not extracted |
| 공시기준이율 weighting | prose only | not published | not published | not published | (내부+외부)/2, 80–120% band | prose only | not extracted |
| Death benefit | 기본보험료의 10% + 적립액 | 책임준비금 + 기본보험료의 10% | not extracted | 순수종신: none after annuitisation | not extracted | Max[납입보험료, 적립액] pre-annuitisation | 재해장해보험금 only |
| Commutation | yes, 공시이율 discount | yes, 연 1회, 연단위 | not extracted | yes, incl. a whole policy year in advance | not extracted | yes, on death or on request | yes |
| Fund floor at annuitisation | not stated | not stated | not stated | not stated | not stated | **100.1% of premiums** | **100.1% of premiums** |
| Distinctive feature | the only full **상품요약서**, with published 개인연금사망률 | the widest illustration table; 12년 → 10년 guarantee shift between vintages | 즉시 and 거치 on one model point | the tax statute written straight into the 보증지급횟수 rule | the only retrieved **사업방법서**, with the 공시이율 algebra and a size discount | the **post-dispute** 상속연금형 wording naming the deduction | a state provider with no 상속연금형 at all |

**What does not vary.** Every retrieved carrier: takes its whole expense load once, at
inception, and applies no surrender deduction thereafter; credits a monthly-reset 공시이율
with a duration-stepped floor; recalculates the annuity when the rate moves; forbids
surrender of a 종신연금형 once in payment; permits commutation of unpaid guaranteed
instalments at the 공시이율; offers the annuity monthly, quarterly or half-yearly with
interest on the deferred portion; charges 0.2% (capped at ₩2,000) for a withdrawal with four
free a year; and uses 보험나이 on the six-month rule.

**Most representative design for the reference implementation.** A single-premium immediate
annuity written at 보험나이 60 on an annual grid, with:

- three selectable payout shapes — **종신연금형** with a 10-year guarantee (the shape 97.3%
  of life-annuity buyers actually chose [R12 표7]), **상속연금형 만기형** over 10/15/20/30
  years, and **확정기간연금형** over 10/15/20/30 years;
- a single-premium load of about **3.5%** taken at inception, split 계약체결비용 2.2% /
  계약관리비용 1.3% [S1], with **no surrender deduction** at any duration [S1] [S10];
- a **0.8% of 연금연액** annual charge during payment [S1];
- a death benefit of **10% of the single premium** plus the fund, payable before annuitisation
  on the life shape and throughout on the inheritance shape [S1] [S3] [R1];
- a 공시이율 of about **2.5%** with a duration-stepped floor of **1.25% / 1.00% / 0.75%**
  [S3], both exposed as scalars because no carrier publishes a derivable rate;
- the 만기환급형 retention implemented **explicitly and switchably**, so both the as-designed
  liability and the 분조위 주문 liability can be projected [R1] [R2];
- annuitant mortality from the published 개인연금사망률 anchors at 50/60/70 [S1], as a
  `[std]` construction with a `provenance` column, used by the 종신연금형 alone;
- no surrender after annuitisation on the 종신연금형, and free surrender on the other two
  [S3] [S7 제31조].

---

## Fetch failures and gaps

**URLs tried that did not yield the content sought**

- `https://fine.fss.or.kr/main/cons_safe/pension/info.jsp` — the FSS's own 즉시연금
  분쟁조정신청 안내 page, announced at [R3 §2]. Returned the FSS error page
  (「페이지가 없거나 잘못된 경로 입니다」). **Lost:** the supervisor's consumer-facing FAQ
  and its case digest. Substituted by [R1] [R2] [R3], which are the underlying documents.
- `https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196` and
  `https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000250658&chrClsCd=010201` —
  보험업감독규정. Both returned navigation chrome only; the viewer is JS-rendered. **Lost:**
  the verbatim text of **제7-60조**, i.e. the five-year minimum guarantee period for a life
  annuity and the single-premium 15-month reserve test. Both are used below the line as
  `[unverified]` and are sourced only to [R12] and to search snippets.
- `https://www.ulex.co.kr/법률/2100000214154-21843-보험업감독` — a third-party mirror of the
  same regulation; **timed out at 60 s**.
- `https://www.fsc.go.kr/po040301/view?noticeId=3864` — FSC 규정변경예고 for a 2023 amendment
  to 제7-60조. The landing page returned metadata only (예고기간 2023-02-14 ~ 2023-03-27,
  보험과) and the text sits in an unretrieved `.hwp`.
- `https://www.fsc.go.kr/comm/getFile?srvcId=RULENOTICE&upperNo=4076&fileTy=ATTACH&fileNo=8`
  — expected to be 보험업감독규정; the bytes are a 72-page **규제영향분석서** dated
  2025-06-12 on unrelated topics. Recorded so the URL is not tried again.
- `https://casenote.kr/법령/상속세 및 증여세법/제8조`,
  `https://casenote.kr/대법원/2019다300934` and
  `https://casenote.kr/서울고등법원/2024나2013287` — all returned **HTTP 503**. CaseNote
  served 소득세법 제16조 and 대법원 2022다225897 successfully in the same session, so the
  503s are transient rather than structural. **Lost:** 상속세및증여세법 제8조 verbatim, the
  full text of the 2023 death-benefit judgment, and one appellate judgment.
- `https://www.hankyung.com/article/2022112300131` — HTTP **403**. **Lost:** the
  contemporaneous report of the November 2022 appellate reversal, including the sentence
  「산출방법서도 약관의 내용으로 봐야 한다」 which is quoted here only from a search snippet.
- `https://m.khan.co.kr/national/court-law/article/202107211640001` [R20] — HTTP **301** to
  the site root. **Lost:** the primary report of the 2021-07-21 first-instance judgment.
  The particulars in the chronology (서울중앙지방법원 민사합의25부, 57 plaintiffs,
  ₩598,000,000-odd) come from a search snippet and are marked accordingly.
- `https://www.fss.or.kr/fss/cmmn/file/fileDown.do?...atchFileId=94c114d0...&fileSn=1` — the
  PDF attached to [R3]. Downloaded (354 KB, 3 pp.) and extracted; **this one succeeded** and
  is the source for the two determination dates. Recorded here because the markdown fetcher
  reported it as unreadable and only the `pypdf` route worked.
- `https://image.kebhana.com/cont/download/insdocument/provide/08L03024328_agree.pdf` — the
  삼성 에이스즉시연금 **약관** (5.4 MB). Downloaded HTTP 200 but is a scan: the pages carry
  JPEG streams with no text layer, and `pypdf` returns nothing. **Lost:** the only chance in
  this session to read an 즉시연금 약관 for the very product whose leaflet is [S5]. No fact
  here is sourced to it.
- `https://www.hanalife.co.kr/anm/product/download.do?code=603620&seq=1` — reached from a
  search result promising an 즉시연금 약관; it is in fact 「무배당 넘버원 변액연금보험
  적립형/거치형 약관」, a variable annuity. Read and discarded. No fact is sourced to it.
- `https://lawinsider.com/ko/contracts/OtBCEVKd5H` — reached from a search result; it is
  「무배당 만원의행복보험」, a Korea Post accident-and-health product. Read and discarded.
- `https://www.ibki.co.kr/process/HP_DIRECTPENSION_PRODUCTINFO_03` — IBK연금보험 product
  page. The fetch returned content that does not correspond to an annuity product page (it
  described a retirement fund with a 4.2% rate and age-indexed projections). Treated as an
  unusable retrieval; **no fact is sourced to it**, and the IBK figures used here come from
  the bank's own page [S14] instead.
- `https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do?MENU_ID1=DF_GDAR000`
  — 한화생명 공시실 적용이율. Returned the disclosure system's explanatory shell; the rate
  tables are behind a JS query. **Lost:** a current per-product 공시이율 table from a large
  carrier. Substituted by [S12] and [S14].
- `https://journal.kci.go.kr/kiri/archive/articlePdf?artiId=ART001773859` — a companion 2013
  KIRI paper on payout-option choice in tax-qualified annuities. **Not attempted** after
  [R12] proved sufficient; recorded as a known unexploited source.
- `https://kiss.kstudy.com/Detail/Ar?key=3937801` — 「즉시연금의 공시이율 결정요인」,
  리스크 관리연구. **Not attempted**; the host is a paywalled aggregator. This is the one
  academic paper that would directly test the 공시이율-setting model at §8.
- `https://www.epostlife.go.kr/ASDSGD0101.do` and searches for a 우체국즉시연금보험
  상품요약서 PDF under `epostlife.go.kr/resources/js/biz/ip/gs/pdf/` — the file-naming
  pattern was found for 연금저축 and 연금보험 products but no 즉시연금 summary was located.
  **Lost:** the state provider's own 즉시연금 disclosure; only the 2011 launch release [R27]
  and the deferred 약관 [S9] were obtained.

**Claims left `[unverified]`, and why**

- **보험업감독규정 제7-60조 in any form.** The five-year minimum guarantee period for a life
  annuity rests solely on a citation in [R12]; the single-premium 15-month reserve test and
  the 2018-01-01 commencement for 생존연금 rest on search snippets. The regulation was not
  retrieved [R31]. Every statement about it in this file is `[unverified]` as to text, though
  the five-year rule is corroborated behaviourally by the absence of a life-only option from
  all eleven retrieved products.
- **The 계산식 in 소득세법 시행령 제25조 제4항 제5호.** The annual-annuity ceiling for a
  종신형 연금보험 is typeset as an image. One retrieval rendered it as 「연금수령 개시일
  현재 연금계좌 평가액 ÷ 기대여명연수」; a multiplier of 3 is widely asserted but was not
  confirmed. **Any downstream use of the ceiling must be `[unverified]` or `[std]`.**
- **상속세 및 증여세법 제8조 and 시행령 제62조.** The estate treatment at §19 rests on a tax
  trade report [R26] and a bank glossary [R29]. Neither statute nor the 예규 itself was
  retrieved. The 3% discount rate for 유기정기금 from the 2016 amendment is `[unverified]`.
- **The deposit-protection limit of ₩100,000,000 from 2025-09-01.** Search results are
  consistent and numerous but no FSC or KDIC document was opened [R30].
- **The number of affected policyholders and the amount at stake.** The figures used here —
  about 160,000 policyholders and ₩800bn–₩1tn industry-wide, 삼성 50,000–55,000 contracts and
  ₩400–430bn, 한화 ₩85bn, 교보 ₩70bn — come from four news reports [R17] [R18] [R19] [R24]
  and are mutually consistent to within about 10%, but **no supervisory document stating any
  of them was retrieved**. [R2] and [R3] give the mechanism and the determinations without a
  single aggregate figure.
- **The number of plaintiffs in the Supreme Court case.** [R21] says 57 (2022다308747,
  308754); [R22] and [R25] say 51. Both are reported of the same 2025-10-16 judgment day.
  The discrepancy is unresolved; both are recorded with their sources.
- **The 2022 appellate reasoning.** The sentence 「산출방법서도 약관의 내용으로 봐야 한다」
  is quoted in this file from a search snippet only, the 한국경제 article having returned 403
  and the 서울고등법원 judgment having returned 503.
- **평균수명 남 86.3세 vs 86.7세** on the 제10회. Two retrieved articles say 86.3 [R13] [R14];
  a third outlet's headline, seen only as a search result, says 86.7. 86.3 is used.
- **The 제10회 경험생명표 itself.** No qx table, and no 보험개발원 release, was retrieved. All
  mortality statements rest on carrier disclosures [S1] and on secondary reporting [R13]
  [R14] [R15].
- **Why the 하나생명 개인연금사망률 is roughly twice the deferred-annuity rates published in
  the sister file.** The numbers are sourced on both sides; the explanation offered at §20 (a
  table loaded on the mortality side because the contract also carries a death benefit) is an
  inference and is `[unverified]`.
- **Current market size for 즉시연금.** No aggregate for new business or in-force in any year
  after FY2009 was located. 생명보험협회's yearbook pages were reached but their tables are
  behind a query interface, and no line-level breakout was found. The market picture at §27
  is therefore **fifteen to eighteen years old**, and the product-spec must say so wherever it
  relies on it. **This is the largest gap in the file.**
- **Whether 즉시연금 is still actively sold, and by whom.** Every 즉시연금-specific product
  document retrieved is from 2011–2017. The 2023–2026 sources ([S7], [S13], [S14]) are
  deferred annuities that offer immediate-style payout options. Search did not surface a
  currently marketed product named 즉시연금 from a major carrier. It is therefore
  `[unverified]` whether the product is written today under that name, or whether it survives
  as a zero-deferral election on a general 연금보험. `product-spec.md` should be written to
  the mechanism, not to a named live product.
- **Joint-life (부부형) mechanics and factors.** [S6] establishes the option exists and raises
  the minimum annuity age to 48 for a male principal insured; nothing further is sourced.
- **Lapse and surrender experience.** No retrieved source gives a surrender rate for
  즉시연금 by duration or by shape. Given that 종신연금형 cannot be surrendered at all after
  month one, the only decrement that matters on that shape is mortality; on the other two
  shapes the lapse assumption is entirely unsourced and must be `[std]`.
- **Expense analysis and profit source split.** No 사차/이차/비차 decomposition, and no
  actual-versus-expected expense analysis, was retrieved for this line.
