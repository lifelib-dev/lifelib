# 外貨建終身保険 (foreign-currency whole life, 積立利率変動型) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese foreign-currency-denominated whole life liability cash flow
reference model (`fx_whole_life` / `FXWholeLife_JP_S`) — the account-value chassis of
`whole_life` extended with a declared crediting rate (積立利率), a market value adjustment
(市場価格調整), a surrender charge (解約控除), a currency-conversion layer
(円入金特約 / 円支払特約 and its 為替手数料), and the target-value conversion rider
(目標到達時円建終身保険移行特約 and its variants).

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually retrieved and read during
this
session, or is tagged [unverified] where it is general knowledge not confirmed against a
retrieved document. Access date for all fetched sources: 2026-08-20.

Note on scope. Japanese carriers sell three structurally different things under the
外貨建終身保険 label, and the difference matters to the model:

- **積立利率変動型 (level premium)** — the crediting rate is redeclared *monthly* and applied to
  an account value; there is no MVA. [S1] [S2]
- **積立利率更改型 / 利率変動型 (single premium)** — the crediting rate is fixed for a multi-year
  積立利率適用期間 (1/3/10/15/20/30 years) and reset at each 積立利率計算基準日; surrender
  inside the period carries an MVA. [S3] [S4] [S8] [S9] [S12]
- **指定通貨建 with yen-fixed premiums** — the premium is a level *yen* amount converted to USD
  each month, and the 予定利率 is reset every five years after 払込満了. [S5] [S6]

All three are in scope for the representative product; the drafting pass must say which
shape it
standardizes on.

---

## Primary sources

### S1 — メットライフ生命, "USドル建終身保険 ドルスマート S" 商品パンフレット (商品概要資料)

- Publisher: メットライフ生命保険株式会社 (MetLife Insurance K.K.)
- Document: ドルスマート S 商品パンフレット, 正式名称「積立利率変動型終身保険（米国通貨建 2002）」,
  document code 補2412-0019 / A605-13（11）（25.04）OT-PDF, Ver.11, 2 pp.,
  "この資料に記載の保障内容などは2025年4月現在のものです"
- Doc type: product summary leaflet (商品概要 / 契約締結前交付書面の補助資料)
- URL: https://spon.metlife.co.jp/document/products_sp/iswl-dollar.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded with a browser User-Agent, 2 pp.,
  text
  extracted and read in full)
- Key content: 契約年齢範囲 満6歳～満80歳; 最低保険金額 3万米ドル; 保険期間 終身;
  最低保証積立利率 年3.00％（予定利率）; 積立利率 set 毎月1日; 増加死亡保険金額 (the uplift);
  特別積立金 at 10 and 20 years; the three-layer charge stack; 解約控除 window; 為替手数料
  TTM＋50銭 / TTM－50銭; rider menu; 契約者配当・満期保険金 なし.

### S2 — メットライフ生命, "ドルスマート S — 重要事項説明書（契約概要・注意喚起情報）・ご契約のしおり・約款"

- Publisher: メットライフ生命保険株式会社
- Document: combined booklet for 契約日が2026年5月1日以降 (the current version at the access date),
  file `iswldollar_20260501.pdf`, 275 pp. The 注意喚起情報 section states
  「記載の内容は2025年12月現在のものです」.
- Doc type: policy conditions (普通保険約款) + policy handbook (ご契約のしおり) + IDD-style
  disclosure (重要事項説明書)
- URL: https://www.metlife.co.jp/content/dam/metlifecom/jp/corp/pdf/yakkan/provision/iswldollar/iswldollar_20260501.pdf
  (index page listing this and the superseded versions:
  https://www.metlife.co.jp/yakkan/provision/iswldollar/)
- Accessed: 2026-08-20. Retrieved: YES (5.2 MB PDF downloaded with a browser User-Agent, 275
  pp.,
  text extracted; the 商品概要, 諸費用, 解約返戻金, 積立利率, 増加死亡保険金額, 失効・復活, 免責,
  普通保険約款第3条/第27条/第46条 and the 低解約返戻金特則 clauses read)
- Key content: 約款第3条（積立金）— 積立利率は月単位の契約応当日ごとに更改, floor at the 予定利率;
  約款第46条（増加死亡保険金額）; 約款第27条（解約返戻金）; 低解約返戻金特則 with the published
  低解約返戻金割合 scale 70％/77.5％/85％/92.5％; two full 解約返戻金額例表 (with and without the
  特則); 自殺免責3年; 復活1年; 自動振替貸付; 契約者貸付; 前納.

### S3 — ジブラルタ生命, "積立利率更改型一時払終身保険（23）（米国ドル建・豪ドル建） ご契約のしおり・約款"

- Publisher: ジブラルタ生命保険株式会社 (Gibraltar Life Insurance Co., Ltd.)
- Document: 2023年10月版 ご契約のしおり／約款, 172 pp., covering the 基本タイプ and the
  積立金定期引出タイプ plus 保険料円入金特約・円支払特約・年金支払移行特約
- Doc type: policy conditions + policy handbook
- URL: https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/L411_ichijibarai_syusin_202310.pdf
- Accessed: 2026-08-20. Retrieved: YES (3.4 MB PDF, 172 pp.; WebFetch's own text layer was
  unusable, so the file was re-extracted locally with PyMuPDF and the 特徴としくみ, 積立利率,
  積立利率適用期間・指標金利, 解約と解約返戻金, 市場価格調整率, 解約控除率, 適用する為替レート
  and 免責 sections read)
- Key content: death benefit = max(積立金相当額, 解約返戻金額); 基本保険金額 at issue = 一時払保険料;
  積立利率 formula (基準利率 ±1.5％ band less three charge rates, floor 0.01％, cap
  (米国債利回り平均値+2.0％) less charges); 積立利率適用期間 by currency and age (USD 20y/15y/1y,
  AUD 10y/1y) with the named 指標金利 indices; the **full published MVA rate table** by elapsed
  year × interest-rate move for a 15-year 積立利率適用期間; the **full 解約控除率 run-off table**
  7.0％→0.7％ over ten years; 為替レート 米国ドル TTM＋50銭 / TTM－1銭, 豪ドル TTM＋50銭 /
  TTM－3銭; 自殺免責2年.

### S4 — ジブラルタ生命, "積立利率更改型一時払終身保険（23）積立利率（外貨建一時払商品）" 利率開示ページ

- Publisher: ジブラルタ生命保険株式会社
- Doc type: rate disclosure page (最新の積立利率・過去の積立利率・最新の基準利率・過去の基準利率)
- URL: https://www.gib-life.co.jp/st/intro/products/kyotsu/rate/tatsuka_syushin_23/fxrate/
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent; server-rendered
  HTML,
  the current and the 2026 historical rate tables read)
- Key content: 契約年齢（被保険者）0歳～90歳, split 0–79 / 80–90 for the USD 積立利率適用期間;
  declared 積立利率 and 実質的な利回り for 2026-08-16 to 2026-08-31 and the fortnightly history
  back through 2026; the 上限利率 flag; 積立利率 is declared **twice a month** (1st and 16th) for
  new business, not monthly.

### S5 — 明治安田生命, "つみたてドル建終身" 商品ページ

- Publisher: 明治安田生命保険相互会社
- Document: product page for 「5年ごと配当付利率変動型積立終身保険（低解約返戻金型・指定通貨建）
  つみたてドル建終身」, including the 為替リスク, 諸費用, 低解約返戻金期間 and 予定利率 sections
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find/list/dolshushin/
- Accessed: 2026-08-20. Retrieved: YES (server-rendered HTML, 87 KB, fetched with a browser
  User-Agent and read in full)
- Key content: 契約年齢 被保険者 0歳～満75歳 / ご契約者 満18歳～満75歳; premiums payable as a
  **level yen amount**; 払込期間 10–30 years in 5-year steps; 第1保険期間 (低解約返戻金期間,
  最長15年) then 第2保険期間 with the 予定利率 reset every 5 years; 最低保証予定利率 0.25％;
  low-surrender factor 70％ / graded / 100％ and the surrender-charge factor
  1−20％×(1−経過月数÷120); 入金用為替レート TTM＋25銭, 支払用為替レート TTM－25銭;
  explicit statement that this product has **no** 市場価格調整; 特定保険契約 status under
  保険業法第300条の2.

### S6 — 明治安田生命, "外貨建保険に適用される予定利率"

- Publisher: 明治安田生命保険相互会社
- Doc type: rate disclosure page
- URL: https://www.meijiyasuda.co.jp/norapl/find/rate/dolcommon/planned_interest_rate/
- Accessed: 2026-08-20. Retrieved: YES (server-rendered HTML, read in full)
- Key content: つみたてドル建終身 第1保険期間 予定利率 **3.50％** for 契約日 2026年9月1日
  (手続期間 2026-08-01 to 2026-08-31), declared 毎月1日; 第2保険期間 index = the average of the
  6-month and 5-year US Treasury yields, reset every 5 years, floor 0.25％, last reset
  between
  ages 101 and 105; sibling products' rates declared twice monthly (1st and 16th) — e.g.
  外貨建・明治安田の一時払養老保険 4.44％/4.67％/4.59％ for 7/10/15-year terms,
  外貨建・そなえてふやす介護終身保険 4.45％, all for 契約日 2026-08-16 to 2026-08-31.

### S7 — オリックス生命, "無配当 米国ドル建終身保険（低解約払戻金型） ご契約のしおり・約款"

- Publisher: オリックス生命保険株式会社
- Document: ご契約のしおり／約款 2023年11月, 148 pp., covering the main contract and the
  米国ドル建特定疾病障害介護終身保険特約（低解約払戻金型）
- Doc type: policy conditions + policy handbook
- URL: https://www.orixlife.co.jp/customer/webclause/pdf/webyakkan_bright_20231102.pdf
- Accessed: 2026-08-20. Retrieved: YES (2.9 MB PDF, 148 pp., extracted with PyMuPDF; the
  諸費用, 円入金特約, 円支払特約, 解約と解約払戻金, 猶予期間と失効, 復活 and 免責 sections read)
- Key content: this is the **fixed-予定利率 (定額)** USD whole life — no 積立利率, no MVA. Included
  for contrast and for the mechanics shared with the crediting-rate products: 解約払戻金支払割合
  **7割 flat** through the 低解約払戻期間 (= 保険料払込期間); 解約控除 over the shorter of the
  premium-paying period or 10 years, deducted from the 責任準備金; 円入金特約 mandatory, 円支払特約
  optional, both at 当社所定の為替レート (no published 銭 spread, floored at TTB on payout);
  猶予期間 月払 = 払込期月の翌月初日から末日, 年払・半年払 = 翌月初日から翌々月の月単位の契約応当日;
  復活 **3年以内**; 自殺免責3年; 告知義務違反 2年.

### S8 — 三井住友海上プライマリー生命, "外貨建定額終身保険（円建終身移行特約付）" ご契約者さま用商品説明資料

- Publisher: 三井住友海上プライマリー生命保険株式会社
- Document: ご契約者さま用商品説明資料, 4 pp., document code MSPL-2204-B-0278-00, covering the
  brands 「しあわせ、ずっと」「しあわせの架け橋」「GROWING LIFE」(sold 2012–2022; the product is
  closed to new business)
- Doc type: product explanation sheet (existing policyholders)
- URL: https://www.ms-primary.com/products/product_stop/pdf/products_stop_FLtumitate.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 4 pp., text extracted and read in
  full)
