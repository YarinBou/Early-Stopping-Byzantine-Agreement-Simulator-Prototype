# Story 4.3: Early Decision Logic - Grade-2 Certificate Detection

**Epic:** Epic 4 - BA Controller & Early-Stopping Logic
**Week:** Weeks 9-11

## User Story

As a BA controller,
I want to detect grade-2 certificates and decide immediately,
So that I can terminate in (1+ε)f rounds without waiting for (t+1) rounds.

## Acceptance Criteria

1. Implement `check_decision_condition() -> Optional[Any]` method
2. Decision condition: grade-2 certificate from GDA (n-t nodes propose same value)
3. If grade-2 detected → set `decided = True`, store decision value
4. If grade-2 not reached → continue to next round
5. Decision is final (no further rounds after decision)
6. Log decision event with round number and justification
7. Unit tests covering: grade-2 triggers decision, lower grades continue
8. Integration test: early termination at round ~(1+ε)f when grade-2 forms

## Prerequisites

Story 4.2

## Notes

This is the heart of early-stopping - enables termination before (t+1) rounds.
