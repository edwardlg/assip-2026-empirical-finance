# B.1 Toolchain

Every regression in this book runs on the same small pile of software. The pile is not big, but the *order* you install it in matters, and the thing that breaks most beginners is not the code — it is having a slightly different version of `pandas` than the person who wrote the example, so a line that worked in the textbook throws a red error on your laptop. This section sets you up so that does not happen. By the end you will have a code editor, an isolated Python environment with every package the camp uses pinned to known-good versions, a way to run notebooks, and a working knowledge of Git — enough to never lose your work and to hand it to an instructor cleanly.

The trick we are revealing here is the one professional researchers learn the hard way: **reproducibility is not a virtue you add at the end; it is the environment you set up at the start.** A result you cannot regenerate on a fresh machine is, for scientific purposes, a result you do not have. So we build the fresh machine first.

## B.1.1 What you are installing, and why each piece exists

There are exactly four moving parts, and it helps to know the job of each before you touch an installer.

1. **A Python distribution and an environment manager.** We use **Miniconda** (or the near-identical **Miniforge**, if you prefer the community channel). Conda does two jobs: it gives you a Python interpreter, and — more importantly — it lets you create *named, isolated environments*. An environment is a private sandbox of packages. The camp's environment will not collide with whatever Python your operating system shipped, or with a different project that needs an older `numpy`. This isolation is the single most valuable habit in the whole appendix.

2. **A code editor.** We use **Visual Studio Code** (VS Code). It is free, runs on Windows, macOS, and Linux, edits both `.py` scripts and `.ipynb` notebooks, has a built-in terminal, and talks to Git through buttons if you are not yet comfortable on the command line.

3. **The scientific Python stack**, pinned. This is the list from `CONVENTIONS.md` §5: `pandas>=2.2`, `numpy`, `scipy`, `statsmodels`, `linearmodels`, `pyfixest`, `matplotlib`, plus the data-access tools `wrds`, `yfinance`, `pandas-datareader`, `requests`, and the fast file format library `pyarrow`. We will say what each does below.

4. **Git**, the version-control system, and a free **GitHub** account. Git records the history of your project so you can undo, branch, and collaborate; GitHub stores a copy in the cloud and is how the camp distributes and collects assignments (Appendix B.2 covers GitHub Classroom in detail).

We install them in that order — conda first, because the environment is the foundation everything else sits on.

## B.1.2 Installing Miniconda

Go to the Miniconda download page and grab the installer for your operating system and your processor. On a recent Mac that means the **Apple Silicon (arm64)** build; on most Windows and Linux machines it is the **64-bit x86_64** build. If you are unsure which Mac you have, the Apple menu's "About This Mac" tells you whether the chip is Apple M-series (arm64) or Intel (x86_64). Picking the wrong architecture is the most common install snag, so check before you click.

- **Windows:** run the `.exe`. When asked, install "Just Me," accept the default location, and leave "Add Miniconda to my PATH" *unchecked* (the installer warns against it for good reason). You will use the **Anaconda Prompt** that the installer adds to your Start Menu as your conda-aware terminal.
- **macOS / Linux:** the download is a `.sh` script. Open Terminal, change into your Downloads folder, and run it with `bash`:

```shell
bash ~/Downloads/Miniconda3-latest-MacOSX-arm64.sh
```

Accept the license, accept the default install path, and when it asks whether to run `conda init`, say **yes**. That edits your shell profile so the `conda` command is available in new terminal windows.

Now **close every terminal window and open a fresh one.** This is not superstition: `conda init` only takes effect in shells started *after* it ran. In the new shell, confirm conda is alive:

```shell
conda --version
```

You should see something like `conda 24.x.x`. If the command is "not found," your terminal did not pick up the init; on Windows use the Anaconda Prompt specifically, and on macOS/Linux make sure you opened a brand-new window.

One housekeeping step makes later installs faster and avoids a class of licensing headaches with the default Anaconda channel. Point conda at the community **conda-forge** channel and turn on the faster solver:

```shell
conda config --add channels conda-forge
conda config --set channel_priority strict
```

`conda-forge` is a large, openly maintained package repository; `strict` priority tells conda to prefer it consistently, which prevents the "mixed channels" conflicts that produce the dreaded multi-minute "Solving environment..." hangs.

## B.1.3 The camp environment: `environment.yml`

Rather than installing packages one at a time (and forgetting which ones, in which order), we declare the whole environment in a single file. This file *is* the reproducibility contract from §5: anyone — you next week, an instructor, a teammate — can recreate your exact environment from it. Create a file named `environment.yml` in the root of your project folder with this content:

```yaml
# environment.yml — the 8-week camp Python environment.
# Recreate with:  conda env create -f environment.yml
# Update with:    conda env update -f environment.yml --prune
name: finlab
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas>=2.2
  - numpy
  - scipy
  - statsmodels
  - linearmodels
  - matplotlib
  - pyarrow
  - requests
  - pandas-datareader
  - jupyterlab
  - ipykernel
  # A few packages live more reliably on PyPI than conda-forge,
  # so we install them with pip *inside* this same env:
  - pip
  - pip:
      - pyfixest
      - wrds
      - yfinance
```

