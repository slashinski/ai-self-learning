# Exercise 5: Create Scope

*Estimated time: 3–4 hours*
*Prerequisites: Module 1 complete — your `create-scope.md` exists with load-bearing audit and Model Ladder baseline documented*

---

## Goal

Your `create-scope` command was built in Module 1 against the Pomodoro kata — a small consumer app with clear scope. Now run it against TeamPulse, which is more complex, enterprise-oriented, and has different implied requirements: multi-user roles, anonymous data handling, recurring scheduled jobs, and SSO integration. The gap between how your command performs on Pomodoro and how it performs on TeamPulse is your starting state for this exercise. Use EDD to close that gap.

---

## Step 1: Run Your Module 1 Command Against TeamPulse (30 minutes)

Open your existing `create-scope.md` from Module 1 — this is your starting point, not a new stub. Run it against the TeamPulse product description from the Module 2 overview. Do not change the command yet. Read the output carefully.

For each element, ask:
- Which of your Module 1 test criteria does this output pass? Which does it fail?
- What assumption did the model make that is not in the TeamPulse description?
- What would a skilled Product Manager always include that the model omitted for this enterprise context?
- What language is too vague to be useful to a developer? Look for "secure," "scalable," "performant," or "anonymous" without measurable definitions.

Write your observations. These are your raw test criteria for TeamPulse — you are already doing EDD, you just haven't committed the test file yet.

---

## Step 2: Extend the Test File (45 minutes)

Add TeamPulse-specific test cases to `create-scope-tests.md` (your existing test file from Module 1, or create a new one if you prefer to keep them separate). Before adding any new Context or Constraints, commit.

Write at least 4 new test criteria for TeamPulse. These should cover failure modes your Module 1 tests did not address:

1. **Anonymous data handling:** The scope document must define what "anonymous" means operationally — not just state that responses are anonymous. Does the model specify that no individual attribution can appear in any view, including admin and database views? Or does it use "anonymous" as a vague assurance?

2. **Multi-role requirements:** TeamPulse has two distinct user types with different access scopes (engineers: survey submission only; managers: dashboard and configuration). The scope document must address both roles with distinct requirements. A scope document that treats the system as if it has one user type is failing this criterion.

3. **Scope specificity:** The TeamPulse description names four explicit out-of-scope items for V1. Your test should verify that all four appear by name in the scope document's out-of-scope section, not just that an out-of-scope section exists.

4. **A criterion of your own:** Based on your Step 1 observations, what failure mode appeared that would affect a developer implementing TeamPulse?

---

## Step 3: Iterate (90 minutes)

If you do not already have `create-scope-promptfoo.yaml` with TeamPulse test cases, create it now. Add your new criteria as assertions. Run baseline against Haiku only — the two-model Model Ladder comparison was a Module 1 exercise and is not repeated here.

Remember the Context-first sequence: if the scope document omits a section or fails to surface a concern because the model doesn't know it's expected, that is a Context problem. If the scope document uses vague language because nothing told it not to, that is a Constraints problem.

Minimum: 3 Promptfoo runs (baseline + 2 iterations) for the TeamPulse domain. Document each with a hypothesis.

After achieving Green on Haiku: load-bearing audit (any new instruction added in this exercise must be tested for removal, not just assumed load-bearing).

---

## Step 4: Kata Stress Test — Pomodoro Regression Check (20 minutes)

Run your updated `create-scope.md` against the Pomodoro kata description you used in Module 1. This is a regression check: your TeamPulse improvements should not have broken what worked for Pomodoro.

Run your full Promptfoo suite (all test cases) and confirm your Module 1 test cases still pass. If any Module 1 assertions now fail, you added a TeamPulse-specific constraint that does not generalize. Find it, make it generic, and re-run.

Document the regression check:

```
## Kata Regression Check — Pomodoro — [date]
Module 1 Promptfoo score after TeamPulse iteration:
  Haiku:  X/Y (was Y/Y after Module 1)
Any regressions: [Yes/No — if Yes, describe and fix]
```

---

## Step 5: Model Ladder Checkpoint (15 minutes)

Record your current Haiku score for `create-scope` after all iterations:

```
## Model Ladder Checkpoint — create-scope.md — [date]
Haiku score:  X/Y

Changes made this exercise to close gaps: [list]
Gaps accepted (with reasoning): [list]
```

**Note:** You are running against Haiku only from this point forward. The two-model Model Ladder comparison was a Module 1 exercise — you learned the lesson once, and now running both models on every evaluation would double your token costs without adding diagnostic value. Green on Haiku means done. If you cannot close a specific gap after several iterations, document it and accept it — but closing it is the default.

You can monitor your AI usage at [usage.improving.ai](https://usage.improving.ai).

---

## Step 6: Comparison Snapshot

Save both a Module 1 starter run output and your current command output against TeamPulse. This side-by-side comparison shows how much the command improved across the two modules.

```
## Create Scope Command Progression — [date]
Module 1 command (Pomodoro-tuned) against TeamPulse:
  Haiku score: [N/Y]
  Key failures: [list]
Module 2 command (TeamPulse-tuned) against TeamPulse:
  Haiku score: [Y/Y]
  Most significant improvement: [which criterion changed most]
```

---

## Step 7: Commit

Commit updated `create-scope.md`, updated test file, updated Promptfoo configuration, regression check results, and Model Ladder checkpoint.

---

## Self-Check

- [ ] At least 4 new TeamPulse-specific test criteria committed before adding new Context or Constraints
- [ ] Context and Constraints were added sequentially (Context first)
- [ ] Minimum 3 Promptfoo runs (Haiku only) with hypotheses recorded for TeamPulse domain
- [ ] Load-bearing audit updated for any new instructions
- [ ] Kata regression check completed — Module 1 test cases still pass
- [ ] Model Ladder checkpoint recorded
- [ ] Comparison snapshot committed
