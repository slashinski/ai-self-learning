# Exercise 24: Stage 4 Certification Portfolio Assembly

*Estimated time: 3–4 hours*
*Prerequisites: Exercises 18–23 complete*

---

## Goal

Assemble the complete Stage 4 certification portfolio. Verify all five required artifacts against the automatic FAIL conditions. Fix any gaps before submission. Submit the portfolio to the certification SharePoint site with a note requesting Stage 4 review.

This is the final assembly exercise. Every artifact you built in Modules 5 and 6 comes together here into a single, reviewer-ready portfolio. The work is not building anything new — it is verifying that what you built actually meets the bar, and being honest about what does not.

---

## Background: What Stage 4 Certification Requires

Stage 4 certification is not a continuation of Stage 3 with more artifacts. It is a different category of capability. Stage 3 certifies that you can build and evaluate individual AI-assisted delivery skills. Stage 4 certifies that you can orchestrate those skills into an automated workflow with guardrails, human punch-out points, measured end-to-end success rates, and per-step cost accountability — and that the workflow runs without a human typing each step.

The five required artifacts are:

1. **Workflow Definition** — the harness script that executes the pipeline end-to-end, plus the Stage 3 evaluation artifacts for each agent in the workflow
2. **Guardrails** — hook scripts, sentinel file schemas, and adversarial review agent prompts between every step
3. **Punch-Out Evidence** — bypass test logs showing that human evacuation points work
4. **End-to-End Success Rate Report** — the composite success rate across multiple pipeline runs
5. **Audit Trail** — per-step model, token, and cost data from actual pipeline runs

Each artifact has automatic FAIL conditions. If any condition is present, the portfolio fails review — not because the reviewer is strict, but because the condition indicates the workflow is not actually Stage 4. This exercise walks you through verifying each one.

---

## Step 1: Create the Portfolio Directory Structure (15 minutes)

Create a `stage-4-portfolio/` directory at the root of your repository. Organize the five artifacts into subdirectories so a reviewer can navigate them without reading your full commit history:

```
stage-4-portfolio/
  01-workflow-definition/
    harness.sh                         (from Exercise 18)
    README.md                          (explains how to run the harness)
    stage-3-eval-artifacts/            (Promptfoo configs + iteration records for each delivery skill in the pipeline)
  02-guardrails/
    hooks/                             (hook scripts from Exercise 19)
    sentinel-schemas/                  (sentinel file schemas for each gated step)
    adversarial-agents/                (adversarial review agent prompts from Exercise 23)
    README.md                          (explains the guardrail layer)
  03-punch-out-evidence/
    bypass-test-logs.md                (from Exercise 20)
    README.md
  04-success-rate/
    success-rate-report.md             (from Exercise 21)
    raw-run-data/                      (individual run logs)
    README.md
  05-audit-trail/
    audit-trail.json                   (from Exercise 22)
    audit-trail-README.md              (explains the schema and how to query it)
  portfolio-checklist.md               (the verification checklist from Step 6)
  submission-note.md                   (the note you will submit to SharePoint)
```

Copy — do not move — your artifacts into this structure. The original files stay where they are in your repository history. The portfolio directory is the reviewer-facing index.

If any of the five subdirectories would be empty, stop. You are missing an artifact from a previous exercise. Go back and complete it before continuing this exercise.

---

## Step 2: Verify Artifact 1 — Workflow Definition (30 minutes)

The workflow definition artifact has two parts: the harness script and the Stage 3 evaluation artifacts for each agent.

### Part A: The Harness Script

Open `harness.sh` and verify:

- [ ] It executes the full 7-step delivery pipeline (or your workflow's equivalent step sequence) end-to-end
- [ ] No step requires a human to type a command or paste output between steps
- [ ] Each step's output is passed programmatically to the next step's input
- [ ] The script exits non-zero on any step failure
- [ ] The script logs each step's start, completion, and status

**FAIL condition: no automated harness.** If the "harness" is a document that says "run this command, then run this command" — that is not a harness. A harness is executable code. If a reviewer cannot run your script and watch the pipeline execute, this artifact fails.

**FAIL condition: human review between steps.** If the harness pauses and waits for a human to approve each step before continuing, the human is the workflow — which is Stage 2, not Stage 4. The harness may pause at defined punch-out points (Artifact 3), but the default path is automated. If your harness has `read` or `prompt` statements between every step, remove them or gate them behind an explicit `--interactive` flag that is not the default.

### Part B: Stage 3 Evaluation Artifacts

For each delivery skill (agent) in the pipeline, verify that its Stage 3 evaluation artifacts are present in `stage-3-eval-artifacts/`:

- [ ] The delivery skill file (e.g., `create-scope.md`)
- [ ] The Promptfoo configuration (e.g., `create-scope-promptfoo.yaml`)
- [ ] At least one iteration record showing a baseline score and a subsequent score after a change
- [ ] The test file that defines the success criteria for that skill

**FAIL condition: missing Stage 3 eval artifacts.** Stage 4 builds on Stage 3. If you cannot show that each agent in the workflow was individually evaluated and iterated — with defined test criteria, measured scores, and documented improvements — the workflow is a pile of untested prompts wired together. That is not certification-worthy.

If any agent in the pipeline lacks its evaluation artifacts, go back to the relevant Module 1–2 exercise and produce them. Do not proceed without them.

---

## Step 3: Verify Artifact 2 — Guardrails (30 minutes)

Open each guardrail artifact and verify it is real, not decorative.

### Hook Scripts

For each hook script in `hooks/`:

- [ ] The script makes a deterministic pass/fail decision — no LLM calls, no subjective judgment
- [ ] The script reads a sentinel file (or equivalent structured output) and checks specific properties
- [ ] The script exits non-zero on failure with a message that tells the developer what to fix
- [ ] The script is triggered automatically by the harness between steps, not manually

**FAIL condition: window-dressing guardrails.** A guardrail that exists but is not wired into the harness is documentation, not a guardrail. If the harness does not call the hook between steps, the hook is not protecting anything. Verify by reading the harness code: does it invoke each hook? Does it check the exit code? Does it halt on failure?

### Sentinel Schemas

For each sentinel schema in `sentinel-schemas/`:

- [ ] The schema defines specific, checkable properties (not "output looks good")
- [ ] The schema was designed before the hook script was built (check commit timestamps if uncertain)
- [ ] The relationship between sentinel checks and Promptfoo assertions is documented — which properties does the sentinel cover (minimum bar), and which are left to Promptfoo (quality bar)?

### Adversarial Review Agents

For each adversarial review agent prompt in `adversarial-agents/`:

- [ ] The agent has a distinct review lens (e.g., scope creep, architectural drift, missing edge cases, spec compliance) — not a generic "review this" prompt
- [ ] The agent is instructed to find problems, not to confirm quality — the prompt should bias toward rejection, not acceptance
- [ ] The agent's output is structured (pass/fail + specific findings), not freeform prose
- [ ] The agent is wired into the harness between the appropriate steps

**FAIL condition: non-adversarial agents.** An adversarial review agent that says "review the output and provide feedback" is not adversarial — it is a mirror. A real adversarial agent is instructed to find a specific class of failure, given the criteria to check against, and required to produce a binary verdict with cited evidence. If your adversarial agent prompts read like "check if this looks good," rewrite them.

---

## Step 4: Verify Artifact 3 — Punch-Out Evidence (20 minutes)

Open `bypass-test-logs.md` and verify:

- [ ] At least 2 punch-out points are defined — specific points in the workflow where a human can take over
- [ ] Each punch-out point has a documented trigger condition (when should a human intervene?)
- [ ] Bypass tests were actually run — the logs show what was tested, what happened, and whether the human could successfully resume the workflow after intervening
- [ ] The bypass test includes at least one case where the punch-out was triggered by a guardrail failure (not just a manual choice to pause)

**FAIL condition: untested punch-outs.** A punch-out point that is defined but never exercised is theoretical. The reviewer needs to see that you actually triggered the punch-out, took over manually, and either completed the step by hand or fixed the issue and resumed the harness. If your bypass test logs say "this should work" without showing a real test run, this artifact fails.

---

## Step 5: Verify Artifacts 4 and 5 — Success Rate and Audit Trail (30 minutes)

### End-to-End Success Rate Report

Open `success-rate-report.md` and verify:

- [ ] The report covers at least 10 pipeline runs (or the number specified in Exercise 21)
- [ ] The success rate is a single composite number — what percentage of runs completed end-to-end without any step failing
- [ ] Per-step failure rates are broken out (which steps fail most often?)
- [ ] The report includes the raw run data so a reviewer can verify the composite number

**FAIL condition: no end-to-end rate.** If the report has per-step quality scores but no composite end-to-end success rate, you have measured the parts but not the whole. Stage 4 is about the workflow, not the individual skills. The end-to-end rate is the single most important number in the portfolio.

### Audit Trail

Open `audit-trail.json` (or your equivalent format) and verify:

- [ ] Each step execution records: the model used, input token count, output token count, and cost
- [ ] The data comes from at least 3 pipeline runs (not a single run)
- [ ] The total cost per run is calculable from the data
- [ ] The schema is documented — a reviewer should be able to understand the structure without reverse-engineering it

**FAIL condition: no cost data.** An audit trail without per-step model, token, and cost data is just a log. The cost data is what makes the workflow measurable in production — you cannot make cost-adjusted capacity decisions without it. If your audit trail records what happened but not what it cost, this artifact fails.

---

## Step 6: Run the FAIL Condition Checklist (30 minutes)

Create `portfolio-checklist.md` in the `stage-4-portfolio/` directory. Work through every FAIL condition below. For each, mark PASS or FAIL with a one-line explanation of what you verified.

```markdown
## Stage 4 Portfolio FAIL Condition Checklist — [date]

### Workflow Definition
- [ ] PASS/FAIL: Automated harness exists and is executable
  - Verified: [what you checked]
- [ ] PASS/FAIL: No human review required between steps (default path is automated)
  - Verified: [what you checked]
- [ ] PASS/FAIL: Stage 3 eval artifacts present for every agent in the pipeline
  - Verified: [which agents, how many artifacts confirmed]

### Guardrails
- [ ] PASS/FAIL: Hook scripts make deterministic decisions (no LLM judgment)
  - Verified: [which hooks, what they check]
- [ ] PASS/FAIL: Hooks are wired into the harness (not standalone scripts)
  - Verified: [how the harness invokes them]
- [ ] PASS/FAIL: Adversarial review agents have distinct lenses and bias toward rejection
  - Verified: [list each agent and its lens]
- [ ] PASS/FAIL: Guardrails are not window-dressing (removing them would change behavior)
  - Verified: [what happens when you remove a guardrail — does the harness still pass?]

### Punch-Out Evidence
- [ ] PASS/FAIL: At least 2 punch-out points defined with trigger conditions
  - Verified: [list the punch-out points]
- [ ] PASS/FAIL: Bypass tests were actually run (not theoretical)
  - Verified: [what the logs show]

### End-to-End Success Rate
- [ ] PASS/FAIL: Composite end-to-end success rate reported from 10+ runs
  - Verified: [the number, how many runs]
- [ ] PASS/FAIL: Per-step failure rates broken out
  - Verified: [which step fails most]

### Audit Trail
- [ ] PASS/FAIL: Per-step model, token, and cost data present for 3+ runs
  - Verified: [how many runs, which fields]
- [ ] PASS/FAIL: Total cost per run is calculable
  - Verified: [example calculation]

### Agent Independence
- [ ] PASS/FAIL: No agent in the workflow requires manual correction to produce usable output
  - Verified: [if any agent does, name it and explain what is being done about it]
```

### The Agent Independence Check

The last FAIL condition deserves special attention: **agents needing manual correction.** This is the most common reason a Stage 4 portfolio fails review. If the reviewer reads your pipeline run notes and sees that you had to manually edit the output of `create-scope` before `create-architecture` could use it, or that `create-deliverable` produced code that required manual fixes before `review-deliverable` could evaluate it — the workflow is not autonomous. It is human-assisted with AI steps in between.

Be honest about this. If an agent does require manual correction, name it in the checklist and explain what you are doing to close the gap. A portfolio that says "create-architecture occasionally produces output that needs manual cleanup before passing to decompose-to-deliverables; I am iterating on the Context section to reduce this" is more credible than one that claims zero manual intervention without evidence.

If more than one agent requires manual correction, the workflow is not ready for Stage 4. That is a valid finding — document it, and plan the work needed to close the gaps.

---

## Step 7: Write the Submission Note (15 minutes)

Create `submission-note.md` in the `stage-4-portfolio/` directory. This is the note you will attach when you submit to the SharePoint site. It should contain:

1. **Repository link** — the URL of your repository
2. **Portfolio directory** — the path to `stage-4-portfolio/` within the repository
3. **Certification stage requested** — explicitly state "Stage 4" (the SharePoint site is labeled "Stage 3 certification requests" — you must note that you are requesting Stage 4 review, not Stage 3)
4. **Artifact summary** — one line per artifact, with the file path:
   - Workflow Definition: `stage-4-portfolio/01-workflow-definition/harness.sh`
   - Guardrails: `stage-4-portfolio/02-guardrails/`
   - Punch-Out Evidence: `stage-4-portfolio/03-punch-out-evidence/bypass-test-logs.md`
   - End-to-End Success Rate: `stage-4-portfolio/04-success-rate/success-rate-report.md`
   - Audit Trail: `stage-4-portfolio/05-audit-trail/audit-trail.json`
5. **Composite success rate** — the single number from your success rate report
6. **Known gaps** — any FAIL condition that did not pass, with what you are doing about it. If everything passed, say so explicitly.
7. **Specific feedback requests** — areas where you want the reviewer to focus (e.g., "I want feedback on whether my adversarial review agents are sufficiently distinct in their lenses")

```markdown
## Stage 4 Certification Submission — [your name] — [date]

**Repository:** [URL]
**Portfolio directory:** stage-4-portfolio/
**Certification stage requested:** Stage 4

### Artifacts
1. Workflow Definition: stage-4-portfolio/01-workflow-definition/harness.sh
2. Guardrails: stage-4-portfolio/02-guardrails/
3. Punch-Out Evidence: stage-4-portfolio/03-punch-out-evidence/bypass-test-logs.md
4. End-to-End Success Rate: stage-4-portfolio/04-success-rate/success-rate-report.md
5. Audit Trail: stage-4-portfolio/05-audit-trail/audit-trail.json

### Summary
- Composite end-to-end success rate: [X]% across [N] runs
- Most common failure point: [which step]
- Total average cost per run: $[X.XX]

### Known Gaps
[Any FAIL conditions that did not pass, or "None — all FAIL conditions verified as PASS."]

### Feedback Requests
[Specific areas where you want reviewer focus.]
```

---

## Step 8: Commit and Submit (20 minutes)

### Commit

Commit the entire `stage-4-portfolio/` directory with a clear commit message:

```
Stage 4 certification portfolio: all five artifacts assembled and verified
```

Verify the commit includes:
- The portfolio directory with all five artifact subdirectories
- `portfolio-checklist.md` with every FAIL condition checked
- `submission-note.md`

### Submit

Go to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx).

