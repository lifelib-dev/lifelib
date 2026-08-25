# Sources

Source ids [S#] and [R#] are carried verbatim from `_research/nursing-care.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps. Two ids are absent here. **R7** (the 日本アクチュアリー会
標準生命表2018 index page) is retrieved in the research file but is not cited by the product
documents, which reach the tables through the numerical tables [R8] and the construction
summary [R9], and through the cross-product entries [REG-R18] and [REG-R21]. **S14** (a
carrier's 介護年金移行特約 ご契約のしおり・約款) downloaded cleanly but its text layer uses an embedded
CID-keyed font that neither `pdftotext` nor `pypdf` could decode; the research file records
that **no fact anywhere is sourced to S14**, and the annuity-conversion mechanics it would
have carried are taken from the same carrier's brochure [S12] instead. Access date for all
sources: 2026-08-20. No sources were newly added at drafting. Cross-product [REG-R#] tags
are listed in their own section at the end.

Thirteen primary documents from **seven carriers** are cited. Only two of the thirteen are
contractual documents in the strict sense — one carrier's 契約締結前交付書面 [S1] and its 普通保険約款
[S2]. The other eleven are consumer product pages and one 商品パンフレット [S12]. That asymmetry is
a fact about this market segment, not an accident of searching: five of the seven carriers
publish nursing-care 約款 only behind a product-selection form or a Web約款 login, and no direct
PDF URL was located for any of them. Every mechanic stated in `product-spec.md` on the
authority of a product page alone is a **consumer summary**, and where such a page is silent
the research file records the silence rather than inferring, which is why several parameters
in this product carry [unverified] rather than a value.

Several product-specific [R#] entries cover the same statute, statistic or table as a
cross-product [REG-R#] entry. Where the fact was extracted for this product — the
certification-band definitions in minutes, the full 認定者数 cross-table, the 第三分野 reserving
paper — the documents cite the product-specific [R#]. Where the load-bearing statement is
the cross-product one — the 要介護2以上 share as the arithmetic step that makes this product
modelled from public data, the ESR regime, the redistribution restriction on the standard
tables, the industry lapse rate — they cite the [REG-R#]. Both resolve to a retrieved
document.

---

## Primary product sources

(jplib-nursing_care-s1)=

### S1 — アフラック生命保険株式会社, 「アフラックのしっかり頼れる介護保険」契約概要・注意喚起情報 (契約締結前交付書面)
- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: 「アフラックのしっかり頼れる介護保険」2025年11月版 お申し込みいただく前に 契約概要・注意喚起情報, document number
  **No.B25E206**, 12 pp. Formal product name 介護保険〔無解約払戻金2021〕
- Doc type: 契約締結前交付書面 (契約概要 + 注意喚起情報, pre-contract disclosure)
- URL: https://www.bank.aflac.co.jp/static/bank/r_kaigo/PDF/bank_r_kaigo_summary_2511.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded with a browser User-Agent, 12
  pp., text extracted with `pdftotext -enc UTF-8` and read in full)

(jplib-nursing_care-s2)=

### S2 — アフラック生命保険株式会社, 「介護保険〔無解約払戻金2021〕ご契約のしおり・約款」 (policy booklet and conditions)
- Publisher: アフラック生命保険株式会社
- Document: ご契約のしおり・約款 booklet carrying the 介護保険〔無解約払戻金2021〕普通保険約款 and the attached 特約条項,
  100 pp.
- Doc type: ご契約のしおり・約款 (普通保険約款 with the booklet front matter)
- URL: https://www.aflac.co.jp/yakkan/bank/pdf/r_kaigo_27569800.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, 100 pp. confirmed with `pypdf`,
  text extracted; the benefit, premium-waiver, grace, lapse, reinstatement and surrender
  articles and 別表70 / 別表71 read)

(jplib-nursing_care-s3)=

### S3 — アフラック生命保険株式会社, 「アフラックのしっかり頼れる介護保険：保障内容」 (product page)
- Publisher: アフラック生命保険株式会社
- Doc type: product page (consumer)
- URL: https://www.aflac.co.jp/kaigo/r_kaigo/
- Accessed: 2026-08-20. Retrieved: YES — **HTTP 403 to a plain fetcher; retrieved on a
  second attempt with a browser User-Agent** (HTTP 200, 119,877 bytes). Page currency note
  "2025年9月現在"

(jplib-nursing_care-s4)=

### S4 — 三井住友海上あいおい生命保険株式会社, 「&LIFE 介護保険Cセレクト」主契約の保障内容 (product page)
- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: product page for the 主契約; formal product name 介護・認知症選択型保障保険（無解約返戻金型）無配当
- Doc type: product page (consumer)
- URL: https://www.msa-life.co.jp/lineup/kaigo/main.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent; HTML converted
  to text and read)

(jplib-nursing_care-s5)=

### S5 — 三井住友海上あいおい生命保険株式会社, 「&LIFE 介護保険Cセレクト」オプション (product page)
- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: the 特則・特約 menu for the same product
- Doc type: product page (consumer)
- URL: https://www.msa-life.co.jp/lineup/kaigo/option.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent)

(jplib-nursing_care-s6)=

### S6 — 三井住友海上あいおい生命保険株式会社, 「&LIFE 介護保険Cセレクト」保障内容・保険料表 (product page with rate table)
- Publisher: 三井住友海上あいおい生命保険株式会社 (きらめきライフダイレクト資料請求サイト)
- Document: product page carrying a published **月払保険料表** by age and sex for six product
  types at fixed benefit levels (一時金 ¥3,000,000 / 年金 ¥600,000)
- Doc type: product page with premium rate table
- URL: https://www.kiramekilife-direct.jp/care/sample.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent; the full rate
  table extracted)

(jplib-nursing_care-s7)=

### S7 — 東京海上日動あんしん生命保険株式会社, 「あんしんねんきん介護」 (product page)
- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: product page for 介護年金保険（無解約返戻金型）[無配当], with a published premium example table
  for ages 30–80 by sex
- Doc type: product page (consumer)
- URL: https://www.tmn-anshin.co.jp/kojin/goods_kaigo/nenkin_kaigo/
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent; HTML converted
  to text and read)

(jplib-nursing_care-s8)=

### S8 — 朝日生命保険相互会社, 「あんしん介護 介護一時金タイプ」 (product page)
- Publisher: 朝日生命保険相互会社
- Document: product page; formal product name 介護一時金保険（返戻金なし型）（2012）, with published monthly
  premiums for a ¥3,000,000 lump sum by sex at ages 40–70
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/anshinkaigo/
- Accessed: 2026-08-20. Retrieved: YES (fetched twice — once with a plain fetcher, once with
  a browser User-Agent to read the premium table verbatim)

(jplib-nursing_care-s9)=

### S9 — 朝日生命保険相互会社, 「あんしん介護 要支援保険」 (product page)
- Publisher: 朝日生命保険相互会社
- Document: product page; 「要支援保険」 is the trade name of 軽度介護定期保険 and 軽度介護終身保険（低解約返戻金型）, with
  published premiums for a ¥500,000 sum insured at ages 40–70
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/anshinyoshien/
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent)

