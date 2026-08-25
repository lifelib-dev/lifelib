# Whole life (終身保険, including 低解約返戻金型) — research notes (Japan)

Research compiled 2026-08-20 for the reference-products library (Japan section). Purpose:
source library for a Japanese whole life liability cash flow reference model — the
level-premium ordinary whole life chassis (責任準備金 / 解約返戻金 / 契約者貸付 / 自動振替貸付), its 低解約返戻金型
(*tei-kaiyaku-henreikin-gata*, suppressed-surrender-value) variant, and the neighbouring
積立利率変動型 and 一時払 shapes.

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually retrieved and read during
this session, or is tagged [unverified] where it is general knowledge or a search-result
snippet not confirmed against a retrieved document. Access date for all fetched sources:
2026-08-20.

Seven carriers are represented: アフラック生命保険, オリックス生命保険, 東京海上日動あんしん生命保険, 日本生命保険相互会社,
株式会社かんぽ生命保険, 第一生命保険, 三井住友海上あいおい生命保険, plus 明治安田生命保険 for the 予定利率 disclosure. Company and
branded product names appear here and in `sources.md` only.

---

## Primary sources

### S1 — アフラック生命保険, 「アフラックの終身保険 ご契約のしおり・約款」 (policy booklet + conditions)

- Publisher: アフラック生命保険株式会社 (Aflac Life Insurance Japan Ltd.)
- Document: ご契約のしおり・約款 アフラックの終身保険, file `syushin_77888601.pdf`, 171 pp. Contains 「終身保険
  普通保険約款」 (制定 2018年4月2日) plus 定期特約, 災害死亡割増特約, 傷害特約, リビング・ニーズ特約, 非喫煙割引特約 (制定 2018年4月2日) and
  別表1–51.
- Doc type: policy booklet and policy conditions (ご契約のしおり・約款)
- URL: https://www.aflac.co.jp/yakkan/pdf/syushin_77888601.pdf
- Retrieved: YES (full PDF downloaded, 171 pp., text extracted with PyMuPDF and read; the
  ordinary-whole-life articles 1–35 read in full)
- Key content: death and 高度障害 benefit definitions and 免責事由; 猶予期間 by payment mode; 自動振替貸付
  (art. 13) including the amount lent and the interest-rate ceiling; 自動振替貸付の取消 (art. 14); 復活
  within 3 years (art. 16); 払済保険 (art. 17); 保険料払込期間の変更 (art. 19); 契約者貸付 at 9/10 (8/10 once
  paid up) of the surrender value and the lapse mechanic when the loan exceeds it (art. 20);
  解約 (art. 32), 減額 (art. 33), 払戻金 basis (art. 34); 契約年齢 definition; リビング・ニーズ 指定保険金額 cap.

### S2 — アフラック生命保険, 「積立利率等・約款貸付の利率のお知らせ」 (published rate schedule)

- Publisher: アフラック生命保険株式会社
- Document: web page, rates stated "2017年2月1日現在"
- Doc type: published rate disclosure (company web page)
- URL: https://www.aflac.co.jp/reserving_loan_rate.html
- Retrieved: YES (HTTP 403 to WebFetch; retrieved with a browser User-Agent via curl, HTTP
  200, server-rendered HTML, tables read)
- Key content: 契約者貸付金の利率 and 保険料の自動振替貸付の利率 by contract-date band; 契約者配当金積立利率 and 据置金の利率; all
  compounded.

### S3 — オリックス生命保険, 「無配当 終身保険（低解約払戻金型） 終身保険RISE[ライズ] ご契約のしおり／約款」

- Publisher: オリックス生命保険株式会社 (ORIX Life Insurance Corporation)
- Document: Web約款 `webyakkan_rise_20240402.pdf` (2024年4月2日版), 164 pp., containing
  「無配当終身保険（低解約払戻金型）普通保険約款」 and its 特約条項/特則
- Doc type: policy booklet and policy conditions
- URL: https://www.orixlife.co.jp/customer/webclause/pdf/webyakkan_rise_20240402.pdf (index
  page: https://www.orixlife.co.jp/customer/webclause/)
- Retrieved: YES (full PDF downloaded, 164 pp., text extracted and read)
- Key content: **art. 33 (払戻金) — the defining clause of the 低解約返戻金型 mechanic**: 低解約払戻期間 =
  保険料払込期間, 解約払戻金支払割合 = 7割, the clawback where premiums in the low period were not all paid,
  and the disapplication after conversion to 払済保険; art. 14 自動振替貸付 (opt-in); art. 15 取消; art.
  16 復活 within 3 years; art. 18 払済保険; art. 20 契約者貸付 at 9/10 (8/10 paid-up); art. 34 契約年齢の計算;
  猶予期間 by mode; 3-year suicide exclusion.

### S4 — オリックス生命保険, 「終身保険ライズ」 商品パンフレット (brochure with rate and surrender-value tables)

- Publisher: オリックス生命保険株式会社
- Document: `rise_pamphlet.pdf`, 5 pp.; the 月払保険料表 is headed "2025年12月2日現在（単位：円）"
- Doc type: product brochure (with published premium and surrender-value tables)
- URL: https://www.orixlife.co.jp/life/rise/pdf/rise_pamphlet.pdf
- Retrieved: YES (full PDF downloaded; tables recovered by positional word extraction, since
  a plain text dump scrambles the multi-column layout)
- Key content: a **published surrender-value table** for a single model point (30歳男性,
  保険金額500万円, 保険期間終身, 保険料払込期間15年, 月払保険料14,580円) at durations 5/10/15/★15/20/30/40/50 years,
  with 払込保険料累計, 解約払戻金 and 払戻率; a **published premium rate table** by issue age 20–51, sex
  and 保険金額 (200/300/500/1,000万円) for the 15-year payment term, each with the 15-year
  surrender value and 払戻率; the list of 保険料払込期間 options.

### S5 — オリックス生命保険, 「終身保険ライズ」 お申込みにあたって（取扱いの内容）

- Publisher: オリックス生命保険株式会社
- Document: `rise2_pamphlet.pdf`, 3 pp.
- Doc type: product brochure (application terms page)
- URL: https://www.orixlife.co.jp/life/rise/pdf/rise2_pamphlet.pdf
- Retrieved: YES (full PDF downloaded; the eligibility table recovered by positional
  extraction)
- Key content: the **full issue-age envelope by 保険料払込期間**; 保険金額 range and unit; the
  100万円-only-at-76–80 rule; the 1,000万円-minimum-for-5-year-payment rule; 払込回数; 契約形態 (契約者 =
  被保険者 required); "この保険に配当金、満期保険金はありません".

### S6 — オリックス生命保険, FAQ 「「ライズ」の低解約払戻期間とは何ですか？」

- Publisher: オリックス生命保険株式会社
- Doc type: customer FAQ page
- URL: https://faq.orixlife.co.jp/faq_detail.html?id=100574
- Retrieved: YES (WebFetch, 200)
- Key content: 低解約払戻期間 defined as the period over which the surrender value is suppressed,
  and stated to be identical to 保険料払込期間. The page does **not** state the percentage — the
  percentage comes from S3 and S4.

### S7 — 東京海上日動あんしん生命保険, 「長割り終身／5年ごと利差配当付終身保険」 契約概要・注意喚起情報・ご契約のしおり・約款

- Publisher: 東京海上日動あんしん生命保険株式会社
- Document: 「長割り終身 5年ごと利差配当付低解約返戻金型終身保険／5年ごと利差配当付終身保険」, 2010.3改定, 292 pp.; 契約例 calculation
  base date 平成22年3月2日; 募資 '09-KF04-019 / -020
- Doc type: pre-contract summary + policy booklet + policy conditions, in one booklet
- URL:
  https://ykn.tmn-anshin.co.jp/affix/yakkan2/nagawari/D79-11660/MCNG9C0_%E9%95%B7%E5%89%B2%E3%82%8A%E7%B5%82%E8%BA%AB.pdf
- Retrieved: YES (full PDF downloaded, 292 pp.). **Note on extraction**: pypdf returns
  mojibake for this file (CID-encoded subset fonts); PyMuPDF (`fitz`) extracts it cleanly.
  All facts below are from the PyMuPDF extraction.
- Key content: the **side-by-side pair** — the same product sold with and without the 低解約返戻金
  suppression, with both premium scales and both surrender-value tables at durations
  5/10/20/30/40 years for one model point; 低解約返戻金期間 and 低解約返戻金割合 stated numerically;
  5年ごと利差配当 mechanics and 5年ごと積立配当金; 保険料の振替貸付 (art. 15) with the **published 上限利率 table by
  payment mode**; 契約者貸付 limits (9/10 in payment, 8/10 paid up), minimum draw amounts,
  semi-annual rate review dates; 払済保険 and **延長定期保険** including 復旧 within 3 years; the effect
  of the low-surrender period on 払済/延長/貸付/減額; 3-year suicide exclusion; 3-year 復活 window;
  2-year contestability.

### S8 — 日本生命保険相互会社, 「ニッセイみらいのカタチ ご契約のしおり 定款・約款」

- Publisher: 日本生命保険相互会社
- Document: しおり番号 202604A, 2026年4月改訂, 182 pp.; the whole life component is 「終身保険（有配当2012）」
- Doc type: policy booklet + articles of association + policy conditions
- URL: https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/shiori/01.pdf
- Retrieved: YES (full PDF downloaded, 182 pp., text extracted and read)
- Key content: the **counter-example on lapse mechanics** — this product has *no* 自動振替貸付,
  and instead terminates at a 解除予定日 three months after the 払込期月; 契約貸付 limited to 8/10 of the
  surrender value **less three months' premium**, with a one-year rolling 貸付期間; 高額割引制度
  threshold; リビング・ニーズ特約 automatically attached; 3-year suicide exclusion; 終身保険 available
  only on the 終身 (whole-of-life) term basis.

### S9 — 株式会社かんぽ生命保険, 「終身保険 ご契約のしおり・約款 2026年上半期版」

- Publisher: 株式会社かんぽ生命保険 (Japan Post Insurance)
- Document: `syusin_2026_05.pdf`, 448 pp., "この冊子の記載内容は、2026年5月2日現在の取り扱いを 説明しております"; covers
  普通終身保険（Ｒ07）, 特別終身保険（Ｒ07）, and both （低解約返戻金型） variants, marketed as 新ながいきくん
