# Exercise 23: Adversarial Review Agent Deep Dive

*Estimated time: 2–3 hours*
*Prerequisites: Exercise 22 complete. Exercise 19 (guardrails) complete — you have at least one adversarial review agent prompt committed to your repository.*

---

## Goal

Build a complete adversarial review agent layer across your 7-step delivery pipeline — one adversarial agent between every pair of pipeline steps, each with a distinct analytical lens, its own prompt, and an explicitly adversarial posture. By the end, no step's output flows into the next step without a dedicated critic examining it first.

---

## Background: From One Adversarial Agent to a Guardrail Layer

In Exercise 19, you built a single adversarial review agent as a guardrail between two pipeline steps. You wrote a prompt designed to find problems — not to confirm quality, but to attack the output from a specific angle. That was the minimal pattern: one critic, one lens, one checkpoint.

This exercise extends that pattern to its Stage 4 conclusion. A complete guardrail layer has **one adversarial agent between every pair of pipeline steps**. Each agent has:

1. **A distinct lens** — a specific analytical perspective that no other agent in the layer duplicates. The lens is not "quality." Your producing agents already self-evaluate for quality. An adversarial agent whose lens is "verify output meets quality standards" is doing the same job as the producing agent's evaluation — a redundant second opinion, not an adversarial challenge.
2. **Its own prompt** — written from scratch to find problems through that lens. Not a template with the lens name swapped in. Different lenses require different instructions, different evaluation criteria, and different failure modes to probe.
3. **An explicitly adversarial posture** — the agent's job is to find what is wrong, missing, risky, or unsupported. It is not the agent's job to praise what is good. A prompt that says "review this output and provide feedback" is not adversarial. A prompt that says "find the three most likely failure modes in this output and explain why each would cause downstream problems" is.

### The Anti-Pattern: Redundant Second Opinion

The most common mistake when building an adversarial agent layer is creating agents that are polite quality reviewers in disguise. If your adversarial agent's prompt says "evaluate whether this output meets the quality standards defined in the producing agent's evaluation criteria," you have built a redundant second opinion. The producing agent already checks its own output against its own criteria. A second agent checking the same criteria adds cost without adding signal.

The distinction that matters: **a redundant second opinion asks "is this good?" An adversarial agent asks "what will break?"**

A redundant second opinion is also susceptible to the same blind spots as the producing agent. If the producing agent's evaluation criteria have a gap — they never check for security implications, for example — a second agent using the same criteria will have the same gap. An adversarial agent with a security lens finds what the producing agent's criteria never thought to look for.

### Why Distinct Lenses Matter

Each pipeline step produces a different kind of artifact with different failure modes. A scope document fails differently than an architecture document, which fails differently than a deliverable plan. An adversarial agent that applies the same generic "review this for problems" prompt to all of them will produce shallow, generic findings. An adversarial agent with a lens calibrated to the specific failure modes of the artifact it is examining will produce specific, actionable findings.

The lenses in this exercise are chosen to target the failure modes most likely to propagate downstream. A requirements gap in the scope document becomes a missing deliverable in the decomposition. An infeasible architecture decision becomes a plan that cannot be executed. A rubber-stamp review becomes a deliverable with undetected defects reaching production. Each lens is a different trap detector.

---

## The Pipeline and Its Guardrail Points

Your 7-step delivery pipeline:

| Step | Producing Agent | Output Artifact |
|------|----------------|-----------------|
| 1 | `create-scope.md` | Scope document |
| 2 | `create-architecture.md` | Architecture document |
| 3 | `create-ux.md` | UX document |
| 4 | `decompose-to-deliverables.md` | Workstreams and deliverables |
| 5 | `plan-deliverable.md` | Deliverable plan |
| 6 | `create-deliverable.md` | Deliverable (code or artifact) |
| 7 | `review-deliverable.md` | Review report |

The guardrail points — one adversarial agent after each producing step:

| After Step | Adversarial Agent | Lens |
|-----------|-------------------|------|
| 1 (create-scope) | Requirements Completeness Reviewer | What requirements are missing, ambiguous, or untestable? |
| 2 (create-architecture) | Security and Feasibility Reviewer | What architectural decisions are insecure, infeasible, or unsupported? |
| 3 (create-ux) | UX Edge Case and Feasibility Reviewer | What user flows break under edge cases, errors, or accessibility constraints? |
| 4 (decompose-to-deliverables) | Coverage and Dependency Reviewer | What requirements have no deliverable? What dependencies are hidden? |
| 5 (plan-deliverable) | Plan Critique Reviewer | What in the plan is under-specified, over-scoped, or likely to fail? |
| 6 (create-deliverable) | Standards and Compliance Reviewer | What standards, conventions, or integration contracts does the deliverable violate? |
| 7 (review-deliverable) | Review Quality Reviewer | Did the review catch real issues, or did it rubber-stamp? |

