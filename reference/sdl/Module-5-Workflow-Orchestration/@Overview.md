# Module 5: Workflow Orchestration

*Estimated time: 12-16 hours*

---

## What This Module Covers

Module 5 is where your individual delivery skills become an automated workflow. In Module 2, you ran the 7-step delivery pipeline by hand — pasting each command's output into the next command's input. In Module 3, you built a 2-step governed flow with a hook checkpoint. Module 5 takes both concepts to their Stage 4 conclusion: a shell-script harness that executes the full pipeline end-to-end, with guardrails between every step, human punch-out points, and end-to-end success rate measurement.

This is the single biggest shift in the program. Everything before this was about building skills. This module is about building the infrastructure around them.

---

## Why This Module Exists

Stage 4 certification requires an **automated harness** — a script that executes the workflow end-to-end without a human typing each step. If a human has to type the command for each step, the human IS the workflow, which is Stage 2 — not Stage 4.

This module teaches you to build that harness using shell scripting. The harness calls the Devin CLI to execute your delivery skills in sequence, passes outputs between steps, fires guardrails, handles failures, and logs everything. Your delivery skills are the intelligence; the harness is the orchestration.

---

## The Shift from Module 2

| Module 2 (Pipeline Run) | Module 5 (Workflow Orchestration) |
|--------------------------|-----------------------------------|
| Human runs each command | Shell script runs each command |
| Human reads output and decides to continue | Harness checks guardrails and decides automatically |
| Human catches errors by reading | Harness catches errors via hooks and sentinel files |
| No audit trail | Per-step logging with model, tokens, cost |
| Per-step quality only | End-to-end success rate measurement |

---

## Prerequisites

- Modules 1-4 complete. You have seven working delivery skills committed to your repository.
- Stage 3 certification submitted or ready to submit.
- The Devin CLI installed and authenticated (`devin --version` works).
- Basic shell scripting familiarity (bash or zsh). You will be writing shell scripts, not AI prompts. The harness is code.

---

## Tool Choice: Devin CLI

This module's examples use the **Devin CLI** for programmatic invocation of AI tools. The Devin CLI supports:
- `devin run --prompt-file <skill.md> --input <input.md> --output-format json` — runs a skill and returns structured output
- Session logs with per-step token and cost data (stored in `~/.local/share/devin/cli/sessions.db`)
- `--output-format json` for machine-readable responses

If you use a different tool (Claude Code, GitHub Copilot), adapt the harness to your tool's CLI invocation path. The governance concepts are tool-independent; the harness implementation is tool-specific.

---

## Exercises in This Module

- [Exercise 18: Building the Harness](Exercise-18-Building-the-Harness.md) — Write a shell script that runs the 7-step delivery pipeline end-to-end
- [Exercise 19: Guardrails Between Steps](Exercise-19-Guardrails.md) — Add deterministic hooks and adversarial review agents between every step
- [Exercise 20: Punch-Out Points and Bypass Testing](Exercise-20-Punch-Out-Points.md) — Define and test human evacuation points
- [Exercise 21: End-to-End Success Rate](Exercise-21-End-to-End-Success-Rate.md) — Measure the composite success rate across multiple pipeline runs

---

## What Done Looks Like

At the end of Module 5, you will have:
- A shell-script harness that runs the full 7-step delivery pipeline without manual intervention
- Guardrails (deterministic hooks + adversarial review agents) between every step
- At least 2 punch-out points with documented bypass testing
- An end-to-end success rate report from 10 pipeline runs
- All artifacts committed to your repository

These are four of the five Stage 4 certification artifacts. Module 6 covers the fifth (audit trail) and portfolio assembly.