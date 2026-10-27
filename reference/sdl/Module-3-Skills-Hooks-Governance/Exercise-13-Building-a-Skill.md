# Exercise 13: Building a Skill

*Estimated time: 2.5–3 hours*
*Prerequisites: Exercise 12 complete*

---

## Goal

Convert one of your existing commands to a skill. Apply EDD with invocation-aware test cases — not just quality tests for the output, but tests for whether the skill should and should not invoke in specific scenarios.

---

## Background: EDD for Skills Is Different

For a command, EDD tests output quality: does this output meet these criteria?

For a skill, EDD also tests invocation correctness: did the model invoke the skill when it should? Did it correctly not invoke the skill when it should not?

A skill with good output quality but incorrect invocation behavior is a broken skill. Over-invocation (skill runs when it should not) is often more dangerous than under-invocation (skill does not run when it should). An un-invoked skill means a human does the work manually. An over-invoked skill means a machine does work no one expected.

---

## Step 1: Write the Skill Test File First (45 minutes)

Choose the command you identified as the stronger skill candidate in Exercise 12. Create `[command-name]-skill-tests.md`. Commit it before building the skill.

A skill test file has three types of cases:

**Positive invocation cases** — scenarios where the skill SHOULD invoke.
- What is the specific input or context?
- What signals would tell the model this is a correct invocation moment?
- What output would you expect?

**Negative invocation cases** — scenarios where the skill SHOULD NOT invoke.
- What is the specific input or context that looks similar but should not trigger the skill?
- What should the model do instead?
- What failure mode occurs if the skill invokes incorrectly here?

**Quality cases** — given that the skill did invoke, does the output meet the standard?
- These are the same criteria from your command's Promptfoo test file
- Restate them here so they are traceable to invocation context

Write at least 2 positive, 2 negative, and 2 quality cases.

**The hard part is the negative cases.** Think carefully about inputs that are adjacent to the correct invocation context but where invoking the skill would be wrong or premature. The closer these are to the positive cases, the more precise your skill's invocation criteria need to be.

---

## Step 2: Build the Skill (45 minutes)

Consult your `skill-mechanism-notes.md` from Exercise 12 to understand the structural differences between a command file and a skill file in your tool.

Create the skill file. The key addition beyond the command file: the skill needs to describe when it should be invoked. In most tools, this is done through metadata, trigger descriptions, or invocation hints in the skill definition itself.

Think carefully about the invocation description: it should be specific enough that the model invokes the skill on positive cases and does not invoke it on negative cases. If the description is too broad, over-invocation will result. If too narrow, under-invocation.

---

## Step 3: Test Invocation Behavior (45 minutes)

Test the skill against your positive and negative cases. For each case:
- Set up the context (paste the relevant input or situation into your AI tool session)
- Observe whether the skill invokes or does not invoke
- Record the result in your test file

If a positive case does not trigger the skill: what would you change in the skill's invocation description to make it trigger?

If a negative case does trigger the skill: what would you change to prevent incorrect invocation?

Iterate until all positive cases invoke and all negative cases do not. Document each iteration the same way you would a Promptfoo iteration: hypothesis, change, result.

---

## Step 4: Quality Validation (20 minutes)

For cases where the skill did invoke, validate the output quality against your quality test cases. If quality has degraded from the command version: diagnose whether the degradation is in the prompt itself or in the invocation context (sometimes skills receive less explicit context than commands do, because the human is not actively directing the task).

---

## Step 5: Commit

Commit the skill file and `[command-name]-skill-tests.md` with the full invocation and quality test results.

---

## Self-Check

- [ ] Skill test file committed before the skill file was built
- [ ] At least 2 positive, 2 negative, and 2 quality test cases
- [ ] All positive cases invoke the skill
- [ ] All negative cases do not invoke the skill
- [ ] Quality test cases pass for output produced by invocation
- [ ] Iteration record committed (hypothesis, change, result format)
- [ ] Skill file is committed in the location your tool expects for skills
