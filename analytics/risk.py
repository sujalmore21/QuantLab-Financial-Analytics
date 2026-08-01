"""
=========================================
Module  : risk.py
Project : QuantLab
Purpose : Portfolio Risk Analytics
=========================================
"""


import numpy as np

from config import (
    TRADING_DAYS,
    RISK_FREE_RATE
)


def _validate_returns(df):
    """
    Validate required column.
    """

    if "Daily Return" not in df.columns:
        raise ValueError(
            "Daily Return column missing."
        )



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

    return (
        volatility(df)
        *
        np.sqrt(TRADING_DAYS)
    )



def sharpe_ratio(
    df,
    risk_free_rate=RISK_FREE_RATE
):
    """
    Calculate annual Sharpe Ratio.

    Formula:
    (Annual Return - Risk Free Rate)
    / Annual Volatility

    Returns
    -------
    float
    """

    _validate_returns(df)

    annual_return = (
        df["Daily Return"].mean()
        *
        TRADING_DAYS
    )

    annual_vol = annual_volatility(df)

    if annual_vol == 0:
        raise ValueError(
            "Volatility cannot be zero."
        )

    return (
        annual_return - risk_free_rate
    ) / annual_vol



def max_drawdown(df):
    """
    Calculate maximum portfolio drawdown.

    Returns
    -------
    float
    """

    _validate_returns(df)

    cumulative_returns = (
        1 + df["Daily Return"]
    ).cumprod()


    rolling_peak = (
        cumulative_returns
        .cummax()
    )


    drawdown = (
        cumulative_returns
        -
        rolling_peak
    ) / rolling_peak


    return drawdown.min()