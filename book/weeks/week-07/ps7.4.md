# PS 7.4 — A Reproducible Merged Analysis Dataset, With Diagnostics

**Course:** 8-Week Empirical Finance Camp · Week 7 · Problem Set 7.4
**Covers:** Ch 7.4 (Building the Analysis Dataset) and the companion notebook nb7.4, with backward callbacks to Ch 7.2 (your raw pulls and data cards), Ch 7.3 (the pre-analysis plan you wrote), and forward into Ch 7.5 (the identification memo your panel must support). Pulls in the survivorship and look-ahead hazards first flagged in the Week 5 Fama–French / momentum reading guides, the missing-data taxonomy from the Week 6 fair-lending arc, and the data-snooping discipline from Week 1.
**Methods allowed:** only what is built through Ch 7.4 and nb7.4 — a one-way `raw → intermediate → analysis` pipeline; `pd.merge` with `validate=` (`one_to_one` / `many_to_one` / etc.) and `indicator=True`; a date-aware crosswalk respecting `LINKTYPE` / `LINKPRIM` / `[LINKDT, LINKENDDT]`; `pd.merge_asof(direction="backward")` with a point-in-time `available_date`; the per-year firm-count survivorship smell test; winsorizing-by-cross-section; a logged missing-data rule with a `groupby` missingness probe; the `step()` row-count logger; and `pd.concat` over a list (never `df.append`). You do **not** need any regression results yet — that is Ch 7.5. You need a *panel a regression could trust*.

**Total: 100 points.** Point values are stated per problem. This is a **build-and-document** problem set, not a by-hand-arithmetic one: most of your grade is a *script that runs* and a *short diagnostics report that defends it*. A panel that produces numbers with no audit trail earns roughly half credit, because the audit trail *is* the skill we are grading — a number you cannot explain is, in this field, the same as no number at all. Solutions are in Appendix E (`E-w7-ps7.4-solutions.md`), which shows one fully worked exemplar build for Sam's value panel; build *your own* project's panel before you look.

**The standing rule on data.** This sheet is built around *your own Week-7 project* — the question you sharpened in Ch 7.1, the sources you pulled and documented in Ch 7.2, the design you pre-registered in Ch 7.3. Wherever a number, match rate, or row count appears in this sheet or its solutions, it is **illustrative** — clearly labeled, internally consistent, chosen to make the story legible — and is **not** a real figure off CRSP, Compustat, HMDA, EDGAR, or PatentsView. Your real diagnostics will differ by snapshot vintage; report *your* numbers, and label any worked example you borrow from the solutions as illustrative. And the hard rule from CONVENTIONS §5 stands over everything: **licensed raw data (CRSP, Compustat, IBES) never leaves GMU infrastructure and is never committed to git** — your repository holds the *code* that builds the panel and the *log* of what it did, not the licensed bytes. Pin your snapshot date in the script header.

**Pick your project once, and stay with it.** Every problem below says "your panel." Use the same project throughout so the build composes into one deliverable:

- **Sam** — CRSP monthly returns × Compustat fundamentals via the CCM link; unit-period = `(permno, month)`; the value-premium build is the chapter's running example.
- **Maya** — HMDA applications (public); unit = loan application; *no CCM to lean on* — she builds a lender/geography crosswalk herself, and the missing-data taxonomy does the heavy lifting.
- **Priya** — Compustat fundamentals × 10-K climate-language scores from EDGAR; unit-period = `(gvkey, fiscal-year)`; crosswalk is CIK ↔ GVKEY.
- **Devon** — on-chain / exchange price series × S-1 disclosure features; unit-period = `(token, day)`; fat-tailed outcome (the winsorize "do *not*" case).
- **Leah** — PatentsView patent counts (public) × CRSP/Compustat financials; unit-period = `(firm, year)`; crosswalk is assignee ↔ PERMNO/GVKEY through CIK or a researched link.

If you have not yet pulled real data, build on the **seeded synthetic fallback from nb7.4** (the offline CRSP/Compustat/CCM stand-ins) so the pipeline runs end-to-end; say so explicitly in your header and treat the diagnostics as illustrative.

