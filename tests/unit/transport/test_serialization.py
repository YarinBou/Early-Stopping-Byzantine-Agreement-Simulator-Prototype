"""
Unit tests for Message Serialization

Tests cover all acceptance criteria:
- AC1: serialization.py module with MessageSerializer class
- AC2: encode(message: Message) -> bytes with canonical key ordering
- AC3: Base64 encoding for binary fields (signature, digest)
- AC4: decode(data: bytes) -> Message reconstruction
- AC5: Round-trip test: decode(encode(msg)) == msg
- AC6: Deterministic output for identical messages
- AC7: Abstraction layer for future CBOR migration
- AC8: Unit tests for encoding, decoding, determinism, base64, error cases
"""

import base64
import json
import pytest
from abc import ABC

from ba_simulator.transport.message import Message
from ba_simulator.transport.serialization import MessageSerializer, JSONMessageSerializer


# ============================================================================
# AC1: Module Structure and Abstract Interface
# ============================================================================


def test_serialization_module_import():
    """Test: Import serialization module successfully"""
    from ba_simulator.transport.serialization import MessageSerializer, JSONMessageSerializer

    assert MessageSerializer is not None
    assert JSONMessageSerializer is not None


def test_message_serializer_is_abstract():
    """Test: MessageSerializer is an abstract base class (ABC)"""
    assert issubclass(MessageSerializer, ABC), "MessageSerializer should inherit from ABC"


def test_message_serializer_cannot_instantiate():
    """Test: Cannot instantiate abstract MessageSerializer directly"""
    with pytest.raises(TypeError):
        MessageSerializer()  # Should fail - abstract class


def test_message_serializer_has_encode_method():
    """Test: MessageSerializer defines abstract encode() method"""
    assert hasattr(MessageSerializer, "encode"), "MessageSerializer should have encode method"


def test_message_serializer_has_decode_method():
    """Test: MessageSerializer defines abstract decode() method"""
    assert hasattr(MessageSerializer, "decode"), "MessageSerializer should have decode method"


def test_json_message_serializer_inherits_from_base():
    """Test: JSONMessageSerializer inherits from MessageSerializer"""
    assert issubclass(
        JSONMessageSerializer, MessageSerializer
    ), "JSONMessageSerializer should inherit from MessageSerializer"


def test_json_message_serializer_can_instantiate():
    """Test: JSONMessageSerializer can be instantiated"""
    serializer = JSONMessageSerializer()
    assert serializer is not None


# ============================================================================
# AC2: encode() Method with Canonical Key Ordering
# ============================================================================


def test_encode_returns_bytes():
    """Test: encode() returns bytes type"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test-value",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    result = serializer.encode(msg)
    assert isinstance(result, bytes), "encode() should return bytes"


def test_encode_produces_valid_json():
    """Test: encode() produces valid JSON that can be parsed"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test-value",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")

    # Should be valid JSON
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict), "Encoded message should parse as JSON dict"


def test_encode_canonical_key_ordering():
    """Test: encode() uses canonical key ordering (sort_keys=True)"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={"z": 1, "a": 2, "m": 3},  # Unsorted keys in aux
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")

    # Verify keys are sorted in JSON output
    # Top-level keys should appear alphabetically: aux, phase, protocol_id, round, sender_id, signature, ssid, value
    # We can check that "aux" appears before "ssid" and "round" appears before "ssid"
    aux_pos = json_str.find('"aux"')
    ssid_pos = json_str.find('"ssid"')
    assert aux_pos < ssid_pos, "Keys should be sorted alphabetically (aux before ssid)"

    # Check aux keys are also sorted (a before m before z)
    aux_section_start = json_str.find('"aux":{')
    aux_section_end = json_str.find("}", aux_section_start)
    aux_json = json_str[aux_section_start : aux_section_end + 1]

    a_pos = aux_json.find('"a"')
    m_pos = aux_json.find('"m"')
    z_pos = aux_json.find('"z"')
    assert a_pos < m_pos < z_pos, "Aux dict keys should be sorted (a, m, z)"


def test_encode_compact_separators():
    """Test: encode() uses compact separators (no whitespace)"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")

    # Canonical JSON should use compact separators: no spaces after colons or commas
    assert ", " not in json_str, "Encoded JSON should not contain ', ' (space after comma)"
    assert ": " not in json_str, "Encoded JSON should not contain ': ' (space after colon)"


