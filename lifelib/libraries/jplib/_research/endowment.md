# Endowment (養老保険) with educational endowment (学資保険) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese endowment liability cash flow reference model — the plain 養老保険
(*yōrō hoken*, endowment: maturity benefit equal to the death benefit) as the base cell, and
学資保険 (*gakushi hoken*, educational endowment) as the second cell, where staged survival
benefits are paid at school-entry ages and the premium stream is waived on the death or
severe disability of the **policyholder** — a life who is not the insured.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually retrieved and read during
this session, or is tagged [unverified] where it is general knowledge or a secondary snippet
that could not be confirmed against a retrieved document. Numbers derived by arithmetic from
retrieved figures are labelled "derived" at the point of use. Access date for all fetched
sources: 2026-08-20.

Six carriers are covered: 第一生命, かんぽ生命, 日本生命, フコク生命, 明治安田生命, ソニー生命.

---

## Primary sources

### S1 — 第一生命, "５年ごと配当付こども学資保険普通保険約款" (policy conditions)
- Publisher: 第一生命保険株式会社 (Dai-ichi Life Insurance Company, Limited)
- Document: ５年ごと配当付こども学資保険 普通保険約款, 平成25年12月18日改正, 24 pp. (file `06_10339_002.pdf` under the
  2014-01 yakkan set `06_2014_01_1`)
- Doc type: 約款 (policy conditions)
- URL: https://event.dai-ichi-life.co.jp/yakkan/06_2014_01_1/pdf/06_10339_002.pdf
- Retrieved: YES (full PDF downloaded, 24 pp.; first extraction with `pypdf` failed on the
  Adobe-Japan1 CID fonts, re-extracted with PyMuPDF and read in full)
- Key content: 学資金 / 満期保険金 / 死亡給付金 payment table with the 18歳満期 and 22歳満期 variants; 死亡給付金 as
  cumulative monthly premium; the three 保険料払込免除 triggers on the **policyholder** and their
  exclusions (3-year suicide, 後継保険契約者の故意, war); 自動すえ置 of 学資金; grace and lapse (Art 14);
  保険料の自動貸付 (Art 15–16); 復活 within three years (Art 17); 告知義務違反 two-year contestability (Art
  22); 解約返還金 (Art 24); 基準保険金額の減額 (Art 26); 契約者貸付 (Art 27); 後継保険契約者 machinery (Art 29–31);
  age calculation (Art 33); 契約者配当 on a five-year cycle (Art 35).

### S2 — かんぽ生命, "普通養老保険普通保険約款" (policy conditions)
- Publisher: 株式会社かんぽ生命保険 (Japan Post Insurance Co., Ltd.)
- Document: 普通養老保険普通保険約款, 平成19年10月1日制定 / 平成28年4月2日改正, 26 pp. as fetched (booklet pages
  84–109), file `yr13.pdf` in the 養老保険 2019.04 Web約款 set
