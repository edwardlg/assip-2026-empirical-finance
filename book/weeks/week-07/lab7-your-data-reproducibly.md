# Lab 7 — Your Data, Reproducibly

This is the lab where your project stops being a pile of notebooks on your laptop and becomes a *research repository* — a single, version-controlled folder that a stranger could clone and understand, that keeps licensed data where the license requires, and that carries a cryptographic time-stamp proving your pre-analysis plan was filed before you saw a single confirmatory result. Everything Week 7 has built points here. Chapter 7.2 taught you to pull data so that the same command run a year from now gives the same answer — pinned, cached, logged. Chapter 7.3 taught you to write a pre-analysis plan and insisted that it only constrains you if you can *date* it, and named the mechanism: a tagged Git commit. This lab is where you actually build the thing those chapters described, and it is not a throwaway exercise. **The repository you stand up today is your capstone deliverable.** Weeks 7 and 8 both live inside it: the dataset build (Chapter 7.4), the identification memo (Chapter 7.5), the first-look regressions (nb7.5, frozen until your PAP is filed), and next week's full analysis and write-up all commit into this same repo. Get the scaffolding right now and the rest of the camp is building on rock.

The discipline this lab drills is the one a referee, a replication team, or future-you cares about most: **reproducibility is a property of the repository, not of any single script.** A brilliant analysis whose data pull cannot be re-run, whose environment cannot be reconstructed, or whose pre-registration cannot be dated is, to a skeptic, just an assertion. We are going to make your project the opposite of an assertion. By the end you will have a repo with a sensible layout, a pinned environment that rebuilds bit-for-bit on a fresh machine, a README a stranger can follow, a data card per source, a `.gitignore` that makes it *impossible* to accidentally commit CRSP or your API keys, and a `pap-filed` tag whose timestamp no one — including you — can quietly move.

There is no synthetic-data simulation in this lab and no estimator to recover. The "result" you are checking is operational: can a fresh clone of your repo, on a machine that has never seen your project, reconstruct the environment, read what the project does, and verify that the licensed bytes and the secrets never left your control? That is a yes/no you can actually test, and the checklist at the end is how you test it.

---

## Learning goals

By the end of this lab you will be able to:

1. **Lay out a research repository** from a sensible template — `data/` (git-ignored), `src/`, `notebooks/`, `paper/`, plus `README.md`, `environment.yml`, and `.gitignore` — and explain what each directory is for.
2. **Use the cohort GitHub workflow** end to end: create your private repo from the template, clone it, commit, push, and understand what the instructor sees on the other side.
3. **Pin your environment** in a conda `environment.yml` with `python=3.11` and the exact stack from CONVENTIONS §5, and explain *why* pinning is the difference between "it ran on my laptop" and "it runs anywhere."
4. **Write a README** (what / why / how-to-run) and a **data card** per source that documents coverage, identifiers, access, license, and the reproducibility pin.
5. **Practice `.gitignore` discipline** so that licensed raw data (CRSP/Compustat/TRACE) and secrets (`.env`, keys) *cannot* be committed — and verify it with `git check-ignore`.
6. **File your pre-analysis plan as a tagged commit** (`git tag pap-filed`) so the registration timestamp is immutable, connecting the mechanic to the argument of Chapter 7.3.
7. **Audit your own repo** against a "you're done when…" checklist that a referee could run.

---

## Setup

You need three tools: **Git** (version control), a **GitHub account** (you almost certainly created one in Week 6), and **conda** (Miniconda or Anaconda, for the pinned environment). The ASSIP container has all three; if you are on your own machine, install Miniconda and Git first. Confirm they are present before you start — a one-line check each:

```bash
git --version          # any 2.x is fine
conda --version        # Miniconda/Anaconda
gh --version           # GitHub CLI, optional but convenient
```