Six agents. Six distinct lenses. Six adversarial prompts.

---

## Step 1: Map Your Pipeline and Identify Guardrail Points (10 minutes)

Before writing any prompts, create a file called `adversarial-layer-map.md` that documents your pipeline's guardrail points. This is the design document — write it before building, not after.

```markdown
## Adversarial Review Agent Layer Map — [date]

### Pipeline Steps
1. create-scope → scope.md
2. create-architecture → architecture.md
3. create-ux → ux.md
4. decompose-to-deliverables → deliverables.yaml
5. plan-deliverable → plan.yaml
6. create-deliverable → deliverable artifact
7. review-deliverable → review.yaml

### Guardrail Points
For each guardrail point, document:
- **Position**: after which step
- **Agent name**: the reviewer's name
- **Lens**: the specific analytical perspective (one sentence)
- **What it is NOT checking**: explicit statement of what the producing agent already covers, to avoid redundancy
- **Key failure modes**: 3–5 specific failure modes this lens targets

### Anti-Pattern Check
For each agent, answer: "If I removed this agent, what would break that the producing agent's own evaluation would NOT catch?"
If you cannot answer this specifically, the lens is too close to "quality" and needs sharpening.
```

Commit `adversarial-layer-map.md` before writing any adversarial prompts.

---

## Step 2: Build the Requirements Completeness Reviewer (20 minutes)

**Position**: After `create-scope.md`, before `create-architecture.md`

**Lens**: What requirements are missing, ambiguous, untestable, or internally contradictory? The scope document is the foundation of the entire pipeline — every gap here compounds downstream.

**What this agent is NOT checking**: Whether the scope document is well-formatted, whether it has the right sections, whether it reads well. Those are the producing agent's self-evaluation concerns.

**Key failure modes to probe**:
- Requirements stated as aspirations rather than testable conditions ("the system should be fast" vs. "API responses under 200ms at p95")
- Implicit requirements that any stakeholder would assume but the document never states
- Requirements that contradict each other (requirement A implies X, requirement B implies not-X)
- Out-of-scope items that are actually in-scope by implication
- Success criteria that cannot be measured or have no threshold

Write the adversarial prompt as `adversarial-requirements-completeness.md`:

```markdown
## Role
You are a requirements auditor who has been hired to find gaps in a scope document before it is used to drive architecture and implementation decisions. You are not here to praise the document. You are here to find what will cause expensive rework downstream.

## Task
Analyze the scope document and produce a findings report that identifies requirements gaps, ambiguities, contradictions, and untestable success criteria. For each finding, explain the downstream consequence — what would break if this gap propagated into architecture, decomposition, and implementation.

## Context
This scope document will be consumed by an architecture step, a UX step, and a deliverable decomposition step. Each of those steps trusts this document. If a requirement is missing, the architecture will not account for it. If a requirement is ambiguous, each downstream step will interpret it differently. If a success criterion is untestable, the team will not know when the deliverable is done.

## Constraints
- Find at least 3 specific problems. If you cannot find 3, state that the document is unusually complete and identify the 1–2 areas where you have the lowest confidence.
- For each finding, provide: the specific text or gap, why it is a problem, and the downstream consequence.
- Do not list things the document does well. Your job is to find problems.
- Classify each finding as: BLOCKER (will cause downstream failure), MAJOR (will cause significant rework), or MINOR (will cause friction).
- Do not suggest fixes. Identifying the problem is your job. Fixing it is the producing agent's job.
- Output format: numbered list of findings, each with classification, description, and downstream consequence.
```

**Adversarial posture check**: Does the prompt tell the agent to find problems? Yes. Does it prohibit praise? Yes. Does it require a minimum number of findings? Yes. Does it prohibit suggesting fixes (which would make the agent a collaborator, not a critic)? Yes.

---

## Step 3: Build the Security and Feasibility Reviewer (20 minutes)

**Position**: After `create-architecture.md`, before `create-ux.md`

