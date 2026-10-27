# Exercise 18: Building the Harness

*Estimated time: 3–4 hours*
*Prerequisites: Modules 1–4 complete — your seven delivery skills are committed and EDD-validated. The Devin CLI is installed and authenticated (`devin --version` works). Basic bash scripting familiarity.*

---

## Goal

Write a bash script that runs the full 7-step delivery pipeline end-to-end without manual intervention. The harness calls the Devin CLI to execute each delivery skill in sequence, passes outputs between steps, and logs per-step metadata. This exercise builds the skeleton — no guardrails, no hooks, no go/no-go decisions between steps. Those come in Exercise 19. Right now the goal is simple: the pipeline runs from start to finish, one command, and every output file lands on disk.

---

## Background: Why a Harness

In Module 2 (Exercise 11) you ran the delivery pipeline by hand. You pasted each command's output into the next command's input, read every output, and decided whether to continue. That is a human-driven pipeline — Stage 2 behavior. A human IS the workflow.

A harness replaces the human as the orchestrator. The shell script calls each skill via the Devin CLI, captures the output, and feeds it to the next step. Your delivery skills remain the intelligence — the harness is pure plumbing. This is the foundational shift of Module 5: you are building infrastructure around your skills, not improving the skills themselves.

The harness you build here is intentionally bare. It does not check output quality between steps. It does not handle failures gracefully. It does not provide punch-out points. It runs the pipeline straight through, logs what happened, and stops. Every limitation is deliberate — Exercise 19 adds guardrails, Exercise 20 adds punch-out points, Exercise 21 measures success rate. Your job in this exercise is to make the pipeline run.

---

## Step 1: Verify Prerequisites and Plan the Directory Layout (15 minutes)

Confirm your environment is ready:

```bash
devin --version
```

If the Devin CLI is not installed or authenticated, stop here and resolve that before proceeding. The harness depends on it entirely.

Your seven delivery skills should be committed as `.md` files in your repository from Modules 1–2:

| # | Skill File | Output File | Input |
|---|-----------|-------------|-------|
| 1 | `create-scope.md` | `scope.md` | Product description |
| 2 | `create-architecture.md` | `architecture.md` | `scope.md` |
| 3 | `create-ux.md` | `ux.md` | `scope.md` |
| 4 | `decompose-to-deliverables.md` | `deliverables.md` | `scope.md` + `architecture.md` + `ux.md` |
| 5 | `plan-deliverable.md` | `plan.md` | One deliverable from `deliverables.md` |
| 6 | `create-deliverable.md` | `deliverable-impl.md` | `plan.md` + selected deliverable |
| 7 | `review-deliverable.md` | `review.md` | `deliverable-impl.md` + `plan.md` |

Decide on a working directory for pipeline runs. Each run should produce its outputs in an isolated directory so runs do not clobber each other:

```
pipeline-runs/
  run-YYYYMMDD-HHMMSS/
    input/
      product-description.md
    output/
      scope.md
      architecture.md
      ux.md
      deliverables.md
      plan.md
      deliverable-impl.md
      review.md
    logs/
      pipeline.log
```

Create the directory structure now. Place a product description in `input/product-description.md` — use the DevLog description from Exercise 11 or any product description you have not iterated against.

---

## Step 2: Write the Harness Skeleton (45 minutes)

Create `harness.sh` in your repository. This is the main script. It defines the pipeline as an ordered array of steps and executes them sequentially.

