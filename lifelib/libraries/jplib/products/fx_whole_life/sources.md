# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/fx-whole-life.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering carries gaps wherever the drafting pass drops one; on this product
it drops none. Every id the research pass created is cited by `product-spec.md` or
`technical-notes.md`, including the two whose documents could **not** be retrieved — [S15]
and [S16] — each of which is cited only for the negative fact it establishes, never for a
product term. Access date for all sources: 2026-08-20. No sources were newly added at
drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

Eight carriers are represented in the retrieved primary set; a ninth appears only as a fetch
failure [S15], and one securities distributor supplies the single retrieved document that
quantifies distributor commission [S13]. Company and branded product names appear in this
file and in `_research/fx-whole-life.md` and **nowhere else** in the library: in
`product-spec.md`, `technical-notes.md`, `model.md` and the model docstrings a carrier is
referred to by its [S#] tag alone.

---

## Primary product sources

(jplib-fx_whole_life-s1)=

### S1 — メットライフ生命保険, "USドル建終身保険 ドルスマート S 商品パンフレット" (product summary leaflet)

- Publisher: メットライフ生命保険株式会社 (MetLife Insurance K.K.)
- Document: 商品パンフレット for the product whose 正式名称 is
  「積立利率変動型終身保険（米国通貨建 2002）」, document code 補2412-0019 /
  A605-13（11）（25.04）OT-PDF, Ver.11, 2 pp.; 「この資料に記載の保障内容などは2025年4月現在のものです」
- Doc type: product summary leaflet (商品概要 / 契約締結前交付書面の補助資料)
- URL: https://spon.metlife.co.jp/document/products_sp/iswl-dollar.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded with a browser User-Agent, 2 pp.,
  text extracted and read in full)
- Supplies: the level-premium 積立利率変動型 shape — 契約年齢 満6歳〜満80歳, 最低保険金額 3万米ドル,
  最低保証積立利率 年3.00％, the monthly rate declaration, the 増加死亡保険金額 uplift, the 特別積立金
  top-ups at 10 and 20 years, the three-layer charge stack, and 為替手数料 TTM＋50銭 / TTM−50銭.

(jplib-fx_whole_life-s2)=

### S2 — メットライフ生命保険, "ドルスマート S 重要事項説明書・ご契約のしおり・約款" (policy conditions and handbook)

- Publisher: メットライフ生命保険株式会社
- Document: combined booklet for 契約日が2026年5月1日以降, file `iswldollar_20260501.pdf`, 275 pp.;
  the 注意喚起情報 section states 「記載の内容は2025年12月現在のものです」
- Doc type: 普通保険約款 (*futsū hoken yakkan*, policy conditions) + ご契約のしおり (policy handbook) +
  重要事項説明書 (IDD-style disclosure)
- URL: https://www.metlife.co.jp/content/dam/metlifecom/jp/corp/pdf/yakkan/provision/iswldollar/iswldollar_20260501.pdf
  (index page listing this and the superseded versions:
  https://www.metlife.co.jp/yakkan/provision/iswldollar/)
- Accessed: 2026-08-20. Retrieved: YES (5.2 MB PDF downloaded with a browser User-Agent,
  275 pp., text extracted; 商品概要, 諸費用, 解約返戻金, 積立利率, 増加死亡保険金額, 失効・復活, 免責 and
  普通保険約款第3条 / 第27条 / 第46条 plus the 低解約返戻金特則 clauses read)
- Supplies: **the anchor model cell and its published surrender-value run** — two complete
  解約返戻金額例表, with and without the 低解約返戻金特則, at 3.00％ / 3.50％ / 4.00％ crediting; the
  約款第3条 crediting mechanic and its floor; the 低解約返戻金割合 scale 70／77.5／85／92.5％; 自殺免責3年;
  復活1年; 自動振替貸付; 契約者貸付; 前納.

(jplib-fx_whole_life-s3)=

### S3 — ジブラルタ生命保険, "積立利率更改型一時払終身保険（23）ご契約のしおり・約款" (policy conditions and handbook)

- Publisher: ジブラルタ生命保険株式会社 (Gibraltar Life Insurance Co., Ltd.)
- Document: 2023年10月版 ご契約のしおり／約款, 172 pp., covering the 基本タイプ and the 積立金定期引出タイプ
  in 米国ドル建 and 豪ドル建, plus 保険料円入金特約, 円支払特約 and 年金支払移行特約
- Doc type: policy conditions + policy handbook
- URL: https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/L411_ichijibarai_syusin_202310.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.4 MB PDF, 172 pp.; the served text layer was
  unusable, so the file was re-extracted locally with PyMuPDF and the 特徴としくみ, 積立利率,
  積立利率適用期間・指標金利, 解約と解約返戻金, 市場価格調整率, 解約控除率, 適用する為替レート and 免責 sections read)
