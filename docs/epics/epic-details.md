# Epic Details

## Epic 1: Foundation Infrastructure (Weeks 1-4)

**Goal:** Establish the foundational transport layer, message schema, cryptographic authentication, and basic project structure that all protocol implementations will build upon.

**Business Value:** Creates the bedrock for Byzantine Agreement research—authenticated, deterministic message handling with cryptographic guarantees. Without this foundation, no protocol validation is possible.

**Technical Scope:**
- Canonical message schema with strict type enforcement
- Ed25519 cryptographic signing and verification (PyNaCl)
- Message acceptance rules (validation, deduplication, anti-replay)
- Basic project structure and testing infrastructure
- JSON serialization with abstraction for future CBOR migration

---

**Story 1.1: Project Structure & Dependencies**

As a researcher,
I want a well-organized Python project with version-locked dependencies,
So that I have a solid foundation for Byzantine Agreement implementation with reproducible builds.

**Acceptance Criteria:**
1. Python 3.10+ project structure created with standard layout (`src/`, `tests/`, `experiments/`, `docs/`)
2. `requirements.txt` with version-locked dependencies: PyNaCl, pytest, pandas, matplotlib, asyncio
3. `README.md` with quickstart setup instructions (virtualenv creation, dependency installation)
4. `.gitignore` configured for Python projects
5. Basic pytest configuration file (`pytest.ini`) created
6. Project runs `pytest` successfully (even with no tests initially)
7. Code formatting tools configured (black, flake8 recommended but optional in MVP)

**Prerequisites:** None (first story)

---

**Story 1.2: Message Schema Data Classes**

As a protocol developer,
I want canonical message data structures with strict type enforcement,
So that all protocol messages follow the schema: `(ssid, round, protocol_id, phase, sender_id, value|digest, aux, signature)`.

**Acceptance Criteria:**
1. Create `message.py` module with `Message` dataclass
2. Fields: `ssid` (str), `round` (int), `protocol_id` (str), `phase` (str), `sender_id` (int), `value` (Any), `digest` (Optional[bytes]), `aux` (Dict), `signature` (bytes)
3. Type hints enforced for all fields
4. `__post_init__` validation ensuring required fields are non-null
5. Helper method `to_dict()` for serialization preparation
6. Helper method `signing_payload()` returning canonical bytes for signing (excludes signature field)
7. Unit tests covering: valid message creation, type validation, signing payload generation
8. Docstrings explaining Byzantine Agreement message semantics

**Prerequisites:** Story 1.1

---

**Story 1.3: JSON Serialization with Canonical Ordering**

As a protocol developer,
I want deterministic JSON serialization for messages,
So that identical messages produce identical serialized bytes for cryptographic hashing and signatures.

**Acceptance Criteria:**
1. Create `serialization.py` module with `MessageSerializer` class
2. `encode(message: Message) -> bytes` method using JSON with canonical key ordering (`sort_keys=True`)
3. Binary fields (signature, digest) base64-encoded for JSON compatibility
4. `decode(data: bytes) -> Message` method reconstructing Message objects
5. Round-trip test: `decode(encode(msg)) == msg` for all message types
6. Deterministic output: same message always produces identical bytes
7. Abstraction layer designed for future CBOR migration (encode/decode interface only)
8. Unit tests covering: encoding, decoding, determinism, base64 handling, error cases

**Prerequisites:** Story 1.2

---

**Story 1.4: Cryptographic Key Generation & Management**

As a simulated node,
I want Ed25519 key pair generation and management,
So that I can sign messages and verify signatures using PyNaCl.

**Acceptance Criteria:**
1. Create `crypto.py` module with `NodeKeys` class
2. `generate_keypair() -> (SigningKey, VerifyKey)` using PyNaCl Ed25519
3. `NodeKeys` class storing `signing_key` (private) and `verify_key` (public)
4. `sign(payload: bytes) -> bytes` method generating Ed25519 signatures
5. `verify(payload: bytes, signature: bytes, verify_key: VerifyKey) -> bool` static method
6. Signature verification returns False for invalid signatures (no exceptions for normal operation)
7. Key serialization methods for test fixtures (optional but helpful)
8. Unit tests covering: key generation, signing, verification success, verification failure, deterministic signatures

**Prerequisites:** Story 1.1

---

**Story 1.5: Message Signing & Verification Integration**

As a protocol developer,
I want to sign messages and verify signatures using node keys,
So that all messages are cryptographically authenticated preventing forgery.

**Acceptance Criteria:**
1. Extend `Message` class with `sign(node_keys: NodeKeys) -> None` method
2. Signing populates `signature` field using `message.signing_payload()`
3. Add `verify_signature(verify_key: VerifyKey) -> bool` method to Message
4. Verification checks signature against signing payload
5. Message constructor validates signature is present when required
6. Integration test: Create message, sign it, verify with correct key (success), verify with wrong key (failure)
7. Unit tests covering: unsigned message handling, signature verification edge cases
8. Docstrings explaining Byzantine Agreement authentication model

**Prerequisites:** Stories 1.2, 1.3, 1.4

---

**Story 1.6: Message Acceptance Rules - Schema Validation**

As a protocol validator,
I want strict message schema validation before processing,
So that malformed or invalid messages are rejected immediately.

**Acceptance Criteria:**
1. Create `validation.py` module with `MessageValidator` class
2. `validate_schema(message: Message) -> bool` method checking:
   - All required fields are non-null
   - `round` is non-negative integer
   - `sender_id` is valid node ID (0 ≤ sender_id < n)
   - `protocol_id` and `phase` are non-empty strings
   - Signature is present and correct length (64 bytes for Ed25519)
3. Return `False` for invalid messages (log reason at debug level)
4. Validation happens before any protocol processing
5. Unit tests covering: valid messages pass, missing fields fail, invalid types fail, edge cases
6. Performance: validation should be fast (< 1ms per message)

**Prerequisites:** Story 1.2

---

**Story 1.7: Message Deduplication with Key-Based Tracking**

As a protocol validator,
I want message deduplication keyed by `(sender_id, round, protocol_id, phase)`,
So that duplicate messages are discarded and never processed twice.

**Acceptance Criteria:**
1. Extend `MessageValidator` with deduplication tracking
2. Maintain internal set of seen message keys: `(sender_id, round, protocol_id, phase)`
3. `is_duplicate(message: Message) -> bool` method checking if key already seen
4. First occurrence: add to seen set, return False
5. Subsequent occurrences: return True (duplicate)
6. Memory management: support clearing old rounds (will implement garbage collection later)
7. Unit tests covering: first message accepted, exact duplicate rejected, different phase accepted
8. Thread-safety considerations documented (not required for MVP single-threaded asyncio)

