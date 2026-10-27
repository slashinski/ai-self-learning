# Exercise 21: End-to-End Success Rate

*Estimated time: 2–3 hours*
*Prerequisites: Exercises 18–20 complete*

---

## Goal

Run your full 7-step delivery pipeline 10 times against 10 different product descriptions. Grade each final output against the original requirements. Calculate your composite end-to-end success rate. Trace every failure back to its originating step. Write a report that answers one question: when I hand this pipeline a product description it has never seen, what percentage of the time does it produce a deliverable I would ship?

This is the number that Stage 4 certification requires. Not per-step accuracy — the composite. If you do not know your end-to-end number, you have not reached Stage 4.

---

## Background: Why Per-Step Accuracy Lies

You have been measuring per-step quality since Module 2. Each delivery skill has a Promptfoo configuration with assertions. You know what score `create-scope` gets, what `create-architecture` gets, what `review-deliverable` gets. Those numbers are real and useful — for improving individual skills.

But they do not tell you what happens when those skills run in sequence. And that is the only thing your client cares about.

Here is the math that makes this exercise necessary. A 7-step pipeline compounds error:

| Per-step accuracy | Composite (0.95^7) | What it means |
|---|---|---|
| 95% | ~70% | 3 in 10 runs fail somewhere |
| 90% | ~48% | Fewer than half succeed end-to-end |
| 85% | ~32% | Two-thirds of runs fail |

If every step is 95% accurate — which sounds excellent — your pipeline still fails 30% of the time. At 90% per-step, you are below a coin flip. At 85%, you fail two times out of three.

This is why Stage 4 does not accept per-step scores as evidence. A reviewer who sees seven Promptfoo configs each scoring 90% and asks "what is your end-to-end success rate?" is not being pedantic — they are asking the only question that matters. Per-step scores measure your skills in isolation. The composite measures your workflow in reality.

The compounding is mathematical, not optional. Every step depends on the output of the previous step. If step 3 produces a flawed architecture document, step 4 builds a flawed decomposition on top of it, step 5 plans a flawed deliverable, and step 6 implements the flawed plan. The error propagates. A step that is 95% accurate in isolation may be 95% accurate given clean input — but given degraded input from an upstream failure, its accuracy drops. The composite captures this. Per-step scores do not.

---

## Step 1: Select 10 Product Descriptions (15 minutes)

You need 10 inputs that your pipeline has never seen. Do not reuse product descriptions from Module 2 (DevLog, Blackjack) or any kata you already ran against during skill development. The whole point is to measure generalization — if you run against inputs you trained on, you are measuring recall, not capability.

Sources for your 10 inputs:

- **Katas from Appendix A.** The [Katas-Intermediate.md](../Appendix-A-Development-Katas/Katas-Intermediate.md), [Katas-Advanced.md](../Appendix-A-Development-Katas/Katas-Advanced.md), and [Katas-Expert.md](../Appendix-A-Development-Katas/Katas-Expert.md) files contain product descriptions you likely have not used. Pick katas that span different domains — a game, a developer tool, a data product, a workflow system. Domain diversity exposes different failure modes.
- **Your own work products.** If you have real product descriptions from client work or personal projects, use them. These are the best test because they represent the inputs your pipeline will actually face.
- **A mix.** Some katas, some real work. This is the most realistic distribution.

Write down all 10 product descriptions in a single file: `pipeline-inputs.md`. Number them 1–10. For each, include the product description and the source (which kata, or which real project).

Do not cherry-pick easy inputs. If your pipeline fails on hard inputs, that is the finding. Selecting only inputs you know it will pass defeats the purpose.

---

## Step 2: Run the Pipeline 10 Times (60–90 minutes)

Run your harness (from Exercise 18) against each of the 10 product descriptions. Your harness should execute all 7 steps end-to-end with guardrails firing between steps. If you have punch-out points (Exercise 20), let them fire — but do not manually intervene unless the harness halts and requires you to.

For each run, record:

1. **Run number** (1–10)
2. **Input** (product description name/identifier)
3. **Did the pipeline complete?** (yes/no — did all 7 steps execute without halting?)
4. **Time to complete** (rough — minutes)
5. **Any guardrail fires** (which step, which guardrail, was it a halt or a warning?)

If a guardrail halts the pipeline mid-run, that run is a failure for the purpose of end-to-end success rate. Record it, note which step halted, and move to the next input. Do not fix the input and re-run — that is iterating on the input, not measuring the pipeline. You are measuring what happens when real inputs hit your workflow. Fixing inputs to make them pass is not measurement; it is coaching the test.

Save all pipeline output files. You will need them for failure tracing in Step 4. Use a directory structure like:

```
runs/
  run-01-<input-name>/
    scope.md
    architecture.md
    ux.md
    workstreams-deliverables.md
    plan.md
    deliverable.md
    review.md
  run-02-<input-name>/
    ...
```

