# Model Deliverable — PS 8.4 (Referee Report + R&R Memo)

**Problem set:** `book/weeks/week-08/ps8.4.md` (PS 8.4, Week 8).
**Chapter:** Ch 8.4 — Peer Review & Revision.

PS 8.4 has no numeric answer key: it is a project deliverable, and what is graded is *judgment* — whether a report names the real threat and says what would change the referee's mind, and whether a memo concedes, defends, and bounds on the evidence. So this appendix entry is not a worked solution but a **model deliverable**: a complete, A-grade referee report (Devon on Maya's fair-lending paper) and an A-grade R&R memo excerpt (Maya answering), written exactly as strong students would submit them, followed by **instructor grading notes** that key each section to the peer-review rubric and — the part most worth reading — contrast a *constructive* report with the *destructive* one a weaker student writes about the same paper.

The running pair is the one from Ch 8.4 §5 and §8: Maya's staggered fair-lending difference-in-differences on HMDA data, with Devon wearing the referee hat. The chapter showed *abridged* versions of both documents to teach the shape; the versions below are the **full deliverables** a student would actually submit and be graded on — longer, with the minor lists complete and the memo answering all three majors. **All empirical magnitudes below are illustrative**, labeled as such, and chosen only to make the quote-change-evidence mechanics concrete; they are not real estimates from any dataset, and a student's own numbers will differ.

---

## THE MODEL DELIVERABLE, PART 1 — `referee-report.md` (Devon on Maya's paper)

