# Story 6.1: Evidence Store Infrastructure

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As a validator,
I want an immutable evidence store for certificates and decision proofs,
So that I can reconstruct execution paths and verify correctness claims.

## Acceptance Criteria

1. Create `evidence_store.py` module with `EvidenceStore` class
2. Evidence types: barrier_certificates, transition_records, decision_packages
3. `add_evidence(type: str, round: int, data: Any)` method storing evidence immutably
4. `get_evidence(type: str, round: int) -> Any` method retrieving evidence
5. Evidence includes: cryptographic proofs (signatures), timestamps, justifications
6. Immutability: evidence cannot be modified after recording
7. Unit tests covering: evidence storage, retrieval, immutability
8. Optional: garbage collection for old rounds (configurable retention policy)

## Prerequisites

Story 1.2

## Notes

Foundation for complete audit trails and evidence-based validation.
