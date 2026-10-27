# [Skill name] - Invocation Tests

**Skill:** skills/[skill-name]/SKILL.md
**Prerequisite:** baseline plus 3 documented iterations in the run log (confirmed: [yes/no])

## Positive Trigger [N]
**User message:** [A message that SHOULD invoke the skill]
**Expected:** The skill is invoked.
**Observed:** [invoked | not invoked]
**Evidence:** [transcript excerpt or file path]

## Negative Trigger [N]
**User message:** [A message that must NOT invoke the skill]
**Expected:** The skill is not invoked.
**Observed:** [invoked | not invoked]
**Evidence:** [transcript excerpt or file path]

## Quality Test [N]
**User message:** [A message that invokes the skill]
**Expected:** The output meets the skill's EC file at the pass threshold.
**Observed score:** [NN.N%]
**Evidence:** [results file path]