---

## Step 3: Grade Each Final Output (30–45 minutes)

For each of the 10 runs, grade the final output — the `review.md` from step 7, plus the `deliverable.md` from step 6 — against the original requirements from the product description. This is not per-step grading. This is end-to-end grading: did the pipeline produce a deliverable that satisfies what the product description asked for?

Use this grading rubric for each run:

- **Pass:** The final deliverable addresses all stated requirements. The review step caught any significant issues. The output is something you would hand to a client or teammate without apology.
- **Partial:** The deliverable addresses most requirements but has a notable gap — a missing feature, a misunderstood constraint, an architectural decision that does not fit the product description. The review step either missed the gap or flagged it but the pipeline did not correct it.
- **Fail:** The deliverable does not meet the requirements. Either the pipeline halted at a guardrail and did not complete, or it completed but the output is fundamentally wrong — wrong scope, wrong architecture, wrong decomposition, wrong implementation.

A "partial" is not a pass. The composite success rate counts only full passes. This is deliberate. A deliverable with a notable gap is not something you ship. If you would not hand it to a client without fixing it first, it is not a pass.

Record your grades in a table:

| Run | Input | Completed? | Grade | Notes |
|---|---|---|---|---|
| 1 | [name] | Yes | Pass/Partial/Fail | [brief] |
| 2 | [name] | Yes | ... | ... |
| ... | | | | |
| 10 | [name] | | | |

Be honest. The temptation to round a partial up to a pass is strong, especially after you have spent hours running the pipeline. Resist it. A partial that you call a pass is a lie that your Stage 4 reviewer will catch when they read the output file.

---

## Step 4: Trace Failures to Origin (30–45 minutes)

For every run that graded Partial or Fail, trace the failure back to the step where it originated. This is the same upstream dependency tracing you did in Module 2 (Exercise 11), but now across 10 runs and with the benefit of your harness logs.

For each failure, answer:

1. **Which step produced the first error?** Not which step you noticed the error in — which step introduced it. A flawed architecture document (step 2) that leads to a flawed decomposition (step 4) that leads to a flawed plan (step 5) that leads to a flawed deliverable (step 6) originated at step 2. Trace to the root.
2. **What was the error?** Describe it concretely. "Architecture chose a monolith when the product description clearly called for event-driven microservices" is useful. "Architecture was wrong" is not.
3. **Did any guardrail catch it?** If a guardrail fired and halted the pipeline, the guardrail worked. If the error propagated through to the final deliverable without any guardrail catching it, that is a guardrail gap — record it.
4. **Was the error an input issue or a skill issue?** Did the product description lack information the skill needed (input issue), or did the skill fail to use information that was present (skill issue)? This distinction tells you whether to fix your inputs or fix your skills.

Record your tracing in a section of your report:

```markdown
## Failure Tracing

### Run 3 — [input name] — Fail
**Origin step:** Step 2 (create-architecture)
**Error:** [concrete description]
**Guardrail caught?** No — the architecture guardrail checked for completeness but not for architectural fit to the product description's constraints
**Root cause:** Skill issue — the architecture skill did not carry forward a constraint from the scope document
**Action:** [what you would change — a skill, a guardrail, or a sentinel schema]
```

Patterns matter more than individual failures. If 4 of your 6 failures originate at step 2, your architecture skill is your bottleneck. If 3 failures originate at step 4 and all involve the same type of error (e.g., missing a deliverable), your decomposition skill has a specific gap. Look for the pattern, not just the individual traces.

---

## Step 5: Calculate Your Composite Success Rate (10 minutes)

Count your full passes. Divide by 10. That is your end-to-end success rate.

```
End-to-end success rate = (number of Pass grades) / 10 × 100%
```

Example: 6 passes out of 10 runs = 60% end-to-end success rate.

Now compare this to what your per-step scores predicted. If your Promptfoo configs show an average per-step accuracy of 90%, the compounding math predicted ~48% end-to-end success. Your actual number may be higher (your guardrails catch some errors before they propagate) or lower (upstream quality degradation makes downstream steps worse than their isolated scores suggest).

Record both numbers:

- **Average per-step accuracy** (from your Promptfoo configs — average across all 7 skills)
- **Predicted composite** (per-step accuracy ^ 7)
- **Actual composite** (from this exercise)

The gap between predicted and actual is your guardrails' contribution. If your per-step average is 88% (predicted composite ~36%) but your actual composite is 55%, your guardrails are catching and correcting failures that would otherwise propagate. That is measurable value from the governance layer you built in Exercises 14 and 19.

If your actual composite is lower than your predicted composite, something is wrong — either your per-step scores are inflated (your Promptfoo assertions are too permissive, which Exercise 16 warned about), or upstream quality degradation is causing cascading failures that isolated testing does not capture. Both are findings worth recording.

---

## Step 6: Write the End-to-End Success Rate Report (30 minutes)

