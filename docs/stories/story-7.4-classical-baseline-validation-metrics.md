# Story 7.4: Classical Baseline Validation & Metrics

**Epic:** Epic 7 - Classical Baseline Implementation
**Week:** Weeks 13-14

## User Story

As a researcher,
I want classical baseline producing metrics for direct comparison,
So that I can demonstrate early-stopping advantage empirically.

## Acceptance Criteria

1. Classical BA produces same metrics as early-stopping: rounds to decision, message count, crypto ops
2. Classical BA respects Byzantine Agreement properties (Agreement, Validity, Termination)
3. Property assertions applied to classical execution
4. Metrics export: CSV with classical baseline results
5. Integration test: classical terminates at t+1, early-stopping terminates earlier (when f ≪ t)
6. Comparison test: plot rounds vs. f for both protocols side-by-side
7. Validation: classical always ≥ early-stopping in round count (no false negatives)

## Prerequisites

Story 7.3

## Notes

Enables empirical demonstration of early-stopping advantage.
