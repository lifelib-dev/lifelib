# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/whole-life.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps: R3 (「標準生命表２０１８の作成過程」) is not cited by the product
documents, because the file downloads but its body text is unreadable under both PDF text
extractors tried, and no fact in this product rests on it. Access date for all sources:
2026-08-20. No sources were newly added at drafting. Cross-product [REG-R#] tags are listed
in their own section at the end.

Seven carriers are represented in the primary set, plus an eighth for the 一時払 予定利率 (*yotei
riritsu*, assumed interest rate) disclosure. Company and branded product names appear in
this file and in `_research/whole-life.md` and **nowhere else** in the library: in
`product-spec.md`, `technical-notes.md`, `model.md` and the model docstrings a carrier is
referred to by its [S#] tag alone.

---

## Primary product sources

(jplib-whole_life-s1)=

### S1 — アフラック生命保険, "アフラックの終身保険 ご契約のしおり・約款" (policy booklet and policy conditions)

- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: ご契約のしおり・約款 アフラックの終身保険, file `syushin_77888601.pdf`, 171 pp. Contains
  「終身保険普通保険約款」 (制定 2018年4月2日) plus 定期特約, 災害死亡割増特約, 傷害特約, リビング・ニーズ特約 and 非喫煙割引特約 (all 制定
  2018年4月2日), and 別表1–51
- Doc type: policy booklet and policy conditions (ご契約のしおり・約款)
- URL: https://www.aflac.co.jp/yakkan/pdf/syushin_77888601.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 171 pp., text extracted with
  PyMuPDF; the ordinary-whole-life articles 1–35 read in full)

(jplib-whole_life-s2)=

### S2 — アフラック生命保険, "積立利率等・約款貸付の利率のお知らせ" (published rate schedule)

- Publisher: アフラック生命保険株式会社
- Document: company web page, rates stated 「2017年2月1日現在」
- Doc type: published rate disclosure (company web page)
- URL: https://www.aflac.co.jp/reserving_loan_rate.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 403 to plain fetchers; retrieved with a browser
  User-Agent, HTTP 200, server-rendered HTML, rate tables read)

(jplib-whole_life-s3)=

### S3 — オリックス生命保険, "無配当 終身保険（低解約払戻金型）ご契約のしおり／約款" (policy booklet and conditions)

- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: Web約款 `webyakkan_rise_20240402.pdf` (2024年4月2日版), 164 pp., containing
  「無配当終身保険（低解約払戻金型）普通保険約款」 and its 特約条項・特則
- Doc type: policy booklet and policy conditions
- URL: https://www.orixlife.co.jp/customer/webclause/pdf/webyakkan_rise_20240402.pdf
  (index page: https://www.orixlife.co.jp/customer/webclause/)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 164 pp., text extracted and
  read). This is the source of the 約款 wording of the 低解約払戻金 mechanic — art. 33.

(jplib-whole_life-s4)=

### S4 — オリックス生命保険, "終身保険 商品パンフレット" (brochure with rate and value tables)

- Publisher: オリックス生命保険株式会社
- Document: `rise_pamphlet.pdf`, 5 pp.; the 月払保険料表 is headed 「2025年12月2日現在（単位：円）」
- Doc type: product brochure (with published premium and surrender-value tables)
- URL: https://www.orixlife.co.jp/life/rise/pdf/rise_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded; the tables recovered by
  positional word extraction — a plain text dump scrambles the multi-column layout). **The
  single most valuable numeric source for this product:** a published surrender-value table
  at eight durations for one model point, and a published premium table by issue age, sex
  and sum assured.

(jplib-whole_life-s5)=

### S5 — オリックス生命保険, "お申込みにあたって（取扱いの内容）" (application terms page)

- Publisher: オリックス生命保険株式会社
- Document: `rise2_pamphlet.pdf`, 3 pp.
- Doc type: product brochure (application terms page)
- URL: https://www.orixlife.co.jp/life/rise/pdf/rise2_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded; the eligibility grid recovered
  by positional extraction)

(jplib-whole_life-s6)=

### S6 — オリックス生命保険, "「ライズ」の低解約払戻期間とは何ですか？" (customer FAQ page)

- Publisher: オリックス生命保険株式会社
- Doc type: customer FAQ page
- URL: https://faq.orixlife.co.jp/faq_detail.html?id=100574
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). The page defines the suppressed period
  and states that it equals the premium-paying period; it does **not** state the percentage,
  which comes from [S3] and [S4].

(jplib-whole_life-s7)=

