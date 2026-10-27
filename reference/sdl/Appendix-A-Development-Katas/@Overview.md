# Appendix A: Development Katas

*Ongoing practice — no fixed time estimate*

---

## What This Module Is

You have been running katas since Module 1. The Pomodoro kata was your first domain. The Conway's, Tic-Tac-Toe, Snake, and Sorting Visualizer katas were stress tests for your delivery skills in Module 2. The Blackjack kata was your final Module 2 pipeline run. Appendix A is not a new practice — it is the continuation and formalization of what you have already been doing.

A **development kata** is a well-specified coding challenge — small enough to complete in a single session (typically 2–4 hours of focused work), complex enough to exercise real engineering judgment.

**Time expectations:** A single kata run (pipeline + build + evaluation) is 2–4 hours. With the feedback loop (two runs + EDD improvement), expect 4–7 hours per kata. All 14 katas with the feedback loop is approximately 45–100 hours — more than the rest of the program combined. This is a multi-month practice, not a weekend sprint. A recommended cadence is 2–3 katas per week. If time is limited, completing at least 6 katas across all 4 difficulty levels provides meaningful practice; the remaining katas are continued compounding for those who want to go deeper.

**Per-difficulty time estimates:**
- Beginner: 2–3 hours per run
- Intermediate: 3–4 hours per run
- Advanced: 4–5 hours per run
- Expert: 5–7 hours per run In traditional practice, the point of a kata is to repeat it until the execution becomes fluid. Here, the point is different: each kata is a stress test for your delivery harness. You run the kata through your pipeline, you observe where the pipeline helps and where it falls short, and you update your commands via EDD. Then you run the next kata — with better commands.

The katas in this module are not exercises in learning new algorithms or UI patterns. They are instruments for improving your AI-assisted development workflow. The kata is the test input. Your delivery skills are the system under test.

---

## The Core Discipline

**Run each kata through your full delivery pipeline before writing a single line of code.**

That means:
1. Use the kata description as your Feature and System Request
2. Run `create-scope.md` → `create-architecture.md` → `create-ux.md` → `decompose-to-deliverables.md`
3. Select one deliverable, run `plan-deliverable.md` → `create-deliverable.md` → `review-deliverable.md`
4. Build the kata using the AI-generated plan and implementation as your starting point
5. Review the results against the kata's success criteria
6. Update your delivery skills via EDD based on what you learned
7. Pick the next kata and repeat — with improved commands

What you are measuring: not how good the kata deliverable is, but how much your delivery skills helped. Where did the pipeline produce output that accelerated the build? Where did it produce output that was generic, incomplete, or actively misleading? Those failures are your next Promptfoo test cases.

---

## The Repetition Principle

**Build each kata at least twice before moving on.** Time your first and second runs. The delta tells you whether your command improvements actually changed your development speed.

Between runs:
- Review your pipeline outputs against the kata's stated requirements
- Identify at least one specific failure in the pipeline (not the implementation — the command output)
- Form a hypothesis, update the relevant command via EDD, run Promptfoo to validate
- Run the kata again with the updated command

If your second run produces the same pipeline failures as the first, your command update did not address the real root cause. Diagnose before running a third time.

**Keep your command improvements generic.** The single most important discipline in this module: do not add kata-specific instructions to your commands. If you add a constraint to `create-scope.md` that says "always include a section on real-time probability calculation," you have broken that command for every future product that does not need probability calculation. Every improvement you make to a command must work for the next kata too. If you cannot write the improvement generically, the improvement is not ready to be in the command.

---

## The Feedback Loop in Practice

After each kata pipeline run, ask:

**Where did the pipeline help?**
- Did the scope document capture the right scope and constraints?
- Did the Architecture identify the technically interesting components?
- Did the Workstreams and Deliverables decompose the work at the right granularity?
- Did the Deliverable Plan give you something useful to start from?

**Where did the pipeline fall short?**
- Did the scope document omit important requirements that were in the kata description?
- Did the Architecture make naive choices about data structures or algorithms?
- Were the Deliverables too large, too vague, or missing dependencies?
- Did the Plan produce generic code scaffolding instead of a specific deliverable approach?

**What would make it better?**
- Is the failure a Context problem (the command needs more information about the domain)?
- Is it a Constraints problem (the command needs a rule it currently lacks)?
- Is it an upstream quality problem (a downstream command failed because an upstream one produced weak output)?

Write your per-run answers in the kata's `kata-run-log.md` (Exercise 17, Step 1), and your cross-kata summary in `kata-feedback-log.md` (Exercise 17, Step 7). This log is the evidence that the practice is working.

---

## Kata Difficulty and Progression

The 14 katas are organized across four difficulty levels. Each level exercises different aspects of your delivery pipeline:

| Level | Count | Primary Challenge |
|-------|-------|------------------|
| Beginner | 4 | State management, basic game loops, UI clarity |
| Intermediate | 5 | Algorithm integration, math accuracy, multi-mode UX |
| Advanced | 3 | Complex algorithm visualization, multi-layer state |
| Expert | 2 | Probabilistic systems, financial computation, rich data viz |

Work through the katas roughly in difficulty order, but do not treat this as a rigid sequence. If a particular kata exposes a gap in a specific command, run another kata with similar characteristics before moving on.

---

## Exercises in This Module

- [Exercise 17: The Kata Feedback Loop](Exercise-17-Kata-Feedback-Loop.md) — How to run any kata through your delivery harness and translate the results into command improvements
- [Kata Reference: Beginner](Katas-Beginner.md) — Four katas focusing on state, game loops, and accessible UI
- [Kata Reference: Intermediate](Katas-Intermediate.md) — Five katas adding algorithm integration, probability, and analytical modes
- [Kata Reference: Advanced](Katas-Advanced.md) — Three katas with complex visualization and multi-layer algorithmic state
- [Kata Reference: Expert](Katas-Expert.md) — Two katas with probabilistic engines and financial computation

---

## What Done Looks Like

There is no formal completion gate for Appendix A — this is ongoing practice. **To complete the SDL program**, you need documented kata stress tests for at least 3 delivery skills (per the program completion criteria). This module provides 14 katas for ongoing practice — completing the minimum of 3 kata stress tests satisfies the program requirement; the remaining katas are continued practice for those who want to compound their skills further. The signal that the practice is working is in your `kata-feedback-log.md`:

- Your delivery skills produce measurably better pipeline output for kata 10 than for kata 1
- Your Promptfoo scores on existing commands have improved as a result of insights from kata runs
- Your Haiku scores have improved on delivery skills where you applied kata-driven improvements
- The time from kata description to a working implementation has decreased across iterations
- Every command improvement you made is generic — it applies to all future katas, not just the one that exposed the gap
