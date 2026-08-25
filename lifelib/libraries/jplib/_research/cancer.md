# がん保険 (cancer insurance) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese がん保険 (*gan hoken*, cancer insurance) liability cash flow
reference model — a third-sector (第三分野, *dai-san bun'ya*) product whose benefits are
triggered by cancer diagnosis, cancer treatment, cancer hospitalisation, cancer surgery and
cancer outpatient attendance rather than by death.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial/statistical reference) pointing at a document actually retrieved and read
during this session, or is tagged [unverified] where it is general knowledge or a secondary
snippet not confirmed against a retrieved document. Access date for all fetched sources:
2026-08-20. Source ids are FROZEN — the product documents cite against them and nobody may
renumber them.

Seven carriers are covered: five life insurers writing a stand-alone cancer main contract, one
life insurer writing a treatment-benefit-only main contract, and one non-life insurer writing
the 自由診療 (*jiyū shinryō*, non-reimbursed / free-choice medicine) expense variant. Company
and branded product names appear here and in `sources.md` only.

---

## Primary sources

### S1 — オリックス生命, 「がん保険Believe［ビリーブ］ ご契約のしおり／約款」 (policy conditions + policyholder booklet)
- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: がん保険Believe ご契約のしおり／約款, file `yakkan_believe_20240402.pdf`, 140 pp.
  The booklet is in two halves: ご契約のしおり (pp. 1–~64, fully text-extractable) followed by
  the 普通保険約款 and 特約条項 (image/subset-font pages, not text-extractable).
- Doc type: ご契約のしおり・約款 (policyholder booklet + policy conditions)
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/yakkan_believe_20240402.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 140 pp.; text layer extracted —
  the しおり half extracted cleanly, the 約款 half did not; all facts below are taken from the
  しおり half, which restates each 約款 article and cross-references it by number)
- Key content: がん責任開始日 (91st day) definition and the invalidity rule for pre-waiting-period
  diagnosis; benefit menu (がん治療給付金 / がん初回診断一時金 / がん入院給付金 / がん手術給付金 /
  がん退院一時金) with triggers and repeat cycles; 上皮内新生物 included in the definition of がん;
  premium-waiver triggers; grace periods by payment mode; reinstatement window; surrender-value
  rule; がん先進医療特約(2018) and がん通院特約 terms and limits; 告知義務違反 contestability.

### S2 — オリックス生命, 「がん保険Believe 商品概要のご説明」 (product summary)
- Publisher: オリックス生命保険株式会社
- Document: 商品概要のご説明, file `believe_shohin_direct.pdf`, 2 pp.
- Doc type: 商品概要 (product summary, the 契約概要-role document for direct sales)
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/believe_shohin_direct.pdf
- Accessed: 2026-08-20. Retrieved: YES, with a caveat. The PDF uses a subset font whose
  numerals decode to combining-mark glyphs rather than ASCII digits. The glyph→digit mapping
  was recovered and then **cross-checked against two values independently confirmed in [S1]**
  (がん先進医療給付金 通算2,000万円 and がん先進医療一時金 1回の療養につき50万円) plus one
  more (退院後30日未満). All three decoded correctly, so the benefit multiples read from this
  document are reported below as sourced rather than [unverified].
- Key content: the full benefit-multiple table expressed as multiples of 基本給付金額
  (100× / 50× / ×日数 / 20× / 10×), the 契約例 基本給付金額 ¥10,000, and the rider limits.

### S3 — オリックス生命, がん保険Believe 商品ページ (product page)
- Publisher: オリックス生命保険株式会社
- Doc type: product page (consumer/direct)
- URL: https://www.orixlife.co.jp/cancer/believe/
- Accessed: 2026-08-20. Retrieved: YES
- Key content: the document index (which named PDFs exist and at which URLs); the headline
  ¥1,000,000 がん初回診断一時金 at the ¥10,000 基本給付金額 course.

### S4 — オリックス生命, がん保険Believe 通信販売用パンフレット (brochure)
- Publisher: オリックス生命保険株式会社
- Document: 通信販売用パンフレット, file `believe_pamphlet.pdf`, 5 pp.
- Doc type: 商品パンフレット
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/believe_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: **NO (partial)** — the file downloaded (5 pp., 1.5 MB) but
  its text layer is subset-encoded with no usable ToUnicode map: Japanese renders as mojibake
  and **all numerals are dropped entirely**. Nothing quantitative was taken from it. Any fact
  that would have come only from this document is marked [unverified] below.

### S5 — 東京海上日動あんしん生命, 「がん治療支援保険 契約概要／注意喚起情報・ご契約のしおり・約款」
- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: がん治療支援保険［無配当］, 2013.10改定 edition, file `A0203131102.pdf`, 156 pp.
  Print code 資13-KF04-035. 契約例 calculation base date 平成25年10月22日 (2013-10-22).
- Doc type: 契約概要／注意喚起情報 + ご契約のしおり・約款
- URL: https://www7.tmn-anshin.co.jp/yakkan/pdf/A0203131102.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 156 pp.; the 契約概要 and
  自動更新 pages extracted cleanly, most of the 約款 body did not — subset fonts). All facts
  below come from the extracted 契約概要 pages.
- Key content: the only **published premium example** found in this session; the 責任開始期
  = 90 days after inception; 診断給付金 repeat cycle of 2 years with an explicit
  再発／転移／新生 trigger list; 抗がん剤治療特約 with a 60-month lifetime cap; 通院給付金 with
  a 45-day-per-hospitalisation and 730-day lifetime cap; surgery benefit with a 60-day
  re-payment bar for certain procedures; the two-part surrender-value formula after premium
  payment ends; 自動更新 mechanics to age 90 with an option to convert to 終身.

### S6 — ジブラルタ生命, 「終身がん保険（無配当） ご契約のしおり・約款」 (policy conditions)
- Publisher: ジブラルタ生命保険株式会社 (Gibraltar Life Insurance)
- Document: 終身がん保険（無配当）ご契約のしおり・約款 2022年12月版, file
  `L105_syusin_gan_202212.pdf`, 132 pp. Internal 約款 code B5-022, 最終修正日 2022-09-13,
  データ出力日 2022-09-26.
- Doc type: ご契約のしおり・約款
- URL: https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/L105_syusin_gan_202212.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 132 pp.; the 約款 body extracted
  cleanly and was read article by article)
- Key content: the **only retrieved contract carrying a genuine 解約返戻金 and the full savings
  machinery** — 保険料の自動振替貸付 (APL), 契約者貸付, 払済保険への変更 — on a cancer product;
  第2条 がんの保障の責任開始期 (day 91); 第4条–第9条 benefit definitions with all amounts
  expressed as multiples of がん入院給付金日額; a **separate, half-rate 上皮内がん診断給付金**;
  a がん死亡保険金 with a reserve floor; 第12条 premium waiver; 第17条 grace; 第19条 APL at
  ≤8% p.a.; 第21条 three-year reinstatement window.

### S7 — アフラック, 「生きるためのがん保険Days1プラス 契約概要」 (contract summary)
- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan)
- Document: 生きるためのがん保険Days1プラス 契約概要, file `days1plus_27604700.pdf`, 24 pp.
  Formal product name 「がん保険〔無解約払戻金2018契約者用〕」.
- Doc type: 契約概要
- URL: https://www.aflac.co.jp/keiyakugaiyou/pdf/days1plus_27604700.pdf
- Accessed: 2026-08-20. Retrieved: YES (24 pp.; benefit tables extracted and read)
- Key content: the most granular published benefit-limit table in this session — 上皮内新生物
  at **10%** of the cancer rate; 複数回診断給付金 on a 2-year cycle with no lifetime cap;
  手術治療給付金 limited to once per 14 days per 一連の手術; 放射線治療給付金 once per 60 days;
  抗がん剤・ホルモン剤治療給付金 paid monthly with a **combined 120× lifetime cap** across
  renewals; 通院給付金 with no day limit and no lifetime limit; 緩和療養給付金 capped at 24
  months; 特定保険外診療給付金 capped at 12 payments; がん先進医療・患者申出療養 capped at
  ¥20,000,000; 10-year term with automatic renewal.

### S8 — アフラック, 「生きるためのがん保険Days1プラス ご契約のしおり・約款」
- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款, file `days1_77945100.pdf`, 212 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.aflac.co.jp/yakkan/pdf/days1_77945100.pdf
- Accessed: 2026-08-20. Retrieved: YES (212 pp.; text extracted, しおり sections read)
- Key content: 責任開始日 defined as **three calendar months** after application/告知 completion
  (not "90 days"); the pre-責任開始日 diagnosis invalidity rule; first-premium 払込期月 and
  grace; second-and-later grace by payment mode; one-year reinstatement window; 契約年齢
  definition (age last birthday, incremented on the policy anniversary).

