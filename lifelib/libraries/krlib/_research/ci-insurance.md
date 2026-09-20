# CI보험 / 중대질병보험 (critical illness) — research notes (Korea)

Research compiled 2026-09-03 for the reference-products library (Korea section). Purpose:
source library for a Korean **CI보험** (*CI boheom*, critical illness insurance) liability
cash-flow reference model — `CI_KR_S`, which inherits the `WholeLife_KR_S` savings/protection
chassis and adds an accelerated critical-illness payment.

CI보험 is not a Korean invention and it is not a 진단비 (*jindanbi*, fixed diagnosis-benefit)
product. It is a **whole-life contract with an acceleration clause**: on diagnosis of a
contractually defined 중대한 질병 (*jungdaehan jilbyeong*, "critical" disease), the insurer
pays a stated fraction — conventionally 50% or 80%, latterly 100% — of the death benefit
early, and the death benefit is reduced by the amount paid. Korea imported it from a
reinsurer's product shelf in 2002, sold it in enormous volume for a decade, and then watched
it lose the health-insurance market to the very 진단비 riders it was designed to replace,
largely because of the word 중대한. That word, and the arithmetic it governs, is what this
file is about.

Three structural facts make the Korean version distinct from the UK accelerated CI cover in
`uklib` and from the Japanese 三大疾病 riders in `jplib`:

1. **The disease definitions are the insurer's own, not a market standard.** The UK has the
   ABI Guide to Minimum Standards; Korea has nothing equivalent for CI. What Korea does have
   is a statutory 장해분류표 (disability schedule) sitting inside the 표준약관, and the
   중대한 뇌졸중 definition points at it — so the *severity gate* is standardised even though
   the *disease definition* is not.
2. **There is no survival period.** Overseas CI pricing typically assumes a 30-day survival
   requirement; the Korean supervisor refused it on consumer-protection grounds, so the
   benefit is payable even where the insured dies of the CI event. That refusal is the direct
   reason the *acceleration* form (rather than the standalone form) became the market default
   [R1].
3. **Because it is written on a whole-life chassis it carries a policy reserve, a surrender
   value, a policy loan and a premium waiver** — and, in the modern generation, the Korean
   무해지/저해지환급형 (no- and low-surrender-value) suppression of that surrender value
   during the premium-paying period. A UK CI policy has none of this.

**What this file is.** It is the provenance layer behind `products/ci_insurance/`'s four
documents — `product-spec.md`, `technical-notes.md`, `model.md` and `sources.md` — and behind
the `CI_KR_S` model's parameter files. Every quantitative claim in those documents should be
traceable to a numbered entry here. **The source numbering below is never renumbered**: the
product documents cite against it, so `S3` means the same document forever. Facts are tagged
`[S#]` where they come from a retrieved primary product document, `[R#]` where they come from
a retrieved regulatory, actuarial, judicial or market reference, and `[unverified]` where they
rest on a search snippet or a document that could not be opened. Where a source is a news
article rather than a primary document, the entry says so and the dependent facts inherit that
weakness.

**Retrieval method.** Plain `curl` is blocked for every Korean host tried in this session
(connection reset by peer at the proxy), so everything below was fetched with `WebFetch`.
`WebFetch` renders HTML but returns Korean PDFs as undecodable binary; in every such case the
binary it saved to disk was extracted locally with `pypdf` and read directly. That is how the
long 약관 (policy conditions) were obtained — the 1,207-page ABL생명 booklet at `[S1]` extracts
cleanly, including its 별표 (annexes), which is where the 중대한 질병 definitions live.
Access date for every source: **2026-09-03**.

---

## Primary sources

### S1 — ABL생명, 「(무)우리가족안심CI통합종신보험(보증비용부과형) 1904 약관」

- Publisher: ABL생명보험주식회사 (ABL Life; formerly 알리안츠생명)
- Document: full 약관집 — 가이드편, 주요내용 요약서, 주계약 약관 and 34 특약 약관, 별표
  1–7, 법규 조항 정리, 신체부위 설명도. **1,207 PDF pages**, product form mark `1904`,
  in force from 2019-04-01
- Doc type: 보험약관 (policy conditions, complete)
- URL: https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2019/04/02/20190401_NP_%EC%9A%B0%EB%A6%AC%EA%B0%80%EC%A1%B1%EC%95%88%EC%8B%ACCI%ED%86%B5%ED%95%A9%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EB%B3%B4%EC%A6%9D%EB%B9%84%EC%9A%A9%EB%B6%80%EA%B3%BC%ED%98%95)1904_%EC%95%BD%EA%B4%80.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (7.6 MB PDF; `WebFetch`'s summariser reported it as unreadable binary but
  saved the file, and `pypdf` recovered all 1,207 pages of Korean text cleanly, including the
  annex tables)
- What was read, and what it is good for: **this is the file's anchor document.** It supplies
  the 중대한 질병 definitions verbatim (별표4), the 중대한 수술 definitions (별표5), the
  중대한 화상 및 부식 definition (별표6), the 보험금 지급기준표 with both acceleration
  fractions and the breast-cancer reduction (별표1), the 장해분류표 including the ADLs
  schedule that the 중대한 뇌졸중 definition points at (별표3), the 장기요양상태 definition
  (제6조), the 90-day 중대한 암 보장개시일 and its five-year re-entry rule (제7조, 별표1 주),
  the premium-waiver triggers, and the whole standard contract apparatus — 보험나이,
  자살면책, 계약 전 알릴 의무, 납입최고, 부활, 해지환급금, 공시이율 and 최저보증이율.

### S2 — ABL생명, 「무배당 걱정말아요CI통합종신보험(저해지환급형) 1705 약관」

- Publisher: ABL생명보험주식회사 (the 약관 text still names 알리안츠생명's 공시실 at
  `www.allianzlife.co.kr`, so this is the transition-period edition)
- Document: full 약관집, form mark `1705`, in force from 2017-07-01; **1,339 PDF pages**
- Doc type: 보험약관 (policy conditions, complete)
- URL: https://www.abllife.co.kr/cms/pban/prdtPban/whlPrdt/__icsFiles/afieldfile/2017/07/19/%EC%95%BD%EA%B4%80(20170701)NP_%EA%B1%B1%EC%A0%95%EB%A7%90%EC%95%84%EC%9A%94CI%ED%86%B5%ED%95%A9%EC%A2%85%EC%8B%A0%EB%B3%B4%ED%97%98(%EC%A0%80%ED%95%B4%EC%A7%80%ED%99%98%EA%B8%89%ED%98%95)(20170701).pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (8.9 MB PDF, all pages extracted; `pypdf` warns
  `Advanced encoding /UniKS-UTF16-H not implemented yet` and the extraction reorders some
  characters within a line — Korean words come out with their trailing particles displaced —
  so only passages that read unambiguously are quoted below, and none of the annex definitions
  is quoted from this document)
- What it is good for: the **저해지환급형** (low-surrender-value) variant of the same product
  family, in two forms — `30% 저해지환급형` and `50% 저해지환급형` — with the surrender-value
  rule stated in terms, and a worked benefit illustration at ₩100,000,000 (1억원) on the 80%
  acceleration. It is the direct evidence that the Korean suppressed-surrender-value design
  was applied to CI business before it became universal.

### S3 — KDB생명, 「무배당 베스트유니버셜CI보험 상품요약서」

- Publisher: KDB생명보험주식회사
- Document: 상품요약서 (product summary), 제작일자 2011년 1월; 32 PDF pages
- Doc type: 상품요약서 — the statutory summary that Korean insurers must publish alongside the
  약관, and the only routinely public document that discloses **pricing parameters**
- URL: https://www.kdblife.co.kr/data_pdf/fp/2011/(%EB%AC%B4)%EB%B2%A0%EC%8A%A4%ED%8A%B8%EC%9C%A0%EB%8B%88%EB%B2%84%EC%85%9CCI%EB%B3%B4%ED%97%98_%EC%83%81%ED%92%88%EC%9A%94%EC%95%BD%EC%84%9C20110103.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (493 KB PDF, extracted cleanly)
- What it is good for: **the quantitative core of this file.** It publishes the product's
  예정이율, its 적용이율 and 최저보증이율, its **예정위험률 for 중대한 암, 중대한
  급성심근경색증 and 중대한 뇌졸중 by sex at ages 20/40/60** — a disclosed CI morbidity basis,
  which is not otherwise obtainable in Korea — its 보험료지수, its 보장위험별 연간보험료 split
  between the CI benefit and the two death benefits, four full 해지환급금 illustration tables
  from which the monthly premium can be recovered exactly, its 가입나이 and 가입한도 by
  acceleration form, and a banded high-sum-assured premium discount scale. Its one weakness is
  its vintage: January 2011, when the 최저보증이율 on this product was 4.0% p.a. compounded.

### S4 — 미래에셋생명, 「건강담은 GI종신보험(무)1904 [해지환급금이 적은 유형]」 상품안내장

- Publisher: 미래에셋생명보험주식회사
- Document: 상품안내장 (product brochure), 제작일자 2019년 8월; 16 PDF pages
- Doc type: 상품안내장 / 가입안내 (consumer brochure carrying the published rate card)
- URL: https://pdf.miraeassetlife.com/directDownloadDocFile.do?Ax=579e39c86d37ae718806f12af1f79d27b07b70d1786ca23d5683a184e905d64e524ebd66da8b940f095b0b06a5a35d10bd22f1ec7a0e3ae91036c9d4e123c908f35cad83ff9ac6434f13cc3a6f1c921065c519b83da76d25f8aec171de5e8ce8f55d3f852fd354789608dc6ff0f8b51b
- Accessed: 2026-09-03
- Retrieved: **yes** (791 KB PDF, extracted cleanly)
- What it is good for: the single richest **premium** source found. It carries a full
  age × sex × acceleration-form × cover-menu grid of monthly premiums at ₩100,000,000
  (1억원) sum assured, 20-year premium term, for both the 기본환급형 and the 해지환급금이
  적은 유형 — 48 published cells for the main contract, plus a rider rate card of comparable
  size. It also documents the **GI** answer to CI (code-based rather than definition-based
  triggers), the 100% 선지급플러스형 with its residual 유족위로금, the 90-day 암 보장개시일,
  the first-year 50% reduction, the 건강인우대 preferred-risk criteria, the banded
  high-sum-assured discount, and a 종신 vs 연금 comparison illustration built on the
  생명보험협회 상품공시시행세칙 basis with its 예정이율 stated.

### S5 — 생명보험협회, 「생보사 주요 CI·GI보험상품 현황」 (별첨)

- Publisher: 생명보험협회 (Korea Life Insurance Association, KLIA)
- Document: a 5-page 별첨 (annex) tabulating, carrier by carrier, the CI and GI products then
  on sale, with each product's headline benefit structure
- Doc type: industry-association 보도자료 별첨
- URL: https://www.klia.or.kr/FileDown.do?fileNo=16793&seq=4
- Accessed: 2026-09-03
- Retrieved: **yes** (the server declares the file `application/x-msdownload`; it is in fact a
  5-page PDF — magic bytes `%PDF-1.4` — and extracted cleanly once renamed)
- What it is good for: a market-wide cross-section in one table — 한화생명, ABL생명, 삼성생명
  (two products), 교보생명 (two), 미래에셋생명, KDB생명, 동양생명 (two), 메트라이프생명,
  AIA생명 (two), NH농협생명 and one further carrier. It is the evidence for the CI → GI
  migration and for the range of acceleration fractions actually on sale.
- **Caveat, recorded at the entry**: the file is served bare, with no parent page reachable
  from the search results, so **its publication date could not be established**. Internal
  evidence — the products named, in particular 삼성생명 GI플러스종신보험 (launched 2020-01,
  [R11]), 미래에셋생명 건강담은 GI종신보험 (2019, [S4]) and 동양생명 수호천사 알뜰한통합GI보험
  — places it in or after 2020. It is treated as an **undated** source and no fact below rests
  on its date.

### S6 — 알리안츠생명, 「무배당 알리안츠유니버셜CI종신보험 약관」 (third-party mirror)

- Publisher: 알리안츠생명보험 (the predecessor of ABL생명); mirrored by Law Insider
- Doc type: 보험약관, mirrored as HTML
- URL: https://www.lawinsider.com/ko/contracts/4s3tMnNkSm6
- Accessed: 2026-09-03
- Retrieved: **in part** (the page renders and a summarising fetch returned the substance of
  the definitions and the benefit table; the mirror is a third-party reproduction, not the
  carrier's own file, so nothing is quoted from it word-for-word below)
- What it is good for: corroboration from a second carrier of the 중대한 암 / 중대한
  급성심근경색증 / 중대한 뇌졸중 definitions and of the 50%/80% pair, and — the fact worth
  having — the **제1보험기간 / 제2보험기간 split at age 80**: 제1보험기간 runs 계약일부터
  80세 계약해당일 전일까지, 제2보험기간 from the 80세 계약해당일 종신토록. That is the
  structure [R1] describes as the original 2002 design.

### S7 — 알리안츠생명, 「무배당 알리안츠어린이CI보험 약관」 (third-party mirror)

- Publisher: 알리안츠생명보험; mirrored by Law Insider
- Doc type: 보험약관, mirrored as HTML
- URL: https://lawinsider.com/ko/contracts/9SLRE7Bms1X
- Accessed: 2026-09-03
- Retrieved: **in part** — the mirror is **heavily redacted** (blocks of ▇▇▇ replace the
  definitional text and every benefit amount). Article headings and the existence of a
  별표1 benefit table on a ₩20,000,000 (2,000만원) basis are legible; nothing else is.
- What it is good for: evidence only that a **children's CI** variant existed on this chassis.
  No number and no definition is taken from it.

### S8 — 삼성생명, 「통합올인원CI보험(무배당, 보증비용부과형)」 상품 페이지

- Publisher: 삼성생명보험주식회사
- Doc type: 상품 페이지 (consumer)
- URL: http://product.samsunglife.com/product/insu/family/univlivcare/insuPrdtUnivLivCareFeat.html?tloParam=bl_allinoneci
- Accessed: 2026-09-03
- Retrieved: **no** — HTTP 503 on both attempts, over `http` and `https`
- Consequence: the market leader's current CI product is present in this file only through the
  KLIA table [S5] and through search snippets, and every fact about it is `[unverified]`. See
  **Fetch failures and gaps**.

---

## Regulatory and actuarial references

### R1 — 보험연구원, 「보험상품 변천과 개발 방향: 생명보험 상품 중심」 Ⅳ. CI보험의 성장

- Publisher: 보험연구원 (Korea Insurance Research Institute, KIRI), 연구보고서 2018-5
- Authors: 김석영·김세영·이선주; 발행 2018년 2월; 원장 한기정's 머리말
- Document: **Chapter Ⅳ, 「CI보험의 성장」, pp. 80–119**, issued as a standalone 40-page PDF
- Doc type: 연구보고서 (research monograph, chapter extract)
- URL: https://www.kiri.or.kr/pdf/%EC%97%B0%EA%B5%AC%EC%9E%90%EB%A3%8C/%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C/nre2018-05_04.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (778 KB PDF; the summarising fetcher declared it corrupt, `pypdf`
  extracted all 40 pages cleanly)
