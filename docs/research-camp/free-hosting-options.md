# Free Static-Site Hosting for the 8-Week Camp Textbook

**Audience:** Prof. Lei Gao (GMU) — empirical-finance textbook for high-school students
**Repository profile:** ~407 Markdown files, ~40 Jupyter notebooks, math-heavy (KaTeX/MathJax),
will be built into a single static HTML site (likely Jupyter Book, Quarto, or MkDocs Material)
**Goal:** Identify the best **free** host that auto-deploys from GitHub, supports a custom
domain with HTTPS, handles a ~1,000-page math-heavy build, and has no degraded free tier
that would push the project off the platform within a year.

This memo verifies every free-tier limit against the host's **own 2026 documentation**.
Where pricing pages were ambiguous, secondary 2026 reviews are cited as cross-checks.

---

## 1. Per-host summaries (2026 free-tier numbers)

### GitHub Pages
GitHub Pages is GitHub's first-party static host. Free tier: **1 GB published site
cap, 100 GB/month soft bandwidth, soft cap of 10 builds/hour (does not apply when
publishing via a custom GitHub Actions workflow), 10-minute deploy timeout**
([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
Sites get free HTTPS with auto-provisioned Let's Encrypt certificates and free
custom-domain support; the platform is global via Fastly's CDN. Crucially, when you
build with GitHub Actions and publish the artifact, **GitHub's own
documentation lists no separate build-minute meter for Pages itself** — Actions usage
counts against the repo's Actions budget (2,000 free minutes/month for private repos,
**unlimited for public repos**). Educational/non-commercial use is explicitly fine;
GitHub Pages **prohibits primarily commercial e-commerce sites** but a free public
textbook is firmly within the allowed-use band
([Pages limits page](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
This is the host that Jupyter Book, MkDocs, Quarto, and QuantEcon all document as the
default deployment target.

### Netlify
Netlify's free plan changed substantively in late 2025. **Legacy accounts** (pre-Sep 4, 2025)
keep the older shape: 100 GB bandwidth, 300 build minutes, 1 concurrent build per month.
**New accounts** are now on a **credit-based** model — 300 credits/month, with deploys
charging 15 credits each, bandwidth at 20 credits/GB, and web requests at 2 credits per
10k ([Netlify pricing](https://www.netlify.com/pricing/);
[AgentDeals 2026 review](https://agentdeals.dev/vendor/netlify);
[Flexprice 2026 guide](https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans)).
For a ~1,000-page textbook that you redeploy daily during the draft phase, the new credit
ceiling is tight — bandwidth alone for one popular semester can exhaust the budget. Netlify
remains the best-in-class **Deploy Preview** platform (PR-level previews, branch deploys,
form handling, redirects/headers via `_redirects` and `_headers`), and it still
auto-builds Jupyter Book ([official guide](https://jupyterbook.org/en/stable/publish/netlify.html)).
Free SSL, free custom domains, unlimited deploy previews.

### Vercel
Vercel's **Hobby** plan is free and now lists usage as: **100 GB Fast Data Transfer, 1M
edge requests, 1M function invocations, 100 GB-Hrs function execution, ~100 Hrs build
execution/month, 200 projects, 50 domains/project, 100 deploys/day, 6,000 build minutes**
([Vercel Hobby plan](https://vercel.com/docs/plans/hobby);
[fair-use guidelines](https://vercel.com/docs/limits/fair-use-guidelines)).
The hard blocker for this project: **Hobby is restricted to non-commercial personal use,
and Vercel's own fair-use page defines "commercial" broadly enough to flag ad-supported
sites, paid-employee-built sites, and "asking for donations"** as commercial. A textbook
authored as part of paid faculty work at GMU sits in a grey zone — Vercel has been known
to flag accounts under this clause. For a personal blog this is fine; for an institutional
textbook with a GMU affiliation, treat Vercel Hobby as **legally risky** unless you
formally email Vercel support for confirmation.

### Cloudflare Pages
Cloudflare's free Pages tier is the most generous on bandwidth: **unlimited bandwidth and
unlimited requests to static assets at every tier including free**, **500 builds/month,
1 concurrent build, 20-minute build timeout, 20,000 files per site, 25 MiB per file,
100 custom domains, and ~100 projects** ([Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/);
[Pages functions pricing](https://developers.cloudflare.com/pages/functions/pricing/);
[Cloudflare developer plans](https://www.cloudflare.com/plans/developer-platform/)).
Static asset requests are explicitly free and unlimited — only Pages **Functions** hit the
Workers Free quota (100k requests/day combined). A pure static textbook will never touch
that quota. Free HTTPS, free custom domains, header/redirect rules via `_headers`/`_redirects`,
optional password protection via Cloudflare Access (free tier covers 50 users).
**Commercial use is allowed.** The 20,000-file limit is the only number to watch: a
naïvely built Jupyter Book with per-cell artifacts can approach it, but a typical book of
this size lands at ~3,000–8,000 files.

### Read the Docs (Community)
Free, ad-supported hosting purpose-built for documentation. The Community plan is
"free forever for open source" and includes versioned docs, full-text search, PR
previews, CDN delivery, and custom domains with HTTPS
([Read the Docs pricing](https://about.readthedocs.com/pricing/)).
Build limits on Community: **15 minutes build time, 7 GB RAM, 5 GB disk (soft),
2 concurrent builds per project** ([RTD build resources](https://docs.readthedocs.com/platform/stable/builds.html)).
Originally Sphinx-only, the platform now also supports **MkDocs and Jupyter Book** via
its `build.commands` config. The two downsides: (a) ads are displayed on Community-hosted
sites (some can be themed but not fully removed without paying), and (b) the 15-minute
build cap is **tight** for a 1,000-page math-heavy Jupyter Book that executes notebooks
during the build — you'd want to pre-execute notebooks locally.

### GitLab Pages
GitLab Pages is bundled with GitLab. Free tier: **10 GiB project storage**, **400 CI/CD
compute minutes/month**, free custom domains, free Let's Encrypt HTTPS, redirects supported
via `_redirects`, headers via `.gitlab-ci.yml` artifact config
([GitLab Pages docs](https://docs.gitlab.com/user/project/pages/);
[GitLab free user limits](https://docs.gitlab.com/user/free_user_limit/);
[Storage docs](https://docs.gitlab.com/user/storage_usage_quotas/)).
**400 minutes is the binding constraint** — for a textbook that rebuilds on every push,
this can be consumed in a week or two. GitLab Pages also assumes the project lives on
GitLab; for a repo currently on GitHub, you'd need either a mirror or to migrate.
**Recommended only if the repo is already on GitLab.**

### Surge.sh
CLI-only deploys (`surge ./_build/html my-book.surge.sh`). **Free for unlimited sites,
unlimited custom domains via CNAME, free SSL on `*.surge.sh` subdomains only — custom SSL
on your own domain requires the paid Surge Plus plan** ([Surge custom domains](https://surge.sh/help/adding-a-custom-domain);
[Surge SSL](https://surge.sh/help/securing-your-custom-domain-with-ssl)). No GitHub
auto-deploy out of the box (you'd configure a GitHub Action that runs `surge`), no PR
previews, no CDN comparable to the big three, no headers/redirects beyond a basic
`200.html` SPA fallback. **Not competitive in 2026** unless you specifically want CLI-only
no-frills hosting.

### Render
Static sites on Render are free with **100 GB bandwidth/month and 500 build pipeline
minutes/month**, free SSL, custom domains, PR previews, headers and redirects via
`_headers`/`_redirects` files ([Render free docs](https://render.com/docs/free);
[Render 2026 free-tier review](https://agentdeals.dev/vendor/render)). The catch: if you
exceed bandwidth and have not added a payment method, **all your free services are
suspended for the rest of the month** — there is no grace mode like Netlify's. Build
minutes work the same way. Render is fine, but offers no advantage over Cloudflare Pages
(which gives unlimited bandwidth) or GitHub Pages (which has no separate build meter for
public-repo Actions).

---

## 2. Feature comparison (2026)

| Feature | GitHub Pages | Cloudflare Pages | Netlify (new) | Vercel Hobby | Read the Docs Community | GitLab Pages | Render Static | Surge.sh |
|---|---|---|---|---|---|---|---|---|
| Site size cap | 1 GB | 20k files, 25 MiB/file | n/a (credit) | 100 MB upload | 5 GB disk | 10 GiB | n/a stated | n/a |
| Bandwidth/mo | 100 GB (soft) | **Unlimited** | ~15 GB (300 cr) | 100 GB | CDN, no cap stated | Not specified | 100 GB | n/a |
| Build minutes/mo | Unlimited via public-repo Actions | 500 builds | ~20 deploys (300 cr) | 6,000 min | 15 min/build, unlimited builds | 400 min | 500 min | n/a (local) |
| Concurrent builds | Actions concurrency | 1 | 1 | 1 | 2 | 1 | 1 | n/a |
| Build timeout | 10 min (Pages) / 6 hr (Actions) | 20 min | 15 min | n/a | 15 min | 1 hr | 15 min | n/a |
| Custom domain | Yes, free | Yes, 100/project | Yes | Yes, 50/project | Yes | Yes | Yes | CNAME free |
| Free HTTPS | Yes (Let's Encrypt) | Yes | Yes | Yes | Yes | Yes (Let's Encrypt) | Yes | Subdomain only |
| Auto-deploy from GitHub | Native + Actions | Native | Native | Native | Native (webhook) | Mirror only | Native | Manual / Action |
| PR / deploy previews | Via Actions | Yes | Yes (flagship) | Yes | Yes | Manual | Yes | No |
| Global CDN | Fastly | Cloudflare (300+ POPs) | Yes | Yes | Yes | Yes | Yes | Limited |
| Headers / redirects | Limited (Jekyll plugins, no `_headers`) | `_headers`, `_redirects` | `_headers`, `_redirects` | `vercel.json` | RTD config | `_redirects` | `_headers`, `_redirects` | `200.html` only |
| Password protection (free) | No | Cloudflare Access (50 users free) | Paid only | Paid only | Paid only | Yes (built-in) | Paid only | No |
| Commercial / institutional use | Allowed (non-e-commerce) | **Allowed** | Allowed | **NOT allowed (Hobby)** | OSS only | Allowed | Allowed | Allowed |
| Educational use friction | None | None | None | **Grey-zone** | OSS-only requirement | None | None | None |

Sources: official limits pages cited inline in §1; cross-verified against 2026 third-party
reviews on [DeployWise](https://deploywise.dev/blog/vercel-free-tier-limits-2026),
[Flexprice](https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans), and
[DevToolReviews](https://www.devtoolreviews.com/reviews/cloudflare-pages-pricing-bandwidth-limits-2026).

---

## 3. Build/deploy ergonomics by textbook platform

### Jupyter Book
Jupyter Book's own documentation ships canonical workflows for **GitHub Pages with
Actions** and **Netlify**
([gh-pages guide](https://jupyterbook.org/en/stable/publish/gh-pages.html);
[Netlify guide](https://jupyterbook.org/en/stable/publish/netlify.html)).
The GitHub Pages path is the most battle-tested — Jupyter Book's official cookiecutter
ships a working `deploy.yml` that builds and pushes to `gh-pages` automatically
([cookiecutter-jupyter-book](https://github.com/executablebooks/cookiecutter-jupyter-book)).
For Cloudflare Pages, you point the build at `pip install -r requirements.txt &&
jupyter-book build .` with publish dir `_build/html` — works identically to Netlify. The
sharpest constraint: **executing all 40 notebooks during the build can easily exceed 15
minutes** if any notebook hits an API or runs a slow simulation. **Recommended pattern:
pre-execute notebooks locally** (or in a separate cached Actions job) and commit the
`.ipynb` outputs, then have the host only run the much faster Sphinx → HTML pass.

### Quarto
Quarto explicitly recommends **GitHub Pages with Actions** when notebooks execute code
([Quarto CI](https://quarto.org/docs/publishing/ci.html)). Quarto's `freeze: auto`
mechanism caches executed outputs in `_freeze/` so the host only re-renders changed pages
— this is the deployment-ergonomic gold standard for a math-heavy book. **Netlify
servers cannot execute code** for Quarto; you must use the freeze pattern or GitHub
Actions ([Quarto on Netlify](https://quarto.org/docs/publishing/netlify.html)).
[Utrecht University's open textbook on Quarto + GitHub Pages](https://utrechtuniversity.github.io/open-textbooks/)
is a worked example of exactly this stack. For Cloudflare Pages, the same
"render-in-Actions-then-deploy" pattern works cleanly with the
[wrangler-action](https://github.com/cloudflare/wrangler-action).
[An April 2026 blog post documents migrating a Quarto blog from Netlify to GitHub Pages](https://www.r-bloggers.com/2026/04/publishing-a-quarto-blog-what-i-learned-moving-from-netlify-to-github-pages/)
specifically citing free-tier degradations on Netlify.

### MkDocs Material
MkDocs is the simplest of the three (pure Markdown → HTML, no notebook execution unless
you add `mkdocs-jupyter`). Material for MkDocs ships [an official GitHub Pages
deploy workflow](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
that completes in under 2 minutes even for sites of several hundred pages.
The `mkdocs gh-deploy` one-liner is the legacy fallback. Math support
(arithmatex extension + MathJax) handles KaTeX/LaTeX cleanly. **For a ~1,000-page book
without executable notebooks, MkDocs Material on GitHub Pages is the lowest-friction
combination by a wide margin** — but the camp's `.ipynb` files are the deciding factor:
Jupyter Book or Quarto handle them natively, MkDocs needs a plugin.

---

## 4. Educational-content considerations

- **Math-heavy rendering:** All three textbook platforms support KaTeX or MathJax,
  and every CDN-backed host (GitHub Pages, Cloudflare, Netlify, Vercel, Render) serves
  the JS bundles without issue.
- **Notebook output size:** Notebooks with embedded plots and DataFrames can balloon the
  built site. With 40 notebooks averaging ~500 KB built HTML each, total site weight
  ≈ 20-50 MB — well under every host's caps.
- **Student traffic:** A camp with ~50 students hitting the site over 8 weeks generates
  trivial bandwidth (< 5 GB/month). If the book later goes viral via GMU or social
  channels, Cloudflare Pages' **unlimited bandwidth** is the only host that won't ever
  bill or throttle you.
- **Privacy for early drafts:** If you need to gate access for early reviewers, **only
  Cloudflare Pages and GitLab Pages offer free password/auth gating**. On GitHub Pages,
  the free tier exposes the site publicly; making the **repo** private requires
  GitHub Pro for private Pages sites. Cloudflare Access (free, up to 50 users) is the
  easiest free draft-gate.
- **Institutional/commercial-use risk:** **Vercel Hobby's fair-use clause flags any site
  produced by paid employees as commercial usage**
  ([Vercel fair use](https://vercel.com/docs/limits/fair-use-guidelines#commercial-usage)).
  A GMU faculty-built textbook is at non-trivial risk of being asked to upgrade.
  GitHub Pages, Cloudflare Pages, Netlify, and Render have no such clause.
- **What comparable books actually use:**
  - QuantEcon's full Python lecture series builds with Jupyter Book and deploys to
    **GitHub Pages** with a custom domain (`python.quantecon.org`)
    ([QuantEcon lecture-python repo](https://github.com/QuantEcon/lecture-python)).
  - "Causal Inference for the Brave and True" deploys to **GitHub Pages**
    ([matheusfacure.github.io/python-causality-handbook](https://matheusfacure.github.io/python-causality-handbook/)).
  - "Python Data Science Handbook" by Jake VanderPlas is hosted as a Jupyter Book on
    **GitHub Pages**.
  - Utrecht University's open-textbooks reference itself uses **Quarto + GitHub Pages**
    ([utrechtuniversity.github.io/open-textbooks](https://utrechtuniversity.github.io/open-textbooks/)).

The pattern is uniform: the comparable open-source educational books in this exact
niche are on **GitHub Pages**, built via GitHub Actions.

---

## 5. Recommendation

**Use GitHub Pages with a custom GitHub Actions workflow.**

Reasons:

1. **No build-minute meter for public-repo Actions.** Public repos get unlimited
   Actions minutes, which dissolves the binding constraint that hurts Netlify (~20
   deploys/month under the new credit model), Render (500 min), Cloudflare Pages
   (500 builds), and GitLab Pages (400 min).
2. **No free-tier degradation risk.** GitHub Pages limits — 1 GB site, 100 GB
   bandwidth, 10-min Pages-internal deploy timeout — have been unchanged for years
   and are documented on a canonical page that GitHub treats as a stable contract.
   Netlify cut its free tier twice in 18 months; Vercel Hobby restricts commercial
   use; Render and Cloudflare Pages both have caps that **could** be hit by a viral
   moment.
3. **First-class fit with the candidate textbook stacks.** Jupyter Book, Quarto, and
   MkDocs Material all ship canonical "deploy to GitHub Pages via Actions" workflows
   as their primary documented path
   ([Jupyter Book gh-pages](https://jupyterbook.org/en/stable/publish/gh-pages.html);
   [Quarto CI](https://quarto.org/docs/publishing/ci.html);
   [Material publishing](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)).
4. **What comparable books use.** QuantEcon, the Python Data Science Handbook, Causal
   Inference for the Brave and True, and Utrecht's open-textbook reference all live
   on GitHub Pages.
5. **No commercial-use friction.** GitHub Pages explicitly allows non-e-commerce
   personal, educational, and institutional sites
   ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
6. **Free HTTPS + custom domain + Fastly CDN.** Sufficient for a 50-student camp and a
   1,000-page book with viral upside up to the 100 GB/month soft limit.

**Workflow shape:** A single `.github/workflows/deploy.yml` that runs on push to
`main`, pre-executes notebooks (or uses Quarto's `freeze`), builds the static HTML,
uploads as a Pages artifact, and calls `actions/deploy-pages@v4`. Cache the
`pip`/`renv`/`_freeze` directories to keep builds under 5 minutes.

## 6. Runner-up: Cloudflare Pages

If you ever expect significant viral traffic (an op-ed picks up the book, the camp
expands to thousands of students), **Cloudflare Pages** is the right runner-up
because of its **unlimited bandwidth** at the free tier and its 300+ PoP CDN.
The 500-builds/month cap is more than ample for a textbook deployed daily, and
its `_headers`/`_redirects` files plus free Cloudflare Access (password
protection up to 50 users) outclass GitHub Pages on advanced features. The single
file limit to monitor is **20,000 files per site** — a Jupyter Book with
per-cell static assets needs a sanity check, but a typical ~1,000-page build with
40 notebooks should produce well under that ([Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/)).

Practical compromise: deploy the live site to GitHub Pages from day one; keep a
parallel `cloudflare-pages` workflow in the repo so that if GitHub ever degrades
the free tier you can flip DNS in one commit.

---

## Sources

- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [Netlify pricing](https://www.netlify.com/pricing/)
- [Netlify free tier 2026 review (AgentDeals)](https://agentdeals.dev/vendor/netlify)
- [Netlify pricing guide 2026 (Flexprice)](https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans)
- [Vercel Hobby plan](https://vercel.com/docs/plans/hobby)
- [Vercel fair-use guidelines](https://vercel.com/docs/limits/fair-use-guidelines)
- [Vercel free-tier 2026 review (DeployWise)](https://deploywise.dev/blog/vercel-free-tier-limits-2026)
- [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/)
- [Cloudflare Pages Functions pricing](https://developers.cloudflare.com/pages/functions/pricing/)
- [Cloudflare developer platform plans](https://www.cloudflare.com/plans/developer-platform/)
- [Cloudflare Pages 2026 pricing review](https://www.devtoolreviews.com/reviews/cloudflare-pages-pricing-bandwidth-limits-2026)
- [Read the Docs pricing](https://about.readthedocs.com/pricing/)
- [Read the Docs build resources](https://docs.readthedocs.com/platform/stable/builds.html)
- [GitLab Pages docs](https://docs.gitlab.com/user/project/pages/)
- [GitLab free user limits](https://docs.gitlab.com/user/free_user_limit/)
- [GitLab storage quotas](https://docs.gitlab.com/user/storage_usage_quotas/)
- [Surge custom domains](https://surge.sh/help/adding-a-custom-domain)
- [Surge HTTPS / SSL](https://surge.sh/help/securing-your-custom-domain-with-ssl)
- [Render free tier docs](https://render.com/docs/free)
- [Render 2026 review](https://agentdeals.dev/vendor/render)
- [Jupyter Book — GitHub Pages and Actions](https://jupyterbook.org/en/stable/publish/gh-pages.html)
- [Jupyter Book — Netlify](https://jupyterbook.org/en/stable/publish/netlify.html)
- [cookiecutter-jupyter-book](https://github.com/executablebooks/cookiecutter-jupyter-book)
- [Quarto CI publishing](https://quarto.org/docs/publishing/ci.html)
- [Quarto on Netlify](https://quarto.org/docs/publishing/netlify.html)
- [Utrecht open-textbooks (Quarto + GitHub Pages)](https://utrechtuniversity.github.io/open-textbooks/)
- [Material for MkDocs publishing](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [Quarto blog: Netlify → GitHub Pages (Apr 2026)](https://www.r-bloggers.com/2026/04/publishing-a-quarto-blog-what-i-learned-moving-from-netlify-to-github-pages/)
- [QuantEcon lecture-python source](https://github.com/QuantEcon/lecture-python)
- [Causal Inference for the Brave and True](https://matheusfacure.github.io/python-causality-handbook/)
