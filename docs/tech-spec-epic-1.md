# Epic Technical Specification: Foundation Infrastructure

Date: 2025-11-04
Author: Yarin
Epic ID: 1
Status: Draft

---

## Overview

Epic 1 establishes the foundational transport layer and message handling infrastructure for the Early-Stopping Byzantine Agreement simulator. This epic creates the bedrock upon which all protocol implementations (CoD, GDA, PoP) and the BA controller will be built. The foundation provides cryptographically authenticated message transport with strict validation, deterministic serialization for reproducibility, and comprehensive acceptance rules preventing Byzantine attacks through replay, forgery, or schema violations.

This epic directly supports the core research goal of proving correctness under adversarial conditions by ensuring every message entering the protocol stack is authenticated, validated, and bound to specific rounds. Without this foundation, no Byzantine Agreement property (Agreement, Validity, Termination) can be reliably validated.

## Objectives and Scope

**In Scope:**
- Canonical message schema `(ssid, round, protocol_id, phase, sender_id, value|digest, aux, signature)` with strict type enforcement
- Ed25519 cryptographic signing and verification using PyNaCl
- Deterministic JSON serialization with canonical key ordering (sort_keys=True) for reproducible hashing
- Message acceptance pipeline integrating: schema validation, signature verification, round binding (anti-replay), and deduplication
- Project structure following src/ layout with version-locked dependencies (requirements.txt)
- Base64 encoding for binary fields (signatures, digests) ensuring JSON compatibility
- Comprehensive unit test coverage (>80% target) for all message handling components

**Out of Scope:**
- CBOR serialization (deferred to Phase 2; abstraction layer provided for future migration)
- Message compression or wire protocol optimization
- Multi-process or distributed message delivery (single-process asyncio simulation sufficient for MVP)
- Real network transport (simulated delivery via centralized scheduler)
- Message batching or pipelining optimizations
- Interactive debugging tools or message inspection GUIs

## System Architecture Alignment

Epic 1 aligns with the architecture's **transport/** module as defined in the Complete Project Structure (architecture.md). The epic implements:

- **src/ba_simulator/transport/message.py**: Message dataclass with all canonical fields (Story 1.2)
- **src/ba_simulator/transport/serialization.py**: MessageSerializer interface with JSON implementation (Story 1.3)
- **src/ba_simulator/transport/crypto.py**: NodeKeys class for Ed25519 signing/verification (Story 1.4)
- **src/ba_simulator/transport/validation.py**: MessageValidator with acceptance pipeline (Stories 1.6-1.9)

**Architectural Constraints Satisfied:**
- **Naming Patterns**: snake_case modules, PascalCase classes, exact field names from PRD
- **Structure Patterns**: 3-group imports (stdlib, third-party, local), dataclass-based data models
- **Format Patterns**: JSON with sort_keys=True, base64 for binary fields
- **Security Architecture**: Ed25519 authentication preventing forgery, round binding preventing replay attacks
- **Data Architecture**: Message dataclass matches specification exactly, no schema deviation

This epic enables Epic 2 (Round Scheduler) by providing validated, authenticated messages. All subsequent protocol implementations (Epic 3+) depend on this transport layer for message handling.

## Detailed Design

### Services and Modules

| Module | Responsibility | Inputs | Outputs | Owner Story |
|--------|---------------|--------|---------|-------------|
| **message.py** | Define canonical message schema with strict type enforcement | Field values (ssid, round, protocol_id, etc.) | Message dataclass instances | Story 1.2 |
| **serialization.py** | Deterministic message serialization for cryptographic hashing | Message objects | Serialized bytes (JSON), deserialized Message objects | Story 1.3 |
| **crypto.py** | Ed25519 key pair management and cryptographic operations | Signing keys, payloads, signatures | Generated signatures, verification results (bool) | Story 1.4 |
| **validation.py** | Message acceptance pipeline enforcing all validation rules | Messages, verify keys, current round | Acceptance decision (bool), rejection reasons | Stories 1.6-1.9 |
| **Project Structure** | Standard Python project layout with dependencies | N/A | Initialized project, requirements.txt, README.md | Story 1.1 |

**Module Dependencies:**
- `message.py` is foundational (no internal dependencies)
- `serialization.py` depends on `message.py`
- `crypto.py` is independent (only PyNaCl dependency)
- `validation.py` depends on `message.py` and `crypto.py`
- Integration point: `validation.py` provides unified acceptance pipeline used by Epic 2 (RoundScheduler)

### Data Models and Contracts

