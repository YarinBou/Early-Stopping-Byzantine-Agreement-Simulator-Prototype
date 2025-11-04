# Non-Functional Requirements

## Correctness (Highest Priority - Non-Negotiable)

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

## Reproducibility (Critical for Research Validity)

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

## Performance Measurement (Not Optimization)

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

## Code Quality & Maintainability

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

## Documentation & Educational Value

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

## Usability (For Researchers)

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

## Reliability & Robustness

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

## Research Ethics & Integrity

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

## Performance Acceptance Criteria

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
