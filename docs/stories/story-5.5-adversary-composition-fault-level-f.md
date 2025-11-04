# Story 5.5: Adversary Composition for Fault Level f

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As a simulation engine,
I want to compose multiple adversary behaviors to reach target fault level f,
So that I can test protocol with exactly f Byzantine nodes.

## Acceptance Criteria

1. Create `AdversaryComposition` class managing multiple adversaries
2. Configuration: list of `(node_id, strategy)` tuples, total f ≤ t
3. Validate: total adversarial nodes ≤ t (fault tolerance bound)
4. Route messages through appropriate adversary strategies per node
5. Honest nodes bypass adversary logic
6. Support mixed strategies: some equivocators, some withholders
7. Unit tests covering: composition validation, routing, mixed strategies
8. Integration test: f=2 with 1 Equivocator + 1 Withholder

## Prerequisites

Stories 5.2, 5.3, 5.4

## Notes

Enables testing with multiple simultaneous Byzantine behaviors.