### S9 — アフラック, 「生きるためのがん保険Days1 契約概要」
- Publisher: アフラック生命保険株式会社
- Document: 生きるためのがん保険Days1 契約概要, file `days1_27545300.pdf`, 20 pp.
- Doc type: 契約概要
- URL: https://www.aflac.co.jp/keiyakugaiyou/pdf/days1_27545300.pdf
- Accessed: 2026-08-20. Retrieved: **NO** — the file downloaded (20 pp., 9.9 MB) but is
  image-only: `pypdf` extracted 19 characters of text in total. No OCR was attempted. This is
  the *base* Days1 product, which (unlike Days1プラス [S7]) carries a がん入院給付金; that
  benefit's daily amount and limits are therefore **not** sourced here.

### S10 — チューリッヒ生命, 「終身ガン治療保険プレミアム／３大疾病保険プレミアム ご契約のしおり・約款」
- Publisher: チューリッヒ生命保険株式会社 (Zurich Life Insurance Company Ltd, Japan branch
  business)
- Document: ご契約のしおり・約款 WC143, 2015年7月改訂 (終身払・短期払), 156 pp. Formal main
  contract name 「無解約払戻金型終身ガン治療保険（抗がん剤等保障）」.
- Doc type: ご契約のしおり・約款
- URL: https://www.zurichlife.co.jp/faq/others/clause/-/media/Files/ZurichLife/faq/clause/kikeiyaku/gan/WC143.ashx?la=ja-JP
- Accessed: 2026-08-20. Retrieved: YES (156 pp.; しおり and 特約条項 extracted and read)
- Key content: the **treatment-benefit-only chassis** — the main contract pays only
  放射線治療給付金 and 抗がん剤・ホルモン剤治療給付金, each a 給付月額 paid per calendar month,
  for life, with hospitalisation/surgery/diagnosis/outpatient all pushed out into 特約;
  90-day 不てん補期間 (cover from day 91); ガン診断給付金 on a 2-year cycle where the *second and
  later* payments additionally require a hospitalisation; ガン通院給付金 with a 60-day
  pre-admission look-back and a 365-day post-discharge window capped at 120 days;
  悪性新生物保険料払込免除特約 that excludes 上皮内新生物; premium-paying options
  55/60/65/70歳払済 or 終身払; 無解約払戻金型.

### S11 — ライフネット生命, 「終身がん保険（無配当・無解約返戻金型） ご契約のしおり・約款」
- Publisher: ライフネット生命保険株式会社 (LIFENET INSURANCE COMPANY)
- Document: ご契約のしおり・約款, file `LIFENET_yakkan_gan_latest.pdf`, 60 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_gan_latest.pdf
- Accessed: 2026-08-20. Retrieved: YES (60 pp.; text extracted and read)
- Key content: 責任開始日 = three months after the application; **no premium is charged during
  those three months**; がん診断一時金 once over the whole policy term; 上皮内新生物診断一時金 at
  **50%**, also once; 治療サポート給付金 of ¥100,000 per treatment month (¥50,000 for a
  hormone-therapy-only month, capped at 60 months); がん収入サポート給付金 paid annually on the
  anniversary for up to 5 payments; がん先進医療給付金 capped at ¥20,000,000; a **two-month**
  grace period; **no reinstatement at all**; no surrender value, no maturity value, no dividend;
  monthly premiums only; and A-type contracts that *terminate* on payment of the diagnosis
  lump sum versus C/D-type contracts that instead waive future premiums.

### S12 — ライフネット生命, 終身がん保険 商品ページ (product page)
- Publisher: ライフネット生命保険株式会社
- Doc type: product page (consumer/direct)
- URL: https://www.lifenet-seimei.co.jp/product/cancer/whole-life-cancer/
- Accessed: 2026-08-20. Retrieved: YES
- Key content: 診断一時金 selectable ¥1,000,000–¥3,000,000 in ¥500,000 steps (¥500,000 also
  available from age 66); 加入年齢 18–80; 保険料払込期間 終身; monthly premiums only; the
  course structure (ライトコース / あんしんコース / あんしんプラスコース).

### S13 — セコム損害保険, 「自由診療保険メディコム 補償内容」 (product page)
- Publisher: セコム損害保険株式会社 (SECOM General Insurance)
- Doc type: product page (consumer)
- URL: https://www.secom.co.jp/medcom/compensation/
- Accessed: 2026-08-20. Retrieved: YES
- Key content: the **自由診療 expense-reimbursement variant**, written by a non-life insurer —
  cancer treatment cost is indemnified at actual cost rather than on a fixed schedule;
  ガン入院保険金 unlimited; ガン外来保険金 capped at ¥20,000,000 which **resets at each 5-year
  renewal**; ガン診断保険金 ¥1,000,000 payable repeatedly subject to a **3-year** cycle;
  上皮内新生物 covered on the same footing as invasive cancer; 90-day waiting period with cover
  from day 91; 5-year policy term automatically renewing to age 90.

### S14 — セコム損害保険, 「新ガン治療費用保険」 パンフレット (brochure)
- Publisher: セコム損害保険株式会社
- Document: ガン保険 新ガン治療費用保険, 2009年5月1日以降保険始期用, file `MEDCOM_BP1030.pdf`,
  5 pp., print code SEK-1101-0902-0008 / BP1030.
- Doc type: 商品パンフレット
- URL: https://www.secom-sonpo.co.jp/pdfbox/MEDCOM_BP1030.pdf
- Accessed: 2026-08-20. Retrieved: **NO (partial)** — the file downloaded (5 pp.) and `pypdf`
  emitted a warning ("Advanced encoding /83pv-RKSJ-H not implemented yet"); the extracted text
  is unreadable Latin-1 mojibake. Only the document's identity, date and print code are
  reported from it. Its formal product name 「新ガン治療費用保険」 corroborates that メディコム
  is the pet name of an expense-cover product, but nothing quantitative was taken from it.

### S15 — 保険市場 (アドバンスクリエイト), がん保険Believe 商品ページ (distributor listing)
- Publisher: 株式会社アドバンスクリエイト (operator of 保険市場) — a **distributor**, not the
  carrier. Treated as a secondary source: used only for the issue-age and premium-term
  envelope, which the carrier's own retrieved documents state only in the non-extractable
  pamphlet [S4].
- Doc type: comparison-site product listing
- URL: https://www.hokende.com/life-insurance/cancer/whole_cancer/item-or15
- Accessed: 2026-08-20. Retrieved: YES
- Key content: 契約可能年齢 0 (from 15 days old at 告知) to 75; 保険期間 終身; 保険料払込期間
  60歳／65歳/終身 for direct sales; the ¥5,000 基本給付金額 course restricted to ages 50–75.

---

## Regulatory and actuarial references

### R1 — 日本アクチュアリー会, 「標準生命表2018」 (standard mortality tables)
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — a title page and **four** tables: 生保標準生命表2018
  （死亡保険用）男/女, to terminal ages 109 and 113, **and 第三分野標準生命表２０１８（男）（女）**,
  to terminal ages 116 and 118 — each a full `x / l_x / d_x / q_x / e_x` table. The file
  contains no 年金開始後用 pair (text correction, 2026-08-20; ids unchanged).
- Doc type: standard table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (5 pp., full numeric tables extracted; spot-checked
  values recorded below)
- Content: the tables are published in full and are freely downloadable — the sharpest contrast
  with `uklib`, where the CMI tables are subscriber-restricted. Effective for contracts written
  from April 2018 [R2].

### R2 — 日本アクチュアリー会, 「標準生命表2018の作成概要」 (construction memorandum)
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料①–⑤; 資料④ is 第三分野標準生命表2018)
- Doc type: technical memorandum
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (6 pp., extracted and read)
- Content: 第三分野標準生命表2018 is built on the **国民表** (第21回生命表, 2010) rather than on
  insured-lives experience — a deliberate change from the 2007 edition, made because
  third-sector business had shifted from riders on death cover to stand-alone main contracts
  with different underwriting; mortality improvement of 2.5% p.a. for 5 years then 1.0% p.a. for
  3 years is projected forward to the table's effective year; a 数学的危険論 margin is added to
  hold the probability of adverse deviation to about **2.28% (2σ)** on an assumed 1,000,000
  policies per sex, with the adjusted rate floored at 70% and capped at 85% of the
  pre-adjustment rate. It is a **mortality** table carrying explicit safety margins: it is not,
  and does not contain, a morbidity or cancer-incidence basis.

### R3 — 金融庁, 「第三分野の責任準備金積立ルール・事後検証等の概要について」 (別紙１−２)
- Publisher: 金融庁 (Financial Services Agency)
- Document: 別紙１−２, 8 pp., published 2006-02-10 as part of the FSA's third-sector reserving
  package
- Doc type: 金融庁 policy paper
- URL: https://www.fsa.go.jp/news/newsj/17/hoken/f-20060210-1/01_2.pdf
- Accessed: 2026-08-20. Retrieved: YES (8 pp., extracted and read)
- Content: the load-bearing regulatory statement for this product. 第三分野 is defined as
  covering 医療保険, がん保険 and 介護保険. Because third-sector products are highly varied and
  lack accumulated data, **no standard incidence rate and no reference pure premium exist**;
  insurers must set each benefit's incidence rate from public data and their own experience.
  The framework therefore requires (i) 事後検証 of the assumed incidence rates each year,
  (ii) a **ストレステスト** performed every reporting period over a **10-year test horizon**,
  comparing future benefit outgo on the pricing incidence rate `P` against outgo on 危険発生率A
  (covering **99%** of incidence risk) and 危険発生率B (covering **97.7%**), with 危険準備金 set
  up when `P` falls short, and (iii) a **負債十分性テスト**; plus disclosure and off-site
  monitoring. It also records that at 平成16年度 third-sector business exceeded ¥3.5 trillion of
  annualised premium and more than 20% of life insurers' in-force.

