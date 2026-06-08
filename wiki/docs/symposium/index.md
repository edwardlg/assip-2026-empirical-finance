---
title: "ASSIP Research Symposium — August 12, 2026"
description: >-
  Symposium logistics, poster format, dress rehearsal, JSSR submission,
  and the pitch advice from Chapter 8.5 of the textbook.
---

# ASSIP Research Symposium

**Wednesday, August 12, 2026** &nbsp;·&nbsp; George Mason University, Fairfax campus &nbsp;·&nbsp; In-person poster session + virtual breakouts for remote interns.

The symposium is the **single required deliverable** of the ASSIP program. It is also the only public moment of your eight weeks — the day when families, Mason faculty, College of Science leadership, and Mason News press walk the floor and stop at the posters that catch their eye. Everything we do from Week 1 forward is, in some sense, in preparation for the ninety minutes you will spend standing next to a 48"×36" sheet of paper defending the question you chose to spend a summer on.

---

## What to expect on the day

The symposium runs the full day. The program office circulates the final schedule in **late July** (typically Week 6), but the rough shape is:

| Time (ET) | Block |
|-----------|-------|
| 8:30 – 9:30 am | Setup — in-person presenters mount posters; remote presenters open Zoom breakouts and verify share-screen |
| 9:30 – 10:00 am | Welcome from the Dean of the College of Science and the ASSIP Program Director |
| 10:00 am – 12:30 pm | **Poster session A** — odd-numbered projects present; even-numbered visit |
| 12:30 – 1:30 pm | Lunch and family reception |
| 1:30 – 4:00 pm | **Poster session B** — even-numbered projects present; odd-numbered visit |
| 4:00 – 4:45 pm | Faculty awards and closing |
| 4:45 – 5:30 pm | Photos, family time, equipment teardown |

**Remote interns** join via virtual breakouts. Your Zoom breakout is named after your project (`P07 — Jane Doe — Fair Lending`), pinned in the symposium's central Zoom room, and visited by floating faculty judges per the same A/B rotation. Your poster PDF is shared via the GMU symposium SharePoint page so in-person visitors can also see it at a printed kiosk on the symposium floor.

---

## Audience

Plan for a mixed-expertise audience:

- **Mason faculty** from the College of Science (mathematics, computer science, statistics) and from Costello College of Business (finance, accounting, economics) — they will ask technically sharp questions and probably know the literature.
- **Other students' mentors** — economists, biologists, neuroscientists. Generalist questions: *what's the question, what data, what's the finding, what's the threat to inference.*
- **Families and friends of the cohort** — non-technical. Charm matters; technical jargon should be unpacked.
- **College of Science leadership** — the Dean and Associate Dean for Research walk every poster row.
- **Mason News press** — the GMU communications office sends a reporter; selected posters end up in a write-up.

Practice the three-minute pitch in **three registers** — for the faculty expert, for the generalist, and for the family member.

---

## Poster format (recap)

The complete spec is on the [poster template page](../projects/poster-template.md). The non-negotiables:

- **48 inches wide × 36 inches tall**, landscape (horizontal).
- **GMU College of Science official template** *(URL TBD — confirm via <cosassip@gmu.edu>)*.
- PDF with embedded fonts.
- All raster figures ≥ 300 DPI at print size.
- Mandatory QR codes in the footer: one to GitHub repo, one to filed PAP.
- If any figure uses synthetic data: visible "Results based on synthetic data" notice per the [poster template](../projects/poster-template.md#synthetic-results-notice-only-if-applicable).

---

## Dress rehearsal — Monday August 10, 2026

The dress rehearsal is a **mandatory** full-cohort Zoom on **Monday August 10, 2026, 1:00 – 4:00 pm ET**.

Each student gives their three-minute pitch in front of the full cohort and the four RA sub-leaders; Prof. Gao floats between breakout rooms. The goal is to catch:

- Layout problems (text too small, figure unreadable at three feet).
- Pitch problems (the question takes 90 seconds to articulate; the headline result is buried).
- Reproducibility problems (`make all` fails on a clean clone).
- Q&A problems (you don't have a planned answer to the obvious challenge).

You leave Monday afternoon with a list of fixes; you spend Tuesday Aug 11 implementing them and (if needed) reprinting; you walk into Wednesday Aug 12 confident.

The dress rehearsal is **not** a place to debug a regression or rewrite a section. The poster needs to be 95% done by the time you join the Zoom on Monday. If it isn't, escalate to your sub-leader **the Friday before** (Aug 7).

---

## JSSR abstract submission

Every ASSIP intern submits an abstract to the **Journal of Student-Scientists' Research**, published by **Mason Publishing** at GMU. JSSR publishes the full annual proceedings of ASSIP abstracts.

- **Format:** 150 – 250 words; structure mirrors your poster (Question · Data · Design · Headline result · Robustness · Contribution).
- **Authorship:** you are the sole listed author; Prof. Gao is acknowledged as faculty mentor.
- **Submission window:** opens at symposium; closes **approximately early September 2026** (program office confirms the exact deadline on Aug 12; historically the window is ~3 weeks after the symposium).
- **Submission portal:** Mason Publishing's JSSR site — URL circulated by <cosassip@gmu.edu>.
- **Synthetic-data disclosure:** if any reported number is based on synthetic data, the abstract must say so in the first sentence of the Results section.
- **Optional full paper:** a smaller number of students each year submit a full paper to JSSR through the same pipeline by a later deadline.

After submission, JSSR runs a light editorial review and publishes the proceedings volume in the fall — typically October — with a permanent DOI per abstract. You can list "Published, JSSR (2026)" on a college application without hedging.

---

## Pitch advice from the textbook

**Chapter 8.5** ("Defending Numbers in Public") of the [textbook](https://lgao9.github.io/8weeks/) walks through the structure of the three-minute pitch. The short version is below; read the chapter for the full treatment.

### The three-minute structure

| Time | What you say | What you point at |
|------|--------------|-------------------|
| 0:00 – 0:30 | **The question.** One sentence. Why does anyone care? | Top-left of the poster |
| 0:30 – 1:00 | **The data.** Source, window, N. What makes this dataset *the right one* to answer the question. | Data section |
| 1:00 – 1:45 | **The design.** Your specification in one sentence, the identification assumption in another. *Point at the PAP* — "we pre-specified this in our PAP, filed June 30th." | Design section |
| 1:45 – 2:30 | **The headline result.** The figure or coefficient that, if a visitor walked away after thirty seconds, you'd want them to walk away with. | Headline figure |
| 2:30 – 2:50 | **The robustness story.** Three checks. "If you don't believe me on the headline, the four robustness checks here all point in the same direction." | Robustness block |
| 2:50 – 3:00 | **The contribution.** *"What did we know before? What do we know now?"* | Contribution bullets |

Then you stop talking and let them ask.

### What to do when you don't know the answer

A Mason faculty member will eventually ask a question you don't know the answer to. Three good responses, none of which are *"I don't know":*

1. *"That's a great question — the closest thing I tested was X, which suggests Y. I'd want to look more carefully at exactly what you're asking before I gave you a real answer."*
2. *"I don't think my design is identified on that margin — here's why. But it's exactly the next thing I'd run."*
3. *"I haven't tested that. Can I take your email and follow up?"*

Then actually follow up. The professional norm in academic Q&A is *graceful uncertainty*, not bluffing; you start practicing it on Aug 12.

---

## Photos, press, and what to wear

- **Photos** — the College of Science photographer walks the floor. You'll get hi-res photos of you and your poster within a week; many students use them on LinkedIn and college applications.
- **Press** — if a Mason News reporter or external press contact wants to talk to you, you do not have to say yes; if you do, keep it factual and resist the temptation to claim more than your numbers can support.
- **What to wear** — business casual. Mason green is a nice touch but not required. Comfortable shoes — you're on your feet for two-and-a-half-hour blocks. Remote presenters: shirt with collar, plain background, good lighting, mic test before 9:30 am ET.

---

## After the symposium

- **Aug 13 – Aug 31:** debrief week. Push the final poster to your repo; write the JSSR abstract; update the README; tag a release.
- **Early September:** JSSR abstract due.
- **October:** JSSR proceedings volume published; DOI for each abstract.
- **Through the school year:** Prof. Gao remains available for letters of recommendation, college-application advice, and conversation about whether the question you spent the summer on is worth turning into a fuller paper. Email him — many ASSIP alumni stay in touch for years.
