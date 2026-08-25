# Regulatory and Actuarial References — Japan Life Insurance

**Status:** Draft, 2026-08-20.

Curated reference library for the Japan section of the reference-product library. It covers
the prudential and supervisory (金融庁 / 保険業法 / 施行規則 / 告示 / 監督指針), actuarial
(日本アクチュアリー会), public-statistics, legislation-and-conduct, and tax-and-accounting
sources that the reference cash-flow-model implementations (term_life / income_guarantee /
whole_life / endowment / medical / cancer / nursing_care / individual_annuity /
fx_whole_life) rely on. Product folders cite entries on this page as **[REG-R#]** (e.g.
`[REG-R1]`); the R1–R47 numbering below is **frozen** — never renumber an entry and never
reuse a number, because product documentation cites against it. Within this page, plain
`[R#]` refers to the same entries. Facts stated under an entry that was actually retrieved
were read from the fetched document; a claim taken from general knowledge, from a
search-result summary, or from a document that could not be fetched is tagged
**[unverified]** and is a to-verify item, not an established fact. Every failed fetch is
disclosed in the entry that needed it and again in §6. No URL on this page is fabricated.
All URLs accessed **2026-08-20**.

**Regulatory architecture in one line:** the 金融庁 (*Kin'yū-chō*, Financial Services Agency,
FSA) supervises insurers under the 保険業法 (*Hoken-gyō-hō*, Insurance Business Act, Act No.
105 of 1995), its 施行規則 (*shikō kisoku*, enforcement regulation) and its 告示 (*kokuji*,
notifications), with supervisory expectations set out in the 監督指針 (*kantoku shishin*,
supervisory guideline); the 保険法 (*Hoken-hō*, Insurance Act, Act No. 56 of 2008) governs the
insurance *contract* between insurer and policyholder; the 日本アクチュアリー会 (Institute of
Actuaries of Japan, IAJ) is the 指定法人 (*shitei hōjin*, designated body) that builds the
standard mortality tables the FSA notification requires; and from **31 March 2026** the
prudential regime is the economic-value 経済価値ベースのソルベンシー規制 (*keizai-kachi bēsu no
soruvenshī kisei*, economic-value-based solvency regulation, **ESR**) [R15], which took over
from the 200%-threshold ソルベンシー・マージン比率 (*soruvenshī mājin hiritsu*, solvency margin
ratio, **SMR**) as the early-corrective-action trigger [R17].

**Scope note on capital:** this library projects **gross best-estimate liability cash
flows**. 標準責任準備金 (*hyōjun sekinin junbikin*, standard policy reserve) [R10], 危険準備金
(*kiken junbikin*, contingency reserve) [R8], 価格変動準備金 (*kakaku hendō junbikin*, price
fluctuation reserve) [R3], and the ESR 所要資本 (*shoyō shihon*, required capital) and MOCE
[R15] are **cited, not specified** — the entries below tell a drafter exactly what the
regime requires without the library implementing any of it, the same way `uklib` treats the
SCR. What `jplib` *does* implement is the shape the Japanese regime asks a liability model
for: the 1号収支分析 (*ichi-gō shūshi bunseki*, item-1 income-and-outgo analysis) of [R22] is a
per-segment projection of premiums, claims, expenses and surrenders over at least ten future
years, and that is what these models produce.

---

## Product-relevance matrix

`x` = load-bearing (a product's documents cite the entry for a specific parameter,
definition or constraint); `(x)` = qualified or background relevance (context, framing, or a
mechanic the product names but does not model); blank = not indicated. Column key: TL =
term_life, IG = income_guarantee, WL = whole_life, END = endowment, MED = medical, CAN =
cancer, LTC = nursing_care, IA = individual_annuity, FX = fx_whole_life.

| R# | Reference (short name) | TL | IG | WL | END | MED | CAN | LTC | IA | FX |
|----|------------------------|----|----|----|-----|-----|-----|-----|----|----|
| R1 | 保険業法 第3条 — sector split | x | x | x | x | x | x | x | x | x |
| R2 | 保険業法 第4条 — 基礎書類 | x | x | x | x | x | x | x | x | x |
| R3 | 保険業法 第115条 — 価格変動準備金 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R4 | 保険業法 第116条 — 責任準備金 | x | x | x | x | x | x | x | x | x |
| R5 | 保険業法 第120条 — 保険計理人の選任 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R6 | 保険業法 第121条 — 職務と意見書 | x | x | x | x | x | x | x | x | x |
| R7 | 施行規則 第68条 — 標準責任準備金対象契約 | x | x | x | x | x | x | x | x | x |
| R8 | 施行規則 第69条 — 責任準備金の区分 | x | x | x | x | x | x | x | x | x |
| R9 | 施行規則 第30条の2 — 剰余金の分配 | (x) | (x) | x | x | (x) | (x) | (x) | x | (x) |
| R10 | 平成8年大蔵省告示第48号 — 標準責任準備金 | x | x | x | x | x | x | x | x | x |
| R11 | 告示48号改正 — 標準生命表2018 の採用 | x | x | x | x | x | x | x | x | x |
| R12 | 告示改正 — 外貨建契約の標準責任準備金 | | | (x) | (x) | | | | (x) | x |
| R13 | 大蔵省告示第231号 — 第三分野ストレステスト | | | | | x | x | x | | |
| R14 | 保険会社向けの総合的な監督指針（本編） | x | x | x | x | x | x | x | x | x |
| R15 | 経済価値ベースのソルベンシー規制の概要 (ESR) | x | x | x | x | x | x | x | x | x |
| R16 | ESR 政策ページ — 告示の索引 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R17 | ソルベンシー・マージン比率と 200% 閾値 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R18 | 標準生命表2018 — the table PDF | x | x | x | x | x | x | x | x | x |
| R19 | 標準生命表 1996/2007/2018 — Excel | x | x | x | x | x | x | x | x | x |
| R20 | 標準生命表2018 の作成概要 | x | x | x | x | x | x | x | x | x |
| R21 | 日本アクチュアリー会 索引と利用規約 | x | x | x | x | x | x | x | x | x |
| R22 | 保険計理人の実務基準 — 1号収支分析 | x | x | x | x | x | x | x | x | x |
| R23 | 監督指針 VI — 指定法人としての IAJ | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R24 | 第23回生命表（完全生命表, 令和2年） | x | x | x | x | (x) | (x) | (x) | x | x |
| R25 | 令和6年簡易生命表 | x | x | x | x | (x) | (x) | (x) | x | x |
| R26 | 患者調査 — 受療率 | | | | | x | x | (x) | | |
| R27 | 患者調査 — 退院患者の平均在院日数 | | | | | x | x | (x) | | |
| R28 | がん統計 — 最新がん統計 | (x) | | (x) | | x | x | | | |
| R29 | がん統計 — データダウンロード | | | | | (x) | x | | | |
| R30 | 介護保険事業状況報告（年報） | | | (x) | | (x) | | x | | |
| R31 | 生命保険の動向 2025年版 | x | x | x | x | x | x | x | x | x |
| R32 | 生命保険に関する全国実態調査 2024年度 | x | x | x | x | x | x | x | x | x |
| R33 | e-Stat 政府統計の総合窓口 | (x) | (x) | (x) | (x) | x | x | x | (x) | (x) |
| R34 | 保険法 第51条 — 保険者の免責 | x | x | x | x | (x) | (x) | (x) | (x) | x |
| R35 | 保険法 第55条 — 告知義務違反による解除 | x | x | x | x | x | x | x | (x) | x |
| R36 | 保険業法 第309条 — クーリング・オフ | x | x | x | x | x | x | x | x | x |
| R37 | 保険業法 第300条の2 — 特定保険契約 | | | (x) | (x) | | | | x | x |
| R38 | 消費者契約法 第4条 — 取消事由 | (x) | (x) | x | x | (x) | (x) | (x) | x | x |
| R39 | 金融サービス提供法 第4条 — 説明義務 | (x) | (x) | x | x | (x) | (x) | (x) | x | x |
| R40 | 生命保険契約者保護機構 — 90% 補償 | x | x | x | x | x | x | x | x | x |
| R41 | 保険業法 第270条の3 — 補償率の委任 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R42 | 介護保険法 第7条 — 要介護状態 | | | (x) | | (x) | | x | | |
| R43 | 所得税法 第76条 — 生命保険料控除 | x | x | x | x | x | x | x | x | x |
| R44 | 相続税法 第12条 — 死亡保険金の非課税限度額 | x | x | x | x | | | | (x) | x |
| R45 | タックスアンサー No.4114 — 相続税 | x | x | x | x | | | | (x) | x |
| R46 | タックスアンサー No.1755 — 満期保険金等 | (x) | (x) | x | x | | | | x | x |
| R47 | IFRS 17 の日本での位置づけ | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |

---

## 1. Prudential and supervisory — 保険業法, 施行規則, 告示 and the 監督指針

(jplib-reg-r1)=

### R1 — e-Gov 法令検索, 保険業法 第3条（免許の種類と分野区分）

- **Publisher:** e-Gov 法令検索 (デジタル庁) — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=3
- **Accessed:** 2026-08-20
- **Retrieved:** yes — through the e-Gov **article REST endpoint**, which returns
  machine-readable XML. The ordinary `laws.e-gov.go.jp` page is a JavaScript single-page
  app that serves an empty shell to plain fetchers; every statute entry on this page was
  retrieved through the article endpoint, with the 法令番号 in kanji numerals,
  percent-encoded.
- **Annotation:** 第3条第4項 lists the business a 生命保険業免許 (life insurance licence) covers:
  第1号, fixed-sum insurance on human survival or death — the **第一分野** (*dai-ichi bun'ya*,
  first sector); 第2号, insurance paying a fixed sum or indemnifying loss on listed events
  (sickness, injury, states requiring nursing care) — the **第三分野** (*dai-san bun'ya*, third
  sector); 第3号, reinsurance of both. 第3条第5項 defines the 損害保険業免許 (第二分野, non-life) as
  indemnity insurance against loss from a fortuitous event **plus** "前項第二号に掲げる保険" — so
  the third sector sits inside *both* licences, which is precisely why Japanese regulation
  names it separately [R1]. Modelling consequence: term_life, income_guarantee, whole_life,
  endowment, individual_annuity and fx_whole_life are 第一分野; medical, cancer and
  nursing_care are 第三分野. The split is not cosmetic — the reserving rules [R8] [R13] [R14]
  and the standard mortality table that must be used [R10] [R18] differ by 分野.

(jplib-reg-r2)=

### R2 — e-Gov 法令検索, 保険業法 第4条（免許申請と基礎書類）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=4
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** 第4条第2項 requires a licence application to attach four documents: 一 定款
  (articles of incorporation); 二 **事業方法書** (*jigyō hōhō-sho*, statement of business
  method); 三 **普通保険約款** (*futsū hoken yakkan*, ordinary policy conditions); 四
  **保険料及び責任準備金の算出方法書** (*sanshutsu hōhō-sho*, statement of the method of calculating
  premiums and policy reserves). 第4項 delegates their required contents to Cabinet Order
  [R2]. This is what a Japanese product filing consists of, and it fixes what is and is not
  public for a reference implementation: the 算出方法書 is where the 予定利率 (*yotei riritsu*,
  assumed interest rate), 予定死亡率 (assumed mortality), 予定事業費率 (assumed expense loadings) and
  the surrender-value formula actually live, and it is **not published**. That is why every
  pricing-basis parameter in `jplib` is **[std]** while contractual parameters are sourced
  from the public 約款 and パンフレット with `[S#]` tags. The composite term **基礎書類** (*kiso
  shorui*) is not defined in 第4条 itself — it is used in later articles, notably 第123条
  (変更), to mean 定款 plus the three documents above [unverified — 第123条 not retrieved].

(jplib-reg-r3)=

### R3 — e-Gov 法令検索, 保険業法 第115条（価格変動準備金）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=115
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** 第1項 requires an insurer to accumulate, as 価格変動準備金, an amount calculated
  under Cabinet Office Ordinance in respect of 株式等 — shares and other assets exposed to
  price movement. 第2項 permits a drawdown only to the extent that losses on 株式等 exceed
  gains on them, larger drawdowns needing the FSA Commissioner's approval. **The statute
  carries no percentage**: the rates sit in 施行規則第65条・第66条 [R3]. Modelling consequence: this
  is a balance-sheet reserve driven by *assets*, not by liability cash flows, so it is cited
  and never modelled here. It matters to fx_whole_life because 施行規則第66条第2項 allows the
  reserve to be computed on the asset segment matching 外貨建て保険 (foreign-currency
  contracts) — see [R14].

(jplib-reg-r4)=

### R4 — e-Gov 法令検索, 保険業法 第116条（責任準備金と標準責任準備金の委任）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=116
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** 第1項 requires an insurer to accumulate 責任準備金 (*sekinin junbikin*, policy
  reserve) at each 決算期 (accounting period end) to prepare for the discharge of future
  obligations under insurance contracts. **第2項** is the operative delegation: for long-term
  contracts specified by Cabinet Office Ordinance, the Prime Minister may prescribe the
  **accumulation method** and the **level of the coefficients** (assumed mortality rate and
  others) forming the basis of the calculation. 第3項 delegates the remainder, including
  reserves for reinsurance ceded [R4]. This paragraph is the hook on which the entire
  標準責任準備金 regime hangs: 施行規則第68条 [R7] says *which* contracts are in scope, and
  平成8年大蔵省告示第48号 [R10] says *the method and the rates*. Every `jplib` document that
  mentions statutory reserving cites this chain rather than stating a formula of its own.

