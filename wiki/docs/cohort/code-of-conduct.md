---
title: "Code of Conduct"
description: >-
  Intellectual honesty, responsible AI use, data licensing, and
  confidentiality. The non-negotiables for the ASSIP 2026 cohort.
---

# Code of Conduct

This is a short document. It is short because the principles are simple and because the consequences of violating them are not. By accepting your seat in the ASSIP 2026 Empirical Finance Research Group you agree to the standards below; they apply to every student, RA sub-leader, and the faculty mentor equally.

---

## 1. Intellectual honesty

Every number, figure, regression coefficient, and sentence you submit must be the one your analysis actually produced. If a number doesn't reproduce when you run the pipeline again, fix the pipeline before you fix the number. If your story doesn't survive a robustness check, change the story.

This means:

- **No p-hacking.** No running 200 specifications and reporting the one that crosses 0.05.
- **No HARKing** (Hypothesizing After Results are Known). The Wednesday-mentor-session conversation about what counts as a finding will return to this repeatedly.
- **No "I'll just adjust the figure a little to make the point clearer."** Figures are evidence, not illustration.

---

## 2. No fabrication

**Fabrication of data, results, or citations is the single fastest way to be removed from this cohort.** This is not a question of degree or of intent; there is no minor case of fabrication. If you do not have the data, say so. If your specification doesn't run, file an issue. If you need synthetic data to prototype, label it loudly and obviously per the [poster template](../projects/poster-template.md#synthetic-results-notice-only-if-applicable).

This applies to:

- Numerical results you didn't actually compute.
- Citations to papers you didn't actually read.
- "Data" you generated with AI and didn't disclose.
- Sample sizes, N's, t-statistics, p-values invented to round a story.

ASSIP's standard here is the same as Mason's standard for any research student.

---

## 3. No plagiarism

Words, code, figures, and ideas all have authors. When you use someone else's:

- **Words** — quote them with the quotation marks and cite the source.
- **Code** — keep the LICENSE file, name the original author in a `# Adapted from …` header, and don't claim authorship of a fork.
- **Figures** — recreate them from raw data; never copy a published figure into your poster.
- **Ideas** — name the paper or the person in your introduction; cite in the references.

The benchmark is the one you'll be held to in college: if a reader couldn't, in five minutes, find out where you got something, you haven't cited it well enough.

---

## 4. Responsible AI use

You may use AI assistants (ChatGPT, Claude, Copilot, Gemini, the GMU Azure APIM models) in your work. Many of you should. AI tools, used well, are how a high-school student can produce college-level empirical work in one summer. But:

The standard is set in **Chapter 6.5** of the [textbook](https://lgao9.github.io/8weeks/) ("Responsible AI Use in Empirical Research"). Three rules from that chapter:

1. **Disclose, in writing, in every artifact you ship.** A line in your PAP, in your poster's footer, and in your JSSR abstract. Be specific — *"GPT-5 was used to help debug the pandas `groupby` calls in `code/02_merge.py`. All resulting numbers were verified against a hand-written sanity check."*
2. **Verify every number.** AI confabulates with confidence; if a chatbot tells you the coefficient on `MLadopt` is –0.012, do not put that on your poster until your own code produces it.
3. **Do not paste in confidential data.** Never paste WRDS data, GMU credentials, license keys, or family-identifying information into a public LLM prompt. Use the on-prem GMU Azure APIM endpoints if you need an LLM over confidential data; if in doubt, ask.

---

## 5. Data licensing compliance

We work with a mix of public-domain data (HMDA, ACS, USPTO PatentsView, FRED) and licensed data (WRDS — CRSP, Compustat, IBES, TAQ, dealscan, etc.).

- **Public-domain data** — you may share, redistribute, and publish derived figures freely. Cite the source.
- **WRDS data stays on GMU infrastructure.** Period. Do not download a CRSP daily-returns file to a personal laptop, do not upload it to GitHub, do not paste it into an LLM, do not share it with a sibling who is not also on a Mason credential. The GMU WRDS license terms govern; the [textbook Appendix C](https://lgao9.github.io/8weeks/) data-cards spell out which datasets are which.
- **Derived results** (regression tables built from WRDS data) **may** be published — the license restriction is on the raw data, not on coefficients that summarize it.
- **Hand-coded or scraped data** — declare the license at the top of the file and stick to it.

Violating a WRDS license is the kind of thing that gets the whole university's access suspended, not just yours. Take it seriously.

---

## 6. Confidentiality of work-in-progress

This is not about secrecy — your final poster will be public on August 12 and your JSSR abstract is published — but about the difference between *in progress* and *published*.

- Other students' draft PAPs, half-baked figures, and "I'm not sure yet" findings are theirs to share, not yours.
- Do not screenshot a teammate's Slack message and post it elsewhere.
- Do not push another student's branch to a public repo on their behalf without their written go-ahead.
- Symposium-day press contact (Mason News, family, alumni) is fine; please don't blog "preliminary results from a friend in another pod."

The professional norm in academic research is *generous about credit, careful about provenance*. We start practicing it on day one.

---

## 7. Reporting concerns

If you observe a possible violation of any of the above — by yourself, a peer, an RA sub-leader, or the mentor — the escalation path is:

1. **Pod RA sub-leader** (Slack DM or 1-on-1).
2. **Prof. Gao** if the concern is about your sub-leader, or if step 1 didn't resolve it.
3. **ASSIP Program Office** (<cosassip@gmu.edu>) if the concern is about Prof. Gao, if the prior steps didn't resolve it, or if you would prefer an institutional channel.

Concerns can be raised anonymously to the program office; retaliation against anyone who raises a concern in good faith is itself a code-of-conduct violation.

---

## Why we wrote this down

You are doing real research at a real university with real data. The standards above are not "stricter than school"; they *are* school, the school you are about to be in. The point of writing them down is so that when something feels off in week 4, you don't have to invent the rule on the spot — you can point at this page, name the principle, and keep moving.
