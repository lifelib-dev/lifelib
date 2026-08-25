# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/endowment.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused ids are omitted, so gaps
in the numbering are normal and correct; on this product there happen to be none — every one
of the sixteen primary sources and all ten regulatory and actuarial references is cited by
`product-spec.md` or `technical-notes.md`, so S1–S16 and R1–R10 run unbroken. Access date
for all sources: 2026-08-20. No sources were newly added at drafting. Cross-product [REG-R#]
tags are listed in their own section at the end.

Six carriers are represented in the primary set: three that publish on both 養老保険 and 学資保険
([S2]–[S5], [S6]–[S9], [S13]–[S15]) and three that publish on 学資保険 alone ([S1], [S10]–[S12],
[S16]). That is why the 養老保険 evidence rests on three carriers and two full 約款 [S2] [S8]
while the 学資保険 evidence rests on all six. Company and branded product names appear in this
file and in `_research/endowment.md` and **nowhere else** in the library: in
`product-spec.md`, `technical-notes.md`, `model.md` and the model docstrings a carrier is
referred to by its [S#] tag alone.

---

## Primary product sources

(jplib-endowment-s1)=

### S1 — 第一生命保険, "５年ごと配当付こども学資保険普通保険約款" (policy conditions)

- Publisher: 第一生命保険株式会社 (Dai-ichi Life Insurance Company, Limited)
- Document: ５年ごと配当付こども学資保険 普通保険約款, 平成25年12月18日改正, 24 pp.; file `06_10339_002.pdf` in the
  2014-01 約款 archive set `06_2014_01_1`
- Doc type: 約款 (policy conditions)
- URL: https://event.dai-ichi-life.co.jp/yakkan/06_2014_01_1/pdf/06_10339_002.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 24 pp.; a first extraction with
  `pypdf` failed on the Adobe-Japan1 CID fonts, re-extracted with PyMuPDF and read in full).
  The most completely drafted 保険料払込免除 article in the set: three triggers on the
  **policyholder**, their carve-outs, the successor-policyholder machinery (Arts 29–31) and
  the grace-period trap that refuses the waiver where a premium is unpaid at the event.

(jplib-endowment-s2)=

### S2 — かんぽ生命保険, "普通養老保険普通保険約款" (policy conditions)

- Publisher: 株式会社かんぽ生命保険 (Japan Post Insurance Co., Ltd.)
- Document: 普通養老保険普通保険約款, 平成19年10月1日制定 / 平成28年4月2日改正; 26 pp. as fetched (booklet pages
  84–109), file `yr13.pdf` in the 養老保険 2019.04 Web約款 set
- Doc type: 約款 (policy conditions)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/yoro/201904/yr13.pdf (index:
  https://www.jp-life.japanpost.jp/products/clause/yoro/201904.html)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 26 pp.; `pypdf` and poppler
  `pdftotext` both failed — poppler reported "Unknown character collection 'Adobe-Japan1'" —
  re-extracted with PyMuPDF and read in full). One of the two full 養老保険 約款 in the set, and
  the only source for the juvenile graded death benefit, the accidental double indemnity and
  the 養老保険 form of the premium waiver.

(jplib-endowment-s3)=

### S3 — かんぽ生命保険, "ご契約のしおり・約款 学資保険（H24）／はじめのかんぽ" (policy booklet)

- Publisher: 株式会社かんぽ生命保険
- Document: 学資保険（H24）ご契約のしおり・約款, 2022年4月作成, 248 pp.; contains the しおり, the 学資保険（H24）普通保険約款
  and every rider condition
- Doc type: ご契約のしおり・約款 (policy booklet: customer guide plus policy conditions)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/gaksi/202204/gaksi_2022_04.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 248 pp., text extracted with
  PyMuPDF; the product diagrams, the benefit tables, 別表1 and the 払込免除 articles read). Source
  of the three 学資祝金 schedules, of the `max(cumulative premiums − benefits − loans, 積立金)`
  death-benefit form, and of the rider menu.

(jplib-endowment-s4)=