(jplib-reg-r5)=

### R5 — e-Gov 法令検索, 保険業法 第120条（保険計理人の選任等）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=120
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** 第1項 requires an insurance company — every life insurer, and non-life
  insurers meeting the Cabinet Office Ordinance conditions — to appoint a **保険計理人**
  (*hoken keirinin*, appointed actuary) by board resolution and to involve that person in
  the actuarial matters the ordinance specifies, **including the method of calculating
  premiums**. 第2項 requires the appointee to have the knowledge and experience the role needs
  and to meet the ordinance's qualification requirements; 第3項 requires appointment and loss
  of office to be notified to the Prime Minister [R5]. Background rather than a cash flow
  driver: it names the office that professionally owns any basis a model uses, and it is the
  statutory anchor of the practice standard at [R22].

(jplib-reg-r6)=

### R6 — e-Gov 法令検索, 保険業法 第121条（保険計理人の職務と意見書）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=121
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API; full Japanese text returned)
- **Annotation:** 第1項 requires the 保険計理人, at each 決算期, to confirm the listed matters in
  the manner Cabinet Office Ordinance prescribes and to submit an **意見書** (*ikensho*,
  written opinion) recording the result to the board. The listed items are **第1号** whether
  the 責任準備金 for the contracts the ordinance specifies "が健全な保険数理に基づいて積み立てられているかどうか"
  — whether it is accumulated on sound actuarial principles; **第2号** whether 契約者配当
  (*keiyakusha haitō*, policyholder dividends) or the distribution of surplus to members
  "が公正かつ衡平に行われているかどうか" — is done fairly and equitably; **第3号** other matters set by
  ordinance. 第2項 sends a copy of the 意見書 to the Prime Minister without delay; 第3項 lets the
  Prime Minister demand an explanation of it [R6]. **This is the load-bearing entry for what
  `jplib` projects.** 第121条第1項第1号 is the statutory demand that the IAJ practice standard
  [R22] turns into the **1号収支分析** — a projected income-and-outgo test over at least ten
  future years. That test is the clearest regulatory *use* of a liability cash flow model in
  Japan, and it is the shape these projections take.

(jplib-reg-r7)=

### R7 — e-Gov 法令検索, 保険業法施行規則 第68条（標準責任準備金対象契約の範囲）

- **Publisher:** e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- **Doc type:** ministerial ordinance (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E5%85%AB%E5%B9%B4%E5%A4%A7%E8%94%B5%E7%9C%81%E4%BB%A4%E7%AC%AC%E4%BA%94%E5%8F%B7;article=68
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** Life insurance contracts concluded on or after the commencement date are
  standard-reserve contracts **except**: (1) contracts whose reserve varies with the value
  of assets held in a 特別勘定 (*tokubetsu kanjō*, separate account); (2) contracts with no
  policy-reserve accumulation provision; (3) "保険約款において、保険会社が責任準備金及び保険料の
  計算の基礎となる係数を変更できる旨を約してある保険契約" — contracts whose 約款 lets the insurer change the
  calculation coefficients; (4) other contracts the FSA judges unsuitable. 第2項 and 第3項
  carry tighter criteria for contracts concluded after dates the FSA specifies, including
  rate-guarantee provisions and unit-linked contracts without a guarantee [R7]. Modelling
  consequence: exclusion (3) is the escape hatch a 予定利率変動型 or reviewable-coefficient
  product uses, and exclusion (1) is why a variable annuity's separate account sits outside
  the standard reserve while its **minimum guarantee** sits inside it ([R10] 第14項).
  Decisive when individual_annuity documents split fixed from variable business, and when
  fx_whole_life explains why its 積立利率変動 design is nonetheless in scope [R12].

(jplib-reg-r8)=

### R8 — e-Gov 法令検索, 保険業法施行規則 第69条（責任準備金の区分）

- **Publisher:** e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- **Doc type:** ministerial ordinance (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E5%85%AB%E5%B9%B4%E5%A4%A7%E8%94%B5%E7%9C%81%E4%BB%A4%E7%AC%AC%E4%BA%94%E5%8F%B7;article=69
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API; article returned, item structure read)
- **Annotation:** 第1項 divides a life insurer's 責任準備金 into **第1号 保険料積立金** (*hokenryō
  tsumitatekin*, the policy reserve proper — "保険数理に基づき計算した金額"), **第2号 未経過保険料**
  (*mikeika hokenryō*, unearned premium, the part matching the unexpired period), **第2号の2
  払戻積立金** (*haramodoshi tsumitatekin*, refund reserve, for contracts promising a premium
  refund) and **第3号 危険準備金** (contingency reserve, "将来発生が見込まれる危険に備えて計算した金額"). Later
  paragraphs cover contracts with unpaid premiums, accumulation-method requirements, 特別勘定
  treatment, the subdivision of 危険準備金 (insurance risk, assumed-interest-rate risk,
  minimum-guarantee risk) and the requirement to follow standards set by the FSA
  Commissioner [R8]. `jplib` projects gross cash flows and builds **none** of these four; a
  product document that touches reserving cites this article for the taxonomy. The 危険準備金
  subdivision — Ⅰ insurance risk / Ⅱ assumed-interest risk / Ⅲ minimum-guarantee risk / Ⅳ
  third sector — is the vocabulary the 監督指針 uses [R14], and Ⅳ is what [R13] stress-tests.

(jplib-reg-r9)=

### R9 — e-Gov 法令検索, 保険業法施行規則 第30条の2（剰余金の分配の基準）

- **Publisher:** e-Gov 法令検索 — 保険業法施行規則, 平成八年大蔵省令第五号
- **Doc type:** ministerial ordinance (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E5%85%AB%E5%B9%B4%E5%A4%A7%E8%94%B5%E7%9C%81%E4%BB%A4%E7%AC%AC%E4%BA%94%E5%8F%B7;article=30_2
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** Where a 相互会社 (mutual company) distributes surplus to its members, it must
  compute the distributable amount **for each category set according to the characteristics
  of the contracts** ("保険契約の特性に応じて設定した区分ごとに"), by one of four permitted methods: (1)
  by premiums paid and the return earned on them, less claims and expenses; **(2)
  剰余金の生じた原因に応じて** — by the *cause* of the surplus, computed per contract on the policy
  reserve or the sum insured; (3) by the insurance period, per contract on the reserve or
  the premiums; (4) an equivalent method [R9]. **Honest limit, and it is the one a drafter
  will be tempted to skip.** Method (2) is the statutory form of the **三利源** (*san-rigen*,
  three sources of surplus) dividend, but this article **does not name 死差 / 利差 / 費差**
  (mortality, interest and expense margins) and neither does the 監督指針: a full-text search
  of the 500-page 本編 [R14] returns zero hits for 利源, 三利源, 死差 and 費差. The 三利源 framing is
  Japanese actuarial and industry practice, not regulatory language [unverified as
  regulatory language; verified as absent from R9 and R14]. `jplib` may use the vocabulary
  and must not attribute it to a regulatory text. Dividend mechanics belong in assumption
  class (b), insurer-discretionary current elements, on 有配当 and 5年ごと利差配当 designs.

(jplib-reg-r10)=

### R10 — 金融庁（旧 大蔵省）, 平成8年大蔵省告示第48号「標準責任準備金の積立方式及び計算基礎率を定める件」

- **Publisher:** 大蔵省 → 金融庁 (notification). The consolidated text used here came from an
  **unofficial third-party mirror** that tracks amendments, captioned "2026年6月15日施行分".
- **Doc type:** 告示 (FSA notification), consolidated text
- **URL (mirror):** http://www.nn.em-net.ne.jp/~s-iwk/current/H08-048/index.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes, **but from an unofficial mirror** — `https://` fails with a self-signed
  certificate and aborts plain fetchers; retrieved over plain HTTP with `curl -k` and a
  browser User-Agent, then decoded from EUC-JP. **The FSA's own consolidated text of this
  告示 was not located in this session.** Treat the paragraph numbering as read and the
  *legal* text as one remove from official. The mirror's amendment list runs
  平成10年金融監督庁・大蔵省告示第52号, 平成12年総理府・大蔵省告示第1号, 平成12年総理府告示第40号, 平成12年金融庁告示第63号,
  平成13年金融庁告示第21号, 平成16年金融庁告示第55号, 平成18年金融庁告示第127号, 平成26年金融庁告示第38号,
  平成28年金融庁告示第30号, 平成29年金融庁告示第31号, 令和3年金融庁告示第39号 and, most recently,
  **令和7年9月5日 金融庁告示第90号**.
- **Annotation:** The most parameter-dense document in this library, and the one a
  reserving pointer in any `jplib` product document lands on.
  - **第1項第1号 積立方式:** "積立方式は、平準純保険料式とする。" — the **平準純保険料式** (*heijun
    jun-hokenryō-shiki*, net level premium method). No Zillmer adjustment.
  - **第1項第2号 予定死亡率:** the rates are those produced by the body designated under 法第122条の2
    第1項 (the IAJ, [R23]) and verified by the FSA Commissioner. イ contracts to 2007-03-31 →
    生保標準生命表1996 (死亡保険用 / 年金開始後用); ロ 2007-04-01 to 2018-03-31 → 生保標準生命表2007 or
    第三分野標準生命表2007; **ハ contracts from 2018-04-01 → 生保標準生命表2018（死亡保険用）,
    生保標準生命表2007（年金開始後用）, or 第三分野標準生命表2018.** Note the asymmetry: the
    **annuity-in-payment table was not updated in 2018** — the 2007 年金開始後用 table remains in
    force, which is why individual_annuity's payout phase reads a different table from its
    accumulation phase [R11] [R19].
  - **第1項第3号 予定利率 (標準利率) base:** イ contracts to 1999-03-31 → **2.75%**; ロ from
    1999-04-01 → **2%**. Every later value is produced by the reset mechanics below rather
    than stated in the text.
  - **第3項:** where the computed 保険料積立金 or 払戻積立金 falls below the 契約者価額, the 契約者価額 is used
    instead. The paragraph's segment-matching conditions reference **マーケット・バリュー・アジャストメント**
    (MVA) and 解約控除額 explicitly, with interest-sensitivity ratio tests — whole-curve ratio
    0.9–1.1, relaxed to 0.8–1.25 for a newly created segment for ten fiscal years, and
    5-year-bucket ratios 0.8–1.25.
  - **第4項 annual reset (regular-premium, JPY):** 基準日 = **1 October** each year. The 対象利率 is
    the lower of the mean 応募者利回り on 10-year JGBs issued over the past 3 years and over the
    past 10 years, measured to the month before the 基準日. Safety coefficients apply in bands
    — **0.9** on the part 0–1.0%, **0.75** on 1.0–2.0%, **0.5** on 2.0–6.0%, **0.25** above
    6.0% — and the sum is the 基準利率. If the 基準利率 differs from the 予定利率 then in force by
    **0.5% or more**, the new 予定利率 is the nearest **0.25% multiple** (rounded *down* on an
    exact 0.125% tie) and applies to contracts concluded **from 1 April of the following
    year**.
  - **第5項 quarterly reset (single-premium, JPY, from 2015-04-01):** 基準日 = **1 January, 1
    April, 1 July and 1 October**; the trigger is **0.25%**; the new rate applies to
    contracts concluded **from three months after the 基準日**. 第1号保険契約 (single-premium death
    or third-sector cover to death) uses the mean of the 10-year and 20-year JGB 流通利回り over
    3 months versus the same mean over 1 year, lower of the two; 第2号保険契約 (single-premium
    endowment and annuity shapes) uses the 10-year 流通利回り alone. Safety bands here: **1.0**
    on the part at or below 0%, 0.9 on 0–1.0%, 0.75 on 1.0–2.0%, 0.5 on 2.0–4.0%, 0.25 above
    4.0%.
  - **第7項** restates the annual reset for JPY contracts other than 第1号/第2号保険契約 on the 第5項
    safety bands, trigger 0.5%, effective the following 1 April.
  - **第8項・第9項 (from 2022-04-01)** replace the single-premium bands with a *less
    conservative* ladder: 1.0 at or below 0%, **0.95** on 0–1.0%, **0.9** on 1.0–2.0%,
    **0.85** on 2.0–3.0%, **0.8** on 3.0–4.0%, **0.75** above 4.0%.
  - **第10項・第11項 FX single-premium (USD and AUD):** 米国通貨建保険契約 and 豪州通貨建保険契約 reset
    **monthly** — 基準日 = the 1st of every month — off **A-rated corporate bond yields in the
    contract currency** (10-year, and the 10y/20y mean for 第1号保険契約), with a **0.05%
    trigger** and rounding to the nearest **0.05%**, effective one month after the 基準日. The
    safety bands differ between the two currencies (on the 2.0–3.0% part, 0.9 for USD and
    0.95 for AUD).
  - **第12項 FX regular-premium:** 3-year and 10-year means of the currency's A-rated 10-year
    corporate bond yield, lower of the two; bands 1.0 / 0.9 / 0.75 / 0.5; trigger 0.5%;
    effective the following 1 April.
  - **第13項:** for a 予定利率変動型保険契約 the rate is re-set on the day after each 利率保証期間 ends,
    treating that day as the contract date — the provision fx_whole_life's 積立利率変動 design
    sits on.
  - **第14項 minimum guarantees on separate-account contracts:** the 標準的方式 reserve is
    `PV(guaranteed outgo) - PV(net premiums for the guarantee)`; mortality per 第1項第2号; the
    discount rate is the 標準利率 for the relevant vintage and currency; and where the 標準的方式 is
    used, the expected return equals the discount rate and the **volatilities are fixed by
    the notification**: 国内株式 **18.4%**, 邦貨建債券 **3.5%**, 外国株式 **18.1%**, 外貨建債券 **12.1%**.
    The separate-account reserve is the balance of income and outgo in that account.
  - **What it does not give.** The 告示 states the *mechanism*, not the current numeric
    standard rate. **The 標準利率 in force at the access date could not be established from a
    retrieved official document** — see §6. Any product document stating a current 標準利率 or a
    market 予定利率 must tag it [unverified], or derive it from JGB yields under the machinery
    above and label the derivation **[std]**.

(jplib-reg-r11)=

### R11 — 金融庁, 告示第48号の一部改正（標準生命表2018 の採用, 2017-06-08 公表）

- **Publisher:** 金融庁
- **Doc type:** 告示改正の公表 (notification-amendment announcement)
- **URL:** https://www.fsa.go.jp/news/29/hoken/20170608.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes
- **Annotation:** The announcement that adopted the current valuation tables, verbatim in
  the operative part: "平成３０年４月１日以降締結する保険契約について、生保標準生命表２０１８（死亡保険用）
  及び第三分野標準生命表２０１８を新たに標準責任準備金の計算基礎とします", and "年金開始後契約に適用する標準生命表については、
  生保標準生命表２００７（年金開始後用）を引き続き用いることとします" [R11]. Background given on the page: the IAJ
  submitted the revised tables on 11 May 2017, reflecting improvement in insurers' and the
  national population's mortality experience. **A trap worth recording:** a machine
  summariser rendered 平成30年4月1日 as "April 2030" during the research pass. 平成30年4月1日 = **1
  April 2018**. Product relevance is universal (table vintage), and specific for
  individual_annuity, whose in-payment basis stays on the 2007 年金開始後用 table [R19].

(jplib-reg-r12)=

### R12 — 金融庁,「標準責任準備金制度にかかる告示の一部改正（案）」等の公表（2021-04-23）

- **Publisher:** 金融庁
- **Doc type:** 告示改正案の公表 / public-consultation announcement
- **URL:** https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes (landing page; the 別紙1–3 PDFs were **not** opened)
- **Annotation:** The extension of the 標準責任準備金 regime to **foreign-currency-denominated
  contracts** — expressly USD- and AUD-denominated — reasoned on the growth of the in-force
  block. The amendment to 平成13年金融庁告示第24号 takes effect **1 April 2022**; the other
  amendments **1 October 2021**. The announcement states that the amendments "define the
  calculation method" for the standard interest rate applying to the new foreign-currency
  contracts; the method itself is [R10] 第10項–第12項 [R12]. This is the provenance of the FX
  standard-reserve regime that fx_whole_life sits inside: **before it, FX business was
  outside 標準責任準備金 altogether**, which is why the product's reserving pointer has a date on
  it. The 別紙 PDFs carrying the drafting detail are [unverified] here.

(jplib-reg-r13)=

### R13 — 大蔵省, 平成10年6月8日大蔵省告示第231号（第三分野保険のストレステストによる危険準備金の算出）

- **Publisher:** 大蔵省 → 金融庁 (notification)
- **Doc type:** 告示
- **URL:** not located. The notification is cited by number in the 監督指針 II-2-1-2(6) [R14].
- **Accessed:** 2026-08-20
- **Retrieved:** **no** — no copy of the notification's own text was found on fsa.go.jp or
  on a consolidated mirror in this session. Everything below comes from [R14], which quotes
  its role but not its formulae.
- **Annotation:** Where a third-sector contingency reserve (危険準備金Ⅳ) is computed using a
  **ストレステスト** (stress test), the calculation must be performed "平成 10 年 6 月 8 日大蔵省告示第
  231 号の規定に基づき", and the calculating unit must be organisationally separated from internal
  audit with documented mutual checks [R14]. **The incidence-rate stress magnitudes and the
  confidence level live in the 告示 itself and are [unverified] here.** For medical, cancer
  and nursing_care this is the named reason a third-sector liability model must be able to
  re-run its incidence basis under a shock, per contract grouping — but `jplib` implements
  the sensitivity, not the statutory stress, and must say so rather than implying it has
  reproduced the notification.

(jplib-reg-r14)=

### R14 — 金融庁,「保険会社向けの総合的な監督指針（本編）」令和8年8月版

- **Publisher:** 金融庁
- **Document:** 保険会社向けの総合的な監督指針（本編）, 500 pp.
- **Doc type:** supervisory guideline
- **URL:** https://www.fsa.go.jp/common/law/guide/ins.pdf — HTML section views under
  https://www.fsa.go.jp/common/law/guide/ins/ (`02b.html` = II-2 財務の健全性, `02d.html` = II-4
  業務の適切性)
