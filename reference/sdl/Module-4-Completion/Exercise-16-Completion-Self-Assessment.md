# Exercise 16: Completion and Self-Assessment

*Estimated time: 3–4 hours*
*Prerequisites: Modules 1–3 complete*

---

## Goal

Review your full artifact set against the handoff checklist. Reflect honestly on behavior change. Write a self-assessment against the four DLP Completion criteria. Complete the AI Adoption Stage Evaluation. Submit your full artifact set to the Stage 3 Certification Request SharePoint site for review.

---

## Step 1: Handoff Checklist Review (60 minutes)

Every artifact you submit must be usable by a developer who was not in this program — someone who just joined a client team and found your files in the repository. Apply this checklist to each committed file:

**For each delivery skill file:**
- [ ] Has a comment header: what it does, when to use it, what the expected input format is, where the test file lives
- [ ] Promptfoo configuration is committed in the same directory as the delivery skill file
- [ ] Every instruction is load-bearing (audit documented)
- [ ] The test file exists and is referenced in the header

**For each Promptfoo configuration:**
- [ ] Committed alongside the delivery skill it tests, not in a separate directory
- [ ] Includes a comment describing the product domain and the constraints being tested

**For the skill file:**
- [ ] Invocation description is specific enough that a new team member would understand when it should and should not trigger
- [ ] Invocation test cases (positive and negative) are committed alongside it

**For the sentinel file schema:**
- [ ] The schema is documented in the hook script or in a separate schema file
- [ ] The relationship between the schema and the Promptfoo assertions is documented (which properties does the sentinel cover, and which are left to Promptfoo?)

**For the hook script:**
- [ ] Comments explain what events trigger the hook and what decision it makes
- [ ] Failure messages are clear enough for a developer to know what to fix without reading the code

Fix anything that fails the checklist before continuing.

---

## Step 2: Behavior Change Reflection (45 minutes)

For each artifact you are submitting, answer:
1. Is this artifact in your actual daily workflow now, or did you build it for this program?
2. When did you last use it in a task that was not a program exercise?
3. If you were not in this program, would you still use it?

Write honest answers in `behavior-change-reflection.md`.

The four most important behaviors to assess honestly:
- **Do you write the test before the prompt?** Not "do you intend to" — do you actually do it, even when you are in a hurry?
- **Do you perform the load-bearing audit?** Not just on program exercises, but on any prompt you craft for real work?
- **Do you run cost-effective evaluations?** When you build a new delivery skill or iterate on an existing one, do you run it against a single model (Haiku or equivalent) and use the score to guide improvements? Have you actually adjusted any delivery skills based on what the score told you?
- **Has any artifact from this program become part of a real workflow?** Not a workflow you created for this program — a workflow you would use on actual work independent of this program.

There is no minimum score for these answers. The point is honesty. A reflection that says "I still default to building first when I am in a hurry, but I have noticed it and am correcting it" is more useful than a reflection that claims full adoption without evidence.

---

## Step 3: Completion Self-Assessment (60 minutes)