### S4 — かんぽ生命保険, "かんぽ生命の養老保険「新フリープラン」" (product page)

- Publisher: 株式会社かんぽ生命保険
- Doc type: product page (consumer)
- URL: https://www.jp-life.japanpost.jp/products/yoro/special/index.html
- Accessed: 2026-08-20. Retrieved: YES. The only published 養老保険 term-and-amount envelope in
  the set (保険期間 10–60 years in one-year steps, 基準保険金額 ¥1,000,000–¥10,000,000), and the
  source of the 定額型 / 2倍保障型 / 5倍保障型 / 10倍保障型 menu in which the death benefit is a stated
  multiple of the maturity benefit.

(jplib-endowment-s5)=

### S5 — かんぽ生命保険, "学資保険「はじめのかんぽ」" (product page)

- Publisher: 株式会社かんぽ生命保険
- Doc type: product page (consumer)
- URL: https://www.jp-life.japanpost.jp/products/gaksi/student.html
- Accessed: 2026-08-20. Retrieved: YES. 被保険者 issue ages 0–12 (0–5 and 0–3 on some courses),
  契約者 18–65, the 17 / 18 / 21歳満期 and 全期間払込 / 12歳払込済 / 18歳払込済 grids, and 基準保険金額
  ¥500,000–¥7,000,000.

(jplib-endowment-s6)=

### S6 — 日本生命保険, "契約基本約款（こども・学資）" (policy conditions, base contract)

- Publisher: 日本生命保険相互会社 (Nippon Life Insurance Company)
- Document: 契約基本約款（こども・学資）, 23 pp.; the common base 約款 for こども保険（有配当2012）, 学資保険（有配当2013）and
  こども総合医療保険（有配当2012）
- Doc type: 約款 (policy conditions)
- URL: https://www.nissay.co.jp/keiyaku/shiori/download/pdf/2014/10/gakushi/02.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 23 pp., text extracted and
  read). Cited chiefly as the **counter-example on lapse mechanics**: no grace article at
  all (a demand is served and the contract is 解除 at the 月ごと応当日 in the third month after the
  due month, Art 7), no 復活 article, no 保険料の自動貸付 article and no 契約者貸付 article in the table of
  contents.

(jplib-endowment-s7)=

### S7 — 日本生命保険, "ニッセイ学資保険 ご契約のしおり" (customer guide)

- Publisher: 日本生命保険相互会社
- Document: ご契約のしおり 定款・約款, しおり番号 202501E, 2025年1月改訂, 75 pp.
- Doc type: ご契約のしおり (customer guide / policy summary)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/gakushi/shiori/01.pdf (index:
  https://www.nissay.co.jp/kojin/shohin/seiho/gakushi/shiori/index.html)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 75 pp., text extracted; the
  benefit tables, the premium-unit-rate band table, the surrender and loan sections and the
  tax section read). The only source publishing a **premium unit rate in volume bands**, the
  only one splitting the staged benefits between 雑所得 and 一時所得, and the only one stating that
  the surrender value is capped at the death benefit.

(jplib-endowment-s8)=

### S8 — 日本生命保険, "養老保険（有配当2012）給付約款" (policy conditions)

- Publisher: 日本生命保険相互会社
- Document: 養老保険（有配当2012）給付約款, pp. 28–33 of the 64-page combined 約款 booklet for
  ニッセイ一時払終身保険・ニッセイ一時払養老保険・ニッセイ一時払年金保険
- Doc type: 約款 (policy conditions)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/ichiji/shiori/02.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 64 pp., text extracted; the
  養老保険 給付約款 read in full). The second full 養老保険 約款, and the source of the flat statement
  that 死亡保険金 = 満期保険金 = 保険金額, of the three-year suicide exclusion returning the 責任準備金
  (*sekinin-junbikin*, policy reserve), and of the fact that the premium waiver is **not**
  in the 主契約 (*shu-keiyaku*, main contract) but in an attachable 保険料払込免除特約 (*tokuyaku*,
  rider).

(jplib-endowment-s9)=

### S9 — 日本生命保険, "保険料率等の改定について" (news release, pricing basis)

