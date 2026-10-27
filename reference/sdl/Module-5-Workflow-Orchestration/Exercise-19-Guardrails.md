# Exercise 19: Guardrails Between Steps

*Estimated time: 3–4 hours*
*Prerequisites: Exercise 18 complete*

---

## Goal

Add guardrails between every step of the delivery pipeline harness you built in Exercise 18. Stage 4 certification requires **two complementary forms of guardrails**: deterministic hooks that validate sentinel file schemas between steps, and adversarial review agents that challenge each step's output through a distinct lens. By the end of this exercise, every step boundary in your pipeline has both layers, and you can explain why neither layer alone is sufficient.

---

## Background: Why Two Layers

In Exercise 14, you built a single hook that inspected one sentinel file after one command. In Exercise 15, you used that hook as a go/no-go gate between two steps. That was the minimal governed flow — one hook, one checkpoint, one decision.

Exercise 18 gave you a harness that runs all seven delivery pipeline steps end-to-end. But a harness without guardrails between steps is just a faster way to propagate garbage. Step 3 runs on Step 2's output regardless of whether Step 2 produced something usable. If Step 2 silently degraded — missing a section, truncating output, hallucinating a field — every downstream step inherits the damage and amplifies it.

Stage 4 certification requires that every step boundary is guarded. "Guarded" means two things, and both are required:

### Layer 1: Deterministic Hooks

Hooks are shell functions that read a sentinel file and make a deterministic pass/fail decision. They are fast, always-on, and predictable. They check structural integrity: required fields present, values within bounds, schema conformed. They cannot evaluate whether the content is *good* — only whether it is *structurally valid*.

### Layer 2: Adversarial Review Agents

Adversarial review agents are Stage 3 delivery skills with a specific, adversarial job: attempt to find something wrong with the producing step's output through a **distinct lens** — security, compliance, completeness, or another dimension the producing agent does not already check. They are not a second pass at quality. They are a deliberate attack from a different angle.

### Why Neither Layer Alone Is Sufficient

A hook catches structural failures: a missing field, a truncated file, a section that vanished. It cannot catch a scope document that is structurally perfect but proposes a solution with a security vulnerability the producing agent didn't consider. An adversarial agent can catch that — but it is non-deterministic, costs tokens, and might miss a structural issue that a hook catches instantly. Together, they cover each other's blind spots.

---

## Stage 4 FAIL Conditions

Two failure modes are automatic FAIL for Stage 4 certification. Understand them before you write anything:

1. **Window-dressing hooks.** A hook that only checks whether a file exists or is non-empty is not a guardrail. Every hook must inspect the *contents* of the sentinel file against a schema with at least three meaningful properties. "File exists and is non-empty" is the floor of the floor — it tells you nothing about whether the step's output is usable.

2. **Adversarial agents that re-check the same criteria as the producing agent.** If your producing agent checks quality and your adversarial agent also checks quality, you have two agents doing the same job. The adversarial agent's lens must be **distinct** from the producing agent's self-check. The whole point of an adversarial posture is to look at the output from an angle the producer did not and would not consider.

---

## Step 1: Map Every Step Boundary (20 minutes)

Your harness from Exercise 18 runs the seven-step delivery pipeline:

1. `create-scope`
2. `create-architecture`
3. `create-ux`
4. `decompose-to-deliverables`
5. `plan-deliverable`
6. `create-deliverable`
7. `review-deliverable`

That means six step boundaries:

| Boundary | From → To | What Passes Through |
|----------|-----------|-------------------|
| 1 → 2 | scope → architecture | Scope document |
| 2 → 3 | architecture → UX | Architecture document |
| 3 → 4 | UX → decomposition | UX document |
| 4 → 5 | decomposition → plan | Deliverable list |
| 5 → 6 | plan → deliverable | Deliverable plan |
| 6 → 7 | deliverable → review | Deliverable artifact |

Write a file called `step-boundary-map.md` that lists each boundary, the sentinel file that the producing step writes, and the three properties your hook will check. You will design the sentinel schemas in Step 2, but the map forces you to think about all six boundaries before writing any code.

```markdown
## Step Boundary Map

### Boundary 1: create-scope → create-architecture
- Sentinel file: scope-sentinel.json
- Hook checks: [list 3+ properties]
- Adversarial lens: [which lens — security, compliance, completeness, etc.]

### Boundary 2: create-architecture → create-ux
- Sentinel file: architecture-sentinel.json
- Hook checks: [list 3+ properties]
- Adversarial lens: [which lens]

[...repeat for all six boundaries...]
```

