from __future__ import annotations

import html
import streamlit as st

from ui.components.html import html_block


def _href(page: str, theme: str) -> str:
    return f"?page={html.escape(page)}&theme={html.escape(theme)}"


def render_navbar(theme: str) -> None:
    is_dark = theme == "dark"
    next_theme = "light" if is_dark else "dark"
    current_page = st.session_state.get("page", "simulation")
    theme_label = "Light theme" if is_dark else "Dark theme"

    pages = [
        ("home", "Home", "01", "Intro"),
        ("simulation", "Simulation", "02", "Lab"),
        ("theory", "Theory", "03", "Model"),
        ("architecture", "Architecture", "04", "Stack"),
        ("publisher", "Publisher", "05", "Contact"),
    ]

    nav_items = "\n".join(
        f"""
        <a href="{_href(key, theme)}" target="_self" class="swdm-nav-item {'active' if current_page == key else ''}">
            <span class="nav-ico">{html.escape(icon)}</span>
            <strong>{html.escape(label)}</strong>
            <small>{html.escape(meta)}</small>
        </a>
        """
        for key, label, icon, meta in pages
    )

    html_block(
        f"""
        <aside class="swdm-sidebar" aria-label="Primary navigation">
            <div class="swdm-brand">
                <div class="swdm-brand-mark">PR</div>
                <div>
                    <strong>PR.dev</strong>
                    <span>Optical analytics</span>
                </div>
            </div>
            <nav class="swdm-nav-group">
                <div class="swdm-nav-label">Workspace</div>
                {nav_items}
            </nav>
            <div class="swdm-sidebar-footer">
                <a href="{_href(current_page, next_theme)}" target="_self" class="theme-pill sidebar-theme-pill">{html.escape(theme_label)}</a>
                <p class="developer-credit">
                    Developed by
                    <a href="https://github.com/parinith-web" target="_blank" rel="noopener noreferrer">Parinith Reddy</a>
                </p>
            </div>
        </aside>
        """
    )
