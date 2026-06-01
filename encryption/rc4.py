"""
encryption/rc4.py -- Full RC4 stream cipher implementation.

Implements the Rivest Cipher 4 (RC4) algorithm exactly as described in:
  "Design and implementation of cipher algorithm based secure optical communication system"

Components:
  - Key Scheduling Algorithm (KSA): initialises the state array S
  - Pseudo-Random Generation Algorithm (PRGA): generates keystream bytes

RC4 is symmetric: encrypt and decrypt are identical operations (XOR with keystream).
"""

from __future__ import annotations
import numpy as np
from typing import Union


class RC4:
    """
    Full RC4 stream cipher.

    Usage
    -----
    >>> cipher = RC4(b"MySecretKey")
    >>> ciphertext = cipher.encrypt(b"Hello World")
    >>> plaintext  = RC4(b"MySecretKey").decrypt(ciphertext)
    >>> assert plaintext == b"Hello World"
    """

    def __init__(self, key: bytes) -> None:
        if not key:
            raise ValueError("RC4 key must be non-empty.")
        self._key = key
        self._S = self._ksa(key)

    #  Key Scheduling Algorithm 

    @staticmethod
    def _ksa(key: bytes) -> list[int]:
        """
        Key Scheduling Algorithm (KSA).

        Initialises the permutation array S[0..255] using the secret key.
        Time complexity: O(256)
        """
        S = list(range(256))
        j = 0
        key_len = len(key)
        for i in range(256):
            j = (j + S[i] + key[i % key_len]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    #  Pseudo-Random Generation Algorithm 

    def _prga(self, n_bytes: int) -> bytes:
        """
        Pseudo-Random Generation Algorithm (PRGA).

        Generates n_bytes of pseudorandom keystream from the internal state.
        Does NOT modify self._S (uses a working copy so the object is reusable).
        """
        S = self._S.copy()
        i = j = 0
        keystream = bytearray(n_bytes)
        for idx in range(n_bytes):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            keystream[idx] = S[(S[i] + S[j]) % 256]
        return bytes(keystream)

    #  Public API 

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt bytes by XOR-ing with the RC4 keystream.

        Parameters
        ----------
        data : bytes
            Plaintext (or ciphertext for decryption).

        Returns
        -------
        bytes
            Encrypted (or decrypted) output.
        """
        keystream = self._prga(len(data))
        return bytes(a ^ b for a, b in zip(data, keystream))

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt bytes (identical to encrypt -- RC4 is self-inverse)."""
        return self.encrypt(data)

    #  Bit-level helpers 

    def encrypt_bits(self, bits: np.ndarray) -> np.ndarray:
        """
        Encrypt a binary NumPy array (dtype uint8, values 0/1).

        The array is packed into bytes, RC4-encrypted, then unpacked back to bits.

        Parameters
        ----------
        bits : np.ndarray
            1-D array of 0s and 1s (length arbitrary).

        Returns
        -------
        np.ndarray
            Encrypted bit array of the same length.
        """
        n_bits = len(bits)
        n_bytes = (n_bits + 7) // 8

        # Pad to byte boundary and pack
        padded = np.zeros(n_bytes * 8, dtype=np.uint8)
        padded[:n_bits] = bits.astype(np.uint8)
        data_bytes = np.packbits(padded)

        # Encrypt
        enc_bytes = self.encrypt(bytes(data_bytes))

        # Unpack and return original length
        enc_bits = np.unpackbits(np.frombuffer(enc_bytes, dtype=np.uint8))
        return enc_bits[:n_bits]

    def decrypt_bits(self, bits: np.ndarray) -> np.ndarray:
        """Decrypt a binary NumPy array (symmetric with encrypt_bits)."""
        return self.encrypt_bits(bits)

    #  Image helpers 

    def encrypt_image(self, img_array: np.ndarray) -> np.ndarray:
        """
        Encrypt a NumPy image array (uint8, any shape).

        Parameters
        ----------
        img_array : np.ndarray
            Original image (H x W or H x W x C), dtype uint8.

        Returns
        -------
        np.ndarray
            Encrypted image of the same shape and dtype.
        """
        flat = img_array.flatten().tobytes()
        enc = self.encrypt(flat)
        return np.frombuffer(enc, dtype=np.uint8).reshape(img_array.shape)

    def decrypt_image(self, enc_array: np.ndarray) -> np.ndarray:
        """Decrypt a NumPy image array (symmetric with encrypt_image)."""
        return self.encrypt_image(enc_array)

    #  Dunder 

    def __repr__(self) -> str:
        return f"RC4(key_len={len(self._key)})"