**Primary Data Model: Message**

```python
@dataclass
class Message:
    """Canonical Byzantine Agreement message schema.

    All protocol messages follow this exact structure for consistency
    and cryptographic authentication.
    """
    ssid: str           # Session identifier (experiment/run ID)
    round: int          # Protocol round number (≥ 0)
    protocol_id: str    # Subprotocol identifier ("CoD", "GDA", "PoP")
    phase: str          # Protocol phase ("SEND", "ECHO", "READY", etc.)
    sender_id: int      # Node identifier (0 ≤ sender_id < n)
    value: Any          # Protocol-specific payload (values, proposals)
    digest: Optional[bytes]  # Optional cryptographic digest
    aux: Dict[str, Any]      # Auxiliary data (participation digests, metadata)
    signature: bytes         # Ed25519 signature (64 bytes)

    def signing_payload(self) -> bytes:
        """Returns canonical bytes for signing (excludes signature field)."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Converts to dictionary for serialization."""
        ...

    def verify_signature(self, verify_key: VerifyKey) -> bool:
        """Verifies signature against provided public key."""
        ...
```

**Supporting Data Models:**

```python
@dataclass
class NodeKeys:
    """Ed25519 key pair for node authentication."""
    signing_key: SigningKey    # Private key (32 bytes)
    verify_key: VerifyKey       # Public key (32 bytes)
    node_id: int                # Associated node identifier

    @staticmethod
    def generate() -> NodeKeys:
        """Generates fresh Ed25519 key pair."""
        ...

    def sign(self, payload: bytes) -> bytes:
        """Signs payload, returns 64-byte signature."""
        ...

    @staticmethod
    def verify(payload: bytes, signature: bytes, verify_key: VerifyKey) -> bool:
        """Verifies signature against public key."""
        ...
```

**Field Constraints:**
- `ssid`: Non-empty string, typically experiment configuration hash
- `round`: Non-negative integer, monotonically increasing
- `protocol_id`: One of {"CoD", "GDA", "PoP", "BA"} (extensible)
- `phase`: Protocol-specific, must be non-empty
- `sender_id`: Valid node ID in range [0, n)
- `value`: Any JSON-serializable type
- `digest`: SHA-256 hash (32 bytes) when present
- `aux`: Dictionary, keys are strings
- `signature`: Exactly 64 bytes (Ed25519 signature length)

**Invariants:**
- Every message MUST have a valid signature
- Messages with round < current_round are "late" (audit only, no state mutation)
- Deduplication key: `(sender_id, round, protocol_id, phase)` must be unique per sender
- Signatures must verify against sender's public key before message acceptance

### APIs and Interfaces

**MessageSerializer Interface** (Story 1.3)

```python
class MessageSerializer(ABC):
    """Abstract interface for message serialization.

    Enables future migration from JSON to CBOR without modifying protocol code.
    """

    @abstractmethod
    def encode(self, message: Message) -> bytes:
        """Serializes message to bytes with deterministic ordering."""
        pass

    @abstractmethod
    def decode(self, data: bytes) -> Message:
        """Deserializes bytes to Message object."""
        pass


class JSONMessageSerializer(MessageSerializer):
    """JSON implementation with canonical key ordering."""

    def encode(self, message: Message) -> bytes:
        """Uses json.dumps with sort_keys=True, base64 for binary fields."""
        ...

    def decode(self, data: bytes) -> Message:
        """Parses JSON, decodes base64 binary fields."""
        ...
```

**MessageValidator Interface** (Stories 1.6-1.9)

```python
class MessageValidator:
    """Unified message acceptance pipeline enforcing all validation rules."""

    def __init__(self, n: int, verify_keys: Dict[int, VerifyKey]):
        """Initialize validator with network size and node public keys."""
        self.n = n
        self.verify_keys = verify_keys
        self.current_round = 0
        self.seen_messages: Set[Tuple[int, int, str, str]] = set()

    def accept_message(self, message: Message) -> bool:
        """Full acceptance pipeline: schema → signature → round → dedup.

        Returns True if message accepted, False otherwise.
        Logs rejection reasons at appropriate levels.
        """
        ...

    def validate_schema(self, message: Message) -> bool:
        """Checks field presence, types, and constraints."""
        ...

    def verify_signature(self, message: Message) -> bool:
        """Verifies Ed25519 signature against sender's public key."""
        ...

    def check_round_binding(self, message: Message) -> bool:
        """Ensures message.round is valid relative to current_round."""
        ...

    def is_duplicate(self, message: Message) -> bool:
        """Checks if (sender_id, round, protocol_id, phase) already seen."""
        ...

    def set_current_round(self, round: int):
        """Updates current round for round binding checks."""
        ...
```