**Prerequisites:** Story 1.6

---

**Story 1.8: Anti-Replay Protection via Round Binding**

As a protocol validator,
I want messages rejected if they reference invalid rounds,
So that old messages cannot be replayed in future rounds (anti-replay protection).

**Acceptance Criteria:**
1. Extend `MessageValidator` with current round tracking
2. `set_current_round(round: int)` method updating validator state
3. Reject messages with `message.round < current_round` (too old)
4. Optionally reject messages with `message.round > current_round + 1` (too far ahead, configurable)
5. Round binding checked before deduplication (invalid rounds never enter seen set)
6. Clear logging when messages rejected due to round mismatch
7. Unit tests covering: current round accepted, old round rejected, future round handling
8. Integration test with round progression

**Prerequisites:** Story 1.7

---

**Story 1.9: Complete Message Acceptance Pipeline**

As a protocol engine,
I want a unified message acceptance pipeline integrating all validation rules,
So that only valid, authenticated, non-duplicate, properly-timed messages enter protocol processing.

**Acceptance Criteria:**
1. Create `accept_message(message: Message, verify_keys: Dict[int, VerifyKey]) -> bool` method
2. Acceptance pipeline order:
   - Schema validation (Story 1.6)
   - Signature verification (Story 1.5)
   - Round binding check (Story 1.8)
   - Deduplication check (Story 1.7)
3. Return `True` only if all checks pass
4. Log rejection reasons at appropriate levels (debug for duplicates, warn for invalid signatures)
5. Performance target: < 5ms per message including signature verification
6. Integration tests covering: fully valid message accepted, failures at each stage rejected
7. Statistics tracking: accepted count, rejected count by reason (helpful for debugging)

**Prerequisites:** Stories 1.5, 1.6, 1.7, 1.8

---

**Epic 1 Summary:**
- **9 stories** establishing foundation infrastructure
- **Can start immediately:** Story 1.1
- **Parallel opportunities:** Stories 1.2, 1.4 can run in parallel after 1.1; Stories 1.6, 1.7, 1.8 can partially overlap
- **Key milestone:** By end of Epic 1, messages can be created, signed, serialized, validated, and accepted with full cryptographic authentication
- **Testing:** Unit test coverage for all components, integration test for full pipeline

## Epic 2: Round Scheduler & Synchrony Model (Weeks 2-4)

**Goal:** Implement lock-step round synchronization with known timeout bound Δ, per-round message inboxes, carryover state management, and deterministic asyncio scheduling.

**Business Value:** Enables the synchronous model critical for early-stopping Byzantine Agreement. Without proper round boundaries and timeout enforcement, the (1+ε)f termination guarantee cannot be validated.

**Technical Scope:**
- Asyncio-based round scheduler with Δ timeout enforcement
- Per-round message inbox isolation (round firewall)
- Carryover state resolution before round advancement
- Certificate ∨ timeout advancement rule
- Deterministic execution for reproducibility

---

**Story 2.1: Basic Round Scheduler with Asyncio**

As a simulation engine,
I want lock-step round coordination using asyncio,
So that all nodes progress through rounds synchronously with controlled timing.

**Acceptance Criteria:**
1. Create `scheduler.py` module with `RoundScheduler` class
2. `__init__(n: int, delta: float)` constructor with node count and timeout bound Δ
3. `advance_round()` async method incrementing current round counter
4. `get_current_round() -> int` method returning current round
5. Asyncio coordination: all nodes wait at round boundary before advancement
6. Basic round progression test: advance through multiple rounds deterministically
7. Unit tests covering: initialization, round advancement, current round tracking
8. Docstrings explaining synchronous model and Δ timeout semantics

**Prerequisites:** Story 1.1

---

**Story 2.2: Per-Round Message Inboxes**

As a protocol node,
I want separate message inboxes per round,
So that messages for round r are isolated from round r+1 (round firewall).

**Acceptance Criteria:**
1. Extend `RoundScheduler` with per-round inbox storage: `Dict[int, List[Message]]`
2. `deliver_message(message: Message)` method routing messages to correct round inbox
3. `get_round_messages(round: int) -> List[Message]` method retrieving messages for specific round
4. Messages delivered to `round_inboxes[message.round]`
5. Round firewall: messages for round < current_round logged but not processed for state mutation
6. Late message handling: flag messages arriving after round transition with `post_round=True` metadata
7. Unit tests covering: message routing, inbox isolation, late message handling
8. Integration test: messages delivered across multiple rounds stay isolated

**Prerequisites:** Stories 1.9, 2.1

---

**Story 2.3: Timeout Enforcement with Δ Bound**

As a round scheduler,
I want timeout-based round advancement after Δ expires,
So that protocol doesn't deadlock when certificates aren't formed.

**Acceptance Criteria:**
1. Add `wait_for_certificate_or_timeout(timeout_seconds: float)` async method
2. Uses `asyncio.wait_for` with Δ timeout
3. Returns `"certificate"` if advancement condition met before timeout
4. Returns `"timeout"` if Δ expires without certificate
5. Configurable Δ per round (default from constructor)
6. Timeout tracking: log timeout events for analysis
7. Unit tests covering: certificate advancement (fast), timeout advancement (slow), edge cases
8. Integration test: round advances via timeout when no certificate forms

**Prerequisites:** Story 2.1

---

**Story 2.4: Certificate Tracking & Advancement Condition**

As a BA controller,
I want to track terminal-phase message accumulation for certificate formation,
So that rounds can advance early when n-t threshold is reached.

**Acceptance Criteria:**
1. Create `certificate_tracker.py` module with `CertificateTracker` class
2. `add_terminal_message(message: Message)` method accumulating terminal-phase messages
3. `has_certificate(n: int, t: int) -> bool` method checking if n-t threshold reached
4. Track messages by `(protocol_id, phase)` for multi-protocol support
5. Certificate condition: at least n-t messages from distinct senders in terminal phase
6. `get_certificate_messages() -> List[Message]` returning messages forming certificate
7. Unit tests covering: threshold detection, distinct sender validation, multi-protocol handling
8. Edge case: exactly n-t messages triggers certificate

**Prerequisites:** Story 1.2

---

**Story 2.5: Carryover State Management**

As a protocol node,
I want carryover state (digests, partial certificates) managed between rounds,
So that information from incomplete protocols carries forward correctly.

**Acceptance Criteria:**
1. Extend `RoundScheduler` with carryover state storage: `Dict[str, Any]`
2. `set_carryover(key: str, value: Any)` method storing state for next round
3. `get_carryover(key: str) -> Any` method retrieving carryover from previous round
4. `clear_carryover()` method resetting carryover after round advancement
5. Carryover resolution happens BEFORE round advancement (state frozen)
6. Carryover includes: participation digests, partial vote counts, prune sets
7. Unit tests covering: set/get carryover, round boundary behavior, clearing
8. Integration test: carryover survives round transition, cleared after use