- Doc type: 約款 (policy conditions)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/yoro/201904/yr13.pdf (index
  page: https://www.jp-life.japanpost.jp/products/clause/yoro/201904.html)
- Retrieved: YES (full PDF downloaded, 26 pp.; `pypdf` and poppler `pdftotext` both failed —
  poppler reported "Unknown character collection 'Adobe-Japan1'" — re-extracted with PyMuPDF
  and read in full)
- Key content: 死亡保険金 = 満期保険金 = 基準保険金額 (Art 1); juvenile graded death benefit (50% under age
  3, 80% under age 6, floored at 積立金); 3-year suicide exclusion; 重度障害 treated as death (Art
  2); 保険金の倍額支払 for accidental death and listed infectious disease after 1年6か月 (Art 3); 払込免除
  on the **insured's** disability (Art 5) and separately on the **policyholder's**
  accidental death where the policyholder is a parent/grandparent/sibling and the child is
  under 10 (Art 6); responsibility commencement and 契約日 (Art 7); premium due windows and a
  three-month grace (Arts 9–11); 加入年齢 rounding (Art 31); 解約 (Art 33); 返戻金 (Art 35); 復活
  within one year (Art 36–38); 契約者貸付 including premium-substituting loans (Art 39); 契約者配当
  (Arts 40–41).

### S3 — かんぽ生命, "ご契約のしおり・約款 学資保険（H24）／はじめのかんぽ" (policy booklet)
- Publisher: 株式会社かんぽ生命保険
- Document: 学資保険（H24）ご契約のしおり・約款, 2022年4月作成, 248 pp. (booklet contains the しおり, the
  学資保険（H24）普通保険約款 and all rider conditions)
- Doc type: ご契約のしおり・約款 (policy booklet: customer guide + policy conditions)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/gaksi/202204/gaksi_2022_04.pdf
- Retrieved: YES (full PDF downloaded, 248 pp., text extracted with PyMuPDF; the product
  diagrams, benefit tables, 別表1 and the 払込免除 articles were read)
- Key content: the three product shapes (17・18歳満期 with no 学資祝金; 学資祝金付17・18歳満期; 学資祝金付21歳満期)
  with their exact 学資祝金 percentages and payment dates; 死亡給付金額 (別表1) as the greater of
  cumulative premiums less benefits and loans, or 積立金; 払込免除 on policyholder death or 重度障害
  with a 3-year suicide carve-out (Art 3); the rider menu (無配当災害特約, 無配当傷害医療特約（R04）,
  無配当総合医療特約（R04）, 無配当先進医療特約（無解約返戻金型）).

### S4 — かんぽ生命, product page "かんぽ生命の養老保険「新フリープラン」"
- Publisher: 株式会社かんぽ生命保険
- Doc type: product page (consumer)
- URL: https://www.jp-life.japanpost.jp/products/yoro/special/index.html
- Retrieved: YES
- Key content: 保険期間 10–60 years selectable in one-year steps; 基準保険金額 ¥1,000,000 to
  ¥10,000,000; the 定額型 / 2倍保障型 / 5倍保障型 / 10倍保障型 menu in which the death benefit is a stated
  multiple of the maturity benefit; premium examples at ages 30 and 40 on the 2026-05-02
  rate basis; rider menu.

### S5 — かんぽ生命, product page "学資保険「はじめのかんぽ」"
- Publisher: 株式会社かんぽ生命保険
- Doc type: product page (consumer)
- URL: https://www.jp-life.japanpost.jp/products/gaksi/student.html
- Retrieved: YES
- Key content: 被保険者 issue ages 0–12 (0–5 and 0–3 on some courses); 契約者 issue ages 18–65; 17
  / 18 / 21歳満期; 全期間払込 / 12歳払込済 / 18歳払込済; 基準保険金額 ¥500,000 to ¥7,000,000 (¥5,000,000 on some
  courses); premium examples before and after the rate revision; at most three riders
  attachable.

### S6 — 日本生命, "契約基本約款（こども・学資）" (policy conditions, base contract)
- Publisher: 日本生命保険相互会社 (Nippon Life Insurance Company)
- Document: 契約基本約款（こども・学資）, 23 pp., the common base 約款 for こども保険（有配当 2012）, 学資保険（有配当2013）and
  こども総合医療保険（有配当2012）
- Doc type: 約款 (policy conditions)
- URL: https://www.nissay.co.jp/keiyaku/shiori/download/pdf/2014/10/gakushi/02.pdf
- Retrieved: YES (full PDF downloaded, 23 pp., text extracted and read)
- Key content: 責任開始期 and 契約日 (Art 2); premium due windows, monthly and annual only (Art 4);
  一括払込 3–12 months and 前納 of 2+ years (Art 6); **no grace period as such** — on non-payment
  the insurer serves notice and the contract is *rescinded* at the 月ごと応当日 in the third month
  after the due month (Art 7); 基準保険金額の減額 (Art 9), which is refused once the 学資年金開始日 has
  arrived; 告知義務 and its two-year contestability (Arts 14–16); 重大事由 (Art 17); 解約 (Art 18);
  契約年齢の計算 (Art 24). The table of contents carries **no 復活 article, no 保険料の自動貸付 article and
  no 契約者貸付 article** — the loan provisions sit in the 給付約款 instead (confirmed by S7).

### S7 — 日本生命, "ニッセイ学資保険 ご契約のしおり" (customer guide)
- Publisher: 日本生命保険相互会社
- Document: ご契約のしおり 定款・約款, しおり番号 202501E, 2025年1月改訂, 75 pp.
- Doc type: ご契約のしおり (customer guide / policy summary)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/gakushi/shiori/01.pdf (index:
  https://www.nissay.co.jp/kojin/shohin/seiho/gakushi/shiori/index.html)
- Retrieved: YES (full PDF downloaded, 75 pp., text extracted; the benefit tables, the
  premium-rate band table, the surrender and loan sections and the tax section were read)
- Key content: こども祝金なし型 / こども祝金あり型; 学資年金 in five instalments — the first equal to 基準保険金額 and
  the second to fifth at 50% of the first; こども祝金 at 20% of 基準保険金額 on the 2月1日 following ages
  5歳10カ月, 11歳10カ月 and 14歳10カ月; 死亡保険金 per 別表2; **premium unit rates in three bands**; premium
  waiver on policyholder death only, with the contract terminating instead on 3-year
  suicide, 後継保険契約者の故意 or war; 学資年金 commutation to a lump sum; 解約払戻金 capped at the death
  benefit; the contract-loan over-run mechanism; tax split (学資年金 = 雑所得, こども祝金 = 一時所得).

### S8 — 日本生命, "養老保険（有配当2012）給付約款" (policy conditions)
- Publisher: 日本生命保険相互会社
- Document: 養老保険（有配当2012）給付約款, pp. 28–33 of the 64-page combined 約款 booklet for
  ニッセイ一時払終身保険・ニッセイ一時払養老保険・ニッセイ一時払年金保険
- Doc type: 約款 (policy conditions)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/ichiji/shiori/02.pdf
- Retrieved: YES (full PDF downloaded, 64 pp., text extracted; the 養老保険 給付約款 read in full)
- Key content: 死亡保険金 = 満期保険金 = 保険金額 (Art 1); 3-year suicide exclusion returning 責任準備金,
  policyholder-caused death returning 解約払戻金; war-risk reduction floored at 責任準備金 (Art 2);
  保険契約者に対する貸付 (Art 9); 払戻金 (Art 10); 特別条件 (Art 11); the provision making part of the
  contract 一時払 (Art 13); the waiver of premium is **not** in the main contract but in an
  attachable 保険料払込免除特約; リビング・ニーズ特約 is automatic on 終身保険 and 養老保険.

### S9 — 日本生命, "保険料率等の改定について" (news release, pricing basis)
- Publisher: 日本生命保険相互会社
- Document: 保険料率等の改定について, 2024年11月21日, 4 pp., document code 2024-2212G
- Doc type: news release (pricing/basis disclosure)
- URL: https://www.nissay.co.jp/news/2024/pdf/20241121b.pdf
- Retrieved: YES (full PDF downloaded, 4 pp., text extracted and read)
- Key content: **予定利率 by product, before and after** — 学資保険・こども保険 0.85% → 1.00%;
  年金保険・養老保険（一時払を除く）・生存給付金付定期保険・長寿生存保険（低解約払戻金型） 0.60% → 1.00%; 終身保険（一時払を除く）・長期定期保険 0.25% →
  0.40%. Effective for contracts dated on or after 2025-01-02 (renewals from 2025-05-02).
  **契約貸付利率 2.00% → 2.40%**. A premium-example table for 学資保険, こども保険, 養老保険, 年金保険, 終身保険 and
  others, giving monthly account-debit premiums before and after.

### S10 — フコク生命, "５年ごと配当付学資保険普通保険約款"（みらいのつばさ）(policy conditions)
- Publisher: 富国生命保険相互会社 (Fukoku Mutual Life Insurance Company)
- Document: ５年ごと配当付学資保険 普通保険約款, 2024年4月改定, 20 pp.; Web約款 閲覧コード 0302404, contracts dated
  2024-04-02 to 2025-07-01, issued 2024年4月／2024年8月
- Doc type: 約款 (policy conditions)
- URL:
  https://web-ic.fukoku-life.co.jp/iportal/CatalogDownload.do?method=downloadPdfCatalog&type=downloadPdfCatalog&volumeID=FLI00002&catalogID=2733240000&applicationPdf=false
  (landing page: https://web-ic.fukoku-life.co.jp/clause/0302404.html)
- Retrieved: YES (the landing page was fetched, its four catalogue download links
  enumerated, and the 普通保険約款 PDF downloaded with a browser User-Agent and a Referer header;
  served as `application/octet-stream` but is a 20-page PDF v1.4; text extracted and read)
- Key content: policyholder eligibility restricted to the child's parent or a supporting
  relative within the insurer's age range (Art 1); the **S型 / J型 祝金 percentage grid by
  policyholder-elected type and the child's issue age** (Art 3); 満期保険金 = 保険金額; 死亡払戻金 =
  責任準備金相当額; 祝金 automatically deferred with interest (Art 4); the three 払込免除 triggers on the
  policyholder and a **two-year** suicide carve-out (Arts 5–6); grace by payment frequency
  (Art 14); lapse (Art 15); 保険料の自動貸付 with an interest cap of 年8% (半年4% for
  monthly/semi-annual) (Art 19); 復活 within three years (Art 20); 払戻金 by elapsed months (Art
  23); **払済保険 conversion turns the policy into an endowment** (Art 25); 原保険契約への復帰 within two
  years (Art 27); 契約者貸付 and forced lapse when loan principal plus interest exceeds the
  surrender value (Art 31); age calculation (Art 33); 出生前加入特則 (Arts 38–45); 兄弟加入特則 (Art 46).

### S11 — フコク生命, product page "学資保険 みらいのつばさモデルプラン"
- Publisher: 富国生命保険相互会社
- Doc type: product page (consumer), model plans
- URL: https://www.fukoku-life.co.jp/plan/tsubasa/modelplan/
- Retrieved: YES
- Key content: three model plans on a 30-year-old male policyholder and a 0-year-old child,
  22歳満期, 満期保険金 ¥1,000,000 — S型 17歳払込 (receipts ¥2,100,000, monthly ¥9,047, total premiums
  ¥1,845,588, 返戻率 approx. 113.7%); J型 17歳払込 (receipts ¥2,000,000, monthly ¥8,439, total
  ¥1,721,556, approx. 116.1%); J型 11歳払込 (receipts ¥2,000,000, monthly ¥12,231, total
  ¥1,614,492, approx. 123.8%). Four premium-paying periods: to ages 5, 11, 14, 17.

### S12 — フコク生命, product page "学資保険 みらいのつばさの特長"
- Publisher: 富国生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.fukoku-life.co.jp/gakushi/forte/
- Retrieved: YES
- Key content: S型 vs J型 positioning; a quoted J型 5歳払込 return of approx. 131.3% on receipts
  of ¥2,000,000; the sibling discount from the second child; that a child medical policy can
  be packaged **except** on prenatal contracts, grandparent-policyholder contracts and the
  5歳払込 option; waiver on policyholder death or 高度障害.

### S13 — 明治安田生命, "明治安田生命つみたて学資 ご案内ブックレット" (product brochure)
- Publisher: 明治安田生命保険相互会社 (Meiji Yasuda Life Insurance Company)
- Document: ご案内ブックレット (商品パンフレット ／ ご契約時の留意事項 ／ 特に重要なお知らせ (注意喚起情報)), 2 pp., 139.6 KB; tax note
  stated as at 2026年1月現在
- Doc type: 商品パンフレット + 注意喚起情報 (pre-contract disclosure)
- URL:
  https://www.meijiyasuda.co.jp/find2/light/list/tumitategakushi/pdf/tumitategakushi_booklet.pdf
- Retrieved: YES (downloaded via WebFetch; `pypdf` and poppler both mis-decoded the
  Adobe-Japan1 CID fonts, re-extracted with PyMuPDF and read in full)
- Key content: 教育資金 equal to 基準保険金額 on the 10月1日 following ages 18, 19 and 20, plus 満期保険金
  equal to 基準保険金額; 死亡給付金 = 月掛保険料相当額 × 経過年月数 during the premium-paying period and, after it,
  the greater of that amount less 教育資金 already paid and the 積立金相当額; the I型 / II型 waiver
  triggers (II型 adds a malignant-neoplasm diagnosis more than 90 days after 責任開始日) with
  **only I型 currently sold**; a premium discount of ¥30 per ¥100,000 of 基準保険金額 at ¥700,000
  and above (monthly basis; ×6 semi-annual, ×12 annual); **no dividends**; prenatal cover
  from 140 days before the due date; age calculation truncating fractions of a year; one
  policy per insured child; **復活, 自動振替貸付, 転換, 延長定期保険 and 払済保険 are all not offered**; 教育資金
  and 満期保険金 taxed as 雑所得 with a stated 必要経費 formula.

### S14 — 明治安田生命, product page "学資保険-明治安田生命つみたて学資"
- Publisher: 明治安田生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find2/light/list/tumitategakushi/index.html
- Retrieved: YES
- Key content: 21歳満期; premium-paying period to age 15, or to age 10 where the child is 0–2;
  policyholder issue ages 18–65 (the upper limit stated to move with market rates); prenatal
  entry from 140 days before the due date; four receipts (three 教育資金 plus 満期保険金) over ages
  18–21; 受取率 up to 129.2% on a stated example (I型, policyholder 25 male, child 0, 21歳満期,
  基準保険金額 ¥700,000, 一括払込); waiver on policyholder death or 身体障害表 第1級・第2級; **no riders can be
  attached**.

### S15 — 明治安田生命, product page "養老保険"
- Publisher: 明治安田生命保険相互会社
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find/list/old/
- Retrieved: YES
- Key content: 被保険者 issue ages 6–75 (varying with the term); death benefit and maturity
  benefit equal; 高度障害保険金 terminates the contract; 保険契約者代理特約 and 代理請求特約 available. Insurance
  amounts, terms and the dividend class are not stated on the page.

### S16 — ソニー生命, product pages "学資保険の特徴" and "ご契約プラン例"
- Publisher: ソニー生命保険株式会社 (Sony Life Insurance Co., Ltd.)
- Doc type: product pages (consumer), including worked plan examples
- URL: https://www.sonylife.co.jp/gakushi/advantage/ and
  https://www.sonylife.co.jp/gakushi/example/
- Retrieved: YES (both pages fetched)
- Key content: three plan types — I型 (level funding across 中学・高校・大学), II型 (weighted to
  university entry), III型 (paid over the years after university entry); terms 17 / 18 / 20 /
  22歳満期; quoted 返戻率 of 116.0% (I型, 基準学資金 ¥1,000,000, 18歳満期), 121.3% (II型, ¥2,000,000, 18歳満期)
  and 127.4% (III型, ¥400,000, 22歳満期); two full III型 worked plans on a 30-year-old male
  policyholder and a 0-year-old child, 基準学資金額 ¥400,000, 22歳満期, 受取学資金総額 ¥2,000,000 — 10歳まで払込
  (monthly ¥13,172, total ¥1,580,640, 返戻率 126.5%, gain ¥419,360) and 18歳まで払込 (monthly
  ¥7,816, total ¥1,688,256, 返戻率 118.4%, gain ¥311,744); waiver on policyholder death,
  所定の高度障害状態, or 身体障害状態 from an accident within 180 days; prenatal entry from 140 days before
  the due date (III型 within 91 days).

---

## Regulatory and actuarial references

### R1 — 日本アクチュアリー会, "標準生命表２０１８" (standard mortality tables)
- Publisher: 公益社団法人日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — p. 2 生保標準生命表2018（死亡保険用）男, p. 3 同 女, p. 4 第三分野標準生命表2018 男, p.
  5 同 女
- Doc type: standard mortality table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf (index:
  https://www.actuaries.jp/lib/standard-life-table/index2018.html)
- Retrieved: YES (the first URL tried,
  `https://www.actuaries.jp/lib/standard-life-table/seimeihyo2018.pdf`, returned the site's
  404 page; the index page was fetched, the real path read off it, and the PDF downloaded
  and parsed — l(x), d(x), q(x) and e(x) by age for all four tables)
- Content: 生保標準生命表2018（死亡保険用）q(x), male: 0.00081 at 0, 0.00056 at 1, 0.00022 at 3, 0.00010
  at 5, 0.00010 at 10, 0.00023 at 15, 0.00038 at 17, 0.00046 at 18, 0.00059 at 20, 0.00066
  at 22, 0.00067 at 25, 0.00068 at 30, 0.00077 at 35, 0.00118 at 40, 0.00177 at 45, 0.00285
  at 50, 0.00653 at 60. Female: 0.00078, 0.00053, 0.00019, 0.00008, 0.00007, 0.00014,
  0.00019, 0.00021, 0.00025, 0.00027, 0.00029, 0.00037, 0.00059, 0.00088, 0.00122, 0.00197,
  0.00363 at the same ages. Radix 100,000.

### R2 — 日本アクチュアリー会, "標準生命表２０１８の作成概要" (table construction note)
- Publisher: 公益社団法人日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp., 資料①–⑤
- Doc type: technical note
- URL: https://www.actuaries.jp/info/pdf/20170512-2.pdf
- Retrieved: YES (full PDF downloaded, text extracted and read)
- Content: 生保標準生命表2018（死亡保険用）is built on observation years 2008, 2009 and 2011 (2010
  excluded for the Tōhoku earthquake), extended to 2005–2009 and 2011 at the young and old
  ages; select-period truncation capped at 10 years, truncating at roughly 50% survivorship
  of policy counts; policy years up to 30; exposure 40.68 million policy-years male / 30.02
  million female with 263,000 / 95,000 deaths. This is a **valuation** table carrying safety
  margins, not a best-estimate experience table.

### R3 — e-Gov 法令検索, 保険業法施行規則 第68条・第69条
- Publisher: 総務省 e-Gov 法令検索 (statute: 平成8年2月29日大蔵省令第5号)
- Doc type: statute (ministerial ordinance)
- URL: https://laws.e-gov.go.jp/law/408M50000040005 (retrieved through the e-Gov law API at
  https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005)
- Retrieved: YES (the HTML page is JavaScript-rendered and returned only chrome; the law XML
  was fetched from the e-Gov API instead — 30.2 MB — stripped of tags and Arts 68–69 read in
  full)
- Content: 第68条 defines the contracts within 標準責任準備金 scope as all life contracts concluded
  after the Act took effect **except** separate-account contracts whose reserve varies with
  the fund, contracts that hold no 保険料積立金 or 払戻積立金, and contracts whose 約款 lets the insurer
  change the 予定利率 (unless a floor above the notified rate is guaranteed). 第69条 requires the
  reserve to be split into 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金; for in-scope contracts the
  保険料積立金 and 払戻積立金 may not fall below the amount computed as the Commissioner directs, and
  for out-of-scope non-separate-account contracts may not fall below the **平準純保険料式** (net
  level premium method), defined in the text as levelling the funding over the whole
  premium-paying period. 危険準備金 is split into 保険リスク, 第三分野保険リスク and 予定利率リスク components.

### R4 — 金融庁, 平成8年大蔵省告示第48号 一部改正（案）の公表 (2014-04-01)
- Publisher: 金融庁 (Financial Services Agency)
- Document: 「保険業法第百十六条第二項の規定に基づく長期の保険契約で内閣府令で定めるものについて
  の責任準備金の積立方式及び予定死亡率その他の責任準備金の計算の基礎となるべき係数の水準 （平成八年大蔵省告示第四十八号）の一部を改正する件（案）」の公表について
- Doc type: 告示改正案 (draft notification, public comment)
- URL: https://www.fsa.go.jp/news/25/hoken/20140401-3.html (attachment:
  https://www.fsa.go.jp/news/25/hoken/20140401-3/01.pdf)
- Retrieved: YES (the HTML page was fetched and read; the attached PDF was not opened)
- Content: confirms that 平成8年大蔵省告示第48号 is the instrument that sets the 標準責任準備金 積立方式, the
  予定死亡率 and the 標準利率; that the 標準利率 references "the lower of the three-year and the ten-year
  average yield on 10-year JGBs", determined annually; and that the 2014 amendment revisits
  that methodology in the light of the growth of single-premium savings products, the wider
  supply of super-long JGBs and more developed ALM. Consultation ran to 2014-05-01.

### R5 — 金融庁, 標準責任準備金制度にかかる告示の一部改正（案）等の公表 (2021-04-23)
- Publisher: 金融庁
- Doc type: 告示改正案 (draft notification, public comment)
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html (attachments 01.pdf,
  02.pdf, 03.pdf under the same directory)
- Retrieved: YES (HTML page fetched and read; attachments not opened)
- Content: amends 平成8年大蔵省告示第48号 and 平成13年金融庁告示第24号 to bring USD- and AUD-denominated
  contracts concluded on or after 2022-04-01 into 標準責任準備金 scope and to set the method for
  their 標準利率; the other amendments took effect 2021-10-01.

### R6 — 国税庁, タックスアンサー No.1755「生命保険契約に係る満期保険金等を受け取ったとき」
- Publisher: 国税庁 (National Tax Agency)
- Doc type: タックスアンサー (tax guidance), updated 2025-04-01
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1755.htm
- Retrieved: YES
- Content: where the premium payer and the recipient are the same person, a lump-sum
  maturity benefit is **一時所得**: receipts less premiums paid less a ¥500,000 special
  deduction, and only half the remainder enters 総所得金額. Where it is taken as an annuity it is
  **雑所得** (annual annuity less the premiums attributable to it), generally subject to
  withholding. Where the payer and the recipient differ, gift tax applies — on the annuity
  *right* in the annuity case.

### R7 — 国税庁, タックスアンサー No.1140「生命保険料控除」
- Publisher: 国税庁
- Doc type: タックスアンサー (tax guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Retrieved: YES
- Content: post-2012-01-01 contracts — three baskets (一般生命保険料 / 介護医療保険料 / 個人年金保険料), each
  capped at ¥40,000 of income-tax deduction, overall cap ¥120,000. Bands: premium ≤ ¥20,000
  fully deductible; ¥20,001–¥40,000 → premium × 1/2 + ¥10,000; ¥40,001–¥80,000 → premium ×
  1/4 + ¥20,000; above ¥80,000 → ¥40,000. Pre-2012 contracts: ≤ ¥25,000 full;
  ¥25,001–¥50,000 → × 1/2 + ¥12,500; ¥50,001–¥100,000 → × 1/4 + ¥25,000; above ¥100,000 →
  ¥50,000. The page covers 所得税 only.

### R8 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁
- Doc type: タックスアンサー (tax guidance), updated 2025-04-01
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Retrieved: YES
- Content: the 一般生命保険料 basket covers contracts paying on survival or death written by life
  insurers, 旧簡易生命保険契約 and agricultural-cooperative 共済 — which is the basket a 養老保険 or a 学資保険
  falls into. The 個人年金保険料 basket requires the 税制適格特約 conditions (annuitant is the payer or
  spouse, level premiums for at least 10 years, and a fixed annuity of at least 10 years or
  a life annuity generally starting at 60). Savings-type contracts with a term under five
  years are excluded.

### R9 — 生命保険協会, "２０２５年版 生命保険の動向" (industry statistics)
- Publisher: 一般社団法人生命保険協会 (Life Insurance Association of Japan)
- Document: 2025年版 生命保険の動向, 33 pp. (FY2024 figures)
- Doc type: industry statistics
- URL: https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf
- Retrieved: YES (full PDF downloaded, 33 pp., text extracted; the 個人保険 sections read)
- Content: FY2024 個人保険 新契約高 by type — 定期保険 ¥24.6666tn (43.2%), 終身保険 ¥12.9965tn (22.8%), 変額保険
  ¥10.7797tn (18.9%), **養老保険 ¥1.5347tn (2.7%)**, **こども保険 ¥347.7bn (0.6%)**. 保有契約件数 195.30
  million, of which 医療保険 45.45 million (23.3%), 終身保険 38.48 million (19.7%), 定期保険 27.21
  million (13.9%), ガン保険 25.22 million (12.9%), **養老保険 7.34 million (3.8%)**. 保有契約高
  ¥778.9902tn, of which **養老保険 ¥27.0379tn (3.5%)**. 個人保険 解約・失効率 **5.6%** in FY2024 (down 0.3
  points), against 5.9% in FY2023, 5.6% in FY2022, 4.9% in FY2021 and 4.7% in FY2020.

### R10 — 生命保険文化センター, "養老保険" (product-taxonomy page)
- Publisher: 公益財団法人生命保険文化センター (Japan Institute of Life Insurance)
- Doc type: consumer education / product taxonomy page
- URL: https://www.jili.or.jp/knows_learns/kind/main/38.html
- Retrieved: YES
- Content: 養老保険 is defined as a fixed-term contract paying a death benefit on death within
  the term and a maturity benefit on survival to the end, with the two **equal in amount**;
  terms come as 年満期 and 歳満期; it carries a savings function but the maturity benefit can fall
  short of total premiums paid; premium modes are 一時払, 年払, 半年払 and 月払.

---

## Fact extraction

### 1. What the two products are, and how they relate

- 養老保険 pays 満期保険金 on survival to the end of a fixed 保険期間 and 死亡保険金 on death within it, and
  **the two amounts are equal** [R10] [S2] [S8]. The equality is written directly into the
  約款 benefit table: both cells read 基準保険金額 [S2] or 保険金額 [S8].
- 保険料払込期間 is normally the whole 保険期間, with a short-pay option [S4].
- 学資保険 is the same chassis with the survival benefit **split into staged instalments** timed
  to school entry, and with the premium stream contingent on the survival of the
  **policyholder** rather than the insured [S1] [S3] [S10] [S13].
- The connection is explicit in one carrier's contract: converting a 学資保険 to 払済保険 turns it
  into "原保険契約と同一保険期間の保険料払済の**養老保険**", after which 祝金 and 死亡払戻金 cease and only a maturity /
  death / 高度障害 benefit equal to the 払済保険金額 remains [S10 Art 25].
- Market weight: 養老保険 is 3.8% of 個人保険 in-force policy count and 3.5% of in-force sum
  assured, and 2.7% of FY2024 new business sum assured; こども保険 is 0.6% of new business sum
  assured [R9]. Both are small relative to 医療保険 (23.3% of count) and 終身保険 (19.7%) [R9].

### 2. Issue-age and term envelopes

養老保険:

- かんぽ生命 新フリープラン: 保険期間 **10–60 years**, selectable in one-year steps [S4]. 基準保険金額
  **¥1,000,000–¥10,000,000** [S4]. Issue ages are not stated on the retrieved page.
- 明治安田生命 養老保険: **被保険者 6–75**, varying with the term [S15]. Amounts and terms are not stated
  on the retrieved page.
- 日本生命 養老保険: the retrieved 給付約款 carries no age or term table [S8]; the pricing release's
  example is 契約年齢 30, 保険期間 to 60, 保険金額 ¥5,000,000 [S9].
- Age is computed as 満年齢 at 契約日 with fractions of a year rounded — かんぽ counts months from
  the birth month to the contract month and rounds ≥ 7 months up, ≤ 6 months down
  [S2 Art 31]; 第一生命 rounds > 6 months up, ≤ 6 months down [S1 Art 33]; フコク生命 **truncates**
  [S10 Art 33]; 明治安田生命 truncates [S13]. After issue, one year is added at each 年単位の契約応当日
  [S1] [S2] [S10] [S13].

学資保険:

- かんぽ生命 はじめのかんぽ: 被保険者 **0–12** (0–5 or 0–3 on some courses), 契約者 **18–65**; 17 / 18 / 21歳満期;
  全期間払込, 12歳払込済 or 18歳払込済; 基準保険金額 **¥500,000–¥7,000,000** (¥5,000,000 on some courses) [S5].
- 明治安田生命 つみたて学資: **21歳満期**; premium-paying to age 15, or to age 10 where the child is 0–2;
  契約者 **18–65**, the upper limit stated to move with market rates [S14].
- フコク生命 みらいのつばさ: **22歳満期**; premium-paying to ages **5, 11, 14 or 17** [S11] [S12]. The 約款
  admits 契約年齢 bands of 0–1, 2–4 and 5–7 for the child in its 祝金 grid, so the child issue-age
  range is 0–7 [S10 Art 3]. Policyholder must be the child's parent or a supporting relative
  within the insurer's age range [S10 Art 1].
- ソニー生命: terms **17 / 18 / 20 / 22歳満期**; premium-paying periods including to ages 10, 15, 17
  and 18 [S16].
- 日本生命 ニッセイ学資保険: 学資年金開始年齢 chosen at issue and fixed thereafter; the documented examples use
  18 with an 18-year premium-paying period, and the 保険期間 runs to 23 in the illustration
  (five annual instalments from 18) [S7].
- 第一生命 こども学資保険: 18歳満期 and 22歳満期 [S1 Art 2].
- Prenatal entry is standard: **140 days** before the expected date of birth at 明治安田生命 [S13]
  [S14] and ソニー生命 [S16] (III型 within 91 days [S16]); フコク生命 has a 出生前加入特則 [S10 Arts 38–45];
  かんぽ生命 has an "お子さまの出生前に加入する場合" section and a special age rule setting the child's 契約年齢 to
  0 [S3 Art 47]. On stillbirth or miscarriage the contract is void and premiums are refunded
  [S13].

### 3. 養老保険 benefit definitions and triggers

- 死亡保険金 and 満期保険金 both equal 基準保険金額 / 保険金額 [S2 Art 1] [S8 Art 1].
- **Juvenile graded death benefit** (かんぽ生命): if the insured dies before age 3 the death
  benefit is 50% of 基準保険金額; before age 6, 80%. If the graded amount would fall below the 積立金
  (the policy reserve), the 積立金 is paid instead [S2 Art 1(2)–(3)].
- **重度障害** (severe disability) is treated as death: on notice, the insurer deems the insured
  to have died on the notice date and applies the death-benefit provisions — but not the
  double payment [S2 Art 2(1)]. The policyholder may instead elect the premium-waiver
  treatment and keep the contract in force [S2 Art 2(4)]. 明治安田生命 likewise pays a 高度障害保険金
  that terminates the contract [S15].
- **保険金の倍額支払** (double indemnity, かんぽ生命): an amount equal to the death benefit is paid again
  if the insured dies from a listed accident within 180 days of it, or from a listed
  infectious disease, provided **1年6か月** has elapsed from 契約日 (6 months from 復活日 on a
  reinstated policy). Excluded for disease-caused accidents, gross negligence or intent of
  the policyholder / insured / named beneficiary, crime, mental disorder, intoxication,
  unlicensed driving and drink-driving [S2 Art 3].
- **Death-benefit multiples** (かんぽ生命 新フリープラン): the same contract is sold as 定額型 (death
  ¥5,000,000, maturity ¥5,000,000), 2倍保障型 (¥5,000,000 / ¥2,500,000), 5倍保障型 (¥5,000,000 /
  ¥1,000,000) and 10倍保障型 (¥5,000,000 / ¥500,000) [S4]. Only the 定額型 is the textbook
  endowment.
- **War risk**: the death benefit may be reduced where the increase in deaths affects the
  pricing basis, but never below the 積立金 / 責任準備金 [S2 Art 4] [S8 Art 2].

### 4. 養老保険 exclusions, grace, lapse and reinstatement

- **Suicide**: excluded for **three years** from 責任開始の日 (from 復活の責任開始の日 on a reinstated
  contract) [S2 Art 1(4)] [S8 Art 1]. Where the exclusion bites, かんぽ生命 pays the 積立金
  [S2 Art 35(2)] and 日本生命 pays the 責任準備金 [S8 Art 1(3)]. This is materially longer than the
  twelve months used in the UK composite.
- Intentional killing by the policyholder or a named death-benefit beneficiary is also
  excluded; 日本生命 pays 解約払戻金 where the policyholder caused the death and 責任準備金 where the
  beneficiary did [S8 Art 1(3)].
- **Premium due windows and grace** (かんぽ生命): the first premium is due from the day
  responsibility starts to the end of the following month, with grace to the day before the
  月ごとの契約応当日 in the **third month** after that window; the second and later premiums are due
  in the month containing the 月ごとの契約応当日, with the same three-month-style grace
  [S2 Arts 9–10]. Failure to pay the first premium rescinds the contract; failure on later
  premiums makes it lapse [S2 Art 11].
- **復活** (reinstatement): かんぽ生命 allows it **within one year** of lapse, subject to
  underwriting, blocked if the surrender value has been claimed or if the reinstated amount
  would exceed the statutory 加入限度額; the reinstated contract is treated as never having
  lapsed, except that benefits and waivers triggered between lapse and reinstatement are not
  paid [S2 Arts 36–38].
- **払済保険** (paid-up conversion): available after **two years** from 契約日, resetting the
  基準保険金額, subject to a minimum [S2 Art 30].
- **契約者貸付**: available within a computed portion of the surrender value; interest accrues at
  a rate the insurer sets; the loan term is one year, extendable; if unpaid one year past
  the loan term the insurer nets the loan against the 積立金 and reduces the 基準保険金額. The
  provision expressly contemplates loans "made for the purpose of switching into premium",
  which is the かんぽ form of automatic premium loan [S2 Art 39]. 日本生命 has a plain 契約者貸付 in the
  養老保険 給付約款 [S8 Art 9].
- Surrender value (返戻金) is computed from the elapsed years and months of the contract and is
  payable on 解除, on notice of 解約, on lapse, on a reduction of the sum assured, and where a
  death-benefit exclusion bites [S2 Art 35].

### 5. 学資保険 survival-benefit schedules — the observed designs

第一生命 こども学資保険 [S1 Art 2], as a percentage of 基準保険金額:

| Type | 学資金 | 満期保険金 | Total |
|---|---|---|---|
| 18歳満期 | 50% at 満15歳 | 100% | 150% |
| 22歳満期 | 100% at 満18歳 | 100% | 200% |

The 学資金 is paid on the **first 2月1日** after the stated age is attained (with the age reduced
by one for children born 2 February to 1 April) [S1 Art 2].

かんぽ生命 はじめのかんぽ [S3 Art 1], as a percentage of 基準保険金額:

| Type | 学資祝金 | 満期保険金 | Total |
|---|---|---|---|
| 17・18歳満期 (no 祝金) | — | 100% | 100% |
| 学資祝金付17・18歳満期 | 5% at 満5歳8か月, 10% at 満11歳8か月, 15% at 満14歳8か月 | 100% | 130% |
| 学資祝金付21歳満期 | 25% at each of ages 18, 19, 20 | 25% | 100% |

The 学資祝金 on the 17・18歳満期 shapes are paid on the **12月1日** following the stated age; on the
21歳満期 shape they are paid at the attained contractual ages [S3 Art 1]. Worked example on
基準保険金額 ¥3,000,000: 祝金 ¥150,000 + ¥300,000 + ¥450,000 and 満期保険金 ¥3,000,000, total receipts
¥3,900,000 [S3].

フコク生命 みらいのつばさ [S10 Art 3], as a percentage of 保険金額, by the child's 契約年齢:

| 被保険者の満年齢 | 契約年齢 0–1 | 契約年齢 2–4 | 契約年齢 5–7 |
|---|---|---|---|
| 2歳7ヵ月 | 5% | — | — |
| 5歳7ヵ月 | 5% | 5% | — |
| 11歳7ヵ月 | 10% | 10% | 10% |
| 14歳7ヵ月 | 10% | 10% | 10% |
| 17歳7ヵ月 | 70% | 70% | 70% |
| 19歳7ヵ月 | 10% | 10% | 10% |

That is the **S(ステップ)型**. The **J(ジャンプ)型** pays a single 祝金 of **100%** at 17歳7ヵ月
[S10 Art 3]. Both then pay 満期保険金 = 保険金額 at 22歳満期 [S10 Art 3]. So S型 at 契約年齢 0–1 returns 110%
+ 100% = 210% of 保険金額 and J型 returns 100% + 100% = 200% — which is exactly what the model
plans show on a ¥1,000,000 maturity benefit: receipts of ¥2,100,000 and ¥2,000,000 [S11]. 祝金
are paid on the 11月1日 following the stated age [S10 Art 3].

日本生命 ニッセイ学資保険 [S7]:

- 学資年金 in **five** annual instalments from the 学資年金開始日 (the 契約応当日 at which the child reaches
  the elected 学資年金開始年齢): the first equal to **基準保険金額**, the second to fifth each **50% of
  the first**. Total = 300% of 基準保険金額.
- こども祝金あり型 adds three payments of **20% of 基準保険金額** on the 2月1日 following ages 5歳10カ月,
  11歳10カ月 and 14歳10カ月; total then 360% of 基準保険金額 [S7].
- Worked illustration: 基準保険金額 ¥1,000,000, child aged 0, 学資年金開始年齢 18, 18-year premium-paying
  period — receipts ¥1,000,000 + 4 × ¥500,000 = ¥3,000,000 (祝金なし型), or with three ¥200,000
  祝金, ¥3,600,000 [S7].
- The type (祝金 present or absent) cannot be changed after issue [S7].
- 学資年金 may be commuted to a lump sum equal to the present value of the remaining
  instalments, at which point the contract terminates [S7].

明治安田生命 つみたて学資 [S13] [S14]:

- 教育資金 equal to **基準保険金額** on the 10月1日 following each of ages 18, 19 and 20 (age reduced by
  one for children born 2 October to 1 April), plus **満期保険金 = 基準保険金額** at 21歳満期. Total =
  400% of 基準保険金額.
- 教育資金 are automatically accumulated at a rate the insurer sets unless the policyholder asks
  otherwise [S13].

ソニー生命 [S16]: three types — I型 spreading the fund across 中学・高校・大学 entry, II型 weighting it to
university entry, III型 paying it over the years after university entry. The retrieved pages
give plan-level receipts and 返戻率 but not the percentage grid.

Deferral of paid 祝金 is the default at three carriers: 第一生命 automatically defers 学資金 with
interest unless the policyholder asks otherwise [S1 Art 4]; フコク生命 does the same [S10 Art 4];
明治安田生命 does the same for 教育資金 [S13].

### 6. 学資保険 death benefit on the child — a return of premium, not a sum assured

None of the retrieved 学資保険 contracts pays a sum assured on the child's death. The four
observed definitions:

- **第一生命**: 死亡給付金 = (基準保険金額に対応する月払保険料) × (経過月数), where 経過月数 runs from 契約日 to the day before
  the 月単位の契約応当日 following death during the premium-paying period, and to the end of the
  premium-paying period after it. Rider premiums are excluded [S1 Art 2 Table 1].
- **かんぽ生命**: 死亡給付金額 = the **greater** of (i) 保険料額 × 経過月数, less 学資祝金 already paid and less
  unpaid premium and loan principal plus interest, and (ii) the **積立金** (the policy reserve)
  [S3 別表1]. 保険料額 is taken at the account-debit rate.
- **明治安田生命**: during the premium-paying period, 月掛保険料相当額 × 経過年月数; after it, the greater of
  that amount less 教育資金 already triggered, and the 積立金相当額 [S13].
- **フコク生命**: 死亡払戻金 = the **責任準備金相当額** at the date of death, full stop [S10 Art 3].
- **日本生命**: 死亡保険金 per 別表2 of the 給付約款, which was not in the retrieved files — the しおり shows
  a worked case with a ¥400,000 death benefit and states that 解約払戻金 is capped at the death
  benefit and that こども祝金 payments reduce the surrender value [S7].

Because the death benefit is a return of premiums (or of the reserve), the child's mortality
is a near-zero-strain decrement: at ages 0–22 the 標準生命表2018 death rates run from 0.00081
down to 0.00007 and back to 0.00066 [R1].

Exclusions on the child's death benefit are narrow: intentional killing by the policyholder
[S1 Art 2] [S3 Art 1] [S10 Art 3], and war [S1 Art 3(7)] [S3 Art 2]. Where the intent
exclusion bites, 第一生命 pays nothing at all (no 責任準備金) [S1 Art 3(6)], かんぽ生命 pays the 返戻金
[S3 Art 1 note 3] and フコク生命 pays nothing [S10 Art 3(5)].

### 7. 保険料払込免除 — the waiver on the policyholder, the product's defining mechanic

This is a decrement on a life who is **not** the insured. The triggers, as written:

| Carrier | Death | 高度障害 / 重度障害 | Accident-caused 身体障害 | Other |
|---|---|---|---|---|
| 第一生命 [S1 Art 7] | during 保険料払込期間 | from injury or disease after 責任開始期, during 保険料払込期間 | within **180 days** of a listed accident, during 保険料払込期間 | — |
| かんぽ生命 学資 [S3 Art 3] | yes | from disease or injury after 責任開始時 | — | — |
| かんぽ生命 養老 [S2 Art 6] | **accident or listed infectious disease only**, and only where the policyholder is the insured's parent, grandparent or elder sibling and the child is under **10** | from disease or injury after 責任開始時 | — | — |
| フコク生命 [S10 Art 5] | during 保険料払込期間 | from a cause after 責任開始期, during 保険料払込期間 | within **180 days** of a listed accident, during 保険料払込期間 | — |
| 明治安田生命 I型 [S13] | yes | 身体障害表 第1級・第2級 | — | II型 adds a malignant-neoplasm diagnosis more than **90 days** after 責任開始日, but only I型 is currently sold |
| ソニー生命 [S16] | yes | 所定の高度障害状態 | within **180 days** of an accident | — |
| 日本生命 [S7] | during 保険料払込期間 | not in the main contract | not in the main contract | a 契約者保障保険料払込免除特約 exists as a rider [S6 Arts 6, 18] |
| 日本生命 養老 [S8 Art 6] | not in the main contract | not in the main contract | not in the main contract | a 保険料払込免除特約 is attachable |

Carve-outs on the waiver:

- **Suicide of the policyholder**: excluded for **three years** from 責任開始期の属する日 at 第一生命
  [S1 Art 7] and かんぽ生命 [S3 Art 3], for **three years** from 責任開始の日 at 日本生命 [S7], and for
  only **two years** at フコク生命 [S10 Art 6].
- Intentional act of the 後継保険契約者 [S1 Art 7] [S7], or of the 被保険者 [S3 Art 3] [S10 Art 6].
- War and civil disturbance, subject to a pricing-materiality override that restores the
  waiver where the extra deaths are immaterial to the basis [S1 Art 7(4)] [S10 Art 6(2)].
- On the accident-caused 身体障害 trigger only: gross negligence, crime, mental disorder,
  intoxication, unlicensed driving, drink-driving, earthquake, eruption, tsunami and war
  [S1 Art 7] [S10 Art 6].

Consequences of the waiver, which is what a model has to implement:

1. **The policy continues in full.** Every future benefit — 学資金, 満期保険金, 死亡給付金 — is paid on
   schedule, and each future premium is treated as having been paid on its 契約応当日
   [S1 Art 7(6)] [S10 Art 5(5)] [S13].
2. The waiver bites from the **next 払込期月 / next 月単位の契約応当日** after the triggering event
   [S1 Art 7(1)] [S10 Art 5] [S13].
3. Contract alterations are frozen afterwards: 第一生命 disallows 基準保険金額の減額, 保険契約者の変更 and 転換
   [S1 Art 7(7)]; フコク生命 disallows the 保険期間満了日の繰り上げ and everything from 払込方法の変更 to 契約者の変更
   [S10 Art 5(6)]; 日本生命 refuses a 保険契約者の変更 while premiums are waived [S6 Art 10(4)].
4. **If the waiver does not apply, the contract dies with the policyholder.** 第一生命
   terminates the policy at the policyholder's death and pays the 責任準備金 to the
   policyholder's legal heirs [S1 Art 7(8), Art 30(2)]; フコク生命 does the same [S10 Art 6(3)];
   日本生命 lists 3-year suicide, 後継保険契約者の故意 and war as the three ways the 学資保険 is extinguished
   by the policyholder's death [S7].
5. **Succession.** 第一生命 requires a 後継保険契約者 (successor policyholder) to be nominated at issue
   from the insured or the insured's parents or relatives, and all rights and obligations
   pass to that person on the policyholder's death [S1 Arts 29–30]. フコク生命 instead makes the
   **insured child** succeed to the policyholder's rights on the death or 高度障害 waiver
   [S10 Art 5(4)]. 日本生命 uses a 後継保険契約者 and makes them the benefit recipient [S7].
6. **A grace-period trap.** If the waiver event happens while a premium is unpaid inside the
   grace period, the unpaid premium must be paid by the end of that grace period or **the
   waiver is refused** [S1 Art 14(4)] [S10 Art 17(2)] [S6 Art 7(7)].
7. The waiver is underwritten on the **policyholder**: the 告知義務 is the policyholder's, and
   it is re-imposed on a 保険契約者の変更 and on 復活 [S1 Art 20] [S10 Art 5(3)] [S6 Art 14].
   Contestability is two years from 責任開始期 [S1 Art 22(3)] [S6 Art 16(1)(5)].
8. A waiver can be undone: 告知義務違反 rescission after a waiver has begun restores the premium
   obligation retrospectively, unless the claimant proves the waiver event was unconnected
   to the undisclosed fact [S1 Art 21(2)–(3)] [S6 Art 15(2)–(3)].

The relevant decrement rates for a policyholder in the 25–45 band, on the statutory
valuation table, are q(x) = 0.00067 (25), 0.00068 (30), 0.00077 (35), 0.00118 (40), 0.00177
(45) male and 0.00029, 0.00037, 0.00059, 0.00088, 0.00122 female [R1].

### 8. Premium structure, modes and published rates

- Modes: 月払, 半年払 (半年一括払), 年払 (年一括払), 一時払 [R10] [S1 Art 10] [S10 Art 14]. 日本生命's 学資保険 base
  contract offers **monthly and annual only** [S6 Art 4].
- Prepayment discounts: 第一生命 discounts 3+ months of monthly premiums paid together and
  discounts 前納 of 2+ annual premiums at a stated rate [S1 Arts 12–13]; フコク生命 discounts 3–12
  months of monthly premiums and 前納 of 2+ years (annual) or 1+ year (semi-annual)
  [S10 Art 18]; 日本生命 does the same [S6 Art 6]; かんぽ生命 discounts 前納 [S2 Art 14].
  "保険料は、まとめて払うほど払込保険料総額が割安となり、返戻率が高くなります" [S16].
- **Volume discounts on the rate itself.** 日本生命's 学資保険 premium unit rate per ¥100,000 of
  基準保険金額 (契約者 30 male, child 0, 学資年金開始年齢 18, 18-year premium-paying period, monthly, account
  debit) is **¥1,313** at 基準保険金額 ≥ ¥1,000,000, **¥1,343** at ¥700,000 to under ¥1,000,000
  and **¥1,373** below ¥700,000 [S7]. 明治安田生命 gives a **¥30 per ¥100,000** monthly discount
  at 基準保険金額 ≥ ¥700,000 and none below (×6 semi-annual, ×12 annual) [S13]. Reducing the sum
  assured can therefore push the policy into a worse rate band [S13].
- **Published 予定利率** (assumed interest rate), one carrier, for contracts dated on or after
  2025-01-02 [S9]:

  | Product group | Before | After |
  |---|---|---|
  | 学資保険・こども保険 | 0.85% | **1.00%** |
  | 年金保険・**養老保険**（一時払を除く）・生存給付金付定期保険・長寿生存保険（低解約払戻金型） | 0.60% | **1.00%** |
  | 終身保険（一時払を除く）・長期定期保険・傷害保障重点期間設定型長期定期保険 | 0.25% | **0.40%** |

  Described in the release as the first 予定利率 increase in about 40 years [S9].
- **契約貸付利率** at the same carrier: 2.00% → **2.40%** for contracts dated on or after
  2025-01-02 [S9].
- **Published premium rates** [S9]:

  | Product | Basis | Before | After |
  |---|---|---|---|
  | 学資保険 (祝金なし型) | 契約者 30 male, child 0, 学資年金開始/払込満了 18, 基準保険金額 ¥1,000,000, monthly | ¥13,350 | **¥13,130** |
  | 同, 契約者 female | same | ¥13,290 | ¥13,080 |
  | こども保険 | 契約者 30 male, 被保険者 22, 基準保険金額 ¥1,500,000, monthly | ¥9,696 | ¥9,592 |
  | **養老保険** | 契約年齢 30, 満期 60, 保険金額 ¥5,000,000, male, monthly | ¥15,195 | **¥15,095** |
  | 同, female | same | ¥15,095 | ¥14,990 |

  The 学資保険 figure ties exactly to the しおり unit rate: ¥1,313 × 10 = ¥13,130 [S7] [S9].
- Derived from those two rows: the 養老保険 example pays ¥15,095 × 12 × 30 = **¥5,434,200** for
  a ¥5,000,000 maturity benefit, a ratio of **92.0%** — an endowment at a 1.00% 予定利率 does
  not return premiums (derived from [S9]). The 学資保険 example pays ¥13,130 × 12 × 18 =
  **¥2,836,080** for receipts of ¥3,000,000, a 返戻率 of **105.8%** (derived from [S7] [S9]).
- Interest is credited on deferred benefits and on prepaid premiums at rates the insurer
  sets and may change with market rates [S1 Art 4] [S10 Art 4] [S13].

### 9. Published 返戻率 (return ratios) — the number these products are sold on

| Carrier | Plan | Receipts | Premiums | 返戻率 |
|---|---|---|---|---|
| 日本生命 [S7] [S9] | 祝金なし型, 基準保険金額 ¥1,000,000, 18歳開始, 18-year pay | ¥3,000,000 | ¥2,836,080 | 105.8% (derived) |
| フコク生命 [S11] | S型, 17歳払込, 満期 ¥1,000,000 | ¥2,100,000 | ¥1,845,588 | approx. 113.7% |
| フコク生命 [S11] | J型, 17歳払込, 満期 ¥1,000,000 | ¥2,000,000 | ¥1,721,556 | approx. 116.1% |
| ソニー生命 [S16] | I型, 基準学資金 ¥1,000,000, 18歳満期 | — | — | 116.0% |
| ソニー生命 [S16] | III型, 基準学資金 ¥400,000, 22歳満期, 18歳まで払込 | ¥2,000,000 | ¥1,688,256 | 118.4% |
| ソニー生命 [S16] | II型, 基準学資金 ¥2,000,000, 18歳満期 | — | — | 121.3% |
| フコク生命 [S11] | J型, 11歳払込, 満期 ¥1,000,000 | ¥2,000,000 | ¥1,614,492 | approx. 123.8% |
| ソニー生命 [S16] | III型, 基準学資金 ¥400,000, 22歳満期, 10歳まで払込 | ¥2,000,000 | ¥1,580,640 | 126.5% |
| ソニー生命 [S16] | III型, 基準学資金 ¥400,000, 22歳満期, 10歳まで払込, **年払** | ¥2,000,000 | — | 127.4% |
| 明治安田生命 [S14] | I型, 契約者 25 male, child 0, 21歳満期, 基準保険金額 ¥700,000, **一括払込** | — | — | up to 129.2% |
| フコク生命 [S12] | J型, 5歳払込 | ¥2,000,000 | — | approx. 131.3% |

Observed range across the six carriers: **105.8% to 131.3%**. The drivers, in the order the
documents give them, are (i) the shortness of the premium-paying period relative to the
benefit dates, (ii) payment frequency, and (iii) the volume band of the 基準保険金額 [S7] [S13]
[S16]. By contrast, a plain 養老保険 at the same carrier's 1.00% 予定利率 returns 92.0% (derived
from [S9]) — the 学資保険 return premium comes from the child's near-zero mortality cost, not
from a better interest basis.

### 10. Surrender values, paid-up, reduction and loans

- Surrender value is a function of elapsed years and months since 契約日, capped at the
  premium-paid duration where the elapsed term exceeds it: 第一生命 computes 解約返還金 from 経過年月数
  (or 払込年月数 if smaller) **and the timing of the 学資金 payments** [S1 Art 24]; フコク生命 from 経過年月数
  with the same cap [S10 Art 23 and note]; かんぽ生命 from 経過した年月数 [S2 Art 35(2)] [S3].
- 日本生命 states outright that the surrender value is usually **less than total premiums paid**
  and, in the early durations, "まったくないか、あってもごくわずか"; it is **capped at the death benefit**;
  and each こども祝金 paid reduces it [S7].
- **基準保険金額の減額**: the reduced portion is treated as a partial surrender and its surrender
  value released; future premiums are re-rated [S1 Art 26] [S10 Art 26] [S6 Art 9]
  [S2 Art 29]. 日本生命 refuses a reduction once the 学資年金開始日 has arrived [S6 Art 9(4)].
- **払済保険**: フコク生命 converts a 学資保険 into a paid-up **養老保険** of the same term, using the
  surrender value as a single premium; 祝金 and 死亡払戻金 then cease and the paid-up policy pays
  満期保険金 / 死亡保険金 / 高度障害保険金 all equal to the 払済保険金額 [S10 Art 25]. The policyholder may revert
  to the original contract within **two years** [S10 Art 27]. かんぽ生命's 養老保険 allows 払済 after
  two years [S2 Art 30]. 明治安田生命 does **not** offer 払済保険 or 延長定期保険 on つみたて学資 [S13].
- **契約者貸付**: 第一生命 [S1 Art 27], フコク生命 [S10 Art 31], かんぽ生命 [S2 Art 39], 日本生命 [S7] [S8 Art 9].
  Where the loan principal plus interest exceeds the surrender value, the contract lapses —
  第一生命 gives notice and lapses the policy on the day after the end of the month following
  the notice month [S1 Art 27(5)–(6)]; フコク生命 lapses it immediately [S10 Art 31(4)]; 日本生命
  runs a 基準日 test and re-tests [S7]; かんぽ生命 instead nets the loan off the 積立金 and reduces the
  sum assured [S2 Art 39(6)].
- Loans and unpaid premiums are netted off every benefit payment [S1 Art 3(9)] [S10 Art 32]
  [S3 別表1] [S6 Art 4(5)].

### 11. Grace, lapse, automatic premium loan and reinstatement — 学資保険

- **Grace**: monthly premiums — from the first day of the month after the 払込期月 to its last
  day at 第一生命 [S1 Art 14] and フコク生命 [S10 Art 14]. Semi-annual and annual — to the 月単位の契約応当日
  in the second following month, with a February/June/November special rule [S1 Art 14]
  [S10 Art 14]. かんぽ生命 runs to the day before the 月ごとの契約応当日 in the **third** month after the
  payment window [S2 Arts 9–10]. 日本生命 has **no grace article**: it serves a demand and
  rescinds the contract at the 月ごと応当日 in the third month after the due month [S6 Art 7].
- **保険料の自動貸付 (automatic premium loan)** keeps the contract alive past the grace period:
  - 第一生命: lends the premium equivalent automatically unless the policyholder has opted out,
    while the loan plus interest stays inside the surrender value; for monthly contracts it
    lends to the next 半年単位の契約応当日, or as many months as the value permits. The loan is deemed
    made at the end of the grace period. Interest is capped at 年8% (半年4%, 月8/12%)
    [S1 Art 15]. The policyholder can undo the APL by surrendering within **three months**
    [S1 Art 16].
  - フコク生命: lends **six months** of premium at a time on monthly contracts, on the test that
    the surrender value computed as if those six premiums had been paid exceeds the six
    premiums plus interest; interest capped at 年8% (半年4% on monthly and semi-annual).
    Opt-out available. Undoable within three months by surrender, 払済 or reduction
    [S10 Art 19].
  - かんぽ生命 has no separate APL article but its 契約者貸付 expressly contemplates loans "made for
    the purpose of switching into premium" [S2 Art 39].
  - **日本生命 and 明治安田生命 do not offer it** — 日本生命's 契約基本約款 has no APL article [S6], and 明治安田生命
    states outright that 自動振替貸付 is not handled [S13].
- **復活 (reinstatement)**: within **three years** of lapse at 第一生命 [S1 Art 17] and フコク生命
  [S10 Art 20]; within **one year** at かんぽ生命 [S2 Art 36]; **not offered** at 明治安田生命 [S13];
  not present in 日本生命's 契約基本約款 [S6]. Reinstatement restarts the 責任開始期 for the waiver, the
  suicide clock and contestability [S1 Art 17(3)] [S10 Art 5 note 2] [S2 Art 37]. Benefits
  and waivers that fell due during the lapsed period are not paid [S2 Art 38 note]
  [S3 Art 3]. One special rule: 第一生命 and フコク生命 pay a 学資金 whose payment age was reached
  **while the policy was lapsed**, but only if the policy is subsequently reinstated
  [S10 Art 3(2)].

### 12. Riders (特約) and packaged cover

- **育英年金 (educational annuity on the policyholder's death)** exists as a rider: 第一生命's
  ５年ごと配当付育英年金特約 is referenced throughout the main 約款 (its premium is excluded from the 死亡給付金
  formula, and its 特約育英年金 recipient is named in the creditor-surrender article)
  [S1 Art 2 Table 1 note 1, Art 25(2)]. 日本生命's こども保険（有配当2012）carries 育英年金 in its main
  contract, and the shared 契約基本約款 names 育英年金受取人 throughout [S6]. Neither 育英年金 rider's own
  特約条項 was retrieved, so its benefit amount, term and taper are [unverified].
- **医療特約 on 学資保険**: かんぽ生命 allows up to three of 無配当災害特約, 無配当傷害医療特約（R04）, 無配当総合医療特約（R04）and
  無配当先進医療特約（無解約返戻金型） [S3] [S5]; the 先進医療特約 is a **10-year auto-renewing 無解約返戻金型** rider
  whose term is capped at the base contract's [S3]. 第一生命 offers 傷害特約Ｄ（５年ごと配当付こども学資保険用） and
  こども新総合医療特約Ｄ（Ｈ22）[S1 Art 2 Table 1 note 1]. 日本生命 sells こども総合医療保険（有配当2012）as a separate 保険契約
  sharing the same 契約基本約款 [S6]. フコク生命 packages a child medical policy, except on prenatal
  contracts, grandparent- policyholder contracts and the 5歳払込 option [S12]. **明治安田生命
  attaches no riders at all** to つみたて学資 [S13] [S14].
- 保険料払込免除不担保特則 exists at 第一生命 — the policyholder can buy the product **without** the waiver
  [S1 概要]. A mirror-image arrangement exists at 日本生命, where the waiver beyond simple death
  is bought as 契約者保障保険料払込免除特約 [S6].
- リビング・ニーズ特約 is attached automatically to 終身保険 and 養老保険 at 日本生命 [S8].
- 兄弟割引 (sibling discount) from the second child at フコク生命, implemented through a 兄弟加入特則 in
  the 約款 [S10 Art 46] [S12]; the discount amount is not published [S12].
- 明治安田生命 limits つみたて学資 to **one policy per insured child** and issues no policy document,
  only a 「ご契約締結内容通知書」 [S13].

### 13. Dividends (契約者配当) and the profit basis

- Both product families are sold in 有配当 and 無配当 forms. 第一生命's こども学資保険 is ５年ごと配当付: dividends
  are allotted at each fifth 年単位の契約応当日 from 契約日 (and at the day after 保険料払込期間満了), at
  maturity, and on termination — with a lower allotment where the policy ends other than by
  death, and a two-year minimum duration for non-death terminations [S1 Art 35]. フコク生命's
  みらいのつばさ is likewise ５年ごと配当付 [S10 Art 21].
- 日本生命's 学資保険（有配当2013）and 養老保険（有配当2012）are 有配当 (社員配当) [S6 Arts 20–21] [S8].
- かんぽ生命's 普通養老保険 allots 契約者配当 annually to policies reaching designated anniversary dates,
  and separately on a long-duration basis [S2 Arts 40–41].
- **明治安田生命's つみたて学資 pays no dividend at all** [S13], and ソニー生命's 学資保険 is 無配当 [S16].
- No retrieved document publishes a dividend scale, a 利差/死差/費差 split, or a 予定事業費率.

### 14. Tax treatment

- **Lump-sum 満期保険金 where the premium payer and the recipient are the same person is 一時所得**:
  receipts less premiums paid less a ¥500,000 special deduction, of which only half enters
  総所得金額 [R6]. Where the payer and the recipient differ, gift tax applies [R6].
- **Staged payments are 雑所得, not 一時所得.** 日本生命 states 学資年金 = 雑所得 and こども祝金 = 一時所得 [S7].
  明治安田生命 states that **both** the 教育資金 and the 満期保険金 of つみたて学資 are 雑所得, with 雑所得 = payment −
  必要経費 and 必要経費 = (総払込保険料 ÷ 教育資金・満期保険金の受取総額) × payment [S13]. This is the annuity treatment
  of R6 applied to a benefit stream — the split matters, because 一時所得 gets a ¥500,000
  deduction and a 1/2 inclusion while 雑所得 gets neither.
- On the **policyholder's** death the right under the policy is inheritance-taxable
  property; the later 教育資金 and 満期保険金 are then taxed as 雑所得 only on the part not already
  caught by inheritance tax [S13].
- Premiums fall in the **一般生命保険料控除** basket — contracts paying on survival or death [R8] —
  capped at ¥40,000 of income-tax deduction on post-2012 contracts, within an overall
  ¥120,000 cap across the three baskets [R7]. Neither 養老保険 nor 学資保険 reaches the 個人年金保険料
  basket, whose 税制適格 conditions require the annuitant to be the payer or spouse, level
  premiums for 10+ years, and a 10-year-certain or life annuity generally from age 60 [R8].
- 明治安田生命 dates its tax note to 2026年1月現在 [S13]; 日本生命 to 2026年1月現在 [S7]; 国税庁 last updated
  both tax answers on 2025-04-01 [R6] [R8].

### 15. Valuation and regulatory framing

- 標準責任準備金 scope is set by 保険業法施行規則第68条: all life contracts except separate-account contracts
  whose reserve varies with the fund, contracts holding no 保険料積立金 or 払戻積立金, and contracts
  whose 約款 lets the insurer change the 予定利率 (unless a floor above the notified rate is
  guaranteed) [R3]. A conventional 養老保険 or 学資保険 is therefore in scope.
- 第69条 requires 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金; for in-scope contracts the 保険料積立金 may not
  fall below the amount computed as the Commissioner directs, and for out-of-scope contracts
  not below the **平準純保険料式** — defined in the regulation as levelling the funding over the
  whole premium-paying period [R3]. 危険準備金 splits into 保険リスク, 第三分野保険リスク and 予定利率リスク [R3].
- The Commissioner's instrument is 平成8年大蔵省告示第48号, which sets the 積立方式, the 予定死亡率 and the
  標準利率; the 標準利率 references the lower of the three-year and ten-year average yield on
  10-year JGBs and is determined annually [R4]. USD- and AUD-denominated contracts written
  on or after 2022-04-01 were brought into scope by the 2021 amendments [R5].
- The 予定死亡率 is 標準生命表2018, produced by 日本アクチュアリー会 under FSA commission and applicable from
  April 2018 [R1] [R2]. It is a **valuation** table with safety margins built in —
  observation years 2008, 2009 and 2011, select truncation at 10 years, policy years to 30
  [R2] — so it is not a best-estimate experience basis.
- The 約款 use "積立金" and "責任準備金" interchangeably for the reserve: かんぽ生命 defines 積立金 as
  "会社の定める方法によって計算される基本契約に対する責任準備金" [S2 Art 1 note 3] [S3 別表1 note 5], and 明治安田生命 defines it
  identically [S13]. The reserve is therefore a contractual floor on several benefits
  (juvenile graded death benefit, war-risk reduction, 学資保険 death benefit) and not only a
  balance-sheet quantity.
- Persistency benchmark: 個人保険 解約・失効率 was **5.6%** in FY2024, 5.9% in FY2023, 5.6% in FY2022,
  4.9% in FY2021 and 4.7% in FY2020 [R9]. No retrieved source gives a lapse curve by
  duration, and none gives one for 養老保険 or こども保険 specifically.

---

## Variation across carriers

| Feature | 第一生命 | かんぽ生命 | 日本生命 | フコク生命 | 明治安田生命 | ソニー生命 |
|---|---|---|---|---|---|---|
| 学資 maturity age | 18 / 22 [S1] | 17 / 18 / 21 [S5] | 学資年金開始年齢 elected, five instalments [S7] | 22 [S10] | 21 [S14] | 17 / 18 / 20 / 22 [S16] |
| Total receipts as % of 基準保険金額 | 150% / 200% [S1] | 100% / 130% / 100% [S3] | 300% (祝金なし) / 360% (祝金あり) [S7] | 210% (S型) / 200% (J型) [S10] [S11] | 400% [S13] | not published [S16] |
| 学資金 payment date rule | first 2月1日 after the age [S1] | 12月1日 after the age (17・18歳満期) [S3] | 2月1日 after the age (祝金); 契約応当日 (年金) [S7] | 11月1日 after the age [S10] | 10月1日 after the age [S13] | not published [S16] |
| Child death benefit | cumulative monthly premium [S1] | max(premiums − benefits − loans, 積立金) [S3] | 別表2 schedule, capped surrender value [S7] | **責任準備金相当額** [S10] | max(premiums − benefits, 積立金) [S13] | not published [S16] |
| Waiver triggers | death / 高度障害 / accident 180日 [S1] | death / 重度障害 (学資) [S3]; accident-only death + 重度障害, child under 10 (養老) [S2] | **death only** in the main contract; more via rider [S7] [S6] | death / 高度障害 / accident 180日 [S10] | death / 身体障害 1–2級; II型 adds cancer at 90日 [S13] | death / 高度障害 / accident 180日 [S16] |
| Waiver suicide carve-out | **3 years** [S1] | **3 years** [S3] | **3 years** [S7] | **2 years** [S10] | not published [S13] | not published [S16] |
| Who succeeds on waiver | 後継保険契約者 nominated at issue [S1] | policyholder change machinery [S3] | 後継保険契約者 [S7] | **the insured child** [S10] | 承継保険契約者 [S13] | not published [S16] |
| Grace (monthly) | to end of following month [S1] | to the 3rd month's 契約応当日 [S2] | **none** — rescission at the 3rd month [S6] | to end of following month [S10] | not published | not published |
| 保険料の自動貸付 | yes, ≤ 年8% [S1] | as a purpose-built 契約者貸付 [S2] | **no** [S6] | yes, 6 months at a time, ≤ 年8% [S10] | **no** [S13] | not published |
| 復活 | **3 years** [S1] | **1 year** [S2] | not in the base 約款 [S6] | **3 years** [S10] | **not offered** [S13] | not published |
| 払済保険 | not in the retrieved 約款 | after 2 years (養老) [S2] | not in the base 約款 [S6] | yes → becomes a 養老保険 [S10] | **not offered** [S13] | not published |
| Riders | 育英年金特約, 傷害特約Ｄ, こども新総合医療特約Ｄ [S1] | up to 3 of 4 [S3] [S5] | こども総合医療保険 as a separate contract [S6] | packaged child medical, with exceptions [S12] | **none** [S13] [S14] | not published |
| Dividends | ５年ごと配当 [S1] | annual + long-duration [S2] | 有配当 (社員配当) [S6] [S8] | ５年ごと配当 [S10] | **none** [S13] | 無配当 [S16] |
| Staged-benefit tax | not published | not published | 学資年金 雑所得, 祝金 一時所得 [S7] | not published | 教育資金 and 満期 both **雑所得** [S13] | not published |
| 返戻率 published | not published | premium tables only [S5] | 105.8% derived [S7] [S9] | 113.7–131.3% [S11] [S12] | up to 129.2% [S14] | 116.0–127.4% [S16] |
| Volume rate bands | not published | not published | 3 bands: ¥1,313 / ¥1,343 / ¥1,373 per ¥100,000 [S7] | not published | ¥30 per ¥100,000 above ¥700,000 [S13] | not published |

養老保険 specifically:

| Feature | かんぽ生命 [S2] [S4] | 日本生命 [S8] [S9] | 明治安田生命 [S15] |
|---|---|---|---|
| Term | 10–60 years, 1-year steps | example 30 → 60 | not published |
| Sum assured | ¥1,000,000–¥10,000,000 | example ¥5,000,000 | not published |
| Issue ages | not on the retrieved page | example 契約年齢 30 | 被保険者 6–75 |
| Death : maturity ratio | 1× / 2× / 5× / 10× menu | 1× | 1× |
| Juvenile graded death benefit | 50% under 3, 80% under 6, floored at 積立金 | none in the 約款 | not published |
| Accidental double indemnity | yes, after 1年6か月, 180-day rule | none in the 約款 | not published |
| Suicide exclusion | 3 years, pays 積立金 | 3 years, pays 責任準備金 | not published |
| Waiver of premium | in the main contract (insured's disability; policyholder's accidental death) | **rider only** (保険料払込免除特約) | not published |
| 予定利率 | not published | 0.60% → **1.00%** from 2025-01-02 | not published |

Most representative design for a reference implementation, on the evidence above: a
guaranteed-premium, single-life 養老保険 on a 30-year-old, 30-year term, level premiums payable
throughout, 死亡保険金 = 満期保険金 = ¥5,000,000, a three-year suicide exclusion, a monthly grace
running to the end of the following month, automatic premium loan against the surrender
value, reinstatement within three years, and a surrender value computed from elapsed months
— with a 学資保険 variant that replaces the single maturity benefit with a staged schedule (the
かんぽ 5/10/15/100 grid and the フコク 5/5/10/10/70/10 grid bracket the observed designs),
replaces the death benefit with a return of premiums, and adds the policyholder waiver as a
second decrement with a three-year suicide carve-out.

---

## Fetch failures and gaps

- **`https://www.jp-life.japanpost.jp/products/clause/pdf/yoro/201904/yr13.pdf` (S2) and
  `.../tumitategakushi_booklet.pdf` (S13)**: retrieved fine as bytes, but `pypdf` and
  poppler `pdftotext` both mis-decoded them. Poppler reported "Unknown character collection
  'Adobe-Japan1'"; `pypdf` produced a glyph-index mojibake. Both were re-extracted
  successfully with PyMuPDF, which ships the Adobe-Japan1 CMaps. No content was lost; noting
  it because the same failure will recur on most Japanese insurer PDFs.
- **`https://www.actuaries.jp/lib/standard-life-table/seimeihyo2018.pdf`**: returned the
  site's 404 page (rendered as a 3-page PDF). The working path is
  `https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf`, read off the
  index page, and that is what R1 cites.
- **`https://www.ja-kyosai.or.jp/okangae/person/pdf/202504_KOD25A.pdf`**: HTTP **404** with
  a browser User-Agent. JA共済's こども共済 (学資応援隊 / 祝金型) was therefore **not** retrieved. Its 養育年金
  rider — the cooperative-sector analogue of 育英年金 — is not cited anywhere above.
- **`https://www.meijiyasuda.co.jp/find2/light/list/tumitategakushi/contract/content/index.html`**
  and **`.../tumitategakushi_detail/`**: HTTP **404**. Meiji Yasuda's full ご契約のしおり・約款 sits
  behind the "MY Web約款" portal at `/norapl/my_web_yakkan/list02.aspx?product=43294`, which
  is session-gated and published only within stated service hours. **The つみたて学資 普通保険約款
  itself was not retrieved.** Everything attributed to [S13] and [S14] comes from the
  two-page brochure and the product page, so the article-level detail available for the
  other four carriers — grace period wording, lapse mechanics, contestability,
  surrender-value formula — is absent for 明治安田生命 and is shown as "not published" in the
  variation tables.
- **明治安田生命 養老保険 (S15)**: the product page gives only issue ages and the death = maturity
  statement. Terms, sums assured, dividend class and the 約款 were not retrieved; the MY Web約款
  entry is `/norapl/my_web_yakkan/list02.aspx?product=43001`, likewise session-gated.
- **日本生命 学資保険 別表2 (the child death-benefit schedule)**: the 給付約款 for 学資保険（有配当2013）was not in
  either retrieved Nissay file — S6 is the 契約基本約款 only, and S8 is the 一時払 booklet. The exact
  死亡保険金 formula at 日本生命 is therefore **[unverified]**; only the ¥400,000 worked example, the
  surrender-value cap and the 祝金 offset are sourced [S7].
- **育英年金特約 conditions**: the existence of 第一生命's ５年ごと配当付育英年金特約 [S1] and of 育英年金 inside
  日本生命's こども保険（有配当2012）[S6] is verified by cross-reference from the main 約款, but neither
  特約条項 was retrieved. The annuity amount, its term, whether it tapers, and whether it is
  payable in addition to the waiver are all **[unverified]**.
- **Current 標準利率 value**: R4 and R5 establish the instrument (平成8年大蔵省告示第48号), the reference
  rate (lower of the 3-year and 10-year average 10-year JGB yield) and the annual reset, but
  **no retrieved document gives the numeric 標準利率 in force at the access date**. The 0.5%
  deviation trigger, the rounding to multiples of 0.25% and the quarterly reset for 一時払
  contracts appear only in secondary commentary and in an unofficial mirror of the 告示 at
  `http://www.nn.em-net.ne.jp/~s-iwk/current/H08-048/index.html`, which failed with a
  self-signed-certificate error. Treat the numeric 標準利率 and the reset mechanics as
  **[unverified]**; the 予定利率 figures in §8 are carrier disclosures [S9] and are sourced.
- **e-Gov 法令検索 HTML**: `https://laws.e-gov.go.jp/law/408M50000040005` is JavaScript-rendered
  and returned only navigation chrome to WebFetch. The statute text in R3 came from the
  e-Gov law API (`/api/1/lawdata/408M50000040005`, 30.2 MB of XML), which is the same
  corpus.
- **金融庁 / 消費者庁 material on 学資保険 返戻率 disclosure**: searched for and **not found**. No FSA,
  消費者庁 or 国民生活センター publication specific to 学資保険 return-ratio disclosure was located. Any
  claim that such disclosure is regulated would be **[unverified]**; the 返戻率 figures in §9
  are carrier marketing disclosures.
- **Premium rate tables**: only 日本生命 publishes a rate — the three-band 保険料単価 [S7] and the
  worked premiums in the pricing release [S9]. かんぽ生命 [S4] [S5], フコク生命 [S11] and ソニー生命 [S16]
  publish single worked examples only. No carrier publishes a full rate basis, a 予定事業費率 or a
  surrender-value table, so any expense loading or surrender-value scale in the reference
  model must be constructed and marked [std].
- **Lapse experience**: R9 gives an all-product 個人保険 解約・失効率 of 5.6% for FY2024 with a
  five-year history, but **no lapse curve by duration** and nothing specific to 養老保険 or
  こども保険. A duration-varying lapse assumption for either cell will have to be [std].
- **JA共済 and other cooperatives, plus 住友生命, 太陽生命, 大同生命 and the corporate-market 「ハーフタックスプラン」
  form of 養老保険**: not fetched this session. The six-carrier set covers every 学資保険 payout
  shape (single 祝金, staged 祝金, five-instalment 学資年金, four-instalment 教育資金) and three 養老保険
  carriers with two full 約款, which was judged sufficient. Adding the corporate 養老保険 market
  would mainly add tax mechanics, not product mechanics.
- **明治安田生命 つみたて学資 II型 cancer-diagnosis waiver**: the brochure states it exists and that only
  I型 is currently sold [S13]. The definition of 悪性新生物 used (non-invasive tumours, carcinoma
  in situ and skin cancer excluded, malignant melanoma included) is sourced [S13], but the
  90-day rule's consequence — reclassification to I型 with a refund — is stated only in the
  brochure's footnote and no 約款 text was seen.