- Supplies: **the two published run-off tables the composite is built on** — the full
  市場価格調整率 (*shijō kakaku chōsei ritsu*, market value adjustment rate) grid by elapsed year ×
  interest-rate move for a 15-year 積立利率適用期間, and the full 解約控除率 (*kaiyaku kōjo ritsu*,
  surrender charge rate) scale 7.0％→0.7％ over ten years; also the crediting-rate formula and
  its ±1.5％ band, cap and 0.01％ floor, the named 指標金利, death benefit = max(積立金相当額,
  解約返戻金額), 為替レート 米国ドル TTM＋50銭 / TTM−1銭, and 自殺免責2年.

(jplib-fx_whole_life-s4)=

### S4 — ジブラルタ生命保険, "積立利率更改型一時払終身保険（23）積立利率" (rate disclosure page)

- Publisher: ジブラルタ生命保険株式会社
- Doc type: rate disclosure page (最新の積立利率・過去の積立利率・最新の基準利率・過去の基準利率)
- URL: https://www.gib-life.co.jp/st/intro/products/kyotsu/rate/tatsuka_syushin_23/fxrate/
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent; server-rendered
  HTML, the current and the 2026 historical rate tables read)
- Supplies: 契約年齢 0歳〜90歳 with the 0–79 / 80–90 split of the USD 積立利率適用期間; the declared
  積立利率 and the 実質的な利回り for the 2026-08-16 to 2026-08-31 window and the fortnightly history
  back through 2026; the fact that the rate is declared **twice a month** for new business.

(jplib-fx_whole_life-s5)=

### S5 — 明治安田生命保険, "つみたてドル建終身 商品ページ" (product page)

- Publisher: 明治安田生命保険相互会社
- Document: product page for 「5年ごと配当付利率変動型積立終身保険（低解約返戻金型・指定通貨建）」, including its
  為替リスク, 諸費用, 低解約返戻金期間 and 予定利率 sections
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find/list/dolshushin/
- Accessed: 2026-08-20. Retrieved: YES (server-rendered HTML, 87 KB, fetched with a browser
  User-Agent and read in full)
- Supplies: the third market shape — a level **yen** premium converted to USD each month;
  第1保険期間 / 第2保険期間 with a five-yearly 予定利率 reset and a 0.25％ floor; the surrender-charge
  factor 1−20％×(1−経過月数÷120) applied after a 70％ low-surrender factor; 為替手数料 TTM＋25銭 /
  TTM−25銭; an explicit statement that the product has **no** 市場価格調整; and its 特定保険契約 status.

(jplib-fx_whole_life-s6)=

### S6 — 明治安田生命保険, "外貨建保険に適用される予定利率" (rate disclosure page)

- Publisher: 明治安田生命保険相互会社
- Doc type: rate disclosure page
- URL: https://www.meijiyasuda.co.jp/norapl/find/rate/dolcommon/planned_interest_rate/
- Accessed: 2026-08-20. Retrieved: YES (server-rendered HTML, read in full)
- Supplies: 第1保険期間 予定利率 3.50％ for 契約日 2026年9月1日, declared 毎月1日; the 第2保険期間 index
  (the average of the 6-month and 5-year US Treasury yields), its five-yearly reset, its
  0.25％ floor and its last reset between ages 101 and 105; sibling products' rates declared
  twice monthly.

(jplib-fx_whole_life-s7)=

### S7 — オリックス生命保険, "無配当 米国ドル建終身保険（低解約払戻金型）ご契約のしおり・約款" (policy conditions and handbook)

- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: ご契約のしおり／約款 2023年11月, 148 pp., covering the main contract and the
  米国ドル建特定疾病障害介護終身保険特約（低解約払戻金型）
- Doc type: policy conditions + policy handbook
- URL: https://www.orixlife.co.jp/customer/webclause/pdf/webyakkan_bright_20231102.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.9 MB PDF, 148 pp., extracted with PyMuPDF; the
  諸費用, 円入金特約, 円支払特約, 解約と解約払戻金, 猶予期間と失効, 復活 and 免責 sections read)
- Supplies: the **fixed-予定利率 (定額)** USD whole life, included for contrast — no 積立利率, no
  MVA, a flat 7割 low-surrender factor, 解約控除 over the shorter of the premium-paying period
  and ten years deducted from the 責任準備金, a mandatory 円入金特約 and optional 円支払特約 at
  当社所定の為替レート, the 猶予期間 rules, 復活 within 3 years, 自殺免責3年 and 告知義務違反 2年.

(jplib-fx_whole_life-s8)=

### S8 — 三井住友海上プライマリー生命保険, "外貨建定額終身保険（円建終身移行特約付）商品説明資料" (product explanation sheet)

- Publisher: 三井住友海上プライマリー生命保険株式会社
- Document: ご契約者さま用商品説明資料, 4 pp., document code MSPL-2204-B-0278-00; the product was
  sold 2012–2022 and is closed to new business
- Doc type: product explanation sheet (existing policyholders)
- URL: https://www.ms-primary.com/products/product_stop/pdf/products_stop_FLtumitate.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 4 pp., text extracted and read in
  full)
- Supplies: the **target-value mechanic** at its widest published granularity — 目標値
  105％〜200％ in 1％ steps against the yen-converted single premium, automatic conversion to a
  yen whole life on 目標達成 and conversion on demand; 契約年齢 0歳〜87歳; 米ドル・豪ドル・ユーロ; a 10-year
  積立利率適用期間 (3 years from age 81); **two vintages** of the 解約控除率 scale (10％→0％ and 5％→0％) and
  no 解約控除 after conversion; 円支払特約 at TTM−50銭; death benefit = max(保障基準価格, 解約払戻金額).

(jplib-fx_whole_life-s9)=

### S9 — Ｔ＆Ｄフィナンシャル生命保険, "生涯プレミアムワールド4 — 目標値到達時終身保険移行特約について" (product page)

- Publisher: Ｔ＆Ｄフィナンシャル生命保険株式会社
- Document: product website section for 「無配当外国為替連動型終身保険（積立利率更改・通貨選択Ⅳ型）」
  定期支払コース, document code 316-19-C032; the product is closed to new business
- Doc type: product page (consumer)
- URL: https://www.tdf-life.co.jp/pre_world4/pre_world4_shushinikou2.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML, read in full)
- Supplies: the **operative detail of the target test** — 目標値 100％／105％／110％ chosen at issue
  and changeable any number of times before the hit, tested every business day from one year
  after 契約日, the test made on the 解約払戻金額 so that FX and MVA enter it, automatic conversion
  to a yen whole life on a hit, and the fixing of the death benefit and surrender value in
  yen thereafter.

(jplib-fx_whole_life-s10)=

### S10 — Ｔ＆Ｄフィナンシャル生命保険, "生涯プレミアムワールド4 — 諸費用について" (charge disclosure page)

- Publisher: Ｔ＆Ｄフィナンシャル生命保険株式会社
- Doc type: product page (consumer), charge disclosure
- URL: https://www.tdf-life.co.jp/pre_world4/pre_world4_gokeiyaku02.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, read in full)
- Supplies: **the only published 契約初期費用 scale in the set** — a flat percentage of the single
  premium banded by issue age, 40–69歳 4.50％, 70–79歳 3.00％, 80–84歳 2.00％, 85–90歳 2.00％ —
  together with the statement that there is no separate in-force charge because the 維持,
  死亡保険金 and 累積追加額 costs are netted out inside the 積立利率, and an annuity management charge
  of up to 1.0％ of each payment.

