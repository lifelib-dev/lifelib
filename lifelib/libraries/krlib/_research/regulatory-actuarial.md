# Regulatory and actuarial framework — research notes (Korea)

Research compiled 2026-09-03 for `krlib`, the Korea section of the reference-products
library. Purpose: the single provenance layer behind all ten Korean products —
`whole_life`, `term_life`, `ci_insurance`, `child`, `indemnity_medical`, `cancer`,
`long_term_care`, `pension_savings`, `variable_annuity` and `immediate_annuity`. Every
one of those products' `product-spec.md`, `technical-notes.md`, `model.md` and
`sources.md` rests on facts recorded here, and on
`references/regulatory-and-actuarial-references.md`, which is built from this file's
source list. **The source numbering below is frozen.** `S1` and `R1` mean the same
documents for the life of the library; product documents cite them through the
cross-product tag `[REG-R#]`, and renumbering would silently repoint every citation in
ten document sets.

Korea's insurance regulation is unusual among the markets in this repository in three
structural ways, and the file is organised so that a drafter meets all three early.
First, **both** of the two large accounting-and-solvency reforms of the decade have
been live since **2023-01-01**: K-IFRS 제1117호 (the Korean adoption of IFRS 17) and
**K-ICS** (신지급여력제도, the Korean Insurance Capital Standard). Japan's economic-value
solvency regime commences 2026 and the UK and EU regimes long predate IFRS 17; Korea
switched liability measurement and capital measurement in the same quarter. Second, on
top of those two Korea layers a **해약환급금준비금** (*haeyak-hwangeupgeum-junbigeum*,
surrender value reserve) inside retained earnings, whose whole purpose is to stop an
IFRS 17 balance sheet from distributing earnings that the surrender-value floor would
later demand — a mechanism with no counterpart in `uslib`, `uklib`, `jplib`, `frlib` or
`delib`. Third, **제3보험** (*je-sam boheom*, "third insurance") is a statutory licence
category, not a market label: 보험업법 제4조제1항제3호 names 상해보험, 질병보험 and
간병보험, and both life and non-life insurers write them. Four of `krlib`'s ten products
sit inside it.

A fourth Korea-specific fact governs the shape of every model in the library. The
industry mortality table, the **경험생명표** (*gyeongheom saengmyeongpyo*, Experience Life
Table) produced by 보험개발원 (Korea Insurance Development Institute, KIDI), is **not
published**. Only summary statistics are released — 평균수명 and 기대여명 — and the qx
table itself is available to member insurers, not to the public. There is therefore no
Korean analogue of Japan's 標準生命表 numeric table or Germany's DAV 2008 T. Every
`mort_table.csv` in `krlib` is consequently a **[std]** construction anchored on
published 국가데이터처 (formerly 통계청) 생명표 statistics and on the KIDI summary figures,
carrying a `provenance` column on every row. Section 25 records exactly what is and is
not public, and section 33 records what that forces on the models.

Citation discipline, as in the sister libraries: every fact below carries `[S#]` where
it was read from a retrieved primary legal or standard-form document, `[R#]` where it
came from a retrieved supervisory release, statistical publication or research paper,
and `[unverified]` where it rests on a search-result summary, on general knowledge, or
on a document that could not be opened. Numbers are given with their units and their
as-of date; Korean amounts are given in 만원 (10,000) and 억원 (100,000,000) as well as
in won, because that is how a Korean source states them.

A note on retrieval, because it determined what this file can say. `law.go.kr` (국가법령
정보센터) serves both statutes and 행정규칙 as a JavaScript shell; a plain fetch of
`https://www.law.go.kr/법령/<name>` returns navigation chrome only. The body is served
from two inner endpoints that **do** return full UTF-8 HTML —
`https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=<id>&efYd=<yyyymmdd>` for 법령 and
`https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=<id>` for 행정규칙 — and the 별표
(schedules), which are images inside those pages, are served as PDFs through
`admRulBylContentsInfoR.do?bylSeq=<id>` followed by `flDownload.do?flSeq=<pdfFlSeq>`.
That three-step route is how 별표 14 (표준해약공제액), 별표 15 (보험가입금액의 산정) and
별표 27 (공시기준이율 산출 기준) were obtained verbatim, and it is worth recording because
those three schedules carry the only published statement of Korea's surrender-charge
cap and crediting-rate formula. Where a formula in the body text of a regulation is
rendered as an image rather than as text, it is recorded here as not retrieved.

---

## Primary sources

### S1 — 보험업법, 법률 제20436호
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2025. 1. 31.] [법률 제20436호, 2024. 9. 20., 타법개정]**
- URL: https://www.law.go.kr/법령/보험업법
  (body retrieved from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131)
- Accessed: 2026-09-03
- Retrieved: yes (full statute, 127,346 characters of extracted text)
- What was read: the whole Act. Articles used below are 제2조 (정의), 제4조 (보험업의
  허가), 제5조 (허가신청서 등의 제출), 제108조 (특별계정), 제120조 (책임준비금 등의
  적립), 제123조 (재무건전성의 유지), 제124조 (공시 등), 제127조 (기초서류의 작성 및
  제출), 제128조 (기초서류에 대한 확인), 제128조의2 (기초서류 관리기준), 제128조의3
  (기초서류 작성ㆍ변경 원칙), 제176조 (보험요율 산출기관), 제181조 (보험계리) and
  제184조 (선임계리사의 의무 등). This is the statute that defines the product taxonomy
  the whole library sits in, and the document set (기초서류) a Korean product filing
  consists of.

### S2 — 보험업법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 4. 21.]** (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/법령/보험업법 시행령
  (body from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421)
- Accessed: 2026-09-03
- Retrieved: yes (153,076 characters)
- What was read: 제1조의2 (보험상품 — the closed lists of 생명보험계약, 손해보험계약 and
  제3보험계약, and the six public schemes excluded from "보험상품"), 제63조 (책임준비금
  등의 계상 — the IFRS 17 vocabulary in delegated form), 제65조 (재무건전성 기준 — the
  100% 지급여력비율 floor), 제71조 (기초서류의 작성 및 변경 — the 30-day pre-filing).

### S3 — 보험업감독규정, 금융위원회고시 제2026-16호
- Publisher: 금융위원회 (보험과), served by 국가법령정보센터 as a 행정규칙
- Version: **[시행 2026. 5. 6.] [금융위원회고시 제2026-16호, 2026. 5. 6., 일부개정]**
- URL: https://www.law.go.kr/행정규칙/보험업감독규정
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112)
- Accessed: 2026-09-03
- Retrieved: yes (226,083 characters of extracted text; formulas that the page renders
  as images did **not** extract — see the fetch-failure section)
- What was read: the whole 고시. Articles used are 제1-2조 (정의 — 기준연령 요건,
  보장성보험, 저축성보험, 금리연동형보험, 평균공시이율, 최적기초율, 참조순보험료,
  요구자본, 충격시나리오방식), 제4-32조 (수수료등 지급기준), 제5-6조 (특별계정의
  설정ㆍ운용), 제5-7조 (특별계정 관련 자금이체), 제6-11조 (책임준비금의 적립),
  제6-11조의4 (적정성 검증), 제6-11조의5 (보증준비금), 제6-11조의6 (해약환급금준비금),
  제6-11조의7 and 제6-13조 (계약자배당), 제6-26조 (특별계정 계약자적립금),
  제7-1조 (지급여력금액), 제7-2조 (지급여력기준금액), 제7-2조의2 (건전성감독기준
  재무상태표), 제7-17조–제7-19조 (적기시정조치), 제7-51조 (신고기준), 제7-60조
  (생명보험의 보험상품설계), 제7-63조 (제3보험의 보험상품설계, including the whole
  실손의료보험 rule set as amended 2026-05-06), 제7-64조 (산출방법서 필수기재사항),
  제7-65조 (계약자적립액의 계산 and the 공시이율 machinery), 제7-66조 (생명보험
  해약환급금의 계산), 제7-67조–제7-70조, and the 부칙 of 금융위원회고시 제2022-53호
  (the K-ICS and 해약환급금준비금 commencement provisions).
- Comparison version also retrieved: **[시행 2023. 3. 2.] [금융위원회고시 제2023-10호]**
  (admRulSeq 2100000220196), used to date the 2023–2026 amendments. Notable drift: the
  filing document is renamed from "보험료 및 **책임준비금** 산출방법서" to "보험료 및
  **해약환급금** 산출방법서" in 제7-69조 and 제7-70조 by the current text.

### S4 — 보험업감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액 (제7-66조 관련)
- Publisher: 금융위원회, schedule to S3
- Version marker on the schedule: **<개정 2011.1.24, 2015.5.7., 2020.1.15.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240711
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927491)
- Accessed: 2026-09-03
- Retrieved: yes (1-page PDF, text extracted cleanly and in full)
- What was read: the complete statement of Korea's **표준해약공제액** — the statutory cap
  on the surrender charge — with all seven notes, including the 연금저축보험 and
  실손의료보험 special cases. This is the single most model-relevant page of Korean
  regulation in the whole file; it is reproduced verbatim in §16.

### S5 — 보험업감독규정 [별표 15] 보험가입금액의 산정 (제7-67조 관련)
- Publisher: 금융위원회, schedule to S3
- Version marker: **<개정 2011.1.24., 2020.1.15.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240715
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927503)
- Accessed: 2026-09-03
- Retrieved: yes (1-page PDF, full text)
- What was read: how 보험가입금액 (the "sum insured" that enters the 표준해약공제액
  formula) is computed for products that are not plain death cover — the 위험보험료 ratio
  method of 제9호, and the exclusion of nursing-care benefit risk premium from it.

### S6 — 보험업감독업무시행세칙, 금융감독원세칙
- Publisher: 금융감독원 (보험감독국), served by 국가법령정보센터 as a 행정규칙
- Version: **[시행 2026. 9. 10.] [금융감독원세칙, 2026. 8. 28., 일부개정]**
- URL: https://www.law.go.kr/행정규칙/보험업감독업무시행세칙
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2200000108939)
- Accessed: 2026-09-03
- Retrieved: yes (114,610 characters)
- Caveat worth recording: the version law.go.kr serves as current takes effect
  **2026-09-10**, one week after the access date. Facts taken from it are facts about
  the imminent text, not about the text in force on 2026-09-03; where that matters it
  is said at the point of use.
- What was read: 제1-1조, 제1-2조, 제5-13조 (표준사업방법서 및 표준약관 → 별표 14 and
  별표 15 of the 세칙), 제5-16조 (the 공시기준이율 delegation and the four external index
  rates), 제5-17조의2, and the 부칙 dating the 계리적 가정 amendments.

### S7 — 보험업감독업무시행세칙 [별표 27] 공시기준이율 산출 기준 (제5-16조 관련)
- Publisher: 금융감독원, schedule to S6
- Version marker: **<신설 2012.9.26, 개정 2013.12.17., 2018.11.6., 2022.12.23.,
  2025.10.28.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295679
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885941)
- Accessed: 2026-09-03
- Retrieved: yes (3-page PDF, full text; two weight formulas render as images and did
  not extract, noted at the point of use)
- What was read: the complete 공시기준이율 formula — the α-weighted blend of an objective
  external index rate and the insurer's own 운용자산이익률, the four index instruments,
  the three-month weighted moving average, the 0.5 percentage-point rounding of the
  weights, and the 60% cap on α.

### S8 — 보험업감독업무시행세칙 [별표 15] 표준약관 (제5-13조제1항 관련)
- Publisher: 금융감독원, schedule to S6
- Version markers: 생명보험 표준약관 **<개정 … 2024.12.20., 2025.3.31., 2025.6.30.>**;
  실손의료보험 표준약관 amended **2026.5.6.**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295613
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885301)
- Accessed: 2026-09-03
- Retrieved: yes (**492-page PDF**, 441,610 characters extracted; the 장해분류표 and
  재해분류표 appendix tables extracted as running text, some tabular layout lost)
- What was read: the 표준약관 table of contents and then, in full, **Ⅰ. 생명보험**
  (제1조–제43조 plus 부표) and, of **Ⅱ. 손해보험**, the 실손의료보험 family: 기본형
  실손의료보험(급여), 실손의료보험 특별약관1(중증 비급여) and 실손의료보험 특별약관2
  (비중증 비급여). This is the definitive statement of the contract mechanics every
  Korean policy must contain — 보험나이, 청약철회, the three-month 품질보증해지, 계약 전
  알릴 의무 and its time bars, 납입최고 and 부활, 해약환급금, 보험계약대출 — and of the
  **fifth-generation 실손** design that took effect 2026-05-06.

### S9 — 상법 (제4편 보험), 법률 제20991호
- Publisher: 국가법령정보센터 (법제처) — 법무부 소관
- Version: **[시행 2026. 7. 23.] [법률 제20991호, 2025. 7. 22., 일부개정]**
- URL: https://www.law.go.kr/법령/상법
  (body from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=…&efYd=20260723)
- Accessed: 2026-09-03
- Retrieved: yes (631,670 characters; 제4편 보험 read in full)
- What was read: 제638조 through 제739조의3 — the general part (제638조–제664조), 인보험
  (제727조–제729조), 생명보험 (제730조–제736조), 상해보험 (제737조–제739조) and 질병보험
  (제739조의2–제739조의3). This is the *contract* law; 보험업법 is the *supervisory* law,
  and Korean practice keeps them strictly apart.

### S10 — 소득세법, 법률
- Publisher: 국가법령정보센터 (법제처) — 기획재정부 소관
- Version: **[시행 2026. 7. 1.]** (lsiSeq 280405, efYd 20260701)
- URL: https://www.law.go.kr/법령/소득세법
- Accessed: 2026-09-03
- Retrieved: yes (356,757 characters)
- What was read: 제16조 (이자소득 — 제1항제9호 저축성보험의 보험차익 and its two
  exclusions), 제20조의3 (연금소득), 제59조의3 (연금계좌세액공제), 제59조의4
  (특별세액공제 — 보장성보험료), 제129조 (원천징수세율). The 연금소득 withholding-rate
  age table in 제129조제1항제5의2호가목 is rendered as an image and did **not** extract.

### S11 — 소득세법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 7. 1.]** (lsiSeq 286211, efYd 20260701)
- URL: https://www.law.go.kr/법령/소득세법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (624,319 characters)
- What was read: 제25조 (저축성보험의 보험차익 — the complete 10-year, ₩100,000,000,
  월적립식 and 종신형 연금보험 exemption conditions) and 제40조의2 (연금계좌 등 — the
  ₩18,000,000 annual contribution ceiling, the 55-and-five-years 연금수령 test and the
  연금수령한도 machinery).

### S12 — 상속세 및 증여세법, 법률
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 1. 2.]** (lsiSeq 276123, efYd 20260102)
- URL: https://www.law.go.kr/법령/상속세 및 증여세법
- Accessed: 2026-09-03
- Retrieved: yes (148,788 characters)
- What was read: 제8조 (상속재산으로 보는 보험금) and 제34조 (보험금의 증여).

### S13 — 금융소비자 보호에 관한 법률, 법률
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2026. 1. 2.]** (lsiSeq 277247, efYd 20260102)
- URL: https://www.law.go.kr/법령/금융소비자 보호에 관한 법률
- Accessed: 2026-09-03
- Retrieved: yes (62,444 characters)
- What was read: 제46조 (청약의 철회) in full — the statutory cooling-off right that the
  표준약관 implements.

### S14 — 예금자보호법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2025. 9. 1.]** (lsiSeq 273001, efYd 20250901)
- URL: https://www.law.go.kr/법령/예금자보호법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (46,515 characters)
- What was read: 제18조 (보험금의 계산방법의 예외 등), in particular **제7항**, which sets
  the protection limit and its per-bucket application. This is the article that
  supersedes the ₩50,000,000 figure that Korean consumer material carried until 2025.

### S15 — 국민건강보험법, 법률
- Publisher: 국가법령정보센터 (법제처) — 보건복지부 소관
- Version: **[시행 2026. 1. 2.]** (lsiSeq 276651, efYd 20260102)
- URL: https://www.law.go.kr/법령/국민건강보험법
- Accessed: 2026-09-03
- Retrieved: yes (98,719 characters)
- What was read: 제41조 (요양급여 and the 급여/비급여 boundary), 제42조 (요양기관 — the
  institution classes the 실손 co-payment table keys off), 제44조 (비용의 일부부담 and
  the 본인부담상한제).

### S16 — 노인장기요양보험법, 법률 제21690호
- Publisher: 국가법령정보센터 (법제처) — 보건복지부 소관
- Version: **[시행 2026. 5. 26.] [법률 제21690호, 2026. 5. 26., 일부개정]**
- URL: https://www.law.go.kr/법령/노인장기요양보험법
- Accessed: 2026-09-03
- Retrieved: yes (133,932 characters)
- What was read: 제2조 (정의 — 노인등, 장기요양급여 and the six-month test), 제15조
  (등급판정 등), 제23조 (장기요양급여의 종류), 제39조 (급여비용의 산정), 제40조
  (본인부담금).

### S17 — 노인장기요양보험법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 5. 12.]** (lsiSeq 286011, efYd 20260512)
- URL: https://www.law.go.kr/법령/노인장기요양보험법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (42,367 characters)
- What was read: **제7조 (등급판정기준 등)** in full — the 장기요양인정점수 thresholds for
  등급 1 to 5 and 인지지원등급, which is the statutory definition of the trigger for
  `LTC_KR_S`.

### S18 — 보험업법 제4조 (보험업의 허가), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr), a third-party statute and case mirror
- URL: https://casenote.kr/법령/보험업법/제4조
- Accessed: 2026-09-03
- Retrieved: yes
- What was read: 제4조제1항 in its three-list form. Used only as a cross-check on S1;
  every fact is also present in S1, which is the authoritative retrieval. Recorded
  because it was the first route that returned article text when the law.go.kr friendly
  URL returned only a shell.

### S19 — 보험업법 제5조 (허가신청서 등의 제출), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr)
- URL: https://casenote.kr/법령/보험업법/제5조
- Accessed: 2026-09-03
- Retrieved: yes
- What was read: the four attachments to a licence application, including the
  three-document definition of 기초서류 — 사업방법서, 보험약관, 보험료 및 해약환급금의
  산출방법서. Cross-checked against S1.

### S20 — 보험업법 제2조 (정의), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr)
- URL: https://casenote.kr/법령/보험업법/제2조
- Accessed: 2026-09-03
- Retrieved: in part (the summariser returned the numbered definitions but compressed
  the 가/나/다 sub-items)
- What was read: 제1호 보험상품 and the 생명보험상품 / 손해보험상품 / 제3보험상품 split.
  Superseded in every particular by S1, which returned the article verbatim.

### S21 — 보험업법 (대한민국), 위키문헌
- Publisher: ko.wikisource.org
- URL: https://ko.wikisource.org/wiki/보험업법_(대한민국)
- Accessed: 2026-09-03
- Retrieved: yes, but the text is **법률 제8902호, 시행 2008. 6. 15.** — seventeen years
  out of date
- What was read: nothing is cited from it. It is listed because it was tried and
  because a future reader should know that this mirror is stale and must not be used.

### S22 — 보험업감독규정, 금융위원회고시 제2023-10호 (comparison version)
- Publisher: 금융위원회
- Version: **[시행 2023. 3. 2.]**
- URL: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000220196)
- Accessed: 2026-09-03
- Retrieved: yes (207,084 characters)
- What was read: the same articles as S3, to date amendments. Used only for
  before/after statements; all current-law facts are cited to S3.

---

## Regulatory and actuarial references

### R1 — 금융위원회·금융감독원, 제4차 보험개혁회의 보도자료 (계리가정·할인율)
- Publisher: 금융위원회 보험과 / 금융감독원 보험리스크관리국
- Date: 보도 2024-11-07, 배포 2024-11-06; the meeting was 2024-11-04
- URL: https://www.fsc.go.kr/no010101/83351
  (attachments at `…/comm/getFile?srvcId=BBSTY1&upperNo=83351&fileTy=ATTACH&fileNo=1`
  and the same with `fileNo=4`)
- Accessed: 2026-09-03
- Retrieved: yes (the 6-page 보도자료 PDF and the 6-page 별첨 「보험부채 할인율 현실화
  연착륙 방안」 PDF, both extracted in full; attachments 2, 3 and 5 are HWP/HWPX and were
  not converted)
- What it is good for: the **무·저해지 해지율** log-linear model and its 0.1% convergence
  point, the 0.8% post-완납 ultimate lapse rate, the ≥30% additional lapse at a
  단기납 종신보험 bonus date, the age-cohort loss-ratio requirement, the
  무·저해지 share-of-new-business series, and the whole IFRS 17 discount-curve
  architecture (LOT, LTFR 4.55%, liquidity premium 91bp) with its phase-in dates. This
  is the most important single supervisory document for `krlib`'s lapse assumptions.

