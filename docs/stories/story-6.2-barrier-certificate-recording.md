# Story 6.2: Barrier Certificate Recording

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As an evidence store,
I want to record barrier certificates (n-t terminal-phase signatures),
So that I can prove round advancement was justified by sufficient honest messages.

## Acceptance Criteria

1. Extend `EvidenceStore` with barrier certificate recording
2. Barrier certificate = set of ≥ n-t signed terminal-phase messages
3. `record_barrier_certificate(round: int, messages: List[Message])` method
4. Certificate validation: verify signatures, check distinct senders, validate phase
5. Compact representation: store message digests + signatures (not full payloads)
6. Certificate proof can be independently verified by third party
7. Unit tests covering: certificate recording, validation, compact storage
8. Integration test: barrier certificates recorded for each round advancement

## Prerequisites

Story 6.1

## Notes

Barrier certificates prove round advancement was justified.