(jplib-fx_whole_life-s11)=

### S11 — Ｔ＆Ｄフィナンシャル生命保険, "生涯プレミアムワールド4 — 積立コース／為替レートについて" (product pages)

- Publisher: Ｔ＆Ｄフィナンシャル生命保険株式会社
- Doc type: product pages (consumer)
- URLs: https://www.tdf-life.co.jp/pre_world4/tsumitate.html and
  https://www.tdf-life.co.jp/pre_world4/rate/exchange_rate.html
- Accessed: 2026-08-20. Retrieved: YES (both fetched with a browser User-Agent and read in
  full)
- Supplies: the 外国為替連動型 shape, in which premium and benefit are both in yen and FX enters
  only as a 為替変動率 multiplier, with **no 為替手数料 charged at all**; the reference TTM published
  each business day around 11:00 and the observed 2026-08-19 values US$1 = ¥159.43 and
  A$1 = ¥112.83; and the 介護年金支払移行特約.

(jplib-fx_whole_life-s12)=

### S12 — 第一フロンティア生命保険, "積立利率変動型終身保険（20）（通貨指定型）市場価格調整用利率" (rate disclosure page)

- Publisher: 第一フロンティア生命保険株式会社
- Doc type: rate disclosure page (解約(減額)時に適用される市場価格調整用利率)
- URL: https://www.d-frontier-life.co.jp/products/index_hendo_shushin_choice_20_b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML, read in full)
- Supplies: a 通貨指定型 chassis carrying 米ドル / 豪ドル / 円 with 積立利率保証期間 of 30y and 10y (USD),
  20y and 10y (AUD), 30y and 15y (JPY); the published 市場価格調整用利率 for 2026-08-16 to
  2026-08-31 (死亡保障型 USD 5.50％ / 4.95％, AUD 5.15％ / 5.06％, JPY 3.67％ / 2.78％); and the
  statement that the same rate both sets the 積立利率 and computes the MVA.

(jplib-fx_whole_life-s13)=

### S13 — ＳＭＢＣ日興証券, "重要情報シート ダブル・フロンティア終身（円建／米ドル建／豪ドル建）" (distributor key information sheet)

- Publisher: ＳＭＢＣ日興証券株式会社 (distributor) for 第一フロンティア生命保険株式会社 (組成会社)
- Document: 重要情報シート, 2024年1月版, 4 pp., registration code (登)B22F0412（2023.2.2）, for
  「積立利率変動型定額部分付変額終身保険（15）／（通貨指定型）」
- Doc type: distributor key information sheet (金融庁 重要情報シート format)
- URL: https://www.smbcnikko.co.jp/products/insurance/pdf/jyuyojoho/d_frontier_shushin.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 4 pp., text extracted and read in
  full)
- Supplies: 解約控除 published as a range by 第1保険期間 and elapsed year — 外貨建 6.5％〜0.0％, 円建
  3.5％〜0.1％, applied to the **基本保険金額**; 保険契約関係費 2.35％ p.a. on the 変額部分 plus 信託報酬
  0.22％; the distributor commission structure (契約時手数料 4.00％ or 2.60％ of the single premium
  for the FX versions, 継続手数料 up to 0.75％ p.a. of the account value, payable for at most
  seven years); the FX return distribution printed in the sheet; and the tax treatment.

(jplib-fx_whole_life-s14)=

### S14 — プルデンシャル生命保険, "外貨建一時払保険の基準利率" (rate disclosure page)

- Publisher: プルデンシャル生命保険株式会社
- Document: rate disclosure page for 「米国ドル建利率変動型一時払終身保険（無告知型）」
- Doc type: rate disclosure page
- URL: https://www.prudential.co.jp/contractor/rate_simulation/standard/
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent; the page is
  Shift-JIS server-rendered HTML, decoded and read)
- Supplies: **the longest public rate series found** — a fortnightly 基準利率 history for
  10-year and 15-year 積立利率保証期間 running from 4.45％ / 4.60％ (2025-11-01 window) to 5.15％ /
  5.29％ (2026-08-16 window), twenty consecutive windows, with the longer guarantee period
  consistently carrying the higher rate.

