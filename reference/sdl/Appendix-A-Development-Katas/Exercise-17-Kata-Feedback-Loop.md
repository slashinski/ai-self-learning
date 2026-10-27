# Exercise 17: The Kata Feedback Loop

*Read this before running any kata. This is the methodology that makes the practice work.*

---

## Overview

Every kata in this module follows the same process. Read it once, understand it completely, then apply it to all 14 katas without deviation. The process is the exercise — the kata is just the input that drives it.

---

## Step 1: Set Up Your Kata Workspace (10 minutes)

For each kata, create a directory in your repository named after the kata (e.g., `katas/sorting-algorithm-visualizer/`). This is where all pipeline outputs for this kata will live.

In that directory, create a `kata-run-log.md` file. This is your iteration record for this kata:

```markdown
# [Kata Name] — Run Log

## Run 1 — [date]
Start time: [time]
End time: [time]

### Pipeline Output Quality
[Fill in after the run]

### Implementation Quality
[Fill in after the run]

### Pipeline Failures Identified
[Fill in after the run]

### EDD Actions Taken
[Fill in after the run]

---

## Run 2 — [date]
...
```

---

## Step 2: Run the Full Delivery Pipeline (45–75 minutes depending on kata complexity)

Take the kata description from the relevant kata reference file and treat it as your Feature and System Request. Run your commands in sequence:

**scope document:** Paste the kata description (challenge, key challenges, and any stretch goals you are targeting) into `create-scope.md`. Save the output as `scope.md` in your kata directory.

**Architecture:** Run `create-architecture.md` against `scope.md`. Save as `architecture.md`. Pay particular attention to: does the architecture correctly identify the computationally interesting parts of this kata? A kata with an algorithm challenge should produce an architecture that explicitly names the data structures and algorithm choices. If it produces a generic "frontend/backend/database" architecture, that is a failure — note it.

**UX:** Run `create-ux.md` against `scope.md`. Save as `ux.md`. Does the UX spec correctly reflect the real-time, interactive nature of most katas? Does it address the specific interaction model (canvas-based, grid-based, form-based)?

**Workstreams and Deliverables:** Run `decompose-to-deliverables.md` against all three upstream outputs. Save as `workstreams-deliverables.md`. Evaluate: are the deliverables at the right granularity for a single-session build? Kata deliverables should be fine-grained enough to build incrementally.

**Plan Deliverable:** Select the single most technically interesting deliverable from the workstreams (usually the core algorithm or simulation deliverable). Run `plan-deliverable.md`. Save as `plan.md`. This plan should give you a specific starting point for implementation — not "implement the sorting algorithm" but a concrete approach with named steps.

**Implement Deliverable:** Run `create-deliverable.md` using the selected deliverable and its plan. Save as `implementation.md`.

**Review Deliverable:** Run `review-deliverable.md` against the deliverable and implementation. Save as `review.md`.

---

## Step 3: Build the Kata (variable — Beginner/Intermediate: 20–60 minutes. Advanced/Expert: 60–180 minutes)

Using your pipeline outputs as context and starting points, build the kata. Your AI tool should be running with the plan and implementation as context. The goal is not to use the AI-generated implementation verbatim — it is to use the pipeline outputs to orient and accelerate the build.

Time this step. Record start and end time in your run log.

Track: which pipeline outputs did you actually use? Which did you ignore? When did you find yourself working around the pipeline output rather than with it? Those are the signal.

---

## Step 4: Evaluate the Pipeline (20 minutes)

Do not evaluate the kata implementation first. Evaluate the pipeline outputs first. Go through each command's output and grade it against the kata's stated requirements:

**scope document quality check:**
- Did it capture the key challenge correctly (not just the surface description)?
- Did it include the implied non-functional requirements (real-time updates, responsive layout, performance at scale for the given data size)?
- Did it correctly scope the stretch goals — as optional, not required?

