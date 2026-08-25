# 定期保険 (level term life) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese 定期保険 (*teiki hoken*, level term life) liability cash flow
reference model — the protection chassis on which `income_guarantee` states its deltas.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(product-specific regulatory/actuarial reference) pointing at a document actually retrieved
and read during this session, or is tagged [unverified] where it is general knowledge or a
search snippet that could not be confirmed against a retrieved document. Access date for all
fetched sources: 2026-08-20.

Retrieval method: PDFs were downloaded with `curl` carrying a browser User-Agent, then text
was extracted with `pdftotext -enc UTF-8` and, where that failed, with `pypdf`. HTML pages
that a summarising fetcher rendered were re-fetched raw and grepped, because the summariser
misread one insurer's premium table by a factor of four (see **Fetch failures and gaps**).

---

## Primary sources

Nine carriers are covered [corrected 2026-08-20: nine, not eight — the list below
names nine]: オリックス生命, ライフネット生命, 日本生命, アクサ生命
(アクサダイレクト生命), チューリッヒ生命, かんぽ生命, FWD生命, メットライフ生命, 大同生命.

### S1 — オリックス生命, 「無配当 無解約払戻金型定期保険（インターネット申込専用） ご契約のしおり／約款」

- Publisher: オリックス生命保険株式会社
- Document: ご契約のしおり／約款 for ネット専用定期保険Bridge［ブリッジ］, 2015年10月版,
  form mark `30ＫＩ07`; 117 PDF pages (しおり pages 1–56, then 約款 renumbered 1–58)
- Doc type: ご契約のしおり・約款 (policy booklet + full policy conditions)
- URL: https://www.orixlife.co.jp/life/bridge/pdf/yakkan_br_20151002.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.88 MB PDF downloaded; `pdftotext` recovered all
  約款 article text and most しおり body text; the display-typeset cover/diagram pages use a
  subset font poppler could not map and came out as mojibake — no fact below rests on them)
- Key content: 普通保険約款 articles 1–40 in full — 死亡保険金/高度障害保険金 (art. 1),
  保険料の払込の免除 (art. 5), 責任開始 (art. 9), 払込方法 (arts. 10–12), 猶予期間・失効
  (art. 13), 復活 (art. 15), 更新 (art. 16), 減額 (art. 19), 告知義務違反 (arts. 27–29),
  払戻金 (art. 32), 契約年齢 (art. 33), 契約者配当 (art. 35), 時効 (art. 36); リビング・ニーズ
  特約条項; 別表3 高度障害状態 and 別表4 身体障害の状態; the tax and 自動更新 sections of the
  しおり.

### S2 — オリックス生命, ネット専用定期保険Bridge 商品ページ (published rate card)

- Publisher: オリックス生命保険株式会社
- Doc type: 商品ページ (consumer), including a 月払保険料例 table
- URL: https://www.orixlife.co.jp/life/bridge/
- Accessed: 2026-08-20. Retrieved: YES (fetched twice — once through the summarising fetcher,
  once raw with `curl` and grepped, to verify the premium figures character-for-character)
- Key content: the full published premium grid (sex × age 30/40/50 × sum assured
  500/1,000/1,500万円, 10-year term, rates as at 2025-07-01); 契約年齢 20–65; 年満了 10–30年
  in 5-year steps and 歳満了 60–80歳 in 5-year steps; auto-renewal to 80; 保険金額
  500–3,000万円 in 100万円 units; 高度障害 at the same amount; リビング・ニーズ; 払込免除.

### S3 — オリックス生命, ネット専用定期保険Bridge 商品詳細ページ

- Publisher: オリックス生命保険株式会社
- Doc type: 商品詳細 (product specification page)
- URL: https://www.orixlife.co.jp/life/bridge/detail.html
- Accessed: 2026-08-20. Retrieved: YES
- Key content: 保険料払込方法（回数）月払・半年払・年払; 払込経路 口座振替・クレジットカード;
  confirmation that リビング・ニーズ特約 is attached in advance (あらかじめ付加) and that
  解約払戻金 is absent for the whole term.

### S4 — ライフネット生命, 「定期死亡保険（無配当・無解約返戻金型） ご契約のしおり・約款」

- Publisher: ライフネット生命保険株式会社
- Document: ご契約のしおり・約款, 2026年6月版, form mark `LN_BB_GAP-25`; 45 PDF pages
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_teiki_latest.pdf
  (linked from https://www.lifenet-seimei.co.jp/policy/yakkan/)
- Accessed: 2026-08-20. Retrieved: YES (758 KB PDF downloaded, text extracted cleanly and
  read; only the しくみ図 diagram is glyph-garbled)
- Key content: 商品の特徴 table (契約年齢, 保険金額 bands, 保険期間, 更新, 無診査限度額 by
  age band); a published 無解約返戻金型 vs 解約返戻金あり premium and value comparison;
  税法上の特典 with both 所得税 and 住民税 生命保険料控除 tables and the 相続税 500万円 rule;
  約款 arts. 10–25 (保険料払込期間, 払込, 猶予期間, 払込免除, 更新, 告知義務, 解除); the
  explicit statement that reinstatement (復活) is not offered.

### S5 — ライフネット生命, 定期死亡保険 商品ページ

- Publisher: ライフネット生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.lifenet-seimei.co.jp/product/life/
- Accessed: 2026-08-20. Retrieved: YES
- Key content: 契約年齢 18–80; 保険金額 bands by age; 保険期間 10/20/30年 and 65/80/90歳満了;
  auto-renewal to 90; monthly premium only; premium examples for 30歳男女, 10年, 1,000万円.

### S6 — ライフネット生命, 「かぞくへの保険 定期死亡保険（無配当・無解約返戻金型）普通保険約款」(2009年12月版)

- Publisher: ライフネット生命保険株式会社
- Document: 普通保険約款 only (no しおり), 2009年12月; 21 numbered pages P-1…P-21
- Doc type: 普通保険約款 (superseded edition, retained on the site)
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_policy_200912_001.pdf
- Accessed: 2026-08-20. Retrieved: YES (304 KB PDF, text extracted and read)
- Key content: the earlier article numbering (第1条 この保険の内容 … 第29条 管轄裁判所) and the
  first-article statement that 満期時の保険金・配当・解約返戻金 are all absent. Useful only as
  corroboration that the no-surrender-value design is long-standing at this carrier.

### S7 — 日本生命, 「ニッセイみらいのカタチ ご契約のしおり－定款・約款」

- Publisher: 日本生命保険相互会社
- Document: ご契約のしおり－定款・約款, 2026年4月改訂, しおり番号 ２０２６０４Ａ; 182 PDF pages
  (this is file `01.pdf` of the booklet set — しおり body plus the 約款 table of contents)
- Doc type: ご契約のしおり・定款・約款 (traditional multi-product menu booklet)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/shiori/01.pdf
- Accessed: 2026-08-20. Retrieved: YES, PARTIAL (12.3 MB PDF downloaded; the running text
  extracts cleanly with both `pdftotext` and `pypdf`, but a substantial minority of the
  display-typeset pages — including many diagram captions — are glyph-garbled in both. Facts
  below are taken only from passages that extracted as clean Japanese.)
- Key content: the 全期型／更新型／終身 taxonomy and which product types may take which;
  高額割引制度 thresholds; the 保険料の払込みの案内と保険契約の解除 mechanic (催告 + 解除予定日)
  that replaces 猶予期間・失効・復活 at this carrier; the explicit absence of
  自動振替貸付制度; 定期保険（有配当2012）給付約款 in the 約款 list; 配当金 mechanics;
  リビング・ニーズ特約 terms; 免責事由 table including the 3-year suicide clause and the
  払戻金 paid on each 免責事由.

### S8 — アクサ生命, 「定期保険（無解約返戻金型） 重要事項説明書／ご契約のしおり／約款」

- Publisher: アクサ生命保険株式会社 (product sold as アクサダイレクトの定期保険2; the booklet
  names アクサ生命 as 引受保険会社)
- Document: 重要事項説明書（契約概要・注意喚起情報）+ ご契約のしおり + 約款; 84 PDF pages
- Doc type: 重要事項説明書／ご契約のしおり／約款
- URL: https://www.axa-direct-life.co.jp/pdf/yakkan_l.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.25 MB PDF downloaded, text extracted and read;
  only the cover and two しくみ図 are glyph-garbled)
- Key content: 契約概要 table — 契約年齢 満20–満69, 保険期間 10年 only, renewal to 80,
  月払 only (年払 not offered as at 2024年4月), 告知扱い; 死亡保険金 and 高度障害保険金
  definitions; 災害割増特約; リビング・ニーズ特約 with its remaining-term restriction and
  3,000万円 cap; 保険料の払込みの免除; 免責事由 table; 猶予期間 and 復活 provisions;
  the no-surrender-value statement and its 解約返戻金あり comparison.

### S9 — チューリッヒ生命, 定期保険プラチナ 商品ページ (published rate card)

- Publisher: チューリッヒ生命保険株式会社
- Doc type: 商品ページ (consumer), including four 月払保険料 tables
- URL: https://www.zurichlife.co.jp/product/category_shibou/teikihoken
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped; the summarising
  fetcher returned wrong figures for this page — see **Fetch failures and gaps**)
- Key content: 契約年齢 15–80 (Web application from 18); 保険期間 10年 (auto-renewal to 90)
  or 60/65/70/90歳満了; 保険金額 100万–1億円 (200万円 minimum other than 90歳満了); no
  解約払戻金; 高度障害保険金 equal to the death benefit; リビング・ニーズ特約; 災害割増特約 and
  特定疾病保険料払込免除特約; 高額割引制度; the 無診査 limits by age band; and the full
  published premium grid for both 10年更新 and 90歳満了 designs (rates as at 2026年7月).

### S10 — かんぽ生命, 定期保険「新普通定期保険」商品ページ (published rate card)

