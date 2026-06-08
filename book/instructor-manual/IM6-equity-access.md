# IM-6 — Equity, Access & Compliance

This section is about the parts of running the camp that decide whether *every* admitted student can
actually do the work — not just the ones who arrive with a fast laptop, a paid API key, a family
budget for the tuition, or no accommodation needs — and about the one rule whose violation is not a
pedagogical problem but a legal one. ASSIP 2026 carries an explicit cost (a **\$25 application fee +
\$1,299 tuition**) and a **fee-waiver program** for Pell-eligible and reduced-lunch students; the
curriculum itself is **completable end to end with no commercial API key, no personal data
subscription, and no hardware beyond a basic laptop**, because the licensed-data and compute paths
all route through GMU College of Science infrastructure that the camp provides. Your job as
instructor is to make sure both designs — the cost design and the access design — actually reach
each admitted student. IM-1 (pacing) tells you when the access-dependent weeks land; this section
tells you how to keep them open to everyone.

ASSIP 2026 program facts the rest of this section assumes: host **George Mason University, College
of Science**; director **Dr. Amanda Haymond Still**; program contact **cosassip@gmu.edu**; format
**full-time M–F 9:00 am–5:00 pm**, **Prof. Gao's slot REMOTE only**; orientation **Thu Jun 18,
2026**, first day **Mon Jun 22, 2026**, **Symposium Wed Aug 12, 2026**; audience HS students 15+
(16+ for in-person wet-lab tracks; ASSIP 2026 College-of-Science remote slot is HS 15+ and
undergrads not yet graduated) with **no GPA minimum** and a **two-summer-session lifetime cap**.

---

## ASSIP fees and waivers: the affordability backstop

ASSIP 2026 charges every admitted student a **\$25 application fee** and **\$1,299 in tuition**.
Both have **full waivers available** for students whose families qualify on financial need —
specifically, **Pell-eligible** (parent or guardian eligible for Pell Grant aid, or the student
themselves if independent) and **reduced-lunch** (the student qualified for free or reduced-price
school lunch in the school year prior to application). The waiver is the equity guarantee that
makes the program's cost not the barrier to a strong applicant's participation. Treat it as
load-bearing infrastructure.

**The waiver process, as the instructor needs to know it.**

1. **The waiver request happens at application time, not after admission.** Students applying to
   ASSIP indicate need on the application form (a checkbox plus a brief financial-need statement)
   and upload one supporting document — most commonly the SNAP/free-or-reduced-lunch determination
   letter for the prior school year, or a parent's Pell-eligibility documentation from FAFSA. The
   College of Science admissions office (under Dr. Haymond Still / cosassip@gmu.edu) reviews the
   request alongside the application; admitted students receive their decision letter with the
   waiver determination attached.
2. **The waiver covers both the \$25 application fee and the \$1,299 tuition** when granted in
   full. There is no partial-waiver tier published for 2026; the determination is full-waiver or
   standard-pay. If a family's circumstances change between application and orientation, the College
   of Science will reconsider — Dr. Haymond Still's office is the contact.
3. **The instructor does not handle waiver paperwork** but **must be aware of which students hold
   waivers** for one reason: the materials supplied by the program (laptops loaned for
   bandwidth-constrained students, the WRDS seat under the institutional subscription, the GMU
   Hopper account, the Azure OpenAI allocation) all come *out of program resources* and are equally
   available to waiver and standard-pay students. Make this invisible in the room — no student
   should learn another student's payment status from how mentorship attention is allocated.
4. **Waivered students complete the same program as standard-pay students** — full-time M–F 9–5,
   the same deliverables, the same Symposium poster, the same JSSR abstract, the same 3 GMU College
   of Science credits. The waiver does not change what is expected; it removes the cost barrier to
   participation.

**The instructor's affirmative responsibilities around the waiver.**

- **Before orientation:** Confirm with Dr. Haymond Still's office that every admitted student's
  cost status has been resolved — no admitted student should arrive on Jun 22 still owing a fee
  whose waiver was filed but unprocessed. Send the cohort list to the College of Science admissions
  office in the first week of June and ask for confirmation back.
- **During the camp:** Do not discuss financial status in any cohort-visible forum. If a student's
  pod sub-leader (IM-4) raises a concern about a student's access to materials, devices, or
  bandwidth, route it through the program office, not through public Zoom or the wiki. Treat the
  waiver as a private piece of an admitted student's record, like an accommodation letter.
- **For a student whose home internet is the bottleneck:** Coordinate with the College of Science
  on the loaner-laptop and mobile-hotspot path (the program has historically supported these
  case-by-case for remote interns). This is not a public conversation; it is a private one with
  the sub-leader, the student, and Dr. Haymond Still's office.

