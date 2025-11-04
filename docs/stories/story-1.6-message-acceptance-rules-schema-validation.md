# Story 1.6: Message Acceptance Rules - Schema Validation

**Epic:** Epic 1 - Foundation Infrastructure
**Week:** Weeks 1-4

## User Story

As a protocol validator,
I want strict message schema validation before processing,
So that malformed or invalid messages are rejected immediately.

## Acceptance Criteria

1. Create `validation.py` module with `MessageValidator` class
2. `validate_schema(message: Message) -> bool` method checking:
   - All required fields are non-null
   - `round` is non-negative integer
   - `sender_id` is valid node ID (0 ≤ sender_id < n)
   - `protocol_id` and `phase` are non-empty strings
   - Signature is present and correct length (64 bytes for Ed25519)
3. Return `False` for invalid messages (log reason at debug level)
4. Validation happens before any protocol processing
5. Unit tests covering: valid messages pass, missing fields fail, invalid types fail, edge cases
6. Performance: validation should be fast (< 1ms per message)

## Prerequisites

Story 1.2

## Notes

Schema validation is the first line of defense against malformed messages.
