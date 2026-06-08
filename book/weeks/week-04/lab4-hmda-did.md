# Lab 4 — A Clean DiD on HMDA + a State Policy Shock

This is the capstone of Week 4, and it is the first time in the camp you will point the causal-inference machinery at a *real* fair-lending dataset that millions of mortgage applications actually live in. Chapter 4.1 built difference-in-differences from four cell means up to the two-way fixed-effects regression and the event study, and it left you with one sentence underlined three times: parallel trends is an assumption about a counterfactual, so it can be *refuted* by a pre-trend but never *confirmed* by one. Chapter 4.2 then showed that the very TWFE regression you trust in the clean $2\times 2$ becomes a contaminated weighted average — sometimes even the wrong sign — the moment treatment timing is staggered and effects are dynamic, and it handed you the cure: Callaway and Sant'Anna's group-time ATTs, estimated against *clean* (never- or not-yet-treated) controls and aggregated on purpose.

In this lab you put those two chapters to work on the dataset Maya has been circling since Week 1: the **Home Mortgage Disclosure Act (HMDA) Loan Application Register (LAR)** — the public record of nearly every mortgage application filed in the United States, the same family of data that Prof. Gao and his coauthor used to ask whether same-sex couples were treated differently when they applied to borrow (Gao & Sun, 2019, *PNAS*). You will build a county-year panel of mortgage *denial rates*, define treatment by a **state-level fair-lending regulatory change** that different states adopt in different years (staggered adoption — exactly the Chapter 4.2 setting), and run the full pipeline: TWFE first (so you can feel *why* it is suspect here), then the event study to inspect the pre-trends, then Callaway–Sant'Anna with clean controls to get an honest number. You will stress the parallel-trends assumption deliberately, the way a regulator or a referee would.

The lab gives you **two paths**, and you should read both even if you only run one:

- **Path A — real HMDA.** The public CFPB HMDA Data Browser API and the FFIEC bulk files. You will see the exact query pattern and the schema you get back, and how to aggregate the raw application-level register up to a county-year panel of denial rates. We do *not* fabricate specific HMDA numbers — the real register is enormous and its values are what they are — so Path A is presented as a reproducible *recipe* you can run on the camp container against a pinned data vintage.
- **Path B — synthetic fallback.** A self-contained, seeded, synthetic county-year panel that *looks* like aggregated HMDA (a denial-rate outcome, states adopting a policy in staggered years) but is built with a **known** treatment effect. This block runs anywhere — no credentials, no network — and lets you run the entire event-study + Callaway–Sant'Anna pipeline and *recover the effect you planted*, confirming the estimator works before you trust it on data whose truth you cannot see.

The discipline this lab drills is the one the whole week has been building toward and the one Lab 3 stated as a slogan: **when you are unsure whether a tool does what it claims, build a universe where you know the truth and check.** Path B is that universe; Path A is the messy world you check it against. A causal estimate on real HMDA is only as trustworthy as your demonstration, on synthetic data, that the same code recovers a known answer.

---

## Learning goals

By the end of this lab you will be able to:

1. **Pull and aggregate** real HMDA LAR data from the CFPB Data Browser API into a reproducible county-year (or tract-year) panel of denial rates, pinning a data vintage and respecting the register's size.
2. **State a fair-lending DiD design** in full empirical-spec discipline (CONVENTIONS §4): outcome, treatment, controls, fixed effects, clustering, sample, and — the load-bearing line — the identifying assumption in one sentence.
3. **Build a staggered synthetic panel** with a *known* dynamic treatment effect, so you can audit every estimator against ground truth.
4. **Run static TWFE** and explain, with the Chapter 4.2 mechanism in hand, *why* its single coefficient is biased/attenuated under staggered adoption with dynamic effects — and confirm the attenuation in numbers.
5. **Estimate and read an event study** — leads as the pre-trend check, lags as the dynamic effect — and stress parallel trends by dialing a differential pre-trend into the treated states and watching the leads tilt.
6. **Estimate Callaway–Sant'Anna group-time ATTs** with clean (never-treated) controls using the `differences` package, aggregate to an event study and a single overall ATT, and verify it recovers the planted effect where TWFE could not.
7. **Connect the design to fair lending** — what a denial-rate gap does and does not establish, and why a clean design (per Gao & Sun, 2019) is what turns "it looks unfair" into a measurement a skeptic must take seriously.

---

## Setup

Per CONVENTIONS §5, every code block runs end-to-end on a fresh environment. Create and activate a conda environment, then install what this lab needs. The two estimators that matter are `pyfixest` (for fast TWFE and the naive event study) and `differences` (the Python implementation of Callaway–Sant'Anna's group-time ATTs, used exactly as in nb4.2). Path A also needs `requests` and `pyarrow`.

```bash
conda create -n week04-lab python=3.11 -y
conda activate week04-lab
pip install numpy "pandas>=2.2" scipy statsmodels pyfixest differences requests pyarrow matplotlib
```

Open `notebooks/week-04/lab4-hmda-did.ipynb` (or a script) and start every run with the same header. Two reproducibility rules you will follow without exception, as in every lab:

- **Pin the seed.** Use `numpy`'s modern generator, `rng = np.random.default_rng(SEED)`, never the legacy global `np.random.seed`.
- **Draw all randomness from that one `rng`.** A single source of randomness makes the synthetic panel replayable bit-for-bit.

```python
import matplotlib
matplotlib.use("Agg")          # headless: render figures to buffers, not a screen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pyfixest as pf
from differences import ATTgt   # Callaway-Sant'Anna group-time ATT (differences 0.3.0)

SEED = 20260528                # any fixed integer; write it down
rng = np.random.default_rng(SEED)
```

One honest note before you start. The synthetic panel (Path B) has random noise in it, so the recovered effect will not equal the planted effect to infinitely many decimals — it will land *close*, within sampling error, which is exactly what "the estimator works" means for a noisy dataset. Reruns with the *same* seed are bit-for-bit identical; the numbers quoted below are what `SEED = 20260528` produces. The point of Path B is not to hit a magic number but to watch the *clean* estimator land near the truth while the *contaminated* one (TWFE) sits visibly short of it.

---

## Path A — Real HMDA from the CFPB Data Browser

You do not have to run Path A to complete the lab — Path B is self-contained — but you should understand it, because this is how you would build the panel for Capstone 1 (*Fair Lending on HMDA*). HMDA LAR is **free, public** data published by the FFIEC and the CFPB: under the Home Mortgage Disclosure Act, most mortgage lenders must report nearly every application they receive, with the action taken (originated, approved-not-accepted, denied, withdrawn), the loan amount, the property location (state, county, census tract), and applicant demographics. It is one of the largest public microdatasets in U.S. finance — tens of millions of records per year — which is the first practical fact that shapes everything you do with it.

### A.1 Pin a vintage, and know the size

**Pin the data vintage first.** HMDA is revised: a given application year is published, then re-published with corrections, and the schema has changed across reform years (the 2018 expansion under Dodd-Frank added many fields). Any reproducible pull must state which year and which snapshot it used. For this lab we pin the **2018–2022 LAR, as published in the CFPB Data Browser snapshot current as of the camp container build** — record that string in your notebook. `[CHECK]` — confirm the exact snapshot date on the container before you cite a number from it; the API serves whatever vintage CFPB currently hosts, and you must not present a figure without naming the vintage it came from.

The register is too large to pull whole — a single year's nationwide LAR is multiple gigabytes. **Never download the full national file to a laptop.** Two disciplined options:

1. **Filtered API pulls** (good for a handful of states): the CFPB Data Browser API lets you request only the rows you need, filtered by state and year, and even pre-aggregated.
2. **FFIEC bulk files** (good for the whole country): the FFIEC publishes per-year pipe-delimited bulk LAR files; download once to the container's read-only data area, then aggregate with `pyarrow`/`pandas` in chunks. The camp container mirrors these so you are not re-downloading gigabytes.