**Prerequisites:** Story 2.1

---

**Story 2.6: Deterministic Asyncio Scheduling**

As a researcher,
I want deterministic asyncio task scheduling with seeded randomness,
So that experimental runs are reproducible with identical seeds.

**Acceptance Criteria:**
1. Create `determinism.py` module with seeded RNG management
2. `set_seed(seed: int)` function configuring global random seed (Python `random`, `numpy` if used)
3. Asyncio task scheduling order made deterministic (use task IDs or explicit ordering)
4. Message delivery order deterministic when multiple messages arrive simultaneously
5. Document any sources of non-determinism (e.g., asyncio internal scheduling)
6. Reproducibility test: same seed produces identical round-by-round message sequences
7. Unit tests covering: seeded execution, reproducible random choices
8. Integration test: two runs with same seed produce bit-identical message delivery order

**Prerequisites:** Story 2.2

---

**Story 2.7: Late Message Logging & Audit Trail**

As a researcher,
I want late-arriving messages logged but never mutating previous round state,
So that I can audit post-round arrivals without violating round firewall.

**Acceptance Criteria:**
1. Extend message delivery to detect late arrivals (message.round < current_round)
2. Late messages logged with full headers + signature but NOT processed for state mutation
3. Late message log includes: message metadata, arrival timestamp, round delta
4. Separate late message storage: `late_messages: List[Message]` for audit
5. Optional: Late message statistics (count by round, sender)
6. Round firewall enforcement test: assert no late message mutates protocol state
7. Unit tests covering: late message detection, logging, isolation from protocol logic
8. Audit trail export for analysis (CSV format with late message details)

**Prerequisites:** Story 2.2

---

**Story 2.8: Complete Certificate ∨ Timeout Advancement**

As a round scheduler,
I want certificate-or-timeout advancement rule fully integrated,
So that rounds progress either when n-t certificate forms OR Δ timeout expires.

**Acceptance Criteria:**
1. Integrate `CertificateTracker` (Story 2.4) with `RoundScheduler` (Story 2.1)
2. `wait_for_advancement(n: int, t: int, delta: float) -> str` async method
3. Advancement triggers:
   - Early: n-t terminal-phase messages → return "certificate"
   - Fallback: Δ timeout expires → return "timeout"
4. Advancement reason recorded in transition log
5. Carryover state resolved BEFORE round increment
6. Round advancement test: certificate-based advancement faster than timeout
7. Integration test: timeout advancement when only n-t-1 messages arrive
8. Performance: advancement detection within 10ms of condition met

**Prerequisites:** Stories 2.2, 2.3, 2.4, 2.5

---

**Epic 2 Summary:**
- **8 stories** implementing synchronous round model
- **Parallel opportunities:** Stories 2.4, 2.6 can develop in parallel with 2.2-2.3
- **Key milestone:** Lock-step round progression with certificate ∨ timeout advancement operational
- **Critical for research:** Deterministic scheduling enables reproducible experiments

---

## Epic 3: Protocol Primitives - CoD & GDA (Weeks 5-8)

**Goal:** Implement Consistent Dissemination (CoD) and Graded Agreement (GDA) subprotocols as independent finite state machines with threshold logic.

**Business Value:** Core subprotocols for early-stopping Byzantine Agreement. CoD provides reliable broadcast, GDA produces graded consensus values enabling early termination.

**Technical Scope:**
- CoD: SEND/ECHO/READY phases with threshold logic
- GDA: PROPOSE/GRADE_VOTE phases with grade computation (0/1/2)
- Finite state machine pattern for protocol modularity
- Threshold detection: n-t, t+1 message counts
- Equivocation detection in CoD

---

**Story 3.1: Protocol FSM Base Class**

As a protocol developer,
I want a base finite state machine pattern for all subprotocols,
So that CoD, GDA, PoP follow consistent implementation structure.

**Acceptance Criteria:**
1. Create `protocol_fsm.py` module with `ProtocolFSM` abstract base class
2. Abstract methods: `process_message(msg: Message)`, `get_output()`, `get_current_phase()`
3. FSM state storage: current phase, accumulated messages per phase, thresholds reached
4. Phase enumeration per protocol (CoD phases, GDA phases, etc.)
5. Helper method `count_messages_from_distinct_senders(phase: str) -> int`
6. Transition logging: record all phase transitions with justification
7. Unit tests for base class behaviors (if not purely abstract)
8. Docstrings explaining Byzantine Agreement FSM pattern

**Prerequisites:** Story 1.2

---

**Story 3.2: CoD - SEND Phase Implementation**

As a CoD protocol,
I want to process SEND messages and accumulate them,
So that I can trigger ECHO phase when n-t SEND messages received.

**Acceptance Criteria:**
1. Create `cod.py` module with `CoD` class inheriting from `ProtocolFSM`
2. Initialize in SEND phase
3. `process_message(msg)` for SEND phase:
   - Validate protocol_id="CoD", phase="SEND"
   - Accumulate SEND messages in internal storage
   - Track distinct senders
4. Threshold detection: when ≥ n-t SEND messages from distinct senders → transition to ECHO
5. ECHO trigger emits broadcast message with aggregated value or digest
6. Unit tests covering: SEND accumulation, threshold detection, ECHO transition
7. Edge case: exactly n-t SEND messages triggers ECHO

**Prerequisites:** Story 3.1

---

**Story 3.3: CoD - ECHO Phase with Equivocation Detection**

As a CoD protocol,
I want to process ECHO messages and detect equivocation,
So that I can safely transition to READY phase with consensus or detect-set.

**Acceptance Criteria:**
1. Extend `CoD` to handle ECHO phase
2. `process_message(msg)` for ECHO phase:
   - Accumulate ECHO messages
   - Detect equivocation: same sender, different values in ECHO
3. Threshold conditions for READY transition:
   - n-t matching ECHO messages → READY with consensus value
   - OR t+1 READY messages → READY (amplification)
4. Equivocation handling: flag conflicting values, produce detect-set
5. Unit tests covering: matching ECHO, equivocation detection, READY transition
6. Integration test: honest nodes reach READY, equivocator detected

**Prerequisites:** Story 3.2

---

**Story 3.4: CoD - READY Phase & Certificate Formation**

As a CoD protocol,
I want to accumulate READY messages and form certificates,
So that I can output consensus value when n-t READY threshold reached.

**Acceptance Criteria:**
1. Extend `CoD` to handle READY phase (terminal phase for CoD)
2. `process_message(msg)` for READY phase:
   - Accumulate READY messages
   - Track distinct senders
