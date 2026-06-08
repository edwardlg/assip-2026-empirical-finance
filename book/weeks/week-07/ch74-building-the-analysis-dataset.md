# Chapter 7.4 — Building the Analysis Dataset

In Chapter 7.2, Sam pulled two raw files off WRDS: a stack of monthly stock returns from **CRSP** (the Center for Research in Security Prices) and a stack of annual accounting numbers from **Compustat**. Each file, on its own, is clean and authoritative. Sam was proud. Then he tried to answer his actual question — *do firms with high book-to-market ratios earn higher returns?* — and discovered that the question lives in *neither* file. The returns are in CRSP. The book value is in Compustat. To compute book-to-market for firm $i$ in month $t$ and line it up against that firm's return, Sam has to **join** the two datasets. And the moment he typed `pd.merge`, every quiet decision he had been making without noticing turned into a loud one with consequences.

This is the chapter nobody puts in the brochure. Chapter 7.2 was the glamorous part — the API call, the data appearing on your screen. Chapter 7.5 is the *identification memo*, where you argue your design is credible. This chapter is the grinding middle: turning two (or five) raw pulls into a single, trustworthy **analysis panel** — one rectangular table, one row per unit-period, that your regression can actually consume. It is unglamorous, it is most of the real work, and it is where the largest, most embarrassing errors in empirical finance are made. A look-ahead bug here will sail through every robustness check in Week 5 and quietly inflate your Sharpe ratio by 40%, and you will not notice until a referee — or worse, real money — does.

The trick of this chapter, stated up front: **a dataset is not data; it is a sequence of decisions, and the decisions are the dataset.** Every merge you run, every row you drop, every outlier you reshape, and every "available as of" date you assign is a modeling choice that can change your answer. The professional skill is not avoiding these choices — they are unavoidable — but making them *deliberately, defensibly, and reproducibly*. We will build Sam's CRSP–Compustat panel step by step, with Maya's HMDA cleaning as a second worked example, and at every step we will do the two things amateurs skip: **count the rows** and **check the match rate**.

---

## 7.4.1 The crosswalk problem: nobody agrees on what to call a firm

Here is the first surprise. Sam assumes that to merge CRSP and Compustat he joins on "the company." But CRSP and Compustat were built by different people, for different purposes, decades apart, and **they do not use the same identifier for a firm.** CRSP, which tracks *securities trading on exchanges*, identifies each security by a **PERMNO** — a permanent number that stays attached to a stock even when its ticker changes (and tickers change constantly; they get recycled, reused, and reassigned). Compustat, which tracks *companies' financial statements*, identifies each company by a **GVKEY** — a permanent company key. A PERMNO is a *security*; a GVKEY is a *company*; and the two concepts are not even the same kind of object. A single company (one GVKEY) can have multiple share classes trading as multiple securities (multiple PERMNOs) — think of Alphabet's Class A and Class C shares.

So Sam cannot merge on a ticker. **Tickers are not identifiers; they are nicknames.** The ticker "C" meant Chrysler before it meant Citigroup. If you merge two financial datasets on ticker, you will silently glue together the returns of one firm to the fundamentals of an unrelated firm that happened to inherit the same three letters years later. This is not a rare edge case — it is a guaranteed source of garbage rows, and it is invisible because the merge "succeeds" and produces numbers.

The solution is a **crosswalk** (also called a *concordance* or *link table*): an external, authoritative table that maps one identifier system to another. For CRSP and Compustat, the crosswalk is the **CRSP/Compustat Merged (CCM) link table**, maintained precisely because this problem is hard enough that a vendor sells the answer. The relevant linking table is `crsp.ccmxpf_lnkhist` (the "link history" file) on WRDS. Its job is to tell you, for each GVKEY, *which PERMNO it corresponds to, and during which span of dates.* That last clause — **during which span of dates** — is the whole game, and the reason a crosswalk is not just a dictionary.

