# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/term-life.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the R-numbering has gaps: R6 and R8 are not cited, because the cross-product
reference library carries the same two documents as [REG-R15] and [REG-R45] with fuller
annotations. Every S# entry is cited, including [S11], which is listed precisely because
it could **not** be read. Access date for all sources: 2026-08-20. No sources were newly
added at drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

Company and branded product names appear in this file and in `_research/term-life.md` and
nowhere else in the library. In `product-spec.md` and `technical-notes.md` a carrier is its
tag alone, so a reader can always resolve who said what — here — and never has to.

---

## Primary product sources

Nine carriers, fourteen documents. Five are full 約款 (*yakkan*, policy conditions) or
booklets containing them [S1] [S4] [S6] [S7] [S8]; one is a 約款 extract that could not be
text-extracted [S11]; one is a product brochure [S12]; and seven are consumer or
specification pages [S2] [S3] [S5] [S9] [S10] [S13] [S14]. **Four documents carry a
published premium scale** — two a full sex × age × sum-assured grid [S2] [S9], one a
sex × age table per ¥1,000,000 of cover, before and after a repricing [S10], and one a
sex × age table at a single sum assured [S12] — with a fifth publishing single worked
examples [S5]. That is the single largest documentary difference from `uklib`, where no
premium basis is observable at all.

(jplib-term_life-s1)=

### S1 — オリックス生命保険株式会社, 「無配当 無解約払戻金型定期保険（インターネット申込専用） ご契約のしおり／約款」 (policy booklet and conditions)

- Publisher: オリックス生命保険株式会社
- Document: ご契約のしおり／約款 for ネット専用定期保険Bridge［ブリッジ］, 2015年10月版, form
  mark `30ＫＩ07`; 117 PDF pages (しおり 1–56, then 約款 renumbered 1–58)
- Doc type: ご契約のしおり・約款
- URL: https://www.orixlife.co.jp/life/bridge/pdf/yakkan_br_20151002.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.88 MB PDF; `pdftotext` recovered all 約款 article
  text and most しおり body text. Display-typeset cover and diagram pages use a subset font
  poppler could not map and extracted as mojibake; no fact cited to [S1] rests on them.)
- The most complete document in the set — 約款 articles 1–40, the リビング・ニーズ特約条項,
  別表3 and 別表4 — and the source of the composite's benefit, exclusion, grace,
  reinstatement and renewal mechanics.

(jplib-term_life-s2)=

### S2 — オリックス生命保険株式会社, ネット専用定期保険Bridge 商品ページ (consumer page with a published rate card)

- Publisher: オリックス生命保険株式会社
- Document: 商品ページ with a 月払保険料例 grid, rates as at 2025-07-01
- Doc type: 商品ページ (consumer)
- URL: https://www.orixlife.co.jp/life/bridge/
- Accessed: 2026-08-20. Retrieved: YES (fetched twice — once through a summarising fetcher,
  once raw with `curl` and grepped, to verify the figures character-for-character)
- Supplies the anchor premium and the policy-fee decomposition.

(jplib-term_life-s3)=

### S3 — オリックス生命保険株式会社, ネット専用定期保険Bridge 商品詳細ページ (product specification page)

- Publisher: オリックス生命保険株式会社
- Doc type: 商品詳細 (product specification page)
- URL: https://www.orixlife.co.jp/life/bridge/detail.html
- Accessed: 2026-08-20. Retrieved: YES

(jplib-term_life-s4)=

### S4 — ライフネット生命保険株式会社, 「定期死亡保険（無配当・無解約返戻金型） ご契約のしおり・約款」 (policy booklet and conditions)