---

## Problem 1 — The crosswalk and the merge contract (18 points)

Before a single row is joined, write down the *contract* of your merge. This is the Ch 7.4.1–7.4.2 discipline: name the identifiers, the crosswalk, and the cardinality you are *asserting* — not hoping.

**(a) (5 pts)** Name, for your project, the two (or more) raw tables you are joining, the **identifier** each uses, and why you cannot simply join on a human-readable name or a ticker. State the **crosswalk** that connects them (the CCM `ccmxpf_lnkhist` for Sam/Priya/Leah's CRSP–Compustat leg; a CIK↔GVKEY link for EDGAR work; a self-built lender/geography key for Maya; an assignee link for Leah's patents). In two sentences, give the concrete failure that a naive name/ticker join would cause — the Chrysler-vs-Citigroup pathology, in your own data's terms.

**(b) (4 pts)** If your crosswalk is *time-varying* (CCM, or any link with validity windows), state the four things the link carries that you must respect — the link-quality codes you keep (`LINKTYPE in ('LU','LC')`), the primary-link flag that resolves multiple share classes (`LINKPRIM in ('P','C')`), and the validity window `[LINKDT, LINKENDDT]`. Explain in one sentence *why a crosswalk cannot be collapsed to a plain `{key: key}` dictionary* — i.e., why the date window is the whole game. (Maya/Devon, who lack a vendor link: state instead the two fields your self-built key joins on and the one ambiguity that makes it not a clean dictionary — e.g., a lender ID that was reassigned, or a ticker that changed.)

**(c) (5 pts)** Write the **merge contract** as a one-line assertion *per join* in your pipeline. For each merge, state: left table, right table, join key(s), `how=`, and the exact `validate=` value you will pass, plus the cardinality claim in plain English. For example, for Sam's link step:

> CRSP returns (left, many rows per PERMNO) ⋈ CCM link (right, one valid link row per PERMNO-window) on `permno`, `how="inner"`, `validate="many_to_one"` — *asserting* many return-months map to at most one link.

Do this for **every** merge in your build (you will have at least two: the identifier link, and the fundamentals/feature attach). Name which one is the riskiest if your cardinality assumption is wrong, and what a **many-to-many** join would do to it (the Cartesian-explosion reweighting).

**(d) (4 pts)** State the **match-rate** check you will run on the link step and *why you build with `how="left"` and `indicator=True` even if the final panel is an inner join.* Give the two lines of code that compute (i) the fraction of left rows that found a partner and (ii) the count of distinct left-keys that found *no* partner. Then state a **threshold for alarm**: at what match rate do you stop and investigate rather than analyze, and name two benign reasons a row legitimately fails to link in *your* data (e.g., ADRs / closed-end funds for CRSP; a lender outside your geography for Maya; a foreign filer with no GVKEY for Priya).

---

## Problem 2 — Survivorship: count the firms that vanished (16 points)

The first content error no syntax checker can catch (Ch 7.4.3). State it, demonstrate it, and prove your panel does not commit it.

**(a) (4 pts)** State survivorship bias in one sentence *for your project*: what is the unit that might have "died," what is the act of death (delisting, bankruptcy, a lender failing, a token delisting from the exchange, a firm ceasing to file), and *why is survival correlated with the outcome you care about* — i.e., which direction does dropping the dead bias your eventual estimate? (Sam: distressed high-book-to-market firms die, so dropping them inflates the value premium. Maya: subprime originators that failed in 2008 are exactly the lenders the question is about. Devon/Priya/Leah: state your own.)

**(b) (6 pts)** Run the **per-year (or per-period) unit-count smell test**. Produce `panel.groupby("year")[unit_id].nunique()` and show the series (a table or a small line plot). State the single diagnostic that distinguishes a healthy churning universe from a survivorship-biased one — *a healthy panel has units entering and exiting; a survivorship-biased one only ever grows and ends exactly at "today's" universe.* Report whether *your* counts churn, and quote two adjacent years where the count *falls* (the exits). If your raw pull cannot lose units, that is your red flag — diagnose it.

