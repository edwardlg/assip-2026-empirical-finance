# B.2 GitHub & GitHub Classroom

Appendix B.1 left you with Git running on your own machine and a GitHub account. This section connects the two into the workflow the camp actually uses to hand out, collect, and review work. The mental model is simple once you see it: **GitHub Classroom is just Git plus a few conveniences for a teacher.** Every assignment is a Git repository. You accept it, clone it, do your work in the commit/push loop you already learned, and the instructor sees your repository update in real time. Week 8 adds one new move — the pull request — for peer review. There is no magic; if you understand `git push`, you already understand most of this.

The reason the camp insists on this rather than emailing notebooks around is the same reason §5 insists on a pinned environment: **the history is the deliverable.** An instructor who can see your commit timeline can see how your analysis evolved, can rerun your exact code, and can leave comments tied to specific lines. A notebook attachment is a dead snapshot; a repository is a living, auditable record. That auditability is also what protects you — your commits are timestamped proof of your own work.

## B.2.1 Accepting a GitHub Classroom assignment

When an assignment opens, the instructor posts an **invitation link** (it looks like `https://classroom.github.com/a/XXXXXXXX`). Open it while signed in to GitHub.

The first time you ever accept a Classroom link, GitHub asks you to **authorize the GitHub Classroom application** and may show a **roster** so you can identify yourself — click your name to associate your GitHub account with the camp roster. Do this carefully; it is how your future submissions get attributed to you instead of to "unmatched student."

After you accept, Classroom does something specific behind the scenes: it creates a *brand-new repository that belongs to you*, seeded from a template the instructor prepared. The repo is named with a pattern like `week3-panel-regression-yourusername`. It already contains the starter files — a notebook skeleton, a `README.md` with the task, often the `environment.yml` from B.1, and a `.gitignore`. You did not have to set any of that up; that is the convenience Classroom adds on top of plain Git. Refresh the page after a few seconds and it shows you a link to *your* new repository.

A few things worth knowing so the model stays clear:

- The repository is **private to you and the instructor**. Other students cannot see it (until Week 8, when you deliberately share for peer review). This is correct and intentional — your in-progress work is yours.
- **Accepting is one-time per assignment.** If you click the same invitation link again later, GitHub recognizes you and just sends you to your existing repository. You will not get a second copy.
- If the roster step lists no name matching you, do not guess — message the instructor. A mismatched roster entry is the single most common reason a submission "disappears."

## B.2.2 Cloning your repository to your machine

Accepting gave you a repository *on GitHub's servers*. To work on it, you pull a copy down to your laptop or the GMU environment. That copy-down is called **cloning**. On your repository's GitHub page, click the green **Code** button and copy the HTTPS URL. Then, in a terminal, in the folder where you keep your camp work:

```shell
git clone https://github.com/your-org/week3-panel-regression-yourusername.git
cd week3-panel-regression-yourusername
```

`git clone` does three things at once: it downloads every file, it downloads the full history, and it automatically sets up the `origin` remote pointing back at GitHub — so you do *not* need the `git remote add` step from B.1. A cloned repo is push-ready immediately.

Now rebuild the environment so your code actually runs. Because the starter repo ships the `environment.yml`, this is the same one-liner from B.1:

```shell
conda env create -f environment.yml   # only if you haven't already built finlab
conda activate finlab
```

Then open the folder in VS Code (`File ▸ Open Folder`), select the `finlab` interpreter, and you are working. This "clone, then recreate the env from the file" sequence is exactly why we declared the environment in a file in the first place — it makes any machine, including a fresh GMU login, ready in two commands.

### A word on authentication

The first time you `git push` over HTTPS, GitHub will ask you to prove you are you. **GitHub no longer accepts your account password for Git operations.** You have two good options:

1. **A Personal Access Token (PAT).** Generate one under GitHub ▸ Settings ▸ Developer settings ▸ Personal access tokens. When Git prompts for a "password," paste the token instead. Treat the token like a password — it is a secret, so it goes in a credential manager, never into a file you commit (this is the §5 secrets rule again, and B.3 applies the same rule to database credentials).
2. **The GitHub CLI**, `gh`. Running `gh auth login` once walks you through a browser sign-in and configures Git to use it automatically thereafter. On the GMU environment this is often the smoothest path.

