# Income Guarantee (収入保障保険, survivor income term) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese 収入保障保険 (*shūnyū hoshō hoken*, survivor income term) liability
cash flow reference model — a **death** benefit paid as a monthly annuity-certain running to
the end of the policy term, with a minimum payment guarantee period (最低支払保証期間 / 支払保証期間) that
floors the tail.

This product is **not** income protection in the disability sense. The insured event is
death or the contractual 高度障害状態 (*kōdo shōgai jōtai*, severe-disability state, which every
retrieved contract treats as an accelerated equivalent of death). Disability and
long-term-care income are sold on this chassis only as riders/特則, and those are noted here
as variants.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually retrieved and read during
this session, or is tagged [unverified] where it is general knowledge or a computed
inference not confirmed against a retrieved document. Every arithmetic result I derived
myself (implied discount rates) is labelled **derived** and is not a published figure.
Access date for all fetched sources: 2026-08-20.

Company and product brand names appear in this file and in `sources.md` only; the product
documents cite these sources by tag alone.

---

## Primary sources

### S1 — SBI生命保険, 「収入保障保険 復活約款」 (policy conditions, 普通保険約款)
- Publisher: SBI生命保険株式会社 (SBI Life Insurance)
- Document: 収入保障保険 復活約款, 無配当 収入保障保険, 2024年4月改訂版; booklet contains the 収入保障保険普通保険約款 (Arts.
  1–43, 別表1–4) followed by the 特約条項 set; 118 pp. Print code 募文M-2310-066-99 on the cover
- Doc type: policy conditions (約款) — the only full 収入保障普通保険約款 retrieved this session whose
  text extracted cleanly
- URL: https://www.sbilife.co.jp/products/yakkan_pdf/F12-syunyu.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 2.17 MB, 118 pp., text
  extracted with pypdf and read article by article)
- Key content: 保険契約の型 (定額型/逓増型) and the 3%-per-elapsed-year increasing formula; 最低支払保証期間 as
  a policy-owner election; the annuity payment timetable and the term-extension mechanic
  that implements the guarantee; commutation (年金の一時支払) of the 未支払分の現価; suicide and other
  免責事由 with the 責任準備金 fallback; 保険料払込免除 on accidental 身体障害; grace, lapse, reinstatement; 減額;
  契約年齢 definition; no policyholder dividend; 別表3 高度障害状態 and 別表4 身体障害の状態; ステップ払込方式.

### S2 — オリックス生命保険, 「商品概要のご説明 ―契約概要―」収入保障保険キープ・アップ
- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance)
- Document: 商品概要のご説明 ―契約概要―, print code ORIX 2025-W-004, 3 pp.
- Doc type: 契約概要 (pre-contract product summary, the Japanese key-facts document)
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/keep-up-shohin.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 3 pp., text extracted and read;
  two small figure captions are CID-encoded and unreadable, the body text is clean)
- Key content: formal product name 無配当無解約払戻金型収入保障保険（2025）; 支払保証期間 1年/5年 menu; the contract
  example (30歳, 65歳満了, 年金月額15万円, 支払保証期間5年); the four-way rate-class grid with its BMI and
  blood-pressure thresholds; 全部一括受取 / 一部一括受取 / 残額一括受取; 特定三疾病保険料払込免除特則（2025） triggers;
  explicit statements that there is no 解約払戻金, no 配当金, no 満期保険金, and that **契約者貸付 and 自動振替貸付
  are not offered**.

### S3 — オリックス生命保険, 「ご契約のしおり／約款」 無配当 無解約払戻金型収入保障保険（2025）
- Publisher: オリックス生命保険株式会社
- Document: 2025年6月 ご契約のしおり 約款, 無配当 無解約払戻金型収入保障保険（2025）, document code 305I16; 161 pp. (しおり
  section then 普通保険約款 Arts. 1–41 then 特約条項)
- Doc type: policy booklet (ご契約のしおり) + policy conditions (約款)
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/yakkan-keep-up-20250602.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 3.09 MB, 161 pp., text
  extracted; the しおり's illustrated diagrams are CID-encoded, all 約款 article text is clean)
- Key content: 第1条 rate classes fixed for the whole term; 第2条支払保証期間 elected at issue and
  **not changeable**; 第3条 the two annuities, their 免責事由, the second-and-later payment rule
  (payable on the monthly anniversary of the 年金支払基準日 **while the recipient is alive**) and
  the guarantee override; 第5条 the recipient succeeds to all rights and no further premium is
  payable; 第6条一括支払; 第7条 recipient's death → 年金現価相当額 to the 法定相続人; 第8条保険料払込免除; grace,
  lapse, 3-year reinstatement window.

### S4 — オリックス生命保険, 「重要事項説明書（注意喚起情報）」収入保障保険キープ・アップ
- Publisher: オリックス生命保険株式会社
- Document: 重要事項説明書（注意喚起情報）, 4 pp.
- Doc type: 注意喚起情報 (pre-contract cautionary disclosure)
- URL: https://www.orixlife.co.jp/life/keep-up/pdf/keep-up-juyou.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 4 pp., text extracted and read)
- Key content: cooling-off; 告知義務違反 contestability from the 責任開始日 (復活日 included); the 3-year
  suicide exclusion stated as an example; the grace-period table for 月払 and for 年払/半年払
  including the first-premium case; reinstatement window.

### S5 — FWD生命保険, 「FWD収入保障 重要事項説明書（契約概要・注意喚起情報）」
- Publisher: FWD生命保険株式会社 (FWD Life Insurance)
- Document: 重要事項説明書 2021年11月改訂, product 無解約返戻金型収入保障保険Ⅱ (pet name FWD収入保障), 13 pp., しおり・約款
  検索コード 096-20211102
- Doc type: 重要事項説明書 (契約概要 + 注意喚起情報)
- URL: http://article.fwdlife.co.jp/yakkan/pdf/juusetsu/096/20211102_juusetsu_fwdshunyu.pdf
  (upgrades to https://article.fwdlife.co.jp/...)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 1.56 MB, 13 pp., text extracted
  and read in full)
- Key content: the widest published 最低支払保証期間 menu found (2年/3年/5年/10年); the annuity
  timetable (first payment on the day before the first monthly policy anniversary after the
  event, then monthly on the day before each anniversary); five payout elections including
  すえ置 (deferral); a fully worked three-case benefit illustration with money amounts; the
  four-way rate-class grid; 配偶者同時災害死亡時割増特則; 生活支援特則 (障害年金/介護年金); 3大疾病保険料払込免除特約Ⅱ with its
  90-day cancer waiting period; リビング・ニーズ特約 with a ¥30,000,000 cap and the six-month
  interest-and-premium deduction; no 解約返戻金, no policyholder dividend, no renewal.

### S6 — チューリッヒ生命, 「収入保障保険プラチナ」 product page
- Publisher: チューリッヒ生命保険株式会社 (Zurich Life Insurance Company Japan)
- Doc type: product page (consumer), figures stated as at 2025年12月2日現在
- URL: https://www.zurichlife.co.jp/product/category_shibou/disability
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched with a browser User-Agent, 228 KB,
  tag-stripped and read)
- Key content: 契約年齢 20～70歳; 年金月額 5万円～ in ¥10,000 steps; maximum 90歳満了 (75歳満了 when the
  収入サポート特約 is attached); a **two**-class rate structure (非喫煙優良体型 / 標準体型) — the narrowest
  observed; published monthly premium rate points by age and sex for two plan shapes; a
  fully numeric commutation illustration (毎月受取 vs 一時金 vs two partial shapes) with the
  wording that the lump sum is 年金月額 times a 所定の係数; 収入サポート特約 (Z02) benefit design and its
  income-based benefit ceilings; conversion (保険契約の変換) without underwriting; 高額割引制度; no
  解約払戻金.

### S7 — 第一ネオ生命保険, 「ネオdeしゅうほ＜無解約返戻金型収入保障保険(2023)＞」 product page
- Publisher: 第一ネオ生命保険株式会社 (formerly ネオファースト生命保険), page dated 2026年4月時点
- Doc type: product page (consumer) with an embedded FAQ
- URL: https://neofirst.co.jp/product/syuho/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, 113 KB, tag-stripped and read)
- Key content: 契約年齢 20歳～70歳; 年金支払保証期間 2年 or 5年; a **five**-way rate structure — the four
  smoker/health cells plus a 保険料率区分なし cell used when the contract is written as 障害介護収入保障年金
  only (死亡収入保障年金不担保特則 + 障害介護収入保障特則); 高度障害 cover supplied by an optional 高度障害収入保障特則 rather
  than by the main contract; 障害介護収入保障特則 triggers (身体障害者手帳1～4級, 障害等級1～2級 excluding mental at
  2級, 要介護1～5); the ¥50,000 floor on the residual 年金月額 after a partial commutation;
  リビング・ニーズ特約（2018） attached free; no relaxed-underwriting version offered; premium
  collection dates.

### S8 — SOMPOひまわり生命保険, 「じぶんと家族のお守り — ご契約年齢、保険期間、保険金額」
- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: product page (consumer), the issue-envelope page
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/note/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Key content: 契約可能年齢 20～80歳; 保険期間 45～90歳; 保険料払込期間 equal to 保険期間 with no further premium
  after an annuity event; 基準年金月額 from ¥50,000 in ¥10,000 steps; and the only published
  **benefit cap expressed as a present value** found this session — 年金現価保険金額3億円まで.

