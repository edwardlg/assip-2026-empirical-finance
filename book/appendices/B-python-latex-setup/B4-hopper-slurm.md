# B.4 — GMU Hopper SLURM

You have spent the camp running code on a laptop, or in a browser tab, or on the camp container — machines that have one user (you), turn on when you ask, and run one thing at a time. This appendix is about the moment that stops being enough. Two things in this program break the laptop model. The first is that the licensed data you query in **B.3** (CRSP, Compustat, TRACE) is not allowed to leave GMU's infrastructure — the license says so, CONVENTIONS §5 says so, and your WRDS agreement says so — which means the *computation* on that data has to happen on a GMU machine, not on your MacBook in a coffee shop. The second is the Week-6 AI module: running a local large language model over a corpus of filings (Chapter 6.5's Ollama and on-cluster fallback for licensed text) needs a **GPU**, and a serious one — far more than a laptop has. Both of those needs are met by the same thing: GMU's research computing cluster, named **Hopper**, run by the Office of Research Computing (ORC). This section explains what a cluster is, why the camp uses one, how to get onto Hopper, and how to actually run work there with SLURM — with complete, copy-and-adapt job scripts for a CPU analysis job, an A100 GPU job for the AI module, and a local-LLM-via-Ollama job that keeps licensed text inside the cluster walls.

A note before we start, in the spirit of the rest of this book: the *shape* of everything here is real and standard, but the cluster-specific strings — the exact partition names, the account/allocation string ORC assigns your group, the module names — are the kind of thing that changes between cluster generations and between research groups. Everywhere one of those appears below it is tagged `[CHECK]`, meaning *confirm this against GMU ORC's current Hopper documentation or your allocation email before you run it.* A SLURM script with the wrong partition name does not run; it sits in the queue forever or rejects immediately, and the fix is always one of these strings.

---

## B.4.1 What a cluster is, and why we use one

A **high-performance computing (HPC) cluster** is, at the simplest level, a few hundred to a few thousand computers (called **nodes**) wired together with a fast network and a shared file system, so that many users can run many jobs on them at once without stepping on each other. You do not get a node by walking up to it; you *request* one (or a slice of one, or a hundred of them) from a piece of software called a **scheduler**, which holds a queue of everyone's requests and parcels out the hardware fairly. Hopper is GMU's cluster, and its scheduler is **SLURM** (Simple Linux Utility for Resource Management) — the same scheduler that runs most academic clusters in the world, which is why the skills here transfer to almost any university HPC system you meet later.

Why does the camp route you onto Hopper at all, when a laptop ran everything for seven weeks? Three reasons, in order of how binding they are.

The first and least negotiable is **data governance**. The licensed datasets — CRSP, Compustat, IBES, TRACE — are leased to GMU under agreements that forbid copying the raw data off GMU-controlled systems. You met this rule in B.3 and in every data card in Appendix C: *licensed data stays on GMU infrastructure, read-only.* Hopper *is* that infrastructure. When your analysis needs to touch the licensed bytes — merge a CRSP return series onto your sample, pull a Compustat fundamentals panel — the cleanest and most defensible place to do it is on the cluster, where the data already lives behind GMU's authentication, rather than downloading an extract to your own disk (which may violate the license and definitely complicates your replication packet's "no licensed data shipped" promise from Lab 8).

The second is **GPUs for the AI module**. Week 6 asks you, in part, to run an open large language model locally so that licensed or governance-sensitive text never goes to a commercial API (Chapter 6.5 §"Local fallback for licensed data"). An 8-billion-parameter model is sluggish on a laptop CPU and a larger model is simply impossible there; both want a GPU with tens of gigabytes of memory. Hopper has nodes with **NVIDIA A100** GPUs — 40 or 80 GB of high-bandwidth memory each — which is enough to serve a capable open model at a usable speed. You request one of those nodes from SLURM for the hour or two you need it, and release it when you are done, rather than buying a $10,000 card you would use twice.