**Architecture quality check:**
- Did it name the right algorithmic approach? (For a sorting visualizer, did it name specific sorting algorithms? For a pathfinding explorer, did it name A* and Dijkstra's specifically?)
- Did it address the rendering and animation requirements?
- Did it avoid a generic three-tier architecture when the kata needed something different?

**Workstreams and Deliverables quality check:**
- Were the deliverables independently implementable?
- Did any deliverables turn out to be too large to complete in a single focused session?
- Were acceptance criteria testable?

**Plan quality check:**
- Did the plan give you a specific starting point or a generic outline?
- Did it reflect the tech stack you actually used?
- Were the steps sequential and each one building on the last?

For each failure, write in your run log:
- What specifically failed (be precise — not "the architecture was weak" but "the architecture did not name a data structure for the priority queue in the A* implementation")
- Whether it is a Context problem or a Constraints problem
- Whether it is an upstream quality problem (the Architecture was weak because the scope document was generic)

---

## Step 5: EDD Update — One Command, One Hypothesis (20–30 minutes)

Pick the single most impactful pipeline failure from Step 4. Form a hypothesis:

> "The [command] failed to [specific thing] because the prompt does not [specific missing element]. I predict that adding [specific change] to the [Context / Constraints] section will cause [specific improvement] on the next kata run."

Make exactly one change. Run Promptfoo on that command using the kata's scope document output as a test case, **against Haiku only**. Record the before/after score.

**The generic discipline:** Before making the change, ask — would this improvement also help the next kata that is technically different from this one? If the improvement is specific to this kata's domain (e.g., "always mention Monte Carlo simulation"), it is not ready. Rewrite it so it applies to any kata with probabilistic or simulation requirements. If you cannot write it generically, either the insight is too narrow to be a command improvement, or you have not yet identified the real root cause.

**The checkpoint:** After your change, look at how the Haiku score moved.

- If the score improved: your change made the prompt clearer. The instruction was ambiguous before; now it is explicit.
- If the score did not improve: your hypothesis was wrong. Try one alternative hypothesis. If that also fails, log the failure in your cross-kata log, note it as an open issue, and move to the next kata. Not every pipeline failure has a clean fix — the log is still valuable evidence.
- If the score improved but a different assertion now fails: your change had an unintended side effect. Add a Promptfoo test case that catches it.

Record the before/after Haiku score in your `kata-feedback-log.md`. You are running against Haiku only — the two-model Model Ladder comparison was a Module 1 exercise and is not repeated here. You can monitor your AI usage at [usage.improving.ai](https://usage.improving.ai).

---

## Step 6: Second Run (same kata, updated command)

Run the kata a second time with the updated command. Time the full pipeline run plus the build. Compare to Run 1:

- Did the specific failure from Step 4 improve?
- Did any new failures appear that the first run did not expose?
- Is your total time from kata description to working implementation shorter?

If the specific failure did not improve: your hypothesis was wrong. Revisit Step 4's root cause analysis before moving to the next kata.

If you introduced a new failure: your command change had an unintended side effect. Diagnose it, add a Promptfoo test case that catches it, and fix it.

---

## Step 7: The Cross-Kata Log

After completing both runs of a kata, update `kata-feedback-log.md` in the root of your kata directory:

```markdown
## [Kata Name] — Summary — [date]

**Pipeline failures identified:** [list]
**Root cause for primary failure:** [Context / Constraints / Upstream quality]
**Command updated:** [which command]
**Change made:** [the specific change, written generically]
**Promptfoo score delta (Haiku):** [before → after]
**Interpretation:** [What did the change tell you about prompt clarity?]
**Time delta (Run 1 → Run 2):** [first run time → second run time]
**Generic applicability confirmed:** Yes / No — [explanation]
```

This log is the evidence that your practice is compounding. By kata 10, you should be able to look back at kata 1's failures and see that most of them are now caught by your Promptfoo test suite.

---

## What to Watch For Across All Katas

**The algorithm gap:** Most katas have a technically interesting algorithm at the center. Your pipeline skills may default to describing a generic deliverable approach without naming the right data structure or algorithm. This is a consistent failure mode — Context about the expected technical depth of deliverable plans is usually the fix.

**The rendering gap:** Many katas involve animation, canvas rendering, or real-time updates. These are domain-specific requirements that a generic scope document or Architecture command may not surface correctly. If your Architecture consistently omits rendering strategy, that is a Constraints problem.

**The scope creep gap:** Katas have explicit core challenges and optional stretch goals. Your scope document command may include stretch goals in the core scope if the prompt does not distinguish them clearly. This makes the Workstreams and Deliverables too large. A Constraints addition about explicit scope boundaries is usually the fix.

**The specificity gap:** Plans that say "implement the algorithm" without naming the algorithm, architectures that say "use appropriate data structures" without naming them, and acceptance criteria that say "the output should be correct" — these are all the same failure mode: the command is not producing specific enough output to be useful. Context about the expected level of technical specificity is usually the fix here, and it must be written generically enough to apply to all katas.
