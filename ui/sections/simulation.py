from __future__ import annotations

import numpy as np
import streamlit as st
from PIL import Image

from config import SystemConfig
from encryption.rc4 import RC4
from simulation.engine import SimulationEngine
from ui.charts import SCENARIO_META, plot_ber, plot_eye_grid, plot_q_factor, plot_single_scenario, plot_waveforms
from ui.components import metric_cards, signal_flow, status_chips, system_params_table


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

from ui.components.html import html_block

def render_simulation_section() -> None:
    html_block("""
    <style>
        /* ── Page entrance animation ── */
        .swdm-page-wrap {
            animation: swdm-enter 500ms cubic-bezier(.22,1,.36,1) both;
        }
        @keyframes swdm-enter {
            from { opacity: 0; transform: translateY(24px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ── Hero panel ── */
        .simulation-panel {
            border: 1px solid rgba(61, 157, 243, 0.34);
            border-radius: 26px;
            background: var(--card-gradient-premium);
            padding: 30px 48px 34px 48px;
            margin: 0 0 var(--space-xl) 0;
            box-shadow: 0 18px 62px rgba(15, 50, 100, 0.10);
        }
        .simulation-hero {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: var(--space-lg);
            margin-bottom: 0;
        }
        .simulation-label {
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin: 0 0 var(--space-xl) 0;
        }
        .simulation-title {
            color: var(--text-primary) !important;
            font-family: var(--font-display) !important;
            font-size: 42px !important;
            font-weight: 760 !important;
            letter-spacing: 0;
            line-height: 1.1 !important;
            margin: 0 !important;
            white-space: nowrap !important;
        }
        .simulation-hero p {
            color: var(--text-secondary);
            font-size: 16px;
            line-height: 1.62;
            margin: 0;
            width: 100%;
            text-align: justify;
            text-align-last: left;
        }

        /* ── Controls container: remove Streamlit's default frame ── */
        .st-key-simulation_controls {
            border: 0 !important;
            background: transparent !important;
            margin: 0 0 var(--space-lg) 0 !important;
            padding: 0 !important;
        }
        .st-key-simulation_controls > [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        .st-key-simulation_controls [data-testid="stHorizontalBlock"] {
            align-items: flex-start !important;
            gap: var(--space-2xl) !important;
            margin: 0 !important;
            padding: 0 !important;
            flex-wrap: nowrap !important;
        }
        .st-key-simulation_controls [data-testid="stColumn"] {
            padding: 0 !important;
            min-width: 0 !important;
        }

        /* Widget label sizing */
        .st-key-simulation_controls [data-testid="stWidgetLabel"] p,
        .st-key-simulation_controls .stSlider label p,
        .st-key-simulation_controls .stSelectbox label p {
            color: var(--text-secondary) !important;
            font-size: 14px !important;
            font-weight: 650 !important;
            letter-spacing: .02em !important;
            margin-bottom: var(--space-xl) !important;
        }
        .st-key-simulation_controls [data-testid="stSlider"] {
            margin-bottom: var(--space-2xl) !important;
        }
        .st-key-simulation_controls [data-testid="stSlider"]:last-child {
            margin-bottom: 0 !important;
        }
        .st-key-simulation_controls [data-testid="stSelectbox"] {
            margin-bottom: var(--space-2xl) !important;
        }
        .st-key-simulation_controls [data-testid="stSelectbox"]:last-child {
            margin-bottom: 0 !important;
        }

        /* Selectbox: theme-aware gradient card */
        .st-key-simulation_controls [data-testid="stSelectbox"] > div > div,
        .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"],
        .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            min-height: 42px !important;
            height: 42px !important;
            border-radius: var(--radius-md) !important;
            background: linear-gradient(135deg, #213440 0%, #151d27 55%, #0f151d 100%) !important;
            border: 1px solid rgba(61, 157, 243, 0.32) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(125, 180, 255, 0.10) !important;
        }
        [data-theme="light"] .st-key-simulation_controls [data-testid="stSelectbox"] > div > div,
        [data-theme="light"] .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"],
        [data-theme="light"] .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: linear-gradient(135deg, #ffffff 0%, #eaf3fb 55%, #ddeaf6 100%) !important;
            border: 1px solid rgba(61, 157, 243, 0.20) !important;
            box-shadow: 0 4px 18px rgba(15, 50, 100, 0.06) !important;
        }
        .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"] span {
            color: var(--text-primary) !important;
            font-size: 14px !important;
            font-weight: 550 !important;
        }
        .st-key-simulation_controls [data-testid="stSelectbox"] [data-baseweb="select"] svg {
            color: var(--accent, #3d9df3) !important;
        }

        /* ── Toggles column: precise 3-point vertical alignment ──
           Toggle 1 → midpoint of WDM channels card
           Toggle 3 → bottom of Rate/channel card
           Toggle 2 → evenly between them

           The WDM channels selectbox sits below its label (~20px) and
           the label margin (~var(--space-xl) ≈ 16px). The selectbox
           itself is 42px tall, so its midpoint is ~21px below its top
           edge. Total offset from the very top of the column to the
           WDM card midpoint ≈ label(14px) + label-margin(16px) + 21px = ~51px.
           We use padding-top to push the flex container down by that
           amount, then space-between to pin the last toggle at the
           bottom of the Rate/channel card.
        ── */
        .st-key-simulation_controls .st-key-link_feature_toggles {
            display: grid !important;
            grid-template-rows: 1fr 1fr 1fr !important;
            align-items: center !important;
            gap: 0 !important;
            /* Exact calculation using actual CSS vars:
               --space-xl = 26.4px,  --space-2xl = 35.2px
               
               Column layout (middle col):
                 WDM label        14px
                 label-margin     26.4px  (--space-xl)
                 WDM selectbox    42px    ← midpoint at +21px
                 selectbox-margin 35.2px  (--space-2xl)
                 Rate label       14px
                 label-margin     26.4px  (--space-xl)
                 Rate selectbox   42px    ← bottom = 200px
               ──────────────────────────────────────────
               Total              200px

               Toggle-1 TOP at WDM selectbox midpoint:
                 14 + 26.4 + 21 = 61.4 ≈ 61px  → padding-top

                Container bottom at Rate/channel selectbox bottom:
                  200px total                    → height (border-box)
            */
            padding-top: 61px !important;
            height: 218px !important;
            box-sizing: border-box !important;
        }
        .st-key-simulation_controls .st-key-link_feature_toggles [data-testid="stElementContainer"] {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            flex-shrink: 0 !important;
        }
        .st-key-simulation_controls .st-key-link_feature_toggles [data-testid="stToggle"] {
            margin: 0 !important;
        }

        /* Toggles column: right-align only the top-level last/3rd columns */
        .st-key-simulation_controls [data-testid="stColumn"]:last-child,
        .st-key-simulation_controls [data-testid="stColumn"]:nth-child(3) {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-end !important;
        }
        .st-key-simulation_controls [data-testid="stColumn"]:last-child [data-testid="stElementContainer"],
        .st-key-simulation_controls [data-testid="stColumn"]:nth-child(3) [data-testid="stElementContainer"] {
            width: 100% !important;
            display: flex !important;
            justify-content: flex-end !important;
        }

        /* Position Column 2 exactly equidistant from Column 1 and Column 3 */
        .st-key-simulation_controls [data-testid="stColumn"]:nth-child(2) [data-testid="stSelectbox"],
        .st-key-simulation_controls [data-testid="stColumn"]:nth-last-child(2) [data-testid="stSelectbox"] {
            width: 280px !important;
            margin-left: 95px !important;
        }

        /* ── Expander slider reset (key-based, no :not() needed) ──────────────
           The slider columns live inside .st-key-adv_tx_params (a container
           added in Python). We target that key directly, matching the same
           specificity as the flex-end rules above so source-order wins.
        ── */
        .st-key-adv_tx_params [data-testid="stColumn"],
        .st-key-adv_tx_params [data-testid="stColumn"]:last-child,
        .st-key-adv_tx_params [data-testid="stColumn"]:nth-child(3) {
            display: block !important;
            flex-direction: initial !important;
            align-items: initial !important;
        }
        .st-key-adv_tx_params [data-testid="stElementContainer"],
        .st-key-adv_tx_params [data-testid="stColumn"]:last-child [data-testid="stElementContainer"],
        .st-key-adv_tx_params [data-testid="stColumn"]:nth-child(3) [data-testid="stElementContainer"] {
            display: block !important;
            justify-content: initial !important;
            width: 100% !important;
        }
        /* Hide min/max tick labels only */
        .st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBar"],
        .st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBarMin"],
        .st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBarMax"] {
            display: none !important;
        }

        .st-key-simulation_controls .st-key-link_feature_toggles [data-testid="stElementContainer"]:nth-child(3) {
            align-self: end !important;
            margin-bottom: -20px !important;
        }

        /* Toggle label alignment */
        .st-key-simulation_controls [data-testid="stCheckbox"] label[data-baseweb="checkbox"] {
            gap: var(--space-lg) !important;
            justify-content: flex-end !important;
            width: 100% !important;
        }
        .st-key-simulation_controls [data-testid="stCheckbox"] {
            width: 100% !important;
        }
        .st-key-simulation_controls [data-testid="stCheckbox"] label[data-baseweb="checkbox"] > div:first-child {
            transform: scale(1.15);
            transform-origin: left center;
        }
        .st-key-simulation_controls [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p {
            color: var(--text-primary) !important;
            font-size: 15px !important;
            font-weight: 550 !important;
            margin: 0 !important;
            min-width: 150px;
        }

        /* ── Run-action row: equal-width buttons + right-aligned toggles ── */
        .sim-run-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1.6fr 1.6fr;
            gap: var(--space-lg);
            align-items: center;
            margin: 0 0 var(--space-xl) 0;
        }

        /* Override Streamlit's default horizontal-block gap in the run row */
        .st-key-sim_run_row [data-testid="stHorizontalBlock"] {
            gap: var(--space-lg) !important;
            align-items: center !important;
        }
        .st-key-sim_run_row [data-testid="stColumn"] {
            padding: 0 !important;
        }

        /* ── Toggle global style consistency ── */
        [data-testid="stToggle"] {
            display: flex !important;
            align-items: center !important;
            gap: var(--space-sm) !important;
        }
        [data-testid="stToggle"] label {
            color: var(--text-primary) !important;
            font-weight: 650 !important;
            font-size: 14px !important;
            margin: 0 !important;
        }
        [data-testid="stToggle"] [role="switch"] {
            background-color: var(--accent) !important;
            border: 2px solid var(--accent) !important;
        }
        [data-testid="stToggle"] [role="switch"][aria-checked="false"] {
            background-color: rgba(61, 157, 243, 0.32) !important;
            border-color: rgba(61, 157, 243, 0.68) !important;
        }
        [data-testid="stToggle"] [role="switch"]::after {
            background-color: white !important;
        }
        [data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input[aria-checked="false"]) > div:first-child {
            background: rgba(61, 157, 243, 0.34) !important;
            border: 1px solid rgba(61, 157, 243, 0.24) !important;
        }
        [data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input[aria-checked="false"]) > div:first-child > div {
            background: #ffffff !important;
            border: 1px solid rgba(61, 157, 243, 0.48) !important;
        }

        /* ── Results panels ── */
        /* panel-section-title: consistent header layout inside workstation-panel */
        .panel-section-title {
            display: flex;
            align-items: flex-start;
            gap: var(--space-lg);
            margin-bottom: var(--space-xl);
        }
        .panel-section-title > div { flex: 1; }
        .panel-section-title h2 {
            color: var(--text-primary) !important;
            font-family: var(--font-display) !important;
            font-size: 22px !important;
            font-weight: 700 !important;
            margin: 0 0 var(--space-xs) 0 !important;
            line-height: 1.25;
        }
        .panel-section-title p {
            color: var(--text-secondary);
            font-size: 13px;
            line-height: 1.6;
            margin: 0 !important;
        }

        /* Responsive */
        @media (max-width: 860px) {
            .simulation-panel { padding: var(--space-xl); }
            .simulation-title { font-size: clamp(28px, 9vw, 38px) !important; white-space: normal !important; }
            .panel-section-title { flex-direction: column; }
            .sim-run-row { grid-template-columns: 1fr 1fr; }
        }
    </style>
    <div class="swdm-page-wrap">
    <div id="simulation" class="section-anchor"></div>
    """)

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
        # 4-metric grid — relies on theme.py's .metric-grid / .metric-card styles
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
        # 3-metric grid — uses theme.py's 3-col variant
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