"""
=========================================
Module  : dashboard.py
Project : QuantLab
Purpose : Executive Dashboard — Power BI-style dense, filter-driven
          overview: KPIs + allocation + correlation + growth charts,
          all reacting to the same global filter bar.
=========================================
"""

import numpy as np
import pandas as pd
import streamlit as st

from services.portfolio_service import PortfolioService
from analytics.optimizer import generate_random_portfolios, find_max_sharpe, find_min_volatility
from config import STOCKS, RAW_DATA_DIR, TRADING_DAYS, RISK_FREE_RATE
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, allocation_donut, comparison_bar,
    correlation_heatmap, indexed_price_chart,
    sidebar_brand, sidebar_foot, render_table, COLORS,
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Executive Dashboard",
)


# ==========================================================
# Data loading (prices for filters / heatmap / growth chart)
# ==========================================================

@st.cache_data(show_spinner=False)
def load_all_prices():
    """Wide DataFrame: Date + one Close column per tracked stock."""
    price_data = pd.DataFrame()

    for stock in STOCKS:
        filepath = RAW_DATA_DIR / f"{stock}.csv"
        if not filepath.exists():
            continue
        df = pd.read_csv(filepath)
        if "Date" not in df.columns or "Close" not in df.columns:
            continue
        df["Date"] = pd.to_datetime(df["Date"])
        df = df[["Date", "Close"]].rename(columns={"Close": stock})
        price_data = df if price_data.empty else price_data.merge(df, on="Date", how="inner")

    price_data.sort_values("Date", inplace=True)
    price_data.reset_index(drop=True, inplace=True)
    return price_data


@st.cache_resource(show_spinner=False)
def get_service():
    return PortfolioService()


# ==========================================================
# Live re-optimization for whatever is currently selected in
# the filter bar. Uses the SAME pure functions as the original
# analytics/optimizer.py — nothing about that file is changed.
# ==========================================================

@st.cache_data(show_spinner=False)
def optimize_for_selection(returns_df: pd.DataFrame, num_portfolios: int = 3000,
                            risk_free_rate: float = RISK_FREE_RATE):
    expected_returns = returns_df.mean() * TRADING_DAYS
    covariance = returns_df.cov() * TRADING_DAYS

    portfolios = generate_random_portfolios(
        expected_returns, covariance, num_portfolios=num_portfolios, risk_free_rate=risk_free_rate
    )
    best = find_max_sharpe(portfolios)
    low_risk = find_min_volatility(portfolios)
    return best, low_risk


def to_alloc_df(portfolio, stocks):
    df = pd.DataFrame({"Stock": stocks, "Weight": portfolio["weights"]})
    df["Weight %"] = df["Weight"] * 100
    return df.sort_values("Weight %", ascending=False).reset_index(drop=True)


all_prices = load_all_prices()
service = get_service()

try:
    with st.spinner("Loading full-universe optimum (fallback)..."):
        global_best = service.get_best_portfolio()
        global_low_risk = service.get_low_risk_portfolio()
except Exception as exc:
    st.error(f"Could not load portfolios: {exc}")
    st.stop()

sidebar_foot(f"{len(STOCKS)} assets under management")


# ==========================================================
# Global filter bar — drives every chart below
# ==========================================================

st.write("")
section_title("Filters", "Global View Controls", icon="sliders")

st.markdown('<div class="ql-card">', unsafe_allow_html=True)
f1, f2 = st.columns([2, 3])

with f1:
    date_min = all_prices["Date"].min().date()
    date_max = all_prices["Date"].max().date()
    date_range = st.date_input(
        "Date range", value=(date_min, date_max),
        min_value=date_min, max_value=date_max,
    )

with f2:
    selected_stocks = st.multiselect(
        "Assets in view", options=STOCKS, default=STOCKS,
    )
st.markdown("</div>", unsafe_allow_html=True)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_min, date_max

if not selected_stocks:
    selected_stocks = STOCKS

mask = (all_prices["Date"].dt.date >= start_date) & (all_prices["Date"].dt.date <= end_date)
filtered_prices = all_prices.loc[mask, ["Date"] + selected_stocks].reset_index(drop=True)
filtered_returns = filtered_prices[selected_stocks].pct_change().dropna()

ruler_rule()


# ==========================================================
# Resolve the ACTIVE portfolio for this run — recomputed live
# from the filtered selection when there's enough data to do
# so, otherwise falls back to the full-universe optimum.
# ==========================================================

is_full_selection = (
    set(selected_stocks) == set(STOCKS)
    and start_date == date_min
    and end_date == date_max
)

