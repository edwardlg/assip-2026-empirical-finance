---
title: "FAQ — Frequently Asked Questions"
description: >-
  The 15 questions that come up every summer in the ASSIP Empirical
  Finance Research Group, answered in one place.
---

# FAQ

The questions below cover the practical mechanics of ASSIP 2026 — the daily schedule, data access, attendance, deliverables, AI policy, and the August 12 symposium. If your question isn't here, ask in Slack `#help-meta` or email Prof. Gao directly.

---

??? question "What's the daily schedule?"
    Monday through Friday, **9:00 am – 5:00 pm Eastern**, fully remote.

    - **9:00 – 9:30 am** — async warm-up (read the day's pages in the textbook, pull latest from the repo).
    - **9:30 – 9:45 am** — pod stand-up on Slack huddle (RA sub-leader runs).
    - **9:45 am – 12:00 pm** — solo work or paired coding on labs/PSets.
    - **12:00 – 1:00 pm** — lunch.
    - **1:00 – 5:00 pm** — block of work, mentor sessions, or pod working sessions per the [weekly schedule](../weekly/index.md).
    - **5:00 pm** — commit-by-5 norm: whatever you have today is pushed to your branch by 5:00 pm ET.

    The Wednesday mentor session with Prof. Gao runs **2:00 – 3:30 pm ET** and is the one fixed weekly anchor.

??? question "How do I get WRDS access?"
    Your GMU NetID is provisioned by the College of Science during the **June 18 orientation**. The program office issues each student a temporary GMU credential that lets you log in to WRDS through Mason's institutional subscription.

    1. Log in to <https://wrds-www.wharton.upenn.edu/> with your GMU NetID.
    2. The first time, you'll be asked to accept the WRDS user agreement — read it; it's the same agreement you're already bound by under the [Code of Conduct](../cohort/code-of-conduct.md).
    3. Set up SSH key access if you want to use the WRDS Cloud Linux machines (recommended for jobs that take more than ~5 minutes).

    If your credential isn't working by **Thursday of Week 1**, email <cosassip@gmu.edu> Cc Prof. Gao. WRDS data **stays on GMU infrastructure** — do not copy it to a personal laptop.

??? question "What if I miss a day?"
    Missing one day is fine; let your pod RA sub-leader know on Slack the night before (or the morning of, if it's unexpected) and the cohort moves on. Tell your sub-leader what you'll skip and what you'll catch up on.

    Missing more than one day per week, or missing the Wednesday mentor session, requires a heads-up to **both** your sub-leader **and** Prof. Gao before the absence — not after. Repeated unplanned absence may put your enrollment at risk because the program is full-time by design.

    Genuine emergencies (medical, family) are handled through the ASSIP program office; email <cosassip@gmu.edu> and we'll make it work.

??? question "Where do I file my PAP?"
    In your project repo, at `pap/pap-v1.md`. The full filing procedure (copy the template, open a PR, get sub-leader review, get Prof. Gao sign-off, `git tag pap-v1`) is on the [PAP template page](../projects/pap-template.md). Update your card on the [project tracker](../projects/index.md) once the tag is pushed.

    The substantive standard for the PAP is set in **Chapter 7.3** of the textbook.

??? question "How do I prepare for the symposium?"
    Three concrete things, in order:

    1. **Build the poster** to spec (48"×36" landscape, the structure in the [poster template](../projects/poster-template.md)). Draft due **Friday Aug 7**, revisions due **Monday Aug 10**.
    2. **Practice the three-minute pitch** out loud, in front of someone who isn't in your pod, at least three times before symposium day. Chapter 8.5 walks through the structure.
    3. **Run the pipeline from scratch on Monday Aug 10** — `make clean && make all` should produce every figure on your poster from raw data with zero errors. The dress rehearsal on Aug 10 is the last point at which we'll catch a layout problem before printing.

    The symposium itself runs the full day **Wednesday August 12, 2026**, in-person at GMU's Fairfax campus with virtual breakouts for remote interns.

??? question "What's JSSR?"
    The **Journal of Student-Scientists' Research** (JSSR), published by **Mason Publishing** at GMU. Every ASSIP intern submits an abstract — 150 – 250 words, the same structure as your poster — and JSSR publishes the full set of abstracts annually as a single proceedings volume.

    - **Format:** 150 – 250 words. Structure: Question · Data · Design · Headline result · Robustness · Contribution.
    - **Due:** approximately **early September 2026** (the program office confirms the exact deadline at symposium). Submission is through Mason Publishing's website; <cosassip@gmu.edu> circulates the link.
    - **Co-authorship:** you are the sole listed author of your abstract; Prof. Gao is acknowledged as faculty mentor in the acknowledgments line.
    - **Optional full paper:** students who want to write the full paper (which a smaller number of ASSIP interns do each year) submit through the same Mason Publishing pipeline by a later deadline.

??? question "Can I use AI tools (ChatGPT, Claude, Copilot)?"
    Yes — with disclosure, verification, and never on confidential data. The full policy is in **Chapter 6.5** of the textbook and in [Section 4 of the Code of Conduct](../cohort/code-of-conduct.md#4-responsible-ai-use). Short version:

    - **Disclose** specifically, in writing, in your PAP, poster, and JSSR abstract.
    - **Verify** every number, citation, and code snippet against your own implementation.
    - **Never paste WRDS data, GMU credentials, or family-identifying info** into a public LLM. Use the on-prem GMU Azure APIM endpoints (GPT-5.4, 4.1, 4o, Maverick) for anything sensitive.

??? question "Do I need to know Python before Week 1?"
    No. AP Statistics-level math and a willingness to break things are the only real prerequisites. Week 1 starts at "what is a list in Python," and the textbook's Chapter 1 lab walks you from a blank `.py` file to a working LLN/CLT simulation. The pod sub-leaders are excellent at unblocking syntactic stuckness.

    What you cannot skip: showing up every weekday with your laptop open and the previous day's notebook ready to discuss.

??? question "Do I get college credit?"
    Yes — **3 GMU College of Science credits** for completing ASSIP. The grade is determined by the symposium poster, the PAP timestamp, and your sub-leader's evaluation of your work over the eight weeks.

    Whether those credits transfer to your home high school or undergraduate institution is determined by *that institution's* policies, not by ASSIP or Prof. Gao. Email the program office (<cosassip@gmu.edu>) for the official transcript and bring it to your registrar.

??? question "How much does ASSIP cost?"
    The published 2026 costs are:

    - **Application fee:** \$25 (non-refundable).
    - **Tuition:** \$1,299 for the full eight-week program.
    - **Full waivers** are available for students who are **Pell-eligible** or qualify for **free/reduced lunch** at their school. The waiver application is on the ASSIP website; the program office reviews it.

    Email <cosassip@gmu.edu> for waiver paperwork; ask early so it's resolved by the start date.

??? question "What does 'remote only' mean for our group in 2026?"
    Prof. Gao's 2026 slot is officially **REMOTE only** — every meeting, every mentor session, every pod stand-up runs on Zoom. You do not need to travel to GMU's Fairfax campus *except* for the August 12 symposium (and even that has a virtual breakout option for remote interns who cannot travel).

    Remote does not mean async; the program is still full-time, 9 am – 5 pm Eastern, with mandatory cohort sessions. You need a reliable laptop, a reliable internet connection, and a quiet place to work for the eight weeks.

??? question "What if my project's results don't replicate or come out null?"
    Excellent — that's a finding. Most of empirical finance is null results, and the August 12 audience knows this. Your poster's value comes from a credible question, a credible PAP, a clean specification, and an honest report of the result. If you reject H₀, fine; if you fail to reject H₀, also fine — but only if you can quantify how *precisely* you failed to reject it.

    Chapter 7 of the textbook makes the case at length. The shortest version: *"underpowered" is not a synonym for "no finding"; it is itself a finding about how much more data the question would need.*

??? function "Can I use my own data or topic instead of one of the five tracks?"
    Yes, with Prof. Gao's sign-off in Week 1. Off-track topics need to:

    1. Have a data source you can actually access within the first two weeks (no "I'll ask the Fed for it").
    2. Have a specification you can run in the eight-week window.
    3. Have at least one anchor paper you can read by Friday of Week 2.

    Some of the best projects in past cohorts have been off-track. Some of the worst have, too. The difference is usually whether constraints (1) and (2) were realistic. Bring the proposal to the Wednesday-of-Week-1 mentor session.

??? question "What happens if I can't finish the poster in time?"
    Tell us early — by **Wednesday of Week 7** at the latest, ideally earlier. The program office and Prof. Gao have several routes for students who are close to done but not quite there (a partial-results poster that focuses on the design and the data; a synthetic-data poster with the [synthetic-results notice](../projects/poster-template.md#synthetic-results-notice-only-if-applicable); a delayed JSSR submission).

    The thing that does not work is showing up on Aug 12 with no poster. Tell the cohort early; we'd rather find the smaller deliverable that works than have a no-show on symposium day.

??? question "Who is the boss of this — Prof. Gao or ASSIP?"
    **Both, on different things.** Prof. Gao runs the empirical-finance content, the mentor sessions, project sign-off, and the day-to-day standard of the cohort. The **ASSIP program office (Dr. Amanda Haymond Still)** runs admissions, tuition, waivers, credit, the symposium logistics, JSSR submission, and any code-of-conduct concern that crosses outside our mentor group.

    The [Mentors page](../cohort/mentors.md) has a "who to ping for what" table that resolves most cases. When in doubt, Cc both — better to over-Cc than to miss a deadline because the email went to the wrong person.
