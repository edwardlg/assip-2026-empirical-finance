# Wiki Platforms for the ASSIP 2026 Course Portal

**Purpose.** Pick a wiki-style web platform for an 8-week ASSIP cohort at GMU (14 students, Prof. Lei Gao, summer 2026). The wiki holds the course schedule, project tracker, student and mentor profiles, reading assignments, FAQ, data-access docs, and symposium information. The long-form textbook already targets Quarto, so this portal must be lighter, faster to edit, and feel like a dashboard, not a book.

**Audience for editing.** Prof. Gao (primary), 1-2 mentors, occasionally a TA, and possibly students contributing FAQ entries. Maintenance must stay low — the professor's time is the binding constraint.

**Date of research.** June 2026. All version numbers below were verified against current vendor docs and changelogs.

---

## Decision criteria, weighted

| Criterion                                    | Why it matters for ASSIP                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| Wiki-native page / sidebar UX                | A course portal needs landing + categorized pages, not a long book TOC.   |
| Markdown vs GUI authoring                    | Mentors are mixed: some `git push`, some prefer a browser editor.         |
| Authentication / gating                      | Student rosters, mentor contact info, and symposium logistics are non-public. |
| Search                                       | 14 students will look up "what's due Friday" 50x; must be instant.        |
| Browser-edit vs file-based                   | Edit-from-phone-at-airport is a real workflow.                            |
| 2026 free-tier limits                        | No discretionary budget; APIM credits go to LLM compute, not SaaS seats.  |
| GitHub-deploy vs hosted-as-a-service         | Repo already on GitHub; CI/CD is solved.                                  |
| Technical-content rendering (math, code)     | Finance formulas, Python snippets, plotly outputs appear in reading guides. |
| Maintenance burden                           | The professor is solo on infra.                                           |

---

## Candidate platforms — 2026 state

### GitHub Wiki
GitHub Wiki is built into every repo, uses Markdown (Gollum), supports rendered math expressions, diagrams, and a customizable sidebar/footer. It is genuinely "wiki-native" — every page has an edit-in-browser button and a history tab.

The fatal constraint for ASSIP: **wikis on organization-owned private repositories are not available on the Free plan**; they require GitHub Team or higher (per the current GitHub Docs on wiki access permissions). A GMU organization repo would either need to go public or buy seats. Search is also weak: only wikis on repos with 500+ stars are indexed by GitHub's search, and the in-wiki search is barebones. Theming is essentially fixed — you cannot ship a "cohort dashboard" feel. Soft limit of 5,000 files is plenty.

**Verdict:** Fine for a public, lightly-used FAQ. Not a fit when student rosters need gating.

### MkDocs Material
The dominant Python-based docs theme. Built on MkDocs, themed for clarity, and trusted by FastAPI, Pydantic, Polars, Ruff, OpenAI Agents, Kubernetes sub-projects, and 50,000+ others. Markdown source, GitHub Pages deploy via a one-line `mkdocs gh-deploy`, instant in-browser client-side search, math via `pymdownx.arithmatex` + KaTeX or MathJax, Pygments code blocks, admonitions, tabs, content tabs, dark mode, social cards, and a blog plugin that fits "weekly update" posts.

**Important 2026 caveat:** Material entered **maintenance mode in November 2025** with the 9.7.x line. Critical bug fixes and security patches ship through at least November 2026. The maintainer is building a successor called **Zensical**. For an 8-week summer program in 2026, "feature freeze + security patches through November" is exactly the stability profile we want. Migration to Zensical is a 2027 problem.

Authentication: MkDocs Material produces static HTML, so gating must happen at the hosting layer. The simplest path is to publish on GitHub Pages from a private repo (requires GitHub Pro, which the professor likely has via the GMU sponsorship or the $4/month Pro plan) and set Pages visibility to private — only people with repo read access see the site. Alternatives: Netlify Identity, Cloudflare Access, or a tiny FastAPI shim.

### Docusaurus
React + MDX, v3.10.1 in mid-2026 with React 19 support and the "Docusaurus Faster" flag heading toward v4. Beautiful, but it is fundamentally an **app**, not a wiki: every page round-trips through React hydration, MDX components, and a `docusaurus.config.js` that grows fast. Algolia DocSearch is the canonical search (free for open-source projects, application required), and math needs `remark-math` + `rehype-katex`. Multi-author editing works fine through Markdown PRs, but the React/MDX surface means a mentor editing a page may stumble on a `<Tabs>` JSX block. Higher floor than Material; not worth the cost for a 14-person cohort.