- What it is good for: **the definitive account of why CI보험 exists in Korea and how it was
  priced.** It is a first-hand institutional history written by KIRI researchers with access to
  the product developers: the 2002 launch, the reinsurer relationships, the decision to price
  on disease *definitions* rather than ICD codes, the regulator's refusal of a survival period,
  the requirement to reflect overlap between CI causes in the risk rate, the 안전할증 cap, the
  new-business and premium-income series for 2002–2004, the thyroid-cancer and breast-cancer
  experience shock, and the whole 2003 → 2008 → 2010 → 2013 → 2016 product evolution. It also
  reproduces, in comparison tables, the 중대한 암 / 중대한 급성심근경색증 / 중대한 뇌졸중
  wordings against their ordinary-cover counterparts — an independent check on [S1].

### R2 — 보험연구원, 「보험상품 변천과 개발 방향: 생명보험 상품 중심」 (full report)

- Publisher: 보험연구원, 연구보고서 2018-5; 김석영·김세영·이선주; 2018년 2월; 308 PDF pages
- Doc type: 연구보고서 (complete)
- URL: https://kiri.or.kr/pdf/%EC%A0%84%EB%AC%B8%EC%9E%90%EB%A3%8C/KIRI_20180419_104228.pdf
- Accessed: 2026-09-03
- Retrieved: **yes** (4.5 MB PDF; front matter, contents and Chapter Ⅶ extracted and read;
  the remaining chapters were not read)
- What it is good for: (a) the report's bibliographic identity, which fixes the citation for
  [R1]; (b) **Chapter Ⅶ, 「간편심사보험의 성장」, pp. 189–220** — the 유병자 (impaired-life)
  market: the 2007 무심사 experiment and its loss experience, the 2012 실버암보험 that made
  simplified underwriting work, the taxonomy of 일반심사 / 간편심사 / 무심사, the three
  simplified-underwriting designs (인수기준 완화형, 한정고지형, 가입한정형), the standard
  10-question 계약전 알릴 의무 form, and a sidebar on the **당뇨CI보험** — a CI product sold
  only to diabetics without complications (HbA1c ≤ 8%), which failed for want of a
  distribution route.

### R3 — 금융위원회, IFRS17 주요 계리가정 가이드라인 보도자료 (2024-11-07)

- Exact title: 「합리적인 계리가정과 단계적 할인율 조정을 통해 보험회계의 신뢰도와
  안정성을 높이겠습니다」
- Publisher: 금융위원회 보험과 (Financial Services Commission), 보도자료,
  **2024-11-07**, issued out of the 제4차 보험개혁회의 (2024-11-04)
- Doc type: 보도자료 (regulator press release)
- URL: https://www.fsc.go.kr/no010101/83351
- Accessed: 2026-09-03. Retrieved: **yes** (HTML rendered and read)
- What it is good for: the **IFRS17 주요 계리가정 가이드라인**, which is the live constraint on
  any lapse assumption a Korean 무·저해지 CI product carries. Content used below: the
  로그-선형 (log-linear) model is imposed as the 원칙모형 for 무·저해지 lapse rates, with a
  convergence point at 납입완료 of **0.1%** and a post-completion ultimate lapse rate of
  **0.8%**; departure from the 원칙모형 requires disclosure, in the audit report and the
  경영공시, of the CSM, K-ICS and net-income differences against it, plus 금융감독원 scrutiny;
  단기납 종신보험 must assume **30% 이상** additional lapse at the bonus date; the 실손 손해율
  method moves to 연령군단별 (age-cohort) analysis. Applies from the 2024 year-end
  close (손해율 by 2025 Q1); the 보험부채 할인율 realignment applies from January 2025
  with the 최종관찰만기 extended to 30 years over three years. Estimated industry
  effect: K-ICS down about **20%p**.

### R4 — 보험업법 제4조 (보험업의 허가) — 제3보험업의 법정 정의

- Publisher: 대한민국 법률; retrieved through CaseNote's statute mirror
- Version shown on the page: 법률 제17636호, 2020-12-08 일부개정, 2021-06-09 시행
- Doc type: statute (mirror)
- URL: https://casenote.kr/%EB%B2%95%EB%A0%B9/%EB%B3%B4%ED%97%98%EC%97%85%EB%B2%95/%EC%A0%9C4%EC%A1%B0
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: 제4조제1항 licenses insurance business by 보험종목 in three groups —
  제1호 생명보험업 (생명보험, 연금보험(퇴직보험을 포함한다), 그 밖에 대통령령으로 정하는
  보험종목); 제2호 손해보험업 (화재, 해상(항공·운송 포함), 자동차, 보증, 재보험, 그 밖에
  대통령령으로 정하는 것); **제3호 제3보험업 — 상해보험, 질병보험, 간병보험**, 그 밖에
  대통령령으로 정하는 보험종목. This is the statutory hook that lets a life insurer write the
  health element of a CI contract and, equally, prevents a non-life insurer from writing the
  질병사망 main contract that acceleration requires — see §3 below.
- **Caveat**: `law.go.kr` itself would not serve the statute (see gaps), so this is a mirror,
  and the article text below is paraphrased from the mirror rather than quoted.

### R5 — 서울중앙지방법원 2016. 1. 14. 선고 2014가단242567 판결 [보험금]

- Publisher: 서울중앙지방법원 (판사 김영수); retrieved through CaseNote
- Doc type: judgment (first instance)
- URL: https://casenote.kr/%EC%84%9C%EC%9A%B8%EC%A4%91%EC%95%99%EC%A7%80%EB%B0%A9%EB%B2%95%EC%9B%90/2014%EA%B0%80%EB%8B%A8242567
- Accessed: 2026-09-03. Retrieved: **yes**
- Content: plaintiff A against 교보생명, on two CI contracts — 「무배당 교보다사랑CI보험」
  (2005-02-28) and 「무배당 교보큰사랑CI보험」 (2007-02-06). The insured was diagnosed
  2014-06-28 with a colorectal carcinoma confined to the mucosa. The court held that the
  약관's 중대한 암 definition — requiring 침윤파괴적 증식 into surrounding tissue — was **not**
  satisfied by a mucosa-confined lesion, and rejected the ₩53,000,000 CI claim; but it allowed
  the ordinary 암 rider claim, because the diagnosis carried the KCD code C18 (결장의 악성
  신생물), and the endoscopic polypectomy satisfied the surgery benefit. Award ₩13,000,000
  (₩10,000,000 diagnosis + ₩3,000,000 surgery), with 6% pre-judgment and 15% post-judgment
  interest.
- Why it matters: it is a clean judicial statement of the gap this product creates — the same
  histology is 암 for the rider and not 중대한 암 for the main contract. It is also the reason
  Korean CI 약관 later wrote 대장점막내암 out of 중대한 암 **expressly** (see [S1] 별표4).

### R6 — 조세금융신문, 「[전문가 칼럼] 중대한 뇌졸중은 왜 받기 어렵나요?」

- Publisher: 조세금융신문; 한규홍 (한결손해사정 손해사정사), 2023-12-25
- Doc type: **secondary** — signed practitioner column, not a primary document
- URL: https://tfmedia.co.kr/mobile/article.html?no=154430
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the practitioner's account of the 25% 장해지급률 gate and two declined claims —
  a confirmed 지주막하출혈 with ICU admission that fell below 25%, and a 뇌경색증 with
  demonstrated cognitive decline that likewise fell below it. No statistics.

### R7 — 한국보험신문, 「'중대한' 문턱 높은 CI보험… 소비자 혼선 여전」

- Publisher: 한국보험신문; 주옥진 기자, 2026-04-06
- Doc type: **secondary** — trade press
- URL: https://www.insnews.co.kr/news/articleView.html?idxno=90022
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the most recent evidence in this file that the 중대한 problem is still live —
  a claimant fifteen years into a CI policy, with a 뇌경색 diagnosis and a mobility aid,
  declined on the ground that 일상생활 remained possible at some level. The article carries no
  statistics.

### R8 — 투데이신문, 「'중대한' 조건에 막힌 CI보험, '불완전 판매' 온상되나」

- Publisher: 투데이신문; 이세미 기자, 2020-05-11
- Doc type: **secondary** — trade press, issue-tracking feature
- URL: https://www.ntoday.co.kr/news/articleView.html?idxno=72483
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: mis-selling allegations at the point of sale, and — the point worth recording —
  a 금융감독원 statement that it had **not** identified a particular mis-selling problem in the
  CI sales process. No claim-denial statistics.

### R9 — 보험저널, 「CIㆍGI 보험…나에게 유리한 상품은?」

- Publisher: 보험저널; 최환의 기자, 2020-09-04 (updated 2020-09-07)
- Doc type: **secondary** — trade press, product comparison
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=2863
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the cleanest statement of the CI/GI distinction — CI uses the 약관 정의 방식,
  GI uses the 한국표준질병·사인분류 (KCD) code; GI covers everything under the C codes where CI
  covers only 중대한 암; CI's 뇌졸중 covers both 뇌출혈 and 뇌경색 but behind the 25% gate,
  whereas GI's cerebrovascular cover is often narrower in scope but unconditional. Its premium
  claim — that CI runs about **2% dearer** than GI for identical cover, and that recent GI
  products often reverse that — is a secondary assertion and is tagged as such below.

### R10 — 소비자가만드는신문, 「CI보험 진단금 받기 '하늘의 별따기', 왜?」

- Publisher: 소비자가만드는신문; 김문수 기자, 2015-09-14
- Doc type: **secondary** — consumer press
- URL: https://www.consumernews.co.kr/news/articleView.html?idxno=505280
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: a declined 지주막하출혈 claim (Gwangju, ten-year policy) on the ground that no
  disability was diagnosed, and the statement of the three-part CI test (disease, severity,
  disability rating). No denial-rate statistics.

### R11 — 전자신문, 「[보험 2020] 삼성생명, 보장요건 완화한 'GI플러스종신보험' 출시」

- Publisher: 전자신문, 2020-03-03 (print edition 2020-03-04)
- Doc type: **secondary** — trade press, product launch
- URL: https://www.etnews.com/20200303000151
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the market leader's move from CI to GI. The product covers the three headline
  diseases (암, 뇌출혈, 급성심근경색증) plus 18 further conditions and surgeries (중증
  만성간질환, 중증 만성폐질환, 관상동맥우회술 among them) and 장기요양 1·2등급; it removes the
  중대한 qualifier; it advertises **25** distinct premium-waiver triggers; and it is 삼성생명's
  first **저해지 30%형**. Its acceleration is quoted at 130% of the sum assured before age 65
  and 180% at 65 or later — figures which, being above 100%, cannot be a pure acceleration and
  are recorded here as reported, tagged `[unverified]` for their construction.

### R12 — 스페셜경제, 「CI에서 GI로, SI에서 WI로…진화의 도마 위로 오른 '종신보험'」

- Publisher: 스페셜경제; 이정화 인턴기자, 2020-07-09
- Doc type: **secondary** — trade press
- URL: http://www.speconomy.com/news/articleView.html?idxno=235502
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the four-generation taxonomy of the Korean accelerated whole-life product —
  **CI** (early 2000s, severity definitions), **GI** (from 2010, KCD codes), **SI** (from 2017,
  staged payments as severity progresses), **WI** (from June 2020, wider cerebrovascular and
  cardiac scope on standard classifications) — and the carriers associated with each. The
  generation dates here are the article's, not a regulator's, and the SI/WI labels are trade
  usage rather than defined terms.

### R13 — 뉴스1, 「삼성생명, 질병단계별로 보험금..통합 스테이지CI보험」

- Publisher: 뉴스1, 2014-01-02
- Doc type: **secondary** — trade press, product launch
- URL: https://www.news1.kr/amp/finance/general-finance/1478797
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the Stage CI design in its selling form — 50% acceleration on 중대한 암 stages
  I–III (20% for breast cancer), 100% on stage IV, blood and lymphatic cancers and the other
  최중증 states, with a further 50% payable if a stage I–III cancer progresses to stage IV;
  11 diseases and 8 surgeries including the five-organ transplants and 관상동맥우회술;
  가입나이 15–60; cover extended to age 100.

### R14 — 서울파이낸스, 「[신상품] 미래에셋생명 '건강담은 GI변액종신보험'」

- Publisher: 서울파이낸스, 2020-01-17
- Doc type: **secondary** — trade press, product launch
- URL: https://www.seoulfn.com/news/articleView.html?idxno=369214
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: the variable-account sibling of [S4]. 17 diseases with acceleration up to 100%
  of the sum assured; the 100% 선지급형 still pays **30%** of the main-contract sum assured to
  the family as an annuity on death; 중증갑상선암 and 남성유방암 are pulled back into 일반암;
  루게릭병 and 다발경화증 sit in the main contract.

### R15 — 보험저널, 「CI 보험 보장분석, 무조건 해지는 금물…"꼼꼼한 점검이 우선"」

- Publisher: 보험저널; 최은빈 기자, 2024-05-29
- Doc type: **secondary** — trade press, consumer advice
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=23012
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: evidence only that a large block of legacy CI business is still in force and
  under review by its policyholders, and that 갱신형 riders attached to it terminate at 80. No
  statistics.

### R16 — 로이즈손해사정, 「중대한 질병 CI보험 진단금 사정 사례」

- Publisher: 로이즈손해사정 (independent loss adjuster), case note; date not stated on the page
- Doc type: **secondary** — practitioner case note
- URL: https://www.lloyds.co.kr/post/중대한-질병-ci보험-진단금-사정-사례
- Accessed: 2026-09-03. Retrieved: **yes**
- Content used: a worked claim — main contract ₩35,000,000 (3,500만원) issued October 2006,
  CI benefit 50% = ₩17,500,000; a left lenticulostriate 뇌경색 with right-sided weakness,
  initially declined for want of a permanent deficit, then paid in full once a 후유장해진단서
  established a permanent ADL restriction. The adjuster records the insurer's working rule as
  **six months or more of rehabilitation with an ADL-based rating of 25% or higher**. That
  six-month practice point is the adjuster's, not the 약관's, and is tagged accordingly.

---

## Fact extraction

### 1. Where CI보험 sits, and why it is a whole-life contract

- **CI보험 is a 종신보험 with an acceleration clause, licensed as first-sector business.** The
  main contract promises a death benefit; the CI payment is a *pre-payment of part of that
  death benefit*, not a separate sum. [S1] states the whole structure in one line of the
  주요내용 요약서: 「사망보험금은 CI/LTC보험금을 수령한 경우에는 기본보험금의
  50%(50%선지급형) 또는 20%(80%선지급형) 만 지급합니다」 [S1].
- The health element rides on 제3보험, which 보험업법 제4조제1항제3호 defines as **상해보험,
  질병보험, 간병보험** [R4]. Both life and non-life insurers may write 제3보험. What they may
  **not** both write is the main contract: a 손해보험회사 cannot make 질병사망 the 주보험, so
  a non-life insurer cannot construct an acceleration at all. [R1] records the consequence
  precisely — when 흥국생명 launched a women's CI product, the non-life market's answer was the
  same disease list written as **독립급부 특약** attached to a 통합보험, 「손해보험회사는
  생명보험회사와 달리 질병사망을 주보험으로 설계할 수 없어 선지급 형태로 설계하지 못하고,
  독립급부 형태로 상품을 설계함」 [R1]. This is the single sharpest structural line in the
  Korean health market and it is a licensing line, not a product-design choice.