### R4 — 金融庁, 「保険会社向けの総合的な監督指針」 II−２ 財務の健全性
- Publisher: 金融庁
- Doc type: 監督指針 (supervisory guideline)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES
- Content: II−２−１−２ (積立方式) and II−２−１−４ (経理処理) carry the third-sector
  reserving checkpoints, citing 平成８年２月29日大蔵省告示第48号 (the 標準責任準備金 notification)
  and 平成10年６月８日大蔵省告示第231号, and requiring that the ストレステスト and 負債十分性テスト
  適切に consider the uncertainty of deteriorating incidence rates and be run, in principle,
  separately for each 契約区分 sharing a common 基礎率. Multiple references to 保険業法施行規則
  第69条 (第５項, 第７項). **Caveat**: the retrieved page did not restate the 99%/97.7% figures
  — those come from [R3].

### R5 — 国立がん研究センター, 「がん統計 集計表ダウンロード」 — 全国がん登録罹患数・率 2016–2023
- Publisher: 国立研究開発法人 国立がん研究センター がん対策研究所 (National Cancer Center Japan),
  from data provided under 「がん登録等の推進に関する法律」
- Document: 全国がん登録に基づく全国がん罹患数・率 2016年-2023年,
  `cancer_incidenceNCR(2016-2023).xls`, ~1.16 MB; sheets `number` (counts by 5-year age band,
  site, sex, diagnosis year), `rate` (rates per 100,000), `asr` (age-standardised),
  `detail`, `pop` (populations)
- Doc type: public statistical table (downloadable Excel)
- URL: https://ganjoho.jp/reg_stat/statistics/data/dl/excel/cancer_incidenceNCR(2016-2023).xls
  (index page: https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)
- Accessed: 2026-08-20. Retrieved: YES (file downloaded and parsed with pandas; sheet names,
  headers and 2023 rows read directly)
- Content: **this is the citable public incidence basis that lets the model ship a sourced
  rather than an invented decrement.** Counts and rates are published by 5-year age band
  (0–4 … 95–99, 100歳以上) × sex × site × diagnosis year 2016–2023, and — crucially for a cancer
  product — the site list carries paired rows **with and without 上皮内がん** (e.g. 全部位
  C00–C96 versus 全部位（上皮内がん含む） C00–C96 D00–D09).

### R6 — 国立がん研究センター, 全国がん登録に基づく5年相対生存率 (2016–2018 diagnoses)
- Publisher: 国立研究開発法人 国立がん研究センター
- Document: 日本の全国がん登録に基づく部位別5年相対生存率,
  `cancer_survivalNCR(2016-2018).xlsx`, ~64 KB; sheets 最新データ（部位）, 最新データ（進行度別）,
  推移データ（部位）, 推移データ（進行度別）, 推移データ（進行度の割合）
- Doc type: public statistical table (downloadable Excel)
- URL: https://ganjoho.jp/reg_stat/statistics/data/dl/excel/cancer_survivalNCR(2016-2018).xlsx
- Accessed: 2026-08-20. Retrieved: YES (file downloaded and parsed)
- Content: 5-year relative survival by site and sex, and by 臨床進行度 (limited / regional /
  distant), with 対象者数 and 標準誤差 on every cell. This is the reference that turns a cancer
  diagnosis into a post-diagnosis survival curve — needed for any repeating diagnosis benefit,
  any income-style benefit, and for the mortality of the diagnosed sub-population.

### R7 — 厚生労働省, 「令和５年（2023）患者調査の概況」
- Publisher: 厚生労働省 (Ministry of Health, Labour and Welfare)
- Document: 令和５年（2023）患者調査の概況, 33 pp.
- Doc type: national statistical survey summary
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/kanjya.pdf
  (index: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/index.html)
- Accessed: 2026-08-20. Retrieved: YES (33 pp., extracted; 推計患者数 and 平均在院日数 tables read)
- Content: the public basis for cancer inpatient days. 推計患者数 as at 2023-10 and
  退院患者平均在院日数 for discharges during 2023-09, both broken down by 傷病分類 and by age band.
  Full detail tables sit on e-Stat under 統計表 Z124-x / Z134 (not separately fetched).

### R8 — 国税庁, タックスアンサー No.1141 「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁 (National Tax Agency)
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the three post-2012 baskets — 生命保険契約等 / **介護医療保険契約等** / 個人年金保険契約等.
  介護医療保険料控除 applies to contracts concluded on or after 2012-01-01 under which benefits
  are paid on 疾病 or 身体の傷害 and specifically 医療費支払事由. Excluded: savings contracts of
  term under 5 years, foreign contracts, credit insurance, 傷害保険, 財形貯蓄.

### R9 — 国税庁, タックスアンサー No.1140 「生命保険料控除」
- Publisher: 国税庁
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the 新制度 (contracts from 2012-01-01) deduction schedule and caps, and the 旧制度
  schedule and caps. Figures reproduced below.

### R10 — 生命保険文化センター, 「2025（令和７）年度 生活保障に関する調査《速報版》」
- Publisher: 公益財団法人 生命保険文化センター (Japan Institute of Life Insurance)
- Document: 2025（令和７）年度 生活保障に関する調査 速報版, 2025年10月, 128 pp.
- Doc type: national household survey
- URL: https://www.jili.or.jp/files/research/chousa/pdf/r7/seikatuhoshouchousa_2025sokuhouban.pdf
- Accessed: 2026-08-20. Retrieved: YES (128 pp., extracted; 図表 II-19 read)
- Content: cancer-cover penetration among households, 図表 II-19, N = 4,837.

### R11 — 生命保険文化センター, 「がん保険」 (product-type explainer)
- Publisher: 公益財団法人 生命保険文化センター
- Doc type: consumer education page (生命保険の種類 → 主契約の種類)
- URL: https://www.jili.or.jp/knows_learns/kind/main/34.html
- Accessed: 2026-08-20. Retrieved: YES
- Content: an independent, non-carrier statement of the product archetype: the benefit menu
  (がん入院給付金, がん手術給付金・がん放射線治療給付金, がん診断給付金, がん死亡給付金, plus
  死亡給付金 for non-cancer death, and outpatient / advanced-medicine / chemotherapy benefits);
  the ~90-day waiting period as the market norm; and the flat statement that the hospitalisation
  benefit has **no day limit**.

---

## Fact extraction

### 1. Product architecture and where it sits

- がん保険 is one of the three 第三分野 (third-sector) lines named by the regulator, alongside
  医療保険 and 介護保険: benefits are paid on 疾病 or 傷害 as 保険金 or 給付金 for treatment [R3].
- Cancer-cover penetration among Japanese households (がん保険・がん特約, all providers including
  JA and 共済) is **39.9%**; through private life insurers alone (民保) it is **35.4%**
  (2025 survey, N = 4,837) [R10]. The series shows no consistent trend over time [R10].
- Third-sector business exceeded **¥3.5 trillion** of annualised premium and **more than 20%** of
  life insurers' in-force by 平成16年度, following the January 2001 full liberalisation that let
  major domestic insurers sell third-sector products stand-alone [R3].
- Two distinct chassis are in the market, and the retrieved documents show both clearly:
  - **Benefit-schedule (定額給付) chassis** — every benefit is a fixed amount or a fixed multiple
    of a base amount. Six of the seven carriers [S1] [S5] [S6] [S7] [S10] [S11].
  - **Expense-reimbursement (実損てん補) chassis** — the actual cancer treatment cost is
    indemnified, including 自由診療 and 先進医療. Written by a non-life insurer [S13].
- Within the 定額給付 chassis there are two further shapes:
  - **Diagnosis-and-hospitalisation centred**: 診断給付金 + 入院給付金(日額) + 手術給付金
    (+ 通院/退院) [S1] [S5] [S6].
  - **Treatment-centred**: the *main contract* pays only 放射線治療給付金 and
    抗がん剤・ホルモン剤治療給付金 as monthly amounts, and hospitalisation, surgery, diagnosis and
    outpatient are all riders [S10]; or a monthly 治療サポート給付金 covering surgery, radiation
    and chemotherapy alike [S11]. This is the direction the market has moved.
- 主契約 + 特約 structure is universal. One carrier's whole benefit menu beyond the two treatment
  benefits sits in nine named 特約 [S10]; another's base contract is just 診断給付金 + 通院給付金
  with eleven riders around it [S7].

### 2. The waiting period (免責期間 / 待ち期間) — the product's defining feature

