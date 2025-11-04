# Story 6.6: Evidence Export for Analysis

**Epic:** Epic 6 - Validation & Evidence Infrastructure
**Week:** Weeks 11-13

## User Story

As a researcher,
I want to export evidence store to CSV/JSON for external analysis,
So that I can validate correctness claims and generate audit reports.

## Acceptance Criteria

1. Implement `export_evidence(format: str, output_path: str)` method
2. Export formats: CSV (tabular), JSON (structured)
3. Export includes: all barrier certificates, transition records, decision packages
4. CSV columns: round, evidence_type, data_summary, timestamp
5. JSON structure: nested hierarchy by round and evidence type
6. Export preserves cryptographic proofs (signatures as base64)
7. Unit tests covering: CSV export, JSON export, round-trip deserialization
8. Integration test: export after full BA execution, validate external loading

## Prerequisites

Story 6.4

## Notes

Evidence export enables external validation and audit.