One identity step, once per machine, so your commits are attributed to you (Git refuses to commit without it, and your `pap-filed` timestamp is only meaningful if it carries your name):

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@gmu.edu"
```

A note on *where* you work. If your project touches licensed data (CRSP, Compustat, IBES, TRACE — anyone doing the equities or fundamentals capstones), the rule from CONVENTIONS §5 and Chapter 7.2 binds: **the licensed bytes live only on GMU infrastructure** (WRDS Cloud or the Hopper cluster), never on a personal laptop. Your *repository* — the code, the README, the data cards, the logs, the PAP — can live on your laptop and on GitHub, because none of those contain licensed data. The `.gitignore` you build in Step 5 is what enforces that wall. So the mental model is: the repo travels freely; the licensed data stays home; the repo's job is to be the *recipe* that reconstructs the data on GMU infrastructure for anyone who has the same access.

---

## Step 1 — Create the project repository from a template

Start from a layout, not a blank folder. A research repo has a small number of directories, each with one job, and the discipline of putting things in the right place from day one is what keeps a six-month project navigable. Here is the template you will build — the same one nb7.2's data-pull harness sets up and the one your capstone uses:

```
your-project/
├── README.md            # what the project is, why, and how to run it
├── environment.yml      # the pinned conda environment (Step 3)
├── .gitignore           # what must NEVER be committed (Step 5)
├── PRE-ANALYSIS-PLAN.md # the PAP you tag as pap-filed (Step 6)
├── DEVIATIONS.md         # running, dated log of departures from the PAP (Ch 7.3)
├── data/
│   ├── raw/             # cached raw pulls — GIT-IGNORED; licensed data lives ONLY here
│   │   └── .gitkeep
│   └── processed/       # built analysis datasets — GIT-IGNORED
│       └── .gitkeep
├── src/                 # importable code: data pulls, cleaning, estimation
│   └── pull_data.py
├── notebooks/           # exploratory and reporting notebooks
├── paper/               # the write-up, figures, tables (Week 8)
├── logs/
│   └── pulls.jsonl      # one line per data pull: what, when, how big, content hash
└── data-cards/          # one card per data source (Step 4)
```

Why this shape, directory by directory. **`data/`** holds inputs and built datasets, and it is split into `raw/` (untouched pulls, your ground truth) and `processed/` (what your cleaning code produces). *The entire `data/` tree is git-ignored* — more on why in Step 5 — but you commit an empty `.gitkeep` file in each subfolder so the *structure* travels even though the *contents* do not. **`src/`** holds reusable code you `import` (the bounded queries, the cleaning functions, the estimators), separated from the **`notebooks/`** where you explore and narrate; the rule of thumb is *logic in `src/`, story in `notebooks/`*, so a function you depend on is tested and importable rather than buried in a cell. **`paper/`** is where Week 8's write-up, figures, and tables go. **`logs/`** holds the append-only pull log from Chapter 7.2. And **`data-cards/`** holds one spec sheet per source.

Build it with plain shell commands. Make the directory, initialize Git, and scaffold the tree:

```bash
mkdir my-capstone && cd my-capstone
git init

# directory skeleton; .gitkeep lets an "empty" dir be committed
mkdir -p data/raw data/processed src notebooks paper logs data-cards
touch data/raw/.gitkeep data/processed/.gitkeep
```

`git init` turns the folder into a repository — it creates the hidden `.git/` directory where Git stores every version of every file. The `.gitkeep` trick is a small but important convention: Git tracks *files*, not directories, so an empty `data/raw/` would simply not exist in a fresh clone. A zero-byte `.gitkeep` (the name is convention, not magic) gives Git something to track so the folder is recreated when someone clones — which matters because your code writes its cache into `data/raw/` and would fail if the folder were missing.

You will fill in `README.md`, `environment.yml`, `.gitignore`, the data cards, and the PAP in the steps that follow. The cohort distributes a **template repository** (a GitHub repo marked "Template") so you do not have to assemble this scaffolding by hand a second time: click *Use this template → Create a new repository* on the template repo's page on GitHub, or, equivalently, run `gh repo create capstone-2026-<your-github-username> --template ASSIP-COHORT-ORG/capstone-template --private` from the command line. Either way you land on the same layout. Doing it once manually first, as above, is worth it so you know what each piece is for.

---

## Step 2 — The cohort GitHub workflow

In this internship, you do not invent a repository name or pick where it lives on the fly — you **create one private repo from the cohort's template**, owned either by you or by the cohort's GitHub organization, and that single repo is the home for everything you build over the next two weeks. Here is the whole workflow, described so you know what is happening at each step and, just as importantly, what the instructor sees on the other side. (ASSIP does not use GitHub Classroom; we use a plain template repo plus a shared cohort organization, which gives you the same private-repo, instructor-visible setup with fewer moving parts.)

**Creating your repo from the template.** Prof. Gao posts the URL of the cohort's template repo (something like `https://github.com/ASSIP-COHORT-ORG/capstone-template`). On that page, click *Use this template → Create a new repository*, and fill in three things: the **owner** (either your own GitHub account or the cohort organization — your pod sub-leader will tell you which we are using this summer), the **name** (`capstone-2026-<your-github-username>`, to keep the cohort consistent), and the **visibility** set to **Private**. That last setting is non-negotiable: the repo may reference licensed data and will hold your in-progress PAP, so only you and the people you explicitly invite should see it. Once created, GitHub copies the template into your new repo with one commit; you are the owner (or admin, if it sits in the cohort org), and from this moment on, **the repository is the submission** — there is no separate upload at the end of Week 8.

