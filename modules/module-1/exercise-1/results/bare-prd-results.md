# bare-prd - Evaluation Results

- Timestamp: 2026-10-27 12:00:47
- Judge model: sonnet
- Usage: claude-sonnet-5-5; 6 call(s); input 22588 (uncached 12, cache write 17706, cache read 4870), output 6530; cost $0.1366
- Context note: every call also carries the account email and the organization instructions. The system prompt is replaced, but these are added by the harness and cannot be removed from the CLI call.

## Prompt

> Write a scope document for a Pomodoro timer application with 25-minute work intervals, 5-minute break intervals, session tracking, and a weekly productivity heat map.

## Summary

**Overall: FAIL** (34.5% of criteria met; threshold 95%)

| Stage | Result | Detail |
|---|---|---|
| Deterministic checks | FAIL | 4 of 11 passed |
| LLM judge | FAIL | 16 of 47 criteria passed |

| Test case | Result | Criteria passed | Average score | Failed criteria |
|---|---|---|---|---|
| PRD Contains Required Sections | FAIL | 4 of 10 | 2.7 | C1, C2, C6, C7, C9, F1 |
| Timer Accuracy | FAIL | 5 of 10 | 3.1 | C2, C4, C6, C7, F3 |
| Productivity Heat Map | FAIL | 4 of 10 | 2.7 | C3, C4, C5, C7, F1, F2 |
| Browser APIs and Notifications | FAIL | 0 of 7 | 1.7 | C1, C2, C3, C4, F1, F2, F3 |
| Developer Open Questions | FAIL | 3 of 10 | 2.7 | C2, C3, C5, C6, F1, F2, F3 |

## Deterministic checks

| Check | Result | Detail |
|---|---|---|
| starts-with: PRD starts with a title heading, no text before it | PASS | first line: '# Scope Document: Pomodoro Timer Application' |
| count: version metadata line | FAIL | 0 found (need 1) |
| count: date metadata line | PASS | 1 found (need 1) |
| count: status metadata line | PASS | 1 found (need 1) |
| headings: Changelog | FAIL | missing: Changelog |
| count: changelog table header | FAIL | 0 found (need 1) |
| changelog: PRD version and date match the topmost data row, and all four fields contain values | FAIL | missing the **Version:** or **Date:** line |
| headings: Product Overview, Features, Non-Functional, Key Implementation, Scope Boundaries, Success Metrics, Definition of Done, Dependencies, Assumptions, Open Questions | FAIL | missing: Product Overview, Features, Key Implementation, Scope Boundaries, Success Metrics, Definition of Done, Open Questions |
| headings: In Scope, Out of Scope | PASS | all present |
| count: Given/When/Then acceptance criteria | FAIL | 0 found (need 5+) |
| no-unmeasured: fast, responsive, accurate | FAIL | found: responsive |

## LLM judge

Scores run from 1 (clearly not met) to 5 (clearly met) and are the judge's own rating.

### PRD Contains Required Sections

| ID | Criterion | Result | Score | Reasoning |
|---|---|---|---|---|
| C1 | PRD contains a problem statement and why it exists. | FAIL | 1 | The document has a Summary and Objectives but no problem statement explaining the problem and why it exists. |
| C2 | PRD contains personas, use cases, user stories, and acceptance criteria(AC) adhering to the format of Given/When/Then behavior. | FAIL | 1 | No personas, use cases, or user stories are present. The single Acceptance Criteria paragraph is not in Given/When/Then format. |
| C3 | PRD contains technical requirements and constraints to understand the how. | PASS | 4 | Sections 5 and 6 cover the architecture, tech stack, and data model, and Section 3 includes technical constraints such as timestamp-based timing and IndexedDB offline storage. |
| C4 | PRD contains non-functional requirements to understand the quality and performance expectations. | PASS | 5 | Section 7 Non-Functional Requirements specifies timer drift, load time, encryption, access control, and logging, with accessibility (WCAG AA) also covered elsewhere. |
| C5 | PRD contains scope and boundaries to understand what is in scope and out of scope. | PASS | 5 | Sections 3 In Scope and 4 Out of Scope clearly define boundaries, including exclusions such as configurable intervals, long breaks, and data export. |
| C6 | PRD contains success metrics to understand the measure of success. | FAIL | 2 | Only a single sentence in Objectives defines success (start a timer, finish a cycle, see it in the heat map). There is no dedicated success metrics section with measurable KPIs. |
| C7 | PRD contains open questions, edge-case(s), and assumptions to understand what we don't know. | FAIL | 3 | Assumptions and a Risks table with edge cases (DST, throttling, sync conflicts) are present, but there is no open questions section. |
| C8 | PRD contains the dependencies and constraints to understand dependencies and constraints. | PASS | 4 | Section 10 Assumptions and Dependencies lists the Azure subscription, the Entra app registration, and supported browsers, though it is brief. |
| C9 | PRD contains changelog to understand the history of updates. | FAIL | 1 | There is no changelog or revision history, only an author, date, and status header. |
| F1 | PRD should not create or specify technical solutions that are not needed for implementation. | FAIL | 1 | The document specifies unneeded technical solutions: React, Vite, Cosmos DB, Azure Functions, Bicep, GitHub Actions or Azure DevOps, and a detailed data model. These go beyond what a PRD requires. |

