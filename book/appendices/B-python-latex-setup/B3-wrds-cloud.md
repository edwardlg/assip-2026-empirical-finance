# B.3 WRDS Cloud

This is where the camp stops practicing on toy data and touches the real thing. **WRDS — Wharton Research Data Services — is the gateway to the datasets that empirical finance is actually built on:** CRSP for stock prices and returns, Compustat for accounting fundamentals, IBES for analyst forecasts, and dozens more. Nearly every paper you will read this summer, including Prof. Gao's, runs on data pulled from WRDS. By the end of this section you will have an account, a connection from Python that never hard-codes your password, and a working query pattern against CRSP and Compustat — together with a clear understanding of the one rule that governs all of it: **the licensed data stays on GMU infrastructure.**

The trick to reveal up front is about *where computation happens*. WRDS is not a file you download. It is a PostgreSQL database living on Wharton's servers, holding data that is licensed — meaning GMU pays for the right to *use* it, under terms that forbid redistributing the raw records. The professional pattern, and the one §5 mandates, is to **send your query to the data rather than pulling the data to your laptop.** You write SQL (or let the `wrds` package write it for you), the WRDS Cloud runs it against the full dataset, and you get back only the filtered, often aggregated result you asked for. The terabytes stay put; a few megabytes of *your* result come back. Everything below is a consequence of that single design choice.

## B.3.1 Getting a WRDS account and seat

WRDS access is institutional. You do not buy your own; you get a **seat under GMU's subscription**, which the camp arranges. The steps:

1. **Request an account** at the WRDS registration page, selecting **George Mason University** as your institution and registering with your **GMU email address**. The GMU email is what ties you to the university's subscription — a personal Gmail will be rejected.
2. **Wait for approval.** A WRDS administrator at GMU (or the camp instructor acting on your behalf) approves the request. This is not instant; request your account in the first days of the camp so it is live when you need it. Approval triggers an email with your **username** and a link to set your **password**.
3. **Log in to the web interface once** at wrds-www.wharton.upenn.edu to confirm the account works and to accept the data-use terms. The web interface is also where you can browse the data dictionaries — which datasets exist, which variables they contain — and it is genuinely the best way to learn the table and column names before you script anything.

A note on what your seat permits: a student seat gives **read-only** access to the subscribed datasets. You can query; you cannot alter the source data, and you cannot share your login. Sharing credentials is both a security problem and a license violation, and it is exactly the behavior the §5 secrets rule is designed to make unnecessary — you will never need to paste your password anywhere a teammate could see it.

## B.3.2 Connecting from Python without hard-coding your password

The `wrds` package (installed via the `environment.yml` in B.1) connects Python to the WRDS PostgreSQL server. The naive way to connect is to type your password into the code. **Do not do this.** It is the precise mistake §5 and B.2's `.gitignore` discipline exist to prevent: a password in code gets committed, pushed, and is then permanently in your repository history for anyone with access to read. We have two clean alternatives. Use either.

### Option A — the `.pgpass` file (recommended for the GMU environment)

WRDS's own recommended setup stores your credential in a PostgreSQL password file called `.pgpass` in your home directory. The `wrds` package looks for it automatically, so once it exists, `wrds.Connection()` just works with no password typed and nothing secret in your code. The first time you connect, the package can create it for you:

```python
import wrds

# First connection: you'll be prompted for username and password
# interactively, then offered to save a .pgpass for next time. Say yes.
db = wrds.Connection(wrds_username="your_gmu_username")
```

When prompted, enter your password once; answer **yes** to "create a pgpass file." From then on, `wrds.Connection(wrds_username="your_gmu_username")` connects silently. The file it writes looks like one line of `hostname:port:database:username:password` and lives at `~/.pgpass` (Windows: `%APPDATA%\postgresql\pgpass.conf`). Two non-negotiable rules about it:

- **Its permissions must be locked down.** On macOS/Linux, `chmod 600 ~/.pgpass` so only you can read it; PostgreSQL will refuse to use a world-readable password file. The `wrds` package usually sets this for you.
- **It must be in your `.gitignore`** (B.2 already listed `.pgpass` and `*.pgpass`). The file is a secret. It never goes in a repository.

### Option B — environment variables (recommended for scripts and Hopper jobs)

For non-interactive runs — a script, an automated job, anything where no human is there to answer a prompt — the §5 idiom is to read the credential from an **environment variable** that you set outside the code. You set the variable once in your shell session (or in a Hopper job script; see the sibling **B.4** on SLURM), and the code reads it at runtime:

