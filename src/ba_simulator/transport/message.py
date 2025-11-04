"""
Byzantine Agreement Message Schema

This module defines the canonical message data structure used throughout the BA simulator.
All protocol messages (CoD, GDA, PoP, BA) follow this strict schema to ensure authenticated,
deterministic message handling in Byzantine fault-tolerant distributed consensus.

The message schema enforces the foundational properties required for Byzantine Agreement:
- Authentication: Every message carries a cryptographic signature
- Integrity: Messages are tamper-evident through signing
- Traceability: Each message is bound to a specific round, protocol, phase, and sender
- Determinism: Canonical serialization ensures reproducible message handling
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Message:
    """
    Canonical message format for Byzantine Agreement protocols.

    Schema: (ssid, round, protocol_id, phase, sender_id, value|digest, aux, signature)

    This dataclass represents a single authenticated protocol message in the BA simulator.
    All messages are cryptographically signed and bound to a specific round and protocol phase.

    Fields:
        ssid: Session identifier - unique string identifying the BA execution instance
        round: Round number (0-indexed) - temporal ordering of protocol execution
        protocol_id: Protocol identifier (e.g., "CoD", "GDA", "PoP", "BA")
        phase: Protocol phase (e.g., "SEND", "ECHO", "READY", "PROPOSE", "VOTE")
        sender_id: Sender's participant ID (0-indexed integer)
        value: Arbitrary protocol-specific payload (proposal, vote, etc.)
        digest: Optional cryptographic digest of value (for large payloads)
        aux: Auxiliary data dictionary for protocol-specific metadata
        signature: Ed25519 signature (64 bytes) authenticating the message

    Byzantine Agreement Semantics:
        - Messages are immutable once signed (dataclass frozen=False but should not be modified)
        - Round binding prevents replay attacks across different rounds
        - Phase binding ensures messages are only processed in correct protocol stage
        - Signature provides non-repudiation and authentication
        - SSID ensures messages from different BA instances don't interfere

    Usage:
        >>> msg = Message(
        ...     ssid="experiment-001",
        ...     round=5,
        ...     protocol_id="CoD",
        ...     phase="SEND",
        ...     sender_id=3,
        ...     value="propose-A",
        ...     digest=None,
        ...     aux={},
        ...     signature=b'\\x00' * 64
        ... )
        >>> payload = msg.signing_payload()  # Get canonical bytes for signing
        >>> msg_dict = msg.to_dict()  # Serialize for JSON export
    """

    ssid: str
    round: int
    protocol_id: str
    phase: str
    sender_id: int
    value: Any
    digest: Optional[bytes]
    aux: Dict[str, Any]
    signature: bytes

    def __post_init__(self) -> None:
        """
        Validate message fields after initialization.

        Ensures all required fields are non-null and signature has correct length.
        This provides early failure detection for malformed messages.

        Raises:
            ValueError: If any required field is None or signature length is invalid
        """
        # Validate required string fields
        if self.ssid is None or self.ssid == "":
            raise ValueError("ssid must be a non-empty string")
        if self.protocol_id is None or self.protocol_id == "":
            raise ValueError("protocol_id must be a non-empty string")
        if self.phase is None or self.phase == "":
            raise ValueError("phase must be a non-empty string")

        # Validate required integer fields
        if self.round is None:
            raise ValueError("round must be a non-null integer")
        if self.sender_id is None:
            raise ValueError("sender_id must be a non-null integer")

        # Validate signature (Ed25519 signatures are exactly 64 bytes)
        if self.signature is None:
            raise ValueError("signature must be non-null bytes")
        if len(self.signature) != 64:
            raise ValueError(
                f"signature must be exactly 64 bytes (Ed25519), got {len(self.signature)}"
            )

        # Validate aux is not None (can be empty dict)
        if self.aux is None:
            raise ValueError("aux must be a dictionary (can be empty)")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary for JSON serialization.

        This method prepares the message for canonical JSON serialization (Story 1.3).
        All fields are included in the dictionary output.

        Returns:
            Dictionary representation of the message with all fields

        Note:
            Binary fields (signature, digest) are returned as bytes objects.
            The JSON serialization layer (Story 1.3) will handle base64 encoding.
        """
        return {
            "ssid": self.ssid,
            "round": self.round,
            "protocol_id": self.protocol_id,
            "phase": self.phase,
            "sender_id": self.sender_id,
            "value": self.value,
            "digest": self.digest,
            "aux": self.aux,
            "signature": self.signature,
        }

    def signing_payload(self) -> bytes:
        """
        Generate canonical bytes for cryptographic signing.

        Returns the message content as canonical bytes, EXCLUDING the signature field.
        This prevents circular dependency during the signing process:
        1. Create unsigned message (signature = empty placeholder)
        2. Generate signing_payload() bytes
        3. Sign the payload to produce signature
        4. Attach signature to message

        The canonical representation uses JSON serialization with sorted keys
        to ensure deterministic byte output (same message always produces same bytes).

        Returns:
            Canonical byte representation of message (without signature field)

        Note:
            This method will be integrated with Story 1.3 (JSON serialization)
            and Story 1.5 (cryptographic signing) to produce authenticated messages.

        Byzantine Agreement Property:
            Deterministic signing payload is critical for:
            - Consistent signature verification across all participants
            - Preventing equivocation detection (same logical message = same bytes)
            - Ensuring canonical message deduplication (Story 1.7)
        """
        import json

        # Create payload dictionary excluding signature
        payload_dict = {
            "ssid": self.ssid,
            "round": self.round,
            "protocol_id": self.protocol_id,
            "phase": self.phase,
            "sender_id": self.sender_id,
            "value": self.value,
            "digest": self.digest.hex() if self.digest else None,  # Convert bytes to hex for JSON
            "aux": self.aux,
        }

        # Canonical JSON: sorted keys, no whitespace, UTF-8 encoding
        # This ensures deterministic byte representation
        canonical_json = json.dumps(payload_dict, sort_keys=True, separators=(",", ":"))
        return canonical_json.encode("utf-8")