- Every retrieved cancer contract has one. It is expressed two ways:
  - **90 days from inception, cover from day 91** — 「責任開始日を含めて91日目」 [S1];
    「保険期間の始期からその日を含めて90日を経過した日の翌日を責任開始期とし」 [S5];
    「責任開始期の属する日からその日を含めて90日目の日の翌日」 [S6]; 「保険期間の始期からその日を
    含めて91日目」 [S10]; 「90日の待機期間」 with cover from day 91 [S13]. All four wordings
    denote the same day.
  - **Three calendar months** — 「申込および告知がともに完了した日…から３か月を経過した日の翌日」
    [S8]; 「その日を含めて3ヶ月を経過した日の翌日（応当日がない場合はその月の末日）」 [S11].
- 生命保険文化センター states the market norm as 90 days and that a cancer diagnosed inside the
  window is not covered [R11].
- The waiting period is **not** merely an exclusion — a diagnosis before it ends makes the whole
  contract **void (無効)**, not merely unpayable:
  - 「保険契約・特約は無効とします」, with premiums refunded only if neither policyholder nor
    insured knew of the diagnosis before 告知; retained if either knew [S1].
  - 「保険契約者、被保険者または給付金の受取人の、その事実の知、不知にかかわらず、ご契約は無効と
    します」 [S5]; 第4条 「がん入院給付金は支払いません」 for a pre-責任開始期 diagnosis [S6];
    「ご契約は無効となり、保険金・給付金のお支払いはできません」 [S10].
- One carrier caps the reach of the voidness rule: if no benefit event occurs within **5 years**
  of がん責任開始日, the pre-diagnosis invalidity treatment is not applied [S1].
- Under the three-month formulation one carrier **charges no premium at all** during the waiting
  period, and says explicitly that this is not a discount [S11]. Under the 90-day formulation the
  contract is in force and premiums are payable from inception — non-cancer covers such as the
  premium waiver already run from 責任開始時 [S1] [S5].
- On **reinstatement (復活)** the waiting period restarts: がん責任開始日 becomes the 復活日, except
  that if the 復活日 falls before the original がん責任開始日 the original date stands [S1] [S6].

### 3. What counts as "cancer", and the treatment of 上皮内新生物

- The definition is by 約款別表 keyed to ICD codes, and 診断確定 must be by a Japanese-qualified
  physician or dentist on 病理組織学的所見 (biopsy), with other findings accepted where biopsy is
  not obtainable [S1] [S6] [S10]. One carrier admits equivalently-qualified foreign physicians
  [S11].
- **The date of diagnosis is the date the diagnostic test was performed**, not the date the
  physician told the patient — stated explicitly and twice [S1]. This matters for the waiting
  period and for any repeat-cycle clock.
- 上皮内新生物 (carcinoma in situ) is handled in three different ways, and the split across
  carriers is the single largest source of benefit-level variation:

  | Treatment of 上皮内新生物 | Carriers |
  |---|---|
  | **Full rate** — 上皮内新生物 is inside the definition of がん | [S1] 「悪性新生物（上皮内新生物を含みます。）」; [S5] 「別表5に定める悪性新生物および上皮内新生物」; [S10] 「ガン（悪性新生物・上皮内新生物）」; [S13] |
  | **Half rate** — a separate, half-size in-situ benefit | [S6] 上皮内がん診断給付金 = 指定倍率の1/2; [S11] 上皮内新生物診断一時金 = がん診断一時金の50% |
  | **10%** | [S7] 「上皮内新生物の場合：診断給付金額の10％」 (and the same 10% on the 複数回診断給付金) |

- The half-rate and 10% carriers keep the in-situ benefit **separately capped**: each is payable
  once over the policy term in its own right, and the in-situ benefit is not payable after the
  cancer benefit has already been triggered [S6] [S11].
- Where a carrier grades benefits, it does not grade *all* of them: one grades the diagnosis
  benefit at 10% but pays 手術治療給付金, 放射線治療給付金 and 通院給付金 in full for in-situ,
  while excluding in-situ entirely from 抗がん剤・ホルモン剤治療給付金, 特定保険外診療給付金,
  外見ケア, 緩和療養 and 女性がん特約 [S7]. In-situ is likewise excluded from the premium waiver
  by one carrier [S10] and from the advanced-medicine benefit by another [S11].
- The public incidence table publishes both bases, so a model can source the split rather than
  assume it: 2023 全部位 (C00–C96) **993,469** cases against 全部位（上皮内がん含む）
  (C00–C96, D00–D09) **1,114,642** — an in-situ increment of **121,173**, i.e. **12.2%** of the
  invasive count and **10.9%** of the combined count [R5]. By sex, 2023: male 556,059 → 611,765
  (increment 55,706); female 437,406 → 502,872 (increment 65,466) [R5].

### 4. 診断給付金 / 診断一時金 — amount, repeat cycle, and what restarts it

- Amount, where published:
  - ¥1,000,000 at the ¥10,000 基本給付金額 course; the schedule is **100 × 基本給付金額** [S2]
    [S3].
  - Selectable ¥1,000,000–¥3,000,000 in ¥500,000 steps, with ¥500,000 additionally available
    from age 66 [S12].
  - ¥1,000,000 flat on the expense product [S13].
  - Expressed as がん入院給付金日額 × a 給付倍率 chosen by the policyholder from a range the
    insurer sets, with the in-situ version at half that 倍率 [S6].
  - ¥2,000,000 in the published 契約例 [S5].
- Repeat cycle — this is where carriers diverge most sharply:

  | Carrier | First payment | Repeat |
  |---|---|---|
  | [S1] | がん初回診断一時金, **once over the whole policy term** | none; repetition is carried instead by がん治療給付金 (below) |
  | [S5] | on first diagnosis | again on 再発 / 転移 / 新たに生じた cancer, **only if ≥ 2 years since the previous payment trigger** |
  | [S6] | がん診断給付金, **once over the policy term**; 上皮内がん診断給付金, once | none |
  | [S7] | 診断給付金, **once**; 上皮内新生物 separately once | via 診断給付金複数回支払特約: **every 2 years**, no lifetime cap, but the 2nd-and-later payments additionally require being *under treatment* (inpatient or 所定の通院) |
  | [S10] | on first diagnosis | **every 2 years**, and the 2nd-and-later payments require a **hospitalisation** for cancer treatment |
  | [S11] | once over the policy term | none (the repeating element is 治療サポート給付金 and がん収入サポート給付金) |
  | [S13] | ¥1,000,000 | **every 3 years**, unlimited number of times |

- **No retrieved document contains a 1年に1回 cancer diagnosis benefit.** The nearest is one
  carrier's 重大疾病一時金特約 (heart/stroke, not cancer), which is 1年に1回 with no lifetime cap
  [S7], and one carrier's がん収入サポート給付金, which is annual but is an *income* benefit paid
  on survival, not a re-diagnosis benefit [S11]. A 1-year diagnosis cycle is therefore
  [unverified] in this session — see Fetch failures and gaps.
- The 2-year clock is measured from a defined event and the definition differs: from the date
  the previous payment trigger occurred [S5]; from the **first day of the month** in which the
  previous payment was made [S7]; from the **start date of the last hospitalisation** for which
  the benefit was paid [S10]. A model that treats these as identical is wrong.
- One carrier converts a continuing hospitalisation into a fresh event: if the insured is still
  in hospital on the day after the 2-year period expires, that is **deemed** a new benefit
  trigger [S1].
- On the once-only structures, payment of the diagnosis lump sum can **terminate the contract**
  (A-type) or instead **waive all future premiums** (C/D-type) [S11]. On another once-only
  contract the policy continues and the other benefits stay live [S1].

### 5. がん入院給付金 — the no-day-limit contrast with 医療保険

- 「がん入院給付金は給付日数無制限です」 [S1]; 「支払日数に制限はありません」 [S3];
  「入院給付金日額 × 入院日数」 with a 支払日数 limit stated for every *other* benefit in the same
  table and none for this one [S5]; 「がん入院給付金日額 / がんの治療を直接の目的とする入院日数」
  with no cap in the article [S6]; 「ガン入院給付日額 × 入院日数」 with no cap [S10];
  「入院給付金の支払日数は無制限です」 stated as the product-type norm [R11]; unlimited on the
  expense product [S13].
- This is the structural contrast with 医療保険, where the same daily-benefit machinery carries a
  支払限度日数 per hospitalisation (typically 60 or 120 days) and a 通算 lifetime limit.
- Two carriers count *adjacent* non-cancer inpatient days into the cancer benefit where the
  insurer accepts that the stay was for cancer treatment: days after a non-cancer illness began
  during a covered cancer stay, and days before the diagnosis date during a stay begun for
  another reason [S6].
- Where the contract is one of the newer treatment-centred designs there is **no** 入院給付金 in
  the main contract at all — it is a rider [S10], or absent from the product entirely [S7].

### 6. 手術給付金, 放射線治療給付金, 抗がん剤治療給付金 — the treatment benefits