- **Accessed:** 2026-08-20
- **Retrieved:** yes — the full 500-page PDF downloaded with a browser User-Agent, text
  extracted and searched; the II-2 HTML view fetched separately. (fsa.go.jp returns PDFs to
  plain fetchers as an undecoded binary stream; `curl` with a browser User-Agent and a local
  extraction is the working route.)
- **Annotation:** The document that turns Japanese product mechanics from folklore into
  regulator-recognised features. By the parts a liability model is held to:
  - **II-2-1-2 積立方式.** For 第一分野 and 第三分野 contracts, standard-reserve contracts must carry
    標準責任準備金 and non-standard-reserve contracts must carry a **平準純保険料式** reserve. (2)
    permits **チルメル式** (Zillmer) only where special circumstances exist and the チルメル歩合 is
    justified against the actual first-year expense level; (3) then requires a planned
    build-up back to the standard or net-level basis.
  - **II-2-1-2(4) automatic renewal under premium waiver.** For contracts on premium waiver
    (specified disease, disability, a defined 要介護状態) that are **automatically renewable**,
    the reserve must be computed **as though every automatic renewal to the final expiry
    occurs** — a real modelling instruction for the waiver riders on medical, cancer and
    nursing_care.
  - **II-2-1-2(5)–(7) 第三分野.** 危険準備金Ⅰ and Ⅳ accumulation standards and limits must be set
    to the risk of 手術給付 and 介護給付 and other benefits. The **ストレステスト** and **負債十分性テスト**
    must (a) properly reflect the uncertainty of deterioration in incidence rates; (b) in
    principle be run **per contract grouping sharing the same 基礎率**, groupable only where
    the benefit content is equivalent in trigger and risk characteristics *and* the
    statistical source used for the 予定発生率 is the same; (c) where insured lives are few,
    permit supplementing with the data underlying the 予定発生率; and (d) use the same contract
    groupings for both tests.
  - **II-2-1-3 minimum guarantees.** Under the 標準的方式 the amount must correspond to
    "概ね 50％の事象をカバーできる水準" — roughly the 50th percentile — for normally foreseeable risk;
    the mortality used is the **死亡保険用** standard table where the guarantee is a minimum
    death benefit and the **年金開始後用** table where it is a minimum annuity fund or minimum
    annuity amount.
  - **II-4-2-2(2)③イ.(ア) 契約締結前交付書面.** The 契約概要 must carry 商品の仕組み, 保障の内容 (with the main
    支払事由 and 免責事由), 付加できる主な特約, 保険期間, 引受条件（保険金額等）, 保険料, 保険料払込みに関する事項, 配当金に関する事項 and
    **解約返戻金等の水準**; the 注意喚起情報 must carry クーリング・オフ, 告知義務, 責任開始期, the main non-payment
    cases and **保険料の払込猶予期間、契約の失効、復活**. For 外貨建て保険 it adds the risk that the yen-converted
    benefit falls below the yen-converted amount at inception, and the currency-specific
    charges. For an **MVA product** it adds an explanation that the surrender value reflects
    the market-rate-driven price movement of the backing assets, that a surrender within a
    period may produce a loss, the effect of any coefficient covering rate moves between the
    calculation-basis date and the surrender date, the transaction cost of liquidating
    assets, and the ongoing charges. The guideline defines MVA in terms a model can
    implement: 解約返戻金 is the 保険料積立金 adjusted for the fair-value movement of the backing
    assets caused by the interest-rate difference between inception and surrender.
  - **III-2-17 ソルベンシー・マージン比率の計算** now contains III-2-17-2 経済価値ベースのバランスシートの外部監査 and
    III-2-17-7 保険負債の計算に用いるイールド・カーブ — the ESR regime [R15] is embedded in the guideline
    as well as in the 告示.
  - **IV 保険商品審査上の留意点等 (pp. 410–436).** The review criteria are 法第5条第1項第3号・第4号 and
    規則第11条・第12条. IV-1-2 requires that "適正な死亡率や発生率が組み込まれている" and that benefits not be so
    large relative to the trigger as to be 射倖的. IV-1-4(3) addresses 無選択型商品 (no-underwriting
    products) and anti-selection. IV-1-7 requires that the 告知義務違反 rescission window not be
    unduly long — the supervisory counterpart to [R35]. IV-1-8 covers 保険金額・保険期間・契約年齢範囲.
    **IV-1-9** names, as products needing extra explanation, **低解約返戻金型商品、無選択型商品、
    MVA を利用した商品**. IV-1-10 requires 解約返戻金 to be disclosed clearly, "例えば、金額を保険証券等に
    表示する、計算方法等を約款等に掲載する". **IV-1-12** requires a **契約者貸付** (*keiyakusha kashitsuke*,
    policy loan) limit to be reasonable against the surrender value with over-loan
    prevention, and requires a **保険料の自動振替貸付** (*jidō furikae kashitsuke*, automatic premium
    loan) to be **at the policyholder's election**, with prompt notice when it is exercised.
    IV-1-14 covers 特別勘定 and 積立勘定 products. IV-1-18 handles alignment with 保険法, including
    the 片面的強行規定 (one-sided mandatory provisions), the shift of 告知 from voluntary disclosure
    to **質問応答義務** (answer-the-question duty), and the rule that an insurer may not rescind
    where an intermediary obstructed or induced non-disclosure.
  - **Modelling consequence in one line:** 低解約返戻金型, 自動振替貸付, MVA and the third-sector
    stress test are all named here, so a `jplib` product that models them is modelling a
    regulator-recognised mechanic — and IV-1-12 is the reason 自動振替貸付 must be modelled as an
    **election**, not as an automatic no-lapse rule.

(jplib-reg-r15)=

### R15 — 金融庁 保険課保険モニタリング室,「経済価値ベースのソルベンシー規制の概要」（2026年7月）

- **Publisher:** 金融庁
- **Document:**「経済価値ベースのソルベンシー規制の概要」, 10 pp.
- **Doc type:** FSA explanatory deck
- **URL:** https://www.fsa.go.jp/policy/economic_value-based_solvency/10.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — plain fetchers returned only the binary stream; downloaded with
  `curl` and a browser User-Agent and text-extracted locally. All ten pages read.
- **Annotation:** **The `jplib` analogue of "Solvency UK", and the entry the library index
  leans on.** This is the authoritative short statement of Japan's economic-value regime.
  - **Commencement.** **2026年3月31日 — 経済価値ベースのソルベンシー規制適用開始**, applied "2026年3月期より",
    on a **three-pillar** structure. Scope: 保険会社, 外国保険会社等, 免許特定法人 and 保険持株会社.
    **少額短期保険業者 (small-amount short-term insurers) stay on the old SMR regime.**
  - **What it replaces.** Under the old regime early corrective action was triggered when
    the **SMR fell below 200%**; under ESR it is triggered when the **ESR falls below 100%**
    ("旧規制においては、SMR が 200%を下回った場合を早期是正措置制度の対象としていた"). The three-band ladder is
    carried over by reference: 第一区分 ESR 70–100% → improvement plan, recovery to ≥100% within
    one year in principle; 第二区分 35–70% → measures order, ≥70% within six months; 第三区分 <35%
    → suspension order, ≥35% within three months.
  - **The balance sheet, and the sentence a modeller should carry.** All assets at fair
    value; liabilities re-measured **at the reporting date**. The deck contrasts the old
    **ロックイン** basis — mortality, lapse, incidence and interest all fixed at issue — with the
    ESR basis, on which assumptions are re-set at the 基準日 and future cash flows are
    discounted to present value. 保険負債 = **現在推計** (*genzai suikei*, current estimate) **+
    MOCE** (Margin Over Current Estimate). 責任準備金対応債券 carried at amortised cost in the
    accounting balance sheet are marked to market for ESR. This is the regime change that
    makes a re-projectable, assumption-parameterised liability cash flow model — the thing
    `jplib` builds — the operative artefact rather than a one-off pricing exercise.
  - **所要資本.** Six risk categories — 保険リスク (life risk by stress: 死亡, 長寿, 罹患・障害, 解約・失効,
    経費; non-life risk by factor), 巨大災害リスク, 市場リスク (金利 / 株式 / 不動産 by stress, 為替 / 資産集中
    by factor), 信用リスク and オペレーショナルリスク — aggregated with correlations. Calibration:
    "200年に１度程度のリスクを考慮" — **原則、99.5%の信頼水準**. The standard model and its coefficients
    are set in FSA 告示 [R16] and share their basic structure with the IAIS **ICS** adopted in
    December 2024, modified where Japanese market characteristics require. Internal models
    are permitted at the outset only for natural-catastrophe risk, undertaking-specific
    stress factors (USP) for life and non-life risk, and an internal discount-rate method
    for interest-rate risk.
  - **適格資本.** Tier 1 / Tier 2 with inclusion limits. For a **相互会社** the limited-Tier-1 cap
    is 30% of 所要資本 and Tier 2 is 60% less limited Tier 1 — materially different from a stock
    company, and material because much of the Japanese life market is mutual.
  - **Reporting.** ESR is reported twice a year, at **31 March and 30 September**, with the
    confirmed figure due **within four months** of period end — **seven months** for the
    2026年3月期 first submission.
  - **Calibration evidence.** From the 2025 field test: 生保単体 **ESR 215% against SMR 873%**;
    損保単体 ESR 203% against SMR 750%. The deck attributes the gap to the stricter confidence
    level, broader risk coverage and higher sensitivity to the economic environment. The
    order-of-magnitude difference between the two ratios is the reason a `jplib` document
    must never present an SMR figure and an ESR figure as comparable.
  - **Timeline (page 10).** 1996年4月 SMR introduced; 2007年4月 review-team report proposing a
    move to economic value; 2020年6月 expert-panel report; 2022年6月 provisional decisions;
    2023年6月 finalisation status; 2024年5月「残論点の方向性」; 2024年10月 and 2025年1月 consultations on
    the 施行規則 amendments; 2024年12月 IAIS adopts ICS; **2025年7月 法令・監督指針の公布・公表**; **2026年3月31日
    適用開始**.
  - **Scope limit.** `jplib` computes neither ESR nor SMR. What it owes this entry is that
    its projections are re-runnable on a re-set assumption basis at a stated 基準日, and that
    its documents describe reserving as J-GAAP 標準責任準備金 [R10] *and* name the economic-value
    balance sheet as the second, separate basis [R47].

