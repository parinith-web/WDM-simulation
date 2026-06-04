"""
main.py -- Command-line interface for the Secure WDM Optical Simulator.

Runs the full simulation pipeline and saves plots to ./outputs/.

Usage:
    python main.py [--length KM] [--encrypt] [--dcf] [--edfa] [--out DIR]

Examples:
    python main.py                            # baseline (no encryption)
    python main.py --encrypt                  # with RC4 encryption
    python main.py --encrypt --dcf --edfa     # with encryption + DCF + EDFA
    python main.py --all                      # run all 3 paper scenarios + sweep
"""

from __future__ import annotations
import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

from config import SystemConfig
from simulation.engine import SimulationEngine
from analysis.ber_analyzer import analytical_q, q_to_ber


#  Argument parser 

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Secure WDM Optical Communication Simulator (paper: OQE 2023 55:86)"
    )
    p.add_argument("--length",  type=float, default=77.0, help="Fiber length [km]")
    p.add_argument("--encrypt", action="store_true",      help="Enable RC4 encryption")
    p.add_argument("--dcf",     action="store_true",      help="Enable DCF")
    p.add_argument("--edfa",    action="store_true",      help="Enable EDFA")
    p.add_argument("--all",     action="store_true",      help="Run all 3 paper scenarios")
    p.add_argument("--bits",    type=int,   default=128,  help="Number of bits to simulate")
    p.add_argument("--out",     type=str,   default="./outputs", help="Output directory")
    p.add_argument("--seed",    type=int,   default=42,   help="RNG seed")
    return p.parse_args()


#  Plotting helpers 

def save_waveform_plot(result, out_dir: Path, filename: str) -> None:
    """Save a 2-panel waveform comparison (input vs encrypted)."""
    t = result.time_ns
    display_ns = min(4.0, t[-1])
    mask = t <= display_ns

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axes[0].plot(t[mask], result.nrz_signal[mask], color="#1565C0", lw=0.9)
    axes[0].set_ylabel("Amplitude (a.u.)")
    axes[0].set_title("(a) Input Message")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t[mask], result.encrypted_nrz[mask], color="#B71C1C", lw=0.9)
    axes[1].set_ylabel("Amplitude (a.u.)")
    axes[1].set_xlabel("Time (ns)")
    axes[1].set_title("(b) Encrypted Message -- RC4")
    axes[1].grid(True, alpha=0.3)

    fig.suptitle(
        f"{result.scenario}  |  L={result.time_ns[-1]/8:.0f} km  |  "
        f"Q={result.empirical_q:.2f}  |  BER={result.empirical_ber:.2e}",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_dir / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_dir / filename}")