### S9 — SOMPOひまわり生命保険, 「じぶんと家族のお守り — 保障内容」
- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/content/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read; also fetched
  once through WebFetch for cross-checking)
- Key content: contract example 35歳男性 / 基準年金月額20万円 / 60歳まで / 最低保証期間2年; 遺族年金 and 高度障害年金 are
  mutually exclusive; no 解約返戻金 through the whole term; and the note that a **平準払込方式**
  election also opens a 5-year guarantee pattern — evidence that the guarantee menu is
  coupled to the premium-payment pattern at this carrier.

### S10 — SOMPOひまわり生命保険, 「じぶんと家族のお守り — お受取方法」
- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/plan_receive/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Key content: a numeric commutation illustration — 35歳男性, 基準年金月額20万円, 60歳まで, death within
  one month of issue: 毎月受取 total ¥60,000,000 against a 一括受取額 of **約5,531万円**; 一部一括受取 limited
  to once during the term; the definition of 年金現価 as the contract value after deducting
  future interest.

### S11 — SOMPOひまわり生命保険, 「じぶんと家族のお守り — オプション」
- Publisher: SOMPOひまわり生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.himawari-life.co.jp/product/omamori_family_m/option/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Key content: 健康体料率特約 — rate class delivered as a **rider** rather than as a rate table
  election; 七大疾病・就労不能保険料免除特約; 無解約返戻金型就労不能保障特約 whose guarantee period is **the same as the
  main contract's 最低保証期間** and which is extinguished by a death or 高度障害 claim;
  無解約返戻金型メンタル疾患保障付七大疾病保障特約 with a fixed 特約年金支払期間 of 2年 or 5年 and commutation on the
  recipient's death.

### S12 — フコクしんらい生命保険, 「低解約返戻金型収入保障保険（守ってあげたいFS）」 product page
- Publisher: フコクしんらい生命保険株式会社 (Fukokushinrai Life Insurance)
- Doc type: product page (consumer), rates and cover stated as at 2026年4月1日現在, print code
  募AQ0225138（26.03）
- URL: https://www.fukokushinrai.co.jp/consider/product/general/shuunyuuhoshou/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Key content: the **低解約返戻金型** variant — the one retrieved product in this set that has a
  surrender value at all, suppressed to a 低解約返戻金割合 of **70%** of the ordinary value
  throughout the premium-paying period; 契約年齢範囲 15～75歳 (the widest observed); 年金月額 from
  ¥50,000 in ¥10,000 steps; 最低支払保証期間 1年/2年/5年; a 満期給付金支払特則 that adds a survival maturity
  benefit **not** subject to the 70% factor; four payout elections with 一部一括受取 limited to
  once; a published premium point (30歳男性, 60歳満了, 最低支払保証期間1年, 年金月額20万円 → 口座振替月払保険料 ¥5,780);
  the explicit statement that the monthly instalments may be subject to withholding as 雑所得;
  and the rider menu.

### S13 — 住友生命保険, 「収入保障特約」 約款
- Publisher: 住友生命保険相互会社 (Sumitomo Life Insurance)
- Document: 収入保障特約 (rider conditions), 23 pp., Arts. 1–33 plus 別表1「年金の現価相当額」 and
  別表2「未払年金の現価」
- Doc type: policy conditions (特約条項)
- URL: https://www.sumitomolife.co.jp/yakkan/pdf2/226.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 664 KB, 23 pp., text extracted
  and read including both appendix rate tables)
- Key content: the **rider** construction of the same economics, and the only source found
  this session that **publishes the commutation factors themselves**. Two 特約の型: 逓減型, whose
  年金支払期間 shortens by one year on each policy anniversary subject to a **5-year floor**, and
  固定型 with a fixed period. Instalments are **annual**, not monthly. 別表1 gives 年金の現価相当額 as
  基本年金額 × a published rate, tabulated by 年金支払期間 and by the type of main contract, with the
  note that there is no dependence on the annuitant's age or sex. 別表2 gives 未払年金の現価 by
  残存年金支払回数 and says the tabulated factor is then further discounted from the request date to
  the day before the next annuity payment date by a method the company determines. Also:
  年金の分割支払い (splitting one year's annuity into instalments with interest at a company rate),
  and commutation both before the first annuity and during the payment period.

### S14 — はなさく生命保険, 「はなさく収入保障 ご契約のしおり・約款」
- Publisher: はなさく生命保険株式会社 (Hanasaku Life Insurance, a 日本生命 subsidiary)
- Document: ご契約のしおり・約款, 108 pp. (the file served at the `_new` path; page footers carry
  2025/10/14 and 2022/06/21 typesetting dates)
- Doc type: policy booklet + policy conditions
- URL: https://www.life8739.co.jp/pdf/shiori/shunyuhoshoushiori_new.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 4.04 MB, 108 pp., text
  extracted and read; the document uses full-width digits and a broken-line font, which
  extracts cleanly)
- Key content: 契約年齢 20歳～70歳 with the age definition worked as an example (35歳7カ月 → 契約年齢35歳,
  i.e. **満年齢, fraction truncated**, not 保険年齢); the four-way rate grid with **age-banded**
  BMI and blood-pressure thresholds — the only carrier observed to band them; a three-case
  worked benefit illustration in payment counts; commutation of the 年金の現価相当額 in whole or
  part with a floor on the residual 年金月額, and the statement that the lump sum is less than
  the sum of the monthly instalments.

### S15 — はなさく生命保険, 「かんたん告知 はなさく収入保障 ご契約のしおり・約款」
- Publisher: はなさく生命保険株式会社
- Document: ご契約のしおり・約款 for 引受緩和型収入保障保険（無解約払戻金型）, 88 pp.
- Doc type: policy booklet + policy conditions
- URL: https://www.life8739.co.jp/pdf/shiori/kanwashunyuhoshoushiori_new.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 3.85 MB, 88 pp., text extracted
  and read)
- Key content: the **relaxed-underwriting (引受基準緩和型)** version of the same product, and the
  only graded-benefit design found: death from the 責任開始日 to the day before the first policy
  anniversary pays **50% of the 年金月額**, with death by 不慮の事故 or a specified 感染症 paying in
  full. Premiums are explicitly loaded relative to the carrier's fully underwritten 収入保障保険;
  no policyholder dividend; the second-and-later payment dates run off the monthly policy
  anniversary following the first payment date; two worked examples including one that shows
  the 50% reduction applied across all 411 remaining instalments.

### S16 — 三井住友海上あいおい生命保険, 「＆LIFE 収入保障Wセレクト — オプション」
- Publisher: 三井住友海上あいおい生命保険株式会社 (Mitsui Sumitomo Aioi Life Insurance)
- Doc type: product page (adviser/consumer)
- URL: https://www.msa-life.co.jp/lineup/syunyu/option.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read)
- Key content: formal product name 死亡・介護障害選択型収入保障保険（無解約返戻金型）無配当; an option menu annotated by
  **direction of premium effect** — 割引 for サポート給付金三大疾病のみ保障特則, サポート給付金女性疾病のみ保障特則,
  サポート給付金不担保特則, 健康診断料率適用特約 and 健康優良割引（区分料率適用特約）; 割増 for ストレス・メンタル疾病サポート特則 and 保険料払込免除特約（22）;
  no change for リビング・ニーズ特約. Rate classes are named as e.g. SD非喫煙者優良体保険料率.

### S17 — 三井住友海上あいおい生命保険, 「＆LIFE 収入保障Wセレクト — お受取例」
- Publisher: 三井住友海上あいおい生命保険株式会社
- Doc type: product page (adviser/consumer)
- URL: https://www.msa-life.co.jp/lineup/syunyu/sample.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read)
- Key content: a numeric commutation illustration — 契約年齢30歳, 基本年金月額10万円, 65歳満了, 最低支払保証期間5年,
  event at 40歳 (契約から10年1か月目): 一括受取 = 年金の現価相当額 **約2,764万円**; the note that the annuity amount
  is computed on the 基礎率 in force when the 年金基金 is set up. The discount rate itself is not
  published.

---

## Regulatory and actuarial references

### R1 — 日本アクチュアリー会, 「標準生命表２０１８」 (mortality tables)
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — four tables: 生保標準生命表２０１８（死亡保険用）男 / 女, and 第三分野標準生命表２０１８男 /
  女, each with 生存数・死亡数・死亡率・平均余命 by single year of age
- Doc type: standard mortality table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 236 KB, 5 pp., text extracted;
  every row parses as text, so the table is machine-readable — but it is **not
  redistributable**)
- (Text correction, 2026-08-20: the retrieval line read "machine-readable and
  redistributable". The two do not follow from one another and the second is wrong. The
  日本アクチュアリー会 site 利用規約 reserves copyright in the published material and prohibits
  reproduction, alteration and transmission to third parties without written consent, so
  the table may be read and cited by anyone but may not be shipped. That prohibition is
  precisely why this library cites the table by URL, quotes only the individual rates a
  worked example needs, and ships `mort_table.csv` as a **[std]** construction whose
  `provenance` column points back at these entries rather than as a copy of the file. Ids
  and numbering unchanged.)
- Content: the full 死亡保険用 table for both sexes. Spot values read directly: male qx = 0.00068
  at 30, 0.00653 at 60, 0.01015 at 65, 0.05006 at 80; female qx = 0.00363 at 60. Male ℓ0 =
  100,000 with 平均余命 80.77 at age 0; female 平均余命 86.56 at age 0. Terminal ages 109 (male) and
  113 (female).