### S7 — 東京海上日動あんしん生命保険, "5年ごと利差配当付低解約返戻金型終身保険／5年ごと利差配当付終身保険" (booklet and conditions)

- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: 契約概要・注意喚起情報・ご契約のしおり・約款, 2010.3改定, 292 pp.; 契約例 calculation base date 平成22年3月2日;
  募資番号 '09-KF04-019 / -020
- Doc type: pre-contract summary + policy booklet + policy conditions, in one booklet
- URL: https://ykn.tmn-anshin.co.jp/affix/yakkan2/nagawari/D79-11660/MCNG9C0_%E9%95%B7%E5%89%B2%E3%82%8A%E7%B5%82%E8%BA%AB.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 292 pp.). Extraction note:
  pypdf returns mojibake for this file (CID-encoded subset fonts); PyMuPDF extracts it
  cleanly, and every fact drawn from it comes from the PyMuPDF extraction. **The only source
  in the set that publishes the suppressed and unsuppressed versions of the same product
  side by side**, with both premium scales and both surrender-value tables. Its 2010 pricing
  basis is dated; its mechanics are not.

(jplib-whole_life-s8)=

### S8 — 日本生命保険相互会社, "ニッセイみらいのカタチ ご契約のしおり 定款・約款" (policy booklet, articles and conditions)

- Publisher: 日本生命保険相互会社
- Document: しおり番号 202604A, 2026年4月改訂, 182 pp.; the whole life component is 「終身保険（有配当2012）」
- Doc type: policy booklet + articles of association + policy conditions
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/shiori/01.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 182 pp., text extracted and
  read). Cited chiefly as the **counter-example on lapse mechanics**: no 自動振替貸付, no
  reinstatement, and a scheduled 解除 in place of 失効.

(jplib-whole_life-s9)=

### S9 — 株式会社かんぽ生命保険, "終身保険 ご契約のしおり・約款 2026年上半期版" (policy booklet and conditions)

- Publisher: 株式会社かんぽ生命保険 (Japan Post Insurance Co., Ltd.)
- Document: `syusin_2026_05.pdf`, 448 pp., 「この冊子の記載内容は、2026年5月2日現在の取り扱いを説明しております」; covers
  普通終身保険（Ｒ07）, 特別終身保険（Ｒ07） and both （低解約返戻金型） variants
- Doc type: policy booklet and policy conditions
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/syusin/202605/syusin_2026_05.pdf
  (index: https://www.jp-life.japanpost.jp/products/clause/syusin/index.html)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 448 pp., text extracted; the
  four 普通保険約款 and the contract-handling chapters read). Carries the suppression factor as a
  literal 約款 multiplier, the statutory 加入限度額, and a loan-default mechanic that reduces the
  sum assured instead of lapsing the contract. It publishes **no** numeric surrender-value
  or premium table.

(jplib-whole_life-s10)=

### S10 — 第一生命保険, "５年ごと配当付終身保険普通保険約款" (policy conditions)

- Publisher: 第一生命保険株式会社
- Document: `01_10334_002.pdf`, 24 pp., 約款 archive folder `01_2014_01_1` (the worked date
  examples in the text use 契約日 平成26年5月1日, i.e. a 2014 vintage)
- Doc type: policy conditions (普通保険約款 only — no しおり in this file)
- URL: https://event.dai-ichi-life.co.jp/yakkan/01_2014_01_1/pdf/01_10334_002.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 24 pp., text extracted and read
  in full). A compact, cleanly drafted ordinary whole life 約款; the source of the
  half-yearly-cycle 自動振替貸付 variant and of the ステップ払込方式 特則.

(jplib-whole_life-s11)=

### S11 — 三井住友海上あいおい生命保険, "終身保険／積立利率変動型終身保険／積立利率変動型終身保険（低解約返戻金型）／積立型終身保険 ご契約のしおり・約款"

- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: `L6095-1.pdf`, 586 pp., 2010.3改定 (申込番号 L6095-1, 2010.04)
- Doc type: policy booklet and policy conditions
- URL: https://www.msa-life.co.jp/customer/msa/yakkan/L6095-1.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 586 pp., text extracted; the
  extraction contains NUL bytes and must be stripped before searching). Source of a third
  independent statement of the 70% suppression factor, of the split of the suppressed value
  on an 積立利率変動型 chassis, of the 積立利率 formula, and of the only level-premium 予定利率 figure
  recovered in the research pass — which carries a 2010 date.

(jplib-whole_life-s12)=

