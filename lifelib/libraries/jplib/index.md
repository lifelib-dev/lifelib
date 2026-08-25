```{module} jplib
```

# The **jplib** Library

```{warning}
{mod}`jplib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **jplib** library packages **nine reference liability cash flow projection models** for the
individual life insurance products sold in Japan — built with modelx, and, for each one, the
product specification and technical notes the model was built from.

The coverage differs in kind from both [uslib](../uslib/index.md) and
[uklib](../uklib/index.md), because the Japanese market does. Three of the nine are
third-sector (*dai-san bun'ya*, **第三分野**) products — medical (医療保険), cancer (がん保険) and
nursing care (介護保険) — and that is not a rounding item. Third-sector cover is what Japanese
households buy most by policy count, and none of the three is priced off a sum assured.
医療保険 is **frequency × severity × limit** — a daily amount, a per-event day cap, a lifetime
day cap; がん保険 keeps the frequency and severity and removes the day limit entirely; and
介護保険 is neither, being a state model whose benefit turns on a grading made by the public
scheme rather than on a count of days. A Japan library without them would describe a market
that does not exist. Group business,
cooperative insurance (共済) and group credit life (団体信用生命保険) are out of scope.

The models are the centre of the library. Each is a by-model-point projection of one product's
gross liability cash flows: premiums, claims, benefits, surrenders, expenses and commission, on
the product's own processing order and timing. None of them discounts — every model publishes
the cash flows and leaves discounting, the current estimate (*genzai suikei*, 現在推計), MOCE
and required capital to a layer that consumes them.

**Each one of these models reproduces a documented worked example, asserted cell by cell to the
precision the notes display.** The chain is deliberate and complete in both directions:

- `product-spec.md` specifies a *representative* product — a standardized composite built from
  publicly available documentation of real products, not any single insurer's contract. It
  records contractual mechanics, a full parameter set, the observed variation across insurers,
  and the rationale for every representative choice.
- `technical-notes.md` turns that product into a liability cash flow model on paper: model point
  attributes, state variables, assumption inputs, the recursions with their explicit processing
  order, policyholder behaviour, and a numeric worked example.
- The **model** implements those notes, and the library's own `tests/` assert the worked example
  against it. Change an assumption, and the test tells you whether the model and the notes have
  parted company.
- `sources.md` lists every source the first two cite, with URLs, access dates and whether the
  document was actually retrieved.

Every quantitative parameter in the library is either **source-tagged** or marked **[std]** — a
standardization introduced for the reference implementation, carrying its rationale and, where
available, the observed range across insurers. Facts taken from source material are never
silently mixed with assumptions made to complete a model.

```{admonition} These are mechanics demonstrations, not pricing or reserving results
:class: warning

More is sourced here than in either sister library — Japanese carriers publish premium rate
cards, and the statutory valuation tables can be read by anyone (see
[What is Japan-specific](#jplib-jp-specific)). That makes it *more* important, not less, to say
what is still standardized: every best-estimate decrement basis, every expense and commission
level, and every behavioural assumption. A published premium is a real premium; the basis this
library projects it on is not the basis it was priced on. Replace both with company data before
drawing any conclusion from the numbers.
```

## The models

Model names are `<short name>_<country>_<grid>`: a short descriptor, then `JP`, then `_A` for an
annual step or `_S` for a monthly one. The grid letters follow lifelib, where
`annuallife/TradLife_A` is the annual-step model and `basiclife/BasicTerm_S` and
`savings/CashValue_SE` are the monthly ones. `S` carries a second sense in lifelib — scalar, one
model point at a time, as against the vectorized `_M` models — and that is true of all nine here,
whether or not they carry the letter.

The short names are **English, and chosen rather than found**. Everywhere else in this library
the Japanese name leads, because it is what the product is called; a model name cannot follow,
being a Python identifier and a directory on disk. Nor is there a market abbreviation to borrow:
uslib takes `MYGA` and `RILA` and uklib takes `IP` and `ULB` from the trade's own usage, and
Japanese products have no Latin short form in circulation. So the pairing of model to product is
written down here and in `tests/jp_registry.py` rather than inferred.

**Protection**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [term life (定期保険)](products/term_life/index.md) | `Term_JP_A` | annual | 平準定期保険, 無配当, 無解約返戻金型: one decrement carrying both 死亡保険金 and 高度障害保険金 at the same sum assured, and **年満了 更新型** (*nen-manryō kōshin-gata*, a fixed-year term that auto-renews) — the term renews at attained-age rates to a ceiling of 80, which is what makes the liability longer than the term |
| [survivor income term (収入保障保険)](products/income_guarantee/index.md) | `IncomeTerm_JP_S` | monthly | A **death** benefit paid as a level 年金月額 to a fixed expiry date, so the total falls month by month, floored by the 最低支払保証期間 — which is implemented as a *term extension*, not a benefit floor, and so carries the projection past policy expiry. On the 定期保険 chassis, with 非喫煙者優良体 rate classes |

**Savings**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [whole life (終身保険)](products/whole_life/index.md) | `WholeLife_JP_A` | annual | Level-premium 終身保険, 無配当, carrying the policy reserve (*hokenryō tsumitatekin*, 保険料積立金) and the surrender value (*kaiyaku henreikin*, 解約返戻金) — the **base chassis** for the two below. The suppressed-surrender-value form (*tei-kaiyaku-henreikin-gata*, **低解約返戻金型**) suppresses the surrender value during the premium-paying period and steps it up at 払込満了: a cliff, not a curve. The automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付) is a modelled state |
| [endowment (養老保険)](products/endowment/index.md) | `Endowment_JP_A` | annual | 死亡保険金 = 満期保険金 over a fixed term, on the 終身保険 chassis; plus a **学資保険** cell whose premium waiver (*hokenryō haraikomi menjo*, 保険料払込免除) runs on the death of the policyholder (*keiyakusha*, 契約者) — a decrement on a life who is not the insured, with no analogue anywhere in the sister libraries |
| [FX whole life (外貨建終身保険)](products/fx_whole_life/index.md) | `FXWholeLife_JP_S` | monthly | 米ドル建 積立利率変動型 on the 終身保険 chassis, with three layers on top: a declared crediting rate over a guaranteed floor, 解約控除 plus MVA (市場価格調整) on surrender, and the currency itself. A **特定保険契約** under 保険業法第300条の2, and the library's one product projected in a currency other than yen |