**Inviting the instructor as a collaborator.** Because the repo is private, Prof. Gao and your pod sub-leader cannot see it until you grant them read (or write) access. On the repo page, go to *Settings → Collaborators → Add people* and add the GitHub usernames your sub-leader gives you on day one — typically Prof. Gao plus your pod's sub-leader, both at *Read* permission (they need to see your commits and clone your repo; they do not need to push to it). If your repo lives inside the cohort GitHub organization, this step may already be handled by an org-level team — confirm with your sub-leader. Either way, **before you push anything sensitive, verify that the right people (and only the right people) can see the repo.** This is the equivalent of GitHub Classroom's "roster" step, just done by hand once.

**Cloning it to where you work.** Once the repo exists on GitHub, clone it to the machine where you will work (the ASSIP container, or GMU infrastructure if you touch licensed data):

```bash
git clone https://github.com/ASSIP-COHORT-ORG/capstone-2026-yourusername.git
cd capstone-2026-yourusername
```

(If the repo lives under your personal account instead of the cohort org, substitute your username for `ASSIP-COHORT-ORG` in the URL — GitHub shows the exact clone URL in the green *Code* dropdown on the repo page.) If you scaffolded a layout by hand in Step 1 and want to push *that* up rather than clone the template, you would instead create an *empty* private repo on GitHub and connect your local folder to it with `git remote add origin <url>` followed by `git push -u origin main`; but the common path is template-first, because the template already has the right shape.

**The commit / push loop.** This is the rhythm of the whole capstone. You make changes (edit the README, add a data card, write a pull script), you *stage* what you want to record, you *commit* it with a message that says what changed, and you *push* it up to GitHub so it is backed up and visible to the instructor:

```bash
git add README.md data-cards/fred.md     # stage specific files (not "git add ." blindly)
git commit -m "Add README and FRED data card"
git push                                  # send commits to GitHub (origin)
```

A commit is a snapshot with a message and a timestamp; a push uploads your local commits to the remote. Commit *often* and in *meaningful units* — "Add FRED data card," not "stuff" — because your commit history is a narrative of how the project was built, and (Step 6) it is the very thing that date-stamps your pre-analysis plan. Prefer `git add <specific files>` over a blind `git add .`, because the second is exactly how people accidentally stage a 2 GB CRSP file or a `.env` full of keys; your `.gitignore` (Step 5) is the safety net, but staging deliberately is the first line of defense.

**The instructor view.** On the other side, Prof. Gao does not see your laptop — he sees your *pushed commits* on GitHub. Once you have added him and your sub-leader as collaborators (or once your repo is in the cohort org), they can browse your repo at its URL just as you do: a single page listing every file, every commit, and every tag, with the latest commit time visible at a glance. Concretely, when you push, the instructor can: read your commit history (so they can see *when* you filed your PAP relative to your first regression — the whole point of Step 6), open any file at any commit, leave review comments on lines of code, and clone your repo to run it themselves. The cohort wiki keeps a roster table linking each intern's GitHub username to their repo URL, so a sub-leader skimming pod progress on a Friday afternoon can click straight from "Maya R." to her latest commit. This is why "the repo is the deliverable" is literal: there is no separate upload, no email submission, no Canvas dropbox. What you push is what is graded, and the history of how you got there is part of what is graded. The corollary is the discipline this whole lab is about — **never push licensed data or secrets**, because once a file is in a pushed commit it is in the history *forever*, even if you delete it in a later commit, and on a repo with collaborators the instructor (and GitHub's servers) already have it.

