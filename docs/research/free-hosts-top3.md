# Top 3 FREE Web Hosts for ASSIP 2026

**Prepared:** June 2026
**For:** Prof. Lei Gao, GMU (ASSIP 2026 — 8-week empirical-finance camp)
**Artifacts to host:**
1. A Quarto-rendered textbook (~265 pages, heavy math, 40 pre-rendered Jupyter notebooks, no server-side execution).
2. A smaller wiki-style course portal (static, much smaller).

Both artifacts are **fully static HTML/CSS/JS** after a local Quarto render — no databases, no server functions. That fact narrows the question to "best static host" and makes Vercel/Netlify dynamic-functions features irrelevant.

---

## TL;DR — Recommendation

| Rank | Host | One-line | Deploy method |
|---|---|---|---|
| 1 (BEST) | **GitHub Pages + Actions** | Already running the camp book; 1 GB site / 100 GB monthly bandwidth; Actions free and unlimited on public repos. | GitHub Actions builds Quarto, pushes to `gh-pages`. |
| 2 | **Cloudflare Pages** | Unlimited bandwidth and unlimited requests on the free tier; 500 builds/month; fast global edge. | Git connect + auto-deploy, or `wrangler pages deploy`. |
| 3 | **Netlify (legacy account)** *or* **Render** | Mature drag-and-drop / git deploy with PR previews; Netlify-legacy keeps 100 GB + 300 build min; Render gives 100 GB + 500 build min. | Git connect or CLI. |

**BEST PICK: GitHub Pages with a GitHub Actions Quarto-render workflow** — same workflow as the existing book repo, zero migration friction, unlimited Actions minutes for public repos, fits comfortably within all soft limits.

---

## How I scored each host

For ASSIP, the dimensions that actually matter are:

1. **Static-only fit.** No server-side execution needed; dynamic-function quotas don't help us.
2. **Total site size.** A Quarto book of 265 pages plus 40 pre-rendered notebooks lands in the 100–400 MB range with figures and HTML widgets. Well under 1 GB.
3. **Bandwidth.** ASSIP draws maybe a few hundred unique readers; even at 50 MB/visit and 5,000 sessions/month, that's ~250 GB. We want headroom but don't need TB-scale.
4. **Build minutes.** A Quarto book render on a public CI runner takes 4–10 minutes; we'll redeploy daily-ish.
5. **License / use clauses.** GMU faculty research-and-teaching project = at minimum *educational*; could be construed as "professional work." Need a host whose TOS allows this without arm-twisting.
6. **Operational maturity.** Continued maintenance after summer 2026, ideally by a student worker.

---

## 1. GitHub Pages + GitHub Actions (BEST PICK)

**2026 free-tier specifics (verified on docs.github.com, June 2026):**

- **Site size:** max 1 GB per published Pages site (soft).
- **Repo size:** recommended ≤ 1 GB.
- **Bandwidth:** soft limit 100 GB / month.
- **Builds:** soft limit 10 Pages-native builds per hour — **does not apply** when you build with a custom Actions workflow (which is what Quarto users do).
- **GitHub Actions on public repos:** *free and unmetered* with standard GitHub-hosted runners in 2026 (private repos get 2,000 min/month on Free). This is huge — every Quarto re-render is "free."
- **HTTPS:** automatic with Let's Encrypt; custom domain free.
- **License clause:** no commercial/non-commercial distinction. Academic and faculty use is unambiguously fine.

**Deploy method.** The existing `8weeks` book already has `.github/workflows/quarto-render.yml`. The flow is: push to `main` → Actions checks out repo → installs Quarto + Python kernel → `quarto render` → publishes the `_site/` to the `gh-pages` branch via `actions-gh-pages` or the `peaceiris/actions-gh-pages@v4` action. The wiki portal can live in a sister repo or the same repo with a different output dir.

**Why it wins for ASSIP:**

- **Already in production for the camp book.** Migration cost = zero. Same workflow file, two output directories, two GitHub Pages targets.
- The 1 GB site cap is roughly 3–4× what a Quarto book of this size produces.
- 100 GB/month bandwidth is 5–10× our expected demand even in a busy week.
- Public repo → free, unlimited Actions minutes. The Quarto render can be as slow as it needs to be.
- No "commercial use" landmine.
- A student worker can ship a fix with a pull request — no platform-specific dashboard to learn.

**Risks / mitigations:**

