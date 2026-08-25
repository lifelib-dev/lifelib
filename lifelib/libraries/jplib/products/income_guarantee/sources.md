# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/income-guarantee.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, which normally leaves gaps; this product has none, because every id the research
pass opened is cited by `product-spec.md` or `technical-notes.md` — S1–S17 and R1–R11 run
unbroken. Access date for all sources: 2026-08-20. No sources were newly added at drafting.
Cross-product [REG-R#] tags are listed in their own section at the end.

Company and branded product names appear in this file and in `_research/income-guarantee.md`
and nowhere else in the library. In `product-spec.md`, `technical-notes.md` and `model.md` a
carrier is its tag alone, so a reader can always resolve who said what — here — and never
has to.

---

## Primary product sources

Ten carriers — nine writing the product as a main contract, one as a rider [S13].
Seventeen documents: four are full 約款 (*yakkan*, policy conditions) or booklets containing
them [S1] [S3] [S14] [S15]; one is a 特約条項 (rider conditions) [S13]; three are pre-contract
disclosure documents (契約概要 / 注意喚起情報 / 重要事項説明書) [S2] [S4] [S5]; and nine are consumer or
specification pages [S6]–[S12] [S16] [S17], of which three publish a numeric 一括受取 (lump-sum
commutation) illustration and one publishes a monthly premium grid. [S13] publishes the
**commutation factor tables themselves**, and is the only document in the set that does.

(jplib-income_guarantee-s1)=

### S1 — SBI生命保険株式会社, 「収入保障保険 復活約款」 (policy conditions, 普通保険約款)

- Publisher: SBI生命保険株式会社
- Document: 収入保障保険 復活約款, 無配当収入保障保険, 2024年4月改訂版; the booklet carries the 収入保障保険普通保険約款 (Arts.
  1–43, 別表1–4) followed by the 特約条項 set; 118 pp., print code 募文M-2310-066-99 on the cover
- Doc type: 普通保険約款 (policy conditions)
- URL: https://www.sbilife.co.jp/products/yakkan_pdf/F12-syunyu.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.17 MB PDF downloaded, 118 pp., text extracted with
  `pypdf` and read article by article)
- The only complete 収入保障 普通保険約款 in the set whose text extracted cleanly, and the source of
  the composite's guarantee wording, annuity timetable, commutation, exclusion, waiver,
  grace, lapse and reinstatement mechanics. Also the only document offering a **逓増型**
  benefit and a **ステップ払込方式** premium pattern.

(jplib-income_guarantee-s2)=

### S2 — オリックス生命保険株式会社, 「商品概要のご説明 ―契約概要―」 (pre-contract product summary)

- Publisher: オリックス生命保険株式会社
- Document: 商品概要のご説明 ―契約概要―, 収入保障保険キープ・アップ, print code ORIX 2025-W-004, 3 pp.; formal
  product name 無配当無解約払戻金型収入保障保険（2025）
- Doc type: 契約概要 (pre-contract key-facts document)
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/keep-up-shohin.pdf
- Accessed: 2026-08-20. Retrieved: YES (3 pp. PDF downloaded, text extracted and read; two
  figure captions are CID-encoded and unreadable, the body text is clean)
- The clearest statement of the dominant chassis: no 解約払戻金, no 配当金, no 満期保険金, and **契約者貸付
  and 自動振替貸付 not offered at all**. Also carries the four-way rate-class grid with its BMI
  and blood-pressure thresholds.

(jplib-income_guarantee-s3)=

### S3 — オリックス生命保険株式会社, 「ご契約のしおり／約款」 (policy booklet and conditions)

- Publisher: オリックス生命保険株式会社
- Document: 2025年6月 ご契約のしおり 約款 for 無配当 無解約払戻金型収入保障保険（2025）, document code 305I16; 161 pp.
  (しおり, then 普通保険約款 Arts. 1–41, then 特約条項)
- Doc type: ご契約のしおり・約款
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/yakkan-keep-up-20250602.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.09 MB PDF downloaded, 161 pp., text extracted; the
  しおり's illustrated diagrams are CID-encoded, all 約款 article text is clean)
- The second full 約款, and the one that words the guarantee as an equality of periods rather
  than as an extension. The only contract in the set whose second-and-later instalments are
  payable **only while the recipient is alive**, with commutation to the 法定相続人 on the
  recipient's death.