```bash
#!/usr/bin/env bash
#
# harness.sh — Delivery pipeline harness (skeleton, no guardrails)
#
# Usage: ./harness.sh <run-dir>
#   <run-dir>  Directory containing input/ and output/ subdirectories
#
# The run directory must contain:
#   input/product-description.md  — the product description to scope
#
# Outputs are written to <run-dir>/output/
# Logs are written to <run-dir>/logs/pipeline.log
#

set -euo pipefail

# --- Configuration -----------------------------------------------------------

RUN_DIR="${1:?Usage: $0 <run-dir>}"
SKILLS_DIR="${SKILLS_DIR:-./skills}"
OUTPUT_DIR="${RUN_DIR}/output"
INPUT_DIR="${RUN_DIR}/input"
LOG_DIR="${RUN_DIR}/logs"
LOG_FILE="${LOG_DIR}/pipeline.log"

# Each step: skill_file | output_file | input_files (space-separated)
# Input files are relative to OUTPUT_DIR unless prefixed with input/
declare -a STEPS=(
  "create-scope.md|scope.md|input/product-description.md"
  "create-architecture.md|architecture.md|scope.md"
  "create-ux.md|ux.md|scope.md"
  "decompose-to-deliverables.md|deliverables.md|scope.md architecture.md ux.md"
  "plan-deliverable.md|plan.md|deliverables.md"
  "create-deliverable.md|deliverable-impl.md|plan.md deliverables.md"
  "review-deliverable.md|review.md|deliverable-impl.md plan.md"
)

# --- Setup -------------------------------------------------------------------

mkdir -p "${OUTPUT_DIR}" "${LOG_DIR}"

log() {
  local timestamp
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "[${timestamp}] $*" | tee -a "${LOG_FILE}"
}

# --- Execute Pipeline --------------------------------------------------------

log "PIPELINE START — run dir: ${RUN_DIR}"

for step in "${STEPS[@]}"; do
  # Parse the step definition
  IFS='|' read -r skill_file output_file input_files <<< "${step}"

  skill_path="${SKILLS_DIR}/${skill_file}"
  output_path="${OUTPUT_DIR}/${output_file}"

  # Resolve input file paths
  input_args=()
  for f in ${input_files}; do
    if [[ "${f}" == input/* ]]; then
      input_args+=("${RUN_DIR}/${f}")
    else
      input_args+=("${OUTPUT_DIR}/${f}")
    fi
  done

  log "STEP START — ${skill_file} → ${output_file}"

  # Build the Devin CLI command
  # For multiple inputs, concatenate them into a single input file
  if [[ ${#input_args[@]} -eq 1 ]]; then
    input_file="${input_args[0]}"
  else
    # Merge multiple inputs into a temporary combined file
    input_file="${OUTPUT_DIR}/.combined-input.md"
    : > "${input_file}"
    for f in "${input_args[@]}"; do
      echo "--- Source: $(basename "${f}") ---" >> "${input_file}"
      cat "${f}" >> "${input_file}"
      echo "" >> "${input_file}"
    done
  fi

  # Execute the skill via Devin CLI
  if devin run \
    --prompt-file "${skill_path}" \
    --input "${input_file}" \
    --output-format json \
    > "${output_path}.raw" 2> "${LOG_DIR}/${skill_file%.md}.stderr"; then

    # Extract the response content from JSON output
    # The Devin CLI returns JSON with a "response" field containing the output
    python3 -c "
import json, sys
with open('${output_path}.raw') as f:
    data = json.load(f)
    print(data.get('response', data.get('output', '')))
" > "${output_path}" 2>> "${LOG_FILE}" || cp "${output_path}.raw" "${output_path}"

    log "STEP END — ${skill_file} → ${output_file} [OK]"
  else
    log "STEP FAILED — ${skill_file} (exit code: $?)"
    log "PIPELINE ABORTED at step: ${skill_file}"
    exit 1
  fi
done

log "PIPELINE COMPLETE — all 7 steps executed"
log "Outputs in: ${OUTPUT_DIR}"
```

Read through the script before running it. Understand what each section does:

- **Configuration:** The `STEPS` array is the pipeline definition. Each entry is `skill_file|output_file|input_files`. This is the single source of truth for the pipeline sequence — change the array, change the pipeline.
- **Setup:** Creates output and log directories. The `log()` function writes timestamped entries to both stdout and the log file.
- **Execution:** Loops through steps, resolves input paths (handling the `input/` prefix for the initial product description), merges multiple inputs when a step needs more than one, calls the Devin CLI, and parses the JSON response.
- **Error handling:** `set -euo pipefail` ensures the script exits on any error. If a Devin CLI call fails, the pipeline aborts immediately. This is the skeleton behavior — Exercise 19 replaces this with guardrail-aware handling.

---

## Step 3: Handle Multi-Input Steps Correctly (30 minutes)

Steps 4 and 7 in the pipeline require multiple input files. Step 4 (`decompose-to-deliverables`) takes scope, architecture, and UX. Step 7 (`review-deliverable`) takes the deliverable implementation and the plan.

The skeleton above handles this by concatenating inputs into a temporary combined file with source markers. This works, but it is crude — your skill files may expect inputs in a specific structure. Check your `decompose-to-deliverables.md` and `review-deliverable.md` skills:

