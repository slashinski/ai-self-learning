# Module 6: Audit and Certification

*Estimated time: 8-12 hours*

---

## What This Module Covers

Module 5 built the harness, guardrails, punch-out points, and success rate measurement. Module 6 adds the final Stage 4 artifact — the audit trail with per-step model, token, and cost data — and then assembles the complete Stage 4 certification portfolio for submission.

This module also deepens the adversarial review agent layer from a single agent (Exercise 19) into a complete guardrail network between every pipeline step.

---

## Why This Module Exists

Stage 4 certification requires five artifacts. Four are built in Module 5. The fifth — the audit trail — is what makes the workflow measurable in production. "Cost-adjusted capacity" means you know what each step costs, not just whether it succeeded. You cannot manage what you do not measure.

The audit trail is also what makes the workflow safe to operate. When a pipeline run fails, you need to trace the failure to its exact origin step, understand what model was used, what it cost, and what the input was. Without that, you are debugging in the dark.

---

## Prerequisites

- Module 5 complete. You have a working shell-script harness with guardrails, punch-out points, and end-to-end success rate data.
- The Devin CLI installed (its session logs in `~/.local/share/devin/cli/sessions.db` are the primary data source for per-step cost data).

---

## Exercises in This Module

- [Exercise 22: Audit Trail with Per-Step Cost Data](Exercise-22-Audit-Trail.md) — Capture model, token, and cost data for every step execution
- [Exercise 23: Adversarial Review Agent Deep Dive](Exercise-23-Adversarial-Review-Agents.md) — Build the full adversarial guardrail layer between every step
- [Exercise 24: Stage 4 Certification Portfolio Assembly](Exercise-24-Stage-4-Portfolio.md) — Organize all five artifacts and verify against FAIL conditions
- [Exercise 25: Self-Assessment and Team Readiness](Exercise-25-Stage-4-Self-Assessment.md) — Honest assessment of solo capability and team gaps

---

## What Done Looks Like

At the end of Module 6, you will have:
- An audit trail log (JSON or CSV) with per-step model, token, and cost data from at least 3 pipeline runs
- A complete adversarial review agent layer between every pipeline step, each with a distinct lens
- A Stage 4 certification portfolio with all five artifacts organized and verified
- An honest self-assessment of what the solo path taught you and where team experience is irreplaceable
- Your portfolio submitted to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx) — note in your submission that you are requesting Stage 4 review