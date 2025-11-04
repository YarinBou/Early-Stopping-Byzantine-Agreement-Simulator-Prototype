# Story 4.4: Value Pruning Based on Graded Evidence

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA controller,
I want to prune impossible values based on graded evidence,
So that I converge toward consensus by eliminating values with low grades.

## Acceptance Criteria

1. Implement `prune_values(gda_output: (value, grade))` method
2. Pruning rule: if value receives grade < 1, eliminate from consideration
3. Maintain working set of viable values across rounds
4. Update input value for next round based on highest-graded value
5. Carryover pruned set to next round
6. Unit tests covering: pruning logic, working set updates
7. Integration test: value set converges over multiple rounds

## Prerequisites

Story 4.3

## Notes

Value pruning accelerates convergence to consensus.