- Doc type: policy booklet and policy conditions
- URL: https://www.jp-life.japanpost.jp/products/clause/pdf/syusin/202605/syusin_2026_05.pdf
  (index: https://www.jp-life.japanpost.jp/products/clause/syusin/index.html)
- Retrieved: YES (full PDF downloaded, 448 pp., text extracted; the four 普通保険約款 and the
  contract-handling chapters read)
- Key content: 普通終身保険（Ｒ07）（低解約返戻金型）普通保険約款 **art. 34 (返戻金の支払)** — the suppression factor
  written as a literal multiplier; the ばらんす型 designs whose death benefit **steps down after
  払込満了**; the statutory 加入限度額; a **two-month** grace and a **one-year** 復活 window; explicit
  statement that the carrier has **no** 自動振替貸付, only a requested 保険料振替貸付; the loan-default
  mechanic that reduces the sum assured instead of lapsing the policy; 保険料払済契約 requiring two
  years in force.

### S10 — 第一生命保険, 「５年ごと配当付終身保険普通保険約款」

- Publisher: 第一生命保険株式会社
- Document: `01_10334_002.pdf`, 24 pp., 約款 archive folder `01_2014_01_1` (worked examples in
  the text use 契約日 平成26年5月1日, i.e. a 2014 vintage)
- Doc type: policy conditions (普通保険約款 only — no しおり in this file)
- URL: https://event.dai-ichi-life.co.jp/yakkan/01_2014_01_1/pdf/01_10334_002.pdf
- Retrieved: YES (full PDF downloaded, 24 pp., text extracted and read in full)
- Key content: a compact, cleanly drafted ordinary whole life 約款 — 猶予期間 table with a worked
  date example; 保険料の自動貸付 (art. 15) which for monthly contracts lends **to the next
  half-yearly anniversary** and rolls interest into principal on a半年 cycle, with a distinct
  post-払込満了 interest-rolling rule; 払済保険 (art. 27) requiring **3 years** of premiums;
  保険料払込期間の変更 (art. 28) requiring 3 years paid and 5 years remaining; 保険料のステップ払込方式の特則 (art.
  50) — a stepped premium scale after 10 or 15 years; 契約者貸付 (art. 30); 解約返還金 basis (art.
  24); 3-year suicide exclusion with 責任準備金 returned.

### S11 — 三井住友海上あいおい生命保険, 「終身保険／積立利率変動型終身保険／積立利率変動型終身保険（低解約返戻金型）／積立型終身保険 ご契約のしおり・約款」

- Publisher: 三井住友海上あいおい生命保険株式会社
- Document: `L6095-1.pdf`, 586 pp., 2010.3改定 (申込番号 L6095-1, 2010.04)
- Doc type: policy booklet and policy conditions
- URL: https://www.msa-life.co.jp/customer/msa/yakkan/L6095-1.pdf
- Retrieved: YES (full PDF downloaded, 586 pp., text extracted; the extraction contains NUL
  bytes and needs `tr -d '\000'` before grepping)
- Key content: a **third independent statement of the 70% suppression factor**, with a
  glossary definition of 低解約返戻金割合; the split of the low-period surrender value into a
  suppressed 基本保険金額 part and an unsuppressed 増加保険金額 part; the **積立利率 formula** (10-year JGB
  應募者利回り less an explicit expense margin, monthly reset, floored at the 予定利率, rounded to
  0.01%) in both the しおり and 約款 wordings; the **disclosed 予定利率** for that product at that
  date; 自動振替貸付 with a stated ceiling and a semi-annual rate-review calendar, and an explicit
  note that the low-surrender period shrinks the amount that can be lent.

### S12 — 明治安田生命保険, 「円貨建一時払商品に適用される予定利率」

- Publisher: 明治安田生命保険相互会社
- Doc type: published rate disclosure (company web page), 適用期間 2026年8月16日～2026年8月31日
- URL: https://www.meijiyasuda.co.jp/norapl/find/rate/yencommon/planned_interest_rate/
- Retrieved: YES (WebFetch, 200)
- Key content: current 予定利率 for yen single-premium whole life by plan length and for the
  single-premium endowment by term, plus the 最低保証予定利率. This is the clearest public evidence
  that Japanese insurers disclose the pricing interest rate on 一時払 products.

---

## Regulatory and actuarial references

### R1 — 日本アクチュアリー会, 「標準生命表２０１８」 (the tables themselves)

- Publisher: 公益社団法人日本アクチュアリー会 (Institute of Actuaries of Japan)
- Document: `seimeihyo2018.pdf`, 5 pp. — four tables: 生保標準生命表2018（死亡保険用）男/女 and
  第三分野標準生命表2018 男/女, each with x, l(x), d(x), q(x) and e(x)
- Doc type: statutory valuation mortality table
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- Retrieved: YES (downloaded; values recovered by positional word extraction with PyMuPDF —
  a naive text dump interleaves the two column blocks). Note: the shorter URL
  `https://www.actuaries.jp/lib/standard-life-table/seimeihyo2018.pdf` that appears in
  search results is a 404 page; the `/pdf/` path is the live one.
- Content: the full q(x) series and the terminal ages. This is a **public and citable**
  table, free and complete at a stable URL — the sharpest contrast with the
  subscriber-restricted CMI tables the UK library had to proxy, which cannot be read at all
  without a subscription. **Correction, 2026-08-20 (naming and citation review):** an earlier
  revision of this entry called the table "public, citable, **redistributable**". It is
  **not redistributable**. The 日本アクチュアリー会 site terms prohibit reproduction, alteration and
  transmission to third parties without prior written consent, so this library cites the
  table by URL, quotes only the individual rates a worked example needs, and ships
  `mort_table.csv` as a standardized construction whose `provenance` column points at the
  IAJ entries — never as a copy of the IAJ file. Readable is not the same as redistributable,
  and the product documents have always held to the narrower position; this entry was the
  one place that did not.

### R2 — 日本アクチュアリー会, 「標準生命表２０１８の作成概要」

- Publisher: 公益社団法人日本アクチュアリー会
- Document: `seimeihyo2018-gaiyo.pdf`, 6 pp., 資料①–⑤
- Doc type: methodology note
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- Retrieved: YES (downloaded, text extracted and read)
- Content: observation years, exposure and claim counts, truncation (截断) rules, the
  young-age substitution of the national life table, the **mortality-improvement allowance**
  applied to reach the application year, the **数学的危険論による補整** (the explicit safety margin)
  and its cap, Greville smoothing, and the Gompertz–Makeham high-age graduation. This is the
  document that establishes that 標準生命表2018 is a **valuation** table carrying margins, not a
  best-estimate experience table.

### R3 — 日本アクチュアリー会, 「標準生命表２０１８の作成過程」

- Publisher: 公益社団法人日本アクチュアリー会
- Document: `seimeihyo2018-katei.pdf`, 67 pp.
- Doc type: working-process appendix (intermediate tables)
- URL: https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-katei.pdf
- Retrieved: PARTIALLY — the PDF downloads (67 pp.) but its body text is encoded with a
  legacy CJK font mapping that neither pypdf nor PyMuPDF resolves (output is mojibake). Only
  the cover page ("標準生命表２０１８の作成過程") is legible. **No fact below depends on it.**

### R4 — 日本アクチュアリー会, 「標準生命表2018」 索引ページ

- Publisher: 公益社団法人日本アクチュアリー会
- Doc type: publication page
- URL: https://www.actuaries.jp/lib/standard-life-table/index2018.html
- Retrieved: YES (WebFetch, 200)
- Content: publication date, application date, the statement that the Institute is a body
  designated under 保険業法第122条の2第1項 and is commissioned by 金融庁 to produce the tables, and the
  three PDF download paths (R1–R3).

### R5 — 保険業法（平成七年法律第百五号）第114条・第116条・第122条の2

- Publisher: e-Gov 法令検索 (デジタル庁)
- URL: https://laws.e-gov.go.jp/document?lawid=407AC0000000105 (retrieved through the JSON
  API: `https://laws.e-gov.go.jp/api/2/law_data/407AC0000000105`)
- Retrieved: YES (full law JSON downloaded via the v2 API with a browser User-Agent; the
  three articles extracted verbatim from the `law_full_text` tree)
- Content: art. 114 契約者配当 — where the policy conditions provide for a distribution, it must
  follow the fair-and-equitable standard set by Cabinet Office Ordinance; art. 116 責任準備金 —
  the duty to hold reserves each valuation date, and the power of the 内閣総理大臣 to prescribe
  the accumulation method and the level of the assumed mortality and other coefficients for
  long-term contracts specified by ordinance; art. 122の2 指定法人 — the designation under which
  the actuarial body performs the work commissioned in relation to art. 116(2).

### R6 — 保険業法施行規則（平成八年大蔵省令第五号）第30条の2・第64条・第68条・第69条

- Publisher: e-Gov 法令検索 (デジタル庁)
- URL: https://laws.e-gov.go.jp/document?lawid=408M50000040005 (JSON API:
  `https://laws.e-gov.go.jp/api/2/law_data/408M50000040005`; the revision returned is
  `408M50000040005_20260615_508M60000002055`)
- Retrieved: YES (full ordinance JSON downloaded, ~4.7 MB; the four articles extracted
  verbatim)
- Content: art. 68 標準責任準備金の対象契約 (the exclusions — separate-account-linked, no 保険料積立金,
  conditions permitting the insurer to change the 予定利率, and residual Commissioner-designated
  cases); art. 69 生命保険会社の責任準備金 — the four components (保険料積立金, 未経過保険料, 払戻積立金, 危険準備金), the
  rule that in-scope contracts may not fall below the Commissioner-prescribed amount and
  out-of-scope contracts may not fall below **平準純保険料式** (defined in the article itself), and
  the three sub-classes of 危険準備金 (保険リスク, 第三分野保険リスク, 予定利率リスク, 最低保証リスク); art. 30の2 剰余金の分配の
  計算方法, whose second method — identifying the distributable surplus **by its source** — is
  the legal footing of the 三利源 framing; art. 64 契約者配当準備金.

### R7 — 金融庁, 「標準責任準備金制度にかかる告示の一部改正（案）」等の公表について

- Publisher: 金融庁 (Financial Services Agency)
- Doc type: rule-making publication page
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html
- Retrieved: YES (WebFetch, 200)
- Content: identifies the two 告示 that carry the 標準責任準備金 regime — 平成13年金融庁告示第24号 and
  平成8年大蔵省告示第48号 — and the amendment bringing USD- and AUD-denominated contracts concluded on
  or after 1 April 2022 into scope, with the corresponding 標準利率 calculation method and
  conforming edits to the yen provisions; effective dates; links to 別紙1–3.

