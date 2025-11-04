# Story 4.2: Subprotocol Sequencing - PoP → CoD → GDA

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA controller,
I want to sequence PoP, CoD, GDA subprotocols within each round,
So that protocols execute in correct order with proper state transitions.

## Acceptance Criteria

1. Implement `run_round(round: int)` async method orchestrating subprotocols
2. Sequencing order: LitePoP → CoD → GDA
3. Each subprotocol runs to completion before next starts
4. State transitions logged: PoP complete, CoD complete, GDA complete
5. Pass outputs between protocols: CoD output → GDA input
6. Handle subprotocol failures gracefully (timeout, no certificate)
7. Unit tests covering: correct sequencing, state transitions, output passing
8. Integration test: full round execution through all three subprotocols

## Prerequisites

Story 4.1

## Notes

Orchestrates the three-phase subprotocol sequence per round.
