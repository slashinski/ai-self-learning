# Exercise 7: Create UX

*Estimated time: 2–2.5 hours*
*Prerequisites: Exercise 6 complete*

---

## Goal

Apply the EDD cycle to the UX command. The model's default UX output tends to be generic — it lists components without specifying interactions, and it assumes user types without grounding them in the actual audience. Context about audience and platform, and Constraints about UX spec format, are the key additions.

---

## The Starter Command

Create `create-ux.md`:

```markdown
# Create UX

## Role
You are a Senior UX Designer who produces clear, developer-ready UX specifications.

## Task
Given a scope document, produce a UX Specification describing the user interface and interaction flows for the described feature or system.

## Context
<!-- TO BE DEFINED through EDD iteration -->

## Constraints
<!-- TO BE DEFINED through EDD iteration -->
```

---

## Step 1: Run the Starter and Observe (15 minutes)

Run `create-ux.md` against the TeamPulse scope document. Record what the model assumes about users (technical vs. non-technical), what format the UX spec takes, and what it omits that a developer would need to implement the UI.

---

## Step 2: Write the Test File First (40 minutes)

Create `create-ux-tests.md`. Commit before adding anything.

Write at least 4 criteria. Think through:

1. **Required elements:** What must a developer-ready UX spec include? At minimum: component inventory (what UI elements exist), interaction flows (how users move through the system), state handling (what happens in error states, empty states, loading states), and accessibility notes.

2. **Audience-specific detail:** TeamPulse has two user types: engineering managers and engineers. How does the UX differ for each? A criterion about audience-appropriate detail would fail against a spec that treats both user types identically.

3. **Format specificity:** "Developer-ready" means a developer can implement the spec without asking clarifying questions. What level of specificity makes a UX spec developer-ready vs. designer-ready vs. just a sketch?

4. **Mobile accessibility:** The product description specifies the survey form must be mobile-accessible and completable in under 3 minutes. Write a criterion that tests whether the UX spec addresses this requirement specifically.

---

## Step 3: Build and Iterate (60 minutes)

Configure `create-ux-promptfoo.yaml` with Haiku as the sole provider. Baseline, then iterate.

Pay attention to the Context vs. Constraints distinction here:
- **Context:** Who are the users (engineering managers and engineers)? What is their technical sophistication? What is the platform (web, mobile-accessible)?
- **Constraints:** What must the UX spec contain? What format should it follow?

Minimum: 3 Promptfoo runs with hypotheses. Load-bearing audit after Green.

---

## Step 4: Three-Command Pipeline Check (20 minutes)

Run scope document → Architecture → UX in sequence using your improved commands. Compare the UX output to what you would get from the starter RT-only commands.

Document any observed quality improvement in `create-ux-tests.md`.

---

## Step 5: Kata Stress Test — Tic-Tac-Toe with Unbeatable AI (20 minutes)

Run your finalized `create-ux.md` against Kata B3 (Tic-Tac-Toe with Unbeatable AI) from Appendix A. Use the kata description as your product description input.

**What to watch for:** This kata has three distinct play modes — Player vs. Player, Easy AI (random move selection), and Impossible AI (minimax with move visualization). Each mode has a different interaction model. The UX spec should address mode-specific UI differences, not treat all three modes as variants of the same interface.

The critical test: does your UX command produce separate interaction flows for each mode? Does it describe how the move evaluation visualization works in Impossible AI mode (showing minimax scores on the board)? A UX spec that says "three play modes with a mode selector" without describing each mode's distinct interface is failing this kata.

Record your findings:

```
## Kata Stress Test — Tic-Tac-Toe — [date]
UX output (key findings):
- Did it produce mode-specific interaction flows? [Yes/No]
- Did it describe the move evaluation visualization? [Yes/No]
- Other notable failures or successes: [describe]
Root cause if failed: [Context gap / Constraints gap / Upstream quality]
Action taken: [hypothesis + change made, if any]
```

---

## Step 6: Checkpoint

**If you cannot close a gap after 3 iterations, document it as accepted with reasoning and move on.** Not every gap can be closed generically — the log of what you accepted and why is as valuable as what you fixed. (15 minutes)

```
## Checkpoint — create-ux.md — [date]
Haiku score:  X/Y

Gaps closed this exercise: [list]
Gaps accepted (with reasoning): [list]
```

---

## Step 7: Commit

Commit `create-ux.md`, `create-ux-tests.md`, `create-ux-promptfoo.yaml`, sample UX output, and kata stress test notes.

---

## Self-Check

- [ ] `create-ux-tests.md` committed before Context or Constraints added
- [ ] Both user types (manager and engineer) addressed in criteria
- [ ] Mobile accessibility requirement addressed in criteria
- [ ] Minimum 3 Promptfoo runs with hypotheses
- [ ] Load-bearing audit completed
- [ ] Kata stress test (Tic-Tac-Toe) completed and documented
- [ ] Model Ladder checkpoint recorded
