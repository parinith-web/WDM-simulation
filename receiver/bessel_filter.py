"""
receiver/bessel_filter.py -- Low-pass Bessel filter.

Paper parameters (Table 1):
  Order : 5 (standard choice for optical receivers)
  Cutoff: 0.75 x bit rate = 7.5 GHz for 10 Gbps

A Bessel filter is chosen because it has maximally flat group delay,
which minimises pulse distortion -- critical for NRZ receivers.
"""

from __future__ import annotations
import numpy as np
from scipy.signal import bessel, sosfilt, besselap, bilinear_zpk, zpk2sos
from config import SystemConfig, DEFAULT_CONFIG


class BesselFilter:
    """
    Analogue-prototype Bessel low-pass filter, discretised at the sample rate.
    """

    def __init__(self, config: SystemConfig = DEFAULT_CONFIG) -> None:
        self.config = config
        self._build_filter()

    def _build_filter(self) -> None:
        """Compute coefficients for the discrete Bessel filter."""
        # Use order 4 as specified in the user's required fixes
        order = 4
        fs = self.config.sample_rate
        fc = self.config.bessel_cutoff_Hz

        from scipy.signal import bessel as _bessel
        # Use (b, a) for filtfilt
        self._b, self._a = _bessel(
            order,
            Wn=fc,
            btype="low",
            analog=False,
            fs=fs,
            output="ba",
        )

    def filter(self, signal: np.ndarray) -> np.ndarray:
        """
        Apply the Bessel filter to a signal using zero-phase filtfilt.
        """
        from scipy.signal import filtfilt as _filtfilt
        return _filtfilt(self._b, self._a, signal)

    def __repr__(self) -> str:
        return (
            f"BesselFilter(order={self.config.bessel_order}, "
            f"fc={self.config.bessel_cutoff_Hz / 1e9:.2f} GHz)"
        )


# 


"""
receiver/regenerator.py -- 3R (Re-amplify, Re-shape, Re-time) regenerator.

The 3R regenerator in the paper is modelled as an ideal decision device:
  - Threshold detection at mid-point between '0' and '1' levels.
  - Sampling at the optimal eye opening instant.
"""


class Regenerator3R:
    """
    Ideal 3R regenerator / decision circuit.

    Samples the filtered photocurrent at the centre of each bit period,
    applies a threshold decision, and outputs regenerated bits.
    """

    def __init__(self, config: SystemConfig = DEFAULT_CONFIG) -> None:
        self.config = config

    def regenerate(
        self,
        filtered_signal: np.ndarray,
        threshold: float | None = None,
    ) -> np.ndarray:
        """
        Decision-based bit recovery.

        Parameters
        ----------
        filtered_signal : np.ndarray
            Filtered photocurrent waveform.
        threshold : float | None
            Decision threshold.  If None, uses mid-swing of the signal.

        Returns
        -------
        np.ndarray
            Recovered bit sequence (uint8 array of 0s and 1s).
        """
        spb = self.config.samples_per_bit

        #  Sample at the centre of each bit period 
        n_bits = len(filtered_signal) // spb
        sample_idx = np.arange(n_bits) * spb + spb // 2
        samples = filtered_signal[sample_idx]

        #  Decision threshold 
        if threshold is None:
            threshold = (samples.max() + samples.min()) / 2.0

        return (samples >= threshold).astype(np.uint8)

    def optimal_threshold(self, filtered_signal: np.ndarray) -> float:
        """
        Compute the optimal decision threshold that minimises BER.

        Uses a Gaussian approximation for '0' and '1' distributions.
        """
        spb = self.config.samples_per_bit
        n_bits = len(filtered_signal) // spb
        sample_idx = np.arange(n_bits) * spb + spb // 2
        samples = filtered_signal[sample_idx]

        # Separate samples into two clusters (simple k-means style)
        med = np.median(samples)
        I1 = samples[samples > med]
        I0 = samples[samples <= med]

        if len(I1) == 0 or len(I0) == 0:
            return float(med)

        mu1, sig1 = float(I1.mean()), float(I1.std() + 1e-30)
        mu0, sig0 = float(I0.mean()), float(I0.std() + 1e-30)

        # Optimal threshold for equal-probability symbols
        thresh = (mu1 * sig0 + mu0 * sig1) / (sig0 + sig1)
        return float(thresh)