The third is plain **scale and unattended running**. Some camp work — embedding a few thousand 10-K chunks for the RAG pipeline, bootstrapping standard errors a few thousand times, classifying a corpus of 8-Ks — takes longer than you want to babysit a laptop for, and longer than a flaky home wifi connection will stay up. A cluster job runs on the cluster's hardware whether or not your laptop is open; you submit it, close your machine, and collect the output later. That is the whole point of a *batch* scheduler, and it is the next idea.

---

## B.4.2 Getting onto Hopper: SSH

You reach Hopper over **SSH** (Secure Shell), the same encrypted-terminal tool you used to talk to GitHub in B.2. You will need three things from ORC first, and getting them is a paperwork step, not a coding step: a Hopper **account** (tied to your GMU NetID), membership in the camp's **allocation/account** (the billing/priority bucket your jobs charge against — `[CHECK]` the exact string ORC emails you, it looks something like `nextgen2026`), and, if you are off the GMU campus network, the GMU **VPN** running so the cluster's login address is reachable.

With those in hand, you connect to a **login node**:

```bash
# Replace NETID with your GMU NetID. The login hostname is [CHECK] against
# ORC's current docs -- it is commonly of the form hopper.orc.gmu.edu.
ssh NETID@hopper.orc.gmu.edu
```

You will be prompted for your GMU password and, almost certainly, a two-factor (2FA) push — Hopper sits behind GMU's authentication exactly because it holds licensed data. The first time you connect, SSH will ask you to confirm the server's fingerprint; say yes once and it is remembered.

A quality-of-life step worth doing on day one: set up an **SSH key** so you are not retyping your password on every connect, and a `~/.ssh/config` entry so you can type a short alias. On your *laptop* (not on Hopper), generate a key if you do not already have one from B.2, then copy its public half to Hopper:

```bash
# On your laptop. Skip ssh-keygen if you already made a key in B.2.
ssh-keygen -t ed25519 -C "you@gmu.edu"      # press Enter to accept defaults; set a passphrase
ssh-copy-id NETID@hopper.orc.gmu.edu        # installs your PUBLIC key on Hopper
```

Then add an alias to `~/.ssh/config` on your laptop so `ssh hopper` is enough:

```
Host hopper
    HostName hopper.orc.gmu.edu     # [CHECK] exact login hostname with ORC
    User NETID
```

> **The login node is not a compute node.** This is the single most important rule of cluster etiquette, and violating it is the fastest way to get a polite-then-stern email from ORC. The login node is a *shared front desk*: dozens of people are connected to it at once, using it to edit files, submit jobs, and check status. It is **not** where you run your analysis. If you launch a heavy Python job directly on the login node, you slow that machine down for everyone, and ORC may kill your process. Everything that does real work — every regression, every model call, every embedding pass — goes through the scheduler onto a *compute* node. The login node is for typing `sbatch`, `squeue`, and `nano`, and nothing more.

Once you are on the login node, your files live on a **shared file system** visible from every node — so a file you create on the login node is there when your job runs on a compute node. Your home directory (`$HOME`, typically with a modest quota) is for code and small files; ORC provides separate, larger **scratch** space (`[CHECK]` the path and policy — often something like `/scratch/$USER`, large but periodically purged) for big intermediate data. Put your repository in `$HOME`, your bulky intermediates in scratch, and never assume scratch files survive forever.

---

## B.4.3 The SLURM model: login vs. compute nodes, and the three commands

SLURM's mental model is a job queue. You write a small shell script that says *what resources I need* (how many CPUs, how much memory, how long, whether a GPU) and *what to run*, then hand that script to SLURM. SLURM finds a slot on the cluster that fits your request, runs your script there, and writes whatever the script prints into a log file you collect afterward. You manage the whole lifecycle with three commands.

**`sbatch` — submit a batch job.** You write a job script (we build several below), then submit it:

```bash
sbatch my_job.slurm        # SLURM prints: "Submitted batch job 1234567"
```

That number, `1234567`, is the **job ID** — your handle for everything afterward. The job does not run *now*; it joins the queue and runs when resources free up, which might be seconds or hours depending on what you asked for and how busy the cluster is. Modest requests (a few CPUs, an hour) start fast; greedy requests (a whole GPU node, 48 hours) wait longer.