Upload or link your submission note and provide:
1. Your repository link
2. The path to the portfolio directory
3. A note that you are requesting **Stage 4** review (not Stage 3 — the site name says "Stage 3" because it handles both)

The reviewer will examine your portfolio against the five artifacts and the FAIL conditions. Expect the review to take 1–2 weeks. The reviewer may request a live walkthrough of the harness running.

---

## Stage 4 Artifact Checklist

Before submitting, confirm every item is present and verified:

- [ ] `stage-4-portfolio/01-workflow-definition/harness.sh` — executable, runs pipeline end-to-end, no manual steps in default path
- [ ] `stage-4-portfolio/01-workflow-definition/stage-3-eval-artifacts/` — eval artifacts for every agent in the pipeline
- [ ] `stage-4-portfolio/02-guardrails/hooks/` — deterministic hook scripts, wired into the harness
- [ ] `stage-4-portfolio/02-guardrails/sentinel-schemas/` — schemas designed before hooks, with documented relationship to Promptfoo assertions
- [ ] `stage-4-portfolio/02-guardrails/adversarial-agents/` — distinct lenses, bias toward rejection, structured output
- [ ] `stage-4-portfolio/03-punch-out-evidence/bypass-test-logs.md` — at least 2 punch-out points, real bypass tests
- [ ] `stage-4-portfolio/04-success-rate/success-rate-report.md` — composite rate from 10+ runs, per-step breakdown
- [ ] `stage-4-portfolio/05-audit-trail/audit-trail.json` — per-step model/token/cost data from 3+ runs
- [ ] `stage-4-portfolio/portfolio-checklist.md` — every FAIL condition checked PASS or FAIL with evidence
- [ ] `stage-4-portfolio/submission-note.md` — complete, with Stage 4 explicitly noted
- [ ] Everything committed to your repository
- [ ] Submitted to the [SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx) with Stage 4 noted

---

## Self-Check

- [ ] All five artifact subdirectories are populated — none are empty
- [ ] The harness runs without manual intervention on the default path
- [ ] Every hook is called by the harness, not just present in the directory
- [ ] Every adversarial agent has a distinct, named review lens
- [ ] Bypass test logs show real test runs, not theoretical descriptions
- [ ] The success rate is a single composite number, not just per-step scores
- [ ] The audit trail has cost data, not just timestamps and outputs
- [ ] No agent in the workflow silently requires manual correction (or if one does, it is documented honestly)
- [ ] The submission note explicitly says "Stage 4"
- [ ] You could hand this portfolio to a reviewer who has never seen your repository and they could navigate to every artifact from the directory structure alone