---

## WRDS seats: a scarce resource to schedule, not assume

WRDS access for ASSIP 2026 runs on the **GMU College of Science institutional seat allocation**, not
on Costello College of Business's separate seat pool. Coordinate the cohort's WRDS provisioning with
**Dr. Amanda Haymond Still / cosassip@gmu.edu** before orientation; she is the institutional contact
for the College-of-Science allocation that this remote-only cohort uses. Seats are limited and
access is institutional, so treat them as a managed resource from day one.

**Request accounts in the first week of June, in one batch.** Approval is not instant — a WRDS
administrator at GMU's College of Science (or you, acting on the students' behalf through Dr.
Haymond Still's office) must approve each request, and it triggers a credential email. Have every
admitted student register with their **GMU email address** (a personal Gmail is rejected, because
the GMU address is what ties them to the subscription) on day one of orientation, so seats are
live by Week 2's first CRSP work and not scrambling the morning a lab needs them. Confirm each
student can log in to the WRDS web interface once before they need it in a notebook.

**Schedule heavy use; do not let the cohort hammer the shared server at once.** The expensive
moments are the CRSP/Compustat-touching labs — the W2 Fama–MacBeth work, the Week-5 portfolio sorts,
Week 7 capstone data acquisition. With a 14-student remote cohort all hitting WRDS in the same
morning curriculum block, server contention is a real risk; stagger by pod. Have students prototype
query *logic* on the small illustrative `permno` lists the appendix uses (which barely touch the
server) during the curriculum block, then run the full-universe pulls on a rota during the 1–4 pm
mentor research block, or as queued Hopper jobs rather than fourteen simultaneous interactive
`SELECT`s. Appendix B.3 already teaches the etiquette that makes this work — bound every query by
date and identifier, prototype small before scaling — and B.4 gives the batch-job path that takes
load off interactive seats entirely. A student seat is **read-only** and **non-shareable**; sharing
a login is both a security problem and a license violation, so the answer to "I can't get a seat in
time" is never "use a podmate's" — it is "pull a small extract on the available seat, or run it on
Hopper," never shared credentials.

**A student who cannot get a WRDS seat can still complete the camp.** Every WRDS-dependent
deliverable has a public-data path. The capstone gallery includes papers built entirely on public
sources (the USPTO PatentsView innovation paper, the FRED macro event study), and the data
dictionary (Appendix C) documents the public alternatives — FRED, SEC EDGAR, HMDA, USPTO, yfinance
— that carry the fair-lending, text, and macro threads without a CRSP seat. If a seat is delayed or
unavailable for a given student, route their capstone project to a public-data question. No student
is blocked from the Symposium poster or JSSR abstract by a seat queue.

---

## Compute access: Hopper, the AI-module API budget, and the local fallback

The camp's compute needs are met by GMU College of Science infrastructure, with deliberate fallbacks
so that lack of money or hardware is never the barrier. The full-remote 2026 format makes the
fallback paths even more important: a student working from a home laptop on a 50 Mbps connection
needs the same compute access as a student with a fast home setup.

**GMU Hopper accounts for the heavy and the licensed work.** Hopper is GMU's research-computing
cluster (Appendix B.4), and it is where two kinds of work belong: anything that touches licensed
data (because that data must stay on GMU infrastructure — see Compliance below) and anything that
needs a GPU or more memory and time than a laptop has. Getting a student onto Hopper is paperwork,
not coding: a Hopper account tied to their GMU NetID, membership in the camp's allocation/account
string, and the GMU VPN since this cohort is fully remote. Start that paperwork in the first week
of June alongside the WRDS requests, because the AI module in Week 6 and the licensed-data steps in
Weeks 7–8 both assume it is in place. The exact partition names, allocation string, and module
names are cluster-specific and are tagged `[CHECK]` in B.4 — confirm them against ORC's current
documentation before the cohort's first submission, because a wrong partition string is the most
common reason a first job never runs.

**The AI-module API budget, and how to ration it.** Week 6 uses LLMs as a research co-pilot, and the
camp provides access two ways (ch6.5): the Anthropic Messages API directly, and OpenAI-family models
(GPT-5.4 / 4.1 / 4o) through **GMU's Azure OpenAI gateway** (`apim-n1ai-use-gmun1.azure-api.net`),
with the key read from `${AZURE_OPENAI_KEY}` and never hard-coded. API calls cost money against a
shared budget, so ration them: have students develop and debug their prompts and pipelines on a
*tiny* sample (a dozen filings) before they run a classifier over a full corpus, and prefer the
local path for the bulk classification job. The two-provider setup is also a robustness check, not
just redundancy — a result that survives re-labeling with a different vendor's model is stronger
evidence — so spending a little budget to cross-check a headline classification is good practice,
not waste.

