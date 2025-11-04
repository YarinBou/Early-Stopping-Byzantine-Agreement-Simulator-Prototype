# Story 2.4: Certificate Tracking & Advancement Condition

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a BA controller,
I want to track terminal-phase message accumulation for certificate formation,
So that rounds can advance early when n-t threshold is reached.

## Acceptance Criteria

1. Create `certificate_tracker.py` module with `CertificateTracker` class
2. `add_terminal_message(message: Message)` method accumulating terminal-phase messages
3. `has_certificate(n: int, t: int) -> bool` method checking if n-t threshold reached
4. Track messages by `(protocol_id, phase)` for multi-protocol support
5. Certificate condition: at least n-t messages from distinct senders in terminal phase
6. `get_certificate_messages() -> List[Message]` returning messages forming certificate
7. Unit tests covering: threshold detection, distinct sender validation, multi-protocol handling
8. Edge case: exactly n-t messages triggers certificate

## Prerequisites

Story 1.2

## Notes

Enables early round advancement when sufficient evidence collected.
