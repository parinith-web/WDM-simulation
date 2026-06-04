from __future__ import annotations

import html
import streamlit as st

from ui.components import info_card, section_header
from ui.components.html import html_block


def render_theory_section() -> None:
    html_block("""
    <style>
        .swdm-page-wrap {
            animation: swdm-enter 500ms cubic-bezier(.22,1,.36,1) both;
        }
        @keyframes swdm-enter {
            from { opacity: 0; transform: translateY(24px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        /* Equal height cards in theory tabs */
        [data-testid="stColumn"]:has(.soft-card) {
            display: flex;
            flex-direction: column;
        }
        [data-testid="stColumn"]:has(.soft-card) > [data-testid="stElementContainer"] {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        [data-testid="stColumn"]:has(.soft-card) > [data-testid="stElementContainer"] > [data-testid="stHtml"] {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .soft-card {
            flex: 1;
            min-height: 190px;
            height: 100%;
        }
        .theory-panel {
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            background: linear-gradient(135deg, color-mix(in srgb, var(--surface-2) 88%, transparent), color-mix(in srgb, var(--surface) 92%, transparent));
            padding: 35.2px 35.2px 26.4px 35.2px;
            margin: 0 auto var(--space-xl);
            box-shadow: var(--shadow);
        }
        .theory-hero {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 13.2px;
            margin-bottom: 0;
        }
        .theory-label {
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin: 0 0 42px;
        }
        .theory-title {
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
        .theory-hero p {
            color: var(--text-secondary);
            font-size: 15px;
            line-height: 1.7;
            margin: 0;
            max-width: 760px;
        }
        .theory-section-block {
            padding: 0;
            margin-bottom: 35.2px;
        }
        .theory-section-block:last-child {
            padding-bottom: 0;
            margin-bottom: 0;
        }
        .theory-flow {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            gap: 8px;
            align-items: center;
            overflow-x: auto;
            padding: var(--space-sm) 2px var(--space-md);
        }
        .theory-flow-node {
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
        .theory-flow-node:not(:last-child)::after {
            content: "";
            position: absolute;
            top: 50%;
            left: calc(100% + 2px);
            width: 6px;
            height: 1px;
            background: var(--accent);
            box-shadow: 0 0 10px color-mix(in srgb, var(--accent) 45%, transparent);
        }
        .theory-flow-node:not(:last-child)::before {
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
        .theory-flow-node small,
        .theory-card span {
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 750;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .theory-flow-node strong {
            color: var(--text-primary);
            font-size: 11px;
            font-weight: 700;
            line-height: 1.2;
        }
        .theory-intro {{
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            background: var(--card-gradient-premium);
            padding: var(--space-lg) var(--space-xl);
            margin: var(--space-xl) 0;
        }}
        .theory-intro p {{
            color: var(--text-secondary);
            font-size: 15px;
            line-height: 1.65;
            margin: 0;
        }}
        .theory-intro strong {{
            color: var(--accent);
            font-weight: 700;
        }}
        @media (max-width: 1180px) {
            .theory-flow {
                grid-template-columns: repeat(8, 80px);
            }
        }
        @media (max-width: 860px) {
            .theory-panel {
                padding: 26.4px;
            }
            .theory-hero {
                gap: 18px;
            }
            .theory-label {
                margin-bottom: 28px;
            }
            .theory-title {
                font-size: clamp(28px, 9vw, 38px) !important;
                white-space: normal !important;
            }
            .theory-section-block {
                margin-bottom: var(--space-lg);
            }
        }
    </style>
    <div class="swdm-page-wrap">
    """)

    html_block("""
    <section class="theory-panel">
        <div class="theory-hero">
            <div>
                <div class="theory-label">03 / Theory</div>
                <div class="theory-title">Optical communication, decoded</div>
            </div>
            <p>
                Secure WDM combines cryptographic encryption, optical signal propagation, and real-time digital recovery. 
                This system integrates RC4 stream cipher with intensity modulation, demonstrating security-performance tradeoffs in optical networks.
            </p>
        </div>
        <div class="theory-section-block">
    """)

    html_block("""
    <style>
        .bd-wrap {
            width: 100%;
            overflow-x: auto;
            margin: var(--space-lg) 0 0;
            padding-bottom: var(--space-md);
        }
        .bd-svg {
            display: block;
            margin: 0 auto;
            background: transparent;
        }
        /* Specialized Card Style from image1.png */
        .bd-card-rect {
            fill: #f0f5fa;
            stroke: rgba(61, 157, 243, 0.25);
            stroke-width: 1.2px;
            rx: 8px;
            ry: 8px;
            transition: all 0.25s ease-in-out;
        }
        .bd-card-rect-sm {
            fill: #f0f5fa;
            stroke: rgba(61, 157, 243, 0.25);
            stroke-width: 1.2px;
            rx: 6px;
            ry: 6px;
            transition: all 0.25s ease-in-out;
        }
        .bd-node:hover .bd-card-rect,
        .bd-node:hover .bd-card-rect-sm {
            stroke: rgba(61, 157, 243, 0.65);
            fill: #e8f1f9;
            filter: drop-shadow(0 0 6px rgba(61, 157, 243, 0.25));
            cursor: pointer;
        }
        /* Text styling */
        .bd-tag {
            font-family: var(--font-mono, monospace);
            font-size: 8px;
            font-weight: 700;
            fill: #3D9DF3;
            letter-spacing: 0.1em;
            text-anchor: middle;
            text-transform: uppercase;
        }
        .bd-tag-sm {
            font-family: var(--font-mono, monospace);
            font-size: 7.5px;
            font-weight: 700;
            fill: #3D9DF3;
            letter-spacing: 0.08em;
            text-anchor: middle;
            text-transform: uppercase;
        }
        .bd-title {
            font-family: var(--font-display, sans-serif);
            font-size: 11px;
            font-weight: 700;
            fill: #0f1923;
            letter-spacing: 0.05em;
            text-anchor: middle;
            text-transform: uppercase;
        }
        .bd-title-sm {
            font-family: var(--font-display, sans-serif);
            font-size: 9.5px;
            font-weight: 700;
            fill: #0f1923;
            letter-spacing: 0.03em;
            text-anchor: middle;
            text-transform: uppercase;
        }
        .bd-title-char {
            font-family: var(--font-display, sans-serif);
            font-size: 9.5px;
            font-weight: 700;
            fill: #0f1923;
            text-anchor: middle;
        }
        /* Group bounding box style from image4.png */
        .bd-group-box {
            fill: none;
            stroke: rgba(61, 157, 243, 0.12);
            stroke-width: 1px;
            stroke-dasharray: 4 4;
            rx: 10px;
            ry: 10px;
        }
        .bd-group-label {
            font-family: var(--font-body, sans-serif);
            font-size: 9px;
            font-weight: 700;
            fill: rgba(61, 157, 243, 0.55);
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        /* Connection lines and arrowheads */
        .bd-line {
            fill: none;
            stroke: #3D9DF3;
            stroke-width: 1.2px;
            opacity: 0.75;
        }
        .bd-line-dashed {
            fill: none;
            stroke: #3D9DF3;
            stroke-width: 1.2px;
            stroke-dasharray: 3 3;
            opacity: 0.6;
        }
        .bd-arrowhead {
            fill: #3D9DF3;
            opacity: 0.75;
        }
    </style>
    <div class="bd-wrap">
    <svg class="bd-svg" viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg" style="min-width:760px; max-width:900px;">
      <defs>
        <!-- Arrowhead Marker -->
        <marker id="bd-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 2 L 7 5 L 0 8 Z" class="bd-arrowhead" />
        </marker>
      </defs>

      <!-- ==================== TOP SECTION: SIGNAL GENERATION CHAIN ==================== -->
      <rect class="bd-group-box" x="150" y="20" width="560" height="85" />
      <text x="430" y="14" text-anchor="middle" class="bd-group-label">Signal Generation Chain</text>

      <!-- PRBS -->
      <g class="bd-node" transform="translate(210, 32)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">TX</text>
        <text class="bd-title" x="40" y="44">PRBS</text>
      </g>
      
      <!-- Arrow 1 -->
      <path class="bd-line" d="M 290 62 H 330" marker-end="url(#bd-arrow)" />

      <!-- RC4 -->
      <g class="bd-node" transform="translate(330, 32)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">SEC</text>
        <text class="bd-title" x="40" y="44">RC4</text>
      </g>

      <!-- Arrow 2 -->
      <path class="bd-line" d="M 410 62 H 450" marker-end="url(#bd-arrow)" />

      <!-- NRZ -->
      <g class="bd-node" transform="translate(450, 32)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">TX</text>
        <text class="bd-title" x="40" y="44">NRZ</text>
      </g>

      <!-- Arrow 3 -->
      <path class="bd-line" d="M 530 62 H 570" marker-end="url(#bd-arrow)" />

      <!-- MZM -->
      <g class="bd-node" transform="translate(570, 32)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">TX</text>
        <text class="bd-title" x="40" y="44">MZM</text>
      </g>


      <!-- ==================== MIDDLE SECTION ==================== -->
      
      <!-- Transmitters Group (Column 1) -->
      <text x="65" y="120" text-anchor="middle" class="bd-group-label">Transmitters</text>
      
      <g class="bd-node" transform="translate(30, 130)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">TX</text>
        <text class="bd-title-sm" x="35" y="30">TX 1</text>
      </g>
      <g class="bd-node" transform="translate(30, 180)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">TX</text>
        <text class="bd-title-sm" x="35" y="30">TX 2</text>
      </g>
      
      <text x="65" y="244" text-anchor="middle" style="font-size:16px; fill:rgba(34, 211, 238, 0.4); font-weight:bold;">⋮</text>
      
      <g class="bd-node" transform="translate(30, 258)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">TX</text>
        <text class="bd-title-sm" x="35" y="30">TX 7</text>
      </g>
      <g class="bd-node" transform="translate(30, 308)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">TX</text>
        <text class="bd-title-sm" x="35" y="30">TX 8</text>
      </g>

      <!-- Connections from Transmitters to WDM MUX -->
      <path class="bd-line" d="M 100 150 H 125" />
      <path class="bd-line" d="M 100 200 H 125" />
      <path class="bd-line" d="M 100 278 H 125" />
      <path class="bd-line" d="M 100 328 H 125" />
      <path class="bd-line" d="M 125 150 V 328" />
      <path class="bd-line" d="M 125 239 H 145" marker-end="url(#bd-arrow)" />


      <!-- WDM MUX Card (Column 2) -->
      <g class="bd-node" transform="translate(145, 189)">
        <rect class="bd-card-rect" x="0" y="0" width="50" height="100" />
        <text class="bd-tag" x="25" y="20">CH</text>
        <text class="bd-title-char" x="25" y="46">W</text>
        <text class="bd-title-char" x="25" y="62">D</text>
        <text class="bd-title-char" x="25" y="78">M</text>
      </g>


      <!-- Fiber Span Stack (Column 3) -->
      <!-- SMF -->
      <g class="bd-node" transform="translate(265, 135)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="50" />
        <text class="bd-tag" x="40" y="20">CH</text>
        <text class="bd-title-sm" x="40" y="38">SMF</text>
      </g>
      
      <!-- Arrow SMF -> EDFA -->
      <path class="bd-line" d="M 305 185 V 205" marker-end="url(#bd-arrow)" />

      <!-- EDFA -->
      <g class="bd-node" transform="translate(265, 205)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="50" />
        <text class="bd-tag" x="40" y="20">CH</text>
        <text class="bd-title-sm" x="40" y="38">EDFA</text>
      </g>

      <!-- Arrow EDFA -> DCF -->
      <path class="bd-line" d="M 305 255 V 275" marker-end="url(#bd-arrow)" />

      <!-- DCF -->
      <g class="bd-node" transform="translate(265, 275)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="50" />
        <text class="bd-tag" x="40" y="20">CH</text>
        <text class="bd-title-sm" x="40" y="38">DCF</text>
      </g>

      <!-- Connection from WDM and MZM (Top) to SMF -->
      <path class="bd-line" d="M 195 239 H 235 V 160 H 265" marker-end="url(#bd-arrow)" />
      <path class="bd-line" d="M 650 62 H 730 V 115 H 235 V 160" />


      <!-- De-WDM DEMUX Card (Column 4) -->
      <g class="bd-node" transform="translate(390, 179)">
        <rect class="bd-card-rect" x="0" y="0" width="50" height="120" />
        <text class="bd-tag" x="25" y="20">CH</text>
        <text class="bd-title-char" x="25" y="42">D</text>
        <text class="bd-title-char" x="25" y="54">E</text>
        <text class="bd-title-char" x="25" y="66">-</text>
        <text class="bd-title-char" x="25" y="78">W</text>
        <text class="bd-title-char" x="25" y="90">D</text>
        <text class="bd-title-char" x="25" y="102">M</text>
      </g>

      <!-- Connection from DCF to De-WDM -->
      <path class="bd-line" d="M 345 300 H 370 V 239 H 390" marker-end="url(#bd-arrow)" />


      <!-- Receivers Group (Column 5) -->
      <g class="bd-node" transform="translate(480, 130)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">RX</text>
        <text class="bd-title-sm" x="35" y="30">RX 1</text>
      </g>
      <g class="bd-node" transform="translate(480, 180)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">RX</text>
        <text class="bd-title-sm" x="35" y="30">RX 2</text>
      </g>
      
      <text x="515" y="244" text-anchor="middle" style="font-size:16px; fill:rgba(34, 211, 238, 0.4); font-weight:bold;">⋮</text>
      
      <g class="bd-node" transform="translate(480, 258)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">RX</text>
        <text class="bd-title-sm" x="35" y="30">RX 3</text>
      </g>
      <g class="bd-node" transform="translate(480, 308)">
        <rect class="bd-card-rect-sm" x="0" y="0" width="70" height="40" />
        <text class="bd-tag-sm" x="35" y="16">RX</text>
        <text class="bd-title-sm" x="35" y="30">RX 4</text>
      </g>

      <!-- Connections from De-WDM to Receivers -->
      <path class="bd-line" d="M 440 239 H 460" />
      <path class="bd-line" d="M 460 150 V 328" />
      <path class="bd-line" d="M 460 150 H 480" marker-end="url(#bd-arrow)" />
      <path class="bd-line" d="M 460 200 H 480" marker-end="url(#bd-arrow)" />
      <path class="bd-line" d="M 460 278 H 480" marker-end="url(#bd-arrow)" />
      <path class="bd-line" d="M 460 328 H 480" marker-end="url(#bd-arrow)" />


      <!-- ==================== BOTTOM SECTION: RECEIVER SIGNAL CHAIN ==================== -->
      <rect class="bd-group-box" x="90" y="365" width="680" height="70" />
      <text x="430" y="465" text-anchor="middle" class="bd-group-label">Receiver Signal Chain</text>

      <!-- PIN -->
      <g class="bd-node" transform="translate(150, 370)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">RX</text>
        <text class="bd-title" x="40" y="44">PIN</text>
      </g>

      <!-- Arrow 1 -->
      <path class="bd-line" d="M 230 400 H 270" marker-end="url(#bd-arrow)" />

      <!-- RC4 Decryption -->
      <g class="bd-node" transform="translate(270, 370)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">SEC</text>
        <text class="bd-title-sm" x="40" y="43">RC4 DEC</text>
      </g>

      <!-- Arrow 2 -->
      <path class="bd-line" d="M 350 400 H 390" marker-end="url(#bd-arrow)" />

      <!-- Bessel -->
      <g class="bd-node" transform="translate(390, 370)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">RX</text>
        <text class="bd-title" x="40" y="44">BESSEL</text>
      </g>

      <!-- Arrow 3 -->
      <path class="bd-line" d="M 470 400 H 510" marker-end="url(#bd-arrow)" />

      <!-- 3R -->
      <g class="bd-node" transform="translate(510, 370)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">RX</text>
        <text class="bd-title" x="40" y="44">3R</text>
      </g>

      <!-- Arrow 4 -->
      <path class="bd-line" d="M 590 400 H 630" marker-end="url(#bd-arrow)" />

      <!-- BER/Q -->
      <g class="bd-node" transform="translate(630, 370)">
        <rect class="bd-card-rect" x="0" y="0" width="80" height="60" />
        <text class="bd-tag" x="40" y="22">QA</text>
        <text class="bd-title" x="40" y="44">BER/Q</text>
      </g>

      <!-- Connection from Receivers Output, down and around, to PIN -->
      <path class="bd-line" d="M 550 150 H 570" />
      <path class="bd-line" d="M 550 200 H 570" />
      <path class="bd-line" d="M 550 278 H 570" />
      <path class="bd-line" d="M 550 328 H 570" />
      <path class="bd-line" d="M 570 150 V 328" />
      
      <!-- Loop line around the right side, down, along bottom, up to left of PIN -->
      <path class="bd-line-dashed" d="M 570 230 H 810 V 450 H 70 V 400 H 150" marker-end="url(#bd-arrow)" />

    </svg>
    </div>
    """)
    
    html_block("""
        </div>
    </section>
    """)

    html_block("""
    <section class="theory-intro">
        <p>
            <strong>Security Layer:</strong> RC4 stream cipher encrypts PRBS data before optical transmission, scrambling patterns to prevent eavesdropping.<br><br>
            <strong>Optical Layer:</strong> MZM intensity modulation and WDM multiplex encrypted signals across wavelengths; fiber attenuation and dispersion degrade the encrypted signal.<br><br>
            <strong>Recovery Layer:</strong> PIN detection, Bessel filtering, and threshold decision recover encrypted bits; BER/Q-factor metrics quantify the security-performance tradeoff without/with EDFA and DCF compensation.
        </p>
    </section>
    """)
    
    tabs = st.tabs(["Encryption Security", "WDM Multiplexing", "Modulation & Detection", "Compensation", "Performance Analysis"])
    with tabs[0]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            info_card(
                "RC4 Stream Cipher",
                "Encrypts PRBS bits using XOR with a derived keystream. Scrambles deterministic patterns into pseudo-random sequences to prevent eavesdropping. Uses key-dependent initialization vectors to secure each transmission."
            )
        with c2:
            info_card(
                "Security-Performance Tradeoff",
                "Scrambled patterns increase susceptibility to fiber dispersion and ASE noise. Without compensation, reach is limited to 77 km; adding EDFA and DCF extends this to 100+ km, recovering the encryption penalty."
            )
    with tabs[1]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            info_card(
                "Wavelength Division Multiplexing",
                "Combines 8 independent 10 Gbps channels spaced at 0.4 nm in the 1550 nm C-band. Each encrypted channel carries independent data, modulated onto a single fiber to maximize bandwidth and aggregate capacity."
            )
        with c2:
            info_card(
                "Multi-Channel Secure System",
                "Demonstrates an 8-channel secure WDM system with an aggregate capacity of 80 Gbps. Each channel is encrypted independently, allowing for individual Q-factor tuning to model realistic, secure optical networks."
            )
    with tabs[2]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            info_card(
                "Mach-Zehnder Modulator (MZM)",
                "Intensity modulates the encrypted electrical signal onto a laser carrier. Extinction ratio controls 0/1 power levels, and the drive voltage determines launch power and SNR to avoid nonlinear fiber impairments."
            )
        with c2:
            info_card(
                "PIN Photodiode & Filtering",
                "Recovers photocurrent proportional to received power. A Bessel low-pass filter suppresses ASE noise and inter-symbol interference, followed by a 3R stage to restore signal shape before the bit decision."
            )
    with tabs[3]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            info_card(
                "EDFA Amplification",
                "Compensates for fiber attenuation loss by restoring signal power to launch levels. Adds amplified spontaneous emission noise, representing a physical limit in long-haul optical communication reach."
            )
        with c2:
            info_card(
                "Dispersion Compensation",
                "Compensates for chromatic dispersion in fiber spans using dispersion compensating fiber (DCF). Reduces pulse broadening and inter-symbol interference to open the eye diagram and minimize the bit error rates."
            )
    with tabs[4]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            info_card(
                "Q-Factor & BER",
                "Quantifies the signal-to-noise ratio at the decision threshold. A Q-factor above 6 corresponds to a bit error rate below 10^-9. These metrics directly evaluate the performance of encryption and compensation."
            )
        with c2:
            info_card(
                "System Reach Analysis",
                "Sweeps distance to find reach limits at a bit error rate of 10^-9. Compares baseline unencrypted reach (77.4 km) against encrypted transmission without compensation (63 km) and with EDFA/DCF support (100+ km)."
            )
    
    html_block("</div>")

