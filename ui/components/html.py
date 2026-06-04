"""Safe HTML rendering helpers.

All custom HTML passes through this module so raw tags are never sent to
`st.write` or plain markdown accidentally.

The key fix: Streamlit's markdown parser treats lines with 4+ spaces of
leading whitespace as code blocks (<pre><code>), even when
unsafe_allow_html=True. We must strip ALL leading whitespace from every
line before passing to st.markdown().
"""

from __future__ import annotations

import re

import streamlit as st


def html_block(markup: str) -> None:
    """Render a complete, self-contained HTML fragment.

    Strips all leading whitespace from every line to prevent Streamlit's
    markdown parser from converting indented HTML into code blocks.
    """
    cleaned = re.sub(r"^\s+", "", markup.strip(), flags=re.MULTILINE)
    st.markdown(cleaned, unsafe_allow_html=True)
