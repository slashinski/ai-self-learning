# Module 1: EDD and RTCC Foundations

*Estimated time: 6–8 hours*

---

## What This Module Covers

Before you build a single prompt, you need two foundational disciplines. This module establishes both:

1. **EDD (Evaluation-Driven Development)** — defining success before building, so you can know whether your instructions are actually doing anything
2. **RTCC (Role, Task, Context, Constraints)** — the four-part prompt structure used throughout this program

You will apply both disciplines to your first delivery skill: `create-scope`. You are building something you will use in Module 2 and every module after. The domain is not throwaway practice material — it is the first piece of real tooling in your AI-assisted development workflow.

---

## Why This Module Exists

Most people who use AI tools follow the same pattern: write a prompt, get output, decide if it looks good, adjust if it doesn't. This is the "I know it when I see it" approach, and it has a consistent failure mode: you end up with prompts that produce output that looks good in isolation but does not consistently meet the actual criteria that matter.

EDD breaks this pattern. By defining success criteria first — in writing, by hand, before you see any AI output — you create a target. Then you close the gap between where the model starts and where you need it to be. The load-bearing audit ensures you don't add instructions that aren't doing real work.

By the end of this module, you will also have run the same prompt against two different models and measured the difference. That gap is not noise — it is a diagnostic instrument. The Model Ladder discipline, introduced in Exercise 4, turns that gap into specific prompt improvements.

**This is the only module where you run evaluations against two models.** The point is to learn the lesson once — that prompt clarity affects which models can execute your instructions, and that cheaper models expose gaps that capable models silently fill. Once you have seen this, you switch to a single model for all subsequent modules to conserve cost. You can monitor your AI usage at [usage.improving.ai](https://usage.improving.ai).

---

## The Domain: `create-scope` for the Pomodoro Kata

The product you will write scope document tests for in Exercise 1 is a **Pomodoro Timer with session analytics** — a well-scoped consumer application with clear surface requirements and several implied non-functional requirements that are not stated in the product description.

This domain was chosen deliberately. The Pomodoro kata has:
- A small, fully specified feature set that will not overwhelm a learner focused on EDD mechanics
- At least one implied non-functional requirement (timer drift correction) that a naive test file will miss — but a careful thinker will catch
- A visual analytics component (weekly heat map) that requires local storage and raises real UX questions

The command you build here — `create-scope.md` — is not a practice artifact. It is the first command in your delivery pipeline. You will carry it into Module 2 and stress-test it against more complex product descriptions.

---

## Exercises in This Module

- [Exercise 1: Writing Tests First](Exercise-01-Writing-Tests-First.md) — Write manual test cases for a scope document before any prompt exists
- [Exercise 2: RTCC Prompt Construction](Exercise-02-RTCC-Structure.md) — Build your first structured `create-scope` command and validate it against your tests
- [Exercise 3: Promptfoo Setup and Baseline](Exercise-03-Promptfoo-Setup.md) — Install Promptfoo, configure multi-model evaluation, and establish your baseline scores on both Sonnet and Haiku
- [Exercise 4: The Load-Bearing Audit](Exercise-04-Load-Bearing-Audit.md) — Prove every instruction earns its place, then run the Model Ladder audit

---

## Before You Start

Make sure you have:
- Your AI tool (Windsurf, Claude Code, or GitHub Copilot) installed and working
- Node.js installed (you will need it for Promptfoo in Exercise 3)
- A personal GitHub repository ready to receive committed work
- About 90 minutes of uninterrupted time for Exercise 1

---

## What Done Looks Like

At the end of Module 1, you will have:
- `create-scope-tests.md` — a manual test file with at least 5 entries, committed before any prompt
- `create-scope.md` — an RTCC-structured scope document command that passes your test criteria on Sonnet
- `create-scope-promptfoo.yaml` — a working Promptfoo configuration running against both Sonnet and Haiku, with baseline results for both
- A load-bearing audit document showing which instructions were tested and which (if any) were removed
- A Model Ladder baseline: the Sonnet score, the Haiku score, the delta, and your first hypothesis about what the delta means

All five artifacts committed to your repository, in the correct order (test file first).

---

## Stage 3 Certification Readiness

**Module 1 completion produces all three artifacts required for Stage 3 certification:**
- **Evaluation Framework Documented:** Your `create-scope-tests.md` with 5+ evaluation criteria
- **Quantified Improvement Evidence:** Your Exercise 4 iteration record with before/after metrics
- **Reusable Task Library:** Your git repository with `create-scope.md`, test files, and Promptfoo configs with version history

You can submit your portfolio to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx) now, or continue to Modules 2-4 for deeper practice before submitting. Either is valid.