- The 2002 design put the acceleration inside a **two-period contract**: 제1보험기간 from
  계약일 to the day before the 80세 계약해당일, 제2보험기간 from the 80세 계약해당일 종신토록
  [S6]. [R1] gives the economics of that split: 「최초 판매된 선지급형 CI보험은 80세까지
  발생하는 중대질병에 대해 사망보험금을 선지급(50%, 80%)하며, 80세 이후부터는 사망보험금을
  100% 지급하도록 설계되었다」 [R1]. From 2008 the CI cover itself was extended to **100세**
  while the death cover stayed 종신 [R1] [R13].
- Because the chassis is whole-life, the CI contract carries everything `WholeLife_KR_S`
  carries: a 계약자적립금 credited at the 공시이율 with a 최저보증이율 floor, a 해지환급금 net
  of 미상각신계약비, a 보험계약대출, and a 납입면제. [S1] articles 34, 37 and 39 and the
  주요내용 요약서 all confirm this. A UK or Australian standalone CI policy has none of it.
- A distinctive Korean floor rides on the sum assured. [S1] defines
  **기본보험금 = max(기본사망보험금, 이미 납입한 보험료, 계약자적립금의 105%)**, where
  기본사망보험금 is 보험가입금액 less 중도인출금액 plus 추가납입보험료 [S1 별표1 주7]. [S3]'s
  older universal-life version of the same product used **110%** rather than 105% [S3]. Every
  benefit — the acceleration and the residual death benefit alike — is a percentage of that
  floored quantity, not of the face amount, which matters for a model: the CI benefit cannot
  fall below half of premiums paid on a 50% form.

### 2. Origin and market history

- **The product concept.** CI was devised in South Africa in **1983** by Dr Marius Barnard,
  who had taken part in the first heart transplant in 1967 and had watched his patients
  survive their disease and lose their livelihoods to the cost of it [R1]. It spread to the
  UK (1985), Australia (1987), Hong Kong (1988) and Taiwan (1990), reaching Korea in **2002**
  [R1].
- **The Korean launch.** 삼성생명 launched the first Korean CI product in **2002년 5월**,
  developed jointly with the reinsurer **RGA** [R1]. RGA had first offered the design to
  ING생명, which declined it [R1]. The commercial motive was defensive: 삼성생명 had stopped
  selling health insurance in **2001** after its 여성시대 product's loss experience, and
  non-life insurers were taking the health market it had vacated with 실손 riders on five-year
  renewable contracts [R1].
- **Reinsurance shaped it.** 삼성생명 ceded about **40%** of the risk. It wrote roughly
  1,000,000 policies in the first two years, and about **2,000,000 in four years**; RGA opened
  a Korean branch on **2004-12-20** on the strength of it, and 삼성생명 later diversified part
  of the cession to Hannover Re's Hong Kong branch [R1]. Every other carrier followed with a
  reinsurer: 대한생명 (now 한화생명) with RGA, 교보생명 with Trans America, 동양생명 and
  메트라이프생명 with Munich Re, ING생명 with GenRe, 금호생명 with 코리안리 [R1].
- **Sales, 2002–2004** [R1], from 금융감독원's 정례브리핑 of 2005-03-29, 「2004년 보험상품
  판매현황 분석」; excludes 변액CI; figures in parentheses are the share of total life
  business:

  | | CY2002 | CY2003 | CY2004 |
  |---|---|---|---|
  | 신계약 건수 (천 건) | 131 (0.5%) | 719 (3.2%) | **2,107 (9.9%)** |
  | 초회보험료 (억 원) | 131 (0.2%) | 916 (1.5%) | **7,096 (11.1%)** |
  | 수입보험료 (억 원) | 370 (0.1%) | 4,847 (1.0%) | **27,879 (5.3%)** |

  The 2004 → 2003 growth was +193.1% in policy count and +674.3% in first-year premium [R1].
  In won: 2004 첫해보험료 ₩709.6bn (7,096억원) and 수입보험료 ₩2,787.9bn (27,879억원).
- **Peak volume.** 「2000년대 중반에는 CI보험이 1년에 약 180만 건 판매되는 기록을 세우기도
  하였다」 [R1] — about 1.8 million policies a year.
- **The experience shock.** Two things went wrong at once. First, **thyroid cancer**: nobody in
  the 2002 pricing discussion anticipated the incidence surge — the RGA team were Australian
  and had debated skin and prostate cancer instead — and thyroid incidence grew at 22.6% a year
  against 3.5% for all cancers [R1]. Second, **sex mix**: over 2003–2005 women bought about
  **150%** of the male policy count but generated about **244%** of the male claim count, on
  breast and thyroid cancer [R1]. Carriers responded by moving early thyroid cancer out of the
  main contract into a rider, and from **2008** by imposing a **180-day 부담보** on breast
  cancer [R1]. The modern descendant of that 180-day bar is the first-year 50% reduction on
  breast cancer in [S1] and the general first-year 50% reduction in [S4] — see §11.
- **Displacement.** [R12] gives the trade's own four-generation account: **CI** (early 2000s,
  severity definitions) → **GI** (from 2010, KCD codes) → **SI** (from 2017, staged payments)
  → **WI** (from June 2020, wider scope on standard classifications). By 2020 the market leader
  itself had launched a GI product explicitly on the ground that it removed the 중대한
  qualifier [R11]. The KLIA cross-section [S5] shows CI and GI selling side by side at the same
  carriers, with GI in the majority of the newer entries. Legacy CI blocks remain large enough
  to be a standing consumer-advice topic in 2024 [R15] and a live complaint topic in 2026 [R7].

### 3. The three benefit forms, and why Korea took the acceleration

[R1] sets out the international taxonomy and Korea's position in it:

| Form | Structure | Korean position [R1] |
|---|---|---|
| **선지급형** (acceleration) | attached to death cover; part of the death benefit paid early on CI | 「CI보험의 대부분이 선지급형으로 설계」 |
| **추가지급형** (additional) | CI benefit added on top of a death benefit, payable if the insured survives a stated period | sold, but 「우리나라는 생존기간 반영이 없음」 |
| **단독형** (stand-alone) | independent CI contract, benefit on surviving a stated period | sold, but again with no survival period |

- **The survival period is the hinge.** Overseas practice prices CI on a minimum **30-day**
  survival requirement [R1]. The Korean supervisor took the opposite view — that requiring
  survival would create disputes where the insured died, and that paying on a post-mortem
  finding of the CI cause was better consumer protection — so no Korean CI product reflects a
  survival period in its benefit definition or its rate [R1]:
  「국내에서 CI 질병에 대한 진[단]보험금 지급 시 일정한 생존기간에 대한 조건을 반영하지
  못하는 것은 궁극적으로 … 사망보험금과 연계한 선지급형 CI보험이 주요상품으로 자리 매김한
  계기가 되었다」 [R1].
- **Consequence for a model**: on the acceleration form the insurer is largely indifferent to
  whether the CI event is followed by early death, because the two benefits share one sum
  assured. That is the whole risk-management logic of the Korean design, and it is why [R1]
  describes CI as 「종신보험의 사망보험금을 선지급하는 상품으로 개발되어 건강보험이 가질 수
  있는 보험리스크를 축소」 [R1].
- **Definitions rather than codes.** The other founding decision was to pay on defined disease
  states rather than on KCD/ICD codes. [R1] records the reasoning from the RGA physician in the
  room: a myocardial infarction can be discovered incidentally at a health check with no
  symptoms the patient ever noticed, and a code-based trigger would have to pay for it [R1].
  Twenty years later that decision is the product's principal liability — see §18.

### 4. The acceleration fraction, and what remains payable on death

This is the parameter the model turns on. Two forms dominate; a third has emerged on GI.

**[S1], (무)우리가족안심CI통합종신보험, 별표1 보험금 지급기준표** — quoted in full because it
is the cleanest published statement of the mechanic:

- **CI/LTC보험금** (payable once only, on the first of 중대한 질병 / 중대한 수술 / 중대한 화상
  및 부식 / 장기요양상태):
  - 50% 선지급형: 기본보험금의 **50%**
  - 80% 선지급형: 기본보험금의 **80%**
  - in either case, if the trigger is **breast cancer within one year of 계약일**, the
    percentage halves — 25% and 40% respectively [S1 별표1].
- **사망보험금**:
  - CI/LTC보험금 지급사유가 발생하지 않은 경우: **기본보험금** (100%)
  - after a CI payment, 50% 선지급형: 기본보험금의 **50%**; 80% 선지급형: 기본보험금의
    **20%** — i.e. exactly the complement
  - after a *first-year breast-cancer* CI payment: **75%** (50% form) and **60%** (80% form),
    again the complement of the halved acceleration [S1 별표1].
- A floor rides underneath the residual: where a death claim follows a CI payment, the insurer
  pays 「CI/LTC보험금 지급사유 발생당시의 기본보험금의 50%(80%형은 20%)와 CI/LTC보험금
  지급사유 발생 후 계약자적립금의 105%」 **중 큰 금액** [S1 별표1 주8]. So on a long-surviving
  post-CI policy the residual death benefit can grow above its nominal complement as the
  account value accumulates. This matters for the model: the residual is
  `max(complement × basic_sum, 1.05 × account_value)`, not a constant.
- The complement identity holds exactly: 50 + 50 = 100, 80 + 20 = 100, 25 + 75 = 100,
  40 + 60 = 100 [S1]. **The acceleration is a true acceleration** — it never adds cover.

**[S2], the 저해지환급형 sibling, worked example at ₩100,000,000 (1억원), 80% 선지급형**
[S2, 용어해설 「보험금 지급 예시」]:

| Case | CI/LTC payment | Later death payment |
|---|---|---|
| CI/LTC event (not first-year breast cancer) | ₩80,000,000 (8,000만원) | ₩20,000,000 (2,000만원) |
| First-year breast-cancer CI/LTC event | ₩40,000,000 (4,000만원) | ₩60,000,000 (6,000만원) |
| Death with no CI/LTC event | — | ₩100,000,000 (1억원) |

**[S3], the universal-life CI of 2011**, uses the identical pair but on a variable chassis:
사망보험금 = 기본보험금 + 변동보험금 before any CI event; after a CI event,
「50%선지급형: CI크리닉보험금 지급시의 기본보험금 50% + 변동보험금 / 80%선지급형: … 기본보험금
20% + 변동보험금」, with the same 「기본보험금의 50%(80%선지급형은 20%)와 … 계약자적립금의
110% 중 큰 금액」 floor [S3]. Note 110% there against 105% in [S1] — the floor multiplier is a
carrier and vintage parameter, not a constant.

**The 100% form is a GI-era innovation, and it is not a pure acceleration.** [S4] offers
50% 선지급형, 80% 선지급형 and **100% 선지급플러스형**. On the 100% form the whole sum assured
is paid on diagnosis after year one and **사망보험금 없음** thereafter [S4]; what remains is a
separate 유족위로금 of **보험가입금액의 1% paid monthly for 30 months** — 30% of the sum
assured in instalments, funded as its own benefit rather than as a residue [S4]. The variable
sibling describes the same 30% as an annuity to the family [R14]. Where a first-year event
triggers the 100% form, the acceleration is **50%** and the residual death benefit is **50%**
[S4].

Summary of observed acceleration fractions, main contract, first CI event after year one:

| Fraction | Residual death benefit | Sources |
|---|---|---|
| 50% | 50% | [S1] [S2] [S3] [S4] [S5] [S6] [R13] |
| 80% | 20% | [S1] [S2] [S3] [S4] [S5] [S6] |
| 100% | nil, plus 유족위로금 1% × 30 (= 30%) | [S4] [R14] |
| 100% (staged, 최중증 only) | nil | [R13] |
| 30%–80%, policyholder-selected | complement | 여성CI [R1] |
| age-varying (higher at old ages) | complement | 메트라이프생명, 2009 [R1] |

### 5. 중대한 암 (critical cancer) — the definition, verbatim

[S1] 별표4 Ⅰ, quoted:

> 「"중대한 암"이라 함은 악성종양세포가 존재하고 또한 주위 조직으로 악성종양세포의
> 침윤파괴적 증식으로 특징지을 수 있는 악성종양을 말하며, 다음 각 목에 해당하는 경우는
> 보장에서 제외합니다.」

The operative words are **침윤파괴적 증식** — invasive, destructive proliferation into
surrounding tissue. That is the whole of the narrowing: the definition does not name a stage,
a size or a grade; it names a behaviour. [R1]'s comparison table makes the point that this is
「암에 대한 일반적인 특징(진행성, 침윤성)을 설명한 것으로 일반암에도 해당할 수 있는 사항임」
— that is, read on its own terms the definition would cover most cancers. **The narrowing is
done by the exclusion list, not by the opening sentence.** [S1] 별표4 Ⅰ①:

- 가. six named malignancies:
  1. 피부의 악성흑색종 (melanoma) with low invasion depth — **TNM 병기분류상 T2aN0M0 이하**
  2. 기타피부암 (**C44**)
  3. 전립선암 (**C61**)
  4. 갑상선암 (**C73**)
  5. a cancer arising before the 중대한 암 보장개시일 that recurs or metastasises after it
  6. **대장점막내암** — defined at length: a colorectal malignancy (C18–C20) whose cells have
     breached the 기저막 (basement membrane) into the 점막고유층 (lamina propria) or the
     점막근층 (muscularis mucosa) but **not** the 점막하층 (submucosa)
- 나. 병리학적으로 전암(前癌)상태, **제자리암** (carcinoma in situ, D00–D09) and **경계성종양**
  (borderline malignancy, D37–D48 excluding D45, D46, D47.1, D47.3, D47.4, D47.5)
- 다. any currently benign tumour, whatever the body site

[S1] then does something a UK CI wording does not: it publishes a **positive KCD code list** of
what *is* 중대한 암, on the 7th revision of the 한국표준질병·사인분류 (통계청고시
제2015-309호, in force 2016-01-01) — C00–C14, C15–C26, C30–C39, C40–C41, C43, C45–C49, C50,
C51–C58, C60, C62, C63, C64–C68, C69–C72, C74, C75, C76–C80, C81–C96, C97, and then the
myeloproliferative group **D45** (진성 적혈구 증가증), **D46** (골수형성이상증후군),
**D47.1** (만성 골수증식질환), **D47.3** (본태성 혈소판혈증), **D47.4** (골수섬유증),
**D47.5** (만성 호산구성 백혈병) [S1 별표4 Ⅰ②]. So the 약관 is simultaneously
definition-based and code-based: the code list bounds the universe and the 침윤파괴적 증식
test and the exclusions cut it down.

Diagnostic-evidence requirements [S1 별표4 Ⅰ③–⑥]:

- the diagnosis, the 원발병소, the type and the stage must be settled by a 병리 or relevant
  specialist (**치과의사 제외**) at a 의료법 제3조 medical institution
- it must rest on the microscopic findings of a **조직검사 (biopsy)**, **미세바늘흡인검사**,
  **혈액검사** or **골수검사**; where none is possible, documented evidence of diagnosis or
  treatment suffices
- staging follows the **AJCC Cancer Staging Manual 제7판**, or whichever edition is current at
  the date of diagnosis
- staging is **병리학적 병기설정 (pathologic staging)** where possible, 임상적 병기설정
  otherwise

A drafting detail worth carrying into a model that reasons about metastases: under the KCD
selection rules, secondary and unspecified sites C77–C80 are classified to the **원발부위**
where a primary is identified [S1 별표4 Ⅰ, 유의사항].

