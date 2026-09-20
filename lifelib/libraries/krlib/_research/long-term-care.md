# 간병보험 (long-term care) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean **간병보험** (*ganbyeong boheom*, long-term care insurance)
liability cash-flow reference model — `LTC_KR_S`, a monthly-grid three-state model whose states
are healthy, in long-term care, and dead, and whose entry into the middle state is not a
medical event at all but an **administrative decision of the state**.

That last sentence is the whole product. Korea runs a compulsory public long-term care scheme,
**노인장기요양보험** (*noin janggi yoyang boheom*), under the 노인장기요양보험법 of 2007 (in
force 2008-07). A 등급판정위원회 (grade assessment committee) sitting inside the
국민건강보험공단 scores an applicant on a 52-item instrument and awards one of six grades —
장기요양 1등급 through 5등급, plus 인지지원등급 — or refuses (등급외). Almost every private
간병보험 contract sold in Korea today defines its benefit trigger by reference to that grade
and to nothing else: 「노인장기요양보험법에 따라 등급판정위원회에서 장기요양 1등급 또는
2등급으로 판정받은 경우」 [S1] [S2] [S3] [S4]. There is no ADL schedule in the contract, no
180-day dependency test, no company-basis alternative limb of the kind that defines the
Japanese 介護保険 product in `jplib`, and no AGGIR-style grid of the kind that defines the
French *assurance dépendance* in `frlib`. The insurer has outsourced its claim definition to a
statute and its claim adjudication to a public committee.

That is a large actuarial fact and it cuts both ways. On one side it removes definitional
dispute almost entirely — the Korean 간병보험 claims record is nothing like the Korean CI
claims record, where the word 중대한 generated a decade of litigation (see
`_research/ci-insurance.md`). On the other it hands the insurer a **basis-change risk it does
not control**: the grade thresholds, the scoring instrument, the certification validity period
and the very existence of the grades are all set by 대통령령 and can be moved by the Ministry
of Health and Welfare without reference to any insurer. The 인지지원등급 was created out of
nothing on 2018-01-01 [R6] and instantly enlarged the population that a 「1~인지지원등급」
rider would have to pay [S2]. Carriers respond with an explicit rewriting clause: where the
statute is amended so that the grades cease to exist or cease to be determinable, the insurer
「객관적이고 합리적인 범위 내에서 기존 계약내용에 상응하는 "장기요양상태"와 관련된 새로운
보장내용으로 이 계약의 내용을 변경합니다」 [S3]. A UK or US LTC contract has no analogue.

Alongside the grade-triggered cover sits a second, quite separate product line that also trades
under the word 간병: **치매보험** (*chimae boheom*, dementia insurance), whose trigger is the
**CDR 척도** (Clinical Dementia Rating) — 경도치매 at CDR 1, 중등도치매 at CDR 2, 중증치매 at
CDR 3 이상 — assessed by a 치매 전문의 rather than by a public committee [S2] [S4]. Dementia
cover was written on the severe tier only until about 2017, expanded to the mild tier in late
2018, and then produced the sharpest product boom in recent Korean insurance history:
초회보험료 across the 치매보험 market rose **3.5-fold in 2018 alone**, and 6.5-fold at non-life
carriers [R8]. The regulator intervened twice inside nine months [R8] [R10]. The design that
came out the other side — a CDR-graded diagnosis benefit with a one-year 면책기간 and a 90-day
persistence test — is what every carrier now sells [S2] [S4].

A third line, **간병인사용일당** (a daily indemnity for hiring a private carer during a
hospital stay), is nominally part of the same product family and is at the time of writing the
Korean market's most acute loss-ratio problem: life-sector loss ratios on it reached roughly
100% by August 2024 against 18.7% two years earlier, and the five largest non-life carriers'
premium on it grew about twenty-fold over four years [R15]. It is a hospital-days indemnity,
not a long-term-care product, and `LTC_KR_S` does not model it; it is recorded here because it
sits inside the same 약관 as the grade-triggered benefits [S1] [S2] [S4] and because a reader
comparing Korean market commentary against this library will otherwise conflate the two.

**What this file is.** It is the provenance layer behind `products/long_term_care/`'s four
documents — `product-spec.md`, `technical-notes.md`, `model.md` and `sources.md` — and behind
the `LTC_KR_S` model's parameter files. Every quantitative claim in those documents should be
traceable to a numbered entry here. **The source numbering below is never renumbered**: the
product documents cite against it, so `S3` means the same document forever. Facts are tagged
`[S#]` where they come from a retrieved primary product document, `[R#]` where they come from a
retrieved regulatory, statutory, actuarial or market reference, and `[unverified]` where they
rest on a search snippet or a document that could not be opened. Where a source is a news
article rather than a primary document, the entry says so and the dependent facts inherit that
weakness. Arithmetic performed in this file on retrieved figures is labelled *derived* at the
point of use, and the inputs are always shown so a reader can redo it.

**Retrieval method.** Plain `curl` is blocked for the Korean government and carrier hosts used
here, so everything below was fetched with `WebFetch`. `WebFetch` renders HTML but returns
Korean PDFs as undecodable binary; in every such case the binary it saved to disk was extracted
locally with `pypdf` and read directly. The single most valuable retrieval of the session was
indirect: the 국민건강보험공단 publishes the **2024 노인장기요양보험 통계연보** as a large PDF
that exceeds the fetcher's size limit, but it also publishes an attachment bundle whose
contents turned out to be a ZIP of five `.xlsx` workbooks holding the yearbook's complete
numerical tables. Those workbooks were opened with `openpyxl` and are the arithmetic backbone
of §5 and §6 below. Access date for every source: **2026-09-03**.

---

## Primary sources

### S1 — 우정사업본부(우체국보험), 「무배당 우체국간병비보험 2309 상품요약서」

- Publisher: 과학기술정보통신부 우정사업본부 (Korea Post Insurance), sold through 체신관서
- Document: 상품요약서 (product summary — the statutory pre-contract summary of the 기초서류),
  36 pp., product code family `P400059, P400060`
- Doc type: 상품요약서 (a 기초서류 extract, not marketing copy)
- URL: https://www.epostlife.go.kr/resources/js/biz/ip/gs/pdf/yoyak_P400059,P400060.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (323.7 kB, 36 pp.), text extracted with `pypdf` and read
  in full
- Key content: **the richest single document retrieved this session.** It carries the complete
  benefit table for 무배당 장기요양(1~2등급)특약 2309, 무배당 장기요양(1~5등급)특약Ⅱ 2309 and
  무배당 장기요양간병비특약Ⅱ 2309 with the exact 지급사유 wording; the **180-day** 장기요양상태
  보장개시일 and its 재해 carve-back; a **two-year 50% 감액기간**; the 간병자금 annuity shape
  (monthly, 10 years, first 12 months guaranteed, 120-month cap, amount fixed by the grade at
  first certification and never re-rated); 가입나이 / 보험기간 / 납입기간 grids; the 갱신
  procedure for the renewable riders; and — uniquely among the documents retrieved — the
  **예정이율 (2.0% annual compound)** and a table of **예정위험률 including 요양(1등급) 발생률
  and 요양(2등급) 발생률 by age and sex**. It also gives 해약환급금 worked examples and the 12%
  세액공제 statement.

### S2 — ABL생명, 「(무)ABL우리가족THE케어간병보험(해약환급금 미지급형)2504」 상품안내장

- Publisher: ABL생명보험주식회사
- Document: 상품안내장 / 보험안내자료, 16 pp., 제작 2025-09-01, 준법감시인 심의필
  제2025-PA276호 (2025-08-27 ~ 2026-08-26)
- Doc type: 보험안내자료 (the regulated pre-sale disclosure document under 보험업법 제95조)
- URL: https://abllife.co.kr/cms/prdt/hlthInjry/__icsFiles/afieldfile/2025/08/28/
  (무)ABL우리가족THE케어간병보험(해약환급금_미지급형)2504_20250901.pdf (the live URL is
  percent-encoded)
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (1.76 MB, 16 pp.), text extracted with `pypdf` and read
  in full
- Key content: the most **modern and most complete** product in the file. Main contract pays
  장기요양(1~2등급)급여금; nine optional riders extend the trigger down to 1~5등급 and to
  1~인지지원등급 and add monthly 재가급여지원금 / 시설급여지원금 / 주야간보호지원금 /
  복지용구지원금 tied to *actual use* of the corresponding public benefit; three CDR-graded
  dementia diagnosis riders (경도이상 / 중등도이상 / 중증); dementia 통원 riders;
  간병인사용지원 입원 riders. Gives the **90-day** 장기요양상태 보장개시일, the **one-year**
  치매 보장개시일, the 90-day persistence requirement inside each CDR definition, the verbatim
  CDR definitions, the 「해약환급금 미지급형」 mechanics (nil during the premium-paying period,
  **50% of the 기본형 value** afterwards), a full **월납 premium rate card at ages 40 / 50 / 60
  by sex for 25 separate covers**, and 해약환급금 / 환급률 progressions. It also reproduces the
  등급판정 score bands and the CDR scale from public sources.

### S3 — 삼성화재해상보험, 「무배당 삼성화재 간병보험 1808.2 (새시대 간병파트너)」 보험약관

- Publisher: 삼성화재해상보험주식회사, 장기상품개발2파트, printed 2018-08
- Document: 보험약관 booklet, 234 pp., comprising the 가입자 유의사항, the 주요내용 요약서, the
  보통약관 and the 특별약관 집
- Doc type: **policy conditions (약관)** — a full primary contract document
- URL: https://www.samsungfire.com/publication/pdf/ZPB214010_0_20180802_file1.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (8.4 MB, 234 pp.), text extracted with `pypdf` and the
  benefit, waiting-period, waiver and grade-definition articles read (extraction is clean for
  the body text; the cover art and some marketing pages come out as mojibake and were skipped)
- Key content: a **non-life carrier's** grade-triggered design, and the only document in the
  file with a genuine **multi-tier trigger menu**: 기본계약 장기요양지원금(1~2등급) plus
  selectable 장기요양지원금(1등급 / 1~3등급 / 1~4등급); 장기요양 생활자금 (1~2 / 1~3 / 1~4등급)
  paid **5년간 매월 가입금액**; and a **두 번째 장기요양지원금(1~2등급)** rider with a **5-year
  면책기간 running from the first 1·2등급 판정일** and a re-test at that date. Gives the
  가입나이 × 보험기간 × 납입기간 grid, states 만기환급금 : 없음 (pure protection), and carries
  the statutory-amendment rewriting clause quoted in the introduction.

### S4 — 한화손해보험, 「무배당 한화 골드클래스 간병보험」 약관

- Publisher: 한화손해보험주식회사; document revision date 2023-07-11 (PDF metadata)
- Document: 보험약관 booklet, 173 pp., covering four plans — 간병보장플랜(표준형),
  간병보장플랜(납입중50%해약환급금지급형), 간병치매보장플랜(표준형),
  간병치매보장플랜(납입중50%해약환급금지급형)
- Doc type: **policy conditions (약관)**
- URL: https://image.kebhana.com/cont/download/insdocument/provide/N02C14145_agree.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (6.6 MB, 173 pp.), text extracted with `pypdf`; the
  유의사항, 감액/면책 tables and the 장기요양진단비 and 치매진단비 articles read verbatim
- Key content: the **verbatim article text** of 장기요양진단비(1등급) 제1조(보험금의 지급사유)
  with its 1-year 50% 감액 table set out inside the article; the same for 1~2등급, 1~3등급
  (1804), 1~4등급 and 1~5등급; the CDR definitions of 경증이상치매상태 / 중등도이상치매상태 /
  중증치매상태 each with a **90-day persistence** test; the **one-year full 면책** on the three
  dementia riders and on 파킨슨병진단비, against a **one-year 50% 감액 and no 면책** on the
  five 장기요양 riders; the 「납입중50%해약환급금지급형」 low-surrender-value mechanics; and
  the exclusion referring to 노인장기요양보험법 제29조 (장기요양급여의 제한). Note the source
  of this file: it is hosted on a bank's (하나은행) insurance-document mirror, not on the
  carrier's own site.

### S5 — 교보생명, 「교보더안심치매·간병보험」 출시 보도자료 (교보생명 뉴스룸)

- Publisher: 교보생명보험주식회사 (own newsroom)
- Doc type: **carrier press release** — not a contract document; every fact from it is a
  carrier's own summary of its own product and is weaker evidence than [S1] – [S4]
- URL: https://news.kyobo.com/교보생명-교보더안심치매간병보험-출시/ (percent-encoded in the
  live URL)
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML rendered)
- Key content: a current whole-of-life 치매·간병 product: 진단자금 (lump sum) at 경도 / 중등도
  / 중증치매 plus a **매월 생활자금 지급 for life with a minimum 3-year (36-instalment)
  guarantee**; 장기요양 1~5등급 and 인지지원등급 cover with separate 재가급여 / 시설급여 /
  방문요양 이용수당 riders; a **premium refund on 장기요양 1~4등급 진단**; 가입나이 30~75세; 5
  / 10 / 15 / 20년납; 보험기간 종신. Reported launch 2026-02-25.

---

## Regulatory and actuarial references

### R1 — 노인장기요양보험법 (Act on Long-Term Care Insurance for the Aged)

- Publisher: 국가법령정보센터 (법제처)
- Doc type: statute
- URL: https://www.law.go.kr/LSW/lsInfoP.do?lsId=010436&ancYnChk=0 (index page); article text
  retrieved through the print form
  `https://www.law.go.kr/LSW//lsBdyPrint.do?efYd=20180914&lsiSeq=202643&joNo=<NNNN>:00&chrClsCd=010201`
- Accessed: 2026-09-03
- Retrieved: **in part** — the index page at `lsInfoP.do` returns only the site chrome and the
  currency line (현행 법률 제21690호, 시행 2026-05-26). The **per-article print form works**:
  제2조, 제15조 and 제23조 were retrieved in full at the 2018-09-14 consolidation (법률
  제15443호). Other articles were not retrieved. **Every article text quoted in this file is
  therefore the 2018 consolidation, not the current one**, and is flagged as such at the point
  of use.
- Key content: 제2조 (정의) — 「노인등」 and 「장기요양급여」; 제15조 (등급판정 등) — the
  six-month test and the 대통령령 grade standard; 제23조 (장기요양급여의 종류) — the exhaustive
  list of 재가급여 (six kinds), 시설급여 and 특별현금급여 (three kinds).

### R2 — 노인장기요양보험법 시행령 [별표 1] 「노인성 질병의 종류」(제2조 관련)

- Publisher: 국가법령정보센터 (법제처); 개정 2022-12-20
- Doc type: annexe to a presidential decree (별표)
- URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=135370071&bylClsCd=110201
- Accessed: 2026-09-03
- Retrieved: **yes** — 1-page PDF downloaded and extracted cleanly; the complete table read
- Key content: the closed list of **25 diseases with KCD codes** that alone let a person under
  65 be certified. This is the Korean analogue of Japan's 16 特定疾病 and is materially
  narrower in scope but broader in code coverage — four dementia codes, one Alzheimer code,
  fourteen cerebrovascular codes, four Parkinson-family codes, plus 척수성 근위축, 다발경화증,
  중풍후유증 and 진전.

### R3 — 찾기쉬운 생활법령정보, 「노인장기요양보험 > 등급판정 절차 및 기준」

- Publisher: 법제처 (찾기쉬운 생활법령정보 / easylaw.go.kr)
- Doc type: official plain-language restatement of statute and decree
- URL: https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=2038&ccfNo=2&cciNo=2&cnpClsNo=1
- Accessed: 2026-09-03
- Retrieved: **yes** (HTML rendered)
- Key content: the **장기요양인정점수 band table** for 1등급 through 인지지원등급 with the 심신
  기능상태 description for each, cited to 노인장기요양보험법 제15조 and 시행령 제7조 제1항; and
  the **30-day** determination deadline with a 30-day extension, cited to 법 제16조 제1항.

### R4 — 국민건강보험공단, 「2024 노인장기요양보험 통계연보」

- Publisher: 국민건강보험공단 빅데이터사업실, 발간 2025-06-30 (제도 시행 17주년)
- Document: the yearbook in five parts — 제1편 적용인구 및 현황, 제2편 장기요양 인정 신청 및
  인정 현황, 제3편 장기요양 급여현황, 제4편 장기요양기관 및 인력현황, 제5편 장기요양 재정 현황
- Doc type: **official national statistics** (국가승인통계; also lodged on KOSIS)
- URL (landing): https://www.nhis.or.kr/nhis/together/wbhaec07200m01.do
- URL (the attachment actually used):
  `https://www.nhis.or.kr/nhis/together/wbhaec07200m01.do?mode=download&articleNo=11003958&attachNo=368127`
- Accessed: 2026-09-03
- Retrieved: **yes, in the form that matters.** The yearbook PDF (`...&attachNo=361507`)
  **failed** — the fetcher refused it with `maxContentLength size of 10485760 exceeded`. The
  해설서 attachment (`...&attachNo=364866`) downloaded but is an HWP 5.0 compound document and
  was not decoded. The third attachment (`...&attachNo=368127`, 5.6 MB) is a **ZIP archive**
  whose members are six `.hwp` front-matter files and **five `.xlsx` workbooks containing the
  yearbook's complete numerical tables**. Those five workbooks were extracted and read with
  `openpyxl`. Every yearbook figure in this file comes from those workbooks, table by named
  table.
- Key content: 표1-1 연도별 65세이상 의료보장 적용인구 (2014–2024); 표1-2 시·도별 65세이상
  적용인구 **by five-year age band and sex**; 표2-1 연도별 자격별 인정 신청 현황; 표2-2
  시·군·구별 자격별 인정 신청 현황 (national totals); 표2-3 65세미만 인정 신청자의 노인성질병
  현황; 표2-5 시·도별 등급별 **인정신청 구분별** 인정 현황; 표2-9 시·도별 등급별 **연령별**
  자격별 등급 판정 현황; 표3-2 / 표3-3 급여실적; 표5-1 연도별 재정현황.

### R5 — 국민건강보험공단 경영공시, 「장기요양 등급 판정 현황」

- Publisher: 국민건강보험공단 (자율공시 / 장기요양보험 경영실적)
- Doc type: official disclosure table
- URL: https://www.nhis.or.kr/announce/wbhaec11503m01.do
- Accessed: 2026-09-03
- Retrieved: **in part** — the page rendered and the 2021 – 2026 Q2 table was described, but
  the fetcher returned only a fragment of the cells (one worked example: 2024 계 1,301,069,
  인정자 1,165,030, 1등급 55,340). Those three numbers agree exactly with [R4], which is used
  instead throughout.

### R6 — 국회예산정책처, 「2018~2027년 노인장기요양보험 재정전망」 (2018년 12월)

- Publisher: 국회예산정책처 추계세제분석실 사회비용추계과 (김윤희)
- Document: 94-page report, 발간 2018-12
- Doc type: legislature-budget-office fiscal projection
- URL: https://www.nabo.go.kr/board/file/down.do?fid=33315305
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (1.5 MB, 94 pp.), text extracted with `pypdf` and read
- Key content: the clearest published description of the **assessment instrument** — 12개 영역
  90개 항목 surveyed, of which **52개 항목** enter the 장기요양인정점수, across 기본적
  일상생활활동(ADL), 수단적 일상생활활동(IADL), 인지기능, 행동변화, 간호처치 and 재활; the
  score bands; the **creation of the 인지지원등급 in January 2018** and the diagram of which
  former 등급외 population it absorbed; a 2013–2017 time series of 노인인구 / 신청자 / 판정자 /
  인정자 / 판정대비 인정률 / 노인인구 대비 인정률 / 급여이용 수급자; 2017 utilisation and
  benefit cost by age band and by grade; the 2018 재가급여 월 한도액 and 급여비용 (수가)
  schedules; and the statutory rule that 1·2등급 may use 시설급여 while 3–5등급 may not except
  by exception.