- Publisher: 株式会社かんぽ生命保険
- Doc type: 商品ページ (consumer), page mark `Ⅱ W 2026.05 14036`
- URL: https://www.jp-life.japanpost.jp/products/teiki/index.html
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped)
- Key content: 加入できる年齢 15–65; 保険期間 10年 or to 55/60/65/70/75歳; 加入できる保険金額
  100万–1,000万円; the 重度障がい benefit (this carrier's name for 高度障害); no 満期保険金,
  no 倍額支払制度; a 更新制度 with limits; 特約 menu (無配当災害特約, 医療特約, 無配当先進医療
  特約), maximum three; and a rate table before/after the 2026-05-02 repricing, at ages
  30/40/50/60 for both sexes, with the base and rider components separately disclosed.

### S11 — かんぽ生命, 「普通定期保険（新普通定期保険） ご契約のしおり・約款」抜粋 (2021年4月版)

- Publisher: 株式会社かんぽ生命保険
- Document: the 定期保険 chapter of the ご契約のしおり・約款, 2021年4月版
- Doc type: ご契約のしおり・約款 (extract)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/teiki/202104/tik06.pdf
- Accessed: 2026-08-20. **Retrieved: NO** (567 KB PDF downloaded successfully — HTTP 200 —
  but both `pdftotext` and `pypdf` returned mojibake for almost all body glyphs, and every
  numeral was dropped. Two short passages survived and are noted in the gaps section, but no
  fact in the extraction below is sourced to this document.)

### S12 — FWD生命, 「FWD定期／FWD優良体定期」パンフレット

- Publisher: FWD生命保険株式会社
- Document: product brochure covering FWD定期 and FWD優良体定期
- Doc type: 商品パンフレット
- URL: https://www.fwdlife.co.jp/files/v3/assets/blt52d7347d77fa3188/blt37f9884b94b1358b/64cb39878403820965f252d5/teikihoken.pdf
- Accessed: 2026-08-20. Retrieved: YES (4.27 MB PDF downloaded, text extracted and read)
- Key content: **the only product in this set with a surrender value** — 解約返戻金 exists and
  払済保険 conversion is offered; 契約年齢 6–75 (FWD定期) and 21–70 (FWD優良体定期); 満了時年齢
  envelopes; auto-renewal to 99 and the 優良体定期 → 定期保険 auto-conversion at expiry; the
  three-tier rate class (標準体／優良体／非喫煙者優良体) with its **published discount
  percentages** and its full underwriting criteria (blood pressure, BMI, one-year smoking
  history, cotinine test); a full premium grid by age 25–55 for both sexes; リビング・ニーズ
  特約; 保険料払込みの免除; and a post-expiry guaranteed-insurability window.

### S13 — メットライフ生命, スーパー割引定期保険 商品ページ

- Publisher: メットライフ生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.metlife.co.jp/products/life/sslt/
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped; the numeric
  rate-class criteria on this page live inside SVG images and were not recoverable as text)
- Key content: the underlying product is a 無配当平準定期保険 to which a リスク細分型保険料率
  is applied; the rate class has **four tiers** driven by 喫煙の有無・血圧・体格; the maximum
  published discount is 約54% (標準体保険料率 vs 非喫煙優良体保険料率, 1,000万円 / 35歳男性 /
  20年); the rate class assigned at issue **persists through every renewal to age 80**;
  保険金額 500万–3,000万円 in 100万円 steps; 保険期間 10年・20年 (更新タイプ) or 60歳・65歳満了
  (満了タイプ); and — a design detail worth noting — 解約返戻金 is absent *because* a
  リスク細分型保険料率 has been applied.

### S14 — 大同生命, 「定期保険 Dタイプ（保険料逓減型）」個人向け 商品ページ

- Publisher: 大同生命保険株式会社
- Document: 商品ページ, page mark `H-2026-0004①（2026年5月27日）`, content as at 2026年6月
- Doc type: 商品ページ (product specification)
- URL: https://www.daido-life.co.jp/join/c_kojin/lineup/muhaid_teigen/
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped)
- Key content: 正式名称 無配当逓減定期保険（保険料逓減・無解約払戻金型); the **逓減 mechanism
  stated as a formula**; 契約年齢 25–75; 保険期間 from 5 years upward in 1-year steps,
  更新型; no 解約払戻金・満期保険金・配当金; 健康体割引特約 (非喫煙者健康体保険料率) with its
  criteria; 災害割増特約, 傷害特約, 年金支払特約, 指定代理請求特約, 保険契約者代理特約;
  高額割引.

---

## Regulatory and actuarial references

### R1 — 保険業法 第3条 (生命保険業免許と第一分野の定義)

- Publisher: e-Gov 法令検索 (デジタル庁) — 保険業法, 平成七年法律第百五号, promulgated
  1995-06-07
- Doc type: statute
- URL (human): https://laws.e-gov.go.jp/law/407AC0000000105 —
  URL (machine, used): https://laws.e-gov.go.jp/api/1/lawdata/407AC0000000105
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (3.7 MB XML; the human-facing page
  is JavaScript-rendered and returns only chrome to plain fetchers — see gaps)
- Content: 第3条第1項 licence requirement; 第2項 the licence is of two kinds only, 生命保険業
  免許 and 損害保険業免許; 第3項 one entity may not hold both; **第4項第1号** — the 第一分野
  definition: insurance that promises to pay a fixed sum 「人の生存又は死亡（当該人の余命が
  一定の期間以内であると医師により診断された身体の状態を含む。）に関し」. The parenthesis is
  load-bearing for this product: it puts the *terminal-prognosis* payment inside the
  first-sector licence, which is the statutory footing of リビング・ニーズ特約.
  第4項第2号 is the 第三分野 list (疾病, 傷害による状態, 傷害を直接の原因とする死亡, 治療);
  第5項 is the 損害保険業免許.

### R2 — 保険業法施行規則 第68条・第69条 (標準責任準備金の対象契約と積立方式)

- Publisher: e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- Doc type: ministerial ordinance
- URL (machine, used): https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (30.2 MB XML)
- Content: 第68条 — which contracts fall under 法第116条第2項 (標準責任準備金); excluded are
  unit-linked contracts, contracts that accumulate no 保険料積立金, and contracts whose
  約款 lets the insurer change the 予定利率. 第69条第1項 — the four reserve components:
  保険料積立金, 未経過保険料, 払戻積立金, 危険準備金. 第69条第4項第1号 — for 標準責任準備金
  contracts the reserve may not fall below the amount computed on the 金融庁長官's basis;
  第4項第2号 — for other contracts it may not fall below the **平準純保険料式** amount, which
  the ordinance defines in line as levelling the funding across the whole premium-paying
  period.

### R3 — 日本アクチュアリー会, 「標準生命表2018」公開ページ

- Publisher: 公益社団法人 日本アクチュアリー会
- Doc type: 専門情報ページ
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Accessed: 2026-08-20. Retrieved: YES
- Content: the Institute is the 指定法人 under 保険業法第122条の2第1項 and is commissioned by
  the FSA under 第122条の2第2項第3号 to prepare the 標準生命表; the 2018 revision was published
  for comment 2017-03-31, resolved 2017-05-10, submitted to the FSA Commissioner 2017-05-11,
  and applies from 2018年4月 after the corresponding 告示 amendment. Links three PDFs:
  the tables themselves, the 作成概要, and the 作成過程.

### R4 — 日本アクチュアリー会, 「標準生命表２０１８」(the numerical tables)

- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８, 5 PDF pages, containing four complete tables:
  生保標準生命表２０１８（死亡保険用）男 and 女, and 第三分野標準生命表２０１８ 男 and 女,
  each with lx, dx, qx and e°x by single year of age from 0
- Doc type: mortality table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (236 KB PDF downloaded, text extracted, qx values
  parsed positionally by age and spot-checked against the printed age labels)
- Content: this is the **publicly downloadable statutory valuation mortality table** — the
  single sharpest contrast with `uklib`, where the current CMI term-assurance tables are
  subscriber-restricted. Sample values read off the table are given in the extraction below.

### R5 — 金融庁, 平成8年大蔵省告示第48号 (標準責任準備金の係数) 改正案の公表

- Publisher: 金融庁
- Document: 「保険業法第百十六条第二項の規定に基づく長期の保険契約で内閣府令で定めるものに
  ついての責任準備金の積立方式及び予定死亡率その他の責任準備金の計算の基礎となるべき係数の
  水準（平成８年大蔵省告示第48号）等の一部を改正する件（案）」の公表について, 平成28年4月27日
- Doc type: パブリックコメント公表ページ (with three 別紙 PDFs)
- URL: https://www.fsa.go.jp/news/27/hoken/20160427-2.html
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched raw and read; the 別紙 PDFs were not
  opened)
- Content: names 平成8年大蔵省告示第48号 as the instrument that fixes, under 保険業法第116条
  第2項, the reserve method and the 予定死亡率 and other coefficients; states in terms that the
  「責任準備金算出基礎としての予定利率（標準利率）」 is derived from an 指標金利 built on
  JGB yield averages with 安全率係数 applied, and that the 2016 amendment added a 安全率係数
  for indicator rates at or below 0%.

### R6 — 金融庁, 「経済価値ベースのソルベンシー規制の概要」

- Publisher: 金融庁 監督局保険課 保険モニタリング室
- Document: 経済価値ベースのソルベンシー規制の概要, dated 2026年7月 on its cover, 10 PDF pages
  (the same URL previously carried a 2025年7月23日 edition)
- Doc type: 説明資料 (regulator explanatory deck)
- URL: https://www.fsa.go.jp/policy/economic_value-based_solvency/10.pdf
- Accessed: 2026-08-20. Retrieved: YES (645 KB PDF downloaded with a browser User-Agent and
  extracted; a plain summarising fetch of the same URL returned undecodable binary — see gaps)
- Content: the three-pillar structure, applying from the **2026年3月期**; ESR = 適格資本 ÷
  所要資本; the old SMR is 原則ロックイン while ESR is 時価評価 with a MOCE loaded on the
  current estimate; the supervisory ladder — **ESR < 100%** enters 早期是正措置 第一区分,
  **< 70%** 第二区分, **< 35%** 第三区分, against the old regime's **SMR < 200%** trigger;
  and industry averages at 2025年3月末 of ESR 215% vs SMR 873% for 生保単体.

