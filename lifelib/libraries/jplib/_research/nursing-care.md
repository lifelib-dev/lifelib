# Nursing care insurance (介護保険, 公的介護保険連動型) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese private nursing-care (介護保険, *kaigo hoken*) liability cash flow
reference model — a third-sector (第三分野, *dai-san bun'ya*) product whose benefit trigger is
normally tied to the public long-term-care certification (公的介護保険連動型, *kōteki kaigo hoken
rendō gata*), paying a lump sum (介護一時金), an annuity (介護年金), or both, plus dementia (認知症) and
mild-cognitive-impairment (軽度認知障害 / MCI) covers.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually retrieved and read during
this session, or is tagged [unverified] where it is general knowledge, a secondary snippet,
or a figure that could not be confirmed against a retrieved document. Access date for all
fetched sources: 2026-08-20.

Seven carriers are represented (アフラック生命保険, 三井住友海上あいおい生命, 東京海上日動あんしん生命, 朝日生命, 第一生命, ジブラルタ生命,
太陽生命). Company and branded product names appear here and in `sources.md` only; every other
document in this product refers to a carrier by its [S#] tag.

---

## Primary sources

### S1 — アフラック生命保険, 「アフラックのしっかり頼れる介護保険」契約概要・注意喚起情報

- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: 「アフラックのしっかり頼れる介護保険」2025年11月版お申し込みいただく前に契約概要・注意喚起情報, document number
  **No.B25E206**, 12 pp. Formal product name: **介護保険〔無解約払戻金2021〕**
- Doc type: 契約締結前交付書面 (契約概要・注意喚起情報) — the pre-contract disclosure document
- URL: https://www.bank.aflac.co.jp/static/bank/r_kaigo/PDF/bank_r_kaigo_summary_2511.pdf
- Retrieved: YES (full PDF downloaded with a browser User-Agent, 12 pp., text extracted with
  `pdftotext -enc UTF-8` and read in full)
- Key content: the complete benefit table (要介護1一時金 / 要介護2一時金 / 介護年金) with the exact 支払事由
  wording, the two annuity-amount 型 (1型 / 2型) and their fractions of the 基準介護年金額, the
  10-payment annuity limit and contract extinction, 保険料払込免除 events, the 日常生活動作における要介護状態 and
  認知症による要介護状態 definitions, issue-age and amount limits, absence of 解約払戻金 and 契約者配当金,
  grace/lapse/復活, cooling-off.

### S2 — アフラック生命保険, 介護保険〔無解約払戻金2021〕ご契約のしおり・約款

- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款 booklet containing 介護保険〔無解約払戻金2021〕普通保険約款 plus attached 特約条項, 100 pp.
- Doc type: policy conditions (普通保険約款) with the ご契約のしおり front matter
- URL: https://www.aflac.co.jp/yakkan/bank/pdf/r_kaigo_27569800.pdf
- Retrieved: YES (full PDF downloaded, 100 pp. confirmed with pypdf, text extracted and the
  benefit, premium, lapse, reinstatement and surrender articles read)
- Key content: 第7条＜給付金の支払＞ verbatim (all three benefits, 支払額, 受取人, 免責事由); 保険料払込免除 article;
  第15条＜保険料払込の猶予期間および保険契約の失効＞; 第16条＜猶予期間中に保険事故が発生した場合＞; 第18条＜保険契約の復活＞; 第28条＜解約＞; 第30条＜解約
  払戻金＞ ("この保険契約の解約払戻金はありません"); 別表70 / 別表71 (the two company-basis care-state definitions).

### S3 — アフラック生命保険, 「アフラックのしっかり頼れる介護保険：保障内容」 (product page)

- Publisher: アフラック生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.aflac.co.jp/kaigo/r_kaigo/
- Retrieved: YES — **HTTP 403 to a plain fetcher; retrieved on the second attempt with a
  browser User-Agent** (HTTP 200, 119,877 bytes)
- Key content: the three-tier design in the carrier's own words (要介護1以上 → 一時金 and premium
  waiver; 要介護3以上 → 介護年金); the published sample plan (Aプラン: 基準介護年金額30万円 / 要介護1一時金10万円 /
  要介護2一時金10万円, 45歳, 保険期間・保険料払込期間終身); page currency note "2025年9月現在".

### S4 — 三井住友海上あいおい生命, 「&LIFE 介護保険Cセレクト」主契約の保障内容

- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: product page for the 主契約; formal product name **介護・認知症選択型保障保険（無解約返戻金型）無配当**
- Doc type: product page (consumer)
- URL: https://www.msa-life.co.jp/lineup/kaigo/main.html
- Retrieved: YES (HTTP 200 with browser User-Agent; HTML converted to text and read)
- Key content: five selectable 保険契約の型 — 要介護1一時金, 要介護2一時金, 要介護1年金, 要介護2年金, 認知症診断一時金 — each
  with its 支払事由 verbatim; the 5年確定年金 / 終身年金 election; premium waiver on the first annuity
  payment; the 認知症診断責任開始期 of 責任開始日から180日を経過した日の翌日（181日目）; the 5% post-premium-paying-period
  surrender value and the equal 死亡時返戻金; the 器質性認知症 definition.

### S5 — 三井住友海上あいおい生命, 「&LIFE 介護保険Cセレクト」オプション

- Publisher: 三井住友海上あいおい生命保険株式会社
- Doc type: product page (consumer), the 特則・特約 menu
- URL: https://www.msa-life.co.jp/lineup/kaigo/option.html
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: 軽度介護一時金給付特則 (要支援1以上); 軽度認知障害診断一時金給付特則 with the MCI definition and the same
  180-day 認知症診断責任開始期; the rule that paying either 特則 benefit extinguishes that 特則 (and stops
  its premium) but not the contract; 新保険料払込免除特約.

### S6 — 三井住友海上あいおい生命, 「&LIFE 介護保険Cセレクト」保障内容・保険料表

- Publisher: 三井住友海上あいおい生命保険株式会社 (きらめきライフダイレクト資料請求サイト)
- Doc type: product page with a published **premium rate table** by age and sex
- URL: https://www.kiramekilife-direct.jp/care/sample.html
- Retrieved: YES (HTTP 200 with browser User-Agent; the full rate table extracted)
- Key content: monthly premiums, 月払 (口座振替扱・クレジットカード扱), 保険期間・保険料払込期間終身, ages 15–69 for the
  direct channel (70歳以上は面談), for six product types at fixed benefit levels (一時金300万円 /
  年金60万円), male and female tables.

### S7 — 東京海上日動あんしん生命, 「あんしんねんきん介護」 (product page)

- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: product page for 介護年金保険（無解約返戻金型）[無配当]
- Doc type: product page (consumer)
- URL: https://www.tmn-anshin.co.jp/kojin/goods_kaigo/nenkin_kaigo/
- Retrieved: YES (HTTP 200 with browser User-Agent; HTML converted to text and read)
- Key content: 支払事由 (公的介護保険制度の要介護2以上と認定されたとき / 所定の要介護状態が 180日を超えて継続したと診断確定されたとき); annuity
  amounts and the three payout shapes (5年有期 / 10年有期 / 終身年金); the three-question simplified
  underwriting and its price — a **1-year 不担保期間**; premium waiver events; 健康祝金特則 (介護年金額の10%,
  5年ごと); 認知症一時金特約 splitting MCI 10% / 認知症 90%; 介護一時金特約; a published premium example table
  (male/female, ages 30–80).

### S8 — 朝日生命, 「あんしん介護介護一時金タイプ」 (product page)

- Publisher: 朝日生命保険相互会社
- Document: product page; formal product name **介護一時金保険（返戻金なし型）（2012）**
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/anshinkaigo/
- Retrieved: YES (fetched twice — once via WebFetch, once with a browser User-Agent to read
  the premium table verbatim)
- Key content: the split trigger — **要介護1以上 for premium waiver, 要介護3以上 for the lump sum**;
  初期介護一時金特約（返戻金なし型）paying at 要介護1以上 (face-to-face sales only); 契約年齢 40歳～79歳; 保険期間・保険料払込期間
  終身; published monthly premiums for a ¥3,000,000 lump sum by sex at ages 40–70; the note
  that 満64歳以下 are certified only for the 16 特定疾病.

### S9 — 朝日生命, 「あんしん介護要支援保険」 (product page)

- Publisher: 朝日生命保険相互会社
- Document: product page; 「要支援保険」は「軽度介護定期保険」「軽度介護終身保険（低解約返戻金型）」の愛称
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/anshinyoshien/
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: **要支援2以上** trigger for the 軽度介護保険金; maximum ¥2,000,000; issue ages 40–79
  (終身タイプ) / 40–75 (定期タイプ); the contract extinguishes on payment of the 軽度介護保険金, 死亡保険金 or
  高度障害保険金; published premiums for a ¥500,000 sum insured at ages 40–70 by sex; the
  low-surrender-value (低解約返戻金型) chassis on the whole-life form.

### S10 — 朝日生命, 「かなえる介護年金」 (product page)

- Publisher: 朝日生命保険相互会社
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/kanaerukaigo/
- Retrieved: YES (WebFetch, HTTP 200)
- Key content: **要介護3以上** trigger for the 介護年金; annuity up to ¥2,000,000; payout shapes 終身年金
  or 5 / 10 / 15-year 有期年金; issue ages 40–79; a 死亡給付金 equal to the first annuity instalment
  if the insured dies without ever receiving one; published monthly premiums for a ¥300,000
  annuity (male 40: ¥3,060 for 5年有期 to ¥7,746 for 終身; female 40: ¥3,021 to ¥10,740).

### S11 — 第一生命, 「要支援1から備えられる第一生命の要支援・介護保険」 (product page)

- Publisher: 第一生命保険株式会社 (the 要支援・介護保険 within the ジャスト product suite)
- Doc type: product page (consumer); page approval code (登)C25P0098（2025.6.6）
- URL: https://www.dai-ichi-life.co.jp/promotion/just/i01/index.html
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: the loosest trigger observed — **公的介護保険の要支援1以上と認定されたとき**, with a
  company-basis alternative of 第一生命が定める要介護状態が180日間継続した (stated to correspond to 要介護2以上); one
  payment only; 保険期間一生涯 (終身タイプ), 保険料払込期間終身払; **no death benefit**; issue restriction that
  applicants already applying for (or actively considering) certification, or living in a
  高齢者向け施設, cannot buy; 契約年齢が65歳以上の場合、保険金額は50万円まで.

### S12 — ジブラルタ生命, 「介護保障付終身保険（低解約返戻金型）〔無配当〕」商品パンフレット

- Publisher: ジブラルタ生命保険株式会社
- Document: 商品パンフレット, 2024年9月改訂版; premium table dated 2024年9月17日現在
- Doc type: 商品パンフレット (product brochure)
- URL: https://www.gib-life.co.jp/st/intro/products/pdf/kaigo_shushin_panf.pdf
- Retrieved: YES (full PDF downloaded, text extracted and read; the numeric tables are text,
  not images)
- Key content: the *accelerated-death-benefit* design of nursing care — 介護保険金 equal to **50%
  of the 保険金額**, paid on 公的介護保険制度の要介護2以上 (or, under 65, a company-basis care state
  continuing 180 days), after which the sum insured is reduced by the same amount, premiums
  are waived, and death/高度障害 cover continues for life; the 低解約返戻金型 rule (**surrender value
  during the premium-paying period is 70% of the ordinary value**); 介護保険金割増年金支払特約 converting
  the 介護保険金 into an enhanced annuity, with the higher 要介護4/要介護5 trigger for the top annuity
  and a 40歳以上 annuity commencement age; 保証金額付介護終身年金 and 10年保証期間付介護終身年金 shapes; 自動振替貸付,
  延長定期保険, 払済保険 and 減額 as the standard preservation options; a full **premium rate table** by
  issue age (20/30/40/50) × 保険料払込期間 (55/60/65/70/75/80/85/90歳満了) × sex for a ¥10,000,000 sum
  insured; the 省令 definition of 要介護2以上 cited in the contract itself; a worked 解約返戻金
  progression for the 30歳男性 / ¥10,000,000 / 60歳払込満了 example.

### S13 — 太陽生命, 「認知症保険」 (太陽生命ダイレクト product page)

- Publisher: 太陽生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.taiyo-seimei.co.jp/net_lineup/dementia_care/ninchi2/index.html
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: the three-layer dementia design — 軽度認知障害保険金 (¥10,000–¥300,000, fixed at 10%
  of the 認知症診断保険金), 認知症診断保険金 (¥100,000–¥3,000,000, on first-ever 器質性認知症 diagnosis), 認知症治療年金
  (¥40,000–¥2,000,000, payable when 所定の状態 has continued **180 days**, then annually while
  the insured survives); a **90-day** waiting period measured 契約日から起算して (benefits refused if
  the state existed within it).

### S14 — ジブラルタ生命, 「ご契約のしおり・約款介護年金移行特約」

- Publisher: ジブラルタ生命保険株式会社
- Document: ご契約のしおり・約款 booklet for the 介護年金移行特約, 24 pp. (file dated 201604)
- Doc type: policy conditions (特約条項)
- URL: https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/kaigo_nenkin_201604.pdf
- Retrieved: **NO** — the PDF downloaded cleanly (HTTP 200, 707,260 bytes, 24 pp.) but its
  text layer uses an embedded CID font that neither `pdftotext` (which reports `Syntax
  Error: Unknown character collection 'Adobe-Japan1'`) nor `pypdf` could decode; the
  extracted text is mojibake. **No fact in this file is sourced to S14.** The
  annuity-conversion mechanics are instead taken from the brochure [S12].

---

## Regulatory and actuarial references

### R1 — 介護保険法（平成9年12月17日法律第123号）

- Publisher: e-Gov 法令検索 (総務省行政管理局)
- Doc type: statute
- URL: https://laws.e-gov.go.jp/law/409AC0000000123 (retrieved through the e-Gov law API
  endpoint https://laws.e-gov.go.jp/api/1/lawdata/409AC0000000123)
- Retrieved: YES — **the HTML page at `laws.e-gov.go.jp/law/...` is a JavaScript shell and
  returns only ~800 bytes to a fetcher; the API endpoint returns the full law as XML**
  (1,904,648 bytes), which was converted to text and read
- Key content: 第1条 purpose; 第7条第1項 the definition of 要介護状態 (basic daily-living actions
  requiring constant care for a period fixed by 厚生労働省令, falling in one of the 要介護状態区分);
  第7条第2項要支援状態; 第7条第3項要介護者 = 要介護状態にある**六十五歳以上**の者, or 四十歳以上六十五歳未満 whose care state arises
  from a 特定疾病; 第9条 the two insured classes (第一号被保険者 = 65歳以上, 第二号被保険者 = 四十歳以上六十五歳未満の医療
  保険加入者); 第19条要介護認定 / 要支援認定; 第27条 the certification process — the decision is due within
  **30 days** of application and takes effect **retroactively to the application date**;
  第28条認定の有効期間 and 要介護更新認定.

### R2 — 要介護認定等に係る介護認定審査会による審査及び判定の基準等に関する省令

- Publisher: e-Gov 法令検索 (平成11年4月30日厚生省令第58号)
- Doc type: ministerial ordinance
- URL: https://laws.e-gov.go.jp/law/411M50000100058 (retrieved through
  https://laws.e-gov.go.jp/api/1/lawdata/411M50000100058)
- Retrieved: YES (API XML, 20,936 bytes, converted and read; the HTML page is a JS shell)
- Key content: the **quantitative definition of every certification band**, in 要介護認定等基準時間
  (the estimated daily minutes of care computed by the 厚生労働大臣-defined method from the
  74-item survey): 要支援1 = 25–32 min; 要支援2 = 32–50 min *with* the additional test that
  support would materially reduce or prevent worsening; 要介護1 = 32–50 min (excluding the 要支援2
  case); 要介護2 = 50–70 min; 要介護3 = 70–90 min; 要介護4 = 90–110 min; 要介護5 = 110 min or more. This
  is the ordinance cited by name inside a carrier's own contract wording [S12].

### R3 — 介護保険法施行令（平成10年政令第412号）第2条特定疾病

- Publisher: e-Gov 法令検索
- Doc type: cabinet order
- URL: https://laws.e-gov.go.jp/law/410CO0000000412 (retrieved through
  https://laws.e-gov.go.jp/api/1/lawdata/410CO0000000412)
- Retrieved: YES (API XML, 1,623,242 bytes, converted and read)
- Key content: the exhaustive list of **16 特定疾病** that alone can support certification of a
  第二号被保険者 (40–64): terminal cancer, 関節リウマチ, 筋萎縮性側索硬化症, 後縦靱帯骨化症, 骨折を伴う骨粗鬆症, 初老期における認知症,
  進行性核上性麻痺・大脳皮質基底核変性症・パーキンソン病, 脊髄小脳変性症, 脊柱管狭窄症, 早老症, 多系統萎縮症, 糖尿病性神経障害・腎症・網膜症, 脳血管疾患,
  閉塞性動脈硬化症, 慢性閉塞性肺疾患, 両側の膝関節または股関節の変形性関節症.

### R4 — 厚生労働省, 「令和5年度介護保険事業状況報告（年報）」報告書の概要

- Publisher: 厚生労働省老健局介護保険計画課
- Document: 報告書の概要 PDF (`r05_gaiyou.pdf`), position as at 令和6年3月末
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/dl/r05_gaiyou.pdf
- Retrieved: YES (PDF downloaded, text extracted, 第1表 and 第2表 read in full)
- Key content: 第1号被保険者数 35,890 thousand (前期高齢者 15,709 / 後期高齢者 20,181); 認定者数約708万人 (第1号
  6,952 thousand, 第2号 131 thousand); the **full 認定者数 cross-table by sex × 6 age bands × 7
  certification bands**; the certification-band mix; the statement that
  軽度（要支援1〜要介護2）は約66.0%.

### R5 — 厚生労働省, 「令和5年度介護保険事業状況報告（年報）」ポイント

- Publisher: 厚生労働省
- Document: ポイント PDF (`r05_point.pdf`)
- Doc type: official statistics (summary)
- URL: https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/dl/r05_point.pdf
- Retrieved: YES (PDF downloaded, text extracted and read; the age-split 認定率 appears only as
  a chart data series, so the two published split rates were cross-checked against the
  counts in R4 before being used)
- Key content: 認定率 (認定者 as a share of 第1号被保険者) rose 19.0% → **19.4%**; the long time series
  from 平成12年度 (13.9%); the 65–75 and 75+ series; サービス受給者数 (1-month average) 609万人.

### R6 — 厚生労働省, 「令和6年度介護給付費等実態統計の概況」

- Publisher: 厚生労働省
- Document: 統計の概要 (`01.pdf`) and 結果の概要 (`02.pdf`), covering 令和6年5月審査分〜令和7年 4月審査分
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kaigo/kyufu/24/index.html (PDFs at
  .../24/dl/01.pdf and .../24/dl/02.pdf)
- Retrieved: YES (both PDFs downloaded with a browser User-Agent, text extracted and read)
- Key content: the statistic is built from every 介護給付費明細書 in the 介護保険総合データベース, i.e. it is a
  claims-paid census, not a survey; 年間累計受給者数 68,597.3 thousand (+2.3% yoy) and 年間実受給者数
  6,754.0 thousand (+1.8%); the 令和6年4月/6月 fee revision of +1.59%.

### R7 — 日本アクチュアリー会, 「標準生命表2018」 (index page)

- Publisher: 公益社団法人日本アクチュアリー会
- Doc type: table library page
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Retrieved: YES (HTTP 200; the three linked PDFs enumerated and downloaded)
- Key content: the 2018 table family is published openly as `seimeihyo2018.pdf` (the
  numerical tables), `seimeihyo2018-gaiyo.pdf` (construction summary) and
  `seimeihyo2018-katei.pdf`. This open availability is the sharpest contrast with the
  subscriber-restricted CMI tables used by the UK section of this library.

### R8 — 日本アクチュアリー会, 「標準生命表2018」数表

- Publisher: 公益社団法人日本アクチュアリー会
- Document: 標準生命表2018 (numerical tables): 生保標準生命表2018（死亡保険用）男/女 and 第三分野標準生命表2018 男/女
- Doc type: actuarial table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Retrieved: YES (PDF downloaded, text extracted; individual `qx` values read off by
  locating the printed age labels, and each quoted value re-checked against its row
  position)
- Key content: `qx` and `ex` by age and sex for both tables. **第三分野標準生命表2018 is a mortality
  table only** — it contains no morbidity, incidence or care-state decrement.

### R9 — 日本アクチュアリー会, 「標準生命表2018の作成概要」

- Publisher: 公益社団法人日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要 (資料①〜⑤)
- Doc type: actuarial technical note
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Retrieved: YES (PDF downloaded, text extracted and the 第三分野 sections read)
- Key content: the 第三分野標準生命表2018 is graduated from **第21回生命表（2010年）**, i.e. the national
  life table, not insured experience — a deliberate change from the 2007 edition, which had
  used death-insurance experience because third-sector cover was then mostly sold as a
  rider; and **第三分野標準生命表2018 は高度障害を含まない死亡率である** (the 2007 edition did include 高度障害).

### R10 — 金融庁, 「第三分野の責任準備金積立ルール・事後検証等の概要について」

- Publisher: 金融庁
- Document: 別紙1-2 to the 2006-02-10 release
- Doc type: regulatory policy paper
- URL: https://www.fsa.go.jp/news/newsj/17/hoken/f-20060210-1/01_2.pdf
- Retrieved: YES (PDF downloaded, text extracted and read)
- Key content: the framework that governs reserving for this product. It states plainly that
  for 第三分野 "標準死亡率、参考純率といったスタンダードな指標が存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない"; requires
  標準責任準備金 plus annual **ストレステスト** (a per-product check that the 予定事故発生率 covers the 99th
  percentile of the incidence-rate risk over a **10-year** test horizon, with 危険準備金 topped
  up where it does not) and, where the 予定発生率 fails to cover the "通常の予測の範囲内のリスク" (defined at
  **97.7%**), a **負債十分性テスト** by future cash flow analysis; requires disclosure of the
  incidence model used; and requires a transparent numeric 基礎率変更権 exercise standard to be
  disclosed at point of sale.

### R11 — 国税庁, タックスアンサー No.1140「生命保険料控除」

- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: the post-2012 (新契約) three-basket regime — 新生命保険料, **介護医療保険料**, 新個人年金保険料 —
  each computed on the same schedule (≤¥20,000: full; ¥20,000–¥40,000: ½ + ¥10,000;
  ¥40,000–¥80,000: ¼ + ¥20,000; >¥80,000: flat **¥40,000**), with an overall cap of
  **¥120,000**; the rule that a contract mixing coverages is allocated to the basket of its
  主たる保障内容, and that rider premiums are allocated by the rider's own coverage.

### R12 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」

- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: the 介護医療保険契約等 basket covers contracts written on or after 2012-01-01 paying
  on 疾病または身体の傷害等 where payment is triggered by a 医療費支払事由; contracts with a term under 5
  years and savings-type contracts are excluded; beneficiaries must all be the premium
  payer, spouse or a relative.

### R13 — 厚生労働省, 「第23回生命表（完全生命表）の概況」

- Publisher: 厚生労働省政策統括官付参事官付人口動態・保健社会統計室 (published 令和4年3月2日)
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/life/23th/dl/23th-11.pdf
- Retrieved: YES (PDF downloaded, text extracted and read)
- Key content: 第23回（令和2年）完全生命表 — 平均寿命男 **81.56** / 女 **87.71**; 平均余命 at 20 (男61.90 /
  女68.01), at 65 (男 **19.97** / 女 **24.88**), at 75 (男12.54 / 女16.22); the full time series
  back to 第22回（平成27年）(男80.75 / 女86.99). The 完全生命表 is produced once every five years off the
  国勢調査 year; the 簡易生命表 fills the intervening years.

### R14 — 生命保険文化センター, 「2024（令和6）年度生命保険に関する全国実態調査＜速報版＞」

- Publisher: 公益財団法人生命保険文化センター (2024年11月)
- Doc type: household survey report
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Retrieved: YES (PDF downloaded, text extracted, the care and product-penetration sections
  read)
- Key content: 民保加入世帯 (excluding かんぽ生命) penetration — **介護保険・介護特約 20.1%** (前回 16.7%) and
  **認知症保険・認知症特約 7.6%** (前回 6.6%), against 医療保険・医療特約 95.1% and ガン保険・ガン特約 68.2%; 介護給付金月額
  average ¥92,000 (世帯主) / ¥65,000 (配偶者); **介護期間 average 55.0 months (4年7か月)**, distribution
  4–10年 27.9%, 2–3年 16.5%, 1–2年 15.0%, 10年以上 14.8%; 介護費用 monthly average **¥90,000**,
  one-off total average **¥472,000**; the most recent certification band among those cared
  for was 要介護3 (20.7%), then 要介護2 (17.6%), then 要介護4 (17.5%); 91.9% had used public
  long-term-care services.

### R15 — 生命保険文化センター, 「介護保険」（生命保険の種類・主契約の種類）

- Publisher: 公益財団法人生命保険文化センター
- Doc type: consumer-education reference on product design
- URL: https://www.jili.or.jp/knows_learns/kind/main/14.html
- Retrieved: YES (WebFetch, HTTP 200)
- Key content: the market-level taxonomy — benefits are 介護一時金, 介護年金, 死亡保険金, 高度障害保険金;
  triggers are either a company basis (daily-living-action dependency, or dementia with
  見当識障害) **that has persisted for a fixed period such as 180 days**, or a
  public-certification link at 要介護3以上 / 要介護2以上 / 要介護1以上; terms come as 有期型 or 終身型, with 有期払
  or 終身払 premiums.

### R16 — 生命保険文化センター, 「介護や支援が必要な人はどれくらい？」

- Publisher: 公益財団法人生命保険文化センター
- Doc type: statistical digest of 介護保険事業状況報告
- URL: https://www.jili.or.jp/lifeplan/lifesecurity/1119.html
- Retrieved: YES (HTTP 200 with browser User-Agent)
- Key content: certified persons grew from about 2.56 million in 平成12年度 (the first year of
  the public scheme) to about 7.08 million in 令和5年度 — roughly **2.8×** in 23 years; the band
  with the largest count is 要介護1 (1.464 million).

---

## Fact extraction

### 1. What the product is, and where it sits

- 介護保険 is 第三分野 business — the FSA groups 医療保険, がん保険 and 介護保険 together as
  "疾病や傷害を事由とした保険金や治療のための給付金が支払われる分野" [R10].
- Unlike 医療保険, the benefit is **not** a `daily amount × days` structure. Every product
  examined pays either a lump sum on entering a defined care state, an annuity while the
  state persists, or both [S1] [S4] [S7] [S8] [S12] [R15]. The modelling shape is therefore
  *incidence into an absorbing (or annually re-tested) state*, not frequency × severity ×
  limit.
- Two chassis are in the market:
  - **stand-alone third-sector cover** with no death benefit and (usually) no surrender
    value — アフラック [S1] [S2], 三井住友海上あいおい生命 [S4], 東京海上日動あんしん生命 [S7], 朝日生命 [S8] [S9] [S10],
    第一生命 [S11] (which states explicitly 死亡保障はありません);
  - **an accelerated benefit on a whole-life contract** — ジブラルタ生命's 介護保障付終身保険 pays 介護保険金 =
    50% of the sum insured, reduces the sum insured by the same amount, waives future
    premiums, and continues death/高度障害 cover for life [S12].
- Household penetration: 民保加入世帯 (excl. かんぽ生命) hold 介護保険・介護特約 at **20.1%** and 認知症保険・認知症特約 at
  **7.6%**, both up on the previous survey (16.7% / 6.6%) [R14]. For scale, 医療保険・医療特約 is at
  95.1% and ガン保険・ガン特約 at 68.2% [R14].

### 2. The public scheme the trigger is wired to

- 介護保険法 covers two insured classes: **第一号被保険者** = residents aged 65 and over, and
  **第二号被保険者** = residents aged 40–64 who are 医療保険加入者 [R1, 第9条].
- A 第二号被保険者 can be certified **only** where the care state arises from one of the 16
  **特定疾病** [R1, 第7条第3項; R3, 第2条]. A carrier's own consumer page states the same restriction
  in plain terms [S8]. This is why every company-basis alternative trigger in this product
  class is written for 満65歳未満 lives (§4).
- Seven bands: 要支援1, 要支援2, 要介護1–5 [R1, 第7条; R2, 第1条・第2条]. The bands are defined
  quantitatively in **要介護認定等基準時間** (estimated minutes of care per day, computed by the
  厚生労働大臣-defined method from the 74-item assessment) [R2, 第3条]:

  | Band | 要介護認定等基準時間 | Extra test |
  |---|---|---|
  | 要支援1 | 25–32 min | — |
  | 要支援2 | 32–50 min | support materially reduces or prevents worsening |
  | 要介護1 | 32–50 min | (the 要支援2 case excluded) |
  | 要介護2 | 50–70 min | — |
  | 要介護3 | 70–90 min | — |
  | 要介護4 | 90–110 min | — |
  | 要介護5 | 110 min and over | — |

  Note the overlap: 要支援2 and 要介護1 share the same 32–50 minute band and are separated only by
  the improvement-potential test [R2]. A model that treats the certification scale as a
  clean severity ladder is wrong at exactly the point where several products place their
  trigger.
- Certification is a municipal administrative act: the decision is due **within 30 days** of
  application and takes effect **retroactively to the application date** [R1, 第27条]. It has
  a finite 有効期間 fixed by 厚生労働省令 and must be renewed (要介護更新認定); the band can move up or down
  at renewal [R1, 第28条].
- Certified persons at 令和6年3月末: **about 7.08 million** in total, of which 6,952 thousand are
  第一号被保険者 and 131 thousand are 第二号被保険者 [R4]. Growth since the scheme began is about **2.8×**
  (≈2.56 million in 平成12年度) [R16].

### 3. The public incidence data — the directly usable basis

This is the sharpest advantage the Japanese market has over the UK and US sections of this
library: the certification counts are a national census, published annually, split by sex,
age band and severity band.

**認定者数 at 令和6年3月末, thousands, from 第2表** [R4]:

| Band | Male 第1号 | Female 第1号 | Total (incl. 第2号) | Share |
|---|---|---|---|---|
| 要支援1 | 322 | 685 | 1,020 | 14.4% |
| 要支援2 | 285 | 691 | 996 | 14.1% |
| 要介護1 | 478 | 966 | 1,464 | 20.7% |
| 要介護2 | 402 | 762 | 1,191 | 16.8% |
| 要介護3 | 295 | 614 | 927 | 13.1% |
| 要介護4 | 252 | 626 | 895 | 12.6% |
| 要介護5 | 153 | 420 | 590 | 8.3% (derived) |
| Total | 2,188 | 4,764 | 7,083 | 100.0% |

Two caveats on the arithmetic. First, the source rounds to thousands and warns that
「数値は、千人未満を四捨五入しているため、計に一致しない場合がある」, so column sums differ from the printed totals by up to a
few thousand — the narrative total in the same document is 約708万人 [R4] against the 7,083
that the printed cells sum to. Second, the 要介護5 share is the one figure derived rather than
printed: the counts are printed [R4] but the 構成比 cell is truncated in the extracted text;
8.3% is the residual and is consistent with the printed male 7.2% / female 8.9% sub-shares.

Three ratios fall straight out and are the ones a pricing model needs:

- **要介護2以上 = 50.8%** of all certified persons (16.8 + 13.1 + 12.6 + 8.3) [R4 derived]. A
  carrier's own brochure states the same 50.8% figure for an earlier year [S12].
- **要介護3以上 = 34.0%** [R4 derived].
- **要介護1以上 = 71.5%**; 軽度（要支援1〜要介護2）= about **66.0%**, stated directly [R4].

**認定者数 by age band, 第1号被保険者 only, thousands** [R4]:

| Age band | Male | Female | Total |
|---|---|---|---|
| 65–70 | 110 | 90 | 200 |
| 70–75 | 237 | 243 | 480 |
| 75–80 | 355 | 506 | 861 |
| 80–85 | 509 | 1,009 | 1,518 |
| 85–90 | 537 | 1,327 | 1,864 |
| 90+ | 439 | 1,589 | 2,028 |

The age gradient is steep and the sex gradient reverses with age: below 75 the counts are
roughly equal by sex, and at 90+ women outnumber men **3.6 : 1** [R4 derived].

**認定率** (certified as a share of 第一号被保険者) [R4] [R5]:

- overall **19.4%** at 令和6年3月末, up from 19.0% a year earlier and from 13.9% in 平成12年度 [R5];
- 前期高齢者 (65–74): 680 thousand certified out of 15,709 thousand = **4.3%** [R4 derived, and
  the same value appears as the terminal point of the 65歳以上75歳未満 series in R5];
- 後期高齢者 (75+): 6,270 thousand out of 20,181 thousand = **31.1%** [R4 derived, matching the
  75歳以上 series terminal point in R5].

Claim volume, for a sanity check on utilisation rather than incidence: 年間実受給者数 **6,754.0
thousand** and 年間累計受給者数 68,597.3 thousand in 令和6年度, drawn from every claim record in the
介護保険総合データベース [R6].

### 4. Benefit triggers — the heart of the product

Every product observed writes the trigger as an **either/or**: the public certification,
*or* a company-defined care state that has persisted for a stated number of days. The
company-basis limb exists because a life under 65 can only be certified for one of the 16
特定疾病 [R1] [R3], so four of the seven carriers restrict that limb to 満65歳未満 lives.

**Public-certification limb — the observed range of thresholds:**

| Threshold | Carrier and benefit |
|---|---|
| 要支援1以上 | 第一生命 要支援・介護保険 (主契約) [S11]; 三井住友海上あいおい生命 軽度介護一時金給付特則 [S5] |
| 要支援2以上 | 朝日生命 あんしん介護 要支援保険 [S9] |
| 要介護1以上 | アフラック 要介護1一時金 + 保険料払込免除 [S1] [S2]; 三井住友海上あいおい生命 要介護1一時金 / 要介護1年金 [S4]; 朝日生命 初期介護一時金特約 + 保険料払込免除 [S8] |
| 要介護2以上 | アフラック 要介護2一時金 [S1] [S2]; 三井住友海上あいおい生命 要介護2一時金 / 要介護2年金 [S4]; 東京海上日動あんしん生命 介護年金 [S7]; ジブラルタ生命 介護保険金 [S12] |
| 要介護3以上 | アフラック 介護年金 [S1] [S2]; 朝日生命 あんしん介護 介護一時金 [S8]; 朝日生命 かなえる介護年金 [S10] |
| 要介護4 / 要介護5 | ジブラルタ生命 介護保険金割増年金支払特約, top annuity tiers [S12]; アフラック 介護年金 amount tiers [S1] |

要介護2以上 is the modal single threshold and is the one 公的介護保険連動型 usually means; but the full
observed spread runs from 要支援1 to 要介護3, and one carrier grades the payout across 要介護3/4/5
rather than switching it on at one band [S1] [S12].

**Company-basis limb (保険会社独自基準) — the exact wording and durations:**

- アフラック, 別表70 「日常生活動作における要介護状態」: both (1) at least one of ①寝返り②歩行 is "全部介助を要する状態", **and**
  (2) at least two of ①衣服の着脱②入浴③食物の摂取④排泄 are "一部介助" or "全部介助", and the insured requires
  another person's care. Must have **continued 180 days or more** and be diagnosed by a
  physician; available only where the insured is **満65歳未満** [S1] [S2]. The document states
  explicitly that 「日常生活動作における要介護状態」の判定基準は、公的介護保険制度の要介護認定基準とは異なります [S1].
- アフラック, 別表71 「認知症による要介護状態」: 器質性認知症と診断され、意識障害のない状態において見当識障害がある状態. 器質性認知症 requires (1) an
  acquired organic lesion or damage in the brain and (2) persistent, global loss of
  already-acquired intelligence caused by it. 見当識障害 is satisfied by any one of a permanent
  time-orientation defect, a place-orientation defect, or a person-orientation defect, each
  spelled out. Must have **continued 90 days or more**; 満65歳未満 only [S1] [S2].
- 三井住友海上あいおい生命: 約款所定の「日常生活介護状態」 (for the 要介護1 types) or 「生活介護状態」 (for the 要介護2 types)
  continuing **180日以上**, 満65歳未満 only [S4]. The carrier uses two differently named states so
  that the company limb lines up with the two different public thresholds.
- ジブラルタ生命: ジブラルタ生命所定の要介護状態 continuing **180日以上**, 満65歳未満 only. The state is defined as (1)
  ❶歩行 or ❷寝返り at 全部介助または一部介助, **and** (2) among four further items either one 全部介助 plus one
  全部/一部介助, or three at 全部/一部介助, requiring another person's care. 歩行 is operationalised as
  whether the insured can walk 5 m or more from standing [S12].
- 東京海上日動あんしん生命: 所定の要介護状態が **180日を超えて** 継続したと診断確定されたとき — note "超えて", not "以上", and **no age
  restriction on the company limb** [S7].
- 第一生命: 第一生命が定める要介護状態が **180日間継続** した, stated by the carrier to correspond to 要介護2以上; **no
  age restriction stated** [S11].
- 太陽生命 認知症治療年金: 器質性認知症に該当し、所定の状態が **180日継続** したとき [S13].

So 180 days is the market convention for a physical care state; 90 days is the convention
for a dementia-defined care state [S1] [S2]; and 東京海上日動あんしん生命's "180日を超えて" is a strictly
tighter form of the same test [S7].

Where both limbs are met, the contract picks one: アフラック pays the amount for the public limb
(ア) where (ア) and (イ) both apply [S1].

### 5. Lump sum vs annuity, and how the annuity is metered

- **Lump sum only**: 朝日生命 あんしん介護 介護一時金タイプ [S8]; 朝日生命 要支援保険 [S9]; 第一生命 要支援・介護保険 (お支払いは1回限り)
  [S11].
- **Annuity only**: 東京海上日動あんしん生命 あんしんねんきん介護 [S7]; 朝日生命 かなえる介護年金 [S10].
- **Both, tiered**: アフラック — 要介護1一時金 and 要介護2一時金 each once only, then the 介護年金 from 要介護3以上
  [S1] [S2]. If the annuity starts before either lump sum has been paid, the unpaid lump
  sums are paid **together with the first annuity instalment** [S1].
- **Either, elected at issue**: 三井住友海上あいおい生命 sells five mutually exclusive 保険契約の型 — 要介護1一時金,
  要介護2一時金, 要介護1年金, 要介護2年金, 認知症診断一時金 — and the 型 cannot be changed mid-term [S4] [S6].

Annuity metering — the single most model-relevant divergence:

- **アフラック: state-tested annually, capped at 10 payments.** The 介護年金支払基準日 is the date the
  trigger was first met and then its annual anniversaries. Each instalment requires the
  insured to *still be* in the state on that date (要介護3以上, or the company-basis state
  continuing). At most one payment per year and **at most 10 over the whole contract**; on
  the 10th payment the contract is extinguished retroactively to the date that 10th
  payment's trigger was met. If the state lapses and the insured later re-qualifies, a
  **new** 介護年金支払基準日 is set. Two amount profiles are sold [S1] [S2]:

  | Certification | 1型 | 2型 |
  |---|---|---|
  | 要介護5 | 基準介護年金額 | 基準介護年金額 |
  | 要介護4 | × 5/6 | × 2/3 |
  | 要介護3 | × 4/6 | × 1/3 |
  | company-basis limb | × 4/6 | × 1/3 |

  There is a **relief on the age condition**: if the insured qualified under the company
  limb while under 65, the age-under-65 condition is not re-applied to instalments 2 onwards
  once the insured passes 65, provided the state continues [S1].
- **三井住友海上あいおい生命: 5年確定年金 or 終身年金, elected at issue.** Instalments 2 onwards fall on the
  annual anniversary of the first payment date; on the 終身年金 basis the only test is
  **生存している限り** — no re-testing of the care state. The remaining instalments may be commuted
  to a lump sum at their present value, which the carrier states will be less than the
  undiscounted total [S4].
- **東京海上日動あんしん生命: 5年有期 / 10年有期 / 終身年金.** Once the trigger has been met the annuity is paid
  for the whole payout period **while the insured survives**, and the carrier states
  explicitly that recovery does not stop it — 「介護年金のお支払事由に該当した後、容体が
  改善した場合」も年金支払期間中、生存されている限りお受け取りいただけます, and the premium waiver likewise stays in force [S7].
- **朝日生命 かなえる介護年金: 終身年金 or 5 / 10 / 15年有期年金** [S10].
- **ジブラルタ生命: annuity by conversion.** The 介護保険金 (a lump sum) can be taken as an enhanced
  annuity under the 介護保険金割増年金支払特約, in 保証金額付介護終身年金 or 10年保証期間付介護終身年金 form; the annuity
  commencement age must be **40 or over**, and the top enhanced tier requires 要介護4 or 要介護5
  [S12].

The distinction matters enormously: a *survival-tested* annuity (三井住友海上あいおい生命, 東京海上日動あんしん生命,
朝日生命, ジブラルタ生命) is a life annuity conditional on one-time entry and needs only an
impaired-life mortality basis after entry, whereas a *state-tested* annuity (アフラック) needs a
recovery/persistency decrement as well, plus the 10-payment cap.

### 6. Dementia and MCI covers

- **三井住友海上あいおい生命**: 認知症診断一時金 as a main-contract 型 — payable on the first diagnosis of
  約款所定の器質性認知症 after the 認知症診断責任開始期, once per contract [S4]. 器質性認知症 examples given:
  アルツハイマー病の認知症, 血管性認知症, レビー小体型認知症. Diagnosis "は、認知機能検査および画像検査によってなされる必要があります", with a
  reasonable-grounds fallback where those tests cannot be performed [S4]. 軽度認知障害診断一時金給付特則
  pays on first MCI diagnosis; MCI is defined as
  「日常生活動作は自立しているものの、認知機能が低下し、認知機能領域の障害が認められる状態」 [S5]. Paying either 特則 benefit extinguishes
  that 特則 (and its premium) but leaves the contract in force; if the main benefit triggers
  first and the 特則 benefit has not been paid, both are paid together [S5].
- **東京海上日動あんしん生命 認知症一時金特約**: a single 認知症一時金額 (¥200,000–¥2,000,000, ¥100,000 steps) split
  **10% on first MCI diagnosis / 90% on first dementia diagnosis**; if dementia is diagnosed
  first with no prior MCI claim, both parts are paid together. The 認知症一時金特約 and 介護一時金特約
  amounts are capped at **¥2,000,000 combined** [S7].
- **太陽生命**: three layers on one contract — 軽度認知障害保険金 fixed at **10% of the 認知症診断保険金**
  (¥10,000–¥300,000), 認知症診断保険金 ¥100,000–¥3,000,000 on first-ever 器質性認知症, and 認知症治療年金
  ¥40,000–¥2,000,000 payable once the 所定の状態 has continued **180 days**, then annually on
  survival [S13].
- **アフラック** does not sell a separate dementia benefit on this contract; instead dementia
  enters through the 認知症による要介護状態 company-basis limb of the same three benefits, with its own
  **90-day** duration test [S1] [S2].
- **朝日生命** sells dementia as a separate product (あんしん介護 認知症保険), issue ages **40–75** against
  40–79 for the care products [S8].

The MCI benefit is uniformly a **small fraction of the dementia amount** — 10% at two
carriers, by explicit design [S7] [S13] — and is uniformly **once only, and extinguishing**
for its own benefit line [S5] [S7].

### 7. Waiting periods, 免責期間 and 不担保期間

Waiting-period practice is the least uniform part of the product, and the range is wide:

| Carrier | Waiting rule |
|---|---|
| アフラック | **No stated waiting period on the care benefits.** Protection instead runs through the 責任開始期前 rule: nothing is paid where the certification or the company-basis state results from an illness contracted, or an accident occurring, before the 責任開始期(日) [S1] [S2] |
| 三井住友海上あいおい生命 | Care benefits: no waiting period stated. **Dementia and MCI: 認知症診断責任開始期 = 責任開始日からその日を含めて180日を経過した日の翌日（181日目）** [S4] [S5] |
| 東京海上日動あんしん生命 | **1-year 不担保期間 on every benefit** (介護年金 and 特約一時金), starting cover at the 契約日の1年後の応当日 — the explicit price of the three-question simplified underwriting. The 責任開始期前 rule also applies, with a carve-back: a complication arising **2 years or more** after the 責任開始期 from a non-disclosable pre-existing illness is covered [S7] |
| 太陽生命 | **90 days from the 契約日**: no 軽度認知障害保険金 if MCI or 器質性認知症 existed within it; no 認知症診断保険金 or 認知症治療年金 if 器質性認知症 existed within it [S13] |

Note the vocabulary distinction that a drafter must not blur: 免責期間 / 待ち期間 in the sense of
"cover has not started yet" (東京海上日動あんしん生命's 1-year 不担保期間 [S7]; 三井住友海上あいおい生命's 180-day
認知症診断責任開始期 [S4]; 太陽生命's 90 days [S13]) is a different mechanism from the **duration test
inside the trigger** — the 180 days or 90 days for which a company-basis care state must
have *persisted* before it counts [S1] [S2] [S4] [S7] [S11] [S12] [S13]. Both appear as
"180日" in marketing copy and they are not the same thing.

### 8. Terms, issue ages, amount limits

| Carrier / product | 保険期間 | 保険料払込期間 | 契約年齢 | Amount limits |
|---|---|---|---|---|
| アフラック 介護保険〔無解約払戻金2021〕 [S1] | 終身 | 終身払 | 満18歳～満79歳 | 基準介護年金額 ¥300,000–¥1,200,000 (¥60,000 steps); 要介護1一時金額 and 要介護2一時金額 each ¥100,000–¥1,000,000 (¥10,000 steps) |
| 三井住友海上あいおい生命 介護保険Cセレクト [S4] [S6] | 終身 | 終身 (a shorter 払込期間 exists — the 5% surrender value is conditional on it) | 15–69 on the direct channel; 70+ face-to-face | published rate table at 一時金 ¥3,000,000 / 年金 ¥600,000 |
| 東京海上日動あんしん生命 あんしんねんきん介護 [S7] | 終身 | 終身 | premium table published for ages 30–80 | 介護年金額 ¥200,000–¥1,000,000 (ages 20–60) or ¥200,000–¥500,000 (ages 61–80), ¥100,000 steps; 認知症一時金 and 介護一時金 ¥200,000–¥2,000,000 each, **¥2,000,000 combined** |
| 朝日生命 あんしん介護 介護一時金タイプ [S8] | 終身 | 終身 | 40–79 | ¥500,000–¥3,000,000 on the postal plan |
| 朝日生命 要支援保険 [S9] | 終身 or 定期 | — | 40–79 (終身), 40–75 (定期) | 軽度介護保険金 up to ¥2,000,000 |
| 朝日生命 かなえる介護年金 [S10] | 終身 | 終身 | 40–79 | 介護年金 up to ¥2,000,000 |
| 第一生命 要支援・介護保険 [S11] | 一生涯 (終身タイプ) | 終身払 | — | **65歳以上の契約は保険金額50万円まで** |
| ジブラルタ生命 介護保障付終身保険 [S12] | 終身 | 55/60/65/70/75/80/85/90歳満了 | rate table published at 20/30/40/50 | 介護保険金 = 50% of the 保険金額 |
| 太陽生命 認知症保険 [S13] | — | — | — | 認知症診断保険金 ¥100,000–¥3,000,000; 軽度認知障害保険金 = 10% of it; 認知症治療年金 ¥40,000–¥2,000,000 |

Every stand-alone product observed is written **whole-of-life with whole-of-life premiums**,
and issue ages cluster at 40 (the age at which public cover itself begins [R1, 第9条]) to
about 79 [S8] [S9] [S10]. アフラック's 18 [S1] and 三井住友海上あいおい生命's 15 [S6] are the outliers at the
young end. The two exceptions to whole-of-life are 朝日生命's 定期 variant of the 要支援保険 [S9] and
ジブラルタ生命's limited-pay whole life [S12].

Underwriting is tight at the front door: アフラック will not accept anyone currently
hospitalised, advised to be hospitalised or operated on, **or who has ever been certified
for, or has ever applied for, 要支援 or 要介護** [S1]. 第一生命 refuses applicants already applying
for certification, actively considering it, or living in a 高齢者向け施設 [S11]. 東京海上日動あんしん生命 asks
only three questions, one of which is whether the applicant has ever applied for
certification and another whether they have ever been examined or treated for 認知症, MCI, or a
suspicion of either — and prices that leniency with the 1-year 不担保期間 [S7].

### 9. Premium structure and published rates

- Premiums are level, 平準払, determined by **sex and 契約日における満年齢** [S1]. Payment modes offered
  by アフラック are 月払 / 半年払 / 年払 [S1]; on 半年払・年払 an unearned-premium refund of the unexpired
  whole months is made when premiums cease mid-period [S1].
- **保険料払込免除** is a defining feature, and it usually triggers at a *lower* care state than
  the main benefit:
  - アフラック: waiver on the **要介護1一時金** trigger, or 高度障害状態, or a 身体障害状態 reached within 180 days
    of an accident. Waived premiums are treated as though paid on each 払込期月の契約応当日; while
    waived, the mode cannot be changed and the sum insured cannot be reduced [S1] [S2].
  - 朝日生命: waiver at **要介護1以上**, against a 要介護3以上 lump-sum trigger [S8].
  - 三井住友海上あいおい生命: waiver on the **first annuity instalment** [S4]; a separate 新保険料払込免除特約
    extends waiver to a listed disease range [S5].
  - 東京海上日動あんしん生命: waiver on the 介護年金 trigger, 高度障害, or an accident-caused 身体障害 within 180
    days; main-contract waiver carries the riders' premiums too [S7].
  - ジブラルタ生命: waiver on payment of the 介護保険金, and (with the 疾病障害による保険料払込免除特約, priced
    separately) on a disease-caused 身体障害状態 [S12].
- **Published monthly premium rates** (all figures ¥, 月払, from the carriers' own tables):

  三井住友海上あいおい生命, 終身 / 終身払, 要介護2一時金額 ¥3,000,000 (介護一時金Ⅱ型) [S6]:

  | Age | Male | Female |
  |---|---|---|
  | 40 | 2,550 | 2,790 |
  | 50 | 3,600 | 4,080 |
  | 60 | 5,820 | 6,690 |
  | 65 | 8,220 | 9,480 |
  | 69 | 11,130 | 12,870 |

  Same source, 要介護2年金額 ¥600,000 (介護年金Ⅱ型), showing the cost of the 終身年金 election [S6]:

  | Age | Male 5年確定 | Male 終身 | Female 5年確定 | Female 終身 |
  |---|---|---|---|---|
  | 40 | 2,484 | 3,906 | 2,748 | 6,450 |
  | 60 | 5,730 | 7,692 | 6,600 | 13,506 |
  | 69 | 10,968 | 13,572 | 12,696 | 24,348 |

  朝日生命 あんしん介護 介護一時金タイプ, 介護一時金額 ¥3,000,000, 終身 / 終身払 [S8]: male 40 ¥2,202 / 50 ¥3,435 / 60
  ¥5,817 / 70 ¥10,764; female 40 ¥2,547 / 50 ¥3,870 / 60 ¥6,522 / 70 ¥12,693.

  朝日生命 要支援保険 (軽度介護終身保険（低解約返戻金型）), 保険金額 ¥500,000 [S9]: male 40 ¥1,192 / 60 ¥2,369 / 70
  ¥3,994; female 40 ¥1,126 / 60 ¥2,185 / 70 ¥3,794.

  東京海上日動あんしん生命 あんしんねんきん介護, 10年有期年金, 健康祝金特則付, 介護年金額 ¥300,000 [S7]: male 30 ¥1,758 / 40 ¥2,082
  / 50 ¥2,670 / 60 ¥3,960 / 70 ¥7,287 / 80 ¥16,218; female 30 ¥2,280 / 40 ¥2,745 / 50 ¥3,636
  / 60 ¥5,589 / 70 ¥11,196 / 80 ¥24,363. At 介護年金額 ¥500,000 the premiums scale exactly 5/3
  (male 40 ¥3,470, female 40 ¥4,575) [S7].

  ジブラルタ生命 介護保障付終身保険, 保険金額 ¥10,000,000 (so 介護保険金 ¥5,000,000), by 払込期間 [S12], male: age 20 —
  55歳満了 ¥20,210, 60歳満了 ¥18,000, 90歳満了 ¥13,130; age 30 — ¥29,150 / ¥24,710 / ¥16,220; age 40
  — ¥50,440 / ¥38,480 / ¥21,060; age 50 — 55歳満了 not offered, 65歳満了 ¥54,670, 90歳満了 ¥29,150.
  Female rates are uniformly lower, e.g. age 30 60歳満了 ¥23,800 against ¥24,710.

  Two structural facts fall out of these tables and belong in any calibration: **(a)** on
  the lump-sum shapes female rates exceed male at every age (the ratio is about 1.09–1.16
  [S6] [S8]), the reverse of a death-benefit product; **(b)** the female loading explodes on
  the 終身年金 shape — female 終身 is about 1.65× male at age 40 and 1.79× at age 69 [S6] —
  because it compounds higher care incidence with much longer post-onset survival.
  Interestingly the low-severity 要支援2 whole-life product runs the *other* way, female
  slightly cheaper than male [S9], which is consistent with mortality dominating incidence
  at that trigger.
- Nobody publishes 予定発生率, 予定利率 or 予定死亡率 for this product. The FSA framework confirms there
  is nothing standard to publish: for 第三分野「標準死亡率、参考純率といったスタンダードな
  指標が存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 [R10].

### 10. Surrender values, dividends, death benefits

- **アフラック**: 第30条 — 「この保険契約の解約払戻金はありません」; and there are no 契約者配当金 [S1] [S2]. The product
  name itself carries the fact: 介護保険〔**無解約払戻金** 2021〕.
- **東京海上日動あんしん生命**: 無解約返戻金型, stated on the product page [S7].
- **朝日生命 あんしん介護 介護一時金タイプ**: 介護一時金保険（**返戻金なし型**）(2012) [S8]; 初期介護一時金特約 likewise 返戻金なし型 [S8].
- **三井住友海上あいおい生命**: no surrender value during the premium-paying period. Where the 払込期間 is
  shorter than the 保険期間 and all premiums have been paid, a surrender value of **5% of the
  elected benefit amount** becomes available after 払込満了 — but only before the main benefit
  has triggered. A **死亡時返戻金 equal to the surrender value** is paid on death (so nil during
  the premium-paying period). Paying a 軽度介護一時金 or 軽度認知障害診断一時金 does not destroy the surrender
  value. Riders carry no surrender value at all [S4] [S5].
- **朝日生命 要支援保険 (終身)**: 軽度介護終身保険（**低解約返戻金型**）[S9].
- **ジブラルタ生命**: full whole-life surrender values, suppressed to **70% of the ordinary value
  during the premium-paying period** and stepping to 100% at 払込満了 — the 低解約返戻金型 cliff. The
  published worked example (30歳男性, ¥10,000,000, 60歳払込満了) shows 払込保険料累計 ≈ ¥5,940,000 against
  解約返戻金 ≈ ¥4,000,000 at age 50 (in the suppressed period) and ≈ ¥8,900,000 against ≈
  ¥8,890,000 immediately after 払込満了 at 60, ≈ ¥9,270,000 at 70 and ≈ ¥9,600,000 at 80 [S12].
- Death benefit: absent from the stand-alone products [S11 states this explicitly], present
  in small conditional forms elsewhere — 朝日生命 かなえる介護年金 pays a 死亡給付金 equal to the first
  annuity instalment if the insured dies having never received one [S10]; 三井住友海上あいおい生命's
  死亡時返戻金 (above) [S4]; and in full on the ジブラルタ生命 chassis, where the 死亡保険金 continues for
  life at the sum insured **less the 介護保険金 already paid** [S12].

### 11. Grace, lapse, reinstatement, contestability, exclusions

From アフラック's 約款 and 契約概要, the fullest set retrieved [S1] [S2]:

- **払込期月 and 猶予期間** (第15条): for a 月払 contract the grace period runs **払込期月の翌月初日から末日まで**; for
  半年払 or 年払 it runs 払込期月の翌月初日から翌々月の月単位の契約応当日まで (with month-end substitutions for the
  2月/6月/11月 anniversaries). If the premium is not paid within the grace period the contract
  lapses **from the day after the grace period expires** [S2].
- **Claims inside the grace period** (第16条): unpaid premiums are deducted from the benefit;
  if the benefit is smaller than the unpaid premium the policyholder must pay the shortfall
  by the end of the grace period, failing which the contract lapses and no benefit is paid
  [S2].
- **復活** (第18条): within **1 year** of the lapse date, on fresh 告知, payment of arrears and
  the carrier's consent. The 復活日 is the later of the arrears payment date and the 告知日, and
  cover restarts from that date — the 責任開始期 is reset, which matters because the whole
  benefit definition is anchored to 責任開始期以後の傷害または疾病 [S1] [S2].
- **告知義務違反**: the contract may be rescinded where a material misstatement is found within
  **2 years** of the 責任開始日; the two-year bar does not help the policyholder where the event
  giving rise to a claim occurred inside those two years. Rescission for fraud is not time-
  limited [S1].
- **クーリング・オフ**: 8 days from the later of 申込日 and 告知日 (or the first-premium receipt date,
  depending on whether the 責任開始期に関する特約 was attached), with a full refund [S1].
- **免責事由** (第7条): the insured's or policyholder's **故意または重大な過失**; the insured's **犯罪行為**;
  **戦争その他の変乱**; **薬物依存**. The war exclusion is qualified — where the number of lives
  affected would not materially change the carrier's liability, the benefit may still be
  paid [S2].
- **Other refusal grounds** [S1]: the certification or company-basis state arising from an
  illness contracted or an accident occurring before the 責任開始期(日); certification at
  **要支援1・要支援2 or 非該当（自立）** where the contract's threshold is a 要介護 band; failing the 約款
  definition of the company-basis states; the contract having lapsed; rescission for 非開示 or
  for 重大事由.
- **No 自動振替貸付 on the stand-alone products**: the mechanism cannot operate where there is no
  surrender value, and the term appears in the アフラック booklet only inside group/collection
  riders as a condition that terminates them [S2]. It **is** available on the whole-life
  chassis [S12], alongside 延長定期保険, 払済保険 and 減額.

### 12. Reserving, tax and the standard tables

- **Standard tables.** 標準生命表2018 is published openly by 日本アクチュアリー会 as three PDFs [R7] [R8]
  [R9]. The relevant table for this product is **第三分野標準生命表2018**, and its two governing
  facts are: it is graduated from the **第21回生命表（2010年）**, the *national* life table, not
  insured experience [R9]; and it **excludes 高度障害** (the 2007 edition included it) [R9].
  Sample `qx` [R8]:

  | Age | 第三分野2018 男 | 第三分野2018 女 | 死亡保険用2018 男 | 死亡保険用2018 女 |
  |---|---|---|---|---|
  | 40 | 0.00076 | 0.00043 | 0.00118 | 0.00088 |
  | 60 | 0.00548 | 0.00209 | 0.00653 | 0.00363 |
  | 65 | 0.00845 | 0.00317 | 0.01015 | 0.00484 |
  | 75 | 0.02242 | 0.00967 | 0.02637 | 0.01289 |
  | 85 | 0.07110 | 0.03843 | 0.09175 | 0.04885 |
  | 90 | 0.11657 | 0.07574 | 0.15760 | 0.09357 |

  The terminal age is **116** for the 第三分野 male table (`qx` = 1.00000 there, with `q(115)` =
  0.58241) and **109** for the 死亡保険用 male table; the 死亡保険用 female table runs to 113 [R8].
  Note the direction of the margin: the 第三分野 rates are **lower** than the 死亡保険用 rates at
  every age shown, which is the conservative direction for a living-benefit product where
  longer survival means more annuity instalments.
- **第三分野標準生命表2018 does not contain a care-state incidence basis.** There is no published
  standard incidence table for 要介護 states at all; the FSA framework says so directly and
  puts the obligation on each insurer to estimate 給付事由ごと incidence from public data and its
  own experience [R10]. That is the gap the 介護保険事業状況報告 [R4] [R5] fills for an open reference
  implementation.
- **Reserving.** 標準責任準備金 applies, and on top of it the FSA requires, every accounting
  period, a **ストレステスト** projecting incidence over a **10-year** test horizon at the 99th
  percentile and comparing the resulting claim amount against the claim amount on the 予定発生率;
  where the 予定発生率 fails to cover the 通常の予測の範囲内のリスク (defined at **97.7%**), a **負債十分性テスト** by
  future cash flow analysis follows, and 危険準備金 is topped up. The incidence model is the
  insurer's own, and must be disclosed, as must a numeric **基礎率変更権** exercise standard,
  explained to the customer at point of sale [R10]. This library projects gross cash flows;
  reserving is cited, not reproduced.
- **Tax.** Premiums for this product fall in the **介護医療保険料** basket of the post-2012 生命保険料控除
  regime [R11] [R12]. The schedule is ≤¥20,000 full, ¥20,000–40,000 half plus ¥10,000,
  ¥40,000–80,000 quarter plus ¥20,000, above ¥80,000 a flat **¥40,000**, with an overall
  three-basket cap of **¥120,000** [R11]. A contract mixing coverages is assigned to the
  basket of its 主たる保障内容, and rider premiums are allocated by the rider's own coverage [R11]
  — which is why the rider-heavy 主契約＋特約 structure of Japanese products has a tax consequence
  a model of premium net of tax relief would have to respect.
- **Mortality after onset.** No published post-onset (impaired) life table exists for the
  care state in the retrieved sources. The population baseline is the 完全生命表: 平均余命 at 65 is
  **19.97** years (male) and **24.88** (female) on the 第23回（令和2年）table [R13]; 平均寿命 is 81.56
  / 87.71 [R13]. Since more than 90% of certified 第1号被保険者 are 75 or older [R4], the 75-year
  平均余命 (12.54 / 16.22) is the more relevant anchor [R13].
- **Duration of the care state.** No official statistic was found. The best available is the
  生命保険文化センター household survey: care given (or in progress) lasted **55.0 months on average
  (4 years 7 months)**, with 27.9% at 4–10 years and 14.8% at 10 years or more [R14]. Cost,
  for benefit-adequacy framing: monthly average **¥90,000**, one-off total average
  **¥472,000** [R14]; the survey's own average 介護給付金月額 across in-force private cover is
  ¥92,000 for the household head [R14].

---

## Variation across carriers

| Feature | アフラック [S1] [S2] [S3] | 三井住友海上あいおい生命 [S4] [S5] [S6] | 東京海上日動あんしん生命 [S7] | 朝日生命 [S8] [S9] [S10] | 第一生命 [S11] | ジブラルタ生命 [S12] | 太陽生命 [S13] |
|---|---|---|---|---|---|---|---|
| Chassis | stand-alone, no CV | stand-alone, no CV in payment period | stand-alone, no CV | stand-alone, 返戻金なし (要支援保険 is 低解約返戻金型) | stand-alone, no death benefit | whole life, accelerated | stand-alone dementia |
| Public trigger | 要介護1 / 要介護2 / 要介護3 (three tiers) | 要介護1 or 要介護2 (elected); 要支援1 on a 特則 | 要介護2以上 | 要介護3以上 (要介護1 for waiver); 要支援2以上 on the 要支援保険 | **要支援1以上** | 要介護2以上 (要介護4/5 for the top annuity) | n/a (dementia diagnosis) |
| Company-basis limb | 180日 ADL **or** 90日 dementia, 満65歳未満 | 180日以上, 満65歳未満 | 180日を**超えて**, no age limit | not stated on the pages fetched | 180日間継続, no age limit stated | 180日以上, 満65歳未満 | 180日 continuation for the annuity |
| Benefit form | 一時金 ×2 tiers + 介護年金 | 一時金 **or** 年金, elected at issue | 介護年金 only | 一時金 (one product) / 年金 (another) | 一時金, once only | 一時金 = 50% of SA, convertible to an annuity | 一時金 ×2 + 治療年金 |
| Annuity metering | **state-tested annually, max 10 payments, then contract ends** | 5年確定 or 終身, survival-tested, commutable | 5/10年有期 or 終身, survival-tested, **explicitly unaffected by recovery** | 終身 or 5/10/15年有期 | n/a | 保証金額付 or 10年保証期間付終身年金, from age 40 | annual on survival |
| Amount graded by band | yes — 1型 5/6, 4/6; 2型 2/3, 1/3 of 基準額 | no | no | no | no | yes, via the 割増年金特約 | no |
| Premium waiver at | 要介護1 | first annuity payment | 介護年金 trigger | **要介護1** (lump sum at 要介護3) | not stated | payment of 介護保険金 | not stated |
| Waiting period | none stated | **180日 for dementia/MCI only** | **1 year, all benefits** | not stated | not stated | not stated | **90日** |
| MCI cover | via the 90日 dementia limb | 軽度認知障害診断一時金給付特則 | 10% of the 認知症一時金額 | separate product (issue 40–75) | no | no | 10% of the 認知症診断保険金 |
| Surrender value | **none** | none in payment period; **5%** after 払込満了 | none | none (要支援保険終身: 低解約返戻金型) | not stated | full, **70%** during 払込期間 | not stated |
| Issue ages | 18–79 | 15–69 direct | table 30–80 | 40–79 (定期 40–75) | not stated | table 20–50 | not stated |
| Term / premium term | 終身 / 終身払 | 終身 / 終身 | 終身 / 終身 | 終身 / 終身 | 終身 / 終身払 | 終身 / limited pay to 55–90 | not stated |

**What does not vary.** Every product ties its primary trigger to the public 要介護 (or 要支援)
certification and names 介護保険法 as the scheme it means [S1] [S12]; every one carries a
company-basis alternative expressed as a defined dependency state that must have *persisted*
for a stated number of days [S1] [S4] [S7] [S11] [S12] [R15]; every stand-alone product is
written whole-of-life with whole-of-life premiums [S1] [S4] [S7] [S8] [S10] [S11]; every one
has a premium-waiver mechanic tied to the care state [S1] [S4] [S7] [S8] [S12]; every 一時金
benefit is once-only per contract [S1] [S4] [S5] [S9] [S11]; and no carrier publishes an
incidence basis, a 予定利率 or a 予定発生率 [R10].

**Most representative design for a reference implementation.** A whole-of-life,
whole-of-life-premium, no-surrender-value stand-alone contract issued at 40–79, paying (i)
a 介護一時金 once on 要介護2以上 certification, (ii) a 介護年金 from 要介護3以上, and (iii) a premium waiver
from 要介護1以上; each trigger carrying a company-basis alternative of a defined dependency state
persisting 180 days (90 days where dementia-defined), restricted to lives under 65; the
annuity survival-tested rather than state-tested, since that is the majority practice [S4]
[S7] [S10] [S12], with the state-tested/10-payment variant modelled as the switchable
alternative [S1]; a dementia 一時金 with an MCI benefit at 10% of it and a 180-day dementia
waiting period [S5] [S7] [S13]; 月払 premiums level by issue age and sex; grace to the end of
the following month, lapse the day after, 復活 within one year, 告知義務違反 contestability of two
years [S2].

---

## Fetch failures and gaps

**URLs that failed or needed special handling:**

- `https://www.aflac.co.jp/kaigo/r_kaigo/` [S3] — HTTP **403** to a plain fetcher
  (WebFetch). Retrieved successfully on a second attempt with a browser User-Agent (HTTP
  200, 119,877 bytes). Recorded as retrieved.
- `https://www.gib-life.co.jp/st/keiyaku/yakkan/pdf/kaigo_nenkin_201604.pdf` [S14] —
  **Retrieved: NO.** The file downloads (HTTP 200, 707,260 bytes, 24 pp.) but its text layer
  uses an embedded CID font: `pdftotext` reports `Syntax Error: Unknown character collection
  'Adobe-Japan1'` on every page and `pypdf` returns mojibake. **No fact in this file is
  sourced to S14**; the ジブラルタ生命 annuity-conversion mechanics come from the brochure [S12]
  instead.
- `https://laws.e-gov.go.jp/law/...` (R1, R2, R3) — the human-facing HTML pages are a
  JavaScript shell and return ~800 bytes of chrome to any fetcher. Worked around by using
  the e-Gov law API (`https://laws.e-gov.go.jp/api/1/lawdata/<lawId>`), which returns the
  complete statute as XML. The URLs recorded in R1–R3 are the citable page URLs; the API
  endpoints are recorded alongside them.
- `https://www.mhlw.go.jp/toukei/saikin/hw/kaigo/kyufu/24/index.html` (R6) — the index page
  itself renders its content client-side and yielded no usable text; the linked PDFs
  (`dl/01.pdf`, `dl/02.pdf`) fetched and extracted cleanly and are what was read.

**Documents sought and not found:**

- **約款 / 契約締結前交付書面 PDFs for 東京海上日動あんしん生命, 朝日生命, 第一生命 and 太陽生命.** Each carrier publishes its
  約款 behind a product-selection form or a Web約款 login, and no direct PDF URL for the
  nursing-care contracts was located. Everything cited to [S7]–[S11] and [S13] therefore
  comes from the carriers' own product pages, which are consumer summaries. Where a page is
  silent the fact is marked below rather than inferred.
- **アフラック 商品パンフレット** — the product is 面談必須 and the pamphlet is not published as a PDF; the
  契約概要・注意喚起情報 [S1] and the 約款 [S2] more than cover it.
- **年齢階級別第1号被保険者数**, which would let 認定率 be computed for each five-year band. The
  介護保険事業状況報告概要 [R4] gives 第1号被保険者数 only split 65–74 / 75+, so only those two 認定率 (4.3% and
  31.1%) could be computed. Band-level rates are available in the e-Stat release of the same
  statistic, which was not fetched this session. A widely repeated pair of figures (2.8% at
  65–69 and 72.7% at 90+) appeared in a search snippet from a commercial blog and is
  **[unverified]** — do not use it.
- **公式平均要介護期間.** No 厚生労働省 statistic for the duration of the care state was found. The
  55.0-month figure [R14] is a household survey of people who *provided* care, not a
  survival study of certified persons, and it is truncated (people currently caring are
  counted at elapsed duration). Treat it as an order of magnitude, not a termination basis.
- **厚生労働省「認知症及び軽度認知障害の有病率調査並びに将来推計に関する研究」** (令和5年度老人保健事業推進費等補助金), cited by a carrier for
  dementia prevalence [S13]. The study itself was not fetched; the prevalence figures quoted
  on that page are **[unverified]** and are not reproduced here.
- **標準責任準備金 for 介護保険 specifically.** [R10] establishes that 第三分野 business is subject to
  標準責任準備金 plus the stress/adequacy testing overlay, but the 平成8年大蔵省告示第48号 (calculation
  method and base rates) and 平成10年大蔵省令第231号 (危険準備金) were **not fetched**. The 標準利率
  applicable to this product class is therefore **[unverified]**.

**Claims left [unverified], and why:**

- 太陽生命 認知症保険 [S13]: 契約年齢, 保険期間, 保険料払込期間, surrender value and premium waiver are **not
  stated** on the fetched page — **[unverified]**.
- 朝日生命 かなえる介護年金 [S10]: 保険料払込免除 and 解約返戻金 are not stated on the fetched page —
  **[unverified]**.
- 第一生命 要支援・介護保険 [S11]: 契約年齢 range, premium rates, 保険料払込免除 and surrender value are not stated
  — **[unverified]**. The page states 65歳以上 contracts are capped at ¥500,000, which implies
  issue above 65 is possible but does not give the upper bound.
- 東京海上日動あんしん生命 [S7]: the exact 契約年齢 envelope is not stated; the benefit-amount bands (20–60歳
  / 61–80歳) and the premium table (30–80) bracket it but do not fix it — **[unverified]**.
- 三井住友海上あいおい生命 [S4] [S6]: the shorter 保険料払込期間 options that make the 5% surrender value
  reachable are referred to but not enumerated — **[unverified]**.
- Grace period, reinstatement window and contestability for every carrier other than アフラック:
  only アフラック's 約款 was retrieved, so the market-wide statement that these are the convention
  rests on one contract [S2]. The one-month grace for monthly premiums and the three-year
  reinstatement window commonly quoted for the Japanese market as a whole are
  **[unverified]** — アフラック's own reinstatement window is **one year**, not three [S1] [S2],
  which is itself a caution against assuming the market convention.
- 予定利率, 予定発生率 and any per-mille rate structure: not published by any carrier examined, and
  [R10] confirms no standard exists. Any incidence basis in the reference model must be
  constructed from [R4]/[R5] and marked **[std]**.
- Post-onset (impaired-life) mortality and recovery/de-certification rates: no source found
  in any register. Certification renewal exists in law [R1, 第28条] and bands demonstrably
  move — a carrier's own FAQ addresses what happens 「要介護状態が改善された場合」 [S3] — but no
  transition-rate table is public. Both must be **[std]**.
