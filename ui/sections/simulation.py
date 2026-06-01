from __future__ import annotations

import numpy as np
import streamlit as st
from PIL import Image

from config import SystemConfig
from encryption.rc4 import RC4
from simulation.engine import SimulationEngine
from ui.charts import SCENARIO_META, plot_ber, plot_eye_grid, plot_q_factor, plot_single_scenario, plot_waveforms
from ui.components import metric_cards, signal_flow, status_chips, system_params_table
from ui.components.html import html_block


def _build_config() -> tuple[SystemConfig, dict]:
    cols = st.columns([1, 1, 1], gap="xlarge")
    with cols[0]:
        fiber_length = st.slider("Fiber length (km)", 1, 120, 77, step=1)
        n_bits = st.select_slider("Bits to transmit", [64, 128, 256, 512], value=128)
    with cols[1]:
        n_channels = st.selectbox("WDM channels", [1, 2, 4, 8], index=3)
        bitrate_gbps = st.selectbox("Rate / channel (Gbps)", [1.0, 2.5, 10.0, 40.0], index=2)
    with cols[2]:
        st.markdown('<div style="height:56px"></div>', unsafe_allow_html=True)
        use_encryption = st.toggle("RC4 Encryption", value=True)

        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        use_edfa = st.toggle("EDFA Amplification", value=True)

        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        use_dcf = st.toggle("DCF Compensation", value=True)

    with st.expander("Advanced transmitter parameters", expanded=False):
        with st.container(key="adv_tx_params"):
            p_col, er_col = st.columns(2)
            with p_col:
                p_tx_dbm = st.slider("Launch power (dBm)", 0, 20, 10)
            with er_col:
                mzm_er = st.slider("MZM extinction ratio (dB)", 10, 40, 30)

    cfg = SystemConfig(
        n_bits=int(n_bits),
        fiber_length_km=float(fiber_length),
        bitrate_per_channel=float(bitrate_gbps) * 1e9,
        n_channels=int(n_channels),
        wavelengths_nm=[1550.0 + i * 0.4 for i in range(int(n_channels))],
        P_tx_dBm=float(p_tx_dbm),
        mzm_extinction_ratio_dB=float(mzm_er),
        encryption_enabled=bool(use_encryption),
        dcf_enabled=bool(use_dcf),
        edfa_enabled=bool(use_edfa),
        rc4_key=b"SecureOpticalKey2023",
    )
    return cfg, {
        "fiber_length": float(fiber_length),
        "use_encryption": bool(use_encryption),
        "use_edfa": bool(use_edfa),
        "use_dcf": bool(use_dcf),
    }


def _run_active(cfg: SystemConfig, options: dict) -> None:
    engine = SimulationEngine(cfg, seed=42)
    st.session_state.active_result = engine.run_waveform(
        fiber_length_km=options["fiber_length"],
        wavelength_nm=1550.0,
        use_encryption=options["use_encryption"],
        use_dcf=options["use_dcf"],
        use_edfa=options["use_edfa"],
    )
    st.session_state.active_cfg = cfg


def _run_benchmarks(cfg: SystemConfig, fiber_length: float) -> None:
    engine = SimulationEngine(cfg, seed=42)
    st.session_state.benchmark_results = [
        engine.run_waveform(fiber_length, wavelength_nm=1550.0, use_encryption=False, use_dcf=False, use_edfa=False),
        engine.run_waveform(fiber_length, wavelength_nm=1550.0, use_encryption=True, use_dcf=False, use_edfa=True),
        engine.run_waveform(fiber_length, wavelength_nm=1550.0, use_encryption=True, use_dcf=True, use_edfa=True),
    ]
    st.session_state.sweeps = engine.sweep_all_scenarios()
    st.session_state.active_cfg = cfg


def _plot(fig_fn, *args, label: str, **kwargs) -> None:
    try:
        fig = fig_fn(*args, theme=st.session_state.theme, **kwargs)
        st.plotly_chart(fig, width="stretch")
    except Exception as exc:
        st.error(f"{label} failed: {exc}")
        import traceback
        st.code(traceback.format_exc(), language="python")


def _synthetic_image(size: int = 128) -> np.ndarray:
    yy, xx = np.indices((size, size))
    rings = (((xx - size / 2) ** 2 + (yy - size / 2) ** 2) ** 0.5 % 14) < 2
    gradient = np.tile(np.linspace(30, 140, size, dtype=np.uint8), (size, 1))
    return np.maximum(np.where(rings, 210, 24).astype(np.uint8), gradient)


