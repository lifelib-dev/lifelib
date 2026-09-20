# 암보험 (cancer) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean 암보험 (*am boheom*, cancer insurance) liability cash flow
reference model — a fixed-benefit (정액, *jeongaek*) 제3보험 (*je-sam boheom*, third-sector)
product whose benefits are triggered by the **diagnosis** of a cancer named in a policy
schedule keyed to the KCD (한국표준질병·사인분류) code list, and secondarily by cancer
surgery, cancer inpatient days and anti-cancer drug or radiation treatment.

Korea's cancer product is not a translated Japanese one. Four features make it its own
thing, and all four are load-bearing for the model. First, the **90-day 면책기간**
(*myeonchaek gigan*, waiting period) is close to universal, and a diagnosis inside it does
not merely fail to pay — it makes the cover **무효** (void), with premiums returned.
Second, a **감액기간** (*gamaek gigan*, reduced-benefit period) of one or two years from
inception during which only 50% of the sum insured is paid sits *on top of* the waiting
period; it is a second, softer anti-selection device with no counterpart in `jplib`.
Third, the benefit is **tiered by cancer site and severity** — 고액암 (high-cost) above,
일반암 (general) in the middle, 특정소액암 and 유사암 (*yusa-am*, "similar cancers":
기타피부암, 갑상선암, 제자리암, 경계성종양, and on many contracts 대장점막내암) below at
10–20% — and the tier boundaries have moved over time under supervisory pressure. Fourth,
because the public 국민건강보험 already caps a cancer patient's own share of scheduled
charges at **5%** for five years under 산정특례, the private product is not there to
reimburse the hospital bill; it is there to replace income and pay for what the public
scheme does not schedule. That is why it is written as a lump sum on diagnosis rather than
as an indemnity.

This file is the **provenance layer** behind `products/cancer/product-spec.md`,
`technical-notes.md`, `model.md` and `sources.md`. Every fact below carries the tag of the
document it came from: `[S#]` for a primary product document (약관, 상품요약서, 상품 공시
페이지) and `[R#]` for a regulatory, actuarial, statistical or legal reference. Where a
statement rests on general knowledge or on a secondary snippet that could not be confirmed
against a retrieved document it is tagged `[unverified]` and is repeated in the *Fetch
failures and gaps* section at the end. **Source ids are FROZEN.** The four product
documents cite against the numbering below and nobody may renumber it.

Access date for every fetched source: **2026-09-03**. Seven carriers are covered: three
life insurers (한화생명, 라이나생명, 교보생명 — the last only through a consumer-education
page), three non-life insurers writing the same cover as 제3보험 (삼성화재, AIG손해보험,
and 삼성화재 다이렉트 as a separate 2026 edition), plus 삼성생명 whose product page could
not be retrieved. Company and branded product names appear here and in `sources.md` only.

A note on the retrieved 약관 text. Korean policy PDFs set article headings in a doubled
bold face, so `pypdf` extracts them as `제제 55조조 ((암암 ,, ...))` rather than
`제5조(암, ...)`. Body text is frequently extracted with a space inserted between every
syllable. Quotations below are given in normalised form (doubling collapsed, inter-syllable
spaces removed); nothing else has been altered, and the article numbers are as printed.

---

## Primary sources

### S1 — 삼성화재, 「무배당 삼성화재 건강보험 태평삼대(1811.6) 15년만기형 보험약관」
- Publisher: 삼성화재해상보험주식회사 (Samsung Fire & Marine Insurance) — a **non-life**
  insurer writing this cover as 제3보험
- Document: 보험약관, file `ZPB205040_0_20180805_file1.pdf`, **382 pp**, 2018 edition
- Doc type: 보험약관 (policy conditions) with a front 상품요약 / 유의사항 section
- URL: https://www.samsungfire.com/publication/pdf/ZPB205040_0_20180805_file1.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (full PDF downloaded, 382 pp.; text layer
  extracted cleanly, ~534,000 characters, including the 보통약관 body and the 특별약관 for
  every rider)
- Key content: the single most complete retrieved statement of the **면책기간 / 감액지급
  matrix** — which of 24 named benefits carry the 90-day waiting period and which carry the
  1-year 50% reduction, benefit by benefit; 제5조 (암, 기타피부암, 갑상선암 및 대장점막내암의
  정의 및 진단확정) and 제6조 (제자리암 및 경계성종양의 정의 및 진단확정) verbatim; the
  five-member 유사암 set; the 특정소액암 / 5대 주요암 / 10대 주요암 tiering with their KCD
  site lists; 제28조 (계약의 무효) with the pre-waiting-period diagnosis rule; 재진단암 on a
  2-year cycle; 암 직접치료 입원일당 at 180 days per stay with 유사암 paid at 20% of the
  daily amount; 항암방사선·약물 치료비 with 기타피부암·갑상선암 at 20%; 제9조 premium waiver;
  a 15-year term with 재가입; 최저보증이율 0.5% on the 적립부분.

### S2 — 삼성화재 다이렉트, 「무배당 삼성화재 다이렉트 건강보험 2601.16 보험약관」
- Publisher: 삼성화재해상보험주식회사 (direct channel)
- Document: 보험약관, file `health_insu.pdf`, **511 pp**, 2601.16 edition (2026)
- Doc type: 보험약관
- URL: https://direct.samsungfire.com/CR_MyAnycarWeb/mall/pdf/health_insu.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (511 pp.; text extracted, ~931,000 characters;
  the 유의사항 tables and the cancer 특별약관 read in full)
- Key content: **the current-market comparator to [S1], eight years later**, and the single
  most valuable retrieved document for showing what has changed. The 암 진단비(유사암 제외)
  rider now carries **no 감액 at all** — 100% from the day after the 90-day wait — while
  유사암 진단비 keeps a 1-year 50% reduction; the 면책기간 does **not** apply to a life
  aged under 보험나이 15 (보장개시일 = 보험계약일); 갱신계약 carries neither 면책기간 nor
  감액; and a 다빈치로봇 수술비 with a **180-day / 1-year two-step** reduction (25% then 50%)
  appears, which is a shape absent from every other retrieved contract.

### S3 — 한화생명, 「한화생명 e암보험(비갱신형) 무배당 약관」
- Publisher: 한화생명보험주식회사 (Hanwha Life Insurance) — a **life** insurer
- Document: 보험약관, 166 pp, edition dated **2025-01-06**; 표준체형/비흡연체형 variants
- Doc type: 보험약관 (주계약 + 제도성특약 + 별표)
- URL: https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e암보험(비갱신형)%20무배당_약관_20250106.pdf
  (query string `?docUrl=dynamic/direct/product/cms_K86hzsQGOOnVEFlC_1736169011449.pdf`)
- Accessed: 2026-09-03. Retrieved: **yes** (166 pp.; text extracted cleanly and read article
  by article)
- Key content: the **cleanest retrieved stand-alone cancer main contract**, and the source
  of the shipped benefit ratios. 별표 1 보험금 지급기준표 states every benefit as an amount
  at 보험가입금액 1,000만원, so the tier ratios are read directly rather than inferred;
  a **2-year** 감액기간 at 50%; 제2조 정의 with 암보장개시일 = day 91; 제3조–제11조 defining
  암 / 특정 고액치료비관련암 / 특정 소액암 / 중증 갑상선암 / 기타피부암 / 갑상선암 /
  대장점막내암 / 제자리암 / 경계성종양 with their KCD numbers; 제12조 the
  contract-vs-diagnosis KCD-vintage rule; 제30조 보험나이 with a worked example; 제41조
  해약환급금 including the **해약환급금 미지급형 (납입기간중 0%, 납입기간후 50%)** form;
  별표 5 the full 악성 신생물 분류표 (24 rows of KCD codes); 별표 10 특정 고액치료비관련암.

### S4 — 한화생명, 「한화생명 e시그니처암보험 무배당 약관」
- Publisher: 한화생명보험주식회사
- Document: 보험약관, **597 pp**, edition dated **2024-04-01** (내부 코드 2063-A01_A02)
- Doc type: 보험약관 — a modular product: one 공통사항 chapter plus **23 separate
  주계약 약관**, each its own module, sold in any combination
- URL: https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e시그니처암보험%20무배당_2063-A01_A02_약관_20240401_.pdf.pdf.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (597 pp.; text extracted, ~887,000 characters;
  the diagnosis, surgery, inpatient and chemotherapy modules read in full)
- Key content: the **갱신형 chassis** and the modular architecture that the Korean market has
  converged on. 제2-11조의6 (계약의 갱신) verbatim: automatic renewal unless the policyholder
  objects 15 days before expiry, final renewal ending at the 100세 계약해당일, premium
  recalculated at the attained age on the rate basis in force at renewal, 보험가입금액
  unchanged, and a module on which a benefit has been paid **does not renew**. On a
  갱신계약 the 암보장개시일 is the **갱신일** — no fresh 90-day wait — and the 감액 does not
  apply. Module benefit schedules give 항암약물치료자금 / 항암방사선치료자금 in two tiers,
  상급종합병원 암입원급여금 at 1일 초과 1일당 with a **120-day per-stay cap**, 암수술자금
  split 관혈 / 비관혈 at 5:1, and 수술 defined by a 수술분류표 with the standard exclusions.

### S5 — 한화생명, 「한화생명 e암치료비보험 무배당 약관」
- Publisher: 한화생명보험주식회사
- Document: 보험약관, 216 pp, edition dated **2025-07-21**
- Doc type: 보험약관 — again modular, but **비갱신형** modules only
- URL: https://direct.hanwhalife.com/products/downloadProxy/한화생명%20e암치료비보험%20무배당_약관_20250721.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (216 pp.; text extracted; the 감액지급 table and
  the 다빈치로봇 module read)
- Key content: the **treatment-cost (치료비) chassis** — no diagnosis lump sum at all, only
  treatment-event benefits (다빈치로봇 수술자금, 암수술자금, 암주요치료자금,
  항암약물·방사선 치료자금). Uniform **2-year 50% 감액**, with a **180-day 25%** first step
  on the robot-surgery module. Confirms that on treatment benefits the 감액 clock runs from
  보험계약일 to the **treatment date**, not to the diagnosis date.

### S6 — 라이나생명, 「무배당 첫날부터라이나암보험(갱신형) 약관」
- Publisher: 라이나생명보험주식회사 (Chubb Life / LINA Life Insurance Korea)
- Document: 보험약관, 48 pp, file `B00370002_1_P.pdf` on the carrier's 공시 directory
- Doc type: 보험약관 with a front 시각화된 약관 요약 (visual summary)
- URL: https://www.lina.co.kr/cms/upload/upload/docs/disclosure/B00370002_1_P.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (48 pp.; text extracted and read)
- Key content: **the one retrieved contract with no waiting period at all** — the product
  name means "from the first day". 제26조 defines 보장개시일 as the day the first premium is
  received and adds 「또한, 보장개시일을 계약일로 봅니다」; the 요약 table lists a 감액지급
  block and **no 면책기간 block**. It keeps a 1-year 50% 감액 on every benefit and pays
  유방암/전립선암 at **20%** and 갑상선암·기타피부암·제자리암·경계성종양 at **10%** of
  보험가입금액. This is the lower bound of the observed 유사암 range.

### S7 — 라이나생명, 「무배당 라이나 퍼펙트케어암보험(갱신형) 약관」
- Publisher: 라이나생명보험주식회사
- Document: 보험약관, 35 pp, file `B00179014_0_P.pdf`
- Doc type: 보험약관 with a 시각화된 약관 요약
- URL: https://www.lina.co.kr/cms/upload/upload/docs/disclosure/B00179014_0_P.pdf
- Accessed: 2026-09-03. Retrieved: **yes** (35 pp.; text extracted and read)
- Key content: the same carrier's **conventional** shape, and therefore a controlled
  comparison against [S6]: 90-day 면책 on 암 and on 유방암/전립선암 but **none** on the four
  유사암; a **2-year** 50% 감액 on everything; identical 20% / 10% tier ratios; renewal to a
  100세 만기 once the insured passes 가입나이 85; 「갱신계약은 면책기간이 없습니다」 and
  「갱신계약은 감액지급이 없습니다」 stated as headline summary lines.

### S8 — AIG손해보험, 「(무)AIG 소문난NEW암보험2106」 상품 페이지
- Publisher: AIG손해보험주식회사 (AIG General Insurance Korea)
- Doc type: 상품 페이지 (product page) with 가입안내, 상품의 특이사항 and a
  해약환급금(률) 예시 table
- URL: https://www.aig.co.kr/wp/dpwpm400c.jsp?prodAlias=cancer01&menuId=MS1050&prodCd=L0216
- Accessed: 2026-09-03. Retrieved: **yes** (HTML retrieved and converted; the 보장내용 and
  가입예시 tabs are rendered client-side and did **not** come through — see gaps)
- Key content: the **only retrieved published premium and surrender-value example** in this
  session, at 남자 40세 / 월납 / 10년납 10년만기 / 순수보장형 for three plans; the
  계약자적립액 적용이율 of **연복리 1.5%**; a **70%** 유사암 payout ratio, the highest
  observed and a pre-2022 design; the full 재진단암 definition (새로운 원발암 / 전이암 /
  재발암 / 잔여암) on a 2-year cycle; and a 2종 만기환급형 variant returning **5%** of
  보험가입금액 at maturity.

### S9 — 교보생명, 「암의 종류와 보장 범위 (유사암 vs 소액암 vs 고액암)」
- Publisher: 교보생명보험주식회사 (Kyobo Life Insurance)
- Doc type: 금융정보 Q&A page (consumer education), dated **2022-06-23**
- URL: https://www.kyobo.com/dgt/web/customer/finance-information/finance-qna/8992
- Accessed: 2026-09-03. Retrieved: **yes** (via WebFetch; the page's substantive text was
  returned, the surrounding navigation was not)
- Key content: a carrier's own four-tier taxonomy — 유사암 (기타피부암, 갑상선암, 제자리암,
  경계성종양), 소액암 (자궁암, 유방암, 방광암, 전립선암), 고액암 (뼈암, 뇌암, 혈액암,
  식도암, 췌장암, 간암, 담낭암, 담도암, 기관지암, 폐암), 일반암 — with the 10~20% payout
  band on the two low tiers and a stated 고액암 treatment cost "averaging over ₩50,000,000".

### S10 — KB손해보험 인사이트, 「암보험 가입할 때 알아야 할 몇 가지」
- Publisher: KB손해보험주식회사 (KB Insurance), corporate content site
- Doc type: 보험 상식 article, dated **2025-11-06**
- URL: https://insight.kbinsure.co.kr/info_cancer/
- Accessed: 2026-09-03. Retrieved: **yes**
- Key content: the most recent **carrier statement of where the market now is**: 유사암
  진단비 now written up to **₩30,000,000 (3천만원)**; 감액기간 on 일반암 being shortened or
  removed; 3대 / 5대 / 10대 고액암 as alternative high-tier definitions; 재진단암 paid
  「매 1~2년마다」; and the flat statement that the diagnosis date is the **조직검사 결과
  보고일**, not the date the certificate is issued — which is what decides whether a claim
  falls inside the 면책기간 or the 감액기간.

### S11 — 삼성생명 다이렉트, 암보험 상품 페이지
- Publisher: 삼성생명보험주식회사 (Samsung Life Insurance)
- Doc type: 상품 페이지 (direct channel)
- URL: https://direct.samsunglife.com/ncancer.eds
- Accessed: 2026-09-03. Retrieved: **NO** — HTTP 200 but the body is a 6,761-byte
  JavaScript shell containing 16 characters of text. Nothing was taken from it. **Korea's
  largest life insurer is therefore not represented in this file by any product document**;
  see *Fetch failures and gaps*.

---

## Regulatory and actuarial references

### R1 — 중앙암등록본부 / 보건복지부, 「2023년 국가암등록통계 참고자료」
- Publisher: 보건복지부 · 중앙암등록본부 (국립암센터), released **2026-01-20**
- Document: 2023년 국가암등록통계 참고자료, **41 pp**, PDF
- Doc type: national cancer registry statistical annex (public)
- URL: https://www.cancer.go.kr/download.do?uuid=cfcd35c3-391f-4060-9688-641db3d86cbd.pdf
  (index: https://www.cancer.go.kr/lay1/bbs/S1T674C816/B/61/view.do?article_seq=85579)
- Accessed: 2026-09-03. Retrieved: **yes** (41 pp. downloaded and fully text-extracted;
  every table below was read off the extracted text)
- Content: **this is the citable public incidence basis that lets the model ship a sourced
  rather than an invented decrement.** It carries: 발생자수 / 조발생률 / 연령표준화발생률 by
  sex for 1999–2023; the 2023 site ranking with 분율; 평생 암발생/사망 위험도 by site and
  sex; **암발생 현황 by 10-year age band × sex** (the table the model's incidence curve is
  built from); the 요약병기 (localized / regional / distant) distribution 2005–2023; 5-year
  relative survival by period 1993–2023 and by 요약병기; 암유병자수 by age band and **by
  elapsed time since diagnosis** (≤1년 / 1–2년 / 2–5년 / >5년); and a separate 별첨 giving
  **상피내암 (carcinoma in situ) 발생률** 1999–2023 by sex and site — the in-situ series that
  a 유사암 tier has to be priced from.

### R2 — 국가암정보센터, 「통계로 보는 암 — 암 발생률」 및 「암종별 발생 현황」
- Publisher: 국립암센터 국가암정보센터 (National Cancer Information Center)
- Doc type: public statistics pages, 최종수정일 **2026-01-27**
- URLs: https://www.cancer.go.kr/lay1/S1T639C640/contents.do (암 발생률) and
  https://www.cancer.go.kr/lay1/S1T639C641/contents.do (암종별 발생 현황)
- Accessed: 2026-09-03. Retrieved: **yes** (HTML retrieved and converted; the data tables
  came through, the charts did not)
- Content: corroborates [R1]'s headline 2023 figures independently (288,613 발생자수;
  조발생률 564.3; 연령표준화발생률 522.9) and carries the year-on-year commentary. Used only
  as a cross-check on [R1]; no figure below rests on it alone.

### R3 — 보험연구원, 「암보험 관련 주요 분쟁사례 연구」 (연구보고서 2019-4)
- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI); 저자 백영화·박정희,
  **2019년 10월**
- Document: 연구보고서 2019-4, **169 pp** PDF
- Doc type: research report (institutional, peer-reviewed by the institute)
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=44
  (chapter II is separately published as
  https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2019-04_2.pdf)
- Accessed: 2026-09-03. Retrieved: **yes** (169 pp. downloaded and text-extracted; chapters
  I, II, III.5, III.6 and III.7 read in full)
