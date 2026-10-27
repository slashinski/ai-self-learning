# Exercise 25: Self-Assessment and Team Readiness

*Estimated time: 2–3 hours*
*Prerequisites: Exercises 18–24 complete*

---

## Goal

Assess your Stage 4 artifacts honestly — production-quality or exercise-quality? Confront the team dimension the SDL cannot fully teach. Decide what comes next: the DLP Stage 4 team engagement or real-world team workflow building. Write a self-assessment that is truthful about what the solo path taught you and where team experience is irreplaceable.

This is not a gate. There is no minimum score. The purpose is an honest accounting of where you are, what you have, and what you still need.

---

## Background: The Solo Ceiling

The SDL is a self-paced, solo path. It can teach you to build all five Stage 4 artifacts:

1. **Workflow Definition** — an automated harness that runs your delivery pipeline end-to-end
2. **Guardrails** — deterministic hooks and adversarial review agents between every step
3. **Punch-Out Evidence** — bypass-tested human evacuation points
4. **End-to-End Success Rate** — the composite success rate across multiple pipeline runs
5. **Audit Trail** — per-step model, token, and cost data for every execution

You can build all five of these alone, in your own repository, and you should. The SDL has walked you through each one.

But Stage 4 is inherently a team event. The Stage 4 DLP proposal is explicit about this: *"Personal agents from Stage 3 must be reconciled into shared workflows."* A single person cannot fully replicate what happens when two or more people bring their own Stage 3 skills, their own standards, their own assumptions about what "good" means — and have to reconcile them into one shared workflow.

The solo path can teach you the artifacts. It cannot teach you the negotiation, the consensus-building, the discovery that your "obvious" standard is not obvious to someone else. It cannot teach you what happens when a teammate picks up your workflow and misunderstands something you thought was self-evident.

This exercise is about facing that gap honestly.

---

## Step 1: Artifact Quality Assessment (45 minutes)

For each of the five Stage 4 artifacts, write an honest assessment in `stage4-artifact-assessment.md`. Use this structure for each artifact:

```markdown
### Artifact N: [name]

**What I built:** [1–2 sentences describing your artifact]

**Production-quality or exercise-quality?** [Pick one and justify]

**What would make it production-quality?** [Specific gaps, if any]

**Would a teammate understand it without me explaining?** [Yes/No, and why]
```

The distinction between **production-quality** and **exercise-quality** is the core of this step:

- **Production-quality** means the artifact could be used by a team on real client work without you being present to maintain it. It handles edge cases. It has documentation. It has been tested against inputs that are not synthetic. It degrades gracefully when things go wrong.

- **Exercise-quality** means the artifact demonstrates the concept and works under the conditions you tested it in, but would not survive contact with a real team doing real work without significant hardening. This is not a failure — it is an honest categorization.

Be specific about what would close the gap. "More testing" is not specific. "The audit trail does not capture cache token costs, which means the cost data is ~15% understated for Sonnet runs" is specific.

The five artifacts to assess:

### Artifact 1: Workflow Definition

Your harness script and the workflow it orchestrates. Consider:
- Does the harness handle failure modes beyond the happy path?
- Is the workflow configuration documented, or does it live in your head?
- Have you run it against inputs that are not katas or program exercises?
- Could someone else clone your repo and run the harness without asking you a question?

### Artifact 2: Guardrails

Your deterministic hooks and adversarial review agents. Consider:
- Do the hooks validate real content, or are some still checking file existence?
- Do the adversarial agents have genuinely distinct lenses, or are any re-checking the same criteria as the producing agent?
- Have the guardrails been tuned for false positive rate, or do they pass/fail binary?
- What happens when a guardrail fails — is the failure message actionable enough for someone else to know what to fix?

### Artifact 3: Punch-Out Evidence

Your bypass-tested human evacuation points. Consider:
- Are the punch-out points at the right locations — do they protect genuine human decision points, or are they ceremony?
- Was the bypass testing rigorous, or did you test the obvious bypass and stop?
- Is the enforcement in the harness code, or does it rely on a human remembering to check?
- Could a teammate disable a punch-out point accidentally?

### Artifact 4: End-to-End Success Rate

Your composite success rate report. Consider:
- Is the success rate measured against real work, or against katas and synthetic inputs?
- Is the grading criteria for "successful end-to-end" documented and reproducible, or is it your judgment call?
- Do you have enough runs to draw a meaningful conclusion (10+), or is the number based on 3 runs?
- Is the trend tracked over time, or is it a single snapshot?