### Astro Starlight
The 2026 darling. Starlight 0.39 (May 2026) ships Pagefind search out of the box, dark mode, i18n, autogenerated sidebars with new flexibility for `siblings`/`ancestors`, MDX, Markdoc, and frontmatter validation with TypeScript types. Math via the `starlight-katex` community plugin (one-line install — no manual `remark-math` config). Hosts trivially on GitHub Pages, Netlify, or Cloudflare Pages. Performance is excellent (zero-JS by default).

Two concerns for this use case: (1) Starlight is opinionated toward **product docs**, not classroom dashboards — the homepage hero, "splash" layout, and three-column TOC scream "open-source SDK." It can be tamed, but bending it toward "course schedule with cards" needs custom Astro components. (2) The professor would be the only person on the team writing Astro; mentors editing Markdown is fine, but anything structural means me-or-Claude time.

**Strong runner-up.** If we wanted a slicker visual identity and were happy to invest 4-6 extra hours in Astro components, Starlight wins.

### Wiki.js
Stable 2.5.x in 2026, with a v3 beta in progress. Genuinely full-featured wiki: visual editor, Markdown editor, plain HTML, version diff/rollback, code highlighting, math rendering, 40+ languages, and an authentication menu that covers local accounts, GitHub/Google/Microsoft OAuth, LDAP, SAML, CAS, Auth0, Okta, Azure AD, and 2FA. Free, open source (AGPLv3), self-hosted.

Cost: hosting. Requires Node.js 22+ runtime, PostgreSQL 16, a dedicated subdomain (no subfolder mapping), Docker preferred. A $5-$10/month DigitalOcean droplet plus a domain, plus the professor watching for security updates. **Maintenance burden is real** for a solo-faculty deployment. Overkill for 14 students.

### DokuWiki
PHP, file-based (no database), plays the "boring works forever" card. Recent releases refactored the extension manager, added trusted-proxy support, and modernized the link wizard. ACLs and authentication (LDAP, OAuth via plugins) are mature. Math via the MathJax plugin; code via syntax-highlighter plugins. The UX is honestly 2010-era and will not inspire 16-year-old high schoolers. Skip unless we have to.

### BookStack
Modern wiki app with a Books > Chapters > Pages hierarchy, WYSIWYG editor (and optional Markdown with live preview), diagrams.net integration, full-text search, MFA, OIDC/SAML/LDAP, role-based permissions. Active in 2026 with regular feature and security releases (v25.x line through 2026). Requires PHP 8.1+, MySQL/MariaDB, and self-hosting on a LAMP-style VPS (~£2.50/month IONOS box is enough). Lovely product, but the **Books > Chapters > Pages mental model fights "course dashboard"**: pages live inside books, not on a free-form hub. Same self-host maintenance pain as Wiki.js.

### Outline (mention only)
Cloud SaaS, $10/month for up to 10 members, $79/month for 11-100. With 14 students + mentors + the professor, ASSIP lands on the $79 tier. The 30% education discount drops it to ~$55/month — non-trivial for an 8-week program. Plus, student PII and unpublished research notes on a third-party SaaS is a needless FERPA conversation. Skip.

### Notion (mention only)
Notion's free Plus tier for education exists, but the privacy story for student data on a U.S. SaaS is the same FERPA conversation, and the "block editor" makes version-controlled Markdown impossible. Skip.

### Quarto (mention only)
Already the textbook engine. Could carry the wiki too, but the whole point of this exercise is to give the cohort a **different surface** — a portal, not a book. Same tool for both would dilute the affordance. Skip for the wiki role; keep it for the textbook.

---

## Recommendation: **MkDocs Material**

Reasoning, plainly:

1. **Zero new infra.** Site lives in a GitHub repo alongside the rest of the course materials, builds in GitHub Actions on push, deploys to GitHub Pages. The professor already has this exact pipeline running for the Quarto book.
2. **Markdown-only authoring.** Mentors edit `.md` files via the GitHub web editor (browser, phone, anywhere). No React, no Astro components, no PHP, no Node host to patch.
3. **Free.** GitHub Pro is the only paid surface if we want to gate the site from a private repo; that's $4/month and the professor's GMU sponsorship may already cover it. Otherwise the site is public and we redact roster details.
4. **Math + code + cards + tabs + admonitions** all work first-class. The `pymdownx.arithmatex` + KaTeX combo handles the finance formulas; fenced code with Pygments handles Python snippets; `grid cards` give us the "dashboard" hero we want.
5. **Search is built in**, client-side, instant, no Algolia application.
6. **Maintenance mode is a feature here, not a bug.** Through November 2026 the platform is frozen on a stable, security-patched line. We are not going to live past November 2026 on this site without revisiting it anyway.

