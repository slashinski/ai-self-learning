# Exercise 8: Create Workstreams and Deliverables

*Estimated time: 2–2.5 hours*
*Prerequisites: Exercises 5–7 complete*

---

## Goal

Apply the EDD cycle to the Workstreams and Deliverables command. This command takes three upstream outputs (scope document, Architecture, UX) as input — which means upstream quality matters more here than anywhere else in the pipeline. The exercises also surface the most common failure modes in deliverable decomposition: deliverables that are too large, acceptance criteria that are untestable, and deliverables that duplicate each other.

---

## The Starter Command

Create `decompose-to-deliverables.md`:

```markdown
# Decompose to Deliverables

## Role
You are an experienced Product Manager who writes precise, developer-ready workstreams and deliverables.

## Task
Given a scope document, Architecture Document, and UX Specification, produce a structured breakdown of Workstreams and Deliverables that fully cover the described feature or system.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

---

## Step 1: Write the Test File First (45 minutes)

Create `decompose-to-deliverables-tests.md`. Commit before adding Context or Constraints.

Before writing criteria, think through the most common ways deliverable decomposition fails:

- **Deliverables that are too large:** A deliverable that takes more than one sprint to implement is too large. How do you write a criterion for this without knowing the team's sprint velocity? Think about what signals "too large" without relying on sprint-specific context.

- **Acceptance criteria that are not testable:** "The system should be performant" is not testable. "The survey form submits in under 2 seconds on a 4G connection" is testable. Write a criterion that distinguishes these.

- **Deliverables that omit dependencies:** If Deliverable B requires work from Deliverable A, that dependency must be explicit. Write a criterion for this.

- **Deliverables that duplicate work:** Two deliverables that describe the same implementation work from different angles. How would you write a criterion that a rubric evaluator could apply?

- **Incomplete coverage:** The workstreams and deliverables should cover the full scope of the scope document. How do you test coverage without manually checking every feature?

Write at least 4 criteria covering these failure modes. Commit the test file.

---

## Step 2: Build and Iterate (60 minutes)

Configure `decompose-to-deliverables-promptfoo.yaml` with Haiku as the sole provider. Baseline, then iterate.

**Context guidance:** The Context section for this command should describe how to interpret and prioritize information from the three upstream documents when they conflict or are incomplete. What should the model do when the scope document says one thing and the Architecture document implies something different? What should it do when the UX spec describes a flow that was not mentioned in the scope document?

Minimum: 3 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

## Step 3: Upstream Quality Experiment (20 minutes)

Run `decompose-to-deliverables.md` twice:

1. With your finalized scope document + Architecture + UX from Exercises 5–7 (high-quality upstream input)
2. With the starter RT-only outputs from those commands (low-quality upstream input)

Compare the resulting Workstreams and Deliverables. Document what changes when upstream quality improves:

```markdown
## Upstream Quality Impact on Workstreams and Deliverables
High-quality upstream → [specific improvements in deliverable quality]
Low-quality upstream → [specific gaps or failure modes in deliverables]
Root cause analysis: [which upstream command had the most impact?]
```

This is the upstream quality dependency documentation for your Module 2 deliverables.

---

## Step 4: Kata Stress Test — Snake with Replay System (20 minutes)

Run your finalized `decompose-to-deliverables.md` against Kata B2 (Snake with Replay System) from Appendix A. Use the full kata description as your product description input (you will need to first run it through `create-scope.md` and `create-architecture.md` to produce upstream inputs, or use the kata description directly if your command can accept it).

**What to watch for:** The ghost snake feature — replaying a prior game while simultaneously playing a new game — is where deliverable decomposition most commonly fails for this kata. It is stated in the challenge description but is easy to underspecify at the deliverable level.

The critical test: does your command produce a deliverable for the ghost snake that includes acceptance criteria specific enough to implement without asking follow-up questions? The criteria should address: does the ghost snake share the same grid? Is it visually distinct? Does it affect the live game? What happens if no prior game exists? A deliverable that says "implement ghost snake replay" as a single acceptance criterion is failing this kata.

Record your findings:

```
## Kata Stress Test — Snake with Replay System — [date]
Workstreams and Deliverables output (key findings):
- Did a dedicated ghost snake deliverable exist? [Yes/No]
- Were the ghost snake acceptance criteria specific enough to implement? [Yes/No]
- Did the deliverables correctly decompose replay recording as a separate deliverable from replay playback? [Yes/No]
Root cause if failed: [Context gap / Constraints gap / Upstream quality]
Action taken: [hypothesis + change made, if any]
```

---

## Step 5: Checkpoint (15 minutes)

```
## Checkpoint — decompose-to-deliverables.md — [date]
Haiku score:  X/Y

Gaps closed this exercise: [list]
Gaps accepted (with reasoning): [list]
```

---

## Step 6: Commit

Commit `decompose-to-deliverables.md`, `decompose-to-deliverables-tests.md`, `decompose-to-deliverables-promptfoo.yaml`, both Workstreams and Deliverables outputs (high- and low-quality upstream comparison), and kata stress test notes.

---

## Self-Check

- [ ] `decompose-to-deliverables-tests.md` committed before Context or Constraints added
- [ ] Test criteria cover testability, size, dependencies, and coverage
- [ ] Minimum 3 Promptfoo runs with hypotheses
- [ ] Load-bearing audit completed
- [ ] Upstream quality comparison committed with root cause analysis
- [ ] Kata stress test (Snake with Replay) completed and documented
- [ ] Model Ladder checkpoint recorded