- Key content: 契約年齢 0歳～87歳; 契約通貨 米ドル・豪ドル・ユーロ; 積立利率適用期間 10 years
  (3 years if age ≥81 at 契約日 or 更改日); the **target-value mechanic** — 目標値 105％〜200％ in
  1％ steps against the yen-converted single premium, automatic conversion to a yen whole
  life on
  目標達成, plus conversion on demand at any time; **two vintages of the 解約控除率 table**
  (contracts before 2019-04: 10％→0％ by whole year; contracts from 2019-05: 5％→0％); no
  解約控除 after conversion to the yen whole life; 円支払特約 rate TTM－50銭; 年金管理費 1％ of
  each annuity payment; death benefit = max(保障基準価格, 解約払戻金額).

### S9 — Ｔ&Ｄフィナンシャル生命, "生涯プレミアムワールド4 — 目標値到達時終身保険移行特約について"

- Publisher: Ｔ&Ｄフィナンシャル生命保険株式会社
- Document: product website section for 「生涯プレミアムワールド4
  無配当外国為替連動型終身保険（積立利率更改・通貨選択Ⅳ型）」, 定期支払コース, document code
  316-19-C032; the product is closed to new business
- Doc type: product page (consumer)
- URL: https://www.tdf-life.co.jp/pre_world4/pre_world4_shushinikou2.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML,
  read in full)
- Key content: 目標値 selectable at issue from **100％ / 105％ / 110％** of the 基本保険金額,
  changeable any number of times before the target is hit; the target is tested **every
  business
  day from one year after 契約日**; on reaching it the contract converts automatically to a yen
  whole life and the death benefit and surrender value are fixed in yen, after which neither
  FX
  nor MVA applies; the target test itself is made on the 解約払戻金額 and therefore *does* carry
  FX and MVA.

### S10 — Ｔ&Ｄフィナンシャル生命, "生涯プレミアムワールド4 — 諸費用について"

- Publisher: Ｔ&Ｄフィナンシャル生命保険株式会社
- Doc type: product page (consumer), charge disclosure
- URL: https://www.tdf-life.co.jp/pre_world4/pre_world4_gokeiyaku02.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, read in full)
- Key content: the **contract-inception charge is published as a flat percentage of the
  single
  premium, banded by issue age**: 40–69歳 4.50％, 70–79歳 3.00％, 80–84歳 2.00％, 85–90歳 2.00％
  (which also pins the issue-age envelope at 40–90). No separate in-force charge: the 積立利率
  is
  set net of ご契約の維持等に必要な費用, 死亡保険金に関する費用 and 累積追加額に関する費用.
  年金の支払管理等に必要な費用 up to 1.0％ of each annuity payment.

### S11 — Ｔ&Ｄフィナンシャル生命, "生涯プレミアムワールド4 — 積立コース" と "為替レートについて"

- Publisher: Ｔ&Ｄフィナンシャル生命保険株式会社
- Doc type: product pages (consumer)
- URLs: https://www.tdf-life.co.jp/pre_world4/tsumitate.html and
  https://www.tdf-life.co.jp/pre_world4/rate/exchange_rate.html
- Accessed: 2026-08-20. Retrieved: YES (both fetched with a browser User-Agent and read in
  full)
- Key content: this is the **外国為替連動型** shape — premium paid and benefits received in yen,
  with a 為替変動率 = (為替レート at the valuation date) ÷ (為替レート at 契約日) applied to the
  benefit; "一時払保険料の払込や累積追加額を払い出す際に為替手数料を別途、ご負担いただくことは
  ありません"; the FX rate used is the plain TTM of a nominated bank, published each business day
  around 11:00 (observed values: 2026-08-19 US$1 = ¥159.43, A$1 = ¥112.83); 積立利率・追加率 set
  at 契約日 by currency and issue age from a named 指標金利 and reset at each 積立利率更改日.

### S12 — 第一フロンティア生命, "積立利率変動型終身保険（20）（通貨指定型）" 市場価格調整用利率ページ

- Publisher: 第一フロンティア生命保険株式会社
- Doc type: rate disclosure page (解約(減額)時に適用される市場価格調整用利率)
- URL: https://www.d-frontier-life.co.jp/products/index_hendo_shushin_choice_20_b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML,
  read in full)
- Key content: currencies 米ドル / 豪ドル / 円 in one 通貨指定型 chassis; 積立利率保証期間
  30y and 10y (USD), 20y and 10y (AUD), 30y and 15y (JPY); published 市場価格調整用利率 for
  2026-08-16 to 2026-08-31 — 死亡保障型 USD 5.50％ (30y) / 4.95％ (10y), AUD 5.15％ (20y) /
  5.06％ (10y), JPY 3.67％ (30y) / 2.78％ (15y); 死亡・認知症介護保障型 USD 5.50％ / 4.72％,
  AUD 5.15％, JPY 3.22％ / 2.06％. The page states explicitly that the 市場価格調整用利率 is the
  rate used **both** to compute the 積立利率 and to compute the MVA rate, and is not itself the
  applied 積立利率.

### S13 — ＳＭＢＣ日興証券, "重要情報シート — ダブル・フロンティア終身（円建／米ドル建／豪ドル建）"

- Publisher: ＳＭＢＣ日興証券株式会社 (distributor) for 第一フロンティア生命 (組成会社)
- Document: 重要情報シート, 2024年1月版, 4 pp., registration code (登)B22F0412（2023.2.2）; the
  product is 「積立利率変動型定額部分付変額終身保険（15）／（通貨指定型）」
- Doc type: distributor key information sheet (FSA 重要情報シート format)
- URL: https://www.smbcnikko.co.jp/products/insurance/pdf/jyuyojoho/d_frontier_shushin.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 4 pp., text extracted and read in
  full)
- Key content: **解約控除 published as a range by 第1保険期間 and elapsed year — 外貨建 6.5％〜0.0％,
  円建 3.5％〜0.1％, applied to the 基本保険金額**; the charge stack for the 定額部分 (the
  ご契約の締結・維持 and 死亡保険金 costs are taken *inside* the 積立利率, not as an explicit
  deduction); 保険契約関係費 2.35％ p.a. on the 変額部分 plus 信託報酬 0.22％; the **distributor
  commission structure** — 契約時手数料 4.00％ or 2.60％ of the single premium (FX) / 1.85％ or
  0.30％ (JPY), 継続手数料 0.75％ or 0.10％ p.a. of the account value (FX) / 0.05％ (JPY), payable
  for at most 7 years; the FX return distribution used in the sheet (USD 1-year returns over
  2017-12 to 2022-11: max 30.4％, min −5.5％, mean 3.4％; AUD max 27.6％, min −16.0％, mean
  1.5％); tax treatment (一時払保険料 → 一般生命保険料控除; 死亡保険金 → 相続税 where
  契約者=被保険者; 解約返還金 − 一時払保険料 → 一時所得＋住民税).

### S14 — プルデンシャル生命, "外貨建一時払保険の基準利率"

- Publisher: プルデンシャル生命保険株式会社
- Document: rate disclosure page for 「米国ドル建利率変動型一時払終身保険（無告知型）」
- Doc type: rate disclosure page
- URL: https://www.prudential.co.jp/contractor/rate_simulation/standard/
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent; page is Shift-JIS
  server-rendered HTML, decoded and read)
- Key content: 積立利率保証期間 of **10 years or 15 years**; the 基準利率 is declared
  **twice monthly**; the published series runs 2026-08-16〜08-31 5.15％ (10y) / 5.29％ (15y);
  2026-08-01〜08-15 5.14％ / 5.27％; 2026-07-16〜07-31 5.01％ / 5.14％;
  2026-07-01〜07-15 4.93％ / 5.04％; 2026-06-16〜06-30 4.99％ / 5.11％;
  2026-06-01〜06-15 5.05％ / 5.18％; 2026-05-16〜05-31 4.86％ / 5.00％;
  2026-05-01〜05-15 4.75％ / 4.91％; 2026-04-16〜04-30 4.78％ / 4.93％;
  2026-04-01〜04-15 4.85％ / 4.99％; 2026-03-16〜03-31 4.60％ / 4.76％;
  2026-03-01〜03-15 4.52％ / 4.68％; 2026-02-16〜02-28 4.63％ / 4.79％;
  2026-02-01〜02-15 4.68％ / 4.84％; 2026-01-16〜01-31 4.63％ / 4.79％;
  2026-01-01〜01-15 4.62％ / 4.78％; 2025-12-16〜12-31 4.62％ / 4.78％;
  2025-12-01〜12-15 4.57％ / 4.73％; 2025-11-16〜11-30 4.61％ / 4.76％;
  2025-11-01〜11-15 4.45％ / 4.60％. (A one-year 基準利率 history at a fortnightly step — the
  best single public series for calibrating a crediting-rate scenario.)

### S15 — マニュライフ生命, "こだわり外貨終身" 商品ページ・積立利率履歴ページ・通貨選択型一時払終身保険 約款

- Publisher: マニュライフ生命保険株式会社
- Doc type: product page, published crediting-rate history, policy conditions
- URLs:
  https://www.manulife.co.jp/ja/individual/products/goods/kodawari-gaikasyushin.html ;
  https://www.manulife.co.jp/ja/individual/rates/kodawari-gaikasyushin/int-past.html ;
  https://www.manulife.co.jp/ja/individual/rates.html ;
  https://www.manulife.co.jp/content/dam/insurance/jp/images/individual/policyholder/web-yakkan/miraisyushin/21120855-387466.pdf
- Accessed: 2026-08-20. **Retrieved: NO** — every manulife.co.jp URL returned HTTP 403 to
  WebFetch and to curl, with and without a browser User-Agent, with Referer and cookie jar,
  and
  over HTTP/1.1. The block is a WAF policy, not a UA check. **No fact in this file is
  sourced to
  Manulife**; the 積立利率 history and the 目標到達時円建終身保険移行特約 wording that these pages
  would have supplied are covered instead by [S4] [S14] and by [S8] [S9] respectively.

### S16 — メットライフ生命, 積立利率公表ページ

- Publisher: メットライフ生命保険株式会社
- Doc type: rate disclosure page (the page [S2] names as the place the declared 積立利率 is
  published)
- URL: https://www.metlife.co.jp/lf1/ahp405/08.html
- Accessed: 2026-08-20. **Retrieved: NO** — HTTP 200, but the response is a React SPA shell
  (`<div id="root">` plus a JS bundle); no rate content is in the served HTML and the page
  is not
  machine-fetchable. The declared crediting-rate history for ドルスマート S is therefore
  **not** available in this file; only the guaranteed floor and the illustration rates in
  [S1] [S2] are.

---

## Regulatory and actuarial references

### R1 — 金融庁, 「標準責任準備金制度にかかる告示の一部改正（案）」等に対するパブリックコメントの結果等について

- Publisher: 金融庁 (Financial Services Agency)
- Document: 2021-06-30 publication; 別紙２「平成8年大蔵省告示第48号及び平成13年金融庁告示第24号の
  一部を改正する件（新旧対照表）」, 21 pp. (vertical Japanese text)
- Doc type: FSA notification amendment + public-comment response
- URLs: https://www.fsa.go.jp/news/r2/hoken/20210630/20210630.html (index) and
  https://www.fsa.go.jp/news/r2/hoken/20210630/02.pdf (新旧対照表)
- Accessed: 2026-08-20. Retrieved: YES (index page via WebFetch; the 新旧対照表 PDF downloaded
  and
  extracted with PyMuPDF, the vertical single-character lines re-joined before reading)
