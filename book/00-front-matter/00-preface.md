# Preface

*by Lei Gao*

To the fourteen of you who will form the ASSIP 2026 Finance and Data Science cohort: welcome. I am writing this in the days before our June 18 orientation, knowing your names but not yet your handwriting, your questions, or the particular ways each of you will get stuck and then unstuck over the next eight weeks. By the time you read this, you will have already accepted a seat in something genuinely unusual — a remote-only, full-time, federally-public-data research apprenticeship inside the College of Science at George Mason University, ending in a poster you will defend in front of faculty, mentors, families, and the press on Wednesday, August 12. I want to use this Preface to tell you, as plainly as I can, what we are doing together and why I think you are ready for it.

## What ASSIP is

The Aspiring Scientists Summer Internship Program — ASSIP — is George Mason University's flagship summer research apprenticeship for high school students aged 15 and up and undergraduates who have not yet graduated. It is run out of the College of Science under the direction of Dr. Amanda Haymond Still (cosassip@gmu.edu), and it has, year after year, placed quantitatively serious young people inside the working research groups of Mason faculty. There is no GPA minimum; what gets you in is a willingness to do real work. The program is full-time, Monday through Friday, 9:00 a.m. to 5:00 p.m., from your first day on Monday, June 22 through the symposium on Wednesday, August 12 — roughly eight active weeks once we subtract the Juneteenth observance on June 19 and the Independence Day observance on July 3. Tuition is $1,299 plus a $25 application fee, with full waivers for Pell-eligible and reduced-lunch students; you also earn three College of Science credits, attend the scientific-writing workshops and career forum, and — crucially — publish an abstract in the *Journal of Student-Scientists' Research* (JSSR), Mason Publishing's peer-edited venue for ASSIP work. An optional full paper is available to those of you who want to keep going past the symposium.

Two facts about our particular group matter, and I want to put them on the table now.

The first is that **Prof. Gao's 2026 slot is officially remote-only.** We will not gather in a wet lab on the Fairfax campus. We will gather every weekday morning on video, in the shared documents we are building together, and in a wiki that, by week eight, will be the single most valuable artifact this cohort produces after the posters themselves. I will say more about what that asks of you in a moment.

The second is that **fourteen is the high end of a typical ASSIP group.** The College of Science describes a normal mentor-to-intern ratio of roughly 2-to-15, and fourteen of you under one faculty mentor is at the upper bound of what works. I am not going to pretend I can give each of you the same one-on-one attention I would give a group of three. Instead, we will run a layered structure: I am the faculty mentor, and beneath that layer is a small team of PhD students and research assistants from my own program who will serve as sub-leaders — each owning a project pod of three or four of you, running the daily 9:00 a.m. standup, doing the first read of your code, and escalating to me what needs escalating. This is how working research labs actually operate. You will see it from the inside.

## Why this track, and why finance and data science

I run a research program at the Costello College of Business that lives at the intersection of empirical finance, household credit, and the institutional plumbing of markets. The questions I keep returning to — and the questions I want to share with you this summer — fall into four clusters, and I will name them honestly so you can see what kind of work the cohort will sit next to.

*Fair lending.* In Gao and Sun (2019), published in the *Proceedings of the National Academy of Sciences* (volume 116, issue 19, pages 9293-9302), my coauthor and I used millions of public mortgage records to ask whether same-sex couples were treated differently when they applied to borrow. The answer, and the way we had to construct it to be trusted by regulators and economists, taught me almost everything I now believe about identification and standards of proof.

*Common ownership.* In Gao, Han, Kim, and Pan (2024), in the *Journal of Corporate Finance* (volume 84, article 102520), we ask what happens when two firms that buy and sell from each other share large institutional shareholders — whether that overlapping ownership changes how aggressively the supplier shapes the earnings number it reports. It is a question about who, really, is keeping public companies honest.

