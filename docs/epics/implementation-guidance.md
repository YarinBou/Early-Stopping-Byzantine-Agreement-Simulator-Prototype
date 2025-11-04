# Implementation Guidance

## Getting Started

**Start Here:** Epic 1, Story 1.1 (Project Structure & Dependencies)

This is the only story with no prerequisites. Once complete, multiple stories can run in parallel.

## Parallel Development Opportunities

**Phase 1 (Weeks 1-4):**
- After Story 1.1: Stories 1.2 and 1.4 can run in parallel
- After Story 1.2: Stories 1.6, 2.1 can start
- Epics 1 and 2 have significant overlap potential

**Phase 2 (Weeks 5-8):**
- After Story 3.1: CoD (3.2-3.4) and GDA (3.5-3.7) can develop completely in parallel
- Story 3.8 (Lite PoP) can also run independently

**Phase 3 (Weeks 9-12):**
- Epics 4 and 5 can partially overlap (adversary framework while finalizing BA controller)
- After Story 5.1: All adversary implementations (5.2-5.4) can run in parallel

**Phase 4 (Weeks 13-18):**
- Epic 7 (Classical Baseline) is independent and can run in parallel with Epic 6 completion
- Epic 8 stories are mostly sequential but can start configuration/harness (8.1-8.2) while Epic 7 completes

## Critical Path

The following stories are on the critical path and block multiple downstream dependencies:

1. **Story 1.1** → Blocks everything
2. **Story 1.2** (Message Schema) → Blocks protocols, validation, adversaries
3. **Story 2.1** (Round Scheduler) → Blocks round management, BA controller
4. **Story 3.1** (Protocol FSM) → Blocks all subprotocol implementations
5. **Story 4.1** (BA Controller) → Blocks early-stopping validation
6. **Story 4.8** (BA Integration Test) → Validates early-stopping behavior, blocks experiments

## Development Phases & Milestones

**Phase 1: Foundation (Weeks 1-4)**
- **Milestone**: Messages can be created, signed, validated, and accepted with full cryptographic authentication
- **Milestone**: Lock-step round progression operational
- **Validation Gate**: Unit tests passing for all foundation components

**Phase 2: Protocols (Weeks 5-8)**
- **Milestone**: CoD and GDA subprotocols operational as independent FSMs
- **Validation Gate**: Integration tests show full protocol execution SEND→ECHO→READY and PROPOSE→GRADE_VOTE

**Phase 3: BA Controller (Weeks 9-11)**
- **Milestone**: Full early-stopping BA stack executing correctly on n=7
- **Validation Gate**: Early-stopping behavior demonstrated (grade-2 certificates trigger early termination)

**Phase 4: Adversaries & Validation (Weeks 10-13)**
- **Milestone**: Zero safety violations under Equivocator, Withholder, Delay/Drop attacks
- **Validation Gate**: Property assertions passing, evidence store capturing complete audit trail

**Phase 5: Baseline & Experiments (Weeks 13-18)**
- **Milestone**: Classical baseline operational, experimental campaign complete
- **Validation Gate**: Publication-quality plots showing early-stopping advantage

## Risk Mitigation Strategy

**If Timeline Pressure Emerges:**

1. **Reduce Protocol Complexity**
   - Keep Lite PoP minimal (defer full PoP to Phase 2)
   - Focus on deterministic BA only (defer randomized variant)

2. **Limit Adversary Suite**
   - Core three adversaries sufficient: Equivocator + Withholder + Delay
   - Defer crash-recovery, flooding, partial-synchrony stress

3. **Simplify Experimental Matrix**
   - Reduce to 3 network sizes: n ∈ {7, 13, 25}
   - Reduce replication count from 30 to 10-15 runs per configuration

4. **Baseline Simplification**
   - If Perry-Toueg too complex, use theoretical (t+1) overlay for comparison rather than side-by-side implementation

**Feature Freeze Decision Point:** Week 18
- Lock implementation once deterministic BA + baseline + metrics demonstrate correctness
- Remaining time for analysis and thesis writing

## Story Estimation Guidelines

**Small Story (2-4 hours):** Configuration, data classes, simple utilities
- Examples: Stories 1.1, 1.2, 1.3, 2.4

**Medium Story (4-8 hours):** Core protocol logic, integrations, test suites
- Examples: Stories 3.2-3.7, 5.2-5.4, 6.1-6.4

**Large Story (8-16 hours):** Complex orchestration, full FSMs, integration tests
- Examples: Stories 4.2, 4.8, 7.2, 8.8

## Testing Strategy

**Unit Test Coverage Target:** >80% for protocol logic

**Testing Levels:**
1. **Unit Tests**: Every story includes unit tests covering nominal and edge cases
2. **Integration Tests**: Multi-component tests validating interfaces (e.g., full CoD execution)
3. **Property Tests**: Byzantine Agreement properties asserted throughout
4. **System Tests**: Complete end-to-end BA execution with adversaries

**Validation Gates:**
- No story marked complete without passing tests
- Integration tests required before advancing to next epic
- Property assertions must pass before scaling to larger networks

## Technical Debt Management

**Acceptable in MVP:**
- JSON serialization (CBOR migration post-MVP via abstraction)
- Single-machine simulation (no distributed execution)
- Basic logging (advanced profiling deferred)
- Manual garbage collection triggers (automatic GC in Phase 2)

**Not Acceptable (Must Fix Before Scaling):**
- Byzantine Agreement property violations
- Round firewall breaches
- Non-deterministic execution
- Missing cryptographic verification

---