```shell
# Set in your shell — NOT in any file you commit.
export WRDS_USERNAME="your_gmu_username"
export WRDS_PASSWORD="set-in-your-shell-not-in-code"
```

```python
import os
import wrds

db = wrds.Connection(
    wrds_username=os.environ["WRDS_USERNAME"],
    wrds_password=os.environ["WRDS_PASSWORD"],
)
```

The password exists only in your shell's memory and in the running Python process. It is never written into a tracked file. (Where do the `export` lines themselves live? In your shell profile or a `.env` that is *git-ignored* — never in the repo. On Hopper, you set them in the job's environment.) This is the same `os.environ[...]` pattern §5 shows for the Azure key; the principle is uniform across every secret in the project.

Whichever option you use, close the connection when you are done so you free your seat:

```python
db.close()
```

## B.3.3 What lives on WRDS, and the names you will use

A short orientation to the three datasets the camp leans on most. The exact table and column names are the kind of thing you confirm in the web interface's data dictionary; the ones below are the standard, long-stable ones, but treat any you have not personally verified as worth a glance there.

- **CRSP** (Center for Research in Security Prices) — the canonical source for U.S. stock prices, returns, shares outstanding, and delisting information. The daily stock file is `crsp.dsf` and the monthly is `crsp.msf`; the security identifier is `permno` (a permanent number that, unlike a ticker, never gets reused or recycled when a company changes name). The core return variable is `ret`.
- **Compustat** — accounting fundamentals from company filings: assets, debt, earnings, book value. The annual fundamentals table is `comp.funda`; firms are identified by `gvkey`, and a critical filter is `indfmt`, `datafmt`, `popsrc`, and `consol` set to the standard `INDL`/`STD`/`D`/`C` values to avoid double-counting restated or non-standard records.
- **IBES** — analyst earnings estimates and recommendations, identified by `ticker` (IBES's own ticker, not the exchange ticker) on tables like `ibes.statsum_epsus`.

Linking CRSP and Compustat — pairing a firm's stock returns with its accounting data — is done through the **CRSP/Compustat Merged** linking table (`crsp.ccmxpf_lnkhist`), which maps `gvkey` to `permno` over time. Getting that link right (respecting the link's valid date range, `linktype`, and `linkprim`) is a genuine skill the chapters develop; for now, just know the merge runs through that table rather than by matching ticker strings, which would be a classic error.

## B.3.4 A sample query pattern

Here is the pattern you will reuse all summer, written so that each piece illustrates a §5 principle. Suppose Devon wants monthly returns for a handful of large tech names to prototype a momentum signal before scaling up to the full universe.

```python
import os
import wrds
import pandas as pd

# --- 1. Connect (credentials from .pgpass or environment; never in code) ---
db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])

# --- 2. Push the filtering to the server: ask only for what you need ---
#   Filter on date range and a permno list IN THE SQL, so the WRDS Cloud
#   does the heavy lifting and only a small result crosses the wire.
query = """
    SELECT permno, date, ret, prc, shrout
    FROM crsp.msf
    WHERE date BETWEEN '2015-01-01' AND '2020-12-31'
      AND permno IN (14593, 90319, 10107)     -- a short illustrative list
    ORDER BY permno, date
"""
monthly = db.raw_sql(query, date_cols=["date"])

# --- 3. Pin the snapshot date for reproducibility (CONVENTIONS §5) ---
SNAPSHOT = "2026-05-15"   # the date you pulled; record it in the notebook
print(f"CRSP monthly pulled {SNAPSHOT}: {len(monthly):,} rows")

db.close()
```

Read what that code is *doing*, because the structure is the lesson:

- **The `WHERE` clause runs on the server.** Both the date range and the `permno` list are filters in the SQL, so the WRDS Cloud scans the full `crsp.msf` and returns only the matching rows. The alternative — `SELECT *` and filtering in pandas afterward — would drag the entire monthly stock file across the network. Filter at the source. This *is* the "send the query to the data" principle made concrete.
- **`db.raw_sql(...)` gives you a DataFrame directly**, with `date_cols` parsed as dates, so the result drops straight into the pandas workflow from B.1.
- **The snapshot date is pinned.** §5 requires that every notebook touching licensed data record the date its CRSP/Compustat snapshot was pulled. WRDS data is versioned — vendors revise history, add delisting returns, restate fundamentals — so a result is only reproducible relative to *when* you pulled. The `SNAPSHOT` variable, recorded in the notebook, is how a reader (or you, in six months) knows which vintage produced the numbers.

