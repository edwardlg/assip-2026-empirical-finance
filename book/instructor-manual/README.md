# Instructor's Manual — ASSIP 2026

This is the teaching companion to the student textbook for **ASSIP 2026** — the **Aspiring
Scientists Summer Internship Program** at George Mason University's College of Science, directed by
Dr. Amanda Haymond Still (cosassip@gmu.edu), with Prof. Lei Gao as the faculty mentor of the
Empirical Finance remote slot. The textbook is a separate document — the eight themed weeks of
chapters, problem sets, notebooks, labs, and assessments a student works through. This manual is
for the person running the room. It does not re-teach the content; it tells you how to *deliver*
it: how to pace the eight weeks against the actual ASSIP calendar (Jun 22 – Aug 12, 2026, full-time
M–F 9:00 am–5:00 pm, remote-only), how to grade every deliverable to one consistent standard, which
errors your strongest students will predictably make and how to catch them, how to run the layered
mentorship that holds a 14-student remote cohort together, how to grade fast and in agreement using
answer keys and anchor work, and how to keep the camp open and compliant for every admitted student
regardless of hardware, budget, accommodation needs, or fee-waiver status.

The six sections are designed to be read in order the first time and consulted by name thereafter.
Every cross-reference inside them is by section name rather than file path, so the manual survives
reordering.

## The six sections

1. **[IM-1 — Pacing Guide](IM1-pacing-guide.md).** The clock. Maps the eight book-weeks one-to-one
   onto ASSIP 2026's eight active program weeks (Mon Jun 22 – Wed Aug 12, 2026), shows the daily
   block structure (9–12 curriculum, 1–4 mentor research, 4–5 cohort sync) that all 14 students
   share Monday through Friday, marks the two holidays (Jun 19 Juneteenth observance the Friday
   before camp opens; Jul 3 Independence Day observance during Week 2), and ends at the **ASSIP
   Research Symposium on Wed Aug 12, 2026**.
2. **[IM-2 — Grading Rubrics (Consolidated)](IM2-grading-rubrics.md).** Every deliverable's rubric
   in one place — daily problem sets, weekly assessments, the **200-point capstone rubric**
   re-allocated for the ASSIP deliverable bundle (Symposium poster + JSSR abstract + 8-minute talk
   + reproducible repo), and the Symposium talk + defense — all built on one standard: a modest
   result honestly stress-tested outscores an ambitious one the student cannot defend.
3. **[IM-3 — Common Student Pitfalls, by Week](IM3-common-pitfalls.md).** The predictable
   misconceptions a smart, well-prepared 16-year-old arrives with or develops, week by week, each
   with a diagnostic question that surfaces it fast and a fix that corrects it without re-teaching
   the chapter. **New for ASSIP 2026**: an ASSIP-specific section on the remote-cohort failure
   modes — silent dropout, pod fragmentation, the wiki ghost town, Zoom-fatigue grading drift, and
   async/sync confusion — that a 14-person remote cohort will produce regardless of curriculum.
4. **[IM-4 — Mentor-Session Facilitation & Guest Lectures](IM4-guest-lectures-mentor-notes.md).**
   How the layered-mentorship model runs — **Prof. Gao's Monday 9–10 am all-hands** for the whole
   14-student cohort, **the four PhD/RA pod sub-leaders' daily 1–4 pm drop-in office hours and 4
   pm pod standups**, and **four guest lectures** dropped into the Wednesday cohort sync across the
   eight weeks.
5. **[IM-5 — Answer Keys & Anchor Work](IM5-answer-keys-anchor-work.md).** How to grade *against*
   the IM-2 rubrics quickly and consistently using Appendix E, the per-week assessment keys, and
   anchor papers pinned at the A/B/C boundaries — plus a worked A-vs-B walk-through against the
   ASSIP capstone bundle (poster + abstract + talk + repo) and a norming protocol for the four
   sub-leaders who are grading their pods' problem sets daily.
6. **[IM-6 — Equity, Access & Compliance](IM6-equity-access.md).** Keeping the access-dependent
   weeks open to everyone — the **\$25 fee + \$1,299 tuition waiver process** for Pell-eligible /
   reduced-lunch students, **WRDS seats via the GMU College of Science institutional allocation**
   coordinated with Dr. Haymond Still's office, Hopper compute, the no-API-key local path, and the
   licensing rule whose violation is a legal problem (not a pedagogical one), made harder in a
   remote cohort because students are working from home machines outside GMU's physical network.

## Before you teach

Four things to internalize before orientation (Thu Jun 18, 2026).

**The cohort is 14 students, full-time M–F, remote-only, in 4 pods of 3 or 4.** Prof. Gao runs the
Monday all-hands; four PhD/RA sub-leaders run their pods daily. IM-4 documents the layered model;
IM-1 schedules it; IM-3 catalogs the remote-cohort failure modes it is designed to prevent.

**The camp is completable with no API key and no out-of-pocket cost.** Every part of it, including
the Week-6 AI module, runs on a local fallback that needs no commercial API key, no personal data
subscription, and no hardware beyond a basic laptop. ASSIP's \$25 application fee and \$1,299
tuition both have full waivers for Pell-eligible / reduced-lunch students, processed through Dr.
Haymond Still's office at application time. A student with no budget is not blocked from any
deliverable. IM-6 is the section that makes sure that design actually reaches each student.

**Licensed data stays on GMU infrastructure.** Per CONVENTIONS §5, CRSP, Compustat, and the other
licensed sources are read-only on GMU's WRDS/Hopper paths and never leave them. Every notebook that
touches licensed data pins its snapshot date. The licensed extract is regenerated from the source,
not copied out — moving licensed data off GMU infrastructure is the one error that caps the
reproducibility rubric row at Missing on its own (IM-6). Remote-only intensifies this: every
student is working from a home machine outside GMU's physical network, so the §5 discipline must be
taught in Week 1 and policed by sub-leaders in their daily drop-ins.

**Two integrity checks are non-negotiable.** First, the **pre-analysis plan is filed as a tagged
commit before the student peeks at confirmatory results** — `git tag pap-filed` must predate every
confirmatory regression in the Git history, or the result is a finding fished from data that
already flattered it (IM-3 Pitfall 7.1). Second, **reproducibility**: the whole pipeline must
regenerate from source under `make clean && make all`, with nothing reported from memory (IM-3
Pitfall 5.1, IM-3 Pitfall 8.3). These are the two things you do not let slide for anyone.

## A note on the program-level weighting

The overall grade weighting proposed in **IM-2 §1** (problem sets / weekly assessments / Week-7
design deliverable / capstone bundle / Symposium defense) is an **editorial proposal for Prof. Gao
to finalize**, not a fixed policy. The per-week assessment files
(`book/weeks/week-0N/assessmentN.md`) remain the authoritative source for each individual rubric;
what IM-2 proposes is only how they sum into a final grade. Treat the program-level percentages as
a starting point pending Prof. Gao's sign-off. The invariant IM-2 defends — that **identification,
execution/robustness, and reproducibility together exceed half the capstone grade** — should
survive any re-weighting.

## A note on the program office

For any institutional question — waiver status, WRDS provisioning, Hopper account paperwork,
accommodations coordination, hardware/bandwidth loans, Symposium logistics, or a compliance
question that needs an institutional answer — the contact is **Dr. Amanda Haymond Still /
cosassip@gmu.edu**. The instructor coordinates with the program office, not around it.
