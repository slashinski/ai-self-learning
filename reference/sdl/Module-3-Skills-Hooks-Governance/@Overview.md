# Module 3: Skills, Hooks, and Governed Flows

*Estimated time: 10–14 hours*

---

## What This Module Covers

Modules 1–2 were entirely about commands — prompts you invoke explicitly, at a time you choose, with full control over when they run. Module 3 introduces the next steps on the automation spectrum:

```
Commands            — you invoke explicitly, full control
    ↓
Skills              — you delegate invocation to the model
    ↓
Hooks + Sentinel    — deterministic checkpoints in non-deterministic flows
Files
    ↓
Governed Workflows  — automated multi-step chains with guardrails
```

The key principle: move one step down this spectrum only when you have sufficient trust in the step above. Specifically:
- Move from Commands to Skills only when your team has explicit consensus about when the command should run
- Move from Skills to Hooks only when you can define deterministic rules for whether to continue
- Never automate a step you cannot govern

---

## Prerequisites

Modules 1–2 complete. You have seven working delivery skill files (`create-scope.md`, `create-architecture.md`, `create-ux.md`, `decompose-to-deliverables.md`, `plan-deliverable.md`, `create-deliverable.md`, `review-deliverable.md`) with Promptfoo configurations, all committed to your repository.

---

## Tool Compatibility

Module 3 exercises depend on tool-specific features that vary across the three supported AI tools. Review this matrix before starting:

| Feature | Claude Code | Windsurf | GitHub Copilot |
|---------|------------|----------|----------------|
| Skills (model-invoked) | Full | Partial | Partial |
| Hooks (file-write events) | Full | Not native | Not native |
| Hook-triggered actions | Limited | Not available | Not available |

**If your primary tool does not support hooks**, you have two options:
1. **Install Claude Code** (free with a Claude subscription) for Module 3 exercises
2. **Use standalone shell scripts** with a file-watcher (`fswatch` on macOS, `entr` on Linux) to simulate hook behavior. The governance concepts are tool-independent; the implementation is tool-specific.

The exercise instructions are written for Claude Code as the primary example. If you use a different tool, adapt the implementation details to your tool's capabilities while preserving the governance patterns.

---

## Why This Order

A command only runs when you run it. If the output is wrong, only you are affected. You learn, iterate, and improve — that is the EDD discipline you have been practicing.

A skill runs when the model decides to run it. If the model invokes the skill at the wrong time, it may produce output that downstream processes act on before anyone reviews it. And because different people on a team may have different expectations about when the skill should trigger, premature shared skills create invisible disagreements about workflow.

**Team consensus** — before a command becomes a skill — means the team has agreed in writing, with test cases, on:
1. Exactly what inputs should trigger the skill
2. Exactly what the skill should do when triggered
3. Exactly what the skill should NOT do in edge cases
4. How to verify the skill triggered correctly

Until that consensus exists, individual commands are not just safer — they are more honest.

---

## Exercises in This Module

- [Exercise 12: Commands vs. Skills](Exercise-12-Commands-vs-Skills.md) — Understanding the difference and when each is appropriate
- [Exercise 13: Building a Skill](Exercise-13-Building-a-Skill.md) — Convert a command to a skill with invocation-aware EDD testing
- [Exercise 14: Hooks and Sentinel Files](Exercise-14-Hooks-and-Sentinel-Files.md) — Deterministic checkpoints in non-deterministic workflows
- [Exercise 15: Governed Two-Step Flow](Exercise-15-Governed-Flow.md) — Connect two commands with a hook-mediated sentinel checkpoint

---

## What Done Looks Like

At the end of Module 3, you will have:
- A written analysis of two of your existing commands: skill-readiness assessment and invocation boundary analysis
- One skill file converted from a command, with invocation test cases (positive, negative, and quality)
- A sentinel file schema for at least one command, designed before being built
- A hook script that reads the sentinel file and makes a deterministic pass/fail decision
- A two-step governed flow built and tested across all four scenarios
- An automation spectrum assessment for your full artifact set
- A governance explanation paragraph written for a non-technical manager
