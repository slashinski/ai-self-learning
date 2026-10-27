---
name: create-prd
description: Create a developer-ready PRD for a browser-based Pomodoro timer application
disable-model-invocation: true
---

# Create PRD

## Role
Act as a Product Manager who writes Product Requirements Documents (PRDs) for software development teams.

## Task
Create a developer-ready PRD for a Pomodoro timer application that developers can use to plan, implement, and test the application.

## Context
The application is a browser-based Pomodoro timer with 25-minute work intervals, 5-minute breaks, session tracking, and a weekly productivity heat map.

The Pomodoro timer will help users improve focus and manage their time.

The intended audience is for a solo-developer or small development team.

## Constraints
1. The PRD must include the following sections:
   - Product Overview (Problem Statement & Goals)
   - Features (Personas, Use Cases, User Stories & Given/When/Then Acceptance Criteria)
   - Functional and Non-Functional Requirements
   - Key Implementation Details
   - Scope Boundaries
   - Success Metrics & Definition of Done
   - Dependencies, Assumptions & Open Questions

2. Requirements must be measurable, testable, and include verification criteria. Avoid vague language such as "responsive," "fast," or "accurate" without measurable definitions.

3. Address key technical considerations, including supported browsers, timer accuracy and lifecycle behavior, session tracking, heat map metrics and thresholds, accessibility, localStorage persistence, required browser capabilities and their purpose, and notification behavior with fallback scenarios.

4. The PRD should express technical considerations as observable, measurable outcomes.

5. Explicitly identify what is in scope and out of scope.

6. Identify unresolved questions, assumptions, and decisions that must be addressed before implementation begins.

7. The application is a browser-based web application with no native dependencies.

## Output Format
Return one Markdown document. It starts with its title as a level-1 heading, with no text before or after the document, then these metadata lines:

**Version:** <major.minor>
**Date:** <YYYY-MM-DD>
**Status:** Draft

A `## Changelog` section follows, with a Markdown table with the columns Version, Date, Author, and Changes, newest entry first. Use "Product Manager" as the author. 

## File Contract
Reads: the existing PRD at the output path, if there is one. Nothing else.

Writes: one Markdown PRD. If the caller passes a file path after the command (for example `/create-prd modules/module-1/exercise-2/results/create-prd.md`), write the PRD to that path. If no path is given, return the complete PRD in the reply and write no file.

Consumed by: create-architecture (uses PRD as input), create-epics-stories (uses PRD as input).

Versioning:
- New PRD: Version 1.0, one changelog row, Changes "Initial draft".
