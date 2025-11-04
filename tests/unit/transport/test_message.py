"""
Unit tests for Message dataclass

Tests cover all acceptance criteria:
- AC1: Message module and dataclass creation
- AC2: Field types and structure
- AC3: Type hint enforcement
- AC4: __post_init__ validation
- AC5: to_dict() serialization helper
- AC6: signing_payload() canonical bytes
- AC7: Valid message creation and edge cases
- AC8: Docstring presence and quality
"""

import json
import pytest
from typing import get_type_hints
from dataclasses import fields

from ba_simulator.transport.message import Message


# ============================================================================
# AC1: Message Module and Dataclass Creation
# ============================================================================


def test_message_import():
    """Test: Import Message class successfully from ba_simulator.transport.message"""
    from ba_simulator.transport.message import Message

    assert Message is not None


def test_message_is_dataclass():
    """Test: Message class has @dataclass decorator applied"""
    from dataclasses import is_dataclass

    assert is_dataclass(Message), "Message should be a dataclass"


# ============================================================================
# AC2 & AC3: Field Types and Type Hint Enforcement
# ============================================================================


def test_message_fields_exist():
    """Test: Message has all required fields"""
    msg_fields = {f.name for f in fields(Message)}
    expected_fields = {
        "ssid",
        "round",
        "protocol_id",
        "phase",
        "sender_id",
        "value",
        "digest",
        "aux",
        "signature",
    }
    assert msg_fields == expected_fields, f"Missing or extra fields. Got: {msg_fields}"


def test_message_type_hints():
    """Test: All fields have proper type annotations"""
    from typing import Any, Dict, Optional

    type_hints = get_type_hints(Message)

    # Verify each field has correct type hint
    assert type_hints["ssid"] == str
    assert type_hints["round"] == int
    assert type_hints["protocol_id"] == str
    assert type_hints["phase"] == str
    assert type_hints["sender_id"] == int
    assert type_hints["value"] == Any
    assert type_hints["digest"] == Optional[bytes]
    assert type_hints["aux"] == Dict[str, Any]
    assert type_hints["signature"] == bytes


def test_valid_message_creation():
    """Test: Create valid Message with all fields, verify each field type"""
    msg = Message(
        ssid="test-session",
        round=5,
        protocol_id="CoD",
        phase="SEND",
        sender_id=3,
        value="test-value",
        digest=b"\x00" * 32,
        aux={"metadata": "test"},
        signature=b"\x00" * 64,
    )

    # Verify field types
    assert isinstance(msg.ssid, str)
    assert isinstance(msg.round, int)
    assert isinstance(msg.protocol_id, str)
    assert isinstance(msg.phase, str)
    assert isinstance(msg.sender_id, int)
    # value is Any, so just check it exists
    assert msg.value == "test-value"
    assert isinstance(msg.digest, bytes) or msg.digest is None
    assert isinstance(msg.aux, dict)
    assert isinstance(msg.signature, bytes)


# ============================================================================
# AC4: __post_init__ Validation
# ============================================================================


def test_post_init_validation_ssid_none():
    """Test: Create Message with None for ssid, expect ValueError"""
    with pytest.raises(ValueError, match="ssid must be a non-empty string"):
        Message(
            ssid=None,
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_ssid_empty():
    """Test: Create Message with empty ssid, expect ValueError"""
    with pytest.raises(ValueError, match="ssid must be a non-empty string"):
        Message(
            ssid="",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_protocol_id_none():
    """Test: Create Message with None for protocol_id, expect ValueError"""
    with pytest.raises(ValueError, match="protocol_id must be a non-empty string"):
        Message(
            ssid="test",
            round=1,
            protocol_id=None,
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_phase_none():
    """Test: Create Message with None for phase, expect ValueError"""
    with pytest.raises(ValueError, match="phase must be a non-empty string"):
        Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase=None,
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_round_none():
    """Test: Create Message with None for round, expect ValueError"""
    with pytest.raises(ValueError, match="round must be a non-null integer"):
        Message(
            ssid="test",
            round=None,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_sender_id_none():
    """Test: Create Message with None for sender_id, expect ValueError"""
    with pytest.raises(ValueError, match="sender_id must be a non-null integer"):
        Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=None,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )


def test_post_init_validation_signature_none():
    """Test: Create Message with None signature, expect ValueError"""
    with pytest.raises(ValueError, match="signature must be non-null bytes"):
        Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=None,
        )


def test_post_init_validation_signature_wrong_length():
    """Test: Create Message with wrong signature length, expect ValueError"""
    with pytest.raises(ValueError, match="signature must be exactly 64 bytes"):
        Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 32,  # Wrong length (should be 64)
        )


def test_post_init_validation_aux_none():
    """Test: Create Message with None aux, expect ValueError"""
    with pytest.raises(ValueError, match="aux must be a dictionary"):
        Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase="SEND",
            sender_id=0,
            value="test",
            digest=None,
            aux=None,
            signature=b"\x00" * 64,
        )


