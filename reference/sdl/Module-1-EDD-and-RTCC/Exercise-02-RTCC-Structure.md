# Exercise 2: RTCC Prompt Construction

*Estimated time: 75 minutes*
*Prerequisites: Exercise 1 completed and committed*

---

## Goal

Build your first RTCC-structured prompt for `create-scope`. Validate it against the test cases you wrote in Exercise 1. By the end of this exercise, your prompt should pass at least the test cases that failed against the bare prompt — without adding instructions that have no test to justify them.

---

## The RTCC Structure

Every prompt in this program follows this four-part structure:

**Role:** Who is the AI acting as? A specific, credentialed persona changes tone, vocabulary, and default assumptions. "An experienced Product Manager who writes developer-ready scope documents" behaves differently from "a helpful assistant" — and if you cannot specify the difference, you do not yet know what role you need.

**Task:** What specific action should it perform? Verb-first, unambiguous. "Given a product description, produce a complete scope document" is better than "help with requirements."

**Context:** What background information does the persona need? What do they know about the situation, the audience, the prior steps? Context gives the model the information it needs to make the right judgment calls — not as rules, but as facts about the situation.

**Constraints:** What rules must the output follow? What should it never do? What format is required? Constraints are guardrails, not substitutes for Role and Task. Adding Constraints before establishing Role and Task often produces outputs that satisfy the guardrails but miss the intent.

---

## Step 1: Draft Each Element Separately (30 minutes)

Draft each RTCC element in isolation before combining them. This order matters — it prevents you from letting a constraint idea drive the prompt design before the core contract is established.

**Role — draft this first:**
Who should be producing this scope document? Think about:
- What expertise does this person have?
- What distinguishes their output from a generic AI summary of the product description?
- Does naming a specific context (e.g., "a Product Manager who writes scope documents for engineering-led teams") change what the model produces in ways that serve your test criteria?

Write 2–3 sentences describing the role.

**Task — draft this second:**
What exactly is this role doing? Be verb-first and specific:
- What are they producing, and from what input?
- What is the intended consumer of the output — who will read this scope document and what decisions will they make from it?
- What is the output's purpose — a planning artifact, a sprint input, a handoff document?

Write 1–3 sentences describing the task.

**Context — draft this third:**
What does this persona need to know about the situation?
- What does a developer-ready scope document include that a designer-ready or business-ready scope document might not? (Think: non-functional requirements, implementation environment, explicit scope boundaries, open questions that must be resolved before implementation begins.)
- What assumptions should the model make about the deployment context (web app, browser-based, no native dependencies)?
- What is the audience for this scope document — a solo developer, a sprint team, a QA team?

Write 3–6 sentences of context. Note: context should be facts and background, not rules. Rules go in Constraints.

**Constraints — draft this last:**
What must be true of the output?
- Required sections (and their minimum content)
- What vague language must never appear without a measurable definition (e.g., "responsive," "fast," "accurate," "easy to use")
- What scope boundary requirements must be present (explicit out-of-scope section, not just absence of features)
- What open-question requirements must be present (implied unknowns must be surfaced, not silently resolved)

Write a set of specific, testable constraints. Each constraint should correspond to at least one criterion from your Exercise 1 test file.

---

## Step 2: Combine and Write the Command File (15 minutes)

Create a file called `create-scope.md` in your repository. Structure it as:

```markdown
# Create Scope

## Role
[Your drafted role]

## Task
[Your drafted task]

## Context
[Your drafted context]

## Constraints
[Your drafted constraints]
```

This is a command file — a prompt you invoke explicitly by pasting or referencing it in your AI tool, followed by the product description as input. Keep it as a Markdown file you can commit, iterate on, and reference precisely.

---

## Step 3: Test the Prompt Against Your Test Cases (20 minutes)

Run `create-scope.md` (with the Pomodoro product description appended as input) against each of your 5 test case inputs from Exercise 1. For each output, grade it against your test criteria. Update your test file with pass/fail results for this version of the prompt.

If test cases that previously failed now pass: good. Note which instruction in your RTCC prompt caused the pass. (This is the beginning of the load-bearing insight — you are already mapping instructions to test outcomes.)

If test cases still fail: identify which RTCC element is missing or weak. Is the failure because the model lacks information (Context problem) or because the model is not following a rule (Constraints problem)? Make one targeted change and re-test.

**Rule: one change per iteration.** Do not change Role and Task and three Constraints at once. You will not know which change made the difference.

---

## Step 4: The Instruction Check (10 minutes)

Before committing, read every sentence in your RTCC prompt. For each sentence, ask: which test criterion would fail if I removed this? If you cannot name a test criterion that would fail, you have two choices:

1. Remove the sentence.
2. Add a test criterion that it corresponds to, then keep the sentence.

Do not keep instructions that have no test to justify them. They are not doing measurable work.

---

## Step 5: Commit (required before moving on)

Commit `create-scope.md` to your repository. The commit timestamp should be after your `create-scope-tests.md` commit — this ordering is the evidence that you did EDD correctly.

---

## Self-Check

Before moving to Exercise 3, verify:

- [ ] `create-scope.md` is committed, with a later timestamp than your test file
- [ ] The prompt has all four RTCC sections
- [ ] Your updated test file shows pass/fail results for this version of the prompt
- [ ] At least 3 of your 5 test cases now pass
- [ ] Every sentence in the prompt has a corresponding test criterion (or was removed)
- [ ] You made at most one change per test iteration (not a wholesale rewrite)