(jplib-reg-r16)=

### R16 — 金融庁,「経済価値ベースのソルベンシー規制」政策ページ（告示の索引）

- **Publisher:** 金融庁
- **Doc type:** policy index page
- **URL:** https://www.fsa.go.jp/policy/economic_value-based_solvency/
- **Accessed:** 2026-08-20
- **Retrieved:** yes
- **Annotation:** The index to the regime's documents. It links the **第1の柱告示**, **第3の柱告示**
  and **格付告示** as PDFs published **2026-03-23** under `/news/r7/hoken/20260323/` (03.pdf,
  04.pdf and 02.pdf respectively), the amended 保険業法施行規則, the updated 監督指針 (2025-07-23)
  and a Q&A, plus a **yield-curve construction tool** and the March 2026 summary of the 2025
  field-test results. The framing is the three pillars and the objectives of policyholder
  protection, risk-management sophistication and information provision [R16]. **Honest
  limit:** the individual 告示 PDFs were **not opened** in this session, so their paragraph
  structure, the standard-formula stress magnitudes, the correlation matrices and the MOCE
  formula are [unverified] here. [R15] is the retrieved substance; this entry is the map,
  and the place a later research pass starts from.

(jplib-reg-r17)=

### R17 — 金融庁, ソルベンシー・マージン比率（平成8年大蔵省告示第50号 and the 200% threshold）

- **Publisher:** 大蔵省 → 金融庁 (notification); the operative rules are 保険業法施行規則第86条・第87条
  and 平成8年大蔵省告示第50号
- **Doc type:** 告示
- **URL:** not located as a consolidated official text.
- **Accessed:** 2026-08-20
- **Retrieved:** **no** — the 告示 itself was not retrieved. Everything below comes from [R14]
  and [R15], both retrieved, except where flagged.
- **Annotation:** The **200%** figure is the *old* threshold for early corrective action,
  superseded for insurance companies from 2026-03-31 by the ESR 100% trigger [R15]. The
  band ladder is expressed in the guideline's own wording as 100 / 70 / 35 [R14] [R15].
  Whole-market SMR at 31 March 2025 was **873% (life, solo)** and **750% (non-life, solo)**
  [R15]. That the calculation basis is 施行規則第86条・第87条 together with 告示第50号 is
  [unverified — from search summaries, not from a retrieved text]. `jplib` computes neither
  ratio; the entry exists so that a product document referring to "the 200% threshold" cites
  something honest about its own provenance, and so that the pre-2026 framing found in older
  insurer disclosure is dateable.

---

## 2. Actuarial — 日本アクチュアリー会

(jplib-reg-r18)=

### R18 — 日本アクチュアリー会,「標準生命表2018」（生保標準生命表2018 / 第三分野標準生命表2018）

- **Publisher:** 公益社団法人 日本アクチュアリー会 (Institute of Actuaries of Japan)
- **Document:**「標準生命表2018」, 5 pp. (title page plus four tables)
- **Doc type:** mortality table (PDF)
- **URL:** https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — 236,023 bytes downloaded with a browser User-Agent, all five pages
  text-extracted and the numbers read. The alternative URL
  `.../standard-life-table/seimeihyo2018.pdf` seen in search results returns an **HTML error
  page with HTTP 200** — the `pdf/` path segment is required, and the 200 makes the failure
  easy to miss.
- **Annotation:** **The single sharpest contrast between `jplib` and `uklib`, and the entry
  every product's mortality section turns on.** Where `uklib` had to ship **[std]** proxies
  because the CMI tables are restricted to Authorised Users, the Japanese statutory
  valuation tables are **published in full, free, at a stable public URL**, and can be read
  and reproduced numerically by anyone. Four tables, each with columns 年齢 x · 生存数 lx ·
  死亡数 dx · 死亡率 qx · 平均余命 ex, on a radix of 100,000:

  | page | table | q0 | terminal age (qx = 1.00000) |
  |---|---|---|---|
  | 2 | 生保標準生命表2018（死亡保険用）男 | 0.00081 | 109 |
  | 3 | 生保標準生命表2018（死亡保険用）女 | 0.00078 | 113 |
  | 4 | 第三分野標準生命表2018 男 | 0.00053 | 116 |
  | 5 | 第三分野標準生命表2018 女 | 0.00052 | 118 |

  Spot values read directly from the PDF: 死亡保険用 男 q30 = 0.00068, q60 = 0.00653,
  q90 = 0.15760; 死亡保険用 女 q30 = 0.00037, q60 = 0.00363, q90 = 0.09357; 第三分野 男
  q30 = 0.00041, q90 = 0.11657; 第三分野 女 q30 = 0.00022, q90 = 0.07574 [R18]. **What these
  tables are, exactly:** they are the **valuation** tables that [R10] 第1項第2号ハ requires for
  標準責任準備金 on contracts concluded from 1 April 2018 — they carry an explicit prudential
  margin and a forward improvement allowance [R20], and they are **not** best-estimate
  experience tables. Two consequences a product document must not blur. First, a `jplib`
  best-estimate mortality basis is a **[std]** adjustment *of* a sourced table, and each
  document must say which of the two it is using at each point. Second, before assuming
  `jplib` may *ship* these numbers, read [R21]: the publisher's terms restrict
  redistribution. 死亡保険用 applies to term_life, income_guarantee, whole_life, endowment,
  fx_whole_life and the accumulation phase of individual_annuity; 第三分野 to medical, cancer
  and nursing_care; the 2007 年金開始後用 table [R19] to individual_annuity in payment.

(jplib-reg-r19)=

### R19 — 日本アクチュアリー会,「標準生命表2018、標準生命表2007および生保標準生命表1996」（Excel）

- **Publisher:** 公益社団法人 日本アクチュアリー会
- **Document:** single-sheet `.xlsx`, sheet「標準生命表」
- **Doc type:** mortality tables (Excel)
- **URL:** https://www.actuaries.jp/lib/standard-life-table/xlsx/seimeihyo960718.xlsx
- **Accessed:** 2026-08-20
- **Retrieved:** yes — 27,443 bytes downloaded and parsed with `openpyxl`; the header
  strings read from `xl/sharedStrings.xml` because the workbook stores its labels in a
  mis-declared encoding and `openpyxl` returns mojibake for them. **The numeric cells are
  correct**; only the labels need the workaround.
- **Annotation:** The machine-readable form of the standard tables. One sheet, ages **0 to
  130** in the index column and **twelve qx columns** — male then female for each of
  生保標準生命表2018（死亡保険用）· 第三分野標準生命表2018 · 生保標準生命表2007（死亡保険用）·
  **生保標準生命表2007（年金開始後用）** · 生保標準生命表1996（死亡保険用）· 生保標準生命表1996（年金開始後用）; the sheet's
  heading strings also name 第三分野標準生命表2007. Age-0 values verified across the first eight
  columns: 0.00081 / 0.00078 (2018 死亡保険用 M/F), 0.00053 / 0.00052 (第三分野2018 M/F),
  0.00108 / 0.00096 (2007 死亡保険用 M/F) and **0.00058 / 0.00047 (2007 年金開始後用 M/F)**; the
  年金開始後用 female column runs to q126 = 1 [R19]. **This is the only public source found for
  the 年金開始後用 table**, which [R10] and [R11] keep in force for annuities in payment — so it
  is the load-bearing file for individual_annuity's payout phase, and the reason that
  product's accumulation and payout phases read different tables. Redistribution is
  restricted on the same terms as [R18]; see [R21].

(jplib-reg-r20)=

### R20 — 日本アクチュアリー会,「標準生命表２０１８の作成概要」