### R7 — 国税庁, タックスアンサー No.1140「生命保険料控除」

- Publisher: 国税庁
- Doc type: タックスアンサー (tax authority guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the post-2012 三区分 — 新生命保険料 (一般), 介護医療保険料, 新個人年金保険料; the
  新契約 (2012-01-01 以後) 所得税 deduction schedule and the 旧契約 schedule; and the
  overall 所得税 cap of 120,000円. The page does not carry the 住民税 schedule (that is
  reproduced from [S4] below).

### R8 — 国税庁, タックスアンサー No.4114「相続税の課税対象になる死亡保険金」

- Publisher: 国税庁
- Doc type: タックスアンサー
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4114.htm
- Accessed: 2026-08-20. Retrieved: YES
- Content: the 非課税限度額 is 「500万円 × 法定相続人の数」, available only where the recipient
  is an heir (those who renounced the inheritance or lost the right are excluded), and
  apportioned across heirs in proportion to the amounts each receives.

### R9 — 生命保険文化センター, 「2024（令和6）年度 生命保険に関する全国実態調査＜速報版＞」

- Publisher: 公益財団法人 生命保険文化センター, 2024年11月
- Doc type: 実態調査 (household survey, speed report edition)
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.74 MB PDF downloaded, text extracted, the summary
  and 図表Ⅰ-70 read)
- Content: household penetration and average benefit levels, and the product mix of the most
  recent policy bought — the market-context numbers quoted in §11 below.

---

## Fact extraction

### 1. Product architecture and where 定期保険 sits

- 定期保険 is 第一分野 business: 保険業法第3条第4項第1号 covers insurance promising a fixed sum
  「人の生存又は死亡…に関し」, and the same clause's parenthesis expressly brings within it the
  state of 「余命が一定の期間以内であると医師により診断された身体の状態」 [R1]. So both the
  death benefit and the living-needs acceleration sit under one first-sector licence — there
  is no separate accelerated-benefit class as there would be if this were rider business.
- The dominant retail shape in this source set is a **平準定期保険** (level term):
  無配当・無解約返戻金型, sum assured constant, premium level for the 保険期間, benefit paid on
  death **or** on 高度障害 at the same amount [S1] [S4] [S8] [S9] [S12]. メットライフ names the
  underlying chassis explicitly: 「無配当平準定期保険」 [S13].
- **逓減定期保険** (decreasing term) is a distinct product, not a payout option on the level
  product: 大同生命's 無配当逓減定期保険（保険料逓減・無解約払戻金型) [S14]. See §7.
- Two structurally different term-length designs coexist and are contrasted by name in the
  documentation: **年満了** (a fixed number of years, then auto-renewal at attained-age rates)
  and **歳満了** (to a stated age, no renewal) [S2] [S4] [S5]. 日本生命 gives the same
  distinction the names **更新型** and **全期型**, alongside 終身 [S7]. This renewal structure
  is the sharpest contrast with a UK term assurance, which simply expires.
- 有配当 vs 無配当 splits by distribution channel in this set. 日本生命's term product is
  written under the 「定期保険（有配当2012）給付約款」 and participates in the annual 配当金
  declaration, which accumulates with interest and is paid on request or on termination [S7].
  Every direct/online writer here is 無配当 and says so in the product name; オリックス生命's
  約款第35条 is a single sentence: 「この保険契約については、契約者配当はありません。」 [S1].
- 主契約 + 特約 structure: the main contract carries only death and 高度障害; everything else is
  a 特約. Which 特約 are automatic and which are optional varies (§6, §9).

### 2. Issue-age and term envelopes

Per carrier, as published:

| Carrier | 契約年齢 | 保険期間 | Renewal ceiling |
|---|---|---|---|
| オリックス生命 [S2] | 20–65 | 年満了 10–30年 (5-year steps); 歳満了 60–80歳 (5-year steps) | 80 |
| ライフネット生命 [S4] [S5] | 18–80 | 10/20/30年; 65/80/90歳満了 | 90 |
| アクサ生命 [S8] | 満20–満69 | 10年 only | 80 |
| チューリッヒ生命 [S9] | 15–80 (Web from 18) | 10年; 60/65/70/90歳満了 | 90 |
| かんぽ生命 [S10] | 15–65 | 10年; 55/60/65/70/75歳満了 | (更新制度 with limits) |
| FWD生命 [S12] | FWD定期 6–75; FWD優良体定期 21–70 | 満了時年齢 9–80 (≥3年) or 81–99 (≥10年); 優良体定期 満了時年齢 31–99 (≥10年) | 99 |
| メットライフ生命 [S13] | not published on the page | 10年・20年 (更新); 60歳・65歳満了 | 80 |
| 大同生命 [S14] | 25–75 | ≥5年, 1-year steps, 更新型 | not published |

- Observed range of minimum issue age: **6 to 25**; the modal retail minimum is 20 [S2] [S8],
  with three carriers at 15–18 [S4] [S5] [S9] [S10] and FWD at 6 [S12].
- Observed range of maximum issue age: **65 to 80** [S2] [S10] vs [S4] [S9].
- Observed range of expiry/renewal ceiling: **75 to 99** [S10] vs [S12]; the mode is 80.
- 保険料払込期間 equals 保険期間 in every product examined [S4 art. 10] [S8] [S9] [S12]; where
  a policy's 保険期間 is altered, 保険料払込期間 is altered with it [S1 art. 18 ⑧].
- 歳満了 has a precise definition worth carrying into the model: the term runs 「被保険者が
  満了年齢になって初めて到来する年単位の契約応当日の前日まで（契約応当日が誕生日の場合は、
  満了年齢になる誕生日の前日まで）」 [S1] [S4]. It is an anniversary-based, not a
  birthday-based, cut-off in the general case.
- 契約年齢 is 満年齢 with fractions of a year discarded [S1 art. 33]. ライフネット生命 measures
  it at 契約日, which is the 1st of the month following application [S4]; かんぽ生命 warns that
  its 加入年齢 is a 契約上の年齢 differing from actual age, and that the calculation itself
  changed at the 2026-05-02 repricing [S10].

### 3. Sum assured envelopes and banding

- オリックス生命: 500万–3,000万円 in 100万円 units, with the maximum varying by 契約年齢 [S2].
- ライフネット生命 bands the minimum by age: 18–50歳 500万–1億円; 51–65歳 300万–1億円;
  66–70歳 200万–1億円; 71–80歳 100万–1億円 — all in 100万円 units. Increases are not permitted
  (a new contract is required); decreases are [S4] [S5].
- チューリッヒ生命: 100万–1億円 for 90歳満了, 200万–1億円 otherwise, 100万円 units [S9].
- かんぽ生命: 100万–1,000万円 [S10] — an order of magnitude below the private writers' ceiling.
- メットライフ生命: 500万–3,000万円 in 100万円 steps [S13].
- Non-medical (告知のみ) limits are published by two carriers and are a genuine underwriting
  parameter, not marketing:
  - ライフネット生命: 18–40歳 3,000万円; 41–45歳 2,500万円; 46–50歳 2,000万円; 51–55歳
    1,500万円; 56–70歳 1,000万円; 71–80歳 500万円 [S4].
  - チューリッヒ生命: 15–39歳 5,000万円; 40–49歳 2,500万円; 50–59歳 2,000万円; 60–64歳
    1,500万円; 65–75歳 1,000万円; 76–80歳 500万円 [S9].
- Reductions: 保険金額の減額 is allowed subject to a floor the insurer sets, future premiums are
  reset, and — on a no-surrender-value product — 「保険金額の減額分に対応する解約払戻金は
  ありません」 [S1 art. 19]. アクサ生命 likewise allows decreases and refuses increases [S8].
- Band discounts exist and are a real premium driver. 日本生命's 高額割引制度 applies where the
  割引適用基準額 reaches **3,000万円**, with a further step at **5,000万円**; for a 定期保険 the
  基準額 is simply the 保険金額 [S7]. チューリッヒ生命 [S9] and 大同生命 [S14] also carry a
  高額割引; neither publishes the thresholds.

### 4. Death benefit and 高度障害保険金 — the distinctive Japanese pair

- The main contract pays **two** benefits of the same amount, and both terminate the policy:
  死亡保険金 on death during the 保険期間, and 高度障害保険金 where the insured comes to be in
  a 高度障害状態 during the 保険期間 from an injury or sickness arising on or after
  責任開始時 [S1 art. 1] [S4] [S8] [S9] [S12]. There is no US or UK analogue in this library:
  it is neither a critical-illness rider nor a terminal-illness acceleration — it is the same
  sum assured on a defined permanent-total-disability list.
- Ordering rules are explicit and matter for a claims model: if the 高度障害保険金 is claimed
  and payable before the death benefit is paid, the death benefit is **not** paid; once the
  death benefit has been paid, no 高度障害 claim is entertained [S1 art. 1 ②③]. アクサ生命 words
  it the other way round from the same principle — if the insured dies before the 高度障害
  claim is settled, the death benefit is paid and the 高度障害保険金 is not [S8].
- Recipient differs between the two: 死亡保険金 goes to the 死亡保険金受取人, 高度障害保険金 goes
  to the **被保険者** and its recipient may not be changed to anyone else (the exception being
  a corporate policyholder that is also the death-benefit beneficiary) [S1 art. 1 ⑤⑥] [S12].
- The 高度障害状態 list (別表3) is a closed eight-item schedule, materially identical across
  carriers [S1]:
  1. 両眼の視力を全く永久に失ったもの
  2. 言語またはそしゃくの機能を全く永久に失ったもの
  3. 中枢神経系または精神に著しい障害を残し、終身常に介護を要するもの
  4. 胸腹部臓器に著しい障害を残し、終身常に介護を要するもの
  5. 両上肢とも、手関節以上で失ったかまたはその用を全く永久に失ったもの
  6. 両下肢とも、足関節以上で失ったかまたはその用を全く永久に失ったもの
  7. １上肢を手関節以上で失い、かつ、１下肢を足関節以上で失ったかまたはその用を全く永久に
     失ったもの
  8. １上肢の用を全く永久に失い、かつ、１下肢を足関節以上で失ったもの