- **手術給付金**
  - **20 × 基本給付金額**, unlimited number of payments [S2]; ≥2 simultaneous procedures count as
    one [S1].
  - **がん入院給付金日額 × 20**, ≥2 simultaneous procedures count as one [S6].
  - 手術給付金額, unlimited number of payments, **but certain procedures (e.g. fibrescopic
    malignant-neoplasm surgery) are limited to one payment per 60 days**; some procedures are
    outside cover altogether [S5].
  - 手術治療給付金 at 特約給付金額, limited to **once per 14 days** for a 一連の手術, unlimited in
    total [S7].
  - ガン手術給付金額 per surgery; simultaneous procedures count as one; where the medical fee
    schedule scores a repeated identical procedure only once, only one payment is made [S10].
- **放射線治療給付金**
  - 特約給付金額 per treatment, limited to **once per 60 days**, unlimited in total [S7].
  - Paid at the 給付月額 as part of the main contract, per calendar month; two identical
    treatments scored once in the fee schedule pay once; two triggers on the same day pay once
    [S10].
  - Folded into a single monthly 治療サポート給付金 alongside surgery and chemotherapy [S11].
- **抗がん剤治療給付金 / ホルモン剤治療給付金**
  - 治療給付金額 **per month in which the trigger occurs**, with a lifetime cap of **60 months**
    across the rider's term [S5].
  - 特約給付金額 × 給付倍率 per qualifying month, 倍率 = **1** for hormone therapy in breast or
    prostate cancer and **2** otherwise, with a **combined lifetime cap of 120×** across
    chemotherapy and hormone therapy, counted across renewals [S7].
  - 給付月額 per qualifying month; a prescription covering two months still pays one month; two
    triggers in one month pay once; two triggers on one day pay once [S10].
  - ¥100,000 per treatment month, or **¥50,000** for a month in which only hormone therapy was
    received, the hormone-only months capped at **60 months** over the policy term; a month with
    several treatments still pays once [S11].
- The definition of qualifying chemotherapy is anchored to public classifications, not to a
  clinical list: 「総務大臣が定める日本標準商品分類における『8742 腫瘍用薬』」, oral
  administration excluded [S1]; drugs for which a 薬剤料 or 処方せん料 is scored under the
  医科診療報酬点数表 or 歯科診療報酬点数表 [S5] [S10]. Every such contract carries a clause
  letting the insurer change the payment triggers, with 主務官庁 approval, if the public
  medical insurance scheme changes — with two months' notice to policyholders [S5] [S1].

### 7. がん通院給付金 (outpatient)

- Two structurally different designs coexist, and one carrier runs both at once:
  - **Treatment-linked, no day limit** — outpatient attendance for surgery, radiation, thermal
    therapy or non-oral chemotherapy, with 「給付の日数の限度はありません」 [S1]; 支払日数は無制限
    for 所定の治療 and no 通算 limit at all [S7].
  - **Hospitalisation-linked, day-limited** — attendance within a window around an inpatient
    stay: 60 days before admission and 180 days after discharge, capped at **45 days per
    hospitalisation** and **730 days lifetime** [S5]; 60 days before admission and 365 days after
    discharge, capped at **120 days per post-discharge period** [S10]; within a 通院治療期間 of
    one year from discharge, capped at **60 days per 通院治療期間** [S1] [S2]; a 通院期間 of 365
    days from a defined start date, unlimited days within it [S7].
- Where a carrier runs both, the tie-break is specified: a day qualifying under both is paid as
  the hospitalisation-linked one until that limit is exhausted, then as the treatment-linked one
  [S1].
- Outpatient attendance during a stay for which the inpatient benefit is paid is not payable
  [S10]; and one carrier will not pay 入院 and 通院 on the same day [S7].

### 8. Other benefits found

- **がん退院一時金** — 10 × 基本給付金額 on discharge from a covered stay of **≥ 10 consecutive
  days**, unlimited number of payments, but not payable for a stay that began **within 30 days**
  of a discharge for which the benefit was already paid; if the discharge is by death the
  policyholder becomes the payee [S1] [S2].
- **がん死亡保険金 / がん高度障害保険金** — がん入院給付金日額 × a chosen 倍率, with the payment
  **floored at the policy reserve** at the date of death if that is larger [S6]. Most cancer
  contracts have no death benefit at all: 「この保険に死亡保険金はありません」 [S1].
- **先進医療 (advanced medicine)** — the technique fee reimbursed in full, capped at a lifetime
  **¥20,000,000** [S1] [S7] [S11], or **¥10,000,000** on the older contract [S5]. A companion
  lump sum is common: **10%** of the advanced-medicine benefit capped at **¥500,000 per
  療養** [S1]; **¥150,000 per 療養, once per policy year** [S7]. Reaching the ¥20m cap
  extinguishes the rider [S1]. One carrier explicitly excludes 患者申出療養 from the benefit
  [S11] while another explicitly includes it [S7].
- **特定保険外診療給付金 (non-scheduled treatment)** — paid per qualifying month for surgery,
  radiation or chemotherapy delivered at a がん診療連携拠点病院等 by a procedure *not* listed in
  the public fee schedule, excluding 先進医療, 患者申出療養 and approved anti-cancer drugs;
  once per month, **12 payments lifetime** across renewals [S7]. This is the 定額給付 chassis's
  answer to 自由診療.
- **がんゲノムプロファイリング検査給付金** — ¥100,000 per qualifying month, once per month [S7].
- **外見ケア給付金** — ¥200,000 for facial/head tumour excision or digit amputation, ¥100,000 on
  a physician-diagnosed hair loss caused by cancer treatment, each once across renewals [S7].
- **緩和療養給付金** — 特約給付金額 per qualifying month for pain-relief drugs, a 緩和ケア病棟 stay
  or qualifying home care, once per month, **24 months** lifetime [S7]; a Zurich equivalent
  capped at **12 months** [S10].
- **女性がん特約 / 女性手術給付金** — ¥200,000 per procedure for breast excision, hysterectomy or
  oophorectomy and ¥500,000 for reconstruction, each once per breast/ovary [S7]; ¥100,000 per
  procedure with the same per-organ counting [S11].
- **がん収入サポート給付金** — 50% of the diagnosis lump sum, paid on each policy anniversary
  after the diagnosis year while the insured is alive, up to **5 payments**; stops on death
  [S11]. This is the closest thing in the market to an income-style cancer benefit.
- **がん要精検後精密検査給付金** — paid on a "further investigation required" result from a
  screening for stomach, cervical, lung, breast or colorectal cancer [S7].

### 9. 自由診療 (non-reimbursed medicine) variants

- The expense-reimbursement product indemnifies the **actual cost** of cancer treatment,
  inpatient or outpatient, whether the treatment is 保険診療, 先進医療 or **自由診療**, and
  includes the cost of diagnostic documentation [S13].
- Structure: ガン入院保険金 **unlimited**; ガン外来保険金 capped at **¥20,000,000**, the cap
  **resetting at each 5-year renewal**; ガン診断保険金 ¥1,000,000 on a 3-year cycle; 5-year
  policy term auto-renewing to age 90; 90-day waiting period [S13].
- On the 定額給付 side, the analogue is the 特定保険外診療給付金 described above [S7], and the
  named 自由診療抗がん剤治療給付金 offered by at least one carrier — the latter appears only in a
  search-result snippet and is [unverified]; the retrieved 2015 edition of that carrier's
  booklet [S10] does **not** contain a 自由診療 benefit.

### 10. 保険料払込免除 (premium waiver)

- Three distinct triggers are in the market:
  - **Disability-only, cancer excluded** — waiver on 高度障害状態 from any 傷害 or 疾病 arising
    after 責任開始時, or on a 身体障害の状態 arising within **180 days** of an 不慮の事故;
    explicitly **not** waived where the 高度障害状態 is caused by a cancer diagnosed before
    がん責任開始日 [S1]. The same two triggers, with the disease limb restricted to
    「がん以外の疾病」 and both conditioned on falling within the premium-paying period [S6].
    Same two triggers again [S5].
  - **Cancer-diagnosis waiver as a rider** — 悪性新生物保険料払込免除特約, on diagnosis of
    悪性新生物 only; **上皮内新生物 does not trigger it**, and a pre-責任開始期 diagnosis does not
    either [S10].
  - **Cancer-diagnosis waiver built into the contract** — from the moment the がん診断一時金
    trigger occurs, on C/D-type contracts (not on the ライトコース A-type, which instead
    terminates) [S11].
- Underwriting can carve the waiver out by named impairment: 特定障害不担保特約 excluding
  designated 視力障害 or 聴力障害 from waiver eligibility [S1].
- The 契約概要 of one carrier's product lists **no** premium-waiver benefit of any kind [S7] —
  recorded as an observed absence for that product, not a general claim.

### 11. Premiums, payment modes, grace, lapse, reinstatement

- **Modes**: 年払 / 半年払 / 月払 via 口座振替 or クレジットカード [S1] [S6]; **月払のみ** on one
  direct writer [S11] [S12].
- **Published premium example** (the only one retrieved): 30-year-old male, 診断給付金額
  ¥2,000,000, 入院給付金日額 ¥20,000, 10-year term and premium term, monthly by direct debit —
  **¥1,456 per month**; at the first renewal at age 40 the renewed premium is **¥2,082**,
  calculated on rates as at the 計算基準日 2013-10-22 and subject to change [S5].