- **Publisher:** 公益社団法人 日本アクチュアリー会
- **Document:**「標準生命表２０１８の作成概要」, 6 pp. (資料①–⑤)
- **Doc type:** methodology note (PDF)
- **URL:** https://www.actuaries.jp/lib/standard-life-table/pdf/seimeihyo2018-gaiyo.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — downloaded and all six pages text-extracted
- **Annotation:** **This entry is what forces every `jplib` best-estimate basis to be
  [std].** It is the document that says, in the publisher's own words, how much margin is
  inside the tables at [R18].
  - **生保標準生命表2018（死亡保険用）.** Observation years **2008, 2009 and 2011** (2010 excluded for
    the Tōhoku earthquake), with 2005–2009 plus 2011 at young and old ages; **4,068万**
    (male) and **3,002万** (female) policy-years exposed, with **26.3万** and **9.5万** deaths;
    select-period truncation capped at 10 years; policy durations to 30 years.
  - **Mortality improvement is built in ahead of the effective date:** "改善率： 年 2.5％（5 年
    間）、年 1.0％（3 年間）" — 2.5% p.a. for five years, then 1.0% p.a. for three.
  - **A prudential margin is built in:** "将来経験する死亡率が変動予測を超える確率を約 2.28%（２σ水準）
    におさえるように補整した。ただし、…補整前死亡率の 130％を上限として補整した。" — a first-order
    「数学的危険論による補整」 to a 2σ (about 2.28%) exceedance level, capped at 130% of the
    unadjusted rate, sized on an assumed **1 million policies per sex**. A second adjustment
    applies Greville 13-term cubic smoothing; a third splices a Gompertz–Makeham form at age
    84 for both sexes.
  - Terminal age 109 (M) / 113 (F); life expectancy on the table basis **80.77 / 86.56**,
    against 78.24 / 84.94 on the 2007 table.
  - The table is built **for use on a 保険年齢方式 basis** (*hoken nenrei hōshiki*, insurance age
    — nearest birthday) and **includes 高度障害** (severe-disability benefit) inside the death
    rate. Any `jplib` document that ages its model points on 満年齢 must say so and say what it
    does about the difference.
  - **第三分野標準生命表2018 is built differently.** Its base data is the **national 第21回生命表
    (2010)** [R24 lineage](#jplib-reg-r24), not insured experience — the note explains that third-sector
    cover has moved from rider to stand-alone main contract and that its underwriting
    differs from death cover. The same 2.5% / 1.0% improvement is applied, and the
    risk-theory adjustment is bounded **below at 70% and above at 85%** of the
    pre-adjustment rate — i.e. the table is deliberately set *below* national mortality,
    because on a morbidity product longer survival means more claims. Terminal age 116 (M) /
    118 (F); life expectancy 83.47 / 89.59. **第三分野標準生命表2018 excludes 高度障害**, unlike the 2007
    version.
  - **Stated plainly for every product document:** 標準生命表2018 is a **valuation** table
    carrying an explicit roughly-2σ margin and a forward improvement allowance. A `jplib`
    best-estimate basis is therefore a **[std]** adjustment of a sourced table, and the
    direction of the margin is *opposite* between 死亡保険用 (margin up, prudent for death
    cover) and 第三分野 (margin down, prudent for morbidity cover). A model that applies one
    sign of adjustment to both is wrong.

(jplib-reg-r21)=

### R21 — 日本アクチュアリー会, 標準生命表 index pages and site 利用規約

- **Publisher:** 公益社団法人 日本アクチュアリー会
- **Doc type:** institutional pages (index, table-vintage page, terms of use)
- **URLs:** https://www.actuaries.jp/lib/standard-life-table/ ·
  https://www.actuaries.jp/lib/standard-life-table/index2018.html ·
  https://www.actuaries.jp/use/
- **Accessed:** 2026-08-20
- **Retrieved:** yes (all three)
- **Annotation:** The index lists 標準生命表2018, 標準生命表2007 and 生保標準生命表1996, the consolidated
  Excel [R19], and for 2018 three PDFs: the tables [R18], the 作成概要 [R20] and the 作成過程
  (`seimeihyo2018-katei.pdf`, **not opened this session** — [unverified]). The 2018 page
  states the tables apply from April 2018 and carries an IAJ copyright notice. The site
  利用規約 states that copyright and other intellectual property in the published material
  belongs to the IAJ and its cooperating bodies unless otherwise stated, and **prohibits
  reproduction and alteration, transmission to third parties, and commercial use** without
  prior written consent [R21]. **The consequence a drafter must not skip.** The framing "the
  Japanese standard tables are public, so `jplib` can ship a real citable table" is **half
  right and must be written as half right**: the tables are publicly retrievable and freely
  readable — that is the real and large contrast with the subscriber-restricted CMI tables —
  but the publisher's terms restrict redistribution. `jplib` therefore cites [R18] and [R19]
  by URL, reproduces only the individual rates its worked examples need, and ships its
  mortality `.csv` as a **[std]** table whose `provenance` column points at [R18] / [R19],
  rather than as a verbatim copy of the IAJ file. Anything stronger needs the IAJ's written
  consent.

(jplib-reg-r22)=

### R22 — 日本アクチュアリー会,「生命保険会社の保険計理人の実務基準」

- **Publisher:** 公益社団法人 日本アクチュアリー会
- **Document:**「生命保険会社の保険計理人の実務基準」, 19 pp.; 制定 平成8年12月9日, latest 改正 **令和8年3月2日**
  (the landing page dates publication 2026-03-19 and the FSA Commissioner's 認定 2026-03-13;
  applied from the FY2025 year-end accounts)
- **Doc type:** professional practice standard (PDF)
- **URLs:** https://www.actuaries.jp/lib/practice-standard/seiho_jitumukijun.html ·
  https://www.actuaries.jp/lib/practice-standard/pdf/seiho_jitumukijun_20260319.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — full PDF downloaded and read
- **Annotation:** **The most directly model-relevant actuarial document in Japan**, and the
  entry that says what a Japanese liability cash flow projection is *for*.
  - 第1条: the standard is the standard practice for a 保険計理人 appointed under 法第120条 [R5] and
    is "平成 12 年金融監督庁・大蔵省告示第 22 号に定める基準として、金融庁長官の認定を受けた基準" — a professional
    standard with statutory recognition. A 保険計理人 may depart from it, but must disclose the
    departure in the 意見書 [R6] and justify the alternative in the 附属報告書.
  - 第8条 defines 責任準備金 as the amount, actuarially evaluated, that the company must accumulate
    so that its future ability to pay is not impaired, having regard to claim incidence,
    expense outgo and investment conditions.
  - 第9条: the 保険計理人 confirms (i) that the year-end reserve is properly accumulated under
    規則第69条第1項・第2項・第4項 [R8], and (ii) by the **1号収支分析** — a forward income-and-outgo
    analysis — that its level is sufficient. The subject of the analysis is in principle the
    **保険料積立金** at the year end, adding 未経過保険料 where judged necessary. Contracts exempt:
    unit-linked without a guarantee; contracts with no 保険料積立金; contracts whose 約款 allows
    the insurer to change the calculation coefficients (from 2001, the 予定利率); and others
    where the standard-reserve coefficients are unsuitable.
  - **第11条: the 1号収支分析 is performed annually and its analysis period is "少なくとも将来 10 年間"
    — at least ten future years**, by 区分経理 product segment, finer or coarser where
    justified. This is the shape of the projection `jplib` writes: per-segment, per-policy
    premiums, claims, expenses and surrenders over a decade or more.
  - 第12条 **1号収支分析(1)**, the stochastic form: scenarios generated probabilistically from an
    interest-rate model, with new business, persistency, mortality and other incidence
    rates, expenses, FX-asset investment income, asset allocation, dividends and transfers
    to 価格変動準備金 and 危険準備金 all set reasonably from past experience. Equity valuation gains are
    in principle **not** released to fund reserves; general-account equity, property and FX
    price movements are **not** projected as P&L; a **closed** variant sets future new
    business and its expenses to zero. Sufficiency: the reserve is sufficient if, in **≥90%
    of scenarios**, the standard reserve (or the FSA-approved reserve) can be accumulated at
    each year end over the **first five years** of the analysis period.
  - 第13条 **1号収支分析(2)**, the deterministic multi-scenario form: sufficiency requires the
    reserve to be accumulable in **all** scenarios over the first five years.
  - **第13条の2 1号基本シナリオ**, the prescribed deterministic scenarios. Interest: (イ) start from
    the latest **長期国債応募者利回り** and fall by `X/5` percentage points each year for five years,
    then hold flat; (ロ) start from the same yield and fall by `X/2` percentage points at the
    start of the next fiscal year, then hold flat; where `X = max(latest 長期国債応募者利回り −
    標準利率 at the start of the analysis period, 0)`. **For USD- and AUD-denominated contracts,
    "長期国債応募者利回り" is read as the A-rated 10-year corporate bond yield in the liability
    currency** — the same substitution [R10] 第10項–第12項 makes for the standard rate. Equity
    valuation gains may fund reserves only up to book value × (latest JGB yield or the
    standard rate) less dividends. Bonds are held at **原価法** — no interest-driven
    revaluation. **For MVA products, realised gains on the matching bonds may fund reserves
    up to the reserve increase the MVA mechanism itself causes.**
  - 第17条 onwards cover the 法第121条第1項第2号 confirmation — that 契約者配当 is fair and equitable.
  - **Modelling consequence.** The 1号収支分析 is Japan's liability-adequacy and
    cash-flow-testing regime, expressed in exactly the terms `jplib` projects in:
    per-segment projected premiums, claims, expenses and surrenders over ≥10 years, closed
    and open variants, deterministic scenario sets, and explicit MVA and FX carve-outs. The
    FX and MVA provisions are decisive for fx_whole_life.

(jplib-reg-r23)=

### R23 — 金融庁, 監督指針 VI.（日本アクチュアリー会関係 — the 指定法人 role）

- **Publisher:** 金融庁 (section view of [R14])
- **Doc type:** supervisory guideline (section)
- **URL:** https://www.fsa.go.jp/common/law/guide/ins/06.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes
- **Annotation:** The IAJ is the **指定法人 under 法第122条の2第1項**. Its members' expertise is
  applied to 責任準備金積立の評価, to 配当等における公正性及び衡平性の確保, to the supply of diverse, good-quality
  products meeting user needs, and to 各種統計資料の作成・分析. Under **法第122条の2第2項第3号** the IAJ is
  entrusted with producing the **coefficients and standards forming the basis of the
  policy-reserve calculation**, with an emphasis on publication, transparency and periodic
  review [R23]. This is the statutory route by which the 標準生命表 of [R18]–[R20] become the
  tables that 告示第48号 [R10] points at — the answer to "on what authority does a private
  professional body's table bind a statutory reserve?".

---

## 3. Statistics and experience data — public and citable

(jplib-reg-r24)=

### R24 — 厚生労働省, 第23回生命表（完全生命表）令和2年

- **Publisher:** 厚生労働省 政策統括官付参事官付人口動態・保健社会統計室
- **Doc type:** national statistics (complete life table)
- **URLs:** https://www.mhlw.go.jp/toukei/saikin/hw/life/23th/index.html · tables
  https://www.mhlw.go.jp/toukei/saikin/hw/life/23th/xls/23th-08.xlsx (男 / 女 sheets)
- **Accessed:** 2026-08-20
- **Retrieved:** yes — the page fetched with `curl` and decoded from CP932 (mhlw.go.jp HTML
  is CP932 and is garbled by plain fetchers); the workbook downloaded and parsed; the
  methodology PDF `dl/23th-02.pdf` read.
- **Annotation:** The 23rd table is the **令和2年 (2020)** complete life table — the 22nd
  actually produced, 第7回 being a skipped number — built from the confirmed Japanese-national
  population of the **2020 Census** and confirmed vital statistics (2020 deaths; 2019 and
  2020 births). 平均寿命 **男 81.56 / 女 87.71**, up 0.81 / 0.73 on the previous complete table.
  寿命中位数 男 84.51 / 女 90.55. e20 = 61.90 / 68.01; e65 = 19.97 / 24.88; e75 = 12.54 / 16.22.
  Deaths peak at age 88 (4,133 per 100,000) for men and 93 (5,130) for women. The workbook
  carries single-year x, lx, ndx, npx and related functions to **age 113** [R24]. Fully
  public, freely downloadable, single-year population mortality — **the redistributable
  comparison basis against which the safety margin in 標準生命表2018 [R20] can actually be
  quantified**, and the base data lineage of the 第三分野 table.

(jplib-reg-r25)=

### R25 — 厚生労働省, 令和6年簡易生命表

- **Publisher:** 厚生労働省
- **Doc type:** national statistics (abridged life table)
- **URLs:** https://www.mhlw.go.jp/toukei/saikin/hw/life/life24/index.html · tables
  https://www.mhlw.go.jp/toukei/saikin/hw/life/life24/xls/life24-12.xlsx
- **Accessed:** 2026-08-20
- **Retrieved:** yes — page fetched with `curl` and decoded from CP932; workbook downloaded
  and parsed
- **Annotation:** The 令和6年 **(2024)** abridged table: two sheets, 男 and 女, with columns 年齢 x
  · 死亡率 nqx · 生存数 lx · 死亡数 ndx · 定常人口 nLx, Tx · 平均余命 ex, radix 100,000, running from
  sub-annual bands (0週, 1週, 2週, 3週, 4週, 2月, 3月, …) to age 120+. **平均寿命 男 81.09 / 女
  87.13.** Also published: 寿命中位数, an international comparison, a cause-of-death analysis
  and a 図表 workbook [R25]. The annual refresh between complete tables. **A trap to record
  in any document that uses it:** its q0 (0.00074 male, 0.00067 female at the 0週 band) is
  not comparable to an annual q0 without aggregating the sub-annual bands.

(jplib-reg-r26)=

### R26 — 厚生労働省, 令和5年(2023)患者調査 — 受療率

- **Publisher:** 厚生労働省
- **Doc type:** national statistics (patient survey)
- **URLs:** https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/index.html ·
  https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/jyuryouritu.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — the 受療率 PDF downloaded and both its tables read in full
- **Annotation:** **The medical morbidity anchor.** Survey reference **October 2023**.
  National 受療率 (*juryō-ritsu*, treatment-receiving rate) per 100,000 population: **入院 945,
  外来 5,850**; by sex 入院 893 (M) / 995 (F), 外来 5,118 / 6,544. By age band (入院, both sexes):
  0歳 1,237 · 1–4 153 · 5–9 86 · 10–14 87 · 15–19 115 · 20–24 137 · 25–29 182 · 30–34 239 ·
  35–39 242 · 40–44 258 · 45–49 318 · 50–54 441 · 55–59 613 · 60–64 838 · 65–69 1,117 ·
  70–74 1,502 · 75–79 2,033 · 80–84 2,952 · 85–89 4,413 · 90歳以上 6,275; restated aggregates
  65歳以上 2,449 and 75歳以上 3,351. By cause (入院, per 100,000): 精神及び行動の障害 171, 循環器系の疾患 147
  (脳血管疾患 88, 心疾患 46), 損傷・中毒等 107 (骨折 77), 神経系の疾患 99 (アルツハイマー病 42), **新生物 96, of which
  悪性新生物 85**, 呼吸器系 67, 筋骨格系 59, 消化器系 48, 腎尿路生殖器系 41 (慢性腎臓病 18), 内分泌・栄養・代謝 23 (糖尿病 10)
  [R26]. **The modelling trap, stated once here so every third-sector document can cite
  it:** an 入院 受療率 is a point-in-time **prevalence** per 100,000, not an incidence rate.
  Turning it into the incidence × duration structure a 日額 (daily-benefit) product needs
  requires the 平均在院日数 of [R27] and an explicit **[std]** conversion step, which must be
  labelled as such.

(jplib-reg-r27)=

### R27 — 厚生労働省, 令和5年(2023)患者調査 — 退院患者の平均在院日数

- **Publisher:** 厚生労働省
- **Doc type:** national statistics (patient survey)
- **URL:** https://www.mhlw.go.jp/toukei/saikin/hw/kanja/23/dl/heikin.pdf
- **Accessed:** 2026-08-20
- **Retrieved:** yes — PDF downloaded, tables read
- **Annotation:** Discharges during **September 2023**. Average length of stay by facility:
  **病院 29.3 日, 一般診療所 14.2 日**; all facilities **28.4 日**. By age band (all facilities):
  0–14 **7.6**, 15–34 **10.5**, 35–64 **20.2**, 65歳以上 **35.5**, 70歳以上 36.7, 75歳以上 39.0.
  By cause (total, days): 精神及び行動の障害 **290.4** (統合失調症等 569.5), 神経系の疾患 **93.3**
  (アルツハイマー病 279.6), 循環器系の疾患 **34.6**, 内分泌・栄養・代謝 24.7 (糖尿病 31.8), 感染症 25.1 (結核 44.3),
  血液・造血器 18.1, **新生物 13.4, of which 悪性新生物 14.4** — 胃 14.7, 結腸及び直腸 15.3, 肝及び肝内胆管 13.6,
  気管・気管支及び肺 14.1, 乳房 9.4. The long-run 病院 trend runs 40.9 日 (昭和59) → 29.3 日 (令和5)
  [R27]. **This is why a Japanese medical product's 支払限度日数** (*shiharai gendo nissū*, the
  per-hospitalisation benefit-day limit, commonly 60 or 120 days) **binds only in the
  tail**: the mean stay for a cancer admission is about 14 days but for a psychiatric
  admission about
  290. A model that applies one mean duration across causes gets the limit's bite badly
  wrong, and the falling long-run trend means a duration assumption calibrated to older data
  overstates claim cost.

