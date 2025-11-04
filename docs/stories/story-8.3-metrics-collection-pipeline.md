# Story 8.3: Metrics Collection Pipeline

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As a metrics collector,
I want to track rounds, messages, and crypto operations per run,
So that I can analyze protocol performance quantitatively.

## Acceptance Criteria

1. Create `metrics.py` module with `MetricsCollector` class
2. Metrics tracked per run:
   - Rounds to decision
   - Total messages sent/received
   - Messages per node per round
   - Signature generation count
   - Signature verification count
   - Wall-clock execution time
3. `collect_metrics(ba_execution: Any) -> RunMetrics` method
4. Metrics validation: ensure counts are consistent (e.g., messages sent ≤ n² per round)
5. Unit tests covering: metric collection, validation
6. Integration test: full BA run produces complete metrics

## Prerequisites

Story 4.8

## Notes

Collects quantitative performance data for analysis.
