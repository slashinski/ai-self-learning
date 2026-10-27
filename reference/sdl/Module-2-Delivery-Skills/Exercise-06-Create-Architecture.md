# Exercise 6: Create Architecture

*Estimated time: 3–3.5 hours*
*Prerequisites: Exercise 5 complete*

---

## Goal

Apply the full EDD cycle to the Architecture command. Architecture documents are heavily context-dependent — the right architecture for a React/Node/Postgres stack looks different from the right architecture for a Python/FastAPI/MongoDB stack. Context that encodes the technical environment is the key addition for this command.

---

## The Starter Command

Create `create-architecture.md`:

```markdown
# Create Architecture

## Role
You are a Senior Solutions Architect who produces clear, implementation-ready architecture documents.

## Task
Given a scope document, produce an Architecture Document describing the technical approach for implementing the described feature or system.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

---

## Step 1: Run the Starter and Observe (20 minutes)

Run `create-architecture.md` against the TeamPulse scope document you produced in Exercise 5. Record what the model assumes about technology choices, integration patterns, and what sections a senior architect would include by default.

Note specifically: does the output reflect the TeamPulse technical context (React, Node.js, PostgreSQL, Entra ID/OIDC)? Or does it produce a generic architecture that could apply to any web application?

---

## Step 2: Write the Test File First (40 minutes)

Create `create-architecture-tests.md`. Commit before adding Context or Constraints.

Write at least 4 criteria. Think through:

1. **Required sections:** What sections does a developer-ready architecture document always include? (Think: component diagram description, data model, API surface, security/auth approach, deployment considerations, open technical decisions.)

2. **Technical specificity:** The architecture should reflect the specified tech stack (React frontend, Node.js backend, PostgreSQL, Entra ID/OIDC SSO). How will you write a criterion that tests this specifically enough to fail against a generic architecture?

3. **The load-bearing Context test:** Run the command with and without your Context section — the outputs should be meaningfully different. Write a criterion that a Context-less run would fail but a Context-informed run would pass.

4. **Open questions:** A good architecture document surfaces what is not yet decided. What specific open questions would a senior architect flag for the TeamPulse system?

---

## Step 3: Build and Iterate (75 minutes)

Configure `create-architecture-promptfoo.yaml` with Haiku as the sole provider. Baseline, then iterate. (From Exercise 6 onward, evaluations run against Haiku only — see the note at the end of Exercise 5's Checkpoint for the reasoning.)

**Specific challenge for this command:** Context that makes the architecture command produce different outputs for different stack descriptions is the goal. Test that your Context is genuinely load-bearing by running the same product description through the command twice — once with the TeamPulse tech stack in Context, once with a different stack (e.g., Python/FastAPI/MongoDB). The architecture documents should differ in specific, named ways. If they don't, your Context is not doing work.

Minimum: 4 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

## Step 4: Upstream Quality Check (20 minutes)

Run your finalized scope document through Architecture. Compare the quality of the Architecture output to what you would get if you ran a starter (RT-only) scope document through Architecture. Does a better upstream scope document produce a better Architecture? Document in `create-architecture-tests.md`:

```markdown
## Upstream Quality Note
scope document quality impact on Architecture:
- Better scope document input → [specific architecture improvements observed]
- Weaker scope document input → [specific gaps in architecture observed]
```

---

## Step 5: Kata Stress Test — Conway's Game of Life (25 minutes)

Run your finalized `create-architecture.md` against Kata B1 (Conway's Game of Life) from Appendix A. Use the kata description as your product description input.

**What to watch for:** Does your architecture command surface the double-buffering requirement for cell state management — maintaining two separate boards (current and next generation) to avoid updating cells while computing their neighbors? Or does it recommend generic React state management ("store the grid in a useState array and update it on each tick")?

A "use React state for the grid" recommendation without addressing the performance pattern is a detectable failure for this kata. The architecture should identify that naively re-rendering 10,000 cells on every tick will be a performance problem and name a specific approach (double-buffering, or an equivalent optimized state model).

Record your findings:

```
## Kata Stress Test — Conway's Game of Life — [date]
Architecture output (key findings):
- Did the architecture name the double-buffering pattern? [Yes/No]
- Did it address rendering optimization? [Yes/No]
- Other notable failures or successes: [describe]
Root cause if failed: [Context gap / Constraints gap / Upstream quality]
Action taken: [hypothesis + change made, if any]
```

If your command failed this kata test: form a hypothesis, make one change, run Promptfoo. Make the change generic — it should improve architecture quality for any performance-critical state management problem, not just Conway's.

---

## Step 6: Checkpoint

**If you cannot close a gap after 3 iterations, document it as accepted with reasoning and move on.** Not every gap can be closed generically — the log of what you accepted and why is as valuable as what you fixed. (15 minutes)

```
## Checkpoint — create-architecture.md — [date]
Haiku score:  X/Y

Gaps closed this exercise: [list]
Gaps accepted (with reasoning): [list]
```

---

## Step 7: Commit

Commit `create-architecture.md`, `create-architecture-tests.md`, `create-architecture-promptfoo.yaml`, sample Architecture output, and kata stress test notes.

---

## Self-Check

- [ ] `create-architecture-tests.md` committed before Context or Constraints added
- [ ] Minimum 4 Promptfoo runs with hypotheses
- [ ] Context load-bearing test completed (different stack → different architecture)
- [ ] Load-bearing audit completed
- [ ] Upstream quality note committed
- [ ] Kata stress test (Conway's Game of Life) completed and documented
- [ ] Model Ladder checkpoint recorded