3. Certificate condition: n-t READY messages from distinct senders
4. `get_output() -> (value, certificate)` method returning consensus value + proof
5. Certificate proof: list of n-t signed READY messages
6. Unit tests covering: READY accumulation, certificate formation, output extraction
7. Integration test: full CoD execution SEND → ECHO → READY → certificate

**Prerequisites:** Story 3.3

---

**Story 3.5: GDA - PROPOSE Phase Implementation**

As a GDA protocol,
I want to process PROPOSE messages and accumulate proposals,
So that I can compute grades based on proposal distribution.

**Acceptance Criteria:**
1. Create `gda.py` module with `GDA` class inheriting from `ProtocolFSM`
2. Initialize in PROPOSE phase
3. `process_message(msg)` for PROPOSE phase:
   - Validate protocol_id="GDA", phase="PROPOSE"
   - Accumulate PROPOSE messages with values
   - Track value distribution: count per distinct value
4. After PROPOSE collection period, transition to GRADE_VOTE phase
5. Prepare for grading: identify most common value(s) and counts
6. Unit tests covering: PROPOSE accumulation, value distribution tracking
7. Edge case: multiple values with equal counts

**Prerequisites:** Story 3.1

---

**Story 3.6: GDA - Grade Computation Logic**

As a GDA protocol,
I want to compute grades ∈ {0, 1, 2} based on message thresholds,
So that I can produce graded consensus values enabling early-stopping.

**Acceptance Criteria:**
1. Implement `compute_grade(value: Any, count: int, n: int, t: int) -> int` method
2. Grade definitions:
   - Grade 2: count ≥ n-t (strong consensus)
   - Grade 1: t+1 ≤ count < n-t (weak consensus)
   - Grade 0: count < t+1 (no consensus)
3. Most common value receives highest grade
4. If no value reaches t+1, all grades are 0
5. Grade computation test: verify thresholds for all grade values
6. Unit tests covering: grade 2, grade 1, grade 0, edge cases (exactly n-t, exactly t+1)
7. Mathematical correctness: grades align with theoretical GDA specification

**Prerequisites:** Story 3.5

---

**Story 3.7: GDA - GRADE_VOTE Phase & Output**

As a GDA protocol,
I want to emit GRADE_VOTE messages with computed grades,
So that all nodes reach agreement on graded values.

**Acceptance Criteria:**
1. Extend `GDA` to handle GRADE_VOTE phase (terminal phase for GDA)
2. After PROPOSE phase, compute grade for most common value
3. Broadcast GRADE_VOTE message with `(value, grade)` tuple
4. Accumulate GRADE_VOTE messages from other nodes
5. `get_output() -> (value, grade)` method returning graded consensus
6. Grade-2 certificates enable early decision (no further rounds needed)
7. Unit tests covering: GRADE_VOTE emission, accumulation, output extraction
8. Integration test: full GDA execution PROPOSE → GRADE_VOTE → graded output

**Prerequisites:** Story 3.6

---

**Story 3.8: Lite PoP - Participation Digest Embedding**

As a Lite PoP implementation,
I want to embed prior-round participation digests in messages,
So that I provide participation evidence without full PoP machinery.

**Acceptance Criteria:**
1. Create `lite_pop.py` module with `LitePoP` class
2. `compute_participation_digest(round: int, messages: List[Message]) -> bytes` method
3. Digest = hash of sorted sender IDs from previous round messages
4. Embed digest in message `aux` field: `aux['participation_digest']`
5. `verify_participation(message: Message, expected_digest: bytes) -> bool` method
6. Local chain verification: check digest matches previous round
7. Unit tests covering: digest computation, embedding, verification
8. Note: Full PoP ANNOUNCE/PROOF phases deferred to Phase 2

**Prerequisites:** Story 1.2

---

**Epic 3 Summary:**
- **8 stories** implementing CoD, GDA, and Lite PoP subprotocols
- **Parallel opportunities:** CoD (Stories 3.2-3.4) and GDA (Stories 3.5-3.7) can develop in parallel after 3.1
- **Key milestone:** All subprotocols operational as independent FSMs with threshold logic
- **Testing:** Unit tests per phase, integration tests for full protocol execution

---

##  Epic 4: BA Controller & Early-Stopping Logic (Weeks 9-11)

**Goal:** Implement deterministic BA controller orchestrating PoP/CoD/GDA subprotocol sequencing, managing carryover state, and implementing early-stopping termination logic.

**Business Value:** The heart of early-stopping Byzantine Agreement—coordinates subprotocols to achieve (1+ε)f termination. This is what differentiates early-stopping from classical (t+1) protocols.

**Technical Scope:**
- BA controller orchestrating PoP → CoD → GDA sequence
- Certificate ∨ timeout advancement integrated with subprotocols
- Decision logic: grade-2 certificates enable early termination
- Value pruning based on graded evidence
- Carryover state management between rounds

---

**Story 4.1: BA Controller Initialization & Configuration**

As a BA simulation,
I want a BA controller managing protocol orchestration,
So that I can coordinate PoP, CoD, GDA execution across rounds.

**Acceptance Criteria:**
1. Create `ba_controller.py` module with `BAController` class
2. `__init__(n: int, t: int, node_id: int, initial_value: Any)` constructor
3. Initialize subprotocol instances: LitePoP, CoD, GDA
4. Configuration: network parameters (n, t), node identity, input value
5. State storage: current round, current subprotocol, accumulated evidence
6. `start_round(round: int)` method initializing round-specific state
7. Unit tests covering: initialization, configuration validation
8. Docstrings explaining BA controller role in early-stopping protocol

**Prerequisites:** Stories 3.4, 3.7, 3.8

---

**Story 4.2: Subprotocol Sequencing - PoP → CoD → GDA**

As a BA controller,
I want to sequence PoP, CoD, GDA subprotocols within each round,
So that protocols execute in correct order with proper state transitions.

**Acceptance Criteria:**
1. Implement `run_round(round: int)` async method orchestrating subprotocols
2. Sequencing order: LitePoP → CoD → GDA
3. Each subprotocol runs to completion before next starts
4. State transitions logged: PoP complete, CoD complete, GDA complete
5. Pass outputs between protocols: CoD output → GDA input
6. Handle subprotocol failures gracefully (timeout, no certificate)
7. Unit tests covering: correct sequencing, state transitions, output passing
8. Integration test: full round execution through all three subprotocols

**Prerequisites:** Story 4.1

---

**Story 4.3: Early Decision Logic - Grade-2 Certificate Detection**

