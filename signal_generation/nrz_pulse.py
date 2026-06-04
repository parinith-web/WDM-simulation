"""
signal_generation/nrz_pulse.py -- Non-Return-to-Zero (NRZ) pulse shaper.

Converts a binary bit sequence into a continuous-time NRZ electrical waveform
with finite rise/fall times, as described in Table 1 of the paper:

  Rectangle shape: exponential
  Bias: 0 a.u.
  Rise time: 0.05 bit
  Fall time: 0.05 bit
  Amplitude: 1 a.u.
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG


def nrz_pulse_shape(
    bits: np.ndarray,
    config: SystemConfig = DEFAULT_CONFIG,
    amplitude_high: float = 1.0,
    amplitude_low: float = 0.0,
) -> np.ndarray:
    """
    Convert a bit sequence into an oversampled NRZ waveform.

    A raised-cosine edge filter is applied with the rise/fall times from
    the paper (0.05 x T_bit for both rise and fall).

    Parameters
    ----------
    bits : np.ndarray
        Binary array (0/1), dtype uint8 or float.
    config : SystemConfig
        System configuration (determines samples_per_bit and rise/fall times).
    amplitude_high : float
        Voltage level for bit-'1'.
    amplitude_low : float
        Voltage level for bit-'0'.

    Returns
    -------
    np.ndarray
        Float64 waveform of length len(bits) x samples_per_bit.
    """
    spb = config.samples_per_bit
    n_bits = len(bits)
    total_samples = n_bits * spb

    #  Step 1: upsample (hold each bit value for spb samples) 
    waveform = np.repeat(
        bits.astype(np.float64) * (amplitude_high - amplitude_low) + amplitude_low,
        spb,
    )

    #  Step 2: apply raised-cosine edge smoothing 
    # Rise/fall time in samples
    rise_samples = max(1, int(config.nrz_rise_time_factor * spb))

    # Build a smoothing kernel of length 2*rise_samples + 1
    t = np.linspace(-1, 1, 2 * rise_samples + 1)
    kernel = 0.5 * (1 + np.cos(np.pi * t))
    kernel /= kernel.sum()

    waveform = np.convolve(waveform, kernel, mode="same")

    return waveform


def waveform_time_axis(n_bits: int, config: SystemConfig = DEFAULT_CONFIG) -> np.ndarray:
    """
    Return the time axis [seconds] for an NRZ waveform.

    Parameters
    ----------
    n_bits : int
        Number of bits.
    config : SystemConfig
        System configuration.

    Returns
    -------
    np.ndarray
        Time axis of length n_bits x samples_per_bit.
    """
    total_samples = n_bits * config.samples_per_bit
    return np.arange(total_samples) * config.dt
