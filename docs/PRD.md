# Early-Stopping Byzantine Agreement Simulator & Prototype - Product Requirements Document

**Author:** Yarin
**Date:** 2025-11-03
**Version:** 1.0

---

## Executive Summary

The Early-Stopping Byzantine Agreement Simulator & Prototype is an M.Sc. research project that bridges the critical gap between theoretical distributed consensus research and empirical validation. This modular, extensible validation framework enables researchers to validate Byzantine Agreement protocols under realistic conditions—obtaining trustworthy safety/liveness verification plus performance analysis in hours rather than weeks.

The system implements a deterministic early-stopping BA stack with Lite PoP, CoD, and GDA subprotocols, built on Python 3.10+ with asyncio concurrency and comprehensive validation. The architecture enforces correctness through always-on property assertions (Agreement, Validity, Termination) while maintaining complete audit trails. Core adversary models exercise Byzantine resilience, and a minimal Perry-Toueg baseline enables direct empirical comparison demonstrating the breakthrough result: termination in approximately (1+ε)f rounds instead of the classical t+1 bound.

This project serves three critical purposes: validates cutting-edge theoretical work through concrete implementation, provides a reference platform for the broader research community, and creates a reusable foundation that prevents future researchers from starting from scratch.

### What Makes This Special

**This project proves elegant theory actually works in messy reality.**

The magic moment: Seeing the first clean plot where the early-stopping curve visibly beats the classical (t+1) curve—visual confirmation that theory bends where math predicts. Then watching adversarial scenarios run with zero Agreement violations, proving the implementation is robust, not a toy.

The lasting impact: Creating a working reference implementation that future researchers can build on instead of reimplementing everything from scratch. When someone says "I used this framework instead of starting from zero," that's when this becomes more than a thesis—it becomes a lasting contribution to distributed systems research.

---

## Project Classification

**Technical Type:** Scientific Computing + Developer Tool (Research Validation Framework)
**Domain:** Academic Research / Distributed Systems
**Complexity:** Medium-High

This project sits at the intersection of scientific computing (protocol simulation, empirical validation, statistical analysis) and developer tooling (extensible framework, pluggable components, research infrastructure). The domain complexity stems from Byzantine Agreement theory, distributed systems validation requirements, and the need to translate formal proofs into executable code with provable correctness properties.