### R7 — 보건복지부, 「2023년 치매역학조사 및 실태조사 결과 발표」 보도자료

- Publisher: 보건복지부 (배포 2025-03-13 조간); survey executed by 중앙치매센터,
  한국보건사회연구원 and ㈜한국갤럽조사연구소
- Doc type: government press release announcing an official epidemiological survey
- URL: https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&act=view&list_no=1484959
- Accessed: 2026-09-03
- Retrieved: **yes** for the release body (HTML). The two 별첨 attachments (`[별첨]2023년
  치매역학조사 및 실태조사 주요 결과` in .hwpx and .pdf) and the `attachPreview.es` viewer were
  **not** retrieved — the viewer returns chrome only.
- Key content: 65세 이상 치매 유병률 **9.25%** (against 9.50% in the 2016 survey) and
  경도인지장애(MCI) 유병률 **28.42%** (against 22.25%); **prevalence by five-year age band**
  (65–69 4.99%, 70–74 5.03%, 75–79 10.70%, 80–84 15.57%, 85+ 21.18%); by sex (남 8.85%, 여
  9.57%); survey window 2023-08-22 to 2024-03-18; a three-stage design (인지선별검사 → 진단검사
  → 실태조사); and projected 추정 치매환자수 (2025 97만명, 2026 약 101만명, 2044 약 201만명).

### R8 — 보험연구원, 「최근 치매보험시장의 이슈와 과제」 (KIRI 이슈분석, 2019-05-13)

- Publisher: 보험연구원 (정성희 연구위원, 문혜정 연구원)
- Document: 4-page 이슈 분석 in the KIRI 리포트 series
- Doc type: research-institute analysis
- URL: https://www.kiri.or.kr/pdf/전문자료/KIRI_20190510_9467.pdf (percent-encoded live)
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (272 kB, 4 pp.), extracted and read in full
- Key content: **the definitive account of the 2018–2019 치매보험 boom.** Gives the CDR scale
  with its seven points and a symptom table for each severity; the market history (severe-only
  until 2017 H2, mild tiers from 2017 H2, 간편치매보험 competition thereafter); the market size
  — 치매보험 초회보험료 **약 233억 원 in 2018, 3.5× the prior year**, of which 손해보험회사
  **약 46억 원, 6.5× the prior year**; the abuse — 「일부 보험회사의 경우 경증치매에 대해 최대
  3천만 원의 보장금액을 제시」 and cross-carrier duplicate purchase; the specific 약관 defect —
  「CDR 척도뿐만 아니라 뇌영상검사 등을 기초로 한 진단이 필요」 and the predicted mass dispute
  over 「CDR 1점 + 뇌 영상자료상 기질적 이상 없음」; the industry's self-imposed **₩30,000,000
  aggregate limit**; and dementia epidemiology (2018 유병률 10.2%, 노인 치매환자 75만 명
  growing 3.2% p.a. against 1.9% for the elderly population, 경증치매 유병률 6.4% = **67% of
  all dementia cases**, 국가관리비용 2017년 13조 6천억 원 ≈ 0.8% of GDP).

### R9 — 보험연구원, 연구보고서 2019-11, Ⅱ장 「우리나라 장기요양서비스/보험의 현황 및 평가」

- Publisher: 보험연구원
- Document: chapter Ⅱ of a research report (30 pp. in the retrieved extract)
- Doc type: research-institute report
- URL: https://www.kiri.or.kr/pdf/연구자료/연구보고서/nre2020-0129_2.pdf (percent-encoded live)
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (651 kB, 30 pp.), extracted and read
- Key content: the **public/private comparison table** (근거법 노인장기요양보험법 vs 보험업법;
  도입시기 2008-07 vs **2003-08**; 급여종류 현물 vs 정액 일시금 또는 연금); the three
  **benefit-trigger archetypes** taken from a 2012 금융감독원 release — ① 회사기준 (중증치매 or
  활동불능상태 diagnosed by the carrier's own definition), ② 공적기준 (the 장기요양등급), ③
  혼합형 — with the observation that 「일반적으로 간병보험에서는 공적기준을 적용하는 경향이
  있다」; the carrier-by-carrier product count at 2019-05 (**99 products**, 생보 46 / 손보 53,
  with 신한생명 12 and 현대해상 14 the largest shelves); the **생명보험 간병보험 실적** series
  (보유계약 2008 143천 건 / 2조 4,430억 원 → 2013 125천 건 / 1조 5,880억 원 → 2018 264천 건 /
  4조 5,390억 원; 신계약 2018 42천 건 / 6,590억 원); household penetration (간병보험 가입률
  **2.5%** overall, 4.8% at 60+, against a 10.0% stated intention to buy); and the
  age-distribution of 치매보험 in force at 2014-06 (5,708,079 계약, 41.1% on lives aged 50–70).

### R10 — 금융감독원, 「치매보험금 분쟁을 선제적으로 예방할 수 있도록 보험약관을
개선하겠습니다」

- Publisher: 금융감독원, 2019-07-02
- Doc type: supervisory press release announcing a 약관 변경권고
- URL (as retrieved): https://eiec.kdi.re.kr/policy/materialView.do?num=190159 (the KDI
  경제교육·정보센터 mirror of the release; the FSS original was not opened — see §Fetch
  failures)
- Accessed: 2026-09-03
- Retrieved: **yes** via the KDI mirror
- Key content: the two substantive reforms — (i) 치매진단 must rest on a **comprehensive
  clinical assessment** (병력청취, 인지기능 및 정신상태 평가, 일상생활능력평가 and 뇌영상검사),
  i.e. imaging is one input and not a gate; (ii) **deletion of 특정 치매질병코드 and 약제투약
  conditions** added to 약관 without rational basis, so that a benefit is payable where a
  specialist diagnoses dementia **and the contractual CDR threshold is met**. Timeline: 약관
  변경권고 in July 2019, revised products on sale from **October 2019**.

### R11 — 한은정·황라일·이정석, 「장기요양 인정자의 사망 전 의료 및 요양서비스 이용 양상 분석」

- Publisher: 한국사회정책 (Korea Social Policy Review) 제25권 제1호, 2018, pp. 99–123. Authors
  at 국민건강보험공단 건강보험정책연구원 and 신한대학교
- Doc type: peer-reviewed journal article using the NHIS claims census
- URL: https://journal.kci.go.kr/kasp/archive/articlePdf?artiId=ART002331210
- Accessed: 2026-09-03
- Retrieved: **yes** — PDF downloaded (1.8 MB), extracted with `pypdf` and the abstract,
  methods and results read
- Key content: **the only post-onset survival evidence retrieved.** Cohort: every person
  certified between 2008-07-01 and 2012-12-31 who also died inside that window — **271,474
  people**, linked across 건강보험, 노인장기요양보험 and 통계청 사망원인통계. Mean time from
  등급인정 to death **516.2 days (SD 430.4)**; **8.7%** died within one month of certification
  and **45.6%** within one year. 74.7% were 75 or over, 60.6% female. Grade mix of the
  decedents (on the pre-2014 three-grade scale): 1등급 26.2%, 2등급 28.3%, 3등급 45.5%. Mean
  장기요양인정점수 82.1 (SD 21.8). Comorbidity: 고혈압 44.3%, **치매 42.3%**, 중풍 29.9%,
  관절염 27.0%. Cause of death: 순환계통 29.8%, 신생물 15.3%. Place of death: 의료기관 64.4%,
  자택 22.0%, 사회복지시설 9.2%. **The sampling is truncated by construction** — only people
  who died inside a 4.5-year window are in it — so 516.2 days is a *lower bound* on the mean
  duration of the care state, not an estimate of it. §7 below does the arithmetic that follows
  from that.

### R12 — 보험업법 제4조 (보험업의 허가)

- Publisher: 국가법령정보센터 (법제처)
- Doc type: statute
- URL: https://www.law.go.kr/LSW/lsSideInfoP.do?lsiSeq=265389&lsId=&joNo=0004&joBrNo=00&
  docCls=jo&chrClsCd=010202&urlMode=lsScJoRltInfoR
- Accessed: 2026-09-03
- Retrieved: **in part** — the article's structure and 제1항제3호 were returned, but not the
  full sub-paragraph text with its 목 lettering. The identical article is cited from a
  retrieved mirror in `_research/ci-insurance.md`.
- Key content: 제1항 — a person carrying on insurance business must be licensed by the
  금융위원회 **by 보험종목**; 제3호 **제3보험업** comprises 상해보험, 질병보험 and **간병보험**
  plus such other 종목 as the 대통령령 prescribes. 간병보험 is therefore not a sub-class of
  질병보험 but a statutory 종목 in its own right, writable by both life and non-life carriers —
  which is why [S1] and [S2] (life-side) and [S3] and [S4] (non-life side) can sell the same
  benefit.

### R13 — 노인장기요양보험법 시행령 제8조 (장기요양인정 유효기간) — 2025-07-01 개정

- Publisher: 보건복지부 / 국민건강보험공단; retrieved through a long-term-care software
  vendor's customer notice restating the amendment
- Doc type: **secondary** — a vendor notice, not the decree. Flagged accordingly.
- URL: https://www.carefor.co.kr/cs/view_notice.php?calmgno=45794&rtnUrl=/cs/list_notice.php
- Accessed: 2026-09-03
- Retrieved: **yes**, but as a restatement
- Key content: the base 유효기간 is **2 years**; where a renewal awards the **same grade** as
  before, the renewed 유효기간 is extended — 1등급 **4 → 5 years**, 2~4등급 **3 → 4 years**,
  5등급 and 인지지원등급 **2 years (unchanged)**, effective **2025-07-01**. The pre-amendment
  values (1등급 4년, 2~4등급 3년, 5등급·인지지원 2년) appeared consistently across search
  results. **The decree text itself was not retrieved**; these values are `[unverified]` and
  are used in §7 only inside a sensitivity, never as a load-bearing input.

### R14 — 금융위원회·금융감독원, 「IFRS17 주요 계리가정 가이드라인」 (2024-11-07)

- Publisher: 금융위원회 / 금융감독원
- Doc type: supervisory guideline — **not retrieved in original**
- URL (release index): https://www.fsc.go.kr/no010101/83351
- Accessed: 2026-09-03
- Retrieved: **no.** The release index page was not opened; the content below comes from
  contemporaneous press accounts (한국경제 2024-11-07, 경향신문 2024-11-07) surfaced in search
  and is therefore **secondary**. The same guideline is cited from a retrieved source as `[R3]`
  in `_research/ci-insurance.md`.
- Key content (secondary): for 무·저해지 contracts the lapse-rate assumption must follow a
  **log-linear model converging to 0% at the premium-completion point** as the principle model,
  with 선형-로그 or 로그-로그 permitted by exception subject to disclosure in the audit report
  and the 경영공시 and quarterly reporting of the difference to the 금융감독원; effective from
  the 2024 year-end close.

### R15 — 헤럴드경제, 「금융당국, 간병인보험 구조 진단 착수」

- Publisher: 헤럴드경제 (biz.heraldcorp.com), H-EXCLUSIVE
- Doc type: **news article** — every figure below inherits that weakness
- URL: https://biz.heraldcorp.com/article/10797305
- Accessed: 2026-09-03
- Retrieved: **yes**
- Key content: 간병인사용일당 loss ratios — life sector near **100% at August 2024**, up 5.3×
  from 18.7% two years earlier; non-life **83.1%**, up 1.7× from 48.1%; some carriers above
  300%. Premium at the five largest non-life carriers grew from ₩101.7bn (1,017억 원) in 2021
  to ₩2.08tn (2조 800억 원) in 2025, about **twenty-fold in four years**. The 금융감독원
  commissioned the 보험연구원 to study a structural overhaul from May 2025, following the 2024
  국정감사. A November 2024 약관 amendment tightened the definition of a 간병인 and the
  documentary requirements (간병계약서, 간병일지, 간호기록 등) without measurably moving the
  loss ratio.

### R16 — 보험신보, 「이슈 — 장기요양등급 인증자 증가하는데」

- Publisher: 보험신보 (insweek.co.kr)
- Doc type: **news / trade-press feature**
- URL: https://www.insweek.co.kr/news/articleView.html?idxno=64798
- Accessed: 2026-09-03
- Retrieved: **yes**
- Key content: the 인정자 / 노인인구 대비 인정률 series 2018–2023 (678,100 / 8.8%; 772,206 /
  9.6%; 857,984 / 10.1%; 953,511 / 10.7%; 1,019,130 / 10.9%; 1.1 million / 11.1%) — the 2020
  onwards values agree with [R4]; private-market penetration at 2023 (손보 신계약 3.95 million
  = 3.85% of 102.5 million; 생보 2.288 million = 2.8% of 82.7 million, up 2.5 and 1.7
  percentage points respectively since 2020); 생명보험협회 2022 survey showing **40.8%** naming
  간병보험 as the cover they would buy next; 2023 급여비 14.5조 원 with 공단부담금 13.2조 원
  and a 재가 62.5% / 시설 37.5% split; a projected fund deficit from 2026 reaching 2.3조 원 by
  2032; and a survey of 2024–2025 product launches (삼성생명 family-carer cover and removal of
  the 120-day hospitalisation cap; 삼성화재 재가 nursing benefits and dementia cover extended
  to age 85; 흥국생명 요양병원 입원 daily benefit ₩50,000–200,000 up to 90 days).

### R17 — 생생비즈, 「치매 환자 100만명 시대 커지는 치매·간병보험 시장…작년 70% 급성장」

- Publisher: 생생비즈 (livebiz.today)
- Doc type: **news article**
- URL: https://www.livebiz.today/news/articleView.html?idxno=6054
- Accessed: 2026-09-03
- Retrieved: **yes**
- Key content: 치매·간병보험 **초회보험료 883억 6,606만 원 for January–November 2024, +70.2%
  year on year**; 계속보험료 2조 835억 원 (2023) → 2조 8,318억 원 (2024), about +36%; estimated
  65+ dementia cases 105만 명 in 2024; private 간병비 spending 8조 원 in 2018 heading above
  10조 원 by 2025; and a product survey naming 교보생명 교보치매·간병안심보험, KB손해보험 KB
  골든케어 간병보험 (with a **CDR 검사지원비 특약**), 흥국화재 (레켐비 / lecanemab cover) and
  한화손해보험.

### R18 — 헬스코리아뉴스, 「노인장기요양보험 인정자수 5년 연속 증가세」 및 백세시대 통계연보
기사

- Publisher: 헬스코리아뉴스 (hkn24.com); 백세시대 (100ssd.co.kr)
- Doc type: **news articles** reporting the 2024 통계연보 launch
- URLs: https://www.hkn24.com/news/articleView.html?idxno=345333 ;
  https://www.100ssd.co.kr/news/articleView.html?idxno=123152
- Accessed: 2026-09-03
- Retrieved: **yes** (both)
- Key content: used only as a cross-check on [R4]. 신청자 1,477,948; 인정자 1,165,030; 판정대비
  인정률 89.5%; 65세이상 인구 10,399,813; the five-year 인정자 series 857,984 (2020) → 953,511
  → 1,019,130 → 1,097,913 → 1,165,030 (2024); 월평균 급여비용 ₩1,495,694 and 공단부담금
  ₩1,365,413 per recipient; 재가급여 9조 2,412억 원 (62.6%) and 시설급여 5조 5,041억 원
  (37.3%); 장기요양기관 29,058 (+2.4%); 종사인력 704,533 (+4.5%); 보험료 부과액 10조 7,772억 원
  (+3.7%). Every one of these that also appears in [R4] agrees with it.

---

## Fact extraction

### 1. Where 간병보험 sits, and what it is not

- **간병보험 is a statutory 보험종목.** 보험업법 제4조제1항제3호 lists 제3보험업 as comprising
  상해보험, 질병보험 and **간병보험** [R12]. It is not a species of 질병보험; it is named
  separately in the licensing article, and both life and non-life carriers may write it. That
  is why the four contract documents in this file come two from life carriers [S1] [S2] and two
  from non-life carriers [S3] [S4] and describe recognisably the same product.
- **It pays 정액 (fixed sums), not indemnity.** The public scheme pays 현물급여 — services
  delivered by a licensed provider, with the recipient paying a 본인일부부담금 — while private
  간병보험 pays 「약정보험금을 일시금(진단자금) 또는 연금(요양자금) 형태로 정액지급」 [R9]. No
  document retrieved reimburses a care invoice. Even the ABL riders that require the insured to
  *have used* 재가급여 or 시설급여 pay a flat ₩100,000 per month, not the cost [S2].
- **The private product predates the public scheme by five years.** 간병보험 was launched in
  **August 2003**; 노인장기요양보험 began in **July 2008** [R9]. The private definitions of the
  early generation were therefore the carriers' own (중증치매 or 활동불능상태, each requiring
  the state to have persisted **90 days or more** with no expectation of improvement) [R9]. The
  realignment onto the public grade came after 2008 and is now near-universal: 「일반적으로
  간병보험에서는 공적기준을 적용하는 경향이 있다」 [R9].
- **Three trigger archetypes are recognised by the supervisor** [R9, quoting a 금융감독원
  release of 2012-07-04]:

  | Type | 보험금 지급사유 |
  |---|---|
  | ① 회사기준 | 중증치매 or 활동불능상태 diagnosed on the carrier's own definition |
  | ② 공적기준 | award of a 장기요양등급 under the public scheme |
  | ③ 혼합형 | a stated grade **and** an activity-limitation or severe-dementia test |

  Every grade-triggered benefit in [S1] – [S4] is type ②. Every CDR-graded dementia benefit in
  [S2] and [S4] is type ①. No type ③ benefit appears in any retrieved document — the hybrid
  form is described in the literature [R9] but was not observed on sale, and any statement that
  it is still written is `[unverified]`.
- **What `LTC_KR_S` therefore models** is a type ② contract. The type ① dementia line is
  modelled as an optional module because it shares the chassis, and because the CDR-graded
  benefit is the commercially dominant form of the product in the 2020s [R17].
- **Relationship to the rest of krlib.** `LTC_KR_S` states its deltas against `Cancer_KR_S`,
  the 정액 제3보험 chassis: same 진단급여금-on-event mechanic, same 면책기간 / 감액기간
  vocabulary, same 무해지환급형 surrender-value suppression. The differences are (i) the
  trigger is an administrative grade rather than a pathological diagnosis, (ii) the benefit has
  an *annuity* form as well as a lump-sum form, and (iii) the state is **not absorbing for
  cash-flow purposes** — an annuity benefit runs while the insured survives, so a post-onset
  mortality basis is required that `Cancer_KR_S` does not need. The LTC trigger also appears
  inside `CI_KR_S` as one of the acceleration events; see `_research/ci-insurance.md` §10 for
  that treatment. The two are deliberately not merged: `CI_KR_S` pays *one* benefit on the
  first of several triggers, whereas `LTC_KR_S` is a standalone contract whose only trigger is
  the grade.

### 2. The public scheme — what the statute actually says

All article text below is the **2018-09-14 consolidation (법률 제15443호)** retrieved through
the 국가법령정보센터 print form; the current law is 법률 제21690호 (시행 2026-05-26) and was
not retrieved article by article [R1]. Where an article has plainly not changed (제23조's list
of 급여 종류 is reproduced verbatim inside a 2025 carrier brochure [S2]) that is noted.