**NodeKeys Interface** (Story 1.4)

```python
class NodeKeys:
    """Ed25519 cryptographic key pair for node authentication."""

    @staticmethod
    def generate(node_id: int) -> NodeKeys:
        """Generates fresh Ed25519 key pair for given node."""
        ...

    def sign(self, payload: bytes) -> bytes:
        """Signs payload using private key, returns 64-byte signature."""
        ...

    @staticmethod
    def verify(payload: bytes, signature: bytes, verify_key: VerifyKey) -> bool:
        """Verifies signature using public key. Returns False for invalid."""
        ...
```

**Integration Points:**
- **Epic 2 (RoundScheduler)** calls `MessageValidator.accept_message()` before delivering messages to protocol FSMs
- **Epic 3 (Protocol FSMs)** receive only validated messages, can assume schema correctness and signature validity
- **Epic 5 (Adversaries)** may generate messages with conflicting signatures (Equivocator), but validation detects this

### Workflows and Sequencing

**Message Creation and Signing Workflow**

```
1. Protocol FSM generates message content
   ↓
2. Create Message object with all fields (signature initially empty)
   ↓
3. Compute signing_payload() → canonical bytes (excludes signature)
   ↓
4. Sign payload using NodeKeys.sign() → 64-byte signature
   ↓
5. Populate message.signature field
   ↓
6. Message ready for transmission
```

**Message Acceptance Workflow** (Story 1.9)

```
Incoming Message
   ↓
1. Schema Validation (Story 1.6)
   - Check all required fields present
   - Validate field types and constraints
   - Ensure sender_id ∈ [0, n)
   └─ REJECT if invalid → Log "schema_validation_failed"
   ↓
2. Signature Verification (Story 1.5)
   - Extract sender's public key from verify_keys
   - Compute message.signing_payload()
   - Verify signature using NodeKeys.verify()
   └─ REJECT if invalid → Log "signature_verification_failed"
   ↓
3. Round Binding Check (Story 1.8)
   - Compare message.round to current_round
   - Reject if message.round < current_round (too old)
   - Optional: reject if message.round > current_round + 1 (too far ahead)
   └─ REJECT if invalid → Log "round_binding_violation"
   ↓
4. Deduplication Check (Story 1.7)
   - Extract key: (sender_id, round, protocol_id, phase)
   - Check if key in seen_messages set
   - If first occurrence: add to set, continue
   └─ REJECT if duplicate → Log "duplicate_message"
   ↓
5. ACCEPT ✓
   └─ Message delivered to protocol FSM for processing
```

**Serialization Round-Trip Workflow**

```
Message Object
   ↓
1. Call serializer.encode(message)
   - Convert to dict via message.to_dict()
   - Encode binary fields (signature, digest) to base64
   - JSON stringify with sort_keys=True
   ↓
2. Bytes (deterministic, hashable)
   ↓
3. (Optional: transmit, store, hash)
   ↓
4. Call serializer.decode(bytes)
   - JSON parse
   - Decode base64 fields back to bytes
   - Reconstruct Message object
   ↓
5. Message Object (identical to original)
```

**Sequencing Notes:**
- Message acceptance is a strict sequential pipeline (short-circuit on first failure)
- Signature verification happens early (expensive operation, but prevents processing of forged messages)
- Deduplication happens last (after all validity checks, avoids polluting seen set with invalid messages)
- Round binding prevents replay attacks by tying messages to specific rounds

## Non-Functional Requirements

### Performance

**Performance Targets (Aligned with NFR-3.2: Measurement, Not Optimization)**

- **Message Acceptance Latency**: < 5ms per message including signature verification (Story 1.9)
- **Schema Validation**: < 1ms per message (Story 1.6)
- **Signature Generation**: ~0.5ms per message (Ed25519 standard performance)
- **Signature Verification**: ~1-2ms per message (Ed25519 standard performance)
- **Serialization Round-Trip**: < 2ms for typical message (JSON encoding + decoding)

**Acceptable Overhead:**
- Detailed logging enabled throughout (research priority over execution speed per NFR-3.2)
- No premature optimization (correctness first, performance second)
- Instrumentation overhead acceptable for n ≤ 31 networks

**Performance Validation:**
- Unit tests confirm validation completes within target latencies
- Integration test: Process 100 messages in < 500ms (5ms avg per message)
- No performance regression testing required for MVP (defer to Phase 2)

