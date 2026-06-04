"""
simulation/engine.py -- Main simulation pipeline.

Orchestrates the full end-to-end simulation:
  PRBS -> NRZ -> (RC4 encrypt) -> MZM -> SSMF -> (EDFA) -> (DCF) -> PIN -> Bessel -> 3R -> (RC4 decrypt)

Also provides the analytical sweep that generates Q-factor / BER vs distance
curves for all 8 WDM channels in each of the 3 scenarios from the paper.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Optional

from config import SystemConfig, DEFAULT_CONFIG
from encryption.rc4 import RC4
from signal_generation.prbs import generate_prbs
from signal_generation.nrz_pulse import nrz_pulse_shape, waveform_time_axis
from modulation.mzm import MachZehnderModulator
from fiber_channel.ssmf import SSMF
from fiber_channel.dcf import DCF
from fiber_channel.edfa import EDFA
from receiver.pin_photodiode import PINPhotodiode
from receiver.bessel_filter import BesselFilter, Regenerator3R
from analysis.ber_analyzer import (
    analytical_q, analytical_ber, empirical_q, count_ber, q_to_ber,
)


#  Result dataclasses 

@dataclass
class WaveformResult:
    """Time-domain waveform outputs from one simulation run."""
    time_ns: np.ndarray           # time axis [ns]
    bits_tx: np.ndarray           # original transmitted bits
    nrz_signal: np.ndarray        # NRZ electrical signal (normalised)
    encrypted_bits: np.ndarray    # RC4-encrypted bits (or same as bits_tx)
    encrypted_nrz: np.ndarray     # NRZ waveform of encrypted data
    optical_power_in: np.ndarray  # |E_in|^2 after MZM [mW]
    optical_power_out: np.ndarray # |E_out|^2 after fiber [mW]
    photocurrent: np.ndarray      # raw photocurrent [muA]
    filtered_signal: np.ndarray   # after Bessel filter [muA]
    bits_rx: np.ndarray           # recovered bits after decision
    bits_decrypted: np.ndarray    # decrypted bits (if encryption was on)
    empirical_q: float            # measured Q-factor
    empirical_ber: float          # measured BER
    scenario: str                 # scenario label


@dataclass
class PerformanceSweep:
    """Q-factor / BER vs distance for one scenario x all wavelengths."""
    scenario: str
    distances_km: np.ndarray
    q_per_channel: dict[float, np.ndarray]    # wl_nm -> Q array
    ber_per_channel: dict[float, np.ndarray]  # wl_nm -> BER array
    max_distance_km: dict[float, float]       # wl_nm -> max link distance


#  Engine 

class SimulationEngine:
    """
    End-to-end WDM-SSMF-RC4 optical communication simulator.

    Parameters
    ----------
    config : SystemConfig
        System parameters.
    seed : int | None
        RNG seed for reproducibility.
    """

    def __init__(
        self,
        config: SystemConfig = DEFAULT_CONFIG,
        seed: int | None = 42,
    ) -> None:
        self.config = config
        self._rng = np.random.default_rng(seed)

    #  Waveform simulation 

    def run_waveform(
        self,
        fiber_length_km: float = 50.0,
        wavelength_nm: float = 1550.0,
        use_encryption: bool = False,
        use_dcf: bool = False,
        use_edfa: bool = False,
        seed: Optional[int] = None,
    ) -> WaveformResult:
        """
        Run a single-channel time-domain simulation.

        Parameters
        ----------
        fiber_length_km : float
        wavelength_nm : float
        use_encryption : bool
        use_dcf : bool
        use_edfa : bool
        seed : int | None
            Per-run seed override.

        Returns
        -------
        WaveformResult
        """
        cfg = self.config.clone(
            fiber_length_km=fiber_length_km,
            encryption_enabled=use_encryption,
            dcf_enabled=use_dcf,
            edfa_enabled=use_edfa,
        )
        rng = np.random.default_rng(seed) if seed is not None else self._rng

        #  1. PRBS generation 
        bits_tx = generate_prbs(cfg.n_bits, order=15, seed=int(rng.integers(1_000_000)))

        #  2. RC4 encryption 
        if use_encryption:
            cipher = RC4(cfg.rc4_key)
            enc_bits = cipher.encrypt_bits(bits_tx.copy())
        else:
            enc_bits = bits_tx.copy()

        #  3. NRZ pulse shaping (Requirement #1) 
        # Use exact 0/1 levels and simple repeat for clear eye boundaries
        nrz_enc = np.repeat(enc_bits.astype(np.float64), cfg.samples_per_bit)
        nrz_orig = np.repeat(bits_tx.astype(np.float64), cfg.samples_per_bit)

        #  4. MZM modulation 
        mzm = MachZehnderModulator(cfg)
        E_tx = mzm.modulate(nrz_enc)

        #  5. SSMF propagation 
        ssmf = SSMF(fiber_length_km, wavelength_nm, cfg)
        E_after_ssmf = ssmf.propagate(E_tx, cfg.dt)

        #  6. DCF (optional) 
        if use_dcf:
            dcf = DCF(fiber_length_km, wavelength_nm, config=cfg)
            E_after_dcf = dcf.propagate(E_after_ssmf, cfg.dt)
        else:
            E_after_dcf = E_after_ssmf

        #  7. EDFA (optional) 
        if use_edfa:
            dcf_loss = dcf.total_loss_dB if use_dcf else 0
            total_loss_dB = ssmf.total_loss_dB + dcf_loss
            edfa = EDFA.from_fiber_loss(total_loss_dB, wavelength_nm, cfg, rng)
            E_rx = edfa.amplify(E_after_dcf, cfg.dt)
        else:
            E_rx = E_after_dcf

        #  7. Photodetection & Noise (Requirement #4 & #5) 
        pin = PINPhotodiode(cfg, rng)
        # Use clean detect then add controlled noise (Step 4)
        rx_signal_clean = pin.detect(E_rx, cfg.dt, add_noise=False)
        
        # Controlled Noise: std = 0.02 * mean(signal)
        noise_std = 0.02 * np.mean(rx_signal_clean)
        noise = rng.normal(0, noise_std, size=rx_signal_clean.shape)
        photocurrent = rx_signal_clean + noise

        #  10. Bessel filter 
        bf = BesselFilter(cfg)
        filtered = bf.filter(photocurrent)
        
        # Convert to muA ONLY for display/metrics if needed, but the paper 
        # often uses normalized units for eye diagrams.
        # Here we just keep the filtered signal.

        #  11. 3R regeneration & decision 
        regen = Regenerator3R(cfg)
        bits_rx = regen.regenerate(filtered)

        #  12. RC4 decryption 
        if use_encryption:
            decipher = RC4(cfg.rc4_key)
            bits_decrypted = decipher.decrypt_bits(bits_rx.copy())
        else:
            bits_decrypted = bits_rx.copy()

        #  12. Quality metrics 
        Q_emp = empirical_q(filtered, enc_bits, cfg)
        BER_emp = count_ber(enc_bits, bits_rx)

        #  Build result 
        t_ns = waveform_time_axis(cfg.n_bits, cfg) * 1e9  # [ns]

        P_in_mW  = np.abs(E_tx)   ** 2 * 1e3
        P_out_mW = np.abs(E_rx)   ** 2 * 1e3

        scenario_label = self._scenario_label(use_encryption, use_dcf, use_edfa)

        #  11. Final Scaling 
        # Ensure result is normalized for display (0.0 to 1.0 range)
        filtered = filtered / np.max(np.abs(filtered))

        return WaveformResult(
            time_ns=t_ns,
            bits_tx=bits_tx,
            nrz_signal=nrz_orig,
            encrypted_bits=enc_bits,
            encrypted_nrz=nrz_enc,
            optical_power_in=P_in_mW,
            optical_power_out=P_out_mW,
            photocurrent=photocurrent,
            filtered_signal=filtered,
            bits_rx=bits_rx,
            bits_decrypted=bits_decrypted,
            empirical_q=max(Q_emp, 0.0),
            empirical_ber=BER_emp,
            scenario=scenario_label,
        )

    #  Performance sweep (analytical model) 

    def sweep_performance(
        self,
        scenario: str = "no_encryption",
    ) -> PerformanceSweep:
        """
        Analytical Q-factor / BER sweep over distance for all 8 WDM channels.

        Uses the calibrated model in analysis.ber_analyzer that reproduces
        the paper's three benchmark distances (77.4, 63, 100 km).

        Parameters
        ----------
        scenario : str
            'no_encryption' | 'encryption' | 'dcf_edfa'

        Returns
        -------
        PerformanceSweep
        """
        cfg = self.config
        distances = np.linspace(
            cfg.distance_sweep_km_start,
            cfg.distance_sweep_km_stop,
            cfg.distance_sweep_points,
        )

        q_per_ch  = {}
        ber_per_ch = {}
        max_dist   = {}

        for wl in cfg.wavelengths_nm:
            Q   = analytical_q(distances, wl, scenario)
            BER = q_to_ber(Q)
            q_per_ch[wl]   = Q
            ber_per_ch[wl] = BER
            # Max distance = last distance where Q >= threshold
            valid = distances[Q >= cfg.q_threshold]
            max_dist[wl] = float(valid[-1]) if len(valid) > 0 else 0.0

        return PerformanceSweep(
            scenario=scenario,
            distances_km=distances,
            q_per_channel=q_per_ch,
            ber_per_channel=ber_per_ch,
            max_distance_km=max_dist,
        )

    def sweep_all_scenarios(self) -> dict[str, PerformanceSweep]:
        """Run sweep for all three paper scenarios."""
        return {
            s: self.sweep_performance(s)
            for s in ("no_encryption", "encryption", "dcf_edfa")
        }

    #  Helpers 

    @staticmethod
    def _scenario_label(
        enc: bool, dcf: bool, edfa: bool
    ) -> str:
        layers = []
        if enc:
            layers.append("Secure")
        if edfa:
            layers.append("EDFA")
        if dcf:
            layers.append("DCF")
        if not layers:
            return "Without Secure, EDFA, or DCF"
        return "With " + " + ".join(layers)