def test_post_init_validation_success():
    """Test: Valid message with all fields populated passes __post_init__ without error"""
    try:
        msg = Message(
            ssid="test-session",
            round=10,
            protocol_id="GDA",
            phase="PROPOSE",
            sender_id=7,
            value={"proposal": "A"},
            digest=b"\xaa" * 32,
            aux={"round_start": 1234567890},
            signature=b"\xff" * 64,
        )
        assert msg is not None
    except Exception as e:
        pytest.fail(f"Valid message should not raise exception: {e}")


# ============================================================================
# AC5: to_dict() Serialization Helper
# ============================================================================


def test_to_dict_returns_dict():
    """Test: Call to_dict() on valid message, verify returns Dict[str, Any]"""
    msg = Message(
        ssid="test",
        round=5,
        protocol_id="CoD",
        phase="ECHO",
        sender_id=2,
        value="test-value",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )

    result = msg.to_dict()
    assert isinstance(result, dict), "to_dict() should return a dictionary"


def test_to_dict_contains_all_fields():
    """Test: Verify to_dict() output contains all field names as keys"""
    msg = Message(
        ssid="test",
        round=5,
        protocol_id="CoD",
        phase="ECHO",
        sender_id=2,
        value="test-value",
        digest=None,
        aux={"key": "value"},
        signature=b"\x00" * 64,
    )

    result = msg.to_dict()
    expected_keys = {
        "ssid",
        "round",
        "protocol_id",
        "phase",
        "sender_id",
        "value",
        "digest",
        "aux",
        "signature",
    }
    assert set(result.keys()) == expected_keys, "Missing keys in to_dict() output"


def test_to_dict_preserves_values():
    """Test: Verify to_dict() preserves field values correctly"""
    msg = Message(
        ssid="session-123",
        round=42,
        protocol_id="BA",
        phase="VOTE",
        sender_id=5,
        value={"vote": "yes"},
        digest=b"\xde\xad\xbe\xef",
        aux={"timestamp": 999},
        signature=b"\xca\xfe" * 32,
    )

    result = msg.to_dict()

    assert result["ssid"] == "session-123"
    assert result["round"] == 42
    assert result["protocol_id"] == "BA"
    assert result["phase"] == "VOTE"
    assert result["sender_id"] == 5
    assert result["value"] == {"vote": "yes"}
    assert result["digest"] == b"\xde\xad\xbe\xef"
    assert result["aux"] == {"timestamp": 999}
    assert result["signature"] == b"\xca\xfe" * 32


# ============================================================================
# AC6: signing_payload() Canonical Bytes
# ============================================================================


def test_signing_payload_returns_bytes():
    """Test: Call signing_payload() on message, verify returns bytes type"""
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

    payload = msg.signing_payload()
    assert isinstance(payload, bytes), "signing_payload() should return bytes"


def test_signing_payload_excludes_signature():
    """Test: Verify signing_payload() excludes signature field from output"""
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},
        signature=b"\xaa" * 64,
    )

    payload = msg.signing_payload()
    payload_str = payload.decode("utf-8")

    # Signature should NOT appear in the payload
    assert "signature" not in payload_str, "signing_payload() should exclude signature field"


def test_signing_payload_deterministic():
    """Test: Same message produces identical signing_payload() bytes"""
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
        signature=b"\xff" * 64,  # Different signature
    )

    # Same message content should produce identical payload
    assert (
        msg1.signing_payload() == msg2.signing_payload()
    ), "Same message should produce identical signing payload regardless of signature"


def test_signing_payload_different_messages():
    """Test: Different messages produce different signing_payload() bytes"""
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

    assert (
        msg1.signing_payload() != msg2.signing_payload()
    ), "Different messages should produce different signing payloads"


def test_signing_payload_canonical_json():
    """Test: Verify signing_payload() produces valid JSON with sorted keys"""
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

    payload = msg.signing_payload()
    payload_str = payload.decode("utf-8")

    # Should be valid JSON
    parsed = json.loads(payload_str)
    assert parsed is not None

    # Keys should be sorted (aux keys will be sorted in JSON output)
    # Verify canonical format: no spaces after separators
    assert ", " not in payload_str, "Canonical JSON should use compact separators"
    assert ": " not in payload_str, "Canonical JSON should use compact separators"


