# Story 4.5: Carryover State Integration with Subprotocols

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA controller,
I want to manage carryover state between rounds,
So that partial certificates, digests, and pruned sets carry forward correctly.

## Acceptance Criteria

1. Integrate carryover state from `RoundScheduler` (Story 2.5) into BA controller
2. Carryover includes: participation digest (PoP), partial vote counts, prune set
3. `prepare_carryover() -> Dict[str, Any]` method packaging state for next round
4. `restore_carryover(state: Dict[str, Any])` method loading previous round state
5. Carryover resolution happens BEFORE round advancement
6. Unit tests covering: carryover preparation, restoration, round boundaries
7. Integration test: state survives round transition, used correctly in next round

## Prerequisites

Stories 2.5, 4.2

## Notes

Manages state continuity across rounds.
