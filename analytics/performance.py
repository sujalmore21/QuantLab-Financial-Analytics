"""
=========================================
Module  : performance.py
Project : QuantLab
Purpose : Portfolio Performance Metrics
=========================================
"""

import pandas as pd

from config import TRADING_DAYS


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