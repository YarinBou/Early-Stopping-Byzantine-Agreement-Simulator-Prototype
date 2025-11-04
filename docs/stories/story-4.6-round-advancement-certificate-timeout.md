# Story 4.6: Round Advancement with Certificate ∨ Timeout

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA controller,
I want round advancement triggered by certificate OR timeout,
So that protocol progresses either when subprotocols complete or Δ expires.

## Acceptance Criteria

1. Integrate `RoundScheduler` advancement (Story 2.8) with BA controller
2. After GDA completes, check for grade-2 certificate (early decision)
3. If no decision, wait for certificate ∨ timeout before advancing
4. Advancement reason logged: "certificate" or "timeout"
5. Timeout-based advancement continues protocol (no early termination)
6. Unit tests covering: certificate-based advancement, timeout fallback
7. Integration test: round advances via timeout when no grade-2 forms

## Prerequisites

Stories 2.8, 4.5

## Notes

Implements the Certificate ∨ Timeout novel pattern in BA context.