- Do they specify an input format? (e.g., "the input will contain a scope document followed by an architecture document")
- Do they expect inputs as separate files or a single combined document?
- Does the order of inputs matter?

If your skills expect structured input, adjust the combined-input logic. For example, if `decompose-to-deliverables.md` expects clearly labeled sections:

```bash
build_combined_input() {
  local output_file="$1"
  shift
  : > "${output_file}"
  for f in "$@"; do
    local label
    label="$(basename "${f}" .md)"
    echo "## ${label^^}" >> "${output_file}"
    echo "" >> "${output_file}"
    cat "${f}" >> "${output_file}"
    echo "" >> "${output_file}"
  done
}
```

If your Devin CLI version supports multiple `--input` flags, use that instead of concatenation:

```bash
# If the CLI supports repeated --input flags:
devin run \
  --prompt-file "${skill_path}" \
  --input "${input_args[0]}" \
  --input "${input_args[1]}" \
  --input "${input_args[2]}" \
  --output-format json
```

Check `devin run --help` to see what your version supports. The correct approach is whatever your CLI and your skills expect — do not assume. Test with a single multi-input step before running the full pipeline.

---

## Step 4: Make the Script Executable and Do a Dry Run (15 minutes)

```bash
chmod +x harness.sh
```

Before running the full pipeline, do a dry run to validate the script structure. Add a `--dry-run` flag that prints what each step would do without calling the Devin CLI:

```bash
DRY_RUN="${DRY_RUN:-false}"

# Inside the execution loop, before the devin run call:
if [[ "${DRY_RUN}" == "true" ]]; then
  log "DRY RUN — would execute: devin run --prompt-file ${skill_path} --input ${input_file} --output-format json"
  log "  → output: ${output_path}"
  continue
fi
```

Run the dry run:

```bash
DRY_RUN=true ./harness.sh pipeline-runs/run-test
```

Verify the log output shows all 7 steps in the correct order with the correct input and output paths. Check that input file resolution works — `input/product-description.md` for step 1, `output/scope.md` for steps 2 and 3, all three for step 4, etc.

Fix any path resolution issues before proceeding. The dry run exists to catch these cheaply.

---

## Step 5: Run the Full Pipeline (60 minutes)

Run the harness against your product description:

```bash
./harness.sh pipeline-runs/run-$(date +%Y%m%d-%H%M%S)
```

This will take 10–20 minutes depending on model response times. Watch the log output. Each step should log START, then END with `[OK]` or FAILED.

If a step fails:

1. Read the stderr log for that step: `cat <run-dir>/logs/<skill-name>.stderr`
2. Check that the input file exists and is non-empty: `wc -l <run-dir>/output/<input-file>`
3. Check that the skill file exists: `ls -la skills/<skill-file>`
4. Fix the issue and re-run. The script creates a new run directory each time, so failed runs do not clobber successful ones.

Common failures:
- **Skill file not found:** Check `SKILLS_DIR` — it defaults to `./skills` but may need to point elsewhere depending on your repo layout.
- **Empty input file:** The previous step produced no output. Check that step's stderr log.
- **JSON parse error:** The Devin CLI returned an unexpected format. Inspect the `.raw` file to see what was returned and adjust the parsing logic.
- **Devin CLI authentication:** Run `devin auth status` or equivalent to verify your session is valid.

Do not change any delivery skill during this exercise. If a skill produces poor output, that is expected — the harness has no guardrails. The point is that the pipeline runs, not that every output is high quality. Quality measurement comes in Exercise 21.

---

## Step 6: Verify All Outputs and Log (20 minutes)

After a successful run, verify all seven output files exist and are non-empty:

```bash
RUN_DIR="pipeline-runs/run-YYYYMMDD-HHMMSS"  # use your actual run dir

for f in scope.md architecture.md ux.md deliverables.md plan.md deliverable-impl.md review.md; do
  if [[ -s "${RUN_DIR}/output/${f}" ]]; then
    echo "✓ ${f} — $(wc -l < "${RUN_DIR}/output/${f}") lines, $(wc -c < "${RUN_DIR}/output/${f}") bytes"
  else
    echo "✗ ${f} — MISSING or EMPTY"
  fi
done
```

Read the pipeline log end-to-end:

```bash
cat "${RUN_DIR}/logs/pipeline.log"
```

Confirm:
- All 7 steps logged START and END
- No step logged FAILED
- The final line says `PIPELINE COMPLETE`
- Timestamps show reasonable execution times per step (not zero, not hours)

Create `harness-run-report.md` in the run directory:

```markdown
## Harness Run Report — [date]

### Run Configuration
- Run directory: [path]
- Product description: [name]
- Skills directory: [path]

### Pipeline Execution Summary
| Step | Skill | Output | Status | Notes |
|------|-------|--------|--------|-------|
| 1 | create-scope | scope.md | OK | |
| 2 | create-architecture | architecture.md | OK | |
| 3 | create-ux | ux.md | OK | |
| 4 | decompose-to-deliverables | deliverables.md | OK | |
| 5 | plan-deliverable | plan.md | OK | |
| 6 | create-deliverable | deliverable-impl.md | OK | |
| 7 | review-deliverable | review.md | OK | |

### Output Quality (cursory — full quality measurement is Exercise 21)
- scope.md: [1–2 sentences on whether it looks reasonable]
- architecture.md: [1–2 sentences]
- review.md: [1–2 sentences]

### Issues Encountered
[Any path resolution problems, CLI errors, input format mismatches, and how you fixed them]

### What This Harness Does NOT Do (yet)
- No guardrails between steps (Exercise 19)
- No go/no-go decisions (Exercise 19)
- No punch-out points for human review (Exercise 20)
- No end-to-end success rate measurement (Exercise 21)
- No retry logic for transient failures
- No token/cost tracking per step
```

---

## Step 7: Make the Harness Reusable (20 minutes)

Your harness should work for any product description, not just the one you tested with. Parameterize the remaining hard-coded values:

1. **Skills directory:** Already configurable via `SKILLS_DIR` environment variable. Verify it works when set explicitly:
   ```bash
   SKILLS_DIR=./my-repo/delivery-skills ./harness.sh pipeline-runs/run-test2
   ```

2. **Run directory naming:** The script already accepts the run directory as an argument. Add a convenience wrapper that auto-generates the timestamped directory:
   ```bash
   # run-pipeline.sh — convenience wrapper
   #!/usr/bin/env bash
   RUN_DIR="pipeline-runs/run-$(date +%Y%m%d-%H%M%S)"
   mkdir -p "${RUN_DIR}/input"
   cp "$1" "${RUN_DIR}/input/product-description.md"
   ./harness.sh "${RUN_DIR}"
   echo "Run complete: ${RUN_DIR}"
   ```

3. **Clean up temporary files:** The `.combined-input.md` and `.raw` files are intermediate artifacts. Add cleanup at the end of the script:
   ```bash
   # After pipeline completion
   rm -f "${OUTPUT_DIR}/.combined-input.md" "${OUTPUT_DIR}"/*.raw
   log "Cleaned up intermediate files"
   ```

4. **Exit codes:** The script exits 1 on any step failure and 0 on success. Verify this works:
   ```bash
   ./harness.sh pipeline-runs/run-test && echo "Exit 0 — success" || echo "Non-zero exit — failure"
   ```

Test the reusable harness with a different product description (the Blackjack kata from Exercise 11 works well). Confirm it produces all seven outputs without code changes.

---

## Step 8: Commit

Commit `harness.sh`, `run-pipeline.sh` (if you created the wrapper), the run directory outputs, the pipeline log, and `harness-run-report.md`.

```bash
git add harness.sh run-pipeline.sh pipeline-runs/ 
git commit -m "Exercise 18: delivery pipeline harness skeleton with Devin CLI"
```

---

## Self-Check

- [ ] `harness.sh` runs the full 7-step pipeline with a single command
- [ ] All seven output files are produced and non-empty for at least one run
- [ ] Pipeline log shows all 7 steps with START/END timestamps
- [ ] Multi-input steps (decompose-to-deliverables, review-deliverable) receive correct combined inputs
- [ ] Dry run mode works and shows correct step ordering and path resolution
- [ ] Harness is parameterized — works with different product descriptions without code changes
- [ ] `harness-run-report.md` documents the run, including any issues encountered
- [ ] No delivery skills were modified during this exercise
- [ ] You understand what the harness does NOT do yet (guardrails, punch-out points, success rate) and can articulate why each is deferred