**The exclusions are where the money is.** Every one of the four named cancers excluded from
중대한 암 — melanoma below T2aN0M0, other skin cancer, prostate, thyroid — was moved out
because of adverse experience or is a low-severity high-frequency site; thyroid and breast were
the two that broke the original pricing [R1]. 대장점막내암 was written out expressly after
litigation of exactly that lesion [R5].

### 6. 중대한 급성심근경색증 (critical acute myocardial infarction)

[S1] 별표4 Ⅱ, quoted:

> 「"중대한 급성심근경색증"이라 함은 관상동맥의 폐색으로 말미암아 심근으로의 혈액공급이
> 급격히 감소되어 해당 심근조직의 비가역적인 괴사를 가져오는 질병으로서 한국표준질병·
> 사인분류 중 '중대한 급성심근경색증 대상 질병분류표'에 해당하는 질병 중에서 발병 당시
> 다음의 3가지 특징을 모두 보여야 합니다.
> 가. 의사가 작성한 진료기록부상 전형적인 흉통의 존재
> 나. 급성 심근경색의 전형적인 심전도 변화(ST분절, T파, Q파)가 새롭게 출현
> 다. CK-MB를 포함한 심근효소의 발병당시 새롭게 상승」

- **All three must be present**, and the 약관 says so twice — 「상기 가.~다. 중 하나 또는 두
  개의 특징만을 가지고 있는 경우 보장에서 제외합니다」, with two worked negatives: a diagnosis
  on cardiac enzymes alone, or on ECG alone, is excluded [S1 별표4 Ⅱ②].
- **Modern imaging does not qualify as the basis.** A diagnosis founded on 심초음파검사,
  핵의학검사, MRI or 양전자방출단층촬영술 rather than on 가.~다. is excluded [S1 별표4 Ⅱ③].
  [R1]'s version of the same clause adds 관상동맥촬영술 to that excluded list.
- **All angina is excluded**, named in terms: 안정협심증, 불안정 협심증, 변형협심증 —
  「모든 종류의 협심증은 보장에서 제외합니다」 [S1 별표4 Ⅱ④]. [R1] notes the reason plainly:
  angina is KCD **I20** and the covered code is **I21** only.
- **The covered code is a single item**: 급성 심근경색증 **I21** [S1 별표4 Ⅱ⑤]. An ordinary
  급성심근경색증 진단비 rider typically covers **I21–I23** [R1].
- What is *not* narrowed: [R1]'s comparison notes that the three features are the ordinary
  clinical picture of an infarction — 「심전도 변화와 심근효소가 상승하는 것을 기준으로 진단
  확정함. 이는 일반적인 급성 심근경색증과 동일함」. The narrowing is the **conjunction** and
  the exclusion of imaging-based and silent infarctions, which is precisely the case the RGA
  physician raised in 2002 [R1].

### 7. 중대한 뇌졸중 (critical stroke) — and the 25% disability gate

[S1] 별표4 Ⅲ, quoted:

> 「"중대한 뇌졸중"이라 함은 지주막하출혈, 뇌내출혈, 기타 비외상성 두개내 출혈, 뇌경색증이
> 발생하여 뇌혈액 순환의 급격한 차단이 생겨 그 결과 영구적인 신경학적 결손(언어 장애,
> 운동실조, 마비 등)이 나타나는 질병을 말합니다.」

and then the clause that decides almost every dispute:

> 「'영구적인 신경학적 결손'이란 주관적인 자각증상(symptom)이 아니라 신경학적인 검사를
> 기초로 한 객관적인 신경학적 이상소견(sign)로 나타난 장애로서 장해분류표에서 정한
> "신경계에 장해가 남아 일상생활 기본동작에 제한을 남긴때"의 **지급률이 25% 이상인
> 장해상태**[장해분류별 판정기준 13. 신경계·정신행동 장해 "가. 장해의 분류 1)" 및
> "나. 장해판정기준 1) 신경계 ①, ③"에 따라 판정함]를 말합니다.」 [S1 별표4 Ⅲ②]

- The disease scope is the same as an ordinary 뇌출혈·뇌경색 rider's: 지주막하출혈 **I60**,
  뇌내출혈 **I61**, 기타 비외상성 두개내출혈 **I62**, 뇌경색증 **I63** [R1]. There is no
  narrowing on the disease at all. **The narrowing is entirely the 25% disability gate**, and
  [R1] says so: 「중대한 뇌졸중은 일반적인 뇌졸중의 범위와 크게 다르지 않으나, 영구적인
  신경학적인 결손(장해지급률 25% 이상) 조건이 요구되기 때문에 영업현장 및 고객의 입장에서
  이해가 쉽지 않은 측면이 있다」 [R1].
- Diagnostic basis: CT, MRI, 뇌혈관조영술, PET, SPECT or 뇌척수액검사, showing findings
  **새롭게 출현** at onset and **consistent with** the permanent deficit; a diagnosis on CT
  alone, or on the deficit alone, is excluded [S1 별표4 Ⅲ③④].
- Excluded absolutely: **일과성 허혈 발작 (TIA)** and **가역적 허혈성 신경학적 결손 (RIND)**;
  and any 뇌출혈/뇌경색 caused by trauma, by a brain tumour, as a complication of brain
  surgery, or by occlusion of the **안동맥 (ophthalmic artery)** producing a deficit
  [S1 별표4 Ⅲ⑤]. The 약관's own glossary fixes the two abbreviations numerically: TIA is a
  deficit resolving **within 24 hours**; RIND is one resolving after 24 hours but **within one
  week** [S1].

**What "25%" actually requires.** The gate is not in the CI definition; it is in the 장해분류표
that every Korean life policy carries, so it is effectively a supervisory parameter.
[S1] 별표3, item 13:

- 「"신경계에 장해를 남긴 때"라 함은 뇌, 척수 및 말초신경계 손상으로 "<붙임>일상생활
  기본동작(ADLs) 제한 장해평가표"의 5가지 기본동작 중 하나 이상의 동작이 제한되었을 때를
  말한다」; the headline range for the item is **10~100%** [S1 별표3].
- Ratings below **10%** are not a recognised disability at all [S1 별표3, 13-나-1)-나)].
- **Timing**: 「뇌졸중, 뇌손상, 척수 및 신경계의 질환 등은 발병 또는 외상 후 **12개월** 동안
  지속적으로 치료한 후에 장해를 평가한다」, with a further 6-month deferral where function is
  still improving or death is expected shortly [S1 별표3, 13-나-1)-라)]. So a CI stroke claim
  is, by construction, **not assessable for a year**. An adjuster's working rule of six months'
  rehabilitation plus a ≥25% rating is reported at [R16], and is that practitioner's, not the
  약관's.
- The assessing physician must be a 재활의학과, 신경외과 or 신경과 전문의 [S1 별표3].

The ADLs schedule itself — 「<붙임> 일상생활 기본동작(ADLs) 제한 장해평가표」, reproduced from
[S1] 별표3 with the percentages exactly as printed:

| Domain | Rating band |
|---|---|
| **이동동작** | 40% / 30% / 20% / 10% |
| **음식물섭취** | 20% / 15% / 10% / 5% |
| **배변·배뇨** | 20% / 15% / 10% / 5% |
| **목욕** | 10% / 5% / 3% |
| **옷 입고 벗기** | 10% / 5% / 3% |

with, at the top of each band [S1]:

- 이동동작 **40%**: cannot leave the room without continuous help from another person even with
  a special aid, or needs continuous help for wheelchair transfer and movement; **30%**: cannot
  leave the room without a wheelchair or another person's help, or cannot walk but can propel a
  wheelchair unaided; **20%**: cannot walk independently without crutches or a walker; **10%**:
  walks unaided but with a limp, cannot manage stairs without a handrail, or cannot walk 100 m
  on the flat continuously
- 음식물섭취 **20%**: cannot eat by mouth at all and is fed partly or wholly by tube or
  intravenous line; **15%**: cannot use utensils and cannot eat at all without continuous help
- 배변·배뇨 **20%**: needs continuous help with a stoma or catheter, or has an indwelling
  catheter, 방광루, 요도루 or 장루
- 목욕 **10%**: needs continuous help with all personal hygiene
- 옷 입고 벗기 **10%**: needs continuous help to dress and undress upper and lower body

**The arithmetic of the gate, which the product spec will need.** The domain maxima sum to
40 + 20 + 20 + 10 + 10 = **100%**. To reach 25% the claimant must therefore be in roughly
one of:

- 이동동작 alone at **30%** or **40%** — that is, wheelchair-dependent or worse; or
- 이동동작 20% (walker-dependent) plus any one of 음식물섭취 5–15%, 배변·배뇨 5–15%, 목욕 3–10%
  or 옷 입고 벗기 3–10% summing to ≥5%; or
- a combination of the four non-mobility domains totalling ≥25%, which requires impairment in
  at least three of them.

An independently mobile stroke survivor with cognitive impairment and no ADL restriction scores
**zero** on this table. That is the whole of the dispute record in §18: [R6]'s two declined
claims, [R7]'s 2026 case, [R10]'s 지주막하출혈 case, and [R16]'s claim that was declined and
then paid once a 후유장해진단서 documented a permanent ADL restriction.

### 8. The other 중대한 질병

[S1] 제3조 defines 중대한 질병 as a closed list of **eight**: 중대한 암, 중대한
급성심근경색증, 중대한 뇌졸중, 말기신부전증, 말기간질환, 말기폐질환, 중증 재생불량성빈혈,
루게릭병 [S1 제3조①]. Definitions from [S1] 별표4:

- **말기신부전증 (Ⅳ)** — 「양쪽 신장 모두가 비가역적인 기능 부전을 보이는 말기신질환(End
  Stage Renal Disease)으로서 보존 요법으로는 치료가 불가능하여 혈액투석이나 복막투석을 받고
  있거나 받은 경우」; 「일시적으로 투석치료를 필요로 하는 신부전증은 … 제외」 [S1]. The gate
  is dialysis in fact, not a creatinine or eGFR threshold.
- **말기간질환 (Ⅴ)** — end-stage liver disease producing cirrhosis, requiring **all three** of
  영구적 황달 (jaundice), 복수 (ascites) and 간성뇌병증 (hepatic encephalopathy), confirmed on
  periodic physical examination, blood tests and imaging [S1].
- **말기폐질환 (Ⅵ)** — a chronic respiratory-failure state requiring **both**: (가) permanent
  oxygen therapy for hypoxia, and (나) **FEV1.0 ≤ 25% of predicted** on lung-function testing.
  The 약관 supplies a 폐질환분류표 of eligible codes: J09–J18, J20–J22, J40–J47, J60–J70,
  J80–J86, J90–J99 [S1]. It also notes that gas-analysis and spirometry results fluctuate, so
  the assessment must rest on the test that best represents the disease course [S1].
- **중증 재생불량성 빈혈 (Ⅶ)** — the most numerically explicit definition in the whole annex.
  Requires an irreversible severe aplastic anaemia with marrow hypocellularity and peripheral
  pancytopenia, under continuing treatment by transfusion, haematopoietic growth factor or
  immunosuppression, with a specialist's opinion that haematopoietic stem-cell transplantation
  is needed. "Irreversible severe" means marrow **cellularity < 25%** (or 25–50% with
  haematopoietic cells < 30%) **and** at least two of three peripheral findings [S1]:
  - 절대호중구수 **< 500/μL**
  - 혈소판 **< 20,000/μL**
  - 교정망상적혈구수 **< 1%**
- **루게릭병 (Ⅷ)** — amyotrophic lateral sclerosis, defined by KCD code: **G12.20** (가족성
  근위축측삭경화증) and **G12.21** (산발형 근위축측삭경화증), diagnosed by a 신경과 전문의
  on history, neurological examination, blood tests, CSF, muscle biopsy, EMG, cervical X-ray,
  MRI or myelography [S1].

[S1] adds one condition that is neither a 질병 nor a 수술:

- **중대한 화상 및 부식 (별표6)** — third-degree burns or chemical corrosion over
  **20% or more of total body surface**, measured by the **Rule of 9's** or the **Lund &
  Browder** chart, or an equivalent standardised chart [S1 별표6]. Its cover starts on the
  계약일, not after the 90-day wait [S2 별표1 주1].

**The list grew over time** [R1]: eight conditions at launch in 2002 (three diseases, three
cardiac surgeries, 말기신부전, 장기이식수술); eleven from 2003 with 말기간질환, 말기폐질환 and
중대한 화상; LTC added as a covered state from 2008; thirteen in 삼성생명's 2013 Stage product
[R13]; and by the GI generation a "17대 질병" menu that folds in 중증루프스신염,
중증세균성수막염, 다발경화증 and 원발성폐동맥고혈압 [S4]. [S5] records 삼성생명's 통합올인원CI
as widening 「보장 대상 질병/수술 기존 28개에서 45개로」 — a count that must include riders,
since no main contract in this file names more than 21.

### 9. 중대한 수술 (critical surgery)

[S1] 제4조 and 별표5 define four, and the drafting is uniformly hostile to catheter-based
technique:

- **관상동맥(심장동맥)우회술** — CABG performed by **개흉술** with an autologous graft (대복재
  정맥, 내유동맥) anastomosed distal to the stenosis. Excluded in terms: **관상동맥성형술
  (PTCA), 스텐트삽입술, 회전죽상반절제술** and any catheter or non-thoracotomy procedure [S1].
- **대동맥인조혈관치환수술** — must be by 개흉술 or 개복술, and must do **both** excise the
  aortic lesion **and** replace it with an artificial graft. "대동맥" means the thoracic or
  abdominal aorta only; branch arteries are excluded. Catheter procedures — expressly
  **경피적 혈관내 대동맥류수술 (EVAR)** — are excluded [S1].
- **심장판막수술** — 개흉술 **and** 개심술, then either complete excision and replacement with
  a prosthetic or bioprosthetic valve, or valvuloplasty. Excluded: catheter procedures,
  expressly **경피적 판막성형술**, and anything not involving both thoracotomy and open heart
  [S1].
- **5대장기이식수술** — transplantation of 간장, 신장, 심장, 췌장 or 폐장 from another person
  into a recipient in chronic organ failure, at a government-recognised transplant institution.
  **랑게르한스소도세포이식수술** (islet-cell transplantation) is excluded [S1].

This is a real and quantifiable morbidity effect, not a drafting nicety: the excluded
percutaneous techniques are now the majority of coronary and aortic intervention. The GI
generation reacts by adding the excluded procedures back as *riders* — [S5] records
미래에셋생명 pairing 관상동맥우회술 with 관상동맥성형술, 대동맥류인조혈관치환수술 with
경피적대동맥류 중재술, and 심장판막수술 with 경피적심장판막 성형술 [S5].

### 10. LTC on the CI chassis — a statutory trigger inside a private contract

- CI and LTC were welded together in **2008**, when 교보생명 added 일상장해상태 and 중증치매 to
  its CI product because standalone LTC would not sell: the buying ages were too young, the
  state was hard to explain, and the premium was too small to pay a meaningful commission
  [R1]. 「장기간병 상품 단독으로는 성공하지 못하였으나 CI와 결합하여 판매한 장기간병담보는
  성공적으로 안착하게 되었다」 [R1].