The CCM link carries, for each GVKEY–PERMNO pair, four things you must respect:

- **`LINKTYPE`** — the *quality* of the link. Codes like `LU` ("link used," a researched and confirmed link) and `LC` ("link confirmed") are the reliable ones; codes like `NR` or `NU` flag links that are unresearched or questionable. The standard practice is to keep only `LINKTYPE in ('LU', 'LC')`. [CHECK: confirm the current full set of recommended LINKTYPE codes against the WRDS CCM documentation for your snapshot vintage; the LU/LC convention is standard but WRDS occasionally revises the code set.]
- **`LINKPRIM`** — the *primary-link* flag, which resolves the multiple-securities problem. When one GVKEY maps to several PERMNOs (multiple share classes), `LINKPRIM in ('P', 'C')` marks the *primary* security so you do not double-count the company.
- **`LINKDT`** and **`LINKENDDT`** — the start and end dates over which the link is valid. A PERMNO–GVKEY pairing is only meaningful *within its date window*. Outside that window, the same PERMNO may belong to a different GVKEY, or the link simply did not exist.

That date window is why you cannot collapse CCM to a simple `{PERMNO: GVKEY}` dictionary. The map is *time-varying*. To merge correctly you must join on identifier **and** require that your observation's date falls inside `[LINKDT, LINKENDDT]`. Skipping the date filter is one of the most common silent errors in student CRSP–Compustat work, and it produces exactly the Chrysler/Citigroup pathology: returns matched to the wrong company in the years before or after the link was valid.

Two other crosswalks you will meet in this camp. First, **CIK ↔ ticker/PERMNO** for SEC EDGAR work: the SEC identifies filers by a **CIK** (Central Index Key), not a ticker or PERMNO. Leah, working on patents and 10-K text, has to map EDGAR filings (CIK) to CRSP returns (PERMNO). The SEC publishes a CIK–ticker lookup (`company_tickers.json`), but tickers are unstable, so the robust route goes through CUSIP or a researched link, not a raw ticker match. Second, **CUSIP** — a security identifier that *both* CRSP and Compustat carry, which tempts you into using it as a shortcut crosswalk. Resist the easy version of that temptation: CUSIPs are **9 characters** (8 + a check digit), but different vendors store **different truncations** (6-digit issuer-level, 8-digit, 9-digit), CUSIPs get **reassigned** over time, and CRSP's historical CUSIP (`NCUSIP`) differs from its current one. A naïve CUSIP merge fails the same way a ticker merge fails, just less obviously. Use the purpose-built link (CCM) when one exists; use CUSIP only when you understand exactly which truncation and which vintage you are matching, and when you still apply a date filter.

The one-sentence lesson: **never join financial datasets on a human-readable name or a recycled code; join on a researched, date-aware identifier crosswalk, and respect its validity window.**

---

## 7.4.2 Merge discipline: cardinality is a claim you must verify

Sam now has the pieces: a CRSP returns table keyed by PERMNO and date, a Compustat fundamentals table keyed by GVKEY and fiscal date, and the CCM link to connect PERMNO and GVKEY. Time to merge. Here is where we install the single most valuable habit in this entire chapter.

Every merge has a **cardinality** — a claim about how rows on the left relate to rows on the right. Is it one-to-one (each left row matches exactly one right row)? One-to-many (each left row matches several right rows)? Many-to-one? Many-to-many? You *think* you know which one you are doing. You are frequently wrong, because of a duplicate you did not know was in the data. And a merge whose cardinality is not what you assumed does not crash — it silently does the wrong thing, most destructively a **many-to-many** join, which produces a *Cartesian explosion*: if a key appears 3 times on the left and 4 times on the right, you get $3 \times 4 = 12$ output rows where you expected far fewer, and every duplicated row quietly reweights your regression.

The reveal-the-trick fix is one keyword. **`pandas` lets you assert the cardinality and refuses to proceed if reality disagrees**, via the `validate=` argument to `merge`:

```python
import pandas as pd

# Assert: each (permno, date) row matches AT MOST ONE link row.
# If a duplicate exists, pandas raises MergeError instead of silently
# exploding the panel.
linked = crsp.merge(
    ccm_links,
    on="permno",
    how="left",
    validate="many_to_one",   # many CRSP rows : one link  -- ASSERTED, not hoped
)
```

The legal values are `"one_to_one"` (`"1:1"`), `"one_to_many"` (`"1:m"`), `"many_to_one"` (`"m:1"`), and `"many_to_many"` (`"m:m"`). The first three *check* a uniqueness assumption and raise `MergeError` if it is violated; `"many_to_many"` checks nothing and is the default behavior you get when you omit the argument. **Always pass `validate=`.** It is one keyword and it converts a silent data-corruption bug into a loud, immediate exception at the exact line that caused it. If you write only one thing differently after reading this chapter, write `validate=`.

But `validate=` only checks *cardinality*; it does not tell you how *complete* your merge was. For that you check the **match rate** — what fraction of your left-hand rows found a partner. This is why you use an *indicator* and a `how="left"` join while you are building, even if the final panel is an inner join:

```python
# Diagnostic merge: keep all left rows and flag where matches came from.
diag = crsp.merge(
    ccm_links,
    on="permno",
    how="left",
    validate="many_to_one",
    indicator=True,            # adds a "_merge" column: left_only / both / right_only
)

match_rate = (diag["_merge"] == "both").mean()
print(f"Linked {match_rate:.1%} of CRSP rows to a GVKEY")
unmatched = diag.loc[diag["_merge"] == "left_only", "permno"].nunique()
print(f"{unmatched:,} PERMNOs found NO Compustat link")
```

Now you have a number to defend. If 98% of your CRSP rows link, fine — the 2% are probably ADRs, closed-end funds, or securities Compustat does not cover, and you should *know* that and say so. If only 60% link, **stop** — something is wrong with your identifiers, your date filter, or your `LINKTYPE` selection, and any result you compute on the 60% is selected on a criterion you have not understood. A match rate is not a nuisance statistic; it is the first place a careful reader looks to decide whether to trust your panel.

One more `pandas` hygiene rule that bites people during merges. After a merge or a `query`/boolean filter, when you intend to *modify* the resulting frame, take an explicit `.copy()`. Pandas will otherwise warn you with the infamous `SettingWithCopyWarning`, and — worse than the warning — your edits may or may not propagate depending on whether you got a view or a copy. **Never chain-index into an assignment.** Do this:

```python
# RIGHT: filter, copy, then assign on the owned frame.
analysis = diag.loc[diag["_merge"] == "both"].copy()
analysis["bm"] = analysis["book_equity"] / analysis["market_equity"]
```

not this:

```python
# WRONG: chained indexing; ambiguous whether you edited a view or a copy.
diag[diag["_merge"] == "both"]["bm"] = ...   # may silently do nothing
```

And while we are listing the deprecated and the dangerous: **do not use `df.append`** to stack frames row by row in a loop — it was removed in pandas 2.0 and was quadratic-time anyway. Build a list and call `pd.concat` once:

```python
frames = []
for year in years:
    frames.append(load_year(year))
panel = pd.concat(frames, ignore_index=True)   # one concat, not N appends
```

---

## 7.4.3 Survivorship bias: the firms that vanished are the ones that matter

Now the *content* errors — the ones no syntax checker can catch. The first is **survivorship bias**, which you met as a flagged hazard in the Week 5 reading guides on Fama–French and momentum, and which we can now see exactly where it enters: at the merge.

State it in one sentence: **survivorship bias is the error of analyzing only the units that survived to the end of your sample, when survival is correlated with the outcome you care about.** Sam wants to know whether high book-to-market ("value") stocks beat the market. Suppose, the lazy way, he downloads the list of firms *trading today* and pulls their entire return history backward. Every firm in that list survived to today. The firms that went bankrupt, got delisted, or were acquired at a loss — the *failures* — are not in the list, because they are not trading today. He has accidentally conditioned his sample on success.