- **제2조 (정의) — who is covered.** 「노인등」 means 「65세 이상의 노인 또는 65세 미만의
  자로서 치매ㆍ뇌혈관성질환 등 대통령령으로 정하는 노인성 질병을 가진 자」 [R1 제2조]. So the
  scheme is **not** an age-65 scheme: a person of any age with one of the listed diseases can
  be certified. 「장기요양급여」 means the 신체활동·가사활동 지원 등 provided to a person
  recognised under 제15조제2항 as unable to perform daily life alone **for six months or
  more**, or the cash paid in lieu [R1 제2조].
- **제15조 (등급판정 등) — the decision.** 「등급판정위원회는 신청인이 제12조의 신청자격요건을
  충족하고 6개월 이상 동안 혼자서 일상생활을 수행하기 어렵다고 인정하는 경우 심신상태 및
  장기요양이 필요한 정도 등 **대통령령으로 정하는 등급판정기준**에 따라 수급자로 판정한다」 [R1
  제15조제2항]. Two things follow. First, the **six-month duration test lives in the statute**,
  which is the Korean equivalent of the 180-day persistence tests that Japanese and French
  products write into their own 약관 — Korea does not need to, because the state has already
  applied one. Second, the grade boundaries themselves are **not in the Act**; they are in the
  시행령, and can be moved by decree.
- **제16조 — the clock.** The determination must be completed **within 30 days** of the
  application, extendable by up to a further 30 days where a detailed investigation is needed
  [R3, citing 법 제16조제1항]. For a monthly-grid model this is short enough to ignore, but it
  matters for the 보장개시일 arithmetic in §11: a 90-day or 180-day waiting period is measured
  from 계약일 to the **판정일**, and the applicant's condition may have existed for months
  before that date.
- **제23조 (장기요양급여의 종류)** [R1 제23조], reproduced verbatim in a 2025 carrier document
  [S2] and therefore current:
  1. **재가급여** — 방문요양, 방문목욕, 방문간호, 주·야간보호, 단기보호, 기타재가급여
     (welfare equipment and home rehabilitation support, defined by 대통령령).
  2. **시설급여** — long-stay admission to a 노인의료복지시설 under 노인복지법 제34조.
  3. **특별현금급여** — 가족요양비 (제24조), 특례요양비 (제25조), 요양병원간병비 (제26조).

  ABL's rider set is written directly onto this taxonomy — 재가급여지원금, 시설급여지원금,
  주야간보호지원금, 복지용구지원금 — and the 약관 explicitly excludes 특별현금급여 from
  counting as either 재가급여 or 시설급여 [S2]. A model that treats "in care" as one state has
  to decide what the ABL riders pay on; §10 sets out why the reference implementation does not
  model them.
- **Which grades may use which benefit.** 「수급자 중 장기요양등급이 1등급 또는 2등급인 자는
  재가급여 또는 시설급여를 이용할 수 있고, 3등급부터 5등급까지인 자는 재가급여만을 이용할 수
  있다」, with three exceptions on which the 등급판정위원회 may permit 시설급여 (family unable
  to care, unsuitable housing, or a condition incompatible with home care) [R6, quoting
  「장기요양급여 제공기준 및 급여비용 산정방법 등에 관한 고시」 제2조]. This is the structural
  reason 1·2등급 is the market's modal private trigger: it is the statutory boundary between
  home care and institutional care.
- **제29조 (장기요양급여의 제한)** is cited inside carrier 약관 as an exclusion: where the
  insured has been awarded a grade but the public benefit is then restricted under 제29조, the
  private benefit is not paid [S2] [S4]. The article itself was not retrieved.
- **본인일부부담금.** On the 2012 consolidation retrieved from a wiki mirror, 제40조 set the
  recipient's share at **15% of the 급여비용 for 재가급여 and 20% for 시설급여**, with
  국민기초생활보장법 recipients excepted. That mirror is an old revision and the current rates
  were not confirmed; the figures are `[unverified]` and are used only as scale-setting in §14.

### 3. 장기요양등급 — the six grades and what triggers each

The score is built from a home visit by a 공단 officer covering **12개 영역 90개 항목** (기본적
일상생활활동 ADL, 수단적 일상생활활동 IADL, 인지기능, 행동변화, 간호처치, 재활, plus disease
and symptom, environment and service-need items), of which **52개 항목** feed the
**장기요양인정점수** [R6]. The bands are set in 시행령 제7조제1항 [R3]:

| 등급 | 장기요양인정점수 | 심신의 기능상태 |
|---|---|---|
| 1등급 | **95점 이상** | 일상생활에서 **전적으로** 다른 사람의 도움이 필요 |
| 2등급 | **75점 이상 ~ 95점 미만** | 일상생활에서 **상당 부분** 다른 사람의 도움이 필요 |
| 3등급 | **60점 이상 ~ 75점 미만** | 일상생활에서 **부분적으로** 다른 사람의 도움이 필요 |
| 4등급 | **51점 이상 ~ 60점 미만** | 일상생활에서 **일정 부분** 다른 사람의 도움이 필요 |
| 5등급 | **45점 이상 ~ 51점 미만** | **치매환자** (노인장기요양보험법 시행령 제2조의 노인성 질병에 해당하는 치매로 한정) |
| 인지지원등급 | **45점 미만** | **치매환자** (동일한 한정) |

Sources: [R3] (the 법제처 restatement, cited to 법 제15조 and 시행령 제7조제1항); [R6] (the
NABO report, which states the same bands and the 52-item derivation); and [S2], where a carrier
reproduces the identical table inside its own 보험안내자료 with the 시행령 제2조 restriction
spelled out.

Three structural points a model must not blur.

1. **5등급 and 인지지원등급 are not the bottom of a severity ladder.** They are a *separate
   gate*: a person scoring below 51 points gets nothing at all unless they have a **dementia
   falling within the 시행령 제2조 list**, in which case they get 5등급 (45–51) or 인지지원등급
   (below 45) [R3] [S2]. A model that treats the six grades as an ordered severity scale and
   interpolates between them is wrong exactly at the two grades that carry the fastest-growing
   private benefit.
2. **인지지원등급 did not exist before 2018-01-01.** It was created to let 경증치매 patients
   with relatively intact physical function use services, and it absorbed part of the former
   등급외 B~C (치매) population [R6, with the transition diagram]. Any experience series that
   crosses that date has a level shift in it.
3. **The 인정점수 is not a linear function of anything an underwriter can observe.** [R11]
   reports the mean 인정점수 of its 271,474 decedents as **82.1 (SD 21.8)** — squarely inside
   2등급 — decomposed as 신체기능 25.5 of 13–36, 인지기능 4.3 of 0–7, 행동변화 1.3 of 0–14,
   간호처치 0.4 of 0–9 and 재활 14.8 of 10–30. The physical and rehabilitation domains dominate
   the total; the cognitive domain contributes at most 7 points out of ~100. That is why a
   dementia sufferer with intact mobility falls below 51 and needs the 5등급 / 인지지원 gate.

### 4. 노인성 질병 — the route in below 65

노인장기요양보험법 시행령 [별표 1], 노인성 질병의 종류 (제2조 관련), 개정 2022-12-20 — the
complete list, verbatim, with KCD codes [R2]:

| | 질병명 | 질병코드 |
|---|---|---|
| 가 | 알츠하이머병에서의 치매 | F00* |
| 나 | 혈관성 치매 | F01 |
| 다 | 달리 분류된 기타 질환에서의 치매 | F02* |
| 라 | 상세불명의 치매 | F03 |
| 마 | 알츠하이머병 | G30 |
| 바 | 지주막하출혈 | I60 |
| 사 | 뇌내출혈 | I61 |
| 아 | 기타 비외상성 두개내출혈 | I62 |
| 자 | 뇌경색증 | I63 |
| 차 | 출혈 또는 경색증으로 명시되지 않은 뇌졸중 | I64 |
| 카 | 뇌경색증을 유발하지 않은 뇌전동맥의 폐쇄 및 협착 | I65 |
| 타 | 뇌경색증을 유발하지 않은 대뇌동맥의 폐쇄 및 협착 | I66 |
| 파 | 기타 뇌혈관질환 | I67 |
| 하 | 달리 분류된 질환에서의 뇌혈관장애 | I68* |
| 거 | 뇌혈관질환의 후유증 | I69 |
| 너 | 파킨슨병 | G20 |
| 더 | 이차성 파킨슨증 | G21 |
| 러 | 달리 분류된 질환에서의 파킨슨증 | G22* |
| 머 | 기저핵의 기타 퇴행성 질환 | G23 |
| 버 | 중풍후유증 | U23.4 |
| 서 | 진전(震顫) | R25.1 |
| 어 | 척수성 근위축 및 관련 증후군 | G12 |
| 저 | 달리 분류된 질환에서의 일차적으로 중추신경계통에 영향을 주는 계통성 위축 | G13* |
| 처 | 다발경화증 | G35 |

비고: 「질병명 및 질병코드는 「통계법」 제22조에 따라 고시된 한국표준질병ㆍ사인분류에 따른다」;
「진전은 보건복지부장관이 정하여 고시하는 범위로 한다」 [R2].

Two observations for pricing.

- The list is **overwhelmingly cerebrovascular and neurodegenerative**, and this shows in the
  data. Of the **58,271** applicants under 65 in 2024, the causes split **뇌혈관질환군 28,628
  (49.1%)**, **치매질환군 15,640 (26.8%)**, **파킨슨질환군 4,086 (7.0%)**, 그 밖의 질병 1,122
  (1.9%), 기타 8,795 (15.1%) [R4 표2-3, shares derived]. By sex the mix differs sharply:
  cerebrovascular disease is 53.8% of male applications under 65 (18,533 of 34,477) but only
  42.4% of female (10,095 of 23,794), while dementia is 24.7% of male and 29.9% of female [R4
  표2-3, derived].
- There is **no cancer on the list**, and no musculoskeletal condition, and no frailty
  category. A person under 65 disabled by cancer or by a hip fracture cannot be certified at
  all. That is the single largest difference from the Japanese scheme, whose 16 特定疾病
  include terminal cancer and 骨折を伴う骨粗鬆症 — and it makes the Korean under-65 exposure
  both smaller and much more concentrated.

### 5. 유효기간, 갱신 and the fact that the grade is not permanent

- The base 장기요양인정 유효기간 is **2 years**; the statute sets a floor of one year and
  delegates the rest to 대통령령 [R1 제19조, retrieved only in summary form]. On **renewal at
  the same grade**, the renewed period is longer: prior to 2025-07-01 it was 1등급 4년, 2~4등급
  3년, 5등급·인지지원등급 2년; from **2025-07-01** it became **1등급 5년, 2~4등급 4년**, with
  5등급 and 인지지원등급 left at 2 years [R13, a vendor restatement of an amendment to 시행령
  제8조 — **the decree text was not retrieved**].
- The practical consequence is visible in the data. Of the **1,165,030** people holding a valid
  certification at end-2024, the route by which the *current* certification was obtained was
  [R4 표2-5]:

  | 인정신청 구분 | 인원 | share (derived) |
  |---|---|---|
  | 인정신청 (first application) | 318,992 | 27.4% |
  | 등급변경신청 (grade change) | 107,365 | 9.2% |
  | 갱신신청 (renewal) | 639,659 | 54.9% |
  | 재신청 (re-application) | 98,983 | 8.5% |
  | 직권재조사 | 31 | 0.0% |
  | 계 | **1,165,030** | 100.0% |

  Renewal is the majority route, and the mix moves sharply by grade. At 인지지원등급 the
  first-application route is **69.8%** (19,436 of 27,835) and renewal only 12.3%; at 1등급 the
  first-application route is **13.3%** (7,371 of 55,340) and renewal **69.5%** [R4 표2-5,
  shares derived]. The reading is straightforward and matters for a model: **1등급 lives are
  overwhelmingly people who have already been in the system for years and have deteriorated
  into the grade**, whereas 인지지원등급 lives are mostly recent first entrants. A private
  contract triggering at 1등급 is therefore not pricing an incidence into 1등급 from health; it
  is pricing a *progression*.
- **Grades move both ways.** 107,365 current certifications came from a 등급변경신청 [R4
  표2-5], and 삼성화재's 「두 번째 장기요양지원금(1~2등급)」 rider is drafted around exactly
  that: it pays where, five years after the first 1·2등급 award, the insured either still holds
  1·2등급 **or** has been re-graded down to 3등급 이하 (「장기요양상태가 아닌 경우도 포함」)
  and is later re-certified at 1·2등급 [S3]. The 약관 also provides that the rider is
  extinguished where the insured has *not* reached 1·2등급 and fewer than five years of the
  policy term remain [S3]. Recovery from the care state is thus explicitly contemplated by at
  least one Korean contract.

### 6. The public statistics — the quantitative basis, 2024

Everything in this section comes from the 2024 노인장기요양보험 통계연보 workbooks [R4], named
table by table. Figures are as at 2024 (the yearbook's convention is a year-end position for
stocks and a calendar-year total for flows). Derived quantities are labelled.

**6.1 Headline stocks and flows** [R4 표2-1, 표2-2, 표2-5, 표1-1]

| Quantity | 2024 |
|---|---|
| 의료보장 적용인구, 전체 | 52,999,168 |
| 의료보장 적용인구, 65세 이상 | **10,399,813** (남 4,613,166 / 여 5,786,647) |
| 인정 신청자 | **1,477,948** (남 445,692 / 여 1,032,256) |
| — of which 65세 미만 | 58,271 |
| — of which 65세 이상 | 1,419,677 |
| 등급 판정 (계) | **1,301,069** |
| — 인정자 | **1,165,030** |
| — 등급외 | 136,039 |
| 판정 대비 인정률 (derived) | **89.5%** |
| 급여이용 수급자 | 1,140,725 |
| 장기요양기관 | 28,403 |

The 89.5% agrees with the figure published in the launch coverage [R18], as do 신청자, 인정자
and the 65+ population.

**6.2 인정자 by grade** [R4 표2-5]

| 등급 | 인원 | 구성비 (derived) |
|---|---|---|
| 1등급 | 55,340 | 4.75% |
| 2등급 | 99,429 | 8.53% |
| 3등급 | 310,717 | 26.67% |
| 4등급 | 536,261 | 46.03% |
| 5등급 | 135,448 | 11.63% |
| 인지지원등급 | 27,835 | 2.39% |
| **계** | **1,165,030** | 100.00% |

By sex: 남 338,714, 여 826,316 — women are **70.9%** of the certified population [R4 표2-5,
derived]. **1·2등급 together are only 13.28%** of all certified lives (154,769 of 1,165,030)
[derived]. Note how far this is from the Japanese distribution in `jplib/_research/
nursing-care.md`, where 要介護2以上 is 50.8% of certified persons: the Korean scale is
concentrated at its *light* end, and a Korean 「1~2등급」 benefit is a much narrower promise
than a Japanese 「要介護2以上」 one. The comparison is not exact — the two scales are
constructed differently — but the direction is unambiguous and it is the single most important
calibration fact in this file.

**6.3 인정자 by five-year age band, and the derived 인정률**

The yearbook's 표2-9 (시·도별 등급별 연령별 자격별 등급 판정 현황) gives, for the national 계
row, the count in each grade and in 등급외 by age band and sex. Its grade columns sum to
1,165,030 and its 등급외 column to 136,039 — i.e. **표2-9 is a stock table of currently valid
determinations**, not a flow of decisions made during the year. Certified counts below are
therefore (계 − 등급외) [R4 표2-9, derived]. Population is [R4 표1-2].

| 연령 | 인정자 (T) | 인구 (T) | **인정률 (T)** | 인정률 (남) | 인정률 (여) |
|---|---|---|---|---|---|
| 65–69 | 66,955 | 3,715,757 | **1.80%** | 1.98% | 1.63% |
| 70–74 | 102,751 | 2,437,413 | **4.22%** | 3.95% | 4.45% |
| 75–79 | 176,578 | 1,796,342 | **9.83%** | 7.45% | 11.76% |
| 80–84 | 320,148 | 1,344,376 | **23.81%** | 15.45% | 29.24% |
| 85+ | 461,622 | 1,105,925 | **41.74%** | 28.63% | 47.31% |
| **65+** | **1,128,054** | **10,399,813** | **10.85%** | **6.87%** | **14.02%** |
| <65 | 36,976 | — | — | — | — |

Underlying age-band counts by sex [R4 표2-9]: 65–69 남 46,146 계 / 10,419 등급외, 여 42,406 /
11,178; 70–74 남 53,877 / 8,519, 여 72,145 / 14,752; 75–79 남 68,490 / 8,604, 여 137,601 /
20,909; 80–84 남 90,505 / 8,828, 여 260,073 / 21,602; 85+ 남 101,099 / 6,693, 여 380,307 /
13,091. Population by band and sex [R4 표1-2]: 65–69 3,715,757 (남 1,803,235 / 여 1,912,522);
70–74 2,437,413 (1,147,409 / 1,290,004); 75–79 1,796,342 (803,983 / 992,359); 80–84 1,344,376
(528,837 / 815,539); 85–89 767,067 (250,684 / 516,383); 90+ 338,858 (79,018 / 259,840).

Four things fall out of this table and all four are load-bearing.

1. **The gradient is roughly a doubling every five years to 80, and steeper after.** From 1.80%
   to 41.74% across four bands is a factor of 23 over twenty years — a force of "morbidity"
   growing at about **17.0% per year of age** on the prevalence scale (derived:
   `(0.41741/0.01802)^(1/20) - 1`). For comparison the Japanese 認定率 runs 4.3% at 65–74 and
   31.1% at 75+ [see `jplib/_research/nursing-care.md` §3]; the Korean 65–74 equivalent is
   about **2.76%** (derived: (66,955 + 102,751) / (3,715,757 + 2,437,413)) and the 75+
   equivalent about **22.57%** (derived: 958,348 / 4,246,643). Korea's certification rate is
   materially *lower* than Japan's at every comparable age, which is consistent with a younger
   scheme, a later start and a tighter score threshold.
2. **The sex crossover is at about age 70.** Below 70 male certification exceeds female (1.98%
   against 1.63%); by 75–79 female exceeds male by 58%; by 85+ by 65%. This reverses the
   direction of a death-benefit rate table and is the same phenomenon observed in the Japanese
   product [see `jplib/_research/nursing-care.md`] and in every carrier premium card in §13
   below, where female 장기요양 rates exceed male at every age.
3. **The grade mix moves with age, but not monotonically** [R4 표2-9, derived]:

   | 연령 | 1등급 | 2등급 | 3등급 | 4등급 | 5등급 | 인지지원 | 1·2등급 계 |
   |---|---|---|---|---|---|---|---|
   | <65 | 11.7% | 10.5% | 30.3% | 36.1% | 8.7% | 2.7% | **22.3%** |
   | 65–69 | 6.5% | 8.1% | 26.8% | 45.5% | 10.0% | 3.0% | **14.6%** |
   | 70–74 | 5.2% | 7.5% | 25.7% | 46.6% | 11.8% | 3.2% | **12.8%** |
   | 75–79 | 4.3% | 7.1% | 24.4% | 47.1% | 13.6% | 3.4% | **11.4%** |
   | 80–84 | 3.8% | 7.3% | 24.6% | 47.6% | 14.0% | 2.8% | **11.1%** |
   | 85+ | 4.7% | 10.1% | 28.9% | 45.3% | 9.7% | 1.4% | **14.8%** |

   The severe share is **U-shaped in age** — high under 65 (22.3%), falling to a minimum around
   80–84 (11.1%), rising again at 85+ (14.8%). The under-65 population is severe because only
   the 노인성 질병 list gets in at all [R2]; the 80–84 trough is where the scheme's marginal
   entrant is a lightly-impaired person newly crossing the 51-point line; the 85+ rise is
   genuine deterioration. **A model that applies a single grade-mix vector at all ages will
   mis-price a 1·2등급 benefit by up to a factor of two.**