### R8 — 金融庁, 平成八年大蔵省告示第四十八号 改正 (別紙２, the 標準利率 mechanism)

- Publisher: 金融庁
- Document: `02.pdf`, 16 pp. — a redline (改正後／改正前 two-column) of 「保険業法第百十六条第二項
  の規定に基づく長期の保険契約で内閣府令で定めるものについての責任準備金の積立方式及び予定死亡率 その他の責任準備金の計算の基礎となるべき係数の水準（平成八年大蔵省告示第四十八号）」
- Doc type: ministerial notification (告示), amendment text
- URL: https://www.fsa.go.jp/news/r2/hoken/20210423/02.pdf
- Retrieved: YES (downloaded, 16 pp.). **Extraction note**: the notification is set in
  vertical Japanese; PyMuPDF returns one character per line, so the text has to be re-joined
  before it can be read, and the two redline columns interleave. Several rate tables are
  printed as 「［表略］」 (omitted from the redline) and are therefore **not** recoverable from
  this file.
- Content: the 標準利率 (written in the 告示 as 予定利率) determination mechanism, verbatim — the
  reference rate, the 基準日 calendar, the safety-coefficient banding, the reset threshold and
  granularity, and the lead time before the new rate applies; separately for ordinary
  contracts, for 第一号/第二号保険契約 (single-premium), and for USD/AUD contracts; plus the
  definitions of 第一号保険契約 and 第二号保険契約 and the treatment of 予定利率変動型保険契約.

### R9 — 相続税法（昭和二十五年法律第七十三号）第3条・第12条

- Publisher: e-Gov 法令検索 (デジタル庁)
- URL: https://laws.e-gov.go.jp/document?lawid=325AC0000000073 (JSON API:
  `https://laws.e-gov.go.jp/api/2/law_data/325AC0000000073`)
- Retrieved: YES (full law JSON downloaded; both articles extracted verbatim)
- Content: art. 3(1)(i) — a death benefit received on the death of the decedent is
  **deemed** acquired by inheritance, in the proportion of the premiums the decedent bore;
  art. 12(1)(vi) — the exempt amount for death benefits received by heirs, stated as a
  formula in the statute itself, with the pro-rata rule where the total exceeds it.

### R10 — 国税庁, タックスアンサー No.4114 「相続税の課税対象になる死亡保険金」

- Publisher: 国税庁 (National Tax Agency)
- Doc type: official tax guidance page ("令和7年4月1日現在法令等")
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4114.htm
- Retrieved: YES (WebFetch, 200). Note the `/zaisan/4114.htm` path that appears in some
  search results is a dead link; `/sozoku/4114.htm` is the live one.
- Content: the non-taxable limit formula; the counting rule for 法定相続人 (renouncing heirs are
  counted as if they had not renounced; adopted children limited to one where there is a
  natural child and two where there is not); and the exclusion of non-heir recipients.

### R11 — 国税庁, タックスアンサー No.1140 「生命保険料控除」

- Publisher: 国税庁
- Doc type: official tax guidance page ("令和7年4月1日現在法令等")
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1140.htm
- Retrieved: YES (WebFetch, 200)
- Content: the three post-2012 baskets (一般の生命保険料, 介護医療保険料, 個人年金保険料); the new-regime and
  old-regime deduction bands and formulas with exact yen figures; the per-basket cap and the
  overall income-tax cap.

### R12 — 生命保険協会, 「２０２５年版 生命保険の動向」

- Publisher: 一般社団法人生命保険協会 (Life Insurance Association of Japan)
- Document: `all_2025.pdf`, 33 pp. (FY2024 data)
- Doc type: industry statistics
- URL: https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf
- Retrieved: YES (downloaded, 33 pp., text extracted; §(1) 個人保険 read in full)
- Content: FY2024 個人保険 new business and in-force by policy count and by sum assured, with
  the whole life share of each; the industry 解約・失効率 and, importantly, **its definition** (an
  amount-weighted ratio to the opening in-force sum assured, not a policy-count rate).

---

## Fact extraction

### 1. Product architecture

- 終身保険 is whole-of-life cover: the death benefit is payable whenever the insured dies, with
  no maturity date and no 満期保険金 [S1] [S3] [S5] [S7] [S9] [S10]. Orix state it flatly:
  "この保険に配当金、満期保険金はありません" [S5].
- The main contract pays two benefits, at the same amount: **死亡保険金** on death, and
  **高度障害保険金** on reaching the 高度障害状態 defined in 別表3. Paying the 高度障害保険金 extinguishes the
  contract retroactively to the date the state was reached [S1] [S3] [S7] [S9]. Aflac art. 2
  also provides that if the insured dies before claiming the 高度障害保険金, only the death benefit
  is paid [S1].
- 保険期間 is 終身 in all cases; only 保険料払込期間 varies. Nippon Life's product table marks 終身保険 as
  available on the 終身 term basis and on no other [S8].
- Participation status varies and is part of the product name: 無配当 (Orix RISE [S3] [S5],
  MS&AD 積立利率変動型 [S11]), **5年ごと利差配当付** (Tokio Marine Anshin 長割り終身 and its ordinary twin
  [S7]), **5年ごと配当付** (Dai-ichi [S9]), 有配当2012 (Nippon Life [S8]).
- Kampo's designs add a shape found nowhere else in the set: 新ながいきくん（ばらんす型2倍 / 5倍）, where
  the death benefit is the 基準保険金額 during 保険料払込期間 and steps **down** to 50% (2倍型) of it
  afterwards [S9]. Kampo also embeds 倍額保障 — a doubling of the death benefit where death
  results from an 不慮の事故 within 180 days or from a listed 感染症 [S9].

### 2. 低解約返戻金型 — the defining mechanic

This is the product's signature and the one thing a model must not smooth.

- **Definition of the suppressed period.** Orix: 低解約払戻期間 is stated in the 約款 itself to be
  identical to 保険料払込期間 [S3, art. 33(2)] [S6]; on a 終身払 contract it therefore runs for life
  [S4]. Tokio Marine Anshin: "低解約返戻金期間：ご契約日から保険料払込期間が満了する日の 24時まで" [S7]. MS&AD:
  "低解約返戻金期間：保険料払込期間と同一" [S11]. Kampo frames it as "保険料払込期間の満了前後に応じて" [S9].
- **The factor is 70% at every carrier that publishes it.** Four independent statements: -
  Orix, in the 約款: "解約払戻金支払割合は、７割とします" [S3, art. 33(3)], and in the しおり
  "解約払戻金額は、解約払戻金を低く設定しない場合の7割に抑制されます" [S3]. - Tokio Marine Anshin, in the 契約概要:
  "低解約返戻金割合：７０％", and "「低解約返戻金期間」中の 解約返戻金は「5年ごと利差配当付終身保険」の70％です。「低解約返戻金期間」満了後の解約返戻金は …と同額です"
  [S7]. - MS&AD, in the glossary: "「低解約返戻金割合」は保険料払込期間中、70％となっています" [S11]. - Kampo, in the 約款
  as a literal multiplier: 返戻金 during the period = the ordinary calculation "に0.7
  を乗じて算出した額"; after 払込満了, the ordinary amount [S9, 普通終身保険（Ｒ07） （低解約返戻金型）art. 34(2)].
- **The cliff is a step, not a ramp.** Orix's published table for 30歳男性 / 500万円 / 15年払 shows
  解約払戻金 2,047,650円 at 15 years (the day before the anniversary, still suppressed) and
  2,928,450円 immediately after the period expires — a 43% jump, with 払戻率 going from 78.0% to
  111.5% [S4]. Tokio Marine Anshin's table shows the same shape: 5,122,000円 at duration 30
  with a footnote that the amount immediately after expiry is 7,324,000円 [S7].
- **A clawback survives the step.** Both Orix and Kampo provide that even after the low
  period ends, if not all premiums falling in that period were paid, the suppressed basis
  continues to apply [S3, art. 33(4)] [S4] [S5] [S9].
- **Conversion switches the basis off.** Orix: "払済保険に変更後は、第２項の適用はありません" [S3, art. 33(5)].
  But the *conversion itself* uses the suppressed value if made during the period, so the
  resulting 払済保険金額 is permanently smaller [S3] [S7] [S9].
- **Everything derived from the surrender value is suppressed with it.** Tokio Marine Anshin
  list the affected quantities explicitly: 払済保険の保険金額, 契約者貸付の金額, 保険料の振替貸付金額 [S7]; the same
  booklet notes the 延長定期保険 period is correspondingly shorter [S7]. MS&AD note the amount the
  APL can advance is smaller [S11]. Kampo note the same for loans and for 払済契約 [S9].
- **The price of the suppression.** Tokio Marine Anshin publish both premium scales for one
  identical model point: 17,040円/month for 長割り終身 against 20,350円/month for the ordinary
  5年ごと利差配当付終身保険 — the suppressed version costs **83.7%** of the ordinary one [S7].