Why does this bias the answer, and which way? Failures are disproportionately firms that *fell* — often the distressed, high-book-to-market firms whose prices collapsed. By dropping them, Sam keeps the value firms that *recovered* and discards the value firms that died. His estimate of the value premium is inflated, possibly enormously, because he is measuring the return to *being a value firm that happened to survive*, which is not a strategy anyone could have followed in real time. The bias is a selection-on-the-outcome problem — exactly the threat the potential-outcomes lens of Week 3 trained you to smell — and it can manufacture a "premium" out of thin air.

The fix is conceptual before it is technical: **your sample must include every unit that existed at the time of the decision, including the ones that later died.** CRSP is built for this — it retains delisted securities and, crucially, records a **delisting return** (`dlret`) that captures the final, often catastrophic, return when a stock is removed from the exchange. The classic survivorship bug is to *drop* delisted firms (because their later rows are missing) instead of *incorporating the delisting return* and then letting them exit. In code, the smell test is simple: count your firms *per year*, not just in total.

```python
# Survivorship smell test: does the firm count only ever grow?
# A real CRSP universe has firms ENTERING (IPOs) and EXITING (delistings)
# every year. A survivorship-biased universe never loses anyone.
counts = panel.groupby("year")["permno"].nunique()
print(counts)
# Red flag: a monotonically increasing count, ending exactly at "today's"
# universe, with no exits -> you dropped the firms that died.
```

If firms only ever enter and never leave, you have a survivorship problem. A healthy financial panel *churns*: IPOs arrive, delistings depart, the count wobbles. Maya's HMDA work has a cousin of this bias — if she studies only lenders still operating today, she misses the subprime originators that failed in 2008, who were precisely the ones whose lending behavior the question is about.

---

## 7.4.4 Look-ahead bias and the point-in-time discipline

The second content error is the deadliest because it is the most seductive: **look-ahead bias**, using information in your analysis that *was not yet knowable* at the moment your strategy or decision would have acted. Your code can see the whole dataset at once; an investor in March 2015 could not see June 2015's data. If your merge accidentally lines up a future number with a past decision, you build a strategy that "works" only because it cheated.

The canonical source of look-ahead bias in finance is the **reporting lag on accounting data.** Compustat records a firm's fiscal-year financials with the **fiscal-period-end date** — say, fiscal year ending December 31, 2014. But that firm does not *file* its annual report (the 10-K with those numbers) on December 31. It files weeks or months later — the SEC allows large filers 60 days, smaller filers up to 90 — and the market cannot trade on numbers it has not seen. If Sam merges December 2014 book equity onto December 2014 returns and forms a portfolio, he is trading on data that did not exist yet. That is look-ahead, and it is precisely why the Week 5 Fama–French reading guide insisted on a lag.

The standard, conservative convention — the one Fama and French use and the one you should default to — is the **6-month Compustat lag**: assume accounting data for a fiscal year ending in calendar year $y$ becomes usable for portfolio formation only from the following **June 30** (i.e., June of year $y+1$). For a December fiscal-year-end, that is a six-month buffer, comfortably after even a late filer has reported. So fiscal-2014 book equity is matched to returns from **July 2015 through June 2016**. Six months is deliberately generous; it trades a little timeliness for the certainty that you never peek. The general principle is to construct, for every accounting variable, a **point-in-time** "available-as-of" date — the earliest date the number could have been *known* — and to merge on *that* date, never on the fiscal-period-end.

Here is the lag done explicitly, and verifiably, in code. The key move is to compute an `available_date` column and merge returns to fundamentals *on the availability date*, with an assertion that no return ever precedes the data it uses.