**Third sector (第三分野)**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [medical (医療保険)](products/medical/index.md) | `Medical_JP_S` | monthly | The **third-sector chassis**: the daily hospitalization benefit (*nyūin kyūfukin nichigaku*, 入院給付金日額) with a 60日 per-hospitalization cap and a 通算1,095日 lifetime cap, 手術給付金 at a multiple of the daily amount, and 先進医療特約. The limits are the model — a projection that pays the daily amount without them is not this product |
| [cancer (がん保険)](products/cancer/index.md) | `Cancer_JP_S` | monthly | Deltas off 医療保険: a **90-day 免責期間** (*menseki kikan*, waiting period) before cover starts, a repeating がん診断一時金 on a stated cycle, がん入院給付金 with **no day limit** at all, 上皮内新生物 as a reduced second tier, and treatment-month benefits. Needs a post-diagnosis survival model, which a medical model does not |
| [nursing care (介護保険)](products/nursing_care/index.md) | `LTC_JP_S` | monthly | Deltas off 医療保険, but structurally a **three-state** model — healthy / in care / dead — with the care state absorbing and carrying its own mortality. The trigger is the public scheme's own 要介護 grading, so the benefit definition is a statute's, not a carrier's |

**Annuity**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [individual annuity (個人年金保険)](products/individual_annuity/index.md) | `Annuity_JP_A` | annual | 定額個人年金保険: accumulation to the annuitisation proceeds (*nenkin genshi*, 年金原資), then a 10年確定年金 payout, with the tax-qualification rider (*zeisei tekikaku tokuyaku*, 税制適格特約) attached. **Two standard tables in one model** — 死亡保険用 in deferral, 年金開始後用 in payment — and using one for both is a pitfall the tests assert against |

