# Exercise 20: Punch-Out Points and Bypass Testing

*Estimated time: 2–3 hours*
*Prerequisites: Exercise 19 complete (guardrails implemented and tested)*

---

## Goal

Implement 2–3 punch-out points in your shell harness — explicit points where the workflow cannot proceed without human sign-off. Then actively attempt to bypass each one. Document what happened when you tried to skip the human and what the system did to stop you.

A punch-out point that exists on paper but was never tested for bypass is a **RED SIGNAL** in Stage 4 certification review. This exercise ensures yours are real.

---

## Background: Punch-Out Points vs Fail-the-Workflow

Your harness has two distinct ways to handle something going wrong. Confusing them is the most common Stage 4 design error.

### Fail the Workflow (Automation Handles)

A **fail-the-workflow** condition is a problem the harness can address without a human. The harness detects the problem and takes one of three actions:

1. **Retry** — run the step again (sometimes with a slightly different invocation, e.g., a different temperature or a re-phrased prompt)
2. **Re-prompt** — feed the failed output back to the model with a correction instruction ("your output was missing the risk section — regenerate with all required sections")
3. **Escalate to a stronger model** — if Haiku failed, retry with Sonnet; if Sonnet failed, retry with Opus

The key property: **no human is involved.** The harness handles it. The failure is logged, the retry is automatic, and the workflow either succeeds on retry or exhausts its retry budget and halts (which is itself a fail-the-workflow outcome, not a punch-out).

Examples of fail-the-workflow conditions:
- Scope document missing a required section (re-prompt with the missing section called out)
- Architecture document references a technology not in the approved stack (retry with a constraint reminder)
- Sentinel check fails because a word count is below threshold (retry with a length requirement)
- Model returned malformed JSON (retry with a format instruction)

### Punch Out to Human (Genuine Human Decision Point)

A **punch-out point** is a point where the workflow cannot proceed without a decision that requires human judgment. The harness does not have the information or authority to make this decision. It stops and waits.

The key property: **the harness cannot resolve this.** It needs a human to make a call.

Examples of genuine punch-out points:
- **Scope approval** — the scope document is structurally complete (passes sentinel) but the scope itself is a business decision. Does this product actually need the features the scope describes? That is not a quality question. It is a product direction question. The harness cannot answer it.
- **Architecture sign-off** — the architecture is valid (passes guardrails) but involves a trade-off that requires stakeholder agreement. "We chose PostgreSQL over MongoDB because the data is relational" is a decision a human needs to approve, not a quality failure the harness can retry around.
- **Deliverable acceptance** — the deliverable passes the review agent's quality bar, but "is this what the client actually wants?" is a question only a human who knows the client can answer. The review agent checks quality. It does not check client satisfaction.

### The Distinction in One Sentence

> **Fail-the-workflow** = the harness detected a problem it can fix. **Punch-out** = the harness detected a decision it cannot make.

### Why Bypass Testing Matters

A punch-out point is a gate. The gate exists to stop the workflow until a human acts. But gates can be broken in ways that are not obvious:

- The harness might check for a sign-off file but not verify who created it (you could `touch scope-approved.flag` and the harness proceeds)
- The harness might check for a non-empty sign-off file but accept any content (you could write `echo "yes" > scope-approved.flag`)
- The harness might check the sign-off file exists but not verify it was created after the scope document (a stale approval from a previous run could satisfy the check)
- The harness might not check at all if the step that produces the scope document also writes the approval file (the gate is cosmetic)

Each of these is a bypass. Someone tried to skip the human and the system let them through. A punch-out point that can be bypassed is not a punch-out point — it is a suggestion. Stage 4 certification treats untested punch-out points as **automatically failing**. The reviewer's question is not "do you have punch-out points?" but "show me what happened when you tried to skip them."

---

## Step 1: Identify Your Punch-Out Points (20 minutes)

Review your 7-step delivery pipeline and identify 2–3 points where the workflow genuinely requires a human decision. Not every step needs a punch-out — some steps are fully automatable once their guardrails pass. But some decisions are inherently human.