**Lens**: What architectural decisions are insecure, infeasible given stated constraints, or unsupported by evidence? The architecture document makes commitments that the rest of the pipeline depends on. If a commitment is infeasible, every downstream plan is built on a false assumption.

**What this agent is NOT checking**: Whether the architecture document is well-structured or covers the required sections. Whether the technology choices are "good." Those are quality concerns the producing agent handles.

**Key failure modes to probe**:
- Security blind spots — authentication, authorization, data protection, and attack surface assumptions that are missing or hand-waved
- Feasibility gaps — technology choices that conflict with stated constraints (budget, team skills, timeline, infrastructure)
- Scalability assumptions that are stated as facts without evidence or load estimates
- Integration points that are assumed to be simple but have no interface contract defined
- Single points of failure that are not acknowledged

Write the adversarial prompt as `adversarial-security-feasibility.md`:

```markdown
## Role
You are a security architect and feasibility auditor reviewing an architecture document for a system that is about to be built. Your job is to find the decisions that will cause security incidents or implementation failure. You are not here to validate the architecture. You are here to break it.

## Task
Analyze the architecture document and produce a findings report focused on security vulnerabilities, infeasible decisions, and unsupported assumptions. For each finding, explain what would happen during implementation or in production if this issue is not addressed.

## Context
This architecture document will be used to decompose work into deliverables and to plan implementation. If a technology choice is infeasible, the plan will be built around something that cannot be delivered. If a security decision is missing, the implementation will ship with a vulnerability. If an integration is assumed simple, the plan will not allocate time for it.

## Constraints
- Find at least 3 specific problems. If you cannot find 3, identify the areas where you have the lowest confidence and explain why.
- For each finding, provide: the specific decision or gap, the security or feasibility risk, and what would happen in production or during implementation.
- Classify each finding as: BLOCKER (security vulnerability or infeasible decision that will block implementation), MAJOR (significant risk that will cause delays or rework), or MINOR (risk that should be documented but is unlikely to block).
- Do not suggest architectural alternatives. Your job is to identify problems, not redesign the system.
- Do not comment on document quality, formatting, or completeness of sections.
- Output format: numbered list of findings, each with classification, description, and production/implementation consequence.
```

---

## Step 4: Build the UX Edge Case and Feasibility Reviewer (20 minutes)

**Position**: After `create-ux.md`, before `decompose-to-deliverables.md`

**Lens**: What user flows break under edge cases, error states, empty states, or accessibility constraints? The UX document describes the happy path. This agent looks for everything that happens when the user does something unexpected, when data is missing, or when the system fails.

**What this agent is NOT checking**: Whether the UX document is well-designed or whether the user flows are clear on the happy path. The producing agent handles happy-path quality.

**Key failure modes to probe**:
- Error states with no defined user experience (what does the user see when the API fails?)
- Empty states with no defined experience (what does the user see on first load with no data?)
- Loading states that are missing or undefined
- Accessibility gaps — interactions that require sight, mouse-only flows, no keyboard navigation, no screen reader considerations
- User flows that assume a specific device, screen size, or network condition without accounting for alternatives
- Edge cases in user input that have no defined handling (extreme values, special characters, very long text, concurrent edits)

Write the adversarial prompt as `adversarial-ux-edge-cases.md`:

```markdown
## Role
You are a UX auditor specializing in failure states, edge cases, and accessibility. You are reviewing a UX document to find every user-facing scenario that the document does not account for. You are not here to evaluate the design. You are here to find the gaps that will cause user frustration or lock out users with different abilities.

## Task
Analyze the UX document and produce a findings report that identifies missing error states, undefined edge cases, accessibility gaps, and device/interaction assumptions. For each finding, describe the user scenario that would be affected and what the user would experience.

## Context
This UX document feeds into deliverable decomposition. If an error state is undefined, no deliverable will be created for it, and it will be missing from the implementation. If an accessibility gap is not identified, it will not be planned for and will reach production. Every gap here becomes a gap in the deliverable set.

## Constraints
- Find at least 3 specific problems. If you cannot find 3, identify the user scenarios where you have the lowest confidence that the UX is complete.
- For each finding, provide: the specific gap, the user scenario that exposes it, and what the user would experience.
- Classify each finding as: BLOCKER (a user scenario that has no defined experience at all), MAJOR (a scenario with a partial or inadequate experience), or MINOR (a refinement that would improve the experience but is not a gap).
- Do not suggest UX designs or redesigns. Your job is to find missing scenarios, not to design them.
- Do not evaluate the happy-path design quality.
- Output format: numbered list of findings, each with classification, gap description, and user experience consequence.
```