- Content: **the load-bearing legal and historical reference for this product.** It gives
  the product's history with dates; the KCD 행동양식 분류번호 mechanics (/0, /1, /2, /3, /6)
  and which D- and C-code ranges they map to; the standard 약관 wording for 암의 정의,
  진단확정, 암보장개시일 and 감액; the FSS 금융분쟁조정위원회 decisions and the court
  judgments on 갑상선암 림프절 전이, on KCD reclassification, and on 요양병원 입원비; the
  2011-04-01 supervisory change on 이차성 암; and the complaint volumes that drove it.

### R4 — 보험연구원, 「암보험 상품의 현황과 발전방향」 (김석영)
- Publisher: 보험연구원; 저자 김석영 연구위원
- Document: KIRI 리포트 / 고령화 리뷰 note, **14 pp** PDF
- Doc type: research note
- URL: https://www.kiri.or.kr/community/boardDownloadFile.do?bid=689&seq=2
- Accessed: 2026-09-03. Retrieved: **yes** (fetched through WebFetch after plain `curl` was
  reset by the host; the returned PDF was saved locally and text-extracted in full)
- Content: **the actuarial history of the product**, and the only retrieved source that
  states how the risk basis was built. It carries a 암보험 상품의 변천 table mapping the
  경험생명표 generations (2회 1992.8–1996.12, 3회 1997.1–2002.12, 4회 2003.1–2005.12,
  5회 2006.1–) to the benefit menu of each era and to the risk-rate source of each era
  (일본통계 → 국내통계 → 경험통계); the statement that 예정위험률 in Korea carries **no
  trend loading**; the 2010 incidence and survival tables; and the four risk factors the
  institute identified in the then-new generation of products.

### R5 — 보험개발원, 「장기손해보험 참조순보험요율 예시」
- Publisher: 보험개발원 (Korea Insurance Development Institute, KIDI)
- Doc type: 공시 page under 알림광장 → 참조 순보험요율 → 장기손해보험
- URL: https://www.kidi.or.kr/user/nd13261.do
- Accessed: 2026-09-03. Retrieved: **yes** (HTML retrieved and converted; the rate tables
  came through as text)
- Content: **the single most important actuarial source in this file.** It publishes, for
  public display, the 참조순보험요율 in force **적용시점 2024년 4월 1일 이후**, including a
  「기타피부암 및 갑상선암 이외의 암 발생률」 table by age (0/10/20/…/80) and sex. That is a
  published, dated, sourced cancer-incidence basis matched to the *insured* definition of
  cancer — invasive cancer excluding C44 and C73 — which is exactly the decrement a Korean
  일반암 진단비 model needs. The same page publishes 질병사망률 and
  질병입원율(1일이상 180일한도) on the same age grid.

### R6 — 금융감독원, 「금융꿀팁 200선 — 암보험 가입자가 꼭 알아야 할 필수정보:
###      암진단비, 암입원비」
- Publisher: 금융감독원 (Financial Supervisory Service), 보도자료 **2017-11-03**
- Doc type: consumer-guidance press release
- URL retrieved: https://www.samili.com/samilinews/ContentSer.asp?idx_no=26063 (삼일인포마인
  reproduction). The FSS's own copy was **not** retrieved — see gaps.