### R2 — 日本アクチュアリー会, 「標準生命表２０１８の作成概要」
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料①–⑤)
- Doc type: technical note on table construction
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 293 KB, 6 pp., text extracted
  and read)
- Content: the margins that make this a **valuation** table rather than a best-estimate
  table. Observation years 2008, 2009, 2011 (2010 excluded for the Tōhoku earthquake), with
  2005–2009 and 2011 for the young and old age bands; select-period truncation capped at 10
  years; mortality improvement applied forward at **2.5% p.a. for five years then 1.0% p.a.
  for three years**; a 数学的危険論 adjustment sized so the probability that experience exceeds
  the variation forecast is about **2.28% (2σ)**, capped at **130%** of the pre-adjustment
  rate, on an assumed portfolio of 1,000,000 policies per sex; Greville 3rd-order 13-term
  smoothing; Gompertz–Makeham extrapolation joined at age 84. Two statements matter directly
  for this product: the table is built **on a 保険年齢方式 (insurance-age) basis**, and the 死亡保険用
  table is **a mortality rate that includes 高度障害** — so a model that treats the 高度障害年金 as a
  second decrement on top of this table double-counts.

### R3 — 日本アクチュアリー会, 「標準生命表2018」 publication page
- Publisher: 公益社団法人 日本アクチュアリー会
- Doc type: publication/announcement page
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read)
- Content: the statutory chain — the IAJ is the 指定法人 under 保険業法第122条の2第1項 and is
  commissioned by the FSA under 第122条の2第2項第3号 to construct the standard tables; the revision
  was published for comment on 2017-03-31, resolved by the board on 2017-05-10, submitted to
  the FSA Commissioner on 2017-05-11, and **applies from April 2018** following the FSA's
  amendment of its 告示. Confirms the table set consists of 標準生命表2018 and 標準生命表2007 (plus
  生保標準生命表1996 in the Excel bundle).

### R4 — 国税庁, タックスアンサー No.1620 (相続等により取得した年金受給権に係る年金の課税)
- Publisher: 国税庁 (National Tax Agency)
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1620.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read)
- Content: the income-tax half of the two-layer treatment of an income-form death benefit.
  Where the annuity right was acquired by 相続・遺贈・贈与 and the recipient is not the premium
  payer, each instalment is split into a 非課税部分 and a 課税部分: the first year of payment is
  wholly exempt and the taxable share then rises **in steps (階段状)** year by year, with the
  schedule keyed to the 相続税評価割合 (illustrated: 相続税評価割合 over 50% and up to 55% → 課税割合 45%).
  Basis: 所得税法第35条, 所得税法施行令第185条・第186条. Public survivor pensions (国民年金・厚生年金) are separately
  exempt.

### R5 — 国税庁, タックスアンサー No.4123 「相続税等の課税対象になる年金受給権」
- Publisher: 国税庁
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4123.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read)
- Content: the inheritance-tax half — the annuity **right** is the taxable object at death
  and is valued under 相続税法第24条 or 第25条, "解約返戻金相当額などにより評価".

### R6 — e-Gov法令検索, 相続税法 第24条（定期金に関する権利の評価）
- Publisher: デジタル庁 e-Gov法令検索 (law 325AC0000000073, 相続税法)
- Doc type: statute
- URL: https://laws.e-gov.go.jp/law/325AC0000000073
  (machine-readable full text obtained from https://elaws.e-gov.go.jp/api/1/lawdata/325AC0000000073)
- Accessed: 2026-08-20. Retrieved: YES (the HTML page is a JS shell and yields nothing, but
  the e-Gov API returned the complete 894 KB XML with HTTP 200; Art. 24 extracted and read
  verbatim)
- Content: for a 定期金給付契約 whose 給付事由 has already occurred, a **有期定期金** (the shape this
  product pays) is valued at the **greatest** of (イ) the 解約返戻金 that would be payable on
  surrender at that moment, (ロ) where a lump sum may be taken instead of the annuity, that
  lump sum, and (ハ) the average annual amount receivable over the remaining period
  multiplied by the 複利年金現価率 at the contract's **予定利率** (the factor being prescribed by
  財務省令). For the 無解約返戻金型 designs that dominate this product, (イ) is zero, so the taxable
  value is driven by the published commutation amount (ロ) or the 予定利率 present value (ハ).

### R7 — 国税庁, タックスアンサー No.1140 「生命保険料控除」
- Publisher: 国税庁
- Doc type: tax guidance (タックスアンサー), stated as 令和7年4月1日現在法令等
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched, tag-stripped and read in full)
- Content: the post-2012 (新契約) three-basket regime and the arithmetic that shapes premium
  design. Per basket: premiums ≤ ¥20,000 fully deductible; ¥20,000–¥40,000 → premium×1/2 +
  ¥10,000; ¥40,000–¥80,000 → premium×1/4 + ¥20,000; over ¥80,000 → a flat ¥40,000. Old (旧契約)
  contracts use ¥25,000 / ¥50,000 / ¥100,000 bands to a ¥50,000 cap. **The sum across
  baskets is capped at ¥120,000.** Basis: 所法76, 120, 所令262, 平成29年国税庁告示10号. A pure 収入保障
  contract falls in the 一般生命保険料 basket; the 就業不能/介護 riders sold on the chassis are what can
  reach the 介護医療 basket.

### R8 — e-Gov法令検索, 保険業法施行規則 第68条・第69条
- Publisher: デジタル庁 e-Gov法令検索 (law 408M50000040005, 保険業法施行規則, 平成8年2月29日大蔵省令第5号)
- Doc type: ministerial ordinance
- URL: https://laws.e-gov.go.jp/law/408M50000040005
  (machine-readable full text from https://elaws.e-gov.go.jp/api/1/lawdata/408M50000040005)
- Accessed: 2026-08-20. Retrieved: YES (API returned the complete 30.2 MB XML with HTTP 200;
  Arts. 65–71 extracted; article captions confirmed as 第68条（標準責任準備金の対象契約） and
  第69条（生命保険会社の責任準備金）)
- Content: 第68条 defines the contracts **excluded** from 標準責任準備金 treatment (contracts whose
  reserve varies with the value of assets held in a separate account; contracts with no
  保険料積立金; contracts where the insurer has disclosed that it may change the calculation
  basis; and residual classes designated by the Commissioner), so a conventional guaranteed
  収入保障 contract is inside the standard-reserve regime. 第69条 requires a life insurer to hold,
  per category, 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金, computed on the method filed in the 事業方法書等.

### R9 — 金融庁, 「保険会社向けの総合的な監督指針」 II. 保険監督上の評価項目 II-2 財務の健全性
- Publisher: 金融庁 (Financial Services Agency)
- Doc type: supervisory guideline (監督指針)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read)
- Content: II-2-1-2 積立方式 requires 標準責任準備金 for 標準責任準備金対象契約 in the first and third sectors;
  II-2-1-3-1 保険料積立金の積立 names the discount rate as the **標準利率 (責任準備金告示に規定する予定利率)**;
  II-2-1-2(5) and II-2-1-3-2 cover 危険準備金 I/III/IV; II-2-1-4 covers 価格変動準備金 handling. The
  guideline does not state a numeric 標準利率.

### R10 — 金融庁, 標準責任準備金制度にかかる告示の一部改正 — パブリックコメントの結果等
- Publisher: 金融庁
- Doc type: public-comment result notice
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/20210630.html
- Accessed: 2026-08-20. Retrieved: YES (fetched through WebFetch and read; the 新旧対照表
  attachments 別紙2 and 別紙3 were **not** fetched)
- Content: identifies the operative instruments as **平成8年大蔵省告示第48号** (the notification
  issued under 保険業法第116条第2項 setting the reserve method and the 予定死亡率 and other coefficients
  for long-term contracts) and 平成13年金融庁告示第24号; the 2021 amendments applied from 令和3年10月1日,
  with the 平成13年金融庁告示第24号 change effective 令和4年4月1日.

### R11 — 生命保険文化センター, 「2024（令和6）年度 生命保険に関する全国実態調査＜速報版＞」
- Publisher: 公益財団法人 生命保険文化センター (Japan Institute of Life Insurance)
- Document: 2024（令和6）年度 生命保険に関する全国実態調査 速報版, 2024年11月, 200 pp.
- Doc type: national household survey
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 2.74 MB, 200 pp., text
  extracted; searched for 収入保障 with no hits — the survey does not break the product out)
- Content: market context only. 世帯加入率 (individual annuities included) 89.2% 全生保 / 79.9% 民保
  (previous 89.8% / 80.3%); 世帯普通死亡保険金額 ¥19,360,000 全生保 (previous ¥20,270,000), ¥18,840,000
  民保; 世帯主の普通死亡保険金額 ¥12,580,000 (previous ¥13,860,000); 個人年金保険の世帯加入率 23.2% (previous 24.3%).
  The declining household sum assured is the demand-side backdrop for a product sold as a
  declining income, not a level lump sum.

---

## Fact extraction

### 1. Product architecture — what the benefit actually is

- The insured event is **death during the policy term**, and the benefit is a stream of
  equal monthly instalments (年金) running from the event to the end of the policy term [S1]
  [S3] [S5] [S9] [S12] [S14]. Because the end date is fixed at issue, the number of
  remaining instalments — and therefore the total benefit — **falls month by month as the
  term runs off** [S3] [S5] [S7] [S9] [S12] [S14]. This is the Japanese analogue of UK
  family income benefit.