```python
import pandas as pd

# Compustat: fundamentals keyed by gvkey and FISCAL-YEAR-END date (datadate).
fund = compustat[["gvkey", "datadate", "book_equity"]].copy()

# Point-in-time availability: 6-month lag (Fama-French convention).
# Data for a fiscal year ending in calendar year y is usable from
# June 30 of year y+1 onward.
fund["available_date"] = (
    pd.to_datetime(fund["datadate"].dt.year.add(1).astype(str) + "-06-30")
)

# Merge-as-of: attach to each monthly return the MOST RECENT fundamental
# whose availability date is on or before the return month. merge_asof is
# the right tool: it joins on the nearest PRIOR key, never a future one.
fund = fund.sort_values("available_date")
rets = crsp_linked.sort_values("ret_date")          # monthly returns, has gvkey

panel = pd.merge_asof(
    rets, fund,
    left_on="ret_date", right_on="available_date",
    by="gvkey",
    direction="backward",            # only look BACKWARD in time -- no peeking
)

# Verification assertion: a fundamental is never used before it was available.
assert (panel["ret_date"] >= panel["available_date"]).all(), \
    "LOOK-AHEAD: a return uses accounting data dated after the return!"
```

`pd.merge_asof` with `direction="backward"` is the workhorse for point-in-time joins precisely because it *structurally cannot* attach a future record — it walks backward to the most recent available value. The `assert` at the end is not decoration; it is a tripwire. Run it on every build. A look-ahead bug is invisible in your results (it just makes them better) but it dies instantly against an explicit "no future data" assertion. Connect this back to Week 5: when the momentum reading guide warned you to skip the most recent month and to lag your signals, *this* is the machinery that enforces it. And connect it to measurement-error thinking from Week 2: a mis-dated regressor is a form of mismeasurement, except here the "noise" is not random — it is the future leaking into the past, which biases you in a predictable, flattering, and entirely fake direction.

---

## 7.4.5 Outliers: winsorizing, trimming, and when to do neither

Sam computes book-to-market and stares at the distribution. Most values sit between 0.2 and 2. But a handful are 400, and one is $-90$. These are **outliers**, and they are not necessarily errors — but they will dominate any mean, any OLS slope (recall from Week 1 and Week 2 that OLS minimizes *squared* error, so a single huge residual can swing $\hat{\beta}$), and any Sharpe ratio. You have to decide what to do, and "leave them and hope" is a decision too.

Where do extreme financial ratios come from? Three sources, and the source dictates the fix. (1) **Data errors** — a misplaced decimal, a units mismatch (thousands vs. millions), a stale CUSIP gluing the wrong firm's book value to a stock. These should be *found and fixed or dropped*, not statistically smoothed. (2) **Definitional artifacts** — a firm with near-zero or negative book equity produces a book-to-market that explodes or flips sign; the ratio is mathematically real but economically meaningless. These are usually *excluded by a stated rule* (e.g., "drop firm-years with negative book equity," a standard Fama–French screen). (3) **Genuine extreme values** — a real firm really is that distressed. These are *signal*, and throwing them away can itself bias you, because in finance the tails are where the action is.

For sources (2) and (3), the standard tool is **winsorizing**: instead of deleting extreme observations, you *cap* them at a percentile. Winsorizing at the 1st and 99th percentiles means every value below the 1st percentile is set *equal to* the 1st-percentile value, and every value above the 99th is set equal to the 99th-percentile value. The observations stay in your sample — you do not lose $N$ — but their leverage on the estimate is bounded. **Trimming** is the more aggressive cousin: you *delete* observations beyond the cutoffs rather than capping them, which does reduce $N$ and discards information. Winsorizing is usually preferred precisely because it keeps the row.