---

## Step 5: Build the Coverage and Dependency Reviewer (20 minutes)

**Position**: After `decompose-to-deliverables.md`, before `plan-deliverable.md`

**Lens**: What requirements from the scope document have no corresponding deliverable? What dependencies between deliverables are hidden or unaccounted for? The decomposition step's job is to break the work into deliverables — this agent checks whether the breakdown actually covers everything and whether the dependency graph is honest.

**What this agent is NOT checking**: Whether the deliverables are well-formatted or properly structured. Whether the decomposition followed the right format. Those are the producing agent's concerns.

**Key failure modes to probe**:
- Requirements from the scope document that have no corresponding deliverable
- Deliverables that have implicit dependencies on other deliverables but do not declare them
- Deliverables that are too large to plan as a single unit (hidden sub-deliverables)
- Deliverables that overlap (two deliverables claim the same work)
- Deliverables that depend on infrastructure or setup work that is not itself a deliverable

Write the adversarial prompt as `adversarial-coverage-dependency.md`:

```markdown
## Role
You are a project auditor reviewing a deliverable decomposition for coverage gaps and hidden dependencies. Your job is to find the work that was missed, the dependencies that were not declared, and the deliverables that are secretly two deliverables. You are not here to validate the decomposition. You are here to find what will cause sprint planning failure.

## Task
Compare the deliverable list against the scope document and produce a findings report that identifies: requirements with no deliverable, undeclared dependencies between deliverables, oversized deliverables, overlapping deliverables, and missing foundational work. For each finding, explain the planning consequence — what would go wrong during planning or implementation.

## Context
This deliverable list will be used to plan individual deliverables. If a requirement has no deliverable, it will be silently dropped. If a dependency is undeclared, the dependent deliverable will be planned as if it can proceed independently. If a deliverable is secretly two deliverables, the plan will under-estimate the work. Every gap here becomes a planning failure.

## Constraints
- You MUST trace each requirement from the scope document to at least one deliverable. Any requirement that cannot be traced is a finding.
- Find at least 3 specific problems. If you cannot find 3, state that the coverage is unusually complete and identify the 1–2 areas where dependency mapping has the lowest confidence.
- For each finding, provide: the specific gap or issue, the requirement or deliverable affected, and the planning consequence.
- Classify each finding as: BLOCKER (a requirement with no deliverable, or a circular dependency), MAJOR (an undeclared dependency or oversized deliverable), or MINOR (a minor overlap or ambiguity).
- Do not suggest how to restructure the deliverables. Your job is to find gaps, not to fix them.
- Output format: numbered list of findings, each with classification, description, and planning consequence. Include a coverage traceability table mapping each requirement to its deliverable(s) or noting the gap.
```

---

## Step 6: Build the Plan Critique Reviewer (20 minutes)

**Position**: After `plan-deliverable.md`, before `create-deliverable.md`

**Lens**: What in the plan is under-specified, over-scoped, or likely to fail during implementation? The plan is the bridge between understanding what to build and actually building it. This agent attacks the plan's assumptions, its scope boundaries, and its implementation strategy.

**What this agent is NOT checking**: Whether the plan follows the correct format or has all required sections. The producing agent handles structural quality.

**Key failure modes to probe**:
- Implementation steps that are under-specified (the step says what to do but not how, leaving the create-deliverable agent to guess)
- Scope creep hidden in the plan (the plan includes work beyond what the deliverable description calls for)
- Missing acceptance criteria or acceptance criteria that are untestable
- Assumptions about the codebase, existing patterns, or available libraries that may not hold
- Steps that depend on outcomes of previous steps without acknowledging the dependency
- Testing or verification approach that is absent or inadequate

Write the adversarial prompt as `adversarial-plan-critique.md`:

