# ai-self-learning

A personal workspace for learning evaluation-driven development (EDD) with AI skills. Each skill is written against evaluation criteria (EC) that are authored by hand before the skill exists, then iterated until it meets the pass threshold. Every run is logged so the history of changes and scores can be read back.

## How the work is done

1. Write the EC for a skill by hand in `modules/module-N/exercise-N/<skill>-tests.md`. Deterministic checks (regex, headings, counts) come first. Judged criteria are used only where a regex cannot decide.
2. Commit the EC file before the skill exists. Commit order is EC, then skill, then results, each in its own commit.
3. Build the skill at `skills/<name>/SKILL.md` with `disable-model-invocation: true`.
4. Run the baseline (the bare prompt, no skill), then iterate. Each iteration changes one thing and records the hypothesis, the change, the baseline and resulting scores as percentages, and one line of reasoning.
5. The pass bar is 95% of criteria met across all test cases. Models are limited to Sonnet and Haiku. Every run logs model, input tokens, output tokens, and cost.

Vocabulary: EC is the quality bar for a skill's output. AC is the product artifact a skill produces. Context is why something is needed. Constraints are how it has to be built.

## Iteration history

Every evaluation run is appended to `modules/module-N/exercise-N/results/<skill>-run.log.md`. The log is the record of truth for scores. Nothing in it is edited by hand except the reasoning line, which `--reasoning-last` fills in after the run.

Each run is a level-two heading followed by bullet fields:

    ## Run 001
    - Timestamp: <ISO-style local time>
    - Mode: baseline | skill
    - Model: sonnet | haiku
    - Hypothesis: <what the change is expected to fix>
    - Change: <the one change made since the previous run>
    - Baseline score: <percent, one decimal>
    - Previous score: <percent or ->
    - Score: <percent> (<met> of <total> criteria; threshold 95%)
    - Reasoning: <one line, or (pending)>
    - Usage: <input tokens, output tokens, cost in USD>
    - Skill: <skill name or ->
    - Previous PRD version: <version or ->
    - Duration: <seconds>
    - PRD version: <version or ->
    - PRD changes: <changelog text>
    - Deterministic: <passed>/<total> passed
    - Judge: <passed>/<total> passed, average score <n> | skipped | not run
    - Overall result: PASS | FAIL

Runs are numbered in order by counting existing `## Run N` headings, so the log reads as baseline (Red), then iterations (Green and Refactor). A reader can list every run with `grep "^## Run" <log>` and every score with `grep "^- Score:" <log>`.

## Layout

```
skills/<name>/SKILL.md       skills under evaluation
modules/module-N/exercise-N/ EC files, run logs, and results for each exercise
scripts/eval.py              evaluation runner (deterministic checks, LLM judge, run logging)
schemas/                     templates for test cases, iteration records, and field notes
understanding/               written answers to comprehension checks
adversarial-agents/          review agents built after the evaluation loop works
evaluations/                 evaluation scripts, committed with the skill they test
```

## Stage 3 grader artifacts

| Grader artifact | Files |
|---|---|
| Skill | `skills/<name>/SKILL.md` |
| Evaluation criteria and scripts | `modules/module-N/exercise-N/*-tests.md`, `scripts/eval.py` |
| Iteration log and audit | `modules/module-N/exercise-N/results/*-run.log.md`, `*-load-bearing-audit.md` |

Pass threshold: 95% of criteria met across all test cases, deterministic checks and judged criteria counted together.

## Stage 4 grader artifacts

Not started. The Stage 4 artifacts are a workflow definition, guardrails, punch-out evidence, an end-to-end success rate, and an audit trail.

## Rerun an evaluation

    python3 scripts/eval.py <skill> <tests.md> --check-ec
    python3 scripts/eval.py <skill> <tests.md> --baseline --bare <prompt> --model haiku
    python3 scripts/eval.py <skill> <tests.md> --skill --hypothesis "..." --change "..." --model haiku
    python3 scripts/eval.py <skill> <tests.md> --reasoning-last "one line after seeing the result"