**Runner-up: Astro Starlight.** Pick this if we decide we want a visually distinctive front door and are willing to spend 4-6 hours wiring custom Astro components for the course-dashboard look. Starlight 0.39 is genuinely excellent in 2026, search via Pagefind is great, and `starlight-katex` removes the math-setup friction. The only reason it loses is incremental complexity that does not pay for itself at n=14 students for 8 weeks.

---

## Three design directions for the MkDocs Material site

### Direction A — "Course dashboard with grid cards"
Home page is a `grid cards` layout (Material's first-class component): six cards for *This Week*, *Schedule*, *Reading*, *Projects*, *Mentors*, *FAQ*. Left sidebar collapsed by default. Top tabs for the four phases of the program (Weeks 1-2 Foundations, 3-4 Methods, 5-6 Build, 7-8 Polish). Color palette in GMU green/gold; logo top-left. Feels like a hub, not a book. Best for: students who land cold and need to orient in 10 seconds.

### Direction B — "Minimal Notion-like with a left nav"
Hide the top tabs, keep only the left sidebar with collapsible sections (Onboarding, Weekly, Projects, References, Symposium). Wide content column, generous typography, no hero. Search bar pinned top. Closest in vibe to Outline/Notion — a quiet, text-first hub for cohort members who already know where things live. Best for: the steady-state phase when novelty has worn off and the site is a working tool.

### Direction C — "Classic wiki feel with a project tracker"
Lean into wiki affordances: every page has a visible "last edited by" line and a `git log`-driven changelog at the bottom (via `git-revision-date-localized-plugin`). A dedicated "Project Tracker" page renders each student's project as a card pulled from a single `projects.yml` data file (via `mkdocs-macros-plugin`). FAQ uses Material's "Discussion"-style admonitions to mimic talk-page Q&A. Best for: making the wiki feel collectively owned by the cohort rather than authored top-down by the professor.

---

## Implementation notes (so the next step is short)

- **Repo layout:** `/wiki/` subdir in the existing course repo, with its own `mkdocs.yml`. Separate GitHub Actions workflow that runs `mkdocs gh-deploy` on push to `main` for files under `wiki/`.
- **Gating decision:** Start public, redact rosters. Revisit if a student's name/email needs to live on the site; at that point, flip the repo to private and use Pages "private visibility" (requires Pro).
- **Plugins to enable from day one:** `material`, `search`, `pymdownx.arithmatex` (KaTeX), `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.tabbed`, `git-revision-date-localized`, `awesome-pages` (sidebar control), `macros` (for Direction C's `projects.yml`).
- **Theme palette:** `primary: green`, `accent: amber`, `scheme: default` with auto dark-mode toggle.
- **First commit:** Direction A scaffold (grid-card home + four phase tabs) is ~150 lines of Markdown + 40 lines of `mkdocs.yml`. Realistic 60-minute first-day setup.

---

## Sources

- [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/)
- [Material for MkDocs: 2026 Review / Maintenance Mode (Docsio)](https://docsio.co/blog/mkdocs-material)
- [Material for MkDocs — Math reference](https://squidfunk.github.io/mkdocs-material/reference/math/)
- [Astro Starlight documentation](https://starlight.astro.build/)
- [Starlight 0.39 release notes](https://astro.build/blog/starlight-039/)
- [Starlight Docs 2026 review (Docsio)](https://docsio.co/blog/starlight-docs)
- [Docusaurus changelog](https://docusaurus.io/changelog)
- [Wiki.js — Get Started](https://js.wiki/get-started)
- [Wiki.js — Hosting requirements](https://docs.requarks.io/install/requirements)
- [BookStack](https://www.bookstackapp.com/)
- [DokuWiki changes](https://www.dokuwiki.org/changes)
- [GitHub Docs — About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)
- [GitHub Docs — Wiki access permissions](https://docs.github.com/en/communities/documenting-your-project-with-wikis/changing-access-permissions-for-wikis)
- [GitHub Pages — Changing site visibility (Enterprise Cloud)](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)
- [Outline pricing](https://www.getoutline.com/pricing)
