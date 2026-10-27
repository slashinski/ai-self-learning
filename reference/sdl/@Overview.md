# AI Self-Directed Learning — Overview

*A self-paced exercise sequence that builds the skills of the AI Bootcamp without an instructor present.*

---

## What This Program Teaches

This program takes you from "I use AI tools off-the-shelf" to a disciplined, measurable, structured approach to AI-assisted work. By the end, you will be able to:

- Apply the EDD (Evaluation-Driven Development) discipline: write tests before building any prompt
- Structure every prompt using RTCC (Role, Task, Context, Constraints)
- Use Promptfoo to measure prompt quality and iterate with evidence — across multiple models
- Verify that every instruction in a prompt is load-bearing
- Use the Model Ladder to quantitatively lower the cost of running a command without sacrificing quality
- Build commands, convert them to skills, and understand when each is appropriate
- Design sentinel file schemas and hooks as deterministic checkpoints in AI workflows
- Articulate the governance spectrum and explain it clearly to a non-technical audience

This is the same set of skills developed in the AI Bootcamp — repackaged so you can work through them alone, at your own pace, with no instructor required.

---

## Who This Is For

This program is for Senior or Principal-level engineers who:

- Have an active AI subscription (Windsurf, Claude, or GitHub Copilot) installed and working
- Are comfortable with basic AI tool usage but have not applied formal prompt structure, evaluation, or governance
- Want to develop the skills to serve as an Embedded Engineer in a Deep Learning Program engagement, or simply to raise the quality and rigor of their own AI-assisted work

**You do not need to already be good at prompting.** The exercises start from the beginning. What you do need is the willingness to do things in the prescribed order — specifically, to write tests before you build prompts.

---

## What You Need Before You Start

**Required:**
- An active subscription to at least one IDE-native AI tool: Windsurf, Claude Code, or GitHub Copilot
- Node.js installed (for Promptfoo)
- A GitHub account and a personal repository to commit your work to