- Publisher: 日本生命保険相互会社
- Document: 保険料率等の改定について, 2024年11月21日, 4 pp., document code 2024-2212G
- Doc type: news release (pricing and basis disclosure)
- URL: https://www.nissay.co.jp/news/2024/pdf/20241121b.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 4 pp., text extracted and
  read). **The single most valuable numeric source for this product**: 予定利率
  (*yotei riritsu*, assumed interest rate) by product group
  before and after the 2025-01-02 revision (学資保険・こども保険 0.85% → 1.00%; 養老保険（一時払を除く）0.60% →
  1.00%), the 契約貸付利率 2.00% → 2.40%, and worked monthly premiums for both 養老保険 and 学資保険 model
  points that tie exactly to the unit rate in [S7].

(jplib-endowment-s10)=

### S10 — 富国生命保険, "５年ごと配当付学資保険普通保険約款"（みらいのつばさ）(policy conditions)

- Publisher: 富国生命保険相互会社 (Fukoku Mutual Life Insurance Company)
- Document: ５年ごと配当付学資保険 普通保険約款, 2024年4月改定, 20 pp.; Web約款 閲覧コード 0302404, for contracts dated
  2024-04-02 to 2025-07-01, issued 2024年4月／2024年8月
- Doc type: 約款 (policy conditions)
- URL:
  https://web-ic.fukoku-life.co.jp/iportal/CatalogDownload.do?method=downloadPdfCatalog&type=downloadPdfCatalog&volumeID=FLI00002&catalogID=2733240000&applicationPdf=false
  (landing page: https://web-ic.fukoku-life.co.jp/clause/0302404.html)
- Accessed: 2026-08-20. Retrieved: YES (the landing page was fetched, its four catalogue
  download links enumerated, and the 普通保険約款 PDF downloaded with a browser User-Agent and a
  Referer header; served as `application/octet-stream` but is a 20-page PDF v1.4; text
  extracted and read). Source of the **S型 / J型 祝金 percentage grid by the child's 契約年齢** that
  the composite adopts, of the two-year (not three-year) suicide carve-out on the waiver, of
  the six-month 自動貸付 cycle, and of the article that converts a 学資保険 into a paid-up **養老保険**.

(jplib-endowment-s11)=

### S11 — 富国生命保険, "学資保険 みらいのつばさモデルプラン" (product page, model plans)

- Publisher: 富国生命保険相互会社
- Doc type: product page (consumer), worked model plans
- URL: https://www.fukoku-life.co.jp/plan/tsubasa/modelplan/
- Accessed: 2026-08-20. Retrieved: YES. Three complete model plans on a 30-year-old male
  policyholder and a 0-year-old child, 22歳満期, 満期保険金 ¥1,000,000, with receipts, monthly
  premium, total premiums and 返戻率 for each — the arithmetic that lets the S型 grid in [S10]
  be checked against a published total. The composite's second model cell is this plan.

(jplib-endowment-s12)=

### S12 — 富国生命保険, "学資保険 みらいのつばさの特長" (product page)

- Publisher: 富国生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.fukoku-life.co.jp/gakushi/forte/
- Accessed: 2026-08-20. Retrieved: YES. S型 versus J型 positioning, the highest 返戻率 in the
  observed set (approx. 131.3% on the J型 5歳払込 option), the sibling discount from the second
  child, and the three cases in which a child medical policy cannot be packaged.

(jplib-endowment-s13)=

### S13 — 明治安田生命保険, "明治安田生命つみたて学資 ご案内ブックレット" (brochure and pre-contract disclosure)

- Publisher: 明治安田生命保険相互会社 (Meiji Yasuda Life Insurance Company)
- Document: ご案内ブックレット (商品パンフレット ／ ご契約時の留意事項 ／ 特に重要なお知らせ（注意喚起情報）), 2 pp., 139.6 KB; the tax
  note is dated 2026年1月現在
- Doc type: 商品パンフレット + 注意喚起情報 (pre-contract disclosure)
- URL:
  https://www.meijiyasuda.co.jp/find2/light/list/tumitategakushi/pdf/tumitategakushi_booklet.pdf
- Accessed: 2026-08-20. Retrieved: YES (downloaded; `pypdf` and poppler both mis-decoded the
  Adobe-Japan1 CID fonts, re-extracted with PyMuPDF and read in full). The **negative-space
  source**: the one carrier in the set that offers neither dividends, nor riders, nor 復活,
  nor 自動振替貸付, nor 転換, nor 延長定期保険, nor 払済保険 — and that taxes both its 教育資金 and its 満期保険金 as
  雑所得 with a stated 必要経費 formula. Its full 普通保険約款 was **not** retrieved (see the gaps
  register in the research file), so everything attributed to [S13] is brochure-level.

(jplib-endowment-s14)=

### S14 — 明治安田生命保険, "学資保険-明治安田生命つみたて学資" (product page)

- Publisher: 明治安田生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find2/light/list/tumitategakushi/index.html
- Accessed: 2026-08-20. Retrieved: YES. 21歳満期, premium-paying to age 15 (or 10 where the
  child is 0–2), 契約者 issue ages 18–65 with the upper limit stated to move with market rates,
  prenatal entry from 140 days before the due date, the four-receipt shape, a 受取率 of up to
  129.2% on a stated example, and the statement that **no riders can be attached**.

(jplib-endowment-s15)=

### S15 — 明治安田生命保険, "養老保険" (product page)

- Publisher: 明治安田生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find/list/old/
- Accessed: 2026-08-20. Retrieved: YES. Thin by design and cited as such: 被保険者 issue ages
  6–75 varying with the term, death benefit equal to maturity benefit, a 高度障害保険金 that
  terminates the contract, and 保険契約者代理特約 / 代理請求特約. Amounts, terms and the dividend class are
  **not** stated on the page, and the corresponding 約款 sits behind a session-gated portal.

(jplib-endowment-s16)=

### S16 — ソニー生命保険, "学資保険の特徴" and "ご契約プラン例" (product pages)

- Publisher: ソニー生命保険株式会社 (Sony Life Insurance Co., Ltd.)
- Doc type: product pages (consumer), including worked plan examples
- URL: https://www.sonylife.co.jp/gakushi/advantage/ and
  https://www.sonylife.co.jp/gakushi/example/
- Accessed: 2026-08-20. Retrieved: YES (both pages fetched). The I型 / II型 / III型 typology
  (level funding across 中学・高校・大学, weighted to university entry, and paid over the years
  after university entry), terms of 17 / 18 / 20 / 22歳満期, five published 返戻率 between 116.0%
  and 127.4%, and two full III型 worked plans whose premium totals reconcile to the monthly
  premium exactly. The percentage grid behind the plans is **not** published.

---

## Regulatory and actuarial references

(jplib-endowment-r1)=

### R1 — 日本アクチュアリー会, 標準生命表２０１８ (standard mortality tables)

- Publisher: 公益社団法人日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — p. 2 生保標準生命表2018（死亡保険用）男, p. 3 同 女, p. 4 第三分野標準生命表2018 男, p.
  5 同 女, each with x, l(x), d(x), q(x) and e(x) on a radix of 100,000
- Doc type: statutory valuation mortality table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf (index:
  https://www.actuaries.jp/lib/standard-life-table/index2018.html)
- Accessed: 2026-08-20. Retrieved: YES (the shorter path
  `.../standard-life-table/seimeihyo2018.pdf` returns the site's 404 page; the index page
  was fetched, the real path read off it, and the PDF downloaded and parsed). Source of the
  child-age q(x) run that makes the 学資保険 death benefit a near-zero-strain decrement, and of
  the policyholder-age q(x) run that prices the waiver.

(jplib-endowment-r2)=

### R2 — 日本アクチュアリー会, 標準生命表２０１８の作成概要 (methodology note)

- Publisher: 公益社団法人日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp., 資料①–⑤
- Doc type: technical note
- URL: https://www.actuaries.jp/info/pdf/20170512-2.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, text extracted and read).
  Establishes 標準生命表2018 as a **valuation** table carrying safety margins — observation years
  2008, 2009 and 2011 (2010 excluded for the Tōhoku earthquake), select-period truncation
  capped at 10 years, policy years to 30, exposure 40.68 million policy-years male and 30.02
  million female — and therefore not a best-estimate experience basis.

(jplib-endowment-r3)=

### R3 — e-Gov 法令検索, 保険業法施行規則 第68条・第69条

- Publisher: 総務省 e-Gov 法令検索 (statute: 平成8年2月29日大蔵省令第5号)
- Doc type: ministerial ordinance (articles)
- URL: https://laws.e-gov.go.jp/law/408M50000040005 (retrieved through the e-Gov law API at
  https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005)
- Accessed: 2026-08-20. Retrieved: YES (the HTML page is JavaScript-rendered and returned
  only navigation chrome; the law XML — 30.2 MB — was fetched from the API instead, stripped
  of tags, and Arts 68–69 read in full). 第68条 is why a conventional 養老保険 or 学資保険 is a
  standard-reserve contract; 第69条 is the 保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金 taxonomy and the
  平準純保険料式 floor.

(jplib-endowment-r4)=

### R4 — 金融庁, 平成8年大蔵省告示第48号 一部改正（案）の公表 (2014-04-01)

- Publisher: 金融庁 (Financial Services Agency)
- Document:「保険業法第百十六条第二項の規定に基づく長期の保険契約で内閣府令で定めるものについての責任準備金の積立方式及び予定死亡率その他の
  責任準備金の計算の基礎となるべき係数の水準（平成八年大蔵省告示第四十八号）の一部を改正する件（案）」の公表について
- Doc type: 告示改正案 (draft notification, public comment)
- URL: https://www.fsa.go.jp/news/25/hoken/20140401-3.html (attachment:
  https://www.fsa.go.jp/news/25/hoken/20140401-3/01.pdf)
- Accessed: 2026-08-20. Retrieved: YES (the HTML page fetched and read; the attached PDF was
  not opened). Confirms that 告示第48号 is the instrument setting the 積立方式, the 予定死亡率 and the
  標準利率 (*hyōjun riritsu*, standard valuation rate), and that the 標準利率 references the lower
  of the three-year and ten-year average yield
  on 10-year JGBs, determined annually.

(jplib-endowment-r5)=

### R5 — 金融庁, 標準責任準備金制度にかかる告示の一部改正（案）等の公表 (2021-04-23)

- Publisher: 金融庁
- Doc type: 告示改正案 (draft notification, public comment)
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html (attachments `01.pdf`,
  `02.pdf`, `03.pdf` under the same directory)
- Accessed: 2026-08-20. Retrieved: YES (HTML page fetched and read; attachments not opened).
  Brings USD- and AUD-denominated contracts concluded on or after 2022-04-01 into 標準責任準備金
  scope and sets the method for their 標準利率; the other amendments took effect 2021-10-01.
  Cited here only as the scope boundary of the yen composite.

(jplib-endowment-r6)=

### R6 — 国税庁, タックスアンサー No.1755「生命保険契約に係る満期保険金等を受け取ったとき」

- Publisher: 国税庁 (National Tax Agency)
- Doc type: タックスアンサー (tax guidance), updated 2025-04-01
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1755.htm
- Accessed: 2026-08-20. Retrieved: YES. The lump-sum-versus-instalment distinction this
  product turns on: where the premium payer and the recipient are the same person, a
  lump-sum 満期保険金 is 一時所得 (receipts less premiums less a ¥500,000 特別控除, half of the remainder
  taxable), while a staged benefit is 雑所得, with neither the deduction nor the halving.

(jplib-endowment-r7)=

### R7 — 国税庁, タックスアンサー No.1140「生命保険料控除」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES. The post-2012 three-basket regime with the exact
  deduction bands and the ¥40,000 per-basket and ¥120,000 overall income-tax caps. The page
  covers 所得税 only.

(jplib-endowment-r8)=

### R8 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax guidance), updated 2025-04-01
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES. Puts both 養老保険 and 学資保険 in the 一般生命保険料 basket
  (contracts paying on survival or death), states the 税制適格 conditions that neither product
  can meet, and excludes savings-type contracts with a term under five years.

(jplib-endowment-r9)=

### R9 — 生命保険協会,「２０２５年版 生命保険の動向」 (industry statistics)

- Publisher: 一般社団法人生命保険協会 (Life Insurance Association of Japan)
- Document: `all_2025.pdf`, 33 pp. (FY2024 figures)
- Doc type: industry statistics
- URL: https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 33 pp., text extracted; the
  個人保険 sections read). Source of the 養老保険 and こども保険 shares of new business and in force on
  all three published measures, and of the industry 解約・失効率 with its five-year history.