```markdown
## Role
You are a senior engineer reviewing a deliverable plan for implementation risk. Your job is to find the parts of the plan that will cause the implementation agent to fail, go off-scope, or produce something that does not meet the acceptance criteria. You are not here to approve the plan. You are here to find where it will break.

## Task
Analyze the deliverable plan and produce a findings report that identifies under-specified steps, scope creep, untestable acceptance criteria, unsupported assumptions, and missing verification. For each finding, explain what would happen during implementation if this issue is not addressed.

## Context
This plan will be consumed by an implementation agent that will follow it step by step. If a step is under-specified, the implementation agent will fill the gap with its own assumptions, which may not match intent. If the acceptance criteria are untestable, the implementation agent will not know when it is done. If there is scope creep, the implementation agent will produce more than asked for, wasting effort and potentially breaking other deliverables.

## Constraints
- Find at least 3 specific problems. If you cannot find 3, identify the steps where implementation risk is highest even if the plan appears sound.
- For each finding, provide: the specific plan section or step, the risk it creates, and what would happen during implementation.
- Classify each finding as: BLOCKER (the plan cannot be implemented as written), MAJOR (the plan will produce incorrect or incomplete output), or MINOR (the plan will work but with friction or inefficiency).
- Do not rewrite the plan. Your job is to find problems, not to fix them.
- Do not evaluate plan formatting or structure.
- Output format: numbered list of findings, each with classification, description, and implementation consequence.
```

---

## Step 7: Build the Standards and Compliance Reviewer (20 minutes)

**Position**: After `create-deliverable.md`, before `review-deliverable.md`

**Lens**: What established standards, conventions, integration contracts, or regulatory requirements does the deliverable violate? The producing agent checks whether the deliverable meets the plan's acceptance criteria. This agent checks whether the deliverable meets the broader standards that the plan may not have enumerated.

**What this agent is NOT checking**: Whether the deliverable is functionally correct or meets the plan's acceptance criteria. The producing agent's self-evaluation and the review-deliverable step handle that. This agent's lens is external standards and conventions — things the producing agent would not check because they are outside the plan's scope.

**Key failure modes to probe**:
- Code that violates the project's established patterns or conventions (naming, structure, error handling style)
- Integration contract violations — the deliverable's interface does not match what consuming components expect
- Missing error handling or logging that the project standard requires
- Security practices that the project mandate requires but the plan did not call out (input validation, output encoding, secrets handling)
- Accessibility or regulatory requirements that apply to the project but were not in the plan
- Test coverage that does not meet the project's minimum bar

Write the adversarial prompt as `adversarial-standards-compliance.md`:

```markdown
## Role
You are a standards and compliance auditor reviewing a deliverable against external standards, project conventions, and integration contracts that the implementation plan may not have enumerated. Your job is to find violations that would pass the plan's acceptance criteria but fail in the broader project context. You are not here to evaluate whether the deliverable works. You are here to find where it violates the rules it was not explicitly told about.

## Task
Analyze the deliverable and produce a findings report that identifies standards violations, convention breaches, integration contract mismatches, and missing compliance elements. For each finding, explain what standard or contract is violated and what the consequence would be in the project context.

## Context
This deliverable was built against a plan that specified what to build. The plan may not have enumerated every project convention, integration contract, or regulatory requirement. The deliverable could meet every acceptance criterion in the plan and still violate project standards. Your job is to find those violations before the deliverable is reviewed and integrated.

## Constraints
- Find at least 3 specific problems. If you cannot find 3, identify the areas where you cannot verify compliance because the standards are not documented, and flag that as a finding.
- For each finding, provide: the specific violation, the standard or contract being violated, and the integration or compliance consequence.
- Classify each finding as: BLOCKER (violation that will cause integration failure or a compliance issue), MAJOR (violation that will require rework before integration), or MINOR (violation that should be fixed but will not block integration).
- Do not fix the violations. Your job is to identify them.
- Do not evaluate functional correctness against the plan's acceptance criteria — that is the review step's job, not yours.
- If the project has no documented standards, state that as a BLOCKER finding — the absence of standards is itself a compliance risk.
- Output format: numbered list of findings, each with classification, violation description, standard/contract reference, and consequence.
```

---

## Step 8: Build the Review Quality Reviewer (20 minutes)

**Position**: After `review-deliverable.md`, at the end of the pipeline

**Lens**: Did the review actually catch real issues, or did it rubber-stamp the deliverable? This is the meta-adversarial agent — it attacks the review itself. A review that says "the deliverable looks good" without identifying specific issues is not a review. It is approval theater.

**What this agent is NOT checking**: Whether the deliverable being reviewed is good. That is the review step's job. This agent checks whether the review did its job.

