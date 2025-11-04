# Story 3.2: CoD - SEND Phase Implementation

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a CoD protocol,
I want to process SEND messages and accumulate them,
So that I can trigger ECHO phase when n-t SEND messages received.

## Acceptance Criteria

1. Create `cod.py` module with `CoD` class inheriting from `ProtocolFSM`
2. Initialize in SEND phase
3. `process_message(msg)` for SEND phase:
   - Validate protocol_id="CoD", phase="SEND"
   - Accumulate SEND messages in internal storage
   - Track distinct senders
4. Threshold detection: when ≥ n-t SEND messages from distinct senders → transition to ECHO
5. ECHO trigger emits broadcast message with aggregated value or digest
6. Unit tests covering: SEND accumulation, threshold detection, ECHO transition
7. Edge case: exactly n-t SEND messages triggers ECHO

## Prerequisites

Story 3.1

## Notes

First phase of Consistent Dissemination protocol.
