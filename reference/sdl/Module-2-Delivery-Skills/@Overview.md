# Module 2: Delivery Skills

*Estimated time: 20–28 hours*

---

## What This Module Covers

In Module 1, you built one delivery skill — `create-scope` — against a small, well-specified product (the Pomodoro kata). You learned the full EDD cycle on one command and established your Model Ladder baseline.

In Module 2, you build the remaining six commands that complete the delivery pipeline, and you stress-test all seven delivery skills against real engineering problems. Each command is paired with a kata from Appendix A — a specific coding challenge chosen because it exposes a particular failure mode in that command. Running against these katas is not a bonus step. It is how you find the gaps in your commands that the TeamPulse exercises will not expose.

---

## The Delivery Pipeline

The seven delivery skills form a connected workflow:

```
Feature & System Request
    ↓
Create Scope
    ↓           ↘
Create Architecture    Create UX
    ↓           ↗
Create Workstreams & Deliverables
    ↓
Plan Deliverable  →  Create Deliverable  →  Review Deliverable
```

Each command's output is the next command's input. Quality problems propagate downstream. A vague scope document produces a vague Architecture, which produces poorly-scoped Deliverables, which produces under-specified deliverable plans. A consistent theme in this module: when a downstream command produces bad output, the root cause is often upstream.

---

## What You Are Building

Exercises 6–10 follow the same structure: you receive a starter command stub with Role and Task defined but Context and Constraints intentionally empty. Your job is to fill them through EDD iteration.

Each exercise has two domains:
1. **TeamPulse** — the primary iteration domain. You build and refine your command against this well-specified enterprise product.
2. **A paired kata** — a stress-test domain chosen specifically because it exposes a failure mode that TeamPulse will not. Running your command against the kata is a required step at the end of each exercise, not optional.

---

## Kata Pairings

| Command | Paired Kata | What the Kata Exposes |
|---------|-------------|----------------------|
| `create-scope` | B4: Pomodoro *(from Module 1)* | Implicit non-functional requirements (drift correction, browser API dependencies) |
| `create-architecture` | B1: Conway's Game of Life | Generic state management vs. performance-critical double-buffering |
| `create-ux` | B3: Tic-Tac-Toe with Unbeatable AI | Multi-mode UI with different per-mode acceptance criteria |
| `decompose-to-deliverables` | B2: Snake with Replay System | Deliverable underspecification of complex interaction features |
| `plan-deliverable` | I1: Sorting Algorithm Visualizer | Generic "implement algorithm" vs. generator-pattern step-through execution |
| `create-deliverable` | I1: Sorting Algorithm Visualizer | Implementation that cannot pause mid-execution for animation |
| `review-deliverable` | I1: Sorting Algorithm Visualizer | Review that does not catch the missing pauseable execution model |

The final pipeline run (Exercise 11) uses Kata I2 (Blackjack with Strategy Coach) as an end-to-end stress test alongside the DevLog product description.

---

## Evaluations in Module 2

All Promptfoo configurations in Module 2 run against Haiku only. You learned the Model Ladder lesson in Module 1 — that prompt clarity affects which models can execute your instructions, and that cheaper models expose gaps that capable models silently fill. Now that you understand the delta, running both models on every command would double your evaluation costs without adding diagnostic value.

A prompt that passes Haiku is well-specified — Sonnet will also pass it. A prompt that fails Haiku tells you exactly which instruction is missing, which is the same diagnostic information the two-model comparison gave you in Module 1. The goal is prompts that work on Haiku; Haiku is the bar.

At the end of each exercise, you record a Model Ladder Checkpoint: your Haiku score, which gaps you closed, and which you deliberately accepted with reasoning. You can monitor your AI usage at [usage.improving.ai](https://usage.improving.ai).

---

## Prerequisites

Module 1 is complete. You have a working, load-bearing-audited `create-scope.md` with documented Model Ladder baseline (the two-model comparison done once in Module 1). Exercise 5 picks up from that command — not from a fresh starter stub.

Promptfoo runs through your existing CLI tools via the wrapper scripts set up in Exercise 3. No separate API key is needed.

---

## Exercises in This Module

- [Exercise 5: Create Scope](Exercise-05-Create-Scope.md) — Extend your Module 1 command against TeamPulse; establish its performance across domains
- [Exercise 6: Create Architecture](Exercise-06-Create-Architecture.md)
- [Exercise 7: Create UX](Exercise-07-Create-UX.md)
- [Exercise 8: Create Workstreams and Deliverables](Exercise-08-Decompose-to-Deliverables.md)
- [Exercise 9: Plan Deliverable](Exercise-09-Plan-Deliverable.md)
- [Exercise 10: Create Deliverable and Review Deliverable](Exercise-10-Create-and-Review-Deliverable.md)
- [Exercise 11: Full Delivery Pipeline Run](Exercise-11-Delivery-Pipeline-Run.md)

---

## What Done Looks Like

At the end of Module 2, you will have:
- Seven delivery skill files with completed Context and Constraints, committed with EDD documentation
- Promptfoo configurations for all seven delivery skills, with baseline + iteration records (all Haiku only)
- Load-bearing audit documentation for all seven delivery skills (if time-constrained, prioritize create-scope, decompose-to-deliverables, and create-deliverable)
- Kata stress test results for at least three delivery skills with documented pipeline failure observations with documented pipeline failure observations
- A documented upstream quality dependency trace: at least one case where a downstream failure was traced to an upstream command
- Model Ladder documentation for Module 1's `create-scope` (the two-model progression done once)
- DevLog pipeline run output files (all seven stages) and run notes
- Blackjack kata pipeline run output and comparison notes

---

## The Product Description

Use this product description for your initial work in Exercises 5–10. You may use additional or modified descriptions in Exercise 11.

---

### Product Description: TeamPulse — Team Health Check System

**System Request:** Build a lightweight team health check system that allows engineering managers to run anonymous, recurring pulse surveys with their teams. Engineers answer 5–7 questions on a weekly or bi-weekly schedule. Results are aggregated and displayed in a trend dashboard visible only to the manager. Individual responses remain anonymous — managers see team-level patterns, not individual attributions.

**Key requirements:**
- Engineers receive a notification (email or Slack) with a link to a brief survey form
- Survey form is mobile-accessible and completable in under 3 minutes
- Managers have a dashboard showing trend lines over time for each question, with comparisons to prior periods
- All responses are stored anonymously — no individual attribution in any view, including admin views
- Managers can configure: question set, frequency (weekly/bi-weekly), and team membership
- The system supports multiple managers with separate teams; no cross-team visibility

**Technical context:** The engineering organization is using a React frontend, a Node.js backend, and a PostgreSQL database. The team uses GitHub for version control and Jira for issue tracking. Authentication is via the company's existing SSO system (Entra ID / OIDC).

**Out of scope for V1:** ML-based sentiment analysis, comparison across teams, integration with HR systems, mobile native apps.
