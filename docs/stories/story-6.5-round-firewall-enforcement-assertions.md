# Story 6.5: Round Firewall Enforcement with Assertions

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As a validator,
I want round firewall enforcement via assertions,
So that post-round messages never mutate state (fail-fast on violations).

## Acceptance Criteria

1. Extend message processing with round firewall checks
2. Before processing any message: `assert message.round >= current_round` (not retroactive)
3. Late messages (round < current) logged but NEVER processed for state mutation
4. Assertion failure: halt execution, dump state, report violation
5. Round firewall test: deliberately send late message, verify assertion fires
6. Unit tests covering: current round accepted, late round rejected with assertion
7. Integration test: round firewall violations detected across full BA execution

## Prerequisites

Story 2.7

## Notes

Round firewall is critical for correctness - prevents retroactive mutations.