(jplib-endowment-r10)=

### R10 — 生命保険文化センター,「養老保険」 (product-taxonomy page)

- Publisher: 公益財団法人生命保険文化センター (Japan Institute of Life Insurance)
- Doc type: consumer education / product taxonomy page
- URL: https://www.jili.or.jp/knows_learns/kind/main/38.html
- Accessed: 2026-08-20. Retrieved: YES. The neutral, non-carrier definition of 養老保険 — a
  fixed-term contract whose death benefit and maturity benefit are **equal in amount** —
  plus the 年満期 / 歳満期 distinction, the four premium modes, and the plain statement that the
  maturity benefit can fall short of total premiums paid.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the endowment
documents:

- **REG-R1** — 保険業法 第3条, licence classes and the 第一分野 / 第三分野 (*dai-san-bun'ya*, third
  sector) split. Retrieved: yes.
- **REG-R2** — 保険業法 第4条, 基礎書類; why the 予定死亡率 and 予定事業費率 are **[std]** while 約款 facts are
  [S#]. Retrieved: yes.
- **REG-R3** — 保険業法 第115条, 価格変動準備金 — asset-driven, cited and never modelled. Retrieved: yes.
- **REG-R4** — 保険業法 第116条, 責任準備金 and the delegation the 標準責任準備金 chain hangs on. Retrieved:
  yes.
- **REG-R5** — 保険業法 第120条, 保険計理人の選任 — the governance frame for any basis this model uses.
  Retrieved: yes.
- **REG-R6** — 保険業法 第121条, the 保険計理人's 意見書 and the 第1号 confirmation. Retrieved: yes.
- **REG-R7** — 施行規則 第68条, which contracts are standard-reserve contracts. Retrieved: yes.
- **REG-R8** — 施行規則 第69条, the four-way reserve taxonomy. Retrieved: yes.
- **REG-R9** — 施行規則 第30条の2, the four surplus-distribution methods; 三利源 is practice, not
  regulatory language. Retrieved: yes.
- **REG-R10** — 平成8年大蔵省告示第48号, 標準責任準備金: 平準純保険料式, table vintages and the 標準利率 reset rules.
  Retrieved: yes, from an unofficial consolidated mirror — see that entry.
- **REG-R11** — 告示48号改正 (2017), adoption of 標準生命表2018 for contracts from 2018-04-01.
  Retrieved: yes.
- **REG-R12** — 告示改正 (2021), extension of 標準責任準備金 to USD- and AUD-denominated contracts —
  the currency scope boundary this yen composite sits inside. Retrieved: yes (landing page;
  the 別紙 PDFs were not opened).
- **REG-R14** — 監督指針（本編）: IV-1-10 requires 解約返戻金 (*kaiyaku-henreikin*, surrender value)
  disclosure and IV-1-12 requires 自動振替貸付 to be at the policyholder's election.
  Retrieved: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: commencement 2026-03-31, the 100% trigger, 現在推計 + MOCE,
  the 99.5% calibration. Retrieved: yes.
- **REG-R16** — ESR 政策ページ, the index to the 柱告示 PDFs; the coefficients are [unverified].
  Retrieved: yes (index only).
- **REG-R17** — ソルベンシー・マージン比率 and the old 200% threshold. Retrieved: no (the 告示 itself was
  not located).
- **REG-R18** — 標準生命表2018 PDF: the public valuation q(x) tables and terminal ages.
  Retrieved: yes.
- **REG-R20** — 標準生命表2018 作成概要: the 2σ margin, the improvement allowance, the 保険年齢
  (*hoken-nenrei*, nearest-birthday age) basis and the inclusion of 高度障害 in the death rate.
  Retrieved: yes.
- **REG-R21** — 日本アクチュアリー会 索引と利用規約: redistribution is restricted, so `jplib` ships a
  **[std]** table citing REG-R18/REG-R19 rather than a copy. Retrieved: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析, its ten-year horizon and its scenario sets.
  Retrieved: yes.
- **REG-R23** — 監督指針 VI, the 指定法人 role: how a professional table binds a statutory reserve.
  Retrieved: yes.
- **REG-R24** — 第23回生命表 (2020): the redistributable national single-year table against which
  the margin in 標準生命表2018 could be quantified. Cited as that benchmark only; no rate from
  it enters `mort_table.csv`. Retrieved: yes.
- **REG-R31** — 生命保険の動向 2025: market mix and the 5.6% industry 解約・失効率 with its definition.
  Retrieved: yes.
- **REG-R32** — 全国実態調査 2024: household penetration and the premium and sum-assured bands a
  model point should sit inside. Retrieved: yes.
- **REG-R34** — 保険法 第51条, 免責: the statutory suicide exclusion has **no** time limit, so the
  three-year 免責期間 is contractual. Retrieved: yes.
- **REG-R35** — 保険法 第55条, 告知義務違反: the five-year contestability ceiling and the one-month
  discovery clock. Retrieved: yes.
- **REG-R36** — 保険業法 第309条, クーリング・オフ: the eight-day dispatch rule, scoped out here.
  Retrieved: yes.
- **REG-R37** — 保険業法 第300条の2, 特定保険契約: why a yen, fixed-予定利率 endowment is **not** one.
  Retrieved: yes.
- **REG-R38** — 消費者契約法 第4条: 断定的判断の提供, and why an advertised 返戻率 must be split into 保証 and
  非保証 elements. Retrieved: yes.
- **REG-R39** — 金融サービス提供法 第4条: the 説明義務 limb covering 解約控除 and suppression periods.
  Retrieved: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: 90% of 責任準備金; the 高予定利率契約 detail is [unverified].
  Retrieved: yes (Q1 only).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of the compensation rate. Retrieved:
  yes.
- **REG-R43** — 所得税法 第76条: three ¥40,000 baskets capped at ¥120,000. Retrieved: yes.
- **REG-R44** — 相続税法 第12条: the ¥5,000,000 × statutory heirs exemption, which attaches to a
  死亡保険金 and not to a transferred contract right. Retrieved: yes.
- **REG-R45** — タックスアンサー No.4114: the heir-only exemption and the heir count. Retrieved:
  yes.
- **REG-R46** — タックスアンサー No.1755: 一時所得 on a lump sum, 雑所得 on an instalment stream.
  Retrieved: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS are
  three separate bases over one projection. Retrieved: yes (index page only).

---

## Provenance note

Extraction details — the section-level fact extraction, the six-carrier variation tables,
and the full gaps register — live in `_research/endowment.md`, which is the citation ground
truth for the S# and R# numbering used here. The gaps that most constrain these documents:
one carrier's 普通保険約款 was never retrieved and everything attributed to it is brochure-level
[S13] [S14]; a second carrier's 養老保険 約款 likewise sits behind a session-gated portal [S15];
the 別表2 child death-benefit schedule of a third carrier's 学資保険 was in neither retrieved
file, so its exact formula is [unverified] [S7]; the 育英年金 rider conditions were not
retrieved at either carrier that offers one [S1] [S6]; the numeric 標準利率 in force at the
access date could not be established from any official document [R4] [R5]; no carrier
publishes a full rate basis, a 予定事業費率 or a surrender-value table; and no source gives a
lapse curve by duration or anything specific to 養老保険 or こども保険 [R9].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R4]: #jplib-endowment-r4
[R5]: #jplib-endowment-r5
[R9]: #jplib-endowment-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