- Accessed: 2026-09-03. Retrieved: **in part** (the reproduction's substantive text was
  returned; the original release's figures and 그림 were not seen)
- Content: the supervisor's own statement of the two timing devices —
  「암에 대한 책임개시일은 계약일로부터 그 날을 포함하여 90일이 지난날의 다음날부터」,
  the exception for 갱신계약 and 어린이암보험, the 「통상 보험계약일 이후 1~2년 이내에 암
  진단확정시에는 암보험 가입금액의 50%」 reduction, and the 유방암 90-day 10% variant.
  [R3] quotes the same release for the 의학적 암의 진단 과정 diagram.

### R7 — 상법 제4편 「보험」 (Commercial Act, Part IV Insurance)
- Publisher: 대한민국 국회 / 법제처; text retrieved from 위키문헌 (Wikisource) transcription
- Doc type: statute
- URL: https://ko.wikisource.org/wiki/대한민국_상법
- Accessed: 2026-09-03. Retrieved: **yes** (full text of Part IV extracted; individual
  articles read verbatim). Caveat: this is a **transcription**, not 법제처's own copy;
  `law.go.kr` was unreachable from this session (see gaps). Article numbering and the
  amendment annotations match the official text as far as could be checked.
- Content: the contract-law furniture the 약관 rest on — 제638조의3 (약관 교부·설명 의무,
  3-month cancellation), 제644조 (보험사고의 객관적 확정의 효과 — the statutory basis of the
  pre-waiting-period 무효 rule), 제651조 (고지의무위반, 1개월 / 3년), 제656조 (보험료의
  지급과 보험자의 책임개시), 제662조 (소멸시효 — 3년 on benefit claims), 제663조
  (불이익변경금지), and **제739조의2 / 제739조의3 (질병보험자의 책임 / 준용규정, both
  신설 2014-03-11)**, which are the private-law recognition of the disease-insurance
  contract that 암보험 is.

### R8 — 보험업법 제4조 (보험업의 허가)
- Publisher: 대한민국 국회 / 법제처; text retrieved from CaseNote
- Document: 보험업법 [시행 2021. 6. 9.] [법률 제17636호, 2020. 12. 8., 일부개정]
- Doc type: statute
- URL: https://casenote.kr/법령/보험업법/제4조
- Accessed: 2026-09-03. Retrieved: **yes** (article text returned verbatim with the
  amendment history)
- Content: the statutory definition of **제3보험업** and its 보험종목 — 가. 상해보험,
  나. 질병보험, 다. 간병보험, 라. 그 밖에 대통령령으로 정하는 보험종목 (제4조제1항제3호) —
  and 제4조제3항, under which a licence for the whole of 생명보험업 or 손해보험업 is deemed
  to carry the 제3보험 licence. That is why both a life insurer [S3] and a non-life
  insurer [S1] can write the identical cancer cover.

### R9 — 통계청, 「2024년 사망원인통계 결과」
- Publisher: 통계청 (Statistics Korea), 보도자료 **2025-09-25**
- Doc type: national statistical release
- URL retrieved: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156721880
  (대한민국 정책브리핑 reproduction of the 부처 브리핑). The 통계청 PDF at
  `files-scs.pstatic.net` was **not** retrievable — see gaps.
- Accessed: 2026-09-03. Retrieved: **in part** (headline figures returned; the by-site and
  by-age detail tables were not seen)
- Content: 2024 총사망자 358,569명, 조사망률 702.6/10만; 악성신생물 **24.8%** of all deaths
  at **174.3/10만**, up 4.5% year on year; 폐암 38.0, 간암 20.4 per 100,000; male cancer
  mortality 215.1 against female 133.7, a ratio of 1.6.

### R10 — 국가데이터처(통계청), 「제8차 한국표준질병·사인분류(KCD-8) 개정·고시」
- Publisher: 통계청 (now 국가데이터처), 보도자료 **2020-07-01**
- Doc type: press release announcing the 고시
- URL: https://mods.go.kr/board.es?mid=a10301010000&bid=246&act=view&list_no=383272
- Accessed: 2026-09-03. Retrieved: **in part** (via WebFetch; the release text returned but
  the 고시 number itself and the code counts were not in the retrieved body)
- Content: KCD-8 was 고시 on **2020-07-01** and took effect **2021-01-01**, reflecting WHO's
  ICD-10 and ICD-O-3 updates. The 고시 number **통계청 고시 제2020-175호** is not in this
  release but *is* stated inside the retrieved 약관 themselves [S3] [S4], which is where the
  number below is taken from.

### R11 — 찾기쉬운 생활법령정보, 「암 예방 및 치료 지원 → 국민건강보험공단 의료비 지원」
- Publisher: 법제처 (Ministry of Government Legislation), 생활법령 service
- Doc type: statutory guidance page
- URL: https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=733&ccfNo=3&cciNo=1&cnpClsNo=2
- Accessed: 2026-09-03. Retrieved: **yes**
- Content: the **산정특례** rule that shapes the whole product. Under 국민건강보험법 제44조
  제1항, 동법 시행령 제19조제1항 및 별표 2, and 「본인일부부담금 산정특례에 관한 기준」
  제4조 및 별표 3, a registered cancer patient pays **5% of the 요양급여비용 총액** for
  **5 years** from registration, inpatient or outpatient, renewable for a further period
  where residual, metastatic or recurrent disease is under continuing chemotherapy.

### R12 — 뉴시스, 「'착한 암' 유사암 진단비, 일반암의 20% 수준으로 축소」
- Publisher: 뉴시스 (Newsis), **2022-08-01** — a **news article**, used here because no
  retrievable primary document for this supervisory action was found
- Doc type: news report
- URL: https://v.daum.net/v/20220801150045941
- Accessed: 2026-09-03. Retrieved: **yes**
- Content: reports that 금융감독원 sent insurers a 공문 setting out 유의사항 for 유사암
  진단 보장상품, with the effect from August 2022 that 유사암 benefits were cut to about
  **20%** of the 일반암 level, from a market in which they had reached **₩50,000,000
  (5천만원)**; names 메리츠화재, DB손해보험, 한화손해보험. **This is a secondary source and
  the underlying 공문 was not retrieved.** Facts resting on it alone are marked as such.

### R13 — 금융감독원, 「질병·상해보험 표준약관」 (보험업감독업무시행세칙 [별표 15])
- Publisher: 금융감독원
- Doc type: 표준약관 (standard policy conditions, mandatory baseline)
- URLs tried: https://www.fss.or.kr/fss/bbs/B0000115/view.do?nttId=55845&menuNo=200504 ;
  https://www.insclaim.co.kr/19/8641153 ; a mirrored PDF on `waf-e.dubudisk.com`
- Accessed: 2026-09-03. Retrieved: **NO** — the FSS board returned an empty reply to
  `curl` and the mirror failed TLS verification; the third URL returned HTTP 404.
  **No verbatim 표준약관 text was obtained in this session.** The dates of its recent
  revisions (개정 2022-02-16 시행 2022-04-01; 개정 2022-09-30 시행 2023-01-01) appear only
  in search-result summaries and are therefore [unverified].

### R14 — 보험개발원, 제10회 경험생명표 (KIDI Experience Life Table, 10th)
- Publisher: 보험개발원
- Doc type: industry mortality table, applied from **2024-04**
- URL tried: https://www.kidi.or.kr/user/nd11592.do (보도자료 index) — the index page was
  retrieved but the release itself was not located
- Accessed: 2026-09-03. Retrieved: **NO**
- Content: not obtained. The table itself is not published to the public in any case (only
  summary statistics are released), so every `mort_table.csv` in `krlib` is a `[std]`
  construction; this entry exists so that the product documents have somewhere to point.

---

## Fact extraction

### 1. Where the product sits: 제3보험 and the public scheme underneath it

- **제3보험업** is a statutory licence category in its own right, alongside 생명보험업 and
  손해보험업. Its 보험종목 are 「가. 상해보험 / 나. 질병보험 / 다. 간병보험 / 라. 그 밖에
  대통령령으로 정하는 보험종목」 (보험업법 제4조제1항제3호) [R8].
- 「생명보험업이나 손해보험업에 해당하는 보험종목의 전부(…보증보험 및 …재보험은
  제외한다)에 관하여 제1항에 따른 허가를 받은 자는 제3보험업에 해당하는 보험종목에 대한
  허가를 받은 것으로 본다」 (제4조제3항) [R8]. A fully licensed life insurer and a fully
  licensed non-life insurer therefore both write cancer cover **without a further licence**,
  and the retrieved documents bear that out: [S1] [S2] [S8] are non-life contracts and
  [S3] [S4] [S5] [S6] [S7] are life contracts, carrying materially the same benefits.
- Private-law recognition arrived late. 상법 제739조의2 (질병보험자의 책임) and 제739조의3
  (질병보험에 대한 준용규정) were both **신설 2014-03-11** [R7]; before that a disease
  contract was construed by analogy to life and accident cover, which 제739조의3 now says
  expressly: 「질병보험에 관하여는 그 성질에 반하지 아니하는 범위에서 생명보험 및 상해보험에
  관한 규정을 준용한다」 [R7].
- **The public scheme sets the private product's job.** A registered cancer patient pays
  **5%** of the total 요양급여비용 for **5 years** from registration, inpatient or outpatient,
  under 국민건강보험법 제44조제1항, 시행령 제19조제1항 및 별표 2, and 「본인일부부담금
  산정특례에 관한 기준」 제4조 및 별표 3 [R11]. The 5-year window can be extended where
  residual, metastatic or recurrent disease is under continuing chemotherapy [R11].
- Consequently 암보험 in Korea is **정액 (fixed-benefit)**, not indemnity: every retrieved
  contract pays 보험가입금액 or a stated fraction of it on a defined event, and none of them
  indemnifies a bill. What the lump sum is understood to cover is stated by the research
  institute rather than by the carriers: 「암은 통상적으로 치료기간이 길고 치료비용이 많이
  발생하며 간병비 등 부대비용과 암을 치료하는 기간 동안 경제활동을 하지 못함으로 인하여
  발생하는 소득 감소분까지 감안하면 암으로 인한 개인의 경제적 부담이 매우 높은 것이 현실」
  [R3].
- One dated cost anchor exists: 국립암센터's 2009 release put the average per-patient cost
  burden at **₩29,700,000 (2,970만원)**, highest for 백혈병 at ₩67,000,000 (6,700만원),
  then 간암 ₩66,200,000, 췌장암 ₩63,700,000, 폐암 ₩46,600,000 [R3, footnote 3, citing
  국립암센터 보도자료 2009-06-03]. A carrier repeats the ₩50,000,000-plus figure for 고액암
  without a date [S9]. Both are historical and neither is a current price.

### 2. History: how the Korean product got its present shape

The two retrieved institutional histories disagree on the start date and agree on
everything after it. Both are reported.

- **First sale.** 「우리나라에서 암보험은 1980년 12월에 최초로 판매되었다」, on a 재무부
  instruction (재무부, 보험 1223-431) that six life insurers jointly develop and sell cancer
  and health cover; the first product covered 암 사망, 수술, 입원, 통원, 요양 [R3]. The other
  source dates it later: 「국내 암보험 상품은 1988년 7월 21세기 암보험을 시작으로」, with the
  same five-benefit menu [R4]. The **discrepancy is unresolved**; both are institutional
  publications and neither cites a primary document that could be retrieved here.
- **No diagnosis benefit at first.** 「최초 상품은 … 현재 판매되고 있는 상품과 달리 암 진단
  급부가 없는 대신 암 사망 급부가 주요 담보였음. 당시, 암 진단 시 오래 생존하지 못한다는
  사회적 통념을 반영한 상품 구조임」 [R4]. The diagnosis benefit was added in **1991년 1월**
  [R4], and 「1991년부터는 암 진단 급부가 추가됨으로써 현재의 암보험의 모습을 갖추기
  시작하였다」 [R3].
- **1997**: non-life insurers were allowed in. 「암보험 상품은 원래 생명보험회사만
  판매하였으나, 1997년부터는 손해보험회사도 암보험 판매가 가능해졌다」, following the
  1997 금융개혁위원회 recommendation to allow 겸영 of 제3분야 [R3].
- **1997**: 상피내암 brought inside cover. 「원래는 암(악성종양, 악성 신생물)만을 담보하던
  암보험 상품에서, 1997년부터는 상피내암 … 도 담보하기 시작하였다 … 다만 일반암보험금의
  **40% 수준**으로 보험금을 지급하기로 하였다」 [R3]. That 40% is the **origin of the
  reduced tier** and is far above where it sits today.
- **2002**: 경계성종양 added on the same footing as 상피내암, following a 금융감독원
  보도자료 of 2002-05-20 on 생명보험 표준약관 개정 [R3].
- **2000s**: loss ratios rose and the market contracted. 「의료기술의 발전에 따른 암의 조기
  발견율 증가 등으로 인하여 2000년대에 들어서 암보험의 손해율이 높아졌고, 그에 따라
  2000년대 중반부터 암보험 시장이 위축되었다. 이에 보험회사들은 … 기타 피부암, 갑상선암
  등은 **소액암으로 분류하여** 일반암에 비해 진단 급부를 축소함으로써 리스크를 관리하고자
  하였다」 [R3]. The companion note dates this to the **5회 경험생명표 era, 2006년 1월
  이후**, whose listed features are 「암보험 판매중지 / **갑상샘암 소액화** / 갱신형 도입」
  [R4].
- The same table [R4] gives the risk-basis lineage, which matters because it says what the
  pricing was built on: **2회 (1992.8–1996.12)** — 「위험률은 모두 일본통계 적용」;
  **3회 (1997.1–2002.12)** — 「암발생률 국내통계 전환」, features 상피내암 급부 추가 and
  기타피부암 소액화; **4회 (2003.1–2005.12)** — 「암발생률 경험통계 전환」, features
  방사선치료 급부, 암수술횟수 도입, 경계성종양 추가; **5회 (2006.1–)** — 판매중지, 갑상샘암
  소액화, 갱신형 도입 [R4].
- **2011-03-14**: 금융감독원 보도자료 「소비자 권익 보호를 위한 보험약관 개선」 required the
  이차성 암 payment rule to be written into 약관 **from 2011-04-01** — see §10 [R3].
- **2010s**: the supervisor pushed the other way. 금융감독원 보도자료 2011-06-20
  「암보험 판매 현황 및 활성화 방안 마련 추진」 and 2013-08-22 「다양해진 암보험, 이것만은
  알고 가입하세요」 are cited for a deliberate revival [R3]. The 2013 release's own
  comparison table, reproduced at [R3] <표 II-1>, is worth quoting in full because it is
  the supervisor's description of the change: 보장금액 「동일 금액(예: 5천만 원) 지급」 →
  「암 진행정도(병기) 및 치료비 등에 따라 차등 지급」; 진단보험금 보장횟수 「통상 1회(최대
  2회)」 → 「보험기간 중 반복 지급(횟수제한 無)」; 가입대상 「60세 이하 건강한 사람」 →
  「80세 이하 및 암·만성질환 등 유병자까지 확대」; 보험기간 「통상 80세 이하」 →
  「100세 혹은 사망 시(종신)까지」 [R3].
- **2019**: carriers began removing the 감액기간. 「최근에는 보험회사들이 이와 같은 감액기간을
  없애고 90일의 부담보기간 종료 이후에는 바로 보험금의 100%를 지급하는 상품들도 출시하고
  있다」 [R3, citing 뉴데일리 2019-06-04]. [R3] also records press reports of the 「암보험
  20%룰」 being broken in 2019 by products paying 유사암 at the full 일반암 level [R3,
  footnote 26, citing 머니투데이 2019-05-13]. The retrieved 2026 contract [S2] shows the
  first of those two changes has stuck: its 암 진단비(유사암 제외) carries no 감액 at all.
- **2022-08**: the supervisor pushed the 유사암 level back down to about 20% of 일반암, by
  공문 rather than by rule [R12] (news source; the 공문 itself was not retrieved).
- **2025**: the market's stated position, from a carrier: 「최근에는 유사암(소액암) 진단비가
  상향되고 일반암에 대한 감액 기간이 축소되는 등, 고객 입장에서 암 보장이 보다 강화된
  상품이 출시되고 있습니다」, with 유사암 진단비 written up to **₩30,000,000** [S10].

### 3. What "cancer" means: the KCD chassis

- Korean cancer policies do not define cancer clinically. They **incorporate a public
  statistical classification by reference and then list the codes in an annex**: 「약관
  본문에서 "암이라 함은 제[ ]차 한국표준질병·사인분류에 있어서 별표[ ]에서 정한 질병을
  말한다"라고 정의하고, 약관 별표에서 악성 신생물 분류표를 제시하여 그 대상이 되는 악성
  신생물의 종류와 분류번호를 열거하고 있다」 [R3].
- The classification is the **한국표준질병·사인분류 (KCD)**, published by 통계청 and
  following the WHO ICD framework [R3]. Revision history, as printed at [R3] footnote 16:
  제1차 1973-01-01, 제2차 1979-01-01, 제3차 1995-01-01, 제4차 2003-01-01, 제5차 2008-01-01,
  제6차 2011-01-01, 제7차 2016-01-01 [R3]. The **제8차** was 고시 2020-07-01 and took effect
  **2021-01-01** [R10]; the retrieved 약관 identify it as **통계청 고시 제2020-175호,
  2021.1.1 시행** [S3] [S4].
- The mechanism that decides the tier is the **행동양식 분류번호** — the fifth digit of the
  ICD-O morphology code. [R3] <표 II-3> maps them, and this table is the spine of the whole
  product:

  | 행동양식 분류번호 | meaning | KCD 제2장 항목 |
  |---|---|---|
  | `/0` | 양성 신생물 | D10–D36 |
  | `/1` | 불확실한 또는 알려지지 않은 성격의 신생물 | D37–D48 |
  | `/2` | 제자리신생물 | D00–D09 |
  | `/3` | 일차성으로 기재 또는 추정된 악성 신생물 | C00–C76, C80–C97, D45, D46, D47.1, D47.3, D47.4, D47.5 |
  | `/6` | 이차성으로 기재 또는 추정된 악성 신생물 | C77–C79 |

  「즉, 행동양식 분류번호가 "/3"인 경우에 암(악성종양)에 해당하는 것이며, "/1"인 경우에는
  경계성종양, "/2"인 경우에는 제자리암에 해당한다고 이해하면 될 것이다」 [R3].
- A **retrieved 별표 5 대상이 되는 악성 신생물 분류표** [S3] gives the code list a Korean
  contract actually carries, under KCD-8:

  C00–C14 입술/구강/인두, C15–C26 소화기관, C30–C39 호흡기 및 흉곽내기관,
  C40–C41 골 및 관절연골, C43 피부의 악성 흑색종, **C44 기타 피부**, C45–C49 중피성 및
  연조직, C50 유방, C51–C58 여성생식기관, C60–C63 남성생식기관, C64–C68 요로,
  C69–C72 눈/뇌 및 중추신경계통, **C73 갑상선**, C74 부신, C75 기타 내분비선,
  **C76–C80 불명확한, 이차성 및 상세불명 부위**, C81–C96 림프·조혈 및 관련 조직,
  C97 독립된(원발성) 여러 부위, D45 진성 적혈구증가증, D46 골수형성이상증후군,
  D47.1 만성 골수증식질환, D47.3 본태성(출혈성) 혈소판혈증, D47.4 골수섬유증,
  D47.5 만성 호산구성 백혈병[과호산구증후군] [S3].

  Note that C44 and C73 are **inside** the annex and then carved back out by the definition
  article; and that the five D-codes are inside it, so a handful of `/1`-behaviour myeloid
  neoplasms are treated as 암 rather than as 경계성종양.
- **전암(前癌)상태** — a pre-malignant condition, «Premalignant condition or condition with
  malignant potential» — is excluded by name in every retrieved cancer definition
  [S1] [S2] [S3] [S4] [S5].
- **Which KCD vintage governs** is itself a benefit term, and the retrieved contracts take
  the modern, symmetrical position. 제12조 (한국표준질병·사인분류 적용 기준) [S3]:
  「① 이 약관에서 규정하는 질병 및 재해 분류는 제8차 개정 한국표준질병·사인분류가
  기준이나, 이후 진단(재해의 경우 발생) 당시 한국표준질병·사인분류가 개정된 경우에는
  개정된 기준으로 최종 판단합니다. ② 진단 당시의 한국표준질병·사인분류에 따라 이
  약관에서 보장하는 질병 … 해당여부를 판단하며, 진단 이후 한국표준질병·사인분류 개정으로
  질병 … 분류가 변경되더라도 이 약관에서 보장하는 질병 … 해당 여부를 다시 판단하지
  않습니다」 [S3] [S4]. The article then gives two worked examples, in both of which the
  answer is "no benefit" — the modern wording cuts **both** ways.
- That is a deliberate change from the older wording, which cut one way only, and which
  produced the litigation described in §11.

### 4. 유사암: the reduced tier, and what is in it

- 「유사암은 제자리암, 기타피부암, 경계성종양 및 갑상선암을 총칭합니다」 is the common
  four-member definition [S9]. Both Samsung Fire contracts add a fifth:
  「「기타피부암」,「갑상선암」,「대장점막내암」,「제자리암」또는「경계성종양」(이하
  「유사암」이라 합니다)」 [S1] [S2].
- The member definitions, quoted from a retrieved 보통약관 [S1] 제5조 and 제6조:
  - 「이 보통약관에서「암」이라 함은 한국표준질병·사인분류에 있어서 악성신생물(암)…로
    분류되는 질병([별표-질병관련1] 악성신생물 분류표 참조)을 말합니다. 다만,「기타피부암」,
    「갑상선암」,「대장점막내암」 또는 「전암(前癌)상태…」는 제외합니다」 [S1].
  - 「「기타피부암」이라 함은 한국표준질병·사인분류 중 분류번호 **C44**(기타 피부의
    악성신생물)에 해당하는 질병을 말합니다」 [S1] [S2].
  - 「「갑상선암」이라 함은 한국표준질병·사인분류 중 분류번호 **C73**(갑상선의
    악성신생물)에 해당하는 질병을 말합니다」 [S1] [S2].
  - 「「대장점막내암」이라 함은 대장의 상피세포층(epithelium)에서 발생한 악성종양세포가
    기저막(basement membrane)을 뚫고 내려가서 점막고유층(lamina propria) 또는
    점막근층(muscularis mucosa)을 침범하였으나 **점막하층(submucosa)까지는 침범하지 않은**
    상태의 질병을 말하며, 대장은 맹장, 충수, 결장, 직장을 말합니다」 [S1] [S2]. The 약관
    prints an anatomical diagram beside it.
  - 「「제자리암」이라 함은 한국표준질병·사인분류에 있어서 제자리신생물로 분류되는 질병
    ([별표-질병관련2] 제자리신생물 분류표 참조)을 말합니다. 다만, …대장점막내암은
    제외합니다」 [S1] — i.e. **D00–D09 less 대장점막내암**, which is carved out into its own
    tier [S3].
  - 「「경계성종양」이라 함은 한국표준질병·사인분류에 있어서 행동양식 불명 또는 미상의
    신생물로 분류되는 질병([별표-질병관련3] …)을 말합니다」 [S1] — i.e. **D37–D48**.
- 대장점막내암 is a **defined clinical depth, not a code**, and it is the only tier member
  that is. That is why it can be carved out of 제자리암 without disturbing the D00–D09
  annex, and why it is the subject of its own litigation [R3].
- Two carriers subdivide 갑상선암 by histology and stage rather than treating C73 as one
  block — a design that post-dates the litigation of §11 and is the market's own answer to
  it [S3]:
  - 「「중증 갑상선암」이라 함은 …「갑상선암」 중에서 '수질암(Medullary carcinoma)' 또는
    '역형성암(미분화암, Anaplastic carcinoma)'에 해당하는 질병을 말합니다」 [S3].
  - 「초기갑상선암 : …「갑상선암」 중에서 유두암(papillary cancer) 또는 여포암(follicular
    cancer)으로서 암 종괴의 크기가 **2.0cm 미만**으로서 **림프절 전이나 원격전이가 없는**
    모든 갑상선암」 [S3].
  - What is left — 「'초기 및 중증' 이외의 갑상선암」 — is pushed up into 특정 소액암 and
    paid at 60% [S3]. So one contract pays C73 at **80% / 60% / 20%** of the 일반암 amount
    depending on histology and size, where the market convention is a flat 10–20%.
- **Observed 유사암 payout ratios**, as a percentage of the 일반암 benefit, all from
  retrieved documents:

  | Carrier / product | 유사암 ratio | Source |
  |---|---|---|
  | 라이나 첫날부터 (갱신형) | **10%** | [S6] |
  | 라이나 퍼펙트케어 (갱신형) | **10%** | [S7] |
  | 한화 e암보험(비갱신형) — 소액질병 진단자금 | **20%** (200만원 at 가입금액 1,000만원) | [S3] |
  | 한화 e시그니처 — 기타피부암·중증이외 갑상선암·대장점막내암 | **20%** | [S4] |
  | 삼성화재 (2018, 2026) — 유사암 진단비 as its own rider | separately underwritten; the 진단비 rider's 가입금액 may not exceed the 암 rider's | [S1] [S2] |
  | AIG 소문난 New 암보험2016 | **70%** | [S8] |
  | 교보생명 (market description) | 10–20% | [S9] |
  | KB손해보험 (market description, 2025) | 10–20%, up to ₩30,000,000 absolute | [S10] |

- The 70% figure [S8] is a pre-2022 design and is the observation that makes the supervisory
  intervention legible: the reported 공문 of August 2022 pushed the market back to about
  20% [R12].
- Grading is **not applied uniformly across benefits within a contract**. In one 2018
  contract the 유사암 are excluded outright from 암 진단비, paid in full under a separate
  유사암 진단비 rider, paid at **20% of the daily amount** under 암 직접치료 입원일당,
  excluded from 암 사망 및 고도후유장해 for 제자리암·경계성종양 but included for
  대장점막내암, and paid at **20%** under 항암방사선·약물 치료비 for 기타피부암·갑상선암
  only [S1]. A model that applies one 유사암 ratio to every benefit is wrong for that
  contract.

### 5. 소액암 and 고액암: the tiers above and between

- 「현재 판매되고 있는 암보험 상품들에서는 일부 암을 따로 분류하여 일반암에 비해 소액
  급부의 대상으로 설계하는 것이 일반적이며, 이 경우 그와 같은 소액암들에 대해서는 암의
  정의에서 제외한 후 별도의 정의 조항을 두고 있다 … 이와 같이 암의 정의에서 제외되는
  소액암의 종류와 범위는 **보험회사별로 차이가 있다**」 [R3].
- 「우선, 다른 암에 비해 치료비용이 저렴하고 예후도 좋은 갑상선암, 기타피부암 등의 경우에는
  일반암보험금의 **10~30%**를 보장하는 것이 일반적이다」 [R3, 2019]. [R3] gives a worked
  carrier example at footnote 25: 유방암·전립선암 **40%**, 갑상선암 **30%**, 기타피부암
  **10%** of the 일반암 진단비.
- **특정소액암** as a named middle tier is retrieved verbatim in two forms:
  - 삼성화재: 「특정소액암 : **유방암, 자궁경부암, 자궁체부암, 전립선암, 방광암**」
    [S1] [S2].
  - 한화생명: 「'특정 소액암'」 = **직·결장암, 유방암(C50), 여성생식기암, 전립선암(C61),
    '초기 및 중증' 이외의 갑상선암**, paid at **600만원 per 1,000만원 = 60%** [S3].
  - 라이나: **유방암/전립선암** as a single named tier at **20%** [S6] [S7].
- **고액암** is defined by enumeration and the enumeration is not standard:
  - 「5대 주요암 : 간암, 담낭암, 담도암, 기관암, 폐암」 and 「10대 주요암 : 식도암, 간암,
    담낭암, 담도암, 췌장암, 기관암, 폐암, 골암, 뇌암, 림프·조혈 및 관련 조직의 악성신생물」
    [S1] [S2] — sold as *additional* riders that stack on top of the 암 진단비.
  - 한화생명's 「특정 고액치료비관련암 분류표」 is much tighter: **C40–C41 (골 및 관절연골),
    C70–C72 (뇌 및 중추신경계통), C91–C95 + D47.1 + D47.5 (백혈병)** [S3].
  - 교보생명 lists 뼈암, 뇌암, 혈액암, 식도암, 췌장암, 간암, 담낭암, 담도암, 기관지암, 폐암
    [S9]; KB손해보험 describes 「3대 고액암(뇌암, 뼈암, 백혈병)을 기본으로, 식도, 췌장암을
    포함한 5대 고액암, 거기에 간, 담낭, 담도, 기관지, 폐암까지 추가하여 10대 고액암」 [S10].
- The high tier **adds to** rather than replaces the general benefit. 「피보험자에게 …
  특정 고액치료비관련 암진단자금의 지급사유가 발생한 경우에는 … 암진단자금을 **더하여**
  지급합니다. 다만, 특정 고액치료비관련 암진단자금, 암진단자금은 각각 최초 1회에 한하여
  지급되므로 보험기간 중 이미 암진단자금을 지급한 이후 특정 고액치료비관련 암진단자금의
  지급사유가 발생한 경우에는 암진단자금을 다시 지급하지 않습니다」 [S3]. So a leukaemia
  diagnosis on that contract pays **2,000만원 per 1,000만원 가입금액**, while a stomach
  cancer pays 1,000만원.
- The full retrieved tier ladder of one contract, at 보험가입금액 1,000만원, after the
  감액기간 has expired [S3, 별표 1]:

  | 급부명칭 | 2년 미만 | 2년 이상 | ratio |
  |---|---|---|---|
  | 특정 고액치료비관련 암진단자금 (+ 암진단자금) | 500만원 (+500) | 1,000만원 (+1,000) | 200% |
  | 암진단자금 (일반암) | 500만원 | 1,000만원 | 100% |
  | 중증 갑상선암 진단자금 | 400만원 | 800만원 | 80% |
  | 특정 소액암 진단자금 | 300만원 | 600만원 | 60% |
  | 소액질병 진단자금 (기타피부암 / 갑상선암 / 대장점막내암 / 제자리암 / 경계성종양, each once) | 100만원 | 200만원 | 20% |

  This is the cleanest retrieved ladder in the session and is what the reference
  implementation's tier ratios are anchored on.

### 6. The 90-day 면책기간 (암보장개시일) and its basis

- The rule, and the reason for it, stated by the research institute:
  「일반적인 보험은 **상법 제656조**에 따라 제1회 보험료 납입일부터 보장이 개시된다. 그러나
  암보험의 경우에는 보험계약일로부터 그 날을 포함하여 **90일이 지난 날의 다음 날**
  ("암보장개시일")부터 보장이 개시된다고 정하고 있으므로 이에 유의할 필요가 있다」 [R3].
  상법 제656조 itself reads 「보험자의 책임은 당사자간에 다른 약정이 없으면 최초의 보험료의
  지급을 받은 때로부터 개시한다」 [R7] — the 「다른 약정」 is the 약관's 암보장개시일 clause.
- Purpose: 「보험 가입 전에 이미 암이 발생하였거나 암이 의심되는 사람이 보험금을 받을
  목적으로 보험에 가입하는 것을 방지하기 위한 것이다 … 특히 암보험의 경우 고액의 보험금이
  지급되므로 사행성이 크다는 점에서 **도덕적 해이에 의한 역선택 방지**를 위해서도 일정
  기간의 부담보기간을 두기로 한 것이다」 [R3]. The supervisor states the same rule in
  consumer guidance [R6].
- The 약관 wording is stable across carriers and is worth having verbatim:
  - 「제1항의 경우「암」에 대한 보장개시일(책임개시일)은 이 계약의 보험계약일…부터 그 날을
    포함하여 90일이 지난 날의 다음 날로 합니다. 이 경우 보험계약일은 이 계약의 제1회
    보험료를 받은 날로 합니다」 [S1] 제3조제6항; the 약관 prints a worked example —
    보험계약일 2014년 4월 10일 → 보장개시일 2014년 7월 9일 [S1]. The 2026 edition prints
    the same example dated 2026년 4월 10일 → 2026년 7월 9일 [S2].
  - 「암보장개시일: …「암…」에 대한 보장개시일은 계약일(계약을 부활(효력회복)하는 경우
    부활(효력회복)일)부터 그 날을 포함하여 90일이 지난 날의 다음 날을 말합니다」
    [S3] 제2조제2호라목.
  - 「이 계약의 암보장개시일은 최초계약의 경우 계약일부터 그 날을 포함하여 90일이 지난
    날의 다음 날로 하고 **갱신계약의 경우 갱신일로 합니다**. 다만, 부활(효력회복)계약의
    암보장개시일은 부활(효력회복)일을 포함하여 90일이 지난 날의 다음 날로 합니다」
    [S7, 별표 1 주2].
- **Four carve-outs from the waiting period are retrieved, and they matter:**
  1. **유사암 have no waiting period.** 「유사암의 보장개시일은 계약일임」 [S1]; the 면책기간
     table marks 유사암 진단비 as `×` [S1] [S2]; 「갑상선암 치료보험금ㆍ기타피부암 …ㆍ
     제자리암(상피내암) …ㆍ경계성종양 치료보험금 — [면책기간] `-`」 [S7]. One carrier is
     the exception and does apply the wait to 갑상선암 [S3].
  2. **Renewal contracts have no waiting period.** 「갱신계약의 경우 갱신일로 합니다」 [S4]
     [S7]; 「※ 갱신계약의 경우 면책기간을 적용하지 않습니다」 [S2].
  3. **Lives under 15 have no waiting period.** 「단, 보험계약일 기준으로 피보험자의
     보험나이가 **15세 미만**인 경우에는 보험계약일을 보장개시일(책임개시일)로 합니다」
     [S2]. The institute records the same convention: 「피보험자의 나이가 15세 미만인 경우
     등에는 위 90일의 부담보기간을 적용하지 않고 제1회 보험료 납입일로부터 보장이
     개시되도록 하는 것이 일반적」 [R3], and the supervisor names 어린이암보험 as the
     exception [R6].
  4. **Whole products without a waiting period exist.** 「첫날부터라이나암보험」 has no
     면책기간 block in its summary at all, and 제26조 defines 보장개시일 as the day the first
     premium is received, adding 「또한, 보장개시일을 계약일로 봅니다」 [S6]. The trade press
     records this as a product category [R3, footnote 27].
- **Reinstatement restarts the clock.** 「부활(효력회복)일을 포함하여 90일이 지난 날의
  다음 날로 합니다」 [S1] [S3] [S7]. One contract adds the under-15 carve-out to
  reinstatement too: 「다만, 부활(효력회복)일을 기준으로 피보험자의 보험나이가 15세 미만인
  경우에는 부활(효력회복)일을 보장개시일(책임개시일)로 합니다」 [S2].

### 7. Diagnosis inside the waiting period: 무효, not merely unpaid

- The statutory hook is 상법 제644조: 「보험계약당시에 보험사고가 이미 발생하였거나 또는
  발생할 수 없는 것인 때에는 그 계약은 **무효**로 한다. 그러나 당사자 쌍방과 피보험자가
  이를 알지 못한 때에는 그러하지 아니하다」 [R7].
- 「피보험자가 암보장개시일 전에 암으로 진단 확정되는 경우에는 **보험계약이 무효**가 되며
  보험회사는 보험계약자에게 기납입보험료를 반환한다」 [R3].
- The retrieved 약관 implement it at the level of the **individual benefit**, not the whole
  contract, which is a material refinement:
  - 「피보험자가 보험계약일부터 …암에 대한 보장개시일(책임개시일)의 전일 이전에 …「암」으로
    진단확정되는 경우에는 …**암 진단비(유사암 제외)계약을 무효로 합니다**」 [S1] 제28조제2항.
  - 「제2항에 따라 …암 진단비(유사암 제외) 계약이 무효가 된 경우, 계약자는「암」의
    진단확정일부터 **90일 이내에** 무효가 된 계약 이외의 계약을 취소할 수 있으며, 해당
    계약은 그 때부터 효력이 없습니다」 [S1] 제28조제3항 — an option, not an automatic
    unwinding: the rest of the contract survives unless the policyholder kills it.
  - 「보험계약일부터 암, 5대 주요암 및 10대 주요암의 보장개시일 전일 이전에 암으로
    진단확정되는 경우 해당 보장(특별약관)은 무효로 하며, 이미 납입한 해당 보장(특별약관)의
    보험료를 돌려드립니다」 [S1].
- **Premiums are returned** — with interest at the 보험계약대출이율 compounded annually
  where the insurer was at fault or knew of the invalidity and did not refund [S1] [S3].
- The waiting period reaches **forward** as well: where a cancer diagnosed before the
  암보장개시일 later recurs or metastasises, the premium waiver is refused —
  「계약자가 …보험계약일부터 암보장개시일 전일 이전에「암」이 발생하였으나 계약자가 이
  계약의 취소를 선택하지 않은 경우에 그「암」이 동일하거나 다른 신체기관에 **재발 또는
  전이**되어 …납입면제 사유가 발생하였을 때」 the waiver does not apply [S1] 제9조제2항.
- The 금감원 분쟁조정 line is the same on benefits: a bone metastasis diagnosed two years
  after a breast cancer that had been diagnosed **inside** the waiting period is not
  「암보장개시일 이후에 최초로 진단 확정된 암」 and is not payable (분쟁조정 제2003-64호)
  [R3].
- By contrast a **genuine recurrence after clinical cure** is a new cancer. Where the
  insured had been treated for a palate cancer in 2001, followed up to 2003, insured in
  2006 and diagnosed again in 2008, the committee held that 「마지막 추적관찰 이후 약 5년
  6개월간 치료 사실이 없다가 암이 재발한 것이므로 … 통상 의학적으로 완치란 5년 이내에
  재발이 없는 경우를 의미하므로 … 보험 가입 이후 새로운 암으로 진단을 받은 것으로 보아
  암보험금 지급 대상에 해당한다」 (제2009-32호) [R3].
- Summary of the committee's two rules: 「분쟁조정위원회는 일반적으로 암이 **전이**된
  경우에는 원발암이 진행된 것으로 보아 원발암 기준으로 판단을 하고, 암이 치료되었다가
  **재발**한 경우에는 새로운 암으로 보는 입장인 것으로 이해된다」 [R3].

### 8. 감액기간: the reduced-benefit period

- The rule as the institute states it: 「암보장개시일이 지났더라도 통상 피보험자가 **보험
  계약일 이후 1년 또는 2년 이내**에 암으로 진단 확정 받은 경우에는 암보험금의 **50%**만
  지급하는 것이 일반적이며, 일부 암보험 상품의 경우 자가진단이 용이한 **유방암**은
  암보장개시일부터 **90일 이내**에 진단 확정 시 암보험금의 **10%**를 지급하기도 한다」 [R3].
  The supervisor states the same 1–2 year / 50% rule [R6].
- **Retrieved 감액 wordings and periods:**
  - **1 year, 50%, applied to almost everything** — 삼성화재 2018: 「최초 보험가입 후 1년
    미만에 보험금 지급사유가 발생한 경우 50% 감액 지급합니다」, listed against 23 named
    benefits including 암 진단비(유사암 제외), 유사암 진단비, 5대/10대 주요암 진단비,
    암 최초수술비, 암 수술비, 유사암 수술비, 항암방사선·약물 치료비 and the 뇌·심 riders
    [S1]. Notably **excluded** from the reduction are 암 직접치료 입원일당 and the
    기타피부암/갑상선암 limbs of 암 사망 및 고도후유장해 [S1].
  - **1 year, 50%, on 유사암 only** — 삼성화재 2026: the 감액지급 table lists 유사암 진단비,
    항암 양성자방사선 치료비, 항암 세기조절방사선 치료비 and 표적항암약물허가 치료비 at
    「가입후 1년간 보험금 50% 지급」, and **암 진단비(유사암 제외) does not appear in the
    table at all** [S2]. Reading its rider article confirms it: 「…「암」으로 진단확정되었을
    때에는 최초 1회에 한하여 보험증권에 기재된 이 특별약관의 보험가입금액을 암 진단비(유사암
    제외)로 …지급합니다」, with no 경과기간 split [S2].
  - **2 years, 50%, on everything** — 한화생명: 「계약일부터 2년 미만에 …보험금 지급사유가
    발생한 경우 계약일부터 2년 이후 보험금 지급사유 발생시 지급하는 …진단자금의 **50%**를
    지급합니다」 [S3] 제14조제9항, and the same in 별표 1's 경과기간 columns [S3] [S4] [S5].
  - **2 years, 50%** — 라이나 퍼펙트케어 [S7]; **1 year, 50%** — 라이나 첫날부터 [S6].
  - **A two-step reduction** — 삼성화재 2026's 암 다빈치로봇 수술비: 「가입후 180일 미만 :
    보험금 25% 지급 / 가입후 1년간(180일미만제외) : 보험금 50% 지급」 [S2]; 한화's robot
    module does the same on a 2-year outer period: 「2년미만 500만원 ※ 단, 계약일부터
    180일 이내 암 다빈치로봇 수술시 250만원 / 2년이상 1,000만원」 [S5].
- **The clock's endpoints are stated and they differ by benefit type.**
  - Diagnosis benefits: 「지급금액의 경과기간은 **보험계약일부터 진단 확정일까지**의
    경과기간입니다」 [S3, 별표 1 주2].
  - Surgery benefits: 「지급금액의 경과기간은 보험계약일부터 **수술일**까지의 경과기간을
    말합니다」 [S4] [S5].
  - And the general statement: 「감액기간은 보험계약일로부터 진단 확정일(진단자금의 경우에
    해당하며, 진단자금 외 담보의 경우 본 상품의 약관 본문을 참고하시기 바랍니다)까지의
    경과기간입니다」 [S5].
  - The date of diagnosis is itself defined: 「이 경우 …의 진단확정 시점은 **상기 검사에 의한
    결과보고 시점**으로 합니다」 [S3] [S4] [S2] — the pathology report, not the certificate.
    A carrier tells consumers the same thing: 「암 진단 시점은 진단서 발급일이 아닌 '조직
    검사 결과 보고일'이므로 암 진단 일이 면책 기간이나 감액 기간에 해당하는지도
    확인하세요」 [S10].
- **The 감액 does not apply on renewal.** 「※ 갱신계약의 경우 감액지급을 적용하지 않습니다」
  [S2]; 「상기 보험금 지급기준표의 내용 중 계약체결 후 2년 미만의 보험금 감액과 관련한
  사항은 갱신계약의 경우에는 적용하지 않습니다」 [S4]; 「※ 갱신계약은 감액지급이 없습니다」
  [S6] [S7]; and the 갱신 column of one table prints 「이 특별약관 보험가입금액의 100%」
  flat [S2].
- Consequence for modelling: on a 갱신형 contract the 면책 and 감액 devices bite **only in
  the first policy term**, never again, so their present-value effect is confined to the
  first 10 or 15 years of a 100-year projection. On a 비갱신형 contract they bite once, at
  the start. Either way they are a **first-two-years** phenomenon and cannot be modelled as
  a permanent benefit scaling.

### 9. 진단확정: who may diagnose, on what evidence, and when

- The standard wording, given by the institute as the market form: 「암의 진단 확정은
  **병리과 또는 진단검사의학과 전문의 자격증을 가진 자**에 의하여 내려져야 하며, 이 진단은
  **조직(Fixed Tissue) 검사, 미세바늘흡인(Fine Needle Aspiration) 검사 또는
  혈액(Hemic System) 검사에 대한 현미경 소견**을 기초로 하여야 합니다. 그러나 상기에 따른
  진단이 가능하지 않을 때에는 피보험자가 암으로 진단 또는 치료를 받고 있음을 증명할 만한
  문서화된 기록 또는 증거가 있어야 합니다」 [R3].
- Every retrieved contract carries it in substantially those words [S1] [S2] [S3] [S4]
  [S5] [S6] [S7]. Two refinements appear in the newer ones:
  - the **timing** rule already quoted — 진단확정 시점 = 검사에 의한 결과보고 시점 [S3] [S4];
  - an explicit statement of when the fallback opens: 「【'제2항에 따른 진단이 가능하지
    않을 때' 예시】 - 피보험자가 조직검사 등 병리학적 검사를 받을 여유없이 급속한 병증
    악화로 사망한 경우 - 종양의 발생부위 및 피보험자의 신체상태 등의 이유로 조직을 추출하는
    경우 생명의 위험을 초래할 수 있어 병리학적 검사를 시행할 수 없는 경우」 [S3] [S4], and
    the exclusion of a 사체검안서 from the acceptable documentary record [S3].
- The older wording accepted clinical diagnosis more readily — 「그러나 상기의 병리학적
  진단이 가능하지 않을 때에는 암에 대한 **임상학적인 진단이 암의 증거로 인정됩니다**」 —
  and was tightened to the present form [R3, footnote 30]. The practical consequence is
  spelled out: 「임상의사가 암으로 진단하더라도 암보험금 지급 대상에 해당하지 않는 상황도
  생길 수 있으므로 유의할 필요가 있다」 [R3].
- **Third-opinion machinery** is in every contract, and the insurer pays for it: 「보험금
  지급사유에 대해 보험수익자와 회사가 합의하지 못할 때는 …함께 제3자를 정하고 그 제3자의
  의견에 따를 수 있습니다. 제3자는 의료법 제3조(의료기관)에 규정한 **종합병원 소속
  전문의** 중에 정하며, 보험금 지급사유 판정에 드는 의료비용은 **회사가 전액 부담**합니다」
  [S1] [S2] [S3]. 의료법 제3조의3's 종합병원 threshold — 100 beds and 7 or 9 named
  specialties with resident consultants — is reproduced in the 약관 and in [R3] footnote 28.
- **Post-mortem crystallisation**: where the insured dies during the policy term and the
  cancer is only then established as the direct cause, 「그 사망일을 진단 확정일로 보고」 the
  benefit is paid, less any 책임준비금 or 계약자적립액 already paid out [S1] [S3] [S4].

### 10. 원발부위 기준: C77–C80 and the 2011-04-01 supervisory change

- The problem: a primary cancer that has spread picks up a **secondary-site code** as well
  as its own. If the primary is a low-tier cancer (C73 갑상선) and the secondary code is a
  general-tier one (C77 림프절의 이차성 및 상세불명의 악성 신생물), which tier pays?
- 「특히 갑상선암이 인접 부위 림프절에 전이된 경우에 대한 분쟁이 다수 발생하였다 …
  한국표준질병·사인분류상 갑상선암에 대해 부여되는 C73 코드 외에 **C77** 코드가 병기되는
  경우가 있으며, 이 때에 원발암인 C73 코드를 기준으로 소액암보험금을 지급해야 하는지
  아니면 C77 코드에 따라 일반암보험금을 지급해야 하는지가 문제된 것이다」 [R3].
- **The FSS dispute committee sided with the primary site.** In 제2014-12호 the insured had
  a 갑상선 좌엽절제술 and central-compartment node dissection, coded C73 and C77; at stake
  was 갑상선암 진단비 **₩3,000,000** against 일반암 진단비 **₩30,000,000** [R3]. Taking
  advice from 대한갑상선학회 and 대한병리학회, the committee held that C77 「원발암 수술
  시에 동시에 발견된 주변 림프절 전이의 경우에 사용하는 코드가 아니며 … C73 단일 코드로
  진단하는 것이 표준」, that dual coding shows 「갑상선암의 '진행 상태'」 rather than two
  cancers, and that **중앙암등록본부's own registration** counts such a case as one cancer,
  C73 [R3].
- **The courts split.** For the primary site: 대구지방법원 2013. 8. 29. 선고
  2013가합201756 — 「전이암은 '별도의 질환'이 아니라 암의 '진행 정도'를 나타내는 것에
  불과하다」 [R3]; 서울중앙지방법원 2014. 8. 20. 선고 2013가단165064 — the tier difference
  reflects 「갑상선암의 발병 빈도·치료 난이도·비용·완치율」 [R3]. For the general tier, on
  the **contra proferentem** ground (작성자 불이익 원칙): 서울남부지방법원 2015. 7. 24.
  선고 2014나50673, reversing the first instance, because 「'한국표준질병·사인분류 질병코딩
  지침서'에서 명확한 기준을 제시하지 않고 있음」 and specialists themselves disagreed [R3];
  부산지방법원 2015. 5. 14. 선고 2013나44321, 2014나7992 [R3]. **No Supreme Court decision
  on this point existed as at the report's date** [R3].
- **The supervisor closed the question prospectively.** 금융감독원 보도자료 2011-03-14
  「소비자 권익 보호를 위한 보험약관 개선」 required 「이차성 암에 대한 보험금 지급기준
  합리화」 to be written into 약관 **from 2011년 4월 1일**: where the primary site is
  identifiable, the primary decides the benefit, and the risk rate must be set accordingly
  — 「예를 들어 갑상선의 악성 신생물(C73)과 림프절의 이차성 및 상세불명의 악성
  신생물(C77) 중 갑상선을 원발부위로 하는 경우를 갑상선암에 모두 포함한 위험률을 적용하라는
  것임」 [R3, footnote 89]. **That is a direct instruction about the pricing basis, and it
  is the reason a Korean 일반암 incidence rate is the rate for cancer *excluding* C44 and
  C73 by primary site — which is exactly the table [R5] publishes.**
- The resulting 약관 clause is in every retrieved contract, in two generations of wording:
  - 2018: 「한국표준질병·사인분류 지침서의 "사망 및 질병이환의 분류번호부여를 위한 선정준칙과
    지침"에 따라 **C77~C80**(불명확한, 이차성 및 상세불명 부위의 악성신생물(암))의 경우
    일차성 악성신생물(암)이 확인되는 경우에는 **원발부위(최초 발생한 부위)를 기준으로
    분류합니다**」 [S1].
  - 2024–25, with a timing rider and worked examples: 「…다만, 이 경우에도 C77~C80…의
    **진단확정 시점은 원발암 진단확정 시점으로 변경되지 않습니다**. 【원발부위 기준 예시】
    · C73(갑상선의 악성신생물)이 림프절로 전이되어 C77…로 진단된 경우에도 C73…에 해당하는
    질병으로 봅니다. · C50(유방의 악성신생물)이 폐로 전이되어 C78.0…로 진단된 경우에도
    C50…에 해당하는 질병으로 봅니다. · C16(위의 악성신생물)이 뇌로 전이되어 C79.3…로
    진단된 경우에도 C16…에 해당하는 질병으로 봅니다」 [S3] [S4] [S5].
  - The 2026 non-life edition adds a carve-out: the timing rule does not hold 「원발부위의
    암이 완치되었다면」 [S2].
- A distinct and older committee decision points the other way on **which** cancer is "the
  first": where an ovarian cancer turned out to be a Krukenberg tumour secondary to a
  gastric primary, 「최초로 진단 확정된 암의 의미는 **원발성 암**을 의미하는 것으로
  해석하는 것이 타당하다」, so the higher 다발성암보험금 ₩70,000,000 was payable rather than
  the ₩30,000,000 (제2000-54호) [R3]. The primary-site rule therefore cuts both ways.
- **Underwriting exclusions follow the primary too.** Where a 특정부위 부담보 특약 excluded
  the thyroid and a thyroid cancer later spread to cervical nodes coded C77, the committee
  held there was no liability, because the node cancer 「갑상선암에서 전이된 것이므로
  갑상선암을 직접적인 원인으로 한 것」 and a metastasis is not a 합병증 (제2006-71호) [R3].

### 11. KCD reclassification between inception and diagnosis

- The asymmetric old wording produced the litigation. Older 약관 said only that a disease
  **added** to the malignant list by a later KCD revision would be included; they said
  nothing about a disease **removed** from it.
- Where a borderline-malignant serous cystadenoma was M8442/3 (C56, malignant) under KCD-4
  (시행 2003-01-01) and became M8442/1 (D39.1, borderline) under KCD-5 (시행 2008-01-01),
  the committee applied the **contract-date** classification and paid the full cancer
  benefit, reasoning that the extension clause 「악성 신생물의 범위보다 그 범위가 '확장'되는
  경우만을 예상하여 …적용을 긍정하는 것이지, 반대로 …'축소'되는 경우는 전혀 예정하고 있지
  않으므로」, so contra proferentem applied (제2012-14호) [R3].
- The mirror case: 랑게르한스세포 조직구증 was D76.0 (경계성종양, ₩4,000,000 paid) when
  diagnosed in 2010-08, and was moved to **C96** by KCD-6 (시행 2011-01-01); the committee
  allowed the full cancer benefit of ₩50,000,000 retrospectively, again on contra
  proferentem (제2011-35호) [R3].
- The Supreme Court set the interpretive rule in a 직장유암종 case: 「보험계약 체결 당시
  고시된 한국표준질병·사인분류에 따라 암에 해당하는지를 정하되, 보험계약 체결 당시에는 악성
  신생물로 보지 않던 것이라도 보험사고의 발생 시점, 즉 **해당 질병의 진단확정 시**를
  기준으로 가장 최근에 개정·고시된 한국표준질병·사인분류에서 새롭게 악성 신생물로 포함하면,
  이를 악성 신생물로 보아 보험금을 지급하겠다는 의미로 보아야 한다」 (**대법원 2018. 7. 24.
  선고 2017다256828 판결**) [R3]. A lower court added that narrowing the old scope by a
  later revision 「특별한 이유 없이 종전의 보장 범위를 좁히는 것으로서 계약자에게 불리하여
  허용될 수 없다」 (서울중앙지방법원 2019. 1. 11. 선고 2018나50361) [R3].
- KIRI recommended the symmetrical wording: 「향후에는 암보험 약관을 개정하여, …'추가'되는
  경우뿐만 아니라 '제외'되는 경우도 포함시켜서, **진단 시점의 기준에 따라 판단한다는 내용을
  약관에 명시**하는 방안을 고려해볼 필요가 있을 것」 [R3]. The retrieved 2024–25 contracts
  do exactly that [S3] [S4] — see §3 — which is a documented case of research feeding
  through into policy wording within five years.
- Note the 약관 in [R3]'s report cited the **제7차** KCD (통계청 고시 제2015-309호,
  시행 2016-01-01) as the then-current basis [R3]; the retrieved contracts cite the
  **제8차** (통계청 고시 제2020-175호, 시행 2021-01-01) [S3] [S4].