### S12 — 明治安田生命保険, "円貨建一時払商品に適用される予定利率" (published rate disclosure)

- Publisher: 明治安田生命保険相互会社
- Document: company rate page, 適用期間 2026年8月16日～2026年8月31日
- Doc type: published rate disclosure (company web page)
- URL: https://www.meijiyasuda.co.jp/norapl/find/rate/yencommon/planned_interest_rate/
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). Cited for the 一時払 scope boundary: it is
  the clearest public evidence that Japanese insurers disclose the pricing interest rate on
  single-premium products, and that they do not disclose it on level-premium ones.

---

## Regulatory and actuarial references

(jplib-whole_life-r1)=

### R1 — 日本アクチュアリー会, 「標準生命表２０１８」 (the tables themselves)

- Publisher: 公益社団法人日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: `seimeihyo2018.pdf`, 5 pp. — 生保標準生命表2018（死亡保険用）男/女 and 第三分野標準生命表2018 男/女, each
  with x, l(x), d(x), q(x) and e(x) on a radix of 100,000
- Doc type: statutory valuation mortality table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (downloaded; values recovered by positional word
  extraction with PyMuPDF — a naive text dump interleaves the two column blocks). The
  shorter URL `.../standard-life-table/seimeihyo2018.pdf` seen in search results is a 404
  page served with HTTP 200; the `/pdf/` path segment is required.

(jplib-whole_life-r2)=

### R2 — 日本アクチュアリー会, 「標準生命表２０１８の作成概要」 (methodology note)

- Publisher: 公益社団法人日本アクチュアリー会
- Document: `seimeihyo2018-gaiyo.pdf`, 6 pp., 資料①–⑤
- Doc type: methodology note
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (downloaded, all six pages text-extracted and read).
  The document that establishes 標準生命表2018 as a **valuation** table carrying an explicit
  roughly-2σ margin and a forward improvement allowance, not a best-estimate table.

(jplib-whole_life-r4)=

### R4 — 日本アクチュアリー会, 「標準生命表2018」 索引ページ (publication page)

- Publisher: 公益社団法人日本アクチュアリー会
- Doc type: publication page
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). Publication and application dates, the
  statement that the Institute is a body designated under 保険業法第122条の2第1項 and is commissioned
  by 金融庁 to produce the tables, and the three PDF download paths.

(jplib-whole_life-r5)=

### R5 — e-Gov 法令検索, 保険業法（平成七年法律第百五号）第114条・第116条・第122条の2

- Publisher: e-Gov 法令検索 (デジタル庁)
- Doc type: primary legislation (articles)
- URL: https://laws.e-gov.go.jp/document?lawid=407AC0000000105 (retrieved through the JSON
  API at `https://laws.e-gov.go.jp/api/2/law_data/407AC0000000105`)
- Accessed: 2026-08-20. Retrieved: YES (full law JSON downloaded via the v2 API with a
  browser User-Agent; the three articles extracted verbatim from the `law_full_text` tree).
  第114条 is the 契約者配当 fair-and-equitable standard, 第116条 the 責任準備金 duty and its delegation,
  第122条の2 the 指定法人 designation.

(jplib-whole_life-r6)=

### R6 — e-Gov 法令検索, 保険業法施行規則（平成八年大蔵省令第五号）第30条の2・第64条・第68条・第69条

- Publisher: e-Gov 法令検索 (デジタル庁)
- Doc type: ministerial ordinance (articles)
- URL: https://laws.e-gov.go.jp/document?lawid=408M50000040005 (JSON API:
  `https://laws.e-gov.go.jp/api/2/law_data/408M50000040005`; the revision returned is
  `408M50000040005_20260615_508M60000002055`)
- Accessed: 2026-08-20. Retrieved: YES (full ordinance JSON downloaded, ~4.7 MB; the four
  articles extracted verbatim). 第68条 the standard-reserve scope and its exclusions, 第69条 the
  four reserve components and the 平準純保険料式 floor, 第30条の2 the four surplus-distribution
  methods, 第64条 the 契約者配当準備金.

(jplib-whole_life-r7)=

### R7 — 金融庁, 「標準責任準備金制度にかかる告示の一部改正（案）」等の公表について

- Publisher: 金融庁 (Financial Services Agency)
- Doc type: rule-making publication page
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). Identifies the two 告示 that carry the
  標準責任準備金 regime — 平成13年金融庁告示第24号 and 平成8年大蔵省告示第48号 — and the amendment bringing USD- and
  AUD-denominated contracts into scope, with effective dates and links to 別紙1–3.