(jplib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside `run.py`,
so the model folder holds formulas and nothing else. `Projection`'s docstring carries the mapping
from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions_jp.py` applies
it to every model in the registry, and each model additionally has its own test module for its
worked example and its product-specific invariants — the notes' "Known modeling pitfalls"
sections are written up there as tests.

The registry is per library; the contract it enforces is the one
[uslib is held to](#uslib-one-shape), and cells names come from lifelib —
`basiclife/BasicTerm_S` first, then `savings/CashValue_SE` — so a name means the same thing here,
in uslib, in uklib and in lifelib. The [shared vocabulary table](#uslib-shared-vocabulary) is the
settled ruling for all three libraries.

The registry lives in `tests/jp_registry.py` rather than in `conftest.py` for a reason worth
knowing: `conftest` is a name pytest fixes, so three in-library suites collected in one run put
three files of that name on `sys.path`, one wins `sys.modules`, and a suite silently locates
another library's models — a green run against the wrong thing.

(jplib-jp-specific)=

### What is Japan-specific about these models

Five things recur across the set and are worth knowing before reading any one of them.

**The statutory tables can be read, but not redistributed — and the difference is the point.**
生保標準生命表2018（死亡保険用）, 生保標準生命表2007（年金開始後用）and 第三分野標準生命表2018 are
published in full, free, at stable public URLs [REG-R18] [REG-R19]. The 2018 PDF holds four
tables and no 年金開始後用 among them — the annuity-in-payment table still in force is the 2007
one, and the consolidated workbook [REG-R19] is its only public source, which is why
`Annuity_JP_A` reads two tables of different vintages. Anyone can retrieve any of them and check
a rate. That
is a real contrast with [uklib](../uklib/index.md), where the CMI tables are restricted to
Authorised Users and cannot be read at all without a subscription. But the publisher's site terms
prohibit reproduction and transmission to third parties without written consent [REG-R21], so
this library **cites the tables and quotes only the individual rates its worked examples use**,
and ships every `mort_table.csv` as a **[std]** construction whose `provenance` column points
back at them. There is a second distinction underneath the first: even the real tables are
**valuation** tables carrying an explicit safety margin [REG-R20], not best-estimate experience,
so a best-estimate basis is a [std] adjustment of them either way. **jplib does not ship the
statutory tables.** It ships a documented proxy anchored to tables you can go and read.

**The pricing side is more observable here than in either sister library.** Japanese carriers
publish premium scales by age and sex, two of them as full grids across sums assured, and one
grid is linear enough in the sum assured that a marginal rate and a flat monthly policy fee can
be **derived** from it — derived, not disclosed: no carrier publishes either component. So the
anchor premium of `Term_JP_A`, `IncomeTerm_JP_S`, `WholeLife_JP_A`, `Endowment_JP_A` and
`FXWholeLife_JP_S` is a **sourced** number rather than a modelling value. uslib reaches that
for a handful of products from specimen policies and prospectuses; uklib reaches it for none,
because UK protection pricing is quote-driven. The third-sector three are the exception and their anchor premiums
are **[std]** — not because nothing is published, but because what is published does not price
the composite: specimen 月払保険料 scales were retrieved for 医療保険, and the filed premium and reserve basis
(*sanshutsu hōhōsho*, 算出方法書) that would settle the representative specification is one of the
基礎書類 (*kiso shorui*) filed with the 金融庁 and is not
published [REG-R2].

**The public morbidity data is good enough to build on.** 厚生労働省 患者調査 publishes 受療率
and 平均在院日数 by age [REG-R26] [REG-R27]; 国立がん研究センター publishes 全国がん登録 罹患率 and
5年相対生存率 [REG-R28] [REG-R29]; 厚生労働省 介護保険事業状況報告 publishes 要介護認定率 by age
band [REG-R30]. That is why the three third-sector models can carry a *derived* incidence basis
with a citation on it rather than an invention — and why the modelling work that matters in
`LTC_JP_S` is the prevalence-to-incidence conversion, which is shown rather than assumed.

**Two contractual mechanics have no analogue in uslib or uklib, and both change the liability
rather than a parameter.** Renewal (更新): a 年満了 定期保険 renews automatically at attained-age
rates unless the owner declines, so the contract boundary question is real and the answer changes
the sign of the reported result — `Term_JP_A` publishes both readings rather than picking one
silently. Automatic premium loan (自動振替貸付): where a premium is unpaid and there is a
解約返戻金, the insurer *lends* the premium against it, so a policy with a surrender value does
not lapse while the loan can carry it. It is a modelled state in `WholeLife_JP_A`, and its
absence from `Term_JP_A` is a product fact — 無解約返戻金型 leaves nothing to lend against.

**Scope limits are stated and validated against, not faked.** Where a deterministic run cannot
reach a mechanic, the notes say so: `FXWholeLife_JP_S`'s 目標到達時円建終身保険移行特約 is a
path-dependent option that a single deterministic path values at intrinsic only, and its 市場価格
調整 needs a rate path the model does not simulate. The models publish what they produce and
name what they do not.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **収入保障保険** states only its deltas against the
  [term life technical notes (定期保険)](products/term_life/technical-notes.md) — the same decrement and
  premium chassis, with the benefit replaced by an income stream and the horizon extended past
  policy expiry by the 最低支払保証期間.
- **養老保険** and **外貨建終身保険** inherit the
  [whole life savings chassis (終身保険)](products/whole_life/technical-notes.md) — 保険料積立金, 解約返戻金,
  自動振替貸付 — and add, respectively, the maturity benefit with the 学資 payment-waiver
  decrement, and the crediting, surrender-charge and currency layers.
- **がん保険** and **介護保険** state their deltas against the
  [medical third-sector chassis (医療保険)](products/medical/technical-notes.md), which is where the
  benefit-day limit machinery is specified once.
- **個人年金保険** stands alone. Its payout phase is not a chassis for anything here, and the
  two other products that project an income stream do not inherit it: 収入保障保険 pays an
  annuity-certain floored by a guarantee period, and 介護保険 a survival-tested 介護年金 capped
  by a number of instalments. Three annuity shapes, three sets of mechanics, stated separately
  because they are separate.

## How to use the library

Create your own copy of the *jplib* library, as described in the {ref}`create-a-project` section.
For example, to copy it to *C:\\path\\to\\your\\jplib*:

```python
>>> import lifelib

>>> lifelib.create("jplib", r"C:\path\to\your\jplib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/term_life/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/term_life/Term_JP_A")

>>> model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is each model's worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by `t` with one column per cash flow line.

The tests ship inside the library and run against *your* copy:

```bash
python -m pytest tests -q
```

## Library contents

```{list-table}
:header-rows: 1
:widths: 28 72

* - File or folder
  - Description
* - `products/<product>/`
  - One directory per product, holding its documents *and* its model together. Nine of them.
* - `products/<product>/product-spec.md`
  - The representative product specification: mechanics, parameters, variation across insurers.
* - `products/<product>/technical-notes.md`
  - The liability cash flow model on paper: state variables, recursions, processing order, worked example.
* - `products/<product>/model.md`
  - How the model implements those notes — what was standardized, what diverges, what the tests cover.
* - `products/<product>/sources.md`
  - Every source the product's documents cite, with URLs, access dates and retrieval status.
* - `products/<product>/<Model>/`
  - The modelx model itself. Formulas only — no embedded data.
* - `products/<product>/*.csv`
  - The model's inputs, external to the model folder so they can be edited or swapped in place.
* - `products/<product>/run.py`
  - Reads the model and prints its cash flow statement.
* - `references/`
  - The cross-product regulatory and actuarial bibliography, cited as `[REG-R#]`.
* - `tests/`
  - One module per model for its worked example and invariants, plus `test_model_conventions_jp.py` for the house style, and `jp_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records which
documents were actually retrieved and which fetches failed. Its source lists are **never
renumbered**: the product documents cite against them.

(jplib-citation-conventions)=

## Citation conventions

Whether a citation tag is a link tells you what kind of source it is. `[R1]` and `[REG-R18]` are
links: the first lands on entry R1 in **that product's** `sources.md`, the second on entry R18 of
the shared [reference library](references/regulatory-and-actuarial-references.md). `[S6]` is not
a link. It stays on the page as you see it, brackets and all, and names entry S6 in that
product's `sources.md` for you to look up.

That asymmetry is deliberate, and it is the same line the `sources.md` files draw between their
own sections. A regulatory or actuarial reference is an **authority** the model is held to, and
following it is part of reading the document. A primary product source is a **specification**
citation — the 約款 or 契約締結前交付書面 a number was taken from — which says where a figure came
from rather than what the model must obey. So one reads as a tag on the page and the other as a
link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (約款, ご契約のしおり, 契約締結前交付書面, 重要事項説明書, パンフレット) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(jplib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a rationale
and, where available, the observed range across insurers.

(jplib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not** be
confirmed against a retrieved document. Treat it as a to-verify item, not an established fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on the decrement bases, which are [std]
constructions anchored to tables this library may cite but not redistribute — see
[What is Japan-specific](#jplib-jp-specific).

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R47**, cited as `[REG-R#]` — with a
product-relevance matrix. It spans the prudential framework (保険業法 and 施行規則, 標準責任準備金
and the 標準利率, and the **経済価値ベースのソルベンシー規制** — Japan's economic-value solvency
regime, which commenced 2026-03-31 and applies from 2026年3月期, moving the early-corrective-action
trigger from ソルベンシー・マージン比率 below 200% to ESR below 100%), the actuarial layer
(日本アクチュアリー会's standard tables and the 保険計理人 practice standards), the public
statistical series the third-sector bases are built on, conduct and consumer protection
(保険法, 消費者契約法, クーリング・オフ, 生命保険契約者保護機構), and tax and accounting
(生命保険料控除's three baskets, 相続税法第12条, and the status of IFRS 17 in Japan).

## Known gaps and caveats

Aggregated from the per-product research; each product's documents carry the full list.

- **The standard tables may be cited, not shipped.** [REG-R21] — the position, and its
  consequences for every model, is set out in
  [What is Japan-specific](#jplib-jp-specific).
- **The 標準利率 in force at the access date could not be pinned down.** The reset machinery is
  fully retrieved [REG-R10], but the current numeric value is not published where the machinery
  is, so every reserve-basis rate used in this library is **[std]** with the mechanism cited.
  This is the single most consequential unresolved number in the library.
- **Two 告示 could not be located at all**: 平成10年6月8日大蔵省告示第231号 (the 第三分野 stress
  test) [REG-R13] and 平成8年大蔵省告示第50号 (ソルベンシー・マージン比率) [REG-R17]. The
  consolidated text of 平成8年大蔵省告示第48号 [REG-R10] was retrieved only from an unofficial
  mirror, which is disclosed at the entry.
- **The ESR 告示 themselves were not opened** — the regime is cited from the FSA's own summary
  [REG-R15], so the standard-formula coefficients and the internal paragraph structure are
  [unverified] here.
- **三利源 (死差・利差・費差) is practice, not regulation.** A full-text search of the 監督指針
  returns no occurrence [REG-R14]; the framing is carried as industry usage and tagged
  accordingly, not asserted as a supervisory requirement.
- **Bot-blocked and encoding-hostile sources.** Several carrier and ministry pages return 403 to
  plain fetchers or serve CP932 that garbles without local decoding; where a document could not
  be retrieved, the facts that depended on it are tagged [unverified] rather than asserted. Each
  product's `sources.md` and `_research/` file records which.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/term_life/index
products/income_guarantee/index
products/whole_life/index
products/endowment/index
products/fx_whole_life/index
products/medical/index
products/cancer/index
products/nursing_care/index
products/individual_annuity/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R10]: #jplib-reg-r10
[REG-R13]: #jplib-reg-r13
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R26]: #jplib-reg-r26
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
[REG-R29]: #jplib-reg-r29
[REG-R30]: #jplib-reg-r30
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
