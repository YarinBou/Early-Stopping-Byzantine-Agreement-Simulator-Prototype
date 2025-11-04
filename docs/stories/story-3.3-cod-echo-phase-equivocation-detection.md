# Story 3.3: CoD - ECHO Phase with Equivocation Detection

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a CoD protocol,
I want to process ECHO messages and detect equivocation,
So that I can safely transition to READY phase with consensus or detect-set.

## Acceptance Criteria

1. Extend `CoD` to handle ECHO phase
2. `process_message(msg)` for ECHO phase:
   - Accumulate ECHO messages
   - Detect equivocation: same sender, different values in ECHO
3. Threshold conditions for READY transition:
   - n-t matching ECHO messages → READY with consensus value
   - OR t+1 READY messages → READY (amplification)
4. Equivocation handling: flag conflicting values, produce detect-set
5. Unit tests covering: matching ECHO, equivocation detection, READY transition
6. Integration test: honest nodes reach READY, equivocator detected

## Prerequisites

Story 3.2

## Notes

Equivocation detection is critical for Byzantine fault tolerance.
