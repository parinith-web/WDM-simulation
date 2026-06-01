"""
signal_generation/prbs.py -- Pseudo-Random Bit Sequence (PRBS) generator.

Implements a maximal-length LFSR sequence (PRBS-31 by default) used as the
test pattern for the 10 Gbps per-channel data stream described in the paper.
"""

from __future__ import annotations
import numpy as np
from typing import Optional


class PRBSGenerator:
    """
    Linear Feedback Shift Register (LFSR) based PRBS generator.

    Standard PRBS polynomials
    -------------------------
    PRBS-7  : x^7  + x^6  + 1   -> period 127
    PRBS-15 : x^15 + x^14 + 1   -> period 32 767
    PRBS-23 : x^23 + x^22 + 1   -> period ~8 M
    PRBS-31 : x^31 + x^30 + 1   -> period ~2 G  (default)
    """

    _TAPS: dict[int, tuple[int, ...]] = {
        7:  (7, 6),
        15: (15, 14),
        23: (23, 22),
        31: (31, 30),
    }

    def __init__(self, order: int = 31, seed: Optional[int] = None) -> None:
        """
        Parameters
        ----------
        order : int
            PRBS order (7, 15, 23, or 31).
        seed : int | None
            Initial LFSR state.  Defaults to 2^order - 1 (all-ones).
        """
        if order not in self._TAPS:
            raise ValueError(f"Unsupported PRBS order {order}. Choose from {list(self._TAPS)}")
        self.order = order
        self._taps = self._TAPS[order]
        self._state = (1 << order) - 1 if seed is None else int(seed) & ((1 << order) - 1)
        if self._state == 0:
            self._state = 1  # zero state is forbidden in LFSR

    def _clock(self) -> int:
        """Clock the LFSR once and return the output bit (LSB of state)."""
        # XOR tapped positions (1-indexed, MSB = position order)
        feedback = 0
        for tap in self._taps:
            feedback ^= (self._state >> (tap - 1)) & 1
        self._state = ((self._state >> 1) | (feedback << (self.order - 1))) & ((1 << self.order) - 1)
        return self._state & 1

    def generate(self, n_bits: int) -> np.ndarray:
        """
        Generate n_bits of PRBS sequence.

        Returns
        -------
        np.ndarray
            uint8 array of 0s and 1s, length n_bits.
        """
        bits = np.empty(n_bits, dtype=np.uint8)
        for i in range(n_bits):
            bits[i] = self._clock()
        return bits

    def reset(self, seed: Optional[int] = None) -> None:
        """Reset the LFSR to a given seed (or all-ones if None)."""
        self._state = (1 << self.order) - 1 if seed is None else int(seed) & ((1 << self.order) - 1)
        if self._state == 0:
            self._state = 1


def generate_prbs(n_bits: int, order: int = 31, seed: Optional[int] = None) -> np.ndarray:
    """Convenience wrapper -- generate n_bits of PRBS sequence."""
    return PRBSGenerator(order=order, seed=seed).generate(n_bits)