```python
def winsorize(s: pd.Series, lower=0.01, upper=0.99) -> pd.Series:
    """Cap a series at its lower/upper quantiles. Returns a NEW series."""
    lo, hi = s.quantile([lower, upper])
    return s.clip(lower=lo, upper=hi)

# Winsorize WITHIN each cross-section (by date), not pooled across all years:
# a 1999 outlier and a 2008 outlier should be judged against their own era.
analysis["bm_w"] = (
    analysis.groupby("ret_date")["bm"]
            .transform(lambda s: winsorize(s, 0.01, 0.99))
)
```

Three points of discipline that separate a defensible winsor from a fudge. First, **winsorize within the cross-section**, not pooled across the whole panel — as the `groupby("ret_date")` above does — so that "extreme" is judged relative to contemporaries, not relative to a different decade. Second, **state the cutoffs and apply them symmetrically and once**; 1%/99% is conventional, but the cardinal sin is *searching* over cutoffs until your t-stat clears 2. That is not cleaning; that is $p$-hacking with extra steps. Third — and this is the "when not to" — **do not winsorize the variable that is the whole point.** Priya studying catastrophe-insurance losses, or Devon studying crypto returns, lives in fat-tailed worlds where the extreme observations *are the phenomenon*. Winsorizing a catastrophe model's largest losses would erase the very risk being measured. The right move there is often a model built for fat tails (a log transform, a quantile regression, a robust estimator), not a cap that defines the problem away. Winsorize the *noise in your controls*; do not winsorize away your *subject*.

---

## 7.4.6 Missing data: why it is missing matters more than how much

Maya's HMDA file is the better teacher here, so we switch to her. The Home Mortgage Disclosure Act data records millions of mortgage applications, and many fields are missing: some applicants do not report income, race fields are blank for some channels, and certain variables (famously the credit score, as the whole Week 6 fair-lending arc hammered) are *never* present. Maya's instinct is to call `dropna()` and move on. **This is the single most common way to silently bias a study**, because the rows you drop are almost never a random sample.

The professional question is never "how much data is missing?" but "**why** is it missing?" There is a formal taxonomy, and you should know it by name. **Missing Completely At Random (MCAR):** missingness is independent of everything — a server randomly dropped some records. Here, dropping the missing rows (*listwise deletion*) loses precision but does not bias you. **Missing At Random (MAR):** missingness depends on *observed* variables — say, income is missing more often for a particular loan-purpose category that you *can* see. Here you can, in principle, correct using the observed variables. **Missing Not At Random (MNAR):** missingness depends on the *unobserved* value itself — applicants with the *lowest* incomes are the most likely to leave income blank. This is the dangerous one: the act of being missing carries information about the very number you wish you had, and no amount of cleverness with the observed columns fully fixes it. Dropping MNAR rows is selecting your sample on the outcome, the survivorship error wearing a different hat.

So what do you actually do? Two honest options, plus one rule.

**Listwise deletion** (drop any row with a missing value in a variable your regression uses) is fine *if* you have argued the missingness is plausibly MCAR or MAR-given-controls, *and* you report how many rows you lost and check that the survivors are not systematically different. **Imputation** (fill missing values with a model-based estimate — the column mean, a regression prediction, or multiple imputation) keeps your $N$ but injects assumptions, and a naïve mean-imputation distorts variances and correlations; it is a real tool but not a free lunch. Whichever you choose, the rule is absolute: **never silently drop.** Log it.

```python
# Missing-data discipline: measure, decide, and RECORD -- never silent.
required = ["loan_amount", "applicant_income", "action_taken"]

before = len(hmda)
miss_table = hmda[required].isna().mean().mul(100).round(2)
print("Percent missing by required field:\n", miss_table.to_string())

# Probe WHY income is missing: is it correlated with an observed field?
# (If denial rates differ sharply between missing- and present-income rows,
#  missingness is informative -> NOT MCAR; document and reconsider dropping.)
hmda["income_missing"] = hmda["applicant_income"].isna()
print(hmda.groupby("income_missing")["denied"].mean())

# Listwise deletion -- explicit, logged, and justified in the build log.
clean = hmda.dropna(subset=required).copy()
after = len(clean)
print(f"Listwise deletion dropped {before - after:,} rows "
      f"({(before-after)/before:.1%}); kept {after:,}.")
```

