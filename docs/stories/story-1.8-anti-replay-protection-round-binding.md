# Story 1.8: Anti-Replay Protection via Round Binding

**Epic:** Epic 1 - Foundation Infrastructure
**Week:** Weeks 1-4

## User Story

As a protocol validator,
I want messages rejected if they reference invalid rounds,
So that old messages cannot be replayed in future rounds (anti-replay protection).

## Acceptance Criteria

1. Extend `MessageValidator` with current round tracking
2. `set_current_round(round: int)` method updating validator state
3. Reject messages with `message.round < current_round` (too old)
4. Optionally reject messages with `message.round > current_round + 1` (too far ahead, configurable)
5. Round binding checked before deduplication (invalid rounds never enter seen set)
6. Clear logging when messages rejected due to round mismatch
7. Unit tests covering: current round accepted, old round rejected, future round handling
8. Integration test with round progression

## Prerequisites

Story 1.7

## Notes

Round binding prevents replay of old messages in new contexts.