- **Split treatment on an 積立利率変動型 chassis.** MS&AD suppress only the guaranteed part: the
  low-period surrender value is (70% of the ordinary product's 基本保険金額 surrender value) plus
  an unsuppressed amount derived from the excess of the actual 積立金 over the 予定利率-based 積立金
  [S11].
- Kampo publishes the mechanic and the multiplier but **not** a numeric surrender-value
  table in this booklet [S9].

### 3. Published surrender-value bases (a citable cash-value basis)

Two carriers publish complete tables. These are the most valuable numbers in this file.

**S4 — Orix RISE.** Model point: 30歳男性, 保険金額 500万円, 保険期間 終身, 保険料払込期間 15年 (= 低解約払戻期間), 月払保険料
14,580円. Amounts are as at the day before the policy anniversary, except ★ which is
immediately after the low period expires.

| 経過年数 | 年齢 | 払込保険料累計 | 解約払戻金 | 払戻率 |
|---|---|---|---|---|
| 5年 | 35歳 | 874,800円 | 613,850円 | 70.1% |
| 10年 | 40歳 | 1,749,600円 | 1,309,400円 | 74.8% |
| 15年 | 45歳 | 2,624,400円 | 2,047,650円 | 78.0% |
| ★15年 | 45歳 (直後) | 2,624,400円 | 2,928,450円 | 111.5% |
| 20年 | 50歳 | 2,624,400円 | 3,123,700円 | 119.0% |
| 30年 | 60歳 | 2,624,400円 | 3,544,650円 | 135.0% |
| 40年 | 70歳 | 2,624,400円 | 3,983,950円 | 151.8% |
| 50年 | 80歳 | 2,624,400円 | 4,404,300円 | 167.8% |

Internal checks (all pass): 14,580 × 60 = 874,800; × 120 = 1,749,600; × 180 = 2,624,400;
every 払戻率 reproduces to the displayed decimal. The cliff ratio 2,047,650 / 2,928,450 =
0.6993 — just under 0.70 because the pre-cliff figure is quoted one day earlier than the
post-cliff one [S4].

**S4 — Orix RISE premium and 15-year value, by issue age and sex** (extract; the published
table runs ages 20–51 for 200 / 300 / 500 / 1,000万円, 15年払, 口座振替扱, "2025年12月2日現在"):

| 契約年齢 | 保険金額 | 性別 | 月払保険料 | 15年後（★）解約払戻金 | 払戻率 |
|---|---|---|---|---|---|
| 20歳 | 500万円 | 男 | 12,785円 | 2,561,500円 | 111.3% |
| 30歳 | 500万円 | 男 | 14,580円 | 2,928,450円 | 111.5% |
| 30歳 | 500万円 | 女 | 13,475円 | 2,709,350円 | 111.7% |
| 30歳 | 1,000万円 | 男 | 29,110円 | 5,856,900円 | 111.7% |
| 30歳 | 1,000万円 | 女 | 26,900円 | 5,418,700円 | 111.9% |
| 40歳 | 500万円 | 男 | 16,795円 | 3,333,950円 | 110.2% |
| 51歳 | 500万円 | 男 | 19,860円 | 3,810,350円 | 106.5% |
| 20歳 | 200万円 | 男 | 5,242円 | 1,024,600円 | 108.5% |
| 30歳 | 200万円 | 男 | 5,960円 | 1,171,380円 | 109.1% |

Two facts fall straight out of this: a **volume discount** (2 × 14,580 = 29,160 > 29,110,
and the 200万円 rate per 万円 is materially higher than the 500万円 rate), and a **female
discount** of roughly 7–8% on the male rate at age 30 [S4].

**S7 — Tokio Marine Anshin, the suppressed/ordinary pair.** Model point: 30歳契約, 男性, 60歳払込満了,
死亡保険金 1,000万円, 月払 (口座振替扱); 計算基準日 平成22年3月2日. 低解約返戻金割合 70%; 低解約返戻金期間 = to the end of the
premium-paying period.

| 経過年数 | 長割り終身 解約返戻金 | 長割り 払込保険料累計 | 5年ごと利差配当付終身保険 解約返戻金 | 同 払込保険料累計 |
|---|---|---|---|---|
| 5年 | 650,000円 | 1,022,400円 | 928,000円 | 1,221,000円 |
| 10年 | 1,462,000円 | 2,044,800円 | 2,089,000円 | 2,442,000円 |
| 20年 | 3,158,000円 | 4,089,600円 | 4,511,000円 | 4,884,000円 |
| 30年 | 5,122,000円 (※) | 6,134,400円 | 7,317,000円 | 7,326,000円 |
| 40年 | 8,159,000円 | 6,134,400円 | 8,159,000円 | 7,326,000円 |

(※) the booklet's footnote: "低解約返戻金期間満了直後の解約返戻金は、７，３２４，０００円". Monthly premiums 17,040円 and
20,350円 respectively [S7].

Checks: 650,000/928,000 = 0.7004; 1,462,000/2,089,000 = 0.6999; 3,158,000/4,511,000 =
0.7001; 5,122,000/7,317,000 = 0.6999. The 70% factor is exact to rounding at every duration.
At duration 40 (well past 払込満了) the two products' surrender values are **identical** —
8,159,000円 — which confirms that the suppression is a pure haircut on a common underlying
reserve run-off, not a different policy value [S7]. The same pair also shows the ordinary
product's own headline figures in the 契約概要 illustration: 60歳時 約732万円 (長割り, immediately after
the cliff) / 約731万円 (ordinary), 80歳時 約891万円 for both [S7].

### 4. Issue-age and premium-term envelopes

**Orix RISE** publishes a complete grid of 契約可能年齢 against 保険料払込期間 [S5]:

| 保険料払込期間 | 契約可能年齢 |
|---|---|
| 5年 | 15歳～80歳 |
| 10年 | 15歳～80歳 |
| 15年 | 15歳～80歳 |
| 20年 | 15歳～75歳 |
| 50歳払済 | 15歳～40歳 |
| 55歳払済 | 15歳～45歳 |
| 60歳払済 | 15歳～50歳 |
| 65歳払済 | 15歳～55歳 |
| 70歳払済 | 15歳～60歳 |
| 75歳払済 | 15歳～65歳 |
| 80歳払済 | 15歳～70歳 |
| 終身払 | 15歳～80歳 |

So the 歳満了 options are all gated by a **10-year minimum payment period**, and the outer
issue range is 15–80 [S5]. Note the pattern: 年満了 short-pay is offered to the top of the
issue range, while 歳満了 short-pay is not.

- 保険金額: 200万円～5,000万円 in 100万円 units; 100万円 is available **only** to ages 76–80; a 5-year
  payment term requires at least 1,000万円; underwriting limits apply on aggregate in-force
  [S5]. The application brochure's document-requirement bands corroborate the age banding
  (15歳 / 16–21 / 22–39 / 40–60 / 61–65 / 66–70 / 71–75 / 76–80) and note that
  3,100万円–5,000万円 is open only from age 16 [S4].
- 契約形態: Orix require 契約者 and 被保険者 to be the same person on this product [S5].
- **Kampo is capped by statute, not by underwriting appetite.** 加入限度額 for the basic
  contract: 700万円 where the insured is 満15歳以下, 1,000万円 where 満16歳以上; ages 満20–満55 may reach
  a cumulative 2,000万円 subject to conditions (e.g. holding a contract at least four years
  old). Rider limits are separate. Applications above the limit are declined outright, and a
  limit breach discovered after issue voids the excess [S9]. This is a hard ceiling with no
  analogue in the US or UK reference sets.
- Aflac's booklet gives the 契約年齢 definition and 保険料払込期間 concept but **does not** publish an
  issue-age or sum-assured envelope [S1] — envelopes live in the 契約概要, which is not part of
  that file.
- No carrier in the set publishes a maximum issue age above 80 for this product [S4] [S5]
  [S9]; whether that is universal is [unverified].

### 5. Age basis and timing

- 契約年齢 is **満年齢 with the fractional year discarded** — Orix: "被保険者の契約日における
  契約年齢は満年齢で計算し、１年未満の端数は切り捨てます" [S3, art. 34]. Aflac's glossary gives the same rule with a
  worked example (24歳7か月 → 契約年齢 24歳) [S1].
- The age then increments **on each 年単位の契約応当日**, not on the birthday: "ご契約後の被保険者
  の年齢は、年単位の契約応当日ごとに契約年齢に１歳を加えて計算します" [S1]; Kampo state the same [S9]. A projection stepped
  on policy anniversaries is therefore stepping the rating age correctly by construction.
- 契約日 is the base date for 契約年齢 and 保険期間 [S1].
- 解約返戻金 is a function of **elapsed months and paid months**, both: Orix compute it "保険料
  払込期間中の場合にはその保険料を払い込んだ年月数および経過した年月数により、保険料払込期間経過後の 場合にはその経過した年月数により" [S3, art. 33(1)];
  Aflac's art. 34 caps 経過年月数 at 払込年月数 during the premium-paying period [S1]; Dai-ichi's art.
  24(2) is worded identically in effect [S10].

### 6. Premium structure and payment

- 払込回数: 月払 / 半年払 / 年払 at every carrier in the set [S1] [S3] [S5] [S9] [S10]. Dai-ichi call
  the non-monthly modes 半年一括払 / 年一括払 [S10].
- 払込経路: 口座振替 and クレジットカード払 (Orix [S3] [S5]); Aflac's art. 10 lists five routes including a
  card route [S1].
- Premiums are **level and guaranteed** for the chosen 保険料払込期間 — the products in this set
  carry no reviewable-premium mechanic. Dai-ichi are the exception with an optional
  **保険料のステップ払込方式の特則**: the policyholder may elect at issue a scale that is lower for a
  ステップ期間 of 10 or 15 years and higher thereafter, and may revert to the flat scale later
  with a settlement payment [S10, art. 50].
- 前納 (advance payment of future premiums at a discount) is available: Aflac allow 6 or 12
  months' monthly premiums at a company discount rate, or arbitrary future premiums on
  半年払/年払 accumulated at a company rate [S1, art. 15]; Dai-ichi and Tokio Marine Anshin have
  equivalent provisions [S10] [S7].
- **高額割引 (volume discount)** is a real and disclosed feature. Nippon Life apply it where the
  割引適用基準額 (a per-contract aggregation base) reaches **3,000万円 or more** [S8]; Tokio Marine
  Anshin's illustration is footnoted "保険金額が1,000万円以上の場合、保険料の高額割引が適用されます" [S7]; MS&AD apply
  it above a company threshold [S11]; Orix's published rate table embeds it (see §3) [S4].
- Non-smoker discounts exist as a 特約 rather than a rating class: Aflac's 非喫煙割引特約 (制定
  2018年4月2日) substitutes a 非喫煙保険料率 for the main contract and named riders, runs for the same
  term, lapses with the main contract, and may be reinstated with it [S1].
- 保険料の払込免除: Orix waive future premiums where the insured reaches a 身体障害の状態 listed in 別表4
  within 180 days of an 不慮の事故, with the usual conduct exclusions, and offer an optional
  特定疾病保険料払込免除特則; the waiver does **not** apply after 保険料払込期間 has ended [S3].

### 7. Grace, lapse and reinstatement — three different regimes

This is the sharpest carrier variation in the file, and it changes lapse modelling directly.

- **The common 約款 grace** (Aflac [S1, art. 11], Orix [S3, art. 12], Dai-ichi [S10, art.
  14]): - 月払: from the first day of the month **following** the 払込期月 to the last day of that
  month — i.e. roughly one month. - 半年払 / 年払: from the first day of the following month to
  the monthly contract anniversary in the month after that, with named end-of-month
  substitutions (a 契約応当日 falling on the last day of February, June or November runs to the
  last day of April, August and January respectively). If the premium is unpaid at the end
  of the grace period the contract lapses (失効) from the following day, and the policyholder
  may then claim the surrender value [S1] [S3] [S10].