{{#if domain_context_summary}}
### Domain Context

{{domain_context_summary}}
{{/if}}

---

## Success Criteria

### Primary Research Questions (Must Answer)

**1. Does early-stopping achieve approximately (1+ε)f rounds in practice?**

**Success**: For realistic settings where f ≪ t, termination rounds must scale linearly with f and remain close to the theoretical bound within a small constant offset. Visual confirmation through plots showing observed round counts tracking the predicted (1+ε)f curve across varied configurations.

**2. Is early-stopping meaningfully faster than (t+1) classical BA?**

**Success**: Clear empirical performance gap demonstrating **2–5× fewer rounds** than classical baseline when actual faults f are low. This validates practical significance of the theoretical improvement in common scenarios where Byzantine faults are rare.

**3. Does correctness hold under adversarial conditions?**

**Safety**: **Zero violations** of Agreement (no two honest nodes decide differently) and Validity (unanimous honest input preserved) across all experimental runs, regardless of adversary strategy or fault configuration.

**Liveness**: Guaranteed termination under synchrony assumptions across all tested scenarios within bounded rounds, even under maximum allowed faults and aggressive adversarial behavior.

### Thesis Committee Success Definition

A successful deliverable must demonstrate:

1. **Empirical Confirmation**: Clear evidence that early-stopping terminates in approximately (1+ε)f rounds under realistic implementation conditions
2. **Consistent Performance Advantage**: Reproducible gains over classical protocols in low-fault scenarios (f ≪ t) representing common operational conditions
3. **Absolute Correctness**: Zero safety violations under any tested adversarial configuration
4. **Transparent Evidence Trail**: Complete audit capability via certificate logs, transition records, and evidence stores
5. **Publication-Ready Presentation**: Clean, documented codebase with compelling visualizations demonstrating theory-to-practice validation

### Quantitative Targets

**Round Complexity**
- Primary metric: Rounds to decision as function of actual faults f
- Configurations: Multiple (n, t) pairs with fault sweeps f = 0…t
- Output: Line plots showing rounds vs. f with theoretical curve overlay

**Message Overhead**
- Total messages per experimental run
- Average messages sent per node per round
- Breakdown of payload bytes, signature overhead, auxiliary data

**Cryptographic Cost**
- Count of signature generation and verification operations
- Per-round cryptographic overhead analysis
- Cost-per-round summaries with baseline comparison

**Statistical Rigor**
- Multiple runs per configuration (10–50 depending on variance)
- Mean results with error bars (standard deviation or interquartile range)
- Seeded pseudo-random generation for deterministic reproducibility
- Statistical significance testing for performance claims

### The Magical Moment Metrics

**Visual Validation**: The moment the early-stopping curve visibly beats classical on the first clean plot—theory confirmed by measurement

**Safety Under Fire**: Zero Agreement violations across all adversarial stress tests—proof of robustness, not a toy implementation

**Researcher Impact**: When future researchers cite or build on this framework instead of reimplementing from scratch—lasting contribution achieved

---

## Product Scope

### MVP - Minimum Viable Product (Thesis Validation - 18-20 Weeks)

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

### Growth Features (Post-Thesis / Phase 2)

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

### Vision (Future / Research Community Platform)

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

## Domain-Specific Requirements

### Academic Research / Scientific Computing Context

This project operates within the academic research domain with specific methodological requirements that shape all design and implementation decisions:

**Reproducibility Requirements**
- Seeded pseudo-random number generation enabling bit-identical experiment reproduction
- Deterministic execution despite asyncio concurrency (controlled scheduling)
- Complete audit trails capturing every state transition and decision justification
- Version-locked dependencies and environment specifications

**Validation Methodology**
- Formal property assertions embedded in code (Agreement, Validity, Termination)
- Statistical rigor: multiple runs per configuration with confidence intervals
- Comparative baselines (Perry-Toueg) using identical experimental conditions
- Publication-quality evidence: graphs, tables, and statistical significance testing

**Theory-to-Practice Translation**
- Synchronous model with known Δ timeout bounds
- Authenticated Byzantine fault tolerance (t < n/2 with cryptographic signatures)
- Round-based execution matching theoretical protocol descriptions
- Evidence that real implementation behavior aligns with formal proofs

**Distributed Systems Complexity**
- Byzantine adversarial behavior (equivocation, withholding, timing attacks)
- Message ordering and scheduling non-determinism (within synchrony bounds)
- Cryptographic operation costs in real execution (not abstract "free" operations)
- Round boundary enforcement preventing retroactive state contamination

**Research Timeline Constraints**
- 18-20 week implementation window aligned with M.Sc. thesis schedule
- Feature freeze by Week 18 to allow analysis and writing (Weeks 19-20)
- Progressive complexity increase with validation gates before scaling
- Fallback scope reduction plan maintaining core research question answers

**Academic Contribution Standards**
- Clean, well-documented codebase serving as reference implementation
- Extensible architecture enabling future protocol experimentation
- Educational value for students learning Byzantine Agreement concepts
- Lasting research infrastructure preventing duplication of foundational work

These domain requirements directly inform the functional architecture (modular FSM design, evidence stores, property assertions) and non-functional requirements (correctness above all else, reproducibility as first-class concern, publication-quality outputs).

---

{{#if innovation_patterns}}
## Innovation & Novel Patterns

{{innovation_patterns}}

### Validation Approach

{{validation_approach}}
{{/if}}

---

{{#if project_type_requirements}}
## {{project_type}} Specific Requirements

{{project_type_requirements}}

{{#if endpoint_specification}}
### API Specification

{{endpoint_specification}}
{{/if}}

{{#if authentication_model}}
### Authentication & Authorization

{{authentication_model}}
{{/if}}

{{#if platform_requirements}}
### Platform Support

{{platform_requirements}}
{{/if}}

{{#if device_features}}
### Device Capabilities

{{device_features}}
{{/if}}

{{#if tenant_model}}
### Multi-Tenancy Architecture

{{tenant_model}}
{{/if}}

{{#if permission_matrix}}
### Permissions & Roles

{{permission_matrix}}
{{/if}}
{{/if}}

---

{{#if ux_principles}}
## User Experience Principles

{{ux_principles}}

### Key Interactions

{{key_interactions}}
{{/if}}

---

## Functional Requirements

### 1. Authenticated Transport Layer

**FR-1.1: Canonical Message Schema**
- System SHALL implement message structure: `(ssid, round, protocol_id, phase, sender_id, value|digest, aux, signature)`
- Each field SHALL have strict type enforcement and validation rules
- Messages SHALL be serialized using JSON with canonical key ordering for deterministic hashing
- Binary signatures SHALL be base64-encoded for JSON compatibility

**FR-1.2: Message Authentication**
- System SHALL cryptographically sign all messages using Ed25519 signatures (PyNaCl)
- System SHALL verify signatures on all received messages before acceptance
- Invalid signatures SHALL result in message rejection with logged audit event
- System SHALL maintain per-node key pairs (public/private) for authentication

**FR-1.3: Message Acceptance Rules**
- System SHALL validate message schema compliance before processing
- System SHALL enforce deduplication keyed by `(sender_id, round, protocol_id, phase)`
- System SHALL reject replayed messages (anti-replay protection via round binding)
- System SHALL enforce round firewall: messages for round r SHALL NOT be processed in rounds < r or after round r+1 transition

**FR-1.4: Message Delivery Scheduling**
- System SHALL support configurable per-message delay distributions (Uniform, Normal, Pareto)
- Delays SHALL be bounded by synchrony parameter Δ in standard operation
- System SHALL support message reordering within synchrony bounds
- System SHALL support controlled message drop with configurable probability

### 2. Protocol Implementation Stack

**FR-2.1: Lite PoP (Proof-of-Participation)**
- System SHALL embed prior-round participation digest in each message
- System SHALL implement local chain verification for participation evidence
- System SHALL track participation status per node per round
- System SHALL NOT require full PoP ANNOUNCE/PROOF phases in MVP

**FR-2.2: CoD (Consistent Dissemination)**
- System SHALL implement three phases: SEND, ECHO, READY
- System SHALL enforce threshold logic:
  - ECHO phase: n-t SEND messages triggers ECHO broadcast
  - READY phase: n-t ECHO messages OR t+1 READY messages triggers READY broadcast
  - Output: n-t READY messages constitutes certificate
- System SHALL detect equivocation through conflicting signed values
- System SHALL produce either consensus value or detect-set of conflicting proposals

**FR-2.3: GDA (Graded Agreement)**
- System SHALL implement two phases: PROPOSE, GRADE_VOTE
- System SHALL compute grades ∈ {0, 1, 2} based on message thresholds:
  - Grade 2: n-t matching proposals (strong consensus)
  - Grade 1: t+1 to n-t-1 matching proposals (weak consensus)
  - Grade 0: < t+1 matching proposals (no consensus)
- System SHALL produce (value, grade) tuples as output
- Grade 2 certificates SHALL enable safe early decision without additional rounds

**FR-2.4: Deterministic BA Controller**
- System SHALL orchestrate PoP → CoD → GDA subprotocol sequencing
- System SHALL implement certificate ∨ timeout advancement rule:
  - Certificate-based: Advance when n-t terminal-phase messages received
  - Timeout-based: Advance when Δ timeout expires without certificate
- System SHALL manage carryover state between rounds (digests, partial certificates)
- System SHALL enforce round monotonicity (no backward progression)
- System SHALL decide when grade-2 certificate obtained or safe decision condition met
- System SHALL prune impossible values based on graded evidence

**FR-2.5: Perry-Toueg Classical Baseline**
- System SHALL implement minimal classical BA with (t+1) round termination bound
- Baseline SHALL use identical transport layer and cryptographic infrastructure
- Baseline SHALL support same (n, t, f) configurations as early-stopping protocol
- Baseline SHALL enable direct performance comparison under identical experimental conditions

### 3. Adversary Models

**FR-3.1: Adversary Framework**
- System SHALL support pluggable adversary strategy interface
- System SHALL allow composition of multiple adversary behaviors to reach fault level f ≤ t
- System SHALL support seeded random number generation for reproducible adversarial behavior
- System SHALL log all adversarial actions for audit and debugging

**FR-3.2: Equivocator Adversary**
- SHALL sign conflicting payloads for identical `(round, protocol_id, phase)` tuples
- SHALL send different values to different honest nodes within same phase
- SHALL exercise protocol safety properties under Byzantine equivocation

**FR-3.3: Withholder Adversary**
- SHALL suppress terminal-phase messages until configurable late rounds
- SHALL delay certificate formation to test timeout-based advancement
- SHALL validate early-stopping resilience when adversaries prevent early termination

**FR-3.4: Delay/Drop Adversary**
- SHALL introduce per-message delays within synchrony bound Δ
- SHALL support configurable delay distributions (Uniform, Normal, Pareto)
- SHALL support message reordering and controlled drop probabilities
- SHALL validate liveness under realistic network jitter and packet loss

### 4. Validation Framework

**FR-4.1: Property Assertions (Always-On)**
- System SHALL enforce Agreement property: No two honest nodes decide different values
- System SHALL enforce Validity property: Unanimous honest input implies that value decided
- System SHALL enforce Termination property: Decision reached within bounded rounds under synchrony
- System SHALL enforce Round Firewall property: Post-round messages never mutate previous round state
- Assertion violations SHALL immediately halt execution with detailed diagnostic information

**FR-4.2: Evidence Store**
- System SHALL record barrier certificates: Sets of n-t terminal-phase signatures justifying round advancement
- System SHALL record transition records: Per-round metadata `{round, carryover_digest, advance_reason, advance_timestamp}`
- System SHALL record decision packages: Grade-2 or READY proof bundles demonstrating decision validity
- System SHALL record late message arrivals with `post_round=1` flag for audit (no state mutation)
- Evidence SHALL be immutable once recorded
- System SHALL support optional garbage collection for long-running experiments

**FR-4.3: Experiment Harness**
- System SHALL support parameterized batch execution over (n, t, f) configuration space
- System SHALL execute multiple runs per configuration (configurable 10-50 replications)
- System SHALL support adversary strategy mix specifications
- System SHALL export results to CSV/Parquet formats for analysis pipeline
- System SHALL generate seeded experiments enabling deterministic reproduction

**FR-4.4: Metrics Collection**
- System SHALL track rounds to decision per experimental run
- System SHALL count total messages sent/received per run
- System SHALL count messages per node per round
- System SHALL count signature generation and verification operations
- System SHALL measure message payload sizes and overhead breakdowns
- System SHALL capture execution timestamps for wall-clock analysis

**FR-4.5: Visualization & Reporting**
- System SHALL generate publication-quality plots: rounds vs. f with theoretical curve overlay
- System SHALL generate comparison plots: early-stopping vs. classical baseline
- System SHALL generate cryptographic cost analysis plots
- System SHALL compute mean results with error bars (standard deviation or IQR)
- System SHALL support statistical significance testing for performance claims

### 5. Simulation Engine

**FR-5.1: Round Scheduler**
- System SHALL implement lock-step round synchronization using asyncio coordination
- System SHALL enforce known timeout bound Δ per round
- System SHALL maintain per-round message inboxes with strict isolation
- System SHALL resolve carryover state before round advancement
- System SHALL prevent late message processing for state mutation (audit logging only)

**FR-5.2: Node Simulation**
- System SHALL simulate all nodes within single Python process (MVP)
- System SHALL maintain independent state per simulated node
- System SHALL enforce message delivery through centralized scheduler
- System SHALL support configurable node behaviors (honest vs. adversarial)

**FR-5.3: Deterministic Execution**
- System SHALL support seeded pseudo-random number generation
- System SHALL enable bit-identical reproduction of experimental runs given same seed
- System SHALL control asyncio scheduling to eliminate non-deterministic races
- System SHALL log sufficient detail to reconstruct execution paths

### 6. Experimental Configurations

**FR-6.1: Parameter Space Coverage**
- System SHALL support network sizes n ∈ {7, 13, 25, 31}
- System SHALL compute fault tolerance threshold t = ⌊(n−1)/2⌋
- System SHALL support fault sweeps f = 0, 1, 2, …, t
- System SHALL emphasize low-fault regime (f = 0-3) representing real-world conditions

**FR-6.2: Timing Parameters**
- System SHALL support configurable synchrony bound Δ (e.g., 50-200ms simulated time)
- System SHALL support delay distribution selection (Uniform, Normal, Pareto)
- System SHALL cap all delays at Δ in standard operation
- System SHALL support stress mode with delays exceeding Δ for robustness testing

**FR-6.3: Experimental Matrix**
- System SHALL support approximately 500-1000 total experimental runs
- Configuration matrix: 4 network sizes × fault sweeps × adversary strategies × replications
- System SHALL support selective execution of configuration subsets
- System SHALL resume interrupted experimental campaigns

### 7. Development & Deployment Infrastructure

**FR-7.1: Technology Stack**
- Language: Python 3.10+
- Concurrency: asyncio for event-driven scheduling
- Cryptography: PyNaCl for Ed25519 signatures
- Testing: pytest with property-based testing support
- Analysis: pandas for data manipulation, matplotlib for visualization

**FR-7.2: Code Organization**
- System SHALL implement modular FSM design for each subprotocol
- System SHALL isolate cryptographic operations from protocol logic
- System SHALL maintain clear separation between simulation engine and protocol implementation
- System SHALL provide plugin interface for future protocol variants

**FR-7.3: Testing Infrastructure**
- System SHALL provide comprehensive unit tests for each subprotocol FSM
- System SHALL provide integration tests for full BA stack
- System SHALL provide property-based tests exploring random adversarial schedules
- System SHALL validate correctness on small networks (n=4, n=7) before scaling

**FR-7.4: Documentation**
- System SHALL provide README with quickstart instructions
- System SHALL document message schema and protocol phases
- System SHALL document adversary models and behaviors
- System SHALL document experimental configuration options
- System SHALL provide code comments explaining Byzantine Agreement concepts

**Acceptance Criteria for FR Completeness:**
- All FR sections implemented enable answering the three primary research questions
- Implementation produces publication-quality empirical evidence within thesis timeline
- System maintains zero safety violations across all tested configurations
- Framework supports future protocol experimentation through pluggable architecture

---

## Non-Functional Requirements

### Correctness (Highest Priority - Non-Negotiable)

**NFR-1.1: Byzantine Agreement Properties**
- **Agreement**: System SHALL guarantee no two honest nodes decide different values (zero violations across all experiments)
- **Validity**: System SHALL guarantee unanimous honest input implies that value is decided
- **Termination**: System SHALL guarantee decision within bounded rounds under synchrony assumptions
- **Round Firewall**: System SHALL guarantee post-round messages never mutate previous round state

**NFR-1.2: Implementation Correctness**
- All threshold computations SHALL be mathematically verified (n-t, t+1 thresholds for n nodes with t fault tolerance)
- GDA grade transitions SHALL correctly implement theoretical specifications
- Certificate construction SHALL be sound (sufficient signatures of correct type and phase)
- Carryover state management SHALL be deterministic and consistent

**NFR-1.3: Verification Strategy**
- Always-on runtime assertions for all Byzantine Agreement properties
- Immediate execution halt with diagnostic information on property violation
- No "soft failures" or warnings for correctness violations—fail fast and loud

### Reproducibility (Critical for Research Validity)

**NFR-2.1: Deterministic Execution**
- All experimental runs SHALL be reproducible given identical seed
- Asyncio scheduling SHALL be deterministic (no uncontrolled race conditions)
- Pseudo-random number generation SHALL be seeded and controlled
- Bit-identical results SHALL be achievable across multiple runs with same configuration

**NFR-2.2: Audit Trail Completeness**
- All state transitions SHALL be recorded with justification (certificate or timeout)
- All messages SHALL be logged with sender, round, protocol, phase, signature
- All adversarial actions SHALL be logged for post-execution analysis
- Evidence store SHALL enable complete execution reconstruction

**NFR-2.3: Version Control**
- All dependencies SHALL be version-locked (requirements.txt with exact versions)
- Python version SHALL be specified (3.10+ minimum)
- Cryptographic library versions SHALL be frozen
- Experimental configuration files SHALL be version-controlled with results

### Performance Measurement (Not Optimization)

**NFR-3.1: Instrumentation Completeness**
- System SHALL measure rounds to decision with ±1 round accuracy
- System SHALL count all messages sent (no uncounted messages)
- System SHALL count all cryptographic operations (signature gen/verify)
- System SHALL measure wall-clock execution time per experimental run

**NFR-3.2: Measurement Overhead Acceptance**
- Logging and instrumentation overhead is ACCEPTABLE (research focus, not production performance)
- Detailed tracing SHALL NOT be disabled to "improve performance"
- Research correctness and evidence quality takes precedence over execution speed
- Single-machine simulation performance sufficient for n ≤ 31 experiments

**NFR-3.3: Scalability Target (MVP)**
- System SHALL complete single experimental run (n=31, f=t) in < 5 minutes
- System SHALL complete full experimental campaign (500-1000 runs) in < 24 hours batch execution
- Memory footprint SHALL remain tractable for laptop execution (< 8GB RAM)
- No distributed execution required for MVP (single-machine sufficient)

### Code Quality & Maintainability

**NFR-4.1: Readability**
- Code SHALL serve as reference implementation for Byzantine Agreement research
- Functions SHALL have clear docstrings explaining Byzantine Agreement concepts where applicable
- Variable names SHALL be descriptive (no cryptic abbreviations except standard BA terminology)
- Complex threshold logic SHALL include inline comments with mathematical justification

**NFR-4.2: Modularity**
- Each subprotocol SHALL be implemented as independent FSM
- Transport layer SHALL be isolated from protocol logic
- Cryptographic operations SHALL be isolated in dedicated module
- Simulation engine SHALL be separate from protocol implementations

**NFR-4.3: Extensibility**
- New protocol variants SHALL be addable without modifying core infrastructure
- New adversary strategies SHALL be pluggable via standard interface
- New delay distributions SHALL be configurable without code changes
- New metrics SHALL be collectable without restructuring measurement framework

**NFR-4.4: Testing Coverage**
- Unit tests SHALL cover all subprotocol phase transitions
- Integration tests SHALL validate full BA stack execution
- Property-based tests SHALL explore adversarial scenario space
- Regression tests SHALL prevent correctness property violations
- Test coverage goal: >80% for protocol logic (not including visualization/plotting code)

### Documentation & Educational Value

**NFR-5.1: Academic Documentation Standards**
- README SHALL provide quickstart with example execution in < 5 minutes
- Architecture document SHALL explain modular FSM design and message flow
- Protocol specification SHALL document all phases, thresholds, and advancement rules
- Adversary models SHALL be documented with behavioral specifications

**NFR-5.2: Reproducibility Documentation**
- Experimental configuration files SHALL be self-documenting
- Result interpretation guide SHALL explain metric meanings
- Plotting scripts SHALL include comments explaining graph constructions
- Seed management SHALL be documented for experiment reproduction

**NFR-5.3: Research Contribution Documentation**
- Code comments SHALL explain "why" not just "what" for Byzantine Agreement logic
- Theory-to-implementation translation SHALL be documented where proofs meet code
- Known limitations and assumptions SHALL be explicitly documented
- Future extension points SHALL be identified for Phase 2 work

### Usability (For Researchers)

**NFR-6.1: Configuration Simplicity**
- Experimental configurations SHALL be YAML or JSON (human-readable)
- Common parameter sweeps SHALL have pre-configured templates
- Default parameters SHALL represent reasonable research settings
- Command-line interface SHALL be intuitive (e.g., `python run_experiment.py --config exp1.yaml`)

**NFR-6.2: Result Accessibility**
- CSV output SHALL have clear column headers
- Plots SHALL have labeled axes, legends, and titles
- Error messages SHALL be helpful (not cryptic stack traces alone)
- Execution progress SHALL be visible (progress indicators for long runs)

**NFR-6.3: Development Experience**
- Setup SHALL be straightforward (virtualenv + pip install -r requirements.txt)
- Unit tests SHALL run fast (full test suite < 2 minutes)
- Linting and formatting SHALL be automated (black, flake8, mypy recommended)
- Development SHALL NOT require specialized hardware or cloud resources

### Reliability & Robustness

**NFR-7.1: Fault Tolerance (Ironic for BA Research)**
- Individual experimental run failures SHALL NOT corrupt entire campaign
- Interrupted batch executions SHALL be resumable
- Invalid configurations SHALL be detected before execution starts
- Assertion failures SHALL produce diagnostic dumps for debugging

**NFR-7.2: Input Validation**
- Invalid (n, t, f) configurations SHALL be rejected with clear error messages (e.g., f > t, t ≥ n/2)
- Missing configuration parameters SHALL use documented defaults or fail explicitly
- Adversary composition SHALL be validated (total adversarial nodes ≤ t)
- Cryptographic key validity SHALL be checked before protocol execution

**NFR-7.3: Graceful Degradation**
- Visualization failures SHALL NOT prevent result data export
- Missing optional components (e.g., plotting libraries) SHALL degrade gracefully
- Timeouts exceeding expected bounds SHALL log warnings but not crash
- Unexpected message patterns SHALL be logged and handled safely

### Research Ethics & Integrity

**NFR-8.1: Data Integrity**
- Raw experimental data SHALL NEVER be manually modified
- Result filtering or exclusion SHALL be documented with justification
- Statistical analysis SHALL report all runs (no cherry-picking)
- Failed runs SHALL be logged and reasons documented

**NFR-8.2: Transparency**
- All assumptions (synchrony, fault model, cryptographic) SHALL be explicitly stated
- Limitations SHALL be documented honestly
- Implementation gaps from theory SHALL be acknowledged
- Simplifications (Lite PoP vs. Full PoP) SHALL be clearly noted

**NFR-8.3: Academic Integrity**
- Code SHALL properly attribute theoretical sources (Elsheimy et al. early-stopping work)
- Baseline implementations SHALL cite original papers (Perry-Toueg)
- External libraries SHALL be properly credited
- Reused code patterns SHALL be documented

### Performance Acceptance Criteria

For MVP thesis validation, the following performance characteristics are ACCEPTABLE:

- **Execution Time**: Single run (n=31) in < 5 minutes; full campaign < 24 hours
- **Memory**: < 8GB RAM for all experimental configurations
- **Storage**: < 1GB for all experimental results (CSV + plots)
- **Instrumentation Overhead**: Detailed logging even if 2-3× slower than optimized version
- **Development Time**: Correctness takes precedence over performance optimization

**What is NOT required in MVP:**
- Production-grade performance optimization
- Signature batching or aggregation
- Message compression or wire protocol optimization
- Distributed multi-machine execution
- Real-time visualization or interactive dashboards

The focus is empirical validation of correctness and performance characteristics, not building a production-optimized system.

---

## Implementation Planning

### Development Timeline (18-20 Weeks)

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

### Development Approach

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

### Epic Breakdown Required

The PRD requirements must be decomposed into implementable epics and bite-sized stories (200k context limit for development agents).

**Next Step:** Run `/bmad:bmm:workflows:create-epics-and-stories` to create the implementation breakdown.

### Project-Level Estimation

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

## References

**Input Documents:**
- Product Brief: `docs/product-brief-final-project-code-2025-11-03.md`

**Theoretical Foundation:**
- Elsheimy et al. - Early-stopping Byzantine Agreement with (1+ε)f termination
- Perry-Toueg - Classical early Byzantine Agreement (baseline comparison)

**Domain Context:**
- Academic Research: M.Sc. thesis validation requirements
- Distributed Systems: Byzantine fault tolerance under synchrony
- Scientific Computing: Empirical protocol validation methodology

---

## Next Steps

### Immediate Next Actions

1. **Epic & Story Breakdown** (Required)
   - Run: `/bmad:bmm:workflows:create-epics-and-stories`
   - Decompose PRD requirements into implementable stories for development agents
   - Organize by architectural layers: Transport → Protocols → Adversaries → Validation → Experiments

2. **Architecture Definition** (Recommended)
   - Run: `/bmad:bmm:workflows:architecture`
   - Define modular FSM architecture for subprotocols
   - Document message flow and state transition patterns
   - Establish interfaces between simulation engine and protocol implementations

3. **Development Environment Setup**
   - Initialize Python 3.10+ virtual environment
   - Create requirements.txt with version-locked dependencies
   - Set up pytest framework for property-based testing
   - Establish code formatting standards (black, flake8, mypy)

### Implementation Sequence

**Phase 1: Foundation (Weeks 1-4)**
- Start with transport layer and message schema
- Validate cryptographic signing/verification
- Build round scheduler with deterministic asyncio coordination

**Phase 2: Protocols (Weeks 5-12)**
- Implement subprotocols as independent FSMs
- Integrate into BA controller with orchestration logic
- Validate on small networks before scaling

**Phase 3: Validation (Weeks 13-18)**
- Implement baseline for comparison
- Build experimental harness and metrics collection
- Execute full parameter sweeps and generate publication-quality results

**Phase 4: Thesis Writing (Weeks 19-20)**
- Analyze results against research questions
- Document findings and integrate into thesis
- Prepare defense materials

---

## The Magic Woven Throughout

**This PRD captures the essence of proving elegant theory works in messy reality.**

Every requirement traces back to the three primary research questions:
1. Does early-stopping achieve (1+ε)f in practice? → *Round tracking, statistical validation, theoretical curve overlay*
2. Is it meaningfully faster than classical BA? → *Perry-Toueg baseline, direct comparison, 2-5× improvement target*
3. Does correctness hold under adversaries? → *Always-on assertions, zero violation requirement, comprehensive adversary suite*

The magic moment this system creates:
- **Visual Validation**: Watching the early-stopping curve visibly beat classical on the first clean plot
- **Safety Under Fire**: Zero Agreement violations across all adversarial stress tests
- **Lasting Contribution**: When future researchers build on this instead of starting from scratch

Success means more than a thesis defense—it means creating a **trustworthy, modular, runnable Byzantine Agreement laboratory** that accelerates the path from theoretical innovation to practical validation.

---

_This PRD was created through collaborative discovery between Yarin and the Product Manager agent, transforming a comprehensive product brief into structured requirements ready for architecture design and epic breakdown._

**PRD Version:** 1.0
**Status:** Ready for Epic Breakdown
**Next Workflow:** `/bmad:bmm:workflows:create-epics-and-stories`
