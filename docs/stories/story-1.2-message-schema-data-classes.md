# Story 1.2: Message Schema Data Classes

**Epic:** Epic 1
**Week:** Weeks TBD

## User Story

As a protocol developer,
I want canonical message data structures with strict type enforcement,
So that all protocol messages follow the schema: `(ssid, round, protocol_id, phase, sender_id, value|digest, aux, signature)`..

## Acceptance Criteria

1. Create `message.py` module with `Message` dataclass
2. Fields: `ssid` (str), `round` (int), `protocol_id` (str), `phase` (str), `sender_id` (int), `value` (Any), `digest` (Optional[bytes]), `aux` (Dict), `signature` (bytes)
3. Type hints enforced for all fields
4. `__post_init__` validation ensuring required fields are non-null
5. Helper method `to_dict()` for serialization preparation
6. Helper method `signing_payload()` returning canonical bytes for signing (excludes signature field)
7. Unit tests covering: valid message creation, type validation, signing payload generation
8. Docstrings explaining Byzantine Agreement message semantics

## Prerequisites

Story 1.1