**Key failure modes to probe**:
- The review report contains no specific findings (only general statements like "the code is well-structured")
- The review report lists findings but none are classified as blocking or major (everything is minor — a sign of rubber-stamping)
- The review report does not reference specific code, sections, or artifacts (findings are generic enough to apply to any deliverable)
- The review report's findings are all about style or formatting, with no functional or correctness issues (avoiding hard findings)
- The review report does not verify acceptance criteria — it does not trace each criterion to evidence of compliance
- The review report accepts the deliverable without any findings at all (a zero-finding review is suspicious, not reassuring)

Write the adversarial prompt as `adversarial-review-quality.md`:

```markdown
## Role
You are a review auditor examining a review report to determine whether the review caught real issues or rubber-stamped the deliverable. Your job is to find evidence that the review was shallow, generic, or avoided hard findings. You are not here to evaluate the deliverable. You are here to evaluate the review.

## Task
Analyze the review report and produce a findings report that identifies: missing specificity, absence of blocking or major findings, lack of acceptance criteria traceability, generic findings that could apply to any deliverable, and suspicious zero-finding reviews. For each finding, explain what the review should have done instead.

## Context
The review report is the last gate before a deliverable is accepted. If the review is shallow, defects pass through to production. A review that finds nothing is not necessarily a sign of a perfect deliverable — it may be a sign of a review that did not look hard enough. Your job is to determine whether the review earned its conclusion.

## Constraints
- Find at least 2 specific problems with the review. If the review is genuinely rigorous, state that and identify the 1 area where the review's confidence is least supported by evidence.
- For each finding, provide: the specific weakness in the review, what the review should have done instead, and the risk of letting the review stand as-is.
- Classify each finding as: BLOCKER (the review rubber-stamped and cannot be trusted), MAJOR (the review has significant gaps that undermine its conclusion), or MINOR (the review is adequate but has room for improvement).
- A review with zero findings is automatically a BLOCKER finding unless the deliverable is trivially simple and the review provides specific evidence for why each acceptance criterion is met.
- A review with only minor/style findings and no functional findings is automatically a MAJOR finding.
- Do not re-review the deliverable yourself. Your job is to evaluate the review's quality, not to replace it.
- Output format: numbered list of findings, each with classification, review weakness, and risk assessment.
```

---

## Step 9: Integrate the Adversarial Layer into Your Harness (25 minutes)

Your harness from Exercise 18 runs the 7-step pipeline. In Exercise 19, you added a single adversarial review agent as a guardrail. Now integrate all six adversarial agents.

For each guardrail point, the harness should:

1. Run the producing step
2. Run the corresponding adversarial agent on the producing step's output
3. Check the adversarial agent's findings for BLOCKER-classified issues
4. If BLOCKERs exist: halt the pipeline, log the findings, and prompt for human review
5. If no BLOCKERs: log the findings as advisory and proceed to the next producing step

Add this logic to your harness. You do not need to halt on MAJOR or MINOR findings — those are advisory and should be logged but not blocking. The distinction matters: BLOCKERs are issues that will cause downstream failure. MAJORs are issues that will cause rework. MINORs are friction. Only BLOCKERs should halt the pipeline.

```bash
#!/bin/bash
# adversarial-layer-run.sh — runs the full pipeline with adversarial guardrails

# Each adversarial agent writes findings to a JSON file with a "findings" array.
# Each finding has a "classification" field: "blocker", "major", or "minor".
# This function checks for blockers and halts if found.

check_blockers() {
  local FINDINGS_FILE="$1"
  local AGENT_NAME="$2"

  if [ ! -f "$FINDINGS_FILE" ]; then
    echo "ADVERSARIAL HALT: $AGENT_NAME did not produce a findings file."
    exit 1
  fi

  BLOCKER_COUNT=$(jq '[.findings[] | select(.classification == "blocker")] | length' "$FINDINGS_FILE")

  if [ "$BLOCKER_COUNT" -gt 0 ]; then
    echo "ADVERSARIAL HALT: $AGENT_NAME found $BLOCKER_COUNT blocker(s)."
    jq '.findings[] | select(.classification == "blocker")' "$FINDINGS_FILE"
    echo "Pipeline halted. Review the findings and address blockers before re-running."
    exit 1
  fi

  MAJOR_COUNT=$(jq '[.findings[] | select(.classification == "major")] | length' "$FINDINGS_FILE")
  MINOR_COUNT=$(jq '[.findings[] | select(.classification == "minor")] | length' "$FINDINGS_FILE"
  echo "ADVERSARIAL ADVISORY: $AGENT_NAME found $MAJOR_COUNT major, $MINOR_COUNT minor. Proceeding."
}
```

