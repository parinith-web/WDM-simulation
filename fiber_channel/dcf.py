"""
fiber_channel/dcf.py -- Dispersion Compensation Fiber (DCF) model.

Paper parameters (Table 1):
  D_dcf  = -85 ps/(nmkm)
  Length : 0.15 km to 18.2 km (chosen to compensate SSMF dispersion)
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG

C_LIGHT_NM_PS = 2.998e5


class DCF:
    """
    Dispersion Compensation Fiber -- negative dispersion to cancel SSMF ISI.

    The DCF length is chosen so that:
        D_ssmf x L_ssmf + D_dcf x L_dcf = 0  (full compensation)

    In practice, slight under-/over-compensation leaves a small residual.
    """

    def __init__(
        self,
        ssmf_length_km: float,
        wavelength_nm: float = 1550.0,
        compensation_ratio: float = 1.0,   # 1.0 = full compensation
        config: SystemConfig = DEFAULT_CONFIG,
    ) -> None:
        """
        Parameters
        ----------
        ssmf_length_km : float
            Length of the SSMF span being compensated.
        wavelength_nm : float
            Channel centre wavelength [nm].
        compensation_ratio : float
            Fraction of SSMF dispersion to compensate (1.0 = full).
        config : SystemConfig
            System configuration.
        """
        self.config = config
        self.wavelength_nm = wavelength_nm

        # Required DCF length
        D_ssmf = config.D_ssmf_ps_nm_km          # ps/nm/km  (positive)
        D_dcf  = config.D_dcf_ps_nm_km            # ps/nm/km  (negative)
        self.length_km = min(
            -D_ssmf * ssmf_length_km * compensation_ratio / D_dcf,
            18.2,   # max DCF length from paper Table 1
        )

        # Power attenuation
        self.alpha_per_km = config.dcf_alpha_db_per_km / (10 / np.log(10))  # Np/km

        #  for DCF
        lam = wavelength_nm
        self.beta2_ps2_per_km = -D_dcf * (lam ** 2) / (2 * np.pi * C_LIGHT_NM_PS)

    def propagate(self, E_in: np.ndarray, dt_s: float) -> np.ndarray:
        """Propagate complex optical field through the DCF."""
        N = len(E_in)
        dt_ps = dt_s * 1e12
        freq = np.fft.fftfreq(N, d=dt_ps)
        omega = 2 * np.pi * freq

        alpha_amp = self.alpha_per_km * self.length_km
        disp_phase = 0.5 * self.beta2_ps2_per_km * self.length_km * omega ** 2

        H = np.exp(-alpha_amp) * np.exp(1j * disp_phase)
        return np.fft.ifft(np.fft.fft(E_in) * H)

    @property
    def total_loss_dB(self) -> float:
        return self.config.dcf_alpha_db_per_km * self.length_km

    @property
    def residual_dispersion_ps_per_nm(self) -> float:
        """Residual dispersion after combining SSMF + DCF [ps/nm]."""
        return (
            self.config.D_ssmf_ps_nm_km * (self.config.fiber_length_km)
            + self.config.D_dcf_ps_nm_km * self.length_km
        )

    def __repr__(self) -> str:
        return (
            f"DCF(L={self.length_km:.2f} km, "
            f"D={self.config.D_dcf_ps_nm_km} ps/nm/km)"
        )
