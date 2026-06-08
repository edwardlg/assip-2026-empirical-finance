# Solutions — PS 7.4 (A Reproducible Merged Analysis Dataset, With Diagnostics)

**Problem set:** `book/weeks/week-07/ps7.4.md` (PS 7.4, Week 7).
**Chapter:** Ch 7.4 — Building the Analysis Dataset, with the companion notebook nb7.4. Callbacks to Ch 7.2 (raw pulls / data cards), Ch 7.3 (the PAP), forward to Ch 7.5 (identification memo); survivorship & look-ahead from the Week 5 reading guides; the missing-data taxonomy from the Week 6 fair-lending arc; data-snooping from Week 1.

Because PS 7.4 is a **build-and-document** assignment, this manual does not give "the answer" — it gives **one fully worked exemplar deliverable** at the A-grade standard, so an instructor can grade *shape and discipline*, and a student can see what "done well" looks like before building their own project's panel. We work **Sam's CRSP × Compustat value panel** (the chapter's running example), because every cast project reduces to the same skeleton: link on a date-aware crosswalk with `validate=`, lag to a point-in-time `available_date`, keep the units that died, winsorize where justified, log the missing-data rule, and emit a row-count audit trail. A grader scoring Maya's HMDA build or Devon's crypto build should map each section below onto that project's analogue (noted in the grading sidebars).

**Every number in this document is illustrative.** The match rates, row counts, and summary statistics below are *hand-chosen, internally consistent teaching figures* — they are **not** real CRSP/Compustat output and must not be quoted as such. A real build's diagnostics differ by snapshot vintage; the point is the *shape of the story*, not the digits. The code patterns, by contrast, are real: they are the ones nb7.4 runs and verifies offline. **Licensed CRSP/Compustat bytes never leave GMU infrastructure and are never committed to git (CONVENTIONS §5)** — what follows commits the *code* and the *log*, not the data.

---

## The exemplar at a glance

> **Project (Sam).** *Do firms with high book-to-market ratios earn higher subsequent returns?* Unit-period: `(permno, month)`. Outcome: monthly return `ret` (delisting-adjusted). Key regressor: lagged, winsorized book-to-market `bm_w`. Snapshot pinned in header: `CRSP_SNAPSHOT = "2026-04-30"`, `COMPUSTAT_SNAPSHOT = "2026-04-30"` (illustrative). Sample: U.S. common stocks (CRSP `shrcd in (10,11)`), 1990–2024, monthly.

The deliverable is two things: a **build script** (outlined below, instrumented end to end) and a **two-page diagnostics report** (the tables and the log it emits, each line defended).

---

## Problem 1 — The crosswalk and the merge contract (18 points)

**(a) (5 pts)** Sam joins **CRSP monthly returns** (`crsp.msf`-style: keyed by **PERMNO**, a permanent *security* number) to **Compustat annual fundamentals** (keyed by **GVKEY**, a permanent *company* key). He cannot join on a ticker or a name: a PERMNO is a security and a GVKEY is a company — different *kinds* of object — and tickers are recycled nicknames (the ticker "C" was Chrysler before Citigroup). A naive ticker join would silently glue Citigroup's returns onto Chrysler's fundamentals for the years before the ticker was reassigned, producing garbage rows that *look* like successful matches. The crosswalk is the **CRSP/Compustat Merged (CCM) link history** (`crsp.ccmxpf_lnkhist`), which maps each GVKEY to the PERMNO(s) it corresponds to, *and the date span over which that link is valid.*

**(b) (4 pts)** CCM is *time-varying*, so Sam respects four things:

- **`LINKTYPE`** — link quality; keep only the researched/confirmed `LINKTYPE in ('LU','LC')`. *(Per Ch 7.4 `[CHECK]`: confirm the full recommended set against the WRDS CCM docs for the pinned vintage — LU/LC is the standard convention but the code set is occasionally revised.)*
- **`LINKPRIM`** — the primary-link flag; keep `LINKPRIM in ('P','C')` so a company with multiple share classes (multiple PERMNOs) is not double-counted.
- **`LINKDT` / `LINKENDDT`** — the validity window; a PERMNO–GVKEY pairing is meaningful *only* inside `[LINKDT, LINKENDDT]`.

The link **cannot** be collapsed to a `{permno: gvkey}` dictionary because the map is time-varying: the same PERMNO can belong to *different* GVKEYs in different eras (or to none), so a dictionary that ignores the date window reproduces exactly the Chrysler/Citigroup error in the years the link did not hold. The date window is the whole game.

**(c) (5 pts)** The merge contract, one assertion per join:

| # | Left (cardinality) | Right (cardinality) | Key(s) | `how=` | `validate=` | Claim |
|---|---|---|---|---|---|---|
| 1 | CRSP returns (many rows / PERMNO) | CCM link (one valid row / PERMNO-window after `LINKTYPE`/`LINKPRIM` filter) | `permno` | `inner` | `many_to_one` | many return-months map to ≤ 1 link |
| 2 | linked returns (many rows / GVKEY) | Compustat fund. with `available_date` (one row / GVKEY-period) | `gvkey` (+ asof on date) | `merge_asof` `backward` | (asof; uniqueness enforced by sort + `by=`) | each month gets the most-recent prior fundamental |

The **riskiest** merge is #1: if the `LINKTYPE`/`LINKPRIM` filter is incomplete, a GVKEY can carry *two* link rows valid on the same date (the two share classes of one company), turning the asserted `many_to_one` into a hidden many-to-many. That is a **Cartesian explosion** — if a key appears twice on the right, every left month for that key *doubles*, silently reweighting the regression. `validate="many_to_one"` converts that silent corruption into a loud `MergeError` at the exact line.

**(d) (4 pts)** Build with `how="left"` + `indicator=True` even though the final panel is an inner join, so you can *measure* completeness before discarding the unmatched:

```python
diag = crsp.merge(ccm, on="permno", how="left",
                  validate="many_to_one", indicator=True)
match_rate = (diag["_merge"] == "both").mean()
unmatched  = diag.loc[diag["_merge"] == "left_only", "permno"].nunique()
print(f"Linked {match_rate:.1%} of CRSP rows; {unmatched:,} PERMNOs found NO link")
```

**Illustrative result:** `Linked 97.6% of CRSP rows; 412 PERMNOs found NO link`. **Alarm threshold:** if the match rate fell below ~90% Sam would *stop* and audit the date filter / `LINKTYPE` selection before analyzing the matched subset, because a result computed on, say, 60% of rows is selected on a criterion he has not understood. Two benign reasons a CRSP row legitimately fails to link: **ADRs** (foreign firms with no Compustat North America GVKEY) and **closed-end funds / ETFs** (securities Compustat fundamentals do not cover). In nb7.4 the deliberately-unmatched case is the **secondary share class** (PERMNO 90001 of GVKEY 1001), correctly excluded by the `LINKPRIM` filter — a feature, not a bug.

> **Grading (18).** (a) names both identifiers *and* the recycled-ticker failure — 5; missing the failure mechanism caps at 3. (b) all four CCM fields + the "not a dictionary because time-varying" reason — 4. (c) a contract *per merge* with an explicit `validate=` value and the riskiest one named — 5; a contract with no `validate=` value is the headline error of the sheet, cap at 2. (d) `how="left"`+`indicator`, both diagnostic lines, an alarm threshold, two *benign* reasons — 4. *Non-CRSP map:* Maya names her self-built lender×geography key and a reassigned-LEI ambiguity; Priya names CIK↔GVKEY; full credit if the date-awareness / non-dictionary point is made in her data's terms.

---

## Problem 2 — Survivorship: count the firms that vanished (16 points)

**(a) (4 pts)** *Survivorship bias for Sam:* the unit is a stock; "death" is **delisting** (bankruptcy, acquisition-at-a-loss, exchange removal). Survival is correlated with the outcome because the firms that died are disproportionately **distressed, high-book-to-market firms whose prices collapsed**. Dropping them keeps the value firms that *recovered* and discards the value firms that *failed*, so Sam's value-premium estimate is biased **upward** — he would be measuring the return to *being a value firm that happened to survive*, a strategy no one could have followed in real time.

**(b) (6 pts)** The per-year firm-count smell test:

```python
counts = panel.groupby("year")["permno"].nunique()
```

**Illustrative series** (the diagnostic is the *shape*, not the digits):

| year | … | 2006 | 2007 | 2008 | 2009 | 2010 | … |
|------|---|------|------|------|------|------|---|
| firms | … | 4,910 | 4,880 | **4,310** | **4,120** | 4,205 | … |

The series **churns**: it *falls* from 2007→2008 (4,880 → 4,310) and again 2008→2009 (4,310 → 4,120) as the financial-crisis delistings exit, then recovers as IPOs enter. **The diagnostic:** a healthy universe has units *entering and exiting* every year; a survivorship-biased universe is **monotonically increasing**, ending exactly at "today's" universe with no exits. Sam's two falling adjacent years (2007→2008, 2008→2009) are the exits — exactly what a survivor-only pull would be missing. *(nb7.4 shows the contrast directly: the full universe churns 16→61→33 while the survivor-only series is monotone.)*

**(c) (3 pts)** The fix is **incorporating the delisting return (`dlret`)**: when a stock is removed, CRSP records its final (often catastrophic) return, and Sam folds `dlret` into the last monthly `ret` *before* the firm exits the panel — he does **not** drop delisted rows just because the months *after* delisting are missing. In the pipeline this is step `01 + delisting ret`, applied to raw CRSP before any merge. If he dropped them instead, he would erase precisely the crashes that make the dead firms informative — re-introducing the upward bias from (a).

**(d) (3 pts)** *Illustrative toy.* Mean monthly return on the **full churning** universe: $0.78\%$. Mean on the **survivors-only** subset (drop every firm not present in the final year): $1.08\%$. Gap $= +0.30$ percentage points, **upward** — survivors look better because the crashes were removed. One sentence: this is **selection on the outcome** — conditioning the sample on survival, which is correlated with the return, is the same potential-outcomes error the Week 3 lens trained Sam to smell. *(nb7.4 asserts this gap is positive on its synthetic universe: `+0.30%`.)*

> **Grading (16).** (a) correct *direction* of bias with the distress mechanism — 4. (b) the `groupby.nunique()` series *and* the entry/exit-vs-monotone diagnostic *and* a quoted falling pair — 6; a series with no interpretation caps at 3. (c) "incorporate `dlret`, don't drop" — 3. (d) two means, the signed gap, the selection-on-outcome sentence — 3. *Maya:* the dead unit is a *failed lender* (2008 subprime originators); same upward-style selection logic, full credit.

---

## Problem 3 — Look-ahead and the point-in-time discipline (20 points)

**(a) (4 pts)** The lagged variable is **Compustat book equity**. It carries a *fiscal-year-end date* (`datadate`, e.g. 2014-12-31) but is not *knowable* until the firm files its 10-K — weeks to months later (the SEC allows large filers 60 days, smaller filers up to 90). The canonical bug: merging December-2014 book equity onto December-2014 returns and forming a portfolio that trades on numbers the market had not yet seen.

**(b) (5 pts)** Build the point-in-time `available_date` with the **6-month Fama–French lag** — fiscal year ending in calendar year $y$ usable from **June 30 of $y{+}1$**:

```python
fund = compustat[["gvkey", "datadate", "book_equity"]].copy()
fund["available_date"] = pd.to_datetime(
    fund["datadate"].dt.year.add(1).astype(str) + "-06-30"
)
```

**Worked example:** fiscal-2017 book equity (`datadate = 2017-12-31`) → `available_date = 2018-06-30` → matched only to returns from **July 2018 through June 2019**. Six months is *deliberately generous*: it sits comfortably after even a late filer has reported, trading a little timeliness for the certainty that Sam never peeks.

**(c) (6 pts)** The point-in-time merge attaches the most-recent *available* fundamental to each return month:

```python
fund = fund.sort_values("available_date")
rets = crsp_linked.sort_values("ret_date")      # monthly returns, carries gvkey
panel = pd.merge_asof(
    rets, fund,
    left_on="ret_date", right_on="available_date",
    by="gvkey", direction="backward",            # look BACKWARD only — no peeking
)
```

`merge_asof(direction="backward")` is the right tool and a plain `merge` is not: it **structurally cannot attach a future record** — it walks backward to the most recent value whose `available_date ≤ ret_date`, so a future fundamental can never leak into a past return, by construction rather than by hope.

**(d) (5 pts)** The tripwire, run on every build:

```python
assert (panel["ret_date"] >= panel["available_date"]).all(), \
    "LOOK-AHEAD: a return uses accounting data dated after the return!"
```

It is **load-bearing and cannot be replaced by eyeballing results** because a look-ahead bug is *invisible in the output* — it raises the mean return, the Sharpe ratio, and tightens the $t$-stat, i.e. it makes everything look *better*, so a good-looking backtest is exactly what a leak produces. The only place the bug shows is in the *dates*, and the assertion checks the dates directly. **Failure demo (nb7.4 "Your Turn" #2):** flip to `direction="forward"` and `merge_asof` attaches the *next* fundamental (dated after the return); the assertion then **fires** —

```
AssertionError: LOOK-AHEAD: a return uses accounting data dated after the return!
```

**Illustrative:** on the forward run the assertion fires on **2,108** of 2,556 panel rows. On the correct backward run it **holds** over all 2,556. That is the design working: the bug cannot survive a clean run.

> **Grading (20).** (a) names the reporting-lag variable + the period-end-vs-knowable gap — 4. (b) `available_date` code + the June-30-of-$y{+}1$ rule + a worked fiscal-year→usable-date example + the "generous on purpose" reason — 5. (c) `merge_asof(direction="backward")` *with* the "structurally cannot attach a future record" justification — 6; using a plain `merge` for the lag caps at 2 (it cannot enforce the asof relation). (d) the assertion verbatim *and* the "invisible in output, only in dates" argument *and* the forward-direction fires-demo — 5. *Universal:* every project must show the no-look-ahead assertion *passing* on its build; missing it is the single most-penalized omission after a missing `validate=`.

---

## Problem 4 — Winsorize where justified (and where not) (14 points)

**(a) (5 pts)** Sources of extreme book-to-market, and the fix each demands:

1. **Data errors** — a misplaced decimal, a thousands-vs-millions units mismatch, a stale CUSIP gluing the wrong firm's book value to a stock → *found and fixed or dropped*, not smoothed.
2. **Definitional artifacts** — a firm with **near-zero or negative book equity** produces a book-to-market that explodes or flips sign; mathematically real, economically meaningless → *excluded by a stated rule*. **Sam's screen: drop firm-years with `book_equity <= 0`** (the standard Fama–French negative-book-equity screen), pipeline step `05 drop neg book eq`.
3. **Genuine extreme values** — a really distressed firm with a really high book-to-market → *kept*; these are signal, and in finance the tails are where the action is.

**(b) (5 pts)** Winsorize `bm` **within each cross-section** (by month), symmetric 1%/99%, $N$ preserved:

```python
def winsorize(s, lower=0.01, upper=0.99):
    lo, hi = s.quantile([lower, upper])
    return s.clip(lower=lo, upper=hi)

panel["bm_w"] = (panel.groupby("ret_date")["bm"]
                      .transform(lambda s: winsorize(s, 0.01, 0.99)))
```

**Illustrative before/after:** pre-winsor max `bm = 440.0`; post-winsor max `bm_w = 280.0` (the 99th-percentile cap of that month); **$N$ unchanged at 2,556** — winsorizing *caps*, it does not delete, which is the whole reason it is preferred over **trimming** (trimming would delete those rows and reduce $N$). Winsorizing **within** the month, not pooled, judges a 1999 outlier against 1999 contemporaries and a 2008 outlier against 2008's, not against a different decade. The cardinal sin **not** committed: searching over cutoffs (1%? 2.5%? 5%?) until the $t$-stat clears 2 — that is $p$-hacking with extra steps; the cutoff is fixed at 1%/99% *before* any regression.

**(c) (4 pts)** **When not to.** Priya's **catastrophe-insurance losses** and Devon's **daily crypto returns** are cases where the extreme observations *are the phenomenon*: winsorizing a catastrophe model's largest losses erases the very tail risk being measured, and capping a 40%-move crypto day deletes the volatility that is the subject. **Principle:** *an outlier is noise to be capped when it is a measurement artifact or a nuisance in a control; it is signal to be preserved when the extreme value is the quantity of interest.* The right move for the fat-tailed case is a **model built for fat tails** — a log transform, a quantile regression, a robust estimator — not a cap that defines the problem away. One sentence: **winsorize the noise in your controls; do not winsorize away your subject.**

> **Grading (14).** (a) all three sources with the *matching* fix, and the negative-book-equity screen named — 5. (b) cross-sectional `groupby.transform` winsorize + $N$-preserved + max-moved-to-cap + the no-cutoff-search discipline — 5; pooled (not by-date) winsorizing caps at 3. (c) a named do-not case + the noise-vs-signal principle + the fat-tail alternative — 4. *Devon:* his answer should put crypto returns in the *do-not-winsorize* column and reach for a robust/fat-tail model.

---

## Problem 5 — Missing data: why it is missing, not how much (16 points)

We work the missing-data discipline on Sam's panel, but flag where **Maya's HMDA** is the sharper teacher (the chapter's lead example).

**(a) (4 pts)** Required fields and percent-missing (illustrative):

| field | % missing |
|---|---:|
| `ret` | 1.8 |
| `bm_w` | 6.1 |
| `me` (market equity) | 0.3 |

`bm_w` is missing most — driven by firm-months with no *available* fundamental yet (a young firm before its first usable 10-K). Sam's suspected mechanism is **MAR-given-controls** (missingness depends on firm age, which he observes), tilting toward **MCAR** in nb7.4's synthetic build where returns are blanked uniformly at random. The professional question is never "how much?" but "*why*?" — for Maya's HMDA income field the answer is the dangerous one, **MNAR**: the lowest-income applicants are the most likely to leave income blank, so the act of being missing carries information about the missing number itself.

**(b) (5 pts)** The probe that earns its keep — compare a downstream quantity across present-vs-missing:

```python
panel["bm_missing"] = panel["bm_w"].isna()
print(panel.groupby("bm_missing")["ret"].mean())
```

**Illustrative (Sam, MCAR-ish):** mean `ret` present $= 0.79\%$ vs missing $= 0.77\%$ — a near-zero gap, **consistent with MCAR**, so listwise deletion loses precision but not unbiasedness. **Contrast — Maya (MNAR), the canonical case:** `df.groupby("income_missing")["denied"].mean()` would show denial rates that differ *sharply* between missing- and present-income rows; that gap is the signal that missingness is **informative**, dropping those rows changes the population studied, and the decision must be made deliberately and documented. *(nb7.4 is MCAR-by-construction — gap ≈ 0.04 SD on log book equity — and its "Your Turn" #1 has students rebuild it MNAR on HMDA so the denial-rate gap widens.)*

**(c) (4 pts)** Given the MCAR-ish verdict, Sam chooses **logged listwise deletion**, never silent:

```python
required = ["ret", "bm_w"]
before = len(panel)
panel = panel.dropna(subset=required).copy()
after = len(panel)
print(f"Listwise dropped {before-after:,} rows "
      f"({(before-after)/before:.1%}); kept {after:,}.")
```

**Illustrative:** `Listwise dropped 231 rows (8.0%); kept 2,640.` Had he **imputed** instead (e.g., mean-fill `bm_w`), he would keep $N$ but inject a cost — naïve mean-imputation **distorts variances and correlations** and is not a free lunch; multiple imputation is the honest version and needs a **set seed**.

**(d) (3 pts)** Dropping MNAR rows is **selection on the outcome** — the same error as **survivorship** (Problem 2), one wearing a missing-data hat and the other a delisting hat; both condition the sample on something correlated with the outcome. In the Ch 7.5 memo Sam will state how many rows the listwise rule dropped *and* check that the **survivors are not systematically different from the dropped on observables he can see** (e.g., compare mean size / industry mix of dropped vs kept) — the difference between cleaning and hiding.

> **Grading (16).** (a) the percent-missing table + a *named* MCAR/MAR/MNAR mechanism with a reason — 4. (b) the `groupby` missingness probe *run*, two group means, and the right verdict (and recognizing Maya's HMDA is MNAR) — 5; "I called `dropna()`" with no probe caps at 1. (c) a *logged* rule with rows-dropped count + the imputation cost named — 4. (d) the MNAR↔survivorship link + the survivors-not-different check — 3.

---

## Problem 6 — The build script and the row-count audit trail (16 points)

**(a) (6 pts) The build-script outline** (one-way `raw → intermediate → analysis`, every step logged):

```python
# build_value_panel.py  —  rebuilds analysis/value_panel.parquet from raw/ with one command.
# SNAPSHOT (pinned): CRSP=2026-04-30, COMPUSTAT=2026-04-30   [illustrative]
# Licensed CRSP/Compustat raw stays read-only on GMU infra; NOT committed to git (CONVENTIONS §5).
import os, logging
import numpy as np, pandas as pd
rng = np.random.default_rng(42)                     # seed wherever randomness enters
WRDS_USER = os.environ["WRDS_USER"]                 # secrets via env vars, never hard-coded

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("build")
def step(df, name):                                 # row-count logger: print shape, return df
    log.info("[%-26s] rows=%9d  unique_firms=%7d", name, len(df), df["permno"].nunique())
    return df

# --- RAW (untouched ground truth) ----------------------------------------
crsp = step(load_parquet("raw/crsp_msf.parquet"),               "00 raw CRSP")
crsp = step(apply_delisting_returns(crsp),                      "01 + delisting ret")   # P2
ccm  = filter_ccm(load_parquet("raw/ccm_lnkhist.parquet"))      # LINKTYPE in (LU,LC), LINKPRIM in (P,C)
fund = load_parquet("raw/compustat_funda.parquet")
fund["available_date"] = june30_next_year(fund["datadate"])     # P3: 6-mo FF lag

# --- INTERMEDIATE (linked, lagged, typed; saved as Parquet) --------------
linked = step(crsp.merge(ccm, on="permno", how="inner",
                         validate="many_to_one"),               "02 link CCM (m:1)")    # P1
linked = step(linked.query("linkdt <= ret_date <= linkenddt").copy(),
                                                                "03 date-window filter")
panel  = step(pd.merge_asof(linked.sort_values("ret_date"),
                            fund.sort_values("available_date"),
                            left_on="ret_date", right_on="available_date",
                            by="gvkey", direction="backward"),  "04 merge_asof (6mo lag)")
assert (panel["ret_date"] >= panel["available_date"]).all(), "LOOK-AHEAD!"             # P3 tripwire
panel.to_parquet("intermediate/linked_lagged.parquet")

# --- ANALYSIS (one rectangular panel: one row per (permno, month)) -------
panel["bm"] = panel["book_equity"] / panel["me"]
panel = step(panel.query("book_equity > 0").copy(),             "05 drop neg book eq")   # P4
panel["bm_w"] = (panel.groupby("ret_date")["bm"]
                      .transform(lambda s: s.clip(*s.quantile([.01, .99]))))            # P4
panel = step(panel.dropna(subset=["ret", "bm_w"]).copy(),       "06 listwise (ret,bm)")  # P5
assert panel.duplicated(subset=["permno", "ret_date"]).sum() == 0, "duplicate key!"     # P6c
panel.to_parquet("analysis/value_panel.parquet")
```

Hygiene satisfied: `validate=` on the one real `merge`; `.copy()` after every `.query`/`.dropna` slice that is then modified; **no chained-index assignment**; **no `df.append`** (any stacking uses a list + a single `pd.concat`); secrets from env; pinned snapshot; seeded RNG.

**(b) (5 pts) The row-count log** (illustrative; the *shape* is the story):

```
[00 raw CRSP               ] rows=  3 482 119  unique_firms=  24 188
[01 + delisting ret        ] rows=  3 482 119  unique_firms=  24 188
[02 link CCM (m:1)         ] rows=  3 105 442  unique_firms=  18 902
[03 date-window filter     ] rows=  2 988 310  unique_firms=  18 711
[04 merge_asof (6mo lag)   ] rows=  2 988 310  unique_firms=  18 711
[05 drop neg book eq       ] rows=  2 871 905  unique_firms=  18 433
[06 listwise (ret,bm)      ] rows=  2 640 117  unique_firms=  17 998
```

Adjacent-gap defense:

- **00→01:** rows unchanged — `dlret` *adjusts* the last return in place, it does not add or drop rows (expected).
- **01→02:** ~5,300 firms drop with no CCM link. **Expected** (ADRs, closed-end funds), but I confirm the *rate* — 97.6% of rows linked (Problem 1d), within tolerance.
- **02→03:** ~117k rows trimmed — return-months falling *outside* any valid `[LINKDT, LINKENDDT]` window, correctly removed.
- **03→04:** rows unchanged — `merge_asof` *attaches* a fundamental, never drops a return (months before a firm's first available fundamental carry NaN `bm`, dropped later at 06).
- **04→05:** ~116k firm-months drop under the stated negative-book-equity screen (Problem 4a).
- **05→06:** ~232k rows — the **listwise deletion**, the **largest single cut** and **the one I must justify in the memo** (Problem 5d): mostly young firm-months before a usable fundamental, plus missing returns.

**(c) (5 pts) Summary-statistics table** (`panel[keys].describe(percentiles=[.25,.5,.75]).T`; illustrative):

| variable | N | mean | sd | min | p25 | p50 | p75 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ret` (monthly) | 2,640,117 | 0.0079 | 0.118 | −0.65 | −0.052 | 0.004 | 0.061 | 2.41 |
| `bm` (raw) | 2,640,117 | 0.84 | 3.10 | 0.001 | 0.34 | 0.61 | 1.02 | 280.0 |
| `bm_w` (winsorized) | 2,640,117 | 0.81 | 1.12 | 0.04 | 0.34 | 0.61 | 1.02 | 8.6 |
| `me` ($M) | 2,640,117 | 3,910 | 18,400 | 1.2 | 96 | 412 | 1,870 | 1.9e6 |

Sanity checks the table **passes**: (i) `bm_w` min/max ($0.04$, $8.6$) are *inside* the raw `bm` range — winsorizing pulled the $0.001$ and $280.0$ tails to the monthly 1%/99% caps, and the SD collapsed $3.10 \to 1.12$ as the extreme leverage was bounded; (ii) $N = 2{,}640{,}117$ matches the final log line `06` exactly; (iii) no impossible values — `ret` never below $-100\%$ ($-0.65$ is the floor), no negative `bm` (the `book_equity > 0` screen worked); (iv) **the unit-period key is unique** — `panel.duplicated(subset=["permno","ret_date"]).sum() == 0` (asserted in the script). The panel passes.

> **Grading (16).** (a) a script with the three-stage structure *and* the `step()` logger on every transform *and* the full §5 hygiene checklist — 6; a missing `validate=`, a chained-index assignment, or a `df.append` is −2 each. (b) the log *plus* a one-sentence defense of every adjacent gap (the listwise cut flagged as the one to justify) — 5; a log with no interpretation caps at 2. (c) the `.describe().T` table + at least two sanity checks including **key uniqueness** — 5. *General:* a panel whose final-log $N$ disagrees with the summary-table $N$ is an automatic flag — it means a step ran that the log did not capture.

---

## Instructor grading notes

**What an A looks like.** The script *runs top-to-bottom on a fresh env from `raw/` with one command*, and the report defends **every line of the log**. The two structural tripwires are present and demonstrably exercised: a `validate=` on every merge (and the student can say what `MergeError` it would throw), and a no-look-ahead `assert` that *passed* on the real build and *fired* on the deliberate `direction="forward"` demo. The match rate is reported *with a threshold and benign-failure reasons*, not as a bare percentage. Every diagnostic number is labeled real-vs-illustrative.

**The five most common failure modes, and the deduction.**

1. **No `validate=` on a merge** (or `validate="many_to_many"`). The headline error of the whole sheet — a silent Cartesian-explosion risk. Cap Problem 1 at 2/18; if it recurs across the script, additional −2 in Problem 6a.
2. **Lagging with a plain `merge` instead of `merge_asof`.** A plain `merge` cannot enforce "most-recent prior available" — it either explodes (one return × many fundamentals) or silently grabs the wrong vintage. Cap Problem 3c at 2/6 and check whether the no-look-ahead assert was even possible to pass.
3. **Dropping delisted firms** "because their later rows are missing." This *is* the survivorship bug. Problem 2c → 0; flag whether the bias direction in 2a was nonetheless reasoned correctly (partial credit there).
4. **Silent `dropna()`** with no probe and no logged count. The single most common way to bias a study. Problem 5 cap at 4/16; the probe (5b) is the part that earns the credit.
5. **A row-count log with no interpretation**, or a final $N$ that disagrees with the summary table. The log is an audit trail only if every gap is *defended*; an undefended log is bookkeeping theater. Problem 6b cap at 2/5.

**Cross-project mapping (grade the *discipline*, not the source).** Maya (HMDA): there is no CCM, so Problem 1 is graded on her **self-built lender×geography crosswalk** and its reassignment ambiguity, and Problem 5 carries *extra* weight because HMDA's missing income is the textbook **MNAR** case (the denial-rate gap must be probed, not assumed). Priya (Compustat × EDGAR): the crosswalk is **CIK↔GVKEY**, the lag is the filing-date availability of the 10-K text score, and her catastrophe-loss variable is the Problem 4c **do-not-winsorize** case. Devon (crypto): fat-tailed returns are the do-not-winsorize subject; his look-ahead risk is the S-1 *filing date* vs the price series. Leah (PatentsView × financials): assignee↔PERMNO link through CIK, annual `(firm, year)` panel; patents are public so the §5 licensing rule binds only on the matched CRSP/Compustat leg.

**On the `[CHECK]` from Ch 7.4.** The exact recommended `LINKTYPE` set (LU/LC) should be verified against the WRDS CCM documentation for the student's pinned snapshot vintage. A student who *flags* this uncertainty rather than asserting a memorized code list is demonstrating exactly the snapshot-discipline the course wants — award the benefit of the doubt and do not penalize a correctly-hedged `[CHECK]`.

**On illustrative numbers.** Every figure in a submission should be tagged real (with a pinned snapshot) or illustrative (synthetic / borrowed). A student who quotes a 97.6% match rate or a "+0.30% survivorship gap" as a *real* CRSP finding — when it is in fact the nb7.4 synthetic value — has violated the standing rule and the CONVENTIONS §6 citation discipline; treat it the way you would a fabricated statistic, and require the relabel before awarding the points.

---

*End of solutions for PS 7.4. This exemplar worked Sam's value panel end to end — the merge contract with `validate=` per join, the 97.6% match-rate diagnostic, the churning per-year firm count, the 6-month `available_date` lag enforced by `merge_asof(direction="backward")` and proven by the no-look-ahead assertion, the by-date winsorize that preserved $N$, the logged MCAR-ish listwise rule, the `raw → intermediate → analysis` audit trail, and the summary-stats table with passing sanity checks — all at the A-grade standard and all with illustrative numbers. The live machinery is in `notebooks/week-07/nb7.4-dataset-build-validation.ipynb`, where `validate=` catches a 4.6× Cartesian explosion red-handed, the look-ahead assertion holds over the whole panel and then fires when `merge_asof` is flipped to `forward`, and the firm count churns the way a real universe does. The panel built here is the foundation Ch 7.5's identification memo stands on: a panel contaminated by survivorship or look-ahead turns the cleverest identification strategy into an estimate of an artifact.*
