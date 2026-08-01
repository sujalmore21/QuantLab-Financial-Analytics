"""
=========================================
Module  : performance.py
Project : QuantLab
Purpose : Portfolio Performance Metrics + Interactive Page
=========================================
"""

import pandas as pd
import streamlit as st

from config import TRADING_DAYS, STOCKS, RAW_DATA_DIR
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, ranked_returns_bar, price_line_chart,
    sidebar_brand, sidebar_foot, COLORS,
)


# ==========================================================
# Metrics (unchanged)
# ==========================================================

def total_return(df):
    """
    Calculate total return.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    float
    """

    if df.empty:
        raise ValueError("DataFrame is empty.")

    if "Close" not in df.columns:
        raise ValueError("'Close' column not found.")

    return (
        df["Close"].iloc[-1]
        /
        df["Close"].iloc[0]
        -
        1
    )


def annual_return(df):
    """
    Calculate annualized return (CAGR).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    float
    """

    if df.empty:
        raise ValueError("DataFrame is empty.")

    if "Close" not in df.columns:
        raise ValueError("'Close' column not found.")

    # Prefer actual dates if available
    if "Date" in df.columns:

        years = (
            (df["Date"].iloc[-1] - df["Date"].iloc[0]).days
            / 365.25
        )

    else:

        years = len(df) / TRADING_DAYS

    if years <= 0:
        raise ValueError("Invalid time period.")

    return (
        (1 + total_return(df))
        **
        (1 / years)
        -
        1
    )


# ==========================================================
# Data loading
# ==========================================================

@st.cache_data(show_spinner=False)
def load_stock_df(stock: str) -> pd.DataFrame:
    """Load a single stock's Date/Close series."""
    filepath = RAW_DATA_DIR / f"{stock}.csv"

    if not filepath.exists():
        raise FileNotFoundError(f"Missing market data file: {filepath}")

    df = pd.read_csv(filepath)

    if "Date" not in df.columns or "Close" not in df.columns:
        raise ValueError(f"Expected Date/Close columns in {stock}.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df[["Date", "Close"]].sort_values("Date").reset_index(drop=True)

    return df


@st.cache_data(show_spinner=False)
def build_performance_table():
    """Total return + annualized return for every tracked stock."""
    rows = []
    errors = []

    for stock in STOCKS:
        try:
            df = load_stock_df(stock)
            rows.append(
                {
                    "Stock": stock,
                    "Total Return %": total_return(df) * 100,
                    "Annual Return %": annual_return(df) * 100,
                }
            )
        except (FileNotFoundError, ValueError) as exc:
            errors.append(f"{stock}: {exc}")

    return pd.DataFrame(rows), errors


# ==========================================================
# Streamlit Page
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Performance",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Return Diagnostics",
)

perf_df, load_errors = build_performance_table()

sidebar_foot(f"{len(perf_df)} of {len(STOCKS)} assets loaded")

if load_errors:
    with st.expander(f"⚠️ {len(load_errors)} asset(s) failed to load", expanded=False):
        for e in load_errors:
            st.write(e)

if perf_df.empty:
    st.error("No performance data could be loaded. Check that your market data files exist under RAW_DATA_DIR.")
else:
    best_row = perf_df.loc[perf_df["Annual Return %"].idxmax()]
    worst_row = perf_df.loc[perf_df["Annual Return %"].idxmin()]
    avg_annual = perf_df["Annual Return %"].mean()

    # ---------------- KPI row ----------------
    st.write("")
    section_title("Snapshot", "Universe Performance Overview", icon="activity")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Top Performer", best_row["Stock"],
                  f"{best_row['Annual Return %']:+.2f}% annualized", "pos", icon="trending-up")
    with k2:
        kpi_card("Weakest Performer", worst_row["Stock"],
                  f"{worst_row['Annual Return %']:+.2f}% annualized",
                  "neg" if worst_row["Annual Return %"] < 0 else "pos", icon="trending-down")
    with k3:
        kpi_card("Average Annual Return", f"{avg_annual:+.2f}%",
                  "across tracked universe", "pos" if avg_annual >= 0 else "neg", icon="bar-chart")
    with k4:
        kpi_card("Tracked Assets", str(len(perf_df)), "with valid data", "neu", icon="layers")

    ruler_rule()

    # ---------------- Ranked bar chart ----------------
    section_title("Ranking", "Annualized Return by Asset", icon="bar-chart")

    st.markdown(
        '<div class="ql-card"><div class="ql-card-label">'
        'Gold = top performer &middot; green = positive &middot; red = negative'
        '</div>', unsafe_allow_html=True,
    )
    st.plotly_chart(
        ranked_returns_bar(perf_df),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    ruler_rule()

    # ---------------- Table + price explorer ----------------
    section_title("Detail", "Metrics Table & Price History", icon="file-text")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="ql-card"><div class="ql-card-label">All assets</div>', unsafe_allow_html=True)
        table = perf_df.sort_values("Annual Return %", ascending=False).reset_index(drop=True)
        st.dataframe(
            table.style.format({"Total Return %": "{:+.2f}%", "Annual Return %": "{:+.2f}%"}),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ql-card"><div class="ql-card-label">Price history</div>', unsafe_allow_html=True)
        selected_stock = st.selectbox("Select an asset", options=list(perf_df["Stock"]), label_visibility="collapsed")
        try:
            price_df = load_stock_df(selected_stock)
            st.plotly_chart(
                price_line_chart(price_df, label=selected_stock),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        except (FileNotFoundError, ValueError) as exc:
            st.warning(f"Could not load price history for {selected_stock}: {exc}")
        st.markdown("</div>", unsafe_allow_html=True)


footer("QuantLab · Quantitative Investment Analytics Platform")