(jplib-fx_whole_life-s15)=

### S15 — マニュライフ生命保険, "こだわり外貨終身 商品ページ・積立利率履歴・通貨選択型一時払終身保険 約款"

- Publisher: マニュライフ生命保険株式会社
- Doc type: product page, published crediting-rate history, policy conditions
- URLs: https://www.manulife.co.jp/ja/individual/products/goods/kodawari-gaikasyushin.html ;
  https://www.manulife.co.jp/ja/individual/rates/kodawari-gaikasyushin/int-past.html ;
  https://www.manulife.co.jp/ja/individual/rates.html ;
  https://www.manulife.co.jp/content/dam/insurance/jp/images/individual/policyholder/web-yakkan/miraisyushin/21120855-387466.pdf
- Accessed: 2026-08-20. **Retrieved: NO** (every URL returned HTTP 403 to both WebFetch and
  curl, with and without a browser User-Agent, with a Referer and a cookie jar, and over
  forced HTTP/1.1; the block is a WAF policy, not a User-Agent check)
- Supplies: **nothing but the gap.** No product term in this library is sourced to it. It is
  cited once, in `product-spec.md`, for the single fact it establishes: the carrier whose
  documents would have carried the rider name 目標到達時円建終身保険移行特約 verbatim cannot be
  retrieved, which is why that name is [unverified] and the two verified rider names of [S8]
  and [S9] are quoted instead.

(jplib-fx_whole_life-s16)=

### S16 — メットライフ生命保険, 積立利率公表ページ (rate disclosure page)

- Publisher: メットライフ生命保険株式会社
- Doc type: rate disclosure page — the page [S2] names as the place the declared 積立利率 is
  published
- URL: https://www.metlife.co.jp/lf1/ahp405/08.html
- Accessed: 2026-08-20. **Retrieved: NO** (HTTP 200, but the response is a React single-page
  application shell — a root `div` plus a JavaScript bundle — with no rate content in the
  served HTML)
- Supplies: the boundary on the crediting scenario. Because the declared-rate history for
  the composite's level-premium shape is not machine-fetchable, the only crediting figures
  available for it are the guaranteed floor and the three illustration rates in [S1] [S2],
  which is why the base run uses the floor and the higher rates are scenarios.

---

## Regulatory and actuarial references

(jplib-fx_whole_life-r1)=

### R1 — 金融庁, 標準責任準備金制度にかかる告示の一部改正に対するパブリックコメントの結果等について

- Publisher: 金融庁 (Financial Services Agency)
- Document: 2021-06-30 publication; 別紙２「平成8年大蔵省告示第48号及び平成13年金融庁告示第24号の一部を改正する件
  （新旧対照表）」, 21 pp. (vertical Japanese text)
- Doc type: FSA notification amendment + public-comment response
- URLs: https://www.fsa.go.jp/news/r2/hoken/20210630/20210630.html (index) and
  https://www.fsa.go.jp/news/r2/hoken/20210630/02.pdf (新旧対照表)
- Accessed: 2026-08-20. Retrieved: YES (index page fetched; the 新旧対照表 PDF downloaded and
  extracted with PyMuPDF, the vertical single-character lines re-joined before reading)
- Supplies: the amendment that brought 米国通貨建 and 豪州通貨建保険契約 into the 標準責任準備金 regime,
  effective 2021-10-01 (2022-04-01 for the 平成13年金融庁告示第24号 changes); the 基準利率 derivation
  from A-rated same-currency corporate yields at 10 and 20 years; the 安全率係数 bands for USD
  and AUD; the monthly 基準日 with its 0.05％ trigger and rounding; and the exclusion of every
  other foreign currency from the 対象契約.

(jplib-fx_whole_life-r2)=

### R2 — 金融庁, 保険会社向けの総合的な監督指針の一部改正（新旧対照表）

- Publisher: 金融庁
- Document: 2021-06-30, 別紙３, 3 pp.
- Doc type: supervisory guideline amendment
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/03.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 3 pp., text extracted and read in
  full)
- Supplies: the extension of the 代替的方式 conditions to non-yen contracts
  「その特性に応じ…に準じた条件」, the unchanged 10％ tolerance against the 標準的方式, and the redefinition
  of 標準利率 by reference to 責任準備金告示 rather than to its 第4項.

