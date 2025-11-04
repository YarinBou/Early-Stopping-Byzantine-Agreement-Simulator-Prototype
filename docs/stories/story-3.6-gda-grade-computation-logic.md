# Story 3.6: GDA - Grade Computation Logic

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a GDA protocol,
I want to compute grades ∈ {0, 1, 2} based on message thresholds,
So that I can produce graded consensus values enabling early-stopping.

## Acceptance Criteria

1. Implement `compute_grade(value: Any, count: int, n: int, t: int) -> int` method
2. Grade definitions:
   - Grade 2: count ≥ n-t (strong consensus)
   - Grade 1: t+1 ≤ count < n-t (weak consensus)
   - Grade 0: count < t+1 (no consensus)
3. Most common value receives highest grade
4. If no value reaches t+1, all grades are 0
5. Grade computation test: verify thresholds for all grade values
6. Unit tests covering: grade 2, grade 1, grade 0, edge cases (exactly n-t, exactly t+1)
7. Mathematical correctness: grades align with theoretical GDA specification

## Prerequisites

Story 3.5

## Notes

Grade computation is the key to early-stopping termination.
