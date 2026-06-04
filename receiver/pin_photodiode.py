"""
receiver/pin_photodiode.py -- PIN photodiode model.

Paper parameters (Table 1):
  Dark current  : 10 nA
  Responsivity  : 1 A/W
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG


class PINPhotodiode:
    """
    Ideal PIN photodiode with shot noise and dark current.

    Converts optical power to photocurrent and adds detection noise.
    """

    def __init__(
        self,
        config: SystemConfig = DEFAULT_CONFIG,
        rng: np.random.Generator | None = None,
    ) -> None:
        self.config = config
        self.rng = rng if rng is not None else np.random.default_rng()

        # Physical constants
        self._q = 1.602e-19      # electron charge [C]
        self._kB = 1.38e-23      # Boltzmann constant [J/K]
        self._T = 300.0          # temperature [K]

    def detect(self, E_field: np.ndarray, dt_s: float, add_noise: bool = True) -> np.ndarray:
        """
        Detect optical field and return photocurrent.

        Parameters
        ----------
        E_field : np.ndarray
            Complex optical field [sqrt(W)].
        dt_s : float
            Sample period [s].
        add_noise : bool
            Whether to add shot and thermal noise.

        Returns
        -------
        np.ndarray
            Photocurrent [A].
        """
        #  Signal photocurrent 
        P_opt = np.abs(E_field) ** 2                              # [W]
        I_signal = self.config.responsivity * P_opt               # [A]
        I_dark = self.config.dark_current_nA * 1e-9              # [A]

        if not add_noise:
            return I_signal + I_dark

        #  Noise bandwidths 
        BW = self.config.bessel_cutoff_Hz

        # Shot noise variance (signal + dark current)
        var_shot = 2 * self._q * (I_signal + I_dark) * BW

        # Thermal noise (Johnson-Nyquist)
        var_thermal = 4 * self._kB * self._T * BW / self.config.load_resistance_ohm

        # Total noise std per sample
        noise_std = np.sqrt(var_shot + var_thermal)

        #  Noisy photocurrent 
        noise = noise_std * self.rng.standard_normal(len(E_field))
        return I_signal + I_dark + noise