(jplib-fx_whole_life-r3)=

### R3 — 金融庁, 保険会社向けの総合的な監督指針 Ⅱ－4 業務の適切性

- Publisher: 金融庁
- Doc type: supervisory guideline (current text)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02d.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML; the 契約締結前交付書面, 外貨建て保険, MVA and 外貨建て保険に係る募集上の留意事項 sections read)
- Supplies: the product-specific 契約概要 items for 外貨建て保険 and for MVA products — including the
  requirement to illustrate 「解約時の保険料積立金に対して控除される割合」, which is why an MVA is disclosed
  as a rate table and not as a formula — the definition of MVA, and the requirement to
  take a signed acknowledgement of FX risk from a non-corporate policyholder.

(jplib-fx_whole_life-r4)=

### R4 — 金融庁, 保険会社向けの総合的な監督指針 Ⅱ－2 財務の健全性

- Publisher: 金融庁
- Doc type: supervisory guideline (current text)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML; the 価格変動準備金 / 危険準備金 provision on 外貨建て保険 read)
- Supplies: the requirement that the 価格変動準備金 inside the 責任準備金 of 外貨建て保険 be scoped from the
  asset classes matching the 外貨建て保険 segment on a segregated-accounting basis, and that the
  危険準備金Ⅱ for those contracts use the 外貨建て保険 risk coefficient.

(jplib-fx_whole_life-r5)=

### R5 — 金融庁, リスク性金融商品の販売会社等による顧客本位の業務運営に関するモニタリング結果（2023事務年度中間報告）

- Publisher: 金融庁
- Document: 2024（令和6）年4月3日, 6 pp.
- Doc type: supervisory monitoring report
- URL: https://www.fsa.go.jp/news/r5/kokyakuhoni/202403/01.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 6 pp., text extracted and read in
  full)
- Supplies: about **60％ of 外貨建一時払保険 surrendered within four years of purchase**,
  concentrated in ターゲット型 policies; the 2023-08-31 run-off cohort of 549,781 policies against
  the 89,452 held five years or more; the return decomposition in which 市場価格調整と解約控除費 push
  the margin down; the target-hit-and-rebuy pattern and the double-charged commission; and
  the L-shaped distributor commission, 5.5％ in year 1 against 0.1％ thereafter.

(jplib-fx_whole_life-r6)=

### R6 — 金融庁, リスク性金融商品の販売・組成会社による顧客本位の業務運営に関するモニタリング結果（概要版）

- Publisher: 金融庁
- Document: 2024（令和6）年7月5日, 9 pp.
- Doc type: supervisory monitoring report (summary)
- URL: https://www.fsa.go.jp/news/r6/kokyakuhoni/fdreport/01.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 9 pp., text extracted and read in
  full)
- Supplies: the FSA's own definition of ターゲット型保険 and its 目標値 granularity, and the
  **average holding period of 2.5 years**.

(jplib-fx_whole_life-r7)=

### R7 — 生命保険協会, 「外貨建保険販売資格試験」の創設について

- Publisher: 一般社団法人 生命保険協会 (The Life Insurance Association of Japan, LIAJ)
- Document: news release attachment, 2020-02-21, 3 pp.
- Doc type: industry association news release
- URLs: https://www.seiho.or.jp/info/news/2020/20200221.html (index; the body is JS-rendered
  and the release content lives in the linked PDF) and
  https://www.seiho.or.jp/info/news/2019/pdf/20200221.pdf (the release itself)
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 3 pp., text extracted and read in
  full)
- Supplies: the bank-channel 外貨建保険 complaint series 2012–2019 H1 and its composition (68％
  説明不十分), and the creation of the 外貨建保険販売資格試験 with its examination date and its
  販売資格者登録制 from around April 2022.

(jplib-fx_whole_life-r8)=

### R8 — 生命保険協会, 生命保険商品に関する適正表示ガイドライン