- Every retrieved contract pairs the death annuity with a **高度障害年金** on identical terms:
  same 年金月額, same payment timetable, same guarantee, and the two are mutually exclusive [S1
  第3条] [S3 第3条] [S5] [S9]. Where the 高度障害年金 has been paid first, no death annuity is
  payable, and vice versa [S1 第3条第3・4項] [S3 第3条第6・7項].
- One carrier makes 高度障害 cover **optional**, supplied by a 高度障害収入保障特則, and offers an
  alternative 障害介護収入保障特則 that cannot be combined with it [S7]. That carrier also allows the
  death cover itself to be switched off (死亡収入保障年金不担保特則) so the contract becomes a pure
  disability/care income policy [S7].
- The dominant chassis is **無解約返戻金型 / 無解約払戻金型** — no surrender value at any point in the
  term [S2] [S5] [S6] [S7] [S9] [S15]. One retrieved product is instead **低解約返戻金型** with a
  real but suppressed surrender value [S12]; and the 約款 of one 無配当 product retains full
  解約返戻金 and 責任準備金 machinery in its text [S1 第23条・第24条].
- The 主契約 has no maturity benefit. One carrier sells a **満期給付金支払特則** that pays a survival
  benefit at expiry if no annuity event occurred, and that benefit is explicitly **not**
  subject to the 70% low-surrender factor [S12].
- No policyholder dividend on any retrieved product [S1 第39条] [S2] [S5] [S15]. Contracts are
  written 無配当.
- No renewal (更新) option [S5]. One carrier offers instead a **保険契約の変換** — conversion into a
  定期保険 or 終身保険 without further underwriting, blocked in the final two years before expiry
  [S6].

### 2. 最低支払保証期間 / 支払保証期間 — the single most important mechanic

- The guarantee is elected by the policy owner at issue, within a range the insurer sets [S1
  第1条] [S3 第2条], and at one carrier it **cannot be changed afterwards** [S3 第2条第2項].
- The mechanic is a **term extension, not a benefit floor**: if the event occurs so late
  that the remaining term is shorter than the guarantee, the annuity payment period is
  extended past the policy expiry date until the guarantee has run [S1 第3条第2項] [S3 第3条第3項]
  [S5] [S12] [S14]. In one 約款 the wording is that "保険期間は、死亡し…た日からその日を含めて最低支払保証期間を
  経過した日までとします" [S1 第3条第2項]; in another it is that "年金支払期間は支払保証期間と同じ期間とします" [S3 第3条第3項].
  Both produce the same cash flow.
- **This is what stops the benefit going to zero at the end of the term.** Without it the
  total benefit would decline linearly to a single instalment on the day before expiry.
- Observed menus (all published):

  | Guarantee menu offered | Source |
  |---|---|
  | 1年 or 5年 | [S2] [S3] |
  | 2年 or 5年 | [S7] |
  | 2年 (5年 also available under the 平準払込方式) | [S9] |
  | 2年 / 3年 / 5年 / 10年 | [S5] |
  | 1年 / 2年 / 5年 | [S12] |
  | 5年 in the published contract examples | [S14] [S15] [S17] |
  | 2年 in the published contract examples | [S6] |
  | "会社の定める範囲内" — no values published | [S1 第1条第2項] |

  So the union of the published menus is **1, 2, 3, 5, 10 years**, and every carrier that
  publishes a menu offers **5年**; every carrier but one offers **2年** or **1年** as the short
  option. 2年 and 5年 are the modal choices.
- One carrier notes that some guarantee lengths become unavailable depending on the
  insured's issue age and the policy term [S5].
- Riders written on this chassis inherit the same guarantee: the 就労不能保障特約's guarantee
  "は主契約の最低保証期間と同一" [S11], and the 障害年金/介護年金 under the 生活支援特則 use the main contract's
  最低支払保証期間 [S5]. Under that 特則, if a disability or care annuity starts just before expiry
  and the insured then dies, the payment period runs from **the first disability/care
  annuity payment date** plus the guarantee [S5].
- The rider construction at one carrier reaches the same shape from the other side: a 逓減型
  収入保障特約 whose 年金支払期間 shortens by one year at every policy anniversary, **floored at 5
  years** [S13 第5条]. That is a guarantee period expressed as a floor on the payment term
  rather than as an extension past expiry.

### 3. Payment timing — instalments in arrears, and where carriers differ

- The commonest timetable: the **first** instalment is paid on the **day before** the first
  monthly policy anniversary falling on or after the event date, and each later instalment
  on the day before the corresponding monthly anniversary, until the payment period ends [S1
  第3条第2項] [S5]. Instalments therefore fall **in arrears** relative to the month they
  support, and the first one is at most one month after the event.
- One carrier instead sets a **年金支払基準日** equal to the event date itself and pays the second
  and later instalments on the monthly anniversaries of that basis date [S3 第3条第3項] — so the
  first instalment is effectively immediate and the run is offset from the policy
  anniversary rather than aligned to it.
- A third variant sets the second-and-later payment dates as the monthly policy
  anniversaries falling after the first payment date [S15].
- One carrier's second-and-later instalments are payable only **while the recipient is
  alive** [S3 第3条第3項]; on the recipient's death the remaining instalments are commuted and
  paid to the 法定相続人 as a lump sum [S3 第7条]. Another reaches the same result by commutation
  on the recipient's death rather than by a survival condition [S1 第3条第6・7項] [S14].
- The **rider** construction pays **annually**, not monthly: the second and later payments
  fall on the annual anniversary of the first payment date [S13 第6条].

### 4. Commutation (一括受取) — the published numbers

- Every retrieved product allows the recipient to take the present value of the unpaid
  instalments as a lump sum. The elections observed:

  | Election | Carriers |
  |---|---|
  | 全部一括受取 (whole, at the start) | [S1] [S2] [S3] [S5] [S6] [S7] [S10] [S12] [S14] [S17] |
  | 一部一括受取 (part at the start, rest as income) | [S2] [S3] [S5] [S7] [S10] [S12] [S14] |
  | 残額一括受取 (rest of the stream, mid-payment) | [S2] [S3] [S12] |
  | 一部すえ置 / 全部すえ置 (deferral of instalments) | [S5] |

  (Text correction, 2026-08-20: the 全部一括受取 row read [S2] [S3] [S5] [S7] [S10] [S12] [S14]
  — six of the nine direct writers — which contradicted the sentence above it and the
  "Commutation elections" row of the comparison matrix below, both of which record whole
  commutation at **all nine**. [S1 第5条第2項] provides that paying the whole present value
  extinguishes the contract, and [S6] and [S17] each publish a worked whole-commutation
  amount, so the three missing tags are added here. Ids and numbering unchanged. The
  一部一括受取 and 残額一括受取 rows were **not** touched and may be understated on the same
  reading; they were not re-verified in this pass.)

- Restrictions: a partial commutation reduces the future 年金月額 and is refused if the residual
  falls below a company minimum [S1 第5条第3項] [S3 第6条第4項] [S14]; at one carrier that minimum
  is stated as **¥50,000** [S7]. 一部一括受取 is not available once the first instalment has been
  paid [S3 第6条第4項第1号], and at two carriers it is limited to **once during the term** [S10]
  [S12]. Paying the whole present value extinguishes the contract [S1 第5条第2項] [S3 第6条第3項]
  [S12] [S14].
- **The discount basis is not published by any of the direct-writing carriers.** The wording
  is "年金月額に所定の係数を乗じた額" [S6], "年金現価とは、将来に発生する利息を差し引いて算出した現在の保険契約の価値" [S10],
  "将来に発生する利子を割引いて算出した現在の保険契約の価値" [S12], and "年金基金設定時の基礎率で計算" [S17].
- **The rider contract does publish the factors.** 年金の現価相当額 = 基本年金額 × the tabulated rate,
  with the note that there is no dependence on the annuitant's age or sex [S13 別表1]:

  | 年金支払期間 | 逓減型 | 固定型 | (second table, 終身保険等 main contract) |
  |---|---|---|---|
  | 45 | 39.542 | — | — |
  | 30 | 27.616 | — | 24.610 |
  | 25 | 23.377 | — | 21.231 |
  | 20 | 18.997 | — | 17.590 |
  | 15 | 14.474 | 14.474 | 13.669 |
  | 10 | 9.801 | 9.801 | 9.444 |
  | 5 | 4.975 | 4.975 | — |

  and 未払年金の現価 by 残存年金支払回数, e.g. 44回 → 38.792, 20回 → 19.007, then further discounted from the
  request date to the day before the next payment date by a company method [S13 別表2]. The
  別表2 factors run about 0.010 above the 別表1 factors at the same count.
- **Derived, not published**: fitting an annuity-due at a flat rate less a small constant to
  the [S13] 別表1 factors gives about **0.61% p.a.** for the first table and about **1.45%
  p.a.** for the 終身保険等 table. The three carriers who publish a worked commutation amount
  imply, if the instalments are treated as monthly in arrears over the exact remaining
  count:

  | Source | Stream | Instalments | Lump sum | Ratio | Implied annual effective rate (**derived**) |
  |---|---|---|---|---|---|
  | [S6] | ¥100,000 × 180 = ¥18,000,000 | 180 | ¥16,594,260 | 0.92190 | ≈ 1.10% |
  | [S10] | ¥200,000 × 300 = ¥60,000,000 | 300 | 約¥55,310,000 | 0.92183 | ≈ 0.66% |
  | [S17] | ¥100,000 × 300 = ¥30,000,000 | 300 | 約¥27,640,000 | 0.92133 | ≈ 0.66% |

  Two of the three amounts are published as approximations (約), so the derived rates carry
  that slack. The **observed commutation ratio clusters tightly at 0.921–0.922** across very
  different terms, which is the more robust observation; the implied rate is not, and any
  use of these numbers must be tagged as a derivation, not a source fact.