- Also in 2008 the private definition was **realigned to the public scheme** [R1]. [S1] shows
  the modern result — the CI product's LTC trigger is a *public administrative decision*:

  > 「"장기요양상태"라 함은 「만 65세 이상 노인」 또는 「노인성 질병을 가진 만 65세 미만의
  > 자」로서 거동이 현저히 불편하여 장기요양이 필요하다고 판단되어 **노인장기요양보험법에
  > 따라 등급판정위원회에서 장기요양 1등급 또는 장기요양 2등급으로 판정받은 경우**」
  > [S1 제6조]

  There is no medical definition in the contract at all. 노인성 질병 (dementia, cerebrovascular
  disease and the rest) is defined by 대통령령 [S1 제6조].
- The LTC trigger shares the CI benefit: [S1] pays **one** CI/LTC보험금, on the first of
  중대한 질병, 중대한 수술, 중대한 화상 및 부식 **or** 장기요양상태 [S1 별표1]. It is not an
  additional benefit; it is another way into the same acceleration.
- Its own waiting period: **장기요양상태 보장개시일** is 90 days from 계약일 (or 부활일), with
  the exception that where the LTC state arises directly from a 재해 (accident) the
  cover starts on the 계약일 itself [S1 별표1 주2].
- [R11] shows the same trigger, 장기요양 1·2등급, carried into the GI generation at 삼성생명.

**The earlier private definitions, for context** [R1]: 삼성생명's 1992 「에버그린보장」 —
Korea's first LTC cover, borrowed from Japan and still using the Japanese word 개호 — paid on
bed-boundedness plus restriction in **3 of 4 ADLs** (식사, 화장실 이용, 목욕, 착탈의); its
dementia cover required 인식불명 (MMSE-K or CDR) plus 2 of 4 ADLs. In 2003 삼성생명 and SCOR
relaxed this to **1 of 4** including immobility, and made dementia turn on 인식불명 alone —
which raised the incidence and therefore the price, and it did not sell [R1]. A dementia rider
on [S3] shows the private wording that survived alongside: 중증치매 = CDR **3점 이상**,
persisting **90일 이상** with no expectation of improvement, after a **2-year** waiting period
[S3].

### 11. 면책기간 and 감액기간 — the 90 days and the first year

- **The 90-day wait applies to 중대한 암 only, and it is drafted as a coverage start date, not
  as an exclusion.** [S1]: 「"CI/LTC보험금"중 "중대한 암"의 보장개시일은 계약일(부활(효력회복)
  일)부터 그 날을 포함하여 **90일이 지난날의 다음날**」 [S1 제7조, 별표1 주1]. The other seven
  중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 are covered **from the 계약일**
  [S1] [S2 별표1 주1]. 장기요양상태 has its own 90-day wait [S1 별표1 주2].
- [S2] words the same thing as a single 「중대한 질병 및 수술 보장개시일」 90 days out, with
  중대한 화상 및 부식 carved back to the 계약일 [S2]. [S3]'s 2011 wording is the same 90 days,
  again excepting the burn [S3]. [S4]'s GI product calls it 「암 보장개시일」 and uses the same
  90 days [S4]. **The 90-day cancer wait is invariant across every document retrieved.**
- **Two consumer protections ride on it**, and both are unusual enough to model:
  1. If 중대한 암 is diagnosed before the 보장개시일, the policyholder may **cancel the
     contract** and recover the premiums [S1 제7조⑤].
  2. If the policyholder does *not* cancel, the pre-inception cancer is permanently outside
     cover — 「동일하거나 다른 신체기관에 재발 또는 전이되어 "중대한 암"으로 … 지급사유가
     발생한 경우라도 CI/LTC보험금을 지급하지 않으며, 보험료의 납입을 면제하지 않습니다」 —
     **but** cover revives if, for **5 years** from the 보장개시일, there is no further
     diagnosis (routine screening excluded) or treatment for it: 「「중대한 암 보장개시일」부터
     5년이 지난 이후에는 보장하여 드립니다」 [S1 제7조⑥, 별표1 주5]. The identical five-year
     revival applies to 장기요양상태 [S1 별표1 주6].
- **감액기간 (reduced-benefit period).** Two designs are in the sources, and they differ:
  - [S1] and [S2] reduce **only for breast cancer, only in the first policy year**, and by
    **half**: 50% 선지급형 pays 25%, 80% 선지급형 pays 40%, with the death benefit's complement
    rising to 75% and 60% [S1 별표1] [S2 별표1]. This is the lineal descendant of the 180-day
    breast-cancer 부담보 imposed across the market from 2008 [R1].
  - [S4]'s GI product reduces **every** trigger in the first policy year, again by half —
    보험가입금액의 25% / 40% / 50% for the 50% / 80% / 100% forms respectively, against 50% /
    80% / 100% thereafter [S4]. The single carve-out runs the other way: a first-year 중대한
    화상 및 부식 claim on the 17대보장형 is paid at the **post-first-year** rate [S4].
  - [S5] records a third pattern at 오렌지라이프 — 「보험가입금액의 100%를 「건강진단보험금」
    으로 선지급 (단, 1년미만 50%)」 [S5] — the same halving.
- **No survival period anywhere** [R1]; see §3.

### 12. 납입면제 (premium waiver)

- [S1] waives all future 기본보험료 on **either** of two events during the premium-paying
  period: (1) a disability state of **50% or more** on the 장해분류표, from one accident or one
  non-accidental cause across several body parts; or (2) **any CI/LTC보험금 지급사유** [S1
  별표1 주4, 제7조]. Because a CI event triggers the waiver, the waiver and the acceleration
  fire together in essentially every CI claim: on this chassis the waiver is not an independent
  decrement.
- [S3]'s universal-life version splits the two thresholds, waiving on **50%–80%** disability or
  a CI event, and terminating the contract at **80% or more** disability — because on that
  product an 80% disability is itself a death-benefit trigger [S3].
- [S4]'s GI product widens the waiver well beyond the acceleration: it fires on a 50%+
  disability **or** on diagnosis of 암 **including 특정암** (breast and prostate, which are
  *not* accelerated on that product), 뇌출혈, 급성심근경색증, 중증질환, 중대한 화상 및 부식,
  or a 중대한 수술 [S4]. Explicitly excluded from the waiver: 기타피부암, 갑상선암 (other than
  중증갑상선암), 대장점막내암 and 비침습방광암 [S4]. [R11] advertises **25** waiver triggers on
  삼성생명's GI product — the waiver has become a competitive feature in its own right.
- Where the waiver fires because of a CI event, [S4] computes the reserve on the
  post-acceleration basis: 「「선지급 진단보험금」 발생 이후 기준의 책임준비금을 계산」 [S4].

### 13. GI보험 — the code-based answer, and the 유병자 market

- **The name.** GI is not a regulatory category. [R1] records its origin as practitioner
  shorthand: 「보험상품 실무자들은 일반적인 CI(Critical Illness) 상품과 달리 이 상품은
  GI(General Illness)라고 별도로 구분하기도 함」 [R1]. Foreign-owned insurers had adopted the
  design first, because their agents were used to selling on ICD codes and could not adapt to
  definition-based selling [R1].
- **The mechanic.** GI replaces the 약관 정의 방식 with the KCD code: a diagnosis carrying a C
  code is 암, full stop; 뇌출혈 and 급성심근경색증 are their code ranges [R9] [R11] [S4]. The
  acceleration structure, the whole-life chassis and the residual death benefit are unchanged.
  [S5] captures the pitch in one line from 동양생명: 「진단받은 질병코드를 통해 보험금을
  지급함으로써 보험금 지급기준을 CI보험 대비 완화함」 [S5].
- **What GI gives up.** Two things, and a model should not assume GI simply dominates CI:
  1. GI's cerebrovascular scope is often **narrower** — several GI products cover 뇌출혈
     (I60–I62) only and leave 뇌경색 to a rider, where CI's 중대한 뇌졸중 covers I60–I63 but
     behind the 25% gate [R9] [S4] [S5].
  2. GI's headline diseases are fewer. [S4]'s menu is explicit: 암보장형, 2대보장형 (뇌출혈,
     급성심근경색증), 3대보장형, and only the **17대보장형** reaches the full CI-era list
     including the 중증질환 group and the four 중대한 수술 [S4].
- **[S4]'s 17대보장형 scope, quoted**: 「'중증질환'은 '말기신부전증', '말기간질환',
  '말기폐질환', '중증재생불량성빈혈', '중증루프스신염', '중증세균성수막염', '루게릭병
  (근위축측삭경화증)', '다발경화증' 및 '원발성폐동맥고혈압'을 말합니다」 [S4]. Note that the
  four 중대한 수술 survive into GI **unchanged** — GI de-defines diseases, not surgeries [S4].
- **Premium relationship.** [R9] reports CI as running about **2%** dearer than GI for
  identical cover, on the strength of CI's wider cerebrovascular scope, and adds that newer GI
  products often reverse the ordering. That is a secondary claim from a 2020 trade article and
  is `[unverified]`; no retrieved primary document prices a CI and a GI product on a comparable
  basis.
- **간편심사 (simplified underwriting) is a different axis, not the same one.** GI relaxes the
  *benefit trigger*; 간편심사 relaxes the *underwriting*. [R2] gives the taxonomy from a
  금융감독원 보도자료 of 2013-05-15:

  | Product | Who may buy | What is underwritten |
  |---|---|---|
  | 일반심사 | 표준체, usually to age 60 | cancer, hypertension, diabetes etc.; **5 years** of treatment history |
  | **간편심사** | 표준체 + some sub-standard, usually to **75** | disease history and **2 years** of treatment history; some named conditions (고혈압, 당뇨병) not asked at all |
  | 무심사 | anyone | nothing |

- The Korean 유병자 market's history is a cautionary one [R2]: 금호생명's 2007 무심사
  정기/종신보험 (가입연령 60–80 by TM, 50–80 by agent; 가입금액 100만–3,000만원) was sold
  in practice to the sick — 「설계사들이 무심사보험 판매를 위해 병원 암센터나 일반병원 병실로
  가서 환자들을 대상으로 판매하였다는 설도 있음」 — and its loss experience poisoned the whole
  category for five years. It was **라이나생명's 2012년 7월 실버암보험**, waiving only the
  hypertension and diabetes questions for lives aged **61 and over**, that made simplified
  underwriting work; the entire market copied it within a year [R2]. 금융감독원 required a 5%
  premium discount for standard lives on it, delivered through the expense loading [R2].
- **CI has been sold into that market too, and it failed.** [R2] records the **당뇨CI보험** — a
  가입한정형 product open only to diabetics without complications and with **HbA1c ≤ 8%**,
  paying on the diabetic complications 뇌졸중, 말기신부전, 실명 and 족부절단. Life-insurer
  version: 가입한도 ₩10,000,000–30,000,000 (1천만–3천만원), 가입연령 30–60, FC channel;
  non-life version: ₩5,000,000–20,000,000, ages 20–55, home-shopping and TM. It could
  not find enough eligible lives and was withdrawn [R2].
- The KLIA cross-section [S5] shows the modern hybrid: AIA생명's 백세시대 꼭하나 건강보험 runs
  a **1형 (간편심사형) for ages 40–75** beside a **2형 (일반심사형) for ages 30–65**, on a
  10-year renewable term to age 100, with three underwriting questions [S5].

### 14. Premiums — the published rate cards

**[S4], 미래에셋생명 건강담은 GI종신보험(무)1904, monthly premium, 보험가입금액 ₩100,000,000
(1억원), 20년납, 월납, 고액계약할인 적용, rates as at 2019-08** — the fullest published grid
found. `[기본환급형]`, in won [S4]:

| Form / menu | 남30 | 남35 | 남40 | 여30 | 여35 | 여40 |
|---|---|---|---|---|---|---|
| **50% 선지급형** 암보장형 | 221,480 | 249,900 | 284,200 | 191,100 | 214,620 | 242,060 |
| 50% 2대보장형 | 214,620 | 243,040 | 276,360 | 187,180 | 211,680 | 239,120 |
| 50% 3대보장형 | 231,280 | 260,680 | 295,960 | 198,940 | 224,420 | 252,840 |
| 50% 17대보장형 | 241,080 | 273,420 | 311,640 | 203,840 | 229,320 | 258,720 |
| **80% 선지급형** 암보장형 | 232,260 | 262,640 | 297,920 | 198,940 | 223,440 | 250,880 |
| 80% 2대보장형 | 222,460 | 250,880 | 285,180 | 193,060 | 217,560 | 246,960 |
| 80% 3대보장형 | 247,940 | 279,300 | 316,540 | 212,660 | 238,140 | 267,540 |
| 80% 17대보장형 | 263,620 | 297,920 | 338,100 | 219,520 | 245,980 | 276,360 |
| **100% 선지급플러스형** 암보장형 | 294,000 | 332,220 | 379,260 | 250,880 | 282,240 | 318,500 |
| 100%+ 2대보장형 | 281,260 | 318,500 | 362,600 | 244,020 | 275,380 | 312,620 |
| 100%+ 3대보장형 | 313,600 | 353,780 | 401,800 | 267,540 | 300,860 | 339,080 |
| 100%+ 17대보장형 | 333,200 | 376,320 | 428,260 | 276,360 | 310,660 | 350,840 |

and the `[해지환급금이 적은 유형]` grid on the same basis [S4]:

| Form / menu | 남30 | 남35 | 남40 | 여30 | 여35 | 여40 |
|---|---|---|---|---|---|---|
| 50% 암보장형 | 196,000 | 221,480 | 253,820 | 169,540 | 190,120 | 214,620 |
| 50% 2대보장형 | 190,120 | 215,600 | 245,980 | 165,620 | 187,180 | 211,680 |
| 50% 3대보장형 | 204,820 | 232,260 | 265,580 | 177,380 | 198,940 | 225,400 |
| 50% 17대보장형 | 215,600 | 245,000 | 281,260 | 181,300 | 204,820 | 231,280 |
| 80% 암보장형 | 205,800 | 233,240 | 266,560 | 177,380 | 197,960 | 223,440 |
| 80% 2대보장형 | 196,980 | 223,440 | 254,800 | 170,520 | 193,060 | 218,540 |
| 80% 3대보장형 | 220,500 | 249,900 | 284,200 | 189,140 | 211,680 | 239,120 |
| 80% 17대보장형 | 235,200 | 267,540 | 306,740 | 196,000 | 219,520 | 247,940 |
| 100%+ 암보장형 | 260,680 | 294,980 | 337,120 | 222,460 | 249,900 | 282,240 |
| 100%+ 2대보장형 | 248,920 | 282,240 | 322,420 | 214,620 | 243,040 | 276,360 |
| 100%+ 3대보장형 | 278,320 | 315,560 | 360,640 | 237,160 | 267,540 | 302,820 |
| 100%+ 17대보장형 | 296,940 | 338,100 | 388,080 | 245,980 | 277,340 | 313,600 |

**What falls out of these 96 cells**, computed here and stated as arithmetic on [S4]:

- **Price of the acceleration fraction.** Holding age, sex and menu fixed, the 80% form costs
  **2.8–9.4%** more than the 50% form and the 100% form **29.6–38.2%** more, over all 96
  cells. The step widens with the menu: the narrowest 80 : 50 step is ×1.0278 (여35 / 2대보장형
  / 기본환급형) and the widest ×1.0935 (남30 / 17대 / 기본환급형); the 100 : 50 step runs from
  ×1.2959 (여30 / 2대 / 저해지) to ×1.3821 (남30 / 17대 / 기본환급형). At 남40 / 17대보장형 /
  기본환급형: 311,640 → 338,100 (×1.085) → 428,260 (×1.374). At 남30 /
  17대보장형: 241,080 → 263,620 (×1.093) → 333,200 (×1.382). The 100% jump is much larger than
  the 50 → 80 step because on that form the death benefit is extinguished and replaced by the
  30% 유족위로금 — it is a different benefit, not a re-weighting.
