"""
=========================================
Module  : loader.py
Project : QuantLab
Purpose : Load market data from CSV files
=========================================
"""

from pathlib import Path

import pandas as pd

from config import RAW_DATA_DIR


def load_stock(symbol):
    """
    Load historical data for a stock.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g. AAPL)

    Returns
    -------
    pandas.DataFrame
        Historical stock data sorted by date.
    """

    filepath = RAW_DATA_DIR / f"{symbol}.csv"

    if not filepath.exists():
        raise FileNotFoundError(
            f"Stock data not found: {filepath}"
        )

    df = pd.read_csv(filepath)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort by Date
    df.sort_values(
        "Date",
        inplace=True
    )

    # Reset index
    df.reset_index(
        drop=True,
        inplace=True
    )

    return df