*Market microstructure.* In Gao, Han, Li, and Zhou (2018), in the *Journal of Financial Economics* (volume 129, pages 394-414), we measure whether the first half-hour of trading predicts the last — an intraday momentum effect — and, more importantly, whether you can measure it without fooling yourself.

*AI in finance.* This one is newer, and I will be honest with you about where the field is genuinely settled versus where it is still arguing with itself. We will read together, we will build, and we will hold the same evidentiary bar to a transformer that we hold to a regression.

Some of you will end up writing your poster on a question close to one of these threads. Some of you will go somewhere else entirely — to FRED macro series, to SEC EDGAR filings, to climate-risk insurance data — and that is welcome. What I am committing to is that every project this cohort produces will use real public data and a defensible research design.

## The arc of the eight weeks

Here is how the summer is built.

The first stretch builds your inferential foundations: how a regression actually works underneath the convenient interface, what its standard errors are really claiming, and the specific ways it lies to you when its assumptions break. The middle stretch is about the question that separates a finding from a coincidence — *causation* — and the modern toolkit (natural experiments, difference-in-differences, instrumental variables, regression discontinuity) that lets a careful researcher say "this caused that" and mean it. The later stretch turns you loose: you will read at the research frontier the way a critic reads, find a question of your own, and see it through to a poster you can defend.

The destination is fixed. On **Wednesday, August 12, 2026**, the ASSIP Research Symposium runs an in-person poster session on the Fairfax campus and virtual breakout rooms for remote interns — that means you. Faculty, mentors, families, College of Science leadership, and the Mason News press will be in the room and on the call. Your poster, and the JSSR abstract that accompanies it, are not optional decorations. They are the deliverables.

## What remote-only asks of you

Working remotely full-time for eight weeks is not a softer version of working in person. It is, in some ways, harder. There is no hallway in which to overhear the answer; there is no lab bench at which to be physically stuck next to someone who can unstick you. What replaces those things is structure, and I am asking you to take it seriously.

We will meet every weekday at 9:00 a.m. for a daily standup — what you did yesterday, what you are doing today, what is blocking you. Your pod sub-leader will be available throughout the day on chat. Code goes into the shared repository. Notes, dead ends, and breakthroughs go into the cohort wiki. The wiki is the shared brain of this group; it is how fourteen of you make each other smarter than any one of you could be alone. If you discover a quirk in the HMDA loan-application file, write it down. If you find a clean way to merge CRSP with Compustat permnos, write it down. If you spend three hours chasing a bug that turned out to be a timezone, write *that* down, because three of your colleagues are about to chase the same bug.

## The bar

I owe you, in writing, the standards I will hold you to — because the standards are the whole point.

We use real public data: CRSP for equity prices, HMDA for mortgage applications, FRED for macroeconomic series, SEC EDGAR for filings. No toy datasets I invented to make a point.

We practice honest identification. When you claim one thing affects another, you will name the threat to that claim and the feature of your design that addresses it. No hand-waving that something "controls for endogeneity." Which specific alternative explanation worried you, and what did you actually do about it?

We replicate. Every number in your poster must come from code that runs start to finish on a clean machine and produces exactly that number.

We do not hand-wave. When a result is fragile, we say how fragile. When we do not know, we write "we do not know" — which, for a researcher, is one of the most respectable sentences in the language.

## A note on the cohort

The fourteen of you are going to need each other. The wiki is not a chore; it is the shared infrastructure of a real research group. The standup is not a check-in; it is how the pod stays a pod. I have watched cohorts where the strongest students hoarded what they knew and the weaker students drifted, and I have watched cohorts where everyone wrote everything down and the median rose dramatically by August. I am asking you to be the second kind.

I will see you at orientation on Thursday, June 18, and I am genuinely looking forward to August 12 — to standing in the virtual breakout room while each of you walks me, and a stranger, through the question you chose, the data you used, the design you defended, and the number you are willing to put your name on.

Let's get to work.

— Lei Gao
Costello College of Business, George Mason University
Faculty Mentor, ASSIP 2026 Finance and Data Science Track