As a BA controller,
I want to detect grade-2 certificates and decide immediately,
So that I can terminate in (1+ε)f rounds without waiting for (t+1) rounds.

**Acceptance Criteria:**
1. Implement `check_decision_condition() -> Optional[Any]` method
2. Decision condition: grade-2 certificate from GDA (n-t nodes propose same value)
3. If grade-2 detected → set `decided = True`, store decision value
4. If grade-2 not reached → continue to next round
5. Decision is final (no further rounds after decision)
6. Log decision event with round number and justification
7. Unit tests covering: grade-2 triggers decision, lower grades continue
8. Integration test: early termination at round ~(1+ε)f when grade-2 forms

**Prerequisites:** Story 4.2

---

**Story 4.4: Value Pruning Based on Graded Evidence**

As a BA controller,
I want to prune impossible values based on graded evidence,
So that I converge toward consensus by eliminating values with low grades.

**Acceptance Criteria:**
1. Implement `prune_values(gda_output: (value, grade))` method
2. Pruning rule: if value receives grade < 1, eliminate from consideration
3. Maintain working set of viable values across rounds
4. Update input value for next round based on highest-graded value
5. Carryover pruned set to next round
6. Unit tests covering: pruning logic, working set updates
7. Integration test: value set converges over multiple rounds

**Prerequisites:** Story 4.3

---

**Story 4.5: Carryover State Integration with Subprotocols**

As a BA controller,
I want to manage carryover state between rounds,
So that partial certificates, digests, and pruned sets carry forward correctly.

**Acceptance Criteria:**
1. Integrate carryover state from `RoundScheduler` (Story 2.5) into BA controller
2. Carryover includes: participation digest (PoP), partial vote counts, prune set
3. `prepare_carryover() -> Dict[str, Any]` method packaging state for next round
4. `restore_carryover(state: Dict[str, Any])` method loading previous round state
5. Carryover resolution happens BEFORE round advancement
6. Unit tests covering: carryover preparation, restoration, round boundaries
7. Integration test: state survives round transition, used correctly in next round

**Prerequisites:** Stories 2.5, 4.2

---

**Story 4.6: Round Advancement with Certificate ∨ Timeout**

As a BA controller,
I want round advancement triggered by certificate OR timeout,
So that protocol progresses either when subprotocols complete or Δ expires.

**Acceptance Criteria:**
1. Integrate `RoundScheduler` advancement (Story 2.8) with BA controller
2. After GDA completes, check for grade-2 certificate (early decision)
3. If no decision, wait for certificate ∨ timeout before advancing
4. Advancement reason logged: "certificate" or "timeout"
5. Timeout-based advancement continues protocol (no early termination)
6. Unit tests covering: certificate-based advancement, timeout fallback
7. Integration test: round advances via timeout when no grade-2 forms

**Prerequisites:** Stories 2.8, 4.5

---

**Story 4.7: Byzantine Agreement Property Assertions**

As a BA validator,
I want always-on assertions for Agreement, Validity, Termination properties,
So that correctness violations halt execution immediately with diagnostics.

**Acceptance Criteria:**
1. Create `assertions.py` module with property checking functions
2. `assert_agreement(decisions: Dict[int, Any])` checks no two honest nodes decide differently
3. `assert_validity(inputs: Dict[int, Any], decision: Any)` checks unanimous input preserved
4. `assert_termination(round: int, max_rounds: int)` checks bounded termination
5. Assertions run after each round and at final decision
6. Assertion failure: halt execution, dump full state, log violation details
7. Unit tests covering: valid executions pass, violations detected
8. Integration test: property violations trigger immediate failure

**Prerequisites:** Story 4.3

---

**Story 4.8: Complete BA Controller Integration Test**

As a BA system,
I want full end-to-end BA controller execution,
So that I can validate early-stopping behavior on small networks (n=7).

**Acceptance Criteria:**
1. Integration test: n=7, t=3, f=0 (no faults) → all nodes decide in ~2-3 rounds
2. Test with f=1 fault → decision in ~3-4 rounds (early-stopping advantage)
3. Test with f=t=3 faults → decision in ≤ t+1 rounds (classical bound)
4. Verify grade-2 certificates trigger early termination
5. Verify timeout advancement when certificates don't form
6. All Byzantine Agreement properties asserted throughout
7. Integration test produces decision log with round count, advancement reasons
8. Performance: n=7 execution completes in < 10 seconds

**Prerequisites:** Stories 4.1-4.7

---

**Epic 4 Summary:**
- **8 stories** implementing complete early-stopping BA controller
- **Key milestone:** Full BA execution operational on small networks (n=7)
- **Critical validation:** Early-stopping behavior demonstrates (1+ε)f termination
- **Testing:** Property assertions enforced throughout execution

---

## Epic 5: Adversary Framework (Weeks 10-12)

**Goal:** Implement pluggable adversary models (Equivocator, Withholder, Delay/Drop) with reproducible seeded behavior for Byzantine resilience testing.

**Business Value:** Validates correctness under adversarial conditions—zero safety violations despite Byzantine behavior is the core research claim.

**Technical Scope:**
- Adversary strategy interface for pluggable behaviors
- Equivocator: conflicting signatures within same phase
- Withholder: suppresses terminal-phase messages
- Delay/Drop: realistic message scheduling within Δ bounds
- Seeded reproducible adversarial behavior

---

**Story 5.1: Adversary Strategy Interface**

As an adversary framework,
I want a pluggable strategy interface for Byzantine behaviors,
So that new adversary types can be added without modifying core infrastructure.

**Acceptance Criteria:**
1. Create `adversary.py` module with `AdversaryStrategy` abstract base class
2. Abstract methods: `intercept_send(message: Message) -> List[Message]`, `should_drop(message: Message) -> bool`
3. Adversary configuration: node_id, fault type, intensity parameters
4. Seeded RNG for reproducible behavior
5. Logging: all adversarial actions logged for audit
6. Multiple adversaries can compose to reach fault level f
7. Unit tests for base interface (if not purely abstract)
8. Docstrings explaining Byzantine adversary patterns

**Prerequisites:** Story 1.2

---

**Story 5.2: Equivocator Adversary Implementation**

As an Equivocator adversary,
I want to send conflicting values to different honest nodes within same phase,
So that I can test CoD equivocation detection and protocol safety.

**Acceptance Criteria:**
1. Create `EquivocatorAdversary` class inheriting from `AdversaryStrategy`
2. `intercept_send(message)` generates multiple conflicting messages:
   - Same `(round, protocol_id, phase, sender_id)`
   - Different `value` fields
   - Each message signed correctly (adversary has valid keys)
