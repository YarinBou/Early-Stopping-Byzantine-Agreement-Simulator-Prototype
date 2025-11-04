# Story 3.7: GDA - GRADE_VOTE Phase & Output

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a GDA protocol,
I want to emit GRADE_VOTE messages with computed grades,
So that all nodes reach agreement on graded values.

## Acceptance Criteria

1. Extend `GDA` to handle GRADE_VOTE phase (terminal phase for GDA)
2. After PROPOSE phase, compute grade for most common value
3. Broadcast GRADE_VOTE message with `(value, grade)` tuple
4. Accumulate GRADE_VOTE messages from other nodes
5. `get_output() -> (value, grade)` method returning graded consensus
6. Grade-2 certificates enable early decision (no further rounds needed)
7. Unit tests covering: GRADE_VOTE emission, accumulation, output extraction
8. Integration test: full GDA execution PROPOSE → GRADE_VOTE → graded output

## Prerequisites

Story 3.6

## Notes

Completes GDA protocol implementation.
