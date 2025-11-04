# Story 3.5: GDA - PROPOSE Phase Implementation

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a GDA protocol,
I want to process PROPOSE messages and accumulate proposals,
So that I can compute grades based on proposal distribution.

## Acceptance Criteria

1. Create `gda.py` module with `GDA` class inheriting from `ProtocolFSM`
2. Initialize in PROPOSE phase
3. `process_message(msg)` for PROPOSE phase:
   - Validate protocol_id="GDA", phase="PROPOSE"
   - Accumulate PROPOSE messages with values
   - Track value distribution: count per distinct value
4. After PROPOSE collection period, transition to GRADE_VOTE phase
5. Prepare for grading: identify most common value(s) and counts
6. Unit tests covering: PROPOSE accumulation, value distribution tracking
7. Edge case: multiple values with equal counts

## Prerequisites

Story 3.1

## Notes

First phase of Graded Agreement protocol.