**`squeue` — see the queue.** To watch your own jobs:

```bash
squeue -u $USER            # your jobs: ID, partition, name, state, time, nodes
```

The **state** column is what you read. `PD` (pending) means it is waiting for resources; `R` (running) means it is on a node right now; and the absence of your job from the list means it has finished (or failed) — check the log. The `NODELIST(REASON)` column tells you *why* a pending job is waiting: `(Resources)` means the hardware is busy, `(Priority)` means others are ahead of you, and `(QOSMaxJobsPerUserLimit)` or similar means you have hit a per-user cap.

**`scancel` — kill a job.** If you submitted something wrong — a typo in the script, a runaway loop — cancel it by ID:

```bash
scancel 1234567            # cancel one job
scancel -u $USER           # cancel ALL of your jobs (use with care)
```

Canceling early is good citizenship: a 48-hour GPU job you know is broken is 48 GPU-hours nobody else can use. Two more commands are worth knowing once you are comfortable: `sinfo` lists the partitions and how busy each is, and `sacct -j 1234567` shows the accounting record (how long a finished job ran, how much memory it actually used, whether it exited cleanly) — invaluable for right-sizing your next request.

A **partition** (SLURM's word for a named pool of nodes) is the other string you must get right. Clusters group nodes into partitions by type — a partition of plain CPU nodes, a partition of GPU nodes, sometimes a short-but-fast "debug" partition for testing. You select one with `--partition`. The exact names on Hopper are `[CHECK]` — ORC's docs are authoritative — but the *pattern* is universal, and the job scripts below show where the name goes.

---

## B.4.4 A CPU batch job template

Here is a complete, realistic CPU job for the kind of work that fills most of the camp: run a Python analysis script that reads data, estimates a model, and writes tables and figures — exactly the `03_analysis.py` step from Lab 8, but on the cluster because it touches licensed data. Save it as `analysis.slurm` in your repository. Every line is annotated; the `#SBATCH` lines at the top are SLURM **directives** — comments to the shell, but instructions to the scheduler.

```bash
#!/bin/bash
#SBATCH --job-name=denial-gap        # shows up in squeue; name it for the task
#SBATCH --partition=normal           # [CHECK] the CPU partition name with ORC
#SBATCH --account=nextgen2026        # [CHECK] your allocation/account string
#SBATCH --nodes=1                    # one node is enough for a single Python process
#SBATCH --ntasks=1                   # one task...
#SBATCH --cpus-per-task=4            # ...with 4 CPU cores (match your code's parallelism)
#SBATCH --mem=16G                    # 16 GB RAM; right-size with sacct after a test run
#SBATCH --time=02:00:00              # walltime HH:MM:SS; the job is KILLED past this
#SBATCH --output=logs/%x-%j.out      # stdout -> logs/<jobname>-<jobid>.out
#SBATCH --error=logs/%x-%j.err       # stderr -> logs/<jobname>-<jobid>.err

# --- environment: make the logs/ dir, load software, activate the conda env ---
mkdir -p logs

# Clusters expose software through "modules"; load Anaconda/Miniconda first.
module purge                         # start from a clean module environment
module load miniconda                # [CHECK] the exact module name (e.g. miniconda3/...)

# Activate the camp's pinned conda env (CONVENTIONS sec.5: python=3.11 + the stack).
source activate capstone             # or: conda activate capstone  [CHECK] env name

# Fail loudly: stop at the first error, treat unset vars as errors, fail piped cmds.
set -euo pipefail

# --- the actual work: run the analysis script ---
echo "Job $SLURM_JOB_ID starting on $(hostname) at $(date)"
python src/03_analysis.py
echo "Job $SLURM_JOB_ID finished at $(date)"
```

Submit it with `sbatch analysis.slurm`, watch it with `squeue -u $USER`, and when it disappears from the queue read `logs/denial-gap-1234567.out` to see what it printed. A few of these directives carry the whole weight of "does this run well," so they deserve a sentence each.

`--time` is the **walltime limit**, and SLURM enforces it absolutely: when the clock hits your limit, your job is killed mid-stride whether or not it finished. Ask for a bit more than you think you need (a job that dies at 1:59:00 of a 2:00:00 limit wasted the whole run), but not wildly more — a tighter, honest estimate starts sooner, because the scheduler can slot a short job into gaps a long one would not fit. `--mem` is the memory ceiling, enforced the same way: blow past it and the job is killed with an out-of-memory error. After a first test run, `sacct -j <jobid> --format=JobID,Elapsed,MaxRSS,State` tells you what the job *actually* used, so your next request is right-sized. `--cpus-per-task` should match how parallel your code really is — asking for 16 cores for single-threaded pandas just makes you wait longer in the queue for cores you never use. And the `%x-%j` in the log paths expands to *jobname-jobid*, so concurrent jobs do not overwrite each other's logs.

The `module load` / `source activate` pair is how you get *your* Python on the compute node. The compute node boots with almost nothing; **modules** are the cluster's mechanism for adding software (a conda installation, a CUDA toolkit, a compiler) to your `PATH` on demand. You load Anaconda's module, then activate the same pinned `capstone` environment you built per CONVENTIONS §5, so the code runs against the exact `pandas>=2.2`/`statsmodels`/`pyfixest` stack it was written for. `module purge` first guarantees you are not inheriting some half-loaded environment from a previous session.

---

## B.4.5 An A100 GPU job for the Week-6 AI module

The AI module needs a GPU. Requesting one is a small delta on the CPU template: you point at the **GPU partition**, add a `--gres=gpu:...` line that asks for the specific card, and load the CUDA toolkit so the GPU libraries are visible. Here is a complete GPU job that runs a Python script using an A100 — for example, embedding a corpus of filings for the RAG pipeline of Chapter 6.5, or running a transformer model that needs the card. Save it as `gpu_embed.slurm`.

```bash
#!/bin/bash
#SBATCH --job-name=rag-embed         # the task: embed the 10-K corpus
#SBATCH --partition=gpuq             # [CHECK] the GPU partition name with ORC
#SBATCH --account=nextgen2026        # [CHECK] your allocation/account string
#SBATCH --qos=gpu                    # [CHECK] some clusters require a GPU QOS string
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8            # GPU jobs still want CPU cores for data loading
#SBATCH --mem=48G
#SBATCH --gres=gpu:a100:1            # <-- request ONE A100. [CHECK] the exact gres name;
                                     #     it may be gpu:A100:1 or gpu:1 depending on config
#SBATCH --time=03:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

mkdir -p logs
module purge
module load miniconda                # [CHECK] module name
module load cuda                     # [CHECK] the CUDA module/version your stack needs

source activate capstone             # the env must have a GPU-enabled torch [CHECK]
set -euo pipefail

echo "Job $SLURM_JOB_ID on $(hostname) at $(date)"
nvidia-smi                           # PROVE a GPU is visible; prints the A100 and its memory
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"   # which physical card SLURM gave you

python src/embed_corpus.py           # your embedding / model script
echo "Job $SLURM_JOB_ID finished at $(date)"
```

The load-bearing new line is `#SBATCH --gres=gpu:a100:1`: `gres` is "generic resource," and `gpu:a100:1` reads as "give me one GPU of type a100." Drop the type qualifier (`--gres=gpu:1`) and you get *any* available GPU, which is fine if you do not care which; keep it when you specifically need the A100's memory. SLURM sets the environment variable `CUDA_VISIBLE_DEVICES` to the card it assigned you, and your GPU libraries (PyTorch, etc.) read that automatically — you do not pick the physical card yourself, and you must not try to use a card SLURM did not give you.

Two habits make GPU jobs go smoothly. First, **run `nvidia-smi` at the top of the job** as a one-line sanity check: it prints the GPU model and its memory, proving the card is actually attached before your script tries to use it. A job that requested a GPU but, due to a wrong `gres` string, did not get one will fail deep inside PyTorch with a confusing "CUDA not available" error; `nvidia-smi` near the top turns that into an obvious early failure. Second, **a GPU is a scarce, expensive resource — hold it for the minimum time.** Do your data downloading, cleaning, and any CPU-only preprocessing in a *separate CPU job* (B.4.4), write the cleaned data to disk, and let the GPU job do only the part that genuinely needs the card. A GPU node idling while your script parses CSVs is a GPU node nobody else can use, and ORC's accounting (and your group's allocation) notices.