---

## Step 3 — Pin the environment

Here is a sentence that has killed more reproductions than any statistical error: *"It worked on my machine."* Your analysis does not run on "Python" — it runs on a specific Python interpreter with specific versions of pandas, numpy, statsmodels, and a dozen other libraries, each of which changes behavior across versions. A `groupby` that returned a sorted result in pandas 1.x, a default that flipped in 2.x, a function that was removed, a numerical routine whose algorithm was improved so the last decimal moved — any of these can make the *same code* produce *different numbers* on a different machine. **Pinning the environment means recording the exact versions** so that anyone — a referee, a teammate, future-you on a new laptop — can reconstruct the identical software stack and get the identical result. Without it, "reproducible" is a hope, not a property.

You pin with a conda **`environment.yml`**: a single file that names the environment, its channels (where conda fetches packages), the Python version, and every dependency. Create `environment.yml` in your repo root with the stack from CONVENTIONS §5, pinned to `python=3.11`:

```yaml
name: capstone
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  # core scientific stack — pin major/minor so reruns are stable
  - pandas>=2.2
  - numpy
  - scipy
  - matplotlib
  - pyarrow            # Parquet I/O for the raw cache (Ch 7.2)
  # econometrics
  - statsmodels
  - linearmodels
  - pyfixest
  # data acquisition
  - requests
  - pandas-datareader  # FRED, Stooq (Ch 7.2)
  - pip:
      # packages best installed from PyPI
      - wrds            # WRDS Cloud access — licensed data stays on GMU infra (§5)
      - yfinance        # free price data, prototyping only (Ch 7.2)
```

Two reasons this exact form. First, it matches CONVENTIONS §5's stack — the same libraries every chapter notebook uses, so your environment is consistent with the camp's. Second, the `name: capstone` and `python=3.11` are the load-bearing pins: a fresh machine reads this file and builds the *same* interpreter and the *same* package set. Create the environment and activate it:

```bash
conda env create -f environment.yml     # reads the file, solves and installs
conda activate capstone
```

Now the subtle, professional step: **freeze the exact solved versions.** The `environment.yml` above pins Python and the majors, but conda's solver picks specific patch versions of every dependency and sub-dependency when it installs. To make the environment reconstructible *to the patch*, export what the solver actually chose into a lock-style file, and commit *that* alongside the human-readable `environment.yml`:

```bash
conda env export --no-builds > environment.lock.yml   # exact versions the solver chose
git add environment.yml environment.lock.yml
git commit -m "Pin conda environment (python=3.11 + CONVENTIONS §5 stack)"
```

The division of labor is deliberate: `environment.yml` is the *human-readable intent* (these libraries, this Python), readable in your README and easy to edit; `environment.lock.yml` is the *machine-exact record* (every package at the version it resolved to) that makes a rebuild bit-for-bit. A reviewer who wants the friendly version reads the first; a reviewer who wants byte-identical results rebuilds from the second. `--no-builds` drops the OS-specific build hashes so the lock file is portable across the camp container and Hopper, which is usually what you want for a student project. `[CHECK]` — if your project must reproduce on a *different OS* than where you exported, confirm the lock file solves there, since a few packages have platform-specific pins; the camp container is the reference platform.

Why this matters concretely, in one line you should be able to say out loud: *"My results were produced under `environment.lock.yml`; rebuild that environment and you rebuild my numbers."* That sentence is the difference between a result a skeptic can check and one they have to take on faith.

---

## Step 4 — Write the README and a data card per source

A repository a stranger cannot understand is not reproducible in any sense that matters. Two documents make yours legible: a **README** that orients a reader to the whole project, and a **data card** per source that documents where each dataset came from and how to re-pull it.

**The README — what, why, how-to-run.** Put `README.md` in the repo root; it is the first thing GitHub shows and the first thing any reader reads. Keep it short and answer three questions: *what* is this project, *why* does it exist (the research question), and *how* do I run it (the exact commands). A skeleton you can fill in:

```markdown
# Conditional Racial Disparity in Mortgage Denial (Capstone — Maya R.)

## What
An empirical study of whether minority mortgage applicants face higher denial
rates than otherwise-similar applicants, and whether the gap is smaller for
algorithmic (FinTech) lenders. Outcome: HMDA denial indicator. See the
pre-analysis plan in `PRE-ANALYSIS-PLAN.md` (filed as tag `pap-filed`).

## Why
Fair-lending disparities are well documented; this project asks the conditional
question with a pre-registered design, to separate a confirmatory test from a
post-hoc search (Ch 7.3). Primary specification and identifying assumption are
stated in the PAP.

## Data
Sources are documented in `data-cards/`. All raw pulls are cached to `data/raw/`
(git-ignored) and logged to `logs/pulls.jsonl`. **No licensed data is committed.**
- HMDA (CFPB Data Browser) — public — see `data-cards/hmda.md`
- FRED macro controls — public — see `data-cards/fred.md`

## How to run
1. Build the environment:
       conda env create -f environment.yml
       conda activate capstone
2. Set required secrets (NEVER commit these):
       export FRED_API_KEY=...          # your own key; see data-cards/fred.md
       export SEC_USER_AGENT="Maya R. maya@gmu.edu"
3. Pull the data (writes to data/raw/, logs to logs/pulls.jsonl):
       python src/pull_data.py
4. Build the analysis dataset, then run notebooks in order:
       python src/build_dataset.py
       jupyter lab notebooks/

## Reproducibility notes
- Environment pinned in `environment.lock.yml`.
- Data vintages pinned in each data card.
- PAP filed before any confirmatory regression: `git show pap-filed`.
```

Notice what the README does *not* do: it does not paste API keys (it tells you to `export` them), and it does not promise that a reader can re-pull licensed data — it points them at the data cards, which are honest about what is public and what is GMU-only. The README is the map; the data cards are the territory.

**A data card per source.** For every data source your project touches, write one card under `data-cards/<source-slug>.md`. The card is the spec sheet you return to while coding, and it follows the same six-field structure Chapter 7.2 used for every source, so cards are comparable at a glance. A filled-in example for FRED (`data-cards/fred.md`):

```markdown
# Data Card — FRED (Federal Reserve Economic Data)

- **Coverage:** macro/financial time series (UNRATE, MORTGAGE30US, DGS10, ...).
- **Key identifiers:** the series ID string (e.g. `UNRATE`).
- **Access:** `pandas-datareader` (no key) or `fredapi` (free key in `FRED_API_KEY`).
  Pull code: `src/pull_data.py::pull_fred`.
- **License:** public; FRED aggregates BLS/BEA/etc. — cite the *underlying* source (§6).
- **Rate limits / gotchas:** ~120 req/min per key; many series are *revised* — for a
  point-in-time design use an ALFRED vintage, not the latest (Ch 7.2.4).
- **Reproducibility pin:** pulled 2026-05-15, latest vintage; cached to
  `data/raw/fred_*.parquet`; logged in `logs/pulls.jsonl` with content hash.
```

Write one of these for *each* source. For a licensed source (CRSP, Compustat), the card additionally states the snapshot date you pinned and, in the license field, the non-negotiable line: *licensed to GMU; analyzed only on GMU infrastructure; raw data never committed.* The data card is where the abstract rule of CONVENTIONS §5 becomes a concrete sentence attached to a concrete file, so that six months from now neither you nor a teammate can plead ignorance about what may leave the building.

---

## Step 5 — The `.gitignore` discipline

This is the step that, done wrong, can get a student into genuine trouble — a license violation, a leaked API key scraped by a bot within minutes of a push — and, done right, makes those failures *impossible* rather than merely unlikely. The tool is a `.gitignore` file: a list of patterns that tells Git which files to *never* track. The discipline has two non-negotiable rules.

**Rule one — never commit licensed raw data.** CRSP, Compustat, IBES, TRACE, and the cleaned Thomson 13F panel are *licensed*, not public. GMU pays for them; the license permits use by GMU researchers *on GMU systems*. Committing any of those bytes to a Git repo — even a private one — is redistribution outside the licensed walls, which violates the license. So the entire `data/` tree is git-ignored, and the licensed bytes live only in `data/raw/` on GMU infrastructure (Chapter 7.2, Rule 2). What you commit instead is the *recipe*: the pull code in `src/`, the data cards, and the `logs/pulls.jsonl` log with its content hashes. A reviewer with GMU access can re-run the recipe and check the hash; a reviewer without it cannot get the data — which is correct, because the license forbids you from shipping it.