- Content: this is the amendment that brought **米国通貨建保険契約 and 豪州通貨建保険契約 into the
  標準責任準備金 regime**. Effective 2021-10-01, except the 平成13年金融庁告示第24号 amendments
  effective 2022-04-01; 8 comments from 3 respondents in the 2021-04-23 to 2021-05-24
  window.
  The 標準利率 (予定利率) for USD/AUD contracts is derived from a 基準利率 = Σ over bands of
  (対象利率 in band × 安全率係数). 対象利率 for 第一号保険契約 = the lower of (i) the average over
  the one month ending the month before the 基準日 and (ii) the average over three months, of
  [10-year A-rated 表示通貨建社債 yield + 20-year yield] ÷ 2; for 第二号保険契約 the 10-year yield
  alone. 安全率係数 (USD / AUD): ≤0％ 1.0/1.0; 0–2％ 0.95/0.95; 2–3％ 0.9/0.95; 3–4％ 0.9/0.9;
  4–5％ 0.85/0.9; 5–6％ 0.8/0.9; >6％ 0.75/0.8. **基準日 is the 1st of every month**; when the
  基準利率 differs from the applied 予定利率 by ≥0.05％ the 予定利率 moves to the nearest multiple
  of 0.05％ and applies to contracts written from one month after the 基準日. A separate
  slower track (three-year / ten-year averages, 0.5％ trigger, 0.25％ rounding, annual 4/1
  application) governs USD/AUD contracts that are neither 第一号 nor 第二号. Other foreign
  currencies are **excluded** from the 対象契約 (the amended 対象契約 list reads
  「外国通貨（アメリカ合衆国通貨及びオーストラリア通貨を除く。）をもって…表示する保険契約」 as an
  exclusion). A new 対象契約 class was also added for 本邦通貨建 contracts that guarantee a
  予定利率 per 区分した保険期間 — i.e. the yen-denominated 利率更改型 shape.

### R2 — 金融庁, 保険会社向けの総合的な監督指針の一部改正（新旧対照表）, 2021-06-30

- Publisher: 金融庁
- Document: 別紙３, 3 pp.
- Doc type: supervisory guideline amendment
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/03.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 3 pp., text extracted and read in
  full)
- Content: consequential renumbering in Ⅱ－2－1－3－1（保険料積立金の積立）from 責任準備金告示
  第5項第1号 to 第14項第1号, and the substitution of 「責任準備金告示に規定する予定利率」 for
  「責任準備金告示第4項に規定する率」 as the definition of 標準利率. The 代替的方式 condition is
  extended to non-yen contracts: the ア.–ウ. conditions apply
  「（邦貨建保険契約以外の保険契約については、その特性に応じ、次のア．からウ．までの条件に準じた
  条件）」. The 10％ tolerance between 代替的方式 and 標準的方式 results is unchanged.

### R3 — 金融庁, 保険会社向けの総合的な監督指針 Ⅱ－4 業務の適切性

- Publisher: 金融庁
- Doc type: supervisory guideline (current text)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02d.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML,
  the 契約締結前交付書面, 外貨建て保険, MVA and 外貨建て保険に係る募集上の留意事項 sections read)
- Content: 特定保険契約 (法第300条の2) requires a 契約締結前交付書面 under 準用金融商品取引法
  第37条の3第1項. The 「契約概要」 item list is product-specific; for **外貨建て保険** it must add
  (l) that the yen-converted benefit at payment can fall below the yen-converted benefit at
  contract date and that a loss may arise, and (m) an explanation of the fees that arise
  specifically from contracting in a foreign currency. For **MVA products** it must add (l)
  that
  the product reflects the price movement of the backing assets in the surrender value, (m)
  that
  surrender within a period can produce a loss because the surrender value is computed on
  market
  rates, (n) where a coefficient is set to cover the rate movement between the calculation
  basis
  date and surrender and the transaction costs of liquidating assets, the effect of that
  coefficient — "解約時の保険料積立金に対して控除される割合の例示等", and (o) the in-force charges.
  MVA is defined in a footnote as 「保険料積立金…に契約時と解約時の金利差によって生じる運用対象
  資産の時価変動に基づく調整を加えたものを解約返戻金とする仕組み」. Separately,
  「外貨建て保険に係る募集上の留意事項」 requires, for non-corporate policyholders, full explanation
  of FX risk at the point of sale and **the taking of a signed confirmation
  (確認書等の取付けを徹底)** that the policyholder understood it. 契約締結前交付書面 for 特定保険契約
  must be set in ≥8-point type with certain items at ≥12 point.

### R4 — 金融庁, 保険会社向けの総合的な監督指針 Ⅱ－2 財務の健全性

- Publisher: 金融庁
- Doc type: supervisory guideline (current text)
- URL: https://www.fsa.go.jp/common/law/guide/ins/02b.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML;
  the 価格変動準備金 / 危険準備金 provision on 外貨建て保険 read)
- Content: where 規則第66条第2項 is used to compute the 価格変動準備金 within the 責任準備金 of
  外貨建て保険, the asset scope must be decided from the asset classes corresponding to the
  外貨建て保険 product segment on a properly segregated accounting basis, and the
  **危険準備金Ⅱ** for the contracts backed by those assets must use the **外貨建て保険 risk
  coefficient**. The policy and process must be documented and applied consistently.

### R5 — 金融庁, "リスク性金融商品の販売会社等による顧客本位の業務運営に関するモニタリング結果（2023事務年度中間報告）"

- Publisher: 金融庁
- Document: 2024（令和6）年4月3日, 6 pp.
- Doc type: supervisory monitoring report
- URL: https://www.fsa.go.jp/news/r5/kokyakuhoni/202403/01.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 6 pp., text extracted and read in
  full)
- Content: monitoring universe — 13 regional bank groups, 6 major banks, 8 insurers. **About
  60％
  of 外貨建一時払保険 are surrendered within four years of purchase**, concentrated in ターゲット型
  policies; the 2023-08-31 run-off cohort (n = 549,781) underperformed the ≥5-year cohort
  (n = 89,452) and comparable developed-market bond funds. Decomposition of the run-off
  cohort's
  return: 積立金増加効果 thin, most of the profit from 円安, and **解約等費用 (市場価格調整と解約
  控除費) push the margin down** — annualized components printed as 3.6％, 0.2％, −1.8％, −1.0％,
  5.2％, 0.8％, 0.2％, 0.5％. Almost all ターゲット型 policies are surrendered on reaching the
  target and the same product is re-sold to the same customer, double-charging the sales
  commission; the FSA says distributors should tell customers **before** the target is
  reached
  that the target can be raised free of charge. Of 287 customer cards analysed, ~20％ showed
  knowledge/experience or investment-policy concerns; among the 87 customers who complained,
  just
  under 30％. Distributor commission is **L-shaped — e.g. 5.5％ in year 1, 0.1％ thereafter**,
  which the FSA links to churning.

### R6 — 金融庁, "リスク性金融商品の販売・組成会社による顧客本位の業務運営に関するモニタリング結果（概要版）"

- Publisher: 金融庁
- Document: 2024（令和6）年7月5日, 9 pp.
- Doc type: supervisory monitoring report (summary)
- URL: https://www.fsa.go.jp/news/r6/kokyakuhoni/fdreport/01.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 9 pp., text extracted and read in
  full)
- Content: the **definition of ターゲット型保険** — a policy that, when the yen-converted account
  value reaches a customer-set 目標値 measured against the premium paid, automatically locks
  the
  result in yen and converts to a yen whole life or similar; 「例えば105％、110〜200％（10％きざみ）
  で設定できる」. **Average holding period 2.5 years.** Product committees adopted products on
  headline 予定利率 / 積立利率 without risk-return analysis. Good-practice examples include the
  manufacturer supplying the distributor with a periodic list of ターゲット型 contracts so the
  distributor can follow up before the target is reached.

### R7 — 生命保険協会, 「外貨建保険販売資格試験」の創設について

- Publisher: 一般社団法人 生命保険協会 (The Life Insurance Association of Japan)
- Document: news release attachment, 2020-02-21, 3 pp.
- Doc type: industry association news release
- URLs: https://www.seiho.or.jp/info/news/2020/20200221.html (index; the body is JS-rendered and
  the release content lives in the linked PDF) and
  https://www.seiho.or.jp/info/news/2019/pdf/20200221.pdf (the release itself)
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 3 pp., text extracted and read in
  full)
- Content: the **外貨建保険 complaint series at bank-channel agencies**: 2012 597, 2013 615,
  2014 922, 2015 1,239, 2016 1,665, 2017 1,888, 2018 2,543, 2019 (Apr–Sep) 1,352 —
  annualized
  2,704; complaint rate against in-force count falling 0.14％ → 0.08％ over the same period.
  **68％ of complaints are 説明不十分**, and within those: 元本割れリスク 37％, 適合性の確認 14％,
  預金誤認 8％, 高齢者対応 6％, その他 28％. The 2019-10-23 市場ワーキング・グループ criticism is
  cited as the trigger. Scheme: industry-common textbook from ~2020-04, **試験開始 2020年10月目途**,
  **販売資格者登録制 (licensing) from ~2022年4月**, with a seven-module curriculum (外貨の基礎知識;
  発売の背景; 商品の概要; 隣接業界の投資性金融商品; コンプライアンス; 募集に係るリテラシー;
  各社独自の商品知識). Registration requires the 専門課程試験 pass plus the common curriculum, in
  the same pattern as the 変額保険販売資格.

### R8 — 生命保険協会, "生命保険商品に関する適正表示ガイドライン"

- Publisher: 一般社団法人 生命保険協会
- Document: 令和8年1月29日 (2026-01-29) edition, 36 pp.; 制定 平成15年10月15日, amended repeatedly
- Doc type: industry association guideline
- URL: https://www.seiho.or.jp/activity/guideline/pdf/tekiseihyouji.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 36 pp., text extracted; the 特定保険契約,
  外貨建て保険 and MVA sections read)
- Content: for **外貨建て一時払い保険（終身保険・養老保険・年金保険）**, the 設計書 must show the
  **実質的な利回り** alongside the 積立利率 / 予定利率. For 外貨建て終身保険 the definition is: the
  annualized compound yield at which the account value or surrender value at a future point,
  discounted over the elapsed period, equals the premium paid — **and the future point to
  display
  is the point at which the MVA, the rate-variation period and the surrender charge have all
  expired**. (Generation-benefit variants add the cumulative 生存給付金.) Variable products,
  mixed fixed/variable products and life annuities are out of scope. The guideline also sets
  the
  standard risk wording for 外貨建て保険 and for MVA products
  (「中途解約時の市場金利がご契約時と比較して上昇した場合には、解約返戻金は減少し、逆に、下落した
  場合には増加することがあります」), and requires that any illustration showing the effect of a
  market move also print the no-move case as a baseline
  (「金利変動であれば死亡・解約時に使用する積立利率が契約時に計算される利率と同じ」).

### R9 — 金融庁, "外貨建保険について"（生命保険協会との意見交換会 論点メモ）

- Publisher: 金融庁
- Document: 2019年2月 論点資料, 6 pp. (item 1 of a multi-topic memo)
- Doc type: FSA discussion memo
- URL: https://www.fsa.go.jp/common/ronten/201902/07.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, 6 pp., text extracted and read)
- Content: the FSA's framing of the product — 外貨建保険 pushes FX risk onto the customer
  relative
  to a yen savings product; complaints about undisclosed FX and principal-loss risk are
  numerous;
  customers compare these against investment trusts, so the sales material must be
  **comparable with an investment trust prospectus (目論見書)** and the information must be
  「見える化」; the FSA and the industry drafted such material with several insurers and the
  生命保険協会 asked the 全国銀行協会 to have banks use it.

### R10 — 生命保険契約者保護機構, 保険契約者保護制度Q&A Q1

- Publisher: 生命保険契約者保護機構 (Life Insurance Policyholders Protection Corporation of Japan)
- Doc type: statutory scheme Q&A
- URL: https://www.seihohogo.jp/qa/qa1.html
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML,
  read in full)