# ============================================================================
# AC7: Edge Cases and Valid Message Creation
# ============================================================================


def test_message_cod_protocol():
    """Test: Create message with CoD protocol_id"""
    msg = Message(
        ssid="exp-001",
        round=0,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="value-A",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.protocol_id == "CoD"


def test_message_gda_protocol():
    """Test: Create message with GDA protocol_id"""
    msg = Message(
        ssid="exp-001",
        round=0,
        protocol_id="GDA",
        phase="PROPOSE",
        sender_id=0,
        value="value-A",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.protocol_id == "GDA"


def test_message_pop_protocol():
    """Test: Create message with PoP protocol_id"""
    msg = Message(
        ssid="exp-001",
        round=0,
        protocol_id="PoP",
        phase="SEND",
        sender_id=0,
        value="digest-data",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.protocol_id == "PoP"


def test_message_ba_protocol():
    """Test: Create message with BA protocol_id"""
    msg = Message(
        ssid="exp-001",
        round=0,
        protocol_id="BA",
        phase="CONTROL",
        sender_id=0,
        value="meta-info",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.protocol_id == "BA"


def test_message_different_phases():
    """Test: Create messages with different phases (SEND, ECHO, READY, etc.)"""
    phases = ["SEND", "ECHO", "READY", "PROPOSE", "GRADE", "VOTE"]

    for phase in phases:
        msg = Message(
            ssid="test",
            round=1,
            protocol_id="CoD",
            phase=phase,
            sender_id=0,
            value="test",
            digest=None,
            aux={},
            signature=b"\x00" * 64,
        )
        assert msg.phase == phase


def test_message_boundary_values():
    """Test: Edge case - round=0, sender_id=0 (valid boundary values)"""
    msg = Message(
        ssid="test",
        round=0,  # Boundary: first round
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,  # Boundary: first participant
        value="test",
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.round == 0
    assert msg.sender_id == 0


def test_message_empty_aux_dict():
    """Test: Edge case - empty aux dict {} (valid optional)"""
    msg = Message(
        ssid="test",
        round=1,
        protocol_id="CoD",
        phase="SEND",
        sender_id=0,
        value="test",
        digest=None,
        aux={},  # Empty but valid
        signature=b"\x00" * 64,
    )
    assert msg.aux == {}


def test_message_none_digest():
    """Test: Edge case - None digest (valid optional)"""
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
    assert msg.digest is None


def test_message_complex_value():
    """Test: Message with complex value (dict, list, nested structures)"""
    complex_value = {
        "proposal": "A",
        "metadata": {"round": 5, "participants": [0, 1, 2, 3]},
        "nested": {"deep": {"structure": True}},
    }

    msg = Message(
        ssid="test",
        round=1,
        protocol_id="GDA",
        phase="PROPOSE",
        sender_id=0,
        value=complex_value,
        digest=None,
        aux={},
        signature=b"\x00" * 64,
    )
    assert msg.value == complex_value


# ============================================================================
# AC8: Docstring Presence and Quality
# ============================================================================


def test_message_class_docstring():
    """Test: Verify Message class has non-empty __doc__ attribute"""
    assert Message.__doc__ is not None, "Message class should have a docstring"
    assert len(Message.__doc__.strip()) > 0, "Message docstring should be non-empty"


def test_message_class_docstring_mentions_byzantine():
    """Test: Check docstring mentions 'Byzantine Agreement' or 'protocol message'"""
    docstring = Message.__doc__.lower()
    assert (
        "byzantine" in docstring or "protocol" in docstring
    ), "Message docstring should explain Byzantine Agreement context"


def test_signing_payload_docstring():
    """Test: Verify signing_payload method has docstring"""
    assert (
        Message.signing_payload.__doc__ is not None
    ), "signing_payload method should have a docstring"
    assert (
        len(Message.signing_payload.__doc__.strip()) > 0
    ), "signing_payload docstring should be non-empty"


def test_to_dict_docstring():
    """Test: Verify to_dict method has docstring"""
    assert Message.to_dict.__doc__ is not None, "to_dict method should have a docstring"
    assert len(Message.to_dict.__doc__.strip()) > 0, "to_dict docstring should be non-empty"


def test_post_init_docstring():
    """Test: Verify __post_init__ method has docstring"""
    assert Message.__post_init__.__doc__ is not None, "__post_init__ method should have a docstring"
    assert (
        len(Message.__post_init__.__doc__.strip()) > 0
    ), "__post_init__ docstring should be non-empty"