### Security

**Cryptographic Authentication (FR-1.2, NFR-1.1)**

- **Algorithm**: Ed25519 via PyNaCl (NIST standard, 128-bit security level)
- **Key Size**: 256-bit private keys, 256-bit public keys
- **Signature Size**: 64 bytes per message
- **Hash Function**: SHA-256 for all digest computations (signing payloads, participation digests)

**Security Guarantees:**
1. **Message Authentication**: Invalid signatures rejected → prevents forgery (no node can impersonate another)
2. **Anti-Replay Protection**: Round binding ensures old messages cannot be replayed in future rounds
3. **Non-Repudiation**: Signed messages provide cryptographic proof of origin
4. **Integrity**: Any message modification invalidates signature, detected during verification

**Threat Model Coverage (Epic 1 Scope):**
- ✓ **Forgery Prevention**: Ed25519 signatures prevent unsigned messages or impersonation
- ✓ **Replay Attack Prevention**: Round binding rejects messages from old rounds
- ✓ **Tampering Detection**: Signature verification catches any message modification
- ⚠ **Byzantine Behavior Detection**: Equivocation detection implemented in Epic 3 (CoD protocol), not Epic 1
- ⚠ **Denial of Service**: Rate limiting and adversary composition managed in Epic 5

**Key Management:**
- Fresh key pairs generated per node per experimental run
- Private keys never leave NodeKeys class (encapsulation)
- Public keys distributed to all nodes at initialization (verified via verify_keys dict)
- No key rotation required for MVP (single-run simulation)

**Security Validation:**
- Unit test: Invalid signatures rejected (Story 1.5)
- Unit test: Message tampering detected (modify value, signature fails)
- Integration test: Adversary-generated messages with wrong keys rejected

### Reliability/Availability

**Error Handling Strategy (Aligned with ADR-009: Hybrid Error Handling)**

**Fail-Fast (Correctness Violations):**
- Schema validation failures → return False, log at DEBUG level (expected Byzantine behavior)
- Missing required fields → raise ValueError immediately (programmer error)
- Signature verification failure → return False, log at WARN level (potential attack)
- Type constraint violations → raise TypeError (programmer error, should never occur with proper Message construction)

**Graceful Handling (Expected Byzantine Behavior):**
- Invalid signatures → reject message, increment rejection counter, continue processing
- Duplicate messages → ignore silently (log at DEBUG), normal operation
- Round binding violations → reject message, log for audit, continue
- Malformed JSON during deserialization → raise exception with helpful error message

**Input Validation:**
- All Message fields validated in `__post_init__` (enforce non-null for required fields)
- MessageValidator checks sender_id ∈ [0, n) before processing
- Round numbers validated as non-negative integers
- Signature length validated (exactly 64 bytes for Ed25519)

**Resilience Patterns:**
- No single invalid message crashes the system
- Rejection statistics tracked for debugging (accepted_count, rejected_by_reason)
- Validation pipeline designed to handle malicious input gracefully
- Clear separation: Byzantine behavior (expected, logged) vs. programmer errors (fail-fast)

**Availability:**
- Message validation is stateless (no external dependencies beyond verify_keys)
- No network calls or I/O during validation (pure in-memory operations)
- Validation failures do not corrupt validator state
- Deduplication set can be cleared per round (memory management)

### Observability

**Structured Logging (Aligned with ADR-008: structlog for JSON Logs)**

All Epic 1 components use structured logging for machine-parseable audit trails:

**Log Events:**
- `message_created`: When new Message object instantiated (fields: ssid, round, protocol_id, phase, sender_id)
- `message_signed`: After signature generated (fields: sender_id, signature_length)
- `message_serialized`: After encoding to bytes (fields: message_id, byte_length)
- `message_deserialized`: After decoding from bytes (fields: message_id, success)
- `validation_started`: Before acceptance pipeline (fields: message_id, current_round)
- `schema_validation_failed`: Schema check failed (fields: message_id, failure_reason)
- `signature_verification_failed`: Invalid signature (fields: sender_id, message_id)
- `round_binding_violation`: Message round invalid (fields: message_round, current_round)
- `duplicate_message`: Deduplication detected (fields: dedup_key)
- `message_accepted`: Passed all validation (fields: message_id, acceptance_time)
- `message_rejected`: Failed validation (fields: message_id, rejection_reason, rejection_stage)