The `groupby("income_missing")["denied"].mean()` line is the one that earns its keep: if applications with missing income are denied at a wildly different rate than those with income reported, missingness is *not* random and dropping those rows changes the population you are studying. You then have to say so in the memo and decide deliberately. That is the difference between cleaning and hiding.

---

## 7.4.7 The build script: raw → intermediate → analysis, with row-count logging

Everything above is a decision. The final discipline is to make those decisions **reproducible and auditable**, which means they live in a *script*, not in the scrollback of a notebook you ran out of order. The organizing principle is a one-way pipeline through three stages, and you never edit a file in place:

- **`raw/`** — exactly what came off WRDS/EDGAR, never modified. This is your ground truth; if a build goes wrong you re-derive from here. (And per the CONVENTIONS, licensed CRSP/Compustat extracts stay read-only on GMU infrastructure, with the snapshot date pinned.)
- **`intermediate/`** — the linked, lagged, typed tables: CRSP joined to CCM, Compustat with availability dates, each saved (as Parquet, via `pyarrow`) so you can inspect them.
- **`analysis/`** — the single rectangular panel your regression consumes, one row per `(permno, month)`.

The non-negotiable feature is **row-count logging at every step**. Each transformation prints how many rows entered, how many left, and why the difference exists. This log *is* your audit trail; when a coauthor or a referee asks "where did the other 4,000 firm-months go?", you point at the log. A tiny logging helper makes this painless:

```python
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("build")

def step(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Log shape after a build step; return df unchanged for chaining."""
    log.info("[%-28s] rows=%9d  unique_firms=%7d",
             name, len(df), df["permno"].nunique())
    return df

# --- BUILD PIPELINE (each line is one auditable decision) ----------------
crsp   = step(load_parquet("raw/crsp_msf.parquet"),        "00 raw CRSP")
crsp   = step(apply_delisting_returns(crsp),               "01 + delisting ret")
linked = step(crsp.merge(ccm, on="permno", how="inner",
                         validate="many_to_one"),          "02 link CCM (m:1)")
linked = step(linked.query("@linked.ret_date.between("
                           "linkdt, linkenddt)").copy(),   "03 date-window filter")
panel  = step(pd.merge_asof(linked.sort_values("ret_date"),
                            fund.sort_values("available_date"),
                            left_on="ret_date", right_on="available_date",
                            by="gvkey", direction="backward"),
                                                           "04 merge_asof (6mo lag)")
panel  = step(panel.query("book_equity > 0").copy(),       "05 drop neg book eq")
panel["bm_w"] = winsorize_by_date(panel)
panel  = step(panel.dropna(subset=["ret", "bm_w"]).copy(), "06 listwise (ret,bm)")
panel.to_parquet("analysis/value_panel.parquet")
```

Running it produces a log that reads like the autobiography of your dataset:

```
[00 raw CRSP                  ] rows=  3 482 119  unique_firms=  24 188
[01 + delisting ret           ] rows=  3 482 119  unique_firms=  24 188
[02 link CCM (m:1)            ] rows=  3 105 442  unique_firms=  18 902
[03 date-window filter        ] rows=  2 988 310  unique_firms=  18 711
[04 merge_asof (6mo lag)      ] rows=  2 988 310  unique_firms=  18 711
[05 drop neg book eq          ] rows=  2 871 905  unique_firms=  18 433
[06 listwise (ret,bm)         ] rows=  2 640 117  unique_firms=  17 998
```

*(Illustrative counts; your numbers will differ by snapshot vintage. The point is the shape of the story, not the digits.)* Read it like a detective. Step 02 dropped about 5,000 firms with no Compustat link — expected (ADRs, funds), but you should confirm the *rate*. Step 03 trimmed a bit more — observations outside any valid link window, correctly removed. Step 05 dropped negative-book-equity firm-years per the stated screen. Step 06 is the listwise deletion, the largest single cut, and the one you must justify in the memo. Every number in that log is a sentence you can defend, and the gap between any two adjacent lines is a decision someone can question. **A build with no row-count log is a build with no audit trail, which is a build no one should believe — including you, three months from now.**

