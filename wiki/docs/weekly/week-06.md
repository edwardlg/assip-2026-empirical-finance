---
title: "Week 6 — Reading the Frontier II (Jul 27 – Jul 31, 2026)"
description: >-
  Text-as-data, modern empirics, and the AI co-pilot for research —
  with responsible-use discipline baked in.
---

# Week 6 — Reading the Frontier II <span class="week-badge upcoming">upcoming</span>

**July 27 – July 31, 2026** · Chapters 6.1 – 6.5 · Lab 6 · Mentor Session 6 · Problem Set 6

> Text-as-data and machine-learning-flavored empirical finance, plus a full module on using LLMs *responsibly* as a research co-pilot.

By Friday your capstone charter is locked. Anything not in the signed charter on Friday at 5 pm is not in your symposium poster on August 12.

---

## Daily schedule

=== "Mon Jul 27"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 6.1 — Kogan, Papanikolaou, Seru & Stoffman (2017)** Reader's Guide (market-based patent value). Work `nb6.1` (patent-value event study). |
    | 1:00 – 4:00 | Capstone team standups (15 min each). |
    | 4:00 – 5:00 | Office hours |

=== "Tue Jul 28"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 6.2 — Hoberg & Phillips (2016)**. TNIC; 10-K cosine similarity. Work `nb6.2` (sklearn vectorization). |
    | 1:00 – 4:00 | Read **Ch 6.3 — Loughran & McDonald (2011)**. Finance sentiment dictionaries. Work `nb6.3`. |
    | 4:00 – 5:00 | Office hours |

=== "Wed Jul 29"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 6.4 — Bartlett et al. (2022) + Bhutta–Hizmo–Ringo** Reader's Guide (fair lending in the algorithmic era; ties to Gao & Sun 2019). Work `nb6.4`. |
    | 2:00 – 3:30 | **Mentor Session 6 — "Responsible AI in empirical research"** |
    | 4:00 – 5:00 | Office hours |

=== "Thu Jul 30"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 6.5 — The AI Co-Pilot for Research (LLM-in-the-Loop)**. Prompt patterns, RAG over 10-Ks, OOS-validated classification, env-var key discipline. |
    | 1:00 – 4:00 | **Lab 6 — RAG over 10-Ks** (offline-safe; live Anthropic / Azure cells are env-gated and optional). |
    | 4:00 – 5:00 | Office hours |

=== "Fri Jul 31"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Wrap PS 6.1 – 6.5. |
    | 1:00 – 3:00 | **Capstone charter — signed off**. Each team presents 5 minutes; Prof. Gao signs (or sends back for revision). |
    | 3:00 – 4:00 | Demo + Week-7 preview |
    | **5:00 pm** | **Deliverable cutoff** |

---

## What to read

- [Ch 6.1 — KPSS 2017 Reader's Guide](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-06/ch61-readers-guide-kpss-2017.html)
- [Ch 6.2 — Hoberg & Phillips 2016 Reader's Guide](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-06/ch62-readers-guide-hoberg-phillips-2016.html)
- [Ch 6.3 — Loughran & McDonald 2011 Reader's Guide](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-06/ch63-readers-guide-loughran-mcdonald-2011.html)
- [Ch 6.4 — Bartlett et al. 2022 + Bhutta–Hizmo–Ringo](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-06/ch64-readers-guide-bartlett-bhutta-fair-lending.html)
- [Ch 6.5 — The AI Co-Pilot for Research](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-06/ch65-ai-copilot-for-research.html)

**Notebooks:** `notebooks/week-06/` — including `nb6.5`, the AI co-pilot lab (offline-safe, env-gated live cells).
**Mentor reading:** Mentor 6 — "Responsible AI in empirical research".

!!! danger "Secrets discipline (mandatory)"
    `nb6.5` and any code that touches an LLM API loads keys **only** from environment variables — never from a literal string in a notebook. Do not commit `.env`. See [Resources → Data access](../resources/data-access.md).

---

## What to submit (due Fri Jul 31, 5:00 pm ET)

1. **Problem Set 6** — PS 6.1 through 6.5.
2. **Lab 6 notebook** with a RAG-augmented classification + an OOS-validated accuracy score.
3. **Capstone charter — signed-off version** in `projects/<team-name>/charter.md`.
4. **Journal entry** — `journal/week-06.md`.
5. **Pull request** — `week-06 — <your name>`.

---

## Data we touch this week

- [EDGAR 10-K / 10-Q](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-10k-10q.html) — for Hoberg–Phillips and LM.
- [USPTO PatentsView](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/uspto-patentsview.html) + [NBER patent linking table](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/nber-patent-link.html) — for KPSS.
- [Loughran–McDonald dictionary](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/loughran-mcdonald-dict.html).
- [HMDA](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/hmda.html) — for the fair-lending paper.

---

## Next week preview

[**Week 7 — Capstone build →**](week-07.md). From research question to pre-analysis plan to cleaned dataset, with the identification memo locked.
