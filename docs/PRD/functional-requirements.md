# Functional Requirements

## 1. Authenticated Transport Layer

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

## 2. Protocol Implementation Stack

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

## 3. Adversary Models

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

## 4. Validation Framework

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

## 5. Simulation Engine

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

## 6. Experimental Configurations

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

## 7. Development & Deployment Infrastructure

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