Write `end-to-end-success-rate-report.md`. This is a Stage 4 certification artifact. Structure it as follows:

```markdown
# End-to-End Success Rate Report — [date]

## Methodology
- Pipeline: 7-step delivery pipeline (create-scope → create-architecture → create-ux → decompose-to-deliverables → plan-deliverable → create-deliverable → review-deliverable)
- Harness: [describe your harness from Exercise 18 — shell script, tool used, guardrails active]
- Inputs: 10 product descriptions from [sources — katas, real work, mix]
- Grading: Pass/Partial/Fail against original product description requirements. Only Pass counts toward the composite.

## Results Summary

| Run | Input | Completed? | Grade | Origin Step (if failure) |
|---|---|---|---|---|
| 1 | [name] | Yes/No | Pass/Partial/Fail | [step or N/A] |
| 2 | [name] | | | |
| ... | | | | |
| 10 | [name] | | | |

## Composite Success Rate
- **Full passes:** [N] / 10
- **End-to-end success rate:** [N]0%
- **Average per-step accuracy (from Promptfoo):** [N]%
- **Predicted composite (per-step^7):** [N]%
- **Actual vs. predicted:** [above/below/at — and why]

## Failure Analysis

### Failures by Origin Step
| Step | Failures Originating Here |
|---|---|
| 1. create-scope | [N] |
| 2. create-architecture | [N] |
| 3. create-ux | [N] |
| 4. decompose-to-deliverables | [N] |
| 5. plan-deliverable | [N] |
| 6. create-deliverable | [N] |
| 7. review-deliverable | [N] |

### Failure Details
[For each Partial/Fail run: origin step, error description, guardrail caught? (Y/N), root cause (input/skill), recommended action]

## Guardrail Effectiveness
- Guardrails fired: [N] times across 10 runs
- Guardrails caught failures that would have propagated: [N] times
- Guardrails missed failures that propagated to final output: [N] times
- Guardrail gaps identified: [list]

## Patterns and Insights
[2–3 paragraphs: What is the dominant failure mode? Which step is the bottleneck? Are failures input issues or skill issues? What would move the composite number up?]

## What I Would Change
[Specific, actionable changes — which skill to improve, which guardrail to add, which sentinel property to check. Not "do better next time" — name the file and the change.]
```

---

## Step 7: Commit (5 minutes)

Commit the following to your repository:

- `pipeline-inputs.md` — the 10 product descriptions
- `runs/` directory — all 10 runs' output files
- `end-to-end-success-rate-report.md` — the full report

Your commit message should include the composite number: `Exercise 21: end-to-end success rate report — [N]0% composite across 10 runs`.

---

## What This Number Means

Your end-to-end success rate is not a grade. It is a measurement. A 60% composite is not a D — it is a number that tells you where your workflow stands and what to improve. A 40% composite with honest failure tracing is more valuable for Stage 4 than an 80% composite with no tracing and generous grading.

The number matters because it is the first time in this program you are measuring the workflow, not the skills. Your Promptfoo scores told you how good each skill is in isolation. This exercise tells you how good the workflow is in reality. Those are different questions, and Stage 4 certification asks the second one.

If your composite is below 50%, that is normal for a first measurement. The compounding math is brutal. The path to improvement is: trace your dominant failure origin, improve that skill or add a guardrail at that step, re-run the 10 inputs, and see if the composite moves. That iteration loop — measure, trace, fix, re-measure — is what Stage 4 operators do. They do not guess what to improve. They measure what fails and fix that.

If your composite is above 70%, scrutinize your grading. Are your "pass" grades honest? Would you hand each pass output to a client without edits? If not, it is a partial, not a pass. The most common certification finding for this exercise is generous self-grading — passes that are actually partials. A reviewer reads your output files. If they see a "pass" with an obvious gap, the whole report loses credibility.

---

## Self-Check

Before you commit, verify:

- [ ] 10 pipeline runs completed (or halted and recorded) against 10 different, unseen inputs
- [ ] Each final output graded Pass/Partial/Fail against original requirements
- [ ] Composite success rate calculated (passes / 10)
- [ ] Per-step accuracy and predicted composite recorded alongside actual composite
- [ ] Every Partial and Fail traced to its origin step with concrete error description
- [ ] Guardrail effectiveness assessed (caught vs. missed)
- [ ] At least one pattern identified across failures (dominant origin step, input vs. skill issue)
- [ ] Specific improvement actions named (which file, which change)
- [ ] `end-to-end-success-rate-report.md` written and committed
- [ ] `pipeline-inputs.md` committed
- [ ] All 10 runs' output files committed in `runs/` directory
- [ ] You can answer this question without looking at your notes: "What is your end-to-end success rate, and which step causes most of your failures?"

If you cannot answer that last question from memory, you have not internalized your own workflow's performance. Read your report again until you can.