# D.4 — The Replication Packet Standard

This is the binding standard. Lab 7 builds it, Lab 8 finishes it, the capstone is graded against it, and Chapter 8.5 tells you *why* it matters; this section tells you *exactly* what a passing packet contains, down to the file names and the one command. Where D.1–D.3 govern what a single table or figure looks like on the page, D.4 governs the *machine* that produces every one of them. A packet is not documentation you write about your project. It is the project, arranged so that a stranger can rebuild it.

Here is the bar, stated once so the rest of the section is just the unpacking of it. **A grader clones your repository onto a machine that has never seen your work, types one command, and watches every table and figure in your paper regenerate from raw inputs to a compiled PDF — with no editing, no emailing you for a missing file, and no manual steps.** That sentence is the whole standard. If your packet does that, it passes; if it does that only "mostly," it fails, because "mostly reproducible" is to a referee exactly what "mostly correct" is to a proof. The reveal under all the mechanics below is that reproducibility is not a courtesy you extend to the reader — it is the form your credibility takes once you stop talking and the skeptic is alone with your folder.

---

## D.4.1 The repository layout

A packet has a fixed shape, and the fixedness is the point: a grader who has seen one packet knows where to look in yours. Lay the repository out exactly like this.

```
your-project/
├── README.md                 # what / why / how-to-run (the run section is ONE line)
├── environment.yml           # human-readable env: python=3.11 + the stack
├── environment.lock.yml      # machine-exact env: every package pinned to a version
├── Makefile                  # `make all` regenerates EVERYTHING (or run_all.py / run_all.sh)
├── config.py                 # the single fixed SEED and shared paths live here
├── .gitignore                # data/raw/ and secrets are listed here — never committed
├── data/
│   ├── raw/                  # GITIGNORED. Licensed raw data lives here and is NEVER committed
│   ├── processed/            # GITIGNORED. Built by code; a rebuild must recreate it from scratch
│   └── cards/                # data cards (committed): one per source, see D.4.3
├── src/                      # logic, in run-order: 01_pull.py, 02_build.py, 03_analysis.py
├── notebooks/                # the story / exploration, mirroring src by chapter
├── paper/
│   ├── main.tex              # the manuscript; \input{tables/...} and \includegraphics{figures/...}
│   ├── tables/               # GITIGNORED or committed-as-generated; WRITTEN by src, never by hand
│   ├── figures/              # same: written by src/03_analysis.py, never pasted
│   └── references.bib
└── logs/
    └── pulls.jsonl           # provenance log: what was pulled, when, with content hashes
```

The division of labor is the rule from Lab 7: **logic lives in `src/`, the story lives in `notebooks/`, derived data and outputs live in `data/processed/` and `paper/tables|figures/` and are *built, never committed by hand*.** The single most important line in the whole tree is the one in `.gitignore` that excludes `data/raw/`. That is not a convenience; it is a license-compliance and honesty requirement, and D.4.2 explains why.

---

## D.4.2 Data: an access script and data cards, never the licensed raw bytes

The first instinct of a beginner is to commit everything, including the raw data, "so it's all in one place." For public data that is correct. For licensed data it is a license violation and an automatic packet failure, and the distinction is the most important data decision in the packet.

**Public data ships *in* the packet.** If your raw inputs are freely redistributable — Fama–French factors from Ken French's library, an SEC EDGAR filing you downloaded, a Yahoo Finance price series, an HMDA public file — cache them in `data/raw/`, pin their vintage (the exact download date and, where the source offers one, the release version), and commit them so the packet is fully self-contained and re-runnable offline. A grader with no credentials can rebuild your entire result.

**Licensed data does *not* ship.** CRSP, Compustat, anything pulled through WRDS, Bloomberg exports — the license forbids redistribution, full stop (CONVENTIONS §5). You do not commit it, you do not email it, you do not put it in a "private" repo and share the link. It stays read-only on GMU infrastructure (Hopper / the WRDS Cloud), and `data/raw/` is gitignored precisely so you cannot commit it by accident. This is the line a grader checks first, because committing a single CRSP extract is the kind of mistake that follows a researcher.

What ships *instead* of the licensed bytes is the **data-access script** in `src/` — a bounded, pinned query that *reconstructs* the licensed dataset for anyone who has the same WRDS access. It names the library and table, fixes the date range and the universe, pins the snapshot date, and pulls secrets from the environment, never from the file:

```python
# src/01_pull_data.py — reconstructs the licensed extract for a user WITH WRDS access.
# Secrets come from the environment ONLY (CONVENTIONS §5); nothing sensitive is hard-coded.
import os, json, hashlib, datetime as dt
import wrds

WRDS_USER = os.environ["WRDS_USERNAME"]          # set by the user: export WRDS_USERNAME=...
SNAPSHOT  = "2026-05-15"                          # the CRSP/Compustat vintage, pinned and documented

db = wrds.Connection(wrds_username=WRDS_USER)     # password via ~/.pgpass or the WRDS prompt, never in code
df = db.raw_sql(
    """
    SELECT permno, date, ret, prc, shrout
    FROM crsp.msf
    WHERE date BETWEEN '2010-01-01' AND '2024-12-31'
    """
)
df.to_parquet("data/raw/crsp_msf.parquet")        # lands in the GITIGNORED dir; never committed

# Provenance: log WHAT we pulled, WHEN, and a content hash so a re-puller can verify identical bytes.
digest = hashlib.sha256(open("data/raw/crsp_msf.parquet", "rb").read()).hexdigest()
with open("logs/pulls.jsonl", "a") as f:
    f.write(json.dumps({
        "source": "crsp.msf", "snapshot": SNAPSHOT,
        "pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "rows": len(df), "sha256": digest,
    }) + "\n")
```

This is the **asymmetry of reproducibility** from Lab 7: public data is *fully* re-runnable by anyone; licensed data is *recipe-reproducible* by anyone with access. The `logs/pulls.jsonl` line, with its content hash, is what lets a reviewer who *does* have WRDS re-pull and confirm they got byte-identical data — the hash is the proof, not your assurance. Your README states honestly which inputs are which, so nobody types `make all` expecting CRSP to materialize from nothing.

**Data cards.** Every source gets a card under `data/cards/` (mirroring the `data-cards/` convention in CONVENTIONS §7), and the cards *do* ship. A data card is a one-page provenance sheet a stranger reads to understand an input without touching it: the source and its URL or library path; the vintage / snapshot date; the license and whether it permits redistribution (this is the field that decides §4.2 for that source); the unit of observation; the columns you actually use and their definitions; the filters you applied and the row counts before and after; and any known quirks (the malformed 2018 column, the suspension of a series). The card is where the cleaning ordeal that Chapter 8.3 banished from the paper's data section legitimately lives. A grader reads the cards to know whether your sample is what you claim before trusting a single number built on it.

---

## D.4.3 Code in run-order

The scripts in `src/` and the notebooks in `notebooks/` must make their *order* unambiguous, because a reviewer should never have to guess which script runs first. Number them: `01_pull_data.py`, `02_build_dataset.py`, `03_analysis.py`, `04_make_figures.py` — whatever ordering your single entry point enforces. The numbering is not decoration; it is the contract that `make all` executes top to bottom.

Three rules keep the code honest. First, **no step reads a file an earlier step did not write** — the pipeline is a chain from raw bytes forward, and a script that secretly depends on a file you made by hand in a notebook one afternoon will break on a fresh clone, which is exactly the break the honesty test (§4.7) exists to catch. Second, **the analysis scripts *write* the paper's tables and figures**; `03_analysis.py` emits `paper/tables/main_results.tex` and `paper/figures/event_study.pdf`, built to the D.1–D.3 standard (named standard errors, defined stars, disclosed fixed effects and clustering, legible-in-grayscale figures), and the manuscript `\input`s and `\includegraphics`es them. Nothing is typed into the manuscript by hand. Third, **logic in `src/`, story in `notebooks/`**: a notebook may explore and narrate, but anything load-bearing — anything that produces a number the paper reports — is a function in `src/` that the entry point calls, so the result does not depend on which cells a human happened to run in which order.

---

## D.4.4 A pinned environment file (and its lock)

"It worked on my machine" is the oldest excuse in computing, and the packet abolishes it by making your machine and the grader's machine into the *same* machine. You ship two files.

The human-readable `environment.yml` declares the stack at the level a person reads — Python 3.11 and the CONVENTIONS §5 libraries, with the loose version floors the project was written against:

```yaml
# environment.yml — human-readable. `conda env create -f environment.yml`
name: your-project
channels: [conda-forge]
dependencies:
  - python=3.11
  - pandas>=2.2
  - numpy
  - scipy
  - statsmodels
  - linearmodels
  - pyfixest
  - matplotlib
  - pyarrow
  - pip
  - pip:
      - wrds
      - yfinance
      - pandas-datareader
```

The machine-exact `environment.lock.yml` records *every* package — including the transitive dependencies you never named — at the exact version the solver chose, so the environment is bit-for-bit reconstructible months later when the loose floors would otherwise resolve to newer, subtly different versions. You generate it once the project works and commit it alongside the readable file:

```bash
# Freeze the EXACT solved environment after the project runs end-to-end:
conda env export --no-builds > environment.lock.yml
```