Either way, your editor or OS will usually remember the credential after the first time, so you authenticate once and forget about it.

## B.2.3 The commit / push loop

This is the rhythm of every working session, and it is the same loop from B.1 — you are just running it inside a Classroom repo now. The cycle has four beats:

```shell
git status                                  # 1. see what changed
git add ch31-panel.ipynb notes.md           # 2. stage the work you mean to save
git commit -m "Add fixed-effects spec and diagnostics"   # 3. snapshot it
git push                                     # 4. send it to GitHub
```

A few habits turn this from a chore into a safety net:

- **Commit often, in meaningful chunks.** A good commit is one coherent step: "Add Compustat merge," then "Add firm-and-year fixed effects," then "Write up results." Each is a point you can roll back to. Lumping a whole evening into one giant "did the assignment" commit throws away most of the value.
- **Stage deliberately.** `git add .` stages everything not ignored, which is fine when everything you changed belongs together. But when you have touched several unrelated things, naming files (`git add ch31-panel.ipynb`) keeps each commit focused.
- **Push at the end of every session, minimum.** A commit only lives on your machine until you push; an unpushed commit is one spilled coffee away from gone. Pushing also means the instructor — and, for group work, your teammates — can see and pull your latest.
- **Restart-and-Run-All before the commit that submits.** As B.1 warned, notebooks carry invisible state. Before the push you consider your hand-in, run **Kernel ▸ Restart and Run All** so you are committing a notebook that genuinely executes top to bottom on the pinned environment. Submitting a notebook that only ran because of a deleted cell is the notebook version of a result you cannot reproduce.

There is no separate "submit" button to hunt for. **Your latest push *is* your submission.** Classroom and the instructor always look at the current state of your `main` branch (and its history). If an assignment has a deadline, what matters is the timestamp of your last commit before it; pushes after the deadline are still visible to the instructor as late work.

## B.2.4 What the instructor sees

It helps to know the view from the other side, because it explains why the habits above matter.

The instructor opens GitHub Classroom and sees an **assignment dashboard**: one row per student, each linking to that student's repository, showing whether they have accepted, how many commits they have made, and when they last pushed. Clicking into your repository, the instructor can:

- **Read your commit history** — the sequence of messages and the diffs between them. This is why specific commit messages help you: they narrate your process. An instructor reviewing "Add clustered SEs after residual plot showed heteroskedasticity" understands your reasoning; "update3" tells them nothing.
- **Open and rerun your notebook** on a recreated `finlab` environment. Because you shipped a working `environment.yml` and a restart-and-run-all-clean notebook, your results regenerate. Because §5 forbids `pd.append` and chained indexing, they regenerate without deprecation surprises.
- **Leave inline comments** on specific lines or cells, and — in the peer-review flow below — request changes.

Optionally, the instructor may wire up **GitHub Actions autograding**, which runs a small test suite on every push and shows a green check or red X next to your submission. If your assignment has autograding, treat the checks as a free TA: push early, read what failed, fix, push again. The checks run on *their* definition of correct, on a fresh environment — yet another reason the pinned env matters.

## B.2.5 Pull requests for peer review (Week 8)

Through Weeks 1–7 you mostly work alone in your own repository. **Week 8 introduces peer review, and the vehicle is the pull request (PR).** A pull request is Git's structured way of saying "here is a set of changes on a branch; please look at them before they join the main version." It is the single most important collaboration primitive on GitHub, and the camp uses it the way professional research teams do: as a place to *discuss* changes, not just deliver them.

The flow, end to end:

**1. Branch.** Do not put proposed changes straight on `main`. Create a branch (the command from B.1):

```shell
git switch -c peer-review-maya-replication
```

The branch name should say what the work is. Make your commits on it and push the branch to GitHub:

```shell
git add ch85-replication.ipynb
git commit -m "Replicate Maya's HMDA DiD and add a robustness check"
git push -u origin peer-review-maya-replication
```

**2. Open the pull request.** On the repository's GitHub page, a banner offers to open a PR from the branch you just pushed; click it (or go to the Pull requests tab ▸ New pull request). You choose the **base** (usually `main`, the version you want to merge into) and the **compare** (your branch). Write a clear title and a description that tells the reviewer what to look at — "Does the parallel-trends check hold? See cell 12." A good PR description is a reading guide for your reviewer.