(jplib-whole_life-r8)=

### R8 — 金融庁, 平成八年大蔵省告示第四十八号 改正（別紙２ — the 標準利率 mechanism）

- Publisher: 金融庁
- Document: `02.pdf`, 16 pp. — a 改正後／改正前 two-column redline of the notification made under
  保険業法第116条第2項 prescribing the reserve accumulation method and the level of the assumed
  mortality and other coefficients
- Doc type: ministerial notification (告示), amendment text
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/02.pdf
- Accessed: 2026-08-20. Retrieved: YES (downloaded, 16 pp.). Extraction note: the
  notification is set in vertical Japanese, PyMuPDF returns one character per line, and the
  two redline columns interleave — the text must be re-joined before it can be read. Several
  rate tables are printed as 「［表略］」 in the redline and are therefore **not** recoverable
  from this file, including the 安全率係数 table for the annual (non-single-premium) case.

(jplib-whole_life-r9)=

### R9 — e-Gov 法令検索, 相続税法（昭和二十五年法律第七十三号）第3条・第12条

- Publisher: e-Gov 法令検索 (デジタル庁)
- Doc type: primary legislation (articles)
- URL: https://laws.e-gov.go.jp/document?lawid=325AC0000000073 (JSON API:
  `https://laws.e-gov.go.jp/api/2/law_data/325AC0000000073`)
- Accessed: 2026-08-20. Retrieved: YES (full law JSON downloaded; both articles extracted
  verbatim). 第3条第1項第1号 deems a death benefit acquired by inheritance in the proportion of
  the premiums the decedent bore; 第12条第1項 states the heirs' exempt amount as a formula in
  the statute itself.

(jplib-whole_life-r10)=

### R10 — 国税庁, タックスアンサー No.4114 「相続税の課税対象になる死亡保険金」

- Publisher: 国税庁 (National Tax Agency)
- Doc type: official tax guidance page (basis stated as 令和7年4月1日現在法令等)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4114.htm
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). The `/zaisan/4114.htm` path that appears
  in some search results is a dead link; `/sozoku/4114.htm` is the live one.

(jplib-whole_life-r11)=

### R11 — 国税庁, タックスアンサー No.1140 「生命保険料控除」

- Publisher: 国税庁
- Doc type: official tax guidance page (basis stated as 令和7年4月1日現在法令等)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). The three post-2012 baskets, the new- and
  old-regime deduction bands with exact yen figures, the per-basket cap and the overall cap.

(jplib-whole_life-r12)=

### R12 — 生命保険協会, 「２０２５年版 生命保険の動向」 (industry statistics)

- Publisher: 一般社団法人生命保険協会 (Life Insurance Association of Japan)
- Document: `all_2025.pdf`, 33 pp. (FY2024 data)
- Doc type: industry statistics
- URL: https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf
- Accessed: 2026-08-20. Retrieved: YES (downloaded, 33 pp., text extracted; §(1) 個人保険 read
  in full). Source of the whole life share of new business and in force on all four
  measures, and of the industry 解約・失効率 **together with its definition** — an amount-weighted
  ratio to opening in-force sum assured, not a policy-count rate.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the whole life
documents:

- **REG-R1** — 保険業法 第3条, licence classes and the 第一分野 / 第三分野 split. Retrieved: yes.
- **REG-R2** — 保険業法 第4条, 基礎書類 (定款・事業方法書・普通保険約款・算出方法書); why every pricing-basis parameter
  here is **[std]** while 約款 facts are [S#]. Retrieved: yes.
- **REG-R3** — 保険業法 第115条, 価格変動準備金 — an asset-driven reserve, cited and never modelled.
  Retrieved: yes.
- **REG-R4** — 保険業法 第116条, 責任準備金 and the delegation the 標準責任準備金 chain hangs on. Retrieved:
  yes.
- **REG-R5** — 保険業法 第120条, the appointment of the 保険計理人 and the actuarial matters the
  office must be involved in. Retrieved: yes.
- **REG-R6** — 保険業法 第121条, the 保険計理人's 意見書 and the 第1号 confirmation behind the 1号収支分析.
  Retrieved: yes.
- **REG-R7** — 施行規則 第68条, which contracts are standard-reserve contracts, and the
  coefficient-change exclusion. Retrieved: yes.
- **REG-R8** — 施行規則 第69条, the 保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金 taxonomy. Retrieved: yes.
- **REG-R9** — 施行規則 第30条の2, the four surplus-distribution methods; 三利源 is practice, not
  regulatory language. Retrieved: yes.
- **REG-R10** — 平成8年大蔵省告示第48号, 標準責任準備金: 平準純保険料式, table vintages and every 標準利率 reset rule.
  Retrieved: yes, from an unofficial consolidated mirror — see that entry.
- **REG-R11** — 告示48号改正 (2017), adoption of 標準生命表2018 for contracts from 2018-04-01.
  Retrieved: yes.
- **REG-R12** — 告示改正 (2021), extension of 標準責任準備金 to USD/AUD contracts. Retrieved: yes
  (landing page; the 別紙 PDFs were not opened).
- **REG-R14** — 監督指針（本編）: IV-1-9 names 低解約返戻金型 as a product needing extra explanation,
  IV-1-10 requires 解約返戻金 disclosure, and IV-1-12 requires 自動振替貸付 to be at the policyholder's
  election. Retrieved: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: commencement 2026-03-31, the 100% trigger, 現在推計 + MOCE,
  the 99.5% calibration. Retrieved: yes.
- **REG-R16** — ESR 政策ページ, the index to the 柱告示 PDFs; the coefficients themselves are
  [unverified]. Retrieved: yes (index only).
- **REG-R17** — ソルベンシー・マージン比率 and the old 200% threshold. Retrieved: no (the 告示 itself was
  not located; the figures come from REG-R14 and REG-R15).
- **REG-R18** — 標準生命表2018 PDF: the public valuation qx tables, spot rates and terminal ages.
  Retrieved: yes.
- **REG-R20** — 標準生命表2018 作成概要: the 2σ margin, the improvement allowance, the 保険年齢 basis and
  the inclusion of 高度障害 in the death rate. Retrieved: yes.
- **REG-R21** — 日本アクチュアリー会 索引と利用規約: redistribution is restricted, so `jplib` ships a
  **[std]** table citing REG-R18/REG-R19 rather than a copy. Retrieved: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析, its ten-year horizon and its scenario sets.
  Retrieved: yes.
- **REG-R31** — 生命保険の動向 2025: market mix and the 5.6% industry 解約・失効率. Retrieved: yes.
- **REG-R32** — 全国実態調査 2024: household penetration and the premium and sum-assured bands
  that model points should sit inside. Retrieved: yes.
- **REG-R34** — 保険法 第51条, 免責: the statutory suicide exclusion has **no** time limit, so the
  three-year 免責期間 is contractual. Retrieved: yes.
- **REG-R35** — 保険法 第55条, 告知義務違反: the five-year contestability ceiling and the one-month
  discovery clock. Retrieved: yes.
- **REG-R36** — 保険業法 第309条, クーリング・オフ: the eight-day dispatch rule, scoped out here.
  Retrieved: yes.
- **REG-R37** — 保険業法 第300条の2, 特定保険契約: why 外貨建 and 変額 designs get FIEA-grade conduct rules,
  and where the scope boundary of this product sits. Retrieved: yes.
- **REG-R38** — 消費者契約法 第4条: 断定的判断の提供 is why an illustration must split 保証 from 非保証 elements.
  Retrieved: yes.
- **REG-R39** — 金融サービス提供法 第4条: the 説明義務 limb that covers a 低解約返戻金型 suppression period.
  Retrieved: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: 90% of 責任準備金; the 高予定利率契約 detail is [unverified].
  Retrieved: yes (Q1 only).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of the compensation rate. Retrieved:
  yes.
- **REG-R43** — 所得税法 第76条: three ¥40,000 baskets capped at ¥120,000. Retrieved: yes.
- **REG-R44** — 相続税法 第12条: the ¥5,000,000 × statutory heirs death-benefit exemption.
  Retrieved: yes.
- **REG-R45** — タックスアンサー No.4114: the heir-only exemption and the heir count. Retrieved:
  yes.
- **REG-R46** — タックスアンサー No.1755: 一時所得 on a lump sum, 雑所得 on an annuity. Retrieved: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS are
  three separate bases. Retrieved: yes (index page only).

---

## Provenance note

Extraction details — which facts were read from which source, the section-level fact
extraction, the carrier-by-carrier variation table, and the full gaps register (the
unrecoverable 安全率係数 table for annual contracts, the unestablished current 標準利率, the
unestablished current level-premium 予定利率, one carrier's 〔低解約払戻金型〕 special provisions printed
as 「（記載省略）」, the absence of any published lapse curve by duration, and the absence of any
published expense basis) — live in `_research/whole-life.md`.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
