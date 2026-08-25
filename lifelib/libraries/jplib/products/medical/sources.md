# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/medical.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so
the numbering has gaps: R8 (令和6年簡易生命表) is retrieved in the research file but is not cited
by the product documents, because the national life table this product's mortality decrement
is benchmarked against is reached through the cross-product entry [REG-R25] instead. Access
date for all sources: 2026-08-20. No sources were newly added at drafting. Cross-product
[REG-R#] tags are listed in their own section at the end.

Two of the twelve primary documents — [S11] and [S12] — were downloaded successfully but
could **not** be text-extracted (non-embedded CID-keyed fonts); they are retained here
because the product documents cite them as the provenance of facts that are consequently
tagged [unverified], and an entry that records a failed extraction is worth more than a
silently dropped source.

Several product-specific [R#] entries cover the same statute, notification or table as a
cross-product [REG-R#] entry. Where the fact was extracted for this product, the documents
cite the product-specific [R#]; where the load-bearing statement is the cross-product one —
the redistribution restriction on the standard tables, the ESR regime, the market
statistics — they cite the [REG-R#]. Both resolve to a retrieved document.

---

## Primary product sources

(jplib-medical-s1)=

### S1 — オリックス生命保険株式会社, 「契約概要／注意喚起情報」医療保険CURE Next／CURE Lady Next (契約締結前交付書面)
- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: 契約概要／注意喚起情報, 医療保険CURE Next［キュア・ネクスト］および医療保険CURE Lady
  Next［キュア・レディ・ネクスト］, file `importance_cure_next_20250402.pdf` (dated 2025-04-02
  in the filename), 28 pp.
- Doc type: 契約締結前交付書面 (pre-contract disclosure: 契約概要 + 注意喚起情報)
- URL: https://www.orixlife.co.jp/importance/pdf/importance_cure_next_20250402.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded with a browser User-Agent,
  28 pp., text extracted and read; p. 1 and parts of the cover use non-embedded CID fonts
  and extracted as mojibake — all substantive tables on pp. 2–28 extracted cleanly)

(jplib-medical-s2)=

### S2 — オリックス生命保険株式会社, 「無配当 無解約払戻金型医療保険（2022）ご契約のしおり／約款」 (policy booklet and conditions)
- Publisher: オリックス生命保険株式会社
- Document: ご契約のしおり／約款, 無配当 無解約払戻金型医療保険（2022）, file
  `yakkan_cure_next_20240402.pdf` (dated 2024-04-02 in the filename), 244 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.orixlife.co.jp/medical/cure_next/pdf/yakkan_cure_next_20240402.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 244 pp., text extracted; the
  narrative and tabular pages extracted cleanly, the diagram captions and several 別表
  (appendix) pages are image-only and did not extract)

(jplib-medical-s3)=

### S3 — オリックス生命保険株式会社, 「医療保険CURE Next［キュア・ネクスト］」商品ページ (product page)
- Publisher: オリックス生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.orixlife.co.jp/medical/cure_next/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched with a browser User-Agent and converted
  to text; the published 月払保険料 table was read from the raw page text)

(jplib-medical-s4)=

### S4 — アフラック生命保険株式会社, 「ちゃんと応える医療保険EVER ご契約のしおり・約款」 (policy booklet and conditions)
- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: ご契約のしおり・約款,「ちゃんと応える医療保険EVER」(正式名称 医療保険〔無解約払戻金〕),
  file `ever_77836200_77841700.pdf`, 221 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.aflac.co.jp/yakkan/pdf/ever_77836200_77841700.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 221 pp., text extracted and
  read; a few illustration captions are image-only)

(jplib-medical-s5)=

### S5 — アフラック生命保険株式会社, 「医療保険に付加する特約 ご契約のしおり・約款」 (rider booklet)
- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款 for the riders attachable to the medical policy (ケガの特約,
  総合先進医療特約〔2012〕, 入院一時金特約, 通院特約, 女性疾病入院特約, 三大疾病無制限型長期入院特約
  ほか), file `kega_senshin_iryo_77978800.pdf`, 280 pp.
- Doc type: ご契約のしおり・約款 (rider booklet)
- URL: https://www.aflac.co.jp/static/yakkan/koushin/pdf/kega_senshin_iryo_77978800.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 280 pp., text extracted and
  read)

(jplib-medical-s6)=