### Artifact 5: Audit Trail

Your per-step model, token, and cost data. Consider:
- Does the audit trail cover every step, or are there gaps?
- Is the cost data accurate, or are you estimating based on assumptions about token pricing?
- Can you trace a failure to its exact origin step using only the audit log, or do you need to look at other files?
- Is the audit log format documented, or would a teammate need to reverse-engineer the schema?

---

## Step 2: Team Dimension Assessment (45 minutes)

This is the part the SDL cannot fully teach. Answer each question honestly in the same `stage4-artifact-assessment.md` file, under a new heading:

```markdown
## Team Dimension Assessment

### Sharing

**Have you shared any of your delivery skills or Stage 4 artifacts with a teammate?**
[Yes/No. If yes: what did you share, with whom, and what was their reaction? If no: why not?]

**If a teammate looked at your harness right now, what would they understand without you in the room?**
[Be specific. What would make sense? What would require explanation?]

### Reconciliation

**Have you ever reconciled your personal AI standards with another person's?**
[Yes/No. This means: sat down with someone who has their own way of doing AI-assisted work and negotiated a shared standard. If yes: what did you agree on? What did you disagree on? If no: this is expected for a solo path — note it honestly.]

**Where would reconciliation be hardest for you?**
[Think about which of your standards are most personal — the ones you would resist changing. Those are the ones that will be hardest to reconcile in a team context.]

### Handoff

**Could a teammate pick up your workflow and run it?**
[Yes/No/Partially. What would they need? How long would it take them to be productive?]

**What is the single biggest barrier to someone else using your workflow?**
[Is it documentation? Tooling? Domain knowledge? The workflow's assumptions? Name the one thing, not a list.]
```

There is no wrong answer here. If the answer to every question is "no" or "I haven't done that," that is the expected state for someone who completed a solo program. The point is to name it, not to hide it.

The team dimension questions are not about your artifacts — they are about you. The artifacts can be built solo. The team practices cannot. Knowing where you are on the team dimension is what tells you what to do next.

---

## Step 3: What Comes Next (30 minutes)

Based on your assessments in Steps 1 and 2, identify your next step. There are two paths, and the honest assessment should make it clear which one applies:

### Path A: DLP Stage 4 Team Engagement

The Stage 4 Deep Learning Program is a 16-week team engagement that takes a cohort of Stage 3-certified practitioners through Stage 4 as a team. It includes:

- A 4–6 person team working on a real business process
- A Trainer delivering 5 sessions plus weekly office hours
- An Embedded Engineer co-building the harness with the team
- An IT Liaison handling infrastructure (API keys, CI/CD, deployment)
- Explicit reconciliation of personal Stage 3 skills into shared team workflows
- Stage 4 certification submission at the end

**This path is right for you if:**
- Your artifacts are exercise-quality and you want to build them to production-quality with team support
- Your team dimension answers are mostly "no" — you have not shared, reconciled, or handed off
- You are on a client team that has a real business process to automate
- You want the structured guidance, office hours, and EE pairing

### Path B: Real-World Team Workflow Building

You take what the SDL taught you and build a real Stage 4 workflow with your actual team, without the formal DLP structure. You use the SDL exercises as a guide, the Stage 4 proposal as a reference, and your own judgment to drive the process.

**This path is right for you if:**
- Your artifacts are close to production-quality and you need team pressure-testing, not a guided rebuild
- You have a teammate or team willing to work through the reconciliation process with you
- You are self-directed enough to drive the team coordination without a Trainer and EE
- You want to move faster than a 16-week engagement allows

### Path C: Stay at Stage 3

You assess that your Stage 3 skills are solid, you understand Stage 4 conceptually, but neither the DLP engagement nor real-world team workflow building makes sense right now. You stay at Stage 3, continue the Development Katas, and revisit Stage 4 when the opportunity is real.

**This path is right for you if:**
- You do not have a team or business process ready for Stage 4
- Your Stage 3 skills are still maturing — the katas are still surfacing gaps
- You understand Stage 4 but the timing is not right

This is not a lesser path. Stage 3 is the target for the core program. Stage 4 is an additional investment that should be made when there is a real team and a real workflow to build.

---

Write your path selection in `stage4-artifact-assessment.md`:

```markdown
## What Comes Next

**Assessed path:** [A / B / C]

**Why:**
[3–5 sentences explaining your choice, grounded in your Step 1 and Step 2 assessments]

**What I will do in the next 30 days:**
[1–3 specific actions. Not "explore options" — name a concrete step: "schedule a conversation with my delivery lead about automating the sprint planning workflow" or "complete 5 more katas and re-assess" or "contact an Improving AI Leader about DLP Stage 4 engagement timing"]
```

---

## Step 4: Solo vs. Team Reflection (30 minutes)

Write a brief reflection — 2–3 paragraphs — on what the SDL taught you about Stage 4 versus what you still need to learn through team practice. This is not a formality. It is the exercise's real deliverable.

Save it as `stage4-solo-reflection.md` in your repository. Address:

1. **What the solo path genuinely taught you.** Name specific capabilities you did not have before Modules 5 and 6 — things you can now do that you could not do before. Be concrete. "I can build a harness" is less useful than "I can write a shell script that calls my delivery skills in sequence, passes outputs between steps, and halts on guardrail failure — and I could not do that before Module 5."

2. **What the solo path could not teach you.** Name the specific things that require a team. Not abstract concepts — concrete experiences. "I have never had someone else try to use my harness and gotten feedback on what confused them" is concrete. "Team coordination" is abstract.

3. **The one thing that surprised you.** Something about Stage 4, about your own skills, or about the gap between solo and team that you did not expect when you started the SDL.

---

## Step 5: Commit

Commit `stage4-artifact-assessment.md` and `stage4-solo-reflection.md` to your repository. These are the final artifacts of the SDL Stage 4 extension.

---

## Module 6 Artifact Review

Before completing the SDL Stage 4 path, confirm you have all five certification artifacts plus this self-assessment:

**The five Stage 4 artifacts (from Exercises 18–24):**
- [ ] **Workflow Definition** — harness script running the full pipeline end-to-end, committed
- [ ] **Guardrails** — deterministic hooks between every step, adversarial review agents with distinct lenses, committed
- [ ] **Punch-Out Evidence** — bypass-tested human evacuation points with test logs, committed
- [ ] **End-to-End Success Rate** — composite success rate report from 10+ runs, committed
- [ ] **Audit Trail** — per-step model/token/cost data from 3+ runs, committed

**This exercise:**
- [ ] `stage4-artifact-assessment.md` — all five artifacts assessed (production-quality vs. exercise-quality), team dimension questions answered, next-path selected with justification
- [ ] `stage4-solo-reflection.md` — 2–3 paragraph reflection on solo vs. team learning

**Portfolio submission (from Exercise 24):**
- [ ] Portfolio submitted to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx) with a note requesting Stage 4 review

---

## Self-Check

- [ ] Every artifact is categorized as production-quality or exercise-quality with specific justification
- [ ] Team dimension questions are answered honestly — "no" is a valid answer and is expected for a solo path
- [ ] Next path is selected with specific 30-day actions, not vague intentions
- [ ] Reflection names concrete capabilities gained and concrete team experiences still missing
- [ ] You can read your solo vs. team reflection out loud and stand behind every claim — if you wince at a sentence, rewrite it

---

## A Final Note

The SDL is a self-paced, solo program. It was designed to teach you the skills of the AI Bootcamp without an instructor. It was extended to cover the Stage 4 artifacts because those artifacts can be built alone, and building them alone teaches you the mechanics — how a harness works, how guardrails fit between steps, how a success rate is measured, what an audit trail captures.

But Stage 4 certification is not just about having the artifacts. It is about having a workflow that a team owns, maintains, and operates. The proposal for the Stage 4 DLP is explicit: *"A single person cannot certify at Stage 4 in isolation."*

This is not a limitation of the SDL. It is a feature of Stage 4. The whole point of Stage 4 is that the workflow belongs to the team, not to one person. If one person built it, maintains it, and is the only one who understands it, that is a Stage 3 workflow with automation — not a Stage 4 workflow.

The SDL got you to the artifacts. The team engagement — whether through the DLP or through real-world practice — is what turns those artifacts into a certified Stage 4 workflow.

If you complete this exercise and realize your artifacts are exercise-quality and your team dimension is empty, that is not a failure. That is the SDL doing exactly what it was designed to do: teaching you the mechanics and then showing you honestly where the mechanics are not enough.