A final reproducibility note that ties back to CONVENTIONS §5: set a random seed wherever any step uses randomness (imputation, sampling), pin your data snapshot date in the script header, read secrets from environment variables, and make the whole thing runnable top to bottom on a fresh environment. A dataset you cannot rebuild from `raw/` with one command is not reproducible, and an irreproducible dataset is, for the purposes of credible empirical work, no dataset at all.

---

## 7.4.8 Putting it together: the panel is the argument's foundation

Step back. Sam started with two clean files and a simple question, and we have spent a chapter turning them into one panel. Along the way we made a dozen decisions: which `LINKTYPE` codes to trust, whether to keep delisted firms (yes — survivorship), what reporting lag to impose (six months — look-ahead), whether to winsorize book-to-market (yes, by date) and whether to winsorize Priya's catastrophe losses (no — that *is* the signal), how to handle Maya's missing income (probe it, then decide and log). None of these is "cleaning" in the janitorial sense. **Each one can change the sign of a result**, and a hostile referee — the imaginary one Week 5 taught you to keep in the room — will ask about every single one.

That is why this chapter sits where it does, between the *acquisition* of Chapter 7.2 and the *identification memo* of Chapter 7.5. The memo will argue that your design identifies a real effect. But identification assumptions are claims about *the data you built* — about *this* panel, with *these* firms, lagged *this* way, cleaned by *these* rules. If the panel is contaminated by survivorship or look-ahead, the cleverest identification strategy in the world is estimating an artifact. The build script is therefore not a preliminary to the analysis; it is the first chapter of the analysis, and the row-count log is its first table. Master it and you have a defensible foundation. Skip it and you have a number you cannot explain — which, in this field, is the same as no number at all.

---

## Your Turn

Open **`nb7.4`** (`notebooks/week-07/nb7.4-dataset-build-and-validation.ipynb`), the dataset-build and validation notebook. There you will assemble the value panel end to end: link CRSP to Compustat through the CCM table with `validate=` on every merge, impose the 6-month lag with `merge_asof` and prove it with the no-look-ahead assertion, run the survivorship per-year firm-count smell test, winsorize book-to-market by date, handle missing data with a logged listwise rule, and emit the full `raw → intermediate → analysis` build log. The "Your Turn" extension reruns the same machinery on a HMDA extract for Maya, where the missing-data taxonomy does the heavy lifting and there is no CCM to lean on — you build the crosswalk yourself.

Three questions to carry into the lab and the Chapter 7.5 memo:

1. **The match rate is a finding, not a footnote.** Suppose your CCM link matches only 72% of CRSP rows to a GVKEY. Before you analyze the 72%, name three distinct reasons a row might fail to link, and for each, say which direction (if any) it biases a value-premium estimate. When is a low match rate a bug in your code, and when is it an honest feature of the data?

2. **Look-ahead is invisible in your results.** A look-ahead bug *improves* every backtest statistic — higher mean return, higher Sharpe, tighter $t$-stat. Given that you cannot detect it by looking at the output, what *structural* checks (assertions, date audits, the choice of `merge_asof` direction) would you build into the pipeline so the bug cannot survive a clean run? Write the one assertion you would never ship without.

3. **Winsorize or not?** You are merging two studies into one build: Sam's value-premium panel (winsorize book-to-market) and Priya's catastrophe-insurance losses (do *not* winsorize the loss variable). State the principle that decides, in general, whether an outlier is noise to be capped or signal to be preserved — and apply it to a third case: Devon's daily crypto returns, where a single day can move 40%. Cap it, model it, or leave it, and defend the choice.