**3. Review.** Your assigned peer opens the PR's **Files changed** tab, which shows a clean diff of exactly what you altered. They click any line to leave a comment — a question, a suggested fix, a "nice catch here." They can submit a formal review as **Comment**, **Approve**, or **Request changes**. This is the heart of peer review: specific, line-anchored, in-context feedback, all preserved in the PR's conversation thread. When you receive review on your own work, the companion skill is to read it for substance rather than nod along — push back where you disagree, with a reason, exactly as you would defend a specification choice.

**4. Respond and iterate.** You address comments by making new commits on the *same branch* and pushing again; the PR updates automatically and the new commits appear in the thread. Conversations get resolved as you handle them. Nothing is lost — the whole back-and-forth is part of the permanent record.

**5. Merge.** Once the reviewer approves, click **Merge pull request**. Your branch's changes fold into `main`, and you can safely delete the now-merged branch. If your repository has autograding or required reviews, the **Merge** button stays disabled until those checks pass — GitHub enforcing the quality gate so a half-finished change cannot sneak into `main`.

Two reasons the camp teaches this beyond Week 8 mechanics. First, the PR is how almost all real software and quantitative-research collaboration happens; learning it here is directly transferable. Second, reviewing a peer's empirical work forces the discipline §4 demands — you cannot meaningfully review a regression unless its outcome, treatment, controls, fixed effects, clustering, sample, and identifying assumption are all stated. Reviewing teaches you to *ask for* those things, which makes you state them in your own work.

## B.2.6 The `.gitignore` discipline: never commit secrets or licensed data

This is the rule with the highest stakes in the entire appendix, so it gets its own section even though B.1 introduced the file. **Git is a near-perfect memory. Anything you commit and push is, for practical purposes, permanent** — even if you delete the file in a later commit, the secret still sits in the history, retrievable by anyone with repository access. There is no clean "undo" once it is pushed; the only real fix is rotating the leaked credential and rewriting history, which is painful and often incomplete. So the entire game is to *never let it in.* That is what `.gitignore` is for.

Two categories must never enter a commit, per §5:

**Secrets and credentials.** No passwords, no API keys, no tokens, no `.pgpass` files, no `.env` files containing your WRDS or Azure credentials. The §5 rule is absolute: **secrets live in environment variables, never in code or committed files.** Your `.gitignore` must therefore exclude every file where a secret could hide:

```
# --- Secrets: NEVER commit ---
.env
.env.*
*.pgpass
.pgpass
secrets.yml
*.key
```

Code that *needs* a secret reads it from the environment at runtime — for example `os.environ["WRDS_PASSWORD"]` — so the secret is present in memory when the program runs but never written into a tracked file. B.3 shows this pattern in full for the WRDS connection.

**Licensed data.** CRSP, Compustat, and IBES data are licensed to GMU; redistributing them — and pushing a `.dta` of CRSP returns to GitHub *is* redistribution — violates that license. Per §5, **licensed data stays on GMU infrastructure (read-only on the WRDS Cloud and Hopper)** and never gets committed. Your `.gitignore` enforces it:

```
# --- Licensed data: NEVER commit (stays on GMU infrastructure) ---
data/raw/
data/licensed/
*.dta
*.sas7bdat
*.parquet
```

The healthy pattern is to keep raw licensed pulls in an ignored `data/raw/` folder, commit only your *code* that regenerates results from that data, and — if you must share a small derived artifact — share an aggregate that contains no licensed row-level records. What goes in the repo is the recipe, not the protected ingredients.

A practical safety check: run `git status` before every commit and actually read it. If you see a `.env`, a `.pgpass`, a `.dta`, or anything in `data/raw/` listed as a change to be committed, **stop** — your `.gitignore` is missing an entry. Add the entry, confirm the file drops off the `git status` list, and only then commit. Two minutes of reading `git status` is cheaper than a leaked credential or a license violation.

With Classroom for hand-in and peer review covered, and the never-commit-secrets rule locked in, the next section connects all of this to the data itself. **B.3 (WRDS Cloud)** shows how to query CRSP/Compustat with credentials supplied safely through the environment, keeping the licensed data exactly where §5 says it belongs.