Commit `step-boundary-map.md` before writing any hook code.

---

## Step 2: Extend Sentinel Schemas to Every Step (45 minutes)

In Exercise 14, you built a sentinel schema for `create-scope` only. Now every step must write a sentinel file when it completes. The sentinel file is what the hook inspects — not the deliverable itself, but a structured summary of the deliverable's key properties.

For each of the seven steps, add a Constraint to the skill file instructing it to write a sentinel JSON file. The sentinel must contain at least three meaningful, inspectable properties — not "file exists" or "is non-empty."

**What counts as a meaningful property:**

- `sections_present`: an array of required section names (hook checks that specific names are present)
- `word_count`: a numeric count (hook checks it falls within a defined range)
- `has_measurable_success_criteria`: boolean (hook checks for `true`)
- `max_nesting_depth`: a number (hook checks it does not exceed a threshold)
- `references_resolve`: boolean indicating all internal references point to real sections (hook checks for `true`)
- `external_dependencies`: an array of named dependencies (hook checks array length is within bounds)

**What does NOT count (window-dressing):**

- `file_exists: true` — this tells the hook nothing
- `output_non_empty: true` — this tells the hook nothing
- `word_count > 0` — the minimum bar is a *range*, not "greater than zero"

Example sentinel instruction to add to `create-architecture.md`:

```
After producing the architecture document, write a file called `architecture-sentinel.json` in the same directory. The file must contain:
- `sections_present`: an array listing the section names that appear in the architecture document (must include: "components", "data-flow", "interfaces", "trade-offs")
- `word_count`: the approximate word count of the architecture document body
- `max_nesting_depth`: the maximum nesting depth of any section in the document (e.g., 2 means sections contain subsections but no deeper)
- `component_count`: the number of distinct components described (must be at least 2)
- `has_trade_offs`: true if the document contains at least one explicit trade-off with a named alternative; false otherwise
```

Do this for all seven steps. Each sentinel schema must be specific to what that step produces — do not copy-paste the same schema across steps. The whole point is that each boundary checks properties relevant to that step's output.

Commit the updated skill files before writing hooks.

---

## Step 3: Write Hook Functions for Every Boundary (60 minutes)

Write one shell hook function per boundary. Each function reads the sentinel file, checks at least three properties against the schema, and exits non-zero with a clear message on failure.

You can write these as individual scripts or as functions in a shared library file that the harness sources. The function approach is recommended — it keeps the guardrail logic alongside the harness and avoids file proliferation.

Create `guardrails.sh`:

```bash
#!/bin/bash
# guardrails.sh — deterministic hook functions for every pipeline step boundary.
# Each function reads a sentinel file, checks >= 3 meaningful properties,
# and exits non-zero with a clear failure message on any check failure.

GUARDRAIL_LOG="guardrail-log.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Helper: log and exit on failure
fail() {
  local message="$1"
  echo "[$TIMESTAMP] FAIL: $message" | tee -a "$GUARDRAIL_LOG"
  exit 1
}

# Helper: log pass
pass() {
  local boundary="$1"
  echo "[$TIMESTAMP] PASS: $boundary sentinel checks passed." | tee -a "$GUARDRAIL_LOG"
}

# Boundary 1: create-scope → create-architecture
check_scope_sentinel() {
  local sentinel="$1"
  [ -f "$sentinel" ] || fail "scope-sentinel.json not found. create-scope may not have completed."

  local sections word_count has_success_criteria has_out_of_scope
  sections=$(jq -r '.sections_present | length' "$sentinel")
  word_count=$(jq -r '.word_count' "$sentinel")
  has_success_criteria=$(jq -r '.has_measurable_success_criteria' "$sentinel")
  has_out_of_scope=$(jq -r '.has_explicit_out_of_scope' "$sentinel")

  # Check 1: required sections present (at least 4)
  [ "$sections" -ge 4 ] || fail "scope document has only $sections sections, expected at least 4 (overview, requirements, out_of_scope, open_questions)."

  # Check 2: word count within bounds (200–2000)
  [ "$word_count" -ge 200 ] || fail "scope document word count ($word_count) below minimum of 200."
  [ "$word_count" -le 2000 ] || fail "scope document word count ($word_count) above maximum of 2000."

  # Check 3: measurable success criteria present
  [ "$has_success_criteria" = "true" ] || fail "scope document does not contain measurable success criteria."

  # Check 4: explicit out-of-scope section present
  [ "$has_out_of_scope" = "true" ] || fail "scope document does not contain an explicit out-of-scope section."

  pass "Boundary 1 (scope → architecture)"
}

# Boundary 2: create-architecture → create-ux
check_architecture_sentinel() {
  local sentinel="$1"
  [ -f "$sentinel" ] || fail "architecture-sentinel.json not found. create-architecture may not have completed."

  local sections word_count component_count has_trade_offs
  sections=$(jq -r '.sections_present | length' "$sentinel")
  word_count=$(jq -r '.word_count' "$sentinel")
  component_count=$(jq -r '.component_count' "$sentinel")
  has_trade_offs=$(jq -r '.has_trade_offs' "$sentinel")

  # Check 1: required sections present (at least 4: components, data-flow, interfaces, trade-offs)
  local has_components has_data_flow
  has_components=$(jq -r '.sections_present | map(. == "components") | any' "$sentinel")
  has_data_flow=$(jq -r '.sections_present | map(. == "data-flow") | any' "$sentinel")
  [ "$has_components" = "true" ] || fail "architecture document missing required 'components' section."
  [ "$has_data_flow" = "true" ] || fail "architecture document missing required 'data-flow' section."

  # Check 2: word count within bounds (300–3000)
  [ "$word_count" -ge 300 ] || fail "architecture document word count ($word_count) below minimum of 300."
  [ "$word_count" -le 3000 ] || fail "architecture document word count ($word_count) above maximum of 3000."

  # Check 3: at least 2 components described
  [ "$component_count" -ge 2 ] || fail "architecture document describes only $component_count component(s), expected at least 2."

  # Check 4: trade-offs section is substantive
  [ "$has_trade_offs" = "true" ] || fail "architecture document does not contain explicit trade-offs with named alternatives."

  pass "Boundary 2 (architecture → ux)"
}

# Boundary 3: create-ux → decompose-to-deliverables
check_ux_sentinel() {
  local sentinel="$1"
  [ -f "$sentinel" ] || fail "ux-sentinel.json not found. create-ux may not have completed."

  local sections word_count screen_count has_accessibility
  sections=$(jq -r '.sections_present | length' "$sentinel")
  word_count=$(jq -r '.word_count' "$sentinel")
  screen_count=$(jq -r '.screen_count' "$sentinel")
  has_accessibility=$(jq -r '.has_accessibility_notes' "$sentinel")

  # Check 1: required sections present
  [ "$sections" -ge 3 ] || fail "UX document has only $sections sections, expected at least 3."

  # Check 2: word count within bounds (200–2500)
  [ "$word_count" -ge 200 ] || fail "UX document word count ($word_count) below minimum of 200."
  [ "$word_count" -le 2500 ] || fail "UX document word count ($word_count) above maximum of 2500."

  # Check 3: at least 1 screen described
  [ "$screen_count" -ge 1 ] || fail "UX document describes 0 screens, expected at least 1."

  # Check 4: accessibility notes present
  [ "$has_accessibility" = "true" ] || fail "UX document does not contain accessibility notes."

  pass "Boundary 3 (ux → decomposition)"
}

# Boundaries 4–6 follow the same pattern.
# Write check_decomposition_sentinel, check_plan_sentinel, check_deliverable_sentinel
# following the same structure: >= 3 meaningful content checks, clear failure messages.
```

**Critical:** Do not write hooks that only check `[ -f "$sentinel" ]` and `[ -s "$sentinel" ]`. That is window-dressing. Every hook function must parse the sentinel with `jq` and verify specific properties against specific thresholds. The example above checks four properties per boundary — your hooks must check at least three.

Complete the remaining three hook functions (`check_decomposition_sentinel`, `check_plan_sentinel`, `check_deliverable_sentinel`) following the same pattern. Design the checks based on the sentinel schemas you defined in Step 2.

---

## Step 4: Integrate Hooks into the Harness (30 minutes)

Modify your harness from Exercise 18 so that after each step completes, the corresponding hook function runs before the next step begins. If the hook fails, the harness halts with a clear message and does not proceed.

Add this pattern after each step invocation in your harness:

```bash
# After Step 1: create-scope
devin run --prompt-file create-scope.md --input product-description.md --output-format json > step-1-output.json

# Run guardrail
source guardrails.sh
check_scope_sentinel scope-sentinel.json || {
  echo "HALT: Boundary 1 guardrail failed. Fix scope document before proceeding."
  exit 1
}

# Only reached if guardrail passed — proceed to Step 2
devin run --prompt-file create-architecture.md --input step-1-output.json --output-format json > step-2-output.json

check_architecture_sentinel architecture-sentinel.json || {
  echo "HALT: Boundary 2 guardrail failed. Fix architecture document before proceeding."
  exit 1
}

# ... continue for all steps ...
```

The harness must source `guardrails.sh` once at the top, then call the appropriate function after each step. The `|| { ... exit 1; }` pattern ensures that a non-zero exit from the hook function halts the entire pipeline.

Test: run the harness end-to-end with valid inputs. Verify that all six guardrails fire and pass. Check `guardrail-log.txt` for six PASS entries.

---

## Step 5: Write One Adversarial Review Agent (60 minutes)

Now add the second layer. You will write **one** adversarial review agent prompt — a Stage 3 delivery skill with a distinct lens, its own prompt, and an explicitly adversarial posture. Module 6 (Exercise 23) will have you build the full network of agents for every boundary; here you build one to learn the pattern.

### Choose the Lens

The adversarial agent's lens must be **distinct from what the producing agent already checks**. If `create-scope` already checks for quality (which it does — it has Promptfoo assertions and a self-check), your adversarial agent must not check quality again. Choose from:

- **Security lens:** Does the scope document propose a solution that introduces an attack surface, handles sensitive data carelessly, or assumes trust where none should exist?
- **Compliance lens:** Does the scope document make commitments that conflict with known regulatory constraints (GDPR, HIPAA, SOC 2) or organizational policies?
- **Completeness lens:** Does the scope document omit a stakeholder, a failure mode, or an integration dependency that the producing agent would not think to include because it is outside the scope of "writing a good scope document"?

Pick the lens that is most relevant to your domain. Write it down before writing the prompt.

### Write the Agent Prompt

Create `adversarial-security-review.md` (or `adversarial-compliance-review.md`, etc.):

```markdown
# Adversarial Security Review

## Role

You are a hostile security auditor. Your job is not to improve the document. Your job is to find the most serious security vulnerability in the proposed solution and explain why it would fail in production.

## Task

Read the scope document. Identify the single most exploitable security weakness in the proposed system. Write a one-paragraph finding that names the vulnerability, describes a concrete attack path, and states what would need to change to close it.

## Context

This scope document was produced by a delivery skill that optimizes for clarity, completeness, and measurable success criteria. It was not reviewed for security. That is your job. You are the only voice in this pipeline that thinks like an attacker.

## Constraints

- You must identify exactly one finding — the most serious one, not a list.
- Your finding must name a concrete attack path, not a vague category. "The system might have injection vulnerabilities" is unacceptable. "The proposed API accepts unvalidated user input in the search field, enabling SQL injection via the query parameter" is acceptable.
- If the scope document genuinely has no security-relevant surface, say so explicitly and explain why. Do not invent a finding to seem useful — a clean bill of health is a valid result.
- Do not comment on document quality, structure, or completeness. Another agent handles that. Your lens is security only.
- Maximum 150 words. A finding that cannot be stated in 150 words is not specific enough.
```

### What Makes This Adversarial (Not Just Another Review)

Three properties distinguish this agent from a second quality check:

1. **Distinct lens.** The producing agent (`create-scope`) optimizes for clarity, completeness, and measurable criteria. The adversarial agent optimizes for finding exploitable weaknesses. These are different objectives that require different reasoning.

2. **Adversarial posture.** The prompt says "hostile security auditor" and "find the most exploitable weakness." This is not "review for improvements" — it is "attack this." The posture shapes what the model looks for and how hard it pushes.

3. **Own prompt.** The agent has its own RTCC-structured prompt file, its own role, its own constraints. It is not a parameterized call to the producing agent with a different instruction tacked on. A distinct agent with a distinct prompt produces distinct reasoning.

### Integrate the Agent into the Harness

After the hook passes at Boundary 1 (scope → architecture), run the adversarial agent before proceeding:

```bash
# Boundary 1: deterministic hook
check_scope_sentinel scope-sentinel.json || { echo "HALT: Boundary 1 hook failed."; exit 1; }

# Boundary 1: adversarial review
devin run --prompt-file adversarial-security-review.md --input step-1-output.json --output-format json > boundary-1-adversarial-review.json

# Check adversarial result — if a finding is reported, log it and decide whether to halt
HAS_FINDING=$(jq -r '.has_finding' boundary-1-adversarial-review.json)
if [ "$HAS_FINDING" = "true" ]; then
  FINDING=$(jq -r '.finding' boundary-1-adversarial-review.json)
  echo "[$TIMESTAMP] ADVERSARIAL FINDING (Boundary 1): $FINDING" | tee -a "$GUARDRAIL_LOG"
  # Decision point: halt or proceed? For this exercise, log and proceed.
  # In production, a critical security finding would halt the pipeline.
fi
```

For this exercise, you need the adversarial agent integrated at one boundary. Module 6 Exercise 23 will extend this to every boundary with a full network of distinct lenses.

---

## Step 6: Test Both Layers (45 minutes)

Test the guardrails by deliberately producing failing inputs. For each test, record what happened in `guardrail-test-notes.md`.

### Hook Tests (at least 3 boundaries)

For each boundary you test, run three scenarios:

**Scenario A — Pass:** Run the producing step with a good input. Verify the hook fires, checks pass, and the harness proceeds.

**Scenario B — Fail (structural):** Craft an input that produces a sentinel file with a missing or out-of-bounds property (e.g., word count below minimum, a required section absent). Verify the hook catches it, prints a clear failure message naming the property, and the harness halts.

**Scenario C — Missing sentinel:** Run the hook without a sentinel file present (simulate the producing step failing silently). Verify the hook detects the missing file and halts with a clear message.

### Adversarial Agent Tests

Run the adversarial agent on three inputs:

**Input 1 — Clean scope document:** A scope document for a well-understood problem with no obvious security surface. Verify the agent either finds a non-obvious vulnerability or issues a clean bill of health with reasoning.

**Input 2 — Vulnerable scope document:** A scope document for a system that handles user authentication and stores passwords. Verify the agent identifies a security weakness (e.g., plaintext storage, missing rate limiting, session fixation).

**Input 3 — Producing agent's quality criteria:** Verify that the adversarial agent does NOT comment on document quality, structure, or completeness. If it does, the lens is not distinct enough — revise the prompt.

```markdown
## Guardrail Test Results — [date]

### Hook Tests

**Boundary 1 (scope → architecture):**
- Scenario A (pass): [sentinel values, hook exit code, harness behavior]
- Scenario B (fail): [what was missing, hook message, harness halted?]
- Scenario C (missing sentinel): [hook behavior]

**Boundary 2 (architecture → ux):**
- [same three scenarios]

**Boundary 3 (ux → decomposition):**
- [same three scenarios]

### Adversarial Agent Tests

**Input 1 (clean scope):**
- Finding: [what the agent found, or clean bill of health]
- Did the agent comment on quality/structure? [should be No]

**Input 2 (vulnerable scope):**
- Finding: [the vulnerability identified]
- Attack path: [was it concrete or vague?]

**Input 3 (distinct lens check):**
- Did the agent stay within its lens? [Yes/No]
- If No, what did it comment on that belongs to the producing agent? [details]

### FAIL Condition Self-Check
- Are any hooks window-dressing (file exists, non-empty only)? [should be No]
- Does the adversarial agent re-check the same criteria as the producing agent? [should be No]
```

---

## Step 7: Commit

Commit the following:
- `step-boundary-map.md`
- Updated skill files (all seven, with sentinel instructions added)
- `guardrails.sh` (all six hook functions)
- Updated harness script (with guardrail calls between every step)
- `adversarial-security-review.md` (or compliance/completeness variant)
- `guardrail-test-notes.md`

---

## Self-Check

- [ ] `step-boundary-map.md` committed before any hook code was written
- [ ] All seven skills write sentinel files with at least three meaningful, inspectable properties
- [ ] All six hook functions parse sentinel contents with `jq` and check at least three properties each — none are window-dressing (file-exists-only or non-empty-only checks)
- [ ] Harness halts on any hook failure with a clear message naming the failed property
- [ ] One adversarial review agent prompt written with a distinct lens (security, compliance, or completeness — not "quality")
- [ ] Adversarial agent has its own RTCC-structured prompt file, its own role, and an explicitly adversarial posture
- [ ] Adversarial agent does not re-check criteria the producing agent already covers
- [ ] Hook tests cover pass, fail, and missing-sentinel scenarios for at least three boundaries
- [ ] Adversarial agent tested on clean input, vulnerable input, and distinct-lens verification
- [ ] `guardrail-test-notes.md` documents all test results including the FAIL condition self-check