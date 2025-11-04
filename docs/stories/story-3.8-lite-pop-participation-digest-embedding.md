# Story 3.8: Lite PoP - Participation Digest Embedding

**Epic:** Epic 3 - Protocol Primitives - CoD & GDA
**Week:** Weeks 5-8

## User Story

As a Lite PoP implementation,
I want to embed prior-round participation digests in messages,
So that I provide participation evidence without full PoP machinery.

## Acceptance Criteria

1. Create `lite_pop.py` module with `LitePoP` class
2. `compute_participation_digest(round: int, messages: List[Message]) -> bytes` method
3. Digest = hash of sorted sender IDs from previous round messages
4. Embed digest in message `aux` field: `aux['participation_digest']`
5. `verify_participation(message: Message, expected_digest: bytes) -> bool` method
6. Local chain verification: check digest matches previous round
7. Unit tests covering: digest computation, embedding, verification
8. Note: Full PoP ANNOUNCE/PROOF phases deferred to Phase 2

## Prerequisites

Story 1.2

## Notes

Lite PoP provides lightweight participation evidence.