- **Grace (猶予期間)**
  - Monthly: from the 1st to the last day of the month following the 払込期月 [S1] [S6] [S8].
  - Annual / semi-annual: from the 1st of the following month to the monthly contract
    anniversary in the month after that; where that day does not exist, the last day of that
    month; and where the anniversary is the last day of February, June or November, extended to
    the last day of April, August or January respectively [S1] [S6].
  - One direct writer runs a **two-month** monthly grace — 「払込期月の翌月初日から翌々月末日まで」
    [S11], as against the one-month norm.
  - First-premium grace is separately defined: 払込期間 from 責任開始日 to the end of the
    following month, then grace from the 1st of the month after that to the end of the month
    after that; failure makes the contract **void**, not lapsed [S1] [S8].
- **Effect of a claim inside the grace period**: unpaid premium is deducted from the benefit;
  for a monthly contract where the event falls on or after the contract anniversary inside the
  grace period, **two months'** premium is deducted or must be paid [S1]; if the benefit is too
  small to cover the arrears the contract lapses at the end of the grace period [S6].
- **自動振替貸付 (automatic premium loan)** — present on the one contract that has a surrender
  value: the insurer automatically lends the premium against the surrender value without any
  request, at an insurer-set rate of **≤ 8% p.a.** compounded into principal on each policy
  anniversary, and keeps doing so until the loan principal plus interest would exceed the
  surrender value; one month's notice is then given before the 失効予定日 [S6]. The APL can be
  **retrospectively cancelled** if the policyholder requests surrender or 払済 within 3 months of
  the grace expiry [S6]. On the 無解約払戻金 contracts APL cannot operate at all, because there is
  no surrender value to lend against [S1] [S7] [S10] [S11].
- **復活 (reinstatement)** — three different regimes:
  - **1 year** from lapse, subject to fresh 告知 and health [S1] [S8]. One carrier additionally
    refuses reinstatement outright once any cancer benefit has been paid, and refuses it after a
    surrender request [S1].
  - **3 years** from lapse, with 延滞保険料 payable and no new policy document issued [S6].
  - **None** — 「失効した保険契約を元の状態に戻すこと（復活）はできません」 [S11].
- **告知義務違反 (misstatement)** — the contract may be rescinded within **2 years** of
  責任開始日 / 復活日 / 特約中途付加日 [S1] [S6]. Fraud and unlawful-benefit-purpose voidness are
  **not** time-barred and can bite after the 2-year window closes [S1].
- **クーリング・オフ** — 15 days from the application date, by post or through the insurer's web
  site, with a full refund and no interest [S1]; 8 days on another carrier [S11].

### 12. Surrender values, 無解約払戻金型 and the low-surrender design

- **No surrender value at all** — 無解約払戻金型 / 無解約払戻金 contracts [S7] [S10] [S11], and
  the riders on every contract examined [S1] [S5].
- **Suppressed during the premium-paying period, then a fixed step** —
  - 終身払: no surrender value ever. Short-pay: no surrender value during the premium-paying
    period; after it ends and once all premiums are paid, **10 × 基本給付金額** [S1]. Because the
    product also pays no death benefit, the same 10× amount is what is returned on death after
    the premium term [S1].
  - No surrender value during the premium-paying period; afterwards the **lesser of** (i) 30% of
    the surrender value that would apply without the suppression and (ii) the **greater of**
    入院給付金日額 × 10 and 診断給付金額 ÷ 10 [S5].
- **Conventional surrender value throughout** — computed from months of premium paid and months
  elapsed, supporting 契約者貸付, 自動振替貸付 and **払済保険への変更** (converted to a paid-up
  contract whose がん入院給付金日額 is set from the surrender value, capped at the pre-conversion
  日額, any excess surrender value being paid out) [S6].
- Consequence for modelling: the lapse decrement on a 無解約払戻金 cancer contract has **no
  cash-value offset** at all — a lapse is a pure release of future premium and future benefit,
  and there is no APL to delay it. On the one contract with a surrender value, the APL will carry
  the policy through a missed premium and a model that lapses it immediately is wrong.

### 13. Issue ages, terms, renewal

- **Whole-life (終身) shapes**: 保険期間 終身; 保険料払込期間 60歳／65歳払済 or 終身払 [S15],
  issue ages **0 (from 15 days old at 告知) to 75** [S15], with the ¥5,000 基本給付金額 course
  restricted to ages 50–75 [S15]. 保険料払込期間 55/60/65/70歳払済 or 終身払 [S10]. 加入年齢
  **18–80**, 保険料払込期間 終身 only [S12].
- **Term (有期) renewable shapes**: a 10-year term automatically renewing, the renewed contract
  taking the same term and the 約款 in force at renewal, benefit-payment and premium-waiver
  history and 責任開始期 treated as continuous across the renewal; renewal blocked where the
  premium term is shorter than the policy term; and on request made at least **2 months** before
  maturity the renewed contract can be made **終身** (premium term also 終身) [S5]. A 10-year
  term with automatic renewal on the supplement product [S7]. A **5-year** term auto-renewing to
  age 90 on the expense product [S13].
- **契約年齢** is age last birthday at the contract date, incremented on each policy anniversary:
  「24歳7か月の被保険者の契約年齢は24歳」 [S8].
- **Benefit-amount reduction (減額)** is available where premiums become unaffordable, subject to
  a minimum the insurer sets; increases require a new contract with fresh underwriting [S1]
  [S12]. Where the daily amount is reduced mid-stay, the benefit is computed at the amount in
  force **on each day** [S6].

### 14. Public incidence, survival and hospitalisation data

- **Incidence** [R5], 全国がん登録, diagnosis year 2023, all sites C00–C96:
  - Cases: total **993,469**; male **556,059**; female **437,406**.
  - Crude rate per 100,000: total **798.92**; male **919.23**; female **684.96**.
  - Age-specific crude rates per 100,000, total sexes, 2023 (5-year bands): 0–4 19.23,
    5–9 9.86, 10–14 12.24, 15–19 16.51, 20–24 24.38, 25–29 40.14, 30–34 75.77, 35–39 132.21,
    40–44 220.28, 45–49 340.48, 50–54 453.38, 55–59 641.76, 60–64 959.00, 65–69 1,406.59,
    70–74 1,948.71, 75–79 2,306.96, 80–84 2,459.27, 85–89 2,497.39, 90–94 2,360.63,
    95–99 2,275.13, 100+ 1,889.77.
  - The male and female age curves cross: female incidence exceeds male from about age 25 to
    about age 55 (e.g. 35–39: female 193.89 vs male 72.92), after which male incidence rises far
    above female (e.g. 70–74: male 2,684.60 vs female 1,291.07) [R5]. A unisex cancer basis is
    therefore materially wrong at every age.
  - The file also carries `asr` (age-standardised on 世界人口, 昭和60年 and 平成27年 model
    populations), `detail` and `pop` sheets, and prefecture-level equivalents [R5].
- **In-situ split** [R5], 2023, as in §3 above: +121,173 cases (12.2% of the invasive count) when
  D00–D09 is included. Paired with/without-in-situ rows exist for 食道, 結腸, 直腸, 大腸, 肺,
  皮膚, 乳房, 子宮, 子宮頸部, 膀胱 and 全部位 [R5].
- **Survival** [R6], 全国がん登録, 2018 diagnoses, 5-year relative survival, all sites:
  male **63.17%** (n = 487,577, s.e. 0.087); female **66.84%** (n = 385,168, s.e. 0.088).
  Selected sites (male / female): 胃 67.54 / 63.20; 大腸 70.99 / 68.44; 肝及び肝内胆管
  36.51 / 32.42; 食道 48.29 / 50.76; 口腔・咽頭 62.34 / 67.12 [R6]. The 進行度別 sheet gives the
  same by 限局 / 領域 stage: all sites 限局 **91.16%** (male) and 領域 **62.21%** [R6].
- **Hospitalisation** [R7], 患者調査 令和5年:
  - 推計患者数 as at 2023-10 (thousands): 悪性新生物 inpatient **106.1** (of which 病院 105.2,
    一般診療所 0.9), outpatient **186.4** (病院 152.8, 一般診療所 33.6). By site, inpatients:
    胃 8.6, 結腸・直腸 15.8, 肝及び肝内胆管 4.0, 気管・気管支・肺 14.3, 乳房 5.4.
  - 退院患者平均在院日数 for discharges during 2023-09: 悪性新生物 **14.4 days** overall, against
    **28.4 days** for all conditions and **29.3 days** for 病院 across all conditions. By age
    band for 悪性新生物: 0–14 19.0, 15–34 14.0, 35–64 10.7, 65+ 15.5, 70+ 16.2, 75+ 17.6. By
    site: 胃 14.7, 結腸・直腸 15.3, 肝及び肝内胆管 13.6, 気管・気管支・肺 14.1, 乳房 9.4 [R7].
  - The mean stay is short and the age gradient is mild — which is exactly why the unlimited-day
    inpatient benefit is affordable, and why the product's cost has migrated to the
    diagnosis and treatment benefits, which do not depend on inpatient days at all.