- One carrier's リビング・ニーズ特約 states the deduction explicitly and so pins the mechanic even
  where the rate is not given: the 特定状態保険金 is the 年金現価 of the designated 年金月額, capped at
  **¥30,000,000**, **less the interest and premium equivalent for six months** [S5]; another
  words it as the designated 保険金額 less six months' interest and premium equivalent [S2]. The
  claim cannot be made in the final year before expiry [S5].

### 5. Issue-age and term envelopes

| Carrier | 契約年齢 | 保険期間 | 年金月額 | 保険料払込期間 |
|---|---|---|---|---|
| [S6] | 20～70歳 | to 90歳満了 max (75歳満了 with the 収入サポート特約) | ¥50,000～, ¥10,000 steps | = 保険期間 |
| [S7] | 20歳～70歳 | example: 60歳まで | residual floor ¥50,000 after part-commutation | = 保険期間 |
| [S8] | 20～80歳 | 45～90歳 | ¥50,000～, ¥10,000 steps; cap 年金現価保険金額 ¥300,000,000 | = 保険期間 |
| [S12] | 15～75歳 | example: 60歳満了 | ¥50,000～, ¥10,000 steps | = 保険期間 (= 低解約返戻金期間) |
| [S14] | 20歳～70歳 | example: 65歳満期 | example: ¥150,000 | = 保険期間 |
| [S2] | not published | example: 65歳満了 | example: ¥150,000 | explicitly **equal** to 保険期間 |
| [S5] | not published | example: 65歳 | example: ¥200,000 | shown equal to 保険期間 in the しくみ図 |

- Terms are set as **歳満了** (to an attained age), not as an n-year term, in every published
  example: 60歳満了 [S2] [S6] [S9] [S12], 65歳満了 [S2] [S5] [S6] [S14] [S15] [S17], to 90歳 at the
  extreme [S6] [S8].
- **保険料払込期間 equals 保険期間** everywhere it is stated [S2] [S8] [S12], and premiums cease once
  an annuity event occurs [S1 第12条第2項] [S3 第5条] [S8].
- 契約年齢 is the **満年齢 with the fraction truncated** — "契約日における満年で計算し、1年未満の端数は切り捨てます" [S1
  第37条], worked as "35歳7カ月の被保険者の方の契約年齢は35歳" [S14]. Note the contrast with R2: the standard
  table is built for **保険年齢方式**, so a model that reads issue age off the contract and
  applies the standard table without adjustment is mixing two age definitions.

### 6. Premium structure, rate classes and the observed discounts

- Premiums are level for the term (no reviewable-premium mechanic appears in any retrieved
  document), payable 月払 / 半年払 / 年払 [S1 第12条], by 口座振替, 送金, 団体扱/集団扱, or クレジットカード [S1 第13条].
  前納 (advance payment of future premiums) is discounted at a company rate [S1 第14条].
- One 約款 carries a **ステップ払込方式** special provision: premiums after a company-set ステップ期間 are
  the earlier premium multiplied by a company-set factor — a two-step premium pattern rather
  than a level one [S1 第43条].
- One carrier's product page distinguishes a **平準払込方式**, and couples the availability of the
  5-year guarantee to it [S9], implying at least one non-level premium pattern is also sold.
- Rate-class structures observed — the spread is the sharpest cross-carrier difference:

  | Structure | Carrier |
  |---|---|
  | 2 classes: 非喫煙優良体型 / 標準体型 | [S6] |
  | 4 classes: 非喫煙者優良体 / 喫煙者優良体 / 非喫煙者標準体 / 喫煙者標準体 | [S2] [S5] [S14] |
  | 5 classes: the four above plus 保険料率区分なし | [S7] |
  | rate class delivered as a rider (健康体料率特約) | [S11] |
  | 健康診断料率適用特約 + 健康優良割引（区分料率適用特約） as separate discount options | [S16] |

- Published qualification thresholds:
  - BMI **18.0以上27.0未満** and 最大血圧 <140 mmHg **and** 最小血圧 <90 mmHg, plus no tobacco in the
    past year [S2]; BMI **18.0～27.0** with the same blood-pressure limits [S5].
  - Blood pressure **139 mmHg以下かつ 89 mmHg以下** with no tobacco in the past year, for the
    single preferred class [S6].
  - Age-banded thresholds, the only carrier to band them: BMI 17以上27以下 (契約年齢20～39歳) /
    17以上28以下 (40～70歳); 最高血圧 <140 / <150 mmHg; 最低血圧 <90 / <100 mmHg [S14].
  - "喫煙" is defined broadly to include cigars, pipe, chewing and snuff tobacco,
    e-cigarettes, heated tobacco, and nicotine patches/gum [S2] [S5] [S6].
  - Non-smoker classes are verified by a **コチニン (cotinine) test** within a company-set
    range, and passive smoking can fail it [S2] [S5]. Preferred classes require a 健康診断結果通知書
    or 人間ドック result; without it, the standard class applies [S2] [S5].
  - The class is fixed at issue and **cannot be changed later** even if BMI, blood pressure
    or smoking status changes [S2] [S14].
- **No carrier publishes a premium rate table.** The only published rate points found this
  session are single-cell quotations:

  | Plan | 30歳 M / F | 35歳 M / F | 40歳 M / F | 45歳 M / F | Source |
  |---|---|---|---|---|---|
  | 60歳満了, 保証2年, 非喫煙優良体型, 年金月額¥100,000 | ¥1,410 / ¥1,200 | ¥1,340 / ¥1,330 | ¥1,360 / ¥1,400 | ¥1,330 / ¥1,340 | [S6] |
  | 65歳満了, 保証2年, 非喫煙優良体型, 年金月額¥150,000 | ¥2,565 / ¥2,175 | ¥2,565 / ¥2,475 | ¥2,730 / ¥2,700 | ¥2,865 / ¥2,760 | [S6] |
  | 60歳満了, 保証1年, 年金月額¥200,000, 低解約返戻金型 | ¥5,780 (30歳男性) | — | — | — | [S12] |

  Both [S6] rate sets are stated as at 2025年12月2日現在. The 特定疾病保険料払込免除特約 rider premium on the
  first plan for a 30歳 male is **+¥30 (3大疾病型)** or **+¥100 (5大疾病型)** [S6]. A **高額割引制度**
  (banded discount by size) exists at that carrier [S6].
- **予定利率 is not published for any of these products.** No retrieved document states an
  assumed interest rate for the 収入保障 main contract.

### 7. The increasing-benefit variant (逓増型)

- One 約款 offers 定額型 and **逓増型** as the two 保険契約の型 [S1 第1条]. Under 逓増型 the monthly annuity is
  `年金月額 = 基準年金月額 × (1 + 0.03 × 経過年数)` where 経過年数 is the number of completed years from the
  契約日 counted at each annual policy anniversary, fractions truncated [S1 第2条第1・2項].
- The interaction with the guarantee is spelled out: where the event falls within the
  guarantee period of the expiry date, the **first twelve months** are paid at the 年金月額 in
  force at the date of death or 高度障害, and each subsequent year during the guarantee adds
  **3% of the 基準年金月額** [S1 第2条第3項]. So the escalation continues through the extended tail.
- No other retrieved carrier offers an escalating benefit on this product.

### 8. The declining-total illustration — the published worked examples

These are the numeric anchors any model should reproduce.

- 契約年齢30歳, 保険期間・年金支払期間 65歳, 最低支払保証期間 5年, 年金月額 ¥200,000 [S5]:
  - death in the first policy month → **420 instalments (35 years) = ¥84,000,000**
  - death 14 years 6 months after issue → **246 instalments (20 years 6 months) =
    ¥49,200,000**
  - death 33 years after issue → remaining term is 2 years, so the guarantee binds: **60
    instalments (5 years) = ¥12,000,000**
  - and, with the 配偶者同時災害死亡時割増特則 in force and both spouses dying in the same accident two
    years before expiry, each of the two annuities pays its own guaranteed 60 instalments —
    ¥12,000,000 + ¥12,000,000.
- 契約年齢30歳, 保険期間 65歳満期, 年金支払保証期間 5年, 年金月額 ¥150,000 [S14]:
  - month 1 → **420 payments = ¥63,000,000**
  - 15 years 1 month → **240 payments = ¥36,000,000**
  - 30 years 1 month → **60 payments = ¥9,000,000** (remaining term is exactly 5 years)
- 契約年齢30歳, 保険期間 65歳満期, 年金支払保証期間 5年, 年金月額 ¥100,000, relaxed underwriting [S15]:
  - death at 20 years 3 months → **178 payments = ¥17,800,000**
  - death by illness at 10 months (within year 1) → **¥100,000 × 50% × 411 payments =
    ¥20,550,000**
- 35歳男性, 基準年金月額 ¥200,000, 60歳まで, death within one month [S10]: monthly total ¥60,000,000,
  commuted 約¥55,310,000.