### S6 — ライフネット生命保険株式会社, 「終身医療保険（無配当・無解約返戻金型）（2019）ご契約のしおり・約款」 (policy conditions)
- Publisher: ライフネット生命保険株式会社 (LIFENET INSURANCE COMPANY)
- Document: ご契約のしおり・約款, 終身医療保険（無配当・無解約返戻金型）（2019）, edition dated
  2026年6月, booklet code LN_BB_GAP-25, 65 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_latest.pdf
  (redirects to https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_20260601.pdf)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 65 pp., text extracted and
  read)

(jplib-medical-s7)=

### S7 — ライフネット生命保険株式会社, 「定期医療保険（無配当・無解約返戻金型）ご契約のしおり・約款」 (policy booklet and conditions)
- Publisher: ライフネット生命保険株式会社
- Document: ご契約のしおり・約款, 定期医療保険（無配当・無解約返戻金型）, edition dated 2024年11月,
  booklet code LN_BB_CXD-170, 65 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_teiki_latest.pdf
  (redirects to
  https://www.lifenet-seimei.co.jp/shared/pdf/LIFENET_yakkan_iryo_teiki_20241125.pdf)
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 65 pp., text extracted and
  read)

(jplib-medical-s8)=

### S8 — ライフネット生命保険株式会社, 「終身医療保険」商品ページ (product page)
- Publisher: ライフネット生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.lifenet-seimei.co.jp/product/medical/whole-life-medical/
- Accessed: 2026-08-20. Retrieved: YES (HTML fetched with a browser User-Agent and converted
  to text; the complete 月額保険料 scale by age and sex, rates as at 2026-06-01, was read from
  the raw page text, not from a summary)

(jplib-medical-s9)=

### S9 — メットライフ生命保険株式会社, 「終身医療保障保険（無解約返戻金型）ご契約のしおり・約款」 (policy booklet and conditions)
- Publisher: メットライフ生命保険株式会社 (MetLife Insurance K.K.)
- Document: ご契約のしおり・約款, 終身医療保障保険（無解約返戻金型）引受基準緩和特則付 (brand
  「マイ フレキシィ」), file `f5wl_20251202.pdf` (2025-12-02 edition), 515 pp.
- Doc type: ご契約のしおり・約款
- URL: https://www.metlife.co.jp/content/dam/metlifecom/jp/corp/pdf/yakkan/provision/f5wl/f5wl_20251202.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 515 pp., text extracted and
  read in the relevant ranges)

(jplib-medical-s10)=

### S10 — アクサ生命保険株式会社, 「医療保険（定期型）約款／重要事項説明書／ご契約のしおり」 (combined booklet)
- Publisher: アクサ生命保険株式会社 (AXA Life Insurance Co., Ltd.; the booklet is branded
  アクサのネット完結保険, formerly アクサダイレクト生命)
- Document: 約款／重要事項説明書／ご契約のしおり, 医療保険（定期型）, Form No. AX-… (the form-number
  digits did not extract), 85 pp.
- Doc type: 重要事項説明書 + ご契約のしおり + 約款 in one booklet
- URL: https://www.axa-direct-life.co.jp/pdf/yakkan_m.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 85 pp., text extracted and
  read; the cover page and one logo block are image/CID and did not extract, including the
  form-number digits and the edition month)

(jplib-medical-s11)=

### S11 — SOMPOひまわり生命保険株式会社, 「健康をサポートする医療保険 健康のお守り」パンフレット (product brochure)
- Publisher: SOMPOひまわり生命保険株式会社
- Document: パンフレット, file `suport_omamori_health.pdf`, 23 pp.
- Doc type: 商品パンフレット
- URL: https://www.himawari-life.co.jp/-/media/himawari/files/product/pamphlet/suport_omamori_health.pdf?la=ja-JP
- Accessed: 2026-08-20. Retrieved: **NO** (HTTP 200, 23-page PDF downloaded successfully,
  but the file uses non-embedded CID-keyed fonts throughout and text extraction returned
  mojibake for essentially every substantive line; the booklet page
  https://www.himawari-life.co.jp/product/suport_omamori_health/booklet/ exposes only this
  one PDF link — the ご契約のしおり・約款 is behind a "Web約款" application, not a static file).
  Every fact attributed to this carrier (a 40日/60日/120日 choice of per-hospitalization limit,
  a 1,000-day aggregate, 手術給付金 at 40/20/10/5倍) rests on a search-result snippet and is
  tagged [unverified] wherever it appears.

(jplib-medical-s12)=