- 備考 to 別表3 fixes the operative definitions numerically: 「視力を全く永久に失ったもの」 is
  corrected visual acuity **0.02 or below** with no prospect of recovery; 「常に介護を要する
  もの」 requires the insured to be unable to perform *any* of eating, toileting and its
  aftermath, dressing, rising, walking and bathing without help; hearing loss (別表4) is
  measured as (a + 2b + c)/4 ≥ **90 dB** at 500/1,000/2,000 Hz [S1].
- A boundary rule with a cash-flow consequence: where at the 保険期間満了日 the disability is
  present but its irrecoverability is not yet clear, and it later turns out to be irrecoverable,
  the insurer treats the 高度障害状態 as having been met **on the expiry date** and pays; if it
  recovers or turns out to be recoverable, nothing is paid [S1]. A claims-run-off model should
  expect 高度障害 claims to be *reported* after the term ends.
- 死亡保険金受取人 default cascade: on the death of the named beneficiary without a
  replacement, the beneficiary's 法定相続人 at that date become the beneficiaries, sharing in
  their statutory proportions [S1 arts. 8–10 of art. 1] [S4].

### 5. Premium structure, payment modes and the published rate cards

- **Japanese direct writers do publish rate cards.** This is a sharp contrast with `uklib`,
  where no premium basis is observable at all and the reference model's rates had to be
  constructed. Two carriers in this set publish an age × sex × sum-assured grid
  [corrected 2026-08-20: two, not four — only [S2] and [S9] tabulate more than one sum
  assured; [S12] gives age × sex at a single 2,000万円 basis and [S5] gives single examples],
  two more publish age × sex rates at one sum-assured basis, and a fifth
  publishes a repricing table. What follows is quoted exactly.
- オリックス生命, 月払保険料, 保険期間・保険料払込期間 10年, rates as at **2025-07-01** [S2]:

  | 保険金額 | 男30歳 | 男40歳 | 男50歳 | 女30歳 | 女40歳 | 女50歳 |
  |---|---|---|---|---|---|---|
  | 500万円 | 611円 | 1,036円 | 2,091円 | 509円 | 811円 | 1,398円 |
  | 1,000万円 | 974円 | 1,823円 | 3,933円 | 770円 | 1,373円 | 2,548円 |
  | 1,500万円 | 1,337円 | 2,611円 | 5,776円 | 1,031円 | 1,936円 | 3,698円 |

  The 500万円 → 1,000万円 → 1,500万円 steps are almost exactly arithmetic (e.g. male 30:
  611 → 974 → 1,337, a constant 363円 per 500万円), which discloses a **per-mille rate plus a
  flat policy fee** structure: the implied policy fee is 611 − 363 = **248円/month** for that
  cell, and the same 248円 falls out of the 40 and 50 rows. The female rows behave the same
  way (30歳: 509 → 770 → 1,031, step 261円, fee 248円). The policy-fee constant is identical
  across ages and sexes.
- チューリッヒ生命, 月払保険料, rates as at **2026年7月** [S9]:

  | Design | 保険金額 | 男30 | 男40 | 男50 | 女30 | 女40 | 女50 |
  |---|---|---|---|---|---|---|---|
  | 10年更新 | 400万円 | 628円 | 992円 | 1,972円 | 540円 | 796円 | 1,384円 |
  | 10年更新 | 1,000万円 | 980円 | 1,890円 | 4,340円 | 760円 | 1,400円 | 2,870円 |
  | 90歳満了 | 100万円 | 613円 | 921円 | 1,307円 | — | 606円 | 818円 |
  | 90歳満了 | 200万円 | 1,226円 | 1,842円 | 2,614円 | 852円 | 1,212円 | 1,636円 |

  The 90歳満了 rows are exactly proportional (100万 → 200万 doubles precisely), so on the
  long-term design there is **no** flat policy fee in the published figures; the 10年更新 rows
  are not proportional, so there is one there. The 90歳満了 premium for a male 30 (613円 per
  100万円) against the 10年更新 premium (157円 per 100万円 at the 400万円 cell) is a clean
  4× ratio — the price of removing renewal risk.
- かんぽ生命, 月払保険料 per **100万円 基準保険金額**, 10年, 口座払込み, as at 2026-05-02 [S10]:
  男30歳 **250円**, 女30歳 **220円**. The carrier's headline "570円 / 720円" figures for age 30
  are the base contract **plus** the 無配当総合医療特約 (男 250 + 320; 女 220 + 500) — the
  medical rider is what makes the female headline dearer, not the term cover. The published
  combined (base + medical rider) figures across ages are 30歳 男570/女720, 40歳 男740/女710,
  50歳 男1,140/女920, 60歳 男2,200/女1,350 [S10].
- FWD生命, FWD定期, 月払（口座振替扱）, 保険金額 2,000万円, 保険期間・保険料払込期間 60歳満了
  [S12]:

  | 契約年齢 | 25 | 30 | 35 | 40 | 45 | 50 | 55 |
  |---|---|---|---|---|---|---|---|
  | 男性 | 5,702円 | 6,328円 | 7,176円 | 8,308円 | 9,788円 | 11,666円 | 14,041円 |
  | 女性 | 3,482円 | 3,848円 | 4,295円 | 4,847円 | 5,547円 | 6,344円 | 7,159円 |

- ライフネット生命 publishes single examples: 30歳男性 / 10年 / 1,000万円 = **1,068円/月**;
  30歳女性 same = **846円/月** [S5]. It also publishes a long-duration example — 男性20歳,
  90歳満了, 1,000万円, 月払 — at **4,864円/月**, against **11,298円/月** for an otherwise
  identical product *with* a surrender value (§8) [S4].
- Payment frequency: オリックス生命 offers 月払・半年払・年払 [S3] and permits switching between
  them [S1 art. 17]. ライフネット生命 and アクサ生命 are **月払 only** (アクサ notes 年払 was not
  on offer as at 2024年4月) [S4] [S8]. Payment route: 口座振替, 振込, クレジットカード, and
  団体扱・特別団体扱 [S1 art. 11]; ライフネット生命 is 口座振替 or credit card only [S4].
- 保険料の前納 (advance payment of future premiums) is available at a discount at the insurer's
  stated rate, held on deposit with interest and applied at each 応当日 [S1 art. 12].
  かんぽ生命 offers a 前納割引 for three months or more paid together and allows 1–12 months or
  a lump payment of the whole remaining term [S10].
- Rating factors that are disclosed: 性別・年齢・保険期間・保険金額・払込方法 [S8] [S9], plus
  the 保険料率区分 where a preferred-risk structure applies (§10) and the 高額割引 band (§3).

### 6. Renewal (更新) — the mechanic with no UK analogue

- Default is **automatic**: unless the policyholder notifies otherwise, the contract renews on
  the day after 保険期間満了日, for the same 保険期間 and the same 保険金額, with **no fresh
  underwriting or 告知** [S1 art. 16 ①] [S4 art. 19 ①] [S8] [S12].
- Notice period to decline renewal: **2 weeks** before expiry (オリックス生命 [S1], アクサ生命
  [S8]); **2 months** (ライフネット生命 [S4]); **1 month** (日本生命 [S7]).
- Premium on renewal is recomputed at the **attained age on the renewal date** and at the
  **rate scale in force at that date**, and the renewed contract is governed by the 約款 then
  in force [S1 art. 16 ②⑦] [S4 art. 19 ④⑥] [S8] [S12]. Every carrier warns in terms that the
  renewed premium is usually higher [S1] [S4] [S7] [S8].
- Renewal is refused, and the ceiling therefore bites, in these cases [S1 art. 16 ⑩]:
  (1) the elapsed period from 契約日 to the renewed expiry date exceeds the insurer's range;
  (2) the attained age on the day after the renewed expiry exceeds the insurer's range;
  (3) **the 保険期間 is 歳満期** — 歳満了 contracts never renew.
- What happens at the ceiling differs, and this is a modelling fork:
  - オリックス生命 and アクサ生命 **truncate**: if renewing on the same term would take the
    policy past 80, it renews as an 80歳満了 contract instead. アクサ states the trigger band
    precisely — renewal ages 満71 to 満79 convert a 10-year term into an 80歳満了 term
    [S1] [S2] [S8].
  - ライフネット生命 truncates in whole years: renewal is refused if the attained age on the
    renewal date is 満90 or more, and where the renewed expiry would fall at age 91 or more the
    term is **shortened year by year so the expiry age is 90** [S4 art. 19 ②⑤] [S5].
  - 日本生命 both shortens *and lengthens*: it truncates the term where the renewed expiry
    would pass the 指定年齢, and it **extends** the term where the renewed expiry would leave
    fewer than 5 years to the 指定年齢 (its worked examples show a 10-year term renewed for 7
    years in the first case and for 13 years in the second) [S7].
  - FWD生命's 優良体定期 does not renew at all — at expiry it **auto-converts** into the
    standard FWD定期 and cover continues [S12].
- Renewal does **not** restart the contestability or suicide clocks: the periods run from the
  original 責任開始 and the renewed term is treated as continuous with the prior term
  [S4 art. 19 ⑦]. アクサ words the same result from the exclusion side —
  「ただし、更新された場合を除きます。」 [S8]; オリックス words it from the coverage side —
  the 3-year suicide window runs 「（更新後の保険期間を含みます。）」 [S1].
- Renewal requires the pre-expiry premiums to have been paid; the first premium of the renewed
  contract is due by the last day of the month containing the renewal date, and if it is unpaid
  through the grace period **the renewal is treated as never having happened** [S1 art. 16
  ③④]. 日本生命 is explicit that in this case the policy simply terminates at expiry rather than
  being 解除 [S7].
- If the insurer no longer writes the product at the renewal date, the policy is moved to a
  comparable contract the insurer designates rather than lapsing [S1 art. 16 ⑨] [S4 art. 19 ⑧]
  [S12].
- No new 保険証券 is issued on renewal [S1] [S4].
- On renewal the reserve/refund clock restarts: 第32条第2項's 「保険料を払い込んだ年月数および
  経過した年月数」 is read as 「更新後の…」 [S1 art. 16 ⑤].