- **Price of the disease menu.** At 남40 / 50% / 기본환급형, going 2대 → 암 → 3대 → 17대 runs
  276,360 → 284,200 → 295,960 → 311,640, a spread of only **12.8%** across the whole menu. The
  three headline diseases carry almost all the cost; the fourteen additional conditions in the
  17대 menu add about **5.3%** over the 3대 menu.
- **Sex.** Female premiums run **0.808–0.872** of male on the same cell — the extremes being
  0.808 at 남40/여40 / 100% / 17대 / 저해지 and 0.872 at 남30/여30 / 50% / 2대 / 기본환급형;
  at 남40 / 여40 / 17대보장형 / 50%, 258,720 / 311,640 = **0.830**.
- **Age slope.** 남 30 → 40 on 17대 / 50% is 241,080 → 311,640 = **×1.293** over ten years, a
  compound 2.6% a year — flat, because a 20-year-pay whole-life premium is dominated by the
  savings element.
- **The 해지환급금이 적은 유형 discount** is **9–12%**: at 남40 / 17대 / 50%,
  281,260 / 311,640 = 0.903; at 남30 / 암보장형 / 50%, 196,000 / 221,480 = 0.885.

**[S3], KDB생명 무배당 베스트유니버셜CI보험, 2011-01.** The 해지환급금 illustrations disclose
the premium exactly, since they tabulate 납입보험료 by elapsed duration. Basis: 주보험
₩100,000,000 (1억원) plus (무)CI플러스추가보장특약 ₩10,000,000 (1,000만원), 특약 80세만기,
20년납, 월납 [S3]:

| Illustration | 3개월 납입보험료 | implied monthly premium |
|---|---|---|
| 50% 선지급형, 남자 40세, 1억원 | ₩827,100 | **₩275,700** |
| 50% 선지급형, 여자 40세, 1억원 | ₩640,200 | **₩213,400** |
| 80% 선지급형, 남자 40세, 9,000만원 | ₩828,300 | **₩276,100** |
| 80% 선지급형, 여자 40세, 9,000만원 | ₩641,400 | **₩213,800** |

(The 80% illustrations use a 9,000만원 main contract because that is the form's maximum — see
§16 — so the two columns are not a like-for-like acceleration comparison.) Female/male ratio at
age 40: 213,400 / 275,700 = **0.774**, close to [S4]'s 0.83 eight years later.

**[S3]'s 보장위험별 연간보험료 and 보험료지수** — the statutory comparison disclosure, on a
basis of 월납, 남자 40세 [S3]:

| Product / benefit | 연간보험료 | 기준보험금 | 보험료지수 |
|---|---|---|---|
| **50% 선지급형**, CI 진단 | ₩165,419 | 1,000만원 | 130.9% |
| 50% 선지급형, CI 진단 전 사망 (80%+ 장해 포함) | ₩79,002 | 1,000만원 | (same) |
| 50% 선지급형, CI 진단 후 사망 | ₩82,715 | 1,000만원 | (same) |
| **80% 선지급형**, CI 진단 | ₩164,025 | 1,000만원 | 130.1% |
| 80% 선지급형, CI 진단 전 사망 | ₩78,336 | 1,000만원 | (same) |
| 80% 선지급형, CI 진단 후 사망 | ₩82,019 | 1,000만원 | (same) |

**This is the most useful single table in the file for a pricing model.** The three components
of the 50% form sum to ₩327,136 per 1,000만원 of 기준보험금, of which the CI acceleration is
₩165,419 — **50.6%**. Scaling by ten to the illustration's 1억원 basis gives ₩3,271,360 a year
against the illustration's actual first-year 납입보험료 of ₩3,308,400, a residue of ₩37,040
attributable to the 1,000만원 CI플러스 rider. The disclosure is internally consistent, and it
says plainly that **on a 50% acceleration at male 40, half the risk cost is the CI benefit and
half is the death benefit.** 보험료지수 130.9% means the office premium is 1.309× the
표준순보험료 computed on the 금융감독원's prescribed rates and interest.

The definitions the disclosure uses, quoted from [S3]: 연간보험료 is 「1년동안 위험보장을
받는데 필요한 영업보험료」 and is meaningful only for comparing carriers, 「납입보험료와
직접적인 관계가 없습니다」; 보험료지수 is the ratio of the product's premium to the
표준순보험료 「금융감독원이 정하는 위험률 및 이율을 적용하여 산출한 보험금 지급을 위한
보험료」 [S3].

**Discounts and loadings.**

- **고액계약할인** — a banded discount on the main-contract premium. [S3], 2011:
  3,000만–4,900만원 **1.0%**; 5,000만–9,800만원 **2.0%**; 1억–1억9,500만원 **3.0%**;
  2억–2억9,600만원 **5.0%**; 3억원 이상 **6.0%** [S3]. [S4], 2019, is shallower:
  7,000만원 미만 none; 7,000만–1억원 미만 **1%**; 1억–2억원 미만 **2%**; 2억원 이상 **3%** —
  and it creates dead bands where a policy may not be written at all (6,900만–7,000만,
  9,900만–1억, 1억9,800만–2억) [S4]. [S5] records ABL생명 discounting **3~4%** of the
  영업보험료 on contracts of 1억원 or more, and 동양생명 discounting above 5,000만원 [S5].
- **건강체할인 (preferred risk).** [S4]'s 건강인우대특약(무)1904 gives a discount on the main
  contract where the life satisfies **all three**: 직전 1년간 비흡연; 수축기 혈압
  **110–139 mmHg**; **BMI 20.0–27.9 kg/m²**. 가입나이 20–60. It may be applied at the proposal
  on the insurer's or an external medical result, or later during the policy term on a fresh
  medical [S4]. **The discount percentage is not published**, which is the one significant hole
  in [S4]'s otherwise complete rate disclosure.
- **효도특약** — 2% of the office premium (riders included) where the insured is the
  policyholder's (or spouse's) parent aged 50 or over and the beneficiary is the policyholder
  or the insured [S4].
- [S3] notes that where a **특별조건부특약 (할증보험료법)** applies, the substandard loading is
  added to the main-contract premium **before** the high-sum-assured discount is taken [S3].

### 15. Surrender value, the 무·저해지 forms, and the crediting rate

- **The suppressed-surrender-value design reached CI early.** [S2], in force 2017-07-01, offers
  two grades, and states the rule in terms:

  > 「'30% 저해지환급형' 및 '50% 저해지환급형'의 계약이 보험료 납입기간 중 … 해지될 경우의
  > 해지환급금은 '30% 저해지환급형'의 경우 '기본형' 해지환급금의 **30%**에 해당하는 금액으로
  > 하며, '50% 저해지환급형'의 경우 '기본형' 해지환급금의 **50%**에 해당하는 금액으로
  > 합니다. 다만, 보험료 납입기간이 완료된 이후 계약이 해지되는 경우에는 '기본형'의
  > 해지환급금과 동일한 금액으로 합니다.」 [S2]

  A carve-out worth noting for the model: the suppression does **not** apply once a
  CI/LTC event has occurred — the clause is expressly conditioned on 「제7조 … 제2호의
  CI/LTC보험금 지급사유가 발생하지 않은 경우」 [S2]. So a post-acceleration surrender
  gets the full 기본형 value.
- The step at 납입완료 is a **cliff, not a curve**, and it is the whole design: [S2] says the
  purpose is 「'기본형' 대비 적은 해지환급금을 지급하는 대신 '기본형'보다 저렴한 보험료로
  종신보험을 가입할 수 있도록 한 상품」 [S2].
- [S4] rebrands the same thing as **해지환급금이 적은 유형**, priced 9–12% below the
  기본환급형 (§14), and adds the same carve-out — the reduced value applies only 「「선지급
  진단보험금」 지급사유 발생 전 납입기간 동안」 [S4]. [S5] records 삼성생명's version as a
  **저해지 30%형** [R11] and 동양생명's 해지환급금일부지급형 as up to **30%** cheaper than the
  표준형 [S5]; a Chubb 종신 brochure retrieved incidentally in this session describes a
  「해지환급금 일부지급형」 paying **50%** of the 표준형 value in the paying period, reaching a
  환급률 of about 100% at 납입완료 [unverified — that brochure is for a non-CI product and is
  not listed as a source here].
- **[S4]'s own surrender illustration.** The brochure's chart is captioned 「30세 남성이 월
  127,000원의 보험료를 납입 완료한 경우」 on the basis 「30세, 남성, 가입금액 5천만원, 20년납,
  해지환급금이 적은 유형, 2대 보장형, 100% 선지급 플러스형」, and prints three 해지환급금
  values with three 원금 대비 환급률 figures: **₩14,217,500 (49.1%)**, **₩30,290,000 (99.4%)**
  and **₩44,569,500 (146.2%)**, against x-axis labels 1년 / 19년 / 20년 / 30년 / 40년 [S4].
  Checking the ratios against 20-year cumulative premiums of ₩127,000 × 12 × 20 = ₩30,480,000:
  30,290,000 / 30,480,000 = 99.4% and 14,217,500 / 28,956,000 (19 years) = 49.1%, so the
  mapping is 19년 → ₩14,217,500, 20년 → ₩30,290,000 and 40년 → ₩44,569,500, with the 1년 and
  30년 points unlabelled in the extraction. The **doubling of the surrender value across the
  final premium payment** is exactly the 저해지 cliff. The mapping is arithmetic inference from
  the printed ratios, not a printed table, and is flagged as such.
- **[S3]'s 해지환급금 tables** are printed in full and need no inference. 50% 선지급형, 남자
  40세, 주보험 1억원, 20년납, 월납, at the January-2011 적용이율 of 4.5% [S3]:

  | 경과 | 납입보험료 | 해지환급금 | 환급율 |
  |---|---|---|---|
  | 3개월 | 827,100 | 1,075 | 0.1% |
  | 1년 | 3,308,400 | 4,300 | 0.1% |
  | 2년 | 6,616,800 | 2,010,947 | 30.4% |
  | 3년 | 9,925,200 | 4,798,777 | 48.3% |
  | 5년 | 16,542,000 | 10,572,754 | 63.9% |
  | 7년 | 23,158,800 | 16,627,469 | 71.8% |
  | 10년 | 33,084,000 | 24,792,283 | 74.9% |
  | 20년 | 66,168,000 | 59,167,014 | 89.4% |
  | 30년 | 66,168,000 | 78,158,981 | 118.1% |
  | 40년 | 66,168,000 | 99,689,584 | 150.7% |

  The female-40 table on the same basis runs 28.1% / 47.5% / 64.5% / 73.3% / 77.6% / 96.6% /
  133.5% / 178.6% at the same durations, on a monthly premium of ₩213,400 [S3]. **This is a
  기본형 pattern, not a 저해지 one** — the value is near-nil for the first year because of the
  universal-life monthly-deduction structure, then climbs smoothly. It is the shape a
  `저해지환급형` product replaces with a cliff.
- **The surrender-value formula**, stated by [S3]: 「보험료 계산시 적용한 위험률로 산출한
  순보험료식 책임준비금에서 **미상각신계약비(해지공제액)**를 공제한 금액을 해지환급금으로
  지급합니다」 [S3]. The statutory cap on that 해지공제액 — the 표준해약공제액 in the
  보험업감독규정/시행세칙 — could not be retrieved this session and is left to
  `_research/regulatory-actuarial.md`.
- **Crediting rate.** [S1] credits the 계약자적립금 at the **공시이율**, with a two-tier
  **최저보증이율**: 「계약일부터 10년 이하의 경과기간에 대하여는 연복리 **1.5%**로 하고,
  10년을 초과하는 경과기간에 대하여는 연복리 **0.5%**로 합니다」 [S1 제36조]. The 약관's own
  worked examples make the mechanic concrete: a contract of 2017-01-01 valued at 2022-01-01
  with a 공시이율 of 0.1% accumulates at 1.5%; the same contract at 2032-01-01 accumulates at
  0.5% [S1].
- The contrast with [S3] is the single most striking interest-rate datapoint in this file:
  KDB생명's 2011 CI product carried a **flat 연복리 4.0%** 최저보증이율 and an 적용이율 of
  **4.5%**, set by a published formula
  「신공시기준이율Ⅹ(%) = A1×10% + (A2 + 0.5%)×50% + (A3 + 0.5%)×40%」 where A1 is the
  운용자산이익률 and A2, A3 are three-month weighted moving averages of the 국고채 and 회사채
  yields, with the 조정율 capped at 20% [S3]. Eight years later the guarantee is 1.5% falling
  to 0.5% [S1]. Any CI in-force projection has to carry that guarantee-rate stratification.
- **예정이율 (pricing rate).** [S3] states it directly for the protection element:
  「무배당 베스트유니버셜CI보험의 보장부분에 적용한 예정이율은 **연복리 4.0%**입니다」 [S3].
  [S4]'s 종신 vs 연금 comparison, prepared on the 생명보험협회 상품공시시행세칙 basis, states
  「종신보험의 예정이율(약 **2.75%**) 및 연금보험의 공시이율(약 2.52%)」 as at 2019 [S4]. No
  CI-specific 예정이율 later than [S3]'s 2011 figure was retrieved.
- **Expense structure.** [S1] names the components as 계약체결비용 and 계약관리비용, the latter
  split into 유지관련비용 and 기타비용, deducted as part of the 월대체보험료 [S1]; the
  추가납입보험료 carries its own 계약관리비용 deducted at payment [S1]. **No numeric expense
  loading is published in any document retrieved** — [S3]'s 예정사업비율 section explains the
  concept and its table did not extract. See gaps.

### 16. Contract mechanics

Drawn from [S1] unless stated; these are the general 약관 articles, and they follow the
생명보험 표준약관 pattern closely (see §19).

- **보험나이 (insurance age).** 「이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다」
  [S1 제26조①], computed as 「계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의
  끝수는 버리고 6개월 이상의 끝수는 1년으로 하여** 계산하며, 이후 매년 계약해당일에 나이가
  증가하는 것으로 합니다」 [S1 제26조②]. Where the month has no corresponding day, the last day
  of the month is the 계약해당일. The 약관's worked example: born 1980-01-20, joining
  2014-07-10 → 만 34년 5개월 20일 → **보험나이 34세**; joining 2014-12-10 → 만 34년 10개월
  20일 → **보험나이 35세** [S1]. The one exception is 제24조 (계약의 무효), where actual 만나이
  applies [S1 제26조①]. **This is the age basis `CI_KR_S` must use for pricing.**
- **가입나이.** [S3]: 만 15세 ~ 최고 **60세**, varying by sex and premium term [S3].
  [S4]: 만 15세 ~ 최고 **60세** [S4]. [R13]: 15–60 [R13]. **Invariant across the sources.**