def test_encode_utf8_encoding():
    """Test: encode() uses UTF-8 encoding"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test-üñíçödé",  # Unicode characters
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)

    # Should decode as UTF-8
    decoded_str = encoded.decode("utf-8")
    assert "test-üñíçödé" in decoded_str or "\\u" in decoded_str, "Should handle UTF-8 encoding"


# ============================================================================
# AC3: Base64 Encoding for Binary Fields
# ============================================================================


def test_encode_base64_signature():
    """Test: encode() base64-encodes signature field"""
    serializer = JSONMessageSerializer()
    signature = b"\xde\xad\xbe\xef" * 16  # 64 bytes
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=signature,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")
    parsed = json.loads(json_str)

    # Signature should be base64-encoded string
    expected_b64 = base64.b64encode(signature).decode("ascii")
    assert parsed["signature"] == expected_b64, "Signature should be base64-encoded"


def test_encode_base64_digest():
    """Test: encode() base64-encodes digest field when present"""
    serializer = JSONMessageSerializer()
    digest = b"\xca\xfe\xba\xbe" * 8  # 32 bytes
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=digest,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")
    parsed = json.loads(json_str)

    # Digest should be base64-encoded string
    expected_b64 = base64.b64encode(digest).decode("ascii")
    assert parsed["digest"] == expected_b64, "Digest should be base64-encoded"


def test_encode_none_digest():
    """Test: encode() handles None digest (optional field)"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,  # Optional field
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    json_str = encoded.decode("utf-8")
    parsed = json.loads(json_str)

    # Digest should be null in JSON
    assert parsed["digest"] is None, "None digest should serialize as null"


# ============================================================================
# AC4: decode() Method Reconstructs Message Objects
# ============================================================================


def test_decode_returns_message():
    """Test: decode() returns Message instance"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    decoded = serializer.decode(encoded)

    assert isinstance(decoded, Message), "decode() should return Message instance"


def test_decode_preserves_all_fields():
    """Test: decode() reconstructs all message fields correctly"""
    serializer = JSONMessageSerializer()
    original = Message(
        ssid="session-123",
        round=42,
        protocol_id="GDA",
        phase="PROPOSE",
        sender_id=7,
        value={"proposal": "A", "data": [1, 2, 3]},
        digest=b"\xaa" * 32,
        aux={"timestamp": 1234567890, "meta": "info"},
        signature=b"\xff" * 64,
    )

    encoded = serializer.encode(original)
    decoded = serializer.decode(encoded)

    # Verify all fields match
    assert decoded.ssid == original.ssid
    assert decoded.round == original.round
    assert decoded.protocol_id == original.protocol_id
    assert decoded.phase == original.phase
    assert decoded.sender_id == original.sender_id
    assert decoded.value == original.value
    assert decoded.digest == original.digest
    assert decoded.aux == original.aux
    assert decoded.signature == original.signature


def test_decode_base64_signature():
    """Test: decode() correctly decodes base64 signature to bytes"""
    serializer = JSONMessageSerializer()
    signature = b"\x12\x34\x56\x78" * 16  # 64 bytes
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=signature,
    )

    encoded = serializer.encode(msg)
    decoded = serializer.decode(encoded)

    assert decoded.signature == signature, "Decoded signature should match original bytes"
    assert isinstance(decoded.signature, bytes), "Decoded signature should be bytes"


def test_decode_base64_digest():
    """Test: decode() correctly decodes base64 digest to bytes"""
    serializer = JSONMessageSerializer()
    digest = b"\xde\xad\xbe\xef" * 8  # 32 bytes
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=digest,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    decoded = serializer.decode(encoded)

    assert decoded.digest == digest, "Decoded digest should match original bytes"
    assert isinstance(decoded.digest, bytes), "Decoded digest should be bytes"


# ============================================================================
# AC5: Round-Trip Test
# ============================================================================


def test_round_trip_equality():
    """Test: decode(encode(msg)) == msg for all message types"""
    serializer = JSONMessageSerializer()

    # Test various message configurations
    test_cases = [
        # CoD SEND message
        Message(
            ssid="exp-001",
            round=0,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="value-A",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        ),
        # GDA PROPOSE with digest
        Message(
            ssid="exp-002",
            round=5,
            protocol_id="GDA",
            phase="PROPOSE",
            sender_id=3,
            value={"proposal": "B"},
            digest=b"\xaa" * 32,
            aux={"round_start": 1000},
            signature=b"\xff" * 64,
        ),
        # BA with complex value
        Message(
            ssid="exp-003",
            round=10,
            protocol_id="BA",
            phase="VOTE",
            sender_id=7,
            value={"votes": [0, 1, 2], "decision": True},
            digest=b"\x12\x34\x56\x78" * 8,
            aux={"metadata": {"nested": True}},
            signature=b"\xca\xfe" * 32,
        ),
        # Empty aux
        Message(
            ssid="minimal",
            round=1,
            protocol_id="PoP",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\xab" * 64,
        ),
    ]

    for msg in test_cases:
        encoded = serializer.encode(msg)
        decoded = serializer.decode(encoded)
        assert decoded == msg, f"Round-trip failed for message: {msg}"


def test_round_trip_multiple_times():
    """Test: Multiple round-trips preserve message integrity"""
    serializer = JSONMessageSerializer()
    original = Message(
        ssid="test",
        round=5,
        protocol_id="CoD",
        phase="ECHO",
        sender_id=2,
        value="test-value",
        digest=b"\xde\xad" * 16,
        aux={"key": "value"},
        signature=b"\xbe\xef" * 32,
    )

    # Perform multiple encode/decode cycles
    msg = original
    for _ in range(3):
        encoded = serializer.encode(msg)
        msg = serializer.decode(encoded)

    assert msg == original, "Multiple round-trips should preserve message"


# ============================================================================
# AC6: Deterministic Output
# ============================================================================


def test_deterministic_output_same_message():
    """Test: Same message always produces identical bytes"""
    serializer = JSONMessageSerializer()

    msg1 = Message(
        ssid="test",
        round=5,
        protocol_id="GDA",
        phase="GRADE",
        sender_id=3,
        value="proposal-X",
        digest=b"\x12\x34",
        aux={"meta": "data"},
        signature=b"\x00" * 64,
    )

    msg2 = Message(
        ssid="test",
        round=5,
        protocol_id="GDA",
        phase="GRADE",
        sender_id=3,
        value="proposal-X",
        digest=b"\x12\x34",
        aux={"meta": "data"},
        signature=b"\x00" * 64,
    )

    encoded1 = serializer.encode(msg1)
    encoded2 = serializer.encode(msg2)

    assert encoded1 == encoded2, "Same message should produce identical bytes"


def test_deterministic_output_multiple_encodings():
    """Test: Encoding same message multiple times produces identical bytes"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={"z": 1, "a": 2},  # Unsorted keys
        signature=b"\x00" * 64,
    )

    # Encode the same message 5 times
    encodings = [serializer.encode(msg) for _ in range(5)]

    # All encodings should be identical
    for encoding in encodings[1:]:
        assert encoding == encodings[0], "Multiple encodings should be identical"