- 契約年齢30歳, 基本年金月額 ¥100,000, 65歳満了, 最低支払保証期間 5年, event at 40歳 (契約から10年1か月目) [S17]: commuted
  約¥27,640,000 (against 300 remaining instalments).

### 9. Exclusions, contestability, grace, lapse and reinstatement

- **Suicide**: no annuity is payable where the insured dies by suicide **within three years
  of the 責任開始期** (re-set to the last 復活 where the contract has been reinstated) [S1 第3条] [S3
  第3条] [S4] [S5]. This is materially longer than the twelve-month UK clause. Where the
  exclusion bites, the insurer pays the **責任準備金** to the policy owner [S1 第3条第10項], or,
  where the policy owner deliberately caused the death, nothing at all [S3 第3条第17項].
- Other 免責事由: 保険契約者 or 受取人の故意, and 戦争その他の変乱 [S1 第3条] [S3 第3条]. The war clause is a **削減
  (reduction)** power, not an absolute exclusion: where the increase in claims would
  materially affect the calculation basis, the insurer may pay in full or reduced [S1 第4条],
  and where it pays a reduced commuted amount that amount may not fall below the 責任準備金 [S3
  第4条].
- **告知義務違反**: the contract may be rescinded within **two years** of the 責任開始日 (or the last
  復活日); after two years it may still be rescinded if the claim event occurred within those
  two years [S1 第21条第5号] [S4] [S5].
- **払込猶予期間 (grace)**, identical wording at two carriers:
  - 月払: from the first day of the month following the 払込期月 to the last day of that month [S1
    第15条] [S3] [S4].
  - 年払/半年払: from the first day of the following month to the monthly policy anniversary in
    the month after that, with the special rule that anniversaries on the last day of
    February, June and November run to the last day of April, August and January
    respectively [S1 第15条] [S4].
  - If a claim arises during grace, the unpaid premium is deducted from the annuity payable
    [S1 第16条第1項]; if the annuity is insufficient, the shortfall is taken from the 死亡時保障換算額
    (the amount that would be paid on commutation at the first annuity event) and the 基準年金月額
    restated [S1 第12条第5項].
- **失効** takes effect on the day after the grace period ends [S1 第15条第2項].
- **復活 (reinstatement)** is available for **three years** from the lapse date, subject to
  fresh underwriting and payment of the arrears plus interest at a company rate [S1 第17条]
  [S3] [S5]. Two carrier-specific narrowings: it is barred once the policy owner has claimed
  the surrender value [S1 第17条第1項], and the window shortens to **two years** where special
  conditions were applied at issue [S5]. The reinstated contract keeps the **same rate
  class** it had before lapse [S3].
- **契約者貸付 and 自動振替貸付 are explicitly not offered** on the 無解約払戻金型 design [S2]. With no cash
  value there is nothing to lend against, so the automatic-premium-loan mechanic that
  carries a Japanese savings policy through non-payment simply does not exist here — the
  policy lapses at the end of grace.
- **時効**: the right to claim an annuity, the 責任準備金, the 解約返戻金 or a premium waiver
  extinguishes after **three years** without a claim [S1 第41条].
- **クーリング・オフ**: 14 days from the later of the application date and receipt of the
  重要事項説明書（注意喚起情報）, with the full amount paid returned [S5].

### 10. 保険料払込免除 (premium waiver)

- The **main-contract** waiver is narrow and accident-only: the insured must suffer a 身体障害の
  状態 as a direct result of a 不慮の事故 occurring after the 責任開始期, within **180 days** of the
  accident, during the premium-paying period [S1 第6条] [S3 第8条] [S5] [S6]. One carrier states
  the negative explicitly: "疾病により所定の身体障害の状態に該当した場合は、保険料のお払込みは免除されません" [S5].
- The 身体障害の状態 list has eight limbs — loss of sight in one eye; loss of hearing in both ears;
  loss of an upper limb at or above the wrist, or of its use, or of the use of two of its
  three major joints; the same for a lower limb at or above the ankle; permanent total loss
  of use of all ten fingers; loss of all five digits of one hand, or of four including the
  thumb and index finger; loss of all ten toes; and severe permanent spinal deformity or
  movement disorder [S1 別表4].
- Waiver 免責: 故意 or 重大な過失 of the policy owner or insured, the insured's criminal act,
  accidents arising from mental disorder or intoxication, driving without a licence, driving
  under the influence, earthquake/eruption/tsunami, and war — with the earthquake and war
  exclusions relaxable at the insurer's discretion where the effect on the calculation basis
  is small [S1 第6条].
- Once waived, premiums are **treated as if paid** at each subsequent due date, and contract
  variations are frozen from that point [S1 第6条第4・5項].
- Waiver does not apply to 一時払 contracts [S1 第6条第7項].
- Disease-based waiver is sold as a **rider**, with meaningfully different triggers:

  | Rider | Cancer | Heart | Cerebrovascular | Source |
  |---|---|---|---|---|
  | 特定三疾病保険料払込免除特則（2025） | first diagnosis on/after the がん責任開始日 = **day 91** from the 責任開始日; 上皮内新生物 included | inpatient admission **or** a specified operation | inpatient admission **or** a specified operation | [S2] |
  | 3大疾病保険料払込免除特約Ⅱ | first diagnosis on/after the 悪性新生物責任開始期 = the day after **90 days** have elapsed; 上皮内新生物 included | specified operation **or** ≥15 consecutive days in hospital | specified operation **or** ≥15 consecutive days in hospital | [S5] |
  | 特定疾病保険料払込免除特約 (3大疾病型 / 5大疾病型) | first diagnosis, 上皮内新生物 included, **90-day** 不てん補期間 | 急性心筋梗塞: ≥1 day inpatient or operation; other heart disease: ≥20 consecutive days or operation | 脳卒中: ≥1 day inpatient or operation; other: ≥20 consecutive days or operation; 5大疾病型 adds 肝疾患 and 腎疾患 at ≥20 days or operation | [S6] |
  | 七大疾病・就労不能保険料免除特約 | — | — | — (七大疾病 plus a 就労不能 trigger) | [S11] |
  | 保険料払込免除特約（22）, priced as a premium **loading** | — | — | — | [S16] |

- Waiver of the main contract's premium also waives the premiums of every attached 特約・特則
  [S5].
- One rider carries a rescission-style unwind: if the insured is diagnosed with cancer
  before the cancer cover starts and so cannot be waived, the policy owner may void the
  rider within six months of that diagnosis; if no request is made in six months the rider
  continues but can never waive premiums for cancer [S5].

### 11. Disability and long-term-care income variants written on this chassis

These are what a Japanese carrier means by 就業不能保障 on a 収入保障 policy. They are riders or 特則,
not the main contract.

- **生活支援特則** [S5]: adds a 障害年金 payable on the 高度障害状態 **or** on a 特定障害状態 defined as a
  身体障害者福祉法 grade 1–4 disability evidenced by the issue of a 身体障害者手帳, and a 介護年金 payable on
  certification at **要介護1以上** under 公的介護保険, the certification taking effect retrospectively
  from the application date. Both pay the 年金月額, both inherit the main contract's 最低支払保証期間,
  both are **毎月受取 only** (no commutation), the two cannot be paid together, and a death
  claim supersedes them. The 特則 cannot be added mid-term. Where it is attached, the main
  contract's 高度障害年金 trigger is absorbed into the 障害年金.
- **障害介護収入保障特則 / 高度障害収入保障特則** [S7]: mutually exclusive; the 障害介護 version triggers on
  身体障害者1～4級, 障害等級1～2級 (grade 2 excluding mental causes), or 要介護1～5.
- **無解約返戻金型就労不能保障特約** [S11]: pays a 就労不能年金 monthly to the rider's expiry, with a guarantee
  period equal to the main contract's 最低保証期間; extinguished by a death or 高度障害 claim on the
  main contract; must be attached together with the 七大疾病・就労不能保険料免除特約.
- **収入サポート特約（Z02）** [S6]: two benefits. A 短期収入サポート月額給付金 equal to **0.5 ×** the 長期収入サポート給付月額
  (¥25,000–¥500,000) payable for a month in which the insured spent ≥10 days in hospital or
  in 在宅療養, limited to **60 occurrences in total**; and a 長期収入サポート月額給付金 of ¥50,000–¥1,000,000
  in ¥10,000 steps payable to expiry **while the insured lives**, triggered by 高度障害状態, by an
  accident-caused 身体障害の状態 within 180 days, or by the award of a grade 1 or 2 障害基礎年金 under
  国民年金法. Its 生存支払保証期間 equals the main contract's 年金支払保証期間. Benefit ceilings are set by the
  insured's income — under ¥4m → ≤¥100,000; ¥4m–¥6m → ≤¥200,000; ¥6m and over → ≤¥1,000,000;
  homemakers ≤¥200,000 regardless of income; those keeping house, living on a pension or on
  assets ≤¥100,000 — and in all cases ≤¥1,000,000 **and** ≤ the main contract's 年金月額.
  Attaching this 特約 caps the main contract at 75歳満了.
- **無解約返戻金型メンタル疾患保障付七大疾病保障特約** [S11]: a 生活サポート年金 paid monthly for a **fixed** 特約年金支払期間 of 2
  or 5 years — a term-certain annuity, not a run-off one — with the remainder commuted on
  the recipient's death or 高度障害.