if filtered_returns.shape[0] < 30 or filtered_returns.shape[1] < 1:
    active_best, active_low_risk = global_best, global_low_risk
    active_stocks = STOCKS
    st.caption(
        "⚠️ Not enough data in this selection (need at least 30 trading days) — "
        "showing the full-universe optimum instead."
    )
elif is_full_selection:
    active_best, active_low_risk = global_best, global_low_risk
    active_stocks = STOCKS
else:
    with st.spinner("Re-optimizing for the selected assets and date range..."):
        active_best, active_low_risk = optimize_for_selection(filtered_returns)
    active_stocks = selected_stocks
    st.caption(
        f"🔄 Recomputed live for **{len(active_stocks)} asset(s)**, "
        f"**{start_date}** to **{end_date}** — {filtered_returns.shape[0]} trading days."
    )


# ==========================================================
# KPI row — reacts to the filter bar
# ==========================================================

section_title("Snapshot", "Optimal Portfolio Overview", icon="target")

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Expected Return", f"{active_best['return']:.2%}",
              f"{(active_best['return'] - active_low_risk['return']):+.2%} vs. min-risk", "pos",
              icon="trending-up")
with k2:
    kpi_card("Portfolio Risk", f"{active_best['risk']:.2%}",
              f"{(active_best['risk'] - active_low_risk['risk']):+.2%} vs. min-risk", "neg",
              icon="activity")
with k3:
    kpi_card("Sharpe Ratio", f"{active_best['sharpe']:.2f}", "risk-adjusted return", "neu",
              icon="target")
with k4:
    kpi_card("Assets in View", str(len(selected_stocks)), f"of {len(STOCKS)} tracked", "neu",
              icon="layers")

ruler_rule()


# ==========================================================
# Row 1 — Allocation donut + Optimal vs. Min-risk comparison
# ==========================================================

section_title("Allocation", "Optimal Portfolio Composition", icon="pie-chart")

r1c1, r1c2 = st.columns([1, 1])

best_df = to_alloc_df(active_best, active_stocks)
low_risk_df = to_alloc_df(active_low_risk, active_stocks).set_index("Stock").loc[best_df["Stock"]].reset_index()

with r1c1:
    st.markdown('<div class="ql-card"><div class="ql-card-label">Distribution</div>', unsafe_allow_html=True)
    st.plotly_chart(allocation_donut(best_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with r1c2:
    st.markdown(
        '<div class="ql-card"><div class="ql-card-label">'
        'Optimal vs. minimum-risk weights, by asset</div>', unsafe_allow_html=True,
    )
    st.plotly_chart(
        comparison_bar(best_df, low_risk_df),
        use_container_width=True, config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

ruler_rule()


# ==========================================================
# Row 2 — Growth chart (indexed to 100) — reacts to filters
# ==========================================================

section_title("Growth", "Indexed Performance — Selected Assets & Range", icon="trending-up")

if filtered_prices.empty or len(selected_stocks) == 0:
    st.warning("No data in the selected range/assets — widen the filters above.")
else:
    st.markdown(
        '<div class="ql-card"><div class="ql-card-label">'
        'Growth of 100, indexed to the start of the selected range &middot; '
        'drag the range slider or use the 1M/3M/6M/1Y buttons to zoom'
        '</div>', unsafe_allow_html=True,
    )
    st.plotly_chart(
        indexed_price_chart(filtered_prices, stocks=selected_stocks),
        use_container_width=True,
        config={"displayModeBar": True, "displaylogo": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

ruler_rule()


# ==========================================================
# Row 3 — Correlation heatmap — reacts to filters
# ==========================================================

section_title("Correlation", "Cross-Asset Return Correlation", icon="waves")

if filtered_returns.empty or filtered_returns.shape[1] < 2:
    st.warning("Select at least 2 assets to compute correlations.")
else:
    st.markdown(
        '<div class="ql-card"><div class="ql-card-label">'
        'Daily return correlation over the selected range &middot; '
        'gold = highly correlated, blue = inversely correlated'
        '</div>', unsafe_allow_html=True,
    )
    st.plotly_chart(
        correlation_heatmap(filtered_returns),
        use_container_width=True, config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

ruler_rule()


# ==========================================================
# Row 4 — Holdings table
# ==========================================================

section_title("Holdings", "Optimal Portfolio Weights", icon="briefcase")

render_table(best_df[["Stock", "Weight %"]], label="Weights", highlight_col="Weight %")


footer("QuantLab · Quantitative Investment Analytics Platform")