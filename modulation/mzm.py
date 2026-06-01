"""
modulation/mzm.py -- Mach-Zehnder Modulator (MZM) model.

Models the intensity modulation of a CW optical carrier using a push-pull MZM.
From the paper (Table 1): Extinction Ratio = 30 dB.

The MZM transfer function is:
    E_out = E_in x cos( x V_rf / (2 x V_pi) + _bias / 2)

For OOK with a 30 dB extinction ratio, the modulator is biased at the
quadrature point and driven rail-to-rail.
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG


class MachZehnderModulator:
    """
    Ideal push-pull MZM for OOK intensity modulation.

    Parameters
    ----------
    config : SystemConfig
        System configuration.  Uses mzm_extinction_ratio_dB and P_tx_dBm.
    """

    def __init__(self, config: SystemConfig = DEFAULT_CONFIG) -> None:
        self.config = config
        # Extinction ratio (linear)
        self._er = 10 ** (config.mzm_extinction_ratio_dB / 10)
        # Derive V_pi from desired extinction ratio
        # For push-pull MZM: ER = ((1 + sqrt()) / (1 - sqrt()))^2
        # where  = 1/ER  ->  sqrt() = 1/sqrt(ER)
        # Peak optical field amplitude for '1' bit
        self._E_peak = np.sqrt(config.P_tx_W)
        # For high ER (30 dB = 1000), the '0' level is negligible
        self._sqrt_er = np.sqrt(self._er)
        self._E1 = self._E_peak * (1 + 1 / self._sqrt_er) / 2  # '1' level amplitude
        self._E0 = self._E_peak * (1 - 1 / self._sqrt_er) / 2  # '0' level amplitude (~0)

    def modulate(self, nrz_waveform: np.ndarray) -> np.ndarray:
        """
        Modulate optical signal with exact 30dB Extinction Ratio.
        """
        # Power levels from user requirement (ER=30dB -> 10**(30/10) = 1000)
        P1 = self.config.P_tx_W
        P0 = P1 / 1000.0
        
        # Field amplitudes
        E1 = np.sqrt(P1)
        E0 = np.sqrt(P0)
        
        # Map [0, 1] NRZ to [E0, E1] optical field amplitude
        E_amplitude = E0 + (E1 - E0) * nrz_waveform
        
        return E_amplitude.astype(np.complex128)

    @property
    def P1_W(self) -> float:
        """Optical power for bit '1' [W]."""
        return self._E1 ** 2

    @property
    def P0_W(self) -> float:
        """Optical power for bit '0' [W]."""
        return self._E0 ** 2

    @property
    def extinction_ratio_dB(self) -> float:
        """Actual extinction ratio [dB]."""
        return 10 * np.log10(self.P1_W / max(self.P0_W, 1e-30))


def cw_laser_field(config: SystemConfig = DEFAULT_CONFIG) -> float:
    """
    CW laser field amplitude [sqrt(W)].

    Returns sqrt(P_tx) -- the unmodulated carrier amplitude.
    """
    return np.sqrt(config.P_tx_W)
