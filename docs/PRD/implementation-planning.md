# Implementation Planning

## Development Timeline (18-20 Weeks)

**Weeks 1-4: Infrastructure Foundation**
- Authenticated transport layer with message schema
- Acceptance rules, deduplication, anti-replay protection
- Round scheduler with asyncio timers and Δ timeout enforcement
- Certificate builder for threshold-based advancement tracking
- **Milestone**: Transport layer passing unit tests with crypto signatures

**Weeks 5-8: Protocol Primitives**
- Lite PoP: Lightweight proof-of-participation with embedded digests
- CoD: Consistent dissemination with SEND/ECHO/READY phases and threshold logic
- GDA: Graded agreement with PROPOSE/GRADE_VOTE phases producing grades ∈ {0,1,2}
- Local phase enumeration and subprotocol state machines
- **Milestone**: All subprotocols validated independently with test cases

**Weeks 9-12: Deterministic BA Controller + Adversaries**
- BA controller orchestration layer sequencing PoP/CoD/GDA subprotocols
- Certificate ∨ timeout round advancement implementation
- Carryover state management and round firewall enforcement
- Adversary implementations: Equivocator, Withholder, Delay/Drop (≤ Δ)
- **Milestone**: Full early-stopping BA stack executing correctly on small networks (n=7)

**Weeks 13-14: Perry-Toueg Baseline**
- Minimal classical BA baseline implementation (t+1 round bound)
- Shared transport layer and cryptographic infrastructure
- Experimental parity validation for fair comparison
- **Milestone**: Baseline demonstrating expected (t+1) termination behavior

**Weeks 15-18: Experiments, Metrics, Visualization**
- Batch experiment execution over (n, t, f) parameter space
- Metrics collection and CSV export infrastructure
- Publication-quality plots: rounds/messages/crypto operations vs. f
- Statistical analysis with error bars and confidence intervals
- **Milestone**: Complete experimental results answering all three research questions

**Weeks 19-20: Analysis + Thesis Writing Buffer**
- Results interpretation and validation against research questions
- Documentation finalization and thesis integration
- Contingency time for unforeseen issues or refinements
- **Milestone**: Frozen system with thesis-ready empirical evidence

## Development Approach

**Incremental Validation Strategy**
1. Build each subprotocol as standalone FSM with comprehensive unit tests
2. Validate correctness on small networks (n=4, n=7) before scaling
3. Progressive complexity increase with validation gates
4. Property assertions enforced from day one (Agreement, Validity, Termination)

**Risk Mitigation Through Scope Control**
- Feature freeze: Lock implementation once deterministic BA + baseline + metrics demonstrate correctness
- Fallback plan: If timeline pressure emerges, reduce to Lite PoP + deterministic controller only (defer randomized variant)
- Core adversary suite maintained: Equivocator + Withholder + Delay (sufficient for thesis validation)

**Technology Decisions Favoring Development Velocity**
- JSON serialization: Debuggability over wire size (CBOR migration post-MVP via abstraction)
- Single-machine simulation: Maximum reproducibility, no distributed system debugging overhead
- Python asyncio: Event-driven concurrency without threading complexity

## Epic Breakdown Required

The PRD requirements must be decomposed into implementable epics and bite-sized stories (200k context limit for development agents).

**Next Step:** Run `/bmad:bmm:workflows:create-epics-and-stories` to create the implementation breakdown.

## Project-Level Estimation

**Complexity Level**: 3 (Medium-High)
- Sophisticated distributed systems concepts (Byzantine Agreement, cryptographic protocols)
- Research validation requirements (correctness proofs, statistical rigor)
- Multi-component architecture (transport, protocols, adversaries, validation, experiments)

**Target Scale**: Research prototype (not production system)
- Network sizes: n ≤ 31 nodes
- Experimental runs: 500-1000 total configurations
- Single-machine execution sufficient

**Technical Stack Maturity**: High
- Python 3.10+: Mature, well-documented
- asyncio: Standard library, proven for event-driven systems
- PyNaCl: Battle-tested cryptographic library
- pytest/pandas/matplotlib: Industry-standard research tools

---
