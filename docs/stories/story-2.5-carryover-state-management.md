# Story 2.5: Carryover State Management

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a protocol node,
I want carryover state (digests, partial certificates) managed between rounds,
So that information from incomplete protocols carries forward correctly.

## Acceptance Criteria

1. Extend `RoundScheduler` with carryover state storage: `Dict[str, Any]`
2. `set_carryover(key: str, value: Any)` method storing state for next round
3. `get_carryover(key: str) -> Any` method retrieving carryover from previous round
4. `clear_carryover()` method resetting carryover after round advancement
5. Carryover resolution happens BEFORE round advancement (state frozen)
6. Carryover includes: participation digests, partial vote counts, prune sets
7. Unit tests covering: set/get carryover, round boundary behavior, clearing
8. Integration test: carryover survives round transition, cleared after use

## Prerequisites

Story 2.1

## Notes

Manages state transitions between rounds for multi-round protocols.