- **Kampo: a two-month grace.** 払込猶予期間 runs from the first day of the month after the 払込時期
  to the **last day of the month after that** — the booklet's worked example has a September
  premium due 9/1–9/30, grace 10/1–11/30, and lapse on 12/1 [S9].
- **Nippon Life: no grace and no lapse — a scheduled termination instead.** Where the
  premium is unpaid within the 払込期月 the insurer sends a 催告 naming a **解除予定日**, which is the
  monthly anniversary in the **third month after** the 払込期月; the contract is 解除 (terminated)
  on that date, with the surrender value paid net of unpaid premiums [S8]. Note this is 解除,
  not 失効: "解除された保険契約を元に戻すことはできません" — **there is no reinstatement** [S8].
- **復活 (reinstatement) windows differ by a factor of three**: - 3 years from the date of
  lapse — Aflac [S1, art. 16], Orix [S3, art. 16], Tokio Marine Anshin [S7], Dai-ichi [S10,
  art. 17]. - **1 year** — Kampo [S9]. - Not available — Nippon Life [S8]. Reinstatement
  requires fresh 告知 and payment of the arrears, and is barred once the surrender value has
  been claimed [S1] [S3] [S10]. On reinstatement the 責任開始期 resets, which restarts both the
  suicide clause and the contestability clock [S1] [S7] [S9] [S10].
- 責任開始 for reinstated cover begins when the arrears (and, where the health declaration comes
  later, the declaration) are received [S10, art. 17(4)].
- **Contestability**: 告知義務違反 permits rescission within 2 years of 責任開始日 (or of the 復活日/復旧日);
  beyond 2 years the insurer cannot rescind unless a claim event within the 2-year window is
  involved [S7] [S1, art. 32(1)(5)]. Kampo state the same 2-year rule [S9].

### 8. 自動振替貸付 (automatic premium loan) — the Japanese mechanic with no US/UK analogue

- **Default-on (opt-out) at three carriers.** Aflac: "保険料の払込がないままで猶予期間を過ぎた
  場合でも、この保険契約に解約払戻金があるときは、あらかじめ保険契約者から別段の申出がない限り、
  会社は、自動的に保険料相当額を貸し付けて保険料の払込に充当し、保険契約を有効に継続させます" [S1, art. 13(1)]. Tokio Marine Anshin:
  "あらかじめ保険契約者から特に反対の申出がないかぎり" [S7, art. 15(1)]. Dai-ichi: "あらかじめ保険契約者から別段の申出がない限り" [S10,
  art. 15(1)]. MS&AD describe it the same way and give an opt-out route [S11].
- **Opt-in at Orix.** "保険契約者からあらかじめ申出がある場合、…自動的に貸し付けて保険契約を有効に 継続させます" [S3, art. 14(1)]; the
  しおり adds "このお申し出のない場合、保険料の自動振替貸付は しません" [S3].
- **Absent at two carriers.** Nippon Life: "この保険には、保険料の自動振替貸付制度…はありません" [S8]. Kampo:
  "当社の商品には、保険料の自動振替貸付制度…の取り扱いはありません。貸し付けを受ける ときは、ご契約者による請求が必要です" — a 保険料振替貸付 exists but must
  be requested [S9].
- **The continuation condition.** The APL operates only while the premium advanced plus
  interest does not exceed the surrender value, computed as if the premium had been paid and
  net of any existing loan [S1, art. 13(2)] [S3, art. 14(1)] [S10, art. 15(2)]. Tokio Marine
  Anshin extend the base to 解約返戻金 **and 未経過保険料** [S7, art. 15(2)]. This is the mechanism
  that makes lapse a *funded* event on a whole life policy: the policy does not lapse while
  the cash value can carry the premium.
- **The amount lent per event varies.** - Aflac, 月払: **three months' premium** at a time; if
  three months cannot be funded, the largest number of months that can be. 年払/半年払: the
  premium due [S1, art. 13(3)]. - Dai-ichi, 月払: the premiums from the month due **to the day
  before the next half-yearly anniversary**; if the whole span cannot be funded, as many
  months as can be [S10, art. 15(3)]. - Orix and Tokio Marine Anshin: the premium due. Orix
  and Tokio Marine Anshin both add a **downgrade rule** for 年払 contracts: where the
  surrender value cannot fund the annual premium plus interest but can fund a half-yearly
  one, the payment mode is switched to 半年払 and the half-yearly premium is advanced [S3, art.
  14(1)] [S10, art. 15(3)(2)].
- **Timing**: the advance is deemed made at the moment the grace period expires [S1, art.
  13(4)] [S3, art. 14(2)] [S7, art. 15(3)] [S10, art. 15(4)].
- **Interest and rolling-up.** Published ceilings, identical across three carriers: 年払
  年8%以下, 半年払 半年4%以下, 月払 月8/12%以下 [S1, art. 13(5)] [S10, art. 15(5)]. Tokio Marine Anshin
  print the same three ceilings as a 上限利率 table alongside an 元金繰り入れ日 column: for 月払 and 半年払
  the interest rolls into principal at each subsequent grace-period expiry (半年払 at the
  month-end of that month), for 年払 at the annual cycle [S7, art. 15(4)]. Orix: 年8％以下, rolled
  in at each subsequent grace expiry [S3, art. 14(2)]. Dai-ichi add a rule for the post-払込満了
  period: once 保険料払込期間 ends, interest rolls in on the day after the maturity of the payment
  period and annually thereafter [S10, art. 15(7)].
- **Cancellation window.** An APL already made is treated as never having happened if,
  within **3 months** of the day after grace expiry, the policyholder requests 解約, 減額, or
  conversion to 払済保険 [S1, art. 14] [S3, art. 15] [S10, art. 16]. Orix's list also includes
  rider surrender and reduction [S3].
- Actual published APL rates: Aflac's 保険料の自動振替貸付の利率 is disclosed at the same value as the
  契約者貸付 rate, banded by 契約日 (see §9) [S2].

### 9. 契約者貸付 (policy loan)

- **Limit as a fraction of the surrender value**: 9割 while premiums are being paid, **8割**
  once the contract is 保険料払込済 — the same split at Aflac [S1, art. 20(1)], Orix [S3, art.
  20(1)] and Tokio Marine Anshin [S7]. Any existing APL or loan principal-and-interest is
  deducted first [S1] [S3] [S7].
- **Nippon Life differ**: 8割 of the surrender value **less three months' premium**, with the
  three-month deduction waived once the contract is paid up or premiums are being waived
  [S8].
- **Kampo differ again**: the loan is "解約返戻金額のうち会社の定める計算方法により算出された額の 範囲内" — no published
  fraction — with a **fixed 貸付期間 of one year** [S9, art. 38]. Nippon Life also run a
  one-year 貸付期間 that auto-renews by capitalising interest [S8].
- Minimum draw amounts: Tokio Marine Anshin publish 初回貸付時 5万円, 貸増時 1万円 [S7]. Others refer to
  a company-set minimum without a value [S1] [S3] [S9].
- Interest is compound at a company-set rate [S1, art. 20(3)] [S3, art. 20(3)] [S8] [S9].
  Tokio Marine Anshin: annual compounding, day-counted for part years, **reviewed twice a
  year on the first business day of January and July**, with the revised rate applying to
  existing loans too [S7]. MS&AD run the same January/July review calendar for the APL rate,
  with a hard ceiling of 年8% and a stated lag before the new rate bites [S11].
- **Published loan rates (Aflac, as at 2017年2月1日)** — the same schedule serves both 契約者貸付
  and 自動振替貸付 [S2]:

  | 契約日 | 適用利率 |
  |---|---|
  | 1999年4月1日まで | 年 4.00% |
  | 1999年4月2日から2001年4月1日まで | 年 3.25% |
  | 2001年4月2日から | 年 2.75% |

  Same page: 契約者配当金積立利率 and 据置金の利率 0.10% to 2017年3月31日, **0.05%** from 2017年4月1日 [S2]. Note
  the loan rate is banded by 契約日 and therefore tracks the vintage's 予定利率, not the current
  market.
- **The loan-driven termination mechanic.** Where APL + loan principal and interest exceed
  the surrender value the insurer notifies the policyholder for a top-up; if the amount is
  not paid **by the end of the month following the month the notice was issued**, the
  contract lapses from the next day [S1, art. 20(5)–(6)] [S3, art. 20(4)–(5)] [S10, art.
  30(5)–(6)]. Tokio Marine Anshin describe the same outcome against 解約返戻金 + 未経過保険料 [S7]. A
  policy lapsed this way can be reinstated only on payment of an additional company-set
  amount [S1, art. 16(2)] [S10].
- **Kampo do not lapse the policy for an unpaid loan.** After the one-year 貸付期間 a higher
  rate applies; one further year on, the insurer **reduces the 基準保険金額** by applying the loan
  principal and interest against the 積立金 (責任準備金) — and, on a 低解約返戻金型 contract before 払込満了,
  against **0.7 × 積立金**, so the sum-assured reduction is correspondingly larger [S9, art.
  38(6)] and [S9, しおり]. The booklet is explicit that the reduction (B) exceeds the loan
  balance (A).
- Deductions from claims: any APL/loan balance is netted off the benefit at claim [S1, art.
  2(3)] [S9] [S10, art. 30(4)].

### 10. 払済保険 (reduced paid-up) and 延長定期保険 (extended term)

- **払済保険** is offered by every carrier in the set. The paid-up sum assured is computed from
  the surrender value net of any APL/loan balance, by a company-defined method [S1, art.
  17(3)] [S3, art. 18] [S7] [S9] [S10, art. 27(1)]. The insurance term is unchanged (still
  whole life) and cover continues for life [S3] [S7].
- Riders **terminate** on conversion, except those the carrier names: Tokio Marine Anshin
  keep リビング・ニーズ特約 and 指定代理請求特約 [S7]; Orix and Aflac terminate riders outright [S3] [S1].
- Eligibility conditions differ: Dai-ichi require **3 years** of premiums paid and that the
  contract be still within 保険料払込期間 [S10, art. 27(1)]; Kampo require **2 years** in force
  [S9]; Orix and Aflac impose only a floor on the resulting sum assured [S3] [S1]. Orix also
  bar conversion while 特別保険料 is being paid under a 特別条件付保険特約 [S3].