(jplib-nursing_care-s10)=

### S10 — 朝日生命保険相互会社, 「かなえる介護年金」 (product page)
- Publisher: 朝日生命保険相互会社
- Document: product page, with published monthly premiums for a ¥300,000 annuity at ages 40+
  on each payout shape
- Doc type: product page (consumer)
- URL: https://anshinkaigo.asahi-life.co.jp/products/kanaerukaigo/
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200)

(jplib-nursing_care-s11)=

### S11 — 第一生命保険株式会社, 「要支援1から備えられる第一生命の要支援・介護保険」 (product page)
- Publisher: 第一生命保険株式会社 (the 要支援・介護保険 within the ジャスト product suite)
- Document: product page; page approval code (登)C25P0098（2025.6.6）
- Doc type: product page (consumer)
- URL: https://www.dai-ichi-life.co.jp/promotion/just/i01/index.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent)

(jplib-nursing_care-s12)=

### S12 — ジブラルタ生命保険株式会社, 「介護保障付終身保険（低解約返戻金型）〔無配当〕」商品パンフレット (brochure)
- Publisher: ジブラルタ生命保険株式会社
- Document: 商品パンフレット, 2024年9月改訂版; premium rate table dated 2024年9月17日現在, by issue age
  (20/30/40/50) × 保険料払込期間 (55/60/65/70/75/80/85/90歳満了) × sex for a ¥10,000,000 sum insured,
  plus a worked 解約返戻金 progression