- **가입한도**, [S3]: 50% 선지급형 **₩20,000,000–150,000,000** (2,000만–1억5,000만원);
  80% 선지급형 **₩10,000,000–90,000,000** (1,000만–9,000만원) [S3]. The 80% form's ceiling is
  lower precisely because the acceleration is larger — the insurer caps the accelerated amount,
  not the sum assured: 0.8 × 9,000만 = 7,200만 against 0.5 × 1억5,000만 = 7,500만원, i.e. the
  two forms are capped at almost the same **accelerated** exposure. [R1] records the market
  practice differently, at a 2억원 maximum with 1억6천만원 accelerated at 80% [R1].
- **보험기간 / 납입기간.** 보험기간 종신 [S3] [S4]. Premium terms, [S3]: 일시납,
  5·10·15·20년납, 55·60·65·70·80세납 [S3]. [S4] is wider: 5·10·15·20·25·30년납,
  55·60·65·70·75·80세납, with 5년납 and 10년납 available on the 기본환급형 only — the
  short pay periods are not offered on the 해지환급금이 적은 유형 [S4]. 납입주기 월납
  [S4]; [S3] adds 일시납.
- **자살면책 2년.** 「피보험자가 고의로 자신을 해친 경우」 is excluded, save that (가) an act
  in a state of 심신상실 is paid, and (나) 「계약의 보장개시일 … 부터 **2년**이 지난 후에
  자살한 경우에는 … 사망보험금을 지급합니다」 [S1 제10조]. **Two years, not three as in
  Japan, and not one as in the UK.** The other two exclusions are the beneficiary and the
  policyholder intentionally killing the insured, with the usual part-beneficiary carve-out
  [S1 제10조].
- **계약 전 알릴 의무 (contestability)** [S1 제19조]. Rescission or restriction is barred
  where: the insurer knew or negligently did not know; **1개월** has passed since it learned
  of the breach; **2년** has passed from the 보장개시일 without a claim event (**1년** for
  disease in a 진단계약); **3년** has passed from the contract date, unconditionally; the
  insurer accepted on submitted medical evidence and the claim arises from something recorded
  in it; or an intermediary obstructed or encouraged the misstatement. So Korea has a
  **two-limb** contestability window — 2 years claim-free, and a hard 3-year longstop —
  against Japan's single 2-year rule.
- **Grace and lapse.** Within the first **3년 (36회 납입)** the 기본보험료 must be paid when
  due; after that the contract may run on 월대체보험료 drawn from the 해지환급금 [S1 제29조].
  On non-payment the insurer must give a 납입최고(독촉)기간 of **14일 이상**, running from the
  day after the due date to the last day of the following month, and the contract is 해지 at
  its end [S1, 주요내용 요약서].
- **부활 (reinstatement)** within **3년** of the lapse, provided the 해지환급금 has not been
  taken; the insurer may decline or restrict cover on health, occupation or job type [S1].
  Reinstatement **restarts the 90-day 중대한 암 보장개시일 and the 2-year suicide clock**, both
  of which are drafted 「계약일(부활(효력회복)일)부터」 [S1 별표1 주1] [S1 제10조].
- **청약철회 15일** from receipt of the policy, and not at all after 30 days from the proposal
  or on a 진단계약 [S1]. **계약취소 3개월** where the 약관 was not delivered, its important
  terms were not explained, or the proposal was not signed [S1]. **계약의 무효** where a
  third-party death contract lacks the insured's written consent, where the insured is under 15
  or lacks capacity, or where the age was outside the permitted range [S1].
- **Claim timetable** [S1 제13조]: **3영업일** from receipt of complete documents; **10영업일**
  where investigation is needed; and where the insurer cannot meet that, it must notify the
  reason, the expected date and the **가지급제도** (advance of up to **50%** of the estimated
  benefit), with the expected date set within **30영업일** except where there is litigation, a
  분쟁조정신청 to the 금융분쟁조정위원회 or 소비자분쟁조정위원회, or certain investigations.
- **Claim documents** for a CI claim [S1 제12조]: 청구서, 사고증명서 (진단서 with the disease
  name, 수술확인서, **진료기록부 including 검사기록지**, 장기요양인정서 as applicable), 신분증.
  The requirement to produce the underlying test records, not merely a certificate, is what
  makes the ADL and enzyme gates operable — and is what [R16] shows a loss adjuster working on.

### 17. The pricing basis — a disclosed CI morbidity table

[S3] publishes the product's **예정위험률**, per annum, by sex at ages 20, 40 and 60. This is
the only disclosed Korean CI morbidity basis found in this session and it is worth reproducing
exactly [S3]:

| 예정위험률 (연) | 남20 | 남40 | 남60 | 여20 | 여40 | 여60 |
|---|---|---|---|---|---|---|
| 예정 경험 사망률 | 0.00051 | 0.00068 | 0.00290 | 0.00027 | 0.00068 | 0.00290 |
| 중대한 암 발생률 | 0.000144 | 0.001023 | 0.011063 | 0.000291 | 0.002220 | 0.006010 |
| 중대한 급성심근경색증 발생률 | 0.000027 | 0.000589 | 0.004371 | 0.000009 | 0.000148 | 0.001814 |
| 중대한 뇌졸중 발생률 | 0.000038 | 0.000907 | 0.003999 | 0.000040 | 0.000399 | 0.002764 |

**Health warning on the mortality row.** The female values at 40 and 60 extract identical to
the male values (0.00068 and 0.00290), which is not plausible for a Korean life table and is
almost certainly a column-merge artefact of the PDF extraction. The three morbidity rows are
fully differentiated by sex and are treated as sound; **the female mortality rates at 40 and
60 are `[unverified]`** and must not be used.

What the morbidity rows say, computed here from [S3]:

- **CI incidence dominates mortality on this chassis.** At male 40 the three CI rates sum to
  0.002519 against a mortality of 0.00068 — the CI decrement is **3.7×** the death decrement.
  At male 60 they sum to 0.019433 against 0.00290, a ratio of **6.7×**. That is why the CI
  benefit takes half the risk premium at a 50% acceleration (§14) despite paying only half the
  sum assured.
- **The sex crossover in 중대한 암 is the product's defining experience feature.** At 40 the
  female rate (0.002220) is **2.17×** the male (0.001023); at 60 it is **0.54×** (0.006010 vs
  0.011063). The young-female excess is breast and thyroid cancer — exactly the exposure that
  broke the 2002 pricing [R1] — and it is the reason breast cancer alone carries a first-year
  halving in [S1].
- **중대한 급성심근경색증 is the most male-skewed**: 4.0× at 40 (0.000589 / 0.000148) and 2.4×
  at 60. **중대한 뇌졸중** is close to unisex at 20 and runs 2.3× male at 40, 1.45× at 60.
- **Age slope.** Male 중대한 암 rises **×7.1** from 20 to 40 (0.001023 / 0.000144) and
  **×10.8** from 40 to 60 (0.011063 / 0.001023) — the cancer log-slope *steepens*. Male AMI
  rises ×21.8 then ×7.4; male stroke ×23.9 then ×4.4, both flattening. These are slopes a
  `[std]` CI incidence construction for `CI_KR_S` should reproduce.
- **What the rates are not.** They are 예정위험률 — pricing rates carrying a safety margin, not
  best-estimate experience. [R1] records the margin regime around them: 안전할증 on the
  기초발생률 was capped at **30%** in the early 2000s, raised to **50%** by the 2015
  보험산업 경쟁력 강화 로드맵, and the cap was **removed from 2017** [R1]. Any best-estimate
  basis derived from [S3] is a `[std]` adjustment and must say so.

**Two Korea-specific pricing rules from [R1]**, both of which bear on how these rates were
built:

1. **Overlap between CI causes must be reflected.** Because the benefit is payable once only,
   overseas practice ignores the correlation between CI causes for rate stability; Korea's
   supervisor required it to be reflected — 「국내의 경우 위험률과 담보 간 일치에 대한 규제가
   강하고 … CI 질병들 간 중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로
   검증받고 사용하였다」 [R1]. So a Korean CI rate is a *first-event* rate across a competing-
   risk set, not a sum of marginal incidences.
2. **No survival period.** See §3. The rates therefore include lives who die of the CI cause
   without a separate diagnosis event, which [R1] notes the underlying diagnosis statistics do
   not capture — an acknowledged upward bias in the exposure that the rate must absorb [R1].

**Rate-change rights.** [S3] states the standard Korean mechanic for a 제3보험 risk rate: the
insurer may, from **5 years** after the contract, obtain 금융위원회 approval to change the
예정위험률; where the change raises the premium or the reserve, the insurer applies the
increase by **reducing the benefit or the sum assured** unless the policyholder pays the
increase over the remaining premium term (or in a lump sum where paid up) [S3]. That is a real
optionality in the liability and it should be named in the technical notes even if the model
does not exercise it.

**Historical context for the rates** [R1]: the **제4회 경험생명표** took effect in **2002** —
the same year CI launched — and reduced both mortality and cancer incidence, which is precisely
what motivated life insurers to look for a product whose margin did not depend on falling
mortality. Industry 위험률차익률 in that period, from 금융감독원's 금융정보통계시스템 [R1]:

| | FY03 | FY04 | FY05 | FY06 | FY07 |
|---|---|---|---|---|---|
| 전체 | 22.8% | 19.4% | 14.9% | 12.8% | 15.9% |
| 국내사 | 20.4% | 17.1% | 12.8% | 11.2% | 15.2% |
| 외국계 | 33.9% | 33.2% | 26.6% | 20.5% | 19.4% |

and cancer-cover 위험률차익률 alone went negative and stayed there — −8.9% (FY05), −9.9%,
−14.0%, −20.3%, −23.9% (FY09) [R1]. The 경험생명표 review cycle for life business was **3
years** until a 2011-01-24 시행령 amendment moved it to **5 years** [R1].

### 18. The dispute record

CI보험 is, by a distance, the most litigated and complained-of life product in Korea, and the
reason is structural rather than behavioural: the 약관 pays on a *severity state* while the
policyholder experiences a *diagnosis*. [R1] anticipated it in 2018 —
「지급심사 담당자들에 따르면 CI보험금 부지급률이 일반적인 건강보험 상품보다 몇 배로 높다고
인지하고 있다」 [R1] — though it publishes no denial-rate figure, and no such figure was found
in this session from any source.

What the retrieved record actually contains:

- **[R5], 서울중앙지방법원 2016-01-14, 2014가단242567.** The cleanest judicial statement. A
  mucosa-confined colorectal carcinoma is **암** for the rider (KCD C18) and **not 중대한 암**
  for the main contract, because the 침윤파괴적 증식 test is not met. CI claim of ₩53,000,000
  rejected; rider claims of ₩13,000,000 allowed. The court construed the definition on its
  terms rather than resolving the ambiguity against the drafter.
- **[R10], 2015.** A ten-year policyholder with 지주막하출혈 and surgery, declined because no
  disability was diagnosed.
- **[R6], 2023.** Two declined stroke claims: a confirmed 지주막하출혈 with ICU admission below
  the 25% rating, and a 뇌경색증 with documented cognitive decline below it.
- **[R16], undated.** A 뇌경색 claim on a 2006 policy (₩35,000,000 main contract, 50%
  acceleration = ₩17,500,000), declined for want of a permanent deficit and then paid in full
  once a 후유장해진단서 recorded a permanent ADL restriction. The adjuster's stated working
  rule — six months of rehabilitation plus a ≥25% ADL rating — is practice, not 약관.
- **[R7], 2026-04-06.** A 뇌경색 claimant fifteen years into a CI policy, using a mobility aid,
  declined on the ground that daily living remained possible at some level.
- **[R8], 2020.** Mis-selling at the point of sale, with an agent's account that carriers
  treated explaining the 중대한 condition as unnecessary because it is in the 약관. Against
  that, the article records **금융감독원 as having found no particular mis-selling problem** in
  the CI sales process — the only regulator statement on CI recovered in this session.

Two observations for the product documents:

1. **All four claim narratives are stroke claims but one.** That is what the arithmetic in §7
   predicts: the cancer and infarction definitions are narrow at the margin, but the stroke
   definition is narrow in the middle of the distribution, because most strokes leave the
   survivor independently mobile.
2. **The industry knew.** [R1] recommended standardisation in terms — 「질병 정의에 대한 회사
   간 경쟁을 지양하고 궁극적으로는 보험회사 공통의 표준화된 정의를 사용하여 … 혼란을 사전에
   방지할 필요가 있다. 해외 대부분의 나라에서는 보험회사가 표준화된 CI 질병의 정의를
   운용하도록 감독당국에서 규제하고 있다」 [R1]. The market's answer was not standardisation
   but GI: it removed the word rather than defining it.

### 19. The regulatory frame

- **표준약관 (standard policy conditions).** The 생명보험 표준약관 sits at
  보험업감독업무시행세칙 **[별표 15]**, issued by 금융감독원, and the 장해분류표 sits inside
  it. Every general article in [S1] follows that pattern — the 2-year suicide window, the
  1개월/2년/3년 contestability limbs, the 14-day 납입최고, the 3-year 부활, the
  3영업일/10영업일/30영업일 claim timetable, the 15-day 청약철회, the 가지급제도 — and [S1]
  별표3's 장해분류표 with its ADLs schedule is the 표준약관 table. **[별표 15] itself could not
  be retrieved this session** (see gaps), so the identification of [S1]'s general articles with
  the 표준약관 rests on their form, and is `[unverified]` as to the exact edition.
- **The 중대한 질병 definitions are not standardised.** No retrieved document identifies a
  supervisory standard wording for 중대한 암, 중대한 급성심근경색증 or 중대한 뇌졸중, and [R1]
  says in terms that Korea lacks what other jurisdictions have [R1]. What *is* standardised is
  the severity gate the stroke definition borrows — the 장해분류표's 신경계 item and its ADLs
  table. So the trigger has a regulated numerator and an unregulated denominator, which is a
  strange place to leave a product and is probably the deepest structural criticism of it.
- **제3보험** is 보험업법 제4조제1항제3호 — 상해보험, 질병보험, 간병보험 [R4]. See §1 for the
  licensing consequence.
- **IFRS17 계리가정.** [R3] is the binding constraint on any Korean CI cash-flow projection
  written on a 무·저해지 chassis, and CI is written on one. Its terms, from the 2024-11-07
  보도자료: the **로그-선형 모형** is the 원칙모형 for 무·저해지 lapse rates, converging to
  **0.1%** at 납입완료, with an ultimate post-completion rate of **0.8%**; any other model
  requires disclosure of the CSM, K-ICS and net-income differences against the 원칙모형 in both
  the audit report and the 경영공시, plus targeted 금융감독원 review; 단기납 종신보험 must
  assume **30% 이상** extra lapse at the bonus date; 실손 손해율 moves to 연령군단별
  analysis. Effective from the 2024 year-end close (손해율 by 2025 Q1); 할인율 realignment
  from January 2025, extending the 최종관찰만기 to **30년** over three years. Industry
  K-ICS effect estimated at about **−20%p** [R3].
- **Risk-rate revision.** From 5 years after issue, subject to 금융위원회 approval, with the
  increase taken out of the benefit unless the policyholder funds it [S3] — see §17.
- **Reserve basis.** [S3] states the surrender value as 순보험료식 책임준비금 less
  미상각신계약비 [S3]. The statutory 표준해약공제액 cap on that deduction, the 표준책임준비금
  basis and K-ICS treatment belong to `_research/regulatory-actuarial.md` and are not
  established here.

---

## Variation across carriers

The observed range is given wherever more than one document states the parameter. The product
spec's representative choices are justified against this table.