A few things to understand about that file, because each line encodes a decision.

- **`name: finlab`** is the environment's name. You will type `conda activate finlab` to switch into it. Pick any name you like, but be consistent; the rest of this appendix assumes `finlab`.
- **`python=3.11`** pins the interpreter exactly, per §5. We do *not* use the newest possible Python. The camp standardizes on 3.11 because every package above is known to work together on it; chasing the bleeding edge is how you end up with a package that has not yet been built for 3.13.
- **`pandas>=2.2`** is a floor, not an exact pin. The camp's code assumes the modern pandas 2.x API — for instance, `pd.append` was *removed* in pandas 2.0, which is exactly why §5 forbids it. Requiring `>=2.2` guarantees you are on the modern API. (If you ever need a fully frozen, bit-for-bit lock, you would generate a `conda-lock` file; for a teaching camp the `environment.yml` floor plus the Python pin is the right amount of strictness.)
- **The two-tier `pip:` block.** Most packages come from conda-forge, but `pyfixest`, `wrds`, and `yfinance` are most reliably installed from PyPI. The correct way to mix them is to list `pip` as a conda dependency and then nest the pip-only packages under it, *inside the same environment file*. Never run a bare `pip install` in your base conda environment — that is how environments get silently corrupted. Keeping pip nested here means the whole stack still recreates from one command.
- **`jupyterlab` and `ipykernel`** give you the notebook interface and let VS Code and JupyterLab find this environment's kernel.

### What each analysis package is for

So the import lines later in the book are not mysterious:

- **`pandas`** — tabular data: the `DataFrame`, the workhorse for everything from CRSP returns to HMDA loan records.
- **`numpy`** — fast numerical arrays; the math layer pandas sits on.
- **`scipy`** — statistical distributions, optimization, hypothesis tests beyond the basics.
- **`statsmodels`** — classical econometrics: OLS, robust and clustered standard errors (the HC1/HC2/HC3 and HAC flavors named in §3), GLM, time series.
- **`linearmodels`** — panel and instrumental-variables estimators (fixed effects, 2SLS) with a clean econometrics-flavored API.
- **`pyfixest`** — very fast high-dimensional fixed-effects regressions, mirroring R's `fixest`; the tool of choice when you have firm *and* year fixed effects on a large panel.
- **`matplotlib`** — every figure in the book.
- **`wrds`** — the official client for the WRDS Cloud (CRSP, Compustat, IBES). Covered in B.3.
- **`yfinance`** — free Yahoo Finance prices, for quick prototyping before you touch licensed data.
- **`pandas-datareader`** — pulls public series like FRED macro data straight into a DataFrame.
- **`requests`** — generic HTTP, e.g. hitting the SEC EDGAR API.
- **`pyarrow`** — reads and writes **Parquet**, a columnar format that is far faster and smaller than CSV for the panel datasets you will be storing.

### Creating and verifying the environment

From the folder containing `environment.yml`, run:

```shell
conda env create -f environment.yml
```

The first time, this takes a few minutes while conda resolves and downloads everything. When it finishes, activate the environment:

```shell
conda activate finlab
```

Your prompt should now be prefixed with `(finlab)`. That prefix is your at-a-glance proof that you are working in the right sandbox — get in the habit of glancing at it before you run anything. Now verify the stack actually imports and reports sane versions:

```shell
python -c "import pandas, numpy, statsmodels, linearmodels, pyfixest; print('pandas', pandas.__version__)"
```

If that prints `pandas 2.2.x` (or higher) with no traceback, your environment is good. If an import fails, the fix is almost always to recreate the environment cleanly rather than patch it:

```shell
conda env remove -n finlab
conda env create -f environment.yml
```

Recreating from the file is cheap and deterministic — that is the entire point of declaring the environment in a file instead of installing by hand. When you later add a package, edit `environment.yml` and run `conda env update -f environment.yml --prune`; the `--prune` removes anything you deleted from the file so the environment stays a faithful mirror of it.

## B.1.4 Installing VS Code and pointing it at the environment

Download **Visual Studio Code** from its official site and install it normally. On first launch, open the Extensions panel (the four-squares icon in the left rail) and install two extensions published by Microsoft: **Python** and **Jupyter**. These give VS Code the ability to select conda environments, run scripts, and open notebooks with inline output.

Now connect VS Code to your `finlab` environment. The key concept: VS Code does not have *one* Python; you tell it, per project, which interpreter to use. Open your project folder (File ▸ Open Folder), then open the Command Palette with `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`), type **"Python: Select Interpreter,"** and choose the one whose path contains `envs/finlab`. From now on, the integrated terminal (Terminal ▸ New Terminal) opens with `(finlab)` already active, and the Run button uses that interpreter.

A useful sanity check: open VS Code's terminal and run `which python` (macOS/Linux) or `where python` (Windows). The path it prints should live inside your `finlab` environment folder. If it points somewhere else — a system Python, or `base` — re-select the interpreter. Mismatched interpreters are the cause of about half of all "but it imports in my terminal!" confusion, and checking `which python` resolves it in one line.