(jplib-income_guarantee-s4)=

### S4 — オリックス生命保険株式会社, 「重要事項説明書（注意喚起情報）」 (pre-contract cautionary disclosure)

- Publisher: オリックス生命保険株式会社
- Document: 重要事項説明書（注意喚起情報）, 収入保障保険キープ・アップ, 4 pp.
- Doc type: 注意喚起情報
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/keep-up-juyou.pdf
- Accessed: 2026-08-20. Retrieved: YES (4 pp. PDF downloaded, text extracted and read)
- Carries the grace-period table for 月払 and for 年払・半年払 including the first-premium case, the
  contestability window, and the three-year suicide exclusion stated as an example.

(jplib-income_guarantee-s5)=

### S5 — FWD生命保険株式会社, 「重要事項説明書（契約概要・注意喚起情報）」 (pre-contract disclosure)

- Publisher: FWD生命保険株式会社
- Document: 重要事項説明書 2021年11月改訂 for 無解約返戻金型収入保障保険Ⅱ, 13 pp., しおり・約款検索コード 096-20211102
- Doc type: 重要事項説明書 (契約概要 + 注意喚起情報)
- URL: http://article.fwdlife.co.jp/yakkan/pdf/juusetsu/096/20211102_juusetsu_fwdshunyu.pdf
  (upgrades to `https://article.fwdlife.co.jp/...`)
- Accessed: 2026-08-20. Retrieved: YES (1.56 MB PDF downloaded, 13 pp., text extracted and
  read in full)
- The widest published 最低支払保証期間 menu found (2年/3年/5年/10年), five payout elections including
  すえ置 deferral, and a fully worked three-case benefit illustration in money — one of the two
  numeric anchors for the declining-total arithmetic.

(jplib-income_guarantee-s6)=

### S6 — チューリッヒ生命保険株式会社, 収入保障保険プラチナ 商品ページ (consumer page with a published rate card)

- Publisher: チューリッヒ生命保険株式会社
- Document: 商品ページ, figures stated as at 2025年12月2日現在
- Doc type: 商品ページ (consumer)
- URL: https://www.zurichlife.co.jp/product/category_shibou/disability
- Accessed: 2026-08-20. Retrieved: YES (228 KB of HTML fetched with a browser User-Agent,
  tag-stripped and read)
- The only source publishing a **premium grid** for this product — monthly rates by age and
  sex for two plan shapes — and the source of the anchor model cell's premium. Also the
  narrowest rate-class structure observed (two classes) and a fully numeric commutation
  illustration.

(jplib-income_guarantee-s7)=

### S7 — 第一ネオ生命保険株式会社, ネオdeしゅうほ 商品ページ (consumer page with an embedded FAQ)

- Publisher: 第一ネオ生命保険株式会社 (formerly ネオファースト生命保険); page dated 2026年4月時点
- Document: 商品ページ for 無解約返戻金型収入保障保険(2023)
- Doc type: 商品ページ (consumer)
- URL: https://neofirst.co.jp/product/syuho/
- Accessed: 2026-08-20. Retrieved: YES (113 KB of HTML fetched, tag-stripped and read)
- The five-way rate structure, the ¥50,000 floor on the residual 年金月額 after a partial
  commutation, and the one design in the set that makes 高度障害 cover **optional** and can
  switch the death cover itself off.

(jplib-income_guarantee-s8)=

### S8 — SOMPOひまわり生命保険株式会社, じぶんと家族のお守り「ご契約年齢、保険期間、保険金額」 (issue-envelope page)

- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/note/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- The widest published issue-age and expiry envelope, and the only **benefit cap expressed
  as a present value** found in the session — 年金現価保険金額3億円まで.

(jplib-income_guarantee-s9)=

### S9 — SOMPOひまわり生命保険株式会社, じぶんと家族のお守り「保障内容」 (cover page)

- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/content/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read; also fetched
  once through a summarising fetcher for cross-checking)
- Evidence that the guarantee menu can be **coupled to the premium-payment pattern**: a
  平準払込方式 election opens a five-year guarantee that is otherwise not on the menu.

(jplib-income_guarantee-s10)=

### S10 — SOMPOひまわり生命保険株式会社, じぶんと家族のお守り「お受取方法」 (payout-election page)

- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/plan_receive/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- One of the three published commutation illustrations, and the definition of 年金現価 as the
  contract value after deducting future interest.

(jplib-income_guarantee-s11)=

### S11 — SOMPOひまわり生命保険株式会社, じぶんと家族のお守り「オプション」 (rider menu page)

- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/option/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Rate class delivered as a **rider** (健康体料率特約) rather than as a rate-table election, and
  the 就労不能保障特約 whose guarantee period is defined to equal the main contract's.

(jplib-income_guarantee-s12)=

### S12 — フコクしんらい生命保険株式会社, 低解約返戻金型収入保障保険 商品ページ (consumer page)

- Publisher: フコクしんらい生命保険株式会社
- Document: 商品ページ for 守ってあげたいFS; rates and cover stated as at 2026年4月1日現在, print code
  募AQ0225138（26.03）
- Doc type: 商品ページ (consumer)
- URL: https://www.fukokushinrai.co.jp/consider/product/general/shuunyuuhoshou/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- The one **低解約返戻金型** design in the set — the only retrieved product with a surrender value
  at all, suppressed to 70% of the ordinary value for the whole term — plus a 満期給付金支払特則, the
  widest issue-age range observed, a published premium point, and the explicit warning that
  instalments may be withheld at source as 雑所得.

(jplib-income_guarantee-s13)=

### S13 — 住友生命保険相互会社, 「収入保障特約」 (rider conditions, 特約条項)

- Publisher: 住友生命保険相互会社
- Document: 収入保障特約, 23 pp., Arts. 1–33 plus 別表1「年金の現価相当額」 and 別表2「未払年金の現価」
- Doc type: 特約条項 (policy conditions, rider)
- URL: https://www.sumitomolife.co.jp/yakkan/pdf2/226.pdf
- Accessed: 2026-08-20. Retrieved: YES (664 KB PDF downloaded, 23 pp., text extracted and
  read including both appendix rate tables)
- **The only document in the set that publishes commutation factors.** Also the only
  rider-construction of the same economics, the only **annual** instalment frequency, and
  the only design expressing the guarantee as a floor on a shrinking payment period rather
  than as an extension past expiry.

(jplib-income_guarantee-s14)=

### S14 — はなさく生命保険株式会社, 「はなさく収入保障 ご契約のしおり・約款」 (policy booklet and conditions)

- Publisher: はなさく生命保険株式会社
- Document: ご契約のしおり・約款, 108 pp. (the file served at the `_new` path; page footers carry
  2025/10/14 and 2022/06/21 typesetting dates)
- Doc type: ご契約のしおり・約款
- URL: https://www.life8739.co.jp/pdf/shiori/shunyuhoshoushiori_new.pdf
- Accessed: 2026-08-20. Retrieved: YES (4.04 MB PDF downloaded, 108 pp., text extracted and
  read; the document uses full-width digits and a broken-line font, which extracts cleanly)
- Works the 契約年齢 definition as an example (35歳7カ月 → 契約年齢35歳), publishes the only
  **age-banded** preferred-risk thresholds observed, and supplies the three-case worked
  benefit illustration in payment counts that the composite's benefit arithmetic is checked
  against.

(jplib-income_guarantee-s15)=

### S15 — はなさく生命保険株式会社, 「かんたん告知 はなさく収入保障 ご契約のしおり・約款」 (policy booklet and conditions)

- Publisher: はなさく生命保険株式会社
- Document: ご契約のしおり・約款 for 引受緩和型収入保障保険（無解約払戻金型）, 88 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.life8739.co.jp/pdf/shiori/kanwashunyuhoshoushiori_new.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.85 MB PDF downloaded, 88 pp., text extracted and
  read)
- The **引受基準緩和型** (relaxed-underwriting) version, and the only graded-benefit design found:
  50% of the 年金月額 for death in the first policy year, in full for accident or a specified
  infectious disease. Its second worked example applies the 50% across all 411 remaining
  instalments, which is what pins the grading as a per-instalment reduction.

(jplib-income_guarantee-s16)=

### S16 — 三井住友海上あいおい生命保険株式会社, ＆LIFE 収入保障Wセレクト「オプション」 (option menu page)

- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: 商品ページ for 死亡・介護障害選択型収入保障保険（無解約返戻金型）無配当
- Doc type: 商品ページ (adviser/consumer)
- URL: https://www.msa-life.co.jp/lineup/syunyu/option.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read)
- The only source annotating each option by its **direction of premium effect** — 割引, 割増, or
  no change — which is a published qualitative measurement where no size is published.

(jplib-income_guarantee-s17)=

### S17 — 三井住友海上あいおい生命保険株式会社, ＆LIFE 収入保障Wセレクト「お受取例」 (payout illustration page)

- Publisher: 三井住友海上あいおい生命保険株式会社
- Doc type: 商品ページ (adviser/consumer)
- URL: https://www.msa-life.co.jp/lineup/syunyu/sample.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read)
- The third published commutation illustration, and the statement that the annuity is
  computed on the 基礎率 in force when the 年金基金 is set up — the closest any direct writer comes
  to disclosing a commutation basis.

---

## Regulatory and actuarial references

(jplib-income_guarantee-r1)=

### R1 — 公益社団法人 日本アクチュアリー会, 「標準生命表２０１８」 (mortality tables)

- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８, 5 pp.; four tables — 生保標準生命表２０１８（死亡保険用）男 and 女, 第三分野標準生命表２０１８ 男 and 女
  — each with 生存数・死亡数・死亡率・平均余命 by single year of age
- Doc type: mortality table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (236 KB PDF downloaded, 5 pp., text extracted; every
  row parses as text)
- Cited for the individual 死亡保険用 qx values the documents quote: male 0.00068 at 30, 0.00653
  at 60, 0.01015 at 65, 0.05006 at 80; female 0.00363 at 60. Terminal ages 109 (male) and
  113 (female).

(jplib-income_guarantee-r2)=

### R2 — 公益社団法人 日本アクチュアリー会, 「標準生命表２０１８の作成概要」 (technical note)

- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料①–⑤)
- Doc type: technical note on table construction
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (293 KB PDF downloaded, 6 pp., text extracted and
  read) - The margins that make this a **valuation** table: improvement applied forward at
  2.5% p.a. for five years then 1.0% for three, a 数学的危険論 adjustment sized to about a 2.28%
  (2σ) exceedance probability and capped at 130% of the unadjusted rate, Greville smoothing
  and Gompertz–Makeham extrapolation joined at age 84. Two statements bear directly on this
  product: the table is built on a **保険年齢方式** basis, and the 死亡保険用 rate **includes 高度障害**.

(jplib-income_guarantee-r3)=

### R3 — 公益社団法人 日本アクチュアリー会, 「標準生命表2018」 publication page

- Publisher: 公益社団法人 日本アクチュアリー会
- Doc type: publication/announcement page
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- The statutory chain: the IAJ as 指定法人 under 保険業法第122条の2第1項, commissioned under
  第122条の2第2項第3号 to construct the tables, the 2018 revision submitted 2017-05-11 and applying
  from April 2018.

(jplib-income_guarantee-r4)=

### R4 — 国税庁, タックスアンサー No.1620「相続等により取得した年金受給権に係る年金の課税」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax authority guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1620.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read)
- The income-tax half of the two-layer treatment of an income-form death benefit: each
  instalment splits into a 非課税部分 and a 課税部分, the first year wholly exempt and the taxable
  share rising **in steps (階段状)**, keyed to the 相続税評価割合. Basis 所得税法第35条, 所得税法施行令第185条・第186条.

(jplib-income_guarantee-r5)=

### R5 — 国税庁, タックスアンサー No.4123「相続税等の課税対象になる年金受給権」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax authority guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4123.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read)
- The inheritance-tax half: the annuity **right** is the taxable object at death, valued
  under 相続税法第24条 or 第25条.

(jplib-income_guarantee-r6)=

### R6 — e-Gov 法令検索, 相続税法 第24条（定期金に関する権利の評価）

- Publisher: デジタル庁 e-Gov 法令検索 — 相続税法, law id 325AC0000000073
- Doc type: statute
- URL (human): https://laws.e-gov.go.jp/law/325AC0000000073 — URL (machine, used):
  https://elaws.e-gov.go.jp/api/1/lawdata/325AC0000000073
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (894 KB XML, HTTP 200; Art. 24
  extracted and read verbatim. The human-facing page is a JavaScript shell and yields
  nothing to plain fetchers.)