| Feature | Observed positions | Range / mode |
|---|---|---|
| Acceleration fraction | 50% [S1] [S2] [S3] [S4] [S5] [S6] [R13]; 80% [S1] [S2] [S3] [S4] [S5] [S6]; 100% [S4] [S5] [R11] [R14]; 30–80% policyholder-chosen [R1]; age-varying [R1] | **50%/80% is the settled pair**; 100% is a GI-era form |
| Residual death benefit after CI | complement of the fraction, floored at 105% of 계약자적립금 [S1]; floored at 110% [S3]; nil + 유족위로금 1%×30 [S4]; nil + 30% annuity [R14]; 30% [S5, 오렌지라이프] | complement is the rule; the 100% forms substitute a separate benefit |
| First-year reduction | breast cancer only, ×½ [S1] [S2]; all triggers, ×½ [S4] [S5]; none stated [S3] | **×½ where present** |
| 중대한 암 waiting period | 90일 [S1] [S2] [S3] [S4] | **no variation** |
| Other CI waiting period | none — cover from 계약일 [S1] [S2] [S3] [S4] | **no variation** |
| 장기요양상태 waiting period | 90일, waived where the cause is a 재해 [S1] | one source |
| Number of 중대한 질병 in the main contract | 8 (2002 launch, incl. surgeries) [R1]; 11 (2003) [R1]; 8 diseases + 4 surgeries + burn [S1] [S2]; 13 [R13]; 17 [S4] [R14]; 18 + 3 [R11]; "45 질병/수술" incl. riders [S5] | **8–17 in the main contract** |
| 중대한 수술 | the same four everywhere — CABG, 대동맥인조혈관치환, 심장판막, 5대장기이식 [S1] [S2] [S4] [S5] | **no variation** |
| 중대한 뇌졸중 gate | 장해지급률 **25% 이상** [S1] [S6] [R1] [R6] [R9] [R10] | **no variation** |
| 중대한 암 exclusions | 초기 악성흑색종 (≤T2aN0M0), C44, C61, C73, 대장점막내암, 제자리암, 경계성종양, 전암상태, pre-inception recurrence [S1]; older wording adds HIV-related malignancy and "초기갑상샘암" [S6] [R1] | the modern list is settled; HIV exclusion is a legacy item |
| LTC trigger | 노인장기요양 **1등급 or 2등급** [S1] [R11]; earlier private ADL/CDR definitions [R1] [S3] | public grades since 2008 |
| 가입나이 | 만 15세–60세 [S3] [S4] [R13] | **no variation** |
| 가입한도 | 50%형 2,000만–1억5,000만원; 80%형 1,000만–9,000만원 [S3]; 최대 2억원 [R1]; dead bands around discount thresholds [S4] | ceiling **9,000만–2억원** |
| 납입기간 menu | 일시납, 5/10/15/20년납, 55/60/65/70/80세납 [S3]; 5–30년납 in 5s, 55–80세납 [S4] | 5년납 to 80세납 |
| Surrender-value form | 기본형 [S3]; 30% 저해지 and 50% 저해지 [S2]; 해지환급금이 적은 유형 [S4]; 저해지 30%형 [R11]; 해지환급금일부지급형 up to −30% premium [S5] | **30%–50% of the 기본형 value in the paying period** |
| 저해지 premium discount | 9–12% [S4, computed]; "up to 30%" [S5, 동양생명]; "24% cheaper" [unverified, secondary] | **~10%–30%** |
| 최저보증이율 | 연복리 4.0% flat (2011) [S3]; 1.5% for 10 years then 0.5% (2019) [S1] | collapsed over the decade |
| 예정이율 | 4.0% (2011, protection element) [S3]; 약 2.75% (2019, 종신 illustration basis) [S4] | **2.75%–4.0%** |
| 기본보험금 floor multiple on 계약자적립금 | 105% [S1]; 110% [S3] | **105%–110%** |
| 고액계약할인 | 1/2/3/5/6% by band from 3,000만원 [S3]; 1/2/3% from 7,000만원 [S4]; 3–4% at 1억원 [S5]; from 5,000만원 [S5] | shallower over time |
| Preferred-risk discount | 건강인우대특약: 비흡연 1년, SBP 110–139, BMI 20.0–27.9, ages 20–60 [S4]; 건강인우대특약 named but unspecified [S1] | criteria published, **discount not published** |
| 납입면제 trigger | 장해 50%+ or any CI/LTC event [S1] [S2]; 장해 50–80% or CI event [S3]; 장해 50%+ or any of 암 incl. 특정암, 뇌출혈, AMI, 중증질환, 화상, 중대한 수술 [S4]; "25 triggers" [R11] | widening steadily |
| Trigger philosophy | 약관 정의 (CI) [S1] [S2] [S3] [S6]; KCD code (GI) [S4] [S5] [R9] [R11]; staged (SI) [R13]; wide-scope code (WI) [R12] | **four generations coexist** |

**What does not vary.** Six things are identical in every document retrieved and should be
treated as the product's fixed spine rather than as choices: (1) the CI benefit is an
**acceleration of the death benefit**, paid **once only** across all triggers, and the death
benefit is reduced by exactly what was paid; (2) the 중대한 암 waiting period is **90 days**
from 계약일 or 부활일 and applies to cancer alone; (3) 중대한 뇌졸중 requires a
**장해지급률 25% 이상** on the 표준약관 장해분류표's ADLs schedule; (4) 중대한
급성심근경색증 requires **all three** of typical chest pain, new characteristic ECG change and
newly raised cardiac enzymes including CK-MB, with all angina excluded and the covered code
**I21** alone; (5) the four 중대한 수술 are CABG, aortic graft replacement, heart-valve surgery
and five-organ transplantation, each requiring open surgery and each excluding the catheter
technique; (6) **no survival period** is required anywhere.

---

## Fetch failures and gaps

**URLs tried and not opened, or opened and unusable.** Roughly 45 distinct URLs were attempted
this session; about 28 returned usable text. The failures:

- `http://product.samsunglife.com/product/insu/family/univlivcare/insuPrdtUnivLivCareFeat.html?tloParam=bl_allinoneci` [S8] and its `https` form — **HTTP 503** on both. **What was lost**:
  the current product of the carrier that invented Korean CI. Its 가입나이, 가입한도, premium
  scale, 무해지/저해지 forms and exact disease list are absent; the 80% acceleration and the
  13-disease list attributed to it in §8 and the 45-item count in [S5] are `[unverified]`.
- `http://www.kyobo.co.kr/webdocs/view.jsp?screenId=SMMISNLM226` (교보생명
  (무)더든든한무배당교보통합CI보험 가입안내) — **DNS failure**, `getaddrinfo ENOTFOUND`.
  **What was lost**: 교보생명 is the carrier that put LTC on the CI chassis in 2008 [R1] and
  sells two CI/GI products per [S5]; none of its product parameters is sourced here.
- `http://inthenews3.mediaon.co.kr/news/article.html?no=11117` (「악성종양이 곧 '중대한 암'..
  금감원 "CI보험금 지급하라"」) — **DNS failure**. **What was lost**: this is the only lead
  found to a **금융감독원 분쟁조정** decision on 중대한 암. No 분쟁조정 결정례 is cited
  anywhere in this file, and the dispute record in §18 rests on one first-instance
  judgment [R5] and five secondary accounts.
- `https://abllife.co.kr/.../20210925_NP_걱정말아요CI통합종신보험(해지환급금일부지급형)2101.pdf`
  — the fetcher refused it: `maxContentLength size of 10485760 exceeded`. **What was lost**:
  the 2021 edition of [S1]/[S2]'s product family, which would have given a post-2020 CI 약관
  and a third generation of the surrender-value suppression. The 2019 [S1] and 2017 [S2]
  editions stand in its place, so this file's 약관 evidence is **five to nine years old**.
- `https://www.law.go.kr/법령/보험업법` — returned the page shell only, no statute text, exactly
  as the house brief warns. `https://www.law.go.kr/LSW/lsInfoP.do?...` returned a
  service-unavailable page ("접속자 증가"). **Recovered in part** through CaseNote's mirror
  [R4], but the 보험업법 article text in §1 and §19 is therefore paraphrase from a mirror, not
  quotation from the 국가법령정보센터.
- `https://www.insclaim.co.kr/19/8641083` and `https://www.insclaim.co.kr/19/11517849`
  (생명보험 표준약관, 보험업감독업무시행세칙 [별표 15]) — **HTTP 404** and **HTTP 404**.
  **What was lost**: the 표준약관 text itself. The identification in §19 of [S1]'s general
  articles with the 표준약관, and of [S1] 별표3 with the statutory 장해분류표, is inference
  from form and is `[unverified]`. The amendment history visible in search snippets
  (2018-03-02, 2018-07-10, 2019-12-20, 2020-07-31, 2020-10-16, 2021-07-01, 2022-02-16,
  2022-09-30, 2022-12-23, …) is **not used** anywhere above.
- `https://www.hankyung.com/article/2020071293331` (한국경제, 「생전에 사망보험금 先지급
  GI보험 잇따라」) — **HTTP 403**. This was the best lead to dating [S5]; [S5] remains undated.
- `http://www.insweek.co.kr/42496` (동양생명 수호천사 알뜰한통합GI보험(저해지환급형)) —
  **HTTP 503**. 동양생명's GI product appears only through [S5].
- `https://casenote.kr/대법원/2018다203395` — **HTTP 503**. **What was lost**: a Supreme Court
  authority on 약관 해석 and the 작성자 불이익의 원칙 (약관의 규제에 관한 법률 제5조제2항) as
  applied to a cancer definition. §18 therefore has no appellate authority in it, and the
  general Korean rule that an objectively ambiguous 약관 clause is construed against the
  drafter is **not** sourced to a retrieved judgment.
- `http://jeongeon.kr/insiter.php?design_file=1160.php&...` (법무법인 정언, 「CI보험의 약관상
  중대한 질병의 정의」) — **HTTP 503**.
- `https://easylaw.go.kr/CSP/CnpClsMain.laf?...` (찾기쉬운 생활법령정보, 금융감독원을 통한
  분쟁조정) — the page returned site navigation only, no body content. **What was lost**: the
  statutory description of the 금융분쟁조정 process, which [S1] 제13조 refers to.
- `https://www.lawinsider.com/ko/clause/중대한-뇌졸중의-정의-및-진단확정` — rendered, but the
  free view exposes a **single** sample clause with no insurer or product named, so it
  could not be used for cross-carrier wording comparison as intended.
- `https://lawinsider.com/ko/contracts/9SLRE7Bms1X` [S7] — rendered but **redacted**; see the
  source entry.

**Documents retrieved that turned out not to be CI products** (recorded so that a later pass
does not re-fetch them):

- `https://www.axa.co.kr/AsianPlatformInternet/doc/internet/public/CI_health_provision2107(B).pdf`
  — the filename says `CI_health_provision`, but the 240-page document is
  **「무배당 AXA생활비받는 건강보험(갱신형)(2107)」**, a renewable health product with no
  중대한 질병 definitions in it (the string 중대한 occurs only in 중대한 과실). Not used.
- `https://image.kebhana.com/cont/download/insdocument/provide/N02C14145_agree.pdf` — indexed by
  search as a 교보생명 CI 약관; it is in fact **한화손해보험 「한화 골드클래스 간병보험」
  약관**, revised 2023-07-01, 173 pages. Not used.
- `https://image.kebhana.com/cont/download/insdocument/provide/08L03014231_agree.pdf` — a
  35-page 삼성생명 약관집 whose product is not named in the extractable text and which contains
  no 중대한 질병 material. Not used.
- `https://www.idbins.com/pc/bizxpress/pdc/pop/pn/FWMALP0730.shtm` — indexed as a CI 가입예시;
  it is a **실손의료비** rate table (40세남, 합계보험료 ₩16,617/월). Not used, but noted
  because it is a genuine 실손 rate card and belongs to `_research/indemnity-medical.md`.

**Facts left `[unverified]`, and why:**

- **Any claim-denial or 부지급률 statistic for CI보험.** [R1] reports adjusters' perception
  that it runs "several times" the rate of ordinary health cover but publishes no number, and
  regulator or association statistic was found. This is the single largest quantitative hole in
  the file, and it bears directly on any lapse or claim-frequency assumption.
- **Any CI in-force or new-business series after 2004.** [R1]'s table stops at CY2004; the
  ~1.8 million-a-year peak is given as a sentence, not a series. 생명보험협회's
  월간생명보험통계 and 통계연보 index pages were seen in search results but the underlying
  tables were not retrieved, and in any case CI is not separately classified in the standard
  breakdowns. **The claim that CI has been displaced by 진단비 중심 건강보험 is qualitative
  throughout this file** — sourced to [R11], [R12] and [S5]'s product mix, never to a market
  share series.
- **삼성생명's current CI product parameters** — see [S8].
- **교보생명's and 한화생명's CI/GI product parameters** beyond [S5]'s one-line summaries.
- **The 건강인우대특약 discount percentage** [S4] — criteria published, discount not.
- **The 예정사업비율 table in [S3]** — the section header and the explanatory Q&A extract, the
  table itself did not. So **no numeric expense loading appears anywhere in this file**, and
  every expense assumption in `CI_KR_S` will be `[std]`.
- **Female 예정 경험 사망률 at ages 40 and 60 in [S3]** — extraction artefact; see §17.
- **[S5]'s publication date** — see the source entry.
- **[R11]'s "130% / 180% 선지급"** for 삼성생명 GI플러스종신보험. Percentages above 100% cannot
  describe a pure acceleration; whether they aggregate a rider, or express a multiple of a
  different base, is not established.
- **[R9]'s "CI is about 2% dearer than GI"** — a secondary comparison with no basis stated.
- **The identity of [S1]'s general articles with 보험업감독업무시행세칙 [별표 15]** — see the
  fetch failures above.
- **The Korean 표준해약공제액 cap** and the 표준책임준비금 basis — not attempted here; they
  belong to `_research/regulatory-actuarial.md`.
- **Reinsurance terms and CI lapse experience by duration.** [R1] gives one cession ratio
  (삼성생명, ~40%, 2002) and no lapse data at all. No Korean equivalent of a published
  protection-lapse table was found, so the lapse basis for `CI_KR_S` must be `[std]`,
  constrained by [R3]'s 무·저해지 log-linear standard model.

**Deliberate scope limits (not gaps):**

- 암보험 (`cancer.md`), 실손의료보험 (`indemnity-medical.md`), 간병보험 (`long_term_care`) and
  어린이보험 (`child.md`) are separate products with their own research files. The LTC material
  in §10 is here only because the LTC state is one of `CI_KR_S`'s acceleration triggers; the
  노인장기요양보험 grade statistics that an LTC incidence basis needs are not gathered here.
- 다중지급 (multi-pay) CI and Stage/Early CI riders are described in §2 and §8 for context,
  from [R1] and [R13], but `CI_KR_S` models the **single-payment acceleration** only. The
  structure — 7–8 disease groups, a second payment on a different group or a second cancer, a
  **3-year** waiting period on the second cancer, a maximum of three payments overseas — is
  recorded in [R1] and is available if the product is ever extended.
- 변액CI (variable CI) is out of scope; [R14] is cited for its GI benefit structure only, and
  the separate-account machinery belongs to `variable_annuity`.
- 당뇨CI보험 and the 유병자 market are described in §13 for completeness; `CI_KR_S` is a
  standard-underwriting product.