### 12. 재진단암: the repeating diagnosis benefit

- The benefit exists as a rider or module, not as part of the base cover, in every retrieved
  contract that has it [S1] [S8].
- The market convention is **2 years**: 「일반적으로 첫 번째 재진단암은 최초로 발생한 암의
  진단확정일부터 그 날을 포함하여 2년이 지난날의 다음날, 두 번째 이후 재진단암은 직전
  재진단암 진단확정일부터 그 날을 포함하여 2년이 지난날의 다음날을 보장개시일로 정하고 있는
  경우가 많다」 [R3].
- Retrieved verbatim [S1]:
  「※「재진단암」의 보장개시일 — 1. 첫 번째 재진단암 : 「최초암」(기타피부암, 갑상선암,
  대장점막내암 제외) 보장개시일 이후 발생한 최초암의 진단확정일부터 그날을 포함하여 **2년이
  지난날의 다음날**임 2. 두 번째 이후 재진단암 : 직전 재진단암의 진단확정일부터 그날을
  포함하여 **2년이 지난날의 다음날**임」, with the underlying 최초암 보장개시일 still the
  day after 90 days [S1]. Excluded from 재진단암 on that contract: 기타피부암, 갑상선암,
  **전립선암**, 대장점막내암 [S1].
- The four qualifying events are defined, and the definitions are worth having because they
  are what a multi-decrement model would have to represent [S8]:
  - **새로운 원발암** — 「원발부위에 발생한 암으로「첫번째암…」 또는「재진단암…」과
    **다른 조직병리학적 특성**(Histopathological Appearance)을 가진「암…」」;
  - **전이암** — 「원발부위의 암세포가 새로운 장소로 퍼져(침윤 또는 원격전이) 다시 그곳에서
    자리를 잡고, 계속적인 분열과 성장과정을 거쳐 증식하는「암…」」;
  - **재발암** — 「…과 **동일한 조직병리학적 특성**을 가진 암으로서 치료를 통해 몸에서
    …암세포를 제거한 후 그 …으로 인하여 새롭게「암」이 출현되어 치료가 필요한 상태로
    판명된「암」」;
  - **잔여암** — 「「암보장개시일」이후 발생한「암…」 진단부위에 **암세포가 남아 있는**
    경우」 [S8].