The sentence you must be able to say out loud, and the one that makes the lock file worth the trouble: *"my results were produced under `environment.lock.yml`; rebuild that environment and you rebuild my numbers."* The readable file is for a human who wants to understand the stack; the lock file is for the machine that must reproduce it. A packet that ships only the readable file has left a door open for the solver to pick a `pandas` that changed a default and quietly moved a number.

---

## D.4.5 A fixed, named SEED

Anywhere your code uses randomness — a bootstrap confidence interval, a train/test split, a permutation test, a synthetic-control placebo, a Monte Carlo — it must draw from a *single, named constant* set once, not from seeds scattered ad hoc through the scripts. Without a fixed seed your bootstrap interval is *different on every run*, which means your headline interval is, strictly, irreproducible: the grader runs your code and gets `[1.2, 2.4]` where your paper said `[1.3, 2.3]`, and now — fairly — they doubt everything. With a fixed seed the random parts come out *identical*, every run, on every machine.

```python
# config.py — ONE seed, imported everywhere randomness happens.
SEED = 20260815   # any fixed int; here, the conference date. The point is FIXED and NAMED.

# at the top of every script/notebook that uses randomness:
import numpy as np
from config import SEED
rng = np.random.default_rng(SEED)     # modern NumPy: a seeded Generator, not legacy np.random.seed()
# every draw goes THROUGH rng — rng.choice(...), rng.permutation(...), bootstrap resamples — and
# you PASS rng into your functions rather than reaching for a global, so each step's randomness is explicit.
```

The discipline is *one* seed, set *once*, threaded through *every* stochastic step, and recorded in the README so a grader knows the number was fixed *before* results, not tuned after. A seed you *searched over* to get a prettier interval is p-hacking with extra steps — the garden of forking paths (Ch 7.3) wearing a disguise — and the pre-analysis-plan tag from Lab 7 is what proves you did not. Use `np.random.default_rng(SEED)`, not the legacy global `np.random.seed()`, because a `Generator` you pass explicitly makes visible exactly which randomness each function consumes.

---

## D.4.6 One entry point: `make all` / `run_all`

This is the one-click. A single command runs the whole pipeline *in order* — pull or load the cached data, build the analysis dataset, run every estimation, regenerate every figure and table, and compile the paper to PDF — so a fresh clone goes from raw inputs to a finished document with no human in the loop. Pick one of the two equivalent shapes; the Makefile is the conventional choice because its dependency graph rebuilds only what changed during development, while still supporting a full `clean` rebuild for the honesty test.

```makefile
# Makefile — `make all` regenerates EVERYTHING from raw inputs to paper/main.pdf.
.PHONY: all data analysis paper clean

all: paper

data:                       ## pull (licensed) or load (public) + build the analysis dataset
	python src/01_pull_data.py
	python src/02_build_dataset.py

analysis: data              ## estimate; WRITE paper/tables/ and paper/figures/ (deterministic via SEED)
	python src/03_analysis.py

paper: analysis             ## compile the manuscript, pulling in the just-built tables/figures
	cd paper && latexmk -pdf main.tex

clean:                      ## delete every derived output so a rebuild is honest
	rm -rf data/processed/* paper/tables/* paper/figures/* paper/main.pdf
```

```bash
# run_all.sh — same idea, no make required: `bash run_all.sh`
set -euo pipefail                 # stop on the FIRST error; never silently half-build and call it done
python src/01_pull_data.py
python src/02_build_dataset.py
python src/03_analysis.py         # tables/figures written here, deterministically (fixed SEED)
( cd paper && latexmk -pdf main.tex )
echo "Rebuilt paper/main.pdf from raw inputs. Compare to the committed PDF."
```

The non-negotiable property under all of this: **the figures and tables in your paper are *generated by the code*, never pasted by hand.** The instant a human copies a number out of a notebook into the manuscript, the chain breaks, the packet stops being one-click, and worse — the pasted number can silently drift out of sync with the code that supposedly produced it, so the paper claims `1.83` while the live code now yields `1.79` and nobody notices until a referee does. The whole pipeline must be *machine-traversable* from raw bytes to the PDF on the screen.

---

## D.4.7 The honesty test: `make clean && make all`

There is exactly one test that proves the packet is real, and you run it on yourself before any grader does: **delete every derived file and rebuild from nothing.**

```bash
make clean && make all      # or: bash run_all.sh after manually clearing derived outputs
```

If the paper comes back *identical* — same tables, same figures, same numbers, same PDF — the packet is real and one-click. If anything differs, or anything errors, you have just discovered, in private, one of two things: a hand-edit (a number you typed into the manuscript that the code does not actually produce) or a hidden dependency (a step that read a file no earlier step wrote). Either way you found it before a reviewer did, which is the entire reason to run it. The test is unforgiving on purpose. A packet that has never survived `make clean && make all` is a packet whose author is *hoping* it reproduces, and hope is not the standard.