### R2 — 금융감독원, 「2024년 실손의료보험 사업실적(잠정)」
- Publisher: 금융감독원 보험계리상품감독국 보험상품제도팀
- Date: 보도 2025-05-13, 배포 2025-05-12
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=266435
  (PDF via https://eiec.kdi.re.kr/policy/callDownload.do?num=266435&filenum=1)
- Accessed: 2026-09-03
- Retrieved: yes (7-page PDF, full text)
- What it is good for: the definitive quantitative picture of 실손의료보험 — contract
  counts by generation, premium income, 보험손익, 경과손해율 overall and by generation,
  premiums by generation for a 40-year-old male, the 급여/비급여 claims split, the
  claim concentration in 비급여 주사제 and 근골격계, claims by institution class, and
  average 비급여 claim per contract by generation. It also reproduces the
  co-payment-rate-by-generation table and the April 2025 reform design.

### R3 — 금융감독원, 「2025년 9월말 기준 보험회사 지급여력비율 현황」
- Publisher: 금융감독원
- Date: 2026-01-06
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=275691
- Accessed: 2026-09-03
- Retrieved: in part (the KDI summary page returned the headline ratios; the underlying
  PDF was not downloaded)
- What it is good for: K-ICS ratios after 경과조치 at 2025-09-30 — all insurers 210.8%,
  생보 201.4%, 손보 224.1%. Component amounts (지급여력금액, 지급여력기준금액) were not
  on the page.

### R4 — 금융위원회, 新회계·자본제도에 맞춘 보험업권 자본규제 고도화
- Publisher: 금융위원회 보험과
- Date: 2025-03-12
- URL: https://www.fsc.go.kr/no010101/84128
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the size of the capital-regime shift — 요구자본 ₩67.9조 under RBC
  at 2022-12-31 against ₩118.9조 under K-ICS at 2024-09-30; the 기본자본 K-ICS ratio
  series; 2024 capital-securities issuance; the 비상위험준비금 reform.

### R5 — 금융위원회, 무(저)해지환급금 보험 상품구조 개선 (감독규정 입법예고)
- Publisher: 금융위원회 보험과
- Date: 2020-07-27
- URL: https://www.fsc.go.kr/no010101/74468
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the origin and the arithmetic of the 무·저해지 환급률 cap that now
  sits in 보험업감독규정 제7-66조제4항제2호 — a worked 20-year 종신보험 comparison of
  97.3% (표준형) against 134.1% (무해지) and the rule that limits the latter to the
  former. Also the count of carriers writing the form in 2020.

### R6 — 금융위원회, 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」
- Publisher: 금융위원회
- Date: published 2025-09-01 (release dated 2025-08-29)
- URL: https://www.fsc.go.kr/no010101/85200
- Accessed: 2026-09-03
- Retrieved: in part (title, dates and the general statement; the release as summarised
  does not itemise the insurance-specific buckets)
- What it is good for: dating the increase of the deposit-protection limit to
  ₩100,000,000. The per-bucket mechanics come from S14, which is authoritative.

### R7 — 금융위원회, 실손의료보험 개혁방안 보도자료 (5세대 설계)
- Publisher: 금융위원회 보험과
- Date: 2025-04-01 (the FSS release R2 refers to the same package as "'25.4.2. 旣발표")
- URL: https://www.fsc.go.kr/no010101/84272
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the design of **5세대 실손** before it became regulation — the
  급여 co-payment formula, the 중증/비중증 비급여 split with their co-payments and
  limits, the ₩5,000,000 annual co-payment cap on 중증 비급여 inpatient care at tertiary
  and general hospitals, the illustrative premium reductions, the 계약재매입 offer to
  first- and early-second-generation policyholders, and the 2026-07 to 2036-06
  ten-year conversion window.

### R8 — 보험개발원 제10회 경험생명표 — as reported by 보험매일
- Publisher of the underlying table: 보험개발원 (Korea Insurance Development Institute)
- Publisher of the retrieved document: 보험매일 (fins.co.kr), a trade newspaper
- Date: article 2024-01-10 (reporting the KIDI release of early January 2024)
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03
- Retrieved: yes (article text)
- **This is a news article, and it is the only retrieved source for the 제10회
  경험생명표 summary figures.** KIDI's own press-release listing (R22) does not carry a
  경험생명표 item in the range served, and the KIDI 보험정보 빅데이터 플랫폼 page refused
  connection. Facts taken from it are so marked.
- What it is good for: 평균수명 남 86.3세 / 여 90.7세 (up 2.8 and 2.2 years on the 제9회),
  65세 기대여명 남 23.7년 / 여 27.1년 (up 2.3 and 1.9), application from 2024-04 to new
  business only, and the directional premium effect by product class.

### R9 — 국가데이터처, 「2024년 생명표 작성 결과」
- Publisher: 국가데이터처 인구동향과 (the renamed 통계청)
- Date: 2025-12-03
- URL: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156732935
- Accessed: 2026-09-03
- Retrieved: yes (briefing text)
- What it is good for: 기대수명 at birth 2024 — 전체 83.7년, 남 80.8년, 여 86.6년; 65세
  기대여명 남 19.5년 / 여 23.7년; 40세 기대여명 남 41.9년 / 여 47.4년; survival to age
  80 of 64.4% (male) and 82.2% (female); the OECD comparison. This is the **public**
  mortality series that a `[std]` `mort_table.csv` must be anchored on.

### R10 — 통계청, 「2023년 생명표」
- Publisher: 통계청 (as it then was)
- Date: 2024-12-04
- URL: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156664008
- Accessed: 2026-09-03
- Retrieved: yes (briefing text)
- What it is good for: the prior year of the same series — 기대수명 전체 83.5년, 남
  80.6년, 여 86.4년; 65세 기대여명 남 19.2년 / 여 23.6년; and the statement of what a
  Korean 생명표 is ("연령별 사망 수준이 그대로 유지될 경우 …"). Useful as the one-year
  check on R9's trend.

### R11 — 보건복지부·중앙암등록본부(국립암센터), 「2023년 국가암등록통계 참고자료」
- Publisher: 중앙암등록본부 / 국가암정보센터
- Date on the document: **2026-01-20**
- URL: https://www.cancer.go.kr/download.do?uuid=cfcd35c3-391f-4060-9688-641db3d86cbd.pdf
- Accessed: 2026-09-03
- Retrieved: yes (41-page PDF; extracted in full and read)
- What it is good for: everything `Cancer_KR_S` needs that is public — 암발생자수 by year
  and sex 1999–2023, 조발생률 and 연령표준화발생률, the top-ten cancers by sex with
  incidence rates, **평생 암발생/사망 위험도** by site and sex, 5-year relative survival
  by period and site, and 암유병자수 with 유병률. The thyroid-cancer share matters
  because Korean cancer policies pay 갑상선암 at the reduced 유사암 tier.

### R12 — 국민건강보험공단, 2024년도 건강보험환자 진료비 실태조사
- Publisher: 국민건강보험공단
- Date: 2025-12-30
- URL: https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf
  (the 보험연구원 weekly-trend reprint of the NHIS 보도자료)
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- What it is good for: the public-scheme underlay that 실손의료보험 sits on — 보장률
  64.9%, 법정 본인부담률 19.3%, 비급여 본인부담률 15.8%, the ₩138.6조 total treatment
  cost split into ₩90.0조 보험자부담금 / ₩26.8조 법정본인부담금 / ₩21.8조 비급여, the
  2012–2024 series, and 보장률 by institution class and by age band.

### R13 — 국민건강보험공단, 「장기요양 등급 판정 현황」 (자율공시 / 경영공시)
- Publisher: 국민건강보험공단
- As-of date on the retrieved table: **2026-06-30 (2026년 2/4분기)**
- URL: https://www.nhis.or.kr/announce/wbhaec11503m01.do
- Accessed: 2026-09-03
- Retrieved: yes (table)
- What it is good for: the grade distribution that `LTC_KR_S`'s incidence basis must
  reproduce in aggregate — 총 등급판정 1,411,466명, 인정자 1,275,370명 (90.4%), 등급외자
  136,096명, and the split 1등급 53,844 / 2등급 100,844 / 3등급 333,143 / 4등급 604,307 /
  5등급 151,681 / 인지지원등급 31,551.

### R14 — 보험연구원, 「K-ICS 경과조치 주요 내용과 시사점」 (KIRI 리포트 이슈 분석), 노건엽
- Publisher: 보험연구원 (Korea Insurance Research Institute)
- Date: 2022-03-07
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=139489
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- What it is good for: the complete inventory of K-ICS 경과조치 — which four items may be
  phased in over ten years, the eligibility tests, the 2024-to-2033 10%-a-year
  recognition of the 보험부채 증가분, the biennial and 50bp re-measurement triggers, the
  dividend-payout penalty, the five-year 적기시정조치 deferral, and a side-by-side
  comparison with Solvency II's transitionals.

### R15 — 보험연구원, 「2026년 보험산업 전망」 (2026년 보험산업 전망과 과제 세미나), 황인창
- Publisher: 보험연구원 금융시장분석실
- Date: 2025-10-21
- URL: http://www.kiri.or.kr/report/downloadFile.do?docId=778039
- Accessed: 2026-09-03
- Retrieved: yes (91-page presentation PDF, extracted in full)
- What it is good for: the market-size tables used in the Market overview section —
  생명보험 수입보험료 by line (보장성/저축성/변액/퇴직연금) for 2023, 2024, 2025(E) and
  2026(E) with growth rates, and the same for 손해보험 원수보험료 (장기손해보험, 개인연금,
  자동차, 일반, 퇴직연금).

### R16 — 한국보험신문, 「2025년 보험사 당기순이익 12.2조원… 생·손보 보험손익 동반 하락」
- Publisher: 한국보험신문 (insnews.co.kr); the figures are attributed in the article to
  금융감독원's 2025년 보험회사 경영실적
- Date: 2026-03-30
- URL: https://www.insnews.co.kr/news/articleView.html?idxno=89914
- Accessed: 2026-09-03
- Retrieved: yes (article text)
- **This is a news article standing in for an FSS release that could not be opened
  directly** (fss.or.kr refused a plain fetch). Facts from it are marked as
  news-sourced.
- What it is good for: 2025 outturn — 수입보험료 ₩266.6595조 (생보 ₩127.5061조, 손보
  ₩139.1533조), the 생보 line split, the 손보 line split, 당기순이익 ₩12.2172조, ROA
  0.94%, ROE 7.86%, 총자산 ₩1,344.2조.

### R17 — 하나생명, 「적용이율 공시 — 표준이율 및 평균공시이율」
- Publisher: 하나생명보험주식회사
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03
- Retrieved: yes (both tables)
- What it is good for: the **평균공시이율 time series** 2016–2026 as published by a
  carrier, and the 표준이율 series 2013–2015 that preceded it. 평균공시이율 is a
  regulatory input (S3 제1-2조제13호) and enters the tax-free-savings test, the 부활
  interest ceiling and the 저축성보험 design test, so its level matters to four of the
  ten products.

### R18 — 교보생명, 「공시기준이율 적용현황」
- Publisher: 교보생명보험주식회사
- URL: https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status
- Accessed: 2026-09-03
- Retrieved: in part (the rate grid returned; **the month selector's value did not
  return**, so the as-of date of the figures is unknown)
- What it is good for: a worked example of the 공시기준이율 / 적용률 / 적용이율 triple that
  S7 defines, at 3.19% across 보장(무배당), 연금(무배당), 연금(배당), 저축(무배당) and
  연금저축(배당). Because the as-of month is unknown, the level is treated as
  illustrative and is not used as a dated fact.

### R19 — 생명보험협회, 공시실 (pub.insure.or.kr)
- Publisher: 생명보험협회 (Korea Life Insurance Association, KLIA)
- URL: https://pub.insure.or.kr/
- Accessed: 2026-09-03
- Retrieved: yes (landing page and category description)
- What it is good for: establishing what Korean product disclosure contains and where —
  상품비교공시 across eleven protection classes plus savings, variable, retirement and
  실손; 경영공시; 기타공시 (민원, 불완전판매비율, 소송). The comparison tool is the public
  route to 약관, 상품요약서 and 해약환급금 illustrations, and is the reason `krlib`'s
  product research files can cite real Korean product parameters at all.

### R20 — 생명보험협회, FACT BOOK
- Publisher: 생명보험협회
- URL: https://www.klia.or.kr/consumer/stats/factbook/list.do
- Accessed: 2026-09-03
- Retrieved: in part (edition list and contents description; the 2025 edition PDF itself
  was not downloaded)
- What it is good for: editions run 2001–2025; the 2025 edition covers FY2024 with
  contract, financial, reserve, asset, distribution and **생명표** sections. Recorded as
  the standard annual reference; no number in this file is taken from it.

### R21 — 생명보험협회, 금융통계월보(생명보험편)
- Publisher: 생명보험협회, with 보험개발원 preparing tables 5–9
- URL: https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do
- Accessed: 2026-09-03
- Retrieved: in part (structure and provenance; the monthly tables are behind a query
  form and were not retrieved)
- What it is good for: knowing that the monthly life series is a 통계청 국가승인통계 built
  from insurers' 업무보고서, with 보유계약, 보장성/저축성 split, 지급유형별
  보험금·환급금·배당금, 경과기간별 보험료수익 and 부문별 손익 prepared by KIDI.

### R22 — 보험개발원, 보도자료 listing
- Publisher: 보험개발원
- URL: https://www.kidi.or.kr/user/nd11592.do
- Accessed: 2026-09-03
- Retrieved: yes (listing, items 742–746, dated 2026-06-02 to 2026-08-18)
- What it is good for: negative evidence. The visible listing carries **no** 경험생명표,
  참조순보험요율 or 보험통계 item, which is why the 제10회 경험생명표 figures in this file
  rest on R8, a newspaper.

### R23 — 한국회계기준원 회계기준위원회, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」
- Publisher: 한국회계기준원 (Korea Accounting Institute), mirrored by KDI 경제교육·정보센터
- Date of the resolution: **2018-05-25**
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=177159
- Accessed: 2026-09-03
- Retrieved: in part (the release body returned; the 별첨 HWP with the standard's
  substance was not converted)
- What it is good for: dating the Korean adoption of IFRS 17 as 기업회계기준서 제1117호
  「보험계약」. The release states an effective date of 2021-01-01, which was the
  pre-deferral date; the operative commencement of 2023-01-01 is established from S3's
  부칙 and from R4.

### R24 — 국민건강보험공단, 「2024 노인장기요양보험 통계연보」, as reported by 메디칼월드뉴스
- Publisher of the underlying yearbook: 국민건강보험공단
- Publisher of the retrieved document: 메디칼월드뉴스 (medicalworldnews.co.kr)
- URL: https://www.medicalworldnews.co.kr/m/view.php?idx=1510968457
- Accessed: 2026-09-03
- Retrieved: **no** — the item was returned only as a search-result summary; the article
  page itself was not opened
- What it would be good for: 2024 인정자 1,165천명 (+6.1%), 신청자 1,478천명 (+3.4%),
  판정 대비 인정률 89.5% (+0.9%p), the grade split (4등급 46.0%, 3등급 26.7%, 5등급 11.6%,
  2등급 8.5%, 1등급 4.8%, 인지지원 2.4%) and 급여비용 ₩16조1,762억 (+11.6%) with a
  공단부담률 of 91.3%. Every one of those figures is **[unverified]**; the grade
  *distribution* is independently corroborated by R13, which was retrieved.

### R25 — 보험저널, 2026년 보험료 전망 및 평균공시이율 관련 기사
- Publisher: 보험저널 (insjournal.co.kr), a trade outlet
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=29000
  (companion: …?idxno=29053)
- Accessed: 2026-09-03 (search-result summaries; the article pages were not opened)
- Retrieved: **no** (summary only)
- What it would be good for: the market's reading of the 2026 평균공시이율 cut to 2.50%
  and its transmission into 예정이율 and premium rates, and the statement that 보장성
  공시이율 stood at 2.2%, 연금 2.29% and 저축 2.22% at the month before the report. All of
  that is **[unverified]** here; the 평균공시이율 level itself is separately verified from
  R17.

### R26 — 금융감독원, 「2025년 3월말 / 6월말 기준 보험회사 지급여력비율 현황」
- Publisher: 금융감독원, mirrored by KDI 경제교육·정보센터
- URLs: https://eiec.kdi.re.kr/policy/materialView.do?num=267710 and
  https://eiec.kdi.re.kr/policy/materialView.do?num=271247
- Accessed: 2026-09-03
- Retrieved: **no** (listed in search results; neither page was opened)
- Recorded so that a later drafter has the quarter-by-quarter series to hand. Only R3's
  September 2025 figures are used.

### R27 — 보험연구원, 「2025년 보험산업 주요 이슈: ② IFRS17 및 K-ICS」
- Publisher: 보험연구원
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=618289
- Accessed: 2026-09-03
- Retrieved: **no** (identified in search results, not downloaded)
- Would carry the 2023–2025 supervisory-guideline chronology in one place, including the
  2023 실손의료보험 계리가정 산출기준 that R1 supersedes only in part.

### R28 — 금융감독원, 보험회사 종합공시 / 금융감독원 공식 사이트
- Publisher: 금융감독원
- URL: https://www.fss.or.kr
- Accessed: 2026-09-03
- Retrieved: **no** — a plain HTTPS request returned "Empty reply from server"; the site
  did not respond to the fetcher at all
- Consequence: every FSS release used in this file was obtained through a mirror (KDI
  경제교육·정보센터 for R2, R3) or through a trade newspaper (R16). Where only the
  newspaper route exists, the fact is marked as news-sourced.

---

## Fact extraction

### 1. The regulatory architecture in one page

- **금융위원회** (Financial Services Commission, FSC) is the rule-maker and the licensing
  authority; **금융감독원** (Financial Supervisory Service, FSS) is the examiner and the
  author of the implementing 세칙. The hierarchy a Korean actuary works down is
  법률 → 시행령 (Presidential Decree) → 시행규칙 (Prime Ministerial Rule) →
  **보험업감독규정** (an FSC 고시) → **보험업감독업무시행세칙** (an FSS 세칙) → 별표
  (schedules to either). Nearly every operative number in Korean insurance regulation
  lives in the last two layers, not in the statute [S1] [S3] [S6].
- **보험업법** governs the *undertaking*: licensing, reserves, solvency, the filing of
  product documents, the appointed actuary [S1]. **상법 제4편 보험** governs the
  *contract* between insurer and policyholder [S9]. They are separate statutes with
  separate ministries (금융위원회 and 법무부 respectively), and a Korean 약관 is drafted
  against both.
- A third layer sits under the 약관: the FSS publishes a **표준약관** (standard policy
  conditions) as 별표 15 to the 시행세칙, and insurers write their own conditions against
  it [S6 제5-13조] [S8]. The 표준약관 is not a model law to be adapted at will — the
  clauses reproduced in §24 below appear near-verbatim in every retail Korean policy.
- **보험개발원** (KIDI) is the statutory rate bureau. 보험업법 제176조 lets insurers set up
  a 보험요율 산출기관 with FSC authorisation; its statutory tasks are "순보험요율의 산출ㆍ
  검증 및 제공", the collection of insurance information and statistics, and research
  [S1 제176조제3항]. A rate it files with the FSC is a **참조순보험요율**, and an insurer
  applying it "순보험료에 대하여 제127조제2항 및 제3항에 따른 신고 또는 제출을 한 것으로
  본다" — deemed to have filed [S1 제176조제6항]. See §27.
- The consumer-conduct layer is the **금융소비자 보호에 관한 법률** (Financial Consumer
  Protection Act), which supplies the statutory cooling-off right and the
  suitability/explanation duties that the 표준약관 then implements [S13].

### 2. 보험업법 제2조 — what a "보험상품" is, and the three-way split

- 제2조제1호 defines 보험상품 as "위험보장을 목적으로 우연한 사건 발생에 관하여 금전 및
  그 밖의 급여를 지급할 것을 약정하고 대가를 수수(授受)하는 계약", excluding what the
  Decree excludes, and splits it three ways [S1 제2조제1호]:
  - **가. 생명보험상품** — "위험보장을 목적으로 사람의 생존 또는 사망에 관하여 약정한
    금전 및 그 밖의 급여를 지급할 것을 약속하고 대가를 수수하는 계약";
  - **나. 손해보험상품** — indemnity for loss from a fortuitous event, expressly
    **excluding** 질병ㆍ상해 및 간병 ("다목에 따른 질병ㆍ상해 및 간병은 제외한다");
  - **다. 제3보험상품** — "위험보장을 목적으로 사람의 질병ㆍ상해 또는 이에 따른 간병에
    관하여 금전 및 그 밖의 급여를 지급할 것을 약속하고 대가를 수수하는 계약".
- The carve-out in 나목 is the structural point: Korea does not treat sickness, injury
  and nursing care as a sub-species of indemnity insurance. It makes them a **third**
  category of their own, and 제2조제5호 then defines 제3보험업 as the business of dealing
  in them [S1].
- 시행령 제1조의2 closes the lists. 생명보험상품 is 생명보험계약 and 연금보험계약(퇴직보험
  계약을 포함한다) — **two** contract types only. 손해보험상품 is a list of fourteen
  (화재, 해상, 자동차, 보증, 재보험, 책임, 기술, 권리, 도난, 유리, 동물, 원자력, 비용,
  날씨). 제3보험상품 is exactly three: **상해보험계약, 질병보험계약, 간병보험계약**
  [S2 제1조의2제2항–제4항].
- 시행령 제1조의2제1항 also excludes six public schemes from "보험상품" altogether:
  고용보험, **국민건강보험**, 국민연금, **노인장기요양보험**, 산업재해보상보험 and 선불식
  할부계약 [S2]. Two of those six are the public schemes that `Medical_KR_S` and
  `LTC_KR_S` sit on top of — the statute is explicit that the private product is a
  different animal from the public one.
- Mapping the ten `krlib` products onto the taxonomy: `whole_life`, `term_life`,
  `pension_savings`, `variable_annuity` and `immediate_annuity` are **생명보험상품**;
  `indemnity_medical`, `cancer` and `long_term_care` are **제3보험상품**; `ci_insurance`
  and `child` are composites written as a 생명보험 주계약 with 제3보험 특약 attached, or
  as 제3보험 with a death rider, depending on the carrier. That composite structure is
  possible because of 제4조제3항, below.

### 3. 보험업법 제4조 — the licence, and why 제3보험 is written by everybody

- 제4조제1항, verbatim in structure [S1] [S18]:
  > 보험업을 경영하려는 자는 다음 각 호에서 정하는 보험종목별로 금융위원회의 허가를
  > 받아야 한다.
  > 1. 생명보험업의 보험종목 — 가. 생명보험 나. 연금보험(퇴직보험을 포함한다) 다. 그 밖에
  >    대통령령으로 정하는 보험종목
  > 2. 손해보험업의 보험종목 — 가. 화재보험 나. 해상보험(항공ㆍ운송보험을 포함한다)
  >    다. 자동차보험 라. 보증보험 마. 재보험(再保險) 바. 그 밖에 대통령령으로 정하는
  >    보험종목
  > 3. **제3보험업의 보험종목 — 가. 상해보험 나. 질병보험 다. 간병보험** 라. 그 밖에
  >    대통령령으로 정하는 보험종목
- **제4조제3항** is the provision that makes 제3보험 a shared field: a person licensed for
  *all* of the 생명보험업 or *all* of the 손해보험업 종목 (excluding 보증보험 and 재보험)
  "제3보험업에 해당하는 보험종목에 대한 허가를 받은 것으로 본다" — is deemed licensed for
  the third sector [S1]. Both a life insurer and a non-life insurer can therefore write
  the same 암보험 or 간병보험, and in practice both do, under different reserving and
  disclosure chapters of the 감독규정.
- 제4조제6항 restricts licensees to 주식회사, 상호회사 and 외국보험회사; a licensed foreign
  branch is treated as a 보험회사 under the Act [S1].
- Modelling consequence for `krlib`. `Cancer_KR_S`, `LTC_KR_S`, `Child_KR_S` and the
  indemnity half of `Medical_KR_S` are 제3보험. Their pricing and surrender rules are
  reached by a **cross-reference**: 감독규정 제7-70조 states that for 제3보험 "보험요율의
  산출과 보험료 및 해약환급금 산출방법서의 작성 등은 제7-65조, 제7-66조, 제7-67조 및
  제7-68조를 준용한다" — the life-insurance rules apply *mutatis mutandis* [S3 제7-70조].
  장기손해보험 gets the identical treatment in 제7-69조 [S3]. So one surrender-value
  regime governs all ten products, which is why this file can carry a single §16.

### 4. 기초서류 — the three documents a Korean product filing consists of

- 보험업법 제5조 requires a licence applicant to attach 정관, a three-year business plan
  with projected financial statements, and — 제3호 — the **기초서류**: "사업방법서,
  보험약관, 보험료 및 해약환급금의 산출방법서" [S19] [S1 제5조].
- 제127조제1항: "보험회사는 취급하려는 보험상품에 관한 기초서류를 작성하여야 한다."
  제127조제2항 makes prior notification to the FSC the **exception**, not the rule: it is
  required only where a new product is introduced or made compulsory by legislation
  (제1호) or where the Decree so provides for policyholder protection (제3호) [S1].
- 시행령 제71조제1항 sends 제127조제2항제3호 to **별표 6**, and 제71조제2항 requires the
  보험상품신고서 to be filed **30 days before the sale-start date** (15 days where it
  follows an FSC recommendation), with two attachments: the 기초서류 verified by the
  **선임계리사** under 제184조제1항, and, where premiums, surrender values or 위험률 change,
  a verification certificate from the **보험요율 산출기관 or an 독립계리업자** [S2 제71조].
- 감독규정 제7-51조 lists the three cases in which a 산출방법서 must be pre-notified
  [S3]:
  1. a 저축성보험 that does **not** spread at least 50% of the acquisition cost evenly
     over the premium-paying period (40% for a whole-life 생존연금, 70% through a
     bancassurance channel, 100% through an online channel), the period being at least
     seven years for a 저축성보험 with a payment term of seven years or more and at least
     fifteen months for single premium;
  2. a 보장성보험 that does not spread the acquisition cost evenly over the
     premium-paying period;
  3. a renewable or re-entry product whose **계약체결비용 on renewal exceeds 70% of the
     first contract's 계약체결비용**.
- 제128조 lets the FSC require FSS verification of a filing and lets it require a
  verification certificate from the rate bureau or an independent actuary on the
  보험료 및 해약환급금 산출방법서 [S1 제128조]. 제128조의2 requires every insurer to
  maintain a **기초서류관리기준** covering the drafting procedure, internal and external
  verification, error control, and the role of the 선임계리사 [S1]. 제128조의3 sets the
  drafting principles: no illegality, no unjustified reduction of policyholder rights,
  and conformity to FSC standards [S1].
- 감독규정 제7-64조 sets the **필필수기재사항** of the 산출방법서 — five items [S3]:
  1. the premium calculation, and for contracts longer than three years that must use
     **현금흐름방식** (cash-flow pricing) an analysis of premium adequacy based on
     **최적기초율** (best-estimate bases) with projected cash flows;
  2. the reserve calculation, including the interest and morbidity/mortality rates used
     in the 보험료적립금;
  3. the **해약환급금** calculation, including the interest rate, the 위험률, the
     해약공제액, and — where the 계약체결비용 exceeds the **표준해약공제액** at the
     기준연령 요건 — a comparison of the two;
  4. the calculation where benefits or premiums change;
  5. the calculation of any 보증비용.
- Provenance consequence, and it is the same as in `jplib`: the 산출방법서 is where
  예정이율, 예정위험률, 예정사업비율 and the surrender formula actually live, and it is
  **not public**. Only the 약관, the 상품요약서 and the 공시 disclosures are. Every
  pricing-basis parameter in `krlib` is therefore `[std]`, and every contractual
  parameter comes from a public 약관 or 상품요약서.

### 5. 선임계리사 — 보험업법 제181조 and 제184조

- 제181조제1항: an insurer must carry out 보험계리 — defined in the article itself as
  "기초서류의 내용 및 배당금 계산 등의 정당성 여부를 확인하는 것" — either by employing
  보험계리사 or by outsourcing to a 보험계리업자 [S1].
- 제181조제2항 requires the appointment of a **선임계리사**, described as the actuary who
  "보험계리에 관한 업무 전반을 관리하고 이를 검증 및 확인하는 등 보험계리 관련 업무를
  총괄하는" — a 2022-12-31 amendment that widened the role from verification to
  overall management of the actuarial function [S1].
- 제184조제1항: "선임계리사는 기초서류의 내용 및 보험계약에 따른 배당금의 계산 등이
  정당한지 여부를 검증하고 확인하여야 한다." 제2항 adds a duty to check compliance with
  the 기초서류관리기준, to report breaches to the board, and to report any statutory
  breach in the 기초서류 **to the FSC** [S1].
- 제184조제4항 gives the office tenure: once appointed, the 선임계리사 cannot be dismissed
  until the end of three consecutive business years following the year of appointment,
  subject to four exceptions (leaking secrets, negligence causing loss, improper demands
  or pressure, or an FSC dismissal demand under 제192조) [S1].
- 제184조제7항, new in 2022, bars the 선임계리사 from three jobs: direct product
  development (verification excepted), CEO or CFO, and any other conflicted role the
  Decree names [S1]. This is a hard separation of pricing from sign-off.
- 감독규정 제6-11조의4 requires a **책임준비금 적정성 검증보고서** within six months of the
  financial-year end, on a form the FSS Governor sets [S3].

### 6. 책임준비금 — the reserve, restated in IFRS 17 vocabulary

- 보험업법 제120조제1항: "보험회사는 결산기마다 보험계약의 종류에 따라 대통령령으로
  정하는 책임준비금과 비상위험준비금을 계상(計上)하고 따로 작성한 장부에 각각 기재하여야
  한다." 제2항 delegates the mechanics to a 총리령; 제3항 lets the FSC set accounting
  standards for their proper recognition [S1].
- 시행령 제63조제1항, as amended 2022-12-27, restates the reserve in IFRS 17 terms
  [S2]:
  1. **보험계약부채**, being the sum of 가. **발생사고요소** ("매 결산기 말 현재 보험계약
     상 지급사유가 발생한 보험금등을 지급하기 위해 미래현금흐름에 대한 현행추정치를
     적용하여 적립한 금액") and 나. **잔여보장요소** (the same, for benefits whose trigger
     has not yet occurred);
  2. **투자계약부채**, for contracts in the legal form of insurance that fall outside
     K-IFRS 1117 and are classified as investment contracts;
  3. anything else the FSC prescribes on a current-estimate basis.
- 시행령 제63조제4항 keeps **비상위험준비금** (catastrophe reserve) for non-life business
  only, within 50% of the year's premiums (150% for 보증보험) [S2]. It is therefore not
  a life-side item and `krlib` does not model it.
- 감독규정 제6-11조 splits 책임준비금 into 보험계약부채, 재보험계약부채 and 투자계약부채,
  and 제2항 splits each of the first two into 잔여보장요소 and 발생사고요소, with the rule
  that where a portfolio's two components sum below zero the balance is presented as a
  **보험계약자산** [S3]. 제4항 delegates the detailed calculation to the FSS Governor
  (i.e. to the 시행세칙 and its 별표).
- Ten paragraphs of the old 감독규정 제6-11조 (paragraphs ⑤ to ⑩) were **deleted on
  2022-12-21** [S22] [S3]. That deletion is the visible trace of the switch from a
  locked-in statutory reserve to a current-estimate one: before 2023 the 고시 itself
  carried accumulation rules; after 2023 it carries a taxonomy and a delegation.
- Scope note for `krlib`, matching the house position in `jplib` and `delib`: this
  library projects **gross best-estimate liability cash flows**. 책임준비금,
  해약환급금준비금, 보증준비금, 비상위험준비금, the K-ICS 요구자본 and the IFRS 17 risk
  adjustment and CSM are **cited, not computed**. What the models do compute is the
  **보험료적립금 / 계약자적립액** and the **해약환급금**, because those are contractual
  quantities defined by the 산출방법서 and bounded by 별표 14.

### 7. 해약환급금준비금 — the Korea-specific layer, in full

This has no counterpart anywhere else in the repository, so it is given in full.

- Legal chain: 보험업법 제120조 → 시행령 제65조제2항제3호 → **감독규정 제6-11조의6**
  (life) and **제6-18조의6** (non-life) [S1] [S2] [S3].
- 제6-11조의6제1항: "보험회사는 영 제65조제2항제3호에 따라 보험계약 해지에 대한 위험을
  고려하여 **보험회사 전체단위로** 해약환급금준비금을 산출하여 적립 또는 환입한다" — it is
  a **company-level**, not a contract-level or portfolio-level, calculation [S3].
- 제6-11조의6제2항 sets the test. At each balance-sheet date (including quarterly interim
  closes), for in-force contracts, compare:
  - **제1호** — 책임준비금 (restricted to the 잔여보장요소 of 보험계약부채 and
    재보험계약부채 plus 투자계약부채, net of the 잔여보장요소 of any 보험계약자산 and
    재보험계약자산 and of investment-contract policy loans) **plus** 특별계정부채 limited
    to the 계약자적립금 of 제6-26조제1항제1호, grossed up for unrealised gains and losses
    on those contracts recognised in OCI before tax; against
  - **제2호** — the **해약환급금 under 제7-66조제1항** (computed under the same rule even
    for the 제7-66조제4항 products that may pay less) **plus** the 미경과보험료 of
    제7-66조제5항, adjusted for policy-loan balances drawn and for amounts to be settled
    with reinsurers on surrender.
  Where 제1호 < 제2호, the shortfall is appropriated to a **해약환급금준비금 inside 이익
  잉여금** [S3].
- **제2항 단서, amended 2025-06-11**: "다만, 직전 분기말 경과조치 적용 전 지급여력비율이
  **130% 이상**인 경우 제3호의 금액을 적립한다", and 제3호 is "그 차액에 **100분의 80**을
  곱하여 산출한 금액" [S3]. So a well-capitalised insurer — measured on the K-ICS ratio
  **before** transitional measures at the previous quarter-end — appropriates only 80%
  of the shortfall. This is a solvency-conditioned distributable-earnings rule, and it
  is new: the 2023 text carried no such relief [S22].
- 제3항: where the insurer has an 미처리결손금 (unappropriated deficit) the appropriation
  starts only once that deficit is cleared, and any excess over the required balance is
  released [S3].
- 제4항: under a 공동재보험계약 (co-insurance-style reinsurance under 제7-12조제1항제3호)
  the cedant and the reinsurer each compute and hold the reserve in proportion to the
  ceded share [S3].
- **보증준비금** sits behind it. 제6-11조의5 requires a guarantee reserve inside retained
  earnings for expected losses on benefit guarantees, and 제2항 makes it explicitly
  junior: "보증준비금은 제6-11조의6에 따른 해약환급금준비금을 적립한 후에 적립하여야
  하며, 이익잉여금에서 … 해약환급금준비금을 차감한 금액을 한도로 한다" [S3]. For
  `VA_KR_S`, whose GMAB and GMDB guarantees are the reason a 보증준비금 exists, the
  ordering matters: the surrender-value reserve is taken first.
- Transitional: the 부칙 to 금융위원회고시 제2022-53호 (2022-12-22, in force 2023-01-01)
  provides for insurers that adopted K-IFRS 1117 early to compute the 해약환급금준비금
  for the first year of application **for corporate-tax purposes**, with an external
  audit-firm verification and a 별지 제26호 「해약환급금준비금 산출명세서」 filed with the
  FSS and reported to the board [S3 부칙].
- Why it exists, stated plainly. Under IFRS 17 a profitable in-force block can carry a
  liability materially below the aggregate contractual surrender value, because the CSM
  is a liability that unwinds into profit rather than a cash obligation. Distributing
  the resulting retained earnings would leave the insurer short if policyholders
  actually surrendered. The 해약환급금준비금 quarantines the difference. It is a
  **distributable-earnings** device, not a solvency device — it sits in 이익잉여금 and is
  therefore inside K-ICS 가용자본, unlike a genuine liability.
- Modelling consequence for `krlib`: none of the ten models computes it, but three
  documents must mention it — `whole_life`, `pension_savings` and `variable_annuity` —
  because in each the gap between 계약자적립액 and IFRS 17 liability is the whole point of
  the product's earnings profile. The 무·저해지 forms make the gap negative in the early
  years and steeply positive after 납입완료, which is exactly the shape the reserve was
  built to catch.

### 8. 계약자배당 — participating business and the 유배당/무배당 split

- 감독규정 제6-11조의7 splits the dividend-related reserves three ways: 계약자배당준비금,
  계약자이익배당준비금 and 배당보험손실보전준비금 [S3]. The 2026 text subdivides
  계약자배당준비금 into **금리차보장준비금, 총괄배당준비금, 장기유지특별배당준비금** and
  **재평가특별배당준비금**; the 2023 text had a five-way subdivision naming 위험률차배당
  준비금, 이자율차배당준비금 and 사업비차배당준비금 separately, which have been collapsed
  into 총괄배당준비금 [S22] [S3]. The Korean three-source vocabulary (위험률차 / 이자율차 /
  사업비차 — the direct analogue of Japan's 三利源) was therefore **regulatory language
  until recently and is no longer**; it survives in practice and in older filings.
- 제6-13조제1항 is the surplus-sharing rule for life insurers: after setting the
  책임준비금, the residual (계약자배당준비금적립전잉여금) is split into 유배당보험손익,
  무배당보험손익 and 자본계정운용손익; the second and third go wholly to shareholders, and
  of the **유배당보험이익 the shareholder share is capped at 100분의 10**, the remainder
  being the policyholder share [S3]. 제3항 ring-fences the policyholder share to dividends
  and to the 배당보험손실보전준비금.
- 제6-13조제4항 makes a shareholder dividend conditional on the **지급여력비율 being 100%
  or more at the year end** [S3].
- Market fact worth carrying: Korean retail protection business is overwhelmingly
  **무배당** (non-participating). Every product name in the 표준약관 illustrations and in
  the carrier disclosures examined carries 무배당; 유배당 survives mainly in legacy
  annuity blocks. `krlib` models no dividend, and says so.

### 9. K-ICS — the solvency regime, from the regulation itself

- 시행령 제65조제1항 defines the three quantities: **지급여력금액** (available capital),
  **지급여력기준금액** (required capital) and **지급여력비율** = the first divided by the
  second [S2]. 제65조제2항제1호, as amended 2026-04-21, states the requirement in one
  line: "**지급여력비율은 100분의 100 이상을 유지할 것**" [S2].
- 감독규정 제7-2조의2 sets the balance sheet the ratio is computed on — the **건전성감독
  기준 재무상태표**, which is (1) based in principle on the K-IFRS consolidated balance
  sheet and (2) measured "경제적이고 시장가격과 일관된 가치로", assets at exit price and
  liabilities at transfer or settlement price, with **no adjustment for the insurer's own
  credit standing** [S3]. That last exclusion is the standard economic-value convention
  and matches Solvency II.
- 감독규정 제7-1조 builds 지급여력금액 as 순자산 (assets less liabilities on that balance
  sheet) plus loss-absorbing liability items, less non-loss-absorbing assets, and then —
  제2항, new in 2022 — classifies the total into **기본자본** (tier 1) and **보완자본**
  (tier 2) by loss-absorbing capacity, with 제4항 capping 보완자본 at **50% of the
  지급여력기준금액** [S3].
- 감독규정 제7-2조제1항 builds 지급여력기준금액 as **기본요구자본 − 법인세조정액 +
  기타요구자본**, where 기본요구자본 aggregates five risk amounts through a correlation
  formula the FSS Governor sets (the formula itself renders as an image and did not
  extract) [S3]. The five are:
  - **생명ㆍ장기손해보험위험액**
  - **일반손해보험위험액**
  - **시장위험액**
  - **신용위험액**
  - **운영위험액**
- 제7-2조제2항 decomposes the life and long-term-health module into **seven** sub-risks,
  each with its stated measurement method [S3]:
  1. **사망위험액** — contracts whose net asset value falls when mortality rises;
     **충격시나리오방식** (shock-scenario);
  2. **장수위험액** — contracts whose net asset value falls when mortality *falls*;
     shock scenario;
  3. **장해ㆍ질병위험액** — disability and disease covers; shock scenario;
  4. **장기재물ㆍ기타위험액** — property, expense and liability covers inside long-term
     non-life; shock scenario;
  5. **해지위험액** — "보험계약자의 옵션행사율 변화 또는 보험계약 대량해지"; shock
     scenario;
  6. **사업비위험액** — every contract with an expense assumption; shock scenario;
  7. **대재해위험액** — extreme and exceptional risks not caught by 1–6 (epidemics, mass
     accidents); **위험계수방식** (factor-based).
- 제7-2조제4항 decomposes 시장위험액 into 금리, 주식, 부동산, 외환 (all shock-scenario) and
  **자산집중위험** (factor-based) [S3]. 제5항 and 제6항 make 신용위험액 and 운영위험액
  factor-based. 제7항 permits either the **표준모형** or an approved **내부모형** [S3].
- Direct relevance to `krlib`: sub-risks 1, 2, 3, 5 and 6 map one-for-one onto the
  decrements and expense assumptions the ten models carry. A `krlib` product document
  that discusses sensitivity should name the K-ICS sub-risk its sensitivity corresponds
  to, because that is the vocabulary a Korean actuary uses. **해지위험액** in particular
  is why the 무·저해지 lapse assumption is a supervisory issue and not only an earnings
  issue.

### 10. 적기시정조치 — the ladder below 100%

- 감독규정 제7-17조제1항제1호: the FSC **must** issue a 경영개선권고 (management-improvement
  recommendation) where "지급여력비율이 **50%이상 100%미만**인 경우", or where the
  경영실태평가 produces the stated grade combinations [S3]. The measures available include
  capital increase or reduction, expense cuts, branch rationalisation, limits on fixed
  assets, disposal of impaired assets, staff and organisational change, and **a
  restriction on shareholder or policyholder dividends** [S3 제7-17조제2항].
- 제7-18조 (경영개선요구) and 제7-19조 (경영개선명령) are the next two rungs; the article
  numbers are recorded because the K-ICS transitional deferral is expressed by reference
  to them.
- Transitional deferral: the 부칙 to 금융위원회고시 제2022-53호, 제4조제1항 allows the FSC
  to defer 제7-17조제1항제1호, 제7-18조제1항제1호 or 제7-19조제1항제2호 **until the
  2027-12-31 closing** for an insurer whose post-transitional K-ICS ratio at the first
  post-commencement balance-sheet date was below 100%, provided the ratio under the
  **old** regime would not have triggered them, that a 경영개선협약 is signed with the FSS
  Governor, and that compliance is reported quarterly [S3 부칙]. 제2항 requires the FSC to
  cancel the deferral on breach or non-reporting.

### 11. K-ICS 경과조치 — the ten-year phase-ins

From the 보험연구원 analysis of the FSS's final K-ICS design [R14]:

- The transitional package was settled at the 보험 자본 건전성 선진화 추진단's 9th meeting
  on 2022-02-24, having been under discussion since the 1st meeting on 2018-11-27 [R14].
- **Available capital.** Capital securities issued before commencement are recognised for
  **ten years**: pre-existing 신종자본증권 count as 기본자본 within the capital-securities
  limit of **15% of total 요구자본** even where they carry a step-up, with the excess
  reclassified to 보완자본; pre-existing 후순위채 count as 보완자본 even beyond the
  **50% of total 요구자본** tier-2 limit [R14].
- **Reporting.** Business-report and management-disclosure deadlines are extended by one
  month over the normal two months (quarterly) and three months (annual), for the first
  **three years** [R14].
- **Four optional ten-year phase-ins**, each conditional [R14]:
  1. **보험부채 증가분** — available only where the K-ICS liability exceeds the old-regime
     liability. The old-basis liability is defined as 해약환급금 + 계약자배당 관련 준비금 +
     보증준비금 − 보험계약대출 잔액 − 재보험자산 중 미경과보험료; the K-ICS liability as
     보험료부채 + 계약자배당 관련 부채 + 위험마진 − 보험계약대출 − 재보험자산 중
     출재보험료부채. The 2023-03-31 in-force book is recognised at **10% a year from 2024,
     reaching 100% in 2033**.
  2. **금리리스크** and 3. **주식리스크** — available only where the RBC risk amount is
     **60% or less** of the K-ICS risk amount. Worked example given: with a K-ICS
     금리위험액 of ₩10 billion and an RBC 금리위험액 of ₩5 billion the test is met, and 60%
     of the risk is recognised in 2023, rising **4 percentage points a year** to 100% from
     2033.
  4. **신규 도입리스크** — the life/long-term sub-risks the old RBC regime did not measure:
     **장수, 해지, 사업비, 대재해**.
- **Re-measurement.** The 보험부채 증가분 transitional is recalculated every two years, or
  whenever the 10-year government-bond yield moves **50bp or more** from the previous
  measurement, restricting the recalculation to the two valuation-type items —
  보증준비금 and the LAT 적립액 [R14].
- **Conditions on users.** Quarterly adequacy-verification reports to the FSS, with an
  additional independent-actuary or rate-bureau verification for the 보험부채 증가분; and
  a **dividend-payout brake** — if the payout ratio exceeds max{50% of the company's own
  five-year average, 50% of the industry's five-year average}, the remaining transitional
  period is **halved** [R14].
- **Comparison with Solvency II** [R14]: the EU phases the liability increase over 16
  years and new risks over 4, and defers early intervention by 2 years; Korea uses a
  uniform 10 years for all four and defers intervention by **5**.
- Two asset-side reliefs are recorded because they touch products in this library: a
  long-held-equity shock cut from **35% to 20%** for qualifying developed-market listed
  equity held on average five years with a documented ten-year holding plan, and a
  mandatory-holding-property shock cut from **25% to 20%** where the property is held
  because 노인장기요양법 or 사회복지사업법 obliges the insurer to own it [R14] — a direct
  regulatory link between an insurer's long-term-care operations and its capital charge.
- Application procedure: an insurer wishing to apply had to notify the FSS Governor
  **within two months of 2023-01-01** [R14].

### 12. K-IFRS 제1117호 — the earnings measure

- The Korean standard is **기업회계기준서 제1117호 「보험계약」**, resolved by the
  회계기준위원회 of the 한국회계기준원 on **2018-05-25** with a stated effective date of
  2021-01-01 [R23]; the effective date was subsequently deferred and the standard came
  into force for Korean insurers on **2023-01-01**, which is the date the 감독규정's
  IFRS 17 articles commence [S3 부칙, 금융위원회고시 제2022-53호] and the date the FSC uses
  [R4].
- The regulation borrows the standard's vocabulary directly: 시행령 제63조 speaks of
  **현행추정치** (current estimate) and of the 발생사고요소 / 잔여보장요소 split, and
  감독규정 제6-11조제3항 defines 투자계약부채 as the measured value of contracts "보험계약의
  법률적 형식을 취하고 있으나, 한국채택국제회계기준 제1117호의 적용을 받지 않아 투자계약
  으로 분류된 계약들" [S2] [S3].
- Scale of the change, from the FSC [R4]: required capital rose from **₩67.9조 under RBC
  at 2022-12-31 to ₩118.9조 under K-ICS at 2024-09-30**; the 기본자본 K-ICS ratio fell from
  145.1% (2023-03) to 132.6% (2024-09); 2024 capital-securities issuance reached **₩8.7조,
  272% of the prior year's ₩3.2조**.
- Discount curve, from the FSS's own description [R1]:
  - the risk-free term structure is built from 국고채 yields, with **관찰금리** used
    directly out to the **최종관찰만기 (LOT / LLP)**, currently **20 years**, then an
    interpolation to 60 years and a convergence segment beyond;
  - the convergence point is the **장기선도금리 (LTFR)**, "실질이자율 장기평균 + 물가상승
    목표", **currently 4.55%**;
  - a **유동성프리미엄** is added, being the total risk spread less the credit spread
    unrelated to the contract, **currently 91bp**;
  - the phase-in agreed in August 2023 raises the annual LTFR adjustment cap from 15bp to
    **25bp** (from 2024), realises the loan-yield input to the liquidity premium (2024),
    removes unexpected risk from the liquidity premium (2027), rationalises the 100%
    adjustment ratio (2026), and extends the LOT from **20 to 30 years from 2025** — the
    last of which was then itself spread over **three years** by the November 2024
    decision [R1].
  - Government 10-year yields quoted in the same document, as the reason for the
    slow-down: **3.74% (2022 year-end) → 3.18% (2023 year-end) → 3.40% (2024-03) → 3.26%
    (2024-06) → 2.99% (2024-09)** [R1].
- Combined financial-impact estimate: at a 10-year government yield of 3.0% the industry
  K-ICS ratio was expected to fall about **20 percentage points** from the 2024-06-30
  level of **217.3%**, absorbed through the existing transitionals [R1].
- CSM levels for context, forecast by 보험연구원 [R15]: 생명보험 CSM ₩64.7조 (2025E) →
  ₩64.3조 (2026E), a 0.6% fall; 손해보험 CSM ₩70.3조 → ₩71.8조, a 2.1% rise against 7.0%
  in 2025 [unverified — these two lines were read from a search summary of the same
  seminar, not from the retrieved slide deck, which carries the premium tables but whose
  CSM slide did not extract cleanly].

### 13. 계약자적립액 and the crediting-rate machinery

- 감독규정 제7-65조제1항: "계약자적립액은 보험료 및 책임준비금 산출방법서에 따라 계산한
  금액으로 한다"; 제2항 permits it to be computed on an **annualised premium** basis
  ("연납보험료를 기준으로 하여 산출할 수 있다") [S3]. That permission is the reason a
  Korean monthly-premium product can carry an annual-recursion account and is directly
  relevant to how `Cancer_KR_S`, `Medical_KR_S`, `Child_KR_S`, `LTC_KR_S` and `VA_KR_S`
  reconcile a monthly grid with an annual reserve.
- 제7-66조제1항제4호 states that 계약자적립액 accrues **monthly before 납입완료** ("보험료
  납입이 완료되기 이전에는 … 월별 기간경과에 따라 산출한다") and **daily afterwards**
  ("보험료납입이 완료된 이후에는 … 일별 기간경과에 따라 산출한다") [S3]. The two formulas
  themselves are images in the source page and did **not** extract — recorded as a gap.
- **공시이율** (the declared crediting rate). 제7-65조제3항: "공시이율은 **공시기준이율**에
  **조정률**을 반영하여 다음 각호의 방법에 따라 결정하여야 한다" [S3]:
  1. 공시기준이율 is computed per the FSS Governor's rules by a weighted average of an
     objective external index rate and the **운용자산이익률**;
  2. 운용자산이익률 = 운용자산수익률 − 투자지출률, computed on invested assets excluding
     unrealised gains and losses not passed through profit or loss, with the
     운용자산수익률 taken from the **preceding twelve months'** investment income
     (excluding insurance finance income) and the investment cost from the same period's
     investment expense (excluding insurance finance expense);
  3. the 공시이율 must be **uniform across a product class** the FSS Governor defines, with
     four exceptions — 유배당 versus 무배당, timing mismatches from differing reset cycles,
     the 농협생명/농협손해보험 legacy 공제계약 versus post-2012-03-02 products, and setting
     a rate **below the floor applying to existing contracts**;
  4. items 1 and 2 must be written into the 기초서류.
- 시행세칙 제5-16조제3항 supplies the FSS's part [S6]:
  - the **objective external index rates** are the yields on **국고채(5년),
    회사채(무보증 3년, AA-), 통화안정증권(1년)** and **양도성예금증서(91일)**, with
    substitution allowed if a publisher discontinues one;
  - the 공시기준이율 calculation is **별표 27**;
  - a newly established insurer, or one with a sharp fall in investment return, may use
    an alternative method notified to the FSS.
- 시행세칙 제5-16조제4항 fixes the product classes across which the rate must be uniform
  [S6]:
  - **생명보험**: 보장성보험(순수보장성 및 기타보장성), 보장성보험(**종신보험**),
    생사혼합보험(만기 7년 이하), 생사혼합보험(만기 7년 초과), **연금보험**, 교육보험;
  - **손해보험**: 보장성보험(만기 15년 이하), 보장성보험(만기 15년 초과), 저축성보험(만기
    7년 이하), 저축성보험(만기 7년 초과), 개인연금보험.
- **별표 27, verbatim in its operative parts** [S7]:
  > 공시기준이율 = 객관적인 외부지표금리 × α + 운용자산이익률 × (1−α)
  >
  > 객관적 외부지표금리 = 국고채(5년) 수익률 × β1 + 회사채(무보증 3년, AA-) 수익률 × β2
  > + 통화안정증권(1년) 수익률 × β3 + 양도성예금증서(91일) 유통수익률 × β4
  - the four yields are taken as a **three-month weighted moving average ending at the
    end of the month two months before the application date**;
  - β1…β4 are the shares of the insurer's own prior-year average balances of domestic
    public bonds, corporate bonds, monetary stabilisation bonds and CDs, "직전년도" being
    the twelve months ending three months before the start of the business year; the
    weights are **rounded to 0.5 percentage points and constrained to [0%, 100%]** and
    held constant through the business year;
  - α is a function of the opening 계약자적립액, the prior year-end asset duration and
    the prior year's premium income (the formula itself is an image and did not extract);
    it is **rounded to 0.5 percentage points**, held constant through the business year,
    and **may not exceed 60%**;
  - the rate is computed **separately by account** (계정별) unless an account is too small
    to permit it;
  - added 2025-10-28: for a reinsurance treaty where the assuming insurer recognises the
    whole investment result on identified assets, those assets and their investment income
    enter the **assuming** insurer's 운용자산이익률, not the ceding insurer's.
- **최저보증이율.** 감독규정 제7-60조제10호: "금리연동형보험의 경우 **최저보증이율 또는
  최저보증금액을 설정하여야 한다**" (신설 2022-12-22) [S3]. A Korean interest-sensitive
  product is therefore required by regulation to carry a guaranteed floor; its level is a
  company matter. 제7-60조제7호 separately requires a **최저사망보험금** for 변액보험 and
  for 금리연동형보험 other than annuities [S3].
- **평균공시이율.** 감독규정 제1-2조제13호 defines it as the average of all insurers'
  공시이율, computed as the FSS Governor prescribes [S3]. The 표준약관 defines it for the
  policyholder as "전체 보험회사 공시이율의 평균으로, 이 계약 체결 시점의 이율" [S8], and
  a carrier disclosure adds that it is "0.25%포인트 단위로 반올림하여 산출" and applied to
  the whole policy term for a contract concluded in that year [R17].

### 14. 평균공시이율 — the published series

From a carrier's regulatory disclosure of the FSS-set figure [R17]:

| Period | 평균공시이율 |
|---|---|
| 2026-01-01 – 2026-12-31 | **2.50%** |
| 2025-01-01 – 2025-12-31 | 2.75% |
| 2024-01-01 – 2024-12-31 | 2.75% |
| 2023-01-01 – 2023-12-31 | 2.25% |
| 2022-01-01 – 2022-12-31 | 2.25% |
| 2021-01-01 – 2021-12-31 | 2.25% |
| 2020-01-01 – 2020-12-31 | 2.50% |
| 2019-01-01 – 2019-12-31 | 2.50% |
| 2018-01-01 – 2018-12-31 | 2.50% |
| 2017-01-01 – 2017-12-31 | 3.00% |
| 2016-01-01 – 2016-12-31 | 3.50% |

The same page carries the predecessor **표준이율**, which the 평균공시이율 replaced: 3.25%
for 2015, 3.50% for 2014 and for 2013-04-01 onwards [R17].

Where the 평균공시이율 bites, all four verified from the regulation:

1. **저축성보험 design test** — 감독규정 제7-60조제3호: the 계약자적립액 accumulated at the
   평균공시이율 must exceed premiums paid at 납입완료 (seven years where the payment term
   is seven years or more, fifteen months for single premium), and for a whole-life
   생존연금 or a 연금저축보험 the test may be run at **평균공시이율 + 0.25%p** [S3].
   제7-60조제4호 requires the risk premium, guarantee charge and separate-account
   management fee to be set to **zero** in that test [S3].
2. **저축성보험 alternative test** — 제7-60조제3의2호 (신설 2023-06-27) exempts an annuity
   product whose 계약자적립액 or annuity amount at the annuity commencement date, computed
   at the 평균공시이율, exceeds that of a 제3호-compliant design, provided the two are
   compared and explained to the customer [S3].
3. **부활 interest ceiling** — 표준약관 제27조: arrears repaid on reinstatement carry
   interest "평균공시이율 + 1% 범위 내에서 각 상품별로 회사가 정하는 이율" [S8].
4. **계약자배당 interest floor** — 감독규정 제6-13조 area: interest added to a declared but
   unpaid dividend must be at least the prior year's 평균공시이율 [S3].
5. **변액보험 보증준비금 roll-forward** — the 부칙 to 고시 제2022-53호 accumulates the
   transition-date guarantee reserve at the pricing interest rate, and for 변액보험 at
   "매 사업연도별 해당시점의 평균공시이율" [S3].

### 15. 예정이율 — what it is, and what is not public

- The term **예정이율** (the pricing interest rate) does **not appear in 보험업감독규정 at
  all** — a full-text search of the retrieved 2026-05-06 text returns zero hits [S3]. It
  lives in the 산출방법서, which is not public, and in the marketing register. What the
  regulation names instead is the **계약자적립액 적용이율**: 제1-2조제6호 defines a
  **금리연동형보험** as one where that rate varies with the insurer's investment return and
  market rates, and 제7호 defines a **금리확정형보험** as one where it is fixed [S3].
- The consequence for `krlib` is unavoidable and must be stated in every product
  document: **the 예정이율 of any specific Korean product is not a published number.**
  Trade reporting places the 2026 direction of travel downward, following the
  평균공시이율 cut from 2.75% to 2.50%, with an expected 2–5% rise in protection premiums
  [R25] — but that is a news summary that was not opened, so it is **[unverified]** and no
  level is asserted here. Every 예정이율 in `krlib` is `[std]`, with the 평균공시이율 series
  in §14 as its anchor and its rationale.
- The 공시이율 by product class **is** published, product by product and month by month,
  through the KLIA 공시실 and each carrier's 공시실 [R19]. A retrieved example: one large
  carrier published a **공시기준이율 of 3.19%** with an 적용률 of 3.19% and hence an
  적용이율 of 3.19% across 보장(무배당), 연금(무배당), 연금(배당), 저축(무배당) and
  연금저축(배당) — but the page's month selector did not return, so the as-of date is
  unknown and the level is recorded as illustrative only [R18].

### 16. 표준해약공제액 — the surrender-charge cap, verbatim

This is the article that bounds unamortised acquisition-cost recovery on surrender, and
it has no US or UK analogue at this level of prescription. Two layers.

**Layer one — 감독규정 제7-66조 (생명보험 해약환급금의 계산)** [S3]:

- 제1항제1호: "해약환급금은 **계약자적립액에서 … 해약공제액을 공제하여 계산한 금액이상**
  으로 산출할 수 있다. 다만, 계약자적립액에서 해약공제액을 공제한 금액이 음(陰)의 값인
  경우에는 이를 **영(零)으로** 처리한다." The formula display itself is an image and did
  not extract; the operative words did.
- 제1항제2호: "제1호에 따른 **해약공제기간**은 보험료 납입기간 또는 신계약비 부가기간으로
  하되, 보험료 납입기간 또는 신계약비 부가기간이 **7년 이상일 때에는 7년으로** 한다."
- 제1항제3호: "제1호에 따른 … 해약공제액은 **별표 14에서 정한 표준해약공제액으로** 한다."
- 제3항: for contracts on which no 해약공제액 is deducted, benefits may instead be
  differentiated on early surrender.
- 제5항 (신설 2022-12-21): "보험회사는 보험계약이 해지되는 경우 해약환급금에 **미경과
  보험료 등을 가산한 금액**을 보험계약자에게 지급하여야 한다."
- 제7-69조 applies the whole of 제7-65조–제7-68조 to **장기손해보험** (including
  연금저축손해보험 and 퇴직보험), and **제7-70조** applies it to **제3보험** [S3]. One rule,
  all ten products.

**Layer two — 별표 14, reproduced in full** [S4]:

> **표준해약공제액**
> **= 연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000**
>
> 주)
> 1. 장기손해보험에서 연령에 관계없이 단일보험료를 적용하는 상품 및 비용손해담보상품의
>    경우에는 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납위험보험료의
>    45%**」로 적용 &lt;개정 2020.1.15.&gt;
> 2. **해약공제계수**는 다음과 같이 적용함
>    - 보장성보험: **보험기간(최대 20년)**
>    - 저축성보험: **보험료 납입기간(최대 12년)**. 명칭을 불문하고 납입기간의 범위 내에서
>      의무적으로 납입해야 하는 별도의 기간을 설정한 경우에는 당해 별도의 납입기간을
>      보험료 납입기간으로 함. 다만, **일시납보험의 경우 납입기간을 1년**으로 함
> 3. **연납순보험료 및 연납위험보험료**는 다음과 같이 적용함 &lt;개정 2020.1.15.&gt;
>    - 보장성보험: **전기납(단, 보험기간이 20년 이상인 경우 20년납)**으로 조정하여 산출한
>      연납순보험료 및 연납위험보험료. 다만, 연납위험보험료 계산시 별표15 제9호 단서의
>      위험보험료 계산에 관한 규정을 준용한다.
>    - 저축성보험: **납입기간(최대 10년)** 동안 동일하게 배분한 평균식 부가보험료를 제외한
>      연간순보험료
> 4. **보험기간이 종신인 생존연금보험(연금저축보험은 제외)** 표준해약공제액의 경우에는
>    **연납순보험료의 6%**를 적용하되, 연납순보험료의 5%와 **해약공제계수 12년**을 적용하여
>    산출한 해약공제액을 초과할 수 없음.
> 5. **연금저축보험** 표준해약공제액의 경우에는 **연납순보험료의 4%(무배당 연금저축보험은
>    3%)**를 적용함 &lt;신설 2014.12.31&gt;
> 6. 보험계약 체결에 사용할 금액을 보험료 납입기간 동안 보험료에 부가하는 저축성 보험의
>    경우에는 보험료에 부가된 금액을 **평균공시이율로 할인**하여 표준해약공제액에서 차감
>    하여 적용함 &lt;신설 2012.2.28, 개정 2014.12.31., 2020.1.15.&gt;
> 7. **실손의료보험**은 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납
>    위험보험료의 15%**」로 적용한다. &lt;신설 2015.5.7., 개정 2020.1.15.&gt;

**Reading it for `krlib`.** The cap is a *level* amount, not a schedule: a single
표준해약공제액 is computed once and deducted from the 계약자적립액 during the 해약공제기간,
which is the premium-paying period capped at seven years. Product by product:

- `Term_KR_S`, `WholeLife_KR_S`, `CI_KR_S`, `Child_KR_S` (protection portion),
  `Cancer_KR_S`, `LTC_KR_S`: 보장성보험. Coefficient = policy term, capped at 20. Annual
  net premium recomputed on a whole-term-pay basis (20-year pay where the term is 20
  years or more). Plus 10/1000 of the sum assured.
- `Medical_KR_S`: 보장성보험, but note 7 replaces the sum-assured term with **15% of the
  annual risk premium** — the only product-specific override in the schedule, and it
  exists precisely because an indemnity product has no 보험가입금액 in the ordinary sense.
- `Pension_KR_S`: 연금저축보험. **4% of the annual net premium** (3% if 무배당), coefficient
  = premium-paying period capped at 12.
- `Immediate_KR_S`: a whole-life 생존연금 that is not a 연금저축보험 — note 4 gives **6% of
  the annual net premium**, subject to the 5% × 12-year ceiling, and a single-premium
  contract takes a coefficient of **1**. Note the interaction: a single-premium immediate
  annuity's cap is therefore very small relative to premium.
- `VA_KR_S`: 저축성보험 for the coefficient (payment period capped at 12; annual premium
  computed over a payment period capped at 10), and 제7-66조제4항제1호 bars a 변액보험 from
  the sub-cap surrender values described in §18.

**Related caps** the same regulation attaches to the same quantity [S3]:

- 제4-32조제5항: for 보장성보험 other than general non-life and motor, the commission and
  other remuneration paid in the **first year** must not exceed the premium the
  policyholder is expected to pay in that year — and where the contract deducts **80% or
  more of the 표준해약공제액** on surrender, the projected surrender value at the one-year
  point is added to the commission side of that test.
- 제4-32조제6항: if the contract lapses within a year, remuneration actually paid (again
  with the surrender value added for the 80%-plus case) must not exceed premiums actually
  received.
- 제4-32조제8항: where the 표준해약공제액 exceeds one year's premiums, the insurer must
  offer distributors an instalment commission structure paying **no more than 60% of the
  표준해약공제액 a year** (수수료 분할지급방식).
- 제7-45조제11항: a 보장성보험 whose **계약체결비용 exceeds the 표준해약공제액** must
  disclose a **계약체결비용지수** and a **부가보험료지수** in the 상품요약서 — except that a
  whole-life death-benefit 보장성보험 need not, provided the 계약체결비용 is within
  **1.4 times** the 표준해약공제액 (applied to the death-benefit portion only where the
  product covers both death and non-death risks) [S3].

That 1.4× tolerance is a useful outer bound for a `[std]` acquisition-cost assumption on
`WholeLife_KR_S`: an insurer may load up to 1.4 × 표준해약공제액 on a whole-life death
product without triggering index disclosure, so a reference implementation that sets
계약체결비용 at or below the 표준해약공제액 is conservative and defensible.

### 17. 보험가입금액 — 별표 15, and why it matters to the cap

별표 15 defines the 보험가입금액 that enters the 표준해약공제액 formula, and it is not
simply "the face amount" [S5]:

> 보험업감독규정 제7-67조의 규정에 의한 보험가입금액은 다음 각호에서 정한 방법에 의하여
> 계산된 금액 **이하**로 하여야 한다.
> 3. **일반사망을 보장하는 보장성보험은 일반사망보험금으로 한다.** &lt;개정 2020.1.15.&gt;
> 6. 유족연금 등과 같이 보험금이 확정되지 아니하는 보험은 **기준연령 요건**으로 가입하여
>    중간시점에 사망한 것으로 하여 지급되는 보험기간별 보험금액 중 **최저 보험금액**으로
>    한다.
> 8. 제3호는 **체증 또는 체감되기 이전의 금액**으로 한다. &lt;개정 2020.1.15.&gt;
> 9. 제3호에 해당되지 아니한 경우에는 기준연령 요건에서 다음과 같이 산출한다.
>    &lt;개정 2020.1.15.&gt;
>    > **보험가입금액 = (위험보험료 / 사망만을 보장하는 순수보장성보험(이하 "정기보험")의
>    > 위험보험료) × 정기보험의 보험가입금액**
>    다만, 정기보험은 해당 보험상품과 동일한 보험기간 기준으로 적용하며, 위험보험료 계산시
>    다음의 항목은 포함하지 아니한다.
>    - 위험 발생여부와 관계없이 지급하는 보험금을 위한 부분
>    - 특정 위험이 발생하지 않을 경우 지급하는 보험금을 위한 부분
>    - **치매 또는 일상생활장해 등 타인의 간병을 필요로 하는 상태 및 이로 인한 치료 등의
>      위험 발생시 지급하는 보험금을 위한 부분**

Three things follow. First, a 제3보험 product with no death benefit gets a *notional*
보험가입금액 by scaling a term policy's face amount by the ratio of risk premiums —
which is how 별표 14's "보험가입금액의 10/1000" term is given meaning for `Cancer_KR_S`
and `Child_KR_S`. Second, the third bullet **excludes long-term-care risk premium** from
that ratio, so `LTC_KR_S`'s notional 보험가입금액 is driven by whatever non-care risk the
contract carries, not by the care benefit. Third, "기준연령 요건" is the standardising
convention defined at 감독규정 제1-2조제2호: "전기납 및 월납 조건으로 **남자가 만 40세**에
보험에 가입하는 경우", with the mid-point issue age used where a 40-year-old male cannot
buy the product or the product is an age-terminating one (including 종신보험 and 연금보험),
and the longest available payment term where whole-term pay is unavailable [S3]. That
40-year-old-male-monthly-whole-term-pay convention is the single reference cell of Korean
product regulation, and `krlib` should make it model point 1 wherever the product allows.

### 18. 무해지 / 저해지환급형 — the form that dominates Korean protection sales

- **The permission.** 감독규정 제7-66조제4항: for a **순수보장성보험** or a whole-life
  생존연금 whose premiums or benefits were calculated using a **최적해지율**, the insurer
  "제1항에서 정한 해약환급금 미만으로 지급할 수 있다" — may pay **less than** the
  별표-14-floored surrender value [S3]. That is the legal basis of the 무해지/저해지 form:
  it is not a contractual gimmick, it is a regulatory dispensation conditional on having
  used a best-estimate lapse rate in pricing.
- **The three exceptions** to that permission [S3 제7-66조제4항]:
  1. **변액보험인 경우** (신설 2020-11-19) — a variable product may never use it;
  2. where the surrender value during the payment period is **less than 50% of that of an
     otherwise identical 표준형 상품**, both of the following must hold:
     - 가. after the payment period, the surrender value **exceeds 50%** of the 표준형
       product's surrender value; and
     - 나. after the payment period, the **환급률** (surrender value over cumulative
       premiums paid at each point) **exceeds the greater of 100% and the 표준형 product's
       환급률**;
  3. (deleted).
- Read carefully, exception 2 is the **환급률 cap**: it permits the deep-discount form only
  if the post-payment refund ratio clears 100% *and* the standard product's ratio — which,
  combined with the FSC's stated intent, is how a 무해지 product is prevented from being a
  better savings vehicle than a 표준형 one. The FSC's own worked example when the rule was
  proposed: a 20-year-pay 종신보험 with a 표준형 20-year 환급률 of **97.3%** against a
  then-current 무해지 20-year 환급률 of **134.1%**, the amendment limiting the latter to
  the former [R5].
- **The 2020 rule-making.** The FSC's July 2020 입법예고 recorded that 20 life insurers and
  11 non-life insurers were selling the form as a flagship product, defined a 무(저)해지
  환급금 보험 as "보험료 산출 또는 보험금(연금액) 산출시 **해지율을 사용한 보험**", and
  strengthened the 시행세칙 제5-19조 internal controls on lapse-rate derivation,
  verification and profitability sensitivity [R5]. The four life insurers and three
  non-life insurers not writing the form were named; no market-share figure was given.
- **The scale of the form.** From the FSC/FSS November 2024 release, the share of
  무·저해지 products in **보장성 초회보험료** (first-year protection premium) [R1]:

  | Year | 무·저해지 share of 보장성 초회보험료 |
  |---|---|
  | 2018 | 11.4% |
  | 2021 | 30.4% |
  | 2023 | 47.0% |
  | 2024 H1 | **63.8%** |

  Nearly two-thirds of new Korean protection business by first-year premium is now written
  in a form whose surrender value is nil or suppressed until 납입완료. Any Korean reference
  library that models only 표준형 products is modelling a minority of the market.
- **The lapse-rate guideline of November 2024**, and it is the most consequential
  assumption ruling in this file [R1]:
  - The problem the FSS named: because there is no experience, insurers assumed **high
    lapse right up to 완납**, which flatters profitability, and the resulting switching out
    of 표준형 products raised observed 표준형 lapse, which was then fed back into the
    무해지 assumption — "악순환".
  - The ruling: among models converging to zero lapse at 완납, the **로그-선형(log-linear)
    모형** is judged most appropriate and is adopted as the **원칙모형**, with a practical
    convergence point of **0.1%**.
  - Alternatives are permitted only within a closed list — **선형-로그모형 (converging to
    0% at 완납)** and **로그-로그모형 (converging to 0.1%)** — and only if the insurer
    discloses, in the audit report and the management disclosure, the reason for the
    choice, an external actuarial verification, and the difference from the principle model
    in **CSM, best-estimate liability, K-ICS ratio (both required and available capital)
    and net income**, reports the difference to the FSS quarterly, and submits to an on-site
    inspection.
  - **Post-완납 ultimate lapse rate: 0.8%**, from overseas statistics, or alternatively a
    **20% relativity** to the overseas standard-form lapse rate.
  - **단기납 종신보험**: where a short-pay whole-life product (5–7 year pay) carries a
    bonus at, say, year 10 producing a refund ratio of e.g. **135%**, the insurer must
    assume an **additional lapse of at least 30%** at the bonus date, or back it out from
    the standard product's cumulative persistency. The 30% floor is calibrated to the
    ten-year average of the **11th-year lapse rate on single-premium bancassurance savings
    business, 29.4%–30.2%**, that being the point at which the tax exemption is met and the
    refund ratio jumps.
  - **Loss ratios must be split by age cohort** where experience is sufficient and the age
    split is statistically significant. The worked industry example given is the
    상해수술 cover: **30s 89% → 40s 103% → 50s 140% → 60s 186%**.
  - Application: from the **2024 year-end closing**, with loss-ratio assumptions permitted
    to slip to 2025 Q1 where systems could not be changed in time; the discount-rate
    soft-landing applies from **2025-01**.
- Modelling consequence for `krlib`, and it should appear in every protection product's
  technical notes: the `lapse_rate` vector on a 무해지 or 저해지 form is not free. A
  reference implementation should use a **log-linear decay to 0.1% at 납입완료 and 0.8%
  thereafter**, tagged `[std]` with R1 as the rationale, and should carry a switch to the
  표준형 assumption so that the two can be compared — which is exactly the comparison the
  guideline requires an insurer to disclose.

### 19. 상품설계 규제 — what a Korean product may and may not do

**생명보험 — 감독규정 제7-60조** [S3], the ten design rules, of which eight survive:

- 제2호: for a 저축성보험 the survival benefit must **exceed premiums paid**, except for an
  annuity paying a 생존연금 and for 변액보험.
- 제3호 and 제4호: the 평균공시이율 accumulation test described in §14.
- 제3의2호: the comparison-based exemption described in §14.
- 제7호: **변액보험 and 금리연동형보험 (other than annuities) must set a 최저사망보험금**.
- 제8호: except where severe injury or disease makes cover impracticable, a contract must
  **not be extinguished** while the risk it covers remains effective. This is the rule
  behind Korean cancer and CI products that continue after a diagnosis payment rather than
  terminating.
- 제9호: the **death benefit must be at least cumulative premiums paid**, except after
  annuity payments have begun and except where the premium-paying period ends at age 80 or
  below.
- 제10호: **금리연동형보험 must set a 최저보증이율 or a 최저보증금액**.

**제3보험 — 감독규정 제7-63조제1항** [S3]:

- 제1호: a product must be designed so that, **on death from a cause the policy does not
  cover**, the 계약자적립액 and the 미경과보험료 of 제7-66조제5항 are paid and the contract
  terminates. This single rule is why `Cancer_KR_S`, `LTC_KR_S` and `Medical_KR_S` all need
  an account balance even though they are not savings products, and it is a first-order
  modelling requirement: a `krlib` 제3보험 model must have a defined payment on
  non-covered death.
- 제7-61조 applies the whole of 제7-63조 to **장기손해보험**, so a non-life insurer's
  long-term health product is designed to the same rules [S3].

### 20. 실손의료보험 — the generations, and the fifth

**What it is.** 실손의료보험 (*silson uiryo boheom*) reimburses the policyholder's own share
of medical cost — the 본인부담금 under 국민건강보험 plus 비급여 (non-covered) charges —
above a deductible and within annual limits. The FSS calls it, in terms, "**제2의 건강보험
역할**" and dates it from 1999 [R2]. It is the only indemnity product in `krlib`.

**The generations, from the FSS's own table** [R2]:

| 세대 | Sold | 자기부담률 |
|---|---|---|
| 1세대 | –2009-09 | 손보 0% / 생보 20% |
| 2세대 | 2009-10 – 2017-03 | 표준형 20%, 선택형Ⅰ 10%, 선택형Ⅱ 급여 10% / 비급여 20% |
| 3세대 | 2017-04 – 2021-06 | 급여 10% or 20%, 비급여 특약 30% |
| 4세대 | 2021-07 – | 주계약 (급여) 20%, 특약 (비급여) 30% |

Renewal cycles: 1세대 1–5 years, 2세대 3 years then 1 year, 3세대 and 4세대 **1 year**
[R2]. The re-entry (재가입) cycle — the point at which the policyholder moves to the
then-current generation's benefit design — is set by 감독규정 제7-63조제2항제6호나목:
"보험기간 및 보장내용 **변경주기를 5년 이내**로 할 것", with three years for 노후실손 and
유병력자실손 [S3]. So a Korean 실손 contract renews annually at attained-age rates and
re-enters a new benefit generation every five years — a contract-boundary structure with no
counterpart elsewhere in this repository.

**The fifth generation.** The FSC announced the design on **2025-04-01** [R7] and the
감독규정 and 표준약관 amendments took effect on **2026-05-06** [S3] [S8]. The three-part
structure:

1. **기본형 실손의료보험 (급여)** — 감독규정 제7-63조제2항제2호 [S3], and 표준약관
   「기본형 실손의료보험(급여 실손의료비)」 [S8]. Two 보장종목: **상해급여** and **질병급여**.
   - **입원**: pays **80% of the 본인부담금** — i.e. a 20% co-payment — with the deducted
     amount capped at **₩2,000,000 (200만원) a year**, the excess above that cap being
     reimbursed within the sum-insured limit [S3] [S8 제5조제4항].
   - **통원** (outpatient plus dispensing, per visit): deduct the greater of
     - **₩20,000 (2만원)**, 20% of the covered cost, or the **건강보험 본인부담률** applied
       to the covered cost — at a 전문요양기관, 상급종합병원 or 종합병원;
     - **₩10,000 (1만원)**, 20%, or the 건강보험 본인부담률 — at any other 의료기관,
       보건소·보건의료원·보건지소, 보건진료소, or pharmacy/한국희귀필수의약품센터 [S3] [S8].
   - The 건강보험 본인부담률 is defined in the 약관 as
     `급여일부본인부담 항목의 본인부담금 ÷ (급여일부본인부담 항목의 본인부담금 + 급여
     공단부담금)`, with 100%-본인부담 items excluded from both the ratio and the cover
     [S8]. This is the linkage the FSC described as "건보정책과의 연계성 강화" [R7] —
     the private co-payment now tracks the public one.
   - **Limits**: annual 보험가입금액 up to **₩50,000,000 (5천만원)** for each of 상해급여 and
     질병급여, combining inpatient and outpatient; outpatient capped at **₩200,000 (20만원)
     per visit** [S8 제5조제1항, 제5항].
2. **실손의료보험 특별약관1 (중증 비급여)** — a separate rider [S3 제7-63조제2항제2의2호]
   [S8]:
   - **입원**: deduct **30%** of covered cost; where the deduction on care at a 종합병원 or
     상급종합병원 exceeds **₩5,000,000 (500만원) a year**, deduct only ₩5,000,000. The
     amendment excludes 근골격계질환 이학요법료, 체외충격파치료 and 비급여주사제 from that
     aggregation, deducting them separately.
   - **통원**: deduct the greater of **₩30,000 (3만원)** and **30%** of covered cost, per
     visit (외래 plus 처방·조제 combined).
   - Scope: 비급여 arising from a condition that **is** a 산정특례 target under 국민건강
     보험법 제44조 area rules — i.e. cancer, cerebrovascular and other severe disease.
3. **실손의료보험 특별약관2 (비중증 비급여)** — the rider that carries the reform's weight
   [S3 제7-63조제2항제2의3호, 신설 2026-05-06] [S8]:
   - **입원**: deduct **50%** of covered cost.
   - **통원**: deduct the greater of **₩50,000 (5만원)** and **50%**, per visit.
   - Annual limits: **₩50,000,000** each for 상해비급여 and 질병비급여; a separate
     **3대비급여** sub-limit; per-visit outpatient limit **₩200,000 (20만원)**; a per-visit
     비급여 cap of **₩3,000,000 (300만원)** on certain items and a **50% of 비급여 병실료**
     rule with a daily average cap [S8].
   - 감독규정 제7-63조제2항제1호 requires 비중증비급여 to be **written as a separate
     특약**, not inside the base contract [S3].
- **비급여 할인·할증 (experience rating).** 감독규정 제7-63조제2항제3의3호, as amended
  2026-05-06, permits an insurer to apply a **요율 상대도** to the net premium of the
  비중증 비급여 특약 on renewal, based on claims paid in the twelve months ending three
  months before the renewal date; 제3의2호 makes the ±25% annual rate-change corridor of
  제3호 apply to the pre-relativity premium [S3]. The 표준약관's implementation is a
  five-band table, reproduced verbatim [S8 특별약관2 제6조제3항]:

  | 단계 | 1단계 (할인) | 2단계 (유지) | 3단계 (할증) | 4단계 (할증) | 5단계 (할증) |
  |---|---|---|---|---|---|
  | 12-month claims paid | ₩0 (no claim) | >₩0 and <₩1,000,000 | ₩1,000,000–<₩1,500,000 | ₩1,500,000–<₩3,000,000 | ≥₩3,000,000 |
  | 요율 상대도 | 할인 (balancing) | 100% | 200% | 300% | 400% |

  The surcharge applies only to contracts with **₩1,000,000 or more** of annual claims, and
  the discount is set each year so that total premium before and after the relativity is
  unchanged — a pure redistribution [S8 제6조제3항, 제4항]. **Long-term-care grades 1 and 2
  under 노인장기요양보험법 are excluded** from the claims count [S8], a direct statutory
  cross-reference between `Medical_KR_S` and `LTC_KR_S`.
- **The ±25% corridor.** 감독규정 제7-63조제2항제3호: "실손의료보험에서 **위험구분단위별로
  보험료의 변경이 매년 ±25%를 초과하지 않을 것**", except where the insurer is under, or
  likely to come under, 제7-16조–제7-19조 measures [S3]. That is a hard bound on the annual
  re-rating a `Medical_KR_S` model may apply.
- **Other design rules** in 제7-63조제2항 [S3]: annual verification of the adequacy of the
  net rate from experience (five years' grace for genuinely new cover) (제6호가목); the
  five-year benefit-change cycle (제6호나목); a requirement to sell or hold a 노후실손 product
  if covering ages 75 and over (제6호다목); a mandatory suspend-and-resume facility for
  policyholders doubly covered through a group scheme (제7호); and a mandatory conversion
  facility from group-only cover to an individual policy (제8호).
- **노후실손** carries its own rules: sum insured capped at the combined annual maximum of
  a normal 실손, outpatient per-visit limit **₩1,000,000 (100만원)**, and a first-tier
  deduction of **₩300,000 (30만원) inpatient / ₩30,000 (3만원) outpatient** before further
  co-payments of at least 20% (급여) and at least 30% (비급여), the inpatient deduction
  capped at **₩5,000,000 (500만원) a year** [S3 제7-63조제2항제5호].
- **계약재매입.** The FSC's April 2025 package offers about **16 million** first- and
  early-second-generation policyholders a voluntary buy-out with **no-underwriting
  conversion** to the new product, with the mechanics to follow in the second half of 2025
  and the 약관 conversion window running **2026-07 to 2036-06** [R7].

### 21. 실손 in numbers — the FSS business results

All from the FSS's 2024 실적 release, which is the authoritative quantitative source [R2].

**Contracts in force (만건, 10,000 contracts), individual business only (group and 공제
excluded):**

| | 2022 | 2023 | 2024 | Change |
|---|---|---|---|---|
| Total | 3,565 | 3,579 | **3,596** | +17 (+0.5%) |
| 생보사 | 614 | 606 | 598 | −8 (−1.3%) |
| 손보사 | 2,951 | 2,973 | 2,998 | +25 (+0.8%) |

**By generation (만건):** 1세대 731 → 682 → **638** (−6.5%); 2세대 1,705 → 1,623 →
**1,552** (−4.4%); 3세대 852 → 826 → **804** (−2.7%); 4세대 208 → 376 → **525** (+39.6%).
A further **77만건 (2.1%)** are 유병력자실손 and 노후실손 [R2].

So at 2024 year-end **35.96 million** individual 실손 contracts were in force against a
population of about 51 million — the "second national health insurance" description is
quantitatively fair — and **43.2%** of them were still second-generation, sold before 2017.

**Premium income (억원):** total 131,885 (2022) → 144,429 (2023) → **163,364** (2024),
+13.1%; 생보사 29,086; 손보사 134,278 [R2].

**Underwriting result (억원):** −15,301 (2022) → −19,747 (2023) → **−16,226** (2024), the
loss narrowing 17.8%. 생보사 turned to a loss of −437; 손보사 −15,788 [R2].

**경과손해율 (earned loss ratio):**

| | 2022 | 2023 | 2024 |
|---|---|---|---|
| Total | 101.3% | 103.4% | **99.3%** |
| 생보사 | 84.7% | 86.4% | 86.5% |
| 손보사 | 104.8% | 107.1% | 102.0% |
| 1세대 | 113.2% | 110.5% | **97.7%** |
| 2세대 | 93.2% | 92.7% | **92.5%** |
| 3세대 | 118.7% | 137.2% | **128.5%** |
| 4세대 | 91.5% | 113.8% | **111.9%** |

The FSS notes that 3세대 first repriced in 2023 and 4세대 first repriced in 2025 [R2].

**Monthly premium, male aged 40, all covers, non-life basis (만원)** [R2]:

| | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|
| 2세대 | 3.0 | 3.5 | 3.8 | **4.0** |
| 3세대 | 1.6 | 1.7 | 2.0 | **2.4** |
| 4세대 | 1.5 | 1.5 | 1.5 | **1.5** |

(1세대 is excluded as its structure is not standardised.) A 4세대 policy at ₩15,000 a month
against a 2세대 policy at ₩40,000 a month for the same insured is a 2.7× spread — which is
the whole economics of the 계약재매입 offer.

**Claims paid (억원)** [R2]: total 128,868 (2022) → 140,813 (2023) → **152,234** (2024),
+8.1%; **급여 63,306** (+7.7%) and **비급여 88,927** (+8.4%). The three largest treatment
groups: **비급여 주사제 28,092억원 (18.5% of all claims, +15.8%)**, **근골격계 물리치료
26,321억원 (17.3%, +14.0%)** and **암 치료 15,887억원 (10.4%, +13.3%)**. Two named
procedures with runaway growth: 무릎줄기세포주사 ₩147억 (2022) → ₩458억 (2023) → **₩645억**
(2024), and 전립선결찰술 ₩262억 → ₩340억 → **₩438억** [R2].

**By institution class** [R2]: 의원 32.2%, 병원 23.3%, 종합병원 17.3%, 상급종합병원 14.0%
of claims paid — against NHIS treatment-cost shares in 2023 of 의원 28.1%, 상급종합 22.9%,
종합병원 20.9%, 병원 10.4%. 한방병원 claims rose from ₩5,115억 to ₩5,939억 (+16.1%) and
한의원 from ₩1,175억 to ₩1,511억 (+28.6%).

**Average 비급여 claim per contract per year (만원)** [R2]: 1세대 36.1 → 36.3 → **40.0**;
2세대 21.9 → 23.1 → **25.4**; 3세대 13.1 → 16.4 → **18.2**; 4세대 7.4 → 10.9 → **13.6**.
The FSS's own summary is that 1세대 runs at **two to three times** 3세대 and 4세대 — a clean
demonstration that the co-payment structure, not the insured population, drives the claim.

### 22. 변액보험 and 특별계정

- **When a separate account is mandatory.** 보험업법 제108조 permits, and 감독규정 제5-6조
  제1항 requires, a 특별계정 for six contract classes [S1] [S3]:
  1. contracts establishing a **연금저축계좌** under 소득세법 제20조의3제1항제2호;
  2. 근로자퇴직급여 보장법 제29조제2항 retirement pension contracts (other than
     퇴직연금실적배당보험) and legacy 퇴직보험;
  3. **변액보험계약 written by a life insurer**, and 퇴직연금실적배당보험;
  4. (deleted);
  5. **장기손해보험 written by a non-life insurer**;
  6. **자산연계형보험** (asset-linked), other than those applying the 공시이율.
- 제5-6조제3항: a life insurer's 변액보험 may be run as **two or more 집합투자기구**
  (collective investment schemes), excluding PEF-type vehicles [S3]. That is the legal
  form of the fund menu.
- 제5-6조제5항: what goes into the separate account is the **적립 보험료** — "영업보험료에서
  위험보장에 필요한 부분과 사업비 등 기초서류에서 정한 사항을 차감한 금액" — and its
  investment return [S3]. This is precisely the `av_pp` recursion a `VA_KR_S` model needs:
  gross premium less risk charge less expense charge, accumulated at the fund return.
- 제5-6조제6항: for classes 1 and 5 the applied rate follows the 공시이율 machinery of
  제7-65조제3항 [S3] — so a **연금저축보험 is a separate-account product whose account
  credits at the 공시이율**, which is the single most important structural fact about
  `Pension_KR_S`.
- 제5-7조 lists the only permitted transfers between the separate and general accounts:
  premium receipt and benefit/dividend/refund payment; transfer to the general account of
  amounts needed for risk cover and for contract acquisition, maintenance and
  administration; management fees, loans and repayments; bond settlement; **covering a
  separate-account deficit out of the general account's shareholder equity**; and anything
  else necessary to maintain the account [S3].
- 제6-26조: the separate-account 계약자적립금 for 변액보험 is the **whole** profit or loss
  arising in that account in the year, appropriated to the contract; for 원리금보장형 it is
  the amount computed under the general account's 산출방법서 [S3].
- **Guarantees.** 제7-60조제7호 requires a **최저사망보험금** for 변액보험 [S3]; the
  guarantee reserve is 제6-11조의5's 보증준비금, junior to the 해약환급금준비금 [S3]; and
  제7-64조제5호 requires the **보증비용** calculation to be written into the 산출방법서 [S3].
  The Korean market names for the two guarantees `VA_KR_S` carries are **최저연금적립금보증
  (GMAB)** and **최저사망보험금보증 (GMDB)**, and their charge is the **보증비용**; those
  three terms do not appear in the retrieved regulation, which speaks only of 최저사망
  보험금 and 보증비용, so the GMAB label is **[unverified]** as regulatory language while
  being standard market usage.
- 제7-66조제4항제1호 bars a 변액보험 from the sub-표준 surrender values of the 무해지 form
  [S3], so `VA_KR_S` must carry a full 별표-14-floored surrender value.

### 23. 상법 제4편 — the contract law a Korean policy is drafted against

The general part (제1장 통칙), all verbatim in the operative words [S9]:

- **제638조** — a contract of insurance takes effect on the promise of premium against the
  promise of "일정한 보험금이나 그 밖의 급여" on an uncertain event affecting property,
  life or body.
- **제638조의2** — the insurer must accept or decline **within 30 days** of receiving the
  application with premium (running from the medical examination in an 인보험 requiring
  one); silence is acceptance (제2항); and if the insured event occurs before acceptance the
  insurer is liable unless it had grounds to decline (제3항).
- **제638조의3** — the insurer must deliver the 약관 and explain its important content; on
  breach the policyholder may **cancel within three months of formation**. (This is the
  statutory source of the 표준약관's 품질보증해지 — see §24.)
- **제640조** — a 보험증권 must be issued without delay once the contract is formed.
- **제649조** — the policyholder may terminate **at any time** before the insured event
  (제1항), and on termination may claim the **미경과보험료** absent other agreement (제3항).
- **제650조** — non-payment of the first premium voids the contract two months after
  formation absent other agreement (제1항); for renewal premiums the insurer must give a
  reasonable period of notice before terminating (제2항).
- **제650조의2** — where a contract has been terminated under 제650조제2항 and **the
  surrender value has not been paid**, the policyholder may within a stated period pay the
  arrears with agreed interest and demand **부활** (reinstatement).
- **제651조** — 고지의무위반: on intentional or grossly negligent misstatement or omission
  of a material fact, the insurer may terminate **within one month of learning of it and
  within three years of formation**, but not if it knew or was grossly negligent in not
  knowing.
- **제651조의2** — a matter the insurer asked about **in writing is presumed material**.
- **제652조** and **제653조** — the duty to notify a material increase in risk, and the
  one-month window to demand an increased premium or terminate.
- **제655조** — where the insurer terminates under 제650조, 제651조, 제652조 or 제653조 after
  the event, it need not pay and may recover what it paid; **but** it must pay "고지의무를
  위반한 사실 또는 위험이 현저하게 변경되거나 증가된 사실이 보험사고 발생에 영향을 미치지
  아니하였음이 증명된 경우" — the causation defence.
- **제656조** — the insurer's liability begins on receipt of the first premium absent other
  agreement.
- **제657조** and **제658조** — notification of the event, and payment **within 10 days** of
  the amount being determined where no period is agreed.
- **제659조** — 면책: no liability where the event arises from the intention or gross
  negligence of the policyholder, insured or beneficiary. **제660조** — no liability for war
  or civil disturbance absent agreement.
- **제662조 (소멸시효)** — "보험금청구권은 **3년**간, 보험료 또는 적립금의 반환청구권은
  **3년**간, 보험료청구권은 **2년**간 행사하지 아니하면 시효의 완성으로 소멸한다."
- **제663조** — the whole Part is **one-way mandatory**: no special agreement may vary it to
  the disadvantage of the policyholder, insured or beneficiary (reinsurance and marine
  excepted).

인보험 and its three sub-classes [S9]:

- **제727조** — the 인보험 insurer pays on an event affecting the life or body of the
  insured; 제2항 (2014) permits **instalment payment** by agreement, which is the statutory
  hook for Korean products that pay a lump sum as an income stream.
- **제729조** — **no subrogation** against third parties in 인보험, except that an 상해보험
  contract may agree subrogation to the extent it does not prejudice the insured.
- **제730조** — the life insurer pays on death, survival, or both.
- **제731조** — a policy on **another's death requires that person's written consent** at
  formation (electronic signature admitted since 2017), and the same on assignment.
- **제732조** — a policy on the death of a person **under 15**, or of a person of unsound
  mind, is **void**, with a narrow exception for a 심신박약자 with capacity at formation or
  when becoming an insured under a group policy. This is why `Child_KR_S` cannot carry a
  meaningful death benefit below age 15 and must be modelled accordingly.
- **제732조의2** — gross negligence of the policyholder, insured or beneficiary does **not**
  exclude a death benefit; and where one of several beneficiaries intentionally kills the
  insured, the others are still paid.
- **제733조** and **제734조** — designation and change of beneficiary, and notice.
- **제735조의3** — 단체보험: 제731조 does not apply where a group insures its members under
  a 규약; but naming a beneficiary who is neither the insured nor the insured's heir
  requires the insured's written consent unless the 규약 says so expressly.
- **제736조** — **보험적립금반환의무**: where the contract is terminated under 제649조,
  제650조, 제651조 or 제652조–제655조, or the insurer is discharged under 제659조 or 제660조,
  the insurer must pay the policyholder "보험수익자를 위하여 적립한 금액" — the accumulated
  amount. This is the statutory floor beneath the 계약자적립액 that 감독규정 제7-63조제1항제1호
  makes explicit for 제3보험.
- **제737조–제739조** — 상해보험: the insurer pays on bodily injury; 제739조 applies the life
  insurance rules **except 제732조**, so a child under 15 *may* be insured against injury.
- **제739조의2** (2014) — 질병보험: "질병보험계약의 보험자는 피보험자의 질병에 관한 보험
  사고가 발생할 경우 보험금이나 그 밖의 급여를 지급할 책임이 있다."
- **제739조의3** — 질병보험 borrows the life and accident rules so far as consistent.

Note what 상법 does **not** contain: there is no 간병보험 chapter. Long-term care is a
제3보험 종목 under 보험업법 but reaches the contract law only through 제739조의3's borrowing.
`LTC_KR_S`'s benefit definition therefore comes from 노인장기요양보험법 (§32) and from the
약관, not from 상법.

### 24. 표준약관 — the clauses every Korean policy carries

All from the 생명보험 표준약관, 별표 15 to the 시행세칙 [S8].

- **보험나이 (제21조)**, verbatim:
  > ① 이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다. 다만, 제19조(계약의
  > 무효) 제2호의 경우에는 실제 만 나이를 적용합니다.
  > ② 제1항의 보험나이는 계약일 현재 피보험자의 **실제 만 나이를 기준으로 6개월 미만의
  > 끝수는 버리고 6개월 이상의 끝수는 1년으로** 하여 계산하며, 이후 매년 계약 해당일에
  > 나이가 증가하는 것으로 합니다.
  > ③ 피보험자의 나이 또는 성별에 관한 기재사항이 사실과 다른 경우에는 정정된 나이 또는
  > 성별에 해당하는 보험금 및 보험료로 변경합니다.

  and the worked example the 약관 itself prints:
  > 【보험나이 계산 예시】 생년월일: 1988년 10월 2일, 현재(계약일): 2014년 4월 13일
  > ⇒ 2014년 4월 13일 − 1988년 10월 2일 = 25년 6월 11일 = **26세**

  This is nearest-birthday age computed by a six-month rule, and it differs from 만나이 for
  half of all issue dates. Every `krlib` model must declare which it uses: **보험나이 for
  pricing, 만나이 for statistics**, because 국가데이터처's 생명표 and the NHIS statistics are
  on 만나이.
- **청약철회 (제17조)** — the cooling-off right. The policyholder may withdraw **within 15
  days of receiving the 보험증권**, and never after **30 days from the application date**
  [S8 제17조제1항, 제2항]; three exclusions — contracts where the insurer funds a health
  examination, contracts of **90 days or less**, and contracts made by a 전문금융소비자.
  Withdrawal takes effect **on despatch** of the notice (phone, writing, e-mail, SMS or
  equivalent), premiums are returned **within 3 business days**, and late return carries
  interest at the **보험계약대출이율 compounded annually** [S8 제17조제3항, 제4항]. The
  statutory source is 금융소비자보호법 제46조제1항제1호: "일반금융소비자가 「상법」 제640조에
  따른 보험증권을 받은 날부터 **15일**과 청약을 한 날부터 **30일** 중 먼저 도래하는 기간"
  [S13]. 제46조제4항 bars any damages or penalty on withdrawal; 제46조제5항 says the
  withdrawal is ineffective if a claim event has already occurred, unless the policyholder
  withdrew knowing it had.
- **품질보증해지 (제18조제3항)** — where the insurer failed to deliver the 약관 and the
  policyholder's copy of the application, or failed to explain the important content, or
  the policyholder did not sign the application, the policyholder may cancel **within three
  months of the contract being formed**, and gets premiums back with 보험계약대출이율
  interest compounded annually [S8]. Statutory source: 상법 제638조의3제2항 [S9].
- **계약 전 알릴 의무 (제13조, 제14조)** — the 약관 states in terms that this "상법상
  '고지의무'와 같습니다". The insurer may **not** terminate or restrict cover where [S8
  제14조제1항]:
  1. it knew or was negligent in not knowing at formation;
  2. **one month has passed since it learned of the breach**, or **two years have passed
     from the 보장개시일 without a claim event (one year for disease in a 진단계약)**;
  3. **three years have passed since the contract date**;
  4. it accepted on the basis of a health-examination document and the claim arises from a
     matter stated in it;
  5. the 보험설계사 prevented or discouraged truthful disclosure.
  제14조제4항 carries the causation defence: if the insurer cannot prove the breach affected
  the occurrence, the claim up to the point of termination is paid. 제14조제5항 bars
  termination for non-disclosure of **other insurance held**.
- **사기에 의한 계약 (제15조)** — proxy examination, drug use to pass underwriting, forged
  certificates, or concealment of a pre-application cancer or HIV diagnosis: the insurer may
  cancel **within five years of the 보장개시일 and within one month of learning of the
  fraud** [S8].
- **계약의 무효 (제19조)** and **보험나이 exception** — the 만나이 is used for the 제19조제2호
  void case (the under-15 death policy of 상법 제732조) [S8].
- **납입최고 and 해지 (제26조)** — on non-payment of a renewal premium the insurer must give
  a demand period of **at least 14 days** (7 days where the policy term is under a year),
  stating that the contract terminates the day after the period ends and that **the policy
  loan principal and interest will immediately be deducted from the surrender value**. The
  insurer remains liable for events before termination. On termination the 제32조제1항
  surrender value is paid [S8].
- **부활 (제27조)** — where the contract terminated under 제26조 and **the surrender value
  has not been drawn** (including where it was consumed by a policy loan, and including
  where there is none — the 무해지 case), the policyholder may apply for reinstatement
  **within three years of termination**, paying the arrears with interest at a rate the
  insurer sets **within 평균공시이율 + 1%** (a rate set in the 사업방법서 for 금리연동형).
  The disclosure articles reapply; the insurer may **not** refuse reinstatement because a
  claim event occurred before termination [S8].
- **해약환급금 (제32조)** — computed per the 산출방법서, paid **within 3 business days** of
  a claim, with interest per 부표 4-1; **the insurer must give the policyholder a table of
  surrender values by elapsed period** (제3항). Where the contract is terminated as a
  위법계약 under 제29조의2, the **계약자적립액** is returned instead [S8].
- **보험계약대출 (제33조)** — the policyholder may borrow within the surrender value on the
  insurer's terms, "그러나 **순수보장성보험 등** 보험상품의 종류에 따라 보험계약대출이
  제한될 수도 있습니다"; unpaid principal and interest are deducted from any benefit or
  surrender value [S8]. So a 무해지 protection product may have no policy loan at all — a
  point `WholeLife_KR_S` and `Term_KR_S` must state.
- **계약자적립액**, defined in a box beside 제22조: "장래의 해약환급금 등을 지급하기 위하여
  계약자가 납입한 보험료 중 일정액을 기준으로 보험료 및 해약환급금 산출방법서에서 정한
  방법에 따라 계산한 금액" [S8].
- **계약의 소멸 (제22조)** — where death makes further benefits impossible, the contract ends
  and, if death is not itself an insured event, the insurer pays "'보험료 및 해약환급금
  산출방법서'에서 정하는 바에 따라 회사가 적립한 **사망 당시의 계약자적립액**" [S8]. This is
  the 표준약관's implementation of 감독규정 제7-63조제1항제1호 for 제3보험 products.
- **보험금의 지급사유 (제3조)** — the five statutory categories a Korean life policy pays
  on: 중도보험금 (survival at a stated point), 만기보험금, 사망보험금, **장해보험금** (a
  disability state on the 장해분류표 percentage scale), and **입원보험금 등** ("질병이 진단
  확정되거나 입원, 통원, 요양, 수술 또는 **수발**이 필요한 상태가 되었을 때") [S8]. The
  fifth category is where 제3보험 benefits attach, and the word 수발 is the 약관's term for
  the need of care that a 간병보험 pays on.
- **소멸시효 (제37조)** and **예금보험에 의한 지급보장 (제43조)** carry the 상법 제662조
  three-year period and a cross-reference to 예금자보호법 [S8].
- The **장해분류표 (부표 3)** defines 장해 as "상해 또는 질병에 대하여 치유된 후 신체에 남아
  있는 **영구적인** 정신 또는 육체의 훼손상태 및 기능상실 상태", excluding temporary states
  during treatment [S8]. It is the common disability scale behind 납입면제 (premium waiver)
  in every Korean protection product, and it is a **percentage** scale, not a binary one.

### 25. 경험생명표 — the mortality basis, and why every krlib table is [std]

- The **경험생명표** is produced by **보험개발원** as the industry's experience mortality
  table, revised roughly every five years. The current edition is the **제10회 경험생명표**,
  released in early January 2024 and applied by insurers to **new business from April
  2024** [R8].
- Published summary statistics [R8]:

  | Statistic | 제10회 (2024-04) | Change vs 제9회 |
  |---|---|---|
  | 평균수명, 남 | **86.3세** | +2.8 years |
  | 평균수명, 여 | **90.7세** | +2.2 years |
  | 65세 기대여명, 남 | **23.7년** | +2.3 years |
  | 65세 기대여명, 여 | **27.1년** | +1.9 years |

  This was the first edition in which female 평균수명 exceeded 90 [R8].
- **What is not published: the qx table.** No 경험생명표 mortality rates were located in any
  public KIDI channel. The KIDI 보도자료 listing served no 경험생명표 item [R22]; the KIDI
  보험정보 빅데이터 플랫폼 page that indexes 경험생명표 **refused connection** on port 9443.
  The table is distributed to member insurers, and its role in regulation is indirect —
  감독규정 제1-2조제1호 defines the **참조순보험요율** as the 위험률 the rate bureau files with
  the FSC, not as a published table [S3]. This is the sharpest single contrast with `jplib`,
  where the IAJ's 標準生命表 numeric tables are downloadable, and with `delib`, where DAV
  tables are documented in published Fachgrundsätze.
- Uses stated for the table by KIDI, as reported: an insurer may use the 경험생명표 where its
  own experience is insufficient; the table is used in computing the **보험가격지수**
  published for consumer comparison; and it serves alongside the 통계청 국민생명표 as a
  national mortality indicator [R8].
- Directional pricing effect of the 제10회 revision, as reported: **death products
  (종신보험, 정기보험) cheaper; annuity and health products dearer** [R8]. That is the
  expected sign and is worth stating in `whole_life`, `term_life`, `pension_savings` and
  `immediate_annuity`.
- **Consequence for `krlib`, stated once here and cross-referenced everywhere.** Because the
  industry table is not public, **every `mort_table.csv` in `krlib` is a `[std]`
  construction.** The construction anchors on:
  1. the public **국가데이터처 생명표** (§26), which gives qx-equivalent survivorship for the
     whole population by single year of age and sex;
  2. the two published 경험생명표 summary statistics — 평균수명 and 65세 기대여명 — which
     bracket the level of *insured* mortality against the population;
  3. the observation, implicit in the pair, that insured mortality is materially lighter
     than population mortality at the ages that matter: population 기대수명 at birth in 2024
     was 남 80.8 / 여 86.6 [R9] against insured 평균수명 남 86.3 / 여 90.7 [R8], and
     population 65세 기대여명 was 남 19.5 / 여 23.7 [R9] against insured 남 23.7 / 여 27.1
     [R8] — a gap of about **4.2 years for males and 3.4 years for females at age 65**.
  Every row of every `krlib` mortality table therefore carries a `provenance` column, and the
  library's tables must never be presented as the 경험생명표.

### 26. 국가데이터처 생명표 — the public alternative

- Korea's official life tables are produced by the **국가데이터처** (National Data Office —
  the renamed 통계청), in two forms: the **완전생명표** (complete, single year of age, from
  vital registration and the register) and the **간이생명표** (abridged). The tables are
  published annually with a two-year lag [R9] [R10].
- **2024년 생명표, published 2025-12-03** [R9]:

  | | 전체 | 남자 | 여자 |
  |---|---|---|---|
  | 기대수명 at birth | **83.7년** | **80.8년** | **86.6년** |
  | change on 2023 | +0.2 | +0.2 | +0.2 |
  | 40세 기대여명 | — | 41.9년 | 47.4년 |
  | 65세 기대여명 | — | **19.5년** | **23.7년** |
  | survival to 80 | — | 64.4% | 82.2% |

  Korea's 기대수명 exceeds the OECD average by 2.3 years (male) and 2.9 years (female),
  ranking 11th and 3rd [R9].
- **2023년 생명표, published 2024-12-04** [R10]: 기대수명 전체 83.5년, 남 80.6년, 여 86.4년
  (+0.8, +0.7, +0.8 on 2022 after the COVID-affected 2022 fall of 0.9); 65세 기대여명 남
  19.2년 / 여 23.6년; the sex gap 5.9 years.
- The definition the release gives is the standard period-table one: "연령별 사망 수준이
  그대로 유지될 경우 향후 몇 세까지 생존할 수 있는지를 추정한 결과" [R10].
- Licensing: 국가데이터처 statistics are public-sector open data. The single-year qx tables
  themselves are distributed through **KOSIS** (kosis.kr); they were **not downloaded** in
  this session — see the fetch-failure section — so `krlib`'s table build must fetch them
  separately and record the KOSIS table id in each product's `sources.md`.

### 27. 참조순보험요율 — the rate bureau's filed rates

- 감독규정 제1-2조제1호: "'참조순보험요율'이란 법 제176조제4항 및 영 제87조제1항에 따라
  **보험요율산출기관이 금융위에 신고한 위험률**을 말한다" [S3].
- 제1-2조제18호: "'참조순보험료'란 **평균공시이율, 평균해지율 및 참조순보험요율을 적용하여
  계산한 순보험료**를 말한다. 다만, 참조순보험요율이 없는 경우에는 제17호의 **최적위험률을
  보수적으로 할인ㆍ할증한 위험률**을 사용한다" (신설 2012-02-28, 개정 2023-06-27) [S3]. The
  2023 amendment added 평균해지율 to the inputs — a direct consequence of the lapse-assumption
  controversy in §18.
- What the 참조순보험료 is *for*: 감독규정 제7-45조제7항 requires a 보장성보험 (other than
  general non-life) to publish in its 상품요약서 a **보험가격지수**, being "보험료총액을
  참조순보험료 총액과 보험회사 평균사업비총액을 합한 금액으로 나눈 비율", and a
  **보장범위지수**; and for 실손의료보험 the 보험가격지수 must be explained **on each
  renewal** as well [S3]. So the rate bureau's reference rates become visible to the public
  only as a *ratio*, never as a rate.
- 보험업법 제176조제6항: applying a filed 참조순보험요율 is deemed compliance with the
  제127조 filing obligation for the net premium [S1]. 제176조제9항 lets the bureau publish
  "순보험요율 산출에 관한 자료" where policyholder protection requires it [S1].
- **No 참조순보험요율 value was retrieved.** They are not published; the KIDI 보도자료 listing
  carried none [R22]. Every morbidity and incidence rate in `krlib` is therefore `[std]`,
  constructed from public epidemiology (§30, §31, §32) and marked as such.

### 28. Tax

**Pension savings — 연금저축, the tax credit** [S10] [S11]:

- 소득세법 제59조의3제1항 gives a **credit against tax, not a deduction from income**, of
  **12%** of the amount paid into a 연금계좌 — **15%** where 종합소득금액 for the year is
  ₩45,000,000 or less (₩55,000,000 총급여 for the employment-income-only case).
- The caps: contributions to a **연금저축계좌 above ₩6,000,000 (600만원) a year are
  disregarded**, and 연금저축 (within that ₩6,000,000) plus 퇴직연금계좌 contributions above
  **₩9,000,000 (900만원) a year** are disregarded [S10 제59조의3제1항 단서].
- 제59조의3제3항 and 제4항 add ISA-conversion amounts to the base, capped at the lesser of
  10% of the converted amount and **₩3,000,000 (300만원)** [S10].
- The rates commonly quoted in the Korean market — **13.2% and 16.5%** — are the statutory
  12% and 15% **grossed up by the 10% 지방소득세 surtax**. The surtax is imposed by the
  지방세법, which was **not retrieved**, so the 13.2/16.5 figures are recorded as
  **[unverified]** arithmetic on a verified base.
- 시행령 제40조의2제2항제1호 caps total contributions at **₩18,000,000 (1,800만원) a year**
  across all 연금계좌 (with a separate cumulative ₩100,000,000 head-room for the 연금주택 and
  연금부동산 downsizing routes added in 2025), and bars contributions once 연금수령 has begun
  [S11]. For an insurance-form account, arrears may be paid up to **three years and two
  months** after the last payment [S11].
- 시행령 제40조의2제3항 defines **연금수령**: the account holder must be **55 or over** and
  have applied to begin drawing; the account must have been open **five years or more**
  (waived where deferred retirement income is in it); and withdrawals must be within the
  **연금수령한도** (the formula is an image and did not extract, but 제4항 states that the
  연금수령연차 runs from the first year in which drawing was possible and that **from year
  11 the limit does not apply**) [S11].
- Taxation on the way out: 소득세법 제20조의3제1항제2호 makes withdrawals in 연금 form from a
  연금계좌 **연금소득**, covering (가) untaxed retirement income, (나) **amounts on which the
  제59조의3 credit was taken**, and (다) investment growth [S10]. 제129조제1항제5의2호 sets
  the withholding rate by the pensioner's age, and **다목 sets 3% for a 종신계약** — a
  lifetime-payment contract [S10]. **The age-band table in 가목 is an image and did not
  extract**; the commonly quoted 5% / 4% / 3% by age band is therefore **[unverified]** here.
  What is verified is that a **lifetime annuity attracts the lowest band, 3%**, which is a
  real product-design incentive for `Pension_KR_S` and `Immediate_KR_S`.

**Protection premiums — 보장성보험료 세액공제** [S10]:

- 소득세법 제59조의4제1항: an employee who pays premiums on a contract "만기에 환급되는
  금액이 납입보험료를 초과하지 아니하는 보험" gets a credit of **12%** of the premium — **15%**
  for a 장애인전용보장성보험 — with each basket capped at **₩1,000,000 (100만원) a year**.
- Note the definition of a qualifying 보장성보험 is *maturity value ≤ premiums paid*, which is
  the same economic test 감독규정 제1-2조제3호 uses to define 보장성보험 at the 기준연령 요건
  [S3]. The two definitions are consistent, which is why Korean products are designed to sit
  cleanly on one side of the line.
- The 12% credit on up to ₩1,000,000 is worth at most **₩120,000 a year** before the local
  surtax; grossed up at 13.2% it is ₩132,000 **[unverified]** as above.

**Savings products — 저축성보험 이자소득 비과세** [S10] [S11]:

- 소득세법 제16조제1항제9호 makes the **보험차익** of a 저축성보험 interest income, **except**
  (가) a policy meeting the Decree's conditions and held **10 years or more** from first
  premium to maturity or surrender, and (나) a **종신형 연금보험** meeting the Decree's
  conditions.
- 시행령 제25조제1항 defines 보험차익 as benefits or refunds received (excluding those paid for
  death, disease, injury or loss of property) **less premiums paid**.
- 시행령 제25조제3항, the 10-year route, sets **two alternative** condition sets:
  1. a 저축성보험 where the **aggregate premiums payable per policyholder across all such
     policies** do not exceed **₩100,000,000 (1억원)** for contracts made from 2017-04-01
     (₩200,000,000 for contracts to 2017-03-31) — but **not** where the premiums are drawn
     down as a fixed-term annuity beginning before the tenth anniversary;
  2. a **월적립식** policy meeting all three of: payment term **5 years or more** from first
     premium; **level basic premium** monthly (an increase up to 1× the original is allowed)
     with advance payment of no more than 6 months; and **aggregate monthly premiums per
     policyholder across all 월적립식 policies of ₩1,500,000 (150만원) or less** (for
     contracts made from 2017-04-01).
- 시행령 제25조제4항, the **종신형 연금보험** route, sets five conditions [S11]:
  1. annuity paid **from age 55 after the payment term ends until death**;
  2. **no payment in any form other than an annuity**;
  3. the contract and the annuity fund must **extinguish on death** — where a guarantee
     period is set it must be **within the sex- and age-specific 기대여명 연수** published by
     the 국가데이터처 (rounded down), and where the annuitant dies within the guarantee period
     the contract extinguishes at the end of it;
  4. **policyholder, insured and beneficiary must be the same person**, and the contract may
     not be surrendered after the first annuity payment and before death;
  5. the annual annuity must not exceed a stated formula (the formula is an image and did not
     extract).
- 시행령 제25조제6항 resets the "first premium date" on three changes: a change of
  policyholder other than by death; conversion of a 보장성 policy to a 저축성 one; and an
  increase of the basic premium beyond 1× the original [S11].
- 시행령 제25조제9항 and 제10항 (신설 2025-06-30) are new and directly relevant to a Korean
  whole-life product's late-life options: where a 보장성보험's sum insured is reduced by
  agreement and the released amount is drawn as an annuity, that is **treated as conversion
  to a 저축성보험**, with the first annuity date as the new first-premium date — **unless**
  the original 보장성보험 was a 월적립식 policy with a sum insured of **₩900,000,000 (9억원)
  or less**, premiums were fully paid before the first annuity date, policyholder, insured and
  beneficiary are the same, and the annuity starts at **55 or later**, in which case the
  original first-premium date is preserved [S11].

  That last provision is the tax basis of the Korean "**연금전환**" feature that many
  종신보험 carry, and `WholeLife_KR_S`'s product spec should record it.

**Death benefits — 상속세 및 증여세법** [S12]:

- 제8조제1항: "피상속인의 사망으로 인하여 받는 생명보험 또는 손해보험의 보험금으로서
  **피상속인이 보험계약자인 보험계약에 의하여 받는 것은 상속재산으로 본다**."
- 제8조제2항: where the policyholder is someone else but **the deceased in substance paid the
  premiums**, the deceased is treated as the policyholder and 제1항 applies.
- 제34조제1항: where the beneficiary and the premium payer differ, the benefit attributable to
  the premiums paid by the other person is a **gift** to the beneficiary; and where the
  beneficiary paid premiums out of property received as a gift, the gift is the benefit less
  those premiums. 제34조제2항 disapplies 제34조 where 제8조 already treats the benefit as
  estate property.
- The practical Korean planning point — that a policy taken out and paid for by the
  *beneficiary* on the life of a parent falls outside 제8조 — follows from 제8조제2항 read with
  제34조, and is why Korean 종신보험 is sold as an inheritance-tax vehicle. No numeric
  threshold or rate is asserted here; the 상속세 rate schedule was not extracted.

### 29. 예금자보호 — the guarantee behind a Korean policy

- 표준약관 제43조: "회사가 파산 등으로 인하여 보험금 등을 지급하지 못할 경우에는 **예금자
  보호법**에서 정하는 바에 따라 그 지급을 보장합니다" [S8].
- **예금자보호법 시행령 제18조제7항, as amended 2025-07-29 and in force 2025-09-01**: "법
  제32조제2항에 따른 보험금의 지급한도는 **1억원**(이하 '보험금 지급한도'라 한다)으로 한다"
  [S14]. **The limit is ₩100,000,000, not ₩50,000,000.** The ₩50,000,000 figure survives only
  in the 부칙 of an earlier amendment [S14] and in pre-2025 consumer material. The FSC
  publicised the change on the commencement date [R6].
- The article then applies the limit **separately to four buckets** [S14 제18조제7항제1호]:
  - 가. DC and IRP-type retirement-pension claims, **per member**;
  - 나. the combined total of **연금저축계좌** claims (소득세법 시행령 제40조의2제1항제1호가목
    and 다목) and legacy 개인연금저축 / 연금저축 claims against a trustee or an insurer;
  - 다. **claims against an insurer that are 보험금** — expressly **excluding benefits payable
    because the policy term has ended** ("보험기간이 종료되어 지급되는 보험금은 제외");
  - 라. everything else.
  ISA claims are combined with bucket 라, per account holder [S14 제18조제7항제2호].
- Two consequences for `krlib`: a `Pension_KR_S` policyholder's protection is in bucket 나 and
  is **separate** from the ₩100,000,000 covering their other insurance claims; and a maturity
  benefit is expressly outside bucket 다, so a maturing 저축성 contract falls into bucket 라
  with the depositor's other claims. Neither point is modelled, both are worth a line in the
  product specs.

### 30. 국민건강보험 — the public layer under 실손

- 국민건강보험법 제41조제1항 lists the seven 요양급여: 진찰·검사, 약제·치료재료의 지급,
  처치·수술 및 그 밖의 치료, 예방·재활, 입원, 간호, 이송 [S15].
- 제41조제2항, added 2016, defines the scope: for everything but drugs, 요양급여 covers
  "제4항에 따라 보건복지부장관이 **비급여대상**으로 정한 것을 제외한 일체의 것" — a negative
  list; drugs are on a positive list [S15]. 제41조제4항 lets the Minister designate as 비급여
  "업무나 일상생활에 지장이 없는 질환에 대한 치료 등" [S15]. **비급여 is therefore a residual
  defined by ministerial designation, and it is the residual that 실손 pays.**
- 제42조제1항 lists the 요양기관 classes — 의료법 institutions, pharmacies, the 한국희귀·필수
  의약품센터, 보건소·보건의료원·보건지소, and 보건진료소 — which are exactly the classes the
  실손 표준약관 keys its outpatient deductible table to [S15] [S8].
- 제44조제1항 imposes the 본인일부부담금 and lets it be raised for **선별급여**; 제44조제2항
  creates the **본인부담상한제**, under which the NHIS refunds the excess of a member's
  annual 본인일부부담금 over an income-graded 본인부담상한액 [S15]. The 실손 표준약관
  expressly makes the 본인부담상한제 refund reduce the insured loss: cover is limited to
  "실제 본인이 부담한 금액 (관련 법령에서 사전 또는 사후 환급이 가능한 금액은 제외한 금액)"
  [S8 제5조제3항]. The per-band 본인부담상한액 amounts sit in 시행령 별표, which was **not
  retrieved**.
- **The 2024 coverage picture** [R12]:

  | | 2023 | 2024 |
  |---|---|---|
  | 건강보험 보장률 | 64.9% | **64.9%** |
  | 법정 본인부담률 | 19.9% | **19.3%** (−0.6%p) |
  | 비급여 본인부담률 | 15.2% | **15.8%** (+0.6%p) |

  with 보장률 defined as 보험자부담금 ÷ (보험자부담금 + 법정본인부담금 + 비급여진료비),
  excluding cosmetic, health-promotion and preventive 비급여 [R12].
- **Total treatment cost 2024: ₩138.6조**, of which **₩90.0조 보험자부담금, ₩26.8조 법정
  본인부담금 and ₩21.8조 비급여진료비** [R12]. The series since 2017 (조 원):

  | Year | 보험자부담금 | 법정본인부담금 | 비급여 | 총 진료비 |
  |---|---|---|---|---|
  | 2017 | 52.5 | 16.9 | 14.3 | 83.7 |
  | 2019 | 66.3 | 20.3 | 16.6 | 103.3 |
  | 2021 | 71.6 | 22.1 | 17.3 | 111.1 |
  | 2022 | 79.2 | 23.7 | 17.6 | 120.6 |
  | 2023 | 86.3 | 26.5 | 20.2 | 133.0 |
  | 2024 | **90.0** | **26.8** | **21.8** | **138.6** |

- 보장률 by institution class 2024: 상급종합 **72.2%** (+1.4%p), 종합병원 **66.7%** (+0.6%p),
  병원 **51.1%** (+0.9%p), 요양병원 **67.3%** (−1.5%p), 의원 **57.5%**, 약국 **69.1%**; by
  age, 5세 이하 **70.4%**, 65세 이상 **69.8%**; 4대 중증질환 **81.0%** [R12].
- Cross-check worth making: private 실손 claims of **₩15.2조** in 2024 [R2] against
  NHIS-measured 비급여 of **₩21.8조** and 법정본인부담금 of **₩26.8조** [R12] — i.e. private
  indemnity insurance reimburses roughly **31%** of the combined ₩48.6조 the patient
  nominally bears. That ratio is the cleanest one-line justification for calling 실손 the
  second health insurance, and it is computed here from two retrieved primary sources.

### 31. 노인장기요양보험 — the statutory trigger for LTC

- **노인장기요양보험법 제2조제1호** defines "노인등" as a person **65 or over**, or under 65
  with a **노인성 질병** the Decree lists (dementia, cerebrovascular disease and others, at
  시행령 별표 1) [S16] [S17 제2조].
- **제2조제2호** defines 장기요양급여 as services or cash "제15조제2항에 따라 **6개월 이상
  동안 혼자서 일상생활을 수행하기 어렵다고 인정되는 자**에게 신체활동·가사활동의 지원 또는
  간병 등" [S16]. The **six-month** duration test is statutory, and it is the natural
  definition of the disability inception a three-state LTC model needs.
- **제15조제2항**: the 등급판정위원회 recognises a claimant meeting the 제12조 eligibility
  and the six-month test "심신상태 및 장기요양이 필요한 정도 등 대통령령으로 정하는
  등급판정기준에 따라" [S16].
- **시행령 제7조제1항 — the grades, verbatim** [S17]:
  > 1. 장기요양 **1등급**: 심신의 기능상태 장애로 일상생활에서 **전적으로** 다른 사람의 도움이
  >    필요한 자로서 **장기요양인정 점수가 95점 이상**인 자
  > 2. 장기요양 **2등급**: … **상당 부분** 다른 사람의 도움이 필요한 자로서 **75점 이상 95점
  >    미만**
  > 3. 장기요양 **3등급**: … **부분적으로** … **60점 이상 75점 미만**
  > 4. 장기요양 **4등급**: … **일정부분** … **51점 이상 60점 미만**
  > 5. 장기요양 **5등급**: **치매**(제2조에 따른 노인성 질병에 해당하는 치매로 한정한다)환자
  >    로서 **45점 이상 51점 미만**
  > 6. 장기요양 **인지지원등급**: 치매(같은 한정)환자로서 **45점 미만**

  제7조제2항 sends the 장기요양인정 점수 itself to a 보건복지부 고시 measuring functional
  decline [S17]. That 고시 was **not retrieved**.
- **제23조** lists the benefit types: 재가급여 (방문요양, 방문목욕, 방문간호, 주·야간보호,
  단기보호, 기타재가급여), **시설급여**, and **특별현금급여** (가족요양비, 특례요양비,
  요양병원간병비) [S16]. **제39조** has the Minister set the 급여비용 annually by benefit
  type and grade after 장기요양위원회 review [S16]. **제40조** imposes a 본인부담금, waived
  for 의료급여 제3조제1항제1호 recipients, with reductions of up to **60%** for listed
  low-income groups [S16].
- **The population the grades describe**, from the NHIS's own disclosure at **2026-06-30**
  [R13]:

  | | Persons | Share of all assessed |
  |---|---|---|
  | 총 등급판정 | 1,411,466 | 100% |
  | **인정자** | **1,275,370** | **90.4%** |
  | 등급외자 | 136,096 | 9.6% |
  | 1등급 | 53,844 | 3.8% |
  | 2등급 | 100,844 | 7.1% |
  | 3등급 | 333,143 | 23.6% |
  | 4등급 | 604,307 | 42.8% |
  | 5등급 | 151,681 | 10.7% |
  | 인지지원등급 | 31,551 | 2.2% |

  Note the shares are of *all assessed*, not of recognised claimants; on the recognised base
  the 4등급 share is about 47%.
- Corroborating annual figures, **[unverified]** because only a search summary of the 2024
  통계연보 was obtained and the article page was not opened [R24]: 인정자 **1,165천명**
  (+6.1% on 2023), 신청자 **1,478천명** (+3.4%), 인정률 **89.5%**, 급여비용 **₩16조1,762억**
  (+11.6%), 공단부담률 **91.3%**. The grade distribution quoted there (4등급 46.0%, 3등급
  26.7%, 5등급 11.6%, 2등급 8.5%, 1등급 4.8%, 인지지원 2.4%) is consistent with the retrieved
  R13 table, which is the reason the unverified figures are recorded at all.
- **Modelling consequence for `LTC_KR_S`.** The benefit trigger is a *public* administrative
  determination, not a policy definition: the model's inception rate is the rate of being
  recognised at or above a stated 등급, and the natural policy design is "1–2등급" (severe)
  or "1–5등급" (broad). Because the 등급별 인정자 stock is public but the **incidence** is
  not, an incidence basis must be constructed `[std]` from the stock and the population, and
  the construction must be shown. The private product cannot define its own trigger without
  abandoning the statutory language, which no Korean carrier does.

### 32. 국가암등록통계 — the incidence basis for cancer and CI

All from the 2023 registry release, dated **2026-01-20** [R11].

- **Incidence 2023**: **288,613** new cancers — 남 151,126, 여 137,487. 조발생률 564.3 per
  100,000 (남 593.4, 여 535.5); **연령표준화발생률 522.9** (남 587.0, 여 488.9), standardised
  on the 2020 주민등록연앙인구. Excluding thyroid cancer: 253,173 cases, 표준화발생률 454.0.
- Series (발생자수 / 연령표준화발생률): 1999 101,854 / 402.7; 2010 222,664 / 565.1; 2019
  258,629 / 518.0; 2020 251,329 / 489.5; 2021 280,042 / 531.4; 2022 281,317 / 521.3; **2023
  288,613 / 522.9**.
- **Top ten, both sexes, 2023** (cases, share, 표준화발생률): 갑상선 35,440 / 12.3% / 68.9;
  폐 32,953 / 11.4% / 57.5; 대장 32,610 / 11.3% / 58.7; 유방 29,871 / 10.3% / 56.8; 위 28,943
  / 10.0% / 51.4; 전립선 22,640 / 7.8% / 39.2; 간 14,707 / 5.1% / 26.1; 췌장 9,748 / 3.4% /
  17.1; 담낭 및 기타담도 7,997 / 2.8% / 13.8; 신장 7,367 / 2.6% / 13.5.
- **Male top five**: 전립선 22,640 (15.0%), 폐 21,846 (14.5%), 위 19,295 (12.8%), 대장 19,156
  (12.7%), 간 10,875 (7.2%). **Female top five**: 유방 29,715 (21.6%), 갑상선 26,114 (19.0%),
  대장 13,454 (9.8%), 폐 11,107 (8.1%), 위 9,648 (7.0%).
- **Lifetime risk of developing cancer (평생 암발생 위험도), 2023**: **all cancers 41.2%
  overall — 남 44.6%, 여 38.2%**; lifetime risk of dying of cancer 19.6% (남 24.2%, 여
  15.6%). By site (전체 / 남 / 여): 폐 6.4 / 8.8 / 4.2; 대장 5.7 / 6.4 / 5.1; 위 5.0 / 6.5 /
  3.6; **갑상선 4.7 / 2.4 / 6.9**; 전립선 4.3 / 8.6 / –; 유방 4.0 / 0.1 / 7.9; 간 2.7 / 3.8 /
  1.6; 췌장 2.0 / 1.9 / 2.0.
- **Five-year relative survival, 2019–2023 diagnoses**: all cancers **73.7%** (남 68.2, 여
  79.4); excluding thyroid **69.6%** (남 65.9, 여 74.0). By site: 갑상선 **100.2%**, 전립선
  96.9%, 유방 94.7%, 위 78.6%, 대장 75.6%, 폐 42.5%, 간 40.4%, 담낭 및 기타담도 29.0%, 췌장
  17.0%, 신장 87.9%. The 1993–95 comparison for all cancers was 42.9%.
- **Prevalence at 2024-01-01** (persons diagnosed 1999–2023 and alive): **2,732,906**, being
  **5.3% of the population** — 남 1,193,944 (4.7%), 여 1,538,962 (6.0%); 조유병률 5,343.4 per
  100,000. Excluding thyroid: 2,145,614 (4.2%). Leading sites: 갑상선 587,292 (21.5%), 위
  366,717 (13.4%), 유방 354,699 (13.0%), 대장 340,064 (12.4%), 전립선 161,768 (5.9%).
- **Why thyroid cancer matters to `krlib`.** 갑상선암 is the single most common cancer in
  Korea (12.3% of all cases; 19.0% of female cases) and has a five-year relative survival of
  **100.2%** — statistically indistinguishable from the general population. Korean cancer
  policies therefore place it, with carcinoma in situ and certain skin and borderline
  tumours, in a reduced **유사암** tier paying a small fraction of the 진단급여금. Any
  `Cancer_KR_S` incidence table that does not separate 갑상선 from the rest will misprice the
  product by a wide margin. The registry gives the split; the tier definition comes from each
  carrier's 약관 and belongs in the `cancer` research file.

---

## Market overview

This section is written to be the source of the library index's market paragraphs. Every
figure carries its as-of date and its source.

**Size, 2025 actual.** Total 수입보험료 for all Korean insurers in 2025 was **₩266.6595조**,
up 11.1% (₩26.6776조) on 2024 — 생명보험사 **₩127.5061조** (+12.4%) and 손해보험사
**₩139.1533조** (+10.0%) [R16]. Net income was **₩12.2172조**, down 14.5%: 생보 ₩4.9680조
(−11.8%), 손보 ₩7.2492조 (−16.2%). ROA 0.94% (−0.21%p), ROE 7.86% (−1.35%p). Total assets
**₩1,344.2조** (+5.9%), total liabilities ₩1,175.6조 (+4.3%), equity ₩168.5조 (+18.5%). The
FSS attributed the profit fall to "손실계약 증가, 예실차 손실 등 보험손익 악화". These
figures come from a **trade newspaper reporting an FSS release**; the FSS site itself did not
respond [R28], so they are news-sourced.

**Life mix, 2025 actual** (수입보험료, 조원) [R16]:

| Line | 2025 | Change |
|---|---|---|
| 보장성보험 | **62.0192** | +12.7% |
| 저축성보험 | 27.4763 | −4.6% |
| 퇴직연금 및 기타 | 25.3979 | +46.4% |
| 변액보험 | 12.6128 | +2.8% |

**Non-life mix, 2025 actual** (수입보험료, 조원) [R16]:

| Line | 2025 | Change |
|---|---|---|
| **장기보험** | **73.3402** | +7.0% |
| 퇴직연금 및 기타 | 29.7187 | +33.3% |
| 자동차보험 | 20.3681 | −1.7% |
| 일반보험 | 15.7264 | +5.0% |

**The single most important structural fact in those two tables.** Korean *personal
protection* insurance is written on **both** sides of the market: 생명보험 보장성보험 at
₩62.0조 and 손해보험 장기보험 at ₩73.3조 — and the non-life figure is the **larger** of the
two. 장기손해보험 is overwhelmingly 장기인보험 (long-term personal cover: health, cancer,
care, accident), written under the 제3보험 deeming provision of 보험업법 제4조제3항 [S1] and
reserved under the same rules by 감독규정 제7-69조 [S3]. A Korea library that looked only at
life insurers would miss more than half of the protection market. `krlib` models the
life-insurer form throughout, and each product document says where a non-life carrier's
version differs.

**Forecast, 2026** (보험연구원, 2025-10-21) [R15]:

| 생명보험 (조원, %) | 2023 | 2024 | 2025(E) | 2026(E) |
|---|---|---|---|---|
| 전체 | 112.4 (−15.3) | 113.4 (+0.9) | 124.0 (+9.3) | **125.3 (+1.0)** |
| 보장성보험 | 48.6 (+3.2) | 55.0 (+13.1) | 61.5 (+11.8) | **66.2 (+7.6)** |
| 저축성보험 | 28.1 (−38.0) | 28.8 (+2.7) | 27.4 (−4.9) | **26.1 (−4.8)** |
| 변액보험 | 12.2 (−4.0) | 12.3 (+0.4) | 12.7 (+3.3) | **12.4 (−2.3)** |
| 퇴직연금 | 23.5 (−14.7) | 17.3 (−26.2) | 22.4 (+29.1) | **20.6 (−7.8)** |
| 퇴직연금 제외 | 88.9 (−15.4) | 96.1 (+8.1) | 101.6 (+5.7) | **104.7 (+3.0)** |

| 손해보험 (조원, %) | 2023 | 2024 | 2025(E) | 2026(E) |
|---|---|---|---|---|
| 전체 | 125.2 (+4.2) | 127.6 (+1.9) | 135.0 (+5.8) | **139.6 (+3.5)** |
| 장기손해보험 | 64.3 (+4.0) | 68.0 (+5.8) | 72.3 (+6.3) | **75.9 (+4.9)** |
| 개인연금 | 1.9 (−10.7) | 1.7 (−13.0) | 1.4 (−15.5) | **1.2 (−15.0)** |
| 자동차보험 | 21.1 (+1.4) | 20.7 (−1.8) | 20.3 (−2.0) | **20.3 (−0.2)** |
| 일반손해보험 | 13.9 (+8.6) | 14.9 (+7.4) | 15.6 (+4.9) | **16.5 (+5.9)** |
| 퇴직연금 | 24.0 (+6.6) | 22.3 (−7.2) | 25.3 (+13.5) | **25.7 (+1.7)** |

보험연구원's summary is that industry premium growth falls to about **2.3% in 2026** from
7.4% in 2025, with 생명보험 at **1.0%** and 손해보험 원수보험료 at **3.5%**, on a base of
roughly ₩265조, and that "성장성 둔화, 수익성 약화, 건전성 악화" is the sequence from 2024
through 2026 [R15].

**보장성 versus 저축성.** On the 2026 forecast, 보장성 is **52.8%** of life premium (₩66.2조
of ₩125.3조) against 저축성 at **20.8%** — and the two are moving apart at roughly 12
percentage points a year of relative growth. 개인연금 written by non-life insurers is in
outright run-off, forecast to fall 15% a year to ₩1.2조 [R15]. The Korean life market is a
protection market with a shrinking savings tail, which is the opposite of the French and
German mixes in `frlib` and `delib`.

**실손 penetration.** **35.96 million** individual policies in force at 2024 year-end against
a population near 51 million, with ₩16.3조 of premium and ₩15.2조 of claims [R2]. Two-thirds
of the population is a reasonable statement of coverage and is consistent with the FSS's own
"제2의 건강보험" framing.

**Solvency.** K-ICS ratio after transitional measures at **2025-09-30: all insurers 210.8%,
생보 201.4%, 손보 224.1%** [R3]; at 2024-06-30 the industry figure was 217.3% [R1]. The
regulatory minimum is **100%** [S2 제65조제2항제1호]; 경영개선권고 begins below it [S3
제7-17조].

**Rate levels.** 평균공시이율 for 2026 is **2.50%**, down from 2.75% for 2024 and 2025 [R17]
— the first fall since 2020 and the level to which every 저축성 design test, the 부활
interest ceiling and the 변액 보증준비금 roll-forward are pegged. Carrier 공시이율 levels sit
close to it: one retrieved carrier grid shows a 공시기준이율 of 3.19% across five product
classes but with an unknown as-of month [R18], and trade reporting places 보장성 공시이율 at
2.2%, 연금 at 2.29% and 저축 at 2.22% shortly before the 2026 cut [R25] — **[unverified]**.
**예정이율 is not published for any product** (§15).

**Interest-rate backdrop.** Ten-year government bond yields quoted by the FSS: 3.74% at 2022
year-end, 3.18% at 2023 year-end, 3.40% (2024-03), 3.26% (2024-06), **2.99% (2024-09)** [R1].
The IFRS 17 long-term forward rate is **4.55%** and the liquidity premium **91bp** [R1].

**Product-mix signal for `krlib`.** Two-thirds of new protection business by first-year
premium is 무·저해지 [R1]; the market's protection growth is in 보장성 (+7.6% forecast for
2026) while 저축성 shrinks [R15]; 실손 is nearly saturated and is being restructured by
regulation rather than by competition [R2] [R7]; and 개인연금 is in run-off on the non-life
side while 퇴직연금 grows. A representative Korean product set is therefore weighted to
protection and to third-sector health, which is what the `krlib` ten are.

---
### 33. What this forces on the `krlib` models

Collected here so that each product document can cite one place rather than re-deriving
the argument.

1. **Every `mort_table.csv` is `[std]`.** The industry table is not published (§25). The
   construction anchors on 국가데이터처 생명표 (§26) with an insured-lives adjustment
   bracketed by the two published 경험생명표 summary statistics, and every row carries a
   `provenance` column.
2. **Every morbidity, incidence and disability rate is `[std]`.** 참조순보험요율 are not
   published (§27); only a ratio derived from them (보험가격지수) reaches the public.
   Cancer incidence is built from the registry (§32), long-term-care inception from the
   grade statistics (§31), and medical utilisation from the NHIS coverage survey (§30).
3. **Every 예정이율 is `[std]`,** anchored on the 평균공시이율 series (§14), because the
   산출방법서 is not public (§4) and the term does not appear in the regulation (§15).
4. **Every 사업비 assumption is `[std]`,** bounded above by the 표준해약공제액 (§16) and by
   the 1.4× 계약체결비용 tolerance of 감독규정 제7-45조제11항.
5. **Surrender values are computed, not assumed.** The 별표 14 formula is public and
   binding, so `cv_pp` in every model is `max(0, 계약자적립액 − 표준해약공제액)` during the
   해약공제기간 (payment period capped at seven years), with the 무해지/저해지 variant
   suppressing it during the payment period and stepping up at 납입완료 subject to the two
   tests of 제7-66조제4항제2호 (§18).
6. **The lapse assumption on a 무해지 form is not free.** A log-linear decay to 0.1% at
   납입완료, with 0.8% thereafter, is the supervisory principle model (§18); a `krlib`
   model should implement it and carry the 표준형 alternative as a switch.
7. **Ages are 보험나이 for pricing and 만나이 for statistics,** and the difference is real
   for half of all issue dates (§24). Every model's registry metadata must say which.
8. **The reference cell is 기준연령 요건** — male, exact age 40, monthly premium, whole-term
   pay (§17) — so model point 1 should be that cell wherever the product admits it.
9. **A 제3보험 model must pay something on non-covered death** — the 계약자적립액 plus
   미경과보험료 — because 감독규정 제7-63조제1항제1호 requires the design (§19), and the
   표준약관 제22조 implements it (§24).
10. **Nothing in `krlib` computes 책임준비금, 해약환급금준비금, 보증준비금 or K-ICS
    요구자본.** They are cited (§6, §7, §9) so that a reader knows what the projection is
    *not*, and so that the products' technical notes can say where a real filing would
    diverge from the reference implementation.

---

## Variation across carriers

This is a cross-product file, so the variation recorded here is variation in the
*parameters the regulation leaves open*, not in benefit menus — those belong in the ten
product research files. Where a range could be bracketed from a retrieved source it is
given; where it could not, that is said.

| Parameter | What the regulation fixes | Observed range or level | Source |
|---|---|---|---|
| 지급여력비율 (K-ICS) | floor 100% | industry 210.8%, 생보 201.4%, 손보 224.1% at 2025-09-30; industry 217.3% at 2024-06-30 | [S2] [R3] [R1] |
| 평균공시이율 | FSS-set, one value for all insurers | 3.50% (2016) → 2.25% (2021–23) → 2.75% (2024–25) → **2.50% (2026)** | [R17] |
| 공시기준이율 | formula fixed by 별표 27; α ≤ 60%, weights to 0.5%p | one carrier's grid at **3.19%** across five classes, as-of month unknown | [S7] [R18] |
| 공시이율 | = 공시기준이율 × 조정률; uniform within a product class | 보장성 2.2%, 연금 2.29%, 저축 2.22% shortly before the 2026 cut — **[unverified]** | [S3] [R25] |
| 최저보증이율 | mandatory for 금리연동형; level free | **no level retrieved from any carrier** | [S3] |
| 예정이율 | not a regulatory term; in the non-public 산출방법서 | **not published by any carrier** | [S3] |
| 표준해약공제액 | fully specified by 별표 14 | identical for all carriers by construction | [S4] |
| 계약체결비용 vs 표준해약공제액 | index disclosure required above 1×, waived to 1.4× for whole-life death cover | actual loadings not public | [S3] |
| 무·저해지 환급률 | must not exceed 표준형 over the whole term | FSC's illustrative pair: 표준형 97.3% vs 무해지 134.1% at 20 years, pre-reform | [S3] [R5] |
| 무·저해지 share of new business | none | 11.4% (2018) → 30.4% (2021) → 47.0% (2023) → **63.8% (2024 H1)** | [R1] |
| 무·저해지 lapse assumption | log-linear principle model, 0.1% at 완납 | two alternative models permitted, with mandatory disclosure of the CSM / BEL / K-ICS / net-income difference | [R1] |
| 단기납 종신 bonus-date extra lapse | ≥30% | industry 11th-year bancassurance benchmark 29.4%–30.2% | [R1] |
| Loss ratio by age | must be split where significant | 상해수술 industry: 30s 89%, 40s 103%, 50s 140%, 60s 186% | [R1] |
| 실손 annual rate change | ±25% per risk cell | 4세대 premium flat at ₩15,000/month 2021–2024 while 3세대 rose ₩16,000 → ₩24,000 | [S3] [R2] |
| 실손 비급여 요율 상대도 | five bands, 100/200/300/400% plus a balancing discount | fixed by the 표준약관; the discount is solved each year to be revenue-neutral | [S8] |
| 실손 손해율 | none | 생보사 86.5%, 손보사 102.0% (2024); by generation 97.7 / 92.5 / 128.5 / 111.9% | [R2] |
| 부활 interest | ≤ 평균공시이율 + 1% | company-set within the cap; 금리연동형 set in the 사업방법서 | [S8] |
| 보험계약대출 | permitted within the surrender value | "순수보장성보험 등" may be excluded entirely — so a 무해지 protection product may offer none | [S8] |
| 청약철회 | 15 days from 보험증권 / 30 from application | a longer period may be agreed (금소법 제46조제1항) but none was observed | [S13] [S8] |
| 유배당 vs 무배당 | shareholder share of 유배당 profit ≤ 10% | retail protection is overwhelmingly 무배당 across the carriers examined | [S3] |
| K-ICS 경과조치 | four optional 10-year phase-ins | uptake not established this session; the FSC's 적기시정조치 deferral runs to the 2027-12-31 closing | [R14] [S3] |

**What does not vary.** The surrender-charge cap, the 해약공제기간 of at most seven years,
the 보험나이 six-month rule, the 15/30-day cooling-off, the three-month 품질보증해지, the
2-year/3-year/1-month non-disclosure time bars, the three-year 부활 window, the three-year
소멸시효, the mandatory 최저보증이율 on interest-sensitive business, the mandatory
최저사망보험금 on 변액보험, the ±25% 실손 corridor and the five-band 실손 experience-rating
table are all fixed by regulation or by the 표준약관 and are therefore **identical across
every Korean carrier**. That is a much larger fixed core than in any other market in this
repository, and it is the reason a Korean reference implementation can be more faithful to
"the market" than, say, a US or UK one: most of what a Korean product does is prescribed.

**Representative choices for the reference implementation**, justified against the above:

- **예정이율**: anchor on the 평균공시이율 of the modelled issue year, i.e. **2.50%** for a
  2026 issue, tagged `[std]` with the §14 series as its rationale. This is deliberately
  not an insurer's real 예정이율, which is not knowable.
- **공시이율**: use the same 2.50% with a **최저보증이율** floor set `[std]` below it, and
  say that the level is a company choice the regulation does not fix.
- **표준해약공제액**: compute it exactly from 별표 14 for each product's class and
  coefficient. This is a *computed*, not an assumed, quantity and should be asserted in the
  test suite.
- **사업비**: set 계약체결비용 equal to the 표준해약공제액 (i.e. a ratio of 1.0 against the
  1.4× disclosure tolerance), which is conservative and avoids the 상품요약서 index
  disclosure trigger.
- **해지율**: on 표준형 forms a conventional decaying vector `[std]`; on 무해지/저해지 forms
  the **log-linear principle model to 0.1% at 납입완료 and 0.8% thereafter**, per R1.
- **모델포인트 1**: 기준연령 요건 — male, 보험나이 40, monthly premium, whole-term pay —
  wherever the product admits it.

---

## Fetch failures and gaps

Recorded in full, because what could not be opened determines what this file may assert.

**Hosts and pages that did not serve content**

- **`https://www.fss.or.kr` (금융감독원)** — a plain HTTPS GET returned
  `curl: (52) Empty reply from server`. The site did not respond to the fetcher at any
  path. **Consequence:** every FSS document in this file was obtained through a mirror —
  the KDI 경제교육·정보센터 for the 실손 실적 [R2] and the 지급여력비율 현황 [R3], the
  보험연구원 weekly-trend reprint for the NHIS coverage release [R12] — or through a trade
  newspaper [R16]. The 2025 경영실적 figures in the Market overview are therefore
  **news-sourced**, and no FSS release was read in its original hosting.
- **`https://www.law.go.kr/법령/<name>` and `https://www.law.go.kr/행정규칙/<name>` via a
  summarising fetcher** — returned the page title and navigation chrome only; the
  statutory text is loaded by JavaScript. Every statute and 고시 in this file was retrieved
  instead through the inner endpoints `LSW/lsInfoR.do` and `LSW/admRulLsInfoR.do`. **Cite
  the friendly URL; note the inner endpoint as the retrieval route.** The friendly URL is
  also the route that returns the current `lsiSeq` / `admRulSeq` in a redirect stub, which
  is how the current version of each instrument was identified.
- **`https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=…`** — the outer 행정규칙 page. Same
  failure mode; body served from `admRulLsInfoR.do`.
- **`https://www.law.go.kr/LSW/lsSideInfoP.do?lsiSeq=266041&joNo=0063&…`** — the
  article-level side panel for 보험업법 시행령 제63조. Returned header and navigation only.
  The article was obtained from the full-statute body instead.
- **`https://casenote.kr/법령/보험업법/제120조` and `…/제127조`** — HTTP **503 Service
  Unavailable** on two attempts each, apparently rate limiting. 제4조, 제5조 and 제2조
  succeeded from the same host. Both failing articles were obtained from S1 instead, so
  nothing is lost.
- **`https://bigin.kidi.or.kr:9443/boarddetail/nd00017_6041`** (보험개발원 보험정보
  빅데이터 플랫폼, the page that indexes 경험생명표) — **`connect ECONNREFUSED
  61.107.27.12:9443`**. The host refused the connection outright. This is the single most
  damaging failure in the session: it was the most likely public route to any 경험생명표
  documentation.
- **`https://www.kidi.or.kr/user/nd11592.do`** (보험개발원 보도자료) — retrieved, but the
  visible listing runs only from 2026-06-02 to 2026-08-18 (items 742–746) and contains **no**
  경험생명표, 참조순보험요율 or 보험통계 release. Pagination to the January 2024 range was
  not attempted.
- **`https://www.samsunglife.com/individual/products/disclosure/pension/PDO-PRPRP010100M`**
  (삼성생명 연금저축보험 상품공시) — returned the string "삼성생명" and nothing else; the
  disclosure grid is JavaScript-rendered. No carrier 연금저축 parameters were obtained.
- **`https://www.hanwhalife.com/main/disclosure/goods/disclosurenotice/DF_GDDN000_P10000.do`**
  (한화생명 적용이율) — returned the disclosure-navigation hub, not the rate table. No
  한화생명 공시이율 or 최저보증이율 was obtained.
- **`https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status`** (교보생명
  공시기준이율 적용현황) — the rate grid returned (3.19% across five classes) but **the
  month selector's value did not**, so the as-of date is unknown. The figure is recorded as
  illustrative and is not used as a dated fact [R18].
- **`https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do`** (금융통계월보) —
  the query form returned; the monthly tables themselves are behind it and were not
  retrieved [R21].
- **`https://pub.insure.or.kr/`** (생명보험협회 공시실) — the landing page and category
  structure returned; no product-level 공시 was drilled into, and no 약관 or 상품요약서 PDF
  was downloaded. That is deliberate — product documents belong in the ten product research
  files — but it means this file asserts **no carrier product parameter** from a primary
  product document.

**Documents that returned but could not be read**

- **`…/comm/getFile?srvcId=RULENOTICE&upperNo=3446&fileTy=ATTACH&fileNo=6`** on `fsc.go.kr`
  — downloaded as a 15-page PDF, but it is a **규제영향분석서** for a 2020s amendment about
  보험설계사 모집경력 disclosure, not the 보험업감독규정 itself. Not used.
- **HWP and HWPX attachments** to FSC releases — attachments 2, 3 and 5 to the November
  2024 IFRS 17 package [R1] are Hancom formats and were not converted. The two PDF
  attachments (the 보도자료 and 「보험부채 할인율 현실화 연착륙 방안」) were read in full;
  the 별첨 「IFRS17 주요 계리가정 가이드라인」 itself is among the unconverted files, so the
  guideline's **full text was not read** — everything about it in §18 comes from the
  보도자료's description of it. The same applies to the 한국회계기준원 release's 별첨 on
  K-IFRS 1117 [R23].
- **`https://www.law.go.kr/LSW/flDownload.do?flSeq=3240711`** — a first guess at the 별표 14
  download returned an unrelated HWP (자동차관리사업등록대장). `flSeq` is a global file id,
  not the `bylSeq`; the correct route is `admRulBylContentsInfoR.do?bylSeq=…` → read
  `pdfFlSeq` → `flDownload.do?flSeq=<pdfFlSeq>`. Recorded so the next drafter does not
  repeat it.

**Formulas and tables that are images inside retrieved documents**

Each of these was in a document that was successfully retrieved, but the operative
expression is a picture and did not extract. Every one is a live gap.

- **감독규정 제7-66조제1항제1호** — the display of `해약환급금 = 계약자적립액 − 해약공제액`.
  The operative words extracted; the display did not. Nothing rests on the display.
- **감독규정 제7-66조제1항제4호가목·나목** — the **계약자적립액 accrual formulas**, monthly
  before 납입완료 and daily after. **This is a real gap**: `krlib` must therefore construct
  the accrual `[std]` and say so. The *rule* (monthly then daily) is verified; the formula
  is not.
- **감독규정 제7-2조제1항제1호나목** — the **correlation aggregation formula** for
  기본요구자본. The five risk categories and the seven life sub-risks extracted; the
  aggregation did not. Nothing in `krlib` needs it.
- **시행세칙 별표 27, 제2호다목 and 제3호가목** — the **β weight formulas** (asset-balance
  shares) and the **α formula** (the function of 계약자적립액, duration and premium income).
  The inputs, the rounding and the 60% cap on α extracted; the expressions did not. A
  `krlib` model that needed to *derive* a 공시기준이율 could not; none does, because the
  crediting rate is taken as an input.
- **소득세법 제129조제1항제5의2호가목** — the **연금소득 withholding-rate table by age**. The
  종신계약 rate of 3% (다목) extracted; the age bands did not. The commonly quoted
  5%/4%/3% is **[unverified]**.
- **소득세법 시행령 제25조제4항제5호** — the **annual-annuity ceiling formula** for a
  tax-exempt 종신형 연금보험. The other four conditions extracted in full. `Immediate_KR_S`
  cannot verify a design against the ceiling.
- **소득세법 시행령 제40조의2제3항제3호** — the **연금수령한도 formula**. The 55-and-five
  test and the "no limit from year 11" rule extracted; the formula did not.
- **표준약관 부표 3 장해분류표** — extracted as running text; the percentage grid per
  impairment is present but the tabular structure is lost. Any product using a specific
  장해지급률 must re-read the schedule.

**Documents identified but not retrieved**

- **시행세칙 [별표 22] 지급여력금액 및 지급여력기준금액 산출기준** (bylSeq 3295667) and
  **[별표 22의 1] 내부모형 적용기준** (3295669) — the operative K-ICS standard formula,
  including every shock scenario and every risk factor. Not downloaded. Everything §9 says
  about K-ICS comes from the 감독규정's framing articles, not from the calibration. Any
  statement about a *shock magnitude* would be unverified, and none is made.
- **시행세칙 [별표 14] 표준사업방법서** (3295611) and **[별표 16] 손익분석기준** (3295655)
  — not downloaded.
- **감독규정 [별표 6] 보험상품군별 보험료 산정기준**, **[별표 17] 금융기관보험대리점등을
  통하여 모집하는 보험상품의 기초서류 작성ㆍ변경 원칙** and **[별지 26] 해약환급금준비금
  산출명세서** — identified in the 별표 index, not downloaded. 별지 26 in particular would
  show the exact line items of the 해약환급금준비금 calculation.
- **시행령 별표 6** (보험업법 시행령) — the list of 기초서류 changes requiring pre-filing,
  referenced by 제71조제1항. Not retrieved; §4's account of the filing trigger rests on
  감독규정 제7-51조, which was.
- **국민건강보험법 시행령 별표 2** — the **본인일부부담금 rates** (the familiar 입원 20% and
  외래 30–60% by institution class) and the income-graded **본인부담상한액**. Not retrieved.
  No co-payment rate under the *public* scheme is asserted in this file; the 실손 약관's own
  deductible table, which is retrieved, is used instead.
- **노인장기요양보험법 시행령 별표 1** (노인성 질병 list) and the 보건복지부 고시 defining
  the **장기요양인정 점수** measurement. Not retrieved. The grade thresholds are verified;
  the scoring instrument is not.
- **보건복지부 장기요양급여비용 고시** — the annual 급여비용 by benefit type and grade under
  법 제39조. Not retrieved. `LTC_KR_S` therefore has no verified public benefit-cost scale
  to calibrate a cash benefit against.
- **국민건강보험공단, 「2024 노인장기요양보험 통계연보」** — the primary yearbook. Only a
  search summary was obtained [R24], and the article page carrying it was not opened. The
  annual figures in §31 marked **[unverified]** are the consequence; the grade distribution
  is separately verified from R13.
- **KOSIS 완전생명표 tables** (kosis.kr) — the single-year-of-age qx tables underlying R9 and
  R10. **Not downloaded.** Only the summary statistics in the press releases were read. A
  `krlib` mortality-table build must fetch them and record the KOSIS table id in each
  product's `sources.md`; until it does, the base table is unverified at the qx level.
- **보험연구원, 「2025년 보험산업 주요 이슈: ② IFRS17 및 K-ICS」** [R27] and **「K-ICS
  영향분석과 보험회사 대응방안」** (docId 614689) — identified, not downloaded.
- **금융감독원 지급여력비율 현황 for 2025-03 and 2025-06** [R26] — identified, not opened.
  Only the September 2025 quarter is used.
- **생명보험협회 FACT BOOK 2025 PDF** and **통계연보** — the edition list and contents were
  read [R20]; the documents were not downloaded and nothing is cited from them.
- **금융위원회 계약재매입 실행방안** — promised for the second half of 2025 [R7]. Not
  located. Whether the buy-out is now open, and on what terms, is unknown.

**Facts left unverified, in priority order**

1. **The 경험생명표 qx table** — not public, and no route to it was found (§25). This is not
   a fetch failure that better searching would fix; it is a structural feature of the Korean
   market, and it is why every `krlib` mortality table is `[std]`.
2. **The 제10회 경험생명표 summary figures themselves** (평균수명 86.3 / 90.7, 65세 기대여명
   23.7 / 27.1, application from 2024-04) rest on a **single trade-newspaper article** [R8],
   corroborated only by other news summaries. No KIDI document was opened. Everything in
   §25 built on those four numbers inherits that weakness.
3. **참조순보험요율 values** — not published. No morbidity or incidence rate in `krlib` can be
   traced to the rate bureau.
4. **예정이율 and 최저보증이율 levels at any carrier** — not published (예정이율) or not
   retrieved (최저보증이율). Both are `[std]` in every model.
5. **공시이율 levels by carrier and month** — the one grid retrieved has no as-of date [R18];
   the trade figures (보장성 2.2%, 연금 2.29%, 저축 2.22%) are from an unopened article
   [R25]. Only the FSS-set **평균공시이율** series is verified [R17].
6. **The 13.2% / 16.5% 연금저축 credit rates and the 13.2% 보장성 credit rate** — the
   statutory 12% and 15% are verified [S10]; the gross-up by the 10% 지방소득세 surtax is
   arithmetic on an unretrieved statute (지방세법).
7. **The 연금소득 withholding age bands (5% / 4% / 3%)** — the table is an image (§28). Only
   the 3% for a 종신계약 is verified.
8. **K-ICS shock magnitudes and risk factors** — 별표 22 not retrieved. §9 describes the
   architecture, never a calibration.
9. **Whether 4세대 실손 remains on sale after 2026-05-06** — the 감독규정 amendment and the
   표준약관 revision are verified [S3] [S8], and the FSC's plan for a ten-year 약관 conversion
   window from 2026-07 is verified [R7], but no document was retrieved stating that new
   4세대 sales have ceased. `Medical_KR_S` should model the **5세대** design, which is the
   one now in the 표준약관, and should say that the in-force market is still 43% 2세대 [R2].
10. **K-ICS 경과조치 uptake** — the number of insurers applying, and which of the four items
    each applied, was not established. A search summary referred to 19 insurers seeking a
    deferral; the article was not opened, so that figure is **[unverified]** and is not
    stated in §11.
11. **The IFRS 17 계리가정 guideline text itself** — only the FSC's description of it was
    read (§18). The precise functional form of the log-linear model, and the definition of
    the "실무상 수렴점", come from the 보도자료, not from the guideline.
12. **CSM levels** — the 생보 ₩64.7조 → ₩64.3조 and 손보 ₩70.3조 → ₩71.8조 forecasts in §12
    were read from a search summary of the same seminar whose premium tables were retrieved;
    the CSM slide did not extract. Marked `[unverified]` at the point of use.
13. **상속세 rates and thresholds** — 상증세법 제8조 and 제34조 are verified [S12]; no rate,
    band or deduction is asserted, because the rate schedule was not extracted.
14. **본인부담상한제 amounts** — the mechanism is verified [S15] and the 약관's treatment of
    it is verified [S8]; the income-graded caps are not.
15. **The 3대비급여 sub-limits in 실손 특별약관2** — the existence of a separate 3대비급여
    annual limit and per-item caps is verified [S8], but the specific 도수치료 /
    체외충격파 / 비급여주사 session and amount limits were not extracted cleanly from the
    492-page schedule and are not stated here. They belong in the `indemnity_medical`
    research file, read from the same schedule.

**One methodological caveat, stated because it affects every date in this file.** The
current version of 보험업감독업무시행세칙 served by 국가법령정보센터 takes effect
**2026-09-10**, a week after the 2026-09-03 access date [S6]. Facts drawn from it — 별표 27,
별표 15 표준약관 and 제5-16조 — are facts about the text that will be in force, not
necessarily about the text in force on the access date. Where a 표준약관 clause carries its
own 개정 date (and most do), that date is given, and none of the clauses cited in §24 or §20
was amended by the 2026-08-28 revision so far as the retrieved 부칙 discloses. A drafter
revisiting this file after 2026-09-10 can treat the citations as current without change.