**(c) (3 pts)** Name the mechanical fix for *your* data. For CRSP-based projects, this is **incorporating the delisting return (`dlret`)** so a stock's final, often catastrophic, return is in the panel before the firm exits — *not* silently dropping delisted rows because their later months are missing. State, in code or prose, where in your pipeline the dead units' final observations enter, and what would go wrong if you dropped them instead. (Non-CRSP projects: state the analogous "keep the failure's last observation" move for your source.)

**(d) (3 pts)** Quantify the bias on a *toy* version (illustrative numbers, clearly labeled). Compute the mean outcome two ways — once on the full churning universe, once on the survivors-only subset — and report the gap and its sign. State the one sentence connecting this to the Week 3 potential-outcomes lens: *survivorship is selection on the outcome.*

---

## Problem 3 — Look-ahead and the point-in-time discipline (20 points)

The deadliest error, because a look-ahead bug *improves* every backtest statistic and is invisible in your results (Ch 7.4.4). Build the machinery that makes it impossible to ship.

**(a) (4 pts)** Identify, for *your* project, the variable that carries a **reporting lag** — the number that exists with a fiscal/period-end date but is not *knowable* until later. (Sam/Priya/Leah: Compustat fundamentals, filed weeks-to-months after fiscal-year-end. Maya: a HMDA field finalized only after the application year closes. Devon: an S-1 disclosure usable only from its filing date.) State the gap between the *period-end date* and the *availability date*, and the canonical bug: merging the period-end number onto a same-dated decision.

**(b) (5 pts)** Construct the **point-in-time `available_date`** column for that variable and state your lag rule explicitly. For Compustat the default is the **6-month Fama–French lag**: a fiscal year ending in calendar year $y$ is usable for portfolio formation only from **June 30 of year $y{+}1$**. Give the code that builds `available_date` and one worked example: "fiscal-2017 book equity → first usable on 2018-06-30 → matched to returns from July 2018 onward." Justify in one sentence why six months is *deliberately generous* (it trades a little timeliness for certainty you never peek).

**(c) (6 pts)** Do the **point-in-time merge** with `pd.merge_asof(..., direction="backward")`, joining each decision-date observation to the *most recent* feature whose `available_date` is on or before it. Give the code. Then state, in one sentence, *why `merge_asof` with `direction="backward"` is the right tool and a plain `merge` is not* — it structurally cannot attach a future record; it walks backward to the most recent available value.

**(d) (5 pts)** Write the **no-look-ahead tripwire** — the assertion you would never ship without:

```python
assert (panel["decision_date"] >= panel["available_date"]).all(), \
    "LOOK-AHEAD: a decision uses data dated after the decision!"
```