4. **The 1·2등급 certification rate itself** — the quantity a 「장기요양(1~2등급)」 benefit is
   exposed to — is [derived from R4 표2-9 and 표1-2]:

   | 연령 | 1·2등급 인정자 | 인구 | **1·2등급 인정률** |
   |---|---|---|---|
   | 65–69 | 9,801 | 3,715,757 | **0.264%** |
   | 70–74 | 13,121 | 2,437,413 | **0.538%** |
   | 75–79 | 20,124 | 1,796,342 | **1.120%** |
   | 80–84 | 35,377 | 1,344,376 | **2.632%** |
   | 85+ | 68,112 | 1,105,925 | **6.159%** |

   Growth here is about **17.0% per year of age** (derived), essentially the same slope as the
   all-grade curve — the severity mix is close enough to flat across 65–85 that the 1·2등급
   curve is a near-parallel shift of the all-grade curve, roughly one seventh of it.

**6.4 The time series** [R4 표1-1; R16; R18]

| 연도 | 인정자 | 65세이상 인구 | 노인인구 대비 인정률 |
|---|---|---|---|
| 2018 | 678,100 | 7,611,770 | 8.8% [R16] |
| 2019 | 772,206 | 8,003,418 | 9.6% [R16] |
| 2020 | 857,984 | 8,480,208 | 10.1% [R16] [R18] |
| 2021 | 953,511 | 8,912,785 | 10.7% [R16] [R18] |
| 2022 | 1,019,130 | 9,377,049 | 10.9% [R16] [R18] |
| 2023 | 1,097,913 | 9,858,810 | **11.14%** (derived) |
| 2024 | 1,165,030 | 10,399,813 | **11.20%** (derived) |

Population is [R4 표1-1]; 인정자 for 2020–2024 is [R18] and agrees with [R4] for 2024; 2018 and
2019 are [R16], a trade-press source. **Note the convention**: the published rate divides *all*
인정자, including the under-65s, by the *65-and-over* population, so it is not a rate in the
demographic sense. The 2023 and 2024 values reproduce the published series to within rounding
when computed that way (11.14% and 11.20% against a published 11.1% for 2023), which confirms
the convention. The **demographically honest 65+ rate for 2024 is 10.85%** (§6.3). Both numbers
appear in Korean commentary and they differ by 0.35 points; a document that quotes one and
compares it against the other is wrong.

The certified population grew **71.8%** between 2018 and 2024 (derived) while the 65+
population grew 36.6% (derived) — so roughly half the growth is demographic and half is a
rising rate, the latter driven mostly by the 2018 creation of 인지지원등급 [R6] and by the
scheme's continuing maturation.

**6.5 Money, for scale** [R4 표5-1; R18]

2024 revenue ₩16,481,847,790 thousand (16조 4,818억 원), of which 보험료 ₩10,777,164,296
thousand (10조 7,772억 원), 국고지원금 ₩2,226,756,000 thousand (2조 2,268억 원) and 의료급여
부담금 ₩3,027,325,035 thousand. Expenditure ₩15,450,696,810 thousand (15조 4,507억 원), of
which 보험급여비 ₩15,089,673,929 thousand and within that 재가급여비 ₩9,424,019,288 thousand.
Per recipient the monthly 급여비용 averaged ₩1,495,694 and the 공단부담금 ₩1,365,413 [R18].
Trade press projects the fund into deficit from 2026, reaching 2조 3,000억 원 by 2032 [R16] — a
news figure, `[unverified]`.

For a benefit-adequacy sanity check on private sums insured, the 2019 재가급여 월 한도액 by
grade was 1등급 ₩1,456,400 / 2등급 ₩1,294,600 / 3등급 ₩1,240,700 / 4등급 ₩1,142,400 / 5등급
₩980,800 / 인지지원등급 ₩551,800 [R6, 2019 values, now stale]. A private 간병연금 of ₩500,000
per month [S1] is therefore roughly a third of the public 재가 ceiling at 1등급 as at 2019, and
the recipient's own 본인부담 on that ceiling would be about ₩218,000 at 15% [derived,
`[unverified]` co-payment rate].

---
### 7. Prevalence to incidence — the conversion, shown rather than assumed

**§6.3 is a prevalence, not an incidence.** It counts people *holding* a certification at a
point in time. A cash-flow model of a 진단급여금 needs the rate at which lives *enter* the
certified state; a model of a 간병연금 needs that entry rate and a post-entry survival basis.
The conversion is the single largest actuarial step in this product and it cannot be done from
the yearbook alone. This section sets out what can be established, what has to be assumed, and
how wide the resulting bracket is.

**7.1 The identity.** In a stationary population the standard relation is

    prevalence  =  incidence  ×  mean duration in the state

so `I(x) ≈ P(x) / D`, with `D` the mean time from certification to exit (exit being death or,
rarely, recovery). The Korean population is not stationary — the certified stock grew 6.1% in
2024 [R18] — so the identity is an approximation, and it understates incidence in a growing
system. Take it as a first-order estimate whose error is of the order of the growth rate.

**7.2 What is known about `D`.** One retrieved study measures it. [R11] followed **271,474**
people certified between 2008-07-01 and 2012-12-31 **who also died within that window**, and
found the mean time from 등급인정 to death to be **516.2 days (1.414 years, SD 430.4)**, with
**8.7%** dying inside one month and **45.6%** inside one year.

This figure **must not be used as `D`**, and the reason is in the study's own design. Only
decedents inside a 4.5-year observation window are in the sample. Anybody certified in 2009 who
was still alive in 2013 — that is, everybody with a long duration — is excluded by
construction. The estimate is right-censored at the window and is therefore a **lower bound**
on the mean duration of the care state. Substituting it into the identity gives, at 65+,

    I(65+)  ≈  10.85% / 1.414  =  7.67% per annum

which is transparently impossible: an entry rate of 7.7% per year sustained against a 10.85%
prevalence would require a mean duration of 1.4 years, and a population in which 45.6% of
entrants die within a year cannot simultaneously support a stock 8.6 times the annual death
count. The arithmetic is its own refutation and is recorded here so that nobody repeats it.

**7.3 A second estimator, from the yearbook's own route table.** [R4 표2-5] classifies the
1,165,030 current certifications by the application type that produced them. **318,992** came
from an **인정신청** — a first application. The validity of a first certification is **2
years** [R13, unverified]. So, approximately, the 인정신청 bucket holds the first-time entrants
of the trailing two years who are still alive, still certified, and have neither renewed nor
applied for a grade change. Writing `E` for annual first entries and `s(t)` for the probability
of remaining in that bucket `t` years after entry,

    318,992  ≈  E · ∫₀² s(t) dt

Using [R11]'s own survival shape as the shape of `s` (a lower bound, since it also has to
absorb exits to 등급변경신청 — 107,365 certifications, 9.2% of the stock, left the bucket that
way) gives `∫₀² s(t) dt` of the order of 1.3–1.5, hence

    E  ≈  318,992 / 1.4  ≈  228,000 per annum   [derived, assumption-dependent]

and therefore, by `stock = E · D`,

    D  ≈  1,165,030 / 228,000  ≈  5.1 years   [derived]

**7.4 A third estimator, from the roll-forward.** 인정자 went from 1,097,913 (2023) to
1,165,030 (2024), a net **+67,117** [R18]. If entries are `E` and exits `X`, then `E − X =
67,117`, and in near-steady state `X ≈ stock / D`. Solving for a range of `D`:

| assumed `D` | implied exits `X` | implied entries `E` | implied 65+ entry rate |
|---|---|---|---|
| 3.0 years | 388,000 | 455,000 | 4.4% |
| 4.0 years | 291,000 | 358,000 | 3.4% |
| 5.1 years | 228,000 | 295,000 | 2.8% |
| 5.5 years | 212,000 | 279,000 | 2.7% |

(derived; the entry rate divides by the 65+ population of 10,399,813, so it is on the same
mixed convention as the published 인정률 and includes under-65 entrants in the numerator).
Directly from the identity `I = P / D` at 65+, with `P = 10.85%`:

| assumed `D` | implied `I(65+)` |
|---|---|
| 3.0 years | 3.62% |
| 4.0 years | 2.71% |
| 5.5 years | 1.97% |

The two routes agree, which is the useful result: **`D` is somewhere near 4–5.5 years and the
all-grade 65+ entry rate is somewhere near 2–3.5% per annum.** That is a factor-of-two bracket
and it is the honest width of what the retrieved evidence supports.

**7.5 Why the same conversion is *wrong* for a 1·2등급 benefit.** Applying `I = P / D` to the
1·2등급 prevalence curve of §6.3 gives, at 65–69 with `D = 4`,

    I₁₂(65–69, male)  ≈  0.2741% / 4  =  0.0685% p.a.   [derived]
    I₁₂(65–69, female) ≈  0.2540% / 4  =  0.0635% p.a.   [derived]

But the 1·2등급 *stock* is not built from direct entries. [R4 표2-5] shows that only **13.3%**
of current 1등급 certifications arose from a first application (7,371 of 55,340) against
**69.5%** from a renewal, whereas at 인지지원등급 the first-application share is **69.8%**
(19,436 of 27,835) [derived]. Severe-grade lives are, in the main, people who entered the
scheme years earlier at a lighter grade and deteriorated. A single-decrement model that treats
`I₁₂` as a healthy-life incidence therefore **overstates the direct entry rate and understates
the delay**, and will put the cash flow years too early. The structurally correct model is
multi-state — healthy → light grade (3–5, 인지지원) → severe grade (1–2) → dead — and
`LTC_KR_S` is built that way, with the light-grade state's exit split between progression and
death. Where the reference implementation collapses it, the collapse is documented and marked
`[std]`.

**7.6 The one disclosed incidence basis.** Exactly one retrieved document publishes a Korean
LTC incidence rate: the 우체국 상품요약서's 예정위험률 table [S1]. It is a *pricing* basis for
an underwritten, 180-day-waited, 2-year-reduced product, not a population rate, and it covers
only three ages and only grades 1 and 2 — but it is the only hard anchor in this file and every
`[std]` incidence assumption in `LTC_KR_S` is calibrated against it. See §16 for the full table
and for the age-gradient and sex-ratio cross-checks, which agree with the population data of
§6.3 in both slope and in the location of the sex crossover.

**7.7 What has to be `[std]`.** No retrieved source gives: a post-certification mortality table
by grade; a recovery or grade-improvement rate; a progression rate between grades; a select
period or an underwriting-selection factor; or a lapse table for a Korean 간병보험. All of
these are `[std]` in `LTC_KR_S`, constrained where possible by [R11] (post-onset mortality
shape), by [R4 표2-5] (progression versus direct entry mix), by [S1] (the level of `I₁₂` at
40/50/60) and by [R14] (the log-linear lapse shape for the 무해지 form).

---

### 8. 치매 and the CDR scale — the second trigger

**8.1 The epidemiology.** The 2023 치매역학조사, run by 중앙치매센터 with 한국보건사회연구원
and 한국갤럽 between 2023-08-22 and 2024-03-18 on a three-stage design (인지선별검사 → 진단검사
→ 실태조사), found [R7]:

| | 2016 조사 | **2023 조사** |
|---|---|---|
| 65세 이상 치매 유병률 | 9.50% | **9.25%** |
| 65세 이상 경도인지장애(MCI) 유병률 | 22.25% | **28.42%** |

Prevalence by age band and by sex [R7]:

| 연령 | 치매 유병률 |
|---|---|
| 65–69 | 4.99% |
| 70–74 | 5.03% |
| 75–79 | 10.70% |
| 80–84 | 15.57% |
| 85+ | 21.18% |
| 남 / 여 (all 65+) | 8.85% / 9.57% |

The release states that prevalence rises sharply from 75 and that the male rate exceeds the
female rate at 65–79 while the female rate exceeds the male at 80 and over [R7] — the same
crossover, at a similar age, as the certification data in §6.3. Projected 추정 치매환자수: 2025
**97만 명**, 2026 **약 101만 명**, 2044 **약 201만 명** [R7].

An older vintage, quoted by a carrier from 「대한민국 치매현황 2023」 (중앙치매센터, 2024-06):
at 2022, 65세 이상 노인인구 **9,010,544** and 65세 이상 치매상병자 **923,003**, a rate of
**10.2%**; and the annual cost of managing one dementia patient rose from **1,851만 원 (2010)**
to **2,220만 원 (2022)** [S2]. The 10.2% and the 9.25% are not the same measure — the former
counts 치매상병자 (people with a dementia diagnosis on health-insurance records), the latter a
survey-diagnosed prevalence — and they should not be compared directly.

[R8] adds the severity split from the 2016 survey vintage: 경증치매 (CDR 1 or 2) prevalence
**6.4%**, i.e. **67% of all dementia cases are mild or moderate**. That single number is the
economics of the whole 치매보험 market: a benefit written at CDR 3 이상 reaches a third of
cases, one written at CDR 1 이상 reaches all of them.

**8.2 The CDR scale itself.** 「CDR 척도(Expanded Clinical Dementia Rating, 2001년)」는
「치매관련 전문의가 실시하는 전반적인 인지기능 및 사회기능정도를 측정하는 검사로, 전체 점수
구성은 0, 0.5, 1, 2, 3, 4, 5의 7등급으로 되어있으며, 점수가 높을수록 중증을 의미합니다」 [S2].
The clinical mapping used in both the carrier literature [S2] and the supervisory analysis
[R8]:

| CDR | 명칭 | 표현 |
|---|---|---|
| 0 | 정상 | — |
| 0.5 | 최경도 / 경도인지기능장애 (MCI) | forgets appointments, misplaces objects, cannot recall familiar names |
| **1** | **경도 치매** | repeats itself, cannot find the right word, apathetic, suspicious, personality change |
| **2** | **중등도 치매** | needs help to go out, disoriented in time, cannot follow a newspaper, gets lost in familiar places, wanders |
| **3 이상** | **중증 치매** | needs help eating, dressing and washing; most memory lost; speech unintelligible; does not recognise family; gait disorder |

Symptom descriptions are [R8]'s 표1; the 0 / 0.5 / 1 / 2 / 3+ grouping is [S2]'s diagram, and
both agree.

**8.3 How the contracts use it.** ABL's definitions, verbatim [S2]:

> 「"경도치매상태"라 함은 CDR 척도(한국판 Expanded Clinical Dementia Rating, 2001년) 검사
> 결과가 **1점**(다만, 이와 동등하다고 국내의학계에서 일반적으로 인정되는 검사 방법을 사용하여
> 이와 동등한 정도로 판정되는 경우를 포함합니다)에 해당되는 상태를 말합니다.」

with 중등도치매상태 at **2점** and 중증치매상태 at **3점 이상**, and in each case the
「최종진단확정」 requires that the state 「그 상태가 진단일부터 **90일 이상 계속되어 장래에 더
이상의 호전을 기대할 수 없는 상태**」 [S2]. 한화손해보험 words the same thing as a threshold
rather than a point: 「"경증이상치매상태"란 … "치매"로 진단확정되고 **90일 이상 CDR척도 1점
이상**의 "경증이상 인지기능의 장애"가 발생한 상태」, and correspondingly 2점 이상 and 3점 이상
[S4].

Note the drafting difference and its effect. ABL's 경도치매상태 is CDR **exactly 1**, so the
경도이상치매 진단급여금 has to be written as an *or* — payable on 경도치매상태 **or**
중등도치매상태 **or** 중증치매상태, once only [S2]. 한화's is CDR **1 이상**, so the tiering
falls out of the definition. The economics are identical; the wording is not, and a reader
comparing 약관 has to notice.

**8.4 Diagnostic procedure — the post-2019 form.** ABL's 약관 wording, which is the shape the
supervisor asked for in 2019 [R10], is [S2]:

> 「… 의료기관의 **치매 전문의(신경과 또는 정신건강의학과)**에 의한 진단서에 의하며, 이 진단은
> 병력청취, 인지기능 및 정신상태 평가, 신체진찰과 신경계진찰, 신경심리검사, 일상생활능력평가,
> 검사실검사, **뇌영상검사** 등 해당 치매의 진단 및 원인질환 감별을 위해 의학적으로 필요한 검사
> 및 그 결과에 대한 종합적인 평가를 기초로 정해지며, **뇌영상검사 등 일부 검사에서 치매의
> 소견이 확인되지 않았다 하더라도 다른 검사에 의한 종합적인 평가를 기초로 치매를 진단할 수
> 있습니다.**」

The final clause is the direct product of the 2019 약관 변경권고 [R10], and it is the single
most important sentence in the Korean dementia-insurance canon: brain imaging is an *input*,
not a *gate*. Before it, carriers wrote imaging as a condition precedent, and [R8] predicted —
correctly — that 「CDR 1점 + 뇌 영상자료상 기질적 이상 없음」 would generate mass dispute.

**8.5 Exclusions specific to dementia.** 「정신분열병이나 우울증과 같은 정신질환으로 인한
인지기능의 장애 및 알콜중독, 의사의 처방에 의하지 않는 약물의 투여로 인한 인지기능의 장애를
원인으로 발생한 "치매", "경도치매상태", "중등도치매상태" 및 "중증치매상태"는 보장대상에서
제외합니다」 [S2]. 한화손해보험's dementia riders carry the same structure and additionally
sell 파킨슨병진단비 with its own one-year 면책 [S4].

**8.6 The relationship between the two triggers.** Dementia is both (i) a route into the public
grade — it is four of the 25 노인성 질병 codes [R2], it is the *sole* qualifying condition for
5등급 and 인지지원등급 [R3], and it is present in **42.3%** of certified decedents [R11] — and
(ii) an independent CDR-graded private trigger [S2] [S4]. A contract carrying both a
장기요양(1~인지지원등급) rider and a 경도이상치매 rider will pay both on the same underlying
event, at different times, on different evidence. That is not double counting in the model —
they are separate benefits with separate sums insured — but the *correlation* is close to one
for the light tiers and a model that treats them as independent decrements will understate the
tail. `LTC_KR_S` handles this by making the dementia module a rider on the same life with a
shared underlying state, not an independent process.

---
### 9. 장기요양 진단급여금 — the lump sum, and how the grade threshold is sold

Every retrieved contract pays a once-only lump sum on first award of a grade at or above a
stated threshold. What varies is which thresholds are on the shelf and whether they are the
main contract or a rider.

**우체국 [S1]** — two separate riders, each 최초 1회에 한함, each extinguishing itself on
payment:

| 특약 | 지급사유 (verbatim) | 지급액 (특약 가입금액 1,000만 원 기준) |
|---|---|---|
| 무배당 장기요양(1~2등급)특약 2309 | 「보험기간 중 장기요양상태 보장개시일 이후에 최초로 **장기요양 1등급 또는 2등급**으로 진단 확정되었을 때 (단, 최초 1회에 한함)」 | 계약일부터 2년 미만 **500만 원** / 2년 이상 **1,000만 원** |
| 무배당 장기요양(1~5등급)특약Ⅱ 2309 | 「… 최초로 **장기요양 1등급, 2등급, 3등급, 4등급 또는 5등급**으로 진단 확정되었을 때 (단, 최초 1회에 한함)」 | 계약일부터 2년 미만 **50만 원** / 2년 이상 **100만 원** |

