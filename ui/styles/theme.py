from __future__ import annotations

import re
import streamlit as st


THEMES = {
    "dark": {
        "bg_primary": "#080a0d",
        "bg_secondary": "#0d1117",
        "surface": "rgba(18, 24, 32, .78)",
        "surface_2": "rgba(25, 33, 43, .82)",
        "surface_3": "rgba(34, 44, 56, .70)",
        "text_primary": "#f4f7fb",
        "text_secondary": "#a9b4c2",
        "text_muted": "#657184",
        "border": "rgba(226, 239, 255, .095)",
        "border_strong": "rgba(226, 239, 255, .16)",
        "accent": "#7ddcff",
        "accent_2": "#6ea8ff",
        "green": "#7bd7b0",
        "amber": "#f2c66d",
        "red": "#f28a9b",
        "shadow": "0 24px 80px rgba(0, 0, 0, .38)",
        "chart_bg": "rgba(10, 14, 20, .90)",
        "plot_bg": "rgba(14, 19, 27, .78)",
        "grid": "rgba(226, 239, 255, .075)",
    },
    "light": {
        "bg_primary": "#e8eef5",
        "bg_secondary": "#f4f8fc",
        "surface": "rgba(255, 255, 255, .96)",
        "surface_2": "rgba(248, 252, 255, .97)",
        "surface_3": "rgba(220, 234, 248, .92)",
        "text_primary": "#0f1923",
        "text_secondary": "#2d4258",
        "text_muted": "#5a7a96",
        "border": "rgba(61, 157, 243, .28)",
        "border_strong": "rgba(61, 157, 243, .48)",
        "accent": "#3D9DF3",
        "accent_2": "#3D9DF3",
        "green": "#0e7a4f",
        "amber": "#9a6a0a",
        "red": "#b53050",
        "shadow": "0 24px 70px rgba(15, 35, 65, .13)",
        "chart_bg": "rgba(255, 255, 255, .99)",
        "plot_bg": "rgba(245, 250, 255, .99)",
        "grid": "rgba(61, 157, 243, .20)",
    },
}

# Light theme card gradient — bright, clean blue-white
_LIGHT_CARD_GRADIENT = "linear-gradient(135deg, #ffffff 0%, #eaf3fb 55%, #ddeaf6 100%)"
_DARK_CARD_GRADIENT  = "linear-gradient(135deg, #213440 0%, #151d27 48%, #0f151d 100%)"


def chart_tokens(theme: str = "dark") -> dict:
    tokens = dict(THEMES.get(theme, THEMES["dark"]))
    tokens.update(
        {
            "bg": tokens["bg_primary"],
            "bg2": tokens["bg_secondary"],
            "surface2": tokens["surface_2"],
            "text": tokens["text_primary"],
            "muted": tokens["text_secondary"],
            "faint": tokens["text_muted"],
            "border2": tokens["border_strong"],
            "cyan": tokens["accent"],
            "blue": tokens["accent_2"],
        }
    )
    return tokens


def _vars(theme: str) -> str:
    t = chart_tokens(theme)
    card_grad = _LIGHT_CARD_GRADIENT if theme == "light" else _DARK_CARD_GRADIENT
    lines = [f"    --{key.replace('_', '-')}: {value};" for key, value in t.items()]
    # Override card gradient with correct value for this theme
    lines.append(f"    --card-gradient-premium: {card_grad};")
    return "\n".join(lines)