- Two termination rules make the rider finite [S8]: if the first cancer has not been
  diagnosed and fewer than 2 years of the policy term remain, the rider lapses; and if a
  재진단암 is diagnosed with fewer than 2 years remaining, the rider lapses.
- The base contract's own diagnosis benefit is **최초 1회한** in every retrieved case
  [S1] [S2] [S3] [S4] [S6] [S7]. The market's phrase for the frequency of the repeating
  rider is 「매 1~2년마다」 [S10], but **no retrieved contract carries a 1-year cycle** —
  every retrieved 재진단암 clause is 2 years [S1] [S8]. A 1-year cancer re-diagnosis cycle
  is therefore `[unverified]`.
- A separate, shorter cycle does exist for the cardiovascular riders that sit beside the
  cancer cover — 「두 번째 뇌출혈」 and 「두 번째 급성심근경색증」 both run on **1 year** from
  the first diagnosis [S1] — so the 1-year machinery exists in the market but not, on the
  evidence retrieved, for cancer.

### 13. 암 수술비: the surgery benefit

- Structure: retrieved contracts write it either as **최초 1회한** (암 최초수술비) or as
  **수술 1회당** (암 수술비), and one carrier sells both riders and requires them to be
  bought together [S1].
- Amount: 「가입금액」 per qualifying surgery [S1] [S2]. The 갱신형 module version splits by
  invasiveness at a **5:1 ratio**: at 보험가입금액 500만원, 「2년이상 — 관혈수술 1회당
  500만원 / 비관혈수술 1회당 100만원」, halved inside the 2-year 감액기간 [S4].
- **What counts as 수술** is defined by a 수술분류표 plus a general clause and a standard
  exclusion list [S4]:
  「'수술'은 기구를 사용해서 생체(生體)에 절단(切斷…), 절제(切除…) 등의 조작(操作)을
  가하는 것(보건복지부 산하 **신의료기술평가위원회**로부터 안전성과 치료효과를 인정받은 최신
  수술기법도 포함됩니다)을 말합니다. 다만, **흡인(吸引…), 천자(穿刺…) 등의 조치 및
  신경 BLOCK, 미용 성형상의 수술, 피임 목적의 수술, …검사 및 진단을 위한 수술[생검, 복강경
  검사 등], 발정술 등 내고정물제거술은 '수술'에서 제외**합니다」 [S4]. The institute
  describes the same list as the market norm and adds 항암방사선치료와 항암약물치료 to the
  exclusions [R3] — those are separately covered, see §15.
- **관혈 / 비관혈** are defined: 「'관혈수술'이라 함은 …병변 부위를 육안으로 직접 보면서
  수술적 조작을 하기 위해 피부에 절개를 가하고 병변 부위를 노출시켜서 수술을 하는 것」, and
  「대뇌내시경, 흉강경수술, 복강경수술 및 조혈모세포이식수술은 **관혈수술에 준합니다**」
  [S4]. Where both are performed in one operation only the 관혈 amount is paid [S1].
- **Robot surgery is a separate, higher-paying module** in the newest contracts —
  「암 다빈치로봇 수술자금」 [S2] [S5], with its own two-step 감액 (§8).
- The institute notes the older market shape: 「통상 수술 1회당 일정액으로 보험금을 지급하며,
  최초 1회의 수술에 한하여 암수술비를 지급하는 상품도 있다 … 보험상품에 따라서는 수술의
  종류를 구분하여 보험금의 액수를 차등화하는 경우도 있으며」, with 내시경수술 or
  카테터수술 paying less than 관혈수술 [R3, footnote 19].

### 14. 암 입원일당: the daily inpatient benefit, and 요양병원

- Amount and limit: 「암 직접치료 입원일당(1일이상) — …암의 직접적인 치료를 목적으로
  병·의원 등에 1일이상 계속 입원하여 직접적인 치료를 받은 경우 (**180일을 한도로 입원1일당**
  일당 지급) … 가입금액 ※ 단, 기타피부암, 갑상선암, 대장점막내암, 제자리암, 경계성종양은
  **가입금액의 20%**」 [S1].
- The 갱신형 module version is tighter still: 「…**2일 이상** 상급종합병원에서 입원하였을
  경우(**1회 입원당 지급일수 120일 한도**) — 2년이상 **1일초과 1일당** 5만원」 at
  보험가입금액 5만원 [S4]. So the first day is not paid, the stay must be at a
  상급종합병원, and the cap is 120 days per stay.
- The institute's description of the market: 「지급일수는 **1회 입원당 120일 또는 180일**을
  한도로 하는 경우가 많으며, 피보험자가 동일한 암의 치료를 목적으로 보험기간 중에 2회 이상
  입원한 경우에는 이를 1회 입원으로 보아 입원일수를 합산하여 계산한다. 다만 암입원비가
  지급된 최종 입원의 퇴원일부터 **180일이 경과하여 개시한 입원은 새로운 입원**으로 보며,
  암입원비가 지급된 최종 입원일부터 180일이 경과하도록 계속 입원 중인 경우에는 암입원비가
  지급된 최종 입원일의 그 다음날을 퇴원일로 본다」 [R3]. Some contracts additionally require
  **4일 이상** continuous inpatient stay, paying either from day 4 or from day 1 [R3,
  footnote 18]; a retrieved product page carries exactly that form —
  「[갱신형]암직접치료(요양병원제외)입원비 (4일이상)」 and 「[갱신형]요양병원 암입원비
  (4일이상)」 as **two separate riders** [S8].
- **This is the most disputed benefit in the Korean market.** 「암보험 약관에서는 …그 암의
  치료를 **직접적인 목적**으로 하여 입원한 경우에 암입원비 급부를 지급하도록 규정하고
  있는데, 암 환자가 암치료를 받은 후 **요양병원**에 입원한 경우에 이것이 '암의 치료를
  직접적인 목적으로 하여 입원을 한 경우'에 해당하는지에 대해 소비자와 보험회사 사이에서
  다툼이 발생한 것이다 … 금융감독원에 따르면 **2018년에 암입원비와 관련하여 2,125건의
  민원**이 제기되었고, 이는 생명보험회사에 대한 민원이 전년 대비 크게 증가하는 원인이 되기도
  하였다」 [R3, citing 금융감독원 보도자료 2019-04-30]. By 2019-08 the FSS had a dedicated
  보험분쟁조정 TF receiving 60–90 new 요양병원 입원비 complaints a week [R3, footnote 4,
  citing 파이낸셜뉴스 2019-08-08].
- The market's structural answer is visible in [S2] and [S8]: the benefit is now **split**
  into 「암 직접치료 입원일당Ⅱ(1일이상)(요양병원 **제외**)」 and 「암 요양병원 입원일당Ⅱ
  (1일이상, **90일한도**)」 — two riders, two prices, and the convalescent-hospital limb
  separately and much more tightly capped [S2].
- A carrier still warns consumers about it: 「치료 후 후유증 완화나 합병증 치료 목적의 입원은
  보험 약관과 법원 판례가 서로 달라 암 입원비가 지급되지 않을 수 있으므로 사전에 확인이 반드시
  필요」 [S10].
- 유사암 are paid the inpatient benefit at **20% of the daily amount** where they are paid at
  all [S1], and one contract excludes them from the 감액 while applying the 면책기간 only to
  invasive cancer [S1].

### 15. 항암방사선치료비 / 항암약물치료비

- These are **treatment-event benefits, not per-cycle or per-month benefits**, in every
  retrieved contract: 「(단, 최초 1회한)」 [S4] [S5], or 「최초 1회한 지급」 [S1]. That is a
  sharp structural contrast with Japan, where the chemotherapy benefit is typically paid per
  qualifying calendar month with a lifetime month cap.
- Definitions, verbatim [S4]:
  - 「'항암약물치료'라 함은 …해당 진료과목의 전문의 자격증을 가진 자가 피보험자의 '암',
    '암(기타피부암 및 갑상선암 제외)'의 직접적인 치료를 목적으로 **항암화학요법 또는
    항암면역요법**에 의해 항암약물을 투여하여 치료하는 것을 말합니다. 단, 항암면역요법이란
    면역기전을 이용해서 암세포를 제거하는 치료를 말하며, **암세포가 없는 상태에서 면역력을
    증가시키는 약물(압노바, 헬릭소, 셀레나제 등) 치료는 제외**됩니다」 [S4].
  - 「'항암방사선치료'라 함은 **방사선종양학과 전문의** 자격증을 가진 자가 …직접적인 치료를
    목적으로 **고에너지 전리 방사선(Ionizing Radiation)**을 이용하는 치료법을 말합니다」 [S4].
- The named exclusion of 압노바 / 헬릭소 / 셀레나제 is the same immune-support therapy that
  drove the 요양병원 disputes [R3], written into the definition so the argument cannot be had
  again.
- **Two-tier structure.** The rider pays a higher amount where the underlying cancer is
  invasive and a lower one where it is any cancer including C44/C73, at 보험가입금액 1,000만원
  [S4]:

  | 세부보장 | trigger | 2년미만 | 2년이상 |
  |---|---|---|---|
  | 항암약물치료자금Ⅰ | 암(기타피부암 및 갑상선암 제외) | 500만원 | 1,000만원 |
  | 항암약물치료자금Ⅱ | 암 (all, incl. C44/C73) | 125만원 | 250만원 |
  | 항암방사선치료자금Ⅰ | 암(기타피부암 및 갑상선암 제외) | 500만원 | 1,000만원 |
  | 항암방사선치료자금Ⅱ | 암 (all) | 125만원 | 250만원 |

  The Ⅱ limb at **25%** of the Ⅰ limb is the same 유사암-style discount applied to a
  treatment benefit rather than to a diagnosis benefit [S4].
- The non-life form applies the discount inside a single rider instead:
  「항암방사선·약물 치료비 — …가입금액 ※ 단, 기타피부암, 갑상선암은 **가입금액의 20%**」
  [S1], with a 90-day 면책 on 암 and none on 기타피부암·갑상선암 [S1].
- The newest edition splits the modality much further —
  「항암 양성자방사선 치료비 / 항암 세기조절 방사선 치료비 / 표적항암약물허가 치료비 /
  항암 중입자방사선 치료비 / 항암 방사선 치료비」 as five separate named riders, each with
  its own 면책 and 감액 [S2]. Three of them carry a 1-year 50% 감액 where the plain
  항암방사선·약물 치료비 does not [S2].

### 16. 암 사망, 납입면제 and the death cover that mostly is not there

- **암 사망** survives only as an optional rider. 「암 사망 및 고도후유장해 — 보장개시일 이후
  암, 기타피부암 또는 갑상선암으로 진단확정되고 그 …으로 인하여 사망 또는 **80% 이상
  후유장해**가 발생한 경우 … ※ 대장점막내암은 암에 포함되며, **제자리암 및 경계성종양은
  지급사유에서 제외**됨」 [S1]. It carries the 90-day wait on 암 only, and the 1-year 50%
  감액 on 암 only [S1].
- On the life-insurer contracts there is **no death benefit at all**; death simply ends the
  contract and returns the accumulated fund: 「피보험자가 보험기간 중 사망한 경우에는
  계약자에게 사망 당시의 **계약자적립액**을 지급하여 드리고 이 계약은 그 때부터 효력이
  없습니다」 [S3] 제31조제1항, and the same in [S4] [S5] [S6] [S7].
- **보험료 납입면제** is a defining feature and its trigger set is narrow and explicit:
  - 「피보험자가 보험료 납입기간 중 보장개시일…이후 최초로 '암(직·결장암, 유방암,
    여성생식기암, 전립선암, 기타피부암, 갑상선암, 대장점막내암 제외)' 또는 '중증 갑상선암'
    으로 진단이 확정되거나 장해분류표 중 동일한 재해 또는 재해 이외의 동일한 원인으로 여러
    신체부위의 장해지급률을 더하여 **50% 이상** 장해상태가 되었을 경우에는 차회 이후 보험료
    납입을 면제하여 드립니다. 그러나, **특정 소액암, 기타피부암, 갑상선암(다만, '중증
    갑상선암'은 제외합니다), 대장점막내암, 제자리암 또는 경계성종양으로 진단이 확정되었을
    경우에는 보험료 납입을 면제하여 드리지 않습니다**」 [S3] 제14조제1항.
  - The non-life form waives on 암 (유사암 제외), 뇌출혈 or 급성심근경색증 [S1] 제9조제1항,
    and 「유사암(기타피부암, 갑상선암, 대장점막내암, 제자리암 및 경계성종양)은 납입면제
    사유에서 제외됨」 [S1].
- **On a renewable contract the waiver does not survive renewal.** 「보험료 납입이 면제된
  이후에 …계약을 갱신하는 경우 보험료 납입은 **더 이상 면제되지 않으며**, 계약자는 갱신된
  계약의 보험료를 납입하여야 합니다」 [S4]. And a waiver granted for one cancer is not
  granted again on the renewed contract for the same cancer — 「이미 보험료의 납입을 면제한
  질병의 종양세포가 잔존하거나 재발 또는 전이된 경우」 — unless **5 years** pass from the
  first renewal's 보장개시일 with no further diagnosis or treatment, after which the same
  cancer can trigger the waiver again [S4]. That five-year rule is a clean, dated,
  contractual definition of "cured" and is the only one retrieved.
- 「이 상품의 사업방법서 별지에 따라 납입면제를 적용하지 않거나 보통약관에서 보험료 납입면제에
  대해 정하지 않은 경우 …제5조(보험료 납입면제) 및 제6조…를 적용하지 않습니다」 [S2] — the
  waiver is switched on and off by the **사업방법서**, not by the 약관, so its presence
  cannot be read off the policy conditions alone.

### 17. 갱신형 vs 비갱신형

- Both forms are in the market for the same cover and the retrieved documents show both.
  갱신형: [S4] [S6] [S7] [S8], and the 재가입형 15-year non-life form [S1] [S2].
  비갱신형: [S3] [S5].
- The renewal mechanics, verbatim [S4] 제2-11조의6:
  - 「① 계약자가 이 계약의 보험기간 만료일 **15일전까지** 이 계약을 계속 유지하지 않는다는
    뜻을 회사에 통지하지 않으면 이 계약은 갱신되어 계속 유지되는 것으로 합니다」 — silence
    renews.
  - 「② 최종 갱신계약의 보험기간 종료일은 피보험자의 **100세 계약 해당일**로 합니다」.
  - 「④ 갱신계약의 보험료는 **갱신일 현재 피보험자의 나이 및 갱신할 때의 보험요율(이율,
    계약체결비용, 계약관리비용, 위험률 등)**을 적용하여 계산하며, 나이의 증가, 위험률의
    변동 등의 사유로 인하여 변동될 수 있습니다」 — attained-age re-rating on the then-current
    basis, i.e. **the renewal premium is a function of the renewal index, not of the policy
    year**.
  - 「⑤ …보험료가 변경되는 경우에는 …만료일 **30일 전까지** 계약자에게 관련 내용(구체적인
    보험료 변동 내용 및 **과거 갱신보험료 변동 내역** 등)을 …안내하여 드립니다」.
  - 「⑥ 갱신계약의 보험가입금액은 갱신 전 계약과 **동일**하게 적용됩니다」.
  - 「⑧ …보험기간 중 …보험금이 지급된 세부보장은 **갱신되지 않으며**, 나머지 세부보장에
    대해서는 제1항 내지 제6항을 적용합니다」 — a module that has paid its once-only benefit
    drops out of the contract at the next renewal.
- Renewal terms observed: **10년** [S8] (with 30–80세 renewing on a 10-year term and 81–89세
  on a 1–9 year term to fit the outer age); **1~10년** stated as the range [S8]; 라이나's
  퍼펙트케어 renews to a **100세 만기** once the insured passes 가입나이 85 [S7].
- The 재가입 form (non-life) is different again and is the analogue of the 실손 mechanism:
  a 15-year policy term with 재가입 at expiry into 「회사가 판매하는 재가입형 상품」, with a
  guarantee that even on refusal the policyholder may re-enter 「재가입전 계약과 보험가입금액
  및 보장내용이 동일한 계약」, at a repriced premium [S1].
- On renewal, as recorded above: **no 면책기간, no 감액, and no fresh 납입면제**
  [S2] [S4] [S6] [S7].
- The institute's assessment of why the market went renewable is explicit and is the single
  most useful sentence in this file for the technical notes: 「현재의 안전할증 수준에서는
  **갱신형으로 상품을 설계하지 않는 한 추세리스크는 항상 존재함**. 갱신형으로 개발할 경우
  고연령층으로 갈수록 보험료의 급격한 상승이 예상되며 이로 인해서 계약자들의 보험갱신이
  어려워지는 문제점이 있음」 [R4].

### 18. 해약환급금, 무·저해지 and the accumulation account

- On the life contracts there is a real 계약자적립액 and a real surrender value, and both
  the **표준형** and a suppressed form are offered [S3] 제41조:
  「② 회사는 **해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)** 계약이 보험료 납입기간
  중 해지될 경우 해약환급금을 지급하지 않으며, 보험료 납입기간이 경과된 이후 해지될 경우
  **'표준형' 해약환급금의 50%**에 해당하는 금액을 지급합니다. 다만, 보험료 납입이 면제된
  이후 보험료 납입기간이 경과되기 이전에 해지할 경우에는 해약환급금을 지급하지 않으며,
  보험료 납입기간이 보험기간과 동일한 계약(이하 '**전기납 계약**'이라 합니다)의 경우에는
  보험기간 중 계약이 해지될 경우 해약환급금을 지급하지 않습니다」 [S3].