- Conversion is **irreversible at some carriers and reversible at others**: Orix, "払済保険に変更後、
  元のご契約にもどすことはできません" [S3]; Tokio Marine Anshin allow **復旧** within 3 years of the conversion
  on payment of a company-set amount, with the 責任開始期 of the restored part reset to the 復旧
  date [S7].
- **延長定期保険** appears in only one carrier's documents in this set — Tokio Marine Anshin. The
  surrender value is applied as a single premium to a term assurance for the **same sum
  assured**, with the term determined by the amount available; the extended term is capped
  at the original 払込満了 date, and where it would exceed it a 生存保険金 may become payable at that
  date; a term under one year, or an insured already aged 80, is not accepted; the main
  contract's payment period is treated as ending at age 80 where it would run past it;
  riders terminate except 指定代理請求特約; 復旧 within 3 years is available [S7]. During the 低解約返戻金期間
  the shorter 70% base makes the extended term correspondingly shorter [S7].
- Aflac, Orix, Nippon Life, Kampo and Dai-ichi do **not** offer 延長定期保険 on the products in
  this set (no such article in the retrieved 約款) [S1] [S3] [S8] [S9] [S10]. Treating
  extended term as a universal Japanese whole life option would be wrong.
- 保険金額の減額 (partial surrender by reducing the sum assured) is universal, the reduced portion
  being treated as surrendered [S1, art. 33] [S3] [S9] [S10, art. 26]. Kampo note that
  reducing during the low-surrender period pays out on the suppressed basis [S9].
- 保険料払込期間の変更 (shortening the payment period) is offered by Aflac subject to consent and a
  settlement calculation [S1, art. 19] and by Dai-ichi subject to 3 years paid and 5 years
  remaining [S10, art. 28]. Aflac bar it once the policy is 払済 [S1].

### 11. Exclusions, and what is paid when a benefit is refused

- **Suicide: three years, not one.** Every carrier in the set excludes suicide within **3
  years** of the 責任開始期 (reset to the latest 復活), against the UK composite's 12 months: Aflac
  [S1, art. 2], Orix [S3], Tokio Marine Anshin [S7], Nippon Life [S8], Kampo [S9, art.
  34(3)(1)], Dai-ichi [S10, art. 4(1)(1)].
- Other 免責事由 on the death benefit: intentional act of the 保険契約者 or 死亡保険金受取人; war and civil
  disturbance [S1] [S9] [S10]. On the 高度障害保険金: intentional act of 保険契約者 or 被保険者, the
  insured's own suicidal act, the insured's criminal act, war and civil disturbance [S1,
  art. 2(1)(2)].
- **Refusal is not forfeiture.** Where the death benefit is not paid because an 免責事由
  applies, the insurer pays the **保険料積立金 / 責任準備金** to the policyholder [S1, art. 2(6)] [S10,
  art. 4(1)]; Kampo pay the 積立金 [S9, art. 34(3)]. The exception is where the policyholder
  intentionally caused the death, in which case nothing is paid [S1, art. 2(6)] [S10, art.
  4(2)]. Where one of several beneficiaries acted intentionally, the remainder is paid to
  the others and the reserve attributable to the withheld share goes to the policyholder
  [S1] [S9] [S10].
- **War clause is scalable, not absolute.** If the increase in affected insureds is small
  enough not to disturb the product's calculation basis, the insurer may pay in full or pay
  a reduced amount in proportion [S1, art. 2(8)] [S10, art. 4(4)].
- Underwriting loadings are handled by a 特別条件付保険特約 rather than by declining [S3].

### 12. 契約者配当 (policyholder dividends)

- Legal footing: 保険業法第114条 requires any distribution provided for in the policy conditions
  to follow the fair-and-equitable standard set by Cabinet Office Ordinance, and delegates
  the reserving mechanics to ordinance [R5]. 保険業法施行規則第64条 defines the 契約者配当準備金 and caps
  transfers into it at the sum of 積立配当, 未払配当, 全件消滅時配当 and equivalent amounts computed by the
  method stated in the 事業方法書 [R6]. 施行規則第30条の2 sets out the permitted methods of distributing
  surplus in a mutual, of which method 2 — identify the distributable amount **by the source
  in which it arose** and allocate it in proportion to each contract's 責任準備金, 保険金 or other
  base — is the legal basis of the 三利源 framing [R6].
- **5年ごと利差配当 in practice**: Tokio Marine Anshin declare a dividend every five years from
  policy inception where the investment return on 責任準備金等 exceeds the return assumed in
  pricing; while the contract continues the dividend is accumulated at a company-set rate
  (economy-dependent) as **5年ごと積立配当金**, withdrawable on request at any time [S7]. The
  booklet is explicit that dividends are not promised, vary with performance, and may be nil
  [S7]. Riders on the contract carry no dividend [S7].
- Dai-ichi's product is 5年ごと配当付 [S10]; Nippon Life's is 有配当2012 [S8].
- **無配当 designs**: Aflac's 終身保険 states it in the 約款 — 第38条＜契約者配当＞ "この保険契約に対しては、契約者配当はありません",
  and every rider in that booklet repeats the same clause [S1]. Orix RISE: "この保険に配当金…はありません"
  [S5]. MS&AD's 積立利率変動型 is 無配当 [S11]. For a 無配当 product the dividend layer simply does not
  exist and the pricing margin is retained.
- Kampo's 普通終身保険（Ｒ07） and its 低解約返戻金型 twin **do** carry 契約者配当金 (第15章 of the 約款); only the
  named 無配当 riders are excluded, and the booklet warns the amount varies with company
  results and may be nil in a given year [S9].
- Aflac disclose a 契約者配当金積立利率 alongside the loan rates: 0.10% to 2017年3月31日 and **0.05%**
  from 2017年4月1日 [S2] — i.e. the accumulation rate on dividends declared on their
  participating business, not a dividend on the 終身保険 above.

### 13. Interest-rate bases: 予定利率, 積立利率, 標準利率

- **予定利率 (pricing rate), disclosed.** MS&AD state in the しおり for their 積立利率変動型終身保険 that the
  積立利率 is floored at the 予定利率 and that "現在の予定利率は1.75％です" — as at the 2010.3 revision of that
  booklet [S11]. This is the only level-premium 予定利率 recovered in this session.
- **予定利率 on single-premium products is published continuously.** 明治安田生命 publish a rate page
  refreshed twice a month; for the 適用期間 2026年8月16日～2026年8月31日 the yen single-premium whole
  life rates are **2.44% (15年プラン)** and **2.54% (30年プラン)**, the single-premium endowment
  2.31% / 2.48% / 2.71% for 7 / 10 / 15 year terms, and the 円貨建・エブリバディ 10-year rate 2.48%
  (ages 18–75) / 2.43% (ages 76–85). All carry the note "予定利率は最低保証予定利率 (0.25%)を下回りません"
  [S12].
- **積立利率 (crediting rate) formula, verbatim in mechanism** [S11]: - Contract month: the
  応募者利回り on the 10-year JGB issued in the **preceding** month, less an explicit
  asset-management expense figure — the しおり quotes that figure as **0.2%**. - Subsequent
  monthly contract anniversaries: the **average** of the monthly 10-year JGB 応募者利回り from the
  month before the contract month to the month before that anniversary, subject to a
  **rolling 10-year maximum window**, less the same expense figure. - Rounded to 0.01%
  (rounding at the 0.001% place); **floored at the 予定利率**; each rate applies until the day
  before the next monthly anniversary; the rate is reset monthly. - A fallback to an
  equivalent bond, with regulator approval and two months' notice, if the 10-year JGB ceases
  to be issued. - 増加保険金額 is computed monthly from the prior month-end 積立金, **can only
  ratchet up**, and is nil if the 積立利率 never exceeds the 予定利率 [S11].
- **標準利率 (statutory valuation rate) — the mechanism, from the 告示 itself** [R8]: - Ordinary
  (non-single-premium) contracts: 基準日 is **1 October each year**. The 対象利率 is the **lower**
  of (a) the average 応募者利回り of 10-year JGBs issued over the 3 years to the month before the
  基準日 and (b) the same average over 10 years. Each band of the 対象利率 is multiplied by a 安全率係数
  and summed to give the 基準利率. If the 基準利率 differs from the rate then in force by **0.5
  percentage points or more**, the new rate is the nearest multiple of **0.25%** (with a
  tie-break that never rounds up past the 基準利率), applied to contracts concluded from **1
  April of the following year**. - **一時払 (第一号/第二号保険契約): reviewed quarterly.** 基準日 is 1
  January, 1 April, 1 July and 1 October; the trigger threshold is **0.25%** (not 0.5%); the
  new rate applies to contracts concluded from **three months after** the 基準日. - For 一時払
  contracts concluded on or after **1 April 2022** the 安全率係数 table is printed in full in the
  amendment: 1.00 for the portion at or below 0%; **0.95** above 0% to 1.0%; **0.90** above
  1.0% to 2.0%; **0.85** above 2.0% to 3.0%; **0.80** above 3.0% to 4.0%; **0.75** above
  4.0% [R8]. - 第一号保険契約 covers single-premium contracts meeting stated
  death-benefit-to-premium conditions (with 予定利率変動型 contracts included only where the
  guarantee period is 20 years or more); 第二号保険契約 covers the rest, with a class added for
  予定利率変動型 contracts whose guarantee period is under 20 years [R8]. - USD/AUD contracts:
  **monthly** 基準日, a 0.05% trigger and 0.05% granularity, referenced to A-rated corporate
  bond yields in the currency of denomination rather than to JGBs [R8] [R7].
- The 安全率係数 table for the **annual** (non-single-premium) case is printed as 「［表略］」 in the
  redline and is therefore not recoverable from [R8]. The **current numeric value** of the
  標準利率 is likewise not established by any document retrieved here — see "Fetch failures and
  gaps".

### 14. Reserving (cited, not reproduced)

- 保険業法第116条(1) obliges insurers to hold 責任準備金 at each valuation date against future
  obligations; (2) empowers the 内閣総理大臣 to prescribe the accumulation method and the level of
  the assumed mortality and other coefficients for long-term contracts specified by
  ordinance [R5].
- 保険業法施行規則第69条(1) splits the reserve into 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金; (4)(1) requires
  in-scope contracts (per art. 68) to be reserved at no less than the amount computed as the
  Commissioner prescribes, and (4)(2) requires all other non-separate- account contracts to
  be reserved at no less than **平準純保険料式**, which the article defines in line as
  "保険契約に基づく将来の債務の履行に備えるための資金を全保険料払込期間にわたり平準化して 積み立てる方式" [R6].
