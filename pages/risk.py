"""
=========================================
Module  : risk.py
Project : QuantLab
Purpose : Portfolio Risk Analytics + Interactive Page
=========================================
"""

import numpy as np
import pandas as pd
import streamlit as st

from config import TRADING_DAYS, RISK_FREE_RATE, STOCKS, RAW_DATA_DIR
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, risk_gradient_bar, drawdown_chart,
    sidebar_brand, sidebar_foot, COLORS,
)


# ==========================================================
# Risk Metrics (unchanged)
# ==========================================================

def _validate_returns(df):
    """
    Validate required column.
    """

    if "Daily Return" not in df.columns:
        raise ValueError("Daily Return column missing.")


def volatility(df):
    """
    Calculate daily volatility.

    Returns
    -------
    float
    """

    _validate_returns(df)

    return df["Daily Return"].std()


def annual_volatility(df):
    """
    Calculate annualized volatility.

    Formula:
    Daily volatility * sqrt(252)

    Returns
    -------
    float
    """

    return volatility(df) * np.sqrt(TRADING_DAYS)


def sharpe_ratio(df, risk_free_rate=RISK_FREE_RATE):
    """
    Calculate annual Sharpe Ratio.

    Formula:
    (Annual Return - Risk Free Rate) / Annual Volatility

    Returns
    -------
    float
    """

    _validate_returns(df)

    annual_return = df["Daily Return"].mean() * TRADING_DAYS
    annual_vol = annual_volatility(df)

    if annual_vol == 0:
        raise ValueError("Volatility cannot be zero.")

    return (annual_return - risk_free_rate) / annual_vol


def max_drawdown(df):
    """
    Calculate maximum portfolio drawdown.

    Returns
    -------
    float
    """

    _validate_returns(df)

    cumulative_returns = (1 + df["Daily Return"]).cumprod()
    rolling_peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_peak) / rolling_peak

    return drawdown.min()


def drawdown_series(df):
    """Full drawdown series (not just the min) — used for the underwater chart."""
    _validate_returns(df)

    cumulative_returns = (1 + df["Daily Return"]).cumprod()
    rolling_peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_peak) / rolling_peak

    return drawdown


# ==========================================================
# Data loading
# ==========================================================

@st.cache_data(show_spinner=False)
def load_stock_returns(stock: str) -> pd.DataFrame:
    """Load a single stock's Date/Close series and compute Daily Return."""
    filepath = RAW_DATA_DIR / f"{stock}.csv"

    if not filepath.exists():
        raise FileNotFoundError(f"Missing market data file: {filepath}")

    df = pd.read_csv(filepath)

    if "Date" not in df.columns or "Close" not in df.columns:
        raise ValueError(f"Expected Date/Close columns in {stock}.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df[["Date", "Close"]].sort_values("Date").reset_index(drop=True)
    df["Daily Return"] = df["Close"].pct_change()
    df = df.dropna(subset=["Daily Return"]).reset_index(drop=True)

    return df


@st.cache_data(show_spinner=False)
def build_risk_table():
    rows = []
    errors = []

    for stock in STOCKS:
        try:
            df = load_stock_returns(stock)
            rows.append(
                {
                    "Stock": stock,
                    "Annual Volatility %": annual_volatility(df) * 100,
                    "Sharpe Ratio": sharpe_ratio(df),
                    "Max Drawdown %": max_drawdown(df) * 100,
                }
            )
        except (FileNotFoundError, ValueError) as exc:
            errors.append(f"{stock}: {exc}")

    return pd.DataFrame(rows), errors


# ==========================================================
# Streamlit Page
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Risk",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Risk Analytics",
)

risk_df, load_errors = build_risk_table()

sidebar_foot(f"{len(risk_df)} of {len(STOCKS)} assets analyzed")

if load_errors:
    with st.expander(f"⚠️ {len(load_errors)} asset(s) failed to load", expanded=False):
        for e in load_errors:
            st.write(e)

if risk_df.empty:
    st.error("No risk data could be computed. Check that your market data files exist under RAW_DATA_DIR.")
else:
    safest_row = risk_df.loc[risk_df["Annual Volatility %"].idxmin()]
    riskiest_row = risk_df.loc[risk_df["Annual Volatility %"].idxmax()]
    worst_dd_row = risk_df.loc[risk_df["Max Drawdown %"].idxmin()]
    best_sharpe_row = risk_df.loc[risk_df["Sharpe Ratio"].idxmax()]

    # ---------------- KPI row ----------------
    st.write("")
    section_title("Snapshot", "Risk Overview", icon="alert-triangle")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Safest Asset", safest_row["Stock"],
                  f"{safest_row['Annual Volatility %']:.2f}% volatility", "pos", icon="shield")
    with k2:
        kpi_card("Riskiest Asset", riskiest_row["Stock"],
                  f"{riskiest_row['Annual Volatility %']:.2f}% volatility", "neg", icon="alert-triangle")
    with k3:
        kpi_card("Deepest Drawdown", worst_dd_row["Stock"],
                  f"{worst_dd_row['Max Drawdown %']:.2f}%", "neg", icon="trending-down")
    with k4:
        kpi_card("Best Risk-Adjusted", best_sharpe_row["Stock"],
                  f"Sharpe {best_sharpe_row['Sharpe Ratio']:.2f}", "pos", icon="target")

    ruler_rule()

    # ---------------- Risk ranking ----------------
    section_title("Ranking", "Annualized Volatility by Asset", icon="bar-chart")

    st.markdown(
        '<div class="ql-card"><div class="ql-card-label">'
        'Blue = lower risk &middot; red = higher risk'
        '</div>', unsafe_allow_html=True,
    )
    st.plotly_chart(
        risk_gradient_bar(risk_df),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    ruler_rule()

    # ---------------- Table + drawdown explorer ----------------
    section_title("Detail", "Metrics Table & Drawdown History", icon="waves")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="ql-card"><div class="ql-card-label">All assets</div>', unsafe_allow_html=True)
        table = risk_df.sort_values("Annual Volatility %").reset_index(drop=True)
        st.dataframe(
            table.style.format({
                "Annual Volatility %": "{:.2f}%",
                "Sharpe Ratio": "{:.2f}",
                "Max Drawdown %": "{:.2f}%",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ql-card"><div class="ql-card-label">Underwater drawdown</div>', unsafe_allow_html=True)
        selected_stock = st.selectbox("Select an asset", options=list(risk_df["Stock"]), label_visibility="collapsed")
        try:
            df = load_stock_returns(selected_stock)
            dd = drawdown_series(df) * 100
            st.plotly_chart(
                drawdown_chart(df["Date"], dd, label=selected_stock),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        except (FileNotFoundError, ValueError) as exc:
            st.warning(f"Could not load drawdown history for {selected_stock}: {exc}")
        st.markdown("</div>", unsafe_allow_html=True)


footer("QuantLab · Quantitative Investment Analytics Platform")