**Metrics Tracked:**
- `messages_created_total`: Count of Message objects created
- `messages_signed_total`: Count of signatures generated
- `messages_accepted_total`: Count passing acceptance pipeline
- `messages_rejected_total`: Count failing acceptance (by reason: schema, signature, round, duplicate)
- `signature_verification_duration_ms`: Distribution of verification latencies
- `serialization_round_trip_duration_ms`: Encode + decode timing

**Log Levels:**
- DEBUG: Duplicate messages, normal rejections (expected during Byzantine behavior)
- INFO: Message acceptance, validation statistics
- WARN: Signature verification failures (potential attacks)
- ERROR: Programmer errors (missing fields, type violations)

**Tracing:**
- Each message assigned unique `message_id` (hash of ssid + round + sender + protocol + phase)
- Message ID included in all log events for traceability
- Structured logs enable querying: "Show all rejections for sender_id=5 in round 10"

**Observability Validation:**
- Unit test: Logs produced at appropriate levels for each validation outcome
- Integration test: Parse structured logs as JSON, verify all expected fields present

## Dependencies and Integrations

**External Dependencies (requirements.txt)**

```txt
# Core Dependencies (Version-Locked per NFR-2.3)
PyNaCl==1.5.0           # Ed25519 cryptographic signatures
pytest==7.4.3           # Unit testing framework
pytest-cov==4.1.0       # Test coverage reporting
structlog==23.2.0       # Structured logging

# Optional Development Dependencies
black==23.12.1          # Code formatting
flake8==6.1.0          # Linting
mypy==1.7.1            # Type checking

# Future Dependencies (Epic 8)
pandas>=2.1.0          # Data analysis (deferred to Epic 8)
matplotlib>=3.8.0      # Visualization (deferred to Epic 8)
```

**Dependency Rationale:**
- **PyNaCl**: Industry-standard Ed25519 implementation, NIST-approved cryptography
- **pytest**: De-facto standard for Python testing, excellent plugin ecosystem
- **structlog**: Machine-parseable JSON logs for research analysis
- **black/flake8/mypy**: Code quality tools (optional but recommended per architecture)

**Internal Module Dependencies:**

```
Story 1.1 (Project Structure)
   ├─→ Story 1.2 (Message Schema) - foundational dataclass
   ├─→ Story 1.3 (Serialization) - depends on Message
   ├─→ Story 1.4 (Crypto) - independent PyNaCl wrapper
   └─→ Story 1.5 (Signing Integration) - depends on Stories 1.2, 1.3, 1.4

Story 1.6 (Schema Validation) - depends on Story 1.2
Story 1.7 (Deduplication) - depends on Story 1.6
Story 1.8 (Round Binding) - depends on Story 1.7
Story 1.9 (Acceptance Pipeline) - depends on Stories 1.5, 1.6, 1.7, 1.8
```

**Integration Points with Other Epics:**

**Epic 2 (Round Scheduler) - PRIMARY CONSUMER**
- RoundScheduler calls `MessageValidator.accept_message()` before delivery
- RoundScheduler uses `Message` dataclass for all message handling
- Round binding (Story 1.8) synchronizes with RoundScheduler's current round tracking

**Epic 3 (Protocol FSMs)**
- CoD, GDA, PoP protocols receive pre-validated messages (assume schema correctness)
- Protocols create new messages using `Message` dataclass
- Protocols sign messages using `NodeKeys.sign()` before broadcasting

**Epic 5 (Adversary Framework)**
- Adversaries create malformed messages to test validation robustness
- Equivocator generates conflicting messages with valid signatures (different values, same phase)
- Validation rejects forged signatures from adversaries using wrong keys

**Epic 6 (Evidence Store)**
- Evidence store records barrier certificates (n-t signed messages)
- Uses `Message.signature` and `Message.digest` for cryptographic proofs
- Relies on signature verification for independent third-party validation

**No External Service Dependencies:**
- All validation is local, in-memory (no network calls)
- No database or persistent storage required (Epic 1 scope)
- No external APIs or microservices

## Acceptance Criteria (Authoritative)

**Epic-Level Acceptance Criteria (All Stories Complete):**

1. **AC-1.1**: Project structure follows src/ layout with `src/ba_simulator/transport/` module containing `message.py`, `serialization.py`, `crypto.py`, `validation.py`

2. **AC-1.2**: `requirements.txt` exists with version-locked dependencies (PyNaCl==1.5.0, pytest==7.4.3, structlog==23.2.0)

3. **AC-1.3**: Message dataclass implements exact schema `(ssid, round, protocol_id, phase, sender_id, value, digest, aux, signature)` with strict type hints