def _image_demo(key: bytes, uploaded_img=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if uploaded_img is None:
        img_array = _synthetic_image()
    else:
        try:
            img = Image.open(uploaded_img).convert("L").resize((128, 128), Image.LANCZOS)
            img_array = np.array(img, dtype=np.uint8)
        except Exception:
            img_array = _synthetic_image()
    encrypted = RC4(key).encrypt_image(img_array)
    decrypted = RC4(key).decrypt_image(encrypted)
    return img_array, encrypted, decrypted


def render_simulation_section() -> None:
    # ── Page Wrap (Animation & Anchor) ────────────────────────────────────
    html_block('<div class="swdm-page-wrap"><div id="simulation" class="section-anchor"></div>')

    # ── Hero ──────────────────────────────────────────────────────────────
    html_block("""
    <section class="simulation-panel">
        <div class="simulation-hero">
            <div>
                <div class="simulation-label">02 / Simulation</div>
                <div class="simulation-title">Optical Secure WDM Simulator</div>
            </div>
            <p>
                The Optical Secure WDM Simulator is a unified analysis workspace for
                designing, testing, and validating wavelength-division multiplexed
                communication links. It enables configuration of transmission spans,
                channel plans, amplification strategies, and security layers while
                providing detailed insight into signal integrity, performance degradation,
                and network resilience. Through an interactive simulation pipeline, users
                can benchmark scenarios, compare configurations, and investigate system
                behavior across diverse operating conditions without modifying the
                underlying simulation engine.
            </p>
        </div>
    </section>
    """)

    # ── Parameter controls ────────────────────────────────────────────────
    with st.container(key="simulation_controls"):
        cfg, options = _build_config()

    # ── Run-action row: 2 equal buttons + 2 wider toggles ─────────────────
    with st.container(key="sim_run_row"):
        run_cols = st.columns([1, 1, 1.6, 1.6], gap="large")
        with run_cols[0]:
            run_one = st.button("Run active link", type="primary", width="stretch")
        with run_cols[1]:
            run_all = st.button("Run benchmarks", width="stretch")
        with run_cols[2]:
            auto_run = st.toggle("Auto-run active link on parameter changes", value=False)
        with run_cols[3]:
            auto_benchmarks = st.toggle("Auto-run benchmarks on parameter changes", value=False)

    if run_one or auto_run:
        with st.spinner("Running active optical link..."):
            _run_active(cfg, options)
    if run_all or auto_benchmarks:
        with st.spinner("Running benchmark waveforms and analytical sweeps..."):
            _run_benchmarks(cfg, options["fiber_length"])

    active    = st.session_state.get("active_result")
    benchmark = st.session_state.get("benchmark_results")
    sweeps    = st.session_state.get("sweeps")

    if active is None and benchmark is None:
        html_block("</div>")
        return

    # ── Active-link results ────────────────────────────────────────────────
    if active is not None:
        html_block(
            f"""
            <section class="workstation-panel">
                <div class="panel-section-title">
                    <div>
                        <h2>Latest run: {active.scenario}</h2>
                        <p>Direct waveform output from the current controls, rendered from the active backend result.</p>
                    </div>
                </div>
            """
        )
        metric_cards([
            (f"{active.empirical_q:.2f}", "Q-FACTOR"),
            (f"{active.empirical_ber:.2e}", "BER"),
            (f"{len(active.bits_rx)}", "BITS"),
            (f"{options['fiber_length']:.0f} km", "FIBER LENGTH"),
        ])
        _plot(plot_waveforms, active, cfg, label="Waveforms")
        html_block("</section>")

    # ── Benchmark results ──────────────────────────────────────────────────
    if benchmark is not None and sweeps is not None:
        names = ["Without Secure", "With Secure + EDFA", "With Secure + EDFA + DCF"]
        html_block(
            """
            <section class="workstation-panel">
                <div class="panel-section-title">
                    <div>
                        <h2>BER and Q-factor benchmark suite</h2>
                        <p>Distance sweeps, eye diagrams, scenario drilldowns, image encryption demo, and benchmark summary.</p>
                    </div>
                </div>
            """
        )
        metric_cards([(f"Q {result.empirical_q:.2f}", name) for result, name in zip(benchmark, names)])

        tabs = st.tabs(["Q-factor", "BER", "Eye diagrams", "Scenario detail", "Image encryption", "Summary"])
        with tabs[0]:
            _plot(plot_q_factor, sweeps, cfg, label="Q-factor")
        with tabs[1]:
            _plot(plot_ber, sweeps, cfg, label="BER")
        with tabs[2]:
            _plot(plot_eye_grid, benchmark, cfg, label="Eye diagrams")
        with tabs[3]:
            scenario = st.selectbox("Scenario detail", list(sweeps.keys()), format_func=lambda s: SCENARIO_META[s]["label"])
            _plot(plot_single_scenario, sweeps[scenario], cfg, label="Scenario detail")
        with tabs[4]:
            uploaded = st.file_uploader("Upload image for RC4 encryption demo", type=["png", "jpg", "jpeg", "bmp"])
            original, encrypted, decrypted = _image_demo(cfg.rc4_key, uploaded)
            image_cols = st.columns(3)
            for col, label, arr in zip(image_cols, ["Original", "Encrypted", "Decrypted"], [original, encrypted, decrypted]):
                with col:
                    st.caption(label)
                    st.image(arr, width="stretch", clamp=True)
        with tabs[5]:
            summary_rows = [
                ("Without Secure",           "77.4 km", "6192 Gbps-km", "Baseline reach"),
                ("With Secure + EDFA",       "63 km",   "5040 Gbps-km", "Security penalty"),
                ("With Secure + EDFA + DCF", "100 km",  "8000 Gbps-km", "Recovered encrypted reach"),
            ]
            html_block(
                """
                <div class="summary-table-card">
                    <table class="summary-table">
                        <thead>
                            <tr>
                                <th>System</th>
                                <th>Max Distance</th>
                                <th>B×L Product</th>
                                <th>Finding</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                + "".join(
                    f"""
                            <tr>
                                <td>{system}</td>
                                <td>{distance}</td>
                                <td>{product}</td>
                                <td>{finding}</td>
                            </tr>
                    """
                    for system, distance, product, finding in summary_rows
                )
                + """
                        </tbody>
                    </table>
                </div>
                """
            )
        html_block("</section>")

    html_block("</div>")
