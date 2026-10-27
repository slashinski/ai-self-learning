# Scope Document: Pomodoro Timer Application

**Author:** Stephen Lashinski
**Date:** 2026-10-27
**Status:** Draft for review

## 1. Summary

This project delivers a Progressive Web App (PWA) that runs 25-minute focus intervals and 5-minute breaks, records every completed session, and shows a weekly productivity heat map. I recommend a React and TypeScript front end hosted on Azure Static Web Apps, with Entra ID sign-in and Azure Functions backed by Azure Cosmos DB for session storage. The tradeoff is that a fully local-only build would ship faster, but it would not sync across devices or give us a clean path to internal use, so I am recommending the hosted option.

## 2. Objectives

The application should help an individual user run consistent focus cycles, see how much focused work they completed, and identify the days and times when they are most productive. Success is measured by a user being able to start a timer, finish a cycle, and view that session reflected in the heat map within the same day.

## 3. In Scope

### 3.1 Timer
- Work interval fixed at 25 minutes and break interval fixed at 5 minutes.
- Automatic transition from work to break and from break to the next work interval.
- Start, pause, resume, reset, and skip controls.
- Timer accuracy based on timestamps rather than tick counting, so it stays correct when the browser tab is throttled or the device sleeps.
- Audible and visual notification at each interval end, with browser Notification API permission handling.

### 3.2 Session Tracking
- A session is logged when a 25-minute work interval completes. Interrupted or reset intervals are recorded with an "abandoned" status and excluded from productivity totals.
- Each record stores start time, end time, duration, status, and an optional short label.
- A history view listing sessions by day, with the ability to edit a label or delete a record.
- Daily summary showing completed sessions and total focus minutes.

### 3.3 Weekly Productivity Heat Map
- A grid of days of the week against hours of the day, with cell intensity based on completed focus minutes.
- Week navigation (previous, next, current) and a hover or tap detail showing exact minutes and session count.
- Week boundaries follow the user's local time zone, with Monday as the default start day.
- Accessible color scale that meets WCAG 2.1 AA contrast, plus numeric values available to screen readers.

### 3.4 Platform and Identity
- Responsive web UI for desktop and mobile browsers, installable as a PWA.
- Entra ID sign-in using the organization tenant, with session data keyed to the user's object ID only.
- Local-first storage in IndexedDB so the timer works offline, with sync to the backend when connected.

## 4. Out of Scope

Configurable interval lengths, long breaks after four cycles, team or manager dashboards, task management integrations, Teams app packaging, native mobile apps, gamification, and data export are excluded from this release. Long breaks and configurable intervals are the most likely candidates for a phase two.

## 5. Proposed Architecture

| Layer | Choice |
|---|---|
| Front end | React, TypeScript, Vite, PWA service worker |
| Hosting | Azure Static Web Apps |
| Auth | Entra ID via Static Web Apps built-in authentication |
| API | Azure Functions (Node.js, TypeScript) |
| Data | Azure Cosmos DB, partitioned by user ID |
| Offline storage | IndexedDB with a sync queue |
| Observability | Application Insights |
| CI/CD | GitHub Actions or Azure DevOps Pipelines |

The heat map aggregation runs client-side from the week's session records, which keeps the API to simple create, read, update, and delete operations.

## 6. Data Model

A session document contains `id`, `userId`, `startedAt` (UTC), `endedAt` (UTC), `durationSeconds`, `type` (work or break), `status` (completed or abandoned), `label`, and `timeZone`. Break intervals are stored for completeness but do not count toward the heat map.

## 7. Non-Functional Requirements

Timer drift must stay under one second per interval. The initial load should complete in under three seconds on a typical broadband connection. All data is encrypted in transit and at rest, access is restricted to the owning user, and application logs must not contain session labels. These controls align with CIS Controls 3 and 6 and support SOC 2 Type II expectations for access control and data protection if the app is adopted internally.

## 8. Deliverables

1. Working PWA deployed to a non-production Azure environment.
2. Infrastructure as code (Bicep) for all Azure resources.
3. Automated unit tests for timer logic and heat map aggregation, plus end-to-end tests for the core flow.
4. Short README covering setup, deployment, and architecture.

## 9. Milestones

| Phase | Duration | Outcome |
|---|---|---|
| 1. Foundation | Week 1 | Repo, CI/CD, Bicep, auth, app shell |
| 2. Timer and tracking | Weeks 2 to 3 | Timer engine, notifications, session logging, history |
| 3. Heat map | Week 4 | Aggregation, visualization, accessibility pass |
| 4. Sync and hardening | Week 5 | Offline sync, testing, performance, security review |
| 5. Release | Week 6 | UAT, fixes, production deployment |

This assumes one full-stack developer and part-time review support.

## 10. Assumptions and Dependencies

An Azure subscription and Entra ID app registration are available. Users are internal Improving staff on current versions of Edge, Chrome, or Safari. No client data or client source code is involved, and no personnel records are stored beyond the Entra object ID.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Browser throttling causes timer inaccuracy | Timestamp-based calculation, tested against background tab behavior |
| iOS PWA notification limitations | Document the limitation and provide in-app alerts as a fallback |
| Offline sync conflicts | Append-only session records with client-generated IDs |
| Time zone and daylight saving errors in the heat map | Store UTC with the original time zone and test across DST boundaries |

## 12. Acceptance Criteria

The release is accepted when a signed-in user can complete a full 25/5 cycle with correct notifications, see the session appear in history, view it in the correct heat map cell for the current week, navigate to prior weeks, and continue using the timer offline with data syncing on reconnection.