- Doc type: 商品パンフレット (product brochure)
- URL: https://www.gib-life.co.jp/st/intro/products/pdf/kaigo_shushin_panf.pdf
- Accessed: 2026-08-20. Retrieved: YES (full PDF downloaded, text extracted and read; the
  numeric tables are text, not images)

(jplib-nursing_care-s13)=

### S13 — 太陽生命保険株式会社, 「認知症保険」 (product page)
- Publisher: 太陽生命保険株式会社 (太陽生命ダイレクト)
- Doc type: product page (consumer)
- URL: https://www.taiyo-seimei.co.jp/net_lineup/dementia_care/ninchi2/index.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent). 契約年齢, 保険期間,
  保険料払込期間, surrender value and premium waiver are **not stated** on the page and are
  [unverified] in the product documents

---

## Regulatory and actuarial references

(jplib-nursing_care-r1)=

### R1 — e-Gov 法令検索, 介護保険法（平成9年12月17日法律第123号）
- Publisher: e-Gov 法令検索 (総務省行政管理局)
- Doc type: statute
- URL: https://laws.e-gov.go.jp/law/409AC0000000123 (retrieved through the e-Gov law API
  endpoint `https://laws.e-gov.go.jp/api/1/lawdata/409AC0000000123`)
- Accessed: 2026-08-20. Retrieved: YES — **the HTML page is a JavaScript shell returning
  about 800 bytes to any fetcher; the API endpoint returns the full law as XML** (1,904,648
  bytes), which was converted to text and read. 第7条 (要介護状態, 要支援状態, the 65+/40–64 split), 第9条
  (第一号 and 第二号被保険者), 第19条 (要介護認定), 第27条 (the 30-day decision, retroactive to the application
  date) and 第28条 (有効期間 and 更新認定) were read

(jplib-nursing_care-r2)=

### R2 — e-Gov 法令検索, 要介護認定等に係る介護認定審査会による審査及び判定の基準等に関する省令
- Publisher: e-Gov 法令検索 (平成11年4月30日厚生省令第58号)
- Doc type: ministerial ordinance
- URL: https://laws.e-gov.go.jp/law/411M50000100058 (retrieved through
  `https://laws.e-gov.go.jp/api/1/lawdata/411M50000100058`)
- Accessed: 2026-08-20. Retrieved: YES (API XML, 20,936 bytes, converted and read; the HTML
  page is a JS shell). This is the ordinance that defines every certification band
  quantitatively in 要介護認定等基準時間, and the one cited by name inside a carrier's own contract
  wording [S12]

(jplib-nursing_care-r3)=

### R3 — e-Gov 法令検索, 介護保険法施行令（平成10年政令第412号）第2条（特定疾病）
- Publisher: e-Gov 法令検索
- Doc type: cabinet order
- URL: https://laws.e-gov.go.jp/law/410CO0000000412 (retrieved through
  `https://laws.e-gov.go.jp/api/1/lawdata/410CO0000000412`)
- Accessed: 2026-08-20. Retrieved: YES (API XML, 1,623,242 bytes, converted and read). The
  exhaustive list of the **16 特定疾病** that alone can support certification of a 第二号被保険者

(jplib-nursing_care-r4)=

### R4 — 厚生労働省, 「令和5年度 介護保険事業状況報告（年報）」報告書の概要
- Publisher: 厚生労働省 老健局 介護保険計画課
- Document: 報告書の概要 PDF (`r05_gaiyou.pdf`), position as at 令和6年3月末
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/dl/r05_gaiyou.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted, 第1表 and 第2表 read in
  full — the 認定者数 cross-table by sex × six age bands × seven certification bands)

(jplib-nursing_care-r5)=

### R5 — 厚生労働省, 「令和5年度 介護保険事業状況報告（年報）」ポイント
- Publisher: 厚生労働省
- Document: ポイント PDF (`r05_point.pdf`)
- Doc type: official statistics (summary)
- URL: https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/dl/r05_point.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted and read; the
  age-split 認定率 appears only as a chart data series, so both published split rates were
  cross-checked against the counts in [R4] before being used)

(jplib-nursing_care-r6)=

### R6 — 厚生労働省, 「令和6年度 介護給付費等実態統計の概況」
- Publisher: 厚生労働省
- Document: 統計の概要 (`dl/01.pdf`) and 結果の概要 (`dl/02.pdf`), covering 令和6年5月審査分 to 令和7年4月審査分
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/kaigo/kyufu/24/index.html
- Accessed: 2026-08-20. Retrieved: YES for the two PDFs (downloaded with a browser
  User-Agent, text extracted and read); **the index page itself renders client-side and
  yielded no usable text**. The statistic is a claims-paid census built from every 介護給付費明細書
  in the 介護保険総合データベース, not a survey