3. Send different values to different recipients (targeted equivocation)
4. Equivocation only in specified phases (e.g., CoD SEND phase)
5. Track equivocation events for logging
6. Unit tests covering: message splitting, conflicting values, signature validity
7. Integration test: Equivocator triggers CoD equivocation detection

**Prerequisites:** Story 5.1

---

**Story 5.3: Withholder Adversary Implementation**

As a Withholder adversary,
I want to suppress terminal-phase messages until late rounds,
So that I can test certificate ∨ timeout advancement and early-stopping resilience.

**Acceptance Criteria:**
1. Create `WithholderAdversary` class inheriting from `AdversaryStrategy`
2. Configuration: withhold_until_round parameter
3. `intercept_send(message)` behavior:
   - If message is terminal-phase (READY, GRADE_VOTE) → buffer message
   - Release buffered messages after withhold_until_round
4. Withholder delays certificate formation, forcing timeout advancement
5. Eventually releases messages (not permanent silence)
6. Unit tests covering: message buffering, release logic, phase targeting
7. Integration test: Withholder prevents early certificate, protocol advances via timeout

**Prerequisites:** Story 5.1

---

**Story 5.4: Delay/Drop Adversary Implementation**

As a Delay/Drop adversary,
I want to introduce message delays and drops within synchrony bound Δ,
So that I can test protocol liveness under realistic network jitter.

**Acceptance Criteria:**
1. Create `DelayDropAdversary` class inheriting from `AdversaryStrategy`
2. Configuration: delay_distribution (Uniform, Normal, Pareto), drop_probability
3. `should_drop(message) -> bool` method using seeded RNG
4. `get_delay(message) -> float` method sampling from delay distribution
5. All delays capped at Δ (synchrony bound)
6. Dropped messages logged for audit
7. Unit tests covering: delay sampling, drop probability, Δ capping
8. Integration test: protocol maintains liveness despite delays/drops

**Prerequisites:** Story 5.1

---

**Story 5.5: Adversary Composition for Fault Level f**

As a simulation engine,
I want to compose multiple adversary behaviors to reach target fault level f,
So that I can test protocol with exactly f Byzantine nodes.

**Acceptance Criteria:**
1. Create `AdversaryComposition` class managing multiple adversaries
2. Configuration: list of `(node_id, strategy)` tuples, total f ≤ t
3. Validate: total adversarial nodes ≤ t (fault tolerance bound)
4. Route messages through appropriate adversary strategies per node
5. Honest nodes bypass adversary logic
6. Support mixed strategies: some equivocators, some withholders
7. Unit tests covering: composition validation, routing, mixed strategies
8. Integration test: f=2 with 1 Equivocator + 1 Withholder

**Prerequisites:** Stories 5.2, 5.3, 5.4

---

**Story 5.6: Reproducible Adversarial Behavior with Seeding**

As a researcher,
I want reproducible adversarial behavior controlled by seed,
So that I can re-run experiments with identical Byzantine patterns.

**Acceptance Criteria:**
1. Extend all adversary strategies to accept seed parameter
2. Seeded RNG used for: equivocation targets, withhold timing, delay sampling, drop decisions
3. Same seed produces identical adversarial action sequence
4. Seed management: global seed or per-adversary seeds
5. Reproducibility test: two runs with same seed produce identical adversary logs
6. Unit tests covering: seeded equivocation, seeded delays, determinism
7. Integration test: full BA execution with seeded adversaries reproduces results

**Prerequisites:** Stories 2.6, 5.5

---

**Epic 5 Summary:**
- **6 stories** implementing core adversary models
- **Parallel opportunities:** Stories 5.2, 5.3, 5.4 can develop in parallel after 5.1
- **Key milestone:** Byzantine resilience validated under Equivocator, Withholder, Delay/Drop attacks
- **Testing:** Zero safety violations despite adversarial behavior

---

## Epic 6: Validation & Evidence Infrastructure (Weeks 11-13)

**Goal:** Implement property assertions, evidence store, round firewall enforcement, and audit trails for complete execution reconstruction.

**Business Value:** Proves correctness through always-on assertions and enables audit of every decision with cryptographic evidence—essential for research credibility.

**Technical Scope:**
- Property assertions: Agreement, Validity, Termination, Round Firewall
- Evidence store: barrier certificates, transition records, decision packages
- Immutable evidence with optional garbage collection
- Audit trail export for analysis

---

**Story 6.1: Evidence Store Infrastructure**

As a validator,
I want an immutable evidence store for certificates and decision proofs,
So that I can reconstruct execution paths and verify correctness claims.

**Acceptance Criteria:**
1. Create `evidence_store.py` module with `EvidenceStore` class
2. Evidence types: barrier_certificates, transition_records, decision_packages
3. `add_evidence(type: str, round: int, data: Any)` method storing evidence immutably
4. `get_evidence(type: str, round: int) -> Any` method retrieving evidence
5. Evidence includes: cryptographic proofs (signatures), timestamps, justifications
6. Immutability: evidence cannot be modified after recording
7. Unit tests covering: evidence storage, retrieval, immutability
8. Optional: garbage collection for old rounds (configurable retention policy)

**Prerequisites:** Story 1.2

---

**Story 6.2: Barrier Certificate Recording**

As an evidence store,
I want to record barrier certificates (n-t terminal-phase signatures),
So that I can prove round advancement was justified by sufficient honest messages.

**Acceptance Criteria:**
1. Extend `EvidenceStore` with barrier certificate recording
2. Barrier certificate = set of ≥ n-t signed terminal-phase messages
3. `record_barrier_certificate(round: int, messages: List[Message])` method
4. Certificate validation: verify signatures, check distinct senders, validate phase
5. Compact representation: store message digests + signatures (not full payloads)
6. Certificate proof can be independently verified by third party
7. Unit tests covering: certificate recording, validation, compact storage
8. Integration test: barrier certificates recorded for each round advancement

**Prerequisites:** Story 6.1

---

**Story 6.3: Transition Record Logging**

As an evidence store,
I want to log transition records for each round advancement,
So that I can audit advancement reasons (certificate vs. timeout) and timestamps.

**Acceptance Criteria:**
1. Extend `EvidenceStore` with transition record logging
2. Transition record fields: `{round, carryover_digest, advance_reason, advance_timestamp}`
3. `record_transition(round: int, reason: str, timestamp: float, carryover: bytes)` method
4. Advancement reason: "certificate" or "timeout"
5. Carryover digest: hash of carryover state proving consistency
6. Timestamps enable timing analysis (wall-clock vs. simulated time)
7. Unit tests covering: transition recording, field validation
8. Integration test: complete execution produces transition log for all rounds

**Prerequisites:** Story 6.1

---

**Story 6.4: Decision Package Assembly**