- For a 有期定期金 whose 給付事由 has occurred, the value is the **greatest** of the surrender value
  payable on the spot, the lump sum available in lieu of the annuity, and the average annual
  amount over the remaining period times the 複利年金現価率 at the contract's 予定利率. On a 無解約返戻金型
  design the first limb is zero, so the commutation amount drives the tax value.

(jplib-income_guarantee-r7)=

### R7 — 国税庁, タックスアンサー No.1140「生命保険料控除」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax authority guidance), stated as 令和7年4月1日現在法令等
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read in full)
- The post-2012 (新契約) three-basket schedule — full premium to ¥20,000, then ½ + ¥10,000 to
  ¥40,000, then ¼ + ¥20,000 to ¥80,000, then a flat ¥40,000 — with the three baskets capped
  together at **¥120,000**. Basis 所法76・120, 所令262, 平成29年国税庁告示10号.

(jplib-income_guarantee-r8)=

### R8 — e-Gov 法令検索, 保険業法施行規則 第68条・第69条

- Publisher: デジタル庁 e-Gov 法令検索 — 保険業法施行規則, 平成8年2月29日大蔵省令第5号, law id 408M50000040005
- Doc type: ministerial ordinance
- URL (machine, used): https://elaws.e-gov.go.jp/api/1/lawdata/408M50000040005
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (30.2 MB XML, HTTP 200; Arts. 65–71
  extracted, captions confirmed as 第68条（標準責任準備金の対象契約）and 第69条（生命保険会社の責任準備金）)
- Cited for the four exclusions from 標準責任準備金 treatment — none of which catches a
  conventional guaranteed 収入保障 contract — and for the 保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金
  taxonomy.

(jplib-income_guarantee-r9)=

### R9 — 金融庁, 「保険会社向けの総合的な監督指針」 II-2 財務の健全性

- Publisher: 金融庁
- Doc type: 監督指針 (supervisory guideline)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read)
- II-2-1-2 requires 標準責任準備金 for in-scope first- and third-sector contracts; II-2-1-3-1 names
  the discount rate as the **標準利率**, defined as 責任準備金告示に規定する予定利率. The guideline states no
  numeric 標準利率.

(jplib-income_guarantee-r10)=

### R10 — 金融庁, 標準責任準備金制度にかかる告示の一部改正 — パブリックコメントの結果等

- Publisher: 金融庁
- Doc type: パブリックコメント結果公表ページ
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/20210630.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through a summarising fetcher and read; the
  新旧対照表 attachments 別紙2 and 別紙3 were **not** fetched, which is why no numeric 標準利率 is
  asserted anywhere in this product's documents)
- Identifies the operative instruments as **平成8年大蔵省告示第48号**, issued under 保険業法第116条第2項, and
  平成13年金融庁告示第24号, with the 2021 amendments applying from 令和3年10月1日 and 令和4年4月1日.

(jplib-income_guarantee-r11)=

### R11 — 公益財団法人 生命保険文化センター, 「2024（令和6）年度 生命保険に関する全国実態調査＜速報版＞」

- Publisher: 公益財団法人 生命保険文化センター, 2024年11月
- Document: 全国実態調査 速報版, 200 pp.
- Doc type: household survey (speed-report edition)
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.74 MB PDF downloaded, 200 pp., text extracted;
  searched for 収入保障 with **no hits** — the survey does not break the product out)
- Market context only: 世帯加入率 89.2% 全生保 / 79.9% 民保; 世帯普通死亡保険金額 ¥19,360,000, down from
  ¥20,270,000; 世帯主の普通死亡保険金額 ¥12,580,000, down from ¥13,860,000. The falling household sum
  assured is the demand-side backdrop for a product sold as a declining income.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose own
