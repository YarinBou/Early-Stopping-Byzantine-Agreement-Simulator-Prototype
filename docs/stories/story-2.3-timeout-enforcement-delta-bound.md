# Story 2.3: Timeout Enforcement with Δ Bound

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a round scheduler,
I want timeout-based round advancement after Δ expires,
So that protocol doesn't deadlock when certificates aren't formed.

## Acceptance Criteria

1. Add `wait_for_certificate_or_timeout(timeout_seconds: float)` async method
2. Uses `asyncio.wait_for` with Δ timeout
3. Returns `"certificate"` if advancement condition met before timeout
4. Returns `"timeout"` if Δ expires without certificate
5. Configurable Δ per round (default from constructor)
6. Timeout tracking: log timeout events for analysis
7. Unit tests covering: certificate advancement (fast), timeout advancement (slow), edge cases
8. Integration test: round advances via timeout when no certificate forms

## Prerequisites

Story 2.1

## Notes

Ensures liveness - protocol always progresses even without certificates.
