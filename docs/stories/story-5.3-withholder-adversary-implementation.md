# Story 5.3: Withholder Adversary Implementation

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As a Withholder adversary,
I want to suppress terminal-phase messages until late rounds,
So that I can test certificate ∨ timeout advancement and early-stopping resilience.

## Acceptance Criteria

1. Create `WithholderAdversary` class inheriting from `AdversaryStrategy`
2. Configuration: withhold_until_round parameter
3. `intercept_send(message)` behavior:
   - If message is terminal-phase (READY, GRADE_VOTE) → buffer message
   - Release buffered messages after withhold_until_round
4. Withholder delays certificate formation, forcing timeout advancement
5. Eventually releases messages (not permanent silence)
6. Unit tests covering: message buffering, release logic, phase targeting
7. Integration test: Withholder prevents early certificate, protocol advances via timeout

## Prerequisites

Story 5.1

## Notes

Tests timeout-based advancement when certificates are delayed.