As an evidence store,
I want to assemble decision packages with grade-2 or READY proofs,
So that I can prove final decisions are justified by sufficient evidence.

**Acceptance Criteria:**
1. Extend `EvidenceStore` with decision package recording
2. Decision package = `{decision_value, decision_round, proof_messages, proof_type}`
3. Proof type: "grade-2 certificate" (GDA) or "READY certificate" (CoD)
4. `record_decision(value: Any, round: int, proof: List[Message])` method
5. Decision proof independently verifiable (signatures, thresholds)
6. Package includes all information needed for third-party validation
7. Unit tests covering: decision package assembly, proof validation
8. Integration test: final decision produces complete verifiable package

**Prerequisites:** Story 6.1

---

**Story 6.5: Round Firewall Enforcement with Assertions**

As a validator,
I want round firewall enforcement via assertions,
So that post-round messages never mutate state (fail-fast on violations).

**Acceptance Criteria:**
1. Extend message processing with round firewall checks
2. Before processing any message: `assert message.round >= current_round` (not retroactive)
3. Late messages (round < current) logged but NEVER processed for state mutation
4. Assertion failure: halt execution, dump state, report violation
5. Round firewall test: deliberately send late message, verify assertion fires
6. Unit tests covering: current round accepted, late round rejected with assertion
7. Integration test: round firewall violations detected across full BA execution

**Prerequisites:** Story 2.7

---

**Story 6.6: Evidence Export for Analysis**

As a researcher,
I want to export evidence store to CSV/JSON for external analysis,
So that I can validate correctness claims and generate audit reports.

**Acceptance Criteria:**
1. Implement `export_evidence(format: str, output_path: str)` method
2. Export formats: CSV (tabular), JSON (structured)
3. Export includes: all barrier certificates, transition records, decision packages
4. CSV columns: round, evidence_type, data_summary, timestamp
5. JSON structure: nested hierarchy by round and evidence type
6. Export preserves cryptographic proofs (signatures as base64)
7. Unit tests covering: CSV export, JSON export, round-trip deserialization
8. Integration test: export after full BA execution, validate external loading

**Prerequisites:** Story 6.4

---

**Epic 6 Summary:**
- **6 stories** implementing validation and evidence infrastructure
- **Key milestone:** Complete audit trail enabling execution reconstruction
- **Critical for research:** Evidence store proves correctness claims with cryptographic proofs
- **Testing:** Round firewall enforcement prevents retroactive state contamination

---

## Epic 7: Classical Baseline Implementation (Weeks 13-14)

**Goal:** Implement minimal Perry-Toueg classical BA baseline demonstrating (t+1) round behavior for direct empirical comparison.

**Business Value:** Enables side-by-side comparison proving early-stopping achieves 2-5× fewer rounds than classical protocols—the core empirical claim.

**Technical Scope:**
- Minimal classical BA with (t+1) termination bound
- Shared transport layer and cryptographic infrastructure
- Experimental parity with early-stopping protocol
- Direct performance comparison under identical conditions

---

**Story 7.1: Classical BA Protocol Structure**

As a baseline implementer,
I want a simple classical BA protocol with (t+1) round bound,
So that I can compare against early-stopping protocol under identical conditions.

**Acceptance Criteria:**
1. Create `classical_ba.py` module with `ClassicalBA` class
2. Simpler structure than early-stopping: no GDA, simpler threshold logic
3. Classical termination: decision guaranteed by round t+1
4. Reuse existing infrastructure: Message schema, crypto, round scheduler
5. Protocol logic: reliable broadcast + decision after sufficient evidence
6. Unit tests covering: initialization, basic execution structure
7. Docstrings explaining classical (t+1) bound vs. early-stopping (1+ε)f

**Prerequisites:** Story 1.9

---

**Story 7.2: Classical Protocol Execution Logic**

As a classical BA,
I want deterministic execution with (t+1) worst-case termination,
So that I demonstrate classical behavior for baseline comparison.

**Acceptance Criteria:**
1. Implement `run_classical_ba(n: int, t: int, input_value: Any) -> Any` function
2. Protocol phases: PROPOSE → VOTE → DECIDE
3. PROPOSE phase: broadcast initial value
4. VOTE phase: collect proposals, determine majority or default
5. DECIDE phase: after t+1 rounds, decide based on accumulated votes
6. Worst-case termination: always decide by round t+1 regardless of faults
7. Unit tests covering: all phases, termination at t+1 rounds
8. Integration test: n=7, t=3 → decision at round 4 (t+1)

**Prerequisites:** Story 7.1

---

**Story 7.3: Baseline Experimental Parity**

As a researcher,
I want classical baseline using identical experimental conditions,
So that comparisons are fair (same n, t, f, Δ, adversaries).

**Acceptance Criteria:**
1. Classical BA uses same `RoundScheduler` with identical Δ
2. Classical BA uses same adversary framework (Equivocator, Withholder, Delay/Drop)
3. Classical BA uses same message acceptance pipeline
4. Classical BA uses same metrics collection (rounds, messages, crypto ops)
5. Configuration parity: run classical and early-stopping with identical parameters
6. Unit tests covering: shared infrastructure usage
7. Integration test: both protocols run on same (n, t, f) configuration, produce comparable metrics

**Prerequisites:** Stories 2.8, 5.6, 7.2

---

**Story 7.4: Classical Baseline Validation & Metrics**

As a researcher,
I want classical baseline producing metrics for direct comparison,
So that I can demonstrate early-stopping advantage empirically.

**Acceptance Criteria:**
1. Classical BA produces same metrics as early-stopping: rounds to decision, message count, crypto ops
2. Classical BA respects Byzantine Agreement properties (Agreement, Validity, Termination)
3. Property assertions applied to classical execution
4. Metrics export: CSV with classical baseline results
5. Integration test: classical terminates at t+1, early-stopping terminates earlier (when f ≪ t)
6. Comparison test: plot rounds vs. f for both protocols side-by-side
7. Validation: classical always ≥ early-stopping in round count (no false negatives)

**Prerequisites:** Story 7.3

---

**Epic 7 Summary:**
- **4 stories** implementing classical baseline
- **Key milestone:** Baseline operational for direct comparison
- **Critical for research:** Demonstrates 2-5× improvement empirically
- **Timeline:** Intentionally short (2 weeks) as baseline is simpler than early-stopping

---

## Epic 8: Experiment Infrastructure & Visualization (Weeks 15-18)

**Goal:** Build batch experiment harness, metrics collection, parameter sweeps, statistical analysis, and publication-quality visualization.

**Business Value:** Produces the experimental results answering all three research questions with publication-ready plots and statistical rigor.