### 7. 逓減定期保険 (decreasing term)

- 大同生命's 無配当逓減定期保険（保険料逓減・無解約払戻金型) states the decrement as a formula:
  死亡・高度障がい保険金 decreases **from the second policy year, every year, by
  「基本保険金額 ÷ 保険期間」, to the final year** [S14]. That is a straight-line run-off of the
  initial sum assured over the term — not the amortisation-schedule shape of a UK decreasing
  term, which tracks a notional repayment mortgage at a stated interest rate.
- **The premium decreases too**, from the second policy year, in step with the cover [S14].
  This is the opposite of the UK convention, where decreasing cover carries a level premium.
- 保険期間 is settable from 5 years upward in 1-year steps, 更新型; 契約年齢 25–75; there is no
  解約払戻金, no 満期保険金 and no 配当金 [S14].
- Secondary sources describe other 逓減 designs — some stepping down to a floor such as 20% of
  the 基本保険金額 rather than to zero, and note that both the 逓減率 and the stepping mechanism
  vary by insurer [unverified — from search snippets only; no second carrier's 逓減 product
  document was retrieved].

### 8. Surrender value, maturity value and dividends

- **Seven of the eight carriers' term products have no surrender value at all.** The 約款 says
  it in one line: 「この保険契約については、解約払戻金はありません。」 [S1 art. 32 ①]. The same
  applies at ライフネット生命 [S4], アクサ生命 [S8], チューリッヒ生命 [S9], かんぽ生命 [S10],
  メットライフ生命 [S13] and 大同生命 [S14]. There is no 満期保険金 on any of them
  [S1] [S8] [S10] [S14].
- **FWD生命 is the exception in this set**: FWD定期 and FWD優良体定期 do have a 解約返戻金 and do
  permit conversion to a **払済保険** (reduced paid-up, same term, smaller sum assured) after
  the first policy year. 延長定期保険 is not offered [S12]. A Japan term chassis therefore
  cannot assume the absence of a cash value the way a UK one can.
- The 責任準備金 exists even where the 解約払戻金 does not, and is computed 「保険料を払い込んだ
  年月数および経過した年月数により」 [S1 art. 32 ②]. It is payable to the policyholder in two of
  the three death-benefit 免責事由 cases (§12).
- ライフネット生命 publishes a direct comparison of its 無解約返戻金型 product against a
  hypothetical 解約返戻金あり product of the same cover — male 20, 90歳満了, 1,000万円, 月払
  [S4]:

  | 経過 | 年齢 | 無解約返戻金型 払込累計 | その解約返戻金 | 解約返戻金あり 払込累計 | その解約返戻金 |
  |---|---|---|---|---|---|
  | 10年 | 30 | 583,680円 | 0円 | 1,355,760円 | 1,037,000円 |
  | 20年 | 40 | 1,167,360円 | 0円 | 2,711,520円 | 2,120,000円 |
  | 30年 | 50 | 1,751,040円 | 0円 | 4,067,280円 | 3,205,000円 |
  | 40年 | 60 | 2,334,720円 | 0円 | 5,423,040円 | 4,218,000円 |
  | 50年 | 70 | 2,918,400円 | 0円 | 6,778,800円 | 5,020,000円 |
  | 60年 | 80 | 3,502,080円 | 0円 | 8,134,560円 | 5,084,000円 |
  | 70年 | 90 | 4,085,760円 | 0円 | 9,490,320円 | 0円 |

  The monthly premiums behind the two columns are **4,864円** and **11,298円** — the
  cash-value version costs 2.32× the protection-only version. The carrier states it does not
  actually sell the 解約返戻金あり version and that the figures are its own 参考金額 [S4].
  The final row is the diagnostic one: the reserve on the cash-value product runs off to zero
  at the terminal age, so a 90歳満了 term is not an endowment however large its mid-term value.
- Dividends: 無配当 products declare none [S1 art. 35] [S8] [S10] [S14]. 日本生命's
  定期保険（有配当2012) does: 配当金 allotted from each year's surplus accumulate from the next
  契約応当日 with interest at a rate the insurer sets, and are paid on request or on
  termination of the whole 組み合わせ; リビング・ニーズ特約 and 保険料払込免除特約 carry no
  dividend; and the carrier states plainly that a dividend may not be payable at all in a
  given year [S7].
- メットライフ生命 states the causal link the other way round from the usual framing: because a
  リスク細分型保険料率 has been applied, there is no 解約返戻金 [S13].

### 9. Riders (特約) and the living-needs acceleration

- **リビング・ニーズ特約** is the near-universal rider on Japanese death cover and is the
  library's closest analogue to UK terminal-illness cover — but it is a *rider*, not an
  embedded benefit, and its economics differ.
  - Trigger: the insured is judged to have **6 months or less** to live, meaning 6 months or
    less 「日本で一般に認められた医療による治療を行っても」. The insurer makes the judgement on
    a physician's certificate and may require examination by a physician it nominates [S1] [S7].
  - Amount paid = **指定保険金額 − six months' interest on it − six months' premiums on it**
    [S1] [S7] [S8] [S12]. オリックス prints it as `支払金額 = Ａ − Ｂ − Ｃ`, and adds that where
    a renewal falls within those six months the post-renewal months are priced at the
    renewal-age premium [S1]. This discount is the whole reason the rider can be free.
  - Cap: 指定保険金額 is limited to **3,000万円** per insured, aggregated across all of that
    insurer's contracts (オリックス aggregates it with its がんリビング・ニーズ特約 as well)
    [S1] [S7] [S8] [S12].
  - Term restriction: no payment where the claim date falls within **1 year** of the main
    contract's 保険期間満了 — except where automatic renewal is still available [S1] [S7] [S8].
  - Effect: paying the whole 死亡保険金額 extinguishes the contract and all 特約 **retroactively
    to the claim date**; paying part reduces the 死亡保険金額 by the 指定保険金額 retroactively
    to the claim date, and the reduced premium continues to be payable on the surviving part.
    No 解約払戻金 arises from the reduction. One payment per contract only [S1] [S7].
  - Attachment differs: 自動付加 at オリックス生命 [S2] [S3] and at 日本生命 (to 終身保険,
    養老保険, 定期保険, 生存給付金付定期保険 and 新３大疾病保障保険（死亡保障100%型）) [S7];
    an **optional** 特約 the applicant elects at アクサ生命 [S8]. Notably, **ライフネット生命's
    定期死亡保険 has no リビング・ニーズ特約 at all** — the string does not occur anywhere in its
    45-page ご契約のしおり・約款 [S4].
  - Premium: 日本生命 lists リビング・ニーズ特約 among the 特約 that carry no 配当金, and no
    separate 特約保険料 is disclosed for it in any document retrieved; the rider being free of
    charge is the market convention [unverified — the free-of-charge point is not asserted in
    terms by any retrieved document, though the six-month discount mechanism supplies the
    economic reason].
- **保険料の払込の免除** (waiver of premium) is in the **main contract** at several carriers, not
  a rider: where the insured, from an 不慮の事故 occurring on or after 責任開始時, comes within
  **180 days** of that accident to be in a 身体障害の状態 (別表4) while premiums are still
  payable, all future premiums are waived and are treated as having been paid at each 応当日
  [S1 arts. 5–6] [S8] [S12] [S14]. ライフネット生命's version keys off 傷害 generally rather
  than an accident-plus-180-days test [S4 art. 14].
  - Exclusions from the waiver: intent or gross negligence of policyholder or insured; the
    insured's criminal act; an accident caused by the insured's mental disorder; an accident
    caused by the insured's intoxication; driving without a licence; driving under the
    influence [S1 art. 6] [S8].
  - 別表4 (身体障害の状態) is a *lower* bar than 別表3: loss of one eye, deafness in both ears,
    loss of one upper or lower limb at the wrist/ankle or of two of its three major joints,
    permanent loss of use of all ten fingers or all ten toes, or marked permanent spinal
    deformity or restriction of movement [S1].
  - 日本生命 sells the waiver as an optional **保険料払込免除特約** instead [S7], and 大同生命
    has it in the main contract [S14].
- **指定代理請求特約**: where the insured is the beneficiary (as for 高度障害保険金 and the
  living-needs benefit) and cannot claim, a pre-nominated 指定代理請求人 may claim in their
  place. アクサ生命 sets the eligible range as spouse, relatives within the second degree, or a
  cohabiting/economically-dependent person the insurer accepts [S8]; it is a standard rider at
  every carrier [S1] [S12] [S14].
- **災害割増特約** adds an accidental-death and accidental-高度障害 amount on top, triggered by
  a 不慮の事故 with death within 180 days of the accident, or by a specified 感染症 [S8] [S9]
  [S14].
- Other riders seen: 特定障害不担保特約 / 「特定障害を不担保とする特則」 (excludes a named
  disability from the 高度障害 and waiver triggers, and **carries into renewed terms**)
  [S1] [S4]; 責任開始に関する特約 and 口座振替特約 [S1]; 特定疾病保険料払込免除特約 [S9];
  傷害特約, 年金支払特約, 保険契約者代理特約 [S14]; 無配当災害特約, 医療特約, 無配当先進医療
  特約 at かんぽ生命, maximum three per contract [S10].
- **Not present anywhere in this set**: an indexation/increasing-cover option, a
  guaranteed-insurability (life-event) option on the main contract, joint-life cover, or a
  conversion option. FWD生命 has the nearest thing to a GIO — where a contract has run more
  than 2 years and then expires, is surrendered or is reduced, a new FWD policy may be taken
  within **1 month** without medical evidence or 告知, subject to conditions [S12].

### 10. Preferred-risk and non-smoker rate classes

