# Story 8.2: Batch Experiment Harness

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As an experimenter,
I want to run batched experiments over parameter configurations,
So that I can execute 500-1000 experimental runs systematically.

## Acceptance Criteria

1. Create `experiment_harness.py` module with `BatchRunner` class
2. `run_batch(config: ExperimentConfig) -> List[Results]` method
3. Iterate over: network sizes × fault levels × adversary mixes × replications
4. Each run: execute BA protocol, collect metrics, store results
5. Progress indicators: show completed runs / total runs
6. Resumable execution: save intermediate results, resume from checkpoint
7. Unit tests covering: batch iteration, progress tracking
8. Integration test: small batch (3 configs × 2 replications) completes successfully

## Prerequisites

Story 8.1

## Notes

Enables systematic execution of large-scale experiments.