For *interactive* GPU work — debugging a model, exploring in a notebook — you do not write a batch script; you ask SLURM for an interactive session on a GPU node with `salloc` (or `srun --pty`), which drops you into a shell *on the compute node* with the GPU attached:

```bash
# Grab one A100 interactively for 1 hour, then you're on the compute node.
salloc --partition=gpuq --account=nextgen2026 --gres=gpu:a100:1 \
       --cpus-per-task=8 --mem=48G --time=01:00:00            # [CHECK] partition/account/gres
# ... when the prompt returns, you are ON the node: run python, nvidia-smi, etc.
# Type `exit` to release the node the moment you're done.
```

This is the right tool for the trial-and-error phase; once the code works, move it into a batch script so the long run is unattended and logged.

---

## B.4.6 Running a local LLM via Ollama on a compute node

This is the piece that ties the cluster back to the camp's central rule. Chapter 6.5 makes the case plainly: licensed and governance-sensitive text — a corpus of filings you pulled under a WRDS/TRACE license, or any data CONVENTIONS §5 says cannot leave GMU — **must not be sent to a commercial LLM API** over the public internet, because the data is not yours to transmit. The defense is to run the model *locally*, inside the secured environment, so the text never crosses the boundary. On a laptop you do that with **Ollama** serving a small model. On Hopper you do the same thing, but on an A100 node, so the model is large enough to be useful *and* the licensed text never leaves the cluster it already lives on.

