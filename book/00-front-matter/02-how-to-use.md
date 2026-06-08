# How to Use This Book

Welcome to ASSIP. You are sixteen, give or take, you have just been admitted to the **Aspiring Scientists Summer Internship Program** at George Mason University's College of Science, and for the next eight weeks empirical finance research is your full-time job. This book is the textbook half of that job. Read this section once, all the way through, before Week 1 starts. It will save you a lot of time, and it will tell you why the parts are shaped the way they are.

## What ASSIP is, and what our cohort looks like

ASSIP is GMU's flagship summer research internship for high schoolers (15+; 16+ for in-person wet-lab work) and undergraduates who have not yet graduated. There is no GPA minimum, you may do up to two summers, and the program is directed by Dr. Amanda Haymond Still (cosassip@gmu.edu). Orientation is **Thursday, June 18, 2026**; the first working day is **Monday, June 22, 2026**; and the program ends with the **ASSIP Research Symposium on Wednesday, August 12, 2026**. We lose **Friday, June 19 (Juneteenth)** and **Friday, July 3 (Independence Day observance)**, which leaves roughly eight net active weeks — exactly the eight-week ladder this book climbs.

Our group is unusual. Prof. Gao's 2026 ASSIP slot is officially **remote-only**, full-time Monday through Friday, **9:00 am to 5:00 pm Eastern**. ASSIP groups normally run between two and fifteen students with a single faculty mentor; ours sits at the very top of that range with **fourteen interns**. Fourteen remote teenagers cannot all queue up for the same professor between problems, so we run a **layered mentorship** model. Prof. Gao steers the cohort, sets weekly direction, and reviews milestones. Day-to-day questions go first to one of our **PhD students or research assistants serving as sub-leaders**, each of whom owns a **research pod of three to four students**. Your pod is where you live: it is the people you Slack first, the people who see your half-finished notebook before anyone else does, and the people whose code you will review on Friday afternoons.

The fourteen real people in your cohort — names, photos, projects, pod assignments, mentor on call, and the rolling schedule — all live on the **cohort wiki** at [../wiki/index.html](../wiki/index.html). The wiki is the source of truth for who-does-what-when. The book is the source of truth for what-it-means-and-why.

## The five students in the worked examples are not your classmates

As you read, you will keep meeting **Maya, Devon, Priya, Sam, and Leah**. They have a fight with a partial derivative, they argue about whether to cluster standard errors, they break a regression on purpose to see what the output looks like when an assumption fails. They are recurring characters in the worked examples — a teaching device, like Alice and Bob in a cryptography book — **not real members of your cohort**. The fourteen real people are on the wiki. The five fictional ones are in the chapters because watching a character get something wrong and recover is one of the fastest ways to learn what "wrong" actually looks like.

## The reveal-the-trick learning model

Every technical idea in this book is taught in the same four-beat rhythm. First, we **state the result in one plain sentence** — what the tool does, in words, before any symbols. Second, we **show why it works**: the intuition, then a worked example with actual numbers you can check by hand, and then the algebra that generalizes the example. Third — the beat most textbooks skip — we **show you when it fails**: the assumption that breaks, what you see in your output when it breaks, and how to tell a result from an artifact. Fourth, we **show the code**, runnable on real data.

We call this revealing the trick because that is what it is. A statistical method is a clever, specific maneuver that works under stated conditions. A magician's trick stops being impressive once you know how it is done; a *scientific* trick becomes more powerful, because now you know exactly when you are allowed to use it. The goal is for you to never be intimidated by a method again, and never fooled by one either.

## Your daily rhythm — full-time, remote, 9 to 5

Eight hours a day for eight weeks is a lot of structure, and remote work without structure is mostly distraction. Here is the daily loop. Treat it as the default; your pod sub-leader will adjust it for your project as you get further into the research half.

- **9:00 – 9:15  Cohort standup** in the group chat. Three lines from each of the fourteen of you: what you finished yesterday, what you are doing today, what is in your way. Camera optional. Two minutes per person, hard cap.
- **9:15 – 12:00  Curriculum block.** Today's **chapter section**, today's **notebook**, today's **problem set** — in that order. This is the book half of the day.
- **12:00 – 1:00  Lunch.** Off camera, off Slack. Eat. Walk. The afternoon is harder than the morning and you will need the break.
- **1:00 – 4:00  Mentor-led research** on **your** project. This is where the eight weeks actually go somewhere — running your own pipeline on your own data, with your pod sub-leader on call and Prof. Gao reviewing milestones. The morning teaches you the trick; the afternoon is where you use it on a question nobody has answered yet.
- **4:00 – 4:45  Peer support / lab-mate review.** Inside your pod, swap notebooks. Run each other's code on a clean kernel. Read each other's regression tables out loud and ask the awkward question. Most bugs and most overclaims die here, before they reach the mentor.
- **4:45 – 5:00  Wrap.** Push your commits. Update your row on the wiki's **project tracker**: today's progress, tomorrow's plan, blockers. Two sentences in your research log. Then close the laptop.