Note the **ten-to-one ratio of sums insured** between the two riders at the same 특약 가입금액
of 1,000만 원 [S1]. That is the carrier's own statement of the relative frequency of the two
thresholds, and it is a useful sanity check on §6: the 1·2등급 share of the certified stock is
13.28% [derived from R4], so a 1:10 benefit ratio implies the two riders carry broadly similar
expected cost per unit of 가입금액 — which is exactly what one would expect of two riders
priced off the same table. The 정의 in both cases is:

> 「"장기요양상태"라 함은 거동이 현저히 불편하여 장기요양이 필요하다고 판단되어
> 「노인장기요양보험법」 및 관련 법령에 따라 등급판정위원회에서 장기요양 1등급 또는 2등급으로
> 판정받은 경우를 말하며 …」 [S1]

**ABL생명 [S2]** — the grade threshold is the **main contract**, and the wider thresholds are
riders:

| 계약 | 급부명 | 지급사유 | 보장내용 |
|---|---|---|---|
| 주계약 | 장기요양(1~2등급)급여금 | 「「장기요양상태 보장개시일」 이후에 "1~2등급 장기요양상태"로 판정받았을 때 (다만, 최초 1회에 한함)」 | 보험가입금액 |
| 선택특약 | 장기요양(1~5등급)급여금 | 「… "1~5등급 장기요양상태"로 판정받았을 때 (최초 1회)」 | 1,000만 원 |
| 선택특약 | 장기요양(1~인지지원등급)급여금 | 「… "1~인지지원등급 장기요양상태"로 판정받았을 때 (최초 1회)」 | 1,000만 원 |

and its definition adds the age/disease qualification explicitly:

> 「"1~2등급 장기요양상태"라 함은 「만 65세 이상 노인」 또는 「**노인성 질병을 가진 만 65세
> 미만의 자**」로서 거동이 현저히 불편하여 장기요양이 필요하다고 판단되어
> 「노인장기요양보험법」에 따라 장기요양등급판정위원회에서 장기요양 1등급 또는 장기요양
> 2등급으로 판정받은 경우를 말합니다. 이때 노인성 질병이란 치매·뇌혈관성질환 등
> 노인장기요양보험법 시행령에서 정하는 질병을 말합니다.」 [S2]

ABL is the only retrieved carrier selling a **1~인지지원등급** threshold — i.e. cover on the
loosest gate the statute provides.

**삼성화재 [S3]** — a non-life carrier with the widest published threshold menu: 기본계약
장기요양지원금(**1~2등급**), plus selectable 장기요양지원금(**1등급**), (**1~3등급**) and
(**1~4등급**), each 「최초 1회한 지급」 at 가입금액. The 지급사유 is 「보험기간 중 **상해 또는
질병을 직접적인 원인으로** 장기요양상태가 되어 1등급 또는 2등급의 장기요양등급을 받은 경우」
with the note 「※ 장기요양상태라 함은 노인장기요양보험법에 따라 장기요양등급판정위원회에서
장기요양급여수급자로 판정받은 경우를 말함」 [S3]. The 「상해 또는 질병을 직접적인 원인으로」
clause is a non-life drafting habit and appears in [S4] too; no retrieved life-carrier document
has it, and no retrieved document explains what a certification *not* caused by 상해 또는 질병
would be.

**한화손해보험 [S4]** — five 장기요양진단비 covers (1등급, 1~2등급, 1~3등급(1804), 1~4등급,
1~5등급) sold across four plans. The article text, verbatim for the 1등급 cover:

> 제1조(보험금의 지급사유) 「회사는 피보험자가 이 보장의 보험기간 중에 **노인장기요양보험 1등급
> 수급대상으로 인정된 경우**에는 **최초 1회에 한하여** 아래의 금액을 장기요양진단비로
> 보험수익자에게 지급합니다.」

| 구분 | 계약일부터 1년 미만 | 1년 이상 |
|---|---|---|
| 질병 | 이 보장 보험가입금액의 **50%** | 이 보장의 보험가입금액 |
| 상해 | 이 보장의 보험가입금액 | 이 보장의 보험가입금액 |

> 「제1항의 "노인장기요양보험 1등급 수급대상으로 인정된 경우"라 함은 「노인장기요양보험법」에
> 따라 「**국민건강보험공단 장기요양등급판정위원회**」(향후 제도변경시에는 동 위원회와 동일한
> 기능을 수행하는 기관)에 의하여 "1등급"의 장기요양등급을 판정받은 경우를 말합니다.」 [S4]

The parenthetical — "or whatever body succeeds it if the scheme changes" — is drafted into the
definition itself, alongside the separate wholesale-rewriting clause in [S3]. Both carriers
have priced the statutory-change risk and neither has taken it.

**교보생명 [S5]** — 1~5등급 and 인지지원등급 cover with 재가급여 / 시설급여 / 방문요양 이용수당
riders and, unusually, a **premium refund** (「장기요양(1~4등급) 진단 시 주계약 및 보험료
환급대상 특약의 보험료를 돌려주는」) on certification at 1~4등급. That is a return-of- premium
feature on a protection contract and would materially change the reserve; it is a press-release
fact only and the mechanics are `[unverified]`.

**The observed threshold range, consolidated.**

| Threshold | Where observed |
|---|---|
| 1등급 only | 삼성화재 [S3]; 한화손보 [S4] |
| **1~2등급** | 우체국 [S1]; ABL 주계약 [S2]; 삼성화재 기본계약 [S3]; 한화손보 [S4] |
| 1~3등급 | 삼성화재 [S3]; 한화손보 (1804) [S4] |
| 1~4등급 | 삼성화재 [S3]; 한화손보 [S4]; 교보 (premium refund) [S5] |
| **1~5등급** | 우체국 [S1]; ABL [S2]; 한화손보 [S4]; 교보 [S5] |
| 1~인지지원등급 | ABL [S2]; 교보 (rider set) [S5] |

**1~2등급 is the modal main-contract trigger** and 1~5등급 the modal rider. No retrieved
document sells a 3등급-only or 5등급-only benefit; the thresholds are always cumulative from
the top.

### 10. The income forms — 간병연금, 생활자금, 지원금

Three architecturally different ways of paying an income were observed, and the difference
between them is the difference between a two-state and a three-state model.

**10.1 우체국 — a survival-tested annuity with a guarantee and a cap** [S1]. 무배당
장기요양간병비특약Ⅱ 2309, 장기요양(1~2등급)진단간병자금:

> 「보험기간 중 장기요양상태 보장개시일 이후에 최초로 장기요양 1등급 또는 2등급으로 진단
> 확정되고, 진단 확정된 날을 최초로 하여 **10년 동안 매년 진단 확정일에 살아있을 때** (단, 최초
> 1회의 진단 확정에 한함) ※**최초 1년(12개월) 보증지급** ※**10년(120개월)을 최고한도로 지급**」

with the amount, at 특약 가입금액 1,000만 원:

| 경과기간 | 1등급 | 2등급 |
|---|---|---|
| 보험계약일부터 2년 미만 | 매월 **25만 원** | 매월 **15만 원** |
| 보험계약일부터 2년 이상 | 매월 **50만 원** | 매월 **30만 원** |

Six mechanical rules attach and each one is a modelling decision [S1]:

1. **Premium waiver fires on the same event**: 「보험료 납입기간 중 … 장기요양(1~2등급)진단
   간병자금 지급사유가 발생하였을 때에는 **차회 이후의 이 특약의 보험료 납입을 면제**합니다」.
2. **The amount is fixed by the grade at first certification and never re-rated**: 「… 최초로
   진단 확정된 장기요양등급(1등급 또는 2등급)을 기준으로 … 지급액이 결정되며, 그 이후에
   장기요양등급이 **변경되더라도 … 지급액은 변경되지 않습니다**」. So a life that enters at
   2등급 and deteriorates to 1등급 keeps the ₩300,000 rate.
3. **The 감액 decision is likewise frozen at first certification**: 「최초 진단 확정일을
   기준으로 경과기간 2년미만의 보험금 감액여부가 결정됩니다. 따라서 … 그 이후에 도래하는 매년
   진단 확정일이 계약일부터 2년이상에 해당하더라도 … 지급액은 변경되지 않습니다」. A claim that
   starts inside the reduction window stays halved **for the whole ten years**.
4. **The contract cannot be surrendered once the annuity starts**: 「최초 지급사유가 발생한
   후에는 이 특약을 해지할 수 없습니다」.
5. **Death terminates it**, and where death follows a paid instalment no 책임준비금 is
   returned: 「… 지급사유가 발생한 후 사망한 경우에는 별도로 책임준비금을 지급하지 않습니다」.
   Where death precedes any claim, the 책임준비금 at death is paid to the 계약자.
6. **Annual proof of life is required**: 「매년 진단 확정일에 피보험자의 주민등록등본을
   제출하여야 합니다」 [S1, 구비서류].

So the shape is: **monthly amount, tested annually on survival (not on continued
certification), first 12 months guaranteed against death, maximum 120 months.**

**10.2 삼성화재 — a fixed five-year monthly stream** [S3]. 장기요양 생활자금(1~2등급 / 1~3등급
/ 1~4등급)(5년 월지급형): 지급사유 identical to the corresponding 지원금, 지급금액 「**5년간
매월 가입금액**」, 「최초 1회한 지급」. No survival test is stated in the summary table;
whether the stream is 확정 (paid to the estate) or 생존 is not resolved by the retrieved
extract and is `[unverified]`.

**10.3 ABL — utilisation-tested monthly support, some of it for life** [S2]. Six riders, all
paying **1회당 10만 원** at **월 1회 한도**, but each conditioned on the insured *actually
using* a named public benefit:

| 특약 | 지급사유 | 지급기간 |
|---|---|---|
| 장기요양(1-2등급)재가급여**종신**지원특약 | first 1·2등급 판정 **and** 「"재가급여"를 이용하였을 때」 | 「장기요양등급 판정일부터 **최대 종신** 지급」 |
| 장기요양(1-5등급)재가급여지원특약 | first 1~5등급 판정 and 재가급여 이용 | 보험기간 동안 |
| 장기요양(1-인지지원등급)재가급여지원특약 | first 1~인지지원 판정 and 재가급여 이용 | 보험기간 동안 |
| 장기요양(1-인지지원등급)주야간보호지원특약 | … and 주·야간보호 이용 | 보험기간 동안 |
| 장기요양(1-인지지원등급)복지용구지원특약 | … and 복지용구 이용 | 보험기간 동안 |
| 장기요양(1-2등급)시설급여**종신**지원특약 | first 1·2등급 판정 and 시설급여 이용 | 최대 종신 |
| 장기요양(1-5등급)시설급여지원특약 | first 1~5등급 판정 and 시설급여 이용 | 보험기간 동안 |

The counting unit is 「"판정후 보험월" 기준 월 1회 한도」 [S2]. 재가급여 and 시설급여 take
their meanings directly from 노인장기요양보험법 제23조제1항제1호 and 제2호, and 특별현금급여
「는 재가급여 및 시설급여에 해당하지 않습니다」 [S2].

**This is the most model-relevant divergence in the product.** A 우체국-style annuity needs
only a post-onset *survival* basis: once the trigger is met, instalments run for up to ten
years on survival alone, regardless of whether the insured recovers, is re-graded, or stops
using services. An ABL-style 지원금 needs, in addition, a **utilisation** basis: the insured
must be receiving the named benefit in the month, and Korean utilisation is far from universal
(급여이용 수급자 1,140,725 against 인정자 1,165,030 in 2024 [R4] — 97.9% overall, but the
composition by service type is 재가 675,070 방문요양 / 213,428 주야간보호 / 261,051 시설, with
substantial overlap [R4 표3-3]). And an ABL 종신 rider needs a lifetime post-onset survival
basis and is exposed to the whole of the longevity tail with no ten-year cap.

**10.4 교보생명 [S5]** — 「매월 생활자금을 평생 지급」 with a **minimum three-year (36-payment)
guarantee** on early death. A lifetime dementia annuity with a guarantee period; the trigger is
the CDR tier, not the grade.

**What `LTC_KR_S` models.** The reference implementation ships (a) a 진단급여금 at a 1·2등급
threshold as the main benefit, and (b) a 간병연금 on the 우체국 shape — monthly, survival-
tested, 12-month guarantee, 120-month cap, amount frozen at the entry grade — as the optional
income module, because it is the shape whose every rule is documented verbatim in a retrieved
기초서류 extract [S1]. The utilisation-conditioned ABL form is described in `product-spec.md`
as an observed variant and is **not modelled**: no retrieved source gives a utilisation rate by
grade, by service type and by duration since certification, and a module whose central
assumption would be entirely `[std]` adds nothing to a reference implementation.

---
### 11. 면책기간 / 보장개시일 and 감액기간 — the least uniform part of the product

Korean practice separates two mechanisms that both get called "waiting period" in English, and
the 약관 keep them separate:

- **보장개시일** — the date cover *starts*. Before it, nothing is payable and the usual
  consequence of a pre-inception event is that the rider is **void with premiums returned**,
  not merely that the claim is refused.
- **감액기간** — cover has started, but the benefit is paid at a stated fraction (invariably
  50% in the retrieved documents) for a stated period from 계약일.

**11.1 장기요양 benefits — the observed range.**

| Carrier | 장기요양상태 보장개시일 | 감액기간 |
|---|---|---|
| 우체국 [S1] | **180일** — 「계약일[부활(효력회복)일]부터 그 날을 포함하여 **180일이 지난 날의 다음날**」; but 「재해를 직접적인 원인으로 장기요양상태가 발생한 경우 … 계약일[부활일]로 합니다」 | **2년**, 50% (진단보험금 500 / 1,000만 원; 간병자금 25·15 / 50·30만 원). Not applied where the cause is 재해; not applied to 갱신계약 |
| ABL생명 [S2] | **90일** — 「계약일(부활(효력회복)계약의 경우 부활(효력회복)일)부터 그 날을 포함하여 **90일이 지난날의 다음 날**」; 재해 카브백 to 계약일 | **none stated** on the 장기요양 covers |
| 삼성화재 [S3] | **none stated** on 장기요양지원금 or 장기요양 생활자금 | **none stated** |
| 한화손보 [S4] | **none stated** on the five 장기요양진단비 covers | **1년, 50%**, 「질병이 원인인 경우 가입 후 1년간 보험금 50% 지급」; full amount where the cause is 상해 |

So the market runs from **no waiting period at all** [S3] [S4] through **90 days** [S2] to
**180 days** [S1], and from **no reduction** [S2] [S3] through **1 year at 50%** [S4] to **2
years at 50%** [S1]. That is a wider spread than any comparable parameter in this library, and
it is the reason `product-spec.md` has to justify its representative choice explicitly rather
than assert a market convention.

The pre-inception consequence is uniform where it is stated: 「장기요양상태 보장개시일 전일
이전에 장기요양 1등급 또는 2등급으로 진단 확정된 경우에는 **특약을 무효로 하며, 이미 납입한
보험료를 돌려드립니다**」 [S1]; and identically in [S2] («이 계약을 무효로 하며, 이미 납입한
보험료를 돌려 드립니다»). Contrast the Korean cancer chassis, where a pre-inception diagnosis
gives the policyholder an *option* to cancel and a five-year revival if untreated [see
`_research/ci-insurance.md` §11] — the LTC covers have no revival clause at all.

**11.2 치매 benefits — a uniform one year, and a separate 90-day persistence test.**

| Carrier | 치매 보장개시일 | 지속기간 요건 |
|---|---|---|
| ABL생명 [S2] | **1년** — 「계약일 … 부터 그 날을 포함하여 **1년이 지난날의 다음 날**」; carve-back to 계약일 where the cause is 「재해로 인한 뇌의 손상」 | the CDR state must have 「진단일부터 **90일 이상 계속되어** 장래에 더 이상의 호전을 기대할 수 없는」 |
| 한화손보 [S4] | **1년** full exclusion — 「"경증이상치매진단비(90일이상)", "중등도이상치매진단비(90일이상)" 및 "중증치매진단비Ⅲ(90일이상)"의 경우 보험계약일부터 **1년 이내**에 질병을 직접적인 원인으로 해당 치매상태가 90일 이상 계속된 경우에는 보험금을 지급하지 않습니다」 | **90일 이상** (written into the benefit name itself) |

Both carriers also apply a one-year exclusion to 파킨슨병진단비 [S4]. ABL adds a cancellation
right analogous to the cancer chassis: where the 경도 or 중등도 state arose before the
보장개시일, 「진단일로부터 **90일 이내에 이 특약을 취소**할 수 있으며, 이 경우 회사는 이미
납입한 보험료를 돌려 드립니다」 — and if the policyholder does not cancel, the benefit is never
payable for that state, even on a later re-diagnosis after the 보장개시일 [S2].

**The one-year dementia 면책 is the market's post-2019 settlement** and is invariant across the
two documents that carry dementia cover [S2] [S4]. Note that it is a *longer* wait than the
90-day cancer convention and than the 90-day or 180-day 장기요양 waits, which is a direct
consequence of the 2018–2019 anti-selection episode described in §12.

**11.3 삼성화재's 5-year 면책 on the second claim** [S3]. 두 번째 장기요양지원금(1~2등급) has a
genuinely distinct structure: 「**면책기간 최초 1등급 또는 2등급의 장기요양등급판정일부터
5년**」, and the benefit is then payable if, at that 보장개시일, the insured either still holds
1·2등급, or is then at 3등급 이하 (「장기요양상태가 아닌 경우도 포함」) but is later re-graded
to 1·2등급 within the policy term. On reinstatement the clock behaviour depends on what
happened before lapse [S3]. It also extinguishes itself where no 1·2등급 award has happened and
fewer than five years of term remain [S3]. This is a *persistency* benefit — it pays for having
stayed severely dependent for five years — and it needs exactly the continuance basis that §7.7
says nobody publishes.

### 12. The 2018–2019 치매보험 boom, and what the regulator did about it

The sequence, from the retrieved sources:

1. **Pre-2017.** 치매보험 covered **중증치매 (CDR 3점 이상)** only [R8]. On [R8]'s own severity
   split, that reaches about a third of dementia cases.
2. **2017 H2.** Carriers begin including **경증치매 (CDR 1점 또는 2점)** [R8].
3. **November–December 2018.** A carrier launches a product covering mild dementia and the
   market follows within weeks. [R8] describes 「보험회사들이 기존의 중증치매 중심에서
   경증치매로 보장을 확대한 치매보험을 경쟁적으로 출시하면서 단기간에 판매가 크게 증가」.
4. **The size of it.** 치매보험 초회보험료 for 2018 was **약 233억 원, 3.5× the prior year**;
   at non-life carriers **약 46억 원, 6.5×** [R8]. A trade-press account puts sales at
   **800,000 policies in three months** and a cumulative **2,804,103 policies across 33
   carriers by October 2019** with **142 products** on sale [`[unverified]` — these two figures
   come from a search snippet of a 디멘시아뉴스 article that was retrieved but did not carry
   them in the body text that came back].
5. **The abuse.** Three things, all named by the supervisor's own analyst [R8]: (i) 경증치매
   sums insured were set 「증상에 비해 지나치게 높게」, with **최대 3천만 원** offered for a
   CDR 1 diagnosis; (ii) duplicate purchase across carriers was possible, so the aggregate
   exposure on one life was unbounded; (iii) the 약관 required 「CDR 척도**뿐만 아니라
   뇌영상검사 등을 기초로 한** 진단」, which [R8] predicted would produce 「대량 민원·분쟁」 on
   the fact pattern 「CDR 1점 + 뇌 영상자료상 기질적 이상 없음」.