For each candidate punch-out point, answer these three questions:

1. **What decision does the human make?** (Not "review the output" — that is a guardrail's job. What specific decision can the harness not make?)
2. **Why can the harness not make this decision?** (What information or authority does it lack?)
3. **What would go wrong if the harness proceeded without this decision?** (What is the concrete risk of skipping the human?)

If you cannot answer all three questions clearly, the point is probably a fail-the-workflow condition, not a punch-out. Move it to the fail-the-workflow path and find a real punch-out point instead.

Write your punch-out point definitions in `punch-out-points.md`:

```markdown
## Punch-Out Point Definitions — [date]

### Punch-Out Point 1: [name — e.g., Scope Approval]

**Location in pipeline:** After create-scope, before create-architecture
**Decision the human makes:** [e.g., Is this scope the right product direction for this client?]
**Why the harness cannot make it:** [e.g., The harness has no knowledge of the client's business priorities, market constraints, or stakeholder preferences]
**Risk of skipping:** [e.g., The architecture, UX, and all downstream deliverables are built for the wrong product — hours of wasted generation]

### Punch-Out Point 2: [name]

**Location in pipeline:** [after step X, before step Y]
**Decision the human makes:** [...]
**Why the harness cannot make it:** [...]
**Risk of skipping:** [...]

### Punch-Out Point 3: [name]

[...]
```

---

## Step 2: Implement the Punch-Out Points in Your Harness (45 minutes)

For each punch-out point, implement a gate in your shell harness. The gate must:

1. **Halt the workflow** — no subsequent step runs until the gate is cleared
2. **Require a specific sign-off artifact** — a file, a prompt response, or an interactive confirmation that records the human's decision
3. **Record the sign-off** — who approved, when, and what was approved (not just "yes" — the sign-off must reference the specific artifact being approved)

Here is a reference implementation for an interactive punch-out point in bash:

```bash
#!/bin/bash
# punch_out_scope_approval.sh
# Punch-out point: scope approval before architecture generation

SCOPE_FILE="$1"
APPROVAL_FILE=".harness/signoffs/scope-approval.json"

mkdir -p .harness/signoffs

# --- Gate: halt until human acts ---
echo ""
echo "=== PUNCH-OUT POINT: Scope Approval ==="
echo "The scope document has passed all guardrails."
echo "Before generating architecture, a human must approve the scope."
echo ""
echo "Scope document: $SCOPE_FILE"
echo ""
echo "Review the file, then return here."
echo ""

# Record what we are asking the human to approve
SCOPE_HASH=$(sha256sum "$SCOPE_FILE" | awk '{print $1}')
SCOPE_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Wait for human sign-off
while true; do
    read -p "Do you approve this scope for architecture generation? (approve/reject): " DECISION

    case "$DECISION" in
        approve)
            # Write a structured sign-off that binds to the specific artifact
            cat > "$APPROVAL_FILE" <<EOF
{
  "punch_out_point": "scope-approval",
  "decision": "approve",
  "approved_file": "$SCOPE_FILE",
  "approved_file_hash": "$SCOPE_HASH",
  "timestamp": "$SCOPE_TIMESTAMP",
  "approved_by": "\${USER:-unknown}"
}
EOF
            echo "Scope approved. Proceeding to architecture generation."
            exit 0
            ;;
        reject)
            cat > "$APPROVAL_FILE" <<EOF
{
  "punch_out_point": "scope-approval",
  "decision": "reject",
  "rejected_file": "$SCOPE_FILE",
  "rejected_file_hash": "$SCOPE_HASH",
  "timestamp": "$SCOPE_TIMESTAMP",
  "rejected_by": "\${USER:-unknown}"
}
EOF
            echo "Scope rejected. Workflow halted."
            exit 1
            ;;
        *)
            echo "Invalid response. Type 'approve' or 'reject'."
            ;;
    esac
done
```

Integrate it into your harness between the relevant steps:

```bash
# In your main harness script (harness.sh), between scope and architecture:

# Step 1: Create scope
run_step "create-scope" "$INPUT_FILE" "outputs/scope.md"

# Guardrail: check scope sentinel
check_guardrail "scope-sentinel.json" || handle_scope_guardrail_failure

# Punch-out point 1: scope approval
bash punch_out_scope_approval.sh "outputs/scope.md"
if [ $? -ne 0 ]; then
    log_event "PUNCH_OUT" "scope-approval" "REJECTED" "Human rejected scope. Workflow halted."
    exit 1
fi

# Step 2: Create architecture (only runs after approval)
run_step "create-architecture" "outputs/scope.md" "outputs/architecture.md"
```

Repeat for your other 2–3 punch-out points. Each one follows the same pattern: halt, wait for human, record the decision with a binding to the specific artifact.

---

## Step 3: Test the Happy Path (15 minutes)

Run your harness with a product description that produces good output. Confirm that:

1. The harness runs each step
2. At each punch-out point, the harness halts and prompts for human sign-off
3. When you approve, the harness proceeds to the next step
4. The sign-off file is written with the correct artifact hash and timestamp
5. The workflow completes end-to-end

Record the happy path result:

```markdown
## Punch-Out Happy Path Test — [date]

**Punch-out point 1 (scope approval):**
- Harness halted: Yes
- Human prompted: Yes
- Decision: approve
- Sign-off file written: Yes
- Sign-off contains correct hash: Yes/No
- Harness proceeded: Yes

**Punch-out point 2 ([name]):**
[...]

**Punch-out point 3 ([name]):**
[...]

**End-to-end completion:** Yes/No
```

---

## Step 4: Bypass Testing — Actively Try to Skip Each Punch-Out Point (60 minutes)

This is the critical step. For each punch-out point, you will attempt to bypass it — to make the harness proceed without a genuine human sign-off. The goal is to find a way through. If you find one, that is a bug in your gate. Fix it and re-test.

### Bypass Attempt 1: Pre-create the sign-off file

Before running the harness, create the sign-off file manually:

```bash
mkdir -p .harness/signoffs
echo '{"punch_out_point":"scope-approval","decision":"approve"}' > .harness/signoffs/scope-approval.json
bash harness.sh
```

**Expected:** The harness detects a pre-existing sign-off file and either (a) refuses to proceed because the sign-off was not created during this run, or (b) validates the sign-off's artifact hash against the current scope document and rejects it because the hash does not match (the scope did not exist when the sign-off was created).

**If the harness proceeds:** Your gate checks for file existence only. It does not bind the sign-off to the current run or the current artifact. Fix: validate the sign-off file's `approved_file_hash` against the actual hash of the scope document at the point of the gate. If they do not match, the sign-off is stale or fabricated — halt.

### Bypass Attempt 2: Write garbage content to the sign-off file

Create the sign-off file with meaningless content:

```bash
echo "yes" > .harness/signoffs/scope-approval.json
bash harness.sh
```

**Expected:** The harness attempts to parse the sign-off file as structured data and fails, halting the workflow with a clear error message.

**If the harness proceeds:** Your gate checks for file existence but does not validate file content. Fix: parse the sign-off file and verify it contains the required fields (`punch_out_point`, `decision`, `approved_file_hash`, `timestamp`). If any field is missing or invalid, halt.

### Bypass Attempt 3: Approve with a reject decision in the file

Write a sign-off file with `decision: reject` but run the harness anyway:

```bash
cat > .harness/signoffs/scope-approval.json <<EOF
{
  "punch_out_point": "scope-approval",
  "decision": "reject",
  "approved_file": "outputs/scope.md",
  "approved_file_hash": "PLACEHOLDER",
  "timestamp": "2025-01-01T00:00:00Z"
}
EOF
bash harness.sh
```

**Expected:** The harness reads the sign-off, sees `decision: reject`, and halts. A rejection is a rejection — the harness must not proceed on a rejected sign-off even if the file exists.

**If the harness proceeds:** Your gate checks for file existence but does not check the decision value. Fix: verify `decision` equals `approve` before proceeding.

### Bypass Attempt 4: Hash mismatch (if your gate validates hashes)

Create a valid-looking sign-off file with a hash that does not match the actual scope document:

```bash
# Generate the scope document first (run step 1 only)
# Then create a sign-off with a wrong hash
cat > .harness/signoffs/scope-approval.json <<EOF
{
  "punch_out_point": "scope-approval",
  "decision": "approve",
  "approved_file": "outputs/scope.md",
  "approved_file_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
bash harness.sh
```

**Expected:** The harness computes the actual hash of `outputs/scope.md`, compares it to the hash in the sign-off file, finds a mismatch, and halts.

**If the harness proceeds:** Your gate does not validate the hash binding. Fix: compute the hash of the approved file at gate time and compare it to the hash recorded in the sign-off. If they differ, the sign-off does not apply to this artifact — halt.

### Bypass Attempt 5: Modify the harness to skip the gate

Edit the harness script to comment out or skip the punch-out call:

```bash
# Comment out the punch-out call in harness.sh
# bash punch_out_scope_approval.sh "outputs/scope.md"
```

Then run the harness.

**Expected:** This bypass will succeed — you have the source code. This is expected and not a failure. The point of this test is to acknowledge it: the harness is software, and anyone with write access to the harness can disable any gate. The defense is not technical — it is procedural. The harness and its sign-off artifacts must be committed to version control, and any commit that removes or weakens a punch-out gate must be visible in the commit history. Document this as an accepted limitation with a procedural mitigation.

### Documenting Bypass Results

For each bypass attempt on each punch-out point, record:

```markdown
## Bypass Test Results — [date]

### Punch-Out Point 1: Scope Approval

**Bypass 1 (pre-create sign-off file):**
- Attempted: [what you did]
- Result: [blocked / bypassed]
- If blocked: [how the gate detected it]
- If bypassed: [how it got through] → Fix: [what you changed] → Re-test: [blocked / bypassed]

**Bypass 2 (garbage content):**
- Attempted: [...]
- Result: [...]
- [...]

**Bypass 3 (reject decision in file):**
- Attempted: [...]
- Result: [...]
- [...]

**Bypass 4 (hash mismatch):**
- Attempted: [...]
- Result: [...]
- [...]

**Bypass 5 (modify harness source):**
- Attempted: [commented out punch-out call]
- Result: Bypassed (expected — source code access)
- Mitigation: [e.g., "Harness and sign-off files committed to git. Commits that remove punch-out gates are visible in history and require review before merge."]

### Punch-Out Point 2: [name]

[Same bypass attempts 1–5]

### Punch-Out Point 3: [name]

[Same bypass attempts 1–5]
```

---

## Step 5: Fix and Re-Test (30 minutes)

For any bypass attempt that succeeded (attempts 1–4 only — attempt 5 is an accepted limitation), fix the gate and re-run the bypass attempt. Document the fix and the re-test result.

A bypass that is fixed and re-tested to blocked is a **strong signal** in certification review. It shows you found a real gap and closed it. A bypass that was never found because you never tried is a **RED SIGNAL**.

Common fixes:

| Bypass | Fix |
|--------|-----|
| Pre-created sign-off file | Validate sign-off timestamp is after the artifact was created, or validate the artifact hash matches the sign-off's recorded hash |
| Garbage content | Parse the sign-off file as structured data (JSON); reject if parse fails or required fields are missing |
| Reject decision in file | Check `decision` field equals `approve` — do not proceed on any other value |
| Hash mismatch | Compute the hash of the approved file at gate time; compare to the sign-off's hash; reject on mismatch |

Update your bypass test results document with the fix and re-test for each successful bypass.

---

## Step 6: Classify Your Fail-the-Workflow Conditions (15 minutes)

To make the distinction between fail-the-workflow and punch-out explicit, list every failure condition your harness handles automatically (without human intervention). For each, classify it as fail-the-workflow and record which automated response the harness uses.

Write this in `failure-mode-classification.md`:

```markdown
## Failure Mode Classification — [date]

### Fail-the-Workflow Conditions (Harness Handles Automatically)

| Condition | Where | Automated Response | Retry Budget |
|-----------|-------|-------------------|--------------|
| Scope missing required section | After create-scope | Re-prompt with missing section called out | 2 retries |
| Sentinel word count below threshold | After create-scope | Retry with length requirement | 1 retry |
| Architecture references unapproved technology | After create-architecture | Retry with stack constraint reminder | 2 retries |
| Model returned malformed JSON | Any step | Retry with format instruction | 3 retries |
| Review agent rejects deliverable quality | After create-deliverable | Re-prompt with review feedback | 1 retry |
| [...] | [...] | [...] | [...] |

### Punch-Out Points (Human Decision Required)

| Punch-Out Point | Where | Decision | Why Human |
|-----------------|-------|----------|-----------|
| Scope approval | After create-scope, before create-architecture | Is this the right product direction? | Harness has no client business context |
| Architecture sign-off | After create-architecture, before create-ux | Is this the right technical trade-off? | Harness has no stakeholder context |
| Deliverable acceptance | After review-deliverable | Is this what the client wants? | Harness cannot assess client satisfaction |

### Why Each Punch-Out Is Not a Fail-the-Workflow

For each punch-out point, explain why the harness cannot handle it automatically:
- Scope approval: [why retry/re-prompt/escalate cannot substitute for a human's product direction judgment]
- Architecture sign-off: [...]
- Deliverable acceptance: [...]
```

This classification is the artifact that proves you understand the distinction. A reviewer will look for it.

---

## Step 7: Commit

Commit the following to your repository:

- `punch-out-points.md` — definitions of your 2–3 punch-out points
- Updated `harness.sh` with punch-out gates integrated
- `punch_out_*.sh` — individual punch-out gate scripts
- `punch-out-happy-path-test.md` — happy path test results
- `bypass-test-results.md` — bypass attempt results with fixes and re-tests
- `failure-mode-classification.md` — fail-the-workflow vs punch-out classification

---

## Self-Check

- [ ] 2–3 punch-out points defined, each with a clear human decision the harness cannot make
- [ ] Each punch-out point implemented as a gate in the harness that halts the workflow
- [ ] Happy path tested: harness halts at each punch-out, proceeds on approval, writes structured sign-off
- [ ] Bypass attempt 1 (pre-create sign-off) tested for each punch-out point — blocked or fixed and re-tested
- [ ] Bypass attempt 2 (garbage content) tested for each punch-out point — blocked or fixed and re-tested
- [ ] Bypass attempt 3 (reject in file) tested for each punch-out point — blocked or fixed and re-tested
- [ ] Bypass attempt 4 (hash mismatch) tested for each punch-out point — blocked or fixed and re-tested
- [ ] Bypass attempt 5 (modify source) documented as accepted limitation with procedural mitigation
- [ ] Every successful bypass (1–4) has a documented fix and re-test showing it is now blocked
- [ ] Fail-the-workflow conditions listed and classified separately from punch-out points
- [ ] Sign-off files bind to specific artifacts via hash, not just file existence
- [ ] All artifacts committed

---

## Reflection

Take 10 minutes to write down your answers to these questions:

1. Which bypass attempt surprised you the most by succeeding? What did you assume was safe that was not?
2. Before this exercise, could you have explained the difference between "fail the workflow" and "punch out to human"? Has the distinction changed how you think about your pipeline?
3. If a reviewer asked you "show me what happened when you tried to skip a punch-out point," would your bypass test results give them confidence that your gates are real? If not, what is missing?
4. The harness source code can always be modified to skip a gate (bypass attempt 5). What procedural or organizational controls would you need in a real team setting to make punch-out points trustworthy beyond a single developer's laptop?