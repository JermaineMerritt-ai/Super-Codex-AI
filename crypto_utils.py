"""
Cryptographic utilities for the AXIOM-FLAME system.

This module provides functions for council key management and message signing
using NaCl (Networking and Cryptography library) with Ed25519 signatures.
"""

from nacl import signing, encoding


def load_council_key(path: str):
    """
    Load a council signing key from a file containing the private key seed.
    
    Args:
        path: Path to the file containing the Ed25519 private key seed
        
    Returns:
        signing.SigningKey: The loaded signing key for cryptographic operations
        
    Raises:
        FileNotFoundError: If the key file doesn't exist
        ValueError: If the key file contains invalid key data
    """
    with open(path, "rb") as f:
        seed = f.read()
    return signing.SigningKey(seed)


def sign_bytes(sk: signing.SigningKey, data: bytes) -> str:
    """
    Sign binary data using an Ed25519 signing key.
    
    Args:
        sk: The signing key to use for the signature
        data: The binary data to sign
        
    Returns:
        str: Base64-encoded signature string
        
    Example:
        >>> sk = load_council_key("/path/to/council.key")
        >>> signature = sign_bytes(sk, b"ceremonial data")
        >>> print(f"Signature: {signature}")
    """
    sig = sk.sign(data).signature
    return encoding.Base64Encoder.encode(sig).decode("utf-8")


def verify_signature(public_key_bytes: bytes, signature: str, data: bytes) -> bool:
    """
    Verify a signature against data using a public key.
    
    Args:
        public_key_bytes: The Ed25519 public key as bytes
        signature: Base64-encoded signature string
        data: The original data that was signed
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        verify_key = signing.VerifyKey(public_key_bytes)
        sig_bytes = encoding.Base64Encoder.decode(signature.encode("utf-8"))
        verify_key.verify(data, sig_bytes)
        return True
    except Exception:
        return False


def get_public_key(sk: signing.SigningKey) -> bytes:
    """
    Extract the public key from a signing key.
    
    Args:
        sk: The signing key
        
    Returns:
        bytes: The Ed25519 public key as bytes
    """
    return bytes(sk.verify_key)


def generate_council_key() -> signing.SigningKey:
    """
    Generate a new Ed25519 signing key for council use.
    
    Returns:
        signing.SigningKey: A new randomly generated signing key
        
    Note:
        The private key seed should be saved securely using save_council_key()
    """
    return signing.SigningKey.generate()


def save_council_key(sk: signing.SigningKey, path: str) -> None:
    """
    Save a council signing key to a file.
    
    Args:
        sk: The signing key to save
        path: Path where to save the private key seed
        
    Security Note:
        The saved file contains sensitive cryptographic material and should
        be protected with appropriate file permissions (600 or similar).
    """
    with open(path, "wb") as f:
        f.write(sk.encode())