- Publisher: 一般社団法人 生命保険協会
- Document: 令和8年1月29日 edition, 36 pp.; 制定 平成15年10月15日, amended repeatedly
- Doc type: industry association guideline
- URL: https://www.seiho.or.jp/activity/guideline/pdf/tekiseihyouji.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 36 pp., text extracted; the 特定保険契約,
  外貨建て保険 and MVA sections read)
- Supplies: the definition of 実質的な利回り for 外貨建 一時払 whole life and the requirement to display
  it **at the point where the MVA, the rate-variation period and the surrender charge have
  all expired**; the standard risk wording for 外貨建て保険 and MVA products; and the requirement
  that any illustration of a market move also print the no-move case.

(jplib-fx_whole_life-r9)=

### R9 — 金融庁, 外貨建保険について（生命保険協会との意見交換会 論点メモ）

- Publisher: 金融庁
- Document: 2019年2月 論点資料, 6 pp. (item 1 of a multi-topic memo)
- Doc type: FSA discussion memo
- URL: https://www.fsa.go.jp/common/ronten/201902/07.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 6 pp., text extracted and read)
- Supplies: the FSA's framing of the product as one that pushes FX risk onto the customer,
  and its demand that the sales material be comparable with an investment trust's 目論見書.

(jplib-fx_whole_life-r10)=

### R10 — 生命保険契約者保護機構, 保険契約者保護制度Q&A Q1

- Publisher: 生命保険契約者保護機構 (Life Insurance Policyholders Protection Corporation of Japan)
- Doc type: statutory scheme Q&A
- URL: https://www.seihohogo.jp/qa/qa1.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML, read in full)
- Supplies: cover of 補償対象契約 to 90％ of the 責任準備金等 at the failure date, with **no carve-out
  for 外貨建 contracts** — the same rule insurers reproduce in their own 外貨建 booklets.

(jplib-fx_whole_life-r11)=

### R11 — 国税庁, タックスアンサー No.1903「給与所得者に生命保険の満期返戻金などの一時所得があった場合」

- Publisher: 国税庁 (National Tax Agency)
- Document: [令和7年4月1日現在法令等]
- Doc type: tax authority guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1903.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML, read in full)
- Supplies: the 一時所得 computation on a lump-sum surrender or maturity payment and the
  half-inclusion rule, with the filing threshold for an employee. It does **not** address
  為替差益 on a foreign-currency policy separately, which is why the treatment of the FX gain is
  [unverified] in this library.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the
`fx_whole_life` documents:

- **REG-R1** — 保険業法 第3条: the 第一分野 licence class this product sits in. Retrieved: yes.
- **REG-R2** — 保険業法 第4条, 基礎書類: why the 予定利率, the charge rates and the surrender-value
  formula are [std] while 約款 facts are [S#]. Retrieved: yes.
- **REG-R3** — 保険業法 第115条, 価格変動準備金: asset-driven, cited never modelled; 施行規則第66条第2項 is
  the FX segment carve-out that [R4] operates. Retrieved: yes.
- **REG-R4** — 保険業法 第116条: the delegation the 標準責任準備金 chain hangs on. Retrieved: yes.
- **REG-R5** — 保険業法 第120条, 保険計理人の選任: the governance frame for the basis. Retrieved: yes.
- **REG-R6** — 保険業法 第121条, 意見書: the statutory demand behind the 1号収支分析. Retrieved: yes.
- **REG-R7** — 施行規則 第68条: which contracts are standard-reserve, and the coefficient-change
  escape hatch that decides whether an 積立利率変動 contract stays in scope. Retrieved: yes.
- **REG-R8** — 施行規則 第69条: the 保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金 taxonomy. Retrieved: yes.
- **REG-R10** — 告示第48号: 平準純保険料式, the table vintages and every 標準利率 reset rule, including
  the foreign-currency bands. Retrieved: yes.
- **REG-R12** — 告示改正 (2021): the extension of 標準責任準備金 to USD and AUD contracts from 2021-10
  and 2022-04 — the provenance of this product's reserving pointer. Retrieved: yes (landing
  page; the 別紙 PDFs are [R1] here).