- The comparator is explicitly a pricing device, not a purchasable product: 「'표준형'은
  보험료 및 해약환급금(환급률 포함)의 **비교 안내만을 위한 상품으로 가입이 불가능**하며,
  '표준형'의 해약환급금은 산출방법서에 정한 방법에 따라 계산한 금액으로 **해지율을 적용하지
  않고** 계산합니다」 [S3]. That sentence is the clearest retrieved statement that the
  suppressed form's pricing **does** use a lapse assumption while the comparator does not.
- 「보험료 납입기간 중이라 함은 계약일로부터 보험료 납입기간이 경과하여 최초로 도래하는
  계약해당일 전일까지의 기간을 말합니다」, with a worked example: 계약일 2018-09-01,
  20년납 → 납입기간 중 = 2018-09-01 to 2038-08-31 [S3]. The step-up is therefore at a
  **known date**, and the surrender-value profile is a cliff, not a curve.
- 「회사는 계약체결시 해약환급금 미지급형 … 및 표준형의 보험료 및 해약환급금(환급률 포함)
  수준을 **비교·안내**하여 드립니다」 [S3] — a disclosure obligation attached to the form.
- **보험계약대출** is available 「이 계약의 해약환급금 범위 내에서」, but 「순수보장성보험 등
  보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 [S3] — so on a 무해지 or
  순수보장형 cancer contract there is effectively no policy loan.
- **The only retrieved surrender-value figures** are on a non-life 순수보장형 product,
  남자 40세 / 월납 / 10년납 10년만기 [S8]:

  | Plan | 1년 | 3년 | 5년 | 7년 | 10년 |
  |---|---|---|---|---|---|
  | Plan 1 납입보험료 (₩) | 119,280 | 357,840 | 596,400 | 834,960 | 1,192,800 |
  | Plan 1 해약환급금 (₩) | – | 40,317 | 128,986 | 170,870 | – |
  | Plan 1 환급률 | 0.0% | 11.3% | 21.6% | 20.5% | 0.0% |
  | Plan 2 납입보험료 (₩) | 187,332 | 561,996 | 936,660 | 1,311,324 | 1,873,320 |
  | Plan 2 해약환급금 (₩) | – | 41,407 | 167,396 | 227,546 | – |
  | Plan 2 환급률 | 0.0% | 7.4% | 17.9% | 17.4% | 0.0% |
  | Plan 3 납입보험료 (₩) | 347,292 | 1,041,876 | 1,736,460 | 2,431,044 | 3,472,920 |
  | Plan 3 해약환급금 (₩) | – | 47,276 | 238,067 | 338,634 | – |
  | Plan 3 환급률 | 0.0% | 4.5% | 13.7% | 13.9% | 0.0% |

  Two things are visible and both matter for the model. The surrender value **peaks around
  year 5–7 and falls to nil at maturity**, which is the signature of a pure-protection
  contract with a small unearned-premium element rather than a savings one; and the
  **환급률 falls as the plan gets richer** (21.6% → 17.9% → 13.7% at year 5), which is what
  a fixed 해약공제액 does when spread over a larger premium. 「회사는 금융감독원장이 인가한
  산출기준에 따라 계산한 이 보험의 **계약자적립액에서 해약공제액을 공제한 금액**을
  해약환급금으로 지급하여 드립니다」 [S8].
- The **계약자적립액 적용이율** on that product is 「연복리 **1.5%**」 [S8]. On the 2018
  non-life contract the 적립부분 is credited at the 공시이율 with a floor of
  「최저보증이율 연단위 복리 **0.5%**」 [S1], and the 만기환급금 is 「기본계약 만기시점의
  적립금」 [S1]. Mid-term withdrawal is allowed after 2 years, up to 4 times per policy year,
  capped at **80%** of the 적립부분 해지환급금 [S1].
- A **만기환급형** cancer product exists: 「2종 상품은 만기환급형 상품으로 보험만기시점에
  보통약관([갱신형]암진단비)이 유효하고 보험료를 완납한 계약에 대하여 보통약관 **보험가입금액
  의 5%**를 만기환급금으로 지급합니다」 [S8].
- Every retrieved contract is **무배당**: 「이 상품은 무배당 상품으로서 배당을 하지 않습니다.
  그러나 무배당 상품은 배당 상품에 비해 보험료가 상대적으로 저렴하다는 특징이 있습니다」
  [S8]; 제43조 (배당금의 지급) appears in the life 약관 as a formal article [S3].

### 19. Premiums, issue ages, terms

- **The only retrieved premium figures** are the three plans of [S8], read off the
  해약환급금 예시 table's 납입보험료 row, at 남자 40세 / 월납 / 10년납 10년만기 /
  순수보장형: **₩119,280, ₩187,332 and ₩347,292 per year**, i.e. **₩9,940, ₩15,611 and
  ₩28,941 per month**. The table does not state each plan's 보험가입금액, so these are
  price points without a benefit denominator — see gaps.
- **Issue ages and terms**, from retrieved documents:
  - 만15세~65세, 보험기간 15년, 납입기간 5/10/15년, 월납·3개월납·6개월납·연납, with
    재가입 at expiry [S1]. Two riders are age-restricted: 두 번째 급성심근경색증 진단비 is
    남자 만15세~65세 but 여자 19세~65세; the 유방/부인과 관련 수술비 riders are 20세~65세 [S1].
  - 20~60세 최초계약, renewing on a 1–10년 term with 갱신연령 30~80세 (10년만기) and
    81~89세 (1~9년만기), 전기납, 월납 [S8].
  - 갱신 to a final 100세 계약해당일 [S4]; renewal to 100세만기 once past 가입나이 85 [S7].
- **비흡연체형** underwriting is offered as a formal 약관 chapter on the life contracts —
  제8관 「비흡연체형 적용에 관한 사항」, with 제53조 가입자격, 제54조 흡연상태 변경통지 —
  and a separate 보험요율 [S3]. On the modular product the smoker/non-smoker split applies
  to some 세부보장 and not others: 「제2-3조 제6호 내지 제7호에서 정한 보험금 지급사유는
  **흡연상태의 구분 없이** 발생하는 위험으로 계산」 [S4].
- **간편심사 (simplified underwriting)** products are what let the issue age reach 75:
  「간편 심사 보험 상품은 보험 가입 시 피보험자의 건강상태 등에 관한 **최소한의 의적고지**를
  받고 가입이 가능한 상품을 말하며, 현재 판매되고 있는 간편 심사 암보험은 피보험자의
  **고혈압 및 당뇨병 유무에 대해서 묻지 않음**」 [R4, footnote 7]. A 간편가입 version of
  the modular cancer product exists [S4-family].
- Underwriting can also attach 「보험가입금액 한도 제한, 일부 보장 제외, 보험금 삭감, 보험료
  할증과 같이 조건부로 승낙」 [S3], and a 특정 신체부위·질병 보장제한부 인수특약 is one of
  the standard 제도성특약 shipped with the contract [S3].

### 20. 보험나이 and the contract-law furniture

- **보험나이** is defined identically across the retrieved life contracts and is the age
  basis for pricing [S3] 제30조:
  「① 이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다. ② 제1항의 보험나이는
  **계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고 6개월 이상의
  끝수는 1년으로 하여 계산**하며, 이후 **매년 계약 해당일**에 나이가 증가하는 것으로
  합니다」, with the worked example 「생년월일 : 1988년 10월 2일, 현재(계약일) : 2018년 4월
  13일 ⇒ 2018년 4월 13일 - 1988년 10월 2일 = 29년 6월 11일 = **보험나이 30세**」 [S3].
- 「매년 계약 해당일 — 제2차년도 이후 매년의 계약일과 동일한 월, 일. 다만, 해당 월에 동일한
  일이 없는 경우에는 해당 월의 말일」 [S3]. So 보험나이 increments on the policy anniversary,
  not on the birthday, and differs from 만나이 for roughly half of all issue dates.
- 「청약서류상 피보험자의 나이 또는 성별에 관한 기재사항이 신분증에 기재된 사실과 다른
  경우에는 신분증에 기재된 나이 또는 성별로 **정정**하고, 정정된 나이 또는 성별에 해당하는
  보험금 및 보험료로 변경합니다」 [S3]. Age misstatement is corrected, not voided, except
  where the corrected age falls outside the product's range, in which case the contract is
  void under 제28조제1항제3호 [S1] — 「다만, 회사가 나이의 착오를 발견하였을 때 이미
  계약나이에 도달한 경우에는 유효한 계약으로 보나」 [S1].
- **Nullity, generally** [S1] 제28조제1항: no written consent of the life insured on a
  third-party death contract; a 만15세 미만자, 심신상실자 or 심신박약자 as the life insured
  on a death benefit; age outside the stated range. Premiums are returned, with interest at
  the 보험계약대출이율 compounded annually where the insurer was at fault [S1].
- **청약철회 / 계약취소**: the contract may be cancelled within **3개월** of formation where
  the 약관 was not delivered or the important terms not explained or the application not
  signed — 상법 제638조의3제2항 [R7], reproduced in the 약관 as 제27조 [S3] and in the
  consumer summary of [S1].
- **부활 (reinstatement)**: 「보험료 납입연체로 보험계약이 해지되었으나 해지환급금을 받지 않은
  경우 보험계약자는 **해지된 날부터 3년 이내**에 회사가 정한 절차에 따라 계약의
  부활(효력회복)을 청약할 수 있습니다. 회사는 피보험자의 건강상태, 직업, 직무 등에 따라
  승낙여부를 결정하며, 합리적인 사유가 있는 경우 부활을 거절하거나 보장의 일부를 제한할 수
  있습니다」 [S1]. Cover for events between lapse and reinstatement is not restored [S1], and
  the 90-day cancer wait restarts from the 부활일 [S1] [S3] [S7].
- **납입최고 (grace)**: 「보험계약자가 제2회 이후의 보험료의 납입을 연체하는 경우 회사는
  **14일 이상**의 기간을 납입최고(독촉)기간으로 정하여 계약자에게 납입최고하고 그 때까지
  해당 보험료를 납입하지 않을 경우 계약이 해지됩니다」 [S1].
- **고지의무 (계약 전 알릴 의무)**: 상법 제651조 allows rescission 「그 사실을 안 날로부터
  **1월내에**, 계약을 체결한 날로부터 **3년내에** 한하여」 [R7]. The 약관 add the
  now-standard two-year incontestability: rescission is barred once 「회사가 그 사실을 안
  날부터 1개월 이상 지났거나 또는 **보장개시일부터 보험금 지급사유가 발생하지 않고 2년**
  (진단계약의 경우 …)」 have passed [S6] [S7]. **사기에 의한 계약** is separately voidable
  「보장개시일부터 **5년 이내**(사기사실을 안 날부터는 1개월 이내)」 [S6] [S7].
- **소멸시효**: 「보험금청구권은 **3년**간, 보험료 또는 적립금의 반환청구권은 3년간,
  보험료청구권은 2년간 행사하지 아니하면 시효의 완성으로 소멸한다」 — 상법 제662조 [R7].
- **불이익변경금지**: 상법 제663조 — the Part IV rules may not be varied to the
  policyholder's, insured's or beneficiary's disadvantage [R7]. This is the statutory floor
  under every 약관 term quoted above.
- **Late-payment interest on benefits** is scheduled in a 별표: 보험계약대출이율 for the
  first 30 days after the due date, then +4.0% to day 60, +6.0% to day 90, and **+8.0%**
  thereafter; 해약환급금 accrues at 평균공시이율 × 50% for the first year and × 40% beyond
  [S6] [S7].

### 21. Public incidence: 국가암등록통계, the basis a Korean cancer model is built on

All figures in this section are from [R1] unless otherwise tagged, and all are for
**diagnosis year 2023** unless a series is quoted. [R1] defines its own terms: 「조발생률:
…새롭게 발생한 악성암 환자 수를 전체 인구 수로 나눈 값으로, 인구 100,000명당 암이
발생하는 비율」; 「연령표준화발생률: …각 연령군에 해당하는 표준인구의 비율을 가중치로
부여해 산출한 가중평균발생률 * 표준인구: 우리나라 **2020년 주민등록연앙인구**」 [R1].

- **Headline, 2023**: 발생자수 **288,613** (남 151,126 / 여 137,487); 조발생률 **564.3**
  per 100,000 (남 593.4 / 여 535.5); 연령표준화발생률 **522.9** (남 587.0 / 여 488.9) [R1].
  Corroborated independently at [R2].
- **The 1999–2023 series** (남녀전체), 발생자수 / 조발생률 / 연령표준화발생률 [R1]:

  | 연도 | 발생자수 | 조발생률 | 표준화발생률 |
  |---|---|---|---|
  | 1999 | 101,854 | 216.0 | 402.7 |
  | 2010 | 222,664 | 444.3 | 565.1 |
  | 2017 | 237,089 | 462.8 | 503.2 |
  | 2018 | 247,509 | 482.5 | 509.8 |
  | 2019 | 258,629 | 503.8 | 518.0 |
  | 2020 | 251,329 | 489.5 | 489.5 |
  | 2021 | 280,042 | 545.5 | 531.4 |
  | 2022 | 281,317 | 548.8 | 521.3 |
  | 2023 | 288,613 | 564.3 | 522.9 |

  The crude rate has risen by 161% since 1999 while the age-standardised rate has risen by
  30% and has been broadly flat since 2017 — 「인구 고령화에 따른 결과로 최근 정체 양상을
  보였습니다」 [R2]. **A model driven by crude rates and a model driven by standardised
  rates will disagree violently about trend**; the product is exposed to the crude one.
- **The age curve, 2023** — the table the incidence basis is built from [R1]:

  | 연령군 | 남녀전체 발생자수 | 조발생률 | 남자 조발생률 | 여자 조발생률 |
  |---|---|---|---|---|
  | 0–9세 | 499 | 14.5 | 16.1 | 12.9 |
  | 10–19세 | 889 | 19.0 | 18.2 | 19.9 |
  | 20–29세 | 5,221 | 83.0 | 51.2 | 117.8 |
  | 30–39세 | 15,032 | 228.9 | 143.4 | 321.2 |
  | 40–49세 | 32,884 | 413.8 | 243.0 | 590.0 |
  | 50–59세 | 51,137 | 595.4 | 518.5 | 673.7 |
  | 60–69세 | 76,309 | 1,021.2 | 1,258.9 | 791.6 |
  | 70–79세 | 63,747 | 1,641.9 | 2,367.7 | 1,029.7 |
  | 80세 이상 | 42,895 | 1,867.1 | 2,930.2 | 1,304.5 |

- **The sexes cross, and the crossing point is stated**: 「성별로 나누어 살펴보면, **50대
  초반까지는 여자의 암발생률이 더 높다가, 50대 후반부터 남자의 암발생률이 더 높아지는**
  것으로 나타났다」 [R1]. At 40–49 the female crude rate is **2.43×** the male; at 80+ the
  male rate is **2.25×** the female. **A unisex cancer basis is materially wrong at every
  age**, and wrong in opposite directions either side of about 55.
- **Site ranking, 2023, 남녀전체** [R1] (발생자수 / 분율 / 조발생률 / 표준화발생률):
  모든 악성암 288,613 / 100.0 / 564.3 / 522.9; **갑상선 35,440 / 12.3 / 69.3 / 68.9**;
  폐 32,953 / 11.4 / 64.4 / 57.5; 대장 32,610 / 11.3 / 63.8 / 58.7;
  유방 29,871 / 10.3 / 58.4 / 56.8; 위 28,943 / 10.0 / 56.6 / 51.4;
  전립선 22,640 / 7.8 / 44.3 / 39.2; 간 14,707 / 5.1 / 28.8 / 26.1 [R1].
- **[R1] publishes the excluding-thyroid basis explicitly** — 「갑상선암 제외 253,173 /
  87.7 / 495.0 / 454.0」 [R1]. That single row is what makes a sourced 일반암 (excluding
  C73) incidence rate constructible from public data: **thyroid cancer is 12.3% of all
  registered cancers**, and it is the single largest site.
- **Site by age band, 2023, 남녀전체** — the rank-1 site by age band is 백혈병 at 0–9,
  갑상선 at 10–49, 유방 at 50–59, then 폐 from 60 up [R1]. For men: 갑상선 to 49, 대장 at
  50–59, 전립선 at 60–79, 폐 at 80+. For women: 갑상선 to 39, 유방 at 40–69, 폐 at 70–79,
  대장 at 80+ [R1]. The 30–39 female 갑상선 crude rate is **164.3 per 100,000** against a
  male 62.9 [R1] — the thyroid tier is overwhelmingly a young-female exposure, which is
  precisely why it was moved out of the general tier.
- **Lifetime risk, 2023** — 「평생 암발생/사망 위험도」, 모든 암 (C00–C96): 발생 **41.2%**
  (남 44.6 / 여 38.2); 사망 **19.6%** (남 24.2 / 여 15.6) [R1]. By site, incidence: 폐 6.4,
  대장 5.7, 위 5.0, 갑상선 4.7, 전립선 4.3 (남 8.6), 유방 4.0 (여 7.9) [R1]. The 2010
  comparator was 36.4% (남 37.6 / 여 33.3) [R4] — a **4.8 percentage-point rise in lifetime
  incidence risk over 13 years**, which is the trend risk [R4] warns about.

