# Exercise 15: Governed Two-Step Flow

*Estimated time: 2.5–3 hours*
*Prerequisites: Exercise 14 complete*

---

## Goal

Connect two of your delivery skills into a governed two-step flow: the first command runs and writes a sentinel file, the hook makes a deterministic go/no-go decision, and the second command runs only if the check passes. Test all four scenarios. Write the governance explanation paragraph.

---

## Background: What Makes a Flow Governed

A governed flow is not fully automated — the human is still present at every no-go checkpoint. But the go path is automated and the gate is deterministic. This is the minimal pattern for safe multi-step AI automation.

The value: you are no longer manually deciding whether the first step's output is good enough to proceed. The hook does that decision deterministically, based on criteria you defined. You review the output only when the hook says something went wrong.

What makes this different from Promptfoo: Promptfoo runs during development to improve a command. The hook runs in production on every execution. It is fast, always-on, and enforces the minimum bar — not the full quality bar.

---

## Step 1: Choose the Two Commands (10 minutes)

Use `create-scope.md` (with the sentinel file you built in Exercise 14) as Step 1. Use `create-architecture.md` as Step 2.

The governed flow you will build:
1. `create-scope` runs and produces `scope.md` + `scope-sentinel.json`
2. Hook reads `scope-sentinel.json`, makes go/no-go decision
3. If go: `create-architecture` runs automatically using `scope.md` as input
4. If no-go: flow halts, human is prompted to review and fix `scope.md` before continuing

---

## Step 2: Extend the Hook for the Go Path (45 minutes)

Modify the hook script from Exercise 14 to add the go path: when all sentinel checks pass, trigger `create-architecture.md`.

How you trigger the next step depends on your tool:
- In Claude Code: the hook can write a trigger file or emit a message that Claude Code can act on
- In Windsurf: consult the documentation for how a hook can trigger a subsequent agent action
- As a fallback: the hook can write a file called `proceed-to-architecture.flag`, and you can configure a second hook that detects this file and triggers the architecture step

The specific implementation depends on your tool. What matters for this exercise is that:
- The go path is triggered automatically (not by you manually)
- The no-go path halts the flow and provides a clear message about what failed

---

## Step 3: Build and Test All Four Scenarios (75 minutes)

Test each scenario and record results in `governed-flow-test-results.md`:

**Scenario 1 — Go path (nominal):**
- Input: a product description that produces a passing scope document
- Expected: scope document written, sentinel written, hook passes, architecture runs automatically
- Test: does it happen without manual intervention?

**Scenario 2 — No-go path:**
- Input: an input that produces a scope document missing a required sentinel property (craft this intentionally)
- Expected: scope document written, sentinel written, hook fails, flow halts, clear failure message
- Test: does the architecture command not run?

**Scenario 3 — Gap scenario:**
- Input: a product description that passes the sentinel but produces a scope document that fails a Promptfoo assertion (passes the minimum bar but not the quality bar)
- Expected: flow proceeds (the sentinel is not full validation), architecture runs on a weaker-than-ideal scope document
- Document: what this gap means and why it is acceptable (sentinel is the minimum bar; Promptfoo is the quality bar, run during development)

**Scenario 4 — Missing sentinel:**
- Input: run the hook without a sentinel file present (simulate a case where the scope document command failed silently)
- Expected: hook detects missing sentinel, halts flow with clear message

```markdown
## Governed Flow Test Results — [date]

**Scenario 1 (go path):**
Input: [product description used]
Sentinel values: [what scope-sentinel.json contained]
Hook decision: PASS
Architecture triggered: Yes/No (should be Yes)
Notes: [anything unexpected]

**Scenario 2 (no-go path):**
Input: [what you did to produce a failing scope document]
Sentinel values: [what scope-sentinel.json contained]
Hook decision: FAIL
Failure message: [exact message from hook]
Architecture triggered: Yes/No (should be No)

**Scenario 3 (gap scenario):**
Input: [product description]
Sentinel pass/fail: PASS
Promptfoo assertion that fails: [which one]
Architecture ran: Yes
Notes: [explanation of why this is acceptable]

**Scenario 4 (missing sentinel):**
Hook behavior: [what happened]
Notes:
```

---

## Step 4: Automation Spectrum Assessment (30 minutes)

Write `automation-spectrum-assessment.md`. For every delivery skill you have built in this program, assess where it sits on the spectrum:

```markdown
## Automation Spectrum Assessment — [date]

For each delivery skill, answer: Is it ready to be a skill? Would a sentinel file add value?
What would team consensus look like before sharing it?

### Delivery Skills
**create-scope:** [assessment — note: already has sentinel]
**create-architecture:** [assessment]
**create-ux:** [assessment]
**decompose-to-deliverables:** [assessment]
**plan-deliverable:** [assessment]
**create-deliverable:** [assessment]
**review-deliverable:** [assessment]

### Overall Assessment
[2–3 sentences: which delivery skills are closest to being shared skills, and what would need to be true first]
```

---

## Step 5: Governance Explanation Paragraph (20 minutes)

Write one paragraph, addressed to a technically-aware manager who has never heard of sentinel files or hooks. The paragraph should explain why you would not automate a multi-step AI workflow without these governance mechanisms, even if all the individual prompts were EDD-validated.

Constraints for this paragraph:
- No jargon from this program (no "sentinel file", "EDD", "RTCC")
- Must address the business risk of automation without governance, not just the technical risk
- Must be conversational — something you could say out loud, not read from a document
- Under 200 words

This paragraph is part of your completion deliverables. It is the most direct test of whether you have internalized the governance rationale.

Save it as `governance-explanation.md`.

---

## Step 6: Commit

Commit the governed flow implementation, `governed-flow-test-results.md`, `automation-spectrum-assessment.md`, and `governance-explanation.md`.

---

## Module 3 Artifact Review

Before moving to Module 4, confirm you have:

- [ ] `skill-readiness-assessment.md` — analysis of two commands for skill readiness
- [ ] Skill file converted from a command, with invocation test cases (positive, negative, quality)
- [ ] `create-scope-sentinel-schema.md` — designed before code was written
- [ ] Hook script with deterministic pass/fail logic, tested against all three scenarios
- [ ] Governed two-step flow tested across all four scenarios
- [ ] `governed-flow-test-results.md` — all four scenarios documented
- [ ] `automation-spectrum-assessment.md` — all commands assessed
- [ ] `governance-explanation.md` — manager-audience paragraph, under 200 words, no program jargon

---

## Self-Check

- [ ] All four governed flow scenarios tested and documented
- [ ] Automation spectrum assessment covers all 7 delivery skills
- [ ] Governance explanation paragraph is under 200 words and avoids program jargon
- [ ] You can read the governance explanation paragraph out loud fluently — if you stumble on it, rewrite it