- Content: established 1998-12-01 under 保険業法; every life insurer doing business in Japan is
  a
  member. On a failure the 保護機構 supports a 救済保険会社, a 承継保険会社 or its own assumption of
  the contracts; **補償対象契約 are covered to 90％ of the 責任準備金等 at the failure date**
  (less for 高予定利率契約, per its Q13), and during the suspension of business benefits are paid
  at 90％ of the previous sum insured. The Q&A does not carve out or specially treat
  外貨建 contracts — the same 90％-of-責任準備金等 rule is the one insurers reproduce in their
  own 外貨建 booklets (see the 保護機構 section of [S7]).

### R11 — 国税庁, タックスアンサー No.1903「給与所得者に生命保険の満期返戻金などの一時所得があった場合」

- Publisher: 国税庁 (National Tax Agency)
- Document: [令和7年4月1日現在法令等]
- Doc type: tax authority guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1903.htm
- Accessed: 2026-08-20. Retrieved: YES (fetched with a browser User-Agent, server-rendered
  HTML,
  read in full)
- Content: where the premium payer receives the maturity/surrender proceeds as a lump sum
  the
  income is 一時所得; 一時所得の金額 = 受取保険金 − (支払保険料総額 − 剰余金) − 特別控除 50万円,
  and **half** of that is the taxable amount. An employee with ≤¥20,000,000 of employment
  income
  need not file unless non-employment income exceeds ¥200,000, tested on the halved amount.
  Statutory basis: 所法22, 34, 120, 121; 所令183; 所基通34-4, 121-6. The page does **not**
  separately address 為替差益 on a foreign-currency policy — see the gaps section.

---

## Fact extraction

### 1. Product architecture and the three shapes

- 積立利率変動型 (MetLife ドルスマート S, 正式名称「積立利率変動型終身保険（米国通貨建 2002）」):
  level premium, whole-of-life cover, an account value (積立金) credited at a rate redeclared
  every month, no MVA. [S1] [S2]
- 積立利率更改型 一時払 (Gibraltar 積立利率更改型一時払終身保険（23）; MS Primary
  外貨建定額終身保険; T&D 生涯プレミアムワールド4; Dai-ichi Frontier 積立利率変動型終身保険（20）):
  single premium, a rate fixed for a multi-year 積立利率適用期間 / 積立利率保証期間 and reset at
  each 積立利率計算基準日 / 更改日, **with** an MVA on surrender inside the period. [S3] [S8] [S11]
  [S12]
- 指定通貨建 with yen-fixed premiums (Meiji Yasuda つみたてドル建終身): the customer pays a level
  **yen** amount, converted to USD at each payment; 第1保険期間 fixes the 予定利率 to 払込満了,
  then 第2保険期間 resets it every five years; explicitly **no** MVA. [S5] [S6]
- 定額 (fixed 予定利率) USD whole life exists alongside all of these (ORIX 米国ドル建終身保険
  （低解約払戻金型）): no crediting rate, no MVA, a flat 70％ low-surrender factor. [S7]
- All are 特定保険契約 under 保険業法第300条の2, so 金融商品取引法第40条（適合性の原則）applies
  by 準用 and a 契約締結前交付書面 is mandatory. [S5] [R3]

### 2. Currencies

- 米ドル建 and 豪ドル建 are the two universally offered currencies. [S3] [S12] [S11]
- ユーロ建 appears in one carrier's 通貨指定型 chassis alongside USD and AUD. [S8]
- One carrier's 通貨指定型 chassis offers **円 as a third "currency"** on the same product, with
  its own 積立利率保証期間 menu (30y / 15y) and its own MVA rate. [S12]
- Only USD and AUD are inside the 標準責任準備金 regime; all other foreign currencies are
  excluded from the 対象契約 by the 2021 amendment. [R1]

### 3. Issue-age and term envelopes

| Carrier / shape | 契約年齢 | 保険期間 | 保険料払込期間 |
|---|---|---|---|
| 積立利率変動型 平準払 [S1] | 満6歳〜満80歳 | 終身 | short-pay (e.g. 60歳払込満了) or whole-life pay |
| 積立利率更改型 一時払 [S4] | 0歳〜90歳 | 終身 | 一時払 |
| 指定通貨建 yen-premium [S5] | 被保険者 0歳〜満75歳; 契約者 満18歳〜満75歳 | 終身 | 10–30 years in 5-year steps |
| 一時払 with 円建終身移行特約 [S8] | 0歳〜87歳 | 終身 | 一時払 |
| 外国為替連動型 一時払 [S10] | 40歳〜90歳 (implied by the charge bands) | 終身 | 一時払 |
| 定額 USD 平準払 [S7] | not published in the retrieved booklet | 終身 | low-surrender period = 払込期間 |

- The 積立利率適用期間 depends on attained age at the reset: USD 20 years below 80, 15 years from
  80 to under 91, **1 year from 91**; AUD 10 years below 91, 1 year from 91. The one-year
  band is
  disclosed as generally producing a lower rate. [S3]
- Another single-premium chassis uses a 10-year 積立利率適用期間, dropping to 3 years where the
  insured is 81 or older at 契約日 or 更改日. [S8]
- A third publishes 積立利率保証期間 of 30 or 10 years (USD), 20 or 10 (AUD), 30 or 15 (JPY). [S12]
- A fourth publishes 10 or 15 years (USD only). [S14]

### 4. Minimums

- 最低保険金額 **3万米ドル** on the level-premium 積立利率変動型 product. [S1]
- On the single-premium 積立利率更改型 product, **契約時の基本保険金額 = 一時払保険料** (the sum
  assured is defined as the single premium itself). [S3]
- No published minimum single premium was found in any retrieved document — see the gaps
  section.

### 5. The crediting rate (積立利率) — declaration and mechanics

**Monthly-declared (積立利率変動型).**

- 「積立利率は毎月1日に設定されます。」 The rate for a month is **the previous-but-one month's
  investment return on the segregated asset pool for this product, less the 資産運用のための運営
  費率, the 積立金を最低保証するための保証費率 and その他費用（所定の率）**. Once set it credits the
  account value for one month. [S1] [S2]
- The 約款 clause is worded differently and is the operative one: 「積立利率は、契約後、月単位の契約
  応当日ごとに更改を行ないます」 (第3条第2項) — i.e. declared on the 1st but **applied from each
  monthly policy anniversary**. A model that credits on calendar month-ends will be off by
  the
  policy-anniversary offset. [S2]
- 約款第3条第3項: 「積立利率は、この保険契約の予定利率…を下回ることはありません」 — the floor is
  the contract's own 予定利率, fixed at issue, not a rate the insurer redeclares. [S2]
- The insurer notifies the policyholder annually of the current 積立利率 (the rate for the month
  containing the policy anniversary) and of the past twelve monthly rates. [S2]
- The declared-rate history page for this product could not be retrieved (SPA) — [S16].

**Period-fixed (積立利率更改型 / 保証期間型).**

- The 積立利率 is set at 契約日 and at each 積立利率計算基準日, and is **unchanged through the whole
  積立利率適用期間**. Rates are published for two windows a month (contracts dated 1st–15th and
  16th–month-end). [S3] [S4]
- The published formula, for 積立利率適用期間 of 10/15/20 years:

      積立利率 = (a rate the insurer sets within ±1.5% of the 基準利率)
                 − (災害死亡保障費率 + 新契約費率 + 維持費率)

  with an **upper bound** of `(米国債の利回りの平均値 + 2.0%) − (災害死亡保障費率 + 新契約費率 +
  維持費率)` — applied to USD contracts with a 15- or 20-year 積立利率適用期間 — and a **lower bound
  of 0.01%**. For a 1-year 積立利率適用期間 the formula is `当社所定の利率 − (the same three charge
  rates)`. [S3]
- 基準利率 timing: for contracts dated 1st–15th, the average of the 指標金利 over the five
  available days immediately before the **26th of the month before last**; for contracts
  dated
  16th–month-end, the five days before the **11th of the current month**. Same rule for the
  米国債の利回りの平均値 used in the cap. [S3]
- 指標金利, by currency and age band [S3]:
  - USD, age <80 (20-year period): the yield of a bond index of A-rated (A+/A/A−) USD
  20-year
    corporates ("USD US Industrials A+/A/A− 20年"), source Bloomberg Finance L.P.
  - USD, age 80–90 (15-year period): the same index at 10 years.
  - AUD, age <91 (10-year period): the secondary-market yield of 10-year Australian
  government
    bonds.
  - Age ≥91: no index; the 1-year 当社所定の利率 applies.
  - The insurer may change the index with 主務官庁 approval on two months' notice.
- 米国債の利回り used in the cap: 20-year remaining maturity for a 20-year 積立利率適用期間,
  10-year for a 15-year period. [S3]
- Observed declared rates for 2026-08-16 to 2026-08-31 [S4]:
  USD 基本タイプ 4.72% (ages 0–79, 20-year) and 4.72% (ages 80–90, 15-year);
  USD 積立金定期引出タイプ 4.62% / 4.62%; AUD 基本タイプ 4.22% (10-year), 積立金定期引出タイプ
  4.12%. The 実質的な利回り printed alongside them is 4.72% / 4.72% for the 基本タイプ but
  3.32% / 3.57% for the 積立金定期引出タイプ — the gap is the cost of the periodic withdrawal.
- The 積立金定期引出特約 lowers the 積立利率 by the rate required to fund the withdrawals, and the
  withdrawals themselves carry **neither 解約控除 nor 市場価格調整**. [S3]
- Another carrier's 基準利率 series for 米国ドル建利率変動型一時払終身保険（無告知型）, fortnightly,
  runs from 4.45% / 4.60% (10y / 15y, 2025-11-01) to **5.15% / 5.29% (2026-08-16)** — the
  longest
  guarantee period consistently carries the higher rate. [S14]

**Five-year reset after 払込満了 (指定通貨建 yen-premium).**

- 第1保険期間: the 予定利率 is set at 契約日 and applies to 払込満了; declared 毎月1日; **3.50%** for
  contracts dated 2026-09-01. [S6]
- 第2保険期間: reset at the 予定利率計算基準日 (第2保険期間開始日 and every 5th policy anniversary
  after it); index = **the average of the 6-month and 5-year US Treasury yields** plus/minus
  a set
  adjustment; floor **最低保証予定利率 0.25%**; the reset at ages 101–105 is the last one. [S5] [S6]
- The reset drives both the death benefit (fixed for the following five years) and the
  surrender
  value growth rate (which increases monthly). At the 0.25% floor the death benefit does not
  grow at all. [S5]

### 6. Guaranteed floor (最低保証積立利率 / 最低保証予定利率) — the published values

| Shape | Floor | As at | Source |
|---|---|---|---|
| 積立利率変動型 平準払 (USD) | **年3.00%（予定利率）** | 2025-04 leaflet; 2025-12 disclosure | [S1] [S2] |
| 積立利率更改型 一時払 (USD/AUD) | **年0.01%** | 2023-10 booklet | [S3] |
| 指定通貨建 yen-premium (USD), 第2保険期間 | **0.25%** | 2026-08 rate page | [S5] [S6] |

The spread between these — 0.01%, 0.25%, 3.00% — is the single widest cross-carrier
divergence
found, and it is not noise: the 3.00% floor belongs to a 2002-generation level-premium
contract
whose floor *is* its 予定利率 and which therefore carries a long-dated guarantee; the 0.01%
floor
belongs to a single-premium contract that resets its rate every 10–20 years and needs no
guarantee between resets. A representative product must pick a shape before it picks a
floor.

### 7. 市場価格調整 (MVA)