### S12 — 東京海上日動あんしん生命保険株式会社, 「メディカルKit R」重要事項説明書 兼 パンフレット (disclosure and brochure)
- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: 医療総合保険（基本保障・無解約返戻金型）健康還付特則付加［無配当］重要事項説明書 兼
  パンフレット, file `kitr3_pamphlet.pdf`, 14 pp.
- Doc type: 重要事項説明書 兼 パンフレット
- URL: https://www.tmn-anshin.co.jp/bk/kitr3/pdf/kitr3_pamphlet.pdf
- Accessed: 2026-08-20. Retrieved: **NO** (HTTP 200, 14-page PDF downloaded, text extraction
  returned mojibake — non-embedded CID fonts; a second candidate,
  https://www.bk.mufg.jp/sonaeru/hoken/syusin/pdf/tmn_medical_kit.pdf, 12 pp., downloaded and
  failed extraction in the same way). The 健康還付特則 (a premium-refund-at-a-stated-age feature
  on a medical chassis) is therefore recorded as a design that exists in the market but
  whose terms are [unverified].

---

## Regulatory and actuarial references

(jplib-medical-r1)=

### R1 — e-Gov 法令検索, 保険業法 第3条（免許の種類と第三分野の定義）
- Publisher: e-Gov 法令検索 (デジタル庁) — 保険業法, 平成七年法律第百五号
- Doc type: statute (article)
- URL: https://laws.e-gov.go.jp/law/407AC0000000105 (article text retrieved through the
  e-Gov law API endpoint https://laws.e-gov.go.jp/api/1/lawdata/407AC0000000105)
- Accessed: 2026-08-20. Retrieved: YES via the API (the HTML page at
  `laws.e-gov.go.jp/law/…` is JavaScript-rendered and returned only chrome to a plain
  fetcher; the API returned a 3.7 MB UTF-8 XML document from which Article 3 was extracted
  verbatim)

(jplib-medical-r2)=

### R2 — e-Gov 法令検索, 保険業法施行規則 第68条・第69条（標準責任準備金の対象契約／責任準備金の区分）
- Publisher: e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- Doc type: ministerial ordinance (articles)
- URL: https://laws.e-gov.go.jp/law/408M50000040005 (retrieved through
  https://laws.e-gov.go.jp/api/1/lawdata/408M50000040005)
- Accessed: 2026-08-20. Retrieved: YES via the API (30.2 MB XML; Articles 68 and 69
  extracted verbatim, including 第69条第6項第1号の2, the separately identified
  「第三分野保険の保険リスクに備える危険準備金」)

(jplib-medical-r3)=

### R3 — 金融庁, 「保険会社向けの総合的な監督指針」II－2－1－2 / II－2－1－4（責任準備金）
- Publisher: 金融庁 (Financial Services Agency)
- Doc type: supervisory guideline (section view)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES

(jplib-medical-r4)=

### R4 — 日本アクチュアリー会, 「標準生命表2018」（数値表）
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: 標準生命表２０１８, 5 pp. — 生保標準生命表2018（死亡保険用）男／女 and
  第三分野標準生命表2018 男／女
