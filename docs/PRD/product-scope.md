# Product Scope

## MVP - Minimum Viable Product (Thesis Validation - 18-20 Weeks)

**Core Definition**: A deterministic early-stopping Byzantine Agreement prototype with Lite PoP, CoD, GDA, certificate-or-timeout advancement, core adversary models, auditable evidence store, minimal Perry-Toueg baseline, and experiment harness producing publication-quality graphs.

**Must-Have Components for Thesis Defense:**

1. **Protocol Implementation Stack**
   - **CoD (Consistent Dissemination)**: SEND/ECHO/READY phases for reliable value propagation with Byzantine fault tolerance
   - **GDA (Graded Agreement)**: PROPOSE/GRADE_VOTE phases producing values with grades ∈ {0,1,2} enabling early decision
   - **Deterministic BA Controller**: Orchestration layer sequencing subprotocols, managing carryover state, enforcing certificate ∨ timeout advancement
   - **Lite PoP**: Minimal participation evidence embedded in messages with local chain verification (not full PoP infrastructure)

2. **Core Adversary Suite** (Essential for Correctness Validation)
   - **Equivocator**: Signs conflicting payloads for identical (round, protocol_id, phase) tuples
   - **Withholder**: Suppresses terminal-phase messages until late rounds to delay certificate formation
   - **Delay/Drop (Bounded by Δ)**: Realistic message scheduling within synchrony bounds (jitter, reordering, controlled loss)

3. **Validation Framework** (Non-Negotiable)
   - **Property Assertions**: Agreement, Validity, Termination, Round Firewall (always-on enforcement)
   - **Evidence Store**: Barrier certificates (n-t terminal-phase signatures), transition records, decision packages
   - **Experiment Harness**: Batch execution over (n, t, f) configurations with CSV/Parquet export
   - **Metrics Collection**: Rounds to decision, total messages, cryptographic operation counts
   - **Reproducibility**: Seeded pseudo-random number generation for deterministic replication

4. **Baseline Comparison**
   - **Perry-Toueg Classical BA**: Minimal implementation demonstrating (t+1) round bound
   - **Experimental Parity**: Identical (n, t, f) configurations, synchrony bounds, adversary models

5. **Experiment Infrastructure**
   - Parameterized runs over network sizes n ∈ {7, 13, 25, 31}
   - Fault sweeps f = 0…t with emphasis on low-fault regime (f = 0, 1, 2, 3)
   - Publication-quality visualizations: rounds/messages/crypto operations vs. f
   - Statistical analysis with error bars and confidence intervals

**Scale Target**: Research-focused configurations (n ≤ 31), single-machine asyncio simulation, 500-1000 experimental runs

## Growth Features (Post-Thesis / Phase 2)

**Protocol Extensions:**
- **Full PoP Machinery**: Complete proof-of-participation protocol with explicit ANNOUNCE/PROOF phases
- **Randomized BA Controller**: Common coin integration for deadlock resolution and stress testing
- **Partial-Synchrony Adaptations**: Stress modes exploring behavior beyond core synchronous model

**Extended Adversary Suite:**
- Crash-only and honest-but-slow variants for graceful degradation testing
- Flooder/spammer adversaries (rate-limited by protocol acceptance rules)
- Sophisticated Byzantine strategy combinations and composed attacks

**Advanced Tooling:**
- Interactive GUI for protocol execution visualization
- Real-time message flow and state transition viewers
- Step-through debugging with evidence store inspection
- Advanced profiling and performance analysis tools

**Performance Optimizations:**
- Signature batching and aggregation techniques
- Message compression and wire format optimization (CBOR migration)
- Adaptive timeout tuning based on network observations

**Deployment Options:**
- Multi-process runner with inter-process communication
- Multi-host distributed execution for demonstrators
- Real network transport layer integration

## Vision (Future / Research Community Platform)

**Extensible Protocol Platform:**
- Plugin architecture for arbitrary BA protocol variants
- Protocol composition framework for building complex consensus mechanisms
- Automated protocol verification against formal specifications

**Research Acceleration Tools:**
- Automated parameter sweep optimization for finding protocol limits
- Machine learning integration for adversary strategy discovery
- Comparative protocol benchmarking suite for consensus algorithm evaluation

**Educational Resources:**
- Interactive tutorials with step-by-step protocol execution
- Visualization libraries for teaching distributed systems concepts
- Comprehensive documentation serving as distributed systems learning platform

**Production Pathway:**
- Integration APIs for real blockchain and distributed database systems
- Performance benchmarking against production consensus implementations (Raft, PBFT, HotStuff)
- Deployment templates for practical system integration

**Community Ecosystem:**
- Public protocol repository with contributed variants
- Shared experimental datasets and reproducibility benchmarks
- Collaborative research platform connecting theoretical and systems researchers

**The Vision**: Transform from thesis validation tool → standard research infrastructure → pathway to production deployment—making Byzantine Agreement research accessible, reproducible, and practically deployable.

---