- MVA applies on the 積立利率更改型 / 保証期間型 single-premium shapes and **not** on the
  monthly-declared level-premium shape [S2] nor on the yen-premium 指定通貨建 shape (which states
  「この商品は、解約時の市場価格調整がないため、お客さまが負う金利変動リスクはありません」) [S5].
- The **published formula** [S3]:

      解約返戻金額 = 積立金額 × (1 − 市場価格調整率 − 解約控除率)

  with the 解約控除率 reaching 0 ten years after 契約日. **No MVA is applied** where the surrender
  or reduction falls on an 積立利率計算基準日, or on a day inside a 1-year 積立利率適用期間;
  otherwise it is. [S3]
- Direction: the MVA rate is positive (and so *reduces* the surrender value) when the **基準利率
  applicable at surrender + A** exceeds the 基準利率 under which the contract's current 積立利率 was
  set — i.e. when rates have risen. The published illustration table sets the zero column at
  a
  **−0.1% rate move**, which pins the spread `A` at 0.1%. [S3]
- The **full published MVA rate table** for a 15-year 積立利率適用期間, by elapsed year × 金利変動幅
  [S3]:

      年 \ Δ   +2.0%   +1.5%   +1.0%   +0.5%    0.0%   -0.1%   -0.5%   -1.0%   -1.5%   -2.0%
       1年    0.1795  0.1402  0.0989  0.0553  0.0095  0.0000 -0.0389 -0.0898 -0.1435 -0.2002
       2年    0.1678  0.1309  0.0921  0.0515  0.0088  0.0000 -0.0360 -0.0831 -0.1326 -0.1846
       3年    0.1559  0.1214  0.0854  0.0476  0.0081  0.0000 -0.0332 -0.0765 -0.1218 -0.1693
       4年    0.1439  0.1119  0.0785  0.0437  0.0074  0.0000 -0.0304 -0.0699 -0.1111 -0.1542
       5年    0.1318  0.1023  0.0717  0.0398  0.0068  0.0000 -0.0276 -0.0634 -0.1005 -0.1392
       6年    0.1194  0.0925  0.0647  0.0359  0.0061  0.0000 -0.0248 -0.0568 -0.0900 -0.1245
       7年    0.1069  0.0827  0.0578  0.0320  0.0054  0.0000 -0.0220 -0.0504 -0.0797 -0.1099
       8年    0.0942  0.0727  0.0507  0.0281  0.0047  0.0000 -0.0192 -0.0439 -0.0694 -0.0955
       9年    0.0813  0.0627  0.0436  0.0241  0.0041  0.0000 -0.0165 -0.0375 -0.0592 -0.0813
      10年    0.0682  0.0525  0.0365  0.0201  0.0034  0.0000 -0.0137 -0.0312 -0.0491 -0.0673
      11年    0.0549  0.0422  0.0293  0.0161  0.0027  0.0000 -0.0110 -0.0249 -0.0391 -0.0535
      12年    0.0415  0.0319  0.0221  0.0121  0.0020  0.0000 -0.0082 -0.0186 -0.0292 -0.0399
      13年    0.0279  0.0213  0.0148  0.0081  0.0014  0.0000 -0.0055 -0.0124 -0.0193 -0.0264
      14年    0.0140  0.0107  0.0074  0.0041  0.0007  0.0000 -0.0027 -0.0062 -0.0096 -0.0131
      15年       —       —       —       —       —       —       —       —       —       —

  The 15-year row is dashes because the 15th year *is* the 積立利率計算基準日, where no MVA applies.
  The magnitude decays roughly linearly in remaining term — at Δ = +2.0% the rate falls from
  0.1795 at year 1 to 0.0140 at year 14, i.e. about 0.0126 per remaining year.
- No carrier publishes a closed-form MVA formula; the disclosure regime requires only the
  mechanism, the loss warning and **an illustration of the deduction ratio**
  (「解約時の保険料積立金に対して控除される割合の例示等」) — which is exactly what the table above
  is. [R3]
- Another carrier publishes the 市場価格調整用利率 itself as a fortnightly rate, by currency and
  guarantee period, and states that the same rate is used both to set the 積立利率 and to
  compute
  the MVA. Observed 2026-08-16 to 2026-08-31, 死亡保障型: USD 5.50% (30y) / 4.95% (10y);
  AUD 5.15% (20y) / 5.06% (10y); JPY 3.67% (30y) / 2.78% (15y). [S12]

### 8. 解約控除 (surrender charge) and its run-off

- The **window** is consistently the shorter of the premium-paying period and ten years from
  契約日 for the level-premium products [S1] [S2] [S7], and a flat ten years from 契約日 for the
  single-premium products [S3] [S8].
- **Published run-off — 積立利率更改型 一時払** [S3]: identical for USD and AUD, a straight
  0.7pp-per-year decline over ten years, constant within each policy year, zero from year
  10.

      経過年数  <1     1–2    2–3    3–4    4–5    5–6    6–7    7–8    8–9    9–10   ≥10
      控除率    7.0%   6.3%   5.6%   4.9%   4.2%   3.5%   2.8%   2.1%   1.4%   0.7%   0%

- **Published run-off — 一時払 with 円建終身移行特約**, two vintages [S8]:

      contracts to 2019-04:  10%  9%  8%  7%  6%  5%  4%  3%  2%  1%  0%
      contracts from 2019-05: 5%  4.5% 4%  3.5% 3%  2.5% 2%  1.5% 1%  0.5% 0%

  and **no 解約控除 at all after conversion to the yen whole life**.
- **Published range — 積立利率変動型定額部分付変額終身保険** [S13]: applied to the **基本保険金額**
  (not the account value), 外貨建 **6.5%〜0.0%**, 円建 **3.5%〜0.1%**, by 第1保険期間 and elapsed year.
- **Formula form — 指定通貨建 yen-premium** [S5]: the surrender deduction is
  `積立金 × 70% × 解約控除率` where `解約控除率 = 20% × (1 − 経過月数 ÷ 120)` — a **monthly**
  straight-line run-off over ten years from a 20% start, applied *after* the 70%
  low-surrender
  factor.
- The level-premium 積立利率変動型 product and the 定額 USD product both decline to state a
  numeric scale: 「経過期間などにより異なるため、一律には記載できません」. [S2] [S7]
- The 解約控除 (with the MVA) is what the FSA identifies as the drag on realized returns: in the
  run-off cohort analysis the 市場価格調整と解約控除費 component pushes down the margin that the
  積立金増加効果 and 円安 built. [R5]

### 9. 低解約返戻金 / 低解約払戻金 — the suppression factor

- **Graduated (4 steps)** [S2]: the 低解約返戻金期間 is identical to the 保険料払込期間; the
  低解約返戻金割合 multiplies the *ordinary* surrender value of a contract that carries the 特則
  (explicitly **not** the surrender value of a contract without the 特則, and **not** the
  premium paid):

      保険期間 = 保険料払込期間 (whole-life pay):        70%
      short-pay, by 残余保険料払込年数:  ≥4年 70% ; 3年 77.5% ; 2年 85% ; 1年 92.5%

  where 残余保険料払込年数 = the period from the monthly policy anniversary of the last premium
  paid to 払込満了, rounded **up** to whole years. The suppression also persists past 払込満了 if
  the last premium of the period was never paid.
- **Flat 7割** [S7]: the ordinary surrender value × 0.7 throughout the 低解約払戻期間, with the same
  "unpaid premium keeps you suppressed" rule.
- **Graded band** [S5]: 70% below 10 years, `70% + a set factor by elapsed months` from 10
  to
  under 15 years, 100% from 15 years — the 低解約返戻金期間 is 第1保険期間 only and is capped at
  15 years.
- Observed effect on premium: the same illustration point (male, 契約年齢40, 100,000米ドル, 月払,
  60歳払込満了) costs **239.60米ドル/月 without the 特則 and 225.00米ドル/月 with it** — a 6.1%
  premium reduction for the suppression. [S2]
- The 特則 can only be added at issue and cannot be surrendered on its own. [S2]

### 10. Published surrender-value scales (the single most model-checkable numbers found)

Both tables are for the same policy: 米ドル建, male, 契約年齢40歳, 主契約保険金額 100,000米ドル,
月払, 口座振替, 60歳払込満了, 保険期間終身. Surrender values are shown net of 解約控除 and include
特別積立金 (shown in parentheses at durations 10 and 20). 払込保険料累計額 is rounded **up** to
the whole US dollar, surrender values rounded **down**, 返戻率 truncated at 1 decimal place.
[S2]

**Without 低解約返戻金特則** (premium 239.60米ドル/月):

      経過  年齢  払込累計   3.00%CV  率      3.50%CV  率      4.00%CV  率
       3    43    8,626      5,557   64.4%    5,610   65.0%    5,663   65.6%
       5    45   14,376     10,822   75.2%   10,973   76.3%   11,125   77.3%
       7    47   20,127     16,332   81.1%   16,639   82.6%   16,951   84.2%
      10    50   28,752     25,082   87.2%   25,895   90.0%   26,735   92.9%
                            (特別積立金 0)     (147)            (302)
      15    55   43,128     40,128   93.0%   41,981   97.3%   43,929  101.8%
      20    60   57,504     57,329   99.6%   61,402  106.7%   65,740  114.3%
                            (特別積立金 0)     (527)          (1,120)
      30    70   57,504     69,516  120.8%   78,331  136.2%   88,196  153.3%
      40    80   57,504     81,350  141.4%   96,493  167.8%  114,308  198.7%
      50    90   57,504     90,715  157.7%  113,322  197.0%  141,257  245.6%

**With 低解約返戻金特則** (premium 225.00米ドル/月):

      経過  年齢  払込累計   3.00%CV  率      3.50%CV  率      4.00%CV  率
       3    43    8,100      3,560   43.9%    3,595   44.3%    3,629   44.8%
       5    45   13,500      7,081   52.4%    7,181   53.1%    7,282   53.9%
       7    47   18,900     10,824   57.2%   11,030   58.3%   11,240   59.4%
      10    50   27,000     16,892   62.5%   17,445   64.6%   18,016   66.7%
                            (特別積立金 0)     (139)            (286)
      15    55   40,500     27,706   68.4%   29,011   71.6%   30,384   75.0%
      20    60   54,000     53,029   98.2%   56,877  105.3%   60,983  112.9%
                            (特別積立金 0)     (521)          (1,108)
      30    70   54,000     69,516  128.7%   78,436  145.2%   88,443  163.7%
      40    80   54,000     81,350  150.6%   96,583  178.8%  114,584  212.1%
      50    90   54,000     90,715  167.9%  113,230  209.6%  141,354  261.7%

The step from 27,706 at duration 15 to 53,029 at duration 20 in the second table is the
低解約返戻金 ramp releasing at 払込満了 combined with five years of premium — a model that smooths
it is wrong. The 3.00% column is the guaranteed run; 3.50% and 4.00% are illustrative only.
[S2]

### 11. Death benefit and its relation to the account value

Three distinct designs were observed, and the choice is load-bearing:

- **基本保険金額 with a ratcheting uplift (増加死亡保険金額).** The death benefit is the sum assured
  fixed at issue **plus** the 増加死亡保険金額 in force at the claim date. The 増加死亡保険金額 is
  computed at every 月単位の契約応当日 (the 約款's 計算日; the 重要事項説明書 says 毎月1日 — the
  約款 wording governs) as:

      増加死亡保険金額 = (i) the account value at the previous day's close, computed on the
                          actually-applied 積立利率 and assuming all premiums due were paid
                        − (ii) the account value at the previous day's close needed to fund the
                          then sum assured with no future premiums, computed at the 予定利率
                          (年3.00%)

  and is not computed at all when (i) − (ii) ≤ 0. It **cannot fall below the previous
  month's
  value** — a ratchet. It exists only on the main contract, never on a 特約. Reducing the sum
  assured reduces the 積立金 and the 増加死亡保険金額 in the same proportion, and the
  増加死亡保険金額 cannot be reduced on its own. [S1] [S2]
