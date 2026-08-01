"""
=========================================
Module  : optimizer.py
Project : QuantLab
Purpose : Portfolio Optimization Engine + Interactive Page
=========================================
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from config import STOCKS, RAW_DATA_DIR
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, allocation_donut, efficient_frontier_chart,
    sidebar_brand, sidebar_foot, COLORS,
)


# ==========================================================
# Load Price Data
# ==========================================================

@st.cache_data(show_spinner=False)
def load_prices():
    """
    Load closing prices of all configured stocks.

    Returns
    -------
    pandas.DataFrame

    Example:
        Date       AAPL    MSFT    NVDA
        2025-01-01 220     420     140
    """

    price_data = pd.DataFrame()

    for stock in STOCKS:

        filepath = RAW_DATA_DIR / f"{stock}.csv"

        if not filepath.exists():
            raise FileNotFoundError(
                f"Missing market data file: {filepath}"
            )

        df = pd.read_csv(filepath)

        if "Date" not in df.columns:
            raise ValueError(
                f"Date column missing in {stock}"
            )

        if "Close" not in df.columns:
            raise ValueError(
                f"Close column missing in {stock}"
            )

        df["Date"] = pd.to_datetime(df["Date"])

        df = df[["Date", "Close"]]

        df.rename(columns={"Close": stock}, inplace=True)

        if price_data.empty:
            price_data = df
        else:
            price_data = price_data.merge(df, on="Date", how="inner")

    price_data.sort_values("Date", inplace=True)
    price_data.reset_index(drop=True, inplace=True)

    return price_data


# ==========================================================
# Calculate Returns Matrix
# ==========================================================

@st.cache_data(show_spinner=False)
def calculate_returns_matrix(price_data):
    """
    Calculate daily returns for all assets.

    Parameters
    ----------
    price_data : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    if "Date" not in price_data.columns:
        raise ValueError("Date column missing")

    returns = price_data.copy()
    returns.set_index("Date", inplace=True)
    returns = returns.pct_change()
    returns.dropna(inplace=True)

    return returns


# ==========================================================
# Covariance Matrix
# ==========================================================