(jplib-nursing_care-r8)=

### R8 — 日本アクチュアリー会, 「標準生命表2018」数表 (actuarial table)
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表2018 numerical tables — 生保標準生命表2018（死亡保険用）男/女 and 第三分野標準生命表2018 男/女
- Doc type: actuarial table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted; individual `qx`
  values read off by locating the printed age labels, each quoted value re-checked against
  its row position). **第三分野標準生命表2018 is a mortality table only** — it carries no morbidity,
  no incidence and no care-state decrement

(jplib-nursing_care-r9)=

### R9 — 日本アクチュアリー会, 「標準生命表2018の作成概要」 (technical note)
- Publisher: 公益社団法人 日本アクチュアリー会
- Document: 標準生命表２０１８の作成概要 (資料①〜⑤)
- Doc type: actuarial technical note
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted, the 第三分野 sections
  read). Records that 第三分野標準生命表2018 is graduated from 第21回生命表（2010年）, the *national* life
  table rather than insured experience, and that it **excludes 高度障害** where the 2007 edition
  included it

(jplib-nursing_care-r10)=

### R10 — 金融庁, 「第三分野の責任準備金積立ルール・事後検証等の概要について」
- Publisher: 金融庁
- Document: 別紙1-2 to the 2006-02-10 release
- Doc type: regulatory policy paper
- URL: https://www.fsa.go.jp/news/newsj/17/hoken/f-20060210-1/01_2.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted and read). The
  framework governing reserving for this product: no standard 第三分野 incidence indicator
  exists, so each insurer must estimate 発生率 per benefit trigger from public data and its own
  experience; 標準責任準備金 plus an annual ストレステスト over a ten-year horizon at the 99th percentile;
  a 負債十分性テスト where the 予定発生率 fails to cover risk defined at 97.7%; disclosure of the
  incidence model and of a numeric 基礎率変更権 exercise standard

(jplib-nursing_care-r11)=

### R11 — 国税庁, タックスアンサー No.1140「生命保険料控除」
- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent). The post-2012
  three-basket regime, the per-basket schedule, the ¥120,000 overall cap, and the rules that
  a mixed contract is allocated to the basket of its 主たる保障内容 and that rider premiums are
  allocated by the rider's own coverage

(jplib-nursing_care-r12)=

### R12 — 国税庁, タックスアンサー No.1141「生命保険料控除の対象となる保険契約等」
- Publisher: 国税庁
- Doc type: tax guidance
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1141.htm
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent). What qualifies
  for the 介護医療保険料 basket: contracts written on or after 2012-01-01 paying on 疾病または身体の傷害等
  where payment is triggered by a 医療費支払事由; contracts under five years and savings-type
  contracts excluded; beneficiaries restricted to the premium payer, spouse or a relative

(jplib-nursing_care-r13)=

### R13 — 厚生労働省, 「第23回生命表（完全生命表）の概況」
- Publisher: 厚生労働省 政策統括官付参事官付人口動態・保健社会統計室 (published 令和4年3月2日)
- Doc type: official statistics
- URL: https://www.mhlw.go.jp/toukei/saikin/hw/life/23th/dl/23th-11.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted and read). 平均寿命 and
  平均余命 at 20, 65 and 75 on the 第23回（令和2年）完全生命表, with the series back to 第22回

(jplib-nursing_care-r14)=

### R14 — 生命保険文化センター, 「2024（令和6）年度 生命保険に関する全国実態調査＜速報版＞」
- Publisher: 公益財団法人 生命保険文化センター (2024年11月)
- Doc type: household survey report
- URL: https://www.jili.or.jp/files/research/zenkokujittai/pdf/r6/2024sokuhou.pdf
- Accessed: 2026-08-20. Retrieved: YES (PDF downloaded, text extracted, the care and
  product-penetration sections read). Household penetration of 介護保険・介護特約 and 認知症保険・認知症特約;
  the 介護給付金月額 held; the duration and cost of care actually given, and the certification band
  of the person cared for

(jplib-nursing_care-r15)=

