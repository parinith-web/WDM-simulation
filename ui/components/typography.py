from __future__ import annotations

import html
from ui.components.html import html_block


def section_header(kicker: str, title: str, copy: str = "") -> None:
    copy_html = f'<p>{html.escape(copy)}</p>' if copy else ""
    html_block(
        f"""
        <div class="section-heading">
            <div class="left">
                <span class="section-kicker">{html.escape(kicker)}</span>
                <h2>{html.escape(title)}</h2>
            </div>
            {copy_html}
        </div>
        """
    )