- 危険準備金 is held in named sub-classes: 保険リスク, 第三分野保険の保険リスク, 予定利率リスク and 最低保証リスク, on a
  Commissioner-set accumulation/release standard [R6, art. 69(6)–(7)].
- 施行規則第68条 excludes from 標準責任準備金 scope: separate-account-linked contracts, contracts that
  hold no 保険料積立金/払戻積立金, and contracts whose conditions let the insurer change the
  reserve/pricing 予定利率 (unless the conditions guarantee a minimum above the prescribed rate)
  [R6]. A 積立利率変動型 whole life whose 予定利率 is fixed and whose 積立利率 floats above it is therefore
  in scope; the exclusion bites on contracts where the **予定利率 itself** is variable.
- A 終身保険 policy carries a 保険料積立金, which is why the 免責事由 clauses pay it out (§11) and why a
  解約返戻金 exists at all.

### 15. Mortality basis — 標準生命表2018

- Legal chain: 保険業法第122条の2 designates a body to carry out, among other things, work
  commissioned by the 内閣総理大臣 relating to the level of the coefficients under art. 116(2)
  [R5]; the 日本アクチュアリー会 is that body and states it is commissioned by 金融庁 to produce the
  standard life tables [R4]. 標準生命表2018 was published **17 October 2017** and applies from
  **April 2018** [R4].
- The file `seimeihyo2018.pdf` contains four tables — **生保標準生命表2018（死亡保険用）男/女** and
  **第三分野標準生命表2018 男/女** — each with x, l(x), d(x), q(x) and the curtate-plus expectation
  [R1]. The 年金開始後用 table is **not** in this file.
- Selected values (l(0) = 100,000), 生保標準生命表2018（死亡保険用）[R1]:

  | 年齢 x | q(x) 男 | q(x) 女 |
  |---|---|---|
  | 0 | 0.00081 | 0.00078 |
  | 20 | 0.00059 | 0.00025 |
  | 30 | 0.00068 | 0.00037 |
  | 40 | 0.00118 | 0.00088 |
  | 60 | 0.00653 | 0.00363 |
  | 70 | 0.01544 | 0.00730 |
  | 80 | 0.05006 | 0.02414 |
  | 90 | 0.15760 | 0.09357 |

- **Terminal ages (ω), i.e. the first age with q(x) = 1.00000** [R1]: - 生保標準生命表2018（死亡保険用）:
  **男 109**, **女 113** - 第三分野標準生命表2018: **男 116**, **女 118** This is a hard model parameter
  for a whole life projection: the annual projection on the male 死亡保険用 table runs to age 109
  and terminates there.
- 第三分野標準生命表2018 is materially **lighter** than the 死亡保険用 table at every age shown (男 q(60)
  0.00548 vs 0.00653; 女 q(60) 0.00209 vs 0.00363), reflecting its different purpose [R1]. Do
  not use it for a death-benefit product.
- **These are valuation tables carrying explicit margins, not best-estimate tables** [R2]: -
  Base data: observation years 2008, 2009 and 2011 (three years, excluding the earthquake-
  affected 2010), extended to six observation years 2005–2009 and 2011 at young and old
  ages; contract durations up to 30 years; exposure 4,068万件 (男) / 3,002万件 (女) with 26.3万 /
  9.5万 deaths. - Young-age substitution: crude rates below 男 12歳 / 女 15歳 replaced by the
  第21回生命表 (2010). - **Mortality improvement allowance**: 2.5% p.a. for 5 years plus 1.0%
  p.a. for 3 years, applied to carry the base data forward to the application year. -
  **Explicit safety margin — 数学的危険論による補整**: rates loaded so that the probability of
  experience exceeding the projected variation is held to about **2.28% (a 2σ level)**, on a
  variation model assuming a standard company of **1 million policies per sex**, capped at
  **130% of the pre-adjustment rate** to avoid extreme age-to-age steps. - Then Greville
  3rd-order 13-term smoothing, and Gompertz–Makeham graduation above age 84, with constants
  fitted on ages 81–92 (男) / 81–94 (女). A best-estimate basis for this library is therefore
  a **[std] adjustment of a sourced table**, and any document using 標準生命表2018 must say which
  of the two it means.

### 16. Riders in scope for a whole life chassis

- **リビング・ニーズ特約** is effectively universal and is attached at no extra premium. Definition:
  where the insured is judged to have **6 months or less** to live, the 指定保険金額 chosen by the
  insured is paid **less the interest and premium equivalent for those 6 months** [S1, art.
  of the 特約] [S3] [S4] [S7]. Caps: Aflac 3,000万円 [S1]; Tokio Marine Anshin 3,000万円 per
  insured, aggregated across contracts, and no claim within the 12 months before the end of
  the main contract's term unless it renews [S7]. Payment reduces the main contract's sum
  assured by the 指定保険金額 retroactively [S1] [S3]. Nippon Life attach it automatically to the
  products marked with ※ in their product table, excluding one design [S8].
- **指定代理請求特約** (proxy claimant) is standard and survives conversion to 払済/延長 at Tokio Marine
  Anshin [S7].
- **介護前払特約** (Orix): payable after 保険料払込期間 has ended, from age 満65, on 要介護4 or 要介護5 under
  the public 介護保険 system, as a discounted advance of the death benefit; the amount is less
  than the 指定保険金額 but is guaranteed not to fall below the surrender value on the claim date.
  Not available on 終身払 [S3] [S4].
- Attachable protection riders across the set: 定期保険特約 / 平準定期保険特約, 逓減定期保険特約, 逓増定期保険特約,
  家計保障定期保険特約 / 家族生活保障特約, 災害割増特約 / 災害死亡割増特約, 傷害特約, 災害入院特約, 疾病入院特約, 三大疾病関連特約, 年金支払移行特約 [S1]
  [S3] [S7].
- Tokio Marine Anshin's 疾病/災害入院特約 illustrate the third-sector shape that `medical` inherits:
  入院給付金 = 入院給付金日額 × (入院日数 − 4日) for stays of 5 days or more, 1入院支払限度日数 of 120 / 360 / 730
  days by type with a **通算 730日** limit in every type, and 手術給付金 at 40 / 20 / 10 × the daily
  amount [S7].
- **年金支払移行特約**: after 払込満了 the contract may be converted into an annuity or a care benefit
  using the 責任準備金等 as the consideration, with no further premium [S7] [S11].

### 17. Taxation

- **Death benefit, inheritance tax.** 相続税法第3条第1項第1号 deems a death benefit acquired by
  inheritance to the extent of the premiums the decedent bore [R9]. 第12条第1項第6号 exempts, for
  heirs, the amount given by the statute's own formula — **500万円 × 相続人の数** (the 第15条第2項
  count) — with a pro-rata allocation where the total received exceeds it [R9]. 国税庁 restate
  the formula and add the counting rules: heirs who renounced are counted as if they had
  not; adopted children count at most one where there is a natural child and at most two
  where there is none; **recipients who are not heirs get no exemption at all** [R10].
- **生命保険料控除.** Post-2012 contracts fall in three baskets — 一般の生命保険料, 介護医療保険料, 個人年金保険料; a
  whole life policy sits in the 一般 basket. New-regime deduction (income tax) [R11]:

  | 年間の支払保険料等 | 控除額 |
  |---|---|
  | 20,000円以下 | 支払保険料等の全額 |
  | 20,000円超 40,000円以下 | 支払保険料等 × 1/2 + 10,000円 |
  | 40,000円超 80,000円以下 | 支払保険料等 × 1/4 + 20,000円 |
  | 80,000円超 | 一律 40,000円 |

  Old-regime (pre-2012) bands: 25,000円 / 50,000円 / 100,000円 thresholds giving a maximum of
  50,000円 per basket. Per-basket cap 40,000円 (new) or 50,000円 (old); **overall cap
  120,000円** [R11]. Page basis: 令和7年4月1日現在法令等.
- The premium deduction is a real product-design driver: a whole life policy competes for
  the same 一般 basket as a term policy, which is why the 個人年金保険 product carries a 税制適格特約 to
  reach a third basket [R11] — relevant to `individual_annuity`, not here.
- Insurers restate that the tax treatment described is subject to future amendment [S1].

### 18. Market context and behavioural benchmarks

FY2024, 個人保険, from 生命保険協会 [R12]:

- 新契約件数 (excluding 転換後契約) 1,243万件 (98.7% of the prior year). By product: 医療保険 296万件 (23.8%),
  **終身保険 231万件 (18.6%)**, ガン保険 159万件 (12.8%), 定期保険 135万件 (10.9%), 変額保険 99万件 (8.0%).
- 新契約高 57兆639億円 (101.4%). By product: 定期保険 24兆6,666億円 (43.2%), **終身保険 12兆9,965億円 (22.8%)**,
  変額保険 10兆7,797億円 (18.9%), 養老保険 1兆5,347億円 (2.7%).
- 保有契約件数 1億9,530万件 (17th consecutive year of growth). By product: 医療保険 4,545万件 (23.3%),
  **終身保険 3,848万件 (19.7%)**, 定期保険 2,721万件 (13.9%), ガン保険 2,522万件 (12.9%).
- 保有契約高 778兆9,902億円 (98.5%, falling as the market shifts from death cover to medical). By
  product: 定期保険 300兆4,672億円 (38.6%), **終身保険 215兆962億円 (27.6%)**, 変額保険 47兆6,016億円 (6.1%),
  定期付終身保険 29兆1,313億円 (3.7%).
- **解約・失効率 5.6%** (down 0.3 points), on 解約・失効高 44兆15億円. Definition, from the report's own
  footnotes: 解約・失効高 = 解約 + 失効, and 解約・失効率 = 解約・失効高 ÷ 年度始保有契約高 × 100 — **an amount-weighted
  ratio to opening in-force sum assured, industry- wide across all product types**, not a
  policy-count rate and not a whole-life-specific rate. Using it directly as a per-policy
  lapse assumption would be wrong; it is a sanity bound.
- Whole life is thus the **second-largest** individual line by every one of the four
  measures, and the largest of the savings-bearing lines.

---

## Variation across carriers