- **REG-R14** — 監督指針（本編）: IV-1-9 names MVA products and 低解約返戻金型 products as needing extra
  explanation, IV-1-10 requires 解約返戻金 disclosure, IV-1-12 requires 自動振替貸付 to be at the
  policyholder's election. Retrieved: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: commencement 2026-03-31, the 100％ trigger,
  現在推計 + MOCE, the 99.5％ calibration, and 為替 as a named market-risk category.
  Retrieved: yes.
- **REG-R16** — ESR 政策ページ: the index to the 柱告示; the coefficients are [unverified].
  Retrieved: yes (index only).
- **REG-R17** — ソルベンシー・マージン比率 and the old 200％ threshold. Retrieved: no (the 告示 itself was
  not located).
- **REG-R18** — 標準生命表2018 PDF: the public valuation qx tables and terminal ages that the
  [std] mortality charge basis is anchored to. Retrieved: yes.
- **REG-R20** — 標準生命表2018 作成概要: the 2σ margin, the improvement allowance, the 保険年齢 basis
  and the inclusion of 高度障害 in the death rate. Retrieved: yes.
- **REG-R21** — 日本アクチュアリー会 利用規約: redistribution is restricted, so `jplib` ships a **[std]**
  table citing REG-R18 rather than a copy. Retrieved: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析, its ten-year horizon, and its explicit treatment of
  MVA and foreign-currency business. Retrieved: yes.
- **REG-R31** — 生命保険の動向 2025: the 5.6％ industry 解約・失効率 against which this product's
  four-year surrender rate is read. Retrieved: yes.
- **REG-R34** — 保険法 第51条, 免責: the statutory suicide exclusion has no time limit, so the
  two- and three-year 免責期間 observed here are contractual. Retrieved: yes.
- **REG-R35** — 保険法 第55条, 告知義務違反: the five-year contestability ceiling. Retrieved: yes.
- **REG-R36** — 保険業法 第309条, クーリング・オフ: the eight-day dispatch rule, scoped out here.
  Retrieved: yes.
- **REG-R37** — 保険業法 第300条の2, 特定保険契約: the statutory reason this product carries FIEA-grade
  conduct rules, and the reason a loss against premiums paid is a definitional
  feature rather than a defect. Retrieved: yes.
- **REG-R38** — 消費者契約法 第4条: 断定的判断の提供 is why an illustration must split 保証 from 非保証
  elements — here, the guaranteed 3.00％ column from the 3.50％ and 4.00％ ones.
  Retrieved: yes.
- **REG-R39** — 金融サービス提供法 第4条: the 説明義務 limb that covers 解約控除, MVA and a 低解約返戻金型
  suppression period — all three of this product's surrender-layer mechanics.
  Retrieved: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: 90％ of 責任準備金; the 高予定利率契約 detail is [unverified].
  Retrieved: yes (Q1 only).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of the compensation rate. Retrieved:
  yes.
- **REG-R43** — 所得税法 第76条: the three ¥40,000 baskets capped at ¥120,000. Retrieved: yes.
- **REG-R44** — 相続税法 第12条: the ¥5,000,000 × statutory heirs exemption. Retrieved: yes.
- **REG-R45** — タックスアンサー No.4114: the heir-only exemption and the heir count.
  Retrieved: yes.
- **REG-R46** — タックスアンサー No.1755: 一時所得 on a lump sum, 雑所得 on an annuity. Retrieved: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS are
  three separate bases over one set of projected cash flows. Retrieved: yes (index
  page only).

---

## Provenance note

Extraction details — which facts were read from which source, the section-level fact
extraction, the carrier-by-carrier variation table, and the full gaps register (the two
unreachable sites, the unpublished minimum single premium, the unquantified
mortality-and-expense charge, the absence of any closed-form MVA, the 増加死亡保険金額 ratchet
that appears in the ご契約のしおり but not in the extracted 約款 text, the 計算日 discrepancy between
the 重要事項説明書 and the 約款, the unverified rider name, the unverified FX-gain tax treatment,
the unestablished current 標準利率 for USD contracts, and the absence of any published
new-business volume for 外貨建終身保険) — live in `_research/fx-whole-life.md`. That file is the
citation ground truth for the S# and R# numbering used here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-fx_whole_life-r1
[R4]: #jplib-fx_whole_life-r4
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
