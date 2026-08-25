# 医療保険 (third-sector medical: hospitalization and surgery benefits) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose: source
library for a Japanese 医療保険 (*iryō hoken*, third-sector medical insurance) liability cash flow
reference model — the `jplib` third-sector **chassis**, from which `cancer` and `nursing_care`
state their deltas. The product is a frequency × severity × limit structure (入院給付金日額 ×
入院日数, capped per hospitalization and in aggregate) plus event benefits (手術給付金,
放射線治療給付金, 先進医療給付金, 一時金), not a sum-assured structure.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(product-specific regulatory/actuarial reference) pointing at a document actually retrieved and
read during this session, or is tagged [unverified] where it is general knowledge or a search
snippet that could not be confirmed against a retrieved document. Company and branded product
names appear here and in `sources.md` only. Access date for all fetched sources: 2026-08-20.

---

## Primary sources

### S1 — オリックス生命, 「契約概要／注意喚起情報」 医療保険CURE Next / CURE Lady Next (契約締結前交付書面)
- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: 契約概要／注意喚起情報, 医療保険CURE Next[キュア・ネクスト] および
  医療保険CURE Lady Next[キュア・レディ・ネクスト], file `importance_cure_next_20250402.pdf`
  (dated 2025-04-02 in the filename), 28 pp.
- Doc type: 契約締結前交付書面 (pre-contract disclosure: 契約概要 + 注意喚起情報)
- URL: https://www.orixlife.co.jp/importance/pdf/importance_cure_next_20250402.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded with a browser User-Agent, 28 pp.,
  text extracted and read; p. 1 and parts of the cover use non-embedded CID fonts and extracted
  as mojibake — all substantive tables on pp. 2–28 extracted cleanly)
- Key content: full benefit menu with amounts, the three 支払限度日数 plans, 手術給付金 structure
  tied to the 医科診療報酬点数表, 先進医療特約(2018) cap and 一時金, 入院一時金特約,
  通院治療支援特約, 特定三疾病一時金特約, 特定三疾病保険料払込免除特則 triggers, the 181-day
  re-admission rule, 解約払戻金 rules, 告知義務違反 window, grace/失効/復活, suicide exclusion.

### S2 — オリックス生命, 「無配当 無解約払戻金型医療保険（2022）ご契約のしおり／約款」
- Publisher: オリックス生命保険株式会社
- Document: ご契約のしおり／約款, 無配当 無解約払戻金型医療保険（2022）, file
  `yakkan_cure_next_20240402.pdf` (dated 2024-04-02 in the filename), 244 pp.
- Doc type: ご契約のしおり・約款 (policy booklet and policy conditions)
- URL: https://www.orixlife.co.jp/medical/cure_next/pdf/yakkan_cure_next_20240402.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 244 pp., text extracted; the
  narrative and tabular pages extracted cleanly, the diagram captions and several 別表
  (appendix) pages are image-only and did not extract)
- Key content: 支払事由 definitions for 疾病入院給付金 / 災害入院給付金 / 手術給付金 /
  女性入院給付金; the excluded-surgery list; the 60-days-between-radiation rule; the 181-day rule
  worked through examples; 七大生活習慣病入院給付特則 (三大疾病無制限型 / 七大疾病無制限型);
  保険料の払込免除.

### S3 — オリックス生命, 商品ページ「医療保険CURE Next[キュア・ネクスト]」
- Publisher: オリックス生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.orixlife.co.jp/medical/cure_next/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched with a browser User-Agent and converted to
  text)
- Key content: 契約年齢 0歳〜80歳; a published 月払保険料 table by age and sex; the per-case cost
  of 陽子線治療 / 重粒子線治療 attributed to a 厚生労働省 先進医療会議 report; the statement that
  日帰り入院 and short stays are covered; the 手術給付金 20倍/5倍 multiples.

### S4 — アフラック, 「ちゃんと応える医療保険EVER ご契約のしおり・約款」
- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: ご契約のしおり・約款, 「ちゃんと応える医療保険EVER」 (正式名称 医療保険〔無解約払戻金〕),
  file `ever_77836200_77841700.pdf`, 221 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.aflac.co.jp/yakkan/pdf/ever_77836200_77841700.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 221 pp., text extracted and read;
  a few illustration captions are image-only)
- Key content: 支払限度の型 table (60日型 / 120日型, 通算1,095日); the **five-day minimum**
  payment rule; 手術給付金 at 10倍 / 5倍 / 40倍 (重大手術); 放射線治療給付金 at 10倍; the full
  免責事由 list; the 180-day one-hospitalization rule; the two-year rule on pre-inception
  disease; grace period; 復活 within one year; 前納 mechanics.

### S5 — アフラック, 「医療保険に付加する特約 ご契約のしおり・約款」 (総合先進医療特約〔2012〕 ほか)
- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款 for the riders attachable to the medical policy
  (ケガの特約, 総合先進医療特約〔2012〕, 入院一時金特約, 通院特約, 女性疾病入院特約,
  三大疾病無制限型長期入院特約 ほか), file `kega_senshin_iryo_77978800.pdf`, 280 pp.
- Doc type: ご契約のしおり・約款 (rider booklet)
- URL: https://www.aflac.co.jp/static/yakkan/koushin/pdf/kega_senshin_iryo_77978800.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 280 pp., text extracted and read)
- Key content: 総合先進医療特約〔2012〕 — benefit equals the 技術料 the insured actually bore,
  通算2,000万円 across all policy periods, rider terminates on reaching the cap, one such rider
  per insured; the rider 免責事由 list.

### S6 — ライフネット生命, 「終身医療保険（無配当・無解約返戻金型）（2019）ご契約のしおり・約款」
- Publisher: ライフネット生命保険株式会社 (LIFENET INSURANCE COMPANY)
- Document: ご契約のしおり・約款, 終身医療保険（無配当・無解約返戻金型）（2019）, edition dated
  2026年6月, booklet code LN_BB_GAP-25, 65 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_latest.pdf
  (redirects to https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_20260601.pdf)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 65 pp., text extracted and read)
- Key content: 契約年齢 18–80; the six 入院給付金日額 options; the five-day minimum payment rule;
  1入院60日 / 通算1,095日 with the 180-day rule; 3大生活習慣病 unlimited-days course;
  手術給付金 10倍/5倍; がん治療給付金 at 100倍; 先進医療給付金 通算2,000万円 plus a
  先進医療見舞給付金 of ¥100,000; 保険料払込期間 options; 解約返戻金 = 10 × 日額 after a short
  pay period completes; **no 復活**; the statement that underwriting uses the 厚生労働省
  「患者調査」 受療率 by prefecture.

### S7 — ライフネット生命, 「定期医療保険（無配当・無解約返戻金型）ご契約のしおり・約款」
- Publisher: ライフネット生命保険株式会社
- Document: ご契約のしおり・約款, 定期医療保険（無配当・無解約返戻金型）, edition dated
  2024年11月, booklet code LN_BB_CXD-170, 65 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_teiki_latest.pdf
  (redirects to https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_teiki_20241125.pdf)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 65 pp., text extracted and read)
- Key content: the **定期 (term) medical** chassis — 契約年齢 18–70, automatic renewal, renewal
  age limits, and the fact that 通算1,095日 and the 先進医療 2,000万円 cap run **across renewals**;
  the treatment of a hospitalization in progress at the end of a policy term.

### S8 — ライフネット生命, 商品ページ「終身医療保険」
- Publisher: ライフネット生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.lifenet-seimei.co.jp/product/medical/whole-life-medical/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched with a browser User-Agent and converted to
  text; the premium table was read from the raw page text, not from a summary)
- Key content: a complete published **月額保険料 scale by age and sex** for a fixed benefit
  specification, rates as at 2026-06-01; the "premiums never rise" statement; confirmation that
  there is no 復活.

### S9 — メットライフ生命, 「終身医療保障保険（無解約返戻金型）ご契約のしおり・約款」 (マイ フレキシィ)
- Publisher: メットライフ生命保険株式会社 (MetLife Insurance K.K.)
- Document: ご契約のしおり・約款, 終身医療保障保険（無解約返戻金型）引受基準緩和特則付
  (brand 「マイ フレキシィ」), file `f5wl_20251202.pdf` (2025-12-02 edition), 515 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.metlife.co.jp/content/dam/metlifecom/jp/corp/pdf/yakkan/provision/f5wl/f5wl_20251202.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 515 pp., text extracted and read in
  the relevant ranges)
- Key content: the **three 保険契約の型** (入院日数連動型 / 短期入院一時金型 / 入院一時金型) with
  their payment formulas; 支払限度の型 60日 / 120日 / 730日 with a 通算 of 1,000日; the rule that
  all hospitalizations count as one **regardless of cause**; the day-count conventions that map a
  一時金 onto the day limits (10 days and 20 days); 手術総合特約 Ⅰ型/Ⅱ型 multiples;
  先進医療特約 (10-year renewable) with 通算2,000万円 and a 先進医療支援給付金 of 20% capped at
  ¥1,000,000 per 療養; 健康サポート特則; a **published specimen premium** for a named age/sex and
  specification; 保険料払込期間満了後死亡保険金; grace and 復活 within one year.

### S10 — アクサ生命（アクサのネット完結保険）, 「定期医療 約款／重要事項説明書／ご契約のしおり」
- Publisher: アクサ生命保険株式会社 (AXA Life Insurance Co., Ltd.; the booklet is branded
  アクサのネット完結保険, formerly アクサダイレクト生命)
- Document: 約款／重要事項説明書／ご契約のしおり, 医療保険（定期型）, Form No. AX-… (the form
  number digits did not extract), 85 pp.
- Doc type: 重要事項説明書 + ご契約のしおり + 約款 in one booklet
- URL: https://www.axa-direct-life.co.jp/pdf/yakkan_m.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 85 pp., text extracted and read;
  the cover page and one logo block are image/CID and did not extract, including the form-number
  digits and the edition month)