Either way, the rule from CONVENTIONS §5 applies: large/licensed-scale data stays on GMU infrastructure (the Hopper cluster or the container's data mount), and you aggregate *down* to a county-year or tract-year panel before doing anything else.

### A.2 The Data Browser API query pattern

The CFPB HMDA Data Browser exposes an HTTP API that returns either raw records or server-side aggregations. For building a panel, the **aggregation endpoint** is what you want: ask CFPB to count actions by the dimensions you care about, so you never move the microdata at all. The pattern is a base URL plus query parameters naming the years, the states, and the variables to group by and to break out.

```python
import requests

# CFPB HMDA Data Browser aggregation endpoint (public, no key required).
# We pin years and a small set of states, and ask the server to AGGREGATE for us
# by state x action_taken, so we never pull the multi-GB microdata down.
HMDA_AGG = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"

def fetch_hmda_state_year(states, years):
    """Pull server-side action-taken counts by state and year from the CFPB API.
    Returns a tidy DataFrame. NOTE: confirm the live schema against the API docs for
    your pinned vintage -- CFPB has revised parameter names across releases.  [CHECK]"""
    frames = []
    for yr in years:
        params = {
            "years": yr,                      # pinned vintage year
            "states": ",".join(states),       # e.g. ["VA","MD","NC"]
            "actions_taken": "1,3",           # 1 = loan originated, 3 = application denied
        }
        r = requests.get(HMDA_AGG, params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()                    # {"aggregations": [{...}, ...]}
        df = pd.json_normalize(payload["aggregations"])
        df["year"] = yr
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

# Example (run on the container, against the pinned vintage):
# raw = fetch_hmda_state_year(["VA", "MD", "NC", "SC", "GA"], years=range(2018, 2023))
```

The **expected schema** of the aggregation response is a small table with one row per (state, year, action-taken) cell and a count, roughly:

| field | meaning |
|---|---|
| `state` | two-letter state code |
| `actions_taken` | HMDA action code (1 = originated, 3 = denied, …) |
| `count` | number of applications in that cell |
| `year` | the pinned vintage year (added by us) |

For a finer panel — county-year or tract-year, which is what you actually want for a DiD with many units — add `counties` or geographic group-by parameters to the query, or pull filtered raw records and aggregate locally. The county identifier in HMDA is the 5-digit **FIPS** code; the tract identifier is the 11-digit census-tract code. **Confirm the exact parameter names against the live API docs for your pinned vintage** — CFPB has renamed fields across releases, so the snippet above is the *pattern*, not a guaranteed-stable contract. `[CHECK]`

### A.3 From counts to a denial-rate panel

Whatever the geography, the outcome you build is the same. The **denial rate** in a (geography, year) cell is denied applications divided by applications that got a decision (originated + denied, optionally including approved-not-accepted), expressed in percentage points:

```python
def denial_rate_panel(raw, geo="state"):
    """Collapse action-taken counts to a denial-rate panel: denials / (originations + denials)."""
    wide = (raw.pivot_table(index=[geo, "year"], columns="actions_taken",
                            values="count", aggfunc="sum")
               .rename(columns={1: "originated", 3: "denied"})
               .fillna(0.0))
    wide["apps_decided"] = wide["originated"] + wide["denied"]
    wide = wide[wide["apps_decided"] >= 100]              # drop thin cells (noisy rates)
    wide["denial_rate"] = 100.0 * wide["denied"] / wide["apps_decided"]
    return wide.reset_index()[[geo, "year", "denied", "apps_decided", "denial_rate"]]
```

Two practical cautions that separate a careful HMDA panel from a sloppy one. First, **thin cells are noise**: a rural county with 40 applications has a denial rate that swings wildly year to year; filter out cells below a minimum application count (above we use 100) so your panel is not dominated by sampling noise in tiny geographies. Second, **the denominator is a choice you must state**: "denied / (originated + denied)" excludes withdrawn and incomplete applications, which is defensible, but a referee will ask, so write it into your spec. The denial rate is a coarse outcome — it does not, by itself, separate discrimination from differences in applicant creditworthiness (that is the whole subtlety of Week 2's OVB chapter and of the fair-lending literature). It is the *starting* outcome for a design that will lean on a policy shock, not the final word.

### A.4 Defining the treatment: a state fair-lending regulatory change

The design needs a **treatment**: a state-level regulatory change, adopted by different states in different years, that plausibly affects denial rates through the fair-lending channel. Real examples of the *kind* of shock you would use: a state adopting (or strengthening) a fair-lending examination regime for state-chartered lenders, a state anti-discrimination statute extending protected classes in credit, or a state-level CRA-style community-reinvestment obligation. You would encode, for each state, the **adoption year** $G_i$ (the calendar year the rule first binds), with never-adopters coded as missing — exactly the cohort structure Chapter 4.2 and the `differences` package expect.

You build that policy table yourself, by hand, from primary sources (statute effective dates, regulator announcements), and you **cite each adoption date** — this is the empirical-spec discipline applied to the treatment definition. For the lab we do not assert specific real adoption years (those are a research task for the capstone, and asserting them here without verification would violate CONVENTIONS §6). Instead, Path B *plants* a clean staggered adoption pattern so you can run and validate the pipeline; on real HMDA you would swap in your verified, cited policy table and run the identical code.

> **The real-data spec, named in full (CONVENTIONS §4, extended per Ch 4.2 §6).** **Outcome** = county-year mortgage denial rate (pp). **Treatment** = state fair-lending regulatory change, staggered adoption year $G_i$ per state. **Controls** = none in the baseline (or covariate-conditional parallel trends via the doubly-robust option). **Fixed effects** = county and year, absorbed inside the group-time estimator. **Clustering** = by state (the unit of treatment — BDM, Ch 4.1 §7). **Sample** = counties in the in-scope states over the pinned vintage years, cells with ≥100 decided applications. **Control group** = never-adopting states (clean throughout). **Aggregation** = event-time average of group-time ATTs, cohort-size weighted. **Identifying assumption (one sentence):** absent the regulation, each adopting cohort's county denial rates would have moved parallel to the never-adopting states' — assumed per cohort, not tested.

---

## Path B — The synthetic fallback (runs anywhere)

Now the universe where you know the truth. Path B builds a county-year panel that mimics aggregated HMDA — a denial-rate outcome, counties nested in states, states adopting a fair-lending policy in staggered years — but with a **planted, dynamic treatment effect**. Because you built it, you know the answer, and you can check whether the event-study + Callaway–Sant'Anna pipeline recovers it. Everything in Path B runs with no network and no credentials.

### Step 1 — Build the synthetic county-year HMDA-like panel

**What to do.** Construct 96 counties (8 counties in each of 12 states), observed 2012–2023. Three waves of states adopt the fair-lending policy — in 2016, 2018, and 2020 — and three states never adopt (the clean controls). The policy **lowers** denial rates, and the effect **builds** with event time: at event time $e\ge 0$ (years since adoption), the per-period effect is $(e+1)\times(-0.40)$ percentage points — $-0.40$ in the adoption year, $-0.80$ the next year, and so on. This is the Chapter 4.2 recipe exactly: *staggered timing plus a dynamic effect*, the combination that breaks TWFE. We add fixed county levels, a common downward drift (denial rates fell broadly over the 2010s), and Gaussian noise — none of which changes the lesson, all of which makes the contrast realistic and the parallel-trends assumption hold *in expectation*.

**Code skeleton.**

```python
YEARS = list(range(2012, 2024))          # 12 HMDA vintages
N_STATES = 12
COUNTIES_PER_STATE = 8                    # 96 counties total

# Staggered adoption: three treated waves + a never-adopting block.
adopt_year = {
    **{s: 2016 for s in range(0, 3)},     # wave 1
    **{s: 2018 for s in range(3, 6)},     # wave 2
    **{s: 2020 for s in range(6, 9)},     # wave 3
    **{s: np.inf for s in range(9, 12)},  # never-adopters (clean controls)
}

TRUE_PER_PERIOD = -0.40                    # policy LOWERS denial rate; effect BUILDS with event time

def event_effect(e):
    """Per-period treatment effect at event time e: (e+1)*(-0.40) for e>=0, else 0."""
    return (e + 1) * TRUE_PER_PERIOD if e >= 0 else 0.0

rows = []
for s in range(N_STATES):
    g = adopt_year[s]
    state_level = rng.normal(11.0, 1.5)                 # baseline denial rate varies by state
    for c in range(COUNTIES_PER_STATE):
        county_level = state_level + rng.normal(0.0, 0.8)   # fixed county heterogeneity
        for t in YEARS:
            common_trend = -0.10 * (t - 2012)               # denial rates drift DOWN everywhere
            treated = (g != np.inf) and (t >= g)
            eff = event_effect(t - g) if (g != np.inf) else 0.0
            denial = county_level + common_trend + eff + rng.normal(0.0, 0.5)
            rows.append({
                "county": f"s{s:02d}_c{c}", "state": f"S{s:02d}", "year": t,
                "G": (np.nan if g == np.inf else float(g)),  # never-treated -> NaN (differences convention)
                "D": int(treated), "denial_rate": denial,
            })
panel = pd.DataFrame(rows)

# The HONEST TARGET: mean of the TRUE effects over all treated county-year cells.
tr = panel.loc[panel["D"] == 1].copy()
true_mean_att = (((tr["year"] - tr["G"]) + 1) * TRUE_PER_PERIOD).mean()

print(f"Panel: {panel['county'].nunique()} counties x {panel['year'].nunique()} years = {len(panel)} rows")
print(f"True mean ATT over treated cells = {true_mean_att:+.4f} pp")
```

**What to expect.** A 1,152-row panel and a true mean ATT of about **$-1.49$ pp** (averaging the planted effects over every treated county-year). Hold that number: it is the truth every estimator below is chasing. Notice the cohort coding — never-adopters carry `G = NaN`, which is exactly the convention `differences.ATTgt` reads as "never-treated, eligible as a clean control."

**Reflection.** Point to the line that creates the staggered timing (`adopt_year`) and the line that creates the *dynamic* effect (`event_effect`). Chapter 4.2 said TWFE breaks only when *both* are present. If you made `event_effect` return a constant $-1.5$ regardless of $e$, which of the two crisis ingredients would you have switched off, and what would you predict happens to TWFE's bias?

### Step 2 — Inspect the panel and the identification argument

**What to do.** Before estimating anything, *look* at the design and state the identification argument out loud — this is the habit CONVENTIONS §4 enforces and the one that catches bad designs before the regression does. Tabulate counties per cohort and plot the raw cohort means over time.

```python
n_by_cohort = panel.drop_duplicates("county").groupby("G", dropna=False).size()
print("Counties per cohort (NaN = never-adopting clean controls):")
print(n_by_cohort.to_string())

# Raw cohort-mean denial rates over time (the picture an analyst looks at first).
cohort_means = panel.groupby(["G", "year"], dropna=False)["denial_rate"].mean().unstack("G")
fig, ax = plt.subplots(figsize=(9, 5))
for g in cohort_means.columns:
    lab = "never-adopt" if pd.isna(g) else f"adopt {int(g)}"
    ax.plot(cohort_means.index, cohort_means[g], marker="o", label=lab)
ax.set_xlabel("year"); ax.set_ylabel("mean county denial rate (pp)")
ax.set_title("Synthetic HMDA: cohort-mean denial rates (staggered fair-lending policy)")
ax.legend(); fig.tight_layout()
fig.savefig("lab4_cohort_means.png", dpi=120)
print("Saved lab4_cohort_means.png")
```

**What to expect.** Four lines that start bunched together and drift gently downward in parallel (the common trend), with each *adopting* cohort's line peeling further below the never-adopters after its adoption year — the building policy effect made visible. The picture is the identification argument in one image: *before* a cohort adopts, its line tracks the never-adopters (the visible parallel pre-trend); *after*, it separates.

**The identification argument, in words.** The **treatment** is the state fair-lending policy; the **outcome** is the county denial rate. The **parallel-trends story** is: counties in adopting states would, absent the policy, have moved like counties in never-adopting states — same downward drift, same shocks. What **threatens** it? Anything that hits adopting states' denial rates differently *at the same time* as the policy, for reasons other than the policy: a state that adopts fair-lending rules *because* its denial rates were already falling (reverse causation in the timing), a coincident state economic boom, or a regional housing shock that happens to align with the adoption wave. The event study (Step 4) lets you *look* for the most detectable of these — a pre-existing divergence — but, as Chapter 4.1 §4.1.6 insisted, a clean pre-trend is evidence, not proof.

### Step 3 — Run TWFE first, and see why it is suspect

**What to do.** Run the static two-way fixed-effects regression from Chapter 4.1 — denial rate on the treatment dummy, absorbing county and year fixed effects, clustered by state. This is the regression a beginner reaches for, and on staggered data with dynamic effects it is exactly the one Chapter 4.2 warned you about.

**Code skeleton.**

```python
m_twfe = pf.feols("denial_rate ~ D | county + year", data=panel, vcov={"CRV1": "state"})
beta_twfe = float(m_twfe.coef()["D"])

print(f"TWFE beta_hat        = {beta_twfe:+.4f} pp")
print(f"true mean ATT        = {true_mean_att:+.4f} pp")
print(f"TWFE recovers {100*beta_twfe/true_mean_att:.0f}% of the truth (right sign, but ATTENUATED)")
```

**What to expect.** The TWFE coefficient comes out around **$-0.81$ pp** against a true mean ATT of **$-1.49$ pp** — the right sign, but only about **55%** of the truth. TWFE is *attenuated*: it is biased toward zero, and a policymaker reading the $-0.81$ would conclude the policy did barely more than half what it actually did. Why? Exactly the Chapter 4.2 mechanism. With staggered adoption, TWFE forms *forbidden* comparisons — it uses **already-treated** states (the 2016 wave) as controls for **newly-treated** states (the 2020 wave) during years when the 2016 wave's *own* effect is still deepening. That still-moving effect of the contaminated control gets subtracted from the newly-treated cohort's estimate, dragging the pooled coefficient toward zero. (Here the sign survives because genuine never-adopting controls exist to dilute the forbidden comparisons; recall from Ch 4.2 §3 that with *no* never-treated unit the sign can flip outright.)

**Reflection.** The attenuation is not noise — rerun with a different seed and TWFE will still land well short of the truth. Name the specific forbidden comparison in this panel: which cohort is wrongly used as a control for which, and in which years? Why would the bias *vanish* if you made the effect constant instead of building (tie this back to your Step 1 reflection)?

### Step 4 — The event study, and stressing parallel trends

**What to do.** Two things. First, estimate the *naive* TWFE event study (Chapter 4.1's leads-and-lags) so you can read the pre-trends — but knowing, from Sun–Abraham (Ch 4.2 §8), that under staggering its lead/lag coefficients can bleed into each other. Second, *stress* the design: dial a differential pre-trend into the treated cohorts and watch the lead coefficients tilt away from zero, reproducing in your own data the failure Chapter 4.1 §4.1.5 described.

**Code skeleton — the event study.**

```python
ev = panel.copy()
# relative (event) time for adopters; never-adopters -> -1 so they sit in the omitted reference bin.
ev["rel"] = np.where(ev["G"].notna(), ev["year"] - ev["G"], np.nan)
ev["rel_f"] = ev["rel"].fillna(-1).astype(int)

m_es = pf.feols("denial_rate ~ i(rel_f, ref=-1) | county + year", data=ev,
                vcov={"CRV1": "state"})
coefs = m_es.coef()
es = {int(k.split("::")[1]): float(v) for k, v in coefs.items() if k.startswith("rel_f::")}
es = pd.Series(es).sort_index()

print("Naive TWFE event-study coefficients (event time : beta_e),  e=-1 omitted:")
for e, v in es.items():
    region = "LEAD (pre-trend check)" if e < 0 else "LAG (dynamic effect)"
    print(f"   e={e:+d}: {v:+.3f}   {region}")
```

**What to expect.** The **leads** ($e<0$) hug zero — the synthetic data has no pre-trend by construction, so the treated and control cohorts moved together before adoption. The **lags** ($e\ge0$) march steadily more negative as the effect builds. That is the canonical clean event-study picture: flat before, growing after. It is *consistent with* parallel trends — but, per Chapter 4.1 §4.1.6, flat leads do not *prove* parallel trends (the logical point: the post-period counterfactual never happened; the statistical point: with few states the leads' confidence bands may be too wide to rule out a worrying slope).

**Code skeleton — stressing parallel trends on purpose.**

```python
def add_pretrend(df, slope_per_year=0.15):
    """Inject a DIFFERENTIAL pre-trend into adopting counties: their denial rate drifts
    extra each year for reasons UNRELATED to the policy. This BREAKS parallel trends."""
    out = df.copy()
    is_adopter = out["G"].notna()
    out.loc[is_adopter, "denial_rate"] += slope_per_year * (out.loc[is_adopter, "year"] - 2012)
    return out

stressed = add_pretrend(panel, slope_per_year=0.15)
ev2 = stressed.copy()
ev2["rel"] = np.where(ev2["G"].notna(), ev2["year"] - ev2["G"], np.nan)
ev2["rel_f"] = ev2["rel"].fillna(-1).astype(int)
m_es2 = pf.feols("denial_rate ~ i(rel_f, ref=-1) | county + year", data=ev2, vcov={"CRV1": "state"})
c2 = m_es2.coef()
es2 = {int(k.split("::")[1]): float(v) for k, v in c2.items() if k.startswith("rel_f::")}
es2 = pd.Series(es2).sort_index()

print("\nWith a planted differential pre-trend (parallel trends BROKEN):")
for e, v in es2.items():
    print(f"   e={e:+d}: {v:+.3f}   {'<- leads now TILT (visible pre-trend!)' if e < 0 else ''}")
```

**What to expect.** Now the **leads slope** — the pre-period coefficients drift away from zero instead of hugging it — because the treated cohorts were already moving differently before any policy. This is the *visible* signature of a parallel-trends violation, the thing the event-study plot exists to catch. The lesson: a tilting pre-trend is a red flag you can *see*; a clean pre-trend is reassurance you *cannot* fully bank. You just manufactured both, so you know the difference from the inside.

**Reflection.** When you inject the pre-trend, the *lag* coefficients also shift, not just the leads — the spurious trend keeps running into the post-period and gets mislabeled as a growing treatment effect (Ch 4.1 §4.1.3). Explain why, with only a few states, you might *fail* to detect even this planted pre-trend (the low-power problem of Ch 4.1 §4.1.6), and what you would report instead of "the pre-trends look fine."

### Step 5 — Callaway–Sant'Anna with clean controls, and recover the planted effect

**What to do.** Now the cure. Estimate Callaway–Sant'Anna group-time ATTs against **never-treated** clean controls, using the `differences` package exactly as in nb4.2: a MultiIndex `(entity, time)` DataFrame and a cohort column where never-treated units are `NaN`. Then aggregate to an event study and to a single overall ATT, and compare to the truth and to the broken TWFE number.

**Code skeleton.**

```python
panel_idx = panel.set_index(["county", "year"]).copy()    # MultiIndex (entity, time); G is NaN for never-treated

att = ATTgt(data=panel_idx, cohort_column="G")
att.fit(
    formula="denial_rate",             # outcome only; unconditional parallel trends
    control_group="never_treated",     # CLEAN controls = the never-adopting states
    progress_bar=False,
)

cs_overall = float(att.aggregate("simple", overall=True).iloc[0, 0])

ev_cs = att.aggregate("event")                              # index = relative period (event time)
att_col = [c for c in ev_cs.columns if c[-1] == "ATT"][0]   # MultiIndex column; ATT under last level
cs_ev = ev_cs[att_col]

print(f"Callaway-Sant'Anna overall ATT = {cs_overall:+.4f} pp   (clean controls)")
print(f"TWFE beta_hat                  = {beta_twfe:+.4f} pp   (attenuated)")
print(f"true mean ATT                  = {true_mean_att:+.4f} pp")
print("\nCS event-study coefficients (relative period : ATT vs planted truth):")
for e, v in cs_ev.items():
    truth_e = event_effect(int(e)) if e >= 0 else 0.0
    tag = "  <- pre-period (should be ~0)" if e < 0 else ""
    print(f"   e={int(e):+d}: {v:+.3f}   (true {truth_e:+.2f}){tag}")
```

**What to expect.** The Callaway–Sant'Anna overall ATT lands around **$-1.32$ pp** — close to the true $-1.49$ and far closer than TWFE's $-0.81$. The event-study coefficients track the planted build-up: the pre-period coefficients ($e<0$) hug zero (max magnitude around $0.16$ pp — flat, as the truth demands), and the post-period coefficients climb in lockstep with the planted $-0.40,-0.80,-1.20,\dots$ profile (you will see roughly $-0.23,-0.71,-1.09,-1.40,\dots$ — the estimator tracing out the truth, dampened only by noise and the diminishing number of clean comparisons at long horizons). The headline contrast is the whole lab: **the clean estimator recovers the planted effect; the contaminated one (TWFE) sits visibly short of it.**

One honest subtlety to notice and explain: the CS *overall* ($-1.32$) is not identical to the raw true-cell-mean ($-1.49$), and that is not an error. The `simple` aggregation weights group-time ATTs by *cohort size*, while the raw target averages over *treated cells* (so later horizons, with more accumulated effect, get different weight). They are *different weighted averages of the same true effects* — which is exactly Chapter 4.2 §6's point that you must **name your aggregation weights**, because "the overall ATT" is not one number until you say how you averaged.

**Code skeleton — the verification assertions (this is the part that proves the pipeline works).**

```python
# 1. CS recovers the planted effect (close, given noise) and TWFE is attenuated toward zero.
assert cs_overall < 0 and true_mean_att < 0,            "both CS and truth must be negative"
assert abs(cs_overall - true_mean_att) < 0.25,          "CS should land near the planted effect"
assert abs(beta_twfe) < abs(cs_overall) < abs(true_mean_att) + 1e-9, \
    "TWFE must be attenuated relative to CS, which is closer to the truth"

# 2. CS pre-period coefficients hug zero (parallel trends visible, no planted pre-trend).
pre = cs_ev[cs_ev.index < 0]
assert pre.abs().max() < 0.5,                           "CS pre-trends should hug zero"

print("\nALL CHECKS PASSED: CS recovers the planted effect; TWFE is attenuated; CS pre-trends flat.")
```

**What to expect.** All assertions pass and the success line prints. You have now *demonstrated*, on data whose truth you planted, that the Callaway–Sant'Anna pipeline recovers the effect and that TWFE does not — which is your license to trust the same code on real HMDA, where you can never see the truth directly.

**Reflection.** The CS pre-period coefficients are genuine placebo checks (effects should be zero before adoption). Why are they *more* trustworthy than the naive TWFE event study's leads from Step 4 (Ch 4.2 §8, Sun–Abraham)? If you reran CS with `control_group="not_yet_treated"` instead of `"never_treated"`, what would change about which states serve as controls for the 2016 cohort, and why might that be more or less credible in real HMDA?

### Step 6 — Put the three numbers side by side

**What to do.** Make the contrast unmissable with one figure: the planted truth, the Callaway–Sant'Anna overall ATT, and the attenuated TWFE coefficient, plus the event-study curves overlaid on the planted profile.

**Code skeleton.**

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# left: event-study curves vs the planted truth
e_grid = np.arange(int(cs_ev.index.min()), int(cs_ev.index.max()) + 1)
truth_curve = np.array([event_effect(e) if e >= 0 else 0.0 for e in e_grid])
ax1.axhline(0, color="0.6", lw=0.8); ax1.axvline(-0.5, color="0.6", lw=0.8, ls=":")
ax1.plot(e_grid, truth_curve, "k--", lw=2, label="planted truth $(e{+}1)\\cdot(-0.40)$")
ax1.plot(cs_ev.index.astype(int), cs_ev.values, "o-", color="C0", lw=2, label="Callaway–Sant'Anna")
ax1.plot(es.index.astype(int), es.values, "s--", color="C3", lw=1.4, label="naive TWFE event study")
ax1.set_xlabel("event time  $e = t - G_i$"); ax1.set_ylabel("effect on denial rate (pp)")
ax1.set_title("Event study: CS tracks the planted effect"); ax1.legend(loc="lower left", fontsize=9)

# right: headline overall numbers
names = ["planted\ntruth", "Callaway–\nSant'Anna", "pooled\nTWFE"]
vals = [true_mean_att, cs_overall, beta_twfe]
bars = ax2.bar(names, vals, color=["k", "C0", "C3"], alpha=0.85)
ax2.axhline(0, color="0.4", lw=0.8); ax2.axhline(true_mean_att, color="k", ls="--", lw=1, alpha=0.6)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width()/2, v - 0.05, f"{v:+.2f}", ha="center", va="top",
             color="white", fontweight="bold")
ax2.set_ylabel("overall ATT (pp)"); ax2.set_title("Headline: CS recovers; TWFE attenuated")
fig.tight_layout(); fig.savefig("lab4_hmda_did_results.png", dpi=120)
print("Saved lab4_hmda_did_results.png")
```

**What to expect.** The left panel shows the CS curve hugging the dashed planted-truth line while the naive TWFE curve drifts off it in the post-period (cohort-bleed). The right panel shows the CS bar reaching most of the way to the planted-truth line while the TWFE bar falls short. One picture, the whole week.

---

## You're done when…

Use this checklist. A box is checked only when you can point to the number or figure that proves it.

- [ ] **Path A understood.** You can write the CFPB Data Browser aggregation query, name the pinned vintage and the `[CHECK]` you owe on it, and explain why you aggregate to county-year on GMU infrastructure rather than pulling the national LAR to a laptop.
- [ ] **Spec named.** You can state the full DiD spec in one breath — outcome, treatment, controls, fixed effects, clustering, sample, control group, aggregation, identifying assumption — for the real-data design.
- [ ] **Step 1.** Your synthetic panel has 1,152 rows, a true mean ATT near $-1.49$ pp, and never-adopters coded `G = NaN`.
- [ ] **Step 3.** Static TWFE comes out around $-0.81$ pp — right sign, ~55% of the truth — and you can name the forbidden comparison (2016 wave used as control for the 2020 wave) that causes the attenuation.
- [ ] **Step 4.** The naive event study's leads hug zero on the clean panel; after `add_pretrend`, the leads *tilt*, and you can explain why a clean pre-trend is reassurance but not proof.
- [ ] **Step 5.** Callaway–Sant'Anna recovers an overall ATT near $-1.32$ pp (close to the planted $-1.49$, far closer than TWFE), the CS pre-period coefficients hug zero, all verification assertions pass, and you can explain why CS's overall differs slightly from the raw cell-mean (aggregation weights).
- [ ] **Step 6.** Your two-panel figure shows the CS curve tracking the planted truth and the CS bar far closer to the truth than the TWFE bar.
- [ ] **Reproducibility.** Every number regenerates from `SEED = 20260528` and one `rng`; you can name your seed and your pinned HMDA vintage.

---

## Reflection questions — tied to the fair-lending thread

These tie the design back to the fair-lending question Maya has carried since Week 1 and that Mentor Session 4 takes up through Gao & Sun (2019, *PNAS*). Answer each by pointing to a number or figure you produced.

1. **What a denial-rate gap does and does not show.** Your synthetic outcome is a county denial rate, and the policy lowered it. But suppose, on *real* HMDA, you found that denial rates fell after a fair-lending rule. Why is "denial rates fell" not yet "the rule reduced discrimination"? Name the Week-2 threat (Ch 2.5) that a raw denial rate confounds, and explain how the DiD design — differencing against never-adopting states — addresses some of it but not all. What would you still need to hold fixed that a county-year denial rate cannot?

2. **The clean-design move, per Gao & Sun.** Gao and Sun (2019) studied whether same-sex couples were treated differently in mortgage lending, using millions of HMDA-style records. The hard part of fair-lending work is not *finding* a gap — gaps are everywhere — but showing a skeptic the gap is *causal* and not an artifact of who applies where and with what creditworthiness. In one paragraph, explain how a staggered policy shock plus a clean Callaway–Sant'Anna comparison turns "we see a gap" into "we measured an *effect of the policy*," and why the parallel-trends assumption is the precise thing a referee would attack.

3. **Parallel trends as the load-bearing wall.** In Step 4 you planted a differential pre-trend and watched the leads tilt. Suppose a state adopted fair-lending rules *because* its denial rates were already falling (the legislature responded to public pressure that also drove lenders to approve more). Which direction would this bias your estimated policy effect, and would the event-study leads necessarily catch it? Tie your answer to Chapter 4.1 §4.1.6 (pre-trends can refute parallel trends but never confirm them) and to the low-power problem when there are few treated states.

4. **Few treated clusters.** Your panel has nine treated states across three waves; a real state-policy design might have far fewer. Recall the Bertrand–Duflo–Mullainathan lesson (Ch 4.1 §4.1.7) and the few-treated-clusters problem. Why is clustering by state the right *level*, and why might the inference still be fragile with only a handful of adopting states? Name one thing you would report (beyond a clustered SE) to be honest about the uncertainty.

5. **From lab to capstone.** This lab is a rehearsal for Capstone 1 (*Fair Lending on HMDA*). Write the three-sentence research plan you would carry into the capstone: the outcome and treatment you would build from real HMDA, the clean control group you would use, and the single identifying assumption your whole result would rest on — and the one robustness check (a placebo, a not-yet-treated control swap, or a sensitivity analysis) you would run to defend it against the skeptic in the room.

---

## Where this connects

You have now built a fair-lending DiD on a HMDA-shaped panel from the ground up: pulled (or simulated) a county-year denial-rate outcome, defined treatment by a staggered state policy, run TWFE and *felt* it attenuate, read an event study and *stressed* parallel trends until the leads tilted, and finally run Callaway–Sant'Anna against clean controls and recovered the effect you planted — the demonstration that earns your trust in the code before you point it at data whose truth you cannot see. The whole arc is the Week-4 thesis in miniature: the credibility comes from the *design* (a clean policy shock, clean controls, a per-cohort parallel-trends bet you state and defend), not from a pile of controls.

That is exactly the move Prof. Gao made in the fair-lending work this week anchors on — Gao & Sun (2019, *PNAS*) — and the move you will make again in **Mentor Session 4** ("Detecting discrimination with a clean design") and in **Capstone 1** (*Fair Lending on HMDA*). The habit underneath, the one every lab in this camp drills: *when you are unsure whether a tool does what it claims, build a universe where you know the truth and check.* You did it with sizes and powers in Lab 1, with a planted risk premium in Lab 2, with a weak instrument's lying confidence interval in Lab 3, and here with a planted policy effect that Callaway–Sant'Anna recovers and naive TWFE does not. Keep this notebook: the synthetic-panel-then-real-data structure, and the `differences` group-time ATT pipeline, are the scaffold of a publishable fair-lending result.

---

### References

- Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How Much Should We Trust Differences-in-Differences Estimates? *Quarterly Journal of Economics*, 119(1), 249–275.
- Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-Differences with Multiple Time Periods. *Journal of Econometrics*, 225(2), 200–230.
- Gao, L., & Sun, H. (2019). Lending practices to same-sex borrowers. *Proceedings of the National Academy of Sciences*, 116(19), 9293–9302.
- Goodman-Bacon, A. (2021). Difference-in-Differences with Variation in Treatment Timing. *Journal of Econometrics*, 225(2), 254–277.
- Sun, L., & Abraham, S. (2021). Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects. *Journal of Econometrics*, 225(2), 175–199.
- Consumer Financial Protection Bureau. *HMDA Data Browser API.* `https://ffiec.cfpb.gov/data-browser/` (vintage pinned per run — `[CHECK]` the snapshot date on the camp container).