R1–R47 numbering is distinct from this file's and is likewise frozen. Within that page plain
[R#] refers to its own entries, so the two schemes must never be read across. Entries cited
by the income guarantee documents, all accessed 2026-08-20:

- **REG-R1** — 保険業法 第3条: the 第一分野 / 第三分野 licence split, which is what makes this a death
  product and its disability and care 特則 third-sector business. retrieved: yes.
- **REG-R2** — 保険業法 第4条: the 算出方法書 holding 予定利率, 予定死亡率 and 予定事業費率 is not public — the reason
  every pricing and commutation-basis parameter here is **[std]**. retrieved: yes.
- **REG-R4** — 保険業法 第116条: the delegation the 標準責任準備金 chain hangs on. retrieved: yes.
- **REG-R6** — 保険業法 第121条: the 意見書, and behind it the 1号収支分析. retrieved: yes.
- **REG-R7** — 施行規則 第68条: which contracts are standard-reserve contracts. retrieved: yes.
- **REG-R8** — 施行規則 第69条: the four-way reserve taxonomy. retrieved: yes.
- **REG-R10** — 告示第48号: 平準純保険料式, table vintages, the 標準利率 reset machinery. retrieved: yes,
  but from an unofficial consolidated mirror — see the entry.
- **REG-R11** — 告示48号改正 (2017): 標準生命表2018 applies from 2018-04-01, and the 年金開始後用 table
  stays on the 2007 vintage. retrieved: yes.
- **REG-R14** — 監督指針（本編）: 契約締結前交付書面 contents, and the treatment of 低解約返戻金型 and 自動振替貸付.
  retrieved: yes.
- **REG-R15** — ESR の概要: commencement 2026-03-31, the 100% trigger, 現在推計+MOCE, 99.5%.
  retrieved: yes.
- **REG-R17** — ソルベンシー・マージン比率: the old 200% threshold. retrieved: **no** — the 告示 was not
  located; the entry rests on [REG-R14] and [REG-R15].
- **REG-R18** — 標準生命表2018 PDF: the freely readable valuation table, verified spot rates and
  terminal ages. retrieved: yes.
- **REG-R20** — 作成概要: the 2σ margin, the improvement allowance, the 保険年齢 basis, and the fact
  that the 死亡保険用 table **includes** 高度障害 in its death rate. retrieved: yes.
- **REG-R21** — IAJ 索引と利用規約: redistribution is restricted, so the library ships a **[std]**
  table citing the IAJ entries rather than a copy. retrieved: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析, at least ten future years, by segment. retrieved:
  yes.
- **REG-R31** — 生命保険の動向 2025年版: the in-force and new-business mix, and the 5.6% industry
  解約・失効率 that any **[std]** lapse assumption must be reconciled to. retrieved: yes.
- **REG-R32** — 全国実態調査 2024年度 workbooks: household penetration and premium bands, which the
  model points sit inside. retrieved: yes.
- **REG-R34** — 保険法 第51条: the statutory suicide exclusion has **no** time limit, so the
  three-year 免責期間 is contractual and a per-carrier fact. retrieved: yes.
- **REG-R35** — 保険法 第55条: the five-year contestability ceiling and one-month discovery clock
  bounding the carriers' two-year windows. retrieved: yes.
- **REG-R36** — 保険業法 第309条: the eight-day dispatch-rule クーリング・オフ, scoped out here.
  retrieved: yes.
- **REG-R39** — 金融サービス提供法 第4条: the 説明義務 that covers a 低解約返戻金型 suppression period — the
  variant design at [S12]. retrieved: yes.
- **REG-R40** — 生命保険契約者保護機構: 90% of the 責任準備金 on insurer failure. retrieved: yes (Q1 page;
  the 高予定利率契約 page was not opened).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation setting that rate. retrieved: yes.
- **REG-R42** — 介護保険法 第7条: 要介護状態 and the 40–64 特定疾病 split, behind the care-income 特則 sold on
  this chassis. retrieved: yes.
- **REG-R43** — 所得税法 第76条: three baskets of ¥40,000 capped at ¥120,000. retrieved: yes.
- **REG-R44** — 相続税法 第12条: ¥5,000,000 × the number of statutory heirs. retrieved: yes.
- **REG-R45** — タックスアンサー No.4114: the administration's mechanics for that exemption.
  retrieved: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan. retrieved: yes.

---

## Provenance note

Extraction details — which fact came from which document, the per-carrier variation table,
and the register of fetch failures and [unverified] claims (four CID-broken PDFs whose
carriers are therefore represented only by their product pages, the unpublished commutation
discount basis at every direct writer, the unpublished 予定利率, the numeric 標準利率, the
財務省令複利年金現価率, and the product's share of Japanese new business) — live in
`_research/income-guarantee.md`, the citation ground truth for the S# and R# numbering used
here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