def test_deterministic_output_different_messages():
    """Test: Different messages produce different bytes"""
    serializer = JSONMessageSerializer()

    msg1 = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="A",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    msg2 = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="B",  # Different value
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    encoded1 = serializer.encode(msg1)
    encoded2 = serializer.encode(msg2)

    assert encoded1 != encoded2, "Different messages should produce different bytes"


# ============================================================================
# AC7: Abstraction Layer for Future Migration
# ============================================================================


def test_abstract_interface_enforces_encode():
    """Test: Subclass without encode() cannot be instantiated"""

    class IncompleteSerializer(MessageSerializer):
        def decode(self, data: bytes) -> Message:
            pass

    with pytest.raises(TypeError):
        IncompleteSerializer()  # Should fail - missing encode()


def test_abstract_interface_enforces_decode():
    """Test: Subclass without decode() cannot be instantiated"""

    class IncompleteSerializer(MessageSerializer):
        def encode(self, message: Message) -> bytes:
            pass

    with pytest.raises(TypeError):
        IncompleteSerializer()  # Should fail - missing decode()


def test_abstraction_layer_allows_multiple_implementations():
    """Test: Multiple serializer implementations can coexist"""

    # Define a mock CBOR serializer (just a stub for testing abstraction)
    class MockCBORSerializer(MessageSerializer):
        def encode(self, message: Message) -> bytes:
            # Stub implementation
            return b"mock-cbor-data"

        def decode(self, data: bytes) -> Message:
            # Stub implementation
            return Message(
                ssid="mock",
                round=0,
                protocol_id="mock",
                phase="mock",
                sender_id=0,
                value="mock",
                digest=None,
                aux={},
                signature=b"\x00" * 64,
            )

    json_serializer = JSONMessageSerializer()
    cbor_serializer = MockCBORSerializer()

    # Both should be instances of MessageSerializer
    assert isinstance(json_serializer, MessageSerializer)
    assert isinstance(cbor_serializer, MessageSerializer)


# ============================================================================
# AC8: Error Handling and Edge Cases
# ============================================================================


