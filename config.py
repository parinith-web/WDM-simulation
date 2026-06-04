"""
config.py -- System configuration for the Secure WDM Optical Communication Simulator.

All parameter values are taken directly from the paper:
  "Design and implementation of cipher algorithm based secure optical communication system"
  Optical and Quantum Electronics (2023) 55:86
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class SystemConfig:
    """
    Complete system parameters for the WDM-SSMF-RC4 optical link.
    """

    # -- Simulation resolution ---------------------------------------------
    n_bits: int = 128           # Number of bits to simulate per channel
    samples_per_bit: int = 64   # Oversampling factor (fs >= 64 * Rb)

    # -- Transmitter -------------------------------------------------------
    bitrate_per_channel: float = 10e9          # 10 Gbps per channel (paper 2)
    n_channels: int = 8                        # 8 WDM channels
    wavelengths_nm: List[float] = field(
        default_factory=lambda: [
            1550.0, 1550.4, 1550.8, 1551.2,
            1551.6, 1552.0, 1552.4, 1552.8,
        ]
    )
    P_tx_dBm: float = 10.0                     # CW laser power (paper Table 1)
    laser_linewidth_Hz: float = 10e6           # 10 MHz linewidth
    mzm_extinction_ratio_dB: float = 30.0      # MZM ER (paper Table 1)
    nrz_rise_time_factor: float = 0.05         # rise/fall = 0.05 * T_bit (paper Table 1)
    nrz_fall_time_factor: float = 0.05

    # -- Standard Single-Mode Fiber (SSMF) --------------------------------
    alpha_db_per_km: float = 0.2               # Attenuation (paper Table 1)
    D_ssmf_ps_nm_km: float = 16.75            # Dispersion constant (paper Table 1)
    reference_wavelength_nm: float = 1550.0
    fiber_length_km: float = 100.0             # Simulation distance (sweep 1-120 km)

    # -- Dispersion Compensation Fiber (DCF) ------------------------------
    D_dcf_ps_nm_km: float = -85.0             # DCF dispersion (paper Table 1)
    dcf_alpha_db_per_km: float = 0.5          # DCF attenuation (typical)
    dcf_enabled: bool = False

    # -- EDFA -------------------------------------------------------------
    edfa_nf_db: float = 3.0                    # Noise figure (paper Table 1)
    edfa_noise_center_wavelength_nm: float = 1550.0
    edfa_noise_bandwidth_THz: float = 13.0
    edfa_enabled: bool = False

    # -- Receiver ---------------------------------------------------------
    responsivity: float = 1.0                  # A/W (PIN, paper Table 1)
    dark_current_nA: float = 10.0              # 10 nA (paper Table 1)
    bessel_order: int = 5
    bessel_cutoff_factor: float = 0.75         # f_cutoff = 0.75 x bitrate (paper Table 1)
    load_resistance_ohm: float = 50.0

    # -- RC4 Encryption ---------------------------------------------------
    encryption_enabled: bool = False
    rc4_key: bytes = b"SecureOpticalKey2023"

    # -- Analysis Thresholds ----------------------------------------------
    q_threshold: float = 6.0       # Q=6 <-> BER=10^-9 (ITU threshold)
    ber_threshold: float = 1e-9

    # -- Sweep ------------------------------------------------------------
    distance_sweep_km_start: float = 1.0
    distance_sweep_km_stop: float = 120.0
    distance_sweep_points: int = 120

    # -- Properties -------------------------------------------------------
    @property
    def T_bit(self) -> float:
        """Bit period [s]."""
        return 1.0 / self.bitrate_per_channel

    @property
    def sample_rate(self) -> float:
        """Sample rate [Hz]."""
        return self.bitrate_per_channel * self.samples_per_bit

    @property
    def dt(self) -> float:
        """Time step [s]."""
        return 1.0 / self.sample_rate

    @property
    def total_samples(self) -> int:
        """Total samples for one simulation frame."""
        return self.n_bits * self.samples_per_bit

    @property
    def total_bitrate_gbps(self) -> float:
        """Total WDM bitrate [Gbps]."""
        return self.bitrate_per_channel * self.n_channels / 1e9

    @property
    def bessel_cutoff_Hz(self) -> float:
        """Bessel filter cutoff frequency [Hz]."""
        return self.bessel_cutoff_factor * self.bitrate_per_channel

    @property
    def P_tx_W(self) -> float:
        """Transmit power [W]."""
        return 10 ** (self.P_tx_dBm / 10) * 1e-3

    def dcf_length_for_full_compensation(self, fiber_length_km: float) -> float:
        """DCF length [km] required to fully compensate SSMF dispersion."""
        return self.D_ssmf_ps_nm_km * fiber_length_km / (-self.D_dcf_ps_nm_km)

    def clone(self, **overrides) -> "SystemConfig":
        """Return a copy of this config with selected fields overridden."""
        import copy
        obj = copy.deepcopy(self)
        for k, v in overrides.items():
            setattr(obj, k, v)
        return obj


# -- Default configuration (paper baseline) --------------------------------
DEFAULT_CONFIG = SystemConfig()
