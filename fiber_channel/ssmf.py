"""
fiber_channel/ssmf.py -- Standard Single-Mode Fiber (SSMF) propagation model.

Implements linear fiber propagation using the frequency-domain transfer function:

    H() = exp(-/2  L)  exp(j  /2  2  L)

where:
     = power attenuation coefficient [1/m]
    = group velocity dispersion [s2/m]  (derived from D)
  L   = fiber length [m]

Paper parameters (Table 1):
   = 0.2 dB/km
  D = 16.75 ps/(nmkm)
  Reference wavelength: 1550 nm
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG


# Physical constants
C_LIGHT = 2.998e8          # Speed of light [m/s]
C_LIGHT_NM_PS = 2.998e5   # Speed of light [nm/ps]


class SSMF:
    """
    Standard Single-Mode Fiber propagation (linear, single-polarisation).

    Uses the split-step approximation with only linear effects (attenuation +
    group-velocity dispersion).  Non-linear effects (SPM, XPM) are neglected
    consistent with the paper's OptiSystem setup for moderate launch powers.
    """

    def __init__(
        self,
        length_km: float,
        wavelength_nm: float = 1550.0,
        config: SystemConfig = DEFAULT_CONFIG,
    ) -> None:
        """
        Parameters
        ----------
        length_km : float
            Fiber span length [km].
        wavelength_nm : float
            Channel centre wavelength [nm].
        config : SystemConfig
            System configuration (, D values).
        """
        self.length_km = length_km
        self.wavelength_nm = wavelength_nm
        self.config = config

        #  Derived parameters 
        # Power attenuation coefficient [1/km]
        alpha_db = config.alpha_db_per_km
        self.alpha_per_km = alpha_db / (10 / np.log(10))   # Np/km

        # Group velocity dispersion  from D
        # D [ps/nm/km] ->  [ps2/km]
        #  = -D  Lambda2 / (2c)   (Lambda in nm, c in nm/ps)
        lam = wavelength_nm  # nm
        D = config.D_ssmf_ps_nm_km   # ps/nm/km
        self.beta2_ps2_per_km = -D * (lam ** 2) / (2 * np.pi * C_LIGHT_NM_PS)  # ps2/km

        # Total accumulated dispersion [ps2]
        self.total_D_ps2 = self.beta2_ps2_per_km * length_km

    def propagate(self, E_in: np.ndarray, dt_s: float) -> np.ndarray:
        """
        Propagate complex optical field through the fiber.

        Parameters
        ----------
        E_in : np.ndarray
            Input optical field envelope E(t) [sqrt(W)], complex128.
        dt_s : float
            Sample period [s].

        Returns
        -------
        np.ndarray
            Output optical field E(t) after propagation, same shape as E_in.
        """
        N = len(E_in)
        dt_ps = dt_s * 1e12   # convert to ps

        #  Frequency axis [rad/ps] 
        # fftfreq gives cycles/sample -> convert to rad/ps
        freq_cycles_per_ps = np.fft.fftfreq(N, d=dt_ps)  # cycles/ps
        omega = 2 * np.pi * freq_cycles_per_ps             # rad/ps

        #  Transfer function 
        # H() = exp(-/2  L)  exp(j  /2  2  L)
        alpha_amplitude = self.alpha_per_km * self.length_km   # total amplitude attenuation
        dispersion_phase = 0.5 * self.beta2_ps2_per_km * self.length_km * omega ** 2

        H = np.exp(-alpha_amplitude) * np.exp(1j * dispersion_phase)

        #  Apply transfer function 
        E_out = np.fft.ifft(np.fft.fft(E_in) * H)
        return E_out

    @property
    def total_loss_dB(self) -> float:
        """Total optical power loss [dB]."""
        return self.config.alpha_db_per_km * self.length_km

    @property
    def dispersion_ps_per_nm(self) -> float:
        """Total accumulated dispersion [ps/nm] for this span."""
        return self.config.D_ssmf_ps_nm_km * self.length_km

    def __repr__(self) -> str:
        return (
            f"SSMF(L={self.length_km} km, Lambda={self.wavelength_nm} nm, "
            f"={self.config.alpha_db_per_km} dB/km, "
            f"D={self.config.D_ssmf_ps_nm_km} ps/nm/km)"
        )
