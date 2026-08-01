"""
=========================================
Module  : optimizer.py
Project : QuantLab
Purpose : Portfolio Optimization Engine
=========================================
"""


from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    STOCKS,
    RAW_DATA_DIR
)


# ==========================================================
# Load Price Data
# ==========================================================

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


        df["Date"] = pd.to_datetime(
            df["Date"]
        )


        df = df[
            [
                "Date",
                "Close"
            ]
        ]


        df.rename(
            columns={
                "Close": stock
            },
            inplace=True
        )


        if price_data.empty:

            price_data = df

        else:

            price_data = price_data.merge(
                df,
                on="Date",
                how="inner"
            )


    price_data.sort_values(
        "Date",
        inplace=True
    )


    price_data.reset_index(
        drop=True,
        inplace=True
    )


    return price_data



# ==========================================================
# Calculate Returns Matrix
# ==========================================================

def calculate_returns_matrix(price_data):
    """
    Calculate daily returns
    for all assets.

    Parameters
    ----------
    price_data : pandas.DataFrame


    Returns
    -------
    pandas.DataFrame
    """


    if "Date" not in price_data.columns:

        raise ValueError(
            "Date column missing"
        )


    returns = price_data.copy()


    returns.set_index(
        "Date",
        inplace=True
    )


    returns = returns.pct_change()


    returns.dropna(
        inplace=True
    )


    return returns

# ==========================================================
# Covariance Matrix
# ==========================================================

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
        raise ValueError(
            "Returns data is empty."
        )


    covariance = (
        returns.cov()
        *
        252
    )


    return covariance



# ==========================================================
# Expected Returns
# ==========================================================

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
        raise ValueError(
            "Returns data is empty."
        )


    expected_returns = (
        returns.mean()
        *
        252
    )


    return expected_returns



# ==========================================================
# Generate Random Portfolios
# ==========================================================

def generate_random_portfolios(
    expected_returns,
    covariance_matrix,
    num_portfolios=5000,
    risk_free_rate=0.02
):
    """
    Generate random portfolios using
    Monte Carlo simulation.

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

        raise ValueError(
            "Number of portfolios must be positive."
        )


    np.random.seed(42)


    portfolio_results = []


    num_assets = len(
        expected_returns
    )


    for _ in range(num_portfolios):


        # Generate random weights

        weights = np.random.random(
            num_assets
        )


        # Normalize weights

        weights = (
            weights /
            np.sum(weights)
        )


        # Expected return

        portfolio_return = np.dot(
            weights,
            expected_returns
        )


        # Portfolio risk

        portfolio_risk = np.sqrt(
            np.dot(
                weights.T,
                np.dot(
                    covariance_matrix,
                    weights
                )
            )
        )


        # Sharpe ratio

        if portfolio_risk == 0:

            sharpe = 0

        else:

            sharpe = (
                portfolio_return
                -
                risk_free_rate
            ) / portfolio_risk



        portfolio_results.append(
            {
                "weights": weights,

                "return": portfolio_return,

                "risk": portfolio_risk,

                "sharpe": sharpe
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
        raise ValueError(
            "Portfolio list is empty."
        )


    best_portfolio = max(
        portfolios,
        key=lambda x: x["sharpe"]
    )


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
        raise ValueError(
            "Portfolio list is empty."
        )


    minimum_risk_portfolio = min(
        portfolios,
        key=lambda x: x["risk"]
    )


    return minimum_risk_portfolio



# ==========================================================
# Complete Optimization Pipeline
# ==========================================================

def optimize_portfolio():
    """
    Complete portfolio optimization pipeline.

    Flow:

    Load Prices
        ↓
    Calculate Returns
        ↓
    Covariance Matrix
        ↓
    Expected Returns
        ↓
    Monte Carlo Simulation
        ↓
    Best Portfolios


    Returns
    -------
    tuple

        (
            max_sharpe_portfolio,
            min_risk_portfolio
        )
    """


    # Load market prices

    prices = load_prices()



    # Calculate daily returns

    returns = calculate_returns_matrix(
        prices
    )



    # Covariance

    covariance = calculate_covariance_matrix(
        returns
    )



    # Expected returns

    expected_returns = calculate_expected_returns(
        returns
    )



    # Generate portfolios

    portfolios = generate_random_portfolios(
        expected_returns,
        covariance
    )



    # Best Sharpe

    max_sharpe = find_max_sharpe(
        portfolios
    )



    # Lowest Risk

    min_risk = find_min_volatility(
        portfolios
    )



    return (
        max_sharpe,
        min_risk
    )