## B.1.5 Running notebooks

The camp ships a Jupyter notebook with every chapter (§5), so you need to be fluent in two ways of running them.

**In VS Code:** open any `.ipynb` file and it renders as a notebook with runnable cells. In the upper-right corner there is a **kernel picker** — click it and choose the `finlab` environment. A *kernel* is just the specific Python process that executes your cells; picking `finlab` guarantees your notebook sees the pinned packages. Run a cell with `Shift+Enter`. The `ipykernel` package you installed is what makes `finlab` show up as a choice here.

**In a browser via JupyterLab:** from an activated `finlab` terminal, run

```shell
jupyter lab
```

This launches a local server and opens JupyterLab in your browser. It is running entirely on your own machine — nothing leaves your laptop. Use whichever interface you prefer; the notebooks behave identically. When you are done, return to the terminal and press `Ctrl+C` to shut the server down.

Two discipline points that will save you grief later. First, **notebooks remember state you cannot see.** A variable defined in a cell you have since deleted still lives in memory, so a notebook can appear to work while being un-rerunnable from scratch. Before you submit anything, run **Kernel ▸ Restart and Run All** and confirm it executes top to bottom with no errors — that is the notebook equivalent of "runs on a fresh env." Second, **clear large outputs before committing.** A notebook with a megabyte of printed DataFrame baked into it bloats your Git history; either clear outputs or keep them small.

## B.1.6 Git basics for someone who has never used it

Git is a time machine for your project. It records *snapshots* (called **commits**) of your files, so you can see what changed, undo mistakes, work on an experiment without breaking your main version, and — through GitHub — collaborate and submit work. You do not need to understand its internals to use it well; you need about six commands. We will run them on the command line because that is the same everywhere, but VS Code's Source Control panel does all of this with buttons once you know what the buttons mean.

First, a one-time identity setup so your commits are attributed to you:

```shell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the same email you will register with GitHub. Now the core loop, illustrated on the camp project folder.

**Initialize a repository.** Inside your project folder, run:

```shell
git init
```

This creates a hidden `.git` directory that holds the entire history. Your folder is now a *repository* ("repo"). You do this once per project.

**Tell Git what to ignore — before your first commit.** Create a file named `.gitignore` listing things that must never be tracked. Per §5, this is where you protect secrets and licensed data. A minimal camp `.gitignore`:

```
# Never commit secrets or credentials
.env
*.pgpass
.pgpass

# Never commit licensed data (CRSP/Compustat stay on GMU infrastructure)
data/raw/
*.dta
*.sas7bdat

# Python and environment noise
__pycache__/
.ipynb_checkpoints/
*.pyc
```

This single file is your first line of defense against the two worst mistakes a finance student can make: committing a password, or committing licensed CRSP/Compustat data that is not yours to redistribute. B.2 returns to `.gitignore` discipline, and B.3 explains why the licensed data never leaves GMU infrastructure in the first place.

**Stage and commit.** Git separates *choosing* what goes into a snapshot (staging, with `git add`) from *taking* the snapshot (committing). Check the current state any time with:

```shell
git status
```

It lists files Git is ignoring, files that changed, and files staged for the next commit — read it often; it is the most useful command in Git. To stage everything that is not ignored and take a snapshot:

```shell
git add .
git commit -m "Set up environment.yml and project structure"
```

The `-m` message is a one-line note to your future self. Write it in the imperative ("Add Week 3 regression," not "added stuff") and make it specific; a folder full of commits named "update" is a time machine with no labels on the dials.

**Connect to GitHub and push.** Create an empty repository on GitHub through its website, then link your local repo to it and upload your commits. GitHub will show you the exact URL; the pattern is:

```shell
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

`origin` is the conventional nickname for "the copy on GitHub," and `main` is the default branch. The `-u` on the first push sets the default so that afterward you can push with a bare `git push`. When you pull collaborators' or instructors' changes down, the mirror command is `git pull`.

**Branching.** A *branch* is a parallel line of work. The point is to try something — a new specification, a risky refactor — without disturbing your working `main`. Create and switch to one in a single command:

```shell
git switch -c experiment-clustered-se
```

Make commits on it as usual. If the experiment works, you merge it back into `main`; if it does not, you switch back to `main` and the experiment is harmlessly parked. To go back:

```shell
git switch main
```

In the camp you will use branches most visibly in **Week 8 peer review**, where each student opens a *pull request* from a branch so teammates can comment before the work is merged. The full pull-request workflow lives in B.2.

That is the whole toolchain. You now have an isolated, pinned environment that anyone can recreate from one file; an editor wired to it; two ways to run notebooks; and version control that makes losing work nearly impossible. Appendix B.2 takes this Git foundation onto GitHub Classroom for assignment hand-in and peer review; B.3 connects the environment to the WRDS Cloud for real CRSP/Compustat data; and the sibling sections **B.4 (Running Jobs on Hopper with SLURM)** and **B.5 (Overleaf and LaTeX)** cover the heavy-compute and writing-up halves of the same workflow.
