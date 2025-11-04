# Story 3.1: Protocol FSM Base Class

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a protocol developer,
I want a base finite state machine pattern for all subprotocols,
So that CoD, GDA, PoP follow consistent implementation structure.

## Acceptance Criteria

1. Create `protocol_fsm.py` module with `ProtocolFSM` abstract base class
2. Abstract methods: `process_message(msg: Message)`, `get_output()`, `get_current_phase()`
3. FSM state storage: current phase, accumulated messages per phase, thresholds reached
4. Phase enumeration per protocol (CoD phases, GDA phases, etc.)
5. Helper method `count_messages_from_distinct_senders(phase: str) -> int`
6. Transition logging: record all phase transitions with justification
7. Unit tests for base class behaviors (if not purely abstract)
8. Docstrings explaining Byzantine Agreement FSM pattern

## Prerequisites

Story 1.2

## Notes

Foundation for all protocol implementations using FSM pattern.