The mechanics: Ollama runs as a small local server that listens on a port (default `11434`) and answers HTTP requests with model completions. On a compute node you start that server in the background, point it at GPU-backed model storage, then run your Python client against `http://localhost:11434` — the same code you saw in Chapter 6.5, unchanged, because "localhost" now means *this compute node*, and the request never leaves it. Save this as `ollama_classify.slurm`.

```bash
#!/bin/bash
#SBATCH --job-name=ollama-classify   # classify licensed filings with a LOCAL model
#SBATCH --partition=gpuq             # [CHECK] GPU partition
#SBATCH --account=nextgen2026        # [CHECK] allocation
#SBATCH --qos=gpu                    # [CHECK] if required
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:a100:1            # [CHECK] gres name; a larger model wants the 80GB A100
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

mkdir -p logs
module purge
module load cuda                     # [CHECK] CUDA module for GPU-backed inference
module load ollama                   # [CHECK] if ORC provides an Ollama module; else use a
                                     #         locally installed/containerized ollama binary
source activate capstone
set -euo pipefail

# Keep model weights in scratch, not in your tiny $HOME quota. [CHECK] scratch path.
export OLLAMA_MODELS="/scratch/$USER/ollama_models"
mkdir -p "$OLLAMA_MODELS"

# 1) Start the Ollama server IN THE BACKGROUND, bound to localhost only.
#    Binding to localhost (the default) is the governance point: nothing off-node
#    can reach it, so licensed text handed to the model never leaves this node.
ollama serve &
OLLAMA_PID=$!
# Make sure the server is shut down when the job ends, however it ends.
trap "kill $OLLAMA_PID 2>/dev/null" EXIT

# 2) Wait until the server answers before sending work (poll its endpoint).
echo "Waiting for Ollama to come up..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:11434/api/tags >/dev/null; then
        echo "Ollama is up."; break
    fi
    sleep 2
done

# 3) Pull the model once (cached in $OLLAMA_MODELS for next time).
ollama pull llama3.1:8b              # a bigger model (e.g. 70b) needs the 80GB A100 [CHECK]

# 4) Run the classifier. The Python client talks to http://localhost:11434 ONLY.
#    The licensed filing text goes from cluster disk -> local model -> labels on disk.
#    It never touches the public internet. (Same client code as Chapter 6.5.)
python src/classify_local.py

echo "Job $SLURM_JOB_ID finished at $(date)"
# the EXIT trap stops the Ollama server here
```