### 15. Regulatory and actuarial basis

- **There is no standard incidence table for third-sector business.** 「第三分野商品は商品内容が
  多種多様であり、十分なデータの蓄積もないことから標準死亡率、参考純率といったスタンダードな指標が
  存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 [R3].
  This is the single most important regulatory fact for this product: the cancer-incidence basis
  is an insurer assumption, not a prescribed table, and any reference model must therefore build
  it from public data [R5] [R6] [R7] and mark it [std].
- **What *is* prescribed** is the mortality basis: 第三分野標準生命表2018, published in full and
  freely downloadable [R1], effective for contracts written from April 2018 [R2], prescribed by
  平成８年２月29日大蔵省告示第48号 for 標準責任準備金 [R4]. The table runs `x / l_x / d_x / q_x /
  e_x` from 0 to 116 for males and 0 to 118 for females. Spot values, **female**: q(0)
  0.00052, q(30) 0.00022, q(60) 0.00209, q(65) 0.00317, q(70) 0.00510, q(75) 0.00967
  [R1]. (Text correction, 2026-08-20: this list was recorded as "male". It is the female
  column of the PDF - the male column reads q(0) 0.00053, q(30) 0.00041, q(60) 0.00548,
  q(65) 0.00845, q(75) 0.02242 - and two other research files read the same six values
  as female. Ids and numbering unchanged.) Spot values, **male**, read off page 4 of the
  same PDF - the 第三分野標準生命表2018（男）table, which occupies that page in two half-tables,
  ages 0-59 on the left and 60-116 on the right: q(0) 0.00053, q(30) 0.00041,
  **q(40) 0.00076** (row 40, `l_40` 98,844, `d_40` 75, `e_40` 44.14), q(60) 0.00548,
  q(65) 0.00845, q(70) 0.01308, q(75) 0.02242, q(80) 0.04046, q(85) 0.07110,
  q(90) 0.11657, q(115) 0.58241, q(116) 1.00000; and **female**, page 5: q(40) 0.00043,
  q(80) 0.01899, q(85) 0.03843, q(90) 0.07574, q(118) 1.00000 [R1]. (Text addition,
  2026-08-20: 男 q(40) = 0.00076 is the anchor of the shipped mort_table.csv and is quoted
  in four files of this product, but the entry recorded no spot value carrying it and it
  could not be found in a retrieved document at review. It is on page 4 of the [R1] PDF at
  the location given above, re-read from the file, so the quote is **sourced and not
  [unverified]**. The remaining anchors of the shipped construction are listed with it, so
  that every rate the product quotes now points at an entry that carries it. Ids and
  numbering unchanged.) The corresponding
  生保標準生命表2018（死亡保険用）male values are materially higher
  (q(60) 0.00653, q(65) 0.01015, q(70) 0.01544, q(75) 0.02637) [R1] — the third-sector table is
  the *lighter* mortality table, which is the prudent direction for a morbidity-driven product
  where survival prolongs benefit payment.
- **It carries safety margins and is not a best-estimate basis** [R2]: built on the 国民表
  (第21回生命表, 2010), improved forward at 2.5% p.a. for 5 years then 1.0% p.a. for 3 years,
  then loaded by a 数学的危険論 adjustment sized to hold adverse deviation to ~2.28% (2σ) on an
  assumed 1,000,000 lives per sex, floored at 70% and capped at 85% of the pre-adjustment rate.
  Any best-estimate mortality used in a projection must be a stated [std] adjustment of it.
- **Third-sector reserving controls** [R3] [R4]: standard reserves under 平成8年大蔵省告示第48号;
  危険準備金 under 平成10年６月８日大蔵省告示第231号; annual 事後検証 of assumed incidence rates;
  a **ストレステスト** over a 10-year horizon comparing outgo at the pricing rate against outgo at
  危険発生率A (99% of incidence risk) and 危険発生率B (97.7%), with 危険準備金 topped up when the
  pricing rate falls short; and a **負債十分性テスト**. The tests are run, in principle, per
  契約区分 sharing a common 基礎率, per 保険業法施行規則 第69条 [R4]. The insurer chooses the
  incidence-projection model, which must be "reasonably" set [R3].
- **Dividends**: 「この保険には契約者配当金はありません」 — 無配当 on the retrieved contracts
  [S5] [S6] [S11]. No 三利源 dividend mechanics arise on this product line.
- **生命保険料控除 (premium tax relief)** [R8] [R9]: cancer insurance premiums fall in the
  **介護医療保険料控除** basket (contracts from 2012-01-01 paying on 疾病 or 身体の傷害 under
  医療費支払事由). New-regime schedule: premiums ≤ ¥20,000 deductible in full; ¥20,001–¥40,000 →
  premium × 1/2 + ¥10,000; ¥40,001–¥80,000 → premium × 1/4 + ¥20,000; above ¥80,000 → flat
  **¥40,000**. Each of the three baskets is capped at ¥40,000 and the combined cap is
  **¥120,000** [R9]. (Old regime, pre-2012 contracts: ¥25,000 / ¥50,000 / ¥100,000 breakpoints,
  flat ¥50,000 cap per basket [R9].)
- **Benefit taxation**: 「がん治療給付金、がん初回診断一時金、がん入院給付金、がん手術給付金、
  がん退院一時金、がん先進医療給付金、がん先進医療一時金およびがん通院給付金は、その受取人が被保険者
  本人のほか、その配偶者、直系血族または生計を一にする親族である場合には、原則として非課税」 [S1].
- **Policyholder protection**: 生命保険契約者保護機構 covers 責任準備金等 to **90%**, less for
  高予定利率契約, with 基礎率 (予定利率, 予定死亡率, 予定事業費率) changeable on transfer and an
  早期解約控除 possible [S1].

---

## Variation across carriers

The observed range that the drafting pass needs. Seven carriers; "—" means the retrieved
documents for that carrier do not state it.

| Feature | [S1] [S2] [S3] | [S5] | [S6] | [S7] [S8] | [S10] | [S11] [S12] | [S13] |
|---|---|---|---|---|---|---|---|
| Chassis | diagnosis + inpatient | diagnosis + inpatient | diagnosis + inpatient | diagnosis + outpatient, treatment riders | treatment-only main contract | diagnosis + monthly treatment | expense reimbursement |
| Waiting period | 90 d (day 91) | 90 d (day 91) | 90 d (day 91) | **3 months** | 90 d (day 91) | **3 months** | 90 d (day 91) |
| Premium in waiting period | payable | payable | payable | payable | payable | **not charged** | — |
| Pre-waiting diagnosis | contract **void** | contract **void** | benefits not paid | contract **void** | contract **void** | contract **void** | — |
| 上皮内新生物 | **full rate** | **full rate** | **half** (separate benefit) | **10%** on diagnosis benefits; full on surgery/radiation/outpatient | **full rate**; excluded from premium waiver | **50%** (separate benefit) | **full rate** |
| Diagnosis benefit repeat | **once ever** | **2 years** | **once ever** | once + rider at **2 years**, unlimited | **2 years**, 2nd+ requires hospitalisation | **once ever** | **3 years**, unlimited |
| 2-year clock measured from | n/a | previous trigger date | n/a | **1st of the month** of previous payment | **start date of last hospitalisation** | n/a | — |
| Inpatient day limit | **none** | **none stated** | **none** | no inpatient benefit | **none** (rider) | no inpatient benefit | **none** |
| Surgery benefit | 20 × base, unlimited | unlimited, but 1/60 d for some procedures | 20 × daily | 1 per **14 days** per 一連の手術 | per surgery, fee-schedule dedup | in monthly treatment benefit | actual cost |
| Radiation benefit | (in outpatient rider) | — | — | 1 per **60 days** | monthly, main contract | in monthly treatment benefit | actual cost |
| Chemotherapy benefit | (in outpatient rider) | monthly, **60-month** cap | — | monthly, 倍率 1 or 2, **120× combined** cap | monthly, main contract | ¥100k/mo (¥50k hormone-only, **60-month** cap) | actual cost |
| Outpatient limit | 60 d per 通院治療期間 (treatment-linked: none) | **45 d** per stay, **730 d** lifetime | — | **no day limit, no lifetime limit** | **120 d** per post-discharge period | in monthly treatment benefit | ¥20m per 5-y term |
| Advanced medicine cap | ¥20,000,000 + 10% lump (≤¥500k) | ¥10,000,000 | — | ¥20,000,000 + ¥150k/policy year | rider | ¥20,000,000, 患者申出療養 excluded | included in expense cover |
| Premium waiver trigger | disability only | disability only | disability only, cancer excluded | **none in the 契約概要** | **cancer diagnosis** (rider), in-situ excluded | **cancer diagnosis** (C/D types) | — |
| Surrender value | none if 終身払; else **10 × base** after premium term | min(30% of unsuppressed CV, max(日額×10, 診断額÷10)) after premium term | **full CV**, + APL + 契約者貸付 + 払済 | **none** | **none** | **none** | — |
| APL (自動振替貸付) | impossible (no CV) | impossible during premium term | **yes, ≤8% p.a.** | no | no | no | — |
| Grace, monthly | 1 month | — | 1 month | 1 month | — | **2 months** | — |
| Reinstatement | **1 year**, barred once a cancer benefit paid | — | **3 years** | **1 year** | — | **none** | — |
| Contestability | 2 years | — | 2 years | — | — | — | — |
| Term / renewal | 終身 | **10 y renewable to 90**, convertible to 終身 | 終身 | 10 y renewable | 終身 | 終身 | **5 y renewable to 90** |
| Issue ages | 0–75 [S15] | example at 30 | — | — | — | 18–80 | — |
| Premium modes | 年 / 半年 / 月 | 月 (example) | 年 / 半年 / 月 | — | — | **月払のみ** | — |
| Dividends | — | **無配当** | **無配当** | — | — | **無配当** | — |