- Key content: 契約年齢 20–69, 保険期間・保険料払込期間 10年, renewal to age 80 with a
  short-final-term rule; 1入院60日 / 通算1,095日 across renewals; 手術給付金 **flat 10倍,
  in-hospital only** — no outpatient surgery benefit; a named list of surgeries excluded for the
  first year and a named list excluded permanently; the verbatim definition of 入院; the
  180-day one-hospitalization rule stated separately for 疾病 and 災害; 入院時一時金給付特約
  capped at two payments per policy year; grace period; **復活 within three years**;
  告知義務違反 contestability of two years; the option to convert to a 終身医療保険 at term end.

### S11 — SOMPOひまわり生命, 「健康をサポートする医療保険 健康のお守り」 パンフレット
- Publisher: SOMPOひまわり生命保険株式会社
- Document: パンフレット (product brochure), file `suport_omamori_health.pdf`, 23 pp.
- Doc type: 商品パンフレット
- URL: https://www.himawari-life.co.jp/-/media/himawari/files/product/pamphlet/suport_omamori_health.pdf?la=ja-JP
- Accessed: 2026-08-20. Retrieved: **NO** (HTTP 200, 23-page PDF downloaded successfully, but the
  file uses non-embedded CID-keyed fonts throughout and text extraction returned mojibake for
  essentially every substantive line; the booklet page
  https://www.himawari-life.co.jp/product/suport_omamori_health/booklet/ exposes only this one
  PDF link — the ご契約のしおり・約款 is behind a "Web約款" application, not a static file)
- Key content: **not readable**. Facts attributed to this carrier below (40日/60日/120日 choice of
  1入院 limit, 通算1,000日, 手術給付金 at 40/20/10/5倍) come from a search-result snippet only and
  are tagged [unverified].

### S12 — 東京海上日動あんしん生命, 「メディカルKit R」 重要事項説明書 兼 パンフレット
- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: 医療総合保険（基本保障・無解約返戻金型）健康還付特則付加［無配当］ 重要事項説明書
  兼 パンフレット, file `kitr3_pamphlet.pdf`, 14 pp.
- Doc type: 重要事項説明書 兼 パンフレット
- URL: https://www.tmn-anshin.co.jp/bk/kitr3/pdf/kitr3_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: **NO** (HTTP 200, 14-page PDF downloaded, text extraction
  returned mojibake — non-embedded CID fonts; a second candidate,
  https://www.bk.mufg.jp/sonaeru/hoken/syusin/pdf/tmn_medical_kit.pdf, 12 pp., downloaded and
  failed extraction in the same way)
- Key content: **not readable**. The 健康還付特則 (a premium-refund-at-a-stated-age feature on a
  medical chassis) is therefore recorded as a design that exists in the market but whose terms are
  [unverified] here.

---

## Regulatory and actuarial references

### R1 — 保険業法 第3条 (免許 — the statutory definition of 第三分野)
- Publisher: e-Gov 法令検索 (デジタル庁) — 保険業法, 平成七年法律第百五号
- Doc type: statute
- URL: https://laws.e-gov.go.jp/law/407AC0000000105 (article text retrieved through the e-Gov law
  API endpoint https://laws.e-gov.go.jp/api/1/lawdata/407AC0000000105)
- Accessed: 2026-08-20. Retrieved: YES via the API (the HTML page at `laws.e-gov.go.jp/law/...`
  is JavaScript-rendered and returned only chrome to a plain fetcher; the API returned a 3.7 MB
  UTF-8 XML document from which Article 3 was extracted verbatim)
- Content: 第3条第4項第2号 — the 生命保険業免許 covers, in addition to life contracts, insurance
  paying a fixed sum or indemnifying loss on: イ 人が疾病にかかったこと; ロ 傷害を受けたこと
  又は疾病にかかったことを原因とする人の状態; ハ 傷害を受けたことを直接の原因とする人の死亡;
  ニ イ又はロに類するものとして内閣府令で定めるもの（人の死亡を除く）; ホ イ、ロ又はニに関し
  治療を受けたこと. 第3条第5項第2号 makes the identical class available to 損害保険業免許
  holders — which is what makes it the "third sector", writable under either licence.

### R2 — 保険業法施行規則 第68条・第69条 (標準責任準備金の対象契約 / 生命保険会社の責任準備金)
- Publisher: e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- Doc type: ministerial ordinance
- URL: https://laws.e-gov.go.jp/law/408M50000040005 (retrieved through
  https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005)
- Accessed: 2026-08-20. Retrieved: YES via the API (30.2 MB XML; Articles 68 and 69 extracted
  verbatim)
- Content: 第68条 defines which contracts fall under 標準責任準備金 (法第116条第2項), excluding
  unit-linked contracts, contracts with no 保険料積立金, and contracts whose 約款 lets the insurer
  vary the 予定利率. 第69条第1項 sets the reserve components: 保険料積立金, 未経過保険料,
  払戻積立金, 危険準備金. 第69条第4項第2号 requires 平準純保険料式 (net level premium) as the floor
  for non-標準責任準備金 contracts. **第69条第6項第1号の2 requires a separately identified
  「第三分野保険の保険リスクに備える危険準備金」** — the contingency reserve specific to this
  product class. 第69条第7項 makes its accumulation and release subject to standards set by the
  金融庁長官.

### R3 — 金融庁, 「保険会社向けの総合的な監督指針」 II－2－1－2 / II－2－1－4 (責任準備金)
- Publisher: 金融庁 (Financial Services Agency)
- Doc type: supervisory guideline
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES
- Content: II－2－1－2(6) — 第三分野保険のストレステストを使用しての危険準備金の算出にあたっては
  **平成10年6月8日大蔵省告示第231号** の規定に基づき算出を行うものとし、算出部門と内部監査部門
  との相互牽制機能を確保する態勢が求められる. II－2－1－2(7) — the ストレステスト and the
  負債十分性テスト must appropriately reflect the uncertainty that 保険事故発生率 deteriorates, and
  are run per contract grouping sharing the same 基礎率. II－2－1－4(2) — disclosure must make the
  reasonableness of the 危険発生率等の設定水準 used in the 負債十分性テスト and ストレステスト
  clear. II－2－1－2 also covers チルメル式責任準備金 where special circumstances exist.

### R4 — 日本アクチュアリー会, 「標準生命表2018」 (数値表)
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — 生保標準生命表2018（死亡保険用）男/女 and
  **第三分野標準生命表2018 男/女**
- Doc type: industry standard table (statutory valuation table)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
  (index page: https://www.actuaries.jp/lib/standard-life-table/index2018.html)
- Accessed: 2026-08-20. Retrieved: YES (5-page PDF downloaded, full numeric tables extracted —
  age, lx, dx, qx, ex for every integral age)
- Content: the table is **public and machine-readable**, which is the sharp contrast with the UK
  CMI position. The index page states that 日本アクチュアリー会 is the 指定法人 under 保険業法
  第122条の2第1項 and is commissioned by the 金融庁 under 第122条の2第2項第3号 to prepare the
  標準生命表; the 改定案 was published 2017-03-31, resolved 2017-05-10, submitted to the 金融庁長官
  2017-05-11, and 標準生命表2018 applies from April 2018 after the 告示 amendment.

### R5 — 日本アクチュアリー会, 「標準生命表2018の作成概要」
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料－①〜⑤)
- Doc type: technical note accompanying the standard table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (6-page PDF downloaded, text extracted and read)
- Content: 資料－④ documents how 第三分野標準生命表2018 was built — 基礎データ is the
  第21回生命表 (2010) national life table (not insured experience, unlike the 2007 table);
  mortality improvement of 2.5% p.a. for five years then 1.0% p.a. for three years was applied;
  a 数学的危険論 margin holds the probability that experience exceeds the projection to about
  2.28% (2σ), floored at 70% and capped at 85% of the unadjusted rate, assuming a 1,000,000-policy
  portfolio; the table's 平均寿命 is 83.47 (male) / 89.59 (female) and the terminal age is 116/118;
  and — critical for a medical model — **第三分野標準生命表2018 は高度障害を含まない死亡率である**
  (the 2007 table did include 高度障害).

### R6 — 厚生労働省, 「令和5年（2023）患者調査の概況」
- Publisher: 厚生労働省 (Ministry of Health, Labour and Welfare)
- Document: 令和5年（2023）患者調査の概況, 33 pp.
- Doc type: official statistics summary (基幹統計)
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/kanjya.pdf
  (index: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/index.html)
- Accessed: 2026-08-20. Retrieved: YES (33-page PDF downloaded, text extracted; the statistical
  tables 4–7 extracted as machine-readable numbers, the figures 7 and 8 are charts whose data
  labels extracted but whose axes did not)
- Content: definitions (受療率（人口10万対）＝推計患者数／推計人口×100,000), national 受療率 and
  退院患者平均在院日数 by age band and by 傷病大分類 — see §16 below for the extracted values.

### R7 — e-Stat 政府統計の総合窓口, 「患者調査 令和5年患者調査 全国編」 統計表
- Publisher: e-Stat 政府統計の総合窓口 (host) / 厚生労働省 (statistic owner), 政府統計コード 00450022
- Doc type: downloadable statistical tables (CSV / Excel)
- URL: https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450022&tstat=000001224321&cycle=7&tclass1=000001224322&layout=datalist&tclass2val=0
- Accessed: 2026-08-20. Retrieved: YES (listing page fetched with a browser User-Agent and the
  full table index read; individual CSV files were **not** downloaded in this session)
