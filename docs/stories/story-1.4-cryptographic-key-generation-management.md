# Story 1.4: Cryptographic Key Generation & Management

**Epic:** Epic 1 - Foundation Infrastructure
**Week:** Weeks 1-4

## User Story

As a simulated node,
I want Ed25519 key pair generation and management,
So that I can sign messages and verify signatures using PyNaCl.

## Acceptance Criteria

1. Create `crypto.py` module with `NodeKeys` class
2. `generate_keypair() -> (SigningKey, VerifyKey)` using PyNaCl Ed25519
3. `NodeKeys` class storing `signing_key` (private) and `verify_key` (public)
4. `sign(payload: bytes) -> bytes` method generating Ed25519 signatures
5. `verify(payload: bytes, signature: bytes, verify_key: VerifyKey) -> bool` static method
6. Signature verification returns False for invalid signatures (no exceptions for normal operation)
7. Key serialization methods for test fixtures (optional but helpful)
8. Unit tests covering: key generation, signing, verification success, verification failure, deterministic signatures

## Prerequisites

Story 1.1

## Notes

Ed25519 provides fast, secure cryptographic signatures for message authentication.
