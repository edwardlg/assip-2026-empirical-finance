---
title: "Data access"
description: >-
  How to get authenticated and pulling data from WRDS, FRED, HMDA, and
  EDGAR — and the secrets-discipline rules that apply everywhere.
---

# Data access

This page is the one-stop guide to the four data sources that cover roughly 90 % of what the cohort will pull this summer: **WRDS** (CRSP, Compustat, IBES, OptionMetrics), **FRED** (macro), **HMDA** (fair lending) via the CFPB Data Browser, and **EDGAR** (10-Ks, 13Fs).

For dataset-by-dataset details — coverage, key fields, gotchas, licensing — see the **data cards** in the textbook at [`data-cards/`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/README.html). The data cards are the canonical reference for "what's in this dataset, how do I cite it, and where does it break"; this page is the canonical reference for "how do I get logged in."

---

## 0. Secrets discipline (read this first)

!!! danger "Three rules. No exceptions."

    1. **No secrets in code.** Every API key, every password, every WRDS connection string lives in environment variables loaded from a `.env` file at the repo root.
    2. **Never commit `.env`.** The repo's `.gitignore` excludes it. If you ever `git add .env` by mistake, **stop**, force-remove from the index (`git rm --cached .env`), and message a sub-leader before pushing.
    3. **Seeds are pinned.** Every notebook uses `numpy.random.default_rng(42)` (or another explicit seed declared at the top). No `np.random.seed()` calls scattered through the code. Reproducibility is not optional.

A working `.env` for this program looks roughly like this (yours will have real values):

```dotenv
# .env — never committed
WRDS_USERNAME=your_gmu_netid
WRDS_PGPASS_PATH=~/.pgpass         # see WRDS setup below
FRED_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=                  # optional, Week 6 only
AZURE_APIM_KEY=                     # optional, Week 6 only
```

Code that loads it:

```python
from dotenv import load_dotenv
import os
load_dotenv()
fred_key = os.environ["FRED_API_KEY"]   # raises if not set — good
```

---

## 1. WRDS — CRSP, Compustat, IBES, OptionMetrics

WRDS (Wharton Research Data Services) is where CRSP, Compustat, IBES, OptionMetrics, and the merged CRSP-Compustat panel live. **Our cohort has access through GMU's institutional seat** — you do *not* need a personal subscription.

### Get authenticated

1. Email Prof. Gao (<lgao9@gmu.edu>) with your full name, NetID, and the request "please sponsor my WRDS account for ASSIP 2026." Send this no later than **Monday June 22**.
2. You will receive a WRDS confirmation email within 2–3 business days. Click the link, set a password, and note your username.
3. Set up `.pgpass` so the Python `wrds` package doesn't prompt every call:

    === "macOS / Linux"

        ```bash
        printf 'wrds-pgdata.wharton.upenn.edu:9737:wrds:YOUR_USERNAME:YOUR_PASSWORD\n' > ~/.pgpass
        chmod 600 ~/.pgpass
        ```

    === "Windows (WSL recommended)"

        Same as Linux above, run from your WSL shell. If you must use native Windows, put `pgpass.conf` at `%APPDATA%\postgresql\pgpass.conf` with the same single-line format.

4. Verify:

    ```python
    import wrds
    db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])
    db.list_libraries()[:5]
    ```

### Licensing rules

CRSP, Compustat, IBES, and OptionMetrics are **licensed data**. They stay on GMU infrastructure (your laptop counts) for the duration of the program. Do **not** push the raw parquet/CSV pulls to GitHub. Push *derived* tables only — e.g., the firm-level panel after merges and winsorizing — and only if your data card says so.

### Data cards

- [`data-cards/crsp.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/crsp.html)
- [`data-cards/compustat.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/compustat.html)
- [`data-cards/ibes.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/ibes.html)
- [`data-cards/optionmetrics.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/optionmetrics.html)

---

## 2. FRED — macro data via API key

FRED (the St. Louis Fed's Federal Reserve Economic Data) hosts the risk-free rate, GDP, unemployment, CPI, and ~800,000 other series. It's free and the API is generous.

### Get an API key

1. Sign up at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html). Free, instant.
2. Put the key in your `.env`:

    ```dotenv
    FRED_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

3. Use it via `pandas-datareader` or the `fredapi` package:

    ```python
    import os
    from fredapi import Fred
    fred = Fred(api_key=os.environ["FRED_API_KEY"])
    rf = fred.get_series("DGS3MO")
    ```

### Data card

[`data-cards/fred.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/fred.html)