6. **March 2019 — first intervention.** 금융감독원 issues a 「치매보험 상품 운영 시 유의사항
   안내」 and a public 보도참고자료 (2019-03-28) telling consumers to check the 경증치매
   진단기준 and announcing that duplicate-purchase controls and 불완전판매 would be inspected
   [R8, citing the 금융위원회 release of 2019-03-28; the release itself was not retrieved — see
   §Fetch failures]. Carriers respond by setting an internal **aggregate limit of ₩30,000,000**
   across the market [R8].
7. **July 2019 — second intervention, and the durable one.** 금융감독원 announces a **약관
   변경권고** on 2019-07-02 requiring (i) diagnosis on a comprehensive clinical assessment of
   which 뇌영상검사 is one component, and (ii) **deletion of 특정 치매질병코드 and 약제투약
   conditions** that had been added as payment conditions without rational basis, so that the
   benefit is payable 「전문의에 의해 치매로 진단되고, 보장대상 CDR척도 기준에 부합하는 경우」.
   Revised products on sale from **October 2019** [R10].
8. **The settled design.** Every dementia benefit in the retrieved 2023 and 2025 documents
   carries: a CDR threshold, a **90-day persistence** requirement, a **one-year 면책기간**, a
   requirement that the diagnosis be by a 신경과 or 정신건강의학과 specialist, the explicit
   statement that a negative brain scan does not defeat the claim, and an exclusion for
   cognitive impairment caused by psychiatric illness, alcohol or unprescribed drugs [S2] [S4].

**What a modeller should take from this.** The 2018-generation contracts and the
2020-generation contracts are not the same product, and any Korean 치매 experience series that
spans 2019 is contaminated at the level of the benefit definition, not merely of the rate. The
90-day persistence test and the one-year 면책 together defer a mild-dementia claim by at least
fifteen months from inception and by at least three months from first diagnosis; the effect on
the first-two-years claim cost is large and is the reason a naive prevalence-based pricing of a
CDR 1 benefit will be badly wrong at short durations.

### 13. Premium rate cards — what carriers actually charge

**13.1 ABL생명, 일반심사형** [S2]. 월납, 원. Basis: 주계약 보험가입금액 1,000만 원, 90세만기,
20년납; 특약 보험가입금액 1,000만 원 (except 장기요양(1-인지지원등급)보장특약 at 500만 원),
90세만기, 20년납; 갱신형 특약 10년만기 전기납, 최초계약.

| 담보 | 남 40 | 남 50 | 남 60 | 여 40 | 여 50 | 여 60 |
|---|---|---|---|---|---|---|
| 주계약 (장기요양 1~2등급급여금) | 3,300 | 4,000 | 4,900 | 5,000 | 6,200 | 7,900 |
| 장기요양(1-5등급)보장특약 | 15,010 | 20,070 | 27,830 | 17,890 | 23,920 | 33,890 |
| 장기요양(1-인지지원등급)보장특약 *(500만 원)* | 7,620 | 10,195 | 14,155 | 9,030 | 12,080 | 17,150 |
| 장기요양(1-2등급)재가급여**종신**지원특약 | 580 | 760 | 1,000 | 850 | 1,120 | 1,480 |
| 장기요양(1-5등급)재가급여지원특약 | 4,830 | 6,450 | 8,830 | 6,460 | 8,630 | 12,140 |
| 장기요양(1-인지지원등급)재가급여지원특약 | 5,330 | 7,110 | 9,770 | 7,180 | 9,600 | 13,540 |
| 장기요양(1-인지지원등급)주야간보호지원특약 | 950 | 1,270 | 1,770 | 1,450 | 1,940 | 2,740 |
| 장기요양(1-인지지원등급)복지용구지원특약 | 1,840 | 2,450 | 3,340 | 2,740 | 3,660 | 5,150 |
| 장기요양(1-2등급)시설급여**종신**지원특약 | 540 | 710 | 930 | 1,150 | 1,520 | 2,030 |
| 장기요양(1-5등급)시설급여지원특약 | 1,630 | 2,170 | 2,960 | 2,910 | 3,880 | 5,480 |
| 경도이상치매진단특약 | 17,400 | 23,200 | 31,790 | 13,920 | 18,510 | 25,060 |
| 중등도이상치매진단특약 | 11,750 | 15,620 | 21,010 | 9,530 | 12,660 | 16,960 |
| 중증치매진단특약 | 5,710 | 7,590 | 10,110 | 5,460 | 7,250 | 9,650 |
| 치매통원보장특약 | 355 | 471 | 621 | 556 | 738 | 975 |
| 간병인사용지원입원보장특약 | 14,670 | 17,620 | 20,000 | 17,700 | 21,370 | 23,800 |
| 급여가정간호치료보장특약 | 570 | 740 | 950 | 880 | 1,150 | 1,500 |

The same document publishes the **간편심사형** (simplified-underwriting) card, which is the
cleanest published measure of the price of relaxed underwriting in Korean LTC [S2]:

| 담보 | 남 40 | 남 50 | 남 60 | 여 40 | 여 50 | 여 60 |
|---|---|---|---|---|---|---|
| 주계약 | 4,500 | 5,600 | 7,000 | 6,800 | 8,700 | 11,200 |
| 장기요양(1-5등급)보장특약 | 18,770 | 25,220 | 35,880 | 21,080 | 28,310 | 47,540 |
| 간병인사용지원입원보장특약 | 24,200 | 29,080 | 33,130 | 31,780 | 38,170 | 42,010 |

Ratios (derived): the 간편심사 loading on the main contract is **1.36 – 1.43×** at every age
and sex; on the 1~5등급 rider **1.25 – 1.40×**; on the 간병인사용 rider **1.65 – 1.80×**. The
underwriting questions that buy that loading are four, and the fourth is the one that matters
here: 「현재 노인장기요양보험에 의한 장기요양급여 수급자이거나 **장기요양인정 심의
중**입니까?」 [S2]. The other three are the standard 3개월 / 2년 / 5년 간편고지 questions, with
the 5-year question naming 「암, 간경화증, 뇌졸중, **경도인지장애, 치매** 또는 파킨슨병」 [S2].

Five structural facts fall out of the ABL card and all five belong in a calibration.

- **Female rates exceed male on every 장기요양 cover at every age** — the ratio runs 1.19–1.61
  and *widens* with age on the 시설급여 riders (여 60 / 남 60 = 2.18 on 1-2등급 시설급여종신)
  [derived]. This is the reverse of a death-benefit table and matches the population sex ratio
  of §6.3.
- **Female rates are *below* male on every 치매 cover** — 경도이상치매 여 40 ₩13,920 against 남
  ₩17,400, a ratio of 0.80 [derived]. Dementia diagnosis benefits and long-term-care grade
  benefits therefore run in **opposite sex directions** in the same document. The most likely
  explanation is competing risk: the male dementia rate at 65–79 exceeds the female [R7], and
  the female advantage only appears at 80+, by which age much of the male exposure has died.
- **The severity ladder is priced roughly 3 : 2 : 1.** At 남 40, 경도이상 ₩17,400 : 중등도이상
  ₩11,750 : 중증 ₩5,710 = 3.05 : 2.06 : 1.00 [derived]. So moving the trigger from CDR 3 to CDR
  1 roughly **triples** the price. Compare [R8]'s epidemiology, which says 경증치매 (CDR 1–2)
  is 67% of cases and 중증 the remaining 33% — implying a 3:1 ratio on prevalence alone
  [derived]. The market price and the epidemiology agree closely, which is reassuring and is
  the strongest available check that the post-2019 CDR definitions are being priced off
  something real.
- **The threshold ladder on the grade benefit is priced about 4.5 : 1.** At 남 40, the 1~5등급
  rider is ₩15,010 against the main contract's ₩3,300 at the same 가입금액 [derived]. Against a
  1·2등급 share of certified lives of 13.28% [derived from R4] — implying about 7.5 : 1 on
  frequency alone — the 4.5 : 1 price ratio says that severe-grade claims are *later* on
  average, which is exactly what §7.5's progression argument predicts.
- **The 종신 riders are cheap and the term riders are not.** 장기요양(1-2등급)재가급여종신
  costs 남 40 ₩580 for ₩100,000 a month for life, against ₩4,830 for the 1~5등급 version
  payable only to age 90 [S2]. The 4.5:1 threshold ratio again dominates the lifetime/term
  difference.

**13.2 우체국 — the surrender-value progression rather than a rate card** [S1]. Basis: 주계약
보험가입금액 1,000만 원, **50세**, 90세만기, 20년납, 월납, 원. 1종(일반가입):

| 경과기간 | 남 납입보험료 | 남 해약환급금 | 여 납입보험료 | 여 해약환급금 |
|---|---|---|---|---|
| 1년 | 45,600 | 5,500 | 19,200 | 0 |
| 3년 | 136,800 | 75,800 | 57,600 | 32,000 |
| 5년 | 228,000 | 147,800 | 96,000 | 66,200 |
| 7년 | 319,200 | 209,900 | 134,400 | 94,000 |
| 10년 | 456,000 | 306,300 | 192,000 | 137,400 |
| 20년 | 912,000 | 640,600 | 384,000 | 291,400 |
| 30년 | 912,000 | 528,000 | 384,000 | 253,300 |
| 40년 | 912,000 | — | 384,000 | — |

The annual premium implied by the table is **남 ₩45,600 / 여 ₩19,200** at age 50 [derived: the
1-year 납입보험료 row], i.e. **₩3,800 and ₩1,600 a month** — a *male* premium 2.375 times the
female, the opposite sign to ABL's 장기요양 covers [S2]. The explanation is that 우체국's
**주계약 pays only a 재해사망보험금** (「보험기간 중 재해를 직접적인 원인으로 사망하였을 때」,
1,000만 원 at a 가입금액 of 1,000만 원; on non-accidental death the 책임준비금 is returned to
the 계약자) [S1]. The male/female ratio of 2.375 tracks the 재해사망률 ratio of 4.69 at age 50
in §16 [derived], diluted by expense loadings. **Do not read [S1]'s ₩45,600 as an LTC
premium**: every 장기요양 cover at 우체국 is a rider and no rider rate is published in the
요약서. The mandatory 입원간병인사용특약 pays 「8시간미만 3만원 / 8시간이상 6만원」 per day of
carer use in a non-요양병원 hospital [S1] — a hospital- days indemnity, and the reason the
product is called 간병비보험 rather than 장기요양보험.

The 2종(간편가입) card is the same shape at a **1.16× loading** on the male 납입보험료 (₩52,800
against ₩45,600 at the 1-year row) and **1.31×** on the female (₩25,200 against ₩19,200)
[derived].

**13.3 ABL 해약환급금 progression** [S2]. Basis: **40세**, 주계약 1,000만 원, 90세만기, 20년납,
월납, 원. 일반심사형:

| 경과기간 | 남 납입보험료 | 남 해약환급금 | 남 환급률 | 여 납입보험료 | 여 해약환급금 | 여 환급률 |
|---|---|---|---|---|---|---|
| 1년 | 39,600 | — | 0.0% | 60,000 | — | 0.0% |
| 5년 | 198,000 | — | 0.0% | 300,000 | — | 0.0% |
| 10년 | 396,000 | — | 0.0% | 600,000 | — | 0.0% |
| 15년 | 594,000 | — | 0.0% | 900,000 | — | 0.0% |
| **20년** | 792,000 | **385,700** | **48.7%** | 1,200,000 | **620,000** | **51.7%** |
| 30년 | 792,000 | 431,150 | 54.4% | 1,200,000 | 733,450 | 61.1% |
| 40년 | 792,000 | 400,050 | 50.5% | 1,200,000 | 715,400 | 59.6% |
| 50년 | 792,000 | — | 0.0% | 1,200,000 | — | 0.0% |

This is the **무해지 cliff in its purest published form**: nil for the whole 20-year
premium-paying period, then a step to 48.7% / 51.7% at 납입완료, a slow rise to a peak around
duration 30, and a decline to nil at the 90세 maturity of a pure protection contract. The
간편심사형 table has the same shape with slightly higher 환급률 (50.6% / 53.8% at 20 years,
peaking at 57.6% / 64.3%) [S2].

---
### 14. 갱신형 vs 비갱신형, and the term/premium-term grids

**14.1 The two architectures observed.**

- **우체국 [S1]** puts the 장기요양 benefits on **비갱신형** riders coterminous with the main
  contract (85 / 90 / 100세 만기, 10 / 15 / 20 / 30년납, 「주계약과 동일한 보험기간, 보험료
  납입기간, 보험료 납입주기로 가입 가능」) and puts the **간병인 hospital-days benefits on 5년
  / 10년 갱신형** riders. The renewal procedure is written out: 「보험기간 만료일 30일 전까지
  계약자에게 서면 또는 전화(음성녹음) 안내 → 보험기간 만료일 15일 전까지 계약자의 별도
  의사표시가 없으면 **자동갱신**」, the last renewal running to the main contract's expiry, and
  「갱신계약의 보험료는 **나이의 증가, 적용 기초율의 변동** 등의 사유로 인상될 수 있음」 [S1].
- **ABL생명 [S2]** does the same split: the 장기요양 and 치매 covers are non-renewable and
  coterminous with the 주계약 (90 / 95 / 100세만기, 10 / 15 / 20 / 30년납), while the 노인성
  질환 riders (관절염수술, 인공관절치환, 중증무릎관절연골손상, 대상포진, 통풍) are 「10년 만기
  자동갱신부 특약으로 보험료는 100세(주계약 보험기간이 90세만기일 경우에는 90세, 95세 만기일
  경우에는 95세)까지 계속 납입하여야 합니다」 [S2].
- **삼성화재 [S3]** and **한화손보 [S4]** are non-life long-term products (장기보장성보험) and
  the retrieved extracts show no renewal mechanic on the 장기요양 covers at all.

**So the Korean LTC benefit itself is written 비갱신형** on every document retrieved, and the
갱신형 machinery attaches to the hospital and musculoskeletal riders that travel with it. That
is the opposite of the Korean *medical* market, where 갱신 is the defining feature [see
`_research/indemnity-medical.md`], and it is the right answer for a benefit whose claim arrives
thirty years after issue — a renewable LTC rider re-rated at attained age would price itself
out of existence exactly when it was needed. `LTC_KR_S` is therefore a **level-premium,
non-renewable** contract, and the renewable form is not modelled.

**14.2 The term and premium-term grids.**

| Carrier / product | 보험기간 | 납입기간 | 가입나이 |
|---|---|---|---|
| 우체국 주계약, 1종(일반가입) [S1] | 85 / 90 / 100세만기 | 10·15·20·30년납 | 만15~55세 (10·15·20·30년납), 56~65세 (10·15·20년납), 66~70세 (10·15년납) |
| 우체국 주계약, 2종(간편가입) [S1] | 85 / 90 / 100세만기 | as above | 30~55 / 56~65 / 66~70세 on the same 납입 grid |
| 우체국 장기요양(1~2등급)특약 [S1] | 85 / 90 / 100세만기 | 10·15·20·30년납 | 30~70 (10·15년납), 30~65 (20년납), 30~55 (30년납); 가입금액 capped at 2,000만 원 where 가입 age ≥ 61 |
| 우체국 장기요양(1~5등급)특약Ⅱ, 장기요양간병비특약Ⅱ [S1] | as above | as above | same, tightening at 100세만기 (e.g. 30년납 남 30~49 / 여 30~48); 가입금액 fixed 500만 원 where age ≥ 61 |
| ABL 주계약, 일반심사형 [S2] | 90 / 95 / 100세만기 | 10·15·20·30년 | **25세 ~ 최대 75세** |
| ABL 주계약, 간편심사형 [S2] | 90 / 95 / 100세만기 | 10·15·20·30년 | **30세 ~ 최대 75세** |
| 삼성화재 기본계약 [S3] | 90 / 100세만기 | 전기납 / 80세납 / 20년납 | 만15~57세 (100세만기 전기납), 만15~59 (80세납), 만15~60 (20년납); 만15~60 on 90세만기 전기납 |
| 삼성화재 장기요양(1~3 / 1~4등급) 특약 [S3] | 90 / 100세만기 | 전기납 / 80세납 / 20년납 | **만15~37세** on 100세만기 전기납 — the tightest issue-age limit in the file |
| 교보 [S5] | 종신 | 5·10·15·20년납 | 30~75세 |

Three observations. First, **the whole market issues from about 15–30 to about 70–75** — much
younger at the bottom end than the Japanese products in `jplib`, which cluster at 40–79, and
much younger than the age at which any claim can arise. A 30-year-old buying a 1·2등급 benefit
is buying a claim expected around age 85. Second, **maturity is 85 / 90 / 95 / 100세 or 종신**;
nothing in the file matures before 85, which is the minimum term at which the benefit means
anything given §6.3. Third, **the issue-age envelope narrows as the term lengthens**, which is
the ordinary consequence of a level-premium contract with a benefit concentrated at the far
end: 삼성화재 will write a 100세만기 전기납 1~4등급 benefit only to age 37 [S3].

**14.3 계약 preservation and mechanics** [S1] unless noted.

- **보험료 납입유예기간**: 「납입기일부터 납입기일이 속하는 달의 **다음 다음달의 마지막
  날**까지」, and the contract is terminated 「유예기간이 끝나는 날의 다음 날」.
- **부활(효력회복)**: 「계약이 해지된 날부터 **3년 이내**」 on payment of arrears with
  interest. Note that reinstatement **restarts the 보장개시일 clock** — every 장기요양 and 치매
  waiting period in [S1] and [S2] is measured 「계약일[부활(효력회복)일]부터」.
- **지정대리청구인**: mandatory practice on the LTC riders, because the insured who reaches
  1등급 usually cannot claim. 우체국's 요약서 makes it near-compulsory: 「계약자가 본인을 위한
  계약을 체결하는 경우 체신관서는 **원칙적으로 지정대리청구인을 지정하도록 하여야 합니다**」,
  and the office must operate 「장기요양상태로 인한 보험금 청구불능을 방지하기 위한 적정한 관리
  체계」 [S1]. The eligible persons are 「피보험자의 가족관계등록부상의 배우자 또는 3촌 이내의
  친족」, up to two, one designated as 대표대리인 [S1]; 삼성화재 requires a handwritten or
  voice-recorded acknowledgement at proposal for the same reason [S3].
- **Claim evidence**: for a 장기요양상태 claim the document required is the **장기요양인정서**;
  for the 간병자금 annuity, 「매년 진단 확정일에 피보험자의 **주민등록등본**을 제출」 [S1].
- **Fraudulent certification**: 「피보험자가 장기요양등급을 판정 받았으나 **허위 또는 부당
  판정사실이 확인되는 경우**, 체신관서는 … 보험금을 지급하지 않습니다」 [S1]; identically in
  [S2], which adds refusal where the public benefit is restricted under 법 제29조.
- **General exclusions** are the Korean standard: 피보험자의 고의, 보험수익자의 고의, 계약자의
  고의 [S1]; and on the non-life side additionally 알코올중독·습관성 약품 또는 환각제,
  전쟁·외국의 무력행사·혁명·내란·사변·폭동, and 임신·출산·산후기 [S4].
- **납입면제**: [S2] waives on a 장해지급률 50% 이상 state from one accident; [S1] waives the
  간병자금 rider's own premiums on the annuity trigger; [S3] waives 기본계약 and every attached
  rider where the 기본계약's waiver event occurs, and the 기본계약's waiver event is the award
  of 1등급 or 2등급 [S3]. Only [S3] makes the grade award itself a whole-contract waiver
  trigger.

