from __future__ import annotations

import html

from ui.components.html import html_block


FLOW_BLOCKS = [
    ("TX", "PRBS"),
    ("SEC", "RC4"),
    ("TX", "NRZ"),
    ("TX", "MZM"),
    ("CH", "WDM"),
    ("CH", "SMF"),
    ("CH", "EDFA"),
    ("CH", "DCF"),
    ("RX", "PIN"),
    ("RX", "Bessel"),
    ("RX", "3R"),
    ("QA", "BER/Q"),
]


SYSTEM_CARDS = [
    (
        "Transmitter Architecture",
        "TX",
        "PRBS -> RC4 -> NRZ -> MZM -> WDM",
        "A Pseudo-Random Bit Sequence generator creates the input data stream. "
        "The RC4 stream cipher encrypts the binary sequence before transmission, "
        "then NRZ pulse shaping prepares the electrical signal for the Mach-Zehnder "
        "Modulator. The MZM modulates the optical carrier and WDM combines multiple "
        "wavelength channels for simultaneous transmission over one fiber.",
    ),
    (
        "Optical Channel Architecture",
        "CH",
        "SMF -> EDFA -> DCF",
        "The Single-Mode Fiber acts as the main transmission medium. EDFA restores "
        "power lost through fiber attenuation, while DCF compensates chromatic "
        "dispersion accumulated during propagation. Together these blocks reduce "
        "pulse broadening, inter-symbol interference, and long-distance quality loss.",
    ),
    (
        "Receiver Architecture",
        "RX",
        "PIN -> Bessel Filter -> 3R -> BER/Q",
        "The PIN photodiode converts the optical signal back into the electrical "
        "domain. A Bessel low-pass filter suppresses noise while preserving timing, "
        "and the 3R stage restores amplitude, shape, and timing before BER and "
        "Q-factor measurements evaluate link reliability.",
    ),
    (
        "Python Architecture",
        "PY",
        "Modules -> Engine -> Analysis -> Streamlit UI",
        "The simulator uses a modular Python structure with independent modules for "
        "PRBS generation, RC4 encryption, NRZ pulse generation, modulation, channel "
        "propagation, receiver processing, and performance analysis. NumPy and SciPy "
        "handle numerical signal processing, Plotly and Matplotlib visualize results, "
        "and Streamlit provides the interactive control layer.",
    ),
]


def _flow_html() -> str:
    nodes = []
    for tag, name in FLOW_BLOCKS:
        nodes.append(
            f"""
            <div class="architecture-flow-node">
                <small>{html.escape(tag)}</small>
                <strong>{html.escape(name)}</strong>
            </div>
            """
        )
    return "".join(nodes)


def _system_cards_html() -> str:
    cards = []
    for title, icon, route, body in SYSTEM_CARDS:
        cards.append(
            f"""
            <article class="architecture-card architecture-summary-card">
                <div>
                    <span>{html.escape(route)}</span>
                    <h3>{html.escape(title)}</h3>
                    <p>{html.escape(body)}</p>
                </div>
            </article>
            """
        )
    return "".join(cards)


