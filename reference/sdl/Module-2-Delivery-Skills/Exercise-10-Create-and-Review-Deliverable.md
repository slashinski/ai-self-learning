# Exercise 10: Create Deliverable and Review Deliverable

*Estimated time: 4–5 hours*
*Prerequisites: Exercise 9 complete*

---

## Goal

Apply the EDD cycle to both the Implement Deliverable and Review Deliverable commands. These are the most context-heavy commands in the pipeline — the quality of their output depends almost entirely on how well the prior commands have defined the deliverable, the acceptance criteria, and the plan. This exercise surfaces a critical insight: adding Constraints to downstream commands often helps less than improving upstream quality.

---

## The Starter Commands

Create `create-deliverable.md`:

```markdown
# Create Deliverable

## Role
You are a senior practitioner who produces clean, tested, production-quality artifacts.

## Task
Given a Deliverable, its Acceptance Criteria, and a Technical Plan, implement the deliverable by producing the required artifacts and tests.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

Create `review-deliverable.md`:

```markdown
# Review Deliverable

## Role
You are a senior practitioner conducting a rigorous deliverable review.

## Task
Given a Deliverable with Acceptance Criteria and an implementation, review the deliverable and produce a structured review report.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

---

## Step 1: Write the Test Files First (45 minutes)

Create `create-deliverable-tests.md` and `review-deliverable-tests.md`. Commit both before adding any Context or Constraints.

**For Create Deliverable, write criteria for:**
- Code quality: what makes the implementation production-quality for the TeamPulse stack? (Think: TypeScript types, error handling at API boundaries, tested behavior)
- Test coverage: what must be tested? (At minimum: the happy path and at least one error path per acceptance criterion)
- Stack alignment: the implementation should use the specified stack's conventions, not generic patterns

**For Review Deliverable, write criteria for:**
- Review structure: what must a review report contain? (At minimum: pass/fail per acceptance criterion, specific issues with file/line references, a clear overall verdict)
- Specificity: the review must cite specific code, not general observations like "error handling could be improved"
- Acceptance criteria traceability: every acceptance criterion must be explicitly addressed in the review

---

## Step 2: Build and Iterate — Implement Deliverable (50 minutes)

Configure `create-deliverable-promptfoo.yaml` with Haiku as the sole provider. Use the deliverable and plan you produced in Exercise 9 as your test input.

**The key insight for this command:** if deliverable quality is low after adding Constraints, check whether the issue is actually in the upstream plan. A well-specified plan produces better implementation than adding implementation Constraints to a poorly-specified plan. Document any cases where you found this to be true.

Minimum: 3 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

---

### Session Break Point

If you are completing this exercise across two sessions, this is the natural stopping point. Steps 1–2 built and iterated the Create Deliverable skill. Steps 3–7 build and iterate the Review Deliverable skill. Pick up from here in your next session.

---

## Step 3: Build and Iterate — Review Deliverable (50 minutes)

Configure `review-deliverable-promptfoo.yaml` with Haiku as the sole provider. Use the deliverable output from Step 2 as your test input.

Note: the quality of the Review Deliverable output is particularly sensitive to the quality of the deliverable's acceptance criteria. If the criteria are vague, the review cannot be specific. If you find the review is too generic, check whether the issue is in the Review Deliverable command or in the Workstreams and Deliverables output that defined the acceptance criteria.

Minimum: 3 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

## Step 4: The Upstream Quality Reflection (20 minutes)

Write a brief note in `create-deliverable-tests.md`:

```markdown
## Upstream Quality Reflection

What I found when trying to improve Implement Deliverable quality:
- Adding Constraints to Implement Deliverable helped with: [specific things]
- Adding Constraints to Implement Deliverable did NOT help with: [specific things]
- The real fix for those failures was: [which upstream command needed improvement]

Conclusion: [Your hypothesis about where in the pipeline the most leverage is for improving deliverable quality]
```

This reflection is a key deliverable — it demonstrates the ability to diagnose pipeline quality rather than just adding Constraints to the most downstream visible failure.

---

## Step 5: Kata Stress Test — Sorting Algorithm Visualizer (20 minutes)

Using the same Sorting Algorithm Visualizer kata (I1) from Exercise 9, run the plan you produced for the visualization/animation deliverable through `create-deliverable.md` and `review-deliverable.md`.

**For Create Deliverable, watch for:** Does the implementation use a generator function or step-queue model that can pause and resume mid-sort? Or does it produce a standard recursive sort that runs to completion and only then updates the UI? The latter will not work for visualization and would need complete restructuring. A plan that named generators should produce an implementation that uses them — if it does not, that is a failure of the Implement Deliverable command to follow the plan.

**For Review Deliverable, watch for:** Does the review catch the absence of the step-through execution model if the implementation gets it wrong? Or does it focus on surface-level concerns (naming, formatting) while missing the fundamental architectural issue?

Record your findings for both commands:

```
## Kata Stress Test — Sorting Algorithm Visualizer — [date]
Implement Deliverable:
- Did it produce pauseable step-through execution? [Yes/No]
- Did it follow the plan from Exercise 9? [Yes/No]
- Notable failures: [describe]

Review Deliverable:
- Did it catch architectural issues (missing step-through model)? [Yes/No]
- Did it cite specific code issues? [Yes/No]
- Notable failures: [describe]

Action taken for each command: [hypothesis + change made, if any]
```

---

## Step 6: Checkpoint

**If you cannot close a gap after 3 iterations, document it as accepted with reasoning and move on.** Not every gap can be closed generically — the log of what you accepted and why is as valuable as what you fixed.s (15 minutes)

Record a Model Ladder checkpoint for each command:

```
## Checkpoint — create-deliverable.md — [date]
Haiku: X/Y
Gaps closed: [list] | Gaps accepted: [list with reasoning]

## Checkpoint — review-deliverable.md — [date]
Haiku: X/Y
Gaps closed: [list] | Gaps accepted: [list with reasoning]
```

---

## Step 7: Commit

Commit both command files, both test files, both Promptfoo configurations, the upstream quality reflection, and kata stress test notes.

---

## Self-Check

- [ ] Both test files committed before any Context or Constraints added
- [ ] Review criteria include acceptance criteria traceability for both commands
- [ ] Minimum 3 Promptfoo runs per command with hypotheses
- [ ] Load-bearing audit completed for both commands
- [ ] Upstream quality reflection committed with a specific conclusion
- [ ] Kata stress test (Sorting Algorithm Visualizer) completed for both commands
- [ ] Model Ladder checkpoints recorded for both commands
