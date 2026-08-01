"""
=========================================
Module  : portfolio.py
Project : QuantLab
Purpose : Portfolio Holdings & Allocation Page
=========================================
"""

import pandas as pd
import streamlit as st

from services.portfolio_service import PortfolioService
from config import STOCKS
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, allocation_donut, comparison_bar,
    sidebar_brand, sidebar_foot, COLORS,
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Portfolio",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Holdings & Allocation",
)


# ==========================================================
# Load Portfolios
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_service():
    return PortfolioService()


service = get_service()

try:
    with st.spinner("Loading optimized portfolios..."):
        best = service.get_best_portfolio()
        low_risk = service.get_low_risk_portfolio()
except Exception as exc:
    st.error(f"Could not load portfolios: {exc}")
    st.stop()

sidebar_foot(f"{len(STOCKS)} assets under management")


def to_alloc_df(portfolio):
    df = pd.DataFrame({"Stock": STOCKS, "Weight": portfolio["weights"]})
    df["Weight %"] = df["Weight"] * 100
    return df.sort_values("Weight %", ascending=False).reset_index(drop=True)


# ==========================================================
# Portfolio Selector
# ==========================================================

st.write("")
section_title("Selection", "Choose an Allocation to Inspect", icon="briefcase")

view = st.radio(
    "Active portfolio",
    ["Optimal (Max Sharpe)", "Minimum Risk"],
    horizontal=True,
    label_visibility="collapsed",
)
active = best if view == "Optimal (Max Sharpe)" else low_risk
active_label = "optimal" if view == "Optimal (Max Sharpe)" else "minimum-risk"

ruler_rule()


# ==========================================================
# KPI Section
# ==========================================================

section_title("Snapshot", f"Active Portfolio — {view}", icon="target")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Expected Return", f"{active['return']:.2%}", "annualized", "neu", icon="trending-up")
with k2:
    kpi_card("Portfolio Risk", f"{active['risk']:.2%}", "annualized volatility", "neu", icon="activity")
with k3:
    kpi_card("Sharpe Ratio", f"{active['sharpe']:.2f}", "risk-adjusted return", "neu", icon="target")
with k4:
    kpi_card("Holdings", str(len(STOCKS)), "positions in portfolio", "neu", icon="layers")

ruler_rule()


# ==========================================================
# Allocation Detail
# ==========================================================

section_title("Allocation", f"{view} — Weights & Distribution", icon="pie-chart")

alloc_df = to_alloc_df(active)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="ql-card"><div class="ql-card-label">Holdings</div>', unsafe_allow_html=True)
    st.dataframe(
        alloc_df[["Stock", "Weight %"]].style.format({"Weight %": "{:.2f}%"}),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download holdings (CSV)",
        data=alloc_df[["Stock", "Weight %"]].to_csv(index=False),
        file_name=f"quantlab_{active_label}_portfolio.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ql-card"><div class="ql-card-label">Distribution</div>', unsafe_allow_html=True)
    st.plotly_chart(
        allocation_donut(alloc_df),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

ruler_rule()


# ==========================================================
# Comparison
# ==========================================================

section_title("Comparison", "Optimal vs. Minimum Risk, by Asset", icon="scale")

best_df = to_alloc_df(best)
low_risk_df = to_alloc_df(low_risk).set_index("Stock").loc[best_df["Stock"]].reset_index()

st.markdown(
    '<div class="ql-card"><div class="ql-card-label">'
    'Gold = optimal weights &middot; blue = minimum-risk weights'
    '</div>', unsafe_allow_html=True,
)
st.plotly_chart(
    comparison_bar(best_df, low_risk_df),
    use_container_width=True,
    config={"displayModeBar": False},
)
st.markdown("</div>", unsafe_allow_html=True)


footer("QuantLab · Quantitative Investment Analytics Platform")