### 15. 무해지환급형 / 저해지환급형 — the surrender-value forms

Every retrieved LTC contract is sold in at least two forms, and the suppressed-surrender-value
form is the headline one.

- **ABL, 「해약환급금 미지급형」** [S2] — the strongest form. 「보험료 납입기간 중 계약이
  해지될 경우 **해약환급금을 지급하지 않으며**, 보험료 납입기간이 완료된 이후 계약이 해지될
  경우 해지율을 적용하지 않는 동일한 보장내용의 상품(이하 '기본형')의 해약환급금 대비 적은
  해약환급금을 지급합니다」, and specifically 「보험료 납입기간이 완료된 이후 … **'기본형'
  해약환급금의 50%**에 해당하는 금액」. The 「기본형」 is a notional comparator that cannot be
  bought: 「'기본형'은 보험료 및 해약환급금(환급률 포함)의 비교, 안내만을 위한 상품으로 가입이
  불가능하며, '기본형'의 해약환급금은 이 계약의 「보험료 및 해약환급금 산출방법서」에서 정한
  방법에 따라 **해지율을 적용하지 않고** 계산합니다」. The disclosure obligations are set out
  in the 사업방법서 별첨 제1호 and require a signed acknowledgement [S2].
- **한화손해보험, 「납입중50%해약환급금지급형」** [S4] — the 저해지 form. 「보험료 납입기간 중
  계약이 해지될 경우 **간병치매보장플랜(표준형) 해약환급금의 50%**를 지급하며, 보험료 납입이
  완료되고 납입기간이 종료된 이후 계약이 해지되는 경우에는 … **표준형의 해약환급금과 동일한
  금액**을 지급합니다」. So 한화 suppresses to 50% *during* the paying period and restores to
  100% after it, whereas ABL suppresses to nil during and to 50% after. **These are two
  materially different products** and the words look almost the same.
- **삼성화재 [S3]** sells the pure-protection form with no maturity value at all — 「만기환급금
  : 없음」 and 「이 상품은 순수보장성보험으로 보험계약 만기시 지급받는 금액(만기환급금)이
  없습니다」 — and the retrieved extract does not describe a 무·저해지 variant.
- **우체국 [S1]** is the outlier: it is a conventional 표준형 with a normal surrender value
  from year 1 (see §13.2), computed as 「순보험료식 책임준비금에서 **미상각신계약비**를 공제한
  금액」. Korea Post insurance is not written under 보험업법 and is not obliged to follow the
  industry's 무해지 practice.

The **cliff** in ABL's published table (§13.3) — 0.0% for fifteen years, then 48.7% at 납입완료
— is the shape the whole Korean protection market has adopted and is the reason the lapse
assumption on these contracts drew supervisory attention in 2024. [R14] requires the lapse-rate
assumption on 무·저해지 business to follow a **log-linear model converging to 0% at 납입완료**,
with alternatives permitted only on disclosure and quarterly reporting of the difference;
effective from the 2024 year-end close. That constraint is what `LTC_KR_S`'s `lapse_rate` shape
is built to satisfy, and the `[std]` justification in `technical-notes.md` cites it. **Note
that [R14] itself was not retrieved** — see §Fetch failures — and the description here is from
contemporaneous press accounts.

### 16. The disclosed pricing basis — 예정이율 and 예정위험률

This is the single most valuable table in the file. 우체국's 상품요약서 publishes, for 무배당
우체국간병비보험 2309, the **예정위험률** used to price the contract, at ages 40, 50 and 60 by
sex [S1]. No other retrieved Korean LTC document publishes any rate at all.

**예정이율**: 「무배당 우체국간병비보험 2309의 주계약 및 특약에 적용한 예정이율은 **연단위 복리
2.0%**입니다」 [S1].

**예정위험률, 1종(일반가입)** [S1]:

| 위험률 | 성 | 40세 | 50세 | 60세 |
|---|---|---|---|---|
| 재해사망률 | 남 | 0.000340 | 0.000685 | 0.000896 |
| | 여 | 0.000090 | 0.000146 | 0.000215 |
| 질병 및 재해 입원간병인사용률 (1일 이상 180일 한도, 요양병원 제외, 1일당 간병인 8시간 이상 사용) | 남 | 0.494541 | 0.718392 | 1.074819 |
| | 여 | 0.532109 | 1.006769 | 1.154830 |
| **요양(1등급) 발생률** | 남 | **0.000028** | **0.000080** | **0.000237** |
| | 여 | **0.000010** | **0.000046** | **0.000209** |
| **요양(2등급) 발생률** | 남 | **0.000018** | **0.000072** | **0.000293** |
| | 여 | **0.000007** | **0.000042** | **0.000250** |

**예정위험률, 2종(간편가입)** [S1]:

| 위험률 | 성 | 40세 | 50세 | 60세 |
|---|---|---|---|---|
| 간편고지 재해사망률 | 남 | 0.000439 | 0.000788 | 0.001071 |
| | 여 | 0.000104 | 0.000184 | 0.000252 |
| 간편심사 질병 및 재해 입원간병인사용률 | 남 | 0.971488 | 1.397091 | 1.953230 |
| | 여 | 1.208050 | 2.062466 | 2.303485 |

No 요양 발생률 is published for the 간편가입 form, because the 장기요양 riders are 「주계약
1종(일반가입)에 한하여 부가 가능」 [S1].

**What the LTC rates say.** All arithmetic below is derived from the table.

1. **Age gradient.** The 1등급 rate multiplies by **2.86** from 40 to 50 and by **2.96** from
   50 to 60 for males — an annual compounding of **11.1%** and **11.5%**. For females the
   multipliers are **4.60** and **4.54**, i.e. **16.5%** and **16.3%** a year. The 2등급 rate
   grows at **14.9% / 15.1%** (남) and **19.6% / 19.5%** (여). Compare the population
   prevalence gradient of §6.3, which is **17.0% a year of age** for both the all-grade and the
   1·2등급 curves. The female pricing gradient sits right on it; the male pricing gradient is
   materially flatter. Since prevalence growth is incidence growth plus duration effects, and
   duration shortens with age, one would expect the incidence gradient to be *steeper* than the
   prevalence gradient, not flatter — so the male rates look conservative at 40 relative to 60,
   or the female rates aggressive at 40. Either way the table is a rate card for a select,
   underwritten population, not an estimate of population incidence, and the difference is
   exactly the selection effect a model has to represent.
2. **Sex ratio, and the crossover.** Female / male on the 1등급 rate is **0.357** at 40,
   **0.575** at 50 and **0.882** at 60; on the 2등급 rate **0.389 / 0.583 / 0.853**.
   Extrapolating the observed convergence puts the crossover between about **62 and 68**, which
   is precisely where §6.3 finds it in the population (male 1.98% against female 1.63% at
   65–69, reversing by 70–74). **The disclosed pricing basis and the national statistics agree
   on the sex crossover to within a few years**, which is the strongest internal consistency
   check available in this file, and it is why `LTC_KR_S`'s `[std]` incidence table is built
   with a sex ratio that crosses one in the late 60s.
3. **1등급 versus 2등급.** At 40 the 1등급 rate *exceeds* the 2등급 rate (남 0.000028 against
   0.000018); by 60 it is below it (0.000237 against 0.000293). The crossover is between 50 and
   60 for both sexes. That inversion is real and it matters: at young ages the severe grade
   dominates, because the only route in below 65 is a 노인성 질병 catastrophe — a major stroke
   or an early dementia — which lands at a high grade, and §6.3 confirms it (**22.3%** of
   under-65 certified lives are 1·2등급 against 11.1% at 80–84). At older ages the light-grade
   entry route opens up and 2등급 becomes the more common first landing.
4. **Combined 1·2등급 incidence** (derived by summing the two rows, which is an upper bound
   since the events are mutually exclusive at first certification): 남 **0.000046 / 0.000152 /
   0.000530** and 여 **0.000017 / 0.000088 / 0.000459** at 40 / 50 / 60.
5. **Cross-check against §7.5.** The prevalence-implied 1·2등급 incidence at 65–69 with a
   4-year duration is **0.000685 (남)** and **0.000635 (여)** [derived in §7.5], against the
   disclosed **0.000530 / 0.000459 at age 60**. The disclosed rates would have to grow by 29%
   (남) or 38% (여) over roughly seven years of age to meet the derived figures — about 3.7%
   and 4.7% a year, far below the 11–20% a year the same table shows at younger ages. The gap
   is the **selection effect plus the progression effect** of §7.5: the certified 1·2등급 stock
   at 65–69 includes lives who entered the scheme at a lower grade years earlier, whom an
   underwritten first-entry rate does not cover. The reconciliation is qualitative and the
   quantitative split between selection and progression is **not established by any retrieved
   source**; it is `[std]` in the model.
6. **The 입원간병인사용률 is not a probability.** At 0.494541 to 2.303485 it is plainly a
   *frequency* (expected days, or expected claims per life-year), and the parenthetical 「1일
   이상 180일 한도 … 1일당 간병인 8시간 이상 사용」 confirms it is a days-based unit. It is
   recorded here for completeness and is not used: `LTC_KR_S` does not model the hospital carer
   benefit.

**계약자배당**: 「무배당 우체국간병비보험 2309는 무배당상품으로서 배당을 하지 않습니다」 [S1].
Every product in the file is 무배당 (the 무 prefix in each product name).

---
### 17. Market size, penetration and product counts

**17.1 The life-insurance 간병보험 series** [R9, from 생명보험협회 「보험통계」 via KOSIS]:

| | 2008 | 2013 | 2018 |
|---|---|---|---|
| 보유계약 건수 (천 건) | 143 | 125 | **264** |
| 보유계약 금액 (십억 원) | 2,443 | 1,588 | **4,539** |
| 신계약 건수 (천 건) | 9 | 19 | **42** |
| 신계약 금액 (십억 원) | 252 | 218 | **659** |

The in-force count **fell 12.6%** between 2008 and 2013 and then **grew 111.2%** to 2018; the
amount fell 35.0% and then grew 185.8% [R9]. The 2008–2013 contraction is the private product
being displaced by the arrival of the public scheme; the 2013–2018 expansion is the market
rediscovering it as a supplement.

**17.2 Product counts at 2019-05** [R9, from the 생명보험협회 and 손해보험협회 공시실] — **99
products** on sale, 46 life and 53 non-life:

| 생보 | 개수 | 손보 | 개수 |
|---|---|---|---|
| 신한생명 | 12 | 현대해상 | 14 |
| 흥국생명 | 7 | 메리츠화재 | 8 |
| 라이나생명 | 6 | 한화손보 | 5 |
| 하나생명 | 6 | 흥국화재 | 5 |
| DB생명 | 4 | KB손보 | 5 |
| 오렌지라이프 | 4 | DB손보 | 4 |
| KDB생명 | 4 | 농협손보 | 3 |
| KB생명 | 2 | 롯데손보 | 1 |
| DGB생명 | 2 | 더케이손보 | 1 |
| 동양생명 | 2 | | |
| 교보생명 (특약 형태) | 2 | | |
| 삼성생명 | 1 | | |
| 메트라이프 | 1 | | |

Notes from the source: life-carrier 간병보험 is classified as 질병보험 within 보장성보험
(except two 라이나 products classified 기타); 교보생명 sells it only as a 특약; non-life
간병보험 is a 장기보장성보험 [R9]. **The transcription of 「라이나」 above is as printed in the
retrieved table; the row label extracted ambiguously and the carrier name should be checked
before it is reused.**

**17.3 Household penetration** [R9, from a 보험연구원 2018 consumer survey]:

| | 전체 | 20대 | 30대 | 40대 | 50대 | 60세 이상 |
|---|---|---|---|---|---|---|
| 간병보험 가입률 (%) | **2.5** | 0.5 | 1.4 | 1.2 | 3.4 | **4.8** |
| 가입 의향 (%) | 10.0 | 3.5 | 5.1 | 7.0 | 15.0 | 16.0 |
| 상품만족도 (5점) | 3.81 | 2.5 | 4.0 | 4.0 | 3.63 | 4.0 |

2.5% is a *very* low penetration by Korean standards — 실손의료보험 is held by about two thirds
of the population [see `_research/indemnity-medical.md`] and 암보험 by a large majority. Stated
intention to buy runs at four times the take-up, and among people the same study identified as
actually needing long-term care it reaches **67.5%** [R9]. Trade-press figures for 2023 put
간병보험 at **3.85% of non-life new business** (3.95 million policies of 102.5 million) and
**2.8% of life new business** (2.288 million of 82.7 million), up 2.5 and 1.7 percentage points
respectively since 2020 [R16, news]; and a 생명보험협회 2022 survey found **40.8%** naming
간병보험 as the cover they would buy next [R16, news].

**17.4 The 2024 surge.** 치매·간병보험 **초회보험료 ₩88,366,060,000 (883억 6,606만 원) for
January–November 2024, +70.2% year on year**; 계속보험료 2조 835억 원 (2023) → 2조 8,318억 원
(2024) [R17, news]. Set that against the 2018 치매보험 초회보험료 of 약 233억 원 [R8] and the
market has grown roughly four-fold in six years on the initial-premium measure — though the two
figures are not on the same definition (one is 치매보험, the other 치매·간병보험) and should
not be treated as a series.

**17.5 The 간병인사용일당 problem, 2024–2025.** Recorded because it dominates Korean commentary
on "간병보험" and because it is **not** the product modelled here. Loss ratios on the daily
carer indemnity reached about **100% in the life sector at August 2024**, up 5.3× from 18.7%
two years earlier, and **83.1% in the non-life sector**, up 1.7× from 48.1%, with some carriers
above 300%; premium at the five largest non-life carriers grew from ₩101.7bn (2021) to ₩2.08tn
(2025), about twenty-fold [R15, news]. A November 2024 약관 amendment tightened the definition
of a 간병인 and the documentary requirements (간병계약서, 간병일지, 간호기록) without
measurably moving the loss ratio, and the 금융감독원 commissioned the 보험연구원 in May 2025 to
study a structural overhaul [R15, news]. The structural diagnosis offered is that the market
sells a **cash 사용일당** rather than a service-provision (지원) form, so the insurer has no
control over utilisation [R15].

The grade-triggered 진단급여금 modelled by `LTC_KR_S` has none of this exposure — its trigger
is a public administrative decision that the insurer neither pays for nor influences, and it is
once-only. That is worth stating explicitly in `product-spec.md`, because a reader who knows
the Korean market only through 2024–2025 press coverage will assume otherwise.

### 18. Tax, and the regulatory frame

- **보장성보험료 세액공제.** 「근로소득자는 연말정산시 납입한 보험료(**연간 100만 원 한도**)에
  대하여 **12% 세액공제**를 받을 수 있습니다」 [S1]. This is a **credit, not a deduction** —
  the distinguishing feature of the Korean personal tax treatment noted throughout krlib — and
  it caps at ₩120,000 of tax relief a year on a ₩1,000,000 premium. 우체국 also offers a
  **장애인전용보험전환특약** converting the contract to the 장애인전용 보장성보험 basket where
  the insured or beneficiary is a 소득세법 장애인 [S1], and ABL carries the same rider [S2].
- **제3보험 classification.** 간병보험 is one of the three 제3보험 종목 in 보험업법
  제4조제1항제3호 [R12], so both life and non-life carriers write it, and the reserving,
  solvency and disclosure treatment follows the 제3보험 rules rather than the life or non-life
  ones. The cross-product regulatory material — 표준해약공제액, 표준책임준비금, K-ICS,
  해약환급금준비금 — belongs in `_research/regulatory-actuarial.md` and is not reproduced here.
- **IFRS 17 lapse assumption on 무·저해지.** [R14], secondary — the log-linear model converging
  to 0% at 납입완료, effective from the 2024 year-end close. See §15.
- **Basis-change risk.** No Korean 간병보험 document retrieved gives the insurer a 기초율변경권
  on the LTC benefit. What it gives instead is the **statutory-change rewriting clause**
  (「법령의 개정에 따라 장기요양상태 판정기준이 폐지되거나 보험금 지급사유에 해당하는 장기요양
  등급 판정이 불가능한 경우 및 기타 금융위원회의 명령이 있는 경우에는 회사는 객관적이고
  합리적인 범위 내에서 기존 계약내용에 상응하는 새로운 보장내용으로 이 계약의 내용을
  변경합니다」 [S3]) and the definitional fallback naming a successor body [S4]. Both are
  **contract-continuity** provisions, not repricing provisions: they let the insurer keep the
  contract alive if the state abolishes the grades, but they do not let it raise the premium if
  the state loosens them. **That asymmetry is the central risk of the Korean product** and it
  has no counterpart in `jplib`, `frlib` or `uklib`, whose LTC triggers are contractual. Its
  realisation in 2018 — the creation of 인지지원등급 out of nothing [R6] — enlarged the covered
  population of every 「1~인지지원등급」 rider overnight, at no additional premium.

---

## Variation across carriers

| Feature | 우체국 [S1] | ABL생명 [S2] | 삼성화재 [S3] | 한화손보 [S4] | 교보생명 [S5] |
|---|---|---|---|---|---|
| Sector | 우정사업본부 (outside 보험업법) | 생보 | 손보 | 손보 | 생보 |
| Document type | 상품요약서 (기초서류 extract) | 보험안내자료 | **약관** | **약관** | press release |
| Vintage | 2023 (2309) | 2025-09 (2504) | 2018-08 (1808.2) | 2023-07 | 2026-02 |
| Main-contract benefit | 재해사망보험금 | **장기요양(1~2등급)급여금** | 상해사망 + **장기요양지원금(1~2등급)** | 장기요양진단비 (plan-dependent) | 치매 진단자금 + 장기요양 |
| Grade thresholds offered | 1~2, 1~5 | 1~2, 1~5, **1~인지지원** | **1, 1~2, 1~3, 1~4** | **1, 1~2, 1~3, 1~4, 1~5** | 1~5, 인지지원 |
| Income form | **10-year monthly annuity**, survival-tested, 12-month guarantee, 120-month cap | **utilisation-tested monthly 지원금**, ₩100,000/month, some 종신 | **5년 월지급형 생활자금**, 가입금액 per month | not in retrieved extract | **lifetime monthly**, 36-payment guarantee |
| Annuity amount by grade | **yes** — 1등급 ₩500,000 / 2등급 ₩300,000 per month | no (flat ₩100,000) | no | n/a | not stated |
| Dementia cover | none | **CDR 1 / 2 / 3 이상** diagnosis riders + 통원 riders | none in retrieved extract | **CDR 1 / 2 / 3 이상 (90일 이상)** + 파킨슨병 | 경도 / 중등도 / 중증 |
| 장기요양 보장개시일 | **180일** (재해 carve-back) | **90일** (재해 carve-back) | **none stated** | **none stated** | not stated |
| 장기요양 감액기간 | **2년, 50%** | none stated | none stated | **1년, 50%** (질병 only) | not stated |
| 치매 보장개시일 | n/a | **1년** | n/a | **1년** (full exclusion) | not stated |
| Repeat/persistency benefit | no | no | **두 번째 장기요양지원금(1~2등급)**, 5-year 면책 from first award | no | no |
| Surrender-value form | **표준형** (normal CV from year 1) | **해약환급금 미지급형** — nil in period, **50% of 기본형** after | 순수보장성, **만기환급금 없음** | **납입중50%해약환급금지급형** — 50% in period, 100% after | not stated |
| 갱신형 | LTC riders 비갱신; 간병인 riders 5/10년 갱신 | LTC/치매 비갱신; 노인성질환 riders 10년 갱신 | not stated | not stated | not stated |
| 가입나이 | 만15~70 (1종) / 30~70 (2종) | 25~75 (일반) / 30~75 (간편) | 만15~60 | not in retrieved extract | 30~75 |
| 보험기간 | 85 / 90 / 100세만기 | 90 / 95 / 100세만기 | 90 / 100세만기 | not in retrieved extract | 종신 |
| Simplified underwriting | **yes**, 2종(간편가입), 3 questions | **yes**, 간편심사형, 4 questions incl. current 장기요양 status | not stated | 유병자 plans referenced | not stated |
| Published rates | 예정이율 **2.0%**, 예정위험률 incl. **요양 1·2등급 발생률** | full월납 rate card, 25 covers × 3 ages × 2 sexes | none | none | none |
| 납입면제 | on the annuity trigger (that rider only) | 장해지급률 50% 이상 | **1·2등급 award waives 기본계약 and all riders** | not in retrieved extract | premium refund at 1~4등급 |

