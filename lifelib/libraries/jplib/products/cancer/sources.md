# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/cancer.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so
the numbering has a gap: S14 (the expense product's 2009 brochure) was downloaded but uses
an encoding `pypdf` does not implement, and nothing beyond the document's own identity could
be read from it, so no product document cites it. Access date for all sources: 2026-08-20.
No sources were newly added at drafting. Cross-product [REG-R#] tags are listed in their own
section at the end.

Five of the fourteen entries below record a **failed or partial retrieval**: [S9] is
image-only and [S4] loses every numeral, so nothing quantitative comes from either; [S1] and
[S5] extracted only in the しおり／契約概要 half, with the 約款 body unreadable; and [S2] needed a
glyph-to-digit mapping recovered before its numbers could be read at all. They are kept
because the product documents cite them as the reason a fact is [unverified] or is taken
from a weaker source, and because an entry that records what could not be read is worth more
than a silently dropped source. [S15] is a **distributor** listing, not a carrier document,
and is used only for the issue-age and premium-term envelope that the carrier states only in
the unreadable [S4].

Several product-specific [R#] entries cover the same statute, notification or table as a
cross-product [REG-R#] entry. Where the fact was extracted for this product the documents
cite the product-specific [R#]; where the load-bearing statement is the cross-product one —
the redistribution restriction on the standard tables, the ESR regime, the market
statistics, the citable cancer-registry download — they cite the [REG-R#]. Both resolve to a
retrieved document.

---

## Primary product sources

(jplib-cancer-s1)=

### S1 — オリックス生命保険株式会社, 「がん保険Believe［ビリーブ］ ご契約のしおり／約款」 (policy booklet and conditions)
- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: ご契約のしおり／約款, がん保険Believe［ビリーブ］, file `yakkan_believe_20240402.pdf` (dated
  2024-04-02 in the filename), 140 pp. The booklet is in two halves: ご契約のしおり (pp. 1–≈64)
  followed by the 普通保険約款 and 特約 (*tokuyaku*, rider) 条項 (pp. ≈65–140).
- Doc type: ご契約のしおり・約款
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/yakkan_believe_20240402.pdf
- Accessed: 2026-08-20. Retrieved: YES, in part (full PDF downloaded, 140 pp.; the しおり half
  extracted cleanly, the 約款 half is image/subset-font and did **not** extract. Every fact
  attributed to this source is taken from the しおり half, which restates each 約款 article and
  cross-references it by article number; verbatim article text is not available)

(jplib-cancer-s2)=

### S2 — オリックス生命保険株式会社, 「がん保険Believe 商品概要のご説明」 (product summary)
- Publisher: オリックス生命保険株式会社
- Document: 商品概要のご説明, file `believe_shohin_direct.pdf`, 2 pp.
- Doc type: 商品概要 (the 契約概要-role document for the direct channel)
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/believe_shohin_direct.pdf
- Accessed: 2026-08-20. Retrieved: YES, with a caveat (the PDF uses a subset font whose
  numerals decode to combining-mark glyphs rather than ASCII digits. The glyph-to-digit
  mapping was recovered and cross-checked against three values independently confirmed in
  [S1] — 通算2,000万円 and 1回の療養につき50万円 on the advanced-medicine rider, and 退院後30日未満 on the
  discharge lump sum. All three decoded correctly, so the benefit multiples read from this
  document are reported as sourced; the decoding step is disclosed in the research file so a
  reviewer can re-run it)

(jplib-cancer-s3)=

### S3 — オリックス生命保険株式会社, がん保険Believe 商品ページ (product page)
- Publisher: オリックス生命保険株式会社
- Doc type: product page (consumer/direct)
- URL: https://www.orixlife.co.jp/cancer/believe/
- Accessed: 2026-08-20. Retrieved: YES (used for the document index — which named PDFs exist
  at which URLs — and for the headline ¥1,000,000 diagnosis lump sum at the ¥10,000 基本給付金額
  course)

(jplib-cancer-s4)=

### S4 — オリックス生命保険株式会社, 「がん保険Believe 通信販売用パンフレット」 (product brochure)
- Publisher: オリックス生命保険株式会社
- Document: 通信販売用パンフレット, file `believe_pamphlet.pdf`, 5 pp., 1.5 MB
- Doc type: 商品パンフレット
- URL: https://www.orixlife.co.jp/cancer/believe/pdf/believe_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: **NO (partial)** — the file downloaded but its text layer
  is subset-encoded with no usable ToUnicode map: Japanese renders as mojibake and **all
  numerals drop out entirely**. Nothing quantitative was taken from it. What is lost is this
  carrier's published premium-rate table by age and sex and its issue-age table; the
  issue-age envelope is taken instead from the distributor listing [S15] and is flagged
  wherever it is used. Two companion files at the same location (`believe_juyou.pdf`,
  `believe_kei.pdf`) failed in the same way and are not given source ids.

(jplib-cancer-s5)=

### S5 — 東京海上日動あんしん生命保険株式会社, 「がん治療支援保険 契約概要／注意喚起情報・ご契約のしおり・約款」
- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: がん治療支援保険［無配当］, 2013.10改定 edition, file `A0203131102.pdf`, 156 pp., print code
  資13-KF04-035; the 契約例 is calculated as at 平成25年10月22日 (2013-10-22)
- Doc type: 契約概要／注意喚起情報 + ご契約のしおり・約款
- URL: https://www7.tmn-anshin.co.jp/yakkan/pdf/A0203131102.pdf
- Accessed: 2026-08-20. Retrieved: YES, in part (full PDF downloaded, 156 pp.; the 契約概要,
  注意喚起情報 and 自動更新 pages extracted cleanly — 483 usable lines — while most of the 約款 body did
  not. The inpatient benefit's *absence* of a day limit is reported from the 契約概要 limits
  column rather than from the benefit article, which is the weaker of the two readings and
  is said so where it is used. This is a **2013 edition**: its structural facts are used,
  its premium figures are treated as a historical data point, not a current rate)

(jplib-cancer-s6)=

### S6 — ジブラルタ生命保険株式会社, 「終身がん保険（無配当） ご契約のしおり・約款」 (policy booklet and conditions)
- Publisher: ジブラルタ生命保険株式会社 (Gibraltar Life Insurance Company, Ltd.)
- Document: ご契約のしおり・約款, 終身がん保険（無配当）, 2022年12月版, file `L105_syusin_gan_202212.pdf`, 132 pp.;
  internal 約款 code B5-022, 最終修正日 2022-09-13, データ出力日 2022-09-26
- Doc type: ご契約のしおり・約款
- URL: https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/L105_syusin_gan_202212.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 132 pp.; the 約款 body extracted
  cleanly and was read article by article — the only retrieved cancer contract for which
  verbatim article text was available, and the only one carrying a genuine 解約返戻金
  (*kaiyaku-henreikin*, surrender value) with
  自動振替貸付, 契約者貸付 and 払済保険への変更)

(jplib-cancer-s7)=

### S7 — アフラック生命保険株式会社, 「生きるためのがん保険Days1プラス 契約概要」 (contract summary)
- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: 契約概要, 生きるためのがん保険Days1プラス (formal product name がん保険〔無解約払戻金2018契約者用〕), file
  `days1plus_27604700.pdf`, 24 pp.
- Doc type: 契約概要
- URL: https://www.aflac.co.jp/keiyakugaiyou/pdf/days1plus_27604700.pdf
- Accessed: 2026-08-20. Retrieved: YES (24 pp. downloaded; the benefit-limit tables
  extracted and read. This is the most granular published benefit-limit table found in this
  session)

(jplib-cancer-s8)=

### S8 — アフラック生命保険株式会社, 「生きるためのがん保険Days1プラス ご契約のしおり・約款」
- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款, file `days1_77945100.pdf`, 212 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.aflac.co.jp/yakkan/pdf/days1_77945100.pdf
- Accessed: 2026-08-20. Retrieved: YES (212 pp. downloaded, text extracted, the しおり sections
  read — 責任開始日, the pre-責任開始日 invalidity rule, first-premium 払込期月 and grace, grace by
  payment mode, the reinstatement window and the 契約年齢 definition)

(jplib-cancer-s9)=

### S9 — アフラック生命保険株式会社, 「生きるためのがん保険Days1 契約概要」 (contract summary)
- Publisher: アフラック生命保険株式会社
- Document: 契約概要, 生きるためのがん保険Days1, file `days1_27545300.pdf`, 20 pp., 9.9 MB
- Doc type: 契約概要
- URL: https://www.aflac.co.jp/keiyakugaiyou/pdf/days1_27545300.pdf
- Accessed: 2026-08-20. Retrieved: **NO** — the file downloaded but is image-only: `pypdf`
  extracted 19 characters of text from the whole document, and no OCR was attempted. This is
  the *base* product of the pair, which — unlike the supplement [S7] — carries a がん入院給付金.
  Its daily amount, its limits and its issue-age table are therefore **not** sourced, and
  this library has no sourced inpatient benefit from this carrier.

(jplib-cancer-s10)=

### S10 — チューリッヒ生命保険株式会社, 「終身ガン治療保険プレミアム／３大疾病保険プレミアム ご契約のしおり・約款」
- Publisher: チューリッヒ生命保険株式会社 (Zurich Life Insurance Company Ltd, Japan branch business)
- Document: ご契約のしおり・約款 WC143, 2015年7月改訂 (終身払・短期払), 156 pp.; formal main-contract name
  無解約払戻金型終身ガン治療保険（抗がん剤等保障）
- Doc type: ご契約のしおり・約款
- URL: https://www.zurichlife.co.jp/faq/others/clause/-/media/Files/ZurichLife/faq/clause/kikeiyaku/gan/WC143.ashx?la=ja-JP
- Accessed: 2026-08-20. Retrieved: YES (156 pp. downloaded; the しおり and 特約条項 extracted and
  read. The **treatment-benefit-only chassis**: the main contract pays only 放射線治療給付金 and
  抗がん剤・ホルモン剤治療給付金, with hospitalisation, surgery, diagnosis and outpatient all pushed out
  into nine named 特約)

(jplib-cancer-s11)=

### S11 — ライフネット生命保険株式会社, 「終身がん保険（無配当・無解約返戻金型） ご契約のしおり・約款」
- Publisher: ライフネット生命保険株式会社 (LIFENET INSURANCE COMPANY)
- Document: ご契約のしおり・約款, 終身がん保険（無配当・無解約返戻金型）, file `LIFENET_yakkan_gan_latest.pdf`, 60 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_gan_latest.pdf
- Accessed: 2026-08-20. Retrieved: YES (60 pp. downloaded, text extracted and read in full)

(jplib-cancer-s12)=

### S12 — ライフネット生命保険株式会社, 終身がん保険 商品ページ (product page)
- Publisher: ライフネット生命保険株式会社
- Doc type: product page (consumer/direct)
- URL: https://www.lifenet-seimei.co.jp/product/cancer/whole-life-cancer/
- Accessed: 2026-08-20. Retrieved: YES (the selectable diagnosis-lump-sum ladder, the
  issue-age range, the premium-term and premium-mode statements and the three-course
  structure were read from the page text)

(jplib-cancer-s13)=

### S13 — セコム損害保険株式会社, 「自由診療保険メディコム 補償内容」 (product page)
- Publisher: セコム損害保険株式会社 (SECOM General Insurance Co., Ltd.) — a **non-life** insurer
- Doc type: product page (consumer)
- URL: https://www.secom.co.jp/medcom/compensation/
- Accessed: 2026-08-20. Retrieved: YES (the 実損てん補 expense-reimbursement variant, written
  under a 損害保険業免許: cancer treatment cost indemnified at actual cost, including 自由診療, rather
  than on a fixed benefit schedule)

(jplib-cancer-s15)=

### S15 — 株式会社アドバンスクリエイト（保険市場）, がん保険Believe 商品ページ (distributor listing)
- Publisher: 株式会社アドバンスクリエイト, operator of the comparison site 保険市場 — a **distributor**, not
  the carrier. Treated throughout as a **secondary** source and used only for the issue-age
  and premium-term envelope, which the carrier states only in the non-extractable [S4].
- Doc type: comparison-site product listing
- URL: https://www.hokende.com/life-insurance/cancer/whole_cancer/item-or15
- Accessed: 2026-08-20. Retrieved: YES. The figures taken from it — 契約可能年齢 0 (from 15 days
  old at 告知) to 75, 保険期間 終身, 保険料払込期間 60歳／65歳／終身 in the direct channel, and the ¥5,000 基本給付金額
  course restricted to ages 50–75 — should be re-verified against a carrier document before
  being relied on as hard parameters.

---

## Regulatory and actuarial references

(jplib-cancer-r1)=

### R1 — 日本アクチュアリー会, 「標準生命表2018」（数値表）
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — a title page and **four** tables:
  生保標準生命表2018（死亡保険用）男／女, running to terminal ages 109 and 113, and
  **第三分野標準生命表２０１８（男）（女）**, running to terminal ages 116 and 118 — each a full
  `x / l_x / d_x / q_x / e_x` table. There is no 年金開始後用 pair in this file
- Doc type: industry standard table (statutory valuation table)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf (index page:
  https://www.actuaries.jp/lib/standard-life-table/index2018.html)
- Accessed: 2026-08-20. Retrieved: YES (5-page PDF downloaded, the full numeric tables
  extracted as machine-readable numbers; the spot values quoted in the product documents
  were read from this file. The index page itself names neither the 告示 nor the table
  variants — those come from the PDFs and from [R4])
- The 第三分野標準生命表2018 tables are pages **4 (男)** and **5 (女)**, each page carrying the
  whole table in two half-tables — ages 0–59 on the left, 60 upward on the right.
  男 q(40) = 0.00076, the anchor of this product's shipped `mort_table.csv`, is the age-40
  row of page 4; every other rate the product quotes is listed against this entry in
  `_research/cancer.md`, so each quote points at the entry that carries it

(jplib-cancer-r2)=

### R2 — 日本アクチュアリー会, 「標準生命表2018の作成概要」
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料①–⑤; 資料④ is 第三分野標準生命表2018)
- Doc type: technical note accompanying the standard table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (6-page PDF downloaded, text extracted and read)

(jplib-cancer-r3)=

### R3 — 金融庁, 「第三分野の責任準備金積立ルール・事後検証等の概要について」（別紙１−２）
- Publisher: 金融庁 (Financial Services Agency)
- Document: 別紙１−２, 8 pp., published 2006-02-10 as part of the FSA's third-sector reserving
  package
- Doc type: FSA policy paper
- URL: https://www.fsa.go.jp/news/newsj/17/hoken/f-20060210-1/01_2.pdf
- Accessed: 2026-08-20. Retrieved: YES (8-page PDF downloaded, text extracted and read). The
  load-bearing regulatory statement for this product: 第三分野 (*dai-san-bun'ya*, third-sector)
  covers 医療保険, がん保険 and 介護保険, and **no standard incidence rate and no reference pure
  premium exist** for it.

(jplib-cancer-r4)=

### R4 — 金融庁, 「保険会社向けの総合的な監督指針」II−２ 財務の健全性
- Publisher: 金融庁
- Doc type: supervisory guideline (section view)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES. II−２−１−２ and II−２−１−４ carry the third-sector
  reserving checkpoints and cite 平成８年２月29日大蔵省告示第48号 and 平成10年６月８日大蔵省告示第231号. The retrieved
  page does **not** restate the 99% / 97.7% stress levels; those come from [R3].

(jplib-cancer-r5)=

### R5 — 国立がん研究センター, 全国がん登録に基づく全国がん罹患数・率 2016–2023
- Publisher: 国立研究開発法人 国立がん研究センター がん対策研究所, from data provided under がん登録等の推進に関する法律
- Document: `cancer_incidenceNCR(2016-2023).xls`, ≈1.16 MB; sheets `number` (counts by
  5-year age band × site × sex × diagnosis year), `rate` (per 100,000), `asr`
  (age-standardised), `detail`, `pop`
- Doc type: public statistical table (downloadable Excel)
- URL: https://ganjoho.jp/reg_stat/statistics/data/dl/excel/cancer_incidenceNCR(2016-2023).xls
  (index page: https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)
- Accessed: 2026-08-20. Retrieved: YES (file downloaded and parsed with pandas; sheet names,
  headers and the 2023 rows read directly). This is the citable public incidence basis that
  lets the model ship a sourced rather than an invented decrement, and it publishes paired
  rows **with and without 上皮内がん** (全部位 C00–C96 against 全部位（上皮内がん含む） C00–C96 D00–D09).

(jplib-cancer-r6)=

### R6 — 国立がん研究センター, 全国がん登録に基づく部位別5年相対生存率 (2016–2018 diagnoses)
- Publisher: 国立研究開発法人 国立がん研究センター
- Document: `cancer_survivalNCR(2016-2018).xlsx`, ≈64 KB; sheets 最新データ（部位）, 最新データ（進行度別）,
  推移データ（部位）, 推移データ（進行度別）, 推移データ（進行度の割合）
- Doc type: public statistical table (downloadable Excel)
- URL: https://ganjoho.jp/reg_stat/statistics/data/dl/excel/cancer_survivalNCR(2016-2018).xlsx
- Accessed: 2026-08-20. Retrieved: YES (file downloaded and parsed; 対象者数 and 標準誤差 sit on
  every cell). It publishes **relative** survival, which is not a cohort survival curve and
  not a mortality table — any post-diagnosis survival model built on it is a [std]
  construction, and the product documents say so.

(jplib-cancer-r7)=

### R7 — 厚生労働省, 「令和５年（2023）患者調査の概況」
- Publisher: 厚生労働省 (Ministry of Health, Labour and Welfare)
- Document: 令和５年（2023）患者調査の概況, 33 pp.
- Doc type: official statistics summary (基幹統計)
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/kanjya.pdf (index:
  https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/index.html)
- Accessed: 2026-08-20. Retrieved: YES (33-page PDF downloaded; the 推計患者数 and 退院患者平均在院日数
  tables extracted as machine-readable numbers). The full detail tables sit on e-Stat under
  統計表 Z124-x / Z134 and were **not** fetched, so a length-of-stay *distribution* — as
  opposed to a mean — is not available from any source retrieved for this product.

(jplib-cancer-r8)=

### R8 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁 (National Tax Agency)
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES (the three post-2012 baskets, and the definition of
  the 介護医療保険契約等 basket into which a がん保険 premium falls)

(jplib-cancer-r9)=

### R9 — 国税庁, タックスアンサー No.1140「生命保険料控除」
- Publisher: 国税庁
- Doc type: tax guidance (タックスアンサー)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES (the 新制度 and 旧制度 deduction schedules and caps; the
  住民税 caps are not stated on the page and are not asserted anywhere in the product
  documents)

(jplib-cancer-r10)=

### R10 — 生命保険文化センター, 「2025（令和７）年度 生活保障に関する調査《速報版》」
- Publisher: 公益財団法人 生命保険文化センター (Japan Institute of Life Insurance)
- Document: 2025（令和７）年度 生活保障に関する調査 速報版, 2025年10月, 128 pp.; N = 4,837
- Doc type: national household survey
- URL: https://www.jili.or.jp/files/research/chousa/pdf/r7/seikatuhoshouchousa_2025sokuhouban.pdf
- Accessed: 2026-08-20. Retrieved: YES (128-page PDF downloaded; 図表 II-19, the cancer-cover
  penetration series, read). Its base and question differ from those of the household survey
  at [REG-R32], and the two penetration figures are **not** comparable; the product
  documents quote both and say which base each is on.

(jplib-cancer-r11)=

### R11 — 生命保険文化センター, 「がん保険」 (product-type explainer)
- Publisher: 公益財団法人 生命保険文化センター
- Doc type: consumer education page (生命保険の種類 → 主契約 (*shu-keiyaku*, main contract) の種類)
- URL: https://www.jili.or.jp/knows_learns/kind/main/34.html
- Accessed: 2026-08-20. Retrieved: YES. An independent, non-carrier statement of the product
  archetype — the benefit menu, the ~90-day waiting period as the market norm, and the flat
  statement that the hospitalisation benefit carries **no day limit**. It is the only source
  in this file that states the archetype without selling a product.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the cancer
documents:

- **REG-R1** — 保険業法 第3条: the 第一分野／第三分野 licence split, and why the same class is writable
  under a 損害保険業免許 — which is how the expense-reimbursement carrier [S13] writes cancer cover
  at all. fetched_ok: yes.
- **REG-R2** — 保険業法 第4条: the 基礎書類, and why every pricing-basis parameter here is [std] while
  every contractual parameter carries an [S#] tag. fetched_ok: yes.
- **REG-R4** — 保険業法 第116条: the delegation the whole 標準責任準備金 chain hangs on. fetched_ok: yes.
- **REG-R5** — 保険業法 第120条: appointment of the 保険計理人. fetched_ok: yes.
- **REG-R6** — 保険業法 第121条: the 意見書 and the statutory demand behind the 1号収支分析. fetched_ok:
  yes.
- **REG-R7** — 施行規則 第68条: which contracts are standard-reserve contracts. fetched_ok: yes.
- **REG-R8** — 施行規則 第69条: the reserve taxonomy, including the separately identified
  third-sector 危険準備金. fetched_ok: yes.
- **REG-R9** — 施行規則 第30条の2: the four surplus-distribution methods — cited only to record
  that this chassis is 無配当 and distributes nothing. fetched_ok: yes.
- **REG-R10** — 平成8年大蔵省告示第48号: 平準純保険料式, the table vintages and the 標準利率
  (*hyōjun riritsu*, standard valuation interest rate) reset machinery.
  fetched_ok: yes, but from an unofficial consolidated mirror.
- **REG-R11** — 告示48号改正 (2017): adoption of 第三分野標準生命表2018 from 2018-04-01. fetched_ok: yes.
- **REG-R13** — 平成10年6月8日大蔵省告示第231号: the 第三分野 stress test. fetched_ok: **no** — the
  notification's own text was not located. Its role is asserted; its magnitudes are
  [unverified], and the 99% / 97.7% levels quoted in these documents come from [R3] instead.
- **REG-R14** — 保険会社向けの総合的な監督指針（本編）: third-sector reserving and the
  automatic-renewal-under-waiver instruction, II-4-2-2 on the 契約締結前交付書面, and 自動振替貸付 as a
  policyholder election. fetched_ok: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: ESR commencement 2026-03-31, the 100% trigger, 現在推計 +
  MOCE, the 99.5% calibration. fetched_ok: yes.
- **REG-R17** — ソルベンシー・マージン比率: the superseded 200% threshold and market SMR levels.
  fetched_ok: **no** for the 告示 itself; the figures come from REG-R14 and REG-R15.
- **REG-R18** — 標準生命表2018 PDF: the public valuation qx tables, including 第三分野標準生命表2018.
  fetched_ok: yes.
- **REG-R19** — 標準生命表 Excel (1996/2007/2018): the machine-readable form of the tables, which
  is what the model's [std] mortality input points at in its `provenance` column.
  fetched_ok: yes.
- **REG-R20** — 標準生命表2018 の作成概要: the 2σ margin, the improvement allowance, the 保険年齢方式
  (*hoken-nenrei hōshiki*, nearest-birthday age) construction basis, and the exclusion of
  高度障害 from the third-sector table. fetched_ok: yes.
- **REG-R21** — 日本アクチュアリー会 索引と利用規約: redistribution of the tables is restricted, which is why
  this library ships a [std] proxy and cites the real table rather than copying it.
  fetched_ok: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析 — at least ten future years, per segment. fetched_ok:
  yes.
- **REG-R23** — 監督指針 VI: the 日本アクチュアリー会 as 指定法人 under 法第122条の2. fetched_ok: yes.
- **REG-R27** — 患者調査 退院患者平均在院日数: stay length by age and cause — the evidence that a
  no-day-limit cancer inpatient benefit is affordable. fetched_ok: yes.
- **REG-R28** — 最新がん統計: 生涯罹患確率 男 61.1% ／ 女 50.1%, 罹患数 993,469 (2023) and 5年相対生存率 64.8% — the
  anchor for why this is a mass-market product and why its benefits are shaped around
  survival rather than death. fetched_ok: yes.
- **REG-R29** — がん統計 データダウンロード: the citable age-and-site incidence datasets and the
  attribution string the model's [std] incidence table must carry in its `provenance`
  column. fetched_ok: yes (index page; the workbooks were opened separately as [R5] and
  [R6]).
- **REG-R31** — 生命保険の動向 2025年版: ガン保険 in force by policy count and its new-business share,
  third-sector annualised premium, and the 5.6% industry lapse rate against which any [std]
  persistency assumption must be reconciled. fetched_ok: yes.
- **REG-R32** — 生命保険に関する全国実態調査 2024年度: household penetration of がん保険・がん特約 on the 民保加入世帯
  base. fetched_ok: yes.
- **REG-R33** — e-Stat: the access route to the machine-readable 患者調査 grids that [R7]
  summarises; licence terms unread. fetched_ok: yes (home page only).
- **REG-R34** — 保険法 第51条: the statutory suicide exclusion has no time limit — cited here to
  record that it does not bite on a composite with no death benefit. fetched_ok: yes.
- **REG-R35** — 保険法 第55条: the five-year contestability ceiling and the one-month discovery
  clock, inside which the observed two-year contractual windows sit. fetched_ok: yes.
- **REG-R36** — 保険業法 第309条: the eight-day dispatch-rule クーリング・オフ, scoped out here
  explicitly. fetched_ok: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: 90%-of-reserve compensation. fetched_ok: yes (Q1 only).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of the compensation rate. fetched_ok:
  yes.
- **REG-R43** — 所得税法 第76条: three ¥40,000 baskets capped at ¥120,000, of which 介護医療保険料 is
  this product's. fetched_ok: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS are
  three separate bases fed by one set of projected cash flows. fetched_ok: yes.

---

## Provenance note

Extraction details — which facts were read from which document, the per-source
fact-extraction sections, the seven-carrier variation table, and the full gaps register (the
image-only 契約概要 [S9], the three subset-font brochures, the non-extractable 約款 halves of [S1]
and [S5], the unfetched e-Stat length-of-stay grids, the absence of any published 標準利率 or
予定利率 (*yotei riritsu*, assumed interest rate) for this class, the absence of any published
lapse experience for cancer business, and
the finding that **no retrieved contract carries a 1年に1回 diagnosis benefit**) — live in
`_research/cancer.md`.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #jplib-cancer-r3
[R4]: #jplib-cancer-r4
[R5]: #jplib-cancer-r5
[R6]: #jplib-cancer-r6
[R7]: #jplib-cancer-r7
[REG-R32]: #jplib-reg-r32
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
