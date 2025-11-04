# Story 2.7: Late Message Logging & Audit Trail

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a researcher,
I want late-arriving messages logged but never mutating previous round state,
So that I can audit post-round arrivals without violating round firewall.

## Acceptance Criteria

1. Extend message delivery to detect late arrivals (message.round < current_round)
2. Late messages logged with full headers + signature but NOT processed for state mutation
3. Late message log includes: message metadata, arrival timestamp, round delta
4. Separate late message storage: `late_messages: List[Message]` for audit
5. Optional: Late message statistics (count by round, sender)
6. Round firewall enforcement test: assert no late message mutates protocol state
7. Unit tests covering: late message detection, logging, isolation from protocol logic
8. Audit trail export for analysis (CSV format with late message details)

## Prerequisites

Story 2.2

## Notes

Provides audit trail while maintaining round firewall integrity.
