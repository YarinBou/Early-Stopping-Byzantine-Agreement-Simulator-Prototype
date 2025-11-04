# Story 1.5: Message Signing & Verification Integration

**Epic:** Epic 1
**Week:** Weeks TBD

## User Story

As a protocol developer,
I want to sign messages and verify signatures using node keys,
So that all messages are cryptographically authenticated preventing forgery..

## Acceptance Criteria

1. Extend `Message` class with `sign(node_keys: NodeKeys) -> None` method
2. Signing populates `signature` field using `message.signing_payload()`
3. Add `verify_signature(verify_key: VerifyKey) -> bool` method to Message
4. Verification checks signature against signing payload
5. Message constructor validates signature is present when required
6. Integration test: Create message, sign it, verify with correct key (success), verify with wrong key (failure)
7. Unit tests covering: unsigned message handling, signature verification edge cases
8. Docstrings explaining Byzantine Agreement authentication model

## Prerequisites

Stories 1.2, 1.3, 1.4