Write `completion-self-assessment.md`. Evaluate yourself against the four DLP Completion criteria (the SDL is Improving's self-paced path to these same completion criteria — the terms are interchangeable here).

**Certification path:** The SDL is a valid alternative to the "How to Trust AI" course on ImprovingU for learning the skills needed for Stage 3 certification. Either path prepares you — choose the one that fits your learning style. Submit your portfolio to the [Stage 3 Certification Request SharePoint site](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx).

---

### Craft

*The ability to apply RTCC structure and the load-bearing discipline to produce prompts that do what they claim to do.*

For this criterion, provide:
- One specific artifact that demonstrates Craft (not "I built eleven delivery skills" — name one and explain why it demonstrates Craft specifically)
- One specific example of using it in real work (not a program exercise)
- An honest assessment of where you are still developing

---

### Evaluate

*The ability to define success before building, measure output quality against defined criteria, and iterate with documented evidence — across multiple models.*

For this criterion, provide:
- One specific artifact that demonstrates Evaluate (a Promptfoo configuration with iteration records, with documented hypotheses)
- One specific example of using Promptfoo or manual test criteria in real work
- Your Model Ladder baseline for at least one command: what was the starting Sonnet/Haiku delta, what did you learn from it, and what did you do about it?
- An honest assessment of where you are still developing (common gaps: rubrics too permissive to fail on bad output; closing the Model Ladder delta without documenting why gaps were accepted)

---

### Iterate

*The ability to diagnose why a prompt is failing — distinguishing Context problems from Constraints problems, and downstream quality problems from upstream quality problems — and to make targeted, one-change-at-a-time improvements.*

For this criterion, provide:
- One specific artifact that demonstrates Iterate (an iteration record showing multiple runs with hypotheses and deltas)
- One specific example of diagnosing and tracing a quality problem to its source
- An honest assessment of where you are still developing (common gap: making multiple changes at once and losing traceability)

---

### Adopt

*The ability to change default workflow behaviors — to reach for EDD, RTCC, load-bearing audits, and single-model evaluations instinctively, not only when reminded.*

For this criterion, provide:
- One specific artifact that is in your active daily workflow (with evidence — last used date, real task)
- One specific habit change that has stuck
- An honest assessment of what adoption looks like for you right now, and what you are still working toward

---

## Step 4: Full Artifact Submission

Compile your final artifact list. Commit everything. Then submit your repository link to the **Stage 3 Certification Request** SharePoint site: [https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx](https://improving.sharepoint.com/sites/IMP-GrowthLearning/Stage%203%20certification%20requests/Forms/AllItems.aspx). Include:

1. A link to your repository
2. A brief note indicating that you have completed the SDL program and are requesting Stage 3 certification review
3. Any specific questions or areas where you want feedback

---

## Completion Artifact Checklist

Verify all of the following are committed to your repository before requesting review:

**Module 1:**
- [ ] `create-scope-tests.md` — committed before command
- [ ] `create-scope.md` — RTCC, load-bearing audit documented
- [ ] `create-scope-promptfoo.yaml` — two-model config (Module 1 only), baseline + iterations recorded
- [ ] Model Ladder baseline documented from Module 1 (Sonnet score, Haiku score, delta, hypotheses)

**Module 2:**
- [ ] The remaining 6 delivery skill files (create-architecture, create-ux, decompose-to-deliverables, plan-deliverable, create-deliverable, review-deliverable) with completed Context and Constraints
- [ ] Promptfoo configurations for all 7 (Haiku only from Module 2), with run results
- [ ] Load-bearing audit documentation for at least 3 delivery skills
- [ ] Kata stress test results documented for at least 3 delivery skills
- [ ] Upstream quality dependency trace (at least one case with root cause analysis)
- [ ] Model Ladder progression documented for at least 1 command (starting delta → hypothesis → change → resulting delta)
- [ ] DevLog pipeline run output files (all seven stages) and `devlog-pipeline-run-notes.md`
- [ ] Blackjack kata pipeline run output files and `blackjack-pipeline-run-notes.md`

**Module 3:**
- [ ] `skill-readiness-assessment.md`
- [ ] Skill file with invocation test cases (positive, negative, and quality) committed alongside it
- [ ] Sentinel file schema (designed before the hook script was built)
- [ ] Hook script with deterministic pass/fail logic, tested against all scenarios
- [ ] `governed-flow-test-results.md`
- [ ] `automation-spectrum-assessment.md`
- [ ] `governance-explanation.md`

**Module 4:**
- [ ] Handoff checklist applied and all failures fixed
- [ ] `behavior-change-reflection.md`
- [ ] `completion-self-assessment.md` with all four criteria addressed
- [ ] `stage-evaluation.md` — AI Adoption Stage scores (7 dimensions + total) and two-paragraph reflection

---

## A Note on the Review

The review is not a formality. A reviewer will look at commit timestamps, iteration records, and the specificity of your test criteria and self-assessment. The most common review findings are:

- Test files written after the delivery skill (commit timestamps reveal this)
- `llm-rubric` assertions that are too permissive (passing trivially on bad output)
- Promptfoo configurations with no iteration records (no evidence of EDD discipline)
- Load-bearing audits that documented zero removed instructions (extremely unlikely to be correct — every prompt has some dead weight)
- Self-assessments that claim full adoption without real-work evidence
- Model Ladder sections (Module 1) that record the delta but never explain what was done about it

Address these proactively in your self-assessment. Naming a known gap is better than having a reviewer find it.

---

## Step 5: AI Adoption Stage Evaluation

*Based on The Trust Evolution: 8 Stages of AI Maturity — Improving's official AI proficiency assessment*

**How this relates to the SDL:** The SDL program teaches EDD, RTCC, load-bearing audits, Promptfoo evaluation, skills/hooks/sentinel files, and governed flows. The 21-question assessment below uses Improving's company-wide AI Adoption Model, which uses a broader vocabulary ("task agents," "workflow agents," "quality gates"). Some dimensions (1, 4, 5) map directly to SDL artifacts. Others (2, 3, 6, 7) measure capabilities the SDL builds foundations for but does not fully develop — workflow orchestration and team practices are Stage 4 territory. Answer honestly based on what you actually do today, not what the SDL taught you in isolation.

*Estimated time: 30 minutes*

Complete this assessment after finishing your DLP completion self-assessment. It maps your practices to Improving's company-wide AI Adoption Model so your results speak the same language as the rest of the organization.

---

### How This Assessment Works

For each question, select the **single response** that most accurately describes what someone would observe if they watched you work for the past 30 days. Choose what is true, not what is aspirational.

**The test:** Read each option as "If someone watched me work for a week, would they see this consistently?" — not "Have I ever done this?" or "Could I do this?"

Scoring: A = 1 point, B = 2 points, C = 3 points, D = 4 points. 21 questions, 7 dimensions of 3 questions each. Total score range: 21–84.

---

### Dimension 1: Prompt Engineering & AI Interaction

**Q1.** Think about the last three times AI produced output you could not ship as-is. What did you do?

- A) I edited the output manually to make it work.
- B) I re-prompted with additional context or examples until the output improved.
- C) I identified the specific missing context or constraint that caused the gap and adjusted my prompt to address the root cause.
- D) I updated a persistent rules file or agent definition so that class of error would not recur — then verified the fix worked on similar inputs.