- Publisher: ライフネット生命保険株式会社
- Document: ご契約のしおり・約款, 2026年6月版, form mark `LN_BB_GAP-25`; 45 PDF pages
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_teiki_latest.pdf
  (linked from https://www.lifenet-seimei.co.jp/policy/yakkan/)
- Accessed: 2026-08-20. Retrieved: YES (758 KB PDF, text extracted cleanly and read; only
  the しくみ図 diagram is glyph-garbled)
- The only document publishing a 無解約返戻金型 versus 解約返戻金あり premium and value
  comparison, and the only one stating in terms that 復活 is not offered.

(jplib-term_life-s5)=

### S5 — ライフネット生命保険株式会社, 定期死亡保険 商品ページ (consumer page with published premium examples)

- Publisher: ライフネット生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.lifenet-seimei.co.jp/product/life/
- Accessed: 2026-08-20. Retrieved: YES

(jplib-term_life-s6)=

### S6 — ライフネット生命保険株式会社, 「かぞくへの保険 定期死亡保険（無配当・無解約返戻金型）普通保険約款」 (superseded policy conditions, 2009年12月版)

- Publisher: ライフネット生命保険株式会社
- Document: 普通保険約款 only, 2009年12月; 21 numbered pages P-1…P-21
- Doc type: 普通保険約款 (superseded edition, retained on the publisher's site)
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_policy_200912_001.pdf
- Accessed: 2026-08-20. Retrieved: YES (304 KB PDF, text extracted and read)
- Cited for one point: its 第1条 already states that 満期保険金, 配当 and 解約返戻金 are all
  absent, so the no-surrender-value design is long-standing rather than a recent artefact.

(jplib-term_life-s7)=

### S7 — 日本生命保険相互会社, 「ニッセイみらいのカタチ ご契約のしおり－定款・約款」 (policy booklet, articles and conditions)

- Publisher: 日本生命保険相互会社
- Document: ご契約のしおり－定款・約款, 2026年4月改訂, しおり番号 ２０２６０４Ａ; 182 PDF pages
  (file `01.pdf` of the booklet set)
- Doc type: ご契約のしおり・定款・約款
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/shiori/01.pdf
- Accessed: 2026-08-20. Retrieved: YES, PARTIAL (12.3 MB PDF; running text extracts cleanly
  with both `pdftotext` and `pypdf`, but a substantial minority of display-typeset pages,
  including many diagram captions, are glyph-garbled in both. Facts cited to [S7] come only
  from passages that extracted as clean Japanese.)
- The only 有配当 product in the set, the only 全期型／更新型 taxonomy stated by name, the only
  carrier that both shortens and lengthens a term at the renewal ceiling, and the document
  that states this product has no 自動振替貸付制度.

(jplib-term_life-s8)=

### S8 — アクサ生命保険株式会社, 「定期保険（無解約返戻金型） 重要事項説明書／ご契約のしおり／約款」 (pre-contract disclosure, booklet and conditions)

- Publisher: アクサ生命保険株式会社 (sold as アクサダイレクトの定期保険2; the booklet names
  アクサ生命 as 引受保険会社)
- Document: 重要事項説明書（契約概要・注意喚起情報）plus ご契約のしおり plus 約款; 84 PDF pages
- Doc type: 重要事項説明書／ご契約のしおり／約款
- URL: https://www.axa-direct-life.co.jp/pdf/yakkan_l.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.25 MB PDF, text extracted and read; only the
  cover and two しくみ図 are glyph-garbled)
- The narrowest envelope in the set, and the carrier that states the renewal-ceiling
  truncation band numerically.

(jplib-term_life-s9)=

### S9 — チューリッヒ生命保険株式会社, 定期保険プラチナ 商品ページ (consumer page with published rate cards)

- Publisher: チューリッヒ生命保険株式会社
- Document: 商品ページ with four 月払保険料 tables, rates as at 2026年7月
- Doc type: 商品ページ (consumer)
- URL: https://www.zurichlife.co.jp/product/category_shibou/teikihoken
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped. A summarising
  fetcher returned 2,512円/3,968円/7,888円 where the page says 628円/992円/1,972円 — which is
  why every numeric table in the research file was verified against raw HTML or extracted
  PDF text.)
- Publishes grids for both a 10年更新 and a 90歳満了 design, so the price of renewal risk can
  be read off published figures.

(jplib-term_life-s10)=

### S10 — 株式会社かんぽ生命保険, 定期保険「新普通定期保険」商品ページ (consumer page with a published rate card)

- Publisher: 株式会社かんぽ生命保険
- Document: 商品ページ, page mark `Ⅱ W 2026.05 14036`, rates before and after the 2026-05-02
  repricing