### R15 — 生命保険文化センター, 「介護保険」（生命保険の種類・主契約の種類）
- Publisher: 公益財団法人 生命保険文化センター
- Doc type: consumer-education reference on product design
- URL: https://www.jili.or.jp/knows_learns/kind/main/14.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200). The market-level taxonomy of benefits,
  triggers and terms — the independent check that the seven carriers cited here span the
  design space rather than sampling one corner of it

(jplib-nursing_care-r16)=

### R16 — 生命保険文化センター, 「介護や支援が必要な人はどれくらい？」
- Publisher: 公益財団法人 生命保険文化センター
- Doc type: statistical digest of 介護保険事業状況報告
- URL: https://www.jili.or.jp/lifeplan/lifesecurity/1119.html
- Accessed: 2026-08-20. Retrieved: YES (HTTP 200 with a browser User-Agent). The growth of
  certified persons from the first year of the public scheme to 令和5年度, and the band with the
  largest count

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product Japan reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R47, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the
nursing-care documents:

- **REG-R1** — 保険業法 第3条: the licence classes and the 第一分野 / 第三分野 split. fetched_ok: yes.
- **REG-R2** — 保険業法 第4条: the 基礎書類, including the unpublished 算出方法書 — the reason every
  pricing-basis parameter here is **[std]** while every contractual parameter carries an
  [S#] tag. fetched_ok: yes.
- **REG-R3** — 保険業法 第115条: 価格変動準備金, cited for what it is *not* — an asset-driven
  balance-sheet reserve outside a liability projection. fetched_ok: yes.
- **REG-R4** — 保険業法 第116条: the 責任準備金 requirement and the delegation the 標準責任準備金 chain hangs
  on. fetched_ok: yes.
- **REG-R5** — 保険業法 第120条: the appointment of the 保険計理人, the office that
  professionally owns any basis this model uses. fetched_ok: yes.
- **REG-R6** — 保険業法 第121条: the 保険計理人's 意見書, the statutory demand behind the 1号収支分析.
  fetched_ok: yes.
- **REG-R7** — 保険業法施行規則 第68条: which contracts are standard-reserve contracts. fetched_ok:
  yes.
- **REG-R8** — 保険業法施行規則 第69条: the reserve taxonomy, including the separately identified
  第三分野保険の保険リスクに備える危険準備金. fetched_ok: yes.
- **REG-R9** — 保険業法施行規則 第30条の2: the four surplus-distribution methods, cited here for what a
  無配当 contract switches off. fetched_ok: yes.
- **REG-R10** — 平成8年大蔵省告示第48号: 標準責任準備金 on the 平準純保険料式, the table vintages and the 標準利率 reset
  rules. fetched_ok: yes, from an unofficial consolidated mirror.
- **REG-R11** — 告示48号改正 (2017): adoption of 第三分野標準生命表2018 for contracts from 2018-04-01.
  fetched_ok: yes.
- **REG-R13** — 平成10年6月8日大蔵省告示第231号: the 第三分野 stress test. fetched_ok: **no** — the
  notification's own text was not located, so its stress magnitudes and confidence level are
  [unverified] and no numeric stress level is asserted in these documents.
- **REG-R14** — 保険会社向けの総合的な監督指針（本編）: third-sector reserving, the 契約締結前交付書面 content list,
  自動振替貸付 as a policyholder election, and 低解約返戻金型 disclosure. fetched_ok: yes.
- **REG-R15** — 経済価値ベースのソルベンシー規制の概要: commencement 2026-03-31, the 100% trigger, 現在推計 + MOCE,
  the 99.5% calibration. fetched_ok: yes.
- **REG-R17** — ソルベンシー・マージン比率: the superseded 200% threshold and market SMR levels.
  fetched_ok: **no** for the 告示 itself; the figures come from REG-R14 and REG-R15.
- **REG-R18** — 標準生命表2018 PDF: the public valuation `qx` tables, including 第三分野標準生命表2018.
  fetched_ok: yes.
- **REG-R19** — 標準生命表2018 ほか（Excel）: the machine-readable form of the same tables,
  cited with [REG-R18] for the `provenance` column of `mort_table.csv`. fetched_ok: yes.
- **REG-R20** — 標準生命表2018 の作成概要: the 2σ margin, the improvement allowance, the 保険年齢方式
  construction, and the exclusion of 高度障害 from the third-sector table. fetched_ok: yes.
- **REG-R21** — 日本アクチュアリー会 索引と利用規約: redistribution of the tables is restricted, so the
  library ships a **[std]** construction citing the tables rather than a copy of them.
  fetched_ok: yes.
- **REG-R22** — 保険計理人の実務基準: the 1号収支分析 — at least ten future years, per segment. fetched_ok:
  yes.
- **REG-R23** — 監督指針 VI: the 日本アクチュアリー会 as 指定法人 under 法第122条の2 — the body that publishes a
  mortality table for this product class and does not publish an incidence table.
  fetched_ok: yes.
- **REG-R24** — 第23回生命表（完全生命表）令和2年: the population 平均余命 — 12.54 years for a male
  at 75 — that anchors the care-state mortality multiple. fetched_ok: yes.
- **REG-R26** — 令和5年患者調査 受療率 and **REG-R27** — 同 平均在院日数: the prevalence statistic the
  third-sector chassis converts, cited here only to name the class of standardization this
  product's own prevalence-to-incidence conversion belongs to. fetched_ok: yes.
- **REG-R30** — 令和5年度 介護保険事業状況報告: 認定率 19.4%, the 4.3% / 31.1% age split, and the band
  composition from which **要介護2以上 = 50.8% of 認定者** falls out — the single arithmetic step
  that makes this product modellable from public data. fetched_ok: yes (ポイント PDF; the 全国版
  workbook was not opened).
- **REG-R31** — 生命保険の動向 2025年版: the market mix by policy count and the only published
  industry-wide persistency figure, 解約・失効率 5.6% on 個人保険. fetched_ok: yes.
- **REG-R32** — 生命保険に関する全国実態調査 2024年度: household penetration of 介護保険・介護特約, and the large 不明
  share that makes 20.1% a floor rather than a point estimate. fetched_ok: yes.
- **REG-R33** — e-Stat: the access route to the machine-readable 介護保険事業状況報告 grids, where the
  five-year-band 認定率 this product's incidence basis wants can be found; licence terms
  unread. fetched_ok: yes (home page only).
- **REG-R34** — 保険法 第51条: the statutory suicide exclusion carries no time limit, so any 免責期間
  is a contractual, per-carrier fact. fetched_ok: yes.
- **REG-R35** — 保険法 第55条: the five-year contestability ceiling and the one-month discovery
  clock, inside which the observed two-year 告知義務違反 windows sit. fetched_ok: yes.
- **REG-R36** — 保険業法 第309条: the eight-day dispatch-rule クーリング・オフ, scoped out here
  explicitly. fetched_ok: yes.
- **REG-R39** — 金融サービス提供法 第4条: the 説明義務, which is what the point-of-sale disclosure of a
  numeric 基礎率変更権 standard rides on. fetched_ok: yes.
- **REG-R40** — 生命保険契約者保護機構 Q&A: compensation at 90% of the 責任準備金. fetched_ok: yes (Q1
  only).
- **REG-R41** — 保険業法 第270条の3: the statutory delegation of that compensation rate.
  fetched_ok: yes.
- **REG-R42** — 介護保険法 第7条: the statutory definition of 要介護状態 and the 65+/40–64 特定疾病 split —
  the definition every 公的介護保険連動型 trigger points at. fetched_ok: yes.
- **REG-R43** — 所得税法 第76条: three ¥40,000 baskets capped at ¥120,000, of which 介護医療保険料 is
  this product's. fetched_ok: yes.
- **REG-R47** — 金融庁 IFRS 関連情報: IFRS 17 is voluntary in Japan, so J-GAAP, ESR and IFRS are
  three separate bases fed by one projection. fetched_ok: yes.

---

## Provenance note

Extraction details — which facts were read from which document, the per-source fact
extraction sections, the seven-carrier variation table, and the full gaps register (the
unreadable 介護年金移行特約 booklet, the five carriers whose 約款 sit behind a login, the missing
年齢階級別第1号被保険者数 that would give band-level 認定率, the absence of any official 平均要介護期間, the
unfetched 平成8年大蔵省告示第48号 and 平成10年大蔵省令第231号, the consequently [unverified] 標準利率 for this
class, and the complete absence of public post-onset mortality and recovery rates) — live in
`_research/nursing-care.md`. That file is the citation ground truth for the S# and R#
numbering used here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R4]: #jplib-nursing_care-r4
[R8]: #jplib-nursing_care-r8
[R9]: #jplib-nursing_care-r9
[REG-R18]: #jplib-reg-r18
[REG-R21]: #jplib-reg-r21
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
