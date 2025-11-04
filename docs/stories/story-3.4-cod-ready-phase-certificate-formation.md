# Story 3.4: CoD - READY Phase & Certificate Formation

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a CoD protocol,
I want to accumulate READY messages and form certificates,
So that I can output consensus value when n-t READY threshold reached.

## Acceptance Criteria

1. Extend `CoD` to handle READY phase (terminal phase for CoD)
2. `process_message(msg)` for READY phase:
   - Accumulate READY messages
   - Track distinct senders
3. Certificate condition: n-t READY messages from distinct senders
4. `get_output() -> (value, certificate)` method returning consensus value + proof
5. Certificate proof: list of n-t signed READY messages
6. Unit tests covering: READY accumulation, certificate formation, output extraction
7. Integration test: full CoD execution SEND → ECHO → READY → certificate

## Prerequisites

Story 3.3

## Notes

Completes CoD protocol implementation.
