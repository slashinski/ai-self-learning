# Exercise 4: The Load-Bearing Audit

*Estimated time: 85 minutes*
*Prerequisites: Exercises 1–3 completed and committed, both baseline scores recorded*

---

## Goal

Act on the hypothesis you formed in Exercise 3. Iterate on your `create-scope` prompt until all test cases pass on Sonnet. Then perform two audits: the load-bearing audit (every instruction earns its place) and the Model Ladder audit (every gap between Sonnet and Haiku is understood and deliberately addressed).

---

## Background: What the Audits Are For

### The Load-Bearing Audit

Prompts tend to accumulate. You add an instruction because the output was bad, the output gets better, you add another instruction for a different failure, and before long you have a prompt that is twenty sentences long and you have no idea which instructions are doing real work and which are just along for the ride.

Dead instructions are not harmless. They take up space, they can conflict with other instructions, and they tell the model things it was already going to do — which crowds out instructions that actually matter.

The load-bearing audit reverses this. You go through the prompt one instruction at a time and remove any that do not correspond to a failing test. What remains is a prompt where every word is earning its place.

### The Model Ladder Audit

Once you have a clean, load-bearing prompt that passes on Sonnet, you have a second question to ask: what would it cost to run this on Haiku instead?

The assertions that pass on Sonnet but fail on Haiku fall into two categories:

1. **Instructions you wrote but Haiku is not following** — the instruction is present, Haiku is misapplying or ignoring it. This is usually an instruction clarity problem: Haiku needs more explicit framing than Sonnet. Rewriting the instruction more precisely often fixes it.

2. **Things Sonnet infers that you never wrote down** — Sonnet is drawing on domain knowledge to fill a gap you left in the prompt. Haiku is not filling that gap. The fix here is not to rewrite an existing instruction — it is to add a new one that makes the implicit explicit.

The second category is more valuable to find. Every implicit inference Sonnet makes on your behalf is something you are paying for at the token level. Making it explicit does not just help Haiku — it makes your prompt more durable, less brittle, and better at handling inputs that differ from the ones you tested.

---

## Step 1: Iterate to Green on Sonnet (40 minutes)

Take the hypothesis you wrote at the end of Exercise 3 for the weakest failing assertion. Make exactly one change to your prompt. Run Promptfoo (both providers will run — record both scores). Record the delta.

Format your iteration record:

```
## Iteration 1 — [date]
Hypothesis: [paste the hypothesis]
Change: Added [specific instruction] to [section]
Sonnet: X/Y → Y/Y assertions passing
Haiku:  X/Y → X'/Y assertions passing
Failing assertions remaining (Sonnet): [list]
Failing assertions remaining (Haiku): [list]
```

Repeat until all Sonnet assertions pass. Record each iteration.

**If you cannot get a specific assertion to pass on Sonnet after 4 iterations:** Examine the rubric. Is it asking for something this prompt genuinely cannot produce, or is the rubric itself ambiguous? If the rubric is ambiguous, rewrite it and re-run from the baseline. If the prompt genuinely cannot produce what the rubric requires, document it.

---

## Step 2: Achieve Green on Sonnet

Confirm all Sonnet assertions pass. Record the Green state:

```
## Green State (Sonnet) — [date]
Sonnet score: Y/Y assertions passing
Haiku score:  [current score]/Y assertions passing
Model Ladder delta at Green: [N] assertions
Iterations from baseline: [N]
```

---

## Step 3: The Load-Bearing Audit (35 minutes)

Read your `create-scope.md` command from top to bottom. For each instruction, ask:

> If I removed this instruction, which assertion in my Promptfoo configuration would fail on Sonnet?

For each instruction, record your prediction:
- **Prediction: [assertion name] would fail** — then verify by removing it and running Promptfoo
- **Prediction: nothing would fail** — remove it and confirm the score holds

Create an audit document:

```
## Load-Bearing Audit — create-scope.md — [date]

| Instruction | Predicted Load-Bearing Assertion | Tested | Result |
|-------------|----------------------------------|--------|--------|
| [instruction text] | [assertion] | Yes | Kept — score dropped as predicted |
| [instruction text] | None — candidate | Yes | Removed — score held |
| ... | ... | ... | ... |
```

---

## Step 4: The Model Ladder Audit (20 minutes)

With your load-bearing-audited prompt in place, look at the remaining Haiku failures. For each assertion that passes on Sonnet but fails on Haiku, apply this two-question test:

**Question 1:** Is the instruction present in my prompt? Run the failing assertion manually against the Haiku output and check whether Haiku is ignoring an instruction that is there, or producing output that reflects a gap in what the prompt says.

- If Haiku is ignoring a present instruction: the instruction needs to be more explicit. Rewrite it so that it leaves less room for interpretation. Test on both models after the change.
- If Haiku is filling a gap Sonnet fills automatically: add a new instruction to cover that gap. Write it as a specific fact or rule, not a general directive.

**Question 2:** Is closing this gap worth the instruction cost? Before adding any new instruction, ask whether it would apply to all future product descriptions — not just the Pomodoro kata. If the instruction you are about to add is specific to Pomodoro timers, do not add it to the command. That is adding a constraint, not improving a command. If you can write it generically (e.g., "The scope document must surface any browser API dependencies that require explicit user permission"), add it and confirm it is load-bearing by verifying a Haiku test case that was previously failing now passes.

Record your Model Ladder audit:

```
## Model Ladder Audit — create-scope.md — [date]
Starting delta: [N] assertions Sonnet passes / Haiku fails

| Failing Assertion (Haiku) | Root Cause | Action Taken | Result |
|---------------------------|------------|--------------|--------|
| [assertion] | Sonnet inferring [X] / instruction ambiguous | Added [instruction] | Haiku now passes |
| [assertion] | Sonnet inferring [X] / not worth fixing generically | Accepted — left on Sonnet | Delta unchanged |
| ... | ... | ... | ... |

Final delta: [N] assertions
Decision: [which remaining gaps are accepted vs. planned for future iteration]
```

---

## Step 5: Final Commit

Commit the final version of `create-scope.md` (with dead instructions removed), your updated test file containing the full iteration record, the load-bearing audit, and the Model Ladder audit.

---

## Self-Check

Before moving to Module 2, verify:

- [ ] All Sonnet assertions pass (Green state recorded)
- [ ] Your test file contains the full iteration record (one entry per Promptfoo run)
- [ ] Load-bearing audit is documented (with the result table)
- [ ] At least one instruction was tested for removal (even if it proved load-bearing)
- [ ] Model Ladder audit is documented: each Haiku failure has a root cause and a decision
- [ ] At least one Haiku failure was addressed by adding a missing explicit instruction (not just a Sonnet-specific improvement)
- [ ] The final `create-scope.md` is committed, and the commit message references "load-bearing audit"

---

## Reflection

Take 10 minutes to write down your answers to these questions (in your test file or a separate notes file):

1. Which instruction surprised you the most by being load-bearing?
2. Which instruction surprised you the most by being dead weight?
3. What did the Haiku failures tell you about what Sonnet was inferring silently?
4. After the Model Ladder audit: which gaps did you close, and which did you deliberately accept? What was your reasoning?

These answers will be useful in Module 2 when you apply the same discipline to six more commands.
