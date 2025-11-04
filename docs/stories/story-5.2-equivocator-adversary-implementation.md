# Story 5.2: Equivocator Adversary Implementation

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As an Equivocator adversary,
I want to send conflicting values to different honest nodes within same phase,
So that I can test CoD equivocation detection and protocol safety.

## Acceptance Criteria

1. Create `EquivocatorAdversary` class inheriting from `AdversaryStrategy`
2. `intercept_send(message)` generates multiple conflicting messages:
   - Same `(round, protocol_id, phase, sender_id)`
   - Different `value` fields
   - Each message signed correctly (adversary has valid keys)
3. Send different values to different recipients (targeted equivocation)
4. Equivocation only in specified phases (e.g., CoD SEND phase)
5. Track equivocation events for logging
6. Unit tests covering: message splitting, conflicting values, signature validity
7. Integration test: Equivocator triggers CoD equivocation detection

## Prerequisites

Story 5.1

## Notes

Tests protocol resilience against conflicting messages.
