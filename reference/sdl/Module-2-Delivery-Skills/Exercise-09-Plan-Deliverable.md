# Exercise 9: Plan Deliverable

*Estimated time: 2–2.5 hours*
*Prerequisites: Exercise 8 complete*

---

## Goal

Apply the EDD cycle to the Plan Deliverable command. This command is where technical specificity matters most: a plan for a Node.js API looks different from a plan for a Python service. Context that encodes the implementation environment is the critical addition, and the test for whether it is load-bearing is concrete: run the same deliverable through the command with two different stack descriptions — the plans should differ in specific ways.

---

## The Starter Command

Create `plan-deliverable.md`:

```markdown
# Plan Deliverable

## Role
You are a senior practitioner who produces clear, actionable technical plans for deliverable implementation.

## Task
Given a Deliverable with Acceptance Criteria, produce a Technical Plan describing how to implement the deliverable.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

---

## Step 1: Select a Deliverable (10 minutes)

From your Workstreams and Deliverables output in Exercise 8, select one deliverable to work with. Choose a deliverable that has enough technical substance to produce an interesting plan — avoid purely administrative deliverables. A good candidate for TeamPulse would be something like the survey form submission flow, the anonymization logic, or the trend dashboard data model.

Note the deliverable and its acceptance criteria in your test file.

---

## Step 2: Write the Test File First (40 minutes)

Create `plan-deliverable-tests.md`. Commit before adding Context or Constraints.

Write at least 3 criteria. Think through:

1. **Technical specificity:** The plan should name specific technologies, libraries, or patterns from the implementation context. A plan that says "create an API endpoint" is less useful than one that says "create a POST /api/surveys endpoint using Express.js that validates the payload against a Zod schema." Write a criterion for this level of specificity.

2. **Stack-load-bearing:** Run the command with and without your Context section, using two different stack descriptions. The plans must differ in specific ways. Write a criterion that would fail for a stack-agnostic plan.

3. **Acceptance criteria traceability:** Each acceptance criterion in the deliverable should correspond to something in the plan. Write a criterion that tests this traceability.

---

## Step 3: Build and Iterate (60 minutes)

Configure `plan-deliverable-promptfoo.yaml` with Haiku as the sole provider. Baseline, then iterate.

**The stack-load-bearing test is required.** Run your plan-deliverable command with the TeamPulse stack (React, Node.js, PostgreSQL) and with an alternative stack (e.g., Python/FastAPI/SQLite). The resulting plans must differ in specific, named ways. If they do not, your Context is not load-bearing — you need to make it more specific.

Minimum: 3 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

## Step 4: Five-Stage Pipeline Check (20 minutes)

Run scope document → Architecture → UX → Workstreams & Deliverables → Plan Deliverable using your improved commands. Review the Plan Deliverable output against the original TeamPulse product description.

Trace any quality gaps back to their source: is the plan weak because the deliverable was vague (Workstreams & Deliverables problem), because the deliverable's context wasn't clear (scope document problem), or because the Plan Deliverable command itself is incomplete?

---

## Step 5: Kata Stress Test — Sorting Algorithm Visualizer (25 minutes)

Run your finalized `plan-deliverable.md` against Kata I1 (Sorting Algorithm Visualizer) from Appendix A. First run the kata description through `create-scope.md` and `decompose-to-deliverables.md` to get a deliverable, then select the deliverable for the visualization/animation subsystem and run it through `plan-deliverable.md`.

**What to watch for:** Standard recursive sorting algorithms cannot be paused mid-execution to update the UI. To animate each comparison and swap step-by-step, the implementation requires a specific structural approach: a generator function (yielding at each comparison and swap) or an equivalent step-iteration model. This is the most important architectural decision in the entire kata.

The critical test: does your Plan Deliverable command name this requirement — generator functions, a step queue, or equivalent — or does it produce a plan that says "implement the sorting algorithm and display it"? A plan that does not address how to make execution pauseable and resumeable is not actionable for this kata.

Record your findings:

```
## Kata Stress Test — Sorting Algorithm Visualizer — [date]
Plan Deliverable output (key findings):
- Did the plan name a step-through execution model (generators or equivalent)? [Yes/No]
- Did the plan address animation pacing and the multi-algorithm simultaneous display? [Yes/No]
- Other notable failures or successes: [describe]
Root cause if failed: [Context gap / Constraints gap / Upstream quality]
Action taken: [hypothesis + change made, if any]
```

---

## Step 6: Checkpoint

**If you cannot close a gap after 3 iterations, document it as accepted with reasoning and move on.** Not every gap can be closed generically — the log of what you accepted and why is as valuable as what you fixed. (15 minutes)

```
## Checkpoint — plan-deliverable.md — [date]
Haiku score:  X/Y

Gaps closed this exercise: [list]
Gaps accepted (with reasoning): [list]
```

---

## Step 7: Commit

Commit `plan-deliverable.md`, `plan-deliverable-tests.md`, `plan-deliverable-promptfoo.yaml`, sample plans for both stack variations, kata stress test notes, and your pipeline check notes.

---

## Self-Check

- [ ] `plan-deliverable-tests.md` committed before Context or Constraints added
- [ ] Stack-load-bearing test completed and documented (same deliverable, two different stacks, specific differences noted)
- [ ] Minimum 3 Promptfoo runs with hypotheses
- [ ] Load-bearing audit completed
- [ ] Five-stage pipeline check documented
- [ ] Kata stress test (Sorting Algorithm Visualizer) completed and documented
- [ ] Model Ladder checkpoint recorded