4. **AC-1.4**: JSON serialization produces deterministic output (identical messages → identical bytes) using `sort_keys=True`

5. **AC-1.5**: Ed25519 signing and verification operational via PyNaCl with 64-byte signatures

6. **AC-1.6**: Message acceptance pipeline integrates: schema validation → signature verification → round binding → deduplication (Stories 1.6-1.9)

7. **AC-1.7**: Invalid signatures rejected with `False` return value and appropriate logging (no exceptions for normal Byzantine behavior)

8. **AC-1.8**: Round binding prevents replay attacks: messages with `round < current_round` rejected

9. **AC-1.9**: Duplicate messages (same `(sender_id, round, protocol_id, phase)`) detected and rejected

10. **AC-1.10**: Unit test coverage ≥ 80% for all transport modules

11. **AC-1.11**: Integration test: Create message → sign → serialize → deserialize → verify → accept (full round-trip succeeds)

12. **AC-1.12**: Performance test: Process 100 messages in < 500ms (5ms avg acceptance latency including signature verification)

13. **AC-1.13**: README.md exists with setup instructions (virtualenv creation, `pip install -r requirements.txt`, `pytest`)

14. **AC-1.14**: All modules follow architectural naming patterns (snake_case files, PascalCase classes, exact field names from PRD)

15. **AC-1.15**: Structured logging produces machine-parseable JSON logs for all validation events

**Story-Specific Acceptance Criteria (Extracted from Epic Details):**

See Epic 1 stories in epics/epic-details.md for detailed per-story acceptance criteria. Each story's AC must be satisfied for epic completion.

## Traceability Mapping

| Acceptance Criteria | Tech Spec Section | Component/Module | Test Idea |
|---------------------|-------------------|------------------|-----------|
| AC-1.1 (Project Structure) | System Architecture Alignment | src/ba_simulator/transport/ | Verify directory structure exists with expected files |
| AC-1.2 (Dependencies) | Dependencies and Integrations | requirements.txt | Parse requirements.txt, verify exact versions present |
| AC-1.3 (Message Schema) | Data Models - Message dataclass | message.py | Unit test: instantiate Message with all fields, verify types |
| AC-1.4 (Deterministic Serialization) | APIs - MessageSerializer | serialization.py | Unit test: serialize same message twice, assert bytes identical |
| AC-1.5 (Ed25519 Crypto) | APIs - NodeKeys | crypto.py | Unit test: generate keys, sign payload, verify signature succeeds |
| AC-1.6 (Acceptance Pipeline) | APIs - MessageValidator | validation.py | Unit test: valid message passes all stages, returns True |
| AC-1.7 (Invalid Signatures) | Security - Signature Verification | validation.py | Unit test: wrong signature → accept_message() returns False |
| AC-1.8 (Round Binding) | Security - Anti-Replay | validation.py | Unit test: message.round < current_round → rejected |
| AC-1.9 (Deduplication) | Workflows - Message Acceptance | validation.py | Unit test: send same message twice, second rejected as duplicate |
| AC-1.10 (Test Coverage) | Test Strategy | tests/unit/test_transport/ | Run pytest-cov, verify ≥80% coverage on transport modules |
| AC-1.11 (Integration Test) | Workflows - Round-Trip | tests/integration/ | Integration test: full message lifecycle end-to-end |
| AC-1.12 (Performance) | NFR - Performance | validation.py | Performance test: measure acceptance latency for 100 messages |
| AC-1.13 (README) | Dependencies - Setup | README.md | Manual verification: follow README instructions, project runs |
| AC-1.14 (Naming Patterns) | System Architecture Alignment | All modules | Code review: verify snake_case, PascalCase conventions |
| AC-1.15 (Structured Logging) | NFR - Observability | All modules | Unit test: parse logs as JSON, verify expected fields present |

**PRD Requirements Traceability:**

| PRD Functional Requirement | Epic 1 Coverage | Implementation |
|-----------------------------|-----------------|----------------|
| FR-1.1 (Canonical Message Schema) | ✓ Full | Message dataclass (Story 1.2) |
| FR-1.2 (Message Authentication) | ✓ Full | NodeKeys crypto (Stories 1.4, 1.5) |
| FR-1.3 (Message Acceptance Rules) | ✓ Full | MessageValidator pipeline (Stories 1.6-1.9) |
| FR-1.4 (Message Delivery Scheduling) | ⚠ Partial | Deferred to Epic 2 (RoundScheduler) |
| FR-7.1 (Technology Stack - Python 3.10+) | ✓ Full | Project structure (Story 1.1) |