**For Module 2 (Delivery Skills) and beyond:**
- Promptfoo installed and configured (`npm install -g promptfoo`)
- The CLI wrapper scripts from [github.com/improving/promptfoo](https://github.com/improving/promptfoo) copied into your project directory (see Exercise 3 for setup — no separate API key required)

---

## The Foundational Principles

### EDD: Evaluation-Driven Development

Every exercise in this program follows the same discipline, without exception:

**Write the test before you write the prompt.**

This is Evaluation-Driven Development (EDD). It is the analogue of Test-Driven Development for prompt engineering. The mechanics are:

1. **Red** — Write your test cases by hand. Define what success looks like specifically, in writing. Run them against a baseline prompt. Some should fail.
2. **Green** — Add instructions to the prompt until all test cases pass.
3. **Refactor** — Review every instruction. If removing it does not cause a test to fail, remove it. Every instruction must be load-bearing.

**The Load-Bearing Rule:** If a test would pass without the instruction you are about to add, do not add it. A prompt instruction that changes nothing measurable is not doing anything — or worse, it is telling the model something it was already going to do, crowding out instructions that actually matter.

**Why manual test files:** When you write test criteria by hand — before building the prompt — you commit to what success looks like before the model has shaped your expectations. If you let the model generate the outputs first, you may end up defining "success" as "what the model does by default," which tells you nothing about whether your instructions are changing anything.

---

### RTCC: Prompt Structure

Every prompt you write in this program follows the RTCC structure:

- **R — Role:** Who is the AI acting as? A specific, credentialed persona changes tone, vocabulary, and default assumptions.
- **T — Task:** What specific action should it perform? Verb-first, unambiguous.
- **C — Context:** What background information does it need? What does it know about the situation, the audience, prior steps?
- **C — Constraints:** What rules must the output follow? What should it never do? What format is required?

---

### The Model Ladder (Module 1 Only)

The Model Ladder is a diagnostic exercise you perform once, in Module 1, to learn something specific: that different models produce different quality from the same prompt, and that the gap between them is measurable and locatable. Once you have seen this — once it is clear to you that you CAN test across multiple models and observe both cost savings and capability differences — you stop. Running every evaluation against two models for the rest of the program would double your token costs without adding diagnostic value you don't already have.

More capable models (Sonnet, Opus, GPT-4o) compensate for underspecified prompts. They infer what you meant, fill in implied context, and apply domain knowledge you never stated. This makes them forgiving of weak prompts — but it also means you can spend significant money letting the model do work that a well-written instruction would have done for free.

**The Model Ladder principle:** Use EDD to measure how much your prompt relies on model reasoning. If your assertions pass on Sonnet and fail on Haiku (or GPT-4o mini), the gap tells you exactly where your prompt is underspecified. Each failing assertion is a specific, locatable instruction gap — not a guess.

The process (performed in Exercises 3-4, then stopped):
1. Build and test your prompt against a capable model (Sonnet or equivalent). Get to Green.
2. Run the same Promptfoo configuration against a lower-cost model (Haiku or equivalent). Record the delta.
3. For each assertion that fails on the cheaper model, ask: is the model failing because the instruction is ambiguous, or because the capable model was inferring something you never wrote down?
4. Add the missing specificity. Re-run on both models. The delta should narrow.

**The target is not always to achieve identical scores on both models.** Some prompts genuinely require more model capability — that is a valid finding. The target is to understand each gap, make a conscious decision about whether to close it, and document the result. A prompt you have deliberately left on Sonnet is different from a prompt you accidentally left on Sonnet because you never measured the alternative.

**When to stop running two models:** As soon as the Model Ladder exercise has made the concept concrete for you — you have seen the delta, you understand what it means, and you know how to act on it — switch to running evaluations against a single model (Haiku or equivalent) only. From Exercise 5 onward, all Promptfoo configurations in this program run against Haiku only. Running both models on every command doubles evaluation overhead without adding information you do not already have.

**Cost awareness:** You can monitor your AI usage at [usage.improving.ai](https://usage.improving.ai), which shows your monthly AI usage across tools. Use it to stay aware of what your evaluations cost. The Model Ladder exercise is designed to teach you to be cost-conscious, not to make every evaluation cost twice as much.

---

## Program Structure

| Module | Focus | Estimated Time |
|--------|-------|---------------|
| 1 | EDD and RTCC Foundations | 6–8 hours |
| 2 | Delivery Skills | 14–18 hours |
| 3 | Skills, Hooks, and Governed Flows | 10–14 hours |
| 4 | Completion and Self-Assessment | 3–4 hours |
| 5 | Development Katas | Ongoing |

Total estimated time for Modules 1–4: **39–54 hours** of focused work. This is designed for completion over 3–6 weeks depending on your pace. Appendix A is ongoing practice — there is no endpoint, only continued compounding improvement to your delivery tooling. Do not try to do multiple modules in a single day — the exercises are cumulative and the discipline takes time to internalize.

---

## How to Use This Program

**Rule 1: Do not skip to the next exercise until the current one is done.** Each exercise produces artifacts that the next exercise depends on. Skipping is detectable — and the point is not to have the files, it is to have done the work.

**Rule 2: Commit everything.** Your repository is the record of your work. Commit your test files before your prompt files. Commit Promptfoo configurations alongside the commands they test. The commit hideliverable is evidence of the EDD discipline.

**Rule 3: Do the load-bearing audit every time.** Every command you build should have a documented load-bearing audit before you move on. This is not optional, even when the prompt is working well.

**Rule 4: One change per Promptfoo iteration.** When iterating: form a hypothesis, make one change, run Promptfoo, record the delta. Do not change three things and then wonder which one made the difference.

**Rule 5: Run both models in Module 1, then stop.** The Model Ladder exercise (Exercises 3-4) runs against both a capable model and a lower-cost model to teach you about prompt clarity and cost. Once you understand the lesson, switch to a single model (Haiku) for all subsequent exercises. Running two models on every evaluation doubles cost without adding diagnostic value. Check [usage.improving.ai](https://usage.improving.ai) to see your monthly AI usage.

---

## Completion Criteria

You have completed this program when you can submit the following:

**Artifacts (committed to your repository):**
- [ ] `create-scope-tests.md` committed before any command was built
- [ ] `create-scope.md` — RTCC-structured, load-bearing audit documented
- [ ] `create-scope-promptfoo.yaml` — two-model config (Module 1 only), baseline + 3+ iterations recorded
- [ ] Model Ladder baseline documented for Module 1's `create-scope` delivery skill (two-model comparison, done once)
- [ ] Seven delivery skill files from Module 2 with completed Context and Constraints
- [ ] Promptfoo configurations for all seven delivery skills (single-model Haiku from Module 2 onward, with iteration records)
- [ ] Load-bearing audit documentation for at least 3 commands
- [ ] Kata stress test documented for at least 3 delivery skills
- [ ] Model Ladder progression documented for Module 1's `create-scope` (starting delta → hypothesis → change → resulting delta)
- [ ] DevLog pipeline run output (all seven stages) and pipeline run notes
- [ ] Blackjack kata pipeline run output and comparison notes
- [ ] At least one skill file converted from a delivery skill, with invocation test cases
- [ ] Sentinel file schema for at least one delivery skill
- [ ] Hook script with deterministic pass/fail logic
- [ ] Two-step governed flow, tested across all four scenarios

**Written deliverables:**
- [ ] Automation spectrum assessment for your artifact set
- [ ] Governance explanation paragraph (written for a non-technical manager)
- [ ] Behavior change reflection: which artifacts are in your active daily workflow
- [ ] Self-assessment against the four DLP Completion criteria (Craft, Evaluate, Iterate, Adopt)

---

## Certification Paths

The SDL is a valid path to learn the skills needed for both Stage 3 and Stage 4 certification. The "How to Trust AI" course on ImprovingU is an alternative way to learn the same Stage 3 skills — either path prepares you. Choose the one that fits your learning style.

**Stage 3 Certification:**
1. Complete Module 1 (produces all three required artifacts: evaluation framework, quantified improvement evidence, reusable task library)
2. Modules 2-4 provide depth and practice — recommended but not required for certification
3. Submit your portfolio to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx)

**Stage 4 Certification:**
1. Complete Modules 1-4 (Stage 3 foundation)
2. Complete Modules 5-6 (Stage 4 artifacts: automated harness, guardrails, punch-out points, end-to-end success rate, audit trail)
3. Submit your portfolio to the same [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx) — note in your submission that you are requesting Stage 4 review

---

## Module Files

- [Module 1](Module-1-EDD-and-RTCC/@Overview.md) — EDD and RTCC Foundations (Stage 3 ready)
- [Module 2](Module-2-Delivery-Skills/@Overview.md) — Delivery Skills (Stage 3 depth)
- [Module 3](Module-3-Skills-Hooks-Governance/@Overview.md) — Skills, Hooks, and Governed Flows (Stage 3/4 foundation)
- [Module 4](Module-4-Completion/@Overview.md) — Completion and Self-Assessment (Stage 3 submit)
- [Module 5](Module-5-Workflow-Orchestration/@Overview.md) — Workflow Orchestration (Stage 4 artifacts 1-4)
- [Module 6](Module-6-Audit-and-Certification/@Overview.md) — Audit and Certification (Stage 4 artifact 5 + submit)
- [Appendix A](Appendix-A-Development-Katas/@Overview.md) — Development Katas (ongoing practice)