- **max(account value, surrender value).** On the single-premium 積立利率更改型 product the death
  benefit is 「死亡日における積立金相当額または解約返戻金額のいずれか大きい金額」 — there is no
  separate sum assured above the fund, and the 基本保険金額 at issue is simply set equal to the
  一時払保険料. A 災害死亡保険金 is paid **in addition** on accidental or infectious-disease death. [S3]
- **max(保障基準価格, 解約払戻金額)**, where 保障基準価格 is a separately-tracked guaranteed floor
  that grows with the credited rate. [S8]
- 高度障害保険金 is paid at the same amount as the death benefit and terminates the contract. [S2]
- On the yen-premium 指定通貨建 shape the USD death benefit is **fixed for five years at a time**
  by the 予定利率 set at each 予定利率計算基準日, and rises only when that rate exceeds the 0.25%
  floor. [S5]

### 12. 特別積立金 (the ten-year experience top-up)

- On the level-premium 積立利率変動型 product only: after 10 and after 20 years in force, an amount
  computed from the **ten-year investment performance** is added to the 積立金. It is never
  paid on
  a contract that terminates before 10 years, and the 20-year tranche is never paid on a
  contract
  that terminates before 20 years. **If the 積立利率 has run at exactly 3.00% throughout there
  is
  no 特別積立金** — the illustration confirms this, showing (0) in the 3.00% column at both
  durations and 147 / 527 at 3.50% and 302 / 1,120 at 4.00%. There is no 特別積立金 on any 特約.
  Where the contract is converted to 払済終身保険 the 特別積立金 is retained by the insurer. [S1] [S2]

### 13. The charge stack

The charge stack **is** the product; the three carriers that disclose it do so in three
incompatible ways.

- **Three named layers, none quantified** [S1] [S2]:
  1. 保険契約の締結・維持にかかる費用 — deducted periodically **from the premium or the account
     value**; the premium net of it is what becomes 積立金.
  2. 死亡・高度障害保障などのための費用 — deducted periodically **from the account value**.
  3. 資産運用のための運営費率 + 積立金を最低保証するための保証費率 + その他費用 — deducted
     **inside the 積立利率 calculation, from the previous-but-one month's investment return**.

  Each is stated to depend on 保険金額・契約年齢・性別・経過期間 and therefore
  「一律には記載できません」. Plus 年金を管理するための費用 = **1.00% of each annuity payment**
  under the 年金支払特約 / 年金移行特約.
- **Charges named inside the crediting-rate formula and therefore observable as a spread**
  [S3]:
  災害死亡保障費率 + 新契約費率 + 維持費率, subtracted from the 基準利率-derived rate. Their sum is
  not published, but the 実質的な利回り disclosure bounds it: for the 基本タイプ the 実質的な利回り
  equals the 積立利率 exactly (4.72% = 4.72%), so no further charge sits outside the rate. [S4]
- **A single front-end percentage of the single premium, banded by issue age** [S10]:
  40–69歳 **4.50%**, 70–79歳 **3.00%**, 80–84歳 **2.00%**, 85–90歳 **2.00%**; and then
  explicitly
  「保険期間中に新たにご負担いただく費用はありません」 because the 維持費, 死亡保険金 cost and
  累積追加額 cost are already netted out of the 積立利率.
- **Split fixed/variable** [S13]: 保険契約関係費 **2.35% p.a.** on the 変額部分 plus 信託報酬
  **0.22% (税込)**, while the 定額部分's costs are again taken inside the 積立利率.
- **Distributor commission** [S13]: 契約時手数料 **4.00% or 2.60%** of the single premium for the
  FX versions and **1.85% or 0.30%** for the yen version; 継続手数料 **0.75% or 0.10% p.a.** of
  the
  account value (FX) and **0.05%** (JPY), for at most 7 years. The FSA's own reading of the
  sector
  is an **L-shaped 5.5% / 0.1%** split. [R5]

### 14. 為替手数料 — the currency spread

This is the one charge every carrier quantifies, and the observed spreads differ by a factor
of
fifty.

| Carrier / shape | 円入金 (JPY→FX) | 円支払 (FX→JPY) | Source |
|---|---|---|---|
| 積立利率変動型 平準払 (USD) | TTM **＋50銭** | TTM **−50銭** | [S1] |
| 積立利率更改型 一時払, 米国ドル | TTM **＋50銭** | TTM **−1銭** (as printed) | [S3] |
| 積立利率更改型 一時払, 豪ドル | TTM **＋50銭** | TTM **−3銭** (as printed) | [S3] |
| 指定通貨建 yen-premium (USD) | TTM **＋25銭** | TTM **−25銭** | [S5] |
| 一時払 with 円建終身移行特約 | (single premium paid in FX) | TTM **−50銭** | [S8] |
| 定額 USD 平準払 | 当社所定 (no published 銭) | 当社所定, floored at TTB | [S7] |
| 外国為替連動型 一時払 | plain TTM, **no FX fee charged** | plain TTM | [S11] |

- The reference TTM is a nominated bank's 対顧客電信仲値; where the published value changes more
  than once in a day the **first** quote of the day is used. [S1] [S3] [S5]
- The 円入金 rate is capped at TTS and the 円支払 rate floored at TTB. [S3] [S5] [S7]
- Every carrier states the spread is 将来変更される可能性があります and gives an as-at date
  (2023-10 for [S3], 2025-04 for [S1], 2026-04 for [S5]).
- The 外国為替連動型 shape avoids the spread entirely by never converting: premium and benefit are
  both in yen and the FX enters only as a **為替変動率 = FX rate at the valuation date ÷ FX rate
  at
  契約日** multiplier. Observed reference rates 2026-08-19: US$1 = ¥159.43, A$1 = ¥112.83.
  [S11]
- 円入金特約 is *mandatory* on one carrier's product (「この保険には円入金特約が付加されています」),
  making the yen-in conversion unavoidable, while 円支払特約 is optional. [S7]
- Receiving in foreign currency instead is not free either: 送金手数料 / 引出手数料 /
  リフティングチャージ apply and are the receiving bank's, not the insurer's. [S1] [S7] [S13]

### 15. 目標到達型 — the target-value conversion rider

The distinguishing feature of the single-premium FX whole life, and the one the FSA has
singled out.

- **Mechanics, carrier A** [S8]: the policyholder sets a 目標値 anywhere from **105% to 200% in
  1%
  steps**, applied to the yen-converted single premium to give a 目標額. When the
  **yen-converted
  surrender value** reaches or exceeds the 目標額, the contract converts **automatically** to a
  yen
  whole life. The policyholder may also convert on demand at any time after 契約日. After
  conversion there is no 解約控除.
- **Mechanics, carrier B** [S9]: 目標値 chosen at issue from **100% / 105% / 110%** of the
  基本保険金額; **changeable any number of times before the target is reached**, by telephone; the
  target is tested **every business day from one year after 契約日**; on a hit the insurer
  posts a
  notice within five business days and the contract converts automatically to a yen whole
  life
  whose death benefit and surrender value are then fixed in yen, after which **neither the
  FX rate
  nor the MVA affects the contract any more**. Crucially, the **test itself is made on the
  解約払戻金額, so the FX rate and the MVA are applied in deciding whether the target has been
  hit** — the trigger is not a clean function of the account value.
- **A one-year dead zone** is standard: reaching the target inside the first year does not
  trigger conversion. [S9]
- **Population-level behaviour** [R5] [R6]: at every focus-monitored distributor, most
  ターゲット型 policies are surrendered on reaching the target and the *same* product is
  immediately sold back to the *same* customer; the FSA calls this economically irrational
  for the
  customer because the front-loaded commission is charged twice. About **60% of 外貨建一時払保険
  are terminated within four years** and the **average holding period is 2.5 years** against
  a
  product designed for long holding. The FSA's fix is that the distributor should tell the
  customer, before the target is reached, that the target can be raised **free of charge**.
- The FSA's canonical definition of the class (useful for the spec's wording): 「払込保険料が顧客の
  設定した目標値（払込保険料対比の円換算額での運用の目標値。例えば105％、110〜200％（10％きざみ）で
  設定できる。）に到達した場合、自動的に円貨で運用成果を確保し、円建の終身保険等に移行する商品」. [R6]
- The exact rider name **目標到達時円建終身保険移行特約** was not confirmed against a retrieved
  document; the two retrieved carriers call theirs 円建終身移行特約 [S8] and
  目標値到達時終身保険移行特約 [S9]. See the gaps section.

### 16. 円入金特約 / 円支払特約

- 円入金特約 converts a yen payment into the operating currency at the 入金用 rate for the premium;
  保険料円入金特約（クレジットカード払用）is a separate rider for card-paid premiums. [S1] [S3] [S7]
- 円支払特約 converts benefits, surrender value, annuity payments and 契約者貸付 repayments back to
  yen at the 支払用 rate. [S1] [S3] [S7]
- The **conversion base date** matters and is published: for death, disability, surrender,
  policy loan and living-needs benefits it is the **day before** the day the completed claim
  documents reach the insurer; for a 据置金 it is the 据置期間満了日; for an annuity fund it is the
  day before the fund is set. If that day is a bank holiday for the nominated bank, the
  immediately preceding business day is used. [S7]
- On one carrier, all money movement is in the operating currency by default and the
  customer needs
  a foreign-currency-capable account unless the 円支払特約 is used; foreign-currency settlement
  is
  disclosed as slower to reach the account than yen. [S3]
- The insurer may convert to yen unilaterally where it cannot transact with the policyholder
  in
  foreign currency. [S3]
- A yen-payment window exists on some products: where the contract lapses, the USD surrender
  value
  is fixed at lapse and the customer has until the end of the following month (送金待機期間) to
  take it in USD or JPY; failing a claim, it is auto-converted at the 支払用為替レート on the day
  after the window closes and remitted. [S5]

### 17. Premium structure and payment

- **一時払** on all the 積立利率更改型 / 目標到達型 shapes. [S3] [S8] [S9] [S11] [S12] [S13]
- **平準払 (月払 / 半年払 / 年払), 口座振替 or credit card**, on the 積立利率変動型 shape, with a
  short-pay option (e.g. 60歳払込満了). [S1] [S2]
- **Level yen premium** on the 指定通貨建 shape, converted to USD each month; the customer may
  reduce (減額) the premium within the insurer's rules but may never restore it, and reducing
  it
  produces no surrender payment. [S5]
- 前納 (advance payment of premiums) is available **only at issue** on one product; while in
  前納期間 the contract cannot be reduced or made 払済. [S2]
- 高額割引 (volume discount) applies above a threshold sum assured. [S2]
- 保険料払込免除: on the level-premium product it is triggered by a **所定の身体障害の状態 arising
  within 180 days of an accident**; after waiver the surrender value progresses as if
  premiums
  were still being paid. Optional riders extend the waiver to 三大疾病 and 要介護状態. [S1] [S2]

### 18. 猶予期間, 失効, 復活, 自動振替貸付

- **払込猶予期間** [S2] [S7]:
  - 月払: from the 1st to the last day of the month **after** the 払込期月.
  - 年払 / 半年払: from the 1st of the month after the 払込期月 to the **monthly policy anniversary
    in the month after that**; where that anniversary does not exist, the last day of that month
    (契約応当日 7/31 → 9/30); with a special rule for month-end anniversaries in Feb, Jun and Nov
    (→ Apr, Aug, Jan month-ends).
  - 第1回保険料 has its own deadline (the end of the month after 責任開始) and non-payment makes
    the contract void, not lapsed. [S2] [S7]
