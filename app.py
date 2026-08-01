"""
=========================================
Application : QuantLab
Purpose     : Main Streamlit Entry
=========================================
"""

import streamlit as st

from theme import (
    inject_css, ticker_header, ruler_rule, pill, footer, COLORS,
    sidebar_brand, sidebar_foot, icon_svg,
)


# =========================================
# Page Configuration
# =========================================

st.set_page_config(
    page_title="QuantLab",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()
sidebar_foot("Data refreshed on load")


# =========================================
# Header
# =========================================

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Institutional Portfolio Intelligence",
)

st.markdown(
    f"""
    <div style="margin-top: 22px; margin-bottom: 6px;">
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem;
        letter-spacing:0.16em; text-transform:uppercase; color:{COLORS['gold']};">
        Platform Overview</span>
    </div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.7rem;
    font-weight:600; color:{COLORS['text']}; margin-bottom:10px;">
        Built for the desk, not the deck.
    </div>
    <div style="max-width:640px; color:{COLORS['muted']}; font-size:0.95rem; line-height:1.6;">
        QuantLab turns Modern Portfolio Theory and Monte Carlo optimization into
        allocations you can act on — expected return, risk, and Sharpe ratio for
        every candidate portfolio, refreshed on demand.
    </div>
    """,
    unsafe_allow_html=True,
)

ruler_rule()


# =========================================
# Module Pills
# =========================================

st.markdown(
    f'<div class="ql-eyebrow">Modules</div>'
    f'<div class="ql-section-title">Explore the platform</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    pill(
        title="Market Analytics",
        body="Stock price history, return distributions, and correlation across the tracked universe.",
        accent=COLORS["blue"],
        icon="bar-chart",
    )

with col2:
    pill(
        title="Portfolio Optimization",
        body="Efficient-frontier search under Modern Portfolio Theory to surface the optimal allocation.",
        accent=COLORS["gold"],
        icon="scale",
    )

with col3:
    pill(
        title="Risk Management",
        body="Volatility, Sharpe ratio, and drawdown diagnostics for every candidate portfolio.",
        accent=COLORS["red"],
        icon="alert-triangle",
    )

st.write("")

st.info("Use the sidebar to open the **Dashboard** and view the current optimal and minimum-risk allocations.")

footer("QuantLab · Quantitative Investment Analytics Platform")