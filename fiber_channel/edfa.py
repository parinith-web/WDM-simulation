"""
fiber_channel/edfa.py -- Erbium-Doped Fiber Amplifier (EDFA) model.

Paper parameters (Table 1):
  Noise Figure: 3 dB
  Noise Center Wavelength: 1550 nm
  Noise Bandwidth: 13 THz

The EDFA:
  1. Provides gain G to compensate the preceding fiber span's loss.
  2. Adds Amplified Spontaneous Emission (ASE) noise modelled as
     zero-mean complex Gaussian white noise with one-sided PSD:

       S_ASE = (G - 1)  nsp  h  

     where nsp = NFG/(2(G-1)) is the spontaneous emission factor.

Reference: Desurvire, "Erbium-Doped Fiber Amplifiers", Wiley 1994.
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG

H_PLANCK = 6.626e-34   # Planck constant [Js]
C_LIGHT   = 2.998e8    # Speed of light [m/s]


class EDFA:
    """
    EDFA model: ideal gain + ASE noise injection.

    The gain is set to exactly compensate the accumulated fiber loss so that
    the signal power at the EDFA output equals the launch power.
    """

    def __init__(
        self,
        gain_dB: float,
        wavelength_nm: float = 1550.0,
        config: SystemConfig = DEFAULT_CONFIG,
        rng: np.random.Generator | None = None,
    ) -> None:
        """
        Parameters
        ----------
        gain_dB : float
            Amplifier gain [dB].
        wavelength_nm : float
            Signal centre wavelength [nm].
        config : SystemConfig
            System configuration (NF, noise bandwidth).
        rng : np.random.Generator | None
            Random number generator (for reproducibility).
        """
        self.config = config
        self.wavelength_nm = wavelength_nm
        self.rng = rng if rng is not None else np.random.default_rng()

        #  Gain 
        self.gain_dB = gain_dB
        self.G = 10 ** (gain_dB / 10)              # linear gain

        #  ASE noise parameters 
        NF = 10 ** (config.edfa_nf_db / 10)       # linear noise figure
        nu = C_LIGHT / (wavelength_nm * 1e-9)      # optical frequency [Hz]
        # Spontaneous emission factor
        if self.G > 1:
            nsp = NF * self.G / (2 * (self.G - 1))
        else:
            nsp = 1.0

        # One-sided ASE PSD per polarisation [W/Hz]
        self.S_ASE = nsp * H_PLANCK * nu * (self.G - 1)

        # Noise bandwidth [Hz]
        self.noise_BW_Hz = config.edfa_noise_bandwidth_THz * 1e12

    @classmethod
    def from_fiber_loss(
        cls,
        fiber_loss_dB: float,
        wavelength_nm: float = 1550.0,
        config: SystemConfig = DEFAULT_CONFIG,
        rng: np.random.Generator | None = None,
    ) -> "EDFA":
        """
        Create an EDFA that exactly compensates a given fiber loss.

        Parameters
        ----------
        fiber_loss_dB : float
            Fiber span loss [dB] (positive value).
        """
        return cls(
            gain_dB=fiber_loss_dB,
            wavelength_nm=wavelength_nm,
            config=config,
            rng=rng,
        )

    def amplify(self, E_in: np.ndarray, dt_s: float) -> np.ndarray:
        """
        Amplify the optical field and add ASE noise.

        Parameters
        ----------
        E_in : np.ndarray
            Input complex optical field [sqrt(W)].
        dt_s : float
            Sample period [s].

        Returns
        -------
        np.ndarray
            Amplified field + ASE noise, same shape as E_in.
        """
        N = len(E_in)

        #  Signal amplification 
        E_out = np.sqrt(self.G) * E_in

        #  ASE noise (complex Gaussian) 
        # Noise variance per sample: 2 = S_ASE / dt_s
        # (both polarisations -> multiply by 2)
        noise_var = 2 * self.S_ASE / dt_s
        noise_std = np.sqrt(noise_var / 2)   # per real/imag component

        noise = noise_std * (
            self.rng.standard_normal(N) + 1j * self.rng.standard_normal(N)
        )
        return E_out + noise

    @property
    def noise_figure_dB(self) -> float:
        """EDFA noise figure [dB]."""
        return self.config.edfa_nf_db

    @property
    def output_ASE_power_dBm(self) -> float:
        """Total output ASE power within the noise bandwidth [dBm]."""
        P_ASE = 2 * self.S_ASE * self.noise_BW_Hz   # both polarisations
        return 10 * np.log10(P_ASE * 1e3 + 1e-30)

    def __repr__(self) -> str:
        return (
            f"EDFA(G={self.gain_dB:.1f} dB, NF={self.config.edfa_nf_db} dB, "
            f"Lambda={self.wavelength_nm} nm)"
        )