- Rate-class structures are real, published, and among the largest single premium levers.
- **FWD生命** publishes three classes and their measured effect, for 30歳男性 / 2,000万円 /
  60歳満了 / 月払 [S12]:

  | Class | Monthly premium | Discount vs 標準体 |
  |---|---|---|
  | 標準体保険料率 (FWD定期) | 6,328円 | — |
  | 優良体保険料率 (FWD優良体定期) | 5,408円 | 約14.5% |
  | 非喫煙者優良体保険料率 (FWD優良体定期) | 4,388円 | 約30.6% |

  Criteria, verbatim [S12] — 優良体 requires all of: (1) health and physical condition assessed
  good on the insurer's underwriting standards; (2) **最大血圧140未満、最小血圧90未満**;
  (3) **BMI 18.0–27.0**, BMI = weight(kg) ÷ height(m)². 非喫煙者優良体 requires those three
  **plus no smoking within the past 1 year**, evidenced by a 告知 on smoking history *and* the
  insurer's own smoking test with a **cotinine level within a stated range**; failing the test
  drops the applicant to 優良体. A medical examination or health-check/人間ドック results must be
  submitted for either class. The brochure warns that passive smoking alone can produce a
  "smoker" determination.
- **メットライフ生命** applies a リスク細分型保険料率 with **four** tiers driven by 喫煙の有無・
  血圧・体格, with a maximum published discount of **約54%** — 標準体保険料率 (no risk
  segmentation) vs 非喫煙優良体保険料率, at 1,000万円 / 35歳男性 / 20年 [S13]. The four class
  names are commonly given as 非喫煙優良体・非喫煙標準体・喫煙優良体・標準体
  [unverified — the page carries them inside SVG images; only 非喫煙優良体 and 標準体 appear as
  text]. Two facts from the page do matter for a model: the class is fixed at issue and
  **applied unchanged through every renewal to age 80**, regardless of later health; and the
  application of a risk-segmented rate is what removes the 解約返戻金.
- **大同生命** offers the same thing as an elective rider — 健康体割引特約, applied where 保険金額,
  age, **血圧・体格・尿検査の結果および喫煙の有無** meet the insurer's standards, giving the
  非喫煙者健康体保険料率. The carrier notes pointedly that 「健康体」 is the name of a rider and
  not a statement about health [S14].
- **No rate-class structure at all** in the オリックス生命 Bridge, ライフネット生命, アクサ生命,
  チューリッヒ生命 or かんぽ生命 products examined: their published grids are indexed by sex and
  age only, and the word 非喫煙 does not occur in the アクサ生命 84-page booklet [S1] [S2] [S4]
  [S8] [S9] [S10].
- So the observed range for a term product's rate-class count is **1 to 4**, and the observed
  maximum non-smoker/preferred discount is **約30.6%** (three-tier, [S12]) to **約54%**
  (four-tier, [S13]).

### 11. Underwriting, distribution and market context

- Underwriting evidence: online writers accept 告知のみ within the age/amount limits in §3 and
  ask for health-check results above them [S4] [S9]; オリックス生命 Bridge takes no medical
  examination at all and gives 即日 cover from the application date [S2]. Preferred classes
  require a medical or health-check submission and a cotinine test [S12].
- 特別条件 (substandard acceptance) takes the Japanese forms of 保険金削減支払法 and
  特定部位不担保法 / 特定障害不担保; 日本生命 states that a policy under 特別条件 cannot be
  renewed unless only 特定部位不担保 applies, or the 削減 period has already run out [S7].
- Contract registration: the insurer registers the insured's name, DOB, sex, address (to
  city/ward level), the 死亡保険金額, the 契約日 and the insurer's name with 生命保険協会 for
  **5 years** from the 契約日, and may query the register when underwriting or when a death or
  高度障害 claim arrives within 5 years [S1 art. 37].
- クーリング・オフ: **15 days** from the application date, in writing, with a full refund
  without interest [S1].
- 時効: the right to claim a 保険金 or 責任準備金, or to have premiums waived, extinguishes
  **3 years** after it becomes exercisable [S1 art. 36] [S10].
- Claim payment timetable, which a cash-flow model may want: **5 business days** from the day
  after complete documents arrive; **45 days** where verification of the event, a possible
  免責事由, a possible 告知義務違反 or a 重大事由 is needed; **180 days** where special enquiries
  (statutory enquiries, expert medical/engineering investigation, criminal-process enquiries,
  overseas investigation) are required [S1 art. 7].
- 据置支払: the beneficiary may leave the benefit on deposit with the insurer for a stated
  period at the insurer's rate, and withdraw the whole at any time [S1].