- *Soft bandwidth limit.* If ASSIP ever goes viral, GitHub may email and ask to reduce; in practice this is a friendly nudge well above 100 GB. Mitigation: front the site with a free Cloudflare CDN if needed (Cloudflare caches everything; origin bandwidth from GitHub drops to near-zero).
- *Repo size with binary notebook outputs.* Use `nbstripout` or commit only the rendered HTML, not the raw cell outputs.

---

## 2. Cloudflare Pages

**2026 free-tier specifics (verified on developers.cloudflare.com, June 2026):**

- **Bandwidth:** *unlimited*. (Cloudflare's distinguishing feature.)
- **Requests:** unlimited static requests.
- **Sites:** unlimited.
- **Builds:** 500 builds/month; 1 concurrent build; build minutes not separately metered (each build has a generous timeout, ~20 min).
- **File-size limits:** max 25 MiB per file, max 20,000 files per site on the free tier (paid plans go to 100,000 in 2026).
- **Custom domains:** 100 per project.
- **HTTPS:** automatic; works out of the box.
- **License clause:** no academic/commercial distinction; permissive.

**Deploy method.** Two options:
1. *Git connect.* Authorize the GitHub repo in the Cloudflare dashboard; Cloudflare runs the build (`quarto render`) and serves `_site/`.
2. *External CI + `wrangler pages deploy _site`.* Have GitHub Actions do the Quarto render (we already have this), then a final step uploads the static output to Cloudflare Pages. This is the cleanest pattern when you want to use a specific Quarto version and avoid Cloudflare's default Node-only build image.

**Why it places second:**

- **Unlimited bandwidth** removes the only ASSIP-scale risk on GitHub Pages.
- Fast global edge — the closest CDN POP to ASSIP students is sub-20 ms.
- 500 builds/month is more than enough; even a CI build per commit on a busy week is ~100/month.
- 20,000 files cap is the only real watchout: a Quarto book with many small fragments and a bunch of figure files could approach this. As of June 2026 the textbook is ~3,400 output files, comfortably under.

**Why not #1:** It is a *parallel* deployment surface to GitHub Pages; we'd be adding a host, not replacing one. Pick this if and only if GitHub Pages bandwidth becomes a constraint, or you want a public-internet edge-cached copy for visibility.

---

## 3. Netlify (legacy account) — or Render (if signing up fresh)

Netlify's free tier got materially worse for new accounts in September 2025. Two cases to distinguish:

### 3a. Netlify — *legacy* accounts (created before 2025-09-04)

- **Bandwidth:** 100 GB/month included.
- **Build minutes:** 300/month.
- **Sites, members:** generous; effectively unmetered for our use.
- **HTTPS, custom domains, PR previews:** all included.
- **License:** no commercial restriction.
- **Deploy:** git connect, drag-and-drop, or `netlify deploy --prod --dir _site`.

If Prof. Gao already has a Netlify account from before September 2025, this is a strong third option. The PR preview / deploy-preview feature is genuinely useful for reviewing chapter edits before merging.

### 3b. Netlify — *new* accounts (post 2025-09-04)

The free tier switched to a **credit-based model**: 300 credits/month, hard cap, no overage, no auto-recharge. Costs: 15 credits per production deploy, 20 credits per GB of bandwidth, 10 credits per GB-hour of compute, 2 credits per 10k web requests. Practical translation: ~15 GB bandwidth + 15 deploys/month before you're out. **Too tight for ASSIP.** Source: Netlify pricing changelog, 2026-04-14.

### 3c. Render (recommended free #3 for new signups)

- **Bandwidth:** 100 GB/month outbound.
- **Build minutes:** 500/month for static sites (more than Netlify legacy).
- **Custom domains, managed TLS:** included on free.
- **No credit card required.**
- **Deploy:** git connect; auto-deploy on push.
- **License:** no commercial restriction.

Render is the cleanest free alternative for someone who doesn't already have a Netlify account.

---

## Hosts considered but NOT in the top 3

### Vercel Hobby — **DO NOT USE** for ASSIP

The Hobby plan is generous (100 GB Fast Data Transfer, 100 GB-Hrs Function Execution, 6,000 build-execution-minutes), **but the Fair Use Guidelines explicitly restrict Hobby to "non-commercial personal use only."** Vercel's own definition of commercial usage includes any deployment "used for the purpose of financial gain of anyone involved in any part of the production of the project, **including a paid employee or consultant writing the code**" (Vercel Fair Use, last updated 2026-02-27).

A GMU faculty member running ASSIP as part of their job *is* a paid employee producing the project. Even though ASSIP is a non-profit educational program with no ads and no payments from visitors, the wording catches us. Vercel rarely enforces against academic users, but the policy risk is real and a Pro upgrade is $20/user/month. **Use Vercel only on a personal-time portfolio, not on the institutional ASSIP site.**

### GitLab Pages

- 400 CI minutes/month on the free tier for private projects; **unlimited for public projects** as of 2026.
- Pages itself is fine; HTTPS automatic; custom domains free.
- We'd be migrating off GitHub for no clear benefit. Skip unless the user specifically prefers GitLab.

### Read the Docs (Community)

- Free for open-source documentation; ads-supported; no project-size limits published.
- **Big caveat: native build pipeline supports Sphinx and MkDocs, not Quarto.** You can host pre-rendered HTML by treating RTD as a generic static host, but you lose the auto-build/versioning value-add — which is the only reason to pick RTD over a generic host. Quarto has its own ecosystem and Posit Connect Cloud handles this niche better.

### Surge.sh

- Free forever, unlimited bandwidth, unlimited apps, custom domains via CNAME.
- **Custom SSL is paywalled** ($30/mo Surge Plus). Wildcard `*.surge.sh` HTTPS is free.
- CLI-only deploy (`surge ./_site assip2026.surge.sh`). Fine as a quick mirror; not great as a primary host because no PR previews and a tiny operator community.

### Cloudways / Hostinger education tiers

- Cloudways has no free tier for academic users in 2026; it's a managed WordPress / DigitalOcean wrapper that doesn't suit a Quarto static book regardless.
- Hostinger does **not** offer a free tier for students or faculty; only discounts (CNHOSTSTUDENT for ~10%, ~25% via Student Beans). Not relevant.
- **InterServer** offers a one-year free hosting for select US-university students — not faculty, and a one-year tail is a maintenance trap. Skip.

### Other notable rejects

- **Surge Cloud / Posit Connect Cloud**: free static publishing tier for Quarto exists, but newer and less battle-tested than the top 3.
- **Firebase Hosting / AWS Amplify / Azure Static Web Apps**: real free tiers exist but require cloud-billing setup and are overkill for a static book; not recommended for a single-faculty project.

---

## Concrete plan if we pick GitHub Pages (recommended)

1. **Repo structure.** Keep the textbook in `8weeks` (current). Create a second repo `assip-portal` for the wiki/course site, or use the existing `8weeks` repo's `docs/portal/` subdir and a second Pages workflow.
2. **Workflow.** Reuse the existing `quarto-render.yml`. Pin Quarto version (`QUARTO_VERSION: 1.9.x`) so renders are reproducible.
3. **Domain.** Either `gao-lei.github.io/8weeks` (default) or a custom `assip.gmu.edu` subdomain if IT will grant it (GMU IT typically will for faculty research sites; submit a CNAME ticket).
4. **Bandwidth insurance.** If demand spikes, put Cloudflare in front of `*.github.io` for free — origin bandwidth drops to ~5% of total.
5. **Mirror (optional).** Set up Cloudflare Pages as an automatic mirror by adding one final `wrangler pages deploy` step to the GitHub Actions workflow. Total cost: zero. Gives a fallback URL if GitHub Pages ever has an outage.

---

## Sources (verified June 2026)

- GitHub Pages limits: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>
- GitHub Actions billing: <https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions>
- Cloudflare Pages limits: <https://developers.cloudflare.com/pages/platform/limits/>
- Cloudflare Pages 2026 file-limit changelog: <https://developers.cloudflare.com/changelog/post/2026-01-23-pages-file-limit-increase/>
- Netlify pricing: <https://www.netlify.com/pricing/>
- Netlify credit-based plans: <https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/>
- Netlify 2026-04 pricing update: <https://www.netlify.com/changelog/2026-04-14-pricing-updates-april-2026/>
- Vercel Hobby plan: <https://vercel.com/docs/plans/hobby>
- Vercel Fair Use (commercial-use clause): <https://vercel.com/docs/limits/fair-use-guidelines>
- Render free tier: <https://render.com/docs/free>
- GitLab compute minutes: <https://docs.gitlab.com/ci/pipelines/compute_minutes/>
- Read the Docs pricing: <https://about.readthedocs.com/pricing/>
- Surge.sh pricing: <https://surge.sh/pricing>
- Hostinger student discount terms: <https://www.studentbeans.com/student-discount/us/hostinger>