**The local-Ollama fallback, and the promise that no key is required.** This is the equity
guarantee that matters most for the AI module: **a student with no API key and no budget can
complete the entire camp**, because the local path runs an open model with **Ollama** on the
student's own machine (an ~8B model serving on `localhost:11434`, data never leaving the laptop) or,
for larger models, on a Hopper A100 node where licensed text already lives and stays. The local
path carries *no API key and no secret of any kind*, because there is no remote service to
authenticate to — which makes CONVENTIONS §5's "secrets via env vars only" rule trivially satisfied
and, more to the point, makes the module free. Tell students this explicitly in Week 6: the API
path is a convenience and a capability boost, not a requirement, and the camp's design assumes some
students will run entirely local. The one cost is capability — an open 8B model is weaker than a
frontier API model — so a locally-labeled classifier needs the *same* out-of-sample
precision/recall/F1 validation against a hand-labeled gold set that any classifier does (ch6.5);
validation is what tells a student whether the free, private choice is also an accurate-enough one,
and if it is not, the larger Hopper model is the escalation, still key-free.

---

## Accommodations for students with disabilities

Run the camp's accommodations through **GMU's Office of Disability Services (ODS)** — registered
accommodations are documented and binding, and you should ask in the orientation-week sub-leader
one-on-ones (privately, not in the cohort Zoom) whether any admitted student has accommodations on
file, then implement them without making the student re-explain. Beyond the formal letter, several
camp-specific points are worth anticipating because the format is intensive, remote, and unusual:

- **Timed and high-stakes work.** The end-of-week assessments and the **8-minute Symposium talk**
  are the timed elements. Extended-time accommodations apply to the assessments as they would to
  any exam; for the Symposium talk, the binding constraint is the *content arc* (question → design
  → result → robustness → contribution), not the stopwatch — coordinate with Dr. Haymond Still's
  office in advance for any student whose accommodation requires a longer talk slot, since the
  Symposium runs to a fixed schedule. The rubric (IM-2 §4b) grades the argument and the defense,
  not raw speed.
- **The notebooks and code.** Make sure the chapter notebooks and any slide decks meet basic
  accessibility — figures with described content for screen-reader users, sufficient color contrast
  in the plots (the CLT animations, coefficient plots, and event-study charts especially), and
  keyboard-navigable tooling. Prefer materials that read well as plain Markdown and LaTeX, which
  the camp already uses, because that format degrades gracefully to assistive technology.
- **The remote format and the daily Zoom load.** Eight hours a day of Zoom is fatiguing for any
  student and disproportionately so for some — students with chronic pain or fatigue conditions,
  attention-related accommodations, or sensory-processing accommodations may need camera-optional
  blocks during specific portions of the day. The default position should be camera-on for the
  cohort sync and Monday all-hands (because cohort glue depends on faces — IM-3 ASSIP-R.1, the
  silent dropout), with camera-off accommodations granted privately by ODS letter without public
  comment. The mentor sessions' written-first structure (warm-ups and stretch questions answered on
  paper) is itself an accessibility feature — it gives every student, including those for whom live
  verbal participation is hard, a prepared way in. Lean on it.
- **Recordings as the documented accommodation path.** Every Monday all-hands, every cohort sync
  guest lecture, and every curriculum-block live demo is recorded with captions and posted to the
  wiki by end-of-day. A student with a documented accommodation can use recordings to revisit
  material at their own pace; the recording is the equity tool the camp's recording discipline
  exists to provide (see IM-3 ASSIP-R.5 for the failure mode where recordings become substitutes
  for synchronous attendance — that failure mode is for students *without* an accommodation; for a
  student *with* a documented one, the recording is the accommodation, full stop).

When in doubt, the principle is the camp's own: the deliverables grade *reasoning and honesty*, so
any accommodation that preserves the student's ability to demonstrate reasoning while removing an
unrelated barrier is consistent with the standard. Coordinate the specifics with GMU ODS through
Dr. Haymond Still's office rather than improvising.

---

## Data-licensing compliance: the §5 rule, restated for the remote ASSIP cohort