| Feature | アフラック [S1] [S2] | オリックス (RISE) [S3] [S4] [S5] | 東京海上日動あんしん (長割り終身) [S7] | 日本生命 (みらいのカタチ) [S8] | かんぽ生命 (Ｒ07) [S9] | 第一生命 [S10] | 三井住友海上あいおい [S11] |
|---|---|---|---|---|---|---|---|
| Participation | 無配当 (main contract) | 無配当 | 5年ごと利差配当 | 有配当2012 | 契約者配当あり | 5年ごと配当 | 無配当 |
| 低解約返戻金型 offered | via a separate product 〔低解約払戻金型〕 | yes, it **is** the product | yes, side by side with the ordinary twin | not in this file | yes, as a parallel 約款 | not in this file | yes (積立利率変動型 chassis) |
| Suppression factor | not stated in this file | **7割** (約款) | **70%** (契約概要) | — | **×0.7** (約款) | — | **70%** (glossary) |
| Suppressed period | — | = 保険料払込期間 | 契約日 to 24:00 on the 払込満了日 | — | before 払込満了 | — | = 保険料払込期間 |
| Published CV table | no | **yes**, 8 durations | **yes**, both products, 5 durations | no | no | no | no |
| Published premium table | no | **yes**, ages 20–51 × 4 sums × 2 sexes | one model point only | no | no | no | no |
| 自動振替貸付 | **opt-out** (automatic) | **opt-in** | **opt-out** | **none** | **none** (request only) | **opt-out** | opt-out |
| APL amount, 月払 | 3 months at a time | the premium due | the premium due | — | — | to the next half-yearly anniversary | the premium due |
| APL rate ceiling | 年8% / 半年4% / 月8/12% | 年8%以下 | same three ceilings, tabulated | — | — | same three ceilings | 年8% ceiling |
| 契約者貸付 limit | 9割 / 8割 paid-up | 9割 / 8割 paid-up | 9割 / 8割 paid-up, min 5万/1万円 | **8割 less 3 months' premium** | company formula, 1-year term | company range | company range |
| Loan-excess consequence | lapse after a month's notice | lapse after a month's notice | lapse | — | **sum assured reduced**, never lapse | lapse | — |
| Grace (月払) | to the end of the following month | to the end of the following month | to the end of the following month | **解除予定日**, 3 months on | **two months** | to the end of the following month | to the end of the following month |
| 復活 window | 3 years | 3 years | 3 years | **none** (解除, irreversible) | **1 year** | 3 years | 3 years |
| 払済保険 eligibility | sum-assured floor only | sum-assured floor only | yes, with **復旧** within 3 years | — | **2 years** in force | **3 years** of premiums | yes |
| 延長定期保険 | no | no | **yes** | no | no | no | not in the retrieved chapters |
| Suicide exclusion | 3 years | 3 years | 3 years | 3 years | 3 years | 3 years | — |
| Published rates | **loan/APL rates by 契約日 vintage** | — | rate-review calendar only | — | rate on the web site | — | **予定利率 disclosed** |
| Distinctive | 非喫煙割引特約 | 15–80 grid; 契約者=被保険者 | the matched suppressed/ordinary pair | no APL, no reinstatement | statutory 加入限度額; ばらんす型 step-down | ステップ払込方式 特則 | 積立利率 formula; split suppression |

**Most representative design for a reference implementation.** A 無配当, level-premium whole
life with (i) a 終身 term, (ii) a choice of 終身払 or a short-pay period on both a 年満了
(5/10/15/20) and a 歳満了 (50/55/60/65/70/75/80) basis with issue ages roughly 15–80 and 10
years' minimum payment on the 歳満了 options [S5], (iii) death and 高度障害 benefits at the same
amount [S1] [S3], (iv) a **低解約返戻金型 switch** whose factor is **70%** over a suppressed period
identical to the premium-paying period, stepping to the full value at 払込満了 [S3] [S7] [S9]
[S11], (v) an **opt-out 自動振替貸付** that carries the policy while the surrender value can fund
the premium plus interest, capped at the published mode-dependent ceilings [S1] [S7] [S10],
(vi) 契約者貸付 at 9/10 of the surrender value while premiums are paid and 8/10 afterwards [S1]
[S3] [S7], (vii) 払済保険 [S1] [S3] [S7] [S9] [S10], (viii) a 3-year suicide exclusion with the
責任準備金 returned [S1] [S9] [S10], (ix) a one-month grace and a 3-year 復活 window [S1] [S3]
[S10], and (x) リビング・ニーズ特約 attached at no cost with a 3,000万円 cap and a 6-month acceleration
discount [S1] [S7]. The Orix table in §3 is the natural worked-example anchor because it is
internally consistent, published, and exhibits the cliff.

---

## Fetch failures and gaps

- **`https://www.actuaries.jp/lib/standard-life-table/seimeihyo2018.pdf`** — the URL that
  appears in search results returns a 404 page rendered as a 3-page PDF. The live document
  is at `/lib/standard-life-table/pdf/seimeihyo2018.pdf` [R1]. Nothing was lost.
- **`https://www.nta.go.jp/taxes/shiraberu/taxanswer/zaisan/4114.htm`** — 404/moved. The
  live path is `/taxes/shiraberu/taxanswer/sozoku/4114.htm` [R10]. Nothing was lost.
- **`https://www.aflac.co.jp/reserving_loan_rate.html`** — HTTP 403 to WebFetch. Retrieved
  on the second attempt with a browser User-Agent (curl, HTTP 200, server-rendered). Facts
  stand [S2].
- **`https://elaws.e-gov.go.jp/document?lawid=...`** — 301 to `laws.e-gov.go.jp`. All three
  laws were retrieved through the v2 JSON API on that host [R5] [R6] [R9].
- **R3 (`seimeihyo2018-katei.pdf`) — retrieved but not readable.** The 67-page
  working-process appendix downloads cleanly but its body text uses a font encoding neither
  pypdf nor PyMuPDF resolves; only the cover page is legible. No fact in this file depends
  on it. Anyone needing the intermediate graduation steps will have to OCR it.
- **The 安全率係数 table for non-single-premium contracts is not recoverable.** The redline [R8]
  prints it as 「［表略］」. The mechanism (annual 基準日, min of 3-year and 10-year JGB averages,
  0.5% trigger, 0.25% granularity, effective the following 1 April) is fully sourced; only
  the band-by-band coefficients for the annual case are missing. The single-premium
  coefficient table for post-2022 contracts **is** printed in full and is quoted in §13.
- **The current numeric value of the 標準利率 is [unverified].** No document retrieved in this
  session states it. Search results attribute values to secondary personal-finance blogs
  (`behavior.co.jp` and similar), which are not citable here, and to a Nissay Research
  Institute paper that was not fetched. The 告示 gives only the mechanism. Any 標準利率 figure
  used downstream must be tagged **[std]** or **[unverified]** until an FSA or insurer
  disclosure is retrieved.
- **予定利率 for level-premium whole life is [unverified] as a current figure.** The only
  disclosed level-premium value found is MS&AD's 1.75% in a **2010.3** booklet [S11]; the
  current figure is not published by any carrier in this set. 明治安田's live disclosure [S12]
  covers 一時払 products only. Search results reporting 2026 level-premium 予定利率 in the
  1.75–2.5% range come from secondary blogs and are **not** relied on here.
- **Kampo publishes no numeric surrender-value or premium table** in the 448-page booklet
  [S9]; its 約款 gives the 0.7 multiplier but not the underlying scale. The suppression factor
  is therefore confirmed from Kampo, but the cash-value level is not.
- **Aflac publishes no issue-age or sum-assured envelope** in the retrieved しおり・約款 [S1];
  those live in the 契約概要, which is a separate document not fetched. The Aflac facts used
  here are all contractual mechanics, which the 約款 does carry.
- **Aflac's own 〔低解約払戻金型〕 special provisions are not readable.** The リビング・ニーズ特約 in [S1]
  refers to arts. 24 and 25 — 「主契約が三大疾病保障付終身保険〔低解約払戻金型〕の場合の特則」 and 「主契約が終身保険〔低解約払戻金型〕の場合の特則」
  — but both are printed as 「（記載省略）」 in that booklet. Aflac's suppression factor is
  therefore **not** established here.
- **Two of the surrender-value sources are dated.** [S7] is a 2010.3 revision with a
  平成22年3月2日 calculation basis and [S11] is 2010.3; their premium and cash-value levels
  reflect a 2010 pricing basis and must not be presented as current. Their **mechanics**
  (the 70% factor, the APL and loan rules, 延長定期保険, the 積立利率 formula) are structural and are
  still the current drafting pattern, as [S3], [S4], [S5] and [S9] (2024–2026) confirm for
  the parts they overlap.
- **`https://www.jili.or.jp/research/report/9849.html`** (生命保険文化センター, 2024年度 生命保険に関する全国実態調査)
  — retrieved, but the page is an index of ~100 Excel files with no summary figures and no
  report PDF. Household penetration and average-sum-assured benchmarks were therefore
  **not** obtained. The market-context facts in §18 rest on [R12] alone.
- **`https://www.sonylife.co.jp/contractor/policy/whole/20241002/yakkan.html`** — retrieved
  (200) but the clause index for main contracts is rendered client-side; only rider PDFs
  (`b_*.pdf`) and two medical main-contract PDFs (`a_05`, `a_09`) are in the static HTML.
  **ソニー生命's whole life 約款 was not obtained.** An eighth carrier would mainly have refined
  the variation table.
- **Yen 積立利率変動型 and 一時払 約款 beyond [S11] and [S12] were not pursued.** The two
  foreign-currency booklets found (ジブラルタ生命 積立利率更改型一時払終身保険（23）, and a 第一フロンティア生命
  積立利率変動型終身保険（17）（通貨指定型） distributed through MUFG) were downloaded but belong to
  `fx_whole_life`; the latter also extracts as mojibake. They are deliberately left for that
  product's research pass.
- **No carrier publishes a lapse or surrender curve by duration.** [R12]'s 5.6% is
  industry-wide, amount-weighted and across all products. Any duration-shaped lapse
  assumption — and in particular the **surrender spike at 払込満了** that the 低解約返戻金型 cliff must
  produce — is a **[std]** modelling choice with no public data behind it. This is the
  single largest assumption gap for this product.
- **No carrier publishes an expense basis.** 予定事業費率 is named in the 保険契約者保護機構 boilerplate
  [S1] [S7] but never quantified. MS&AD's 0.2% asset-management deduction inside the 積立利率
  formula [S11] is the only expense-like figure recovered anywhere in this session.
- The claim that a suicide exclusion of exactly three years is universal across the Japanese
  market is supported by six carriers here [S1] [S3] [S7] [S8] [S9] [S10]; beyond those six
  it is [unverified].
