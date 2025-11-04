# Story 5.1: Adversary Strategy Interface

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As an adversary framework,
I want a pluggable strategy interface for Byzantine behaviors,
So that new adversary types can be added without modifying core infrastructure.

## Acceptance Criteria

1. Create `adversary.py` module with `AdversaryStrategy` abstract base class
2. Abstract methods: `intercept_send(message: Message) -> List[Message]`, `should_drop(message: Message) -> bool`
3. Adversary configuration: node_id, fault type, intensity parameters
4. Seeded RNG for reproducible behavior
5. Logging: all adversarial actions logged for audit
6. Multiple adversaries can compose to reach fault level f
7. Unit tests for base interface (if not purely abstract)
8. Docstrings explaining Byzantine adversary patterns

## Prerequisites

Story 1.2

## Notes

Foundation for pluggable adversary models.
