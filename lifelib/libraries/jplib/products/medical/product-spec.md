# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*, 約款),
policy booklet (*go-keiyaku no shiori*, ご契約のしおり), pre-contract disclosure (*keiyaku
teiketsu-mae kōfu shomen*, 契約締結前交付書面), statement of material matters (*jūyō jikō
setsumeisho*, 重要事項説明書) and product pages) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/medical.md` and resolved in `sources.md` (same
directory; numbering frozen, never renumbered), and [REG-R#] (the cross-product reference
library `references/regulatory-and-actuarial-references.md`, whose own R-numbering is
distinct) — were extracted from the cited document. Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row carries a
numbered footnote giving the rationale and the observed range across insurers. Facts the
research file could not verify are flagged [unverified]. The composite is drawn from five
carriers' current retail medical products: one carrier's whole-of-life (*shūshin*, 終身)
chassis with a lifestyle-disease limit relaxation [S1] [S2] [S3]; a second carrier's 終身
chassis with a severe-surgery tier, plus its rider booklet [S4] [S5]; a third carrier's
paired 終身 and term (*teiki*, 定期) products, with the only complete published premium scale
found [S6] [S7] [S8]; a fourth carrier's three-型 chassis [S9]; and a fifth carrier's
ten-year renewable 定期型 [S10]. Two further carriers' documents downloaded but could not be
text-extracted, and the facts attributed to them are [unverified] [S11] [S12].

**This is the `jplib` third-sector chassis.**
[cancer (がん保険)](../cancer/product-spec.md) and [nursing care (介護保険)](../nursing_care/product-spec.md) state
their deltas against this document rather than restating the machinery. The benefit structure specified
here is **frequency × severity × limit** — a daily amount multiplied by paid days, capped
per hospitalization and again in aggregate, with event benefits layered on top — not a sum
assured. Every downstream document should treat that as the defining structural fact.

---

## Product overview and market role

Medical insurance (*iryō hoken*, 医療保険) is third-sector (*dai-san-bun'ya*, **第三分野**)
business. Insurance Business Act (*Hoken-gyō-hō*, 保険業法) 第3条第4項第2号 lists, among the
business a life licence (生命保険業免許) covers, insurance paying a fixed sum or indemnifying loss
on a person contracting a disease (人が疾病にかかったこと), a state of the person caused by injury or
disease (傷害を受けたこと又は疾病にかかったことを原因とする人の状態) and receiving treatment for
either (治療を受けたこと); 第3条第5項第2号 makes the identical class available under a
non-life licence (損害保険業免許) [R1] [REG-R1]. Writable under either licence, it is named
separately — and the separation is not cosmetic: the reserving rules and the standard
valuation table differ by 分野 [REG-R8] [REG-R10] [REG-R13].

**It is the largest individual line in Japan by policy count.** At 31 March 2025, 医療保険
stood at 4,545万件 in force — 23.3% of all 個人保険 policies, ahead of 終身保険 (19.7%), 定期保険
(13.9%) and ガン保険 (12.9%) — and took 23.8% of new business by count [REG-R31]. The picture
inverts on sum insured, where 定期保険 holds 38.6% and a 医療保険 has no sum assured to report at
all. Third-sector 年換算保険料 in force was 7兆3,062億円, a series that has risen every year
published. In FY2024 the industry paid hospitalization benefit (*nyūin kyūfukin*, 入院給付金) on
800万件 of claims totalling 7,598億円 and surgery benefit (*shujutsu kyūfukin*, 手術給付金) on
561万件 totalling 4,900億円 [REG-R31] — mean claims of roughly ¥95,000 and ¥87,000, the order of
magnitude this specification has to reproduce. Household penetration is near-saturation:
95.1% of insured households hold a 医療保険 or a medical rider (*iryō tokuyaku*, 医療特約)
[REG-R32], and 65.6% of individuals hold cover paying 疾病入院給付金, at an average enrolled daily
amount of **¥8,500** against a self-assessed need of ¥10,100 [R12].

**The public morbidity data is the sharp contrast with
[uklib](../../../uklib/index.md).** Where a UK protection model must proxy restricted CMI
tables, a Japanese medical model can be calibrated from
厚生労働省 statistics anyone can download. Patient Survey (*kanja chōsa*, 患者調査), a 基幹統計, gives
hospitalization treatment-receiving rate (*nyūin juryō-ritsu*, 入院受療率) per 100,000
population — national **945** in October 2023, rising from 137 at ages 20–24 to 2,952 at
80–84 and 6,275 at 90 and over [R6] [REG-R26] — and average length of stay (*heikin zaiin
nissū*, 退院患者平均在院日数), national **28.4 days**, down from 40.8 in 平成8年 and 32.8 in 平成23年
[R6] [REG-R27]. The same survey publishes the length-of-stay distribution in **32 bands** by
five-year age band and by cause, its cumulative form, and 推計退院患者数 by
過去の入院の有無・再入院までの期間 — respectively what a 60-day cap, a per-cause severity split and the
180-day re-admission rule each need, all as downloadable CSV [R7] [REG-R33]; 医療給付実態調査 adds
a claims-cost cross-check from the public schemes' own records [R13]. What is **not** public
is any morbidity table: 日本アクチュアリー会 publishes the mortality basis only — free, in full, and
machine-readable [R4] [REG-R18] [REG-R19] — and every insurer's incidence rate (*kiken
hasseiritsu*, 危険発生率) is its own.

Two structural facts shape everything below. First, the main contract is non-participating,
without surrender value (*mu-haitō*, *mu-kaiyaku-henreikin-gata*, **無配当・無解約返戻金型**). The
no-surrender-value half is in the formal product name at four of the five carriers [S2]
[S4] [S6] [S9]; the 無配当 half is in the formal name at three [S2] [S6] [S7] and stated in
terms at two [S1] [S6]. There is no savings element, no dividend, and — decisively —
**no 自動振替貸付** (*jidō furikae
kashitsuke*, automatic premium loan), because there is no surrender value to lend against;
one carrier says so in terms [S1]. A medical policy really does lapse when a premium is
missed, which is where this chassis parts company with the
[whole life savings chassis (終身保険)](../whole_life/product-spec.md). Second,
the policy is main contract (*shu-keiyaku*, 主契約) plus riders (*tokuyaku*, 特約) and special
provisions elected at issue (*tokusoku*, 特則), and much of the economics lives in the
riders — the advanced-medicine rider (*senshin iryō tokuyaku*, 先進医療特約) costs about 2% of the
premium [S9] and buys a ¥20,000,000 lifetime cap.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 医療保険, 無配当・無解約返戻金型; 主契約 paying 疾病入院給付金, 災害入院給付金 and 手術給付金, with 特約 attached | [S1] [S2] [S4] [S6] [S9] [S10] |
| Regulatory class | 第三分野 (保険業法 第3条第4項第2号 / 第5項第2号) | [R1] [REG-R1] |
| Chassis | Whole-of-life cover (終身), whole-of-life or short premium term; 10年更新 定期型 as a model-point flag | [S1] [S6] [S9] vs [S7] [S10]; **[std]** (1) |
| Issue age (契約年齢) range | 20–80 | observed range; **[std]** (2) |
| Age basis | Attained age at 契約日 with the fraction discarded (*man-nenrei*, 満年齢), incremented at each 年単位の契約応当日 | [S4] [S10] |
| Policy term (保険期間) | 終身 (to the terminal age of the mortality table) | [S1] [S6] [S9] |
| Premium-paying period (保険料払込期間) | Pay for life (終身払) default; 65歳払済 短期払 variant | [S1] [S6]; **[std]** (3) |
| Daily hospitalization amount (入院給付金日額) menu | ¥3,000 / ¥5,000 / ¥8,000 / ¥10,000 / ¥12,000 / ¥15,000; composite default **¥5,000** | menu [S6]; default **[std]** (4) |
| Underwriting | Written declaration (*kokuchi-atsukai*, 告知扱い), no medical examination in the direct channels; 告知受領権 rests with the company | [S1] [S6] [S10] |
| Lives basis | Single life only | [S1] [S4] [S6] [S9] [S10] |
| 死亡保険金 in the main contract | None | [S1] [S4] [S6] [S9] [S10] |
| **Anchor model cell** | Male, 契約年齢 40, 終身 chassis, 入院給付金日額 ¥5,000, 60日型 per-hospitalization limit, 通算1,095日, 終身払, level premium ¥2,100 per month, 手術給付金 20倍/5倍, 先進医療特約 attached, five-day minimum payment off | **[std]** (5) |

Footnotes to [std] rows:

1. Three carriers write 終身 only [S1] [S4] [S9]; one writes 終身 and 定期 as separate products
   [S6] [S7]; one writes only a 医療保険（定期型）, ten-year renewable to age 80 with a contractual
   conversion into a 終身医療保険 at a term end [S10]. The composite takes 終身 — the majority
   design, and the one that exercises the lifetime aggregate limit, which a ten-year term
   does not. The 定期 chassis is retained as a model-point flag: cover renews automatically at
   the renewal-date age and rate scale, and the 通算 aggregate limit and the 先進医療 cap run
   **across renewals** [S7] [S10].
2. Observed: 0–80 [S3]; 18–80 終身 and 18–70 定期 [S6] [S7]; 20–69 [S10]; not published in the
   retrieved booklets at two carriers [S4] [S9] [unverified]. The composite takes 20–80 —
   the two published whole-of-life ranges, with the lower bound raised to 20 because
   juvenile morbidity is a different risk and only one carrier writes it [S3].
3. Observed: 終身 / 60歳まで / 65歳まで [S6]; 終身払 with a 短期払 option [S1]; 全期払（終身）versus
   短期払 distinguished by a payment-period-completion death benefit [S9]. 終身払 is the default
   because it is offered everywhere and is the design under which no surrender value ever
   arises; the 65歳払済 variant is retained because it is the only route by which this chassis
   acquires a surrender value at all (footnote 22).
4. Only one carrier publishes the full menu [S6]. Illustrated contracts use ¥10,000 [S1]
   [S9]; both published premium tables are quoted on ¥5,000 [S3] [S8]; the market average
   enrolled amount is ¥8,500 [R12]. ¥5,000 is the default because it is the amount for which
   public rates exist, so the anchor cell's premium and benefit are consistent with each
   other; ¥10,000 is the standard model-point variant.
5. Age 40 male is the age both published scales quote and the age of one specimen contract
   [S3] [S8] [S9]. The ¥2,100 monthly premium sits between the two published specimen rates
   for a ¥5,000 daily amount at that age on a whole-life-pay 終身 chassis: ¥2,121 on one
   carrier's エコノミーコース, which is 60日 only [S6] [S7] [S8], and ¥2,080 for a 60日型 with the
   三大疾病無制限型 relaxation and 先進医療特約(2018) attached [S3]. Whether the first quotation includes
   a 先進医療特約 is not stated in the retrieved page [unverified], so the two are not a clean
   rider-on/rider-off pair. No carrier publishes a rate table by age and duration, so
   the office premium is a model-point input, not a computed quantity (footnote 7).

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level for the whole premium-paying period, 無配当 — no dividend, no premium review; on the 定期 flag, recomputed at each renewal | [S3] [S6] [S8] for 終身; [S7] [S10] for 定期 |
| Frequency (払込回数) | Monthly (月払) default; 半年払 / 年払 available | [S1] [S4]; default **[std]** (6) |
| Payment route (払込経路) | 口座振替 / クレジットカード / 団体扱 / 振込 | [S1] [S4] |
| Advance payment (前納) | 月払 contracts may prepay 6 or 12 months at a company-set discount; not modeled | [S4]; scope **[std]** (6) |
| Rating factors | 契約年齢, sex, 入院給付金日額, 支払限度の型, riders and 特則 elected, 告知 outcome; one carrier discloses that it also prices 受療率 by prefecture of residence, taken from 患者調査 | [S6]; composite **[std]** (7) |
| Rate structure | Not published by any carrier; the office premium is a model-point input, backed by a **[std]** morbidity basis constructed from 患者調査 in the technical notes | gap; **[std]** (7) |
| Anchor premium | ¥2,100 per month | **[std]** (5) |
| Waiver of premium (保険料払込免除) | Disability-triggered: severe disability (*kōdo shōgai jōtai*, 高度障害状態) from any cause, or a listed 身体障害の状態 arising from an accident (不慮の事故) within 180 days of it; available only during the premium-paying period | [S1] [S2] [S9] [S10] |

6. Monthly is the dominant retail mode and one net-direct product is 月払 only as at its
   2024年4月 edition [S10]; the composite standardizes on monthly (which is also why the model
   runs on a monthly grid) and treats 前納 discounting [S4] as an immaterial modal refinement.
7. The statement of the method of calculating premiums and policy reserves (*sanshutsu
   hōhō-sho*, 算出方法書) is a 基礎書類 filed with the 金融庁 and is **not published** [REG-R2] — which
   is precisely why every pricing-basis parameter in this library is [std] while every
   contractual parameter carries an [S#] tag. Two carriers publish specimen scales by age
   and sex on a fixed specification [S3] [S8] and one publishes a single specimen contract
   with its rider split out [S9]; that is the complete set of public rates found. Both
   scales show a **sex crossover between ages 30 and 40** — female premiums exceed male at
   20 and 30 and fall below from 40 onward [S3] [S8]. That is a real morbidity feature
   (childbirth-related and gynaecological admissions at younger ages), not a pricing
   artefact, and any [std] morbidity basis must reproduce it.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Disease hospitalization benefit (疾病入院給付金) | 入院給付金日額 × 入院日数 per hospitalization | [S1] [S2] [S6] [S9] [S10] |
| Accident hospitalization benefit (災害入院給付金) | Same daily amount; admission must begin within 180 days of the accident | [S1] [S4] [S9] [S10] |
| Concurrency | 疾病入院給付金 and 災害入院給付金 are never paid for the same day; where 災害 is running and a disease is diagnosed mid-stay, 疾病 begins the day after the 災害 period ends | [S1] [S2] [S4] [S9] [S10] |
| Same-day admission (日帰り入院) | Covered — the 支払事由 is one day or more of 入院 | [S3] [S6] [S9] |
| Five-day minimum payment | Switch, **off** in the composite base; when on, a stay of 5 days or fewer pays 日額 × 5 | [S4] [S6] [S7] have it, [S1] [S2] [S9] [S10] do not; **[std]** (8) |
| Per-hospitalization day limit (1入院の支払限度日数) | **60日型** default; 120日型 switch | [S1] [S4] [S9]; **[std]** (9) |
| One-hospitalization test | Two or more admissions are one hospitalization where the causes are the same or medically related; a new hospitalization begins on the **181st day** counting from the day after the previous discharge | [S1] [S2] [S6] [S7] [S10]; **[std]** (10) |
| Aggregate day limit (通算支払限度日数) | **1,095日**, applied separately to the 疾病 and 災害 limbs; 1,000日 switch; on the 定期 flag it runs across renewals | [S4] [S6] [S7] [S10] vs [S1] [S9]; **[std]** (11) |
| Surgery benefit (手術給付金) | 入院給付金日額 × **20** for surgery during a paid hospitalization, × **5** otherwise; unlimited in count | [S1] [S3]; **[std]** (12) |
| Surgery trigger | Procedures chargeable under 手術料 in the public health system's medical fee schedule (*ika shinryō hōshū tensū-hyō*, 医科診療報酬点数表), plus 放射線治療料-listed procedures, plus 骨髄移植術 chargeable under 輸血料, plus procedures qualifying as 先進医療 | [S1] [S2] [S4] [S9] [S10] |
| Surgery exclusions | The seven-item list: 傷の処理; 切開術（皮膚、鼓膜）; 骨・関節の非観血的整復術等; 抜歯; 異物除去（外耳、鼻腔内）; 鼻焼灼術; 魚の目・タコ切除術 | [S2] [S4] [S6] [S10] |
| Surgery frequency limits | One surgery per day (the highest-paying); a per-day-charged 手術料 pays the first day only; 放射線照射 and 温熱療法 pay at most once in 60 days | [S1] [S2] [S9] [S10] |
| Surgery during a stay whose day limit is exhausted | Paid, at the in-hospital multiple | [S4] vs [S10]; **[std]** (13) |
| Radiation therapy benefit (放射線治療給付金) | Folded into 手術給付金 through the 放射線治療料 limb of the trigger, at most once per 60 days | [S1] [S2] [S6] [S10]; **[std]** (14) |
| Outpatient benefit (通院給付金) | Not in the composite main contract | [S1] [S5]; **[std]** (15) |
| Bone-marrow harvesting (骨髄幹細胞の採取術) | Covered only from one year after the date cover attaches (*sekinin kaishi-bi*, 責任開始日); 自家移植 excluded | [S1] [S2] [S6] [S9] [S10] |
| Pre-inception disease and injury | Not covered — only disease arising, and accidents occurring, on or after 責任開始時 | [S1] [S2] [S9] [S10] vs [S4]; **[std]** (16) |
| Exclusions (免責事由) | 故意 or 重大な過失 of the policyholder or insured; the insured's criminal act; an accident caused by 精神障害 or 泥酔; unlicensed driving; drink-driving; 薬物依存; 頚部症候群（むちうち症）or 腰痛 with no objective findings, whatever the cause; 地震・噴火・津波; 戦争その他の変乱 | [S4], matched on substance by [S1] [S5] [S10] |
| Catastrophe proportionality | Where an earthquake, eruption, tsunami or war raises claims but its effect on the pricing basis is small, the insurer may pay in full or reduce the benefit in proportion | [S4] |
| Suicide | Nothing is paid where the insured takes their own life within **3 years** of 責任開始日 | [S1]; statutory frame [REG-R34] |
| Termination on exhausting the limits | Cover ceases where both the 疾病 and 災害 aggregate limits are reached | [S9]; **[std]** (17) |

8. Two of the five carriers guarantee a five-day minimum — 「入院1回につき、入院給付金日額×入院日数
   ただし、入院日数が5日以内の場合は、入院給付金日額×5」 on both the 疾病 and 災害 limbs [S4], with an
   identical rule at another carrier, which states that it covers 日帰り入院 [S6] [S7]. The other
   three pay actual days with no minimum [S1] [S2] [S9] [S10]. This is a first-order model
   choice, not a detail: against a national mean stay of 28.4 days the floor is invisible,
   but against the 2.4-day mean stay for 白内障 it roughly doubles the payment [R6]. The
   composite takes the majority position as the base and carries the floor as a switch,
   because the two cannot be averaged.
9. Observed menus: 60日型 / 120日型 [S1] [S4]; 60日 only [S6] [S7] [S10]; 60日型 / 120日型 /
   730日型 [S9]; 40日 / 60日 / 120日 [S11] [unverified]. 60日 is the only value every carrier
   offers and the sole option at three, so it is the default and 120日 the switch. The 型 is
   elected at issue and can never be changed [S4] [S9], so it is a model-point attribute,
   not a state variable.
10. Three carriers use a same-cause-or-medically-related test [S1] [S2] [S6] [S7] [S10] and
    two aggregate regardless of cause [S4] [S9]. The boundary arithmetic differs in wording
    only: 「the 181st day counting from the day after the last discharge inclusive」 [S1] [S2]
    against 「after 180 days have elapsed from the day after the last discharge」 [S4] resolve
    to the same date, and writing it out once stops an implementation gaining or losing a
    day. The composite takes the majority cause test and the 181st-day reset. Riders may use
    a **different** test: one carrier's 入院一時金特約 and 通院治療支援特約 aggregate cause-blind while
    its main contract does not [S1].
11. Observed: 1,095日 [S4] [S6] [S7] [S10]; 1,000日 [S1] [S2] [S9]; 1,000日 [S11] [unverified].
    The composite takes the four-carrier majority, with 1,000 as a switch. Applying the cap
    separately to the two limbs is the disclosed treatment at two carriers — at 1,095 [S4]
    and at 1,000 [S1] — and is what the composite implements. One carrier converts 一時金
    benefits into days against the limits (10 days for a short-stay lump sum, 20 for a
    hospitalization lump sum, whatever the days actually spent) [S9]; the composite does not
    adopt that.
12. Four structures are in the market and they are not interchangeable: 20倍 in hospital / 5倍
    outpatient, unlimited count [S1] [S3]; 10倍 / 5倍 [S6] [S7]; 10倍 / 5倍 with a **40倍 重大手術**
    tier on an enumerated list of open cranial, thoracic and abdominal procedures for
    malignancy, major cardiovascular procedures and transplants under the 臓器移植法 [S4]; flat
    **10倍, in-hospital only**, outpatient surgery not covered at all [S10]; plus, as a
    separate rider on its own 手術給付金基準額 set independently of the 日額, 20倍 (Ⅰ型) or 10倍 (Ⅱ型) in
    hospital and 5倍 outpatient [S9]; 40/20/10/5倍 [S11] [unverified]. The composite takes
    20倍/5倍 — the richest two-tier form, and the one for which a published premium exists at
    the composite's own specification [S3]; the 10倍/5倍 and flat-10倍 forms are switches, the
    latter because it removes the in-hospital/outpatient distinction entirely.
13. A **genuine contradiction between carriers**, not a gap: where surgery is performed
    during a stay for which 入院給付金 is no longer payable because the per-hospitalization limit
    is exhausted, one carrier treats it as in-hospital and pays the higher multiple [S4] and
    another pays nothing at all [S10]. The composite pays at the in-hospital multiple, the
    only positively stated treatment among the retrieved 約款, and carries the alternative as
    a switch. The two positions differ by the whole surgery benefit on exactly the long
    stays where the day limit bites.
14. One carrier pays a **separate** 放射線治療給付金 of 日額 × 10 for procedures listed under
    放射線治療料, including 電磁波温熱療法 and excluding 血液照射 [S4]; a second pays radiation inside
    its surgery rider at 20倍/10倍 [S9]; three fold it into 手術給付金 through the 放射線治療料 limb of
    the trigger [S1] [S2] [S6] [S10]. The composite folds it in and applies the 60-day
    lockout every carrier imposes in one wording or another [S1] [S2] [S6] [S9] [S10]. For
    the model that means radiation is not a separate claim stream in the base run; it is
    surgery-benefit frequency.
15. No general 通院給付金 exists on this chassis at the composite's carriers. One sells a
    通院治療支援特約（退院時一時金給付型）paying a lump sum on surviving discharge from a paid admission,
    once per discharge, 通算50回 [S1]; another sells a general 通院特約 in its rider booklet [S5].
    The composite leaves outpatient benefits out of the main contract and out of the base
    run, so that [cancer (がん保険)](../cancer/product-spec.md) introduces a 通院 benefit as its own
    delta rather than inheriting an unused one.
16. The base rule everywhere is that only post-責任開始時 disease and accidents are covered
    [S1] [S2] [S9] [S10]. One carrier softens it twice: a pre-inception condition **is**
    covered if the admission or procedure begins more than **two years** after 責任開始日, and is
    paid in full where the insured had never consulted a doctor about it and had never been
    flagged at a health check [S4]. No equivalent appears in the other four sets of
    conditions, so the composite takes the strict rule; the softening is named because it is
    a material anti-selection difference, not a drafting nicety.
17. One carrier states it directly: if, during the premium-paying period, both the 疾病入院給付金等
    and the 災害入院給付金等 aggregate limits are reached, 保険契約は消滅します [S9]; another terminates
    dependent riders on the same event [S1]. The composite terminates the contract when both
    limbs are exhausted. This gives the model a **benefit-driven termination decrement**
    that a death-benefit product does not have, and is why the aggregate limit must be a
    tracked state variable rather than a cap applied at the end.

### Options — 特約 and 特則

| Parameter | Representative value | Basis |
|---|---|---|
| 先進医療特約 | Reimburses in full the technique fee (技術料) of a 厚生労働大臣-designated 先進医療, which sits entirely outside the public scheme; lifetime aggregate **¥20,000,000**; the rider terminates on reaching the cap | [S1] [S3] [S5] [S6] [S7] [S9] |
| 先進医療 cash top-up | 10% of the 先進医療給付金, capped at ¥500,000 per 療養 | [S1]; **[std]** (18) |
| 先進医療 unit of claim | A series of treatments under the same 先進医療 counts as one 療養; cover is tested at the treatment date, so a technology that has left the 先進医療 list pays nothing; 患者申出療養 is excluded | [S1] [S5] [S6] [S9] |
| 先進医療特約 term | Attached for the life of the main contract | [S1] [S5] vs [S9]; **[std]** (18) |
| Hospitalization lump-sum rider (入院一時金特約) | ¥100,000 per hospitalization, one payment per hospitalization, 通算50回, cause-blind aggregation with the same 181st-day reset | [S1]; **[std]** (19) |
| 三大疾病無制限 特則 | Elected at issue and never cancellable: for がん（悪性新生物・上皮内新生物）, 心疾患 and 脳血管疾患 the per-hospitalization limit is 無制限 and those days sit outside the 通算 limit; for the remaining four 七大生活習慣病 the per-hospitalization limit doubles | [S1] [S2]; **[std]** (20) |
| Three-disease waiver (特定三疾病保険料払込免除特則) | Premiums waived for life on: がん — first diagnosis on or after the がん責任開始日, the 91st day from 責任開始日; 心疾患 — 急性心筋梗塞 on any admission for treatment or a listed surgery, other 心疾患 on a continuous stay of 10 days or more or a listed surgery; 脳血管疾患 — the same structure with 脳卒中 as the acute limb | [S1] |
| Relaxed underwriting (引受基準緩和型) | Out of scope | [S9]; scope **[std]** (21) |

18. The **¥20,000,000 cap is uniform** at every carrier that publishes one [S1] [S3] [S5]
    [S6] [S7] [S9] — one of the few genuinely market-wide parameters in the product. The
    cash top-up is not: 10% of the benefit capped at ¥500,000 per 療養 [S1]; 20% of the 技術料
    capped at ¥1,000,000 [S9]; a flat ¥100,000 with no second payment inside 60 days [S6];
    and reimbursement only, of the amount the insured actually bore, at a fourth [S5]. The
    composite takes 10%/¥500,000, the middle of the three cash shapes. On term: one
    carrier's rider is **10-year renewable** with no renewal limit, repriced at each
    renewal, the cap applied treating pre- and post-renewal periods as continuous [S9]; two
    attach it for the life of the contract and allow one such rider per insured across their
    own policies [S1] [S5]. The composite attaches it for life, with renewal repricing
    carried as the 定期-flag behaviour. The rider is cheap and the cap is large — a published
    specimen puts it at **¥114 of a ¥5,874 monthly premium** [S9]. The public claim
    experience shows why, and why the average is the wrong calibration target: in 令和5年度,
    144,282 patients received 先進医療 across 81 technologies, and 先進医療A averaged about ¥67,700
    per case — but 陽子線治療 ran to about ¥2,660,000 per case over 824 cases and 重粒子線治療 to about
    ¥3,140,000 over 462 cases [R9]. The aggregate average is dominated by high-volume
    fertility technologies whose exposure is not this rider's.
19. Only one carrier's rider is specified at this level in the retrieved documents [S1]; a
    second's 入院時一時金給付特約 is limited to two payments per policy year [S10]; a third makes the
    lump sum a **main-contract 型** — a 短期入院一時金型 paying 日額 × 10 on any admission and then
    日額 × (入院日数 − 10) from day 11, and an 入院一時金型 paying 日額 × 20 per hospitalization and
    nothing per day [S9]. The composite keeps the lump sum as an optional rider on a per-day
    main contract, the majority architecture. It matters economically because it is the
    market's answer to falling stay lengths [R6] [REG-R27]: as the mean stay falls a per-day
    benefit shrinks and a per-admission benefit does not.
20. The relaxation is sold in four wrappers: a 七大生活習慣病入院給付特則 offering a 三大疾病無制限プラン
    and a 七大疾病無制限プラン off one main contract [S1] [S2]; an おすすめコース for the 3大生活習慣病,
    expressly excluding 上皮内新生物 and 異形成 from 「がん」 [S6]; a separate 三大疾病無制限型長期入院特約
    [S5]; and nothing at all [S10]. The composite takes the 三大疾病 form as a switch — the most
    common relaxation, and what the published premium at the composite's specification
    includes [S3]. Its weight is large: lifetime cancer incidence in Japan is about 61.1%
    for men and 50.1% for women [REG-R28], so removing the day limit for cancer, heart
    disease and cerebrovascular disease is a mass-market feature, not a fringe option. Two
    mid-stay reclassification rules come with it and a model must not smooth them: under
    三大疾病無制限型 a stay that starts for a non-七大 cause and during which treatment of a 七大生活習慣病
    **other than 高血圧症** begins is treated as a 七大 stay **from the admission date**; under
    七大疾病無制限型 a mid-stay start of 高血圧症 treatment does **not** convert the stay [S1] [S2].
21. One carrier's booklet is for a 引受基準緩和特則付 product — relaxed underwriting, and so a
    different morbidity basis [S9]. The composite is fully underwritten;
    relaxed-underwriting business is a separate product, not a rider.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value (*kaiyaku-henreikin*, 解約返戻金) | None under 終身払, at any duration; under the 65歳払済 variant, **10 × 入院給付金日額** once the premium-paying period completes | [S1] [S6] [S9]; **[std]** (22) |
| Policyholder dividend (配当金) | None — the chassis is 無配当; no maturity benefit (満期保険金) exists | [S1] [S6]; [REG-R9] |
| 契約者貸付 / 自動振替貸付 | Neither offered — there is no surrender value to lend against, so a missed premium lapses the policy | [S1]; [REG-R14] |
| Rider values | Riders carry no surrender value at any point in the policy period | [S1] |
| Grace period (払込猶予期間), 月払 | From the first day of the month following the 払込期月 to the **last day of that month** | [S1] [S4] [S10]; **[std]** (23) |
| 払込猶予期間, 半年払・年払 | From the first day of the month following the 払込期月 to the monthly contract anniversary in the month after that | [S1] [S4] |
| Claims during grace | Unpaid premiums are deducted from the benefit; if the benefit is insufficient the balance must be paid by the end of grace, failing which the contract lapses from the day after grace expires and neither the benefit nor the waiver is given | [S4] |
| Lapse (失効) | From the day after the grace period expires | [S1] [S4] [S6] [S10] |
| Reinstatement (復活) | Available within **1 year** of 失効, on payment of arrears and fresh 告知; may be refused on health grounds; cover restarts on the 復活日 and the pre-existing-condition and waiting-period clocks reset to it | [S4] [S9]; **[std]** (24) |
| First-premium failure | The contract is **void** (無効), not lapsed | [S1] [S10] |
| Non-disclosure (告知義務違反) | Rescission within **2 years** of 責任開始日 or of the 復活日; no defeat of a claim where there is no causal connection; 詐欺による取消 has no time limit and returns nothing | [S1] [S10]; ceiling [REG-R35] |
| クーリング・オフ | 15 days from the application date [S1] / 8 days from the day after it [S10]; out of scope | [REG-R36]; scope **[std]** (25) |
| Death of the insured | Cover terminates; any surrender value that exists is paid to the policyholder | [S1] |

22. Every carrier examined writes **no surrender value during the premium-paying period**
    [S1] [S6] [S9] [S10]. Where a 短期払 is chosen a small value appears afterwards,
    standardized across two carriers at 10 × 入院給付金日額 [S1] [S6]; a third converts the same
    idea into a 保険料払込期間満了後死亡保険金 of 10 × 入院給付金日額, payable only under a 短期払 [S9]; a fourth
    says a value "may exist but is small" without a figure [S10]. The composite adopts 10 ×
    日額 after a completed 短期払 and zero everywhere else. On the anchor cell (終身払) it is
    identically zero, which is the point: the surrender decrement here carries no cash flow
    at all, unlike on the [whole life savings chassis (終身保険)](../whole_life/product-spec.md).
23. Three carriers state the same monthly grace [S1] [S4] [S10] and one states two months
    [S6]; the composite takes the majority. One carrier's calendar special case for 半年払・年払
    where the 契約応当日 falls on the last day of February, June or November [S4] is not adopted.
24. **The widest carrier divergence in the whole product.** Reinstatement is not available
    at all at one carrier — 「保険料が未払いで契約が失効してしまうと、契約を元に戻すこと（復活）ができません」
    [S6] [S8]; within 1 year at two [S4] [S9]; within 3 years at a fourth [S10]; described
    only as 「a period that varies by product」 at the fifth [S1]. The composite takes one
    year, the modal published window. It is material because it decides whether lapse is
    absorbing, and because reinstatement re-runs the waiting periods and resets the
    pre-existing-condition clock [S4] [S9] — a reinstated policy is not the policy that
    lapsed.
25. 保険業法 第309条 sets an eight-day window from the later of delivery of the disclosure
    document and the application date, effective on **dispatch** of the notice [REG-R36];
    one carrier contracts for 15 days [S1], another for the statutory 8 [S10]. `jplib`
    models from the point cover is in force and treats the window as out of scope — it is a
    pre-inception decrement, and modelling it would need a new-business funnel this library
    does not have.

---

## Contractual mechanics

### The benefit structure: frequency × severity × limit

Write `D` for the 入院給付金日額, `L1` for the per-hospitalization day limit (60 or 120), `LA`
for the 通算 aggregate limit (1,095), and index hospitalizations by `i`. A hospitalization is
not a claim event of fixed size: it is a draw of a **duration** from a length-of-stay
distribution, truncated by two limits, one of which has memory. That is the whole product.

    days_used(i)   = days of stay i that fall inside the same "one hospitalization"
                     grouping as any earlier stay it is joined to
    paid_days(i)   = min( stay_days(i), L1 - days_used(i) )         [per-stay limit]
    paid_days(i)   = min( paid_days(i), LA - agg_days_paid_before )  [aggregate limit]
    hosp_benefit(i) = D * paid_days(i)

With the five-day minimum switch on, and only when the stay is not truncated by a limit:

    paid_days(i) = 5    if stay_days(i) <= 5

The floor is expressed by the carriers as an amount, 日額 × 5, rather than as five days [S4]
[S6] [S7]; the two readings differ only if the floor could itself push a stay through the
aggregate limit, and the composite treats the floor as an amount so that it cannot.

Where the insurer treats a later admission as part of an earlier hospitalization, the later
days are simply aggregated against `L1` and the excess is not paid [S2]. Where the 日額 is
reduced mid-stay, one carrier applies the amount in force on each day, except that the first
five days use the amount in force at admission [S4]; the composite holds `D` constant for
the life of the contract, so the rule does not bind.

### What counts as one hospitalization — the 180-day rule

The rule that gives this product its memory. Two admissions `i` and `j`, with `j` later, are
**one hospitalization** when both hold:

    cause(j) is the same as cause(i), or is medically related to it
    admission_date(j) <= discharge_date(i) + 180 days

and `j` starts a **new** hospitalization on the 181st day counting the day after
`discharge_date(i)` as day 1 [S1] [S2]. For the 災害 limb one carrier tests the same accident
rather than the same cause, plus admission within 180 days of the accident date [S10].
Riders may carry their own grouping: one carrier's 入院一時金特約 and 通院治療支援特約 aggregate
cause-blind while its main contract does not [S1], so a model that shares one grouping
across main contract and riders is wrong for that design. The empirical basis for
calibrating how often the rule binds is public: 患者調査 publishes 推計退院患者数 by 過去の入院の有無 and by
再入院までの期間 [R7] [REG-R33].

### Aggregate limit and benefit-driven termination

    agg_days_paid(t) = cumulative paid_days over all hospitalizations to time t,
                       tracked separately for the 疾病 and 災害 limbs

Each limb has its own `LA` = 1,095 [S4] [S1]. When both limbs are exhausted the contract
terminates [S9]. Under the 三大疾病無制限 特則, days attributable to がん, 心疾患 or 脳血管疾患 are
paid without a per-hospitalization limit **and are excluded from `agg_days_paid`** [S1] [S2]
— which means electing the 特則 does not merely raise the limits, it removes the largest
single consumer of the aggregate from the count, and materially defers the termination
decrement.

On the 定期 chassis flag, `agg_days_paid` and the 先進医療 cap carry across renewals:
「保険期間（更新契約の保険期間を含みます）を通じて1,095日」 [S7], and the same at the other term carrier [S10].
The general rider principle is stated as 「給付金の通算支払限度の規定を適用するときは、更新前の特約で
既に支払われた給付金を通算します」 [S5].

### Surgery benefit

    surg_benefit = D * m,    m = 20 if the surgery falls inside a hospitalization
                                  for which 入院給付金 is payable
                             m = 5  otherwise

with the composite's frequency limits [S1] [S2] [S9] [S10]:

- several surgeries on the same day pay only the single highest-paying one;
- a surgery spanning two or more days is dated at its start [S2];
- where the 手術料 is charged per day, only the first day is paid;
- where the 診療報酬点数表 charges 手術料 once for a connected course of treatment, only the
  highest-paying single instance is paid [S2] — one carrier expresses the identical rule as
  a 60-day lockout after a paid surgery of that kind [S10];
- 放射線照射 and 温熱療法 pay at most once in any 60 days.

The covered set is defined by reference to the public fee schedule, not by a private list of
named conditions [S1] [S2] [S4] [S9] [S10], and every carrier reserves the right to change
the 支払事由 prospectively, with 主務官庁 approval, if the public scheme is amended [S2] [S6].
**This is a real structural advantage over a UK critical-illness definition set**: the
benefit trigger is enumerable from a public document, and it moves when that document moves.
A public surgery-rate proxy exists too — 患者調査 crosses 推計退院患者数 and 平均在院日数 with 手術の有無 [R7].

### 先進医療 benefit

    adv_paid(k)   = min( tech_fee(k), 20,000,000 - adv_paid_cumulative )
    adv_top_up(k) = min( 0.10 * adv_paid(k), 500,000 )

and the rider terminates when `adv_paid_cumulative` reaches ¥20,000,000 [S1] [S5]. A series
of treatments under one 先進医療 is a single 療養 [S1] [S6] [S9]. Eligibility is tested at the
date of treatment, so a technology, institution or indication that has since left the
厚生労働大臣's 先進医療 list pays nothing [S1] [S5]; 患者申出療養 is a different scheme and is excluded
[S6].

### Premium waiver

The base waiver is **disability-triggered, not sickness-triggered**: 高度障害状態 from any cause,
or a listed 身体障害の状態 arising from an 不慮の事故 within 180 days of the accident [S1] [S2]
[S10]. It does not apply once the premium-paying period has ended, and is excluded where the
condition arises from 故意・重大な過失, the insured's criminal act, 精神障害, 泥酔, unlicensed
driving or drink-driving [S2]. On the anchor cell, which is 終身払, the waiver is live for the
whole projection.

The 特定三疾病保険料払込免除特則 extends it with **explicitly different triggers per disease** [S1]:

- **がん** — first diagnosis on or after the がん責任開始日, defined as the 91st day counting from
  責任開始日; the diagnosis date is the date the confirming test was performed, not the date the
  doctor communicated the result.
- **心疾患** — 急性心筋梗塞: any admission for treatment, or a listed surgery. Other 心疾患: a
  **continuous stay of 10 days or more**, or a listed surgery.
- **脳血管疾患** — the same structure, with 脳卒中 as the acute limb.

The ten-day continuous-stay condition is a materially different trigger from a diagnosis
trigger: it must be modelled off the length-of-stay distribution, not off an incidence rate.
That is the single most easily mis-modelled item in this document. It also interacts with
[REG-R14] II-2-1-2(4), which requires that where a contract on premium waiver is
automatically renewable, the reserve be computed **as though every automatic renewal to
final expiry occurs** — a real reserving instruction for the 定期 flag.

### Waiting periods, 責任開始 and 告知

There is **no general waiting period** on the main medical cover: cover starts at 責任開始 and
the waiting periods that exist are targeted [S1]. The full set found: がん 90 or 91 days on
the cancer-linked riders and 特則 [S1] [S6]; one year on 骨髄幹細胞の採取術 at four carriers [S1] [S2]
[S6] [S9] [S10], capped at two payments over the whole policy period including renewals at
one of them [S10]; one year on a named list of eight elective procedures — 痔瘻・痔核・脱肛手術, named
子宮関係手術, 脊髄硬膜内外手術, 副鼻腔炎手術, 白内障・水晶体観血手術, endoscopic 大腸・胃 resections,
眼瞼下垂症手術 and 扁桃腺摘出術 — with the exclusion **not** re-imposed at renewal [S10]; two years
on a 白内障 limb of one 先進医療特約 [S6]; and one year on a 骨髄ドナー入院給付金, where nothing is paid
if the stay *ends* within the year [S9].

告知 is an answer-the-question duty (質問応答義務) made in writing or on screen; 告知受領権 rests with
the company and, where there is one, the examining physician — telling a 生命保険募集人 orally is
not 告知 [S1] [S10]. Rescission for 告知義務違反 runs for **2 years** from 責任開始日 or 復活日
[S1] [S10], inside the statutory ceiling of five years from inception [REG-R35]; a shorter
contractual window is permitted because it favours the policyholder.

### Grace, lapse and reinstatement

For a 月払 contract, grace runs from the first day of the month following the 払込期月 to the
last day of that month — roughly one extra month [S1] [S4] [S10]. A claim arising in the
grace window is paid net of the unpaid premium; if the benefit is smaller than the arrears
the balance must be paid by the end of grace, failing which the contract lapses from the day
after grace expires and **neither the benefit nor the waiver** is given [S4]. Non-payment
produces 失効 from the day after grace expires [S1] [S4] [S6] [S10].

There is nothing to break the fall. On a product with a 解約返戻金 the insurer would advance the
premium under 自動振替貸付 — an election the 監督指針 requires be at the policyholder's choice and
notified promptly [REG-R14] — but this chassis has no surrender value and one carrier states
that neither 契約者貸付 nor 自動振替貸付 is offered [S1]. **The lapse is real and immediate**, and
that is the structural difference between the third-sector chassis and the
[whole life savings chassis (終身保険)](../whole_life/product-spec.md).

復活 within one year restores cover from the 復活日 on payment of arrears and fresh 告知, and may
be refused on health grounds [S4] [S9]. Reinstatement is not a rewind: the 責任開始期 for
pre-existing-condition tests resets to the last 復活 [S4], and a waiting period is re-run from
the 復活日 where the remainder would otherwise have expired [S9].

---

## Riders and options

**In scope (modeled or parameterized):**

- **先進医療特約** — modelled as a reimbursement stream with a lifetime cap and a 10% capped
  top-up, and a rider termination on reaching the cap [S1] [S5] [S6] [S9]. Switchable off.
- **入院一時金特約** — ¥100,000 per hospitalization, 通算50回, on its own cause-blind grouping
  [S1]. Switchable off; off in the base run.
- **三大疾病無制限 特則** — removes the per-hospitalization limit for がん, 心疾患 and 脳血管疾患 and
  takes those days out of the aggregate [S1] [S2]. Switchable; off in the base run.
- **特定三疾病保険料払込免除特則** — a premium-waiver extension with three distinct triggers,
  including the ten-day continuous-stay limb [S1]. Parameterized; off in the base run.
- **Base 保険料払込免除** — disability-triggered, in force during the premium-paying period
  [S1] [S2] [S10]; a waiver state is specified in the technical notes.
- **Five-day minimum payment** — a benefit-formula switch, off in the base run [S4] [S6]
  [S7].
- **120日型 and 1,000日 aggregate** — limit switches [S1] [S4] [S9] vs [S6] [S7] [S10].

**Out of scope:** 通院治療支援特約（退院時一時金給付型）and general 通院特約 [S1] [S5];
特定三疾病一時金特約 and がん治療給付金 (which belong to
[cancer (がん保険)](../cancer/product-spec.md)) [S1] [S6]; 女性入院給付金 and
女性疾病入院特約 [S2] [S5]; 七大疾病無制限 as distinct from 三大疾病無制限 [S1] [S2]; the
主契約-型 lump-sum designs — 短期入院一時金型 and 入院一時金型 — and their day-conversion rules
[S9]; the 手術総合特約 written on a separate 手術給付金基準額 [S9]; the separate 放射線治療給付金 of
日額 × 10 [S4]; the 重大手術 40倍 tier [S4]; 終身保険特約（無解約払戻金型）and other death-benefit
riders [S1]; 健康サポート特則 [S9]; 引受基準緩和特則 [S9]; ケガの特約 and 三大疾病無制限型長期入院特約
[S5]; the 健康還付特則 premium-refund design, which exists in the market but whose terms could
not be read [S12] [unverified]; and the 定期 chassis's contractual conversion into a 終身医療保険
at a term end [S10].

---

## Variations across insurers

1. **Chassis.** 終身 only at three carriers [S1] [S4] [S9]; 終身 and 定期 as separate products at
   a fourth [S6] [S7]; 定期型 only, ten-year renewable to 80 with a conversion right, at a
   fifth [S10]. Composite: 終身 base with a 定期 model-point flag — the majority design, and the
   one that exercises the lifetime aggregate limit (footnote 1).
2. **Five-day minimum payment.** Present at two of five [S4] [S6] [S7], absent at three
   [S1] [S2] [S9] [S10]. Composite: absent in the base run, switchable — the two positions
   differ by roughly a factor of two on the modal short stay and cannot be averaged
   (footnote 8).
3. **Per-hospitalization day limit.** 60/120 [S1] [S4]; 60 only [S6] [S7] [S10]; 60/120/730
   [S9]; 40/60/120 [S11] [unverified]. Composite: 60 default, 120 switch — 60 is the only
   value every carrier offers.
4. **Aggregate day limit.** 1,095 at four [S4] [S6] [S7] [S10]; 1,000 at three [S1] [S2]
   [S9]. Composite: 1,095, applied separately to the 疾病 and 災害 limbs, with 1,000 as a
   switch.
5. **What counts as one hospitalization.** Same-cause-or-medically-related at three
   [S1] [S2] [S6] [S7] [S10] against cause-blind at two [S4] [S9]; the 災害 limb is tested on
   the same accident at one [S10]. Composite: same-or-related with the 181st-day reset;
   cause-blind is strictly more aggregating and is a switch (footnote 10).
6. **Surgery benefit structure.** 20倍/5倍 [S1] [S3]; 10倍/5倍 [S6] [S7]; 10倍/5倍/40倍 重大手術
   [S4]; flat 10倍 in-hospital only [S10]; 20倍 or 10倍 on a separate rider 基準額 [S9];
   40/20/10/5倍 [S11] [unverified]. Composite: 20倍/5倍 (footnote 12). The widest dispersion in
   benefit *level* in the product — on a ¥5,000 daily amount the same surgery pays ¥100,000
   at one carrier and ¥50,000 at another.
7. **Surgery during a stay whose day limit is exhausted.** Paid at the in-hospital multiple
   [S4]; not paid at all [S10]; unstated in the other three sets of conditions. Composite:
   paid, as a switch. A genuine contradiction, and it bites where the day limit bites.
8. **Radiation therapy.** A separate 放射線治療給付金 at 日額 × 10 [S4]; inside a surgery rider at
   20倍/10倍 [S9]; folded into 手術給付金 at three [S1] [S2] [S6] [S10]. Composite: folded in, with
   the 60-day lockout all five impose.
9. **Lifestyle-disease limit relaxation.** A 七大生活習慣病入院給付特則 with 三大 and 七大 unlimited
   plans [S1] [S2]; an おすすめコース for the 3大生活習慣病 excluding 上皮内新生物 [S6]; a separate
   長期入院特約 [S5]; nothing [S10]. Composite: 三大疾病無制限 as a switch (footnote 20).
10. **先進医療 top-up.** 10% capped ¥500,000 per 療養 [S1]; 20% of the 技術料 capped ¥1,000,000
    [S9]; flat ¥100,000 [S6]; reimbursement only [S5]. Composite: 10%/¥500,000. The
    ¥20,000,000 cap itself does not vary.
11. **Hospitalization lump sum.** A rider at ¥100,000 with 通算50回 [S1]; a rider capped at two
    payments per policy year [S10]; a **main-contract 型** paying 日額 × 10 or × 20 with a
    day-conversion against the limits [S9]; absent [S6] [S7]. Composite: optional rider on a
    per-day main contract.
12. **復活.** Not available at all [S6] [S8]; within 1 year [S4] [S9]; within 3 years [S10];
    unstated [S1]. Composite: 1 year (footnote 24). It determines whether lapse is
    absorbing.
13. **Pre-inception disease.** Covered after two years, and paid in full where never
    consulted or flagged, at one carrier [S4]; not covered at the other four [S1] [S2] [S9]
    [S10]. Composite: not covered.
14. **Grace period.** One month at three [S1] [S4] [S10]; two months at one [S6]. Composite:
    one month. クーリング・オフ likewise differs — 15 days [S1] against the statutory 8 [S10]
    [REG-R36] — and is out of scope either way.
15. **What does not vary.** The surgery trigger is the 公的医療保険制度's 医科診療報酬点数表 at every
    carrier, with the same seven-item exclusion list and the same 60-day radiation lockout
    [S1] [S2] [S4] [S6] [S9] [S10]; the 先進医療 aggregate cap is ¥20,000,000 everywhere it is
    published [S1] [S3] [S5] [S6] [S7] [S9]; 疾病 and 災害 hospitalization benefits are never
    paid for the same day, and the 災害 limb always requires admission within 180 days of the
    accident [S1] [S4] [S9] [S10]; the 180-day window is the one-hospitalization boundary
    everywhere, however the cause test is drawn [S1] [S2] [S4] [S6] [S7] [S9] [S10];
    bone-marrow harvesting always carries a one-year wait and excludes 自家移植 [S1] [S2] [S6]
    [S9] [S10]; the per-hospitalization 型 is elected at issue and never changeable [S4]
    [S9]; and every main contract is 無配当 and, during the premium-paying period, 無解約返戻金 [S1]
    [S2] [S4] [S6] [S9]. These are the invariant core of the composite, and the parts of it
    a [cancer (がん保険)](../cancer/product-spec.md) or
    [nursing care (介護保険)](../nursing_care/product-spec.md) delta should expect to inherit unchanged.

---

## Regulatory context

**Classification.** 医療保険 is 第三分野 business under 保険業法 第3条第4項第2号, and the same class is
available under a 損害保険業免許 by 第3条第5項第2号 [R1] [REG-R1]. Everything below follows from that
classification rather than from the product's shape.

**Prudential — the third-sector reserving overlay.** 保険業法 第116条第1項 requires a policy
reserve (*sekinin-junbikin*, 責任準備金) at each 決算期, and 第2項 delegates the accumulation method
and the level of the calculation coefficients for long-term contracts [REG-R4]; 施行規則 第68条
says which contracts are in scope of the resulting standard policy reserve (*hyōjun
sekinin-junbikin*, 標準責任準備金) [R2] [REG-R7]; and 平成8年大蔵省告示第48号 sets the method — net level
premium (*heijun jun-hokenryō-shiki*, **平準純保険料式**), with no Zillmer adjustment — the table
vintages and the standard valuation interest rate (*hyōjun riritsu*, 標準利率) reset machinery
[REG-R10]. For contracts concluded on or after **1 April 2018** the third-sector valuation
mortality is **第三分野標準生命表2018** [REG-R11] [R4] [REG-R18].

On top of that sits the overlay specific to this product class. 施行規則 第69条第1項 divides the
reserve into 保険料積立金, 未経過保険料, 払戻積立金 and contingency reserve (*kiken junbikin*,
危険準備金) [R2] [REG-R8], and **第69条第6項第1号の2 requires a separately identified
「第三分野保険の保険リスクに備える危険準備金」** — a contingency reserve held specifically against
third-sector insurance risk, whose accumulation and release follow standards set by the
金融庁長官 [R2]. The 監督指針 then says how it is computed: 「第三分野保険のストレステストを使用しての
危険準備金の算出にあたっては」 the calculation must be performed under **平成10年6月8日大蔵省告示第231号**,
with organisational separation between the calculating unit and internal audit [R3]
[REG-R13]; the ストレステスト and the accompanying 負債十分性テスト must properly reflect the uncertainty
that 保険事故発生率 deteriorates, and must in principle be run **per contract grouping sharing the
same 基礎率**, groupable only where the benefit trigger and risk characteristics are equivalent
*and* the statistical source for the 予定発生率 is the same [R3] [REG-R14]. Disclosure must make
the reasonableness of the 危険発生率等の設定水準 clear [R3].

**This is the exact boundary at which the reference model marks its morbidity basis [std].**
There is no published morbidity table: 日本アクチュアリー会 publishes the mortality basis only, under
its 指定法人 role in 保険業法 第122条の2 [R4] [REG-R23], and every insurer's incidence, duration and
surgery-frequency assumptions are its own and sit in the unpublished 算出方法書 [REG-R2]. What
the regulator supplies instead of a table is a **test**. `jplib` implements the sensitivity
— a re-runnable incidence basis — and **not** the statutory stress, whose magnitudes could
not be retrieved and are [unverified] [REG-R13].

Three facts about the valuation mortality table that a medical model must not blur. First,
第三分野標準生命表2018 is deliberately **lighter** than the death-insurance table: male q40 is
0.00076 against 0.00118 on 生保標準生命表2018（死亡保険用）, and q60 0.00548 against 0.00653 [R4].
That is the correct direction of conservatism — on a health product death *releases* the
liability, so the valuation table must under-state mortality — and it means a best-estimate
medical model must not adopt the valuation table as its mortality decrement without an
explicit [std] adjustment, and must say which of the two it is using at each point [REG-R20]
[REG-R21]. Second, **第三分野標準生命表2018 excludes 高度障害**, unlike its 2007 predecessor [R5]
[REG-R20], so a model that treats 高度障害 as a termination must add it separately. The table
was built on the national 第21回生命表 (2010) with 2.5% p.a. improvement for five years and 1.0%
for three, plus a 2σ risk-theory margin bounded **below at 70% and above at 85%** of the
unadjusted rate, and it is constructed for use on a nearest-birthday (*hoken-nenrei
hōshiki*, 保険年齢方式) basis while the contracts age on 満年齢 [R5] [REG-R20] — half a year of age
between a pricing and a valuation model.

Third, **the table is readable but not redistributable, and the difference matters.**
日本アクチュアリー会 publishes it free, in full and machine-readable at a stable public URL [R4]
[REG-R18] [REG-R19] — anyone can retrieve it and check a rate, which is the sharp contrast
with the subscriber-only UK tables — but the publisher's site terms prohibit reproduction,
alteration and transmission to third parties without written consent [REG-R21]. So `jplib`
**cites** the table by URL, **quotes** only the handful of rates a worked example actually
uses, and **ships** a documented **[std]** construction over those quoted rates. It does
not ship the table, and no document in this library should say that it does.

**Prudential — solvency.** From **31 March 2026** insurers are supervised on the
economic-value **ESR** (経済価値ベースのソルベンシー規制), a three-pillar regime in which liabilities are
現在推計 plus MOCE, re-measured at each 基準日 on assumptions re-set then, with required capital
calibrated at **99.5%**; early corrective action is triggered below an ESR of **100%**
[REG-R15]. It replaces the ソルベンシー・マージン比率 trigger at **200%** [REG-R17], and the two ratios
are not comparable — the 2025 field test showed 生保単体 ESR 215% against SMR 873% [REG-R15].
`jplib` computes neither. What it owes the regime is that its projections are re-runnable on
a re-set assumption basis at a stated 基準日 — for a third-sector product, exactly the
capability the ストレステスト demands.

**Conduct.** 監督指針 II-4-2-2 fixes what the 契約締結前交付書面 must contain: 商品の仕組み, 保障の内容 with
the main 支払事由 and 免責事由, 付加できる主な特約, 保険期間, 引受条件, 保険料, 保険料払込みに関する事項,
配当金に関する事項 and 解約返戻金等の水準 in the 契約概要; クーリング・オフ, 告知義務, 責任開始期, the main
non-payment cases and 保険料の払込猶予期間、契約の失効、復活 in the 注意喚起情報 [REG-R14] — item for item,
the source list this specification is built from. クーリング・オフ is the eight-day dispatch-rule
right of 保険業法 第309条 [REG-R36], contracted wider at one carrier [S1], and is out of scope
here. Non-disclosure remedies run under 保険法 第55条, whose ceiling is five years from inception
with a one-month clock from discovery [REG-R35]; the two-year contractual windows observed
[S1] [S10] are permitted as 片面的強行規定 narrowing in the policyholder's favour [REG-R14]. The
suicide exclusion of 保険法 第51条第1号 carries **no statutory time limit at all**, so the
three-year 免責期間 observed [S1] is a contractual narrowing and a per-carrier fact [REG-R34].
On insurer failure, contracts are compensated up to **90% of the 責任準備金** at the failure date
through the 生命保険契約者保護機構 [REG-R40], the rate set by ordinance under 保険業法 第270条の3
[REG-R41].

**Tax.** A 医療保険 premium falls in the **介護医療保険料** basket of the post-2012 three-basket
life insurance premium deduction (*seimei hokenryō kōjo*, 生命保険料控除), which covers contracts
concluded on or after 2012-01-01 that pay on 医療費支払事由 [R11]. The income-tax deduction is the
full premium up to ¥20,000; premium/2 + ¥10,000 to ¥40,000; premium/4 + ¥20,000 to ¥80,000;
and a flat **¥40,000** above — capped at ¥40,000 per basket and **¥120,000** overall [R10]
[REG-R43]. The anchor cell pays about ¥25,200 a year, sitting in the second band for a
deduction of about ¥22,600: real, and second-order. The 住民税 caps are not stated on the 国税庁
pages retrieved and are [unverified] [R11]. Benefits are not modelled net of policyholder
tax.

**Professional standards.** Every life insurer appoints an appointed actuary (*hoken
keirinin*, 保険計理人) under 保険業法 第120条 [REG-R5], who confirms at each 決算期 whether the 責任準備金
「が健全な保険数理に基づいて積み立てられているかどうか」 and submits an 意見書 under 第121条 [REG-R6]. The
日本アクチュアリー会 実務基準 turns that item into the **1号収支分析** — a forward income-and-outgo
analysis over 「少なくとも将来10年間」, by 区分経理 segment, with sufficiency judged over the first five
years [REG-R22]. That is Japan's cash-flow-testing regime, and it is the shape these
projections take. Statutory reserving under J-GAAP, the ESR economic balance sheet and IFRS
17 — voluntary in Japan, not mandatory [REG-R47] — are three measurement bases fed by one
set of projected cash flows, which is why this library keeps product cash flows
basis-agnostic. This chassis is 無配当, so the surplus-distribution methods of 施行規則 第30条の2
[REG-R9] and the 三利源 framing that goes with them do not apply to it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-medical-r1
[R10]: #jplib-medical-r10
[R11]: #jplib-medical-r11
[R12]: #jplib-medical-r12
[R13]: #jplib-medical-r13
[R2]: #jplib-medical-r2
[R3]: #jplib-medical-r3
[R4]: #jplib-medical-r4
[R5]: #jplib-medical-r5
[R6]: #jplib-medical-r6
[R7]: #jplib-medical-r7
[R9]: #jplib-medical-r9
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
[REG-R26]: #jplib-reg-r26
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
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