### Timer Accuracy

| ID | Criterion | Result | Score | Reasoning |
|---|---|---|---|---|
| C1 | PRD explicitly defines acceptable timer drift tolerance (ex: plus/minus 2 seconds over a 25 minute session) | PASS | 3 | NFR section states 'Timer drift must stay under one second per interval,' which is an explicit tolerance, though it is brief and not tied to a specific measurement method. |
| C2 | PRD uses timestamps driven from `Date.now()`. | FAIL | 2 | The PRD specifies 'timestamps rather than tick counting' but never mentions Date.now() specifically, so the explicit requirement is only loosely met. |
| C3 | PRD calls out the issue of background throttling and identifies how to mitigate. | PASS | 4 | Throttling is named in 3.1 and in the Risks table with mitigation 'Timestamp-based calculation, tested against background tab behavior,' so the issue and its mitigation are both identified. |
| C4 | PRD addresses the question, "if a laptop sleeps mid-session, the app must decide what to do on wake?" (example: continue, complete, or invalidate). | FAIL | 2 | Sleep is mentioned only as 'stays correct when the device sleeps' with no decision on whether the session continues, completes, or is invalidated on wake. |
| C5 | PRD specifies whether or not pause timer is acceptable | PASS | 4 | Section 3.1 lists pause, resume, reset, and skip controls as in scope, which establishes that pausing is acceptable, though behavior of paused sessions is not detailed. |
| C6 | PRD states how active timer state is persisted or recovered. | FAIL | 2 | Local-first IndexedDB storage and sync are described for session data, but nothing states how an active running timer state is persisted or recovered after a reload or crash. |
| C7 | Acceptance Criteria are written and are testable. | FAIL | 2 | Section 12 gives a single paragraph of high-level acceptance criteria that is not broken into discrete, measurable, testable items. |
| F1 | PRD defines background throttling without defining how to mitigate. | PASS | 5 | Throttling is paired with a mitigation (timestamp-based calculation plus testing), so the failure does not occur. |
| F2 | PRD defines a setinterval without addressing timer drift. | PASS | 5 | No setInterval is defined, and timer drift is addressed via timestamp-based accuracy and a drift limit. |
| F3 | PRD addresses sleep without indication of what action to do. | FAIL | 2 | Sleep is addressed only as 'stays correct when the device sleeps' without stating what action to take on wake, which is the failure condition. |

### Productivity Heat Map

| ID | Criterion | Result | Score | Reasoning |
|---|---|---|---|---|
| C1 | PRD defines the tracking metric and handling of incomplete sessions. | PASS | 4 | Section 3.2 says completed work intervals are logged as sessions and interrupted or reset ones are recorded as 'abandoned' and excluded from productivity totals; the metric is completed focus minutes. |
| C2 | PRD specifies weekly day-by-hour grid layout, boundaries, and navigation. | PASS | 4 | Section 3.3 specifies a days-of-week by hours-of-day grid, week navigation (previous, next, current), local time zone boundaries, and Monday start. |
| C3 | PRD defines numerical intensity thresholds and accessibility requirements. | FAIL | 2 | Accessibility is covered (WCAG 2.1 AA contrast, numeric values for screen readers), but no numerical intensity thresholds are defined; intensity is only 'based on completed focus minutes'. |
| C4 | PRD establishes client-only scope without backend or accounts. | FAIL | 1 | The PRD explicitly requires a backend: Azure Functions, Cosmos DB, and Entra ID sign-in, which contradicts client-only scope. |
| C5 | PRD defines storage location (localStorage vs. IndexedDB vs. server), data retention limit, and behavior when storage is unavailable | FAIL | 2 | Storage is IndexedDB plus Cosmos DB, but no data retention limit is defined and there is no behavior specified for unavailable storage. |
| C6 | PRD specifies a concrete storage schema with field names and types (e.g., { id, startTime,    endTime, completed: boolean, type: 'work' / 'break' }) | PASS | 4 | Section 6 lists the fields id, userId, startedAt, endedAt, durationSeconds, type, status, label, and timeZone with some value types, though types are not fully explicit for all fields. |
| C7 | PRD defines how session data is stored, retained, and recovered after browser restart. | FAIL | 2 | Persistence is via IndexedDB with sync and Cosmos DB, which implies recovery across restarts, but retention and recovery after browser restart are not explicitly defined. |
| F1 | PRD introduces backend, authentication or syncing to cloud as requirements. | FAIL | 1 | The PRD introduces a backend (Azure Functions, Cosmos DB), Entra ID authentication, and cloud sync as requirements. |
| F2 | PRD omits metrics, grid definition, or heat intensity thresholds. | FAIL | 2 | Metrics and the grid are defined, but numerical heat intensity thresholds are omitted. |
| F3 | PRD fails to handle incomplete sessions. | PASS | 5 | Incomplete sessions are handled by being recorded as 'abandoned' and excluded from totals. |

