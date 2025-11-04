# Story 6.4: Decision Package Assembly

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As an evidence store,
I want to assemble decision packages with grade-2 or READY proofs,
So that I can prove final decisions are justified by sufficient evidence.

## Acceptance Criteria

1. Extend `EvidenceStore` with decision package recording
2. Decision package = `{decision_value, decision_round, proof_messages, proof_type}`
3. Proof type: "grade-2 certificate" (GDA) or "READY certificate" (CoD)
4. `record_decision(value: Any, round: int, proof: List[Message])` method
5. Decision proof independently verifiable (signatures, thresholds)
6. Package includes all information needed for third-party validation
7. Unit tests covering: decision package assembly, proof validation
8. Integration test: final decision produces complete verifiable package

## Prerequisites

Story 6.1

## Notes

Decision packages prove final decisions are justified.