---

## D.4.8 The provenance stamp

The last load-bearing piece is a small block, written by the run itself, that records *the conditions under which these specific numbers were produced* — so that if a result is ever questioned, there is a record of the world it came from. Have `03_analysis.py` emit it, and reproduce it in the README:

```python
# emitted by the run into paper/provenance.txt and echoed in the README:
import sys, numpy, pandas, statsmodels, subprocess
stamp = {
    "git_commit": subprocess.run(["git","rev-parse","HEAD"], capture_output=True, text=True).stdout.strip(),
    "built_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "python": sys.version.split()[0],
    "numpy": numpy.__version__, "pandas": pandas.__version__, "statsmodels": statsmodels.__version__,
    "seed": SEED,
    "data_snapshot": SNAPSHOT,     # the CRSP/Compustat vintage from the pull script
}
```

The stamp answers, after the fact, every "which version / which seed / which data vintage produced this?" question a skeptic can raise. It is the difference between "the numbers came from somewhere" and "the numbers came from *exactly this* commit, seed, environment, and data snapshot — here is the record."

---

## D.4.9 The grader's checklist

This is the audit a grader — or Prof. Gao, at the conference — runs against your packet. It is also the audit you run on yourself before you submit. A packet passes only when every box is checked.

**Repository structure**
- [ ] The layout matches D.4.1: `README.md`, `environment.yml`, `environment.lock.yml`, `Makefile`/`run_all`, `config.py`, and the `data/`, `src/`, `notebooks/`, `paper/`, `logs/` directories.
- [ ] `.gitignore` excludes `data/raw/`, `data/processed/`, and any secrets; nothing sensitive is tracked.

**Data**
- [ ] No licensed raw data is committed anywhere in the repo's history (not just the current tree).
- [ ] Public raw inputs that *are* committed have a pinned vintage / download date.
- [ ] A data-access script in `src/` reconstructs each licensed input, with the snapshot date pinned.
- [ ] `logs/pulls.jsonl` records what was pulled, when, and a content hash for verification.
- [ ] Every source has a data card under `data/cards/` stating source, vintage, license/redistribution, unit, variables, filters, and row counts.
- [ ] The README states honestly which inputs are public (re-runnable) and which are licensed (recipe-reproducible).

**Code**
- [ ] Scripts are numbered/named so run-order is unambiguous, and the entry point enforces that order.
- [ ] No step reads a file an earlier step did not write (no hidden hand-made inputs).
- [ ] Tables and figures are *written by the code*; none are pasted into the manuscript by hand.

**Environment**
- [ ] `environment.yml` declares Python 3.11 and the CONVENTIONS §5 stack.
- [ ] `environment.lock.yml` pins every package (including transitive deps) to an exact version.

**Seed**
- [ ] A single named `SEED` lives in `config.py` and is used everywhere randomness occurs.
- [ ] Randomness uses `np.random.default_rng(SEED)` (not the legacy global), and `rng` is passed explicitly.
- [ ] The README records the seed and confirms it was fixed before results, not searched.

**One command**
- [ ] A single `make all` / `run_all` regenerates *every* table and figure and compiles the paper to PDF.
- [ ] `run_all.sh` (if used) sets `set -euo pipefail` so a failure halts the build instead of half-completing.

**Secrets**
- [ ] No credentials, API keys, or passwords appear anywhere in the code or committed files; secrets come from environment variables only (CONVENTIONS §5).

**The honesty test**
- [ ] `make clean && make all` rebuilds the paper *identically* from a fresh state, with no manual steps.
- [ ] On a *fresh clone* on a different machine, the public-data path runs end-to-end to PDF.

**Provenance**
- [ ] A provenance stamp records the git commit, build time, Python and key package versions, the seed, and the data snapshot, and it is reflected in the README.

Read this checklist the way Chapter 8.5 frames it: you are not asking the grader to *trust* you, you are inviting them to *verify* you, which is the stronger posture and the one with nothing to hide. A talk that ends with "trust me" and one that ends with "here is the one command that checks me" are received completely differently by a serious audience — the packet is what lets you be the second kind of researcher. When every box above is checked, a stranger types one command and your headline number emerges from raw bytes through your seeded, pinned, run-ordered code into a compiled PDF. That is what turns a claim about a result into a result. See D.1 for table layout and notes, D.2 for which coefficients to report and the fixed-effects/cluster/sample disclosure, and D.3 for the robustness section and the threats-and-responses table — the standards that govern what the code in this packet emits onto the page.