Adapt this to your harness structure. The key integration points:

- After `create-scope` runs → invoke `adversarial-requirements-completeness.md` on the scope output → `check_blockers`
- After `create-architecture` runs → invoke `adversarial-security-feasibility.md` on the architecture output → `check_blockers`
- After `create-ux` runs → invoke `adversarial-ux-edge-cases.md` on the UX output → `check_blockers`
- After `decompose-to-deliverables` runs → invoke `adversarial-coverage-dependency.md` on the deliverables output → `check_blockers`
- After `plan-deliverable` runs → invoke `adversarial-plan-critique.md` on the plan output → `check_blockers`
- After `create-deliverable` runs → invoke `adversarial-standards-compliance.md` on the deliverable output → `check_blockers`
- After `review-deliverable` runs → invoke `adversarial-review-quality.md` on the review output → `check_blockers`

---

## Step 10: Test the Adversarial Layer (25 minutes)

Run your harness on a product description you have used before (DevLog or another domain from your Exercise 11 runs). Observe what each adversarial agent finds.

Create `adversarial-layer-test-results.md`:

```markdown
## Adversarial Layer Test Results — [date]

### Pipeline Run
Product: [name]
Date: [date]

### Adversarial Findings by Guardrail Point

**Requirements Completeness Reviewer (after create-scope):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]
- Did this finding propagate downstream? [trace what happened in later steps]

**Security and Feasibility Reviewer (after create-architecture):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]

**UX Edge Case and Feasibility Reviewer (after create-ux):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]

**Coverage and Dependency Reviewer (after decompose-to-deliverables):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]
- Coverage traceability gaps: [any requirements with no deliverable]

**Plan Critique Reviewer (after plan-deliverable):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]

**Standards and Compliance Reviewer (after create-deliverable):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]

**Review Quality Reviewer (after review-deliverable):**
- Blockers: [count and summary]
- Majors: [count and summary]
- Minors: [count and summary]
- Most significant finding: [description]

### Cross-Adversarial Analysis
[2–3 paragraphs answering: Did different adversarial agents find related issues? Did an upstream adversarial finding predict a downstream problem? Did any adversarial agent find nothing — and is "nothing" credible or suspicious?]

### Pipeline Halt Analysis
- Did any adversarial agent halt the pipeline with a BLOCKER? [Yes/No]
- If yes: which agent, what was the blocker, how did you address it?
- If no: is the absence of blockers credible, or do you suspect the adversarial prompts are too lenient?

### Anti-Pattern Check
For each adversarial agent, answer honestly:
- Did this agent find something the producing agent's self-evaluation would NOT have caught?
- If no, the lens is too close to "quality" and needs sharpening.
```

---

## Step 11: Commit

Commit the following:

- `adversarial-layer-map.md` — the design document from Step 1
- Six adversarial agent prompt files:
  - `adversarial-requirements-completeness.md`
  - `adversarial-security-feasibility.md`
  - `adversarial-ux-edge-cases.md`
  - `adversarial-coverage-dependency.md`
  - `adversarial-plan-critique.md`
  - `adversarial-standards-compliance.md`
  - `adversarial-review-quality.md`
- Updated harness with adversarial layer integration
- `adversarial-layer-test-results.md`

---

## Self-Check

- [ ] `adversarial-layer-map.md` committed before any adversarial prompts were written
- [ ] Six adversarial agent prompts written, each with a distinct lens
- [ ] No two adversarial agents share the same lens — each targets different failure modes
- [ ] Each adversarial prompt has an explicitly adversarial posture (find problems, prohibit praise, require minimum findings, prohibit fix suggestions)
- [ ] Each adversarial prompt states what it is NOT checking (to avoid the redundant second opinion anti-pattern)
- [ ] The Review Quality Reviewer exists and attacks the review step itself, not the deliverable
- [ ] Harness integrated with all six adversarial guardrail points
- [ ] Harness halts on BLOCKER findings and logs MAJOR/MINOR as advisory
- [ ] `adversarial-layer-test-results.md` documents findings from a real pipeline run
- [ ] Anti-pattern check completed for each agent in the test results
- [ ] For each agent, you can answer the question: "What would break that the producing agent's own evaluation would NOT catch?" — if you cannot, the lens needs sharpening