(jplib-reg-r28)=

### R28 — 国立がん研究センター がん情報サービス, 最新がん統計

- **Publisher:** 国立がん研究センター がん情報サービス
- **Doc type:** national cancer statistics (summary page)
- **URL:** https://ganjoho.jp/reg_stat/statistics/stat/summary.html
- **Accessed:** 2026-08-20 (page last updated 2026-07-14)
- **Retrieved:** yes
- **Annotation:** **罹患数 993,469 (2023)** — 男 556,059, 女 437,406. **死亡数 384,111 (2024)** —
  男 221,786, 女 162,325. **生涯罹患確率 男 61.1% / 女 50.1%**, roughly one in two. **5年相対生存率
  64.8%** overall for 2018 diagnoses — 男 63.2%, 女 66.8% [R28]. The cancer anchor: a lifetime
  incidence probability above 50% is what makes a stand-alone がん保険 a mass-market product in
  Japan rather than a niche rider, and the survival rate is what makes a diagnosis benefit
  plus a treatment-linked benefit stream, rather than a death benefit, the right shape.

(jplib-reg-r29)=

### R29 — 国立がん研究センター がん情報サービス, がん統計 データダウンロード

- **Publisher:** 国立がん研究センター がん情報サービス
- **Doc type:** statistics download index
- **URL:** https://ganjoho.jp/reg_stat/statistics/data/dl/index.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes (index page; the individual workbooks were **not** opened)
- **Annotation:** Downloadable Excel datasets: **死亡数・率** from 人口動態統計, national 1958–2024
  and by prefecture and site 1995–2024; **罹患数・率** from the **全国がん登録** (national cancer
  registry) 2016–2023, national and by prefecture, plus a long series splicing regional
  registries with the national registry 1985–2023 and childhood/AYA cases 2009–2011;
  **生存率** — national-registry 5-year survival for 2016–2018 diagnoses, regional registry
  1993–2011, 10-year and conditional survival 2002–2006; **将来推計** of incidence, mortality
  and prevalence 2015–2054; and prefecture smoking rates 2001–2022. Use requires attribution
  to "Cancer Statistics. Cancer Information Service, National Cancer Center, Japan" with the
  underlying source named (全国がん登録 or 人口動態統計) [R29]. Age-and-site incidence rates for a
  cancer model are obtainable here and — unlike a carrier's pricing basis — are citable. The
  `jplib` cancer incidence input should be a **[std]** table whose `provenance` column
  points here, with the attribution string carried.

(jplib-reg-r30)=

### R30 — 厚生労働省 老健局, 令和5年度 介護保険事業状況報告（年報）

- **Publisher:** 厚生労働省 老健局
- **Doc type:** administrative statistics (annual report)
- **URLs:** https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/index.html · ポイント
  https://www.mhlw.go.jp/topics/kaigo/osirase/jigyo/23/dl/r05_point.pdf · 全国版 workbook
  `dl/r05_zenkokukei.xlsx`
- **Accessed:** 2026-08-20
- **Retrieved:** yes — the ポイント PDF downloaded and read; **the 全国版 workbook was not
  opened**, so the full age × grade grid is [unverified] here
- **Annotation:** **The nursing-care anchor**, at **31 March 2024** unless stated. 第1号被保険者
  (aged 65+) **3,589万人**. **要介護（要支援）認定者数 708万人**, up 14万 or 2.0% on the year. **認定率 =
  認定者 / 第1号被保険者 = 19.4%** (+0.4pt), decomposed by age as **65歳以上75歳未満 4.3%** and
  **75歳以上 31.1%** — a more-than-sevenfold step at 75. Composition by care level: 要支援1
  **14.4%**, 要支援2 **14.1%**, 要介護1 **20.7%**, 要介護2 **16.8%**, 要介護3 **13.1%**, 要介護4
  **12.6%**, 要介護5 **8.3%**. Service recipients averaged **609万人 per month** in FY2023; total
  cost **11兆7,186億円**, benefits paid **10兆8,263億円** [R30]. Modelling consequence: a
  公的介護保険連動型 product pays on a stated 要介護度 — commonly 要介護2 or above — so the level
  composition above is the ratio that turns an all-levels prevalence into a
  benefit-triggering prevalence: 要介護2以上 is 16.8 + 13.1 + 12.6 + 8.3 = **50.8%** of 認定者.
  That single arithmetic step is the reason nursing_care can be modelled from public data at
  all.

(jplib-reg-r31)=

### R31 — 生命保険協会,「２０２５年版 生命保険の動向」

- **Publisher:** 一般社団法人 生命保険協会 (Life Insurance Association of Japan, LIAJ)
- **Document:**「２０２５年版 生命保険の動向」, 33 pp., issued **2025年11月**
- **Doc type:** industry statistics
- **URL:** https://www.seiho.or.jp/data/statistics/trend/pdf/all_2025.pdf (index:
  https://www.seiho.or.jp/data/statistics/trend/)
- **Accessed:** 2026-08-20
- **Retrieved:** yes — full PDF downloaded, text extracted, contract-trend and payout
  sections read
- **Annotation:** Market structure and the only published industry-wide persistency figure,
  for **FY2024** (year to 31 March 2025), member companies.
  - **個人保険 in force: 1億9,530万件** — a 17th consecutive annual increase — and **778兆9,902億円**
    of sum insured, 98.5% of the prior year, falling as the market shifts from death cover
    to medical cover.
  - In force **by policy count**: 医療保険 **4,545万件 (23.3%)** · 終身保険 3,848万 (19.7%) · 定期保険
    2,721万 (13.9%) · ガン保険 2,522万 (12.9%) · 養老保険 734万 (3.8%).
  - In force **by sum insured**: 定期保険 **300兆4,672億円 (38.6%)** · 終身保険 215兆962億 (27.6%) ·
    変額保険 47兆6,016億 (6.1%) · 定期付終身保険 29兆1,313億 (3.7%) · 養老保険 27兆379億 (3.5%).
  - New business **by count**: 医療保険 296万 (23.8%) · 終身保険 231万 (18.6%) · ガン保険 159万 (12.8%) ·
    定期保険 135万 (10.9%) · 変額保険 99万 (8.0%). **By sum insured**: 定期保険 24兆6,666億 (43.2%) ·
    終身保険 12兆9,965億 (22.8%) · 変額保険 10兆7,797億 (18.9%) · 養老保険 1兆5,347億 (2.7%) · こども保険 3,477億
    (0.6%).
  - **解約・失効率（個人保険）= 5.6%** of opening in-force sum assured, down 0.3pt; **個人年金保険 3.4%**
    on pre-annuitisation contracts, down 0.1pt.
  - **個人年金保険**: in force **2,006万件 / 104兆1,428億円**; 定額年金 87.5% of count and 84.4% of
    amount, 変額年金 12.5% / 15.6%. New business 147万件 / 9兆4,843億円, of which 定額年金 5兆4,646億
    (57.6%).
  - **年換算保険料**: in force 個人保険 **22兆1,448億円**, 個人年金 6兆1,399億; **第三分野 in force 7兆3,062億円**
    with new business 5,555億円 — third-sector annualised premium has risen every year in the
    published series.
  - **Benefits paid**: 死亡保険金 124万件 / 4兆2,529億円; 満期保険金 108万件 / 2兆2,567億円; **入院給付金 800万件 /
    7,598億円**; **手術給付金 561万件 / 4,900億円**.
  - **一般勘定利回り 1.71%** (prior year 2.75%) — 公社債 0.76%, 株式 16.49%, 外国証券 2.48%, 一般貸付
    1.58%, 不動産 2.73%.
  - Premium income by payment mode, 一時払 39.9% / 月払 38.8% / 年払 15.3%, is **[unverified]** —
    that line came from a search-result summary of the same document, not from the pages
    read.
  - **Modelling consequence.** The lapse figure is the only published, industry-wide
    persistency number in the Japanese market: **5.6% p.a. on 個人保険 and 3.4% on 個人年金**. Any
    **[std]** lapse assumption in `jplib` must be reconciled to it and must say so. The
    product mix is the evidence for the library's framing that the third sector dominates by
    policy count while term and whole life dominate by sum insured.

(jplib-reg-r32)=

### R32 — 生命保険文化センター, 2024（令和6）年度「生命保険に関する全国実態調査」

- **Publisher:** 公益財団法人 生命保険文化センター (JILI)
- **Document:** 2024年度 全国実態調査, published **2025年1月**; household sample **n = 4,000**
- **Doc type:** household survey
- **URLs:** https://www.jili.or.jp/research/report/9849.html · data workbooks under
  `https://www.jili.or.jp/files/research/zenkokujittai/xls/r6/` (`3-1.xlsx`, `3-2.xlsx`,
  `3-10.xlsx`, `2-1.xlsx`, `1-21.xlsx`, `1-52.xlsx`, `all.zip`)
- **Accessed:** 2026-08-20
- **Retrieved:** yes — landing page fetched and seven data workbooks downloaded and parsed
- **Annotation:** Household penetration, on a **民保加入世帯 base** — households insured with a
  private-sector life insurer, the survey's own base, which excludes the postal insurer
  (n = 3,085):
  **医療保険・医療特約 世帯 95.1%** (世帯主 90.0%, 配偶者 69.8%); **ガン保険・ガン特約 世帯 68.2%** (世帯主 60.7%,
  配偶者 46.5%); **介護保険・介護特約 世帯 20.1%** (世帯主 16.8%, 配偶者 11.0%; 加入していない 48.4%, 不明 31.4%).
  On the full sample (n = 4,000), **個人年金保険 世帯加入率 23.2%**. 普通死亡保険金 and 年間払込保険料 are
  published as **banded distributions** (n = 3,568), not as a single mean — for example
  年間払込保険料 12万円未満 17.8%, 12–24万 19.3%, 24–36万 15.7% [R32]. **Honest limits.** The large
  不明 share on the nursing-care question makes the 20.1% a **floor**, not a point estimate.
  The headline 生命保険世帯加入率 and the published **means** of 世帯普通死亡保険金 and 世帯年間払込保険料 sit in
  summary tables that were **not read cell by cell** in this session and are [unverified]
  here; the penetration and band figures above were read directly from the workbooks.
  Modelling consequence: model-point sums assured and premium levels in `jplib` should sit
  inside these observed bands and cite this entry when they do.

(jplib-reg-r33)=

### R33 — 総務省統計局 / 統計センター, e-Stat 政府統計の総合窓口

- **Publisher:** 総務省統計局 / 独立行政法人統計センター
- **Doc type:** statistics portal
- **URL:** https://www.e-stat.go.jp/ (terms at https://www.e-stat.go.jp/terms-of-use)
- **Accessed:** 2026-08-20
- **Retrieved:** yes (home page; **the terms-of-use page itself was not opened**)
- **Annotation:** The single portal for Japanese official statistics, run by the Statistics
  Bureau and the Statistics Center. It exposes 統計表, searchable databases, downloadable
  files, an **API** and dashboard visualisations across 17 themes and by publishing ministry
  [R33]. Its use in this library is as the access route to the machine-readable forms of
  [R26], [R27] and [R30] — 患者調査 tables under `toukei=00450022` and 介護保険事業状況報告 under
  `tid=000001031648`, both links taken from the MHLW pages retrieved for those entries.
  Where a `jplib` input CSV needs a full age × cause grid rather than a summary PDF, this is
  where it comes from. **Honest limit:** the specific licence terms for reuse are on the
  linked 利用規約 page, which was **not read** — [unverified].

---

## 4. Legislation, conduct and consumer protection

(jplib-reg-r34)=

### R34 — e-Gov 法令検索, 保険法 第51条（保険者の免責）

- **Publisher:** e-Gov 法令検索 — 保険法, 平成二十年法律第五十六号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%BA%8C%E5%8D%81%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E4%BA%94%E5%8D%81%E5%85%AD%E5%8F%B7;article=51
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** "死亡保険契約の保険者は、次に掲げる場合には、保険給付を行う責任を負わない。" — 一 **被保険者が自殺
  をしたとき** (the insured commits suicide); 二 保険契約者が被保険者を故意に死亡させたとき; 三
  保険金受取人が被保険者を故意に死亡させたとき, with a proviso preserving cover for other beneficiaries;
  四 **戦争その他の変乱によって被保険者が死亡したとき** [R34]. **The point a protection document must
  make.** The statutory suicide exclusion has **no time limit at all**. The familiar
  Japanese 免責期間 — commonly measured in years from the 責任開始日 (*sekinin kaishi-bi*, date cover
  attaches), and materially longer than the UK's twelve months — is a **contractual
  narrowing** of 第51条第1号 in the 約款, not a statutory period. Its length is therefore a
  per-carrier fact, to be sourced from each 約款 with an `[S#]` tag and never asserted as law.

(jplib-reg-r35)=

### R35 — e-Gov 法令検索, 保険法 第55条（告知義務違反による解除）