- Doc type: 商品ページ (consumer)
- URL: https://www.jp-life.japanpost.jp/products/teiki/index.html
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped)
- The public-sector writer: an order of magnitude below the private ceiling on sum assured,
  and the only rate card disclosing base and rider components separately.

(jplib-term_life-s11)=

### S11 — 株式会社かんぽ生命保険, 「普通定期保険（新普通定期保険） ご契約のしおり・約款」抜粋 (policy conditions extract, 2021年4月版)

- Publisher: 株式会社かんぽ生命保険
- Document: the 定期保険 chapter of the ご契約のしおり・約款, 2021年4月版
- Doc type: ご契約のしおり・約款 (extract)
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/teiki/202104/tik06.pdf
- Accessed: 2026-08-20. **Retrieved: NO** (567 KB PDF downloaded successfully — HTTP 200 —
  but both `pdftotext -enc UTF-8` and `pypdf` returned mojibake for almost all body glyphs
  and dropped every numeral. Two short fragments survived and are reported as [unverified].)
- Listed rather than dropped because the absence is a documented limit: this carrier's
  猶予期間, 復活, 免責事由 and 更新 clauses are missing from the comparison.

(jplib-term_life-s12)=

### S12 — FWD生命保険株式会社, 「FWD定期／FWD優良体定期」パンフレット (product brochure)

- Publisher: FWD生命保険株式会社
- Document: brochure covering FWD定期 and FWD優良体定期
- Doc type: 商品パンフレット
- URL: https://www.fwdlife.co.jp/files/v3/assets/blt52d7347d77fa3188/blt37f9884b94b1358b/64cb39878403820965f252d5/teikihoken.pdf
- Accessed: 2026-08-20. Retrieved: YES (4.27 MB PDF, text extracted and read)
- The exception that stops the composite assuming a Japanese term policy has no cash value:
  the only product in the set with a 解約返戻金 and a 払済保険 conversion. Also publishes a
  three-tier rate class with its discount percentages and full underwriting criteria.

(jplib-term_life-s13)=

### S13 — メットライフ生命保険株式会社, スーパー割引定期保険 商品ページ (consumer product page)

- Publisher: メットライフ生命保険株式会社
- Doc type: 商品ページ (consumer)
- URL: https://www.metlife.co.jp/products/life/sslt/
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped. The numeric
  rate-class criteria and the premium comparison chart live inside SVG images and were not
  recoverable as text, so only the headline discount is usable as a number.)
- The four-tier risk-segmented design, the class fixed at issue and carried unchanged
  through every renewal, and the carrier's statement that applying a risk-segmented rate is
  *why* there is no 解約返戻金.

(jplib-term_life-s14)=

### S14 — 大同生命保険株式会社, 「定期保険 Dタイプ（保険料逓減型）」個人向け 商品ページ (product specification page)

- Publisher: 大同生命保険株式会社
- Document: 商品ページ, page mark `H-2026-0004①（2026年5月27日）`, content as at 2026年6月
- Doc type: 商品ページ (product specification)
- URL: https://www.daido-life.co.jp/join/c_kojin/lineup/muhaid_teigen/
- Accessed: 2026-08-20. Retrieved: YES (fetched raw with `curl` and grepped)
- The 逓減定期保険 comparison point: the only retrieved document stating a decreasing-cover
  mechanism as a formula, and the only one in which the **premium** decreases with the cover.

---

## Regulatory and actuarial references

(jplib-term_life-r1)=

### R1 — e-Gov 法令検索 (デジタル庁), 保険業法 第3条（生命保険業免許と第一分野の定義）

- Publisher: e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- Doc type: statute
- URL (human): https://laws.e-gov.go.jp/law/407AC0000000105 — URL (machine, used):
  https://laws.e-gov.go.jp/api/1/lawdata/407AC0000000105
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (3.7 MB XML; the human-facing page
  is a JavaScript single-page app returning only site chrome to plain fetchers)
- Cited for what the cross-product entry does not carry: the parenthesis in 第3条第4項第1号
  bringing 「余命が一定の期間以内であると医師により診断された身体の状態」 inside the
  first-sector licence — the statutory footing of リビング・ニーズ特約.

