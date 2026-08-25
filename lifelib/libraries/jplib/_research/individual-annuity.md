# 個人年金保険 (fixed individual deferred annuity) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese fixed individual deferred annuity (定額個人年金保険,
*teigaku kojin nenkin hoken*) liability cash flow reference model — a deferral phase that
accumulates to a 年金原資 (*nenkin genshi*, annuity fund) and a payout phase written as
確定年金 (*kakutei nenkin*, annuity-certain) or 保証期間付終身年金 (*hoshō-kikan-tsuki
shūshin nenkin*, life annuity with a guarantee period) — together with the 税制適格特約
(*zeisei tekikaku tokuyaku*, tax-qualification rider) that shapes the whole design.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(product-specific regulatory/actuarial reference) pointing at a document actually retrieved
and read during this session, or is tagged [unverified] where it is general knowledge or a
search snippet that could not be confirmed against a retrieved document. Access date for all
fetched sources: 2026-08-20.

---

## Primary sources

### S1 — 第一生命, 「個人年金保険料税制適格特約条項（Ｓ60）」 (rider policy conditions)
- Publisher: 第一生命保険株式会社 (Dai-ichi Life)
- Document: 個人年金保険料税制適格特約条項（Ｓ60）, 平成22年４月２日改正; extracted booklet
  pages 27–29 (3 pp. PDF)
- Doc type: 特約条項 (rider policy conditions), verbatim contract wording
- URL: https://event.dai-ichi-life.co.jp/yakkan/15_2014_01_1/pdf/15_10343_027.pdf
- Retrieved: YES (full PDF downloaded, 3 pp., text extracted and read in full)
- Key content: the four attachment conditions of the tax-qualification rider verbatim;
  the special handling it forces on dividends, refunds, prepaid premium balances, policy
  loans, contract changes and paid-up conversion; the deemed-termination triggers; the rule
  that the rider cannot be surrendered on its own.

### S2 — 第一生命, 「個人年金保険（2018）ご契約のしおり－約款」 (booklet: policy summary + policy conditions)
- Publisher: 第一生命保険株式会社
- Document: ご契約のしおり－約款, 第4分冊, 2022年7月版; contains 個人年金保険（2018）
  普通保険約款 (2021年9月17日改正), 個人年金保険料税制適格特約（Ｓ60）, 指定代理請求特約
  (2022年7月2日改正) and the 未払年金の現価 factor table (112 pp.)
- Doc type: ご契約のしおり・約款 (policy summary bound with policy conditions)
- URL: https://dl-shiori.jp/shiori/no04/2207/04.pdf
- Retrieved: YES (full PDF downloaded, 112 pp., text extracted; product, tax-rider,
  policy-conditions and 未払年金の現価 sections read)
- Key content: the annuity is a 確定年金 with 5/10/15-year payment periods fixed at issue;
  death benefit during deferral = monthly premium × elapsed months; surrender value capped
  at the death benefit; automatic deferral of annuity instalments with interest; commutation
  (年金の一括払) at the present value of unpaid instalments; continuation option on death
  during payout; a published table of commutation factors; three-year suicide exclusion;
  three-year reinstatement window; no automatic premium loan on this product.

### S3 — 第一生命, ニュースリリース 「“長生き”のための新しい個人年金保険 とんちん年金『ながいき物語』の発売について」
- Publisher: 第一生命保険株式会社
- Document: news release dated 2017年3月16日, registration code (登)C16P0565(2017.3.6)⑤,
  4 pp.
- Doc type: product news release (product outline, parameter table, specimen premiums)
- URL: https://www.dai-ichi-life.co.jp/company/news/pdf/2016_090.pdf
- Retrieved: YES (full PDF downloaded, 4 pp., text extracted and read in full)
- Key content: the full issue envelope of a tontine annuity (契約年齢 50–80,
  年金支払開始年齢 60–90, 保険料払込期間 5–30 years, すえ置期間 ≤ 15 years,
  contract-to-annuitisation ≤ 30 years); death refund fixed at 70% of cumulative premiums;
  surrender refund capped at the death refund; four annuity types; specimen premiums and 返還率
  for both sexes; and — uniquely — the same insurer's ordinary annuity shown side by side on
  an identical model point, which isolates the tontine effect.

### S4 — 三井住友海上あいおい生命, 「個人年金保険（5年ごと利差配当付・無選択加入特則付加）契約概要／注意喚起情報・ご契約のしおり・約款」
- Publisher: 三井住友海上あいおい生命保険株式会社 (Mitsui Sumitomo Aioi Life)
- Document: booklet, document codes 【MS】B2193 【AD】92-193, 2017.09.01（改・一）,
  registration 登A（2018.4.2）, 140 pp.
- Doc type: ご契約のしおり・約款 bound with 契約概要／注意喚起情報
- URL: https://www.msa-life.co.jp/customer/msa/yakkan/2018-0420.pdf
- Retrieved: YES (full PDF downloaded, 140 pp., text extracted; the front-matter pages use
  a subset font that does not extract, but the whole body — product mechanics, tax rider,
  premium payment, grace, reinstatement, loans, dividends, tax treatment — extracted cleanly
  and was read)
- Key content: the two annuity types offered (確定年金 and 保証期間付終身年金（定額型）);
  death benefit = monthly premium × elapsed months; surrender value limited by the death
  benefit; the insurer's own statement of the statutory tax-qualification conditions split
  into 所得税法 and 所得税法施行令 limbs; grace-period table by premium mode; automatic
  premium loan with an 8% p.a. cap; policy loans; 5-year dividend cycle; the full
  生命保険料控除 tables for income tax and residence tax; annuity/death-benefit taxation
  matrix; 年金内容変更制度 (annuity-type election and split election at annuitisation).