- **自動振替貸付**: where the 猶予期間 expires unpaid and an APL is possible, the insurer
  **automatically lends the premium** and keeps the contract in force unless the
  policyholder has
  opted out in advance (the opt-out itself must be lodged before the 猶予期間満了日). Interest is
  charged at a set rate, compounded. This is why a FX whole life with a cash value does not
  lapse
  on the first missed premium. [S2]
- **失効** occurs only when the APL cannot carry the premium. A lapsed contract may still be
  surrendered for its surrender value. [S2]
- **復活**: **within 1 year** of lapse on one carrier [S2]; **within 3 years** on another
  [S7].
  Both require fresh 告知 and payment of the arrears; both may be refused on health grounds;
  on
  one, riders reinstated this way carry a **90-day 不てん補期間**. [S2]
- On the yen-premium 指定通貨建 shape there is no APL and no 復活: failure to pay inside the
  猶予期間 **terminates** the contract on the day after the 猶予期間満了日 and pays out the
  surrender value. [S5]

### 19. 免責 (exclusions) and contestability

- **自殺免責**: **3 years** from the 責任開始の日 (including a 復活 or 復旧) on two carriers
  [S2] [S7]; **2 years** on a third [S3]. Suicide while in a state of 心神喪失 may still be
  paid.
  Note the contrast with the UK/US composite's 12-month clause.
- Other death-benefit exclusions: the 契約者 or 死亡保険金受取人's 故意, and 戦争その他の変乱 (with
  the standard discretion to pay in full or reduced where the extra claims do not materially
  affect the pricing basis). 高度障害保険金 additionally excludes the insured's own 自殺行為 at any
  time. [S2]
- **Even where a death-benefit exclusion applies, the 積立金 or 解約返戻金 may still be paid** —
  this is a real cash-flow item on an account-value product and has no analogue on a pure
  protection product. [S2]
- **告知義務違反**: contestable **within 2 years** of the 責任開始日 (including 復活 and
  中途付加). Fraud in taking out or reinstating the contract voids it with **no time limit**.
  [S3] [S7]

### 20. Other contract options

- **契約者貸付** and **払済終身保険への変更** are available on the level-premium product; converting
  to 払済 triggers the 解約控除 and forfeits the 特別積立金. Reversal to the original contract
  (復旧) is available within 1 year of the 払済 conversion or the reduction. [S2]
- **減額** is treated as a partial surrender: the reduced portion's surrender value is
  computed
  under the surrender clause, the 積立金 and 増加死亡保険金額 are reduced in the same proportion,
  and the future premium is recalculated. The 増加死亡保険金額 cannot be reduced alone. [S2]
- **積立金定期引出特約**: takes a periodic withdrawal from the account value; the cost is charged by
  **lowering the 積立利率**, and the withdrawals themselves are free of both 解約控除 and 市場価格
  調整. [S3]
- **年金支払特約 / 年金移行特約 / 年金支払移行特約**: convert the death benefit or surrender value
  into an annuity. Payment terms of 5 / 10 / 15 years, 定額型 or 逓増型（5％複利）on one carrier
  [S7]; a 1.00% of each payment management charge on two [S1] [S8]; "within 1.0%, set at the
  annuity start date" on a third [S10].
- **リビング・ニーズ特約** (terminal illness, life expectancy ≤6 months) is standard. [S1]
- **三大疾病・介護給付終身保険特約 / 三大疾病・介護保険料払込免除特約** and a
  **定期保険特約（無解約返戻金型 米ドル建）** are the common FX-denominated riders. [S1]
- **介護年金支払移行特約** on one single-premium product converts the surrender value into a
  lifetime care annuity on 要介護1 or above under the public LTC scheme. [S11]
- **契約者配当 and 満期保険金 do not exist** on the 無配当 shapes; 保険金の据置支払 is not offered.
  [S2] One carrier's 指定通貨建 shape is **5年ごと配当付**. [S5]

### 21. Reserving, solvency and the 標準責任準備金 treatment

- USD and AUD contracts have been **inside the 標準責任準備金 regime since 2021-10-01**
  (the 平成13年金融庁告示第24号 changes from 2022-04-01). Contracts denominated in any other foreign
  currency are excluded from the 対象契約. [R1]