- Doc type: industry standard table (statutory valuation table)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf (index page:
  https://www.actuaries.jp/lib/standard-life-table/index2018.html)
- Accessed: 2026-08-20. Retrieved: YES (5-page PDF downloaded, full numeric tables extracted
  — 年齢, lx, dx, qx, ex for every integral age)

(jplib-medical-r5)=

### R5 — 日本アクチュアリー会, 「標準生命表2018の作成概要」
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要, 6 pp. (資料－①〜⑤)
- Doc type: technical note accompanying the standard table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (6-page PDF downloaded, text extracted and read)

(jplib-medical-r6)=

### R6 — 厚生労働省, 「令和5年（2023）患者調査の概況」
- Publisher: 厚生労働省 (Ministry of Health, Labour and Welfare)
- Document: 令和5年（2023）患者調査の概況, 33 pp.
- Doc type: official statistics summary (基幹統計)
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/kanjya.pdf (index:
  https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/index.html)
- Accessed: 2026-08-20. Retrieved: YES (33-page PDF downloaded, text extracted; the
  statistical tables 4–7 extracted as machine-readable numbers, figures 7 and 8 are charts
  whose data labels extracted but whose axes did not)

(jplib-medical-r7)=

### R7 — e-Stat 政府統計の総合窓口, 「患者調査 令和5年患者調査 全国編」統計表
- Publisher: e-Stat 政府統計の総合窓口 (host) / 厚生労働省 (statistic owner), 政府統計コード 00450022
- Doc type: downloadable statistical tables (CSV / Excel)
- URL: https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450022&tstat=000001224321&cycle=7&tclass1=000001224322&layout=datalist&tclass2val=0
- Accessed: 2026-08-20. Retrieved: YES for the listing page (fetched with a browser
  User-Agent and the full table index read); the individual CSV/Excel files (Z69 入院受療率,
  Z111 and Z114–Z120 the 32-band length-of-stay distributions, Z121–Z123 平均在院日数,
  Z125/Z126 手術の有無別, Z83–Z87 再入院までの期間) were **NOT** downloaded in this session, so
  their column layouts and cell values are not verified here.

(jplib-medical-r9)=

### R9 — 厚生労働省 先進医療会議, 「令和5年6月30日時点で実施されていた先進医療の実績報告について」
- Publisher: 厚生労働省 (先進医療会議 資料 先－2－1 および参考資料1)
- Document: 令和5年度（令和4年7月1日〜令和5年6月30日）実績報告, 13 pp.
- Doc type: regulatory committee statistical report
- URL: https://www.mhlw.go.jp/content/12404000/001178108.pdf
- Accessed: 2026-08-20. Retrieved: YES (13-page PDF downloaded, per-technology tables
  extracted as machine-readable numbers)

(jplib-medical-r10)=

### R10 — 国税庁, タックスアンサー No.1140「生命保険料控除」
- Publisher: 国税庁 (National Tax Agency)
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES

(jplib-medical-r11)=

### R11 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES (the 住民税 caps are not stated on this page and are
  not asserted anywhere in the product documents)

(jplib-medical-r12)=

### R12 — 生命保険文化センター, 「2025（令和7）年度 生活保障に関する調査（速報版）」
- Publisher: 公益財団法人 生命保険文化センター (Japan Institute of Life Insurance)
- Document: プレスリリース, 2025-10-23; survey fieldwork 2025-04-05 to 2025-06-11; n = 4,837
- Doc type: industry survey (press release)
- URL: https://www.jili.or.jp/press/2025/10212.html
- Accessed: 2026-08-20. Retrieved: YES

(jplib-medical-r13)=

### R13 — 厚生労働省, 「医療給付実態調査」（統計ページ）
- Publisher: 厚生労働省 保険局
- Doc type: official statistics landing page (政府統計コード 00450389)
- URL: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/iryouhoken/database/zenpan/iryoukyufu.html
- Accessed: 2026-08-20. Retrieved: YES for the landing page, which is largely a pointer to
  e-Stat; the statistical tables themselves (件数・日数（回数）・点数（金額）by 疾病分類 × 診療種類 ×
  年齢階級) were **NOT** downloaded. A search snippet stating that the survey was discontinued
  after 令和5年度 could not be confirmed on the page and is [unverified].

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the medical
documents:

- **REG-R1** — 保険業法 第3条: the 第一分野／第三分野 licence split, and why the third sector is
  writable under either licence. fetched_ok: yes.