**Q2.** Right now, in your current active project, which of these best describes your AI instruction setup?

- A) I type prompts from scratch each session or use the tool's default settings.
- B) I have go-to prompt patterns I reuse, but they live in my head or a notes file — not integrated into my tools.
- C) I have a rules file, system prompt, or project instructions file that persists across sessions and encodes my standards.
- D) My instruction artifacts distinguish between good patterns and technical debt the AI should not replicate. They are version-controlled and updated regularly based on output quality.

**Q3.** In the last 30 days, how many times did you modify a persistent AI instruction artifact (rules file, system prompt, agent definition) because output quality fell short?

- A) Zero — I do not maintain one, or I have not needed to change it.
- B) 1–2 times.
- C) 3–5 times — it is becoming a regular practice.
- D) 6+ times — I treat instruction artifacts as living documents that improve with every iteration.

---

### Dimension 2: Task Agents & Single-Box Automation

**Q4.** If asked right now, could you draw your current workflow as boxes (discrete steps) and arrows (handoffs), labeling each one?

- A) I have not mapped my workflow this way. I work on things as they come.
- B) I could sketch it roughly, but I have not actually documented it.
- C) I have documented my workflow and can identify which boxes a human must own versus which an agent could handle.
- D) My workflow is documented, and at least one box is currently handled by an agent with defined opinions, constraints, and a definition of done.

**Q5.** For the task you most frequently hand to AI, which best describes how you interact with it?