**What does not vary.** Every retrieved contract: (i) has a waiting period before cancer cover
starts, and treats a diagnosis inside it as voiding the contract rather than merely excluding the
claim; (ii) dates the diagnosis to the *examination*, not the consultation; (iii) requires
diagnosis by a Japanese-qualified physician or dentist on histopathological findings; (iv) pays
the inpatient benefit with **no day limit** where it has one at all; (v) treats two simultaneous
surgeries as one; (vi) carries a clause allowing the insurer to change the payment triggers, with
regulatory approval, if the public medical insurance scheme changes; and (vii) is 無配当 where the
dividend basis is stated.

**Most representative design for a reference implementation.** A whole-life, 無解約払戻金型
cancer contract with a 90-day waiting period (cover from day 91) and pre-waiting-period diagnosis
voiding the contract; 上皮内新生物 inside the definition of cancer but paying a **reduced**
diagnosis benefit (the half-rate design is the median of the three observed treatments); a
診断一時金 of ¥1,000,000 repeating on a **2-year** cycle with no lifetime cap, the clock running
from the previous payment trigger; a daily inpatient benefit with **no day limit and no lifetime
limit**; a surgery benefit at a multiple of the daily amount with no count limit; a **monthly**
treatment benefit for chemotherapy and radiation subject to a stated lifetime month cap;
an outpatient benefit on the treatment-linked, unlimited-day design; premium waiver on cancer
diagnosis excluding in-situ; monthly premiums with a one-month grace, a one-year reinstatement
window and no APL.

---

## Fetch failures and gaps

**URLs that could not be retrieved, or retrieved without usable content**

- `https://www.aflac.co.jp/keiyakugaiyou/pdf/days1_27545300.pdf` [S9] — downloaded (20 pp.,
  9.9 MB) but **image-only**: 19 characters of text extracted from the whole file. No OCR
  attempted. **What is lost**: the base Days1 product's がん入院給付金 daily amount and its
  limits, and its issue-age table. Everything reported for that carrier therefore comes from the
  *Days1プラス* supplement [S7] [S8], which has no inpatient benefit — so this library has **no
  sourced Aflac inpatient benefit**.
- `https://www.orixlife.co.jp/cancer/believe/pdf/believe_pamphlet.pdf` [S4] — downloaded but the
  text layer is subset-encoded with no ToUnicode map; **all numerals drop out**. **What is
  lost**: the published premium-rate table by age and sex for that product, and its issue-age
  table (recovered instead from a distributor listing [S15], which is secondary).
- `https://www.orixlife.co.jp/cancer/believe/pdf/believe_juyou.pdf` and
  `.../believe_kei.pdf` — downloaded (5 pp. and 8 pp.) but both mojibake for the same reason.
  Nothing taken from either; they are not given source ids.
- `https://www.secom-sonpo.co.jp/pdfbox/MEDCOM_BP1030.pdf` [S14] — downloaded but uses the
  `/83pv-RKSJ-H` encoding, which `pypdf` does not implement; text is unreadable. **What is
  lost**: the expense product's premium table, per-claim sub-limits and issue ages. The
  structural facts for that carrier come from its product page [S13] instead.
- `https://www.orixlife.co.jp/cancer/believe/pdf/yakkan_believe_20240402.pdf` — the *約款* half
  of this file (roughly pages 65–140) is not text-extractable, though the *しおり* half is.
  **What is lost**: verbatim article text. Mitigated: the しおり restates every rule and gives
  the article number, and every fact reported from [S1] is drawn from the しおり half.
- `https://www7.tmn-anshin.co.jp/yakkan/pdf/A0203131102.pdf` [S5] — the 約款 body is likewise
  not extractable; only the 契約概要 / 注意喚起情報 / 自動更新 pages came through (483 usable
  lines from 156 pages). **What is lost**: verbatim benefit-article text, the inpatient benefit's
  day-limit clause (its *absence* from the 契約概要 limits column is what is reported, which is
  weaker than reading the article), and the exclusions list.
- `https://www.actuaries.jp/lib/standard-life-table/index2018.html` — retrieved, but the page
  itself does **not** name the 告示 or list the table variants; the variant list and the
  第三分野 table come from the PDFs [R1] [R2] and the 告示 number from the supervisory guideline
  [R4].
- e-Stat 患者調査 detail tables (統計表 Z124-x, Z134 — 退院患者平均在院日数 by 傷病小分類 ×
  性・年齢階級) were **not fetched**. Only the 概況 summary [R7] was retrieved. **What is lost**:
  length-of-stay distributions by cancer site and age at finer granularity than the 傷病大分類
  bands quoted above; a length-of-stay *distribution* (as opposed to a mean) is not available
  from any source retrieved this session.

**Claims left [unverified], and why**

- **A 1年に1回 cancer diagnosis benefit.** The task brief named 1年に1回 as a live market
  alternative to 2年に1回. **No retrieved document contains one.** The retrieved cycles are:
  once-only (3 carriers), 2 years (3 carriers) and 3 years (1 carrier). The only 1-year cycles
  found are on a *heart/stroke* rider [S7] and on an annual *survival income* benefit [S11].
  Treat a 1-year cancer diagnosis cycle as [unverified] and out of the sourced range until a
  contract carrying one is retrieved.
- **自由診療抗がん剤治療給付金** as a named benefit (reported in search-result text at
  ¥200,000/month against a ¥100,000/month standard chemotherapy benefit, on a later edition of
  [S10]'s product). The retrieved 2015 edition [S10] does **not** contain it. [unverified].
- **Orix Believe issue ages and premium terms** — taken from a distributor listing [S15] because
  the carrier's own statement of them sits only in the non-extractable pamphlet [S4]. The
  0–75 range and the 60/65/終身 premium terms should be re-verified against a carrier document
  before being cited as a hard parameter.
- **Orix Believe benefit multiples** (100× / 50× / ×日数 / 20× / 10×) — decoded from a
  subset-font PDF [S2] with a glyph→digit mapping that was validated against three values
  independently confirmed in [S1]. Reported as sourced, but flagged here so that a reviewer can
  see exactly how they were obtained.
- **The 東京海上日動あんしん生命 document is a 2013.10 edition** [S5]. Its premium example is on a
  2013-10-22 calculation base and its benefit menu predates the treatment-benefit shift visible
  in [S7] and [S10]. Its structural facts (renewal mechanics, 2-year diagnosis cycle, surrender
  formula, outpatient caps) are used; its premium figures should be treated as a historical data
  point, not a current rate.
- **Aflac premium waiver** — reported as *absent* from the retrieved 契約概要 [S7]. That is an
  observed absence in one document for one product, not a claim that the carrier offers no
  premium waiver on any cancer product.
- **Suicide and other exclusions** — not extracted for this product line. Cancer contracts pay on
  diagnosis and treatment, so the suicide clause bites only where a death benefit exists ([S6]
  alone among the retrieved contracts). The exclusions lists in the retrieved 約款 bodies were
  mostly in the non-extractable halves. [unverified] for this product.
- **標準利率 / 予定利率 for third-sector contracts** — not established this session. The
  標準責任準備金 notification is identified [R4] but its current interest rate was not retrieved.
  This is a cross-product matter and belongs in the `[REG-R#]` reference library rather than here.
- **Lapse and persistency experience for cancer business** — no public source retrieved. Nothing
  in [R3], [R10] or the carrier documents gives a lapse rate by duration. Any persistency
  assumption in the model must be [std].
- **Loss ratios, expense loadings, or any pricing basis** — none published by any carrier
  retrieved. The single premium example [S5] is the only price point in this file.
- **In-situ *incidence by age band*** — [R5] publishes with/without-in-situ **totals** by site and
  sex and the age-banded rates for the invasive definition; whether the age-banded breakdown is
  also published on the in-situ-inclusive basis was not confirmed cell by cell. The 12.2%
  increment quoted above is an all-ages figure and should not be assumed age-invariant.
- **Cancer-specific mortality for the diagnosed population** — [R6] gives 5-year *relative*
  survival, which is not the same as a cohort survival curve and is not a mortality table. Any
  post-diagnosis survival model built on it is a [std] construction.