**Rule two — never commit secrets.** Your API keys, your WRDS credentials, your `.env` file. A key is a password; the instant it lands in a *pushed* commit it is in your repo's history forever (deleting it later does not remove it from history), and bots scrape public GitHub for exactly such strings within minutes. Keys live in environment variables or a `.env` file that is *git-ignored and never committed* (Chapter 7.2, Rule 1). Your code reads them with `os.environ[...]`; the repo never contains them.

Create `.gitignore` in the repo root:

```gitignore
# === Never commit data ===
# Licensed raw data (CRSP/Compustat/TRACE) stays on GMU infrastructure (CONVENTIONS §5).
# Public raw data is cached here too but is large/regenerable — keep it out of git.
data/raw/*
data/processed/*
!data/raw/.gitkeep         # keep the folder structure, not its contents
!data/processed/.gitkeep

# === Never commit secrets ===
.env
.env.*
*.key
*.pem
.pgpass                    # WRDS credentials file

# === Caches and build noise ===
__pycache__/
*.pyc
.ipynb_checkpoints/
*.parquet                  # belt-and-suspenders: never commit a cached table anywhere
```

A few things to understand in this file. The pattern `data/raw/*` ignores everything *inside* `data/raw/`, and the negation `!data/raw/.gitkeep` then *un-ignores* the placeholder so the folder structure survives a clone while its contents never do. (The order matters and the directory-level form `data/raw/*` plus a negation is what makes the exception work — a bare `data/` would swallow the `.gitkeep` too.) The `*.parquet` line is deliberate belt-and-suspenders: even if a stray cache file lands outside `data/`, it still cannot be committed. And `.pgpass` is the file the `wrds` package stores credentials in — ignoring it by name is one more guard on your licensed-data access.

Now **verify** it, because an untested `.gitignore` is a hope, not a guarantee. Git ships a tool that tells you exactly whether a path is ignored. Create a couple of dummy files that *should* be blocked and confirm Git refuses them:

```bash
# create files that MUST be ignored
touch data/raw/crsp_msf.parquet .env

# git check-ignore prints any path that IS ignored (and exits 0); silence = NOT ignored
git check-ignore -v data/raw/crsp_msf.parquet .env
# expected output names both files with the .gitignore rule that caught them

# the real proof: stage everything and look at what Git would actually track
git add -A
git status --short
# you should see .gitignore and the .gitkeep placeholders staged,
# and NEITHER crsp_msf.parquet NOR .env anywhere in the list

rm data/raw/crsp_msf.parquet .env     # clean up the dummies
```

If `git status --short` shows `crsp_msf.parquet` or `.env` staged for commit, *stop* — your `.gitignore` has a hole, and you fix it before you ever `push`. This two-minute check is the cheapest insurance in the entire camp. Commit the working `.gitignore`:

```bash
git add .gitignore data/raw/.gitkeep data/processed/.gitkeep
git commit -m "Add .gitignore: block licensed data and secrets"
```

One last habit worth internalizing: the `.gitignore` is the *automatic* guard, but the *deliberate* guard is staging files by name (`git add README.md`, not `git add .`). Two independent layers — a machine rule and a human habit — are why a leaked key or a committed CRSP file should never happen to you, not merely rarely happen.

---

## Step 6 — File the pre-analysis plan as a tagged commit

Now the step that ties this lab to Chapter 7.3 and turns your repo into an instrument of scientific honesty. Recall the argument: a pre-analysis plan only constrains you if its contents are *fixed before* you analyze your outcomes, and the only way to prove that to a skeptic is a credible time-stamp. Chapter 7.3 named the mechanism for this camp — **your Git history is your registry, and you file the PAP as a tagged commit.** This step is where you do it.

First, the PAP itself must exist as a committed file. You wrote it in nb7.3 (the PAP companion emitted a filled-in template) and saved it as `PRE-ANALYSIS-PLAN.md`. Commit it as its own clean commit, with nothing else mixed in, so the commit is unambiguously "the moment the plan was filed":