### S5 — 住友生命, ニュースリリース 「平準払個人年金保険の保険料率の改定について」
- Publisher: 住友生命保険相互会社 (Sumitomo Life)
- Document: news release dated 2025年7月22日, 2 pp.
- Doc type: pricing-basis news release
- URL: https://www.sumitomolife.co.jp/about/newsrelease/pdf/2025/250722a.pdf
  (302-redirects to https://www.sumitomolife.co.jp/news/news_file/file/250722a.pdf)
- Retrieved: YES (full PDF downloaded, 2 pp., text extracted and read in full)
- Key content: **published 予定利率 values** for a level-premium individual annuity, split by
  years to annuitisation, before and after the October 2025 revision, plus the separate
  post-annuitisation 予定利率; the effective date rule keyed to 契約日; and specimen monthly
  premiums and 年金受取率 by issue age and sex on a stated model point.

### S6 — 住友生命, 商品ページ 「たのしみワンダフル」 (individual annuity product page)
- Publisher: 住友生命保険相互会社
- Document: product page for 5年ごと利差配当付生存保障重視型個人年金保険(14)
  「たのしみワンダフル」 (bank-channel name 「たのしみ未来」), figures stated as at
  2025年10月現在
- Doc type: product page (consumer)
- URL: https://www.sumitomolife.co.jp/lineup/select/shouhin/tanowan/
  (redirects to https://www.sumitomolife.co.jp/lineup/shouhin/detail/tanowan.html)
- Retrieved: YES (fetched twice — once through a browser-UA HTML fetch and once through the
  markdown converter, to cross-check the parameter strings)
- Key content: 契約年齢 0–75; the 据置期間 lever ("setting a deferral period between the end
  of premium payment and the start of the annuity increases the annuity"); the たのしみランク
  premium discount threshold; death cover during premium payment suppressed to cumulative
  premiums paid; a full specimen table by issue age and sex giving 払込保険料総額, 年金原資,
  一括受取率, 基本年金額, 年金受取総額 and 年金受取率; the tax-qualification conditions.

### S7 — 住友生命, 「契約概要／注意喚起情報 兼 商品パンフレット（たのしみ未来 ほか）」
- Publisher: 住友生命保険相互会社
- Document: 契約概要／注意喚起情報 兼 商品パンフレット, 14 pp.
- Doc type: 契約締結前交付書面 (pre-contract disclosure) bound with the product pamphlet
- URL: https://www.sumitomolife.co.jp/lineup/select/other/fi/t_mirai_shinkin/ta3.pdf
  (resolves to https://www.sumitomolife.co.jp/lineup/pdf/other/fi/t_mirai_shinkin/ta3.pdf)
- Retrieved: **NO (partial)** — the PDF downloaded cleanly (HTTP 200, 1.28 MB, 14 pp.) but
  is typeset entirely in subset CID fonts with no ToUnicode map; both `pypdf` extraction and
  the markdown-converting fetcher returned mojibake. Only isolated numerals survived. **No
  fact in this file is sourced to S7.** The same insurer's page [S6] and news release [S5]
  were used instead.

### S8 — 日本生命, ニュースリリース 「保険料率等の改定について」
- Publisher: 日本生命保険相互会社 (Nippon Life / Nissay)
- Document: news release dated 2024年11月21日, 4 pp.
- Doc type: pricing-basis news release
- URL: https://www.nissay.co.jp/news/2024/pdf/20241121b.pdf
- Retrieved: YES (full PDF downloaded, 4 pp., text extracted and read in full)
- Key content: **published 予定利率 before and after** for 年金保険 and for
  長寿生存保険（低解約払戻金型） (the tontine), described as the first increase in about
  40 years; the parallel **契約貸付利率** revision; effective date keyed to 契約日; specimen
  monthly premiums for a 10年確定年金 at two issue ages and for the tontine, by sex.

### S9 — 日本生命, 商品ページ 「ニッセイ みらいのカタチ 年金保険」
- Publisher: 日本生命保険相互会社
- Document: product page, tax statements dated 2026年4月現在
- Doc type: product page (consumer)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/nenkin/
- Retrieved: YES (browser-UA HTML fetch, text extracted and read)
- Key content: 契約年齢 range and the narrower online-channel range; the menu of annuity types
  selectable **at issue** versus **at annuitisation**; the 10年保証期間付終身年金 rider and the
  fact that its annuity amount is set on the basis in force at annuitisation, not at issue;
  deferral of the first annuity payment date by up to five years; the four
  tax-qualification conditions as the insurer states them; a 保険料払込免除特約 covering the
  three major diseases.

### S10 — 日本生命, 商品ページ 「ニッセイ 長寿生存保険（低解約払戻金型）【Gran Age グランエイジ】」
- Publisher: 日本生命保険相互会社
- Document: product page, tax statements dated 2026年3月現在 / 2026年4月現在
- Doc type: product page (consumer)
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/choju/
- Retrieved: YES (browser-UA HTML fetch, text extracted and read)
- Key content: a second tontine design, from a different carrier than [S3]:
  sex-differentiated issue-age range; **no death cover at all** during deferral (the death
  payment equals the surrender value); the suppression ratio stated as a percentage; the two
  annuity types; the explicit warning that a life annuity with a short guarantee can return
  less than premiums paid; specimen premiums and cumulative premiums by issue age and sex.

### S11 — 日本生命, 「主な諸利率一覧（2012年４月２日以降販売商品）」
- Publisher: 日本生命保険相互会社
- Document: rate schedule PDF, rates stated as at 2026年4月2日, 5 pp.
- Doc type: policyholder rate disclosure
- URL: https://www.nissay.co.jp/keiyaku/oshirase/riyoritsu/pdf/riyoritu.pdf
- Retrieved: YES (full PDF downloaded, 5 pp., text extracted and read)
- Key content: the **contract-loan rate by issue-date cohort** back to 2012;
  the prepaid-premium discount and accumulation rates; the dividend accumulation rate; the
  deferral (据置) rate for benefits left with the insurer; and — directly relevant here — the
  accumulation rate applied to *refunds arising on a tax-qualified annuity*
  (税制適格型年金保険の払戻金等の積立利率), together with the lump-payment discount tables.

### S12 — 明治安田生命, 商品ページ 「明治安田の長期運用年金」
- Publisher: 明治安田生命保険相互会社 (Meiji Yasuda Life)
- Document: product page for a 予定利率更新型 individual annuity, minimum-guarantee rate
  stated as at 2026年6月時点
- Doc type: product page (consumer)
- URL: https://www.meijiyasuda.co.jp/find3/shisankeisei/list/unyounenkin/
- Retrieved: YES (browser-UA HTML fetch, text extracted and read)
- Key content: a **rate-resetting** fixed annuity — a design absent from the other four
  carriers: the 予定利率 is refreshed once, at a stated policy duration, subject to a
  minimum-guarantee 予定利率 fixed at issue; the illustration's payout-phase rate assumptions
  in the up and down scenarios; a 金利キャッチアップ配当 that pays when new-business rates
  rise; a stated duration after which the surrender value exceeds cumulative premiums; and
  the statement that without the tax-qualification rider the premium falls in the *general*
  deduction basket instead.

### S13 — 明治安田生命, 「円貨建一時払商品に適用される予定利率」
- Publisher: 明治安田生命保険相互会社
- Document: declared-rate page, rate window 2026年8月16日～2026年8月31日
- Doc type: declared-rate disclosure
- URL: https://www.meijiyasuda.co.jp/norapl/find/rate/yencommon/planned_interest_rate/
- Retrieved: YES (browser-UA HTML fetch, text extracted and read)
- Key content: how a **single-premium** yen product's 予定利率 is set and reset — twice a
  month for new business, then at stated 予定利率計算基準日 intervals, floored by a
  minimum-guarantee 予定利率, and pegged to named JGB benchmark yields chosen by the insured's
  age. **Scope caution: the products priced on this page are 一時払養老 and 一時払終身, not
  一時払個人年金**; it is cited only for the rate-setting mechanism, never for annuity
  parameters.

### S14 — 東京海上日動あんしん生命, 「個人年金保険（5年ごと利差配当付・無選択加入特則付加）契約概要／注意喚起情報・ご契約のしおり・約款」
- Publisher: 東京海上日動あんしん生命保険株式会社 (Tokio Marine & Nichido Life)
- Document: booklet, 2014.11改定, file A9902141102, 76 pp.
- Doc type: ご契約のしおり・約款 bound with 契約概要／注意喚起情報
- URL: https://www7.tmn-anshin.co.jp/yakkan/pdf/A9902141102.pdf
- Retrieved: **NO (partial)** — the PDF downloaded cleanly (HTTP 200, 10.8 MB, 76 pp.) but
  is set in subset CID fonts without a ToUnicode map; extraction produced mojibake across
  every page. **No fact in this file is sourced to S14.** It is recorded to document that a
  sixth carrier was attempted.

### S15 — かんぽ生命, 「定期年金保険 ご契約のしおり・約款 2016.04版」
- Publisher: 株式会社かんぽ生命保険 (Japan Post Insurance)
- Document: 約款 分冊1 of the 2016.04 edition (a back-number product), 10 pp.
- Doc type: 約款 (policy conditions)
- URL:
  https://www.jp-life.japanpost.jp/products/clause/pdf/teiki-nenkin/201604/nenkin_2016_04_yakkan_1.pdf
  (index at https://www.jp-life.japanpost.jp/products/clause/teiki-nenkin/index.html)
- Retrieved: **NO (partial)** — the PDF downloaded cleanly (HTTP 200, 10 pp.) but is set in
  subset CID fonts without a ToUnicode map; extraction produced mojibake. **No fact in this
  file is sourced to S15.** Recorded to document that a seventh carrier was attempted.

---

## Regulatory and actuarial references

### R1 — 日本アクチュアリー会, 「標準生命表2018」 (公開ページ)
- Publisher: 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan, IAJ)
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Retrieved: YES (browser-UA HTML fetch)
- Content: IAJ is the 指定法人 under 保険業法第122条の2第1項 and is commissioned by the FSA
  under 第122条の2第2項第3号 to prepare the 標準生命表; the 2018 revision was published
  2017年10月17日, board-resolved 2017年5月10日, submitted to the FSA Commissioner
  2017年5月11日, and **applied from April 2018** after the FSA amended its notification.
  The page links exactly three PDFs: the tables, the 作成概要 and the 作成過程.

### R2 — 日本アクチュアリー会, 「標準生命表２０１８」 (the tables themselves)
- Publisher: 日本アクチュアリー会
- Document: 標準生命表２０１８, 5 pp. PDF (cover + four tables)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Retrieved: YES (full PDF downloaded, 5 pp., text extracted; the ℓx / dx / qx / e°x columns
  extract cleanly as text and are machine-readable)
- Content: the file contains **exactly four tables** —
  生保標準生命表２０１８（死亡保険用）男 and 女, and 第三分野標準生命表２０１８ 男 and 女.
  **There is no 年金開始後用 (post-annuitisation) table in the 2018 revision.**

### R3 — 日本アクチュアリー会, 「標準生命表（Excel形式）」
- Publisher: 日本アクチュアリー会
- Document: seimeihyo960718.xlsx — one sheet, 130 age rows, 16 columns
- URL: https://www.actuaries.jp/lib/standard-life-table/xlsx/seimeihyo960718.xlsx
  (linked from https://www.actuaries.jp/lib/standard-life-table/)
- Retrieved: YES (downloaded and parsed with `openpyxl`; qx values read directly)
- Content: qx for 生保標準生命表2018（死亡保険用）男/女, 第三分野標準生命表2018 男/女,
  生保標準生命表2007（死亡保険用）男/女, **生保標準生命表2007（年金開始後用）男/女**,
  第三分野標準生命表2007 男/女, 生保標準生命表1996（死亡保険用）男/女 and
  生保標準生命表1996（年金開始後用）男/女. This is the **publicly readable and
  machine-readable** source of the annuity valuation mortality basis.
  **Correction, 2026-08-20 (naming and citation review):** an earlier revision of this
  entry called the workbook "**redistributable**". It is **not**. The 日本アクチュアリー会
  site terms prohibit reproduction, alteration and transmission to third parties without
  prior written consent, so the file may be downloaded and read and its individual rates
  quoted with attribution, but no copy of it may be shipped. `mort_table.csv` and
  `mort_anchor_table.csv` are therefore **[std]** constructions whose `provenance` columns
  point at this entry — never copies of the IAJ file. Readable is not redistributable.

### R4 — 日本アクチュアリー会, ニュース 「標準生命表の水準の妥当性について」
- Publisher: 日本アクチュアリー会
- Document: news item dated 2025年12月18日
- URL: https://www.actuaries.jp/info/20251218.html
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the annual adequacy confirmation. For FY2026 the IAJ confirms continued
  application of 生保標準生命表2018（死亡保険用）for death cover, 第三分野標準生命表2018 for third-sector
  cover, and **生保標準生命表2007（年金開始後用）for post-annuitisation cover**, each with
  the reasoning (experience mortality below the table; national life-table expectation of
  life below the table's).

### R5 — e-Gov 法令検索, 保険業法施行規則 第68条（標準責任準備金の対象契約）
- Publisher: デジタル庁 e-Gov 法令検索 (保険業法施行規則, 平成8年大蔵省令第5号)
- URL: https://laws.e-gov.go.jp/law/408M50000040005
  (retrieved via the e-Gov API: https://laws.e-gov.go.jp/api/2/law_data/408M50000040005)
- Retrieved: YES (law data pulled as JSON through the e-Gov API v2 and Article 68 extracted;
  the HTML view is JS-rendered and was not used)
- Content: which contracts fall inside the 標準責任準備金 regime. Excluded are contracts whose
  reserve varies with the value of assets in a 特別勘定 (i.e. variable annuities), contracts
  that do not set up a 保険料積立金 or 払戻積立金, contracts whose 約款 lets the insurer change
  the 予定利率 or the reserve/premium basis — with a carve-out for contracts whose 約款
  guarantees a floor at or above the 標準利率 applicable at issue — and any other contract the
  FSA Commissioner designates.

### R6 — 金融庁, 「『標準責任準備金制度にかかる告示の一部改正（案）』等に対するパブリックコメントの結果等の公表について」
- Publisher: 金融庁 (Financial Services Agency)
- Document: 令和3年6月30日 publication
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/20210630.html
- Retrieved: YES (browser-UA HTML fetch)
- Content: the notifications amended are 平成8年大蔵省告示第48号 and 平成13年金融庁告示第24号;
  promulgated 2021年6月30日; the 平成13年告示第24号 amendment applies from 令和4年4月1日 and
  the rest from 令和3年10月1日; the 保険会社向けの総合的な監督指針 was amended alongside.

### R7 — 金融庁, 平成8年大蔵省告示第48号及び平成13年金融庁告示第24号の一部を改正する件（新旧対照表）
- Publisher: 金融庁
- Document: 新旧対照表 PDF attached to R6, 21 pp.
- URL: https://www.fsa.go.jp/news/r2/hoken/20210630/02.pdf
- Retrieved: YES (full PDF downloaded, 21 pp.; text extracts but is vertically typeset one
  character per line, so it was flattened before reading — only the amended provisions are
  reproduced, not the whole notification)
- Content: confirms the full title and legal basis of the notification that sets the
  標準利率 —「保険業法第百十六条第二項の規定に基づく長期の保険契約で内閣府令で定めるものに
  ついての責任準備金の積立方式及び予定死亡率その他の責任準備金の計算の基礎となるべき係数の
  水準（平成八年大蔵省告示第四十八号）」— and that the 基準日 for the level-premium
  standard-rate calculation is **1 October each year**, computed from JGB yields over a
  look-back window. The current numeric 標準利率 is **not** in this amendment document.

### R8 — 金融庁, 「平成８年大蔵省告示第48号等の一部を改正する件（案）の公表について」
- Publisher: 金融庁
- Document: 平成28年4月27日 publication
- URL: https://www.fsa.go.jp/news/27/hoken/20160427-2.html
- Retrieved: YES (browser-UA HTML fetch)
- Content: states plainly that the notification governs "責任準備金算出基礎としての予定利率
  （標準利率）の算出" and the solvency-margin coefficients, and that this amendment added a
  safety-factor coefficient for the case where the 指標金利 (the average JGB yield) is
  **zero or negative** — i.e. the standard rate is a JGB-linked, safety-loaded rate.

### R9 — e-Gov 法令検索, 所得税法 第76条（生命保険料控除）
- Publisher: デジタル庁 e-Gov 法令検索 (所得税法, 昭和40年法律第33号)
- URL: https://laws.e-gov.go.jp/law/340AC0000000033
  (retrieved via https://laws.e-gov.go.jp/api/2/law_data/340AC0000000033)
- Retrieved: YES (JSON via the e-Gov API v2; Article 76 extracted and paragraph 8 read)
- Content: 第76条第8項 defines 新個人年金保険契約等 — contracts concluded on or after
  2012年1月1日 that provide annuities and carry all three of: (1) the annuity recipient is the
  premium payer or, where alive, their spouse; (2) premiums are paid periodically over a
  period of **10 years or more before the annuity payment start date**; (3) the annuity
  payments meet the requirements set by Cabinet Order [R10].

### R10 — e-Gov 法令検索, 所得税法施行令 第183条・第211条・第212条
- Publisher: デジタル庁 e-Gov 法令検索 (所得税法施行令, 昭和40年政令第96号)
- URL: https://laws.e-gov.go.jp/law/340CO0000000096
  (retrieved via https://laws.e-gov.go.jp/api/2/law_data/340CO0000000096)
- Retrieved: YES (JSON via the e-Gov API v2; the three articles extracted and read in full)
- Content: **第211条** — the contract-design requirements: (イ) no cash payment other than the
  annuity except on the insured's death or severe disability (dividends and surrender value
  excepted); (ロ) that death/severe-disability amount must be defined so that it **increases
  progressively with elapsed policy duration or with cumulative premiums paid**;
  (ハ) annuities must be paid periodically at least once a year throughout the payment period
  and the contract must **not** permit partial commutation (other than instalments inside a
  guarantee period); (ニ) no cash distribution of dividends before the annuity start date
  beyond that year's premium. **第212条** — the payment-timing requirement: either
  (1) payments begin on or after a contract-stated date falling on or after 1 January of the
  year in which the recipient turns 60 (with a special rule moving that boundary to 1 July
  of the previous year where the 60th birthday falls between 1 January and 30 June) and
  continue periodically for **10 years or more**; or (2) they continue for the recipient's
  lifetime; or (3) a severe-disability-triggered annuity of ≥ 10 years or for life.
  **第183条** — how the 雑所得 on annuity receipts is computed: the necessary-expense fraction is
  total premiums divided by the total payments (or expected total payments) fixed at the
  annuity start date, rounded up at the third decimal.

### R11 — 国税庁, タックスアンサー No.1140「生命保険料控除」
- Publisher: 国税庁 (National Tax Agency)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the post-2012 (新契約) deduction schedule and per-basket / overall income-tax caps;
  the pre-2012 (旧契約) schedule and caps; the combination rule where a taxpayer holds both;
  the definition of 支払保険料等 as premiums net of dividends received that year; the statutory
  basis 所法76・120, 所令262.

### R12 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the NTA's plain-language restatement of the 個人年金保険契約等 conditions —
  recipient is the payer or spouse; premiums paid periodically over ≥ 10 years until
  payments begin; payments start when the recipient is in principle 60 and run ≥ 10 years or
  for life; plus the note that a severe-disability-triggered ≥ 10-year or life annuity also
  qualifies. Statutory basis 所法76・120, **所令208の3～212**, 262, 所規40の6・40の7・47の2.

### R13 — 国税庁, タックスアンサー No.1610「保険契約者(保険料の負担者)である本人が支払を受ける個人年金」
- Publisher: 国税庁
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1610.htm
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: where payer and recipient are the same person the annuity is 雑所得 (non-public
  pension), computed as the annuity received less the matching premium; a lump sum taken
  **instead of** the future annuity — before or after the payment start date — is 一時所得
  instead; the withholding formula and the threshold below which no withholding is made;
  where payer and recipient differ, the right to the annuity is deemed gifted at the trigger
  date and gift tax applies, with the income-tax stepping schedule of [R15] thereafter.

### R14 — 国税庁, タックスアンサー No.1620「相続等により取得した年金受給権に係る生命保険契約等に基づく年金の課税関係」
- Publisher: 国税庁
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1620.htm
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the double-taxation relief mechanism — an annuity whose 年金受給権 was acquired by
  inheritance, bequest or gift is split into a non-taxable and a taxable part; the first
  year is wholly non-taxable and the taxable part rises stepwise thereafter; the 課税割合 table
  keyed to 相続税評価割合 = 相続税評価額 ÷ total (or expected total) annuity payments; and the note
  that a lump sum taken **before** the annuity start date on such a right is income-tax
  exempt.

### R15 — 生命保険協会, 「２０２５年版 生命保険の動向」
- Publisher: 一般社団法人 生命保険協会 (Life Insurance Association of Japan, LIAJ)
- Document: 生命保険の動向 2025年版, 33 pp.
- URL: https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf
- Retrieved: YES (full PDF downloaded, 33 pp., text extracted; the individual-annuity
  section and the definitional footnotes read)
- Content: FY2024 new business, in-force and surrender/lapse volumes for 個人年金保険, split
  between 定額年金保険 and 変額年金保険 by count and by 契約高; the **definition of 契約高**
  for annuities (年金原資 before annuitisation, 責任準備金 after) — which matters when
  reading these numbers into a model; the surrender-and-lapse rate and its denominator
  (pre-annuitisation in-force only); and the sex split of new business.

### R16 — 生命保険文化センター, 「個人年金保険」（主契約の種類）
- Publisher: 公益財団法人 生命保険文化センター (JILI)
- URL: https://www.jili.or.jp/knows_learns/kind/main/30.html
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the market-wide taxonomy a single carrier's documents cannot give — the four
  annuity types (確定年金 / 保証期間付終身年金 / 有期年金 / 夫婦年金) and how each pays on
  death; 年金総額保証付終身年金 as a further variant; the 生存保障重視型 and
  長寿年金・長寿生存保険 death-benefit designs and their surrender-value ceilings; typical
  annuity-start ages; typical minimum annuity amount and minimum single premium; premium
  modes; 据置期間 practice for level-premium and single-premium contracts; issue-age ranges
  across the market; dividend types; the surrender rules before and after annuitisation;
  and the effect of the tax-qualification rider on dividend withdrawal.

### R17 — 生命保険文化センター, 「変額個人年金保険」（主契約の種類）
- Publisher: 生命保険文化センター (JILI)
- URL: https://www.jili.or.jp/knows_learns/kind/main/28.html
- Retrieved: YES (browser-UA HTML fetch, full body read)
- Content: the boundary of the fixed-annuity scope — 変額個人年金保険 runs in a 特別勘定 with
  the market risk borne by the policyholder; annuity fund and total-payment guarantees may
  or may not exist; surrender values are usually unguaranteed; death benefits are usually
  guaranteed at premiums paid; the account normally moves to the 一般勘定 at annuitisation so
  the annuity is fixed from then on, though variable-payout designs exist.

---

## Fact extraction

### 1. Product architecture and the two phases

- The contract has a **deferral phase** and a **payout phase**. Premiums accumulate to a
  年金原資 at the 年金支払開始日; the annuity is then paid annually while the insured lives
  (or, for 確定年金, regardless) [S2] [S4] [R16].
- 年金支払開始日 is defined as the **年単位の契約応当日 on which the insured's age reaches the
  年金支払開始年齢 chosen at issue**; 年金支払日 is that date for the first instalment and its
  annual anniversaries thereafter [S2] [S4] [S9].
- Because the 予定利率 at issue is applied, **the annuity amount is fixed at issue** for the
  annuity type chosen at issue [S2] [S3]. The exception is a type elected *at* annuitisation
  (notably 保証期間付終身年金), whose amount is computed on the 基礎率 (予定利率, 予定死亡率
  etc.) in force at the 年金支払開始日 and is therefore **not** determined at issue [S2] [S9].
- Under one design the whole basis is refreshed once mid-contract: the 予定利率 is updated at a
  stated duration in the light of market rates, subject to a minimum-guarantee 予定利率 fixed
  at issue, and the 年金原資 moves with it [S12].
- Annuity instalments that fall due are, on one carrier's contract, **automatically left on
  deposit** (年金の自動すえ置) with interest at a declared rate and paid on request or on
  termination, unless the annuitant elects otherwise [S2].
- Underwriting: the 無選択 designs require **no health disclosure at all** — one carrier's
  standard annuity states 「ご契約に際して、告知は不要です」 [S2], the **same carrier's**
  tontine states 「医師の診査や告知なしでお申し込みいただけます」 [S3], and a **second**
  carrier offers a 無選択特則 which, when attached, removes both the disclosure and the
  premium-waiver benefit [S4].
  [corrected 2026-08-20: the tontine at [S3] and the standard annuity at [S2] are the
  **same** carrier, so this bullet covers two carriers, not three. The earlier wording
  "another's tontine … and a third" is where the carrier count corrected downstream came
  from.]

### 2. Issue-age, premium-term, deferral and annuity-start envelopes

Observed ranges across the carriers whose documents were retrieved:

- 契約年齢 (issue age): **0–75** [S6]; **7–65** (18–55 through the online channel) [S9];
  **0–80** for one carrier's ordinary annuity [S3]; **満18歳から** [S12]. Market-wide, JILI
  describes carriers starting at age 0 and topping out around 65–70, with single-premium
  contracts written into the late 80s [R16].
- Tontine designs sit at the top of the age range: **50–80** [S3] and **male 50–87 /
  female 50–86** [S10].
- 年金支払開始年齢: **60–90** on the tontine [S3]; 65 in the standard illustration [S5] [S6];
  in principle 65 on one carrier [S12]. JILI reports that outside single-premium business
  the common menu is 「55歳、60歳、65歳、70歳、75歳のいずれか」 [R16].
- 保険料払込期間: **5–30 years** on the tontine [S3]. The tax rider forces ≥ 10 years on any
  contract that claims the third deduction basket [S1] [R9].
- 据置期間 (deferral gap between the end of premium payment and the annuity start):
  **≤ 15 years** on the tontine [S3]; on another carrier a deferral period is an explicit
  lever — "setting a deferral period increases the annuity" [S6]. The specimen contract
  60歳払込満了 / 65歳年金開始 carries a five-year 据置期間 [S5] [S6].
- Contract-to-annuitisation span: **≤ 30 years** on the tontine [S3].
- 年金支払期間 for 確定年金: **5 / 10 / 15 years**, chosen at issue [S2] [S3] [S9]; one carrier
  offers 確定年金 without stating the term menu on the retrieved page but the 5/10/15 menu is
  the mode. **A 5-year 確定年金 is incompatible with the tax rider** and one carrier's rider
  therefore refuses a change to a 5-year term [S2].
- Minimum sizes: JILI reports carriers writing from 年金年額 ¥120,000 and, for single premium,
  from about ¥1,000,000 [R16]. One carrier applies a premium-band discount
  (「たのしみランク」) once the monthly-equivalent premium reaches **¥15,000** [S6].

### 3. Annuity types and how each pays

- **確定年金** — paid on each 年金支払日 during the payment period. If the insured dies during
  the payment period before the last instalment, the **present value of the unpaid
  instalments** (残余年金支払期間の未払年金の現価) is paid to the annuitant / a nominated
  未払年金現価受取人; the annuitant may instead elect **continuation** of the instalments to
  the end of the term (年金の継続支払) [S2]. JILI describes the same shape market-wide [R16].
- **保証期間付終身年金** — paid for life; during the guarantee period payment does not depend
  on survival. Death inside the guarantee period pays the present value of the unpaid
  guaranteed instalments [S4] [R16]. Guarantee periods observed: **10 years** [S2] [S3] [S9]
  and **5 years** [S10].
- **有期年金** — paid while the insured lives during a fixed term (10 or 15 years typically);
  with a guarantee period the guaranteed instalments are unconditional; **without** one,
  death during the term typically returns any excess of premiums paid (or the 年金原資) over
  instalments already received, as a lump sum [R16]. **No retrieved carrier document in this
  session offers 有期年金 as a current option**; it survives in the taxonomy [R16] and in the
  wording of one carrier's tax rider, which contemplates 保証期間付有期年金 [S1].
- **夫婦年金** — pays while **either** spouse lives, usually with a ~10-year guarantee; if both
  insureds die inside the guarantee period the remaining guaranteed instalments (or their
  lump-sum value) go to the survivors [R16]. It is typically reached by **converting at
  annuitisation** from a 確定年金 or 保証期間付終身年金 [R16]. In the retrieved carrier
  documents it appears only as a 夫婦年金特約 / 夫婦年金移行特約 cross-referenced from other
  riders, with a 第１被保険者 and a 第２被保険者 [S2]; the rider's own conditions are in a
  different booklet and were not retrieved.
- **年金総額保証付（死亡時保証金額付）終身年金** — a life annuity that guarantees payment up
  to a stated amount (commonly the 年金原資), paying any shortfall as a lump sum [R16].
- 年金の一括払 / 一括受取 (commutation): the annuitant may, at any time from the annuity start
  date up to the last 年金支払日, take the **present value of the remaining instalments** — the
  remaining payment period for 確定年金, the remaining guarantee period for
  保証期間付終身年金 — as a lump sum, and the contract then terminates [S2] [S4].
- Payout-phase restrictions after annuitisation: no policy loan and no reduction of the
  annuity amount; only commutation of the remaining guaranteed instalments is available
  [S4]. JILI puts it generally: after annuitisation the contract cannot normally be
  surrendered [R16].

### 4. 年金原資, the annuitisation election, and the lump-sum option

- 年金原資 is the accumulated fund at the 年金支払開始日 out of which the annuity is bought.
  One carrier publishes both a **一括受取率 (= 年金原資 ÷ 払込保険料総額)** and a
  **年金受取率 (= 年金受取総額 ÷ 払込保険料総額)** for the same model point, which pins down
  exactly what the 年金原資 is [S6].
- Specimen, level monthly premium ¥15,000, 60歳払込満了, 65歳年金開始, 10年確定年金, as at
  2025年10月, after the band discount [S6]:

  | 契約年齢 | Sex | 払込保険料総額 | 年金原資 | 一括受取率 | 基本年金額 | 年金受取総額 | 年金受取率 |
  |---|---|---|---|---|---|---|---|
  | 20 | M | ¥7,200,000 | approx. ¥8,780,000 | approx. 121.9% | ¥895,100 | ¥8,951,000 | approx. 124.3% |
  | 30 | M | ¥5,400,000 | approx. ¥6,260,000 | approx. 115.9% | ¥638,300 | ¥6,383,000 | approx. 118.2% |
  | 40 | M | ¥3,600,000 | approx. ¥3,890,000 | approx. 108.0% | ¥396,500 | ¥3,965,000 | approx. 110.1% |
  | 20 | F | ¥7,200,000 | approx. ¥8,750,000 | approx. 121.6% | ¥892,800 | ¥8,928,000 | approx. 124.0% |
  | 30 | F | ¥5,400,000 | approx. ¥6,250,000 | approx. 115.8% | ¥637,500 | ¥6,375,000 | approx. 118.0% |
  | 40 | F | ¥3,600,000 | approx. ¥3,890,000 | approx. 108.0% | ¥396,500 | ¥3,965,000 | approx. 110.1% |

- 年金内容変更制度: at annuitisation the annuitant may elect the annuity type inside the
  insurer's range (保証期間付終身年金 or 確定年金) and may **split** the fund across more than
  one type (複数年金選択制度) [S4]. Another carrier lets the type be changed at annuitisation
  to any of 5/10/15年確定年金 or 10年保証期間付終身年金, subject to the type still being
  offered and the resulting annuity clearing the insurer's minimum [S9].
- The **first annuity payment date may be deferred** by up to five years at the
  policyholder's election [S9].
- Where the tax rider is attached and the fund has been split across several annuity types,
  a commutation request on **one** of them is treated as a request on **all** of them [S1],
  and partial commutation of one type alone is refused [S4]. This is the contractual
  expression of 所令211①ハ, which forbids partial commutation [R10].

### 5. Death benefit during deferral (死亡給付金)

- The market splits into three designs [R16]:
  1. **生存保障重視型** — the death benefit is held down to the cumulative premiums paid, which
     buys a larger annuity;
  2. **長寿年金・長寿生存保険 (tontine)** — the death benefit is held down to about **70%** of
     cumulative premiums, buying a larger annuity still;
  3. designs adding a 災害死亡給付金 at a stated uplift (e.g. 110%) over the ordinary amount.
- Contractually, two carriers define the deferral-phase death benefit as
  **月払保険料 × 経過月数** — the monthly premium for the basic annuity multiplied by elapsed
  months, the *same amount whichever premium mode is in force* [S2] [S4]. A third describes
  it as 既払込保険料相当額 [S6]. These are the same idea expressed two ways.
- This is not a marketing choice: 所令211①ロ **requires** the death (or severe-disability)
  amount on a deduction-qualifying annuity to be defined so that it increases progressively
  with elapsed duration or with cumulative premiums paid [R10].
- Tontine variants:
  - one carrier pays a 死亡返還金 of **払込保険料相当額の7割** [S3];
  - another provides **no death cover at all** — 「死亡保障を行わないため、年金開始日前に
    被保険者が死亡されたときは、解約払戻金と同額の死亡払戻金しか支払われません」, with the
    surrender value itself set at a **70%** suppression ratio [S10].
- Where the death benefit is *not* paid because an exclusion bites, one carrier's 約款 pays
  the **責任準備金 instead, capped at the death benefit amount** [S2].
- Death benefits may be taken as a lump sum, as an annuity, or left on deposit [S4].
- Unpaid premiums, policy-loan principal and interest, and automatic-premium-loan balances
  are deducted from the death benefit [S2] [S4].

### 6. Surrender value during deferral (解約返戻金 / 解約返還金)

- Surrender is available **only before the 年金支払開始日** [S2].
- The value is computed from 経過年月数 — capped at the 払込年月数 where premiums are still
  being paid — and is **limited to the death benefit amount**: 「解約返還金は…死亡給付金の額を
  限度とします」 [S2]. The same ceiling appears in the other carrier's wording: where the fund
  accumulated for future annuity payments exceeds the death benefit, the surrender value is
  paid only up to the death benefit, so the policyholder receives less than the accumulated
  fund [S4], and 「この保険の解約返戻金は、一定期間経過後は死亡給付金と同額になります」 [S4].
- Consequence for a 生存保障重視型 contract: the surrender value **can never exceed cumulative
  premiums paid** [R16]. For a tontine it can never exceed **70%** of them, so surrender is
  loss-making at every duration [S3] [S10].
- Early durations: 「ご契約後短期間で解約されたときには、解約返還金がない場合があります」
  [S2]; 「まったくないか、あってもごくわずか」 [S4].
- The rate-resetting design instead states a duration after which the surrender value
  **exceeds** cumulative premiums [S12].
- Reduction of the basic annuity (基本年金額の減額) pays out the surrender value of the reduced
  portion — but see §11: under the tax rider that payment is not released [S1] [S4].
- Payment is made within five business days of the complete claim file arriving [S2] [S4].

### 7. Premium structure, modes and prepayment

- Modes: 月払 / 年払 / 半年払, plus 一時払 on single-premium products [S4] [R16]. Payment routes
  are direct debit, transfer slip (annual and semi-annual only), group/payroll, and credit
  card [S2] [S4].
- 前納 (prepayment of three or more annual premiums at once): the prepaid amount is
  **discounted** at a declared rate and the balance accumulated at a declared rate, from
  which each annual premium is drawn at the anniversary; any residue is refunded on
  termination [S4]. One carrier publishes the prepaid-premium discount rate as **年0.01%**
  and the prepaid-premium accumulation rate as **年0.60%** as at 2026年4月2日 [S11].
- Lump-payment discounts for 3–12 months of premiums paid together are published as a table
  by issue-date cohort, policy term and product [S11].
- Refund on early termination: for annual and semi-annual policies the unused whole months
  of premium are refunded; **for monthly policies nothing is refunded** [S4].
- 保険料の払込免除: where the insured reaches the 約款-defined 高度障害状態, or a listed
  身体障害の状態 from an accident within 180 days, future premiums are waived — but **not** if
  the 無選択特則 is attached [S4]. Another carrier sells the waiver as a rider triggered by the
  three major diseases [S9].
- Band discount: one carrier applies 「たのしみランク」 once the monthly-equivalent premium
  reaches ¥15,000 [S6].

### 8. 予定利率 — the pricing basis, and what is published

Japanese annuity documentation publishes the pricing interest rate directly. Retrieved
values:

| Carrier | Product | Basis | Before | After | Effective |
|---|---|---|---|---|---|
| [S8] | 年金保険 (excl. 一時払) | 予定利率 | 0.60% | **1.00%** | 契約日 2025-01-02 onward |
| [S8] | 長寿生存保険（低解約払戻金型） | 予定利率 | 0.60% | **1.00%** | 契約日 2025-01-02 onward |
| [S5] | 生存保障重視型個人年金保険(14), ≥ 30 yrs to annuitisation | 予定利率 | 0.80% | **1.20%** | 契約日 2025-10-02 onward |
| [S5] | same, < 30 yrs to annuitisation | 予定利率 | 0.65% | **1.00%** | 契約日 2025-10-02 onward |
| [S5] | same, **post-annuitisation** | 予定利率 | 0.65% | 0.65% (unchanged) | — |

- Two facts a modeller cannot guess follow from this table. First, the deferral-phase 予定利率
  can be **banded by the years remaining to annuitisation** [S5]. Second, the **payout phase
  carries its own 予定利率**, set separately from the deferral phase and left unchanged when the
  deferral rate moved [S5].
- The 2025 increase was described as the first in about **40 years** [S8].
- A rate-resetting design publishes a **minimum-guarantee 予定利率 of 0.50%** (as at 2026年6月),
  fixed at issue and unchangeable thereafter, with the actual rate updated once at a stated
  duration; its illustration assumes a payout-phase 予定利率 of **0.55%** in the rate-maintained
  or rate-rising scenario and **0.15%** in the rate-falling scenario, and a future
  new-business rate of **2.30%** for the 金利キャッチアップ配当 projection [S12].
- Derived, not published: the 未払年金の現価 factor table in one carrier's 約款 [S2] implies a
  commutation discount rate of about **0.40% p.a.** The published factors are 1.010, 2.016,
  3.018, 4.016, 5.010, 6.000, 6.986, 7.968, 8.946, 9.921, 10.891, 11.858, 12.821 and 13.780
  for 1 to 14 remaining instalments; successive first differences fall in a near-constant
  ratio of 0.99602, i.e. i ≈ 0.400%, and the factors are close to an annuity-due at that
  rate scaled by about 1.010. The 約款 then discounts the result from the death or commutation
  date to the day before the next 年金支払日 at a **declared** rate [S2]. Treat 0.40% as an
  inference from the published table, not as a published 予定利率.
- Single-premium rate mechanics (for contrast, from a non-annuity product line of the same
  group): the 予定利率 for a yen single-premium contract is reset **twice a month** for new
  business, then again at stated 予定利率計算基準日 anniversaries, floored by a minimum-guarantee
  予定利率 of 0.25%, and pegged to named JGB benchmark yields chosen by the insured's age [S13].

### 9. Dividends (契約者配当)

- The mainstream chassis is **5年ごと利差配当** (interest-differential dividends every five
  years). Where the investment return on the 責任準備金 exceeds the assumed return, a dividend is
  paid from the **sixth policy year, then every five years**, and additionally on
  termination by death, on surrender or reduction, and on commutation [S4]. One product line
  is 5年ごと配当付 [S3]. Market-wide the menu is 無配当 / 5年ごと利差配当 / 毎年配当, with 無配当 dominating
  single-premium, 積立利率変動型 and foreign-currency annuities [R16].
- Before annuitisation the dividend is accumulated at a declared 配当積立利率 and applied to
  increase the annuity; after annuitisation it may be taken as cash with each instalment,
  used to buy additional annuity, or accumulated [S4] [S2].
- Under the tax rider the accumulated dividend **cannot be withdrawn** before annuitisation
  and is instead applied as a single premium increasing the 基本年金額 [S1] [S4] [S12] [R16].
  This is the contractual expression of 所令211①ニ [R10].
- One carrier pays no dividend at all on surrender or reduction within the first two policy
  years, and states that the dividend paid on surrender is smaller than the one paid on
  death [S4].
- One carrier's declared 社員配当金の積立利率 is **年0.60%** as at 2026年4月2日 [S11].
- A design outside the dividend chassis pays a 金利キャッチアップ配当 when new-business 予定利率
  rises above the rate at issue [S12].

### 10. Policy loans, automatic premium loans, grace, lapse and reinstatement

- **契約者貸付**: available within the insurer's stated fraction of the surrender value, with
  compound interest at a declared rate reviewed twice a year (first business day of January
  and July, applying from the following 1 April and 1 October) [S4]. One carrier publishes
  the rate by issue-date cohort: 3.05% (2012-04-02 to 2014-04-01), 2.55% (to 2017-04-01),
  2.25% (to 2022-04-01), 2.00% (to 2025-01-01), and **2.40% for contracts dated 2025-01-02
  onward** [S11], the increase announced alongside the 予定利率 rise [S8]. No policy loan is
  available after annuitisation [S4].
- **自動振替貸付 (automatic premium loan)**: if the premium is unpaid at the end of the grace
  period the insurer automatically lends the premium against the surrender value and keeps
  the policy in force unless the policyholder has opted out; compound interest applies at a
  rate reviewed twice a year and **capped at 年8%** [S4]. **This is product-specific, not
  universal: one carrier's annuity states outright 「この保険には、保険料の自動貸付の取り扱いはありません」**
  [S2].
- Where loan principal and interest exceed the surrender value, the insurer demands a
  payment; if it is not made by the stated deadline the contract lapses from the moment the
  excess arose [S4].
- At annuitisation the loan must be settled. Under the tax rider the choices are: take the
  commutation lump sum at the annuity start date and net the loan off it, or deduct it from
  successive annuity instalments [S4]; or, in another carrier's wording, deduct it from the
  annuity, unless the balance exceeds a stated amount, in which case it is deducted from the
  責任準備金 and the net paid as a lump sum, terminating the contract [S1] [S2]. Where the loan
  is netted off the reserve, the residual reserve is used to redefine the annuity, and if
  the redefined annuity falls below the insurer's minimum it is paid as a lump sum instead
  [S4].
- **払込猶予期間 (grace)**: for **monthly** premiums the grace period runs from the first day of
  the month after the 払込期月 to the **last day of that month** — i.e. to the end of the
  following month. For **annual and semi-annual** premiums it runs from the first day of the
  next month to the monthly contract anniversary of the month after that (with special
  end-of-month handling where the anniversary falls on the last day of February, June or
  November, in which case it runs to the last day of April, August or January respectively)
  [S4].
- Where a death claim or a waiver trigger arises during the grace period on a monthly
  direct-debit contract, **two months of premium** are deducted from the claim or must be
  paid [S4].
- **失効 (lapse)**: the contract loses effect from the day after the grace period expires if
  the premium is unpaid and no automatic premium loan is made [S4].
- **復活 (reinstatement)**: available within **three years of lapse** [S2] [S4], and only
  before the 年金支払開始日 [S2]. It requires a reinstatement application, payment of all arrears
  plus late interest in one sum, and fresh health disclosure (waived where the 無選択特則 is
  attached) [S2] [S4]. Cover restarts when the insurer accepts and receives the money [S4].
  Reinstatement is barred once a refund equal to the surrender value has been claimed [S2].
- **払済年金保険 (paid-up)**: premiums stop and the 基本年金額 is redefined — normally lower —
  from the surrender value, with the 年金支払開始日 unchanged and the death benefit held at its
  value at conversion, net of any loan [S2] [S4]. **Under the tax rider, conversion to
  paid-up is refused inside the first ten policy years** [S1] [S4] [S12].
- **復旧 (reversal)**: within three years of a paid-up conversion or a reduction, the original
  contract can be restored [S4].

### 11. 税制適格特約 — the mechanic that shapes the product

**The four attachment conditions**, verbatim from a rider's own 第1条 [S1]:

1. 年金受取人は保険契約者またはその配偶者のいずれかであること
2. 年金受取人は被保険者と同一人であること
3. 保険料払込期間は10年以上であること
4. 年金の種類が確定年金または保証期間付有期年金の場合、年金支払開始日における被保険者の年齢は
   60歳以上で、かつ、年金支払期間は10年以上であること

One other carrier states the same four in the same order, on both of its retrieved product
pages [S9] [S10], and a second states them split into an 所得税法 limb and an 所得税法施行令
limb, adding that **condition 4 does not apply to 保証期間付終身年金** [S4]
[corrected 2026-08-20: [S9] and [S10] are two documents of the **same** carrier, not two
carriers. Counting the rider itself [S1], two of the five carriers state the four
conditions in that order and a third splits them — which is the count carried downstream] — consistent with 所令212 treating a lifetime annuity as qualifying
on its own [R10].

**How the four map onto the statute** [R9] [R10] [R11] [R12]:

- Condition 1 is 所法76⑧一 — the recipient is the premium payer or, where alive, their spouse.
- Condition 3 is 所法76⑧二 — premiums paid periodically over ≥ 10 years **before the annuity
  payment start date**.
- Condition 4 is 所令212一 — payments begin on or after a contract-stated date falling on or
  after **1 January of the year in which the recipient turns 60** (moved back to 1 July of
  the previous year where the 60th birthday falls between 1 January and 30 June) and
  continue for **≥ 10 years**; 所令212二 qualifies a lifetime annuity without any term test.
- Condition 2 (年金受取人 = 被保険者) is **not** in the statutory text retrieved. 所法76⑧ ties
  the recipient to the payer or spouse [R9] and 所令211/212 govern the payment structure and
  the recipient's age [R10]; the NTA restatement likewise does not mention it [R12]. The
  insured-equals-annuitant condition is stated by **three of the five carriers** [S1] [S4]
  [S9] [S10] — every carrier whose retrieved documents state the conditions at all — and is
  best read as
  [corrected 2026-08-20: "every carrier" over-counted; [S9] and [S10] are one carrier, so
  the four tags are three carriers out of the five] the industry's way of making the 60-year test operable on the policy's age
  basis (Japanese policies compute everything from 契約年齢 of the 被保険者). Treat the *statutory*
  status of condition 2 as [unverified]; its *contractual* status is fully sourced.

**The contract-design conditions the rider must also satisfy** — 所令211第1号 [R10]:

- **イ** no cash payment other than the annuity, except on the insured's death or severe
  disability (dividends and surrender value excepted). One carrier's summary of the same
  rule: 「年金以外の金銭によるお支払いは、死亡給付金（死亡保険金）、高度障害保険金、解約返戻金に限る
  こと」 [S4].
- **ロ** the death / severe-disability amount must **increase progressively** with elapsed
  duration or cumulative premiums. This is why the death benefit is 月払保険料 × 経過月数 [S2]
  [S4] rather than a level sum assured.
- **ハ** annuities paid at least yearly throughout the term, and **no partial commutation**.
- **ニ** no cash dividend distribution before the annuity start date. One carrier's summary:
  「年金支払開始日前に契約者配当金の金銭によるお支払いを行わないこと」 [S4].

**What attaching the rider does to the contract** [S1] [S4] [S2] [S9] [S12]:

- 年金受取人の変更は取り扱いません — the annuitant may not be changed [S1] [S2] [S4].
- Contract changes that would breach the conditions are refused, including bringing the
  premium term forward below ten years, and changing to a 5-year 確定年金 [S1] [S2].
- 払済 conversion is allowed only after ten years of premiums have been paid on a policy in
  force from the contract date [S1] [S2] [S4] [S12].
- Any refund arising on a change (reduction of the basic annuity, cancellation of another
  rider, the residue of prepaid premiums) is **not paid out**. It is accumulated at a
  declared rate to the annuity start date and applied as a single premium increasing the
  基本年金額; if the contract terminates before annuitisation it is paid to the policyholder (or
  the death-benefit beneficiary) [S1] [S2] [S4]. One carrier publishes the rate applied to
  such amounts — 税制適格型年金保険の払戻金等の積立利率 **年0.60%** as at 2026年4月2日 [S11].
- On a reduction, the loan is **not** netted off the payment, and a reduction that would
  leave the loan exceeding the surrender value is refused outright [S1] [S2].
- Dividends before annuitisation are accumulated and applied to increase the annuity; they
  cannot be drawn [S1] [S2] [S4].
- The rider **cannot be surrendered on its own**: 「この特約のみの解約はできません」 [S1] [S4].
- The rider is **deemed to have lapsed** when the main contract terminates, when the premium
  waiver is triggered, or when a change of policyholder breaks condition 1 [S1].
- Without the rider the premium falls in the **一般生命保険料控除** basket instead [S12] [R16].

### 12. 生命保険料控除 — the three baskets and their caps

Post-2012 (新契約) income-tax schedule, per basket [S4] [R11]:

| 年間の支払保険料等 | 控除額 |
|---|---|
| ≤ ¥20,000 | the whole amount |
| > ¥20,000 and ≤ ¥40,000 | premium × 1/2 + ¥10,000 |
| > ¥40,000 and ≤ ¥80,000 | premium × 1/4 + ¥20,000 |
| > ¥80,000 | ¥40,000 flat |

Residence-tax schedule, per basket [S4]:

| 年間の支払保険料等 | 控除額 |
|---|---|
| ≤ ¥12,000 | the whole amount |
| > ¥12,000 and ≤ ¥32,000 | premium × 1/2 + ¥6,000 |
| > ¥32,000 and ≤ ¥56,000 | premium × 1/4 + ¥14,000 |
| > ¥56,000 | ¥28,000 flat |

- Caps: **¥40,000 per basket, ¥120,000 overall** for income tax; **¥28,000 per basket,
  ¥70,000 overall** for residence tax [S4] [R11]. The three baskets are 一般生命保険料 / 介護医療保険料 /
  **個人年金保険料** [S4] [R11] [R16].
- Pre-2012 (旧契約) schedule: whole amount to ¥25,000; ×1/2 + ¥12,500 to ¥50,000; ×1/4 +
  ¥25,000 to ¥100,000; ¥50,000 flat above — cap ¥50,000 per basket [R11].
- 支払保険料等 is premiums paid in the calendar year **net of dividends received or accumulated
  that year** [S4] [R11].
- Claiming requires a 生命保険料控除証明書, which the insurer issues in October for annual and
  semi-annual policies paid by end-September, and after confirming the September collection
  for monthly direct-debit policies [S4].

### 13. Taxation of the benefits

- **Annuity, payer = annuitant**: 雑所得 (non-public-pension), = annuity received less the
  matching premium [S4] [R13]. The matching-premium fraction is total premiums ÷ total (or
  expected total) payments fixed at the annuity start date, rounded up at the third decimal
  [R10]. Withholding is **(annuity − matching premium) × 10.21%**, and **no withholding**
  where that difference is under ¥250,000 for the year [R13].
- **Annuity, payer ≠ annuitant**: the right to the annuity is deemed gifted at the trigger
  date and **gift tax** applies on the tax-law valuation; income tax on each subsequent
  instalment then follows the stepped schedule — wholly exempt in year one, the taxable
  share rising stepwise thereafter [S4] [R13] [R14]. The 課税割合 is read off a table keyed to
  相続税評価割合 = 相続税評価額 ÷ total (or expected total) annuity payments [R14].
- **A lump sum taken instead of the future annuity** — before or after the payment start
  date — is **一時所得**, not 雑所得 [R13]; where the right was acquired by inheritance or gift and
  the lump sum is taken **before** the payment start date, it is **income-tax exempt**
  [R14].
- **Death benefit during deferral** [S4]:

  | 契約形態 | Tax |
  |---|---|
  | 契約者 = 被保険者 | 相続税 |
  | 契約者 = 受取人 | 所得税（一時所得） |
  | 契約者・被保険者・受取人 all different | 贈与税 |

### 14. Exclusions, contestability and forfeiture

- **自殺免責**: no death benefit where the insured takes their own life **within three years,
  counted inclusive, from the 責任開始日 (or, where the policy was reinstated, from the last
  復活日)** [S2] [S4]. This is materially longer than the UK's twelve months. Where the
  exclusion bites, one carrier pays the 責任準備金, capped at the death benefit amount, to the
  policyholder [S2].
- Also excluded: death caused intentionally by the policyholder (no refund of any reserve)
  or by the death-benefit beneficiary (the remaining beneficiaries are paid their shares)
  [S2] [S4].
- **告知義務違反**: the insurer may rescind within **two years of the 責任開始日 (or 復活日)**
  and within one month of learning the fact [S4].
- **詐欺 / 不法取得目的**: the contract is void; premiums are not refunded [S2] [S4].
- **無効 for non-payment of the first premium**: where the first premium is not paid by the
  end of its grace period the contract is void, no refund is made, it cannot be restored,
  and the insurer declines new business on the same lives for **two years** from that
  contract date [S4].
- **クーリング・オフ**: withdrawal is available within eight days of the later of the application
  date and the delivery of the disclosure documents [S4].
- **時効**: claims for the annuity, the death benefit and the surrender value prescribe after
  the statutory period stated in the 約款 [S2].

### 15. トンチン年金 (tontine annuities) — a distinctively Japanese design

- Definition as the carriers give it: 「死亡時のお支払額を抑えることで、その分生きている他の
  加入者の年金額を大きくする仕組み」 [S3]; 「死亡した方の持分が生きている方に移ることで、より
  多くの給付が与えられる割合」 [S10]. JILI classes them as 長寿年金・長寿生存保険 [R16].
- Two carriers' designs, both retrieved:

  | Feature | Carrier A [S3] | Carrier B [S10] |
  |---|---|---|
  | Product class | 5年ごと配当付生存保障重視型個人年金保険 | 長寿生存保険（低解約払戻金型）|
  | 契約年齢 | 50–80 | male 50–87, female 50–86 |
  | 年金支払開始年齢 | 60–90 | chosen 指定年齢 at issue |
  | 保険料払込期間 | 5–30 years | e.g. to 70 or 80 |
  | すえ置期間 | ≤ 15 years | not stated on the page |
  | Contract to annuitisation | ≤ 30 years | not stated |
  | 年金の種類 | 10年保証期間付終身年金, 確定年金 5/10/15 | 5年保証期間付終身年金, 10年確定年金 |
  | Death payment in deferral | 死亡返還金 = 70% of premiums paid | none as such — 死亡払戻金 = the surrender value |
  | Surrender in deferral | capped at the 死亡返還金 | suppression ratio 70% |
  | Underwriting | none (no medical, no disclosure) | not stated on the page |
  | Riders | 指定代理請求特約, 個人年金保険料税制適格特約（Ｓ60） | 個人年金保険料税制適格特約 |

- Carrier A's release prices the **same model point** on its tontine and its ordinary
  annuity — 50-year-old male, premiums to 65, annuity from 75, ¥50,000/month, 10年確定年金 [S3]:

  | | 死亡/解約 floor | 年金額 | 10-year 返還率 |
  |---|---|---|---|
  | Tontine | 70% of premiums paid | ¥1,024,500 | 113.8% |
  | Ordinary annuity | 100% of premiums paid | ¥948,600 | 105.4% |

  The tontine buys about **8% more annuity** for the same premium by giving up 30% of the
  death and surrender floor. That difference is the whole economics of the design.
- Carrier A's full specimen set [S3]:

  | 年金種類 | Sex | 加入年齢 | 払込満了 | 年金開始 | 月払保険料 | 年金額 | 返還率 |
  |---|---|---|---|---|---|---|---|
  | 10年保証期間付終身年金 | M | 50 | 70 | 70 | ¥30,000 | ¥378,600 | 163.0% at age 100 |
  | 10年保証期間付終身年金 | M | 50 | 65 | 75 | ¥50,000 | ¥602,600 | 174.0% at age 100 |
  | 10年保証期間付終身年金 | F | 50 | 70 | 70 | ¥30,000 | ¥304,300 | 131.0% at age 100 |
  | 10年保証期間付終身年金 | F | 50 | 65 | 75 | ¥50,000 | ¥474,000 | 136.9% at age 100 |
  | 10年確定年金 | M | 50 | 70 | 70 | ¥30,000 | ¥770,200 | 106.9% |
  | 10年確定年金 | M | 50 | 65 | 75 | ¥50,000 | ¥1,024,500 | 113.8% |
  | 10年確定年金 | F | 50 | 70 | 70 | ¥30,000 | ¥763,200 | 106.0% |
  | 10年確定年金 | F | 50 | 65 | 75 | ¥50,000 | ¥1,000,100 | 111.1% |

- Carrier B publishes premiums for a ¥600,000 annuity, 払込満了 80, 10年確定年金, showing the
  female premium **above** the male at each issue age (e.g. issue 50: male ¥14,622, female
  ¥14,904 monthly; issue 55: ¥17,784 / ¥18,132; issue 60: ¥22,572 / ¥22,998) [S10]. Same
  direction in carrier B's rate-change release for the same product (issue 50, annuity from
  70, ¥600,000 p.a., 10年確定年金: male ¥23,004, female ¥23,172 after the change) [S8]. The sign
  is the survivorship effect: with the death benefit suppressed, the longer-lived sex must
  pay more for the same guaranteed annuity.
- Carrier B's warning is worth carrying into the model: on a **5-year guaranteed life
  annuity**, 「年金開始日から被保険者の死亡日までの期間によっては、年金および死亡一時金の支払額の合計額が
  払込保険料の合計額を下回ることがあります」 [S10].

### 16. Valuation basis — standard tables, standard reserve, standard rate

- **標準生命表2018 contains no annuity table.** The published file holds exactly four tables:
  生保標準生命表2018（死亡保険用）男/女 and 第三分野標準生命表2018 男/女 [R2].
- The post-annuitisation valuation table is **生保標準生命表2007（年金開始後用）**, and the IAJ
  confirmed on 2025年12月18日 that it continues to apply for **FY2026**, alongside
  生保標準生命表2018（死亡保険用）for death cover and 第三分野標準生命表2018 for third-sector
  cover [R4].
- The 年金開始後用 table is downloadable and machine-readable from the IAJ's combined Excel
  file [R3], and is **not redistributable** — the sample rates below are quoted, with
  attribution, because a worked example needs them, and no copy of the file is shipped.
  [corrected 2026-08-20: an earlier revision of this bullet said "redistributable"; the
  日本アクチュアリー会 site terms bar reproduction and transmission to third parties without
  written consent, so the library cites and quotes but ships a [std] construction instead
  — see the correction on R3.] Sample qx (生保標準生命表2007 年金開始後用):

  | Age | Male qx | Female qx |
  |---|---|---|
  | 20 | 0.00037 | 0.00014 |
  | 40 | 0.00090 | 0.00047 |
  | 50 | 0.00241 | 0.00118 |
  | 60 | 0.00642 | 0.00218 |
  | 65 | 0.00966 | 0.00301 |
  | 70 | 0.01411 | 0.00410 |
  | 80 | 0.03357 | 0.01275 |
  | 90 | 0.08318 | 0.04851 |
  | 100 | 0.17469 | 0.12540 |
  | 110 | 0.31667 | 0.25764 |

  Terminal ages (first age with qx = 1): **male 122, female 126** [R3]. For contrast, the
  死亡保険用 2018 table terminates at male 109 / female 113 and the 第三分野2018 table at
  male 116 / female 118 [R3].
- The annuity table is materially **lighter** than the death-cover table at every adult age
  — at age 80 the male rate is 0.03357 against 0.05006, and at age 90 0.08318 against
  0.15760 [R3]. That is the anti-selection margin working in the opposite direction, and it
  is why an annuity reserve cannot be computed off the death-cover table.
- **標準責任準備金 scope**: 保険業法施行規則第68条 excludes from the regime contracts whose
  reserve varies with 特別勘定 assets, contracts with no 保険料積立金 or 払戻積立金, and
  contracts whose 約款 permits the insurer to change the 予定利率 or the reserve/premium basis —
  except where the 約款 guarantees a floor at or above the 標準利率 applicable at issue [R5].
  Read against [S12], this is precisely why a rate-resetting annuity carries a
  **minimum-guarantee 予定利率 fixed at issue**.
- **標準利率**: set by 平成8年大蔵省告示第48号 under 保険業法第116条第2項, most recently amended
  (with 平成13年金融庁告示第24号) by a notification promulgated 2021年6月30日, applying from
  2021年10月1日 and, for the 平成13年告示第24号 limb, 2022年4月1日 [R6] [R7]. The level-premium
  standard rate is computed from JGB yields with safety-factor coefficients, on a 基準日 of
  **1 October each year** [R7]; a 2016 amendment added the coefficient for a
  zero-or-negative 指標金利 [R8]. **The current numeric 標準利率 could not be established from a
  retrieved document** — see the gaps section.
- Insolvency backstop: the 生命保険契約者保護機構 covers **90% of the 責任準備金等** except for
  高予定利率契約, for which the coverage is 90% − {Σ(予定利率 − 基準利率 over the last five
  years) ÷ 2}; for a variable annuity the 年金原資保証額 is likewise covered at 90% [S4].

### 17. Market context (for scale and for behavioural assumptions)

FY2024, all LIAJ member companies, 個人年金保険 [R15]:

- 新規契約件数 1.49 million (112.5% of the prior year); 新規契約高 ¥9.3397 trillion (113.8%),
  a fourth consecutive year of growth.
- 新契約件数 (excluding conversions) 1.47 million; split 定額年金保険 **0.95 million (64.9%)** /
  変額年金保険 0.51 million (35.1%). By 契約高, 定額 ¥5.4646 trillion (57.6%) / 変額 ¥4.0197
  trillion (42.4%).
- 保有契約件数 **20.06 million** (100.6%, the first rise in eight years); 保有契約高
  **¥104.1428 trillion** (102.0%). Split by count: 定額 17.56 million (87.5%) / 変額 2.50
  million (12.5%); by 契約高: 定額 ¥87.8836 trillion (84.4%) / 変額 ¥16.2592 trillion (15.6%).
- **解約・失効高 ¥2.8644 trillion; 解約・失効率 3.4%** (down 0.1 pt). The denominator is
  **pre-annuitisation in-force 契約高 at the start of the year only** [R15] — so this is a
  deferral-phase decrement rate, which is exactly the one a model needs.
- 契約高 definition, which is not obvious: **年金原資** for contracts before annuitisation and
  **責任準備金** for contracts after it [R15].
- New business sex split FY2024: male 45.9%, female 54.1% [R15].

### 18. Scope boundaries

- **一時払個人年金**: single-premium contracts normally carry a 据置期間, ranging across the
  market from 1/2/3 years to 5/10/15 years; they are typically 無配当; the minimum single
  premium is around ¥1,000,000; issue ages run into the late 80s; and no premium waiver
  applies because there are no future premiums [R16]. For the rate mechanics of yen
  single-premium business (though on 養老 and 終身, not annuity) the 予定利率 is reset twice monthly
  for new business and again at stated 予定利率計算基準日, floored by a minimum guarantee and pegged
  to named JGB benchmarks [S13].
- **変額個人年金保険**: assets in a 特別勘定, market risk on the policyholder; the annuity fund
  and/or total payments may be guaranteed but the surrender value usually is not; the death
  benefit is usually guaranteed at premiums paid; at annuitisation the fund normally moves
  to the 一般勘定 so the annuity is fixed from then on, though variable-payout designs exist;
  annuity types are 確定年金, 保証期間付終身年金 and 夫婦年金 [R17]. Contracts whose reserve varies with
  特別勘定 assets are **outside 標準責任準備金** [R5].
- **外貨建 / 市場価格調整 (MVA)**: JILI notes both exist in the individual-annuity market and
  carry market risk borne by the policyholder [R16].
- The tax rider is available only on the fixed, level-premium chassis in the retrieved
  documents; one carrier notes it cannot be attached where the insured's age at the relevant
  point falls outside the qualifying range [S12], and another that it cannot be attached to
  a particular plan variant [S6].

---

## Variation across carriers

| Feature | 第一生命 [S1] [S2] [S3] | 三井住友海上あいおい [S4] | 住友生命 [S5] [S6] | 日本生命 [S8]–[S11] | 明治安田生命 [S12] |
|---|---|---|---|---|---|
| Annuity types at issue | 確定年金 5/10/15 only [S2]; tontine adds 10年保証期間付終身年金 [S3] | 確定年金 and 保証期間付終身年金（定額型）[S4] | 確定年金 (10-yr in all published examples) [S5] [S6] | 確定年金 5/10/15 [S9] | not stated on the retrieved page |
| Type electable at annuitisation | 10年保証期間付終身年金 via rider [S2] | 保証期間付終身年金 or 確定年金, and a **split across several types** [S4] | not stated | 5/10/15年確定年金 or 10年保証期間付終身年金 [S9] | not stated |
| 契約年齢 | 0–80 (ordinary) [S3]; 50–80 (tontine) [S3] | not extracted | 0–75 [S6] | 7–65 (18–55 online) [S9]; tontine M 50–87 / F 50–86 [S10] | from 18 [S12] |
| Death benefit in deferral | 月払保険料 × 経過月数 [S2]; tontine 70% of premiums [S3] | 月払保険料 × 経過月数 [S4] | 既払込保険料相当額 [S6] | tontine: none — equals the surrender value [S10] | 死亡給付金 payable to the end of premium payment [S12] |
| Surrender ceiling | ≤ death benefit [S2]; tontine ≤ 死亡返還金 [S3] | ≤ death benefit; equal to it after a period [S4] | below premiums paid during premium payment [S6] | tontine: 70% suppression, always below premiums [S10] | exceeds premiums after a stated duration [S12] |
| 自動振替貸付 | **none on this product** [S2] | yes, compound, **capped at 8% p.a.** [S4] | not extracted | not extracted | not extracted |
| 契約者貸付利率 | not extracted | declared, reviewed each January and July [S4] | not extracted | **2.40%** for 2025-01-02+ contracts, by cohort back to 3.05% [S11] [S8] | not extracted |
| Published 予定利率 | not published on the retrieved documents | not published | **1.20% / 1.00%** by years to annuitisation; **0.65%** post-annuitisation [S5] | **1.00%** (from 0.60%) [S8] | rate-resetting, **minimum guarantee 0.50%** [S12] |
| Dividend chassis | 5年ごと配当 (tontine) [S3] | 5年ごと利差配当, from year 6 then every 5 years [S4] | 5年ごと利差配当 [S5] [S6] | not extracted | 金利キャッチアップ配当 [S12] |
| Distinctive feature | 年金の自動すえ置; a **published commutation factor table** [S2] | 複数年金選択制度 (split the fund across annuity types) [S4] | 据置期間 as an explicit annuity-increasing lever; 一括受取率 published [S6] | first annuity date deferrable by up to 5 years [S9] | 予定利率 refreshed once mid-contract with a floor [S12] |
| Underwriting | none [S2] [S3] | 無選択特則 optional; without it, a premium waiver applies [S4] | not extracted | 保険料払込免除特約 for the three major diseases [S9] | not extracted |

**What does not vary.** Every retrieved carrier: fixes the annuity at issue for a type
chosen at issue; suppresses the deferral-phase death benefit to (at most) premiums paid;
caps the surrender value at that death benefit; offers commutation of the remaining certain
or guaranteed instalments; states the same four tax-qualification conditions; and stops
policy loans and annuity reductions after annuitisation.

Most representative design for a reference implementation: a level-annual-premium
生存保障重視型 fixed deferred annuity with the 税制適格特約 attached; issue age in the 20–55
band; premiums to age 60; a 0–5 year 据置期間; annuity from 65; **10年確定年金** as the base
payout shape with 10年保証期間付終身年金 as the annuitisation election; deferral-phase death
benefit equal to cumulative premiums (monthly premium × elapsed months); surrender value
capped at that death benefit; a monthly grace running to the end of the following month; a
three-year reinstatement window; a three-year suicide exclusion; a policy loan at a declared
rate; and a commutation option at the present value of the unpaid instalments.

---

## Fetch failures and gaps

**URLs that could not be usefully retrieved**

- `https://www.sumitomolife.co.jp/lineup/select/other/fi/t_mirai_shinkin/ta3.pdf` [S7] —
  HTTP 200, 1.28 MB, 14 pp., but subset CID fonts with no ToUnicode map. `pypdf` and the
  markdown-converting fetcher both returned mojibake. **Lost:** the insurer's own
  契約概要／注意喚起情報 parameter table (issue-age table, premium minima, 年金原資 limits,
  suicide-exclusion period, reinstatement window). Substituted by the same insurer's product
  page [S6] and rate release [S5]; the missing items are carried from other carriers
  instead.
- `https://www7.tmn-anshin.co.jp/yakkan/pdf/A9902141102.pdf` [S14] — HTTP 200, 10.8 MB, 76
  pp., same font problem. **Lost:** a sixth carrier's 約款-level wording. No fact depends on
  it.
- `https://www.jp-life.japanpost.jp/products/clause/pdf/teiki-nenkin/201604/nenkin_2016_04_yakkan_1.pdf`
  [S15] — HTTP 200, 10 pp., same font problem. **Lost:** Japan Post Insurance's 定期年金保険
  wording. No fact depends on it.
- `https://www.sumitomolife.co.jp/lineup/select/other/fi/t_mirai/t_mirai.pdf` — HTTP **404**
  (`NoSuchKey`), although the URL appears in search results. Not used.
- `https://laws.e-gov.go.jp/api/2/keyword` — HTTP 404; `https://laws.e-gov.go.jp/api/2/laws`
  with `law_title=責任準備金` returned `total_count: 0`. FSA **告示** are not carried in e-Gov
  法令検索, so 平成8年大蔵省告示第48号 could not be read in consolidated form. Only its title,
  legal basis and the 2021 and 2016 amendments were retrieved [R6] [R7] [R8].
- The e-Gov HTML law viewer (`https://laws.e-gov.go.jp/law/...`) is JS-rendered and returns
  only navigation chrome to plain and browser-UA fetchers alike; the **e-Gov API v2**
  (`/api/2/law_data/<lawId>?response_format=json&law_full_text_format=json`) was used
  instead and returned complete, machine-readable statute text [R5] [R9] [R10].

**Claims left [unverified], and why**

- **The current numeric 標準利率 for annuity business.** The notification framework, its title,
  its legal basis, the 1 October 基準日 and the JGB-linked safety-factor construction are all
  verified [R5] [R6] [R7] [R8], but no retrieved document states the rate in force. Search
  snippets asserting 0.25% for 第一分野 level-premium business, and a separate quarterly rate
  for 一時払 products, were **not** confirmed against a retrieved FSA document. Any
  standard-rate figure used downstream must be marked **[std]** or `[unverified]` until the
  notification itself is retrieved.
- **The statutory basis of the "年金受取人 = 被保険者" condition.** Three of the five carriers
  state it [S1] [S4] [S9] [S10] [corrected 2026-08-20: "every carrier" over-counted — [S9]
  and [S10] are one carrier], but it does not appear in the retrieved text of 所法76⑧ [R9], 所令211/212
  [R10] or the NTA restatement [R12]. Its contractual status is fully sourced; its statutory
  status is `[unverified]`.
- **The commutation discount rate of ~0.40% p.a.** is *derived* by me from the published
  未払年金の現価 factors [S2], not published as a 予定利率. The factors themselves are sourced;
  the implied rate is an inference and must be tagged as such.
- **有期年金 as a currently sold shape.** JILI documents the type [R16] and one rider's wording
  contemplates 保証期間付有期年金 [S1], but no retrieved carrier product offers it today. Treat
  "有期年金 is sold in the current market" as `[unverified]`.
- **夫婦年金 mechanics at contract level.** JILI describes the shape [R16] and one carrier's
  booklet cross-references a 夫婦年金特約 and a 夫婦年金移行特約 with a 第１/第２被保険者 [S2],
  but the rider's own conditions live in a booklet that was not retrieved. Anything beyond
  "either spouse's survival keeps the annuity in payment, usually with a ~10-year guarantee"
  is `[unverified]`.
- **Third-carrier issue-age and premium-term envelopes.** 三井住友海上あいおい's numeric issue-age
  and annuity-start ranges were not located in the retrieved 140-page booklet (they sit in
  the 設計書, not the しおり). The envelope in §2 is therefore built from four carriers, not five.
- **Mortality improvement.** No Japanese analogue of a projection model was sought or
  retrieved. The 標準生命表 are static valuation tables [R2] [R3] [R4]; whether and how carriers
  project improvement for annuity pricing is `[unverified]` here.
- **Lapse by duration.** [R15] gives a single market-wide pre-annuitisation
  surrender-and-lapse rate of 3.4% for FY2024. A lapse curve by policy duration for
  individual annuity business is not public in any retrieved source.
- **Expense loadings and 三利源 splits.** No retrieved document discloses 予定事業費率 or a
  死差/利差/費差 decomposition for this product line.
- **一時払個人年金 rate levels.** [S13] gives single-premium rate *mechanics* for 養老 and 終身,
  not for annuity. Search snippets quoting 1.75%–2.08% for single-premium products in
  2025–26 are `[unverified]`; no annuity-specific single-premium 予定利率 was retrieved.