- The 標準利率 (the 予定利率 in the notification's terms) for USD/AUD is a **基準利率 computed
  monthly** as Σ (対象利率 in each band × 安全率係数), where 対象利率 is built from A-rated
  same-currency corporate bond yields at 10 and 20 years (第一号保険契約: the average of the 10y
  and
  20y yields; 第二号保険契約: the 10y alone), each taken as the **lower** of the one-month and
  three-month trailing averages ending the month before the 基準日. The 基準日 is the 1st of every
  month; a deviation of ≥0.05% from the applied 予定利率 moves it to the nearest 0.05% multiple,
  effective for contracts written from one month after the 基準日. [R1]
- 安全率係数 by band [R1]:

      対象利率 band      USD    AUD
      ≤0%                1.0    1.0
      0% – 2.0%          0.95   0.95
      2.0% – 3.0%        0.9    0.95
      3.0% – 4.0%        0.9    0.9
      4.0% – 5.0%        0.85   0.9
      5.0% – 6.0%        0.8    0.9
      >6.0%              0.75   0.8

- USD/AUD 第二号保険契約 whose 保険期間 (or, for a 予定利率変動型 contract, whose 利率保証期間) is
  **20 years or longer, or runs to death**, may instead use the 第一号 対象利率 definition. [R1]
- USD/AUD contracts that are neither 第一号 nor 第二号 sit on a slow track: three-year or ten-year
  trailing averages of the 10-year yield, a 0.5% trigger, 0.25% rounding, and application
  from
  **1 April of the following year**. [R1]
- The minimum-guarantee 保険料積立金 machinery (標準的方式 / 代替的方式, 責任準備金告示第14項第1号)
  applies with the discount rate being the 標準利率; for non-yen contracts the 代替的方式 conditions
  apply 「その特性に応じ…に準じた条件」, and the ≤10% deviation tolerance between the two methods is
  unchanged. [R2]
- 価格変動準備金 within the 責任準備金 of 外貨建て保険 must be scoped from the asset classes matching
  the 外貨建て保険 product segment on a segregated-accounting basis, and the 危険準備金Ⅱ for those
  contracts must use the **外貨建て保険 risk coefficient**. [R4]
- Reserving is **cited, not reproduced** in this library; the model projects gross cash
  flows.

### 22. Conduct layer — the reason this product is unusual

- **Complaints.** Bank-channel 外貨建保険 complaints rose from **597 (2012) to 2,543 (2018)**,
  with
  2019 H1 at 1,352 (annualized 2,704); the complaint rate against in-force count fell from
  0.14%
  to 0.08% over the same window. **68% were 説明不十分**; inside that, 元本割れリスク 37%,
  適合性の確認 14%, 預金誤認 8%, 高齢者対応 6%, その他 28%. [R7]
- **The sales licence.** The 生命保険協会 created the **外貨建保険販売資格試験** as an industry-common
  examination, with the industry-common textbook from ~April 2020, the **examination from
  October
  2020**, and a **販売資格者登録制 (licence register) from around April 2022** — after which an
  unqualified 募集人 cannot sell 外貨建保険. Seven-module curriculum; registration requires the
  専門課程試験 plus the common curriculum, mirroring the 変額保険販売資格. [R7]
- **Disclosure.** The 監督指針 adds product-specific 契約概要 items for 外貨建て保険 (yen-converted
  shortfall risk; the fees that arise specifically from contracting in foreign currency) and
  for
  **MVA products** (the mechanism, the loss risk on early surrender, **an illustration of
  the
  deduction ratio against the 保険料積立金**, and the in-force charges). It also requires, on
  non-corporate 外貨建て保険 sales, a **signed acknowledgement of FX risk** from the policyholder.
  [R3]
- **実質的な利回り.** For 外貨建一時払 終身・養老・年金, the 設計書 must print the 実質的な利回り
  alongside the 積立利率 / 予定利率, defined as the annualized compound yield that discounts the
  future account or surrender value back to the premium — measured **at the point where the
  MVA,
  the rate-variation period and the surrender charge have all run off**. [R8] Carriers
  publish it
  next to the declared rate. [S4]
- **Supervisory findings.** ~60% surrendered within four years, average holding 2.5 years,
  systematic target-hit-and-rebuy churn, L-shaped commission (5.5% year 1 / 0.1% after),
  ~20% of
  sampled customers showing suitability concerns (just under 30% among complainants), and
  the
  MVA + 解約控除 identified as the drag on realized returns. [R5] [R6]
- The FSA's earlier framing had already required the sales material to be comparable with an
  investment-trust 目論見書. [R9]

### 23. Policyholder protection and tax

- **保護機構**: 90% of the 責任準備金等 at the failure date for 補償対象契約 (less for 高予定利率
  契約), and 90% of the previous sum insured for claims during the business suspension. No
  special
  carve-out for 外貨建 contracts. [R10]
- **Tax** [R11] [S13]:
  - Premiums: a 外貨建 whole life premium (including a single premium) counts toward the
    一般生命保険料控除 basket.
  - Death benefit: 相続税 where 契約者 = 被保険者 (with the 500万円 × 法定相続人 exemption where the
    beneficiary is an heir [S11]).
  - Surrender / maturity proceeds taken as a lump sum by the premium payer: **一時所得**,
    = proceeds − (premiums paid − 剰余金) − ¥500,000 special deduction, of which **half** is taxable.
    An employee with ≤¥20m employment income files only if the halved amount exceeds ¥200,000.
  - The proceeds and the premiums are both translated to yen for this computation, so the FX
  gain
    is folded into the 一時所得 rather than taxed separately — but see the gaps section: the NTA
    page does not say so explicitly.
  - Not eligible for NISA or iDeCo. [S13]

---

## Variation across carriers

The observed range on every parameter a modeller has to choose. Carrier identity is by [S#]
tag.

| Feature | Observed values | Range / note |
|---|---|---|
| Crediting-rate declaration | monthly, applied from the monthly policy anniversary [S2]; twice monthly for new business, then fixed for 1/10/15/20 years [S3] [S4] [S14]; monthly for 第1保険期間 then every 5 years [S5] [S6]; at 契約日 then at each 更改日 [S11] | monthly ↔ 30-year lock |
| 積立利率適用期間 / 保証期間 | 1, 3, 10, 15, 20, 30 years [S3] [S8] [S12] [S14] | shortens with attained age (91+ → 1 year [S3]; 81+ → 3 years [S8]) |
| 最低保証積立利率 | **0.01%** [S3], **0.25%** [S5] [S6], **3.00%** [S1] [S2] | 0.01%–3.00%; the high floor belongs to a 2002-generation level-premium contract |
| Index driving the rate | A-rated USD corporate index 10y/20y; AUD 10y govvies [S3]; average of 6-month and 5-year UST [S6]; 米国債 for the cap [S3] | corporate ↔ sovereign, 0.5y ↔ 20y |
| Rate cap | (米国債利回り平均 + 2.0%) − charges, USD 15/20-year only [S3] | only one carrier publishes a cap |
| Rate band | 基準利率 ±1.5%, insurer's discretion inside it [S3] | discretionary band is itself a product fact |
| 市場価格調整 | present on all single-premium 更改型 shapes [S3] [S8] [S12] [S13]; **absent** on monthly-declared level-premium [S2] and on the yen-premium 指定通貨建 shape [S5] | presence is a shape property, not a carrier preference |
| MVA disclosure | full rate table by year × Δ [S3]; the 市場価格調整用利率 itself, fortnightly, by currency and period [S12]; narrative only [S8] [S13] | one carrier publishes enough to reproduce the adjustment |
| 解約控除 run-off | 7.0%→0.7% straight-line over 10y [S3]; 10%→0% and 5%→0% (two vintages) [S8]; 6.5%→0.0% FX / 3.5%→0.1% JPY [S13]; 20%×(1−m/120) monthly [S5]; undisclosed [S2] [S7] | 3.5%–20% at outset, always to zero at 10 years |
| 解約控除 base | 積立金 [S3] [S5]; 責任準備金 [S7]; **基本保険金額** [S13] | the base differs — a 6.5% charge on the sum assured is not a 6.5% charge on the fund |
| 解約控除 window | shorter of 払込期間 and 10 years [S1] [S2] [S7]; flat 10 years from 契約日 [S3] [S8] | |
| 低解約返戻金割合 | flat **70%** [S7]; **70 / 77.5 / 85 / 92.5%** by remaining premium years [S2]; **70% → graded → 100%** at 10/15 years [S5] | 70% is universal at the bottom; the release is a cliff, a 4-step ramp or a monthly grade |
| Premium saved by the 特則 | 225.00 vs 239.60 USD/month = **6.1%** [S2] | one observation |
| Death benefit | 基本保険金額 + ratcheting 増加死亡保険金額 [S1] [S2]; **max(積立金, 解約返戻金)** [S3]; max(保障基準価格, 解約払戻金) [S8]; 5-year-fixed USD amount reset with the 予定利率 [S5] | uplift ↔ no uplift is the sharpest design fork |
| Accidental-death add-on | 災害死亡保険金 paid in addition [S3]; not present [S2] | |
| Experience top-up | 特別積立金 at 10 and 20 years, zero if the rate ran at the floor [S1] [S2] | one carrier only |
| 為替手数料 in | TTM+50銭 [S1] [S3]; TTM+25銭 [S5]; 当社所定 [S7]; none [S11] | 0–50銭 per US$ |
| 為替手数料 out | TTM−50銭 [S1] [S8]; TTM−25銭 [S5]; TTM−1銭 (USD) / −3銭 (AUD) as printed [S3]; 当社所定 ≥TTB [S7]; none [S11] | 0–50銭; one carrier is near-symmetric-free on the way out |
| Front-end charge | 4.50/3.00/2.00/2.00% of single premium by age band [S10]; not separately disclosed [S1] [S2] [S3] | published ↔ folded into the rate |
| In-force charge | 2.35% p.a. on the 変額部分 [S13]; three named layers, unquantified [S1] [S2]; none outside the rate [S10] | |
| Annuity management charge | 1.00% of each payment [S1] [S8]; "within 1.0%, fixed at annuity start" [S10] | |
| 目標値 | 105–200% in 1% steps [S8]; 100/105/110% [S9]; 105%, 110–200% in 10% steps [R6] | 1% ↔ 10% granularity |
| Target test frequency | every business day, from 1 year after 契約日 [S9]; continuous from 契約日 with a 1-year block on the conversion [S8] | |
| Target changeable | any number of times before the hit, free [S9]; the FSA says raising it should be free and offered [R5] | |
| 自殺免責 | **3 years** [S2] [S7]; **2 years** [S3] | 2–3 years (vs 12 months in the UK composite) |
| 復活 window | **1 year** [S2]; **3 years** [S7]; **no reinstatement at all** [S5] | |
| 自動振替貸付 | present, opt-out [S2] [S7]; absent [S5] | governs whether a missed premium lapses |
| 猶予期間 | 月払: to the end of the following month; 年払/半年払: to the monthly anniversary two months on [S2] [S7] | uniform |
| Currencies | USD + AUD [S3] [S11] [S14]; USD + AUD + EUR [S8]; USD + AUD + **JPY** in one chassis [S12]; USD only [S1] [S5] [S7] | |
| Issue ages | 6–80 [S1]; 0–75 [S5]; 0–87 [S8]; 0–90 [S4]; 40–90 [S10] | |
| Premium mode | 一時払 [S3] [S8] [S9] [S12]; 月/半年/年払 by 口座振替 or card [S1]; level **yen** amount [S5] | |

**What does not vary.** Every retrieved product: is 終身 (whole-of-life); carries a 解約控除 that
runs to zero at exactly ten years; treats a 減額 as a partial surrender; offers 円入金特約 and/or
円支払特約 with the reference rate being a nominated bank's TTM and the first published quote of
the day; is a 特定保険契約 requiring a 契約締結前交付書面 and a signed FX-risk acknowledgement; and
warns that a loss can arise **even with no FX movement at all**, purely from the currency
spread.
Every carrier declines to publish the mortality-and-expense charge in currency terms, giving
only
「契約年齢・性別・経過期間などにより異なるため一律には記載できません」.

---

## Fetch failures and gaps

### URLs that could not be retrieved

- **All manulife.co.jp URLs — HTTP 403** [S15]. The product page, the published 積立利率 history
  for
  こだわり外貨終身, the rate index page and the 通貨選択型一時払終身保険 約款 PDF each returned 403
  to WebFetch and to curl, with and without a browser User-Agent, with a Referer and a
  cookie jar,
  and over forced HTTP/1.1. This is a WAF policy, not a User-Agent check, and the usual
  browser-UA workaround does not defeat it. **No fact in this file is sourced to Manulife.**
  What
  was lost: a second published monthly-declared 積立利率 series (partially compensated by
  [S14]'s
  fortnightly 基準利率 series and [S4]'s fortnightly 積立利率 series), and the verbatim wording of a
  rider actually named 目標到達時円建終身保険移行特約.
- **https://www.metlife.co.jp/lf1/ahp405/08.html — retrieved 200 but empty** [S16]. React SPA
  shell; no rate content in the served HTML. What was lost: the declared 積立利率 history for
  the
  monthly-declared product. The guaranteed floor (3.00%) and the illustration rates (3.00 /
  3.50 /
  4.00%) in [S1] [S2] are the only crediting-rate figures available for that product.
- **https://www.seiho.or.jp/info/news/2020/20200221.html — body JS-rendered.** The release text is
  not in the served HTML; the substance was recovered from the linked PDF at
  `/info/news/2019/pdf/20200221.pdf`, which is what [R7] cites. Nothing was lost.
- The Gibraltar booklet's PDF text layer defeated both WebFetch's extractor and `pdftotext`
  (poppler's Adobe-Japan1 CMaps are absent from this environment). The file was re-extracted
  locally with PyMuPDF; the extraction is clean and was cross-checked block-by-block for the
  FX-rate table. No content was lost, but any figure quoted from [S3] rests on that local
  extraction rather than on a rendered page.

### Claims left [unverified], and why

- **The rider name 目標到達時円建終身保険移行特約.** The brief names this rider explicitly and search
  results attribute it to Manulife's 通貨選択型一時払終身保険 and 通貨選択型変額終身保険, but the
  only carrier documents retrieved use **円建終身移行特約** [S8] and **目標値到達時終身保険移行特約**
  [S9]. The mechanic is fully verified from [S8] [S9] [R6]; **the exact rider name
  「目標到達時円建終身保険移行特約」 is [unverified]** and the drafting pass should either use a
  neutral description or cite the two verified names.
- **Whether the target-value rider requires a companion 定期支払特約.** One carrier's page says
  the
  rider requires 定期支払特約 at issue and cannot be added mid-term [S9]; whether that is general
  is
  [unverified].
- **The Gibraltar 円支払特約 spread of TTM−1銭 (USD) / TTM−3銭 (AUD)** [S3]. This is what the
  booklet's table prints and the block extraction is unambiguous (cell text
  `米国ドル\nTTM＋50銭\nTTM－1銭`), but a 1-sen payout spread against a 50-sen inbound spread is
  far outside the range every other carrier publishes. Reported verbatim; **treat the
  asymmetry as
  [unverified] until a rendered page confirms it**, and do not use it as the basis of a
  `[std]`
  spread.
- **Minimum single premium.** No retrieved document publishes one for any 一時払 product. The
  平準払 product's 最低保険金額 of 3万米ドル [S1] is the only published minimum found.
- **The mortality-and-expense charge in currency or per-mille terms.** Every carrier refuses
  to
  quantify it. Any `[std]` charge basis in the reference implementation must be constructed
  and
  labelled as such; the only quantitative handles are the front-end 4.50%/3.00%/2.00% age
  bands
  [S10], the 2.35% p.a. 保険契約関係費 on a variable sleeve [S13], and the fact that on one product
  the 実質的な利回り equals the 積立利率 exactly, bounding the outside-the-rate charge at zero [S4].
- **The closed-form MVA formula.** Not published by any carrier. The [S3] table is the only
  reproducible artefact; the disclosure regime requires an illustration, not a formula [R3].
  Any
  algebraic MVA in the model is a `[std]` reconstruction.
- **The 増加死亡保険金額 ratchet.** The ratchet
  (「前月に計算された増加死亡保険金額を下回ることはありません」) appears in the ご契約のしおり
  section of [S2] but not in the 約款 第46条 text as extracted. The computation formula in 第46条
  is verified; the **ratchet is sourced to the しおり only** and the apparent 約款 silence should
  be
  re-checked against a rendered page before it is asserted as a contract term.
- **The 計算日 discrepancy.** The 重要事項説明書 says the 増加死亡保険金額 is computed 毎月1日; the
  約款 第46条 says 月単位の契約応当日. Both are in [S2]. The 約款 governs, but the discrepancy is
  real and should be surfaced in the technical notes rather than silently resolved.
- **為替差益 taxation on a foreign-currency policy.** [R11] establishes the 一時所得 computation
  and [S13] confirms 解約返還金 − 一時払保険料 is taxed as 一時所得 + 住民税, but **no retrieved NTA
  page addresses the FX gain component separately**. The common statement that the FX gain
  is
  absorbed into the 一時所得 rather than taxed as a separate 雑所得 is **[unverified]** here.
- **The current 標準利率 value for USD and AUD contracts.** [R1] gives the complete derivation
  and
  the monthly reset mechanism, but the FSA does not publish the resulting rate on a page
  that was
  retrieved. The carrier-published 基準利率 / 市場価格調整用利率 series [S12] [S14] and the
  Gibraltar 基準利率 disclosure [S4] are proxies for the level, **not** the statutory 標準利率.
- **標準生命表2018 applicability to 外貨建 contracts.** Not addressed by any retrieved document in
  this session. The 2021 amendment [R1] changes the interest basis for USD/AUD contracts;
  whether
  and how the mortality basis differs is **[unverified]** here and belongs to the
  cross-product
  reference library.
- **ESR (経済価値ベースのソルベンシー規制) treatment of FX contracts.** Out of scope of everything
  retrieved this session; **[unverified]**.
- **Complaint counts after 2019.** [R7] carries the series only to 2019 H1. The later FSA
  reports
  [R5] [R6] give qualitative complaint findings and the 287-customer-card analysis but no
  updated
  count. A post-2019 complaint series is **not established** here.
- **New-business volume and market size for 外貨建終身保険 specifically.** [R6] shows 販売額 and
  残高 trend directions by distributor channel for 外貨建一時払保険 as a class, but no absolute
  figure for FX whole life was retrieved. **[unverified]**.
- **Carriers not fetched.** 日本生命, 住友生命, ソニー生命, 大樹生命, 太陽生命, 東京海上日動あんしん
  生命 and 三井住友海上プライマリー生命's *current* 三井住友プライマリー終身保険 were identified in
  search results but not fetched; the eight carriers covered ([S1]–[S14], excluding the two
  failed
  entries) already span all four product shapes with policy-conditions-grade documents for
  three
  of them, which was judged sufficient. Adding a ninth would mainly tighten the variation
  ranges.
