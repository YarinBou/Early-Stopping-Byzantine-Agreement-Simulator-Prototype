# Story 1.3: JSON Serialization with Canonical Ordering

**Epic:** Epic 1 - Foundation Infrastructure
**Week:** Weeks 1-4

## User Story

As a protocol developer,
I want deterministic JSON serialization for messages,
So that identical messages produce identical serialized bytes for cryptographic hashing and signatures.

## Acceptance Criteria

1. Create `serialization.py` module with `MessageSerializer` class
2. `encode(message: Message) -> bytes` method using JSON with canonical key ordering (`sort_keys=True`)
3. Binary fields (signature, digest) base64-encoded for JSON compatibility
4. `decode(data: bytes) -> Message` method reconstructing Message objects
5. Round-trip test: `decode(encode(msg)) == msg` for all message types
6. Deterministic output: same message always produces identical bytes
7. Abstraction layer designed for future CBOR migration (encode/decode interface only)
8. Unit tests covering: encoding, decoding, determinism, base64 handling, error cases

## Prerequisites

Story 1.2

## Notes

Deterministic serialization is critical for reproducibility and cryptographic operations.