```bash
git add PRE-ANALYSIS-PLAN.md
git commit -m "File pre-analysis plan (pre-registration)"
```

Now **tag** that commit. A Git *tag* is a permanent, human-named pointer to a specific commit; an *annotated* tag (the `-a` form) additionally stores its own message, author, and — the part that matters — a date. This is your registration time-stamp:

```bash
git tag -a pap-filed -m "PAP filed before any confirmatory regression (Ch 7.3)"
git push origin pap-filed     # push the tag so the instructor can see it
```

Confirm it landed and read back its message and date:

```bash
git show pap-filed            # shows the tagged commit, its date, and the PAP diff
git tag -n5 -l pap-filed      # shows the tag and its annotation message
```

Why this is a *cryptographic* promise and not just a sticky note. Git names every commit by a SHA-256 hash of its full contents *and the hash of its parent* — so each commit's identity depends on the entire history before it. A commit made *after* you ran your confirmatory regression cannot be retroactively inserted *before* the `pap-filed` commit without changing every subsequent hash, which would visibly rewrite the whole pushed history (and the instructor, and GitHub's servers, already hold the original). In plain terms: **anyone can verify that the PAP existed, in exactly this form, before the commits that contain your confirmatory results.** That is the entire point of Chapter 7.3's "register by time-stamping." The tag is the seal; the hash chain is what makes the seal unbreakable.

The discipline that follows from this is the order of operations. The PAP is tagged *first*. Only *after* `pap-filed` do you run the confirmatory regressions (nb7.5 is frozen until exactly this moment, per Chapter 7.3). When you inevitably deviate from the plan — a control drops out for collinearity, 2020 needs special handling — you do *not* silently edit the tagged PAP (you cannot, honestly; the tag points at the old version). Instead you record every departure, dated, in `DEVIATIONS.md`, exactly as Chapter 7.3's deviation log prescribes, and commit it *after* `pap-filed`:

```bash
# later, when reality intrudes — NEVER edit the tagged PAP; log the deviation instead
git add DEVIATIONS.md
git commit -m "Deviation: cluster by county (lender ID corrupted, 4% of rows); not outcome-driven"
```

The commit history now tells the honest story by construction: here is the plan (tagged, dated, immutable), and here — in commits that provably come *after* — is everything that changed and why. A referee reading that history trusts you *more*, not less, because the seams are visible. That is the reveal of Chapter 7.3 made operational in your repository: the tag is not paperwork, it is the difference between a number that *tested* a hypothesis and a number that was *selected* to look like it did.

---

## You're done when…

Use this checklist. A box is checked only when you can point to the command output or the file that proves it — this is exactly the audit a referee (or Prof. Gao, browsing your repo on GitHub) would run on your code.

- [ ] **Layout.** Your repo has `README.md`, `environment.yml`, `.gitignore`, `PRE-ANALYSIS-PLAN.md`, and the directories `data/{raw,processed}/`, `src/`, `notebooks/`, `paper/`, `logs/`, `data-cards/`. A fresh `git clone` reproduces the structure (the `.gitkeep` files travel).
- [ ] **Cohort GitHub.** You created your private repo `capstone-2026-<your-github-username>` from the cohort template, added Prof. Gao and your pod sub-leader as collaborators (or confirmed the cohort-org team grants them read access), and `git push` puts your commits where the instructor can see them. The repo URL is logged on the cohort wiki roster.
- [ ] **Environment pinned.** `conda env create -f environment.yml` builds on a fresh machine; `environment.lock.yml` records exact versions; both are committed. You can say the sentence: *"my results were produced under `environment.lock.yml`."*
- [ ] **README.** A stranger can read `README.md` and answer *what / why / how-to-run* — including the exact commands to build the env, set secrets via `export`, and run the pull — without asking you anything.
- [ ] **Data cards.** There is one card per source under `data-cards/`, each naming coverage, identifiers, access path, license, and the reproducibility pin (vintage / snapshot / accession). Licensed sources state "GMU-only, never committed."
- [ ] **`.gitignore` verified.** `git check-ignore -v data/raw/test.parquet .env` reports *both* as ignored, and `git status --short` after `git add -A` shows *no* data file and *no* `.env` staged. You proved it, not just hoped it.
- [ ] **No secrets, no licensed data, anywhere in history.** A scan of your tracked files (`git ls-files`) shows no `.env`, no `*.parquet`, no CRSP/Compustat extract, no hard-coded key.
- [ ] **PAP tagged.** `git show pap-filed` displays your pre-analysis plan with a date *before* any confirmatory-regression commit; the tag is pushed (`git ls-remote --tags origin` lists `pap-filed`). Deviations, if any, are in `DEVIATIONS.md` in commits that come *after* the tag.