- **Publisher:** e-Gov 法令検索 — 保険法, 平成二十年法律第五十六号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%BA%8C%E5%8D%81%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E4%BA%94%E5%8D%81%E5%85%AD%E5%8F%B7;article=55
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** 第1項 lets the insurer rescind where the policyholder or the insured,
  **故意又は重大な過失** (intentionally or by gross negligence), failed to disclose or misstated a
  告知事項. 第2項 bars rescission where the insurer knew or negligently failed to know, where an
  intermediary obstructed disclosure, or where an intermediary induced non-disclosure or a
  false statement; 第3項 disapplies those bars where the breach would have happened anyway.
  **第4項, verbatim:** "第一項の規定による解除権は、保険者が同項の規定による解除の原因があることを知った時から
  **一箇月間**行使しないときは、消滅する。生命保険契約の締結の時から**五年**を経過したときも、同様とする。" [R35].
  Modelling consequence: the statutory contestability ceiling is **five years from
  inception**, with a **one-month** use-it-or-lose-it clock from discovery. Carriers
  commonly contract to two years, which is permitted because it favours the policyholder
  (片面的強行規定, [R14] IV-1-18) — so the contestability window in a product document is again a
  per-carrier `[S#]` fact bounded by a statutory maximum. 保険法 is Act No. 56 of 2008, in
  force from **1 April 2010** ([R14] IV: "平成 22 年 4 月より保険法が施行されており").

(jplib-reg-r36)=

### R36 — e-Gov 法令検索, 保険業法 第309条（クーリング・オフ）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=309
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** An applicant or policyholder may withdraw or cancel by written document or
  electromagnetic record, **except** where **eight days** have passed from the later of the
  date the disclosure document was delivered and the application date; or the contract is
  business or commercial; or the applicant is a corporation or public body; or the
  **insurance period is one year or less**; or the cover is legally compulsory; or the
  application was made at the insurer's office or an equivalent place where policyholder
  protection is otherwise adequate. Withdrawal takes effect **when the document is
  dispatched** ("当該書面を発した時"), or when the storage medium is sent. The insurer may claim
  neither damages nor a penalty, must return the money promptly, and on cancellation may
  retain the premium for the period on risk [R36]. Modelling consequence: an eight-day
  dispatch-rule cooling-off is a real early-duration decrement on every `jplib` product
  whose term exceeds one year. `jplib` models from the point cover is in force and treats
  the cooling-off window as **out of scope** — each product document says so rather than
  silently omitting it.

(jplib-reg-r37)=

### R37 — e-Gov 法令検索, 保険業法 第300条の2（特定保険契約と金融商品取引法の準用）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=300_2
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** A **特定保険契約** (*tokutei hoken keiyaku*, specified insurance contract) is a
  contract under which a loss may arise from movements in interest rates, currency values,
  market prices or other indicators specified by reference to 金融商品取引法第2条第14項 —
  characterised by the possibility that **total premiums paid exceed total benefits
  received**. For such contracts the listed FIEA provisions apply mutatis mutandis to
  insurers, foreign insurers and brokers, covering advertising rules, pre-contract
  disclosure
  (契約締結前交付書面), the prohibition on loss compensation, the **適合性の原則** (suitability
  principle) and the professional-investor regime, with defined-term substitutions [R37].
  Modelling consequence: **変額保険, 変額年金 and 外貨建保険 are 特定保険契約**, so their sales conduct is
  FIEA-grade, and this is the statutory reason the 監督指針 [R14] carries the extra 外貨建て保険 and
  MVA disclosure items. For fx_whole_life and a variable individual_annuity the design point
  follows directly: the possibility of a loss against premiums paid is **not a defect to be
  smoothed away in the documentation — it is the definitional feature**, and a model that
  cannot produce that outcome in some scenario is mis-specified.

(jplib-reg-r38)=

### R38 — e-Gov 法令検索, 消費者契約法 第4条（誤認・困惑等による取消し）

- **Publisher:** e-Gov 法令検索 — 消費者契約法, 平成十二年法律第六十一号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E5%8D%81%E4%BA%8C%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E5%85%AD%E5%8D%81%E4%B8%80%E5%8F%B7;article=4
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** A consumer may rescind an offer or acceptance induced by **不実告知** (telling
  the consumer something contrary to fact about a 重要事項); **断定的判断の提供** (providing a
  conclusive judgement about a future amount or value that is by nature uncertain, so that
  the consumer believes it certain); **不利益事実の不告知** (intentionally or by gross negligence
  failing to disclose a disadvantageous fact about a 重要事項); **困惑** (a list of
  distress-inducing sales behaviours); and **過量契約** (soliciting a quantity significantly
  beyond the consumer's normal needs while knowing it) [R38]. Modelling relevance is
  indirect but structural: the **断定的判断の提供** limb makes it actionable to illustrate a
  non-guaranteed 積立利率 (*tsumitate riritsu*, crediting rate) or 契約者配当 as if it were certain.
  That is the legal reason a Japanese illustration separates 保証 from 非保証 elements — which
  is exactly the (a) contractual/guaranteed versus (b) insurer-discretionary split `jplib`'s
  technical notes use for assumption inputs.

(jplib-reg-r39)=

### R39 — e-Gov 法令検索, 金融サービスの提供及び利用環境の整備等に関する法律 第4条（説明義務）

- **Publisher:** e-Gov 法令検索 — 平成十二年法律第百一号 (formerly 金融商品の販売等に関する法律)
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E5%8D%81%E4%BA%8C%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%B8%80%E5%8F%B7;article=4
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API; the response confirmed the law number 平成十二年法律第百一号)
- **Annotation:** A seller of a financial product must explain the **重要事項** before sale,
  covering the risk that principal is lost through movements in market indicators; the risk
  that losses exceed principal through the same; the same two risks arising from a change in
  the issuer's or counterparty's condition; other material risks set by ordinance; and any
  **exercise period or restriction on cancellation**. 第2項, verbatim: "説明は、顧客の知識、経験、
  財産の状況及び当該金融商品の販売に係る契約を締結する目的に照らして、当該顧客に理解されるために必要な方法及び程度によるもので
  なければならない。" 第7項 exempts 特定顧客 and customers who expressly waive the explanation [R39].
  Modelling consequence: the "restriction on cancellation" limb is the statutory hook for
  disclosing a **解約控除** (*kaiyaku kōjo*, surrender charge), an **MVA**, and a **低解約返戻金型**
  (*tei-kaiyaku-henreikin-gata*, suppressed-surrender-value) period — all three are cash
  flow features `jplib` models explicitly, and all three are disclosed because of this
  article.

(jplib-reg-r40)=

### R40 — 生命保険契約者保護機構, 保険契約者保護制度 Q&A

- **Publisher:** 生命保険契約者保護機構 (Life Insurance Policyholders Protection Corporation of
  Japan)
- **Doc type:** institutional Q&A
- **URL:** https://www.seihohogo.jp/qa/qa1.html (home: https://www.seihohogo.jp/)
- **Accessed:** 2026-08-20
- **Retrieved:** yes (the Q1 page; the home page carries only navigation, and **Q13 — the
  高予定利率契約 page — was not opened**)
- **Annotation:** The Corporation was established under 保険業法 and began operating on **1
  December 1998**. On a member insurer's failure, contracts transferred to or assumed by a
  successor are covered "**破綻時点の補償対象契約の責任準備金等の90％まで**" — up to **90% of the policy
  reserve** at the failure date — and benefits are then paid at 90% of the previous sum
  insured [R40]. **高予定利率契約 are covered at a reduced rate, stated on the Corporation's Q13,
  which was not retrieved.** What is [unverified] here: that a 高予定利率契約 is one whose 予定利率
  exceeded a 基準利率 (3% as at April 2006) throughout the five years before failure, and the
  reduction formula — both come from a search-result summary of member insurers' disclosure
  pages, not from a retrieved primary page. That the 90% figure's statutory chain runs
  保険業法第270条の3 → 内閣府令・財務省令 is established by [R41]; **the 90% number itself is set in the
  ordinance, which was not retrieved**. Modelling consequence: a 90%-of-reserve floor and
  the possibility of a downward revision of the 予定利率 on transfer are the Japanese tail risk
  a policyholder faces — cited, never modelled.

(jplib-reg-r41)=

### R41 — e-Gov 法令検索, 保険業法 第270条の3（資金援助と補償率の委任）

- **Publisher:** e-Gov 法令検索 — 保険業法, 平成七年法律第百五号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B8%83%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%94%E5%8F%B7;article=270_3
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** The article governs financial assistance on a transfer of insurance
  contracts. 補償対象契約 are the contracts meeting standards set by 内閣府令・財務省令, and the
  compensation amount is "**特定責任準備金等の額に、補償対象契約の種類、予定利率その他の内容等を勘案して
  内閣府令・財務省令で定める率を乗じて得た額**" — the specified policy reserve multiplied by a rate the
  ordinance sets, having regard to the contract type, the **予定利率** and other contents [R41].
  **The term 高予定利率契約 does not appear in 第270条の3**; both the 90% and the reduced rate live in
  the ordinance, which was not retrieved here. Cited alongside [R40] so that a product
  document can state the statutory chain accurately without over-claiming the number.

(jplib-reg-r42)=

### R42 — e-Gov 法令検索, 介護保険法 第7条（要介護状態・要支援状態の定義）

- **Publisher:** e-Gov 法令検索 — 介護保険法, 平成九年法律第百二十三号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E5%B9%B3%E6%88%90%E4%B9%9D%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E7%99%BE%E4%BA%8C%E5%8D%81%E4%B8%89%E5%8F%B7;article=7
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** **要介護状態** (*yō-kaigo jōtai*, a state requiring nursing care) is defined as
  "身体上又は精神上の障害があるために、入浴、排せつ、食事等の日常生活における基本的な動作の全部又は一部について、
  厚生労働省令で定める期間にわたり継続して、常時介護を要すると見込まれる状態", classified into grades set by MHLW
  ordinance. **要支援状態** is the parallel definition for a state needing support to prevent
  deterioration. A **要介護者** is a person **aged 65 or over** in a 要介護状態, or a person **aged
  40–64** in that state due to a **特定疾病** attributable to ageing; **要支援者** is the same split
  for 要支援状態 [R42]. **Honest limit:** the article delegates both the **duration** (widely
  stated as six months) and the **grade scale** (要支援1–2 and 要介護1–5) to MHLW ordinance and
  does **not** state either — the six-month period and the seven-grade scale are
  [unverified] against this article, though the seven grades are evidenced empirically by
  the composition table in [R30]. Modelling consequence: a 公的介護保険連動型 benefit trigger is
  defined by reference to this statute plus the grade ordinance, which is exactly why
  nursing_care can be modelled off public 認定率 data [R30] rather than off proprietary
  incidence tables.

---

## 5. Tax and accounting

(jplib-reg-r43)=

### R43 — e-Gov 法令検索, 所得税法 第76条（生命保険料控除）

- **Publisher:** e-Gov 法令検索 — 所得税法, 昭和四十年法律第三十三号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E6%98%AD%E5%92%8C%E5%9B%9B%E5%8D%81%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E4%B8%89%E5%8D%81%E4%B8%89%E5%8F%B7;article=76
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** **生命保険料控除** (*seimei hokenryō kōjo*, the life insurance premium
  deduction) in its post-2012 form: three separate deductions, each computed on the same
  band schedule — **新生命保険料** (第1項), **介護医療保険料** (第2項) and **新個人年金保険料** (第3項).

  | annual premium in the basket | deduction |
  |---|---|
  | ≤ ¥20,000 | the full amount |
  | ¥20,001 – ¥40,000 | ¥20,000 plus 50% of the excess over ¥20,000 |
  | ¥40,001 – ¥80,000 | ¥30,000 plus 25% of the excess over ¥40,000 |
  | > ¥80,000 | **¥40,000** |

  **第4項** caps the sum of the three: "合計額が十二万円を超える場合には、これらの規定にかかわらず、**十二万円**
  とする" — an overall ceiling of **¥120,000** [R43]. Modelling consequence: three baskets of
  ¥40,000, capped at ¥120,000, at national income-tax level. This is the tax structure that
  shapes Japanese product design — it explains why a household holds a 医療保険 *and* a 個人年金
  *and* a 終身保険 rather than one larger contract, and it is the reason the **税制適格特約**
  (*zeisei tekikaku tokuyaku*, tax-qualification rider) exists on 個人年金保険: that rider is
  what puts the premium into the third basket. **Honest limits:** the 税制適格条件 themselves —
  annuitant = policyholder = premium payer, premium-paying period ≥10 years, annuity
  commencement age ≥60, annuity period ≥10 years or for life — sit in **所得税法施行令第211条**,
  which was **not retrieved** and is [unverified]; the parallel **住民税** deduction (a lower
  schedule, ¥28,000 per basket and ¥70,000 overall) is likewise [unverified] here.

(jplib-reg-r44)=

### R44 — e-Gov 法令検索, 相続税法 第12条（死亡保険金の非課税限度額）

- **Publisher:** e-Gov 法令検索 — 相続税法, 昭和二十五年法律第七十三号
- **Doc type:** primary legislation (article)
- **URL:** https://laws.e-gov.go.jp/api/1/articles;lawNum=%E6%98%AD%E5%92%8C%E4%BA%8C%E5%8D%81%E4%BA%94%E5%B9%B4%E6%B3%95%E5%BE%8B%E7%AC%AC%E4%B8%83%E5%8D%81%E4%B8%89%E5%8F%B7;article=12
- **Accessed:** 2026-08-20
- **Retrieved:** yes (e-Gov article API)
- **Annotation:** Among 非課税財産, insurance proceeds received by heirs are exempt up to
  "**五百万円に当該被相続人の第十五条第二項に規定する相続人の数を乗じて算出した金額**" — **¥5,000,000 × the number of
  statutory heirs**. Where the total received by all heirs is within the limit each heir's
  whole amount is exempt; where it exceeds the limit, the exemption is apportioned in the
  ratio of amounts received. An identically structured exemption applies to death retirement
  benefits [R44]. **Honest limit:** the item number within 第12条第1項 was rendered differently
  by the text extractor on different passes — **the formula and its statutory home
  (相続税法第12条) are verified; the item number is not**. [R45] cites 相続税法第3条・第12条・第15条
  without an item number, which is the safer citation form. This is the estate-planning
  demand driver behind 終身保険 in particular, and it is why a whole_life document discusses
  sum-assured selection in multiples of ¥5,000,000 per heir.

