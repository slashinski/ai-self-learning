# Exercise 14: Hooks and Sentinel Files

*Estimated time: 3–4 hours*
*Prerequisites: Exercise 13 complete*

---

## Goal

Build a sentinel file schema for one of your delivery skills, and write a hook that reads the sentinel file and makes a deterministic pass/fail decision. Understand what hooks are good at, what they are not for, and how they complement Promptfoo.

---

## Background: What a Hook Is

A **hook** is a shell command that runs deterministically in response to an IDE event — a tool call, a file write, a command completion. Hooks are code, not AI. They run every time their trigger fires and produce consistent, predictable behavior. This is their value: you cannot fully predict what an AI will output, but you can predict exactly what a hook will do given any particular input.

Hooks give you a deterministic decision point inside an otherwise non-deterministic workflow. This is the safety layer that makes automation governable.

**What hooks are good at:** Inspecting structured data for the presence of required fields, checking length bounds, verifying that required sections exist, halting a workflow if a minimum bar is not met.

**What hooks are not for:** Replacing Promptfoo. A hook cannot evaluate whether a scope document is "good" — it can only check whether it contains the required sections. Quality validation is Promptfoo's job. Checkpoint enforcement is the hook's job.

---

## Step 1: Hello World Hook (30 minutes)

Before building anything meaningful, verify that your tool's hook mechanism works.

Consult your tool's documentation for how to configure hooks. In Claude Code, hooks are configured in `.claude/settings.json`. In Windsurf and GitHub Copilot, consult the respective documentation for hook or plugin configuration.

Build a "hello world" hook: when any file is written, log the filename and a timestamp to a local file called `hook-log.txt`.

Test it: write a file, verify `hook-log.txt` was updated. If this does not work, do not proceed — debug the hook setup before building the sentinel file logic.

---

## Step 2: Sentinel File Schema Design (45 minutes)

A **sentinel file** is a structured output file that a prompt is explicitly instructed to write when it completes. The act of writing the file is a tool call — which a hook can catch. This gives you an inspection point between two AI steps.

Choose `create-scope.md` as your sentinel file target. Design the sentinel file schema before writing any code.

Answer these questions:
1. What 3–5 properties of scope document output are most critical and easiest to inspect deterministically? (Think: required sections present? Length within expected bounds? Key fields populated?)
2. What format should the sentinel file use? (JSON is recommended — easy to parse in a shell script)
3. What should the hook do if a required property is missing? (Options: log and halt, log and alert, log and continue with warning)
4. What should the hook do if a required property is present but out of bounds? (Same options)

Write the schema design in a file called `create-scope-sentinel-schema.md`:

```markdown
## Scope Document Sentinel File Schema

### Purpose
[What this sentinel file is for and what the hook does with it]

### Schema
```json
{
  "sections_present": ["overview", "requirements", "out_of_scope", "open_questions"],
  "word_count": 500,
  "has_measurable_success_criteria": true,
  "has_explicit_out_of_scope": true
}
```

### Required Properties
| Property | Type | Required Value | On Failure |
|----------|------|---------------|------------|
| sections_present | array | must include: [list] | halt workflow |
| word_count | number | between X and Y | warn |
| ... | ... | ... | ... |

### What This Does NOT Validate
[Describe what this sentinel cannot catch, and where Promptfoo should be used instead]
```

Commit `create-scope-sentinel-schema.md` before writing any code.

---

## Step 3: Modify the Command to Write the Sentinel File (30 minutes)

Add a Constraint to `create-scope.md` instructing it to write a sentinel file. The instruction must:
- Specify the exact filename and location
- Specify the exact JSON schema
- Make this a mandatory constraint (always required, regardless of input)

Example constraint:
```
After producing the scope document, write a file called `scope-sentinel.json` in the same directory. The file must contain:
- `sections_present`: an array of the section names that appear in the scope document output
- `word_count`: the approximate word count of the scope document body
- `has_measurable_success_criteria`: true if the scope document contains at least one measurable success criterion with a specific numeric or behavioral target; false otherwise
- `has_explicit_out_of_scope`: true if the scope document contains an explicit out-of-scope section; false otherwise
```

Test: run `create-scope.md` and verify that `scope-sentinel.json` is written with the correct structure.

---

## Step 4: Write the Hook Script (45 minutes)

Write a shell script that:
1. Reads `scope-sentinel.json`
2. Checks each required property against your schema
3. Logs the result to `hook-log.txt`
4. If any required property fails: exits with a non-zero status and prints a clear failure message naming the specific property that failed
5. If all required properties pass: exits with 0 and prints a pass message

```bash
#!/bin/bash
# scope-sentinel-hook.sh
# Reads scope-sentinel.json and enforces minimum quality bar for scope document output.

SENTINEL_FILE="scope-sentinel.json"
LOG_FILE="hook-log.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ ! -f "$SENTINEL_FILE" ]; then
  echo "[$TIMESTAMP] FAIL: scope-sentinel.json not found. scope document command may not have completed." | tee -a "$LOG_FILE"
  exit 1
fi

# Read properties using jq (install if not present: brew install jq)
HAS_OUT_OF_SCOPE=$(jq -r '.has_explicit_out_of_scope' "$SENTINEL_FILE")
HAS_SUCCESS_CRITERIA=$(jq -r '.has_measurable_success_criteria' "$SENTINEL_FILE")

if [ "$HAS_OUT_OF_SCOPE" != "true" ]; then
  echo "[$TIMESTAMP] FAIL: scope document does not contain an explicit out-of-scope section." | tee -a "$LOG_FILE"
  exit 1
fi

if [ "$HAS_SUCCESS_CRITERIA" != "true" ]; then
  echo "[$TIMESTAMP] FAIL: scope document does not contain measurable success criteria." | tee -a "$LOG_FILE"
  exit 1
fi

echo "[$TIMESTAMP] PASS: scope document sentinel checks passed." | tee -a "$LOG_FILE"
exit 0
```

Customize this template to match your actual schema.

Connect the hook to your tool's hook configuration so it fires when `scope-sentinel.json` is written.

---

## Step 5: Test the Hook (30 minutes)

Test all three scenarios:
1. **Pass:** Run `create-scope.md` on a good input, verify the hook fires and exits 0
2. **Fail:** Craft an input that produces a scope document missing a required property. Verify the hook catches it and exits non-zero with a clear message
3. **Missing sentinel:** Remove `scope-sentinel.json` and run the hook manually. Verify it handles the missing file case

Record results in `hook-test-notes.md`:
```markdown
## Hook Test Results — [date]

**Test 1 (pass):** [what input, what sentinel values, hook exit code]
**Test 2 (fail):** [what input, what specifically failed, hook message]
**Test 3 (missing file):** [hook behavior]

**What the hook is good at detecting:** [specific]
**What failure modes it misses:** [specific — these should go in Promptfoo instead]
```

---

## Step 6: Commit

Commit `create-scope-sentinel-schema.md`, the updated `create-scope.md`, the hook script, and `hook-test-notes.md`.

---

## Self-Check

- [ ] `create-scope-sentinel-schema.md` committed before any code was written
- [ ] Sentinel file is written by the command (not manually) when the command runs
- [ ] Hook script correctly handles pass, fail, and missing-file cases
- [ ] Hook fires automatically (not manually) via tool configuration
- [ ] `hook-test-notes.md` documents what the hook can and cannot detect