@st.cache_data(show_spinner=False)
def calculate_covariance_matrix(returns):
    """
    Calculate annualized covariance matrix.

    Parameters
    ----------
    returns : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    if returns.empty:
        raise ValueError("Returns data is empty.")

    covariance = returns.cov() * 252

    return covariance


# ==========================================================
# Expected Returns
# ==========================================================

@st.cache_data(show_spinner=False)
def calculate_expected_returns(returns):
    """
    Calculate annual expected returns.

    Parameters
    ----------
    returns : pandas.DataFrame

    Returns
    -------
    pandas.Series
    """

    if returns.empty:
        raise ValueError("Returns data is empty.")

    expected_returns = returns.mean() * 252

    return expected_returns


# ==========================================================
# Generate Random Portfolios
# ==========================================================

def generate_random_portfolios(
    expected_returns,
    covariance_matrix,
    num_portfolios=5000,
    risk_free_rate=0.02,
):
    """
    Generate random portfolios using Monte Carlo simulation.

    Parameters
    ----------
    expected_returns : pandas.Series
    covariance_matrix : pandas.DataFrame
    num_portfolios : int
    risk_free_rate : float

    Returns
    -------
    list
        Portfolio dictionaries
    """

    if num_portfolios <= 0:
        raise ValueError("Number of portfolios must be positive.")

    np.random.seed(42)

    portfolio_results = []

    num_assets = len(expected_returns)

    for _ in range(num_portfolios):

        # Generate random weights
        weights = np.random.random(num_assets)

        # Normalize weights
        weights = weights / np.sum(weights)

        # Expected return
        portfolio_return = np.dot(weights, expected_returns)

        # Portfolio risk
        portfolio_risk = np.sqrt(
            np.dot(weights.T, np.dot(covariance_matrix, weights))
        )

        # Sharpe ratio
        if portfolio_risk == 0:
            sharpe = 0
        else:
            sharpe = (portfolio_return - risk_free_rate) / portfolio_risk

        portfolio_results.append(
            {
                "weights": weights,
                "return": portfolio_return,
                "risk": portfolio_risk,
                "sharpe": sharpe,
            }
        )

    return portfolio_results


# ==========================================================
# Find Maximum Sharpe Portfolio
# ==========================================================

def find_max_sharpe(portfolios):
    """
    Find portfolio with highest Sharpe Ratio.

    Parameters
    ----------
    portfolios : list

    Returns
    -------
    dict
    """

    if not portfolios:
        raise ValueError("Portfolio list is empty.")

    best_portfolio = max(portfolios, key=lambda x: x["sharpe"])

    return best_portfolio


# ==========================================================
# Find Minimum Risk Portfolio
# ==========================================================

def find_min_volatility(portfolios):
    """
    Find portfolio with lowest risk.

    Parameters
    ----------
    portfolios : list

    Returns
    -------
    dict
    """

    if not portfolios:
        raise ValueError("Portfolio list is empty.")

    minimum_risk_portfolio = min(portfolios, key=lambda x: x["risk"])

    return minimum_risk_portfolio


# ==========================================================
# Complete Optimization Pipeline
# ==========================================================

def optimize_portfolio(num_portfolios=5000, risk_free_rate=0.02):
    """
    Complete portfolio optimization pipeline.

    Flow:
    Load Prices -> Calculate Returns -> Covariance Matrix
    -> Expected Returns -> Monte Carlo Simulation -> Best Portfolios

    Returns
    -------
    tuple
        (all_portfolios, max_sharpe_portfolio, min_risk_portfolio)
    """

    prices = load_prices()
    returns = calculate_returns_matrix(prices)
    covariance = calculate_covariance_matrix(returns)
    expected_returns = calculate_expected_returns(returns)

    portfolios = generate_random_portfolios(
        expected_returns, covariance, num_portfolios, risk_free_rate
    )

    max_sharpe = find_max_sharpe(portfolios)
    min_risk = find_min_volatility(portfolios)

    return portfolios, max_sharpe, min_risk


# ==========================================================
# ==========================================================
# Streamlit Page
# ==========================================================
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Optimizer",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Optimization Engine",
)

st.write("")
section_title("Monte Carlo", "Run the Optimizer", icon="sliders")

with st.form("optimizer_form"):
    c1, c2, c3 = st.columns([2, 2, 1])

    with c1:
        num_portfolios = st.slider(
            "Simulated portfolios", min_value=500, max_value=20000,
            value=5000, step=500,
        )

    with c2:
        risk_free_rate = st.slider(
            "Risk-free rate", min_value=0.0, max_value=0.10,
            value=0.02, step=0.005, format="%.1f%%",
        )

    with c3:
        st.write("")
        st.write("")
        run = st.form_submit_button("Run simulation", use_container_width=True)

if run or "ql_portfolios" not in st.session_state:
    try:
        with st.spinner("Simulating portfolios..."):
            portfolios, max_sharpe, min_risk = optimize_portfolio(
                num_portfolios=num_portfolios, risk_free_rate=risk_free_rate
            )
        st.session_state["ql_portfolios"] = portfolios
        st.session_state["ql_max_sharpe"] = max_sharpe
        st.session_state["ql_min_risk"] = min_risk
    except (FileNotFoundError, ValueError) as exc:
        st.error(f"Could not run the optimizer: {exc}")

sidebar_foot(f"{len(st.session_state.get('ql_portfolios', []))} portfolios in memory")

if "ql_portfolios" in st.session_state:

    portfolios = st.session_state["ql_portfolios"]
    max_sharpe = st.session_state["ql_max_sharpe"]
    min_risk = st.session_state["ql_min_risk"]

    ruler_rule()

    # ---------------- KPI row ----------------
    section_title("Results", "Best Candidates", icon="target")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Max Sharpe Return", f"{max_sharpe['return']:.2%}", "optimal candidate", "neu", icon="trending-up")
    with k2:
        kpi_card("Max Sharpe Risk", f"{max_sharpe['risk']:.2%}", "optimal candidate", "neu", icon="activity")
    with k3:
        kpi_card("Min Risk Return", f"{min_risk['return']:.2%}", "conservative candidate", "neu", icon="shield")
    with k4:
        kpi_card("Min Risk Risk", f"{min_risk['risk']:.2%}", "conservative candidate", "neu", icon="shield")

    ruler_rule()

    # ---------------- Efficient frontier ----------------
    section_title("Frontier", "Risk / Return Landscape", icon="scale")

    st.markdown('<div class="ql-card"><div class="ql-card-label">'
                f'{len(portfolios):,} simulated portfolios &middot; star = max Sharpe &middot; diamond = min risk'
                '</div>', unsafe_allow_html=True)
    st.plotly_chart(
        efficient_frontier_chart(portfolios, max_sharpe, min_risk),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    ruler_rule()

    # ---------------- Allocation breakdown ----------------
    section_title("Allocation", "Inspect a Candidate Portfolio", icon="pie-chart")

    view = st.radio(
        "Portfolio to inspect", ["Max Sharpe", "Minimum Risk"],
        horizontal=True, label_visibility="collapsed",
    )
    chosen = max_sharpe if view == "Max Sharpe" else min_risk

    alloc_df = pd.DataFrame({"Stock": STOCKS, "Weight": chosen["weights"]})
    alloc_df["Weight %"] = alloc_df["Weight"] * 100
    alloc_df = alloc_df.sort_values("Weight %", ascending=False).reset_index(drop=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="ql-card"><div class="ql-card-label">Weights</div>', unsafe_allow_html=True)
        st.dataframe(
            alloc_df[["Stock", "Weight %"]].style.format({"Weight %": "{:.2f}%"}),
            use_container_width=True,
            hide_index=True,
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

else:
    st.info("Set your parameters above and click **Run simulation** to generate the efficient frontier.")


footer("QuantLab · Quantitative Investment Analytics Platform")