State precisely *why this assertion is load-bearing and cannot be replaced by eyeballing the results* (a look-ahead bug raises your mean return, Sharpe, and $t$-stat — you cannot see it in the output, only in the dates). Then, as a deliberate failure demo (this is nb7.4 "Your Turn" #2): say what happens if you flip the merge to `direction="forward"`, and confirm the assertion *fires*. Report the line that fired and the count of violating rows on a toy run (illustrative).

---

## Problem 4 — Winsorize where justified (and where not) (14 points)

Outliers are decisions, not nuisances (Ch 7.4.5). The grade here is for the *judgment*, applied symmetrically and once — not for a cap that flatters a $t$-stat.

**(a) (5 pts)** For *your* project's key variable(s), classify each extreme-value source you expect among the three from Ch 7.4.5: **(1) data errors** (decimal/units/stale-link), **(2) definitional artifacts** (e.g., near-zero or negative book equity exploding a ratio), **(3) genuine extreme values** (a real, distressed unit). State the fix each source demands — fix-or-drop errors; exclude artifacts by a *stated rule* (e.g., "drop firm-years with negative book equity," a standard Fama–French screen); and *keep* genuine extremes unless you have a reason. Identify which of your variables, if any, has its **negative-book-equity-style screen**, and state that screen.

**(b) (5 pts)** Winsorize the variable that *should* be winsorized, **within the cross-section** (by date/period), at stated symmetric cutoffs (1%/99% is conventional). Give the code (a `groupby(period).transform(...)` over a `clip`-to-quantiles helper), and confirm two properties: (i) $N$ is **preserved** (winsorizing caps, it does not delete — contrast with trimming, which would reduce $N$), and (ii) the max/min moved to the cutoff value. Report the before/after max on a toy run (illustrative). State the cardinal sin you are *not* committing: searching over cutoffs until significance appears — that is $p$-hacking with extra steps.

**(c) (4 pts)** State the **"when not to."** Name one variable in your project (or in a campmate's: Priya's catastrophe losses, Devon's daily crypto returns) where the extreme observations *are the phenomenon*, and winsorizing would *erase the signal you are measuring*. State the general principle that decides noise-to-cap vs. signal-to-preserve, and the right alternative move for the fat-tailed case (a log transform, a quantile/robust estimator, a model built for fat tails — *not* a cap that defines the problem away). One sentence: *winsorize the noise in your controls; do not winsorize away your subject.*

---

## Problem 5 — Missing data: why it is missing, not how much (16 points)

The single most common way to silently bias a study is `dropna()` on a non-random subset (Ch 7.4.6). Measure, probe, decide, and **log** — never silent.

**(a) (4 pts)** List the variables your regression will *require*, and produce the **percent-missing table** for them on your raw panel (`df[required].isna().mean()*100`). Report the figures (illustrative if synthetic). For the one field with the most missingness, name which **MCAR / MAR / MNAR** mechanism you suspect and *why* — the question is never "how much is missing?" but "*why* is it missing?"

**(b) (5 pts)** Run the **missingness probe** that earns its keep: create an `is_missing` flag on your worst field and compare a downstream quantity across the present-vs-missing groups (`df.groupby("x_missing")[outcome].mean()`). For Maya this is the canonical one — `groupby("income_missing")["denied"].mean()` — and if the denial rate differs sharply, missingness is **informative (not MCAR)** and dropping those rows changes the population. Report your two group means and state the verdict: is your missingness plausibly MCAR/MAR-given-controls, or MNAR? (nb7.4's synthetic build is MCAR-by-construction — returns blanked uniformly at random — so the gap is near zero; the "Your Turn" #1 has you rebuild it **MNAR** so the gap widens. Say which regime *your* data is in.)

**(c) (4 pts)** Choose and **justify** your handling — **listwise deletion** or **imputation** — given your part-(b) verdict. State the absolute rule (*never silently drop; log it*) and give the logged-deletion code that prints rows-before, rows-after, the count and percent dropped. If you impute, name the method and the one cost it injects (naïve mean-imputation distorts variances and correlations; it is a real tool, not a free lunch), and set a seed if any randomness is involved.

**(d) (3 pts)** In two sentences, connect MNAR-dropping back to **survivorship** (Problem 2): both are *selection on the outcome*, the same error wearing two hats. State what you will write in your Ch 7.5 memo about the rows you dropped — specifically, the check that the survivors are not systematically different from the dropped on observables you *can* see.

---

## Problem 6 — The build script and the row-count audit trail (16 points)

Everything above is a decision; the final discipline is making the decisions **reproducible and auditable** (Ch 7.4.7). The deliverable is a script and the log it emits.

**(a) (6 pts)** Assemble your full pipeline as a single runnable script with the three-stage, one-way structure: **`raw/`** (untouched, the ground truth, licensed bytes never committed), **`intermediate/`** (linked, lagged, typed tables, saved as Parquet), **`analysis/`** (the one rectangular panel, one row per unit-period). Instrument **every** transformation with the `step()` row-count logger so each line prints rows-in, rows-out, and unique-units. Submit the script. It must satisfy the CONVENTIONS §5 hygiene checklist (see the submission checklist below): `validate=` on every merge, `.copy()` after every slice you then modify, **no chained-index assignment**, **no `df.append`** (build a list and `pd.concat` once), secrets via env vars, a pinned snapshot date in the header, and a set seed wherever randomness enters.

**(b) (5 pts)** Run it and paste the **row-count log** — the autobiography of your dataset. It should read like the chapter's example: `00 raw → 01 +delisting → 02 link → 03 date-window → 04 merge_asof lag → 05 screen → 06 winsorize → 07 listwise`. For **each adjacent pair of lines**, write one sentence naming the decision that caused the row change and whether the magnitude is *expected* — e.g., "step 02 dropped ~5,000 firms with no Compustat link (expected: ADRs, funds; confirm the *rate*)"; "step 07 listwise deletion is the largest single cut and the one I must justify in the memo." (Illustrative counts are fine if synthetic; label them.)

**(c) (5 pts)** Produce the **summary-statistics table** for your final analysis panel: for each key variable, $N$, mean, SD, min, p25, median, p75, max (a one-liner: `panel[keys].describe(percentiles=[.25,.5,.75]).T`). State two sanity checks the table must pass — e.g., the winsorized variable's min/max sit at the cross-sectional caps (Problem 4), $N$ matches the final log line (Problem 6b), no impossible values (a negative count, a return below $-100\%$), and the unit-period key is unique (`panel.duplicated(subset=key_cols).sum() == 0`). Report whether your panel passes.

---

## Submission checklist (graded as part of the problems above)

Tick every box; an unticked box is points off on the problem it belongs to.

- [ ] **One script**, runnable top-to-bottom on a fresh `python=3.11` env, that rebuilds the panel from `raw/` with one command (Ch 7.4.7 / CONVENTIONS §5).
- [ ] **`validate=`** passed on *every* `merge` (P1, P6a); the riskiest cardinality named (P1c).
- [ ] **Match-rate** computed with `how="left"` + `indicator=True`, with an alarm threshold and benign-failure reasons (P1d).
- [ ] **Per-year unit-count** churns (entries *and* exits); delisting/failure last-observation incorporated (P2).
- [ ] **`available_date`** + `merge_asof(direction="backward")` + the **no-look-ahead assertion** that you ran and that *passed* (P3); the `direction="forward"` failure demo shown to *fire* it (P3d).
- [ ] **Winsorize** by cross-section at stated symmetric cutoffs, $N$ preserved; the **do-not-winsorize** case named (P4).
- [ ] **Missing-data**: percent-missing table, the `groupby` missingness probe, a *logged* (never silent) handling rule with rows-dropped count (P5).
- [ ] **Row-count audit trail** from `step()`, every adjacent gap explained (P6b).
- [ ] **Summary-statistics table** with passing sanity checks; **unit-period key is unique** (P6c).
- [ ] **No** `df.append`, **no** chained-index assignment, **no** committed licensed bytes, **no** hard-coded secrets; **pinned snapshot date** in the header; **seed set** if randomness enters (CONVENTIONS §5).
- [ ] Every diagnostic number labeled **real** (your snapshot, vintage pinned) or **illustrative** (synthetic / borrowed from the solutions).

**Point recap.** P1 (18) + P2 (16) + P3 (20) + P4 (14) + P5 (16) + P6 (16) = **100**. The two heaviest problems — the merge contract (P1) and look-ahead (P3) — are heaviest on purpose: a cardinality bug or a look-ahead leak invalidates the panel no matter how clean the rest is.

---

*End of PS 7.4. When your script runs clean and your report defends every line of the log, check yourself against `book/appendices/E-solutions-manual/E-w7-ps7.4-solutions.md`, which works one complete exemplar (Sam's value panel) end to end — the merge contract, the match-rate table, the survivorship smell test, the no-look-ahead assertion, the winsorize, the missing-data probe, the full `raw → analysis` audit trail, and the summary-stats table — at the A-grade standard, with every number flagged illustrative. The full machinery lives in `notebooks/week-07/nb7.4-dataset-build-validation.ipynb` (`nb7.4`), where `validate=` catches a Cartesian explosion red-handed, the look-ahead assertion holds over the whole panel and then fires when you flip `merge_asof` to `forward`, and the per-year firm count churns the way a real universe does. The panel you build here is the foundation the Ch 7.5 identification memo stands on: if it is contaminated by survivorship or look-ahead, the cleverest identification strategy in the world is estimating an artifact.*