- Content: the table inventory that makes this product modellable from public data. The tables
  that matter, by their e-Stat table numbers:
  - **Z69** 入院受療率（人口10万対），性・年齢階級（５歳）× 傷病分類別 — the incidence proxy.
  - **Z111** 推計退院患者数，在院期間（32区分）× 性・年齢階級（５歳）× 病院－一般診療所・病床の種類別
    — the **length-of-stay distribution in 32 bands** by five-year age band, i.e. exactly what a
    60日 / 120日 per-hospitalization cap needs.
  - **Z114 / Z115 / Z116 / Z117** the same 32-band distribution crossed with 傷病大/中/小分類.
  - **Z120** 在院期間（32区分）別推計退院患者数構成割合（累積），傷病中分類別 — the cumulative
    distribution, already computed.
  - **Z121 / Z122 / Z123** 退院患者平均在院日数，性・年齢階級（５歳）× 傷病分類 × 病院－一般診療所別.
  - **Z125 / Z126** 退院患者平均在院日数 × 手術の有無別 — a public surgery-rate proxy.
  - **Z83 / Z85 / Z86 / Z87** 推計退院患者数 × 過去の入院の有無・再入院までの期間 — the empirical
    basis for the 180-day re-admission rule.
  - **Z4-4 / Z5-2 / Z7-3** the long time series of 受療率 and 平均在院日数.

### R8 — 厚生労働省, 「令和6年簡易生命表の概況」
- Publisher: 厚生労働省
- Document: 令和6年簡易生命表の概況 (基幹統計), summary section `life24-01.pdf` (1 p.) plus
  per-sex tables and Excel files
