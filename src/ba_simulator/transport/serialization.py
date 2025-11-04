"""
Message Serialization Infrastructure

This module provides a pluggable serialization abstraction layer for Byzantine Agreement messages.
The design supports future migration from JSON to CBOR while maintaining deterministic byte output
for cryptographic hashing and signature verification.

Key Features:
- Abstract MessageSerializer interface for format-agnostic serialization
- JSONMessageSerializer concrete implementation with canonical key ordering
- Base64 encoding for binary fields (signature, digest) to ensure JSON compatibility
- Deterministic output: identical messages always produce identical bytes
- Round-trip guarantee: decode(encode(msg)) == msg

Design Rationale:
The abstraction layer isolates serialization format from the rest of the codebase,
enabling seamless transition to CBOR (or other formats) without impacting message
handling, signing, or verification logic. This follows the dependency inversion principle
and prepares the system for production-grade efficiency improvements.
"""

import base64
import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from .message import Message


class MessageSerializer(ABC):
    """
    Abstract base class for message serialization.

    This interface defines the contract for all message serializers, ensuring
    consistent encode/decode behavior regardless of underlying format (JSON, CBOR, etc.).

    All implementations MUST guarantee:
    1. Determinism: Same message always produces identical bytes
    2. Round-trip integrity: decode(encode(msg)) == msg
    3. Binary field handling: Proper encoding of signature and digest fields
    """

    @abstractmethod
    def encode(self, message: Message) -> bytes:
        """
        Serialize a Message object to bytes.

        Args:
            message: Message instance to serialize

        Returns:
            Deterministic byte representation of the message

        Raises:
            ValueError: If message validation fails
        """
        pass

    @abstractmethod
    def decode(self, data: bytes) -> Message:
        """
        Deserialize bytes to a Message object.

        Args:
            data: Serialized message bytes

        Returns:
            Reconstructed Message instance

        Raises:
            ValueError: If deserialization fails or message is invalid
        """
        pass


class JSONMessageSerializer(MessageSerializer):
    """
    JSON-based message serializer with canonical key ordering.

    Implementation Details:
    - Uses json.dumps with sort_keys=True for deterministic output
    - Binary fields (signature, digest) are base64-encoded for JSON compatibility
    - Compact representation: separators=(',', ':') removes whitespace
    - UTF-8 encoding for all byte conversions

    Canonical Ordering:
    JSON keys are sorted alphabetically, ensuring identical messages produce
    identical byte streams. This is critical for:
    - Cryptographic signing and verification
    - Message deduplication via hash-based tracking
    - Consistent replay protection across all participants

    Binary Field Handling:
    Ed25519 signatures (64 bytes) and SHA-256 digests (32 bytes) are base64-encoded
    before JSON serialization. During decode, base64 strings are converted back to bytes.

    Example:
        >>> serializer = JSONMessageSerializer()
        >>> msg = Message(...)
        >>> data = serializer.encode(msg)
        >>> reconstructed = serializer.decode(data)
        >>> assert reconstructed == msg  # Round-trip guarantee
    """

    def encode(self, message: Message) -> bytes:
        """
        Encode Message to canonical JSON bytes.

        Process:
        1. Convert message to dictionary via to_dict()
        2. Base64-encode binary fields (signature, digest)
        3. JSON serialize with sorted keys and no whitespace
        4. Encode to UTF-8 bytes

        Args:
            message: Message instance to encode

        Returns:
            Canonical JSON bytes with deterministic ordering

        Raises:
            ValueError: If message validation fails in to_dict()
        """
        # Convert message to dictionary
        msg_dict = message.to_dict()

        # Base64-encode binary fields for JSON compatibility
        encoded_dict = self._encode_binary_fields(msg_dict)

        # Canonical JSON: sorted keys, no whitespace
        json_str = json.dumps(encoded_dict, sort_keys=True, separators=(",", ":"))

        # Return UTF-8 encoded bytes
        return json_str.encode("utf-8")

    def decode(self, data: bytes) -> Message:
        """
        Decode JSON bytes to Message object.

        Process:
        1. Decode UTF-8 bytes to string
        2. Parse JSON to dictionary
        3. Base64-decode binary fields (signature, digest)
        4. Reconstruct Message object with decoded fields

        Args:
            data: UTF-8 encoded JSON bytes

        Returns:
            Reconstructed Message instance

        Raises:
            ValueError: If JSON parsing fails, base64 decoding fails, or Message validation fails
            json.JSONDecodeError: If data is not valid JSON
        """
        # Decode UTF-8 bytes to string
        json_str = data.decode("utf-8")

        # Parse JSON
        msg_dict = json.loads(json_str)

        # Decode binary fields from base64
        decoded_dict = self._decode_binary_fields(msg_dict)

        # Reconstruct Message object
        return Message(**decoded_dict)

    def _encode_binary_fields(self, msg_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert binary fields (signature, digest) to base64 strings.

        Args:
            msg_dict: Message dictionary with binary fields as bytes

        Returns:
            Dictionary with binary fields base64-encoded as strings
        """
        encoded = msg_dict.copy()

        # Encode signature (always present)
        if "signature" in encoded and encoded["signature"] is not None:
            encoded["signature"] = base64.b64encode(encoded["signature"]).decode("ascii")

        # Encode digest (optional field)
        if "digest" in encoded and encoded["digest"] is not None:
            encoded["digest"] = base64.b64encode(encoded["digest"]).decode("ascii")

        return encoded

    def _decode_binary_fields(self, msg_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert base64 strings back to binary fields (signature, digest).

        Args:
            msg_dict: Message dictionary with base64-encoded binary fields

        Returns:
            Dictionary with binary fields decoded to bytes

        Raises:
            ValueError: If base64 decoding fails
        """
        decoded = msg_dict.copy()

        # Decode signature (always present)
        if "signature" in decoded and decoded["signature"] is not None:
            try:
                decoded["signature"] = base64.b64decode(decoded["signature"])
            except Exception as e:
                raise ValueError(f"Failed to decode signature from base64: {e}")

        # Decode digest (optional field)
        if "digest" in decoded and decoded["digest"] is not None:
            try:
                decoded["digest"] = base64.b64decode(decoded["digest"])
            except Exception as e:
                raise ValueError(f"Failed to decode digest from base64: {e}")

        return decoded