def inject_theme(theme: str) -> None:
    cls = "dark-theme" if theme == "dark" else "light-theme"
    css_vars = _vars(theme)

    # Light-only extra card/element colours as plain CSS values (not vars)
    # so they don't depend on cascade scoping
    if theme == "light":
        card_bg      = _LIGHT_CARD_GRADIENT
        card_border  = "rgba(61, 157, 243, .28)"
        card_shadow  = "0 2px 16px rgba(15, 50, 100, .08)"
        text_h       = "#0f1923"
        text_body    = "#2d4258"
        text_muted   = "#5a7a96"
        accent_col   = "#3D9DF3"
        accent_bg    = "rgba(61, 157, 243, .09)"
        accent_bdr   = "rgba(61, 157, 243, .28)"
    else:
        card_bg      = _DARK_CARD_GRADIENT
        card_border  = "rgba(226, 239, 255, .095)"
        card_shadow  = "0 24px 80px rgba(0, 0, 0, .38)"
        text_h       = "#f4f7fb"
        text_body    = "#a9b4c2"
        text_muted   = "#657184"
        accent_col   = "#7ddcff"
        accent_bg    = "rgba(125, 220, 255, .10)"
        accent_bdr   = "rgba(125, 220, 255, .24)"

    raw = f"""<style>
/* ── THEME TOKENS ── */
:root {{
{css_vars}
    --space-xs: 6px;
    --space-sm: 10px;
    --space-md: 14px;
    --space-lg: 20px;
    --space-xl: 28px;
    --space-2xl: 40px;
    --space-3xl: 60px;
    --radius-xs: 5.5px;
    --radius-sm: 8.8px;
    --radius-md: 13.2px;
    --radius-lg: 17.6px;
    --sidebar-w: 272.8px;
    --ease: 143ms cubic-bezier(.2, .8, .2, 1);
    --ease-slow: 418ms cubic-bezier(.22, 1, .36, 1);
    --font-body: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", system-ui, sans-serif;
    --font-display: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", system-ui, sans-serif;
    --font-mono: "SF Mono", "Menlo", "Courier New", monospace;
    --card-gap: var(--space-2xl);
}}

/* ── BASE STYLES ── */
html {{
    height: 100%;
    scroll-behavior: smooth;
    background: var(--bg-primary);
    overflow: hidden;
}}

html, body, .stApp, .block-container {{
    font-family: var(--font-body) !important;
}}

body, .stApp {{
    height: 100%;
    overflow: hidden !important;
}}

.stApp {{
    color: var(--text-primary) !important;
    background:
        radial-gradient(circle at 18% 0%, color-mix(in srgb, var(--accent) 7%, transparent), transparent 28rem),
        radial-gradient(circle at 92% 12%, color-mix(in srgb, var(--accent-2) 6%, transparent), transparent 30rem),
        linear-gradient(135deg, var(--bg-primary), var(--bg-secondary) 58%, var(--bg-primary)) !important;
}}

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{
    display: none !important;
}}

.block-container {{
    max-width: 100% !important;
    height: 100vh !important;
    overflow: hidden !important;
    padding: 17.6px 26.4px 17.6px calc(var(--sidebar-w) + 44px) !important;
    margin: 0 !important;
}}

.app-theme-root::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(255,255,255,.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.015) 1px, transparent 1px);
    background-size: 80px 80px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,.4), transparent 70%);
}}

[data-testid="stElementContainer"]:has(.app-theme-root),
[data-testid="stElementContainer"]:has(.swdm-sidebar) {{
    display: contents !important;
}}

/* ── SIDEBAR ── */
.swdm-sidebar {{
    position: fixed;
    z-index: 9500;
    left: 17.6px;
    top: 17.6px;
    bottom: 17.6px;
    width: var(--sidebar-w);
    display: flex;
    flex-direction: column;
    padding: var(--space-lg);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    background:
        linear-gradient(180deg, color-mix(in srgb, var(--surface-2) 88%, transparent), color-mix(in srgb, var(--surface) 92%, transparent)),
        color-mix(in srgb, var(--bg-secondary) 74%, transparent);
    backdrop-filter: blur(24px) saturate(140%);
    box-shadow: var(--shadow);
}}

.swdm-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: var(--space-lg);
    border-bottom: 1px solid var(--border);
}}

.swdm-brand-mark {{
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    color: var(--bg-primary);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent-2) 72%, white));
    box-shadow: 0 0 28px color-mix(in srgb, var(--accent) 23%, transparent);
}}

.swdm-brand strong {{
    display: block;
    color: var(--text-primary);
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0;
    line-height: 1.2;
}}

.swdm-brand span {{
    display: block;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 10px;
    line-height: 1.4;
}}

.swdm-nav-group {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: var(--space-lg) 0;
}}

.swdm-nav-label {{
    margin: 0 0 4px 3px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 650;
    letter-spacing: .12em;
    text-transform: uppercase;
}}

.swdm-nav-item {{
    width: 100%;
    border: 0;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--text-secondary);
    text-decoration: none !important;
    display: grid;
    grid-template-columns: 28px 1fr auto;
    align-items: center;
    gap: 8px;
    padding: 8px 8px;
    text-align: left;
    cursor: pointer;
    font-size: 13px;
    transition: background var(--ease), color var(--ease), transform var(--ease);
}}

.swdm-nav-item:hover {{
    color: var(--text-primary);
    background: color-mix(in srgb, var(--surface-3) 72%, transparent);
    transform: translateX(2px);
}}

.swdm-nav-item.active {{
    color: var(--text-primary);
    background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 13%, transparent), color-mix(in srgb, var(--surface-3) 72%, transparent));
    box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 20%, transparent);
}}

.nav-ico {{
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: grid;
    place-items: center;
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    background: color-mix(in srgb, var(--accent) 7%, transparent);
    flex-shrink: 0;
}}

.swdm-nav-item.active .nav-ico {{
    background: color-mix(in srgb, var(--accent) 13%, transparent);
    box-shadow: 0 0 12px color-mix(in srgb, var(--accent) 18%, transparent);
}}

.swdm-nav-item strong {{
    color: currentColor;
    font-size: 12px;
    font-weight: 550;
}}

.swdm-nav-item small {{
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 600;
}}

.swdm-sidebar-footer {{
    margin-top: auto;
    padding-top: var(--space-lg);
    border-top: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}}

.sidebar-footer-btn {{
    width: 100%;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: color-mix(in srgb, var(--surface-3) 62%, transparent);
    color: var(--text-secondary);
    text-decoration: none !important;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 550;
    transition: background var(--ease), color var(--ease), border-color var(--ease);
}}

.sidebar-footer-btn:hover {{
    color: var(--text-primary);
    background: color-mix(in srgb, var(--surface-2) 72%, transparent);
    border-color: color-mix(in srgb, var(--accent) 20%, var(--border));
}}

/* ── MAIN CONTENT SHELL ── */
.st-key-dashboard_shell {{
    position: fixed;
    top: 16px;
    bottom: 16px;
    left: calc(var(--sidebar-w) + 56px);
    right: auto;
    width: calc(100vw - var(--sidebar-w) - 80px);
    max-height: calc(100vh - 32px);
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--space-lg) !important;
    margin: 0 !important;
}}

/* ── TYPOGRAPHY ── */
.stMarkdown h1, [data-testid="stHeading"] h1 {{
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-size: 38px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
    margin: 0 0 var(--space-xl) 0 !important;
}}

.stMarkdown h2, [data-testid="stHeading"] h2 {{
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-size: 30px !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
    line-height: 1.25 !important;
    margin: var(--space-2xl) 0 var(--space-xl) 0 !important;
}}

.stMarkdown h3, [data-testid="stHeading"] h3 {{
    color: var(--text-secondary) !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    margin: var(--space-lg) 0 var(--space-md) 0 !important;
}}

.stMarkdown p {{
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    margin-bottom: var(--space-md) !important;
}}

.stMarkdown code {{
    color: var(--accent) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    background: color-mix(in srgb, var(--accent) 7%, transparent) !important;
    padding: 2px 6px !important;
    border-radius: var(--radius-xs) !important;
}}

/* ── BUTTONS ── */
.stButton > button {{
    width: 100%;
    height: 41.8px;
    border: 0;
    border-radius: var(--radius-sm);
    background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent-2) 85%, white));
    color: var(--bg-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 650 !important;
    cursor: pointer;
    transition: transform var(--ease), box-shadow var(--ease);
    box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 18%, transparent);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 32px color-mix(in srgb, var(--accent) 24%, transparent);
}}

.stButton > button:active {{
    transform: translateY(0);
}}

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stFileUploader"] section,
[data-testid="stSlider"] {{
    color: var(--text-primary) !important;
}}

[data-testid="stSlider"] [data-testid="stTickBar"] {{
    display: none !important;
}}

[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {{
    min-height: 45px !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    background: var(--card-gradient-premium) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    line-height: 1.2 !important;
    padding: 4px 12px !important;
    align-items: center !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    min-height: 45px !important;
    align-items: center !important;
    border-radius: var(--radius-sm) !important;
    background: var(--card-gradient-premium) !important;
    color: {text_h} !important;
    overflow: hidden !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] input {{
    font-size: 11px !important;
    line-height: 1.2 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}}

[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] ul,
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="menu"],
[data-baseweb="menu"] ul,
[data-baseweb="menu"] li {{
    background: {card_bg} !important;
    color: {text_h} !important;
    border-color: {card_border} !important;
}}

[data-baseweb="popover"] {{
    border-radius: var(--radius-md) !important;
}}

[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="menu"] {{
    border: 1px solid {card_border} !important;
    border-radius: var(--radius-md) !important;
    box-shadow: {card_shadow} !important;
    overflow: hidden !important;
}}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover {{
    background: color-mix(in srgb, var(--accent) 12%, var(--surface-2)) !important;
    color: {text_h} !important;
}}

[data-baseweb="popover"] [role="option"] *,
[data-baseweb="popover"] li *,
[data-baseweb="menu"] li * {{
    color: {text_h} !important;
}}

[data-testid="stWidgetLabel"] p, .stSlider label p, .stSelectbox label p, .stTextInput label p {{
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .02em !important;
    margin-bottom: var(--space-sm) !important;
}}

[data-testid="stToggle"] label {{
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 550 !important;
}}

/* ── EXPANDERS ── */
[data-testid="stExpander"] {{
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: var(--card-gradient-premium) !important;
    overflow: hidden !important;
    box-shadow: {card_shadow} !important;
}}

[data-testid="stExpander"] summary {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    padding: var(--space-md) !important;
    background: transparent !important;
}}

[data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] summary:focus {{
    background: color-mix(in srgb, var(--accent) 8%, transparent) !important;
    outline: none !important;
}}

[data-testid="stExpander"] details,
[data-testid="stExpander"] [data-testid="stVerticalBlock"],
[data-testid="stExpanderDetails"],
[data-testid="stExpanderDetails"] > div {{
    color: var(--text-primary) !important;
}}

/* ── METRICS ── */
[data-testid="stMetric"] {{
    min-height: 105.6px;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: var(--card-gradient-premium) !important;
    padding: var(--space-lg) !important;
    box-shadow: {card_shadow} !important;
}}

[data-testid="stMetricDelta"] {{
    color: var(--accent) !important;
    background: color-mix(in srgb, var(--accent) 13%, transparent) !important;
    border-radius: 999px !important;
    width: fit-content !important;
    padding: 3px 8px !important;
}}

[data-testid="stMetricValue"] {{
    color: {text_h} !important;
    font-family: var(--font-display) !important;
    font-size: 28.6px !important;
    font-weight: 700 !important;
}}

[data-testid="stMetricLabel"] p {{
    color: {text_muted} !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    font-weight: 650 !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
}}

/* ── DATA FRAME ── */
[data-testid="stDataFrame"] {{
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    background: var(--card-gradient-premium) !important;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 5px !important;
    padding: 5px !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    background: var(--card-gradient-premium) !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
}}

.stTabs [data-baseweb="tab-border"] {{
    display: none !important;
}}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [role="tab"]::after {{
    display: none !important;
    opacity: 0 !important;
}}

.stTabs [data-baseweb="tab"] {{
    flex: 1 1 0 !important;
    justify-content: center !important;
    min-height: 32px !important;
    border-radius: 999px !important;
    color: {text_body} !important;
    font-family: var(--font-body) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 0 12px !important;
}}

.stTabs [aria-selected="true"] {{
    color: {text_h} !important;
    background: color-mix(in srgb, var(--surface-3) 78%, transparent) !important;
    border-bottom: 2px solid {accent_col} !important;
}}

/* ── CHARTS ── */
.js-plotly-plot {{
    border: 1px solid var(--border);
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    background: var(--chart-bg);
}}

/* ── CAPTIONS ── */
.stCaption, [data-testid="stCaptionContainer"] {{
    color: {text_muted} !important;
    font-size: 12px !important;
}}

/* ── CUSTOM HTML CARD COMPONENTS ── */
/* These use hardcoded colours for this theme because CSS vars
   may not cascade correctly into st.markdown-injected HTML */

.metric-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-lg);
    margin: var(--space-xl) 0 !important;
    width: 100%;
    padding: 0;
    box-sizing: border-box;
}}

.metric-card {{
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    min-height: 88px;
    justify-content: flex-end;
    box-shadow: {card_shadow};
}}

.metric-card strong {{
    color: {text_h};
    font-size: 24.2px;
    font-weight: 700;
    font-family: var(--font-display);
}}

.metric-card span {{
    color: {text_body};
    font-size: 10px;
    font-weight: 650;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.flow-strip {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: var(--card-gap);
    margin: var(--card-gap) 0;
}}

.flow-node {{
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    padding: var(--space-md);
    display: flex;
    flex-direction: column;
    gap: 4.4px;
    align-items: center;
    text-align: center;
    min-height: 77px;
    justify-content: center;
    box-shadow: {card_shadow};
}}

.flow-node strong {{
    color: {text_h};
    font-size: 13.2px;
    font-weight: 650;
}}

.flow-node small {{
    color: {accent_col};
    font-size: 9.9px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
}}

.status-chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: var(--card-gap);
    margin: var(--card-gap) 0;
}}

.status-chip {{
    display: inline-block;
    border: 1px solid {accent_bdr};
    border-radius: 999px;
    background: {accent_bg};
    color: {accent_col};
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 650;
}}

.status-chip.off {{
    background: color-mix(in srgb, var(--text-muted) 8%, transparent);
    color: var(--text-muted);
    border-color: color-mix(in srgb, var(--text-muted) 20%, var(--border));
}}

.section-heading {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-lg);
    padding: var(--space-lg);
    margin-bottom: var(--card-gap);
}}

.workstation-panel,
.st-key-active_run_panel,
.st-key-benchmark_suite_panel {{
    border: 1px solid {card_border} !important;
    border-radius: var(--radius-lg) !important;
    background: {card_bg} !important;
    padding: var(--space-lg) var(--space-xl) !important;
    margin-bottom: var(--space-xl) !important;
    box-shadow: {card_shadow} !important;
}}

.simulator-intro {{
    border: 1px solid {card_border};
    border-radius: var(--radius-lg);
    background: {card_bg};
    padding: var(--space-lg) var(--space-xl);
    margin-bottom: var(--space-xl);
    box-shadow: {card_shadow};
}}

.simulator-intro h2 {{
    color: {text_h};
    font-size: 34px;
    font-weight: 700;
    margin: 0 0 var(--space-md);
}}

.simulator-intro p {{
    color: {text_body};
    font-size: 15px;
    line-height: 1.65;
    margin: 0;
}}

.panel-section-title {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-lg);
    margin: 0;
}}

.panel-section-title h2 {{
    margin: 0 !important;
}}

.panel-section-title p {{
    margin: 0 !important;
}}

.contact-grid {{
    display: flex;
    flex-direction: column;
    gap: var(--card-gap);
    margin-bottom: var(--card-gap);
}}

.contact-card {{
    display: flex;
    align-items: center;
    gap: var(--space-md);
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    padding: var(--space-lg);
    text-decoration: none !important;
    box-shadow: {card_shadow};
    transition: border-color var(--ease), transform var(--ease);
}}

.contact-card:hover {{
    border-color: {accent_bdr};
    transform: translateY(-1px);
}}

.contact-icon {{
    width: 32px;
    height: 32px;
    border-radius: var(--radius-sm);
    display: grid;
    place-items: center;
    color: {accent_col};
    background: {accent_bg};
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    flex-shrink: 0;
}}

.contact-card strong {{
    display: block;
    color: {text_h};
    font-size: 13px;
    font-weight: 600;
}}

.contact-card small {{
    display: block;
    color: {text_muted};
    font-family: var(--font-mono);
    font-size: 10px;
    margin-top: 2px;
}}

.theme-pill {{
    border: 1px solid color-mix(in srgb, var(--accent) 28%, var(--border));
    border-radius: var(--radius-sm);
    background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent-2) 78%, white));
    color: var(--bg-primary) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 40px;
    padding: 9px 12px;
    text-decoration: none !important;
    font-size: 12px;
    font-weight: 750;
    transition: transform var(--ease), box-shadow var(--ease);
    box-shadow: 0 2px 8px color-mix(in srgb, var(--accent) 18%, transparent);
}}

.theme-pill:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 12px color-mix(in srgb, var(--accent) 24%, transparent);
}}

.developer-credit {{
    color: {text_muted};
    font-size: 11px;
    line-height: 1.5;
    margin: 0;
    text-align: center;
}}

.developer-credit a {{
    color: {accent_col};
    font-weight: 700;
    text-decoration: none;
}}

.developer-credit a:hover {{
    text-decoration: underline;
}}

.publisher-footer {{
    color: {accent_col};
    font-family: var(--font-mono);
    font-size: 11px;
}}

.soft-card {{
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    box-shadow: {card_shadow};
}}

.block-card {{
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
    box-shadow: {card_shadow};
}}

.soft-card h3,
.block-card h3 {{
    color: {text_h};
    font-size: 15px;
    font-weight: 650;
    margin: 0 0 var(--space-sm) 0;
}}

.soft-card p,
.block-card p {{
    color: {text_body};
    font-size: 13px;
    line-height: 1.55;
    margin: 0;
}}

.soft-card small {{
    color: {accent_col};
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.block-tag {{
    display: inline-block;
    width: fit-content;
    border: 1px solid {accent_bdr};
    border-radius: var(--radius-xs);
    background: {accent_bg};
    color: {accent_col};
    padding: 4px 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.param-list {{
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}}

.param-row {{
    display: flex;
    justify-content: space-between;
    gap: var(--space-md);
    border-top: 1px solid {card_border};
    padding-top: var(--space-xs);
    color: {text_body};
    font-size: 12px;
}}

.param-row b {{
    color: {text_h};
    font-weight: 650;
}}

.theory-intro {{
    border: 1px solid {card_border};
    border-radius: var(--radius-lg);
    background: {card_bg};
    padding: var(--space-lg) var(--space-xl);
    margin: var(--space-xl) 0;
    box-shadow: {card_shadow};
}}

.theory-intro p {{
    color: {text_body};
    font-size: 15px;
    line-height: 1.65;
    margin: 0;
}}

.theory-intro strong {{
    color: {accent_col};
    font-weight: 700;
}}

/* ── SPACING HELPERS ── */
/* Vertical spacing between primary blocks in the main shell */
.st-key-dashboard_shell > [data-testid="stVerticalBlock"] {{
    gap: var(--space-xl) !important;
}}

.st-key-dashboard_shell [data-testid="stElementContainer"] {{
    margin-bottom: 0 !important;
}}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]),
[data-testid="stHorizontalBlock"]:has(.block-card),
[data-testid="stHorizontalBlock"]:has(.soft-card),
[data-testid="stHorizontalBlock"]:has(.contact-card),
[data-testid="stHorizontalBlock"]:has(.workstation-panel),
[data-testid="stHorizontalBlock"]:has(.st-key-active_run_panel),
[data-testid="stHorizontalBlock"]:has(.st-key-benchmark_suite_panel),
[data-testid="stHorizontalBlock"]:has(.st-key-simulation_hero_card) {{
    gap: var(--card-gap) !important;
}}

[data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]) {{
    gap: var(--space-lg) !important;
}}

div[style*="margin-bottom: 16px"][style*="border-left"] {{
    margin-bottom: 12px !important;
}}

/* ── TOGGLE AND CONTROL IMPROVEMENTS ── */
[data-testid="stToggle"] label {{
    color: {text_h} !important;
}}

[data-testid="stToggle"] [role="switch"] {{
    background-color: {accent_col} !important;
    border: 1px solid {accent_bdr} !important;
    box-shadow: inset 0 0 0 1px color-mix(in srgb, white 30%, transparent) !important;
}}

[data-testid="stToggle"] [role="switch"][aria-checked="false"] {{
    background-color: color-mix(in srgb, var(--accent) 32%, white) !important;
    border-color: color-mix(in srgb, var(--accent) 68%, var(--border)) !important;
    box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 22%, transparent), 0 2px 8px rgba(61, 157, 243, .16) !important;
}}

[data-testid="stToggle"] [role="switch"][aria-checked="false"] > div {{
    background-color: #ffffff !important;
    border: 1px solid color-mix(in srgb, var(--accent) 44%, var(--border)) !important;
    box-shadow: 0 1px 4px rgba(15, 35, 65, .18) !important;
}}

[data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input[aria-checked="false"]) > div:first-child {{
    background: color-mix(in srgb, var(--accent) 34%, white) !important;
    border: 1px solid color-mix(in srgb, var(--accent) 24%, var(--border)) !important;
    box-shadow: 0 2px 8px rgba(61, 157, 243, .10) !important;
}}

[data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input[aria-checked="false"]) > div:first-child > div {{
    background: #ffffff !important;
    border: 1px solid color-mix(in srgb, var(--accent) 48%, var(--border)) !important;
    box-shadow: 0 1px 5px rgba(15, 35, 65, .22) !important;
}}

[data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input[aria-checked="false"]):hover > div:first-child {{
    background: color-mix(in srgb, var(--accent) 42%, white) !important;
    border-color: color-mix(in srgb, var(--accent) 34%, var(--border)) !important;
}}

.summary-table-card {{
    border: 1px solid {card_border};
    border-radius: var(--radius-md);
    background: {card_bg};
    box-shadow: {card_shadow};
    overflow: hidden;
}}

.summary-table {{
    width: 100%;
    border-collapse: collapse;
    color: {text_body};
    font-size: 12px;
}}

.summary-table th,
.summary-table td {{
    padding: 11px 14px;
    border-bottom: 1px solid {card_border};
    text-align: left;
}}

.summary-table th {{
    color: {text_h};
    background: color-mix(in srgb, var(--accent) 8%, transparent);
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.summary-table tr:last-child td {{
    border-bottom: 0;
}}

/* ── SIMULATION SECTION SPECIFIC STYLES ── */
.st-key-simulation_hero_card,
.st-key-active_run_panel,
.st-key-benchmark_suite_panel {{
    border: 1px solid {card_border} !important;
    border-radius: 24px !important;
    background: var(--card-gradient-premium) !important;
    padding: var(--space-xl) var(--space-2xl) !important;
    margin-bottom: 0 !important;
    box-shadow: {card_shadow} !important;
    overflow: visible !important;
}}

.simulation-panel {{
    border: 0;
    background: transparent;
    padding: 0;
    margin: 0;
}}

.simulation-hero {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-lg);
    margin-bottom: 0;
}}

.simulation-label {{
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin: 0 0 var(--space-xl) 0;
}}

.simulation-title {{
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-size: 42px !important;
    font-weight: 760 !important;
    letter-spacing: 0;
    line-height: 1.1 !important;
    margin: 0 !important;
    white-space: nowrap !important;
}}

.simulation-hero p {{
    color: var(--text-secondary);
    font-size: 16px;
    line-height: 1.62;
    margin: 0;
    width: 100%;
    text-align: justify;
    text-align-last: left;
}}

.st-key-simulation_controls {{
    border: 1px solid {card_border} !important;
    border-radius: 24px !important;
    background: var(--card-gradient-premium) !important;
    padding: var(--space-xl) var(--space-2xl) !important;
    margin-bottom: var(--space-xl) !important;
    box-shadow: {card_shadow} !important;
    overflow: visible !important;
}}

.st-key-simulation_controls > [data-testid="stVerticalBlock"] {{
    gap: 0 !important;
}}

.st-key-simulation_controls [data-testid="stHorizontalBlock"] {{
    align-items: flex-start !important;
    gap: var(--space-2xl) !important;
    margin: 0 !important;
    padding: 0 !important;
    flex-wrap: nowrap !important;
}}

.st-key-simulation_controls [data-testid="stColumn"] {{
    padding: 0 !important;
    min-width: 0 !important;
}}

.st-key-simulation_controls [data-testid="stWidgetLabel"] p,
.st-key-simulation_controls .stSlider label p,
.st-key-simulation_controls .stSelectbox label p {{
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    font-weight: 650 !important;
    letter-spacing: .02em !important;
    margin-bottom: var(--space-xl) !important;
}}

.st-key-simulation_controls [data-testid="stSlider"] {{
    margin-bottom: var(--space-2xl) !important;
}}

.st-key-simulation_controls [data-testid="stSlider"]:last-child {{
    margin-bottom: 0 !important;
}}

.st-key-simulation_controls [data-testid="stSelectbox"] {{
    margin-bottom: var(--space-2xl) !important;
}}

.st-key-simulation_controls [data-testid="stSelectbox"]:last-child {{
    margin-bottom: 0 !important;
}}

.st-key-simulation_controls .st-key-link_feature_toggles {{
    display: grid !important;
    grid-template-rows: 1fr 1fr 1fr !important;
    align-items: center !important;
    gap: 0 !important;
    padding-top: 61px !important;
    height: 218px !important;
    box-sizing: border-box !important;
}}

.st-key-simulation_controls .st-key-link_feature_toggles [data-testid="stElementContainer"] {{
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
}}

.st-key-simulation_controls [data-testid="stColumn"]:last-child,
.st-key-simulation_controls [data-testid="stColumn"]:nth-child(3) {{
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-end !important;
}}

.st-key-simulation_controls [data-testid="stColumn"]:last-child [data-testid="stElementContainer"],
.st-key-simulation_controls [data-testid="stColumn"]:nth-child(3) [data-testid="stElementContainer"] {{
    width: 100% !important;
    display: flex !important;
    justify-content: flex-end !important;
}}

.st-key-simulation_controls [data-testid="stColumn"]:nth-child(2),
.st-key-simulation_controls [data-testid="stColumn"]:nth-last-child(2) {{
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
}}

.st-key-simulation_controls [data-testid="stColumn"]:nth-child(2) [data-testid="stElementContainer"],
.st-key-simulation_controls [data-testid="stColumn"]:nth-last-child(2) [data-testid="stElementContainer"] {{
    width: 100% !important;
    display: flex !important;
    justify-content: flex-start !important;
}}

.st-key-simulation_controls [data-testid="stColumn"]:nth-child(2) [data-testid="stSelectbox"],
.st-key-simulation_controls [data-testid="stColumn"]:nth-last-child(2) [data-testid="stSelectbox"] {{
    width: 280px !important;
    margin-left: 90px !important;
}}

.st-key-adv_tx_params [data-testid="stColumn"],
.st-key-adv_tx_params [data-testid="stColumn"]:last-child,
.st-key-adv_tx_params [data-testid="stColumn"]:nth-child(3) {{
    display: block !important;
    flex-direction: initial !important;
    align-items: initial !important;
}}

.st-key-adv_tx_params [data-testid="stElementContainer"],
.st-key-adv_tx_params [data-testid="stColumn"]:last-child [data-testid="stElementContainer"],
.st-key-adv_tx_params [data-testid="stColumn"]:nth-child(3) [data-testid="stElementContainer"] {{
    display: block !important;
    justify-content: initial !important;
    width: 100% !important;
}}

.st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBar"],
.st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBarMin"],
.st-key-adv_tx_params [data-testid="stSlider"] [data-testid="stTickBarMax"] {{
    display: none !important;
}}

.st-key-simulation_controls .st-key-link_feature_toggles [data-testid="stElementContainer"]:nth-child(3) {{
    align-self: end !important;
    margin-bottom: -20px !important;
}}

.st-key-simulation_controls [data-testid="stCheckbox"] label[data-baseweb="checkbox"] {{
    gap: var(--space-lg) !important;
    justify-content: flex-end !important;
    width: 100% !important;
}}

.st-key-simulation_controls [data-testid="stCheckbox"] label[data-baseweb="checkbox"] > div:first-child {{
    transform: scale(1.15);
    transform-origin: left center;
}}

.st-key-simulation_controls [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p {{
    color: var(--text-primary) !important;
    font-size: 15px !important;
    font-weight: 550 !important;
    margin: 0 !important;
    min-width: 150px;
}}

.sim-run-row {{
    display: grid;
    grid-template-columns: 1fr 1fr 1.6fr 1.6fr;
    gap: var(--space-lg);
    align-items: center;
    margin: 0 0 var(--space-xl) 0;
}}

.st-key-sim_run_row [data-testid="stHorizontalBlock"] {{
    gap: var(--space-lg) !important;
    align-items: center !important;
}}

.st-key-sim_run_row [data-testid="stColumn"] {{
    padding: 0 !important;
}}

.st-key-sim_run_row [data-testid="stColumn"]:nth-child(3),
.st-key-sim_run_row [data-testid="stColumn"]:nth-child(4) {{
    display: flex !important;
    justify-content: flex-end !important;
}}

.st-key-sim_run_row [data-testid="stColumn"]:nth-child(3) [data-testid="stElementContainer"],
.st-key-sim_run_row [data-testid="stColumn"]:nth-child(4) [data-testid="stElementContainer"] {{
    width: auto !important;
}}

/* ── FILE UPLOADER VISIBILITY ── */
[data-testid="stFileUploader"] button {{
    background-color: var(--accent) !important;
    color: var(--bg-primary) !important;
    border: 1px solid var(--accent) !important;
    font-weight: 600 !important;
}}

[data-testid="stFileUploader"] button:hover {{
    background-color: var(--accent-2) !important;
    box-shadow: 0 4px 12px color-mix(in srgb, var(--accent) 25%, transparent) !important;
}}

[data-testid="stFileUploaderDropzone"] {{
    border: 2px dashed var(--border-strong) !important;
    background: color-mix(in srgb, var(--accent) 4%, transparent) !important;
    color: var(--text-primary) !important;
}}

/* ── RESPONSIVE ── */
@media (max-width: 1180px) {{
    :root {{ --sidebar-w: 220px; }}
    .block-container {{ padding-left: calc(var(--sidebar-w) + 32px) !important; }}
    .st-key-dashboard_shell {{
        left: calc(var(--sidebar-w) + 48px) !important;
        width: calc(100vw - var(--sidebar-w) - 64px) !important;
    }}
    .flow-strip {{ grid-template-columns: repeat(6, 1fr); }}
}}

@media (max-width: 860px) {{
    :root {{ --sidebar-w: 100%; }}
    .swdm-sidebar {{
        left: 12px; right: 12px; top: 12px; bottom: auto;
        width: auto; height: auto; padding: 10px;
        border-radius: var(--radius-md);
    }}
    .metric-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .swdm-brand {{ padding-bottom: 10px; gap: 8px; }}
    .swdm-brand-mark {{ width: 32px; height: 32px; font-size: 10px; }}
    .swdm-brand strong {{ font-size: 13px; }}
    .swdm-nav-group {{
        flex-direction: row; overflow-x: auto; padding: 8px 0 0; gap: 3px;
    }}
    .swdm-nav-label, .swdm-sidebar-footer {{ display: none; }}
    .swdm-nav-item {{
        width: auto; min-width: 100px;
        grid-template-columns: 24px 1fr; padding: 6px; font-size: 11px;
    }}
    .nav-ico {{ width: 24px; height: 24px; font-size: 10px; }}
    .block-container {{ padding: 140px 12px 12px 12px !important; max-width: 100% !important; }}
    .st-key-dashboard_shell {{
        top: 140px !important; left: 12px !important;
        width: calc(100vw - 24px) !important;
    }}
    .section-heading, .panel-section-title {{
        flex-direction: column; align-items: flex-start;
    }}
    .simulation-panel {{ padding: var(--space-xl); }}
    .simulation-title {{ font-size: clamp(28px, 9vw, 38px) !important; white-space: normal !important; }}
}}

/* metric-grid 3-col variant */
.metric-grid[style*="grid-template-columns: repeat(3"] {{
    grid-template-columns: repeat(3, 1fr) !important;
}}

</style>
<div class="{cls} app-theme-root"></div>
<script>
    (function() {{
        // Apply theme class to <html> so CSS selectors work document-wide
        var html = window.parent.document.documentElement;
        html.classList.remove('dark-theme', 'light-theme');
        html.classList.add('{cls}');
        // Remove curtain
        setTimeout(function() {{
            var curtain = window.parent.document.getElementById('theme-curtain');
            if (curtain) {{
                curtain.style.transform = 'translateY(-200%)';
                setTimeout(function() {{ curtain.remove(); }}, 700);
            }}
        }}, 50);
    }})();
</script>
"""
    cleaned = re.sub(r"^\s+", "", raw.strip(), flags=re.MULTILINE)
    st.markdown(cleaned, unsafe_allow_html=True)
