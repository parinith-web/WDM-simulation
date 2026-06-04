from __future__ import annotations

import html
import streamlit as st

from ui.components.html import html_block


def metric_cards(items: list[tuple[str, str]]) -> None:
    """Render a horizontal row of metric cards.

    The grid uses theme.py's .metric-grid styles (4-col default).
    For 2 or 3 items an inline style is emitted so theme.py's
    attribute-selector variant fires correctly.
    """
    n = len(items)
    if n == 3:
        grid_style = ' style="grid-template-columns: repeat(3, 1fr);"'
    elif n == 2:
        grid_style = ' style="grid-template-columns: repeat(2, 1fr);"'
    elif n == 1:
        grid_style = ' style="grid-template-columns: 1fr;"'
    else:
        grid_style = ""  # 4-col default defined in theme.py

    cards = "".join(
        f"""
        <div class="metric-card">
            <strong>{html.escape(value)}</strong>
            <span>{html.escape(label)}</span>
        </div>
        """
        for value, label in items
    )
    html_block(f'<div class="metric-grid"{grid_style}>{cards}</div>')


def signal_flow() -> None:
    nodes = [
        ("TX", "PRBS"),
        ("SEC", "RC4"),
        ("TX", "NRZ"),
        ("TX", "MZM"),
        ("CH", "WDM"),
        ("CH", "SMF/EDFA/DCF"),
        ("RX", "PIN"),
        ("RX", "Bessel + 3R"),
        ("QA", "BER/Q"),
    ]
    markup = "".join(
        f'<div class="flow-node"><small>{html.escape(tag)}</small><strong>{html.escape(name)}</strong></div>'
        for tag, name in nodes
    )
    html_block(f'<div class="flow-strip">{markup}</div>')


def status_chips(items: list[tuple[str, bool]]) -> None:
    chips = "".join(
        f'<span class="status-chip {"" if enabled else "off"}">{html.escape(label)}</span>'
        for label, enabled in items
    )
    html_block(f'<div class="status-chip-row">{chips}</div>')


def info_card(title: str, content: str, tag: str = "") -> None:
    tag_html = f'<small>{html.escape(tag)}</small>' if tag else ""
    html_block(
        f"""
        <article class="soft-card">
            {tag_html}
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(content)}</p>
        </article>
        """
    )


def block_card(name: str, tag: str, tag_class: str, desc: str, params: dict[str, str] | None = None) -> None:
    rows = ""
    if params:
        rows = "".join(
            f'<div class="param-row"><span>{html.escape(k)}</span><b>{html.escape(v)}</b></div>'
            for k, v in params.items()
        )
    html_block(
        f"""
        <article class="block-card">
            <span class="block-tag {html.escape(tag_class)}">{html.escape(tag)}</span>
            <h3>{html.escape(name)}</h3>
            <p>{html.escape(desc)}</p>
            <div class="param-list">{rows}</div>
        </article>
        """
    )


def system_params_table() -> None:
    rows = [
        ("PRBS Generator", "Bit rate", "10 Gbps / channel"),
        ("WDM", "Channels", "8, 1550.0-1552.8 nm"),
        ("CW Laser", "Launch power", "10 dBm"),
        ("MZM", "Extinction ratio", "30 dB"),
        ("SSMF", "Attenuation", "0.2 dB/km"),
        ("SSMF", "Dispersion", "16.75 ps/nm/km"),
        ("DCF", "Dispersion", "-85 ps/nm/km"),
        ("EDFA", "Noise figure", "3 dB"),
        ("PIN", "Responsivity", "1 A/W"),
        ("Bessel Filter", "Cutoff", "0.75 x bit rate"),
    ]
    st.dataframe(
        [{"Component": c, "Parameter": p, "Value": v} for c, p, v in rows],
        width="stretch",
        hide_index=True,
    )


def contact_card_html(icon: str, title: str, subtitle: str, href: str) -> str:
    return f"""
    <a class="contact-card" href="{html.escape(href)}" target="_blank">
        <span class="contact-icon">{html.escape(icon)}</span>
        <strong>{html.escape(title)}</strong>
        <small>{html.escape(subtitle)}</small>
    </a>
    """