**Technical Scope:**
- Parameterized batch execution over (n, t, f) configurations
- Metrics collection: rounds, messages, crypto operations
- CSV/Parquet export for analysis pipeline
- Statistical analysis with error bars
- Publication-quality matplotlib plots

---

**Story 8.1: Experiment Configuration Management**

As an experimenter,
I want YAML-based experiment configurations,
So that I can define parameter sweeps and adversary mixes declaratively.

**Acceptance Criteria:**
1. Create `experiment_config.py` module with config loading
2. YAML schema: network_sizes, fault_sweeps, adversary_configs, replication_count
3. Example config: n ∈ {7, 13, 25, 31}, f = 0..t, replications = 10
4. Config validation: ensure f ≤ t, n valid, Δ positive
5. `load_config(path: str) -> ExperimentConfig` function
6. Config includes: delay distributions, timeout bounds, random seeds
7. Unit tests covering: config loading, validation, default values
8. Example configs for common scenarios (no faults, low faults, max faults)

**Prerequisites:** Story 1.1

---

**Story 8.2: Batch Experiment Harness**

As an experimenter,
I want to run batched experiments over parameter configurations,
So that I can execute 500-1000 experimental runs systematically.

**Acceptance Criteria:**
1. Create `experiment_harness.py` module with `BatchRunner` class
2. `run_batch(config: ExperimentConfig) -> List[Results]` method
3. Iterate over: network sizes × fault levels × adversary mixes × replications
4. Each run: execute BA protocol, collect metrics, store results
5. Progress indicators: show completed runs / total runs
6. Resumable execution: save intermediate results, resume from checkpoint
7. Unit tests covering: batch iteration, progress tracking
8. Integration test: small batch (3 configs × 2 replications) completes successfully

**Prerequisites:** Story 8.1

---

**Story 8.3: Metrics Collection Pipeline**

As a metrics collector,
I want to track rounds, messages, and crypto operations per run,
So that I can analyze protocol performance quantitatively.

**Acceptance Criteria:**
1. Create `metrics.py` module with `MetricsCollector` class
2. Metrics tracked per run:
   - Rounds to decision
   - Total messages sent/received
   - Messages per node per round
   - Signature generation count
   - Signature verification count
   - Wall-clock execution time
3. `collect_metrics(ba_execution: Any) -> RunMetrics` method
4. Metrics validation: ensure counts are consistent (e.g., messages sent ≤ n² per round)
5. Unit tests covering: metric collection, validation
6. Integration test: full BA run produces complete metrics

**Prerequisites:** Story 4.8

---

**Story 8.4: CSV/Parquet Export for Analysis**

As an analyst,
I want experiment results exported to CSV or Parquet,
So that I can perform statistical analysis using pandas/R.

**Acceptance Criteria:**
1. Extend `BatchRunner` with export functionality
2. `export_results(format: str, output_path: str)` method
3. CSV columns: n, t, f, adversary_type, run_id, rounds, messages, crypto_ops, decision_value
4. Parquet format for large datasets (optional but recommended)
5. Export includes metadata: experiment date, config hash, protocol version
6. Round-trip test: export and re-import results successfully
7. Unit tests covering: CSV export, Parquet export (if implemented)
8. Integration test: batch execution exports results, pandas loads successfully

**Prerequisites:** Story 8.3

---

**Story 8.5: Statistical Analysis - Mean, StdDev, Confidence Intervals**

As a statistician,
I want statistical summaries with error bars,
So that I can report results with confidence intervals and variance measures.

**Acceptance Criteria:**
1. Create `statistics.py` module with analysis functions
2. `compute_statistics(results: List[RunMetrics]) -> Statistics` function
3. Statistics per configuration: mean, median, std_dev, min, max
4. Confidence intervals: 95% CI using standard error or bootstrap
5. Outlier detection: identify runs with anomalous metrics
6. Statistical significance testing: compare early-stopping vs. classical (t-test)
7. Unit tests covering: mean/stddev computation, CI calculation, significance tests
8. Integration test: batch results produce statistical summary

**Prerequisites:** Story 8.4

---

**Story 8.6: Publication-Quality Plots - Rounds vs. f**

As a researcher,
I want clean plots showing rounds to decision vs. fault count f,
So that I can visually demonstrate early-stopping advantage.

**Acceptance Criteria:**
1. Create `visualization.py` module with matplotlib plotting functions
2. `plot_rounds_vs_f(results: Statistics, output_path: str)` function
3. Line plot: x-axis = f (fault count), y-axis = rounds to decision
4. Multiple lines: early-stopping (experimental), classical baseline, theoretical (1+ε)f curve
5. Error bars: standard deviation or 95% CI
6. Plot styling: labeled axes, legend, title, grid
7. Export formats: PNG (raster), PDF (vector for publications)
8. Unit tests covering: plot generation (no crashes)
9. Integration test: produces publication-ready plot from real experimental data

**Prerequisites:** Story 8.5

---

**Story 8.7: Comparison Plots - Early-Stopping vs. Classical**

As a researcher,
I want side-by-side comparison plots,
So that I can demonstrate 2-5× round reduction visually.

**Acceptance Criteria:**
1. Extend visualization with comparison plotting
2. `plot_comparison(early_results, classical_results, output_path)` function
3. Comparison metrics: rounds, messages, crypto operations
4. Bar charts: early-stopping vs. classical side-by-side per (n, f) configuration
5. Percentage improvement annotation: "(X% fewer rounds)"
6. Color coding: early-stopping (green), classical (red)
7. Unit tests covering: comparison plot generation
8. Integration test: visual confirmation early-stopping < classical in low-fault regime

**Prerequisites:** Story 8.6

---

**Story 8.8: Complete Experimental Campaign Execution**

As a researcher,
I want to run complete experimental campaign answering all research questions,
So that I have thesis-ready empirical evidence.

**Acceptance Criteria:**
1. Full parameter sweep: n ∈ {7, 13, 25, 31}, f = 0..t, adversaries, replications
2. Early-stopping protocol executed across all configurations
3. Classical baseline executed across same configurations
4. Metrics collected, exported, analyzed statistically
5. Plots generated: rounds vs. f, comparison plots, crypto cost plots
6. Execution time: < 24 hours for full campaign (500-1000 runs)
7. Results validation: early-stopping ≤ classical in all cases, (1+ε)f bound empirically confirmed
8. Integration test: complete campaign produces all deliverables (CSVs, plots, statistical summaries)

**Prerequisites:** Stories 8.1-8.7

---

**Epic 8 Summary:**
- **8 stories** implementing complete experimental infrastructure
- **Key milestone:** Full experimental campaign produces publication-ready results
- **Critical deliverable:** Answers all three primary research questions with empirical evidence
- **Timeline:** Weeks 15-18 for implementation + execution + analysis