---

## 3. HMDA — via CFPB Data Browser

HMDA (Home Mortgage Disclosure Act) data lives at the Consumer Financial Protection Bureau and is **free, public, and requires no auth**. We use it in Lab 3 (PSM + 2SLS fair-lending) and Week 6's Bartlett / Bhutta–Hizmo–Ringo replication.

### Pull HMDA

- Browser-based: [ffiec.cfpb.gov/data-browser](https://ffiec.cfpb.gov/data-browser/). Build a query, download a CSV.
- Programmatic: the CFPB exposes a JSON API; see `nb3.4` and `nb6.4` for cached-or-fetch patterns.

### Data card

[`data-cards/hmda.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/hmda.html) — coverage, key fields (race, sex, action_taken, loan_amount, applicant_income), version notes (the 2018 reformat).

---

## 4. EDGAR — 10-Ks, 10-Qs, 13Fs, 8-Ks

EDGAR (SEC's filings database) is free, public, and rate-limited to 10 requests / second per User-Agent. Set a polite User-Agent string with your name and email.

```python
import requests
HEADERS = {"User-Agent": "Your Name your-email@gmu.edu"}
r = requests.get("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K", headers=HEADERS)
```

### Data cards

- [`data-cards/edgar-10k-10q.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-10k-10q.html)
- [`data-cards/edgar-13f.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-13f.html)
- [`data-cards/edgar-8k.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-8k.html)
- [`data-cards/edgar-def14a.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-def14a.html)
- [`data-cards/edgar-nport.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-nport.html)
- [`data-cards/edgar-xbrl.md`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-xbrl.html)

---

## 5. Other sources you may touch

The textbook has data cards for **35 datasets** in total. Browse [`data-cards/`](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/README.html) for the full list. Highlights:

- [PatentsView (USPTO)](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/uspto-patentsview.html) — Week 6 and innovation capstones.
- [Loughran–McDonald dictionary](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/loughran-mcdonald-dict.html) — Week 6 sentiment.
- [FFIEC Call Reports](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/ffiec-call-reports.html) — bank-regulation capstones.
- [FR Y-9C](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/fr-y9c.html) — BHC-level bank data.
- [TRACE](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/trace.html), [MSRB EMMA](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/msrb-emma.html), [Treasury / FINRA](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/treasury-finra.html) — fixed-income capstones.
- [CFPB Consumer Complaints](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/cfpb-complaints.html) — fair-lending text capstones.
- [NOAA / FEMA](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/noaa-fema.html) — climate-risk capstones.

---

## 6. The GitHub repo

Each student forks the cohort repo at the start of the program and works on their own fork. Pull requests go from `your-fork:week-NN-your-name` into `cohort:main`.

### One-time setup

1. **Make a GitHub account** if you don't have one. Use your real name; this repo will appear on your résumé.
2. **Generate a Personal Access Token** at [github.com/settings/tokens](https://github.com/settings/tokens). Scope: `repo` and `workflow`. Save the token in a password manager — GitHub will not show it again.
3. **Configure git locally:**

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your-email@example.com"
    ```

4. **Fork** the cohort repo (button in the top-right of the GitHub repo page).
5. **Clone your fork:**

    ```bash
    git clone https://github.com/YOUR-USERNAME/ASSIP8weeks.git
    cd ASSIP8weeks
    git remote add upstream https://github.com/leigao-gmu/ASSIP8weeks.git
    ```

6. **Set up the environment** — see [Setup](setup.md).

### Daily flow

```bash
git checkout main
git pull upstream main          # always start from the latest cohort main
git checkout -b week-03-your-name
# ...work...
git add notebooks/week-03/lab3.ipynb book/weeks/week-03/ps3.1.md  # specific files only
git commit -m "Week 3: PS 3.1–3.5 + lab"
git push origin week-03-your-name
# Then open a PR on GitHub from your fork's branch into cohort:main
```

!!! warning "Never `git add .` blindly"
    `git add .` will happily pick up `.env`, raw CRSP parquet files, virtual-env directories, and other things that should not be on GitHub. Add files by name.

---

## Last word

If you cannot pull a dataset, **post in `#help` on Slack with the exact error message and the exact command you ran** — not "WRDS isn't working." We can almost always fix a data-access problem in under 15 minutes if you give us the literal traceback.
