# Security Architecture

## Cryptographic Guarantees

**Message Authentication:** Ed25519 signatures on all messages
- **Algorithm:** Ed25519 via PyNaCl
- **Key size:** 256-bit
- **Signature size:** 64 bytes
- **Verification:** All messages validated before acceptance

**Digest Computation:** SHA-256 for all hashes
- Participation digests
- Carryover digests
- Certificate digests

**Anti-Replay:** Round binding prevents message replay
- Messages bound to specific rounds
- Round firewall rejects retroactive messages

## Byzantine Fault Tolerance

**Fault model:** Authenticated Byzantine (t < n/2)
- Up to t nodes can behave arbitrarily
- All messages are signed (no impersonation)
- Synchronous model with known Δ

**Safety properties:**
- **Agreement:** No two honest nodes decide differently
- **Validity:** Unanimous honest input implies that value decided
- **Assertion enforcement:** Property violations crash immediately

**Adversary resilience:**
- Equivocation detected by CoD
- Withholder forces timeout advancement (liveness preserved)
- Delay/Drop within Δ bounds

---