### Browser APIs and Notifications

| ID | Criterion | Result | Score | Reasoning |
|---|---|---|---|---|
| C1 | PRD identifies required browser APIs and purpose. | FAIL | 2 | Only the Notification API, service worker, and IndexedDB are mentioned in passing; there is no explicit section listing the required browser APIs (Web Audio, Page Visibility, etc.) with their purposes. |
| C2 | PRD defines visual, audio, and system notifications when a session ends. | FAIL | 2 | It says 'Audible and visual notification at each interval end, with browser Notification API permission handling' in one line, with no definition of what each notification actually is (sound, on-screen banner, system notification). |
| C3 | PRD defines the complete fallback chain: what the user sees/hears if notification permission is denied, if audio context is suspended due to no prior user gesture, and if the tab is closed. | FAIL | 1 | No fallback chain is defined for denied permission, suspended AudioContext, or closed tab; only an iOS risk row mentions 'in-app alerts as a fallback'. |
| C4 | PRD defines expected behavior when the browser tab is hidden, closed or reopened. | FAIL | 2 | Hidden-tab behavior is partly covered by timestamp-based timing and throttling tests, but closed and reopened tab behavior is not defined. |
| F1 | PRD assumes browser notifications or audio always work. | FAIL | 2 | It mentions permission handling and an iOS fallback, but it largely assumes audio and notifications work, with no mention of audio autoplay restrictions or denied permission outcomes. |
| F2 | PRD introduces unnecessary backend services or approaches for basic notifications. | FAIL | 1 | It introduces Azure Functions, Cosmos DB, Entra ID, and sync for a basic timer, even though the request only needed local storage and client-side alerts. |
| F3 | PRD leaves background behaviors undefined. | FAIL | 2 | Background behavior is only partly addressed (timestamp-based accuracy); behavior for notifications when hidden, closed, or reopened is left undefined. |

### Developer Open Questions

| ID | Criterion | Result | Score | Reasoning |
|---|---|---|---|---|
| C1 | PRD defines timer transitions, controls, session completion, and interruption behavior. | PASS | 4 | Section 3.1 defines automatic transitions, start/pause/resume/reset/skip controls, and 3.2 covers completion and abandoned status. Interruption behavior such as tab throttling and sleep is covered, though pause-related session handling and skip semantics are underspecified. |
| C2 | PRD addresses data retention, accessibility, UI/UX expectations, and analytics requirements. | FAIL | 2 | Accessibility (WCAG 2.1 AA) and basic UI are covered, but data retention is not addressed at all, and analytics requirements are only minimally covered through the heat map and Application Insights. UI/UX expectations are thin. |
| C3 | PRD identifies measurable non-functional requirements and how they will be verified. | FAIL | 3 | Section 7 gives measurable targets (drift under one second, load under three seconds), but encryption and access controls lack verification methods, and the document does not say how any NFR will be verified. The load target is also vague ('typical broadband'). |
| C4 | PRD establishes boundaries, dependencies, and a definition of done. | PASS | 4 | Out of Scope section, Assumptions and Dependencies, Deliverables, and Acceptance Criteria establish boundaries and a definition of done. |
| C5 | PRD explicitly identifies unresolved decisions, assumptions, and questions requiring stakeholder input. | FAIL | 1 | There is no open questions section. Decisions such as CI/CD choice (GitHub Actions or Azure DevOps), hosted vs local, and retention are presented as settled or left unflagged, with no stakeholder questions listed. |
| C6 | PRD requirements are appropriate for a solo developer or small development team, without introducing unnecessary architectural complexity or enterprise-level dependencies. | FAIL | 2 | The architecture (Entra ID, Azure Functions, Cosmos DB, Bicep IaC, sync queue, offline PWA) is heavy for a simple Pomodoro timer and introduces unneeded cloud dependencies for a solo developer. |
| F1 | PRD leaves necessary development decisions ambiguous without identifying them as open questions. | FAIL | 2 | Several necessary decisions are left ambiguous without being flagged as open questions, including data retention, behavior on pause duration, skip semantics, CI/CD tool, and the abandoned session threshold. |
| F2 | PRD contains non-functional requirements without measurable acceptance criteria. | FAIL | 3 | Some NFRs are measurable, but 'encrypted in transit and at rest', 'access restricted to the owning user', and 'logs must not contain labels' have no measurable acceptance criteria. |
| F3 | PRD introduces unsupported functionality beyond the stated scope. | FAIL | 2 | The document adds functionality beyond the stated request, including Entra ID sign-in, cross-device sync, editing and deleting records, labels, history view, and PWA installability. |
| F4 | PRD lacks sufficient information for developers to estimate and plan implementation. | PASS | 4 | The document provides architecture, a data model, milestones, deliverables, and risks, which gives developers enough information to estimate and plan. |