def render_architecture_section() -> None:
    html_block(
        """
        <style>
            .architecture-panel {
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                background: linear-gradient(135deg, color-mix(in srgb, var(--surface-2) 88%, transparent), color-mix(in srgb, var(--surface) 92%, transparent));
                padding: 52.8px;
                margin: 16px auto var(--space-xl);
                box-shadow: var(--shadow);
            }
            .architecture-hero {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                gap: 22px;
                margin-bottom: 35.2px;
            }
            .architecture-label {
                color: var(--accent);
                font-family: var(--font-mono);
                font-size: 11px;
                font-weight: 800;
                letter-spacing: .1em;
                text-transform: uppercase;
                margin: 0 0 42px;
            }
            .architecture-title {
                color: var(--text-primary) !important;
                font-family: var(--font-display) !important;
                font-size: 38px !important;
                font-weight: 700 !important;
                letter-spacing: 0;
                line-height: 1.1 !important;
                margin: 0 !important;
                max-width: none;
                white-space: nowrap !important;
            }
            .architecture-hero p {
                color: var(--text-secondary);
                font-size: 15px;
                line-height: 1.7;
                margin: 0;
                max-width: 760px;
            }
            .architecture-section-block {
                padding: 0;
                margin-bottom: 35.2px;
            }
            .architecture-section-block:last-child {
                padding-bottom: 0;
                margin-bottom: 0;
            }
            .architecture-flow {
                display: grid;
                grid-template-columns: repeat(12, minmax(54px, 1fr));
                gap: 10px;
                align-items: center;
                overflow-x: auto;
                padding: var(--space-sm) 2px var(--space-md);
            }
            .architecture-flow-node {
                position: relative;
                min-height: 78px;
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                background: linear-gradient(135deg, color-mix(in srgb, var(--surface-3) 78%, transparent), color-mix(in srgb, var(--surface) 94%, transparent));
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 6px;
                text-align: center;
                box-shadow: inset 0 0 0 1px color-mix(in srgb, white 3%, transparent);
            }
            .architecture-flow-node:not(:last-child)::after {
                content: "";
                position: absolute;
                top: 50%;
                left: calc(100% + 2px);
                width: 6px;
                height: 1px;
                background: var(--accent);
                box-shadow: 0 0 10px color-mix(in srgb, var(--accent) 45%, transparent);
            }
            .architecture-flow-node:not(:last-child)::before {
                content: "";
                position: absolute;
                top: calc(50% - 4px);
                left: calc(100% + 6px);
                width: 8px;
                height: 8px;
                border-top: 1px solid var(--accent);
                border-right: 1px solid var(--accent);
                transform: rotate(45deg);
            }
            .architecture-flow-node small,
            .architecture-card span {
                color: var(--accent);
                font-family: var(--font-mono);
                font-size: 10px;
                font-weight: 750;
                letter-spacing: .08em;
                text-transform: uppercase;
            }
            .architecture-flow-node strong {
                color: var(--text-primary);
                font-size: 11px;
                font-weight: 700;
                line-height: 1.2;
            }
            .architecture-card-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 17.6px;
            }
            .architecture-card {
                display: flex;
                align-items: center;
                gap: 17.6px;
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                background: var(--card-gradient-premium);
                padding: 17.6px;
                min-height: 108px;
                width: 100%;
                box-sizing: border-box;
                text-decoration: none;
                transition: border-color var(--ease), transform var(--ease), background var(--ease);
            }
            .architecture-card:hover {
                border-color: color-mix(in srgb, var(--accent) 34%, var(--border));
                transform: translateY(-1px);
                background: var(--card-gradient-premium);
            }
            .architecture-summary-card {
                display: block;
            }
            .architecture-card-icon {
                width: 52px;
                height: 52px;
                flex: 0 0 52px;
                display: grid;
                place-items: center;
                border-radius: var(--radius-sm);
                background: color-mix(in srgb, var(--accent) 10%, transparent);
                color: var(--accent);
                font-family: var(--font-mono);
                font-size: 11px;
                font-weight: 800;
            }
            .architecture-card h3 {
                color: var(--text-primary);
                font-family: var(--font-display);
                font-size: 16px;
                font-weight: 700;
                margin: var(--space-sm) 0;
            }
            .architecture-card p {
                color: var(--text-secondary);
                font-size: 13px;
                line-height: 1.58;
                margin: 0;
            }
            @media (max-width: 1180px) {
                .architecture-flow {
                    grid-template-columns: repeat(12, 64px);
                }
            }
            @media (max-width: 860px) {
                .architecture-panel {
                    padding: 26.4px;
                }
                .architecture-hero {
                    gap: 18px;
                }
                .architecture-label {
                    margin-bottom: 28px;
                }
                .architecture-title {
                    font-size: clamp(28px, 9vw, 38px) !important;
                    white-space: normal !important;
                }
                .architecture-section-block {
                    margin-bottom: var(--space-lg);
                }
                .architecture-card {
                    padding: 17.6px;
                }
            }
        </style>
        <div class="swdm-page-wrap">
        """
    )

    html_block(
        f"""
        <section class="architecture-panel">
            <div class="architecture-hero">
                <div>
                    <div class="architecture-label">03 / Architecture</div>
                    <div class="architecture-title">System and Python architecture</div>
                </div>
                <p>
                    The secure optical pipeline and the modular Python framework behind the simulator.
                    Each block is organized inside one unified architecture card, matching the page style
                    used for the publisher section.
                </p>
            </div>
            <div class="architecture-section-block">
            <div class="architecture-flow">{_flow_html()}</div>
            </div>
            <div class="architecture-section-block">
            <div class="architecture-card-grid">{_system_cards_html()}</div>
            </div>
        </section>
        </div>
        """
    )
