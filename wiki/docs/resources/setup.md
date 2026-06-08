---
title: "Environment setup"
description: >-
  Conda env, Python 3.11 with pinned scientific stack, VS Code, Quarto,
  MkDocs, and GitHub auth — the day-one onboarding checklist.
---

# Environment setup

This is the **orientation-day checklist**. Work through it Thursday June 18 (orientation) or, at the latest, the morning of Monday June 22 before our 1:00 pm kickoff. If anything fails, post in `#help` *before* the kickoff — we will not have time to debug installs live.

The whole stack runs natively on macOS and Linux, and inside WSL on Windows. We strongly recommend WSL on Windows over native PowerShell.

---

## Checklist (top to bottom)

- [ ] Install conda (Miniforge preferred)
- [ ] Create the `assip2026` conda env from `environment.yml`
- [ ] Install VS Code + the Python and Jupyter extensions
- [ ] Install Quarto (for the textbook site)
- [ ] Install MkDocs Material (for this wiki, if you'll preview locally)
- [ ] Configure git + GitHub auth (PAT)
- [ ] Clone your fork of the cohort repo
- [ ] Create `.env` (see [Data access](data-access.md))
- [ ] Run the smoke-test notebook and post a screenshot of the green checks in `#help`

---

## 1. Conda (Miniforge)

Miniforge is the conda flavor we use because it defaults to the `conda-forge` channel (faster, more permissive licensing than the Anaconda Inc. channels).

=== "macOS"

    ```bash
    brew install miniforge
    conda init "$(basename "$SHELL")"
    exec "$SHELL"
    ```

=== "Linux / WSL"

    ```bash
    curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    bash Miniforge3-Linux-x86_64.sh   # accept defaults; let it modify your shell rc
    exec "$SHELL"
    ```

=== "Windows (use WSL!)"

    1. Install WSL 2 with Ubuntu 22.04 from the Microsoft Store.
    2. Open Ubuntu; follow the Linux instructions above.

Verify:

```bash
conda --version
# conda 24.x or newer
```

---

## 2. The `assip2026` conda env

The cohort repo ships an `environment.yml` at its root. From inside your cloned fork:

```bash
conda env create -f environment.yml -n assip2026
conda activate assip2026
```

The pinned stack:

- `python=3.11`
- `pandas>=2.2`, `numpy`, `scipy`
- `statsmodels`, `linearmodels`, `pyfixest`
- `matplotlib`, `seaborn`
- `wrds`, `yfinance`, `pandas-datareader`, `fredapi`, `requests`
- `pyarrow`, `python-dotenv`
- `jupyter`, `jupyterlab`, `ipykernel`
- `pytest`, `black`, `ruff`

To verify, open a Python REPL and run:

```python
import pandas, numpy, statsmodels, linearmodels, pyfixest, wrds, matplotlib
print("ok")
```

!!! tip "Re-create, don't repair"
    If your env gets into a weird state (mismatched versions, a half-failed install), the right move is almost always `conda env remove -n assip2026 && conda env create -f environment.yml -n assip2026`. Cheap, reliable.

---

## 3. VS Code

VS Code is what we recommend, but PyCharm and JupyterLab are fine if you prefer.

1. Download from [code.visualstudio.com](https://code.visualstudio.com).
2. Install the extensions:
    - **Python** (Microsoft)
    - **Jupyter** (Microsoft)
    - **Pylance** (Microsoft) — type-checking
    - **GitLens** (GitKraken) — git history in the gutter
    - **Black Formatter** + **Ruff** — formatting + linting on save
3. Open the cohort repo folder (`File → Open Folder`).
4. **Select the interpreter:** `Ctrl/Cmd + Shift + P → Python: Select Interpreter → assip2026`.
5. Open `notebooks/week-01/nb1.1.ipynb` and click "Run All". It should run end-to-end on a fresh env with no errors.

---

## 4. Quarto (for the textbook)

The textbook is a Quarto site. You will read it via the deployed URL on `github.io`, but to render it locally:

=== "macOS"

    ```bash
    brew install --cask quarto
    quarto --version
    ```

=== "Linux / WSL"

    ```bash
    curl -L -O https://quarto.org/download/latest/quarto-linux-amd64.deb
    sudo dpkg -i quarto-linux-amd64.deb
    quarto --version
    ```

=== "Windows native"

    Download the `.msi` installer from [quarto.org/docs/get-started/](https://quarto.org/docs/get-started/) and run it.

To render the textbook locally:

```bash
cd /path/to/ASSIP8weeks    # the textbook lives here, not in the wiki/ folder
quarto preview
```

This opens `http://localhost:4444/` with hot-reload.

---

## 5. MkDocs Material (this wiki, optional)

Only needed if you want to preview the wiki locally. The deployed wiki on `github.io` is updated by CI on every push to `main`.

```bash
cd wiki/
pip install -r requirements.txt
mkdocs serve
```

Opens `http://127.0.0.1:8000/`.

---

## 6. Git + GitHub auth

See the more detailed walkthrough in [Data access → The GitHub repo](data-access.md#6-the-github-repo). The short version:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git config --global pull.rebase false
git config --global init.defaultBranch main
```

When git prompts for your password the first time you push, paste your GitHub **personal access token** (not your account password). Save the token in a password manager.

On macOS the OS keychain caches it automatically. On Linux/WSL:

```bash
git config --global credential.helper "cache --timeout=86400"   # 24 h
```

---

## 7. `.env` file

See [Data access → Secrets discipline](data-access.md#0-secrets-discipline-read-this-first). Create `.env` at the repo root, fill in your WRDS username and FRED API key, and confirm `.gitignore` excludes it (it does, in the cohort repo, but double-check).

---

## 8. Smoke test

When everything is installed:

```bash
conda activate assip2026
cd /path/to/ASSIP8weeks
pytest -q notebooks/week-01/
```

You should see a row of dots and `5 passed`. Screenshot it and post in `#help` with the message "ready for kickoff" — that is how Prof. Gao knows you are set on Monday morning.

---

## Troubleshooting one-liners

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: pandas` | `conda activate assip2026` (you are in base, not the env) |
| `wrds.exceptions.LoginError` | `.pgpass` is missing or has wrong permissions: `chmod 600 ~/.pgpass` |
| `FRED_API_KEY not set` | `.env` not loaded; add `load_dotenv()` at the top of the notebook |
| `Permission denied (publickey)` on git push | Use HTTPS + PAT, not SSH — easier for the first summer |
| Notebook kernel says "Python 3.11" but `import wrds` fails | You're on the system Python; select the `assip2026` kernel from the top-right |
| `quarto: command not found` | Add `/usr/local/bin/quarto` (or wherever the installer put it) to your `$PATH` |

If none of these match, post the **full error traceback** in `#help` — never paraphrase a traceback. The exact text matters.