- A) I describe what I need in conversational terms and guide the AI step by step.
- B) I give AI a clear prompt with context, review what comes back, and make corrections as needed.
- C) I hand the task to an agent with predefined opinions, constraints, and standards, then review the output against my definition of done.
- D) Most steps in my workflow have dedicated agents with documented standards. I have refined each through multiple iterations and can name specific failure modes I have corrected for.

**Q6.** Describe the last time an AI agent produced output that was wrong or off-target for a task you delegated.

- A) I cannot recall a specific instance — I have not delegated complete tasks to AI.
- B) It happened, but I fixed the output and moved on.
- C) I diagnosed why it failed and adjusted my prompt or instructions to prevent that error type.
- D) I can name three or more specific failure modes I have discovered and corrected for. Each correction is encoded in my rules, not just in my memory.

---

### Dimension 3: Workflow Orchestration & Coordination

**Q7.** When one step of your work produces output that feeds into the next step, how does the handoff happen?

- A) I manually copy, paste, or transfer output between tools and steps.
- B) I prompt AI for each step separately, manually passing context forward.
- C) At least one handoff is automated — one agent's output feeds directly into another without manual transfer.
- D) A workflow agent sequences multiple task agents, manages state between steps, and captures artifacts at each stage. I review checkpoints rather than managing transitions.

**Q8.** How many of the transitions (arrows) between steps in your workflow are currently automated — meaning AI handles the handoff without you intervening?

- A) None. I manage all transitions manually.
- B) I have experimented with automating one, but it is not reliable enough to use consistently.
- C) 1–2 transitions are reliably automated. I am working on more.
- D) Most transitions in my primary workflow are automated with quality gates at key checkpoints.

**Q9.** Which best describes the quality checks in your AI-assisted workflow?

- A) I review AI output by reading through it. There are no formal quality checks.
- B) I have informal checks — I review the output and sometimes run tests manually.
- C) At least one automated quality gate (tests, builds, linting) runs before I review output.
- D) Multiple automated quality gates fire at different stages. At least one agent's job is to check another agent's work before it reaches me.

---

### Dimension 4: Output Evaluation & Quality Judgment

**Q10.** When you receive output from AI, how do you determine whether it is good enough to use?

- A) I read through it and use my judgment. If it looks right, I use it.
- B) I check for specific known failure patterns — hallucinations, wrong conventions, common AI mistakes I have seen before.
- C) I evaluate against a defined rubric or scoring criteria — specific dimensions like accuracy, style conformance, and completeness — before accepting or rejecting.
- D) I run output through multiple evaluation methods (automated checks, rubric scoring, comparison against reference examples) and track scores over time to measure whether my agents are improving.

**Q11.** Do you have a documented definition of "good enough" for AI output in your workflow?

- A) No. I know it when I see it.
- B) I have informal criteria in my head that I check against, but nothing written down.
- C) I have written acceptance criteria or a scoring rubric that I apply consistently to AI output.
- D) My acceptance criteria are encoded in automated evaluations that run on every output. I review the scores, not just the output itself.

**Q12.** When AI output quality shifts over time (model updates, prompt changes, new projects), how do you detect it?

- A) I notice when something feels off, but I do not track quality systematically.
- B) I keep mental notes of when quality drops and adjust my prompts when I notice problems.
- C) I have specific test cases or reference outputs I re-run periodically to verify my agents still meet my standards.
- D) I maintain an evaluation harness — a repeatable set of inputs, expected outputs, and scoring criteria — that I run regularly to measure quality trends and catch regressions before they affect my work.

---

### Dimension 5: Governance, Trust & Safety Nets

**Q13.** Can you list, right now without looking, three anti-patterns or technical debt items in your codebase that AI might treat as the standard way to do things?

- A) I have not thought about this.
- B) I can think of one or two, but I have not told my AI tools about them.
- C) I know the major ones and have documented them in my AI instruction artifacts.
- D) I maintain an explicit list that AI references. I have caught instances where AI replicated debt, and my rules now prevent it.