A good day arrives at the 1:00 mentor block with a specific question and a specific number you cannot explain. Do not arrive having read nothing; do not arrive having read everything and tried nothing.

## How the parts interlock

The four morning artifacts do four different jobs and they are not interchangeable.

**Chapters** carry the ideas — five per week, read in order. **Notebooks** mirror the chapters one-for-one in Jupyter, with sample output so you can confirm your environment is producing the right answers and a **"Your Turn"** extension at the end that hands you a related question with less scaffolding. Notebooks that touch licensed data (CRSP, Compustat, and the like) pin the exact snapshot date they were run against and note that the licensed data stays read-only on GMU infrastructure. **Problem sets** test whether you actually understood the chapter or merely nodded along; some are by-hand derivations, some are short interpretation prompts, and some ask you to break a method on purpose so you can recognize the failure later. **Labs and reading guides** — the latter starting in the middle weeks, when we dissect published papers including Prof. Gao's own — are where you defend reasoning out loud.

The afternoon research block is **your project**, and it ladders up to one terminal deliverable.

## The terminal deliverable: poster + JSSR abstract for the August 12 symposium

Every ASSIP intern presents at the **ASSIP Research Symposium on Wednesday, August 12, 2026**. In-person interns hang a poster in the hall; remote interns — that is us — present in virtual breakout rooms, with Mason faculty, mentors, families, College of Science leadership, and Mason News press in the audience. Two pieces are required of you:

1. **A research poster** for the symposium. Standard ASSIP scientific format: question, data, design, identifying assumption in one sentence, results, robustness, limits, what's next.
2. **An abstract published in JSSR** — the *Journal of Student-Scientists' Research*, hosted by GMU Mason Publishing. This is a real edited venue; your name goes on a citable record.

A full paper is optional but encouraged. You will also earn **three College of Science credits** and participate in ASSIP's scientific-writing and career forums along the way. (Program cost is \$25 application fee plus \$1,299 tuition; full waivers are available for Pell-eligible and reduced-lunch students.)

Every chapter, every notebook, every problem set is in service of the poster and the abstract. Keep them in view.

## Reproducibility discipline, from Day 1

Two expectations are non-negotiable.

**Code must be reproducible.** Every result you report comes from code that runs start to finish on a clean environment (`python=3.11`, libraries pinned per Appendix B) and produces exactly the number you wrote down. No "it worked on my laptop earlier." Use the pinned environment, set your random seed at the top of every notebook, and keep secrets such as API keys in environment variables, never in the notebook. Before you run your headline regression for the paper, **tag the commit `PAP-v1`** — your pre-analysis plan, frozen — so reviewers can see exactly which specifications were declared before you saw the result and which were post-hoc.

**Writing must be honest.** When you state a regression specification, you state all of it: outcome, treatment or key regressor, controls, fixed effects, clustering, sample, and the identifying assumption in one sentence. You never write that something "controls for endogeneity"; you name the specific threat and the specific design that addresses it. When a result is fragile, you show how fragile. When you cannot rule out an alternative explanation, you write that down — your poster gets stronger for the admission.

## Before Week 1: the prerequisite self-test

Your very next stop is **`03-prerequisite-self-test.md`**. It is twenty questions across single-variable calculus, basic probability and statistics, and light Python, with full worked solutions. Be honest when you grade it; this is a routing decision, not a score.

If you miss several **calculus or stats** items, start with **Appendix A: Math Toolkit** before touching Week 1. If the **Python** items tripped you, work **Appendix B** first to get your environment and `pandas` fundamentals solid. Routing through an appendix is not punishment — it is exactly what Maya does, and it is exactly what Devon skips before hitting a wall on partial derivatives in Week 2. Be Maya.

## The eight-week ladder

**Weeks 1–2** build the engine: regression mechanics and honest inference. **Weeks 3–4** confront causation: what it would take to claim one thing *caused* another, and the designs that make such a claim defensible. **Weeks 5–6** teach you to read the research frontier critically and to turn a frontier paper into a question of your own. **Weeks 7–8** turn you loose to specify, estimate, write, and ship — poster up, abstract submitted, by August 12.

Each rung depends on the one below it. You cannot reason about causation in Week 3 without trusting your inference from Week 2, and you cannot trust your inference without the mechanics from Week 1. Resist the urge to jump ahead. By Symposium Wednesday you will have done the real thing — and your fourteen pod-mates, your sub-leader, Prof. Gao, and the five fictional friends from the worked examples will all have been on the ladder with you the whole way up.