(jplib-term_life-r2)=

### R2 — e-Gov 法令検索, 保険業法施行規則 第68条・第69条（標準責任準備金の対象契約と積立方式）

- Publisher: e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- Doc type: ministerial ordinance
- URL (machine, used): https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005
- Accessed: 2026-08-20. Retrieved: YES via the e-Gov API (30.2 MB XML)
- Cited for 第69条第4項第2号, which defines the 平準純保険料式 floor **in line** as levelling
  the funding across the whole premium-paying period.

(jplib-term_life-r3)=

### R3 — 公益社団法人 日本アクチュアリー会, 「標準生命表2018」公開ページ (institutional page)

- Publisher: 公益社団法人 日本アクチュアリー会
- Doc type: 専門情報ページ
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Accessed: 2026-08-20. Retrieved: YES
- The Institute's own account of its 指定法人 status under 保険業法第122条の2第1項 and of the
  2018 revision's timetable, applying from 2018年4月.

(jplib-term_life-r4)=

### R4 — 公益社団法人 日本アクチュアリー会, 「標準生命表２０１８」 (mortality tables)

- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８, 5 PDF pages; four tables — 生保標準生命表２０１８（死亡保険用）
  男 and 女, 第三分野標準生命表２０１８ 男 and 女 — each with lx, dx, qx and e°x by single year
  of age from 0, radix 100,000
- Doc type: mortality table (statutory valuation basis)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (236 KB PDF, text extracted, qx parsed positionally
  by age and spot-checked against the printed age labels)
- Cited for the individual 死亡保険用 qx values quoted in the product documents. The terminal
  age was **not** confirmed in this pass — the extraction ran to qx ≈ 0.69 (male) without
  reaching 1.00000 — so terminal ages are cited to [REG-R18], where they were read.

(jplib-term_life-r5)=

### R5 — 金融庁, 平成8年大蔵省告示第48号（標準責任準備金の係数）改正案の公表

- Publisher: 金融庁
- Document: 「…（平成８年大蔵省告示第48号）等の一部を改正する件（案）」の公表について, 平成28年4月27日
- Doc type: パブリックコメント公表ページ (three 別紙 PDFs, not opened)
- URL: https://www.fsa.go.jp/news/27/hoken/20160427-2.html
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched raw and read)
- The regulator's plain-language statement that the 標準利率 derives from an 指標金利 built on
  JGB yield averages with 安全率係数 applied, and that the 2016 amendment added a coefficient
  for indicator rates at or below 0%.

(jplib-term_life-r7)=

### R7 — 国税庁, タックスアンサー No.1140「生命保険料控除」

- Publisher: 国税庁 (National Tax Agency)
- Doc type: タックスアンサー (tax authority guidance)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES
- The post-2012 三区分 and the 所得税 deduction schedules for 新契約 and 旧契約, with the
  120,000円 overall cap. The page does not carry the 住民税 schedule; that is cited to [S4].

(jplib-term_life-r9)=

### R9 — 公益財団法人 生命保険文化センター, 「2024（令和6）年度 生命保険に関する全国実態調査＜速報版＞」

- Publisher: 公益財団法人 生命保険文化センター, 2024年11月
- Doc type: household survey (speed-report edition)
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.74 MB PDF, text extracted, summary and 図表Ⅰ-70
  read)