**Q14.** What happens automatically when an AI agent in your workflow produces output that does not meet standards?

- A) Nothing automatic. I catch problems during manual review.
- B) I sometimes run manual checks (tests, builds) after getting output.
- C) At least one automated check runs on AI output before I see it. If it fails, I know before reviewing.
- D) Multiple automated gates fire in sequence. Agents specifically challenge other agents' output — review, architectural checks, security scans — before it reaches me.

**Q15.** In the last 30 days, how many times did an automated quality gate (not your manual review) catch a problem in AI-generated output before it would have reached production?

- A) I do not have automated quality gates on AI output.
- B) Zero catches, but I have some gates in place.
- C) 1–3 catches. The gates are proving their value.
- D) 4+ catches. I track what the gates catch and use the patterns to improve my agent definitions.

---

### Dimension 6: Trust & Working Identity

**Q16.** When an AI agent delivers output that passes your quality checks and meets your definition of done, what happens next?

- A) I do not have defined quality checks, so I review everything line by line.
- B) I still review thoroughly even when checks pass — I am not comfortable shipping without reading every line.
- C) I spot-check key areas but generally trust output that passed my gates. I ship faster than I used to.
- D) I ship it. My gates and definitions encode what good looks like. If it passes, rewriting is waste, not diligence.

**Q17.** If a colleague asked what you do all day, which answer sounds most like yours?

- A) I write code, produce deliverables, and do the work myself — sometimes with AI help.
- B) I use AI tools to draft things, then I refine and finish the work.
- C) I define tasks for AI agents, review their output, and focus my time on the parts that require my judgment.
- D) I design workflows, define standards, and review outputs. The agents produce the work; I produce the outcomes.

**Q18.** How has AI changed the way you break down and plan your work?

- A) It has not. I work through tasks the same way, just sometimes faster.
- B) I batch certain tasks and use AI to accelerate them, but my process is fundamentally the same.
- C) I decompose work specifically around what agents can handle versus what I need to do.
- D) I think in workflows and agent capabilities when I plan. My throughput has measurably increased because agents handle entire workflow stages.

---

### Dimension 7: Team & Organizational Practices

*For consultants: "Team" means both your Improving delivery team and the client team you are embedded with. High scores here require alignment in both contexts.*

**Q19.** If you were suddenly unavailable, could a teammate pick up your AI setup (rules files, agent definitions, workflow configurations) and produce similar-quality output?

- A) No. My AI use is conversational and has no persistent configuration to hand off.
- B) They could find my configuration, but they would need significant explanation to use it.
- C) My agent definitions encode my standards clearly enough that a competent teammate could use them with minimal explanation.
- D) My team already shares and uses these definitions. Our standards are encoded in agents, not just documented in a wiki.

**Q20.** How does your delivery team (including client team members where applicable) coordinate on AI-assisted work?

- A) AI use is individual. Each person uses their own tools their own way.
- B) We share tips and prompts informally, but everyone has their own setup.
- C) We have shared standards for AI use, but they are guidelines — not enforced by tooling.
- D) We share workflow agents with a collective definition of done. Changes to shared agent definitions go through team review.

**Q21.** Does your organization provide governance tooling (security scanning, compliance checking, architecture validation) that plugs into your AI workflow?

- A) No organizational governance tooling exists for AI workflows.
- B) Guidelines exist, but they are policy documents — not automated checks.
- C) Some automated governance exists, and I integrate it into my workflow manually.
- D) Organizational governance agents plug into my workflow automatically. Policies about what agents can do are enforced by agents, not just by people.

---

### Scoring

**Step 1: Score each question** — A = 1, B = 2, C = 3, D = 4.

**Step 2: Calculate dimension scores** — add the three scores per dimension (range: 3–12) and divide by 3 for the average.