The `wrds` package also offers convenience methods — `db.get_table("crsp", "msf", obs=10)` to peek at a table, `db.list_tables(library="crsp")` to see what is there, `db.describe_table("crsp", "msf")` to list columns. These are for *exploration*; once you know what you want, a targeted `raw_sql` with a tight `WHERE` clause is the production pattern, because it minimizes both the data crossing the network and the load you put on the shared server.

One more discipline point: **be a considerate tenant of a shared resource.** WRDS is used by thousands of researchers at once. A `SELECT *` on a daily file with no date filter is the query that gets accounts throttled. Always bound your query by date and identifier, pull what you need, and prototype on a small `permno` list (as above) before unleashing the full universe.

## B.3.5 Where the data is allowed to live: GMU environment vs. your laptop

This is the rule the whole section has been building toward, and it is worth stating plainly because the consequences are real. **Licensed CRSP/Compustat/IBES data stays on GMU infrastructure (§5).** In practice that means:

- You **query WRDS read-only**, from either the WRDS Cloud directly or from the GMU compute environment (Hopper; see **B.4**). The query result — your filtered, often aggregated extract — is a derived product you may work with for your camp project.
- You **do not download the raw licensed datasets to a personal laptop** and you **do not redistribute them** — not by committing them to GitHub (B.2's `.gitignore` blocks `*.dta`, `*.sas7bdat`, `data/raw/`), not by emailing them, not by posting them. Pushing a CRSP `.dta` to a repo is redistribution and breaches GMU's license; that is precisely why those file types are git-ignored.

So which machine should you run on? The honest answer is a spectrum:

- **A laptop is fine for connecting and pulling small, bounded extracts** — the prototype-scale pulls like Devon's three-`permno` example — provided the result stays local-and-private and never gets committed or shared. Small derived extracts for active analysis are normal research practice; raw-dataset mirroring is not.
- **The GMU environment (Hopper) is where the heavy work belongs:** large pulls, the full firm universe, panel merges across millions of rows, and anything compute-intensive. Running there keeps the licensed data on GMU infrastructure end to end and gives you far more memory and CPU than a laptop. It is also the only sane place to run a job that takes hours — you submit it with SLURM (**B.4**) and let it run without your laptop being awake. When in doubt about a large or sensitive pull, do it on Hopper.

The clean way to think about it: **your repository holds code, not licensed data.** Anyone with your repo and a WRDS seat can rerun your code and regenerate your extract from the source — that is reproducibility done right. What they cannot do, and must not be able to do, is read GMU's licensed data *out of your repository*, because it was never there. The recipe travels; the protected ingredients stay in the GMU kitchen.

## B.3.6 Quick troubleshooting

A few snags that catch nearly everyone the first week:

- **`OperationalError` / "could not connect."** Usually the account is not approved yet, or the username is mistyped. Confirm you can log in to the WRDS web interface first; if the web works but Python does not, recheck the `wrds_username` you passed.
- **It keeps prompting for a password.** Your `.pgpass` either does not exist, is in the wrong place, or has loose permissions. Recreate it (let `wrds.Connection()` write it) and ensure `chmod 600 ~/.pgpass`.
- **A query hangs or returns nothing.** Check your date format (`'YYYY-MM-DD'` string literals in the SQL) and confirm the table and column names against `db.describe_table(...)` — a typo in a column name is the usual culprit, and case sometimes matters.
- **A pull that "worked yesterday" gives slightly different numbers.** That is the snapshot effect — the vendor may have revised data. This is the entire reason §5 makes you pin the snapshot date; record it, and the discrepancy becomes explainable rather than mysterious.

You now have a WRDS seat, a connection that keeps your password out of your code and your repository, a query pattern that does its filtering on the server, and a firm grasp of why the licensed data lives on GMU infrastructure and only your derived results come home with you. With B.1 (the environment), B.2 (GitHub and hand-in), and B.3 (the data) in place, the remaining setup sections cover scale and writing: **B.4 (Running Jobs on Hopper with SLURM)** for when a query or estimation outgrows an interactive session, and **B.5 (Overleaf and LaTeX)** for turning your results into the paper you present in Phase 2.
