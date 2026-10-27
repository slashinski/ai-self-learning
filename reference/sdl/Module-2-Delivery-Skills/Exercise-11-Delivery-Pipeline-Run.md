# Exercise 11: Full Delivery Pipeline Run and Module 2 Wrap

*Estimated time: 4.5–5.5 hours*
*Prerequisites: Exercises 5–10 complete*

---

## Goal

Run two complete delivery pipeline passes. If time-constrained, prioritize Run 1 (DevLog). The Blackjack run can be completed in a follow-up session. using product descriptions you have not iterated against: DevLog (a software product) and Kata I2 (Blackjack with Strategy Coach). Do not change any command during either run. The goal is to measure how well your commands generalize — and to stress-test them against a domain that exposes different failure modes than the ones you trained against.

---

## Run 1: DevLog — Daily Developer Activity Digest

### Product Description

**System Request:** Build a lightweight daily digest system that helps individual contributors recap and share their work at end of day. Developers fill out a short daily log (3–5 fields: what they worked on, what they completed, blockers, and what they plan tomorrow). The system sends a formatted summary to a configurable Slack channel at the end of each business day.

**Key requirements:**
- Developers access a simple web form (or Slack shortcut) to fill out their daily log — no more than 2 minutes to complete
- A nightly job aggregates that day's entries and posts a formatted summary to a team Slack channel
- The summary is readable in Slack without clicking through to another page
- Developers can configure their display name and whether their entries are included in the team digest (opt-out)
- Managers can view a rolling 30-day history of their team's logs in a web dashboard

**Technical context:** The team uses React, Python (FastAPI), and PostgreSQL. Slack integration via Slack Bolt for Python. Infrastructure is Docker-based, deployed on AWS (ECS Fargate). Authentication via Entra ID / OIDC.

**Out of scope for V1:** AI summarization, sentiment analysis, cross-team comparisons, integrations other than Slack.

---

### Step 1: Full DevLog Pipeline Run (60 minutes)

Run all seven delivery skills in sequence. Do not change any command.

1. `create-scope.md` → `devlog-scope.md`
2. `create-architecture.md` → `devlog-architecture.md` (input: `devlog-scope.md`)
3. `create-ux.md` → `devlog-ux.md` (input: `devlog-scope.md`)
4. `decompose-to-deliverables.md` → `devlog-workstreams-deliverables.md` (input: above three)
5. `plan-deliverable.md` → `devlog-plan.md` (input: one selected deliverable)
6. `create-deliverable.md` → `devlog-deliverable.md` (input: deliverable + plan)
7. `review-deliverable.md` → `devlog-review.md` (input: deliverable + implementation)

---

### Step 2: DevLog Quality Review (30 minutes)

Grade each output against the test criteria from the corresponding command's test file. Trace any failures.

Create `devlog-pipeline-run-notes.md`:

```markdown
## Delivery Pipeline Run Notes — DevLog — [date]

### Output Quality by Stage
**Create scope document:** [pass/fail summary]
**Create Architecture:** [pass/fail summary]
**Create UX:** [pass/fail summary]
**Workstreams & Deliverables:** [pass/fail summary]
**Plan Deliverable:** [pass/fail summary]
**Implement Deliverable:** [pass/fail summary]
**Review Deliverable:** [pass/fail summary]

### Generalization: What Held Up vs. What Did Not
[For each command that failed on DevLog criteria: was the failure a prompt issue or an input quality issue?]

### Upstream Dependency Trace
[At least one failure traced to its source command]
```

---

## Run 2: Kata I2 — Blackjack with Strategy Coach

### The Kata Description (Abbreviated)

Build a Blackjack game following standard casino rules (dealer hits on soft 16, stands on soft 17, blackjack pays 3:2). For every player decision point, display the mathematically optimal play based on basic strategy charts. Track and display player decision accuracy — the percentage of decisions that matched optimal strategy — across the session.

Key challenges: the basic strategy lookup table (a 2D table mapping player hand vs. dealer up-card to optimal action — not a function that calculates the optimal play, but a table you implement correctly); multi-hand split logic; soft vs. hard hand distinction.

See [Katas-Intermediate.md](../Appendix-A-Development-Katas/Katas-Intermediate.md) for the full kata description and stretch goals.

---

### Step 3: Full Blackjack Pipeline Run (60 minutes)

Run all seven delivery skills in sequence against the Blackjack kata description. Do not change any command.

1. `create-scope.md` → `blackjack-scope.md`
2. `create-architecture.md` → `blackjack-architecture.md`
3. `create-ux.md` → `blackjack-ux.md`
4. `decompose-to-deliverables.md` → `blackjack-workstreams-deliverables.md`
5. `plan-deliverable.md` → `blackjack-plan.md` (select the core strategy implementation deliverable)
6. `create-deliverable.md` → `blackjack-deliverable.md`
7. `review-deliverable.md` → `blackjack-review.md`

---

### Step 4: Blackjack Quality Review (30 minutes)

This kata specifically exposes whether your commands recognize the distinction between "look up the correct value in a table" and "compute the optimal value algorithmically." These are architecturally different. A scope document that describes the basic strategy as "an algorithm that calculates the optimal play" has misunderstood the domain. A Plan Deliverable that says "implement the strategy function" without identifying the table structure has missed the key implementation decision.

Grade each stage against this specific focus area in addition to your standard test criteria.

Create `blackjack-pipeline-run-notes.md`:

```markdown
## Delivery Pipeline Run Notes — Blackjack — [date]

### Table vs. Algorithm Distinction
**scope document:** Did it identify the basic strategy as a lookup table, not a computed function? [Yes/No]
**Architecture:** Did it describe the data structure for the strategy table? [Yes/No]
**Plan Deliverable:** Did it specify table-based lookup rather than algorithmic calculation? [Yes/No]

### Output Quality by Stage
[Pass/fail summary for each stage]

### Comparison to DevLog Run
[For each command: did performance differ between DevLog and Blackjack? If so, why?]

### Upstream Dependency Trace
[At least one Blackjack-specific failure traced to its source]
```

---

## Step 5: Module 2 Artifact Review

Before moving to Module 3, confirm you have all of the following committed:

- [ ] `create-scope.md` — Context and Constraints complete, load-bearing audit done, Model Ladder checkpoint recorded
- [ ] `create-architecture.md` — Context and Constraints complete, stack load-bearing test done, kata stress test (Conway's) documented
- [ ] `create-ux.md` — Context and Constraints complete, load-bearing audit done, kata stress test (Tic-Tac-Toe) documented
- [ ] `decompose-to-deliverables.md` — Context and Constraints complete, upstream quality comparison done, kata stress test (Snake) documented
- [ ] `plan-deliverable.md` — Context and Constraints complete, stack load-bearing test done, kata stress test (Sorting Visualizer) documented
- [ ] `create-deliverable.md` — Context and Constraints complete, upstream quality reflection done
- [ ] `review-deliverable.md` — Context and Constraints complete
- [ ] Promptfoo configurations with run results for all seven delivery skills (all Haiku only)
- [ ] Load-bearing audit documentation for at least three commands
- [ ] Upstream quality dependency trace: at least one documented case with root cause analysis
- [ ] Model Ladder documentation for at least one command showing full progression
- [ ] DevLog pipeline run output files (all seven) and `devlog-pipeline-run-notes.md`
- [ ] Blackjack kata pipeline run output files (all seven) and `blackjack-pipeline-run-notes.md`

---

## Step 6: Commit Everything

Commit all DevLog and Blackjack output files and both pipeline run notes files.