**What does not vary.** Every product in the file defines its long-term-care trigger **solely**
by reference to a 장기요양등급 awarded by the 등급판정위원회 under 노인장기요양보험법 [S1] [S2]
[S3] [S4] [S5]; no product carries a company-basis ADL alternative; every 진단급여금 is **최초
1회에 한함** and extinguishes the rider that pays it [S1] [S2] [S3] [S4]; every product is
**무배당** [S1] [S2] [S3] [S4]; every one names 「허위 또는 부당 판정」 as a ground for refusal
[S1] [S2]; every one contemplates a 지정대리청구인 because the claimant cannot claim [S1] [S3];
and every dementia benefit uses the **CDR 척도** with a **90-day persistence** test and a
**one-year** waiting period [S2] [S4].

**Most representative design for a reference implementation.** A monthly-grid, level-premium,
non-renewable, 무배당 protection contract issued at ages 30–70 to age 90, sold in a
무해지환급금 form (nil surrender value during the premium-paying period, a fraction of the
notional 기본형 value afterwards), paying:

1. a **장기요양 진단급여금** once on first award of **장기요양 1등급 or 2등급**, subject to a
   **90-day 보장개시일** with a 재해 carve-back and a **first-year 50% 감액**;
2. an optional **간병연금** on the 우체국 shape — monthly, tested annually on survival, first
   12 months guaranteed, capped at 120 months, the monthly amount set by the grade at first
   certification (1등급 at the full rate, 2등급 at 60% of it) and never re-rated;
3. an optional **치매 진단급여금** tiered on the CDR scale (CDR 1 이상 / 2 이상 / 3 이상, once
   only across the tier set), subject to a **one-year 보장개시일** and a **90-day persistence**
   requirement inside the definition;
4. a **premium waiver** on award of 1등급 or 2등급, which fires simultaneously with the
   진단급여금 and is therefore not an independent decrement.

Every one of those choices is observed in at least two retrieved documents except the 90-day
보장개시일 with a first-year 50% 감액, which is a *combination* of ABL's waiting period [S2]
and 한화's reduction [S4]; `product-spec.md` justifies that combination against the observed
range in §11 and marks it `[std]`.

---

## Fetch failures and gaps

**Scale of the session.** Roughly **45 distinct URLs** were attempted; about **28** returned
usable text. The successes are the five product documents [S1] – [S5], the five statutory or
official-statistical sources [R1] – [R4] and [R7], the three research documents [R6], [R8],
[R9], [R11], and the trade-press set [R15] – [R18]. The failures are below, each with what was
lost.

**URLs tried and not opened, or opened and unusable:**

- `https://www.nhis.or.kr/nhis/together/wbhaec07200m01.do?mode=download&articleNo=11003958&attachNo=361507`
  — the **2024 노인장기요양보험 통계연보 PDF itself**. The fetcher refused it:
  `maxContentLength size of 10485760 exceeded`. **Recovered in full** through the
  `attachNo=368127`
  ZIP of `.xlsx` workbooks; nothing was lost, but the page-numbered PDF citation form (e.g.
  "통계연보 p. 92") is unavailable and every citation in this file is by **table number**
  instead.
- `...&attachNo=364866` (2024 노인장기요양보험 통계연보 **해설서**) — downloaded (166 kB) but
  it is an **HWP 5.0 compound document**, not a ZIP, and was not decoded. **What was lost**:
  the yearbook's own definitions of 인정자, 판정, 수급자 and 급여이용수급자, and its notes on
  discontinuities in the series. Every definitional statement about the yearbook's conventions
  in §6 is therefore **inference from the tables' own totals** — sound, because the totals
  reconcile, but not quoted from the compiler.
- `https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1YL20631` — **302 redirect to an
  SSO endpoint** (`sso.kosis.kr/ksso/sso/pmi-sso2.jsp`). KOSIS was not usable this session.
  **What was lost**: nothing, since [R4] supplies the same data at source.
- `https://www.nid.or.kr/info/today_list_2023.aspx` and
  `https://ansim.nid.or.kr/community/pds_view.aspx?BID=317` — **both blocked by a web
  application firewall** ("blocked request", client IP recorded). **What was lost**: the
  **중앙치매센터 「대한민국 치매현황」 report itself**, in every vintage. Every dementia
  prevalence figure in §8.1 therefore comes either from the 보건복지부 press release [R7] or,
  for the 2022-vintage 치매상병자 numbers, from a **carrier's brochure quoting the report**
  [S2]. The report's own age × sex × severity cross-tabulation, its regional detail and its
  MCI-to-dementia conversion rates are **absent from this file**.
- `https://www.mohw.go.kr/attachPreview.es?bid=0027&list_no=1484959&seq=1` — the 별첨
  「2023년 치매역학조사 및 실태조사 주요 결과」 viewer returned chrome only, no body.
  **What was lost**: the survey's sample size, its diagnostic instruments (whether CDR, CDR-SB,
  MMSE-KC or CERAD-K was used for case ascertainment), its 치매 유형별 (알츠하이머 / 혈관성 /
  기타) split and its MCI prevalence by age band. **The 2023 survey's diagnostic instrument is
  therefore `[unverified]`**, which matters because the private product's trigger is the CDR
  and a prevalence measured on a different instrument is not directly transferable.
- `http://mhdata.or.kr/mailing/Numbers248_240716_B1_Part.pdf` — downloaded (792 kB, 2 pp.) but
  the text layer uses an undecodable embedded font and `pypdf` returns mojibake. Not used.
- `https://www.korea.kr/briefing/pressReleaseView.do?newsId=156323907` — the 정책브리핑 page for
  the **금융감독원 보도참고자료 of 2019-03-28** rendered, but the body is delivered only in the
  attached `.pdf` and `.hwp`, whose links were not resolvable from the returned HTML.
  **What was lost**: the first of the two 2019 supervisory interventions in its own words.
  §12's
  account of it rests on [R8], a 보험연구원 summary, and on its footnote 9 citing the release.
- `https://www.fsc.go.kr/po010103/77174?...` — fetched, but it is a different document
  (실손보험 지급금 변동 연구, 2021-12-31). The FSS original of [R10] was **not located**; the
  KDI 경제교육·정보센터 mirror was used instead. **What this means**: the 2019-07-02 약관
  개선 content in §12 and §8.4 is quoted from a **government-portal mirror of the release**,
  not
  from the 금융감독원 site.
- `https://www.fsc.go.kr/no010101/83351` ([R14], the IFRS17 계리가정 가이드라인 of 2024-11-07) —
  **not attempted directly**; only search-surfaced press accounts were read. **What was lost**:
  the guideline text. The log-linear lapse model described in §15 and §18 is therefore
  **secondary** and is marked so at both places. The same guideline is cited from a retrieved
  source as `[R3]` in `_research/ci-insurance.md`, and that citation should be preferred.
- `https://www.law.go.kr/LSW/lsInfoP.do?lsId=010436&ancYnChk=0` — returned the site chrome and
  the currency line only, exactly as the house brief warns. **Worked around** with the
  per-article print form `lsBdyPrint.do`, which returned 제2조, 제15조 and 제23조 in full — but
  only at the **efYd=20180914 / lsiSeq=202643** consolidation. **What was lost**: 제12조,
  제13조,
  제16조, 제17조, 제19조, 제20조, 제29조 and 제40조 in their current form, and *any* article in
  the current 법률 제21690호 (시행 2026-05-26). The 30-day determination deadline in §2 is
  taken
  from the 법제처 restatement [R3] rather than from 제16조 itself; the 유효기간 in §5 is from a
  vendor notice [R13] rather than from 시행령 제8조; and the 본인부담률 in §2 is from a
  **2012-vintage wiki mirror** and is `[unverified]`.
- `http://www.yeslaw.com/lims/front/page/fulltext.html?pAct=view&pPromulgationNo=186245` —
  fetched and rendered, but the returned "article text" is **demonstrably wrong**: it described
  노인장기요양보험법 제15조 as 「요양보험료의 납부」 and 제23조 as a six-way benefit
  classification, neither of which matches the text retrieved from 국가법령정보센터.
  **No fact in this file is sourced to yeslaw**, and the entry is recorded so that a later pass
  does not trust it.
- `https://casenote.kr/법령/보험업법/제4조` — **HTTP 503**. **What was lost**: a clean mirror of
  보험업법 제4조. [R12] returned the article's structure and 제1항제3호 but not the full 목
  lettering, so the statement in §1 that 간병보험 is a named 종목 rests on a partial retrieval
  plus the identical retrieval recorded in `_research/ci-insurance.md`.
- `https://www.lotteins.co.kr/upload/C/let_simple_easy355_vip_2210_2_yak.pdf` — **HTTP 503**.
  **What was lost**: 롯데손해보험 「무배당 let:simple 간편355 간병보험 (for VIP)(2210)」 약관,
  indexed as containing a 「장기요양자금(1,2등급) 특별약관」. That would have been a **fifth
  carrier and a second 간편심사 LTC product**; no 롯데 parameter appears anywhere in this file.
- `http://www.kbinsure.co.kr/images/pban_info/pdf/2026_01_01.pdf` — downloaded (1.6 MB) but it
  is a **scanned image PDF** (a single 1657×2346 DCTDecode JPEG per page) with no text layer.
  **What was lost**: KB손해보험's current 간병보험 disclosure, including the **CDR 검사지원비
  특약** that trade press names as a KB innovation [R17]. KB appears in this file only through
  [R9]'s product count and [R17]'s news summary.
- `http://www.insweek.co.kr/38201` → `http://www.insweek.co.kr/news/articleView.html?idxno=38201`
  — a **cross-host redirect** that was returned rather than followed and was not re-fetched.
  **What was lost**: the trade-press account of **삼성생명 통합유니버설LTC종신보험**, which
  [R9] names as 삼성생명's single 간병보험 product. **No 삼성생명 product parameter appears in
  this file**; the largest life carrier in Korea is represented only by its non-life affiliate
  [S3] and by secondary mentions [R9] [R16].
- `https://www.dementianews.co.kr/news/articleView.html?idxno=1641` — rendered, but the body
  that came back is a consumer-guidance piece and did not carry the sales-volume figures that
  the search snippet attributed to it. **The two figures「3개월간 80만 건」 and 「2019년
  10월까지
  33개사 누적 2,804,103건, 142개 상품」 in §12 are therefore `[unverified]`** and are flagged
  as
  such in the text; they are not used for any calibration.
- `https://easylaw.go.kr/CSP/CnpClsMain.laf?...&ccfNo=2&cciNo=3&cnpClsNo=1` (장기요양인정의
  유효기간) — the URL variant tried returned the site's top-level category index, not the
  content page. **What was lost**: an official restatement of 시행령 제8조. §5's 유효기간
  values rest on [R13], a vendor notice.
- `https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do?idx_cd=2766` — fetched, but it
  is 노인복지시설 현황, not the long-term-care indicator. The e-나라지표 page for 노인장기요양
  was not located.
- `https://journal.kci.go.kr/kasp/archive/articlePdf?artiId=ART002331210` [R11] — **retrieved
  successfully** after local extraction, but note that the fetcher itself could not read it and
  reported the file as unreadable binary; the paper is usable only because `pypdf` decoded it.
  The same is true of [R6], [R8], [R9] and every product PDF.

**Documents sought and not found at all:**

- **Any 약관 (full policy conditions) for a *life* carrier's 간병보험.** [S1] is a 상품요약서 —
  authoritative, being a 기초서류 extract, but a summary; [S2] is a 보험안내자료. The two full
  약관 retrieved [S3] [S4] are both **non-life**. So every statement in this file about a life
  carrier's grace period, reinstatement, contestability, 고지의무 or 무효/취소 machinery comes
  from a summary document, and the *articles* behind them were not read.
- **Any 사업방법서 or 보험료 및 해약환급금 산출방법서.** [S2] refers to both by name (the
  무해지 comparator is defined by reference to the 산출방법서, and the disclosure obligation to
  사업방법서 별첨 제1호) but neither is published. **No 예정사업비율, no 표준해약공제액
  application, and no 신계약비 상각 schedule appears anywhere in this file**, so every expense
  assumption in `LTC_KR_S` is `[std]`.
- **Any 경험생명표 or 참조위험률 for 장기요양.** 보험개발원 publishes neither a 장기요양
  incidence table nor a post-onset mortality table publicly, and no reference to one was found
  in any retrieved document. [S1]'s 예정위험률 is a single carrier's own basis and is the only
  disclosed rate in the file.
- **A post-certification (impaired-life) mortality table by grade.** [R11] gives a mean
  survival and a one-month and one-year mortality for a truncated decedent cohort, and a grade
  mix of decedents on the pre-2014 three-grade scale. It gives **no survival curve**, no split
  by grade at entry, and no age-specific rates. **The post-onset mortality basis in `LTC_KR_S`
  is entirely `[std]`**, shaped by [R11]'s means and by the population mortality of
  `_research/regulatory-actuarial.md`.
- **A recovery or grade-improvement rate.** 삼성화재's 두 번째 장기요양지원금 rider is drafted
  around re-grading downwards and back up again [S3], and 107,365 current certifications came
  from a 등급변경신청 [R4 표2-5], so the transition plainly happens in both directions — but no
  retrieved source gives a transition matrix. `[std]`.
- **A utilisation rate by grade, service type and duration.** Needed for ABL's 지원금 riders
  [S2]. [R4 표3-3] gives 급여이용 수급자 by service type (방문요양 675,070; 주야간보호 213,428;
  노인요양시설 261,051; 복지용구 600,141; 방문목욕 130,904; 방문간호 22,128; 단기보호 2,372;
  노인요양공동생활가정 18,965; 통합재가 2,347, out of 1,140,725 recipients with overlap) but
  not by grade × service × duration. This is why the utilisation-conditioned riders are
  described and not modelled (§10.4).
- **A Korean 간병보험 lapse table.** None found. `[std]`, constrained by [R14]'s log-linear
  shape for the 무해지 form.
- **삼성생명, 교보생명, 한화생명, 신한라이프, NH농협생명, 미래에셋생명, 현대해상, 메리츠화재
  and DB손해보험 product parameters.** None retrieved. The five carriers in [S1] – [S5] cover
  one state-run insurer, one mid-size life carrier, two non-life carriers and one press
  release; the largest life carriers are absent. §17.2 shows that 현대해상 (14 products) and
  신한생명 (12) had the largest shelves in 2019 and neither appears here.
- **The 2024 재가급여 월 한도액 and 급여비용 고시.** §6.5 uses the **2019** values from [R6]
  and says so; the current 보건복지부 고시 was not fetched. Any benefit-adequacy statement
  built on those figures is stale by six years.

**Claims left `[unverified]`, and why:**

- **The 본인일부부담금 rates** (재가 15%, 시설 20%) — from a 2012-vintage wiki mirror of 법
  제40조; the current rates were not confirmed. Used only for scale in §6.5.
- **The 장기요양인정 유효기간 values** in §5 — from a vendor notice [R13], not from 시행령
  제8조. Used only inside the §7.3 sensitivity, never as a load-bearing input.
- **The 2019 치매보험 policy counts** (「3개월간 80만 건」; 「2019년 10월 누적 2,804,103건,
  33개사, 142개 상품」) — search snippets whose source article did not carry them in the body
  retrieved. Not used for calibration.
- **The projected 장기요양보험 fund deficit** (from 2026, reaching 2조 3,000억 원 by 2032) —
  [R16], a trade-press figure with no published projection behind it in the retrieved text.
- **The 삼성화재 장기요양 생활자금's survival test** — the retrieved summary table says 「5년간
  매월 가입금액」 but does not say whether the stream is 확정 or 생존-conditional [S3]. The
  reference implementation assumes survival-conditional, following [S1], and marks it `[std]`.
- **교보생명's premium refund on 1~4등급 진단** [S5] — a press-release statement whose reserve
  mechanics are not described. It would be a material feature and it is not modelled.
- **The 2023 치매역학조사's diagnostic instrument** — see the `attachPreview.es` failure above.
- **The 라이나생명 row in §17.2's product-count table** — the carrier-name cell extracted
  ambiguously from [R9]'s table and should be re-checked before reuse.
- **Whether any Korean carrier still writes a 회사기준 (company-definition) LTC trigger.** [R9]
  describes the three archetypes as current in 2019 and says the 공적기준 predominates, but no
  retrieved 2018-or-later contract contains a company-basis limb. The statement in §1 that the
  hybrid form is no longer written is `[unverified]`; what is established is only that it was
  not observed.
- **The relative frequency of 상해 versus 질병 as the cause of certification.** Both [S3] and
  [S4] price them differently — [S4] pays the full amount for a 상해-caused claim inside the
  reduction period and half for a 질병-caused one — so the split matters commercially. No
  retrieved source gives it. §6 shows the *disease* composition of under-65 applications [R4
  표2-3] but nothing on accident causation at any age.

**Deliberate scope limits (not gaps):**

- **간병인사용일당 / 간호·간병통합서비스 daily indemnities** are described in §17.5 and appear
  in [S1], [S2] and [S4]'s rider sets, but `LTC_KR_S` does not model them. They are a
  hospital-days frequency-severity product with an acute Korean loss-ratio problem [R15] and
  they share nothing with the grade-triggered benefit except the word 간병.
- **치매 통원급여금 and the 노인성 질환 riders** (관절염수술, 인공관절치환, 대상포진, 통풍,
  중증무릎관절연골손상) [S2] are recorded in §13.1's rate card for completeness and are outside
  scope.
- **The LTC acceleration inside `CI_KR_S`** — a CI product whose 장기요양상태 trigger is
  장기요양 1등급 또는 2등급 with its own 90-day 보장개시일 — is documented in
  `_research/ci-insurance.md` §10 and is deliberately not duplicated here. The two products
  share a statutory trigger and nothing else: `CI_KR_S` pays one accelerated benefit on the
  first of several events, `LTC_KR_S` pays a standalone benefit on the grade alone.
- **표준해약공제액, 표준책임준비금, K-ICS, IFRS 17 CSM and 해약환급금준비금** belong to
  `_research/regulatory-actuarial.md` and are referenced here only where a specific LTC
  consequence follows.
- **경험생명표 construction** — the `mort_table.csv` shipped with `LTC_KR_S`, like every other
  mortality input in krlib, is a `[std]` construction anchored on published summary statistics
  and 통계청 완전생명표 data with a `provenance` column on every row, because the 제10회
  경험생명표 is not published in full. That decision is made once, in
  `_research/regulatory-actuarial.md`, and inherited here.
