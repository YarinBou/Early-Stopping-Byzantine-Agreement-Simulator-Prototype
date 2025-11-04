# Story 2.8: Complete Certificate ∨ Timeout Advancement

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a round scheduler,
I want certificate-or-timeout advancement rule fully integrated,
So that rounds progress either when n-t certificate forms OR Δ timeout expires.

## Acceptance Criteria

1. Integrate `CertificateTracker` (Story 2.4) with `RoundScheduler` (Story 2.1)
2. `wait_for_advancement(n: int, t: int, delta: float) -> str` async method
3. Advancement triggers:
   - Early: n-t terminal-phase messages → return "certificate"
   - Fallback: Δ timeout expires → return "timeout"
4. Advancement reason recorded in transition log
5. Carryover state resolved BEFORE round increment
6. Round advancement test: certificate-based advancement faster than timeout
7. Integration test: timeout advancement when only n-t-1 messages arrive
8. Performance: advancement detection within 10ms of condition met

## Prerequisites

Stories 2.2, 2.3, 2.4, 2.5

## Notes

Implements core novel pattern: Certificate ∨ Timeout advancement.
