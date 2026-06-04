"""
ui/app.py -- Composition root for the Secure WDM product site.

Run with:
    streamlit run ui/app.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from ui.components import render_navbar
from ui.sections import (
    render_architecture_section,
    render_home_section,
    inject_hero_scripts,
    render_publisher_section,
    render_simulation_section,
    render_theory_section,
)
from ui.styles import inject_theme, inject_motion


st.set_page_config(
    page_title="Secure WDM Optical Simulator",
    page_icon="SW",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def init_state() -> None:
    requested_theme = st.query_params.get("theme")
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if requested_theme in ("dark", "light"):
        st.session_state.theme = requested_theme
    if st.session_state.theme not in ("dark", "light"):
        st.session_state.theme = "dark"
    # Active page: "home" | "simulation" | "theory" | "architecture" | "publisher"
    requested_page = st.query_params.get("page")
    valid_pages = {"home", "simulation", "theory", "architecture", "publisher"}
    if requested_page in valid_pages:
        st.session_state.page = requested_page
    else:
        st.session_state.setdefault("page", "simulation")
    st.session_state.setdefault("active_result", None)
    st.session_state.setdefault("benchmark_results", None)
    st.session_state.setdefault("sweeps", None)
    st.session_state.setdefault("active_cfg", None)


def main() -> None:
    init_state()
    inject_theme(st.session_state.theme)
    inject_motion()
    inject_hero_scripts()
    render_navbar(st.session_state.theme)

    page = st.session_state.get("page", "home")

    with st.container(key="dashboard_shell"):
        if page == "home":
            render_home_section()
        elif page == "simulation":
            render_simulation_section()
        elif page == "theory":
            render_theory_section()
        elif page == "architecture":
            render_architecture_section()
        elif page == "publisher":
            render_publisher_section()
        else:
            render_home_section()


if __name__ == "__main__":
    main()