### 22. Survival, staging, and the post-diagnosis population

- 「5년, 10년 상대생존율: 해당기간 중 발생한 암환자가 5년, 10년 이상 생존할 확률을 추정한
  것으로 암 이외의 원인으로 사망했을 경우의 효과를 보정하기 위하여 **관찰생존율을 일반인구의
  기대생존율로 나누어** 구한 값」 [R1]. The 2023 edition's survival analysis covers
  **4,855,981** people diagnosed 1993–2023 and followed for vital status to 2024-12-31 [R1].
- **5년 상대생존율, 모든 암, by diagnosis period** [R1]:

  | 성별 | ’93–’95 | ’96–’00 | ’01–’05 | ’06–’10 | ’11–’15 | ’16–’20 | ’19–’23 | 증감 |
  |---|---|---|---|---|---|---|---|---|
  | 남녀전체 | 42.9 | 45.2 | 54.2 | 65.5 | 70.8 | 71.7 | **73.7** | +30.8%p |
  | 남자 | 33.2 | 36.4 | 45.6 | 56.9 | 63.2 | 65.8 | **68.2** | +35.0%p |
  | 여자 | 55.2 | 56.4 | 64.3 | 74.5 | 78.4 | 78.0 | **79.4** | +24.2%p |

- **Excluding thyroid** the same series is materially lower: 남녀전체 41.2 → **69.6**;
  남자 32.7 → **65.9**; 여자 52.6 → **74.0** [R1]. The 4.1-point gap at ’19–’23 is what
  the thyroid tier does to a headline survival number.
- **By site, ’19–’23, 남녀전체**: 갑상선 **100.2**, 전립선 96.9, 유방 94.7, 위 78.6,
  대장 75.6, 신장 87.9, 폐 42.5, 간 40.4, 담낭 및 기타담도 29.0, 췌장 **17.0** [R1].
  자궁경부 79.0 [R1]. Thyroid relative survival above 100% means the diagnosed population
  outlives the matched general population — which is the whole actuarial argument for
  putting C73 in the reduced tier.
- **By 요약병기 (SEER summary stage), ’19–’23, 남녀전체** [R1] — 환자분율 / 생존율:
  모든 암 국한 46.1 / **92.7**, 국소 28.0 / 75.6, 원격 17.8 / **27.8**, 모름 8.2 / 60.5.
  By site, 국한 vs 원격: 폐 81.5 vs 13.9; 대장 94.9 vs 20.4; 위 97.6 vs 7.5;
  췌장 47.8 vs 2.4 [R1]. **Survival is a stage story far more than a site story.**
- **Stage at diagnosis is improving and is published as a series** [R1]:
  국한 45.6% (’05) → 47.2 (’10) → 47.9 (’15) → 48.7 (’20) → 50.5 (’21) → 51.0 (’22) →
  **51.8 (’23)**; 원격 21.3 → 18.8 over the same span [R1]. For the six screened sites the
  국한 share in 2023 is 위 70.5, 대장 44.8, 간 54.0, 폐 33.0, 유방 64.8, 자궁경부 55.0 [R1].
  Stomach cancer's localised share has risen **18.8 percentage points since 2005** [R1].
- **Prevalence, 2023**: 암유병자 **2,732,906** (남 1,193,944 / 여 1,538,962) — **5.3%** of
  the population; 조유병률 5,343.4 per 100,000; 연령표준화유병률 4,931.7 [R1]. Excluding
  thyroid, 2,145,614 (4.2% of the population) [R1]. By site: 갑상선 587,292 (21.5%),
  위 366,717 (13.4%), 유방 354,699 (13.0%), 대장 340,064 (12.4%) [R1].
- **Prevalence by age band, 2023** (조유병률 per 100,000): 40–49세 3,497.8;
  50–59세 6,151.5; 60–69세 10,364.9; 70–79세 15,873.1; **80세 이상 17,328.7** — i.e. by
  age 80 roughly **one person in six** is a cancer survivor [R1].
- **Prevalence by elapsed time since diagnosis, 2023, 모든 암** — the table that a repeating
  or 재진단 benefit has to be sized against [R1]:
  ≤1년 **258,721**; 1년 초과 2년 이하 **224,013**; 2년 초과 5년 이하 **552,373**;
  5년 초과 **1,697,799** [R1]. Sixty-two per cent of the prevalent population is more than
  five years out from diagnosis, and **224,013 people are inside the one-to-two-year window
  that the 재진단암 clock (§12) has to run through before it opens**.
- **The population inside the 감액기간 is quantifiable from the same table**: on the 2-year
  design, 482,734 of the prevalent population (≤2년) sit inside the window; on the 1-year
  design, 258,721. Those are prevalence counts, not incidence, so they are indicative only.
- Historical comparator for the trend: 5년 상대생존율 was **64.1%** for 2006–2010 diagnoses
  against 41.2% for 1993–1995 [R4]; and 2010 staging was 국한 42.6% / 국소 30.9% [R4],
  against 51.8 / 29.3 in 2023 [R1].

### 23. 상피내암 (carcinoma in situ): the 유사암 tier's own incidence series

[R1] carries a dedicated 별첨 for in-situ cancer, on the same definitions and the same
standard population [R1]. This is what makes the 유사암 tier priceable from public data.

- 「상피내암: 암이 원발 장소(상피층)에 머무르면서 다른 조직층으로의 침윤 및 악성의 행태를
  보이지 않는 단계 혹은 그러한 성질을 가지는 경우의 암」 [R1].
- **The series, 1999–2023** [R1]:

  | 구분 | 성 | 1999 | 2011 | 2017 | 2019 | 2021 | 2022 | 2023 |
  |---|---|---|---|---|---|---|---|---|
  | 발생자수 | 남녀전체 | 3,595 | 14,645 | 26,596 | 30,212 | 34,736 | 35,859 | **38,204** |
  | | 남자 | 120 | 3,381 | 8,660 | 10,013 | 11,008 | 11,391 | **12,219** |
  | | 여자 | 3,475 | 11,264 | 17,936 | 20,199 | 23,728 | 24,468 | **25,985** |
  | 조발생률 | 남녀전체 | 7.6 | 29.2 | 51.9 | 58.8 | 67.7 | 70.0 | **74.7** |
  | | 남자 | 0.5 | 13.5 | 33.9 | 39.1 | 43.0 | 44.6 | **48.0** |
  | | 여자 | 14.8 | 45.0 | 69.9 | 78.5 | 92.2 | 95.1 | **101.2** |
  | 표준화발생률 | 남녀전체 | 9.0 | 32.9 | 54.6 | 59.9 | 66.6 | 67.8 | **71.3** |
  | | 남자 | 1.2 | 20.2 | 40.7 | 43.8 | 44.8 | 44.9 | **46.7** |
  | | 여자 | 16.7 | 46.8 | 70.9 | 78.5 | 91.0 | 93.5 | **98.8** |

- **The in-situ increment relative to invasive cancer, 2023**: 38,204 in-situ against
  288,613 invasive — **13.2%** of the invasive count, **11.7%** of the combined total [R1,
  derived from the two tables]. The male increment is 8.1% of male invasive cases and the
  female increment is 18.9% of female invasive cases [R1, derived].
- **The trend is the problem.** The in-situ age-standardised rate has risen from 9.0 to 71.3
  per 100,000 between 1999 and 2023 — a factor of **7.9** — while the invasive standardised
  rate rose by a factor of 1.30 over the same period [R1]. Male in-situ standardised
  incidence rose from 1.2 to 46.7, a factor of **39** [R1]. Any 유사암 benefit priced on
  historical experience and left un-repriced is exposed to a decrement that has been growing
  at a wholly different rate from the one the main benefit is exposed to. This is the
  quantitative backdrop to the supervisory intervention of §4 and to KIDI's finding that
  「유방암·제자리암·기타피부암 등 유사암 발생률은 이전보다 늘어난 것」 `[unverified]`.
- **By site, 2023** [R1]:
  - 남녀전체: 모든 상피내암 38,204 / 조발생률 74.7 / 표준화 71.3. 1 자궁경부 11,202 (29.3%),
    2 대장 8,540 (22.4%), 3 유방 7,032 (18.4%), 4 방광 3,216 (8.4%), 5 위 2,719 (7.1%).
  - 남자: 12,219 / 48.0 / 46.7. 1 대장 5,378 (44.0%), 2 방광 2,654 (21.7%), 3 위 1,947
    (15.9%).
  - 여자: 25,985 / 101.2 / 98.8. 1 자궁경부 11,202 (43.1%), 2 유방 7,018 (27.0%),
    3 대장 3,162 (12.2%), 4 피부 1,177 (4.5%), 5 위 772 (3.0%).
- The site codes are given: 위 D002, 대장 D010–D012, 피부 D04, 유방 D05, 자궁경부 D06,
  방광 D090, 기타 상피내암 Re.D00–D09 [R1] — which maps directly onto the 제자리신생물
  분류표 (D00–D09) that the 약관 annex carries [S1] [S3].
- Note that **대장점막내암**, which several contracts carve out of 제자리암 into its own
  tier [S1] [S3], is not separately identified in [R1]: it sits inside 대장 D010–D012.
  A model that prices 대장점막내암 separately cannot source its incidence from [R1].

### 24. Mortality

- **2024 national figures** [R9]: 총사망자 **358,569**, up 6,058 (1.7%) on 2023;
  조사망률 **702.6** per 100,000. 악성신생물 accounted for **24.8%** of all deaths at a
  rate of **174.3** per 100,000, up 4.5% year on year. By site: 폐암 38.0, 간암 20.4, then
  대장암, 췌장암, 위암. Male cancer mortality **215.1** against female **133.7** — a ratio
  of **1.6** [R9]. 3대 사망원인 (암, 심장 질환, 폐렴) were 42.6% of all deaths [R9].
- **Lifetime cancer mortality risk, 2023**: 19.6% overall (남 24.2 / 여 15.6); by site,
  폐 4.4, 대장 2.3, 간 2.1, 위 1.7, 췌장 1.7 [R1]. **갑상선 0.1** [R1] — the tier's whole
  actuarial justification in one number.
- KIDI's published 참조순보험요율 for **질병사망률** on the same age grid as its cancer
  incidence table, 남자 / 여자 [R5]: 20세 0.000141 / 0.000091; 30세 0.000154 / 0.000154;
  40세 0.000525 / 0.000353; 50세 0.001722 / 0.000721; 60세 0.004568 / 0.001466;
  70세 0.013471 / 0.005028; 80세 0.034049 / 0.017189 [R5]. Note this is **disease mortality
  only**, not all-cause, and is a *reference pure premium* rate rather than a best estimate.

### 25. 참조순보험요율: the published incidence basis

- 보험개발원 publishes, for public display, the 참조순보험요율 in force **적용시점
  「2024년 4월 1일 이후」** for 장기손해보험 [R5]. The 구성 table shows that 「질병 —
  암관련 질병」 covers 「사망, 후유장해, **발생**, 입원, 수술」 [R5].
- **「기타피부암 및 갑상선암 이외의 암 발생률」, by age and sex** [R5]:

  | 연령 | 남자 | 여자 |
  |---|---|---|
  | 0세 | 0.000297 | 0.000318 |
  | 10세 | 0.000148 | 0.000152 |
  | 20세 | 0.000230 | 0.000250 |
  | 30세 | 0.000531 | 0.001005 |
  | 40세 | 0.001343 | 0.003382 |
  | 50세 | 0.003567 | 0.004962 |
  | 60세 | 0.008540 | 0.006239 |
  | 70세 | 0.019206 | 0.008626 |
  | 80세 | 0.027892 | 0.011452 |

- **This is the single most useful actuarial table retrieved in this session**, for four
  reasons. (i) It is a **published, dated** rate with a stated effective date. (ii) Its
  definition — cancer *excluding* C44 and C73 — is the insured definition of 일반암, not the
  epidemiological one, so it already embodies the tier carve-out of §4 and the primary-site
  rule of §10. (iii) It is a **참조순보험요율**, i.e. a net premium rate, so it is an
  incidence rate with a loading already in it (see below) rather than a best estimate.
  (iv) Its sex crossover is at about **age 55–60**, matching [R1]'s 「50대 후반부터」
  statement exactly: at 40 the female rate is 2.52× the male, at 60 the male is 1.37× the
  female, at 80 the male is 2.44× the female [R5, derived].
- Sense check against [R1]: the KIDI 40세 male rate of 0.001343 (134 per 100,000) sits
  between [R1]'s 30–39세 male crude rate of 143.4 and its 40–49세 male crude rate of 243.0
  per 100,000 — but the KIDI rate excludes C44 and C73, and thyroid alone is 60.7 per
  100,000 for men at 40–49 [R1]. The two are broadly consistent, which is as far as an
  unsourced reconciliation can go here.
- The same page publishes **질병입원율 (1일이상 180일 한도)**, 남자 / 여자 [R5]: 0세
  3.664744 / 4.388319; 10세 0.276394 / 0.304980; 20세 0.446516 / 0.387364;
  30세 0.402254 / 0.504312; 40세 0.727696 / 0.934549; 50세 1.279489 / 1.966879;
  60세 2.529219 / 3.276503; 70세 4.626935 / 5.442847; 80세 8.646292 / 10.597399 [R5].
  These are **expected days per life-year**, not probabilities, which is the natural
  quantity for a daily inpatient benefit.
- **Safety loading.** The reference rates 「include a safety loading of approximately 10%」
  is a claim seen only in a search-result summary and is `[unverified]`. What *is* sourced is
  the institute's assessment that the loading is inadequate for trend: 「암 발생률이 지속적으로
  상승하고 있는데 반해, **예정위험률 산출 시 이를 반영하지 못함**에 따라 추세리스크가
  존재하여 보험회사들은 적극적으로 암보험 상품을 판매하지 않음 … **현재도 예정위험률 산출 시
  미래의 추세를 반영하지 않고 있음**」 [R4], and 「현행 안전할증 수준으로는 충분하지 않으며,
  향후 문제 발생 시 보험회사들은 상품의 판매를 중단할 수밖에 없음. 우리나라와는 달리 일본의
  경우 안전할증 설정 시 **수준리스크, 추세리스크 등을 모두 반영**하여 산출함」 [R4].
- **경험위험률.** Insurers do not have to use the reference rate: 「'경험위험률'이란 보험사
  자체 위험률(사망률, 사고율)과 평균수명 등을 예측한 수치로, 보험개발원의 참조 요율에
  보험사의 통계를 더해 산출합니다」 `[unverified]` — from a search summary, not a retrieved
  document. The **제10회 경험생명표** applied from **2024-04** with 평균수명 남 86.3세 /
  여 90.7세, up 2.8 and 2.2 years on the 9회 `[unverified]`; and KIDI's 제10회 참조위험률
  analysis is reported to have found overall cancer incidence broadly unchanged but
  **유사암 incidence up** `[unverified]`. None of these three was confirmed against a
  retrieved KIDI document [R14].

### 26. The three risks the institute names, and why they belong in the model

[R4] is the only retrieved source that states what an actuary should worry about on this
product, and it names three risks plus a fourth design problem. They are reproduced because
`technical-notes.md` should be conscious of them.

- **추세리스크 (trend risk)** — 「보장기간 연장은 장기보장으로 인한 추세리스크가 발생함.
  현재도 암 발생률은 상승하고 있으며, 향후 어느 시점에서 암 발생률 상승이 멈출지는 예측하기
  어려움」 [R4]. The mitigations the market actually used: 「보험회사들은 현재 갑상선암,
  유방암 등 발생률이 급격히 상승하는 일부 암들을 **소액화**하여 추세리스크를 최소화하고,
  암사망을 함께 담보함으로써 암 발생 증가로 인한 리스크를 완화하려고 함 … 일부 보험회사들은
  **10년 혹은 15년 갱신형**으로 상품을 설계하여 100세 혹은 종신토록 암 진단을 보장하지만
  갱신 시점에서 보험료를 인상할 수 있게 함으로써 근본적으로 추세 리스크를 제어하려고 함」
  [R4]. And a quantified claim: 「갑상선암과 같이 발생률이 급격히 증가하는 암에 대해
  보험금을 소액화 함으로써 실질적인 **전체 암발생 증가율을 연 2% 수준**으로 둔화시킬 수 있어
  보장기간 확대가 가능해짐」 [R4].
- **수준리스크 (level risk)** — 「가입연령 확대로 새롭게 가입이 확대된 연령층(**61~75세**)에
  대한 경험 부족으로 수준리스크가 존재함 … 간편 심사 암보험 상품이 과거에 판매된 적이 없기
  때문에 간편 심사가 위험률에 미치는 영향에 대한 분석이 충분치 못함 … 현재, 위험률에
  부가되는 안전할증이 **수준리스크의 크기에 영향을 받지 않기 때문에** 다른 상품들에 비해서
  수준리스크가 큰 상품은 수준리스크에 대한 적절한 대비가 요구됨」 [R4].
- **재발 발생률의 불확실성** — 「최초 암 발생 이후 재발하는 암에 대한 정확한 발생률 예측이
  어려움 … 과거에는 암이 재발할 경우 대부분 곧 사망했지만, 최근에는 의료기술 발달로 인해
  재발하더라도 계속적으로 생존할 것으로 예상되고 있으며, 이는 **3차, 4차 암 진단보험금 지급이
  가능함**을 의미함 … 향후 암이 여러 번 재발할 확률은 매우 불확실하며, 이에 따른 리스크도
  매우 큼」 [R4]. This is the actuarial statement behind §12.
- **Stage-graded benefits** — 「암 단계별로 보험금 차등 지급의 경우도 암의 진행 단계에 대한
  정확한 구분이 어려우며, 이로 인해 민원이 발생할 가능성이 높음」, with the observation that
  「**남아프리카 공화국**은 암뿐만이 아니라 다른 중대한 질병들의 진행 단계에 대한 구분이
  보편적으로 알려져 있으며, 따라서 남아프리카 공화국만이 암 단계별 보험금 차등지급
  상품(stage cancer product)이 성공적으로 판매되고 있음」 [R4, footnote 10]. No retrieved
  Korean contract grades by 병기; the graded tiers that did emerge grade by **site and
  histology** instead [S3] — which is [R4]'s prediction proved half right.
- Finally, the pricing regime: 「새롭게 도입된 보험료 산출 방식인 **현금흐름 방식**하에서,
  다양한 리스크에 대한 정확한 분석과 함께 합리적인 현금흐름 가정을 사용한 보험료가 산출되어야
  할 것임」 [R4] — cash-flow pricing, which is what the reference model implements.

---

## Variation across carriers