- Doc type: official statistics (national life table)
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/life/life24/index.html
  (summary PDF: https://www.mhlw.go.jp/toukei/saikin/hw/life/life24/dl/life24-01.pdf)
- Accessed: 2026-08-20. Retrieved: YES for the index page and `life24-01.pdf`; the numeric
  per-sex tables (`life24-12.xlsx`, `life24-13.xlsx`) were **not** downloaded
- Content: 簡易生命表 is produced annually from 人口推計 and the 人口動態統計月報年計（概数）;
  完全生命表 is produced every five years from the 国勢調査 確定数 and 人口動態統計 確定数; the
  令和6年 table covers 2024-01-01 to 2024-12-31. The published downloads include Excel
  (`.xlsx`) life-table files, so a national mortality basis is directly obtainable.

### R9 — 厚生労働省 先進医療会議, 「令和5年6月30日時点で実施されていた先進医療の実績報告について」
- Publisher: 厚生労働省 (先進医療会議 資料 先－2－1 および参考資料1)
- Document: 令和5年度（令和4年7月1日〜令和5年6月30日）実績報告, 13 pp.
- Doc type: regulatory committee statistical report
- URL: https://www.mhlw.go.jp/content/12404000/001178108.pdf
- Accessed: 2026-08-20. Retrieved: YES (13-page PDF downloaded, per-technology tables extracted
  as machine-readable numbers)
- Content: aggregate and per-technology counts and money for every 先進医療 technology — the
  public basis for pricing a 先進医療特約. Figures in §10 below.

### R10 — 国税庁, タックスアンサー No.1140 「生命保険料控除」
- Publisher: 国税庁 (National Tax Agency)
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the 新契約 (contracts concluded on or after 2012-01-01) income-tax deduction bands:
  annual premium ≤ ¥20,000 → the whole amount; ¥20,000–¥40,000 → premium × 1/2 + ¥10,000;
  ¥40,000–¥80,000 → premium × 1/4 + ¥20,000; over ¥80,000 → a flat ¥40,000. Each of the three
  baskets is capped at ¥40,000 and the total 生命保険料控除 is capped at **¥120,000**.

### R11 — 国税庁, タックスアンサー No.1141 「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the three baskets — 一般の生命保険料, **介護医療保険料**, 個人年金保険料 — and the
  definition that the 介護医療保険料 basket covers contracts paying on 医療費支払事由; the
  新制度 applies to contracts concluded on or after 2012-01-01. A 医療保険 sits in the
  介護医療保険料 basket. (The 住民税 caps are not stated on this page — see gaps.)

### R12 — 生命保険文化センター, 「2025（令和7）年度 生活保障に関する調査（速報版）」
- Publisher: 公益財団法人 生命保険文化センター (Japan Institute of Life Insurance)
- Document: プレスリリース, 2025-10-23; survey fieldwork 2025-04-05 to 2025-06-11; n = 4,837
- Doc type: industry survey (press release)
- URL: https://www.jili.or.jp/press/2025/10212.html
- Accessed: 2026-08-20. Retrieved: YES
- Content: 疾病入院給付金の支払われる生命保険の加入率 **65.6%**; the average enrolled amount is
  **¥8,500 per day** (and ¥194,000 as a lump sum) against a self-assessed need of ¥10,100 per day
  (and ¥240,000). Also 民間の介護保険・介護特約の加入率 10.4%.

### R13 — 厚生労働省, 「医療給付実態調査」 (統計ページ)
- Publisher: 厚生労働省 保険局
- Doc type: official statistics landing page (政府統計コード 00450389)
- URL: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/iryouhoken/database/zenpan/iryoukyufu.html
- Accessed: 2026-08-20. Retrieved: YES (page fetched; it is largely a pointer to e-Stat)
- Content: the survey is compiled by fiscal year and published around the end of the following
  fiscal year; the statistical tables (件数・日数（回数）・点数（金額） by 疾病分類 × 診療種類 ×
  年齢階級, by insurance scheme) live on e-Stat. Useful as a claims-cost cross-check on 患者調査,
  but the tables themselves were **not** downloaded in this session, and a search snippet stating
  that the survey was discontinued after 令和5年度 in favour of the 高齢者医療確保法 anonymised
  database could **not** be confirmed on this page — see gaps.

---

## Fact extraction

### 1. Product architecture — what the third-sector chassis is

- The product class exists because 保険業法第3条第4項第2号 / 第5項第2号 carve out insurance on
  「人が疾病にかかったこと」 and 「傷害を受けたこと又は疾病にかかったことを原因とする人の状態」,
  writable under either a life or a non-life licence — the 第三分野 [R1].
- Every carrier examined writes the same main contract shape: a 主契約 paying
  疾病入院給付金 and 災害入院給付金 as 入院給付金日額 × 入院日数, plus a 手術給付金 as a multiple
  of the same 日額, with 特約 (riders) bolted on [S1] [S4] [S6] [S9] [S10].
- The main contract is normally **無解約返戻金型 / 無解約払戻金型** (no surrender value) — this is
  stated in the product's formal name at four carriers: 「無配当 無解約払戻金型医療保険（2022）」
  [S2], 「医療保険〔無解約払戻金〕」 [S4], 「終身医療保険（無配当・無解約返戻金型）（2019）」 [S6],
  「終身医療保障保険（無解約返戻金型）」 [S9].
- 終身 (whole-of-life) and 定期 (term, renewable) chassis both exist and are sold as separate
  products by the same carrier: one carrier sells both a 終身医療保険 [S6] and a
  定期医療保険 [S7]; another's 医療保険（定期型） is 10-year renewable with a contractual
  conversion into a 終身医療保険 at the end of a term [S10].
- 死亡保険金 is **not** part of the main contract on any of the five carriers' medical products;
  where it exists it is a 特約 (a 終身保険特約（無解約払戻金型） paid as 入院給付金日額 × 給付倍率
  — the illustrated case is 給付倍率200倍 = ¥2,000,000 on a ¥10,000 daily amount) [S1], or a
  payment-period-completion benefit (a 保険料払込期間満了後死亡保険金 = 10 × 入院給付金日額,
  payable only under a 短期払) [S9].

### 2. Issue ages, policy term, premium-paying period, premium modes

- 契約年齢 (issue age) ranges observed:
  - **0歳〜80歳** [S3].
  - **18歳以上、80歳以下** (終身) [S6]; **18歳以上、70歳以下** (定期) [S7].
  - **満20歳〜満69歳** (定期型) [S10].
  - Not published in the retrieved booklet at one carrier [unverified]; that booklet's specimen
    contract is 契約年齢40歳 男性 [S9].
- 契約年齢 is defined as the attained age at the 契約日 with the fractional year discarded, rising
  by one at each 年単位の契約応当日 — stated explicitly with the example 「24歳7か月の被保険者の
  契約年齢は24歳」 [S4], and the identical convention and example appear at another carrier [S10].
  This is **満年齢方式**; note that 第三分野標準生命表2018 was constructed on a **保険年齢方式**
  basis [R5], so a valuation model and a pricing model can differ by half a year of age.
- 保険期間: 終身 (whole of life) for the 終身 products [S1] [S6] [S9]; **10年** with automatic
  renewal for the 定期型, renewable to a maximum age of 80, and where a renewal would run
  past 80 the term is shortened in whole years so that it ends at 80 [S10]. The other 定期医療保険
  renews while the renewal-date age is ≤ 89 and shortens the final term so it expires at age 90
  [S7].
- 保険料払込期間: 終身払 (whole-life pay) or 短期払 (a pay-to-age). One carrier offers
  終身 / 60歳まで / 65歳まで [S6]; another offers 終身払 with a 短期払 option [S1]; a third
  distinguishes 全期払（終身） from 短期払 by the presence of the 保険料払込期間満了後死亡保険金
  [S9].
- 払込回数: 月払 / 半年払 / 年払 [S1] [S4]; one net-only product is **月払 only** as at its
  2024年4月 edition [S10]. 払込経路: 口座振替 / クレジットカード / 団体扱 / 振込 [S1] [S4].
- 前納 (advance payment) is available and discounted: 月払 contracts may prepay 6 or 12 months at
  a discount rate set by the company; 半年払/年払 contracts may prepay future premiums discounted
  at a company-set interest rate, the balance accumulating with interest and being applied at each
  contract anniversary [S4].
- 保険料 are **level for life** on the 終身 products and rise at each renewal on the 定期 products,
  recomputed at the renewal-date age and the renewal-date rate scale [S7] [S8] [S10].

### 3. 入院給付金 — the daily benefit and how it is paid

- 入院給付金日額 (daily hospitalization amount) is chosen at issue from a company-set menu. One
  carrier publishes the full menu: **¥3,000 / ¥5,000 / ¥8,000 / ¥10,000 / ¥12,000 / ¥15,000**,
  with ¥3,000 available only at issue age 66 and over [S6]. Two carriers' illustrated contracts
  use ¥10,000 [S1] [S9]; the two published premium tables use ¥5,000 [S3] [S8]. The market-average
  enrolled amount is **¥8,500 per day** [R12].
- The base payment rule is `入院給付金日額 × 入院日数` per hospitalization [S1] [S2] [S6] [S9]
  [S10].
- **A five-day minimum applies at two of the five carriers.** 「支払額 入院1回につき、
  入院給付金日額×入院日数 ただし、入院日数が5日以内の場合は、入院給付金日額×5」 for both
  疾病入院給付金 and 災害入院給付金 [S4]; another carrier uses the identical rule and states it
  covers 日帰り入院 [S6] [S7]. The other three pay actual days with **no** minimum [S1] [S2] [S9]
  [S10]. This is a first-order model choice: a five-day floor roughly doubles the expected payment
  on the modal short stay.
- 日帰り入院 (same-day admission and discharge) is covered: one carrier says so in terms
  (「日帰り入院を含む」) [S6] [S7]; another's 支払事由 is 「1日以上入院したとき」 [S9]; a third's
  product page says 「日帰り入院からの短期入院も保障します」 [S3].
- If the 日額 is reduced mid-stay, one carrier applies the amount in force on each day, except that
  the first five days use the amount in force at admission [S4].
- 疾病入院給付金 and 災害入院給付金 are **never paid concurrently** for the same day [S1] [S4]
  [S9] [S10]. Two carriers work the example: where 災害入院給付金 is being paid and a disease is
  diagnosed mid-stay, 疾病入院給付金 begins the day after the 災害入院給付金 period ends [S2] [S4].
- 災害入院給付金 requires the admission to begin within **180 days of the accident** [S1] [S4]
  [S9] [S10].
- If a disease is contracted mid-stay, the stay continues to be treated as caused by the original
  admitting disease [S4].
- **入院 is defined** verbatim at one carrier: 「医師による治療が必要であり、かつ、自宅等での治療が
  困難なため、病院または診療所に入り常に医師の管理下において治療に専念すること」 [S10]. Another
  defers to 約款別表7「入院」 [S2] (that appendix page is image-only and did not extract).
- One carrier excludes a specific admission type: no 疾病入院給付金等 where the admission was for
  睡眠時無呼吸 or suspicion of it and the diagnosis is not confirmed [S9].

### 4. 1入院の支払限度日数 and what counts as ONE hospitalization

- The per-hospitalization day limit is a **型 chosen at issue and never changeable afterwards**
  [S4] [S9].
- Observed menus:
  - **60日型 / 120日型** [S4] [S1].
  - **60日 only** — 終身 and 定期 at one carrier [S6] [S7], and the 定期型 at another [S10].
  - **60日型 / 120日型 / 730日型** [S9].
  - **40日 / 60日 / 120日** [unverified] (see [S11]: the document could not be read).
- **The 180-day re-admission rule.** Two hospitalizations are treated as one, their days
  aggregated against the per-hospitalization limit, unless the later one begins after the
  180-day window from the previous discharge. The carriers differ in the *cause* test and in the
  boundary arithmetic:
  - Two or more admissions count as one where 「それぞれの入院の原因が同一のとき」 もしくは
    「それぞれの入院の原因に医学上重要な関係がある」場合 (including concurrent causes); a new
    hospitalization begins on **the 181st day counting from the day after the last discharge
    inclusive** (for 災害入院, from the accident date) [S1] [S2].
  - Admissions count as one **regardless of whether the cause is the same**
    (「同一の疾病であるか否かにかかわらず」), with a new hospitalization recognised where it starts
    **after 180 days have elapsed** from the day after the last discharge, counting that day [S4].
  - Same-cause-or-medically-related test, new hospitalization after 180 days from the day after
    discharge [S6] [S7].
  - Cause-blind aggregation for both 疾病 and 災害 (「それらの入院が同一の原因であるか否かに
    かかわらず、1回の入院とみなします」), with the definition of a "new hospitalization" depending
    on the 保険契約の型 [S9].
  - Same-cause-or-medically-related test for 疾病入院, and for 災害入院 the test is the **same
    accident** plus admission within 180 days of the accident date [S10].
- Where the insurer treats admissions as one, the days of the later admissions are aggregated, and
  days beyond the per-hospitalization limit are simply not paid [S2].
- Riders can use a **different** one-hospitalization test from the main contract. One carrier's
  入院一時金特約 and 通院治療支援特約 both aggregate admissions 「入院の原因を問わず」 (cause-blind)
  even though the main contract's test is cause-based, with the same 181st-day reset [S1].

### 5. 通算支払限度日数 (the lifetime day cap)

- Observed values, and they are **not** uniform:
  - **1,095日** [S4], [S6], [S7], [S10].
  - **1,000日** [S1] [S2], [S9].
  - 1,000日 [unverified] ([S11] unreadable).
- The cap is applied **separately to 疾病入院給付金 and 災害入院給付金** in one carrier's table
  (each 1,095日) [S4] and in another's (each 1,000日) [S1].
- On the 定期 chassis the aggregate cap runs **across renewals**: 「保険期間（更新契約の保険期間を
  含みます）を通じて1,095日」 [S7], and the same at the other term carrier [S10]. The general
  principle for riders is stated as 「給付金の通算支払限度の規定を適用するときは、更新前の特約で
  既に支払われた給付金を通算します」 [S5].
- Exhausting the cap can **terminate cover**: if, during the premium-paying period, both
  疾病入院給付金等 and 災害入院給付金等 reach the 通算支払限度, 保険契約は消滅します [S9]. At
  another carrier the 入院一時金特約 and 通院治療支援特約 terminate when the main contract's
  1,000-day caps are both reached (except where the 七大生活習慣病入院給付特則 applies) [S1].
- A 一時金-type benefit is **converted into days** for limit purposes at one carrier: a
  短期疾病/災害入院一時金 consumes **10 days** of both the per-hospitalization and the aggregate
  limit regardless of actual days; a 疾病/災害入院一時金 (入院一時金型) consumes **20 days** of the
  aggregate limit [S9].

### 6. 生活習慣病 unlimited-days features (the standard limit-relaxation)

- One carrier sells three plans off one main contract via the 七大生活習慣病入院給付特則 [S1] [S2]:
  - **三大疾病無制限プラン** — for がん（悪性新生物・上皮内新生物）, 心疾患, 脳血管疾患 the
    per-hospitalization limit is **無制限** and those days are outside the 1,000-day aggregate;
    for the other four 七大生活習慣病 the per-hospitalization limit doubles (60日型 → 120日,
    120日型 → 180日); all other disease keeps 60/120.
  - **七大疾病無制限プラン** — all seven are 無制限 and outside the aggregate.
  - **no 特則** — a flat 60日 or 120日 with a 1,000-day aggregate.
- The 七大生活習慣病 are named: **がん（悪性新生物・上皮内新生物）, 心疾患, 脳血管疾患, 糖尿病,
  高血圧性疾患, 肝硬変, 慢性腎臓病**; the 三大疾病 are the first three [S1] [S2].
- The 特則 carries two mid-stay reclassification rules that a model must not smooth over: under
  三大疾病無制限型, a stay that starts for a non-七大 cause and during which treatment of a
  七大生活習慣病 **other than 高血圧症** begins is treated as a 七大 stay **from the admission
  date**; under 七大疾病無制限型, a mid-stay start of 高血圧症 treatment does **not** convert the
  stay [S1] [S2]. The 特則 can only be applied at issue and can never be cancelled [S2].
- Another carrier's おすすめコース (約款 types A2/F2) gives unlimited days for the 3大生活習慣病
  (がん（悪性新生物）, 心疾患, 脳血管疾患), explicitly excluding 上皮内新生物 and 異形成 from "がん"
  [S6].
- A third sells the equivalent as a separate rider, 三大疾病無制限型長期入院特約 [S5].

### 7. 手術給付金 — three structures, and they are not interchangeable

- **The trigger is the same everywhere and it is tied to the public system.** The covered set is
  the procedures listed as chargeable under 手術料 in the 公的医療保険制度's 医科診療報酬点数表,
  plus (usually) 放射線治療料-listed procedures, plus 骨髄移植術 chargeable under 輸血料, plus
  procedures that qualify as 先進医療 [S1] [S2] [S4] [S9] [S10]. Every carrier reserves the right
  to change 支払事由 prospectively, with 主務官庁 approval, if the 公的医療保険制度 is amended
  [S2] [S6].
- **The same seven-item exclusion list appears verbatim at four carriers**: 傷の処理（創傷処理、
  デブリードマン）; 切開術（皮膚、鼓膜）; 骨・関節の非観血的整復術・非観血的整復固定術・非観血的
  授動術; 抜歯; 異物除去（外耳、鼻腔内）; 鼻焼灼術（鼻粘膜、下甲介粘膜）; 魚の目・タコ切除術
  （鶏眼・胼胝切除術） [S2] [S4] [S6] [S10]. One of them adds 巻き爪手術（陥入爪手術） as a tenth
  permanently excluded item [S10].
- **The payment structures observed:**
  - **入院中 / 外来 two-tier multiple of the 日額** — **20倍 / 5倍**, payment count unlimited
    [S1] [S3]; **10倍 / 5倍** [S6] [S7].
  - **Three-tier with a 重大手術 category** — 入院中の手術 **10倍**, それ以外 **5倍**,
    重大手術 **40倍** [S4]. 重大手術 is defined by an enumerated list: 開頭・開胸・開腹手術 and
    四肢切断術 for 悪性新生物; 脊髄腫瘍摘出術, 頭蓋内腫瘍開頭摘出術, 縦隔腫瘍開胸摘出術;
    open procedures on 心臓・大動脈・大静脈・肺動脈・冠動脈; and transplants of 心臓・肺・肝臓・
    膵臓・腎臓 performed in Japan under the 臓器移植法, donor side excluded — with 腹腔鏡・胸腔鏡・
    穿頭 excluded from the category [S4].
  - **A separate rider with its own 基準額 and two grades** — a 手術総合特約 paying
    入院手術給付金 Ⅰ型 **手術給付金基準額 × 20**, Ⅱ型 **× 10**; 外来手術給付金 **× 5** in both;
    unlimited payment count. The 手術給付金基準額 is set independently of the 入院給付金日額 (the
    specimen contract sets both to ¥10,000) [S9].
  - **Flat, in-hospital only** — **入院給付金日額 × 10**, and 入院外手術 is not covered at all
    [S10]. Because the multiple does not vary, this is the market's 一律型 end of the range.
  - 40/20/10/5倍 [unverified] ([S11] unreadable).
- **Frequency limits inside the surgery benefit** (these bind and are easy to miss):
  - Where several surgeries are performed on the same day, only the single highest-paying one is
    paid [S1] [S2] [S10]; where one surgery spans two or more days, its start date is the date of
    surgery [S2].
  - Where a surgery's 手術料 is charged per day, only the first day is paid [S1] [S2].
  - Where the 診療報酬点数表 charges 手術料 only once for a connected course of treatment, only
    the highest-paying single instance is paid [S2]; another carrier expresses the same rule as a
    **60-day lockout** after a paid surgery of that kind [S10].
  - 放射線照射 or 温熱療法 repeated: payment is limited to **once in 60 days** [S1] [S2] [S9]
    [S10]; one carrier phrases it as no payment for radiation received within 60 days of a paid
    one [S6].
  - Surgery received during a stay for which 入院給付金 is no longer payable because the day limit
    is exhausted: one carrier **treats it as an in-hospital surgery** and pays the higher multiple
    [S4]; another **does not pay the surgery benefit at all** [S10]. This is a genuine
    contradiction between carriers and must be a modelled switch.
- **Waiting periods inside the surgery benefit.** 骨髄幹細胞の採取術 (bone-marrow donation) is
  covered only from **one year** after 責任開始日 at four carriers [S1] [S2] [S6] [S9] [S10], and
  at one of them it is additionally capped at **2 payments** over the whole policy period including
  renewals [S10]; 自家移植 (donor and recipient the same person) is excluded [S2] [S9]. One carrier
  additionally excludes for the **first policy year** a named list of eight elective procedures —
  痔瘻・痔核・脱肛手術, 子宮関係手術（子宮筋腫摘出術、子宮ポリープ切除術、流産手術、子宮内容除去術）,
  脊髄硬膜内外手術, 副鼻腔炎手術, 白内障・水晶体観血手術, ファイバースコープでの大腸・胃に対する
  切除術, 眼瞼下垂症手術, 扁桃腺摘出術 — with the exclusion **not** re-imposed at renewal [S10].

### 8. 放射線治療給付金

- One carrier pays a **separate 放射線治療給付金 of 入院給付金日額 × 10** for procedures listed
  under 放射線治療料 in the 医科診療報酬点数表 (including 電磁波温熱療法, excluding 血液照射),
  with 放射線照射 limited to 体外照射・組織内照射・腔内照射 [S4].
- Another pays 放射線治療給付金 inside the 手術総合特約 at **基準額 × 20 (Ⅰ型) / × 10 (Ⅱ型)**,
  unlimited in count but at most once per 60 days [S9].
- The remaining three do **not** have a separate radiation benefit — radiation is folded into
  手術給付金 through the 放射線治療料 limb of the trigger, subject to the 60-day rule [S1] [S2]
  [S6] [S10].

### 9. 一時金 benefits layered on the daily benefit

- **入院一時金 / 短期入院一時金** — the market's answer to shortening hospital stays:
  - 入院一時金特約: **¥100,000 per hospitalization**, one payment per hospitalization,
    **通算50回**, cause-blind aggregation with a 181st-day reset; terminates on reaching 50
    payments or when the main contract's 1,000-day caps are reached [S1].
  - One carrier makes it a **main-contract 型**: 短期入院一時金型 pays **日額 × 10** on any
    admission of one day or more, then pays 日額 × (入院日数 − 10) from day 11; 入院一時金型 pays
    **日額 × 20** per hospitalization and nothing per day [S9].
  - 入院時一時金給付特約: a fixed 入院時一時金額 per hospitalization, 疾病 and 災害 combined
    limited to **2 payments per policy year** (a year running anniversary to anniversary) [S10].
- **通院** — one carrier does not sell a general 通院給付金 on this chassis; it sells
  通院治療支援特約（退院時一時金給付型）, paying a lump sum on surviving discharge from a paid
  admission, once per discharge, 通算50回 [S1]. A cancer-specific 通院 benefit exists as
  がん通院特約 (日額 × 通院日数, capped at 60 days per 通院治療期間 for post-discharge visits and
  unlimited for treatment-type visits) [S1]. Another sells a general 通院特約 [S5].
- **三大疾病/特定三疾病 一時金** — a 特定三疾病一時金特約 pays a lump sum for each of
  がん / 心疾患 / 脳血管疾患, unlimited in count but **at most once per year each**; the cancer limb
  starts only from the **がん責任開始日 = the 91st day counting from 責任開始日**, while the
  心疾患 and 脳血管疾患 limbs start at 責任開始日 [S1].
- **がん治療給付金** — one carrier pays **日額 × 100** on first cancer diagnosis after a 90-day
  wait, and again for cancer treatment at least one year after the previous payment, capped at
  **5 payments** over the policy period [S6].

### 10. 先進医療特約 (advanced-medicine rider) — the most widely sold rider on this chassis

- Structure is uniform: the rider reimburses the **技術料 of a 厚生労働大臣-designated 先進医療**
  in full, because that fee is entirely outside the 公的医療保険制度, subject to a lifetime
  aggregate cap.
- **The cap is ¥20,000,000 (通算2,000万円) at every carrier examined** [S1] [S3], [S5], [S6] [S7],
  [S9]. Reaching the cap **terminates the rider** [S1] [S5].
- Carriers add a cash top-up alongside the reimbursement, and its shape varies:
  - 先進医療一時金: **10% of the 先進医療給付金**, capped at **¥500,000 per 療養** [S1].
  - 先進医療支援給付金: **20% of the 技術料**, capped at **¥1,000,000 per 療養** [S9].
  - 先進医療見舞給付金: a flat **¥100,000 per 療養**, with no second payment for a 療養 received
    within 60 days of a paid one [S6].
  - One carrier pays reimbursement only, and only of the amount the insured actually bore
    (「先進医療にかかる技術料のうち被保険者が負担した費用と同額」) [S5].
- A series of treatments under the same 先進医療 counts as **one 療養** [S1] [S6] [S9].
- Cover is determined at the date of treatment, not at issue: if the technology, the institution
  or the indication has since left the 先進医療 list, nothing is paid [S1] [S5].
- 患者申出療養 is **not** 先進医療 and is excluded [S6].
- One carrier imposes a **two-year waiting period on 白内障** treatment for both the
  先進医療給付金 and the 見舞給付金 [S6].
- Only one 先進医療 rider per insured is allowed across the carrier's own policies [S1] [S5].
- **The rider is often term, not whole-of-life.** One carrier's 先進医療特約 has a **10-year
  term with automatic renewal, no renewal limit**, and its premium is recalculated at each renewal
  at the then-current age and rate [S9]; the aggregate cap is applied treating pre- and
  post-renewal periods as continuous [S9], the same principle another carrier applies on a rider
  conversion [S5].
- **Published premium**: a specimen contract at 契約年齢40歳男性 shows the 先進医療特約 premium as
  **¥114 per month** out of a total monthly premium of ¥5,874 [S9] — i.e. under 2% of the premium
  buys a ¥20,000,000 cap. That ratio is the single most useful published data point for
  calibrating 先進医療 incidence.
- **The public claim experience behind it** [R9], for 令和5年度 (令和4年7月1日〜令和5年6月30日):
  - Overall: 81 technologies, 477 institutions, **144,282 patients**, 総金額 約765.1億円, of which
    保険外併用療養費（保険診療分） 約663.9億円 and **先進医療費用の総額 約101.2億円** (13.2% of the
    total).
  - 先進医療A alone: 28 technologies, 389 institutions, 142,653 patients, 先進医療総額
    **¥9,655,654,885** — an average of about **¥67,700 per case**, but the distribution is
    dominated by high-volume, low-cost fertility technologies added in 令和4年4月.
  - The tail that drives the ¥20,000,000 cap: **陽子線治療** — 824 cases, 先進医療総額
    **¥2,191,024,100** (≈ ¥2,660,000 per case), 平均入院期間 15.6日, 17 institutions;
    **重粒子線治療** — 462 cases, 先進医療総額 **¥1,448,673,000** (≈ ¥3,140,000 per case),
    平均入院期間 4.2日, 7 institutions [R9].
  - One carrier quotes the same two technologies at **約267万円** and **約314万円 per case**,
    citing 「厚生労働省 第138回先進医療会議資料 令和6年度実績報告（令和5年7月1日〜令和6年6月30日）」
    [S3] — consistent with the 令和5年度 figures computed above, so the per-case cost is stable
    year on year.
  - Volume by technology, for scale: タイムラプス撮像法による受精卵・胚培養 79,700 cases,
    子宮内膜刺激術 19,701 cases, 強拡大顕微鏡を用いた形態学的精子選択術 12,565 cases [R9]. A model
    calibrated on the aggregate average will badly misstate a rider whose exposure is adult
    policyholders.

### 11. 保険料払込免除 (waiver of premium) and the 三大疾病 variant

- The base waiver is disability-triggered, not sickness-triggered: 高度障害状態 from any cause, or
  a listed 身体障害の状態 arising from an 不慮の事故 within **180 days** of the accident [S1] [S2]
  [S10]. One carrier words it as 所定の身体障害の状態 during the premium-paying period [S9];
  another as 約款所定の障害状態 [S6].
- Waiver does **not** apply after the premium-paying period has run out, and is excluded where the
  condition arises from the policyholder's or insured's 故意・重大な過失, the insured's criminal
  act, 精神障害, 泥酔, driving without a licence, or drink-driving [S2].
- **特定三疾病保険料払込免除特則** — an optional waiver extension, with explicitly different
  triggers per disease [S1]:
  - がん: first diagnosis on or after the **がん責任開始日 = the 91st day from 責任開始日**, the
    diagnosis date being the date the confirming test was performed, not the date the doctor
    communicated it.
  - 心疾患: 急性心筋梗塞 — any admission for treatment, or a listed surgery; other 心疾患 — a
    **continuous stay of 10 days or more**, or a listed surgery.
  - 脳血管疾患: 脳卒中 — any admission for treatment, or a listed surgery; other 脳血管疾患 — a
    continuous stay of 10 days or more, or a listed surgery.
- The 10-day continuous-stay condition for the non-acute limbs is a materially different trigger
  from a diagnosis trigger and must be modelled off the length-of-stay distribution, not off an
  incidence rate.

### 12. 解約返戻金, 配当, 契約者貸付, 自動振替貸付

- The main contract has **no surrender value during the premium-paying period** at every carrier
  examined [S1] [S6] [S9] [S10].
- Where a **短期払** is chosen, a small surrender value appears **after** the premium-paying period
  completes, and its amount is standardised across two carriers at **10 × 入院給付金日額** [S1]
  [S6]. A third converts the same idea into a death benefit — 保険料払込期間満了後死亡保険金 =
  **10 × 入院給付金日額** [S9]. Under 終身払 there is no surrender value at all [S1] [S6].
- **配当金 and 満期保険金 do not exist** on this chassis — it is 無配当 [S1] [S6].
- **契約者貸付 and 自動振替貸付 are not offered** on one carrier's medical main contract
  (「契約者貸付、保険料の自動振替貸付は取扱いません」) [S1] — a direct consequence of there being
  no surrender value to lend against. This is the point where the third-sector chassis diverges
  from the `whole_life` savings chassis: **a medical policy really does lapse when the premium is
  missed**, because there is no APL to carry it. (That carrier's general 注意喚起情報 text
  describes 自動振替貸付 as available for products that have it, and notes 「保険料の自動振替貸付の
  取扱いがない保険種類もあります」 [S1].)
- Riders carry no surrender value at all, through the whole policy period [S1].
- On death of the insured, cover terminates; any surrender value that exists is paid to the
  policyholder [S1].

### 13. 免責事由, waiting periods, 責任開始, 告知

- **免責事由 (exclusions)** — the most complete list found, and it is representative [S4]:
  故意または重大な過失 of the policyholder or insured; 被保険者の犯罪行為; an accident caused by
  the insured's 精神障害; an accident caused by 泥酔; driving without the licence required by law;
  drink-driving or equivalent; 薬物依存; **頚部症候群（むちうち症）or 腰痛 with no objective
  findings, whatever the cause**; 地震・噴火・津波; 戦争その他の変乱. Two other carriers' lists
  match on the substantive items [S1] [S10]; the rider booklet repeats the same list [S5].
- Where a 地震・噴火・津波・戦争 event increases claims but its effect on the pricing basis is
  small, the insurer may pay in full or **reduce** the benefit in proportion [S4].
- **Suicide**: one carrier lists 「責任開始日から3年以内に被保険者が自殺した場合」 among the
  cases where nothing is paid [S1] — a three-year clause, longer than the UK's twelve months.
- **No general waiting period applies to the main medical cover.** Cover starts at 責任開始; the
  waiting periods that exist are targeted: がん 90/91 days on the cancer-linked riders and 特則
  [S1] [S6]; one year on 骨髄幹細胞の採取術 [S1] [S6] [S9] [S10]; one year on a named list of eight
  elective surgeries [S10]; two years on a 白内障 先進医療 limb [S6]; one year on a
  骨髄ドナー入院給付金 (no payment if the stay **ends** within one year) [S9]. One disclosure notes
  generically that 「保険種類によっては、一部、責任開始日から一定期間は保障されない場合があります」
  [S1].
- **Pre-inception conditions.** The base rule is that only disease arising, and accidents
  occurring, on or after 責任開始時 are covered [S1] [S2] [S9]. Two softening rules matter, and
  only one carrier has them:
  - A condition that pre-dates 責任開始期 **is** covered if the admission, surgery or procedure
    begins after **two years** from 責任開始日 [S4]. Separately, a pre-inception disease is paid
    within the terms accepted if the insurer knew of it at underwriting, and is paid in full if the
    insured had never consulted a doctor about it and had never been flagged at a health check
    (unless the insured was aware of the symptoms) [S4].
  - No equivalent two-year rule appears in the other retrieved disclosures [S1] [S2] [S6] [S9]
    [S10].
- **告知**: underwriting is 告知扱い — a written or on-screen declaration, with no medical
  examination in the direct channels [S1] [S6] [S10]. 告知受領権 rests with the company (and the
  examining physician where there is one); telling a 生命保険募集人 orally is not 告知 [S1] [S10].
- **告知義務違反**: the insurer may rescind within **2 years** of 責任開始日 (or of the 復活日)
  [S1] [S10]. Rescission does not defeat a claim where there is no causal connection between the
  misstatement and the event [S1]. 詐欺による取消 has no such time limit and returns nothing —
  no premium refund and no surrender value [S1].
- One carrier discloses that underwriting explicitly prices 受療率 by prefecture of residence,
  taken from the 厚生労働省「患者調査」 (受療率 per 100,000 population), alongside occupation and
  income [S6]. That is a public statement that the public morbidity data in §16 is the industry's
  own reference set.

### 14. 払込猶予期間, 失効, 復活

- **First premium**: one carrier gives a 払込期間 from 責任開始日 to the end of the following
  month and a 猶予期間 from the first day of the month after that to the end of the month after
  that; failure makes the contract **void** (無効), not lapsed [S1]. Another likewise makes the
  contract void if the first premium is unpaid by the end of its grace period [S10].
- **月払 grace**: from the first day of the month following the 払込期月 to the **last day of that
  month** — i.e. roughly one extra month. Stated identically at three carriers [S1] [S4] [S10].
  One carrier states a **two-month** grace (「その翌月から2ヶ月間の支払い猶予期間」) [S6].
- **半年払・年払 grace**: from the first day of the month following the 払込期月 to the monthly
  contract anniversary in the month after that [S1] [S4]; one carrier adds the calendar special
  case that where the 契約応当日 falls on the last day of February, June or November, grace runs to
  the last day of April, August and January respectively [S4].
- **Claims during grace**: unpaid premiums are deducted from the benefit; if the benefit is not
  enough to cover them the policyholder must pay the balance by the end of the grace period, else
  the contract lapses from the day after grace expires and neither the benefit nor the waiver is
  given [S4].
- Failure to pay within grace causes **失効** from the day after grace expires [S1] [S4] [S6] [S10].
- **復活 (reinstatement) — the widest carrier divergence in the whole product**:
  - **Not available at all** — 「保険料が未払いで契約が失効してしまうと、契約を元に戻すこと（復活）
    ができません」 [S6] [S8].
  - **Within 1 year of lapse** [S4], [S9].
  - **Within 3 years of lapse** [S10].
  - One carrier says only 「一定の期間内（保険種類により異なります）」 without a number [S1].
- 復活 requires payment of the arrears and **fresh 告知** (and possibly a medical), and may be
  refused on health grounds [S1] [S4] [S9] [S10]. Cover restarts on the 復活日, and the 責任開始期
  for pre-existing-condition tests resets to the last 復活 [S4]; a waiting period is re-run from
  the 復活日 where the rest of the waiting period would otherwise have expired [S9].
- クーリング・オフ windows differ: **15 days from the application date** (excluded where a medical
  examination was taken, for group-issued policies, or for business contracts) [S1]; **8 days from
  the day after the application date** [S10].

### 15. Published premium levels (rare, and worth citing exactly)

- **終身医療保険, エコノミーコース, 入院給付金日額 ¥5,000, 保険期間・保険料払込期間 終身,
  monthly, rates as at 2026-06-01** [S8]:

  | 契約年齢 | 男性 | 女性 |
  |---|---|---|
  | 20 | ¥1,199 | ¥1,369 |
  | 30 | ¥1,578 | ¥1,701 |
  | 40 | ¥2,121 | ¥2,034 |
  | 50 | ¥2,892 | ¥2,577 |
  | 60 | ¥3,923 | ¥3,363 |
  | 70 | ¥5,266 | ¥4,435 |
  | 80 | ¥6,829 | ¥5,962 |

  Note the **sex crossover between 30 and 40**: female premiums exceed male at 20 and 30 and fall
  below from 40 onward. That is a real morbidity fact (childbirth-related and gynaecological
  admissions at younger ages), not a pricing artefact, and any [std] morbidity basis must
  reproduce it.
- **終身医療保険, 三大疾病無制限型, 60日型, 先進医療特約(2018) 付加, 終身払, 入院給付金日額
  ¥5,000, monthly, rates as at 2025-07-01** [S3]:

  | 契約年齢 | 男性 | 女性 |
  |---|---|---|
  | 30 | ¥1,470 | ¥1,680 |
  | 40 | ¥2,080 | ¥1,995 |
  | 50 | ¥3,025 | ¥2,695 |

  The same crossover appears between 30 and 40, and the level sits within about 7% of the other
  carrier's for a richer specification.
- **終身医療保障保険, 入院日数連動型 60日型, 入院給付金日額 ¥10,000, 健康サポート特則（3年型）,
  手術総合特約 Ⅰ型（手術給付金基準額 ¥10,000）, 先進医療特約, 全期払（終身）, 口座振替, 月払:
  契約年齢40歳 男性 → ¥5,874 per month, of which the 先進医療特約 is ¥114** [S9]. Scaling the
  other carrier's 40M ¥2,121 on a ¥5,000 daily amount to ¥10,000 gives ¥4,242 for the daily benefit
  alone, so the ¥5,874 is consistent once the 20× surgery rider and the 健康サポート特則 are added.
- No carrier publishes a **rate table by policy year or a full age-by-age scale**; the above are
  the complete set of public specimen rates found. Any per-mille morbidity structure for the
  reference model must be constructed and marked [std].

### 16. The public morbidity data — the sharp contrast with `uklib`

This is the section that makes a Japanese medical model buildable from public sources where a UK
one is not.

- **入院受療率（人口10万対）, 令和5年** — national total **945**; 男 893, 女 995. By five-year age
  band [R6]:

  | 年齢階級 | 入院受療率 | 年齢階級 | 入院受療率 |
  |---|---|---|---|
  | 0歳 | 1,237 | 45–49 | 318 |
  | 1–4 | 153 | 50–54 | 441 |
  | 5–9 | 86 | 55–59 | 613 |
  | 10–14 | 87 | 60–64 | 838 |
  | 15–19 | 115 | 65–69 | 1,117 |
  | 20–24 | 137 | 70–74 | 1,502 |
  | 25–29 | 182 | 75–79 | 2,033 |
  | 30–34 | 239 | 80–84 | 2,952 |
  | 35–39 | 242 | 85–89 | 4,413 |
  | 40–44 | 258 | 90歳以上 | 6,275 |

  Re-stated groups: 0–14歳 164, 15–34歳 171, 35–64歳 450, 65歳以上 2,449, 70歳以上 2,787,
  75歳以上 3,351 [R6].
- 外来受療率 for the same year is **5,850** national total, giving 総数 6,795 [R6].
- **退院患者平均在院日数, 令和5年9月** — national **28.4 days**; **病院 29.3 days**,
  **一般診療所 14.2 days** [R6]. The series is falling steadily: 40.8 (平成8年) → 37.9 (平成14年)
  → 32.8 (平成23年) → 29.3 (平成29年) → 32.3 (令和2年, COVID-affected, flagged by 厚生労働省 as
  requiring care) → 28.4 (令和5年) [R6]. **A medical model calibrated on a stay-length
  distribution more than a few years old will systematically overstate the daily benefit.**
- **平均在院日数 by age band, 令和5年9月** [R6]: 総数 28.4; 0–14歳 7.6; 15–34歳 10.5;
  35–64歳 20.2; 65歳以上 35.5; 70歳以上 36.7; 75歳以上 39.0.
- **平均在院日数 by 傷病大分類, 令和5年** [R6] — the longest first:
  Ⅴ 精神及び行動の障害 **290.4** (統合失調症等 569.5); Ⅵ 神経系の疾患 **93.3**;
  Ⅸ 循環器系の疾患 **34.6** (脳血管疾患 68.9, 脳梗塞 65.6, 心疾患（高血圧性のものを除く）18.3,
  虚血性心疾患 7.7, 高血圧性疾患 41.6); Ⅳ 内分泌，栄養及び代謝疾患 24.7 (糖尿病 31.8);
  Ⅰ 感染症及び寄生虫症 25.1 (結核 44.3); Ⅲ 血液及び造血器の疾患 18.1;
  Ⅱ 新生物 **13.4** (悪性新生物 14.4 — 胃 14.7, 結腸及び直腸 15.3, 気管，気管支及び肺 14.1);
  Ⅷ 耳及び乳様突起の疾患 5.4; Ⅶ 眼及び付属器の疾患 **3.2** (白内障 **2.4**).
- The two extremes are the model's stress points: **精神及び行動の障害 at 290 days** blows straight
  through a 60-day or 120-day per-hospitalization cap and into the 通算 cap, while
  **白内障 at 2.4 days** sits entirely inside a five-day minimum-payment guarantee. A single mean
  stay length is not a usable assumption for this product.
- **Length-of-stay distribution.** 患者調査 publishes 推計退院患者数 by **在院期間 in 32 bands**
  crossed with sex and five-year age band (Z111), with 傷病大/中/小分類 (Z114/Z115/Z117), and as a
  **cumulative proportion** by 傷病中分類 (Z120), all as downloadable CSV [R7]. This is what a
  60日/120日 cap requires and it is public.
- **Re-admission interval.** 患者調査 publishes 推計退院患者数 by 過去の入院の有無・再入院までの期間
  (Z83, Z85, Z86, Z87) [R7] — the empirical basis for calibrating how often the 180-day rule binds.
- **Surgery rate.** 患者調査 publishes 退院患者平均在院日数 and 推計退院患者数 crossed with
  手術の有無 (Z106–Z109, Z125, Z126) [R7], giving a public in-hospital surgery proportion.
- **Cross-checks**: 医療給付実態調査 gives 件数・日数（回数）・点数（金額） by 疾病分類 × 診療種類 ×
  年齢階級 from the actual claims of the public schemes [R13]; 国民生活基礎調査 is the other
  household-level source (not retrieved this session — see gaps).
- The public system's own claim schedule, the **医科診療報酬点数表**, is the definitional backbone
  of the surgery benefit at every carrier [S1] [S2] [S4] [S9] [S10]; that means the benefit set can
  in principle be enumerated from a public document, unlike a UK critical-illness definition set.

### 17. Reserving, decrements and tax — what constrains the model

- **The valuation mortality table is public but not redistributable.**
  [corrected 2026-08-20: "not redistributable", not "redistributable" — the 日本アクチュアリー会
  site terms prohibit reproduction, alteration and transmission to third parties without
  written consent [REG-R21], so the table can be retrieved, read and cited but not shipped;
  numbering and every other line of this file are unchanged.]
  第三分野標準生命表2018 is
  published as a full numeric table by 日本アクチュアリー会, which prepares it under 保険業法
  第122条の2 on commission from the 金融庁 [R4]. Sample male rates: q40 = **0.00076**,
  q60 = **0.00548**, q80 = **0.04046**, e0 = 83.47; sample female rates: q40 = 0.00043,
  q60 = 0.00209, q80 = 0.01899, e0 = 89.59 [R4].
- **It is deliberately lighter than the death-insurance table.** 生保標準生命表2018（死亡保険用）
  male q40 = 0.00118 and q60 = 0.00653 against the third-sector table's 0.00076 and 0.00548 [R4].
  That is the correct direction of conservatism: on a health product, death **releases** the
  liability, so the valuation table must under-state mortality. A best-estimate medical model must
  therefore **not** use 第三分野標準生命表2018 as its mortality decrement without an explicit [std]
  adjustment, and must say which of the two it is using.
- 第三分野標準生命表2018 is **高度障害を含まない** (the 2007 table included it) [R5] — so a model
  that treats 高度障害 as a termination must add it separately.
- The table was built on the national 第21回生命表 (2010) with 2.5% p.a. improvement for five years
  then 1.0% p.a. for three, plus a 2σ statistical margin bounded at 70%–85% of the unadjusted rate
  on a 1,000,000-policy portfolio assumption [R5]. It is a **valuation** table carrying margins, not
  an experience table.
- **There is no published morbidity table.** 日本アクチュアリー会 publishes the mortality basis
  only; the 危険発生率 (incidence, length, surgery frequency) is each insurer's own. What the
  regulator requires instead is a **test**: 保険業法施行規則第69条第6項第1号の2 mandates a separate
  「第三分野保険の保険リスクに備える危険準備金」 [R2], and the 監督指針 requires that it be computed
  under the **ストレステスト** of 平成10年6月8日大蔵省告示第231号, with a 負債十分性テスト, both
  reflecting the uncertainty that 保険事故発生率 deteriorates, run per grouping sharing the same
  基礎率, and with the reasonableness of the 危険発生率等の設定水準 disclosed [R3]. **This is the
  exact boundary at which the reference model must mark its morbidity basis [std].**
- 標準責任準備金 applies to contracts not excluded by 保険業法施行規則第68条, and the floor for
  contracts outside it is **平準純保険料式** (net level premium) [R2].
- **生命保険料控除**: a 医療保険 premium falls in the **介護医療保険料** basket of the post-2012
  三区分 regime [R11]. Income-tax deduction: full premium up to ¥20,000; premium/2 + ¥10,000 to
  ¥40,000; premium/4 + ¥20,000 to ¥80,000; flat ¥40,000 above — **¥40,000 cap per basket,
  ¥120,000 overall** [R10]. At the observed premium levels (§15), a ¥5,000-daily-amount medical
  policy at age 40 pays roughly ¥25,000/year and so sits in the second band — the deduction is a
  real but second-order part of the product's economics.
- **Market context**: 65.6% of households hold life insurance paying 疾病入院給付金, at an average
  enrolled amount of ¥8,500 per day against a self-assessed need of ¥10,100 [R12].

---

## Variation across carriers

| Feature | [S1] [S2] [S3] | [S4] [S5] | [S6] [S7] [S8] | [S9] | [S10] |
|---|---|---|---|---|---|
| Chassis | 終身 | 終身 | 終身 **and** 定期 (separate products) | 終身 | 定期 (10年更新, converts to 終身) |
| 契約年齢 | 0–80 | not in fetched docs | 18–80 (終身) / 18–70 (定期) | not in fetched docs | 20–69 |
| 入院給付金日額 menu | not published; examples ¥5,000 / ¥10,000 | not published | ¥3,000/5,000/8,000/10,000/12,000/15,000 | example ¥10,000 | not published |
| 5日分最低保証 | **No** | **Yes** (≤5日 → 日額×5) | **Yes** (≤5日 → 日額×5) | **No** (入院日数連動型) | **No** |
| 1入院限度 | 60 / 120日 | 60 / 120日 | 60日 only | 60 / 120 / **730日** | 60日 only |
| 通算限度 | **1,000日** | **1,095日** | **1,095日** | **1,000日** | **1,095日** (across renewals) |
| One-hospitalization test | same cause **or** medically related | **cause-blind** | same cause or medically related | **cause-blind** | same cause or medically related (疾病); same accident (災害) |
| Re-admission reset | 181st day from day after discharge | after 180 days elapse | after 180 days | 型-dependent | 180 days |
| 生活習慣病 relaxation | 七大生活習慣病入院給付特則 — 三大 or 七大 unlimited, and outside the 通算 | separate 三大疾病無制限型長期入院特約 | おすすめコース — 3大生活習慣病 unlimited | not in the main contract | none |
| 手術給付金 | 20倍 入院中 / 5倍 外来, unlimited | **10倍 / 5倍 / 40倍 重大手術** | 10倍 / 5倍 | rider: Ⅰ型 20倍 / Ⅱ型 10倍 入院中, 5倍 外来, on a separate 基準額 | **flat 10倍, 入院中 only** |
| 放射線治療 | inside 手術給付金 (60日に1回) | **separate 給付金, 10倍** | inside 手術給付金 (60日に1回) | inside rider, 20倍/10倍 (60日に1回) | inside 手術給付金 (60日に1回) |
| Surgery during a day-limit-exhausted stay | not stated in fetched docs | **paid at the in-hospital multiple** | not stated | not stated | **not paid at all** |
| 先進医療 cap | 通算2,000万円 | 通算2,000万円 | 通算2,000万円 | 通算2,000万円 (10年更新, cap across renewals) | not in this booklet |
| 先進医療 top-up | 10% of benefit, ≤¥500,000/療養 | none (reimburses actual cost borne) | flat ¥100,000/療養 | 20% of 技術料, ≤¥1,000,000/療養 | — |
| 入院一時金 | 特約: ¥100,000, 通算50回 | 特約 (入院一時金特約) | none on this chassis | **main-contract 型**: 短期 10倍 / 一時金型 20倍 | 特約: max 2 per policy year |
| 解約返戻金 | none (終身払); 10 × 日額 after a 短期払 completes | none | none; 10 × 日額 after a 短期払 completes | none; 10 × 日額 as a post-payment death benefit | "may exist but small" |
| 契約者貸付 / 自動振替貸付 | **neither offered** | not in fetched docs | not in fetched docs | not in fetched docs | not in fetched docs |
| 月払 grace | to the end of the following month | to the end of the following month | **2 months** | a stated 猶予期間 | to the end of the following month |
| 復活 | "a period that varies by product" | **within 1 year** | **not available at all** | **within 1 year** | **within 3 years** |
| Pre-inception disease | not covered | **covered after 2 years** | not covered | not covered | not covered |
| クーリング・オフ | 15 days from application | not in fetched range | not in fetched range | not in fetched range | 8 days from the day after |

**What does not vary.** The surgery trigger is the 公的医療保険制度's 医科診療報酬点数表 at every
carrier, with the same seven-item exclusion list and the same 60-day radiation lockout; the
先進医療 aggregate cap is ¥20,000,000 everywhere; 疾病 and 災害 hospitalization benefits are never
paid concurrently; the 災害 limb always requires admission within 180 days of the accident;
bone-marrow donation surgery always carries a one-year wait and excludes 自家移植; and every main
contract is 無配当 and, during the premium-paying period, 無解約返戻金.

**Most representative design for a reference implementation.** A whole-of-life (終身),
無配当・無解約返戻金型 medical policy issued at ages 18–80, level premiums payable for life (with a
pay-to-65 variant), 入院給付金日額 ¥5,000 or ¥10,000, a 60日 per-hospitalization limit with a 120日
switch, a 1,095-day aggregate cap with a 1,000-day switch, a 180-day one-hospitalization rule on a
same-cause test, an optional five-day minimum payment, 手術給付金 at 20倍 in-hospital / 5倍
outpatient (with a 10倍/5倍 switch and a flat-10倍 switch), radiation folded into the surgery
benefit at once per 60 days, an optional 先進医療特約 reimbursing the 技術料 to a ¥20,000,000
aggregate cap with a 10% cash top-up capped at ¥500,000 per 療養, an optional 入院一時金特約, an
optional 三大疾病保険料払込免除特則, a disability-triggered base waiver, no surrender value, no
policy loan and no APL, a one-month grace on monthly premiums, and reinstatement within one year.

---

## Fetch failures and gaps

- **[S11] the SOMPOひまわり生命 「健康のお守り」 パンフレット** — HTTP 200, 23-page PDF (6.8 MB)
  downloaded successfully, but the PDF uses non-embedded CID-keyed fonts and `pypdf` text
  extraction returned mojibake for every substantive line. The booklet landing page
  (https://www.himawari-life.co.jp/product/suport_omamori_health/booklet/) links only this one
  PDF; the ご契約のしおり・約款 is served through a "Web約款" application rather than as a static
  file, so there is no alternative URL to try. Everything attributed to this carrier
  (1入院 40日/60日/120日 選択, 通算1,000日, 手術給付金 40/20/10/5倍, 通販は60日のみ) rests on a
  search-result snippet and is tagged **[unverified]**.
- **[S12] the 東京海上日動あんしん生命 「メディカルKit R」 booklet** — HTTP 200, 14-page PDF
  downloaded, same CID-font extraction failure; a second copy of a sibling document
  (https://www.bk.mufg.jp/sonaeru/hoken/syusin/pdf/tmn_medical_kit.pdf, 12 pp.) failed identically.
  The 健康還付特則 (return of premiums at a stated age on a medical chassis) is therefore recorded
  as existing in the market but its mechanics are **[unverified]**.
- **アクサ生命 (b_wlm09b) 「入院保障保険（終身型09）〈60日型〉重要事項説明書」**
  (https://www2.axa.co.jp/products/b_wlm09b/pdf/important.pdf) — HTTP 200, 8 pp., downloaded but
  the whole document is CID-garbled. Not used; the AXA material cited is [S10] instead, which
  extracted cleanly.
- **はなさく生命 「はなさく医療」 契約概要・注意喚起情報**
  (https://www.life8739.co.jp/pdf/shiori/direct/iryo_keiyakugaiyou_direct_202005.pdf) — HTTP 200,
  8 pp., CID-garbled. Not used; no facts depend on it.
- **A pamphlet at one carrier** (`https://www.orixlife.co.jp/medical/cure_next/pdf/cu_next_pamphlet.pdf`)
  — HTTP 200, 4 pp., CID-garbled. The premium and 契約年齢 facts that would have come from it were
  obtained instead from the product page [S3] and the 契約概要 [S1].
- **e-Gov 法令検索 HTML pages** (https://laws.e-gov.go.jp/law/407AC0000000105 and
  https://laws.e-gov.go.jp/law/408M50000040005) return only navigation chrome to a plain fetcher —
  the statute text is JavaScript-rendered. Both statutes were retrieved instead through the e-Gov
  law API (https://laws.e-gov.go.jp/api/1/lawdata/<lawid>), which returns the full UTF-8 XML.
  **Cite the human-readable page but note the API as the retrieval route.**
- **平成10年6月8日大蔵省告示第231号** (the 第三分野 ストレステスト notification) itself was **not**
  retrieved. Its existence, number, date and role are verified only through the 金融庁 監督指針
  [R3]; the notification's actual stress parameters are **[unverified]** and no numeric stress
  level is asserted anywhere above.
- **標準利率 for 第三分野 contracts** — not established this session. No 予定利率 or 標準利率 value
  is asserted in these notes. The 医療保険 products examined are 無配当・無解約返戻金型 with no
  published 予定利率, so the interest basis is not disclosed by any carrier document retrieved.
- **契約年齢範囲 at two carriers** [S4] [S9] — not found in the retrieved booklets or on the
  retrieved product pages. Only the 引受基準緩和型 sibling product in one booklet carries an
  explicit range in the extracted text (契約年齢 満30歳〜…, the upper bound falling outside the
  extracted line) [S4]; that is a different product and is not used.
- **住民税 (local inhabitant tax) caps on 生命保険料控除** — 国税庁 タックスアンサー No.1140 and
  No.1141 cover income tax only [R10] [R11]. The commonly quoted ¥28,000 per basket / ¥70,000
  overall local-tax caps are **[unverified]** and are not asserted above.
- **医療給付実態調査 discontinuation** — a search snippet stated the survey ends after 令和5年度,
  replaced from 令和6年度 by tabulations from the 高齢者医療確保法 anonymised medical-insurance
  database. The 厚生労働省 landing page [R13] fetched cleanly but carries no such notice, so the
  claim is **[unverified]**.
- **国民生活基礎調査** — named in the brief as a morbidity source but **not fetched this session**.
  Its 有訴者率 / 通院者率 series would complement 患者調査 but nothing above depends on it.
- **e-Stat CSV files themselves** — the 患者調査 令和5年 table **index** was retrieved and every
  table number cited in [R7] was read from that index. The individual CSV/Excel files (Z69, Z111,
  Z120, Z121, Z125, Z83–Z87) were **not** downloaded, so their column layouts and cell values are
  not verified here. The numeric values quoted in §16 come from the 概況 PDF [R6], which is a
  retrieved document.
- **完全生命表 / 簡易生命表 numeric tables** — only the 令和6年簡易生命表 methodology page and its
  summary sheet were retrieved [R8]; the per-sex qx tables (`life24-12.xlsx`, `life24-13.xlsx`)
  and the 第23回生命表 (完全生命表) files were not downloaded. The often-quoted 令和6 平均寿命
  figures are therefore **[unverified]** and are not stated above.
- **令和6年度 先進医療実績報告** — one carrier cites 第138回先進医療会議資料 for 令和6年度
  (令和5年7月1日〜令和6年6月30日) [S3]; that MHLW document was **not** located. The 令和5年度 report
  [R9] was retrieved and used, and the two agree on the per-case cost of 陽子線/重粒子線治療 to
  within rounding.
- **Premium rate structures** — no carrier publishes a rate table by age and duration; only the
  specimen rates in §15 are public. Any per-mille incidence, length-of-stay or surgery-frequency
  assumption for the reference model must be constructed from the 患者調査 tables and marked
  **[std]**, with the 危険発生率 explicitly identified as an insurer-discretionary basis subject to
  the ストレステスト requirement [R3].