(jplib-reg-r45)=

### R45 — 国税庁, タックスアンサー No.4114「相続税の課税対象になる死亡保険金」

- **Publisher:** 国税庁 (National Tax Agency)
- **Doc type:** tax authority guidance
- **URL:** https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4114.htm
- **Accessed:** 2026-08-20
- **Retrieved:** yes
- **Annotation:** The administration's statement of [R44]: "**500万円 × 法定相続人の数 ＝
  非課税限度額**". The exemption applies **only where an heir receives the proceeds** — proceeds
  received by a non-heir get no exemption. The count of 法定相続人 is taken **as if no heir had
  renounced**, with a cap on the number of adopted children. Statutory basis cited on the
  page: **相続税法第3条、第12条、第15条** [R45]. Secondary source — use it for the mechanics and cite
  [R44] for the law.

(jplib-reg-r46)=

### R46 — 国税庁, タックスアンサー No.1755「生命保険契約に係る満期保険金等を受け取ったとき」

- **Publisher:** 国税庁
- **Doc type:** tax authority guidance
- **URL:** https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1755.htm
- **Accessed:** 2026-08-20
- **Retrieved:** yes
- **Annotation:** Where the premium payer and the recipient are the same person, a **lump
  sum** is **一時所得** (*ichiji shotoku*, occasional income) — proceeds received, less premiums
  already paid, less the **¥500,000 特別控除**, of which **half** enters taxable income — while
  an **annuity** is **雑所得** (*zatsu shotoku*, miscellaneous income) — the year's annuity
  less the corresponding premiums, subject in principle to withholding. Statutory basis
  cited: 所法34、35、207、208、209 [R46]. Modelling consequence: the lump-sum versus annuity
  election on a maturing 養老保険 or an individual annuity is a *tax* choice with a real
  behavioural effect on take-up. `jplib` models the contractual cash flows and not the
  policyholder's tax position, but the annuitisation-versus-commutation assumption in
  individual_annuity and endowment should cite this entry as the reason the election is not
  a coin flip.

(jplib-reg-r47)=

### R47 — 金融庁, IFRS 関連情報（the status of IFRS 17 in Japan）

- **Publisher:** 金融庁
- **Doc type:** policy index page
- **URL:** https://www.fsa.go.jp/status/ifrs.html
- **Accessed:** 2026-08-20
- **Retrieved:** yes (index page; the IFRS適用レポート and the adopter list were **not** opened)
- **Annotation:** IFRS applies in Japan as **指定国際会計基準** (designated IFRS) and adoption is
  **任意適用 — voluntary, not mandatory**; the page's own framing is "IFRSの任意適用の積上げ", the
  accumulation of voluntary adopters. It is an index to announcements, Monitoring Board
  activity, the IFRS適用レポート and disclosure examples, and **it carries no current count of
  adopters** [R47]. **The frame a drafter must not import from `uklib` or `uslib`:** Japan
  has **no mandatory IFRS 17**. Named voluntary adopters among insurers, and their
  transition dates, are [unverified] — no adopter list was opened in this session.

### The three measurement bases one projection feeds

Unlike `uklib`, where one accounting standard sits over every product, `jplib` sits under
**three distinct bases**, and a product document that conflates them will be wrong about
which assumptions are fixed and which are re-set.

**J-GAAP statutory reserving.** The statutory accounts every Japanese life insurer must
produce are **J-GAAP** accounts prepared under the 保険業法 and its 施行規則 別紙様式, with 責任準備金 on
the **平準純保険料式** at the 標準利率 and the 標準生命表 [R4] [R7] [R8] [R10] [R18], plus 危険準備金 [R8]
and 価格変動準備金 [R3]. The basis is **ロックイン** — mortality, lapse, incidence and interest fixed
at issue [R15] — and 責任準備金対応債券 are held at amortised cost. Adequacy is tested forward, not
re-measured, through the 1号収支分析 [R22].

**The ESR economic balance sheet.** From 2026-03-31 insurers must also produce an
economic-value balance sheet on which assets are at fair value and liabilities are 現在推計
plus MOCE, re-measured **at each 基準日** on assumptions re-set then, discounted on the
prescribed yield curve [R15] [R16]. This is a *regulatory* measurement, not an accounting
standard — the distinction matters, because the natural `uklib` reflex is to reach for IFRS
17 as the economic frame and in Japan that reflex is wrong.

**IFRS 17, for voluntary adopters only.** IFRS 17 applies to the subset of groups that have
voluntarily adopted 指定国際会計基準 for their consolidated statements [R47].

The **projected per-policy cash flows are common to all three** — the same premiums, claims,
expenses, surrenders and options-and-guarantees streams. What differs is discounting, the
margin (安全割増 inside the standard basis, MOCE under ESR, risk adjustment plus CSM under IFRS
17) and aggregation. That is why `jplib`'s reference implementations keep product cash flows
basis-agnostic and treat discounting, margins and tax as configuration layered on top —
exactly the design `uklib` and `uslib` use, reached here from a different regulatory
starting point.

---

## 6. Gaps, fetch failures and every claim left unverified

Disclosed in full, as the research standard requires. Nothing in this section is a
formality: each item is a place where a product document must tag [unverified] rather than
assert, or must derive a value and tag the derivation **[std]**.

**Not retrieved at all**

1. **平成10年6月8日大蔵省告示第231号** (第三分野 stress test) — [R13]. No copy located on fsa.go.jp or
   on a consolidated mirror. Its stress magnitudes and confidence level are [unverified];
   only its role, quoted from [R14], is established.
2. **平成8年大蔵省告示第50号** (ソルベンシー・マージン比率) — [R17]. Not located. The 200% threshold is
   established indirectly from [R15]'s own statement about the old regime; that the
   calculation basis is 施行規則第86条・第87条 is [unverified].
3. **The ESR 告示 PDFs** (1柱告示 / 3柱告示 / 格付告示, all 2026-03-23) — listed in [R16] but not
   opened. Standard-formula stress magnitudes, correlation matrices and the MOCE formula are
   therefore [unverified] here; [R15] gives the architecture and the 99.5% calibration.
4. **保険業法施行令 and the 内閣府令・財務省令 setting the 90% protection rate** — [R40], [R41]. The
   statutory delegation is verified; the ordinance carrying the number is not.
5. **生命保険契約者保護機構 Q13** (高予定利率契約) — the definition, the 3% 基準利率 and the reduction formula
   are [unverified], taken from a search summary of insurers' disclosure pages.
6. **所得税法施行令第211条** (税制適格特約 conditions) — [R43]. Not retrieved; the four conditions
   commonly stated are [unverified].
7. **住民税 生命保険料控除** band schedule — [unverified]; not retrieved.
8. **標準生命表2018 の作成過程** (`seimeihyo2018-katei.pdf`) — listed on [R21]'s page, not opened.
9. **生命保険文化センター** summary tables giving the **means** of 世帯普通死亡保険金 and 世帯年間払込保険料, and
   the overall 生命保険世帯加入率 — [R32]. Only the banded distributions and the penetration rates
   were read.
10. **e-Stat 利用規約** — [R33]. Reuse licence terms not read.
11. **介護保険事業状況報告 全国版 workbook** (`r05_zenkokukei.xlsx`) — [R30]. Only the ポイント PDF was
    read; the full age × grade grid was not extracted.
12. **保険業法第123条** (基礎書類の変更) — not retrieved; the composite meaning of 基礎書類 is
    [unverified] ([R2]).
13. **The 別紙1–3 PDFs** behind the FX standard-reserve consultation — [R12]. The
    announcement's operative dates were read; the drafting detail was not.

**Retrieved, but from a non-official source**

14. **平成8年大蔵省告示第48号** — [R10]. The consolidated text used is an **individual's mirror
    site**, served over plain HTTP with a self-signed certificate; retrieval required
    `curl -k` with a browser User-Agent and a decode from EUC-JP. Every parameter quoted in
    [R10] was read from that mirror, **not from an FSA-published consolidation**, which
    could not be located. This is the most heavily cited entry in the file and the citation
    weakest in provenance — a product document that leans hard on a specific paragraph of
    告示48号 should say so in the same sentence.

**The single most consequential unresolved number**

15. **The 標準利率 in force at the access date.** [R10] gives the complete reset machinery — the
    基準日 calendar, the yield inputs, the safety-coefficient ladders, the 0.5% / 0.25% / 0.05%
    triggers and the rounding — but not a current value, because the value is derived rather
    than published in the 告示. Searches on fsa.go.jp surfaced no announcement stating the
    current rate, and secondary sources gave conflicting figures. **Any `jplib` document
    stating a current 標準利率 or a market 予定利率 must tag it [unverified], or derive it from JGB
    yields under [R10] and label the derivation [std].** Secondary reporting seen in search
    results — that the 標準利率 moved 2.75% (1996) → 2% (1999-04) → 1.5% (2001-04) → 1%
    (2013-04) → 0.25% (2017-04); that one large carrier raised its 予定利率 in January 2025
    (annuity 0.60% → 1.00%, whole life 0.25% → 0.40%); and that 2026 market 予定利率 on
    single-premium and annuity products sit in the 1.75–2.5% region — is **all
    [unverified]**: none of it came from a retrieved primary document.

**Terminology recorded as practice, not regulation**

16. **三利源 / 死差・利差・費差.** A full-text search of the 500-page 監督指針 本編 [R14] returns **zero**
    occurrences of 利源, 三利源, 死差 and 費差, and 施行規則第30条の2 [R9] expresses the concept only as
    "剰余金の生じた原因に応じて". The three-source framing is Japanese actuarial and industry practice;
    `jplib` may use the vocabulary and **must not** attribute it to a regulatory text.

**Retrieval notes worth carrying into every product research pass**

17. e-Gov statute text is machine-readable only through the **article REST endpoint**
    `https://laws.e-gov.go.jp/api/1/articles;lawNum=<法令番号>;article=<n>`, with the 法令番号 in
    kanji numerals, percent-encoded. The ordinary page URL returns an empty single-page-app
    shell.
18. `fsa.go.jp` PDFs are returned to plain fetchers as an undecoded binary stream. Download
    with `curl` plus a browser User-Agent and extract locally.
19. `mhlw.go.jp` HTML is **CP932** and is garbled by plain fetchers; `curl` plus a local
    decode works.
20. `www.actuaries.jp` serves PDFs only under the `pdf/` path segment — the shorter URL that
    appears in search results returns an HTML error page **with HTTP 200**, which is easy to
    mistake for a successful fetch.
21. The 標準生命表 Excel [R19] stores its sheet and header strings in a mis-declared encoding;
    `openpyxl` returns mojibake for the labels while the **numeric cells are correct**. Read
    the labels from `xl/sharedStrings.xml` directly.

**What is not in scope here, and where it lives instead**

This page carries only the cross-product references. Product-specific regulatory and
actuarial sources — a rider-specific notification, a single product's tax treatment, a
carrier's disclosure of its own 予定利率 — are numbered `R#` inside that product's
`sources.md`, carried verbatim from its `_research/<slug>.md`, and are cited as `[R#]`
rather than `[REG-R#]`. Primary product documentation (約款, ご契約のしおり, パンフレット,
契約締結前交付書面, 重要事項説明書) is never listed here; it is `[S#]` in the product folder, and it is
the only place an individual carrier is identified at all.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-reg-r1
[R10]: #jplib-reg-r10
[R11]: #jplib-reg-r11
[R12]: #jplib-reg-r12
[R13]: #jplib-reg-r13
[R14]: #jplib-reg-r14
[R15]: #jplib-reg-r15
[R16]: #jplib-reg-r16
[R17]: #jplib-reg-r17
[R18]: #jplib-reg-r18
[R19]: #jplib-reg-r19
[R2]: #jplib-reg-r2
[R20]: #jplib-reg-r20
[R21]: #jplib-reg-r21
[R22]: #jplib-reg-r22
[R23]: #jplib-reg-r23
[R24]: #jplib-reg-r24
[R25]: #jplib-reg-r25
[R26]: #jplib-reg-r26
[R27]: #jplib-reg-r27
[R28]: #jplib-reg-r28
[R29]: #jplib-reg-r29
[R3]: #jplib-reg-r3
[R30]: #jplib-reg-r30
[R32]: #jplib-reg-r32
[R33]: #jplib-reg-r33
[R34]: #jplib-reg-r34
[R35]: #jplib-reg-r35
[R36]: #jplib-reg-r36
[R37]: #jplib-reg-r37
[R38]: #jplib-reg-r38
[R39]: #jplib-reg-r39
[R4]: #jplib-reg-r4
[R40]: #jplib-reg-r40
[R41]: #jplib-reg-r41
[R42]: #jplib-reg-r42
[R43]: #jplib-reg-r43
[R44]: #jplib-reg-r44
[R45]: #jplib-reg-r45
[R46]: #jplib-reg-r46
[R47]: #jplib-reg-r47
[R5]: #jplib-reg-r5
[R6]: #jplib-reg-r6
[R7]: #jplib-reg-r7
[R8]: #jplib-reg-r8
[R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
