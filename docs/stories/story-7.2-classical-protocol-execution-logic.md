# Story 7.2: Classical Protocol Execution Logic

**Epic:** Epic 7 - Classical Baseline Implementation
**Week:** Weeks 13-14

## User Story

As a classical BA,
I want deterministic execution with (t+1) worst-case termination,
So that I demonstrate classical behavior for baseline comparison.

## Acceptance Criteria

1. Implement `run_classical_ba(n: int, t: int, input_value: Any) -> Any` function
2. Protocol phases: PROPOSE → VOTE → DECIDE
3. PROPOSE phase: broadcast initial value
4. VOTE phase: collect proposals, determine majority or default
5. DECIDE phase: after t+1 rounds, decide based on accumulated votes
6. Worst-case termination: always decide by round t+1 regardless of faults
7. Unit tests covering: all phases, termination at t+1 rounds
8. Integration test: n=7, t=3 → decision at round 4 (t+1)

## Prerequisites

Story 7.1

## Notes

Demonstrates classical (t+1) termination behavior.
