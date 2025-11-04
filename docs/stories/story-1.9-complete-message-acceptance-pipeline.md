# Story 1.9: Complete Message Acceptance Pipeline

**Epic:** Epic 1
**Week:** Weeks TBD

## User Story

As a protocol engine,
I want a unified message acceptance pipeline integrating all validation rules,
So that only valid, authenticated, non-duplicate, properly-timed messages enter protocol processing..

## Acceptance Criteria

1. Create `accept_message(message: Message, verify_keys: Dict[int, VerifyKey]) -> bool` method
2. Acceptance pipeline order:
   - Schema validation (Story 1.6)
   - Signature verification (Story 1.5)
   - Round binding check (Story 1.8)
   - Deduplication check (Story 1.7)
3. Return `True` only if all checks pass
4. Log rejection reasons at appropriate levels (debug for duplicates, warn for invalid signatures)
5. Performance target: < 5ms per message including signature verification
6. Integration tests covering: fully valid message accepted, failures at each stage rejected
7. Statistics tracking: accepted count, rejected count by reason (helpful for debugging)

## Prerequisites

Stories 1.5, 1.6, 1.7, 1.8