def save_performance_sweep(engine: SimulationEngine, out_dir: Path) -> None:
    """Save Q-factor and BER vs distance plots for all 3 scenarios."""
    sweeps = engine.sweep_all_scenarios()
    distances = next(iter(sweeps.values())).distances_km
    wls = engine.config.wavelengths_nm
    colors = plt.cm.tab10(np.linspace(0, 0.8, len(wls)))

    SCENARIO_STYLE = {
        "no_encryption": ("Without Secure",        "-",  0.8),
        "encryption":    ("With Secure + EDFA",    "--", 0.8),
        "dcf_edfa":      ("Enc. + EDFA + DCF",     "-.", 0.8),
    }

    #  Q-factor figure 
    fig, ax = plt.subplots(figsize=(9, 6))
    for sc_name, sweep in sweeps.items():
        style = SCENARIO_STYLE[sc_name]
        for i, (wl, Q) in enumerate(sweep.q_per_channel.items()):
            ax.plot(distances, Q, linestyle=style[1], color=colors[i], lw=1.3, alpha=style[2],
                    label=f"{wl} nm" if sc_name == "no_encryption" else None)

    # Manual legend for scenarios
    from matplotlib.lines import Line2D
    sc_legend = [
        Line2D([0], [0], color="gray", ls=st[1], lw=2, label=st[0])
        for st in SCENARIO_STYLE.values()
    ]
    ax.legend(handles=sc_legend, loc="upper right", fontsize=9)
    ax.axhline(y=6, color="k", ls=":", lw=1.2, label="Q=6 threshold")
    ax.set_xlabel("Link Distance (km)"); ax.set_ylabel("Q-Factor")
    ax.set_title("Q-Factor vs Distance -- All Scenarios (8 WDM channels)")
    ax.set_xlim(0, 120); ax.set_ylim(0, 72)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = out_dir / "q_vs_distance.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")

    #  BER figure 
    fig, ax = plt.subplots(figsize=(9, 6))
    for sc_name, sweep in sweeps.items():
        style = SCENARIO_STYLE[sc_name]
        for i, (wl, BER) in enumerate(sweep.ber_per_channel.items()):
            ax.semilogy(distances, np.clip(BER, 1e-81, 1),
                        linestyle=style[1], color=colors[i], lw=1.3, alpha=style[2],
                        label=f"{wl} nm" if sc_name == "no_encryption" else None)

    ax.legend(handles=sc_legend, loc="upper right", fontsize=9)
    ax.axhline(y=1e-9, color="k", ls=":", lw=1.2, label="BER=10^-9")
    ax.set_xlabel("Link Distance (km)"); ax.set_ylabel("BER")
    ax.set_title("BER vs Distance -- All Scenarios (8 WDM channels)")
    ax.set_xlim(0, 120); ax.set_ylim(1e-81, 1)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    path = out_dir / "ber_vs_distance.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def print_summary(engine: SimulationEngine) -> None:
    """Print max link distances matching paper Table 2."""
    sweeps = engine.sweep_all_scenarios()
    cfg = engine.config
    print("\n" + "" * 55)
    print("  PERFORMANCE SUMMARY (paper Table 2 benchmark)")
    print("" * 55)
    print(f"  {'System':<30} {'Max Dist (km)':>12}  {'BL':>8}")
    print("" * 55)
    rows = [
        ("no_encryption", "Without Secure"),
        ("encryption",    "With Secure + EDFA"),
        ("dcf_edfa",      "With Secure + EDFA + DCF"),
    ]
    for sc, label in rows:
        sweep = sweeps[sc]
        # Average max distance across all channels
        avg_max = np.mean(list(sweep.max_distance_km.values()))
        bl = cfg.total_bitrate_gbps * avg_max
        print(f"  {label:<30} {avg_max:>12.1f}  {bl:>8.0f}")
    print("" * 55)
    print(f"  Paper benchmarks: 77.4 km / 63 km / 100 km")
    print("" * 55 + "\n")


#  Main 

def main() -> None:
    args = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "" * 60)
    print("  Secure WDM Optical Communication Simulator")
    print("  Based on: OQE (2023) 55:86 -- RC4 + WDM + SSMF")
    print("" * 60)

    cfg = SystemConfig(n_bits=args.bits, fiber_length_km=args.length)
    engine = SimulationEngine(cfg, seed=args.seed)

    t0 = time.time()

    if args.all:
        print("\n[1/3] Running all 3 paper scenarios...")
        configs = [
            (args.length, False, False, False, "scenario1_no_enc.png"),
            (args.length, True,  False, True,  "scenario2_enc_edfa.png"),
            (args.length, True,  True,  True,  "scenario3_enc_dcf_edfa.png"),
        ]
        for L, enc, dcf, edfa, fname in configs:
            print(f"  Running: L={L} km, enc={enc}, dcf={dcf}, edfa={edfa}")
            result = engine.run_waveform(L, use_encryption=enc, use_dcf=dcf, use_edfa=edfa)
            save_waveform_plot(result, out_dir, fname)
            print(f"  -> Q={result.empirical_q:.2f}  BER={result.empirical_ber:.2e}")

        print("\n[2/3] Generating performance sweep plots...")
        save_performance_sweep(engine, out_dir)

        print("\n[3/3] Summary:")
        print_summary(engine)

    else:
        print(f"\nRunning single simulation: L={args.length} km, "
              f"enc={args.encrypt}, dcf={args.dcf}, edfa={args.edfa}")
        result = engine.run_waveform(
            args.length,
            use_encryption=args.encrypt,
            use_dcf=args.dcf,
            use_edfa=args.edfa,
        )
        save_waveform_plot(result, out_dir, "waveform.png")
        save_performance_sweep(engine, out_dir)
        print_summary(engine)
        print(f"Result -> Q={result.empirical_q:.2f}  BER={result.empirical_ber:.2e}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.2f} s.  Outputs in: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