- **REG-R2** — 保険業法 第4条: the 基礎書類, and why every pricing-basis parameter here is [std]
  while contractual parameters carry [S#] tags. fetched_ok: yes.
- **REG-R3** — 保険業法 第115条: 価格変動準備金 is driven by 株式等 and carries no percentage in
  the statute — cited here only to place it outside a liability projection. fetched_ok: yes.
- **REG-R4** — 保険業法 第116条: the delegation the whole 標準責任準備金 (*hyōjun
  sekinin-junbikin*, standard policy reserve) chain hangs on. fetched_ok: yes.
- **REG-R5** — 保険業法 第120条: appointment of the 保険計理人. fetched_ok: yes.
- **REG-R6** — 保険業法 第121条: the 意見書 and the statutory demand behind the 1号収支分析.
  fetched_ok: yes.
- **REG-R7** — 施行規則 第68条: which contracts are standard-reserve contracts. fetched_ok: yes.
- **REG-R8** — 施行規則 第69条: the reserve taxonomy and the 危険準備金 Ⅰ–Ⅳ subdivision, of which
  Ⅳ is the third-sector reserve. fetched_ok: yes.
- **REG-R9** — 施行規則 第30条の2: the four surplus-distribution methods — cited here only to
  record that this chassis is 無配当 and distributes nothing. fetched_ok: yes.
- **REG-R10** — 平成8年大蔵省告示第48号: 平準純保険料式, the table vintages and the 標準利率 reset
  machinery. fetched_ok: yes, but from an unofficial consolidated mirror.
- **REG-R11** — 告示48号改正 (2017): adoption of 第三分野標準生命表2018 from 2018-04-01.
  fetched_ok: yes.
- **REG-R13** — 平成10年6月8日大蔵省告示第231号: the 第三分野 stress test. fetched_ok: **no** — the
  notification's own text was not located, so its stress magnitudes are [unverified] and no
  numeric stress level is asserted in these documents.
- **REG-R14** — 保険会社向けの総合的な監督指針（本編）: II-2-1-2(4)–(7) on third-sector reserving and
  automatic renewal under premium waiver, II-4-2-2 on the 契約締結前交付書面, IV-1-12 on
  自動振替貸付 as an election. fetched_ok: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: ESR commencement 2026-03-31, the 100%
  trigger, 現在推計 + MOCE, the 99.5% calibration. fetched_ok: yes.
- **REG-R17** — ソルベンシー・マージン比率: the superseded 200% threshold and market SMR levels.
  fetched_ok: **no** for the 告示 itself; the figures come from REG-R14 and REG-R15.
- **REG-R18** — 標準生命表2018 PDF: the public valuation qx tables, including
  第三分野標準生命表2018. fetched_ok: yes.
- **REG-R19** — 標準生命表 Excel (1996/2007/2018): the machine-readable form. fetched_ok: yes.
- **REG-R20** — 標準生命表2018 の作成概要: the 2σ margin, the improvement allowance,
  保険年齢方式 (*hoken-nenrei hōshiki*, nearest-birthday basis), and the exclusion of 高度障害
  from the third-sector table. fetched_ok: yes.
- **REG-R21** — 日本アクチュアリー会 索引と利用規約: redistribution of the tables is restricted.
  fetched_ok: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析 — at least ten future years, per segment.
  fetched_ok: yes.
- **REG-R23** — 監督指針 VI: the IAJ as 指定法人 under 法第122条の2. fetched_ok: yes.
- **REG-R26** — 患者調査 受療率: hospitalisation prevalence by age and cause, and the
  prevalence-is-not-incidence trap. fetched_ok: yes.
- **REG-R27** — 患者調査 平均在院日数: stay length by age and cause; why 支払限度日数 binds only in
  the tail. fetched_ok: yes.
- **REG-R28** — 最新がん統計: lifetime cancer incidence, cited for why the 三大疾病 limit
  relaxations are mass-market features. fetched_ok: yes.
- **REG-R31** — 生命保険の動向 2025年版: the market mix by policy count, 入院給付金 and 手術給付金
  paid, third-sector annualised premium, and the 5.6% industry lapse rate. fetched_ok: yes.
- **REG-R32** — 生命保険に関する全国実態調査 2024年度: household penetration of 医療保険・医療特約.
  fetched_ok: yes.
- **REG-R33** — e-Stat: the access route to the machine-readable 患者調査 grids; licence terms
  unread. fetched_ok: yes (home page only).
- **REG-R34** — 保険法 第51条: the statutory suicide exclusion has no time limit, so a 免責期間
  is a contractual fact per carrier. fetched_ok: yes.
- **REG-R35** — 保険法 第55条: the five-year contestability ceiling and the one-month discovery
  clock. fetched_ok: yes.
- **REG-R36** — 保険業法 第309条: the eight-day dispatch-rule クーリング・オフ, scoped out here
  explicitly. fetched_ok: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: 90%-of-reserve compensation. fetched_ok: yes (Q1
  only; the 高予定利率契約 page was not opened).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of the compensation rate.
  fetched_ok: yes.
- **REG-R43** — 所得税法 第76条: three ¥40,000 baskets capped at ¥120,000, of which
  介護医療保険料 is this product's. fetched_ok: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS
  are three separate bases. fetched_ok: yes.

---

## Provenance note

Extraction details — which facts were read from which document, the per-source fact
extraction sections, the carrier-by-carrier variation table, and the full gaps register
(the two unreadable brochures, the unretrieved 大蔵省告示第231号, the absence of any published
標準利率 (*hyōjun riritsu*, standard valuation interest rate) or 予定利率 (*yotei riritsu*,
assumed interest rate) for this class, the undownloaded e-Stat CSVs, the unverified 住民税 caps,
and the missing 令和6年度 先進医療実績報告) — live in `_research/medical.md`.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R25]: #jplib-reg-r25
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
