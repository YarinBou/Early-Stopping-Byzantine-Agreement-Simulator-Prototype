# Story 1.7: Message Deduplication with Key-Based Tracking

**Epic:** Epic 1
**Week:** Weeks TBD

## User Story

As a protocol validator,
I want message deduplication keyed by `(sender_id, round, protocol_id, phase)`,
So that duplicate messages are discarded and never processed twice..

## Acceptance Criteria

1. Extend `MessageValidator` with deduplication tracking
2. Maintain internal set of seen message keys: `(sender_id, round, protocol_id, phase)`
3. `is_duplicate(message: Message) -> bool` method checking if key already seen
4. First occurrence: add to seen set, return False
5. Subsequent occurrences: return True (duplicate)
6. Memory management: support clearing old rounds (will implement garbage collection later)
7. Unit tests covering: first message accepted, exact duplicate rejected, different phase accepted
8. Thread-safety considerations documented (not required for MVP single-threaded asyncio)

## Prerequisites

Story 1.6