---

## Reflection questions

Answer each by pointing to a file, a command output, or a commit in your own repo.

1. **The asymmetry of reproducibility.** Chapter 7.2 closed on the idea that public data is *fully re-runnable* while licensed data is *recipe-reproducible only*. Open your repo and name, for each of your sources, exactly what a reviewer *without* GMU access could do to check your work, and what they could not. What is the single file in your repo that makes even the licensed-data part as reproducible as the license allows?

2. **Why pin to the patch?** You committed both `environment.yml` (Python + majors) and `environment.lock.yml` (every package's exact version). Construct a concrete scenario — name a library and a kind of change — in which two people running your code from `environment.yml` alone could get *different numbers*, but running from `environment.lock.yml` could not. Which file would you cite in your paper's methods section, and why both?

3. **The hole you would never find by reading.** You verified your `.gitignore` with `git check-ignore` rather than by eyeballing it. Write down one pattern you *thought* would block a file but, when you tested it, did not (or construct one — e.g., why does a bare `data/` line also swallow your `.gitkeep`?). What does this teach you about the difference between a rule that is *written* and a rule that is *verified*?

4. **What the tag actually proves — and what it does not.** Your `pap-filed` tag proves the PAP existed before your confirmatory commits. State, in one sentence each, (a) what scientific failure this *does* prevent (tie it to the garden of forking paths, Ch 7.3.1) and (b) one failure it does *not* prevent (hint: a pre-registered design can still be a *bad* design — Ch 7.3.5's "false confidence" peril). Which Week-7 deliverable addresses (b)?

5. **From repo to capstone.** This repository is your Week-8 deliverable too. Write the three commands a teammate joining next week would run, in order, to go from a fresh clone to your first reproduced figure — and identify the one place in that sequence where they would need something you cannot put in the repo (and what your README tells them to do about it).

---

## Where this connects

You now have a research repository that is reproducible *as a repository*, not as a lucky collection of scripts: a sensible layout, an environment pinned to the patch, a README and data cards a stranger can follow, a `.gitignore` you *verified* blocks both licensed data and secrets, and a `pap-filed` tag whose date no one can quietly move. Every piece traces to a Week-7 chapter — the pinned/cached/logged pull discipline of Chapter 7.2, the pre-registration-by-tag mechanism of Chapter 7.3 — and every piece is now a concrete file or command you can point a skeptic to.

The repo does not stop here; it *is* the rest of the camp. Chapter 7.4 fills `src/` with the dataset-build and the survivorship/look-ahead checks the PAP referred to; Chapter 7.5's identification memo commits alongside the PAP (the memo argues the pond is the right pond, where the PAP promised you would not fish — you need both); nb7.5's first-look regressions run *only after* `pap-filed`; and all of Week 8 — the full analysis, the figures in `paper/`, the write-up — commits into this same repository, under this same environment, governed by this same pre-registered plan. The habit underneath is the one this lab exists to install: **a result a stranger cannot reconstruct is not yet a result.** You built the thing that makes yours reconstructible. Keep committing into it.

---

### References

- Olken, B. A. (2015). Promises and Perils of Pre-Analysis Plans. *Journal of Economic Perspectives*, 29(3), 61–80.
- Wharton Research Data Services (WRDS). *Data access and licensing terms.* (Licensed; GMU-affiliated use on GMU infrastructure — CONVENTIONS §5.)
- Consumer Financial Protection Bureau. *HMDA Data Browser.* `https://ffiec.cfpb.gov/data-browser/` (public; vintage pinned per run — `[CHECK]` the snapshot date on the camp container).
- GitHub. *Creating a repository from a template*, *Inviting collaborators to a personal repository*, and *Managing files with .gitignore.* `https://docs.github.com/` (workflow and tool reference for the cohort template-and-collaborators flow used in Step 2).
