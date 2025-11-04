# Story 4.1: BA Controller Initialization & Configuration

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA simulation,
I want a BA controller managing protocol orchestration,
So that I can coordinate PoP, CoD, GDA execution across rounds.

## Acceptance Criteria

1. Create `ba_controller.py` module with `BAController` class
2. `__init__(n: int, t: int, node_id: int, initial_value: Any)` constructor
3. Initialize subprotocol instances: LitePoP, CoD, GDA
4. Configuration: network parameters (n, t), node identity, input value
5. State storage: current round, current subprotocol, accumulated evidence
6. `start_round(round: int)` method initializing round-specific state
7. Unit tests covering: initialization, configuration validation
8. Docstrings explaining BA controller role in early-stopping protocol

## Prerequisites

Stories 3.4, 3.7, 3.8

## Notes

Central orchestrator for Byzantine Agreement execution.