The Python side is exactly the snippet from Chapter 6.5 — read the key-free local endpoint, send the rubric and the filing, get a label — and it is worth restating that it carries **no API key and no secret of any kind**, because there is no remote service to authenticate to. CONVENTIONS §5's "secrets via env vars only, never hard-coded" rule is satisfied trivially here: there is nothing to hide, which is itself the point of running locally.

```python
# src/classify_local.py -- the model runs on THIS compute node; data never leaves it.
import requests, json

SYSTEM_PROMPT = "..."   # the frozen classification rubric from Chapter 6.5 sec.6.5.2

def classify(filing_text: str) -> str:
    resp = requests.post(
        "http://localhost:11434/api/chat",      # localhost == this node; no internet
        json={
            "model": "llama3.1:8b",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": filing_text},
            ],
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()
# Loop over your licensed corpus, write labels to disk, and -- per Chapter 6.5 --
# validate them against a hand-labeled gold set before any label enters a regression.
```

Four details make this job correct rather than merely plausible, and they generalize to running any *server* process inside a batch job. First, `ollama serve &` launches the server in the **background** (the `&`) so the script can continue to the client step; without it, the script would hang on the server forever. Second, the `trap "kill $OLLAMA_PID" EXIT` line guarantees the server is **shut down when the job ends**, however it ends — a server left running after your script finishes would hold the GPU until the walltime limit, wasting hours of an A100. Third, the **poll loop** waits for the server to actually answer before sending work, because `ollama serve` takes a few seconds to come up and a request fired too early just errors. Fourth, `OLLAMA_MODELS` is pointed at **scratch**, not `$HOME` — model weights are gigabytes and will blow a home-directory quota instantly; `[CHECK]` your scratch path and remember scratch may be purged, so a re-`pull` on a later job is normal.

The governance argument, restated once because it is the reason this whole section exists: the model and the data are *both* on the same compute node, the server listens only on `localhost`, and the only thing that ever leaves the node is the *labels* you write to disk — never the licensed filing text. That is what lets you use a capable LLM on CRSP-adjacent or TRACE-licensed text without violating the data-use agreement, and it is the on-cluster version of the laptop-Ollama fallback Chapter 6.5 introduced. The cost, as that chapter warned, is capability: an open 8B model is weaker than a frontier API model, so its classifier needs the *same* out-of-sample precision/recall/F1 validation against a hand-labeled gold set before you trust a single label — and you may find you need the 70B model (and thus the 80 GB A100) to clear your F1 bar. The cluster gives you that option; validation tells you whether you need it.

---

## B.4.7 Where this connects

This appendix is the infrastructure floor under three other parts of the book. The pinned conda environment your jobs `source activate` is the one from **B.1** (the toolchain and `python=3.11` stack); the repository you `sbatch` from is the one you stood up in **B.2** (GitHub workflow) and finished as a one-click packet in Lab 8; the licensed data your CPU jobs read is accessed under the read-only, stays-on-GMU rules of **B.3** (WRDS Cloud). And the GPU and Ollama jobs are the operational backing for Chapter 6.5's local-model fallback. When you write your capstone's replication packet (Appendix D, Lab 8), the SLURM scripts themselves belong *in the repo*, alongside the `Makefile` — a reviewer with a Hopper account should be able to `sbatch analysis.slurm` and watch your licensed-data step reproduce, exactly as a reviewer without one runs `make all` on the public-data path. The scripts are part of the recipe.

Two closing habits. **Always test small first**: run on a 100-row sample with a 10-minute walltime before you submit the 40,000-document, 4-hour job, so a typo costs you ten minutes and not four hours of queue-plus-run. And **read `sacct` after every real job** to right-size the next one — clusters reward honest resource requests with faster starts, and ORC notices users who routinely ask for an 80 GB GPU and 48 hours to run a 20-minute CPU script. Every `[CHECK]` in this section — the login hostname, partition names, the account string, module names, the `gres` qualifier, scratch paths, whether Ollama is provided as a module — is a value to confirm against GMU ORC's current Hopper documentation or your allocation email before your first submission. Get those strings right once, save the working scripts, and the cluster becomes as routine as the laptop it replaced.
