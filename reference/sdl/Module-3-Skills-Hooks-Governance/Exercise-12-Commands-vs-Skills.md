# Exercise 12: Commands vs. Skills

*Estimated time: 1.5–2 hours*
*Prerequisites: Modules 1–2 complete*

---

## Goal

Develop a clear, principled understanding of the difference between a command and a skill, and apply that understanding to assess which of your existing commands are candidates for skill conversion.

This exercise is primarily analytical — you will read, think, and write. The writing you produce becomes part of your certification deliverables and your coaching vocabulary.

---

## Background: The Structural Difference

**A command** is a prompt file you invoke explicitly. You choose when it runs. You review the output before anything downstream happens. Commands are the default mode.

**A skill** is a prompt file the model can invoke autonomously, based on its interpretation of context. You give up explicit invocation control in exchange for convenience and integration. In tools like Claude Code, Windsurf, and GitHub Copilot, skills are discoverable by the model and can be triggered without you explicitly invoking them.

The practical difference: if you run a command and the output is wrong, you catch it before anything downstream acts on it. If a skill invokes at the wrong time, it may produce output that is acted on before anyone reviews it.

---

## Step 1: Read and Understand Your Tool's Skill Mechanism (30 minutes)

Consult the documentation for your AI tool (Claude Code, Windsurf, or GitHub Copilot) to understand:

- How does the tool discover and load skill files?
- How does the model decide when to invoke a skill?
- What signals (file naming, metadata, invocation hints) influence whether and when a skill triggers?
- How can you observe or log skill invocations?

Write a brief summary (5–10 sentences) of how your tool's skill mechanism works. This goes in a file called `skill-mechanism-notes.md` — it is for your own reference and does not need to be polished.

---

## Step 2: Invocation Boundary Analysis (45 minutes)

Choose two commands from your Module 1–2 artifact set. For each, answer these questions in writing:

**Command 1:** [name it]

1. What input or context triggers a human to run this command? (Be specific — what are they looking at, thinking about, or working on when they decide to invoke it?)
2. Could the model identify that trigger from context alone, without the human explicitly thinking "I should run this command"? Why or why not?
3. What is the harm if the model invokes this command at the wrong time? (Consider: what downstream actions depend on its output? Who acts on the output before reviewing it?)
4. What is the harm if the model fails to invoke it when it should? (Is the failure mode "human does the work manually" or "the step gets skipped entirely"?)
5. What ambiguous cases exist where you would not be sure whether to invoke this command? What would the model probably do in those cases?

**Command 2:** [name it]

Answer the same five questions.

---

## Step 3: Team Consensus Simulation (30 minutes)

Pick one of your two commands and do this exercise in writing:

Imagine there are two engineers who both use this command independently. They have both been happy with it in their own workflows. They are now asked to agree on a shared version — one skill that both will use, with one shared definition of when it should invoke.

Write out:
- At least two scenarios where they would likely disagree about whether the skill should invoke
- What the consequence of each disagreement would be (one engineer's expectation is violated)
- What they would need to agree on in writing before converting this command to a shared skill

This is the team consensus requirement made concrete. If you cannot answer these questions for a command, that command is not ready to become a shared skill.

---

## Step 4: Commit

Create `skill-readiness-assessment.md` with the full text of your invocation boundary analysis and team consensus simulation. Commit it.

---

## Self-Check

- [ ] `skill-mechanism-notes.md` committed with a clear summary of your tool's skill mechanism
- [ ] `skill-readiness-assessment.md` committed with analysis for two commands
- [ ] All five invocation boundary questions answered for each command
- [ ] Team consensus simulation completed for at least one command, with specific disagreement scenarios
- [ ] You have identified which command is the stronger candidate for skill conversion (you will use it in Exercise 13)