- **ストレス・メンタル疾病サポート特則** [S16]: triggered by hospitalisation or home medical care continuing
  ≥30 days, and priced as a premium **loading**.
- **配偶者同時災害死亡時割増特則** [S5]: where the insured and the legally married spouse both die from
  the **same** 不慮の事故 within 180 days of it, a 災害割増遺族年金 equal to the 年金月額 is paid on top of
  the 遺族年金, with the same guarantee period. **The premium is the same whether or not the 特則
  is applied** — a free doubling of the benefit in a narrow state.

### 12. Riders common to the chassis

- **リビング・ニーズ特約** is on every retrieved product, attached automatically and free [S2] [S5]
  [S7]. On a life expectancy of six months or less it converts the designated part of the
  annuity into a lump sum equal to its 年金現価 less six months' interest and premium
  equivalent, capped at ¥30,000,000 [S5], and the corresponding 年金月額 is extinguished
  retroactively to the claim date [S2].
- **指定代理請求人特約 / 指定代理請求特約** — a nominated proxy claimant where the insured cannot claim [S1]
  [S5] [S12].
- The 約款 of the traditional carrier carries a much longer 特約 menu on the same main contract:
  定期保険特約, 災害割増特約, 傷害特約, 災害入院特約, 疾病入院特約, 特別条件特約, 保険料口座振替特約, 団体扱特約, 特別団体扱特約, 集団扱特約 [S1]. The
  低解約返戻金型 product's menu is 平準定期保険特約, 災害割増特約, 特定疾病保障定期保険特約, 傷害特約, がん保障定期保険特約,
  リビング・ニーズ特約（2009）, 介護保障定期保険特約, 保険契約者代理特約, 軽度介護保障特約, 指定代理請求特約 [S12].

### 13. Surrender, reduction and the 低解約返戻金型 variant

- On the dominant design there is **no surrender value at any duration** [S2] [S5] [S6] [S7]
  [S9] [S15], and surrender is in any case available only **before** an annuity event [S1
  第23条] [S3].
- **基準年金月額の減額** is available: the reduced portion is treated as surrendered, any
  corresponding 解約返戻金 is refunded, future premiums are restated, and the reduction takes
  effect from the policy anniversary on or after the request [S1 第28条]. It is refused if the
  residual falls below the company minimum [S1 第28条第1項] [S7]. On a 無解約払戻金型 contract a
  reduction produces no refund at all [S3].
- The **低解約返戻金型** variant [S12]: the surrender value during the premium-paying period (which
  is also the 低解約返戻金期間) is the ordinary value computed from the months of premium paid and
  elapsed, multiplied by a **低解約返戻金割合 of 70%**. The same 70% factor applies on a reduction
  of the 年金月額. The 満期給付金 under the 満期給付金支払特則 is **not** reduced by the 70% factor. Since the
  premium-paying period equals the whole policy term here, the step-up to 100% at 払込満了 that
  characterises 低解約返戻金型 whole life has no analogue — the suppression runs to expiry.
- 保険期間 and 保険料払込期間 may be shortened by variation, subject to the result staying inside the
  company's range [S1 第27条].
- 2年以上継続 policyholders may take out another individual policy without medical evidence
  within one month of expiry or surrender, capped at the **lowest** 死亡時保障換算額 over the
  remaining term [S1 第29条].

### 14. 高度障害状態 — the definition, and why it matters for the mortality basis

- The seven-limb definition, identical in form across the retrieved 約款 [S1 別表3]: permanent
  total loss of sight in both eyes; permanent total loss of speech or mastication; a severe
  disorder of the central nervous system, mind, or thoracic/abdominal organs requiring
  permanent constant nursing care; loss of both upper limbs at or above the wrist or
  permanent total loss of their use; the same for both lower limbs at or above the ankle;
  loss of one upper limb at or above the wrist together with loss of one lower limb at or
  above the ankle or permanent total loss of its use; and permanent total loss of use of one
  upper limb together with loss of one lower limb at or above the ankle.
- Both carriers carry the **expiry-date look-through**: where at expiry the insured's
  condition met every limb of the definition except that recovery could not yet be ruled
  out, and the condition then persists and recovery is later ruled out, the insured is
  **deemed** to have met the definition on the expiry date and the 高度障害年金 is paid [S1
  第3条第12項] [S3 第3条第9項]. Instalments already fallen due are then paid as a lump sum [S1
  第3条第13項].
- **This is the modelling trap.** 生保標準生命表2018（死亡保険用）is stated to be "高度障害を含む死亡率" [R2] — the
  高度障害 incidence is already inside the published qx. Adding a separate disability decrement
  on top of the standard table double-counts.

### 15. Taxation of an income-form death benefit

- At the death, the object taxed for **相続税** is the **年金受給権** (the right to the annuity),
  not the instalments [R5]. A 有期定期金 is valued at the **greatest** of the surrender value
  that would be payable, the lump sum available in lieu of the annuity, and the average
  annual amount receivable over the remaining period multiplied by the 複利年金現価率 at the
  contract's 予定利率 [R6, 相続税法第24条第1項第1号]. For a 無解約返戻金型 contract the first limb is zero, so
  the taxable value is set by the published commutation amount or the 予定利率 present value.
- Each subsequent instalment is then **雑所得** in the recipient's hands, but only in part: the
  first year of payment is wholly exempt and the taxable share rises **in steps**
  thereafter, the schedule keyed to the 相続税評価割合 — e.g. a 相続税評価割合 above 50% and up to 55%
  gives a 課税割合 of 45% [R4, 所得税法第35条, 所令185・186]. The step schedule is what prevents the same
  economic value being taxed twice.
- One carrier discloses the consequence on the product page: "万一のときにお受け取りいただく毎月の
  年金は雑所得として源泉徴収の対象となる場合があります。このため、実際にお受け取りになる金額が上記よりも少なくなる場合があります" [S12].
- On the premium side, a pure 収入保障 contract falls in the **一般生命保険料** basket of the post-2012
  生命保険料控除. Per basket the deduction is the full premium up to ¥20,000, then
  premium×1/2+¥10,000 to ¥40,000, then premium×1/4+¥20,000 to ¥80,000, then a flat ¥40,000;
  the total across the three baskets is capped at **¥120,000** [R7]. The 介護医療 basket is what
  the 就業不能/介護 riders on this chassis can reach.

### 16. Valuation and regulatory framing

- A conventional guaranteed 収入保障 contract is inside the **標準責任準備金** regime: 保険業法施行規則第68条
  excludes only separate-account-linked contracts, contracts with no 保険料積立金, contracts where
  the insurer has disclosed it may change the basis, and residually designated classes [R8].
  第69条 requires 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金 [R8].
- The reserve discount rate is the **標準利率**, defined by the supervisory guideline as
  "責任準備金告示に規定する予定利率" [R9], the 告示 being **平成8年大蔵省告示第48号** issued under 保険業法第116条第2項, amended
  alongside 平成13年金融庁告示第24号 with effect from 令和3年10月1日 and 令和4年4月1日 respectively [R10].
- The valuation mortality is 生保標準生命表2018（死亡保険用）, applying from April 2018 [R3], constructed
  by the IAJ as the FSA's 指定法人 under 保険業法第122条の2 [R3].
- The table is a **valuation** basis, not experience: it carries a forward
  mortality-improvement allowance (2.5% p.a. for five years then 1.0% p.a. for three), a 2σ
  risk-theory margin capped at 130% of the unadjusted rate, and is smoothed and extrapolated
  [R2]. Any best-estimate basis must be a stated adjustment of it.
- Market backdrop: 89.2% of households hold life insurance (79.9% with private carriers) and
  the average household 普通死亡保険金額 has fallen to ¥19,360,000 from ¥20,270,000 in the previous
  survey, with the household-head figure at ¥12,580,000 [R11]. The survey does not report
  収入保障保険 as a separate category.

---

## Variation across carriers

The drafting pass turns this table into the product's "Variations across insurers" section.
Every cell is a published fact from the tagged source; blanks mean the carrier does not
publish it.

