# Story 8.4: CSV/Parquet Export for Analysis

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As an analyst,
I want experiment results exported to CSV or Parquet,
So that I can perform statistical analysis using pandas/R.

## Acceptance Criteria

1. Extend `BatchRunner` with export functionality
2. `export_results(format: str, output_path: str)` method
3. CSV columns: n, t, f, adversary_type, run_id, rounds, messages, crypto_ops, decision_value
4. Parquet format for large datasets (optional but recommended)
5. Export includes metadata: experiment date, config hash, protocol version
6. Round-trip test: export and re-import results successfully
7. Unit tests covering: CSV export, Parquet export (if implemented)
8. Integration test: batch execution exports results, pandas loads successfully

## Prerequisites

Story 8.3

## Notes

Enables external analysis with pandas/R/statistical tools.