- Market context [R9], 2024（令和6）年度 survey, two-or-more-person households:
  - 世帯加入率 (全生保, incl. 個人年金) **89.2%** (prior 89.8%); 民保 79.9%.
  - 世帯普通死亡保険金額 average **1,936万円** (prior 2,027万円) — falling.
  - 世帯年間払込保険料 average **35.3万円**; 世帯加入件数 3.8件.
  - Product mix of the **most recently bought** 民保 policy (2019–2024 purchases): 終身保険
    **29.2%**, 医療保険 **28.1%**, ガン保険 10.5%, **定期保険 8.3%**, 定期付終身保険 3.2%,
    養老保険 1.7%. The three survivor-benefit shapes (終身・定期・定期付終身) together are
    **40.7%**.
  - Distribution: 加入チャネル ①生命保険会社の営業職員 **56.7%**, ②保険代理店 15.7%.
  This is the numeric case for the house style's claim that 第三分野 dominates by policy count,
  and it also places stand-alone 定期保険 as a minority of new individual sales — the reason
  this chassis matters more as a building block (and as `income_guarantee`'s parent) than as a
  headline product.

### 12. Exclusions, contestability, grace, lapse and reinstatement

**免責事由 for the death benefit** — three, and only three, in every 約款 retrieved:

1. **Suicide within 3 years** of the 責任開始日. Precisely: 「責任開始（復活が行なわれた場合は
   最後の復活の際の責任開始…）の日からその日を含めて３年以内の被保険者の自殺」 [S1 art. 1].
   The window includes renewed terms [S1], and renewal does not restart it [S4] [S8].
   Three years is the settled market position: オリックス生命 [S1], ライフネット生命 [S4],
   日本生命 [S7], アクサ生命 [S8] all say 3 years. This is **three times the UK's twelve
   months**.
2. Intentional killing of the insured by the **死亡保険金受取人**. Where that person is only a
   part-beneficiary, the remaining share is paid to the others [S1 art. 1 ⑦].
3. Intentional killing of the insured by the **保険契約者**.

What is paid instead differs by limb, and this is a real (if small) cash flow:
the **責任準備金** is paid to the policyholder on limbs 1 and 2, and **nothing** is paid on
limb 3 [S1 art. 1 ⑪]. 日本生命 splits it slightly differently — 責任準備金 on the suicide limb
and on the beneficiary-intent limb, and the 解約払戻金 on the policyholder-intent limb [S7].
ライフネット生命 notes that suicide arising from a mental disorder may still be paid [S4], as
does アクサ生命 [S8].

**免責事由 for 高度障害保険金**: intent of the policyholder, or intent of the insured
[S1 art. 1]. アクサ生命 adds the insured's self-harm, the insured's criminal act, and gross
negligence of policyholder or insured [S8].

**War and catastrophe**: not an exclusion but a **reduction** power — where war or other
upheaval (and, for the waiver, also earthquake, eruption or tsunami) increases claim numbers
enough to affect the product's costing basis, the insurer may pay a reduced 死亡保険金 or
高度障害保険金 [S1 arts. 2, 6] [S4 art. 14 ②] [S8].

**Pre-inception cause**: the 高度障害保険金 and the premium waiver are not payable where the
cause is a sickness or accident arising **before** 責任開始時 — unless the condition was
disclosed and accepted, or there was no prior consultation, no abnormality flagged at a health
check, and no awareness of symptoms [S1] [S4] [S8]. The **death** benefit carries no such
pre-existing-condition restriction.

**告知義務違反 (contestability)** [S1 arts. 27–29] [S4 arts. 20–22]:
- The insurer may rescind prospectively where the policyholder or insured, intentionally or by
  gross negligence, failed to state or misstated a fact it asked about. Rescission is available
  **even after** a claim event, in which case the benefit is not paid and any benefit already
  paid may be reclaimed [S1 art. 28].
- Rescission is barred where the insurer knew or negligently did not know the fact; where an
  intermediary obstructed or encouraged the misstatement; **1 month** after the insurer learns
  the ground; or where **2 years** have passed from 責任開始 (or the last 復活) without a claim
  or waiver event arising [S1 art. 29] [S4 art. 22]. So the contestability window is **2 years**,
  against the suicide window's 3.
- Causation defence: even after rescission, the benefit is paid if the claimant proves the
  event did not arise from the concealed fact [S1 art. 28 ③] [S7].
- On rescission by 告知義務違反 there is **no 払戻金** on a no-surrender-value product
  [S1 art. 28 ⑤]; 日本生命 pays the 解約払戻金 where one exists [S7].
- 詐欺 (rescission for fraud) and 不法取得目的 (voidness) are separate and are **not**
  time-limited: オリックス生命 warns in terms that 「責任開始日…からの年数は問いません。告知
  義務違反による解除の対象外となる２年経過後にも取消または無効となることがあります」, and no
  refund is paid in either case [S1].
- 重大事由による解除 covers claim-provoking, fraud in the claim, anti-social-forces
  affiliation, and — at ライフネット生命 — gross over-insurance across contracts [S1 art. 30]
  [S4 art. 23].

**Grace, lapse and reinstatement** — the widest variation in the whole product:

| Carrier | 猶予期間 (monthly) | Consequence | 復活 |
|---|---|---|---|
| オリックス生命 [S1] | 払込期月の翌月初日〜末日 (~1 month) | 失効 the day after | **3 years**, with interest at **年6% compound** on arrears |
| アクサ生命 [S8] | 払込期月の翌月1日〜末日 (~1 month) | 失効 | **3 years**, subject to health |
| ライフネット生命 [S4] | 払込期月の翌月初日〜**翌々月末日** (~2 months) | 失効 | **not offered** — 「契約の復活はできません」 |
| 日本生命 [S7] | no 猶予期間; a 催告 is issued and a **解除予定日** is set at the 月ごと応当日 in the **3rd month** after 払込期月 | 解除 on that date | **not offered** — 「解除された保険契約をもとに戻すことはできません」 |

- For 年払 and 半年払 contracts オリックス生命's grace runs to the monthly anniversary in the
  month **after next**, with named substitutions where the anniversary falls on the last day of
  February, June or November (to the last day of April, August and January respectively)
  [S1 art. 13 ①(2)].
- A claim arising **within** the grace period is paid, with the unpaid premium deducted from the
  benefit [S1 art. 14] [S4 art. 13 ②] [S8]. A **waiver** event arising in the grace period is
  different: the arrears must actually be paid by the end of grace or the policy lapses and the
  waiver is refused [S1 art. 14 ②] [S4 art. 13 ③].
- **自動振替貸付 (automatic premium loan) does not apply to this product.** 日本生命 states it
  twice, in terms: 「この保険には、保険料の自動振替貸付制度…はありません。」 The policyholder may
  instead draw on the 契約貸付制度 and apply the loan to the premium [S7]. かんぽ生命's 定期保険
  likewise carries 「契約者貸付制度の利用はできません」 [S11 — the one legible fragment; treated
  as [unverified] because the document did not extract]. This is the expected consequence of
  there being no 解約返戻金 to lend against: the APL mechanic that matters so much on
  `whole_life` is simply absent from the protection chassis.
- 日本生命's design has a further consequence: because the whole 組み合わせ shares one premium,
  non-payment 解除s **every** contract in the package except any whose premium was paid
  separately, and a 頭金 already paid is lost with it [S7].

### 13. Alterations available after issue

- 保険料払込方法（回数）の変更 between 年払/半年払/月払 — 年払 effective from the 契約応当日,
  半年払 from a 半年ごと応当日 or 契約応当日 [S1 art. 17].
- 保険期間の変更, with the insurer's consent; premiums are reset from the next 保険料期間; **no**
  amount is refunded to the policyholder, and any shortfall in the 責任準備金 must be paid in;
  refused where the new term falls outside the insurer's range or where a 特約 carries a
  特別条件; the 保険料払込期間 changes with it [S1 art. 18]. アクサ生命 additionally refuses a
  term change within **2 years** of the 契約日 or 更新日 [S8].
- 保険金額の減額 (§3). 増額 is generally not available — アクサ生命 refuses it outright, and
  ライフネット生命 requires a new contract with fresh underwriting [S8] [S4].
- 保険契約者の変更 with the insured's and insurer's consent [S1 art. 20];
  死亡保険金受取人の変更 by notice or by will, effective against the insurer only when notified
  [S1 arts. 23–24] [S4 arts. 15–16].
- Where the 保険料の払込が免除された, the alteration rights (payment frequency, term, sum
  assured, and the "other individual insurance" handling) are switched off [S1 art. 5 ③];
  日本生命 similarly bars a term change at renewal once the waiver is running [S7].

### 14. Tax treatment

- **生命保険料控除.** Premiums fall in the **一般生命保険料** basket of the post-2012 三区分
  (一般 / 介護医療 / 個人年金) [R7]. 新契約 (concluded 2012-01-01 or later) 所得税 deduction
  [R7], confirmed identically in a carrier document [S4]:

  | 年間正味払込保険料 | 控除額 |
  |---|---|
  | 20,000円以下 | 全額 |
  | 20,000円超 40,000円以下 | ×1/2 + 10,000円 |
  | 40,000円超 80,000円以下 | ×1/4 + 20,000円 |
  | 80,000円超 | 一律 40,000円 |

  旧契約 (2011-12-31 以前): 25,000円以下 全額; –50,000円 ×1/2+12,500円; –100,000円
  ×1/4+25,000円; 超 一律 50,000円 [R7]. Overall 所得税 cap across the three baskets:
  **120,000円** [R7].
- **住民税** schedule (not on the NTA page; taken from a carrier document) [S4]:
  12,000円以下 全額; –32,000円 ×1/2+6,000円; –56,000円 ×1/4+14,000円; 超 一律 28,000円.
- **控除証明書** timing: certificates are posted from late October; where an 年払/半年払 premium
  falls due in November or December the certificate may miss 年末調整, and 所得税基本通達196-1
  permits the employer to run 年末調整 with the deduction on condition the certificate is
  submitted by **31 January** of the following year [S1].
- **死亡保険金 taxation** turns on the 契約者／被保険者／受取人 triangle [S1]:
  - 契約者 = 被保険者 → **相続税**
  - 契約者 = 受取人, 被保険者 different → **所得税（一時所得）**
  - all three different → **贈与税**
- Where 相続税 applies and the beneficiary is a 法定相続人, **500万円 × 法定相続人の数** is
  exempt, apportioned across recipient heirs in proportion to what each receives; heirs who
  renounced or lost the right are excluded from the beneficiary test but the count itself is
  the statutory 法定相続人の数 [R8] [S4].
- **高度障害保険金 and リビング・ニーズ保険金 are in principle tax-free** where received by the
  insured or by their spouse, lineal blood relative, or a relative sharing their household
  [S1] [S4].

### 15. Valuation and actuarial basis

- **標準責任準備金.** Under 保険業法第116条第2項 the FSA fixes, by 告示, the reserve method and
  the 予定死亡率 and other coefficients for the long-term contracts the 内閣府令 specifies
  [R5]. 保険業法施行規則第68条 defines that set of contracts (excluding unit-linked business,
  contracts with no 保険料積立金, and contracts whose 約款 lets the insurer reset the 予定利率),
  and 第69条第4項第1号 says the 保険料積立金 for those contracts may not fall below the amount on
  the Commissioner's basis. For contracts outside that set, 第69条第4項第2号 imposes a floor of
  the **平準純保険料式** amount, defined in the ordinance as levelling the funding across the
  whole premium-paying period [R2].
- The four reserve components named in 第69条第1項 are **保険料積立金, 未経過保険料,
  払戻積立金, 危険準備金** [R2]. This library projects gross cash flows and cites reserving
  rather than reproducing it.
- **標準利率** is the 予定利率 element of that 告示 basis. The FSA describes it as derived from
  an 指標金利 built on JGB yield averages, with 安全率係数 applied by band; the 2016 amendment
  added a 安全率係数 for indicator rates at or below 0% [R5]. The **current numeric value** of
  the 標準利率 for level-premium 第一分野 business could not be established from any document
  retrieved this session — [unverified]. See the gaps section.
- **標準生命表2018.** Prepared by 日本アクチュアリー会 as the 指定法人 under 保険業法第122条の2
  第1項, on commission from the FSA under 第122条の2第2項第3号; the 2018 revision took effect
  from 2018年4月 following the corresponding 告示 amendment [R3]. **The tables themselves are
  a free public PDF** [R4] — no subscription, no licence gate. This is the single most
  consequential difference from `uklib`, which had to ship `[std]` proxies because the current
  CMI term-assurance tables are subscriber-only.
- The published PDF carries four complete tables — 生保標準生命表2018（死亡保険用）男 and 女,
  and 第三分野標準生命表2018 男 and 女 — each giving lx, dx, qx and e°x by single year of age
  from 0, with lx radix 100,000 [R4]. Values read off the 死亡保険用 tables:

  | 年齢 x | qx 男 | qx 女 |
  |---|---|---|
  | 20 | 0.00059 | 0.00025 |
  | 30 | 0.00068 | 0.00037 |
  | 35 | 0.00077 | 0.00059 |
  | 40 | 0.00118 | 0.00088 |
  | 50 | 0.00285 | 0.00197 |
  | 60 | 0.00653 | 0.00363 |
  | 65 | 0.01015 | 0.00484 |

  Also on the male 死亡保険用 table: lx(0) = 100,000, lx(30) = 98,850, lx(60) = 92,339,
  e°x(0) = 80.77 [R4].
- **The critical caveat**: 標準生命表2018（死亡保険用）is a **valuation** table carrying safety
  margins, not a best-estimate experience table. Any best-estimate mortality basis in this
  library is therefore a `[std]` adjustment of a sourced table, and every document must say
  which of the two it is using.
- **予定利率.** Japanese product documentation discloses the pricing basis more than US or UK
  documentation does — 日本生命 names 予定利率 and 予定死亡率 as the basis coefficients and warns
  that they differ between an in-force contract and a replacement [S7]. But **no carrier in
  this set publishes the 予定利率 of its 定期保険**; the disclosures relate to savings products.
  For a protection product the observable basis is the rate card (§5), not the parameters.
- **ESR.** 経済価値ベースのソルベンシー規制 applies from the **2026年3月期**, on three pillars
  [R6]. ESR = 適格資本 ÷ 所要資本, on a balance sheet where assets are all at fair value and
  liabilities are the current estimate of future cash flows re-based at the valuation date plus
  a **MOCE**, against the old SMR regime's locked-in liability basis. Supervisory ladder:
  **ESR < 100%** → 早期是正措置 第一区分 (improvement plan, restore to 100% within about a
  year); **< 70%** → 第二区分 (measures to strengthen payment capacity, restore to 70% within
  about six months); **< 35%** → 第三区分 (business suspension order, restore to 35% within
  about three months). The old trigger was **SMR < 200%** [R6]. At 2025年3月末 the 生保単体
  industry averages were **ESR 215%** against **SMR 873%**; the FSA attributes the gap to a
  stricter confidence level, wider risk coverage and greater sensitivity to the economic
  environment [R6].

---

## Variation across carriers

The drafting pass turns this into the product-spec's "Variations across insurers" section.
The observed range is given wherever more than one carrier states the parameter.

| Feature | Observed positions | Range |
|---|---|---|
| 契約年齢 (min) | 6 [S12]; 15 [S9] [S10]; 18 [S4]; 20 [S2] [S8]; 25 [S14] | **6–25**, mode 20 |
| 契約年齢 (max) | 65 [S2] [S10]; 69 [S8]; 70 (優良体) [S12]; 75 [S12] [S14]; 80 [S4] [S9] | **65–80** |
| 保険期間 menu | 10年 only [S8]; 10/20年 + 60/65歳満了 [S13]; 10/20/30年 + 65/80/90歳満了 [S4]; 年満了 10–30年 in 5s + 歳満了 60–80歳 in 5s [S2]; 10年 + 60/65/70/90歳満了 [S9]; 10年 + 55/60/65/70/75歳満了 [S10]; ≥5年 in 1-year steps [S14]; free 満了時年齢 within an envelope [S12] | one term to a fully free envelope |
| Renewal ceiling | 75 [S10]; 80 [S2] [S8] [S13]; 90 [S4] [S9]; 99 [S12] | **75–99**, mode 80 |
| Behaviour at the ceiling | truncate to a 歳満了 term [S2] [S8]; shorten year by year to expiry-age 90 [S4]; shorten **or lengthen** to reach the 指定年齢 [S7]; auto-convert to another product [S12] | four distinct rules |
| 保険金額 range | 100万–1,000万円 [S10]; 500万–3,000万円 [S2] [S13]; 100万/200万–1億円 [S9]; 100万/500万–1億円 banded by age [S4] | ceiling **1,000万–1億円** |
| Rate classes | 1 [S1] [S2] [S4] [S8] [S9] [S10]; 3 [S12]; 4 [S13] | **1–4** |
| Max preferred discount | 約14.5% (優良体) / 約30.6% (非喫煙者優良体) [S12]; 約54% [S13] | **~30%–~54%** |
| 解約返戻金 | none [S1] [S4] [S8] [S9] [S10] [S13] [S14]; **present, with 払済保険** [S12] | 7 : 1 |
| 配当 | 無配当 [S1] [S8] [S9] [S10] [S14]; 有配当2012 with accumulating dividends [S7] | 無配当 dominant |
| リビング・ニーズ特約 | 自動付加 [S2] [S3] [S7]; elective 特約 [S8] [S12]; **absent** [S4] | present in 7 of 8 |
| Living-needs cap | 3,000万円 per insured, aggregated [S1] [S7] [S8] [S12] | **no variation** |
| Living-needs term bar | no claim within 1 year of expiry unless renewable [S1] [S7] [S8] | **no variation** |
| Waiver of premium | in the main contract, accident + 180 days + 別表4 [S1] [S8] [S12] [S14]; in the main contract on 傷害 generally [S4]; sold as an optional 保険料払込免除特約 [S7] | main contract dominant |
| 猶予期間 (monthly) | ~1 month [S1] [S8]; ~2 months [S4]; **no grace — 催告 + 解除予定日 ~3 months** [S7] | **1–3 months** |
| 復活 | 3 years, 年6% compound interest on arrears [S1]; 3 years subject to health [S8]; **not offered** [S4] [S7] | 3 years or nothing |
| 自動振替貸付 | **absent** [S7]; 契約者貸付 also unavailable [S11, unverified] | absent on this chassis |
| Suicide exclusion | 3 years from 責任開始日 (or last 復活), running through renewals [S1] [S4] [S7] [S8] | **no variation** |
| Contestability | 2 years from 責任開始 (or last 復活), no claim event | **no variation** [S1] [S4] |
| Notice to decline renewal | 2 weeks [S1] [S8]; 1 month [S7]; 2 months [S4] | **2 weeks – 2 months** |
| Payment frequency | 月払 only [S4] [S8]; 月払/半年払/年払 [S1] [S3]; 1–12 months or lump [S10] | monthly always available |
| 高額割引 | 3,000万円 / 5,000万円 steps [S7]; present, thresholds unpublished [S9] [S14]; absent elsewhere | present at 3 of 8 |
| 逓減 mechanism | 基本保険金額 ÷ 保険期間 per year from year 2, **premium decreases too** [S14] | one carrier only |

**What does not vary.** Five things are identical across every carrier examined and should be
treated as the product's fixed spine, not as choices: (1) the death benefit and the
高度障害保険金 are the **same amount**, and either one terminates the contract; (2) the
高度障害状態 schedule is the same eight-item 別表3 with the same 備考 definitions; (3) the
suicide exclusion is **3 years** from 責任開始日, restarting only on 復活 and never on renewal;
(4) the contestability window is **2 years** on the same clock; (5) the living-needs benefit
is 指定保険金額 less six months' interest and premiums, capped at 3,000万円 per insured, and
barred within one year of a non-renewable expiry.

---

## Fetch failures and gaps

**URLs that could not be retrieved, or retrieved but not usable:**

- `https://www.jp-life.japanpost.jp/products/clause/pdf/teiki/202104/tik06.pdf` [S11] — HTTP
  200, 567 KB PDF downloaded, but both `pdftotext -enc UTF-8` and `pypdf` returned mojibake for
  nearly all glyphs and dropped every numeral. Two short fragments survived
  (「契約者貸付制度の利用はできません」 and 「保険金の倍額支払の制度はありません」); both are
  reported above as [unverified] rather than as [S11] facts. **What was lost**: かんぽ生命's
  policy-condition text — its 猶予期間, 復活, 免責事由 and 更新 clauses are therefore absent from
  the comparison, and かんぽ生命 appears in this file only through its product page [S10].
- `https://laws.e-gov.go.jp/law/407AC0000000105` — the human-facing e-Gov page is
  JavaScript-rendered and returns only site chrome to plain fetchers. **Recovered** by using
  the e-Gov API (`/api/1/lawdata/<lawId>`), which returns the full law as XML; the statute text
  in [R1] and [R2] is from that API, and both entries record the API URL used.
- `https://medical.life-direct.jp/sslt/hosyo.html` (メットライフ's 保険料率チェックシート) —
  HTTP 200, but the rate-class criteria are rendered inside an SVG image (`img_hosyo01_pc.svg`)
  and no criteria text or rate table is present in the HTML. **What was lost**: the numeric
  blood-pressure and body-size thresholds for メットライフ's four tiers, and its class names
  beyond 非喫煙優良体 and 標準体. Those names are therefore tagged [unverified] in §10.
- `https://www.metlife.co.jp/products/life/sslt/` [S13] — retrieved, but the same SVG problem
  affects the premium comparison chart, so メットライフ's four premium figures are not available
  as numbers; only the 約54% headline discount is.
- `https://www.fsa.go.jp/policy/economic_value-based_solvency/10.pdf` [R6] — the summarising
  fetcher returned undecodable binary and reported the PDF as corrupt. **Recovered** by
  `curl` with a browser User-Agent followed by `pdftotext`; the file is intact.
- `https://www.zurichlife.co.jp/product/category_shibou/teikihoken` [S9] — retrieved fine, but
  the summarising fetcher **misreported the premium table**, returning 2,512円 / 3,968円 /
  7,888円 for male 30/40/50 at 400万円 where the page actually says 628円 / 992円 / 1,972円.
  The figures in §5 are from a raw `curl` fetch and a grep of the page text. This is why every
  numeric table in this file was verified against raw HTML or extracted PDF text rather than
  taken from a summariser.
- `https://www.zurichlife.co.jp/product/category_shibou/teikihoken-test` — a stale URL found in
  search results for 定期保険プレミアムDX; it serves the 定期保険プラチナ content. The DX product
  is discontinued and no document for it was retrieved. The 非喫煙優良体型 criteria quoted in
  search snippets for that product (血圧 129/84 for ages 20–49, 139/89 for 50–69; cotinine
  saliva test) are **[unverified]** and are not used above.

**Claims left [unverified], and why:**

- **The current numeric 標準利率** for level-premium 第一分野 contracts. The mechanism is sourced
  [R5] [R2], but no retrieved document states the value in force. Secondary sources put the
  2017-04 level at 0.25% and describe a subsequent rise, and report insurers lifting 予定利率 on
  savings products through 2025–2026 to 1.75–2.08%; none of that is from a retrieved primary
  document and it is not used above.
- **The 予定利率 of any 定期保険 in this set.** No carrier publishes it for a protection product.
- **リビング・ニーズ特約 being free of charge.** No retrieved document states a nil 特約保険料 in
  terms. 日本生命 lists it among the 特約 that carry no 配当金 [S7], and the six-month
  interest-and-premium deduction supplies the economic reason, but the "normally free" claim is
  not verified.
- **メットライフ生命's four rate-class names**, and its numeric preferred-risk criteria (§10) —
  image-only, see above.
- **かんぽ生命's 契約者貸付 unavailability and its 倍額支払 absence** — from the two legible
  fragments of the unextractable [S11].
- **逓減定期保険 designs other than 大同生命's**, including the reported "steps down to 20% of
  the 基本保険金額" floor variant (§7) — search snippets only; no second 逓減 product document
  was retrieved.
- **チューリッヒ生命's 高額割引 thresholds** and **大同生命's 高額割引 thresholds** — stated to
  exist [S9] [S14] without published values. Only 日本生命's 3,000万円 / 5,000万円 steps are
  sourced [S7].
- **The terminal age (ω) of 標準生命表2018**. qx values were parsed positionally from [R4] and
  spot-checked against printed age labels up to the sixties; the tail of the extraction ran to
  qx ≈ 0.69 (male) and 0.76 (female) without reaching 1, which suggests the extraction did not
  capture the final rows. Ages 20–65 as tabulated in §15 are verified; the terminal age is not.
- **標準生命表2018（年金開始後用）** — the 2018 PDF [R4] contains the 死亡保険用 and 第三分野
  tables only. Whether a 2018-vintage 年金開始後用 table exists was not established here; it is
  the `individual_annuity` product's problem, not this one's.
- **Whether ライフネット生命 offers any terminal-illness-style acceleration** under a different
  name. The word リビング does not occur in [S4]; no substitute rider was found; but a
  categorical "this carrier has no acceleration benefit" was not confirmed against a product
  list.

**Deliberate scope limits (not gaps):**

- 団体定期保険 (group term) and 収入保障保険 are out of scope here; the latter is the
  `income_guarantee` product and states its deltas against this chassis.
- 法人向け 長期平準定期保険 and 逓増定期保険 (the corporate tax-driven designs) were not
  researched; 大同生命's 逓減 product [S14] is quoted for its 逓減 mechanism only, and it is
  offered on both a 法人 and a 個人 basis.
- Reinsurance terms, commission structures and lapse experience by duration: no Japanese
  equivalent of the FCA's published pure-protection lapse data was found in this session, and
  none is asserted. A best-estimate lapse basis will have to be `[std]`.