**Architecture Decision Traceability:**

| ADR | Epic 1 Implementation |
|-----|----------------------|
| ADR-001 (src/ layout) | Story 1.1 project structure |
| ADR-002 (pip + requirements.txt) | Story 1.1 dependency management |
| ADR-005 (Serializer abstraction) | Story 1.3 MessageSerializer interface |
| ADR-008 (structlog) | Observability section, all modules |
| ADR-009 (Hybrid error handling) | Reliability section, validation.py |
| ADR-012 (Dataclasses) | Story 1.2 Message dataclass, Story 1.4 NodeKeys |

## Risks, Assumptions, Open Questions

**RISK-1.1: Ed25519 Signature Performance**
- **Type**: Risk
- **Description**: Signature verification may be slower than 5ms target on some hardware, affecting overall message acceptance latency
- **Likelihood**: Low (Ed25519 is typically <2ms even on modest hardware)
- **Impact**: Medium (would increase round execution time)
- **Mitigation**: Benchmark early on target hardware; Ed25519 chosen specifically for performance; if needed, batch verification can be added in Phase 2
- **Owner**: Story 1.4, 1.5

**RISK-1.2: JSON Serialization Overhead**
- **Type**: Risk
- **Description**: JSON with base64 encoding may introduce unexpected overhead compared to binary formats
- **Likelihood**: Low (JSON is well-optimized in Python standard library)
- **Impact**: Low (acceptable per NFR-3.2 measurement focus)
- **Mitigation**: Abstraction layer (MessageSerializer interface) enables CBOR migration if needed; overhead acceptable for MVP
- **Owner**: Story 1.3

**ASSUMPTION-1.1: Single-Process Simulation**
- **Type**: Assumption
- **Description**: All message validation happens in single Python process with shared memory (no distributed validation)
- **Rationale**: Simplifies MVP, sufficient for n ≤ 31 networks per architecture
- **Impact**: No network serialization overhead, deterministic execution easier
- **Validation**: Architecture document confirms single-process simulation for MVP

**ASSUMPTION-1.2: Pre-Distributed Public Keys**
- **Type**: Assumption
- **Description**: All nodes receive `verify_keys` dictionary at initialization (no key exchange protocol)
- **Rationale**: Simplifies MVP, realistic for controlled experimental environments
- **Impact**: Reduces implementation complexity, no PKI required
- **Validation**: Common pattern in BA research implementations

**ASSUMPTION-1.3: No Message Compression Required**
- **Type**: Assumption
- **Description**: JSON message size acceptable without compression for research validation
- **Rationale**: Network bandwidth not a bottleneck in single-process simulation
- **Impact**: Simpler implementation, easier debugging with human-readable messages
- **Validation**: Message sizes estimated <1KB, acceptable for n ≤ 31

**QUESTION-1.1: Deduplication Memory Management**
- **Type**: Open Question
- **Description**: How long should `seen_messages` set be retained? Clear per round or accumulate?
- **Options**: (a) Clear after each round advancement (Epic 2 integration), (b) Retain for entire run, (c) LRU cache with size limit
- **Recommendation**: Start with (a) clear per round, simplest and sufficient for MVP
- **Resolution Needed By**: Story 1.7 implementation
- **Decision Owner**: Developer implementing Story 1.7, review with SM

**QUESTION-1.2: Round Binding Future Messages**
- **Type**: Open Question
- **Description**: Should messages with `round > current_round + 1` be rejected or buffered?
- **Options**: (a) Reject entirely, (b) Buffer for future delivery, (c) Accept with warning
- **Recommendation**: Start with (a) reject, simpler; round progression is lock-step so future messages indicate timing bugs
- **Resolution Needed By**: Story 1.8 implementation
- **Decision Owner**: Developer implementing Story 1.8, review with SM

**QUESTION-1.3: Test Coverage Target**
- **Type**: Open Question
- **Description**: Is 80% coverage sufficient or should we target higher (90%+)?
- **Current Target**: 80% per AC-1.10
- **Consideration**: Higher coverage catches more edge cases but increases test maintenance
- **Recommendation**: Start with 80%, increase if correctness issues found during integration
- **Resolution Needed By**: Story 1.9 (final epic story)
- **Decision Owner**: SM/Developer consensus

## Test Strategy Summary

**Test Pyramid for Epic 1**