This is the one rule in the camp whose violation is not a learning setback but a **breach of GMU's
license agreements**, and it is your responsibility to enforce it across the cohort. The
remote-only format of ASSIP 2026 makes data-licensing compliance *more* important than in a
residential cohort, not less, for two reasons. First, every student is working from a personal home
machine outside GMU's physical network, so the temptation to "pull a quick extract to my laptop"
exists where in a residential cohort the lab desktop would have been the natural workspace.
Second, the WRDS seat is provisioned through the **College of Science institutional allocation**,
which is the seat pool that the College's license terms govern — any compliance breach reflects on
the College's institutional standing with the data vendors and on Dr. Haymond Still's office
directly. Both pressures point the same way: enforce §5 from Day 1 in unmistakable terms.

CONVENTIONS §5 states the rule; here it is in the form ASSIP 2026 instructors need.

**Licensed data stays on GMU infrastructure, read-only. Never have students pull CRSP, Compustat,
TRACE, IBES, or any other licensed dataset to a personal machine or send it to an external API.**
GMU *leases* these datasets under agreements that forbid copying the raw records off GMU-controlled
systems or redistributing them. The professional pattern, which the camp teaches from Week 2
onward, is to **send the query to the data, not the data to the laptop**: the filtering runs on the
WRDS Cloud or on Hopper, and only a small *derived* extract — your filtered, often aggregated
result — comes back as a working product. The terabytes stay put.

What this means in practice for a remote cohort, as the lines you police:

- **No raw licensed datasets on personal laptops.** A small bounded extract for active analysis is
  normal research practice; mirroring a raw dataset is not. When a pull is large or sensitive, it
  runs on Hopper, where the data lives behind GMU authentication end to end. Sub-leaders watch for
  this in their daily drop-in office hours: if a student's screen-share shows a `data/raw/crsp*.dta`
  file on their home machine that is bigger than a derived extract should be, that is the
  conversation to have on the spot.
- **No licensed data in any repository.** The capstone repos (Lab 7, Lab 8) must *not* ship CRSP or
  Compustat bytes. The repo holds *code* — a pinned access script that re-pulls identical bytes for
  a reviewer who has their own seat — never the licensed data itself. The template `.gitignore`
  already blocks `*.dta`, `*.sas7bdat`, and `data/raw/`; pushing a CRSP `.dta` to GitHub is
  redistribution and breaches the license. Audit every student's repo for this before any capstone
  is deposited for the Symposium and before any JSSR abstract is filed.
- **No licensed text to a commercial API.** Sending raw CRSP/Compustat/TRACE-licensed text to an
  external LLM over the public internet may violate the data-use agreement regardless of the
  vendor's privacy policy — the data is not the student's to transmit. When the text to classify is
  licensed, the model runs *locally* (Ollama on the laptop, or an open model on a Hopper A100), so
  the text never crosses the boundary. This is the same local-fallback path that also makes the
  module free; here it is doing double duty as the compliance mechanism.
- **No shared WRDS credentials, ever.** Sharing a login is both a security problem and a license
  violation. The §5 secrets rule — credentials via `.pgpass` or environment variables, never in
  code, never pasted where a podmate can see them on Zoom screen-share, never written in a wiki
  page — exists precisely so no student ever needs to share a password.
- **Pin the snapshot date.** Every notebook that touches licensed data records the date its
  CRSP/Compustat snapshot was pulled, because vendors revise history and a result is only
  reproducible relative to *when* it was pulled. This is reproducibility hygiene and a compliance
  trail at once.

The clean mental model to teach and to enforce: **the recipe travels; the protected ingredients
stay in the GMU kitchen.** Anyone with a student's repo and their own WRDS seat can rerun the code
and regenerate the extract from the source — that is reproducibility done right. What no one can
do, and must not be able to do, is read GMU's licensed data *out of a student's repository or
laptop*, because it was never there. Make this rule explicit in Week 2 when students first touch
WRDS, restate it at the Lab 7 repo build, and verify it at the **Symposium capstone deposit** and
the **JSSR abstract submission**. A hard-coded secret or shipped licensed data is the one error
that caps the reproducibility rubric row at Missing on its own (IM-2 §4c, CONVENTIONS §5), and the
one error that has consequences beyond the gradebook — it touches the College of Science's
institutional license with the vendor and Dr. Haymond Still's office's relationship with WRDS.

---

## A note on the program office contact

For anything in this section — waiver questions, WRDS provisioning, Hopper account paperwork,
accommodations coordination, bandwidth/hardware loans, or a compliance question that needs an
institutional answer — the contact is **Dr. Amanda Haymond Still / cosassip@gmu.edu**. The
instructor is not the program office; do not improvise. Coordinate, document, and route through the
office that owns the institutional relationships, because those relationships are what make this
8-week program possible for every admitted student.