- Distinct from [REG-R32], which reads the same survey's workbooks: the summary means that
  [REG-R32] flags as [unverified] there — 世帯加入率 89.2%, 世帯普通死亡保険金 1,936万円,
  世帯年間払込保険料 35.3万円 — and the product mix of the most recently bought policy were
  read from this PDF here.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md`, whose
own R1–R47 numbering is distinct from this file's and is likewise frozen. Within that page
plain [R#] refers to its own entries, so the two schemes must never be read across. Entries
cited by the term life documents, all accessed 2026-08-20:

- **REG-R1** — 保険業法 第3条: the 第一分野 / 第三分野 licence split. retrieved: yes.
- **REG-R2** — 保険業法 第4条: the 算出方法書 holding 予定利率, 予定死亡率 and 予定事業費率 is
  not published — the reason every pricing-basis parameter here is **[std]**. retrieved: yes.
- **REG-R4** — 保険業法 第116条: the delegation the 標準責任準備金 chain hangs on. retrieved: yes.
- **REG-R6** — 保険業法 第121条: the 意見書, and behind it the 1号収支分析. retrieved: yes.
- **REG-R7** — 施行規則 第68条: which contracts are standard-reserve contracts. retrieved: yes.
- **REG-R8** — 施行規則 第69条: the four-way reserve taxonomy. retrieved: yes.
- **REG-R10** — 告示第48号: 平準純保険料式, table vintages, 標準利率 reset machinery.
  retrieved: yes, but from an unofficial consolidated mirror — see the entry.
- **REG-R11** — 告示48号改正 (2017): 標準生命表2018 from 2018-04-01. retrieved: yes.
- **REG-R14** — 監督指針（本編）: 契約締結前交付書面 contents, including the requirement to
  disclose 払込猶予期間・失効・復活, and IV-1-12 on 自動振替貸付 as an election. retrieved: yes.
- **REG-R15** — ESR の概要: commencement 2026-03-31, the 100% trigger, 現在推計+MOCE, 99.5%.
  retrieved: yes.
- **REG-R16** — ESR 政策ページ（告示の索引）: the index to the 柱告示. retrieved: yes, but the
  individual 告示 PDFs were **not opened**, which is why the standard-model treatment of a
  no-underwriting auto-renewal — the contract-boundary question — is [unverified] here.
- **REG-R17** — ソルベンシー・マージン比率: the old 200% threshold. retrieved: **no** — the
  告示 was not located; the entry rests on [REG-R14] and [REG-R15].
- **REG-R18** — 標準生命表2018 PDF: the freely readable valuation table, verified spot rates
  and terminal ages. retrieved: yes.
- **REG-R20** — 作成概要: the 2σ margin, the improvement allowance, the 保険年齢 basis, and
  the fact that the 死亡保険用 table **includes** 高度障害 in its death rate. retrieved: yes.
- **REG-R21** — IAJ 索引と利用規約: redistribution is restricted, so the library ships a
  **[std]** table citing the IAJ entries rather than a copy. retrieved: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析, at least ten future years, by segment.
  retrieved: yes.
- **REG-R31** — 生命保険の動向 2025年版: in-force and new-business mix, and the 5.6% industry
  解約・失効率. retrieved: yes.
- **REG-R32** — 全国実態調査 2024年度 workbooks: penetration and premium bands. retrieved: yes.
- **REG-R34** — 保険法 第51条: the statutory suicide exclusion has **no** time limit, so the
  three-year 免責期間 is contractual and a per-carrier fact. retrieved: yes.
- **REG-R35** — 保険法 第55条: the five-year contestability ceiling and one-month discovery
  clock bounding the carriers' two-year windows. retrieved: yes.
- **REG-R36** — 保険業法 第309条: the eight-day dispatch-rule クーリング・オフ, scoped out here.
  retrieved: yes.
- **REG-R40** — 生命保険契約者保護機構: 90% of the 責任準備金 on failure. retrieved: yes (Q1
  page; the 高予定利率契約 page was not opened).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation setting that rate. retrieved: yes.
- **REG-R43** — 所得税法 第76条: three baskets of ¥40,000 capped at ¥120,000. retrieved: yes.
- **REG-R44** — 相続税法 第12条: ¥5,000,000 × the number of statutory heirs. retrieved: yes.
- **REG-R45** — タックスアンサー No.4114: the administration's mechanics for that exemption.
  retrieved: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan. retrieved: yes.

---

## Provenance note

Extraction details — which fact came from which document, the per-carrier comparison
tables, and the register of fetch failures and [unverified] claims (the current numeric
標準利率, the 予定利率 of any protection product, whether リビング・ニーズ特約 is free of
charge, one carrier's four rate-class names, the 標準生命表2018 terminal age as parsed in
this pass, and the unextractable [S11]) — live in `_research/term-life.md`, the citation
ground truth for the S# and R# numbering used here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R18]: #jplib-reg-r18
[REG-R32]: #jplib-reg-r32
[REG-R45]: #jplib-reg-r45
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
