from __future__ import annotations
import base64
from pathlib import Path

from ui.components import html_block


def render_publisher_section() -> None:
    avatar_path = Path(__file__).resolve().parents[2] / "assets" / "avatar.png"
    avatar_base64 = ""
    
    if avatar_path.exists():
        try:
            avatar_base64 = base64.b64encode(avatar_path.read_bytes()).decode()
        except Exception as e:
            print(f"Error loading avatar: {e}")
    
    avatar_img_tag = f'<img src="data:image/png;base64,{avatar_base64}" alt="Avatar" class="publisher-avatar">' if avatar_base64 else ""
    
    html_block(
        f"""
        <style>
            .swdm-page-wrap {{
                animation: swdm-enter 500ms cubic-bezier(.22,1,.36,1) both;
            }}
            @keyframes swdm-enter {{
                from {{ opacity: 0; transform: translateY(24px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}
            .publisher-section {{
                display: grid;
                grid-template-columns: minmax(320px, .9fr) minmax(340px, 1.1fr);
                gap: 52.8px;
                align-items: center;
                padding: 52.8px;
                background: linear-gradient(135deg, color-mix(in srgb, var(--surface-2) 88%, transparent), color-mix(in srgb, var(--surface) 92%, transparent));
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
            }}
            .publisher-copy {{
                display: flex;
                flex-direction: column;
                gap: 26.4px;
            }}
            .publisher-copy h2 {{
                font-size: 48px;
                font-weight: 700;
                margin: 0;
                color: var(--text-primary);
            }}
            .publisher-copy p {{
                font-size: 15px;
                line-height: 1.6;
                margin: 0;
                color: var(--text-secondary);
            }}
            .site-label {{
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: var(--accent);
                font-family: var(--font-mono);
                margin-bottom: 8.8px;
            }}
            .contact-grid {{
                display: flex;
                flex-direction: column;
                gap: 13.2px;
            }}
            .contact-card {{
                display: flex;
                align-items: center;
                gap: 13.2px;
                padding: 17.6px;
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                background: var(--card-gradient-premium);
                text-decoration: none !important;
                transition: all var(--ease);
            }}
            .contact-card:hover {{
                border-color: color-mix(in srgb, var(--accent) 34%, var(--border));
                transform: translateY(-2px);
            }}
            .contact-icon {{
                width: 40px;
                height: 40px;
                display: grid;
                place-items: center;
                border-radius: var(--radius-sm);
                background: color-mix(in srgb, var(--accent) 10%, transparent);
                color: var(--accent);
                font-weight: 700;
                flex-shrink: 0;
                font-size: 12px;
            }}
            .contact-card strong {{
                color: var(--text-primary);
                font-size: 13px;
                font-weight: 600;
                margin: 0;
            }}
            .contact-card small {{
                color: var(--text-muted);
                font-size: 10px;
                font-weight: 600;
            }}
            .publisher-footer {{
                font-size: 14px;
                font-weight: 600;
                color: var(--accent);
                font-family: var(--font-mono);
                margin-top: 17.6px;
                letter-spacing: 0.05em;
            }}
            .publisher-art {{
                position: relative;
                width: 100%;
                height: 100%;
                min-height: 400px;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }}
            .publisher-avatar {{
                width: min(100%, 620px);
                height: auto;
                object-fit: contain;
                max-height: min(62vh, 560px);
                display: block;
                margin: auto;
            }}
            @media (max-width: 860px) {{
                .publisher-section {{
                    grid-template-columns: 1fr;
                    padding: 26.4px;
                    gap: 26.4px;
                }}
                .publisher-art {{
                    min-height: 260px;
                }}
                .publisher-avatar {{
                    width: min(100%, 420px);
                    max-height: 360px;
                }}
            }}
        </style>
        <div class="swdm-page-wrap">
        <div id="publisher" class="section-anchor"></div>
        <section class="publisher-section">
            <div class="publisher-copy">
                <div class="site-label">05 / Publisher</div>
                <h2>Let's Connect</h2>
                <p>
                    I'm open to research collaborations, internships, and full-time roles in optical communication, 
                    AI/ML, and backend engineering. Feel free to reach out.
                </p>
                <div class="contact-grid">
                    <a class="contact-card" href="mailto:parinithreddymavurapu@gmail.com" target="_blank">
                        <span class="contact-icon">@</span>
                        <div>
                            <strong>Email</strong>
                            <small>parinithreddymavurapu@gmail.com</small>
                        </div>
                    </a>
                    <a class="contact-card" href="https://www.linkedin.com/in/parinith-reddy" target="_blank">
                        <span class="contact-icon">in</span>
                        <div>
                            <strong>LinkedIn</strong>
                            <small>linkedin.com/in/parinith-reddy</small>
                        </div>
                    </a>
                    <a class="contact-card" href="https://github.com/parinith-web" target="_blank">
                        <span class="contact-icon">gh</span>
                        <div>
                            <strong>GitHub</strong>
                            <small>github.com/parinith-web</small>
                        </div>
                    </a>
                </div>
                <div class="publisher-footer">New Delhi, India &bull; +91 83285 34237</div>
            </div>
            <div class="publisher-art">
                {avatar_img_tag}
            </div>
        </section>
        </div>
        """
    )