```
                    ┌─────────────────┐
                    │  Integration    │  (2-3 tests)
                    │   Full Pipeline │
                    └─────────────────┘
                  ┌─────────────────────┐
                  │   Component Tests   │  (10-15 tests)
                  │  (Acceptance, Crypto)│
                  └─────────────────────┘
              ┌───────────────────────────┐
              │      Unit Tests           │  (40-50 tests)
              │ (Message, Serializer,     │
              │  Validator individual fns)│
              └───────────────────────────┘
```

**Unit Tests (40-50 tests, >80% coverage target)**

- **Story 1.2 (Message Schema)**:
  - Test valid Message creation with all fields
  - Test field type validation (round must be int, sender_id must be int, etc.)
  - Test `signing_payload()` excludes signature field
  - Test `to_dict()` conversion

- **Story 1.3 (Serialization)**:
  - Test encode produces deterministic bytes (same message → same output)
  - Test round-trip: decode(encode(msg)) == msg
  - Test base64 encoding for binary fields (signature, digest)
  - Test malformed JSON handling (raises appropriate exception)

- **Story 1.4 (Crypto)**:
  - Test key generation produces valid Ed25519 keys
  - Test signing produces 64-byte signatures
  - Test verification succeeds with correct key
  - Test verification fails with wrong key
  - Test deterministic signatures (same payload → same signature with same key)

- **Story 1.6 (Schema Validation)**:
  - Test valid message passes validation
  - Test missing field rejected
  - Test invalid sender_id (< 0 or >= n) rejected
  - Test negative round number rejected
  - Test invalid signature length rejected

- **Story 1.7 (Deduplication)**:
  - Test first message accepted
  - Test exact duplicate rejected
  - Test different phase accepted (same sender, round, protocol)
  - Test different round accepted (same sender, protocol, phase)

- **Story 1.8 (Round Binding)**:
  - Test current round message accepted
  - Test old round (round < current) rejected
  - Test future round handling (per QUESTION-1.2 resolution)

- **Story 1.9 (Acceptance Pipeline)**:
  - Test fully valid message accepted (returns True)
  - Test schema failure rejected at stage 1
  - Test signature failure rejected at stage 2
  - Test round binding failure rejected at stage 3
  - Test duplicate rejected at stage 4

**Component Tests (10-15 tests)**

- **Message Signing Integration**:
  - Create message → sign with NodeKeys → verify signature succeeds
  - Create message → sign → tamper with value → verify fails

- **Serialization + Crypto**:
  - Serialize message → hash bytes → deterministic digest
  - Serialize signed message → deserialize → signature still valid

- **Acceptance Pipeline Integration**:
  - Valid message passes all stages
  - Invalid signature rejected with appropriate log message
  - Duplicate message rejected on second attempt
  - Late message (old round) rejected with round_binding_violation log

**Integration Tests (2-3 tests)**

- **Full Message Lifecycle**:
  - Create Message object
  - Sign with NodeKeys
  - Serialize to JSON bytes
  - Deserialize back to Message
  - Verify signature
  - Accept through MessageValidator
  - Assert: accepted == True

- **Adversarial Message Rejection**:
  - Create message with wrong sender's key
  - Attempt acceptance
  - Assert: rejected with signature_verification_failed

- **Performance Validation**:
  - Process 100 messages through acceptance pipeline
  - Measure total time
  - Assert: total_time < 500ms (5ms avg per message)

**Test Coverage Goals**

- **Target**: ≥80% line coverage for all transport modules
- **Critical Paths**: 100% coverage on acceptance pipeline (security-critical)
- **Measurement**: `pytest --cov=src/ba_simulator/transport --cov-report=term-missing`
- **Exclusions**: Logging statements, type checking code, `__repr__` methods (low risk)

**Test Data Strategy**

- **Valid Test Messages**: 5-10 fixtures covering different protocol_ids, phases, values
- **Invalid Test Cases**: Missing fields, wrong types, invalid signatures, old rounds
- **Key Pairs**: Generate fresh keys per test (deterministic with seeded RNG)
- **Round Progression**: Test with current_round = 0, 5, 10, 100 (various round states)

**Regression Prevention**

- All tests run on every commit (CI integration ready)
- Property-based testing (optional): Use `hypothesis` to generate random valid messages
- Mutation testing (optional): Use `mutmut` to verify tests catch code changes

**Testing Timeline**

- Unit tests developed alongside implementation (TDD encouraged)
- Component tests added after Stories 1.5, 1.9
- Integration tests added at epic completion
- Performance test validates AC-1.12 before epic sign-off
