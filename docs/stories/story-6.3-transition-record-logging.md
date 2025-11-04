# Story 6.3: Transition Record Logging

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As an evidence store,
I want to log transition records for each round advancement,
So that I can audit advancement reasons (certificate vs. timeout) and timestamps.

## Acceptance Criteria

1. Extend `EvidenceStore` with transition record logging
2. Transition record fields: `{round, carryover_digest, advance_reason, advance_timestamp}`
3. `record_transition(round: int, reason: str, timestamp: float, carryover: bytes)` method
4. Advancement reason: "certificate" or "timeout"
5. Carryover digest: hash of carryover state proving consistency
6. Timestamps enable timing analysis (wall-clock vs. simulated time)
7. Unit tests covering: transition recording, field validation
8. Integration test: complete execution produces transition log for all rounds

## Prerequisites

Story 6.1

## Notes

Transition records enable audit of round progression.
