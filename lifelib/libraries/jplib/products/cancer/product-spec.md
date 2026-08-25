# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*, 約款),
policy booklet (*go-keiyaku no shiori*, ご契約のしおり), contract summary (*keiyaku gaiyō*, 契約概要),
product summary (*shōhin gaiyō*, 商品概要) and product pages) and [R#] (product-specific
regulatory, actuarial and statistical references), both numbered per `_research/cancer.md`
and resolved in `sources.md` (same directory; numbering frozen, never renumbered), and
[REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and the observed range across insurers. Facts the research
file could not verify are flagged [unverified]. The composite is drawn from **seven
carriers**: five life insurers writing a stand-alone cancer main contract on the
fixed-benefit chassis [S1] [S2] [S3] [S5] [S6] [S7] [S8] [S11] [S12], one life insurer
writing a treatment-benefit-only main contract [S10], and one **non-life** insurer writing
the non-reimbursed medicine (*jiyū shinryō*, 自由診療) expense-reimbursement variant [S13].
Two of the cited documents downloaded but could not be read — an image-only 契約概要 [S9] and a
subset-font brochure whose numerals all drop out [S4] — and the facts they would have carried
are named as gaps where they arise.

**Deltas against the medical insurance (*iryō hoken*, 医療保険) chassis.** The
[medical product specification (医療保険)](../medical/product-spec.md) is the `jplib` third-sector
(*dai-san-bun'ya*, 第三分野) chassis: daily amount (*nichigaku*, 日額) times paid days,
capped per hospitalization and again in aggregate, with event benefits layered on. This
product inherits the chassis and changes five things, each of which is a first-order modelling difference and none of which is
cosmetic.

1. **A 90-day waiting period (*menseki kikan*, 免責期間) from attachment of cover (*sekinin
   kaishi*, 責任開始)** before any cancer benefit is payable — and a diagnosis inside it makes the
   whole contract **void**, not merely unpayable. No other product in this library has a
   general waiting period on its main cover.
2. **Cancer diagnosis lump sum (*gan shindan ichijikin*, がん診断一時金) as a repeating lump sum on
   a stated cycle**, not a once-only benefit. The cycle clock is a state variable with
   memory of its own, separate from the 180-day one-hospitalization memory in `medical`.
3. **がん入院給付金 with no day limit at all** — no per-hospitalization day limit (*shiharai gendo
   nissū*, 支払限度日数) and no lifetime aggregate (*tsūsan*, 通算) limit. This is
   the sharpest contrast with `medical`, whose 60/120-day cap and 1,095-day aggregate are
   the defining features of that product's benefit formula, and it removes `medical`'s
   benefit-driven termination decrement entirely.
4. **Carcinoma in situ (*jōhinai shinseibutsu*, 上皮内新生物) paid at a reduced rate**, on a
   separate and separately capped benefit, rather than covered or not covered.
5. **Treatment-based monthly benefits — chemotherapy benefit (*kō-gan-zai chiryō kyūfukin*,
   抗がん剤治療給付金) and radiotherapy benefit (*hōshasen chiryō kyūfukin*, 放射線治療給付金)** —
   which pay per *calendar month in which a qualifying treatment occurred*, not per event
   and not per day. They are increasingly the centre of the product, and on one retrieved
   contract they are the *only* main-contract benefits [S10].

---

## Product overview and market role

Cancer insurance (*gan hoken*, がん保険) is 第三分野 business. The
regulator names it directly: 第三分野 covers 医療保険, **がん保険** and 介護保険, and its benefits are paid
on disease (疾病) or injury (傷害) as 保険金 or 給付金 for treatment [R3]. Because 保険業法 第3条 makes that
class writable under either a life or a non-life licence [REG-R1], the same risk is sold in
two structurally different ways — a point the composite has to take a position on, since one
of the seven carriers here holds a 損害保険業免許 [S13].

**It is the fourth-largest individual line in Japan by policy count in force, and the third
largest by new business count.** At 31 March 2025 ガン保険 stood at **2,522万件** in force, 12.9%
of all 個人保険 policies — behind 医療保険 (23.3%), 終身保険 (19.7%) and 定期保険 (13.9%) — and took
**159万件**, 12.8%, of new business by count, behind only 医療保険 (296万, 23.8%) and 終身保険
(231万, 18.6%) [REG-R31]. Third-sector 年換算保険料 in force was 7兆3,062億円, a series that has risen every
year published [REG-R31]. The line has been open to the whole industry only since the
January 2001 liberalisation; by 平成16年度 third-sector business already exceeded **¥3.5
trillion** of annualised premium and more than **20%** of life insurers' in-force [R3].

Penetration depends sharply on how it is measured, and the two published figures are **not**
comparable. On a 民保加入世帯 base — households already holding private life cover, n = 3,085 —
**68.2%** hold がん保険 or a がん特約 (*tokuyaku*, rider) (60.7% of 世帯主, 46.5% of 配偶者)
[REG-R32]. On the household base
of a different survey covering all providers including JA and 共済, N = 4,837, cancer cover
stands at **39.9%**, and **35.4%** through private life insurers alone, a series with no
consistent trend over time [R10]. Both are quoted here with their bases attached; a model
point should not be justified by silently picking the larger.

**Why it is a mass-market product rather than a niche rider is arithmetic.** Lifetime
incidence probability in Japan is **61.1% for men and 50.1% for women** [REG-R28] — roughly
one person in two will be diagnosed. Registered incidence in 2023 was **993,469** cases
(male 556,059, female 437,406) at a crude rate of 798.92 per 100,000 [R5] [REG-R28]. And the
insurable event is survivable: five-year relative survival for 2018 diagnoses was **63.17%**
for men and **66.84%** for women, all sites [R6]. A benefit menu built around a diagnosis
lump sum and a treatment-linked payment stream, rather than a death benefit, follows
directly from that survival rate.

**The public incidence data is what makes this product modellable, and its shape constrains
the model.** 全国がん登録 publishes counts and rates by 5-year age band, site, sex and diagnosis
year, freely downloadable [R5] [REG-R29] — a citable basis of a kind no UK protection model
has for its morbidity. Age-specific crude rates per 100,000 (2023, both sexes) run 24.38 at
20–24, 220.28 at 40–44, 959.00 at 60–64, 1,948.71 at 70–74 and 2,497.39 at 85–89 [R5]. Two
features of that data are load-bearing. First, **the male and female curves cross**: female
incidence exceeds male from roughly age 25 to roughly age 55 (35–39: female 193.89 against
male 72.92) and is far below it afterwards (70–74: male 2,684.60 against female 1,291.07)
[R5]. A unisex cancer basis is materially wrong at every age. Second, the file publishes
paired rows **with and without 上皮内がん**: 全部位 C00–C96 at 993,469 against 全部位（上皮内がん含む） C00–C96
D00–D09 at **1,114,642** — an in-situ increment of **121,173**, 12.2% of the invasive count
[R5]. The in-situ grading a contract applies can therefore be sourced rather than assumed,
though the increment quoted is an all-ages figure and should not be assumed age-invariant.

**What the inpatient data explains is why the product looks the way it does.** Mean length
of stay for 悪性新生物 discharges was **14.4 days** in September 2023, against **28.4 days** for
all conditions, with only a mild age gradient (35–64: 10.7; 65+: 15.5; 75+: 17.6) [R7]
[REG-R27]. A daily benefit with no day limit is affordable precisely because cancer stays
are short — and, symmetrically, the economic weight of the product has migrated to the
diagnosis and treatment benefits, which do not depend on inpatient days at all. Two of the
seven carriers no longer carry an inpatient benefit in the main contract [S7] [S10]. What is
**not** available is a length-of-stay *distribution*: the finer 患者調査 grids sit on e-Stat
under 統計表 Z124-x and Z134 and were not fetched for this product [R7] [REG-R33], so every
statement below about stay length rests on a mean.

Two structural facts frame everything below. First, the market runs **two incompatible
chassis**: the fixed-benefit (定額給付) chassis, where every benefit is a fixed amount or a
fixed multiple of a base amount, at six of the seven carriers [S1] [S5] [S6] [S7] [S10]
[S11]; and the expense-reimbursement (実損てん補) chassis, where the actual treatment cost is
indemnified including 先進医療 and 自由診療, at the non-life carrier [S13]. Second, within the 定額給付
chassis the design has been moving from **diagnosis-and-hospitalisation centred** [S1] [S5]
[S6] to **treatment centred** [S10] [S11] — on one contract the main contract pays only the
two monthly treatment benefits and everything else is a 特約 [S10]. The
composite specified below sits deliberately between the two, because a reference model that
implements only one cannot express the other.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | がん保険, non-participating, no surrender value (無配当・無解約払戻金型); main contract (*shu-keiyaku*, 主契約) paying diagnosis, inpatient, surgery, treatment and outpatient benefits, with 特約 attached | [S7] [S10] [S11]; menu **[std]** (1) |
| Regulatory class | 第三分野 (保険業法 第3条第4項第2号 ／ 第5項第2号) | [R3] [REG-R1] |
| Chassis | Whole-of-life cover (終身); 10年更新 定期型 as a model-point flag | [S1] [S6] [S10] [S11] vs [S5] [S7] [S13]; **[std]** (1) |
| Issue age (契約年齢) range | 20–75 | observed 0–75 [S15], 18–80 [S12]; **[std]** (2) |
| Age basis | 契約年齢 = age last birthday at the 契約日, incremented at each 年単位の契約応当日 (「24歳7か月の被保険者の契約年齢は24歳」) | [S8] |
| Policy term (保険期間) | 終身 (to the terminal age of the mortality table); no maturity benefit | [S1] [S6] [S10] [S11] |
| Premium-paying period (保険料払込期間) | Pay for life (終身払) default; 65歳払済 短期払 as a variant | [S10] [S12] [S15]; **[std]** (3) |
| Base benefit amount (基本給付金額) | ¥5,000 / ¥10,000 menu; composite default **¥10,000** | [S2] [S3] [S15]; default **[std]** (4) |
| Underwriting | Written declaration (*kokuchi-atsukai*, 告知扱い): the application and the 告知 together are the acts that complete underwriting and start cover [S8], and 復活 needs a fresh 告知 [S1] [S8]. Whether a medical examination is ever required is not stated in any retrieved document | [S1] [S8]; [unverified] on the examination |
| Lives basis | Single life only — no retrieved contract writes a joint life, but none states the restriction either | [S1] [S5] [S6] [S7] [S10] [S11]; observed absence, **[std]** (1) |
| 死亡保険金 in the main contract | None — 「この保険に死亡保険金はありません」 | [S1]; against [S6]; **[std]** (1) |
| Cancer cover start (がん責任開始日) | The 91st day counting the 責任開始日 as day 1 | [S1] [S5] [S6] [S10] [S13]; **[std]** (9) |
| **Anchor model cell** | Male, 契約年齢 40, 終身 chassis, 終身払, 基本給付金額 ¥10,000 — giving がん診断一時金 ¥1,000,000 on a 2-year repeat cycle, がん入院給付金日額 ¥10,000 with no day limit, がん手術給付金 ¥200,000, がん治療給付金 ¥100,000 per treatment month capped at 60 months, がん通院給付金日額 ¥10,000; 上皮内新生物 at 50% of the diagnosis lump sum; がん責任開始日 at day 91; premium waiver on first invasive diagnosis; 先進医療特約 attached; level premium **¥3,000 per month** | **[std]** (5) |

Footnotes to [std] rows:

1. The retrieved contracts fall into three menu shapes and they are not interchangeable:
   diagnosis + inpatient + surgery (+ discharge or outpatient) at three carriers [S1] [S5]
   [S6]; diagnosis + outpatient in the main contract with every treatment benefit in riders
   at a fourth [S7]; and a main contract paying **only** 放射線治療給付金 and 抗がん剤・ホルモン剤治療給付金, with
   hospitalisation, surgery, diagnosis and outpatient all in nine named 特約, at a fifth
   [S10]. A sixth folds surgery, radiation and chemotherapy into a single monthly 治療サポート給付金
   [S11]; the seventh indemnifies actual cost [S13]. The composite main contract carries
   **all five** benefit types on the 定額給付 chassis, each independently switchable, so that a
   model point can be configured into any of the first six shapes. 終身 is the chassis because
   four of the seven write it [S1] [S6] [S10] [S11], against a 10-year renewable term at two
   [S5] [S7] and a 5-year renewable term at the expense carrier [S13]; the 定期 flag carries
   automatic renewal with benefit history, premium-waiver history and 責任開始期 treated as
   continuous across the renewal [S5]. A 死亡保険金 exists on exactly one retrieved contract —
   がん入院給付金日額 times a chosen 倍率, floored at the policy reserve [S6] — and is excluded: it is
   the minority design and it would import a death-benefit reserve into a morbidity product.
2. Observed: 0 (from 15 days old at 告知) to 75 [S15], on a distributor listing because the
   carrier states it only in the unreadable [S4]; 18–80 [S12]; a specimen contract at age 30
   [S5]; not published in the retrieved documents at the other four carriers. The two
   published whole-of-life ranges overlap on 18–75. The composite takes **20–75**: the lower
   bound is raised to 20 because juvenile cancer is a different risk written by one carrier
   only, and the age-specific incidence rate below 20 is an order of magnitude below the
   adult rates (16.51 per 100,000 at 15–19 against 220.28 at 40–44) [R5]; the upper bound is
   the tighter of the two published values.
3. Observed: 60歳／65歳/終身 [S15]; 55/60/65/70歳払済 or 終身払 [S10]; 終身払 only [S12]. 終身払 is the
   default because it is offered everywhere and is the design under which **no surrender
   value ever arises** on any retrieved contract (footnote 22). The 短期払 variant is retained
   because it is the only route by which this chassis acquires a surrender value at all.
4. The benefit schedule is expressed as multiples of a base amount at three carriers —
   基本給付金額 [S2] [S3], がん入院給付金日額 [S6], 特約給付金額 [S7] — and as free-standing yen amounts at the
   rest. The only published course menu is ¥5,000 and ¥10,000, with the ¥5,000 course
   restricted to ages 50–75 [S15]; the ¥10,000 course is the one the carrier's own 契約例 uses
   and the one for which the 100× diagnosis multiple gives the ¥1,000,000 headline [S2]
   [S3]. ¥10,000 is therefore the default: it is the amount at which the published multiples
   and the published headline figure are mutually consistent. It also sits at the bottom of
   the independent ¥1,000,000–¥3,000,000 selectable ladder at another carrier [S12] and
   equals the flat ¥1,000,000 of the expense product [S13].
5. Age 40 male is chosen because it is the age at which the only retrieved premium example
   renews [S5] and because it sits on the steep part of the incidence curve without being in
   the tail (220.28 per 100,000 at 40–44, against 959.00 at 60–64) [R5]. **No carrier
   publishes a rate table for this product** (footnote 7), so the ¥3,000 monthly premium is
   a pure modelling value, not a computed or quoted one. It is anchored as follows: the
   single published price point is a 10-year term at 診断給付金額 ¥2,000,000 and 入院給付金日額 ¥20,000 —
   twice the composite's benefit amounts — costing **¥1,456 per month** at age 30 and
   **¥2,082** on renewal at age 40, on a 2013-10-22 calculation basis [S5]. Halving the
   benefit amounts and repricing a 10-year term as a whole-life-pay 終身 contract with a
   repeating diagnosis benefit, a monthly treatment benefit and an unlimited outpatient
   benefit pushes it back up; ¥3,000 is the round figure in that neighbourhood. It is a
   model-point input in every sense and no result in this library depends on its being a
   market rate.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level for the whole premium-paying period; 無配当 — no dividend, no premium review. On the 定期 flag, recomputed at the renewal-date age | [S5] [S6] [S11]; [REG-R9] |
| Frequency (払込回数) | Monthly (月払) default; 半年払 / 年払 available | [S1] [S6]; one carrier is 月払 only [S11] [S12]; default **[std]** (6) |
| Payment route (払込経路) | 口座振替 / クレジットカード | [S1] [S6] |
| Premium during the waiting period | Payable from 責任開始 — the non-cancer covers are already in force | [S1] [S5] [S6] [S7] [S10]; against [S11]; **[std]** (9) |
| Rating factors | 契約年齢, sex, 基本給付金額, benefits and 特約 elected, 告知 outcome | [S6] [S12]; composite **[std]** (7) |
| Rate structure | Not published by any carrier; the office premium is a model-point input, backed by a **[std]** incidence basis constructed from 全国がん登録 in the technical notes | gap; **[std]** (7) |
| Anchor premium | ¥3,000 per month | **[std]** (5) |
| Premium waiver (保険料払込免除) | On first diagnosis of an 悪性新生物 on or after the がん責任開始日; **上皮内新生物 does not trigger it**; premiums waived for the remaining premium-paying period | [S10] [S11]; **[std]** (8) |

6. 月払 is the dominant retail mode and is the *only* mode at one direct writer [S11] [S12];
   annual and semi-annual exist at two others [S1] [S6]. The composite standardizes on
   monthly — which is also why the model runs on a monthly grid, and why the 90-day waiting
   period lands exactly on a grid boundary (footnote 9).
7. The statement of the method of calculating premiums and policy reserves (*sanshutsu
   hōhō-sho*, 算出方法書) is a 基礎書類 filed with the 金融庁 and is **not published** [REG-R2] — which
   is exactly why every pricing-basis parameter in this library is [std] while every
   contractual parameter carries an [S#] tag. For this product the gap is wider than for a
   death-benefit product, because there is also **no standard incidence table to fall back
   on** for third-sector business [R3] (Regulatory context, below). One premium example was
   retrieved, on a 2013 basis and a different specification [S5]; the carrier's own rate
   table sits only in an unreadable brochure [S4]. Sex is a rating factor by construction,
   given the incidence crossover between ages 25 and 55 [R5], but no retrieved document
   lists the rating factors explicitly and the list above is [unverified] in its detail.
8. **Three distinct waiver triggers are in the market and they are not variants of one
   rule.** (i) *Disability only, cancer excluded*: 高度障害状態 from any cause, or a 身体障害の状態
   arising within 180 days of an 不慮の事故 — and explicitly **not** waived where the 高度障害状態 is
   caused by a cancer diagnosed before the がん責任開始日 [S1], the same two triggers with the
   disease limb restricted to 「がん以外の疾病」 at a second carrier [S6] and again at a third [S5].
   (ii) *Cancer-diagnosis waiver as a rider*: 悪性新生物保険料払込免除特約, on diagnosis of an 悪性新生物 only,
   with 上皮内新生物 expressly **not** triggering it and a pre-責任開始期 diagnosis not triggering it
   either [S10]. (iii) *Cancer-diagnosis waiver built into the contract*, from the moment
   the diagnosis-benefit trigger occurs [S11]. The 契約概要 of a fourth carrier lists **no**
   premium waiver at all [S7] — an observed absence in one document, not a claim about that
   carrier's range. The composite takes (ii)/(iii): a cancer-diagnosis waiver excluding
   in-situ. It is the trigger that actually interacts with this product's benefit model, it
   is the market's direction of travel, and it makes the waiver a *correlated* decrement
   rather than an independent one — which is the modelling point. The disability-only
   trigger is retained as a switch.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Waiting period | 90 days: cover attaches on the **91st day** counting the 責任開始日 as day 1 | [S1] [S5] [S6] [S10] [S13] [R11]; **[std]** (9) |
| Diagnosis inside the waiting period | The **contract is void (無効)**, not merely the claim unpayable; premiums refunded where neither policyholder nor insured knew of the diagnosis before 告知, retained where either knew | [S1] [S5] [S10]; **[std]** (9) |
| Reach of the voidness rule | Not applied where no benefit event occurs within **5 years** of the がん責任開始日 | [S1]; **[std]** (9) |
| Definition of がん | By 約款別表 keyed to ICD codes; 診断確定 by a Japanese-qualified physician or dentist on biopsy (病理組織学的所見), other findings admitted where biopsy is not obtainable | [S1] [S6] [S10] [S11] |
| Date of diagnosis | **The date the diagnostic test was performed**, not the date the result was communicated | [S1] |
| がん診断一時金 | 100 × 基本給付金額 = ¥1,000,000 at the default course | [S2] [S3] [S13]; level **[std]** (11) |
| Repeat cycle | Payable again on 再発 / 転移 / 新たに生じた cancer, at most once in any **2 years**, with **no lifetime cap** | [S5] [S7] [S10]; **[std]** (12) |
| 2-year clock measured from | The date of the **previous payment trigger** | [S5]; **[std]** (13) |
| Continuing hospitalisation at cycle expiry | Still an inpatient on the day after the 2-year period expires ⇒ deemed a fresh trigger | [S1]; **[std]** (13) |
| 上皮内新生物 diagnosis benefit | **50%** of the diagnosis lump sum, payable **once** over the policy term, on a separate cap; not payable after a full-rate cancer benefit has been paid | [S6] [S11]; **[std]** (10) |
| 上皮内新生物 on other benefits | Paid **in full** on the inpatient, surgery, treatment and outpatient benefits; does **not** trigger the premium waiver | [S7] [S10]; **[std]** (10) |
| がん入院給付金 | 入院給付金日額 × 入院日数 for a stay whose direct purpose is cancer treatment — **no per-hospitalization day limit and no 通算 limit** | [S1] [S3] [S5] [S6] [S10] [S13] [R11]; **[std]** (14) |
| Adjacent non-cancer days | Days after a non-cancer illness begins during a covered cancer stay, and days before the diagnosis date in a stay begun for another reason, count into the cancer benefit where the insurer accepts the stay was for cancer treatment | [S6] |
| がん手術給付金 | **20 × 基本給付金額** = ¥200,000; unlimited number of payments; two or more simultaneous procedures count as one | [S2] [S6]; **[std]** (15) |
| がん治療給付金 (monthly) | ¥100,000 (= 10 × 基本給付金額) **per calendar month in which a qualifying chemotherapy, hormone-therapy or radiotherapy treatment occurred**; several treatments in one month pay once; lifetime cap **60 months** | [S5] [S10] [S11]; **[std]** (16) |
| Qualifying treatment definition | Anchored to public classifications, not a clinical list: 総務大臣が定める日本標準商品分類 「8742 腫瘍用薬」 (oral administration excluded) [S1], or drugs scored under 薬剤料 / 処方せん料 in the 医科・歯科診療報酬点数表 [S5] [S10] | [S1] [S5] [S10] |
| Trigger-change clause | The insurer may change the payment triggers prospectively, with 主務官庁 approval, if the public medical insurance scheme changes; two months' notice | [S1] [S5] |
| がん通院給付金 | 通院給付金日額 ¥10,000 per day of outpatient attendance **for** surgery, radiation, thermal therapy or non-oral chemotherapy — treatment-linked, **no day limit and no 通算 limit** | [S1] [S7]; **[std]** (17) |
| Outpatient during a paid stay | Not payable | [S7] [S10] |
| Exclusions (免責事由) | Not extracted for this product line — the exclusion lists sit in the non-extractable 約款 halves | [unverified]; **[std]** (18) |
| Suicide | No death benefit exists in the composite, so the 免責 clause has nothing to bite on | [S1]; [REG-R34]; **[std]** (18) |
| Termination on benefit payment | **None** — payment of the diagnosis lump sum neither terminates the contract nor exhausts it; cover runs to the terminal age | [S1]; against [S11]; **[std]** (12) |

9. **The defining feature of the product, and the one modelling delta that has no analogue
   anywhere else in this library.** Every retrieved cancer contract has a waiting period,
   and it is expressed two ways. Five carriers write **90 days with cover from day 91**:
   「責任開始日を含めて91日目」 [S1], 「保険期間の始期からその日を含めて90日を経過した日の翌日」 [S5], 「責任開始期の属する日からその日を含めて90日目の日の翌日」
   [S6], 「保険期間の始期からその日を含めて91日目」 [S10], and 「90日の待機期間」 with cover from day 91 [S13] — four
   different wordings denoting the same day. Two write **three calendar months**:
   「申込および告知がともに完了した日…から３か月を経過した日の翌日」 [S8] and 「その日を含めて3ヶ月を経過した日の翌日（応当日がない場合はその月の末日）」 [S11].
   生命保険文化センター states 90 days as the market norm [R11]. The composite takes 90 days. On a
   monthly projection grid the two formulations collapse into the same thing — **three
   months of the grid** — and the model must not pretend to a precision it does not have.
   What does *not* collapse is the consequence: the waiting period is not an exclusion but
   an **invalidity rule**, 「保険契約・特約は無効とします」 [S1], 「知、不知にかかわらず、ご契約は無効とします」 [S5], and the same
   at two more carriers [S10] [S6]. One carrier caps its reach at 5 years from the がん責任開始日
   [S1] and the composite adopts that cap, because an uncapped voidness rule is a rescission
   right of indefinite duration and no other retrieved contract states one. Premium
   treatment during the window also differs: five carriers charge from inception, since the
   premium waiver and any non-cancer cover are already running [S1] [S5] [S6] [S7] [S10];
   one **charges nothing at all** during the three months and says explicitly that this is
   not a discount [S11]; the seventh does not state it [S13]. The composite charges, the
   majority position. On reinstatement (*fukkatsu*, 復活) the waiting period **restarts** from
   the 復活日, except that a 復活日 earlier than the original がん責任開始日 leaves the original date
   standing [S1] [S6].
10. **The single largest source of benefit-level variation in the product**, and it splits
    three ways. *Full rate* — in-situ inside the definition of がん — at four carriers:
    「悪性新生物（上皮内新生物を含みます。）」 [S1], 「別表5に定める悪性新生物および上皮内新生物」 [S5], 「ガン（悪性新生物・上皮内新生物）」 [S10], and
    the expense product [S13]. *Half rate*, as a separate benefit, at two: 上皮内がん診断給付金 at
    指定倍率の1/2 [S6] and 上皮内新生物診断一時金 at 50% of the cancer lump sum [S11]. *10%* at one:
    「上皮内新生物の場合：診断給付金額の10％」, applied to both the once-only and the repeating diagnosis
    benefits [S7]. The composite takes **50%** — the median of the three treatments, and the
    design under which the in-situ benefit is a distinct, separately capped benefit whose
    incidence can be sourced from the with/without-上皮内がん rows of the registry [R5] rather
    than folded invisibly into the cancer rate. Two consequential rules come with the
    half-rate design and the composite adopts both: the in-situ benefit is payable **once**
    in its own right, and it is not payable once the full-rate cancer benefit has already
    been triggered [S6] [S11]. Grading is **not** applied uniformly across the menu: the
    10%-grading carrier pays 手術治療給付金, 放射線治療給付金 and 通院給付金 in full for in-situ while excluding
    it entirely from the chemotherapy, non-scheduled-treatment, appearance-care,
    palliative-care and women's-cancer benefits [S7], and in-situ is excluded from the
    premium waiver at another [S10] and from the advanced-medicine benefit at a third [S11].
    The composite grades the diagnosis benefit and the waiver only, and pays every other
    benefit in full.
11. The 100× **multiple** is sourced [S2], as is the resulting ¥1,000,000 at the ¥10,000
    course [S2] [S3]; what is standardized is the **level**, because the market spread is
    wide. The observed points are ¥1,000,000 at the default course [S2] [S3]; a selectable
    ladder of ¥1,000,000–¥3,000,000 in ¥500,000 steps, with ¥500,000 additionally available
    from age 66 [S12]; ¥1,000,000 flat on the expense product [S13]; がん入院給付金日額 × a 給付倍率
    chosen by the policyholder from a range the insurer sets, with the in-situ version at
    half that 倍率 [S6]; and ¥2,000,000 in the one published 契約例 [S5]. ¥1,000,000 is taken
    because it is the bottom of the selectable ladder, the published headline at two
    carriers and the flat value at a third — three of the five points that state one — and
    because at a 2-year repeat cycle with no lifetime cap the *level* is the least
    interesting parameter in the product and should be the one a model point varies first.
12. Observed repeat cycles: **once ever** at three carriers [S1] [S6] [S11]; **2 years** at
    three [S5] [S7] [S10]; **3 years, unlimited**, at the expense carrier [S13]. **No
    retrieved document contains a 1年に1回 cancer diagnosis benefit** — the only annual cycles
    found are on a heart/stroke rider [S7] and on a *survival income* benefit [S11], so a
    one-year cycle is [unverified] and outside the sourced range. The composite takes **2
    years with no lifetime cap**: it is the modal repeating design, it is the shape that
    makes the diagnosis benefit a recurring liability rather than a single event, and a
    model that can express a 2-year cycle can express a once-only one by setting the cycle
    beyond the projection horizon. The once-only designs also differ in what payment *does*:
    at one carrier the A-type contract **terminates** on payment while C/D-type contracts
    instead waive all future premiums [S11]; at another the policy simply continues with the
    other benefits live [S1]. The composite continues and waives (footnote 8) — termination
    on the first diagnosis would delete the treatment, inpatient and outpatient benefits
    precisely when they are incurred. The composite additionally does **not** condition the
    second and later payments on the insured being under treatment: two of the three 2-year
    designs do so, requiring a hospitalisation [S10] or inpatient-or-prescribed-outpatient
    treatment [S7], while the third requires only a fresh 再発／転移／新生 [S5]. The unconditioned
    form is taken as the base and the treatment condition is carried as a switch, because
    the two differ by the whole conditional probability of being in treatment at the cycle
    date.
13. **The 2-year clock is measured from a different event at every carrier that runs one**,
    and a model that treats them as identical is wrong. From the date the previous payment
    trigger occurred [S5]; from the **first day of the calendar month** in which the
    previous payment was made [S7]; from the **start date of the last hospitalisation** for
    which the benefit was paid [S10]. The composite takes the previous trigger date — the
    only one of the three that does not require a second state variable (a payment date, or
    an admission date) to be carried alongside the trigger. The deeming rule that converts a
    continuing hospitalisation at cycle expiry into a fresh trigger [S1] is adopted because
    without it the benefit is unpayable exactly for the insured whose treatment never
    stopped.
14. **No day limit is the invariant of this product**, and it is stated as such by every
    source that speaks to it: 「がん入院給付金は給付日数無制限です」 [S1]; 「支払日数に制限はありません」 [S3]; a limits
    column that states a 支払日数 cap for every *other* benefit and none for this one [S5]; no
    cap in the benefit article [S6] [S10]; unlimited on the expense product [S13]; and, from
    the independent consumer-education source, 「入院給付金の支払日数は無制限です」 stated as the product-type
    norm [R11]. Against `medical`'s 60/120-day per-hospitalization cap and 1,095-day
    aggregate, this removes both limits **and** the benefit-driven termination decrement
    they create — a cancer contract cannot exhaust itself. Two caveats are recorded rather
    than smoothed: at one carrier the absence is read from the 契約概要 limits column and not
    from the benefit article, because the 約款 body did not extract [S5]; and at the two
    treatment-centred carriers there is no inpatient benefit in the main contract to limit,
    it being a rider [S10] or absent [S7]. The composite therefore has **no** `L1` and no
    `LA` on the inpatient limb, and the one-hospitalization test that dominates `medical`
    does not arise at all — a simplification, and the reason a cancer model is not a
    re-parameterization of a medical model.
15. Observed: **20 × 基本給付金額**, unlimited count, simultaneous procedures counted as one [S1]
    [S2]; **がん入院給付金日額 × 20** on the same counting rule [S6]; unlimited count but certain
    procedures (fibrescopic malignant-neoplasm surgery among them) limited to **one payment
    per 60 days**, with some procedures outside cover altogether [S5]; 手術治療給付金 at the rider
    amount, limited to **once per 14 days** for a 一連の手術 [S7]; and per-surgery payment with
    fee-schedule de-duplication, where a repeated identical procedure scored once in the
    schedule pays once [S10]. The composite takes 20× with no count limit, the value two
    carriers publish at the composite's own base amount [S2] [S6]; the 14-day and 60-day
    re-payment bars are carried as switches, since they bind only on repeated procedures and
    the retrieved documents do not agree on which procedures they apply to.
16. **This is the benefit the market has moved to, and the one whose unit of payment is
    easiest to get wrong: it is a *month*, not an event and not a day.** Observed: 治療給付金額
    per month in which the trigger occurs, lifetime cap **60 months** [S5]; 特約給付金額 × a 倍率 of
    1 for hormone therapy in breast or prostate cancer and 2 otherwise, with a **combined
    lifetime cap of 120×** across chemotherapy and hormone therapy, counted across renewals
    [S7]; 給付月額 per qualifying month, where a prescription covering two months still pays one
    month and two triggers on one day pay once [S10]; and ¥100,000 per treatment month, or
    ¥50,000 for a month of hormone therapy only, the hormone-only months capped at **60
    months** [S11]. The composite takes **¥100,000 per qualifying month with a 60-month
    lifetime cap**. ¥100,000 is the only published monthly amount [S11] and equals 10 × the
    composite's base amount. 60 months is chosen because it is the only absolute cap two
    carriers state in months [S5] [S11] and because the third carrier's 120× cap is
    exhausted by **60 qualifying months at 倍率 2** — the non-hormone case [S7] — so the same
    number is the effective ceiling under two of the three designs. Radiotherapy is folded
    into the same monthly benefit rather than paid separately: two carriers pay it that way
    [S10] [S11], against a per-treatment payment limited to once per 60 days at a third
    [S7]. Folding it in is what makes the benefit a single monthly indicator variable, which
    is the whole computational advantage of the design; the separate per-treatment form is a
    switch. The 倍率-1 hormone-only reduction is not adopted, because only one carrier grades
    that way in months [S11] and one in 倍率 [S7], and averaging a 50% amount reduction with a
    50% multiplier reduction would produce a figure neither carrier writes.
17. Two structurally different outpatient designs coexist, and one carrier runs both at
    once. *Treatment-linked, no day limit* — attendance **for** surgery, radiation, thermal
    therapy or non-oral chemotherapy, with 「給付の日数の限度はありません」 [S1] and 支払日数は無制限 with no 通算
    limit at all [S7]. *Hospitalisation-linked and day-limited* — attendance in a window
    around an inpatient stay: 60 days before admission and 180 days after discharge, capped
    at **45 days per hospitalisation** and **730 days lifetime** [S5]; 60 days before
    admission and 365 days after discharge, capped at **120 days per post-discharge period**
    [S10]; a 通院治療期間 of one year from discharge capped at **60 days** [S1] [S2]; a 通院期間 of
    365 days from a defined start date with unlimited days inside it [S7]. The composite
    takes the treatment-linked, unlimited-day form: it is the design that does not require
    the inpatient-stay state the composite has otherwise discarded (footnote 14), and it is
    the form two carriers write [S1] [S7]. Where a carrier runs both, the tie-break is
    contractual and specified — a day qualifying under both is paid as the
    hospitalisation-linked one until that limit is exhausted, then as the treatment-linked
    one [S1]; the composite has one stream and no tie-break.
18. **An honest gap.** The 免責事由 lists sit in the 約款 halves that did not extract at both
    carriers whose booklets were retrieved in full form [S1] [S5], and no other retrieved
    document reproduces them. They are therefore [unverified] for this product line, and the
    composite carries **no** exclusion set beyond the waiting-period invalidity rule and the
    non-disclosure remedy. The one exclusion whose absence is *not* a gap is suicide: 保険法
    第51条 carries no statutory time limit and a 免責期間 is purely contractual [REG-R34], but the
    composite has no death benefit, so the clause has nothing to attach to. It becomes live
    only if the 死亡保険金 design of the minority carrier [S6] is switched on.

### Options — 特約 and 特則

| Parameter | Representative value | Basis |
|---|---|---|
| がん先進医療特約 | The 技術料 of a 厚生労働大臣-designated 先進医療 reimbursed in full, lifetime aggregate **¥20,000,000**; the rider terminates on reaching the cap | [S1] [S7] [S11]; **[std]** (19) |
| 先進医療 cash top-up | **10%** of the 先進医療給付金, capped at ¥500,000 per 療養 | [S1]; **[std]** (19) |
| 患者申出療養 | Excluded from the composite's advanced-medicine benefit | [S11] vs [S7]; **[std]** (19) |
| がん退院一時金 | 10 × 基本給付金額 = ¥100,000 on discharge from a covered stay of **10 or more consecutive days**; unlimited count, but not payable for a stay beginning **within 30 days** of a discharge already paid; on discharge by death the policyholder becomes the payee | [S1] [S2]; **[std]** (20) |
| がん収入サポート給付金 | **50%** of the diagnosis lump sum on each policy anniversary after the diagnosis year while the insured is alive, up to **5 payments**; stops on death | [S11]; scope **[std]** (21) |
| 特定保険外診療給付金 | Out of scope | [S7]; scope **[std]** (21) |
| 緩和療養給付金, 外見ケア給付金, 女性がん特約, がんゲノムプロファイリング検査給付金, がん要精検後精密検査給付金 | Out of scope | [S7] [S11]; scope **[std]** (21) |
| Expense-reimbursement (実損てん補) chassis | Out of scope | [S13]; scope **[std]** (21) |

19. The **¥20,000,000 lifetime cap is uniform** at every carrier that publishes one for a
    current product [S1] [S7] [S11] — as it is on the `medical` chassis — against
    ¥10,000,000 on the 2013-edition contract [S5], which is the same parameter at an earlier
    vintage rather than a genuine alternative. Reaching the cap extinguishes the rider [S1].
    The cash top-up is not uniform: 10% of the benefit capped at ¥500,000 per 療養 [S1]
    against **¥150,000 per 療養, once per policy year** [S7]. The composite takes the former,
    which is the form that scales with the underlying claim. 患者申出療養 is expressly
    **excluded** at one carrier [S11] and expressly **included** at another [S7]; the
    composite excludes it, matching the `medical` chassis so that the two products'
    advanced-medicine streams are configured identically.
20. The discharge lump sum is specified at exactly one carrier in the retrieved set [S1]
    [S2] and is retained because its shape — a lump sum conditioned on stay length, with a
    30-day re-payment bar — is the one benefit in this product that reads *back* onto the
    length-of-stay distribution, and 平均在院日数 for 悪性新生物 is 14.4 days [R7] [REG-R27], close
    enough to the 10-day threshold that the benefit's value is sensitive to the distribution
    rather than to its mean. It is off in the base run.
21. Out-of-scope items are named rather than dropped, because each is a real benefit some
    insured actually holds. The income-style benefit [S11] is the closest thing in the
    market to a cancer income stream and would be modelled as an annuity-certain contingent
    on survival, which is the `income_guarantee` machinery, not this product's; 特定保険外診療給付金 —
    per qualifying month for treatment at a がん診療連携拠点病院等 by a procedure *not* in the public
    fee schedule, once per month, **12 payments lifetime** — is the 定額給付 chassis's answer to
    自由診療 [S7] and is the point at which the two market chassis meet, but it needs a
    non-scheduled-treatment incidence basis that no retrieved source supplies. The expense
    chassis [S13] is out of scope entirely: indemnifying actual cost, with ガン入院保険金
    unlimited, ガン外来保険金 capped at ¥20,000,000 **resetting at each 5-year renewal**, and a
    ¥1,000,000 diagnosis benefit on a 3-year cycle, it is a different model — severity
    distributions of cost rather than fixed amounts — and it is written under a non-life
    licence [REG-R1].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value (*kaiyaku-henreikin*, 解約返戻金) | **None**, at any duration, under 終身払 | [S7] [S10] [S11]; **[std]** (22) |
| Policyholder dividend (配当金) | None — 無配当; no 満期保険金 | [S5] [S6] [S11]; [REG-R9] |
| 契約者貸付 / 自動振替貸付 | Neither offered — there is no surrender value to lend against, so a missed premium lapses the policy | [S1] [S7] [S10] [S11]; **[std]** (22) |
| Rider values | Riders carry no surrender value at any point | [S1] [S5] |
| Grace (払込猶予期間), 月払 | From the first day of the month following the 払込期月 to the **last day of that month** | [S1] [S6] [S8]; **[std]** (23) |
| 払込猶予期間, 半年払・年払 | From the first day of the following month to the 月単位の契約応当日 in the month after that, with the stated month-end and February/June/November extensions | [S1] [S6] |
| Claims during grace | Unpaid premium deducted from the benefit; for a monthly contract where the event falls on or after the contract anniversary inside the window, **two months'** premium is deducted; if the benefit cannot cover the arrears the contract lapses at the end of grace | [S1] [S6] |
| Lapse (失効) | From the day after the grace period expires | [S1] [S6] [S11] |
| Reinstatement (復活) | Within **1 year** of 失効, on payment of arrears and fresh 告知; may be refused on health grounds; **the waiting period restarts from the 復活日** | [S1] [S8]; **[std]** (24) |
| First-premium failure | The contract is **void (無効)**, not lapsed | [S1] [S8] |
| Non-disclosure (告知義務違反) | Rescission within **2 years** of the 責任開始日, 復活日 or 特約中途付加日; 詐欺 and unlawful-purpose voidness are **not** time-barred | [S1] [S6]; ceiling [REG-R35] |
| Benefit reduction (減額) | Available where premiums become unaffordable, subject to an insurer-set minimum; increases require a new contract with fresh underwriting; where the daily amount is reduced mid-stay the benefit is computed at the amount in force **on each day** | [S1] [S6] [S12] |
| クーリング・オフ | 15 days [S1] / 8 days [S11] from the application date; out of scope | [REG-R36]; scope **[std]** (25) |
| Death of the insured | Cover terminates; no death benefit in the composite | [S1] |

22. **Four positions on surrender value, and the spread is the widest structural variation
    in the product.** *None at all* — 無解約払戻金型 — at three carriers [S7] [S10] [S11] and on
    the riders of every contract examined [S1] [S5]. *Suppressed then a fixed step*: no
    value ever under 終身払, and under a 短期払 no value during the premium-paying period and **10
    × 基本給付金額** afterwards, which — since the product pays no death benefit — is also what is
    returned on death after the premium term [S1]; or no value during the premium-paying
    period and afterwards the **lesser of** 30% of the unsuppressed value and the **greater
    of** 入院給付金日額 × 10 and 診断給付金額 ÷ 10 [S5]. *Conventional value throughout*, computed from
    months paid and months elapsed, at exactly one carrier [S6] — and it is the only
    retrieved cancer contract carrying the full savings machinery: 契約者貸付, **自動振替貸付 at ≤ 8%
    p.a.** compounded into principal at each anniversary and continuing until principal plus
    interest would exceed the surrender value, with one month's notice before the 失効予定日 and
    retrospective cancellation if surrender or 払済 is requested within 3 months of grace
    expiry, and **払済保険への変更** setting a paid-up がん入院給付金日額 from the surrender value capped at
    the pre-conversion 日額 [S6]. The composite takes **no surrender value**: three carriers
    write the contract that way outright and a fourth gives zero under the 終身払 default, so
    it is the majority position at the composite's own specification. The consequence is the
    one to carry into the model — **the lapse decrement has no cash-value offset and there
    is no 自動振替貸付 to delay it.** A lapse is a pure release of future premium and future
    benefit, and a missed premium lapses the policy at the end of grace. On the one contract
    with a value, a model that lapses immediately is wrong, because the APL carries the
    policy; that is a switch, not the base.
23. Three carriers state the same one-month monthly grace [S1] [S6] [S8]; one direct writer
    runs **two months** — 「払込期月の翌月初日から翌々月末日まで」 [S11]. The composite takes one month, the
    majority and the same value as the `medical` chassis. The first-premium rule is
    separately defined and materially different in *kind*: the payment period runs from the
    責任開始日 to the end of the following month, then grace to the end of the month after that,
    and failure makes the contract **void, not lapsed** [S1] [S8] — so a first-premium
    failure produces no in-force policy at all rather than a lapse decrement.
24. Three regimes, and they decide whether lapse is absorbing. **1 year** from 失効 with fresh
    告知 [S1] [S8], with one of those carriers additionally refusing reinstatement outright
    once any cancer benefit has been paid and after a surrender request [S1]; **3 years**,
    with 延滞保険料 payable and no new policy document issued [S6]; and **none at all** —
    「失効した保険契約を元の状態に戻すこと（復活）はできません」 [S11]. The composite takes 1 year, the modal published
    window and the same as `medical`. What makes reinstatement more than a persistency
    detail on *this* product is that **the waiting period re-runs**: がん責任開始日 becomes the
    復活日, unless the 復活日 precedes the original date [S1] [S6]. A reinstated cancer policy is
    therefore not the policy that lapsed — it is a policy with 90 days of no cover in front
    of it, which is a real anti-selection control and a real modelling state.
25. 保険業法 第309条 sets an eight-day window from the later of delivery of the disclosure
    document and the application date, effective on **dispatch** [REG-R36]; one carrier
    contracts for 15 days with a full refund and no interest [S1], another for the statutory
    8 [S11]. `jplib` models from the point cover is in force and scopes the window out — it
    is a pre-inception decrement and modelling it would need a new-business funnel this
    library does not have.

---

## Contractual mechanics

### The waiting period, and why it is not an exclusion

Write `d0` for the 責任開始日. Cancer cover attaches on

    がん責任開始日 = d0 + 90 days       (i.e. the 91st day counting d0 as day 1)

and on a monthly grid, with `t` in months from issue, that is the boundary `t = 3`
**[std]**. Nothing turns on the 90-day/3-month distinction at monthly resolution, and the
model does not claim otherwise; the two contractual wordings [S1] [S11] are recorded in
footnote 9 so that a daily implementation can separate them.

The rule that matters is what happens to a diagnosis *inside* the window. It does not simply
go unpaid: the contract is **void** [S1] [S5] [S10], premiums are refunded where neither
party knew of the diagnosis before 告知 and retained where either did [S1], and — under the
composite — the treatment is not applied at all if no benefit event occurs within 5 years of
the がん責任開始日 [S1]. For a projection this is a **de-recognition, not a decrement**: the policy
was never in force, so it releases premium already collected as well as future benefit, and
it belongs in a validity adjustment at outset rather than in the lapse column. The diagnosis
date that tests it is the date the **diagnostic test was performed**, not the date the
physician communicated the result [S1] — a distinction that also moves a diagnosis across a
repeat-cycle boundary.

On 復活 the clock restarts from the 復活日 unless the 復活日 falls before the original がん責任開始日 [S1]
[S6].

### The diagnosis benefit and its cycle

Let `A` be the 基本給付金額 (¥10,000 at the anchor cell), `DB = 100 × A` the diagnosis lump sum,
and `T_last` the date of the most recent payment trigger. The benefit is payable when

    the insured is first diagnosed with an 悪性新生物 on or after がん責任開始日     [first payment]
    or 再発 / 転移 / 新たに生じた cancer is diagnosed and  now - T_last >= 2 years   [repeat]

with no limit on the number of payments [S5]. `T_last` is set to the trigger date, not the
payment date [S5], and if the insured is still an inpatient on the day after the two-year
period expires, that day is **deemed** a fresh trigger [S1].

For 上皮内新生物 the benefit is `0.50 × DB`, payable **once** over the policy term, on its own
cap, and not payable once a full-rate cancer benefit has been paid [S6] [S11]. In-situ pays
in full on every other benefit and does not trigger the premium waiver [S7] [S10].

The cycle is a state variable with its own memory, and it is *not* the 180-day
one-hospitalization memory of the `medical` chassis: it is keyed to a diagnosis event, it
runs for two years rather than 180 days, and it is unaffected by admissions and discharges
except through the deeming rule. A model that reuses one clock for both is wrong.

### The inpatient benefit — no limits

    hosp_benefit(i) = D * stay_days(i)

for every stay `i` whose direct purpose is cancer treatment, with `D` the がん入院給付金日額 [S1]
[S5] [S6] [S10]. There is no `L1` and no `LA` [S1] [S3] [R11]. Days adjacent to the cancer
treatment count in where the insurer accepts the stay was for that purpose — days after a
non-cancer illness begins during a covered stay, and days before the diagnosis date in a
stay begun for another reason [S6].

Two consequences follow and both are deltas against `medical`. The 180-day
one-hospitalization test does not arise, so successive admissions need no grouping logic.
And **the contract cannot exhaust itself**: `medical`'s benefit-driven termination
decrement, which fires when both aggregate limbs are used up, has no analogue here. Cover
runs to the terminal age of the mortality table, and the only decrements are death, lapse
and — on the waiting-period rule — invalidity.

### Surgery, and the monthly treatment benefit

    surg_benefit  = 20 * A         per surgery, unlimited count,
                                   simultaneous procedures counted as one   [S2] [S6]

    treat_benefit(m) = 10 * A      for each calendar month m in which at least one
                                   qualifying chemotherapy, hormone-therapy or
                                   radiotherapy treatment occurred,
                                   subject to  sum over m of 1  <=  60 months

The monthly benefit's unit of payment is the **calendar month**, and every retrieved
contract that writes one says so in a different way that means the same thing: a
prescription covering two months still pays one month, two triggers in one month pay once,
two triggers on one day pay once [S10]; several treatments in a month pay once [S11]. The
60-month lifetime cap is [std] (footnote 16). On a monthly projection grid the benefit is
therefore an **indicator variable per period**, not a count and not a duration — which is
why the treatment-centred design is computationally simpler than the inpatient one, and why
the market moved to it.

The covered set is defined by reference to public classifications rather than a private list
of named drugs — 日本標準商品分類 「8742 腫瘍用薬」 with oral administration excluded [S1], or whatever
attracts a 薬剤料 or 処方せん料 under the 医科・歯科診療報酬点数表 [S5] [S10]. As on the `medical` chassis, that
makes the trigger enumerable from a public document, and every such contract carries a
clause letting the insurer change the 支払事由 prospectively, with 主務官庁 approval and two months'
notice, if the public scheme changes [S1] [S5].

### The outpatient benefit

    outp_benefit = D * days of attendance FOR surgery, radiation, thermal therapy
                     or non-oral chemotherapy,      no day limit, no 通算 limit   [S1] [S7]

The trigger is the treatment, not proximity to a hospital stay, so the benefit needs no
admission or discharge date. A day of attendance during a stay for which the inpatient
benefit is paid is not payable [S7] [S10].

### 先進医療

    adv_paid(k)   = min( tech_fee(k), 20,000,000 - adv_paid_cumulative )
    adv_top_up(k) = min( 0.10 * adv_paid(k), 500,000 )

and the rider terminates when the cumulative amount reaches ¥20,000,000 [S1] [S7] [S11].
患者申出療養 is excluded [S11].

### Premium waiver

The composite waiver fires on the **first diagnosis of an 悪性新生物 on or after the がん責任開始日**,
and 上皮内新生物 does not fire it [S10] [S11]. Premiums cease for the remaining premium-paying
period; on the 終身払 anchor cell that is the rest of the projection.

This is a *correlated* decrement, and that is the modelling point. Unlike the
disability-triggered waiver of the `medical` chassis — an event essentially independent of
the insured benefits — this waiver is triggered by the **same event** that starts the
diagnosis benefit, the treatment benefit and, usually, an inpatient stay. Every cancer claim
in the model that fires the diagnosis benefit for the first time must also stop the premium
stream. The disability-only trigger observed at three carriers [S1] [S5] [S6] is retained as
a switch, and one carrier's 特定障害不担保特約, which carves designated 視力障害 or 聴力障害 out of waiver
eligibility at underwriting [S1], is out of scope.

### Grace, lapse and reinstatement

For a 月払 contract, grace runs from the first day of the month following the 払込期月 to the last
day of that month [S1] [S6] [S8]. A claim arising inside the window is paid net of the
unpaid premium, and where the event falls on or after the contract anniversary inside the
window **two months'** premium is deducted [S1]; if the benefit cannot cover the arrears the
contract lapses at the end of grace [S6]. 失効 runs from the day after grace expires.

**There is nothing to break the fall.** On a product with a 解約返戻金 the insurer would advance
the premium under 自動振替貸付, an election the 監督指針 requires be at the policyholder's choice and
notified promptly [REG-R14]; the composite has no surrender value, so neither 契約者貸付 nor
自動振替貸付 can operate [S1] [S7] [S10] [S11]. The lapse is real and immediate — the same
position as the `medical` chassis, and the opposite of `jplib`'s savings chassis. On the one
retrieved cancer contract that does carry a value, the APL runs at **≤ 8% p.a.** compounded
annually until principal plus interest would exceed the surrender value [S6], and a model
that lapses that contract on a missed premium is wrong.

復活 within one year restores cover from the 復活日 on payment of arrears and fresh 告知 [S1] [S8],
and the waiting period re-runs (above). One carrier refuses reinstatement outright once any
cancer benefit has been paid [S1] — a control with no analogue on the `medical` chassis, and
one that makes the reinstatement option conditional on the claim history the model is
already carrying.

---

## Riders and options

**In scope (modeled or parameterized):**

- **がん診断一時金 repeat cycle** — 2 years, unconditioned, no lifetime cap; the under-treatment
  condition [S7] and the hospitalisation condition [S10] are switches, and a once-only
  design is the same cycle set beyond the horizon [S1] [S6] [S11].
- **上皮内新生物 grading** — 50% of the diagnosis benefit, once, separately capped [S6] [S11]; the
  full-rate [S1] [S5] [S10] and 10% [S7] treatments are switches on the same parameter.
- **がん治療給付金 (monthly)** — ¥100,000 per qualifying month, 60-month lifetime cap; the
  radiotherapy limb is folded in [S10] [S11], and paying it separately per treatment on a
  60-day lockout [S7] is a switch.
- **がん通院給付金** — treatment-linked, unlimited days [S1] [S7]; the hospitalisation-linked,
  day-limited designs [S5] [S10] are switches.
- **がん先進医療特約** — a reimbursement stream with a ¥20,000,000 lifetime cap and a 10% capped
  top-up, the rider terminating on the cap [S1] [S7] [S11]. Switchable off.
- **がん退院一時金** — ¥100,000 on discharge from a stay of 10+ days, with the 30-day re-payment
  bar [S1] [S2]. Off in the base run.
- **保険料払込免除** — cancer-diagnosis trigger excluding in-situ [S10] [S11]; the disability-only
  trigger [S1] [S5] [S6] is a switch.
- **10年更新 定期 chassis flag** — automatic renewal with benefit history, waiver history and
  責任開始期 continuous across the renewal, and an option exercisable at least 2 months before
  maturity to convert to 終身 [S5] [S7].

**Out of scope:** the 実損てん補 expense chassis and its 自由診療 cover [S13]; 特定保険外診療給付金 [S7];
がん収入サポート給付金 [S11]; 緩和療養給付金 (24-month [S7] and 12-month [S10] caps); 外見ケア給付金 [S7]; 女性がん特約 and
女性手術給付金 [S7] [S11]; がんゲノムプロファイリング検査給付金 and がん要精検後精密検査給付金 [S7]; the 悪性新生物 death benefit
floored at the policy reserve [S6]; 払済保険への変更, 契約者貸付 and 自動振替貸付 [S6]; the 特定障害不担保特約
underwriting carve-out [S1]; 重大疾病一時金特約 (heart and stroke, not cancer) [S7]; 減額 and 中途付加
alterations [S1] [S12]; and クーリング・オフ [REG-R36].

---

## Variations across insurers

1. **Chassis and benefit menu.** Diagnosis + inpatient + surgery at three carriers [S1] [S5]
   [S6]; diagnosis + outpatient with treatment benefits in riders at a fourth [S7]; a
   **treatment-only main contract** with nine riders at a fifth [S10]; diagnosis + a single
   monthly treatment benefit at a sixth [S11]; expense reimbursement at the seventh [S13].
   Composite: all five 定額給付 benefit types in one main contract, independently switchable, so
   that any of the first six shapes is a configuration (footnote 1).
2. **Waiting period wording.** 90 days with cover from day 91 at five carriers [S1] [S5]
   [S6] [S10] [S13]; **three calendar months** at two [S8] [S11]. Composite: 90 days, which
   on a monthly grid is three months either way (footnote 9).
3. **Premium during the waiting period.** Payable at five carriers [S1] [S5] [S6] [S7]
   [S10]; **not charged at all** at one, which says explicitly that this is not a discount
   [S11]; not stated at the seventh [S13]. Composite: payable.
4. **上皮内新生物.** Full rate at four [S1] [S5] [S10] [S13]; **half rate** on a separate benefit
   at two [S6] [S11]; **10%** at one [S7]. Composite: 50% on the diagnosis benefit, full
   elsewhere, no waiver trigger — the median treatment, and the one whose incidence is
   separately sourceable from the registry's with/without-上皮内がん rows [R5] (footnote 10).
5. **Diagnosis-benefit repeat cycle.** Once ever at three [S1] [S6] [S11]; 2 years at three
   [S5] [S7] [S10]; 3 years at one [S13]. **No retrieved contract writes a 1-year cycle**
   [unverified]. Composite: 2 years, no lifetime cap (footnote 12).
6. **What the 2-year clock runs from.** The previous trigger date [S5]; the **first of the
   month** of the previous payment [S7]; the **start date of the last hospitalisation**
   [S10]. Composite: the trigger date — the only one needing no second date carried
   alongside it (footnote 13).
7. **Condition on the second and later diagnosis payments.** None [S5]; being under
   inpatient or prescribed outpatient treatment [S7]; a **hospitalisation** for cancer
   treatment [S10]. Composite: none, with the condition as a switch. The two differ by the
   whole conditional probability of being in treatment at the cycle date.
8. **Chemotherapy and radiotherapy benefit.** Monthly with a **60-month** cap [S5]; monthly
   at 倍率 1 or 2 with a **combined 120×** cap counted across renewals [S7]; monthly in the
   main contract, uncapped [S10]; ¥100,000 per month with ¥50,000 for hormone-only months
   capped at 60 months [S11]. Radiotherapy sits inside the same monthly benefit at two
   carriers [S10] [S11] but is paid separately per treatment, once per 60 days, at a third
   [S7]. Composite: ¥100,000 per qualifying month, 60-month cap, radiotherapy folded in
   (footnote 16).
9. **Surgery limits.** Unlimited count [S1] [S2] [S6]; unlimited but **1 per 60 days** for
   named procedures [S5]; **1 per 14 days** for a 一連の手術 [S7]; fee-schedule de-duplication
   [S10]. Composite: unlimited at 20 × the base amount, with the re-payment bars as
   switches.
10. **Outpatient benefit.** Treatment-linked with no day limit at two [S1] [S7];
    hospitalisation-linked and day-limited at three, on caps of 45 days per stay and 730
    lifetime [S5], 120 days per post-discharge period [S10], and 60 days per 通院治療期間 [S1].
    Composite: treatment-linked, unlimited (footnote 17).
11. **Premium waiver trigger.** Disability only at three [S1] [S5] [S6]; **cancer
    diagnosis** as a rider excluding in-situ at one [S10]; **cancer diagnosis** built into
    the contract at one [S11]; **none stated** in the 契約概要 of a sixth [S7]. Composite:
    cancer diagnosis excluding in-situ — the correlated trigger (footnote 8).
12. **Surrender value and 自動振替貸付.** None at three [S7] [S10] [S11]; none under 終身払 with 10 ×
    the base amount after a completed 短期払 at one [S1]; a two-part formula after the premium
    term at another [S5]; and a **conventional value throughout with APL at ≤ 8% p.a., 契約者貸付
    and 払済保険への変更** at exactly one [S6]. Composite: none — so the lapse decrement has no
    cash-value offset and nothing delays it (footnote 22).
13. **復活.** 1 year at two [S1] [S8], one of which also bars it once any cancer benefit has
    been paid [S1]; 3 years at one [S6]; **none at all** at one [S11]. Composite: 1 year. It
    decides whether lapse is absorbing, and on this product it also re-runs the 90-day
    waiting period (footnote 24).
14. **Grace, monthly.** One month at three [S1] [S6] [S8]; **two months** at one [S11].
    Composite: one month. クーリング・オフ likewise differs — 15 days [S1] against the statutory 8
    [S11] [REG-R36] — and is out of scope either way.
15. **Death benefit.** Stated absent in terms at one carrier — 「この保険に死亡保険金はありません」 [S1] — and
    not found in any other retrieved contract except one, where it is がん入院給付金日額 × a chosen
    倍率 **floored at the policy reserve** [S6]. Composite: absent.
16. **What does not vary.** Every retrieved contract (i) has a waiting period before cancer
    cover starts and treats a diagnosis inside it as **voiding the contract** rather than
    merely excluding the claim [S1] [S5] [S6] [S10] [S13]; (ii) dates the diagnosis to the
    **examination**, not the consultation [S1]; (iii) requires 診断確定 by a Japanese-qualified
    physician or dentist on histopathological findings [S1] [S6] [S10] [S11]; (iv) pays the
    inpatient benefit with **no day limit** wherever it has one at all [S1] [S3] [S5] [S6]
    [S10] [S13] [R11]; (v) counts two simultaneous surgeries as one [S1] [S6] [S10]; (vi)
    defines the treatment benefits by reference to a **public classification** and carries a
    clause allowing the 支払事由 to be changed prospectively, with regulatory approval, if the
    public medical insurance scheme changes [S1] [S5] [S10]; and (vii) is **無配当** wherever
    the dividend basis is stated [S5] [S6] [S11]. These are the invariant core of the
    composite, and (i), (iv) and (vi) are exactly the three facts a reader coming from the
    [medical product specification (医療保険)](../medical/product-spec.md) must not carry over
    unchanged.

---

## Regulatory context

**Classification.** がん保険 is named by the regulator as one of the three 第三分野 lines, alongside
医療保険 and 介護保険 [R3], writable under either a 生命保険業免許 or a 損害保険業免許 by 保険業法 第3条第4項第2号 and
第5項第2号 [REG-R1]. That is not a formality here: six of the seven carriers in this composite
hold a life licence and the seventh, writing the same risk as an expense indemnity, holds a
non-life one [S13].

**Prudential — and the fact that shapes this whole document.** The FSA says of 第三分野 business
that 「標準死亡率、参考純率といったスタンダードな指標が存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 [R3]. **There is
no standard cancer-incidence table and no reference pure premium.** Every insurer's incidence
rate (*kiken hasseiritsu*, 危険発生率) is its own, sits in the unpublished 算出方法書 [REG-R2],
and is set from public data plus that insurer's experience. What the regulator supplies
instead of a table is a **test**: annual 事後検証 of the assumed incidence rates; a **ストレステスト**
each reporting period over a **10-year** horizon comparing future benefit outgo on the
pricing rate `P` against outgo on 危険発生率A, covering **99%** of incidence risk, and 危険発生率B,
covering **97.7%**, with contingency reserve (*kiken junbikin*, 危険準備金) established where `P`
falls short; and a **負債十分性テスト** [R3]. The 監督指針 requires the calculation be performed under
平成10年6月8日大蔵省告示第231号 [R4] [REG-R13], with the tests run in principle **per 契約区分 sharing a
common 基礎率** under 保険業法施行規則 第69条 [R4] [REG-R8]. The reserve itself is the standard policy
reserve (*hyōjun sekinin-junbikin*, 標準責任準備金) chain: 保険業法 第116条 requires the reserve and
delegates the method [REG-R4], 施行規則 第68条 says which contracts are in scope [REG-R7], and
平成8年大蔵省告示第48号 sets 平準純保険料式 with the table vintages and the standard valuation interest rate
(*hyōjun riritsu*, 標準利率) reset machinery [R4] [REG-R10]. `jplib` implements the
**sensitivity** — a re-runnable incidence basis — and **not** the statutory stress, whose
own notification text was not retrieved [REG-R13]; the 99% / 97.7% levels quoted above come
from the FSA policy paper [R3], not from the 告示.

**The mortality basis, by contrast, is prescribed and public.** For contracts written from
April 2018 the third-sector valuation mortality is **第三分野標準生命表2018** [R1] [R2] [REG-R11]
[REG-R18], published in full and freely downloadable — the sharpest contrast with `uklib`,
where the CMI tables cannot be read at all without a subscription. It is deliberately the
**lighter** table: male q(30) is 0.00041 against 0.00068 on 生保標準生命表2018（死亡保険用）, and male
q(90) 0.11657 against 0.15760 [REG-R18]. That is the correct direction of conservatism for a
morbidity product — survival prolongs benefit payment, so death *releases* the liability —
and it is precisely why a best-estimate cancer model must not adopt the valuation table as its
mortality decrement without a stated [std] adjustment. The table is not best estimate in any
case: built on the 国民表 (第21回生命表, 2010), improved forward at 2.5% p.a. for five years then
1.0% for three, then loaded by a 数学的危険論 margin sized to hold adverse deviation to about
**2.28% (2σ)** on an assumed 1,000,000 lives per sex, floored at 70% and capped at 85% of
the unadjusted rate, and constructed on a nearest-birthday age (*hoken-nenrei*, 保険年齢) basis
while the contracts age on attained age with the fraction discarded (*man-nenrei*, 満年齢) [R2]
[REG-R20]. **`jplib` cites these tables and does not ship them**: the 日本アクチュアリー会's site
terms prohibit reproduction and transmission without written consent [REG-R21], so the
model's mortality input is a [std] construction whose `provenance` column points at the IAJ
entries [REG-R18] [REG-R19], and the cancer-incidence input is a [std] table built from
全国がん登録 downloads carrying the attribution string those datasets require [R5] [REG-R29]. The
IAJ acts as 指定法人 in this chain under 保険業法 第122条の2 [REG-R23].

**Prudential — solvency.** From **31 March 2026** insurers are supervised on the
economic-value **ESR** (経済価値ベースのソルベンシー規制), a three-pillar regime valuing liabilities at 現在推計
plus MOCE, re-measured at each 基準日 on assumptions re-set then, with required capital
calibrated at **99.5%** and early corrective action below an ESR of **100%** [REG-R15]. It
supersedes the ソルベンシー・マージン比率 trigger at **200%** [REG-R17], and the two are not comparable.
`jplib` computes neither. What it owes both regimes is that its projections are re-runnable
on a re-set assumption basis at a stated 基準日 — which, for a third-sector product, is exactly
the capability the ストレステスト demands of the insurer anyway.

**Conduct.** 監督指針 II-4-2-2 fixes what the 契約締結前交付書面 must contain — 商品の仕組み, 保障の内容 with the
main 支払事由 and 免責事由, 付加できる主な特約, 保険期間, 引受条件, 保険料, 配当金に関する事項 and 解約返戻金等の水準 in the 契約概要; and
クーリング・オフ, 告知義務, 責任開始期, the main non-payment cases and 保険料の払込猶予期間・契約の失効・復活 in the 注意喚起情報
[REG-R14]. That list is, item for item, the source set this specification is built from.
クーリング・オフ is the eight-day dispatch-rule right of 保険業法 第309条 [REG-R36], contracted wider at
one carrier [S1] and scoped out here. Non-disclosure remedies run under 保険法 第55条, whose
ceiling is five years from inception with a one-month clock from discovery [REG-R35]; the
two-year contractual windows observed [S1] [S6] narrow that in the policyholder's favour and
are permitted. On insurer failure, contracts are compensated up to **90% of the 責任準備金** at
the failure date through the 生命保険契約者保護機構 [REG-R40], the rate set by ordinance under 保険業法
第270条の3 [REG-R41]; one carrier's booklet adds that the 基礎率 (予定利率, *yotei riritsu*, the
assumed interest rate; 予定死亡率; 予定事業費率) may be changed on transfer and an 早期解約控除 may
apply [S1].

**Tax.** A がん保険 premium falls in the **介護医療保険料控除** basket of the post-2012 three-basket
生命保険料控除, which covers contracts concluded on or after 2012-01-01 paying on 疾病 or 身体の傷害 under
医療費支払事由 [R8]. The income-tax deduction is the full premium up to ¥20,000; premium × 1/2 +
¥10,000 to ¥40,000; premium × 1/4 + ¥20,000 to ¥80,000; and a flat **¥40,000** above —
capped at ¥40,000 per basket and **¥120,000** overall [R9] [REG-R43]. The anchor cell pays
¥36,000 a year, sitting in the second band for a deduction of ¥28,000 = ¥36,000 × 1/2 +
¥10,000: real, and second-order. The 住民税 caps are not stated on the 国税庁 pages retrieved and
are [unverified] [R9]. On the benefit side, one carrier states that its cancer treatment,
first-diagnosis, inpatient, surgery, discharge, advanced-medicine and outpatient benefits
are **in principle non-taxable** where the payee is the insured, a spouse, a lineal relative
or a 生計を一にする親族 [S1]. Benefits are not modelled net of policyholder tax.

**Professional standards.** Every life insurer appoints an appointed actuary (*hoken
keirinin*, 保険計理人) under 保険業法 第120条 [REG-R5], who confirms at each 決算期 whether the 責任準備金 is
accumulated on sound actuarial principles and submits an 意見書 under 第121条 [REG-R6]. The
日本アクチュアリー会 実務基準 turns that into the **1号収支分析** — a forward income-and-outgo analysis over
「少なくとも将来10年間」 by 区分経理 segment, with sufficiency judged over the first five years [REG-R22] —
which is the same ten-year horizon the third-sector ストレステスト uses [R3], and the shape these
projections take. Statutory reserving under J-GAAP, the ESR economic balance sheet and IFRS
17, which is voluntary in Japan [REG-R47], are three measurement bases fed by one set of
projected cash flows, which is why this library keeps product cash flows basis-agnostic.
This chassis is 無配当, so the surplus-distribution methods of 施行規則 第30条の2 [REG-R9] and the 三利源
framing that goes with them do not apply to it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-cancer-r1
[R10]: #jplib-cancer-r10
[R11]: #jplib-cancer-r11
[R2]: #jplib-cancer-r2
[R3]: #jplib-cancer-r3
[R4]: #jplib-cancer-r4
[R5]: #jplib-cancer-r5
[R6]: #jplib-cancer-r6
[R7]: #jplib-cancer-r7
[R8]: #jplib-cancer-r8
[R9]: #jplib-cancer-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R13]: #jplib-reg-r13
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R23]: #jplib-reg-r23
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
[REG-R29]: #jplib-reg-r29
[REG-R31]: #jplib-reg-r31
[REG-R32]: #jplib-reg-r32
[REG-R33]: #jplib-reg-r33
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R47]: #jplib-reg-r47
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