| Feature | [S1] | [S2] [S3] [S4] | [S5] | [S6] | [S7] | [S8]–[S11] | [S12] | [S13] | [S14] [S15] | [S16] [S17] |
|---|---|---|---|---|---|---|---|---|---|---|
| Guarantee menu | 会社の定める範囲内 | 1年 / 5年 | 2/3/5/10年 | 2年 (examples) | 2年 / 5年 | 2年 (5年 under 平準払込方式) | 1年 / 2年 / 5年 | 5-year **floor** on a shrinking term | 5年 (examples) | 5年 (example) |
| Guarantee implemented as | term extension past expiry | 年金支払期間 = 支払保証期間 | term extension | — | — | — | term extension | floor on the 年金支払期間 | term extension | — |
| Instalment frequency | monthly, day before the monthly anniversary | monthly, anniversary of the 年金支払基準日 | monthly, day before the monthly anniversary | monthly | monthly | monthly | monthly | **annual** | monthly, anniversary after the first payment date | monthly |
| Survival condition on instalments | no (commuted on death) | **yes** | no | — | — | — | — | — | no (commuted on death) | — |
| Rate classes | not published | 4 | 4 | **2** | **5** (incl. 保険料率区分なし) | via 健康体料率特約 | not published | n/a (rider) | 4, thresholds **age-banded** | 区分料率適用特約 + 健康診断料率適用特約 |
| Benefit shapes | 定額型 / **逓増型 (+3%/yr)** | 定額型 only | 定額型 only | 定額型 only | 定額型 only | 定額型 only | 定額型 only | **逓減型 / 固定型** | 定額型 only | 定額型 only |
| Surrender value | 解約返戻金 machinery retained | **none** | **none** | **none** | **none** | **none** | **低解約返戻金型, 70%** | n/a (rider) | none | **none** |
| 高度障害 cover | in the main contract | in the main contract | in the main contract | in the main contract | **optional 特則** | in the main contract | in the main contract | in the rider | in the main contract | in the main contract |
| Graded early benefit | no | no | no | no | no | no | no | no | **50% in year 1 on the 引受緩和型** [S15] | no |
| Maturity benefit | no | no | no | no | no | no | **満期給付金支払特則** | no | no | no |
| Commutation elections | whole / part | whole / part / residual | whole / part / residual / **deferral** | whole / part / residual | whole / part | whole / part / residual, part once only | 4 shapes, part once only | before and during payment | whole / part | whole |
| Commutation factors published | no | no | no | worked example only | no | worked example only | no | **yes, 別表1 and 別表2** | no | worked example only |
| Issue ages | not published | not published | not published | 20–70 | 20–70 | **20–80** | **15–75** | n/a | 20–70 | not published |
| Maximum expiry | not published | not published | not published | **90歳** (75歳 with 収入サポート特約) | not published | **90歳** | not published | n/a | not published | not published |
| Benefit cap | not published | not published | LN特約 ¥30m | 年金月額 ≥¥50,000 on any election | residual ≥¥50,000 | **年金現価保険金額 ¥300m** | not published | n/a | not published | not published |
| Policy loan / APL | 約款 retains 解約返戻金 | **explicitly not offered** | — | — | — | — | — | — | — | — |
| Non-level premium option | **ステップ払込方式** | no | no | no | no | 平準払込方式 named as one option | no | n/a | no | no |
| Relaxed-underwriting version | — | — | **FWD収入保障引受緩和** named | — | **explicitly not offered** | — | — | — | **かんたん告知はなさく収入保障** | — |

**What does not vary.** Across all nine carriers: the benefit is a level monthly annuity
from the event to a fixed expiry date, so the total falls as the term runs off; a guarantee
period floors the tail; 高度障害 is paid on the same terms as death and the two are mutually
exclusive; the suicide exclusion runs **three years** from the 責任開始期; 告知義務違反 contestability
runs **two years**; grace for monthly premiums runs to the end of the following month;
reinstatement is available for **three years** after lapse; premiums cease on an annuity
event; the recipient may commute the remaining instalments; the products are 無配当 with no
policyholder dividend; and 保険料払込期間 equals 保険期間.

---

## Fetch failures and gaps

Every URL that failed, and every claim left [unverified].

- **SOMPOひまわり生命商品パンフレット** —
  `https://www.himawari-life.co.jp/-/media/himawari/files/product/pamphlet/family.pdf?la=ja-JP`.
  HTTP 200, 2.40 MB, 17 pp. downloaded successfully, but the PDF uses subset fonts without a
  ToUnicode map and **pypdf extraction returns mojibake for essentially the whole
  document**. Nothing from this file is cited. The facts it would have carried are instead
  sourced from the carrier's product pages [S8]–[S11]; what is lost is the full issue-limit
  table by plan type and the rider premium detail.
- **フコクしんらい生命商品パンフレット・契約概要・注意喚起情報** —
  `https://www.fukokushinrai.co.jp/consider/product/general/shuunyuuhoshou/pdf/prod.pdf`.
  HTTP 200, 2.96 MB, 16 pp. downloaded, **same CID-font extraction failure**; the pages are
  also typeset vertically. Nothing from this file is cited; the product page [S12] carries
  the headline parameters instead. Lost: the 低解約返戻金 surrender-value table and the full rider
  specification.
- **第一ネオ生命ご契約のしおり・約款 (067F) and 重要事項説明書 (067F)** —
  `https://download.neofirst.co.jp/webcatalog/yakkan/webyakkan/067F.pdf` (7.43 MB, 262 pp.) and
  `https://download.neofirst.co.jp/webcatalog/yakkan/webimportant/067F.pdf` (2.14 MB, 32 pp.).
  Both HTTP 200 and downloaded, both **CID-broken on extraction**. All 第一ネオ生命 facts here
  come from the product page [S7]; the 約款-level mechanics (payment timetable, guarantee
  wording, waiver detail) are therefore **not** verified for that carrier.
- **アクサダイレクト生命収入保障2** — the 約款 index could not be located. The file at
  `https://www.axa-direct-life.co.jp/pdf/yakkan_m.pdf` fetched with HTTP 200 but is the
  **定期医療** booklet, not the 収入保障 one, and `https://www.axa-direct-life.co.jp/products/income/example/`
  returns a meta-refresh stub to the site root. No AXA Direct facts are asserted anywhere in
  this file.
- **チューリッヒ生命収入保障保険プレミアムDX FAQ** —
  `https://www.zurichlife.co.jp/faq/insurance/hoken/shunyuhoshoudx`. Fetched HTTP 200 but the page
  is an FAQ **index**; the answer bodies are behind separate URLs that were not enumerated.
  Consequence: the widely reported claim that プレミアムDX offered a **1年/2年/5年/10年** guarantee
  menu, a 20–70 issue-age range and a ¥50,000 minimum 年金月額 is **[unverified]** — it appeared
  only in a search-result summary, not in a retrieved document. The [S6] figures for the
  current 収入保障保険プラチナ are retrieved and are what this file relies on.
- **オリックス生命 issue-age and term envelope** — neither the 約款 [S3] nor the 契約概要 [S2] publishes
  the 契約年齢 range or the 保険期間 range; the 約款 only says "会社の定める契約年齢の範囲" [S3 第34条・第35条 area].
  Left blank rather than inferred.
- **Commutation discount rate at the direct writers** — not published by [S2] [S3] [S5] [S6]
  [S10] [S12] [S14] [S17]. The three implied rates in §4 and the two fitted rates from the
  [S13] factor tables are **derived by me from published amounts**, not source facts, and
  are labelled as such. Anything the drafting pass takes from them must be tagged **[std]**
  with the observed 0.66%–1.45% range, not [S#].
- **予定利率** — no retrieved document states an assumed interest rate for any 収入保障 main
  contract. The [S13] factor tables are the closest published proxy, and they belong to a
  rider attached to a different main contract.
- **標準利率, numeric level** — [R9] establishes that the reserve discount rate is the 標準利率
  defined in the 責任準備金告示, and [R10] identifies the 告示 and the 2021 amendment dates, but **no
  numeric 標準利率 was retrieved**. The 新旧対照表 attachments (別紙2, 別紙3) on the FSA public-comment
  page were not fetched. Any statement of the current 標準利率 level, and of the
  quarterly-versus-annual reset split between 一時払 and 平準払 products, is **[unverified]** here
  and belongs to the cross-product reference library rather than to this file.
- **生保標準生命表2018（年金開始後用）** — the 標準生命表 index [R3] lists only 標準生命表2018 and 標準生命表2007, and the
  retrieved 2018 PDF [R1] contains four tables: 死亡保険用男/女 and 第三分野男/女. Whether a
  2018-vintage 年金開始後用 table exists is **[unverified]**; the 死亡保険用 table is the relevant one
  for this product in any case, since the annuity here is a term-certain with no mortality
  on the recipient except where a survival condition applies [S3 第3条第3項].
- **Rate tables** — no carrier publishes a per-mille or per-¥10,000-of-annuity rate table.
  Only the single-cell quotations in §6 are public, and two of them are dated 2025年12月2日. A
  rate basis for the reference model must be constructed from [R1] plus loadings and marked
  **[std]**.
- **Lapse and persistency experience** — nothing product-specific was found. [R11] does not
  break out 収入保障保険. Any lapse assumption is **[std]**.
- **Market share and new-business volume for 収入保障保険** — not found in a retrieved source. The
  生命保険協会「生命保険の動向」series was not fetched this session. Any claim about the product's share of
  Japanese individual new business is **[unverified]**.
- **相続税法施行令 / 財務省令定める複利年金現価率** — [R6] establishes that the factor is prescribed by 財務省令,
  but the ministerial ordinance itself was not fetched, so the numeric factors are
  **[unverified]**.
- **The 0.010 gap between [S13] 別表1 and 別表2 factors** at equal payment counts is a real,
  retrieved observation, but **no explanation for it is published** and none is asserted
  here.
- **The e-Gov HTML pages** (`laws.e-gov.go.jp/law/...`) return an 800-byte JavaScript shell
  to plain fetchers and are useless; both statutory citations [R6] [R8] were obtained from
  the e-Gov **API** endpoints instead, which return complete XML with HTTP 200. Recorded so
  the next research pass does not repeat the failure.
- **Carriers not fetched**: 明治安田生命, 日本生命, 第一生命, 太陽生命, 大同生命, メットライフ生命, T&Dフィナンシャル生命, 楽天生命,
  マニュライフ生命, アフラック. The nine-carrier set here spans every structural variant the product
  exhibits — 無解約返戻金型 and 低解約返戻金型, 定額型 and 逓増型 and 逓減型, main-contract and rider construction,
  monthly and annual instalments, fully underwritten and relaxed underwriting, 2/4/5 rate
  classes — so adding a tenth would mainly refine the variation table.
