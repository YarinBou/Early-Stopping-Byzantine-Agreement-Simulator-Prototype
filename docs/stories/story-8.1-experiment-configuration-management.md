# Story 8.1: Experiment Configuration Management

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As an experimenter,
I want YAML-based experiment configurations,
So that I can define parameter sweeps and adversary mixes declaratively.

## Acceptance Criteria

1. Create `experiment_config.py` module with config loading
2. YAML schema: network_sizes, fault_sweeps, adversary_configs, replication_count
3. Example config: n ∈ {7, 13, 25, 31}, f = 0..t, replications = 10
4. Config validation: ensure f ≤ t, n valid, Δ positive
5. `load_config(path: str) -> ExperimentConfig` function
6. Config includes: delay distributions, timeout bounds, random seeds
7. Unit tests covering: config loading, validation, default values
8. Example configs for common scenarios (no faults, low faults, max faults)

## Prerequisites

Story 1.1

## Notes

Foundation for declarative experiment configuration.