def test_decode_invalid_json():
    """Test: decode() raises error on malformed JSON"""
    serializer = JSONMessageSerializer()

    invalid_json = b"not-valid-json"

    with pytest.raises((json.JSONDecodeError, ValueError)):
        serializer.decode(invalid_json)


def test_decode_invalid_base64_signature():
    """Test: decode() raises error on invalid base64 in signature field"""
    serializer = JSONMessageSerializer()

    # Create JSON with invalid base64 (not valid base64 string)
    invalid_json = json.dumps(
        {
            "ssid": "test",
            "round": 1,
            "protocol_id": "CoD",
            "phase": "SEND",
            "sender_id": 0,
            "value": "test",
            "digest": None,
            "aux": {},
            "signature": "not-valid-base64!@#$",  # Invalid base64
        }
    ).encode("utf-8")

    with pytest.raises(ValueError, match="Failed to decode signature"):
        serializer.decode(invalid_json)


def test_decode_invalid_base64_digest():
    """Test: decode() raises error on invalid base64 in digest field"""
    serializer = JSONMessageSerializer()

    # Create JSON with invalid base64 digest
    invalid_json = json.dumps(
        {
            "ssid": "test",
            "round": 1,
            "protocol_id": "CoD",
            "phase": "SEND",
            "sender_id": 0,
            "value": "test",
            "digest": "not-valid-base64!@#$",  # Invalid base64
            "aux": {},
            "signature": base64.b64encode(b"\x00" * 64).decode("ascii"),
        }
    ).encode("utf-8")

    with pytest.raises(ValueError, match="Failed to decode digest"):
        serializer.decode(invalid_json)


def test_decode_missing_required_field():
    """Test: decode() raises error when required field is missing"""
    serializer = JSONMessageSerializer()

    # JSON missing 'signature' field
    incomplete_json = json.dumps(
        {
            "ssid": "test",
            "round": 1,
            "protocol_id": "CoD",
            "phase": "SEND",
            "sender_id": 0,
            "value": "test",
            "digest": None,
            "aux": {},
            # Missing 'signature'
        }
    ).encode("utf-8")

    with pytest.raises((TypeError, KeyError)):
        serializer.decode(incomplete_json)


def test_decode_invalid_message_validation():
    """Test: decode() raises error when Message validation fails"""
    serializer = JSONMessageSerializer()

    # JSON with invalid signature length (wrong size)
    invalid_msg_json = json.dumps(
        {
            "ssid": "test",
            "round": 1,
            "protocol_id": "CoD",
            "phase": "SEND",
            "sender_id": 0,
            "value": "test",
            "digest": None,
            "aux": {},
            "signature": base64.b64encode(b"\x00" * 32).decode(
                "ascii"
            ),  # Wrong size (32 instead of 64)
        }
    ).encode("utf-8")

    with pytest.raises(ValueError, match="signature must be exactly 64 bytes"):
        serializer.decode(invalid_msg_json)


def test_encode_with_empty_aux():
    """Test: Edge case - encode message with empty aux dict"""
    serializer = JSONMessageSerializer()
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},  # Empty dict
        signature=b"\x00" * 64,
    )

    encoded = serializer.encode(msg)
    decoded = serializer.decode(encoded)

    assert decoded.aux == {}


def test_encode_with_various_value_types():
    """Test: Edge case - encode messages with different value types"""
    serializer = JSONMessageSerializer()

    test_values = [
        "string-value",
        42,
        3.14,
        True,
        False,
        None,
        ["list", "of", "items"],
        {"dict": "value"},
        {"nested": {"deep": {"structure": [1, 2, 3]}}},
    ]

    for value in test_values:
        msg = Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value=value,
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )

        encoded = serializer.encode(msg)
        decoded = serializer.decode(encoded)

        assert decoded.value == value, f"Failed to round-trip value type: {type(value)}"


def test_encode_binary_fields_with_different_patterns():
    """Test: Edge case - encode signature and digest with various byte patterns"""
    serializer = JSONMessageSerializer()

    # Test different byte patterns
    patterns = [
        (b"\x00" * 64, b"\x00" * 32),  # All zeros
        (b"\xff" * 64, b"\xff" * 32),  # All ones
        (b"\xaa\x55" * 32, b"\x12\x34\x56\x78" * 8),  # Alternating patterns
        (bytes(range(64)), bytes(range(32))),  # Sequential bytes
    ]

    for signature, digest in patterns:
        msg = Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=digest,
            aux={},
            signature=signature,
        )

        encoded = serializer.encode(msg)
        decoded = serializer.decode(encoded)

        assert decoded.signature == signature
        assert decoded.digest == digest