| Dimension | Q# | Sum (3–12) | Average |
|---|---|---|---|
| 1. Prompt Engineering & AI Interaction | Q1, Q2, Q3 | | |
| 2. Task Agents & Single-Box Automation | Q4, Q5, Q6 | | |
| 3. Workflow Orchestration & Coordination | Q7, Q8, Q9 | | |
| 4. Output Evaluation & Quality Judgment | Q10, Q11, Q12 | | |
| 5. Governance, Trust & Safety Nets | Q13, Q14, Q15 | | |
| 6. Trust & Working Identity | Q16, Q17, Q18 | | |
| 7. Team & Organizational Practices | Q19, Q20, Q21 | | |
| **TOTAL** | | | |

**Step 3: Map total score to stage**

| Total Score | Stage | Name | Description |
|---|---|---|---|
| 21–31 | 1–2 | Zero AI / Off the Shelf | Using AI tools without structured workflows. Build prompt engineering fundamentals, document your workflow as boxes and arrows, and begin experimenting with task agents. |
| 32–42 | ~3 | Inflection Point | Building trust but not delegating full tasks consistently. Pick one workflow box, define a task agent for it, and refine until output is within 5% of what you would produce. |
| 43–58 | 3 | Task (Wave 2) ✓ | **DLP target stage.** AI executes single tasks independently. You review output. Build task agents for every remaining box and encode discovered failure modes into agent definitions. |
| 59–74 | ~4 | Approaching Workflow | Task agents are solid. Focus on orchestrating handoffs — add governance, quality gates, evaluation harnesses, and combative agents. Align your delivery team on shared definitions of done. |
| 75–84 | 4 | Workflow (Wave 2) | AI coordinates your full workflow with governance. Schedule a 1-on-1 with an Improving AI Leader to evaluate readiness for Stage 5+ (Wave 3: Agentic Operations). |

---

### What DLP Completion Should Produce

**Stage 3 is the target for this program.** A total score of 43–58 means you have built the personal practices this program was designed to produce: structured prompt engineering, task agents with defined standards, an evaluation harness, and automated quality gates. That is the goal. Completing this program does not put you at Stage 4 — advancing beyond Stage 3 requires additional skills investment and time operating your harness in an actual team delivery context.

Stage 4 cannot be meaningfully self-assessed. It requires looking at your team and organization, not just your own workflow. If your results suggest consistent Stage 4 practice, the next step is a 1-on-1 with an Improving AI Leader who can evaluate demonstrated capability across a team context — not a form you fill out alone.

Here is how the DLP artifacts map to the model dimensions:

**Dimension 1 (Prompt Engineering):** Your RTCC delivery skill files, load-bearing audits, and EDD iteration records are the evidence for C answers. If you built commands and never touched them again, you are at B. If you ran iterations with documented hypotheses and the delivery skills improved as a result, you are at C.

**Dimension 4 (Output Evaluation):** Your Promptfoo configurations are your evaluation harness. Two-provider configs with rubric assertions and recorded before/after scores are C or D territory. This is the dimension most DLP completers score highest on — it is the core of what the program teaches.

**Dimension 5 (Governance):** Your hook script and sentinel file are the evidence for C answers on Q14–Q15. If your governed flow tests showed the hook catching a missing or invalid sentinel, that is a real catch — record it honestly.

**Dimensions 2, 3, 6, and 7 (Task Agents, Workflow Orchestration, Trust & Working Identity, Team Practices):** These dimensions measure capabilities the SDL builds foundations for but does not fully develop. The SDL teaches single-task delivery skills (Dimension 2, answer B-C) and introduces governed flows (Dimension 3, answer B). Full workflow orchestration and team practices are Stage 4 territory. Score these honestly — lower scores here are expected and meaningful, not failures. They tell you what comes next.

---

### Record Your Results

Add a `stage-evaluation.md` file to your completion artifacts with your dimension scores, total score, and two paragraphs of reflection:

1. Which dimension surprised you most — either higher or lower than expected — and why?
2. What is the single most concrete behavior change that would move your lowest-scoring dimension up one letter across its three questions?

Include `stage-evaluation.md` in your submission to Tim Rayburn alongside your other completion artifacts.