> **Verdict: Major revision.**
>
> **Referee Report — "Do State Fair-Lending Examinations Narrow the Mortgage-Denial Gap?"**
>
> **Summary.** The paper asks whether state-level fair-lending examination programs reduced the gap in mortgage-denial rates between minority and white applicants. Using HMDA loan-application data aggregated to the county-year, the author estimates a staggered difference-in-differences comparing counties in adopting states to counties in not-yet- and never-adopting states, with county and year fixed effects and standard errors clustered by state. The headline result (Table 2, column 3) is that examinations narrow the denial gap by about 1.4 percentage points — roughly a fifth of the pre-period mean gap — significant at the 1% level *(illustrative magnitude)*. The question is well-posed, the institutional setup of how states adopt examination programs is clearly explained, and the design is the natural one for the question. My report below leads with the concern that most threatens the headline and works down from there; none of my major points asks the author to write a different paper.
>
> **Major points.**
>
> 1. *(Biggest concern — identification: anticipation and pre-trends.)* The entire causal claim rests on parallel trends, and I cannot currently assess it, because the paper reports no event study — only the single post-period coefficient. This is my central concern. Fair-lending examination programs are typically debated in a state legislature for a year or more before adoption, which is exactly the condition under which lenders might change behavior *in anticipation* of the coming examination, contaminating the pre-period. **What would change my mind:** an event-study plot of the denial gap with at least four pre-period leads and several post-period lags, normalized at $k=-1$. *Flat, jointly-insignificant leads would substantially reassure me; a downward pre-trend in adopting states would be close to fatal,* because it would mean the gap was already closing before the policy and the design is mislabeling a trend as an effect. As written, I cannot tell which world we are in, and the headline cannot be evaluated until I can.
>
> 2. *(Identification: the forbidden comparison.)* The design is staggered, and the methods section says "two-way fixed effects" without addressing the negative-weights problem (Ch 4.2): already-treated counties are serving as controls for later-treated ones, which biases the two-way-FE estimate when the treatment effect is dynamic — and the anticipation story in point 1 makes dynamic effects likely. **What would change my mind:** re-estimate the headline with a heterogeneity-robust estimator (Callaway–Sant'Anna against never- and not-yet-treated controls only) and report it beside the TWFE number. If the two agree, the TWFE number is safe to report as the headline; if they diverge, the robust one is the result and the paper should say so.
>
> 3. *(Specification: the denominator of the denial gap.)* The county-year denial gap is constructed from raw HMDA application counts, but the text does not say whether counties with very few minority applications are dropped, winsorized, or kept. A handful of small counties where the gap is mechanically volatile could be driving the estimate. **What would change my mind:** a robustness column weighting by application volume, and a second dropping counties below some minimum minority-application threshold. If the estimate is stable across both, the result is not a small-cell artifact and I am reassured; if it moves a lot, the headline is a composition story, not a policy effect.
>
> **Minor points.** (None of these changes my verdict; they improve the paper.)
>
> - Table 2's note does not state the significance thresholds the stars denote. Per the Appendix D convention, the note should be explicit — read-the-note, never-assume.
> - The introduction states the paper "establishes that examinations cause fairer lending." That verb is stronger than a DiD credible-conditional-on-parallel-trends can support; I would soften "establishes... cause" to "is consistent with examinations narrowing the gap," to match what the design can deliver (this is the same calibrated-verb discipline the author would have applied to their own identification memo).
> - Figure 1 has no y-axis label; I assume it is the denial gap in percentage points, but the reader should not have to guess.
> - Bertrand, Duflo & Mullainathan (2004) is the right citation for the state-level clustering choice and should appear where clustering is introduced in the text, not only in the reference list.
> - The sample-construction paragraph gives the year range but not the final county count; please report $N$ (counties and county-years) so the reader can size the panel.
>
> **Verdict (expanded). Major revision.** The question is good, the data are real, and the design is the right one for the claim; the paper is one event study and one robust-estimator column away from being convincing. I want to stress to the editor that this is a *major revision and not a reject*: the bones are sound, and every major point I raise asks the author to *defend the design they already have*, not to abandon it. If the event-study leads come back flat and the Callaway–Sant'Anna number tracks the TWFE estimate, I expect to recommend acceptance.

---

## THE MODEL DELIVERABLE, PART 2 — `rr-memo.md` (Maya answering Devon)

> **Response to Referee 1**
>
> We thank the referee for an unusually constructive report. Below we respond to each major point in turn; referee comments are in italics, our responses follow, and we have labeled each as a **concession**, a **defense**, or a **bounded threat** so the logic of each is explicit. New material is flagged in blue in the revised manuscript.
>
> **Major point 1 (anticipation / pre-trends) — bounded threat.** *"The entire causal claim rests on parallel trends, and I cannot currently assess it because the paper reports no event study... Flat, jointly-insignificant leads would substantially reassure me; a downward pre-trend would be close to fatal."*
>
> > This was the right thing to ask first, and we are glad we ran it. **What we changed:** we have added an event study as **new Figure 2** and discuss it in **Section 4.2**. **The evidence:** the four pre-period leads are individually insignificant and jointly insignificant (joint F-test p = 0.41), with no visible downward drift in the denial gap before adoption; the effect emerges in the year of examination and grows over the following two years *(illustrative figures)*. We read this as consistent with — though, as we now stress in the text, not proof of — parallel trends, and against the anticipation story. **What we did not claim:** flat leads cannot *confirm* the post-period counterfactual, only fail to refute it, so we have added a sentence to the limitations (**Section 6**) stating that anticipation remains the threat most likely to bias our estimate and noting the direction. This is the threat we bound rather than dispatch: it is real, it is partly untestable, and we have presented the strongest indirect evidence we have rather than pretending it is gone.
>
> **Major point 2 (forbidden comparison / staggered DiD) — concession.** *"The design is staggered... already-treated counties are serving as controls... I would want the headline re-estimated with a heterogeneity-robust estimator and the two numbers compared."*
>
> > The referee is correct and this was a real gap in the original submission. **What we changed:** we have re-estimated the headline using the Callaway–Sant'Anna estimator against never- and not-yet-treated controls only (**new Table 3**) and now report it beside the TWFE number. **The evidence:** the robust estimate is **−1.5 pp**, very close to the **−1.4 pp** TWFE estimate *(illustrative figures)*, which suggests the negative-weights problem is not material in our panel — consistent with effects that, while dynamic, are similarly signed across adoption cohorts. We now report both numbers and note the agreement in **Section 5.1**. We retain TWFE as the headline for comparability with the prior literature but state explicitly that the robust estimate is the one we would defend if the two diverged. We are grateful for the push; the paper is more credible for carrying both numbers.
>
> **Major point 3 (small-cell denominator) — defense.** *"A handful of small counties where the gap is mechanically volatile could be driving the estimate... a robustness column weighting by application volume, or dropping small counties, would tell us whether the result is real."*
>
> > We respectfully believe the result is not a small-cell artifact, and — as the referee suggests — we have checked this directly rather than merely asserting it. **What we changed:** **new columns 4 and 5 of Table 2** weight by application volume and drop counties below 50 minority applications per year, respectively. **The evidence:** the estimate is stable across both — **−1.3 pp** weighted and **−1.5 pp** on the trimmed sample, against the **−1.4 pp** baseline *(illustrative figures)*. We have added a sentence in **Section 5.2** reporting this and concluding the headline is not driven by mechanically volatile small counties. We note that this is a defense in which the referee's suggested test became part of the paper: we disagreed with the conclusion that small cells drive the result, but we settled the disagreement with the evidence the referee asked for rather than with argument.
>
> **Minor points.** We have made all five minor changes: Table 2's note now states the significance thresholds; the introduction's "establishes that examinations cause" is softened to "is consistent with examinations narrowing the gap"; Figure 1's y-axis is now labeled (denial gap, percentage points); Bertrand, Duflo & Mullainathan (2004) is now cited in the text where clustering is introduced; and the sample paragraph now reports the county and county-year counts.
>
> We believe the paper is substantially stronger for these additions — particularly the event study, which we should have included in the first submission — and every change described above is in the revised manuscript at the location named. We are grateful for the report.

---

## INSTRUCTOR GRADING NOTES (keyed to the peer-review rubric)

These notes show *why* this pair earns an A, where a weaker submission loses points, and — the highest-signal section for a student — what separates a **constructive** report from a **destructive** one written about the very same paper.

### Part A — The referee report (60 pts) → **Excellent**

**A1, Summary (10).** Faithful, specific, in Devon's own words; it names the design (staggered DiD, county+year FE, state clustering) and the headline magnitude, and closes by *announcing the report's own ordering* ("leads with the concern that most threatens the headline"). Maya would recognize her paper in it. *Where a typical submission loses points:* a one-line restatement of the title, or a "summary" that is really the first criticism — comprehension proof must come before judgment.

**A2, Biggest concern first (15) — the heaviest single judgment.** Devon leads with anticipation/pre-trends, which *is* the most dangerous threat to this paper, not merely the most findable one, and he names it *specifically* — anticipation contaminating the pre-period, not "endogeneity." Crucially he states the change-my-mind contract with both directions: flat leads reassure, a downward pre-trend is "close to fatal." *Where points are lost, hard:* a report that opens with the Figure 1 axis-label nit and reaches the missing event study on page two has mis-ranked its own concerns and forfeits most of A2 however correct the later points are. The single most common A2 failure is naming a *vague* threat with no falsifying evidence attached — a complaint, not a contract.

**A3, Identification menu in danger order (12).** Devon covers the DiD menu for *this* design — pre-trends (in A2), the forbidden comparison (point 2) — in descending danger, each paired with the evidence that settles it. He respects the asymmetry: point 2 asks Maya to *re-estimate her design*, not replace it, and the verdict explicitly says "every major point asks the author to defend the design they already have." *Where points are lost:* hijacking — three paragraphs on the IV Devon would have run instead. That is not refereeing.

**A4–A5, Specification then exposition (10 + 5).** The small-cell denominator question is correctly placed *below* identification (a specification point, not a design-killer), and the truly downstream items — the table note, the axis label, the citation placement, the missing $N$ — are correctly demoted to minors. The overclaiming-verb point ("establishes... cause") sits in minors because softening a sentence does not change the result, but it is flagged because it is the same calibrated-verb discipline from the author's own Week-7 memo. *Where points are lost:* letting a robustness nit or a typo crowd into the major list, which mis-signals to the author where to spend revision energy.

**A6, Major/minor, change-my-mind, verdict (8).** Two clean numbered lists; *every* major point carries the evidence that would move the referee; the verdict is on the top line, calibrated, and — the A-grade move — *expanded* to tell the editor explicitly this is "a major revision and not a reject," with the condition under which Devon expects to accept. *Where points are lost:* a major point with no falsifying evidence (incomplete contract), or a vague "promising but needs work" verdict that Ch 8.4 §3 calls the unkind one because it wastes the author's month.

**The tone gate (across A).** Every sentence is about the paper: "the methods section says two-way fixed effects without addressing the negative-weights problem," never "you forgot about negative weights." No false reassurance — the potentially-fatal pre-trend is flagged as potentially fatal. This is tough *and* kind, which is the whole norm.

### Part B — The R&R memo (40 pts) → **Excellent**

**B1, Quote-change-evidence for every major (16).** Each of the three majors is answered in the exact order: verbatim quote, then "what we changed" with a specific location (new Figure 2 / new Table 3 / new columns 4–5), then "the evidence" with a specific *number* (joint-test p = 0.41; −1.5 pp vs −1.4 pp; −1.3/−1.5 pp). *Where points are lost, near-zero for the point:* "we have addressed this" with no location and no number — unverifiable, and graded as if nothing was done.

**B2, Concede / defend / bound, one of each, labeled (15).** All three moves are present and explicitly tagged. The **concession** (point 2) is textbook: Maya agrees the gap was real, runs the requested estimator, and reports both numbers — and because they agree, the concession cost her nothing and bought credibility. The **defense** (point 3) is the cleanest kind: it *does the requested work first* (the two robustness columns) and only then states the conclusion, so the disagreement is settled by evidence, not assertion. The **bounded threat** (point 1) is the most sophisticated: flat leads are offered as the best available evidence, but Maya explicitly refuses to claim they *confirm* the counterfactual and promotes the residual into the limitations section — the fourth column of her Ch 7.5 threats table, made public. *Where points are lost:* a memo that concedes everything (weak), fights everything (weaker), or "defends" by assertion with no test run; or one that claims a clean sweep with no residual limitation, which reads as naïve.

**B3, Do-what-you-said-you-did (9).** Every change the memo names — Figure 2, Table 3, columns 4–5, the five minor fixes, the softened intro verb — is described precisely enough that a referee can verify it in the revised paper in under a minute, and the memo closes by asserting exactly that. *Where points are lost, terminally:* any memo claim the revised paper does not back up. A caught discrepancy zeroes B3 and casts doubt on the rest, mirroring how a single caught overclaim ends a referee's trust for the rest of a career. This is the load-bearing wall, and the exemplar honors it.

### Constructive vs. destructive — the same paper, two reports

The most useful thing a student can study here is the *destructive* report a weaker referee writes about Maya's identical paper, point against point:

| | **Constructive (Devon, the exemplar)** | **Destructive (what to avoid)** |
|---|---|---|
| Summary | Faithful, in own words, proves comprehension. | Skips it, or "this paper is about fair lending" — author cannot tell if the referee read it. |
| Biggest concern | Anticipation, named specifically, *with the evidence that would change his mind.* | "I have doubts about the causality" — a feeling, not a threat; nothing the author can act on. |
| Hardest point | "The identification section does not rule out anticipation." (About the paper.) | "You clearly don't understand DiD." (About the person — gets rejected for tone, so the real flaw goes unfixed.) |
| Standard errors | Cites Petersen / BDM, names the level treatment varies at. | "The stats seem off." |
| Alternative design | One sentence noting an alternative exists. | Three paragraphs on the paper the referee would rather have written — hijacking. |
| A weak design | "Reject as currently identified — the design cannot support the claim," said plainly. | "Promising but needs work" — false reassurance that wastes the author's next month. |
| Verdict | Calibrated, with the condition for acceptance stated. | Either rubber-stamps a broken design to be nice, or savages a sound one to seem rigorous. |

The pattern is the one Ch 8.4 §4 names: the destructive referee is **soft on the work and hard on the person** — exactly backwards. The constructive referee is **hard on the work and kind to the person**, attaches falsifying evidence to every hard point, and stays inside the author's project. A report can be entirely correct on the merits and still be destructive if its tone makes the author defensive, because a defensive author argues instead of fixing — which makes the paper worse and defeats the only purpose of the report.

### One-line grading heuristic

The two highest-signal questions for any PS 8.4 submission. **For the report:** does it lead with the *genuinely most dangerous* threat, named specifically, with the evidence that would change the referee's mind — and is it hard on the work while kind to the person? **For the memo:** is every major answered in quote-change-evidence shape with a real number, does it show a conscious concede/defend/bound for the three hardest, and — checked directly — does the revised paper actually contain every change the memo claims? A student who clears both has the peer-review mindset: they read tables-first and identification-first as a service to a peer, and they rebuild credibility evidence-by-evidence and honestly. This pair clears both cleanly, which is what an A looks like.

---

*End of model deliverable for PS 8.4. The pair is Devon refereeing Maya's HMDA fair-lending staggered DiD and Maya answering — the same pair worked abridged in Ch 8.4 §5 and §8, here in full deliverable form. All magnitudes are explicitly illustrative and not real estimates. Method references invoked in the report (Callaway–Sant'Anna 2021 for the heterogeneity-robust estimator; Goodman-Bacon 2021 for the negative-weights logic, built in Ch 4.2) and the clustering and inference citations (Petersen 2009; Bertrand, Duflo & Mullainathan 2004, from Week 5) are reference-only here. The referee report is the Ch 7.5 threats table written about someone else's paper; the R&R memo is the author's own threats table promoted into a public defense — the symmetry Ch 8.4 §9 closes on.*
