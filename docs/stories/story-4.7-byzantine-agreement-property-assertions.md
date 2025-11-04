# Story 4.7: Byzantine Agreement Property Assertions

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA validator,
I want always-on assertions for Agreement, Validity, Termination properties,
So that correctness violations halt execution immediately with diagnostics.

## Acceptance Criteria

1. Create `assertions.py` module with property checking functions
2. `assert_agreement(decisions: Dict[int, Any])` checks no two honest nodes decide differently
3. `assert_validity(inputs: Dict[int, Any], decision: Any)` checks unanimous input preserved
4. `assert_termination(round: int, max_rounds: int)` checks bounded termination
5. Assertions run after each round and at final decision
6. Assertion failure: halt execution, dump full state, log violation details
7. Unit tests covering: valid executions pass, violations detected
8. Integration test: property violations trigger immediate failure

## Prerequisites

Story 4.3

## Notes

Property assertions ensure correctness - fail-fast on violations.