The observed range that the drafting pass needs. Seven carriers; "—" means the retrieved
documents for that carrier do not state it. `[S1]`/`[S2]` are the same non-life carrier
eight years apart and are shown separately because the differences are the point.

| Feature | [S1] 삼성화재 2018 | [S2] 삼성화재 2026 | [S3] 한화 비갱신 | [S4] 한화 갱신 (modular) | [S6] 라이나 첫날부터 | [S7] 라이나 퍼펙트케어 | [S8] AIG |
|---|---|---|---|---|---|---|---|
| Writer | 손해보험 (제3보험) | 손해보험 (제3보험) | 생명보험 | 생명보험 | 생명보험 | 생명보험 | 손해보험 |
| Chassis | 진단 + 입원 + 수술 + 치료, one contract | same, far more granular | diagnosis only, 5 tiers | 23 independent modules | diagnosis only, 3 tiers | diagnosis only, 3 tiers | 진단 + riders |
| 갱신 / 비갱신 | 15년 만기 + **재가입** | 15년 + 재가입, 갱신형 riders | **비갱신** | **갱신** to 100세 | **갱신** | **갱신**, to 100세만기 past 85 | **갱신** 1–10년 to 89세 |
| 면책기간, 일반암 | **90일** | **90일** | **90일** | **90일** (최초계약만) | **none** | **90일** | **90일** |
| 면책기간, 유사암 | none | none | 갑상선암 90일; others none | 갑상선암 90일; others none | none | none | — |
| 면책기간, under-15 | — | **none** (보장개시일 = 계약일) | — | — | n/a | — | — |
| 면책기간 on renewal | n/a | **none** | n/a | **none** (개시일 = 갱신일) | **none** | **none** | — |
| Pre-waiting diagnosis | that **benefit** 무효, premiums returned; rest cancellable within 90 days | same | that module 무효 | that module 무효 | n/a | that benefit 무효 | — |
| 감액기간, 일반암 | **1년 50%** | **none** | **2년 50%** | **2년 50%** | **1년 50%** | **2년 50%** | — |
| 감액기간, 유사암 | 1년 50% | **1년 50%** | 2년 50% | 2년 50% | 1년 50% | 2년 50% | — |
| 감액 two-step | — | **180일 25% / 1년 50%** (robot surgery) | — | — | — | — | — |
| 감액 on renewal | n/a | **none** | n/a | **none** | **none** | **none** | — |
| 감액 clock ends at | 진단확정일 / 수술일 | 진단확정일 / 수술일 | 진단확정일 | 진단확정일 / 수술일 | 진단확정일 | 진단확정일 | — |
| 유사암 members | 기타피부암, 갑상선암, **대장점막내암**, 제자리암, 경계성종양 | same five | 기타피부암, 갑상선암, 대장점막내암, 제자리암, 경계성종양 (as 소액질병) | same | 갑상선암, 기타피부암, 제자리암, 경계성종양 | same four | 기타피부암, 갑상선암, 제자리암, 경계성종양 |
| 유사암 ratio | separate rider, own 가입금액 | separate rider | **20%** | **20%** | **10%** | **10%** | **70%** |
| Middle tier | 특정소액암 = 유방·자궁경부·자궁체부·전립선·방광 | same | **특정 소액암 60%** = 직결장·유방·여성생식기·전립선·비초기비중증 갑상선 | 소액암 **60%** | 유방·전립선 **20%** | 유방·전립선 **20%** | — |
| 갑상선암 subdivided | no | no | **yes** — 중증 80% / 초기 20% / 그 외 60% | **yes** — 중증이외 20% | no | no | no |
| High tier | 5대 주요암, 10대 주요암 (separate riders) | same + 전이암 riders | **특정 고액치료비관련암 = C40–41, C70–72, C91–95+D47.1+D47.5**, paid **on top** | same | — | — | 고액치료비암 rider |
| 진단비 frequency | 최초 1회한 + 재진단암 rider (2년) | 최초 1회한 + 재진단암 | 최초 1회한 | 최초 1회한 | 최초 1회한 | 최초 1회한 | 최초 1회한 + 재진단암 rider (2년) |
| 입원일당 | 180일 한도, 유사암 20% | split 요양병원 제외 / 요양병원 90일 한도 | — | 상급종합병원, **2일 이상, 1일 초과, 120일 한도** | — | — | 4일 이상, 요양병원 separate |
| 수술비 | 최초 1회한 + 1회당, both required | + 다빈치로봇 rider | — | 관혈 : 비관혈 = **5 : 1** | — | — | 암수술비 rider |
| 항암치료비 | one rider; 기타피부암·갑상선암 at **20%** | five riders by modality | — | Ⅰ / Ⅱ tiers at **4 : 1** | — | — | rider |
| 납입면제 trigger | 암(유사암 제외), 뇌출혈, 급심 | per 사업방법서 | 암 (excl. 소액·유사암) or **장해 50%** | same; **not renewed**, 5-year re-arm | 장해 50% and 암 | 장해 50% and 암 | 일반암 진단 |
| 사망 on the contract | 암 사망 rider (80% 후유장해) | rider | none — pays **계약자적립액** | none | none | none | 질병사망 rider |
| 해약환급금 | 적립부분, 공시이율, floor **0.5%** | 적립부분 | 표준형 or **미지급형 (납입중 0% / 납입후 50%)** | — | 계약자적립액 | 계약자적립액 | 계약자적립액 @ **연복리 1.5%**; peak ~year 5–7, nil at maturity |
| 만기환급금 | 기본계약 만기 적립금 | — | none | none | none | none | **5% of 가입금액** on 2종 |
| 배당 | 무배당 | 무배당 | 무배당 | 무배당 | 무배당 | 무배당 | 무배당 |
| Issue ages | 만15~65세 | — | — | — | — | to 85 for renewal | 20~60세 |
| Premium modes | 월/3개월/6개월/연납 | — | — | — | — | — | 월납 |

**What does not vary.** Every retrieved contract: (i) defines cancer by reference to the
KCD and lists the codes in an annex; (ii) requires 진단확정 by a **병리과 또는
진단검사의학과 전문의** on 조직검사 / 미세바늘흡인검사 / 혈액검사 microscopy, with a
documented-evidence fallback; (iii) dates the diagnosis to the **검사 결과보고 시점**;
(iv) carries the **C77–C80 원발부위 기준** clause mandated from 2011-04-01; (v) excludes
전암(前癌)상태 by name; (vi) pays the main diagnosis benefit **최초 1회한**; (vii) provides
a **제3자 (종합병원 전문의)** opinion procedure at the insurer's expense; and (viii) is
**무배당**.

**What varies most, in order.** The 유사암 payout ratio (10% to 70% observed, converging on
20%); the presence and length of the 감액기간 (none / 1년 / 2년, with a 180-day inner step
appearing); the membership of 유사암 (four or five); whether 갑상선암 is subdivided; whether
the 면책기간 exists at all; and the high-tier enumeration (three sites, five, or ten).

**Most representative design for a reference implementation.** A monthly-grid, 무배당,
갱신형-capable 정액 cancer contract with: a **90-day 면책기간** on invasive cancer (cover
from day 91), none on 유사암, none on a 갱신계약, and none for a life under 보험나이 15; a
pre-보장개시일 diagnosis voiding **that benefit only**, with premiums returned; a **1-year
50% 감액기간** measured from 보험계약일 to the pathology report date, disapplied on renewal
— the median of the observed none / 1년 / 2년 range, and the level the supervisor itself
describes [R6]; a **일반암 진단비 of ₩30,000,000 (3천만원)** paid 최초 1회한; a **유사암
진단비 at 20%** of it (the post-2022 supervisory level [R12], and the level of the cleanest
retrieved ladder [S3]); a **고액암** top-up paid *in addition* on a short named list; an
inpatient daily benefit capped at 180 days per stay with 유사암 at 20% of the daily amount;
a surgery benefit split 관혈 / 비관혈 at 5:1; a single 항암약물·방사선 치료비 paid 최초
1회한; premium waiver on invasive cancer diagnosis only; monthly premiums with a 14-day
납입최고 and a 3-year 부활 window; and a **해약환급금 미지급형** surrender basis with the
step-up at 납입완료.

---

## Fetch failures and gaps

**URLs tried and not opened, or opened without usable content**

- `https://direct.samsunglife.com/ncancer.eds` [S11] — HTTP 200, 6,761 bytes, of which 16
  characters are text; the page is a JavaScript shell. **What is lost**: any product
  document from **삼성생명**, Korea's largest life insurer. The life-insurer side of this
  file therefore rests on 한화생명 [S3] [S4] [S5] and 라이나생명 [S6] [S7] only.
- `https://www.fss.or.kr/fss/bbs/B0000115/view.do?nttId=55845&menuNo=200504` and
  `...&menuNo=200143` [R13] — `curl` received an empty reply from the server (HTTP/0);
  `https://www.insclaim.co.kr/19/8641153` returned **404**; and the mirrored PDF at
  `https://waf-e.dubudisk.com/.../질병상해보험 표준약관 (2018.11.06 개정).pdf` failed TLS
  verification (`unable to get local issuer certificate`) both with and without the session
  CA bundle. **What is lost: the 질병·상해보험 표준약관 itself.** Every statement in this
  file about what the *standard* conditions require is therefore taken from the carriers'
  own 약관, which implement the standard but may add to it, or from [R3] and [R6], which
  describe it. Specifically **unverified**: the exact 표준약관 article numbers; whether the
  90-day 암보장개시일 is mandated by the 표준약관 or is a market convention that the
  표준약관 merely permits; and the 표준약관 revision dates (개정 2022-02-16 시행 2022-04-01;
  개정 2022-09-30 시행 2023-01-01) which appear only in search summaries.
- `https://www.mohw.go.kr/board.es?...list_no=1488742...` — connection reset by peer on
  every attempt. **What is lost**: 보건복지부's own press release on the 2023
  국가암등록통계. Mitigated: the underlying statistical annex [R1] was retrieved in full and
  is the primary document; the press release is a summary of it.
- `https://www.kca.go.kr/home/board/download.do?...fno=10006310...` (한국소비자원,
  「암보험상품 보험료비교 조사연구」) and `...fno=10013089...` (한국소비자원, 「암보험 약관의
  문제점 및 개선방안」) — plain `curl` failed with `SSL_ERROR_SYSCALL`; WebFetch returned
  **HTTP 503** on both. **What is lost**: the only identified source of a **cross-carrier
  premium comparison at a common model point**, and an independent consumer-body critique of
  the 약관 with its own dispute statistics. This is the largest unclosed gap in the file —
  see below.
- `https://files-scs.pstatic.net/.../2024년_사망원인통계 결과 최종.pdf` [R9] — connection
  reset. **What is lost**: the by-site and by-age cancer mortality detail tables. Only the
  headline figures, taken from the 정책브리핑 reproduction, are reported.
- `https://www.kidi.or.kr/user/nd60694.do` — HTTP 400. `https://www.kidi.or.kr/user/nd11592.do`
  (보도자료 index) was retrieved but the 제10회 경험생명표 release could not be located within
  it [R14]. `https://www.kidi.or.kr/user/nd5367.do` (공시기준이율) returned a page whose data
  is behind a file download that was not attempted. **What is lost**: the 경험생명표 release,
  the 참조위험률 methodology, and the 공시기준이율 series.
- `https://www.law.go.kr/...` — every attempt in this session was reported by the agent proxy
  as `ws_closed_mid_exchange`. **What is lost**: 법제처's own text of 상법, 보험업법 and the
  보험업감독규정. Mitigated for 상법 by the Wikisource transcription [R7] and for 보험업법
  제4조 by CaseNote [R8]; **not** mitigated for 보험업감독규정 or 보험업감독업무시행세칙,
  neither of which was retrieved at all.
- `https://www.aig.co.kr/wp/dpwpm400c.jsp?...` [S8] — the page was retrieved but its
  보장내용 and 가입예시 tabs render client-side and did not come through. **What is lost**:
  the benefit amounts that go with the three retrieved premium figures. The premiums are
  therefore **price points without a benefit denominator** and cannot be used to infer a
  rate per unit of sum insured.
- `https://www.cancer.go.kr/lay1/S1T639C643/contents.do` and `.../S1T639C646/contents.do`
  (생존율 and 상피내암 pages) — retrieved, but the returned HTML contained only the site
  navigation; the data tables are injected client-side. No facts are taken from them.
  Mitigated: both datasets are in [R1] in full.

**Claims left `[unverified]`, and why**

- **The 표준약관's own text and the statutory status of the 90-day rule.** Not retrieved
  [R13]. Every retrieved contract has a 90-day 암보장개시일 [S1] [S2] [S3] [S4] [S7], and
  both the institute [R3] and the supervisor [R6] describe it as the norm — but one
  retrieved product has none at all [S6], which is only possible if the 90 days is a
  convention rather than a mandate. **The product spec should say the 90 days is a market
  convention, sourced to the carriers' own 약관 and to [R3] [R6], and must not assert that
  it is required by the 표준약관.**
- **The 2022 유사암 20% cap.** Sourced only to a news report [R12]; the 금융감독원 공문 was
  not retrieved and no FSS document naming it was found. That the market *is* at about 20%
  is independently confirmed by the retrieved contracts [S3] [S4], and that it was once much
  higher is confirmed by [S8] at 70% — so the *effect* is sourced even though the
  *instrument* is not.
- **The date 갑상선암 was moved to 유사암.** A search summary gives **2007년 4월**; the
  retrieved institutional sources give only 「2000년대 중반부터」 [R3] and place it in the
  5회 경험생명표 era beginning **2006년 1월** [R4]. **The precise date is unverified**; the
  product documents should say "from the mid-2000s, on the 5회 경험생명표 basis effective
  from 2006-01" and cite [R4], not a specific month.
- **The first sale date of 암보험 in Korea.** [R3] says 1980년 12월; [R4] says 1988년 7월.
  Both are institutional publications. **Unresolved.** Both are reported in §2 and neither
  should be quoted alone.
- **A 1-year 재진단암 cycle.** [S10] describes the market benefit as 「매 1~2년마다」, but
  **every retrieved 재진단암 clause is 2 years** [S1] [S8]. A 1-year cancer re-diagnosis
  cycle is `[unverified]` and is outside the sourced range.
- **제10회 경험생명표** — 평균수명 남 86.3세 / 여 90.7세, applied from 2024-04, and the
  reported finding that 유사암 incidence rose while overall cancer incidence did not.
  All from search summaries; the KIDI release was not retrieved [R14]. `[unverified]`.
- **The 10% safety loading on 참조순보험요율.** From a search summary only. What *is*
  sourced is that the loading contains **no trend allowance** [R4]. `[unverified]`.
- **경험위험률 methodology** — that insurers add their own experience to the KIDI reference
  rate. From a search summary. `[unverified]`.
- **Loss ratios.** No carrier or industry loss-ratio figure for 암보험 was retrieved. [R4]
  describes 「손해율 급등」 in the 2000s and [R3] describes 「손해율이 높아졌고」 without
  numbers. **There is no sourced 손해율 in this file.**
- **Lapse and persistency.** No public source retrieved. The only quantitative trace is the
  surrender-value table of [S8], from which nothing about lapse *rates* can be inferred.
  **Any persistency assumption in the model must be `[std]`.** Note that the 해약환급금
  미지급형 pricing explicitly *does* use a 해지율 while the 표준형 comparator does not
  [S3] — so the assumption is material and the model should say so.
- **Expense loadings, 사업비, 해약공제액.** Not retrieved for any product. [S8] states the
  surrender value is 「계약자적립액에서 **해약공제액**을 공제한 금액」 without quantifying
  it, and [S1] names 계약체결비용 and 계약관리비용 without amounts. **The 표준해약공제액 cap
  in the 보험업감독규정 was not retrieved** — that belongs to
  `_research/regulatory-actuarial.md`.
- **Premium rates by age and sex.** The three figures at [S8] are the only retrieved
  premiums and they lack their benefit denominator (above). Search summaries offering
  「40세 남성, 일반암 진단비 1,000만원 → 월 11,270원」 and 「암진단금 3,000만원 → 월 4만원
  비갱신형」 are from consumer-comparison sites, are not carrier documents, and are
  `[unverified]`. **The model's premium must be computed, not quoted.**
- **재진단암 incidence.** No public source gives a cancer *re*-diagnosis rate. [R1]'s
  elapsed-time prevalence table (§22) is the closest public quantity and is a prevalence
  stock, not an incidence flow. [R4] says the quantity is 「매우 불확실」 [R4]. **Any
  재진단암 decrement in the model is a `[std]` construction.**
- **대장점막내암 incidence.** Carved out as its own tier by several contracts [S1] [S3] but
  not separately identified in [R1], where it sits inside 대장 D010–D012. Not sourceable.
- **In-situ incidence by age band.** [R1] publishes the in-situ series by **sex and site**
  and by year, and the invasive series by **age band**, but not in-situ by age band. The
  13.2% in-situ-to-invasive ratio computed in §23 is an **all-ages** figure and must not be
  assumed age-invariant — the sex split alone (8.1% male, 18.9% female) shows it is not
  demographically flat.
- **Post-diagnosis mortality.** [R1] gives 5-year *relative* survival, which is a ratio to
  an expected general-population survival, not a cohort survival curve and not a mortality
  table. Any post-diagnosis survival model built on it is a `[std]` construction. The stage
  distribution [R1] would be needed to make it credible and is published only as a
  proportion, not as a transition rate.
- **The 90-day 유방암 10% variant.** [R3] and [R6] both describe it —
  「자가진단이 용이한 유방암은 암보장개시일부터 90일 이내에 진단 확정 시 암보험금의 10%를
  지급하기도 한다」 — but **no retrieved 약관 contains it.** Treat as a real but
  unrepresented market variant; do not model it.
- **금융감독원 press releases** of 2002-05-20, 2011-01-31, 2011-03-14, 2011-06-20,
  2013-08-22 and 2019-04-30, all cited by [R3], were **not independently retrieved**. Facts
  attributed to them here are quoted **as reported by [R3]**, which is a peer-reviewed
  institutional report and quotes them with dates and titles; they are treated as sourced to
  [R3], not to the FSS.
- **Suicide, war and other general exclusions** were not extracted for this product line.
  A cancer contract with no death benefit has little use for a suicide clause, and the
  retrieved 보험금을 지급하지 않는 사유 articles were not read in full. `[unverified]` for
  this product.
- **K-IFRS 1117 / K-ICS treatment of this product**, the **해약환급금준비금**, the
  **표준해약공제액**, the **예정이율 / 공시이율 / 최저보증이율** framework beyond the two
  figures retrieved here (0.5% floor [S1]; 1.5% credited [S8]), and the **contract-boundary**
  question on a 갱신형 rider are all cross-product matters and belong in
  `_research/regulatory-actuarial.md` and `references/regulatory-and-actuarial-references.md`,
  not here. Nothing in this file should be read as settling them.
