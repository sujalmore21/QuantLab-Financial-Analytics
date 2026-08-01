"""
=========================================
Module  : returns.py
Project : QuantLab
Purpose : Portfolio Return Calculations
=========================================
"""

import pandas as pd


def calculate_daily_returns(df):
    """
    Calculate daily percentage returns.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    if "Close" not in df.columns:
        raise ValueError(
            "'Close' column not found."
        )

    df = df.copy()

    df["Daily Return"] = df["Close"].pct_change()

    return df


def calculate_cumulative_returns(df):
    """
    Calculate cumulative returns.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    df = df.copy()

    if "Daily Return" not in df.columns:
        df = calculate_daily_returns(df)

    df["Cumulative Return"] = (
        1 + df["Daily Return"]
    ).cumprod()

    return df